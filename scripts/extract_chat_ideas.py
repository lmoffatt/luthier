#!/usr/bin/env python3
"""Extract the ideas about Luthier from each conversation with an AI in the record.

For every thread `.md` under the input directory (default record/IA/raw, as `iachat fetch` leaves
it), the prompt `extract_ideas_dialogue_v1` is run through the `claude` (or `codex`) command line
and the ideas are written to `<output-dir>/<source>_<date>_<id8>_<prompt>_<agent>_<model>_ideas.md`.
A long thread is cut into windows at turn boundaries (--window-chars); each window is one call,
and the bodies are concatenated under one heading per window. Tool turns are dropped before the
cut (--keep-tool-turns keeps them).

The frontmatter of the output is written here, deterministically (source, key, title, started,
turns, windows, sha256 of the thread, prompt and its sha256, agent, model); the model writes only
the body. Idempotent: a thread with a non-empty output is skipped (unless --force). Luciano runs
it, as he runs extract_ideas.py on the voice notes.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_ID = "extract_ideas_dialogue_v1"
DEFAULT_INPUT = REPO_ROOT / "record" / "IA" / "raw"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "ideas"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / f"{PROMPT_ID}.md"
DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5"
PLACEHOLDER = "<<<THREAD>>>"
MODE = "editor"

TURN_RE = re.compile(r"^## (\d+)\. (Luciano|Model|Tool)\b.*$", re.MULTILINE)
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"\A```[a-zA-Z]*\n")
FENCE_CLOSE_RE = re.compile(r"\n```\s*\Z")
IDEA_RE = re.compile(r"^### ", re.MULTILINE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directory", type=Path, nargs="?", default=DEFAULT_INPUT,
                   help="where the threads are; searched recursively")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto")
    p.add_argument("--model", default=None)
    p.add_argument("--agent", default=None, help="name of the agent in the frontmatter; default by CLI")
    p.add_argument("--window-chars", type=int, default=60000, help="largest window sent in one call")
    p.add_argument("--keep-tool-turns", action="store_true", help="keep the Tool turns in what the model sees")
    p.add_argument("--only", nargs="*", default=None, help="only threads whose file name contains one of these")
    p.add_argument("--force", action="store_true", help="redo threads that have an output")
    p.add_argument("--dry-run", action="store_true", help="list the threads and windows; call no model")
    p.add_argument("--sleep", type=float, default=0.0, help="pause between calls, seconds")
    p.add_argument("--timeout", type=float, default=600.0, help="per call, seconds")
    return p.parse_args(argv)


def _resolve_cli(choice: str) -> str:
    for name in ((choice,) if choice != "auto" else ("claude", "codex")):
        if shutil.which(name):
            return name
    raise RuntimeError(f"{choice if choice != 'auto' else 'neither claude nor codex'} is not on the PATH")


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-") or "x"


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


def _clean_body(raw: str) -> str:
    body = raw.strip()
    body = FRONT_RE.sub("", body)
    body = FENCE_OPEN_RE.sub("", body)
    body = FENCE_CLOSE_RE.sub("", body)
    return body.strip()


# --- the thread ---------------------------------------------------------------------------------

def parse_thread(text: str) -> tuple[dict, list[dict]]:
    """The frontmatter as a dict and the turns as dicts (n, author, text), text with its heading."""
    front: dict = {}
    m = FRONT_RE.match(text)
    if m:
        for ln in m.group(1).splitlines():
            k, sep, v = ln.partition(":")
            if sep and not ln.startswith((" ", "-")):
                front[k.strip()] = v.strip().strip('"')
    marks = list(TURN_RE.finditer(text))
    turns = []
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        turns.append({"n": int(mk.group(1)), "author": mk.group(2), "text": text[mk.start():end].rstrip() + "\n"})
    return front, turns


def windows(turns: list[dict], window_chars: int) -> list[list[dict]]:
    """Cut the turns into runs no longer than window_chars; a single turn longer than that is its own window."""
    out: list[list[dict]] = []
    cur: list[dict] = []
    size = 0
    for t in turns:
        n = len(t["text"])
        if cur and size + n > window_chars:
            out.append(cur)
            cur, size = [], 0
        cur.append(t)
        size += n
    if cur:
        out.append(cur)
    return out


def window_input(front: dict, win: list[dict], k: int, total: int, n_turns: int) -> str:
    head = [f"source: {front.get('source', '')}", f"title: {front.get('title', '')}",
            f"started: {front.get('started', '')}",
            f"window: {k} of {total}; turns {win[0]['n']} to {win[-1]['n']} of {n_turns}", ""]
    return "\n".join(head) + "\n" + "\n".join(t["text"] for t in win)


def output_stem(front: dict, path: Path) -> str:
    source = front.get("source") or path.parent.name
    started = front.get("started", "")[:10] or "undated"
    ident = (front.get("id") or path.stem)[:8]
    return f"{source}_{started}_{ident}"


def frontmatter(*, front: dict, path: Path, sha: str, n_turns: int, n_windows: int, n_ideas: int,
                prompt_sha: str, agent: str, model: str, window_chars: int) -> str:
    lines = ["---", f"source: {front.get('source', '')}", f"key: {front.get('source', '')}:{front.get('account', '')}:{front.get('id', '')}",
             f"title: \"{front.get('title', '').replace(chr(34), chr(39))}\"", f"started: {front.get('started', '')}",
             f"ended: {front.get('ended', '')}", f"thread: {path.name}", f"thread_sha256: {sha}",
             f"turns: {n_turns}", f"windows: {n_windows}", f"window_chars: {window_chars}", f"ideas: {n_ideas}",
             f"generated_by: {PROMPT_ID}", f"prompt_sha256: {prompt_sha}", f"mode: {MODE}",
             f"agent: {agent}", f"model: {model}", "---"]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    if not args.directory.is_dir():
        print(f"ERROR: not a directory: {args.directory}", file=sys.stderr)
        return 2
    if not args.prompt.is_file():
        print(f"ERROR: prompt not found: {args.prompt}", file=sys.stderr)
        return 2
    template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"ERROR: the prompt has no {PLACEHOLDER}", file=sys.stderr)
        return 2
    prompt_sha = hashlib.sha256(args.prompt.read_bytes()).hexdigest()

    cli = None
    if not args.dry_run:
        try:
            cli = _resolve_cli(args.cli)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    model = args.model or (DEFAULT_CODEX_MODEL if cli == "codex" else DEFAULT_CLAUDE_MODEL)
    agent = args.agent or ("codex" if cli == "codex" else "claude-code")
    tag = f"{PROMPT_ID}_{_slug(agent)}_{_slug(model)}_ideas"

    threads = sorted(p for p in args.directory.rglob("*.md") if p.is_file())
    if args.only:
        threads = [p for p in threads if any(s in p.name for s in args.only)]
    if not threads:
        print(f"no threads .md under {args.directory}", file=sys.stderr)
        return 1

    jobs, skipped = [], 0
    for path in threads:
        text = path.read_text(encoding="utf-8")
        front, turns = parse_thread(text)
        if not turns:
            print(f"skip (no turns): {path.name}", file=sys.stderr)
            continue
        out = args.output_dir / f"{output_stem(front, path)}_{tag}.md"
        if out.exists() and out.stat().st_size > 0 and not args.force:
            skipped += 1
            continue
        jobs.append((path, text, front, turns, out))
    print(f"threads: {len(threads)} | done: {skipped} | pending: {len(jobs)}")
    print(f"CLI: {cli or '-'} | model: {model} | agent: {agent} | prompt: {PROMPT_ID} | window: {args.window_chars}")

    failures = 0
    for i, (path, text, front, turns, out) in enumerate(jobs, 1):
        kept = turns if args.keep_tool_turns else [t for t in turns if t["author"] != "Tool"]
        wins = windows(kept, args.window_chars)
        if args.dry_run:
            print(f"[dry {i}/{len(jobs)}] {path.name} -> {out.name}  ({len(turns)} turns, {len(wins)} windows)")
            continue
        print(f"[{i}/{len(jobs)}] {path.name}  ({len(turns)} turns, {len(wins)} windows)", flush=True)
        bodies = []
        try:
            for k, win in enumerate(wins, 1):
                prompt_text = template.replace(PLACEHOLDER, window_input(front, win, k, len(wins), len(turns)))
                body = _clean_body(_call(cli, prompt_text, model, args.timeout))
                if len(wins) > 1:
                    body = f"## Window {k} of {len(wins)}: turns {win[0]['n']} to {win[-1]['n']}\n\n{body}"
                bodies.append(body)
                if args.sleep:
                    time.sleep(args.sleep)
        except Exception as exc:  # one failed thread must not stop the others
            failures += 1
            print(f"  ERROR: {exc}", file=sys.stderr)
            continue
        body = "\n\n".join(bodies)
        fm = frontmatter(front=front, path=path, sha=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                         n_turns=len(turns), n_windows=len(wins), n_ideas=len(IDEA_RE.findall(body)),
                         prompt_sha=prompt_sha, agent=agent, model=model, window_chars=args.window_chars)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out.write_text(fm + "\n\n" + body + "\n", encoding="utf-8")
        print(f"  -> {out.name}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
