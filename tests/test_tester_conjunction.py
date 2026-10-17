"""The core's bite 4b (record/plan/core-2026-10-17/prompt-bite-4b.md; D-2026-10-18-f): the tester
splits a law whose body is a conjunction of partially applied laws into its conjuncts, and the region
classifier's two bounds are budgets of the line (7.S8, P11)."""
import random

from luthier import term as t, tester



# ---------------------------------------------------------------------- the classifier's bounds (7.S8)

BOUNDS = '''import "test.lth" test ExhaustiveMode
mat : { m n : Int, f : Int -> Int -> Float64 } := { m := 3, n := 3, f := fn i j { 1.5 } }
xs : List Float64 := [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
Trivial (b : Bool) : Bool := b or not b
test "Trivial" ExhaustiveMode
'''


def _classifier(runner, budgets):
    """A classifier over no law, reading the numbers of a value under `budgets`."""
    classifier = object.__new__(tester.Classifier)
    classifier.runner = runner
    classifier.values = tester.Values(runner, random.Random(0), 10, budgets, 100_000)
    return classifier


def test_the_classifier_bounds_are_the_line_s_budgets(tmp_path):
    path = tmp_path / "bounds.test.lut"
    path.write_text(BOUNDS, encoding="utf-8")
    runner, names, _ = tester.load_program(path, 1_000_000, ("mat", "xs"))
    specs = [tester.read_spec(runner, t.Var(n)) for n in names]
    assert specs[0].budgets["regionNumbers"] == 4000 and specs[0].budgets["regionEntries"] == 400
    loose = dict(specs[0].budgets)
    assert len(_classifier(runner, loose).numbers(t.Var("mat"), [])) == 9
    assert len(_classifier(runner, loose).numbers(t.Var("xs"), [])) == 8
    # a matrix written as a function with more entries than `regionEntries` gives the classifier none
    assert _classifier(runner, dict(loose, regionEntries=8)).numbers(t.Var("mat"), []) == []
    # at most `regionNumbers` doubles of a value are read (the one that crosses it included)
    assert len(_classifier(runner, dict(loose, regionNumbers=3)).numbers(t.Var("xs"), [])) == 4
