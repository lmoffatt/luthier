#!/usr/bin/env python3
"""Check that every quote of the record is found, verbatim, at the line its source names.

The record is `docs/decisions.md` and `docs/principles.md`. An entry starts at column 0 with its
id (`P<n>` or `D-YYYY-MM-DD-<letters>`), then spaces and its statement, which may continue on
indented lines. Its fields follow, one per `Name:` at column 0, each continued on indented lines.
Blank lines separate entries; fence lines (``` or ~~~ indented by at most three spaces, as in
Markdown) are ignored. A line indented further, such as ``` inside a wrapped quote, is text.
Entries sit inside fenced blocks; outside them, a line that starts with an id and has no fields
after it is prose (such as "P10 and P11 are in force").

`Quote:` holds one or more quotes. Each starts with `"` at the start of a line and ends at the last
`"` before the next quote starts; text after that closing `"` (such as "(same line)") is not part
of the quote. A line starting with `"` starts the next quote only when the quote before it is
closed, that is, holds an even number of `"`: a wrapped quote may have a line that starts with a
quotation of its own. `Source:` holds one source per line, in the grammar

    <repo>@<commit>:<path>:<line>     or  <repo>@<commit>:<path>:<a>-<b>
    chat:<session8>:<line>            (or <a>-<b>)

where <repo> is a name given by --repo-root (luthier and sonolocalizacion by default) or the
absolute path of a git repository, and a chat source names a line of the Claude Code transcript
`<transcripts>/*/<session8>*.jsonl`. The text of a transcript line is every "text" string in
message.content (a string or a list of text blocks) and in attachment.prompt. A session found in
more than one project folder is read from its longest copy, when the others are its start.

Rules:
- an entry's fields are among Author, Quote, Source, Assumption, Kind, Principles and Status, each
  given once, and a decision has Author; inside a fence, every field line belongs to an entry;
- an entry with Quote has Source in the grammar, with as many sources as quotes or one for all,
  paired in order;
- a decision whose Author mentions Luciano has Quote; a principle has Quote, unless its Status
  says "source to pin" (then a warning);
- each quote is found in its source, with every run of whitespace taken as one space, both texts
  in Unicode's composed form (NFC, so that "é" typed as one character or as "e" and an accent
  is the same text), and nothing else changed: it neither starts nor ends inside a word of the
  source, and
  - in a file, it occurs in lines a .. a+30 (a .. b+30 for a range) joined by spaces, and its
    match starts within line a (lines a .. b for a range);
  - in a transcript, where a line is a whole message, it lies within line a (one of lines a .. b
    for a range), never across two messages;
- a repository that isn't on disk, or a transcript that isn't found, gives a warning and no
  failure, since each repository is self-contained.

Failures go to stdout as `<record>:<entry line>: quote: <message>`, warnings to stderr as
`<record>:<entry line>: warning: <message>`. Exit status: 1 with failures, else 0.

Step 4.1 of docs/plan-working-method-execution-2026-10-06.md.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOTS = {
    "luthier": REPO_ROOT,
    "sonolocalizacion": REPO_ROOT.parent / "sonolocalizacion",
}
DEFAULT_RECORDS = ("docs/decisions.md", "docs/principles.md")
DEFAULT_TRANSCRIPTS = Path.home() / ".claude" / "projects"
DEFAULT_CONTEXT = 30
SOURCE_TO_PIN = "source to pin"
FIELDS = ("Author", "Quote", "Source", "Assumption", "Kind", "Principles", "Status")

ID_RE = re.compile(r"^(P\d+|D-\d{4}-\d{2}-\d{2}-[a-z]+)(?:\s+(.*))?$")
FIELD_RE = re.compile(r"^([A-Z][A-Za-z]*):(?:\s+(.*))?$")
FENCE_RE = re.compile(r"^ {0,3}(```|~~~)")
COMMIT_RE = re.compile(r"@([0-9a-fA-F]{7,40}):")
PATH_LINES_RE = re.compile(r"^(.+):(\d+)(?:-(\d+))?$")
CHAT_RE = re.compile(r"^chat:([0-9A-Za-z-]+):(\d+)(?:-(\d+))?$")
GRAMMAR = "<repo>@<commit>:<path>:<line> or chat:<session8>:<line>, with <a>-<b> for a range"


# ---------------------------------------------------------------- the record

@dataclass
class Field:
    name: str
    line: int
    lines: list[str]  # the value, one string per line, stripped of its indentation


@dataclass
class Entry:
    id: str
    line: int
    in_fence: bool
    fields: dict[str, Field] = field(default_factory=dict)
    repeated: list[str] = field(default_factory=list)  # names of fields given twice

    def text(self, name: str) -> str | None:
        f = self.fields.get(name)
        return None if f is None else " ".join(" ".join(f.lines).split())


def read_record(text: str) -> tuple[list[Entry], list[tuple[int, str]]]:
    """The entries of a record, and the field lines inside a fence that belong to no entry."""
    entries: list[Entry] = []
    orphans: list[tuple[int, str]] = []
    entry: Entry | None = None
    current: Field | None = None
    in_fence = False
    # Lines end at "\n" only, as git and grep count them (str.splitlines also breaks at
    # characters such as U+2028 that may sit inside a pasted quote).
    for n, line in enumerate(text.split("\n"), 1):
        line = line.removesuffix("\r")
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not line.strip():
            entry, current = None, None
            continue
        m = ID_RE.match(line)
        if m:
            entry, current = Entry(m.group(1), n, in_fence), None
            entries.append(entry)
            continue
        if line[0].isspace():
            if current is not None:
                current.lines.append(line.strip())
            continue  # the statement's continuation, or indented prose
        m = FIELD_RE.match(line)
        if m and entry is not None:
            current = Field(m.group(1), n, [m.group(2).strip()] if m.group(2) else [])
            if current.name in entry.fields:
                entry.repeated.append(current.name)
            else:
                entry.fields[current.name] = current
            continue
        if m and in_fence and m.group(1) in FIELDS:
            orphans.append((n, m.group(1)))
        entry, current = None, None
    return entries, orphans


def read_quotes(lines: list[str]) -> tuple[list[str], list[str]]:
    """The quotes of a Quote: field, whitespace normalized, and what is wrong with it."""
    spans: list[list[str]] = []
    errors: list[str] = []
    for text in lines:
        # A quote holding quotations of its own has an even number of '"' once closed, so a
        # line starting with '"' while the quote before is open continues it.
        if text.startswith('"') and (not spans or "".join(spans[-1]).count('"') % 2 == 0):
            spans.append([text])
        elif spans:
            spans[-1].append(text)
        elif text:
            errors.append(f"text before the first quote: {shorten(text)}")
    quotes: list[str] = []
    for span in spans:
        joined = "\n".join(span)
        close = joined.rfind('"')
        if close == 0:
            errors.append(f"quote not closed: {shorten(joined)}")
            continue
        quote = normalize(joined[1:close])
        if not quote:
            errors.append("empty quote")
            continue
        quotes.append(quote)
    if not spans and not errors:
        errors.append("Quote: is empty")
    return quotes, errors


# ---------------------------------------------------------------- sources

@dataclass(frozen=True)
class Source:
    text: str
    first: int
    last: int
    repo_label: str = ""
    repo_path: Path | None = None
    commit: str = ""
    path: str = ""
    session: str = ""

    @property
    def is_chat(self) -> bool:
        return bool(self.session)


def parse_source(text: str, roots: dict[str, Path]) -> Source | str:
    """The source, or why it isn't in the grammar."""
    m = CHAT_RE.match(text)
    if m:
        first, last = int(m.group(2)), int(m.group(3) or m.group(2))
        if first < 1 or last < first:
            return f"bad line range in {text}"
        return Source(text, first, last, session=m.group(1))
    commits = list(COMMIT_RE.finditer(text))
    if not commits:
        return f"not in the grammar {GRAMMAR}: {text}"
    at = commits[-1]
    repo, rest = text[:at.start()], text[at.end():]
    m = PATH_LINES_RE.match(rest)
    if not repo or not m:
        return f"not in the grammar {GRAMMAR}: {text}"
    first, last = int(m.group(2)), int(m.group(3) or m.group(2))
    if first < 1 or last < first:
        return f"bad line range in {text}"
    if repo in roots:
        repo_path = roots[repo]
    elif repo.startswith("/"):
        repo_path = Path(repo)
    else:
        return (f"unknown repository {repo!r} in {text}: a name given by --repo-root "
                f"({', '.join(sorted(roots))}) or an absolute path")
    return Source(text, first, last, repo, repo_path, at.group(1), m.group(1))


class Fetched:
    """The lines of a source's file, or a warning, or a failure."""

    def __init__(self, lines: list[str] | None = None, warning: str = "", failure: str = ""):
        self.lines, self.warning, self.failure = lines, warning, failure


class Reader:
    """Reads the files sources point at, each once."""

    def __init__(self, transcripts: Path):
        self.transcripts = transcripts
        self.cache: dict[tuple, Fetched] = {}

    def fetch(self, src: Source) -> Fetched:
        key = ("chat", src.session) if src.is_chat else ("git", src.repo_path, src.commit, src.path)
        if key not in self.cache:
            self.cache[key] = self._chat(src) if src.is_chat else self._git(src)
        return self.cache[key]

    def _git(self, src: Source) -> Fetched:
        repo = src.repo_path
        assert repo is not None
        if not repo.is_dir():
            return Fetched(warning=f"repository {src.repo_label} not on disk at {repo}; "
                                   f"{src.text} not checked")
        if git(repo, "rev-parse", "--git-dir").returncode != 0:
            return Fetched(warning=f"{repo} is not a git repository; {src.text} not checked")
        if git(repo, "cat-file", "-e", f"{src.commit}^{{commit}}").returncode != 0:
            return Fetched(failure=f"commit {src.commit} not found in {repo} ({src.text})")
        shown = git(repo, "cat-file", "blob", f"{src.commit}:{src.path}")
        if shown.returncode != 0:
            return Fetched(failure=f"{src.path} is not a file at {src.commit} ({src.text})")
        lines = shown.stdout.decode("utf-8", errors="replace").split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        return Fetched(lines)

    def _chat(self, src: Source) -> Fetched:
        found = sorted(self.transcripts.glob(f"*/{src.session}*.jsonl"))
        if not found:
            return Fetched(warning=f"no transcript {src.session}*.jsonl under {self.transcripts}; "
                                   f"{src.text} not checked")
        if len({f.name for f in found}) > 1:
            return Fetched(failure=f"{len(found)} transcripts match {src.session} under "
                                   f"{self.transcripts}; write more characters of the session id")
        # One session in several project folders: the copies agree when each is the start of
        # the longest, and then the longest is read.
        data = sorted((f.read_bytes() for f in found), key=len)
        if any(not data[-1].startswith(d) for d in data[:-1]):
            return Fetched(failure=f"session {found[0].stem} is in {len(found)} project folders "
                                   f"under {self.transcripts}, and the copies differ")
        raw = data[-1].split(b"\n")
        if raw and raw[-1] == b"":
            raw.pop()
        return Fetched([transcript_text(line) for line in raw])


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True)


def transcript_text(raw: bytes) -> str:
    """Every "text" string of message.content and attachment.prompt in one line of a transcript."""
    try:
        obj = json.loads(raw)
    except ValueError:
        return ""
    if not isinstance(obj, dict):
        return ""
    texts: list[str] = []
    message, attachment = obj.get("message"), obj.get("attachment")
    if isinstance(message, dict):
        texts += block_texts(message.get("content"))
    if isinstance(attachment, dict):
        texts += block_texts(attachment.get("prompt"))
    return "\n".join(texts)


def block_texts(content: object) -> list[str]:
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        return [b["text"] for b in content
                if isinstance(b, dict) and b.get("type") == "text"
                and isinstance(b.get("text"), str)]
    return []


# ---------------------------------------------------------------- matching

def normalize(text: str) -> str:
    """Every run of whitespace as one space, in Unicode's composed form (NFC)."""
    return " ".join(unicodedata.normalize("NFC", text).split())


def shorten(text: str, width: int = 50) -> str:
    text = normalize(text)
    return f'"{text}"' if len(text) <= width else f'"{text[:width - 3]}..."'


def is_word(c: str) -> bool:
    # A combining mark (category M) belongs to the letter before it.
    return c.isalnum() or c == "_" or unicodedata.category(c).startswith("M")


def starts(quote: str, lines: list[str], first: int, last: int) -> list[int]:
    """The lines, among first..last, where the quote starts (lines numbered from 1)."""
    parts: list[str] = []
    offsets: list[int] = []  # where each nonblank line begins in the joined text
    numbers: list[int] = []
    pos = 0
    for n in range(first, min(last, len(lines)) + 1):
        t = normalize(lines[n - 1])
        if not t:
            continue
        if parts:
            pos += 1
        offsets.append(pos)
        numbers.append(n)
        parts.append(t)
        pos += len(t)
    text = " ".join(parts)
    found: list[int] = []
    i = text.find(quote)
    while i >= 0:
        end = i + len(quote)
        if not (is_word(quote[0]) and i > 0 and is_word(text[i - 1])) and \
           not (is_word(quote[-1]) and end < len(text) and is_word(text[end])):
            found.append(numbers[bisect.bisect_right(offsets, i) - 1])
        i = text.find(quote, i + 1)
    return found


def found_at(quote: str, lines: list[str], first: int, last: int, context: int,
             one_line: bool) -> list[int]:
    """The lines among first..last where the quote starts. With one_line (a transcript, whose
    line is a whole message) it must lie within that line; otherwise it may run on into the
    `context` lines after `last`."""
    if one_line:
        return [n for n in range(first, min(last, len(lines)) + 1) if starts(quote, lines, n, n)]
    return [n for n in starts(quote, lines, first, last + context) if n <= last]


def check_quote(quote: str, src: Source, lines: list[str], context: int) -> str:
    """Why the quote is not at its source, or "" when it is. When it isn't, the message says
    where in the file it does start, if anywhere."""
    if found_at(quote, lines, src.first, src.last, context, src.is_chat):
        return ""
    where = f"line {src.first}" if src.first == src.last else f"lines {src.first}-{src.last}"
    if src.first > len(lines):
        why = f": the file has {len(lines)} lines"
    elif not any(normalize(lines[n - 1]) for n in range(src.first, min(src.last, len(lines)) + 1)):
        why = f": {where} has no text"
    else:
        why = ""
    elsewhere = sorted(set(found_at(quote, lines, 1, len(lines), 0, src.is_chat)))
    if elsewhere:
        at = ", ".join(str(n) for n in elsewhere[:5]) + (", ..." if len(elsewhere) > 5 else "")
        return f"not at {src.text}{why}; it starts at line {at}"
    if src.is_chat:
        across = sorted(set(starts(quote, lines, 1, len(lines))))
        if across:
            return (f"not at {src.text}{why}; it runs across messages, from line {across[0]}, "
                    f"and a quote lies within one message")
    return f"not at {src.text}{why}, nor anywhere else in that file"


# ---------------------------------------------------------------- the rules

@dataclass
class Report:
    failures: list[tuple[int, str]] = field(default_factory=list)
    warnings: list[tuple[int, str]] = field(default_factory=list)

    def fail(self, line: int, message: str) -> None:
        if (line, message) not in self.failures:
            self.failures.append((line, message))

    def warn(self, line: int, message: str) -> None:
        if (line, message) not in self.warnings:
            self.warnings.append((line, message))


def check_entry(entry: Entry, report: Report, roots: dict[str, Path], reader: Reader,
                context: int) -> None:
    def fail(message: str) -> None:
        report.fail(entry.line, f"{entry.id}: {message}")

    # A misspelt or repeated field would hide a quote, or the Author that requires one.
    for name in entry.fields:
        if name not in FIELDS:
            fail(f"{name}: not a field of the record (the fields are {', '.join(FIELDS)})")
    for name in entry.repeated:
        fail(f"{name}: given twice")
    if entry.id.startswith("D") and "Author" not in entry.fields:
        fail("a decision has Author, which says whether it needs a Quote")

    quote_field = entry.fields.get("Quote")
    if quote_field is None:
        if entry.id.startswith("P"):
            if SOURCE_TO_PIN in (entry.text("Status") or "").lower():
                report.warn(entry.line, f"{entry.id}: no Quote; its Status says {SOURCE_TO_PIN}")
            else:
                fail(f'a principle has Quote, unless its Status says "{SOURCE_TO_PIN}"')
        elif "luciano" in (entry.text("Author") or "").lower():
            fail("a decision whose Author mentions Luciano has Quote")
        return

    quotes, errors = read_quotes(quote_field.lines)
    for error in errors:
        fail(f"Quote: {error}")
    source_field = entry.fields.get("Source")
    if source_field is None or not any(source_field.lines):
        fail("has Quote but no Source")
        return
    sources: list[Source | None] = []
    for text in (t for t in source_field.lines if t):
        parsed = parse_source(text, roots)
        if isinstance(parsed, str):
            fail(f"Source: {parsed}")
            sources.append(None)
        else:
            sources.append(parsed)
    if errors:
        return  # quotes and sources can't be paired when a quote couldn't be read
    if len(sources) not in (1, len(quotes)):
        fail(f"{len(quotes)} quotes and {len(sources)} sources: they pair in order, one source "
             f"per quote or one for all")
        return

    for k, quote in enumerate(quotes):
        src = sources[k] if len(sources) == len(quotes) else sources[0]
        if src is None:
            continue
        fetched = reader.fetch(src)
        if fetched.warning:
            report.warn(entry.line, f"{entry.id}: {fetched.warning}")
            continue
        if fetched.failure:
            fail(fetched.failure)
            continue
        assert fetched.lines is not None
        problem = check_quote(quote, src, fetched.lines, context)
        if problem:
            label = f"quote {k + 1} of {len(quotes)}" if len(quotes) > 1 else "quote"
            fail(f"{label} {shorten(quote)} {problem}")


def check_record(text: str, roots: dict[str, Path], reader: Reader, context: int) -> Report:
    report = Report()
    entries, orphans = read_record(text)
    for line, name in orphans:
        report.fail(line, f"{name}: belongs to no entry (a blank line inside an entry, or an id "
                          f"not of the form P<n> or D-YYYY-MM-DD-<letters>?)")
    for entry in entries:
        if not entry.in_fence and not entry.fields and not entry.repeated:
            continue  # prose that starts with an id, such as "P10 and P11 are in force"
        check_entry(entry, report, roots, reader, context)
    report.failures.sort(key=lambda f: f[0])
    return report


# ---------------------------------------------------------------- command line

def display(path: Path) -> str:
    """The path relative to the working directory when it lies under it, else as given."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def count(value: str) -> int:
    if not value.isdigit():
        raise argparse.ArgumentTypeError(f"expected a whole number of lines, got {value!r}")
    return int(value)


def repo_root(value: str) -> tuple[str, Path]:
    name, sep, path = value.partition("=")
    if not sep or not name or not path:
        raise argparse.ArgumentTypeError(f"expected NAME=PATH, got {value!r}")
    return name, Path(path).expanduser()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("records", nargs="*", type=Path,
                        help="record files (default: docs/decisions.md and docs/principles.md "
                             "of --repo)")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT,
                        help="the repository whose record is checked by default "
                             "(default: %(default)s)")
    parser.add_argument("--repo-root", type=repo_root, action="append", default=[],
                        metavar="NAME=PATH",
                        help="where the repository named NAME in a source lives; repeatable "
                             "(defaults: " + ", ".join(f"{k}={v}" for k, v in DEFAULT_ROOTS.items())
                             + ")")
    parser.add_argument("--transcripts", type=Path, default=DEFAULT_TRANSCRIPTS,
                        help="the folder of Claude Code transcripts, one subfolder per project "
                             "(default: %(default)s)")
    parser.add_argument("--context", type=count, default=DEFAULT_CONTEXT,
                        help="lines of a file after the cited ones that a quote may run into; "
                             "in a transcript a quote stays within its line "
                             "(default: %(default)s)")
    args = parser.parse_args(argv)

    roots = dict(DEFAULT_ROOTS)
    roots.update(dict(args.repo_root))
    reader = Reader(args.transcripts.expanduser())

    if args.records:
        records, required = args.records, True
    else:
        records, required = [args.repo / r for r in DEFAULT_RECORDS], False

    failed = False
    for record in records:
        label = display(record)
        try:
            text = record.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            print(f"{label}:0: quote: the record is not UTF-8 ({e.reason} at byte {e.start})")
            failed = True
            continue
        except OSError as e:
            if required:
                print(f"{label}:0: quote: cannot read the record: {e.strerror}")
                failed = True
            else:
                print(f"{label}:0: warning: no record here", file=sys.stderr)
            continue
        report = check_record(text, roots, reader, args.context)
        for line, message in report.warnings:
            print(f"{label}:{line}: warning: {message}", file=sys.stderr)
        for line, message in report.failures:
            print(f"{label}:{line}: quote: {message}")
        failed = failed or bool(report.failures)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
