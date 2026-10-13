"""World places for one run; derived from world_model.lut at 1f8c61c."""
from pathlib import Path

_stdout = ""
_files: dict[str, str] = {}


def reset():
    global _stdout
    _stdout = ""
    _files.clear()


def places():
    return ["stdout", *_files]


def read_place(name):
    return _stdout if name == "stdout" else _files.get(name)


def print_line(w, s):
    global _stdout
    _stdout += s + "\n"
    return w, None


def read_file(w, path):
    text = Path(path).read_text(encoding="utf-8")
    _files[path] = text
    return w, text
