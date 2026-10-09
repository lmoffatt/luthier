"""scripts/consolidate_lineages.py with a stub of the claude command line: every lineage placed once,
themes defined, states in the three classes, the retry with the errors, and the map written."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONS = ROOT / "scripts" / "consolidate_lineages.py"

STUB = r'''#!PYTHON
import json, os, re, sys
from pathlib import Path
if "--version" in sys.argv:
    print("9.9.9"); sys.exit(0)
prompt = sys.stdin.read()
Path(os.environ["STUB_LOG"]).open("a").write(json.dumps({"prompt": prompt}) + "\n")
bad = Path(os.environ["STUB_LOG"] + ".bad")
labs = re.findall(r"^(l\d+) \|", prompt, re.M)
entries = [[l, "T1" if i % 2 == 0 else "T2", ["seedling", "latent_seed", "open_tension"][i % 3]] for i, l in enumerate(labs)]
if not bad.exists():
    bad.write_text("x"); entries = entries[1:]
print(json.dumps({"themes": [{"id": "T1", "name": "Types as theories", "about": "x"}, {"id": "T2", "name": "Records", "about": "y"}],
                  "lineages": entries}))
'''


def test_map_of_ideas(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "claude").write_text(STUB.replace("PYTHON", sys.executable))
    (bin_dir / "claude").chmod(0o755)
    rows = [{"id": f"r{i}", "time_utc": f"2026-05-2{i}T10:00:00Z", "time_local": f"2026-05-2{i} 07:00:00", "who": "Luciano",
             "quote": f"cita {i}", "what": "x", "source": f"n{i}.md"} for i in range(1, 5)]
    (tmp_path / "timeline.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    state = {"lineages": {f"L-{i}": {"id": f"L-{i}", "scope": "language", "statement": f"Idea {i}."} for i in range(1, 5)},
             "assign": {f"r{i}": {"lineage": f"L-{i}", "relation": "states"} for i in range(1, 5)}, "unplaced": {}}
    (tmp_path / "lin.json").write_text(json.dumps(state))
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env['PATH']}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    r = subprocess.run([sys.executable, str(CONS), "--lineages", str(tmp_path / "lin.json"), "--timeline", str(tmp_path / "timeline.jsonl"),
                        "--output-dir", str(tmp_path / "out"), "--var", "language=Luthier", "--var", "designers=Luciano Moffatt",
                        "--cli", "claude", "--date", "2026-01-02"], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    run = json.loads((tmp_path / "out" / "2026-01-02_consolidate_lineages_v1_claude-code_opus.json").read_text())
    assert len(run["attempts"]) == 2 and "lineages not placed: 1" in run["attempts"][0]["errors"][0]
    md = (tmp_path / "out" / "2026-01-02_consolidate_lineages_v1_claude-code_opus.md").read_text()
    assert "4 ideas in 2 themes" in md and "## Types as theories" in md and "*seedling* `L-1`: Idea 1." in md
    prompt = json.loads((tmp_path / "calls.jsonl").read_text().splitlines()[0])["prompt"]
    assert "l1 | language | Luciano | 2026-05-21 | 1 | Idea 1." in prompt and '- Luciano: "cita 1"' in prompt
