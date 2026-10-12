"""project_principles: the record's entries parse, the projection keeps formulation and status and
drops quotes, sources and history, and the check finds an undefined tag."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import project_principles as pp  # noqa: E402

RECORD = """# The record

## The drafts

| Draft | Commit |
|---|---|
| 1 | abc |

## Terms

A *theory* is a type with laws.

## The organizers

```
G0  Type theory is the guide.
Tier:       the guide
Formulation: a type is a proposition and a value
            its proof.
Quote:      "la guía es la teoría de tipos" (audio)
Source:     audio 09.19
Status:     settled
History:    draft 2 (cd24137): stated.
```

(History: an aside the projection drops.)

### From the guide, G0

```
L2  A type is a proposition, and membership
    is a guarantee.
From:       G0 directly
Formulation: belonging to a type asserts its laws.
Status:     settled
```
"""


def test_parse_entries_and_prose():
    items = pp.parse_record(RECORD)
    entries = [e for k, e in items if k == "entry"]
    assert [e["tag"] for e in entries] == ["G0", "L2"]
    assert entries[0]["Formulation"] == "a type is a proposition and a value its proof."
    assert entries[1]["statement"] == "A type is a proposition, and membership is a guarantee."
    assert entries[1]["From"] == "G0 directly"
    prose = [p for k, p in items if k == "prose"]
    assert any(p.startswith("## Terms") for p in prose)
    assert not any("The drafts" in p for p in prose)


def test_projection_keeps_and_drops(monkeypatch):
    monkeypatch.setattr(pp, "record_commit", lambda: "abc1234")
    text = pp.project(RECORD, today="2026-10-12")
    assert "**G0. Type theory is the guide.** A type is a proposition and a value its proof." in text
    assert "Tier: the guide." in text and "Status: settled." in text
    assert "From: G0 directly." in text
    assert "la guía" not in text and "cd24137" not in text and "audio 09.19" not in text
    assert "(History:" not in text and "The drafts" not in text
    assert "abc1234" in text and pp.VERSION in text


def test_check_reports_undefined_tag(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(pp, "record_commit", lambda: "abc1234")
    proj = tmp_path / "principles.md"
    readers = tmp_path / "readers.md"
    monkeypatch.setattr(pp, "PROJECTION", proj)
    monkeypatch.setattr(pp, "READERS", readers)
    monkeypatch.setattr(pp, "REPO_ROOT", tmp_path)
    proj.write_text(pp.project(RECORD, today="2000-01-01"), encoding="utf-8")
    readers.write_text("The guide (G0) and the guarantee (L2) and a ghost (L99).", encoding="utf-8")
    assert pp.check(RECORD) == 1
    assert "L99" in capsys.readouterr().out
    readers.write_text("The guide (G0).", encoding="utf-8")
    assert pp.check(RECORD) == 0
    assert "not cited: L2" in capsys.readouterr().out


# ---- v2: clauses, the numbering section, the lints (D-2026-10-12-g, -o) -------------------------

RECORD_V2 = """# The record

## Numbering

| Draft 10 | Before |
|---|---|
| L2 | L2 |

## Terms

A *theory* is a type with laws. A certificate is the record that a law was checked at a grade.

## The organizers

```
G0  Type theory is the guide.
Tier:       the guide
Formulation: a type is a proposition and a value its proof.
Status:     settled
```

### From the guide, G0

```
L2  A type is a proposition, and membership is a guarantee.
From:       G0 directly
L2.1  Belonging to a type asserts the laws the value satisfies, through its certificate
      (D-2026-10-11-n). [settled]
L2.2  A certificate is the record that a law was checked at a grade. [proposed]
Example:    `Z7` with its ring laws, checked exhaustively (`05` R13).
References: `05` R13; P11
Rests on:   the algebra of costs
Status:     settled
```
"""


def test_parse_clauses_and_render():
    items = pp.parse_record(RECORD_V2)
    l2 = [e for k, e in items if k == "entry"][1]
    assert [c["n"] for c in l2["clauses"]] == [1, 2]
    assert l2["clauses"][0]["status"] == "settled"
    assert l2["clauses"][0]["text"].endswith("(D-2026-10-11-n).")
    assert l2["clauses"][1]["status"] == "proposed"
    assert l2["Rests on"] == "the algebra of costs"
    text = pp.render_entry(l2)
    assert "- L2.1 Belonging to a type" in text and "[settled]" in text
    assert "- L2.2 A certificate" in text and "[proposed]" in text
    assert "Example: `Z7`" in text and "References: `05` R13; P11." in text
    assert "Rests on: the algebra of costs." in text
    assert text.index("From:") < text.index("- L2.1") < text.index("Example:") < text.index("Status:")


def test_projection_ends_with_numbering(monkeypatch):
    monkeypatch.setattr(pp, "record_commit", lambda: "abc1234")
    text = pp.project(RECORD_V2, today="2026-10-12")
    assert text.rstrip().endswith("| L2 | L2 |")
    assert text.index("## Numbering") > text.index("## Terms")
    assert "Draft 10 | Before" in text


def test_lint_clauses_numbering_and_status():
    bad = RECORD_V2.replace("L2.2  A certificate", "L2.3  A certificate").replace(" [proposed]", "")
    problems = pp.lint_clauses(pp.parse_record(bad))
    assert any("numbered [1, 3]" in p for p in problems)
    assert any("L2.3: no status" in p for p in problems)
    assert pp.lint_clauses(pp.parse_record(RECORD_V2)) == []


def test_lint_references(tmp_path):
    (tmp_path / "record").mkdir()
    (tmp_path / "record/decisions.md").write_text("D-2026-10-11-n  certification by default\n", encoding="utf-8")
    (tmp_path / "record/principles.md").write_text("P11 every criterion is a parameter\n", encoding="utf-8")
    (tmp_path / "docs/spec").mkdir(parents=True)
    (tmp_path / "docs/spec/05-static-semantics.md").write_text("R13 two models refused\n", encoding="utf-8")
    assert pp.lint_references(pp.parse_record(RECORD_V2), RECORD_V2, tmp_path) == []
    bad = RECORD_V2.replace("(D-2026-10-11-n)", "(D-2026-10-11-z, L9, L2.7, P12, R14, `07` §1)")
    problems = pp.lint_references(pp.parse_record(bad), bad, tmp_path)
    joined = "\n".join(problems)
    for missing in ("D-2026-10-11-z", "L9 is not an entry", "L2.7 is not a clause", "P12", "R14", "`07`"):
        assert missing in joined, (missing, joined)
    # a class whose file is missing is not checked
    (tmp_path / "record/principles.md").unlink()
    problems = pp.lint_references(pp.parse_record(bad), bad, tmp_path)
    assert not any("P12" in p for p in problems)


def test_lint_duplicates():
    problems = pp.lint_duplicates(pp.parse_record(RECORD_V2))
    assert len(problems) == 1 and "## Terms, L2" in problems[0]
    assert "a certificate is the record" in problems[0]
    twice = RECORD_V2.replace("L2.2  A certificate is the record that a law was checked at a grade. [proposed]",
                              "L2.2  Belonging to a type asserts the laws the value satisfies, through its "
                              "certificate (D-2026-10-11-n). [proposed]")
    problems = pp.lint_duplicates(pp.parse_record(twice))
    assert any(p.startswith("L2, L2:") for p in problems)


def test_check_strict_fails_on_lints(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(pp, "record_commit", lambda: "abc1234")
    proj = tmp_path / "principles.md"
    readers = tmp_path / "readers.md"
    monkeypatch.setattr(pp, "PROJECTION", proj)
    monkeypatch.setattr(pp, "READERS", readers)
    monkeypatch.setattr(pp, "REPO_ROOT", tmp_path)
    proj.write_text(pp.project(RECORD_V2, today="2000-01-01"), encoding="utf-8")
    readers.write_text("The guide (G0) and the guarantee (L2).", encoding="utf-8")
    assert pp.check(RECORD_V2) == 0            # the duplicate sentence is information
    assert "duplicates (information)" in capsys.readouterr().out
    assert pp.check(RECORD_V2, strict=True) == 1
    assert "duplicates (problem)" in capsys.readouterr().out
