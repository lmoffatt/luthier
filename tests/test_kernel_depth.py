"""Deep demands use no Python stack in proportion to their depth (kernel 2026-10-27).

record/plan/after-core-2026-10-23/report-night-V.md, findings 1 and 2: session A's 30 by 30
matrices (a right fold of 900 terms) and the native driver's 500 iterations passed Python's
recursion limit in the Runner's whnf, force and operands. These cases raise RecursionError while
the Runner's demands recurse on the Python stack; they are expected to fail (strict) until run.py's
demands run on an explicit stack (report-kernel-2026-10-27.md), and that change removes the mark.
"""

from __future__ import annotations

import pytest

from luthier import run
from luthier.kernel import reduce
from luthier.term import App, Data, Define, IntConst, Lam, Lit, Match, PCon, PVar, Primitive, Universe, Var

DEEP = 3000  # past Python's default limit of 1000 frames, and past a 500-iteration run
KERNEL_DEEP = 500  # kernel.step walks to the redex from the top: the fold is quadratic in it

SOURCE = """-- deep demands for the Runner
ones (n : Int) : List Int := if n <= 0 then nil else cons 1 (ones (n - 1))
total (xs : List Int) : Int := foldList Int Int (fn a b { a + b }) 0 (fn x { x }) xs
countUp (k : Int) (acc : Int) : Int := if k <= 0 then acc else countUp (k - 1) (acc + 1)
"""


RUNNER = pytest.mark.xfail(strict=True, reason="the Runner's whnf recurses on the Python stack (run.py)")


@pytest.fixture
def deep(tmp_path):
    path = tmp_path / "deep.lut"
    path.write_text(SOURCE, encoding="utf-8")
    return path


def _value(path, term):
    try:
        value, _, _ = run.evaluate([str(path)], term)
    except RecursionError:
        # a thousand frames of traceback cost pytest a minute to show; the fact is enough
        raise AssertionError("RecursionError") from None
    return value


@RUNNER
def test_a_right_fold_over_a_long_list(deep):
    # foldList's `op (f x) (foldList ... rest)`: each `+` demands the rest of the fold first
    assert _value(deep, f"total (ones {DEEP})") == Lit(IntConst(DEEP))


@RUNNER
def test_a_recursion_whose_accumulator_is_demanded_at_the_end(deep):
    # the argument `acc + 1` is shared, not reduced, at each call: the last demand forces a chain
    # of DEEP sums, as the native driver's state after 500 iterations
    assert _value(deep, f"countUp {DEEP} 0") == Lit(IntConst(DEEP))


@RUNNER
def test_the_cores_finite_fold(deep):
    # sumTo, foldWith over Fin n, as the 30 by 30 matrices' symmetry checks fold 900 entries
    assert _value(deep, f"sumTo {DEEP} (fn k {{ 1.0 }})").constant.value == float(DEEP)


@RUNNER
def test_the_depth_is_a_parameter(deep, monkeypatch):
    # P11 (every criterion is a parameter): the explicit stack's bound, EVALUATION_DEPTH, stops a
    # demand deeper than it with the RecursionError the Python stack gave
    monkeypatch.setattr(run, "EVALUATION_DEPTH", 500)
    with pytest.raises(RecursionError):
        run.evaluate([str(deep)], f"countUp {DEEP} 0")


def test_the_kernel_reduces_a_long_fold():
    # kernel.reduce on its own (no Runner): a right fold by a match over KERNEL_DEEP cons cells.
    # Its step already ran on explicit stacks; this guards it.
    cons = lambda h, t: App(App(Var("cons"), h), t)
    xs = Var("nil")
    for _ in range(KERNEL_DEEP):
        xs = cons(Lit(IntConst(1)), xs)
    lists = Data("L", (("nil", Var("L")), ("cons", Var("L"))))
    plus = lambda a, b: App(App(Primitive("+"), a), b)
    body = Lam("xs", Var("L"), Match(Var("xs"), (
        (PCon("nil", ()), Lit(IntConst(0))),
        (PCon("cons", (PVar("h"), PVar("t"))), plus(Var("h"), App(Var("sum"), Var("t")))))))
    program = (Define("L", Universe(), lists), Define("sum", Universe(), body))
    assert reduce(program, 100 * KERNEL_DEEP, App(Var("sum"), xs)) == Lit(IntConst(KERNEL_DEEP))
