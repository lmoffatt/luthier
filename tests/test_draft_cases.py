"""scripts/draft_cases.py with a stub in place of the claude command line: the material from the
transcript, the checks of an answer and its quotes, the draw of A and B, non-decisions, units with
private words, idempotence, and refusal of provisional candidates."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT = ROOT / "scripts" / "draft_cases.py"

STUB = r'''#!PYTHON
import json, os, re, sys
from pathlib import Path
if "--version" in sys.argv:
    print("9.9.9 (stub)"); sys.exit(0)
prompt = sys.stdin.read()
log = Path(os.environ["STUB_LOG"])
with log.open("a") as f:
    f.write(json.dumps({"prompt": prompt}) + "\n")
bad = Path(os.environ["STUB_LOG"] + ".bad")
luciano = prompt.split("[LUCIANO]")[1].split("[MODEL AFTER]")[0].strip()
if "NODEC" in luciano:
    print(json.dumps({"is_decision": False, "reason_if_not": "a command"})); sys.exit(0)
quote = " ".join(luciano.split()[:4])
if os.environ.get("STUB_BAD_ONCE") and not bad.exists():
    bad.write_text("x"); quote = "words nobody said"
print(json.dumps({"is_decision": True, "question": "Which way?", "alternatives": ["keep the rule", "drop the rule"],
                  "chosen_index": 0, "counterfactual_status": "constructed", "evidence_chosen": quote,
                  "evidence_counterfactual": "", "decided_by": "luciano_choice", "evidence_decided_by": quote}))
'''


def setup(tmp_path, provisional=False):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "claude").write_text(STUB.replace("PYTHON", sys.executable))
    (bin_dir / "claude").chmod(0o755)
    t = tmp_path / "s.jsonl"
    t.write_text("".join(json.dumps(x) + "\n" for x in [
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "Propongo quitar la regla."}]}},
        {"type": "user", "message": {"content": "mantengamos la regla porque decide casos"}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "La mantengo."},
                                                       {"type": "tool_use", "name": "Edit", "input": {"file_path": "/x/a.md", "old_string": "a", "new_string": "b"}}]}},
        {"type": "user", "message": {"content": "NODEC corré los tests"}},
        {"type": "user", "message": {"content": "mirá lo de databaum"}}]))
    units = [{"id": f"s:{n}", "time": "2026-09-20T10:00:00Z", "source": str(t), "account": 1, "session_repo": "luthier",
              "areas": ["method"], "luciano": {"line": n, "text": txt}, "proposal": {"text": "Propongo quitar la regla."},
              "actions": [{"line": 3, "tool": "Edit", "files": ["/x/a.md"]}], "commits": []}
             for n, txt in ((2, "mantengamos la regla porque decide casos"), (4, "NODEC corré los tests"), (5, "mirá lo de databaum"))]
    (tmp_path / "units.jsonl").write_text("".join(json.dumps(u) + "\n" for u in units))
    (tmp_path / "cands.json").write_text(json.dumps({"provisional": provisional, "candidates": [
        {"unit": u["id"], "reasons": ["eligible for P11"], "eligible_for": ["P11"]} for u in units]}))
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env['PATH']}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    return env


def run(tmp_path, env, *args):
    return subprocess.run([sys.executable, str(DRAFT), "--candidates", str(tmp_path / "cands.json"), "--units", str(tmp_path / "units.jsonl"),
                           "--output-dir", str(tmp_path / "out"), "--cli", "claude", *args], capture_output=True, text=True, env=env)


def calls(tmp_path):
    p = tmp_path / "calls.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def test_drafts_checks_draws_and_skips(tmp_path):
    env = setup(tmp_path)
    env["STUB_BAD_ONCE"] = "1"
    r = run(tmp_path, env)
    assert r.returncode == 0, r.stderr
    cases = {c["unit"]: c for c in map(json.loads, (tmp_path / "out" / "decision_cases.jsonl").read_text().splitlines())}
    a = cases["s:2"]
    assert a["is_decision"] and a["approved"] is False and a["decided_by"] == "luciano_choice"
    assert {a["A"], a["B"]} == {"keep the rule", "drop the rule"} and a[a["actual"]] == "keep the rule"
    assert a["evidence"]["chosen"] == "mantengamos la regla porque"
    assert cases["s:4"]["is_decision"] is False and cases["s:4"]["reason_if_not"] == "a command"
    assert cases["s:5"]["skipped"] == "private words in the material"
    cs = calls(tmp_path)
    assert len(cs) == 3  # s:2 twice (its first answer quoted words not in the material), s:4 once; s:5 never sent
    assert "[MODEL AFTER]\n\nLa mantengo." in cs[0]["prompt"] and "[edit a.md]" in cs[0]["prompt"]
    assert "## Your previous answer was rejected" in cs[1]["prompt"]
    runs = [json.loads(l) for l in (tmp_path / "out" / "draft_runs.jsonl").read_text().splitlines()]
    assert len(runs[0]["attempts"]) == 2 and runs[0]["attempts"][0]["errors"]
    r = run(tmp_path, env)
    assert r.returncode == 0 and len(calls(tmp_path)) == 3 and "to draft: 0" in r.stdout


def test_the_draw_depends_on_the_seed_and_the_unit_only(tmp_path):
    env = setup(tmp_path)
    run(tmp_path, env, "--only", "s:2")
    first = json.loads((tmp_path / "out" / "decision_cases.jsonl").read_text().splitlines()[0])
    run(tmp_path, env, "--only", "s:2", "--force")
    again = json.loads((tmp_path / "out" / "decision_cases.jsonl").read_text().splitlines()[0])
    assert (first["A"], first["actual"]) == (again["A"], again["actual"])


def test_provisional_candidates_are_refused(tmp_path):
    env = setup(tmp_path, provisional=True)
    r = run(tmp_path, env)
    assert r.returncode == 2 and "provisional" in r.stderr and calls(tmp_path) == []
