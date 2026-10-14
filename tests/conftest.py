"""Shared test hygiene. A run records a host action validated at its first application in the
store of the file that defines the model (record/IA/certification-2026-10-14/
prompt-first-action.md, 10.S10), and a test that runs a program over world_model.lut would write
its fixture's arguments into src/luthier/lib/world_model.cert.json; the library's stores are put
back as they were after each test, so that they hold what `luthier run` and `luthier certify`
wrote on purpose."""
from pathlib import Path

import pytest

LIBRARY = Path(__file__).resolve().parents[1] / "src" / "luthier" / "lib"


@pytest.fixture(autouse=True)
def _library_stores_untouched():
    stores = {p: p.read_bytes() for p in LIBRARY.glob("*.cert.json")}
    yield
    for store, text in stores.items():
        if store.exists() and store.read_bytes() != text:
            store.write_bytes(text)
