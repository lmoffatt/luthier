#!/usr/bin/env python3
"""Find candidate principles among the lineages of a language's ideas, blind to the principles the
language already has (the first of two steps; match_principles.py is the second, for Luthier).

Reads the lineages (`link_ideas.py`'s state) and the timeline they point into, and runs the prompt
`prompts/find_principles_v1.md`, isolated (no tools, no session), in one call. The prompt carries
Luciano's criterion of infectability and nothing about the language beyond its name and its
designers (--var language=... --var designers=...): no description of it, no principles in force,
no decisions, no objectives (Luciano, 2026-10-09: a filter that carries the language's ideas finds
what it brings). --redact TERM=REPLACEMENT replaces names in what the model is shown, for the
controls on languages a model may know.

The answer is checked before it is accepted: every lineage classified once (candidate, considered,
not a principle), every id known, each quote found in what the model was shown of its row and that
row in one of the candidate's lineages, one strongest axis and at most two more, a list of harms,
the closest lineage left out (classified considered), and why each candidate ranks above the next.
A rejected answer is asked again with its errors. Whose words a quote is, its source and how often
its lineages recur are filled in from the rows by this script.

Writes `<output-dir>/<date>_find_principles_v1_<agent>_<model>.json` (inputs and prompt by sha256,
the labels, every attempt, the accepted answer, warnings) and `.md` (the candidates, then the
considered lineages). Luciano runs it on Luthier's record.
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

VERSION = "find_principles v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "find_principles_v2.md"
DEFAULT_LINEAGES = REPO_ROOT / "record" / "ideas" / "lineages_link_ideas_v1_claude-code_opus.json"
DEFAULT_TIMELINE = REPO_ROOT / "record" / "ideas" / "timeline.jsonl"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "distillation"
PLACEHOLDER = "<<<INPUT>>>"
VERDICTS = ("candidate", "considered", "not_principle")
SCOPES = ("language", "method", "other")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--lineages", type=Path, default=DEFAULT_LINEAGES)
    p.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--redact", action="append", default=[], metavar="TERM=REPLACEMENT",
                   help="replace a name in what the model is shown (controls on known languages)")
    p.add_argument("--max-candidates", type=int, default=7, help="the most candidates one run may propose (P12)")
    p.add_argument("--quotes-per-lineage", type=int, default=4)
    p.add_argument("--quote-chars", type=int, default=300)
    p.add_argument("--max-input-chars", type=int, default=700000)
    p.add_argument("--date", default=date.today().isoformat())
    pc.common_args(p, DEFAULT_PROMPT)
    return p.parse_args(argv)


def expand(ans: dict, llabels: dict, qlabels: dict) -> tuple[dict, list[str]]:
    if not isinstance(ans, dict):
        return ans, ["the answer is not a JSON object"]
    errors, cls = [], []
    lid = lambda x: llabels.get(x, f"?{x}")
    for c in ans.get("classification", []) or []:
        if not (isinstance(c, list) and len(c) in (3, 4)):
            errors.append(f"classification entry {c!r} is not [l<n>, verdict, C<n> or '', note]")
            continue
        cls.append({"lineage": lid(c[0]), "label": c[0], "verdict": c[1],
                    "candidate": (c[2] or None) if c[1] == "candidate" else None, "note": c[3] if len(c) == 4 else ""})
    cands = []
    for c in ans.get("candidates", []) or []:
        c = dict(c)
        c["lineages"] = [lid(x) for x in c.get("lineages", []) or []]
        q = c.pop("quote", None)
        c["quote_label"], c["quote_row"], c["quote"] = q, qlabels.get(q, f"?{q}"), c.pop("quote_text", "")
        if isinstance(c.get("beats"), dict):
            c["beats"] = {**c["beats"], "lineage": lid(c["beats"].get("lineage"))}
        cands.append(c)
    return {"classification": cls, "candidates": cands}, errors


def check_answer(ans: dict, der: dict, qtext: dict, max_candidates: int, needs_alternative: bool = False) -> list[str]:
    errors: list[str] = []
    cands = ans.get("candidates", []) or []
    cand_ids = [str(c.get("id", "")) for c in cands]
    if len(cands) > max_candidates:
        errors.append(f"{len(cands)} candidates; at most {max_candidates}")
    if len(set(cand_ids)) != len(cand_ids):
        errors.append("candidate ids repeat")
    seen = Counter()
    for c in ans.get("classification", []):
        seen[c["lineage"]] += 1
        if c["lineage"] not in der:
            errors.append(f"classification of unknown lineage {c['label']!r}")
        if c["verdict"] not in VERDICTS:
            errors.append(f"{c['label']}: verdict {c['verdict']!r} is not one of {VERDICTS}")
        if c["verdict"] == "candidate" and c["candidate"] not in cand_ids:
            errors.append(f"{c['label']}: candidate {c['candidate']!r} is not among the candidates")
    verdict_of = {c["lineage"]: c["verdict"] for c in ans.get("classification", [])}
    missing = [l for l in der if seen[l] == 0]
    if missing:
        errors.append(f"lineages not classified: {len(missing)}, for example {', '.join(missing[:10])}")
    twice = [l for l in der if seen[l] > 1]
    if twice:
        errors.append(f"lineages classified more than once: {', '.join(twice[:10])}")
    for c in cands:
        cid = c.get("id")
        lins = c.get("lineages", [])
        if not lins or any(l not in der for l in lins):
            errors.append(f"{cid}: lineages unknown or missing")
        rows = {m["id"] for l in lins if l in der for m in der[l]["members"]}
        if c["quote_row"] not in rows:
            errors.append(f"{cid}: quote {c['quote_label']!r} is not a quote of its lineages")
        elif not pc.quote_in(c.get("quote", ""), qtext.get(c["quote_label"], "")):
            errors.append(f"{cid}: quote_text is not in {c['quote_label']}: \"{str(c.get('quote', ''))[:80]}\"")
        if c.get("scope") not in SCOPES:
            errors.append(f"{cid}: scope {c.get('scope')!r} is not one of {SCOPES}")
        if not str(c.get("statement", "")).strip():
            errors.append(f"{cid}: empty statement")
        if needs_alternative and not str(c.get("instead_of", "")).strip():
            errors.append(f"{cid}: instead_of is missing; a principle names the road not taken")
        st = c.get("strongest") or {}
        if not isinstance(st, dict) or st.get("axis") not in pc.AXES or not str(st.get("why", "")).strip():
            errors.append(f"{cid}: strongest needs an axis among {pc.AXES} and a why")
        also = c.get("also") or []
        if not isinstance(also, list) or len(also) > 2 or any(
                not isinstance(e, dict) or e.get("axis") not in pc.AXES or not str(e.get("why", "")).strip() for e in also):
            errors.append(f"{cid}: also is at most 2 axes, each with a why")
        if not isinstance(c.get("harms"), list) or any(not str(h).strip() for h in c.get("harms") or []):
            errors.append(f"{cid}: harms must be a list of non-empty strings, empty if you looked and found none")
        b = c.get("beats") or {}
        bl = b.get("lineage") if isinstance(b, dict) else None
        if bl not in der or bl in lins or verdict_of.get(bl) != "considered" or not str(b.get("why", "")).strip():
            errors.append(f"{cid}: beats must name a lineage classified considered, outside the candidate, with a why")
    for c in cands[:-1]:
        if not str(c.get("above_next", "")).strip():
            errors.append(f"{c.get('id')}: above_next is missing")
    return errors


def run_warnings(ans: dict) -> list[str]:
    cands = ans["candidates"]
    out = []
    if len(cands) > 2 and len({c["strongest"]["axis"] for c in cands}) == 1:
        out.append(f"every candidate's strongest axis is {cands[0]['strongest']['axis']}.")
    if len(cands) > 2 and all(not c.get("harms") for c in cands):
        out.append("no candidate names a harm.")
    return out


def write_report(md: Path, run: dict, ans: dict, der: dict) -> None:
    by_v = Counter(c["verdict"] for c in ans["classification"])
    L = [f"# Candidate principles of {run['vars'].get('language', '?')}, found blind, {run['date']}", "",
         f"Written by `scripts/find_principles.py` ({VERSION}). Prompt `{run['prompt']}` (sha256 {run['prompt_sha256'][:12]}),",
         f"model {run['model']} at effort {run['effort']} via {run['agent']} ({run['cli_version']}); the model saw only the",
         "lineages and the criterion of infectability" + (f", with names redacted ({'; '.join(run['redact'])})" if run["redact"] else "") + ".",
         "Inputs by sha256: " + "; ".join(f"`{k}` {v['sha256'][:12]}" for k, v in run["inputs"].items()) + ".",
         "Each candidate shows apart what the script took from the rows and what is the model's reading.", "",
         f"Lineages: {len(der)}; " + ", ".join(f"{v} {by_v.get(v, 0)}" for v in VERDICTS) + ".", ""]
    if run.get("warnings"):
        L += ["Warnings on the run: " + " ".join(run["warnings"]), ""]
    L += ["## Candidates", "", "```"]
    for c in ans["candidates"]:
        lins = [l for l in c["lineages"] if l in der]
        rows = {m["id"]: m for l in lins for m in der[l]["members"]}
        q = rows.get(c["quote_row"], {})
        first = min((der[l]["first"] for l in lins), key=lambda m: m.get("time_utc", ""))
        L += [f"{c['id']}  {pc.wrap(c['statement'], indent='    ')}",
              *([f"Instead of: {pc.wrap(c['instead_of'])}"] if c.get("instead_of") else []),
              f"Scope:      {c['scope']}",
              "-- from the rows, by the script",
              f"Quote:      \"{pc.wrap(q.get('quote', c['quote']))}\"",
              f"Said by:    {q.get('who', '?')}, {q.get('time_local', '')[:16]}",
              f"Source:     {pc.wrap(q.get('source', ''))} (row {c['quote_row']})",
              f"Lineages:   {pc.wrap(', '.join(lins))}",
              f"Witnesses:  first {first.get('time_local', '')[:10]} by {first.get('who', '?')}; "
              f"{sum(der[l]['witnesses'] for l in lins)} witnesses over "
              f"{len({m.get('time_local', '')[:10] for l in lins for m in der[l]['members']})} days",
              f"-- the model's reading ({run['model']}, effort {run['effort']})",
              f"Strongest:  {pc.wrap(c['strongest']['axis'] + '. ' + c['strongest']['why'])}",
              *[f"Also:       {pc.wrap(e['axis'] + '. ' + e['why'])}" for e in c.get("also", [])],
              *([f"Harms:      {pc.wrap(h)}" for h in c["harms"]] or ["Harms:      none found"]),
              f"Beats:      {pc.wrap(c['beats']['lineage'] + ' (' + der[c['beats']['lineage']]['statement'] + '). ' + c['beats']['why'])}",
              *([f"Above next: {pc.wrap(c['above_next'])}"] if c.get("above_next") else []), ""]
    L += ["```", "", "## Considered and left out", ""]
    cons = [c for c in ans["classification"] if c["verdict"] == "considered"]
    for c in cons:
        d = der[c["lineage"]]
        L.append(f"- `{d['id']}` ({d['origin']}, {d['rows']} rows): {d['statement']} *{c.get('note', '')}*")
    if not cons:
        L.append("none")
    md.write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    for k, p in (("lineages", args.lineages), ("timeline", args.timeline), ("prompt", args.prompt)):
        if not p.is_file():
            print(f"ERROR: {k} not found: {p}", file=sys.stderr)
            return 2
    template, left = pc.fill(args.prompt.read_text(encoding="utf-8"), args.var + [f"max_candidates={args.max_candidates}"])
    if left:
        print(f"ERROR: the prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
        return 2
    state = json.loads(args.lineages.read_text(encoding="utf-8"))
    rows = link_ideas.load_timeline(args.timeline)
    der = link_ideas.derive(state, {r["id"]: r for r in rows})
    if not der:
        print("ERROR: no lineages", file=sys.stderr)
        return 2
    red = pc.redactor(args.redact)
    qlabels, qtext = {}, {}
    body = pc.lineage_blocks(der, args.quotes_per_lineage, args.quote_chars, red, qlabels, qtext)
    llabels = pc.labels_for(der)
    prompt_text = template.replace(PLACEHOLDER, body)
    pending = sum(1 for r in rows if r["id"] not in state["assign"] and r["id"] not in state["unplaced"])
    print(f"lineages: {len(der)} | rows not yet in a lineage: {pending} | input: {len(prompt_text):,} chars "
          f"(~{len(prompt_text) // 4:,} tokens) | max candidates: {args.max_candidates}")
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
    prompt_id = args.prompt.stem
    tag = f"{args.date}_{prompt_id}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json, out_md = args.output_dir / f"{tag}.json", args.output_dir / f"{tag}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2
    run = {"version": VERSION, "date": args.date, "prompt": prompt_id, "prompt_sha256": pc.sha256_bytes(args.prompt.read_bytes()),
           "vars": dict(kv.partition("=")[::2] for kv in args.var), "redact": args.redact,
           "model": model, "agent": agent, "effort": args.effort, "cli_version": link_ideas.cli_version(cli),
           "max_candidates": args.max_candidates, "max_thinking_tokens": args.max_thinking_tokens,
           "quotes_per_lineage": args.quotes_per_lineage, "quote_chars": args.quote_chars,
           "inputs": {pc.rel(p): {"sha256": pc.sha256_bytes(p.read_bytes())} for p in (args.lineages, args.timeline)},
           "input_sha256": pc.sha256_bytes(prompt_text.encode()), "lineage_labels": llabels, "quote_labels": qlabels,
           "lineages": len(der)}

    def expand_check(raw: dict):
        a, errors = expand(raw, llabels, qlabels)
        return a, errors + (check_answer(a, der, qtext, args.max_candidates, "instead_of" in template)
                            if isinstance(a, dict) else [])
    ans, run["attempts"] = pc.ask(cli, prompt_text, args, expand_check)
    run["answer"] = ans
    run["warnings"] = run_warnings(ans) if ans else []
    for w in run["warnings"]:
        print(f"warning: {w}", file=sys.stderr)
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if ans is None:
        print(f"no answer passed the checks; the attempts are in {out_json}", file=sys.stderr)
        return 1
    write_report(out_md, run, ans, der)
    print(f"written: {out_json}\n         {out_md}\ncandidates: {len(ans['candidates'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
