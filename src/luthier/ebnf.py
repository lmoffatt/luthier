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


@lru_cache(maxsize=16)
def _productions(e: Ebnf):
    """Expand EBNF without merging alternative occurrences or user nonterminals."""
    productions = []
    by_name = {}
    fresh = 0

    def add(lhs, symbols):
        index = len(productions)
        productions.append((lhs, tuple(symbols)))
        by_name.setdefault(lhs, []).append(index)

    def symbol(r):
        nonlocal fresh
        kind = r[0]
        if kind in {"lit", "cat"}:
            return r
        if kind == "ref":
            return ("nt", r[1])
        name = fresh
        fresh += 1
        if kind == "eps":
            add(name, ())
        elif kind == "seq":
            add(name, [symbol(x) for x in r[1]])
        elif kind == "alt":
            for child in r[1]:
                add(name, [symbol(child)])
        elif kind == "opt":
            add(name, ())
            add(name, [symbol(r[1])])
        elif kind == "rep":
            child = symbol(r[1])
            # A private wrapper marks the consuming first round of RepRounds.
            round_name = fresh
            fresh += 1
            add(round_name, [child])
            add(name, ())
            add(name, [("nonempty", round_name), ("nt", name)])
        else:
            raise ValueError(f"unknown right-hand side {r!r}")
        return ("nt", name)

    for lhs, rhs in e.rules:
        add(lhs, [symbol(rhs)])
    return productions, by_name


def count_derivations(e: Ebnf, tokens: list[TokenView], start: str | None = None) -> int:
    """Count derivations, stopping at 2 (0, 1, or at least 2).

    Earley items recognize only reachable prefixes; a packed forest counts distinct
    productions and splits afterwards. Literals match text, categories match kind
    (LitOne, CatOne). As in WellFormedEbnf, the grammar has no left recursion;
    each repetition round must consume at least one token (RepRounds).
    """
    productions, by_name = _productions(e)
    n = len(tokens)
    # A node is (end, production, dot, origin). Edges are predecessor/child
    # pairs; predictions are seeds, never multiplied by their callers.
    forest = {}
    charts = [[] for _ in range(n + 1)]
    waiting = [{} for _ in range(n + 1)]
    completed = [{} for _ in range(n + 1)]

    def insert(end, rule, dot, origin, edge=None):
        node = (end, rule, dot, origin)
        if node not in forest:
            forest[node] = set()
            charts[end].append(node)
        if edge is not None:
            forest[node].add(edge)
        return node

    for rule in by_name.get(start or e.start, ()):
        insert(0, rule, 0, 0)

    def advance(parent, child):
        end, rule, dot, origin = parent
        symbol = productions[rule][1][dot]
        if symbol[0] == "nonempty" and child[0] == end:
            return
        insert(child[0], rule, dot + 1, origin, (parent, child))

    for end, agenda in enumerate(charts):
        for node in agenda:
            _, rule, dot, origin = node
            lhs, symbols = productions[rule]
            if dot == len(symbols):
                completed[end].setdefault((origin, lhs), []).append(node)
                for parent in waiting[origin].get(lhs, ()):
                    advance(parent, node)
            else:
                symbol = symbols[dot]
                kind, value = symbol
                if kind in {"nt", "nonempty"}:
                    waiting[end].setdefault(value, []).append(node)
                    for predicted in by_name.get(value, ()):
                        insert(end, predicted, 0, end)
                    # Nullable completions may precede this waiting item.
                    for child in completed[end].get((end, value), ()):
                        advance(node, child)
                elif end < n and (tokens[end][1] if kind == "lit" else tokens[end][0]) == value:
                    insert(end + 1, rule, dot + 1, origin, (node, None))

    roots = completed[n].get((0, start or e.start), ())
    counts = {}
    # Iterative postorder avoids changing Python's recursion limit on large acts.
    for root in roots:
        stack = [(root, False)]
        while stack:
            node, ready = stack.pop()
            if node in counts:
                continue
            if node[2] == 0:
                counts[node] = 1
            elif ready:
                total = 0
                for parent, child in forest[node]:
                    total += counts[parent] * (1 if child is None else counts[child])
                    if total >= 2:
                        break
                counts[node] = min(2, total)
            else:
                stack.append((node, True))
                for parent, child in forest[node]:
                    if parent not in counts:
                        stack.append((parent, False))
                    if child is not None and child not in counts:
                        stack.append((child, False))
    return min(2, sum(counts[root] for root in roots))


def derives(e: Ebnf, tokens: list[TokenView], start: str | None = None) -> bool:
    """`derives`: whether the grammar derives the token list."""
    return count_derivations(e, tokens, start) > 0


def derives_program(e: Ebnf, tokens: list[TokenView], act: str = "act", end: TokenView = ("literal", "\n")) -> bool:
    """`derives` for a whole laid-out file of `luthierSyntax`, act by act. Since
    `program ::= { act newline }` and the newline token occurs nowhere else, a file derives iff it
    ends in a newline (or is empty) and each segment up to a newline derives `act`.
    Each segment is recognized with Earley items; splitting avoids retaining a forest
    for the whole file."""
    segment: list[TokenView] = []
    for t in tokens:
        if t == end:
            if not derives(e, segment, act):
                return False
            segment = []
        else:
            segment.append(t)
    return not segment
