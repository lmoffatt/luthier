#!/usr/bin/env python3
"""Draft one decision case per candidate unit (step 4 of
record/plan-principles-validation-2026-10-09-execution.md).

For each unit of `draft_candidates.json`, the script assembles the moment from the transcript and
git: the model's text before Luciano's turn, his turn, the model's text after it, and what changed
(each commit's diff, and the edits the agent made), each cut to a parameter's length. It runs the
prompt `prompts/draft_decision_case_v1.md`, isolated, one call per unit. The drafter never sees a
principle, a date, or another unit.

The answer is checked before it is accepted: the fields and their values, two distinct options,
every evidence quote verbatim in the material (words only, an ellipsis for skipped words), an empty
counterfactual evidence only for a constructed alternative. A rejected answer is asked again with its
errors. The options are then labelled A and B by a draw seeded with --seed and the unit's id, so the
drafter never labels them. Every case starts with `approved: false`.

A unit whose material carries a word of `scripts/export_chat.private` is not sent and is recorded as
skipped (D6). Idempotent: a unit already drafted with this prompt is skipped (unless --force).

Writes `record/validation/decision_cases.jsonl` (one case per unit, the non-decisions included,
marked) and `record/validation/draft_runs.jsonl` (per unit: the material's sha256, every attempt and
raw answer). Run by the model with Luciano's authorization (D11).
"""
from __future__ import annotations

import argparse
import gzip
import json
import random
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_ideas  # noqa: E402
import principles_common as pc  # noqa: E402
import eligible_cases as ec  # noqa: E402

VERSION = "draft_cases v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATION = REPO_ROOT / "record" / "validation"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "draft_decision_case_v1.md"
PRIVATE = REPO_ROOT / "scripts" / "export_chat.private"
PLACEHOLDER = "<<<INPUT>>>"
STATUSES = ("explicitly_discussed", "strongly_implied", "constructed")
DECIDERS = ("luciano_choice", "luciano_confirmation", "model_margin")
REPOS = {"luthier": Path.home() / "Projects" / "luthier", "sonolocalizacion": Path.home() / "Projects" / "sonolocalizacion"}


def parse_args(argv: list[str]):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--candidates", type=Path, default=VALIDATION / "draft_candidates.json")
    p.add_argument("--units", type=Path, default=VALIDATION / "decision_units.jsonl")
    p.add_argument("--output-dir", type=Path, default=VALIDATION)
    p.add_argument("--seed", type=int, default=20261009, help="the draw of A and B")
    p.add_argument("--text-chars", type=int, default=3000, help="each turn is cut to this length")
    p.add_argument("--diff-chars", type=int, default=6000, help="what changed is cut to this length")
    p.add_argument("--only", nargs="*", default=None, help="only these unit ids")
    p.add_argument("--limit", type=int, default=0, help="draft at most this many units (0: all)")
    p.add_argument("--provisional-ok", action="store_true", help="accept candidates made from unmarked dates")
    pc.common_args(p, DEFAULT_PROMPT)
    return p.parse_args(argv)


def private_patterns() -> list[re.Pattern]:
    if not PRIVATE.exists():
        return []
    ws = [w.strip() for w in PRIVATE.read_text(encoding="utf-8").splitlines() if w.strip() and not w.startswith("#")]
    return [re.compile(r"(?<!\w)" + re.escape(unicodedata.normalize("NFC", w)) + r"(?!\w)", re.I) for w in ws]


def read_events(path: Path) -> dict[int, dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    out = {}
    with opener(path, "rt", encoding="utf-8") as fh:
        for n, l in enumerate(fh, 1):
            try:
                out[n] = json.loads(l)
            except json.JSONDecodeError:
                continue
    return out


def next_model_text(events: dict[int, dict], after: int, cap: int) -> str:
    texts = []
    for n in sorted(k for k in events if k > after):
        ev = events[n]
        c = ev.get("message", {}).get("content") if isinstance(ev.get("message"), dict) else None
        if ev.get("type") == "user" and (isinstance(c, str) or (isinstance(c, list) and any(
                isinstance(x, dict) and x.get("type") == "text" for x in c))):
            break
        if ev.get("type") == "assistant" and isinstance(c, list):
            texts += [x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text" and x.get("text", "").strip()]
            if texts:
                break
    return "\n".join(texts)[:cap]


def edits(events: dict[int, dict], lines: list[int]) -> list[str]:
    out = []
    for n in lines:
        ev = events.get(n, {})
        for x in ev.get("message", {}).get("content", []) or []:
            if isinstance(x, dict) and x.get("type") == "tool_use" and x.get("name") in ("Edit", "Write", "MultiEdit"):
                inp = x.get("input", {}) or {}
                f = Path(inp.get("file_path", "")).name
                if x["name"] == "Write":
                    out.append(f"[write {f}]\n{inp.get('content', '')}")
                else:
                    out.append(f"[edit {f}]\n- {inp.get('old_string', '')}\n+ {inp.get('new_string', '')}")
    return out


def commit_diff(c: dict) -> str:
    repo = REPOS.get(c.get("repo", ""))
    if not repo:
        return ""
    r = subprocess.run(["git", "-C", str(repo), "show", "--stat", "--patch", "--format=commit %h %s", c["hash"]],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def material(u: dict, cap_text: int, cap_diff: int) -> str:
    events = read_events(ec.transcript_path(u["source"]))
    changed = [commit_diff(c) for c in u.get("commits", [])] + edits(events, [a["line"] for a in u.get("actions", [])])
    parts = ["[MODEL BEFORE]", ((u.get("proposal") or {}).get("text") or "(nothing)")[-cap_text:],
             "[LUCIANO]", u["luciano"]["text"][:cap_text],
             "[MODEL AFTER]", next_model_text(events, u["luciano"]["line"], cap_text) or "(nothing)",
             "[WHAT CHANGED]", ("\n\n".join(x for x in changed if x) or "(no file content recorded)")[:cap_diff]]
    return "\n\n".join(parts)


def check(ans: dict, mat: str) -> list[str]:
    if not isinstance(ans, dict):
        return ["the answer is not a JSON object"]
    if ans.get("is_decision") is False:
        return [] if str(ans.get("reason_if_not", "")).strip() else ["reason_if_not is empty"]
    if ans.get("is_decision") is not True:
        return ["is_decision must be true or false"]
    e = []
    alts = ans.get("alternatives")
    if not (isinstance(alts, list) and len(alts) == 2 and all(str(a).strip() for a in alts)):
        e.append("alternatives must be two non-empty strings")
    elif pc.words(alts[0]) == pc.words(alts[1]):
        e.append("the two alternatives are the same")
    if ans.get("chosen_index") not in (0, 1):
        e.append("chosen_index must be 0 or 1")
    if not str(ans.get("question", "")).strip():
        e.append("question is empty")
    if ans.get("counterfactual_status") not in STATUSES:
        e.append(f"counterfactual_status must be one of {STATUSES}")
    if ans.get("decided_by") not in DECIDERS:
        e.append(f"decided_by must be one of {DECIDERS}")
    for field in ("evidence_chosen", "evidence_decided_by", "evidence_counterfactual"):
        q = str(ans.get(field, "")).strip()
        if not q:
            if field != "evidence_counterfactual" or ans.get("counterfactual_status") != "constructed":
                e.append(f"{field} is empty")
        elif not pc.quote_in(q, mat):
            e.append(f"{field} is not in the material: \"{q[:80]}\"")
    return e


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    cands = json.loads(args.candidates.read_text(encoding="utf-8"))
    if cands.get("provisional") and not args.provisional_ok:
        print("ERROR: the candidates come from unmarked dates (provisional); mark the dates or pass --provisional-ok",
              file=sys.stderr)
        return 2
    template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"ERROR: the prompt has no {PLACEHOLDER}", file=sys.stderr)
        return 2
    prompt_sha = pc.sha256_bytes(args.prompt.read_bytes())
    units = {u["id"]: u for u in map(json.loads, args.units.read_text(encoding="utf-8").splitlines()) if u}
    out_cases, out_runs = args.output_dir / "decision_cases.jsonl", args.output_dir / "draft_runs.jsonl"
    done = set()
    if out_cases.exists() and not args.force:
        for l in out_cases.read_text(encoding="utf-8").splitlines():
            c = json.loads(l)
            if c.get("drafted", {}).get("prompt_sha256") == prompt_sha:
                done.add(c["unit"])
    todo = [c for c in cands["candidates"] if c["unit"] not in done and (not args.only or c["unit"] in args.only)]
    if args.limit:
        todo = todo[:args.limit]
    print(f"candidates: {len(cands['candidates'])} | drafted with this prompt: {len(done)} | to draft: {len(todo)}")
    if args.dry_run:
        for c in todo:
            print(f"  {c['unit']}: {'; '.join(c['reasons'])}")
        return 0
    try:
        cli, model, agent = pc.resolve(args)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    priv = private_patterns()
    version = link_ideas.cli_version(cli)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.force and out_cases.exists():  # redo only the units drafted now; keep the others
        again = {c["unit"] for c in todo}
        keep = [l for l in out_cases.read_text(encoding="utf-8").splitlines() if json.loads(l)["unit"] not in again]
        out_cases.write_text("".join(l + "\n" for l in keep), encoding="utf-8")
    with out_cases.open("a", encoding="utf-8") as fc, out_runs.open("a", encoding="utf-8") as fr:
        for i, c in enumerate(todo, 1):
            u = units.get(c["unit"])
            if u is None:
                print(f"[{i}/{len(todo)}] {c['unit']}: not among the units", file=sys.stderr)
                continue
            mat = material(u, args.text_chars, args.diff_chars)
            base = {"id": f"C-{u['id']}", "unit": u["id"], "time": u["time"], "account": u.get("account"),
                    "session_repo": u.get("session_repo"), "areas": u.get("areas"), "eligible_for": c.get("eligible_for", []),
                    "reverses": u.get("reverses", []), "reversed_by": u.get("reversed_by", []),
                    "commits": [x["hash"] for x in u.get("commits", [])], "approved": False,
                    "drafted": {"version": VERSION, "prompt": args.prompt.stem, "prompt_sha256": prompt_sha, "model": model,
                                "effort": args.effort, "cli_version": version, "seed": args.seed,
                                "material_sha256": pc.sha256_bytes(mat.encode()),
                                "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}}
            if any(p.search(unicodedata.normalize("NFC", mat)) for p in priv):
                fc.write(json.dumps({**base, "is_decision": None, "skipped": "private words in the material"}, ensure_ascii=False) + "\n")
                print(f"[{i}/{len(todo)}] {u['id']}: skipped, private words in the material")
                continue
            ans, attempts = pc.ask(cli, template.replace(PLACEHOLDER, mat), args, lambda raw: (raw, check(raw, mat)), f"{u['id']}: ")
            fr.write(json.dumps({"unit": u["id"], "material_sha256": base["drafted"]["material_sha256"], "attempts": attempts},
                                ensure_ascii=False) + "\n")
            if ans is None:
                print(f"[{i}/{len(todo)}] {u['id']}: no answer passed the checks", file=sys.stderr)
                continue
            if not ans.get("is_decision"):
                case = {**base, "is_decision": False, "reason_if_not": ans.get("reason_if_not", "")}
            else:
                swap = random.Random(f"{args.seed}:{u['id']}").random() < 0.5
                alts = ans["alternatives"][::-1] if swap else ans["alternatives"]
                chosen = 1 - ans["chosen_index"] if swap else ans["chosen_index"]
                case = {**base, "is_decision": True, "question": ans["question"], "A": alts[0], "B": alts[1],
                        "actual": "AB"[chosen], "counterfactual_status": ans["counterfactual_status"],
                        "decided_by": ans["decided_by"],
                        "evidence": {"chosen": ans["evidence_chosen"], "counterfactual": ans.get("evidence_counterfactual", ""),
                                     "decided_by": ans["evidence_decided_by"]}}
            fc.write(json.dumps(case, ensure_ascii=False) + "\n")
            fc.flush()
            fr.flush()
            print(f"[{i}/{len(todo)}] {u['id']}: " + (f"{case['decided_by']}, {case['counterfactual_status']}" if case["is_decision"]
                                                      else f"no decision ({case['reason_if_not'][:60]})"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
