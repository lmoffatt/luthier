#!/usr/bin/env python3
"""Score Luthier's principles on the approved decision cases (step 6 of
record/plan-principles-validation-2026-10-09-execution.md). Luciano runs it, after his review.

Which cases: approved by Luciano, a decision whose alternative is not constructed, and, for each
principle, only the cases temporally eligible for it whose exposure is `none` (the judge said none,
or he marked its answer no). `--include-possible` adds the cases judged `possible`, for a sensitivity
run. The main result counts the decisions he took (choice and confirmation); the model's own are
reported apart.

What the model sees: for a principle, its statement and the cases as numbered questions with options
A and B, in an order shuffled with --seed. Nothing else: no id, date, source, outcome, status, other
principle or document name; a guard refuses a payload carrying any case's id, unit, time or commit.
Every principle runs twice, the options in the original order and swapped; an answer that changes
meaning with the order is position-unstable and is not evidence.

D10, before any outcome is looked at: --subset cases drawn with the seed are run one per call and
compared with the batched answers; below --agreement, the batched run is discarded and everything
runs one case per call.

Baselines (D13): B0, no principle; B1, each case with a principle drawn among those not eligible for
it; B2, the statements permuted among the principles (a derangement drawn with the seed).

Per principle: n, coverage, the four outcomes of D14 (picked the chosen option; lost a conflict, it
picked the other while another principle picked the chosen one; picked the other and no principle
picked the chosen one; NEITHER), unstable answers, stable accuracy with its Wilson interval, the
same for B0, B1 and B2 on the same cases. The conflict matrix and the reversals one by one. A zero
denominator gives null. No thresholds or labels (D4 as Luciano marked it).

Writes `record/validation/runs/<UTC timestamp>_temporal_principles_<model>.json` and `.md`; a run
never overwrites another.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402

VERSION = "validate_principles_temporal v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATION = REPO_ROOT / "record" / "validation"
PRINCIPLE_PROMPT = REPO_ROOT / "prompts" / "apply_principle_blind_v1.md"
BASELINE_PROMPT = REPO_ROOT / "prompts" / "apply_baseline_blind_v1.md"
PLACEHOLDER = "<<<INPUT>>>"
CHOICES = ("A", "B", "NEITHER")
MAIN_DECIDERS = ("luciano_choice", "luciano_confirmation")


def wilson(k: int, n: int, z: float = 1.96) -> list[float] | None:
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def ratio(a: int, b: int) -> float | None:
    return round(a / b, 3) if b else None


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def select(cases, eligibility, exposure, include_possible) -> tuple[dict, dict]:
    """(cases by id, principle -> [case ids]) for the run, with the reason each pair is out."""
    usable = {c["id"]: c for c in cases if c.get("approved") is True and c.get("is_decision")
              and c.get("counterfactual_status") != "constructed"}
    by_unit = {c["unit"]: cid for cid, c in usable.items()}
    expo = {}
    for r in exposure:
        for e in ((r.get("answer") or {}).get("exposure") or []):
            expo[(r["case"], e["principle"])] = e["level"]
    pairs = defaultdict(list)
    for p in eligibility:
        cid = by_unit.get(p["unit"])
        if not (p["eligible"] and cid):
            continue
        level = expo.get((cid, p["principle"]), "none")
        his = ((usable[cid].get("review") or {}).get("exposure") or {}).get(p["principle"], "").strip().lower()
        if level != "none" and his == "no":
            level = "none"
        if level == "none" or (include_possible and level == "possible"):
            pairs[p["principle"]].append(cid)
    return usable, dict(pairs)


def payload(cases: list[dict], swapped: bool) -> tuple[str, list[str]]:
    """The numbered decisions as the model sees them, built from question, A and B only."""
    lines, order = [], []
    for k, c in enumerate(cases, 1):
        a, b = (c["B"], c["A"]) if swapped else (c["A"], c["B"])
        lines.append(f"{k}. {c['question']}\n   A: {a}\n   B: {b}")
        order.append(c["id"])
    return "\n\n".join(lines), order


def guard(text: str, cases: list[dict]) -> None:
    for c in cases:
        for leak in [c["id"], c["unit"], c.get("time", "")[:16], *(h[:7] for h in c.get("commits", []))]:
            if leak and leak in text:
                raise RuntimeError(f"the payload carries {leak!r} of {c['id']}")


def check_answers(raw, n: int) -> tuple[dict, list[str]]:
    if not isinstance(raw, dict) or not isinstance(raw.get("answers"), list):
        return raw, ["answers must be a list"]
    got, errs = {}, []
    for a in raw["answers"]:
        k = a.get("case") if isinstance(a, dict) else None
        if not isinstance(k, int) or not 1 <= k <= n:
            errs.append(f"case {k!r} is not in the list")
            continue
        if k in got:
            errs.append(f"case {k} answered twice")
        if a.get("choice") not in CHOICES:
            errs.append(f"case {k}: choice must be one of {CHOICES}")
        got[k] = a
    missing = [k for k in range(1, n + 1) if k not in got]
    if missing:
        errs.append(f"cases not answered: {missing[:20]}")
    return raw, errs


class Runner:
    def __init__(self, args, cli, record):
        self.args, self.cli, self.record = args, cli, record

    def ask(self, template: str, statement: str | None, cases: list[dict], swapped: bool, label: str) -> dict[str, str]:
        """Choices per case id, mapped back to the original order of the options."""
        text, order = payload(cases, swapped)
        guard(text, cases)
        prompt = template.replace("{principle}", statement or "").replace(PLACEHOLDER, text)
        if "{principle}" in template and not statement:
            raise RuntimeError("a principle prompt without a principle")
        ans, attempts = pc.ask(self.cli, prompt, self.args, lambda raw: check_answers(raw, len(cases)), f"{label}: ")
        self.record.append({"label": label, "swapped": swapped, "order": order, "payload_sha256": pc.sha256_bytes(prompt.encode()),
                            "payload": prompt, "attempts": attempts, "answer": ans})
        if ans is None:
            raise RuntimeError(f"{label}: no answer passed the checks")
        out = {}
        for a in ans["answers"]:
            ch = a["choice"]
            if swapped and ch in ("A", "B"):
                ch = "B" if ch == "A" else "A"
            out[order[a["case"] - 1]] = ch
        return out

    def both(self, template, statement, cases, label, single: bool) -> dict[str, str]:
        """The stable choice per case (A, B, NEITHER), or 'unstable'."""
        if single:
            o, s = {}, {}
            for c in cases:
                o.update(self.ask(template, statement, [c], False, f"{label}:{c['id']}:orig"))
                s.update(self.ask(template, statement, [c], True, f"{label}:{c['id']}:swap"))
        else:
            o = self.ask(template, statement, cases, False, f"{label}:orig")
            s = self.ask(template, statement, cases, True, f"{label}:swap")
        return {cid: (o[cid] if o[cid] == s[cid] else "unstable") for cid in o}


def score(stable: dict[str, str], cases: dict) -> dict:
    n = len(stable)
    applicable = [cid for cid, ch in stable.items() if ch in ("A", "B")]
    correct = sum(1 for cid in applicable if stable[cid] == cases[cid]["actual"])
    return {"n": n, "applicable": len(applicable), "neither": sum(ch == "NEITHER" for ch in stable.values()),
            "unstable": sum(ch == "unstable" for ch in stable.values()), "correct": correct,
            "incorrect": len(applicable) - correct, "coverage": ratio(len(applicable), n),
            "accuracy": ratio(correct, len(applicable)), "wilson95": wilson(correct, len(applicable))}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", type=Path, default=VALIDATION / "decision_cases.jsonl")
    ap.add_argument("--eligibility", type=Path, default=VALIDATION / "eligibility.jsonl")
    ap.add_argument("--exposure", type=Path, nargs="*", default=None, help="default: every exposure_*.jsonl of the validation folder")
    ap.add_argument("--dates", type=Path, default=VALIDATION / "principle_dates.json")
    ap.add_argument("--statements", type=Path, default=None,
                    help="statements.json of eligible_cases --candidates: score candidates instead of the principles in force")
    ap.add_argument("--output-dir", type=Path, default=VALIDATION / "runs")
    ap.add_argument("--baseline-prompt", type=Path, default=BASELINE_PROMPT)
    ap.add_argument("--include-possible", action="store_true", help="sensitivity: add the cases judged possibly exposed")
    ap.add_argument("--seed", type=int, default=20261011)
    ap.add_argument("--subset", type=int, default=10, help="cases run one per call to check the batched answers (D10)")
    ap.add_argument("--agreement", type=float, default=0.9, help="the agreement the batched run must reach (D10)")
    ap.add_argument("--mode", choices=("auto", "batch", "single"), default="auto")
    ap.add_argument("--stamp", default=None, help="the run's name; default the UTC time (fixed only to test or reproduce a name)")
    pc.common_args(ap, PRINCIPLE_PROMPT)
    args = ap.parse_args(argv)

    for p in (args.prompt, args.baseline_prompt):
        t = p.read_text(encoding="utf-8")
        if PLACEHOLDER not in t:
            print(f"ERROR: {p.name} has no {PLACEHOLDER}", file=sys.stderr)
            return 2
    template, base_template = args.prompt.read_text(encoding="utf-8"), args.baseline_prompt.read_text(encoding="utf-8")
    exposure = [r for p in (args.exposure or sorted(VALIDATION.glob("exposure_*.jsonl"))) for r in load_jsonl(p)]
    cases, pairs = select(load_jsonl(args.cases), load_jsonl(args.eligibility), exposure, args.include_possible)
    src = (json.loads(args.statements.read_text(encoding="utf-8"))["candidates"] if args.statements
           else json.loads(args.dates.read_text(encoding="utf-8"))["principles"])
    statements = {pid: d["statement"] for pid, d in src.items()}
    main_pairs = {p: [c for c in cids if cases[c]["decided_by"] in MAIN_DECIDERS] for p, cids in pairs.items()}
    print("approved usable cases:", len(cases), "| cases per principle:",
          ", ".join(f"{p} {len(v)}" for p, v in sorted(main_pairs.items(), key=lambda kv: int(kv[0][1:]))) or "none")
    if not any(main_pairs.values()):
        print("nothing to score: no approved, eligible, unexposed case", file=sys.stderr)
        return 1
    if args.dry_run:
        return 0
    stamp = args.stamp or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    cli, model, agent = pc.resolve(args)
    out = args.output_dir / f"{stamp}_temporal_principles_{model}"
    if out.with_suffix(".json").exists():
        print(f"ERROR: {out.name} exists", file=sys.stderr)
        return 2
    record: list[dict] = []
    run = Runner(args, cli, record)
    rng = random.Random(args.seed)
    shuffled = {p: rng.sample(cids, len(cids)) for p, cids in pairs.items() if cids}

    # D10: the batched answers against single calls, before any outcome is looked at
    single = args.mode == "single"
    agreement = None
    if args.mode == "auto":
        pool = [(p, c) for p, cids in sorted(shuffled.items()) for c in cids]
        check = rng.sample(pool, min(args.subset, len(pool)))
        batched = {p: run.ask(template, statements[p], [cases[c] for c in shuffled[p]], False, f"{p}:check-batch")
                   for p in {p for p, _ in check}}
        same = sum(batched[p][c] == run.ask(template, statements[p], [cases[c]], False, f"{p}:check-single:{c}")[c] for p, c in check)
        agreement = ratio(same, len(check))
        single = agreement is not None and agreement < args.agreement
        print(f"D10: {same}/{len(check)} single answers agree with the batched ones; running " + ("one case per call" if single else "batched"))

    stable = {p: run.both(template, statements[p], [cases[c] for c in cids], p, single) for p, cids in sorted(shuffled.items())}
    every = sorted({c for cids in shuffled.values() for c in cids})
    b0 = run.both(base_template, None, [cases[c] for c in every], "B0", single)
    eligible_for = defaultdict(set)
    for p, cids in pairs.items():
        for c in cids:
            eligible_for[c].add(p)
    unrelated = {c: rng.choice(sorted(set(statements) - eligible_for[c] or set(statements))) for c in every}
    b1 = {}
    for u in sorted(set(unrelated.values())):
        group = [cases[c] for c in every if unrelated[c] == u]
        b1.update(run.both(template, statements[u], group, f"B1:{u}", single))
    ids = sorted(statements, key=lambda p: (len(p), p))
    perm = ids[:]
    while len(ids) > 1 and any(a == b for a, b in zip(ids, perm)):
        rng.shuffle(perm)
    derange = dict(zip(ids, perm))
    b2 = {p: run.both(template, statements[derange[p]], [cases[c] for c in cids], f"B2:{p}<-{derange[p]}", single)
          for p, cids in sorted(shuffled.items())}

    results = {}
    for p, cids in sorted(main_pairs.items(), key=lambda kv: int(kv[0][1:])):
        if not cids:
            continue
        mine = {c: stable[p][c] for c in cids}
        outcomes = {"picked_chosen": 0, "lost_conflict": 0, "against_all": 0, "neither": 0, "unstable": 0}
        for c in cids:
            ch, actual = mine[c], cases[c]["actual"]
            if ch == "unstable":
                outcomes["unstable"] += 1
            elif ch == "NEITHER":
                outcomes["neither"] += 1
            elif ch == actual:
                outcomes["picked_chosen"] += 1
            elif any(stable[q].get(c) == actual for q in stable if q != p):
                outcomes["lost_conflict"] += 1
            else:
                outcomes["against_all"] += 1
        results[p] = {"target": score(mine, cases), "outcomes": outcomes, "B0": score({c: b0[c] for c in cids}, cases),
                      "B1": score({c: b1[c] for c in cids}, cases), "B2": score({c: b2[p][c] for c in cids}, cases)}
    conflicts = []
    for c in every:
        votes = {p: stable[p][c] for p in stable if c in stable[p] and stable[p][c] in ("A", "B")}
        for p in votes:
            for q in votes:
                if p < q and votes[p] != votes[q]:
                    conflicts.append({"case": c, "pair": [p, q], "chosen": cases[c]["actual"], p: votes[p], q: votes[q]})
    reversals = [{"case": c, "actual": cases[c]["actual"], "reverses": cases[c].get("reverses", []),
                  "reversed_by": cases[c].get("reversed_by", []), "votes": {p: stable[p][c] for p in stable if c in stable[p]}}
                 for c in every if cases[c].get("reverses") or cases[c].get("reversed_by")]
    margin = {p: score({c: stable[p][c] for c in cids if cases[c]["decided_by"] == "model_margin"}, cases)
              for p, cids in pairs.items() if any(cases[c]["decided_by"] == "model_margin" for c in cids)}

    report = {"version": VERSION, "date": stamp, "model": model, "agent": agent, "effort": args.effort,
              "cli_version": link_ideas.cli_version(cli), "seed": args.seed, "mode": "single" if single else "batch",
              "d10_agreement": agreement, "include_possible": args.include_possible,
              "prompts": {"principle": pc.sha256_bytes(args.prompt.read_bytes()), "baseline": pc.sha256_bytes(args.baseline_prompt.read_bytes())},
              "inputs": {pc.rel(p): pc.sha256_bytes(p.read_bytes()) for p in (args.cases, args.eligibility, args.dates)},
              "b2_derangement": derange, "results": results, "model_margin": margin, "conflicts": conflicts,
              "reversals": reversals, "calls": record}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    fmt = lambda s: (f"{s['accuracy']:.2f} [{s['wilson95'][0]:.2f}, {s['wilson95'][1]:.2f}]" if s["accuracy"] is not None else "null")
    L = [f"# Principles against the decisions, {stamp}", "",
         f"Written by `scripts/validate_principles_temporal.py` ({VERSION}); model {model}, effort {args.effort}; mode "
         f"{'one case per call' if single else 'batched'}" + (f" (D10 agreement {agreement})" if agreement is not None else "")
         + ("; cases judged possibly exposed included (sensitivity)" if args.include_possible else "") + ".",
         "Accuracy is over the cases where the answer was A or B in both orders; the interval is Wilson's at 95%.", "",
         "| principle | n | coverage | picked chosen | lost a conflict | against all | neither | unstable | accuracy | B0 | B1 | B2 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p, r in results.items():
        o, t = r["outcomes"], r["target"]
        L.append(f"| {p} | {t['n']} | {t['coverage']} | {o['picked_chosen']} | {o['lost_conflict']} | {o['against_all']} | "
                 f"{o['neither']} | {o['unstable']} | {fmt(t)} | {fmt(r['B0'])} | {fmt(r['B1'])} | {fmt(r['B2'])} |")
    L += ["", f"## Conflicts ({len(conflicts)})", ""]
    L += [f"- {x['case']}: {x['pair'][0]} {x[x['pair'][0]]}, {x['pair'][1]} {x[x['pair'][1]]}; chosen {x['chosen']}" for x in conflicts] or ["none"]
    L += ["", f"## Reversals ({len(reversals)})", ""]
    L += [f"- {x['case']}: chosen {x['actual']}; " + ", ".join(f"{p} {v}" for p, v in x["votes"].items()) for x in reversals] or ["none"]
    if margin:
        L += ["", "## Decisions the model took on its own (apart)", ""]
        L += [f"- {p}: n {s['n']}, accuracy {fmt(s)}" for p, s in margin.items()]
    out.with_suffix(".md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written: {out}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
