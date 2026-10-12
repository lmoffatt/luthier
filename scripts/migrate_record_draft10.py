#!/usr/bin/env python3
"""Step 1 of the draft 11 plan: rewrite record/principles-language.md so that its projection is
draft 10 of docs/principles.md (b7a7e23), with the new numbering (G1 theory, G2 cost, G3 demand;
L1 to L15 in six topics), nothing of the old entries dropped: Quote, Source and History of the
merged entries are carried into the entry that absorbed them; G4 (retired), the former L20 and
the section on how the organizers depend on each other become (History:) paragraphs, which the
projection does not print. Mechanical, no model; the From fields and the History lines for
draft 10 are written here by hand."""
import importlib.util
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pp", ROOT / "scripts/project_principles.py")
pp = importlib.util.module_from_spec(spec); spec.loader.exec_module(pp)

record_text = (ROOT / "record/principles-language.md").read_text(encoding="utf-8")
draft_text = (ROOT / "docs/principles.md").read_text(encoding="utf-8")

# ---- the old record -------------------------------------------------------------------------
old = {}
old_items = pp.parse_record(record_text)
for kind, item in old_items:
    if kind == "entry":
        old[item["tag"]] = item
# the record's prose before `## Terms`
head_lines = record_text.splitlines()
terms_i = next(i for i, l in enumerate(head_lines) if l.strip() == "## Terms")
# prose blocks of the old record, by heading
old_prose = [item for kind, item in old_items if kind == "prose"]
import re as _re
_sections = {}
for _b in old_prose:
    for _chunk in _re.split(r"(?m)^(?=##+ )", _b):
        if _chunk.strip():
            _sections[_chunk.splitlines()[0].strip()] = _chunk.rstrip("\n")
def old_block(start):
    for h, b in _sections.items():
        if h.startswith(start):
            return b
    raise SystemExit(f"no old prose block starting with {start!r}")
old_terms = old_block("## Terms")
old_org = old_block("## The organizers")
old_dep = old_block("## How the organizers depend on each other")
old_lintro = old_block("## The principles of the language")

# ---- draft 10 ------------------------------------------------------------------------------
d10 = draft_text[draft_text.index("\n## Terms"):]
paras = re.split(r"\n\s*\n", d10.strip("\n"))
ENTRY_RE = re.compile(r"^\*\*([GL]\d+)(?: \((?:was )?([^)]*)\))?\. (.*?)\*\* ?(.*?) Status: (.*?)\.?$", re.S)
d10_entries = {}
d10_order = []          # list of ("prose", text) | ("entry", tag)
for p in paras:
    flat = " ".join(l.strip() for l in p.splitlines())
    if flat.startswith("**G") or flat.startswith("**L"):
        m = ENTRY_RE.match(flat)
        if not m:
            raise SystemExit("cannot parse draft 10 entry: " + flat[:80])
        tag, was, stmt, form, status = m.groups()
        d10_entries[tag] = {"tag": tag, "was": was, "statement": stmt.strip(), "formulation": form.strip(),
                            "status": status.strip()}
        d10_order.append(("entry", tag))
    else:
        d10_order.append(("prose", p))

# ---- the mapping -----------------------------------------------------------------------------
G_OLD = {"G0": "G0", "G1": "G2", "G2": "G3", "G3": "G1"}
L_OLD = {"L1": ["L1"], "L2": ["L2"], "L3": ["L4"], "L4": ["L8"], "L5": ["L16", "L21"], "L6": [],
         "L7": ["L5", "L11", "L21"], "L8": ["L15"], "L9": ["L9", "L18"], "L10": ["L19", "L13"],
         "L11": ["L12"], "L12": ["L17"], "L13": ["L10"], "L14": ["L14", "L22", "L11", "L21"],
         "L15": ["L6", "L7"]}
# which old entries are the primary carrier (their Quote/Source/History copied whole); the others
# contribute only the part named
PART = {("L7", "L21"): "the distinction identity/law", ("L14", "L11"): "delegation as citation",
        ("L14", "L21"): "the graded transport", ("L5", "L21"): "the identity clauses"}

TIER = {
    "G0": "the guide",
    "G1": "eureka, the first (the trigger, audio 09.19, 00:00 to 00:14); G2 until draft 9, printed "
          "first since draft 8 (D-2026-10-12-a)",
    "G2": "the second eureka on his note of 2026-10-12; good use until draft 9, when it was G3",
    "G3": "the executive face; an eureka until draft 9, when it was G1; printed third on his "
          "renumbering of 2026-10-12",
}
FROM = {
    "L1": "G1 (what is known of a thing is its description; \"la idea de luthier es ayudar a "
          "descubrir las invariantes de los calculos\", note), with P14 (a type is a concept)",
    "L2": "G0 directly; the second clause is the step to G1",
    "L3": "G0 (a law is a proposition; its subtype is the type of its proofs) with G1 (verified, "
          "not constructed)",
    "L4": "G0 (a hole is a hypothesis of the context) with G3 (nothing is produced until demanded)",
    "L5": "G0 (the identity type and its levels) with G2 (under cost, the identity proposition "
          "acquires a distance); the identity clauses from G1 (the specimen can be recognized as "
          "the same specimen, or described)",
    "L6": "G2 directly (lift, exact and within were named under it on his mark, draft 9) with G3 "
          "(the cutoff lives in the demand)",
    "L7": "G0 (a law defines the object) and G1 (a law that transcribes the specimen is "
          "acquaintance, not description; observation is how a description is verified) with G2 "
          "(the grade is the uncertainty of the cost); extends P10 (the mathematical object that "
          "best represents a concept is the invariant of its type)",
    "L8": "G2 directly: the realization's distance to the ideal law is the law's value, and the "
          "tolerance is the demand's (G3)",
    "L9": "G3 (the DAG is what the demand walks backward) with G2 (the second structure's metric); "
          "a definition without effects is G3's precondition rather than its consequence: the "
          "declarative face can be universal and minimally processed only if definitions have no "
          "effects; the separation of the second structure is the model's proposal",
    "L10": "G3 directly; the audio of 08.58 (15:35 to 17:12, 30:37 to 31:21) adds the iteration "
           "step, read every demand, run, collapse to the outputs, write, and asks whether the "
           "code object is consumed or stable: kept; with G1 for what is derived (the former L13)",
    "L11": "G0 (identity is the first proposition; his \"path equivalence is the fundamental "
           "concept\", 2026-05-29); the two faces are G3's statement; the verification of actions "
           "from G1 (observation) and G3",
    "L12": "G3 (the tolerance belongs to the demand) and G2 (a law states a distance, not a "
           "threshold), so a constant in the code has no place to live; restates P11 (every "
           "criterion is a parameter, never a constant in the code)",
    "L13": "G0 (the quotient), G2 (the choice by cost and the database of runs) and, before its "
           "retirement, G4 (every path expressible; now L13's own clause)",
    "L14": "G1: an absorbed library is a specimen known by its description, and its code is not "
           "needed (\"que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las "
           "funciones con sus propias invarianzas\", audio 08.58, 31:25 to 32:00); the world from "
           "G3 (the demand names the world it runs in) with L11; delegation from G1 and G2 (the "
           "former L11); transport from G1 (the former L21)",
    "L15": "G0 (a type theory is a few rules whose judgments a person checks; a small trusted "
           "kernel) and G1 (the paper semantics is the description, and every interpreter is a "
           "specimen certified against it); programs as data from G0 through the universe, the "
           "type of types (the object classifier of HoTT; the note's \"object classifier\" names "
           "this when it means types as values, and the subobject classifier when it means G2's "
           "truth values)",
}
D10 = "draft 10 (72cc7be, 81c1794, 25f9c5e, b7a7e23)"
HIST10 = {
    "G0": f"{D10}: statement and formulation kept; the organizers renumbered on his note of "
          "2026-10-12 (G1 theory and model, G2 cost, G3 the demand).",
    "G1": f"{D10}: renumbered from G2 on his note of 2026-10-12; the formulation is his note put "
          "in order, the long form of draft 9 kept below in this History; the former L3 (defining "
          "a model defines its test) and L20 (a function is declared in a theory) absorbed, their "
          "fields below.",
    "G2": f"{D10}: renumbered from G3 on his note of 2026-10-12 and named the second eureka; lift, "
          "exact and within moved to the new L6; the formulation rewritten in his words.",
    "G3": f"{D10}: renumbered from G1 on his note of 2026-10-12, printed third.",
    "L1": f"{D10}: number kept; first of the six topics.",
    "L2": f"{D10}: number kept.",
    "L3": f"{D10}: renumbered from L4; \"from a law\" is his correction of 2026-10-12.",
    "L4": f"{D10}: renumbered from L8.",
    "L5": f"{D10}: renumbered from L16; the identity clauses of the former L21 joined; the "
          "composition of identities as paths added from his note of 2026-10-12 on the reorder "
          "plan, proposed.",
    "L6": f"{D10}: new, on his note of 2026-10-12 on the plan (\"faltan las leyes de los costos y "
          "de los predicates y cómo se lift a costos\"); the text is the record's G3 of draft 9 "
          "(lift, exact, within) and the paragraph that stood in G2; the composed grade from the "
          "former L11.",
    "L7": f"{D10}: the former L5 and L11 merged and renumbered; the distinction identity/law of "
          "the former L21 joined; delegation as citation moved to L14.",
    "L8": f"{D10}: renumbered from L15.",
    "L9": f"{D10}: the former L9 and L18 merged.",
    "L10": f"{D10}: the former L19 and L13 merged; the decorated output as another model added "
           "(proposed, on his note on Terms); the former L13 restated without the forgetful "
           "functor on his note of 2026-10-12.",
    "L11": f"{D10}: renumbered from L12; shortened on his note of 2026-10-12: evaluation and "
           "execution are in Terms, the reading of computation as the kernel of a function stays "
           "in this record (History below).",
    "L12": f"{D10}: renumbered from L17; statement in his words, 2026-10-12.",
    "L13": f"{D10}: renumbered from L10; statement in his words, 2026-10-12; his formula for the "
           "efficiency, exp(−cost) over the resources, added (proposed wording).",
    "L14": f"{D10}: the former L14 and L22 merged; delegation (former L11) and transport (former "
           "L21, his correction) placed here on his note of 2026-10-12.",
    "L15": f"{D10}: the former L6 and L7 merged.",
}
# text of draft 9 formulations that draft 10 dropped from the projection and the entry keeps
KEEP = {
    "G1": "the long form of G2 at draft 9: " + old["G2"]["Formulation"],
    "L11": "the reading dropped from the projection at draft 10: " + old["L12"]["Formulation"],
}

# ---- rendering -------------------------------------------------------------------------------
def field(name, text):
    pad = " " * 12
    first = f"{name}:" + " " * max(1, 12 - len(name) - 1)
    return textwrap.fill(text, width=100, initial_indent=first, subsequent_indent=pad,
                         break_long_words=False, break_on_hyphens=False)

def statement_line(tag, stmt):
    first = f"{tag}" + " " * max(1, 4 - len(tag))
    return textwrap.fill(stmt, width=100, initial_indent=first, subsequent_indent="    ",
                         break_long_words=False, break_on_hyphens=False)

def merged(new_tag, olds, name):
    parts = []
    for o in olds:
        e = old[o]
        if name not in e:
            continue
        part = PART.get((new_tag, o))
        label = f"({o}" + (f", {part}" if part else "") + ") " if len(olds) > 1 else ""
        parts.append(label + e[name])
    return " ".join(parts)

def entry(tag, olds, d, from_text=None, tier=None):
    out = [statement_line(tag, d["statement"])]
    if tier:
        out.append(field("Tier", tier))
    if from_text:
        out.append(field("From", from_text))
    out.append(field("Formulation", d["formulation"]))
    q = merged(tag, olds, "Quote")
    if q:
        out.append(field("Quote", q))
    s = merged(tag, olds, "Source") or "his note of 2026-10-12 on the reorder plan (14ea9f0)"
    out.append(field("Source", s))
    out.append(field("Status", d["status"]))
    h = merged(tag, olds, "History")
    h = (h + " " if h else "") + HIST10[tag]
    if tag in KEEP:
        h += " " + KEEP[tag]
    out.append(field("History", h))
    return "\n".join(out)

def history_para(title, text):
    return textwrap.fill(f"(History: {title} {text})", width=100, break_long_words=False,
                         break_on_hyphens=False)

def old_entry_as_text(o):
    e = old[o]
    bits = [f"{o} {e['statement']}"]
    for n in ("Tier", "From", "Formulation", "Quote", "Source", "Status", "History"):
        if n in e:
            bits.append(f"{n}: {e[n]}")
    return " ".join(bits)

def wrap_prose(block):
    # draft 10 prose is already wrapped; keep as is
    return block

# ---- the head of the record ---------------------------------------------------------------------
head = "\n".join(head_lines[:terms_i]).rstrip("\n")
head = head.replace(
    "The statements and the sources of the L are those of draft 1 unless the history says otherwise;\n"
    "L numbers are kept (D4 of the generative plan), and the entries are printed by organizer, in his\n"
    "order of the eurekas (G2 first, D-2026-10-12-a).",
    "Since draft 10 the entries carry the numbering of 2026-10-12: G1 theory and model, G2 cost, G3\n"
    "the demand; L1 to L15 in his six topics. The table under Numbering maps the old tags to the\n"
    "new; inside `Quote:`, `Source:` and `History:` a tag written before draft 10 is an old one, and\n"
    "`record/decisions.md` keeps the old tags in its Kind lines until it is updated.")
assert "Since draft 10" in head
new_row = ("| 10 | 2026-10-12 | 72cc7be, 81c1794, 25f9c5e, b7a7e23 | Written by hand from the projection "
           "of 44df5a7 and his corrections (d5e81e3, e3fa339, 323bda0, 59ea8e9, 01ba854, 660b019, "
           "792ac84): the L reordered in six topics and renumbered L1 to L15 on his marks on the reorder "
           "plan (14ea9f0): five merges, L6 new, L21 dissolved, L3 and L20 absorbed into G1; the "
           "organizers renumbered (G1 theory and model, G2 cost, G3 the demand). `--check` failed "
           "until the record caught up. |\n"
           "| record | 2026-10-12 | this file | Step 1 of `record/plan-principles-draft-11-2026-10-12-execution.md`: "
           "the entries rewritten from draft 10 by `scripts/migrate_record_draft10.py` with the new numbering, the fields of the merged entries "
           "carried into the entry that absorbed them, G4 and the former L20 kept as (History:) paragraphs; "
           "the projection shows the From and Tier lines draft 10 had lost and no longer the \"(was …)\" in "
           "the headings, which the table below carries. |")
head = head.replace(
    "| record | 2026-10-12 | this file | D-2026-10-12-d: the entries below rewritten from draft 9 (120a49a) into fields, the draft marks moved into `History:`, nothing dropped; `docs/principles.md` becomes the projection. |",
    "| record | 2026-10-12 | 72cc7be | D-2026-10-12-d: the entries below rewritten from draft 9 (120a49a) into fields, the draft marks moved into `History:`, nothing dropped; `docs/principles.md` becomes the projection. |\n" + new_row)
assert "Step 1 of" in head

numbering = """
## Numbering

The tags of draft 10 against those of drafts 1 to 9 (his marks on the reorder plan, 14ea9f0).

| Draft 10 | Before | What happened |
|---|---|---|
| G0 | G0 | kept |
| G1 | G2 | theory and model, printed first since draft 8; the former L3 and L20 absorbed |
| G2 | G3 | cost, the second eureka on his note; lift, exact and within moved to L6 |
| G3 | G1 | the demand, printed third |
| retired | G4 | retired in draft 9 (D-2026-10-12-c); its content became L22, now in L14 |
| L1 | L1 | kept |
| L2 | L2 | kept |
| L3 | L4 | renumbered; "from a law" his correction |
| L4 | L8 | renumbered |
| L5 | L16, L21 | merged: equality has levels, with the identity clauses of L21 |
| L6 | new | how laws combine, the lift and the cutoff, from the former G3 |
| L7 | L5, L11, L21 | merged: a law characterizes, verified by one operation; identity is not the law |
| L8 | L15 | renumbered |
| L9 | L9, L18 | merged: a DAG of definitions without effects |
| L10 | L19, L13 | merged: the demand determines the computation and the types produced |
| L11 | L12 | renumbered and shortened |
| L12 | L17 | renumbered; statement in his words |
| L13 | L10 | renumbered; statement in his words |
| L14 | L14, L22, L11 (delegation), L21 (transport) | merged |
| L15 | L6, L7 | merged: the core is minimal and its programs are data |
| absorbed | L3 | into G1 (draft 10) |
| absorbed | L20 | into G1 (draft 9) |
"""

# ---- assemble ----------------------------------------------------------------------------------
def g_entry(g):
    d = d10_entries[g]
    e_text = entry(g, [G_OLD[g]], d, tier=TIER[g])
    if g == "G1":
        extra = " (absorbed L3) " + old_entry_as_text("L3") + " (absorbed L20) " + old_entry_as_text("L20")
        lines = e_text.split("\n")
        hi = next(i for i, l in enumerate(lines) if l.startswith("History:"))
        hist_text = " ".join(l.strip() for l in lines[hi:]).split(":", 1)[1].strip()
        lines = lines[:hi] + [field("History", hist_text + extra)]
        e_text = "\n".join(lines)
    return e_text

def flat(block, drop_heading=True):
    ls = block.splitlines()[1:] if drop_heading else block.splitlines()
    return " ".join(l.strip() for l in ls if l.strip())

pending = {
    "## Terms": [history_para("the Terms of draft 9, before his note of 2026-10-12 on dependences and "
                             "on the carrier coming with its models:", flat(old_terms))],
    "## The organizers": [
        history_para("the introduction of draft 9:", flat(old_org)),
        history_para("G4, retired in draft 9 and no longer projected since draft 10:", old_entry_as_text("G4")),
        history_para("the section \"How the organizers depend on each other\", proposed (D8 of the "
                     "generative plan), projected until draft 9 and dropped from the projection in "
                     "draft 10; in the old numbering:", flat(old_dep)),
    ],
    "## The principles of the language": [
        history_para("the introduction of draft 9:", flat(old_lintro)),
        history_para("the former L20, absorbed into G1 in draft 9 and no longer projected since draft "
                     "10; the clause on specializations and bridges belongs to L13 and modules as "
                     "values to the spec (`03`):", old_entry_as_text("L20")),
    ],
}

out = [head, numbering.rstrip("\n"), ""]
fence = False
current = None
entries_buf = []
def close_fence():
    global fence, entries_buf
    if fence:
        out.append("```")
        out.append("\n\n".join(entries_buf))
        out.append("```")
        out.append("")
        entries_buf = []
        fence = False
def flush_pending():
    global current
    if current in pending:
        for h in pending[current]:
            out.append(h)
            out.append("")
        current = None
for k, p in d10_order:
    if k == "prose":
        close_fence()
        if p.startswith("## "):
            flush_pending()
            current = p.splitlines()[0].strip()
        out.append(p)
        out.append("")
    else:
        tag = p
        fence = True
        if tag.startswith("G"):
            entries_buf.append(g_entry(tag))
        else:
            entries_buf.append(entry(tag, L_OLD[tag], d10_entries[tag], from_text=FROM[tag]))
close_fence()
flush_pending()

text = "\n".join(out).rstrip("\n") + "\n"
(ROOT / "record/principles-language.md").write_text(text, encoding="utf-8")
print("wrote record:", len(text.splitlines()), "lines,", len(text.split()), "words")
