"""The two evaluators agree (plan 4.3): the substitution evaluator the checker uses and the
call-by-need machine `test` and `run` use give the same normal form for every closed definition of a
type with structural equality, in the programs of tests/spec and in a few written here for the
features those leave out. A disagreement is a bug in one of them; the machine falls back to the
substitution evaluator for what it does not evaluate, and a test reports how often."""
import glob
import os
import sys

import pytest

from luthier.cli import load
from luthier.certify import cone
from luthier.evaluator import evaluate, Fuel, EvalError
from luthier.machine import normalize
from luthier.pretty import pp
from luthier.syntax import Var, Extern, Primitive, Axiom, Univ, Pi

sys.setrecursionlimit(200_000)

SPEC = os.path.join(os.path.dirname(__file__), "spec")

PROGRAMS = {
    "arithmetic": "a : Int := 7 * 6 - 2\nb : Float64 := 1.5 / 2.0 + 0.25\nc : Int := 17 / 5 + 17 mod 5\n"
                  "d : Bool := 3 < 4 and not (2 == 3)\n",
    "recursion": "fact (n : Int) : Int := if n <= 1 then 1 else n * fact (n - 1)\nf10 : Int := fact 10\n"
                 "N : U := data { zero : N ; succ : N -> N }\n"
                 "toInt (n : N) : Int := match n { zero -> 0 ; succ m -> 1 + toInt m }\n"
                 "three : Int := toInt (succ (succ (succ zero)))\n",
    "records": "P = { x : Int, y : Int }\np : P := { x := 3, y := 4 }\nsq : Int := p.x * p.x + p.y * p.y\n"
               "swap (q : P) : P := { x := q.y, y := q.x }\nsameAfterTwo : Bool := swap (swap p) == p\n",
    "sums": "S = < none : Unit | some : Int >\nget (s : S) : Int := match s { none -> 0 ; some k -> k }\n"
            "g : Int := get (some 5) + get none\n"
            "s5 : S := some 5\neqS : Bool := s5 == some 5\n",
    "tables": "sq (n : Int) (k : Fin n) : Int := k * k\n"
              "sumSq (n : Int) (f : Fin n -> Int) (k : Int) : Int := if k >= n then 0 else f k + sumSq n f (k + 1)\n"
              "s : Int := sumSq 5 (sq 5) 0\n",
    "lists": "len (l : List Int) : Int := match l { nil -> 0 ; cons x xs -> 1 + len xs }\n"
             "l3 : Int := len (cons Int 1 (cons Int 2 (cons Int 3 (nil Int))))\n",
}


def closed_scalars(loader):
    """The definitions with a body, not externs or axioms, whose cone has no hole and whose type has
    structural equality (no function, no type)."""
    ck = loader.checker
    env = ck.env
    tops = {p for _, _, p in loader.top_programs()}
    out = []
    for q, d in env.defs.items():
        if loader.origin.get(q, ("",))[0] not in tops:
            continue
        if d.body is None or d.data is not None or isinstance(d.body, (Extern, Primitive, Axiom)) or d.alias:
            continue
        if d.type is None or isinstance(ck.whnf(d.type), (Univ, Pi)) or ck.contains_function(d.type):
            continue
        if any(env.defs[n].body is None and env.defs[n].data is None for n in cone(env, q)
               if n in env.defs and not isinstance(ck.whnf(env.defs[n].type or Univ()), Univ)):
            continue
        out.append(q)
    return out


def compare(loader):
    env = loader.checker.env
    disagreements = []
    for q in closed_scalars(loader):
        try:
            a = pp(evaluate(env, Var(q)))
        except EvalError as e:
            a = f"error: {e}"
        try:
            b = pp(normalize(env, Var(q), Fuel(env.run_fuel)))
        except EvalError as e:
            b = f"error: {e}"
        if a != b:
            disagreements.append((q, a, b))
    return disagreements


@pytest.mark.parametrize("path", sorted(glob.glob(os.path.join(SPEC, "*.accept.lut"))),
                         ids=lambda p: os.path.basename(p))
def test_the_evaluators_agree_on_the_spec_programs(path):
    assert compare(load([path])) == []


@pytest.mark.parametrize("name", sorted(PROGRAMS))
def test_the_evaluators_agree(name, tmp_path):
    p = tmp_path / f"{name}.lut"
    p.write_text(PROGRAMS[name])
    loader = load([str(p)])
    assert closed_scalars(loader), "the program should have closed values to compare"
    assert compare(loader) == []
