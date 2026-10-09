#!/usr/bin/env python3
"""The sample of decision cases, its exposure, and Luciano's review (step 5 of
record/plan-principles-validation-2026-10-09-execution.md). Four subcommands, run in this order:

  draw      draws the sample (D9): from the drafted decisions whose alternative is not constructed and
            that Luciano took (by choice or confirmation), plus every reversal, stratified by area,
            who decided and repository, with a recorded seed; freezes it in
            `record/validation/sample_<date>.json`. A sample is never redrawn or replenished.
  exposure  the exposure judge (D3), prompt `judge_exposure_v1`, one isolated call per sampled case
            that is eligible for some principle: it reads the session up to Luciano's turn and the
            case's eligible principles, and answers none, possible or explicit per principle, with a
            verbatim quote checked against the session. Writes `exposure_<date>.jsonl`.
  write     writes `review_<date>.md`: per case the question, A and B, what was chosen, who decided,
            the evidence, the exposure answers that are not none (each with a line for Luciano's ok
            or no), an optional line for a known tradeoff in his words, and a `Mark:` line.
  apply     after Luciano's marks are committed, reads them and sets `approved: true` on the cases
            marked ok, with the review's commit; `no` rejects; any other text is kept as his
            correction and the case stays unapproved until redrafted. Nothing else sets approved.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402
import eligible_cases as ec  # noqa: E402

VERSION = "review_cases v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATION = REPO_ROOT / "record" / "validation"
JUDGE_PROMPT = REPO_ROOT / "prompts" / "judge_exposure_v1.md"
PLACEHOLDER = "<<<INPUT>>>"
LEVELS = ("none", "possible", "explicit")


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def area_of(case: dict) -> str:
    return "language" if "language" in (case.get("areas") or []) else "method"


def draw(args) -> int:
    out = args.output_dir / f"sample_{args.date}.json"
    if list(args.output_dir.glob("sample_*.json")) and not args.another:
        print(f"ERROR: a sample exists ({', '.join(p.name for p in args.output_dir.glob('sample_*.json'))}); "
              "a sample is never redrawn (--another only for a new, separately reported experiment)", file=sys.stderr)
        return 2
    cases = load_jsonl(args.cases)
    pool = [c for c in cases if c.get("is_decision") and c.get("counterfactual_status") != "constructed"]
    rev = [c for c in pool if c.get("reverses") or c.get("reversed_by")]
    main = [c for c in pool if c.get("decided_by") in ("luciano_choice", "luciano_confirmation") and c not in rev]
    rng = random.Random(args.seed)
    chosen = list(rev)[:args.n]
    strata = defaultdict(list)
    for c in sorted(main, key=lambda c: c["id"]):
        strata[(area_of(c), c["decided_by"], c.get("session_repo"))].append(c)
    left = args.n - len(chosen)
    total = sum(len(v) for v in strata.values())
    if left > 0 and total:
        quota = {k: max(1, round(left * len(v) / total)) for k, v in strata.items()}
        while sum(quota.values()) > left:  # trim the largest quotas first
            k = max(quota, key=lambda k: (quota[k], k))
            quota[k] -= 1
        for k in sorted(strata):
            chosen += rng.sample(strata[k], min(quota.get(k, 0), len(strata[k])))
    sample = {"version": VERSION, "date": args.date, "seed": args.seed, "n": args.n, "cases_sha256": pc.sha256_bytes(args.cases.read_bytes()),
              "pool": {"drafted": len(cases), "decisions_not_constructed": len(pool), "reversals": len(rev), "main": len(main)},
              "strata": {"|".join(map(str, k)): len(v) for k, v in sorted(strata.items())},
              "cases": [c["id"] for c in chosen]}
    out.write_text(json.dumps(sample, indent=1) + "\n", encoding="utf-8")
    print(f"sample of {len(chosen)} cases ({len(rev)} reversals) written to {out}; commit it before anyone reads the cases")
    return 0


def exposure(args) -> int:
    sample = json.loads(args.sample.read_text(encoding="utf-8"))
    cases = {c["id"]: c for c in load_jsonl(args.cases)}
    pairs = defaultdict(list)
    for p in load_jsonl(args.eligibility):
        if p["eligible"]:
            pairs[p["unit"]].append(p["principle"])
    dates = json.loads(args.dates.read_text(encoding="utf-8"))["principles"]
    units = {u["id"]: u for u in load_jsonl(args.units)}
    out = args.output_dir / f"exposure_{sample['date']}.jsonl"
    done = {r["case"] for r in load_jsonl(out)}
    todo = [cid for cid in sample["cases"] if cid not in done and pairs.get(cases[cid]["unit"])]
    print(f"sampled cases: {len(sample['cases'])} | eligible for some principle and not yet judged: {len(todo)}")
    if args.dry_run:
        return 0
    template = args.prompt.read_text(encoding="utf-8")
    cli, model, agent = pc.resolve(args)
    with out.open("a", encoding="utf-8") as fh:
        for cid in todo:
            u = units[cases[cid]["unit"]]
            turns = ec.session_turns(ec.transcript_path(u["source"]))
            before = "\n\n".join(f"[line {n}] {t}" for n, t in turns if n <= u["luciano"]["line"])[-args.session_chars:]
            princ = pairs[u["id"]]
            listing = "\n".join(f"- {p}: {dates[p]['statement']} (his words: \"{dates[p].get('quote', '')}\")" for p in princ)
            body = f"## The principles\n\n{listing}\n\n## The session, up to the moment of the decision\n\n{before}"

            def chk(raw, princ=princ, before=before):
                errs = []
                got = {e.get("principle"): e for e in (raw.get("exposure") or []) if isinstance(e, dict)} if isinstance(raw, dict) else {}
                for p in princ:
                    e = got.get(p)
                    if e is None:
                        errs.append(f"{p} is not answered")
                    elif e.get("level") not in LEVELS:
                        errs.append(f"{p}: level must be one of {LEVELS}")
                    elif e["level"] != "none" and not pc.quote_in(e.get("quote", ""), before):
                        errs.append(f"{p}: the quote is not in the session: \"{str(e.get('quote', ''))[:80]}\"")
                return raw, errs
            ans, attempts = pc.ask(cli, template.replace(PLACEHOLDER, body), args, chk, f"{cid}: ")
            fh.write(json.dumps({"case": cid, "unit": u["id"], "principles": princ, "answer": ans, "attempts": attempts,
                                 "prompt_sha256": pc.sha256_bytes(args.prompt.read_bytes()), "model": model, "effort": args.effort,
                                 "input_sha256": pc.sha256_bytes(body.encode())}, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"{cid}: " + (", ".join(f"{e['principle']} {e['level']}" for e in ans["exposure"]) if ans else "no answer passed"))
    return 0


def write(args) -> int:
    sample = json.loads(args.sample.read_text(encoding="utf-8"))
    cases = {c["id"]: c for c in load_jsonl(args.cases)}
    expo = {r["case"]: r for r in load_jsonl(args.output_dir / f"exposure_{sample['date']}.jsonl")}
    out = args.output_dir / f"review_{sample['date']}.md"
    if out.exists():
        print(f"ERROR: {out.name} exists; it may already carry marks", file=sys.stderr)
        return 2
    L = [f"# Review of the sampled decision cases, {sample['date']}", "",
         f"Written by `scripts/review_cases.py write` ({VERSION}) for Luciano. {len(sample['cases'])} cases, drawn with seed {sample['seed']}",
         "and frozen before anyone read them; the approved ones are the experiment, none is replaced.", "",
         "Under each case: `Mark:` ok (the case is a real decision, the question and options are fair, what was chosen is right),",
         "no, or a correction in your words. `Tradeoff:` optional, a tradeoff you know the decision weighed, without naming a",
         "principle. Under each exposure answer: ok if the agent had that principle in view before this moment, no if not.", ""]
    for cid in sample["cases"]:
        c = cases[cid]
        L += [f"## {cid}", "", f"**Question.** {c['question']}", "", f"- A: {c['A']}", f"- B: {c['B']}", "",
              f"Chosen: {c['actual']}. Decided by: {c['decided_by']}. Alternative: {c['counterfactual_status']}. "
              f"Unit {c['unit']}, {c['time'][:16]}, {c.get('session_repo')}, account {c.get('account')}"
              + (f", commits {', '.join(h[:7] for h in c['commits'])}" if c.get("commits") else "")
              + (", a reversal" if c.get("reverses") or c.get("reversed_by") else "") + ".", "",
              f"> chosen: \"{c['evidence']['chosen']}\"", ">",
              f"> alternative: \"{c['evidence']['counterfactual'] or '(constructed)'}\"", ">",
              f"> who: \"{c['evidence']['decided_by']}\"", ""]
        for e in ((expo.get(cid) or {}).get("answer") or {}).get("exposure", []):
            if e["level"] != "none":
                L += [f"Exposure {e['principle']} ({e['level']}): \"{e['quote']}\"", f"Exposure {e['principle']}: ", ""]
        L += ["Tradeoff: ", "", "Mark: ", ""]
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out}; commit it before marking")
    return 0


def apply(args) -> int:
    top = subprocess.run(["git", "-C", str(args.review.resolve().parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if not top:
        print("ERROR: the review is not in a git repository", file=sys.stderr)
        return 2
    rel = args.review.resolve().relative_to(top)
    dirty = subprocess.run(["git", "-C", top, "status", "--porcelain", "--", str(rel)], capture_output=True, text=True).stdout
    commit = subprocess.run(["git", "-C", top, "log", "-1", "--format=%h", "--", str(rel)], capture_output=True, text=True).stdout.strip()
    if dirty.strip() or not commit:
        print("ERROR: commit the marked review first; the marks are applied from a commit", file=sys.stderr)
        return 2
    marks, cur = {}, None
    for line in args.review.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (C-\S+)", line)
        if m:
            cur = m.group(1)
            marks[cur] = {"mark": "", "tradeoff": "", "exposure": {}}
        elif cur and line.startswith("Mark:"):
            marks[cur]["mark"] = line[5:].strip()
        elif cur and line.startswith("Tradeoff:"):
            marks[cur]["tradeoff"] = line[9:].strip()
        elif cur and (m := re.match(r"^Exposure (P\d+): (.*)$", line)):
            marks[cur]["exposure"][m.group(1)] = m.group(2).strip()
    cases = load_jsonl(args.cases)
    n = {"ok": 0, "no": 0, "correction": 0, "unmarked": 0}
    for c in cases:
        if c["id"] not in marks:
            continue
        mk = marks[c["id"]]
        word = mk["mark"].strip().lower()
        verdict = "ok" if word == "ok" else ("no" if word == "no" else ("unmarked" if not word else "correction"))
        n[verdict] += 1
        c["approved"] = verdict == "ok"
        c["review"] = {"file": str(rel), "commit": commit, "verdict": verdict, "mark": mk["mark"], "tradeoff": mk["tradeoff"],
                       "exposure": mk["exposure"]}
    args.cases.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cases), encoding="utf-8")
    print(f"applied from {commit}: " + ", ".join(f"{k} {v}" for k, v in n.items()))
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("draw", "exposure", "write", "apply"):
        s = sub.add_parser(name)
        s.add_argument("--cases", type=Path, default=VALIDATION / "decision_cases.jsonl")
        s.add_argument("--output-dir", type=Path, default=VALIDATION)
        if name == "draw":
            s.add_argument("--n", type=int, default=40)
            s.add_argument("--seed", type=int, default=20261010)
            s.add_argument("--date", default=date.today().isoformat())
            s.add_argument("--another", action="store_true")
        if name in ("exposure", "write"):
            s.add_argument("--sample", type=Path, required=True)
        if name == "exposure":
            s.add_argument("--units", type=Path, default=VALIDATION / "decision_units.jsonl")
            s.add_argument("--eligibility", type=Path, default=VALIDATION / "eligibility.jsonl")
            s.add_argument("--dates", type=Path, default=VALIDATION / "principle_dates.json")
            s.add_argument("--session-chars", type=int, default=60000, help="how much of the session before the decision the judge reads")
            pc.common_args(s, JUDGE_PROMPT)
        if name == "apply":
            s.add_argument("--review", type=Path, required=True)
    args = ap.parse_args(argv)
    return {"draw": draw, "exposure": exposure, "write": write, "apply": apply}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
