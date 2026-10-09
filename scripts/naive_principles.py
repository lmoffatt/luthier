#!/usr/bin/env python3
"""The naive way of finding a language's principles, against which the pipeline of lineages and
find_principles is measured (Luciano, 2026-10-10: "Quizas darle todas las ideas a un agente naive
y pedirle que extraiga de ahi las reglas y principios sea mejor que esta arquitectura elaborada").

Reads the timeline of ideas (`ideas_timeline.py`'s rows, no lineages), shows the model every row as
`r<n> | date | who | the idea`, and asks, with the prompt `prompts/naive_principles_v1.md`, for the
rules and principles of the language: no criterion, no definition of a principle, no instruction to
be blind. One isolated call (no tools, no session). The answer is checked only for its form (at
most --max-candidates, ids unique, each with a statement and rows that exist) and asked again with
its errors. The quote shown with each candidate is the first row it cites, filled in by this script.

Writes `<output-dir>/<date>_naive_principles_v1_<agent>_<model>.json` in the shape
`compare_principles.py --candidates` reads, and `.md`.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402

VERSION = "naive_principles v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "naive_principles_v1.md"
PLACEHOLDER = "<<<INPUT>>>"


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--timeline", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--redact", action="append", default=[], metavar="TERM=REPLACEMENT",
                   help="replace a name in what the model is shown (controls on known languages)")
    p.add_argument("--max-candidates", type=int, default=7)
    p.add_argument("--quote-chars", type=int, default=300)
    p.add_argument("--max-input-chars", type=int, default=700000)
    p.add_argument("--date", default=date.today().isoformat())
    pc.common_args(p, DEFAULT_PROMPT)
    return p.parse_args(argv)


def idea_lines(rows: list[dict], red=lambda t: t) -> tuple[str, dict[str, str]]:
    labels, lines = {}, []
    for i, r in enumerate(rows, 1):
        labels[f"r{i}"] = r["id"]
        what = " ".join(str(r.get("what", "")).split())
        lines.append(f"r{i} | {r.get('time_local', '')[:10]} | {red(str(r.get('who', '?')))} | {red(what)}")
    return "\n".join(lines), labels


def check(ans, labels: dict[str, str], max_candidates: int) -> list[str]:
    if not isinstance(ans, dict) or not isinstance(ans.get("candidates"), list) or not ans["candidates"]:
        return ["the answer must be an object with a non-empty list candidates"]
    cands, errors = ans["candidates"], []
    if len(cands) > max_candidates:
        errors.append(f"{len(cands)} candidates; at most {max_candidates}")
    ids = [c.get("id") if isinstance(c, dict) else None for c in cands]
    if len(set(ids)) != len(ids) or not all(ids):
        errors.append("candidate ids missing or repeated")
    for c in cands:
        if not isinstance(c, dict):
            errors.append(f"candidate {c!r} is not an object")
            continue
        if not str(c.get("statement", "")).strip():
            errors.append(f"{c.get('id')}: empty statement")
        rows = c.get("rows")
        if not isinstance(rows, list) or not rows:
            errors.append(f"{c.get('id')}: rows must be a non-empty list of r<n>")
        elif bad := [x for x in rows if x not in labels]:
            errors.append(f"{c.get('id')}: unknown rows {', '.join(map(str, bad[:5]))}")
    return errors


def expand(ans: dict, labels: dict[str, str], by_id: dict[str, dict], quote_chars: int) -> dict:
    out = []
    for c in ans["candidates"]:
        rows = [labels[x] for x in c["rows"]]
        first = by_id[rows[0]]
        out.append({"id": c["id"], "statement": c["statement"], "rows": rows,
                    "quote": link_ideas.clip(first.get("quote", ""), quote_chars),
                    "quote_row": rows[0], "who": first.get("who", "?"), "time_local": first.get("time_local", "")})
    return {"candidates": out}


def write_report(md: Path, run: dict, ans: dict) -> None:
    L = [f"# Principles of {run['vars'].get('language', '?')}, asked naively, {run['date']}", "",
         f"Written by `scripts/naive_principles.py` ({VERSION}). Prompt `{run['prompt']}` (sha256 {run['prompt_sha256'][:12]}),",
         f"model {run['model']} at effort {run['effort']} via {run['agent']} ({run['cli_version']}); the model saw every row",
         "of the timeline (date, who, the idea) and was asked for the rules and principles, nothing more"
         + (f"; names redacted ({'; '.join(run['redact'])})" if run["redact"] else "") + ".",
         "Inputs by sha256: " + "; ".join(f"`{k}` {v['sha256'][:12]}" for k, v in run["inputs"].items()) + ".",
         f"Rows shown: {run['rows']}. The quote is the first row each candidate cites, filled in by the script.", "", "```"]
    for c in ans["candidates"]:
        L += [f"{c['id']}  {pc.wrap(c['statement'], indent='    ')}",
              f"Quote:      \"{pc.wrap(c['quote'])}\"",
              f"Said by:    {c['who']}, {c['time_local'][:16]} (row {c['quote_row']})",
              f"Rows:       {len(c['rows'])}", ""]
    L.append("```")
    md.write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    for k, p in (("timeline", args.timeline), ("prompt", args.prompt)):
        if not p.is_file():
            print(f"ERROR: {k} not found: {p}", file=sys.stderr)
            return 2
    template, left = pc.fill(args.prompt.read_text(encoding="utf-8"), args.var + [f"max_candidates={args.max_candidates}"])
    if left:
        print(f"ERROR: the prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
        return 2
    rows = link_ideas.load_timeline(args.timeline)
    body, labels = idea_lines(rows, pc.redactor(args.redact))
    prompt_text = template.replace(PLACEHOLDER, body)
    print(f"rows: {len(rows)} | input: {len(prompt_text):,} chars (~{len(prompt_text) // 4:,} tokens) | "
          f"max candidates: {args.max_candidates}")
    if args.show_input:
        args.show_input.write_text(prompt_text, encoding="utf-8")
        print(f"written: {args.show_input}")
        return 0
    if len(prompt_text) > args.max_input_chars:
        print(f"ERROR: the input is {len(prompt_text):,} chars, over --max-input-chars", file=sys.stderr)
        return 2
    if args.dry_run:
        return 0
    try:
        cli, model, agent = pc.resolve(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    tag = f"{args.date}_{args.prompt.stem}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json, out_md = args.output_dir / f"{tag}.json", args.output_dir / f"{tag}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2
    run = {"version": VERSION, "date": args.date, "prompt": args.prompt.stem,
           "prompt_sha256": pc.sha256_bytes(args.prompt.read_bytes()),
           "vars": dict(kv.partition("=")[::2] for kv in args.var), "redact": args.redact,
           "model": model, "agent": agent, "effort": args.effort, "cli_version": link_ideas.cli_version(cli),
           "max_candidates": args.max_candidates, "quote_chars": args.quote_chars, "rows": len(rows),
           "inputs": {pc.rel(args.timeline): {"sha256": pc.sha256_bytes(args.timeline.read_bytes())}},
           "input_sha256": pc.sha256_bytes(prompt_text.encode()), "row_labels": labels}
    by_id = {r["id"]: r for r in rows}

    def expand_check(raw):
        errors = check(raw, labels, args.max_candidates)
        return (None if errors else expand(raw, labels, by_id, args.quote_chars)), errors
    ans, run["attempts"] = pc.ask(cli, prompt_text, args, expand_check)
    run["answer"] = ans
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if ans is None:
        print(f"no answer passed the checks; the attempts are in {out_json}", file=sys.stderr)
        return 1
    write_report(out_md, run, ans)
    print(f"written: {out_json}\n         {out_md}\ncandidates: {len(ans['candidates'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
