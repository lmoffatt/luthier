#!/usr/bin/env python3
"""Project `docs/principles.md` from `record/principles-language.md`, and check the three documents.

The record (D-2026-10-12-d) holds every organizer (G) and principle of the language (L) as an
entry inside a fenced block: a head line `<tag>  <statement>` at column 0, the statement continued
on indented lines, then fields `Name:` at column 0 continued on indented lines, and, since v2
(D-2026-10-12-g), numbered clauses `<tag>.<n>  <text> [<status>]` at column 0, continued on
indented lines, each with its own status from the vocabulary settled, proposed, candidate, mark
pending. The fields are Tier, From, Formulation, Example, References, Rests on, Quote, Source,
Status, History. Outside the fences, the record has prose sections under `##` and `###` headings;
before `## Terms` it has the drafts table and a `## Numbering` section.

The projection, written for the agent that builds the specification, keeps from the record what
follows its `## Terms` heading: the headings, the prose, and for each entry its tag, statement,
Formulation, Tier or From, clauses, Example, References, Rests on, and Status; it ends with the
record's `## Numbering` section. It drops Quote, Source and History (they are in the record), the
drafts table before `## Terms`, and any prose paragraph that starts with `(History:`. Its header
names the record's content hash, the record's last commit, this script's version and the date, so
the projection carries how it was derived (P2).

`--check` exits 1 when `docs/principles.md` differs from the projection of the record (compared
below the header, which carries the date), when `docs/principles-for-readers.md` cites a G or L the
record does not define, and it lists, as information, the entries the readers' document does not
cite. It also runs the two lints of D-2026-10-12-o over the projected text: every reference
resolves (a G, L or L.n tag to an entry or clause; a D id to `record/decisions.md`; a P to
`record/principles.md`; a W to `docs/way-of-working.md`; an R to the static semantics; a
backticked spec or rationale number to a file), and no sentence of eight words or more appears
twice, in two entries or in one (any run of eight words). The lints are information unless `--strict`, when they fail the
check; clause statuses outside the vocabulary and gaps in clause numbering fail it always.
`--write` writes the projection. With neither, prints it.

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

VERSION = "project_principles v2"
REPO_ROOT = Path(__file__).resolve().parent.parent
RECORD = REPO_ROOT / "record" / "principles-language.md"
PROJECTION = REPO_ROOT / "docs" / "principles.md"
READERS = REPO_ROOT / "docs" / "principles-for-readers.md"

HEAD_RE = re.compile(r"^([GL]\d+)\s+(.*)$")
CLAUSE_RE = re.compile(r"^([GL]\d+)\.(\d+)\s+(.*)$")
FIELD_RE = re.compile(r"^(Tier|From|Formulation|Example|References|Rests on|Quote|Source|Status|History):\s*(.*)$")
TAG_RE = re.compile(r"\b([GL]\d+)\b")
REF_RE = re.compile(r"\b([GL]\d+)(?:\.(\d+))?\b")
D_RE = re.compile(r"\bD-\d{4}-\d{2}-\d{2}-[a-z]+\b")
P_RE = re.compile(r"\bP(\d+)\b")
W_RE = re.compile(r"\bW(\d+)\b")
R_RE = re.compile(r"\bR(\d+)\b")
DOC_RE = re.compile(r"`(\d\d)(?: §\d+)?`")
STATUS_RE = re.compile(r"^(.*?)\s*\[(settled|proposed|candidate|mark pending)\]$")
STATUSES = ("settled", "proposed", "candidate", "mark pending")
FIELDS_PROJECTED = ("Formulation", "Tier", "From", "Example", "References", "Rests on", "Status")
START_HEADING = "## Terms"
NUMBERING_HEADING = "## Numbering"
MIN_WORDS = 8


def parse_record(text: str) -> list[tuple[str, object]]:
    """Return the record from `## Terms` on, as a list of ("prose", str) and ("entry", dict).

    An entry dict has "tag", "statement", its fields by name, and "clauses": a list of dicts with
    "n", "text" and "status" (None when the clause carries no bracketed status)."""
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
            for c in entry["clauses"]:
                m = STATUS_RE.match(c["text"])
                if m:
                    c["text"], c["status"] = m.group(1), m.group(2)
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
        m = CLAUSE_RE.match(line)
        if m and entry is not None:
            if m.group(1) != entry["tag"]:
                raise SystemExit(f"{entry['tag']}: clause {m.group(1)}.{m.group(2)} under another tag")
            entry["clauses"].append({"n": int(m.group(2)), "text": m.group(3).strip(), "status": None})
            field = "clause"
            continue
        m = HEAD_RE.match(line)
        if m and entry is None:
            entry = {"tag": m.group(1), "statement": m.group(2).strip(), "clauses": []}
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
            if field == "clause":
                c = entry["clauses"][-1]
                c["text"] = (c["text"] + " " + line.strip()).strip()
            else:
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
    if e["clauses"]:
        out.append("\n".join(
            wrap(f"- {e['tag']}.{c['n']} {c['text']}" + (f" [{c['status']}]" if c["status"] else ""))
            .replace("\n", "\n  ") for c in e["clauses"]))
    for name in ("Example", "References", "Rests on"):
        if name in e:
            out.append(wrap(f"{name}: {e[name]}."))
    if "Status" in e:
        out.append(wrap(f"Status: {e['Status']}."))
    return "\n".join(out)


def render_prose(block: str) -> str:
    paras = re.split(r"\n\s*\n", block)
    kept = [p for p in paras if not p.lstrip().startswith("(History:")]
    return "\n\n".join(kept)


def numbering_section(record_text: str) -> str:
    """The record's `## Numbering` section, from before `## Terms`, or the empty string."""
    m = re.search(rf"(?ms)^{re.escape(NUMBERING_HEADING)}\s*$.*?(?=^## |\Z)", record_text)
    return m.group(0).rstrip("\n") if m else ""


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
        "what it derives from, its clauses each with its status, and its status; his quotes, the sources "
        "and the history by draft are in the record, and the way of working, W1 to W15, is "
        "`docs/way-of-working.md`.",
    ])


def project(record_text: str, today: str | None = None) -> str:
    today = today or date.today().isoformat()
    parts = [header(record_text, today)]
    for kind, item in parse_record(record_text):
        parts.append(render_prose(item) if kind == "prose" else render_entry(item))
    parts.append(numbering_section(record_text))
    return "\n\n".join(p for p in parts if p.strip()) + "\n"


def body(text: str) -> str:
    """The projection below its header: from the first `## ` heading on."""
    i = text.find("\n## ")
    return text[i:] if i >= 0 else text


# ---- the lints (D-2026-10-12-o) ----------------------------------------------------------------

def known_ids(root: Path) -> dict[str, set[str] | None]:
    """The ids each class of reference may resolve to; None when the file to read is missing, in
    which case that class is not checked."""
    def ids(path: Path, pattern: str) -> set[str] | None:
        if not path.exists():
            return None
        return set(re.findall(pattern, path.read_text(encoding="utf-8"), re.M))
    docs = set()
    for d in ("docs/spec", "docs/rationale"):
        if (root / d).exists():
            docs |= {p.name[:2] for p in (root / d).glob("[0-9][0-9]-*.md")}
    return {
        "D": ids(root / "record/decisions.md", r"^(D-\d{4}-\d{2}-\d{2}-[a-z]+)\s"),
        "P": ids(root / "record/principles.md", r"^P(\d+)\b"),
        "W": ids(root / "docs/way-of-working.md", r"^\*\*W(\d+)\b"),
        "R": ids(root / "docs/spec/05-static-semantics.md", r"\bR(\d+)\b"),
        "doc": docs if docs else None,
    }


def lint_references(items: list, record_text: str, root: Path) -> list[str]:
    """Every G, L, L.n, D, P, W, R and backticked document number in the projected text resolves."""
    entries = [e for k, e in items if k == "entry"]
    tags = {e["tag"] for e in entries}
    clauses = {f"{e['tag']}.{c['n']}" for e in entries for c in e["clauses"]}
    known = known_ids(root)
    problems: list[str] = []
    scopes: list[tuple[str, str]] = []
    for kind, item in items:
        if kind == "prose":
            scopes.append((scope_label(item), render_prose(item)))
        else:
            text = " ".join(item.get(f, "") for f in FIELDS_PROJECTED)
            text += " " + " ".join(c["text"] for c in item["clauses"])
            scopes.append((item["tag"], text))
    for where, text in scopes:
        for m in REF_RE.finditer(text):
            tag, n = m.group(1), m.group(2)
            if tag not in tags:
                problems.append(f"{where}: {tag} is not an entry")
            elif n and f"{tag}.{n}" not in clauses:
                problems.append(f"{where}: {tag}.{n} is not a clause")
        for cls, rx in (("D", D_RE), ("P", P_RE), ("W", W_RE), ("R", R_RE), ("doc", DOC_RE)):
            if known[cls] is None:
                continue
            for m in rx.finditer(text):
                ident = m.group(1) if cls != "D" else m.group(0)
                if ident not in known[cls]:
                    problems.append(f"{where}: {m.group(0)} does not resolve")
    return sorted(set(problems))


def sentences(text: str) -> list[str]:
    """The sentences of MIN_WORDS words or more, normalized; headings dropped, a paragraph break
    and a bullet a sentence boundary."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        lines = [re.sub(r"^\s*[-*]\s+", "", l) for l in para.splitlines() if not l.lstrip().startswith("#")]
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z(\"`*])", " ".join(l.strip() for l in lines)):
            s = re.sub(r"\s+", " ", s).strip().strip("\"'").lower()
            if len(s.split()) >= MIN_WORDS:
                out.append(s)
    return out


def scope_label(block: str) -> str:
    """A prose block is named by its first heading, or its first line."""
    for l in block.splitlines():
        if l.startswith("#"):
            return l.strip()[:40]
    return block.splitlines()[0][:40]


def shingles(text: str) -> list[tuple[str, ...]]:
    """Every run of MIN_WORDS consecutive words of the text, normalized; a run never crosses a
    paragraph break, a heading or a bullet."""
    runs = []
    for para in re.split(r"\n\s*\n", text):
        lines = [re.sub(r"^\s*[-*]\s+", "", l) for l in para.splitlines() if not l.lstrip().startswith("#")]
        for piece in re.split(r"^\s*$", " ".join(l.strip() for l in lines), flags=re.M):
            words = [re.sub(r"[^\w'∞ε≡]+", "", w.lower()) for w in piece.split()]
            words = [w for w in words if w]
            runs.extend(tuple(words[i:i + MIN_WORDS]) for i in range(len(words) - MIN_WORDS + 1))
    return runs


def lint_duplicates(items: list) -> list[str]:
    """No run of MIN_WORDS words appears in two entries, or twice in one; one line per pair, with
    the longest shared run as the example."""
    where_runs: dict[str, list[tuple[str, ...]]] = {}
    for kind, item in items:
        if kind == "prose":
            where, text = scope_label(item), render_prose(item)
        else:
            where = item["tag"]
            text = "\n\n".join([item.get("Formulation", ""), item.get("Example", "")]
                                + [c["text"] for c in item["clauses"]])
        where_runs[where] = shingles(text)
    problems = []
    wheres = list(where_runs)
    sets = {w: set(r) for w, r in where_runs.items()}
    def longest(shared: set, runs_a, runs_b) -> str:
        # extend a shared run to the longest common stretch, greedily from its first occurrence
        best = ""
        for run in shared:
            i = runs_a.index(run)
            j = runs_b.index(run)
            k = MIN_WORDS
            while i + k - MIN_WORDS + 1 < len(runs_a) and j + k - MIN_WORDS + 1 < len(runs_b) \
                    and runs_a[i + k - MIN_WORDS + 1] == runs_b[j + k - MIN_WORDS + 1]:
                k += 1
            words = list(run) + [runs_a[i + t][-1] for t in range(1, k - MIN_WORDS + 1)]
            if len(words) > len(best.split()):
                best = " ".join(words)
        return best
    for a_i, a in enumerate(wheres):
        runs_a = where_runs[a]
        counts: dict[tuple[str, ...], int] = {}
        for r in runs_a:
            counts[r] = counts.get(r, 0) + 1
        twice = {r for r, c in counts.items() if c > 1}
        if twice:
            problems.append(f"{a}, {a}: \"{longest(twice, runs_a, runs_a)}\"")
        for b in wheres[a_i + 1:]:
            shared = sets[a] & sets[b]
            if shared:
                problems.append(f"{a}, {b}: \"{longest(shared, runs_a, where_runs[b])}\"")
    return problems


def lint_clauses(items: list) -> list[str]:
    """Clause numbers run 1..n and every clause carries a status from the vocabulary."""
    problems = []
    for kind, e in items:
        if kind != "entry" or not e["clauses"]:
            continue
        ns = [c["n"] for c in e["clauses"]]
        if ns != list(range(1, len(ns) + 1)):
            problems.append(f"{e['tag']}: clauses numbered {ns}, expected 1..{len(ns)}")
        for c in e["clauses"]:
            if c["status"] is None:
                problems.append(f"{e['tag']}.{c['n']}: no status; one of {', '.join(STATUSES)}")
    return problems


def check(record_text: str, strict: bool = False) -> int:
    rc = 0
    items = parse_record(record_text)
    tags = [e["tag"] for k, e in items if k == "entry"]
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
    for p in lint_clauses(items):
        print(f"clauses: {p}"); rc = 1
    refs = lint_references(items, record_text, REPO_ROOT)
    dups = lint_duplicates(items)
    label = "problem" if strict else "information"
    for p in refs:
        print(f"references ({label}): {p}")
    for p in dups:
        print(f"duplicates ({label}): {p}")
    if strict and (refs or dups):
        rc = 1
    print(f"lints: {len(refs)} unresolved references, {len(dups)} repeated sentences")
    print("ok" if rc == 0 else "problems found")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--record", type=Path, default=RECORD)
    ap.add_argument("--write", action="store_true", help=f"write {PROJECTION.relative_to(REPO_ROOT)}")
    ap.add_argument("--check", action="store_true", help="check the three documents; exit 1 on a problem")
    ap.add_argument("--strict", action="store_true", help="with --check: the two lints fail the check")
    ap.add_argument("--date", default=None, help="date for the header (default: today)")
    args = ap.parse_args()
    record_text = args.record.read_text(encoding="utf-8")
    if args.check:
        return check(record_text, strict=args.strict)
    text = project(record_text, args.date)
    if args.write:
        PROJECTION.write_text(text, encoding="utf-8")
        print(f"wrote {PROJECTION.relative_to(REPO_ROOT)} ({len(text.splitlines())} lines)")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
