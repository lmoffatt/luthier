#!/usr/bin/env python3
"""Group the rows of the timeline of ideas into lineages: one idea each, with every row that states,
restates, refines, corrects, rejects, confirms or proposes it.

Reads `record/ideas/timeline.jsonl` (written by `ideas_timeline.py`) and runs the prompt
`prompts/link_ideas_v1.md` through the `claude` (or `codex`) command line, isolated: no tools, no
session, so an answer depends only on the prompt and what this script puts in it. The rows go in
time order, in windows of --window-chars; each window sees the lineages made so far and places its
rows in one of them, in a new one, or in the unplaced list with a reason. The same mechanism makes
the script incremental: run again after the timeline grows and only the new rows are placed.

Every answer is checked before it is accepted: each row of the window placed exactly once, no
foreign row, every lineage id known or newly defined, every relation in the vocabulary. A rejected
answer is asked again with the errors appended, up to --retries times; the errors and every attempt
are recorded. Who said an idea first, and whether a model's idea was adopted by Luciano, is
computed here from the times and the authors, never taken from the model.

Writes, under --output-dir (default record/ideas):
  lineages_<prompt>_<agent>_<model>.json   the state: lineages, placements, and every call with
                                            its input sha256, the raw answer, the attempts
  lineages_<prompt>_<agent>_<model>.md     for Luciano: counts, then each lineage with its rows

The state is saved after every call, so an interrupted run resumes. A state made with another
prompt version or model is not continued (--force starts over). Luciano runs this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

VERSION = "link_ideas v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_ID = "link_ideas_v1"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / f"{PROMPT_ID}.md"
DEFAULT_TIMELINE = REPO_ROOT / "record" / "ideas" / "timeline.jsonl"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "ideas"
DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5"
DEFAULT_EFFORT = "low"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
PLACEHOLDER = "<<<INPUT>>>"
RELATIONS = ("states", "restates", "refines", "corrects", "rejects", "confirms", "proposes", "questions")
SCOPES = ("language", "method", "other")
ID_RE = re.compile(r"^L-[a-z0-9]+(?:-[a-z0-9]+)*$")
ADOPTING = ("states", "restates", "refines", "confirms")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--timeline", type=Path, default=DEFAULT_TIMELINE)
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    p.add_argument("--var", action="append", default=[], metavar="KEY=VALUE",
                   help="fills {KEY} in the prompt (link_ideas_v2: --var language=... --var designers=...)")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto")
    p.add_argument("--model", default=None)
    p.add_argument("--agent", default=None)
    p.add_argument("--effort", choices=EFFORTS, default=DEFAULT_EFFORT, help="passed to claude; codex ignores it")
    p.add_argument("--window-chars", type=int, default=60000, help="largest block of rows sent in one call")
    p.add_argument("--max-output-tokens", type=int, default=0,
                   help="passed to claude as CLAUDE_CODE_MAX_OUTPUT_TOKENS (0: the CLI's default)")
    p.add_argument("--max-thinking-tokens", type=int, default=0,
                   help="passed to claude as MAX_THINKING_TOKENS, a cap on the model's reasoning (0: the CLI's default)")
    p.add_argument("--quote-chars", type=int, default=200, help="each row's quote is cut to this length in the prompt")
    p.add_argument("--max-calls", type=int, default=0, help="stop after this many calls (0: no limit)")
    p.add_argument("--retries", type=int, default=2, help="asks again when an answer fails the checks")
    p.add_argument("--timeout", type=float, default=1200.0)
    p.add_argument("--force", action="store_true", help="discard the state and start over")
    p.add_argument("--dry-run", action="store_true", help="say what would be sent; call no model")
    p.add_argument("--report-only", action="store_true", help="rewrite the Markdown from the state; call no model")
    return p.parse_args(argv)


# --- the model, isolated -------------------------------------------------------------------------

def resolve_cli(choice: str) -> str:
    for name in ((choice,) if choice != "auto" else ("claude", "codex")):
        if shutil.which(name):
            return name
    raise RuntimeError(f"{choice if choice != 'auto' else 'neither claude nor codex'} is not on the PATH")


def cli_version(cli: str) -> str:
    try:
        return subprocess.run([cli, "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:
        return ""


TOKEN_LIMIT_MARK = "output token maximum"


class OutputLimit(RuntimeError):
    """The CLI cut the answer at its output token limit; it says so in plain text, exit 0."""


def call(cli: str, prompt_text: str, model: str, effort: str, timeout: float, max_output_tokens: int = 0,
         max_thinking_tokens: int = 0) -> str:
    if cli == "claude":
        cmd = ["claude", "-p", "--model", model, "--effort", effort, "--output-format", "text",
               "--no-session-persistence", "--tools", ""]
    else:
        cmd = ["codex", "exec", "--skip-git-repo-check", "--color", "never", "--sandbox", "read-only", "-m", model, "-"]
    env = None
    if max_output_tokens or max_thinking_tokens:
        import os
        env = dict(os.environ)
        if max_output_tokens:
            env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(max_output_tokens)
        if max_thinking_tokens:
            env["MAX_THINKING_TOKENS"] = str(max_thinking_tokens)
    proc = subprocess.run(cmd, input=prompt_text, capture_output=True, text=True, timeout=timeout, env=env)
    text = (proc.stdout or "") + (proc.stderr or "")
    if TOKEN_LIMIT_MARK in text and "{" not in proc.stdout:
        raise OutputLimit(text.strip()[:300])
    if proc.returncode != 0:
        raise RuntimeError(text.strip() or f"{cli} failed")
    return proc.stdout


def parse_json(raw: str) -> dict:
    s, e = raw.find("{"), raw.rfind("}")
    if s < 0 or e <= s:
        raise ValueError("no JSON object in the answer")
    return json.loads(raw[s:e + 1])


# --- the input -------------------------------------------------------------------------------------

def load_timeline(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def clip(text: str, n: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n - 1].rstrip() + "…"


def row_line(r: dict, quote_chars: int, label: str | None = None) -> str:
    return (f"{label or r['id']} | {r.get('time_local', '')[:16]} | {r.get('who', '')} | {r.get('kind', 'idea')} | "
            f"{clip(r.get('what', ''), 300)} | \"{clip(r.get('quote', ''), quote_chars)}\"")


def lineage_line(lin: dict, first: str, n: int) -> str:
    return f"{lin['id']} | {lin['scope']} | {first} | {n} | {lin['statement']}"


def windows(rows: list[dict], window_chars: int, quote_chars: int) -> list[list[dict]]:
    out, cur, size = [], [], 0
    for r in rows:
        n = len(row_line(r, quote_chars)) + 1
        if cur and size + n > window_chars:
            out.append(cur)
            cur, size = [], 0
        cur.append(r)
        size += n
    if cur:
        out.append(cur)
    return out


def build_input(state: dict, by_id: dict, win: list[dict], quote_chars: int) -> str:
    members = defaultdict(list)
    for rid, a in state["assign"].items():
        if rid in by_id:
            members[a["lineage"]].append(by_id[rid])
    lines = ["## Existing lineages", ""]
    lins = sorted(state["lineages"].values(),
                  key=lambda l: (min((m.get("time_utc", "") for m in members[l["id"]]), default="~"), l["id"]))
    if not lins:
        lines.append("(none yet)")
    for lin in lins:
        ms = members[lin["id"]]
        first = min((m.get("time_local", "")[:10] for m in ms), default="")
        lines.append(lineage_line(lin, first, len(ms)))
    lines += ["", f"## Rows to place ({len(win)})", ""]
    lines += [row_line(r, quote_chars, f"r{i}") for i, r in enumerate(win, 1)]
    return "\n".join(lines) + "\n"


# --- the checks ------------------------------------------------------------------------------------

def expand(ans: dict, win: list[dict]) -> tuple[dict, list[str]]:
    """The compact answer (rows as r<n>, entries as lists) in the long form, with row ids."""
    if not isinstance(ans, dict):
        return ans, ["the answer is not a JSON object"]
    local = {f"r{i}": r["id"] for i, r in enumerate(win, 1)}
    errors, assign, unplaced = [], [], []
    for a in ans.get("assign", []) or []:
        if not (isinstance(a, list) and len(a) == 3):
            errors.append(f"assign entry {a!r} is not [r<n>, lineage, relation]")
            continue
        assign.append({"row": local.get(a[0], f"?{a[0]}"), "lineage": a[1], "relation": a[2]})
    for u in ans.get("unplaced", []) or []:
        if not (isinstance(u, list) and len(u) == 2):
            errors.append(f"unplaced entry {u!r} is not [r<n>, reason]")
            continue
        unplaced.append({"row": local.get(u[0], f"?{u[0]}"), "reason": str(u[1])})
    return {"new_lineages": ans.get("new_lineages", []) or [], "assign": assign, "unplaced": unplaced}, errors


def check_answer(ans: dict, state: dict, win: list[dict]) -> list[str]:
    errors: list[str] = []
    if not isinstance(ans, dict):
        return ["the answer is not a JSON object"]
    new = ans.get("new_lineages", []) or []
    assign = ans.get("assign", []) or []
    unplaced = ans.get("unplaced", []) or []
    known = set(state["lineages"])
    new_ids = []
    for l in new:
        lid = str(l.get("id", ""))
        if not ID_RE.match(lid):
            errors.append(f"new lineage id {lid!r} is not of the form L-<kebab-slug>")
        if lid in known or lid in new_ids:
            errors.append(f"new lineage id {lid} already exists")
        if l.get("scope") not in SCOPES:
            errors.append(f"{lid}: scope {l.get('scope')!r} is not one of {SCOPES}")
        if not str(l.get("statement", "")).strip():
            errors.append(f"{lid}: empty statement")
        new_ids.append(lid)
    ids = known | set(new_ids)
    window_ids = [r["id"] for r in win]
    seen = Counter()
    for a in assign:
        rid = a.get("row")
        seen[rid] += 1
        if a.get("lineage") not in ids:
            errors.append(f"row {label_of(rid, win)}: lineage {a.get('lineage')!r} is neither existing nor new")
        if a.get("relation") not in RELATIONS:
            errors.append(f"row {label_of(rid, win)}: relation {a.get('relation')!r} is not one of {RELATIONS}")
    for u in unplaced:
        seen[u.get("row")] += 1
        if not str(u.get("reason", "")).strip():
            errors.append(f"row {label_of(u.get('row'), win)}: unplaced without a reason")
    label = {r["id"]: f"r{i}" for i, r in enumerate(win, 1)}
    foreign = [str(r).lstrip("?") for r in seen if r not in set(window_ids)]
    missing = [label[r] for r in window_ids if seen[r] == 0]
    twice = [label[r] for r in window_ids if seen[r] > 1]
    if foreign:
        errors.append(f"row ids not in this window: {', '.join(map(str, foreign[:10]))}")
    if missing:
        errors.append(f"rows of the window not placed: {', '.join(missing[:20])}" + (f" and {len(missing) - 20} more" if len(missing) > 20 else ""))
    if twice:
        errors.append(f"rows placed more than once: {', '.join(twice[:10])}")
    return errors


def label_of(rid, win: list[dict]) -> str:
    for i, r in enumerate(win, 1):
        if r["id"] == rid:
            return f"r{i}"
    return str(rid).lstrip("?")


def apply_answer(ans: dict, state: dict, n_call: int) -> None:
    used = {a["lineage"] for a in ans.get("assign", [])}
    for l in ans.get("new_lineages", []):
        if l["id"] in used:
            state["lineages"][l["id"]] = {"id": l["id"], "scope": l["scope"], "statement": l["statement"].strip(),
                                          "call": n_call}
    for a in ans.get("assign", []):
        state["assign"][a["row"]] = {"lineage": a["lineage"], "relation": a["relation"], "call": n_call}
    for u in ans.get("unplaced", []):
        state["unplaced"][u["row"]] = {"reason": u["reason"].strip(), "call": n_call}


# --- derived, computed here ------------------------------------------------------------------------

def witness_key(r: dict) -> str:
    """One utterance, however many extractions read it: a voice note's stem and stamp, or the source."""
    return r.get("source") or r["id"]


def derive(state: dict, by_id: dict) -> dict[str, dict]:
    members = defaultdict(list)
    for rid, a in state["assign"].items():
        if rid in by_id:
            members[a["lineage"]].append({**by_id[rid], "relation": a["relation"]})
    out = {}
    for lid, lin in state["lineages"].items():
        ms = sorted(members.get(lid, []), key=lambda r: (r.get("time_utc", ""), r["id"]))
        if not ms:
            continue
        first = ms[0]
        lucianos = [m for m in ms if m.get("who") == "Luciano"]
        adopted = None
        if first.get("who") != "Luciano":
            later = [m for m in lucianos if m["relation"] in ADOPTING]
            if later:
                adopted = later[0]
        out[lid] = {**lin, "members": ms, "first": first, "origin": first.get("who", "?"),
                    "first_luciano": lucianos[0] if lucianos else None, "adopted_by_luciano": adopted,
                    "rows": len(ms), "witnesses": len({witness_key(m) for m in ms}),
                    "days": len({m.get("time_local", "")[:10] for m in ms}),
                    "last": ms[-1].get("time_local", "")[:10]}
    return out


# --- outputs ---------------------------------------------------------------------------------------

def save_state(path: Path, state: dict) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_report(md: Path, state: dict, rows: list[dict], by_id: dict) -> None:
    der = derive(state, by_id)
    gone = [r for r in state["assign"] if r not in by_id] + [r for r in state["unplaced"] if r not in by_id]
    pending = [r for r in rows if r["id"] not in state["assign"] and r["id"] not in state["unplaced"]]
    by_scope_origin = Counter((d["scope"], d["origin"]) for d in der.values())
    origins = sorted({o for _, o in by_scope_origin})
    L = [f"# Lineages of the ideas about Luthier", "",
         f"Written by `scripts/link_ideas.py` ({VERSION}) for Luciano and for the distillation. Prompt `{state['prompt']}`",
         f"(sha256 {state['prompt_sha256'][:12]}), model {state['model']} at effort {state['effort']} via {state['agent']}"
         f" ({state.get('cli_version', '')}); {len(state['calls'])} calls. Input: `{state['timeline_path']}`, last read with sha256",
         f"{state['calls'][-1]['timeline_sha256'][:12] if state['calls'] else '-'}. Who said an idea first and whether Luciano adopted"
         " a model's idea are computed from the rows' times and authors, not by the model.", "",
         f"Rows: {len(rows)} in the timeline; placed {sum(r in by_id for r in state['assign'])}, unplaced "
         f"{sum(r in by_id for r in state['unplaced'])}, pending {len(pending)}"
         + (f", {len(gone)} placed rows no longer in the timeline" if gone else "") + f". Lineages: {len(der)}.", "",
         "| scope | " + " | ".join(f"first said by {o}" for o in origins) + " |", "|---|" + "---|" * len(origins)]
    for sc in SCOPES:
        if any(s == sc for s, _ in by_scope_origin):
            L.append(f"| {sc} | " + " | ".join(str(by_scope_origin.get((sc, o), 0)) for o in origins) + " |")
    adopted = [d for d in der.values() if d["adopted_by_luciano"]]
    L += ["", f"First said by a model and then taken up by Luciano: {len(adopted)}.", "", "## Lineages, by first appearance", ""]
    for d in sorted(der.values(), key=lambda d: (d["first"].get("time_utc", ""), d["id"])):
        f = d["first"]
        head = (f"first {f.get('time_local', '')[:16]} by {d['origin']}; {d['rows']} rows, {d['witnesses']} witnesses, "
                f"{d['days']} days, last {d['last']}")
        if d["adopted_by_luciano"]:
            head += f"; taken up by Luciano {d['adopted_by_luciano'].get('time_local', '')[:10]}"
        L += [f"### {d['id']} ({d['scope']})", "", d["statement"], "", head, ""]
        shown = d["members"] if len(d["members"]) <= 8 else d["members"][:6] + d["members"][-2:]
        for i, m in enumerate(shown):
            if len(d["members"]) > 8 and i == 6:
                L.append(f"- ... {len(d['members']) - 8} more rows")
            L.append(f"- {m.get('time_local', '')[:16]} {m.get('who')} {m['relation']} [{m.get('source', '')}] "
                     f"`{m['id']}`: \"{clip(m.get('quote', ''), 160)}\"")
        L.append("")
    reasons = defaultdict(list)
    for rid, u in state["unplaced"].items():
        if rid in by_id:
            reasons[u["reason"]].append(rid)
    L += ["## Unplaced rows", ""]
    for reason, rids in sorted(reasons.items(), key=lambda kv: -len(kv[1])):
        L.append(f"- {reason} ({len(rids)}): " + ", ".join(f"`{r}`" for r in rids[:12]) + (" ..." if len(rids) > 12 else ""))
    if gone:
        L += ["", "## Placed rows no longer in the timeline", "", ", ".join(f"`{r}`" for r in gone)]
    md.write_text("\n".join(L) + "\n", encoding="utf-8")


# --- main ------------------------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    for p in (args.timeline, args.prompt):
        if not p.is_file():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            return 2
    template = args.prompt.read_text(encoding="utf-8")
    global PROMPT_ID
    PROMPT_ID = args.prompt.stem  # the prompt's file names it; the default is link_ideas_v1
    for kv in args.var:
        k, _, v = kv.partition("=")
        template = template.replace("{" + k + "}", v)
    left = sorted(set(re.findall(r"\{([a-z_]+)\}", template)))
    if left:
        print(f"ERROR: the prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
        return 2
    if PLACEHOLDER not in template:
        print(f"ERROR: the prompt has no {PLACEHOLDER}", file=sys.stderr)
        return 2
    prompt_sha = sha256_bytes(args.prompt.read_bytes())
    cli = None
    if not (args.dry_run or args.report_only):
        try:
            cli = resolve_cli(args.cli)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    model = args.model or (DEFAULT_CODEX_MODEL if cli == "codex" else DEFAULT_CLAUDE_MODEL)
    agent = args.agent or ("codex" if cli == "codex" else "claude-code")
    tag = f"lineages_{PROMPT_ID}_{agent}_{model}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    state_path = args.output_dir / f"{tag}.json"
    md_path = args.output_dir / f"{tag}.md"

    # one run per state: a second run would overwrite the first's placements (2026-10-09, two runs at once)
    import fcntl
    lock = open(args.output_dir / f"{tag}.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"ERROR: another link_ideas run holds {tag}.lock; wait for it or stop it", file=sys.stderr)
        return 2
    rows = sorted(load_timeline(args.timeline), key=lambda r: (r.get("time_utc", "") or "~", r["id"]))
    by_id = {r["id"]: r for r in rows}
    if len(by_id) != len(rows):
        dup = [i for i, n in Counter(r["id"] for r in rows).items() if n > 1]
        print(f"ERROR: the timeline repeats {len(dup)} row ids ({', '.join(dup[:3])}); regenerate it with ideas_timeline.py",
              file=sys.stderr)
        return 2
    if state_path.exists() and not args.force:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state["prompt_sha256"] != prompt_sha or state["model"] != model:
            print(f"ERROR: {state_path.name} was made with prompt {state['prompt_sha256'][:12]} and model {state['model']}; "
                  f"this run has {prompt_sha[:12]} and {model}. --force starts over.", file=sys.stderr)
            return 2
    else:
        try:
            timeline_rel = str(args.timeline.resolve().relative_to(REPO_ROOT))
        except ValueError:
            timeline_rel = str(args.timeline)
        state = {"version": VERSION, "prompt": PROMPT_ID, "prompt_sha256": prompt_sha, "model": model, "agent": agent,
                 "effort": args.effort, "cli_version": cli_version(cli) if cli else "", "window_chars": args.window_chars,
                 "max_thinking_tokens": args.max_thinking_tokens,
                 "quote_chars": args.quote_chars, "timeline_path": timeline_rel, "prompt_vars": args.var,
                 "lineages": {}, "assign": {}, "unplaced": {}, "calls": []}
    if args.report_only:
        write_report(md_path, state, rows, by_id)
        print(f"written: {md_path}")
        return 0

    pending = [r for r in rows if r["id"] not in state["assign"] and r["id"] not in state["unplaced"]]
    wins = windows(pending, args.window_chars, args.quote_chars)
    timeline_sha = sha256_bytes(args.timeline.read_bytes())
    print(f"rows: {len(rows)} | placed: {len(state['assign'])} | unplaced: {len(state['unplaced'])} | "
          f"pending: {len(pending)} in {len(wins)} windows | lineages: {len(state['lineages'])}")
    print(f"CLI: {cli or '-'} | model: {model} | effort: {args.effort} | prompt: {PROMPT_ID} ({prompt_sha[:12]})")
    if args.dry_run:
        for k, w in enumerate(wins, 1):
            print(f"  window {k}: {len(w)} rows, {w[0].get('time_local', '')[:10]} to {w[-1].get('time_local', '')[:10]}")
        return 0

    failed = False
    queue = list(wins)
    k = 0
    while queue:
        win = queue.pop(0)
        k += 1
        if args.max_calls and k > args.max_calls:
            break
        body = build_input(state, by_id, win, args.quote_chars)
        base_prompt = template.replace(PLACEHOLDER, body)
        attempts, prompt_text, ans = [], base_prompt, None
        print(f"[{k}/{k + len(queue)}] {len(win)} rows, {win[0].get('time_local', '')[:10]} to {win[-1].get('time_local', '')[:10]}", flush=True)
        split = False
        for attempt in range(args.retries + 1):
            t0 = time.time()
            try:
                raw = call(cli, prompt_text, model, args.effort, args.timeout, args.max_output_tokens, args.max_thinking_tokens)
            except OutputLimit as exc:
                attempts.append({"error": f"output limit: {exc}", "seconds": round(time.time() - t0)})
                split = len(win) > 1
                print(f"  the answer hit the output token limit; " + ("the window is split in two" if split else "a single row, cannot split"), file=sys.stderr)
                break
            except Exception as exc:
                attempts.append({"error": str(exc)[:500], "seconds": round(time.time() - t0)})
                print(f"  call failed: {str(exc)[:200]}", file=sys.stderr)
                continue
            try:
                cand, errors = expand(parse_json(raw), win)
                errors = errors + check_answer(cand, state, win)
            except (ValueError, json.JSONDecodeError) as exc:
                cand, errors = None, [f"not valid JSON: {exc}"]
            attempts.append({"answer": raw, "answer_sha256": sha256_bytes(raw.encode()), "errors": errors,
                             "seconds": round(time.time() - t0)})
            if not errors:
                ans = cand
                break
            print(f"  answer rejected ({len(errors)} errors): {errors[0][:160]}\n  the answer began: {raw.strip()[:200]!r}", file=sys.stderr)
            prompt_text = (base_prompt + "\n\n## Your previous answer was rejected\n\n" + "\n".join(f"- {e}" for e in errors)
                           + "\n\nAnswer again, the whole JSON object for this window.\n")
        n_call = len(state["calls"]) + 1
        state["calls"].append({"n": n_call, "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                               "rows": len(win), "first_row": win[0]["id"], "last_row": win[-1]["id"],
                               "input_sha256": sha256_bytes(base_prompt.encode()), "timeline_sha256": timeline_sha,
                               "accepted": ans is not None, "split": split, "attempts": attempts})
        if split:
            half = len(win) // 2
            queue[:0] = [win[:half], win[half:]]
            save_state(state_path, state)
            continue
        if ans is None:
            save_state(state_path, state)
            print(f"  window {k} not placed after {len(attempts)} attempts; state saved, run again to resume", file=sys.stderr)
            failed = True
            break
        apply_answer(ans, state, n_call)
        save_state(state_path, state)
        print(f"  placed {len(ans.get('assign', []))}, unplaced {len(ans.get('unplaced', []))}, "
              f"new lineages {len(ans.get('new_lineages', []))}; total {len(state['lineages'])}", flush=True)
    write_report(md_path, state, rows, by_id)
    print(f"written: {state_path}\n         {md_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
