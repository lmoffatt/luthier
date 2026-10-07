"""The Python side: load a program, fill its holes, evaluate, certify."""
import math
import os

import pytest

import luthier
from luthier import FillError


def write(tmp_path, name, src):
    p = tmp_path / name
    p.write_text(src)
    return str(p)


def test_a_filled_hole_evaluates_and_its_laws_are_certified(tmp_path):
    path = write(tmp_path, "sq.lut", '''
import "real"
import "real_python"
Sqrt : U := { f : Positive -> R | \\ (x : Positive) { approx 0.000000001 (f x * f x) x } }
root : Sqrt
twice (x : Positive) : R := root x + root x
''')
    P = luthier.load(path)
    assert P.holes() == ["root"]
    assert P.blocked_by("root") == {"holes": ["root"], "types": []}
    P.fill("root", math.sqrt)
    assert P.holes() == []
    assert P.eval("twice 16.0") == 8.0
    r = P.test("root", n=50, seed=1)
    assert r.passed and r.laws[0].cases == 50
    assert os.path.exists(str(tmp_path / "sq.cert.json"))
    assert "root" in P.checker.certified


def test_the_signature_is_checked_against_the_type(tmp_path):
    path = write(tmp_path, "f.lut", 'f : R -> R -> R\n')
    P = luthier.load(path)
    with pytest.raises(FillError):
        P.fill("f", lambda a: a)
    with pytest.raises(FillError):
        P.fill("f", lambda a, b, c: a)
    P.fill("f", lambda a, b: a * b)
    assert P.eval("f 2.0 3.5") == 7.0
    with pytest.raises(FillError):
        P.fill("R", float)         # not a hole of the program


def test_records_cross_as_dataclasses_in_both_directions(tmp_path):
    path = write(tmp_path, "pt.lut", '''
import "real"
import "real_python"
Pt : U := { x : R, y : R | true }
norm : Pt -> R
mk   : R -> Pt
mk2  : R -> Pt
far (r : R) : R := norm (mk r)
''')
    P = luthier.load(path)
    seen = []

    def norm(p):
        seen.append(p)
        return math.hypot(p.x, p.y)
    P.fill("norm", norm)
    assert P.eval("norm (3.0, 4.0)") == 5.0
    assert type(seen[0]).__name__ == "Pt" and seen[0].x == 3.0
    Pt = P.record("Pt")
    P.fill("mk", lambda r: Pt(x=r, y=r))           # a dataclass comes back
    P.fill("mk2", lambda r: (r, 2.0 * r))           # so does a tuple in order
    assert abs(P.eval("far 3.0") - math.sqrt(18.0)) < 1e-12
    assert P.eval("norm (mk2 3.0)") == math.hypot(3.0, 6.0)
    p = P.eval("mk 1.5")
    assert p.x == 1.5 and p.y == 1.5


def test_a_value_hole_a_list_and_a_returned_callable(tmp_path):
    path = write(tmp_path, "misc.lut", '''
import "real"
import "real_python"
c : R
sumList : List R -> R
scale : R -> (R -> R)
Ev : U := { region : R -> Bool, level : R | true }
mkEv : R -> Ev
holds (e : Ev) (x : R) : Bool := e.region x
''')
    P = luthier.load(path)
    P.fill("c", lambda: 2.5)
    assert P.eval("c + 1.0") == 3.5
    P.fill("sumList", lambda xs: float(sum(xs)))
    assert P.eval("sumList [1.0, 2.0, 3.5]") == 6.5
    P.fill("scale", lambda k, x: k * x)             # R -> (R -> R) is R -> R -> R: two arguments
    assert P.eval("scale 2.0 3.0") == 6.0
    assert P.eval("scale 2.0") (4.0) == 8.0          # a partial application comes back as a callable
    P.fill("mkEv", lambda lo: ((lambda x: x >= lo), 0.5))
    assert P.eval("holds (mkEv 1.0) 2.0") is True
    assert P.eval("holds (mkEv 1.0) 0.5") is False


def test_a_luthier_function_passed_to_python_receives_typed_arguments(tmp_path):
    path = write(tmp_path, "fn.lut", '''
import "real"
import "real_python"
Pt : U := { x : R, y : R | true }
applyAt : (Pt -> R) -> R -> R
norm2 (p : Pt) : R := p.x * p.x + p.y * p.y
''')
    P = luthier.load(path)
    P.fill("applyAt", lambda f, r: f((r, r)))     # Python calls the Luthier function on a record
    assert P.eval("applyAt norm2 3.0") == 18.0


def test_filling_a_hole_makes_dependent_certificates_stale(tmp_path):
    path = write(tmp_path, "dep.lut", '''
import "real"
import "real_python"
k : R
Big : U := { f : R -> R | \\ (x : R) { f x >= x } }
grow : Big := \\ x { x + k }
test grow with 20
''')
    P = luthier.load(path)
    assert P.blocked_by("grow")["holes"] == ["k"]
    P.fill("k", lambda: 1.0)
    assert P.test("grow", seed=3).passed
    Q = luthier.load(path)
    Q.fill("k", lambda: -1.0)
    r = Q.test("grow", seed=3)
    assert not r.passed and r.laws[0].failure is not None
