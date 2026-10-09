#!/usr/bin/env python3
"""The chronological list of ideas about Luthier: one row per idea, in time order, with who said
it, when, the quote and where it comes from.

Reads every ideas file of `record/ideas/` written by the four extractors (per voice note,
`extract_ideas_v1`; per day, `extract_ideas_day_v1`; per conversation, `extract_ideas_dialogue_v1`;
per written note, `extract_ideas_note_v1`; the list is --prompts), pinned by the sha256 of each file. No model: this is a merge, and a model
may run it. The three formats become one row: id, time, who (Luciano, model, pasted), kind, what,
quote, source (the note and its `[mm:ss]`, or the thread and its turn), the extraction it comes
from and the prompt that wrote it.

Time. A voice note's name carries its local time (`WhatsApp Ptt 2026-05-29 at 14.03.24`), to
which the quote's `[mm:ss]` is added; --note-tz says which zone that is. A chat turn carries UTC.
A written note's time is its creation date, as its file's metadata gave it, in the same zone.
Every row gets both the UTC instant and the local time, and the order is by instant.

Both extractions of a note are kept (Luciano, 2026-10-09: "ambas"): a row from the per-note
extraction says whether the same day was also extracted by day, and the reverse, so a reader
can tell a restatement from a duplicate.

Writes `record/ideas/timeline.jsonl` (one row per idea) and `record/ideas/timeline.md` (a header
with the inputs and counts, then the rows by day). Written for Luciano and for the tools that read
the timeline (the lineages, the distillation).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

VERSION = "ideas_timeline v1"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "record" / "ideas"
DEFAULT_PROMPTS = ("extract_ideas_v1", "extract_ideas_day_v1", "extract_ideas_dialogue_v1", "extract_ideas_note_v1")
DEFAULT_TZ = "America/Argentina/Buenos_Aires"

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
ENTRY_RE = re.compile(r"^### (.+?)\s*$", re.MULTILINE)
NOTE_TIME_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2}) at (\d{2})\.(\d{2})\.(\d{2})")
STAMP_RE = re.compile(r"\[(\d{1,2}):(\d{2})(?::(\d{2}))?(?:\s*[–-]\s*\d{1,2}:\d{2}(?::\d{2})?)?\]")
FIELD_RE = re.compile(r"^- \*\*(?P<name>[^*]+?)\*\*(?: \([^)]*\))?:\s*(?P<value>.*?)\s*$", re.MULTILINE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_front(text: str) -> dict:
    """The frontmatter's top-level `key: value` lines (nested lists are skipped)."""
    front: dict = {}
    m = FRONT_RE.match(text)
    if m:
        for ln in m.group(1).splitlines():
            if ln.startswith((" ", "-", "\t")):
                continue
            k, sep, v = ln.partition(":")
            if sep:
                front[k.strip()] = v.strip().strip('"')
    return front


def entries(text: str) -> list[tuple[str, dict]]:
    """(slug, fields) per `### ` block of the body; a field is a `- **Name**: value` line."""
    body = FRONT_RE.sub("", text, count=1)
    marks = list(ENTRY_RE.finditer(body))
    out = []
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        block = body[mk.end():end]
        fields = {f.group("name").strip(): f.group("value") for f in FIELD_RE.finditer(block)}
        out.append((mk.group(1).strip(), fields))
    return out


def note_local_time(name: str, tz: ZoneInfo) -> datetime | None:
    m = NOTE_TIME_RE.search(name)
    if not m:
        return None
    y, mo, d, h, mi, s = (int(x) for x in m.groups())
    return datetime(y, mo, d, h, mi, s, tzinfo=tz)


def stamp_seconds(text: str) -> tuple[int | None, str]:
    m = STAMP_RE.search(text)
    if not m:
        return None, ""
    a, b, c = m.group(1), m.group(2), m.group(3)
    secs = (int(a) * 3600 + int(b) * 60 + int(c)) if c else (int(a) * 60 + int(b))
    return secs, m.group(0)


def unquote(value: str) -> str:
    """The quoted text of a Cita or Quote field, without the trailing source parenthesis or stamp."""
    m = re.match(r'\s*"(.*)"', value, re.DOTALL)
    if m:
        return m.group(1)
    return value.strip().strip('"')


def rows_of_note_file(path: Path, text: str, front: dict, tz: ZoneInfo) -> list[dict]:
    audio = front.get("audio", "")
    base = note_local_time(audio, tz)
    rows = []
    for slug, f in entries(text):
        cita = f.get("Cita", "")
        secs, stamp = stamp_seconds(cita)
        t = base + timedelta(seconds=secs or 0) if base else None
        rows.append({"who": "Luciano", "kind": "idea", "slug": slug, "what": f.get("Qué", ""),
                     "quote": unquote(re.sub(r"`\[[^\]]*\]`\s*$", "", cita)),
                     "open": f.get("Ambigüedad / tensión", ""),
                     "source": f"{Path(audio).stem}.md {stamp}".strip(), "note": Path(audio).stem,
                     "time": t})
    return rows


def rows_of_day_file(path: Path, text: str, front: dict, tz: ZoneInfo) -> list[dict]:
    rows = []
    for slug, f in entries(text):
        q = f.get("Quote", "")
        src = re.search(r"\(`([^`]+)`\s*`(\[[^\]]+\])`\)\s*$", q)
        note = Path(src.group(1)).stem if src else ""
        secs, stamp = stamp_seconds(src.group(2) if src else "")
        base = note_local_time(note, tz) if note else None
        t = base + timedelta(seconds=secs or 0) if base else None
        rows.append({"who": "Luciano", "kind": "idea", "slug": slug, "what": f.get("What", ""),
                     "quote": unquote(re.sub(r"\s*\(`[^`]+`\s*`\[[^\]]+\]`\)\s*$", "", q)),
                     "open": f.get("Open", ""), "course": f.get("Course", ""),
                     "source": f"{note}.md {stamp}".strip() if note else "", "note": note, "time": t})
    return rows


def rows_of_dialogue_file(path: Path, text: str, front: dict, tz: ZoneInfo) -> list[dict]:
    rows = []
    for slug, f in entries(text):
        turn = f.get("Turn", "")
        m = re.match(r"(\d+),\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) UTC", turn)
        n = int(m.group(1)) if m else None
        t = datetime.strptime(m.group(2), "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) if m else None
        who = f.get("Who", "").strip().lower()
        rows.append({"who": {"luciano": "Luciano", "model": "model", "pasted": "pasted"}.get(who, who or "?"),
                     "kind": f.get("Kind", "idea"), "slug": slug, "what": f.get("What", ""),
                     "quote": unquote(f.get("Quote", "")), "open": f.get("Open", ""),
                     "also_in": f.get("Also in", ""),
                     "source": f"{front.get('thread', path.name)} turn {n}" if n else front.get("thread", ""),
                     "thread": front.get("key", ""), "turn": n, "time": t})
    return rows


def rows_of_written_file(path: Path, text: str, front: dict, tz: ZoneInfo) -> list[dict]:
    author = front.get("author", "Luciano")
    who = "Luciano" if author.lower().startswith("luciano") else "model"
    created = front.get("created", "")
    try:
        base = datetime.strptime(created[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=tz)
    except ValueError:
        base = None
    rows = []
    for slug, f in entries(text):
        q = f.get("Quote", "")
        ln = re.search(r"\(line (\d+)\)\s*$", q)
        rows.append({"who": who, "kind": "idea", "slug": slug, "what": f.get("What", ""),
                     "quote": unquote(re.sub(r"\s*\(line \d+\)\s*$", "", q)), "open": f.get("Open", ""),
                     "also_in": f.get("Also at", ""), "note": front.get("note", path.name),
                     "source": f"{front.get('note', path.name)} line {ln.group(1)}" if ln else front.get("note", path.name),
                     "time": base})
    return rows


PARSERS = {"extract_ideas_v1": ("note", rows_of_note_file),
           "extract_ideas_note_v1": ("written", rows_of_written_file),
           "extract_ideas_day_v1": ("day", rows_of_day_file),
           "extract_ideas_dialogue_v1": ("dialogue", rows_of_dialogue_file)}


def build(input_dir: Path, prompts: tuple[str, ...], tz: ZoneInfo) -> tuple[list[dict], list[dict], list[str]]:
    """(rows, inputs, problems)."""
    rows, inputs, problems = [], [], []
    for path in sorted(input_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        front = parse_front(text)
        prompt = front.get("generated_by") or front.get("generado_por") or ""
        if prompt not in prompts or prompt not in PARSERS:
            continue
        extractor, parser = PARSERS[prompt]
        sha = sha256(path)
        file_rows = parser(path, text, front, tz)
        inputs.append({"file": path.name, "sha256": sha, "prompt": prompt, "extractor": extractor,
                       "rows": len(file_rows), "quotes_found": front.get("quotes_found", ""),
                       "model": front.get("model") or front.get("modelo", ""), "effort": front.get("effort", "")})
        for i, r in enumerate(file_rows, 1):
            if r["time"] is None:
                problems.append(f"{path.name}: no time for '{r['slug']}'")
            if extractor == "note":
                stem = NOTE_TIME_RE.search(r.get("note", "") or path.name)
                key = f"{stem.group(1)}-{stem.group(2)}-{stem.group(3)}T{stem.group(4)}.{stem.group(5)}.{stem.group(6)}" if stem else path.name[:20]
            elif extractor == "day":
                key = front.get("date", path.name[:10])
            elif extractor == "written":
                # date and the note's own name: two copies of a note on one day are two sources
                key = path.name.split("_extract_ideas_note_v1")[0]
            else:
                ident = (front.get("key") or path.name).split(":")[-1]
                key = ident[:8] if "-" in ident else ident  # a uuid is cut to its first block; a date id stays whole
            r.update(extractor=extractor, extraction=path.name, extraction_sha256=sha, prompt=prompt,
                     id=f"{extractor}:{key}:{r['slug']}")
            rows.append(r)
    # the duplicates by construction: a note extracted both per note and by day
    day_dates = {r["time"].astimezone(tz).date().isoformat() for r in rows if r["extractor"] == "day" and r["time"]}
    note_dates = {r["time"].astimezone(tz).date().isoformat() for r in rows if r["extractor"] == "note" and r["time"]}
    for r in rows:
        if not r["time"]:
            continue
        d = r["time"].astimezone(tz).date().isoformat()
        if r["extractor"] == "note":
            r["also_by_day"] = d in day_dates
        elif r["extractor"] == "day":
            r["also_by_note"] = d in note_dates
    seen: dict[str, int] = {}
    for r in rows:  # an id repeated inside one extraction (a slug used twice) gets a suffix
        n = seen.get(r["id"], 0)
        seen[r["id"]] = n + 1
        if n:
            problems.append(f"{r['extraction']}: id {r['id']} repeated, suffixed -{n + 1}")
            r["id"] = f"{r['id']}-{n + 1}"
    rows.sort(key=lambda r: (r["time"] or datetime.max.replace(tzinfo=timezone.utc), r["extraction"], r["slug"]))
    for r in rows:
        if r["time"]:
            r["time_utc"] = r["time"].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            r["time_local"] = r["time"].astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        else:
            r["time_utc"] = r["time_local"] = ""
        del r["time"]
    return rows, inputs, problems


def write_outputs(rows: list[dict], inputs: list[dict], problems: list[str], out_dir: Path, tz_name: str,
                  today: str) -> tuple[Path, Path]:
    jsonl = out_dir / "timeline.jsonl"
    md = out_dir / "timeline.md"
    with jsonl.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    by_month_author = Counter((r["time_local"][:7] or "undated", r["who"]) for r in rows)
    months = sorted({m for m, _ in by_month_author})
    authors = sorted({a for _, a in by_month_author})
    by_extractor = Counter(r["extractor"] for r in rows)
    lines = ["# Timeline of ideas about Luthier", "",
             f"Written by `scripts/ideas_timeline.py` ({VERSION}) on {today}, for Luciano and for the tools that read it.",
             f"One row per idea as the extractors found it, in time order; the local times are in {tz_name}, a chat turn's",
             "time is its UTC converted. A note extracted both per note and by day gives two rows, each marked, so a",
             "restatement across notes is told from the same note read twice. Nothing here was judged or merged.", "",
             f"Rows: {len(rows)} ({', '.join(f'{k} {v}' for k, v in sorted(by_extractor.items()))}). "
             f"Inputs: {len(inputs)} files, listed at the end with their sha256.", ""]
    if problems:
        lines += ["Rows without a time (listed last): " + "; ".join(problems), ""]
    lines += ["| month | " + " | ".join(authors) + " | total |", "|---|" + "---|" * (len(authors) + 1)]
    for m in months:
        counts = [by_month_author.get((m, a), 0) for a in authors]
        lines.append(f"| {m} | " + " | ".join(str(c) for c in counts) + f" | {sum(counts)} |")
    lines += ["", "## Ideas, by day", ""]
    day = None
    for r in rows:
        d = r["time_local"][:10] or "undated"
        if d != day:
            day = d
            lines += [f"### {d}", ""]
        mark = {"note": "note", "day": "day", "dialogue": "chat", "written": "written"}[r["extractor"]]
        dup = " (also by day)" if r.get("also_by_day") else (" (also per note)" if r.get("also_by_note") else "")
        kind = f" {r['kind']}" if r.get("kind") and r["kind"] != "idea" else ""
        lines.append(f"- **{r['time_local'][11:16]}** {r['who']}{kind} [{mark}: {r['source']}]{dup} `{r['id']}`")
        lines.append(f"  {r['what']}")
        if r.get("quote"):
            lines.append(f"  > {r['quote']}")
        lines.append("")
    lines += ["## Inputs", "", "| file | prompt | model | effort | rows | quotes found | sha256 |", "|---|---|---|---|---|---|---|"]
    for i in inputs:
        lines.append(f"| {i['file']} | {i['prompt']} | {i['model']} | {i['effort']} | {i['rows']} | {i['quotes_found']} | {i['sha256'][:12]} |")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return jsonl, md


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory", type=Path, nargs="?", default=DEFAULT_INPUT, help="where the ideas files are")
    ap.add_argument("--output-dir", type=Path, default=None, help="default: the input directory")
    ap.add_argument("--prompts", nargs="*", default=list(DEFAULT_PROMPTS), help="the extraction prompts whose files are read")
    ap.add_argument("--note-tz", default=DEFAULT_TZ, help="the zone of the times in the voice notes' names")
    ap.add_argument("--date", default=datetime.now().date().isoformat())
    args = ap.parse_args(argv)
    if not args.directory.is_dir():
        print(f"ERROR: not a directory: {args.directory}", file=sys.stderr)
        return 2
    tz = ZoneInfo(args.note_tz)
    rows, inputs, problems = build(args.directory, tuple(args.prompts), tz)
    if not rows:
        print("no ideas found", file=sys.stderr)
        return 1
    out_dir = args.output_dir or args.directory
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonl, md = write_outputs(rows, inputs, problems, out_dir, args.note_tz, args.date)
    print(f"{len(rows)} ideas from {len(inputs)} files -> {jsonl.name}, {md.name}")
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
