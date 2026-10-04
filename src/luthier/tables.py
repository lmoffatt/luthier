"""Tables and their text codec: the implementation behind lib/table.lut.

A table is a list of named, typed columns and a list of rows. The text format is CSV with the
type of each column in its header cell, `name:type`, with type one of int, float, str; reading
therefore never guesses a type. Writing is canonical: ints as Python writes them, floats as
their shortest repr (which reads back to the same double), strings quoted only where CSV needs
it. Reading is tolerant of what does not change the content: CRLF line endings, a missing or an
extra final newline, spaces around numbers and header cells, floats written with more digits or
trailing zeros. It rejects what it cannot read without guessing: an unknown or missing type, a
repeated column name, a row with the wrong number of cells, a number that does not parse, a
float that is not finite.
"""
from __future__ import annotations

import csv
import io
import math
import random
from dataclasses import dataclass
from typing import Optional

TYPES = ("int", "float", "str")


@dataclass(frozen=True)
class Table:
    columns: tuple   # of (name, type)
    rows: tuple      # of tuples, one value per column

    def index(self, name: str) -> int:
        for k, (n, _) in enumerate(self.columns):
            if n == name:
                return k
        raise KeyError(name)

    # the components of the native type of lib/table.lut: this table is a value of it as it is
    @property
    def nRows(self) -> int:
        return len(self.rows)

    @property
    def names(self) -> list:
        return [n for n, _ in self.columns]

    @property
    def kinds(self) -> list:
        return [ty for _, ty in self.columns]

    def cell(self, name: str, row: int):
        """None where there is no such column; otherwise (label, value) of the sum Cell."""
        for k, (n, ty) in enumerate(self.columns):
            if n == name:
                return (_LABEL[ty], self.rows[row][k])
        return None


_LABEL = {"int": "int", "float": "real", "str": "text"}


def as_table(x) -> "Table":
    """A table built in Luthier crosses as a record of its components; read it back as a Table."""
    if isinstance(x, Table):
        return x
    names, kinds, n = list(x.names), list(x.kinds), int(x.nRows)
    rows = []
    for r in range(n):
        row = []
        for name in names:
            c = x.cell(name, r)
            row.append(c[1] if isinstance(c, tuple) else c)
        rows.append(tuple(row))
    return Table(tuple(zip(names, kinds)), tuple(rows))


class ParseError(ValueError):
    pass


# ------------------------------------------------------------------ the codec

def _cell(value, typ: str) -> str:
    if typ == "int":
        return str(int(value))
    if typ == "float":
        return repr(float(value))
    return str(value)


def render(t: Table) -> str:
    t = as_table(t)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow([f"{n}:{ty}" for n, ty in t.columns])
    for row in t.rows:
        w.writerow([_cell(v, ty) for v, (_, ty) in zip(row, t.columns)])
    return buf.getvalue()


def _read(raw: str, typ: str, where: str):
    if typ == "str":
        return raw
    s = raw.strip()
    try:
        if typ == "int":
            return int(s)
        x = float(s)
    except ValueError:
        raise ParseError(f"{where}: {raw!r} is not a {typ}")
    if not math.isfinite(x):
        raise ParseError(f"{where}: {raw!r} is not a finite float")
    return x


def parse_or_raise(text: str) -> Table:
    lines = [r for r in csv.reader(io.StringIO(text, newline="")) if r]   # blank lines carry nothing
    if not lines:
        raise ParseError("no header")
    columns = []
    for cell in lines[0]:
        name, sep, typ = cell.partition(":")
        name, typ = name.strip(), typ.strip()
        if not sep or typ not in TYPES:
            raise ParseError(f"header cell {cell!r} is not name:type with type in {TYPES}")
        if not name:
            raise ParseError(f"header cell {cell!r} has no name")
        if any(name == n for n, _ in columns):
            raise ParseError(f"column {name!r} appears twice")
        columns.append((name, typ))
    rows = []
    for r, cells in enumerate(lines[1:], start=1):
        if len(cells) != len(columns):
            raise ParseError(f"row {r}: {len(cells)} cells for {len(columns)} columns")
        rows.append(tuple(_read(c, ty, f"row {r}, column {n}") for c, (n, ty) in zip(cells, columns)))
    return Table(tuple(columns), tuple(rows))


def parse(text: str) -> Optional[Table]:
    try:
        return parse_or_raise(text)
    except ParseError:
        return None


def parse_error(text: str) -> str:
    try:
        parse_or_raise(text)
        return ""
    except ParseError as e:
        return str(e)


def read_file(path: str) -> Optional[Table]:
    with open(path, newline="") as f:
        return parse(f.read())


def write_file(path: str, t: Table) -> None:
    t = as_table(t)
    with open(path, "w", newline="") as f:
        f.write(render(t))


# ------------------------------------------------------------------ accessors

def same(a: Table, b: Table) -> bool:
    return a == b


def n_rows(t: Table) -> int:
    return len(t.rows)


def n_cols(t: Table) -> int:
    return len(t.columns)


def has_column(t: Table, name: str, typ: str) -> bool:
    return (name, typ) in t.columns


def int_at(t: Table, name: str, k: int) -> int:
    return int(t.rows[int(k)][t.index(name)])


def real_at(t: Table, name: str, k: int) -> float:
    return float(t.rows[int(k)][t.index(name)])


def text_at(t: Table, name: str, k: int) -> str:
    return str(t.rows[int(k)][t.index(name)])


def real_column(t: Table, name: str):
    import numpy as np
    k = t.index(name)
    return np.array([float(r[k]) for r in t.rows])


def from_columns(names, types, columns) -> Table:
    """A table from parallel lists: names, types, and one list of values per column."""
    rows = tuple(zip(*columns)) if columns and len(columns[0]) else ()
    return Table(tuple(zip(names, types)), rows)


# ------------------------------------------------------------------ generators
# Strings include what CSV must quote (commas, quotes, line breaks), spaces at the ends, empty
# strings and strings that look like numbers; floats include integral values, signs, zero and
# extreme exponents.

_CHARS = "ab xyz09.,\"\n\r-+e:"


def _gen_str(rng: random.Random) -> str:
    k = rng.random()
    if k < 0.1:
        return ""
    if k < 0.2:
        return str(rng.randint(-99, 99))
    return "".join(rng.choice(_CHARS) for _ in range(rng.randint(1, 8)))


def _gen_float(rng: random.Random, size: int) -> float:
    k = rng.random()
    if k < 0.1:
        return 0.0
    if k < 0.2:
        return float(rng.randint(-size, size))
    if k < 0.3:
        return rng.uniform(-1, 1) * 10.0 ** rng.randint(-300, 300)
    return rng.uniform(-size, size)


def _gen_value(rng: random.Random, typ: str, size: int):
    if typ == "int":
        return rng.randint(-10 ** rng.randint(1, 18), 10 ** rng.randint(1, 18))
    if typ == "float":
        return _gen_float(rng, size)
    return _gen_str(rng)


def gen_table(rng: random.Random, size: int) -> Table:
    ncol = rng.randint(1, 5)
    columns = tuple((f"c{k}", rng.choice(TYPES)) for k in range(ncol))
    nrow = rng.randint(0, max(0, min(size, 8)))
    rows = tuple(tuple(_gen_value(rng, ty, size) for _, ty in columns) for _ in range(nrow))
    return Table(columns, rows)


def _perturb(rng: random.Random, t: Table) -> str:
    """A rendering of t written differently, in ways that do not change its content."""
    lines = []
    header = [f"{n}:{ty}" for n, ty in t.columns]
    if rng.random() < 0.5:
        header = [f" {n} : {ty} " for n, ty in t.columns]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow(header)
    for row in t.rows:
        cells = []
        for v, (_, ty) in zip(row, t.columns):
            c = _cell(v, ty)
            if ty == "float" and rng.random() < 0.3:
                c = "%.17g" % float(v)
            elif ty == "float" and "." in c and "e" not in c and rng.random() < 0.3:
                c = c + "0"
            if ty != "str" and rng.random() < 0.3:
                c = " " + c + " "
            cells.append(c)
        w.writerow(cells)
    text = buf.getvalue()
    k = rng.random()
    if k < 0.3:
        text = text.replace("\n", "\r\n")      # also inside quoted strings: CSV keeps those
        text = None if any("\n" in str(v) or "\r" in str(v) for r in t.rows for v in r) else text
    if text is None:
        text = buf.getvalue()
    if rng.random() < 0.3 and text.endswith("\n"):
        text = text[:-1]
    elif rng.random() < 0.3:
        text = text + "\n"
    return text


def gen_perturbed(rng: random.Random, size: int):
    t = gen_table(rng, size)
    return (t, _perturb(rng, t))


def gen_text(rng: random.Random, size: int) -> str:
    return _perturb(rng, gen_table(rng, size))


def gen_broken(rng: random.Random, size: int) -> str:
    """A text that must be rejected: one defect in an otherwise valid rendering."""
    t = gen_table(rng, max(size, 2))
    while not t.rows:
        t = gen_table(rng, max(size, 2))
    lines = render(t).split("\n")
    numeric = [k for k, (_, ty) in enumerate(t.columns) if ty != "str"]
    kind = rng.choice(["ragged", "unknown type", "repeated name", "bad number", "not finite"])
    if kind == "unknown type":
        return lines[0].replace(":" + t.columns[0][1], ":real", 1) + "\n" + "\n".join(lines[1:])
    if kind == "repeated name" and len(t.columns) >= 2:
        header = ",".join(f"{t.columns[0][0]}:{ty}" if k == 1 else f"{n}:{ty}"
                          for k, (n, ty) in enumerate(t.columns))
        return header + "\n" + "\n".join(lines[1:])
    if kind in ("bad number", "not finite") and numeric:
        k = numeric[0]
        bad = "abc" if kind == "bad number" or t.columns[k][1] == "int" else rng.choice(["nan", "inf", "-inf"])
        row = list(t.rows[0])
        cells = [_cell(v, ty) for v, (_, ty) in zip(row, t.columns)]
        cells[k] = bad
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerow(cells)
        body = render(Table(t.columns, t.rows[1:])).split("\n", 1)[1]
        return lines[0] + "\n" + buf.getvalue() + body
    # ragged: a row with one cell more
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerow(
        [_cell(v, ty) for v, (_, ty) in zip(t.rows[0], t.columns)] + ["extra"])
    body = render(Table(t.columns, t.rows[1:])).split("\n", 1)[1]
    return lines[0] + "\n" + buf.getvalue() + body
