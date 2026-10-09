#!/usr/bin/env python3
"""The synthesis of Luthier's ideas, rules and principles, in one document for Luciano (step A4 of
record/plan-synthesis-2026-10-09.md). Mechanical, no model.

Reads the outputs of the night, each by path: the map of themes (`consolidate_lineages.py`), the
candidates found blind (`find_principles.py`) and their match against the principles in force
(`match_principles.py`, optional), the rules traced to the ideas (`trace_rules.py`), and the lineages
and timeline they all read. Writes `record/synthesis/<date>_synthesis.md`: a one-screen summary, then
the three parts, each pointing to its full file. Every input is listed with its sha256.
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

VERSION = "assemble_synthesis v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
STATES = ("seedling", "latent_seed", "open_tension")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--themes", type=Path, required=True)
    ap.add_argument("--found", type=Path, required=True)
    ap.add_argument("--match", type=Path, default=None)
    ap.add_argument("--rules", type=Path, required=True)
    ap.add_argument("--lineages", type=Path, default=REPO_ROOT / "record" / "ideas" / "lineages_link_ideas_v1_claude-code_opus.json")
    ap.add_argument("--timeline", type=Path, default=REPO_ROOT / "record" / "ideas" / "timeline.jsonl")
    ap.add_argument("--output-dir", type=Path, default=REPO_ROOT / "record" / "synthesis")
    ap.add_argument("--seeds-per-theme", type=int, default=5,
                    help="latent seeds listed per theme, those first said by Luciano, earliest first; the rest are in the full map")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args(argv)

    der = link_ideas.derive(json.loads(args.lineages.read_text(encoding="utf-8")),
                            {r["id"]: r for r in link_ideas.load_timeline(args.timeline)})
    th = json.loads(args.themes.read_text(encoding="utf-8"))
    fo = json.loads(args.found.read_text(encoding="utf-8"))
    ma = json.loads(args.match.read_text(encoding="utf-8")) if args.match else None
    ru = json.loads(args.rules.read_text(encoding="utf-8"))
    tl, fl = th["labels"], fo["lineage_labels"]
    themes = {t["id"]: t for t in th["answer"]["themes"]}
    members = defaultdict(list)
    for lab, t, st in th["answer"]["lineages"]:
        if tl[lab] in der:
            members[t].append((der[tl[lab]], st))
    states = Counter(st for _, _, st in th["answer"]["lineages"])
    cands = fo["answer"]["candidates"]
    match = {m["candidate"]: m for m in (ma["answer"]["matches"] if ma else [])}
    rules, trace = ru["rules"], {rid: labs for rid, labs in ru["answer"]["traces"]}
    untraced = [r for r in rules if not trace.get(r["id"])]
    order = sorted(members, key=lambda t: -len(members[t]))
    inputs = [args.themes, args.found, args.rules, args.lineages, args.timeline] + ([args.match] if args.match else [])

    L = [f"# Synthesis of Luthier's ideas, rules and principles, {args.date}", "",
         f"Written by `scripts/assemble_synthesis.py` ({VERSION}) for Luciano, from the night's outputs (plan:",
         "`record/plan-synthesis-2026-10-09.md`). Every grouping, state, candidate and trace is a model's reading; who said each",
         "idea and when comes from the rows. Nothing here is decided: the candidates have a `Mark:` line for you.", "",
         "## Summary", "",
         f"- **Ideas.** {len(der)} ideas in {len(members)} themes; " + ", ".join(f"{states.get(s, 0)} {s.replace('_', ' ')}" for s in STATES)
         + ". Largest themes: " + "; ".join(f"{themes[t]['name']} ({len(members[t])})" for t in order[:6]) + ".",
         f"- **Principles.** {len(cands)} candidates found blind from the ideas" + (
             ": " + ", ".join(f"{v} {sum(1 for m in match.values() if m['verdict'] == v)}" for v in ("new", "extends", "covered"))
             + " against P1 to P14." if match else "."),
         f"- **Rules.** {len(rules)} rules ({sum(r['kind'] == 'spec' for r in rules)} of the specification, "
         f"{sum(r['kind'] == 'decision' for r in rules)} decisions); {len(rules) - len(untraced)} come from at least one idea, "
         f"{len(untraced)} from none.", "",
         "## 1. The ideas, by theme", "",
         f"The full map, every idea with its state: `{pc.rel(args.themes).replace('.json', '.md')}`. Here each theme with its size;",
         f"under it every open tension, and at most {args.seeds_per_theme} latent seeds, those you said first, earliest first.", "",
         "| theme | ideas | seedling | latent seed | open tension |", "|---|---|---|---|---|"]
    for t in order:
        c = Counter(st for _, st in members[t])
        L.append(f"| {themes[t]['name']} | {len(members[t])} | {c['seedling']} | {c['latent_seed']} | {c['open_tension']} |")
    for t in order:
        tensions = sorted((d for d, st in members[t] if st == "open_tension"), key=lambda d: d["first"].get("time_utc", ""))
        seeds = sorted((d for d, st in members[t] if st == "latent_seed"), key=lambda d: d["first"].get("time_utc", ""))
        his = [d for d in seeds if d["origin"] == "Luciano"]
        L += ["", f"### {themes[t]['name']}", "", themes[t].get("about", ""), ""]
        for d in tensions:
            L.append(f"- *open tension*: {d['statement']} ({d['origin']}, {d['first'].get('time_local', '')[:10]}, `{d['id']}`)")
        for d in his[:args.seeds_per_theme]:
            L.append(f"- *latent seed*: {d['statement']} ({d['first'].get('time_local', '')[:10]}, `{d['id']}`)")
        rest = len(seeds) - min(len(his), args.seeds_per_theme)
        if rest:
            L.append(f"- and {rest} more latent seeds in the full map" + (f" ({len(seeds) - len(his)} first said by a model)" if len(seeds) > len(his) else ""))
    L += ["", "## 2. The candidate principles", "",
          f"Found blind by `{fo['prompt']}` (it saw only the ideas and your criterion of infectability)"
          + (f", set against P1 to P14 by `{ma['prompt']}`" if ma else "") + ". Full detail: `"
          + pc.rel(args.match or args.found).replace(".json", ".md") + "`.", "", "```"]
    for c in cands:
        lins = [l for l in c["lineages"] if l in der]
        rows = {m["id"]: m for l in lins for m in der[l]["members"]}
        q = rows.get(c["quote_row"], {})
        m = match.get(c["id"], {})
        L += [f"{c['id']}  {pc.wrap(c['statement'], indent='    ')}",
              *([f"Instead of: {pc.wrap(c['instead_of'])}"] if c.get("instead_of") else []),
              f"Quote:      \"{pc.wrap(q.get('quote', c['quote']))}\"",
              f"Said by:    {q.get('who', '?')}, {q.get('time_local', '')[:16]}",
              f"Strongest:  {pc.wrap(c['strongest']['axis'] + '. ' + c['strongest']['why'])}",
              *([f"In force:   {m['verdict']}" + (f" {m['principle']}" if m.get("principle") else "")
                 + (f": {m['change']}" if m.get("change") else "")] if m else []),
              "Mark:       ", ""]
    L += ["```", "", "## 3. The rules and the ideas behind them", "",
          f"Full detail: `{pc.rel(args.rules).replace('.json', '.md')}`.", "",
          "| source | rules | from at least one idea | from none |", "|---|---|---|---|"]
    by_src = defaultdict(list)
    for r in rules:
        by_src[r["source"].split(":")[0]].append(r)
    for src, rs in sorted(by_src.items()):
        n = sum(1 for r in rs if trace.get(r["id"]))
        L.append(f"| `{src}` | {len(rs)} | {n} | {len(rs) - n} |")
    L += ["", "Rules with no idea behind them (written in the specification or decided in the log without a trace in your ideas):", ""]
    L += [f"- **{r['id']}** {r['title']}" for r in untraced] or ["none"]
    L += ["", "## Inputs", ""] + [f"- `{pc.rel(p)}` sha256 {pc.sha256_bytes(p.read_bytes())[:12]}" for p in inputs]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / f"{args.date}_synthesis.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
