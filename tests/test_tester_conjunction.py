"""The core's bite 4b (record/plan/core-2026-10-17/prompt-bite-4b.md; D-2026-10-18-f): the tester
splits a law whose body is a conjunction of partially applied laws into its conjuncts, and the region
classifier's two bounds are budgets of the line (7.S8, P11)."""
import json
import random
from dataclasses import replace

import pytest

from luthier import certify, term as t, tester



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


# ---------------------------------------------------------------------- a conjunction of laws (D-2026-10-18-f)

# bite 2's `Equivalence` written bare (report-bite-2.md, its question): a `&` of partially applied
# laws whose missing variables differ (`x : A`, `p : Related A r`, `c : Chain A r`), and `Mixed`,
# whose two conjuncts are graded differently under one line (exhaustive over Bool, cases on a census)
BARE = '''import "core/properties/relations.lth" Related Chain Reflexive Symmetric Transitive
import "core/properties/operations.lth" Commutative
import "core/structures/equality.lth" Object
BareEquivalence (A : U) (r : A -> A -> Bool) := Reflexive A r & Symmetric A r & Transitive A r
LocalIntEquivalence (r : Int -> Int -> Bool) := BareEquivalence Int r
boolEq : Object Bool := { eq := fn x y { x == y } }
Mixed (r : Int -> Int -> Bool) := Commutative Bool Bool boolEq (fn a b { a and b }) & Reflexive Int r
parity : Int -> Int -> Bool := fn a b { (a - b) mod 2 == 0 }
leq : Int -> Int -> Bool := fn a b { a <= b }
smallInts : List Int := [0, 1, 2]
'''
LINES = '''import "test.lth" test ExhaustiveMode SampledMode
import "generators_model.lut" linear
import "generators.lth" Binding
import "laws.lth" Listed
import "bare.lut" LocalIntEquivalence Mixed parity leq smallInts
onParity : List Binding := [ { parameter := just "r", type := nothing, generator := "parity", coverage := Listed } ]
onLeq : List Binding := [ { parameter := just "r", type := nothing, generator := "leq", coverage := Listed } ]
onSmall : List Binding := [ { parameter := just "r", type := nothing, generator := "leq", coverage := Listed },
  { parameter := nothing, type := just "Int", generator := "smallInts", coverage := Listed } ]
test "LocalIntEquivalence" (SampledMode linear) (profile <- onParity)
test "LocalIntEquivalence" (SampledMode linear) (profile <- onLeq)
test "LocalIntEquivalence" (SampledMode linear) (profile <- onLeq) (control <- true)
test "Mixed" ExhaustiveMode (profile <- onSmall)
'''


@pytest.fixture
def bare(tmp_path):
    (tmp_path / "bare.lut").write_text(BARE, encoding="utf-8")
    path = tmp_path / "bare_laws.test.lut"
    path.write_text(LINES, encoding="utf-8")
    return path


def test_a_conjunction_is_split_into_its_conjuncts_each_quantified_on_its_own(bare):
    holds, refuted, control, mixed = tester.run_tests(bare)
    assert [o.conjunct for o in holds.parts] == ["Reflexive Int r", "Symmetric Int r", "Transitive Int r"]
    assert [o.parameters for o in holds.parts] == [("r", "x"), ("r", "p"), ("r", "c")]
    assert all(o.verdict == "Supported" and o.grade == "Sampled" and o.evaluated == 100 for o in holds.parts)
    assert (holds.verdict, holds.grade, holds.evaluated) == ("Supported", "Sampled", 300) and tester.passes(holds)
    # each conjunct has its entry: the conjunction's law and cone, the conjunct named, apart in identity
    entries = [o.entry for o in holds.parts]
    assert {e["law"] for e in entries} == {"LocalIntEquivalence"} and len({e["cone"] for e in entries}) == 1
    assert entries[0]["cone"] == holds.cone
    assert [e["conjunct"] for e in entries] == [o.conjunct for o in holds.parts]
    assert all(e["conjuncts"] == [o.conjunct for o in holds.parts] for e in entries)
    assert len({certify.identity(e) for e in entries}) == 3
    assert [d["parameter"] for d in entries[1]["binding"]] == ["r", "p"]
    # the conjunction's grade is the demand's combination of its conjuncts' (5.S8), the weakest by
    # default: one line's bindings weaken every conjunct alike (cases here, the census `Listed`), so
    # the conjuncts are given two grades by hand
    assert [o.grade for o in mixed.parts] == ["Cases", "Cases"] and mixed.grade == "Cases"
    exhaustive = replace(mixed.parts[0], verdict="Confirmed", grade="ExhaustiveGrade")
    combined = tester._conjunction_outcome(mixed.spec, [exhaustive, mixed.parts[1]], mixed.cone, None)
    assert (combined.verdict, combined.grade, combined.conjunct) == ("Supported", "Cases", "Reflexive Int r")
    graded = [dict(mixed.parts[0].entry, grade="ExhaustiveGrade"), mixed.parts[1].entry]
    assert certify.certificate_grade(graded, "Mixed", mixed.cone) == "Cases"
    assert certify.certificate_grade(graded, "Mixed", mixed.cone, "strongest") == "ExhaustiveGrade"
    lines = tester.line(holds).splitlines()
    assert lines[0] == "LocalIntEquivalence: conjunction of 3, 300 cases, sampled (3 of 3 ran)"
    assert lines[2].startswith("  conjunct Symmetric Int r: sampled (seed 0, size 10")


def test_a_conjunction_is_refuted_when_a_conjunct_is_and_its_control_refutes_it(bare):
    _, refuted, control, _ = tester.run_tests(bare)
    assert [o.verdict for o in refuted.parts] == ["Supported", "Refuted", "Supported"]
    assert refuted.verdict == "Refuted" and refuted.grade is None and not tester.passes(refuted)
    assert tester.line(refuted).splitlines()[0].startswith(
        "LocalIntEquivalence: conjunction of 3, 300 cases, refuted at Symmetric Int r: r = leq, p = ")
    # a control refutes the conjunction when it refutes one conjunct: one entry, the conjunct named
    assert control.spec.control and control.verdict == "Refuted" and tester.passes(control)
    assert control.entry["kind"] == "Control" and "conjunct" not in control.entry
    assert control.entry["outcome"]["ControlRefuted"].startswith("Symmetric Int r: r = leq, p = ")
    assert [d["parameter"] for d in control.entry["binding"]] == ["r", "x", "p", "c"]
    result = certify.certify_file(str(bare), store=False)
    standing = dict((law, s) for law, _, s in result["laws"])
    assert standing["LocalIntEquivalence"].startswith("refuted at Symmetric Int r: r = leq")
    assert standing["Mixed"] == "cases"
    cone = dict((law, c) for law, c, _ in result["laws"])["LocalIntEquivalence"]
    assert certify.control_status(result["control entries"], "LocalIntEquivalence", cone).startswith("controlled")


def test_the_conjuncts_entries_are_stored_and_known_and_grade_the_conjunction(bare):
    first = tester.run_tests(bare, store=True)
    store = bare.parent / "bare.cert.json"
    entries = json.loads(store.read_text(encoding="utf-8"))
    assert sum(1 for e in entries if e.get("conjunct")) == 3 + 3 + 2
    again = tester.run_tests(bare, store=True)
    assert all(o.known is not None for o in again[0].parts) and again[0].known is not None
    assert tester.line(again[0]).splitlines()[0].endswith("sampled (known)")
    good = [e for e in entries if e.get("binding", [{}])[0].get("generator", "").startswith("parity")]
    assert certify.certificate_grade(good, "LocalIntEquivalence", first[0].cone) == "Sampled"
    # a conjunct missing from the entries leaves the conjunction without a grade
    assert certify.certificate_grade(good[1:], "LocalIntEquivalence", first[0].cone) is None
    assert certify.certificate_grade(good[:1], "LocalIntEquivalence", first[0].cone) is None


# ---------------------------------------------------------------------- an axiom conjunct (prompt-b1-b3-d1.md, item 4)

AXIOM_CONJUNCT = '''import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
Pick : { f : Bool -> Bool }
Twice (p : Pick) (b : Bool) : Bool := p.f (p.f b) == b
Faithful (p : Pick) : Bool := axiom "the pick is faithful to the world"
Pick (p : Pick) := Twice p & Faithful p
notPick : Pick := { f := fn b { not b } }
broken : Pick := { f := fn b { true } }
models : List Binding := [ { parameter := nothing, type := just "Pick", generator := "notPick", coverage := Listed } ]
brokens : List Binding := [ { parameter := nothing, type := just "Pick", generator := "broken", coverage := Listed } ]
test "Pick" ExhaustiveMode (profile <- models)
test "Pick" ExhaustiveMode (profile <- brokens) (control <- true)
'''


def test_an_axiom_conjunct_is_graded_assumed_with_no_case(tmp_path):
    """report-B2.md's question, answered yes: as run.py's `axioms` accepts a law whose body is an axiom,
    the tester grades an axiom conjunct assumed with no case run, so the conjunction is a line graded
    assumed (the weakest of its conjuncts), not one left unsettled; a control does not run it."""
    path = tmp_path / "pick.test.lut"
    path.write_text(AXIOM_CONJUNCT, encoding="utf-8")
    law, control = tester.run_tests(path, store=False)
    assert law.grade == "AssumedGrade", tester.line(law)
    axiom = next(o for o in law.parts if o.conjunct.startswith("Faithful"))
    assert axiom.evaluated == 0 and axiom.entry["evidence"] == {"Assumed": "the pick is faithful to the world"}
    assert axiom.entry["grade"] == "AssumedGrade" and certify.store_errors([axiom.entry]) == []
    assert "assumed, an axiom" in tester.line(law)
    assert control.verdict == "Refuted"
