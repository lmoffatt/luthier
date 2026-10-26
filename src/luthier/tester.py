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

Not in this bite (each says so where it applies): the placement of `SampledMode` (draws are uniform
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

Of the budgets (7.S8) `tries`, `coveringAbove`, `fuel`, the two masses and the region classifier's
two bounds (`regionNumbers`, `regionEntries`) are read, each from the
line's `Budgets` (test.lth's `defaultBudgets` unless the line gives its own), none held here: a draw a
filter cannot give within `tries` makes the law not run (7.S6), so `drawsPerCase` and `redraws` have
nothing to bound yet; `fuel` is the reduction steps a case or a draw may take, which `fuel` given to
`run_tests` (`--fuel`) overrides for a run, and the entry's budgets record the fuel the line ran
with (the core's budgets brief, 2026-10-18). A case
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

import functools
import hashlib
import inspect
import json
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
    placement: t.Term | None
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


@dataclass
class Vacuous:
    """laws.lth's `Vacuous n` (wave A, bite A3; D-2026-10-16-m): `evaluated` cases evaluated, in none
    of which every premise the law states by `then` or by `if p then q else true` held."""
    evaluated: int


@dataclass
class AssumedAxiom:
    """laws.lth's `Assumed` for a law whose body is an axiom (11.R3, `FailuresIndependent`): no case
    runs, the grade is assumed (test.lth's `grade Assumes`), and the statement is kept in the entry
    (`"axiom"`). [bite of prompt-b1-b3-d1.md, item 4; report-B2.md's question, answered yes by the
    coordinator] As run.py's `axioms` accepts such a law at the demand's price for assumptions, so a
    conjunction with an axiom conjunct (`IndependentComposition`) is a line graded assumed rather than
    one left unsettled."""
    statement: str


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
    conjunct: str | None = None  # the conjunct this outcome is of, or the one a conjunction's refutation names
    parts: list | None = None    # a conjunction's line: the outcomes of its conjuncts (D-2026-10-18-f)
    law_store: object = None     # the file that states the line's law (`law_file`), whose store holds its controls
    held: int | None = None      # the cases in which every premise held, when the law states one (`premises_of`)
    measured: dict | None = None  # a numerical law's worst ratio, overall and per region (`measured_record`, bite C1)
    heads: dict | None = None    # a conjunction's: per conjunct, the law it applies and its cone (`conjunct_heads`, bite D1)


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
    # [bite A3] `p -> q` of Bools elaborates to core's `implies`, which no name of the source writes, so
    # the slice dropped it and such a law gave `implies ...`, no Bool
    implication = tuple(n for n in [loaded.name(loaded.core, "implies")] if n) if loaded.core is not None else ()
    roots = (core_data(loaded) + implication + tuple(d.name for d in specs) + named
             + tuple(loaded.name(top, n) or n for n in extra) + grading + regioning)
    kept = runtime_slice(loaded.acts + specs, specs[0].name if specs else "main", roots, theory_laws=True)
    loaded.demand(kept)
    program = tuple(_primitive_body(a) for a in elaborate_program(_refined_records(kept)))
    program += tuple(t.Define(op, t.Universe(), t.Primitive(op)) for op in kernel.BOOTSTRAP_PRIMITIVES)
    # the conjuncts of a law that is a conjunction, each a definition the tester runs (D-2026-10-18-f)
    program += conjunct_definitions(program, named + tuple(loaded.name(top, n) or n for n in extra))
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
        sampled, placement = False, None
    elif isinstance(mode, t.App) and _base(mode) == "SampledMode":
        sampled, placement = True, mode.argument
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
    return Spec(_text(record["law"]), sampled, placement, _int(record["cases"]), _int(record["size"]),
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
            # A theory's record is its type view; its definition is a predicate used as a value.
            # Retaining bare predicates for law expansion must not make model generation try
            # to draw a conjunction of functions (IntegerDivision exposed this).
            head, args = _spine(ty)
            declared = self.runner.types.get(head.name) if isinstance(head, t.Var) else None
            for arg in args:
                if not isinstance(declared, t.Pi):
                    declared = None
                    break
                declared = _instantiate(declared.name, arg, declared.codomain)
            if isinstance(declared, t.Record):
                ty = declared
            else:
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
        for _ in range(self.budgets["tries"]):
            v = self.draw_base(base, lo, hi, fixed)
            if self.holds(predicates, v):
                return v
        raise Unfit(f"no value of {_show(ty)} in {self.budgets['tries']} tries (7.S6)")

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
        share = float(self.budgets["specialMass"])
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
            v = generators.special(rng, lo, hi, integer, self.budgets["specialMass"],
                                   self.budgets["atomAtZero"], () if integer else self.literals)
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
            if not ty.constructors:
                raise NoGenerator(f"{ty.name} is empty: ExhaustiveMode certifies its absence of cases")
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


def fixed_carrier(runner, law, params):
    """The parameters a structure's laws fix (4.R6, the coordinator's (a) of 2026-10-22): the law (or
    a conjunct of it) is a structure `S (F : U) (d : S Float64) := ...` whose model is typed by `S` at
    arguments that are not its parameters, so `F` is `Float64`: {name: value}; {} otherwise."""
    base = law.split(_CONJUNCT)[0]
    declared = next((a for a in runner.program if isinstance(a, t.Declare) and a.name == base), None)
    if declared is None:
        return {}
    k, ty = 0, declared.type
    while isinstance(ty, t.Pi):
        k, ty = k + 1, ty.codomain
    if not (k and isinstance(ty, t.Record) and len(params) > k):
        return {}
    head, args = params[k][1], []
    while isinstance(head, t.App):
        args.append(head.argument); head = head.function
    names = {n for n, _ in params[:k]}
    if head != t.Var(base) or len(args) != k or any(names & set(kernel.free_names(a)) for a in args):
        return {}
    return {n: a for (n, _), a in zip(params[:k], reversed(args))}


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
    """The law's verdict at the case. A numerical law (laws.lth §5, bite C1) gives a `Law` at each
    case: `Within A d bound a b`, held when `d a b <= bound`, the case with its distance and bound
    appended to the runner's `MEASURES` list when `run_measured` set one; or `Case b` outside its
    range, held as `b`, with nothing measured. [proposed] The measures pass by the runner and not by an
    argument so that `run_spec`, part of the drawing code whose source is every sampled entry's
    fingerprint (`drawing_revision`), keeps its text: a numerical law changes no draw."""
    measured = getattr(runner, MEASURES, None)
    runner.fuel = fuel
    r = runner.whnf(Runner.apply(t.Var(law), list(case)))
    while True:
        if r == TRUE:
            return True
        if r == FALSE:
            return False
        head, args = _spine(r)
        if isinstance(head, t.Var) and _base(head) == "Case" and len(args) == 1:
            r = runner.whnf(args[0])
            continue
        if isinstance(head, t.Var) and _base(head) == "Within" and len(args) == 5:
            _, d, bound, a, b = args
            distance = _float_value(runner, Runner.apply(d, [a, b]))
            w = _float_value(runner, bound)
            if measured is not None:
                measured.append((case, distance, w))
            return distance <= w
        raise RunError(f"the law gave {_show(r)}, not a Bool")


def _float_value(runner, term):
    v = runner.value(term)
    if not (isinstance(v, t.Lit) and isinstance(v.constant.value, (int, float))):
        raise RunError(f"a numerical law's distance or bound gave {_show(v)}, not a Float64")
    return float(v.constant.value)


def ratio_of(distance, bound):
    """laws.lth's `ratioOf`: zero for a distance of zero whatever the bound, None (unbounded) for a
    positive distance at a bound of zero or below, else the quotient."""
    if distance == 0.0:
        return 0.0
    if bound <= 0.0:
        return None
    return distance / bound


def worse_ratio(r, s):
    """laws.lth's `worseRatio`: the larger, an unbounded one (None) worst."""
    if r is None or s is None:
        return None
    return r if r >= s else s


MEASURES = "within_measures"  # the runner's attribute `evaluate` appends a numerical law's measures to


def run_measured(runner, spec, fuel, loaded=None, start=None):
    """`run_spec`, and for a numerical law (laws.lth §5) its measures: the worst ratio overall and per
    region (`measured_record`) in the outcome's `measured`."""
    law = _as_called(loaded, spec.law)
    if not is_within(runner, law):
        return run_spec(runner, spec, fuel, loaded, start)
    setattr(runner, MEASURES, [])
    try:
        outcome = run_spec(runner, spec, fuel, loaded, start)
        measures = getattr(runner, MEASURES)
    finally:
        delattr(runner, MEASURES)
    if not isinstance(outcome.evidence, Points):
        return outcome
    points = outcome.evidence.cases
    members = _case_regions(runner, loaded, spec, law, fuel, [c for c, _ in points]) if outcome.regions else None
    return replace(outcome, measured=measured_record(measures, points, members, outcome.regions))


def _case_regions(runner, loaded, spec, law, fuel, cases):
    """The regions each case is counted in, as `run_spec` classifies them (its `Classifier`, with the
    parameters bound to a census fixed and those bound to one value single); None when the
    classification raises."""
    params = parameters(runner, law) or []
    names = tuple(n for n, _ in params)
    carried = fixed_carrier(runner, law, params)
    fixed, single = [], []
    try:
        for k, (name, ty) in enumerate(params):
            if name in carried:
                fixed.append(k)
                single.append(k)
                continue
            b = resolve_binding(spec, name, _head_name(ty))
            if b is None:
                continue
            called = _as_called(loaded, b.generator)
            if generator_of(runner, called, names[:k]) is not None:
                continue
            fixed.append(k)
            if len(census(runner, b, ty, called)) == 1:
                single.append(k)
        values = Values(runner, random.Random(spec.seed), spec.size, spec.budgets, fuel, spec.seed)
        members = []
        Classifier(runner, loaded, values, params, fixed=fixed, single=single).classify(cases, members)
        return members
    except (NoGenerator, *_RAISES):
        return None


def axiom_of(runner, law):
    """The statement of the `axiom` the law's body is, through the definitions its body applies (a
    conjunct `L%conjunct1` applies `FailuresIndependent`, whose body is the axiom), as run.py's
    `axiom_of` reads the surface; None when it is no axiom."""
    defined = {}
    for a in runner.program:
        if isinstance(a, t.Define):
            defined.setdefault(a.name, a)
    name = law
    for _ in range(UNFOLD):
        d = defined.get(name)
        if d is None:
            return None
        body = d.body
        while isinstance(body, t.Lam):
            body = body.body
        if type(body) is t.Axiom:
            return body.text
        head, args = _spine(body)
        # the elaborated `axiom "..."` (run.py's `_FREE`): the name applied to its statement
        if (isinstance(head, t.Var) and head.name.partition("@")[0] == "axiom" and len(args) == 1
                and isinstance(args[0], t.Lit) and isinstance(args[0].constant, t.StringConst)):
            return args[0].constant.value
        if not isinstance(head, t.Var):
            return None
        name = head.name
    return None


def assumed(spec, statement):
    """The outcome of a line on an axiom (`AssumedAxiom`): graded assumed with no case, or, for a
    control, not run, since no broken model can refute what no case checks."""
    if spec.control:
        return _not_run(spec, f"an axiom, assumed and never run, which no broken model refutes: {statement}")
    return Outcome(spec, AssumedAxiom(statement), "Assumes", "AssumedGrade", 0, None)


def is_within(runner, law):
    """Whether the law is a numerical law (laws.lth §5): its result is a `Law` and its body, as
    written, applies `Within`; it runs case by case as a `Bool` law does, each case measured."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == law), None)
    return (definition is not None and _law_typed(definition.type)
            and _applies(runner, definition.body, "Within", set()))


def _applies(runner, term, name, seen, depth=0):
    """Whether `term` mentions the constructor `name`, through the definitions it applies up to UNFOLD
    deep (a conjunct is the law it applies)."""
    if _mentions_base(term, name):
        return True
    if depth >= UNFOLD:
        return False
    for free in kernel.free_names(term):
        if free in seen:
            continue
        seen.add(free)
        d = next((a for a in runner.program if isinstance(a, t.Define) and a.name == free), None)
        if d is not None and _law_typed(d.type) and _applies(runner, d.body, name, seen, depth + 1):
            return True
    return False


def _mentions_base(term, name):
    """`_mentions` of a name however a clash qualified it (`Within@...`)."""
    if isinstance(term, t.Var):
        return term.name.partition("@")[0] == name
    if isinstance(term, tuple):
        return any(_mentions_base(x, name) for x in term)
    if is_dataclass(term) and not isinstance(term, type):
        return any(_mentions_base(getattr(term, f.name), name) for f in fields(term))
    return False


def _law_typed(ty):
    while isinstance(ty, t.Pi):
        ty = ty.codomain
    return _head_name(ty) == "Law"


# ---------------------------------------------------------------------- a conjunction of laws (D-2026-10-18-f)

# A law whose body is a conjunction `&` of partially applied laws (`Equivalence A r := Reflexive A r &
# Symmetric A r & Transitive A r`) is no Bool the kernel reduces (report-bite-2.md): it is tested
# conjunct by conjunct (the core's bite 4b, record/plan/core-2026-10-17/prompt-bite-4b.md). Each
# conjunct is a law of its own, its parameters the conjunction's and then the variables it leaves
# missing (`x` of `Reflexive A r`, `p` of `Symmetric A r`), each quantified on its own by the
# generators of its type, bound by name as any parameter (7.R1). A conjunct that is itself a law whose
# body is a conjunction (`Preorder A r` in `PartialOrder`) is split in turn. The tester runs conjunct k
# of the law `L` as the definition `L%conjunct<k>`, which `load_program` adds to the program; it is in
# no cone but its own, so no other name's hash moves.

_CONJUNCT = "%conjunct"


@dataclass
class Conjunct:
    """A conjunct of a law: the definition the tester runs it as, and the conjunct as the law
    applies it, the conjunction's parameters free (`Reflexive Int r`)."""
    called: str
    shown: str


def _spine(term):
    """The head of an application and its arguments, in order."""
    args = []
    while isinstance(term, t.App):
        args.append(term.argument)
        term = term.function
    return term, args[::-1]


def _is_conjunction(term):
    return isinstance(term, t.App) and isinstance(term.function, t.App) and term.function.function == t.Var("&")


def _parts(defined, term, depth=0, theories=frozenset()):
    """Split bare laws, including a conjunction applied pointwise to its shared model.

    A declared theory's record describes its models, not the missing variables of its law.
    Unfold its predicate until the leaves name the actual properties (7.S22).
    """
    if depth > len(defined):
        return None
    if _is_conjunction(term):
        out = []
        for side in (term.function.argument, term.argument):
            out += _parts(defined, side, depth + 1, theories) or [side]
        return out
    head, args = _spine(term)
    if head == t.Var("&") and len(args) > 2:
        out = []
        for side in args[:2]:
            applied = Runner.apply(side, args[2:])
            out += _parts(defined, applied, depth + 1, theories) or [applied]
        return out
    d = defined.get(head.name) if isinstance(head, t.Var) else None
    if d is None or (not args and isinstance(d.body, t.Lam)):
        return None
    body = d.body
    for k, arg in enumerate(args):
        if isinstance(body, t.Lam):
            body = kernel.substitute(body.name, arg, body.body)
        elif _is_conjunction(body):
            out = []
            for side in (body.function.argument, body.argument):
                applied = Runner.apply(side, args[k:])
                out += _parts(defined, applied, depth + 1, theories) or [applied]
            return out
        else:
            body = t.App(body, arg)
    if isinstance(body, t.Lam):
        return None
    parts = _parts(defined, body, depth + 1, theories)
    return parts if parts is not None else [body] if head.name in theories else None


def _missing(defined, term, used):
    """The variables a conjunct leaves missing, (name, type), from the type of the law at its head
    with the arguments given; each renamed apart from `used` (the conjunction's parameters and the
    conjunct's free names) and from the others."""
    head, args = _spine(term)
    d = defined.get(head.name) if isinstance(head, t.Var) else None
    out = []
    if d is not None and d.type is not None:
        ty = d.type
        for a in args:
            if not isinstance(ty, t.Pi):
                return out
            ty = _instantiate(ty.name, a, ty.codomain)
        while isinstance(ty, t.Pi):
            name = ty.name if ty.name != "_" else "x"
            while name in used:
                name += "'"
            used.add(name)
            out.append((name, ty.domain))
            ty = ty.codomain if name == ty.name else kernel.substitute(ty.name, t.Var(name), ty.codomain)
    return out


def conjunction_parts(program, law):
    """The conjuncts of the law `law` (as the program calls it) whose body is a conjunction of
    partially applied laws: [(the definition's type, its body, the conjunct)], each definition taking
    the law's parameters and then the conjunct's missing variables; None when the law is no
    conjunction."""
    defined = {}
    for a in program:
        if isinstance(a, t.Define):
            defined.setdefault(a.name, a)
    d = defined.get(law)
    if d is None or _CONJUNCT in law:
        return None
    params, body = [], d.body
    while isinstance(body, t.Lam):
        params.append((body.name, body.type))
        body = body.body
    theories = set()
    for act in program:
        if isinstance(act, t.Declare):
            ty = act.type
            while isinstance(ty, t.Pi):
                ty = ty.codomain
            if isinstance(ty, t.Record):
                theories.add(act.name)
    parts = _parts(defined, body, theories=theories)
    if parts is None:
        return None
    out = []
    for part in parts:
        used = {n for n, _ in params} | set(kernel.free_names(part))
        missing = _missing(defined, part, used)
        ty, value = t.Var("Bool"), Runner.apply(part, [t.Var(n) for n, _ in missing])
        for name, domain in reversed(params + missing):
            ty, value = t.Pi(name, domain, ty), t.Lam(name, domain, value)
        out.append((ty, value, part))
    return out


def conjunct_definitions(program, laws):
    """The definitions the conjuncts of the laws among `laws` run as (`L%conjunct<k>`)."""
    out = []
    defined = {}
    for a in program:
        if isinstance(a, t.Define):
            defined.setdefault(a.name, a)
    for law in dict.fromkeys(laws):
        for k, (ty, value, part) in enumerate(conjunction_parts(program, law) or ()):
            out.append(t.Define(f"{law}{_CONJUNCT}{k}", _numerical(defined, part, ty), value))
    return tuple(out)


def _numerical(defined, part, ty):
    """[bite C1] A conjunct that is a numerical law (laws.lth §5) keeps its result type, `Law`, so that
    the tester measures it: the `Bool` at the end of `ty` becomes `Law` when the law the conjunct
    applies gives a `Law` and applies `Within`; any other conjunct's type is `ty` as it was."""
    head, _ = _spine(part)
    d = defined.get(head.name) if isinstance(head, t.Var) else None
    if d is None or not _law_typed(d.type) or not _mentions_base(d.body, "Within"):
        return ty
    if isinstance(ty, t.Pi):
        return t.Pi(ty.name, ty.domain, _numerical(defined, part, ty.codomain))
    return t.Var("Law")


def _shown_conjunct(part):
    """A conjunct as its law applies it, `Reflexive Int r`, a compound argument in parentheses."""
    head, args = _spine(part)
    shown = [_show(head)]
    for a in args:
        text = _show(a)
        shown.append(f"({text})" if " " in text and not text.startswith(("(", "[", "{")) else text)
    return " ".join(shown)


def conjuncts_of(runner, law):
    """The conjuncts of the law (as the program calls it), in the order written; [] when it is no
    conjunction."""
    return [Conjunct(f"{law}{_CONJUNCT}{k}", _shown_conjunct(part))
            for k, (_, _, part) in enumerate(conjunction_parts(runner.program, law) or ())]


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
    limit = spec.budgets["coveringAbove"]
    # each parameter: a census or a generator its binding names, or the mode's functor over its type
    con = _constructor(loaded)
    drawn = t.App(con("Drawn"), t.Lit(t.IntConst(spec.seed)))
    plan, coverage = [], (drawn if spec.sampled else con("Exhaustive"))
    fixed = fixed_carrier(runner, law, params)
    try:
        for k, (name, ty) in enumerate(params):
            if name in fixed:
                plan.append([fixed[name]])
                continue
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
            cutoffs = tuple(k for k, (_, ty) in enumerate(params) if is_cutoff(runner, ty))
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
            fixed = [k for k, p in enumerate(plan) if isinstance(p, list)]  # bound to a census, not drawn
            single = [k for k in fixed if len(plan[k]) == 1]  # bound to one value: the law is claimed there only
            found, named = Classifier(runner, loaded, values, params, fixed=fixed,
                                      single=single).classify([c for c, _ in points])
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


# ---------------------------------------------------------------------- vacuity and the empty experiment

# [wave A, bite A3; record/plan/audit-algebras-2026-10-22/execution.md; the audit of 2026-10-22,
# section 12 "Vacuity, empty evidence and uncovered regions" (report.md, 5b1a05e)] A premise stated as a
# subtype (`c : Chain A r`) is met by every case drawn, and the regions count it (`Classifier`). One
# stated in the law's body is not: `p -> q` (`implies`, L12.7: `then` is material), `if p then q else
# true` or `q or not p` (bite A3b), at the top of the body, under its lets (`{ r := ... ; if
# r.converged then ... else true }`), or in the body of a law it applies, unfolded. Such a law held at every case where `p` was false, so with
# `p` never true it passed with no evidence. `judged` counts the cases where every premise held; none
# is laws.lth's `Vacuous n`, not run with the count as its reason (D-2026-10-16-m), never a pass. A run
# that evaluated no case and raised none is an empty experiment, not run with its reason (7.S12;
# test.lth's `CountsCases`: an empty sample is no evidence), except when an exhaustive run enumerated
# an empty type whole: there the law holds of every value there is (`EmptyIsInitial`, `x : Empty`;
# bite 13c item 5, record/plan/core-2026-10-17/report-bite-13c.md), the one exception. An empty census
# is refused before (`census`). `judged` runs after `run_spec` and outside `_drawing_code`: it changes
# no draw, so no identity.

# [proposed] How deep `premises_of` unfolds the laws a body applies before it stops looking.
UNFOLD = 8


def measured_record(measures, points, members, regions):
    """A numerical law's evidence as the entry keeps it (laws.lth §5, D-2026-10-18-j): the cases
    measured, the worst ratio of distance to bound with the distance and bound it came from (`worst`
    None when a positive distance met a zero bound, `ratioOf`'s `nothing`), and the worst per region
    (the regions' order, D-2026-10-16-i), each region's worst over the measured cases it counted.
    The verdict is the comparison at each case; the ratio records how tight the bound was."""
    worst, at = 0.0, None
    for _, distance, bound in measures:
        r = ratio_of(distance, bound)
        if at is None or (worst is not None and (r is None or r > worst)):
            worst, at = r, (distance, bound)
    out = {"measured": len(measures), "worst": worst if measures else None,
           "distance": at[0] if at else None, "bound": at[1] if at else None}
    if members is not None and regions is not None and len(members) == len(points):
        by_case = {id(case): k for k, (case, _) in enumerate(points)}
        per = {}
        for case, distance, bound in measures:
            for key in members[by_case[id(case)]]:
                r = ratio_of(distance, bound)
                per[key] = worse_ratio(per[key], r) if key in per else r
        out["regions"] = [{"region": g["region"], "worst": per[(g["region"]["source"], g["region"]["name"])]}
                          for g in regions if (g["region"]["source"], g["region"]["name"]) in per]
    return out


# ---------------------------------------------------------------------- vacuity and the empty experiment

# [wave A, bite A3; record/plan/audit-algebras-2026-10-22/execution.md; the audit of 2026-10-22,
# section 12 "Vacuity, empty evidence and uncovered regions" (report.md, 5b1a05e)] A premise stated as a
# subtype (`c : Chain A r`) is met by every case drawn, and the regions count it (`Classifier`). One
# stated in the law's body is not: `p -> q` (`implies`, L12.7: `then` is material), `if p then q else
# true` or `q or not p` (bite A3b), at the top of the body, under its lets (`{ r := ... ; if
# r.converged then ... else true }`), or in the body of a law it applies, unfolded. Such a law held at every case where `p` was false, so with
# `p` never true it passed with no evidence. `judged` counts the cases where every premise held; none
# is laws.lth's `Vacuous n`, not run with the count as its reason (D-2026-10-16-m), never a pass. A run
# that evaluated no case and raised none is an empty experiment, not run with its reason (7.S12;
# test.lth's `CountsCases`: an empty sample is no evidence), except when an exhaustive run enumerated
# an empty type whole: there the law holds of every value there is (`EmptyIsInitial`, `x : Empty`;
# bite 13c item 5, record/plan/core-2026-10-17/report-bite-13c.md), the one exception. An empty census
# is refused before (`census`). `judged` runs after `run_spec` and outside `_drawing_code`: it changes
# no draw, so no identity.

# [proposed] How deep `premises_of` unfolds the laws a body applies before it stops looking.
UNFOLD = 8


def _is_false(term):
    return isinstance(term, t.Var) and _base(term) == "false"


def _disjuncts(term):
    """The disjuncts of a chain of `or`, in order, with the head `or` as the program calls it."""
    head, args = _spine(term)
    if isinstance(head, t.Var) and _base(head) == "or" and len(args) == 2:
        left, h = _disjuncts(args[0])
        right, _ = _disjuncts(args[1])
        return left + right, head
    return [term], None


def _negated(term):
    """`p` when `term` is `not p`, else None."""
    head, args = _spine(term)
    return args[0] if isinstance(head, t.Var) and _base(head) == "not" and len(args) == 1 else None


def _premise_split(term):
    """(premise, rest) when `term` is `implies p q`, `match p { true -> q ; false -> true }`, or a
    disjunction with exactly one negated disjunct, `q or not p` (`not p or q`), with `q` not the
    literal `false` (`not p` is that match, and states no premise); else None. [bite A3b, the
    coordinator's answer of 2026-10-23 to report-wave-a-3.md's question] `q or not p` is material `p ->
    q`, the form of the core's antisymmetry and injectivity (`o.eq x y or not (r x y and r y x)`).
    [proposed] With two negated disjuncts or more the reading is the author's and not the form's:
    `not (wellFormed p) or ... or not (image (retitle p s) == image p)` (plot.lth's
    `ImageSeesTheTitle`) has its conclusion under a `not` too, so nothing is read there."""
    head, args = _spine(term)
    if isinstance(head, t.Var) and _base(head) == "implies" and len(args) == 2:
        return args[0], args[1]
    parts, connective = _disjuncts(term)
    if connective is not None:
        negated = [(k, _negated(d)) for k, d in enumerate(parts) if _negated(d) is not None]
        if len(negated) == 1:
            k, premise = negated[0]
            others = parts[:k] + parts[k + 1:]
            rest = others[0]
            for d in others[1:]:
                rest = Runner.apply(connective, [rest, d])
            if not _is_false(rest):
                return premise, rest
    if isinstance(term, t.Match) and len(term.arms) == 2:
        arms = {}
        for pattern, body in term.arms:
            if not (isinstance(pattern, t.PCon) and not pattern.patterns):
                return None
            arms[pattern.name.partition("@")[0]] = body
        yes, no = arms.get("true"), arms.get("false")
        if yes is not None and _holds_trivially(no) and not _is_false(yes):
            return term.value, yes
    return None


def _holds_trivially(term):
    """`true`, or the law that is the case `true` (`Case true`, a numerical law outside its range,
    laws.lth §5)."""
    if isinstance(term, t.Var) and _base(term) == "true":
        return True
    head, args = _spine(term)
    return isinstance(head, t.Var) and _base(head) == "Case" and len(args) == 1 and _holds_trivially(args[0])


def premises_of(runner, law):
    """The premises the law (as the program calls it) states in its body, in order, as a function of
    its parameters each (`t.Lam`s over them); [] when it states none."""
    defined = {}
    for a in runner.program:
        if isinstance(a, t.Define):
            defined.setdefault(a.name, a)
    d = defined.get(law)
    if d is None:
        return []
    binders, body = [], d.body
    while isinstance(body, t.Lam):
        binders.append((body.name, body.type))
        body = body.body
    out, depth, lets = [], 0, []
    while True:
        split = _premise_split(body)
        if split is not None:
            premise = split[0]
            for name, ty, value in reversed(lets):  # a premise under `{ r := ... ; ... }` keeps its lets
                premise = t.Let(name, ty, value, premise)
            out.append(premise)
            body = split[1]
            continue
        if isinstance(body, t.Let):
            lets.append((body.name, body.type, body.value))
            body = body.body
            continue
        head, args = _spine(body)
        unfolded = defined.get(head.name) if isinstance(head, t.Var) and args and depth < UNFOLD else None
        if unfolded is None:
            break
        inner = unfolded.body
        for arg in args:
            if not isinstance(inner, t.Lam):
                inner = None
                break
            inner = kernel.substitute(inner.name, arg, inner.body)
        if inner is None or isinstance(inner, t.Lam):
            break
        body, depth = inner, depth + 1
    wrapped = []
    for p in out:
        for name, ty in reversed(binders):
            p = t.Lam(name, ty, p)
        wrapped.append(p)
    return wrapped


def _premises_held(runner, premises, case, fuel):
    """Whether every premise holds at the case, read in order (a later one only when the earlier held);
    a premise whose reduction raises or gives no Bool did not hold."""
    for p in premises:
        runner.fuel = fuel
        try:
            if runner.whnf(Runner.apply(p, list(case))) != TRUE:
                return False
        except _RAISES:
            return False
    return True


def judged(runner, loaded, spec, outcome, fuel):
    """`run_spec`'s outcome judged for vacuity and for an empty experiment (above): laws.lth's
    `Vacuous n` when no evaluated case held the law's premises, `NotRun` when no case was evaluated
    and none raised (but an empty type enumerated whole), else the outcome with the count of the cases
    that held its premises, when it states any (`held`)."""
    if not isinstance(outcome.evidence, Points):
        return outcome
    if not outcome.evidence.cases:
        if outcome.raised:
            return outcome
        if spec.sampled:
            return _not_run(spec, f"an empty experiment: {spec.cases} cases asked, none drawn (7.S12)",
                            outcome.parameters)
        return outcome  # an empty type enumerated whole (`EmptyIsInitial`)
    premises = premises_of(runner, _as_called(loaded, spec.law))
    if not premises:
        return outcome
    held = sum(1 for case, _ in outcome.evidence.cases if _premises_held(runner, premises, case, fuel))
    if held or outcome.verdict == "Refuted":
        return replace(outcome, held=held)
    return replace(outcome, evidence=Vacuous(outcome.evaluated), verdict="Unsettled", grade=None, held=0,
                   regions=None, labels=None)


def vacuity_reason(evaluated):
    """The reason a vacuous run is not run (D-2026-10-16-m: its premise count)."""
    return f"vacuous: no premise held in the {evaluated} cases evaluated (D-2026-10-16-m)"


# ---------------------------------------------------------------------- the regions (certification.lth §2)

# [proposed] The types of the cutoffs a law takes, the demand's (D-2026-10-14-c; D-2026-10-16-k item
# 20 makes per-law cutoffs typed fields of `Demand`, which will list them): a parameter of one gives
# the law's regions just above and just below it (D-2026-10-16-j, certification.lth's `lawRegions`).
CUTOFF_TYPES = ("Tolerance", "RankFloor", "Sequential")
# [proposed] How near a cutoff is "just above" or "just below": a number of the case within this
# factor of the cutoff, (c, c w] above and [c / w, c) below (generators.py's `specials` draws c w and
# c / w); and the factor a premise stated by a cutoff is read at to find its boundary.
CUTOFF_WIDTH = 2.0


def is_cutoff(runner, ty, cutoff_types=CUTOFF_TYPES):
    """Whether a parameter's type is a cutoff's: one of `cutoff_types`, or a subtype of one
    (`ClearFloor`, a `RankFloor` below 0.001)."""
    for _ in range(20):
        if _base(ty) in cutoff_types:
            return True
        if isinstance(ty, t.Subtype):
            ty = ty.type
        elif isinstance(ty, t.Var) and ty.name in runner.types and runner.types[ty.name] != ty:
            ty = runner.types[ty.name]
        else:
            return False
    return False


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
      `w` the width; a cutoff of 0 has no sides, and gives no region; a cutoff bound to a census (a
      value the demand fixed) has none either: its sides exist only when it is drawn (the
      coordinator's answer to finding 6, 2026-10-17);
    - a parameter bound to a census of one value gives no region of any kind, neither a degenerate
      case of its type nor a premise's boundary (nor a cutoff's sides, above): the law is claimed
      only at that value (the coordinator's answer to the remaining finding, 2026-10-17);
    - the boundary of a premise stated by a cutoff (`PsdAt m fl`) is where its predicate holds at the
      cutoff and fails at the cutoff times w or divided by it; of a premise with bounds (`Nat`,
      `Fin n`, `Seed`), the bounds and their neighbours; of an exact premise (`Symmetric`), every case
      (the premise held, 7.S14);
    - a degenerate case of the type that no case met and whose witness is outside the parameter's
      type at every case is no region of the law (`SymmetricOf 3` and `0 x 0`)."""

    def __init__(self, runner, loaded, values, params, cutoff_types=CUTOFF_TYPES, width=CUTOFF_WIDTH, fixed=(),
                 single=()):
        self.runner, self.values, self.params, self.width = runner, values, params, width
        self.single = set(single)  # bound to one value: no region of any kind from it
        self.cutoffs = [k for k, (_, ty) in enumerate(params) if is_cutoff(runner, ty, cutoff_types)]
        # [the coordinator's answer, 2026-10-17] a cutoff bound to a census is fixed by the demand
        # and is never drawn: its two sides exist only when it is drawn, so only those cutoffs give them
        self.sided = [k for k in self.cutoffs if k not in set(fixed)]
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
    def numbers(self, v, out, budget=None):
        """The doubles a value holds: a literal, the entries of a vector or a matrix (a host array, or
        a function on indices read entry by entry up to the line's `regionEntries`), the parts of a
        pair, a record, an injection, a list; at most the line's `regionNumbers` of them (7.S8: both
        budgets of the line, generators.lth's `Budgets`, the core's bite 4b)."""
        if budget is None:
            budget = self.values.budgets["regionNumbers"]
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
                    if int(np.prod(shape)) <= self.values.budgets["regionEntries"]:
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
        for j in self.sided:
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
        """The parameters of a subtype other than the cutoffs: (k, the cutoffs its type names).
        [proposed] A type parameter (`S : Concrete`, a subtype of `U`) is no premise of the tester's:
        its predicate is the checker's to decide (4.R8), and it has no boundary a case can reach."""
        out = []
        for k, (name, ty) in enumerate(self.params):
            if k in self.cutoffs or k in self.single:
                continue
            try:
                base, predicates = self.values.form(ty)
            except _RAISES:
                continue
            if predicates and not isinstance(base, t.Universe):
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
    def classify(self, cases, members=None):
        """The grading regions with their cases, in order (the type's, then each cutoff's sides,
        then each premise's boundary), and the labels with theirs: ([(source, name, n)], [(name, n)]).
        `members`, a list, receives for each case the set of regions it is counted in, (source, name)
        (bite C1: a numerical law's worst ratio per region)."""
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
                    instances[k] = [] if k in self.single else self.instance(k, ty, labels=False)
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
            for j in self.sided:
                c = _number_of(self.runner, first[j])
                if c is not None and c != 0.0:
                    add(("FromLaw", f"{self.params[j][0]} above"), counts, order, 0)
                    add(("FromLaw", f"{self.params[j][0]} below"), counts, order, 0)
            for k, _ in premises:
                add(("FromLaw", f"{self.params[k][0]} boundary"), counts, order, 0)
        inside = {name: False for name in witnesses}  # a witness inside its parameter's type at some case
        for case in cases:
            counted = set()
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
                    counted.add(("FromType", name))
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
                    counted.add(("FromLaw", name))
            for k, stated_by in premises:
                try:
                    if self.at_boundary(k, stated_by, case):
                        counts[("FromLaw", f"{self.params[k][0]} boundary")] += 1
                        counted.add(("FromLaw", f"{self.params[k][0]} boundary"))
                except _RAISES:
                    pass
            if members is not None:
                members.append(counted)
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
    # [bite C1] a numerical law (laws.lth §5, `Within`) is a `Law` too, but runs case by case
    return _head_name(ty) == "Law" and not _applies(runner, definition.body, "Within", set())


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
    earlier parameter. [proposed] A predicate that reduces to neither `true` nor `false` (stuck on a
    leaf with no body, `hasStructuralEquality` of `Concrete`, which the checker decides, 4.R8) is not
    the tester's to decide, and is passed over."""
    key = (param[0], id(v)) if ty == param[1] else None
    checked = values.__dict__.setdefault("checked", {})
    if key is not None and checked.get(key) is v:
        return
    _, predicates = values.form(ty)
    for name, p in predicates:
        if values.whnf(kernel.substitute(name, v, p)) == FALSE:
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


def _case_text(outcome):
    """The refuting case of an outcome; of a conjunction's, or a control's of one, with the conjunct it
    refuted (`Symmetric Int r: p = ...`)."""
    case = show_case(outcome.parameters, outcome.refuting)
    named = outcome.conjunct is not None and (outcome.parts is not None or outcome.spec.control)
    return f"{outcome.conjunct}: {case}" if named else case


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
    if isinstance(outcome.evidence, Vacuous):
        return f"not run: {vacuity_reason(outcome.evidence.evaluated)}"
    if isinstance(outcome.evidence, Tested):
        return _tested_tail(outcome)
    if isinstance(outcome.evidence, AssumedAxiom):
        return f"assumed, an axiom: {outcome.evidence.statement}"
    if outcome.spec.control and outcome.verdict == "Refuted":
        return f"refuted at {_case_text(outcome)}{ratio_text(outcome.measured)}: the control passed"
    if outcome.spec.control and outcome.grade is not None and _CONJUNCT in outcome.spec.law:
        # [bite D1] one conjunct holding on the broken model is no failure of the control: the line
        # fails only when no conjunct refutes it
        return f"held ({_GRADE_WORDS.get(outcome.grade, outcome.grade)}): this conjunct does not see the break"
    if outcome.spec.control and outcome.grade is not None:
        return f"{_CONTROL_FAILED} ({_GRADE_WORDS.get(outcome.grade, outcome.grade)})"
    if outcome.verdict == "Refuted":
        return f"refuted at {_case_text(outcome)}{ratio_text(outcome.measured)}"
    if outcome.verdict == "Unsettled":
        case, message = outcome.raised[0]
        return (f"unsettled: {len(outcome.raised)} cases raised, the first at "
                f"{show_case(outcome.parameters, case)}: {message}")
    return _GRADE_WORDS.get(outcome.grade, outcome.grade) + ratio_text(outcome.measured)


def ratio_text(measured):
    """A numerical law's worst ratio of distance to bound, as a line shows it (bite C1)."""
    if not measured or not measured.get("measured"):
        return ""
    worst = measured["worst"]
    return ", worst ratio " + ("unbounded" if worst is None else f"{worst:.6g}")


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
            return grade + ratio_text(entry.get("measured"))
        start = entry["evidence"].get("from")
        more = f", {certify.continued_text(start, tested['spent'])}" if start else ""
        return f"supported, {grade}: held at {certify.tested_text(tested)}{more}"
    if "ControlRefuted" in o:
        return f"refuted at {o['ControlRefuted']}: the control passed"
    if "ControlConfirmed" in o and entry.get("conjunct") is not None:
        return f"held ({o['ControlConfirmed']}): this conjunct does not see the break"
    if "ControlConfirmed" in o:
        return f"{_CONTROL_FAILED} ({o['ControlConfirmed']})"
    if "Failed" in o:
        return f"refuted at {o['Failed']}"
    if "Unresolved" in o:
        return certify.show_outcome(o)
    shown = "NotRun" in entry["evidence"] or "Vacuous" in entry["evidence"]
    return f"not run: {o['NotRunFor']}" if shown else o["NotRunFor"]


def line(outcome):
    """One line per test: the law, the mode, the cases evaluated, the grade or the refuting case,
    and whether it ran or its outcome was known (7.S13). A control of a conjunction, then a line per
    conjunct (bite D1)."""
    spec = outcome.spec
    if outcome.parts is not None and not spec.control:
        return _conjunction_line(outcome)
    if outcome.parts is not None:
        return "\n".join([line(replace(outcome, parts=None))] + ["  " + line(o) for o in outcome.parts])
    mode = f"sampled (seed {spec.seed}, size {spec.size}, placement ignored)" if spec.sampled else "exhaustive"
    counted = f"{outcome.evaluated} cases"
    if isinstance(outcome.evidence, Tested) or "Tested" in (outcome.evidence if isinstance(outcome.evidence, dict) else {}):
        mode, counted = f"sequential (seed {spec.seed % SEEDS})", f"{outcome.evaluated} samples"
    law = spec.law if outcome.conjunct is None or (spec.control and _CONJUNCT not in spec.law) \
        else f"conjunct {outcome.conjunct}"
    head = f"{'control of ' if spec.control else ''}{law}: {mode}, {counted}"
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
    if isinstance(outcome.evidence, dict):  # settled from a known conjunct's entry (`_settle_known`)
        return f"{head}, {_entry_tail(outcome.entry)} ({how})"
    return f"{head}, {_tail(outcome)} ({how})"


def _conjunction_line(outcome):
    """A conjunction's line: the law with the conjunction's outcome and how many conjuncts ran, then
    one indented line per conjunct (D-2026-10-18-f)."""
    ran = sum(1 for o in outcome.parts if o.known is None)
    how = "known" if ran == 0 else f"{ran} of {len(outcome.parts)} ran"
    base = next(o for o in outcome.parts if o.conjunct == outcome.conjunct)
    tail = _entry_tail(base.entry) if base.known is not None else _tail(base)
    if outcome.verdict == "Refuted":
        tail = f"refuted at {outcome.conjunct}: " + tail.removeprefix("refuted at ")
    elif outcome.grade is not None:
        tail = _GRADE_WORDS.get(outcome.grade, outcome.grade)
    else:
        tail = f"not graded, {outcome.conjunct}: {tail}"
    head = f"{outcome.spec.law}: conjunction of {len(outcome.parts)}, {outcome.evaluated} cases, {tail} ({how})"
    return "\n".join([head] + ["  " + line(o) for o in outcome.parts])


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


def run_tests(path, seed=None, fuel=None, deep=False, store=False):
    """Run every `test` line of the file; the outcomes in order. Each line runs with the fuel of its
    budgets (7.S8), or with `fuel` when one is given (`--fuel`), which its entry's budgets then
    record. With `store`, each line's identity
    is looked up first in the store of the file that makes its claim (`claim_file`; a known outcome
    is reused unless `deep`) and each line run is recorded there, under its lock
    (certification.lth's `known` and `record`: an agreeing replay writes nothing, a disagreeing one
    is kept beside, D-2026-10-15-f; a run cut by its fuel is never written, D-2026-10-15-g); the test
    program's own store is neither read nor written. A line on a law whose body is a conjunction of
    laws runs its conjuncts (`_run_conjunction`, D-2026-10-18-f). The file is a test program
    (`x.test.lut`, 12.R2), refused otherwise before anything is read."""
    require_kind(path, "test")
    runner, specs, loaded = prepare(path) if fuel is None else prepare(path, fuel)
    cones = certify.Cones(runner)
    stores = {}  # the file that makes a claim -> its store's entries, as read
    outcomes = []
    for spec in specs:
        if seed is not None:
            spec.seed = seed
        if fuel is not None:
            spec.budgets["fuel"] = fuel  # the run's fuel in place of the line's, recorded as its budget
        given = spec.budgets["fuel"]
        home = claim_file(loaded, spec, runner)
        if home not in stores:
            stores[home] = certify.read_store(home) if store else []
        parts = conjuncts_of(runner, _as_called(loaded, spec.law))
        if parts:
            outcomes.append(_run_conjunction(runner, loaded, spec, parts, cones, given, home, stores, deep, store))
        else:
            entry = new_entry(runner, loaded, spec, cones, given)
            outcomes.append(_run_line(runner, loaded, spec, entry, given, home, stores, deep, store))
        outcomes[-1].law_store = law_file(loaded, spec.law)
    return outcomes


def _run_line(runner, loaded, spec, entry, given, home, stores, deep, store, run=None):
    """One line whose entry is `entry`: its known outcome from the store of `home`, unless `deep`;
    else run (`run_spec`, or `run` given the statistical start) and recorded there when `store`. A
    line that binds a census of another type than its parameter's is refused at its start, not run
    with the reason (`mistyped_census`), whatever its store knows, and nothing is stored."""
    refusal = mistyped_census(runner, loaded, spec) if run is None else None
    if refusal is not None:
        names = tuple(n for n, _ in parameters(runner, _as_called(loaded, spec.law)) or [])
        outcome = _not_run(spec, refusal, names)
        settle(entry, outcome)
        outcome.cone, outcome.entry, outcome.store = entry["cone"], entry, home
        return outcome
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
        if "Vacuous" in evidence:
            verdict, evaluated = "Unsettled", evidence["Vacuous"]
        if "Assumed" in evidence:
            verdict = "Assumes"
        reused = Outcome(spec, evidence, verdict, found["grade"], evaluated, None, cone=entry["cone"],
                         entry=found, known=found["date"], store=home)
        if certify.disputed_at(entries, key):
            reused.differs = [e for e in entries if certify.identity(e) == key][1]["date"]
        return reused
    # a statistical stretch continues the test of the law under its binding (D-2026-10-16-g)
    start = (lambda c, p, entry=entry, entries=entries: certify.continuation(entries, entry, c, p)) if store else None
    statement = axiom_of(runner, _as_called(loaded, spec.law)) if run is None else None
    if statement is not None:
        outcome = assumed(spec, statement)
    else:
        outcome = judged(runner, loaded, spec, run_measured(runner, spec, given, loaded, start), given) if run is None else run(start)
    settle(entry, outcome)
    outcome.cone, outcome.entry, outcome.store = entry["cone"], entry, home
    fuel_spent = certify.out_of_fuel(entry)
    if found is not None and not fuel_spent and not certify.agree(entry, found):
        outcome.differs = found["date"]
    old = next((e for e in entries if e["law"] == entry["law"] and e["binding"] == entry["binding"]
                and e.get("conjunct") == entry.get("conjunct") and certify.stale(entry["cone"], e)), None)
    if old is not None:
        outcome.stale = old["date"]
    if store and not fuel_spent:
        certify.add_entry(home, entry)
        stores[home] = certify.read_store(home)
    return outcome


def mistyped_census(runner, loaded, spec):
    """[report-controls-M.md 3.1] Why a line's binding cannot stand, or None: a parameter bound to a
    census whose values are not of the parameter's type. A binding by name reaches every conjunct
    with a parameter of that name (`x` the verdicts of `Commutative` and an `A` of `WithinIsMeasured`
    in `Settling`), and the law ran on values of another type. A type that names an earlier
    parameter is read with that parameter's value when its census has one member (`A` bound to
    `[Int]`), and not checked otherwise; a generator is not checked (its draws are typed by it)."""
    law = _as_called(loaded, spec.law)
    params = parameters(runner, law) or []
    names = [n for n, _ in params]
    known = {}  # an earlier parameter bound to a census of one member: that member
    for k, (name, ty) in enumerate(params):
        b = resolve_binding(spec, name, _head_name(ty))
        if b is None:
            continue
        called = _as_called(loaded, b.generator)
        definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == called), None)
        if definition is None or definition.type is None:
            continue
        try:
            if generator_of(runner, called, names[:k]) is not None:
                continue
            members = census(runner, b, ty, called)
        except (NoGenerator, RunError):
            continue
        for n, v in known.items():
            ty = kernel.substitute(n, v, ty)
        if len(members) == 1:
            known[name] = members[0]
        if set(names[:k]) & set(kernel.free_names(ty)):
            continue
        value = definition.type
        if _list_depth(runner, value) > _list_depth(runner, ty):
            value = _applied(runner.resolve(value), "List")
        if _surely_differ(runner, ty, value):
            return (f"{name} : {_show(ty)} is bound to the census {b.generator}, whose values are "
                    f"{_show(value)}: bind a census of its type (a binding by name reaches every "
                    f"conjunct with a parameter {name}; bind by type there)")
    return None


def _surely_differ(runner, a, b):
    """Whether two types surely differ: their kinds, as far as they are read (`_type_kind`), differ,
    or their parts do. What is not read (a type computed by a function, a value inside a type, a
    dependent arrow) is taken as the same: the check refuses only what it is sure of. `Nat`, `Int`
    and `Fin n` are one kind, an integer (a census's values are checked against the refinement)."""
    a, b = _type_unfolded(runner, a), _type_unfolded(runner, b)
    if kernel.alpha_equal(a, b):
        return False
    ka, kb = _type_kind(a), _type_kind(b)
    if ka is None or kb is None:
        return False
    if ka != kb:
        return True
    if isinstance(a, t.App):
        xs, ys = _spine(a)[1], _spine(b)[1]
        return len(xs) == len(ys) and any(_surely_differ(runner, x, y) for x, y in zip(xs, ys))
    if isinstance(a, t.Record):
        return any(_surely_differ(runner, x, y) for (_, x), (_, y) in zip(a.fields, b.fields))
    if isinstance(a, t.Sum):
        return any(_surely_differ(runner, x, y) for (_, x), (_, y) in zip(a.alternatives, b.alternatives))
    if isinstance(a, (t.Pi, t.Sigma)):
        if a.name in kernel.free_names(a.codomain) or b.name in kernel.free_names(b.codomain):
            return False
        return _surely_differ(runner, a.domain, b.domain) or _surely_differ(runner, a.codomain, b.codomain)
    return False


def _type_kind(ty):
    """What `_surely_differ` reads of a type, or None: a primitive's name, a data type's, `List` or
    `Maybe` with its arity, a record's labels, a sum's, an arrow, a pair."""
    if isinstance(ty, t.Var):
        name = ty.name.partition("@")[0]
        return ("integer",) if name in _INTEGERS else ("named", name) if name in _PRIMITIVE_TYPES else None
    if isinstance(ty, t.Data):
        return ("data", ty.name)
    if isinstance(ty, t.App):
        head, args = _spine(ty)
        name = head.name.partition("@")[0] if isinstance(head, t.Var) else None
        return ("integer",) if name == "Fin" else (name, len(args)) if name in ("List", "Maybe") else None
    if isinstance(ty, t.Record):
        return ("record", tuple(n for n, _ in ty.fields))
    if isinstance(ty, t.Sum):
        return ("sum", tuple(n for n, _ in ty.alternatives))
    if isinstance(ty, t.Pi):
        return ("arrow",)
    if isinstance(ty, t.Sigma):
        return ("pair",)
    return None


_INTEGERS = {"Int", "Nat"}
_PRIMITIVE_TYPES = {"Float64", "String", "Unit", "Bool"}


def _type_unfolded(runner, ty):
    """A type as `Runner.resolve` unfolds it, and a name defined as a value that is a type
    (`pushedType : Concrete := Int`) unfolded to it."""
    for _ in range(64):
        ty = runner.resolve(ty)
        if not isinstance(ty, t.Var):
            return ty
        d = next((a for a in runner.program if isinstance(a, t.Define) and a.name == ty.name), None)
        if d is None or d.body is None or isinstance(d.body, t.Lam) or d.body == ty:
            return ty
        ty = d.body
    return ty


def _run_conjunction(runner, loaded, spec, parts, cones, given, home, stores, deep, store):
    """A line on a law whose body is a conjunction of laws (D-2026-10-18-f; the core's bite 4b). Each
    conjunct runs as a line of its own (`conjuncts_of`), under the line's mode, seed, `n`, budgets and
    bindings by name, its missing variables drawn by the generators of their types. A law's line
    gives each conjunct its entry, in the store of the conjunction's claim: the conjunction's law and
    cone, the conjunct named (`conjunct`, part of the identity) and the conjuncts listed
    (`conjuncts`), and its outcome is the conjunction's (`_conjunction_outcome`). [wave D, bite D1;
    L9.14, D-2026-10-25-a question 4: the unit of control is the conjunct] A control's line runs every
    conjunct on the broken model, each its own control entry (`conjunct` in its identity), and passes
    when it refutes one; it also writes the conjunction's control entry, whose binding is every
    conjunct's and whose outcome is the first refutation, as before D1, so that a line that refutes
    no conjunct still fails its control loudly. Each outcome carries the law each conjunct applies
    with that law's cone (`heads`), so that a control line of the conjunct's own law counts for it."""
    of = _as_called(loaded, spec.law)
    specs = [replace(spec, law=c.called) for c in parts]
    entries = [new_entry(runner, loaded, s, cones, given, (spec.law, c, parts)) for s, c in zip(specs, parts)]
    heads = conjunct_heads(runner, parts, cones)
    done = []
    for s, c, e in zip(specs, parts, entries):
        o = _run_line(runner, loaded, s, e, given, home, stores, deep, store)
        o.conjunct = c.shown
        done.append(o)
    if not spec.control:
        outcome = _conjunction_outcome(spec, done, cones.hash(of), home)
        outcome.heads = heads
        return outcome
    entry = dict(entries[0], law=spec.law)
    for k in ("conjunct", "conjuncts"):
        entry.pop(k, None)
    entry["binding"] = list({json.dumps(b, sort_keys=True): b for e in entries for b in e["binding"]}.values())
    entry["reach"] = list({json.dumps(r, sort_keys=True): r for e in entries for r in e["reach"]}.values())
    entry["hosts"] = sorted({tuple(h) for e in entries for h in e["hosts"]})
    entry["hosts"] = [list(h) for h in entry["hosts"]]
    outcome = _run_line(runner, loaded, spec, entry, given, home, stores, deep, store,
                        lambda start: _conjunction_outcome(spec, done, entry["cone"], home))
    outcome.parts, outcome.heads = done, heads
    return outcome


def conjunct_heads(runner, parts, cones):
    """[bite D1] Per conjunct, the law it applies, as a test line names it, and the hash of that law's
    cone: a control line of `MetresWithin` controls the conjunct `MetresWithin t` of `Tape`."""
    defined = {a.name for a in runner.program if isinstance(a, t.Define)}
    heads = {}
    for c in parts:
        d = next((a for a in runner.program if isinstance(a, t.Define) and a.name == c.called), None)
        body = d.body if d is not None else None
        while isinstance(body, t.Lam):
            body = body.body
        head, _ = _spine(body) if body is not None else (None, ())
        if isinstance(head, t.Var) and head.name in defined:
            heads[c.shown] = (head.name.partition("@")[0], cones.hash(head.name))
    return heads


def line_conjuncts(path, fuel=1_000_000):
    """[bite D1] Per law a line of the file names, its conjuncts as the tester names them, each with the
    law it applies and that law's cone (`conjunct_heads`); a law no conjunction has none."""
    runner, specs, loaded = prepare(path, fuel)
    cones = certify.Cones(runner)
    found = {}
    for spec in specs:
        if spec.law in found:
            continue
        parts = conjuncts_of(runner, _as_called(loaded, spec.law))
        found[spec.law] = [(c.shown, *conjunct_heads(runner, [c], cones).get(c.shown, (None, None))) for c in parts]
    return found


def _conjunction_outcome(spec, parts, cone, home):
    """A conjunction's outcome from its conjuncts': refuted when one is, at its case; when every one
    has a grade, the combination of their grades the demand chooses (5.S8; `certify.COMBINATION`,
    the weakest by default), confirmed when every one is; otherwise what the first conjunct without
    a grade settled. Known when every conjunct's outcome was."""
    refuted = next((o for o in parts if o.verdict == "Refuted"), None)
    if refuted is not None:
        base, verdict, grade = refuted, "Refuted", None
    elif all(o.grade is not None for o in parts):
        comb = certify.COMBINATIONS[certify.COMBINATION]
        grade = functools.reduce(lambda g, o: comb(o.grade, g), parts, None)
        base = next(o for o in parts if o.grade == grade)
        verdict = "Confirmed" if all(o.verdict == "Confirmed" for o in parts) else "Supported"
    else:
        base = next(o for o in parts if o.grade is None)
        verdict, grade = base.verdict, None
    known = [o.known for o in parts]
    return Outcome(spec, base.evidence, verdict, grade, sum(o.evaluated for o in parts), base.refuting,
                   list(base.raised), base.parameters, cone=cone, store=home,
                   known=max(known) if all(known) else None,
                   out_of_fuel=base.out_of_fuel if verdict != "Refuted" else None,
                   regions=base.regions, labels=base.labels, conjunct=base.conjunct, parts=parts)


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
    them loads it), else the first; nothing is written in two stores. A control line's home is the
    file that states the law whatever models it binds besides the broken one (D-2026-10-22-a: a
    control is the law's; core bite 13a), unless that file is the test program itself."""
    if spec.control:
        stated = law_file(loaded, spec.law)
        if stated != loaded.top:
            return stated
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
    names, or each member of a census that is a list literal of names. A type alias (`WorldState`,
    demand.lth's `RunRecord`), a type (`UnitList`), a constructor (`Sampled`) or a census whose
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


def _list_literal(loaded, found):
    """A definition's body when it is a list literal (`[csv, parsed text]`), as the file that defines
    the census writes it; None when its body is anything else."""
    file = loaded.files.get(found[0])
    if file is None:
        return None
    for act in file.acts:
        if isinstance(act, s.Define) and act.name == found[1] and not act.binders:
            body = getattr(act.body, "term", None)
            if isinstance(body, s.List):
                return body
    return None


def _list_members(loaded, found):
    """The names a definition's list literal body holds (`[csv, built]`), as the file that defines
    the census writes them; none when its body is anything else."""
    body = _list_literal(loaded, found)
    return [] if body is None else [v.name for v in body.values if isinstance(v, s.Name)]


def _builds_members(loaded, called):
    """Whether a census is a list literal some of whose members are built by an expression
    (`parsed smallText`) rather than named, so that no member's cone holds that code."""
    if loaded is None:
        return False
    found = next(((f, n) for f in loaded.files for n in loaded.files[f].defined
                  if loaded.internal(f, n) == called), None)
    body = None if found is None else _list_literal(loaded, found)
    return body is not None and any(not isinstance(v, s.Name) for v in body.values)


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


# [the coordinator's addition to the core's bite 1, 2026-10-17; j2a's finding 4] The code that draws
# a sampled entry's cases: the tester's sampling (the draw over a type, a generator driven, a census
# walked, the cutoffs' literals) and generators.py. The interpreter's revision is the last tag
# (D-2026-10-15-i) and no tag comes until after the core, so without this a change to the draws
# left the identity as it was and `--deep` replays disagreed (RankUnderRotation,
# PrecisionSymmetric, DensityPeaksAtMean). [proposed] The functions are named here rather than the
# whole of tester.py hashed, so that a change to how a line is reported stales nothing.
def _drawing_code():
    return (Values, _draw_case, _in_its_type, census, generator_of, resolve_binding, is_cutoff, run_spec,
            parameters, _parts, _missing, conjunction_parts)


@functools.cache
def drawing_revision():
    """The hash of the code that draws a sampled entry's cases (`_drawing_code`'s sources, the
    alphabet of a drawn string and the range of a seed, generators.py's bytes); it is the
    fingerprint of a parameter drawn under SampledMode and is added to a generator's."""
    h = hashlib.sha256()
    for code in _drawing_code():
        h.update(inspect.getsource(code).encode("utf-8"))
    h.update(repr((_LETTERS, SEEDS)).encode("utf-8"))
    h.update(Path(generators.__file__).read_bytes())
    return "sha256:" + h.hexdigest()


def new_entry(runner, loaded, spec, cones, fuel, conjunct=None):
    """The entry of a line before it runs: its identity (the law, the hash of its cone, the binding
    expanded per parameter, the seed, `n`), the budgets, the reach of each parameter, the date, the
    interpreter and the host code by route (the law's cone's and each census's). The evidence, the
    grade and the outcome are `settle`'s.

    [proposed] A parameter's generator is the census its binding names, printed with the binding's
    coverage, its fingerprint the hash of the census's cone; or the generator its binding names
    (bite 3), printed with the parameters it reads and the size, its fingerprint the hash of its
    cone and the hash of the code that drives it (`drawing_revision`) (7.S9: a name with its
    fingerprint), no reach (a draw lists no values); otherwise the mode's functor over the
    parameter's type, printed with the placement and the size, its fingerprint the hash of the drawing
    code under SampledMode and empty under ExhaustiveMode. The reach: a census's members; the support of the
    type under ExhaustiveMode; under SampledMode, for an `Int` or a `Float64` (refined or not, not
    dependent on an earlier parameter), the interval it is drawn from; no reach otherwise, which
    covers no value a run gives (certification.lth's `coversAll`).

    `conjunct`, (the conjunction's law as the line writes it, the `Conjunct`, every conjunct), makes
    the entry a conjunct's (D-2026-10-18-f): the conjunction's law and the hash of its cone, the
    conjunct's parameters, the conjunct and the list of them recorded."""
    law = _as_called(loaded, spec.law)
    params = parameters(runner, law) or []
    statistical = is_statistical(runner, law)  # its bindings are censuses of one, a stream among them
    values = Values(runner, random.Random(0), spec.size, spec.budgets, fuel)
    of = law if conjunct is None else _as_called(loaded, conjunct[0])
    binding, reach, hosts = [], [], dict(cones.hosts(of))
    fixed = fixed_carrier(runner, law, params)
    for k, (name, ty) in enumerate(params):
        if name in fixed:
            binding.append({"parameter": name, "generator": f"{_show(fixed[name])} (fixed by the structure's laws)",
                            "fingerprint": ""})
            continue
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
                                "fingerprint": f"{cones.hash(called)},{drawing_revision()}"})
                hosts.update(cones.hosts(called))
                continue
            # a census that lists models: the hashes of its members, comma-joined, so that a run
            # naming one model finds its own hash there (`at` in certify.py) [proposed]; and the
            # hash of the census's own cone when it names none, or when a member is built by an
            # expression, whose code is in no named member's cone (3h's finding: a change to
            # tables.py left `parsed ...` members' lines known)
            listed = _listed_called(loaded, called)
            prints = [cones.hash(m) for m in listed]
            if not listed or _builds_members(loaded, called):
                prints.append(cones.hash(called))
            binding.append({"parameter": name, "generator": f"{b.generator} ({_show(b.coverage)})",
                            "fingerprint": ",".join(prints)})
            hosts.update(cones.hosts(called))
            try:
                members = census(runner, b, ty, called)
            except (NoGenerator, RunError):
                continue
            reach.append({"parameter": name, "reach": {"Members": [_value(runner, v) for v in members]}})
            continue
        mode = f"SampledMode {_show(spec.placement)} (size {spec.size})" if spec.sampled else "ExhaustiveMode"
        binding.append({"parameter": name, "generator": f"{mode} over {_show(ty)}",
                        "fingerprint": drawing_revision() if spec.sampled else ""})
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
    entry = {"law": spec.law if conjunct is None else conjunct[0], "cone": cones.hash(of), "binding": binding,
             "seed": spec.seed, "cases": spec.cases,
             "budgets": dict(spec.budgets), "reach": reach, "evidence": None, "grade": None, "outcome": None,
             "date": certify.now(), "interpreter": certify.interpreter_revision(),
             "hosts": [[r, h] for r, h in sorted(hosts.items())]}
    if conjunct is not None:
        entry["conjunct"], entry["conjuncts"] = conjunct[1].shown, [c.shown for c in conjunct[2]]
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
    if isinstance(outcome.evidence, AssumedAxiom):  # laws.lth's `Assumed`, its statement kept
        entry["evidence"] = {"Assumed": outcome.evidence.statement}
        entry["outcome"], entry["grade"] = "Passed", outcome.grade
        return entry
    if isinstance(outcome.evidence, Tested):
        return _settle_tested(entry, outcome)
    if isinstance(outcome.evidence, dict):  # a known conjunct's evidence, as its store records it
        return _settle_known(entry, outcome)
    if isinstance(outcome.evidence, Vacuous):  # laws.lth's `Vacuous n`, not run (D-2026-10-16-m), a control too
        entry["evidence"] = {"Vacuous": outcome.evidence.evaluated}
        entry["outcome"] = {"NotRunFor": vacuity_reason(outcome.evidence.evaluated)}
        return entry
    entry["evidence"] = {"Points": {"evaluated": outcome.evaluated, "raised": len(outcome.raised),
                                    "coverage": _show(outcome.evidence.coverage), "verdict": outcome.verdict}}
    if outcome.held is not None:  # the cases in which the premises the law states held (bite A3)
        entry["evidence"]["Points"]["held"] = outcome.held
    if outcome.measured is not None:  # laws.lth's `Measured`, its worst ratio (bite C1, D-2026-10-18-j)
        entry["measured"] = outcome.measured
    # 7.S9: the entry records its regions and its labels (certification.lth's `RegionEvidence`)
    if outcome.regions is not None:
        entry["regions"] = outcome.regions
    if outcome.labels:
        entry["labels"] = outcome.labels
    if outcome.spec.control:
        # a control's outcome: refuted is the control passing, a grade the control failing; neither
        # is the law's grade nor its failure (7.S19, D-2026-10-15-a)
        if control_passes(outcome.verdict):
            entry["outcome"] = {"ControlRefuted": _case_text(outcome)}
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


def _settle_known(entry, outcome):
    """[report-controls-M.md 3.2] A conjunction's entry whose evidence is a known conjunct's, reused
    from its store (`_run_line`), so already recorded: that record with the conjunction's cases and
    verdict, as `settle` writes a run's; its refuting case is the one the conjunct's entry records,
    the conjunct named as `_case_text` names it; otherwise as `settle`."""
    base = next((o for o in outcome.parts or () if o.evidence is outcome.evidence), None)
    known = base.entry["outcome"] if base is not None and base.entry is not None else None
    evidence = json.loads(json.dumps(outcome.evidence))
    points = evidence.get("Points")
    if points is not None:
        points.update(evaluated=outcome.evaluated, verdict=outcome.verdict)
        points.pop("held", None)  # a conjunction states no premise of its own, as when it runs
    entry["evidence"] = evidence
    if outcome.regions is not None:
        entry["regions"] = outcome.regions
    if outcome.labels:
        entry["labels"] = outcome.labels
    control = outcome.spec.control
    if outcome.verdict == "Refuted":
        case = next(iter(known.values())) if isinstance(known, dict) else _case_text(outcome)
        if points is not None and outcome.conjunct is not None and isinstance(known, dict):
            case = f"{outcome.conjunct}: {case}"
        entry["outcome"] = {"ControlRefuted" if control else "Failed": case}
    elif outcome.grade is not None:
        if control:
            entry["outcome"] = {"ControlConfirmed": _GRADE_WORDS.get(outcome.grade, outcome.grade)}
        else:
            entry["outcome"], entry["grade"] = "Passed", outcome.grade
    else:
        entry["outcome"] = known if isinstance(known, dict) and "NotRunFor" in known else {"NotRunFor": _tail(outcome)}
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
