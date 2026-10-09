"""scripts/ideas_timeline.py and scripts/principles_ledger.py on small fixtures: the three ideas
formats merge into one time order with the right zone, duplicates by construction are marked, and
the ledger counts For and against, pairs, idle principles, reversals and the CLAUDE.md list."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMELINE = ROOT / "scripts" / "ideas_timeline.py"
LEDGER = ROOT / "scripts" / "principles_ledger.py"


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


NOTE_FILE = """---
audio: WhatsApp Ptt 2026-05-29 at 14.03.24.mp3
fecha: 2026-05-29
duracion: ~00:30
ideas: 1
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### tipos-dependientes-como-funciones
- **Qué**: Los tipos dependientes como funciones que devuelven un tipo.
- **Cita** (verbatim): "Es como una función que tira un tipo" `[00:15]`
- **Ambigüedad / tensión**: queda como pregunta.

### rango
- **Qué**: Una idea con rango de tiempo.
- **Cita** (verbatim): "en lenguajes hay sustantivos" `[00:10–00:18]`
"""

DAY_FILE = """---
date: 2026-05-29
notes:
  - audio: WhatsApp Ptt 2026-05-29 at 14.03.24.mp3
    transcript: WhatsApp Ptt 2026-05-29 at 14.03.24.md
    duration: ~00:30
    sha256: abc
ideas: 1
quotes_found: 1/1 (match: words)
generated_by: extract_ideas_day_v1
prompt_sha256: def
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### tipos-dependientes
- **What**: Dependent types as a function that returns a type.
- **Quote**: "Es como una función que tira un tipo" (`WhatsApp Ptt 2026-05-29 at 14.03.24.mp3` `[00:15]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-29 at 14.03.24.mp3`: he works it out.
"""

DIALOGUE_FILE = """---
source: gemini
key: gemini::20260529T1400
title: "Bueno, vamos a soñar"
started: 2026-05-29T17:00:30Z
ended: 2026-05-29T18:21:51Z
thread: 2026-05-29_20260529T1400_bueno.md
thread_sha256: 123
copy: tracked
turns: 30
windows: 1
window_chars: 60000
ideas: 2
quotes_found: 2/2
generated_by: extract_ideas_dialogue_v1
prompt_sha256: 456
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### paths-entre-implementaciones
- **Who**: model
- **Turn**: 2, 2026-05-29 17:00:30 UTC
- **Kind**: proposal
- **What**: A path between two implementations.
- **Quote**: "podrías definir un Path"

### expresividad
- **Who**: Luciano
- **Turn**: 17, 2026-05-29 17:45:00 UTC
- **Kind**: decision
- **What**: Expressivity over redundancy.
- **Quote**: "garpa más"
- **Open**: when redundancy is wanted.
"""

OTHER_FILE = """---
fuentes: 42
generado_por: consolidate_ideas_v1
---

### something
- **Qué**: not an extraction
"""


def test_timeline_merges_three_formats_in_time_order_and_marks_duplicates(tmp_path):
    d = tmp_path / "ideas"
    d.mkdir()
    (d / "WhatsApp Ptt 2026-05-29 at 14.03.24_extract_ideas_v1_claude-code_opus_ideas.md").write_text(NOTE_FILE, encoding="utf-8")
    (d / "2026-05-29_extract_ideas_day_v1_claude-code_opus_ideas.md").write_text(DAY_FILE, encoding="utf-8")
    (d / "gemini_2026-05-29_20260529_extract_ideas_dialogue_v1_claude-code_opus_ideas.md").write_text(DIALOGUE_FILE, encoding="utf-8")
    (d / "_consolidated.md").write_text(OTHER_FILE, encoding="utf-8")
    r = subprocess.run([sys.executable, str(TIMELINE), str(d), "--date", "2026-01-02"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rows = [json.loads(l) for l in (d / "timeline.jsonl").read_text().splitlines()]
    # the chat turn at 17:00:30 UTC is 14:00:30 in Buenos Aires, before the note of 14:03:24
    assert [x["slug"] for x in rows] == ["paths-entre-implementaciones", "rango", "tipos-dependientes",
                                          "tipos-dependientes-como-funciones", "expresividad"]
    assert rows[1]["time_local"] == "2026-05-29 14:03:34" and rows[1]["time_utc"] == "2026-05-29T17:03:34Z"
    assert rows[0]["time_local"] == "2026-05-29 14:00:30" and rows[0]["who"] == "model" and rows[0]["kind"] == "proposal"
    assert rows[2]["extractor"] == "day" and rows[2]["also_by_note"] is True
    assert rows[3]["extractor"] == "note" and rows[3]["also_by_day"] is True and rows[3]["who"] == "Luciano"
    assert rows[3]["quote"] == "Es como una función que tira un tipo" and rows[3]["source"] == "WhatsApp Ptt 2026-05-29 at 14.03.24.md [00:15]"
    assert rows[4]["source"] == "2026-05-29_20260529T1400_bueno.md turn 17" and rows[4]["open"] == "when redundancy is wanted."
    assert {x["id"] for x in rows} == {"note:2026-05-29T14.03.24:rango", "note:2026-05-29T14.03.24:tipos-dependientes-como-funciones",
                                       "day:2026-05-29:tipos-dependientes", "dialogue:20260529T1400:paths-entre-implementaciones",
                                       "dialogue:20260529T1400:expresividad"}
    md = (d / "timeline.md").read_text()
    assert "| 2026-05 | 4 | 1 | 5 |" in md and "### 2026-05-29" in md and "(also by day)" in md and "(also per note)" in md
    assert "_consolidated.md" not in md and "sha256" in md


PRINCIPLES = """# Principles

```
P1  Luciano's part stays discernible.
Quote:      "x"
Source:     a
Assumption: b
Status:     current since 2026-10-06

P2  Everything derived carries how it was derived.
Quote:      "y"
Status:     current

P3  A principle that wraps onto a second
                line of statement.
Status:     proposed 2026-10-07
```
"""

DECISIONS = """# Decisions

D-2026-10-06-a  First decision.
Author:     Luciano
Kind:       principle. For P1, P2; against P3 unless something
Status:     current

D-2026-10-06-b  Second decision.
Kind:       principle. For P2
Status:     reversed by D-2026-10-06-c

D-2026-10-06-c  Third decision, names no principle.
Kind:       principle. P8 is met since there was a case
Status:     current

D-2026-10-06-d  Fourth, free.
Kind:       free
Status:     current
"""

CLAUDE = """# Working rules

## Principles in force

- P1 Luciano's part stays discernible.
- P2 Everything derived carries how it was derived.
- P4 Not in the file.
"""


def test_ledger_counts_for_against_pairs_reversals_and_the_list(tmp_path):
    (tmp_path / "principles.md").write_text(PRINCIPLES, encoding="utf-8")
    (tmp_path / "decisions.md").write_text(DECISIONS, encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text(CLAUDE, encoding="utf-8")
    r = subprocess.run([sys.executable, str(LEDGER), "--principles", str(tmp_path / "principles.md"),
                        "--decisions", str(tmp_path / "decisions.md"), "--claude-md", str(tmp_path / "CLAUDE.md"),
                        "--date", "2026-01-02"], capture_output=True, text=True)
    assert r.returncode == 1, r.stdout  # P8 is named and not defined
    out = r.stdout
    assert "| P1 Luciano's part stays discernible. | current | 1 | 0 | 10-06-a |  |" in out
    assert "| P2 Everything derived carries how it was derived. | current | 2 | 0 | 10-06-a, 10-06-b |  |" in out
    assert "| P3 A principle that wraps onto a second line of statement. | proposed | 0 | 1 |  | 10-06-a |" in out
    assert "| P1 | P3 | 1 | 10-06-a |" in out and "| P2 | P3 | 1 | 10-06-a |" in out
    assert "- D-2026-10-06-b: P2" in out
    assert "In CLAUDE.md and not in principles.md: P4" in out
    assert "In principles.md and not in CLAUDE.md: P3 (proposed)" in out
    assert "- D-2026-10-06-c: names P8, which principles.md does not define" in out
    assert "Guiding nothing yet (P13's measure):** none" in out


def test_ledger_history_reads_the_git_log(tmp_path):
    repo = tmp_path / "repo"
    (repo / "record").mkdir(parents=True)
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True)
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    p = repo / "record" / "principles.md"
    p.write_text(PRINCIPLES.replace("Status:     proposed 2026-10-07", "Status:     proposed"), encoding="utf-8")
    git("add", "."); git("commit", "-q", "-m", "first")
    p.write_text(PRINCIPLES, encoding="utf-8")
    git("add", "."); git("commit", "-q", "-m", "P3 status dated")
    (repo / "record" / "decisions.md").write_text("# Decisions\n", encoding="utf-8")
    mod = load(LEDGER)
    mod.REPO_ROOT = repo
    hist = mod.history(p)
    assert [h["subject"] for h in hist] == ["first", "P3 status dated"]
    assert [c[1] for c in hist[0]["changes"]] == ["added", "added", "added"]
    assert hist[1]["changes"] == [("P3", "status changed", "proposed 2026-10-07")]
