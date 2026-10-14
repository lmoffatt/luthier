"""The host side of world_model.lut's `host` (0c920f0): observe, print_line, read_file.

Derivation: brief record/IA/run-2026-10-13/prompt-2.md (bite 2), after prompt.md (bite 1);
choices in record/IA/run-2026-10-13/opus-2.md. The host keeps the standard output so far; files
are read from disk at each observation (bite 3, prompt-3.md: observe takes the places). Bite 8
(prompt-8.md, D-2026-10-14-a): the calls the host makes back into Luthier, counted for the run's
record (12.S18). Plots (record/IA/plots-2026-10-15/prompt-host.md): a file is read as bytes and
turned into a string by `text_of_bytes`, so a binary file (a PNG) is observed, one character per
byte, as plots.py's `image` gives it, for world.lth's `agreement`.
"""
from dataclasses import dataclass
from pathlib import Path

_stdout = ""
_calls = {}


@dataclass(frozen=True)
class Just:
    """`just value` of `Maybe`, as it crosses the bridge (run.py turns it into the constructor)."""
    value: object


class _Nothing:
    def __repr__(self):
        return "NOTHING"


NOTHING = _Nothing()
"""`nothing` of `Maybe`, as it crosses the bridge."""


def text_of_bytes(data):
    """A file's bytes as a string: UTF-8 when they are valid UTF-8, with Python's universal
    newlines as `read_text` gave it (a text file reads as before), Latin-1 otherwise, one
    character per byte (a binary file, a PNG, plot.lth §5 [proposed])."""
    try:
        return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def _read(path):
    return text_of_bytes(Path(path).read_bytes())


def reset():
    global _stdout
    _stdout = ""
    _calls.clear()


def count(route, position):
    """One call the host made to a Luthier function it received from the extern at `route`, at
    `position` among its arguments ("1", or "1.value" for a field of a record argument)."""
    per_route = _calls.setdefault(route, {})
    per_route[position] = per_route.get(position, 0) + 1


def calls():
    """The calls counted so far in this run: route -> position -> how many (world.lth's
    `CallsAreCounted`)."""
    return {route: dict(positions) for route, positions in _calls.items()}


def stdout():
    """The text printed so far in this run (what `luthier run` writes at the end)."""
    return _stdout


def observe(w, places):
    """`W -> List String -> W * S`, `S = { stdout : String, files : List (String * String) }`, the
    state standing for the world at `places`: `stdout` is the text printed so far when "stdout" is
    among them, and "" otherwise; `files` holds (path, text) for each place that is a readable file
    on disk now (read every time; a missing file is absent), in the order of `places`."""
    files = []
    for place in places:
        if place == "stdout":
            continue
        try:
            files.append((place, _read(place)))
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
            pass
    return w, {"stdout": _stdout if "stdout" in places else "", "files": files}


def print_line(w, s):
    global _stdout
    _stdout += s + "\n"
    return w, None


def read_file(w, path):
    """`W -> String -> W * Maybe String`: `nothing` when there is no file to read."""
    try:
        text = _read(path)
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
        return w, NOTHING
    return w, Just(text)
