"""Python specimen of translation.lth (5d7963b), user prompt 2026-10-13 v1; the core's bite 4,
typing for resolution (record/plan/core-2026-10-17/execution.md §2.2, §2.3 and §6, bite 4;
D-2026-10-18-b, D-2026-10-18-g), 2026-10-18.

Typing is what resolution needs, not a full type checker (4.R9's strict conversion and 4.R11's
refinements stay item 39's later part). `infer` gives the type of every term the library writes or
raises `Untyped` naming the term: names declared in the context, literals, lambdas, applications
(a polymorphic constructor or function instantiated by matching its domain against the argument's
type), projections (through a theory's record and a type's definition), `match` (each pattern
variable typed from the scrutinee's type), blocks, records, tuples and subtypes. Where nothing fixes
a type, as the parameter of a lambda with no expected type or the element of `nil`, the type is a
named unknown, `Hole('?x')`, the principal type's variable; `Hole('type')`, the old "not inferred",
is never a result.

The core encloses every file (12.S22): `core.lut` and the files it imports are read once and seed
every context, their operator bindings elaborating to the kernel's symbol (3.S17: the kernel
computes `+ - * / mod` on constants and the connectives `and`, `or`), as a run has always reduced
them. An operator (2.S9's bindable `+ - * / mod and or`) is resolved by the type of its left operand,
matched under instantiation and through a subtype to its base (4.R13); no binding at that type is an
error, never the bare symbol, and the right operand must fit the binding's domain (4.R9).

Rule 2.2 (D-2026-10-18-b): a structure is a name declared at a record with parameters (`Functor (F :
U -> U) : { map : ... }`); a claim `X : Bool := S T m` binds the model `m` to `S` at `T`, read from
every act the context holds (the claim is the binding, no second act). A field of a structure used
unqualified (`size xs`) is resolved by the type of its discriminating argument, the first whose
type is headed by a parameter of the structure; `S.f` names the structure, `S.f m` the model too. A
parameter whose type is a structure applied to types, omitted at a call, is filled with the model
the type names (D-2026-10-18-g: the structure from the type's model when omitted; another passed by
name; a graded structure's bound is a parameter the demand supplies, never filled here). Failures
are `TypingError`s naming the name, the type found and the candidates.

Numbers default to Int/Float64. Implicits `{A : U}` are inferred from explicit argument types by
matching. Imports retain qualified names but do not load modules. Applied externs remain stuck
kernel terms: no host calls are performed. Fresh names are deterministic.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, fields, is_dataclass, replace
from functools import lru_cache
from pathlib import Path

from . import surface as s, term as t
from .kernel import alpha_equal, pattern_names, substitute


class ElaborationError(ValueError):
    pass


class TypingError(ElaborationError):
    """A term the typing refuses (execution.md 2.2.5): `check` reports it under `rule`, 4.R9 for a
    type that does not fit, 4.R13 for a name no model resolves."""

    def __init__(self, message, rule='4.R9'):
        super().__init__(message)
        self.rule = rule


class Untyped(ElaborationError):
    """`infer` has no type for a term, named in the message: a defect of the typing (bite 4), or a
    name the context does not hold (4.R2's to report)."""


def apps(f, args):
    for a in args:
        f = t.App(f, a)
    return f


def pairs(values, cls=t.Pair):
    if not values:
        raise ElaborationError('empty tuple has no kernel representation')
    result = values[-1]
    for value in reversed(values[:-1]):
        result = cls(value, result)
    return result


def constant(value):
    return {s.IntLit: t.IntConst, s.FloatLit: t.FloatConst,
            s.StringLit: t.StringConst}[type(value)](value.value)


# 2.S9: the symbols an `operator` act binds; the comparisons are the kernel's on every concrete type
BINDABLE = frozenset({'+', '-', '*', '/', 'mod', 'and', 'or'})
# 2.S12: the labels of the binary sum `A + B`, never a structure's field
KERNEL_LABELS = frozenset({'left', 'right'})
# the kernel's own types (11.R1), known without a definition
BASE_TYPES = frozenset({'Int', 'Float64', 'Bool', 'String', 'Nat', 'Unit', 'Real', 'Rational', 'Empty'})
LIB = Path(__file__).parent / 'lib'
PRELUDE = LIB / 'core' / 'core.lut'


@dataclass(frozen=True)
class Binding:
    """An operator bound at a type: `vars` the type parameters the domain may mention (the leading
    `(A : U)` binders of the function), `domain` the type of its first operand, `term` what a use
    elaborates to, `type` the function's type, `name` the function bound."""
    vars: tuple
    domain: t.Term
    term: t.Term
    type: t.Term
    name: str


@dataclass(frozen=True)
class Structure:
    """A name declared at a record with parameters: `params` (name, type) and its `record`."""
    params: tuple
    record: t.Record


@dataclass(frozen=True)
class Claim:
    """`name (binders) : Bool := S args model`: the model of `S` at `args`, `binders` free in both."""
    name: str
    binders: tuple
    args: tuple
    model: t.Term


@dataclass
class Context:
    types: dict = field(default_factory=dict)
    signatures: dict = field(default_factory=dict)
    aliases: dict = field(default_factory=dict)
    operators: dict = field(default_factory=dict)
    constructors: set = field(default_factory=lambda: {'true', 'false', 'nil', 'cons', 'just', 'nothing', 'ok', 'failed'})
    names: dict = field(default_factory=dict)
    used: set = field(default_factory=set)
    refinements: set = field(default_factory=set)  # names that are types by refining one (`is_type`)
    # [kept for the sugar of 2.S17; since bite 4 a projection's type is always read through the
    # record of the theory its model is typed by, binder annotations being erased in the hash]
    models: bool = False
    bindings: dict = field(default_factory=dict)     # operator -> [Binding]
    structures: dict = field(default_factory=dict)   # structure name -> Structure
    claims: dict = field(default_factory=dict)       # structure name -> [Claim]
    datas: dict = field(default_factory=dict)        # constructor -> the parameters of its data
    labels: dict = field(default_factory=dict)       # label of a sum -> [the sums]
    bodies: dict = field(default_factory=dict)       # type name -> (parameters, its definition)
    defined: set = field(default_factory=set)        # names defined or declared at the top level
    predicates: dict = field(default_factory=dict)   # a name declared at a type and defined by a predicate -> the type
    counter: list = field(default_factory=lambda: [0])
    errors: dict = field(default_factory=dict)       # act -> the error reading it

    def child(self):
        c = Context.__new__(Context)
        c.__dict__.update(self.__dict__)
        c.types = self.types.copy(); c.names = self.names.copy()
        return c

    def fork(self):
        """A fresh context for a program, seeded with this one's (the prelude's) knowledge."""
        return Context(types=self.types.copy(), signatures=self.signatures.copy(), aliases=self.aliases.copy(),
                       operators=self.operators.copy(), constructors=set(self.constructors), names={}, used=set(),
                       refinements=set(self.refinements), models=False,
                       bindings={k: list(v) for k, v in self.bindings.items()},
                       structures=self.structures.copy(), claims={k: list(v) for k, v in self.claims.items()},
                       datas=self.datas.copy(), labels={k: list(v) for k, v in self.labels.items()},
                       bodies=self.bodies.copy(), defined=set(self.defined), predicates=self.predicates.copy(),
                       counter=[0], errors={})

    def fresh(self, name):
        candidate = name
        while candidate in self.used:
            candidate += "'"
        self.used.add(candidate)
        return candidate

    def meta(self, name):
        """A named unknown type (`?x3`): what the principal type leaves open."""
        self.counter[0] += 1
        return t.Hole(f'?{name}{self.counter[0]}')


def is_meta(x):
    return isinstance(x, t.Hole) and x.name.startswith('?')


def has_hole(x):
    """Whether a term holds `Hole('type')`, the old "not inferred"."""
    if isinstance(x, t.Hole):
        return x.name == 'type'
    if isinstance(x, tuple):
        return any(has_hole(y) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return any(has_hole(getattr(x, f.name)) for f in fields(x))
    return False


def show(v):
    try:
        return show_term(v)
    except TypeError:
        return repr(v)


# ---------------------------------------------------------------------- types: unfolding, matching

def head_of(ty):
    """The head and the arguments of an application: `List Int` -> (`List`, [Int])."""
    args = []
    while isinstance(ty, t.App):
        args.append(ty.argument); ty = ty.function
    return ty, list(reversed(args))


def unfold(ty, c):
    """A type name's definition under its arguments (`Moderate`, `VecOf n`), a theory's record
    (`Monoid M`), or None. A `data` is nominal and not unfolded."""
    h, args = head_of(ty)
    if not isinstance(h, t.Var):
        return None
    if h.name in ('*', '+') and len(args) == 2 and h.name not in c.types:
        # a product or a sum the elaborator wrote as the symbol applied (`T * Float64` with `T :
        # Concrete`, kept for the hash): read as the type it means
        return t.Sigma('_', args[0], args[1]) if h.name == '*' else t.Sum((('left', args[0]), ('right', args[1])))
    if h.name in c.predicates and not args:
        return c.predicates[h.name]
    if h.name in c.bodies:
        params, body = c.bodies[h.name]
        if len(params) != len(args):
            return None
        for p, a in zip(params, args):
            body = substitute(p, a, body)
        return body
    record = theory_record(ty, c)
    return record


def base(ty, c, fuel=12):
    """Look through definitions and subtypes to the type a value is checked at: `Nat` is `Int`,
    `Moderate` is `Float64`, a refined record its record."""
    while fuel:
        fuel -= 1
        if isinstance(ty, t.Subtype):
            ty = as_type(ty.type); continue
        u = unfold(ty, c)
        if u is None or u == ty:
            return ty
        ty = u
    return ty


def bases(ty, c, fuel=12):
    """`ty` and each type it unfolds to, outermost first."""
    out = [ty]
    while fuel:
        fuel -= 1
        if isinstance(ty, t.Subtype):
            ty = as_type(ty.type)
        else:
            u = unfold(ty, c)
            if u is None or u == ty:
                break
            ty = u
        out.append(ty)
    return out


def sigma_parts(ty, c):
    """The components of a product of several types, `A * B * C` however nested (the parser nests
    a type to the left and a tuple to the right), or None when `ty` is not a product."""
    ty = next((x for x in bases(ty, c) if isinstance(x, t.Sigma)), None)
    if ty is None or ty.name != '_' and ty.name in _free(ty.codomain):
        return None
    return (sigma_parts(ty.domain, c) or [ty.domain]) + (sigma_parts(ty.codomain, c) or [ty.codomain])


def pair_parts(q):
    """The components of a tuple pattern however nested."""
    if isinstance(q, t.PPair):
        return pair_parts(q.left) + pair_parts(q.right)
    return [q]


def widen(ty, c, fuel=12):
    """A subtype's carrier: `Fin n` is `Int`, `FailureFor d` is `Entry`; another type is itself."""
    while fuel:
        fuel -= 1
        if isinstance(ty, t.Subtype):
            ty = as_type(ty.type); continue
        u = unfold(ty, c)
        if isinstance(u, t.Subtype):
            ty = u; continue
        return ty
    return ty


def instantiate(ty, sigma):
    """`ty` with each name or unknown of `sigma` replaced (names capture-avoiding)."""
    for k, v in sigma.items():
        if not k.startswith('?'):
            ty = substitute(k, v, ty)
    metas = {k: v for k, v in sigma.items() if k.startswith('?')}
    return _replace_metas(ty, metas) if metas else ty


def _replace_metas(x, metas):
    if isinstance(x, t.Hole):
        return metas.get(x.name, x)
    if isinstance(x, tuple):
        return tuple(_replace_metas(y, metas) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return replace(x, **{f.name: _replace_metas(getattr(x, f.name), metas) for f in fields(x)})
    return x


def solve(pattern, actual, vars, sigma, c, fuel=8):
    """Extend `sigma` so that `pattern` under it is `actual`; `vars` the names free in `pattern` to
    solve (its unknowns are solved too). First-order: an application by its head and arguments, a
    function type by domain and codomain, a record by its fields; a definition on either side is
    unfolded when the shapes differ. False when they cannot agree."""
    if isinstance(pattern, t.Var) and pattern.name in vars or is_meta(pattern):
        key = pattern.name
        if key in sigma:
            return True if is_meta(sigma[key]) or is_meta(actual) else fits(actual, sigma[key], c) and fits(sigma[key], actual, c)
        if actual != pattern:
            sigma[key] = actual
        return True
    if isinstance(actual, t.Hole):
        return True
    if pattern == actual or alpha_equal(pattern, actual):
        return True
    if type(pattern) is type(actual):
        match pattern, actual:
            case t.App(), t.App():
                if solve(pattern.function, actual.function, vars, sigma, c, fuel) and solve(pattern.argument, actual.argument, vars, sigma, c, fuel):
                    return True
            case t.Sigma(), t.Sigma() if pattern.name == '_' and actual.name == '_':
                pa, pb = sigma_parts(pattern, c), sigma_parts(actual, c)
                if pa is not None and pb is not None and len(pa) == len(pb):
                    return all(solve(x, y, vars, sigma, c, fuel) for x, y in zip(pa, pb))
                return solve(pattern.domain, actual.domain, vars, sigma, c, fuel) and solve(pattern.codomain, actual.codomain, vars, sigma, c, fuel)
            case (t.Pi() | t.Sigma()), _:
                other = actual.codomain if actual.name == pattern.name else substitute(actual.name, t.Var(pattern.name), actual.codomain)
                return solve(pattern.domain, actual.domain, vars, sigma, c, fuel) and solve(pattern.codomain, other, vars, sigma, c, fuel)
            case t.Record(), t.Record():
                if [n for n, _ in pattern.fields] == [n for n, _ in actual.fields]:
                    return all(solve(x, y, vars, sigma, c, fuel) for (_, x), (_, y) in zip(pattern.fields, actual.fields))
            case t.Sum(), t.Sum():
                if [n for n, _ in pattern.alternatives] == [n for n, _ in actual.alternatives]:
                    return all(solve(x, y, vars, sigma, c, fuel) for (_, x), (_, y) in zip(pattern.alternatives, actual.alternatives))
            case t.Subtype(), t.Subtype():
                return solve(pattern.type, actual.type, vars, sigma, c, fuel)
    if fuel:
        u = unfold(actual, c) if not isinstance(actual, t.Subtype) else None
        if u is not None and u != actual:
            return solve(pattern, u, vars, sigma, c, fuel - 1)
        p = unfold(pattern, c)
        if p is not None and p != pattern:
            return solve(p, actual, vars, sigma, c, fuel - 1)
    return False


def fits(actual, expected, c, fuel=16):
    """Whether a value of type `actual` passes where `expected` is asked, as far as typing for
    resolution knows (4.R9): an unknown passes; types are compared through their definitions and
    subtypes to their bases (a value crossing into a subtype is checked where it crosses, 4.R5, or
    owes its predicate, 4.R11); `Float64` and `Rational` refine `Real` (11.R1); a `Bool` verdict is a
    `Law` (5.S6); functions are contravariant in the domain and covariant in the codomain."""
    if isinstance(actual, t.Hole) or isinstance(expected, t.Hole) or not fuel:
        return True
    if actual == expected or alpha_equal(actual, expected):
        return True
    a, b = base(actual, c), base(expected, c)
    if isinstance(a, t.Hole) or isinstance(b, t.Hole) or a == b or alpha_equal(a, b):
        return True
    if isinstance(b, t.Var) and (b.name == 'Real' and isinstance(a, t.Var) and a.name in ('Float64', 'Rational')
                                 or b.name == 'Law' and a == t.Var('Bool')):
        return True
    if is_two_units(a) and b == t.Var('Bool') or is_two_units(b) and a == t.Var('Bool'):
        return True
    match a, b:
        case t.Pi(), t.Pi():
            return fits(b.domain, a.domain, c, fuel - 1) and fits(a.codomain, substitute(b.name, t.Var(a.name), b.codomain) if a.name != b.name else b.codomain, c, fuel - 1)
        case t.Sigma(), t.Sigma():
            pa, pb = sigma_parts(a, c), sigma_parts(b, c)
            if pa is not None and pb is not None and len(pa) == len(pb):
                return all(fits(x, y, c, fuel - 1) for x, y in zip(pa, pb))
            if a.name == '_' and b.name != '_' and b.name in _free(b.codomain):
                # a pair's type does not say on which first component the second depends
                return fits(a.domain, b.domain, c, fuel - 1)
            return fits(a.domain, b.domain, c, fuel - 1) and fits(a.codomain, substitute(b.name, t.Var(a.name), b.codomain) if a.name != b.name else b.codomain, c, fuel - 1)
        case t.Record(), t.Record():
            return ([n for n, _ in a.fields] == [n for n, _ in b.fields]
                    and all(fits(x, y, c, fuel - 1) for (_, x), (_, y) in zip(a.fields, b.fields)))
        case (t.Record(), t.Sigma()) | (t.Sigma(), t.Record()):
            # a record is a named product (D-2026-10-13-x): its fields are a tuple's components
            pa = [x for _, x in a.fields] if isinstance(a, t.Record) else sigma_parts(a, c) or [a.domain, a.codomain]
            pb = [x for _, x in b.fields] if isinstance(b, t.Record) else sigma_parts(b, c) or [b.domain, b.codomain]
            return len(pa) == len(pb) and all(fits(x, y, c, fuel - 1) for x, y in zip(pa, pb))
        case t.Sum(), t.Sum():
            # 3.R2: a sum is identified by its shape, its labels are binders
            return (len(a.alternatives) == len(b.alternatives)
                    and all(fits(x, y, c, fuel - 1) for (_, x), (_, y) in zip(a.alternatives, b.alternatives)))
        case t.App(), t.App():
            ha, xs = head_of(a); hb, ys = head_of(b)
            return (len(xs) == len(ys) and fits(ha, hb, c, fuel - 1)
                    and all(fits(x, y, c, fuel - 1) for x, y in zip(xs, ys)))
        case t.Universe(), t.Universe():
            return True
    # a theory's record (`Monoid M`) and a record type of the same fields
    return False


def refines(actual, expected, c, fuel=16):
    """Whether `actual` refines `expected` (4.R9, 11.R1), in the one direction: a subtype refines
    its base and a definition is its body, never the other way; `Float64` and `Rational` refine
    `Real`, a `Bool` verdict is a `Law` (5.S6); functions contravariant in the domain, covariant in
    the codomain; products, records, sums and applied types covariant in their parts; a value index
    of a type family (`Fin n` against `Fin m`) is not decided here; an unknown agrees."""
    if isinstance(actual, t.Hole) or isinstance(expected, t.Hole) or not fuel:
        return True
    if actual == expected or alpha_equal(actual, expected):
        return True
    if isinstance(expected, t.Var) and isinstance(actual, t.Var) and (
            expected.name == 'Real' and actual.name in ('Float64', 'Rational')
            or expected.name == 'Law' and actual.name == 'Bool'):
        return True
    if is_two_units(actual) and expected == t.Var('Bool') or is_two_units(expected) and actual == t.Var('Bool'):
        return True
    match actual, expected:
        case t.Pi(), t.Pi():
            return refines(expected.domain, actual.domain, c, fuel - 1) and refines(
                actual.codomain, substitute(expected.name, t.Var(actual.name), expected.codomain) if actual.name != expected.name else expected.codomain, c, fuel - 1)
        case t.Sigma(), t.Sigma():
            pa, pb = sigma_parts(actual, c), sigma_parts(expected, c)
            if pa is not None and pb is not None and len(pa) == len(pb):
                return all(refines(x, y, c, fuel - 1) for x, y in zip(pa, pb))
            return refines(actual.domain, expected.domain, c, fuel - 1) and (
                expected.name != '_' and actual.name == '_' or refines(actual.codomain, expected.codomain, c, fuel - 1))
        case t.Record(), t.Record():
            return ([n for n, _ in actual.fields] == [n for n, _ in expected.fields]
                    and all(refines(x, y, c, fuel - 1) for (_, x), (_, y) in zip(actual.fields, expected.fields)))
        case (t.Record(), t.Sigma()) | (t.Sigma(), t.Record()):
            # a record is a named product (D-2026-10-13-x): its fields are a tuple's components
            pa = [x for _, x in actual.fields] if isinstance(actual, t.Record) else sigma_parts(actual, c) or [actual.domain, actual.codomain]
            pb = [x for _, x in expected.fields] if isinstance(expected, t.Record) else sigma_parts(expected, c) or [expected.domain, expected.codomain]
            return len(pa) == len(pb) and all(refines(x, y, c, fuel - 1) for x, y in zip(pa, pb))
        case t.Sum(), t.Sum():
            # 3.R2: a sum is identified by its shape, its labels are binders
            return (len(actual.alternatives) == len(expected.alternatives)
                    and all(refines(x, y, c, fuel - 1) for (_, x), (_, y) in zip(actual.alternatives, expected.alternatives)))
        case t.App(), t.App():
            ha, xs = head_of(actual); hb, ys = head_of(expected)
            if len(xs) == len(ys) and alpha_equal(ha, hb):
                return all(refines(x, y, c, fuel - 1) or not _is_type_term(x, c) for x, y in zip(xs, ys))
    # one step of the actual's definition or subtype toward its base
    u = as_type(actual.type) if isinstance(actual, t.Subtype) else unfold(actual, c)
    if u is not None and u != actual:
        return refines(u, expected, c, fuel - 1)
    # a definition expected is its body (an alias-like name), not a narrowing of it
    if not isinstance(expected, t.Subtype):
        u = unfold(expected, c)
        if u is not None and u != expected and not isinstance(u, t.Subtype):
            return refines(actual, u, c, fuel - 1)
    return False


def is_two_units(x):
    """A sum of two units, which is `Bool` (3.R2)."""
    return isinstance(x, t.Sum) and len(x.alternatives) == 2 and all(y == t.Var('Unit') for _, y in x.alternatives)


def _is_type_term(x, c):
    try:
        return is_type(x, infer(x, c), c)
    except ElaborationError:
        return False


# ---------------------------------------------------------------------- infer

def infer(v, c):
    """The type of the elaborated term `v` in `c`; `Untyped` names a term it cannot type."""
    match v:
        case t.Var(n):
            return var_type(n, c)
        case t.Lit(k):
            return t.Var({t.IntConst: 'Int', t.FloatConst: 'Float64', t.StringConst: 'String'}[type(k)])
        case t.Universe() | t.World() | t.Pi() | t.Sigma() | t.Sum() | t.Record() | t.Data() | t.Subtype() | t.Hole():
            return t.Universe()
        case t.Lam(n, a, b):
            inner = c.child(); inner.types[n] = a
            return t.Pi(n, a, infer(b, inner))
        case t.App(f, a):
            return app_type(v, f, a, c)
        case t.RecordValue(fs):
            return t.Record(tuple((n, infer(x, c)) for n, x in fs))
        case t.Proj(r, n):
            return proj_type(r, n, c)
        case t.Let(n, a, x, b):
            inner = c.child()
            inner.types[n] = a if not isinstance(a, t.Hole) or is_meta(a) else _lenient(x, c)
            return infer(b, inner)
        case t.Match(x, arms):
            return match_type(x, arms, c)
        case t.Pair(a, b):
            return t.Sigma('_', infer(a, c), infer(b, c))
        case t.Inj(label, x):
            return label_sum(label, c)
        case t.Extern() | t.Primitive() | t.Axiom():
            # what the host or the kernel gives: its declaration's type, read where it is declared
            return c.meta('declared')
    raise Untyped(f'no type for {show(v)}')


def _lenient(v, c):
    try:
        return infer(v, c)
    except Untyped:
        return c.meta('t')


def var_type(n, c):
    if n in c.types:
        ty = c.types[n]
        if n in c.datas and c.datas[n]:
            # a constructor of a data with parameters: each parameter an unknown, solved by its use
            ty = instantiate(ty, {p: c.meta(p) for p in c.datas[n]})
        return theory_domains(ty, c)
    if n in {'List', 'Maybe', 'Failures'}:
        return t.Pi('_', t.Universe(), t.Universe())
    if n in BASE_TYPES:
        return t.Universe()
    if n in c.labels or n in KERNEL_LABELS:
        return label_type(n, c)
    raise Untyped(f'no type for {n}: not a name the context declares')


def label_sum(label, c):
    """The sum a label belongs to when one sum has it, else an unknown."""
    distinct = []
    for x in c.labels.get(label, ()):
        if not any(alpha_equal(x, y) for y in distinct):
            distinct.append(x)
    return distinct[0] if len(distinct) == 1 else c.meta('sum')


def label_type(label, c):
    """A label of a `||` sum (2.S12) written bare: the value of its sum when its payload is
    `Unit` (`NoArm`), else the function into its sum."""
    sm = label_sum(label, c)
    if isinstance(sm, t.Sum):
        payload = dict(sm.alternatives)[label]
        return sm if payload == t.Var('Unit') else t.Pi('_', payload, sm)
    return c.meta('sum')


# the kernel's symbols, read by their head when no definition names them
COMPARISONS = frozenset({'==', '/=', '<', '<=', '>', '>=', 'and', 'or', 'implies', 'holds', 'not'})
ARITHMETIC = frozenset({'+', '-', '*', '/', 'mod'})


def app_type(v, f, a, c):
    if isinstance(f, t.App) and f.function == t.Var('&'):
        return conjunction_type(f.argument, a, c)
    head, args = head_of(v)
    if isinstance(head, t.Var) and head.name not in c.types:
        if (head.name in c.labels or head.name in KERNEL_LABELS) and len(args) == 1:
            return label_sum(head.name, c)
        if head.name in COMPARISONS:
            return t.Var('Bool')
        if head.name in ARITHMETIC and args:
            return infer(args[0], c)
        if head.name in ('primitive', 'extern', 'axiom'):
            return c.meta('declared')
        if head.name == 'quote':
            return t.Var('Term') if 'Term' in c.types else c.meta('quoted')
    ty = infer(f, c)
    fuel = 12
    while not isinstance(ty, t.Pi) and fuel:
        fuel -= 1
        if isinstance(ty, t.Hole):
            return c.meta('r')
        if isinstance(ty, t.Record) and theory_applied(f, c):
            # a theory applied to its parameters and a model is its laws' verdict (4.R6, 5.S6)
            return t.Var('Bool')
        u = as_type(ty.type) if isinstance(ty, t.Subtype) else unfold(ty, c)
        if u is None or u == ty:
            break
        ty = u
    if not isinstance(ty, t.Pi):
        if isinstance(ty, t.Record) and theory_applied(f, c):
            return t.Var('Bool')
        raise Untyped(f'no type for {show(v)}: {show(f)} has type {show(ty)}, not a function')
    if ty.name == '_' or ty.name not in _free(ty.codomain):
        sigma = {}
        domain_metas = _metas(ty.domain)
        if domain_metas:
            try:
                at = infer(a, c)
            except Untyped:
                at = None
            if at is not None:
                # a parameter is instantiated at the carrier of a subtype (`cons f es` with `f :
                # FailureFor d` and `es : List Entry` is a `List Entry`)
                solve(ty.domain, widen(at, c), frozenset(), sigma, c)
        return instantiate(ty.codomain, sigma) if sigma else ty.codomain
    return substitute(ty.name, a, ty.codomain)


def _free(x):
    from .kernel import free_names
    return free_names(x)


def _metas(x):
    out = set()
    def go(y):
        if isinstance(y, t.Hole):
            if y.name.startswith('?'): out.add(y.name)
        elif isinstance(y, tuple):
            for z in y: go(z)
        elif is_dataclass(y) and not isinstance(y, type):
            for f in fields(y): go(getattr(y, f.name))
    go(x)
    return out


def theory_applied(f, c):
    """Whether `f` is a theory (a name declared at a record) applied to its parameters."""
    h, args = head_of(f)
    if not isinstance(h, t.Var):
        return False
    declared = c.types.get(h.name)
    n = 0
    while isinstance(declared, t.Pi):
        declared = declared.codomain; n += 1
    return isinstance(declared, t.Record) and n == len(args)


def conjunction_type(left_term, right_term, c):
    left = infer(left_term, c)
    right = infer(right_term, c)
    if (isinstance(left, t.Subtype) and isinstance(right, t.Subtype)
            and alpha_equal(left.type, right.type)):
        law = substitute(right.name, t.Var(left.name), right.predicate)
        return t.Subtype(left.name, left.type, apps(t.Var('&'), [left.predicate, law]))
    # Laws may quantify different arguments after their model.
    # Their conjunction is still a predicate over that model.
    # [proposed] translation.lth states no type for `&`; by spec 5.S6 (a
    # combination of Boolean laws and laws.lth's `Law` lifts each Boolean part)
    # a conjunction with a `Law` part is a `Law` over the model, and a
    # conjunction of Boolean laws stays Boolean.
    if isinstance(left, t.Pi) and isinstance(right, t.Pi):
        values = {law_value(left), law_value(right)}
        if (values <= {t.Var('Bool'), t.Var('Law')}
                and alpha_equal(left.domain, right.domain)):
            value = t.Var('Law') if t.Var('Law') in values else t.Var('Bool')
            return theory_domains(t.Pi(left.name, left.domain, value), c)
    if left == right:
        return left
    # [proposed, bite 4] laws over different models or quantified apart (core.lut's `CoreData`):
    # the conjunction of their verdicts, each conjunct quantified on its own (D-2026-10-18-f)
    values = {law_value(left), law_value(right)}
    if values <= {t.Var('Bool'), t.Var('Law')}:
        return t.Var('Law') if t.Var('Law') in values else t.Var('Bool')
    raise Untyped(f'no type for the conjunction of {show(left_term)} : {show(left)} and {show(right_term)} : {show(right)}')


def record_of(ty, c):
    """The record a value of type `ty` has fields of, through definitions and theories, or None."""
    for x in bases(ty, c):
        if isinstance(x, t.Record):
            return x
        if isinstance(x, t.Sigma) and False:
            return None
    return None


def proj_type(r, n, c):
    ty = infer(r, c)
    if isinstance(ty, t.Hole):
        return c.meta(n)
    record = record_of(ty, c)
    if record is None:
        raise Untyped(f'no type for {show(r)}.{n}: {show(r)} has type {show(ty)}, not a record')
    names = [m for m, _ in record.fields]
    if n not in names:
        raise TypingError(f'{show(r)}.{n}: {show(r)} has type {show(ty)}, whose fields are {", ".join(names)}; it has no field {n}')
    # a later field's type may name an earlier one (a dependent record): that one of this value
    result = dict(record.fields)[n]
    for m in names[:names.index(n)]:
        result = substitute(m, t.Proj(r, m), result)
    return result


def bind_pattern(q, ty, c):
    """Give the variables of the pattern `q` their types, read from the scrutinee's type `ty`."""
    match q:
        case t.PVar(n):
            c.types[n] = ty
        case t.PWild() | t.PLit():
            return
        case t.PPair(a, b):
            sg = next((x for x in bases(ty, c) if isinstance(x, t.Sigma)), None)
            parts, qs = sigma_parts(ty, c), pair_parts(q)
            if parts is not None and len(parts) == len(qs) and len(qs) > 2:
                for p, x in zip(qs, parts):
                    bind_pattern(p, x, c)
            elif sg is None:
                bind_pattern(a, c.meta('a'), c); bind_pattern(b, c.meta('b'), c)
            else:
                bind_pattern(a, sg.domain, c)
                bind_pattern(b, sg.codomain if sg.name == '_' else c.meta('b'), c)
        case t.PInj(label, p):
            sm = next((x for x in bases(ty, c) if isinstance(x, t.Sum)), None)
            bind_pattern(p, dict(sm.alternatives).get(label, c.meta(label)) if sm else c.meta(label), c)
        case t.PCon(name, ps):
            sm = next((x for x in bases(ty, c) if isinstance(x, t.Sum)), None)
            if sm is not None and name in dict(sm.alternatives):
                payload = dict(sm.alternatives)[name]
                if len(ps) == 1:
                    bind_pattern(ps[0], payload, c)
                else:
                    for p in ps: bind_pattern(p, c.meta(name), c)
                return
            ctype = c.types.get(name)
            if ctype is None:
                for p in ps: bind_pattern(p, c.meta(name), c)
                return
            if not ps and isinstance(ctype, t.Pi):
                # a constructor with arguments written bare is the variable the author meant (a
                # name another file's data takes, `name` of grammar.lth in `schema name ->`); the
                # term keeps the constructor, as the elaborator has always written it
                c.types[name] = c.meta(name)
                return
            if name in c.datas and c.datas[name]:
                ctype = instantiate(ctype, {p: c.meta(p) for p in c.datas[name]})
            domains = []
            for _ in ps:
                if not isinstance(ctype, t.Pi):
                    domains.append(c.meta(name)); continue
                domains.append(ctype.domain); ctype = ctype.codomain
            sigma = {}
            solve(ctype, ty, frozenset(), sigma, c)
            for p, d in zip(ps, domains):
                bind_pattern(p, instantiate(d, sigma) if sigma else d, c)


def match_type(x, arms, c):
    if not arms:
        return c.meta('absurd')
    try:
        ty = infer(x, c)
    except Untyped:
        ty = c.meta('m')
    found = []
    for q, b in arms:
        inner = c.child()
        bind_pattern(q, ty, inner)
        found.append(infer(b, inner))
    return next((y for y in found if not _metas(y)), found[0])


def theory_record(ty, c):
    """The record of a theory applied to its arguments, else None: `Host State`, with `Host (S :
    Concrete) : { ..., print : W -> String -> W * Unit }` declared, is that record with `S` as
    `State`. A model typed by an imported theory (`host : HostConsole`, `HostConsole = Host State`)
    has its fields' types read from it, so the sugar of 2.S17 sees `host.print w "x"` as an action
    (record/IA/v04-2026-10-15/prompt-sugar.md)."""
    head = ty
    args = []
    while isinstance(head, t.App):
        args.append(head.argument); head = head.function
    if not isinstance(head, t.Var):
        return None
    declared = c.types.get(head.name)
    for arg in reversed(args):
        declared = substitute(declared.name, arg, declared.codomain) if isinstance(declared, t.Pi) else None
    return declared if isinstance(declared, t.Record) else None


def theory_domains(ty, c):
    """Keep a law's model domain tied to the declared theory record."""
    if isinstance(ty, t.Pi):
        return t.Pi(ty.name, theory_record(ty.domain, c) or ty.domain, theory_domains(ty.codomain, c))
    return ty


def law_value(ty):
    """What a law's type gives once all its arguments are applied: `Bool`, `Law`, or another."""
    while isinstance(ty, t.Pi):
        ty = ty.codomain
    return ty


def is_type(v, ty, c):
    """Whether the term `v`, of inferred type `ty`, is a type: its type is `U` (or a subtype of `U`,
    as `Concrete`), or it is a name that refines a type (`refining`)."""
    return (isinstance(ty, t.Universe) or isinstance(v, t.Var) and v.name in c.refinements
            or ty is not None and not isinstance(ty, t.Hole) and isinstance(base(ty, c), t.Universe))


def refining(act, c):
    """Whether a definition makes its name a type by refining the type it is declared at.

    [proposed] spec 11.R1: `Float64 : Real := primitive "ieee754-binary64"` is a type, the finite
    doubles, refining `Real`, though its declared type is `Real` and not `U`. A name declared at
    a type that is not a function type (`Real : U`) and given a `primitive` body is read as such a
    type. Declaration at a type alone does not make one (`x : Real` is a number), and 11.R2 keeps
    `primitive` to core.lut, whose primitives at a type other than a function type are all types
    (`Float64`, `Rational`). A subtype by a predicate body (4.S7) is not read here.
    """
    if not (isinstance(act, s.Define) and act.type is not None and not act.binders
            and isinstance(act.body, s.TermBody)):
        return False
    head = act.body.term
    while isinstance(head, s.App):
        head = head.function
    if head != s.Name('primitive'):
        return False
    ty = c.types.get(act.name)
    try:
        return ty is not None and not isinstance(ty, t.Pi) and isinstance(infer(ty, c), t.Universe)
    except Untyped:
        return False


def as_type(u):
    """A term in type position: `implies A B` there is the arrow `A -> B`.

    `walk` reads `A -> B` as the Bool implication when it cannot infer that `A` is a type, as for a
    name brought in by an import (`context_of` does not load imports). An implication is never a
    type, so where a type is expected it can only be the arrow (check.py's `arrows`, its bite 3b
    part 1, moved here). Predicates of subtypes are not entered: there `implies` is the
    implication.
    """
    match u:
        case t.App(t.App(t.Var('implies'), a), b): return t.Pi('_', as_type(a), as_type(b))
        case t.Pi(n, a, b): return t.Pi(n, as_type(a), as_type(b))
        case t.Sigma(n, a, b): return t.Sigma(n, as_type(a), as_type(b))
        case t.Record(fs): return t.Record(tuple((n, as_type(x)) for n, x in fs))
        case t.Sum(xs): return t.Sum(tuple((n, as_type(x)) for n, x in xs))
        case t.Subtype(n, a, p): return t.Subtype(n, as_type(a), p)
        case t.App(f, a): return t.App(as_type(f), as_type(a))
    return u


def walk_type(v, c):
    """Elaborate `v` where a type is expected (an annotation, a binder's type, a field's)."""
    return as_type(walk(v, c))


def pattern(p, c, fresh=False):
    """A surface pattern as in a `match` arm; `fresh` renames its variables, as a block item does."""
    match p:
        case s.PWild(): return t.PWild()
        case s.PLit(k): return t.PLit(constant(k))
        case s.PTuple(ps): return pairs([pattern(x, c, fresh) for x in ps], t.PPair)
        case s.PApp(n, ps):
            if ps or n in c.constructors:
                return t.PCon(n, tuple(pattern(x, c, fresh) for x in ps))
            m = c.fresh(n) if fresh else n
            c.names[n] = m
            return t.PVar(m)
    raise ElaborationError(f'unsupported pattern {p!r}')


def bare_name(p, c):
    """The name of a pattern that is a bare variable, else None."""
    if isinstance(p, s.PApp) and not p.patterns and p.name not in c.constructors:
        return p.name
    return None


def pattern_types(q, ty, c):
    """Give the variables of `q` the components of `ty` where its shape follows the pattern."""
    bind_pattern(q, ty, c)


def is_action(ty):
    """An action's result: `W * A` for the world `W` (D8, D-2026-10-13-ag)."""
    return isinstance(ty, t.Sigma) and isinstance(ty.domain, t.World)


def block(items, body, c, expected):
    """translation.lth (87d6091) law `Blocks`: each item in order, the rest of the block under it.

    `x := t` and a bare name on a value that is not an action are a `Let` on a fresh name (4.R12);
    a pattern on `<-` is a `match` with one arm (on an action's `W * A`), a bare name on `W * Unit` binding
    the token and dropping the unit (D-2026-10-13-ag). A pattern that is not a bare name is that
    one-arm `match` whatever the value's type (1665b9d, 2.S17); only a bare name on a non-action
    stays a `Let`.
    """
    if not items:
        return walk(body, c, expected)
    item, rest = items[0], items[1:]
    name = item.name if isinstance(item, s.Bind) else bare_name(item.pattern, c)
    if name is not None:
        # a rebinding takes the type of the binding before it as the expected one
        bound = name in c.names or name in c.types
        previous = walk(s.Name(name), c) if bound else None
        value = walk(item.value, c, _lenient(previous, c) if bound else None)
    else:
        value = walk(item.value, c)
    ty = _lenient(value, c)
    if isinstance(item, s.Rebind) and (is_action(ty) or name is None):
        inner = c.child()
        if name is not None and ty.codomain == t.Var('Unit'):
            n = inner.fresh(name); inner.names[name] = n
            q = t.PPair(t.PVar(n), t.PWild())
        else:
            q = pattern(item.pattern, inner, fresh=True)
        pattern_types(q, ty, inner)
        return t.Match(value, ((q, block(rest, body, inner, expected)),))
    inner = c.child()
    n = inner.fresh(name); inner.names[name] = n; inner.types[n] = ty
    return t.Let(n, ty, value, block(rest, body, inner, expected))


def parameters(binders, c):
    result = []
    for b in binders:
        a = walk_type(b.type, c)
        for n in b.names:
            result.append((n, a)); c.types[n] = a; c.names[n] = n
    return result


def curry(cls, params, body):
    for n, a in reversed(params):
        body = cls(n, a, body)
    return body


# ---------------------------------------------------------------------- structures (rule 2.2)

def is_kind(ty):
    """`U`, `U -> U`, ...: the type of a type parameter."""
    while isinstance(ty, t.Pi):
        if not is_kind(ty.domain):
            return False
        ty = ty.codomain
    return isinstance(ty, t.Universe)


def structure_of(ty, c):
    """The structure a type names when it is one applied to its parameters (`Object A`), else None."""
    h, args = head_of(ty)
    if isinstance(h, t.Var) and h.name in c.structures and len(args) == len(c.structures[h.name].params):
        return h.name
    return None


def is_field_name(n, c):
    """A name used free that is a field of a structure: not local, not defined, not a constructor
    nor a label (rule 2.2.1)."""
    return (n not in c.names and n not in c.aliases and n not in c.defined and n not in c.types
            and n not in c.constructors and n not in c.labels and n not in KERNEL_LABELS
            and any(n in dict(st.record.fields) for st in c.structures.values()))


def qualified(head, c):
    """(S, f) when `head` is `S.f` (a dotted name or a projection of a name) with `S` a structure
    and not a local name (rule 2.2.3), else None."""
    if isinstance(head, s.Name) and '.' in head.name and head.name not in c.names and head.name not in c.types:
        root, _, rest = head.name.partition('.')
        if root in c.structures and root not in c.names and '.' not in rest:
            return root, rest
    if isinstance(head, s.Proj) and isinstance(head.value, s.Name):
        root = head.value.name
        if root in c.structures and root not in c.names:
            return root, head.field
    return None


def field_shape(st, fname):
    """A field's type split: the leading type binders (`(A B : U)`), the value binders (name,
    domain) and the result; with the index of the discriminating binder, the first whose domain is
    headed by a parameter of the structure (rule 2.2.1), or None."""
    ftype = dict(st.record.fields)[fname]
    tvars = []
    while isinstance(ftype, t.Pi) and is_kind(ftype.domain) and ftype.name != '_':
        tvars.append(ftype.name); ftype = ftype.codomain
    values = []
    while isinstance(ftype, t.Pi):
        values.append((ftype.name, ftype.domain)); ftype = ftype.codomain
    params = {p for p, _ in st.params}
    j = None
    for k, (_, d) in enumerate(values):
        h, _ = head_of(d)
        if isinstance(h, t.Var) and h.name in params:
            j = k; break
    return tvars, values, ftype, j


def claim_matches(S, pattern_of, dty, extra_vars, c):
    """The claims of `S` whose instance of `pattern_of(claim)` matches the type `dty` (or one of its
    bases): [(claim, sigma)]."""
    found = []
    for claim in c.claims.get(S, ()):
        pattern = pattern_of(claim)
        for candidate in bases(dty, c):
            sigma = {}
            if solve(pattern, candidate, frozenset(claim.binders) | frozenset(extra_vars), sigma, c):
                found.append((claim, sigma)); break
    return found


def model_of(claim, sigma, c, where):
    """The claim's model at the solution `sigma` of its binders."""
    model = claim.model
    for b in claim.binders:
        if b in sigma:
            model = substitute(b, sigma[b], model)
        elif b in _free(model):
            raise TypingError(f'{where}: the model {claim.name} gives depends on {b}, which the type does not fix', '4.R13')
    return model


def structure_param_pattern(S, claim, d, c):
    """A field's domain `d` with the structure's parameters replaced by the claim's arguments."""
    for (p, _), a in zip(c.structures[S].params, claim.args):
        d = substitute(p, a, d)
    return d


def resolve_field(fname, structure, arguments, c, expected=None):
    """A field of a structure applied to `arguments` (surface), resolved by the type of its
    discriminating argument (rule 2.2.1), or of the structure `structure` when qualified (2.2.3)."""
    where = f'{structure}.{fname}' if structure else fname
    named = [a for a in arguments if isinstance(a, s.NamedArg)]
    if named:
        raise TypingError(f'{where}: a field of a structure takes no named argument ({named[0].name})', '4.R13')
    candidates = [S for S, st in c.structures.items()
                  if (structure is None or S == structure) and fname in dict(st.record.fields)]
    if not candidates:
        raise TypingError(f'{where}: {structure} has no field {fname}', '4.R13')
    walked = {}

    def walked_at(k):
        if k not in walked:
            walked[k] = walk(arguments[k], c)
        return walked[k]

    matches = []
    unresolved = []
    found_type = None
    for S in candidates:
        st = c.structures[S]
        tvars, values, result, j = field_shape(st, fname)
        if j is None:
            unresolved.append(f'{S} (no argument of {fname} has a type of its parameters)'); continue
        ntypes = len(tvars) if tvars and arguments and _is_type_argument(arguments[0], c) else 0
        k = ntypes + j
        if k < len(arguments):
            dty = _lenient(walked_at(k), c)
        elif isinstance(expected, t.Pi):
            e = expected
            for _ in range(k - len(arguments)):
                e = e.codomain if isinstance(e, t.Pi) else None
            dty = e.domain if isinstance(e, t.Pi) else c.meta('d')
        else:
            raise TypingError(f'{where}: resolved by the type of its argument {k + 1}, which is not given; '
                              f'apply it, or write {S}.{fname} with its model', '4.R13')
        if isinstance(dty, t.Hole):
            raise TypingError(f'{where}: resolved by the type of its argument {k + 1}, which is not known; '
                              f'annotate it, or write {S}.{fname} with its model', '4.R13')
        found_type = dty
        pattern_of = lambda claim, d=values[j][1], S=S: structure_param_pattern(S, claim, d, c)
        for claim, sigma in claim_matches(S, pattern_of, dty, tvars, c):
            matches.append((S, claim, sigma, tvars, values, ntypes, j))
    if not matches:
        claimed = '; '.join(f'{S} at ' + ', '.join(show(a) for a in claim.args) + f' ({claim.name})'
                            for S in candidates for claim in c.claims.get(S, ())) or 'none'
        raise TypingError(f'{where}: no model of {" or ".join(candidates)} at {show(found_type) if found_type is not None else "the type of its argument"}'
                          f'{"; " + "; ".join(unresolved) if unresolved else ""}; the models claimed: {claimed}', '4.R13')
    structures = list(dict.fromkeys(m[0] for m in matches))
    if len(structures) > 1:
        raise TypingError(f'{where}: a field of {" and ".join(structures)}, each with a model at {show(found_type)}; '
                          f'write ' + ' or '.join(f'{S}.{fname}' for S in structures), '4.R13')
    if len(matches) > 1:
        raise TypingError(f'{where}: two models of {structures[0]} at {show(found_type)} ('
                          + ', '.join(m[1].name for m in matches) + '); a type with two models is two types (4.R13)', '4.R13')
    S, claim, sigma, tvars, values, ntypes, j = matches[0]
    model = model_of(claim, sigma, c, where)
    term = t.Proj(model, fname)
    st = c.structures[S]
    # the field's binders at this model: the parameters the claim's arguments, a sibling field its
    # projection from the model (a dependent record), the type binders solved
    names = [m for m, _ in st.record.fields]

    def at_model(d):
        d = structure_param_pattern(S, claim, d, c)
        for m in names:
            d = substitute(m, t.Proj(model, m), d)
        return instantiate(d, {k: v for k, v in sigma.items() if k in tvars}) if sigma else d

    type_args = [walk_type(arguments[i], c) for i in range(ntypes)]
    if ntypes:
        sigma.update(zip(tvars, type_args))
    args = []
    order = [j] + [k for k in range(len(values)) if k != j]
    given = {}
    for k in order:
        i = ntypes + k
        if i >= len(arguments):
            continue
        d = at_model(values[k][1])
        for (n, _), v in zip(values, [given.get(x) for x in range(len(values))]):
            if v is not None and n != '_':
                d = substitute(n, v, d)
        unknown = {tv: c.meta(tv) for tv in tvars if tv not in sigma}
        d = instantiate(d, unknown) if unknown else d
        value = walked[i] if k == j and i in walked else walk(arguments[i], c, d)
        given[k] = value
        if any(tv not in sigma for tv in tvars):
            local = {}
            if solve(d, _lenient(value, c), frozenset(), local, c):
                for tv, m in unknown.items():
                    if m.name in local:
                        sigma[tv] = local[m.name]
    missing = [tv for tv in tvars if tv not in sigma]
    if missing and any(ntypes + k < len(arguments) for k in range(len(values))):
        raise TypingError(f'{where}: its type argument {", ".join(missing)} is not fixed by its arguments; write it', '4.R13')
    if not missing:
        term = apps(term, [sigma[tv] for tv in tvars])
    elif tvars:
        raise TypingError(f'{where}: its type argument {", ".join(missing)} is not fixed; apply it to its arguments', '4.R13')
    for k in range(len(values)):
        if k in given:
            term = t.App(term, given[k])
        else:
            break
    rest = arguments[ntypes + len(given):] if len(given) == len(values) else ()
    for arg in rest:
        term = t.App(term, walk(arg, c))
    return term


def _is_type_argument(arg, c):
    """Whether a surface argument is a type (the field's type arguments written, `map Int Bool f
    xs`); a lambda, a literal, a list, a tuple, a record or a block never is."""
    if isinstance(arg, (s.Lambda, s.Literal, s.List, s.Tuple, s.RecordValue, s.Block, s.MatchOf, s.IfThen)):
        return False
    try:
        value = walk(arg, c.child())
        return is_type(value, infer(value, c), c)
    except ElaborationError:
        return False


def qualified_application(S, fname, arguments, c, expected=None):
    """`S.f m args` with a model `m` (its type `S T` or a record with the field) projects it; `S.f
    args` resolves the field in `S` alone (rule 2.2.3)."""
    if fname not in dict(c.structures[S].record.fields):
        raise TypingError(f'{S}.{fname}: {S} has no field {fname}', '4.R13')
    if arguments and not isinstance(arguments[0], s.NamedArg):
        first = walk(arguments[0], c)
        ty = _lenient(first, c)
        if structure_of(ty, c) == S or isinstance(record_of(ty, c), t.Record) and fname in dict(record_of(ty, c).fields) and not is_type(first, ty, c):
            result = t.Proj(first, fname)
            for arg in arguments[1:]:
                result = t.App(result, walk(arg, c))
            return result
    return resolve_field(fname, S, arguments, c, expected)


def fill_structure(slot_type, c, where):
    """The model the types of a structure's parameters name (rule 2.2.2, D-2026-10-18-g)."""
    S = structure_of(slot_type, c)
    _, args = head_of(slot_type)
    found = []
    for claim in c.claims.get(S, ()):
        sigma = {}
        if all(solve(p, a, frozenset(claim.binders), sigma, c) for p, a in zip(claim.args, args)):
            found.append((claim, sigma))
    if not found:
        claimed = ', '.join(f'{S} ' + ' '.join(show(a) for a in cl.args) + f' ({cl.name})' for cl in c.claims.get(S, ())) or 'none'
        raise TypingError(f'{where}: {show(slot_type)} is not given and no claim names it; the models claimed: {claimed}', '4.R13')
    if len(found) > 1:
        raise TypingError(f'{where}: two models of {show(slot_type)} ({", ".join(cl.name for cl, _ in found)}); pass one by name', '4.R13')
    return model_of(found[0][0], found[0][1], c, where)


def is_model_type(ty, S, c):
    """Whether a value of type `ty` can be a model of the structure `S`: its type is `S` applied, a
    record, or not known (an argument is read as the model unless its type says otherwise)."""
    if isinstance(ty, t.Hole):
        return True
    for x in bases(ty, c):
        if structure_of(x, c) == S or isinstance(x, t.Record):
            return True
        h, _ = head_of(x)
        if isinstance(h, t.Hole):
            return True
    return False


# ---------------------------------------------------------------------- application

def application(v, c, expected=None):
    def apply(result, arguments):
        ty = _lenient(result, c)
        for arg in arguments:
            value = walk(arg, c, ty.domain if isinstance(ty, t.Pi) else None)
            result = t.App(result, value)
            ty = substitute(ty.name, value, ty.codomain) if isinstance(ty, t.Pi) else None
        return result

    arguments = []
    head = v
    while isinstance(head, s.App):
        arguments.append(head.argument); head = head.function
    arguments.reverse()
    if (head == s.Name('extern') and arguments
            and isinstance(arguments[0], s.Literal)
            and isinstance(arguments[0].literal, s.StringLit)):
        # a named argument of `extern` (`provisional <- "why"`, 4.R5) is a mark of the declaration,
        # read by the checker and by `run` (D-2026-10-16-c), and no argument of the host's function
        return apps(t.Extern(arguments[0].literal.value),
                    [walk(x, c) for x in arguments[1:] if not isinstance(x, s.NamedArg)])
    if isinstance(head, s.Name) and head.name in c.aliases:
        alias = c.aliases[head.name]
        ns = [n for b in alias.binders for n in b.names]
        if len(arguments) < len(ns):
            raise ElaborationError(f'alias {head.name} needs {len(ns)} arguments')
        inner = c.child()
        for n, arg in zip(ns, arguments):
            inner.names[n] = walk(arg, c)
        return apply(walk(alias.value, inner), arguments[len(ns):])
    if isinstance(head, s.Lambda) and arguments and not any(isinstance(x, s.NamedArg) for x in arguments):
        # a lambda applied where it is written, `(fn k { k + 1 }) x`: its parameters take the types
        # of its arguments (a `let` in disguise)
        values = [walk(x, c) for x in arguments]
        want = c.meta('r')
        for value in reversed(values):
            want = t.Pi('_', _lenient(value, c), want)
        return apps(walk(head, c, want), values)
    q = qualified(head, c)
    if q is not None:
        return qualified_application(q[0], q[1], arguments, c, expected)
    if isinstance(head, s.Name) and is_field_name(head.name, c):
        return resolve_field(head.name, None, arguments, c, expected)
    if not isinstance(head, s.Name) or head.name not in c.signatures:
        return apply(walk(head, c), arguments)
    bs = c.signatures[head.name]
    slots = [(n, b) for b in bs for n in b.names]
    named = {x.name: x.value for x in arguments if isinstance(x, s.NamedArg)}
    positional = [x for x in arguments if not isinstance(x, s.NamedArg)]
    unknown_named = [n for n in named if n not in {m for m, _ in slots}]
    if unknown_named:
        raise ElaborationError(f'unknown named argument {unknown_named[0]}')
    inner = c.child()
    # Earlier arguments instantiate dependent parameter types. Infer implicit type arguments by
    # matching the explicit argument's type against its parameter's (`{A : U} (xs : List A)`).
    implicit_names = [n for n, b in slots if isinstance(b, s.Implicit)]
    given = {}
    deferred = []
    pos = 0
    for n, b in slots:
        if isinstance(b, s.Implicit):
            continue
        if n in named:
            arg = named[n]
        elif pos < len(positional):
            arg = positional[pos]
            # rule 2.2.2: a parameter whose type is a structure, omitted when the argument in its
            # place is not a model of it, is filled from the type's model once the call is read
            slot_type = _lenient_type(b.type, inner)
            S = structure_of(slot_type, c) if slot_type is not None else None
            if S is not None and omitted(arg, S, c):
                deferred.append((n, b)); continue
            pos += 1
        else:
            continue
        expected_type = _lenient_type(b.type, inner)
        given[n] = walk(arg, c, expected_type)
        inner.names[n] = given[n]
        if implicit_names and any(m not in given for m in implicit_names):
            pattern_type = walk_type(b.type, _without(inner, implicit_names))
            sigma = {}
            arg_type = _lenient(given[n], c)
            if solve(pattern_type, arg_type, frozenset(implicit_names), sigma, c):
                for m in implicit_names:
                    if m not in given and m in sigma:
                        given[m] = sigma[m]; inner.names[m] = sigma[m]
            if isinstance(b.type, s.Name) and b.type.name in implicit_names and b.type.name not in given:
                given[b.type.name] = arg_type; inner.names[b.type.name] = arg_type
    for n in implicit_names:
        if n not in given:
            raise ElaborationError(f'cannot infer implicit {n}')
    for n, b in deferred:
        given[n] = fill_structure(walk_type(b.type, inner), c, f'{head.name} ({n})')
        inner.names[n] = given[n]
    complete = all(n in given or isinstance(b, s.Explicit) and b.default is not None for n, b in slots)
    result = walk(head, c)
    for n, b in slots:
        if n not in given and complete and isinstance(b, s.Explicit) and b.default is not None:
            given[n] = walk(b.default, inner, walk(b.type, inner))
        if n not in given:
            break
        result = t.App(result, given[n]); inner.names[n] = given[n]
    return apply(result, positional[pos:])


def _lenient_type(u, c):
    try:
        return walk_type(u, c)
    except ElaborationError:
        return None


def _without(c, names):
    inner = c.child()
    for n in names:
        inner.names.pop(n, None)
    return inner


def omitted(arg, S, c):
    """Whether the surface argument `arg`, in the place of a parameter of structure `S`, is not its
    model (rule 2.2.2): a lambda, a literal, a list or a tuple never is; a record value always may
    be; otherwise its type decides (an unknown type keeps it as the model)."""
    if isinstance(arg, (s.Lambda, s.Literal, s.List, s.Tuple)):
        return True
    if isinstance(arg, s.RecordValue):
        return False
    try:
        value = walk(arg, c.child())
        ty = infer(value, c)
    except ElaborationError:
        return False
    return not is_model_type(ty, S, c)


# ---------------------------------------------------------------------- walk

def dotted(n, c):
    """`d.law` as the projection it is when its root is a name the context types (runtime_slice
    splits it the same way before a run), else None: `module.g` of an import stays a name."""
    if '.' not in n or n in c.names or n in c.types or n in c.aliases:
        return None
    root, *rest = n.split('.')
    if not root or not all(rest):
        return None
    if root in c.names or root in c.types:
        result = s.Name(root)
        for part in rest:
            result = s.Proj(result, part)
        return result
    return None


def plain(x):
    """A type with each program name `name@file` (run.py's `Loaded`) read as `name`, so a core
    binding at `Bool` meets a run's `Bool@core`."""
    if isinstance(x, t.Var) and '@' in x.name:
        return t.Var(x.name.partition('@')[0])
    if isinstance(x, tuple):
        return tuple(plain(y) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return replace(x, **{f.name: plain(getattr(x, f.name)) for f in fields(x)})
    return x


def operator_binding(op, ty, c):
    """The binding of `op` at the type `ty` of its left operand, matched under instantiation and
    then through the type's bases (4.R13): (Binding, sigma) or None."""
    candidates = bases(ty, c)
    for candidate in candidates + [plain(x) for x in candidates if plain(x) != x]:
        found = []
        for b in c.bindings.get(op, ()):
            sigma = {}
            if solve(b.domain, candidate, frozenset(b.vars), sigma, c):
                found.append((b, sigma))
        if found:
            exact = [x for x in found if not x[0].vars]
            return (exact or found)[0]
    return None


def walk(v, c, expected=None):
    match v:
        case s.Name(n):
            if n in c.names:
                value = c.names[n]
                return t.Var(value) if isinstance(value, str) else value
            if n in c.aliases:
                if c.aliases[n].binders:
                    raise ElaborationError(f'alias {n} needs arguments')
                return walk(c.aliases[n].value, c)
            q = qualified(v, c)
            if q is not None:
                return qualified_application(q[0], q[1], (), c, expected)
            split = dotted(n, c)
            if split is not None:
                return walk(split, c, expected)
            if is_field_name(n, c):
                return resolve_field(n, None, (), c, expected)
            return t.Var(n)
        case s.Literal(k): return t.Lit(constant(k))
        case s.Universe(): return t.Universe()
        case s.World(): return t.World()
        case s.App(): return application(v, c, expected)
        case s.Binop(op, a, b):
            left = walk(a, c); right = walk(b, c)
            try:
                ty = infer(left, c)
            except Untyped:
                ty = None
            if op in {'->', '*', '+'} and ty is not None and (isinstance(ty, t.Universe) or isinstance(left, t.Var) and left.name in c.refinements):
                left, right = as_type(left), as_type(right)
                return t.Sum((('left', left), ('right', right))) if op == '+' else (t.Pi if op == '->' else t.Sigma)('_', left, right)
            op = 'implies' if op == '->' else op
            if op not in BINDABLE:
                return apps(t.Var(op), [left, right])
            if ty is None or is_type(left, ty, c):
                # [bite 4, kept for the hash] a left operand the context does not name (4.R2 refuses
                # it), or a type typed by a subtype of `U` (`T * Float64` with `T : Concrete`, which
                # has always elaborated to the symbol applied, not to a product: a finding of the
                # bite's report, whose correction moves the cones of generators.lth and world.lth)
                return apps(t.Var(op), [left, right])
            return operator_use(op, a, left, right, ty, c)
        case s.Neg(x):
            value = walk(x, c)
            zero = t.FloatConst(0.0) if _lenient(value, c) == t.Var('Float64') else t.IntConst(0)
            return apps(t.Var('-'), [t.Lit(zero), value])
        case s.Tuple(xs):
            parts = []
            e = expected
            for i, x in enumerate(xs):
                if i == len(xs) - 1:
                    parts.append(walk(x, c, e)); break
                sg = next((y for y in bases(e, c) if isinstance(y, (t.Sigma, t.Record))), None) if e is not None else None
                if isinstance(sg, t.Record):
                    # a tuple where a record is expected: its components are the fields in order
                    fs = list(sg.fields)
                    if len(fs) == len(xs):
                        parts = [walk(y, c, ty) for y, (_, ty) in zip(xs, fs)]
                        break
                    sg = None
                parts.append(walk(x, c, sg.domain if sg is not None else None))
                e = sg.codomain if sg is not None and sg.name == '_' else None
            return pairs(parts)
        case s.Pi(ns, a, b) | s.Sigma(ns, a, b):
            inner = c.child(); domain = walk_type(a, c)
            for n in ns: inner.types[n] = domain
            return curry(t.Pi if isinstance(v, s.Pi) else t.Sigma, [(n, domain) for n in ns], walk_type(b, inner))
        case s.SigmaNamed(n, a, m, b):
            inner = c.child(); left = walk_type(a, c); inner.types[n] = left
            return t.Record(((n, left), (m, walk_type(b, inner))))
        case s.Record(fs, law):
            if law is not None:
                return walk(refined_record(v), c, expected)
            # a later field's type may name an earlier one (a dependent record)
            inner = c.child(); result = []
            for f in fs:
                ty = walk_type(f.type, inner)
                for n in f.names:
                    result.append((n, ty)); inner.types[n] = ty
            return t.Record(tuple(result))
        case s.RecordValue(fs):
            record = record_of(expected, c) if expected is not None else None
            want = dict(record.fields) if record is not None else {}
            return t.RecordValue(tuple((n, walk(x, c, want.get(n))) for n, x in fs))
        case s.Sum(xs): return t.Sum(tuple((n, walk_type(x, c)) for n, x in xs))
        case s.List(xs):
            element = None
            if expected is not None:
                h, args = head_of(base(expected, c))
                if h == t.Var('List') and len(args) == 1:
                    element = args[0]
            result = t.Var('nil')
            for x in reversed(xs): result = apps(t.Var('cons'), [walk(x, c, element), result])
            return result
        case s.Proj(x, n):
            q = qualified(v, c)
            if q is not None:
                return qualified_application(q[0], q[1], (), c, expected)
            return t.Proj(walk(x, c), n)
        case s.Block(items, body): return block(tuple(items), body, c.child(), expected)
        case s.Lambda(params, items, body):
            inner = c.child(); ps = []; shapes = []; exp = expected
            exp = _function_type(exp, c)
            for p in params:
                a = walk_type(p.type, inner) if isinstance(p, s.TypedParam) else exp.domain if isinstance(exp, t.Pi) else inner.meta(p.name if isinstance(p, s.PlainParam) else 'p')
                if isinstance(p, s.ShapeParam):
                    n = inner.fresh('p'); q = pattern(s.PTuple(p.patterns), inner); shapes.append((n, q)); ns = [n]
                    bind_pattern(q, a, inner)
                else: ns = p.names if isinstance(p, s.TypedParam) else [p.name]
                for n in ns:
                    ps.append((n, a)); inner.types[n] = a; inner.names[n] = n
                    if isinstance(exp, t.Pi): exp = substitute(exp.name, t.Var(n), exp.codomain) if exp.name != '_' else exp.codomain
                    exp = _function_type(exp, c) if exp is not None and len(ps) < _arity(params) else exp
            result = walk(s.Block(items, body), inner, exp) if items else walk(body, inner, exp)
            for n, q in reversed(shapes): result = t.Match(t.Var(n), ((q, result),))
            return curry(t.Lam, ps, result)
        case s.MatchOf(x, arms):
            value = walk(x, c)
            ty = _lenient(value, c)
            result = []
            for p, b in arms:
                inner = c.child(); q = pattern(p, inner); bind_pattern(q, ty, inner)
                result.append((q, walk(b, inner, expected)))
            return t.Match(value, tuple(result))
        case s.IfThen(cond, yes, no):
            value = walk(cond, c); a = walk(yes, c, expected); ty = _lenient(value, c)
            failures = isinstance(ty, t.App) and ty.function == t.Var('Failures')
            if no is None and failures:
                x = c.fresh('x'); xs = c.fresh('xs')
                return t.Match(value, ((t.PCon('nil', ()), t.App(t.Var('ok'), a)), (t.PCon('cons', (t.PVar(x), t.PVar(xs))), t.App(t.Var('failed'), t.Var(x)))))
            if failures: value = t.App(t.Var('holds'), value)
            b = walk(no, c, expected) if no is not None else t.Var('nothing')
            if no is None: a = t.App(t.Var('just'), a)
            return t.Match(value, ((t.PCon('true', ()), a), (t.PCon('false', ()), b)))
        case s.Subtype(s.PApp(n, ()), a, law):
            domain = walk_type(a, c)
            inner = c.child(); inner.types[n] = domain
            return t.Subtype(n, domain, walk(law, inner))
        case s.Quoted(x): return t.App(t.Var('quote'), walk(x, c))
    raise ElaborationError(f'unsupported surface form {v!r}')


def _arity(params):
    return sum(len(p.names) if isinstance(p, s.TypedParam) else 1 for p in params)


def _function_type(e, c):
    """An expected type read as a function type through definitions (`Predicate = A -> Bool`)."""
    if e is None or isinstance(e, t.Pi):
        return e
    for x in bases(e, c):
        if isinstance(x, t.Pi):
            return x
    return e


def operator_use(op, a, left, right, ty, c):
    """`left op right` (4.R13): the binding at the left operand's type, the right operand fitting
    its domain (4.R9); no binding is an error that names the type and the types that have one."""
    if ty is None or isinstance(ty, t.Hole):
        raise TypingError(f'{op} on {show_term(left)}: the type of the left operand is not known, so no model of {op} is found; annotate it', '4.R13')
    found = operator_binding(op, ty, c)
    if found is None:
        types = ', '.join(dict.fromkeys(show(b.domain) for b in c.bindings.get(op, ()))) or 'none'
        raise TypingError(f'{show_term(left)} {op} {show_term(right)}: {show(ty)} names no model of {op}; the types that have one: {types}', '4.R13')
    binding, sigma = found
    fty = binding.type
    for name in binding.vars:
        # the type parameters of the bound function, at the left operand's instance
        if isinstance(fty, t.Pi):
            fty = substitute(fty.name, sigma.get(name, t.Var(name)), fty.codomain)
    if isinstance(fty, t.Pi) and isinstance(fty.codomain, t.Pi):
        second = fty.codomain.domain if fty.codomain.name == '_' or fty.name == '_' else substitute(fty.name, left, fty.codomain).domain
        try:
            rty = infer(right, c)
        except Untyped:
            rty = None
        if rty is not None and not fits(rty, second, c) and not fits(plain(rty), plain(second), c):
            raise TypingError(f'{show_term(left)} {op} {show_term(right)}: {op} at {show(binding.domain)} ({binding.name}) takes {show(second)}, '
                              f'but {show_term(right)} has type {show(rty)}', '4.R9')
    target = apps(binding.term, [sigma[n] for n in binding.vars]) if binding.vars else binding.term
    return apps(target, [left, right])


def refined_record(v):
    """A record type with a refinement, `{ x y : A | p }`, as a subtype of the record: `{ r : { x y :
    A } | (fn x y { p }) r.x r.y }`, as tester.py's `_refined_records` writes it before a run."""
    names = [n for f in v.fields for n in f.names]
    predicate = s.Lambda(tuple(s.PlainParam(n) for n in names), (), v.law)
    for n in names:
        predicate = s.App(predicate, s.Proj(s.Name('record%'), n))
    return s.Subtype(s.PApp('record%', ()), replace(v, law=None), predicate)


# ---------------------------------------------------------------------- the context

def _prelude_acts():
    """core.lut and the files it imports, imports first (12.S22: the core encloses every file), and
    the names core.lut itself defines, the ones a file sees (run.py's `Loaded`)."""
    from .parse import parse
    seen, acts = set(), []
    own = set()

    def visit(path):
        path = path.resolve()
        if path in seen:
            return
        seen.add(path)
        r = parse(path.read_text(encoding='utf-8'))
        if not isinstance(r, s.Parsed):
            return
        for a in r.program:
            if isinstance(a, s.ImportAct):
                target = path.parent / a.path
                if not target.exists():
                    target = LIB / a.path
                if target.exists():
                    visit(target)
        acts.extend(a for a in r.program if not isinstance(a, s.ImportAct))
        if path == PRELUDE.resolve():
            own.update(a.name for a in r.program if isinstance(a, (s.Declare, s.Define, s.Alias)))

    if PRELUDE.exists():
        visit(PRELUDE)
    return tuple(acts), frozenset(own)


@lru_cache(maxsize=1)
def prelude():
    """The core's context, read once: its types, data, structures, claims and operator bindings,
    each binding elaborating to the kernel's symbol."""
    c = Context()
    acts, own = _prelude_acts()
    read(c, acts, core=True)
    c.errors = {}
    # a file sees core.lut's own names; what core.lut imports types them and stays out of sight
    # (its aliases are inlined in the types already read)
    c.aliases = {n: a for n, a in c.aliases.items() if n in own}
    c.signatures = {n: b for n, b in c.signatures.items() if n in own}
    c.defined = {n for n in c.defined if n in own}
    return c


def context_of(program, core=True):
    c = prelude().fork() if core else Context()
    # Reserve source names as well as generated names to avoid capturing a free name.
    def reserve(v):
        if isinstance(v, str): c.used.add(v)
        elif isinstance(v, tuple):
            for x in v: reserve(x)
        elif is_dataclass(v):
            for f in fields(v): reserve(getattr(v, f.name))
    reserve(program)
    read(c, program)
    return c


def read(c, program, core=False):
    """Read a program's acts into `c`: signatures, types, type definitions, labels, structures,
    claims and operator bindings; an act that cannot be read is recorded in `c.errors`."""
    for act in program:
        if isinstance(act, s.Alias): c.aliases[act.name] = act
        if isinstance(act, (s.Declare, s.Define)):
            c.signatures[act.name] = act.binders
            c.defined.add(act.name)
            if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
                c.constructors.update(n for n, _ in act.body.constructors)
                params = tuple(n for b in act.binders for n in b.names)
                for n, _ in act.body.constructors:
                    c.datas[n] = params

    def read_types():
        typed_here = set()
        for act in program:
            if isinstance(act, (s.Declare, s.Define)):
                try:
                    inner = c.child(); ps = parameters(act.binders, inner)
                    annotation = walk_type(act.type, inner) if act.type is not None else None
                    if annotation is not None or act.name not in typed_here:
                        c.types[act.name] = curry(t.Pi, ps, annotation if annotation is not None else c.meta(act.name))
                        typed_here.add(act.name)
                    if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
                        inner.types[act.name] = c.types[act.name]
                        for n, ty in act.body.constructors: c.types[n] = walk_type(ty, inner)
                except ElaborationError as e:
                    c.errors[act] = e
    if not core:
        # a label of the program is not a name core hides behind it
        written = set(_surface_labels(program))
        for n in written & set(c.aliases):
            if not any(isinstance(a, s.Alias) and a.name == n for a in program):
                del c.aliases[n]

    def read_bodies():
        # the definitions of types, unfolded where a value of the type is read (a subtype's base, a
        # record's fields): a definition at `U` (or at a function into `U`) whose body is not a `data`
        for act in program:
            if isinstance(act, s.Define) and isinstance(act.body, s.TermBody) and _defines_type(act, c):
                try:
                    inner = c.child(); ps = parameters(act.binders, inner)
                    c.bodies[act.name] = (tuple(n for n, _ in ps), walk_type(act.body.term, inner))
                except ElaborationError:
                    pass
            elif isinstance(act, s.Define) and act.name in c.bodies and not core:
                c.bodies.pop(act.name, None)

    def read_operators():
        for act in program:
            if isinstance(act, s.OperatorAct):
                c.errors.pop(act, None)
                try:
                    bind_operator(act, c, core)
                except ElaborationError as e:
                    c.errors[act] = e

    read_types()
    # 4.R6: `Even : Int` with `Even := fn n { ... }` is a type refining `Int`
    declared_at = {a.name: c.types.get(a.name) for a in program if isinstance(a, s.Declare) and not a.binders}
    for a in program:
        ty = declared_at.get(getattr(a, 'name', None))
        if (isinstance(a, s.Define) and a.type is None and not a.binders and isinstance(a.body, s.TermBody)
                and isinstance(a.body.term, s.Lambda) and ty is not None
                and not isinstance(ty, (t.Universe, t.Pi, t.Record, t.Hole))):
            c.predicates[a.name] = ty
    # A name that refines a type is known once the types are read; they are then read again
    # (11.R1: `floatPlus : Float64 -> Float64 -> Float64` after `Float64 : Real`).
    refined = {a.name for a in program if refining(a, c)}
    if refined:
        c.refinements.update(refined)
        read_types()
    read_operators()
    read_bodies()
    # a type that reads a field of a value of a defined type (`Node (p : Positions) = Fin (p.n /
    # 3)`) needs that definition: once the definitions are read, the types are read again
    if any(isinstance(a, (s.Declare, s.Define, s.OperatorAct)) for a in c.errors):
        for a in [a for a in c.errors if isinstance(a, (s.Declare, s.Define))]:
            del c.errors[a]
        read_types()
        read_operators()
        read_bodies()
    # the labels of the sums the program writes
    for act in program:
        roots = []
        if isinstance(act, (s.Declare, s.Define)) and act.name in c.types:
            roots.append(c.types[act.name])
        if isinstance(act, s.Define) and act.name in c.bodies:
            roots.append(c.bodies[act.name][1])
        if isinstance(act, s.Alias):
            try:
                inner = c.child(); parameters(act.binders, inner)
                roots.append(walk_type(act.value, inner))
            except ElaborationError:
                pass
        for root in roots:
            for x in _sums(root):
                for label, _ in x.alternatives:
                    c.labels.setdefault(label, []).append(x)
    # structures: a name declared at a record, with parameters (rule 2.2)
    for act in program:
        if isinstance(act, s.Declare) and act.binders and act.name in c.types:
            ty = c.types[act.name]; params = []
            while isinstance(ty, t.Pi):
                params.append((ty.name, ty.domain)); ty = ty.codomain
            if isinstance(ty, t.Record):
                c.structures[act.name] = Structure(tuple(params), ty)
    # claims: `X (binders) : Bool := S args model`, the binding of S's model at the args (2.2, (b))
    for act in program:
        claim = _claim(act, c)
        if claim is not None:
            S, cl = claim
            c.claims[S] = [x for x in c.claims.get(S, ()) if x.name != cl.name] + [cl]


def _surface_labels(x):
    if isinstance(x, s.Sum):
        for n, _ in x.alternatives:
            yield n
    if isinstance(x, tuple):
        for y in x:
            yield from _surface_labels(y)
    elif is_dataclass(x) and not isinstance(x, type):
        for f in fields(x):
            yield from _surface_labels(getattr(x, f.name))


def _defines_type(act, c):
    if act.type is None:
        return False
    h = act.body.term
    while isinstance(h, s.App):
        h = h.function
    if isinstance(h, s.Name) and h.name in ('primitive', 'extern', 'axiom'):
        return False
    try:
        inner = c.child(); parameters(act.binders, inner)
        return isinstance(as_type(walk(act.type, inner)), t.Universe)
    except ElaborationError:
        return False


def _sums(x):
    if isinstance(x, t.Sum):
        yield x
    if isinstance(x, tuple):
        for y in x:
            yield from _sums(y)
    elif is_dataclass(x) and not isinstance(x, type):
        for f in fields(x):
            yield from _sums(getattr(x, f.name))


def _claim(act, c):
    if not (isinstance(act, s.Define) and act.type == s.Name('Bool') and isinstance(act.body, s.TermBody)):
        return None
    args = []
    head = act.body.term
    while isinstance(head, s.App):
        args.append(head.argument); head = head.function
    args.reverse()
    if not (isinstance(head, s.Name) and head.name in c.structures
            and len(args) == len(c.structures[head.name].params) + 1):
        return None
    S = head.name
    try:
        inner = c.child(); ps = parameters(act.binders, inner)
        walked = []
        record = c.structures[S].record
        for (p, _), a in zip(c.structures[S].params, args):
            value = walk_type(a, inner); walked.append(value)
            record = substitute(p, value, record)
        model = walk(args[-1], inner, record)
    except ElaborationError:
        return None
    return S, Claim(act.name, tuple(n for n, _ in ps), tuple(walked), model)


def bind_operator(act, c, core=False):
    """`operator op := f` (4.R13): `f` bound at the type of its first operand. A binding the core
    makes elaborates to the kernel's symbol (3.S17), which is what a run reduces; a program binding
    the same function at the same type keeps it."""
    target = walk(act.value, c)
    ty = infer(target, c)
    if not isinstance(ty, t.Pi):
        raise ElaborationError('operator needs a declared function type')
    vars_ = []
    fty = ty
    while isinstance(fty, t.Pi) and is_kind(fty.domain) and fty.name != '_' and isinstance(fty.codomain, t.Pi):
        vars_.append(fty.name); fty = fty.codomain
    if not isinstance(fty, t.Pi):
        raise ElaborationError('operator needs a declared function type')
    name = act.value.name if isinstance(act.value, s.Name) else show(target)
    domain = fty.domain
    for b in c.bindings.get(act.operator, ()):
        if b.name == name and alpha_equal(b.domain, domain):
            c.operators[(act.operator, domain)] = b.term
            return
    term = t.Var(act.operator) if core else target
    binding = Binding(tuple(vars_), domain, term, ty, name)
    c.bindings[act.operator] = [b for b in c.bindings.get(act.operator, ()) if not alpha_equal(b.domain, domain)] + [binding]
    c.operators[(act.operator, domain)] = term


def elaborate_term(surface: s.Surface, context: s.SurfaceProgram | Context) -> t.Term:
    """Elaborate in a surface program (or an internal Context); see typing limits above.

    Raises ElaborationError for unsupported/inferentially unresolved cases, rather
    than returning the theory's Maybe. It does not certify well-typedness.
    """
    return walk(surface, context if isinstance(context, Context) else context_of(context))


def elaborate_program(surface_program: s.SurfaceProgram, context: Context | None = None, errors: dict | None = None) -> t.Program:
    """The kernel program of a surface program. With `errors`, an act that does not elaborate is
    left out and its error recorded there (check.py's typing reads each act in the whole file's
    context); without, the first error is raised."""
    c = context_of(surface_program) if context is None else context
    if c.errors:
        if errors is None:
            raise next(iter(c.errors.values()))
        errors.update(c.errors)
    result = []
    for act in surface_program:
        if act in c.errors:
            continue
        try:
            elaborated = elaborate_act(act, c)
        except ElaborationError as e:
            if errors is None:
                raise
            errors[act] = e
            continue
        if elaborated is not None:
            result.append(elaborated)
    return tuple(result)


def elaborate_act(act, c):
    if isinstance(act, (s.Declare, s.Define)):
        inner = c.child(); ps = parameters(act.binders, inner)
        annotation = c.types.get(act.name)
        if annotation is None:
            raise ElaborationError(f'{act.name} has no type')
        if isinstance(act, s.Declare): return t.Declare(act.name, annotation)
        expected = annotation
        for _ in ps:
            if isinstance(expected, t.Pi): expected = expected.codomain
        # A separate base declaration admits a predicate body (4.R6).
        if (act.type is None and isinstance(act.body, s.TermBody)
                and isinstance(act.body.term, s.Lambda)
                and not isinstance(expected, (t.Pi, t.Hole))):
            expected = t.Pi('_', expected, t.Var('Bool'))
        if isinstance(expected, t.Hole):
            expected = None
        match act.body:
            case s.TermBody(v): body = walk(v, inner, expected)
            case s.DataBody(xs): body = t.Data(act.name, tuple((n, walk_type(x, inner)) for n, x in xs))
            case s.ClausesBody(clauses):
                arms = []
                for clause in clauses:
                    local = inner.child(); pats = [pattern(p, local) for p in clause.patterns]
                    for q, (_, ty) in zip(pats, ps):
                        bind_pattern(q, ty, local)
                    arms.append((pairs(pats, t.PPair), walk(clause.body, local)))
                body = t.Match(pairs([t.Var(n) for n, _ in ps]), tuple(arms))
        body = curry(t.Lam, ps, body)
        if act.type is None:
            inferred = _lenient(body, c)
            # A theory's declaration supplies its record, while its body
            # supplies the laws (4.R6, 4.S9).
            declared = expected
            if not isinstance(declared, t.Record):
                annotation = inferred
            c.types[act.name] = annotation
        return t.Define(act.name, annotation, body)
    elif isinstance(act, s.Datum):
        return t.Datum(walk(act.value, c))
    return None


def show_term(v):
    """Readable surface-style rendering; no promise of parser round-tripping."""
    match v:
        case t.Var(n) | t.Primitive(n): return n
        case t.Lit(k): return json.dumps(k.value, ensure_ascii=False)
        case t.Universe(): return 'U'
        case t.World(): return 'W'
        case t.App(f, a): return f'({show_term(f)} {show_term(a)})'
        case t.Lam(n, a, b): return f'fn ({n} : {show_term(a)}) {{ {show_term(b)} }}'
        case t.Pi(n, a, b): return f'({n} : {show_term(a)}) -> {show_term(b)}'
        case t.Sigma(n, a, b): return f'({n} : {show_term(a)}) * {show_term(b)}'
        case t.Pair(a, b): return f'({show_term(a)}, {show_term(b)})'
        case t.Record(fs) | t.RecordValue(fs):
            sep = ' : ' if isinstance(v, t.Record) else ' := '
            return '{ ' + ', '.join(n + sep + show_term(x) for n, x in fs) + ' }'
        case t.Proj(r, n): return f'({show_term(r)}).{n}'
        case t.Let(n, _, x, b): return f'{{ {n} := {show_term(x)}; {show_term(b)} }}'
        case t.Sum(xs): return '{ ' + ' || '.join(n + ' : ' + show_term(x) for n, x in xs) + ' }'
        case t.Data(_, xs): return 'data { ' + '; '.join(n + ' : ' + show_term(x) for n, x in xs) + ' }'
        case t.Match(x, arms): return 'match ' + show_term(x) + ' { ' + '; '.join(show_pattern(p) + ' -> ' + show_term(b) for p, b in arms) + ' }'
        case t.Inj(n, x): return f'{n} {show_term(x)}'
        case t.Hole(n): return '?' + n if not n.startswith('?') else n
        case t.Extern(n): return 'extern ' + json.dumps(n)
        case t.Axiom(n): return 'axiom ' + json.dumps(n)
        case t.Subtype(n, a, p): return f'{{ {n} : {show_term(a)} | {show_term(p)} }}'
    raise TypeError(v)


def show_pattern(p):
    match p:
        case t.PVar(n): return n
        case t.PWild(): return '_'
        case t.PLit(k): return json.dumps(k.value)
        case t.PCon(n, ps): return n + ''.join(' (' + show_pattern(x) + ')' for x in ps)
        case t.PPair(a, b): return f'({show_pattern(a)}, {show_pattern(b)})'
        case t.PInj(n, x): return n + ' ' + show_pattern(x)
    raise TypeError(p)
