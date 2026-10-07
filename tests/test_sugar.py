"""The syntax phase 6 of record/plan-2026-10-05.md added (06 §6.1): `let p = e in body`, the unary minus,
and implicit parameters `{A : U}` inferred where a definition is applied. Self-contained: core.lut
and real.lut only."""
import sys

import pytest

from luthier.parser import parse, parse_term
from luthier.checker import Checker, TypeCheckError
from luthier.evaluator import Env, evaluate
from luthier.pretty import pp
from luthier.cli import CORE, LIB_DIR, Loader

import os

sys.setrecursionlimit(50_000)


def load(src: str) -> Checker:
    ck = Checker(Env())
    loader = Loader(ck)
    loader.load_file(CORE)
    loader.load_file(os.path.join(LIB_DIR, "real.lut"))
    ck.load(parse(src))
    return ck


def ev(ck: Checker, src: str) -> str:
    with ck.silent():
        t, _ = ck.infer([], parse_term(src))
    return pp(evaluate(ck.env, t))


def test_let_binds_a_name_and_a_pattern():
    ck = load("a : Int := let x = 3 in x * x - 1\n"
              "b : Float64 := let (p, q) = (2.0, 3.0) in p * q\n"
              "c : Int := let x = 2 in let y = x + 1 in x * y\n")
    assert ev(ck, "a") == "8" and ev(ck, "b") == "6.0" and ev(ck, "c") == "6"


def test_a_let_inside_a_branch_carries_the_branch_condition():
    # the obligation of `v.f k` holds only where k < v.n, which the if states
    ck = load("V = { n : Nat, f : Fin n -> Int }\n"
              "at (v : V) (k : Int) : Int := if 0 <= k and k < v.n then let y = v.f k in y + 1 else 0\n")
    assert ck.resolve("at")


def test_unary_minus_on_int_and_float():
    ck = load("a : Int := -3 + 5\nb : Float64 := -(1.5 * 2.0)\nc : Int := 2 * -3\nd : Float64 := let x = 4.0 in -x\n")
    assert ev(ck, "a") == "2" and ev(ck, "b") == "-3.0" and ev(ck, "c") == "-6" and ev(ck, "d") == "-4.0"


def test_unary_minus_on_another_type_is_an_error():
    with pytest.raises(TypeCheckError, match="unary minus"):
        load('x : String := -"a"\n')


IMPLICIT = """
first {A B : U} (p : A * B) : A := match p { (a, b) -> a }
twice {A : U} (f : A -> A) (x : A) : A := f (f x)
len {A : U} (l : List A) : Int := match l { nil -> 0 ; cons x xs -> 1 + len xs }
inc (n : Int) : Int := n + 1
"""


def test_implicit_parameters_are_inferred_from_the_arguments():
    ck = load(IMPLICIT + 'a : Int := first (3, "x")\n'
                         "b : Int := twice inc 5\n"
                         "c : Int := twice (\\ n { n * 2 }) 3\n"
                         "d : Int := len (cons Int 1 (cons Int 2 (nil Int)))\n")
    assert [ev(ck, x) for x in "abcd"] == ["3", "7", "12", "2"]


def test_implicit_parameters_can_still_be_given_explicitly():
    ck = load(IMPLICIT + 'e : Int := first Int String (4, "y")\n')
    assert ev(ck, "e") == "4"


def test_an_implicit_parameter_that_cannot_be_inferred_is_an_error():
    with pytest.raises(TypeCheckError, match="cannot infer the implicit"):
        load("mk {A : U} (n : Int) : List A := nil A\nz : Int := match mk 3 { nil -> 0 ; cons x xs -> 1 }\n")


def test_an_implicit_parameter_must_be_a_type():
    with pytest.raises(TypeCheckError, match="must be a type"):
        load("g {n : Int} (x : Int) : Int := x + n\n")
