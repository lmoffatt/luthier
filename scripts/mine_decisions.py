#!/usr/bin/env python3
"""Mine the decision units of the Claude Code transcripts: every turn of Luciano's followed by an
action before his next turn. Mechanical, no model.

Luciano barely writes code; models write it. So a decision leaves its whole trace in the session
transcript (Luciano, 2026-10-09: "la historia esta mas en los chats en .claude que en git"): the
model's proposal, his turn (a choice, a correction, or a short confirmation), and the act that
follows (files edited, commands run, a commit). Git keeps only the act, several decisions at once.

A unit holds: the session and the line of Luciano's turn, its time and text; the model's last text
before it (the proposal it answers); the actions until his next turn (tool, files, the start of a
command, the line); the commits made (hash and message, read from the command's output); the areas
the files belong to (language, method, other; the patterns are parameters); and the form of his
turn (short, at most --short-words words, or long). Whether a short turn confirms a model's
proposal is a heuristic, recorded as such; who decided is settled later, case by case.

Sources: by default the transcripts pinned in `~/Projects/IA_chat/raw/claude-code/` (sha256 in its
manifest); with --live, `~/.claude/projects/` as it is now, each file's sha256 recorded. Subagent
transcripts are not read; a turn followed by an agent or a workflow counts as delegated action.
Events repeated across files (a resumed session copies its history) are counted once, by uuid.

The output goes to a public repository: a unit whose texts contain a word of
`scripts/export_chat.private` keeps its metadata and loses its texts.

Writes `<output-dir>/decision_units.jsonl` and `decision_units.md`. Luciano runs it.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

VERSION = "mine_decisions v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
IACHAT = Path.home() / "Projects" / "IA_chat"
LIVE = Path.home() / ".claude" / "projects"
DEFAULT_PROJECTS = ["-home-lmoffatt-Projects-luthier", "-home-lmoffatt-Projects-sonolocalizacion"]
DEFAULT_OUTPUT = REPO_ROOT / "record" / "validation"
PRIVATE = REPO_ROOT / "scripts" / "export_chat.private"
LANGUAGE = [r"(^|/)docs/spec/", r"(^|/)docs/semantica/", r"(^|/)docs/guide/", r"(^|/)docs/rationale/",
            r"(^|/)src/luthier/", r"\.lut$", r"(^|/)tests/spec/", r"(^|/)examples/"]
METHOD = [r"(^|/)record/", r"(^|/)CLAUDE\.md$", r"(^|/)prompts/", r"(^|/)scripts/", r"(^|/)docs/[^/]*\.md$",
          r"(^|/)\.claude/", r"/memory/"]
HARNESS = re.compile(r"^\s*(<|\[Request interrupted|Your response above was cut off|Continue from where you left off"
                     r"|Caveat:|This session is being continued|Another Claude session sent)")
GIT_WRITE = re.compile(r"\bgit (commit|mv|rm)\b")
REDIRECT = re.compile(r"(?:^|[^0-9&>])>{1,2}\s*([\"']?)([^\s\"';|&<>)]+)\1")
OTHER_WRITE = re.compile(r"\bsed -i\b|\btee\b|write_text\(|open\([^)]*,\s*['\"][wa]|\bmv\s|\brm\s")
COMMIT_OUT = re.compile(r"^\[[^\]]*? ([0-9a-f]{7,40})\] (.+)$|^([0-9a-f]{7,12}) (\S.*)$", re.M)
DEFAULT_REPOS = [Path.home() / "Projects" / "luthier", Path.home() / "Projects" / "sonolocalizacion"]


def scratch(path: str) -> bool:
    return path.startswith(("/tmp", "/dev/")) or "/scratchpad/" in path or path in ("&1", "&2")


def bash_write(cmd: str) -> tuple[bool, list[str]]:
    """Whether a command writes outside scratch space, and the files it names as targets."""
    targets = [m.group(2) for m in REDIRECT.finditer(cmd)]
    real = [t for t in targets if not scratch(t) and not t.startswith("$")]
    if GIT_WRITE.search(cmd) or real:
        return True, real
    if OTHER_WRITE.search(cmd) and "/tmp/" not in cmd and "scratchpad" not in cmd:
        return True, []
    return False, []


def commit_files(h: str, repos: list[Path]) -> tuple[str, list[str]]:
    import subprocess
    for r in repos:
        out = subprocess.run(["git", "-C", str(r), "show", "--name-only", "--format=", h], capture_output=True, text=True)
        if out.returncode == 0:
            return r.name, [l for l in out.stdout.splitlines() if l.strip()]
    return "", []
DELEGATE = ("Agent", "Workflow", "Task")
EDIT_TOOLS = ("Edit", "Write", "NotebookEdit", "MultiEdit")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def private_words() -> list[re.Pattern]:
    if not PRIVATE.exists():
        return []
    ws = [w.strip() for w in PRIVATE.read_text(encoding="utf-8").splitlines() if w.strip() and not w.startswith("#")]
    return [re.compile(r"(?<!\w)" + re.escape(unicodedata.normalize("NFC", w)) + r"(?!\w)", re.I) for w in ws]


def sources(projects: list[str], live: bool, folder: Path | None = None) -> list[tuple[Path, str]]:
    """(path, sha256) of every main-session transcript of the projects; the newest pin per session."""
    out = []
    if folder is not None:
        return [(f, sha256(f)) for f in sorted(folder.iterdir()) if f.name.endswith((".jsonl", ".jsonl.gz"))]
    if live:
        for p in projects:
            for f in sorted((LIVE / p).glob("*.jsonl")):
                out.append((f, sha256(f)))
        return out
    best: dict[str, Path] = {}
    for p in projects:
        for f in sorted((IACHAT / "raw" / "claude-code").glob(f"*/{p}/*.jsonl.gz")):
            sid = f.name.split(".")[0]
            if sid not in best or f.parent.parent.name > best[sid].parent.parent.name:
                best[sid] = f
    for f in sorted(best.values()):
        out.append((f, sha256(f)))
    return out


def read_events(path: Path) -> list[tuple[int, dict]]:
    opener = gzip.open if path.suffix == ".gz" else open
    out = []
    with opener(path, "rt", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            try:
                out.append((n, json.loads(line)))
            except json.JSONDecodeError:
                continue
    return out


def luciano_text(ev: dict) -> str | None:
    """The text Luciano typed, or None for tool results, harness messages and meta events."""
    if ev.get("type") != "user" or ev.get("isSidechain") or ev.get("isMeta"):
        return None
    c = ev.get("message", {}).get("content")
    if isinstance(c, str):
        parts = [c]
    elif isinstance(c, list):
        if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
            return None
        parts = [x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text"]
    else:
        return None
    parts = [p for p in parts if p.strip() and not HARNESS.match(p)]
    text = "\n".join(parts).strip()
    return text or None


def area_of(path: str, language: list[str], method: list[str]) -> str:
    if any(re.search(p, path) for p in language):
        return "language"
    if any(re.search(p, path) for p in method):
        return "method"
    return "other"


def mine_session(events: list[tuple[int, dict]], seen_uuids: set, args) -> list[dict]:
    units, cur, last_text = [], None, None
    pending_cmd: dict[str, dict] = {}
    for n, ev in events:
        uid = ev.get("uuid")
        if uid and uid in seen_uuids:
            continue
        if uid:
            seen_uuids.add(uid)
        t = luciano_text(ev)
        if t is not None:
            if cur and cur["actions"]:
                units.append(cur)
            cur = {"line": n, "uuid": uid, "time": ev.get("timestamp", ""), "text": t,
                   "proposal": last_text, "actions": [], "commits": []}
            continue
        c = ev.get("message", {}).get("content") if isinstance(ev.get("message"), dict) else None
        if ev.get("type") == "assistant" and isinstance(c, list):
            texts = [x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text" and x.get("text", "").strip()]
            if texts:
                last_text = {"line": n, "time": ev.get("timestamp", ""), "text": "\n".join(texts)}
            for x in c:
                if not (isinstance(x, dict) and x.get("type") == "tool_use") or cur is None:
                    continue
                name, inp = x.get("name"), x.get("input", {}) or {}
                act = None
                if name in EDIT_TOOLS:
                    f = inp.get("file_path") or inp.get("notebook_path") or ""
                    if not scratch(f):
                        act = {"tool": name, "files": [f]}
                elif name == "Bash":
                    writes, targets = bash_write(inp.get("command", ""))
                    if writes:
                        act = {"tool": "Bash", "files": targets, "command": inp.get("command", "")[:200]}
                        if GIT_WRITE.search(inp.get("command", "")):
                            pending_cmd[x.get("id", "")] = act
                elif name in DELEGATE:
                    act = {"tool": name, "files": [], "command": str(inp.get("description", ""))[:200]}
                if act:
                    act.update(line=n, time=ev.get("timestamp", ""))
                    cur["actions"].append(act)
        if ev.get("type") == "user" and isinstance(c, list) and cur is not None:
            for x in c:
                if isinstance(x, dict) and x.get("type") == "tool_result" and x.get("tool_use_id") in pending_cmd:
                    out = x.get("content")
                    out = out if isinstance(out, str) else " ".join(y.get("text", "") for y in out or [] if isinstance(y, dict))
                    for m in COMMIT_OUT.finditer(out):
                        h, msg = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
                        if all(c["hash"] != h for c in cur["commits"]):
                            cur["commits"].append({"hash": h, "message": msg[:200], "line": n})
    if cur and cur["actions"]:
        units.append(cur)
    return units


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--projects", nargs="*", default=DEFAULT_PROJECTS, help="Claude Code project folders")
    ap.add_argument("--live", action="store_true", help="read ~/.claude/projects instead of the pinned copies")
    ap.add_argument("--transcripts", type=Path, default=None, help="read the transcripts of this folder instead")
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--short-words", type=int, default=6, help="a turn of at most this many words is short")
    ap.add_argument("--proposal-chars", type=int, default=3000, help="how much of the model's proposal is kept")
    ap.add_argument("--text-chars", type=int, default=3000, help="how much of Luciano's turn is kept")
    ap.add_argument("--language", nargs="*", default=LANGUAGE, help="path patterns of the language's files")
    ap.add_argument("--method", nargs="*", default=METHOD, help="path patterns of the method's files")
    ap.add_argument("--repos", nargs="*", type=Path, default=DEFAULT_REPOS, help="where a commit's files are looked up")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args(argv)
    srcs = sources(args.projects, args.live, args.transcripts)
    if not srcs:
        print("no transcripts found", file=sys.stderr)
        return 1
    priv = private_words()
    seen: set = set()
    rows = []
    for path, sha in sorted(srcs, key=lambda s: s[0].name):
        events = read_events(path)
        sid = next((e.get("sessionId") for _, e in events if e.get("sessionId")), path.name.split(".")[0])
        for u in mine_session(events, seen, args):
            for c in u["commits"]:
                c["repo"], c["files"] = commit_files(c["hash"], args.repos)
            files = sorted({f for a in u["actions"] for f in a["files"] if f} | {f for c in u["commits"] for f in c["files"]})
            areas = sorted({area_of(f, args.language, args.method) for f in files}) or ["unknown"]
            words = len(u["text"].split())
            prop = u["proposal"]
            try:
                src = str(path.relative_to(IACHAT))
            except ValueError:
                src = str(path)
            row = {"id": f"{sid[:8]}:{u['line']}", "session": sid, "project": next((p for p in args.projects if p in str(path)), ""),
                   "source": src, "source_sha256": sha,
                   "time": u["time"], "luciano": {"line": u["line"], "uuid": u["uuid"], "words": words,
                                                  "text": u["text"][:args.text_chars]},
                   "proposal": ({"line": prop["line"], "time": prop["time"], "text": prop["text"][-args.proposal_chars:]}
                                if prop else None),
                   "actions": u["actions"], "files": files, "areas": areas, "commits": u["commits"],
                   "form": "short" if words <= args.short_words else "long",
                   "heuristic_confirmation": words <= args.short_words and prop is not None}
            blob = row["luciano"]["text"] + " " + (prop["text"] if prop else "") + " " + " ".join(
                a.get("command", "") for a in u["actions"]) + " " + " ".join(c["message"] for c in u["commits"])
            hits = [p.pattern for p in priv if p.search(unicodedata.normalize("NFC", blob))]
            if hits:
                row["withheld"] = f"private words ({len(hits)})"
                row["luciano"]["text"] = "[withheld]"
                if row["proposal"]:
                    row["proposal"]["text"] = "[withheld]"
                for a in row["actions"]:
                    if "command" in a:
                        a["command"] = "[withheld]"
                for c in row["commits"]:
                    c["message"] = "[withheld]"
            rows.append(row)
    rows.sort(key=lambda r: (r["time"], r["id"]))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "decision_units.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    by = Counter((r["project"].split("-")[-1], "+".join(r["areas"]), r["form"]) for r in rows)
    L = [f"# Decision units mined from the Claude Code transcripts, {args.date}", "",
         f"Written by `scripts/mine_decisions.py` ({VERSION}), no model. A unit is a turn of Luciano's followed by an action",
         "before his next turn. Sources: " + ("the live transcripts" if args.live else "the copies pinned in IA_chat") +
         f", {len(srcs)} sessions, each by sha256 in the jsonl. Short turns have at most {args.short_words} words; whether one",
         "confirms a model's proposal is a heuristic. Units with a private word keep only their metadata.", "",
         f"Units: {len(rows)}; with a commit {sum(bool(r['commits']) for r in rows)}; withheld {sum('withheld' in r for r in rows)}.", "",
         "| project | areas | form | units |", "|---|---|---|---|"]
    for (p, a, f), n in sorted(by.items()):
        L.append(f"| {p} | {a} | {f} | {n} |")
    L += ["", "## Units", ""]
    for r in rows:
        t = r["luciano"]["text"].replace("\n", " ")
        L.append(f"- {r['time'][:16]} `{r['id']}` {r['form']}, {'+'.join(r['areas'])}"
                 + (f", commit {', '.join(c['hash'][:7] for c in r['commits'])}" if r["commits"] else "")
                 + f": {t[:160]}")
    (args.output_dir / "decision_units.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(rows)} units from {len(srcs)} sessions -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
