"""scripts/assemble_synthesis.py on small outputs: the summary, the themes with their open tensions and
Luciano's latent seeds, the candidates with a Mark line, the rules with no idea. No model."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_assemble(tmp_path):
    rows = [{"id": f"r{i}", "time_utc": f"2026-05-2{i}T10:00:00Z", "time_local": f"2026-05-2{i} 07:00:00",
             "who": "Luciano" if i < 3 else "model", "quote": f"cita {i}", "what": "x", "source": f"n{i}.md"} for i in range(1, 4)]
    (tmp_path / "tl.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    lin = {"lineages": {f"L-{i}": {"id": f"L-{i}", "scope": "language", "statement": f"Idea {i}."} for i in range(1, 4)},
           "assign": {f"r{i}": {"lineage": f"L-{i}", "relation": "states"} for i in range(1, 4)}, "unplaced": {}}
    (tmp_path / "lin.json").write_text(json.dumps(lin))
    labels = {"l1": "L-1", "l2": "L-2", "l3": "L-3"}
    (tmp_path / "themes.json").write_text(json.dumps({"labels": labels, "answer": {
        "themes": [{"id": "T1", "name": "Types", "about": "what types are"}],
        "lineages": [["l1", "T1", "open_tension"], ["l2", "T1", "latent_seed"], ["l3", "T1", "latent_seed"]]}}))
    (tmp_path / "found.json").write_text(json.dumps({"prompt": "find_principles_v2", "lineage_labels": labels, "answer": {"candidates": [
        {"id": "C1", "statement": "A type is a theory.", "instead_of": "a tag", "lineages": ["L-1"], "quote_row": "r1", "quote": "cita 1",
         "strongest": {"axis": "conceptual", "why": "reframes"}}]}}))
    (tmp_path / "match.json").write_text(json.dumps({"prompt": "match_principles_v1", "answer": {"matches": [
        {"candidate": "C1", "verdict": "new", "principle": "", "change": ""}]}}))
    (tmp_path / "rules.json").write_text(json.dumps({"rules": [
        {"id": "R1", "kind": "spec", "source": "docs/spec/05.md:1", "title": "Declared names."},
        {"id": "D-1", "kind": "decision", "source": "record/decisions.md", "title": "One log."}],
        "answer": {"traces": [["R1", ["l1"]], ["D-1", []]]}}))
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "assemble_synthesis.py"), "--themes", str(tmp_path / "themes.json"),
                        "--found", str(tmp_path / "found.json"), "--match", str(tmp_path / "match.json"), "--rules", str(tmp_path / "rules.json"),
                        "--lineages", str(tmp_path / "lin.json"), "--timeline", str(tmp_path / "tl.jsonl"), "--output-dir", str(tmp_path),
                        "--date", "2026-01-02", "--seeds-per-theme", "1"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    md = (tmp_path / "2026-01-02_synthesis.md").read_text()
    assert "3 ideas in 1 themes; 0 seedling, 2 latent seed, 1 open tension" in md
    assert "*open tension*: Idea 1." in md and "*latent seed*: Idea 2." in md and "Idea 3." not in md.split("## 2.")[0].split("| Types")[1]
    assert "and 1 more latent seeds in the full map (1 first said by a model)" in md
    assert "C1  A type is a theory." in md and "Instead of: a tag" in md and "In force:   new" in md and "Mark:" in md
    assert "**D-1** One log." in md and "1 come from at least one idea, 1 from none" in md
