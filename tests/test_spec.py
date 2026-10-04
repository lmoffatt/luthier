"""The specification suite of docs/semantica/04-kernel.md and 05-static-semantics.md.

Every `*.accept.lut` under tests/spec must load without error; every `*.reject.lut` must fail
with a message containing the fragment of its `-- expect:` comment. The kernel of `04` and the
static semantics of `05` are not implemented yet, so each case is marked xfail; a case that
starts passing is reported as XPASS, which is the signal to drop its mark.
"""
import glob
import os
import re

import pytest

from luthier.cli import load

HERE = os.path.dirname(__file__)
SPEC = os.path.join(HERE, "spec")

ACCEPT = sorted(glob.glob(os.path.join(SPEC, "*.accept.lut")))
REJECT = sorted(glob.glob(os.path.join(SPEC, "*.reject.lut")))

NOT_IMPLEMENTED = pytest.mark.xfail(reason="04 kernel and 05 static semantics not implemented", strict=False)


def expected_fragment(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"--\s*expect:\s*(.*)", line)
            if m:
                return m.group(1).strip()
    raise AssertionError(f"{os.path.basename(path)} has no `-- expect:` comment")


@NOT_IMPLEMENTED
@pytest.mark.parametrize("path", ACCEPT, ids=[os.path.basename(p) for p in ACCEPT])
def test_accepted(path):
    load([path])


@NOT_IMPLEMENTED
@pytest.mark.parametrize("path", REJECT, ids=[os.path.basename(p) for p in REJECT])
def test_rejected(path):
    fragment = expected_fragment(path)
    with pytest.raises(SystemExit) as e:
        load([path])
    assert fragment in str(e.value), f"expected {fragment!r} in {e.value}"
