"""Numerical laws (laws.lth §5, `Within`) through the tester and the certifier: wave C, bite C1 of
record/plan/audit-algebras-2026-10-22/execution.md (D-2026-10-18-j, L9.18; the audit of 2026-10-22,
section 5, its boundary cases). Written 2026-10-25 by Claude Opus 5.5."""
from luthier import certify, tester
from luthier.cli import main
from luthier.run import demand_of

WITHIN = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Law Within Case Listed
gap (a b : Float64) : Float64 := if a < b then b - a else a - b
-- a quarter off against a bound of a half: ratio one half
Quarter (x : Int) : Law := Within Float64 gap 0.5 (toFloat64 x) (toFloat64 x + 0.25)
-- one off against a half: ratio two
TooFar (x : Int) : Law := Within Float64 gap 0.5 (toFloat64 x) (toFloat64 x + 1.0)
-- the boundary cases: no distance at a bound of zero (ratio zero), a distance at a bound of zero
-- (no finite ratio)
Exact (x : Int) : Law := Within Float64 gap 0.0 (toFloat64 x) (toFloat64 x)
AtZeroBound (x : Int) : Law := Within Float64 gap 0.0 (toFloat64 x) (toFloat64 x + 1.0)
-- the ratio grows with x inside the range, x / 4 at most three quarters; outside it nothing is claimed
Ranged (x : Int) : Law := if 0 <= x then Within Float64 gap 0.5 0.0 (toFloat64 x / 8.0) else Case true
-- a range no case falls in
NeverInRange (x : Int) : Law := if x < -1000 then Within Float64 gap 0.5 0.0 1.0 else Case true
small : List Int := [-1, 0, 1, 2, 3]
xs : List Binding := [ { parameter := just "x", type := nothing, generator := "small", coverage := Listed } ]
test "Quarter" ExhaustiveMode (profile <- xs)
test "TooFar" ExhaustiveMode (profile <- xs)
test "Exact" ExhaustiveMode (profile <- xs)
test "AtZeroBound" ExhaustiveMode (profile <- xs)
test "Ranged" ExhaustiveMode (profile <- xs)
test "NeverInRange" ExhaustiveMode (profile <- xs)
test "TooFar" ExhaustiveMode (profile <- xs) (control <- true)
'''


def _outcomes(tmp_path):
    path = tmp_path / "within.test.lut"
    path.write_text(WITHIN, encoding="utf-8")
    return tester.run_tests(path)


def test_a_within_law_is_measured_case_by_case_and_records_its_worst_ratio(tmp_path):
    quarter, too_far, exact, zero_bound, ranged, never, control = _outcomes(tmp_path)
    assert (quarter.verdict, quarter.grade) == ("Supported", "Cases")
    assert quarter.measured["measured"] == 5 and quarter.measured["worst"] == 0.5
    assert (quarter.measured["distance"], quarter.measured["bound"]) == (0.25, 0.5)
    assert quarter.entry["measured"]["worst"] == 0.5  # laws.lth's `Measured`, kept in the entry
    assert tester.line(quarter).endswith("cases, worst ratio 0.5 (ran)")
    # past the bound the comparison refutes, and the ratio says by how much
    assert too_far.verdict == "Refuted" and too_far.measured["worst"] == 2.0
    assert "worst ratio 2" in tester.line(too_far)
    # a control on a law past its bound passes
    assert control.verdict == "Refuted" and tester.passes(control)


def test_the_boundary_cases_of_the_ratio(tmp_path):
    _, _, exact, zero_bound, *_ = _outcomes(tmp_path)
    # no distance: ratio zero, at any bound, a bound of zero included
    assert exact.verdict == "Supported" and exact.measured["worst"] == 0.0
    # a distance at a bound of zero: refuted, no finite ratio
    assert zero_bound.verdict == "Refuted" and zero_bound.measured["worst"] is None
    assert "worst ratio unbounded" in tester.line(zero_bound)
    assert (tester.ratio_of(0.0, 0.0), tester.ratio_of(1.0, 0.0), tester.ratio_of(1.0, 4.0)) == (0.0, None, 0.25)
    assert tester.worse_ratio(0.5, None) is None and tester.worse_ratio(0.5, 0.75) == 0.75


def test_a_range_is_a_premise_and_a_range_never_met_is_vacuous(tmp_path):
    *_, ranged, never, _ = _outcomes(tmp_path)
    # the case outside the range (x = -1) is no measurement; the four inside are
    assert ranged.verdict == "Supported" and ranged.measured["measured"] == 4 and ranged.measured["worst"] == 0.75
    assert ranged.held == 4  # the premise `0 <= x`, read from `if p then Within ... else Case true`
    # no case in the range: laws.lth's `Vacuous n`, never a pass (D-2026-10-16-m)
    assert isinstance(never.evidence, tester.Vacuous) and never.grade is None


def test_a_demand_caps_the_worst_ratio_an_entry_serves_at():
    entry = {"law": "L", "cone": "sha256:c", "binding": [], "seed": 0, "cases": 10, "reach": [], "outcome": "Passed",
             "grade": "Sampled", "evidence": {"Points": {"evaluated": 10, "coverage": "(Drawn 0)", "verdict": "Supported"}},
             "measured": {"measured": 10, "worst": 0.7, "distance": 0.7, "bound": 1.0}}
    demand = {"law": "L", "cone": "sha256:c", "given": [], "accepts": "Sampled"}
    assert certify.serves(demand, entry)  # the default cap, one: every passed entry serves
    assert certify.serves({**demand, "bound": 0.8}, entry)
    assert not certify.serves({**demand, "bound": 0.5}, entry)
    # an unbounded worst serves no cap; an entry that measured nothing is not capped
    assert not certify.within_cap(10.0, None)
    assert certify.entry_bound({**entry, "measured": {"measured": 0, "worst": None}}) == 0.0
    # pooling keeps the largest worst over the union of the stretches (the three-levels report 2.5)
    other = {**entry, "seed": 1, "evidence": {"Points": {"evaluated": 10, "coverage": "(Drawn 1)", "verdict": "Supported"}},
             "measured": {"measured": 10, "worst": 0.9, "distance": 0.9, "bound": 1.0}}
    assert certify.pooled_worst([entry, other], "L", "sha256:c", certify.union_key(entry)) == 0.9


def test_the_demand_carries_and_records_its_bound():
    assert demand_of().bound == 1.0
    d = demand_of(bound=0.5)
    assert d.law("L", "sha256:c", [], {})["bound"] == 0.5 and d.record("sha256:c")["bound"] == 0.5
    assert d.inner("other").bound == 0.5
