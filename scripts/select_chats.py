#!/usr/bin/env python3
"""Select the conversations with AIs that belong in luthier's record.

The candidates come from the archive of conversations (`~/Projects/IA_chat`) through its own
command, `iachat fetch --dry-run`, so the same privacy rules apply: a thread the fetch would
withhold is still judged here, and reported as withheld, so that Luciano knows what stays out.
A model reads each candidate (Luciano's turns complete, the model's turns shortened) with
`prompts/select_chats_v1.md` and answers yes, partial or no, with its reason and the turns that
are about Luthier. A thread whose cwd is this repository is taken without asking a model
(--cwd-is-yes; --no-cwd-rule sends it to the model too).

Output, in --output-dir (default record/IA/selection):
  <date>_select_chats_v1_<agent>_<model>.jsonl   one line per candidate, with everything used
  <date>_select_chats_v1_<agent>_<model>.md      the table for Luciano and the fetch command

Idempotent: a key already in the jsonl is not judged again (unless --force). Luciano runs it, and
the `iachat fetch` it prints is his to run too. Nothing is committed.
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
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_ID = "select_chats_v1"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / f"{PROMPT_ID}.md"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "IA" / "selection"
DEFAULT_TO = REPO_ROOT / "record" / "IA" / "raw"
DEFAULT_IACHAT = Path.home() / "Projects" / "IA_chat"
DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5"
PLACEHOLDER = "<<<THREAD>>>"
VERDICTS = ("yes", "partial", "no")

TURN_RE = re.compile(r"^## (\d+)\. (Luciano|Model|Tool)\b(.*)$", re.MULTILINE)
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--iachat", type=Path, default=DEFAULT_IACHAT, help="root of the archive (its tools/iachat.py is used)")
    p.add_argument("--query", default="luthier", help="full-text query that selects the candidates")
    p.add_argument("--since", default="2026-05-01")
    p.add_argument("--until", default=None)
    p.add_argument("--source", default=None, help="only this source of the archive")
    p.add_argument("--to", type=Path, default=DEFAULT_TO, help="where the fetch would copy; only used to build the dry run and the command")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto")
    p.add_argument("--model", default=None)
    p.add_argument("--agent", default=None, help="name of the agent in the output; default by CLI")
    p.add_argument("--date", default=date.today().isoformat(), help="date of the run, in the file names")
    p.add_argument("--max-model-chars", type=int, default=600, help="how much of each model turn the judge sees")
    p.add_argument("--cwd-is-yes", dest="cwd_rule", action="store_true", default=True,
                   help="a thread whose cwd is this repository is yes without a model (default)")
    p.add_argument("--no-cwd-rule", dest="cwd_rule", action="store_false")
    p.add_argument("--take", default="yes,partial", help="verdicts that go into the fetch command")
    p.add_argument("--force", action="store_true", help="judge again the keys already in the output")
    p.add_argument("--dry-run", action="store_true", help="list the candidates and call no model")
    p.add_argument("--sleep", type=float, default=0.0)
    p.add_argument("--timeout", type=float, default=300.0)
    p.add_argument("--retries", type=int, default=1, help="calls repeated when the answer is not the JSON asked for")
    return p.parse_args(argv)


# --- the archive, through its command -------------------------------------------------------

def _iachat(root: Path, *args: str) -> str:
    tool = root / "tools" / "iachat.py"
    if not tool.is_file():
        raise RuntimeError(f"no iachat at {tool}")
    proc = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "iachat failed")
    return proc.stdout


def candidates(root: Path, query: str, since: str | None, until: str | None, source: str | None,
               to: Path) -> list[dict]:
    """What `iachat fetch --dry-run` would copy or withhold, one dict per thread."""
    args = ["fetch", "--query", query, "--to", str(to), "--dry-run"]
    if since:
        args += ["--since", since]
    if until:
        args += ["--until", until]
    if source:
        args += ["--source", source]
    out: list[dict] = []
    for line in _iachat(root, *args).splitlines():
        if line.startswith("would copy  "):
            rest = line[len("would copy  "):]
            head, _, rel = rest.rpartition("  -> ")
            key, _, title = head.partition("  ")
            out.append({"key": key, "title": title, "withheld": "", "rel": rel})
        elif line.startswith("withheld  "):
            rest = line[len("withheld  "):]
            head, _, reason = rest.rpartition("  (")
            key, _, title = head.partition("  ")
            out.append({"key": key, "title": title, "withheld": reason.rstrip(")"), "rel": ""})
    return out


def thread_path(root: Path, key: str) -> Path:
    return Path(_iachat(root, "show", key, "--path").strip())


# --- the digest a judge sees ------------------------------------------------------------------

def parse_thread(text: str) -> tuple[dict, list[dict]]:
    """The frontmatter as a dict and the turns as dicts (n, author, heading, body)."""
    front: dict = {}
    m = FRONT_RE.match(text)
    if m:
        for ln in m.group(1).splitlines():
            k, sep, v = ln.partition(":")
            if sep and not ln.startswith(" ") and not ln.startswith("-"):
                front[k.strip()] = v.strip().strip('"')
    marks = list(TURN_RE.finditer(text))
    turns = []
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        turns.append({"n": int(mk.group(1)), "author": mk.group(2), "heading": mk.group(0).strip(),
                      "body": text[mk.end():end].strip()})
    return front, turns


def digest(text: str, max_model_chars: int) -> str:
    front, turns = parse_thread(text)
    head = [f"source: {front.get('source', '')}", f"title: {front.get('title', '')}",
            f"started: {front.get('started', '')}", f"turns: {front.get('turns', len(turns))}",
            f"cwd: {front.get('cwd', '')}", ""]
    parts = ["\n".join(head)]
    for t in turns:
        if t["author"] == "Tool":
            continue
        body = t["body"]
        if t["author"] == "Model" and len(body) > max_model_chars:
            body = body[:max_model_chars].rstrip() + " [...]"
        parts.append(f"{t['heading']}\n\n{body}\n")
    return "\n".join(parts)


def luciano_turns(text: str) -> list[int]:
    return [t["n"] for t in parse_thread(text)[1] if t["author"] == "Luciano"]


def cwd_is_repo(front: dict, repo: Path) -> bool:
    cwd = front.get("cwd", "")
    return bool(cwd) and cwd == "-" + str(repo).replace("/", "-").lstrip("-")


# --- the model --------------------------------------------------------------------------------

def _resolve_cli(choice: str) -> str:
    for name in ((choice,) if choice != "auto" else ("claude", "codex")):
        if shutil.which(name):
            return name
    raise RuntimeError(f"{choice if choice != 'auto' else 'neither claude nor codex'} is not on the PATH")


def _call(cli: str, prompt_text: str, model: str, timeout: float) -> str:
    if cli == "claude":
        proc = subprocess.run(["claude", "-p", "--model", model, "--output-format", "text",
                               "--no-session-persistence", "--tools", ""],
                              input=prompt_text, capture_output=True, text=True, timeout=timeout)
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout).strip() or "claude failed")
        return proc.stdout
    proc = subprocess.run(["codex", "exec", "--skip-git-repo-check", "--color", "never",
                           "--sandbox", "read-only", "-m", model, "-"],
                          input=prompt_text, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "codex failed")
    return proc.stdout


def parse_answer(raw: str, valid_turns: list[int]) -> dict:
    m = JSON_RE.search(raw)
    if not m:
        raise ValueError("no JSON object in the answer")
    ans = json.loads(m.group(0))
    if ans.get("verdict") not in VERDICTS:
        raise ValueError(f"verdict {ans.get('verdict')!r} is not one of {VERDICTS}")
    turns = sorted({int(n) for n in ans.get("turns", []) if int(n) in valid_turns})
    return {"verdict": ans["verdict"], "reason": str(ans.get("reason", "")).strip(),
            "turns": turns, "topics": [str(t) for t in ans.get("topics", [])][:6]}


def judge(cli: str, template: str, text: str, model: str, timeout: float, max_model_chars: int,
          retries: int) -> dict:
    prompt_text = template.replace(PLACEHOLDER, digest(text, max_model_chars))
    valid = luciano_turns(text)
    last: Exception | None = None
    for _ in range(retries + 1):
        raw = _call(cli, prompt_text, model, timeout)
        try:
            return parse_answer(raw, valid)
        except (ValueError, json.JSONDecodeError) as exc:
            last = exc
    raise RuntimeError(f"the answer was not the JSON asked for: {last}")


# --- the outputs ------------------------------------------------------------------------------

def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_done(jsonl: Path) -> dict[str, dict]:
    done: dict[str, dict] = {}
    if jsonl.exists():
        for ln in jsonl.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                row = json.loads(ln)
                done[row["key"]] = row
    return done


def write_summary(md: Path, rows: list[dict], args: argparse.Namespace, prompt_sha: str,
                  model: str, agent: str, errors: list[str]) -> None:
    take = [v.strip() for v in args.take.split(",") if v.strip()]
    rows = sorted(rows, key=lambda r: (r.get("started", ""), r["key"]))
    taken = [r for r in rows if r.get("verdict") in take and not r["withheld"]]
    lost = [r for r in rows if r.get("verdict") in take and r["withheld"]]
    lines = [f"# Selection of conversations for luthier's record, {args.date}", "",
             f"Written by `scripts/select_chats.py` for Luciano. Prompt `{PROMPT_ID}` (sha256 {prompt_sha}),",
             f"model {model} via {agent}; candidates from `iachat fetch --dry-run --query {args.query}"
             f"{' --since ' + args.since if args.since else ''}{' --until ' + args.until if args.until else ''}"
             f"{' --source ' + args.source if args.source else ''}` at `{args.iachat}`; a thread whose cwd is this",
             f"repository is yes by rule ({'on' if args.cwd_rule else 'off'}); the model's turns were cut to "
             f"{args.max_model_chars} characters. Verdicts taken: {', '.join(take)}.", "",
             f"Candidates: {len(rows)}. Taken: {len(taken)}. Withheld by the archive's privacy rules but "
             f"judged {', '.join(take)}: {len(lost)}. Errors: {len(errors)}.", "",
             "| started | source | key | verdict | by | withheld | reason |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r.get('started', '')[:10]} | {r['source']} | `{r['key']}` | {r.get('verdict', '')} | "
                     f"{r.get('judged_by', '')} | {r['withheld']} | {r.get('reason', '').replace('|', '/')} |")
    if taken:
        ids = " ".join(r["key"] for r in taken)
        lines += ["", "## The fetch (Luciano runs it)", "", "```",
                  f"iachat fetch --ids {ids} --to {args.to}", "```"]
    if lost:
        lines += ["", "## Judged relevant but withheld", "",
                  "These stay in the archive; copying them needs a decision (a redacted copy, a local-only "
                  "copy, or an override in `flags.override`).", ""]
        lines += [f"- `{r['key']}` {r['title'][:60]}: {r['withheld']}" for r in lost]
    if errors:
        lines += ["", "## Errors", ""] + [f"- {e}" for e in errors]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    if not args.prompt.is_file():
        print(f"ERROR: prompt not found: {args.prompt}", file=sys.stderr)
        return 2
    template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"ERROR: the prompt has no {PLACEHOLDER}", file=sys.stderr)
        return 2
    prompt_sha = _sha(args.prompt)
    try:
        cands = candidates(args.iachat, args.query, args.since, args.until, args.source, args.to)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not cands:
        print("no candidates")
        return 1

    cli = None
    if not args.dry_run:
        try:
            cli = _resolve_cli(args.cli)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    model = args.model or (DEFAULT_CODEX_MODEL if cli == "codex" else DEFAULT_CLAUDE_MODEL)
    agent = args.agent or ("codex" if cli == "codex" else "claude-code")
    tag = f"{args.date}_{PROMPT_ID}_{agent}_{model}"
    jsonl = args.output_dir / f"{tag}.jsonl"
    md = args.output_dir / f"{tag}.md"
    done = {} if args.force else load_done(jsonl)

    print(f"candidates: {len(cands)} | already judged: {sum(c['key'] in done for c in cands)} | "
          f"withheld by the archive: {sum(bool(c['withheld']) for c in cands)}")
    if args.dry_run:
        for c in cands:
            print(f"  {'withheld ' if c['withheld'] else 'candidate'}  {c['key']}  {c['title'][:50]}"
                  + (f"  ({c['withheld']})" if c['withheld'] else ""))
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = list(done.values())
    errors: list[str] = []
    if args.force and jsonl.exists():
        jsonl.unlink()
    with jsonl.open("a", encoding="utf-8") as fh:
        for i, c in enumerate(cands, 1):
            if c["key"] in done:
                continue
            try:
                path = thread_path(args.iachat, c["key"])
                text = path.read_text(encoding="utf-8")
                front, _ = parse_thread(text)
                row = {**c, "source": front.get("source", c["key"].split(":")[0]),
                       "started": front.get("started", ""), "cwd": front.get("cwd", ""),
                       "thread_path": str(path), "thread_sha256": _sha(path),
                       "prompt": PROMPT_ID, "prompt_sha256": prompt_sha, "model": model, "agent": agent,
                       "max_model_chars": args.max_model_chars, "date": args.date}
                if args.cwd_rule and cwd_is_repo(front, REPO_ROOT):
                    row.update(verdict="yes", reason="cwd is this repository", turns=luciano_turns(text),
                               topics=[], judged_by="rule")
                else:
                    row.update(judge(cli, template, text, model, args.timeout, args.max_model_chars,
                                     args.retries), judged_by=model)
                    if args.sleep:
                        time.sleep(args.sleep)
            except Exception as exc:  # one bad thread must not stop the others
                errors.append(f"{c['key']}: {exc}")
                print(f"[{i}/{len(cands)}] ERROR {c['key']}: {exc}", file=sys.stderr)
                continue
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            fh.flush()
            rows.append(row)
            print(f"[{i}/{len(cands)}] {row['verdict']:7s} {row['judged_by']:8s} {c['key']}  {c['title'][:40]}"
                  + ("  (withheld)" if c["withheld"] else ""))
    write_summary(md, rows, args, prompt_sha, model, agent, errors)
    print(f"written: {jsonl}\n         {md}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
