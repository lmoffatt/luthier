"""Luthier version 0: definitions, data, subtypes with laws, extern, test.

From Python: `luthier.load("file.lut")` gives a Program whose holes the environment fills
with `fill`, evaluates with `eval` and certifies with `test` (see api.py)."""
__version__ = "0.0.1"

from .api import load, Program, FillError  # noqa: E402,F401
