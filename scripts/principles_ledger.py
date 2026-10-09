#!/usr/bin/env python3
"""The ledger of the principles: which decisions each one guided, which pairs collided, which guide
nothing, and how each one's text changed. Mechanical, no model; a lint any session may run.

Reads `record/principles.md` (entries `P<n> statement`, with Quote, Source, Assumption, Status)
and `record/decisions.md` (entries `D-<date>-<letter> statement`, whose `Kind:` line names the
principles the decision is `For` and the ones it goes `against`), and the list of principles in
force in `CLAUDE.md`. With --history, every commit that touched the principles file is read with
`git show` and the changes to each principle's statement, assumption and status are listed.

Prints the ledger; --write saves it as Markdown (for example under record/audits/). Exit 1 when a
decision has no `Kind:` line or a principle is named that the file does not define.

What it measures is P13 in its countable form: a principle is worth the decisions it guides. It
says nothing about whether a decision was right.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

VERSION = "principles_ledger v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PRINCIPLES = REPO_ROOT / "record" / "principles.md"
DEFAULT_DECISIONS = REPO_ROOT / "record" / "decisions.md"
DEFAULT_CLAUDE_MD = REPO_ROOT / "CLAUDE.md"

P_HEAD_RE = re.compile(r"^(P\d+)\s+(.*)$")
D_HEAD_RE = re.compile(r"^(D-\d{4}-\d{2}-\d{2}-[a-z]+)\s+(.*)$")
FIELD_RE = re.compile(r"^(Quote|Source|Assumption|Status|Author|Kind|Replaces|Reverses):\s*(.*)$")
P_REF_RE = re.compile(r"\bP\d+\b")
CLAUDE_P_RE = re.compile(r"^- (P\d+)\s+(.*)$", re.MULTILINE)


def parse_entries(text: str, head_re: re.Pattern) -> dict[str, dict]:
    """Entries of a record file: id -> {statement, fields...}. A statement may wrap onto indented
    lines; a field runs until the next field or the next entry."""
    entries: dict[str, dict] = {}
    cur: dict | None = None
    field: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        hm = head_re.match(line)
        if hm:
            cur = {"id": hm.group(1), "statement": hm.group(2).strip()}
            entries[cur["id"]] = cur
            field = "statement"
            continue
        if cur is None:
            continue
        fm = FIELD_RE.match(line)
        if fm:
            field = fm.group(1)
            cur[field] = fm.group(2).strip()
        elif line.startswith((" ", "\t")) and field:
            cur[field] = (cur.get(field, "") + " " + line.strip()).strip()
        elif not line.strip():
            continue
        else:
            cur, field = None, None  # prose outside entries
    return entries


def refs(text: str) -> list[str]:
    return sorted(set(P_REF_RE.findall(text)), key=lambda p: int(p[1:]))


def split_kind(kind: str) -> tuple[list[str], list[str]]:
    """The principles a decision is For and the ones it goes against, from its Kind line.
    `against` starts the against part; `For` (or a bare list of P's) the for part."""
    low = kind
    i = re.search(r"\bagainst\b", low)
    if i:
        for_part, against_part = low[:i.start()], low[i.end():]
    else:
        for_part, against_part = low, ""
    # the against part ends at a sentence end or a semicolon followed by text that names no P
    m = re.match(r"[^;.]*", against_part)
    against_part = m.group(0) if m else against_part
    return refs(for_part), refs(against_part)


def status_word(status: str) -> str:
    s = status.lower()
    for w in ("reversed", "proposed", "dropped", "superseded", "current"):
        if w in s:
            return w
    return s.split(";")[0].split(".")[0].strip()[:30] or "?"


def claude_list(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in CLAUDE_P_RE.finditer(text)}


def norm(s: str) -> str:
    return " ".join(s.lower().replace("(", "").replace(")", "").split())


def history(path: Path) -> list[dict]:
    """For each commit that touched the file, the principles whose statement, assumption or status
    changed against the previous commit."""
    try:
        log = subprocess.run(["git", "-C", str(path.parent), "log", "--format=%h%x09%ad%x09%s", "--date=short",
                              "--follow", "--", path.name], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return []
    commits = [ln.split("\t", 2) for ln in log.splitlines() if ln.strip()]
    commits.reverse()
    out, prev = [], {}
    rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
    for h, d, subject in commits:
        names = subprocess.run(["git", "-C", str(path.parent), "show", "--name-only", "--format=", h],
                               capture_output=True, text=True).stdout.split()
        shown = ""
        for n in names:
            if Path(n).name == path.name:
                r = subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"{h}:{n}"], capture_output=True, text=True)
                if r.returncode == 0:
                    shown = r.stdout
                    break
        cur = parse_entries(shown, P_HEAD_RE) if shown else {}
        changes = []
        for pid in sorted(set(cur) | set(prev), key=lambda p: int(p[1:])):
            a, b = prev.get(pid), cur.get(pid)
            if a is None:
                changes.append((pid, "added", b.get("statement", "")[:90]))
            elif b is None:
                changes.append((pid, "removed", ""))
            else:
                for f in ("statement", "Assumption", "Status"):
                    if norm(a.get(f, "")) != norm(b.get(f, "")):
                        changes.append((pid, f"{f.lower()} changed", b.get(f, "")[:90]))
        if changes:
            out.append({"commit": h, "date": d, "subject": subject[:80], "changes": changes})
        prev = cur
    return out


def ledger(principles: dict[str, dict], decisions: dict[str, dict], in_force: dict[str, str],
           hist: list[dict] | None, today: str) -> tuple[str, list[str]]:
    problems: list[str] = []
    guided = defaultdict(list)
    opposed = defaultdict(list)
    pairs = Counter()
    pair_decisions = defaultdict(list)
    no_principle = []
    reversed_for = []
    for did, d in decisions.items():
        kind = d.get("Kind")
        if kind is None:
            problems.append(f"{did}: no Kind line")
            continue
        fors, againsts = split_kind(kind)
        for p in fors + againsts:
            if p not in principles:
                problems.append(f"{did}: names {p}, which principles.md does not define")
        for p in fors:
            guided[p].append(did)
        for p in againsts:
            opposed[p].append(did)
        for a in fors:
            for b in againsts:
                pairs[(a, b)] += 1
                pair_decisions[(a, b)].append(did)
        if kind.lower().startswith("principle") and not fors and not againsts:
            no_principle.append(did)
        if status_word(d.get("Status", "")) == "reversed" and fors:
            reversed_for.append((did, fors))

    L = [f"# Ledger of the principles, {today}", "",
         f"Written by `scripts/principles_ledger.py` ({VERSION}) from `record/principles.md` ({len(principles)} entries)",
         f"and `record/decisions.md` ({len(decisions)} entries). Counts only; it says nothing about whether a decision was right.", "",
         "## Per principle", "",
         "| principle | status | guided (For) | against | decisions For | decisions against |", "|---|---|---|---|---|---|"]
    idle = []
    for pid, p in sorted(principles.items(), key=lambda kv: int(kv[0][1:])):
        f, a = guided.get(pid, []), opposed.get(pid, [])
        if not f and not a:
            idle.append(pid)
        L.append(f"| {pid} {p['statement'][:60]} | {status_word(p.get('Status', ''))} | {len(f)} | {len(a)} | "
                 f"{', '.join(x.replace('D-2026-', '') for x in f)} | {', '.join(x.replace('D-2026-', '') for x in a)} |")
    L += ["", f"**Guiding nothing yet (P13's measure):** {', '.join(idle) if idle else 'none'}.", ""]
    L += ["## Pairs on opposite sides of one decision", ""]
    if pairs:
        L += ["| for | against | times | decisions |", "|---|---|---|---|"]
        for (a, b), n in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0])):
            L.append(f"| {a} | {b} | {n} | {', '.join(x.replace('D-2026-', '') for x in pair_decisions[(a, b)])} |")
    else:
        L.append("none")
    L += ["", "## Decisions of kind principle that name none", "",
          ", ".join(no_principle) if no_principle else "none", "",
          "## Reversed decisions and the principles they were For (evidence against an assumption)", "",
          "\n".join(f"- {did}: {', '.join(f)}" for did, f in reversed_for) if reversed_for else "none", "",
          "## CLAUDE.md against principles.md", ""]
    only_claude = sorted(set(in_force) - set(principles), key=lambda p: int(p[1:]))
    only_file = sorted(set(principles) - set(in_force), key=lambda p: int(p[1:]))
    differ = [p for p in in_force if p in principles and norm(in_force[p]) != norm(principles[p]["statement"])]
    L += [f"- In CLAUDE.md and not in principles.md: {', '.join(only_claude) or 'none'}",
          f"- In principles.md and not in CLAUDE.md: {', '.join(f'{p} ({status_word(principles[p].get('Status', ''))})' for p in only_file) or 'none'}",
          f"- Statement differs: {', '.join(differ) or 'none'}", ""]
    if hist is not None:
        L += ["## History of the principles file", ""]
        if not hist:
            L.append("no commits found")
        for h in hist:
            L.append(f"- {h['date']} `{h['commit']}` {h['subject']}")
            for pid, what, txt in h["changes"]:
                L.append(f"  - {pid} {what}" + (f": {txt}" if txt else ""))
        L.append("")
    if problems:
        L += ["## Problems", ""] + [f"- {p}" for p in problems] + [""]
    return "\n".join(L), problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--principles", type=Path, default=DEFAULT_PRINCIPLES)
    ap.add_argument("--decisions", type=Path, default=DEFAULT_DECISIONS)
    ap.add_argument("--claude-md", type=Path, default=DEFAULT_CLAUDE_MD)
    ap.add_argument("--history", action="store_true", help="add the changes per principle from the git history")
    ap.add_argument("--write", type=Path, default=None, help="save the ledger as Markdown here")
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args(argv)
    for p in (args.principles, args.decisions):
        if not p.is_file():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            return 2
    principles = parse_entries(args.principles.read_text(encoding="utf-8"), P_HEAD_RE)
    decisions = parse_entries(args.decisions.read_text(encoding="utf-8"), D_HEAD_RE)
    in_force = claude_list(args.claude_md.read_text(encoding="utf-8")) if args.claude_md.is_file() else {}
    hist = history(args.principles) if args.history else None
    text, problems = ledger(principles, decisions, in_force, hist, args.date)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.write}")
    else:
        print(text)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
