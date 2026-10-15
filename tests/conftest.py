"""Shared test hygiene. A run records a host action validated at its first application in the
store of the file that defines the model (record/IA/certification-2026-10-14/
prompt-first-action.md, 10.S10), and a test that runs a program over world_model.lut would write
its fixture's arguments into src/luthier/lib/world_model.cert.json. Each test reads and writes a
copy of the library's stores instead, in a directory of its own that certify.store_path takes from
`LUTHIER_LIBRARY_STORES` (the processes a test spawns inherit it), so that the library's stores
hold what `luthier run` and `luthier certify` wrote on purpose, and a `luthier certify` running
beside the suite keeps what it writes (record/IA/controls-2026-10-15/prompt-tail.md; before, the
stores were put back after each test, which reverted certify's writes made meanwhile)."""
import contextlib
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from luthier import certify

LIBRARY = Path(__file__).resolve().parents[1] / "src" / "luthier" / "lib"


@contextlib.contextmanager
def library_stores_apart():
    """The library's stores copied to a temporary directory that the stores are read from and
    written to while inside; the library's own are not touched, and the copy is removed after."""
    before = os.environ.get(certify.LIBRARY_STORES)
    with tempfile.TemporaryDirectory(prefix="library-stores-") as copy:
        for store in LIBRARY.glob("*.cert.json"):
            shutil.copyfile(store, Path(copy) / store.name)
        os.environ[certify.LIBRARY_STORES] = copy
        try:
            yield Path(copy)
        finally:
            if before is None:
                os.environ.pop(certify.LIBRARY_STORES, None)
            else:
                os.environ[certify.LIBRARY_STORES] = before


@pytest.fixture(autouse=True)
def _library_stores_apart():
    with library_stores_apart():
        yield
