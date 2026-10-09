#!/usr/bin/env python3
"""The judge of the controls (record/controls/README.md): compare candidate principles with the
reference of a language and with Luthier's items, and score the filter.

Candidates come from a `find_principles.py` output (--candidates), or, with --recall, from the
model's memory alone: the prompt `recall_principles_v1` asks for the language's principles with no
text to read, which measures what a model knows before it reads the corpus.

The judge, prompt `compare_principles_v1`, sees the candidates (statement and quote) and two lists,
A and B, without being told that A is the language's reference and B is Luthier's principles P1 to
P14 and features F1 to F16 (docs/rationale/10, section 0); it says which items of each list every
candidate states, with a reason. The answer is checked (every candidate once, every item id known)
and asked again with its errors if needed. The scores are computed here, by the rules the README
fixed before any run: a hit is a candidate that states an item of A; a leak is one that states an
item of B and none of A; the filter passes with no leak and at least half its candidates hits.

Writes `<control>/<date>_<tag>_compare_principles_v1_<agent>_<model>.json` and `.md`.
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

VERSION = "compare_principles v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "compare_principles_v1.md"
RECALL_PROMPT = REPO_ROOT / "prompts" / "recall_principles_v1.md"
FEATURES = REPO_ROOT / "docs" / "rationale" / "10-prior-art-languages.md"
PLACEHOLDER = "<<<INPUT>>>"
ITEM_RE = re.compile(r"^- ([A-Z]\d+) (.+)$")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--reference", type=Path, required=True, help="the control's reference.md")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--candidates", type=Path, help="a find_principles output (.json)")
    src.add_argument("--recall", action="store_true", help="candidates from the model's memory, no corpus")
    p.add_argument("--principles", type=Path, default=pl.DEFAULT_PRINCIPLES)
    p.add_argument("--features", type=Path, default=FEATURES)
    p.add_argument("--output-dir", type=Path, default=None, help="default: the reference's folder")
    p.add_argument("--max-candidates", type=int, default=7, help="for --recall")
    p.add_argument("--date", default=date.today().isoformat())
    pc.common_args(p, DEFAULT_PROMPT)
    return p.parse_args(argv)


def reference_items(path: Path) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for l in path.read_text(encoding="utf-8").splitlines() if (m := ITEM_RE.match(l))}


def luthier_items(principles: Path, features: Path) -> dict[str, str]:
    items = {pid: e["statement"] for pid, e in pl.parse_entries(principles.read_text(encoding="utf-8"), pl.P_HEAD_RE).items()}
    text = features.read_text(encoding="utf-8")
    sec = text[text.index("## 0."):text.index("## 1.")]
    cur = None
    for line in sec.splitlines():
        m = re.match(r"^- (F\d+) (.+)$", line)
        if m:
            cur = m.group(1)
            items[cur] = m.group(2).strip()
        elif cur and line.startswith("  ") and line.strip():
            items[cur] += " " + line.strip()
        else:
            cur = None
    return items


def block(title: str, items: dict[str, str]) -> str:
    return f"## {title}\n\n" + "\n".join(f"- {k}: {v}" for k, v in items.items())


def check(ans: dict, cands: dict, a: dict, b: dict) -> list[str]:
    if not isinstance(ans, dict):
        return ["the answer is not a JSON object"]
    errors, seen = [], []
    for j in ans.get("judgments", []) or []:
        cid = j.get("candidate")
        seen.append(cid)
        if cid not in cands:
            errors.append(f"unknown candidate {cid!r}")
        for lst, items in (("A", a), ("B", b)):
            for e in j.get(lst, []) or []:
                if not isinstance(e, dict) or e.get("item") not in items:
                    errors.append(f"{cid}: {lst} item {e!r} is not in list {lst}")
    missing = [c for c in cands if c not in seen]
    if missing:
        errors.append(f"candidates not judged: {', '.join(missing)}")
    if len(seen) != len(set(seen)):
        errors.append("a candidate is judged more than once")
    return errors


def score(ans: dict, cands: dict) -> dict:
    rows = []
    for j in ans["judgments"]:
        hit, echo = bool(j.get("A")), bool(j.get("B"))
        rows.append({"candidate": j["candidate"], "verdict": "hit" if hit else ("leak" if echo else "neither"),
                     "A": [e["item"] for e in j.get("A", [])], "B": [e["item"] for e in j.get("B", [])]})
    n = len(rows)
    hits = sum(r["verdict"] == "hit" for r in rows)
    leaks = sum(r["verdict"] == "leak" for r in rows)
    return {"rows": rows, "candidates": n, "hits": hits, "leaks": leaks,
            "neither": n - hits - leaks, "passes": leaks == 0 and hits * 2 >= n}


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    a = reference_items(args.reference)
    b = luthier_items(args.principles, args.features)
    if not a or not b:
        print("ERROR: a list is empty", file=sys.stderr)
        return 2
    out_dir = args.output_dir or args.reference.parent
    try:
        cli, model, agent = pc.resolve(args) if not args.dry_run else ("-", args.model or "opus", "claude-code")
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    run = {"version": VERSION, "date": args.date, "model": model, "agent": agent, "effort": args.effort,
           "cli_version": link_ideas.cli_version(cli) if cli != "-" else "",
           "inputs": {pc.rel(p): {"sha256": pc.sha256_bytes(p.read_bytes())} for p in (args.reference, args.principles, args.features)}}
    if args.recall:
        tmpl, left = pc.fill(RECALL_PROMPT.read_text(encoding="utf-8"), args.var + [f"max_candidates={args.max_candidates}"])
        if left:
            print(f"ERROR: the recall prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
            return 2
        tag = "recall"
        run["recall_prompt_sha256"] = pc.sha256_bytes(RECALL_PROMPT.read_bytes())
        if args.dry_run:
            print(tmpl)
            return 0

        def rc(raw):
            cs = raw.get("candidates") if isinstance(raw, dict) else None
            ok = isinstance(cs, list) and cs and all(isinstance(c, dict) and c.get("id") and c.get("statement") for c in cs)
            return raw, ([] if ok else ["candidates must be a non-empty list of {id, statement}"])
        rec, run["recall_attempts"] = pc.ask(cli, tmpl, args, rc, "recall: ")
        if rec is None:
            print("the recall answer did not pass", file=sys.stderr)
            return 1
        cands = {c["id"]: {"statement": c["statement"], "quote": ""} for c in rec["candidates"]}
    else:
        found = json.loads(args.candidates.read_text(encoding="utf-8"))
        tag = Path(args.candidates).stem.split("_")[0] + "_find"
        run["inputs"][pc.rel(args.candidates)] = {"sha256": pc.sha256_bytes(args.candidates.read_bytes())}
        cands = {c["id"]: {"statement": c["statement"], "quote": c["quote"]} for c in found["answer"]["candidates"]}
    run["candidates"] = cands
    body = "\n\n".join([
        "## List C\n\n" + "\n".join(f"- {cid}: {c['statement']}" + (f" (quote: \"{c['quote']}\")" if c["quote"] else "")
                                     for cid, c in cands.items()),
        block("List A", a), block("List B", b)])
    prompt_text = args.prompt.read_text(encoding="utf-8").replace(PLACEHOLDER, body)
    run["prompt_sha256"] = pc.sha256_bytes(args.prompt.read_bytes())
    run["input_sha256"] = pc.sha256_bytes(prompt_text.encode())
    if args.show_input:
        args.show_input.write_text(prompt_text, encoding="utf-8")
        return 0
    if args.dry_run:
        print(f"candidates {len(cands)}, list A {len(a)}, list B {len(b)}, input {len(prompt_text):,} chars")
        return 0
    stem = f"{args.date}_{tag}_{args.prompt.stem}_{agent}_{model}"
    out_json, out_md = out_dir / f"{stem}.json", out_dir / f"{stem}.md"
    if out_json.exists() and not args.force:
        print(f"ERROR: {out_json.name} exists; --force redoes it", file=sys.stderr)
        return 2
    ans, run["attempts"] = pc.ask(cli, prompt_text, args, lambda raw: (raw, check(raw, cands, a, b)), "judge: ")
    run["answer"] = ans
    if ans is None:
        out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("the judge's answer did not pass", file=sys.stderr)
        return 1
    run["score"] = s = score(ans, cands)
    out_json.write_text(json.dumps(run, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    why = {(j["candidate"], lst, e["item"]): e.get("why", "") for j in ans["judgments"] for lst in ("A", "B") for e in j.get(lst, [])}
    L = [f"# Control: {args.reference.parent.name}, {'from memory (no corpus)' if args.recall else 'the blind filter'}, {args.date}", "",
         f"Written by `scripts/compare_principles.py` ({VERSION}); judge prompt `{args.prompt.stem}` (sha256 {run['prompt_sha256'][:12]}),",
         f"model {model} at effort {args.effort}. List A is `{pc.rel(args.reference)}`; list B is Luthier's P1 to P14 and F1 to F16;",
         "the judge was not told which is which. Rules fixed in record/controls/README.md before any run.", "",
         "| candidates | hits | leaks | neither | passes |", "|---|---|---|---|---|",
         f"| {s['candidates']} | {s['hits']} | {s['leaks']} | {s['neither']} | {'yes' if s['passes'] else 'no'} |", "",
         "## Candidates", ""]
    for r in s["rows"]:
        c = cands[r["candidate"]]
        L.append(f"- **{r['candidate']}** ({r['verdict']}): {c['statement']}")
        for k in r["A"]:
            L.append(f"  - states reference {k}: {a[k]} *({why.get((r['candidate'], 'A', k), '')})*")
        for k in r["B"]:
            L.append(f"  - echoes Luthier {k}: {b[k][:120]} *({why.get((r['candidate'], 'B', k), '')})*")
    missed = [k for k in a if not any(k in r["A"] for r in s["rows"])]
    L += ["", f"## Reference items no candidate states ({len(missed)} of {len(a)})", "",
          ", ".join(missed) if missed else "none"]
    out_md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out_md}\nhits {s['hits']}/{s['candidates']}, leaks {s['leaks']}, passes: {s['passes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
