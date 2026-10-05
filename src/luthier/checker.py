"""Bidirectional type checker with subtypes and deferred obligations.

`infer(ctx, t)` returns the elaborated term and its type; `check(ctx, t, ty)`
returns the elaborated term. Elaboration resolves constructor names, turns
`a -> b` into Pi or implication, `a * b` into Sigma or multiplication, and
list literals into `nil`/`cons`.

A value checked against a subtype is checked against the base type and then:
if closed and the predicate evaluates to `true`, accepted; to `false`, rejected;
otherwise an obligation is recorded on the current definition, for `test`.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import importlib
import os
import sys

from .syntax import *
from .subst import subst, fresh, free_vars
from .pretty import pp, pp_pat
from .evaluator import (Env, ExternInfo, Fuel, whnf, conv, unapply, apply, as_bool, record_components,
                        EvalError, BUILTIN_TYPES, shaped, generator_key)


class TypeCheckError(Exception):
    pass


@dataclass
class Obligation:
    def_name: str
    params: list          # [(name, type)] local context where the check happened
    term: Term            # Bool-valued or law-valued, with the params free
    label: str


Ctx = list  # list[tuple[str, Term]]


def lookup(ctx: Ctx, name: str) -> Optional[Term]:
    for n, t in reversed(ctx):
        if n == name:
            return t
    return None


def pi_arity(ty: Term) -> int:
    n = 0
    while isinstance(ty, Pi):
        n += 1
        ty = ty.cod
    return n


def pattern_to_term(p: Pattern) -> Optional[Term]:
    if isinstance(p, PVar):
        return Var(p.name)
    if isinstance(p, PPair):
        a = pattern_to_term(p.fst)
        b = pattern_to_term(p.snd)
        return Pair(a, b) if a is not None and b is not None else None
    return None


class Checker:
    def __init__(self, env: Optional[Env] = None):
        self.env = env or Env()
        self.obligations: dict[str, list[Obligation]] = {}
        self.current_def: Optional[str] = None
        self.prefix: str = ""          # module prefix of the file being loaded ("" at top level)
        self.recording: bool = True    # whether checks against subtypes record obligations
        self.certified: dict = {}      # qualified name -> certificate entry accepted at import
        self.gens: dict = {}           # generator key (05 R7: aliases unfolded) -> ("luthier", label, term) | ("extern", target, None)
        self.gens_by: dict = {}        # generator key -> the name its `gen` was written on
        self.object_of: dict = {}      # qualified name -> the members of its object (a strongly connected component)
        self._operand_memo: dict = {}  # id of an operand -> (operand, context, whether it is a type)
        self.implicit_params: dict = {}  # qualified name -> how many leading parameters are implicit
        self._meta_names: set = set()     # the unknowns made for implicit parameters, all distinct
        self.operators: dict = {}      # op -> [(lhs type, rhs type, result type, function term)]
        self.labels: dict = {}         # label -> (alias name, index) for sums named by an alias; None if ambiguous
        self.kernel: bool = False      # loading core.lut: the kernel's own definitions (exempt from R4)
        self.provisional: dict = {}    # name -> [declared types it builds on], for `extern provisional`
        self.library: bool = False     # loading core.lut or a library of the distribution (lib/)
        self.axioms: dict = {}         # name -> description, for `axiom` (06 §3)
        self.path: list = []           # conditions of the enclosing `if` branches (Bool terms)
        self.lets: list = []           # (name, term): `match e { x -> ... }` binds x to e

    # ----------------------------------------------------------- namespaces
    def qualify(self, name: str) -> str:
        return f"{self.prefix}.{name}" if self.prefix else name

    def resolve(self, name: str) -> Optional[str]:
        """The qualified key a source name refers to: the current module first, then the globals."""
        for cand in ([self.qualify(name)] if self.prefix else []) + [name]:
            if cand in self.env.defs or cand in self.env.cons or cand in self.env.datas or cand in BUILTIN_TYPES:
                return cand
        return None

    # ------------------------------------------------------------ utilities
    def fuel(self) -> Fuel:
        return Fuel(self.env.fuel)

    def whnf(self, t: Term) -> Term:
        return whnf(self.env, t, self.fuel())

    def conv(self, a: Term, b: Term) -> bool:
        try:
            return conv(self.env, a, b, self.fuel())
        except EvalError:
            return False

    def err(self, msg: str):
        where = f"in {self.current_def}: " if self.current_def else ""
        raise TypeCheckError(where + msg)

    def is_unit(self, ty: Term) -> bool:
        w = self.whnf(ty)
        return isinstance(w, Var) and w.name == "Unit"

    def is_bool(self, ty: Term) -> bool:
        """`Bool` is `< true : Unit | false : Unit >`, by its labels: another sum of two units
        (`< wrong : Unit | right : Unit >`) is not a Bool, and its first alternative is not true."""
        w = self.whnf(self.base_type(ty))
        if isinstance(w, Var) and w.name == "Bool":
            return True
        return isinstance(w, Sum) and w.labels() == ["true", "false"] and all(self.is_unit(a) for _, a in w.alts)

    def sum_of(self, ty: Term) -> Optional[Sum]:
        w = self.whnf(self.base_type(ty))
        return w if isinstance(w, Sum) else None

    def strip_subtype(self, ty: Term) -> Optional[Term]:
        w = self.whnf(ty)
        return w.base if isinstance(w, Subtype) else None

    def base_type(self, ty: Term) -> Term:
        while True:
            b = self.strip_subtype(ty)
            if b is None:
                return ty
            ty = b

    def is_law(self, ty: Term) -> bool:
        w = self.whnf(ty)
        if isinstance(w, Var) and w.name in ("Bool", "Law"):
            return True
        if self.is_bool(w):
            return True
        if isinstance(w, Pi):
            return self.is_law(subst(w.cod, {w.name: Var(fresh(w.name))}))
        return False

    # -------------------------------------------------------------- program
    def load(self, prog: Program):
        """The whole file at once (05 §2): its entries are grouped by name, the dependency graph is
        built from the names each one mentions, and the objects (strongly connected components)
        are checked in an order where every dependency comes first."""
        from .graph import file_objects
        for d in prog.defs:
            if getattr(d, "implicit", 0):
                self.implicit_params[self.qualify(d.name)] = d.implicit
        for obj in file_objects(self, prog):
            self.load_object(obj)
        for g in prog.gens:
            self.add_gen(g)

    # ------------------------------------------------------------ objects
    def load_object(self, obj):
        """One object: first every declared base, then every law and value, then the types the
        laws define. Then the rules that need the object: R2."""
        members = obj.members
        names = {self.qualify(m.name) for m in members if m.kind != "operator"}
        for q in names:
            self.object_of[q] = sorted(names)     # 05 §7: `test n` runs every member of n's object
        # an operator directive goes first, unless its function is in this same object (the
        # function's own body uses the operator symbol on other types): then it goes last
        late_ops = [m for m in members if m.kind == "operator" and (m.refs & {x.name for x in members})]
        for m in members:
            if m.kind == "operator" and m not in late_ops:
                self.add_operator(m.defn)
            elif m.kind == "alias":
                self.add_alias(m)
        pending = [m for m in members if m.kind == "entry" and m.pending]
        for m in members:
            if m.kind != "entry":
                continue
            if m.pending:
                self.declare_pending(m)
            elif m.decl is not None and m.decl.type is not None and (m.defn is None or m.defn is not m.decl):
                self.add_def(Def(m.name, m.decl.type, None, line=m.decl.line))
            elif m.defn is not None and m.defn.type is not None and m.defn.data is None and len(members) > 1:
                # a complete definition in a cycle: its type first, so the others can use it
                self.add_def(Def(m.name, m.defn.type, None, line=m.defn.line))
        for m in members:
            if m.kind == "entry" and not m.pending and m.defn is not None:
                d = m.defn
                if m.decl is not None and m.decl is not d:
                    d = Def(m.name, d.type, d.body, data=d.data, line=d.line)
                self.add_def(d, object_names=names)
        for m in pending:
            if m.defn is not None:
                self.define_pending(m)
        for m in late_ops:
            self.add_operator(m.defn)
        for q in names:
            self.check_defined_types(q, names)

    def add_alias(self, m):
        """`name = term`: elaborated once; wherever the name is used it unfolds to the term. It has
        no states and cannot be declared or defined (05 R7)."""
        d = m.alias
        qname = self.qualify(d.name)
        self.current_def = qname
        try:
            if m.decl is not None or m.defn is not None:
                what = "defined" if m.defn is not None and m.defn.body is not None else "declared"
                self.err(f"{d.name} is an alias and cannot be {what}")
            if qname in self.env.defs:
                self.err(f"{d.name} is an alias and cannot be defined twice")
            body, ty = self.infer([], d.body)
            self.env.defs[qname] = Def(qname, ty, body, alias=True, line=d.line)
            self.register_labels(qname, body, ty)
            self.check_defined_types(qname, {qname})
        finally:
            self.current_def = None

    # ------------------------------------------------------------ declared types
    def declare_pending(self, m):
        """`T : base` whose body, given later in the same object, is a predicate: until then `T` is
        the labeled base, so the laws of the object can be written over its components."""
        qname = self.qualify(m.name)
        self.current_def = qname
        try:
            params, base_src = _peel_pi(m.decl.type)
            ctx: Ctx = []
            for n, t in params:
                ctx.append((n, self.check(ctx, t, Univ())))
            base = self.check(ctx, base_src, Univ())
            shape = base if (isinstance(base, Subtype) and isinstance(base.pred, NoLaw)) else \
                Subtype(PVar(fresh("x")), base, NoLaw())
            ty: Term = Univ()
            body: Term = shape
            for n, t in reversed(ctx):
                ty = Pi(n, t, ty)
                body = Lam(PVar(n), body, t)
            self.env.defs[qname] = Def(qname, ty, body, pending=True, line=m.decl.line)
            m.base_ctx, m.base = ctx, base
        finally:
            self.current_def = None

    def define_pending(self, m):
        """The body of a declared type: a predicate over its base, or a law, or a conjunction of
        laws, whose first parameter is the type itself (05 R6)."""
        qname = self.qualify(m.name)
        self.current_def = qname
        try:
            ctx, base = m.base_ctx, m.base
            body_src = m.defn.body
            for n, _ in ctx:
                if not (isinstance(body_src, Lam) and isinstance(body_src.param, PVar)):
                    self.err(f"{m.name} is declared with parameters; its definition takes them too")
                body_src = body_src.body
            shape = self.env.defs[qname].body
            for _ in ctx:
                shape = shape.body
            param = shape.param
            if not ctx:
                # a declared name used as a type that turns out to be given a value of its base:
                # an ordinary definition (`n : Int`, `n := 3`, used in `VecOf n`)
                try:
                    with self.silent():
                        self.check([], body_src, base)
                    self.env.defs[qname] = Def(qname, base, None, line=m.defn.line)
                    value = self.check([], body_src, base)
                    self.env.defs[qname] = Def(qname, base, value, line=m.defn.line)
                    return
                except TypeCheckError:
                    self.env.defs[qname] = Def(qname, Univ(), self.env.defs[qname].body if
                                               self.env.defs[qname].pending else shape, pending=True,
                                               line=m.decl.line)
            fn = self.as_predicate(ctx, qname, body_src, shape, base)
            self.check_labels_touched(m.name, shape, fn)
            pred = _apply_law(fn, pattern_to_term(shape.param))
            sub = Subtype(param, shape.base, pred)
            ty: Term = Univ()
            body: Term = sub
            for n, t in reversed(ctx):
                ty = Pi(n, t, ty)
                body = Lam(PVar(n), body, t)
            self.env.defs[qname] = Def(qname, ty, body, line=m.defn.line)
        finally:
            self.current_def = None

    def as_predicate(self, ctx: Ctx, qname: str, src: Term, shape: Subtype, base: Term) -> Term:
        """The predicate of a declared type, with the shape's pattern variables free."""
        self_ty: Term = Var(qname)
        for n, _ in ctx:
            self_ty = App(self_ty, Var(n))
        try:
            with self.silent():
                fn = self.check(ctx, src, Pi("_", self_ty, Var("Bool")))
            fn = self.check(ctx, src, Pi("_", self_ty, Var("Bool")))
        except TypeCheckError:
            with self.silent():
                try:
                    fn, fty = self.infer(ctx, src)
                except TypeCheckError:
                    fn, fty = None, None
            if fn is None or not self._law_over(fty, self_ty):
                shown = pp(fty) if fty is not None else "something else"
                self.err(f"{qname} was declared as a refinement of {pp(base)}, but its body has type {shown}")
        return fn

    def _law_over(self, ty: Term, self_ty: Term) -> bool:
        if isinstance(ty, Var) and ty.name == "Law":
            return True
        w = self.whnf(ty)
        if isinstance(w, Var) and w.name == "Law":
            return True
        return isinstance(w, Pi) and self.conv(w.dom, self_ty) and self.is_law(subst(w.cod, {w.name: Var(fresh("c"))}))

    def check_labels_touched(self, name: str, shape: Subtype, fn: Term):
        """R3: the law that defines a type over a labeled base touches every label. `fn` is the
        law as written, a function of the whole value (or a conjunction of such)."""
        labels = [n for n in pattern_vars(shape.param)]
        touched = self.labels_touched_by(fn, labels)
        self._report_untouched(name, labels, touched)

    def _report_untouched(self, name: str, labels: list, touched: set):
        if not touched:
            self.err(f"the predicate of {name} touches none of its labels" if len(labels) > 1 else
                     f"the predicate of {name} does not mention its argument")
        for lab in labels:
            if lab not in touched:
                self.err(f"label {lab.split('~')[0]} of {name} is touched by no law")

    def labels_touched_by(self, fn: Term, labels: list) -> set:
        if isinstance(fn, And):
            return self.labels_touched_by(fn.lhs, labels) | self.labels_touched_by(fn.rhs, labels)
        if isinstance(fn, Lam) and isinstance(fn.param, PVar):
            return _projections_of(fn.body, fn.param.name, labels)
        h, args = unapply(fn)
        if isinstance(h, Var) and h.name in self.env.defs:
            body = self.env.defs[h.name].body
            for _ in args:
                if not isinstance(body, Lam):
                    return self._undecidable_touch(fn, labels)
                body = body.body
            if isinstance(body, Lam) and isinstance(body.param, PVar):
                return _projections_of(body.body, body.param.name, labels)
        return self._undecidable_touch(fn, labels)

    def _undecidable_touch(self, fn: Term, labels: list) -> set:
        """R3 is read off the law as written: a function of the whole value whose body projects its
        labels. A law in another form (an application whose body is not such a function) does not say
        which labels it touches; counting them all as touched would let a predicate define a type it
        does not constrain, so it is an error (05 R3)."""
        if os.environ.get("LUTHIER_R3_REPORT"):
            print(f"[R3 undecidable] {self.current_def}: {pp(fn)[:160]}", file=sys.stderr)
            return set(labels)
        self.err(f"cannot tell which labels of the base {pp(fn)[:120]} touches; write the law as a function "
                 f"of the whole value, \\ x {{ ... x.label ... }}, or name one that is (05 R3)")

    # ------------------------------------------------------------ R2
    def defined(self, q: str) -> bool:
        """Whether a type name has a definition (05 §1): a body that is not pending, a data, an
        alias, or a primitive of the kernel. A provisional extern type is debt, not a definition."""
        if q in BUILTIN_TYPES:
            return True
        d = self.env.defs.get(q)
        if d is None:
            return q in self.env.datas
        if d.data is not None or d.alias:
            return True
        if d.pending or d.body is None:
            return False
        if isinstance(d.body, Extern) and d.body.provisional:
            return False
        return True

    def is_type_name(self, q: str) -> bool:
        d = self.env.defs.get(q)
        if d is None or d.type is None:
            return False
        t = d.type
        while isinstance(t, Pi):
            t = t.cod
        return isinstance(t, Univ)

    def check_defined_types(self, q: str, object_names: set):
        """R2: every type a definition mentions is defined, unless it is in the definition's own
        object. Declarations and provisional externs are exempt."""
        d = self.env.defs.get(q)
        if d is None or (d.body is None and d.data is None) or d.pending:
            return
        if isinstance(d.body, Extern) and d.body.provisional:
            return
        used = set()
        if d.type is not None:
            used |= _global_names(d.type)
        if d.body is not None and not isinstance(d.body, Extern):
            used |= _global_names(d.body)
        if d.data is not None:
            for c in d.data.constructors:
                used |= _global_names(c.type)
        for n in sorted(used):
            if n == q or n in object_names or not self.is_type_name(n):
                continue
            if not self.defined(n):
                self.current_def = q
                try:
                    self.err(f"{n.split('.')[-1] if self.prefix else n} is used as a type but is only declared "
                             f"(05 R2): define it, or take it as a parameter")
                finally:
                    self.current_def = None

    def add_operator(self, d: OperatorDirective):
        """`operator op := f`: f must take two arguments; op on values of their types means f."""
        self.current_def = d.name
        try:
            term, ty = self.infer([], d.term)
            w = self.whnf(self.base_type(ty))
            if not isinstance(w, Pi):
                self.err(f"operator {d.op}: {pp(d.term)} is not a function")
            w2 = self.whnf(self.base_type(w.cod))
            if not isinstance(w2, Pi):
                self.err(f"operator {d.op}: {pp(d.term)} does not take two arguments")
            self.operators.setdefault(d.op, []).append((w.dom, w2.dom, w2.cod, term))
        finally:
            self.current_def = None

    def resolve_operator(self, ctx: Ctx, op: str, l: Term, lt: Term, rhs: Term):
        """A registered meaning of `op` whose first argument takes l and whose second takes the
        right-hand side, or None. The right side is inferred when it can be, so the types of
        both operands choose; otherwise the first candidate for the left type is checked."""
        head = self._head(lt)
        cands = [c for c in self.operators.get(op, ())
                 if self._heads_may_meet(head, self._head(c[0]))
                 and (self.convertible(lt, c[0]) or self.conv(self.base_type(lt), self.base_type(c[0])))]
        if not cands:
            return None
        if self.inferable(rhs):
            # inferred once, with its obligations recorded, and the obligations taken back if no
            # meaning of the operator takes it (inferring it silently and then again doubled the work
            # at every level of a nested expression)
            cd = self.current_def
            mark = len(self.obligations.get(cd, [])) if cd is not None else 0
            r, rt = self.infer(ctx, rhs)
            for d1, d2, cod, f in cands:
                if self.convertible(rt, d2) or self.conv(self.base_type(rt), self.base_type(d2)):
                    return App(App(f, l), self.coerce(ctx, r, rt, d2)), cod
            if cd is not None and cd in self.obligations:
                del self.obligations[cd][mark:]
            return None
        d1, d2, cod, f = cands[0]
        return App(App(f, l), self.check(ctx, rhs, d2)), cod

    def _head(self, ty: Term):
        """The outermost former of a type, below its refinements: a primitive's name, or the class of
        the former (a product, a function type, a sum). What two types must share to be convertible."""
        w = self.whnf(self.base_type(ty))
        if isinstance(w, Var):
            return ("name", w.name)
        h, _ = unapply(w)
        if isinstance(h, Var):
            return ("applied", h.name)
        return ("former", type(w).__name__)

    @staticmethod
    def _heads_may_meet(a, b) -> bool:
        if a[0] == "name" and a[1] in ("Int", "Float64", "Real", "String"):
            return b == a
        if b[0] == "name" and b[1] in ("Int", "Float64", "Real", "String"):
            return b == a
        return True

    def add_gen(self, g: GenDirective):
        """`gen T := term`: the term must be a `Gen T`. Recorded by the qualified type name."""
        q = self.resolve(g.type_name)
        if q is None:
            self.err(f"gen: unknown type {g.type_name}")
        d = self.env.defs.get(q)
        if d is not None and d.alias:
            # an alias is the type it stands for (05 R7): its generator is that type's
            if _ends_in_universe(d.type) and not isinstance(self.whnf(d.type), Univ):
                self.err(f"gen {g.type_name}: {g.type_name} is an alias of a type operator; give the "
                         f"generator to the type it stands for")
            key, _, _ = generator_key(self.env, Var(q))
        else:
            key = q
        prior = self.gens_by.get(key)
        if prior is not None and prior != g.type_name:
            self.err(f"gen {g.type_name}: {prior} already has a generator, and {g.type_name} is the same "
                     f"type ({key}); an alias has no identity of its own (05 R7), so a distribution that "
                     f"means something needs a type with a law (a subtype)")
        self.gens_by[key] = g.type_name
        if g.term is None:
            self.gens[key] = ("extern", g.target, None)
            return
        if self.resolve("Gen") is None:
            self.err('gen: `Gen` is not in scope; add `import "random"`')
        want = App(Var(self.resolve("Gen")), Var(q))
        self.current_def = f"gen {q}"
        try:
            with self.silent():
                term = self.check([], g.term, want)
        finally:
            self.current_def = None
        self.gens[key] = ("luthier", pp(g.term), term)

    def add_def(self, d: Def, object_names: Optional[set] = None):
        self._operand_memo.clear()      # its entries name terms of the previous definition
        if isinstance(d, OperatorDirective):
            self.add_operator(d)
            return
        qname = self.qualify(d.name)
        self.current_def = qname
        try:
            existing = self.env.defs.get(qname)
            if existing is not None and existing.alias:
                self.err(f"{d.name} is an alias and cannot be defined")
            if existing is not None and (existing.body is not None or existing.data is not None) \
                    and not existing.pending:
                self.err(f"{qname} is defined twice")
            if qname in self.env.datas:
                self.err(f"{qname} is defined twice")
            if d.data is not None:
                if existing is not None:
                    self.err(f"{qname} was declared as a value, it cannot become a data type")
                self.add_data(d, qname)
                return
            if existing is not None and existing.pending and d.body is not None:
                # a declared type of an imported file, defined here by its laws
                self.define_pending(_pending_member(d, existing))
                return
            ty = None
            if d.type is not None:
                ty = self.check([], d.type, Univ())
                k = self.implicit_params.get(qname, 0)
                w = ty
                for _ in range(k):
                    w = self.whnf(w)
                    if not isinstance(w, Pi) or not _ends_in_universe(w.dom):
                        self.err(f"an implicit parameter of {d.name} must be a type (of type U or a type "
                                 f"operator): it is inferred from the types of the explicit arguments")
                    w = w.cod
            if existing is not None:
                # filling a hole: the type must agree with the declaration
                if ty is not None and not self.conv(ty, existing.type):
                    self.err(f"{qname} was declared with type {pp(existing.type)}, but is defined with {pp(ty)}")
                ty = existing.type
            if d.body is None:
                if ty is None:
                    self.err(f"{qname} has neither type nor body")
                self.env.defs[qname] = Def(qname, ty, None, doc=d.doc, line=d.line)
                return
            if isinstance(d.body, Extern):
                self.add_extern(qname, d, ty)
                return
            if isinstance(d.body, Primitive):
                if not self.kernel:
                    self.err(f"primitive is allowed only in core.lut: {d.name} must be defined natively")
                base = None if (ty is None or isinstance(self.whnf(ty), Univ)) else ty
                self.env.defs[qname] = Def(qname, Univ(), Primitive(d.body.desc, base), doc=d.doc, line=d.line)
                return
            if isinstance(d.body, Axiom):
                if not self.library:
                    self.err(f"an axiom is allowed only in core.lut and lib/: {d.name} must be tested, "
                             f"not assumed")
                if ty is None:
                    self.err(f"axiom {d.name} needs a type")
                self.env.defs[qname] = Def(qname, ty, Axiom(d.body.desc), doc=d.doc, line=d.line)
                self.axioms[qname] = d.body.desc
                return
            if ty is not None:
                if existing is not None and existing.body is None and not _ends_in_universe(ty):
                    # a declared name given a body: an inhabitant of its base, or a predicate over it (R6)
                    body = self._inhabitant_or_predicate(qname, d, ty)
                    if body is not None:
                        return
                # declare first so the body can be recursive
                self.env.defs[qname] = Def(qname, ty, None, doc=d.doc, line=d.line)
                before = len(self.obligations.get(qname, []))
                body = self.check([], d.body, ty)
                w = self.whnf(ty)
                if isinstance(w, Subtype) and len(self.obligations.get(qname, [])) == before:
                    # the body was already of this subtype (an instance built by another
                    # definition): the laws still belong to this name, so `test` can run them
                    self.subtype_obligation([], body, w, ty)
            else:
                if d.name in free_vars(d.body):
                    self.err(f"recursive definition {qname} needs a declared type")
                body, ty = self.infer([], d.body)
            if _ends_in_universe(ty):
                self.check_new_type(qname, body)
            self.env.defs[qname] = Def(qname, ty, body, doc=d.doc, line=d.line)
        finally:
            self.current_def = None

    def _inhabitant_or_predicate(self, qname: str, d: Def, ty: Term):
        """`x : T` then `x := t`: if `t` is a `T`, the ordinary definition (returns None and the
        caller proceeds); if it is a predicate over `T`, `x` becomes that subtype of `T`."""
        try:
            with self.silent():
                self.env.defs[qname] = Def(qname, ty, None, doc=d.doc, line=d.line)
                self.check([], d.body, ty)
            return None
        except TypeCheckError as first:
            first_error = first
        shape = ty if isinstance(ty, Subtype) and isinstance(ty.pred, NoLaw) else \
            Subtype(PVar(fresh("x")), ty, NoLaw())
        self.env.defs[qname] = Def(qname, Univ(), shape, pending=True, line=d.line)
        try:
            fn = self.as_predicate([], qname, d.body, shape, ty)
        except TypeCheckError:
            self.env.defs[qname] = Def(qname, ty, None, doc=d.doc, line=d.line)
            raise
        self.check_labels_touched(d.name, shape, fn)
        pred = _apply_law(fn, pattern_to_term(shape.param))
        body = Subtype(shape.param, shape.base, pred)
        self.env.defs[qname] = Def(qname, Univ(), body, doc=d.doc, line=d.line)
        return body

    def check_new_type(self, qname: str, body: Term):
        """R4: a definition makes a new type only by laws (a subtype with a predicate) or by
        recursion (a data); R3: the predicate touches every label of its base."""
        b = body
        while isinstance(b, Lam):
            b = b.body
        if isinstance(b, Subtype) and not isinstance(b.pred, NoLaw) and \
                not (isinstance(b.pred, Con) and b.pred.name == "true"):
            labels = pattern_vars(b.param)
            touched = set(labels) & free_vars(b.pred)
            if len(labels) > 1 or touched or not self.kernel:
                self._report_untouched(qname.split(".")[-1], labels, touched)
            return
        if self.kernel:
            return
        name = qname.split(".")[-1]
        self.err(f"{name} names a structural type and states no law; write {name} = {pp(b)}, "
                 f"or declare {name} : {pp(b)} and define it by its laws (05 R4)")

    def add_extern(self, qname: str, d: Def, ty: Optional[Term]):
        """R5: an extern gives a value of a defined type, never a type; `extern provisional` lifts
        both requirements and is recorded as debt."""
        provisional = d.body.provisional
        if ty is None:
            self.err(f"extern {qname} needs a type")
        if _ends_in_universe(ty):
            if not provisional:
                self.err(f"an extern gives a value, not a type: define {d.name} natively, or write "
                         f"extern provisional (05 R5)")
            self.env.defs[qname] = Def(qname, ty, Extern(d.body.target, ty, provisional=True), doc=d.doc,
                                       line=d.line)
            self.provisional[qname] = []
            return
        ext = Extern(self.register_extern(d.body.target, ty), ty, provisional=provisional)
        self.env.defs[qname] = Def(qname, ty, ext, doc=d.doc, line=d.line)
        if provisional:
            self.provisional[qname] = sorted(n for n in _global_names(ty)
                                             if self.is_type_name(n) and not self.defined(n))
        # the environment's value is checked against every refinement of its type by `test`
        self.extern_obligations([], Var(qname), ty)

    def extern_obligations(self, ctx: Ctx, value: Term, ty: Term, depth: int = 0):
        """Every refinement in the type of a value the environment gives, as an obligation on that
        value (05 R5): the predicate of a subtype; the codomain of each arrow, quantified over its
        domain; each component of a record or a pair. The dimensions of an array are read off the
        array's shape by the bridge and owe nothing; its entries do (`Vec (Fin n)` owes that each
        entry is below n). A sum or a data type is not entered: a refinement under a constructor
        (the `Table` of a `Maybe Table`) stays unchecked (07 §9)."""
        if depth > 16:
            return
        w = self.whnf(ty)
        if isinstance(w, Subtype):
            if not isinstance(w.pred, NoLaw) and not (isinstance(w.pred, Con) and w.pred.name == "true"):
                self.subtype_obligation(ctx, value, w, ty)
            if isinstance(w.param, PPair):
                labels = [n.split("~")[0] for n in pattern_vars(w.param)]
                if shaped(self.env, ty) is not None:
                    labels = labels[-1:]       # an array: only the entries can break a refinement
                for label in labels:
                    with self.silent():
                        proj, fty = self.project(ctx, value, ty, label)
                    self.extern_obligations(ctx, proj, fty, depth + 1)
                return
            self.extern_obligations(ctx, value, w.base, depth + 1)
            return
        if isinstance(w, Pi):
            x = _readable_name(w.name if w.name != "_" else "x", ctx, value)
            cod = w.cod if w.name == "_" else subst(w.cod, {w.name: Var(x)})
            self.extern_obligations(ctx + [(x, w.dom)], App(value, Var(x)), cod, depth + 1)
            return
        if isinstance(w, Sigma):
            a, b = fresh("a"), fresh("b")
            fst = Match(value, ((PPair(PVar(a), PWild()), Var(a)),))
            snd = Match(value, ((PPair(PWild(), PVar(b)), Var(b)),))
            self.extern_obligations(ctx, fst, w.fst, depth + 1)
            self.extern_obligations(ctx, snd, w.snd if w.name == "_" else subst(w.snd, {w.name: fst}), depth + 1)

    def add_data(self, d: Def, qname: str):
        decl = d.data
        ctx: Ctx = []
        params = []
        for n, t in decl.params:
            t2 = self.check(ctx, t, Univ())
            params.append((n, t2))
            ctx.append((n, t2))
        dty = Univ()
        for n, t in reversed(params):
            dty = Pi(n, t, dty)
        qdecl = DataDecl(qname, params, [])
        self.env.defs[qname] = Def(qname, dty, None, data=qdecl)
        self.env.datas[qname] = qdecl
        for c in decl.constructors:
            qc = self.qualify(c.name)
            if qc in self.env.cons or qc in self.env.defs:
                self.err(f"constructor {qc} is defined twice")
            cty = self.check(ctx, c.type, Univ())
            # the constructor must produce the data type being declared
            h, _ = unapply(self._codomain(cty))
            if not (isinstance(h, Var) and h.name == qname):
                self.err(f"constructor {c.name} of {qname} must return {qname}")
            full = cty
            for n, t in reversed(params):
                full = Pi(n, t, full)
            qdecl.constructors.append(Constructor(qc, cty))
            self.env.cons[qc] = (qname, full)
        recursive = any(qname in _global_names(dom)
                        for c in qdecl.constructors for _, dom in _peel_pi(c.type)[0])
        if not self.kernel and not recursive:
            alts = []
            for c in qdecl.constructors:
                doms = [t for _, t in _peel_pi(c.type)[0]]
                payload = "Unit" if not doms else " * ".join(pp(t) for t in doms)
                alts.append(f"{c.name.split('.')[-1]} : {payload}")
            name = qname.split(".")[-1]
            self.err(f"{name} is not recursive; write {name} = < {' | '.join(alts)} > (05 R4)")

    def _codomain(self, ty: Term) -> Term:
        while isinstance(ty, Pi):
            ty = ty.cod
        return ty

    def register_extern(self, target: str, ty: Term):
        spec = target.split(":", 1)[1] if target.startswith("python:") else target
        if ":" in spec:
            mod, attr = spec.split(":", 1)
        else:
            mod, _, attr = spec.rpartition(".")
        if not mod:
            self.err(f'extern target {target!r} must be module.attr or module:attr')
        try:
            m = importlib.import_module(mod)
            fn = m
            for part in attr.split("."):
                fn = getattr(fn, part)
        except (ImportError, AttributeError) as e:
            self.err(f"cannot resolve extern {target!r}: {e}")
        base = self.pi_chain(ty)
        # keyed by target and type: one Python function may be declared at several types
        # (approx on R, on Vec, on Mat), and each declaration marshals by its own
        key = f"{target}@{pp(base)}"
        self.env.externs[key] = ExternInfo(fn, pi_arity(base), base)
        return key

    def pi_chain(self, ty: Term) -> Term:
        """Each arrow exposed (a subtype of a function type is seen as the function type), so
        arity can be read; domains and the final result keep their declared types."""
        w = self.whnf(self.base_type(ty))
        if isinstance(w, Pi):
            return Pi(w.name, w.dom, self.pi_chain(w.cod))
        return ty

    # ---------------------------------------------------------- obligations
    def add_obligation(self, ctx: Ctx, term: Term, label: str):
        if not self.recording or self.current_def is None:
            return
        name = self.current_def
        bound = {}
        if self.lets:
            # a variable bound by `match e { x -> ... }` is e: the law speaks of e, not of every x
            for n, t in self.lets:
                bound[n] = subst(t, bound) if bound else t
            term = subst(term, bound)
            ctx = [(n, subst(t, bound)) for n, t in ctx if n not in bound]
        if self.path:
            # raised inside a branch: the branch's condition is a precondition of the law (05 §7)
            try:
                with self.silent():
                    _, tt = self.infer(ctx, term)
                if self.is_bool(tt):
                    for cond in reversed(self.path):
                        term = App(App(Var("implies"), subst(cond, bound) if bound else cond), term)
            except (TypeCheckError, EvalError):
                pass
        self.obligations.setdefault(name, []).append(Obligation(name, list(ctx), term, label))

    class _Silent:
        def __init__(self, ck): self.ck = ck
        def __enter__(self): self.saved = self.ck.recording; self.ck.recording = False
        def __exit__(self, *a): self.ck.recording = self.saved

    def silent(self):
        """Context manager: type without recording obligations (laws at test time, eval)."""
        return Checker._Silent(self)

    # ---------------------------------------------------------------- infer
    def infer(self, ctx: Ctx, t: Term):
        if isinstance(t, Var):
            ty = lookup(ctx, t.name)
            if ty is not None:
                return t, ty
            q = self.resolve(t.name)
            if q is None and t.name in self.labels:
                return self.label_value(t.name)
            if q is None:
                if t.name in ("__nil__", "__cons__"):
                    self.err("a list literal needs an expected type or a first element")
                if "." in t.name:
                    dotted = self.infer_dotted(ctx, t.name)
                    if dotted is not None:
                        return dotted
                self.err(f"unbound name {t.name}")
            if q in self.env.cons:
                return Con(q), self.env.cons[q][1]
            if q in self.env.defs:
                return Var(q), self.env.defs[q].type
            return Var(q), Univ()
        if isinstance(t, Con):
            return t, self.env.cons[t.name][1]
        if isinstance(t, Lit):
            if isinstance(t.value, bool):
                self.err("bool literal")
            if isinstance(t.value, int):
                return t, Var("Int")
            if isinstance(t.value, float):
                return t, Var("Float64")
            return t, Var("String")
        if isinstance(t, Univ):
            return t, Univ()
        if isinstance(t, Extern):
            if t.type is None:
                self.err("an extern needs its type from the context: use it where the expected type is known")
            return t, t.type
        if isinstance(t, RecordLit):
            self.err("a record literal needs its type from the context: use it where the expected type is known")
        if isinstance(t, Sum):
            alts = []
            for label, a in t.alts:
                if label in [l for l, _ in alts]:
                    self.err(f"label {label} appears twice in a sum")
                alts.append((label, self.check(ctx, a, Univ())))
            return Sum(tuple(alts)), Univ()
        if isinstance(t, Inj):
            if t.type is None:
                self.err(f"the injection {pp(t)} needs its sum type from the context")
            return t, t.type
        if isinstance(t, Named):
            self.err(f"({t.name} : {pp(t.type)}) names a position of a product or a sum; "
                     f"write it next to another with `*` or `+`")
        if isinstance(t, NoLaw):
            return t, Var("Law")
        if isinstance(t, App):
            return self.infer_app(ctx, t)
        if isinstance(t, Lam):
            if t.ann is None:
                self.err(f"cannot infer the type of {pp(t)}: annotate the parameter or give an expected type")
            dom = self.check(ctx, t.ann, Univ())
            param, ctx2 = self.bind_pattern(ctx, t.param, dom)
            if t.res is not None and isinstance(param, PVar):
                # elaborated: the body was checked against its result type already
                return Lam(param, t.body, dom, t.res), Pi(param.name, dom, t.res)
            body, cod = self.infer(ctx2, t.body)
            name = param.name if isinstance(param, PVar) else fresh("p")
            if not isinstance(param, PVar):
                pt = pattern_to_term(param)
                if pt is not None:
                    # cod may mention the pattern variables; abstract them through a fresh Pi variable is not
                    # expressible here, so require cod not to depend on them
                    if set(pattern_vars(param)) & free_vars(cod):
                        self.err("the result type of a tuple-pattern lambda cannot depend on its components")
            return Lam(param, body, dom), Pi(name, dom, cod)
        if isinstance(t, Pi):
            dom = self.check(ctx, t.dom, Univ())
            cod = self.check(ctx + [(t.name, dom)], t.cod, Univ())
            return Pi(t.name, dom, cod), Univ()
        if isinstance(t, Sigma):
            a = self.check(ctx, t.fst, Univ())
            b = self.check(ctx + [(t.name, a)], t.snd, Univ())
            return Sigma(t.name, a, b), Univ()
        if isinstance(t, Pair):
            a, ta = self.infer(ctx, t.fst)
            b, tb = self.infer(ctx, t.snd)
            return Pair(a, b), Sigma("_", ta, tb)
        if isinstance(t, Arrow):
            l, lt = self.infer(ctx, t.lhs)
            if self.conv(lt, Univ()):
                r = self.check(ctx, t.rhs, Univ())
                return Pi("_", l, r), Univ()
            if self.is_bool(lt):
                r = self.check(ctx, t.rhs, Var("Bool"))
                return App(App(Var("implies"), l), r), Var("Bool")
            self.err(f"'->' expects a type or a Bool on the left, got {pp(l)} : {pp(lt)}")
        if isinstance(t, BinOp):
            return self.infer_binop(ctx, t)
        if isinstance(t, And):
            l, lt = self.infer(ctx, t.lhs)
            if not self.is_law(lt):
                self.err(f"left side of '&' is not a law: {pp(l)} : {pp(lt)}")
            r, rt = self.infer(ctx, t.rhs)
            if not self.is_law(rt):
                self.err(f"right side of '&' is not a law: {pp(r)} : {pp(rt)}")
            return And(l, r), Var("Law")
        if isinstance(t, Forget):
            a, ta = self.infer(ctx, t.arg)
            b = self.strip_subtype(ta)
            if b is None:
                self.err(f"forget applied to {pp(a)} : {pp(ta)}, which is not a subtype")
            return a, b
        if isinstance(t, Subtype) and isinstance(t.pred, NoLaw):
            base = self.check(ctx, t.base, Univ())
            return Subtype(t.param, base, NoLaw()), Univ()
        if isinstance(t, Subtype):
            base = self.check(ctx, t.base, Univ())
            param, ctx2 = self.bind_pattern(ctx, t.param, base)
            mark = len(self.obligations.get(self.current_def, [])) if self.current_def else None
            pred, pt = self.infer(ctx2, t.pred)
            if not self.is_law(pt):
                self.err(f"the predicate of a subtype must be Bool-valued or a law: {pp(pred)} : {pp(pt)}")
            # a coercion inside the predicate is a precondition of the law: it joins the predicate
            if mark is not None and self.current_def in self.obligations:
                raised = self.obligations[self.current_def][mark:]
                del self.obligations[self.current_def][mark:]
                if not self.obligations[self.current_def]:
                    del self.obligations[self.current_def]
                for ob in raised:
                    law = ob.term
                    for name, ty in reversed(ob.params[len(ctx2):]):
                        law = Lam(PVar(name), law, ann=ty)
                    pred = And(law, pred)
            return Subtype(param, base, pred), Univ()
        if isinstance(t, Match):
            return self.check_match(ctx, t, None)
        if isinstance(t, Proj):
            base, bty = self.infer(ctx, t.term)
            return self.project(ctx, base, bty, t.field)
        self.err(f"cannot infer {t!r}")

    # ---------------------------------------------------------- projections
    def infer_dotted(self, ctx: Ctx, name: str):
        """`a.b.c` that is not a qualified name: the longest prefix that is a variable or a
        definition, then one projection per remaining segment. A module is a record whose
        components are its definitions, so qualification and projection share the dot; the
        whole name is tried first, which is what makes a module alias win."""
        segs = name.split(".")
        for k in range(len(segs) - 1, 0, -1):
            prefix, fields = ".".join(segs[:k]), segs[k:]
            ty = lookup(ctx, prefix) if k == 1 else None
            if ty is not None:
                term = Var(prefix)
            else:
                q = self.resolve(prefix)
                if q is None:
                    continue
                if q in self.env.cons:
                    term, ty = Con(q), self.env.cons[q][1]
                elif q in self.env.defs:
                    term, ty = Var(q), self.env.defs[q].type
                else:
                    term, ty = Var(q), Univ()
            for f in fields:
                term, ty = self.project(ctx, term, ty, f)
            return term, ty
        return None

    def project(self, ctx: Ctx, term: Term, ty: Term, field: str):
        """`term.field` as a one-branch match on the component pattern of term's type. The type
        of the component may mention earlier components; those become projections too."""
        w = self.whnf(ty)
        while isinstance(w, Subtype) and not isinstance(w.param, PPair):
            w = self.whnf(w.base)          # a refinement { x : T | p } has the components of T
        if not isinstance(w, Subtype):
            self.err(f"{pp(term)} : {pp(ty)} has no named components, so .{field} means nothing")
        names = pattern_vars(w.param)
        hits = [n for n in names if n.split("~")[0] == field]
        if not hits:
            shown = ", ".join(n.split("~")[0] for n in names)
            self.err(f"{pp(term)} : {pp(ty)} has no component {field}; its components are {shown}")
        var = hits[0]

        def keep_only(p: Pattern, name: str) -> Pattern:
            if isinstance(p, PVar):
                return p if p.name == name else PWild()
            if isinstance(p, PPair):
                return PPair(keep_only(p.fst, name), keep_only(p.snd, name))
            if isinstance(p, PCon):
                return PCon(p.name, tuple(keep_only(a, name) for a in p.args))
            return p

        proj = Match(term, ((keep_only(w.param, var), Var(var)),))
        with self.silent():
            _, ctx2 = self.bind_pattern(ctx, w.param, w.base)
        fty = lookup(ctx2, var)
        for n in names:
            if n != var and n in free_vars(fty):
                fty = subst(fty, {n: Match(term, ((keep_only(w.param, n), Var(n)),))})
        return proj, fty

    def infer_app(self, ctx: Ctx, t: App):
        if isinstance(t.fn, Var) and t.fn.name == "__negate__":
            return self.infer_negation(ctx, t.arg)
        h, args = unapply(t)
        if isinstance(h, Var) and lookup(ctx, h.name) is None:
            q = self.resolve(h.name)
            k = self.implicit_params.get(q, 0) if q is not None else 0
            if k:
                res = self.infer_implicit_app(ctx, h, args, k)
                if res is not None:
                    return res
        f, fty = self.infer(ctx, t.fn)
        w = self.whnf(self.base_type(fty))
        if not isinstance(w, Pi):
            self.err(f"{pp(f)} : {pp(fty)} is not a function, cannot apply it to {pp(t.arg)}")
        a = self.check(ctx, t.arg, w.dom)
        return App(f, a), subst(w.cod, {w.name: a})

    # ------------------------------------------------------------ implicit arguments
    def infer_implicit_app(self, ctx: Ctx, h: Var, args: list, k: int):
        """`f a1 ... an` where f's first k parameters are implicit types. When a1 is itself a type the
        call gives them explicitly, as every call did before implicit parameters existed, and the
        ordinary path checks it (None is returned). Otherwise each implicit parameter is an unknown,
        solved by unifying the type of each explicit argument with the type of its parameter; an
        argument whose type cannot be inferred alone (a lambda) is checked once the others solved
        what its type needs. The elaborated term passes every argument explicitly."""
        try:
            with self.silent():
                _, a0t = self.infer(ctx, args[0])
            if _ends_in_universe(self.whnf(a0t)) or isinstance(self.whnf(a0t), Univ):
                return None
        except TypeCheckError:
            pass
        f, fty = self.infer(ctx, h)
        metas = []
        ty = fty
        for _ in range(k):
            w = self.whnf(ty)
            if not isinstance(w, Pi):
                self.err(f"{h.name} has {k} implicit parameters but its type has fewer arrows")
            m = f"?{w.name.split('~')[0]}~{len(self._meta_names)}"
            self._meta_names.add(m)
            metas.append(m)
            ty = subst(w.cod, {w.name: Var(m)}) if w.name != "_" else w.cod
        sol: dict = {}
        # the parameter types, each with the arguments before it in place of their names
        doms, rest = [], ty
        for a in args:
            w = self.whnf(rest)
            if not isinstance(w, Pi):
                self.err(f"{h.name} is applied to more arguments than its type takes")
            doms.append(w)
            rest = subst(w.cod, {w.name: a}) if w.name != "_" else w.cod
        inferred: dict = {}
        for i, a in enumerate(args):
            if self._mentions_metas(doms[i].dom, metas):
                got = self._try_infer(ctx, a)
                if got is not None:
                    inferred[i] = got
                    self.unify(doms[i].dom, got[1], sol, metas)
        unsolved = [m for m in metas if m not in sol]
        if unsolved:
            names = ", ".join(m[1:].split("~")[0] for m in unsolved)
            self.err(f"cannot infer the implicit parameter(s) {names} of {h.name} from its arguments; "
                     f"give them explicitly, {h.name} {' '.join('T' for _ in metas)} ...")
        term: Term = f
        for m in metas:
            term = App(term, sol[m])
        ty = fty
        for m in metas:
            w = self.whnf(ty)
            ty = subst(w.cod, {w.name: sol[m]}) if w.name != "_" else w.cod
        for i, a in enumerate(args):
            w = self.whnf(ty)
            if i in inferred:
                ae, at = inferred[i]
                a2 = self.coerce(ctx, ae, at, w.dom)
            else:
                a2 = self.check(ctx, a, w.dom)
            term = App(term, a2)
            ty = subst(w.cod, {w.name: a2}) if w.name != "_" else w.cod
        return term, ty

    def _try_infer(self, ctx: Ctx, a: Term):
        """The elaboration and type of a term when it has one by itself; None for a term only checking
        gives a type (an unannotated lambda), with any obligation the attempt recorded taken back."""
        cd = self.current_def
        mark = len(self.obligations.get(cd, [])) if cd is not None else 0
        try:
            return self.infer(ctx, a)
        except TypeCheckError:
            if cd is not None and cd in self.obligations:
                del self.obligations[cd][mark:]
            return None

    def _mentions_metas(self, t: Term, metas: list) -> bool:
        return bool(free_vars(t) & set(metas))

    def unify(self, p: Term, t: Term, sol: dict, metas: list, depth: int = 0):
        """First-order matching of a parameter type `p`, with unknowns among `metas`, against an
        argument's type `t`, recording solutions in `sol`. What it cannot match it leaves: the
        argument is checked against the solved type afterwards, which reports a real mismatch."""
        if depth > 40:
            return
        p = subst(p, {m: v for m, v in sol.items()}) if sol else p
        if not self._mentions_metas(p, metas):
            return
        if isinstance(p, Var) and p.name in metas:
            sol[p.name] = t
            return
        tw = t
        for attempt in range(3):
            if isinstance(p, Pi) and isinstance(tw, Pi):
                self.unify(p.dom, tw.dom, sol, metas, depth + 1)
                pc = subst(p.cod, {p.name: Var(tw.name)}) if p.name != "_" and tw.name != "_" else p.cod
                self.unify(pc, tw.cod, sol, metas, depth + 1)
                return
            if isinstance(p, Sigma) and isinstance(tw, Sigma):
                self.unify(p.fst, tw.fst, sol, metas, depth + 1)
                ps = subst(p.snd, {p.name: Var(tw.name)}) if p.name != "_" and tw.name != "_" else p.snd
                self.unify(ps, tw.snd, sol, metas, depth + 1)
                return
            if isinstance(p, Sum) and isinstance(tw, Sum) and len(p.alts) == len(tw.alts):
                for (_, x), (_, y) in zip(p.alts, tw.alts):
                    self.unify(x, y, sol, metas, depth + 1)
                return
            hp, ap = unapply(p)
            ht, at = unapply(tw)
            if isinstance(hp, Var) and isinstance(ht, Var) and hp.name == ht.name and len(ap) == len(at) and ap:
                for x, y in zip(ap, at):
                    self.unify(x, y, sol, metas, depth + 1)
                return
            # unfold the argument's type (an alias, a refinement) and the parameter's, and try again
            nt = self.whnf(tw)
            if isinstance(nt, Subtype) and not isinstance(self.whnf(p), Subtype):
                nt = self.whnf(nt.base)
            np_ = self.whnf(p)
            if nt == tw and np_ == p:
                return
            tw, p = nt, np_

    def infer_negation(self, ctx: Ctx, x: Term):
        """`-x`: `0 - x` on an Int, `0.0 - x` on a Float64, and on any other type the meaning of `-`
        registered for it applied to its zero is not guessed: the negation is an error there."""
        _, xt = self.infer(ctx, x)
        prim = self.whnf(self.base_type(xt))
        if isinstance(prim, Var) and prim.name == "Int":
            return self.infer(ctx, BinOp("-", Lit(0), x))
        if isinstance(prim, Var) and prim.name == "Float64":
            return self.infer(ctx, BinOp("-", Lit(0.0), x))
        self.err(f"unary minus on {pp(xt)}: it is defined on Int and Float64; write the negation of "
                 f"this type explicitly")

    def infer_binop(self, ctx: Ctx, t: BinOp):
        op = t.op
        if op in ("and", "or"):
            l = self.check(ctx, t.lhs, Var("Bool"))
            r = self.check(ctx, t.rhs, Var("Bool"))
            return App(App(Var(op), l), r), Var("Bool")
        if op == "+" and self._type_operand(ctx, t):
            # `A + B + C` is `A + (B + C)`: anonymous sums inject with left and right (04 §2)
            operands = []

            def flatten(x):
                if isinstance(x, BinOp) and x.op == "+":
                    flatten(x.lhs)
                    flatten(x.rhs)
                else:
                    operands.append(x)
            flatten(t)
            types = [self.check(ctx, x, Univ()) for x in operands]
            out = types[-1]
            for a in reversed(types[:-1]):
                out = Sum((("left", a), ("right", out)))
            return out, Univ()
        if op == "*" and self._type_operand(ctx, t, "*"):
            # `A * B * C` is `A * (B * C)`, as the tuple `(a, b, c)` is `(a, (b, c))`
            operands = []

            def flatten_prod(x):
                if isinstance(x, BinOp) and x.op == "*":
                    flatten_prod(x.lhs)
                    flatten_prod(x.rhs)
                else:
                    operands.append(x)
            flatten_prod(t)
            types = [self.check(ctx, x, Univ()) for x in operands]
            out = types[-1]
            for a in reversed(types[:-1]):
                out = Sigma("_", a, out)
            return out, Univ()
        l, lt = self.infer(ctx, t.lhs)
        if op in self.operators:
            res = self.resolve_operator(ctx, op, l, lt, t.rhs)
            if res is not None:
                return res
        if op in ("==", "/="):
            if self.contains_function(lt):
                why = ("the reals have no computable equality; compare Float64 values, or "
                       if self._mentions_real(lt) else "")
                self.err(f"no structural equality on {pp(self.base_type(lt))}: {why}compare with an equality "
                         f"given as a parameter or a component (05 R8)")
            if self.inferable(t.rhs):
                r, rt = self.infer(ctx, t.rhs)
                if not (self.convertible(lt, rt) or self.convertible(rt, lt)
                        or self.conv(self.base_type(lt), self.base_type(rt))):
                    self.err(f"cannot compare {pp(l)} : {pp(lt)} with {pp(r)} : {pp(rt)}")
            else:
                r = self.check(ctx, t.rhs, self.base_type(lt))
            return BinOp(op, l, r), Var("Bool")
        bt = self.base_type(lt)
        bw = self.whnf(bt)
        num = isinstance(bw, Var) and bw.name in ("Int", "Float64")
        if op == "+" and isinstance(bw, Var) and bw.name == "String":
            r = self.check(ctx, t.rhs, bt)
            return BinOp(op, l, r), bt
        if not num:
            hint = "; the operations of Real are not computed (06 §2)" if self._is_real(bw) else ""
            self.err(f"operator {op} expects Int or Float64, got {pp(l)} : {pp(lt)}{hint}")
        r = self.check(ctx, t.rhs, bt)
        if op in ("<", "<=", ">", ">="):
            return BinOp(op, l, r), Var("Bool")
        return BinOp(op, l, r), bt

    # ---------------------------------------------------------------- check
    def check(self, ctx: Ctx, t: Term, ty: Term) -> Term:
        w = self.whnf(ty)
        sm = w if isinstance(w, Sum) else None
        if sm is not None:
            inj = self.try_injection(ctx, t, sm, ty)
            if inj is not None:
                return inj
        if isinstance(t, RecordLit):
            rc = record_components(self.env, ty)
            if rc is None:
                self.err(f"a record literal needs a type with named components, not {pp(ty)}")
            hname, names, _ = rc
            given = dict(t.fields)
            if len(given) != len(t.fields):
                self.err(f"a field is given twice in a {hname} literal")
            missing = [n for n in names if n not in given]
            extra = [n for n in given if n not in names]
            if missing or extra:
                self.err(f"{hname} literal: missing {missing}, unknown {extra}" if missing and extra
                         else f"{hname} literal: missing fields {missing}" if missing
                         else f"{hname} literal: unknown fields {extra}")
            vals = [given[n] for n in names]
            term = vals[-1]
            for v in reversed(vals[:-1]):
                term = Pair(v, term)
            return self.check(ctx, term, ty)
        if isinstance(t, Extern) and t.type is None:
            # an extern inside a term takes the expected type, as a definition takes its declared one
            if isinstance(w, Univ):
                self.err("an extern type is only allowed as the body of a definition")
            ext = Extern(self.register_extern(t.target, ty), ty)
            self.extern_obligations(ctx, ext, ty)
            return ext
        if isinstance(t, Lam) and isinstance(w, Pi):
            if t.ann is not None:
                ann = self.check(ctx, t.ann, Univ())
                if not self.conv(ann, w.dom):
                    self.err(f"parameter {pp_pat(t.param)} annotated {pp(ann)} but expected {pp(w.dom)}")
            param, ctx2 = self.bind_pattern(ctx, t.param, w.dom)
            pt = pattern_to_term(param)
            cod = subst(w.cod, {w.name: pt}) if pt is not None else w.cod
            body = self.check(ctx2, t.body, cod)
            # keep the result type: a component projected out of a value is typed again later
            # (a law of an enclosing structure), and must have the type it was checked at
            return Lam(param, body, w.dom, cod if isinstance(param, PVar) else None)
        if isinstance(t, Pair) and isinstance(w, Sigma):
            a = self.check(ctx, t.fst, w.fst)
            b = self.check(ctx, t.snd, subst(w.snd, {w.name: a}))
            return Pair(a, b)
        if isinstance(t, Match) and not isinstance(w, Subtype):
            term, _ = self.check_match(ctx, t, ty)
            return term
        if (isinstance(t, Var) and t.name == "__nil__" or (isinstance(t, App) and self._is_cons(t))) \
                and not isinstance(w, Subtype):
            return self.check_list(ctx, t, w)
        if isinstance(w, Subtype) and isinstance(t, Match) and (isinstance(w.pred, NoLaw) or
                                                               (isinstance(w.pred, Con) and w.pred.name == "true")):
            # a record type that names components and states no law: check each branch against
            # it, so a record literal in a branch still sees the component names
            term, _ = self.check_match(ctx, t, ty)
            return term
        if isinstance(w, Subtype) and isinstance(w.pred, NoLaw):
            # a labeled product is the product: check against it, report against the labels
            if self.inferable(t):
                term, tty = self.infer(ctx, t)
                return self.coerce(ctx, term, tty, ty)
            return self.check(ctx, t, w.base)
        if isinstance(w, Subtype):
            if self.inferable(t):
                term, tty = self.infer(ctx, t)
                if self.convertible(tty, ty):
                    return term          # already of this subtype: nothing to prove
                inner = self.coerce(ctx, term, tty, w.base)
            else:
                inner = self.check(ctx, t, w.base)
            self.subtype_obligation(ctx, inner, w, ty)
            return inner
        term, tty = self.infer(ctx, t)
        return self.coerce(ctx, term, tty, ty)

    def inferable(self, t: Term) -> bool:
        if isinstance(t, Var) and t.name in self.labels and self.resolve(t.name) is None:
            return self.labels[t.name] is not None
        return not isinstance(t, (Lam, Pair, Match, RecordLit)) and not (
            isinstance(t, Var) and t.name == "__nil__") and not (isinstance(t, App) and self._is_cons(t))

    def convertible(self, have: Term, want: Term) -> bool:
        """`have` is `want`, or a subtype of it (through any number of layers), including the
        refinement of a primitive type (`Float64 : Real`), or a function type that passes for
        `want` by variance (05 R9)."""
        cur = have
        for _ in range(32):
            if self.conv(cur, want):
                return True
            b = self.strip_subtype(cur)
            if b is None:
                b = self.primitive_base(cur)
            if b is None:
                return self.function_passes(cur, want)
            cur = b
        return False

    def primitive_base(self, ty: Term) -> Optional[Term]:
        """`Real` for `Float64`: the type a primitive refines, or None."""
        w = self.whnf(ty)
        if isinstance(w, Var):
            d = self.env.defs.get(w.name)
            if d is not None and isinstance(d.body, Primitive) and d.body.base is not None:
                return d.body.base
        return None

    def _is_real(self, ty: Term) -> bool:
        w = self.whnf(ty)
        return isinstance(w, Var) and w.name == "Real"

    def function_passes(self, have: Term, want: Term) -> bool:
        """R9: `A -> B` passes for `A' -> B'` when A' refines A and B refines B'."""
        hw = self.whnf(self.base_type(have))
        ww = self.whnf(self.base_type(want))
        if not (isinstance(hw, Pi) and isinstance(ww, Pi)):
            return False
        if hw == ww:
            return False
        x = Var(fresh("x"))
        if not self.convertible(ww.dom, hw.dom):
            return False
        return self.convertible(subst(hw.cod, {hw.name: x}), subst(ww.cod, {ww.name: x}))

    def coerce(self, ctx: Ctx, term: Term, have: Term, want: Term) -> Term:
        """Accept `term : have` where `want` is expected: equal types, a subtype seen in its base
        (forget), a base seen in a subtype (an obligation), or pairs of those, component by component."""
        if self.convertible(have, want):
            return term
        w = self.whnf(want)
        if isinstance(w, Subtype) and isinstance(w.pred, NoLaw):
            try:
                return self.coerce(ctx, term, have, w.base)
            except TypeCheckError:
                self.err(f"{pp(term)} has type {pp(have)} but {pp(want)} was expected")
        if isinstance(w, Subtype):
            inner = self.coerce(ctx, term, have, w.base)
            self.subtype_obligation(ctx, inner, w, want)
            return inner
        hw = self.whnf(self.base_type(have))
        if isinstance(w, Sigma) and isinstance(hw, Sigma):
            # project with a match and coerce each component; the obligations fall on the projections
            pat = PPair(PVar("p1"), PVar("p2"))
            fst = Match(term, ((pat, Var("p1")),))
            snd = Match(term, ((pat, Var("p2")),))
            try:
                self.coerce(ctx, fst, hw.fst, w.fst)
                self.coerce(ctx, snd, subst(hw.snd, {hw.name: fst}), subst(w.snd, {w.name: fst}))
            except TypeCheckError:
                self.current_def, saved = None, self.current_def
                try:
                    raise TypeCheckError((f"in {saved}: " if saved else "") +
                                         f"{pp(term)} has type {pp(have)} but {pp(want)} was expected")
                finally:
                    self.current_def = saved
            return term
        hint = ""
        if isinstance(w, Var) and w.name == "Float64" and self._is_real(self.base_type(have)):
            hint = ("; a Real has no computation of its own (06 §3), so nothing turns it into a Float64 yet: "
                    "write the code over Float64, or generic in its number type (06 §4)")
        self.err(f"{pp(term)} has type {pp(have)} but {pp(want)} was expected{hint}")

    def subtype_obligation(self, ctx: Ctx, value: Term, sub: Subtype, ty: Term):
        if isinstance(sub.pred, NoLaw) or (isinstance(sub.pred, Con) and sub.pred.name == "true"):
            return          # a labeled product names components and states no law
        if isinstance(sub.param, PVar) and not (free_vars(value) & set(pattern_vars(sub.param)) - {sub.param.name}):
            applied = subst(sub.pred, {sub.param.name: value})     # readable: the law on the value
        else:
            applied = App(Lam(sub.param, sub.pred, ann=sub.base), value)
        local = {n for n, _ in ctx}
        if not (free_vars(value) & local):
            try:
                b = self.decide_closed(applied)
            except EvalError:
                b = None
            if b is True:
                return
            if b is False:
                self.err(f"{pp(value)} does not satisfy {pp(ty)}")
        self.add_obligation(ctx, applied, pp(ty))

    def decide_closed(self, t: Term) -> Optional[bool]:
        """True/False if the closed predicate reduces to Bools (through conjunctions); None if a
        conjunct is a quantified law or is stuck, in which case `test` decides."""
        r = whnf(self.env, t, self.fuel())
        if isinstance(r, And):
            a = self.decide_closed(r.lhs)
            if a is False:
                return False
            b = self.decide_closed(r.rhs)
            if b is False:
                return False
            return True if (a is True and b is True) else None
        return as_bool(r)

    def _is_cons(self, t: Term) -> bool:
        h, args = unapply(t)
        return isinstance(h, Var) and h.name == "__cons__"

    def check_list(self, ctx: Ctx, t: Term, w: Term) -> Term:
        h, args = unapply(w)
        if not (isinstance(h, Var) and h.name == "List" and len(args) == 1):
            self.err(f"a list literal was given but {pp(w)} was expected")
        elt = args[0]
        items = []
        while isinstance(t, App):
            _, a = unapply(t)
            items.append(a[0])
            t = a[1]
        out = App(Con("nil"), elt)
        for x in reversed(items):
            out = App(App(App(Con("cons"), elt), self.check(ctx, x, elt)), out)
        return out

    def check_match(self, ctx: Ctx, t: Match, ty: Optional[Term]):
        scrut, sty = self.infer(ctx, t.scrut)
        sw = self.whnf(self.base_type(sty))
        branches = []
        result_ty = ty
        covered = set()
        catch_all = False
        for pat, body in t.branches:
            pat2, ctx2 = self.bind_pattern(ctx, pat, sw, binding=False)
            if isinstance(pat2, PVar):
                # a variable pattern is the scrutinee itself: it keeps the declared type, so a
                # value of a record type keeps its component names
                ctx2 = ctx2[:-1] + [(pat2.name, sty)]
            if isinstance(pat2, (PVar, PWild)):
                catch_all = True
            elif isinstance(pat2, PCon):
                covered.add(pat2.name)
            elif isinstance(pat2, PInj):
                covered.add(pat2.label)
            cond = None
            if isinstance(pat2, PInj) and pat2.index in (0, 1) and self.is_bool(sty):
                cond = scrut if pat2.index == 0 else App(Var("not"), scrut)
                self.path.append(cond)
            # `match e { x -> t }` and `match e { (x, y) -> t }` name e, or its components: an
            # obligation in t speaks of e, not of every x and y (05 §7)
            lets = _tuple_lets(pat2, scrut)
            let = bool(lets)
            for nm, tm in lets:
                self.lets.append((nm, tm))
            try:
                if result_ty is None:
                    body2, result_ty = self.infer(ctx2, body)
                else:
                    body2 = self.check(ctx2, body, result_ty)
            finally:
                if cond is not None:
                    self.path.pop()
                for _ in lets:
                    self.lets.pop()
            branches.append((pat2, body2))
        if isinstance(sw, Sum) and not catch_all:
            got = {p.index for p, _ in branches if isinstance(p, PInj)}
            missing = [l for i, (l, _) in enumerate(sw.alts) if i not in got]
            if missing:
                self.err(f"match on {pp(scrut)} does not cover: {', '.join(missing)}")
        h, _ = unapply(sw)
        if isinstance(h, Var) and h.name in self.env.datas and not catch_all:
            names = {c.name for c in self.env.datas[h.name].constructors}
            missing = names - covered
            if missing:
                self.err(f"match on {pp(scrut)} does not cover: {', '.join(sorted(missing))}")
        return Match(scrut, tuple(branches)), result_ty

    # ------------------------------------------------------------- sums
    def _type_operand(self, ctx: Ctx, t: BinOp, op: str = "+") -> bool:
        """Whether `a + b` (or `a * b`) is a sum (a product) of types: its leftmost operand is a type.
        Decided by the operand's form where it can be (a literal, a local of a type that is not U, an
        application of a function whose result is not a type), and by inferring it otherwise, once
        per operand: a chain `a + b + c` asks the question at every `+` about the same `a`."""
        x = t
        while isinstance(x, BinOp) and x.op == op:
            x = x.lhs
        quick = self._is_type_by_form(ctx, x)
        if quick is not None:
            return quick
        hit = self._operand_memo.get(id(x))
        if hit is not None and hit[0] is x and hit[1] is ctx:
            return hit[2]
        try:
            with self.silent():
                _, xt = self.infer(ctx, x)
            answer = isinstance(self.whnf(xt), Univ)
        except TypeCheckError:
            answer = False
        self._operand_memo[id(x)] = (x, ctx, answer)
        return answer

    def _is_type_by_form(self, ctx: Ctx, x: Term) -> Optional[bool]:
        """True or False when the form of a term says whether it is a type; None when it does not."""
        if isinstance(x, (Lit, Pair, Lam, RecordLit)):
            return False
        if isinstance(x, (Univ, Pi, Sigma, Sum, Subtype, Arrow)):
            return True
        h, args = unapply(x)
        if isinstance(h, Var):
            local = lookup(ctx, h.name)
            if local is not None:
                if args:
                    return None
                return isinstance(self.whnf(local), Univ)
            q = self.resolve(h.name)
            d = self.env.defs.get(q) if q is not None else None
            if d is not None and d.type is not None and not d.alias:
                cod = d.type
                for _ in args:
                    if not isinstance(cod, Pi):
                        return None
                    cod = cod.cod
                while isinstance(cod, Pi):
                    return False            # a function value, partially applied: not a type
                if isinstance(cod, Univ):
                    return True
                if isinstance(cod, Var) and cod.name in ("Int", "Float64", "Real", "String", "Bool"):
                    return False
        return None

    def try_injection(self, ctx: Ctx, t: Term, sm: Sum, ty: Term) -> Optional[Term]:
        """`label` or `label arg` checked against a sum with that label: the injection."""
        head, args = unapply(t)
        if not isinstance(head, Var) or lookup(ctx, head.name) is not None:
            return None
        labels = sm.labels()
        if head.name not in labels or len(args) > 1:
            return None
        i = labels.index(head.name)
        alt = sm.alts[i][1]
        if not args:
            if not self.is_unit(alt):
                return None      # a label of a non-unit alternative alone is the injection function
            return Inj(i, head.name, Con("unit"), ty)
        return Inj(i, head.name, self.check(ctx, args[0], alt), ty)

    def register_labels(self, qname: str, body: Term, ty: Term):
        """An alias whose body is a sum makes its labels usable without an expected type: a label
        of a unit alternative is a value, any other is the function into the sum (taking the
        alias's parameters first). A label two aliases share is usable only by the expected type."""
        params = []
        b = body
        while isinstance(b, Lam):
            params.append((b.param.name, b.ann))
            b = b.body
        if not isinstance(b, Sum):
            return
        for i, (label, _) in enumerate(b.alts):
            if label in self.labels and self.labels[label] is not None and self.labels[label][0] != qname:
                self.labels[label] = None
            elif label not in self.labels:
                self.labels[label] = (qname, i, params)

    def label_value(self, label: str):
        entry = self.labels[label]
        if entry is None:
            self.err(f"label {label} belongs to several sums: use it where the expected type is known")
        qname, i, params = entry
        sum_ty: Term = Var(qname)
        for n, _ in params:
            sum_ty = App(sum_ty, Var(n))
        w = self.whnf(sum_ty)
        alt = w.alts[i][1]
        if self.is_unit(alt):
            term = Inj(i, label, Con("unit"), sum_ty)
            ty = sum_ty
        else:
            x = fresh("x")
            term = Lam(PVar(x), Inj(i, label, Var(x), sum_ty), alt)
            ty = Pi("_", alt, sum_ty)
        for n, ann in reversed(params):
            term = Lam(PVar(n), term, ann)
            ty = Pi(n, ann, ty)
        return term, ty

    def contains_function(self, ty: Term, seen: Optional[set] = None) -> bool:
        """Whether `==` is not structural on values of `ty` (05 R8): they can contain a function, or a
        Real, whose equality is the axiom's and not computable. A data type is looked into through
        the types of its constructors, instantiated; one already being looked into adds nothing, so a
        recursive type ends without a depth cut that would let `==` through."""
        seen = set() if seen is None else seen
        w = self.whnf(self.base_type(ty))
        if isinstance(w, Var) and w.name == "Real":
            return True
        if isinstance(w, Pi):
            return True
        if isinstance(w, Sigma):
            return self.contains_function(w.fst, seen) or \
                self.contains_function(subst(w.snd, {w.name: Var(fresh(w.name))}), seen)
        if isinstance(w, Sum):
            return any(self.contains_function(a, seen) for _, a in w.alts)
        h, args = unapply(w)
        if isinstance(h, Var) and h.name in self.env.datas:
            key = pp(w)
            if key in seen:
                return False
            seen.add(key)
            for c in self.env.datas[h.name].constructors:
                cty = self.env.cons[c.name][1]
                for a in args:
                    cw = self.whnf(cty)
                    if not isinstance(cw, Pi):
                        break
                    cty = subst(cw.cod, {cw.name: a})
                cw = self.whnf(cty)
                while isinstance(cw, Pi):
                    if self.contains_function(cw.dom, seen):
                        return True
                    cw = self.whnf(cw.cod if cw.name == "_" else subst(cw.cod, {cw.name: Var(fresh(cw.name))}))
            return False
        return False

    def _mentions_real(self, ty: Term) -> bool:
        w = self.whnf(self.base_type(ty))
        return isinstance(w, Var) and w.name == "Real"

    def _is_type_term(self, a: Term) -> bool:
        try:
            with self.silent():
                _, at = self.infer([], a)
            return isinstance(self.whnf(at), Univ)
        except (TypeCheckError, EvalError):
            return False

    # ------------------------------------------------------------- patterns
    def bind_pattern(self, ctx: Ctx, p: Pattern, ty: Term, binding: bool = True):
        """Resolve constructor names in `p`, return (pattern, extended ctx).
        `binding`: lambda and subtype parameters always bind; in a match, a name that is a
        constructor of the scrutinee's type is a constructor pattern."""
        if isinstance(p, PWild):
            return p, ctx
        if isinstance(p, PVar):
            if not binding:
                sm = self.sum_of(ty)
                if sm is not None and p.name in sm.labels():
                    return self.bind_pattern(ctx, PCon(p.name, ()), ty, binding)
            q = self.resolve(p.name) if not binding else None
            if q is not None and q in self.env.cons and self._con_of_type(q, ty):
                return self.bind_pattern(ctx, PCon(q, ()), ty, binding)
            return p, ctx + [(p.name, ty)]
        if isinstance(p, PInj):
            sm = self.sum_of(ty)
            if sm is None or p.index >= len(sm.alts):
                self.err(f"pattern {pp_pat(p)} against {pp(ty)}, which is not a sum with that alternative")
            if isinstance(p.arg, PWild):
                return p, ctx
            a, ctx2 = self.bind_pattern(ctx, p.arg, sm.alts[p.index][1], binding)
            return PInj(p.index, p.label, a), ctx2
        if isinstance(p, PLit):
            return p, ctx
        w = self.whnf(self.base_type(ty))
        if isinstance(p, PPair):
            if not isinstance(w, Sigma):
                self.err(f"tuple pattern {pp_pat(p)} against non-pair type {pp(ty)}")
            f, ctx2 = self.bind_pattern(ctx, p.fst, w.fst, binding)
            ft = pattern_to_term(f)
            snd_ty = subst(w.snd, {w.name: ft}) if ft is not None else w.snd
            s, ctx3 = self.bind_pattern(ctx2, p.snd, snd_ty, binding)
            return PPair(f, s), ctx3
        if isinstance(p, PCon) and isinstance(w, Sum) and p.name in w.labels():
            i = w.labels().index(p.name)
            if not p.args:
                return PInj(i, p.name, PWild()), ctx
            if len(p.args) > 1:
                self.err(f"label {p.name} takes one pattern for its payload; group several with a tuple")
            a, ctx2 = self.bind_pattern(ctx, p.args[0], w.alts[i][1], binding)
            return PInj(i, p.name, a), ctx2
        if isinstance(p, PCon) and p.name in ("true", "false") and not p.args:
            # the labels of Bool are never a variable: `if c` on a sum of two other units, or a pattern
            # `true` against another type, would otherwise bind anything and take its branch always
            self.err(f"{p.name} is a label of Bool, and the value matched is of type {pp(ty)}: the condition "
                     f"of an if, and a match on true and false, need a Bool")
        if isinstance(p, PCon):
            q = self.resolve(p.name)
            if q is None or q not in self.env.cons:
                if not p.args:
                    return PVar(p.name), ctx + [(p.name, ty)]
                self.err(f"unknown constructor {p.name} in pattern")
            p = PCon(q, p.args)
            dname, full = self.env.cons[q]
            h, targs = unapply(w)
            if not (isinstance(h, Var) and h.name == dname):
                self.err(f"constructor {p.name} belongs to {dname}, but the scrutinee has type {pp(ty)}")
            cty = full
            for a in targs:
                if not isinstance(cty, Pi):
                    self.err(f"constructor {p.name}: too many type parameters")
                cty = subst(cty.cod, {cty.name: a})
            ctx2 = ctx
            args = []
            for q in p.args:
                if not isinstance(cty, Pi):
                    self.err(f"constructor {p.name} takes fewer arguments than the pattern {pp_pat(p)}")
                q2, ctx2 = self.bind_pattern(ctx2, q, cty.dom, binding)
                qt = pattern_to_term(q2)
                cty = subst(cty.cod, {cty.name: qt}) if qt is not None else cty.cod
                args.append(q2)
            if isinstance(cty, Pi):
                self.err(f"pattern {pp_pat(p)} does not bind all arguments of {p.name}")
            return PCon(p.name, tuple(args)), ctx2
        self.err(f"unknown pattern {p!r}")

    def _con_of_type(self, cname: str, ty: Term) -> bool:
        dname, _ = self.env.cons[cname]
        h, _ = unapply(self.whnf(self.base_type(ty)))
        return isinstance(h, Var) and h.name == dname


# ---------------------------------------------------------------- helpers of the object rules

def _tuple_lets(pat: Pattern, scrut: Term) -> list:
    """(variable, the term it names) for a pattern made of variables, wildcards and tuples."""
    def plain(p):
        return isinstance(p, (PVar, PWild)) or (isinstance(p, PPair) and plain(p.fst) and plain(p.snd))
    if not plain(pat):
        return []
    if isinstance(pat, PVar):
        return [(pat.name, scrut)]

    def keep_only(p, name):
        if isinstance(p, PVar):
            return p if p.name == name else PWild()
        if isinstance(p, PPair):
            return PPair(keep_only(p.fst, name), keep_only(p.snd, name))
        return p
    return [(v, Match(scrut, ((keep_only(pat, v), Var(v)),))) for v in pattern_vars(pat)]


def _pending_member(d: Def, existing: Def):
    """A Member-like view of a declared type defined in another file than its declaration."""
    from .graph import Member
    body = existing.body
    ctx = []
    while isinstance(body, Lam):
        ctx.append((body.param.name, body.ann))
        body = body.body
    m = Member("entry", d.name, d.line, decl=Def(d.name, existing.type, None, line=existing.line), defn=d,
               pending=True)
    m.base_ctx, m.base = ctx, body.base
    return m


def _readable_name(base: str, ctx: Ctx, value: Term) -> str:
    """A parameter name for an obligation that a reader can follow: the base, primed until it is
    neither bound in the context nor free in the value."""
    name = base.split("~")[0]
    taken = {n for n, _ in ctx} | free_vars(value)
    while name in taken:
        name += "'"
    return name


def _ends_in_universe(t: Term) -> bool:
    while isinstance(t, Pi):
        t = t.cod
    return isinstance(t, Univ)


def _peel_pi(t: Term):
    params = []
    while isinstance(t, Pi):
        params.append((t.name, t.dom))
        t = t.cod
    return params, t


def _apply_law(fn: Term, whole: Term) -> Term:
    """The predicate a law, or a conjunction of laws, states about the value `whole`."""
    if isinstance(fn, And):
        return And(_apply_law(fn.lhs, whole), _apply_law(fn.rhs, whole))
    if isinstance(fn, Lam) and isinstance(fn.param, PVar):
        return subst(fn.body, {fn.param.name: whole})
    return App(fn, whole)


def _projections_of(body: Term, param: str, labels: list) -> set:
    """Labels of `param` projected in `body`; all of them if `param` is used whole."""
    names = {l.split("~")[0]: l for l in labels}
    found = set()
    whole = [False]

    def walk(t):
        if isinstance(t, Match) and isinstance(t.scrut, Var) and t.scrut.name == param and len(t.branches) == 1:
            pat, b = t.branches[0]
            vs = [v for v in pattern_vars(pat)]
            if len(vs) == 1 and isinstance(b, Var) and b.name == vs[0]:
                lab = names.get(vs[0].split("~")[0])
                if lab is not None:
                    found.add(lab)
                    return
            for p_, b_ in t.branches:
                walk(b_)
            return
        if isinstance(t, Var):
            if t.name == param:
                whole[0] = True
            return
        for child in _children(t):
            walk(child)
    walk(body)
    return set(labels) if whole[0] else found


def _children(t: Term) -> list:
    if isinstance(t, App):
        return [t.fn, t.arg]
    if isinstance(t, Lam):
        return [t.body] + ([t.ann] if t.ann is not None else []) + ([t.res] if t.res is not None else [])
    if isinstance(t, (Pi,)):
        return [t.dom, t.cod]
    if isinstance(t, Sigma):
        return [t.fst, t.snd]
    if isinstance(t, (Pair,)):
        return [t.fst, t.snd]
    if isinstance(t, (BinOp, And, Arrow)):
        return [t.lhs, t.rhs]
    if isinstance(t, Match):
        return [t.scrut] + [b for _, b in t.branches]
    if isinstance(t, Subtype):
        return [t.base, t.pred]
    if isinstance(t, Sum):
        return [a for _, a in t.alts]
    if isinstance(t, Inj):
        return [t.arg] + ([t.type] if t.type is not None else [])
    if isinstance(t, Extern):
        return [t.type] if t.type is not None else []
    if isinstance(t, Forget):
        return [t.arg]
    return []


def _global_names(t: Term, bound=frozenset()) -> set:
    """The free names of an elaborated term (globals: locals are bound by its binders)."""
    out = set()

    def walk(t, bound):
        if isinstance(t, Var):
            if t.name not in bound:
                out.add(t.name)
            return
        if isinstance(t, Lam):
            if t.ann is not None:
                walk(t.ann, bound)
            inner = bound | set(pattern_vars(t.param))
            if t.res is not None:
                walk(t.res, inner)
            walk(t.body, inner)
            return
        if isinstance(t, Pi):
            walk(t.dom, bound)
            walk(t.cod, bound | {t.name})
            return
        if isinstance(t, Sigma):
            walk(t.fst, bound)
            walk(t.snd, bound | {t.name})
            return
        if isinstance(t, Subtype):
            walk(t.base, bound)
            walk(t.pred, bound | set(pattern_vars(t.param)))
            return
        if isinstance(t, Match):
            walk(t.scrut, bound)
            for p, b in t.branches:
                walk(b, bound | set(pattern_vars(p)))
            return
        if isinstance(t, Inj):
            walk(t.arg, bound)
            if t.type is not None:
                walk(t.type, bound)
            return
        for c in _children(t):
            walk(c, bound)
    walk(t, set(bound))
    return out
