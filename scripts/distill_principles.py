#!/usr/bin/env python3
"""Distill the lineages of ideas into candidate principles, for Luciano to mark.

Reads the lineages (`link_ideas.py`'s state), the timeline they point into, `record/principles.md`,
`record/decisions.md`, `record/objectives.md` and the ledger computed from the last two by
`principles_ledger.py`, every one pinned by sha256, and runs the prompt
`prompts/distill_principles_v1.md` through the `claude` (or `codex`) command line, isolated: no
tools, no session. One call: the model sees all lineages at once, since a principle compresses
ideas from anywhere in time.

The model classifies every lineage (covered by a principle in force, extends one, candidate, or not
a principle) and drafts at most --max-candidates candidates, each with one quote from its lineages.
Its answer is checked before it is accepted: every lineage classified once, every id known, every
candidate's quote found in its row (words only, an ellipsis standing for skipped words), and that
row a member of one of the candidate's lineages. A rejected answer is asked again with the errors,
up to --retries times. Whose words the quote is, its source, and how often its lineages recur are
filled in here from the rows, never taken from the model.

Writes, under --output-dir (default record/distillation):
  <date>_distill_principles_v1_<agent>_<model>.json   inputs with sha256, the assembled input's
                                                       sha256, every attempt, the accepted answer
  <date>_distill_principles_v1_<agent>_<model>.md     for Luciano: the candidates in the format of
                                                       record/principles.md, each with a Mark: line

Committing the .md, then Luciano's marks on it, is the documented process: what was proposed, from
what, and what he decided. Luciano runs this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402  the lineages are derived the same way the linking script reports them
import principles_ledger as pl  # noqa: E402  one reading of the record files

VERSION = "distill_principles v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_ID = "distill_principles_v1"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / f"{PROMPT_ID}.md"
DEFAULT_LINEAGES = REPO_ROOT / "record" / "ideas" / "lineages_link_ideas_v1_claude-code_opus.json"
DEFAULT_TIMELINE = REPO_ROOT / "record" / "ideas" / "timeline.jsonl"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "distillation"
DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5"
DEFAULT_EFFORT = "low"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
PLACEHOLDER = "<<<INPUT>>>"
VERDICTS = ("covered", "extends", "candidate", "considered", "not_principle")
AXES = ("aesthetic", "ethical", "emotive", "conceptual")
CONSUMERS = ("reader", "computation")
HARMED = ("reader", "computation", "writer")
CONSUMER_NAMES = {"reader": "the person who uses and reads it", "computation": "the computation",
                  "writer": "the model that writes it"}
SCOPES = ("language", "method")
ELLIPSIS_RE = re.compile(r"\s*(?:\.\.\.|…|\[\.\.\.\]|\[…\])\s*")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--lineages", type=Path, default=DEFAULT_LINEAGES)
    p.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    p.add_argument("--principles", type=Path, default=pl.DEFAULT_PRINCIPLES)
    p.add_argument("--decisions", type=Path, default=pl.DEFAULT_DECISIONS)
    p.add_argument("--objectives", type=Path, default=REPO_ROOT / "record" / "objectives.md")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto")
    p.add_argument("--model", default=None)
    p.add_argument("--agent", default=None)
    p.add_argument("--effort", choices=EFFORTS, default=DEFAULT_EFFORT, help="passed to claude; codex ignores it")
    p.add_argument("--max-candidates", type=int, default=7, help="the most candidates one run may propose (P12)")
    p.add_argument("--quotes-per-lineage", type=int, default=4)
    p.add_argument("--quote-chars", type=int, default=300)
    p.add_argument("--max-input-chars", type=int, default=700000, help="refuse to send more than this")
    p.add_argument("--retries", type=int, default=2)
    p.add_argument("--timeout", type=float, default=1800.0)
    p.add_argument("--max-output-tokens", type=int, default=0,
                   help="passed to claude as CLAUDE_CODE_MAX_OUTPUT_TOKENS (0: the CLI's default)")
    p.add_argument("--max-thinking-tokens", type=int, default=0,
                   help="passed to claude as MAX_THINKING_TOKENS, a cap on the model's reasoning (0: the CLI's default)")
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--force", action="store_true", help="redo a run of this date that exists")
    p.add_argument("--dry-run", action="store_true", help="assemble and measure the input; call no model")
    p.add_argument("--show-input", type=Path, default=None, help="write the assembled prompt here and stop")
    return p.parse_args(argv)


# --- the input ------------------------------------------------------------------------------------

def pick_quotes(members: list[dict], n: int) -> list[dict]:
    """Deterministic: the first row, the first of Luciano's, corrections and rejections, the last."""
    chosen: list[dict] = []

    def add(m):
        if m is not None and m not in chosen and len(chosen) < n:
            chosen.append(m)
    add(members[0])
    add(next((m for m in members if m.get("who") == "Luciano"), None))
    for m in members:
        if m["relation"] in ("corrects", "rejects"):
            add(m)
    add(members[-1])
    for m in members:
        add(m)
    return sorted(chosen, key=lambda m: (m.get("time_utc", ""), m["id"]))


def lineage_block(d: dict, n_quotes: int, quote_chars: int, label: str, qlabels: dict) -> str:
    head = f"scope: {d['scope']} | origin: {d['origin']} | first seen: {d['first'].get('time_local', '')[:10]}"
    if d["adopted_by_luciano"]:
        head += f" | taken up by Luciano: {d['adopted_by_luciano'].get('time_local', '')[:10]}"
    lines = [f"### {label} {d['id']}", head, f"statement: {d['statement']}", "quotes:"]
    for m in pick_quotes(d["members"], n_quotes):
        q = f"q{len(qlabels) + 1}"
        qlabels[q] = m["id"]
        lines.append(f"- {q} | {m.get('time_local', '')[:16]} | {m.get('who')} | {m['relation']} | "
                     f"\"{link_ideas.clip(m.get('quote', ''), quote_chars)}\"")
    return "\n".join(lines)


def labels_for(der: dict[str, dict]) -> dict[str, str]:
    """l<n> -> lineage id, in order of first appearance."""
    order = sorted(der.values(), key=lambda d: (d["first"].get("time_utc", ""), d["id"]))
    return {f"l{i}": d["id"] for i, d in enumerate(order, 1)}


def assemble(texts: dict[str, str], der: dict[str, dict], n_quotes: int, quote_chars: int,
             qlabels: dict | None = None) -> str:
    """The input; fills qlabels (q<n> -> row id) as the quotes are numbered."""
    qlabels = {} if qlabels is None else qlabels
    llabels = labels_for(der)
    blocks = [f"## Principles in force (record/principles.md)\n\n{texts['principles']}",
              f"## Decision log (record/decisions.md)\n\n{texts['decisions']}",
              f"## Ledger (scripts/principles_ledger.py, computed from the two above)\n\n{texts['ledger']}",
              f"## Objectives (record/objectives.md)\n\n{texts['objectives']}",
              f"## Lineages ({len(der)})\n\n" + "\n\n".join(
                  lineage_block(der[lid], n_quotes, quote_chars, lab, qlabels) for lab, lid in llabels.items())]
    return "\n\n".join(blocks) + "\n"


# --- the checks -----------------------------------------------------------------------------------

def words(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text)).replace("\\n", " ")
    text = "".join(" " if unicodedata.category(c)[0] in "PS" else c for c in text)
    return " ".join(text.casefold().split())


def quote_in(quote: str, source: str) -> bool:
    hay, pos = words(source), 0
    pieces = [words(p) for p in ELLIPSIS_RE.split(quote) if words(p)]
    if not pieces:
        return False
    for piece in pieces:
        i = hay.find(piece, pos)
        if i < 0:
            return False
        pos = i + len(piece)
    return True


def expand(ans: dict, llabels: dict[str, str], qlabels: dict[str, str]) -> tuple[dict, list[str]]:
    """The compact answer (l<n>, q<n>, classification as lists) in the long form, with ids."""
    if not isinstance(ans, dict):
        return ans, ["the answer is not a JSON object"]
    errors, cls = [], []
    lid = lambda x: llabels.get(x, f"?{x}")
    for c in ans.get("classification", []) or []:
        if not (isinstance(c, list) and len(c) in (3, 4)):
            errors.append(f"classification entry {c!r} is not [l<n>, verdict, ref, note]")
            continue
        ref = c[2] or None
        cls.append({"lineage": lid(c[0]), "verdict": c[1], "principle": ref if c[1] in ("covered", "extends") else None,
                    "candidate": ref if c[1] == "candidate" else None, "note": c[3] if len(c) == 4 else ""})
    cands = []
    for c in ans.get("candidates", []) or []:
        c = dict(c)
        c["lineages"] = [lid(x) for x in c.get("lineages", []) or []]
        q = c.pop("quote", None)
        c["quote_row"] = qlabels.get(q, f"?{q}")
        c["quote_label"] = q
        c["quote"] = c.pop("quote_text", "")
        if isinstance(c.get("beats"), dict):
            c["beats"] = {**c["beats"], "lineage": lid(c["beats"].get("lineage"))}
        cands.append(c)
    against = []
    for a in ans.get("against", []) or []:
        a = dict(a)
        a["evidence"] = [llabels.get(e, e) for e in a.get("evidence", []) or []]
        against.append(a)
    return {"classification": cls, "candidates": cands, "against": against}, errors


def check_answer(ans: dict, der: dict, principles: dict, decisions: dict, max_candidates: int) -> list[str]:
    if not isinstance(ans, dict):
        return ["the answer is not a JSON object"]
    errors: list[str] = []
    cands = ans.get("candidates", []) or []
    cand_ids = [str(c.get("id", "")) for c in cands]
    if len(cands) > max_candidates:
        errors.append(f"{len(cands)} candidates; at most {max_candidates}")
    if len(set(cand_ids)) != len(cand_ids):
        errors.append("candidate ids repeat")
    for cid in cand_ids:
        if not re.match(r"^C\d+$", cid):
            errors.append(f"candidate id {cid!r} is not C<n>")
    seen = Counter()
    for c in ans.get("classification", []) or []:
        lid, v = c.get("lineage"), c.get("verdict")
        seen[lid] += 1
        if lid not in der:
            errors.append(f"classification of unknown lineage {lid!r}")
        if v not in VERDICTS:
            errors.append(f"{lid}: verdict {v!r} is not one of {VERDICTS}")
        if v in ("covered", "extends") and c.get("principle") not in principles:
            errors.append(f"{lid}: {v} names principle {c.get('principle')!r}, which is not in force")
        if v == "candidate" and c.get("candidate") not in cand_ids:
            errors.append(f"{lid}: candidate {c.get('candidate')!r} is not among the candidates")
    verdict_of = {c.get("lineage"): c.get("verdict") for c in ans.get("classification", []) or []}
    missing = [l for l in der if seen[l] == 0]
    twice = [l for l in der if seen[l] > 1]
    if missing:
        errors.append(f"lineages not classified: {', '.join(missing[:20])}" + (f" and {len(missing) - 20} more" if len(missing) > 20 else ""))
    if twice:
        errors.append(f"lineages classified more than once: {', '.join(twice[:10])}")
    for c in cands:
        cid = c.get("id")
        if c.get("scope") not in SCOPES:
            errors.append(f"{cid}: scope {c.get('scope')!r} is not one of {SCOPES}")
        lins = c.get("lineages", []) or []
        unknown = [l for l in lins if l not in der]
        if not lins or unknown:
            errors.append(f"{cid}: lineages {unknown or 'none'} unknown or missing")
        rows = {m["id"]: m for l in lins if l in der for m in der[l]["members"]}
        qr = c.get("quote_row")
        if qr not in rows:
            errors.append(f"{cid}: quote_row {qr!r} is not a row of its lineages")
        elif not quote_in(c.get("quote", ""), rows[qr].get("quote", "")):
            errors.append(f"{cid}: the quote is not in row {qr}: \"{str(c.get('quote', ''))[:80]}\"")
        for g in c.get("guides", []) or []:
            if g not in decisions:
                errors.append(f"{cid}: guides {g!r}, which is not in the decision log")
        for k in c.get("conflicts", []) or []:
            if k.get("principle") not in principles:
                errors.append(f"{cid}: conflicts with {k.get('principle')!r}, which is not in force")
        for field in ("statement", "assumption"):
            if not str(c.get(field, "")).strip():
                errors.append(f"{cid}: empty {field}")
        st = c.get("strongest") or {}
        if not isinstance(st, dict) or st.get("consumer") not in CONSUMERS or st.get("axis") not in AXES \
                or not str(st.get("why", "")).strip():
            errors.append(f"{cid}: strongest needs a consumer among {CONSUMERS}, an axis among {AXES} and a why")
        also = c.get("also") or []
        if not isinstance(also, list) or len(also) > 2:
            errors.append(f"{cid}: also is a list of at most 2 pairs")
        for e in also if isinstance(also, list) else []:
            if not isinstance(e, dict) or e.get("consumer") not in CONSUMERS or e.get("axis") not in AXES \
                    or not str(e.get("why", "")).strip():
                errors.append(f"{cid}: each pair of also needs a consumer, an axis and a why")
        harms = c.get("harms")
        if not isinstance(harms, list):
            errors.append(f"{cid}: harms must be a list, empty if you looked and found none")
        for e in harms if isinstance(harms, list) else []:
            if not isinstance(e, dict) or e.get("consumer") not in HARMED or not str(e.get("how", "")).strip():
                errors.append(f"{cid}: each harm needs a consumer among {HARMED} and how")
        b = c.get("beats") or {}
        bl = b.get("lineage") if isinstance(b, dict) else None
        if bl not in der or bl in lins or verdict_of.get(bl) != "considered" or not str(b.get("why", "")).strip():
            errors.append(f"{cid}: beats must name a lineage classified considered, outside the candidate, with a why")
    for c in cands[:-1]:
        if not str(c.get("above_next", "")).strip():
            errors.append(f"{c.get('id')}: above_next is missing; every candidate but the last says why it ranks above the next")
    for a in ans.get("against", []) or []:
        if a.get("principle") not in principles:
            errors.append(f"against: {a.get('principle')!r} is not in force")
        for e in a.get("evidence", []) or []:
            if e not in der and e not in decisions:
                errors.append(f"against {a.get('principle')}: evidence {e!r} is neither a lineage nor a decision")
    return errors


def run_warnings(ans: dict, template: str) -> list[str]:
    """Signs the rubric did not discriminate; printed and shown, not grounds for rejection."""
    out = []
    cands = ans.get("candidates", [])
    if len(cands) > 2:
        if len({c["strongest"]["axis"] for c in cands}) == 1:
            out.append(f"every candidate's strongest axis is {cands[0]['strongest']['axis']}.")
        if len({c["strongest"]["consumer"] for c in cands}) == 1:
            out.append(f"every candidate's strongest consumer is {cands[0]['strongest']['consumer']}.")
        if all(not c.get("harms") for c in cands):
            out.append("no candidate names a harm.")
    table = " ".join(l for l in template.splitlines() if l.startswith("| "))
    tw = words(table).split()
    grams = {" ".join(tw[k:k + 8]) for k in range(len(tw) - 7)}
    for c in cands:
        for e in [c["strongest"], *c.get("also", [])]:
            ww = words(e["why"]).split()
            if any(" ".join(ww[k:k + 8]) in grams for k in range(len(ww) - 7)):
                out.append(f"{c['id']}: a why repeats eight words of the table.")
                break
    return out


# --- the report -----------------------------------------------------------------------------------

def wrap(text: str, width: int = 100, indent: str = "            ") -> str:
    out, line = [], ""
    for w in str(text).split():
        if line and len(line) + 1 + len(w) > width - len(indent):
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    return ("\n" + indent).join(out)


def write_report(md: Path, run: dict, ans: dict, der: dict, principles: dict) -> None:
    cls = ans["classification"]
    by_verdict = Counter(c["verdict"] for c in cls)
    by_principle = defaultdict(lambda: Counter())
    for c in cls:
        if c["verdict"] in ("covered", "extends"):
            by_principle[c["principle"]][c["verdict"]] += 1
    L = [f"# Distillation of the ideas into principles, {run['date']}", "",
         f"Written by `scripts/distill_principles.py` ({VERSION}) for Luciano to mark. Prompt `{PROMPT_ID}` (sha256",
         f"{run['prompt_sha256'][:12]}), model {run['model']} at effort {run['effort']} via {run['agent']} ({run['cli_version']}).",
         "Inputs, each by sha256: " + "; ".join(f"`{k}` {v['sha256'][:12]}" for k, v in run["inputs"].items()) + ".",
         "The candidates are the model's drafts, chosen and ordered by the model's reading of infectability, Luciano's",
         "criterion for finding principles; whether one stays is judged later by P13, from the decisions it guides once",
         "applied (D-2026-10-09-b). Each candidate shows apart what the script took from the rows (the quote, whose words,",
         "the source, how often its lineages recur) and what is the model's reading. Under each, a Mark: line for ok, no,",
         "or a correction.", "",
         *([f"Warnings on the run: " + " ".join(run["warnings"]), ""] if run.get("warnings") else []),
         f"Lineages: {len(der)}. " + ", ".join(f"{v} {by_verdict.get(v, 0)}" for v in VERDICTS) + ".", "",
         "| principle | lineages it covers | lineages that extend it |", "|---|---|---|"]
    for pid in sorted(principles, key=lambda p: int(p[1:])):
        c = by_principle.get(pid, Counter())
        L.append(f"| {pid} {principles[pid]['statement'][:60]} | {c['covered']} | {c['extends']} |")
    L += ["", "## Candidates", "", "```"]
    lin_of = defaultdict(list)
    for c in cls:
        if c["verdict"] == "candidate":
            lin_of[c["candidate"]].append(c["lineage"])
    for c in ans["candidates"]:
        lins = [l for l in c["lineages"] if l in der]
        rows = {m["id"]: m for l in lins for m in der[l]["members"]}
        q = rows.get(c["quote_row"], {})
        first = min((der[l]["first"] for l in lins), key=lambda m: m.get("time_utc", ""))
        origins = Counter(der[l]["origin"] for l in lins)
        pair = lambda e: f"{CONSUMER_NAMES[e['consumer']]}, {e['axis']}. {e['why']}"
        L += [f"{c['id']}  {wrap(c['statement'], indent='    ')}",
              f"Scope:      {c['scope']}",
              "-- from the rows, by the script",
              f"Quote:      \"{wrap(c['quote'])}\"",
              f"Said by:    {q.get('who', '?')}, {q.get('time_local', '')[:16]}",
              f"Source:     {wrap(q.get('source', ''))} (row {c['quote_row']})",
              f"Lineages:   {wrap(', '.join(lins))}",
              f"Witnesses:  first {first.get('time_local', '')[:10]} by {first.get('who', '?')}; "
              f"{sum(der[l]['witnesses'] for l in lins)} witnesses over {len({m.get('time_local', '')[:10] for l in lins for m in der[l]['members']})} days; "
              f"lineages begun by " + ", ".join(f"{o} {n}" for o, n in origins.items()),
              f"-- the model's reading ({run['model']}, effort {run['effort']})",
              f"Strongest:  {wrap(pair(c['strongest']))}",
              *[f"Also:       {wrap(pair(e))}" for e in c.get("also", [])],
              *([f"Harms:      {wrap(CONSUMER_NAMES[e['consumer']] + '. ' + e['how'])}" for e in c["harms"]]
                or ["Harms:      none found"]),
              f"Beats:      {wrap(c['beats']['lineage'] + ' (' + der[c['beats']['lineage']]['statement'] + '). ' + c['beats']['why'])}",
              *([f"Above next: {wrap(c['above_next'])}"] if c.get("above_next") else []),
              f"Assumption: {wrap(c['assumption'])}",
              f"Would have guided (for P13, later): {', '.join(c.get('guides', [])) or 'no decision in the log'}",
              f"Conflicts:  {wrap('; '.join(k['principle'] + ': ' + k['how'] for k in c.get('conflicts', [])) or 'none named')}",
              "Status:     proposed by distill_principles_v1, for Luciano to mark",
              "Mark:       ", ""]
    L += ["```", "", "## Ideas that extend a principle in force", ""]
    ext = [c for c in cls if c["verdict"] == "extends"]
    for pid in sorted({c["principle"] for c in ext}, key=lambda p: int(p[1:])):
        L.append(f"- **{pid}**")
        for c in ext:
            if c["principle"] == pid:
                d = der[c["lineage"]]
                L.append(f"  - `{d['id']}` ({d['origin']}, {d['rows']} rows): {d['statement']} *{c.get('note', '')}*")
    if not ext:
        L.append("none")
    L += ["", "## Considered and left out", ""]
    cons = [c for c in cls if c["verdict"] == "considered"]
    for c in cons:
        d = der[c["lineage"]]
        L.append(f"- `{d['id']}` ({d['origin']}, {d['rows']} rows): {d['statement']} *{c.get('note', '')}*")
    if not cons:
        L.append("none")
    L += ["", "## Principles in force the ideas argue against", ""]
    for a in ans.get("against", []) or []:
        L.append(f"- **{a['principle']}**: {a['why']} Evidence: {', '.join(a.get('evidence', []))}")
    if not ans.get("against"):
        L.append("none")
    L += ["", "## Every lineage and its classification", "", "| lineage | scope | origin | rows | verdict | note |", "|---|---|---|---|---|---|"]
    for c in sorted(cls, key=lambda c: (VERDICTS.index(c["verdict"]), c["lineage"])):
        d = der[c["lineage"]]
        tag = c.get("principle") or c.get("candidate") or ""
        L.append(f"| `{d['id']}` | {d['scope']} | {d['origin']} | {d['rows']} | {c['verdict']} {tag} | {str(c.get('note', '')).replace('|', '/')} |")
    md.write_text("\n".join(L) + "\n", encoding="utf-8")


# --- main -----------------------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    paths = {"lineages": args.lineages, "timeline": args.timeline, "principles": args.principles,
             "decisions": args.decisions, "objectives": args.objectives, "prompt": args.prompt}
    for k, p in paths.items():
        if not p.is_file():
            print(f"ERROR: {k} not found: {p}", file=sys.stderr)
            return 2
    template = args.prompt.read_text(encoding="utf-8").replace("{max_candidates}", str(args.max_candidates))
    if PLACEHOLDER not in template:
        print(f"ERROR: the prompt has no {PLACEHOLDER}", file=sys.stderr)
        return 2

    state = json.loads(args.lineages.read_text(encoding="utf-8"))
    rows = link_ideas.load_timeline(args.timeline)
    by_id = {r["id"]: r for r in rows}
    der = link_ideas.derive(state, by_id)
    if not der:
        print("ERROR: no lineages", file=sys.stderr)
        return 2
    principles = pl.parse_entries(args.principles.read_text(encoding="utf-8"), pl.P_HEAD_RE)
    decisions = pl.parse_entries(args.decisions.read_text(encoding="utf-8"), pl.D_HEAD_RE)
    in_force = pl.claude_list(pl.DEFAULT_CLAUDE_MD.read_text(encoding="utf-8")) if pl.DEFAULT_CLAUDE_MD.is_file() else {}
    ledger_text, _ = pl.ledger(principles, decisions, in_force, None, args.date)
    texts = {"principles": args.principles.read_text(encoding="utf-8"), "decisions": args.decisions.read_text(encoding="utf-8"),
             "objectives": args.objectives.read_text(encoding="utf-8"), "ledger": ledger_text}
    qlabels: dict[str, str] = {}
    body = assemble(texts, der, args.quotes_per_lineage, args.quote_chars, qlabels)
    llabels = labels_for(der)
    prompt_text = template.replace(PLACEHOLDER, body)
    pending = sum(1 for r in rows if r["id"] not in state["assign"] and r["id"] not in state["unplaced"])
    print(f"lineages: {len(der)} | timeline rows not yet in a lineage: {pending} | input: {len(prompt_text):,} chars "
          f"(~{len(prompt_text) // 4:,} tokens) | max candidates: {args.max_candidates}")
    if pending:
        print(f"  note: {pending} rows of the timeline are not placed yet; run link_ideas.py first to include them", file=sys.stderr)
    if args.show_input:
        args.show_input.write_text(prompt_text, encoding="utf-8")
        print(f"written: {args.show_input}")
        return 0
    if len(prompt_text) > args.max_input_chars:
        print(f"ERROR: the input is {len(prompt_text):,} chars, over --max-input-chars {args.max_input_chars:,}", file=sys.stderr)
        return 2
    if args.dry_run:
        return 0

    try:
        cli = link_ideas.resolve_cli(args.cli)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    model = args.model or (DEFAULT_CODEX_MODEL if cli == "codex" else DEFAULT_CLAUDE_MODEL)
    agent = args.agent or ("codex" if cli == "codex" else "claude-code")
    tag = f"{args.date}_{PROMPT_ID}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json, out_md = args.output_dir / f"{tag}.json", args.output_dir / f"{tag}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2

    def rel(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(REPO_ROOT))
        except ValueError:
            return str(p)
    run = {"version": VERSION, "date": args.date, "prompt": PROMPT_ID, "prompt_sha256": sha256_bytes(args.prompt.read_bytes()),
           "model": model, "agent": agent, "effort": args.effort, "cli_version": link_ideas.cli_version(cli),
           "max_candidates": args.max_candidates, "max_thinking_tokens": args.max_thinking_tokens, "quotes_per_lineage": args.quotes_per_lineage, "quote_chars": args.quote_chars,
           "inputs": {rel(p): {"sha256": sha256_bytes(p.read_bytes())} for k, p in paths.items() if k != "prompt"},
           "ledger_sha256": sha256_bytes(ledger_text.encode()), "input_sha256": sha256_bytes(prompt_text.encode()),
           "lineage_labels": llabels, "quote_labels": qlabels,
           "lineages": len(der), "attempts": [], "answer": None}
    text, ans = prompt_text, None
    for attempt in range(args.retries + 1):
        t0 = time.time()
        try:
            raw = link_ideas.call(cli, text, model, args.effort, args.timeout, args.max_output_tokens, args.max_thinking_tokens)
        except link_ideas.OutputLimit as exc:
            run["attempts"].append({"error": f"output limit: {exc}", "seconds": round(time.time() - t0)})
            print("the answer hit the output token limit; raise it with --max-output-tokens", file=sys.stderr)
            break
        except Exception as exc:
            run["attempts"].append({"error": str(exc)[:500], "seconds": round(time.time() - t0)})
            print(f"call failed: {str(exc)[:200]}", file=sys.stderr)
            continue
        try:
            cand, errors = expand(link_ideas.parse_json(raw), llabels, qlabels)
            errors = errors + check_answer(cand, der, principles, decisions, args.max_candidates)
        except (ValueError, json.JSONDecodeError) as exc:
            cand, errors = None, [f"not valid JSON: {exc}"]
        run["attempts"].append({"answer": raw, "answer_sha256": sha256_bytes(raw.encode()), "errors": errors,
                                "seconds": round(time.time() - t0),
                                "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
        if not errors:
            ans = cand
            break
        print(f"answer rejected ({len(errors)} errors): {errors[0][:160]}\nthe answer began: {raw.strip()[:200]!r}", file=sys.stderr)
        text = (prompt_text + "\n\n## Your previous answer was rejected\n\n" + "\n".join(f"- {e}" for e in errors)
                + "\n\nAnswer again, the whole JSON object.\n")
    run["answer"] = ans
    run["warnings"] = run_warnings(ans, template) if ans else []
    for w in run["warnings"]:
        print(f"warning: {w}", file=sys.stderr)
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if ans is None:
        print(f"no answer passed the checks after {len(run['attempts'])} attempts; the attempts are in {out_json}", file=sys.stderr)
        return 1
    write_report(out_md, run, ans, der, principles)
    print(f"written: {out_json}\n         {out_md}")
    print(f"candidates: {len(ans['candidates'])}; " + ", ".join(f"{v} {sum(c['verdict'] == v for c in ans['classification'])}" for v in VERDICTS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
