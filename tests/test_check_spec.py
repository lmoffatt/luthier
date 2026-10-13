"""Tests of scripts/check_spec.py: each check is exercised on a small repository in tmp_path."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_spec.py"

CHAPTER_1 = """\
# 1. Alpha

Chapter 1 of the specification, draft 0, written for the tests of the checker.

## §1 First

**1.R1. Sound rule.** [implemented] Alpha text that stands alone and says nothing else.
It realizes L1 and L1.2, leaves O1 open, follows W5 and P11, and rests on D-2026-01-01-a.
Files: a.accept.lut, a.reject.lut.

**1.S1. A statement.** [proposed] The statement mentions `L9.9` only inside a code span.

## Open

O1.
"""

CHAPTER_2 = """\
# 2. Beta

Chapter 2 of the specification, a header paragraph that nobody checks for repeats.

## §1 Only

**2.R1. Other rule.** [decided D-2026-01-01-a] Beta text about completely different matters.
Files: a.accept.lut.

## Open

O1.
"""

PRINCIPLES = """\
# Principles

**G0. Guide.** Words of the organizer.

**L1. Entry.** Words of the entry.

- L1.2 A clause of the entry.

- **O1** An open question.
"""


def build(tmp: Path, ch1: str = CHAPTER_1, ch2: str | None = CHAPTER_2) -> Path:
    for d in ("docs/spec", "record", "tests/spec"):
        (tmp / d).mkdir(parents=True, exist_ok=True)
    (tmp / "docs/spec/00-index.md").write_text("# index\n", encoding="utf-8")
    (tmp / "docs/spec/01-alpha.md").write_text(ch1, encoding="utf-8")
    if ch2 is not None:
        (tmp / "docs/spec/02-beta.md").write_text(ch2, encoding="utf-8")
    (tmp / "docs/principles.md").write_text(PRINCIPLES, encoding="utf-8")
    (tmp / "docs/way-of-working.md").write_text("**W5. Concepts live in Luthier.** x\n", encoding="utf-8")
    (tmp / "record/decisions.md").write_text("D-2026-01-01-a  A decision.\n", encoding="utf-8")
    (tmp / "record/principles.md").write_text("P11 Every criterion is a parameter.\n", encoding="utf-8")
    for n in ("a.accept.lut", "a.reject.lut"):
        (tmp / "tests/spec" / n).write_text("", encoding="utf-8")
    return tmp


def run(tmp: Path, *files: str) -> tuple[int, list[str]]:
    r = subprocess.run([sys.executable, str(SCRIPT), "--root", str(tmp), *files],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines()


def line_of(text: str, needle: str) -> int:
    return next(i + 1 for i, l in enumerate(text.splitlines()) if needle in l)


def expect(out: list[str], path: str, line: int, fragment: str) -> None:
    prefix = f"{path}:{line}: check-spec: "
    assert any(o.startswith(prefix) and fragment in o for o in out), (prefix, fragment, out)


def test_clean_chapter_passes(tmp_path):
    build(tmp_path)
    code, out = run(tmp_path)
    assert (code, out) == (0, [])


def test_missing_status(tmp_path):
    ch = CHAPTER_1.replace("[implemented] ", "")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "**1.R1."), "1.R1 has no status")


def test_bad_decision_id(tmp_path):
    ch = CHAPTER_1.replace("[implemented]", "[decided D-2026-01-01-z]")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "**1.R1."), "D-2026-01-01-z is not in record/decisions.md")


def test_decided_by_a_settled_clause(tmp_path):
    prin = PRINCIPLES.replace("- L1.2 A clause of the entry.", "- L1.2 A clause of the entry. [settled]\n- L1.3 Another\n  clause. [proposed]")
    ch = CHAPTER_1.replace("[implemented]", "[decided L1.2]", 1)
    build(tmp_path, ch)
    (tmp_path / "docs/principles.md").write_text(prin, encoding="utf-8")
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert not any("1.R1" in l and "settled" in l for l in out)
    for clause, msg in (("L1.3", "L1.3 is not settled"), ("L1.9", "L1.9 is not a clause")):
        bad = CHAPTER_1.replace("[implemented]", f"[decided {clause}]", 1)
        build(tmp_path, bad)
        (tmp_path / "docs/principles.md").write_text(prin, encoding="utf-8")
        code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
        assert code == 1
        expect(out, "docs/spec/01-alpha.md", line_of(bad, "**1.R1."), msg)


def test_missing_accept_file(tmp_path):
    ch = CHAPTER_1.replace("Files: a.accept.lut, a.reject.lut.", "Files: a.reject.lut, b.accept.lut.")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "Files:"), "b.accept.lut not found")


def test_implemented_without_reject_or_files(tmp_path):
    ch = CHAPTER_1.replace("Files: a.accept.lut, a.reject.lut.", "Files: a.accept.lut.")
    build(tmp_path, ch)
    _, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "Files:"), "names no .reject.lut")
    ch = CHAPTER_1.replace("Files: a.accept.lut, a.reject.lut.\n", "")
    build(tmp_path, ch)
    _, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "**1.R1."), "has no Files line")


def test_unresolved_principle_citation(tmp_path):
    ch = CHAPTER_1.replace("realizes L1 and", "realizes L9.9 and")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "realizes L9.9"), "L9.9 does not resolve")


def test_unresolved_section_citation(tmp_path):
    ch = CHAPTER_1.replace("leaves O1 open", "leaves O1 open (spec 2 §2)")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "spec 2 §2"), "chapter 2 has no section 2")


def test_resolved_citations_pass(tmp_path):
    ch = CHAPTER_1.replace("leaves O1 open", "leaves O1 open (spec 2 §1, spec 2.R1)")
    build(tmp_path, ch)
    assert run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md")) == (0, [])


def test_chapter_not_written_is_information(tmp_path):
    ch = CHAPTER_1.replace("leaves O1 open", "leaves O1 open (spec 3 §2)")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 0
    line = line_of(ch, "spec 3 §2")
    assert out == [f"docs/spec/01-alpha.md:{line}: check-spec (information): chapter 3 not written"]


def test_repeated_eight_word_run_across_chapters(tmp_path):
    shared = "the model of a theory is verified by the certifier against every law"
    ch1 = CHAPTER_1.replace("Alpha text that stands alone and says nothing else.", shared + ".")
    ch2 = CHAPTER_2.replace("Beta text about completely different matters.", "Then, " + shared + ".")
    build(tmp_path, ch1, ch2)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch1, "the model of a theory"),
           "shares a run of 13 words with docs/spec/02-beta.md")


def test_repeat_within_chapter_and_with_principles(tmp_path):
    twice = "a bread of seven different green words is always baked tonight"
    ch = CHAPTER_1.replace("## Open", f"{twice}.\n\nOther things happen here. {twice}.\n\n## Open")
    build(tmp_path, ch)
    _, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert any("repeats a run from line" in o for o in out), out
    prin = "the organizer sentence which sits in the principles file verbatim"
    (tmp_path / "docs/principles.md").write_text(PRINCIPLES + f"\n{prin}.\n", encoding="utf-8")
    ch = CHAPTER_1.replace("Alpha text that stands alone and says nothing else.", prin + ".")
    (tmp_path / "docs/spec/01-alpha.md").write_text(ch, encoding="utf-8")
    _, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    expect(out, "docs/spec/01-alpha.md", line_of(ch, prin), "with docs/principles.md")


def test_header_and_code_excluded_from_duplicates(tmp_path):
    header = "A header paragraph that is long enough to repeat itself across chapters."
    ch1 = CHAPTER_1.replace("Chapter 1 of the specification, draft 0, written for the tests of the checker.", header)
    ch2 = CHAPTER_2.replace("Chapter 2 of the specification, a header paragraph that nobody checks for repeats.", header)
    build(tmp_path, ch1, ch2)
    assert run(tmp_path) == (0, [])


def test_missing_open_section(tmp_path):
    ch = CHAPTER_1.replace("## Open\n\nO1.\n", "")
    build(tmp_path, ch)
    code, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    assert code == 1
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "## §1 First"), "last section is not `## Open`")


def test_title_and_numbering(tmp_path):
    ch = CHAPTER_1.replace("# 1. Alpha", "# 7. Alpha").replace("**1.S1.", "**1.S2.")
    build(tmp_path, ch)
    _, out = run(tmp_path, str(tmp_path / "docs/spec/01-alpha.md"))
    expect(out, "docs/spec/01-alpha.md", 1, "title says chapter 7")
    expect(out, "docs/spec/01-alpha.md", line_of(ch, "**1.S2."), "1.S2 where 1.S1 was expected")


def test_unreadable_file_exits_2(tmp_path):
    build(tmp_path)
    code, _ = run(tmp_path, str(tmp_path / "docs/spec/09-missing.md"))
    assert code == 2
