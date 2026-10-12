#!/usr/bin/env python3
"""Project `docs/principles.md` from `record/principles-language.md`, and check the three documents.

The record (D-2026-10-12-d) holds every organizer (G) and principle of the language (L) as an
entry inside a fenced block: a head line `<tag>  <statement>` at column 0, the statement continued
on indented lines, then fields `Name:` at column 0 continued on indented lines. The fields are
Tier, From, Formulation, Quote, Source, Status, History. Outside the fences, the record has prose
sections under `##` and `###` headings.

The projection, written for the agent that builds the specification, keeps from the record what
follows its `## Terms` heading: the headings, the prose, and for each entry its tag, statement,
Formulation, Tier or From, and Status. It drops Quote, Source and History (they are in the record),
the drafts table before `## Terms`, and any prose paragraph that starts with `(History:`. Its
header names the record's content hash, the record's last commit, this script's version and the
date, so the projection carries how it was derived (P2).

`--check` exits 1 when `docs/principles.md` differs from the projection of the record (compared
below the header, which carries the date), when `docs/principles-for-readers.md` cites a G or L the
record does not define, and it lists, as information, the entries the readers' document does not
cite. `--write` writes the projection. With neither, prints it.

Mechanical, no model.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

VERSION = "project_principles v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
RECORD = REPO_ROOT / "record" / "principles-language.md"
PROJECTION = REPO_ROOT / "docs" / "principles.md"
READERS = REPO_ROOT / "docs" / "principles-for-readers.md"

HEAD_RE = re.compile(r"^([GL]\d+)\s+(.*)$")
FIELD_RE = re.compile(r"^(Tier|From|Formulation|Quote|Source|Status|History):\s*(.*)$")
TAG_RE = re.compile(r"\b([GL]\d+)\b")
FIELDS_PROJECTED = ("Formulation", "Tier", "From", "Status")
START_HEADING = "## Terms"


def parse_record(text: str) -> list[tuple[str, object]]:
    """Return the record from `## Terms` on, as a list of ("prose", str) and ("entry", dict)."""
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == START_HEADING)
    except StopIteration:
        raise SystemExit(f"{RECORD.name}: no `{START_HEADING}` heading")
    items: list[tuple[str, object]] = []
    in_fence = False
    prose: list[str] = []
    entry: dict | None = None
    field: str | None = None

    def close_entry():
        nonlocal entry, field
        if entry is not None:
            items.append(("entry", entry))
        entry, field = None, None

    def close_prose():
        nonlocal prose
        block = "\n".join(prose).strip("\n")
        if block.strip():
            items.append(("prose", block))
        prose = []

    for line in lines[start:]:
        if re.match(r"^\s{0,3}(```|~~~)", line):
            if in_fence:
                close_entry()
            else:
                close_prose()
            in_fence = not in_fence
            continue
        if not in_fence:
            prose.append(line)
            continue
        if not line.strip():
            close_entry()
            continue
        m = HEAD_RE.match(line)
        if m and entry is None:
            entry = {"tag": m.group(1), "statement": m.group(2).strip()}
            field = "statement"
            continue
        m = FIELD_RE.match(line)
        if m and entry is not None:
            field = m.group(1)
            if field in entry:
                raise SystemExit(f"{entry['tag']}: field {field} given twice")
            entry[field] = m.group(2).strip()
            continue
        if entry is not None and field and line.startswith(" "):
            entry[field] = (entry[field] + " " + line.strip()).strip()
            continue
        raise SystemExit(f"{RECORD.name}: cannot read line inside a fence: {line!r}")
    if in_fence:
        raise SystemExit(f"{RECORD.name}: a fence is not closed")
    close_prose()
    return items


def wrap(text: str, width: int = 100) -> str:
    import textwrap
    return "\n".join(textwrap.fill(p, width=width, break_long_words=False, break_on_hyphens=False)
                     for p in text.split("\n"))


def render_entry(e: dict) -> str:
    head = f"**{e['tag']}. {e['statement']}**"
    if "Formulation" in e:
        f = e["Formulation"]
        head += " " + f[:1].upper() + f[1:]
    out = [wrap(head)]
    if "Tier" in e:
        out.append(wrap(f"Tier: {e['Tier']}."))
    if "From" in e:
        out.append(wrap(f"From: {e['From']}."))
    if "Status" in e:
        out.append(wrap(f"Status: {e['Status']}."))
    return "\n".join(out)


def render_prose(block: str) -> str:
    paras = re.split(r"\n\s*\n", block)
    kept = [p for p in paras if not p.lstrip().startswith("(History:")]
    return "\n\n".join(kept)


def record_commit() -> str:
    try:
        h = subprocess.run(["git", "log", "-1", "--format=%h", "--", str(RECORD)], cwd=REPO_ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", str(RECORD)], cwd=REPO_ROOT,
                               capture_output=True, text=True, check=True).stdout.strip()
        return h + (" (modified in the working tree)" if dirty else "")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def header(record_text: str, today: str) -> str:
    digest = hashlib.sha256(record_text.encode("utf-8")).hexdigest()[:12]
    return "\n".join([
        "# The principles of Luthier",
        "",
        f"Projected from `record/principles-language.md` (sha256 {digest}, commit {record_commit()}) by "
        f"`scripts/project_principles.py` ({VERSION}) on {today}; not edited by hand: edit the record and "
        "rerun the script (D-2026-10-12-d). Written for the agent that builds the specification. Each "
        "entry gives its statement, its current formulation (the model's unless a clause is marked his), "
        "what it derives from, and its status; his quotes, the sources and the history by draft are in "
        "the record, and the way of working, W1 to W15, is `docs/way-of-working.md`.",
    ])


def project(record_text: str, today: str | None = None) -> str:
    today = today or date.today().isoformat()
    parts = [header(record_text, today)]
    for kind, item in parse_record(record_text):
        parts.append(render_prose(item) if kind == "prose" else render_entry(item))
    return "\n\n".join(p for p in parts if p.strip()) + "\n"


def body(text: str) -> str:
    """The projection below its header: from the first `## ` heading on."""
    i = text.find("\n## ")
    return text[i:] if i >= 0 else text


def check(record_text: str) -> int:
    rc = 0
    tags = [e["tag"] for k, e in parse_record(record_text) if k == "entry"]
    if PROJECTION.exists():
        if body(PROJECTION.read_text(encoding="utf-8")) != body(project(record_text)):
            print(f"{PROJECTION.relative_to(REPO_ROOT)} differs from the projection of the record; "
                  f"run scripts/project_principles.py --write")
            rc = 1
    else:
        print(f"{PROJECTION.relative_to(REPO_ROOT)} missing"); rc = 1
    if READERS.exists():
        cited = set(TAG_RE.findall(READERS.read_text(encoding="utf-8")))
        undefined = sorted(cited - set(tags), key=lambda t: (t[0], int(t[1:])))
        if undefined:
            print(f"{READERS.relative_to(REPO_ROOT)} cites what the record does not define: "
                  f"{', '.join(undefined)}")
            rc = 1
        uncited = [t for t in tags if t not in cited]
        print(f"{READERS.relative_to(REPO_ROOT)}: {len(cited & set(tags))} of {len(tags)} entries cited"
              + (f"; not cited: {', '.join(uncited)}" if uncited else ""))
    else:
        print(f"{READERS.relative_to(REPO_ROOT)} missing (not written yet)")
    print("ok" if rc == 0 else "problems found")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--record", type=Path, default=RECORD)
    ap.add_argument("--write", action="store_true", help=f"write {PROJECTION.relative_to(REPO_ROOT)}")
    ap.add_argument("--check", action="store_true", help="check the three documents; exit 1 on a problem")
    ap.add_argument("--date", default=None, help="date for the header (default: today)")
    args = ap.parse_args()
    record_text = args.record.read_text(encoding="utf-8")
    if args.check:
        return check(record_text)
    text = project(record_text, args.date)
    if args.write:
        PROJECTION.write_text(text, encoding="utf-8")
        print(f"wrote {PROJECTION.relative_to(REPO_ROOT)} ({len(text.splitlines())} lines)")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
