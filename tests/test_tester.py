"""`luthier test`, bite 1 (record/IA/tester-2026-10-14/prompt.md): test.lth's Tester over the
programs under tests/tester/; names scoped by run.py's loader since run.py bite 6 (prompt-6.md)."""
import json
import os
from pathlib import Path

import pytest

from luthier import term as t, tester
from luthier.cli import main

ROOT = Path(__file__).resolve().parents[1]
LAWS = ROOT / "tests" / "tester" / "laws.test.lut"
CASES = ROOT / "tests" / "tester" / "cases.test.lut"


def lines_of(capsys, *args):
    # --no-cert: the programs under tests/ get no store (test_certify.py tests the store)
    code = main(["test", "--no-cert", *map(str, args)])
    return code, capsys.readouterr().out.splitlines()


def test_the_five_kinds_of_outcome(capsys):
    code, lines = lines_of(capsys, LAWS)
    assert code == 1  # a law is refuted and one is not run
    assert lines == [
        "NotInvolutive: exhaustive, 2 cases, exhaustive (ran)",
        "AndIsOr: exhaustive, 4 cases, refuted at a = true, b = false (ran)",
        "IntPlusCommutes: sampled (seed 7, size 10, placement ignored), 200 cases, sampled (ran)",
        "Small: sampled (seed 0, size 10, placement ignored), 100 cases, sampled (ran)",
        "Small: sampled (seed 0, size 1000, placement ignored), 100 cases, refuted at x = 552 (ran)",
        "IntPlusCommutes: exhaustive, 0 cases, not run: x : Int: Int is infinite: "
        "ExhaustiveMode needs its bounds or a census (7.R3) (ran)",
    ]


def test_outcomes_carry_laws_evidence_and_test_lth_grade():
    outcomes = tester.run_tests(LAWS)
    holds, refuted, sampled, _, at_size, not_run = outcomes
    assert (holds.verdict, holds.grade) == ("Confirmed", "ExhaustiveGrade")
    assert [ok for _, ok in holds.evidence.cases] == [True, True]
    assert (refuted.verdict, refuted.grade) == ("Refuted", None)
    assert (sampled.verdict, sampled.grade, sampled.evaluated) == ("Supported", "Sampled", 200)
    assert sampled.spec.cases == 200 and sampled.spec.seed == 7
    assert at_size.verdict == "Refuted" and at_size.spec.size == 1000
    assert isinstance(not_run.evidence, tester.NotRun) and not_run.grade is None


def test_the_spec_takes_test_lth_defaults():
    spec = tester.run_tests(LAWS)[0].spec
    assert (spec.cases, spec.size, spec.seed, spec.where, spec.profile) == (100, 10, 0, [], [])
    assert spec.budgets["tries"] == 2000 and spec.budgets["coveringAbove"] == 20000
    assert spec.budgets["fuel"] == 3_000_000  # test.lth's, no longer certify.FUEL (7.S8)


def test_a_seed_is_deterministic_and_the_option_replaces_it():
    first = [tester.line(o) for o in tester.run_tests(LAWS)]
    assert first == [tester.line(o) for o in tester.run_tests(LAWS)]
    other = tester.run_tests(LAWS, seed=12345)
    assert all(o.spec.seed == 12345 for o in other)


def test_a_failure_on_a_case_is_reported_on_that_case(capsys):
    code, lines = lines_of(capsys, CASES)
    assert code == 1
    host, stuck, census, unbound, scoped, infinite = lines
    assert "unsettled" in host and "the first at x = -" in host and "math domain error" in host
    assert stuck == "Partial: exhaustive, 1 cases, unsettled: 1 cases raised, the first at b = false: stuck match (ran)"
    assert census == "DivisionAlgorithm: sampled (seed 0, size 10, placement ignored), 30 cases, sampled (ran)"
    assert "not run: m : IntegerDivision" in unbound and "bind a census (7.R4)" in unbound
    # numbers.lth's TimesMonotone over its own NonNegative (generators.lth defines one too)
    assert scoped == "TimesMonotone: sampled (seed 0, size 10, placement ignored), 30 cases, sampled (ran)"
    assert "not run: a : Int" in infinite


def test_a_census_weakens_the_coverage():
    outcomes = tester.run_tests(CASES)
    assert tester._base(outcomes[2].evidence.coverage) == "Drawn"  # weaker than the census's Listed


def test_a_file_without_test_lines(tmp_path, capsys):
    # the tester runs none; the checker refuses such a test program (12.R2), and `luthier test`
    # refuses a file that is not a test program
    path = tmp_path / "none.test.lut"
    path.write_text("x : Int := 1\n", encoding="utf-8")
    assert lines_of(capsys, path) == (0, [])
    model = tmp_path / "none.lut"
    model.write_text("x : Int := 1\n", encoding="utf-8")
    assert main(["test", str(model)]) == 1
    assert "`luthier test` takes a .test.lut file" in capsys.readouterr().err


def test_the_grade_is_test_lth_s_assumed_not_laws_lth_s():
    # test.lth's Grade and laws.lth's Evidence both have a constructor `Assumed`; the loader keeps
    # them apart (run.py, prompt-6.md), and `grade` gives test.lth's
    runner, _, loaded = tester.load_program(LAWS, 100000)
    con = tester._constructor(loaded)
    grade = runner.value(t.App(t.App(con("grade"), con("Assumes")), t.App(t.Var("just"), con("Exhaustive"))))
    assert grade == t.App(t.Var("just"), t.Var(loaded.name(tester._TEST_LTH, "AssumedGrade")))
    assert loaded.name(tester._TEST_LTH, "AssumedGrade") != loaded.name(tester._LAWS_LTH, "Assumed")
    assert tester._base(grade.argument) == "AssumedGrade"


def test_a_name_is_shown_as_its_file_writes_it():
    assert tester._show(t.App(t.Var("LeqBoth@numbers"), t.Var("doubles"))) == "(LeqBoth doubles)"


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="a few minutes; set LUTHIER_SLOW=1")
def test_the_laws_of_numbers_lth(capsys):
    _, lines = lines_of(capsys, ROOT / "tests" / "tester" / "numbers_laws.test.lut")
    assert not any("refuted" in line for line in lines), lines
    # the log laws settle since the extern's arity is its declared type's (run.py, prompt-6.md)
    assert not any("unsettled" in line for line in lines), lines
    assert not any("@" in line for line in lines), lines


def test_an_exhaustive_run_is_the_whole_type_weakened_by_its_bindings():
    """test.lth's CoverageIsTheWeakest: `wholeCoverage` is `Exhaustive` weakened by the bindings."""
    plain, listed = tester.run_tests(ROOT / "tests" / "tester" / "weakest.test.lut")
    assert tester._base(plain.evidence.coverage) == "Exhaustive" and plain.verdict == "Confirmed"
    assert tester._base(listed.evidence.coverage) == "Listed" and listed.verdict == "Supported"


BOX = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Bounded
SquareNonNegative (x : Int) : Bool := x * x >= 0
box : List Int := [-1, 0, 1]
test "SquareNonNegative" ExhaustiveMode (whereBindings <- [{ parameter := just "x", type := nothing, generator := "box", coverage := Bounded 1 }])
'''


OVER_A_TYPE = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
SelfEqual (A : U) (eq : A -> A -> Bool) (x : A) : Bool := eq x x
types : List U := [Bool]
eqs : List (Bool -> Bool -> Bool) := [fn a b { a == b }]
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
test "SelfEqual" ExhaustiveMode (whereBindings <- [bind "eq" "eqs"])
test "SelfEqual" ExhaustiveMode (whereBindings <- [bind "A" "types", bind "eq" "eqs"])
'''


def test_a_law_quantified_over_a_type_the_line_does_not_name_is_a_static_error(tmp_path):
    # D-2026-10-16-l, L5 (7.R2): refused at the line's start, before anything is drawn or looked up,
    # with the static error's reason; the line that names the instance (a census of types) runs
    path = tmp_path / "overu.test.lut"
    path.write_text(OVER_A_TYPE, encoding="utf-8")
    unnamed, named = tester.run_tests(path)
    assert isinstance(unnamed.evidence, tester.NotRun)
    assert "A : U: the law is quantified over a type, a static error (7.R2)" in unnamed.evidence.reason
    assert (named.verdict, named.evaluated) == ("Supported", 2)


def test_every_value_of_a_box_confirmed_is_confirmed_on_that_box(tmp_path):
    # D-2026-10-16-k item 17: `Bounded n` is a domain, not a grade; laws.lth's ForallOnPoints
    # confirms on the box, as on the whole type, and test.lth grades it exhaustive (7.S10)
    path = tmp_path / "box.test.lut"
    path.write_text(BOX, encoding="utf-8")
    outcome, = tester.run_tests(path)
    assert tester._base(outcome.evidence.coverage) == "Bounded"
    assert (outcome.verdict, outcome.grade) == ("Confirmed", "ExhaustiveGrade")


SHAPES = '''import "test.lth" test ExhaustiveMode SampledMode
import "generators_model.lut" linear
import "generators.lth" Binding
import "laws.lth" Listed
import "arrays.lth" Dim VecOf MatOf Square
VecHasItsLength (n : Dim) (x : VecOf n) : Bool := x.n == n and x.f (n - 1) == x.f (n - 1)
MatHasItsShape (r c : Dim) (a : MatOf r c) : Bool := a.m == r and a.n == c and a.f (r - 1) (c - 1) <= 10.0
SquareIsSquare (a : Square) : Bool := a.m == a.n
size (xs : List Int) : Int := match xs { nil -> 0 ; cons x rest -> 1 + size rest }
AtMostTwo (xs : List Int) : Bool := size xs <= 2
lists : List (List Int) := [nil, [1, 2], [3]]
test "VecHasItsLength" (SampledMode linear)
test "MatHasItsShape" (SampledMode linear)
test "SquareIsSquare" (SampledMode linear)
test "AtMostTwo" ExhaustiveMode (whereBindings <- [{ parameter := just "xs", type := nothing, generator := "lists", coverage := Listed }])
'''


def test_arrays_are_drawn_and_a_census_of_lists_lists_its_elements(tmp_path, capsys):
    # record/IA/evidence-2026-10-14/prompt.md: a `Fin n -> Float64` is drawn as the host array it
    # is, a field a refinement equates to a value is built (`VecOf n`, `MatOf r c`, `Square`), and
    # a census of lists for a parameter that is a list gives its elements
    program = tmp_path / "shapes.test.lut"
    program.write_text(SHAPES)
    code, lines = lines_of(capsys, program)
    assert code == 0
    assert lines == [
        "VecHasItsLength: sampled (seed 0, size 10, placement ignored), 100 cases, sampled (ran)",
        "MatHasItsShape: sampled (seed 0, size 10, placement ignored), 100 cases, sampled (ran)",
        "SquareIsSquare: sampled (seed 0, size 10, placement ignored), 100 cases, sampled (ran)",
        "AtMostTwo: exhaustive, 3 cases, cases (ran)",
    ]


GENERATED = '''import "test.lth" test ExhaustiveMode SampledMode
import "generators_model.lut" linear symmetricOf orthogonal unitList
import "generators.lth" Gen Seed byParameter
import "arrays.lth" Dim MatOf SymmetricOf SymmetricMatrix Vec
import "probability.lth" UnitList unitVec
counter : Gen Int := fn n s { (s mod 7, (s * 1103515245 + 12345) mod 2147483648) }
wide : Gen Int := fn n s { (s mod 70, (s + 1) mod 2147483648) }
Seven : U := { x : Int | 0 <= x and x < 7 }
InSeven (x : Seven) : Bool := x < 7
Rotated (k : Dim) (q : MatOf k k) (s : SymmetricOf k) : Bool := q.m == k and s.m == k
AllUnit (vs : UnitList) : Bool := all List (Vec Float64) unitVec vs
IsSquare (s : SymmetricMatrix) : Bool := s.m == s.n
test "InSeven" (SampledMode linear) (whereBindings <- [byParameter "x" "counter"])
test "InSeven" (SampledMode linear) (whereBindings <- [byParameter "x" "wide"])
test "InSeven" ExhaustiveMode (whereBindings <- [byParameter "x" "counter"])
test "Rotated" (SampledMode linear) (cases <- 10) (whereBindings <- [byParameter "q" "orthogonal", byParameter "s" "symmetricOf"])
test "AllUnit" (SampledMode linear) (cases <- 10) (whereBindings <- [byParameter "vs" "unitList"])
test "IsSquare" (SampledMode linear) (cases <- 10) (whereBindings <- [byParameter "s" "orthogonal"])
'''


def test_a_binding_names_a_generator(tmp_path, capsys):
    # record/IA/tester-2026-10-14/prompt-3.md: a binding names a value of `Gen T`, in Luthier
    # (`counter`) or the host's (generators_model.lut), or a family reading an earlier parameter
    # (`orthogonal k`); what it gives is checked against the parameter's type (7.S1)
    program = tmp_path / "generated.test.lut"
    program.write_text(GENERATED)
    code, lines = lines_of(capsys, program)
    assert code == 1
    luthier, invalid, exhaustive, family, host, unread = lines
    assert luthier == "InSeven: sampled (seed 0, size 10, placement ignored), 100 cases, sampled (ran)"
    assert "not run: x : Seven: the generator wide gave a value outside Seven at seed 7 (7.S1)" in invalid
    assert "not run: x is bound to the generator counter: ExhaustiveMode lists values" in exhaustive
    assert family == "Rotated: sampled (seed 0, size 10, placement ignored), 10 cases, sampled (ran)"
    assert host == "AllUnit: sampled (seed 0, size 10, placement ignored), 10 cases, sampled (ran)"
    assert "the generator orthogonal reads k, which the law does not quantify before this parameter" in unread


def test_a_generator_threads_its_seed_and_its_entry_names_it(tmp_path):
    program = tmp_path / "generated.test.lut"
    program.write_text(GENERATED)
    outcomes = tester.run_tests(program)
    drawn = [case[0].constant.value for case, _ in outcomes[0].evidence.cases]
    seed, expected = 0, []
    for _ in range(100):  # counter's values, the seed threaded from the spec's (7.S1)
        expected.append(seed % 7)
        seed = (seed * 1103515245 + 12345) % 2 ** 31
    assert drawn == expected
    assert tester._base(outcomes[0].evidence.coverage) == "Drawn"
    binding = outcomes[3].entry["binding"]
    assert [b["generator"] for b in binding[1:]] == ["orthogonal k (generator, size 10)",
                                                     "symmetricOf k (generator, size 10)"]
    assert all(b["fingerprint"].startswith("sha256:") for b in binding[1:])
    assert any(route == "python:luthier.generators.orthogonal" for route, _ in outcomes[3].entry["hosts"])
    assert tester.run_tests(program)[0].evidence.cases == outcomes[0].evidence.cases


def test_the_host_generators_give_their_family_and_the_next_seed():
    import numpy as np
    from luthier import generators as g
    a, s1 = g.symmetric(10, 5)
    assert np.array_equal(a, a.T) and 0 <= s1 < 2 ** 31 and g.symmetric(10, 5)[1] == s1
    q, _ = g.orthogonal(7, 10, 5)
    assert np.allclose(q.T @ q, np.eye(7), atol=1e-13)
    p, _ = g.gram(10, 5)
    assert np.all(np.linalg.eigvalsh(p) >= -1e-9 * max(1.0, np.abs(p).max()))
    vs, _ = g.unit_list(0.5, 10, 5)
    assert all(((0.0 <= v) & (v <= 1.0)).all() for v in vs)
    d, _ = g.clear_diagonal(0.25, 1.0, 1000.0, 10, 5)
    assert all(x == 0.0 or 1.0 <= abs(x) <= 1000.0 for x in d)


# ---------------------------------------------------------------------- controls (7.S19, L9.14)
# record/IA/controls-2026-10-15/prompt-tester.md: a line `(control <- true)` (test.lth's `control`)
# is a law tested on a model broken on purpose, expected to be refuted

CONTROLS = ROOT / "tests" / "tester" / "tables_controls.test.lut"


def test_a_control_line_is_read_and_its_refutation_is_the_control_passing(capsys):
    outcomes = tester.run_tests(CONTROLS)
    outcome = outcomes[0]  # the first line, CellsOfTheirKind on holeT; the others as it
    assert all(o.spec.control and o.verdict == "Refuted" and tester.passes(o) for o in outcomes)
    assert outcome.spec.control and outcome.verdict == "Refuted" and outcome.grade is None
    assert tester.passes(outcome)
    assert outcome.entry["kind"] == "Control" and outcome.entry["grade"] is None
    assert outcome.entry["outcome"] == {"ControlRefuted": "t = holeT"}
    code, lines = lines_of(capsys, CONTROLS)
    assert code == 0  # the control passed: `luthier test` succeeds
    assert lines[0] == ("control of CellsOfTheirKind: exhaustive, 1 cases, refuted at t = holeT: "
                        "the control passed (ran)")
    # ten since core bite 11 (TableIsIndexed, TableIsAnObject), twelve since 5ca7e15 (the symmetry and
    # the transitivity of the tables' equality)
    # [bite D1] a control of a conjunction prints a line per conjunct below its own
    lines = [line for line in lines if not line.startswith("  ")]
    assert len(lines) == 12 and all(line.endswith(": the control passed (ran)") for line in lines)


def test_a_law_line_is_no_control_by_default():
    assert not any(o.spec.control for o in tester.run_tests(LAWS))
    assert all("kind" not in o.entry for o in tester.run_tests(LAWS))


def test_a_control_its_law_holds_on_is_a_failed_control(tmp_path, capsys):
    path = tmp_path / "held.test.lut"
    path.write_text('import "test.lth" test ExhaustiveMode\n'
                    'LocalReflexive (a : Bool) : Bool := a == a\n'
                    'test "LocalReflexive" ExhaustiveMode (control <- true)\n', encoding="utf-8")
    outcome, = tester.run_tests(path)
    assert outcome.verdict == "Confirmed" and not tester.passes(outcome)
    assert outcome.entry["outcome"] == {"ControlConfirmed": "exhaustive"} and outcome.entry["grade"] is None
    code, lines = lines_of(capsys, path)
    assert code == 1
    assert lines == ["control of LocalReflexive: exhaustive, 2 cases, CONTROL FAILED: the law held on the model "
                     "broken on purpose, too weak to see the break (7.S19) (exhaustive) (ran)"]


# ---------------------------------------------------------------------- statistical laws (laws.lth §4)
# record/IA/statistical-2026-10-15/prompt-tester.md (7.S17 to 7.S19, L9.15, D-2026-10-15-b): a law
# whose value is `Statistical S T l draw c` runs Wald's sequential test once, from the line's seed,
# at the cutoffs bound as a census of one; constant streams of p-values, as report-theory.md checked
# them by hand: p = 0 fails at 8 samples, p = 1 holds at 2, p = 0.5 is unresolved at the budget

STATISTICAL = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Seed Binding
import "laws.lth" Law Statistical StatisticalLaw Sequential byPValue Listed
pv : StatisticalLaw Float64 := byPValue Float64 (fn p { p })
AtZero (c : Sequential) : Law := Statistical Float64 Seed pv (fn n s { (0.0, s) }) c
AtOne (c : Sequential) : Law := Statistical Float64 Seed pv (fn n s { (1.0, s) }) c
AtHalf (c : Sequential) : Law := Statistical Float64 Seed pv (fn n s { (0.5, s) }) c
OnPairs (c : Sequential) : Law := Statistical Float64 Int pv (fn n s { (1.0, s) }) c
wald : Sequential := { alpha := 0.01, beta := 0.01, delta := 0.9, initial := 1, budget := 400 }
twice : List Sequential := [wald, wald]
broken : Sequential := { alpha := 0.6, beta := 0.6, delta := 0.9, initial := 1, budget := 400 }
cutoffs : List Binding := [ { parameter := just "c", type := nothing, generator := "wald", coverage := Listed } ]
both : List Binding := [ { parameter := just "c", type := nothing, generator := "twice", coverage := Listed } ]
bad : List Binding := [ { parameter := just "c", type := nothing, generator := "broken", coverage := Listed } ]
test "AtZero" ExhaustiveMode (seed <- 3) (profile <- cutoffs)
test "AtOne" ExhaustiveMode (seed <- 3) (profile <- cutoffs)
test "AtHalf" ExhaustiveMode (seed <- 3) (profile <- cutoffs)
test "AtZero" ExhaustiveMode (seed <- 3) (profile <- cutoffs) (control <- true)
test "AtOne" ExhaustiveMode (seed <- 3) (profile <- cutoffs) (control <- true)
test "AtOne" ExhaustiveMode (seed <- 3)
test "AtOne" ExhaustiveMode (seed <- 3) (profile <- both)
test "AtOne" ExhaustiveMode (seed <- 3) (profile <- bad)
test "OnPairs" ExhaustiveMode (seed <- 3) (profile <- cutoffs)
'''
RATES = "by the sequential test (alpha 0.01, beta 0.01, delta 0.9, budget 400)"


def test_a_statistical_law_runs_the_sequential_test(tmp_path):
    path = tmp_path / "statistical.test.lut"
    path.write_text(STATISTICAL, encoding="utf-8")
    fails, holds, unresolved, *_ = tester.run_tests(path)
    # laws.lth's StatisticalByTest: Fails refutes, Holds supports (sampled over Drawn seed), Unresolved
    # settles nothing; the evidence is `Tested` with the rates and what was spent
    assert (fails.verdict, fails.grade, fails.evidence.verdict, fails.evidence.spent) == ("Refuted", None, "Fails", 8)
    assert (holds.verdict, holds.grade, holds.evidence.spent) == ("Supported", "Sampled", 2)
    assert tester._show(holds.evidence.coverage) == "(Drawn 3)"
    assert (unresolved.verdict, unresolved.grade, unresolved.evidence.spent) == ("Unsettled", None, 400)
    # the ratio the test stopped at, from which a later stretch would continue it (D-2026-10-16-g)
    assert abs(holds.entry["evidence"].pop("ratio") - 0.01) < 1e-12
    assert holds.entry["evidence"].pop("cutoffs") == "c"  # left out of the union's binding (D-2026-10-16-g)
    assert holds.entry["evidence"] == {"Tested": {"verdict": "Holds", "alpha": 0.01, "beta": 0.01, "delta": 0.9,
                                                  "spent": 2, "initial": 1, "budget": 400}, "coverage": "(Drawn 3)"}
    assert (holds.entry["outcome"], holds.entry["grade"]) == ("Passed", "Sampled")
    assert fails.entry["outcome"] == {"Failed": f"8 samples of 1 {RATES}"}
    assert list(unresolved.entry["outcome"]) == ["Unresolved"] and unresolved.entry["outcome"]["Unresolved"]["spent"] == 400
    assert holds.entry["binding"] == [{"parameter": "c", "generator": "wald (Listed)",
                                       "fingerprint": holds.entry["binding"][0]["fingerprint"]}]


BUILT = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
one : Int := 1
double (x : Int) : Int := x + x
xs : List Int := [one, double 2]
Positive (x : Int) : Bool := x > 0
test "Positive" ExhaustiveMode (whereBindings <- [{ parameter := just "x", type := nothing, generator := "xs", coverage := Listed }])
'''


def test_a_census_built_by_an_expression_changes_its_fingerprint_when_its_members_change(tmp_path):
    # 3h's finding: a census that names some members and builds others (`[one, double 2]`) was
    # fingerprinted by its named members only, so a change to the code that builds the others left
    # the line known
    def fingerprint(text):
        path = tmp_path / "built.test.lut"
        path.write_text(text, encoding="utf-8")
        [outcome] = tester.run_tests(path)
        assert outcome.grade is not None
        return outcome.entry["binding"][0]["fingerprint"]
    base = fingerprint(BUILT)
    assert fingerprint(BUILT.replace("x + x", "2 * x")) != base          # the code that builds a member
    assert fingerprint(BUILT.replace("double 2", "double 3")) != base    # the expression itself
    assert fingerprint(BUILT.replace("one : Int := 1", "one : Int := 2")) != base  # a named member
    assert fingerprint(BUILT) == base
    # a census of names only keeps the hashes of its members, as a run naming one model reads them
    names = fingerprint(BUILT.replace("[one, double 2]", "[one]"))
    assert "," not in names and names.startswith("sha256:")


def test_the_lines_of_a_statistical_law(tmp_path, capsys):
    path = tmp_path / "statistical.test.lut"
    path.write_text(STATISTICAL, encoding="utf-8")
    code, lines = lines_of(capsys, path)
    assert code == 1
    assert lines == [
        f"AtZero: sequential (seed 3), 8 samples, refuted at 8 samples of 1 {RATES} (ran)",
        f"AtOne: sequential (seed 3), 2 samples, supported, sampled: held at 2 samples of 1 {RATES} (ran)",
        f"AtHalf: sequential (seed 3), 400 samples, unresolved at 400 samples of 1 {RATES} (ran)",
        # a statistical control passes on Fails, and fails when the test holds the law
        f"control of AtZero: sequential (seed 3), 8 samples, refuted at 8 samples of 1 {RATES}: "
        "the control passed (ran)",
        "control of AtOne: sequential (seed 3), 2 samples, CONTROL FAILED: the law held on the model broken on "
        f"purpose, too weak to see the break (7.S19) (sampled, held at 2 samples of 1 {RATES}) (ran)",
        # the cutoffs are the demand's: never drawn, one value, within Sequential's predicate
        "AtOne: exhaustive, 0 cases, not run: c : Sequential: the sequential test's cutoffs are the demand's "
        "and never drawn; bind them as a census of one (D-2026-10-14-c, L9.15) (ran)",
        "AtOne: exhaustive, 0 cases, not run: c: a statistical law runs once per line (L9.15); the census twice "
        "has 2 values, bind one (ran)",
        "AtOne: exhaustive, 0 cases, not run: the cutoffs { alpha := 0.6, beta := 0.6, delta := 0.9, initial := 1, "
        "budget := 400 } break Sequential's predicate (laws.lth `sequentialCutoffs`) (ran)",
        "OnPairs: exhaustive, 0 cases, not run: the stream's state is Int, not Seed: the seed is the test's "
        "(L9.15) (ran)",
    ]


def test_a_statistical_control_is_its_own_kind(tmp_path):
    path = tmp_path / "statistical.test.lut"
    path.write_text(STATISTICAL, encoding="utf-8")
    outcomes = tester.run_tests(path)
    passed, failed = outcomes[3], outcomes[4]
    assert tester.passes(passed) and not tester.passes(failed)
    assert passed.entry["kind"] == "Control" and passed.entry["grade"] is None
    assert passed.entry["outcome"] == {"ControlRefuted": f"8 samples of 1 {RATES}"}
    assert failed.entry["outcome"] == {"ControlConfirmed": f"sampled, held at 2 samples of 1 {RATES}"}


def test_a_type_a_census_lists_is_no_model_home():
    # probability_laws.test.lut binds `S : U` to `[UnitList]`: probability.lth is no model whose store
    # takes the entry; numpy's sort's file is (its `SourceIsUniform` line, the contrast before, went
    # to generators_laws.test.lut as `UniformSampleIsUniform`'s; KolmogorovOfOne binds the same `d`)
    path = ROOT / "tests" / "tester" / "probability_laws.test.lut"
    runner, specs, loaded = tester.prepare(path)
    homes = {spec.law: [Path(h).name for h in tester.model_homes(loaded, spec, runner)] for spec in specs
             if spec.law in ("NoAlternativeAtZero", "KolmogorovOfOne")}
    assert homes == {"NoAlternativeAtZero": [], "KolmogorovOfOne": ["probability_model.lut"]}


def test_an_alias_or_a_constructor_is_no_model_home(tmp_path):
    # report-e.md, finding 1: demand_laws.test.lut and world_laws.test.lut as first written, with demand.lth's
    # alias `RunRecord` and world_model.lut's alias `WorldState` listed for a parameter `K : U` or `S :
    # Concrete`, and test.lth's constructor `Sampled` for `accepts : Grade`; none is a model, so
    # none of their files is a home. A model is a value whose type is the parameter's theory head:
    # certification_model.lut's `certifying : Certifying`, world_model.lut's `host : HostConsole`
    tester_dir = ROOT / "tests" / "tester"
    demand = (tester_dir / "demand_laws.test.lut").read_text(encoding="utf-8")
    assert "keyTypes : List U := [Key]" in demand
    (tmp_path / "demand_laws.test.lut").write_text(
        demand.replace("keyTypes : List U := [Key]", "keyTypes : List U := [RunRecord]"), encoding="utf-8")
    world = (tester_dir / "world_laws.test.lut").read_text(encoding="utf-8")
    first = (world.replace("cutoff : List Grade := [sampledCutoff, assumedCutoff]",
                           "cutoff : List Grade := [Sampled, AssumedGrade]")
             .replace('bind "S" "hostStates"', 'bind "S" "states"')
             .replace("hosts : List (Host WorldState) := [listedHost]", "hosts : List (Host WorldState) := [host]"))
    assert first.count('bind "S" "states"') > world.count('bind "S" "states"') and "[Sampled, AssumedGrade]" in first
    (tmp_path / "world_laws.test.lut").write_text(first, encoding="utf-8")
    homes = {}
    for name in ("demand_laws.test.lut", "world_laws.test.lut"):
        runner, specs, loaded = tester.prepare(tmp_path / name)
        for spec in specs:
            if spec.law in ("OneIdentityOneResult", "NoPriceRefusesAssumed", "AppliedWhenSettled", "HostAgreesPrint",
                            "PrintAppendsALine"):
                homes.setdefault(spec.law, [Path(h).name for h in tester.model_homes(loaded, spec, runner)])
    assert homes == {"OneIdentityOneResult": [], "NoPriceRefusesAssumed": ["certification_model.lut"],
                     "AppliedWhenSettled": [], "HostAgreesPrint": ["world_model.lut"],
                     "PrintAppendsALine": ["world_model.lut"]}


FIXED_CARRIER = '''import "test.lth" test SampledMode
import "generators_model.lut" linear
import "generators.lth" Binding
import "laws.lth" Listed

Machine (F : U) : { plus : F -> F -> F }
PlusOfZero (m : Machine Float64) (x : Float64) : Bool := m.plus x 0.0 == x
ZeroPlus (m : Machine Float64) (x : Float64) : Bool := m.plus 0.0 x == x
Machine (F : U) (m : Machine Float64) := PlusOfZero m & ZeroPlus m
machine : Machine Float64 := { plus := fn a b { a + b } }
models : List Binding := [
  { parameter := nothing, type := just "Machine", generator := "machine", coverage := Listed } ]

test "Machine" (SampledMode linear) (profile <- models)
'''


def test_a_structure_whose_laws_fix_its_carrier_runs_at_that_carrier(tmp_path):
    # the coordinator's (a) of 2026-10-22: `Doubles (F : U) (d : Doubles Float64) := ...` fixes `F`;
    # before, the line was not run, "F : U: a parameter of type U has no generator (7.R2)"
    top = tmp_path / "machine.test.lut"
    top.write_text(FIXED_CARRIER, encoding="utf-8")
    [o] = tester.run_tests(top)
    line = tester.line(o)
    assert "not run" not in line and "conjunction of 2" in line, line


VACUITY = ROOT / "tests" / "tester" / "vacuity.test.lut"


def test_a_law_whose_premise_never_holds_is_vacuous_and_not_run(capsys):
    """Wave A, bite A3 (D-2026-10-16-m): `x < 0 -> x > 0` over `Nat`, by `then`, by `if ... else true`
    and through a law that applies it, is laws.lth's `Vacuous n`, never a pass; a premise that held
    in some cases leaves the law run, with the count in its entry."""
    outcomes = tester.run_tests(VACUITY)
    by_law = {o.spec.law: o for o in outcomes}
    for law in ("NeverNegative", "NeverNegativeIf", "NeverNegativeApplied", "NeverNegativeOr"):
        o = by_law[law]
        assert isinstance(o.evidence, tester.Vacuous) and o.evidence.evaluated == 100
        assert o.grade is None and not tester.passes(o)
        assert o.entry["evidence"] == {"Vacuous": 100}
        assert o.entry["outcome"] == {"NotRunFor": tester.vacuity_reason(100)} and o.entry["grade"] is None
        assert "not run: vacuous" in tester.line(o)
    some = by_law["SometimesNegative"]
    assert some.grade == "Sampled" and 0 < some.held < some.evaluated == 100
    assert some.entry["evidence"]["Points"]["held"] == some.held
    assert "held" not in by_law["NothingIsFalse"].entry["evidence"]["Points"]  # states no premise
    assert by_law["NotNegative"].grade == by_law["TwoNegations"].grade == "Sampled"  # they state no premise


def test_an_empty_experiment_is_not_run_but_an_empty_type_enumerated_whole(capsys):
    """Bite A3 (7.S12): `cases <- 0` is an empty experiment, not run with its reason; `x : Empty` under
    ExhaustiveMode keeps its pass (`EmptyIsInitial`'s exception, bite 13c item 5)."""
    by_law = {o.spec.law: o for o in tester.run_tests(VACUITY)}
    empty = by_law["ZeroIsNeutral"]
    assert isinstance(empty.evidence, tester.NotRun) and "an empty experiment" in empty.evidence.reason
    assert empty.entry["outcome"] == {"NotRunFor": empty.evidence.reason} and empty.grade is None
    whole = by_law["NothingIsFalse"]
    assert (whole.verdict, whole.grade, whole.evaluated) == ("Confirmed", "ExhaustiveGrade", 0)
    code, _ = lines_of(capsys, VACUITY)
    assert code == 1  # the vacuous and the empty lines are not graded


def test_premises_are_read_from_then_from_if_else_true_and_through_an_applied_law():
    runner, specs, loaded = tester.prepare(VACUITY)
    count = {s.law: len(tester.premises_of(runner, tester._as_called(loaded, s.law))) for s in specs}
    assert count == {"NeverNegative": 1, "NeverNegativeIf": 1, "NeverNegativeApplied": 1, "NeverNegativeOr": 1,
                     "NotNegative": 0, "TwoNegations": 0, "SometimesNegative": 1, "ZeroIsNeutral": 0, "NothingIsFalse": 0}


# ---------------------------------------------------------------------- a control over a conjunction, partly known
# report-controls-M.md 3.2: a control line over a conjunction whose refuting conjunct's entry is known
# while the line's own entry is new (a binding reaching one conjunct only) crashed in `settle`, which
# read `.coverage` from the reused outcome's evidence, the store's dict

PARTS = '''LeftZero (f : Int -> Int -> Int) (x : Int) : Bool := f 0 x == x
Swaps (f : Int -> Int -> Int) (a : Int) (b : Int) : Bool := f a b == f b a
LocalPair (f : Int -> Int -> Int) := LeftZero f & Swaps f
'''
PARTS_LINES = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "parts.lut" LocalPair
broken : Int -> Int -> Int := fn a b { if a == 0 then b else a }
small : List Int := [0, 1, 2]
other : List Int := [0, 2]
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
ofType (t g : String) : Binding := { parameter := nothing, type := just t, generator := g, coverage := Listed }
profile : List Binding := [bind "f" "broken", ofType "Int" "small"EXTRA]
test "LocalPair" ExhaustiveMode (whereBindings <- profile) (control <- true)
'''


def test_a_control_over_a_conjunction_settles_from_a_known_refuting_conjunct(tmp_path):
    (tmp_path / "parts.lut").write_text(PARTS, encoding="utf-8")
    path = tmp_path / "parts.test.lut"
    path.write_text(PARTS_LINES.replace("EXTRA", ""), encoding="utf-8")
    first, = tester.run_tests(path, store=True)
    assert first.verdict == "Refuted" and tester.passes(first)
    # `x` bound by name reaches `LeftZero` alone: `Swaps`, the refuting conjunct, stays known
    path.write_text(PARTS_LINES.replace("EXTRA", ', bind "x" "other"'), encoding="utf-8")
    again, = tester.run_tests(path, store=True)
    assert [o.known is not None for o in again.parts] == [False, True]
    assert again.known is None and again.verdict == "Refuted" and tester.passes(again)
    assert again.entry["outcome"] == first.entry["outcome"]
    assert again.entry["evidence"]["Points"]["verdict"] == "Refuted"
    assert again.entry["evidence"]["Points"]["coverage"] == first.entry["evidence"]["Points"]["coverage"]
    assert tester.line(again).splitlines()[0] == ("control of LocalPair: exhaustive, 11 cases, refuted at "
                                                  "Swaps f: f = broken, a = 1, b = 2: the control passed (ran)")


# ---------------------------------------------------------------------- a census of the wrong type
# report-controls-M.md 3.1: a binding by name reaches every conjunct with a parameter of that name; a
# census whose values are not of the parameter's type ran the law on them (integers for verdicts)

MISTYPED = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
LocalExcluded (x : Bool) : Bool := x or not x
LocalSquare (x : Int) : Bool := x * x >= 0
LocalBoth (k : Int) := LocalExcluded & LocalSquare
ints : List Int := [0, 1]
bools : List Bool := [true, false]
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
onInts : List Binding := [bind "x" "ints"]
fine : List Binding := [bind "x" "bools"]
test "LocalExcluded" ExhaustiveMode (whereBindings <- onInts)
test "LocalSquare" ExhaustiveMode (whereBindings <- onInts)
test "LocalExcluded" ExhaustiveMode (whereBindings <- fine)
test "LocalBoth" ExhaustiveMode (whereBindings <- [bind "k" "ints", bind "x" "ints"])
'''


def test_a_census_of_another_type_than_its_parameter_is_refused(tmp_path):
    path = tmp_path / "mistyped.test.lut"
    path.write_text(MISTYPED, encoding="utf-8")
    refused, square, fine, conjunction = tester.run_tests(path)
    assert isinstance(refused.evidence, tester.NotRun) and refused.evaluated == 0 and not tester.passes(refused)
    reason = refused.evidence.reason
    assert "x : Bool" in reason and "the census ints" in reason and "Int" in reason
    assert square.grade is not None and square.evaluated == 2
    assert fine.grade is not None and fine.evaluated == 2
    # in a conjunction, the conjunct whose `x` is a Bool is refused, the one whose `x` is an Int runs
    excluded, squared = conjunction.parts
    assert isinstance(excluded.evidence, tester.NotRun) and "x : Bool" in excluded.evidence.reason
    assert squared.grade is not None and squared.evaluated == 4
    # refused at the line's start: nothing stored, nothing known reused
    stored = tester.run_tests(path, store=True)[0]
    assert isinstance(stored.evidence, tester.NotRun) and stored.known is None
    entries = json.loads((tmp_path / "mistyped.test.cert.json").read_text(encoding="utf-8"))
    assert entries and all("NotRun" not in e["evidence"] for e in entries)


# [bite C2, record/plan/audit-algebras-2026-10-22/execution.md; L9.17, D-2026-10-18-d] A numerical law
# whose bound is a parameter of type `Bound` (resources.lth), run at a list of bounds the line gives:
# the tester records, per bound, the cases, the worst ratio and the fuel each case spent, the measured
# resource the scaling law of the algorithm's theory is read against.
SCALING = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Law Within Case Listed
import "resources.lth" Bound
gap (a b : Float64) : Float64 := if a < b then b - a else a - b
halvings (w t : Float64) : Nat := if w <= t then 0 else 1 + halvings (w / 2.0) t
-- one halved down to the bound and back: exact, so the ratio is zero; its cost grows as log2 (1 / b)
Halves (b : Bound) (x : Int) : Law := Within Float64 gap b (toFloat64 x) (toFloat64 x + 0.0 * toFloat64 (halvings 1.0 b))
-- the same with an integer in place of the bound: no scaling record
Plain (k : Int) (x : Int) : Law := Within Float64 gap 1.0 (toFloat64 x) (toFloat64 (x + 0 * halvings 1.0 (toFloat64 k)))
bounds : List Bound := [0.5, 1.0e-3, 1.0e-6, 1.0e-9]
one : List Bound := [1.0e-3]
xs : List Int := [1, 2, 3]
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
test "Halves" ExhaustiveMode (whereBindings <- [bind "b" "bounds", bind "x" "xs"])
test "Halves" ExhaustiveMode (whereBindings <- [bind "b" "one", bind "x" "xs"])
test "Plain" ExhaustiveMode (whereBindings <- [bind "k" "xs", bind "x" "xs"])
'''


def test_a_numerical_law_run_at_a_list_of_bounds_records_the_fuel_per_bound(tmp_path):
    path = tmp_path / "scaling.test.lut"
    path.write_text(SCALING, encoding="utf-8")
    halves, single, plain = tester.run_tests(path)
    assert halves.verdict == "Supported" and halves.measured["worst"] == 0.0
    scaling = halves.measured["scaling"]
    assert scaling["parameter"] == "b" and scaling["resource"] == "fuel"
    # the bounds from the loosest down, each with its three cases, its worst ratio, and what it spent
    assert [s["bound"] for s in scaling["bounds"]] == [0.5, 1.0e-3, 1.0e-6, 1.0e-9]
    assert all(s["cases"] == 3 and s["worst"] == 0.0 for s in scaling["bounds"])
    fuel = [s["fuel"] for s in scaling["bounds"]]
    assert all(isinstance(f, int) and f > 0 for f in fuel) and fuel == sorted(fuel) and fuel[0] < fuel[-1]
    assert all(s["least"] <= s["fuel"] for s in scaling["bounds"])
    assert halves.entry["measured"]["scaling"] == scaling  # kept in the entry
    assert "fuel per case" in tester.line(halves) and "4 bounds" in tester.line(halves)
    # one bound is no scaling, and a parameter that is not a `Bound` is none either
    assert "scaling" not in single.measured and "scaling" not in plain.measured
