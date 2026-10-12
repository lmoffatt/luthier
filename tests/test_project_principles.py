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
