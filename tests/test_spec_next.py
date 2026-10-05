"""The specification suite of docs/semantica/06-numbers.md, decided and not implemented yet.

The accept/reject programs under tests/spec/next, and the bridge's checks, which are about running
rather than checking. Every case is marked xfail; a case that passes is reported as XPASS, the
signal to move it to tests/spec and drop its mark.
"""
import glob
import os
import re

import pytest

from luthier.cli import load

HERE = os.path.dirname(__file__)
NEXT = os.path.join(HERE, "spec", "next")

ACCEPT = sorted(glob.glob(os.path.join(NEXT, "*.accept.lut")))
REJECT = sorted(glob.glob(os.path.join(NEXT, "*.reject.lut")))

NOT_YET = pytest.mark.xfail(reason="06-numbers not implemented", strict=False)


def expected_fragment(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"--\s*expect:\s*(.*)", line)
            if m:
                return m.group(1).strip()
    raise AssertionError(f"{os.path.basename(path)} has no `-- expect:` comment")


@NOT_YET
@pytest.mark.parametrize("path", ACCEPT, ids=[os.path.basename(p) for p in ACCEPT])
def test_accepted(path):
    load([path])


@NOT_YET
@pytest.mark.parametrize("path", REJECT, ids=[os.path.basename(p) for p in REJECT])
def test_rejected(path):
    fragment = expected_fragment(path)
    with pytest.raises(SystemExit) as e:
        load([path])
    assert fragment in str(e.value), f"expected {fragment!r} in {e.value}"


def _eval(tmp_path, src: str, term: str):
    import luthier
    p = tmp_path / "bridge.lut"
    p.write_text(src)
    return luthier.load(str(p)).eval(term)


@NOT_YET
def test_nan_from_the_environment_is_an_error(tmp_path):
    from luthier.evaluator import EvalError
    with pytest.raises(EvalError, match="NaN"):
        _eval(tmp_path, 'npSqrt : Float64 -> Float64 := extern "python:numpy.sqrt"\n', "npSqrt (0.0 - 1.0)")


@NOT_YET
def test_overflow_to_infinity_is_an_error(tmp_path):
    from luthier.evaluator import EvalError
    with pytest.raises(EvalError, match="overflow|infinite"):
        _eval(tmp_path, "big : Float64 := 1e308 * 10.0\n", "big")


@NOT_YET
def test_an_integer_beyond_64_bits_does_not_cross_into_numpy(tmp_path):
    from luthier.evaluator import EvalError
    src = 'npAbs : Int -> Int := extern "python:numpy.abs"\n'
    with pytest.raises(EvalError, match="64"):
        _eval(tmp_path, src, "npAbs (2 * 9223372036854775807)")


@NOT_YET
def test_axioms_are_listed_by_check(tmp_path, capsys):
    from luthier.cli import main
    p = tmp_path / "uses_reals.lut"
    p.write_text('import "algebra"\n')
    assert main(["check", str(p), "-v"]) == 0
    assert "assumed realField" in capsys.readouterr().out
