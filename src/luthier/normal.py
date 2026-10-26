"""The normal form of a law, and the core properties a law is an instance of.

Luciano's idea, 2026-10-27 (record/notes/idea-law-normal-form-2026-10-27.md): a law written ad hoc,
`ReadingSymmetric (t : Tape) (a b : Mark) : Bool := t.reading a b == t.reading b a`, is recognized as
the core's `Commutative Mark Float64 (structural Float64) t.reading` by a normal form: the free term
algebra over the operations and the law's variables, quotiented by the properties the operations
are certified to have, one representative chosen by an order with no meaning, and a dictionary from
normal forms to names. Built on the brief record/plan/law-normal-form-2026-10-27/prompt.md by Claude
Opus 5.5, an agent of the coordinating session, 2026-10-27. Deterministic, no seed. Every criterion
below is a parameter (P11): UNFOLD, EXACT, WITHIN, ALIASES, DICTIONARY_FILES, MAX_PERMUTATIONS,
FUEL, LABEL_ROUNDS.

The steps, as the brief numbers them:
1. `unfold`: the law's body with its definitions unfolded (delta) and reduced (beta, a record's
   projection, a `Let`), over the elaborated program `check.py`'s typing builds. [proposed] What is
   unfolded is a parameter, UNFOLD: a law or predicate (a definition at `Bool` whose name is
   capitalized, the library's convention for laws) and a model (a definition whose body is a record
   value, `structural`); a value function (`metres`, a distance) stays folded, since it is the
   operation a law is about; a definition by `match`, a primitive, an extern and a recursive
   definition stay folded too. Bound names compare up to alpha (`key`).
2. `prepare` and `sort`: the arguments of `==` and `/=` are sorted (the structural equality is
   symmetric exactly), those of `and` and `or` flattened and sorted, and those of an operation the
   core claims commutative exactly (EXACT, by the carrier the typing gives) sorted, flattened only
   where it claims it associative exactly. Floating-point `+` is commutative exactly and associative
   only within a bound (numbers.lth's `PlusAssociativeWithin`): its two arguments are sorted, never
   flattened. The order (`key`) is total and has no meaning: by the kind of term, then by name.
3. `normal_form`: the law's variables named by first occurrence in the ordered body, the order
   recomputed with those names, to a fixed point (LABEL_ROUNDS; a cycle takes its least form).
4. The operation abstracted: a core property's parameters, and the projections of its parameters
   (`o.eq`, `m.d`), are pattern variables; matching one against the law's normal form binds it to
   whatever head the law applies (`t.reading`, `+`, a function of the library), a first-order match
   on curried application, which is Miller's pattern fragment for the core's properties (a
   parameter applied to the quantified variables).
5. `dictionary`: the normal forms of the core's properties (DICTIONARY_FILES), each with its name;
   a property with an equality `o : Object B` is entered twice, as written and at `o = structural
   B`, where `o.eq` unfolds to `==`.
6. `recognize`: the core properties a law is an instance of, with the instantiation of their
   parameters, or nothing. A match is accepted when the property instantiated normalizes to the
   law's normal form exactly (`_verified`). [proposed] An instance of an exact property at an
   operation the core claims it of only within a bound (WITHIN: float associativity) is withheld:
   the law states what the core says the operation does not do.

Limits. It recognizes what the order decides and claims nothing on the rest: equality of programs
is undecidable (Richardson's theorem for the elementary functions), equations other than
commutativity and associativity would need completion (Knuth-Bendix), which may not terminate, and
a flattened operation is matched only at its arity (no matching modulo AC of a pattern variable
against part of a sum). A law that is a claim the normalization used (an integer associativity)
becomes `X == X` and is reported `trivial`, never recognized. Commuting `and` and `or` is exact
for the Boolean they denote, not for evaluation: one guarding the other's error is changed by it,
which a notice may do and a run may not.
"""
from __future__ import annotations

import functools
import itertools
from dataclasses import dataclass, fields, is_dataclass, replace
from pathlib import Path

from . import kernel, term as t

LIB = Path(__file__).resolve().parent / "lib"
CORE = LIB / "core"

# Step 5: the files whose capitalized Bool definitions are the core's properties (the brief's list;
# the structures' laws enter where they are single properties: a conjunction `&` never does).
DICTIONARY_FILES = ("properties/relations.lth", "properties/operations.lth", "properties/functions.lth",
                    "structures/equality.lth", "structures/algebraic.lth", "structures/order.lth",
                    "structures/containers.lth", "structures/universal.lth")

# Step 1: which definitions unfold. "laws and models" unfolds a capitalized definition at Bool and a
# definition whose body is a record value; "all" unfolds every non-recursive definition by a term.
UNFOLD = "laws and models"

# Step 2: what the core claims of its operations, by the operator and the carrier's base type.
# EXACT: the properties claimed exactly; sorting needs Commutative, flattening Associative.
# Sources: core.lut's `intIsACommutativeRingModel` (Int's + and *), `boolIsABooleanAlgebraModel`
# (and, or), numbers.lth's `Doubles` (Commutative on plus and times, line 155).
EXACT = {
    ("+", "Int"): frozenset({"Commutative", "Associative"}),
    ("*", "Int"): frozenset({"Commutative", "Associative"}),
    ("and", "Bool"): frozenset({"Commutative", "Associative"}),
    ("or", "Bool"): frozenset({"Commutative", "Associative"}),
    ("+", "Float64"): frozenset({"Commutative"}),
    ("*", "Float64"): frozenset({"Commutative"}),
}
# WITHIN: the properties claimed only within a bound (numbers.lth's PlusAssociativeWithin,
# TimesAssociativeWithin, TimesDistributiveWithin, DivideInvertibleWithin).
WITHIN = {
    ("+", "Float64"): frozenset({"Associative"}),
    ("*", "Float64"): frozenset({"Associative", "Distributive"}),
    ("/", "Float64"): frozenset({"Invertible"}),
}
# the comparisons symmetric exactly at every carrier (the structural equality, 4.R8)
SYMMETRIC = frozenset({"==", "/="})
# the core's names for its operators (core.lut binds `+` to intPlus and floatPlus, `and` to conj)
ALIASES = {"intPlus": "+", "floatPlus": "+", "intTimes": "*", "floatTimes": "*", "conj": "and", "disj": "or",
           "floatDivide": "/"}

MAX_PERMUTATIONS = 6   # the largest flattened node whose arguments the matcher permutes
FUEL = 400             # unfolding steps per law
LABEL_ROUNDS = 12      # rounds of step 3 before a cycle is cut


# ---------------------------------------------------------------------- terms

@dataclass(frozen=True)
class AC:
    """A node of the ordered form: an operator applied to its arguments, sorted when `commutative`,
    flattened when the operator is associative exactly."""
    op: str
    args: tuple
    commutative: bool


def spine(u):
    args = []
    while isinstance(u, t.App):
        args.append(u.argument)
        u = u.function
    return u, args[::-1]


def apps(h, args):
    for a in args:
        h = t.App(h, a)
    return h


def to_kernel(u):
    """An ordered form back to a kernel term (a flattened node nests to the left)."""
    if isinstance(u, AC):
        args = [to_kernel(a) for a in u.args]
        out = t.App(t.App(t.Var(u.op), args[0]), args[1])
        for a in args[2:]:
            out = t.App(t.App(t.Var(u.op), out), a)
        return out
    return _map(u, to_kernel)


def _map(u, f):
    """`u` with `f` applied to each of its children that is a term (or a pattern)."""
    def g(x):
        if isinstance(x, tuple):
            return tuple(g(y) for y in x)
        if is_dataclass(x) and not isinstance(x, type):
            return f(x)
        return x
    if isinstance(u, tuple):
        return g(u)
    if is_dataclass(u) and not isinstance(u, type):
        return replace(u, **{fl.name: g(getattr(u, fl.name)) for fl in fields(u)})
    return u


def free_vars(u, bound=frozenset()):
    """The free `Var` names of a term or ordered form."""
    if isinstance(u, AC):
        return set().union(*(free_vars(a, bound) for a in u.args))
    if isinstance(u, t.Lam):
        # an annotation is no part of the value (certify.erase, D-2026-10-15-e)
        return free_vars(u.body, bound | {u.name})
    if isinstance(u, (t.Pi, t.Sigma)):
        return free_vars(u.domain, bound) | free_vars(u.codomain, bound | {u.name})
    if isinstance(u, t.Var):
        return set() if u.name in bound else {u.name}
    if isinstance(u, t.Match):
        out = free_vars(u.value, bound)
        for p, b in u.arms:
            out |= free_vars(b, bound | set(kernel.pattern_names(p)))
        return out
    if isinstance(u, t.Let):
        return free_vars(u.value, bound) | free_vars(u.body, bound | {u.name})
    if isinstance(u, t.Subtype):
        return free_vars(u.type, bound) | free_vars(u.predicate, bound | {u.name})
    if isinstance(u, tuple):
        return set().union(set(), *(free_vars(x, bound) for x in u))
    if is_dataclass(u) and not isinstance(u, type) and not isinstance(u, (t.Lit,)):
        return set().union(set(), *(free_vars(getattr(u, fl.name), bound) for fl in fields(u)))
    return set()


# ---------------------------------------------------------------------- the order (step 2)

def key(u, labels=None, bound=()):
    """A total order on terms with no meaning: by the kind of term, then by name. A law's variable
    (`$i`) by its label (`labels`, step 3; its own name when None; all alike when `labels` is
    "anonymous"), a bound name by its de Bruijn index (alpha), a pattern variable and a global by
    name."""
    if isinstance(u, AC):
        return ("6a", ("3g", u.op), len(u.args), tuple(key(a, labels, bound) for a in u.args))
    if isinstance(u, t.Var):
        n = u.name
        if n in bound:
            return ("0b", bound[::-1].index(n))
        if n.startswith("$"):
            if labels == "anonymous":
                return ("1v", (2, ""))
            if labels is not None and n in labels:
                return ("1v", (0, labels[n]))
            return ("1v", (1, n))
        if n.startswith("?"):
            return ("2p", n)
        return ("3g", n)
    if isinstance(u, t.Lit):
        return ("4l", type(u.constant).__name__, repr(u.constant.value))
    if isinstance(u, t.Proj):
        return ("5r", key(u.record, labels, bound), u.label)
    if isinstance(u, t.App):
        h, args = spine(u)
        return ("6a", key(h, labels, bound), len(args), tuple(key(a, labels, bound) for a in args))
    if isinstance(u, t.Lam):
        return ("7f", key(u.body, labels, bound + (u.name,)))
    if isinstance(u, t.Let):
        return ("7l", key(u.value, labels, bound), key(u.body, labels, bound + (u.name,)))
    if isinstance(u, t.Match):
        arms = []
        for p, b in u.arms:
            names = tuple(dict.fromkeys(kernel.pattern_names(p)))
            q = kernel._map_pattern(p, lambda x: "#" if x in names else x)
            arms.append((repr(q), key(b, labels, bound + names)))
        return ("8m", key(u.value, labels, bound), tuple(arms))
    if isinstance(u, t.RecordValue):
        return ("9r", tuple((n, key(v, labels, bound)) for n, v in u.fields))
    if isinstance(u, tuple):
        return ("zt", tuple(key(x, labels, bound) for x in u))
    if is_dataclass(u) and not isinstance(u, type):
        return ("z", type(u).__name__, tuple(key(getattr(u, fl.name), labels, bound) if not isinstance(getattr(u, fl.name), str)
                                              else ("s", getattr(u, fl.name)) for fl in fields(u)))
    return ("zz", repr(u))


# ---------------------------------------------------------------------- the program a law lives in

class Env:
    """The elaborated program a law is read in: its definitions (the file's, its imports' and the
    core dictionary files'), and the typing that gives a term's type (check.py's `Typing`)."""

    def __init__(self, typing, extra=()):
        self.typing = typing
        self.defs = {}
        for act in tuple(extra) + tuple(typing.program):
            if isinstance(act, t.Define):
                self.defs[act.name] = act

    @functools.cached_property
    def _ctx(self):
        c = self.typing.context.child()
        c.types.update(self.typing.types)
        return c

    def type_of(self, u, ctx):
        from .elaborate import infer, as_type, ElaborationError
        c = self._ctx.child()
        c.types.update(ctx)
        try:
            ty = infer(u, c)
        except (ElaborationError, RecursionError, KeyError, TypeError, AttributeError):
            return None
        return None if isinstance(ty, t.Hole) else as_type(ty)

    def carrier(self, ty):
        """The base type's name (`Mark` is `Int`, `Moderate` is `Float64`), or None."""
        from .elaborate import base
        if ty is None:
            return None
        try:
            b = base(ty, self._ctx)
        except Exception:  # a type the elaborator cannot unfold has no known carrier
            return None
        return b.name if isinstance(b, t.Var) else None

    def unfoldable(self, name, policy=None):
        policy = policy or UNFOLD
        d = self.defs.get(name)
        if d is None:
            return None
        core = d.body
        while isinstance(core, t.Lam):
            core = core.body
        if isinstance(core, (t.Primitive, t.Extern, t.Axiom, t.Data, t.Match, t.Hole)):
            return None
        if name in kernel.free_names(d.body):
            return None
        result = d.type
        while isinstance(result, t.Pi):
            result = result.codomain
        if isinstance(result, t.Universe):
            return None
        if policy == "all":
            return d.body
        law = result == t.Var("Bool") and name[:1].isupper()
        model = isinstance(core, t.RecordValue)
        return d.body if law or model else None


# ---------------------------------------------------------------------- step 1: delta, beta

class _Fuel:
    def __init__(self, n):
        self.n = n


def unfold(u, env, fuel=None, bound=frozenset()):
    """The term with definitions unfolded (UNFOLD) and beta, a record's projection and a `Let`
    reduced, everywhere, within FUEL unfolding steps."""
    fuel = fuel if isinstance(fuel, _Fuel) else _Fuel(FUEL if fuel is None else fuel)
    return _unfold(u, env, fuel, bound)


def _head_step(h, env, fuel, bound):
    if isinstance(h, t.Var) and h.name not in bound and fuel.n > 0:
        body = env.unfoldable(h.name)
        if body is not None:
            fuel.n -= 1
            return body
    if isinstance(h, t.Let):
        return kernel.substitute(h.name, h.value, h.body)
    if isinstance(h, t.Proj):
        r = _unfold(h.record, env, fuel, bound)
        if isinstance(r, t.RecordValue):
            for n, v in r.fields:
                if n == h.label:
                    return v
        return None if r == h.record else t.Proj(r, h.label)
    return None


def _unfold(u, env, fuel, bound):
    if isinstance(u, (t.App, t.Var, t.Proj, t.Let)):
        h, args = spine(u)
        while True:
            if isinstance(h, t.Lam) and args:
                h = kernel.substitute(h.name, args[0], h.body)
                args = args[1:]
                continue
            if isinstance(h, t.App):
                h, more = spine(h)
                args = more + args
                continue
            nxt = _head_step(h, env, fuel, bound)
            if nxt is None or nxt == h:
                break
            h = nxt
        if not isinstance(h, (t.Var, t.Proj)):
            h = _unfold(h, env, fuel, bound)
        return apps(h, [_unfold(a, env, fuel, bound) for a in args])
    if isinstance(u, t.Lam):
        return t.Lam(u.name, u.type, _unfold(u.body, env, fuel, bound | {u.name}))
    if isinstance(u, t.Match):
        arms = tuple((p, _unfold(b, env, fuel, bound | set(kernel.pattern_names(p)))) for p, b in u.arms)
        return t.Match(_unfold(u.value, env, fuel, bound), arms)
    if isinstance(u, t.RecordValue):
        return t.RecordValue(tuple((n, _unfold(v, env, fuel, bound)) for n, v in u.fields))
    if isinstance(u, t.Pair):
        return t.Pair(_unfold(u.left, env, fuel, bound), _unfold(u.right, env, fuel, bound))
    if isinstance(u, t.Inj):
        return t.Inj(u.label, _unfold(u.value, env, fuel, bound))
    return u


# ---------------------------------------------------------------------- step 2: the quotient

def _claims(op, carrier):
    op = ALIASES.get(op, op)
    if op in SYMMETRIC:
        return op, frozenset({"Commutative"})
    if op in ("and", "or"):
        return op, EXACT[(op, "Bool")]
    return op, EXACT.get((op, carrier), frozenset())


def prepare(u, env, ctx, bound=()):
    """The ordered form's skeleton: each application of an operator the core claims commutative
    exactly becomes an `AC` node, flattened where it claims it associative exactly; the carrier is
    the base type of the first argument (`Env.carrier`)."""
    if isinstance(u, t.App):
        h, args = spine(u)
        args = [prepare(a, env, ctx, bound) for a in args]
        if isinstance(h, t.Var) and h.name not in bound and len(args) == 2:
            name = ALIASES.get(h.name, h.name)
            carrier = None
            if name not in SYMMETRIC and name not in ("and", "or"):
                carrier = env.carrier(env.type_of(to_kernel(args[0]), ctx)) if env is not None else None
            op, claims = _claims(h.name, carrier)
            if "Commutative" in claims or "Associative" in claims:
                flat = []
                for a in args:
                    if "Associative" in claims and isinstance(a, AC) and a.op == op:
                        flat.extend(a.args)
                    else:
                        flat.append(a)
                return AC(op, tuple(flat), "Commutative" in claims)
            h = t.Var(name) if name != h.name else h
        else:
            h = prepare(h, env, ctx, bound) if not isinstance(h, t.Var) else h
        return apps(h, args)
    if isinstance(u, t.Lam):
        inner = dict(ctx)
        inner[u.name] = u.type
        return t.Lam(u.name, u.type, prepare(u.body, env, inner, bound + (u.name,)))
    if isinstance(u, t.Match):
        arms = tuple((p, prepare(b, env, ctx, bound + tuple(kernel.pattern_names(p)))) for p, b in u.arms)
        return t.Match(prepare(u.value, env, ctx, bound), arms)
    if isinstance(u, t.Proj):
        return t.Proj(prepare(u.record, env, ctx, bound), u.label)
    if isinstance(u, t.RecordValue):
        return t.RecordValue(tuple((n, prepare(v, env, ctx, bound)) for n, v in u.fields))
    if isinstance(u, t.Let):
        return t.Let(u.name, u.type, prepare(u.value, env, ctx, bound), prepare(u.body, env, ctx, bound + (u.name,)))
    return u


def sort(u, labels=None, bound=()):
    """Each commutative node's arguments in the order `key` gives, bottom up."""
    if isinstance(u, AC):
        args = tuple(sort(a, labels, bound) for a in u.args)
        if u.commutative:
            args = tuple(sorted(args, key=lambda a: key(a, labels, bound)))
        return AC(u.op, args, u.commutative)
    if isinstance(u, t.App):
        return t.App(sort(u.function, labels, bound), sort(u.argument, labels, bound))
    if isinstance(u, t.Lam):
        return t.Lam(u.name, u.type, sort(u.body, labels, bound + (u.name,)))
    if isinstance(u, t.Let):
        return t.Let(u.name, u.type, sort(u.value, labels, bound), sort(u.body, labels, bound + (u.name,)))
    if isinstance(u, t.Match):
        return t.Match(sort(u.value, labels, bound),
                       tuple((p, sort(b, labels, bound + tuple(kernel.pattern_names(p)))) for p, b in u.arms))
    if isinstance(u, t.Proj):
        return t.Proj(sort(u.record, labels, bound), u.label)
    if isinstance(u, t.RecordValue):
        return t.RecordValue(tuple((n, sort(v, labels, bound)) for n, v in u.fields))
    return u


# ---------------------------------------------------------------------- step 3: the variables

def occurrences(u, out=None, bound=()):
    """The law's variables (`$i`) in the order they first occur, in preorder."""
    out = [] if out is None else out
    if isinstance(u, t.Var):
        if u.name.startswith("$") and u.name not in bound and u.name not in out:
            out.append(u.name)
    elif isinstance(u, AC):
        for a in u.args:
            occurrences(a, out, bound)
    elif isinstance(u, t.App):
        h, args = spine(u)
        for x in [h] + args:
            occurrences(x, out, bound)
    elif isinstance(u, t.Lam):
        occurrences(u.body, out, bound + (u.name,))
    elif isinstance(u, t.Let):
        occurrences(u.value, out, bound)
        occurrences(u.body, out, bound + (u.name,))
    elif isinstance(u, t.Match):
        occurrences(u.value, out, bound)
        for p, b in u.arms:
            occurrences(b, out, bound + tuple(kernel.pattern_names(p)))
    elif isinstance(u, t.Proj):
        occurrences(u.record, out, bound)
    elif isinstance(u, t.RecordValue):
        for _, v in u.fields:
            occurrences(v, out, bound)
    elif isinstance(u, t.Pair):
        occurrences(u.left, out, bound)
        occurrences(u.right, out, bound)
    elif isinstance(u, t.Inj):
        occurrences(u.value, out, bound)
    return out


def canonical_labels(prepared, variables=()):
    """Step 3: the variables named by first occurrence in the ordered body, the body ordered again
    with those names, to a fixed point; a cycle is cut at its least ordered form. The first round
    orders with every variable alike. Variables that do not occur follow, in their order."""
    def labels_of(order):
        order = order + [v for v in variables if v not in order]
        return {v: i for i, v in enumerate(order)}
    labels = labels_of(occurrences(sort(prepared, "anonymous")))
    seen = []
    for _ in range(LABEL_ROUNDS):
        ordered = sort(prepared, labels)
        new = labels_of(occurrences(ordered))
        if new == labels:
            return labels
        if new in seen:
            cycle = seen[seen.index(new):]
            return min(cycle, key=lambda ls: key(sort(prepared, ls), ls))
        seen.append(labels)
        labels = new
    return labels


# ---------------------------------------------------------------------- a law

@dataclass
class Law:
    """A law as the normal form reads it: its name, its parameters (renamed `$0`, `$1`, ... in
    order, with their types and written names) and its body over them."""
    name: str
    params: tuple       # (internal name, written name, type)
    body: t.Term        # over the internal names
    env: Env

    @property
    def ctx(self):
        return {n: ty for n, _, ty in self.params}

    @property
    def written(self):
        return {n: w for n, w, _ in self.params}


def law_of(act, env, prefix="$"):
    """A definition as a law: its leading lambdas are its parameters, renamed `prefix` and their
    position (innermost first, so a shadowed name is the inner one)."""
    body, params = act.body, []
    while isinstance(body, t.Lam):
        params.append((body.name, body.type))
        body = body.body
    internal = [f"{prefix}{i}" for i in range(len(params))]
    for i in reversed(range(len(params))):
        body = kernel.substitute(params[i][0], t.Var(internal[i]), body)
    types = []
    for i, (n, ty) in enumerate(params):
        for j in reversed(range(i)):
            ty = kernel.substitute(params[j][0], t.Var(internal[j]), ty)
        types.append(ty)
    return Law(act.name, tuple(zip(internal, (n for n, _ in params), types)), body, env)


def is_law(act):
    """A definition at `Bool` with parameters, no conjunction `&` of laws in its body."""
    if not isinstance(act, t.Define) or not isinstance(act.body, t.Lam):
        return False
    result = act.type
    while isinstance(result, t.Pi):
        result = result.codomain
    return result == t.Var("Bool") and "&" not in kernel.free_names(act.body)


@dataclass(frozen=True)
class Normal:
    """A law's normal form: the ordered body (`form`, its variables named `v0`, `v1`, ... by step
    3) and the labels of the law's internal names."""
    form: object
    labels: dict

    def __eq__(self, other):
        return isinstance(other, Normal) and key(self.form) == key(other.form)

    def __hash__(self):
        return hash(key(self.form))


def ordered(law):
    """Steps 1 and 2 on a law's body: unfolded, its operators' nodes prepared."""
    return prepare(unfold(law.body, law.env), law.env, law.ctx)


def normal_form(law):
    """Steps 1 to 3: the body unfolded, ordered, its variables named canonically."""
    prepared = ordered(law)
    labels = canonical_labels(prepared, [n for n, _, _ in law.params])
    form = sort(prepared, labels)
    names = {n: t.Var(f"v{i}") for n, i in labels.items()}
    return Normal(_rename(form, names), labels)


def _rename(u, names, bound=()):
    if isinstance(u, t.Var):
        return names.get(u.name, u) if u.name not in bound else u
    if isinstance(u, AC):
        return AC(u.op, tuple(_rename(a, names, bound) for a in u.args), u.commutative)
    if isinstance(u, t.Lam):
        return t.Lam(u.name, u.type, _rename(u.body, names, bound + (u.name,)))
    if isinstance(u, t.Let):
        return t.Let(u.name, u.type, _rename(u.value, names, bound), _rename(u.body, names, bound + (u.name,)))
    if isinstance(u, t.Match):
        return t.Match(_rename(u.value, names, bound),
                       tuple((p, _rename(b, names, bound + tuple(kernel.pattern_names(p)))) for p, b in u.arms))
    if isinstance(u, t.App):
        return t.App(_rename(u.function, names, bound), _rename(u.argument, names, bound))
    if isinstance(u, t.Proj):
        return t.Proj(_rename(u.record, names, bound), u.label)
    if isinstance(u, t.RecordValue):
        return t.RecordValue(tuple((n, _rename(v, names, bound)) for n, v in u.fields))
    if isinstance(u, t.Pair):
        return t.Pair(_rename(u.left, names, bound), _rename(u.right, names, bound))
    if isinstance(u, t.Inj):
        return t.Inj(u.label, _rename(u.value, names, bound))
    return u


def trivial(law):
    """Whether the law's normal form is `X == X`: true by the claims the quotient used (an integer
    associativity written out), so an instance of nothing."""
    form = normal_form(law).form
    return isinstance(form, AC) and form.op == "==" and len(form.args) == 2 and key(form.args[0]) == key(form.args[1])


# ---------------------------------------------------------------------- step 5: the dictionary

@dataclass
class Entry:
    """A core property in the dictionary: its name, file, parameters (pattern names `?x`, written
    names, types over the written names), which are types (`U`), the equalities set to `structural`
    in this variant, its body unfolded over the pattern names (kernel form) and prepared."""
    name: str
    file: str
    params: tuple       # (pattern name, written name, type)
    type_params: frozenset
    structural: tuple   # written names of the `Object` parameters set to `structural B`
    body: t.Term
    prepared: object

    def __repr__(self):
        at = f" at {', '.join(self.structural)} structural" if self.structural else ""
        return f"<Entry {self.name}{at}>"


def _chains(u, params):
    """A projection chain rooted at a parameter (`?o.eq`) becomes one pattern variable (`?o:eq`)."""
    if isinstance(u, t.Proj):
        inner = _chains(u.record, params)
        if isinstance(inner, t.Var) and inner.name in params:
            return t.Var(inner.name + ":" + u.label)
        return t.Proj(inner, u.label)
    if isinstance(u, AC):
        return AC(u.op, tuple(_chains(a, params) for a in u.args), u.commutative)
    if isinstance(u, t.Var):
        return u
    return _map(u, lambda x: _chains(x, params))


def _object_param(ty):
    """The carrier `X` of a parameter typed `Object X`, or None."""
    if isinstance(ty, t.App) and ty.function == t.Var("Object"):
        return ty.argument
    return None


def entries_of(act, env, file=""):
    """The dictionary's entries of one core property: as written, and with each subset of its
    equalities `o : Object X` set to `structural X` (D-2026-10-12-ak: every concrete type's)."""
    law = law_of(act, env, prefix="?")
    params = tuple((n, w, ty) for n, w, ty in law.params)
    written_types = []
    body0 = act.body
    while isinstance(body0, t.Lam):
        written_types.append((body0.name, body0.type))
        body0 = body0.body
    type_params = frozenset(w for (n, w, _), (_, ty) in zip(params, written_types) if isinstance(ty, t.Universe))
    objects = [(n, w, _object_param(ty)) for (n, w, _), (_, ty) in zip(params, written_types) if _object_param(ty) is not None]
    out, forms = [], set()
    for k in range(len(objects) + 1):
        for chosen in itertools.combinations(objects, k):
            body = law.body
            for n, w, carrier in chosen:
                # the carrier over the pattern names (`B` -> `?B`)
                c = carrier
                for pn, pw, _ in params:
                    c = kernel.substitute(pw, t.Var(pn), c)
                body = kernel.substitute(n, t.App(t.Var("structural"), c), body)
            unfolded = unfold(body, env)
            names = {n for n, _, _ in params}
            prepared = _chains(prepare(unfolded, None, {}), names)
            if key(prepared) in forms or "&" in free_vars(unfolded):
                continue
            forms.add(key(prepared))
            out.append(Entry(act.name, file, tuple((n, w, ty) for (n, w, _), (_, ty) in zip(params, written_types)),
                             type_params, tuple(w for _, w, _ in chosen), _chains(unfolded, names), prepared))
    return out


@functools.cache
def core_env():
    """The core's dictionary files read together (check.py's typing of each, with its imports),
    with core.lut's `structural`."""
    from .check import Program, load_imports, hidden_constructors, typing_of
    from .parse import parse
    acts, programs = {}, []
    for rel in DICTIONARY_FILES:
        path = CORE / rel
        program = Program(parse(path.read_text(encoding="utf-8")).program)
        program.imported = load_imports(program, path)
        program.hidden = hidden_constructors(program, program.imported)
        q = typing_of(program)
        programs.append((rel, q, {a.name for a in program if hasattr(a, "name")}))
    structural = _core_definition("structural")
    return programs, structural


@functools.cache
def _core_definition(name):
    from .elaborate import elaborate_program, context_of
    from .parse import parse
    program = parse((CORE / "core.lut").read_text(encoding="utf-8")).program
    act = next(a for a in program if getattr(a, "name", None) == name and type(a).__name__ == "Define")
    return next(a for a in elaborate_program((act,), context_of((act,))) if isinstance(a, t.Define))


@functools.cache
def dictionary():
    """Step 5: the normal forms of the core's properties, each with its name: every capitalized
    definition at `Bool` of DICTIONARY_FILES that is a single property (no `&`), in each variant
    of its equalities."""
    programs, structural = core_env()
    extra = [structural] + [a for _, q, _ in programs for a in q.program if isinstance(a, t.Define)]
    out, seen = [], set()
    for rel, q, own in programs:
        env = Env(q, extra)
        for act in q.program:
            if isinstance(act, t.Define) and act.name in own and act.name[:1].isupper() and is_law(act) \
                    and act.name not in seen:
                seen.add(act.name)
                out.extend(entries_of(act, env, rel))
    return tuple(out)


@functools.cache
def core_definitions():
    """The core's definitions a law's unfolding may reach (its properties, `structural`)."""
    programs, structural = core_env()
    return (structural,) + tuple(a for _, q, _ in programs for a in q.program if isinstance(a, t.Define))


# ---------------------------------------------------------------------- step 4: matching

def _view(u):
    """A node as (head, arguments, permutable)."""
    if isinstance(u, AC):
        return t.Var(u.op), list(u.args), u.commutative
    if isinstance(u, t.App):
        h, args = spine(u)
        return h, args, False
    return None


def atom(u):
    """A term a property's parameter may stand for in an argument's position: a variable, a
    projection of one (`p.a`, `t.neutral`), a literal or a global name; never an application."""
    while isinstance(u, t.Proj):
        u = u.record
    return isinstance(u, (t.Var, t.Lit))


def _bindable(name, u, head):
    """Step 4's restriction (Miller's pattern fragment, read on the core's properties): a parameter
    in a head's position stands for a head (an atom, or one applied to atoms: `t.reading`, `dist
    p`), one in an argument's position for an atom; a projection of a parameter (`o.eq`) never for
    the structural equality, which the variant at `structural` states."""
    if ":" in name and isinstance(u, t.Var) and u.name in SYMMETRIC:
        return False
    if head:
        h, args = spine(u)
        return atom(h) and all(atom(a) for a in args)
    return atom(u)


def match(p, u, sigma, bound=(), head=False):
    """The substitutions of the pattern variables (`?x`, `?o:eq`) that make `p` the term `u`, up to
    the order of the arguments of a commutative node; a generator."""
    if isinstance(p, t.Var) and p.name.startswith("?"):
        if free_vars(u) & set(bound) or not _bindable(p.name, u, head):
            return
        if p.name in sigma:
            if key(sigma[p.name]) == key(u):
                yield sigma
            return
        yield {**sigma, p.name: u}
        return
    pv, uv = _view(p), _view(u)
    if pv is not None and uv is not None:
        (ph, pargs, _), (uh, uargs, perm) = pv, uv
        if isinstance(p, AC) != isinstance(u, AC) and (len(pargs) != 2 or len(uargs) != 2):
            return
        extra = len(uargs) - len(pargs)
        if extra < 0 or (extra and (isinstance(u, AC) or not (isinstance(ph, t.Var) and ph.name.startswith("?")))):
            return
        head = apps(uh, uargs[:extra]) if extra else uh
        rest = uargs[extra:]
        orders = itertools.permutations(rest) if perm and len(rest) <= MAX_PERMUTATIONS else [rest]
        for order in orders:
            for s1 in match(ph, head, sigma, bound, head=True):
                yield from _match_all(pargs, list(order), s1, bound)
        return
    if type(p) is not type(u):
        return
    if isinstance(p, t.Var):
        if key(p, None, bound) == key(u, None, bound):
            yield sigma
        return
    if isinstance(p, t.Lam):
        # binders matched by position: the pattern's name is renamed to the term's
        yield from match(_rename(p.body, {p.name: t.Var(u.name)}), u.body, sigma, bound + (u.name,))
        return
    if isinstance(p, t.Proj):
        if p.label == u.label:
            yield from match(p.record, u.record, sigma, bound)
        return
    if isinstance(p, t.Lit):
        if key(p) == key(u):
            yield sigma
        return
    if isinstance(p, t.RecordValue):
        if [n for n, _ in p.fields] == [n for n, _ in u.fields]:
            yield from _match_all([v for _, v in p.fields], [v for _, v in u.fields], sigma, bound)
        return
    if isinstance(p, t.Match):
        if len(p.arms) != len(u.arms):
            return
        for s1 in match(p.value, u.value, sigma, bound):
            yield from _match_arms(p.arms, u.arms, s1, bound)
        return
    if isinstance(p, (t.Pi, t.Sigma)):
        for s1 in match(p.domain, u.domain, sigma, bound):
            yield from match(_rename(p.codomain, {p.name: t.Var(u.name)}), u.codomain, s1, bound + (u.name,))
        return
    if is_dataclass(p) and not isinstance(p, type) and not isinstance(p, (t.Lit, t.Primitive, t.Extern, t.Axiom)):
        # any other node (a record type, an injection, a pair): field by field
        ps, us = [], []
        for fl in fields(p):
            a, b = getattr(p, fl.name), getattr(u, fl.name)
            if isinstance(a, str) or not (is_dataclass(a) or isinstance(a, tuple)):
                if a != b:
                    return
            else:
                ps.append(a)
                us.append(b)
        yield from _match_all(ps, us, sigma, bound)
        return
    if isinstance(p, tuple) and isinstance(u, tuple):
        if len(p) == len(u) and all(isinstance(a, str) == isinstance(b, str) for a, b in zip(p, u)):
            if all(a == b for a, b in zip(p, u) if isinstance(a, str)):
                yield from _match_all([a for a in p if not isinstance(a, str)], [b for b in u if not isinstance(b, str)],
                                      sigma, bound)
        return
    if key(p, None, bound) == key(u, None, bound):
        yield sigma


def _match_arms(ps, us, sigma, bound):
    """A match's arms, in order: the same pattern up to its variables' names, then the bodies with
    the pattern's names renamed to the term's."""
    if not ps:
        yield sigma
        return
    (pp, pb), (up, ub) = ps[0], us[0]
    pn = tuple(dict.fromkeys(kernel.pattern_names(pp)))
    un = tuple(dict.fromkeys(kernel.pattern_names(up)))
    if len(pn) != len(un):
        return
    rename = dict(zip(pn, un))
    if kernel._map_pattern(pp, lambda x: rename.get(x, x)) != up:
        return
    for s1 in match(_rename(pb, {a: t.Var(b) for a, b in rename.items()}), ub, sigma, bound + un):
        yield from _match_arms(ps[1:], us[1:], s1, bound)


def _match_all(ps, us, sigma, bound):
    if len(ps) != len(us):
        return
    if not ps:
        yield sigma
        return
    for s1 in match(ps[0], us[0], sigma, bound):
        yield from _match_all(ps[1:], us[1:], s1, bound)


# ---------------------------------------------------------------------- step 6: recognition

@dataclass(frozen=True)
class Instance:
    """A law recognized as a core property: the property, its variant's `structural` equalities,
    and each parameter with the law's term it is (written by `show`), in the property's order."""
    law: str
    property: str
    file: str
    at: tuple           # (parameter, shown term)

    def notice(self):
        return f"{self.law} is {self.property} at " + ", ".join(f"{p} = {v}" for p, v in self.at)


def _instantiate(u, sigma):
    if isinstance(u, t.Var) and u.name in sigma:
        return sigma[u.name]
    if isinstance(u, t.Var):
        return u
    return _map(u, lambda x: _instantiate(x, sigma))


def _verified(entry, sigma, law, target):
    """The property's body with `sigma`, normalized as the law is, equals the law's ordered body."""
    body = _instantiate(entry.body, {k: to_kernel(v) for k, v in sigma.items()})
    if any(n.startswith("?") for n in free_vars(body)):
        return False
    mine = sort(prepare(unfold(body, law.env), law.env, law.ctx), None)
    return key(mine) == key(target)


def _unify(pattern, actual, variables, tsub):
    if isinstance(pattern, t.Var) and pattern.name in variables:
        tsub.setdefault(pattern.name, actual)
        return
    if isinstance(pattern, t.Pi) and isinstance(actual, t.Pi):
        _unify(pattern.domain, actual.domain, variables, tsub)
        _unify(pattern.codomain, actual.codomain, variables, tsub)
    elif isinstance(pattern, t.App) and isinstance(actual, t.App):
        _unify(pattern.function, actual.function, variables, tsub)
        _unify(pattern.argument, actual.argument, variables, tsub)


def _withheld(entry, sigma, law, tsub):
    """An exact property instantiated at an operator the core claims it of only within a bound."""
    for n, w, ty in entry.params:
        image = sigma.get(n)
        if not isinstance(image, t.Var) or image.name.startswith("$"):
            continue
        op = ALIASES.get(image.name, image.name)
        ty = _subst_types(ty, tsub)
        carrier = law.env.carrier(ty.domain) if isinstance(ty, t.Pi) else None
        if entry.name in WITHIN.get((op, carrier), ()) and entry.name not in EXACT.get((op, carrier), ()):
            return True
    return False


def _subst_types(ty, tsub):
    for v, a in tsub.items():
        ty = kernel.substitute(v, a, ty)
    return ty


def recognize(law):
    """Step 6: the core properties `law` is an instance of, each with its instantiation; [] when
    none is found (which claims nothing)."""
    target = sort(ordered(law), None)
    found, seen = [], set()
    for entry in dictionary():
        for sigma in match(entry.prepared, target, {}):
            sigma = {k: to_kernel(v) for k, v in sigma.items()}
            if not _verified(entry, sigma, law, target):
                continue
            images = [key(v) for v in sigma.values()]
            if len(set(images)) != len(images):
                continue
            tsub = {}
            ordered_params = sorted(entry.params, key=lambda p: not (isinstance(p[2], t.Var) and p[2].name in entry.type_params))
            for n, w, ty in ordered_params:
                if n in sigma:
                    actual = law.env.type_of(sigma[n], law.ctx)
                    if actual is not None:
                        _unify(ty, actual, entry.type_params, tsub)
            if _withheld(entry, sigma, law, tsub):
                continue
            at = []
            for n, w, ty in entry.params:
                if w in entry.type_params:
                    value = tsub.get(w, sigma.get(n))
                    at.append((w, show(value, law.written) if value is not None else "?"))
                elif w in entry.structural:
                    carrier = _object_param(ty)
                    carrier = _subst_types(carrier, tsub) if carrier is not None else None
                    at.append((w, "structural " + _atom(carrier, law.written) if carrier is not None else "structural ?"))
                elif n in sigma:
                    at.append((w, show(sigma[n], law.written)))
                else:
                    chains = sorted((k.split(":", 1)[1], v) for k, v in sigma.items() if k.startswith(n + ":"))
                    if chains:
                        at.append((w, "{ " + ", ".join(f"{lab} := {show(v, law.written)}" for lab, v in chains) + " }"))
                    else:
                        at.append((w, "?"))
            inst = Instance(law.name, entry.name, entry.file, tuple(at))
            if inst not in seen:
                seen.add(inst)
                found.append(inst)
            break
    return found


# ---------------------------------------------------------------------- reading files

def env_of(path):
    """The environment of a file: check.py's typing of it with its imports, and the core's
    definitions the unfolding may reach."""
    from .check import Program, load_imports, hidden_constructors, typing_of
    from .parse import parse
    path = Path(path)
    program = Program(parse(path.read_text(encoding="utf-8")).program)
    program.imported = load_imports(program, path)
    program.hidden = hidden_constructors(program, program.imported)
    q = typing_of(program)
    return Env(q, core_definitions()), {a.name for a in program if hasattr(a, "name")}


def laws_of(env, own=None):
    """The laws among an environment's own definitions."""
    for act in env.typing.program:
        if is_law(act) and (own is None or act.name in own):
            yield law_of(act, env)


def notices(typing, own):
    """The `check -v` notices: one line per law of the file recognized as a core property."""
    env = Env(typing, core_definitions())
    out = []
    for law in laws_of(env, own):
        for inst in recognize(law):
            out.append((law.name, inst.notice()))
    return out


# ---------------------------------------------------------------------- printing

INFIX = {"==", "/=", "+", "-", "*", "/", "<", "<=", ">", ">=", "and", "or", "mod"}


def _atom(u, names):
    s = show(u, names)
    return s if " " not in s or s.startswith(("(", "{")) else f"({s})"


def show(u, names=None):
    """A term as the surface writes it, near enough for a notice."""
    names = names or {}
    if isinstance(u, AC):
        u = to_kernel(u)
    if isinstance(u, t.Var):
        return names.get(u.name, u.name)
    if isinstance(u, t.Lit):
        v = u.constant.value
        return f'"{v}"' if isinstance(v, str) else repr(v)
    if isinstance(u, t.Proj):
        return f"{_atom(u.record, names)}.{u.label}"
    if isinstance(u, t.App):
        h, args = spine(u)
        if isinstance(h, t.Var) and h.name in INFIX and len(args) == 2:
            return f"{_atom(args[0], names)} {h.name} {_atom(args[1], names)}"
        return " ".join([_atom(h, names)] + [_atom(a, names) for a in args])
    if isinstance(u, t.Lam):
        return f"fn {u.name} {{ {show(u.body, names)} }}"
    if isinstance(u, t.Pi):
        return f"{_atom(u.domain, names)} -> {show(u.codomain, names)}"
    return repr(u)
