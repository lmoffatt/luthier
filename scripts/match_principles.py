#!/usr/bin/env python3
"""Set the candidates found blind (find_principles.py) against what Luthier already has, and write
the document Luciano marks: the second of the two steps that replace the single distillation.

Reads a find_principles output, the lineages and timeline it was made from, `record/principles.md`,
`record/decisions.md`, `record/objectives.md` and the ledger computed from the log by
`principles_ledger.py`, all pinned by sha256, and runs `prompts/match_principles_v1.md`, isolated,
in one call. For each candidate the model says whether it is new, covered by a principle in force or
extends one, what it assumes, which decisions it would have guided (P13's first evidence) and what
it pulls against; then which principles in force the candidates argue against. The answer is
checked (every candidate once, every principle and decision id known) and asked again with its
errors.

Writes `<output-dir>/<date>_match_principles_v1_<agent>_<model>.json` and `.md`: each candidate in
the format of record/principles.md, with the blind step's reading, this step's, and a Mark: line.
Luciano runs it, reads it, marks it; his marks are committed verbatim.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402
import principles_ledger as pl  # noqa: E402

VERSION = "match_principles v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "match_principles_v1.md"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "distillation"
PLACEHOLDER = "<<<INPUT>>>"
VERDICTS = ("new", "covered", "extends")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--found", type=Path, required=True, help="a find_principles output (.json)")
    p.add_argument("--lineages", type=Path, default=None, help="default: the one the found run read")
    p.add_argument("--timeline", type=Path, default=None, help="default: the one the found run read")
    p.add_argument("--principles", type=Path, default=pl.DEFAULT_PRINCIPLES)
    p.add_argument("--decisions", type=Path, default=pl.DEFAULT_DECISIONS)
    p.add_argument("--objectives", type=Path, default=REPO_ROOT / "record" / "objectives.md")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--date", default=date.today().isoformat())
    pc.common_args(p, DEFAULT_PROMPT)
    return p.parse_args(argv)


def check(ans: dict, cands: dict, principles: dict, decisions: dict) -> list[str]:
    if not isinstance(ans, dict):
        return ["the answer is not a JSON object"]
    errors, seen = [], Counter()
    for m in ans.get("matches", []) or []:
        cid = m.get("candidate")
        seen[cid] += 1
        if cid not in cands:
            errors.append(f"unknown candidate {cid!r}")
        if m.get("verdict") not in VERDICTS:
            errors.append(f"{cid}: verdict {m.get('verdict')!r} is not one of {VERDICTS}")
        if m.get("verdict") in ("covered", "extends") and m.get("principle") not in principles:
            errors.append(f"{cid}: {m.get('verdict')} names {m.get('principle')!r}, which is not in force")
        if m.get("verdict") == "extends" and not str(m.get("change", "")).strip():
            errors.append(f"{cid}: extends without a change")
        if not str(m.get("assumption", "")).strip():
            errors.append(f"{cid}: empty assumption")
        for g in m.get("guides", []) or []:
            if g not in decisions:
                errors.append(f"{cid}: guides {g!r}, which is not in the log")
        for k in m.get("conflicts", []) or []:
            if not isinstance(k, dict) or k.get("principle") not in principles:
                errors.append(f"{cid}: conflicts with {k!r}, not a principle in force")
    for c in cands:
        if seen[c] != 1:
            errors.append(f"{c}: matched {seen[c]} times, not once")
    for a in ans.get("against", []) or []:
        if a.get("principle") not in principles:
            errors.append(f"against: {a.get('principle')!r} is not in force")
        for e in a.get("evidence", []) or []:
            if e not in cands and e not in decisions:
                errors.append(f"against {a.get('principle')}: evidence {e!r} is neither a candidate nor a decision")
    return errors


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    found = json.loads(args.found.read_text(encoding="utf-8"))
    if not found.get("answer"):
        print("ERROR: the found run has no accepted answer", file=sys.stderr)
        return 2
    paths = list(found["inputs"])
    lin_path = args.lineages or REPO_ROOT / next(p for p in paths if p.endswith(".json"))
    tl_path = args.timeline or REPO_ROOT / next(p for p in paths if p.endswith(".jsonl"))
    der = link_ideas.derive(json.loads(Path(lin_path).read_text(encoding="utf-8")),
                            {r["id"]: r for r in link_ideas.load_timeline(Path(tl_path))})
    cands = {c["id"]: c for c in found["answer"]["candidates"]}
    principles = pl.parse_entries(args.principles.read_text(encoding="utf-8"), pl.P_HEAD_RE)
    decisions = pl.parse_entries(args.decisions.read_text(encoding="utf-8"), pl.D_HEAD_RE)
    in_force = pl.claude_list(pl.DEFAULT_CLAUDE_MD.read_text(encoding="utf-8")) if pl.DEFAULT_CLAUDE_MD.is_file() else {}
    ledger_text, _ = pl.ledger(principles, decisions, in_force, None, args.date)
    cand_text = "\n\n".join(
        f"### {cid}\nstatement: {c['statement']}\nscope: {c['scope']}\nquote: \"{c['quote']}\"\nlineages:\n"
        + "\n".join(f"- {der[l]['statement']}" for l in c["lineages"] if l in der) for cid, c in cands.items())
    body = "\n\n".join([f"## Candidates\n\n{cand_text}",
                        f"## Principles in force (record/principles.md)\n\n{args.principles.read_text(encoding='utf-8')}",
                        f"## Decision log (record/decisions.md)\n\n{args.decisions.read_text(encoding='utf-8')}",
                        f"## Ledger\n\n{ledger_text}",
                        f"## Objectives (record/objectives.md)\n\n{args.objectives.read_text(encoding='utf-8')}"])
    prompt_text = args.prompt.read_text(encoding="utf-8").replace(PLACEHOLDER, body)
    print(f"candidates: {len(cands)} | input: {len(prompt_text):,} chars")
    if args.show_input:
        args.show_input.write_text(prompt_text, encoding="utf-8")
        return 0
    if args.dry_run:
        return 0
    try:
        cli, model, agent = pc.resolve(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    stem = f"{args.date}_{args.prompt.stem}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json, out_md = args.output_dir / f"{stem}.json", args.output_dir / f"{stem}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2
    run = {"version": VERSION, "date": args.date, "prompt": args.prompt.stem,
           "prompt_sha256": pc.sha256_bytes(args.prompt.read_bytes()), "model": model, "agent": agent,
           "effort": args.effort, "cli_version": link_ideas.cli_version(cli),
           "inputs": {pc.rel(p): {"sha256": pc.sha256_bytes(Path(p).read_bytes())}
                      for p in (args.found, lin_path, tl_path, args.principles, args.decisions, args.objectives)},
           "ledger_sha256": pc.sha256_bytes(ledger_text.encode()), "input_sha256": pc.sha256_bytes(prompt_text.encode())}
    ans, run["attempts"] = pc.ask(cli, prompt_text, args, lambda raw: (raw, check(raw, cands, principles, decisions)))
    run["answer"] = ans
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if ans is None:
        print(f"no answer passed the checks; the attempts are in {out_json}", file=sys.stderr)
        return 1
    match = {m["candidate"]: m for m in ans["matches"]}
    L = [f"# Candidate principles of Luthier, {args.date}", "",
         f"Written by `scripts/match_principles.py` ({VERSION}) for Luciano to mark. Two steps, each a model's reading:",
         f"the candidates were found blind by `{found['prompt']}` (sha256 {found['prompt_sha256'][:12]}, {found['model']}, effort",
         f"{found['effort']}; it saw only the lineages and the criterion of infectability), then set against the principles in",
         f"force, the log and the objectives by `{run['prompt']}` (sha256 {run['prompt_sha256'][:12]}, {model}, effort {args.effort}).",
         "Whose words each quote is and its source were filled in from the rows by the scripts. Under each candidate, a",
         "Mark: line for ok, no, or a correction.", "", "```"]
    for cid, c in cands.items():
        m = match[cid]
        lins = [l for l in c["lineages"] if l in der]
        rows = {r["id"]: r for l in lins for r in der[l]["members"]}
        q = rows.get(c["quote_row"], {})
        L += [f"{cid}  {pc.wrap(c['statement'], indent='    ')}",
              f"Scope:      {c['scope']}",
              f"Quote:      \"{pc.wrap(q.get('quote', c['quote']))}\"",
              f"Said by:    {q.get('who', '?')}, {q.get('time_local', '')[:16]}",
              f"Source:     {pc.wrap(q.get('source', ''))} (row {c['quote_row']})",
              f"Found:      {pc.wrap(c['strongest']['axis'] + '. ' + c['strongest']['why'])}",
              *([f"Harms:      {pc.wrap(h)}" for h in c.get("harms", [])] or ["Harms:      none found"]),
              f"Against:    {m['verdict']}" + (f" {m['principle']}" if m.get("principle") else "")
              + (f": {m['change']}" if m.get("change") else ""),
              f"Assumption: {pc.wrap(m['assumption'])}",
              f"Would have guided (for P13, later): {', '.join(m.get('guides', [])) or 'no decision in the log'}",
              f"Conflicts:  {pc.wrap('; '.join(k['principle'] + ': ' + k['how'] for k in m.get('conflicts', [])) or 'none named')}",
              "Status:     proposed, for Luciano to mark",
              "Mark:       ", ""]
    L += ["```", "", "## Principles in force the candidates argue against", ""]
    L += [f"- **{a['principle']}**: {a['why']} Evidence: {', '.join(a.get('evidence', []))}" for a in ans.get("against", [])] or ["none"]
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out_json}\n         {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
