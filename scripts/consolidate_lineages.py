#!/usr/bin/env python3
"""The map of ideas: the lineages grouped into themes, each idea with its state (step A1 of
record/plan/principles/plan-synthesis-2026-10-09.md).

Reads the lineages (`link_ideas.py`'s state) and the timeline, and runs the prompt
`prompts/consolidate_lineages_v1.md`, isolated, in one call: the model sees each lineage's scope,
origin, first appearance, number of rows, statement and up to two quotes, under a short label, and
the language's name and designers (--var); nothing else. It groups the lineages into themes and gives
each idea a state, the classes of `consolidate_ideas_v1` (seedling, latent seed, open tension). The
answer is checked (every lineage once, every theme defined, every state in the three classes) and
asked again with its errors.

Writes `<output-dir>/<date>_consolidate_lineages_v1_<agent>_<model>.json` (inputs by sha256, the
labels, every attempt, the accepted answer) and `.md` (the themes, largest first, each idea with its
state, who said it first and when).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402

VERSION = "consolidate_lineages v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "consolidate_lineages_v1.md"
PLACEHOLDER = "<<<INPUT>>>"
STATES = ("seedling", "latent_seed", "open_tension")


def lines_for(der: dict, labels: dict, quotes: int, quote_chars: int) -> str:
    out = []
    for lab, lid in labels.items():
        d = der[lid]
        out.append(f"{lab} | {d['scope']} | {d['origin']} | {d['first'].get('time_local', '')[:10]} | {d['rows']} | {d['statement']}")
        for m in pc.pick_quotes(d["members"], quotes):
            out.append(f"    - {m.get('who')}: \"{link_ideas.clip(m.get('quote', ''), quote_chars)}\"")
    return "\n".join(out)


def check(ans: dict, labels: dict) -> list[str]:
    if not isinstance(ans, dict):
        return ["the answer is not a JSON object"]
    errs = []
    themes = {t.get("id") for t in ans.get("themes", []) or [] if isinstance(t, dict) and str(t.get("name", "")).strip()}
    if not themes:
        errs.append("no themes")
    seen = Counter()
    for e in ans.get("lineages", []) or []:
        if not (isinstance(e, list) and len(e) == 3):
            errs.append(f"entry {e!r} is not [l<n>, T<n>, state]")
            continue
        lab, t, st = e
        seen[lab] += 1
        if lab not in labels:
            errs.append(f"{lab!r} is not a lineage")
        if t not in themes:
            errs.append(f"{lab}: theme {t!r} is not defined")
        if st not in STATES:
            errs.append(f"{lab}: state {st!r} is not one of {STATES}")
    missing = [l for l in labels if seen[l] == 0]
    if missing:
        errs.append(f"lineages not placed: {len(missing)}, for example {', '.join(missing[:10])}")
    twice = [l for l in labels if seen[l] > 1]
    if twice:
        errs.append(f"lineages placed twice: {', '.join(twice[:10])}")
    return errs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lineages", type=Path, default=REPO_ROOT / "record" / "ideas" / "lineages_link_ideas_v1_claude-code_opus.json")
    ap.add_argument("--timeline", type=Path, default=REPO_ROOT / "record" / "ideas" / "timeline.jsonl")
    ap.add_argument("--output-dir", type=Path, default=REPO_ROOT / "record" / "synthesis")
    ap.add_argument("--quotes", type=int, default=2)
    ap.add_argument("--quote-chars", type=int, default=200)
    ap.add_argument("--date", default=date.today().isoformat())
    pc.common_args(ap, DEFAULT_PROMPT)
    args = ap.parse_args(argv)
    template, left = pc.fill(args.prompt.read_text(encoding="utf-8"), args.var)
    if left:
        print(f"ERROR: the prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
        return 2
    der = link_ideas.derive(json.loads(args.lineages.read_text(encoding="utf-8")),
                            {r["id"]: r for r in link_ideas.load_timeline(args.timeline)})
    labels = pc.labels_for(der)
    prompt_text = template.replace(PLACEHOLDER, lines_for(der, labels, args.quotes, args.quote_chars))
    print(f"lineages: {len(der)} | input: {len(prompt_text):,} chars (~{len(prompt_text) // 4:,} tokens)")
    if args.dry_run:
        return 0
    cli, model, agent = pc.resolve(args)
    stem = f"{args.date}_{args.prompt.stem}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json, out_md = args.output_dir / f"{stem}.json", args.output_dir / f"{stem}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2
    ans, attempts = pc.ask(cli, prompt_text, args, lambda raw: (raw, check(raw, labels)))
    run = {"version": VERSION, "date": args.date, "prompt": args.prompt.stem, "prompt_sha256": pc.sha256_bytes(args.prompt.read_bytes()),
           "vars": args.var, "model": model, "agent": agent, "effort": args.effort, "cli_version": link_ideas.cli_version(cli),
           "inputs": {pc.rel(p): pc.sha256_bytes(p.read_bytes()) for p in (args.lineages, args.timeline)},
           "input_sha256": pc.sha256_bytes(prompt_text.encode()), "labels": labels, "attempts": attempts, "answer": ans}
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if ans is None:
        print(f"no answer passed the checks; the attempts are in {out_json}", file=sys.stderr)
        return 1
    themes = {t["id"]: t for t in ans["themes"]}
    members = defaultdict(list)
    for lab, t, st in ans["lineages"]:
        members[t].append((der[labels[lab]], st))
    states = Counter(st for _, _, st in ans["lineages"])
    L = [f"# The map of ideas about {dict(kv.partition('=')[::2] for kv in args.var).get('language', '?')}, {args.date}", "",
         f"Written by `scripts/consolidate_lineages.py` ({VERSION}); prompt `{args.prompt.stem}` (sha256 {run['prompt_sha256'][:12]}), "
         f"model {model} at effort {args.effort}. The grouping and the states are the model's reading; who said each idea",
         "first and when come from the rows.", "",
         f"{len(der)} ideas in {len(members)} themes: " + ", ".join(f"{s.replace('_', ' ')} {states.get(s, 0)}" for s in STATES) + ".", "",
         "| theme | ideas | seedling | latent seed | open tension |", "|---|---|---|---|---|"]
    order = sorted(members, key=lambda t: -len(members[t]))
    for t in order:
        c = Counter(st for _, st in members[t])
        L.append(f"| {themes[t]['name']} | {len(members[t])} | {c['seedling']} | {c['latent_seed']} | {c['open_tension']} |")
    for t in order:
        L += ["", f"## {themes[t]['name']}", "", themes[t].get("about", ""), ""]
        for d, st in sorted(members[t], key=lambda x: (STATES.index(x[1]), x[0]["first"].get("time_utc", ""))):
            L.append(f"- *{st.replace('_', ' ')}* `{d['id']}`: {d['statement']} ({d['origin']}, {d['first'].get('time_local', '')[:10]}, {d['rows']} rows)")
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out_md}\n{len(members)} themes; " + ", ".join(f"{s} {states.get(s, 0)}" for s in STATES))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
