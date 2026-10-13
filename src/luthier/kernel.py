"""Python specimen of term.lth §2–§5, following term_model.lut's nominal choices.

Sources: 9a89873dad71493a72ca885585fdc7b5a8ff527d; synthesis prompt v1:
record/IA/kernel-2026-10-13/prompt.md. Law caveats and deviations: its codex.md.
Update derivation: user request v2; current audit: codex-2.md.
Update derivation: user request v3; codex-3.md records source hashes and choices.
Reduction uses an explicit generator stack for each weak-head step; externs
remain values. This module neither translates surface trees nor calls the host.
"""

# Update: fe3bdab, user request v4; audit codex-4.md.

from __future__ import annotations

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
            case Sum(kvs) | Record(kvs) | RecordValue(kvs):
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
    """Compare both trees with a stack of nearest paired bindings (including patterns; Data names are fixed)."""
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
                if x != y or len(ps) != len(qs):
                    return False
                for (k, c), (l, d) in zip(ps, qs):
                    if k != l:
                        return False
                    pending.append((c, d, env))
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


def substitute(x: str, s: Term, t: Term) -> Term:
    """Capture-avoiding substitution, matching the model's apostrophe freshening."""
    return _run(_substitute(x, s, t))


def _substitute(x: str, s: Term, t: Term):
    if x not in free_names(t):
        return t
    if isinstance(t, _BINDERS):
        y, a, b = _binder_parts(t)
        if x != y and x in free_names(b):
            if y in free_names(s):
                z = _fresh_name(y, {x} | _all_names(s) | _all_names(b))
                b = swap(y, z, b)
                y = z
            b = yield _substitute(x, s, b)
        a = yield _substitute(x, s, a)
        return type(t)(y, a, b)
    match t:
        case Let(y, a, v, b):
            if x != y and x in free_names(b):
                if y in free_names(s):
                    z = _fresh_name(y, {x} | _all_names(s) | _all_names(b))
                    b = swap(y, z, b)
                    y = z
                b = yield _substitute(x, s, b)
            a = yield _substitute(x, s, a)
            v = yield _substitute(x, s, v)
            return Let(y, a, v, b)
        case Var(y):
            return s if x == y else t
        case App(a, b) | Pair(a, b):
            left = yield _substitute(x, s, a)
            right = yield _substitute(x, s, b)
            return type(t)(left, right)
        case Inj(l, a):
            value = yield _substitute(x, s, a)
            return Inj(l, value)
        case Proj(a, l):
            value = yield _substitute(x, s, a)
            return Proj(value, l)
        case Sum(kvs) | Record(kvs) | RecordValue(kvs) | Data(_, kvs):
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
                body = yield _substitute(x, s, b)
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
                    b = yield _substitute(x, s, b)
                result.append((p, b))
            value = yield _substitute(x, s, a)
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
            case Sum(kvs) | Record(kvs) | RecordValue(kvs) | Data(_, kvs):
                inner = env
                if isinstance(node, Data):
                    y = node.name
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


_OPERATORS = {"+", "*", "-", "==", "<"}


def _operator(t: Term) -> str | None:
    return t.name if isinstance(t, Primitive) and t.name in _OPERATORS else None


def _primitive(op: str, a, b) -> Term | None:
    if type(a) is not type(b):
        return None
    if isinstance(a, IntConst):
        if op in {"+", "*", "-"}:
            value = a.value + b.value if op == "+" else a.value * b.value if op == "*" else a.value - b.value
            return Lit(IntConst(value))
        return Var("true" if (a.value == b.value if op == "==" else a.value < b.value) else "false")
    if isinstance(a, FloatConst) and op == "+":
        return Lit(FloatConst(a.value + b.value))
    if isinstance(a, StringConst) and op == "==":
        return Var("true" if a.value == b.value else "false")
    return None


def _constructor(t: Term) -> tuple[str, tuple[Term, ...]] | None:
    args = []
    while isinstance(t, App):
        args.append(t.argument)
        t = t.function
    if isinstance(t, Var):
        return t.name, tuple(reversed(args))
    return None


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


def _demand(env: dict[str, Term | None], v: Term) -> _Work:
    changed, w = yield _step(env, v)
    return _Demand(w) if changed else _Blocked()


def _pattern(env: dict[str, Term | None], p: Pattern, v: Term) -> _Work:
    match p:
        case PVar(x):
            return ((x, v),)
        case PWild():
            return ()
        case PLit(c):
            if isinstance(v, Lit):
                return () if c == v.constant else None
        case PPair(a, b) if isinstance(v, Pair):
            xs = yield _pattern(env, a, v.left)
            if xs is None or isinstance(xs, _Blocked):
                return xs
            if isinstance(xs, _Demand):
                return _Demand(Pair(xs.value, v.right))
            ys = yield _pattern(env, b, v.right)
            if ys is None or isinstance(ys, _Blocked):
                return ys
            if isinstance(ys, _Demand):
                return _Demand(Pair(v.left, ys.value))
            return xs + ys
        case PInj(l, q) if isinstance(v, Inj):
            if l != v.label:
                return None
            xs = yield _pattern(env, q, v.value)
            return _Demand(Inj(l, xs.value)) if isinstance(xs, _Demand) else xs
        case PCon(c, ps):
            view = _constructor(v)
            if view is not None and view[0] == c:
                args = view[1]
                if len(args) != len(ps):
                    return None
                bs: Bindings = ()
                for i, (q, a) in enumerate(zip(ps, args)):
                    xs = yield _pattern(env, q, a)
                    if xs is None or isinstance(xs, _Blocked):
                        return xs
                    if isinstance(xs, _Demand):
                        return _Demand(_apply_args(c, args[:i] + (xs.value,) + args[i + 1:]))
                    bs += xs
                return bs
        case PPair() | PInj():
            pass
        case _:
            raise TypeError(f"unknown pattern: {type(p).__name__}")
    return (yield _demand(env, v))


def _consistent(bs: Bindings) -> bool:
    seen: dict[str, Term] = {}
    for x, v in bs:
        if x in seen and not alpha_equal(seen[x], v):
            return False
        seen[x] = v
    return True


def _step(env: dict[str, Term | None], t: Term) -> _Work:
    match t:
        case Let(x, _, v, b):
            return True, substitute(x, v, b)
        case Var(x):
            body = env.get(x)
            return (False, t) if body is None else (True, body)
        case App(Lam(x, _, b), a):
            return True, substitute(x, a, b)
        case App(App(op, i), j) if _operator(op) is not None:
            if isinstance(i, Lit):
                if isinstance(j, Lit):
                    result = _primitive(_operator(op), i.constant, j.constant)
                    return result is not None, t if result is None else result
                changed, k = yield _step(env, j)
                return changed, App(App(op, i), k)
            changed, k = yield _step(env, i)
            return changed, App(App(op, k), j)
        case App(f, a):
            changed, g = yield _step(env, f)
            return changed, App(g, a)
        case Proj(r, label):
            if isinstance(r, RecordValue):
                for key, value in r.fields:
                    if key == label:
                        return True, value
                return False, t
            changed, value = yield _step(env, r)
            return changed, Proj(value, label)
        case Match(s, arms):
            changed, value = yield _step(env, s)
            if changed:
                return True, Match(value, arms)
            for p, b in arms:
                bs = yield _pattern(env, p, s)
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
            changed, v = yield _step(env, s)
            return changed, Match(v, arms)
        case _ if isinstance(t, _BINDERS + _LEAVES + (Pair, Inj, Sum, Data, Record, RecordValue)):
            return False, t
    raise TypeError(f"unknown term: {type(t).__name__}")


def step(program: Program, t: Term) -> Term | None:
    """One weak-head transition; None means weak head normal form."""
    env: dict[str, Term | None] = {}
    for act in program:
        match act:
            case Define(x, _, b):
                env.setdefault(x, b)
            case Declare() | Datum():
                pass
            case _:
                raise TypeError(f"unknown act: {type(act).__name__}")
    changed, value = _run(_step(env, t))
    return value if changed else None


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
