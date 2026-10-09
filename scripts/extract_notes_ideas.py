#!/usr/bin/env python3
"""Extract the ideas about Luthier from written notes, one call per note.

For every `.md` under the input directories (default `record/Lucianos ideas` and the model texts
of `record/IA/HoTTification-2025-06`, searched recursively; manifests, fetched conversations,
local-only copies and the ideas files themselves are skipped), the prompt
`extract_ideas_note_v1` is run through the `claude` (or `codex`) command line with the note's
lines numbered, and the ideas are written to
`<output-dir>/<created-date>_<note-slug>_<prompt>_<agent>_<model>_ideas.md`.

The note's author and creation date come from its frontmatter (`author:`, `created:`; the files
`import_notes.py` writes have them) or, failing that, from the `manifest.jsonl` next to it, or
from --author and the file's modification time. The frontmatter of the output is written here:
note, its sha256, author, created, the prompt and its sha256, agent, model, effort, and how many
quotes the check found. After each call every quote is looked for in the note (words only:
punctuation and case dropped, an ellipsis for skipped words) and on or near the line it cites;
the misses are printed. --check-only reruns that check without the model. Idempotent: a note with
a non-empty output is skipped (unless --force). Luciano runs it.
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
import unicodedata
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_ID = "extract_ideas_note_v1"
DEFAULT_INPUTS = [REPO_ROOT / "record" / "Lucianos ideas", REPO_ROOT / "record" / "IA" / "HoTTification-2025-06"]
DEFAULT_OUTPUT = REPO_ROOT / "record" / "ideas"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / f"{PROMPT_ID}.md"
DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5"
DEFAULT_EFFORT = "low"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
PLACEHOLDER = "<<<NOTE>>>"
VARS: list[str] = []  # the --var values of this run, recorded in each output
MODE = "editor"
SKIP_NAMES = {"manifest.jsonl", "timeline.md", "README.md"}
SKIP_SUFFIX = ("_ideas.md",)

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"\A```[a-zA-Z]*\n")
FENCE_CLOSE_RE = re.compile(r"\n```\s*\Z")
ENTRY_RE = re.compile(r"^### (.+)$", re.MULTILINE)
ELLIPSIS_RE = re.compile(r"\s*(?:\.\.\.|…|\[\.\.\.\]|\[…\])\s*")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directories", type=Path, nargs="*", default=None, help="where the notes are; searched recursively")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT)
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto")
    p.add_argument("--model", default=None)
    p.add_argument("--effort", choices=EFFORTS, default=DEFAULT_EFFORT, help="thinking effort passed to claude (codex ignores it)")
    p.add_argument("--agent", default=None)
    p.add_argument("--author", default="Luciano", help="author of a note that states none")
    p.add_argument("--var", action="append", default=[], metavar="KEY=VALUE",
                   help="fills {KEY} in the prompt (for the controls: --var language=Python)")
    p.add_argument("--only", nargs="*", default=None, help="only notes whose file name contains one of these")
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--check-only", action="store_true", help="check the quotes of existing outputs; call no model")
    p.add_argument("--sleep", type=float, default=0.0)
    p.add_argument("--timeout", type=float, default=600.0)
    return p.parse_args(argv)


def _resolve_cli(choice: str) -> str:
    for name in ((choice,) if choice != "auto" else ("claude", "codex")):
        if shutil.which(name):
            return name
    raise RuntimeError(f"{choice if choice != 'auto' else 'neither claude nor codex'} is not on the PATH")


def _slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-") or "x"


def _call(cli: str, prompt_text: str, model: str, timeout: float, effort: str) -> str:
    if cli == "claude":
        proc = subprocess.run(["claude", "-p", "--model", model, "--effort", effort, "--output-format", "text",
                               "--no-session-persistence", "--tools", ""],
                              input=prompt_text, capture_output=True, text=True, timeout=timeout)
    else:
        proc = subprocess.run(["codex", "exec", "--skip-git-repo-check", "--color", "never", "--sandbox", "read-only",
                               "-m", model, "-"], input=prompt_text, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or f"{cli} failed")
    return proc.stdout


def _clean_body(raw: str) -> str:
    body = FRONT_RE.sub("", raw.strip(), count=1)
    body = FENCE_OPEN_RE.sub("", body)
    body = FENCE_CLOSE_RE.sub("", body)
    return body.strip()


# --- the note -----------------------------------------------------------------------------------

def parse_front(text: str) -> tuple[dict, str]:
    front: dict = {}
    m = FRONT_RE.match(text)
    if not m:
        return front, text
    for ln in m.group(1).splitlines():
        k, sep, v = ln.partition(":")
        if sep and not ln.startswith((" ", "-")):
            front[k.strip()] = v.strip().strip('"')
    return front, text[m.end():]


def manifest_row(path: Path) -> dict:
    mf = path.parent / "manifest.jsonl"
    if mf.exists():
        for ln in mf.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                row = json.loads(ln)
                if row.get("file") == path.name:
                    return row
    return {}


def note_meta(path: Path, text: str, default_author: str) -> tuple[dict, str]:
    """(meta, body): author, created, title; from the frontmatter, else the manifest, else defaults."""
    front, body = parse_front(text)
    row = manifest_row(path)
    author = front.get("author") or row.get("author") or default_author
    created = front.get("created") or row.get("created") or row.get("modified") \
        or datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%S")
    title = front.get("title") or path.stem
    return {"author": author, "created": created, "title": title, "front": front}, body


def numbered(body: str) -> tuple[str, list[str]]:
    lines = body.splitlines()
    return "\n".join(f"{i:4d}  {ln}" for i, ln in enumerate(lines, 1)), lines


# --- the check ----------------------------------------------------------------------------------

def _words(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace("\\n", " ")
    text = "".join(" " if unicodedata.category(c)[0] in "PS" else c for c in text)
    return " ".join(text.casefold().split())


def _in_order(quote: str, haystack: str) -> bool:
    pos, pieces = 0, [_words(p) for p in ELLIPSIS_RE.split(quote) if _words(p)]
    if not pieces:
        return False
    for piece in pieces:
        i = haystack.find(piece, pos)
        if i < 0:
            return False
        pos = i + len(piece)
    return True


def check_quotes(ideas_body: str, lines: list[str], window: int = 2) -> tuple[int, int, list[str]]:
    """Every entry's quote looked for in the note, and its first words on or near the cited line."""
    whole = _words("\n".join(lines))
    found, total, problems = 0, 0, []
    for m in ENTRY_RE.finditer(ideas_body):
        end = ideas_body.find("\n### ", m.end())
        entry = ideas_body[m.end(): end if end >= 0 else len(ideas_body)]
        q = re.search(r"^- \*\*Quote\*\*: \"(.*)\"\s*\(line (\d+)\)\s*$", entry, re.MULTILINE)
        if not q:
            q2 = re.search(r"^- \*\*Quote\*\*: \"(.*)\"", entry, re.MULTILINE)
            if q2:
                total += 1
                problems.append(f"{m.group(1).strip()}: quote without a line number")
            continue
        total += 1
        slug, quote, n = m.group(1).strip(), q.group(1), int(q.group(2))
        if not _in_order(quote, whole):
            problems.append(f"{slug}: not in the note: \"{quote[:80]}\"")
            continue
        head = " ".join(_words(quote).split()[:5])
        near = _words("\n".join(lines[max(0, n - 1 - window): n + window]))
        if n < 1 or n > len(lines) or head not in near:
            problems.append(f"{slug}: the quote is in the note but not at line {n}: \"{quote[:60]}\"")
            continue
        found += 1
    return found, total, problems


# --- the outputs --------------------------------------------------------------------------------

def output_name(meta: dict, path: Path, tag: str) -> str:
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}\s*", "", path.stem)  # an imported note's name starts with its date
    return f"{meta['created'][:10]}_{_slug(stem)[:40]}_{tag}.md"


def frontmatter(*, path: Path, sha: str, meta: dict, n_ideas: int, quotes: str, prompt_sha: str,
                agent: str, model: str, effort: str) -> str:
    return "\n".join(["---", f"note: {path.name}", f"note_dir: {path.parent.name}", f"note_sha256: {sha}",
                      f"title: \"{meta['title'].replace(chr(34), chr(39))}\"", f"author: {meta['author']}",
                      f"created: {meta['created']}", f"ideas: {n_ideas}", f"quotes_found: {quotes}",
                      f"generated_by: {PROMPT_ID}", f"prompt_sha256: {prompt_sha}", f"mode: {MODE}",
                      *([f"prompt_vars: {'; '.join(VARS)}"] if VARS else []),
                      f"agent: {agent}", f"model: {model}", f"effort: {effort}", "---"])


def notes_under(dirs: list[Path]) -> list[Path]:
    out = []
    for d in dirs:
        if d.is_file():
            out.append(d)
            continue
        for f in sorted(d.rglob("*.md")):
            if f.name in SKIP_NAMES or f.name.endswith(SKIP_SUFFIX) or "local-only" in f.parts:
                continue
            if "raw" in f.parts:  # fetched conversations are read by extract_chat_ideas
                continue
            out.append(f)
    return out


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    dirs = args.directories or DEFAULT_INPUTS
    if not args.prompt.is_file():
        print(f"ERROR: prompt not found: {args.prompt}", file=sys.stderr)
        return 2
    template = args.prompt.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        print(f"ERROR: the prompt has no {PLACEHOLDER}", file=sys.stderr)
        return 2
    prompt_sha = hashlib.sha256(args.prompt.read_bytes()).hexdigest()
    global PROMPT_ID, VARS
    VARS = list(args.var)
    PROMPT_ID = args.prompt.stem  # the prompt's file names it; the default is extract_ideas_note_v1
    for kv in args.var:
        k, _, v = kv.partition("=")
        template = template.replace("{" + k + "}", v)
    left = sorted(set(re.findall(r"\{([a-z_]+)\}", template)))
    if left:
        print(f"ERROR: the prompt has unfilled {', '.join(left)}; pass --var", file=sys.stderr)
        return 2
    cli = None
    if not (args.dry_run or args.check_only):
        try:
            cli = _resolve_cli(args.cli)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    model = args.model or (DEFAULT_CODEX_MODEL if cli == "codex" else DEFAULT_CLAUDE_MODEL)
    agent = args.agent or ("codex" if cli == "codex" else "claude-code")
    tag = f"{PROMPT_ID}_{_slug(agent)}_{_slug(model)}_ideas"

    notes = notes_under([Path(d) for d in dirs])
    if args.only:
        notes = [n for n in notes if any(s in n.name for s in args.only)]
    if not notes:
        print("no notes found", file=sys.stderr)
        return 1

    if args.check_only:
        bad = 0
        for path in notes:
            text = path.read_text(encoding="utf-8")
            meta, body = note_meta(path, text, args.author)
            out = args.output_dir / output_name(meta, path, tag)
            if not out.exists():
                continue
            ideas = out.read_text(encoding="utf-8")
            found, total, problems = check_quotes(ideas, numbered(body)[1])
            out.write_text(re.sub(r"^quotes_found:.*$", f"quotes_found: {found}/{total}", ideas, count=1, flags=re.MULTILINE),
                           encoding="utf-8")
            print(f"{out.name}: quotes found {found}/{total}")
            for pr in problems:
                print(f"  - {pr}")
            bad += bool(problems)
        return 1 if bad else 0

    jobs, skipped = [], 0
    for path in notes:
        text = path.read_text(encoding="utf-8")
        meta, body = note_meta(path, text, args.author)
        out = args.output_dir / output_name(meta, path, tag)
        if out.exists() and out.stat().st_size > 0 and not args.force:
            skipped += 1
            continue
        jobs.append((path, text, meta, body, out))
    print(f"notes: {len(notes)} | done: {skipped} | pending: {len(jobs)}")
    print(f"CLI: {cli or '-'} | model: {model} | effort: {args.effort} | agent: {agent} | prompt: {PROMPT_ID}")
    failures = 0
    for i, (path, text, meta, body, out) in enumerate(jobs, 1):
        if args.dry_run:
            print(f"[dry {i}/{len(jobs)}] {path.name} ({meta['author']}, {meta['created'][:10]}) -> {out.name}")
            continue
        print(f"[{i}/{len(jobs)}] {path.name} ({meta['author']}, {meta['created'][:10]})", flush=True)
        shown, lines = numbered(body)
        head = f"author: {meta['author']}\ntitle: {meta['title']}\ncreated: {meta['created']}\nfile: {path.name}\n\n"
        try:
            raw = _call(cli, template.replace(PLACEHOLDER, head + shown), model, args.timeout, args.effort)
        except Exception as exc:
            failures += 1
            print(f"  ERROR: {exc}", file=sys.stderr)
            continue
        ideas = _clean_body(raw)
        found, total, problems = check_quotes(ideas, lines)
        fm = frontmatter(path=path, sha=hashlib.sha256(text.encode("utf-8")).hexdigest(), meta=meta,
                         n_ideas=len(ENTRY_RE.findall(ideas)), quotes=f"{found}/{total}", prompt_sha=prompt_sha,
                         agent=agent, model=model, effort=args.effort)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out.write_text(fm + "\n\n" + ideas + "\n", encoding="utf-8")
        print(f"  -> {out.name} (quotes found {found}/{total})")
        for pr in problems:
            print(f"     - {pr}")
        if args.sleep:
            time.sleep(args.sleep)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
