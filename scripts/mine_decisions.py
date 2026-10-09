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
manifest); with --live, `~/.claude/projects/` and the second account's
`~/.claude-databaum/projects/` as they are now, each file's sha256 recorded. A unit records the
repository its session ran in (`session_repo`), whose CLAUDE.md and memory the agent read, and the
reversals found in git: a later commit that removes lines an earlier unit's commit added. Subagent
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
ACCOUNTS = [Path.home() / ".claude", Path.home() / ".claude-databaum"]  # account 1, account 2
LIVE = [a / "projects" for a in ACCOUNTS]
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


def added_and_removed(repo: Path, h: str) -> tuple[dict, dict]:
    """Per file, the lines a commit added and the lines it removed (stripped, non-trivial)."""
    import subprocess
    out = subprocess.run(["git", "-C", str(repo), "show", "--unified=0", "--format=", h], capture_output=True, text=True).stdout
    added, removed, cur = {}, {}, None
    for l in out.splitlines():
        if l.startswith("+++ "):
            cur = l[6:] if l.startswith("+++ b/") else None
        elif l.startswith("--- "):
            continue
        elif cur and l.startswith("+") and len(l.strip("+ \t")) > 3:
            added.setdefault(cur, set()).add(l[1:].strip())
        elif cur and l.startswith("-") and len(l.strip("- \t")) > 3:
            removed.setdefault(cur, set()).add(l[1:].strip())
    return added, removed


def link_reversals(rows: list[dict], repos: list[Path], min_lines: int, min_share: float = 0.5) -> int:
    """A later unit reverses an earlier one when one of its commits removes, from a file, at least
    min_lines lines and at least min_share of the lines a commit of the earlier unit added to that
    file. Lines the later commit writes again (a text moved within the file) do not count."""
    by_repo = {r.name: r for r in repos}
    commits = [(row, c) for row in rows for c in row["commits"] if c.get("repo") in by_repo]
    diffs = {c["hash"]: added_and_removed(by_repo[c["repo"]], c["hash"]) for _, c in commits}
    n = 0
    for i, (ra, ca) in enumerate(commits):
        add_a = diffs[ca["hash"]][0]
        for rb, cb in commits[i + 1:]:
            if rb is ra or cb["repo"] != ca["repo"] or rb["time"] <= ra["time"]:
                continue
            add_b, rem_b = diffs[cb["hash"]]
            best = 0
            for f in add_a.keys() & rem_b.keys():
                gone = (add_a[f] & rem_b[f]) - add_b.get(f, set())
                if len(gone) >= min_lines and len(gone) >= min_share * len(add_a[f]):
                    best = max(best, len(gone))
            if best and all(x["unit"] != rb["id"] for x in ra.get("reversed_by", [])):
                ra.setdefault("reversed_by", []).append({"unit": rb["id"], "commit": cb["hash"], "lines": best})
                rb.setdefault("reverses", []).append({"unit": ra["id"], "commit": ca["hash"], "lines": best})
                n += 1
    return n


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


def account_of(path: Path, manifest: dict[str, str]) -> int:
    """1 or 2: the account a transcript came from, by its path, or by the origin IA_chat recorded for a pin."""
    origin = manifest.get(str(path.relative_to(IACHAT)) if str(path).startswith(str(IACHAT)) else "", str(path))
    for i, a in enumerate(ACCOUNTS, 1):
        if origin.startswith(str(a) + "/"):
            return i
    return 0


def label_path(f: str) -> str:
    """A file under an account's folder, written with the account's number instead of the folder's name
    (which may carry a private word)."""
    for i, a in enumerate(ACCOUNTS, 1):
        if f.startswith(str(a) + "/"):
            return f"[account {i}]/" + f[len(str(a)) + 1:]
    return f


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
        for root in LIVE:
            for p in projects:
                for f in sorted((root / p).glob("*.jsonl")):
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
        # a resumed or forked session copies earlier events, sometimes with new uuids: the time and
        # the content identify an event as well
        key = (ev.get("timestamp", ""), ev.get("type", ""), json.dumps(ev.get("message", {}), sort_keys=True)[:400])
        if (uid and uid in seen_uuids) or (ev.get("timestamp") and key in seen_uuids):
            continue
        if uid:
            seen_uuids.add(uid)
        if ev.get("timestamp"):
            seen_uuids.add(key)
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
                    found = [(m.group(1), m.group(2)) for m in COMMIT_OUT.finditer(out) if m.group(1)]
                    if not found:  # a quiet commit: the newest line of the git log that follows is the commit
                        first = next((m for m in COMMIT_OUT.finditer(out) if m.group(3)), None)
                        found = [(first.group(3), first.group(4))] if first else []
                    for h, msg in found:
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
    ap.add_argument("--reversal-lines", type=int, default=3,
                    help="lines a later commit must remove, of those an earlier one added, to count as a reversal")
    ap.add_argument("--reversal-share", type=float, default=0.5,
                    help="share of the earlier commit's added lines in that file the later one must remove")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args(argv)
    srcs = sources(args.projects, args.live, args.transcripts)
    if not srcs:
        print("no transcripts found", file=sys.stderr)
        return 1
    priv = private_words()
    manifest = {}
    if (IACHAT / "manifest.jsonl").exists():
        for l in (IACHAT / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
            try:
                m = json.loads(l)
            except json.JSONDecodeError:
                continue
            if m.get("source") == "claude-code":
                manifest[m["path"]] = m.get("origin", "")
    seen: set = set()
    rows = []
    for path, sha in sorted(srcs, key=lambda s: s[0].name):
        events = read_events(path)
        sid = next((e.get("sessionId") for _, e in events if e.get("sessionId")), path.name.split(".")[0])
        for u in mine_session(events, seen, args):
            for c in u["commits"]:
                c["repo"], c["files"] = commit_files(c["hash"], args.repos)
            for a in u["actions"]:
                a["files"] = [label_path(f) for f in a["files"]]
            files = sorted({f for a in u["actions"] for f in a["files"] if f} | {f for c in u["commits"] for f in c["files"]})
            areas = sorted({area_of(f, args.language, args.method) for f in files}) or ["unknown"]
            words = len(u["text"].split())
            prop = u["proposal"]
            try:
                src = str(path.relative_to(IACHAT))
            except ValueError:
                src = label_path(str(path))
            project = next((p for p in args.projects if p in str(path)), "")
            row = {"id": f"{sid[:8]}:{u['line']}", "session": sid, "project": project,
                   # the repository whose CLAUDE.md and memory the session's agent read: its working folder
                   "session_repo": project.rsplit("-Projects-", 1)[-1] if "-Projects-" in project else project,
                   # each account has its own memory per project and its own global CLAUDE.md
                   "account": account_of(path, manifest),
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
    owned: set = set()
    for r in rows:  # a commit belongs to the first unit that made it
        r["commits"] = [c for c in r["commits"] if (c.get("repo"), c["hash"][:7]) not in owned]
        owned |= {(c.get("repo"), c["hash"][:7]) for c in r["commits"]}
    n_rev = link_reversals(rows, args.repos, args.reversal_lines, args.reversal_share)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "decision_units.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    by = Counter((r["project"].split("-")[-1], "+".join(r["areas"]), r["form"]) for r in rows)
    L = [f"# Decision units mined from the Claude Code transcripts, {args.date}", "",
         f"Written by `scripts/mine_decisions.py` ({VERSION}), no model. A unit is a turn of Luciano's followed by an action",
         "before his next turn. Sources: " + ("the live transcripts" if args.live else "the copies pinned in IA_chat") +
         f", {len(srcs)} sessions, each by sha256 in the jsonl. Short turns have at most {args.short_words} words; whether one",
         "confirms a model's proposal is a heuristic. Units with a private word keep only their metadata.", "",
         f"Units: {len(rows)}; with a commit {sum(bool(r['commits']) for r in rows)}; withheld {sum('withheld' in r for r in rows)};"
         f" reversals {n_rev} (a later commit removes at least {args.reversal_lines} lines and {args.reversal_share:.0%} of what an"
         " earlier one added to a file).", "",
         "| project | areas | form | units |", "|---|---|---|---|"]
    for (p, a, f), n in sorted(by.items()):
        L.append(f"| {p} | {a} | {f} | {n} |")
    L += ["", "## Units", ""]
    for r in rows:
        t = r["luciano"]["text"].replace("\n", " ")
        L.append(f"- {r['time'][:16]} `{r['id']}` {r['form']}, {'+'.join(r['areas'])}"
                 + (f", commit {', '.join(c['hash'][:7] for c in r['commits'])}" if r["commits"] else "")
                 + (f", reversed by {', '.join(x['unit'] for x in r['reversed_by'])}" if r.get("reversed_by") else "")
                 + f": {t[:160]}")
    (args.output_dir / "decision_units.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(rows)} units from {len(srcs)} sessions -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
