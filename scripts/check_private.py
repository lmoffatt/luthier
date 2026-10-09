#!/usr/bin/env python3
"""Lint: no private word in what the repository publishes.

luthier is public. What comes from the archive of conversations (`record/IA/`) and what is
derived from it (`record/ideas/`, the selection, the extractions) may carry a private word from a
quote or from a model's summary. This lint scans the given paths (default: record/ideas and
record/IA) for the words of `scripts/export_chat.private` (one word or phrase per line, `#`
comments; the same list `export_chat.py` uses), whole words, case-insensitive, and prints every
hit as `path:line: word`. Exit 1 when there is one. The file at `record/IA/raw/local-only/` is
ignored by git and is skipped (--all scans it too).

    python3 scripts/check_private.py
    python3 scripts/check_private.py record/IA/selection some/file.md --words other.private
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORDS = REPO_ROOT / "scripts" / "export_chat.private"
DEFAULT_PATHS = [REPO_ROOT / "record" / "ideas", REPO_ROOT / "record" / "IA"]
SKIP_DIRS = {"local-only", "__pycache__", ".git"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".lut", ".py", ".csv", ".yaml", ".yml", ".bib", ""}


def load_words(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [w.strip() for w in path.read_text(encoding="utf-8").splitlines()
            if w.strip() and not w.startswith("#")]


def pattern(word: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(unicodedata.normalize("NFC", word)) + r"(?!\w)", re.IGNORECASE)


def files_under(paths: list[Path], all_dirs: bool) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES \
                        and (all_dirs or not (SKIP_DIRS & set(f.relative_to(p).parts[:-1]))):
                    out.append(f)
    return out


def scan(files: list[Path], words: list[str]) -> list[tuple[Path, int, str]]:
    pats = [(w, pattern(w)) for w in words]
    hits = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(unicodedata.normalize("NFC", text).splitlines(), 1):
            for w, p in pats:
                if p.search(line):
                    hits.append((f, n, w))
    return hits


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", type=Path, default=None, help="files or directories; default record/ideas and record/IA")
    ap.add_argument("--words", type=Path, default=DEFAULT_WORDS, help="the private words, one per line")
    ap.add_argument("--all", action="store_true", help="scan local-only folders too")
    args = ap.parse_args(argv)
    words = load_words(args.words)
    if not words:
        print(f"no private words at {args.words}; nothing to check", file=sys.stderr)
        return 2
    paths = args.paths or DEFAULT_PATHS
    hits = scan(files_under(paths, args.all), words)
    for f, n, w in hits:
        try:
            shown = f.relative_to(REPO_ROOT)
        except ValueError:
            shown = f
        print(f"{shown}:{n}: {w}")
    print(f"{len(hits)} hit{'s' if len(hits) != 1 else ''} of {len(words)} private words in {len(paths)} path{'s' if len(paths) != 1 else ''}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
