"""Python specimen of term.lth §2–§5, following term_model.lut's nominal choices.

Sources: 9a89873dad71493a72ca885585fdc7b5a8ff527d; synthesis prompt v1:
record/IA/kernel-2026-10-13/prompt.md. Law caveats and deviations: its codex.md.
Update derivation: user request v2; current audit: codex-2.md.
Update derivation: user request v3; codex-3.md records source hashes and choices.
Reduction uses an explicit generator stack for each weak-head step; externs
remain values. This module neither translates surface trees nor calls the host.
"""

# Update: 66d5cae, user request v6; IotaConstructors; audit codex-6.md.
# Update: fe3bdab, user request v4; audit codex-4.md.
# Update: 23d23f4, 048cd55, 1c521a7, reference b1582ca; user request v5; codex-5.md.
# Update: bite 12 (prompt-12.md), from 69684d7: `step` memoizes the environment and constructor
# table per program (by identity); substitution reads free names through a memo by identity.
# No law, reduction order or result changes.
# Update: bite 10 (prompt-10.md): `/=` on every concrete type, parameterized data constructors.
# Update: 051e6aa term.lth §5 PrimStructural, PrimConstructors, EqualityStuck;
# record/IA/kernel-2026-10-13/prompt-7.md; report opus-7.md.

from __future__ import annotations

import math
from collections.abc import Generator

from .term import (
    App, Axiom, Data, Datum, Declare, Define, Extern, Hole, Inj, IntConst, Lam, Let,
    Lit, FloatConst, StringConst, Match, Pair, Pattern, PCon, PInj, PLit, PPair, Primitive, Program, PVar,
    PWild, Pi, Proj, Record, RecordValue, Sigma, Subtype, Sum, Term, Universe, Var, World,
)


_BINDERS = (Lam, Pi, Sigma, Subtype)
_LEAVES = (Lit, Universe, World, Extern, Primitive, Axiom, Hole)
Env = tuple[tuple[str, str], ...]
Bindings = tuple[tuple[str, Term], ...]


def _binder_parts(t: Term) -> tuple[str, Term, Term]:
    match t:
        case Lam(x, a, b) | Pi(x, a, b) | Sigma(x, a, b) | Subtype(x, a, b):
            return x, a, b
    raise TypeError(f"not a binder: {type(t).__name__}")


def pattern_names(p: Pattern) -> tuple[str, ...]:
    """Binding occurrences in left-to-right order, including repeated names."""
    names: list[str] = []
    pending = [p]
    while pending:
        match pending.pop():
            case PVar(x):
                names.append(x)
            case PCon(_, ps):
                pending.extend(reversed(ps))
            case PPair(a, b):
                pending.extend((b, a))
            case PInj(_, q):
                pending.append(q)
            case PWild() | PLit():
                pass
            case other:
                raise TypeError(f"unknown pattern: {type(other).__name__}")
    return tuple(names)


def free_names(t: Term) -> frozenset[str]:
    """The set represented by term.lth's freeVars list; binder types are outside scope."""
    names: set[str] = set()
    pending = [(t, frozenset())]
    while pending:
        node, bound = pending.pop()
        if isinstance(node, _BINDERS):
            x, a, b = _binder_parts(node)
            pending.extend(((a, bound), (b, bound | {x})))
            continue
        match node:
            case Let(x, a, v, b):
                pending.extend(((a, bound), (v, bound), (b, bound | {x})))
            case Var(x):
                if x not in bound:
                    names.add(x)
            case App(a, b) | Pair(a, b):
                pending.extend(((a, bound), (b, bound)))
            case Inj(_, a) | Proj(a, _):
                pending.append((a, bound))
            case Match(a, arms):
                pending.append((a, bound))
                pending.extend((b, bound | set(pattern_names(p))) for p, b in arms)
            case Record(kvs):
                # [proposed] (3.S31; term.lth's freeVars says `Record kvs -> pairsFree kvs`, silent
                # on scope): a dependent record type's label binds in the LATER fields' types, never
                # in its own or in earlier ones. A `RecordValue`'s labels are labels, not names.
                inner = bound
                for k, b in kvs:
                    pending.append((b, inner))
                    inner = inner | {k}
            case Sum(kvs) | RecordValue(kvs):
                pending.extend((b, bound) for _, b in kvs)
            case Data(x, kvs):
                pending.extend((b, bound | {x}) for _, b in kvs)
            case _ if isinstance(node, _LEAVES):
                pass
            case _:
                raise TypeError(f"unknown term: {type(node).__name__}")
    return frozenset(names)


def head(t: Term) -> str:
    """Constructor name, as in term.lth head (including Let)."""
    return type(t).__name__


def _all_names(t: Term) -> set[str]:
    names: set[str] = set()
    pending = [t]
    while pending:
        node = pending.pop()
        if isinstance(node, _BINDERS):
            x, a, b = _binder_parts(node)
            names.add(x)
            pending.extend((a, b))
            continue
        match node:
            case Let(x, a, v, b):
                names.add(x)
                pending.extend((a, v, b))
            case Var(x):
                names.add(x)
            case App(a, b) | Pair(a, b):
                pending.extend((a, b))
            case Inj(_, a) | Proj(a, _):
                pending.append(a)
            case Match(a, arms):
                pending.append(a)
                for p, b in arms:
                    names.update(pattern_names(p))
                    pending.append(b)
            case Sum(kvs) | Record(kvs) | RecordValue(kvs):
                pending.extend(b for _, b in kvs)
            case Data(x, kvs):
                names.add(x)
                pending.extend(b for _, b in kvs)
            case _ if isinstance(node, _LEAVES):
                pass
            case _:
                raise TypeError(f"unknown term: {type(node).__name__}")
    return names


def _name_equal(env: Env, x: str, y: str) -> bool:
    for a, b in env:
        if x == a or y == b:
            return x == a and y == b
    return x == y


def _pattern_bindings(p: Pattern, q: Pattern) -> Env | None:
    pairs: list[tuple[str, str]] = []
    pending = [(p, q)]
    while pending:
        a, b = pending.pop()
        if type(a) is not type(b):
            return None
        match a, b:
            case PVar(x), PVar(y):
                pairs.append((x, y))
            case PWild(), PWild():
                pass
            case PLit(c), PLit(d):
                if c != d:
                    return None
            case PCon(c, ps), PCon(d, qs):
                if c != d or len(ps) != len(qs):
                    return None
                pending.extend(reversed(tuple(zip(ps, qs))))
            case PPair(a1, a2), PPair(b1, b2):
                pending.extend(((a2, b2), (a1, b1)))
            case PInj(l, a1), PInj(k, b1):
                if l != k:
                    return None
                pending.append((a1, b1))
            case _:
                raise TypeError(f"unknown pattern: {type(a).__name__}")
    env = tuple(pairs)
    # The same name occurring twice must have the same binding correspondence.
    if not all(_name_equal(env, x, y) for x, y in env):
        return None
    return env


def alpha_equal(a: Term, b: Term) -> bool:
    """Compare both trees with a stack of nearest paired bindings (including patterns and Data names)."""
    pending: list[tuple[Term, Term, Env]] = [(a, b, ())]
    while pending:
        s, t, env = pending.pop()
        if type(s) is not type(t):
            return False
        if isinstance(s, _BINDERS):
            x, a1, b1 = _binder_parts(s)
            y, a2, b2 = _binder_parts(t)
            pending.extend(((a1, a2, env), (b1, b2, ((x, y),) + env)))
            continue
        match s, t:
            case Let(x, a, v, b), Let(y, c, w, d):
                pending.extend(((a, c, env), (v, w, env), (b, d, ((x, y),) + env)))
            case Var(x), Var(y):
                if not _name_equal(env, x, y):
                    return False
            case (App(a1, b1), App(a2, b2)) | (Pair(a1, b1), Pair(a2, b2)):
                pending.extend(((a1, a2, env), (b1, b2, env)))
            case (Inj(l, a1), Inj(k, a2)) | (Proj(a1, l), Proj(a2, k)):
                if l != k:
                    return False
                pending.append((a1, a2, env))
            case Match(a1, ps), Match(a2, qs):
                if len(ps) != len(qs):
                    return False
                pending.append((a1, a2, env))
                for (p, c), (q, d) in zip(ps, qs):
                    bs = _pattern_bindings(p, q)
                    if bs is None:
                        return False
                    pending.append((c, d, bs + env))
            case (Sum(ps), Sum(qs)) | (Record(ps), Record(qs)) | (RecordValue(ps), RecordValue(qs)):
                if len(ps) != len(qs):
                    return False
                for (k, c), (l, d) in zip(ps, qs):
                    if k != l:
                        return False
                    pending.append((c, d, env))
            case Data(x, ps), Data(y, qs):
                if len(ps) != len(qs):
                    return False
                for (k, c), (l, d) in zip(ps, qs):
                    if k != l:
                        return False
                    pending.append((c, d, ((x, y),) + env))
            case _ if isinstance(s, _LEAVES):
                if s != t:
                    return False
            case _:
                raise TypeError(f"unknown term: {type(s).__name__}")
    return True


def _map_pattern(p: Pattern, rename) -> Pattern:
    def walk(q):
        match q:
            case PVar(x):
                return PVar(rename(x))
            case PCon(c, ps):
                result = []
                for child in ps:
                    result.append((yield walk(child)))
                return PCon(c, tuple(result))
            case PPair(a, b):
                left = yield walk(a)
                right = yield walk(b)
                return PPair(left, right)
            case PInj(l, child):
                value = yield walk(child)
                return PInj(l, value)
            case PWild() | PLit():
                return q
        raise TypeError(f"unknown pattern: {type(q).__name__}")
    return _run(walk(p))


def swap(x: str, y: str, t: Term) -> Term:
    """Nominal transposition from term.lth, including shadowed binder names."""
    def name(n: str) -> str:
        return y if n == x else x if n == y else n

    def walk(node):
        if isinstance(node, _BINDERS):
            n, a, b = _binder_parts(node)
            left = yield walk(a)
            right = yield walk(b)
            return type(node)(name(n), left, right)
        match node:
            case Let(n, a, v, b):
                annotation = yield walk(a)
                value = yield walk(v)
                body = yield walk(b)
                return Let(name(n), annotation, value, body)
            case Var(n):
                return Var(name(n))
            case App(a, b) | Pair(a, b):
                left = yield walk(a)
                right = yield walk(b)
                return type(node)(left, right)
            case Inj(l, a):
                value = yield walk(a)
                return Inj(l, value)
            case Proj(a, l):
                value = yield walk(a)
                return Proj(value, l)
            case Match(a, arms):
                value = yield walk(a)
                result = []
                for p, b in arms:
                    body = yield walk(b)
                    result.append((_map_pattern(p, name), body))
                return Match(value, tuple(result))
            case Sum(kvs) | Record(kvs) | RecordValue(kvs) | Data(_, kvs):
                result = []
                for k, b in kvs:
                    body = yield walk(b)
                    result.append((k, body))
                return Data(name(node.name), tuple(result)) if isinstance(node, Data) else type(node)(tuple(result))
            case _ if isinstance(node, _LEAVES):
                return node
        raise TypeError(f"unknown term: {type(node).__name__}")
    return _run(walk(t))


def _fresh_name(x: str, avoid: set[str]) -> str:
    while x in avoid:
        x += "'"
    return x


def _subterms(node: Term) -> tuple[Term, ...]:
    if isinstance(node, _BINDERS):
        _, a, b = _binder_parts(node)
        return a, b
    match node:
        case Let(_, a, v, b):
            return a, v, b
        case App(a, b) | Pair(a, b):
            return a, b
        case Inj(_, a) | Proj(a, _):
            return (a,)
        case Match(a, arms):
            return (a,) + tuple(b for _, b in arms)
        case Sum(kvs) | Record(kvs) | RecordValue(kvs) | Data(_, kvs):
            return tuple(b for _, b in kvs)
        case Var():
            return ()
        case _ if isinstance(node, _LEAVES):
            return ()
    raise TypeError(f"unknown term: {type(node).__name__}")


def _free_names_of(node: Term, free) -> frozenset[str]:
    """free_names(node) from the free names `free(child)` of its immediate subterms: the same
    scopes as `free_names`, read one level at a time."""
    if isinstance(node, _BINDERS):
        x, a, b = _binder_parts(node)
        return free(a) | (free(b) - {x})
    match node:
        case Let(x, a, v, b):
            return free(a) | free(v) | (free(b) - {x})
        case Var(x):
            return frozenset((x,))
        case App(a, b) | Pair(a, b):
            return free(a) | free(b)
        case Inj(_, a) | Proj(a, _):
            return free(a)
        case Match(a, arms):
            names = set(free(a))
            for p, b in arms:
                names.update(free(b) - set(pattern_names(p)))
            return frozenset(names)
        case Record(kvs):
            names, labels = set(), set()
            for k, b in kvs:
                names.update(free(b) - labels)
                labels.add(k)
            return frozenset(names)
        case Sum(kvs) | RecordValue(kvs):
            return frozenset().union(*(free(b) for _, b in kvs))
        case Data(x, kvs):
            return frozenset().union(*(free(b) for _, b in kvs)) - {x}
        case _ if isinstance(node, _LEAVES):
            return frozenset()
    raise TypeError(f"unknown term: {type(node).__name__}")


def _memo_free_names(memo: dict[int, tuple[Term, frozenset[str]]]):
    """`free_names`, with the free names of every subterm it reads kept in `memo` by identity
    (record/IA/kernel-2026-10-13/prompt-12.md): within one substitution the same subterms are asked
    again at each level it descends, and `s` at each binder it passes. The memo keeps each term
    it keys, so no identity is reused while it lives."""
    def lookup(u: Term) -> frozenset[str]:
        return memo[id(u)][1]

    def free(t: Term) -> frozenset[str]:
        found = memo.get(id(t))
        if found is not None:
            return found[1]
        pending = [(t, False)]
        while pending:
            node, ready = pending.pop()
            if id(node) in memo:
                continue
            if ready:
                memo[id(node)] = (node, _free_names_of(node, lookup))
                continue
            pending.append((node, True))
            pending.extend((u, False) for u in _subterms(node) if id(u) not in memo)
        return memo[id(t)][1]
    return free


# The free names substitution has read, by identity, kept across substitutions: the bodies of a
# program's definitions and arms are substituted into again and again, the same objects each time.
# Emptied when it holds more than FREE_NAMES_MEMO_LIMIT terms (it keeps each alive); only the time
# a substitution takes depends on the limit.
FREE_NAMES_MEMO_LIMIT = 1 << 12
_free_names_memo: dict[int, tuple[Term, frozenset[str]]] = {}
_memo_free = _memo_free_names(_free_names_memo)


def substitute(x: str, s: Term, t: Term) -> Term:
    """Capture-avoiding substitution, matching the model's apostrophe freshening."""
    if len(_free_names_memo) > FREE_NAMES_MEMO_LIMIT:
        _free_names_memo.clear()
    return _run(_substitute(x, s, t, _memo_free))


def _substitute(x: str, s: Term, t: Term, free_names):
    if x not in free_names(t):
        return t
    if isinstance(t, _BINDERS):
        y, a, b = _binder_parts(t)
        if x != y and x in free_names(b):
            if y in free_names(s):
                z = _fresh_name(y, {x} | _all_names(s) | _all_names(b))
                b = swap(y, z, b)
                y = z
            b = yield _substitute(x, s, b, free_names)
        a = yield _substitute(x, s, a, free_names)
        return type(t)(y, a, b)
    match t:
        case Let(y, a, v, b):
            if x != y and x in free_names(b):
                if y in free_names(s):
                    z = _fresh_name(y, {x} | _all_names(s) | _all_names(b))
                    b = swap(y, z, b)
                    y = z
                b = yield _substitute(x, s, b, free_names)
            a = yield _substitute(x, s, a, free_names)
            v = yield _substitute(x, s, v, free_names)
            return Let(y, a, v, b)
        case Var(y):
            return s if x == y else t
        case App(a, b) | Pair(a, b):
            left = yield _substitute(x, s, a, free_names)
            right = yield _substitute(x, s, b, free_names)
            return type(t)(left, right)
        case Inj(l, a):
            value = yield _substitute(x, s, a, free_names)
            return Inj(l, value)
        case Proj(a, l):
            value = yield _substitute(x, s, a, free_names)
            return Proj(value, l)
        case Record(kvs):
            # [proposed] (3.S31): a label binds in the later fields' types, as in `free_names`. A
            # label is part of the term and cannot be renamed, so once x is a label the later
            # fields are left alone; a label free in `s` is not avoided (it would be captured).
            result = []
            shadowed = False
            for k, b in kvs:
                if not shadowed:
                    b = yield _substitute(x, s, b, free_names)
                result.append((k, b))
                shadowed = shadowed or k == x
            return Record(tuple(result))
        case Sum(kvs) | RecordValue(kvs) | Data(_, kvs):
            if isinstance(t, Data):
                y = t.name
                if x == y:
                    return t
                if y in free_names(s):
                    avoid = {x} | _all_names(s)
                    for _, b in kvs:
                        avoid.update(_all_names(b))
                    z = _fresh_name(y, avoid)
                    kvs = tuple((k, swap(y, z, b)) for k, b in kvs)
                    y = z
            result = []
            for k, b in kvs:
                body = yield _substitute(x, s, b, free_names)
                result.append((k, body))
            return Data(y, tuple(result)) if isinstance(t, Data) else type(t)(tuple(result))
        case Match(a, arms):
            result = []
            for p, b in arms:
                vs = pattern_names(p)
                if x not in vs and x in free_names(b):
                    seen: set[str] = set()
                    for y in vs:
                        if y in seen:
                            continue
                        seen.add(y)
                        if y in free_names(s):
                            avoid = {x} | _all_names(s) | set(pattern_names(p)) | _all_names(b)
                            z = _fresh_name(y, avoid)
                            p = _map_pattern(p, lambda n: z if n == y else y if n == z else n)
                            b = swap(y, z, b)
                    b = yield _substitute(x, s, b, free_names)
                result.append((p, b))
            value = yield _substitute(x, s, a, free_names)
            return Match(value, tuple(result))
        case _ if isinstance(t, _LEAVES):
            return t
    raise TypeError(f"unknown term: {type(t).__name__}")


def unqualify(name: str) -> str:
    return name.rsplit(".", 1)[-1]


def canonical(t: Term) -> Term:
    """Global preorder x0, x1, …, skipping unqualified free names to prevent capture."""
    avoid = {unqualify(x) for x in free_names(t)}
    counter = 0

    def binder() -> str:
        nonlocal counter
        while f"x{counter}" in avoid:
            counter += 1
        name = f"x{counter}"
        counter += 1
        return name

    def resolve(env: Env, x: str) -> str:
        for a, b in env:
            if a == x:
                return b
        return unqualify(x)

    def walk(node, env):
        if isinstance(node, _BINDERS):
            x, a, b = _binder_parts(node)
            y = binder()  # The binder precedes its annotation in the model's traversal.
            left = yield walk(a, env)
            right = yield walk(b, ((x, y),) + env)
            return type(node)(y, left, right)
        match node:
            case Let(x, a, v, b):
                y = binder()
                annotation = yield walk(a, env)
                value = yield walk(v, env)
                body = yield walk(b, ((x, y),) + env)
                return Let(y, annotation, value, body)
            case Var(x):
                return Var(resolve(env, x))
            case App(a, b) | Pair(a, b):
                left = yield walk(a, env)
                right = yield walk(b, env)
                return type(node)(left, right)
            case Inj(l, a):
                value = yield walk(a, env)
                return Inj(l, value)
            case Proj(a, l):
                value = yield walk(a, env)
                return Proj(value, l)
            case Record(kvs):
                inner = env
                result = []
                for k, b in kvs:
                    body = yield walk(b, inner)
                    result.append((k, body))
                    inner = ((k, k),) + inner  # [proposed] (3.S31): a label shadows an outer binder
                return Record(tuple(result))
            case Sum(kvs) | RecordValue(kvs) | Data(_, kvs):
                inner = env
                if isinstance(node, Data):
                    y = binder()
                    inner = ((node.name, y),) + env
                result = []
                for k, b in kvs:
                    body = yield walk(b, inner)
                    result.append((k, body))
                return Data(y, tuple(result)) if isinstance(node, Data) else type(node)(tuple(result))
            case Match(a, arms):
                value = yield walk(a, env)
                result = []
                for p, b in arms:
                    bs = tuple((x, binder()) for x in dict.fromkeys(pattern_names(p)))
                    q = _map_pattern(p, lambda x: resolve(bs, x))
                    body = yield walk(b, bs + env)
                    result.append((q, body))
                return Match(value, tuple(result))
            case _ if isinstance(node, _LEAVES):
                return node
        raise TypeError(f"unknown term: {type(node).__name__}")
    return _run(walk(t, ()))


# Generators request another generator's result. The explicit stack replaces
# recursive head evaluation and recursive pattern demands within one step.
_Work = Generator["_Work", object, object]


def _run(work: _Work):
    stack = [work]
    value = None
    while stack:
        try:
            child = stack[-1].send(value)
        except StopIteration as done:
            stack.pop()
            value = done.value
        else:
            stack.append(child)
            value = None
    return value


_OPERATORS = {"+", "*", "-", "==", "<", "/", "mod", "<=", ">", ">=", "/="}
# The names core.lut binds to a `primitive` body; a program (cli.py's bootstrap, eval_at) defines
# each as `Primitive name`. toFloat64 is applied to one argument, the rest to two.
BOOTSTRAP_PRIMITIVES = tuple(sorted(_OPERATORS)) + ("toFloat64",)


def _operator(t: Term) -> str | None:
    return t.name if isinstance(t, Primitive) and t.name in _OPERATORS else None


def _finite(x: float) -> Term | None:
    # 11.S7: NaN and an overflow are errors and no constant; the step does not exist
    return Lit(FloatConst(x)) if math.isfinite(x) else None


def _truth(b: bool) -> Term:
    return Var("true" if b else "false")


def _primitive(op: str, a, b) -> Term | None:
    """PrimInt, PrimFloat, PrimString on two constants of one type; None is no step."""
    if type(a) is not type(b):
        return None
    x, y = a.value, b.value
    if isinstance(a, IntConst):
        match op:
            case "+": return Lit(IntConst(x + y))
            case "-": return Lit(IntConst(x - y))
            case "*": return Lit(IntConst(x * y))
            case "/" | "mod":
                if y == 0:
                    return None
                return Lit(IntConst(x // y if op == "/" else x % y))
    elif isinstance(a, FloatConst):
        try:
            match op:
                case "+": return _finite(x + y)
                case "-": return _finite(x - y)
                case "*": return _finite(x * y)
                case "/": return None if y == 0 else _finite(x / y)
        except OverflowError:
            return None
    elif isinstance(a, StringConst):
        match op:
            case "+": return Lit(StringConst(x + y))
            case "/=": return _truth(x != y)  # 4.R8, PrimString [proposed]
    if isinstance(a, (IntConst, FloatConst)):
        match op:  # `==` is _equal's
            case "<": return _truth(x < y)
            case "<=": return _truth(x <= y)
            case ">": return _truth(x > y)
            case ">=": return _truth(x >= y)
            case "/=": return _truth(x != y)
    return None


def _to_float64(c) -> Term | None:
    if not isinstance(c, IntConst):
        return None
    try:
        return _finite(float(c.value))
    except OverflowError:
        return None


def _constructor(t: Term) -> tuple[str, tuple[Term, ...]] | None:
    args = []
    while isinstance(t, App):
        args.append(t.argument)
        t = t.function
    if isinstance(t, Var):
        return t.name, tuple(reversed(args))
    return None


class _Constructors(dict):
    """A constructor's name to the constructors of its data; `arity` counts its type's Pis."""

    def __init__(self) -> None:
        super().__init__()
        self.arity: dict[str, int] = {}


def _concrete(constructors: _Constructors, t: Term) -> bool:
    """A closed value of concrete parts (term.lth §5): constants, pairs, records with distinct
    labels, injections, and constructors of a data of the program applied to all their parts.
    A lambda, an extern, a hole, an open term or a part not yet a value is not."""
    pending = [t]
    while pending:
        node = pending.pop()
        match node:
            case Lit():
                pass
            case Pair(a, b):
                pending.extend((a, b))
            case RecordValue(fields):
                if len({k for k, _ in fields}) != len(fields):
                    return False
                pending.extend(v for _, v in fields)
            case Inj(_, v):
                pending.append(v)
            case _:
                view = _constructor(node)
                if view is None or view[0] not in constructors or len(view[1]) != constructors.arity[view[0]]:
                    return False
                pending.extend(view[1])
    return True


def _equal(constructors: _Constructors, a: Term, b: Term) -> bool | None:
    """Structural `==` (PrimStructural, PrimConstructors); None where it does not step
    (EqualityStuck, and the conservative readings of record/IA/kernel-2026-10-13/opus-7.md: two values of different
    types, records with different labels)."""
    if not (_concrete(constructors, a) and _concrete(constructors, b)):
        return None
    equal = True
    pending = [(a, b)]
    while pending:
        s, t = pending.pop()
        match s, t:
            case Lit(c), Lit(d):
                if type(c) is not type(d):
                    return None
                equal = equal and c.value == d.value
            case Pair(s1, s2), Pair(t1, t2):
                pending.extend(((s1, t1), (s2, t2)))
            case RecordValue(ps), RecordValue(qs):
                fields = dict(qs)
                if set(fields) != {k for k, _ in ps}:
                    return None
                pending.extend((v, fields[k]) for k, v in ps)
            case Inj(l, v), Inj(k, w):
                if l == k:
                    pending.append((v, w))
                else:
                    equal = False
            case _:
                left, right = _constructor(s), _constructor(t)
                if left is None or right is None:
                    return None
                if left[0] == right[0]:
                    pending.extend(zip(left[1], right[1]))
                elif right[0] in constructors[left[0]]:
                    equal = False
                else:
                    return None
    return equal


def _comparable(constructors: _Constructors, t: Term) -> bool:
    """A weak head normal form whose head `==` may compare: its right operand may then step."""
    if isinstance(t, (Lit, Pair, RecordValue, Inj)):
        return True
    view = _constructor(t)
    return view is not None and view[0] in constructors


def _apply_args(name: str, args: tuple[Term, ...]) -> Term:
    t: Term = Var(name)
    for a in args:
        t = App(t, a)
    return t


# Pattern answers: None is a definite mismatch, bindings a match, Demand a head step.
class _Blocked:
    pass


class _Demand:
    def __init__(self, value: Term):
        self.value = value


def _demand(env: dict[str, Term | None], constructors: dict[str, frozenset[str]], v: Term) -> _Work:
    changed, w = yield _step(env, constructors, v)
    return _Demand(w) if changed else _Blocked()


def _pattern(env: dict[str, Term | None], constructors: dict[str, frozenset[str]], p: Pattern, v: Term) -> _Work:
    match p:
        case PVar(x):
            return ((x, v),)
        case PWild():
            return ()
        case PLit(c):
            if isinstance(v, Lit):
                return () if c == v.constant else None
        case PPair(a, b) if isinstance(v, Pair):
            xs = yield _pattern(env, constructors, a, v.left)
            if xs is None or isinstance(xs, _Blocked):
                return xs
            if isinstance(xs, _Demand):
                return _Demand(Pair(xs.value, v.right))
            ys = yield _pattern(env, constructors, b, v.right)
            if ys is None or isinstance(ys, _Blocked):
                return ys
            if isinstance(ys, _Demand):
                return _Demand(Pair(v.left, ys.value))
            return xs + ys
        case PInj(l, q) if isinstance(v, Inj):
            if l != v.label:
                return None
            xs = yield _pattern(env, constructors, q, v.value)
            return _Demand(Inj(l, xs.value)) if isinstance(xs, _Demand) else xs
        case PCon(c, ps):
            view = _constructor(v)
            if view is not None and view[0] not in env and view[0] == c:
                args = view[1]
                if len(args) != len(ps):
                    return None
                bs: Bindings = ()
                for i, (q, a) in enumerate(zip(ps, args)):
                    xs = yield _pattern(env, constructors, q, a)
                    if xs is None or isinstance(xs, _Blocked):
                        return xs
                    if isinstance(xs, _Demand):
                        return _Demand(_apply_args(c, args[:i] + (xs.value,) + args[i + 1:]))
                    bs += xs
                return bs
            if view is not None and view[0] != c and c in constructors.get(view[0], ()):
                return None
        case PPair() | PInj():
            pass
        case _:
            raise TypeError(f"unknown pattern: {type(p).__name__}")
    return (yield _demand(env, constructors, v))


def _consistent(bs: Bindings) -> bool:
    seen: dict[str, Term] = {}
    for x, v in bs:
        if x in seen and not alpha_equal(seen[x], v):
            return False
        seen[x] = v
    return True


def _demand_parts(env: dict[str, Term | None], constructors: dict[str, frozenset[str]], t: Term) -> _Work:
    """EqualityDemandsParts: one step in the leftmost part of a pair or record value that steps."""
    match t:
        case Pair(a, b):
            changed, k = yield _demand_parts(env, constructors, a)
            if changed:
                return True, Pair(k, b)
            changed, k = yield _demand_parts(env, constructors, b)
            return changed, Pair(a, k) if changed else t
        case RecordValue(fields):
            for n, (key, v) in enumerate(fields):
                changed, k = yield _demand_parts(env, constructors, v)
                if changed:
                    return True, RecordValue(fields[:n] + ((key, k),) + fields[n + 1:])
            return False, t
        case _:
            return (yield _step(env, constructors, t))


def _step(env: dict[str, Term | None], constructors: dict[str, frozenset[str]], t: Term) -> _Work:
    match t:
        case Let(x, _, v, b):
            return True, substitute(x, v, b)
        case Var(x):
            body = env.get(x)
            return (False, t) if body is None else (True, body)
        case App(Lam(x, _, b), a):
            return True, substitute(x, a, b)
        case App(App(op, i), j) if _operator(op) in ("==", "/="):
            # PrimStructural, PrimConstructors, EqualityStuck: operands to weak head normal
            # form, left first; then one step to true or false, or none.
            changed, k = yield _step(env, constructors, i)
            if changed:
                return True, App(App(op, k), j)
            if not _comparable(constructors, i):
                return False, t
            # EqualityDemandsParts: a part not yet a value is reduced in place, leftmost first
            # (the parts of the left operand, then the right operand, then its parts)
            changed, k = yield _demand_parts(env, constructors, i)
            if changed:
                return True, App(App(op, k), j)
            changed, k = yield _step(env, constructors, j)
            if changed:
                return True, App(App(op, i), k)
            changed, k = yield _demand_parts(env, constructors, j)
            if changed:
                return True, App(App(op, i), k)
            result = _equal(constructors, i, j)
            if result is None:
                return False, t
            return True, _truth(result if op.name == "==" else not result)
        case App(App(Var("and" | "or" as conn), i), j) if conn not in env:
            # `and`/`or` on Var "true"/Var "false" (the Bool of core), left operand first,
            # the right one only when the left does not decide
            changed, k = yield _step(env, constructors, i)
            if changed:
                return True, App(App(Var(conn), k), j)
            if i == Var("true" if conn == "and" else "false"):
                return True, j
            if i == Var("false" if conn == "and" else "true"):
                return True, i
            return False, t
        case App(Primitive("toFloat64") as f, a):
            if isinstance(a, Lit):
                result = _to_float64(a.constant)
                return result is not None, t if result is None else result
            changed, k = yield _step(env, constructors, a)
            return changed, App(f, k)
        case App(App(op, i), j) if _operator(op) is not None:
            if isinstance(i, Lit):
                if isinstance(j, Lit):
                    result = _primitive(_operator(op), i.constant, j.constant)
                    return result is not None, t if result is None else result
                changed, k = yield _step(env, constructors, j)
                return changed, App(App(op, i), k)
            changed, k = yield _step(env, constructors, i)
            return changed, App(App(op, k), j)
        case App(f, a):
            changed, g = yield _step(env, constructors, f)
            return changed, App(g, a)
        case Proj(r, label):
            if isinstance(r, RecordValue):
                for key, value in r.fields:
                    if key == label:
                        return True, value
                return False, t
            changed, value = yield _step(env, constructors, r)
            return changed, Proj(value, label)
        case Match(s, arms):
            changed, value = yield _step(env, constructors, s)
            if changed:
                return True, Match(value, arms)
            for p, b in arms:
                bs = yield _pattern(env, constructors, p, s)
                if isinstance(bs, _Blocked):
                    return False, t
                if isinstance(bs, _Demand):
                    return True, Match(bs.value, arms)
                if bs is not None and _consistent(bs):
                    fresh = []
                    avoid = _all_names(b) | {x for x, _ in bs}
                    for _, v in bs:
                        avoid.update(_all_names(v))
                    for x, v in bs:
                        z = _fresh_name(x, avoid)
                        avoid.add(z)
                        b = substitute(x, Var(z), b)
                        fresh.append((z, v))
                    for z, v in fresh:
                        b = substitute(z, v, b)
                    return True, b
            changed, v = yield _step(env, constructors, s)
            return changed, Match(v, arms)
        case _ if isinstance(t, _BINDERS + _LEAVES + (Pair, Inj, Sum, Data, Record, RecordValue)):
            return False, t
    raise TypeError(f"unknown term: {type(t).__name__}")


# What `step` reads from a program, memoized (record/IA/kernel-2026-10-13/prompt-12.md): the
# program last read, by identity (as check.py's `constructors`), with its environment and its
# constructor table. Both are pure functions of the program, which is immutable, and `_step` only
# reads them; the reference kept here makes an identity test safe.
_tables: list = [None, None, None]


def _program_tables(program: Program) -> tuple[dict[str, Term | None], _Constructors]:
    if _tables[0] is program:
        return _tables[1], _tables[2]
    env, constructors = _build_tables(program)
    _tables[:] = [program, env, constructors]
    return env, constructors


def step(program: Program, t: Term) -> Term | None:
    """One weak-head transition; None means weak head normal form."""
    env, constructors = _program_tables(program)
    changed, value = _run(_step(env, constructors, t))
    return value if changed else None


def _build_tables(program: Program) -> tuple[dict[str, Term | None], _Constructors]:
    env: dict[str, Term | None] = {}
    for act in program:
        match act:
            case Define(x, _, b):
                env.setdefault(x, b)
            case Declare() | Datum():
                pass
            case _:
                raise TypeError(f"unknown act: {type(act).__name__}")
    # Definitions retain Delta priority over declarations, as in term.lth.
    # Every act name is excluded from constructor matching, including holes.
    for act in program:
        if isinstance(act, Declare):
            env.setdefault(act.name, None)
    constructors = _Constructors()
    for act in program:
        body = act.body if isinstance(act, Define) else None
        while isinstance(body, Lam):  # a parameterized data: the constructors through its binders
            body = body.body
        if isinstance(body, Data):
            names = frozenset(name for name, _ in body.constructors if name not in env)
            for name, ty in body.constructors:
                if name in names:
                    constructors[name] = names
                    constructors.arity[name] = 0
                    while isinstance(ty, Pi):
                        constructors.arity[name] += 1
                        ty = ty.codomain
    return env, constructors


def reduce(program: Program, fuel: int, t: Term) -> Term | None:
    """Exactly term.lth's fuelled iteration, including the final observation unit."""
    if type(fuel) is not int or fuel < 0:
        raise ValueError("fuel must be a non-negative integer")
    while fuel:
        value = step(program, t)
        if value is None:
            return t
        t = value
        fuel -= 1
    return None


def eval_at(expected: type, t: Term, *, fuel: int = 1000) -> int | float | str | None:
    """Evaluate scalar terms, checking their resulting constant type (term.lth §6).

    Core arithmetic names are definitions of primitives. Fuel exhaustion, stuck
    terms and type mismatch give None; fuel is a caller-selectable parameter.
    """
    constants = {int: IntConst, float: FloatConst, str: StringConst}
    if expected not in constants:
        raise TypeError("expected must be int, float or str")
    program = tuple(Define(op, Universe(), Primitive(op)) for op in BOOTSTRAP_PRIMITIVES)
    value = reduce(program, fuel, t)
    if isinstance(value, Lit) and type(value.constant) is constants[expected]:
        return value.constant.value
    return None
