"""EBNF grammars as data, read from Luthier's theory files, and how many ways they derive a token list.

The Python specimen of `Derives` (src/luthier/lib/ebnf.lth), counting derivations instead of
deciding them, so that a test can also see a text with two trees. It reads the value
`luthierSyntax` from src/luthier/lib/grammar.lth itself, so the grammar has one statement (spec
2.S9, L14.6): nothing here transcribes it.

A right-hand side is a tuple: ("eps",), ("lit", text), ("cat", kind), ("ref", name),
("seq", (rhs, ...)), ("alt", (rhs, ...)), ("opt", rhs), ("rep", rhs). A token view is a pair
(kind, text), as `TokenView` in ebnf.lth.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

Rhs = tuple
TokenView = tuple[str, str]

GRAMMAR_LTH = Path(__file__).parent / "lib" / "grammar.lth"

_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_]+|:=|[\[\](),{}]')


@dataclass(frozen=True)
class Ebnf:
    start: str
    rules: tuple[tuple[str, Rhs], ...]

    def rules_of(self, name: str) -> tuple[Rhs, ...]:
        return tuple(r for lhs, r in self.rules if lhs == name)


def _unquote(s: str) -> str:
    body = s[1:-1]
    return re.sub(r"\\(.)", lambda m: {"n": "\n"}.get(m.group(1), m.group(1)), body)


def read_ebnf(text: str, value: str) -> Ebnf:
    """Read the `Ebnf` value named `value` from the text of a Luthier file, in the form
    `value : ... := { start := "s", rules := [ { lhs := "n", rhs := <rhs> }, ... ] }`."""
    at = re.search(rf"^{re.escape(value)}\s*:", text, re.M)
    if at is None:
        raise ValueError(f"no value {value!r}")
    toks = _TOKEN.findall(text[at.end():])
    pos = 0

    def take(expect: str | None = None) -> str:
        nonlocal pos
        tok = toks[pos]
        pos += 1
        if expect is not None and tok != expect:
            raise ValueError(f"expected {expect!r}, got {tok!r} near {toks[pos - 5:pos + 5]}")
        return tok

    def rhs() -> Rhs:
        head = take()
        if head == "eps":
            return ("eps",)
        if head in ("lit", "cat", "ref"):
            return (head, _unquote(take()))
        if head in ("seq", "alt"):
            take("[")
            items = []
            while toks[pos] != "]":
                items.append(rhs())
                if toks[pos] == ",":
                    take(",")
            take("]")
            return (head, tuple(items))
        if head in ("rep", "opt"):
            if toks[pos] == "(":
                take("(")
                inner = rhs()
                take(")")
                return (head, inner)
            return (head, rhs())
        if head == "(":
            inner = rhs()
            take(")")
            return inner
        raise ValueError(f"unexpected {head!r}")

    while toks[pos] != "{":
        pos += 1
    take("{")
    take("start"), take(":=")
    start = _unquote(take())
    take(",")
    take("rules"), take(":="), take("[")
    rules = []
    while toks[pos] == "{":
        take("{"), take("lhs"), take(":=")
        lhs = _unquote(take())
        take(","), take("rhs"), take(":=")
        rules.append((lhs, rhs()))
        take("}")
        if toks[pos] == ",":
            take(",")
    take("]")
    return Ebnf(start, tuple(rules))


def luthier_syntax() -> Ebnf:
    """`luthierSyntax`, read from grammar.lth."""
    return read_ebnf(GRAMMAR_LTH.read_text(encoding="utf-8"), "luthierSyntax")


def _children(r: Rhs) -> tuple[Rhs, ...]:
    if r[0] in ("seq", "alt"):
        return r[1]
    if r[0] in ("rep", "opt"):
        return (r[1],)
    return ()


def _walk(r: Rhs):
    yield r
    for c in _children(r):
        yield from _walk(c)


def lits_of(e: Ebnf) -> list[str]:
    """Every literal of the grammar, once, in order of appearance (`litsOf`)."""
    seen: list[str] = []
    for _, r in e.rules:
        for x in _walk(r):
            if x[0] == "lit" and x[1] not in seen:
                seen.append(x[1])
    return seen


def cats_of(e: Ebnf) -> list[str]:
    """Every category of the grammar, once (`catsOf`)."""
    seen: list[str] = []
    for _, r in e.rules:
        for x in _walk(r):
            if x[0] == "cat" and x[1] not in seen:
                seen.append(x[1])
    return seen


def lits_of_names(e: Ebnf, names: list[str]) -> list[str]:
    """The literals written directly in the rules of the named nonterminals (`litsOfNames`)."""
    seen: list[str] = []
    for lhs, r in e.rules:
        if lhs in names:
            for x in _walk(r):
                if x[0] == "lit" and x[1] not in seen:
                    seen.append(x[1])
    return seen


def count_derivations(e: Ebnf, tokens: list[TokenView], start: str | None = None) -> int:
    """How many derivations of `tokens` from `start` (the grammar's start symbol by default).
    A literal matches a token by its text, a category by its kind (`LitOne`, `CatOne`). Defined on
    grammars without left recursion (`WellFormedEbnf`): a right-hand side is entered at the same
    span only behind a part that derived the empty list."""
    ts = tuple(tokens)
    rules = {lhs: e.rules_of(lhs) for lhs, _ in e.rules}
    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(limit, 20000))
    try:
        @lru_cache(maxsize=None)
        def nt(name: str, i: int, j: int) -> int:
            return sum(rhs(r, i, j) for r in rules.get(name, ()))

        @lru_cache(maxsize=None)
        def rhs(r: Rhs, i: int, j: int) -> int:
            kind = r[0]
            if kind == "eps":
                return int(i == j)
            if kind == "lit":
                return int(j == i + 1 and ts[i][1] == r[1])
            if kind == "cat":
                return int(j == i + 1 and ts[i][0] == r[1])
            if kind == "ref":
                return nt(r[1], i, j)
            if kind == "alt":
                return sum(rhs(x, i, j) for x in r[1])
            if kind == "opt":
                return int(i == j) + rhs(r[1], i, j)
            if kind == "seq":
                return seq(r[1], i, j)
            if kind == "rep":
                return rep(r[1], i, j)
            raise ValueError(f"unknown right-hand side {r!r}")

        @lru_cache(maxsize=None)
        def seq(xs: tuple[Rhs, ...], i: int, j: int) -> int:
            if not xs:
                return int(i == j)
            total = 0
            for m in range(i, j + 1):
                first = rhs(xs[0], i, m)
                if first:
                    total += first * seq(xs[1:], m, j)
            return total

        @lru_cache(maxsize=None)
        def rep(x: Rhs, i: int, j: int) -> int:
            # a round consumes something (`RepRounds`)
            if i == j:
                return 1
            total = 0
            for m in range(i + 1, j + 1):
                first = rhs(x, i, m)
                if first:
                    total += first * rep(x, m, j)
            return total

        return nt(start or e.start, 0, len(ts))
    finally:
        sys.setrecursionlimit(limit)


def derives(e: Ebnf, tokens: list[TokenView], start: str | None = None) -> bool:
    """`derives`: whether the grammar derives the token list."""
    return count_derivations(e, tokens, start) > 0
