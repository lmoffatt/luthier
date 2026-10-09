"""scripts/trace_rules.py: rules read from a specification (bold identifiers, or numbered sections) and
a decision log; the trace checked and written. A stub stands in for the claude command line."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACE = ROOT / "scripts" / "trace_rules.py"

STUB = r'''#!PYTHON
import json, os, re, sys
from pathlib import Path
if "--version" in sys.argv:
    print("9.9.9"); sys.exit(0)
prompt = sys.stdin.read()
Path(os.environ["STUB_LOG"]).open("a").write(json.dumps({"prompt": prompt}) + "\n")
rules = re.findall(r"^- (\S+) \((spec|decision)\):", prompt, re.M)
bad = Path(os.environ["STUB_LOG"] + ".bad")
out = [[r, ["l1"] if r == "R1" else []] for r, _ in rules]
if not bad.exists():
    bad.write_text("x"); out[0][1] = ["l99"]
print(json.dumps({"traces": out}))
'''


def test_rules_and_their_ideas(tmp_path):
    spec = tmp_path / "spec"
    spec.mkdir()
    (spec / "05-rules.md").write_text("# Rules\n\n## 5. Rules\n\n**R1. A declaration mentions declared names.** Every name exists.\n\n"
                                      "**R2. A definition uses defined types.** Every type is defined.\n")
    (spec / "02-grammar.md").write_text("# Grammar\n\n## 0. Notation\n\nx\n\n## 1. Lexical\n\nTokens are words.\n\n## 8. Open\n\ny\n")
    (tmp_path / "decisions.md").write_text("# Decisions\n\nD-2026-10-06-a  One log per repository.\nKind:       rule\nStatus:     current\n")
    rows = [{"id": "r1", "time_utc": "2026-05-21T10:00:00Z", "time_local": "2026-05-21 07:00:00", "who": "Luciano",
             "quote": "q", "what": "x", "source": "n.md"}]
    (tmp_path / "timeline.jsonl").write_text(json.dumps(rows[0]) + "\n")
    (tmp_path / "lin.json").write_text(json.dumps({"lineages": {"L-a": {"id": "L-a", "scope": "language", "statement": "Names are declared."}},
                                                    "assign": {"r1": {"lineage": "L-a", "relation": "states"}}, "unplaced": {}}))
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "claude").write_text(STUB.replace("PYTHON", sys.executable))
    (bin_dir / "claude").chmod(0o755)
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env['PATH']}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    r = subprocess.run([sys.executable, str(TRACE), "--spec", str(spec), "--decisions", str(tmp_path / "decisions.md"),
                        "--lineages", str(tmp_path / "lin.json"), "--timeline", str(tmp_path / "timeline.jsonl"),
                        "--output-dir", str(tmp_path / "out"), "--var", "language=Luthier", "--var", "designers=Luciano Moffatt",
                        "--cli", "claude", "--date", "2026-01-02"], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    run = json.loads((tmp_path / "out" / "2026-01-02_trace_rules_v1_claude-code_opus.json").read_text())
    assert [x["id"] for x in run["rules"]] == ["S02.1", "R1", "R2", "D-2026-10-06-a"]  # notation and open sections left out
    assert len(run["attempts"]) == 2 and "are not lineages" in run["attempts"][0]["errors"][0]
    md = (tmp_path / "out" / "2026-01-02_trace_rules_v1_claude-code_opus.md").read_text()
    assert "**R1** A declaration mentions declared names." in md and "`L-a`" in md and "1 traced to at least one idea; 3 to none" in md
