"""Rules of the checker as phase 3 of docs/plan-2026-10-05.md fixed them: Bool is told by its labels,
not by position (04); `==` exists only where equality is structural, which excludes Real and a data
type with a function inside (05 R8); a law whose labels cannot be read is an error, not a pass
(05 R3). Self-contained: core.lut only."""
import sys

import pytest

from luthier.parser import parse
from luthier.checker import Checker, TypeCheckError
from luthier.evaluator import Env
from luthier.cli import CORE, Loader

sys.setrecursionlimit(50_000)


def load(src: str) -> Checker:
    ck = Checker(Env())
    Loader(ck).load_file(CORE)
    ck.load(parse(src))
    return ck


def test_a_sum_of_two_units_is_not_a_bool():
    src = "Verdict = < wrong : Unit | right : Unit >\n" \
          "AlwaysWrong (x : Int) : Verdict := wrong\n" \
          "three : { x : Int | AlwaysWrong x } := 3\n"
    with pytest.raises(TypeCheckError, match="Bool-valued or a law"):
        load(src)


def test_a_verdict_cannot_be_the_condition_of_an_if():
    src = "Verdict = < wrong : Unit | right : Unit >\n" \
          "v : Verdict := wrong\n" \
          "x : Int := if v then 1 else 2\n"
    with pytest.raises(TypeCheckError):
        load(src)


def test_bool_itself_still_works():
    ck = load("b : Bool := 1 < 2\nx : Int := if b then 1 else 2\n")
    assert ck.resolve("x")


def test_the_reals_have_no_structural_equality():
    with pytest.raises(TypeCheckError, match="no computable equality"):
        load("x : Real\ny : Real\nsame : Bool := x == y\n")


def test_a_recursive_data_type_holding_a_function_has_no_structural_equality():
    src = "FTree : U := data { fleaf : (Int -> Int) -> FTree ; fnode : FTree -> FTree -> FTree }\n" \
          "f (x : Int) : Int := x\n" \
          "same : Bool := fleaf f == fleaf f\n"
    with pytest.raises(TypeCheckError, match="no structural equality on FTree"):
        load(src)


def test_a_recursive_data_type_of_numbers_has_it():
    ck = load("Tree : U := data { leaf : Int -> Tree ; node : Tree -> Tree -> Tree }\n"
              "same : Bool := leaf 1 == node (leaf 1) (leaf 2)\n")
    assert ck.resolve("same")


def test_a_law_whose_labels_cannot_be_read_is_an_error():
    src = "P2 : { a : Int, b : Int }\n" \
          "Both (p : Int -> Bool) (r : P2) : Bool := p r.a and p r.b\n" \
          "pos (x : Int) : Bool := x > 0\n" \
          "PosBoth : P2 -> Bool := Both pos\n" \
          "P2 := PosBoth\n"
    with pytest.raises(TypeCheckError, match="cannot tell which labels"):
        load(src)


def test_a_law_written_over_the_whole_value_is_read():
    ck = load("P2 : { a : Int, b : Int }\n"
              "Both (p : Int -> Bool) (r : P2) : Bool := p r.a and p r.b\n"
              "pos (x : Int) : Bool := x > 0\n"
              "P2 := Both pos\n")
    assert ck.resolve("P2")
