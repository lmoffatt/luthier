"""The host side of world_model.lut's `host` (0c920f0): observe, print_line, read_file.

Derivation: brief record/IA/run-2026-10-13/prompt-2.md (bite 2), after prompt.md (bite 1);
choices in record/IA/run-2026-10-13/opus-2.md. The host keeps the standard output so far; files
are read from disk at each observation (bite 3, prompt-3.md: observe takes the places). Bite 8
(prompt-8.md, D-2026-10-14-a): the calls the host makes back into Luthier, counted for the run's
record (12.S18). Plots (record/IA/plots-2026-10-15/prompt-host.md): a file is read as bytes and
turned into a string by `text_of_bytes`, so a binary file (a PNG) is observed, one character per
byte, as plots.py's `image` gives it, for world.lth's `agreement`.

2026-10-26, Claude Opus 5.5, night agent P, on D-2026-10-16-n (what is trusted and what is checked):
in a run (`reset(stdout)`), `print_line` writes at once to the run's standard output and checks
what each `write()` returns, raising `Rejected` when the system takes no byte or reports an error,
so the action fails; the standard output is observed according to what it is connected to
(`place`): a regular file by re-reading it from where the run began, a pipe by the host's own copy
of the bytes it accepted (its tee), a terminal or another device by the bytes it accepted. Without
a stream (`eval`, `session`, a test calling the host) `print_line` keeps the copy alone, as before.
"""
import fcntl
import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path

_stdout = ""
_calls = {}
_reads = []
_out = None    # the run's standard output: (stream, its descriptor or None), or None with no stream
_place = None  # what the standard output is connected to (`place`)


class Rejected(OSError):
    """The system rejected bytes an action wrote (D-2026-10-16-n): the action failed. `place` is
    where, `accepted` how many bytes of the text it took before it stopped."""
    def __init__(self, place, message, accepted=0):
        super().__init__(message)
        self.place, self.accepted = place, accepted


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
    data = Path(path).read_bytes()
    pair = (str(path), "sha256:" + hashlib.sha256(data).hexdigest())
    if pair not in _reads:
        _reads.append(pair)
    return text_of_bytes(data)


def files_read():
    """The files read so far in this run, as (path as the program gave it, sha256 of its bytes), in
    the order first read, each pair once (12.S18: what a record needs to say the inputs were the same)."""
    return list(_reads)


def reset(stream=None):
    """A new run: nothing printed, called or read. With `stream` (`run` gives `sys.stdout`), the
    run's standard output, written at once by `print_line` and observed by what it is connected to
    (`place`); without it, `print_line` keeps the copy alone."""
    global _stdout, _out, _place
    _stdout = ""
    _calls.clear()
    _reads.clear()
    _out, _place = None, None
    if stream is not None:
        try:
            fd = stream.fileno()
        except (AttributeError, OSError, ValueError):
            fd = None  # a stream with no descriptor (a test's capture): observed by its copy
        _out = (stream, fd)
        _place = _connected(fd)


def _connected(fd):
    """What the descriptor `fd` is connected to (D-2026-10-16-n): `kind` (file, pipe, terminal,
    device, or stream when there is no descriptor), how it is `observed` (re-read, tee, accepted)
    and the root of trust that observation rests on (world.lth §5, L11.9): a re-read rests on the
    file system, a copy of the accepted bytes on the system's delivery. A file is re-read from
    `start`, where the run's first byte goes: the end of the file when it is opened to append,
    the current offset otherwise."""
    if fd is None:
        return {"kind": "stream", "observed": "tee", "root": "SystemDelivers"}
    st = os.fstat(fd)
    if stat.S_ISREG(st.st_mode):
        append = bool(fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_APPEND)
        start = st.st_size if append else os.lseek(fd, 0, os.SEEK_CUR)
        return {"kind": "file", "observed": "re-read", "root": "FileSystemKeeps", "start": start,
                "file": (st.st_dev, st.st_ino)}
    if stat.S_ISFIFO(st.st_mode) or stat.S_ISSOCK(st.st_mode):
        return {"kind": "pipe", "observed": "tee", "root": "SystemDelivers"}
    if os.isatty(fd):
        return {"kind": "terminal", "observed": "accepted", "root": "SystemDelivers"}
    return {"kind": "device", "observed": "accepted", "root": "SystemDelivers"}


def place():
    """What the run's standard output is connected to and how it is observed, for the run's
    record (`kind`, `observed`, `root`, and `accepted`, the bytes the system accepted there); None
    with no stream."""
    if _place is None:
        return None
    shown = {k: v for k, v in _place.items() if k in ("kind", "observed", "root")}
    shown["accepted"] = len(_stdout.encode("utf-8"))
    return shown


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
    """The text printed so far in this run: the host's copy of what the standard output accepted."""
    return _stdout


def _text(data):
    """The standard output's bytes as a string, as they are: UTF-8, or Latin-1 when they are not."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def _reread(fd):
    """The bytes of the regular file at `fd` from where the run began, read through a descriptor
    of its own (the run's may be open for writing only); None when the file cannot be opened again
    as the same file."""
    for where in (f"/proc/self/fd/{fd}", f"/dev/fd/{fd}"):
        try:
            with open(where, "rb") as f:
                st = os.fstat(f.fileno())
                if (st.st_dev, st.st_ino) != _place["file"]:
                    continue
                f.seek(_place["start"])
                return f.read()
        except OSError:
            continue
    return None


def observed_stdout():
    """The standard output as observed (D-2026-10-16-n): a regular file re-read, so what the file
    system keeps there is what is compared; a pipe, a terminal or a device by the copy of the bytes
    they accepted. A file that cannot be opened again is observed by the copy, and the place says
    so (`observed` tee)."""
    if _place is None or _place["kind"] != "file":
        return _stdout
    stream, fd = _out
    try:
        stream.flush()
    except OSError as exc:
        raise Rejected("stdout", f"stdout: {exc.strerror or exc}") from exc
    data = _reread(fd)
    if data is None:
        _place.update(observed="tee", root="SystemDelivers")
        return _stdout
    return _text(data)


def check_stdout():
    """At the end of a run: None when the standard output reads back what the host wrote there,
    else what differs. Only a file can say it (its re-read); elsewhere the copy is all there is."""
    if _place is None or _place["observed"] != "re-read":
        return None
    seen = observed_stdout()
    if seen == _stdout:
        return None
    at = next((i for i, (a, b) in enumerate(zip(seen, _stdout)) if a != b), min(len(seen), len(_stdout)))
    return (f"stdout, a file, reads back {seen[at:at + 40]!r} at character {at} where the run wrote "
            f"{_stdout[at:at + 40]!r}")


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
    return w, {"stdout": observed_stdout() if "stdout" in places else "", "files": files}


def _write(data):
    """Write `data` at the run's standard output now, checking what each `write()` returns: a
    short write goes on with the rest, an error or a write that takes nothing raises `Rejected`
    with the bytes accepted before it (D-2026-10-16-n). What Python buffered on the stream goes
    first, so that the place reads in order."""
    stream, fd = _out
    done = 0
    try:
        stream.flush()
        if fd is None:
            stream.write(data.decode("utf-8"))
            stream.flush()
            return len(data)
        view = memoryview(data)
        while done < len(data):
            n = os.write(fd, view[done:])
            if n <= 0:
                raise Rejected("stdout", f"stdout: the system took no byte of {len(data) - done}", done)
            done += n
    except Rejected:
        raise
    except OSError as exc:
        raise Rejected("stdout", f"stdout: {exc.strerror or exc} after {done} of {len(data)} bytes", done) from exc
    return done


def print_line(w, s):
    """`W -> String -> W * Unit`: the line written at once at the run's standard output, failing
    when the system rejects it; the copy holds what was accepted."""
    global _stdout
    line = s + "\n"
    if _out is not None:
        data = line.encode("utf-8")
        try:
            _write(data)
        except Rejected as exc:
            _stdout += data[:exc.accepted].decode("utf-8", errors="replace")
            raise
    _stdout += line
    return w, None


def read_file(w, path):
    """`W -> String -> W * Maybe String`: `nothing` when there is no file to read."""
    try:
        text = _read(path)
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
        return w, NOTHING
    return w, Just(text)
