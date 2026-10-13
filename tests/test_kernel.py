"""term.lth §2–§5 law cases, plus Alpha's inherited Object laws.

Inputs: source revision 9a89873dad71493a72ca885585fdc7b5a8ff527d and
record/IA/kernel-2026-10-13/prompt.md v1. Generator v2 (records): seed 0x10132026,
100 terms per law, recursive-constructor budget 7; pattern budget at most 3;
small programs at most 4 acts and term budget 4 per embedded term.
Leaf constructors cost zero; each recursive constructor costs one, and size-1
is split among its children (matching the prompt's size-zero convention).
Update prompt: user request v2, recorded in codex-2.md.
Update prompt: user request v3; source commits cc2542d and 2409c59, codex-3.md.
Update: fe3bdab, user request v4; generator v3 adds Let; same seed and budgets.
Update: user request v5, 23d23f4/048cd55/1c521a7, reference b1582ca;
generator v4 carries Axiom text, same seed and budgets.
Update: user request v6, source 66d5cae; IotaConstructors, same seed and budgets.
Update: prompt-7.md, source 051e6aa; structural ==, same seed and budgets.
Tests are finite law evidence, not a universal semantic certificate.
"""

from copy import deepcopy
from dataclasses import FrozenInstanceError, fields, is_dataclass
import random

import pytest

from luthier.kernel import (
    alpha_equal, canonical, eval_at, free_names, head, pattern_names, step, reduce, substitute, swap, unqualify,
)
from luthier.term import (
    Act, App, Axiom, Constant, Data, Datum, Declare, Define, Extern, FloatConst,
    Hole, Inj, IntConst, Lam, Let, Lit, Match, Pair, Pattern, PCon, PInj, PLit,
    PPair, Primitive, Program, PVar, PWild, Pi, Sigma, StringConst, Subtype,
    Sum, Proj, Record, RecordValue, Term, Universe, Var, World,
)

SEED = 0x10132026
CASES = 100
SIZE = 7
NAMES = ("x", "y", "z", "x0", "x1", "x'", "m.x", "a.b.c", "", "true", "false", "+", "*", "==", "<")
LABELS = ("left", "right", "C", "D", "m.C", "")
BINDERS = (Lam, Pi, Sigma, Subtype)


def split_size(rng: random.Random, size: int, count: int) -> tuple[int, ...]:
    """Split one exact non-negative budget among the recursive arguments."""
    if count == 0:
        return ()
    cuts = sorted(rng.randint(0, size) for _ in range(count - 1))
    ends = (0, *cuts, size)
    return tuple(b - a for a, b in zip(ends, ends[1:]))


def constant(rng: random.Random) -> Constant:
    kind = rng.randrange(3)
    if kind == 0:
        return IntConst(rng.randint(-20, 20))
    if kind == 1:
        return FloatConst(rng.choice((-2.5, 0.0, 1.25, 9.5)))
    return StringConst(rng.choice(("", "text", "中文", "a.b")))


def pattern(rng: random.Random, size: int) -> Pattern:
    constructors = (PVar, PWild, PLit) if size == 0 else (PVar, PWild, PLit, PCon, PPair, PInj)
    cls = rng.choice(constructors)
    if cls is PVar:
        return PVar(rng.choice(NAMES))
    if cls is PWild:
        return PWild()
    if cls is PLit:
        return PLit(constant(rng))
    if cls is PCon:
        count = rng.randrange(3)
        budgets = split_size(rng, size - 1, count)
        return PCon(rng.choice(LABELS), tuple(pattern(rng, b) for b in budgets))
    if cls is PPair:
        a, b = split_size(rng, size - 1, 2)
        return PPair(pattern(rng, a), pattern(rng, b))
    return PInj(rng.choice(LABELS), pattern(rng, size - 1))


def term(rng: random.Random, size: int) -> Term:
    """At zero only non-recursive Term constructors; otherwise split size-1."""
    leaves = (Var, Lit, Universe, World, Extern, Primitive, Axiom, Hole)
    cls = rng.choice(leaves if size == 0 else leaves + BINDERS + (App, Pair, Match, Inj, Sum, Data, Record, RecordValue, Proj, Let))
    if cls in (Universe, World):
        return cls()
    if cls in (Var, Hole, Extern, Primitive, Axiom):
        return cls(rng.choice(NAMES))
    if cls is Lit:
        return Lit(constant(rng))
    if cls in BINDERS or cls in (App, Pair):
        a, b = split_size(rng, size - 1, 2)
        args = (term(rng, a), term(rng, b))
        return cls(rng.choice(NAMES), *args) if cls in BINDERS else cls(*args)
    if cls is Let:
        budgets = split_size(rng, size - 1, 3)
        return Let(rng.choice(NAMES), *(term(rng, b) for b in budgets))
    if cls is Proj:
        return Proj(term(rng, size - 1), rng.choice(LABELS))
    if cls is Inj:
        return Inj(rng.choice(LABELS), term(rng, size - 1))
    count = rng.randrange(3)
    budgets = split_size(rng, size - 1, count + (cls is Match))
    if cls is Match:
        value = term(rng, budgets[0])
        arms = tuple((pattern(rng, min(3, b)), term(rng, b)) for b in budgets[1:])
        return Match(value, arms)
    kvs = tuple((rng.choice(LABELS), term(rng, b)) for b in budgets)
    return Data(rng.choice(NAMES), kvs) if cls is Data else cls(kvs)


def program(rng: random.Random) -> Program:
    acts = []
    for _ in range(rng.randrange(5)):
        cls = rng.choice((Declare, Define, Datum))
        if cls is Datum:
            acts.append(Datum(term(rng, 4)))
        elif cls is Declare:
            acts.append(Declare(rng.choice(NAMES), term(rng, 4)))
        else:
            acts.append(Define(rng.choice(NAMES), term(rng, 4), term(rng, 4)))
    return tuple(acts)


def corpus() -> tuple[Term, ...]:
    ty = Universe()
    return (
        *(Var(x) for x in NAMES), Lit(IntConst(-2)), Lit(FloatConst(1.25)), Lit(StringConst("中文")),
        ty, World(), Extern("host.fn"), Primitive("+"), Axiom("axiom text"), Hole("m.h"),
        Lam("x", Var("x"), Lam("x", Var("x"), Var("x"))),
        Let("x", Var("x"), Var("x"), Pair(Var("x"), Var("y"))),
        Let("y", ty, Var("x"), Let("y", Var("y"), Var("y"), Var("y"))),
        Pi("x", ty, Var("x")), Sigma("x", ty, Var("x")), Subtype("x", ty, Var("x")),
        Lam("a", ty, Pair(Var("a"), Var("x0"))), Lam("a", ty, Var("m.x0")),
        App(Lam("x", ty, Var("x")), Lit(IntConst(3))), Pair(Var("x"), Var("y")),
        Inj("m.tag", Var("m.x")), Sum((("m.tag", Var("m.x")),)),
        Data("D", (("m.C", Pi("x", Var("D"), App(Var("D"), Var("x")))),)),
        Match(Var("x"), ((PPair(PVar("x"), PVar("y")), Pair(Var("x"), Var("y"))),)),
        Match(Var("v"), ((PCon("C", (PVar("x"), PVar("x"))), Var("x")),)),
        Match(Var("v"), ((PInj("left", PVar("y")), Lam("y", Var("y"), Var("x"))),)),
        Match(Inj("left", Var("v")), ((PInj("right", PWild()), Var("b")),)),
        Match(Var("x"), ()), Sum(()), Data("D", ()),
    )


@pytest.fixture
def rng():
    return random.Random(SEED)


@pytest.fixture
def samples(rng):
    return corpus() + tuple(term(rng, SIZE) for _ in range(CASES))


def binder_parts(t):
    # An independent field view for constructing renamed law witnesses.
    return tuple(getattr(t, f.name) for f in fields(t))


def alpha_variant(t: Term) -> Term:
    """Independent binder renaming, avoiding the implementation's canonical/swapping helpers."""
    counter = 0

    def fresh():
        nonlocal counter
        counter += 1
        return f"renamed{counter}"

    def pat(p, names):
        match p:
            case PVar(x):
                return PVar(names[x])
            case PPair(a, b):
                return PPair(pat(a, names), pat(b, names))
            case PCon(c, ps):
                return PCon(c, tuple(pat(q, names) for q in ps))
            case PInj(l, q):
                return PInj(l, pat(q, names))
            case _:
                return p

    def walk(node, env):
        if isinstance(node, BINDERS):
            x, a, b = binder_parts(node)
            y = fresh()
            return type(node)(y, walk(a, env), walk(b, env | {x: y}))
        match node:
            case Let(x, a, v, b):
                y = fresh()
                return Let(y, walk(a, env), walk(v, env), walk(b, env | {x: y}))
            case Var(x):
                return Var(env.get(x, x))
            case App(a, b) | Pair(a, b):
                return type(node)(walk(a, env), walk(b, env))
            case Inj(l, a):
                return Inj(l, walk(a, env))
            case Sum(kvs) | Record(kvs) | RecordValue(kvs):
                return type(node)(tuple((k, walk(b, env)) for k, b in kvs))
            case Proj(a, l):
                return Proj(walk(a, env), l)
            case Data(x, kvs):
                y = fresh()
                return Data(y, tuple((k, walk(b, env | {x: y})) for k, b in kvs))
            case Match(a, arms):
                value = walk(a, env)
                result = []
                for p, b in arms:
                    names = {x: fresh() for x in dict.fromkeys(pattern_names(p))}
                    result.append((pat(p, names), walk(b, env | names)))
                return Match(value, tuple(result))
            case _:
                return node
    return walk(t, {})


def fresh_for(t, prefix="fresh"):
    while prefix in free_names(t):
        prefix += "'"
    return prefix


def test_reflexive(samples):
    for t in samples:
        assert alpha_equal(t, t)


def test_symmetric(samples):
    for t in samples:
        u = alpha_variant(t)
        assert alpha_equal(t, u)
        assert alpha_equal(u, t)


def test_transitive(samples):
    for t in samples:
        u = alpha_variant(t)
        v = alpha_variant(u)
        assert alpha_equal(t, u) and alpha_equal(u, v) and alpha_equal(t, v)


def test_structural_is_object(samples):
    for t in samples:
        u, v = deepcopy(t), deepcopy(t)
        assert t == t and t == u and u == t
        assert u == v and t == v


def test_substitutive(samples):
    # Equal independently copied trees, observed by operations and name-reading functions.
    observations = (lambda t: t, repr, hash, type, lambda t: tuple(getattr(t, f.name) for f in fields(t)),
                    free_names, canonical, lambda t: swap("x", "y", t),
                    lambda t: substitute("x", Var("y"), t), lambda t: reduce((), 20, t))
    for t in samples:
        u = deepcopy(t)
        assert t == u
        for f in observations:
            assert f(t) == f(u)


def test_free_variables_are_names(rng):
    for x, y in [("x", "y"), ("x", "x"), *( (rng.choice(NAMES), rng.choice(NAMES)) for _ in range(CASES))]:
        assert alpha_equal(Var(x), Var(y)) == (x == y)


def test_rename_bound(samples, rng):
    failures = []
    for b in samples:
        x = rng.choice(NAMES)
        y = fresh_for(b)
        ty = term(rng, 4)
        for cls in BINDERS:
            if not alpha_equal(cls(x, ty, b), cls(y, ty, swap(x, y, b))):
                failures.append((cls, x, b))
        value = term(rng, 3)
        if not alpha_equal(Let(x, ty, value, b), Let(y, ty, value, swap(x, y, b))):
            failures.append((Let, x, b))
        scrutinee = term(rng, 3)
        if not alpha_equal(Match(scrutinee, ((PVar(x), b),)), Match(scrutinee, ((PVar(y), swap(x, y, b)),))):
            failures.append((Match, x, b))
    assert alpha_equal(Lam("x", Universe(), Lam("y", Universe(), Var("x"))),
                       Lam("y", Universe(), Lam("x", Universe(), Var("y"))))

    assert alpha_equal(Lam("x", Universe(), Data("x", ())), Lam("fresh", Universe(), Data("fresh", ())))
    assert not failures, failures

def test_alpha_keeps_head(samples):
    for t in samples:
        u = alpha_variant(t)
        assert alpha_equal(t, u)
        assert head(t) == head(u)
    assert head(Let("x", Universe(), Var("v"), Var("x"))) == "Let"


def test_alpha_keeps_free(samples):
    for t in samples:
        u = alpha_variant(t)
        assert alpha_equal(t, u)
        assert free_names(t) == free_names(u)


def test_alpha_congruent(samples, rng):
    for t in samples:
        s = term(rng, SIZE)
        u, v = alpha_variant(t), alpha_variant(s)
        for cls in (App, Pair):
            assert alpha_equal(cls(t, s), cls(u, v))
        for cls in BINDERS:
            assert alpha_equal(cls("x", t, s), cls("x", u, v))
        assert alpha_equal(Let("x", t, t, s), Let("x", u, u, v))
        assert alpha_equal(Inj("l", t), Inj("l", u))
        assert alpha_equal(Proj(t, "l"), Proj(u, "l"))
        for cls in (Sum, Record, RecordValue):
            assert alpha_equal(cls((("l", t),)), cls((("l", u),)))
        assert alpha_equal(Data("D", (("l", t),)), Data("D", (("l", u),)))
        assert alpha_equal(Match(t, ((PWild(), s),)), Match(u, ((PWild(), v),)))


def parts_agree(eq, s, t):
    if type(s) is not type(t):
        return False
    if isinstance(s, BINDERS):
        x, d, b = binder_parts(s)
        y, e, c = binder_parts(t)
        return eq(d, e) and ((x == y and eq(b, c)) or (x not in free_names(c) and eq(b, c if x == y else swap(y, x, c))))
    match s, t:
        case Let(x, d, v, b), Let(y, e, w, c):
            return eq(d, e) and eq(v, w) and ((x == y and eq(b, c)) or (x not in free_names(c) and eq(b, c if x == y else swap(y, x, c))))
        case (App(f, x), App(g, y)) | (Pair(f, x), Pair(g, y)):
            return eq(f, g) and eq(x, y)
        case (Inj(l, u), Inj(k, v)) | (Proj(u, l), Proj(v, k)):
            return l == k and eq(u, v)
        case (Sum(xs), Sum(ys)) | (Record(xs), Record(ys)) | (RecordValue(xs), RecordValue(ys)):
            return len(xs) == len(ys) and all(k == j and eq(u, v) for (k, u), (j, v) in zip(xs, ys))
        case Data(x, xs), Data(y, ys):
            def pairs_agree(ds):
                return len(xs) == len(ds) and all(k == j and eq(u, v) for (k, u), (j, v) in zip(xs, ds))
            return (x == y and pairs_agree(ys)) or (
                all(x not in free_names(v) for _, v in ys)
                and pairs_agree(tuple((k, v if x == y else swap(y, x, v)) for k, v in ys)))
        case Match(u, xs), Match(v, ys):
            if not eq(u, v) or len(xs) != len(ys):
                return False
            for (p, b), (q, c) in zip(xs, ys):
                if pattern_shape(p) != pattern_shape(q):
                    return False
                remaining = list(pattern_names(q))
                for x in pattern_names(p):
                    y = remaining.pop(0)
                    if x != y:
                        c = swap(y, x, c)
                        remaining = [x if n == y else y if n == x else n for n in remaining]
                if not eq(b, c):
                    return False
            return True
        case _:
            return s == t


def pattern_shape(p):
    match p:
        case PVar(): return PVar("_")
        case PPair(a, b): return PPair(pattern_shape(a), pattern_shape(b))
        case PInj(l, q): return PInj(l, pattern_shape(q))
        case PCon(c, ps): return PCon(c, tuple(map(pattern_shape, ps)))
        case _: return p


def linear_patterns(t):
    if isinstance(t, Match):
        if any(len(pattern_names(p)) != len(set(pattern_names(p))) for p, _ in t.arms):
            return False
    for field in fields(t):
        value = getattr(t, field.name)
        if type(value) in Term.__args__ and not linear_patterns(value):
            return False
        if isinstance(value, tuple):
            for entry in value:
                if isinstance(entry, tuple) and type(entry[-1]) in Term.__args__ and not linear_patterns(entry[-1]):
                    return False
    return True


def test_alpha_parts_agree(samples):
    for t in samples:
        if not linear_patterns(t):
            continue
        u = alpha_variant(t)
        assert alpha_equal(t, u)
        assert parts_agree(alpha_equal, t, u)
    for s, t in ((Lit(IntConst(1)), Lit(IntConst(2))), (Primitive("+"), Primitive("*")), (Inj("l", Universe()), Inj("r", Universe())), (App(Var("x"), Var("y")), App(Var("y"), Var("x")))):
        assert not alpha_equal(s, t)


def test_weak_alpha_fails_parts_agree():
    weak = lambda s, t: type(s) is type(t) and free_names(s) == free_names(t)
    s, t = Lit(IntConst(1)), Lit(IntConst(2))
    assert weak(s, t)
    assert not parts_agree(weak, s, t)


def test_alpha_parts_agree_permuted_pattern():
    s = Match(Var("v"), ((PPair(PVar("x"), PVar("y")), Var("x")),))
    t = Match(Var("v"), ((PPair(PVar("y"), PVar("x")), Var("y")),))
    assert alpha_equal(s, t)
    assert parts_agree(alpha_equal, s, t)


def test_subst_hits(samples, rng):
    for s in samples:
        x = rng.choice(NAMES)
        assert alpha_equal(substitute(x, s, Var(x)), s)


def test_subst_misses(samples, rng):
    for s in samples:
        x, y = rng.sample(NAMES, 2)
        assert alpha_equal(substitute(x, s, Var(y)), Var(y))
    assert substitute("x", Var("y"), Var("y")) == Var("y")


def test_subst_goes_inside(samples, rng):
    for f in samples:
        x, l = rng.choice(NAMES), rng.choice(LABELS)
        s, b = term(rng, SIZE), term(rng, SIZE)
        for cls in (App, Pair):
            assert alpha_equal(substitute(x, s, cls(f, b)), cls(substitute(x, s, f), substitute(x, s, b)))
        assert alpha_equal(substitute(x, s, Inj(l, f)), Inj(l, substitute(x, s, f)))
        assert alpha_equal(substitute(x, s, Proj(f, l)), Proj(substitute(x, s, f), l))
        for cls in (Sum, Record, RecordValue):
            assert alpha_equal(substitute(x, s, cls(((l, f),))), cls(((l, substitute(x, s, f)),)))
        assert alpha_equal(substitute(x, s, Match(f, ((PWild(), b),))), Match(substitute(x, s, f), ((PWild(), substitute(x, s, b)),)))


def test_subst_stops_at_shadow(samples, rng):
    for b in samples:
        x, s, ty = rng.choice(NAMES), term(rng, SIZE), term(rng, SIZE)
        for cls in BINDERS:
            assert alpha_equal(substitute(x, s, cls(x, ty, b)), cls(x, substitute(x, s, ty), b))
        assert alpha_equal(substitute(x, s, Let(x, ty, s, b)), Let(x, substitute(x, s, ty), substitute(x, s, s), b))
        assert alpha_equal(substitute(x, s, Match(ty, ((PVar(x), b),))), Match(substitute(x, s, ty), ((PVar(x), b),)))
    assert substitute("x", Var("y"), Lam("x", Var("x"), Var("x"))) == Lam("x", Var("y"), Var("x"))


def test_subst_passes_binder(samples, rng):
    for s in samples:
        y, x = fresh_for(s), rng.choice(NAMES)
        ty, b = term(rng, SIZE), term(rng, SIZE)
        for cls in BINDERS:
            assert x == y or alpha_equal(substitute(x, s, cls(y, ty, b)), cls(y, substitute(x, s, ty), substitute(x, s, b)))
        assert x == y or alpha_equal(substitute(x, s, Let(y, ty, ty, b)), Let(y, substitute(x, s, ty), substitute(x, s, ty), substitute(x, s, b)))


def test_subst_avoids_capture(samples, rng):
    cases = [("y", "z", Var("y"), Data("y", ()))]
    for source in samples:
        # Draw y from free names, as CaptureCase requires; no rejection sampling.
        names = sorted(free_names(source))
        if names:
            body = term(rng, SIZE)
            y = rng.choice(names)
            z = fresh_for(Pair(source, body))
            cases.append((y, z, source, body))
    failures = []
    for y, z, source, body in cases:
        assert y in free_names(source) and z not in free_names(source) | free_names(body) and y != z
        x = "x" if source == Var("y") and body == Data("y", ()) else rng.choice(NAMES)
        ty = term(rng, SIZE)
        if x != y and x != z:
            left = substitute(x, source, Lam(y, ty, body))
            right = Lam(z, substitute(x, source, ty), substitute(x, source, swap(y, z, body)))
            if not alpha_equal(left, right):
                failures.append((x, y, z, source, body, ty))
    assert not failures, failures


def test_subst_not_free(samples, rng):
    for t in samples:
        x = fresh_for(t)
        assert alpha_equal(substitute(x, term(rng, SIZE), t), t)


def test_subst_respects_alpha(samples, rng):
    for t in samples:
        x, s = rng.choice(NAMES), term(rng, SIZE)
        u = alpha_variant(t)
        assert alpha_equal(t, u)
        assert alpha_equal(substitute(x, s, t), substitute(x, s, u))


def test_canon_of_alpha(samples):
    for t in samples:
        assert canonical(t) == canonical(alpha_variant(t))


def test_canon_idempotent(samples):
    for t in samples:
        assert canonical(canonical(t)) == canonical(t)


def test_canon_of_name(rng):
    for x in (*NAMES, "a.", ".", "模块.名称", *(rng.choice(NAMES) for _ in range(CASES))):
        assert canonical(Var(x)) == Var(unqualify(x))


def test_unqualify_idempotent(rng):
    for x in (*NAMES, "a.", ".", "模块.名称", *(rng.choice(NAMES) for _ in range(CASES))):
        assert unqualify(unqualify(x)) == unqualify(x)
    assert unqualify("a.b.c") == "c"


def test_canon_keeps_term(samples):
    witnessed = 0
    for t in samples:
        if all(unqualify(x) == x for x in free_names(t)):
            witnessed += 1
            assert alpha_equal(canonical(t), t)
    assert witnessed > 0


def steps_to(result, target):
    return result is not None and alpha_equal(result, target)


def test_beta(samples, rng):
    for b in samples:
        x, arg = rng.choice(NAMES), term(rng, SIZE)
        assert steps_to(step(program(rng), App(Lam(x, Universe(), b), arg)), substitute(x, arg, b))


def test_delta(samples, rng):
    assert step((Define("f", Universe(), Var("f")),), Var("f")) == Var("f")
    assert step((Define("f", Universe(), Var("stuck")),), App(Var("f"), Var("a"))) == App(Var("stuck"), Var("a"))
    for b in samples:
        f = rng.choice(NAMES)
        definition = Define(f, Universe(), b)
        for p in ((definition,) + program(rng), (Declare(f, Universe()), definition), (Datum(b), Declare(f, Universe()), definition)):
            assert steps_to(step(p, Var(f)), b)


def test_zeta(samples, rng):
    for body in samples:
        x, ty, value = rng.choice(NAMES), term(rng, SIZE), term(rng, SIZE)
        assert steps_to(step(program(rng), Let(x, ty, value, body)), substitute(x, value, body))


def test_head_first(samples, rng):
    for b in samples:
        x, u, arg = rng.choice(NAMES), term(rng, SIZE), term(rng, SIZE)
        redex = App(Lam(x, Universe(), b), u)
        target = substitute(x, u, b)
        arms = ((PWild(), arg),)
        p = program(rng)
        assert steps_to(step(p, App(redex, arg)), App(target, arg))
        assert steps_to(step(p, Match(redex, arms)), Match(target, arms))
        assert steps_to(step(p, Proj(redex, "l")), Proj(target, "l"))


def test_holes_stay(samples, rng):
    for b in samples:
        f, arg, c = rng.choice(NAMES), term(rng, SIZE), term(rng, SIZE)
        p = (Declare(f, Universe()),)
        assert step(p, Var(f)) is None
        assert step(p, App(Var(f), arg)) is None
        assert step(p, Match(Var(f), ((PLit(constant(rng)), b), (PWild(), c)))) is None
        assert steps_to(step(p, Match(Var(f), ((PWild(), c),))), c)
        assert step((), Hole(f)) is None
        assert step((), Axiom(f)) is None


def test_iota(samples, rng):
    for v in samples:
        l, y, b, k = rng.choice(LABELS), rng.choice(NAMES), term(rng, SIZE), constant(rng)
        p = program(rng)
        assert steps_to(step(p, Match(Inj(l, v), ((PInj(l, PVar(y)), b),))), substitute(y, v, b))
        if not any(isinstance(a, (Declare, Define)) and a.name == l for a in p):
            assert steps_to(step(p, Match(App(Var(l), v), ((PCon(l, (PVar(y),)), b),))), substitute(y, v, b))
        for pat, target in ((PLit(k), b), (PVar(y), substitute(y, Lit(k), b)), (PWild(), b)):
            assert steps_to(step(p, Match(Lit(k), ((pat, b),))), target)


def test_iota_pair(samples, rng):
    for s in samples:
        z, y, b = fresh_for(s), rng.choice(NAMES), term(rng, SIZE)
        p = program(rng)
        if y != z:
            assert steps_to(step(p, Match(Pair(s, Var(y)), ((PPair(PVar(y), PVar(z)), b),))), substitute(z, Var(y), substitute(y, s, b)))
            assert steps_to(step(p, Match(Pair(Var(z), s), ((PPair(PVar(z), PVar(y)), b),))), substitute(z, Var(z), substitute(y, s, b)))


def test_iota_skips(samples, rng):
    for v in samples:
        b, c = term(rng, SIZE), term(rng, SIZE)
        assert steps_to(step(program(rng), Match(Inj("left", v), ((PInj("right", PWild()), b), (PInj("left", PVar("x")), c)))), substitute("x", v, c))


def constructor_data():
    return Define("T", Universe(), Data("T", (
        ("c", Var("T")), ("k", Var("T")),
        ("f", Pi("_", Var("T"), Var("T"))),
        ("g", Pi("_", Var("T"), Var("T"))),
    )))


def test_iota_constructors(samples, rng):
    # 66d5cae term.lth IotaConstructors: withData and all four conjuncts.
    for v in samples:
        p = (constructor_data(),) + program(rng)
        b, d = term(rng, SIZE), term(rng, SIZE)
        assert steps_to(step(p, Match(Var("c"), ((PCon("c", ()), b),))), b)
        assert steps_to(step(p, Match(Var("c"), ((PCon("k", ()), b), (PCon("c", ()), d)))), d)
        assert steps_to(step(p, Match(Var("k"), ((PCon("c", ()), b), (PWild(), d)))), d)
        assert steps_to(step(p, Match(App(Var("f"), v), (
            (PCon("g", (PVar("y"),)), b), (PCon("f", (PVar("y"),)), d),
        ))), substitute("y", v, d))


def test_constructor_act_names_and_unknown_names():
    data = constructor_data()
    arms = ((PCon("k", ()), Var("wrong")), (PCon("c", ()), Var("hit")), (PWild(), Var("fallback")))
    for p in ((data, Declare("c", Universe())), (Declare("c", Universe()), data)):
        assert step(p, Match(Var("c"), arms)) is None
        assert step(p, Match(Var("c"), ((PCon("c", ()), Var("hit")),))) is None
        assert step(p, Match(App(Var("c"), Universe()), ((PCon("c", (PWild(),)), Var("hit")),))) is None
    p = (data, Define("c", Universe(), Var("k")))
    assert step(p, Match(Var("c"), arms)) == Match(Var("k"), arms)
    assert step((data,), Match(Var("unknown"), arms)) is None
    assert step((), Match(Var("c"), arms)) is None
    other = Define("U", Universe(), Data("U", (("u", Var("U")),)))
    assert step((data, other), Match(Var("u"), arms)) is None


def test_proj_of_record(samples, rng):
    for u in samples:
        v, p = term(rng, SIZE), program(rng)
        r = RecordValue((("x", u), ("y", v)))
        assert steps_to(step(p, Proj(r, "x")), u)
        assert steps_to(step(p, Proj(r, "y")), v)


def prim(op, a, b, head=Primitive):
    return App(App(head(op), Lit(IntConst(a))), Lit(IntConst(b)))


def test_prim(rng):
    for _ in range(CASES):
        i, j = rng.randint(-20, 20), rng.randint(-20, 20)
        p = program(rng)
        for op, result in (("+", Lit(IntConst(i+j))), ("*", Lit(IntConst(i*j))), ("-", Lit(IntConst(i-j))), ("<", Var("true" if i<j else "false")), ("==", Var("true" if i==j else "false"))):
            assert steps_to(step(p, prim(op, i, j)), result)
        u, v = rng.choice((-2.5, 0., 1.25)), rng.choice((-2.5, 0., 1.25))
        assert steps_to(step(p, App(App(Primitive("+"), Lit(FloatConst(u))), Lit(FloatConst(v)))), Lit(FloatConst(u+v)))
        a, b = rng.choice(("", "text", "中文")), rng.choice(("", "text", "中文"))
        assert steps_to(step(p, App(App(Primitive("=="), Lit(StringConst(a))), Lit(StringConst(b)))), Var("true" if a == b else "false"))
    assert step((), prim("+", 1, 2, Var)) is None
    assert step((Declare("+", Universe()),), prim("+", 1, 2, Var)) is None
    assert step((Define("+", Universe(), Primitive("+")),), prim("+", 1, 2, Var)) == prim("+", 1, 2)



# 051e6aa term.lth §5: PrimStructural, PrimConstructors, EqualityStuck; prompt-7.md.
def eq(a, b):
    return App(App(Primitive("=="), a), b)


def num(i):
    return Lit(IntConst(i))


def truth(b):
    return Var("true" if b else "false")


def test_prim_structural(rng):
    # PrimStructural: each conjunct, over random integers, labels and programs.
    for _ in range(CASES):
        i, j = rng.randint(-3, 3), rng.randint(-3, 3)
        x, y, p = rng.choice(LABELS), rng.choice(LABELS), program(rng)
        assert steps_to(step(p, eq(Pair(num(i), num(j)), Pair(num(i), num(j)))), truth(True))
        assert steps_to(step(p, eq(Pair(num(i), num(j)), Pair(num(j), num(i)))), truth(i == j))
        assert steps_to(step(p, eq(RecordValue(((x, num(i)),)), RecordValue(((x, num(j)),)))), truth(i == j))
        assert steps_to(step(p, eq(Inj(x, num(i)), Inj(y, num(i)))), truth(x == y))
        assert steps_to(step(p, eq(Lit(FloatConst(1.5)), Lit(FloatConst(1.5)))), truth(True))


def test_prim_constructors(rng):
    # PrimConstructors: the data of IotaConstructors added to a program that leaves its names free.
    names = ("T", "c", "k", "f", "g")
    for _ in range(CASES):
        i, j = rng.randint(-3, 3), rng.randint(-3, 3)
        rest = program(rng)
        if any(isinstance(a, (Declare, Define)) and a.name in names for a in rest):
            continue
        p = (constructor_data(),) + rest
        assert steps_to(step(p, eq(Var("c"), Var("c"))), truth(True))
        assert steps_to(step(p, eq(Var("c"), Var("k"))), truth(False))
        assert steps_to(step(p, eq(App(Var("f"), num(i)), App(Var("f"), num(j)))), truth(i == j))
        assert steps_to(step(p, eq(App(Var("f"), num(i)), App(Var("g"), num(i)))), truth(False))


def test_equality_stuck(samples, rng):
    # EqualityStuck: two lambdas, two externs, a declared name against a literal, a pair with a hole.
    for b in samples:
        x, f, ty, i = rng.choice(NAMES), rng.choice(NAMES), term(rng, SIZE), rng.randint(-3, 3)
        assert step((), eq(Lam(x, ty, b), Lam(x, ty, b))) is None
        assert step((), eq(Extern(f), Extern(f))) is None
        assert step((Declare(f, ty),), eq(Var(f), num(i))) is None
        assert step((Declare(f, ty),), eq(Pair(Var(f), num(i)), Pair(num(i), num(i)))) is None


def list_data():
    # core's List as a data of the program: cons and nil, the same rule as any constructor
    return Define("List", Universe(), Data("List", (
        ("nil", Var("List")), ("cons", Pi("_", Var("Int"), Pi("_", Var("List"), Var("List")))),
    )))


def bool_data():
    return Define("Bool", Universe(), Data("Bool", (("true", Var("Bool")), ("false", Var("Bool")))))


def lst(*xs):
    result = Var("nil")
    for x in reversed(xs):
        result = App(App(Var("cons"), x), result)
    return result


def test_equality_nested_values_lists_and_records():
    p = (list_data(), bool_data(), constructor_data())
    one, two = num(1), num(2)
    nested = Pair(RecordValue((("a", lst(one, two)), ("b", Inj("l", App(Var("f"), Var("c")))))), Var("true"))
    assert step(p, eq(nested, nested)) == truth(True)
    other = Pair(RecordValue((("a", lst(one, two)), ("b", Inj("l", App(Var("f"), Var("k")))))), Var("true"))
    assert step(p, eq(nested, other)) == truth(False)
    assert step(p, eq(lst(one, two), lst(one, two))) == truth(True)
    assert step(p, eq(lst(one, two), lst(two, one))) == truth(False)
    assert step(p, eq(lst(one), lst(one, two))) == truth(False)
    assert step(p, eq(lst(), lst())) == truth(True)
    # records compare by field, whatever the order of the fields
    r = RecordValue((("a", one), ("b", two)))
    assert step(p, eq(r, RecordValue((("b", two), ("a", one))))) == truth(True)
    assert step(p, eq(r, RecordValue((("b", one), ("a", one))))) == truth(False)
    # a differing label decides, whatever the parts under it
    assert step(p, eq(Inj("l", one), Inj("r", Lit(StringConst("x"))))) == truth(False)
    assert step(p, eq(Lit(FloatConst(1.5)), Lit(FloatConst(2.5)))) == truth(False)
    assert step(p, eq(Lit(StringConst("a")), Lit(StringConst("a")))) == truth(True)


def test_equality_steps_operands_then_compares():
    p = (Define("x", Universe(), Pair(num(1), num(2))), Define("==", Universe(), Primitive("==")))
    assert step(p, eq(Var("x"), Pair(num(1), num(2)))) == eq(Pair(num(1), num(2)), Pair(num(1), num(2)))
    assert step(p, eq(Pair(num(1), num(2)), Var("x"))) == eq(Pair(num(1), num(2)), Pair(num(1), num(2)))
    assert reduce(p, 10, App(App(Var("=="), Var("x")), Var("x"))) == truth(True)


def test_equality_stuck_conservative_readings():
    # Where term.lth is silent the step is withheld (opus-7.md): a part not yet a value, an
    # undeclared name, a partial constructor, different types, different record labels.
    p = (list_data(), bool_data(), constructor_data(), Define("y", Universe(), num(1)))
    one = num(1)
    assert step(p, eq(Var("free"), Var("free"))) is None
    assert step(p, eq(Var("f"), Var("f"))) is None
    assert step(p, eq(App(App(Var("f"), one), one), App(App(Var("f"), one), one))) is None
    assert step(p, eq(one, Lit(FloatConst(1.0)))) is None
    assert step(p, eq(Pair(one, one), Inj("l", one))) is None
    assert step(p, eq(Var("c"), Var("true"))) is None
    assert step(p, eq(RecordValue((("a", one),)), RecordValue((("b", one),)))) is None
    assert step(p, eq(RecordValue((("a", one), ("a", one))), RecordValue((("a", one), ("a", one))))) is None
    assert step(p, eq(Hole("h"), Hole("h"))) is None
    assert step(p, eq(Universe(), Universe())) is None
    # a constructor the program declares or defines is a name, not a constructor
    assert step(p + (Declare("c", Universe()),), eq(Var("c"), Var("c"))) is None
    assert step((), eq(lst(one), lst(one))) is None

def plus(i, j):
    return App(App(Primitive("+"), num(i)), num(j))


def test_equality_demands_parts():
    # EqualityDemandsParts (term.lth 924df6b): each case, then the order, then it ends in a value.
    p = (Define("y", Universe(), num(1)), list_data(), bool_data(), constructor_data())
    assert step(p, eq(Pair(plus(1, 1), num(1)), Pair(num(2), num(1)))) == eq(Pair(num(2), num(1)), Pair(num(2), num(1)))
    assert step(p, eq(Pair(num(1), num(1)), Pair(num(1), plus(1, 1)))) == eq(Pair(num(1), num(1)), Pair(num(1), num(2)))
    assert step(p, eq(num(1), App(Lam("x", Universe(), Var("x")), num(1)))) == eq(num(1), num(1))
    assert step(p, eq(num(1), Var("y"))) == eq(num(1), num(1))
    r = lambda a, b: RecordValue((("a", a), ("b", b)))
    assert step(p, eq(r(num(1), plus(1, 1)), r(num(1), num(2)))) == eq(r(num(1), num(2)), r(num(1), num(2)))
    assert step(p, eq(r(num(1), num(2)), r(num(1), plus(1, 1)))) == eq(r(num(1), num(2)), r(num(1), num(2)))
    assert step(p, eq(Pair(Var("y"), num(1)), Pair(num(1), num(1)))) == eq(Pair(num(1), num(1)), Pair(num(1), num(1)))
    # leftmost first: the left pair's first part, its second, the right operand
    assert step(p, eq(Pair(plus(1, 1), plus(2, 2)), Pair(plus(3, 3), num(0)))) == eq(Pair(num(2), plus(2, 2)), Pair(plus(3, 3), num(0)))
    assert step(p, eq(Pair(num(2), plus(2, 2)), Pair(plus(3, 3), num(0)))) == eq(Pair(num(2), num(4)), Pair(plus(3, 3), num(0)))
    assert step(p, eq(Pair(num(2), num(4)), Pair(plus(3, 3), plus(0, 0)))) == eq(Pair(num(2), num(4)), Pair(num(6), plus(0, 0)))
    assert step(p, eq(r(plus(1, 1), plus(2, 2)), r(plus(3, 3), num(0)))) == eq(r(num(2), plus(2, 2)), r(plus(3, 3), num(0)))
    # a stuck part is passed over: a later part still steps; the whole stays stuck once none does
    stuck = Pair(Hole("h"), plus(1, 1))
    assert step(p, eq(stuck, stuck)) == eq(Pair(Hole("h"), num(2)), stuck)
    assert step(p, eq(Pair(Hole("h"), num(2)), Pair(Hole("h"), num(2)))) is None
    assert step(p, eq(Pair(Lam("x", Universe(), Var("x")), num(1)), Pair(Lam("x", Universe(), Var("x")), num(1)))) is None
    assert reduce(p, 20, eq(Pair(plus(1, 1), Var("y")), Pair(num(2), plus(0, 1)))) == truth(True)
    assert reduce(p, 20, eq(Pair(plus(1, 1), Var("y")), Pair(num(2), plus(0, 2)))) == truth(False)


def test_agreement_comparison_steps():
    # world.lth §5 agreement: `d.describe before == (after, x)`, describe returning a pair of redexes
    describe = Lam("s", Universe(), Pair(App(App(Primitive("+"), Var("s")), num(1)), App(App(Primitive("*"), Var("s")), num(2))))
    for after, x, want in ((4, 6, True), (4, 7, False)):
        t = eq(App(describe, num(3)), Pair(num(after), num(x)))
        assert reduce((), 20, t) == truth(want)


def test_extern_is_value(rng):
    for _ in range(CASES):
        assert step(program(rng), Extern(rng.choice(NAMES))) is None


def test_values_stay(samples, rng):
    for b in samples:
        x, c, ty, p = rng.choice(NAMES), constant(rng), term(rng, SIZE), program(rng)
        kvs = (("C", b),)
        for v in (Lam(x, ty, b), Lit(c), Universe(), World(), Pi(x, ty, b), Sigma(x, ty, b), Sum(kvs), Data(x, kvs), Subtype(x, ty, b), Record(kvs), RecordValue(kvs), Pair(ty, b), Inj(x, b), Primitive(x)):
            assert step(p, v) is None


def test_datum_is_inert(samples, rng):
    for t in samples:
        p, d = program(rng), term(rng, SIZE)
        assert step((Datum(d),) + p, t) == step(p, t)


# Additional observations catch vacuous agree-only implementations and scope mistakes.
def test_data_are_frozen_and_cover_every_constructor():
    all_classes = (*Constant.__args__, *Pattern.__args__, *Term.__args__, *Act.__args__)
    for cls in all_classes:
        assert is_dataclass(cls) and cls.__dataclass_params__.frozen
    with pytest.raises(FrozenInstanceError):
        Var("x").name = "y"


def test_generator_budget_and_constructor_coverage(rng):
    def nodes(t):
        if isinstance(t, BINDERS):
            _, a, b = binder_parts(t)
            return 1 + nodes(a) + nodes(b)
        match t:
            case Let(_, a, v, b):
                return 1 + nodes(a) + nodes(v) + nodes(b)
            case App(a, b) | Pair(a, b):
                return 1 + nodes(a) + nodes(b)
            case Inj(_, a) | Proj(a, _):
                return 1 + nodes(a)
            case Match(a, arms):
                return 1 + nodes(a) + sum(nodes(b) for _, b in arms)
            case Sum(kvs) | Data(_, kvs) | Record(kvs) | RecordValue(kvs):
                return 1 + sum(nodes(b) for _, b in kvs)
            case _:
                return 0
    seen = set()
    for _ in range(1000):
        t = term(rng, SIZE)
        seen.add(type(t))
        assert nodes(t) <= SIZE
        assert type(term(rng, 0)) in (Var, Lit, Universe, World, Extern, Primitive, Axiom, Hole)
    assert seen == set(Term.__args__)
    a, b = random.Random(SEED), random.Random(SEED)
    assert [term(a, SIZE) for _ in range(CASES)] == [term(b, SIZE) for _ in range(CASES)]


def test_binding_scopes_and_negative_alpha_cases():
    assert free_names(Lam("x", Var("x"), Var("x"))) == {"x"}
    assert free_names(Data("D", (("C", App(Var("D"), Var("x"))),))) == {"x"}
    assert free_names(Match(Var("v"), ((PVar("x"), App(Var("x"), Hole("h"))),))) == {"v"}
    assert not alpha_equal(Lam("x", Universe(), Var("y")), Lam("y", Universe(), Var("y")))
    assert not alpha_equal(Lam("x", Universe(), Lam("x", Universe(), Var("x"))),
                           Lam("a", Universe(), Lam("b", Universe(), Var("a"))))
    assert not alpha_equal(Match(Var("v"), ((PPair(PVar("x"), PVar("x")), Var("x")),)),
                           Match(Var("v"), ((PPair(PVar("y"), PVar("z")), Var("y")),)))
    assert not alpha_equal(Lit(IntConst(1)), Lit(FloatConst(1.0)))


def test_capture_avoidance_in_every_binding_form():
    # Non-vacuous CaptureCase with z fresh only in free names (it is bound in b).
    b = Pair(Var("x"), Lam("z", Universe(), Var("y")))
    assert alpha_equal(substitute("x", Var("y"), Lam("y", Var("x"), b)),
                       Lam("z", Var("y"), substitute("x", Var("y"), swap("y", "z", b))))
    for cls in BINDERS:
        result = substitute("x", Var("y"), cls("y", Universe(), Pair(Var("x"), Var("y"))))
        assert result == cls("y'", Universe(), Pair(Var("y"), Var("y'")))
        assert free_names(result) == {"y"}
    assert substitute("x", Var("D"), Data("D", (("C", Pair(Var("x"), Var("D"))),))) == Data("D'", (("C", Pair(Var("D"), Var("D'"))),))
    t = Match(Var("v"), ((PPair(PVar("y"), PVar("y'")), Pair(Var("x"), Var("y"))),))
    expected = Match(Var("v"), ((PPair(PVar("y''"), PVar("y'")), Pair(Var("y"), Var("y''"))),))
    assert substitute("x", Var("y"), t) == expected
    # Nested shadowed names and annotations cannot become the fresh target accidentally.
    t = Lam("y", Universe(), Pair(Var("x"), Lam("y'", Universe(), Var("y"))))
    assert substitute("x", Var("y"), t) == Lam("y''", Universe(), Pair(Var("y"), Lam("y'", Universe(), Var("y''"))))


def test_canonical_order_capture_and_literal_tags():
    t = Lam("a", Lam("b", Universe(), Var("b")), Pair(Var("a"), Var("x0")))
    assert canonical(t) == Lam("x1", Lam("x2", Universe(), Var("x2")), Pair(Var("x1"), Var("x0")))
    assert canonical(Lam("a", Universe(), Pair(Var("a"), Var("m.x0")))) == Lam("x1", Universe(), Pair(Var("x1"), Var("x0")))
    assert canonical(Inj("m.tag", Var("m.x"))) == Inj("m.tag", Var("x"))
    for t in (Hole("m.h"), Extern("m.host"), Primitive("m.op")):
        assert canonical(t) == t


def test_pattern_priority_nested_demand_and_nonlinearity():
    p = (Define("n", Universe(), Lit(IntConst(2))),)
    arms = ((PLit(IntConst(2)), Var("first")), (PWild(), Var("last")))
    assert reduce(p, 4, Match(Var("n"), arms)) == Var("first")
    nested = PCon("C", (PPair(PLit(IntConst(2)), PVar("x")),))
    value = App(Var("C"), Pair(Var("n"), Lit(IntConst(3))))
    assert reduce(p, 4, Match(value, ((nested, Var("x")),))) == Lit(IntConst(3))
    nonlinear = ((PPair(PVar("x"), PVar("x")), Var("same")), (PWild(), Var("different")))
    assert reduce((), 2, Match(Pair(Var("a"), Var("a")), nonlinear)) == Var("same")
    assert reduce((), 2, Match(Pair(Var("a"), Var("b")), nonlinear)) == Var("different")


def test_fuel_exhaustion_and_long_reductions():
    assert reduce((), 0, Universe()) is None
    assert reduce((), 1, Universe()) == Universe()
    beta = App(Lam("x", Universe(), Var("x")), Universe())
    assert reduce((), 1, beta) is None
    assert reduce((), 2, beta) == Universe()
    p = tuple(Define(f"f{i}", Universe(), Var(f"f{i+1}")) for i in range(3000))
    assert reduce(p, 3000, Var("f0")) is None
    assert reduce(p, 3001, Var("f0")) == Var("f3000")
    assert reduce((Define("loop", Universe(), Var("loop")),), 10000, Var("loop")) is None
    omega_lam = Lam("x", Universe(), App(Var("x"), Var("x")))
    assert reduce((), 2000, App(omega_lam, omega_lam)) is None
    t = Var("head")
    for _ in range(2500):
        t = App(t, Universe())
    v = reduce((), 1, t)
    assert v is not None and alpha_equal(v, t)
    for n in (-1, True, 1.5):
        with pytest.raises(ValueError, match="non-negative integer"):
            reduce((), n, Universe())


def test_deep_beta_substitution_and_pattern_demands():
    body = Var("head")
    expected = Var("head")
    for _ in range(1500):
        body = App(body, Var("x"))
        expected = App(expected, Var("a"))
    result = reduce((), 2, App(Lam("x", Universe(), body), Var("a")))
    assert result is not None and alpha_equal(result, expected)
    assert alpha_equal(canonical(result), expected)
    assert alpha_equal(swap("a", "b", result), substitute("a", Var("b"), expected))
    p = PLit(IntConst(2))
    v = Var("n")
    for _ in range(1500):
        p = PInj("tag", p)
        v = Inj("tag", v)
    program = (Define("n", Universe(), Lit(IntConst(2))),)
    assert reduce(program, 3, Match(v, ((p, Var("hit")),))) == Var("hit")


def test_record_labels_and_traversal():
    for cls in (Record, RecordValue):
        t = cls((("m.x", Lam("y", Universe(), Pair(Var("x"), Var("y")))),))
        assert free_names(t) == {"x"}
        assert alpha_equal(t, alpha_variant(t))
        assert not alpha_equal(t, cls((("x", t.fields[0][1]),)))
        assert swap("x", "z", t).fields[0][0] == "m.x"
        u = substitute("x", Var("y"), t)
        assert u == cls((("m.x", Lam("y'", Universe(), Pair(Var("y"), Var("y'")))),))
        assert canonical(t) == cls((("m.x", Lam("x0", Universe(), Pair(Var("x"), Var("x0")))),))
        proj = Proj(t, "m.x")
        assert free_names(proj) == {"x"}
        assert alpha_equal(proj, Proj(alpha_variant(t), "m.x"))
        assert not alpha_equal(proj, Proj(t, "x"))
        assert substitute("x", Var("y"), proj) == Proj(u, "m.x")
        assert canonical(proj) == Proj(canonical(t), "m.x")
        assert swap("x", "z", proj) == Proj(swap("x", "z", t), "m.x")


def test_let_scope_traversal_and_capture():
    t = Let("x", Var("x"), Var("x"), Pair(Var("x"), Var("y")))
    assert free_names(t) == {"x", "y"}
    assert swap("x", "z", t) == Let("z", Var("z"), Var("z"), Pair(Var("z"), Var("y")))
    assert canonical(t) == Let("x0", Var("x"), Var("x"), Pair(Var("x0"), Var("y")))
    assert not alpha_equal(t, Let("z", Var("z"), Var("x"), Pair(Var("z"), Var("y"))))
    assert not alpha_equal(t, Let("z", Var("x"), Var("z"), Pair(Var("z"), Var("y"))))
    assert substitute("x", Var("y"), Let("y", Var("x"), Var("x"), Pair(Var("x"), Var("y")))) == Let("y'", Var("y"), Var("y"), Pair(Var("y"), Var("y'")))
    assert step((), Let("x", Hole("ty"), Var("loop"), Universe())) == Universe()


def test_unqualify_removes():
    assert unqualify("m.f") == "f"
    assert unqualify("a.b.c") == "c"
    assert unqualify("f") == "f"


def test_axiom_text_stays_literal():
    for text in ("", "x", "m.f", "axiom 中文"):
        t = Axiom(text)
        assert free_names(t) == set()
        assert head(t) == "Axiom"
        assert swap("x", "y", t) == t
        assert substitute("x", Var("y"), t) == t
        assert canonical(t) == t
        assert step((), t) is None
        assert reduce((), 1, t) == t
        assert alpha_equal(t, Axiom(text))
        assert not alpha_equal(t, Axiom(text + "!"))


def test_eval_computes(rng):
    cases = [(0, 0, ""), (-10**40, 10**40 + 1, "+")]
    cases += [(rng.randint(-10**20, 10**20), rng.randint(-10**20, 10**20), rng.choice(NAMES)) for _ in range(CASES)]
    for i, j, x in cases:
        value = Lit(IntConst(i))
        assert eval_at(int, App(App(Var("+"), value), Lit(IntConst(j)))) == i + j
        assert eval_at(int, App(Lam(x, Var("Int"), Var(x)), value)) == i
        assert eval_at(int, Let(x, Var("Int"), value, Var(x))) == i


def test_eval_constants_and_checks(rng):
    for _ in range(CASES):
        i, s = rng.randint(-10**20, 10**20), rng.choice(("", "text", "中文"))
        assert eval_at(int, Lit(IntConst(i))) == i
        assert eval_at(str, Lit(StringConst(s))) == s
        assert eval_at(int, Lit(StringConst(s))) is None
    assert eval_at(int, App(App(Var("+"), Lit(IntConst(1))), Lit(IntConst(2)))) == 3
    assert eval_at(int, Axiom("unproved")) is None
    assert eval_at(int, Lit(IntConst(1)), fuel=0) is None
    assert eval_at(int, Lit(FloatConst(1.0))) is None
