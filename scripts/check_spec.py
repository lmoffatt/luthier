#!/usr/bin/env python3
"""Check the chapters of the specification against the format of `docs/spec/00-index.md`.

For each chapter file given (or every `docs/spec/NN-*.md` except `00-index.md`): the first line
is `# N. Title` with N the chapter's number; sections are `## §k Title` numbered from 1 and the
last one is `## Open`; every item `**N.Rk. Title.**` (rule) or `**N.Sk. Title.**` (statement)
carries exactly one status (`[implemented]`, `[decided D-YYYY-MM-DD-x]`, `[decided Ln.k]`, `[proposed]`)
and R and S are numbered 1..n; a decided id exists in `record/decisions.md`, and a decided clause
`Ln.k` is a clause of `docs/principles.md` marked `[settled]` (D-2026-10-13-g); a rule ends with a `Files:` line
naming programs of `tests/spec/` (an implemented rule needs an accept and a reject one, a
statement has no Files line); citations resolve (`spec M §k`, `spec M.Rk`, `spec M.Sk`, `G/L/O`
entries of `docs/principles.md`, `D-` ids, `W` of `docs/way-of-working.md`, `P` of
`record/principles.md`; code spans are ignored); and no run of eight words repeats across two
chapters, between a chapter and `docs/principles.md`, or twice in a chapter (headings, tables,
code blocks and the chapter's header paragraph are left out).

Each finding is printed as `path:line: check-spec: message`; information (a cited chapter not
written yet) as `path:line: check-spec (information): message`. Exit status: 0 with no findings,
1 with findings, 2 when a file cannot be read. `--root` is the repository root (default: the one
this script lives in).

Specified in record/spec-brief-template.md and docs/spec/00-index.md.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIN_WORDS = 8

TITLE_RE = re.compile(r"^#\s+(\d+)\.\s+\S")
SECTION_RE = re.compile(r"^##\s+§(\d+)\s+\S")
ITEM_RE = re.compile(r"^\*\*(\d+)\.([RS])(\d+)\.\s*(.*?)\*\*\s*(.*)$")
STATUS_RE = re.compile(r"^\[([^\]]*)\]")
DECIDED_RE = re.compile(r"^decided (D-\d{4}-\d{2}-\d{2}-[a-z]+)$")
DECIDED_CLAUSE_RE = re.compile(r"^decided (L\d+\.\d+)$")
DECISION_LINE_RE = re.compile(r"^(D-\d{4}-\d{2}-\d{2}-[a-z]+)\s")
FILES_RE = re.compile(r"^Files:\s*(.*)$")
CHAPTER_NAME_RE = re.compile(r"^(\d\d)-.+\.md$")
CODE_SPAN_RE = re.compile(r"`[^`]*`")
CITE_SPEC_RE = re.compile(r"\bspec (\d+)(?:\s*§(\d+)|\.([RS])(\d+))?(?!\d)")
CITE_PRINCIPLE_RE = re.compile(r"(?<![\w.-])([GLO])(\d+)(?:\.(\d+))?(?!\w)")
CITE_DECISION_RE = re.compile(r"(?<![\w-])(D-\d{4}-\d{2}-\d{2}-[a-z]+)(?![\w-])")
CITE_W_RE = re.compile(r"(?<![\w.-])W(\d+)(?!\w)")
CITE_P_RE = re.compile(r"(?<![\w.-])P(\d+)(?!\w)")

Finding = tuple[int, str]  # (1-based line, message)


@dataclass
class Item:
    chapter: int
    kind: str  # "R" or "S"
    number: int
    line: int
    status: str  # text inside the brackets, "" when missing
    files: list[str] | None  # None when there is no Files line
    files_line: int = 0


@dataclass
class Chapter:
    path: Path
    number: int  # from the file name
    lines: list[str]
    title_number: int | None = None
    sections: dict[int, int] = field(default_factory=dict)  # k -> line
    headings: list[tuple[int, str]] = field(default_factory=list)  # `## ` lines
    items: list[Item] = field(default_factory=list)


@dataclass
class Block:
    line: int
    words: list[str]


@dataclass
class Refs:
    decisions: set[str]
    principles: list[str]
    way: list[str]
    method: list[str]
    tests_dir: Path
    chapters: dict[int, Chapter]


# ---------------------------------------------------------------- parsing

def paragraphs(lines: list[str]) -> list[tuple[int, list[str]]]:
    """Paragraphs (text between blank lines) as (1-based first line, lines)."""
    out: list[tuple[int, list[str]]] = []
    cur: list[str] = []
    start = 0
    for i, l in enumerate(lines):
        if l.strip():
            if not cur:
                start = i + 1
            cur.append(l)
        elif cur:
            out.append((start, cur))
            cur = []
    if cur:
        out.append((start, cur))
    return out


def parse_files(text: str) -> list[str]:
    names = [n.strip() for n in text.strip().rstrip(".").split(",")]
    return [n for n in names if n]


def parse_item(lines: list[str], start: int) -> Item | None:
    m = ITEM_RE.match(lines[0])
    if not m:
        return None
    sm = STATUS_RE.match(m.group(5))
    files = None
    files_line = 0
    for k, l in enumerate(lines):
        fm = FILES_RE.match(l)
        if fm:
            files = parse_files(fm.group(1))
            files_line = start + k
    return Item(int(m.group(1)), m.group(2), int(m.group(3)), start,
                sm.group(1).strip() if sm else "", files, files_line)


def parse_chapter(path: Path, number: int, text: str) -> Chapter:
    lines = text.splitlines()
    ch = Chapter(path, number, lines)
    if lines:
        tm = TITLE_RE.match(lines[0])
        ch.title_number = int(tm.group(1)) if tm else None
    fence = False
    for i, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            fence = not fence
        elif not fence and l.startswith("## "):
            ch.headings.append((i + 1, l))
            sm = SECTION_RE.match(l)
            if sm:
                ch.sections.setdefault(int(sm.group(1)), i + 1)
    for start, plines in paragraphs(lines):
        item = parse_item(plines, start)
        if item:
            ch.items.append(item)
    return ch


def load_chapters(spec_dir: Path) -> dict[int, Chapter]:
    out: dict[int, Chapter] = {}
    for p in sorted(spec_dir.glob("[0-9][0-9]-*.md")):
        m = CHAPTER_NAME_RE.match(p.name)
        if not m or m.group(1) == "00":
            continue
        try:
            out[int(m.group(1))] = parse_chapter(p, int(m.group(1)), p.read_text(encoding="utf-8"))
        except OSError:
            continue
    return out


# ---------------------------------------------------------------- format checks

def check_title(ch: Chapter) -> list[Finding]:
    if not ch.lines or ch.title_number is None:
        return [(1, "first line is not `# N. Title`")]
    if ch.title_number != ch.number:
        return [(1, f"title says chapter {ch.title_number}, file name says {ch.number}")]
    return []


def check_sections(ch: Chapter) -> list[Finding]:
    out: list[Finding] = []
    if not ch.headings or ch.headings[-1][1].strip() != "## Open":
        out.append((ch.headings[-1][0] if ch.headings else max(len(ch.lines), 1),
                    "the last section is not `## Open`"))
    expected = 1
    for line, text in ch.headings:
        if text.strip() == "## Open":
            continue
        m = SECTION_RE.match(text)
        if not m:
            out.append((line, f"section heading is not `## §k Title`: {text.strip()}"))
        elif int(m.group(1)) != expected:
            out.append((line, f"section §{m.group(1)} where §{expected} was expected"))
            expected = int(m.group(1)) + 1
        else:
            expected += 1
    return out


def label_of(item: Item) -> str:
    return f"{item.chapter}.{item.kind}{item.number}"


def clause_status(principles: list[str], clause: str) -> str | None:
    """The status in brackets at the end of clause `Ln.k` of the projected principles, "" when the
    clause has none, None when there is no such clause."""
    start = next((i for i, l in enumerate(principles) if l.startswith(f"- {clause} ")), None)
    if start is None:
        return None
    text = principles[start]
    for l in principles[start + 1:]:
        if not l.startswith("  ") or not l.strip():
            break
        text += " " + l.strip()
    m = re.search(r"\[([a-z ]+)\]\s*$", text)
    return m.group(1) if m else ""


def check_status(item: Item, decisions: set[str], principles: list[str] | None = None) -> list[Finding]:
    s = item.status
    if not s:
        return [(item.line, f"{label_of(item)} has no status (`[implemented]`, "
                            "`[decided D-...]` or `[proposed]`)")]
    if s in ("implemented", "proposed"):
        return []
    c = DECIDED_CLAUSE_RE.match(s)
    if c:
        status = clause_status(principles or [], c.group(1))
        if status is None:
            return [(item.line, f"{label_of(item)}: {c.group(1)} is not a clause of docs/principles.md")]
        if status != "settled":
            return [(item.line, f"{label_of(item)}: {c.group(1)} is not settled in docs/principles.md")]
        return []
    m = DECIDED_RE.match(s)
    if not m:
        return [(item.line, f"{label_of(item)} has an invalid status [{s}]")]
    if m.group(1) not in decisions:
        return [(item.line, f"{label_of(item)}: {m.group(1)} is not in record/decisions.md")]
    return []


def check_numbering(ch: Chapter) -> list[Finding]:
    out: list[Finding] = []
    for kind in "RS":
        for n, item in enumerate((i for i in ch.items if i.kind == kind), 1):
            if item.chapter != ch.number:
                out.append((item.line, f"item {label_of(item)} in chapter {ch.number}"))
            if item.number != n:
                out.append((item.line, f"{label_of(item)} where {item.chapter}.{kind}{n} was expected"))
    return out


def check_files(item: Item, tests_dir: Path) -> list[Finding]:
    label = label_of(item)
    if item.kind == "S":
        if item.files is not None:
            return [(item.files_line, f"{label} is a statement and has a Files line")]
        return []
    if item.files is None:
        if item.status == "implemented":
            return [(item.line, f"{label} is implemented and has no Files line")]
        return []
    out: list[Finding] = []
    for n in item.files:
        if not n.endswith((".accept.lut", ".reject.lut")):
            out.append((item.files_line, f"{label}: {n} is neither .accept.lut nor .reject.lut"))
        elif not ((tests_dir / n).is_file() or (tests_dir / "v0.1" / n).is_file()):
            # until the new checker exists, a program may still be one of v0.1's (D-2026-10-13-h)
            out.append((item.files_line, f"{label}: {n} not found in tests/spec/ or tests/spec/v0.1/"))
    if item.status == "implemented":
        for kind in ("accept", "reject"):
            if not any(n.endswith(f".{kind}.lut") for n in item.files):
                out.append((item.files_line, f"{label} is implemented and names no .{kind}.lut file"))
    return out


# ---------------------------------------------------------------- citations

def code_free_lines(lines: list[str]) -> list[tuple[int, str]]:
    """(1-based line, text without fenced blocks or code spans)."""
    out = []
    fence = False
    for i, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            fence = not fence
        elif not fence:
            out.append((i + 1, CODE_SPAN_RE.sub(" ", l)))
    return out


def has_line(lines: list[str], prefix: str) -> bool:
    return any(l.startswith(prefix) for l in lines)


def spec_citations(line: int, text: str,
                   chapters: dict[int, Chapter]) -> tuple[list[Finding], list[Finding]]:
    bad: list[Finding] = []
    info: list[Finding] = []
    for m in CITE_SPEC_RE.finditer(text):
        num = int(m.group(1))
        if num not in chapters:
            info.append((line, f"chapter {num} not written"))
        elif m.group(2) and int(m.group(2)) not in chapters[num].sections:
            bad.append((line, f"spec {num} §{m.group(2)}: chapter {num} has no section {m.group(2)}"))
        elif m.group(3) and not any(i.kind == m.group(3) and i.number == int(m.group(4))
                                    for i in chapters[num].items):
            bad.append((line, f"spec {num}.{m.group(3)}{m.group(4)}: chapter {num} has no such item"))
    return bad, info


def principle_citations(line: int, text: str, principles: list[str]) -> list[Finding]:
    out: list[Finding] = []
    for m in CITE_PRINCIPLE_RE.finditer(text):
        tag, n, clause = m.groups()
        if tag == "O":
            ok = clause is None and has_line(principles, f"- **O{n}**")
        elif clause is not None:
            ok = tag == "L" and has_line(principles, f"- {tag}{n}.{clause} ")
        else:
            ok = has_line(principles, f"**{tag}{n}.")
        if not ok:
            out.append((line, f"{m.group(0)} does not resolve in docs/principles.md"))
    return out


def other_citations(line: int, text: str, refs: Refs) -> list[Finding]:
    out: list[Finding] = []
    for m in CITE_DECISION_RE.finditer(text):
        if m.group(1) not in refs.decisions:
            out.append((line, f"{m.group(1)} is not in record/decisions.md"))
    for m in CITE_W_RE.finditer(text):
        if not has_line(refs.way, f"**W{m.group(1)}."):
            out.append((line, f"W{m.group(1)} does not resolve in docs/way-of-working.md"))
    for m in CITE_P_RE.finditer(text):
        if not has_line(refs.method, f"P{m.group(1)} "):
            out.append((line, f"P{m.group(1)} does not resolve in record/principles.md"))
    return out


def check_citations(ch: Chapter, refs: Refs) -> tuple[list[Finding], list[Finding]]:
    bad: list[Finding] = []
    info: list[Finding] = []
    for line, text in code_free_lines(ch.lines):
        b, i = spec_citations(line, text, refs.chapters)
        bad += b + principle_citations(line, text, refs.principles) + other_citations(line, text, refs)
        info += i
    return bad, info


# ---------------------------------------------------------------- duplicates

def normalize(word: str) -> str:
    return re.sub(r"[^\w']+", "", word.lower())


def blocks(lines: list[str], drop_header: bool) -> list[Block]:
    """Runs of prose: no headings, table rows, fenced code or blank lines inside; a bullet starts
    a new block. With drop_header, the paragraph before the first `## ` heading is left out."""
    out: list[Block] = []
    cur: list[str] = []
    start = 0
    fence = False

    def close() -> None:
        nonlocal cur
        words = [w for w in (normalize(x) for x in " ".join(cur).split()) if w]
        if words:
            out.append(Block(start, words))
        cur = []

    for i, l in enumerate(lines):
        if l.lstrip().startswith("```"):
            close()
            fence = not fence
        elif fence or l.lstrip().startswith(("#", "|")) or not l.strip():
            close()
        else:
            bullet = re.match(r"^\s*[-*]\s+", l)
            if bullet:
                close()
                l = l[bullet.end():]
            if not cur:
                start = i + 1
            cur.append(l.strip())
    close()
    if drop_header and out:
        first = next((i + 1 for i, l in enumerate(lines) if l.startswith("## ")), len(lines) + 1)
        if out[0].line < first:
            out = out[1:]
    return out


def run_index(bs: list[Block]) -> dict[tuple[str, ...], list[tuple[int, int]]]:
    idx: dict[tuple[str, ...], list[tuple[int, int]]] = {}
    for b, blk in enumerate(bs):
        for p in range(len(blk.words) - MIN_WORDS + 1):
            idx.setdefault(tuple(blk.words[p:p + MIN_WORDS]), []).append((b, p))
    return idx


def extend(wa: list[str], pa: int, wb: list[str], pb: int) -> list[str]:
    """The common run starting at wa[pa] and wb[pb], at least MIN_WORDS long."""
    k = MIN_WORDS
    while pa + k < len(wa) and pb + k < len(wb) and wa[pa + k] == wb[pb + k]:
        k += 1
    return wa[pa:pa + k]


def cross_duplicates(mine: list[Block], other: list[Block]) -> tuple[int, list[str]] | None:
    """The longest run shared by the two block lists, with the line in `mine` where it starts."""
    idx = run_index(mine)
    best: tuple[int, list[str]] | None = None
    for blk in other:
        for p in range(len(blk.words) - MIN_WORDS + 1):
            for (b, q) in idx.get(tuple(blk.words[p:p + MIN_WORDS]), []):
                run = extend(mine[b].words, q, blk.words, p)
                if best is None or len(run) > len(best[1]):
                    best = (mine[b].line, run)
    return best


def self_duplicates(bs: list[Block]) -> list[Finding]:
    best: dict[tuple[int, int], list[str]] = {}
    for occ in run_index(bs).values():
        for x in range(len(occ)):
            for y in range(x + 1, len(occ)):
                (a, pa), (b, pb) = occ[x], occ[y]
                if a == b and pb - pa < MIN_WORDS:
                    continue
                r = extend(bs[a].words, pa, bs[b].words, pb)
                if len(r) > len(best.get((a, b), [])):
                    best[(a, b)] = r
    return [(bs[b].line, f"repeats a run from line {bs[a].line}: \"{' '.join(r)}\"")
            for (a, b), r in best.items()]


def check_duplicates(ch: Chapter, others: dict[str, list[Block]]) -> list[Finding]:
    mine = blocks(ch.lines, drop_header=True)
    out = self_duplicates(mine)
    for name, bs in others.items():
        hit = cross_duplicates(mine, bs)
        if hit:
            out.append((hit[0], f"shares a run of {len(hit[1])} words with {name}: "
                                f"\"{' '.join(hit[1])}\""))
    return out


# ---------------------------------------------------------------- driver

def check_chapter(ch: Chapter, refs: Refs,
                  others: dict[str, list[Block]]) -> tuple[list[Finding], list[Finding]]:
    found = check_title(ch) + check_sections(ch) + check_numbering(ch)
    for item in ch.items:
        found += check_status(item, refs.decisions, refs.principles) + check_files(item, refs.tests_dir)
    bad, info = check_citations(ch, refs)
    found += bad + check_duplicates(ch, others)
    return sorted(set(found)), sorted(set(info))


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def load_refs(root: Path, chapters: dict[int, Chapter]) -> Refs:
    decisions = {m.group(1) for l in read_lines(root / "record" / "decisions.md")
                 if (m := DECISION_LINE_RE.match(l))}
    return Refs(decisions, read_lines(root / "docs" / "principles.md"),
                read_lines(root / "docs" / "way-of-working.md"),
                read_lines(root / "record" / "principles.md"),
                root / "tests" / "spec", chapters)


def display(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("chapters", nargs="*", type=Path,
                        help="chapter files (default: every docs/spec/NN-*.md but 00-index.md)")
    parser.add_argument("--root", type=Path, default=REPO_ROOT,
                        help="the repository root (default: %(default)s)")
    args = parser.parse_args(argv)
    root = args.root
    known = load_chapters(root / "docs" / "spec")
    paths = args.chapters or [c.path for c in known.values()]

    try:
        targets: list[Chapter] = []
        for p in paths:
            m = CHAPTER_NAME_RE.match(p.name)
            if not m or m.group(1) == "00":
                print(f"check-spec: {p} is not a chapter file NN-name.md", file=sys.stderr)
                return 2
            ch = parse_chapter(p, int(m.group(1)), p.read_text(encoding="utf-8"))
            known.setdefault(ch.number, ch)
            targets.append(ch)
        refs = load_refs(root, known)
    except OSError as e:
        print(f"check-spec: cannot read {e.filename}: {e.strerror}", file=sys.stderr)
        return 2

    principle_blocks = blocks(refs.principles, drop_header=False)
    chapter_blocks = {n: blocks(c.lines, drop_header=True) for n, c in known.items()}
    status = 0
    for ch in targets:
        others = {display(known[n].path, root): b for n, b in chapter_blocks.items() if n != ch.number}
        others["docs/principles.md"] = principle_blocks
        found, info = check_chapter(ch, refs, others)
        label = display(ch.path, root)
        for line, msg in found:
            print(f"{label}:{line}: check-spec: {msg}")
        for line, msg in info:
            print(f"{label}:{line}: check-spec (information): {msg}")
        status = 1 if found else status
    return status


if __name__ == "__main__":
    sys.exit(main())
