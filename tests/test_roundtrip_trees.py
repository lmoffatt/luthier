"""Direct WrittenProgram census: grammar.lth wf*, generator v2, seeds 0..999, sizes 0..6."""

from dataclasses import fields, is_dataclass, replace
import math
import random

import pytest

from luthier.ebnf import lits_of_names, luthier_syntax
from luthier.parse import lex, parse, print_program
from luthier import surface as s

NAMES = ("a", "b", "x", "y", "f", "T", "m.f")
G = luthier_syntax()
BINARY = tuple(lits_of_names(G, ["ampTerm", "arrowTerm", "orTerm", "andTerm",
                                 "cmpTerm", "addTerm", "mulTerm"]))
BOUND = tuple(lits_of_names(G, ["opSymbol"]))
SEEDS = range(1000)
SIZES = range(7)


def is_name(text):
    result = lex(text)
    return isinstance(result, s.Lexed) and len(result.tokens) == 1 and (
        result.tokens[0].kind == "name" and result.tokens[0].text == text
    )


def wf(node):
    """Literal transcription of wfPattern, wf, wfBody, wfAct and their helpers.

    Literal fields first satisfy their declared Nat/NonNegativeFloat domains;
    no parser/printer success or checker verdict is part of this predicate.
    """
    match node:
        case s.IntLit(value):
            return type(value) is int and value >= 0
        case s.FloatLit(value):
            return type(value) is float and math.isfinite(value) and value >= 0.0
        case s.StringLit() | s.PWild() | s.Universe() | s.World():
            return True
        case s.Name(name) | s.PlainParam(name):
            return is_name(name)
        case s.Literal(literal) | s.PLit(literal):
            return wf(literal)
        case s.PApp(name, patterns):
            return is_name(name) and all(map(wf, patterns))
        case s.PTuple(patterns) | s.ShapeParam(patterns):
            return len(patterns) >= 2 and all(map(wf, patterns))
        case s.Tuple(values):
            return len(values) >= 2 and all(map(wf, values))
        case s.Binop(operator, left, right):
            return operator in BINARY and wf(left) and wf(right)
        case s.OperatorAct(operator, value):
            return operator in BOUND and wf(value)
        case s.Pi(names, domain, codomain) | s.Sigma(names, domain, codomain):
            return bool(names) and all(map(is_name, names)) and wf(domain) and wf(codomain)
        case s.Field(names, typ) | s.TypedParam(names, typ) | s.Implicit(names, typ):
            return bool(names) and all(map(is_name, names)) and wf(typ)
        case s.Explicit(names, typ, default):
            return bool(names) and all(map(is_name, names)) and wf(typ) and maybe_wf(default)
        case s.Record(fs, law):
            return bool(fs) and all(map(wf, fs)) and maybe_wf(law) and (
                sum(len(f.names) for f in fs) >= 2 or law is None
            )
        case s.Subtype(pattern, typ, law):
            pattern_ok = (is_name(pattern.name) and not pattern.patterns
                          if isinstance(pattern, s.PApp) else wf(pattern))
            return pattern_ok and wf(typ) and wf(law)
        case s.RecordValue(pairs):
            return bool(pairs) and all(is_name(k) and wf(v) for k, v in pairs)
        case s.Sum(pairs):
            return len(pairs) >= 2 and all(is_name(k) and wf(v) for k, v in pairs)
        case s.DataBody(pairs):
            return all(is_name(k) and wf(v) for k, v in pairs)
        case s.Lambda(params, items, body):
            return bool(params) and all(map(wf, params)) and all(map(wf, items)) and wf(body)
        case s.Clause(patterns, body):
            return bool(patterns) and all(map(wf, patterns)) and wf(body)
        case s.ClausesBody(clauses):
            return bool(clauses) and all(map(wf, clauses))
        case s.ImportAct(_, names):
            return bool(names) and all(map(wf, names))
        case s.ImportName(name, theory, alias):
            return is_name(name) and maybe_name(theory) and maybe_name(alias)
        case s.Declare(name, binders, typ):
            return is_name(name) and all(map(wf, binders)) and wf(typ)
        case s.Define(name, binders, typ, body):
            return is_name(name) and all(map(wf, binders)) and maybe_wf(typ) and wf(body)
        case s.Alias(name, binders, value):
            return is_name(name) and all(map(wf, binders)) and wf(value)
        case s.SigmaNamed(x, a, y, b):
            return is_name(x) and is_name(y) and wf(a) and wf(b)
        case s.NamedArg(name, value) | s.Bind(name, value):
            return is_name(name) and wf(value)
        case s.Rebind(pattern, value):
            return wf(pattern) and wf(value)
        case s.Proj(value, field):
            return wf(value) and is_name(field)
        case s.App(f, a):
            return wf(f) and wf(a)
        case s.Neg(value) | s.Quoted(value) | s.TermBody(value) | s.Datum(value):
            return wf(value)
        case s.List(values):
            return all(map(wf, values))
        case s.Block(items, value):
            return all(map(wf, items)) and wf(value)
        case s.MatchOf(value, arms):
            return wf(value) and all(wf(p) and wf(t) for p, t in arms)
        case s.IfThen(c, a, b):
            return wf(c) and wf(a) and maybe_wf(b)
        case _:
            raise TypeError(node)


def maybe_wf(value):
    return value is None or wf(value)


def maybe_name(value):
    return value is None or is_name(value)


def wf_program(program):
    return all(isinstance(act, s.SurfaceAct.__args__) and wf(act) for act in program)


def split_budget(rng, budget, count):
    """Distribute exactly budget among recursive arguments, including zero shares."""
    if not count:
        return []
    cuts = sorted(rng.randrange(budget + 1) for _ in range(count - 1))
    bounds = [0, *cuts, budget]
    shares = [b - a for a, b in zip(bounds, bounds[1:])]
    rng.shuffle(shares)
    return shares


class Trees:
    """Construct wf trees directly; only recursive constructors spend one depth unit."""

    def __init__(self, seed):
        self.rng = random.Random(seed)

    def name(self):
        return self.rng.choice(NAMES)

    def names(self):
        return tuple(self.name() for _ in range(self.rng.randint(1, 2)))

    def literal(self):
        return self.rng.choice((s.IntLit(0), s.IntLit(1), s.IntLit(2),
                               s.FloatLit(0.5), s.FloatLit(1.5), s.FloatLit(-0.0),
                               s.StringLit(''), s.StringLit('a"\\\nb')))

    def children(self, size, categories):
        return [self.node(kind, share) for kind, share in
                zip(categories, self.child_budgets(size, categories))]

    def child_budgets(self, size, categories):
        minima = [int(kind in {'item', 'binder'}) for kind in categories]
        remaining = size - 1 - sum(minima)
        assert remaining >= 0
        return [a + b for a, b in zip(minima, split_budget(self.rng, remaining, len(categories)))]

    def node(self, kind, size):
        rng = self.rng
        if kind == 'surface':
            leaf = lambda: rng.choice((s.Name(self.name()), s.Literal(self.literal()),
                                       s.Universe(), s.World()))
            choices = [leaf]
            if size:
                def pair(cls):
                    return cls(*self.children(size, ['surface', 'surface']))

                def sequence(cls, minimum):
                    return cls(tuple(self.children(size, ['surface'] * rng.randint(minimum, minimum + 1))))

                def named_pair(cls):
                    a, b = self.children(size, ['surface', 'surface'])
                    return cls(self.name(), a, self.name(), b)

                def record():
                    count = rng.randint(1, 2)
                    has_law = bool(rng.randrange(2))
                    names = [self.names() for _ in range(count)]
                    if has_law and sum(map(len, names)) < 2:
                        names[0] += (self.name(),)
                    values = self.children(size, ['surface'] * (count + has_law))
                    return s.Record(tuple(s.Field(n, v) for n, v in zip(names, values)),
                                    values[-1] if has_law else None)

                def subtype():
                    p, a, law = self.children(size, ['subpattern', 'surface', 'surface'])
                    return s.Subtype(p, a, law)

                def pairs(cls, minimum=1):
                    values = self.children(size, ['surface'] * rng.randint(minimum, 2))
                    return cls(tuple((self.name(), value) for value in values))

                def block():
                    count = rng.randint(0, min(2, size - 1))
                    values = self.children(size, ['item'] * count + ['surface'])
                    return s.Block(tuple(values[:-1]), values[-1])

                def lambda_():
                    params, items = rng.randint(1, 2), rng.randint(0, min(2, size - 1))
                    values = self.children(size, ['param'] * params + ['item'] * items + ['surface'])
                    return s.Lambda(tuple(values[:params]), tuple(values[params:-1]), values[-1])

                def match():
                    count = rng.randint(0, 2)
                    values = self.children(size, ['surface'] + ['pattern', 'surface'] * count)
                    return s.MatchOf(values[0], tuple(zip(values[1::2], values[2::2])))

                def if_():
                    values = self.children(size, ['surface'] * rng.randint(2, 3))
                    return s.IfThen(*values[:2], values[2] if len(values) == 3 else None)

                choices += [lambda: pair(s.App),
                            lambda: s.Binop(rng.choice(BINARY), *self.children(size, ['surface'] * 2)),
                            lambda: s.Neg(self.children(size, ['surface'])[0]),
                            lambda: sequence(s.Tuple, 2),
                            lambda: s.Pi(self.names(), *self.children(size, ['surface'] * 2)),
                            lambda: s.Sigma(self.names(), *self.children(size, ['surface'] * 2)),
                            lambda: named_pair(s.SigmaNamed),
                            record, subtype, lambda: pairs(s.RecordValue), block,
                            lambda: pairs(s.Sum, 2), lambda: sequence(s.List, 0), lambda_, match,
                            lambda: s.NamedArg(self.name(), self.children(size, ['surface'])[0]),
                            if_, lambda: s.Proj(self.children(size, ['surface'])[0], self.name()),
                            lambda: s.Quoted(self.children(size, ['surface'])[0])]
        elif kind in {'pattern', 'subpattern'}:
            choices = [lambda: s.PWild(), lambda: s.PLit(self.literal()),
                       lambda: s.PApp(self.name(), ())]
            if size:
                choices += [lambda: s.PTuple(tuple(self.children(size, ['pattern'] * rng.randint(2, 3))))]
                if kind == 'pattern':
                    choices += [lambda: s.PApp(self.name(), tuple(self.children(size, ['pattern'] * rng.randint(1, 2))))]
        elif kind == 'param':
            choices = [lambda: s.PlainParam(self.name())]
            if size:
                choices += [lambda: s.TypedParam(self.names(), self.children(size, ['surface'])[0]),
                            lambda: s.ShapeParam(tuple(self.children(size, ['pattern'] * rng.randint(2, 3))))]
        elif kind == 'item':
            # Items have a recursive argument, so callers may not request them at zero.
            assert size > 0
            if rng.randrange(2):
                return s.Bind(self.name(), self.children(size, ['surface'])[0])
            # Rebind's left is a pattern (D-2026-10-13-ag); half of those with room are a tuple,
            # the action's `W * A`, which the uniform pattern choice would rarely give.
            pattern_size, value_size = self.child_budgets(size, ['pattern', 'surface'])
            if pattern_size and rng.randrange(2):
                pattern = s.PTuple(tuple(self.children(pattern_size, ['pattern'] * rng.randint(2, 3))))
            else:
                pattern = self.node('pattern', pattern_size)
            return s.Rebind(pattern, self.node('surface', value_size))
        elif kind == 'binder':
            assert size > 0
            values = self.children(size, ['surface'] * rng.randint(1, 2))
            return (s.Implicit(self.names(), values[0]) if rng.randrange(2) else
                    s.Explicit(self.names(), values[0], values[1] if len(values) == 2 else None))
        elif kind == 'body':
            choices = [lambda: s.DataBody(())]
            if size:
                def clauses():
                    count = rng.randint(1, 2)
                    patterns = [rng.randint(1, 2) for _ in range(count)]
                    values = iter(self.children(size, sum((['pattern'] * n + ['surface'] for n in patterns), [])))
                    return s.ClausesBody(tuple(s.Clause(tuple(next(values) for _ in range(n)), next(values)) for n in patterns))
                choices += [lambda: s.TermBody(self.children(size, ['surface'])[0]),
                            lambda: s.DataBody(tuple((self.name(), v) for v in self.children(size, ['surface'] * rng.randint(1, 2)))),
                            clauses]
        elif kind == 'act':
            def import_():
                return s.ImportAct(rng.choice(('x.lth', 'a"\\\nb.lut', '')),
                                   tuple(s.ImportName(self.name(), self.name() if rng.randrange(2) else None,
                                                      self.name() if rng.randrange(2) else None)
                                         for _ in range(rng.randint(1, 2))))
            choices = [import_]
            if size:
                def named(cls):
                    count = rng.randint(0, min(2, size - 1))
                    values = self.children(size, ['binder'] * count + ['surface'])
                    return cls(self.name(), tuple(values[:-1]), values[-1])

                def define():
                    count = rng.randint(0, min(2, size - 1))
                    annotation = bool(rng.randrange(2))
                    values = self.children(size, ['binder'] * count + ['surface'] * annotation + ['body'])
                    return s.Define(self.name(), tuple(values[:count]), values[count] if annotation else None, values[-1])
                choices += [lambda: named(s.Declare), define, lambda: named(s.Alias),
                            lambda: s.OperatorAct(rng.choice(BOUND), self.children(size, ['surface'])[0]),
                            lambda: s.Datum(self.children(size, ['surface'])[0])]
        else:
            raise ValueError(kind)
        return rng.choice(choices)()

    def program(self, size):
        count = self.rng.randint(0, 3)
        return tuple(self.node('act', part) for part in split_budget(self.rng, size, count))


RECURSIVE_TYPES = (s.Surface.__args__ + s.SurfacePattern.__args__ + s.SurfaceAct.__args__
                   + s.LambdaParam.__args__ + s.Item.__args__ + s.Binder.__args__ + s.Body.__args__)


def recursive_children(value):
    if isinstance(value, RECURSIVE_TYPES):
        yield value
    elif is_dataclass(value):
        for field in fields(value):
            yield from recursive_children(getattr(value, field.name))
    elif isinstance(value, tuple):
        for child in value:
            yield from recursive_children(child)


def recursive_depth(value):
    """Depth through recursive constructors; Field/Clause/pair records are metadata wrappers."""
    if isinstance(value, RECURSIVE_TYPES):
        children = [child for field in fields(value)
                    for child in recursive_children(getattr(value, field.name))]
        return 1 + max(map(recursive_depth, children)) if children else 0
    return max((recursive_depth(child) for child in recursive_children(value)), default=0)


def measure(value):
    if is_dataclass(value):
        return (2 if isinstance(value, s.SurfaceAct.__args__) and not isinstance(value, s.Datum) else 1) + sum(measure(getattr(value, field.name)) for field in fields(value))
    if isinstance(value, tuple):
        return sum(map(measure, value))
    return len(value) if isinstance(value, str) else 0


def reductions(value):
    """Cheap structural shrinking; wf validation rejects invalid cardinalities."""
    if is_dataclass(value):
        if isinstance(value, s.Surface.__args__):
            yield s.Name('a')
            for field in fields(value):
                child = getattr(value, field.name)
                if isinstance(child, s.Surface.__args__):
                    yield child
        if isinstance(value, s.SurfacePattern.__args__):
            yield s.PWild()
        if isinstance(value, s.SurfaceAct.__args__) and not isinstance(value, s.Datum):
            for field in fields(value):
                child = getattr(value, field.name)
                if isinstance(child, s.Surface.__args__):
                    yield s.Datum(child)
                if isinstance(child, s.TermBody):
                    yield s.Datum(child.term)
        for field in fields(value):
            child = getattr(value, field.name)
            for smaller in reductions(child):
                yield replace(value, **{field.name: smaller})
            if child is not None and field.name in {'default', 'law', 'else_branch', 'type', 'theory', 'asName'}:
                # Optional-field validity is checked by wf; required fields never become None.
                if isinstance(value, (s.Define, s.Explicit, s.Record, s.IfThen, s.ImportName)):
                    yield replace(value, **{field.name: None})
    elif isinstance(value, str) and value in NAMES and value != 'a':
        yield 'a'
    elif isinstance(value, str) and value in BOUND and value != '+':
        yield '+'
    elif isinstance(value, tuple):
        for i, child in enumerate(value):
            yield value[:i] + value[i + 1:]
            for smaller in reductions(child):
                yield value[:i] + (smaller,) + value[i + 1:]


def outcome(program):
    text = print_program(program)
    return text, parse(text)


def descendants(value):
    yield value
    if is_dataclass(value):
        for field in fields(value):
            yield from descendants(getattr(value, field.name))
    elif isinstance(value, tuple):
        for child in value:
            yield from descendants(child)


def complexity(value):
    return measure(value), repr(value)


def shrink(program):
    current = program
    for _ in range(100):
        improved = False
        candidates = [(s.Datum(t),) for t in descendants(current) if isinstance(t, s.Surface.__args__)]
        candidates.extend(reductions(current))
        for candidate in candidates:
            if complexity(candidate) >= complexity(current):
                continue
            try:
                valid = wf_program(candidate)
            except (TypeError, AttributeError, ValueError):
                valid = False
            if valid and outcome(candidate)[1] != s.Parsed(candidate):
                current = candidate
                improved = True
                break
        if not improved:
            return current
    return current


def test_names_are_lexical_names():
    assert all(map(is_name, NAMES))


@pytest.mark.parametrize('size', SIZES)
def test_random_written_programs(size):
    failures = []
    for seed in SEEDS:
        program = Trees(seed).program(size)
        assert wf_program(program), f'seed={seed}, size={size}, tree={program!r}'
        text, result = outcome(program)
        if result != s.Parsed(program):
            minimal = shrink(program)
            failures.append((seed, size, minimal, *outcome(minimal)))
    # Complete the entire seed census even when an earlier tree failed.
    assert not failures, '\n'.join(map(repr, failures))


def test_random_items_round_trip():
    """Items are rare in whole programs, so the item generator gets a census of its own:
    each item, first in a block, written and read back (the tuple case of BlockOrRecordValue)."""
    failures, tuples = [], 0
    for size in range(1, 7):
        for seed in SEEDS:
            item = Trees(seed).node('item', size)
            tuples += isinstance(item, s.Rebind) and isinstance(item.pattern, s.PTuple)
            program = (s.Datum(s.Block((item,), s.Name('a'))),)
            assert wf_program(program), f'seed={seed}, size={size}, tree={program!r}'
            text, result = outcome(program)
            if result != s.Parsed(program):
                failures.append((seed, size, program, text, result))
    assert not failures, '\n'.join(map(repr, failures))
    assert tuples


def test_generator_wf_and_canonical_without_expected_failure():
    seen = set()
    for size in SIZES:
        for seed in SEEDS:
            program = Trees(seed).program(size)
            context = f'seed={seed}, size={size}, tree={program!r}'
            assert wf_program(program), context
            assert recursive_depth(program) <= size, context
            assert program == Trees(seed).program(size), context
            seen.update(type(node) for node in descendants(program) if is_dataclass(node))
            text, result = outcome(program)
            # Canonical is true when parsing fails, exactly as grammar.lth states it.
            if isinstance(result, s.Parsed):
                assert parse(print_program(result.program)) == result, context + f', text={text!r}'
    assert set(s.Surface.__args__) | set(s.SurfaceAct.__args__) <= seen


def test_wf_shape_constraints():
    a = s.Name('a')
    assert not wf(s.Tuple((a,)))
    assert not wf(s.PTuple((s.PWild(),)))
    assert not wf(s.Pi((), a, a))
    assert not wf(s.Record((s.Field(('a',), a),), a))
    assert wf(s.Record((s.Field(('a', 'b'), a),), a))
    assert not wf(s.Subtype(s.PApp('a', (s.PWild(),)), a, a))
    assert wf(s.Subtype(s.PTuple((s.PApp('a', (s.PWild(),)), s.PWild())), a, a))
    assert not wf(s.RecordValue(()))
    assert not wf(s.Sum(()))
    assert not wf(s.Sum((("a", a),)))
    assert wf(s.DataBody(()))
    assert not wf(s.ClausesBody(()))
    assert not wf(s.Clause((), a))
    assert not wf(s.ImportAct('x.lth', ()))
    assert not wf(s.Lambda((), (), a))
    assert not wf(s.Binop(':=', a, a))
    assert not wf(s.OperatorAct('==', a))
    assert not wf(s.Literal(s.IntLit(-1)))
    assert not wf(s.PLit(s.FloatLit(-0.5)))
    assert not wf(s.Literal(s.FloatLit(float('inf'))))
    assert not wf(s.Literal(s.FloatLit(float('nan'))))
    assert wf(s.Literal(s.FloatLit(-0.0)))
    assert wf_program(())
