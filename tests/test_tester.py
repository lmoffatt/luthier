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
    code = main(["test", *map(str, args)])
    return code, capsys.readouterr().out.splitlines()


def test_the_five_kinds_of_outcome(capsys):
    code, lines = lines_of(capsys, LAWS)
    assert code == 1  # a law is refuted and one is not run
    assert lines == [
        "NotInvolutive: exhaustive, 2 cases, exhaustive",
        "AndIsOr: exhaustive, 4 cases, refuted at a = true, b = false",
        "PlusCommutes: sampled (seed 7, size 10, metric ignored), 200 cases, sampled",
        "Small: sampled (seed 0, size 10, metric ignored), 100 cases, sampled",
        "Small: sampled (seed 0, size 1000, metric ignored), 100 cases, refuted at x = 729",
        "PlusCommutes: exhaustive, 0 cases, not run: x : Int: Int is infinite: "
        "ExhaustiveMode needs its bounds or a census (7.R3)",
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
    assert stuck == "Partial: exhaustive, 1 cases, unsettled: 1 cases raised, the first at b = false: stuck match"
    assert census == "DivisionAlgorithm: sampled (seed 0, size 10, metric ignored), 30 cases, sampled"
    assert "not run: m : IntegerDivision" in unbound and "bind a census (7.R4)" in unbound
    # numbers.lth's LeqTransitive over its own LeqChain (kernel_laws.lth and algebra.lth define one too)
    assert scoped == "LeqTransitive: sampled (seed 0, size 10, metric ignored), 30 cases, sampled"
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
    assert grade == t.App(t.Var("just"), t.Var(loaded.name(tester._TEST_LTH, "Assumed")))
    assert loaded.name(tester._TEST_LTH, "Assumed") != loaded.name(tester._LAWS_LTH, "Assumed")
    assert tester._base(grade.argument) == "Assumed"


def test_a_name_is_shown_as_its_file_writes_it():
    assert tester._show(t.App(t.Var("LeqBoth@numbers"), t.Var("doubles"))) == "(LeqBoth doubles)"


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="a few minutes; set LUTHIER_SLOW=1")
def test_the_laws_of_numbers_lth(capsys):
    _, lines = lines_of(capsys, ROOT / "tests" / "tester" / "numbers_laws.lut")
    assert not any("refuted" in line for line in lines), lines
    # the log laws settle since the extern's arity is its declared type's (run.py, prompt-6.md)
    assert not any("unsettled" in line for line in lines), lines
    assert not any("@" in line for line in lines), lines
