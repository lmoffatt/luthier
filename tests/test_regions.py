"""The evidence of a law kept per region, in the code (record/IA/regions-2026-10-17/prompt-code.md;
D-2026-10-16-i, D-2026-10-16-j, L9.16; certification.lth §2, generators.lth §9): the special values
and the degenerate families of the generators, the tester's classification of each case, the entry's
regions and labels, and the certificate's grade read over them with the demand's combination."""
import random

import numpy as np
import pytest

from luthier import certify, generators, tester
from luthier.run import RunError, demand_of


# ---------------------------------------------------------------------- the generators (items 1, 2)

def test_special_values_are_in_the_support_and_hold_the_bounds_zero_and_the_cutoffs():
    values = generators.specials(0.0, 1.0, False, [1.0e-3])
    assert all(0.0 <= v <= 1.0 for v in values)
    assert {0.0, 1.0, 1.0e-3, 2.0e-3, 5.0e-4} <= set(values)
    assert -1.0 not in values
    assert generators.specials(-3, 3, True) == [-3, -2, 2, 3, 0, 1, -1]


def test_the_atom_at_zero_and_the_special_mass_are_the_budgets():
    rng = random.Random(1)
    drawn = [generators.special(rng, -10.0, 10.0, False, 0.0, 1.0) for _ in range(50)]
    assert drawn == [0.0] * 50  # the atom takes all the mass
    rng = random.Random(1)
    assert all(generators.special(rng, -10.0, 10.0, False, 0.0, 0.0) is None for _ in range(50))
    rng = random.Random(1)
    special = [generators.special(rng, 2.0, 10.0, False, 1.0, 1.0) for _ in range(50)]
    assert 0.0 not in special and all(v in generators.specials(2.0, 10.0, False) for v in special)


def test_the_symmetric_family_draws_the_census_of_dimensions_and_the_degenerate_matrices():
    shapes, zero, deficient = set(), 0, 0
    for seed in range(300):
        a, _ = generators.symmetric(10, seed)
        assert np.array_equal(a, a.T)
        shapes.add(a.shape[0])
        if a.size and not a.any():
            zero += 1
        elif a.shape[0] >= 2 and not a.any(axis=1).all():
            deficient += 1
    assert shapes == set(generators.DIMENSIONS)
    assert zero > 0 and deficient > 0
    assert {generators.symmetric(3, s)[0].shape[0] for s in range(100)} <= {0, 1, 2, 3}


# ---------------------------------------------------------------------- the tester (items 3, 4, 9, 10)

PROGRAM = '''
import "test.lth" test ExhaustiveMode SampledMode
import "generators_model.lut" linear
import "generators.lth" Binding DegenerateCase Degeneracies
import "laws.lth" Listed
import "numbers.lth" Tolerance
import "arrays.lth" Mat mat zeroMat

tolerance : Tolerance := 1.0e-3
cut : List Binding := [ { parameter := just "tol", type := nothing, generator := "tolerance", coverage := Listed } ]
corner : Degeneracies (Mat Float64) := { cases := [
  { name := "negative corner", holds := fn a { if a.m == 0 or a.n == 0 then false else a.f 0 0 < 0.0 }, witness := zeroMat 1 1 } ] }
threes : List (Mat Float64) := [mat Float64 3 3 (fn i j { 1.0 }), zeroMat 3 3]
listed : List Binding := [ { parameter := just "a", type := nothing, generator := "threes", coverage := Listed } ]
nats : List Int := [3, 4, 0 - 1]
badNat : List Binding := [ { parameter := just "k", type := nothing, generator := "nats", coverage := Listed } ]
Dims (a : Mat Float64) : Bool := a.m >= 0 and a.n >= 0
Small (tol : Tolerance) (x : Float64) : Bool := x * x >= 0.0
Count (k : Nat) : Bool := k >= 0
test "Dims" (SampledMode linear) (cases <- 200)
test "Dims" ExhaustiveMode (whereBindings <- listed)
test "Small" (SampledMode linear) (whereBindings <- cut)
test "Count" (SampledMode linear)
test "Count" ExhaustiveMode (whereBindings <- badNat)
'''


@pytest.fixture(scope="module")
def outcomes(tmp_path_factory):
    path = tmp_path_factory.mktemp("regions") / "regions.test.lut"
    path.write_text(PROGRAM, encoding="utf-8")
    return tester.run_tests(path, store=False)


def _regions(outcome):
    return {r["region"]["name"]: r["n"] for r in outcome.regions or ()}


def test_the_type_declares_its_cases_and_the_tester_counts_them(outcomes):
    drawn = _regions(outcomes[0])
    assert set(drawn) == {"zero", "0 x 0", "1 x 1", "rank deficient"}
    assert all(n > 0 for n in drawn.values())  # the generator gave every case mass
    assert all(r["region"]["source"] == "FromType" for r in outcomes[0].regions)


def test_a_listed_census_that_misses_a_case_leaves_it_empty(outcomes):
    listed = _regions(outcomes[1])
    assert listed["zero"] == 1 and listed["rank deficient"] == 2
    assert listed["0 x 0"] == 0 and listed["1 x 1"] == 0


def test_an_authors_label_is_recorded_with_its_share_and_never_as_a_region(outcomes):
    labels = outcomes[0].labels
    assert [l["label"] for l in labels] == ["negative corner"] and labels[0]["n"] > 0
    assert labels[0]["share"] == labels[0]["n"] / outcomes[0].evaluated
    assert "negative corner" not in _regions(outcomes[0])
    entry = tester.settle({}, outcomes[0])
    assert entry["labels"] == labels and entry["regions"] == outcomes[0].regions


def test_a_cutoff_gives_its_two_sides_and_a_premise_its_boundary(outcomes):
    assert set(_regions(outcomes[2])) == {"tol above", "tol below"}
    assert _regions(outcomes[3]) == {"k boundary": _regions(outcomes[3])["k boundary"]}
    assert _regions(outcomes[3])["k boundary"] > 0  # 0 and 1, the bound and its neighbour, drawn


def test_a_census_value_outside_its_type_makes_the_law_not_run(outcomes):
    bad = outcomes[4]
    assert bad.verdict == "NotRun" and "outside" in bad.evidence.reason and "7.S1" in bad.evidence.reason


# ---------------------------------------------------------------------- the grade (items 6, 7)

def _entry(binding, grade="Cases", regions=None, seed=0, kind=None):
    e = {"law": "L", "cone": "sha256:1", "binding": [{"parameter": "a", "generator": binding, "fingerprint": ""}],
         "seed": seed, "cases": 10, "budgets": {}, "reach": [{"parameter": "a", "reach": "Support"}],
         "evidence": {"Points": {"evaluated": 10, "raised": 0, "coverage": "Listed", "verdict": "Supported"}},
         "grade": grade, "outcome": "Passed", "date": f"2026-10-17T00:00:0{seed}+00:00"}
    if regions is not None:
        e["regions"] = [{"region": {"source": s, "name": n}, "n": k} for s, n, k in regions]
    if kind:
        e["kind"] = kind
    return e


def test_no_regions_leave_the_grade_and_an_empty_region_caps_it_at_sampled():
    assert certify.certificate_grade([_entry("x")], "L", "sha256:1") == "Cases"
    full = _entry("x", regions=[("FromType", "zero", 2), ("FromLaw", "tol above", 1)])
    assert certify.certificate_grade([full], "L", "sha256:1") == "Cases"
    empty = _entry("x", regions=[("FromType", "zero", 2), ("FromLaw", "tol above", 0)])
    assert certify.certificate_grade([empty], "L", "sha256:1") == "Sampled"
    assert certify.standing([empty], "L", "sha256:1") == "sampled (no case in tol above)"
    # the demand's other combination keeps the strongest
    assert certify.certificate_grade([empty], "L", "sha256:1", "strongest") == "Cases"


def test_a_label_enters_no_grade():
    labelled = _entry("x", regions=[("Label", "kappa above 1e8", 0), ("FromType", "zero", 1)])
    assert certify.certificate_grade([labelled], "L", "sha256:1") == "Cases"


def test_the_regions_combine_across_bindings_and_a_binding_without_the_case_caps():
    one = _entry("x", regions=[("FromType", "zero", 3)])
    other = _entry("y", regions=[("FromType", "zero", 0)], seed=1)
    assert certify.certificate_grade([one], "L", "sha256:1") == "Cases"
    assert certify.certificate_grade([other, one], "L", "sha256:1") == "Sampled"
    assert certify.certificate_grade([other, one], "L", "sha256:1", "strongest") == "Cases"


def test_an_agreeing_replay_is_written_when_it_adds_the_regions():
    old = _entry("x")
    new = dict(_entry("x", regions=[("FromType", "zero", 1)]), date="2026-10-17T01:00:00+00:00")
    assert certify.record([old], new)[0] is new
    again = dict(new, date="2026-10-17T02:00:00+00:00")
    assert certify.record([new, old], again) == [new, old]


def test_a_run_is_served_at_the_grade_read_over_the_regions_with_its_combination():
    empty = _entry("x", regions=[("FromType", "zero", 0)])
    demand = {"law": "L", "cone": "sha256:1", "given": [], "accepts": "Cases"}
    assert certify.serves(demand, empty)  # without the store, the entry's own grade
    assert not certify.serves_over(demand, empty, [empty])
    assert certify.serves_over(dict(demand, combine="strongest"), empty, [empty])
    assert certify.serves_over(dict(demand, accepts="Sampled"), empty, [empty])
    assert demand_of().combine == "weakest" and demand_of(combine="strongest").law("L", "c", [], {})["combine"] == "strongest"
    with pytest.raises(RunError):
        demand_of(combine="vector")
