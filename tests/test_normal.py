"""normal.py: a law recognized as a core property by its normal form (record/plan/
law-normal-form-2026-10-27/prompt.md; Luciano's idea, record/notes/idea-law-normal-form-2026-10-27.md)."""
from pathlib import Path

import pytest

from luthier import normal

REPO = Path(__file__).resolve().parent.parent
TAPE = REPO / "docs" / "concepts" / "tape.lth"

# the tape's laws written other ways, and laws that are no core property
VARIANTS = """
Mark : U := { k : Int | 0 <= k and k <= 50000 }
Tape : { reading : Mark -> Mark -> Float64 }
ReadingSymmetric (t : Tape) (a b : Mark) : Bool := t.reading a b == t.reading b a
Swapped (t : Tape) (a b : Mark) : Bool := t.reading b a == t.reading a b
Renamed (s : Tape) (q p : Mark) : Bool := s.reading p q == s.reading q p
FloatAssociative (a b c : Float64) : Bool := (a + b) + c == a + (b + c)
IntAssociative (a b c : Int) : Bool := (a + b) + c == a + (b + c)
ReadingSteps (t : Tape) (a : Mark) : Bool := t.reading a (a + 1) == 1.0
MinusCommutes (a b : Int) : Bool := a - b == b - a
"""


@pytest.fixture(scope="module")
def variants(tmp_path_factory):
    path = tmp_path_factory.mktemp("normal") / "variants.lth"
    path.write_text(VARIANTS, encoding="utf-8")
    env, own = normal.env_of(path)
    return {law.name: law for law in normal.laws_of(env, own)}


@pytest.fixture(scope="module")
def tape():
    env, own = normal.env_of(TAPE)
    return {law.name: law for law in normal.laws_of(env, own)}


def test_the_tapes_symmetry_is_commutative(tape):
    found = normal.recognize(tape["ReadingSymmetric"])
    assert [i.notice() for i in found] == [
        "ReadingSymmetric is Commutative at A = Mark, B = Float64, o = structural Float64, op = t.reading, x = a, y = b"]


@pytest.mark.parametrize("name", ["Swapped", "Renamed"])
def test_sides_swapped_or_variables_renamed_are_the_same_law(variants, tape, name):
    assert normal.normal_form(variants[name]) == normal.normal_form(tape["ReadingSymmetric"])
    [found] = normal.recognize(variants[name])
    assert found.property == "Commutative"
    assert dict(found.at)["op"] in ("t.reading", "s.reading")


def test_a_float_associativity_is_not_associative(variants):
    law = variants["FloatAssociative"]
    # its sums are sorted, never flattened: the two sides stay distinct
    assert not normal.trivial(law)
    assert all(i.property != "Associative" for i in normal.recognize(law))


def test_an_integer_associativity_is_true_by_the_quotient(variants):
    law = variants["IntAssociative"]
    assert normal.trivial(law)
    assert normal.recognize(law) == []


def test_a_law_that_is_no_core_property_is_nothing(variants, tape):
    assert normal.recognize(variants["ReadingSteps"]) == []
    assert normal.recognize(tape["ReadingAdds"]) == []


def test_a_global_operation_is_matched_as_written(variants):
    # `-` is claimed nothing: the law states its commutativity, which it lacks, and is recognized
    [found] = normal.recognize(variants["MinusCommutes"])
    assert (found.property, dict(found.at)["op"], dict(found.at)["A"]) == ("Commutative", "-", "Int")


def test_the_dictionary_holds_the_brief_properties():
    names = {e.name for e in normal.dictionary()}
    assert {"Commutative", "Associative", "Neutral", "Symmetric", "Transitive", "Injective", "Involutive",
            "Triangular", "AssociativeWithin"} <= names
    variants = [e for e in normal.dictionary() if e.name == "Commutative"]
    assert sorted(e.structural for e in variants) == [(), ("o",)]


def test_every_core_property_is_itself():
    programs, _ = normal.core_env()
    entries = {e.name for e in normal.dictionary()}
    missed, seen = [], 0
    for rel, q, own in programs:
        env = normal.Env(q, normal.core_definitions())
        for law in normal.laws_of(env, own):
            if law.name in entries:
                seen += 1
                if law.name not in {i.property for i in normal.recognize(law)}:
                    missed.append(f"{rel}:{law.name}")
    assert seen > 50 and missed == []


def test_the_canonical_labels_reach_a_fixed_point(tape):
    law = tape["ReadingSymmetric"]
    form = normal.normal_form(law)
    assert sorted(form.labels.values()) == [0, 1, 2]
    assert normal.show(normal.to_kernel(form.form)) == "(v0.reading v1 v2) == (v0.reading v2 v1)"
