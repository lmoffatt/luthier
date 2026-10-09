#!/usr/bin/env python3
"""Extract the ideas of Luthier from the voice notes of each day, all the notes of a day in one call.

The transcripts `.md` of the input directory (default record/audios) are grouped by the date in
their name; for every day, the prompt `extract_ideas_day_v1` is run once through the `claude` (or
`codex`) command line with the day's notes in order, and the ideas are written to
`<output-dir>/<date>_<prompt>_<agent>_<model>_ideas.md`. The per-note counterpart is
`extract_ideas.py`; this one exists because Luciano records in bursts, and an idea started in one
note is restated or corrected in the next.

The frontmatter of the output is written here, deterministically: the date, every note with its
sha256 and duration, the number of ideas, the prompt and its sha256, agent, model, and the count
of quotes found verbatim in the transcript they cite. The model writes only the body.

Idempotent: a day whose output exists and lists the same notes with the same hashes is skipped
(unless --force); a day with a new or changed note is redone, since its output no longer covers
its inputs. Luciano runs it, as he runs extract_ideas.py.

After each call every quote of the body is looked for in the note it cites, with whitespace
collapsed and both texts in Unicode's composed form; the quotes not found are printed, and the
counts go to the frontmatter. --check-only runs that check on existing outputs, without the model.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "record" / "audios"
DEFAULT_OUTPUT = REPO_ROOT / "record" / "ideas"
DEFAULT_PROMPT = REPO_ROOT / "prompts" / "extract_ideas_day_v1.md"
PLACEHOLDER = "<<<TRANSCRIPCIONES>>>"
MODE = "editor"

DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5.4-mini"
DEFAULT_TIMEOUT = 900.0

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
ARCHIVO_RE = re.compile(r"^\s*\*\*Archivo:\*\*\s*(.+?)\s*$", re.MULTILINE)
DURACION_RE = re.compile(r"^\s*\*\*Duraci[óo]n:\*\*\s*(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"\A\s*```[a-zA-Z]*\s*\n")
FENCE_CLOSE_RE = re.compile(r"\n```\s*\Z")
IDEA_HEADING_RE = re.compile(r"^###\s+\S", re.MULTILINE)
TIMESTAMP_RE = re.compile(r"\[\d{1,2}:\d{2}(?::\d{2})?\]")
# - **Quote**: "words" (`file.mp3` `[mm:ss]`)
QUOTE_RE = re.compile(
    r"^\s*-\s*\*\*Quote\*\*:\s*\"(?P<text>.*?)\"\s*\(\s*`(?P<file>[^`]+)`\s*`\[(?P<ts>[^\]]+)\]`\s*\)",
    re.MULTILINE | re.DOTALL,
)
SHA_LINE_RE = re.compile(r"^\s*sha256:\s*([0-9a-f]{64})\s*$", re.MULTILINE)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directory", type=Path, nargs="?", default=DEFAULT_INPUT,
                   help=f"Directory with the transcripts .md (default: {DEFAULT_INPUT}).")
    p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT,
                   help=f"Output directory (default: {DEFAULT_OUTPUT}).")
    p.add_argument("--prompt", type=Path, default=DEFAULT_PROMPT,
                   help=f"Prompt file (must contain {PLACEHOLDER}).")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto",
                   help="Command line to use; 'auto' prefers claude and falls back to codex.")
    p.add_argument("--model", default=None, help="Model; default by command line.")
    p.add_argument("--agent", default=None, help="Agent name in the frontmatter; default by command line.")
    p.add_argument("--days", nargs="*", default=None,
                   help="Only these dates (YYYY-MM-DD); default every day found.")
    p.add_argument("--force", action="store_true", help="Redo a day even when its output covers its notes.")
    p.add_argument("--dry-run", action="store_true", help="List the days and their notes without calling the model.")
    p.add_argument("--check-only", action="store_true",
                   help="Only check the quotes of the existing outputs against the transcripts.")
    p.add_argument("--sleep", type=float, default=0.0, help="Pause between calls (seconds).")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Timeout per call (seconds, default {DEFAULT_TIMEOUT:.0f}); a day is several notes.")
    return p.parse_args(argv)


def _resolve_cli(choice: str) -> str:
    if choice == "claude":
        if shutil.which("claude") is None:
            raise RuntimeError("claude is not in the PATH")
        return "claude"
    if choice == "codex":
        if shutil.which("codex") is None:
            raise RuntimeError("codex is not in the PATH")
        return "codex"
    if shutil.which("claude"):
        return "claude"
    if shutil.which("codex"):
        return "codex"
    raise RuntimeError("neither claude nor codex is in the PATH")


def _slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "x"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _run_claude(prompt_text: str, model: str, timeout: float) -> str:
    proc = subprocess.run(
        ["claude", "-p", "--model", model, "--output-format", "text",
         "--no-session-persistence", "--tools", ""],
        input=prompt_text, capture_output=True, text=True, timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "claude failed")
    return proc.stdout


def _run_codex(prompt_text: str, model: str, timeout: float, workdir: Path) -> str:
    with tempfile.NamedTemporaryFile("w+", suffix=".txt", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        proc = subprocess.run(
            ["codex", "exec", "--skip-git-repo-check", "--color", "never",
             "--sandbox", "read-only", "-C", str(workdir),
             "--output-last-message", str(tmp_path), "-m", model, "-"],
            input=prompt_text, capture_output=True, text=True, timeout=timeout,
        )
        if proc.returncode != 0:
            raise RuntimeError((proc.stderr or proc.stdout).strip() or "codex failed")
        return tmp_path.read_text(encoding="utf-8")
    finally:
        tmp_path.unlink(missing_ok=True)


def _clean_body(raw: str) -> str:
    body = raw.strip()
    body = FRONTMATTER_RE.sub("", body)          # drop any frontmatter the model wrote
    body = FENCE_OPEN_RE.sub("", body)
    body = FENCE_CLOSE_RE.sub("", body)
    return body.strip()


class Note:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.raw = path.read_bytes()
        self.text = self.raw.decode("utf-8")
        self.sha256 = _sha256(self.raw)
        am = ARCHIVO_RE.search(self.text)
        self.audio = am.group(1).strip() if am else f"{path.stem}.mp3"
        dm = DURACION_RE.search(self.text)
        self.duration = dm.group(1).strip() if dm else ""
        fm = DATE_RE.search(path.stem)
        self.date = fm.group(1) if fm else ""


def _group_by_day(directory: Path) -> dict[str, list[Note]]:
    days: dict[str, list[Note]] = defaultdict(list)
    for p in sorted(directory.glob("*.md")):
        if not p.is_file():
            continue
        note = Note(p)
        if not note.date:
            print(f"WARNING: no date in the name, skipped: {p.name}", file=sys.stderr)
            continue
        days[note.date].append(note)
    return dict(sorted(days.items()))


def _assemble_input(notes: list[Note]) -> str:
    parts = []
    for i, n in enumerate(notes, 1):
        parts.append(f"## Note {i} of {len(notes)}: {n.audio}\n\n{n.text.strip()}\n")
    return "\n".join(parts)


def _build_frontmatter(*, date: str, notes: list[Note], n_ideas: int, quotes_found: int,
                       quotes_total: int, prompt_id: str, prompt_sha: str, agent: str,
                       model: str) -> str:
    lines = ["---", f"date: {date}", "notes:"]
    for n in notes:
        lines += [f"  - audio: {n.audio}", f"    transcript: {n.path.name}",
                  f"    duration: {n.duration}", f"    sha256: {n.sha256}"]
    lines += [
        f"ideas: {n_ideas}",
        f"quotes_found: {quotes_found}/{quotes_total}",
        f"generated_by: {prompt_id}",
        f"prompt_sha256: {prompt_sha}",
        f"mode: {MODE}",
        f"agent: {agent}",
        f"model: {model}",
        "---",
    ]
    return "\n".join(lines)


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split())


def check_quotes(body: str, notes: list[Note]) -> tuple[int, int, list[str]]:
    """Return (found, total, problems): each quote looked for in the transcript of the note it cites."""
    by_audio = {n.audio: n for n in notes}
    by_stem = {n.path.stem: n for n in notes}
    found, problems = 0, []
    quotes = list(QUOTE_RE.finditer(body))
    for m in quotes:
        text, file_name, ts = m.group("text"), m.group("file").strip(), m.group("ts")
        note = by_audio.get(file_name) or by_stem.get(Path(file_name).stem)
        if note is None:
            problems.append(f"[{ts}] cites a note not in this day: {file_name}")
            continue
        haystack = _norm(TIMESTAMP_RE.sub(" ", note.text))
        if _norm(text) in haystack:
            found += 1
        else:
            problems.append(f"not found in {note.path.name} [{ts}]: \"{text[:80]}\"")
    return found, len(quotes), problems


def _existing_hashes(out: Path) -> set[str]:
    if not out.exists() or out.stat().st_size == 0:
        return set()
    text = out.read_text(encoding="utf-8")
    fm = FRONTMATTER_RE.match(text)
    return set(SHA_LINE_RE.findall(fm.group(0))) if fm else set()


def _rewrite_quote_counts(out: Path, found: int, total: int) -> None:
    text = out.read_text(encoding="utf-8")
    new, n = re.subn(r"^quotes_found:.*$", f"quotes_found: {found}/{total}", text, count=1, flags=re.MULTILINE)
    if n:
        out.write_text(new, encoding="utf-8")


def main(argv: list[str]) -> int:
    args = _parse_args(argv)

    if not args.directory.is_dir():
        print(f"ERROR: not a directory: {args.directory}", file=sys.stderr)
        return 2
    if not args.prompt.is_file():
        print(f"ERROR: prompt not found: {args.prompt}", file=sys.stderr)
        return 2
    prompt_bytes = args.prompt.read_bytes()
    prompt_template = prompt_bytes.decode("utf-8")
    prompt_sha = _sha256(prompt_bytes)
    if PLACEHOLDER not in prompt_template:
        print(f"ERROR: the prompt does not contain {PLACEHOLDER}", file=sys.stderr)
        return 2

    days = _group_by_day(args.directory)
    if args.days:
        unknown = [d for d in args.days if d not in days]
        if unknown:
            print(f"ERROR: no notes on {', '.join(unknown)}", file=sys.stderr)
            return 2
        days = {d: days[d] for d in args.days}
    if not days:
        print(f"No transcripts .md in {args.directory}", file=sys.stderr)
        return 1

    if args.check_only:
        cli = "none"
        model = args.model or DEFAULT_CLAUDE_MODEL
        agent = args.agent or "claude-code"
    else:
        try:
            cli = _resolve_cli(args.cli)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        model = args.model or (DEFAULT_CLAUDE_MODEL if cli == "claude" else DEFAULT_CODEX_MODEL)
        agent = args.agent or ("claude-code" if cli == "claude" else "codex")
    prompt_id = args.prompt.stem
    tag = f"{prompt_id}_{_slug(agent)}_{_slug(model)}_ideas"
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.check_only:
        bad = 0
        for date, notes in days.items():
            out = args.output_dir / f"{date}_{tag}.md"
            if not out.exists():
                continue
            body = FRONTMATTER_RE.sub("", out.read_text(encoding="utf-8"))
            found, total, problems = check_quotes(body, notes)
            _rewrite_quote_counts(out, found, total)
            print(f"{out.name}: quotes found {found}/{total}")
            for pr in problems:
                print(f"  - {pr}")
            bad += len(problems)
        return 1 if bad else 0

    jobs, skipped, redo = [], 0, 0
    for date, notes in days.items():
        out = args.output_dir / f"{date}_{tag}.md"
        have = _existing_hashes(out)
        want = {n.sha256 for n in notes}
        if have and not args.force:
            if have == want:
                skipped += 1
                continue
            redo += 1
        jobs.append((date, notes, out))

    n_notes = sum(len(v) for v in days.values())
    print(f"Days: {len(days)} ({n_notes} notes) | done: {skipped} | pending: {len(jobs)}"
          + (f", of which {redo} redone because their notes changed" if redo else ""))
    print(f"CLI: {cli} | model: {model} | agent: {agent} | prompt: {prompt_id} ({prompt_sha[:12]})")
    if not jobs:
        print("Nothing to do.")
        return 0
    if args.dry_run:
        for i, (date, notes, out) in enumerate(jobs, 1):
            words = sum(len(n.text.split()) for n in notes)
            print(f"[dry {i:02d}/{len(jobs):02d}] {date}: {len(notes)} notes, {words} words -> {out.name}")
            for n in notes:
                print(f"      {n.path.name} ({n.duration})")
        return 0

    generated, failed = 0, []
    for i, (date, notes, out) in enumerate(jobs, 1):
        try:
            user_message = prompt_template.replace(PLACEHOLDER, _assemble_input(notes))
            print(f"[{i:02d}/{len(jobs):02d}] {date}: {len(notes)} notes", flush=True)
            if cli == "claude":
                raw = _run_claude(user_message, model, args.timeout)
            else:
                raw = _run_codex(user_message, model, args.timeout, REPO_ROOT)
            body = _clean_body(raw)
            n_ideas = len(IDEA_HEADING_RE.findall(body))
            found, total, problems = check_quotes(body, notes)
            frontmatter = _build_frontmatter(
                date=date, notes=notes, n_ideas=n_ideas, quotes_found=found, quotes_total=total,
                prompt_id=prompt_id, prompt_sha=prompt_sha, agent=agent, model=model,
            )
            out.write_text(f"{frontmatter}\n\n{body}\n", encoding="utf-8")
            generated += 1
            print(f"  -> {out.name} ({n_ideas} ideas, quotes found {found}/{total})", flush=True)
            for pr in problems:
                print(f"     - {pr}", flush=True)
            if args.sleep:
                time.sleep(args.sleep)
        except Exception as exc:  # noqa: BLE001
            failed.append((date, str(exc)))
            print(f"  -> FAILED {date}: {exc}", file=sys.stderr, flush=True)

    print(f"\nSummary: generated {generated} | failed {len(failed)}")
    for date, reason in failed:
        print(f"  - {date}: {reason}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
