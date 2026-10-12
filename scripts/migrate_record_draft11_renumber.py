#!/usr/bin/env python3
"""Draft 11, the contiguous numbering (D-2026-10-12-v): the principles renumbered in document order,
L1 to L13, in record/principles-language.md and docs/principles-for-readers.md. Remapped: the entry
tags, the clause tags, and every L reference in the projected fields (statement, From, clauses,
Example, References, Rests on, Status) and in the prose after `## Purpose`, except the (History:)
paragraphs; untouched: Quote, Source, History, the drafts table and the P13 table, which keep the
tags of their time. The Numbering table gains a column. Mechanical, no model."""
import re
import textwrap
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pp", ROOT / "scripts/project_principles.py")
pp = importlib.util.module_from_spec(spec); spec.loader.exec_module(pp)
RECORD = ROOT / "record/principles-language.md"
READERS = ROOT / "docs/principles-for-readers.md"

MAP = {"L1": "L1", "L4": "L2", "L5": "L3", "L9": "L4", "L10": "L5", "L13": "L6", "L15": "L7",
       "L2": "L8", "L7": "L9", "L16": "L10", "L14": "L11", "L6": "L12", "L8": "L13"}
MERGED = {"L3": "L8", "L11": "L4", "L12": "L5"}     # draft 10 tags merged in draft 11, and where
TAG = re.compile(r"\bL(\d+)(\.\d+)?\b")

def remap(text: str) -> str:
    def sub(m):
        t = "L" + m.group(1)
        if t not in MAP:
            raise SystemExit(f"unmapped tag {t} in: {text[max(0, m.start()-60):m.end()+20]!r}")
        return MAP[t] + (m.group(2) or "")
    return TAG.sub(sub, text)

text = RECORD.read_text(encoding="utf-8")
lines = text.splitlines()
start = next(i for i, l in enumerate(lines) if l.strip() == "## Purpose")
head, body = "\n".join(lines[:start]), "\n".join(lines[start:])

# ---- the head: the note and the Numbering table ------------------------------------------------
head = head.replace(
    "The table under Numbering maps the old tags to the\nnew; inside `Quote:`, `Source:` and `History:` a tag written before draft 10 is an old one, and\n`record/decisions.md` keeps the old tags in its Kind lines until it is updated.",
    "Since draft 11 (D-2026-10-12-v) they are\nnumbered contiguously in document order, L1 to L13. The table under Numbering maps the tags of\neach draft; inside `Quote:`, `Source:` and `History:` a tag carries the numbering of its time, and\n`record/decisions.md` keeps in its Kind lines the tags of the day each decision was taken.")
assert "numbered contiguously" in head
rows_out = []
in_table = False
new_head = []
for l in head.splitlines():
    if l.startswith("| Draft 11 | Before | What happened |"):
        new_head.append("| Draft 11 | Draft 10 | Before | What happened |")
        in_table = True
        continue
    if in_table and l.startswith("|---|---|---|"):
        new_head.append("|---|---|---|---|")
        continue
    if in_table and l.startswith("| "):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        d10, before, what = cells[0], cells[1], cells[2]
        if d10 in MAP:
            d11 = MAP[d10]
        elif d10 in MERGED:
            d11 = f"merged into {MERGED[d10]}"
        elif d10.startswith("G"):
            d11 = d10 if d10 != "G3" else "dissolved"
        else:
            d11 = "—"
        new_head.append(f"| {d11} | {d10} | {before} | {what} |")
        continue
    if in_table and not l.startswith("|"):
        in_table = False
    new_head.append(l)
head = "\n".join(new_head)
head = head.replace("The tags of draft 10 against those of drafts 1 to 9 (his marks on the reorder plan, 14ea9f0).",
                    "The tags of draft 11 (contiguous, in document order, D-2026-10-12-v) against those of draft 10\n(his marks on the reorder plan, 14ea9f0) and of drafts 1 to 9.")
assert "| L10 | L16 | new |" in head and "| merged into L8 | L3 |" in head, head[-3000:]

# ---- the body: prose and entries ---------------------------------------------------------------
def field(name, t):
    first = f"{name}:" + " " * max(1, 12 - len(name) - 1)
    return textwrap.fill(t, width=100, initial_indent=first, subsequent_indent=" " * 12,
                         break_long_words=False, break_on_hyphens=False)

def head_line(tag, stmt):
    return textwrap.fill(stmt, width=100, initial_indent=f"{tag}" + " " * max(1, 4 - len(tag)),
                         subsequent_indent="    ", break_long_words=False, break_on_hyphens=False)

def clause_line(tag, n, t, status):
    first = f"{tag}.{n}" + " " * max(1, 7 - len(f"{tag}.{n}"))
    return textwrap.fill(f"{t} [{status}]", width=100, initial_indent=first, subsequent_indent=" " * 7,
                         break_long_words=False, break_on_hyphens=False)

def render(e):
    old_tag = e["tag"]
    tag = MAP.get(old_tag, old_tag)
    out = [head_line(tag, remap(e["statement"]))]
    for name in ("Tier", "From", "Formulation"):
        if name in e:
            out.append(field(name, remap(e[name])))
    for c in e["clauses"]:
        out.append(clause_line(tag, c["n"], remap(c["text"]), c["status"]))
    for name in ("Example", "References", "Rests on"):
        if name in e:
            out.append(field(name, remap(e[name])))
    if "Quote" in e:
        out.append(field("Quote", e["Quote"]))
    out.append(field("Source", e["Source"]))
    if "Status" in e:
        out.append(field("Status", remap(e["Status"])))
    hist = e.get("History", "")
    if old_tag != tag:
        hist += f" draft 11 (2026-10-12): renumbered from {old_tag} of draft 10 (D-2026-10-12-v)."
    out.append(field("History", hist.strip()))
    return "\n".join(out)

def remap_prose(block):
    paras = re.split(r"(\n\s*\n)", block)
    return "".join(p if p.lstrip().startswith("(History:") or re.fullmatch(r"\n\s*\n", p) else remap(p)
                   for p in paras)

out = []
items = pp.parse_record(body if body.startswith("## Purpose") else "## Purpose\n" + body)
fence_open = False
entries_buf = []
for k, it in items:
    if k == "prose":
        if entries_buf:
            out += ["```", "\n\n".join(entries_buf), "```", ""]
            entries_buf = []
        out += [remap_prose(it), ""]
    else:
        entries_buf.append(render(it))
if entries_buf:
    out += ["```", "\n\n".join(entries_buf), "```", ""]
res = head.rstrip("\n") + "\n\n" + "\n".join(out).rstrip("\n") + "\n"
RECORD.write_text(res, encoding="utf-8")

# ---- the readers' document ---------------------------------------------------------------------
r = READERS.read_text(encoding="utf-8")
i = r.index("## What Luthier is")
rhead, rbody = r[:i], r[i:]
rbody = re.sub(r"\(((?:[GL]\d+)(?:, [GL]\d+)*)\)",
               lambda m: "(" + ", ".join(dict.fromkeys(MAP.get(t, t) for t in m.group(1).split(", "))) + ")",
               rbody)
old = ("Draft 4, 2026-10-12, unapproved: the citations follow draft 11 of `docs/principles.md`, where L3,\n"
       "L11 and L12 merged into L2, L9 and L10 and L16 (certificates) is new; the prose unchanged.\n")
new = ("Draft 5, 2026-10-12, unapproved: the citations follow the contiguous numbering of draft 11 of\n"
       "`docs/principles.md` (D-2026-10-12-v; the Numbering table there maps every draft); the prose\n"
       "unchanged. Draft 4, 2026-10-12: the citations followed draft 11 before its renumbering, where\n"
       "three entries merged into others and the certificate entry was new.\n")
assert old in rhead
rhead = rhead.replace(old, new)
READERS.write_text(rhead + rbody, encoding="utf-8")
print("renumbered:", len(res.splitlines()), "lines")
