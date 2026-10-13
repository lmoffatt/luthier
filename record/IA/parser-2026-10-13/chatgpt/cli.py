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
    ns = parser.parse_args(argv)

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
                print(f"{path}:{error.line}:{error.column}: {error.message}")
        elif ns.tree and isinstance(result, Parsed):
            for act in result.program:
                print(act)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())