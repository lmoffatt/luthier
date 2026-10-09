#!/usr/bin/env python3
"""Replace the words of `scripts/export_chat.private` by `[private word]` in the given files, in place.

For outputs a model wrote (a lineage named with a private word, a summary that repeats one) that are
going to a public repository. The same words as `check_private.py`, matched the same way (whole word,
any case); the replacement is the same everywhere, so ids stay consistent across files. Prints what it
changed; the change is committed on its own, after the commit of the files as they came, so the
record keeps how they were.
"""
from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_private as cp  # noqa: E402

MARK = "[private word]"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--words", type=Path, default=cp.DEFAULT_WORDS)
    args = ap.parse_args(argv)
    pats = [cp.pattern(w) for w in cp.load_words(args.words)]
    total = 0
    for f in cp.files_under(args.paths, all_dirs=True):
        try:
            text = unicodedata.normalize("NFC", f.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            continue
        n = 0
        for p in pats:
            text, k = p.subn(MARK, text)
            n += k
        if n:
            f.write_text(text, encoding="utf-8")
            print(f"{f}: {n} replaced")
            total += n
    print(f"{total} replaced")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
