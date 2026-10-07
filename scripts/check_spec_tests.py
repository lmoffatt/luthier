#!/usr/bin/env python3
"""Check that every well-formedness rule of the static semantics has its tests.

The rules are the paragraphs of section 5 of `docs/spec/05-static-semantics.md` that start
with `**R<n>.`. A rule's paragraph runs until the next rule or the next heading. Each rule needs
at least one test the checker must accept and one it must reject in `tests/spec/`, named
`r<n>_<name>.accept.lut` and `r<n>_<name>.reject.lut`. A rule whose paragraph says "not
implemented" is reported as such, never as missing tests.

Each finding is printed as `path:line: spec-tests: message`, where path and line point at the rule
in the specification. Exit status: 0 with no findings, 1 with findings, 2 when the specification
cannot be read or has no rules in section 5.

Step 4.2 of record/plan-working-method-execution-2026-10-06.md.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SPEC = REPO_ROOT / "docs" / "spec" / "05-static-semantics.md"
DEFAULT_TESTS = REPO_ROOT / "tests" / "spec"

SECTION_RE = re.compile(r"^##\s+5\.\s")
SECTION_END_RE = re.compile(r"^#{1,2}\s")
HEADING_RE = re.compile(r"^#+\s")
RULE_RE = re.compile(r"^\*\*R(\d+)\.\s*(.*)$")
TITLE_RE = re.compile(r"^(.*?)\*\*")
TEST_RE = re.compile(r"^r(\d+)_.+\.(accept|reject)\.lut$")
NOT_IMPLEMENTED = "not implemented"


@dataclass
class Rule:
    number: int
    title: str
    line: int  # 1-based line of the rule in the specification
    text: str  # the paragraph with its whitespace collapsed to single spaces


def read_rules(spec_text: str) -> list[Rule]:
    """The rules of section 5, in the order they appear."""
    lines = spec_text.splitlines()
    start = next((i for i, l in enumerate(lines) if SECTION_RE.match(l)), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(lines)) if SECTION_END_RE.match(lines[i])),
               len(lines))

    rules: list[Rule] = []
    current: tuple[int, str, int, list[str]] | None = None

    def close() -> None:
        if current is not None:
            number, title, line, body = current
            rules.append(Rule(number, title, line, " ".join(" ".join(body).split())))

    for i in range(start + 1, end):
        text = lines[i]
        m = RULE_RE.match(text)
        if m:
            close()
            title_match = TITLE_RE.match(m.group(2))
            title = (title_match.group(1) if title_match else m.group(2)).strip().rstrip(".")
            current = (int(m.group(1)), title, i + 1, [text])
        elif HEADING_RE.match(text):
            close()
            current = None
        elif current is not None:
            current[3].append(text)
    close()
    return rules


def read_tests(tests_dir: Path) -> dict[int, set[str]]:
    """For each rule number, the kinds of test files present ("accept", "reject")."""
    kinds: dict[int, set[str]] = {}
    for entry in sorted(tests_dir.iterdir()) if tests_dir.is_dir() else []:
        m = TEST_RE.match(entry.name)
        if m and entry.is_file():
            kinds.setdefault(int(m.group(1)), set()).add(m.group(2))
    return kinds


def findings(rules: list[Rule], tests: dict[int, set[str]], tests_label: str) -> list[tuple[Rule, str]]:
    out: list[tuple[Rule, str]] = []
    for rule in rules:
        name = f"R{rule.number} ({rule.title})"
        if NOT_IMPLEMENTED in rule.text.lower():
            out.append((rule, f"{name} is marked not implemented"))
            continue
        present = tests.get(rule.number, set())
        missing = [k for k in ("accept", "reject") if k not in present]
        if len(missing) == 2:
            out.append((rule, f"{name} has no tests: no r{rule.number}_*.accept.lut and no "
                              f"r{rule.number}_*.reject.lut in {tests_label}"))
        elif missing:
            kind = missing[0]
            out.append((rule, f"{name} has no {kind} test: no r{rule.number}_*.{kind}.lut in "
                              f"{tests_label}"))
    return out


def display(path: Path) -> str:
    """The path relative to the working directory when it lies under it, else as given."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC,
                        help="the static semantics (default: %(default)s)")
    parser.add_argument("--tests", type=Path, default=DEFAULT_TESTS,
                        help="the folder of specification tests (default: %(default)s)")
    args = parser.parse_args(argv)

    try:
        spec_text = args.spec.read_text(encoding="utf-8")
    except OSError as e:
        print(f"spec-tests: cannot read {args.spec}: {e}", file=sys.stderr)
        return 2
    rules = read_rules(spec_text)
    if not rules:
        print(f"spec-tests: no rules `**R<n>.` in section 5 of {args.spec}", file=sys.stderr)
        return 2
    if not args.tests.is_dir():
        print(f"spec-tests: {args.tests} is not a folder", file=sys.stderr)
        return 2

    spec_label = display(args.spec)
    found = findings(rules, read_tests(args.tests), display(args.tests))
    for rule, message in found:
        print(f"{spec_label}:{rule.line}: spec-tests: {message}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
