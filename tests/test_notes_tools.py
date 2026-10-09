"""scripts/import_notes.py, scripts/extract_notes_ideas.py (with a stub claude) and the written-note
format of scripts/ideas_timeline.py."""
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
IMPORT = ROOT / "scripts" / "import_notes.py"
EXTRACT = ROOT / "scripts" / "extract_notes_ideas.py"
TIMELINE = ROOT / "scripts" / "ideas_timeline.py"

META_XML = """<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/"><office:meta>
<meta:creation-date>2023-03-13T14:48:27.880977827</meta:creation-date><dc:date>2023-03-29T18:28:11.289373570</dc:date>
<meta:document-statistic meta:word-count="7"/></office:meta></office:document-meta>"""

CLAUDE_STUB = r'''#!PYTHON
import json, os, sys
from pathlib import Path
prompt = sys.stdin.read()
with Path(os.environ["STUB_LOG"]).open("a", encoding="utf-8") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "prompt": prompt}) + "\n")
print("## Ideas\n\n### cadena-de-asignaciones\n- **What**: A program is a chain of assignments.\n"
      "- **Quote**: \"Luthier es una cadena de asignaciones\" (line 3)\n\n"
      "### wrong-line\n- **What**: x\n- **Quote**: \"cada asignacion tiene un identificador\" (line 1)\n\n"
      "### invented\n- **What**: y\n- **Quote**: \"esto no esta en la nota\" (line 2)\n")
'''


def make_odt(path: Path, body_md: str) -> None:
    tmp = path.with_suffix(".src.md")
    tmp.write_text(body_md, encoding="utf-8")
    subprocess.run(["pandoc", str(tmp), "-o", str(path)], check=True)
    tmp.unlink()
    # replace meta.xml with one that carries the dates
    src = zipfile.ZipFile(path)
    items = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    with zipfile.ZipFile(path, "w") as z:
        for info, data in items:
            if info.filename == "meta.xml":
                continue
            z.writestr(info, data)
        z.writestr("meta.xml", META_XML)


pandoc = shutil.which("pandoc")


@pytest.mark.skipif(pandoc is None, reason="pandoc not installed")
def test_import_converts_odt_with_its_dates_and_copies_model_texts(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    make_odt(src / "hacia Luthier.odt", "tema la vaca\n\nLuthier es una cadena de asignaciones.\n\ncada asignacion tiene un identificador\n")
    (src / "manifesto.md").write_text("# Manifesto\n\nTypes as entities.\n", encoding="utf-8")
    notes, model = tmp_path / "notes", tmp_path / "model"
    r = subprocess.run([sys.executable, str(IMPORT), str(src), "--notes-out", str(notes), "--model-out", str(model)],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    md = notes / "2023-03-13 hacia Luthier.md"
    assert md.exists() and (notes / "hacia Luthier.odt").exists()
    text = md.read_text()
    assert "created: 2023-03-13T14:48:27" in text and "modified: 2023-03-29T18:28:11" in text and "author: Luciano" in text
    assert "Luthier es una cadena de asignaciones." in text
    rows = [json.loads(l) for l in (notes / "manifest.jsonl").read_text().splitlines()]
    assert rows[0]["original"] == "hacia Luthier.odt" and rows[0]["created"] == "2023-03-13T14:48:27" and len(rows[0]["sha256"]) == 64
    assert (model / "manifesto.md").read_text() == "# Manifesto\n\nTypes as entities.\n"
    mrows = [json.loads(l) for l in (model / "manifest.jsonl").read_text().splitlines()]
    assert mrows[0]["author"] == "model (ChatGPT)" and mrows[0]["kind"] == "model text"


def test_extract_notes_numbers_lines_checks_quotes_and_reads_the_frontmatter(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stub = bin_dir / "claude"
    stub.write_text(CLAUDE_STUB.replace("PYTHON", sys.executable), encoding="utf-8")
    stub.chmod(0o755)
    env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    notes = tmp_path / "notes"
    (notes / "raw" / "gemini").mkdir(parents=True)
    (notes / "raw" / "gemini" / "x.md").write_text("a fetched conversation, skipped\n", encoding="utf-8")
    (notes / "manifest.jsonl").write_text("{}\n", encoding="utf-8")
    (notes / "2023-03-13 hacia Luthier.md").write_text(
        "---\ntitle: \"hacia Luthier\"\nauthor: Luciano\ncreated: 2023-03-13T14:48:27\n---\ntema la vaca\n\n"
        "Luthier es una cadena de asignaciones.\n\ncada asignacion tiene un identificador\n", encoding="utf-8")
    out = tmp_path / "ideas"
    r = subprocess.run([sys.executable, str(EXTRACT), str(notes), "--output-dir", str(out), "--cli", "claude"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    files = list(out.glob("*.md"))
    assert [f.name for f in files] == ["2023-03-13_hacia-luthier_extract_ideas_note_v1_claude-code_opus_ideas.md"]
    text = files[0].read_text()
    assert "author: Luciano" in text and "created: 2023-03-13T14:48:27" in text and "quotes_found: 1/3" in text
    assert "wrong-line: the quote is in the note but not at line 1" in r.stdout and "invented: not in the note" in r.stdout
    calls = [json.loads(l) for l in (tmp_path / "calls.jsonl").read_text().splitlines()]
    assert len(calls) == 1 and "   3  Luthier es una cadena de asignaciones." in calls[0]["prompt"]
    assert "author: Luciano" in calls[0]["prompt"] and calls[0]["argv"][calls[0]["argv"].index("--effort") + 1] == "low"
    r = subprocess.run([sys.executable, str(EXTRACT), str(notes), "--output-dir", str(out), "--check-only"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 1 and "quotes found 1/3" in r.stdout and len((tmp_path / "calls.jsonl").read_text().splitlines()) == 1


def test_timeline_reads_written_notes(tmp_path):
    d = tmp_path / "ideas"
    d.mkdir()
    (d / "2023-03-13_hacia-luthier_extract_ideas_note_v1_claude-code_opus_ideas.md").write_text(
        "---\nnote: 2023-03-13 hacia Luthier.md\nnote_dir: HoTTification\nnote_sha256: abc\ntitle: \"hacia Luthier\"\n"
        "author: Luciano\ncreated: 2023-03-13T14:48:27\nideas: 1\nquotes_found: 1/1\ngenerated_by: extract_ideas_note_v1\n"
        "prompt_sha256: def\nmode: editor\nagent: claude-code\nmodel: opus\neffort: low\n---\n\n## Ideas\n\n"
        "### cadena-de-asignaciones\n- **What**: A program is a chain of assignments.\n"
        "- **Quote**: \"Luthier es una cadena de asignaciones\" (line 3)\n- **Also at**: lines 9\n", encoding="utf-8")
    (d / "2025-06-17_glossary_extract_ideas_note_v1_claude-code_opus_ideas.md").write_text(
        "---\nnote: vault_glossary_v1.md\nauthor: model (ChatGPT)\ncreated: 2025-06-17T06:23:00\n"
        "generated_by: extract_ideas_note_v1\n---\n\n## Ideas\n\n### types-as-entities\n- **What**: x\n"
        "- **Quote**: \"Types as entities\" (line 8)\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(TIMELINE), str(d), "--date", "2026-01-02"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rows = [json.loads(l) for l in (d / "timeline.jsonl").read_text().splitlines()]
    assert [x["id"] for x in rows] == ["written:2023-03-13_hacia-luthier:cadena-de-asignaciones", "written:2025-06-17_glossary:types-as-entities"]
    assert rows[0]["who"] == "Luciano" and rows[0]["time_local"] == "2023-03-13 14:48:27" and rows[0]["time_utc"] == "2023-03-13T17:48:27Z"
    assert rows[0]["source"] == "2023-03-13 hacia Luthier.md line 3" and rows[0]["quote"] == "Luthier es una cadena de asignaciones"
    assert rows[1]["who"] == "model" and rows[1]["extractor"] == "written"
    assert "| 2023-03 | 1 | 0 | 1 |" in (d / "timeline.md").read_text()
