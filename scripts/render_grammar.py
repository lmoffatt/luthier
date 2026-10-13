#!/usr/bin/env python3
"""Render luthierSyntax in chapter 2's notation (renderer v1; no seed or parameters)."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from luthier.ebnf import GRAMMAR_LTH, Ebnf, Rhs, luthier_syntax

CHAPTER = ROOT / "docs/spec/02-grammar.md"
BEGIN = "<!-- luthierSyntax: begin -->"
END = "<!-- luthierSyntax: end -->"


def rhs_tokens(rhs: Rhs, parent: str = "") -> list[str]:
    """Keep literals atomic when wrapping, and preserve nested tuple grouping."""
    kind = rhs[0]
    if kind == "lit":
        return ["newline" if rhs[1] == "\n" else json.dumps(rhs[1], ensure_ascii=False)]
    if kind in ("cat", "ref"):
        return [rhs[1]]
    if kind in ("opt", "rep"):
        left, right = ("[", "]") if kind == "opt" else ("{", "}")
        return [left, *rhs_tokens(rhs[1]), right]
    if kind in ("seq", "alt") and len(rhs[1]) >= 2:
        out = []
        for child in rhs[1]:
            if out and kind == "alt":
                out.append("|")
            out.extend(rhs_tokens(child, kind))
        if parent == kind or (kind == "alt" and parent == "seq"):
            return ["(", *out, ")"]
        return out
    raise ValueError(f"chapter notation cannot faithfully render {rhs!r}")


def render(grammar: Ebnf) -> str:
    lines = []
    for name, rhs in grammar.rules:
        line = f"    {name} ::="
        continuation = "        "
        depth = 0
        for token in rhs_tokens(rhs):
            depth += (token == "(") - (token == ")")
            if (token == "|" and depth == 0) or len(line) + 1 + len(token) > 100:
                lines.append(line)
                line = continuation + token
            else:
                line += " " + token
            if len(line) > 100:
                raise ValueError(f"token too long for chapter notation: {token!r}")
        lines.append(line)
        lines.append("")
    return "\n".join(lines) + "\n"


def generated_block() -> str:
    digest = hashlib.sha256(GRAMMAR_LTH.read_bytes()).hexdigest()
    return (
        "\n\nGenerated from `src/luthier/lib/grammar.lth` by `scripts/render_grammar.py`\n"
        f"(v1; sha256: {digest}).\n\n"
        + render(luthier_syntax()) + "\n"
    )


def updated_chapter(text: str) -> str:
    lines = text.splitlines(keepends=True)
    begins = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == BEGIN]
    ends = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == END]
    if len(begins) != 1 or len(ends) != 1 or begins[0] >= ends[0]:
        raise ValueError("chapter must contain one ordered pair of luthierSyntax marker lines")
    return (
        "".join(lines[:begins[0] + 1]) + generated_block()[1:] + "".join(lines[ends[0]:])
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--chapter", type=Path, default=CHAPTER, help="chapter path (for copies)")
    args = parser.parse_args()
    try:
        original = args.chapter.read_text(encoding="utf-8")
        expected = updated_chapter(original)
        if args.write:
            args.chapter.write_text(expected, encoding="utf-8")
        elif original != expected:
            print(f"{args.chapter}: generated grammar is stale; run scripts/render_grammar.py --write",
                  file=sys.stderr)
            return 1
    except (OSError, ValueError) as error:
        print(f"{args.chapter}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
