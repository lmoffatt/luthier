#!/usr/bin/env python3
"""Export the conversation of one Claude Code transcript to Markdown.

Input: a transcript `.jsonl` (one JSON object per line), as Claude Code writes
it under `~/.claude/projects/<project>/<session id>.jsonl`.

Output: `record/chat/<date>_<session8>.md` at the root of this repository, or the
path given with --out. `<date>` is the UTC date (YYYY-MM-DD) of the first
exported turn and `<session8>` the first 8 characters of the session id.

What the export holds, in order:

- frontmatter: session id, sha256 of the transcript, number of turns, version
  of this script;
- the turns that contain an entry of `export_chat.private` (next to this
  script, one word or phrase per line, matched without regard to case), or
  "none";
- the turns, each under a heading with its author (Luciano or Model), its
  timestamp (UTC) and the transcript line(s) it comes from.

Kept: Luciano's typed text, including the messages he sent while the model was
working (attachments of type `queued_command`), and the visible text of the
model's replies. Consecutive text blocks of the model, with nothing of Luciano
between them, form one turn. Text Luciano pasted (`<pasted_content>`) is kept
verbatim in a fenced block marked as pasted, since it may not be his. Other
text that opens a code fence and never closes it (a terminal banner of "~~~",
say) is put, unchanged, in a fence of its own, so the turns after it still
render as text.

Dropped: tool calls and their results, thinking blocks, subagent (sidechain)
lines, `isMeta` lines, the text the harness inserts (system reminders, IDE
notices, slash-command wrappers, output of local commands, skill bodies, task
notifications), and compact summaries, which become one line.

The transcript format is internal to Claude Code and changes between versions.
Every record type and content shape seen in the transcripts on 2026-10-06 is
handled below, kept or dropped on purpose. Anything else stops the script with
"line N: ..." on stderr and exit code 2, so a new shape is looked at before it
is exported or lost.

The same transcript always gives the same bytes: nothing depends on the clock,
the locale or the machine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path


SCRIPT_VERSION = "1"

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT_DIR = REPO_ROOT / "record" / "chat"
PRIVATE_WORDS_FILE = Path(__file__).resolve().parent / "export_chat.private"

SUMMARY_LINE = "[summary inserted by the harness]"
PASTED_LABEL = "[pasted text]"


class TranscriptError(Exception):
    """A line of the transcript this script does not understand."""

    def __init__(self, line: int, message: str):
        super().__init__(f"line {line}: {message}")


# --- Record types --------------------------------------------------------

# Top-level record types that carry no conversation text. Each is dropped on
# purpose.
DROPPED_RECORD_TYPES = {
    # Queue bookkeeping. A message that is delivered reaches the transcript as
    # a user line or a queued_command attachment; one that is removed from the
    # queue before delivery was never part of the conversation.
    "queue-operation",
    # Session metadata: titles, the last prompt (a copy of a user line), the
    # agent's name, the permission mode, model switches.
    "last-prompt",
    "ai-title",
    "custom-title",
    "agent-name",
    "mode",
    "permission-mode",
    "atis-latch",
    # File backups taken before edits.
    "file-history-snapshot",
    "file-history-delta",
    # Cost and remote-session bookkeeping, links to PRs and artifacts.
    "cost-state",
    "bridge-session",
    "pr-link",
    "frame-link",
}

# Subtypes of "system" records. All are written by the harness.
DROPPED_SYSTEM_SUBTYPES = {
    "api_error",  # a failed API call and its retry
    "compact_boundary",  # marks a compaction; the summary is a user line
    "model_refusal_fallback",  # notice of a switch to another model
    "local_command",  # output of a local slash command
    "stop_hook_summary",  # which hooks ran when the model stopped
}

# Attachment types other than queued_command. All are context the harness
# gives the model (reminders, listings, environment, file snapshots, hook
# output, mode changes), never something Luciano typed.
DROPPED_ATTACHMENT_TYPES = {
    "agent_listing_delta",
    "auto_mode",
    "auto_mode_exit",
    "batching_reminder_sent",
    "command_permissions",
    "compact_file_reference",
    "credential_org",
    "date",
    "date_change",
    "deferred_tools_delta",
    "deferred_tools_record",
    "edited_text_file",
    "environment",
    "file",
    "hook_additional_context",
    "instructions",
    "mcp_instructions_delta",
    "model",
    "plan_mode",
    "plan_mode_exit",
    "prompt_snapshot",
    "read_truncation_notice",
    "remote_session_change",
    "secondary_reminder_sent",
    "session_context",
    "silent_turn_reminder",
    "skill_listing",
    "task_reminder",
    "task_status",
    "thinking_drop",
    "thinking_stripped",
    "todo_reminder",
    "total_tokens_reminder",
    "ultra_effort_enter",
    "ultra_effort_exit",
    "workflow_keyword_request",
}

# Values of "origin.kind" on user lines and queued commands. A missing origin
# (older versions) is a human message too.
HUMAN_ORIGINS = {None, "human"}
DROPPED_ORIGINS = {
    "task-notification",  # a background task finished; written by the harness
    "peer",  # a subagent's report handed back; model output
}

# Blocks of an assistant message.
ASSISTANT_TEXT_BLOCK = "text"
DROPPED_ASSISTANT_BLOCKS = {
    "thinking",
    "redacted_thinking",
    "tool_use",
    "fallback",  # harness marker of a switch to another model
}

# Blocks of a user message.
USER_TEXT_BLOCK = "text"
USER_ATTACHED_BLOCKS = {"image", "document"}  # exported as a placeholder
TOOL_RESULT_BLOCK = "tool_result"

# Tags the harness wraps around text it inserts into user lines. A complete
# pair <tag ...>...</tag> is removed together with what it encloses, but only
# when it fills whole lines (indentation and trailing spaces aside), which is
# how the harness writes it. A pair inside a line of prose is left alone, and
# the check below then stops on it, so words of Luciano's that mention a tag
# are never removed in silence.
HARNESS_TAGS = (
    "system-reminder",
    "ide_opened_file",
    "ide_selection",
    "ide_diagnostics",
    "command-message",
    "command-name",
    "command-args",
    "skill-format",
    "local-command-caveat",
    "local-command-stdout",
    "local-command-stderr",
    "task-notification",
    "agent-message",
)
HARNESS_PAIR_RE = re.compile(
    r"^[ \t]*<(" + "|".join(re.escape(t) for t in HARNESS_TAGS) + r")\b[^>]*>.*?</\1>[ \t]*$",
    re.DOTALL | re.MULTILINE,
)

# Text the harness writes as a user line of its own when Luciano interrupts the
# model. Dropped: it is not his text.
INTERRUPTION_MARKERS = {
    "[Request interrupted by user]",
    "[Request interrupted by user for tool use]",
}

# Text Luciano pasted: <pasted_content id="x"> ... </pasted_content id="x">.
PASTED_RE = re.compile(
    r'<pasted_content(?: id="([^"]*)")?>\n?(.*?)\n?</pasted_content(?: id="([^"]*)")?>',
    re.DOTALL,
)
PASTED_TAG_RE = re.compile(r"</?pasted_content\b")

# Typed text that, once the known pairs are removed, still holds a tag that it
# also closes, anywhere in it, looks like harness text of a kind not seen
# before (or a known tag in a place not seen before): stop and look at it. None
# of the transcripts of 2026-10-06 has such a pair in Luciano's text.
LEFTOVER_PAIR_RE = re.compile(r"<([a-z][a-z0-9_-]*)(?:\s[^<>]*)?>.*?</\1>", re.DOTALL)

TIMESTAMP_RE = re.compile(r"\A(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})(?:\.\d+)?Z\Z")


# --- Turns ---------------------------------------------------------------

@dataclass
class Segment:
    """A piece of a turn's text: typed (or written by the model), or pasted."""

    text: str
    pasted: bool = False


@dataclass
class Turn:
    author: str  # "Luciano" or "Model"
    timestamp: str  # as in the transcript
    lines: list[int]
    segments: list[Segment]
    queued: bool = False  # sent while the model was working


@dataclass
class Marker:
    """A line that stands for something dropped, such as a compact summary."""

    line: int
    text: str


@dataclass
class Export:
    session_id: str | None = None
    entries: list = field(default_factory=list)  # Turn or Marker, in order


# --- Reading the transcript ----------------------------------------------

def origin_kind(record: dict, line: int) -> str | None:
    origin = record.get("origin")
    if origin is None:
        return None
    if not isinstance(origin, dict):
        raise TranscriptError(line, f"origin is not an object: {origin!r}")
    return origin.get("kind")


def check_timestamp(record: dict, line: int) -> str:
    ts = record.get("timestamp")
    if not isinstance(ts, str) or not TIMESTAMP_RE.match(ts):
        raise TranscriptError(line, f"missing or unreadable timestamp: {ts!r}")
    return ts


def split_pasted(text: str, line: int) -> list[Segment]:
    """Split a text into typed and pasted segments."""
    segments: list[Segment] = []
    pos = 0
    for m in PASTED_RE.finditer(text):
        if m.group(1) != m.group(3):
            raise TranscriptError(line, "pasted_content tags with different ids")
        before = text[pos:m.start()]
        if PASTED_TAG_RE.search(before):
            raise TranscriptError(line, "unbalanced pasted_content tag")
        segments.append(Segment(before))
        segments.append(Segment(m.group(2), pasted=True))
        pos = m.end()
    rest = text[pos:]
    if PASTED_TAG_RE.search(rest):
        raise TranscriptError(line, "unbalanced pasted_content tag")
    segments.append(Segment(rest))
    return segments


def clean_typed(text: str, line: int) -> str:
    """Remove the harness's tagged insertions from text Luciano typed."""
    text = HARNESS_PAIR_RE.sub("", text)
    m = LEFTOVER_PAIR_RE.search(text)
    if m:
        raise TranscriptError(line, f"tag <{m.group(1)}> in user text, of a kind or in a place not seen before")
    return text


def luciano_segments(blocks: list, line: int) -> list[Segment]:
    """The exported segments of a user message or a queued command.

    `blocks` is a list of content blocks (text, image, document). Returns an
    empty list when nothing of Luciano's is left.
    """
    segments: list[Segment] = []
    for block in blocks:
        if not isinstance(block, dict):
            raise TranscriptError(line, f"content block is not an object: {block!r}")
        kind = block.get("type")
        if kind == USER_TEXT_BLOCK:
            text = block.get("text")
            if not isinstance(text, str):
                raise TranscriptError(line, "text block without text")
            if text.strip() in INTERRUPTION_MARKERS:
                continue
            if text.lstrip().startswith("<task-notification>"):
                # Older versions mark task notifications only by this tag.
                continue
            for seg in split_pasted(text, line):
                if not seg.pasted:
                    seg = Segment(clean_typed(seg.text, line))
                if seg.text.strip():
                    segments.append(seg)
        elif kind in USER_ATTACHED_BLOCKS:
            segments.append(Segment(f"[{kind} not exported]"))
        else:
            raise TranscriptError(line, f"unknown block type {kind!r} in a message of Luciano's")
    return segments


def as_blocks(content, line: int) -> list:
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if isinstance(content, list):
        return content
    raise TranscriptError(line, f"content is neither text nor a list: {type(content).__name__}")


def read_user(record: dict, line: int, export: Export) -> None:
    if record.get("isMeta"):
        # Skill bodies, caveats, image notes, "Continue from where you left
        # off.", messages from other sessions: all inserted by the harness.
        return
    message = record.get("message")
    if not isinstance(message, dict) or message.get("role") != "user":
        raise TranscriptError(line, "user record without a user message")
    if record.get("isCompactSummary"):
        export.entries.append(Marker(line, SUMMARY_LINE))
        return
    blocks = as_blocks(message.get("content"), line)
    kinds = {b.get("type") if isinstance(b, dict) else None for b in blocks}
    if TOOL_RESULT_BLOCK in kinds:
        if kinds != {TOOL_RESULT_BLOCK}:
            raise TranscriptError(line, f"tool result mixed with other blocks: {sorted(map(str, kinds))}")
        return
    kind = origin_kind(record, line)
    if kind in DROPPED_ORIGINS:
        return
    if kind not in HUMAN_ORIGINS:
        raise TranscriptError(line, f"unknown origin {kind!r} of a user line")
    segments = luciano_segments(blocks, line)
    if segments:
        ts = check_timestamp(record, line)
        export.entries.append(Turn("Luciano", ts, [line], segments))


def read_assistant(record: dict, line: int, export: Export) -> None:
    message = record.get("message")
    if not isinstance(message, dict) or message.get("role") != "assistant":
        raise TranscriptError(line, "assistant record without an assistant message")
    if record.get("isApiErrorMessage") or message.get("model") == "<synthetic>":
        # Error notices and "No response requested.", written by the harness.
        return
    content = message.get("content")
    if not isinstance(content, list):
        raise TranscriptError(line, f"assistant content is not a list: {type(content).__name__}")
    texts = []
    for block in content:
        if not isinstance(block, dict):
            raise TranscriptError(line, f"content block is not an object: {block!r}")
        kind = block.get("type")
        if kind == ASSISTANT_TEXT_BLOCK:
            text = block.get("text")
            if not isinstance(text, str):
                raise TranscriptError(line, "text block without text")
            if text.strip():
                texts.append(text)
        elif kind in DROPPED_ASSISTANT_BLOCKS:
            continue
        else:
            raise TranscriptError(line, f"unknown block type {kind!r} in a message of the model")
    if not texts:
        return
    ts = check_timestamp(record, line)
    segments = [Segment(t) for t in texts]
    last = export.entries[-1] if export.entries else None
    if isinstance(last, Turn) and last.author == "Model":
        last.segments.extend(segments)
        if last.lines[-1] != line:
            last.lines.append(line)
    else:
        export.entries.append(Turn("Model", ts, [line], segments))


def read_attachment(record: dict, line: int, export: Export) -> None:
    attachment = record.get("attachment")
    if not isinstance(attachment, dict):
        raise TranscriptError(line, "attachment record without an attachment")
    kind = attachment.get("type")
    if kind in DROPPED_ATTACHMENT_TYPES:
        return
    if kind != "queued_command":
        raise TranscriptError(line, f"unknown attachment type {kind!r}")
    mode = attachment.get("commandMode")
    if mode == "task-notification":
        return
    if mode != "prompt":
        raise TranscriptError(line, f"unknown commandMode {mode!r} of a queued command")
    okind = origin_kind(attachment, line)
    if okind in DROPPED_ORIGINS:
        return
    if okind not in HUMAN_ORIGINS:
        raise TranscriptError(line, f"unknown origin {okind!r} of a queued command")
    if attachment.get("isMeta") or record.get("isMeta"):
        # Seen only on subagent hand-backs (origin "peer", dropped above). On
        # a message of Luciano's it would be a shape not seen before.
        raise TranscriptError(line, "queued command marked isMeta with a human origin")
    segments = luciano_segments(as_blocks(attachment.get("prompt"), line), line)
    if segments:
        ts = check_timestamp(record, line)
        export.entries.append(Turn("Luciano", ts, [line], segments, queued=True))


def read_system(record: dict, line: int, export: Export) -> None:
    subtype = record.get("subtype")
    if subtype not in DROPPED_SYSTEM_SUBTYPES:
        raise TranscriptError(line, f"unknown system subtype {subtype!r}")


READERS = {
    "user": read_user,
    "assistant": read_assistant,
    "attachment": read_attachment,
    "system": read_system,
}


def read_transcript(data: bytes) -> Export:
    export = Export()
    for line, raw in enumerate(data.split(b"\n"), start=1):
        if not raw.strip():
            if line == data.count(b"\n") + 1:
                break  # the empty string after the final newline
            raise TranscriptError(line, "empty line")
        try:
            record = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise TranscriptError(line, f"not a JSON object ({e}); if the session is still running, run again")
        if not isinstance(record, dict):
            raise TranscriptError(line, "not a JSON object")
        sid = record.get("sessionId")
        if sid is not None:
            if export.session_id is None:
                export.session_id = sid
            elif sid != export.session_id:
                raise TranscriptError(line, f"session id {sid} differs from {export.session_id}")
        rtype = record.get("type")
        if rtype in DROPPED_RECORD_TYPES:
            continue
        reader = READERS.get(rtype)
        if reader is None:
            raise TranscriptError(line, f"unknown record type {rtype!r}")
        if record.get("isSidechain"):
            # A subagent's line. Its work reaches the conversation, if at all,
            # through the model's own text.
            continue
        reader(record, line, export)
    if export.session_id is None:
        raise TranscriptError(1, "no record carries a session id")
    return export


# --- Writing the export --------------------------------------------------

def load_private_words(path: Path) -> list[str]:
    words = []
    # utf-8-sig: a byte-order mark an editor may add must not hide the first word.
    for entry in path.read_text(encoding="utf-8-sig").splitlines():
        entry = entry.strip()
        if entry:
            words.append(entry)
    return words


def private_pattern(word: str) -> re.Pattern:
    # The spaces of a phrase match any run of white space, line breaks too.
    # Words and turns are compared in composed form (NFC), so an accented
    # letter matches however it was typed.
    parts = [re.escape(p) for p in unicodedata.normalize("NFC", word).split()]
    return re.compile(r"\s+".join(parts), re.IGNORECASE)


def turn_text(turn: Turn) -> str:
    return "\n\n".join(s.text for s in turn.segments)


def fence_for(text: str) -> str:
    longest = max((len(m.group(0)) for m in re.finditer(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


FENCE_LINE_RE = re.compile(r"\A {0,3}(`{3,}|~{3,})(.*)\Z")


def leaves_fence_open(text: str) -> bool:
    """Whether the text opens a Markdown code fence it never closes.

    Such a text, rendered as it is, would turn every later turn into code (a
    terminal banner of "~~~" lines typed into a message does this).
    """
    open_fence = None
    for line in text.split("\n"):
        m = FENCE_LINE_RE.match(line)
        if not m:
            continue
        run, rest = m.group(1), m.group(2)
        if open_fence is None:
            if not (run[0] == "`" and "`" in rest):  # a backtick fence's info has no backtick
                open_fence = run
        elif run[0] == open_fence[0] and len(run) >= len(open_fence) and not rest.strip():
            open_fence = None
    return open_fence is not None


def render_segment(seg: Segment) -> str:
    if not seg.pasted:
        text = seg.text.strip("\n")
        if leaves_fence_open(text):
            fence = fence_for(text)
            return f"{fence}\n{text}\n{fence}"
        return text
    fence = fence_for(seg.text)
    return f"{PASTED_LABEL}\n\n{fence}\n{seg.text}\n{fence}"


def format_timestamp(ts: str) -> str:
    m = TIMESTAMP_RE.match(ts)
    return f"{m.group(1)} {m.group(2)} UTC"


def format_lines(lines: list[int]) -> str:
    if len(lines) == 1:
        return f"line {lines[0]}"
    return "lines " + ", ".join(str(n) for n in lines)


def heading(number: int, turn: Turn) -> str:
    parts = [f"## Turn {number}. {turn.author}", format_timestamp(turn.timestamp), format_lines(turn.lines)]
    if turn.queued:
        parts.append("sent while the model worked")
    return ", ".join(parts)


def render(export: Export, sha256: str, private_words: list[str]) -> str:
    turns = [e for e in export.entries if isinstance(e, Turn)]
    patterns = [(w, private_pattern(w)) for w in private_words]

    out = [
        "---",
        f"session: {export.session_id}",
        f"transcript_sha256: {sha256}",
        f"turns: {len(turns)}",
        f"script_version: {SCRIPT_VERSION}",
        "---",
        "",
        "## Turns with private words",
        "",
    ]
    hits = []
    for number, turn in enumerate(turns, start=1):
        text = unicodedata.normalize("NFC", turn_text(turn))
        found = [w for w, p in patterns if p.search(text)]
        if found:
            hits.append(f"- Turn {number}, {turn.author}, {format_lines(turn.lines)}: {', '.join(found)}")
    out.extend(hits if hits else ["none"])
    out.append("")

    number = 0
    for entry in export.entries:
        if isinstance(entry, Marker):
            out.extend([entry.text, ""])
            continue
        number += 1
        out.extend([heading(number, entry), ""])
        for seg in entry.segments:
            out.extend([render_segment(seg), ""])
    return "\n".join(out)


def default_out(export: Export) -> Path:
    turns = [e for e in export.entries if isinstance(e, Turn)]
    if not turns:
        raise TranscriptError(1, "no turns to export, so no date for the file name")
    date = TIMESTAMP_RE.match(turns[0].timestamp).group(1)
    return DEFAULT_OUT_DIR / f"{date}_{export.session_id[:8]}.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("transcript", type=Path, help="a Claude Code transcript (.jsonl)")
    parser.add_argument("--out", type=Path, help="output path (default: record/chat/<date>_<session8>.md)")
    args = parser.parse_args(argv)

    try:
        data = args.transcript.read_bytes()
    except OSError as e:
        print(f"{args.transcript}: {e.strerror}", file=sys.stderr)
        return 2
    # luthier is public: only a luthier session may land in its record/chat/ without saying so.
    if args.out is None and not args.transcript.resolve().parent.name.endswith("-luthier"):
        print(f"{args.transcript}: not a session of the luthier project; pass --out "
              "(a session of sonolocalizacion goes to that repository's record/chat/)", file=sys.stderr)
        return 2
    sha256 = hashlib.sha256(data).hexdigest()
    try:
        export = read_transcript(data)
        out = args.out if args.out is not None else default_out(export)
    except TranscriptError as e:
        print(e, file=sys.stderr)
        return 2
    private_words = load_private_words(PRIVATE_WORDS_FILE)
    text = render(export, sha256, private_words)

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    n_turns = sum(isinstance(e, Turn) for e in export.entries)
    print(f"{out}: {n_turns} turns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
