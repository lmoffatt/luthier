"""The bridge with Python (06 §6) and the generators, as phase 1 of docs/plan-2026-10-05.md fixed
them: a value of the environment is checked against its declared type at the crossing; every
refinement in the type of an extern is an obligation on it; a registered generator's values are
checked against their type; the table of a function to Int is an int64 array; a generator given
to an alias is the generator of the type the alias stands for. Self-contained: core.lut only."""
import random
import sys

import numpy as np
import pytest

from luthier.parser import parse, parse_term
from luthier.checker import Checker, TypeCheckError
from luthier.evaluator import Env, EvalError, evaluate
from luthier.generators import Generators, GenError
from luthier.testing import run_test
from luthier.pretty import pp
from luthier.cli import CORE, Loader, typed_setting

sys.setrecursionlimit(50_000)

ARRAYS = """
V = { n : Nat, f : Fin n -> Float64 }
VI = { n : Nat, f : Fin n -> Int }
NonNeg : U := { x : Float64 | x >= 0.0 }
"""


def load(src: str) -> Checker:
    ck = Checker(Env())
    Loader(ck).load_file(CORE)
    ck.load(parse(ARRAYS + src))
    return ck


def ev(ck: Checker, src: str) -> str:
    with ck.silent():
        t, _ = ck.infer([], parse_term(src))
    return pp(evaluate(ck.env, t))


def run_laws(ck: Checker, name: str, n: int = 20):
    gens = Generators.from_checker(ck)
    return run_test(ck, gens, ck.resolve(name), n=n, seed=7, deep=True)


# ------------------------------------------------------------------ 1.1 values checked at the crossing

def test_a_string_is_not_a_float():
    ck = load('h : String -> Float64 := extern "python:bridge_externs.hello"')
    with pytest.raises(EvalError, match="not a value of Float64"):
        ev(ck, 'h "x"')


def test_an_int_is_promoted_to_a_float_so_division_is_real():
    ck = load('f : Int -> Float64 := extern "python:bridge_externs.as_int"')
    assert ev(ck, "f 3 / f 2") == "1.5"


@pytest.mark.parametrize("fn", ["three_float", "true_value"])
def test_a_float_or_a_bool_is_not_an_int(fn):
    ck = load(f'x : Int := extern "python:bridge_externs.{fn}"')
    with pytest.raises(EvalError, match="not a value of Int"):
        ev(ck, "x + 1")


def test_a_numpy_integer_is_an_int():
    ck = load('x : Int := extern "python:bridge_externs.numpy_int"')
    assert ev(ck, "x + 1") == "8"


def test_an_integer_array_is_a_vector_of_floats():
    ck = load('v : V := extern "python:bridge_externs.int_array"')
    assert ev(ck, "v.f 1 / 2.0") == "1.0"


def test_a_float_array_is_not_a_vector_of_ints():
    ck = load('v : VI := extern "python:bridge_externs.float_array"')
    with pytest.raises(EvalError, match="its entries are Int"):
        ev(ck, "v.n")


def test_a_matrix_is_not_a_vector():
    ck = load('v : V := extern "python:bridge_externs.matrix"')
    with pytest.raises(EvalError, match="1 dimension"):
        ev(ck, "v.n")


def test_nan_in_a_list_is_an_error():
    ck = load('v : V := extern "python:bridge_externs.nan_list"')
    with pytest.raises(EvalError, match="NaN"):
        ev(ck, "v.n")


def test_a_number_is_not_a_vector():
    ck = load('v : V := extern "python:bridge_externs.scalar"')
    with pytest.raises(EvalError, match="not a value of"):
        ev(ck, "v.n")


def test_unit_crosses_as_none_only():
    ck = load('u : Unit := extern "python:bridge_externs.not_none"')
    with pytest.raises(EvalError, match="Unit crosses as None"):
        ev(ck, "u")


def test_a_setting_is_read_by_the_type_of_its_hole():
    ck = load("dir : String\nsigma : Float64\nk : Int\nflag : Bool")
    env = ck.env
    ty = lambda n: env.defs[ck.resolve(n)].type
    assert typed_setting(env, "dir", "2026", ty("dir")) == "2026"
    assert typed_setting(env, "sigma", "3", ty("sigma")) == 3.0
    assert isinstance(typed_setting(env, "sigma", "3", ty("sigma")), float)
    assert typed_setting(env, "k", "3", ty("k")) == 3
    assert typed_setting(env, "flag", "true", ty("flag")) is True
    for name, raw in [("k", "3.5"), ("sigma", "nan"), ("sigma", "abc"), ("flag", "yes")]:
        with pytest.raises(SystemExit):
            typed_setting(env, name, raw, ty(name))


# ------------------------------------------------------------------ 1.2 refinements of an extern's type

def test_the_codomain_of_an_extern_is_an_obligation():
    ck = load('neg : Float64 -> NonNeg := extern "python:bridge_externs.negative"')
    assert ck.obligations.get(ck.resolve("neg"))
    r = run_laws(ck, "neg")
    assert not r.passed


def test_the_entries_of_an_array_from_the_environment_are_an_obligation():
    src = 'Idx = { n : Nat, f : Fin n -> Fin 3 }\nbad : Idx := extern "python:bridge_externs.indices_out_of_range"\n' \
          'good : Idx := extern "python:bridge_externs.indices_in_range"'
    ck = load(src)
    assert not run_laws(ck, "bad").passed
    assert run_laws(ck, "good").passed


def test_an_extern_with_no_refinement_owes_nothing():
    ck = load('vf : Float64 -> V := extern "python:bridge_externs.pair_of_vector"')
    assert not ck.obligations.get(ck.resolve("vf"))


# ------------------------------------------------------------------ 1.3 registered generators

def test_a_generator_outside_its_type_is_an_error():
    src = 'gen NonNeg := extern "python:bridge_externs.gen_positive_wrongly"\n' \
          'Small (x : NonNeg) : Bool := x >= 0.0\n' \
          's : { p : Unit | \\ (x : NonNeg) { Small x } } := unit'
    ck = load(src)
    r = run_laws(ck, "s")
    assert not r.passed
    assert "gave a value outside" in (r.laws[0].error or "")


# ------------------------------------------------------------------ 1.4 integer tables

def test_the_table_of_a_function_to_int_is_an_int64_array():
    ck = load("")
    gens = Generators.from_checker(ck)
    with ck.silent():
        ty, _ = ck.infer([], parse_term("Fin 4 -> Int"))
    v = gens.sample(ty, random.Random(1), 8)
    assert v.value.dtype == np.int64


# ------------------------------------------------------------------ 1.5 generators of aliases

def test_two_aliases_of_one_type_cannot_both_have_a_generator():
    src = 'A = { x : Float64, y : Float64 }\nB = { x : Float64, y : Float64 }\n' \
          'gen A := extern "python:bridge_externs.gen_unit_point"\n' \
          'gen B := extern "python:bridge_externs.gen_unit_point"'
    with pytest.raises(TypeCheckError, match="same type"):
        load(src)


def test_the_generator_of_an_alias_is_the_generator_of_its_type():
    # the law holds only on the unit circle; it is written over the type, not over the alias
    src = 'Point = { x : Float64, y : Float64 }\n' \
          'gen Point := extern "python:bridge_externs.gen_unit_point"\n' \
          'OnCircle (p : { x : Float64, y : Float64 }) : Bool := p.x * p.x + p.y * p.y <= 1.0000001\n' \
          'c : { u : Unit | \\ (p : { x : Float64, y : Float64 }) { OnCircle p } } := unit'
    ck = load(src)
    assert run_laws(ck, "c", n=50).passed


# ------------------------------------------------------------------ phase 4 of the plan

def test_a_refinement_under_a_constructor_is_an_obligation():
    src = 'Idx = Fin 3\nMI = < nothing : Unit | just : Fin 3 >\n' \
          'pick : Int -> MI := extern "python:bridge_externs.maybe_index"\n'
    ck = load(src)
    labels = [o.label for o in ck.obligations.get(ck.resolve("pick"), [])]
    assert labels and all("just" in l for l in labels)
    assert not run_laws(ck, "pick", n=40).passed      # pick 5 is just 5, outside Fin 3


def test_run_checked_tests_what_an_extern_gives(tmp_path):
    from luthier.cli import main
    lut = tmp_path / "checked.lut"
    lut.write_text('import "real"\nimport "real_python"\nimport "table"\nimport "table_python"\n'
                   'mkTable : Int -> Table := extern "python:bridge_externs.bad_table_of"\n'
                   'main : Int := (mkTable 3).nRows\n')
    assert main(["run", str(lut), "--no-record"]) == 0
    with pytest.raises(SystemExit, match="outside Table"):
        main(["run", str(lut), "--checked", "--no-record"])


def test_a_law_blocked_by_a_hole_is_reported_with_its_name():
    ck = load("k : Int\nAbove (x : Int) : Bool := x + k > x\n"
              "a : { u : Unit | \\ (x : Int) { Above x } } := unit\n")
    r = run_laws(ck, "a")
    assert r.laws[0].outcome == "not run" and "k" in r.laws[0].error


# ------------------------------------------------------------------ the rationals (06 §8)

def test_rationals_are_exact_and_cross_as_fractions():
    ck = load('third : Rational := extern "python:bridge_externs.third"\n'
              'one : Bool := third + third + third == third * (third + third + third) / third\n'
              'notHalf : Rational := extern "python:bridge_externs.a_float"\n')
    assert ev(ck, "third * third") == "1/9"
    assert ev(ck, "one") == "true"
    with pytest.raises(EvalError, match="Fraction"):
        ev(ck, "notHalf")


def test_mod_is_not_defined_on_rationals():
    with pytest.raises(TypeCheckError, match="mod"):
        load('q : Rational := extern "python:bridge_externs.third"\nr : Rational := q mod q\n')
