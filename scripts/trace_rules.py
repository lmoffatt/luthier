#!/usr/bin/env python3
"""The rules of Luthier and the ideas they come from (step A3 of record/plan/principles/plan-synthesis-2026-10-09.md).

Mechanical part: the rules are the bold-numbered statements of the specification (`**R1. ...**` in
05, `**G1. ...**` and `**C1. ...**` in 08), the numbered sections of the documents that have no such
identifiers (02, 03, 04, 06; notation, example and open sections left out), and the entries of
`record/decisions.md`. Model part, prompt `prompts/trace_rules_v1.md`, one isolated call: for each
rule, at most five lineages that state or motivate it, or none. The answer is checked (every rule
once, every label a lineage) and asked again with its errors.

Writes `<output-dir>/<date>_trace_rules_v1_<agent>_<model>.json` (the rules with their sources,
inputs by sha256, attempts, answer) and `.md` (each rule with its ideas, and the rules with none).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402
import principles_ledger as pl  # noqa: E402

VERSION = "trace_rules v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "trace_rules_v1.md"
PLACEHOLDER = "<<<INPUT>>>"
BOLD = re.compile(r"^\*\*([A-Z]{1,2}\d+[a-z]?)\. (.+?)\*\*(.*)$")
SECTION = re.compile(r"^## (\d+)\. (.+)$")
SKIP = re.compile(r"notation|open|example|added|done", re.I)


def spec_rules(spec_dir: Path, body_chars: int) -> list[dict]:
    rules = []
    for f in sorted(spec_dir.glob("*.md")):
        lines = f.read_text(encoding="utf-8").splitlines()
        doc = f.stem.split("-")[0]
        bold = [(i, m) for i, l in enumerate(lines) if (m := BOLD.match(l))]
        if bold:
            for k, (i, m) in enumerate(bold):
                end = bold[k + 1][0] if k + 1 < len(bold) else min(len(lines), i + 15)
                body = " ".join(l.strip() for l in lines[i:end] if not l.startswith("#"))
                rules.append({"id": m.group(1), "kind": "spec", "source": f"{pc.rel(f)}:{i + 1}",
                              "title": m.group(2).strip(), "text": body[:body_chars]})
        else:
            secs = [(i, m) for i, l in enumerate(lines) if (m := SECTION.match(l))]
            for k, (i, m) in enumerate(secs):
                if SKIP.search(m.group(2)):
                    continue
                end = secs[k + 1][0] if k + 1 < len(secs) else len(lines)
                body = " ".join(l.strip() for l in lines[i + 1:end] if l.strip())
                rules.append({"id": f"S{doc}.{m.group(1)}", "kind": "spec", "source": f"{pc.rel(f)}:{i + 1}",
                              "title": m.group(2).strip(), "text": body[:body_chars]})
    return rules


def decision_rules(decisions: Path) -> list[dict]:
    out = []
    for did, e in pl.parse_entries(decisions.read_text(encoding="utf-8"), pl.D_HEAD_RE).items():
        out.append({"id": did, "kind": "decision", "source": pc.rel(decisions), "title": e["statement"][:160],
                    "text": e["statement"]})
    return out


def check(ans, rule_ids: list[str], labels: dict, most: int) -> list[str]:
    if not isinstance(ans, dict) or not isinstance(ans.get("traces"), list):
        return ["traces must be a list"]
    errs, seen = [], {}
    for t in ans["traces"]:
        if not (isinstance(t, list) and len(t) == 2 and isinstance(t[1], list)):
            errs.append(f"entry {t!r} is not [rule id, [l<n>, ...]]")
            continue
        rid, labs = t
        if rid not in rule_ids:
            errs.append(f"{rid!r} is not a rule")
        if rid in seen:
            errs.append(f"{rid} traced twice")
        seen[rid] = labs
        bad = [l for l in labs if l not in labels]
        if bad:
            errs.append(f"{rid}: {bad[:5]} are not lineages")
        if len(labs) > most:
            errs.append(f"{rid}: more than {most} lineages")
    missing = [r for r in rule_ids if r not in seen]
    if missing:
        errs.append(f"rules not traced: {', '.join(missing[:15])}")
    return errs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", type=Path, default=REPO_ROOT / "docs" / "spec")
    ap.add_argument("--decisions", type=Path, default=pl.DEFAULT_DECISIONS)
    ap.add_argument("--lineages", type=Path, default=REPO_ROOT / "record" / "ideas" / "lineages_link_ideas_v1_claude-code_opus.json")
    ap.add_argument("--timeline", type=Path, default=REPO_ROOT / "record" / "ideas" / "timeline.jsonl")
    ap.add_argument("--output-dir", type=Path, default=REPO_ROOT / "record" / "synthesis")
    ap.add_argument("--body-chars", type=int, default=500)
    ap.add_argument("--most", type=int, default=5)
    ap.add_argument("--date", default=date.today().isoformat())
    pc.common_args(ap, DEFAULT_PROMPT)
    args = ap.parse_args(argv)
    template, left = pc.fill(args.prompt.read_text(encoding="utf-8"), args.var)
    if left:
        print(f"ERROR: the prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
        return 2
    rules = spec_rules(args.spec, args.body_chars) + decision_rules(args.decisions)
    der = link_ideas.derive(json.loads(args.lineages.read_text(encoding="utf-8")),
                            {r["id"]: r for r in link_ideas.load_timeline(args.timeline)})
    labels = pc.labels_for(der)
    body = ("## The rules\n\n" + "\n".join(f"- {r['id']} ({r['kind']}): {r['title']}: {r['text']}" for r in rules)
            + "\n\n## The lineages\n\n" + "\n".join(f"- {lab}: {der[lid]['statement']}" for lab, lid in labels.items()))
    prompt_text = template.replace(PLACEHOLDER, body)
    print(f"rules: {len(rules)} ({sum(r['kind'] == 'spec' for r in rules)} of the specification) | lineages: {len(der)} | "
          f"input: {len(prompt_text):,} chars")
    if args.dry_run:
        return 0
    cli, model, agent = pc.resolve(args)
    stem = f"{args.date}_{args.prompt.stem}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json, out_md = args.output_dir / f"{stem}.json", args.output_dir / f"{stem}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2
    ids = [r["id"] for r in rules]
    ans, attempts = pc.ask(cli, prompt_text, args, lambda raw: (raw, check(raw, ids, labels, args.most)))
    run = {"version": VERSION, "date": args.date, "prompt": args.prompt.stem, "prompt_sha256": pc.sha256_bytes(args.prompt.read_bytes()),
           "model": model, "effort": args.effort, "cli_version": link_ideas.cli_version(cli),
           "inputs": {pc.rel(p): pc.sha256_bytes(p.read_bytes()) for p in (args.lineages, args.timeline, args.decisions)},
           "spec_sha256": {pc.rel(f): pc.sha256_bytes(f.read_bytes()) for f in sorted(args.spec.glob("*.md"))},
           "input_sha256": pc.sha256_bytes(prompt_text.encode()), "rules": rules, "labels": labels, "attempts": attempts, "answer": ans}
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if ans is None:
        print("no answer passed the checks", file=sys.stderr)
        return 1
    trace = {rid: labs for rid, labs in ans["traces"]}
    none = [r for r in rules if not trace.get(r["id"])]
    L = [f"# The rules and the ideas they come from, {args.date}", "",
         f"Written by `scripts/trace_rules.py` ({VERSION}); prompt `{args.prompt.stem}`, model {model} at effort {args.effort}. The",
         "traces are the model's reading. Rules: the bold-numbered statements of the specification, the numbered sections of",
         "the documents without them, and the entries of the decision log.", "",
         f"{len(rules)} rules; {len(rules) - len(none)} traced to at least one idea; {len(none)} to none.", ""]
    for kind, title in (("spec", "The specification"), ("decision", "The decision log")):
        L += [f"## {title}", ""]
        for r in rules:
            if r["kind"] != kind:
                continue
            labs = trace.get(r["id"], [])
            L.append(f"- **{r['id']}** {r['title']} (`{r['source']}`)")
            for lab in labs:
                d = der[labels[lab]]
                L.append(f"  - `{d['id']}` ({d['origin']}, {d['first'].get('time_local', '')[:10]}): {d['statement']}")
            if not labs:
                L.append("  - no idea behind it")
        L.append("")
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out_md}\n{len(rules) - len(none)} of {len(rules)} rules traced to an idea")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
