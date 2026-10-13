"""Command line interface for the bootstrap Luthier parser."""

from __future__ import annotations

import argparse
from pathlib import Path

from .parse import parse
from .surface import ParseFailed, Parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="luthier")
    sub = parser.add_subparsers(dest="command", required=True)
    p_parse = sub.add_parser("parse", help="parse Luthier source files")
    p_parse.add_argument("--tree", action="store_true", help="print each parsed act")
    p_parse.add_argument("files", nargs="+")
    p_check = sub.add_parser("check", help="check static semantics")
    p_check.add_argument("-v", "--verbose", action="store_true")
    p_check.add_argument("files", nargs="+")
    p_eval = sub.add_parser("eval", help="reduce a definition to weak head normal form")
    p_eval.add_argument("file")
    p_eval.add_argument("name")
    p_eval.add_argument("--fuel", type=int, default=10000)
    p_run = sub.add_parser("run", help="run a program with the host world")
    p_run.add_argument("file")
    p_run.add_argument("--main", default="main")
    p_run.add_argument("--fuel", type=int, default=10_000_000,
                       help="reduction fuel [proposed: default 10,000,000, 10,000 was a hundred times too small for validate_graph.lut]")
    ns = parser.parse_args(argv)

    if ns.command == "run":
        from .run import run_file
        try:
            print(run_file(ns.file, ns.main, ns.fuel), end="")
            return 0
        except (OSError, ValueError, RecursionError) as exc:
            import sys
            print(f"{ns.file}: {exc}", file=sys.stderr)
            return 1

    if ns.command == "eval":
        from .elaborate import ElaborationError, elaborate_program, show_term
        from .kernel import reduce
        from . import term as t
        try:
            result = parse(Path(ns.file).read_text(encoding="utf-8"))
            if isinstance(result, ParseFailed):
                for error in result.errors:
                    print(f"{ns.file}:{error.line}:{error.column}: {error.message}")
                return 1
            program = elaborate_program(result.program)
            if not any(isinstance(a, t.Define) and a.name == ns.name for a in program):
                print(f"unknown definition: {ns.name}")
                return 1
            # Bootstrap core arithmetic, retaining user definitions as overrides.
            # (a reversible choice: the alternative resolves through core.lut's `operator` acts)
            from .kernel import BOOTSTRAP_PRIMITIVES
            program += tuple(t.Define(op, t.Universe(), t.Primitive(op))
                             for op in BOOTSTRAP_PRIMITIVES)
            value = reduce(program, ns.fuel, t.Var(ns.name))
            if value is None:
                print(f"fuel spent ({ns.fuel})")
                return 1
            print(show_term(value))
            return 0
        except (OSError, ElaborationError, ValueError) as exc:
            print(f"{ns.file}: {exc}")
            return 1

    failed = False
    for raw_path in ns.files:
        path = Path(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"{path}:1:0: {exc}")
            failed = True
            continue
        result = parse(text)
        if isinstance(result, ParseFailed):
            failed = True
            for error in result.errors:
                print(f"{path}:{error.line}: syntax <parse>: {error.message}" if ns.command == "check"
                      else f"{path}:{error.line}:{error.column}: {error.message}")
        elif ns.command == "check":
            from .check import check, report
            import re
            def line_of(name):
                return next((i for i, line in enumerate(text.splitlines(), 1)
                             if re.match(r"^" + re.escape(name) + r"(?:\s|:|=|$)", line)), 1)
            failures = check(result.program, path)
            failed |= bool(failures)
            for failure in failures:
                print(f"{path}:{line_of(failure.name)}: {failure.rule} {failure.name}: {failure.message}")
            if ns.verbose:
                for item in report(result.program):
                    print(f"{path}:{line_of(item.name)}: {item.kind} {item.name}: {item.message}")
        elif ns.tree and isinstance(result, Parsed):
            for act in result.program:
                print(act)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
