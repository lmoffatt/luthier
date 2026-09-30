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

from .syntax import *
from .subst import subst, fresh, free_vars
from .pretty import pp, pp_pat
from .evaluator import (Env, ExternInfo, Fuel, whnf, conv, unapply, apply, as_bool,
                        EvalError, BUILTIN_TYPES)


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

    def is_type(self, ty: Term, name: str) -> bool:
        w = self.whnf(ty)
        return isinstance(w, Var) and w.name == name

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
        if isinstance(w, Pi):
            return self.is_law(subst(w.cod, {w.name: Var(fresh(w.name))}))
        return False

    # -------------------------------------------------------------- program
    def load(self, prog: Program):
        for d in prog.defs:
            self.add_def(d)
        for g in prog.gens:
            pass  # generators are registered by the test runner

    def add_def(self, d: Def):
        qname = self.qualify(d.name)
        self.current_def = qname
        try:
            existing = self.env.defs.get(qname)
            if existing is not None and (existing.body is not None or existing.data is not None):
                self.err(f"{qname} is defined twice")
            if qname in self.env.datas:
                self.err(f"{qname} is defined twice")
            if d.data is not None:
                if existing is not None:
                    self.err(f"{qname} was declared as a value, it cannot become a data type")
                self.add_data(d, qname)
                return
            ty = None
            if d.type is not None:
                ty = self.check([], d.type, Univ())
            if existing is not None:
                # filling a hole: the type must agree with the declaration
                if ty is not None and not self.conv(ty, existing.type):
                    self.err(f"{qname} was declared with type {pp(existing.type)}, but is defined with {pp(ty)}")
                ty = existing.type
            if d.body is None:
                if ty is None:
                    self.err(f"{qname} has neither type nor body")
                self.env.defs[qname] = Def(qname, ty, None, doc=d.doc)
                return
            if isinstance(d.body, Extern):
                if ty is None:
                    self.err(f"extern {qname} needs a type")
                ext = Extern(d.body.target, ty)
                self.register_extern(d.body.target, ty)
                self.env.defs[qname] = Def(qname, ty, ext, doc=d.doc)
                w = self.whnf(ty)
                if isinstance(w, Subtype):
                    # the environment's function is checked against the declared laws by `test`
                    self.subtype_obligation([], Var(qname), w, ty)
                return
            if ty is not None:
                # declare first so the body can be recursive
                self.env.defs[qname] = Def(qname, ty, None, doc=d.doc)
                body = self.check([], d.body, ty)
            else:
                if d.name in free_vars(d.body):
                    self.err(f"recursive definition {qname} needs a declared type")
                body, ty = self.infer([], d.body)
            self.env.defs[qname] = Def(qname, ty, body, doc=d.doc)
        finally:
            self.current_def = None

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
        self.env.externs[target] = ExternInfo(fn, pi_arity(base), base)

    def pi_chain(self, ty: Term) -> Term:
        """The type with subtypes stripped and each Pi exposed, so arity and result type can be read."""
        w = self.whnf(self.base_type(ty))
        if isinstance(w, Pi):
            return Pi(w.name, w.dom, self.pi_chain(w.cod))
        return w

    # ---------------------------------------------------------- obligations
    def add_obligation(self, ctx: Ctx, term: Term, label: str):
        if not self.recording or self.current_def is None:
            return
        name = self.current_def
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
            if q is None:
                if t.name in ("__nil__", "__cons__"):
                    self.err("a list literal needs an expected type or a first element")
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
                return t, Var("R")
            return t, Var("String")
        if isinstance(t, Univ):
            return t, Univ()
        if isinstance(t, Extern):
            if t.type is None:
                self.err("extern is only allowed as the body of a definition")
            return t, t.type
        if isinstance(t, App):
            return self.infer_app(ctx, t)
        if isinstance(t, Lam):
            if t.ann is None:
                self.err(f"cannot infer the type of {pp(t)}: annotate the parameter or give an expected type")
            dom = self.check(ctx, t.ann, Univ())
            param, ctx2 = self.bind_pattern(ctx, t.param, dom)
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
            if self.is_type(self.base_type(lt), "Bool"):
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
        self.err(f"cannot infer {t!r}")

    def infer_app(self, ctx: Ctx, t: App):
        f, fty = self.infer(ctx, t.fn)
        w = self.whnf(self.base_type(fty))
        if not isinstance(w, Pi):
            self.err(f"{pp(f)} : {pp(fty)} is not a function, cannot apply it to {pp(t.arg)}")
        a = self.check(ctx, t.arg, w.dom)
        return App(f, a), subst(w.cod, {w.name: a})

    def infer_binop(self, ctx: Ctx, t: BinOp):
        op = t.op
        if op in ("and", "or"):
            l = self.check(ctx, t.lhs, Var("Bool"))
            r = self.check(ctx, t.rhs, Var("Bool"))
            return App(App(Var(op), l), r), Var("Bool")
        l, lt = self.infer(ctx, t.lhs)
        if op == "*" and self.conv(lt, Univ()):
            r = self.check(ctx, t.rhs, Univ())
            return Sigma("_", l, r), Univ()
        if op in ("==", "/="):
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
        num = isinstance(bw, Var) and bw.name in ("Int", "R")
        if op == "+" and isinstance(bw, Var) and bw.name == "String":
            r = self.check(ctx, t.rhs, bt)
            return BinOp(op, l, r), bt
        if not num:
            self.err(f"operator {op} expects Int or R, got {pp(l)} : {pp(lt)}")
        r = self.check(ctx, t.rhs, bt)
        if op in ("<", "<=", ">", ">="):
            return BinOp(op, l, r), Var("Bool")
        return BinOp(op, l, r), bt

    # ---------------------------------------------------------------- check
    def check(self, ctx: Ctx, t: Term, ty: Term) -> Term:
        w = self.whnf(ty)
        if isinstance(t, Lam) and isinstance(w, Pi):
            if t.ann is not None:
                ann = self.check(ctx, t.ann, Univ())
                if not self.conv(ann, w.dom):
                    self.err(f"parameter {pp_pat(t.param)} annotated {pp(ann)} but expected {pp(w.dom)}")
            param, ctx2 = self.bind_pattern(ctx, t.param, w.dom)
            pt = pattern_to_term(param)
            cod = subst(w.cod, {w.name: pt}) if pt is not None else w.cod
            body = self.check(ctx2, t.body, cod)
            return Lam(param, body, w.dom)
        if isinstance(t, Pair) and isinstance(w, Sigma):
            a = self.check(ctx, t.fst, w.fst)
            b = self.check(ctx, t.snd, subst(w.snd, {w.name: a}))
            return Pair(a, b)
        if isinstance(t, Match):
            term, _ = self.check_match(ctx, t, ty)
            return term
        if isinstance(t, Var) and t.name == "__nil__" or (isinstance(t, App) and self._is_cons(t)):
            return self.check_list(ctx, t, w)
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
        return not isinstance(t, (Lam, Pair, Match)) and not (
            isinstance(t, Var) and t.name == "__nil__") and not (isinstance(t, App) and self._is_cons(t))

    def convertible(self, have: Term, want: Term) -> bool:
        """`have` is `want`, or a subtype of it (through any number of layers)."""
        cur = have
        for _ in range(32):
            if self.conv(cur, want):
                return True
            b = self.strip_subtype(cur)
            if b is None:
                return False
            cur = b
        return False

    def coerce(self, ctx: Ctx, term: Term, have: Term, want: Term) -> Term:
        cur = have
        for _ in range(32):
            if self.conv(cur, want):
                return term
            b = self.strip_subtype(cur)
            if b is None:
                break
            cur = b
        self.err(f"{pp(term)} has type {pp(have)} but {pp(want)} was expected")

    def subtype_obligation(self, ctx: Ctx, value: Term, sub: Subtype, ty: Term):
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
            if isinstance(pat2, (PVar, PWild)):
                catch_all = True
            elif isinstance(pat2, PCon):
                covered.add(pat2.name)
            if result_ty is None:
                body2, result_ty = self.infer(ctx2, body)
            else:
                body2 = self.check(ctx2, body, result_ty)
            branches.append((pat2, body2))
        h, _ = unapply(sw)
        if isinstance(h, Var) and h.name in self.env.datas and not catch_all:
            names = {c.name for c in self.env.datas[h.name].constructors}
            missing = names - covered
            if missing:
                self.err(f"match on {pp(scrut)} does not cover: {', '.join(sorted(missing))}")
        return Match(scrut, tuple(branches)), result_ty

    # ------------------------------------------------------------- patterns
    def bind_pattern(self, ctx: Ctx, p: Pattern, ty: Term, binding: bool = True):
        """Resolve constructor names in `p`, return (pattern, extended ctx).
        `binding`: lambda and subtype parameters always bind; in a match, a name that is a
        constructor of the scrutinee's type is a constructor pattern."""
        if isinstance(p, PWild):
            return p, ctx
        if isinstance(p, PVar):
            q = self.resolve(p.name) if not binding else None
            if q is not None and q in self.env.cons and self._con_of_type(q, ty):
                return self.bind_pattern(ctx, PCon(q, ()), ty, binding)
            return p, ctx + [(p.name, ty)]
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
