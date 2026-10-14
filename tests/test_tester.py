"""`luthier test`, bite 1 (record/IA/tester-2026-10-14/prompt.md): test.lth's Tester over the
programs under tests/tester/; names scoped by run.py's loader since run.py bite 6 (prompt-6.md)."""
import os
from pathlib import Path

import pytest

from luthier import term as t, tester
from luthier.cli import main

ROOT = Path(__file__).resolve().parents[1]
LAWS = ROOT / "tests" / "tester" / "laws.lut"
CASES = ROOT / "tests" / "tester" / "cases.lut"


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
        "PlusCommutes: sampled (seed 7, size 10, metric ignored), 200 cases, sampled (ran)",
        "Small: sampled (seed 0, size 10, metric ignored), 100 cases, sampled (ran)",
        "Small: sampled (seed 0, size 1000, metric ignored), 100 cases, refuted at x = 729 (ran)",
        "PlusCommutes: exhaustive, 0 cases, not run: x : Int: Int is infinite: "
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
    assert census == "DivisionAlgorithm: sampled (seed 0, size 10, metric ignored), 30 cases, sampled (ran)"
    assert "not run: m : IntegerDivision" in unbound and "bind a census (7.R4)" in unbound
    # numbers.lth's LeqTransitive over its own LeqChain (kernel_laws.lth and algebra.lth define one too)
    assert scoped == "LeqTransitive: sampled (seed 0, size 10, metric ignored), 30 cases, sampled (ran)"
    assert "not run: a : Int" in infinite


def test_a_census_weakens_the_coverage():
    outcomes = tester.run_tests(CASES)
    assert tester._base(outcomes[2].evidence.coverage) == "Drawn"  # weaker than the census's Listed


def test_a_file_without_test_lines(tmp_path, capsys):
    path = tmp_path / "none.lut"
    path.write_text("x : Int := 1\n", encoding="utf-8")
    assert lines_of(capsys, path) == (0, [])


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
    _, lines = lines_of(capsys, ROOT / "tests" / "tester" / "numbers_laws.lut")
    assert not any("refuted" in line for line in lines), lines
    # the log laws settle since the extern's arity is its declared type's (run.py, prompt-6.md)
    assert not any("unsettled" in line for line in lines), lines
    assert not any("@" in line for line in lines), lines


def test_an_exhaustive_run_is_the_whole_type_weakened_by_its_bindings():
    """test.lth's CoverageIsTheWeakest: `wholeCoverage` is `Exhaustive` weakened by the bindings."""
    plain, listed = tester.run_tests(ROOT / "tests" / "tester" / "weakest.lut")
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
    program = tmp_path / "shapes.lut"
    program.write_text(SHAPES)
    code, lines = lines_of(capsys, program)
    assert code == 0
    assert lines == [
        "VecHasItsLength: sampled (seed 0, size 10, metric ignored), 100 cases, sampled (ran)",
        "MatHasItsShape: sampled (seed 0, size 10, metric ignored), 100 cases, sampled (ran)",
        "SquareIsSquare: sampled (seed 0, size 10, metric ignored), 100 cases, sampled (ran)",
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
Unit (vs : UnitList) : Bool := allUnit vs
IsSquare (s : Symmetric) : Bool := s.m == s.n
test "InSeven" (SampledMode linear) (whereBindings <- [byParameter "x" "counter"])
test "InSeven" (SampledMode linear) (whereBindings <- [byParameter "x" "wide"])
test "InSeven" ExhaustiveMode (whereBindings <- [byParameter "x" "counter"])
test "Rotated" (SampledMode linear) (cases <- 10) (whereBindings <- [byParameter "q" "orthogonal", byParameter "s" "symmetricOf"])
test "Unit" (SampledMode linear) (cases <- 10) (whereBindings <- [byParameter "vs" "unitList"])
test "IsSquare" (SampledMode linear) (cases <- 10) (whereBindings <- [byParameter "s" "orthogonal"])
'''


def test_a_binding_names_a_generator(tmp_path, capsys):
    # record/IA/tester-2026-10-14/prompt-3.md: a binding names a value of `Gen T`, in Luthier
    # (`counter`) or the host's (generators_model.lut), or a family reading an earlier parameter
    # (`orthogonal k`); what it gives is checked against the parameter's type (7.S1)
    program = tmp_path / "generated.lut"
    program.write_text(GENERATED)
    code, lines = lines_of(capsys, program)
    assert code == 1
    luthier, invalid, exhaustive, family, host, unread = lines
    assert luthier == "InSeven: sampled (seed 0, size 10, metric ignored), 100 cases, sampled (ran)"
    assert "not run: x : Seven: the generator wide gave a value outside Seven at seed 7 (7.S1)" in invalid
    assert "not run: x is bound to the generator counter: ExhaustiveMode lists values" in exhaustive
    assert family == "Rotated: sampled (seed 0, size 10, metric ignored), 10 cases, sampled (ran)"
    assert host == "Unit: sampled (seed 0, size 10, metric ignored), 10 cases, sampled (ran)"
    assert "the generator orthogonal reads k, which the law does not quantify before this parameter" in unread


def test_a_generator_threads_its_seed_and_its_entry_names_it(tmp_path):
    program = tmp_path / "generated.lut"
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
