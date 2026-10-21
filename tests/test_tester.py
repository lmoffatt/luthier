"""`luthier test`, bite 1 (record/IA/tester-2026-10-14/prompt.md): test.lth's Tester over the
programs under tests/tester/; names scoped by run.py's loader since run.py bite 6 (prompt-6.md)."""
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
    # numbers.lth's LeqTransitive over its own LeqChain (core/structures/algebraic.lth and algebra.lth define one too)
    assert scoped == "LeqTransitive: sampled (seed 0, size 10, placement ignored), 30 cases, sampled (ran)"
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
import "arrays.lth" Dim MatOf SymmetricOf Symmetric
import "probability.lth" UnitList allUnit
counter : Gen Int := fn n s { (s mod 7, (s * 1103515245 + 12345) mod 2147483648) }
wide : Gen Int := fn n s { (s mod 70, (s + 1) mod 2147483648) }
Seven : U := { x : Int | 0 <= x and x < 7 }
InSeven (x : Seven) : Bool := x < 7
Rotated (k : Dim) (q : MatOf k k) (s : SymmetricOf k) : Bool := q.m == k and s.m == k
AllUnit (vs : UnitList) : Bool := allUnit vs
IsSquare (s : Symmetric) : Bool := s.m == s.n
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
    assert len(lines) == 8 and all(line.endswith(": the control passed (ran)") for line in lines)


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
    # alias `Record` and world_model.lut's alias `State` listed for a parameter `K : U` or `S :
    # Concrete`, and test.lth's constructor `Sampled` for `accepts : Grade`; none is a model, so
    # none of their files is a home. A model is a value whose type is the parameter's theory head:
    # certification_model.lut's `certifying : Certifying`, world_model.lut's `host : HostConsole`
    tester_dir = ROOT / "tests" / "tester"
    demand = (tester_dir / "demand_laws.test.lut").read_text(encoding="utf-8")
    assert "keyTypes : List U := [Key]" in demand
    (tmp_path / "demand_laws.test.lut").write_text(
        demand.replace("keyTypes : List U := [Key]", "keyTypes : List U := [Record]"), encoding="utf-8")
    world = (tester_dir / "world_laws.test.lut").read_text(encoding="utf-8")
    first = (world.replace("cutoff : List Grade := [sampledCutoff, assumedCutoff]",
                           "cutoff : List Grade := [Sampled, AssumedGrade]")
             .replace('bind "S" "hostStates"', 'bind "S" "states"')
             .replace("hosts : List (Host State) := [listedHost]", "hosts : List (Host State) := [host]"))
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
