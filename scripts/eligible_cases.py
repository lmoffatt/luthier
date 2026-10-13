#!/usr/bin/env python3
"""Temporal eligibility of the decision units for each principle (step 3 of
record/plan/principles/plan-principles-validation-2026-10-09-execution.md). Mechanical, no model.

A pair (unit, principle) is eligible when the unit's time is after the principle's explicit date and
before the principle became operative for the agent of that unit: the earliest of the first commit
putting it in the CLAUDE.md of the session's repository, its entry in that account's global
CLAUDE.md, and the memory notes of that account and repository that Luciano marked as stating it.
A unit exactly at a boundary is not eligible. Luciano's marks are read from
`record/validation/principle_dates.md` (`ok`, `earlier <row id>`, `memory <note.md>`); a principle
without a mark stops the script, unless --provisional, which marks every output as provisional.

For each eligible pair, the share of the principle's terms that appear in the session's earlier
turns is stored as a flag, with the turns where most of them are (D3): it points at turns worth
reading and decides nothing.

Writes `record/validation/eligibility.jsonl` (every pair, with its verdict and reason),
`draft_candidates.json` (the units eligible for some principle, and every reversal, without the
units withheld for private words) and `eligibility.md`.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

VERSION = "eligible_cases v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATION = REPO_ROOT / "record" / "validation"
IACHAT = Path.home() / "Projects" / "IA_chat"
ACCOUNTS = [Path.home() / ".claude", Path.home() / ".claude-databaum"]
STOP = set("the a an of to in is and or for on it be by as at that this with not are its from what his he no one "
           "de la el en y que los las un una es no se por con para lo su al del como".split())


def pc_rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def when(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(timezone.utc)


def terms(text: str) -> set[str]:
    t = unicodedata.normalize("NFKD", str(text).lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z]{4,}", t) if w not in STOP}


def read_marks(md: Path) -> dict[str, str]:
    marks, cur = {}, None
    for line in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (P\d+)\b", line)
        if m:
            cur = m.group(1)
        elif cur and line.startswith("Mark:"):
            marks[cur] = line[len("Mark:"):].strip()
    return marks


def parse_mark(text: str) -> tuple[str | None, list[str], list[str]]:
    """(earlier row id or None, memory note names, problems)."""
    earlier, notes, problems = None, [], []
    for tok in [t.strip() for t in text.split(";") if t.strip()]:
        low = tok.lower()
        if low == "ok":
            continue
        if low.startswith("earlier "):
            earlier = tok.split(None, 1)[1].strip("` ")
        elif low.startswith("memory "):
            notes += [n.strip("` ") for n in tok.split(None, 1)[1].split(",") if n.strip()]
        else:
            problems.append(f"cannot read the mark {tok!r}")
    return earlier, notes, problems


def resolve_dates(dates: dict, marks: dict[str, str], rows_by_id: dict, provisional: bool) -> tuple[dict, list[str]]:
    """Per principle: explicit (datetime) and a function of (account, repo) giving the operative datetime or None."""
    out, problems = {}, []
    for pid, d in dates.items():
        mark = marks.get(pid, "")
        if not mark and not provisional:
            problems.append(f"{pid}: no mark")
            continue
        earlier, notes, pr = parse_mark(mark or "ok")
        problems += [f"{pid}: {p}" for p in pr]
        explicit = when(d["explicit"]) if d.get("explicit") else None
        if earlier:
            row = rows_by_id.get(earlier)
            if row is None or not row.get("time_utc"):
                problems.append(f"{pid}: earlier row {earlier!r} is not in the timeline")
            else:
                explicit = when(row["time_utc"])
        listed = {(n["note"], n["account"], repo): n["first_written"]
                  for repo, o in d["operative"].items() for n in o.get("memory_candidates", [])}
        for n in notes:
            if not any(k[0] == n for k in listed):
                problems.append(f"{pid}: memory note {n!r} is not among the listed candidates")
        op = {}
        for repo, o in d["operative"].items():
            for acct in ("1", "2"):
                ts = []
                if o.get("claude_md"):
                    ts.append(when(o["claude_md"]["time"]))
                if acct in (d.get("global_claude_md") or {}):
                    ts.append(when(d["global_claude_md"][acct]["time"]))
                ts += [when(t) for (n, a, r), t in listed.items() if n in notes and str(a) == acct and r == repo]
                op[(acct, repo)] = min(ts) if ts else None
        out[pid] = {"explicit": explicit, "operative": op, "earlier": earlier, "notes": notes, "mark": mark,
                    "statement": d["statement"]}
    return out, problems


def transcript_path(source: str) -> Path:
    m = re.match(r"\[account (\d+)\]/(.*)", source)
    if m:
        return ACCOUNTS[int(m.group(1)) - 1] / m.group(2)
    p = Path(source)
    return p if p.is_absolute() else IACHAT / p


def session_turns(path: Path) -> list[tuple[int, str]]:
    """(line, text) of every typed or written turn of a session, tool output left out."""
    opener = gzip.open if path.suffix == ".gz" else open
    out = []
    with opener(path, "rt", encoding="utf-8") as fh:
        for n, l in enumerate(fh, 1):
            try:
                ev = json.loads(l)
            except json.JSONDecodeError:
                continue
            c = ev.get("message", {}).get("content") if isinstance(ev.get("message"), dict) else None
            if isinstance(c, str):
                out.append((n, c))
            elif isinstance(c, list):
                txt = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
                if txt.strip():
                    out.append((n, txt))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--units", type=Path, default=VALIDATION / "decision_units.jsonl")
    ap.add_argument("--dates", type=Path, default=VALIDATION / "principle_dates.json")
    ap.add_argument("--marks", type=Path, default=VALIDATION / "principle_dates.md")
    ap.add_argument("--timeline", type=Path, default=REPO_ROOT / "record" / "ideas" / "timeline.jsonl")
    ap.add_argument("--output-dir", type=Path, default=VALIDATION)
    ap.add_argument("--flag-share", type=float, default=0.6,
                    help="share of the principle's terms in the session's earlier turns that raises the lexical flag")
    ap.add_argument("--provisional", action="store_true", help="read a principle without a mark as ok, and say so")
    ap.add_argument("--candidates", type=Path, default=None,
                    help="a find_principles output: score its candidates instead of the principles of principle_dates")
    ap.add_argument("--after", default=None,
                    help="only units after this UTC time are eligible (a cutoff: what the candidates were found from ends here)")
    ap.add_argument("--match", type=Path, default=None,
                    help="the match_principles output for those candidates: a candidate covered by or extending a principle "
                         "in force inherits its operative dates")
    args = ap.parse_args(argv)

    units = [json.loads(l) for l in args.units.read_text(encoding="utf-8").splitlines() if l.strip()]
    dates = json.loads(args.dates.read_text(encoding="utf-8"))["principles"]
    rows_by_id = {}
    if args.timeline.exists():
        for l in args.timeline.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                rows_by_id[r["id"]] = r
    marks = read_marks(args.marks) if args.marks.exists() else {}
    if args.candidates:
        # the principles in force only lend their operative dates; unmarked ones are read as proposed
        inforce, _ = resolve_dates(dates, marks, rows_by_id, provisional=True)
        found = json.loads(args.candidates.read_text(encoding="utf-8"))
        match = {m["candidate"]: m for m in (json.loads(args.match.read_text(encoding="utf-8"))["answer"]["matches"]
                                              if args.match else [])}
        resolved, problems, statements = {}, [], {}
        for c in found["answer"]["candidates"]:
            row = rows_by_id.get(c["quote_row"])
            if row is None or not row.get("time_utc"):
                problems.append(f"{c['id']}: its quote row {c['quote_row']} has no time in the timeline")
                continue
            m = match.get(c["id"], {})
            heir = m.get("principle") if m.get("verdict") in ("covered", "extends") else None
            op = inforce[heir]["operative"] if heir in inforce else {}
            resolved[c["id"]] = {"explicit": when(row["time_utc"]), "operative": defaultdict(lambda: None, op), "earlier": None,
                                 "notes": [], "mark": f"candidate; inherits {heir}" if heir else "candidate", "statement": c["statement"]}
            statements[c["id"]] = {"statement": c["statement"], "quote": c["quote"], "explicit": row["time_utc"], "inherits": heir}
        dates = {cid: {"statement": v["statement"], "quote": v["quote"]} for cid, v in statements.items()}
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "statements.json").write_text(json.dumps({"from": pc_rel(args.candidates), "candidates": statements},
                                                                    ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    else:
        resolved, problems = resolve_dates(dates, marks, rows_by_id, args.provisional)
    if problems:
        print("ERROR: the dates are not ready:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 2

    pairs, cache = [], {}
    for u in units:
        t, acct, repo = when(u["time"]), str(u.get("account", 1)), u.get("session_repo", "")
        for pid, r in resolved.items():
            op = r["operative"].get((acct, repo))
            if r["explicit"] is None:
                ok, why = False, "no explicit date"
            elif args.after and not t > when(args.after):
                ok, why = False, "before the cutoff"
            elif not t > r["explicit"]:
                ok, why = False, "before the principle was formulated"
            elif op is not None and not t < op:
                ok, why = False, "after the principle was operative for this account and repository"
            else:
                ok, why = True, "between formulation and operation"
            pair = {"unit": u["id"], "principle": pid, "eligible": ok, "reason": why, "account": int(acct), "repo": repo,
                    "explicit": r["explicit"].strftime("%Y-%m-%dT%H:%MZ") if r["explicit"] else None,
                    "operative": op.strftime("%Y-%m-%dT%H:%MZ") if op else None}
            if ok:
                src = u["source"]
                if src not in cache:
                    try:
                        cache[src] = session_turns(transcript_path(src))
                    except OSError:
                        cache[src] = None
                want = terms(r["statement"] + " " + dates[pid].get("quote", ""))
                turns = cache[src]
                if turns is None or not want:
                    pair["lexical_exposure"] = None
                else:
                    earlier = [(n, terms(x) & want) for n, x in turns if n < u["luciano"]["line"]]
                    seen = set().union(*(s for _, s in earlier)) if earlier else set()
                    share = len(seen) / len(want)
                    top = sorted(earlier, key=lambda e: -len(e[1]))[:3]
                    pair["lexical_exposure"] = {"share": round(share, 2), "flag": share >= args.flag_share,
                                                "lines": [n for n, s in top if s]}
            pairs.append(pair)

    by_unit = defaultdict(list)
    for p in pairs:
        if p["eligible"]:
            by_unit[p["unit"]].append(p["principle"])
    cands = []
    for u in units:
        reasons = []
        if by_unit.get(u["id"]):
            reasons.append("eligible for " + ", ".join(by_unit[u["id"]]))
        if u.get("reverses") or u.get("reversed_by"):
            reasons.append("reversal")
        if reasons and "withheld" not in u:
            cands.append({"unit": u["id"], "reasons": reasons, "eligible_for": by_unit.get(u["id"], [])})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = {"version": VERSION, "provisional": args.provisional, "flag_share": args.flag_share, "after": args.after}
    (args.output_dir / "eligibility.jsonl").write_text("".join(json.dumps({**p, **stamp}, sort_keys=True) + "\n" for p in pairs),
                                                       encoding="utf-8")
    (args.output_dir / "draft_candidates.json").write_text(json.dumps({**stamp, "candidates": cands}, indent=1) + "\n",
                                                           encoding="utf-8")
    per = Counter((p["principle"], p["account"], p["repo"]) for p in pairs if p["eligible"])
    flagged = Counter(p["principle"] for p in pairs if p["eligible"] and (p.get("lexical_exposure") or {}).get("flag"))
    L = [f"# Eligibility of the decision units, {datetime.now(timezone.utc):%Y-%m-%d}", "",
         f"Written by `scripts/eligible_cases.py` ({VERSION}), no model." + (" PROVISIONAL: unmarked principles read as ok." if args.provisional else ""),
         f"A pair is eligible when the unit falls after the principle's explicit date and before it was operative for that",
         f"account and repository. The lexical flag (share of the principle's terms already in the session, at least {args.flag_share:.0%})",
         "points at turns to read; it decides nothing.", "",
         f"Units: {len(units)}; candidates for drafting: {len(cands)} (eligible for some principle, or a reversal; withheld units left out).", "",
         "| principle | account | repository | eligible units | lexically flagged |", "|---|---|---|---|---|"]
    for (pid, a, repo), n in sorted(per.items(), key=lambda kv: (int(kv[0][0][1:]), kv[0][1], kv[0][2])):
        L.append(f"| {pid} | {a} | {repo} | {n} | {sum(1 for p in pairs if p['eligible'] and p['principle'] == pid and p['account'] == a and p['repo'] == repo and (p.get('lexical_exposure') or {}).get('flag'))} |")
    none = [pid for pid in resolved if not any(k[0] == pid for k in per)]
    L += ["", f"Principles with no eligible unit: {', '.join(none) or 'none'}."]
    (args.output_dir / "eligibility.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{sum(p['eligible'] for p in pairs)} eligible pairs; {len(cands)} candidates for drafting"
          + (" (provisional)" if args.provisional else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
