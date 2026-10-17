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
covering arrays (7.R3: above `coveringAbove` cases the test is not run); a size schedule (every
case is drawn at the spec's size).

A binding names a census (one value, or a list of values, of the program) or a generator (bite 3,
record/IA/tester-2026-10-14/prompt-3.md; 7.R1, 7.S1, 7.S7): a value of `Gen T`, written in Luthier
or a host extern, or a family `(x : A) -> ... -> Gen T` whose parameters are named after earlier
parameters of the law, which it reads (generators.lth's `dependent`). Under SampledMode the tester
applies it to those values, the spec's size and the current seed; the seed starts at the spec's
and each draw gives the next (7.S1), so one first seed fixes every draw. What it gives must belong
to the parameter's type, checked on every draw (7.S1's validity); a value outside it makes the law
not run, the generator's failure and not the law's. Its coverage is `Drawn` at the spec's seed.

Of the budgets (7.S8) only `tries` and `coveringAbove` are read: a draw a filter cannot give within `tries`
makes the law not run (7.S6), so `drawsPerCase` and `redraws` have nothing to bound yet. A case
whose reduction raises (the host failed, a match stuck, the fuel spent) is not evaluated
(7.S12); it is reported on that case and leaves the law unsettled unless another case refutes it.
A name two libraries define is scoped by its file in run.py's loader (12.S22): a law or a census
a test line names is the one the test file sees.

The store (bite 2, record/IA/certification-2026-10-14/prompt-certify.md; certification.lth §1,
7.S9, 7.S13): each line's identity is the law, the hash of its cone (certify.py), the binding
expanded per parameter, the seed and `n`. Before a line runs its identity is looked up in
the store of the file that makes the line's claim (`claim_file`): a known outcome, whatever it is,
is reused and reported as known with its date; `deep` runs it again, and its entry is recorded by
the store law (certify.py's `record`, D-2026-10-15-f): nothing new when it agrees with the known
entry, written beside it when it disagrees, and the law is then refused until a later run agrees
(the line says "replay disagrees"). A line run writes its entry there, with the reach of each
parameter, the evidence, the grade when it passed, the date, the interpreter's revision and the
host code by route. [D-2026-10-15-g] A line cut by its fuel (a case or a draw stopped with the
Runner's fuel at zero) settles nothing and writes nothing: its outcome is `NotRunFor "fuel spent"`,
the line says how much fuel it was given, and the next run runs it again; the fuel is in no
identity. The file that makes the claim (L10.12, D-2026-10-16-b; record/IA/
code-follows-2026-10-16/prompt-claim-store.md) is the file that defines the model of the library
the line's binding names (`model_homes`), or, when it names none, the file that states the law; a
test program, which only gathers evidence, keeps no store of its own, and none beside it is read.

A control (record/IA/controls-2026-10-15/prompt-tester.md; 7.S19 as D-2026-10-15-a generalized it,
L9.14; test.lth's `control` field and `controlPasses`): a line written `(control <- true)` tests its
law on a model broken on purpose and expects it refuted. It runs as any line, and its entry is its
own kind, `"kind": "Control"` [proposed], whose outcome is `ControlRefuted` (the case: the control
passed), `ControlConfirmed` (the law held on the broken model: the control failed, the law too weak
to see the break) or `NotRunFor`; it never carries a grade, never grades or refutes the law, and
lives as any line's entry beside the claim it controls (`claim_file`: the broken model being the
test program's, the file that states the law). certify.py reads it as the law's control.

A statistical law (record/IA/statistical-2026-10-15/prompt-tester.md; laws.lth §4, 7.S17 to 7.S19,
L9.15, D-2026-10-15-b): a law whose result type is `Law` and whose body, at its bindings, reduces to
`Statistical S T l draw c`. Every parameter is bound by a census of one (a binding that names a
`Gen T` is the stream itself here, not a generator of the parameter); the cutoffs `c : Sequential`
are the demand's and are never drawn, so a line that leaves them unbound is not run, with that
reason. The line runs laws.lth's `sequential S T l draw c seed` once through the Runner, the spec's
seed the stream's state (`T` must be `Seed`; L9.15: the seed is the test's), and its evidence is
`Tested v` with alpha, beta, delta and the samples spent (with the cutoffs' `initial` and `budget`)
written in the entry (7.S17). The verdict is laws.lth's `StatisticalByTest`: `Holds` supports the
law, graded by test.lth's `grade` over `Drawn seed` (sampled); `Fails` refutes it; `Unresolved`
settles nothing, the budget spent in the entry. A statistical control passes on `Fails`.

Stretches (record/IA/code-follows-2026-10-16/prompt-pool-seeds.md; D-2026-10-16-g, laws.lth's
`ratioAfter`): the lines of a statistical law under one binding are one sequential test. A line of a
new seed, with the store read, continues the test from the ratio and the samples the latest stretch of
the law, cone, kind and binding (without its cutoffs' drawing) left at the same alpha, beta, delta and
sample size (certify.py's `continuation`). The budget bounds the whole test: a new seed buys none, and a
line whose budget the test has spent draws nothing and is unresolved; a line with a larger budget
continues it. Its entry records the ratio it stops at, its cutoffs' parameter and where it started
(`"from"`: the ratio, the samples and the seeds before it), its `spent` its own samples, and its line
says which seeds it continues. A replay (`--deep`), or its seed under another budget, starts where that
seed's stretch started, so it is deterministic given its identity and that record.
"""
from __future__ import annotations

import random
import string
from dataclasses import dataclass, field, fields, is_dataclass, replace
from pathlib import Path

from . import certify, generators, host, kernel, surface as s, term as t
from .elaborate import elaborate_program, show_term as _show_term
from .parse import parse
import numpy as np

from .run import (Entries, Loaded, Runner, RunError, _applied, _arrow, _instantiate, _primitive_body, core_data,
                  require_kind, runtime_slice)

TRUE, FALSE = t.Var("true"), t.Var("false")
_TEST_LTH = (Path(__file__).parent / "lib" / "test.lth").resolve()
_LAWS_LTH = (Path(__file__).parent / "lib" / "laws.lth").resolve()
_GENERATORS_LTH = (Path(__file__).parent / "lib" / "generators.lth").resolve()
_LETTERS = string.ascii_letters + string.digits + " "  # [proposed] the alphabet of a drawn String


class NoGenerator(Exception):
    """A parameter's type has no generator under the mode: the test is not run (7.R2 to 7.R4)."""


class Unfit(Exception):
    """A filter gave no value within its budget of tries: the law is not run (7.S6)."""


SEEDS = 2 ** 31  # generators.lth's `Seed`: an integer in [0, 2^31)


@dataclass
class Generator:
    """A binding's generator (7.R1, 7.S1): the definition as the program calls it, the binding's
    name for it, and the earlier parameters of the law it reads, in its order (7.S7)."""
    called: str
    written: str
    reads: tuple = ()


class Invalid(Exception):
    """A generator gave a value outside the parameter's type (7.S1): the law is not run."""


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
    control: bool = False   # test.lth's `control`: the line is a control, expected to be refuted


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
class Tested:
    """laws.lth's `Tested v`: the sequential test's verdict (`Holds`, `Fails`, `Unresolved`) with its
    rates (`alpha`, `beta`, `delta`, the samples `spent`), and the cutoffs' `initial` and `budget`."""
    verdict: str
    alpha: float
    beta: float
    delta: float
    spent: int
    initial: int
    budget: int
    coverage: t.Term = None
    ratio: float | None = None   # the likelihood ratio the stretch stopped at (laws.lth's `ratioAfter`)
    start: dict | None = None    # where it started, when it continued earlier stretches (D-2026-10-16-g)
    cutoffs: str | None = None   # the parameter of its cutoffs, which its union key leaves out

    def record(self):
        return {"verdict": self.verdict, "alpha": self.alpha, "beta": self.beta, "delta": self.delta,
                "spent": self.spent, "initial": self.initial, "budget": self.budget}


# laws.lth's `StatisticalByTest`: what the sequential test's verdict settles
SETTLED_BY_TEST = {"Holds": "Supported", "Fails": "Refuted", "Unresolved": "Unsettled"}


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
    differs: str | None = None  # the date of the entry a replay disagrees with (D-2026-10-15-f)
    store: object = None        # the file whose store holds the line's entry (`claim_file`)
    out_of_fuel: int | None = None  # the fuel given, when the run was cut by it (D-2026-10-15-g)
    regions: list | None = None  # the grading regions with their n (`regions_record`, D-2026-10-16-i)
    labels: list | None = None   # an author's labels with their share (`labels_record`), no grade


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
    grading = tuple(_constructor(loaded)(n).name for n in ("grade", "Coverage", "Verdict", "Grade", "sequential",
                                                             "sequentialFrom", "ratioAfter"))
    # the degenerate cases declared in the files loaded and `casesOf`, which classify reads
    regioning = tuple(n for n, _ in degeneracies_in(loaded))
    if regioning and (cases_of := loaded.name(_GENERATORS_LTH, "casesOf")) is not None:
        regioning += (cases_of,)
    else:
        regioning = ()
    roots = (core_data(loaded) + tuple(d.name for d in specs) + named
             + tuple(loaded.name(top, n) or n for n in extra) + grading + regioning)
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
    control = runner.whnf(record["control"]) == TRUE if "control" in record else False
    return Spec(_text(record["law"]), sampled, metric, _int(record["cases"]), _int(record["size"]),
                _int(record["seed"]), bindings(record["whereBindings"]), bindings(record["profile"]), budgets,
                control)


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

    def __init__(self, runner, rng, size, budgets, fuel, seed=0):
        self.runner, self.rng, self.size, self.budgets, self.fuel = runner, rng, size, budgets, fuel
        self.seed = seed % SEEDS  # the seed a generator binding draws from next (7.S1)
        # the literals of 7.S4's special values: the cutoffs the case has given so far (`_draw_case`)
        self.literals = ()

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

    def generate(self, generator, earlier, ty):
        """A value of `ty` from a binding's generator: applied to the earlier parameters it reads,
        the size and the current seed; the seed it gives back is the next draw's (7.S1). Invalid
        when the value is outside `ty` or the next seed is not a seed."""
        args = [earlier[n] for n in generator.reads] + [t.Lit(t.IntConst(self.size)), t.Lit(t.IntConst(self.seed))]
        pair = self.whnf(Runner.apply(t.Var(generator.called), args))
        if not isinstance(pair, t.Pair):
            raise RunError(f"the generator {generator.written} gave {_show(pair)}, not a value and a seed")
        following = self.whnf(pair.right)
        if not (isinstance(following, t.Lit) and isinstance(following.constant, t.IntConst)
                and 0 <= following.constant.value < SEEDS):
            raise Invalid(f"the generator {generator.written} gave {_show(following)} as the next seed (7.S1)")
        self.runner.fuel = self.fuel
        value = self.runner.value(pair.left)
        _, predicates = self.form(ty)
        if not self.holds(predicates, value):
            raise Invalid(f"the generator {generator.written} gave a value outside {_show(ty)} at seed "
                          f"{self.seed} (7.S1)")
        self.seed = following.constant.value
        return value

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
        if base == t.Var("Float64") and len(shape) == 2:
            array = self.degenerate(array)
        return self.runner.host_object(Entries(array), ty)

    def degenerate(self, array):
        """7.S5's zero and rank-deficient families given their share in a drawn matrix (D-2026-10-16-i,
        arrays.lth's `matDegeneracies`): the zero matrix with the budgets' `specialMass`, and with as
        much again (two rows or more) the last row made equal to the first (`rowsRepeatOrVanish`).
        [proposed] The special mass of a number read as the mass of each degenerate family of a
        matrix, until the budgets name one."""
        share = float(self.budgets.get("specialMass", 0.0))
        u = self.rng.random()
        if u < share:
            return np.zeros_like(array)
        if u < 2 * share and array.shape[0] >= 2:
            array = array.copy()
            array[-1, :] = array[0, :]
        return array

    def dimension(self, ty):
        """A dimension of a record (a field a later field's type reads, `m` of `Mat`) from 7.S5's
        census (generators.py's `DIMENSIONS`), those within the field's bounds and not above the
        size, that the field's type admits; None when none is, and the field is drawn as any."""
        base, predicates = self.form(ty)
        if base != t.Var("Int"):
            return None
        lo, hi = self.bounds(predicates, "Int")
        hi = self.size if hi is None else min(hi, self.size)
        allowed = [t.Lit(t.IntConst(d)) for d in generators.DIMENSIONS
                   if (lo is None or lo <= d) and d <= hi]
        allowed = [v for v in allowed if self.holds(predicates, v)]
        return allowed[self.rng.randrange(len(allowed))] if allowed else None

    def draw_base(self, ty, lo, hi, fixed=None):
        rng, n = self.rng, self.size
        if isinstance(ty, t.Var) and ty.name in ("Int", "Float64"):
            # 7.S3: the bounds of the type, otherwise [-s, s]; a missing side at s from the other
            lo = -n if lo is None else lo
            hi = (max(lo, 0) + n) if hi is None else hi
            if hi < lo:
                raise Unfit(f"an empty interval [{lo}, {hi}]")
            # 7.S4: the atom at 0 and the special values, with the budgets' masses (generators.py)
            integer = ty.name == "Int"
            v = generators.special(rng, lo, hi, integer, self.budgets.get("specialMass", 0.0),
                                   self.budgets.get("atomAtZero", 0.0), () if integer else self.literals)
            if v is not None:
                return t.Lit(t.IntConst(int(v)) if integer else t.FloatConst(float(v)))
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
                if v is None and any(_mentions(later, label) for _, later in types[k + 1:]):
                    v = self.dimension(fty)  # 7.S5: a dimension from its census
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


def generator_of(runner, name, law_parameters=()):
    """The binding's definition read as a generator (7.R1, 7.S1): its type, its leading arrows
    aside, is `Nat -> Seed -> T * Seed` (`Gen T` unfolded); the leading arrows are the law's
    earlier parameters it reads, by name (7.S7). None when it is not a generator (a census)."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == name), None)
    if definition is None or definition.type is None:
        return None
    arrows, ty = [], definition.type
    while (arrow := _arrow(ty)) is not None:
        arrows.append(arrow)
        ty = arrow[2]
    if len(arrows) < 2 or not isinstance(ty, t.Sigma) or _head_name(ty.codomain) != "Seed":
        return None
    if _head_name(arrows[-2][1]) not in ("Nat", "Int") or _head_name(arrows[-1][1]) != "Seed":
        return None
    reads = tuple(a[0] for a in arrows[:-2])
    unknown = [r for r in reads if law_parameters is not None and r not in law_parameters]
    if unknown:
        raise NoGenerator(f"the generator {name.partition('@')[0]} reads {', '.join(unknown)}, which the law "
                          f"does not quantify before this parameter (7.S7)")
    return Generator(name, name.partition("@")[0], reads)


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


def run_spec(runner, spec, fuel, loaded=None, start=None):
    """test.lth's `Tester.run`: the evidence of the law the spec names, with its verdict and grade.
    `start`, given the cutoffs and their parameter, is where a statistical law's stretch continues the
    test from (D-2026-10-16-g)."""
    law = _as_called(loaded, spec.law)
    params = parameters(runner, law)
    if params is None:
        return _not_run(spec, f"no definition {spec.law}")
    names = tuple(n for n, _ in params)
    if is_statistical(runner, law):
        return run_statistical(runner, spec, fuel, loaded, law, params, start)
    values = Values(runner, random.Random(spec.seed), spec.size, spec.budgets, fuel, spec.seed)
    limit = spec.budgets.get("coveringAbove", 20000)
    # each parameter: a census or a generator its binding names, or the mode's functor over its type
    con = _constructor(loaded)
    drawn = t.App(con("Drawn"), t.Lit(t.IntConst(spec.seed)))
    plan, coverage = [], (drawn if spec.sampled else con("Exhaustive"))
    try:
        for k, (name, ty) in enumerate(params):
            b = resolve_binding(spec, name, _head_name(ty))
            if b is None:
                plan.append(None)
                continue
            called = _as_called(loaded, b.generator)
            g = generator_of(runner, called, names[:k])
            if g is not None and not spec.sampled:
                raise NoGenerator(f"{name} is bound to the generator {b.generator}: ExhaustiveMode lists values, "
                                  f"a generator draws them (SampledMode)")
            plan.append(g if g is not None else census(runner, b, ty, called))
    except (NoGenerator, RunError) as exc:
        return _not_run(spec, str(exc), names, _spent(runner, fuel))
    for b in spec.where + spec.profile:  # test.lth's specCoverage: every binding weakens it
        # a generator's coverage is a draw from the spec's seed, whatever the binding says
        is_generator = _is_generator(runner, loaded, b)
        coverage = _weaker(_weaker(b.coverage, drawn) if is_generator else b.coverage, coverage)

    cases = []
    try:
        if not spec.sampled:
            cases = _every_case(values, params, plan, limit)
            if len(cases) > limit:
                return _not_run(spec, f"more than {limit} cases (coveringAbove); covering arrays are a later bite (7.R3)", names)
        else:
            # 7.S6: a draw that a filter cannot give within its tries makes the law not run
            cutoffs = tuple(k for k, (_, ty) in enumerate(params) if _base(ty) in CUTOFF_TYPES)
            cases = [_draw_case(values, params, plan, k, cutoffs) for k in range(spec.cases)]
    except (NoGenerator, Unfit, Invalid) as exc:
        return _not_run(spec, str(exc), names)
    except RunError as exc:
        return _not_run(spec, f"drawing the cases: {exc}", names, _spent(runner, fuel))

    points, raised, refuting, spent = [], [], None, None
    for case in cases:
        try:
            ok = evaluate(runner, law, case, fuel)
        except (RunError, RecursionError, ValueError, KeyError, TypeError) as exc:
            raised.append((case, str(exc) or type(exc).__name__))
            spent = spent or _spent(runner, fuel)
            continue
        points.append((case, ok))
        if not ok and refuting is None:
            refuting = case
    evidence = Points(points, coverage)
    # the regions of the cases evaluated, and the labels (D-2026-10-16-i, -j; `Classifier`)
    regions = labels = None
    if loaded is not None and points:
        try:
            found, named = Classifier(runner, loaded, values, params).classify([c for c, _ in points])
            regions, labels = regions_record(found), labels_record(named, len(points))
        except _RAISES:
            pass
    # laws.lth's ForallOnPoints; a case that raised settles nothing (its evidence is NotRun)
    if refuting is not None:
        verdict = "Refuted"
    elif raised:
        verdict = "Unsettled"
    else:
        verdict = "Confirmed" if _base(coverage) == "Exhaustive" else "Supported"
    # a refutation stands at any fuel; a run cut by its fuel otherwise settles nothing (D-2026-10-15-g)
    return Outcome(spec, evidence, verdict, grade_of(runner, verdict, coverage, loaded), len(points), refuting,
                   raised, names, out_of_fuel=spent if verdict != "Refuted" else None, regions=regions,
                   labels=labels)


# ---------------------------------------------------------------------- the regions (certification.lth §2)

# [proposed] The types of the cutoffs a law takes, the demand's (D-2026-10-14-c; D-2026-10-16-k item
# 20 makes per-law cutoffs typed fields of `Demand`, which will list them): a parameter of one gives
# the law's regions just above and just below it (D-2026-10-16-j, certification.lth's `lawRegions`).
CUTOFF_TYPES = ("Tolerance", "RankFloor", "Sequential")
# [proposed] How near a cutoff is "just above" or "just below": a number of the case within this
# factor of the cutoff, (c, c w] above and [c / w, c) below (generators.py's `specials` draws c w and
# c / w); and the factor a premise stated by a cutoff is read at to find its boundary.
CUTOFF_WIDTH = 2.0
_MOST_ENTRIES = 400  # [proposed] the entries of a matrix written as a function read for its numbers


def degeneracies_in(loaded):
    """The declarations of degenerate cases in the files loaded (generators.lth §9: a definition of
    type `Degeneracies T`), each (the name the program calls it, whether it is a label): a
    declaration in a theory or a model is its type's, shared by every law over it (D-2026-10-16-j,
    the first source); [proposed] one the test program makes is an author's label (7.S14's
    `classify`), recorded with its share and entering no grade (`ALabelEntersNoGrade`)."""
    if loaded is None:
        return []
    found = []
    for path, acts in loaded.by_file.items():
        for a in acts:
            if isinstance(a, s.Define) and a.type is not None and _surface_head(a.type) == "Degeneracies":
                found.append((a.name, path == loaded.top))
    return found


def _surface_head(ty):
    while isinstance(ty, s.App):
        ty = ty.function
    if isinstance(ty, s.Name):
        return ty.name.partition("@")[0]
    if isinstance(ty, s.PApp):
        return ty.name.partition("@")[0]
    return None


def _match(pattern, term, holes, found):
    """Whether `term` is `pattern` with its holes (the declaration's type parameters) filled, which
    `found` collects."""
    if isinstance(pattern, t.Var) and pattern.name in holes:
        if pattern.name in found:
            return found[pattern.name] == term
        found[pattern.name] = term
        return True
    if isinstance(pattern, t.App) and isinstance(term, t.App):
        return _match(pattern.function, term.function, holes, found) and _match(pattern.argument, term.argument, holes, found)
    return pattern == term


class Classifier:
    """The regions of a law's cases (D-2026-10-16-i, D-2026-10-16-j, L9.16; certification.lth §2,
    generators.lth §9; report-theory.md section 5, items 3, 4 and 9): from the type, each degenerate
    case its theory declares for a parameter's type (the most specific type in the chain a subtype
    unfolds to that has a declaration whose other parameters the law's give), counted by `casesOf`;
    from the law, the two sides of each cutoff parameter (`CUTOFF_TYPES`) and the boundary of each
    other parameter of a subtype (`lawRegions`). An author's labels (`degeneracies_in`) are counted
    apart and never grade. Branch coverage (the third source, item 5) is not in this bite.

    [proposed] The readings this bite chose, each the tester's and not yet a theory's:
    - a case is just above a cutoff `c` when a number of its other parameters (a scalar, an entry of
      a vector or a matrix), in absolute value, is in (c, c w], and just below when in [c / w, c),
      `w` the width; a cutoff of 0 has no sides, and gives no region;
    - the boundary of a premise stated by a cutoff (`PsdAt m fl`) is where its predicate holds at the
      cutoff and fails at the cutoff times w or divided by it; of a premise with bounds (`Nat`,
      `Fin n`, `Seed`), the bounds and their neighbours; of an exact premise (`Symmetric`), every case
      (the premise held, 7.S14);
    - a degenerate case of the type that no case met and whose witness is outside the parameter's
      type at every case is no region of the law (`SymmetricOf 3` and `0 x 0`)."""

    def __init__(self, runner, loaded, values, params, cutoff_types=CUTOFF_TYPES, width=CUTOFF_WIDTH):
        self.runner, self.values, self.params, self.width = runner, values, params, width
        self.cutoffs = [k for k, (_, ty) in enumerate(params) if _base(ty) in cutoff_types]
        self.cases_of = loaded.name(_GENERATORS_LTH, "casesOf") if loaded is not None else None
        defined = {a.name: a for a in runner.program if isinstance(a, t.Define)}
        self.declarations = []
        for name, label in degeneracies_in(loaded):
            d = defined.get(name)
            if d is None or self.cases_of is None:
                continue
            binders, ty = [], d.type
            while isinstance(ty, t.Pi):
                binders.append((ty.name, ty.domain))
                ty = ty.codomain
            if isinstance(ty, t.App) and _base(ty.function) == "Degeneracies":
                self.declarations.append((name, binders, ty.argument, label))

    # ---------------------------------------------------------- the type's cases
    def chain(self, ty):
        """The types a parameter's type unfolds to, the most specific first: itself, the type a
        subtype refines, a name's definition, a family applied."""
        out = []
        for _ in range(30):
            out.append(ty)
            if isinstance(ty, t.Subtype):
                ty = ty.type
            elif isinstance(ty, t.Var) and ty.name in self.runner.types and self.runner.types[ty.name] != ty:
                ty = self.runner.types[ty.name]
            elif (applied := self.runner.family_applied(ty)) is not None:
                ty = applied
            else:
                break
        return out

    def instance(self, k, ty, labels):
        """The declaration that classifies parameter `k` of type `ty`: (name, its arguments as a
        function of the case, T); labels instead, every one that matches. [] when none does."""
        out = []
        for element in self.chain(ty):
            for name, binders, declared, label in self.declarations:
                if label != labels:
                    continue
                holes = {b for b, dom in binders if isinstance(dom, t.Universe)}
                found = {}
                if not _match(declared, element, holes, found):
                    continue
                args, ok = [], True
                for b, dom in binders:
                    if b in holes:
                        if b not in found:
                            ok = False
                            break
                        args.append(("given", found[b]))
                        continue
                    head = _program_head(dom)
                    j = next((j for j, (_, pty) in enumerate(self.params)
                              if j != k and head is not None and _program_head(pty) == head), None)
                    # [proposed] a parameter no parameter of the law gives (the element of
                    # `listDegeneracies`' witness) stays a hole the predicates never read
                    args.append(("parameter", j) if j is not None else ("given", t.Var(f"%{b}")))
                if not ok:
                    continue
                out.append((name, args, element))
                if not labels:
                    return out
        return out

    def declared(self, instance, case):
        name, args, _ = instance
        values = [case[a] if kind == "parameter" else a for kind, a in args]
        return t.Proj(Runner.apply(t.Var(name), values), "cases")

    def names_in(self, instance, case, x):
        self.runner.fuel = self.values.fuel
        cs = self.declared(instance, case)
        found = _list(self.runner, Runner.apply(t.Var(self.cases_of), [instance[2], cs, x]))
        return [_text(self.runner.whnf(n)) for n in found]

    def cases_declared(self, instance, case):
        """(name, witness) of each case of the declaration."""
        self.runner.fuel = self.values.fuel
        out = []
        for c in _list(self.runner, self.declared(instance, case)):
            out.append((_text(self.runner.whnf(t.Proj(c, "name"))), t.Proj(c, "witness")))
        return out

    # ---------------------------------------------------------- the numbers of a value
    def numbers(self, v, out, budget=4000):
        """The doubles a value holds: a literal, the entries of a vector or a matrix (a host array, or
        a function on indices read entry by entry up to `_MOST_ENTRIES`), the parts of a pair, a
        record, an injection, a list."""
        if len(out) > budget:
            return out
        self.runner.fuel = self.values.fuel
        v = self.runner.whnf(v)
        if isinstance(v, t.Lit):
            if isinstance(v.constant, t.FloatConst):
                out.append(float(v.constant.value))
            return out
        obj = getattr(v, "obj", None)
        if obj is not None:
            array = getattr(obj, "array", obj)
            if isinstance(array, np.ndarray) and array.dtype.kind == "f":
                out.extend(float(x) for x in array.ravel()[:budget])
            return out
        if isinstance(v, t.RecordValue):
            fields = dict(v.fields)
            if "f" in fields and ("n" in fields):
                dims = [self.runner.whnf(fields[d]) for d in ("m", "n") if d in fields]
                if all(isinstance(d, t.Lit) and isinstance(d.constant, t.IntConst) for d in dims):
                    shape = [d.constant.value for d in dims]
                    f = self.runner.whnf(fields["f"])
                    if getattr(f, "obj", None) is not None:
                        return self.numbers(f, out, budget)
                    if int(np.prod(shape)) <= _MOST_ENTRIES:
                        for index in np.ndindex(*shape):
                            self.numbers(Runner.apply(f, [t.Lit(t.IntConst(int(i))) for i in index]), out, budget)
                    return out
            for _, x in v.fields:
                self.numbers(x, out, budget)
            return out
        if isinstance(v, t.Pair):
            self.numbers(v.left, out, budget)
            return self.numbers(v.right, out, budget)
        if isinstance(v, t.Inj):
            return self.numbers(v.value, out, budget)
        if isinstance(v, t.App) and isinstance(v.function, t.App) and _base(v.function.function) == "cons":
            self.numbers(v.function.argument, out, budget)
            return self.numbers(v.argument, out, budget)
        return out

    # ---------------------------------------------------------- the law's regions
    def sides(self, case):
        """The cutoffs' sides this case is in: {"c above", "c below"} by parameter name; and the
        names of the cutoffs that have sides (a cutoff of 0 has none)."""
        found, defined = set(), set()
        numbers = None
        for j in self.cutoffs:
            c = _number_of(self.runner, case[j])
            if c is None or c == 0.0:
                continue
            name = self.params[j][0]
            defined.add(name)
            if numbers is None:
                numbers = []
                for k, v in enumerate(case):
                    if k not in self.cutoffs:
                        try:
                            self.numbers(v, numbers)
                        except _RAISES:
                            pass
            c = abs(c)
            for x in numbers:
                x = abs(x)
                if c < x <= c * self.width:
                    found.add(f"{name} above")
                elif c / self.width <= x < c:
                    found.add(f"{name} below")
        return found, defined

    def premises(self):
        """The parameters of a subtype other than the cutoffs: (k, the cutoffs its type names)."""
        out = []
        for k, (name, ty) in enumerate(self.params):
            if k in self.cutoffs:
                continue
            try:
                _, predicates = self.values.form(ty)
            except _RAISES:
                continue
            if predicates:
                out.append((k, [j for j in self.cutoffs if j < k and _mentions(ty, self.params[j][0])]))
        return out

    def typed_at(self, k, case, replaced=None):
        """Parameter k's type with the earlier parameters' values put in (one replaced: (j, value))."""
        ty = self.params[k][1]
        for j, ((earlier, _), v) in enumerate(zip(self.params[:k], case)):
            if replaced is not None and replaced[0] == j:
                v = replaced[1]
            ty = _instantiate(earlier, v, ty)
        return ty

    def at_boundary(self, k, stated_by, case):
        v = case[k]
        ty = self.typed_at(k, case)
        if stated_by:
            for j in stated_by:
                c = _number_of(self.runner, case[j])
                if c is None:
                    continue
                for moved in (c * self.width, c / self.width):
                    _, predicates = self.values.form(self.typed_at(k, case, (j, t.Lit(t.FloatConst(moved)))))
                    if not self.values.holds(predicates, v):
                        return True
            return False
        base, predicates = self.values.form(ty)
        kind = base.name if isinstance(base, t.Var) else None
        if kind in ("Int", "Float64"):
            lo, hi = self.values.bounds(predicates, kind)
            if lo is not None or hi is not None:
                x = _number_of(self.runner, v)
                if x is None:
                    return False
                near = [n for b in (lo, hi) if b is not None for n in generators.neighbours(b, kind == "Int")]
                return any(x == n for n in near)
        return True  # an exact premise: the premise held (7.S14)

    # ---------------------------------------------------------- classify
    def classify(self, cases):
        """The grading regions with their cases, in order (the type's, then each cutoff's sides,
        then each premise's boundary), and the labels with theirs: ([(source, name, n)], [(name, n)])."""
        counts, labels = {}, {}
        order, label_order = [], []
        def add(key, into, order_, n=1):
            if key not in into:
                into[key] = 0
                order_.append(key)
            into[key] += n
        first = cases[0] if cases else None
        instances, label_instances = {}, {}
        if first is not None:
            for k in range(len(self.params)):
                try:
                    ty = self.typed_at(k, first)
                    instances[k] = self.instance(k, ty, labels=False)
                    label_instances[k] = self.instance(k, ty, labels=True)
                except _RAISES:
                    instances[k], label_instances[k] = [], []
        # every declared case is a region before any case is counted, with its witness to drop it by
        witnesses = {}
        for k, found in instances.items():
            for inst in found:
                try:
                    for name, w in self.cases_declared(inst, first):
                        add(("FromType", name), counts, order, 0)
                        witnesses.setdefault(name, []).append((k, w))
                except _RAISES:
                    pass
        for k, found in label_instances.items():
            for inst in found:
                try:
                    for name, _ in self.cases_declared(inst, first):
                        add(name, labels, label_order, 0)
                except _RAISES:
                    pass
        premises = self.premises()
        sided = set()
        if first is not None:
            for j in self.cutoffs:
                c = _number_of(self.runner, first[j])
                if c is not None and c != 0.0:
                    add(("FromLaw", f"{self.params[j][0]} above"), counts, order, 0)
                    add(("FromLaw", f"{self.params[j][0]} below"), counts, order, 0)
            for k, _ in premises:
                add(("FromLaw", f"{self.params[k][0]} boundary"), counts, order, 0)
        inside = {name: False for name in witnesses}  # a witness inside its parameter's type at some case
        for case in cases:
            met = set()
            for k, found in instances.items():
                for inst in found:
                    try:
                        met |= set(self.names_in(inst, case, case[k]))
                    except _RAISES:
                        pass
            for name in met:
                if ("FromType", name) in counts:
                    counts[("FromType", name)] += 1
            for k, found in label_instances.items():
                for inst in found:
                    try:
                        for name in set(self.names_in(inst, case, case[k])):
                            add(name, labels, label_order)
                    except _RAISES:
                        pass
            try:
                found_sides, _ = self.sides(case)
            except _RAISES:
                found_sides = set()
            for name in found_sides:
                if ("FromLaw", name) in counts:
                    counts[("FromLaw", name)] += 1
            for k, stated_by in premises:
                try:
                    if self.at_boundary(k, stated_by, case):
                        counts[("FromLaw", f"{self.params[k][0]} boundary")] += 1
                except _RAISES:
                    pass
            for name, ws in witnesses.items():
                if inside[name] or counts[("FromType", name)]:
                    continue
                for k, w in ws:
                    try:
                        _, predicates = self.values.form(self.typed_at(k, case))
                        self.runner.fuel = self.values.fuel
                        if self.values.holds(predicates, self.runner.value(w)):
                            inside[name] = True
                            break
                    except _RAISES:
                        inside[name] = True  # a witness that cannot be read is kept
                        break
        regions = [(source, name, counts[(source, name)]) for source, name in order
                   if not (source == "FromType" and counts[(source, name)] == 0 and not inside.get(name, True))]
        return regions, [(name, labels[name]) for name in label_order]


def regions_record(regions):
    """certification.lth's `RegionEvidence` as the entry keeps it (7.S9): each region with its n."""
    return [{"region": {"source": source, "name": name}, "n": n} for source, name, n in regions]


def labels_record(labels, evaluated):
    """An author's labels with their share of the cases evaluated (7.S14): informative, no grade."""
    return [{"label": name, "n": n, "share": (n / evaluated if evaluated else 0.0)} for name, n in labels]


def is_statistical(runner, law):
    """Whether the law's result type, past its parameters, is laws.lth's `Law` (a form a test runs
    as a whole: today `Statistical`), not a `Bool` evaluated case by case."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == law), None)
    if definition is None:
        return False
    ty = definition.type
    while isinstance(ty, t.Pi):
        ty = ty.codomain
    return _head_name(ty) == "Law"


_RAISES = (RunError, RecursionError, ValueError, KeyError, TypeError)


def run_statistical(runner, spec, fuel, loaded, law, params, start=None):
    """A statistical law at its bindings (laws.lth §4, L9.15): each parameter a census of one, the
    body reduced to `Statistical S T l draw c`, and `sequentialFrom S T l draw c seed r 0` run once
    through the Runner from the spec's seed, `r` and `k` the ratio and the samples `start` gives for
    these cutoffs (one and none when it gives nothing, which is `sequential`), and `ratioAfter`
    likewise for the ratio it stops at; the budget bounds the whole test (D-2026-10-16-g).
    The evidence is `Tested v`; the verdict `StatisticalByTest`'s; the grade test.lth's over
    `Drawn seed`."""
    names = tuple(n for n, _ in params)
    seed = spec.seed % SEEDS
    con = _constructor(loaded)
    values = Values(runner, random.Random(seed), spec.size, spec.budgets, fuel, seed)
    case = []
    for name, ty in params:
        for (earlier, _), v in zip(params, case):
            ty = _instantiate(earlier, v, ty)
        b = resolve_binding(spec, name, _head_name(ty))
        if b is None:
            if _head_name(ty) == "Sequential":
                return _not_run(spec, f"{name} : Sequential: the sequential test's cutoffs are the demand's and "
                                      f"never drawn; bind them as a census of one (D-2026-10-14-c, L9.15)", names)
            return _not_run(spec, f"{name} : {_show(ty)}: a statistical law runs once, at its bindings (L9.15); "
                                  f"bind it as a census of one", names)
        try:
            members = census(runner, b, ty, _as_called(loaded, b.generator))
        except (NoGenerator, RunError) as exc:
            return _not_run(spec, f"{name}: {exc}", names)
        if len(members) != 1:
            return _not_run(spec, f"{name}: a statistical law runs once per line (L9.15); the census "
                                  f"{b.generator} has {len(members)} values, bind one", names)
        case.append(members[0])
    try:
        runner.fuel = fuel
        form = runner.whnf(Runner.apply(t.Var(law), case))
        args, head = [], form
        while isinstance(head, t.App):
            args.insert(0, head.argument)
            head = head.function
        if _base(head) != "Statistical" or len(args) != 5:
            return _not_run(spec, f"the law gives {_show(form)} at its bindings; of the forms of a Law the tester "
                                  f"runs `Statistical` only (laws.lth §4)", names)
        if _base(args[1]) != "Seed":
            return _not_run(spec, f"the stream's state is {_show(args[1])}, not Seed: the seed is the test's "
                                  f"(L9.15)", names)
        cutoffs = runner.value(args[4])
        _, predicates = values.form(con("Sequential"))
        if not values.holds(predicates, cutoffs):
            return _not_run(spec, f"the cutoffs {_show(cutoffs)} break Sequential's predicate (laws.lth "
                                  f"`sequentialCutoffs`)", names)
        c = {label: v.constant.value for label, v in cutoffs.fields}
        parameter = next((n for n, ty in params if _head_name(ty) == "Sequential"), None)
        start = start(c, parameter) if start else None
        before = int(start["spent"]) if start else 0
        from_ratio = float(start["ratio"]) if start else 1.0
        stretch = args + [t.Lit(t.IntConst(seed)), t.Lit(t.FloatConst(from_ratio)), t.Lit(t.IntConst(before))]
        runner.fuel = fuel
        verdict = runner.value(Runner.apply(con("sequentialFrom"), stretch))
        runner.fuel = fuel
        stopped = runner.value(Runner.apply(con("ratioAfter"), stretch))
    except _RAISES as exc:
        return _not_run(spec, f"the sequential test raised: {exc or type(exc).__name__}", names, _spent(runner, fuel))
    if not (isinstance(verdict, t.App) and _base(verdict.function) in SETTLED_BY_TEST
            and isinstance(verdict.argument, t.RecordValue)):
        return _not_run(spec, f"the sequential test gave {_show(verdict)}, not a StatisticalVerdict", names)
    rates = {label: v.constant.value for label, v in verdict.argument.fields}
    coverage = t.App(con("Drawn"), t.Lit(t.IntConst(seed)))
    evidence = Tested(_base(verdict.function), float(rates["alpha"]), float(rates["beta"]), float(rates["delta"]),
                      int(rates["spent"]) - before, int(c["initial"]), int(c["budget"]), coverage,
                      float(stopped.constant.value), start, parameter)
    settled = SETTLED_BY_TEST[evidence.verdict]
    return Outcome(spec, evidence, settled, grade_of(runner, settled, coverage, loaded), evidence.spent, None,
                   parameters=names)


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
        if plan[k] is not None:
            _in_its_type(values, params[k], ty, v)
        out.extend(_every_case(values, params, plan, limit, prefix + (v,)))
        if len(out) > limit:
            break
    return out


def _draw_case(values, params, plan, walked, cutoffs=()):
    """One case: each parameter drawn, generated or walked in its census, in order. The numbers the
    cutoffs among the earlier parameters (`cutoffs`, their indices) have taken are the literals of
    7.S4's special values for the later ones (D-2026-10-16-j: the two sides of a cutoff given mass)."""
    case = []
    for k, (name, ty) in enumerate(params):
        for (earlier, _), v in zip(params, case):
            ty = _instantiate(earlier, v, ty)
        values.literals = tuple(x for j in cutoffs if j < k and (x := _number_of(values.runner, case[j])) is not None)
        # a census is walked in turn, each value once per round (generators.lth's `walk`, gen.10);
        # a generator draws from the seed it threads (7.S1)
        try:
            if isinstance(plan[k], Generator):
                case.append(values.generate(plan[k], {n: v for (n, _), v in zip(params, case)}, ty))
            elif plan[k] is not None:
                v = plan[k][walked % len(plan[k])]
                _in_its_type(values, params[k], ty, v)
                case.append(v)
            else:
                case.append(values.draw(ty))
        except (NoGenerator, Unfit, Invalid) as exc:
            raise type(exc)(f"{name} : {_show(params[k][1])}: {exc}") from exc
    values.literals = ()
    return tuple(case)


def _in_its_type(values, param, ty, v):
    """A census value checked against the predicate of its parameter's type, as a generator's is
    (7.S1; report-theory.md section 4, finding 1: a census bound to `r : GradingRegion` ran a label):
    Invalid otherwise, and the law is not run. Checked once per value when the type reads no
    earlier parameter."""
    key = (param[0], id(v)) if ty == param[1] else None
    checked = values.__dict__.setdefault("checked", {})
    if key is not None and checked.get(key) is v:
        return
    _, predicates = values.form(ty)
    if predicates and not values.holds(predicates, v):
        raise Invalid(f"the census gives {_show(v)}, a value outside {_show(ty)} (7.S1)")
    if key is not None:
        checked[key] = v


def _number_of(runner, v):
    """The number a value is (a census of one naming `1.0e-12`, a literal), or None."""
    try:
        runner.fuel = 10000
        w = runner.whnf(v)
    except _RAISES:
        return None
    if isinstance(w, t.Lit) and isinstance(w.constant, (t.IntConst, t.FloatConst)):
        return float(w.constant.value)
    return None


def _is_generator(runner, loaded, binding):
    """Whether the binding names a generator (by its type, `generator_of`) rather than a census."""
    try:
        return generator_of(runner, _as_called(loaded, binding.generator), None) is not None
    except NoGenerator:
        return True


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


def _not_run(spec, reason, names=(), out_of_fuel=None):
    return Outcome(spec, NotRun(reason), "NotRun", None, 0, None, parameters=names, out_of_fuel=out_of_fuel)


def _spent(runner, fuel):
    """The fuel given, when the Runner stopped with none left (its `fuel spent`, however a host or
    a message wrapped it), else None (D-2026-10-15-g)."""
    return fuel if runner.fuel <= 0 else None


# ---------------------------------------------------------------------- the command

_GRADE_WORDS = {"Proved": "proved", "ExhaustiveGrade": "exhaustive", "Cases": "cases", "Sampled": "sampled",
                "AssumedGrade": "assumed"}


def show_case(names, case):
    return ", ".join(f"{n} = {_show(v)}" for n, v in zip(names, case))


def control_passes(verdict):
    """test.lth's `controlPasses`: a control passes when its law is refuted on the broken model."""
    return verdict == "Refuted"


def passes(outcome):
    """Whether a line came out as asked: a law line with a grade, a control refuted."""
    return control_passes(outcome.verdict) if outcome.spec.control else outcome.grade is not None


_CONTROL_FAILED = "CONTROL FAILED: the law held on the model broken on purpose, too weak to see the break (7.S19)"


def _tail(outcome):
    """What the line settled: the grade, the refuting case, or why it settled nothing; for a
    control, whether it passed (its law refuted) or failed (its law held). A run cut by its fuel
    says so first, with the fuel it was given (D-2026-10-15-g)."""
    if outcome.out_of_fuel is not None:
        return f"fuel spent ({outcome.out_of_fuel} given; nothing stored, run again with more): " + _tail(
            replace(outcome, out_of_fuel=None))
    if isinstance(outcome.evidence, NotRun):
        return f"not run: {outcome.evidence.reason}"
    if isinstance(outcome.evidence, Tested):
        return _tested_tail(outcome)
    if outcome.spec.control and outcome.verdict == "Refuted":
        return f"refuted at {show_case(outcome.parameters, outcome.refuting)}: the control passed"
    if outcome.spec.control and outcome.grade is not None:
        return f"{_CONTROL_FAILED} ({_GRADE_WORDS.get(outcome.grade, outcome.grade)})"
    if outcome.verdict == "Refuted":
        return f"refuted at {show_case(outcome.parameters, outcome.refuting)}"
    if outcome.verdict == "Unsettled":
        case, message = outcome.raised[0]
        return (f"unsettled: {len(outcome.raised)} cases raised, the first at "
                f"{show_case(outcome.parameters, case)}: {message}")
    return _GRADE_WORDS.get(outcome.grade, outcome.grade)


def _tested_tail(outcome):
    """What a statistical line settled: the sequential test's verdict, its rates and what it spent."""
    rates = certify.tested_text(outcome.evidence.record())
    if outcome.evidence.start:  # a stretch that continued earlier ones (D-2026-10-16-g)
        rates += ", " + certify.continued_text(outcome.evidence.start, outcome.evidence.spent)
    if outcome.verdict == "Refuted":
        return f"refuted at {rates}" + (": the control passed" if outcome.spec.control else "")
    if outcome.verdict == "Unsettled":
        return f"unresolved at {rates}"
    grade = _GRADE_WORDS.get(outcome.grade, outcome.grade)
    if outcome.spec.control:
        return f"{_CONTROL_FAILED} ({grade}, held at {rates})"
    return f"supported, {grade}: held at {rates}"


def _entry_tail(entry):
    o = entry["outcome"]
    if o == "Passed":
        tested = (entry.get("evidence") or {}).get("Tested")
        grade = _GRADE_WORDS.get(entry["grade"], entry["grade"])
        if not tested:
            return grade
        start = entry["evidence"].get("from")
        more = f", {certify.continued_text(start, tested['spent'])}" if start else ""
        return f"supported, {grade}: held at {certify.tested_text(tested)}{more}"
    if "ControlRefuted" in o:
        return f"refuted at {o['ControlRefuted']}: the control passed"
    if "ControlConfirmed" in o:
        return f"{_CONTROL_FAILED} ({o['ControlConfirmed']})"
    if "Failed" in o:
        return f"refuted at {o['Failed']}"
    if "Unresolved" in o:
        return certify.show_outcome(o)
    return f"not run: {o['NotRunFor']}" if "NotRun" in entry["evidence"] else o["NotRunFor"]


def line(outcome):
    """One line per test: the law, the mode, the cases evaluated, the grade or the refuting case,
    and whether it ran or its outcome was known (7.S13)."""
    spec = outcome.spec
    mode = f"sampled (seed {spec.seed}, size {spec.size}, metric ignored)" if spec.sampled else "exhaustive"
    counted = f"{outcome.evaluated} cases"
    if isinstance(outcome.evidence, Tested) or "Tested" in (outcome.evidence if isinstance(outcome.evidence, dict) else {}):
        mode, counted = f"sequential (seed {spec.seed % SEEDS})", f"{outcome.evaluated} samples"
    head = f"{'control of ' if spec.control else ''}{spec.law}: {mode}, {counted}"
    if outcome.known is not None:
        tail = f"{head}, {_entry_tail(outcome.entry)} (known, {outcome.known}"
        if outcome.differs is not None:
            tail += f"; replay disagrees with the entry of {outcome.differs}, the law refused until resolved"
        return tail + ")"
    how = "ran"
    if outcome.stale is not None:
        how += f"; the entry of {outcome.stale} is stale, kept"
    if outcome.differs is not None:
        how += (f"; replay disagrees with the known entry of {outcome.differs}: both kept, the law refused "
                f"until a later run agrees (D-2026-10-15-f)")
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
    is looked up first in the store of the file that makes its claim (`claim_file`; a known outcome
    is reused unless `deep`) and each line run is recorded there, under its lock
    (certification.lth's `known` and `record`: an agreeing replay writes nothing, a disagreeing one
    is kept beside, D-2026-10-15-f; a run cut by its fuel is never written, D-2026-10-15-g); the test
    program's own store is neither read nor written. The file is a test program (`x.test.lut`,
    12.R2), refused otherwise before anything is read."""
    require_kind(path, "test")
    runner, specs, loaded = prepare(path, fuel)
    cones = certify.Cones(runner)
    stores = {}  # the file that makes a claim -> its store's entries, as read
    outcomes = []
    for spec in specs:
        if seed is not None:
            spec.seed = seed
        entry = new_entry(runner, loaded, spec, cones, fuel)
        home = claim_file(loaded, spec, runner)
        if home not in stores:
            stores[home] = certify.read_store(home) if store else []
        entries = stores[home]
        key = certify.identity(entry)
        found = certify.known(entries, key)
        if found is not None and not deep:
            evidence = found["evidence"]
            points = evidence.get("Points", {})
            verdict, evaluated = points.get("verdict", "NotRun"), points.get("evaluated", 0)
            if "Tested" in evidence:
                verdict = SETTLED_BY_TEST[evidence["Tested"]["verdict"]]
                evaluated = evidence["Tested"]["spent"]
            reused = Outcome(spec, evidence, verdict, found["grade"], evaluated, None, cone=entry["cone"],
                             entry=found, known=found["date"], store=home)
            if certify.disputed_at(entries, key):
                reused.differs = [e for e in entries if certify.identity(e) == key][1]["date"]
            outcomes.append(reused)
            continue
        # a statistical stretch continues the test of the law under its binding (D-2026-10-16-g)
        start = (lambda c, p, entry=entry, entries=entries: certify.continuation(entries, entry, c, p)) if store else None
        outcome = run_spec(runner, spec, fuel, loaded, start)
        settle(entry, outcome)
        outcome.cone, outcome.entry, outcome.store = entry["cone"], entry, home
        fuel_spent = certify.out_of_fuel(entry)
        if found is not None and not fuel_spent and not certify.agree(entry, found):
            outcome.differs = found["date"]
        old = next((e for e in entries if e["law"] == entry["law"] and e["binding"] == entry["binding"]
                    and certify.stale(entry["cone"], e)), None)
        if old is not None:
            outcome.stale = old["date"]
        outcomes.append(outcome)
        if store and not fuel_spent:
            certify.add_entry(home, entry)
            stores[home] = certify.read_store(home)
    return outcomes


def law_file(loaded, law):
    """The file that states the law a test line names: the one the test program sees by that name,
    else the one the loader calls by it (a control file may name a law it does not import), else
    the first file loaded that defines it."""
    try:
        found = loaded.see(loaded.top, law)
    except RunError:
        found = None
    if found is not None:
        return found[0]
    if law in loaded.plain:
        return loaded.plain[law]
    return next((p for p, f in loaded.files.items() if law in f.defined), loaded.top)


def _reached(loaded, path):
    """The files `path` imports, directly or through what it imports."""
    seen, todo = set(), [path]
    while todo:
        f = loaded.files.get(todo.pop())
        for target, _ in (f.imports.values() if f is not None else ()):
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return seen


def claim_file(loaded, spec, runner):
    """The file that makes the claim a line's entry certifies, whose store alone holds the entry
    (L10.12, D-2026-10-16-b): the file that defines the model of the library its binding names
    (`model_homes`), or, when it names none (a theory's own law tested on a census, a control on a
    model the test program breaks), the file that states the law. [proposed] When the binding names
    models of several files, the one that imports the others (a run that demands the law on all of
    them loads it), else the first; nothing is written in two stores."""
    homes = model_homes(loaded, spec, runner)
    for home in homes:
        reached = _reached(loaded, home)
        if all(other == home or other in reached for other in homes):
            return home
    if homes:
        return homes[0]
    return law_file(loaded, spec.law)


def model_homes(loaded, spec, runner=None):
    """[proposed, night default for decision 1 of report-run.md] The files, other than the test
    program and core, that define a model a binding of the line names (`numpy` in
    arrays_model.lut): the claim's file is one of them (`claim_file`), whose store a run of an
    importer reads (12.S11). [proposed, 2026-10-16, prompt-claim-store.md] A law the test program
    defines (a wrapper) on a model of the library has that model's file as its home too, so that the
    test program keeps no store; before, it had none and its entry stayed beside the test program.

    A model is a value whose type is the theory head of the parameter the binding binds (`numpy :
    Arrays` for `a : Arrays`, `listedHost : Host State` for `o : Host S`): the census the binding
    names, or each member of a census that is a list literal of names. A type alias (`State`,
    demand.lth's `Record`), a type (`UnitList`), a constructor (`Sampled`) or a census whose
    parameter's type is no theory head (`S : U`, `g : Grade`) is no model, and its file no home
    (report-e.md, finding 1)."""
    if loaded is None or runner is None:
        return []
    top = loaded.top
    homes = []
    for name, ty in parameters(runner, _as_called(loaded, spec.law)) or []:
        head = _program_head(ty)
        if head is None or not _theory_head(runner, head):
            continue
        b = resolve_binding(spec, name, _head_name(ty))
        # [proposed] a generator is not a model the law is certified on: its file is no home
        if b is None or _is_generator(runner, loaded, b):
            continue
        try:
            found = loaded.see(top, b.generator)
        except RunError:
            continue
        if found is None:
            continue
        # the census itself when it is a model, else each member of its list literal that is one
        # (`codecs : List Codec := [csv]`, csv in tables_model.lut) [proposed]
        candidates = [found] if _is_model(runner, loaded, found, head) else []
        for member in _list_members(loaded, found):
            try:
                there = loaded.see(found[0], member)
            except RunError:
                continue
            if there is not None and _is_model(runner, loaded, there, head):
                candidates.append(there)
        for f, _ in candidates:
            if f not in (top, loaded.core) and f not in homes:
                homes.append(f)
    return homes


def _program_head(ty):
    """The name at the head of a type as the program calls it (`Host` of `Host S`), or None."""
    while isinstance(ty, t.App):
        ty = ty.function
    return ty.name if isinstance(ty, t.Var) else None


def _theory_head(runner, name):
    """Whether `name` (as the program calls it) is a theory head: declared at a record, `Host (S :
    Concrete) : { ... }` (check.py's `theory_head`; its definition by laws, `Host (S : Concrete) :=
    HostAgreesPrint S & ...`, is not kept in a runner's program)."""
    declared = next((a for a in runner.program if isinstance(a, t.Declare) and a.name == name), None)
    if declared is None:
        return False
    ty = declared.type
    while isinstance(ty, t.Pi):
        ty = ty.codomain
    return isinstance(ty, t.Record)


def _is_model(runner, loaded, there, head):
    """Whether the name `there` (file, name) is a model of the theory `head`: its file defines it as
    a value (no alias, no constructor, no label of a sum) and its type's head is `head`."""
    file = loaded.files.get(there[0])
    if file is None or there[1] in file.constructors or loaded.is_label(*there):
        return False
    if not any(isinstance(a, s.Define) and a.name == there[1] for a in file.acts):
        return False
    called = loaded.internal(*there)
    d = next((a for a in runner.program if isinstance(a, t.Define) and a.name == called), None)
    return d is not None and _program_head(d.type) == head


def _listed_called(loaded, called):
    """The members of a census that is a list literal of names, as the program calls them."""
    if loaded is None:
        return []
    found = next(((f, n) for f in loaded.files for n in loaded.files[f].defined
                  if loaded.internal(f, n) == called), None)
    if found is None:
        return []
    out = []
    for member in _list_members(loaded, found):
        try:
            there = loaded.see(found[0], member)
        except RunError:
            return []
        if there is None:
            return []
        out.append(loaded.internal(*there))
    return out


def _list_members(loaded, found):
    """The names a definition's list literal body holds (`[csv, built]`), as the file that defines
    the census writes them; none when its body is anything else."""
    file = loaded.files.get(found[0])
    if file is None:
        return []
    for act in file.acts:
        if isinstance(act, s.Define) and act.name == found[1] and not act.binders:
            body = getattr(act.body, "term", None)
            if isinstance(body, s.List):
                return [v.name for v in body.values if isinstance(v, s.Name)]
    return []


def line_claims(path, fuel=1_000_000):
    """Each (law, control) the file's test lines name, the law as the file writes it, with the hash
    of the law's cone: [(law, cone, control)]; and the files whose stores hold the lines' entries
    (`claim_file`), each once, in the order of the lines."""
    runner, specs, loaded = prepare(path, fuel)
    cones = certify.Cones(runner)
    lines = [(law, cone, control) for (law, control), cone in
             {(spec.law, spec.control): cones.hash(_as_called(loaded, spec.law)) for spec in specs}.items()]
    return lines, list(dict.fromkeys(claim_file(loaded, spec, runner) for spec in specs))


def line_cones(path, fuel=1_000_000):
    """Each (law, control) the file's test lines name, with the hash of the law's cone (`line_claims`)."""
    return line_claims(path, fuel)[0]


def law_cones(path, fuel=1_000_000, control=False):
    """Each law the file's test lines name, as the file writes it, with the hash of its cone; with
    `control`, the laws its control lines name instead."""
    return [(law, cone) for law, cone, c in line_cones(path, fuel) if c == control]


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
    coverage, its fingerprint the hash of the census's cone; or the generator its binding names
    (bite 3), printed with the parameters it reads and the size, its fingerprint the hash of its
    cone (7.S9: a name with its fingerprint), no reach (a draw lists no values); otherwise the mode's functor over the
    parameter's type, printed with the metric and the size, its fingerprint empty (the drawing code
    is the interpreter's, in the cone's hash). The reach: a census's members; the support of the
    type under ExhaustiveMode; under SampledMode, for an `Int` or a `Float64` (refined or not, not
    dependent on an earlier parameter), the interval it is drawn from; no reach otherwise, which
    covers no value a run gives (certification.lth's `coversAll`)."""
    law = _as_called(loaded, spec.law)
    params = parameters(runner, law) or []
    statistical = is_statistical(runner, law)  # its bindings are censuses of one, a stream among them
    values = Values(runner, random.Random(0), spec.size, spec.budgets, fuel)
    binding, reach, hosts = [], [], dict(cones.hosts(law))
    for k, (name, ty) in enumerate(params):
        b = resolve_binding(spec, name, _head_name(ty))
        if b is not None:
            called = _as_called(loaded, b.generator)
            try:
                g = None if statistical else generator_of(runner, called, None)
            except NoGenerator:
                g = None
            if g is not None:
                reads = "".join(f" {r}" for r in g.reads)
                binding.append({"parameter": name, "generator": f"{b.generator}{reads} (generator, size {spec.size})",
                                "fingerprint": cones.hash(called)})
                hosts.update(cones.hosts(called))
                continue
            # a census that lists models: the hashes of its members, comma-joined, so that a run
            # naming one model finds its own hash there (`at` in certify.py) [proposed]
            listed = _listed_called(loaded, called)
            binding.append({"parameter": name, "generator": f"{b.generator} ({_show(b.coverage)})",
                            "fingerprint": ",".join(cones.hash(m) for m in listed) if listed else cones.hash(called)})
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
    entry = {"law": spec.law, "cone": cones.hash(law), "binding": binding, "seed": spec.seed, "cases": spec.cases,
             "budgets": dict(spec.budgets), "reach": reach, "evidence": None, "grade": None, "outcome": None,
             "date": certify.now(), "interpreter": certify.interpreter_revision(),
             "hosts": [[r, h] for r, h in sorted(hosts.items())]}
    if spec.control:
        entry["kind"] = certify.CONTROL  # its own kind, part of its identity (certify.identity)
    return entry


def settle(entry, outcome):
    """The entry's evidence, grade and outcome from the line's: passed with its grade; failed at
    the refuting case; not run with its reason, or unsettled with the first case that raised. A
    control's entry has no grade, and its outcome is `ControlRefuted` or `ControlConfirmed`. A run
    cut by its fuel is `NotRunFor "fuel spent"`, which the store never takes (D-2026-10-15-g)."""
    if outcome.out_of_fuel is not None:
        settle(entry, replace(outcome, out_of_fuel=None))
        entry["outcome"], entry["grade"] = {"NotRunFor": certify.FUEL_SPENT}, None
        return entry
    if isinstance(outcome.evidence, NotRun):
        entry["evidence"] = {"NotRun": outcome.evidence.reason}
        entry["outcome"] = {"NotRunFor": outcome.evidence.reason}
        return entry
    if isinstance(outcome.evidence, Tested):
        return _settle_tested(entry, outcome)
    entry["evidence"] = {"Points": {"evaluated": outcome.evaluated, "raised": len(outcome.raised),
                                    "coverage": _show(outcome.evidence.coverage), "verdict": outcome.verdict}}
    # 7.S9: the entry records its regions and its labels (certification.lth's `RegionEvidence`)
    if outcome.regions is not None:
        entry["regions"] = outcome.regions
    if outcome.labels:
        entry["labels"] = outcome.labels
    if outcome.spec.control:
        # a control's outcome: refuted is the control passing, a grade the control failing; neither
        # is the law's grade nor its failure (7.S19, D-2026-10-15-a)
        if control_passes(outcome.verdict):
            entry["outcome"] = {"ControlRefuted": show_case(outcome.parameters, outcome.refuting)}
        elif outcome.grade is not None:
            entry["outcome"] = {"ControlConfirmed": _GRADE_WORDS.get(outcome.grade, outcome.grade)}
        else:
            entry["outcome"] = {"NotRunFor": _tail(outcome)}
        return entry
    if outcome.verdict == "Refuted":
        entry["outcome"] = {"Failed": show_case(outcome.parameters, outcome.refuting)}
    elif outcome.grade is not None:
        entry["outcome"], entry["grade"] = "Passed", outcome.grade
    else:
        entry["outcome"] = {"NotRunFor": _tail(outcome)}
    return entry


def _settle_tested(entry, outcome):
    """A statistical line's entry (7.S17: the verdict carries its error rates into the certificate):
    the evidence `Tested` with alpha, beta, delta, the samples spent, the cutoffs' `initial` and
    `budget`, and the coverage; passed with its grade when the test held the law, failed when it
    failed it, `NotRunFor` an unresolved test (it settles nothing, laws.lth `StatisticalByTest`). A
    control's outcome is `ControlRefuted` when the test failed the law, `ControlConfirmed` when it
    held it."""
    tested = outcome.evidence.record()
    entry["evidence"] = {"Tested": tested, "coverage": _show(outcome.evidence.coverage)}
    if outcome.evidence.ratio is not None:  # where the stretch stopped and started (D-2026-10-16-g)
        entry["evidence"]["ratio"] = outcome.evidence.ratio
    if outcome.evidence.cutoffs is not None:
        entry["evidence"]["cutoffs"] = outcome.evidence.cutoffs
    if outcome.evidence.start:
        entry["evidence"]["from"] = outcome.evidence.start
    rates = certify.tested_text(tested)
    if outcome.verdict == "Refuted":
        entry["outcome"] = {"ControlRefuted" if outcome.spec.control else "Failed": rates}
    elif outcome.verdict == "Unsettled":
        entry["outcome"] = {"Unresolved": tested}
    elif outcome.spec.control:
        entry["outcome"] = {"ControlConfirmed": f"{_GRADE_WORDS.get(outcome.grade, outcome.grade)}, held at {rates}"}
    else:
        entry["outcome"], entry["grade"] = "Passed", outcome.grade
    return entry
