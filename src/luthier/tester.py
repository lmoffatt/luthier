"""`luthier test`: the specimen of test.lth's `Tester`, exhaustive and sampled.

Sources: spec 7.S1, 7.S3, 7.S7, 7.S8, 7.S10, 7.S12, 7.S20, 7.R1 to 7.R4 (docs/spec/07-tests.md);
src/luthier/lib/test.lth (`TestSpec`, `test`, `Tester`, `grade`), laws.lth (`Evidence`, `Points`,
`NotRun`, `Coverage`, `Verdict`, `ForallOnPoints`), generators.lth (`Seed`, `Binding`, `resolve`,
`Budgets`). Derivation: record/IA/tester-2026-10-14/prompt.md, bite 1 (step 5.2 of the plan from
zero), by a Claude agent of the coordinating session, 2026-10-14.

A file's top-level `test` lines are data (D9): each is reduced with run.py's Runner to the
`TestSpec` test.lth's `test` builds, with its defaults. The law it names is a definition whose
parameters are the quantified variables and whose result is `Bool`; each case gives a value to
every parameter and is reduced with the same Runner (core, imports, the host) to `true` or
`false`. Under `ExhaustiveMode` the cases are every value of the parameters' types when they are
finite; under `SampledMode` `n` cases are drawn from the seed. The evidence is laws.lth's: the
points evaluated with the coverage reached, or `NotRun` with the reason. The verdict over the
points is laws.lth's `ForallOnPoints`, and the grade is test.lth's `grade`, reduced by the Runner.

Not in this bite (each says so where it applies): the metric of `SampledMode` (draws are uniform
between the bounds, 7.S4's special values and atom at 0 too); the sized generators of recursive
data other than `List` (7.S3's [proposed] row); enumeration of lists under `ExhaustiveMode`;
covering arrays (7.R3: above `coveringAbove` cases the test is not run); bindings to a generator
(a binding here names a census: one value, or a list of values, of the program); a size schedule
(every case is drawn at the spec's size). Of the budgets
(7.S8) only `tries` and `coveringAbove` are read: a draw a filter cannot give within `tries`
makes the law not run (7.S6), so `drawsPerCase` and `redraws` have nothing to bound yet. A case
whose reduction raises (the host failed, a match stuck, the fuel spent) is not evaluated
(7.S12); it is reported on that case and leaves the law unsettled unless another case refutes it.
A name two libraries define is scoped by its file in run.py's loader (12.S22): a law or a census
a test line names is the one the test file sees.

The store (bite 2, record/IA/certification-2026-10-14/prompt-certify.md; certification.lth §1,
7.S9, 7.S13): each line's identity is the law, the hash of its cone (certify.py), the binding
expanded per parameter, the seed and `n`. Before a line runs its identity is looked up in
`x.cert.json`: a known outcome, whatever it is, is reused and reported as known with its date;
`deep` runs it again (and records nothing new: the store keeps one outcome per identity). A line
run writes its entry, with the reach of each parameter, the evidence, the grade when it passed,
the date, the interpreter's revision and the host code by route.
"""
from __future__ import annotations

import random
import string
from dataclasses import dataclass, field, fields, is_dataclass, replace
from pathlib import Path

from . import certify, host, kernel, surface as s, term as t
from .elaborate import elaborate_program, show_term as _show_term
from .parse import parse
import numpy as np

from .run import (Entries, Loaded, Runner, RunError, _applied, _arrow, _instantiate, _primitive_body, core_data,
                  runtime_slice)

TRUE, FALSE = t.Var("true"), t.Var("false")
_TEST_LTH = (Path(__file__).parent / "lib" / "test.lth").resolve()
_LAWS_LTH = (Path(__file__).parent / "lib" / "laws.lth").resolve()
_LETTERS = string.ascii_letters + string.digits + " "  # [proposed] the alphabet of a drawn String


class NoGenerator(Exception):
    """A parameter's type has no generator under the mode: the test is not run (7.R2 to 7.R4)."""


class Unfit(Exception):
    """A filter gave no value within its budget of tries: the law is not run (7.S6)."""


def _unqualified(term):
    """A term with each name as its file writes it, without the `@file` the loader gives a name
    two files define (run.py's `Loaded`), which the user never sees."""
    if isinstance(term, t.Var):
        return t.Var(term.name.partition("@")[0])
    if isinstance(term, tuple):
        return tuple(_unqualified(x) for x in term)
    if is_dataclass(term) and not isinstance(term, type):
        return replace(term, **{f.name: _unqualified(getattr(term, f.name)) for f in fields(term)
                                if f.init and not isinstance(getattr(term, f.name), str)})
    return term


def _show(term):
    return _show_term(_unqualified(term))


# ---------------------------------------------------------------------- the spec (test.lth §1)

@dataclass
class Binding:
    """generators.lth's `Binding`: the generator named for a parameter or a type, with its coverage."""
    parameter: str | None
    type: str | None
    generator: str
    coverage: t.Term


@dataclass
class Spec:
    """test.lth's `TestSpec`, read from the value the `test` line reduces to."""
    law: str
    sampled: bool
    metric: t.Term | None
    cases: int
    size: int
    seed: int
    where: list
    profile: list
    budgets: dict


# ---------------------------------------------------------------------- the evidence (laws.lth)

@dataclass
class Points:
    """laws.lth's `Points A pts c`: each case (the values of the parameters) with its evidence,
    `Evaluated b`, and the coverage reached."""
    cases: list
    coverage: t.Term


@dataclass
class NotRun:
    reason: str


@dataclass
class Outcome:
    spec: Spec
    evidence: object
    verdict: str            # a constructor of laws.lth's `Verdict`, or "NotRun"
    grade: str | None       # a constructor of test.lth's `Grade`, or None
    evaluated: int          # cases evaluated to a verdict (7.S12)
    refuting: tuple | None  # the first refuting case
    raised: list = field(default_factory=list)  # (case, message): the host failed or the reduction stuck
    parameters: tuple = ()
    cone: str | None = None     # the hash of the law's cone (certify.py)
    entry: dict | None = None   # the store's entry of this line (certification.lth's `Entry`)
    known: str | None = None    # the date of the known entry reused, when the line did not run
    stale: str | None = None    # the date of a stale entry of the same law and binding, kept
    differs: str | None = None  # under `deep`, the date of a known entry whose outcome differs


# ---------------------------------------------------------------------- loading

def _refined_records(value):
    """A record type with a refinement, `{ x y : A | p }`, as a subtype of the record, so the
    elaborator takes it and the tester filters by it: `{ r : { x y : A } | (fn x y { p }) r.x r.y }`
    (the elaborator refuses record refinements, which check.py reads)."""
    if isinstance(value, tuple):
        return tuple(_refined_records(v) for v in value)
    if not is_dataclass(value) or isinstance(value, type):
        return value
    value = replace(value, **{f.name: _refined_records(getattr(value, f.name)) for f in fields(value)})
    if isinstance(value, s.Record) and value.law is not None:
        names = [n for f in value.fields for n in f.names]
        predicate = s.Lambda(tuple(s.PlainParam(n) for n in names), (), value.law)
        for n in names:
            predicate = s.App(predicate, s.Proj(s.Name("record%"), n))
        return s.Subtype(s.PApp("record%", ()), replace(value, law=None), predicate)
    return value


def _string_literals(value):
    if isinstance(value, s.StringLit):
        yield value.value
    elif isinstance(value, tuple):
        for v in value:
            yield from _string_literals(v)
    elif is_dataclass(value) and not isinstance(value, type):
        for f in fields(value):
            yield from _string_literals(getattr(value, f.name))


def collect_tests(path):
    """The file's own top-level `test` lines (D9), not those of what it imports."""
    result = parse(Path(path).read_text(encoding="utf-8"))
    if isinstance(result, s.ParseFailed):
        raise RunError("; ".join(f"{path}:{e.line}:{e.column}: {e.message}" for e in result.errors))
    lines = []
    for act in result.program:
        if isinstance(act, s.Datum):
            head = act.value
            while isinstance(head, s.App):
                head = head.function
            if head == s.Name("test"):
                lines.append(act.value)
    return lines


def load_program(path, fuel, extra=()):
    """The runtime program of the file as `run` loads it (core, imports scoped by file, the host's
    routes), with each test line as a definition `test%k`, the laws and censuses its string
    literals name (and `extra`), and test.lth's `grade` as roots; the Runner over it, the names of
    the test lines and the loader (whose `name` gives a name of a file as the program calls it)."""
    host.reset()
    loaded = Loaded(path)
    top = loaded.top
    specs = []
    for k, v in enumerate(collect_tests(path)):
        missing = []
        specs.append(s.Define(f"test%{k}", (), None, s.TermBody(loaded.rename(top, v, set(), missing))))
        if missing:
            loaded.errors[f"test%{k}"] = missing
    specs = tuple(specs)
    named = tuple(dict.fromkeys(loaded.name(top, n) or n for d in specs for n in _string_literals(d)))
    grading = tuple(_constructor(loaded)(n).name for n in ("grade", "Coverage", "Verdict", "Grade"))
    roots = (core_data(loaded) + tuple(d.name for d in specs) + named
             + tuple(loaded.name(top, n) or n for n in extra) + grading)
    kept = runtime_slice(loaded.acts + specs, specs[0].name if specs else "main", roots)
    loaded.demand(kept)
    program = tuple(_primitive_body(a) for a in elaborate_program(_refined_records(kept)))
    program += tuple(t.Define(op, t.Universe(), t.Primitive(op)) for op in kernel.BOOTSTRAP_PRIMITIVES)
    return Runner(program, fuel), [d.name for d in specs], loaded


# ---------------------------------------------------------------------- reading the spec

def _int(v):
    if isinstance(v, t.Lit) and isinstance(v.constant, t.IntConst):
        return v.constant.value
    raise RunError(f"not an integer: {_show(v)}")


def _text(v):
    if isinstance(v, t.Lit) and isinstance(v.constant, t.StringConst):
        return v.constant.value
    raise RunError(f"not a string: {_show(v)}")


def _list(runner, v):
    items = []
    v = runner.whnf(v)
    while isinstance(v, t.App) and isinstance(v.function, t.App) and v.function.function == t.Var("cons"):
        items.append(v.function.argument)
        v = runner.whnf(v.argument)
    if v != t.Var("nil"):
        raise RunError(f"not a list: {_show(v)}")
    return items


def _maybe_text(v):
    if v == t.Var("nothing"):
        return None
    if isinstance(v, t.App) and v.function == t.Var("just"):
        return _text(v.argument)
    raise RunError(f"not a Maybe String: {_show(v)}")


def read_spec(runner, value):
    runner.fuel = 1_000_000
    record = dict(runner.value(value).fields)
    mode = record["mode"]
    if _base(mode) == "ExhaustiveMode":
        sampled, metric = False, None
    elif isinstance(mode, t.App) and _base(mode) == "SampledMode":
        sampled, metric = True, mode.argument
    else:
        raise RunError(f"not a Mode: {_show(mode)}")
    def bindings(v):
        out = []
        for b in _list(runner, v):
            b = dict(runner.value(b).fields)
            out.append(Binding(_maybe_text(b["parameter"]), _maybe_text(b["type"]), _text(b["generator"]),
                               b["coverage"]))
        return out
    budgets = {label: v.constant.value for label, v in record["budgets"].fields}
    return Spec(_text(record["law"]), sampled, metric, _int(record["cases"]), _int(record["size"]),
                _int(record["seed"]), bindings(record["whereBindings"]), bindings(record["profile"]), budgets)


# ---------------------------------------------------------------------- coverage (test.lth §2)

def _rank(c):
    """test.lth's `rankOf`."""
    return {"Exhaustive": 3, "Bounded": 2, "Listed": 1, "Drawn": 0}[_base(c)]


def _weaker(c, d):
    return c if _rank(c) <= _rank(d) else d


def resolve_binding(spec, parameter, type_name):
    """generators.lth's `resolve`: a parameter's binding in `where`, then in the profile, then a
    binding of its type in `where`, then in the profile."""
    for bs, by_parameter in ((spec.where, True), (spec.profile, True), (spec.where, False), (spec.profile, False)):
        for b in bs:
            if by_parameter and b.parameter == parameter:
                return b
            if not by_parameter and b.parameter is None and b.type == type_name:
                return b
    return None


# ---------------------------------------------------------------------- types and their values

def _mentions(term, name):
    if term == t.Var(name):
        return True
    if isinstance(term, tuple):
        return any(_mentions(x, name) for x in term)
    if is_dataclass(term) and not isinstance(term, type):
        return any(_mentions(getattr(term, f.name), name) for f in fields(term))
    return False


def _conjuncts(p):
    if isinstance(p, t.App) and isinstance(p.function, t.App) and p.function.function == t.Var("and"):
        return _conjuncts(p.function.argument) + _conjuncts(p.argument)
    return [p]


def _head_name(ty):
    while isinstance(ty, t.App):
        ty = ty.function
    return ty.name.partition("@")[0] if isinstance(ty, t.Var) else None


class Values:
    """The values of a type as kernel terms: every one (exhaustive) or one drawn (sampled)."""

    def __init__(self, runner, rng, size, budgets, fuel):
        self.runner, self.rng, self.size, self.budgets, self.fuel = runner, rng, size, budgets, fuel

    def whnf(self, term):
        self.runner.fuel = self.fuel
        return self.runner.whnf(term)

    def form(self, ty):
        """The type unfolded and its refinements collected: (base, [(name, predicate), ...])."""
        predicates = []
        while True:
            ty = self.whnf(ty)
            if isinstance(ty, t.Subtype):
                predicates.append((ty.name, ty.predicate))
                ty = ty.type
            elif isinstance(ty, t.Var) and ty.name in self.runner.types and self.runner.types[ty.name] != ty:
                ty = self.runner.types[ty.name]
            else:
                return ty, predicates

    def holds(self, predicates, value):
        for name, p in predicates:
            r = self.whnf(kernel.substitute(name, value, p))
            if r == FALSE:
                return False
            if r != TRUE:
                raise RunError(f"a refinement gave {_show(r)}, not a Bool")
        return True

    def bounds(self, predicates, kind):
        """The interval a refinement states with literal bounds (7.S6), each side or None."""
        lo = hi = None
        for name, p in predicates:
            for c in _conjuncts(p):
                if not (isinstance(c, t.App) and isinstance(c.function, t.App) and isinstance(c.function.function, t.Var)):
                    continue
                op, left, right = c.function.function.name, c.function.argument, c.argument
                if op not in ("<=", "<", ">=", ">"):
                    continue
                if left == t.Var(name) and not _mentions(right, name):
                    bound, upper = right, op in ("<=", "<")
                elif right == t.Var(name) and not _mentions(left, name):
                    bound, upper = left, op in (">=", ">")
                else:
                    continue
                try:
                    bound = self.whnf(bound)
                except RunError:
                    continue
                if not (isinstance(bound, t.Lit) and isinstance(bound.constant, (t.IntConst, t.FloatConst))):
                    continue
                b = bound.constant.value
                if kind == "Int" and op in ("<", ">"):
                    b = b - 1 if upper else b + 1
                if upper:
                    hi = b if hi is None else min(hi, b)
                else:
                    lo = b if lo is None else max(lo, b)
        return lo, hi

    # ---------------------------------------------------------- exhaustive (7.S3, 7.R3)

    def every(self, ty, limit):
        """Every value of a finite type, at most `limit + 1` of them; NoGenerator when infinite."""
        base, predicates = self.form(ty)
        if isinstance(base, t.Var) and base.name == "Int":
            lo, hi = self.bounds(predicates, "Int")
            if lo is None or hi is None:
                raise NoGenerator(f"{_show(ty)} is infinite: ExhaustiveMode needs its bounds or a census (7.R3)")
            values = (t.Lit(t.IntConst(k)) for k in range(lo, hi + 1))
        else:
            values = self.every_base(base, limit)
        out = []
        for v in values:
            if self.holds(predicates, v):
                out.append(v)
                if len(out) > limit:
                    break
        return out

    def every_base(self, ty, limit):
        if isinstance(ty, t.Universe):
            raise NoGenerator("a parameter of type U has no generator (7.R2)")
        if isinstance(ty, t.Data):
            return self.every_constructor(ty, limit)
        if isinstance(ty, t.Sigma):
            out = []
            for left in self.every(ty.domain, limit):
                for right in self.every(_instantiate(ty.name, left, ty.codomain), limit):
                    out.append(t.Pair(left, right))
                    if len(out) > limit:
                        return out
            return out
        if isinstance(ty, t.Record):
            return [t.RecordValue(tuple(items)) for items in self.every_fields(list(ty.fields), limit)]
        if isinstance(ty, t.Sum):
            return [t.Inj(label, v) for label, a in ty.alternatives for v in self.every(a, limit)]
        if _applied(ty, "List") is not None:
            raise NoGenerator("a list under ExhaustiveMode: its enumeration up to the size is a later bite")
        if _arrow(ty) is not None:
            raise NoGenerator(f"a function {_show(ty)}: bind a census (7.R4)")
        raise NoGenerator(f"{_show(ty)} has no finite enumeration (7.R3)")

    def every_fields(self, types, limit):
        if not types:
            return [[]]
        (label, ty), rest = types[0], types[1:]
        out = []
        for v in self.every(ty, limit):
            later = [(l, _instantiate(label, v, f)) for l, f in rest]
            for items in self.every_fields(later, limit):
                out.append([(label, v)] + items)
                if len(out) > limit:
                    return out
        return out

    def every_constructor(self, data, limit):
        out = []
        for name, ty in data.constructors:
            domains = self.domains(data, ty)
            combos = [[]]
            for d in domains:
                combos = [c + [v] for c in combos for v in self.every(d, limit)]
                if len(combos) > limit:
                    break
            out.extend(Runner.apply(t.Var(name), c) for c in combos)
            if len(out) > limit:
                break
        return out

    def domains(self, data, ty):
        """The argument types of a constructor; NoGenerator when one is the data itself."""
        domains = []
        while (arrow := _arrow(ty)) is not None:
            if _mentions(arrow[1], data.name):
                raise NoGenerator(f"recursive data {data.name}: its sized generator is a later bite (7.S3)")
            domains.append(arrow[1])
            ty = arrow[2]
        return domains

    # ---------------------------------------------------------- sampled (7.S3, 7.S6)

    def draw(self, ty):
        base, predicates = self.form(ty)
        kind = base.name if isinstance(base, t.Var) else None
        lo, hi = self.bounds(predicates, kind) if kind in ("Int", "Float64") else (None, None)
        fixed = self.fixed_fields(predicates) if isinstance(base, t.Record) else {}
        for _ in range(self.budgets.get("tries", 2000)):
            v = self.draw_base(base, lo, hi, fixed)
            if self.holds(predicates, v):
                return v
        raise Unfit(f"no value of {_show(ty)} in {self.budgets.get('tries', 2000)} tries (7.S6)")

    def fixed_fields(self, predicates):
        """The fields of a record a refinement equates, conjunct by conjunct, to a value: `v.n == k`
        (`VecOf k`), `a.m == r and a.n == c` (`MatOf r c`), `a.m == a.n` (`Square`). Each is built,
        not drawn and filtered (7.S6): {label: (name, expression)}, the expression read once the
        fields it names are drawn."""
        fixed = {}
        for name, p in predicates:
            for c in _conjuncts(p):
                if not (isinstance(c, t.App) and isinstance(c.function, t.App) and c.function.function == t.Var("==")):
                    continue
                for side, other in ((c.function.argument, c.argument), (c.argument, c.function.argument)):
                    if isinstance(side, t.Proj) and side.record == t.Var(name) and side.label not in fixed:
                        if not _mentions(other, name) or isinstance(other, t.Proj) and other.record == t.Var(name):
                            fixed[side.label] = (name, other)
                            break
        return fixed

    def fixed_value(self, fixed, label, items):
        """The value a refinement fixes for `label`, given the fields drawn so far, or None."""
        if label not in fixed:
            return None
        name, expr = fixed[label]
        if _mentions(expr, name):
            if not (isinstance(expr, t.Proj) and expr.label in dict(items)):
                return None
            return dict(items)[expr.label]
        try:
            v = self.whnf(expr)
        except RunError:
            return None
        return v if isinstance(v, t.Lit) else None

    def table(self, ty):
        """A function on finite indices, `Fin n -> ... -> A` with `A` a `Float64` or an `Int` (each a
        subtype, bounds read), drawn entry by entry as the host array it is (3.S21, 11.S9): the
        values of a `Vec` or a `Mat`. None when the domain is not a `Fin` of a known length."""
        shape, leaf = [], ty
        while (arrow := _arrow(self.whnf(leaf))) is not None:
            if arrow[0] != "_" and _mentions(arrow[2], arrow[0]):
                return None
            try:
                k = self.runner.size(arrow[1])
            except RunError:
                return None
            if k is None:
                return None
            shape.append(k)
            leaf = arrow[2]
        base, _ = self.form(leaf)
        if not shape or base not in (t.Var("Float64"), t.Var("Int")):
            return None
        count = int(np.prod(shape)) if shape else 1
        entries = [self.draw(leaf).constant.value for _ in range(count)]
        array = np.array(entries, dtype=np.float64 if base == t.Var("Float64") else np.int64).reshape(shape)
        return self.runner.host_object(Entries(array), ty)

    def draw_base(self, ty, lo, hi, fixed=None):
        rng, n = self.rng, self.size
        if isinstance(ty, t.Var) and ty.name in ("Int", "Float64"):
            # 7.S3: the bounds of the type, otherwise [-s, s]; a missing side at s from the other
            lo = -n if lo is None else lo
            hi = (max(lo, 0) + n) if hi is None else hi
            if hi < lo:
                raise Unfit(f"an empty interval [{lo}, {hi}]")
            if ty.name == "Int":
                return t.Lit(t.IntConst(rng.randint(int(lo), int(hi))))
            return t.Lit(t.FloatConst(float(rng.uniform(float(lo), float(hi)))))
        if ty == t.Var("String"):
            return t.Lit(t.StringConst("".join(rng.choice(_LETTERS) for _ in range(rng.randint(0, n)))))
        if isinstance(ty, t.Universe):
            raise NoGenerator("a parameter of type U has no generator (7.R2)")
        if isinstance(ty, t.Data):
            name, cty = ty.constructors[rng.randrange(len(ty.constructors))]
            return Runner.apply(t.Var(name), [self.draw(d) for d in self.domains(ty, cty)])
        if isinstance(ty, t.Sigma):
            left = self.draw(ty.domain)
            return t.Pair(left, self.draw(_instantiate(ty.name, left, ty.codomain)))
        if isinstance(ty, t.Record):
            items, types = [], list(ty.fields)
            for k, (label, fty) in enumerate(types):
                v = self.fixed_value(fixed or {}, label, items)
                if v is None:
                    v = self.draw(fty)
                items.append((label, v))
                types[k + 1:] = [(l, _instantiate(label, v, f)) for l, f in types[k + 1:]]
            return t.RecordValue(tuple(items))
        if isinstance(ty, t.Sum):
            label, a = ty.alternatives[rng.randrange(len(ty.alternatives))]
            return t.Inj(label, self.draw(a))
        if (element := _applied(ty, "List")) is not None:
            result = t.Var("nil")
            for _ in range(rng.randint(0, n)):
                result = t.App(t.App(t.Var("cons"), self.draw(element)), result)
            return result
        if _arrow(ty) is not None:
            if (drawn := self.table(ty)) is not None:
                return drawn
            raise NoGenerator(f"a function {_show(ty)}: bind a census (7.R4)")
        raise NoGenerator(f"no generator of {_show(ty)}")


# ---------------------------------------------------------------------- running (test.lth §2)

def parameters(runner, law):
    """The law's quantified variables: (name, type) of its definition's arrows, its result Bool."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == law), None)
    if definition is None:
        return None
    ty, params = definition.type, []
    while isinstance(ty, t.Pi):
        params.append((ty.name, ty.domain))
        ty = ty.codomain
    return params


def _list_depth(runner, ty):
    """How many `List`s a type is nested in: a census of lists, for a parameter that is a list,
    lists its elements (`List (List A)` for a `List A`; a refined list, `UnitList`, read as one)."""
    depth = 0
    while (element := _applied(runner.resolve(ty), "List")) is not None:
        depth, ty = depth + 1, element
    return depth


def census(runner, binding, ty, name):
    """The values a binding names (7.R4): a definition of the program, `name` there, its elements
    when it is a list and the parameter is not."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == name), None)
    if definition is None:
        raise NoGenerator(f"the binding names {binding.generator}, which is not defined")
    if _list_depth(runner, definition.type) > _list_depth(runner, ty):
        values = _list(runner, t.Var(name))
        if not values:
            raise NoGenerator(f"the census {binding.generator} is empty")
        return values
    return [t.Var(name)]


def evaluate(runner, law, case, fuel):
    runner.fuel = fuel
    r = runner.whnf(Runner.apply(t.Var(law), list(case)))
    if r == TRUE:
        return True
    if r == FALSE:
        return False
    raise RunError(f"the law gave {_show(r)}, not a Bool")


def run_spec(runner, spec, fuel, loaded=None):
    """test.lth's `Tester.run`: the evidence of the law the spec names, with its verdict and grade."""
    law = _as_called(loaded, spec.law)
    params = parameters(runner, law)
    if params is None:
        return _not_run(spec, f"no definition {spec.law}")
    names = tuple(n for n, _ in params)
    values = Values(runner, random.Random(spec.seed), spec.size, spec.budgets, fuel)
    limit = spec.budgets.get("coveringAbove", 20000)
    # each parameter: a census its binding names, or the mode's functor over its type
    con = _constructor(loaded)
    plan, coverage = [], (t.App(con("Drawn"), t.Lit(t.IntConst(spec.seed))) if spec.sampled else con("Exhaustive"))
    try:
        for name, ty in params:
            b = resolve_binding(spec, name, _head_name(ty))
            plan.append(census(runner, b, ty, _as_called(loaded, b.generator)) if b else None)
    except (NoGenerator, RunError) as exc:
        return _not_run(spec, str(exc), names)
    for b in spec.where + spec.profile:  # test.lth's specCoverage: every binding weakens it
        coverage = _weaker(b.coverage, coverage)

    cases = []
    try:
        if not spec.sampled:
            cases = _every_case(values, params, plan, limit)
            if len(cases) > limit:
                return _not_run(spec, f"more than {limit} cases (coveringAbove); covering arrays are a later bite (7.R3)", names)
        else:
            # 7.S6: a draw that a filter cannot give within its tries makes the law not run
            cases = [_draw_case(values, params, plan, k) for k in range(spec.cases)]
    except (NoGenerator, Unfit) as exc:
        return _not_run(spec, str(exc), names)
    except RunError as exc:
        return _not_run(spec, f"drawing the cases: {exc}", names)

    points, raised, refuting = [], [], None
    for case in cases:
        try:
            ok = evaluate(runner, law, case, fuel)
        except (RunError, RecursionError, ValueError, KeyError, TypeError) as exc:
            raised.append((case, str(exc) or type(exc).__name__))
            continue
        points.append((case, ok))
        if not ok and refuting is None:
            refuting = case
    evidence = Points(points, coverage)
    # laws.lth's ForallOnPoints; a case that raised settles nothing (its evidence is NotRun)
    if refuting is not None:
        verdict = "Refuted"
    elif raised:
        verdict = "Unsettled"
    else:
        verdict = "Confirmed" if _base(coverage) == "Exhaustive" else "Supported"
    return Outcome(spec, evidence, verdict, grade_of(runner, verdict, coverage, loaded), len(points), refuting,
                   raised, names)


def _every_case(values, params, plan, limit, prefix=()):
    """The product of every parameter's values in order, a later type reading the earlier values."""
    if len(prefix) == len(params):
        return [prefix]
    k = len(prefix)
    ty = params[k][1]
    for (name, _), v in zip(params, prefix):
        ty = _instantiate(name, v, ty)
    out = []
    try:
        every = plan[k] if plan[k] is not None else values.every(ty, limit)
    except NoGenerator as exc:
        raise NoGenerator(f"{params[k][0]} : {_show(params[k][1])}: {exc}") from exc
    for v in every:
        out.extend(_every_case(values, params, plan, limit, prefix + (v,)))
        if len(out) > limit:
            break
    return out


def _draw_case(values, params, plan, walked):
    case = []
    for k, (name, ty) in enumerate(params):
        for (earlier, _), v in zip(params, case):
            ty = _instantiate(earlier, v, ty)
        # a census is walked in turn, each value once per round (generators.lth's `walk`, gen.10)
        try:
            case.append(plan[k][walked % len(plan[k])] if plan[k] is not None else values.draw(ty))
        except (NoGenerator, Unfit) as exc:
            raise type(exc)(f"{name} : {_show(params[k][1])}: {exc}") from exc
    return tuple(case)


def grade_of(runner, verdict, coverage, loaded=None):
    """test.lth's `grade`, reduced: the grade's constructor, or None."""
    runner.fuel = 100000
    con = _constructor(loaded)
    g = runner.value(Runner.apply(con("grade"), [con(verdict), t.App(t.Var("just"), coverage)]))
    if isinstance(g, t.App) and g.function == t.Var("just"):
        return _base(g.argument)
    return None


def _as_called(loaded, n):
    """A name the test file writes (a law, a census) as the program calls it."""
    return n if loaded is None else (loaded.name(loaded.top, n) or n)


def _constructor(loaded):
    """A name of test.lth (`grade`, `Grade`'s constructors) or laws.lth (`Verdict`'s and
    `Coverage`'s) as the program calls it."""
    def con(n):
        if loaded is None:
            return t.Var(n)
        return t.Var(next((m for f in (_TEST_LTH, _LAWS_LTH) if (m := loaded.name(f, n)) is not None), n))
    return con


def _base(term):
    """The name at the head of a term, without the file a clash qualified it by (run.py's loader)."""
    while isinstance(term, t.App):
        term = term.function
    return term.name.partition("@")[0] if isinstance(term, t.Var) else None


def _not_run(spec, reason, names=()):
    return Outcome(spec, NotRun(reason), "NotRun", None, 0, None, parameters=names)


# ---------------------------------------------------------------------- the command

_GRADE_WORDS = {"Proved": "proved", "ExhaustiveGrade": "exhaustive", "Cases": "cases", "Sampled": "sampled",
                "AssumedGrade": "assumed"}


def show_case(names, case):
    return ", ".join(f"{n} = {_show(v)}" for n, v in zip(names, case))


def _tail(outcome):
    """What the line settled: the grade, the refuting case, or why it settled nothing."""
    if isinstance(outcome.evidence, NotRun):
        return f"not run: {outcome.evidence.reason}"
    if outcome.verdict == "Refuted":
        return f"refuted at {show_case(outcome.parameters, outcome.refuting)}"
    if outcome.verdict == "Unsettled":
        case, message = outcome.raised[0]
        return (f"unsettled: {len(outcome.raised)} cases raised, the first at "
                f"{show_case(outcome.parameters, case)}: {message}")
    return _GRADE_WORDS.get(outcome.grade, outcome.grade)


def _entry_tail(entry):
    o = entry["outcome"]
    if o == "Passed":
        return _GRADE_WORDS.get(entry["grade"], entry["grade"])
    if "Failed" in o:
        return f"refuted at {o['Failed']}"
    return f"not run: {o['NotRunFor']}" if "NotRun" in entry["evidence"] else o["NotRunFor"]


def line(outcome):
    """One line per test: the law, the mode, the cases evaluated, the grade or the refuting case,
    and whether it ran or its outcome was known (7.S13)."""
    spec = outcome.spec
    mode = f"sampled (seed {spec.seed}, size {spec.size}, metric ignored)" if spec.sampled else "exhaustive"
    head = f"{spec.law}: {mode}, {outcome.evaluated} cases"
    if outcome.known is not None:
        return f"{head}, {_entry_tail(outcome.entry)} (known, {outcome.known})"
    how = "ran"
    if outcome.stale is not None:
        how += f"; the entry of {outcome.stale} is stale, kept"
    if outcome.differs is not None:
        how += f"; the known entry of {outcome.differs} differs and is kept"
    return f"{head}, {_tail(outcome)} ({how})"




def prepare(path, fuel=1_000_000):
    """The file's program with its test lines read as specs: the Runner, the specs, the loader."""
    runner, names, loaded = load_program(path, fuel)
    specs = [read_spec(runner, t.Var(name)) for name in names]
    # the laws and censuses the specs name, when a definition (a profile) holds their names
    defined = {a.name for a in runner.program if isinstance(a, (t.Define, t.Declare))}
    wanted = {n for spec in specs for n in [spec.law] + [b.generator for b in spec.where + spec.profile]}
    missing = sorted(n for n in wanted if _as_called(loaded, n) not in defined)
    if missing:
        runner, names, loaded = load_program(path, fuel, missing)
        specs = [read_spec(runner, t.Var(name)) for name in names]
    return runner, specs, loaded


def run_tests(path, seed=None, fuel=1_000_000, deep=False, store=False):
    """Run every `test` line of the file; the outcomes in order. With `store`, each line's identity
    is looked up in `x.cert.json` first (a known outcome is reused unless `deep`) and each line run
    is recorded there (certification.lth's `known` and `record`)."""
    runner, specs, loaded = prepare(path, fuel)
    cones = certify.Cones(runner)
    entries = certify.read_store(path) if store else []
    outcomes = []
    for spec in specs:
        if seed is not None:
            spec.seed = seed
        entry = new_entry(runner, loaded, spec, cones, fuel)
        found = certify.known(entries, certify.identity(entry))
        if found is not None and not deep:
            evidence = found["evidence"]
            points = evidence.get("Points", {})
            outcomes.append(Outcome(spec, evidence, points.get("verdict", "NotRun"), found["grade"],
                                    points.get("evaluated", 0), None, cone=entry["cone"], entry=found,
                                    known=found["date"]))
            continue
        outcome = run_spec(runner, spec, fuel, loaded)
        settle(entry, outcome)
        outcome.cone, outcome.entry = entry["cone"], entry
        if found is not None and found["outcome"] != entry["outcome"]:
            outcome.differs = found["date"]
        old = next((e for e in entries if e["law"] == entry["law"] and e["binding"] == entry["binding"]
                    and certify.stale(entry["cone"], e)), None)
        if old is not None:
            outcome.stale = old["date"]
        outcomes.append(outcome)
        if store:
            recorded = certify.record(entries, entry)
            if recorded is not entries:
                entries = recorded
                certify.write_store(path, entries)
            for home in model_homes(loaded, spec):
                certify.add_entry(home, entry)
    return outcomes


def model_homes(loaded, spec):
    """[proposed, night default for decision 1 of report-run.md] The files, other than the test
    program and core, that define a census a binding of the line names (`numpy` in
    arrays_model.lut), when the law is itself defined in another file than the test program's: the
    entry is also written into their stores, which a run of an importer reads (12.S11). A law the
    test program defines (a wrapper) has no such home."""
    if loaded is None:
        return []
    top = loaded.top
    try:
        law = loaded.see(top, spec.law)
    except RunError:
        return []
    if law is None or law[0] == top:
        return []
    homes = []
    for b in spec.where + spec.profile:
        try:
            found = loaded.see(top, b.generator)
        except RunError:
            continue
        if found is not None and found[0] not in (top, loaded.core) and found[0] not in homes:
            homes.append(found[0])
    return homes


def law_cones(path, fuel=1_000_000):
    """Each law the file's test lines name, as the file writes it, with the hash of its cone."""
    runner, specs, loaded = prepare(path, fuel)
    cones = certify.Cones(runner)
    return list({spec.law: cones.hash(_as_called(loaded, spec.law)) for spec in specs}.items())


# ---------------------------------------------------------------------- the entry (certification.lth §1)

def _value(runner, v):
    """certification.lth's `Value`: a census member that reduces to a number literal (`tolerance :=
    1.0e-12`) as the number, anything else printed as the census writes it."""
    try:
        runner.fuel = 10000
        w = runner.whnf(v)
    except (RunError, RecursionError, ValueError, KeyError, TypeError):
        w = v
    if isinstance(w, t.Lit) and isinstance(w.constant, (t.IntConst, t.FloatConst)):
        return {"Number": float(w.constant.value)}
    return {"Printed": _show(v)}


def new_entry(runner, loaded, spec, cones, fuel):
    """The entry of a line before it runs: its identity (the law, the hash of its cone, the binding
    expanded per parameter, the seed, `n`), the budgets, the reach of each parameter, the date, the
    interpreter and the host code by route (the law's cone's and each census's). The evidence, the
    grade and the outcome are `settle`'s.

    [proposed] A parameter's generator is the census its binding names, printed with the binding's
    coverage, its fingerprint the hash of the census's cone; otherwise the mode's functor over the
    parameter's type, printed with the metric and the size, its fingerprint empty (the drawing code
    is the interpreter's, in the cone's hash). The reach: a census's members; the support of the
    type under ExhaustiveMode; under SampledMode, for an `Int` or a `Float64` (refined or not, not
    dependent on an earlier parameter), the interval it is drawn from; no reach otherwise, which
    covers no value a run gives (certification.lth's `coversAll`)."""
    law = _as_called(loaded, spec.law)
    params = parameters(runner, law) or []
    values = Values(runner, random.Random(0), spec.size, spec.budgets, fuel)
    binding, reach, hosts = [], [], dict(cones.hosts(law))
    for k, (name, ty) in enumerate(params):
        b = resolve_binding(spec, name, _head_name(ty))
        if b is not None:
            called = _as_called(loaded, b.generator)
            binding.append({"parameter": name, "generator": f"{b.generator} ({_show(b.coverage)})",
                            "fingerprint": cones.hash(called)})
            hosts.update(cones.hosts(called))
            try:
                members = census(runner, b, ty, called)
            except (NoGenerator, RunError):
                continue
            reach.append({"parameter": name, "reach": {"Members": [_value(runner, v) for v in members]}})
            continue
        mode = f"SampledMode {_show(spec.metric)} (size {spec.size})" if spec.sampled else "ExhaustiveMode"
        binding.append({"parameter": name, "generator": f"{mode} over {_show(ty)}", "fingerprint": ""})
        if not spec.sampled:
            reach.append({"parameter": name, "reach": "Support"})
            continue
        if any(_mentions(ty, earlier) for earlier, _ in params[:k]):
            continue
        try:
            base, predicates = values.form(ty)
            if base not in (t.Var("Int"), t.Var("Float64")):
                continue
            lo, hi = values.bounds(predicates, base.name)
        except (RunError, RecursionError):
            continue
        lo = -spec.size if lo is None else lo        # draw_base's defaults
        hi = (max(lo, 0) + spec.size) if hi is None else hi
        reach.append({"parameter": name, "reach": {"Interval": [float(lo), float(hi)]}})
    return {"law": spec.law, "cone": cones.hash(law), "binding": binding, "seed": spec.seed, "cases": spec.cases,
            "budgets": dict(spec.budgets), "reach": reach, "evidence": None, "grade": None, "outcome": None,
            "date": certify.now(), "interpreter": certify.interpreter_revision(),
            "hosts": [[r, h] for r, h in sorted(hosts.items())]}


def settle(entry, outcome):
    """The entry's evidence, grade and outcome from the line's: passed with its grade; failed at
    the refuting case; not run with its reason, or unsettled with the first case that raised."""
    if isinstance(outcome.evidence, NotRun):
        entry["evidence"] = {"NotRun": outcome.evidence.reason}
        entry["outcome"] = {"NotRunFor": outcome.evidence.reason}
        return entry
    entry["evidence"] = {"Points": {"evaluated": outcome.evaluated, "raised": len(outcome.raised),
                                    "coverage": _show(outcome.evidence.coverage), "verdict": outcome.verdict}}
    if outcome.verdict == "Refuted":
        entry["outcome"] = {"Failed": show_case(outcome.parameters, outcome.refuting)}
    elif outcome.grade is not None:
        entry["outcome"], entry["grade"] = "Passed", outcome.grade
    else:
        entry["outcome"] = {"NotRunFor": _tail(outcome)}
    return entry
