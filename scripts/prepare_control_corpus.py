#!/usr/bin/env python3
"""Prepare the corpora of the control on Python and Haskell: the design texts the filter will read,
with the passages that state each language's principles taken out, so that what the filter finds
can be compared with what the designers said.

The sources are downloaded by hand into `record/controls/<language>/sources/` (outside git, as the
bibliography's copies are, D-2026-10-09-a) and pinned by sha256 in that control's README. This
script reads them as data and writes one Markdown note per unit into
`record/controls/<language>/texts/` (outside git too), each with a frontmatter the notes extractor
reads: author, created, title, source, and the sha256 of the source file. It prints the sha256 of
every note it writes, for the README.

python: the Atom feed of Guido van Rossum's blog "The History of Python"; one note per post by him,
        leaving out the posts named in --python-exclude (the reference and noise).
haskell: the text of "A History of Haskell: Being Lazy With Class" (Hudak, Hughes, Peyton Jones,
        Wadler, HOPL III, 2007), converted with `pdftotext` (no -layout); one note per top-level
        section, leaving out section 3 (Goals, principles, and processes), the six goals of 2.3,
        and everything from the references on.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTROLS = REPO_ROOT / "record" / "controls"
PY_EXCLUDE = ["Python's Design Philosophy", "import this and The Zen of Python", "New! Now in Japanese!"]
HASKELL_AUTHORS = "Paul Hudak, John Hughes, Simon Peyton Jones, Philip Wadler"
HASKELL_DATE = "2007-06-09T00:00:00"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "x"


def html_to_text(fragment: str) -> str:
    t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>|</div>", "\n", fragment)
    t = re.sub(r"(?i)<li[^>]*>", "\n- ", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    lines = [l.strip() for l in t.splitlines()]
    out, blank = [], False
    for l in lines:
        if not l:
            if not blank and out:
                out.append("")
            blank = True
        else:
            out.append(l)
            blank = False
    return "\n".join(out).strip() + "\n"


def write_note(out_dir: Path, name: str, front: dict, body: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{name}.md"
    head = "---\n" + "".join(f"{k}: {v}\n" for k, v in front.items()) + "---\n\n"
    p.write_text(head + body, encoding="utf-8")
    return p


def python(args) -> list[Path]:
    src = CONTROLS / "python" / "sources" / "feed.xml"
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.parse(src).getroot()
    out = []
    for e in root.findall("a:entry", ns):
        title = e.find("a:title", ns).text or ""
        author = e.find("a:author/a:name", ns).text or ""
        if author != "Guido van Rossum" or title in args.python_exclude:
            continue
        link = next((l.get("href") for l in e.findall("a:link", ns) if l.get("rel") == "alternate"), "")
        published = e.find("a:published", ns).text[:19]
        body = html_to_text(e.find("a:content", ns).text or "")
        out.append(write_note(CONTROLS / "python" / "texts", f"{published[:10]}_{slug(title)}",
                              {"author": author, "created": published, "title": f"\"{title.replace(chr(34), chr(39))}\"",
                               "source": link, "source_file": "sources/feed.xml", "source_sha256": sha256(src)}, body))
    return out


def haskell(args) -> list[Path]:
    src = CONTROLS / "haskell" / "sources" / "history_flow.txt"
    lines = src.read_text(encoding="utf-8").split("\n")  # pdftotext puts form feeds; count lines as grep does
    titles = ["Introduction", "The genesis of Haskell", "Goals, principles, and processes", "Syntax",
              "Data types and pattern matching", "Haskell as a type-system laboratory", "Monads and input/output",
              "Haskell in middle age", "Implementations", "Profiling and debugging", "Applications",
              "The impact of Haskell", "Conclusion"]
    secs = []
    for n, t in enumerate(titles, 1):
        i = next((i for i, l in enumerate(lines) if l.strip() == f"{n}. {t}"), None)
        if i is None:
            raise SystemExit(f"heading not found: {n}. {t}")
        secs.append((i, n, t))
    refs = next((i for i, l in enumerate(lines) if l.strip() == "References"), len(lines))
    goals_a = next(i for i, l in enumerate(lines) if l.startswith("1. It should be suitable for teaching"))
    goals_b = next(i for i, l in enumerate(lines) if l.startswith("6. It should reduce unnecessary diversity")) + 2
    out = []
    for k, (i, n, title) in enumerate(secs):
        end = secs[k + 1][0] if k + 1 < len(secs) else refs
        end = min(end, refs)
        if n == 3 or i >= refs:
            continue
        body_lines = [l for j, l in enumerate(lines[i:end], i) if not (goals_a <= j < goals_b)]
        if n == 2:
            body_lines.insert(goals_a - i, "[The six goals the committee agreed on are left out here: they are the reference.]")
        out.append(write_note(CONTROLS / "haskell" / "texts", f"{n:02d}_{slug(title)}",
                              {"author": HASKELL_AUTHORS, "created": HASKELL_DATE, "title": f"\"{n}. {title}\"",
                               "source": "https://doi.org/10.1145/1238844.1238856", "source_file": "sources/history_flow.txt",
                               "source_sha256": sha256(src), "lines": f"{i + 1}-{end}"}, "\n".join(body_lines) + "\n"))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("language", choices=("python", "haskell"))
    ap.add_argument("--python-exclude", nargs="*", default=PY_EXCLUDE)
    args = ap.parse_args(argv)
    notes = python(args) if args.language == "python" else haskell(args)
    words = 0
    for p in notes:
        words += len(p.read_text(encoding="utf-8").split())
        print(f"{sha256(p)}  {p.relative_to(CONTROLS)}")
    print(f"{len(notes)} notes, {words} words", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
