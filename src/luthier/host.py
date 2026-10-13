"""The host side of world_model.lut's `host` (0c920f0): observe, print_line, read_file.

Derivation: brief record/IA/run-2026-10-13/prompt-2.md (bite 2), after prompt.md (bite 1);
choices in record/IA/run-2026-10-13/opus-2.md. The world of one run is the standard output so
far and the files read so far, the representation `State` of world_model.lut.
"""
from dataclasses import dataclass
from pathlib import Path

_stdout = ""
_files: dict[str, str] = {}


@dataclass(frozen=True)
class Just:
    """`just value` of `Maybe`, as it crosses the bridge (run.py turns it into the constructor)."""
    value: object


class _Nothing:
    def __repr__(self):
        return "NOTHING"


NOTHING = _Nothing()
"""`nothing` of `Maybe`, as it crosses the bridge."""


def reset():
    global _stdout
    _stdout = ""
    _files.clear()


def stdout():
    """The text printed so far in this run (what `luthier run` writes at the end)."""
    return _stdout


def observe(w):
    """The representation `State = { stdout : String, files : List (String * String) }`."""
    return w, {"stdout": _stdout, "files": list(_files.items())}


def print_line(w, s):
    global _stdout
    _stdout += s + "\n"
    return w, None


def read_file(w, path):
    """`W -> String -> W * Maybe String`: `nothing` when there is no file to read."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
        return w, NOTHING
    _files[path] = text
    return w, Just(text)
