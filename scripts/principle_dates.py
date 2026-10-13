#!/usr/bin/env python3
"""The dates of each principle, for the validation against real decisions (step 2 of
record/plan/principles/plan-principles-validation-2026-10-09-execution.md). Mechanical, no model.

For each principle of `record/principles.md`:
- explicit: the time of each source its entry cites (a turn of a chat, or a line of a committed
  document, dated by the commit that introduced the line); by default the earliest of them. D1 as
  Luciano marked it: an earlier formulation of his counts instead when it already says which way to
  go; the script lists, as candidates, his earlier rows in the timeline that share the most terms
  with the principle's quote and statement, and he marks one or none.
- operative, per repository: the first commit that put the principle's id in that repository's
  `CLAUDE.md` (or, for a repository whose `CLAUDE.md` points to its own principles file, in that
  file); the first write of `~/.claude/CLAUDE.md` whose text carries the principle's statement; and,
  as candidates for his mark, the memory notes of the project that share the most terms with the
  principle, with the time each was first written. Transcripts are read from every account folder
  given (--accounts).

Every time is converted to UTC. Writes `record/validation/principle_dates.json` and
`principle_dates.md`, the second with a `Mark:` line per principle for Luciano.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import principles_ledger as pl  # noqa: E402

VERSION = "principle_dates v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS = Path.home() / "Projects"
DEFAULT_ACCOUNTS = [Path.home() / ".claude", Path.home() / ".claude-databaum"]
DEFAULT_REPOS = {"luthier": "-home-lmoffatt-Projects-luthier", "sonolocalizacion": "-home-lmoffatt-Projects-sonolocalizacion"}
REF_RE = re.compile(r"(chat:[0-9a-f]{8}:\d+(?:-\d+)?|[a-z_]+@[0-9a-f]{7,40}:[^\s:]+:\d+(?:-\d+)?)")
STOP = set("the a an of to in is and or for on it be by as at that this with not are its from what his he no one "
           "de la el en y que los las un una es no se por con para lo su al del como".split())


def utc(ts: str) -> str:
    """An ISO time, with Z or an offset, in UTC to the minute."""
    d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def terms(text: str) -> set[str]:
    t = unicodedata.normalize("NFKD", str(text).lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return {w for w in re.findall(r"[a-z]{4,}", t) if w not in STOP}


def transcript(s8: str, accounts: list[Path]) -> Path | None:
    for a in accounts:
        for f in (a / "projects").glob(f"*/{s8}*.jsonl"):
            return f
    return None


def account_label(path: Path, accounts: list[Path]) -> str:
    """Which account a transcript is in, by its position in --accounts, not by its folder's name
    (a folder's name may carry a private word)."""
    for i, a in enumerate(accounts, 1):
        if str(path).startswith(str(a)):
            return f"account {i}, {path.parent.name}/{path.name}"
    return path.name


def chat_time(ref: str, accounts: list[Path]) -> tuple[str, str]:
    _, s8, line = ref.split(":")
    n = int(line.split("-")[0])
    f = transcript(s8, accounts)
    if f is None:
        return "", f"no transcript for {s8}"
    with f.open(encoding="utf-8") as fh:
        for i, l in enumerate(fh, 1):
            if i == n:
                try:
                    return utc(json.loads(l).get("timestamp", "")), account_label(f, accounts)
                except (ValueError, json.JSONDecodeError):
                    return "", f"line {n} of {f.name} has no time"
    return "", f"{f.name} has no line {n}"


def git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def doc_time(ref: str) -> tuple[str, str]:
    """repo@commit:path:line -> the time of the commit that introduced that line, as of that commit."""
    m = re.match(r"([a-z_]+)@([0-9a-f]+):(.+):(\d+)", ref)
    repo, commit, path, line = PROJECTS / m.group(1), m.group(2), m.group(3), m.group(4)
    out = git(repo, "blame", "--porcelain", "-L", f"{line},{line}", commit, "--", path)
    h = out.split(" ", 1)[0] if out else ""
    t = git(repo, "show", "-s", "--format=%cI", h).strip() if h else ""
    return (utc(t), f"{m.group(1)}@{h[:7]}") if t else ("", f"cannot blame {ref}")


def first_commit_with(repo: Path, needle: str, paths: list[str]) -> tuple[str, str]:
    out = git(repo, "log", "--reverse", "--format=%h %cI", "-S", needle, "--", *paths)
    line = out.splitlines()[0] if out.strip() else ""
    if not line:
        return "", ""
    h, t = line.split(" ", 1)
    return utc(t), f"{repo.name}@{h}"


REDIRECT = re.compile(r"(?:>{1,2}|\btee\s+(?:-a\s+)?)\s*([\"']?)([^\s\"';|&<>)]+)\1")
CD = re.compile(r"\bcd\s+([\"']?)([^\s\"';&|]+)\1")


def bash_targets(cmd: str) -> list[str]:
    """The files a command writes by redirection or tee, made absolute against a preceding cd."""
    out, cwd = [], ""
    for part in re.split(r"&&|;|\n", cmd):
        m = CD.search(part)
        if m:
            cwd = m.group(2).replace("~", str(Path.home()))
        for t in REDIRECT.finditer(part):
            f = t.group(2).replace("~", str(Path.home()))
            if f.startswith("/dev/") or f.startswith("&"):
                continue
            if "$" in f:
                continue
            out.append(f if f.startswith("/") else str(Path(cwd or ".") / f))
    return out


def writes(accounts: list[Path], path_re: re.Pattern, prefilter: str = "") -> list[dict]:
    """Every write of a file matching path_re in the transcripts: time, file, text written, session.
    prefilter is a cheaper text a transcript line must contain (a folder name) when the path itself
    may be relative."""
    out = []
    pre = re.compile(re.escape(prefilter)) if prefilter else path_re
    for acct, a in enumerate(accounts, 1):
        for f in (a / "projects").glob("*/*.jsonl"):
            with f.open(encoding="utf-8") as fh:
                for n, l in enumerate(fh, 1):
                    if '"tool_use"' not in l or not (path_re.search(l) or pre.search(l)):
                        continue
                    try:
                        ev = json.loads(l)
                    except json.JSONDecodeError:
                        continue
                    for x in ev.get("message", {}).get("content", []) or []:
                        if not (isinstance(x, dict) and x.get("type") == "tool_use"):
                            continue
                        inp = x.get("input", {}) or {}
                        fp = inp.get("file_path", "")
                        txt = inp.get("content") or inp.get("new_string") or ""
                        cmd = inp.get("command", "")
                        if fp and path_re.search(fp):
                            out.append({"time": utc(ev["timestamp"]), "file": fp, "text": txt, "source": f"chat:{f.stem[:8]}:{n}",
                                        "account": acct})
                        elif cmd:
                            for target in bash_targets(cmd):
                                if path_re.search(target):
                                    out.append({"time": utc(ev["timestamp"]), "file": target, "text": cmd,
                                                "source": f"chat:{f.stem[:8]}:{n}", "account": acct})
    return sorted(out, key=lambda w: w["time"])


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--principles", type=Path, default=pl.DEFAULT_PRINCIPLES)
    ap.add_argument("--timeline", type=Path, default=REPO_ROOT / "record" / "ideas" / "timeline.jsonl")
    ap.add_argument("--accounts", nargs="*", type=Path, default=DEFAULT_ACCOUNTS)
    ap.add_argument("--output-dir", type=Path, default=REPO_ROOT / "record" / "validation")
    ap.add_argument("--candidates", type=int, default=3, help="earlier rows and memory notes listed per principle")
    ap.add_argument("--min-shared", type=int, default=3, help="terms a candidate must share with the principle")
    ap.add_argument("--global-share", type=float, default=0.7,
                    help="share of the statement's terms a write of ~/.claude/CLAUDE.md must carry to count")
    args = ap.parse_args(argv)

    principles = pl.parse_entries(args.principles.read_text(encoding="utf-8"), pl.P_HEAD_RE)
    rows = [json.loads(l) for l in args.timeline.read_text(encoding="utf-8").splitlines() if l.strip()]
    # each account has its own global CLAUDE.md and its own memory per project; a write belongs to the
    # account whose folder the written file is in, whichever account's session wrote it
    def owner(path: str) -> int:
        for i, a in enumerate(args.accounts, 1):
            if path.startswith(str(a) + "/"):
                return i
        return 0
    global_writes = {}
    for i, a in enumerate(args.accounts, 1):
        # the transcript may name the file with ~, so the cheap filter is the file's name alone
        global_writes[i] = [w for w in writes(args.accounts, re.compile(re.escape(str(a)) + r"/CLAUDE\.md"), prefilter="/CLAUDE.md")
                            if owner(w["file"]) == i]
    memory = {}
    for repo, folder in DEFAULT_REPOS.items():
        notes = {}
        for w in writes(args.accounts, re.compile(re.escape(folder) + r"/memory/[\w.-]+\.md"), prefilter=f"{folder}/memory"):
            name, acct = Path(w["file"]).name, owner(w["file"])
            if name != "MEMORY.md" and acct and (acct, name) not in notes:
                notes[(acct, name)] = w
        for i, a in enumerate(args.accounts, 1):
            for p in (a / "projects" / folder / "memory").glob("*.md"):
                if (i, p.name) in notes:
                    notes[(i, p.name)]["now"] = p.read_text(encoding="utf-8")
        memory[repo] = notes

    out, problems = {}, []
    for pid, e in sorted(principles.items(), key=lambda kv: int(kv[0][1:])):
        refs = REF_RE.findall(e.get("Source", ""))
        dated = []
        for r in refs:
            t, where = chat_time(r, args.accounts) if r.startswith("chat:") else doc_time(r)
            dated.append({"ref": r, "time": t, "where": where})
            if not t:
                problems.append(f"{pid}: {where}")
        times = [d["time"] for d in dated if d["time"]]
        explicit = min(times) if times else ""
        want = terms(e["statement"] + " " + e.get("Quote", ""))
        earlier = []
        for r in rows:
            if r.get("who") == "Luciano" and r.get("time_utc") and explicit and r["time_utc"][:16] < explicit[:16]:
                shared = want & terms(r.get("quote", "") + " " + r.get("what", ""))
                if len(shared) >= args.min_shared:
                    earlier.append((len(shared), r))
        earlier = [{"row": r["id"], "time": r["time_utc"], "quote": r["quote"][:200], "shared": n}
                   for n, r in sorted(earlier, key=lambda x: (-x[0], x[1]["time_utc"]))[:args.candidates]]
        operative = {}
        for repo in DEFAULT_REPOS:
            t, src = first_commit_with(PROJECTS / repo, f"- {pid} ", ["CLAUDE.md", "docs/principles.md", "record/principles.md"]
                                       if repo == "sonolocalizacion" else ["CLAUDE.md"])
            notes = []
            for (acct, name), w in memory[repo].items():
                shared = want & terms(w.get("now", "") or w["text"])
                if len(shared) >= args.min_shared:
                    notes.append({"note": name, "account": acct, "first_written": w["time"], "source": w["source"],
                                  "shared": len(shared)})
            notes = sorted(notes, key=lambda x: -x["shared"])[:args.candidates]
            operative[repo] = {"claude_md": {"time": t, "source": src} if t else None, "memory_candidates": notes}
        stmt = terms(e["statement"])
        glob_ = {}
        for i, ws in global_writes.items():
            g = next((w for w in ws if len(stmt & terms(w["text"])) >= max(3, round(args.global_share * len(stmt)))), None)
            if g:
                glob_[str(i)] = {"time": g["time"], "source": g["source"]}
        out[pid] = {"statement": e["statement"], "quote": e.get("Quote", ""), "sources": dated, "explicit": explicit,
                    "explicit_earlier_candidates": earlier,
                    "operative": operative, "global_claude_md": glob_,
                    "status": "proposed: Luciano marks the explicit date and the memory notes"}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "principle_dates.json").write_text(json.dumps({"version": VERSION, "principles": out, "problems": problems},
                                                                     ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    L = ["# Dates of the principles, for Luciano to mark", "",
         f"Written by `scripts/principle_dates.py` ({VERSION}), no model. Times in UTC. `explicit` is the earliest source of the",
         "principle's entry in record/principles.md; an earlier row of his is listed when it shares terms with the principle, for",
         "you to say whether it already decides (D1). `operative` is the first commit putting the principle's id in that",
         "repository's CLAUDE.md, the first write of ~/.claude/CLAUDE.md carrying its statement, and the memory notes that may",
         "state it (candidates, by shared terms).", "",
         "How to mark, under each principle, on its `Mark:` line, separated by `;`:",
         "`ok` (the explicit date as proposed, no memory note counts); `earlier <row id>` (that earlier row of yours already",
         "decides, so the principle counts from it); `memory <note.md>` (that note states the principle; it counts from the time",
         "it was first written, in the repository it is listed under). Example: `earlier day:2026-10-04:x; memory nunca-hardcodear.md`.", ""]
    for pid, d in out.items():
        L += [f"## {pid} {d['statement']}", "", f"- explicit: {d['explicit'] or '?'} (" + "; ".join(
            f"{s['ref']} {s['time'] or s['where']}" for s in d["sources"]) + ")"]
        for c in d["explicit_earlier_candidates"]:
            L.append(f"  - earlier? {c['time']} `{c['row']}`: \"{c['quote']}\"")
        for repo, o in d["operative"].items():
            cm = o["claude_md"]
            L.append(f"- operative in {repo}: CLAUDE.md {cm['time'] + ' ' + cm['source'] if cm else 'never'}")
            for n in o["memory_candidates"]:
                L.append(f"  - memory? `{n['note']}` of account {n['account']}, first written {n['first_written']}"
                         f" ({n['source']}, {n['shared']} shared terms)")
        for acct, g in d["global_claude_md"].items():
            L.append(f"- operative in every repository of account {acct}: its global CLAUDE.md, {g['time']} ({g['source']})")
        L += ["", "Mark: ", ""]
    if problems:
        L += ["## Problems", ""] + [f"- {p}" for p in problems]
    (args.output_dir / "principle_dates.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(out)} principles; problems: {len(problems)}")
    for p in problems:
        print("  -", p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
