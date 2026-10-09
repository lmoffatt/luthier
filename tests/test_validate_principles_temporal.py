"""scripts/validate_principles_temporal.py with a stub in place of the claude command line: which
cases enter, the blind payload, the swap of A and B, unstable answers, NEITHER, the baselines, the
D10 rule, conflicts, zero denominators, and that a run never overwrites another. No model is called."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAL = ROOT / "scripts" / "validate_principles_temporal.py"

STUB = r'''#!PYTHON
import json, os, re, sys
from pathlib import Path
if "--version" in sys.argv:
    print("9.9.9"); sys.exit(0)
prompt = sys.stdin.read()
Path(os.environ["STUB_LOG"]).open("a").write(json.dumps({"prompt": prompt}) + "\n")
principle = prompt.split("## The principle")[1].split("## Your answer")[0] if "## The principle" in prompt else ""
items = re.findall(r"^(\d+)\. .*\n   A: (.*)\n   B: (.*)$", prompt, re.M)
out = []
for k, a, b in items:
    if "KEEP" in principle:
        ch = "A" if "keep" in a else ("B" if "keep" in b else "NEITHER")
        if os.environ.get("STUB_DISAGREE") and len(items) > 1:
            ch = {"A": "B", "B": "A"}.get(ch, ch)
    elif "DROP" in principle:
        ch = "A" if "drop" in a else ("B" if "drop" in b else "NEITHER")
    elif "POSITION" in principle:
        ch = "A"
    else:
        ch = "NEITHER"
    out.append({"case": int(k), "choice": ch, "confidence": 0.8, "reason": "stub"})
print(json.dumps({"answers": out}))
'''


def case(i, actual="A", **kw):
    return {"id": f"C-s:{i}", "unit": f"s:{i}", "time": f"2026-09-2{i}T10:00:00Z", "is_decision": True, "question": f"Question {i}?",
            "A": "keep the rule" if actual == "A" else "drop the rule", "B": "drop the rule" if actual == "A" else "keep the rule",
            "actual": actual, "decided_by": "luciano_choice", "counterfactual_status": "explicitly_discussed",
            "approved": True, "commits": ["abcdef1234"], **kw}


def setup(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    (bin_dir / "claude").write_text(STUB.replace("PYTHON", sys.executable))
    (bin_dir / "claude").chmod(0o755)
    cases = [case(1), case(2), case(3, actual="B"), case(4),
             case(5, approved=False), case(6, counterfactual_status="constructed"),
             case(7, review={"exposure": {"P1": "no"}}), case(8)]
    (tmp_path / "cases.jsonl").write_text("".join(json.dumps(c) + "\n" for c in cases))
    elig = [{"unit": f"s:{i}", "principle": "P1", "eligible": True} for i in range(1, 9)]
    elig += [{"unit": f"s:{i}", "principle": "P2", "eligible": True} for i in (1, 2)]
    elig += [{"unit": f"s:{i}", "principle": "P3", "eligible": True} for i in (1, 3)]
    (tmp_path / "elig.jsonl").write_text("".join(json.dumps(e) + "\n" for e in elig))
    (tmp_path / "expo.jsonl").write_text("".join(json.dumps(x) + "\n" for x in [
        {"case": "C-s:7", "answer": {"exposure": [{"principle": "P1", "level": "possible", "quote": "q"}]}},   # he said no: in
        {"case": "C-s:8", "answer": {"exposure": [{"principle": "P1", "level": "possible", "quote": "q"}]}}]))  # unmarked: out
    (tmp_path / "dates.json").write_text(json.dumps({"principles": {
        "P1": {"statement": "KEEP what decides cases."}, "P2": {"statement": "POSITION matters."},
        "P3": {"statement": "DROP what does not pay."}, "P4": {"statement": "Something unrelated."}}}))
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env['PATH']}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    return env


def run(tmp_path, env, *args):
    return subprocess.run([sys.executable, str(VAL), "--cases", str(tmp_path / "cases.jsonl"), "--eligibility", str(tmp_path / "elig.jsonl"),
                           "--exposure", str(tmp_path / "expo.jsonl"), "--dates", str(tmp_path / "dates.json"),
                           "--output-dir", str(tmp_path / "runs"), "--cli", "claude", "--stamp", "T", *args],
                          capture_output=True, text=True, env=env)


def calls(tmp_path):
    return [json.loads(l)["prompt"] for l in (tmp_path / "calls.jsonl").read_text().splitlines()]


def test_scores_outcomes_baselines_and_conflicts(tmp_path):
    env = setup(tmp_path)
    r = run(tmp_path, env, "--mode", "batch")
    assert r.returncode == 0, r.stderr
    rep = json.loads((tmp_path / "runs" / "T_temporal_principles_opus.json").read_text())
    p1, p2, p3 = rep["results"]["P1"], rep["results"]["P2"], rep["results"]["P3"]
    # cases 1-4 and 7 enter P1; 5 unapproved, 6 constructed, 8 possibly exposed and unmarked
    assert p1["target"]["n"] == 5 and p1["target"]["accuracy"] == 1.0 and p1["outcomes"]["picked_chosen"] == 5
    assert p2["outcomes"]["unstable"] == 2 and p2["target"]["applicable"] == 0 and p2["target"]["accuracy"] is None
    # P3 picks "drop" in both its cases, where "keep" was chosen and P1 picked it: two conflicts lost
    assert p3["outcomes"] == {"picked_chosen": 0, "lost_conflict": 2, "against_all": 0, "neither": 0, "unstable": 0}
    assert p1["B0"]["accuracy"] is None and p1["B0"]["neither"] == 5  # the baseline never discriminates
    assert p1["B2"]["n"] == 5 and rep["b2_derangement"]["P1"] != "P1"
    assert [(c["case"], c["pair"]) for c in rep["conflicts"]] == [("C-s:1", ["P1", "P3"]), ("C-s:3", ["P1", "P3"])]
    for prompt in calls(tmp_path):  # the payload is blind
        assert "C-s:" not in prompt and "s:1" not in prompt and "2026-09" not in prompt and "abcdef1" not in prompt
        assert "luciano" not in prompt.lower().split("## the decisions")[-1]
    md = (tmp_path / "runs" / "T_temporal_principles_opus.md").read_text()
    assert "| P1 | 5 | 1.0 | 5 | 0 | 0 | 0 | 0 | 1.00 [" in md and "null" in md
    r = run(tmp_path, env, "--mode", "batch")
    assert r.returncode == 2 and "exists" in r.stderr  # never overwrites a run


def test_d10_falls_back_to_one_case_per_call(tmp_path):
    env = setup(tmp_path)
    env["STUB_DISAGREE"] = "1"
    r = run(tmp_path, env, "--subset", "4")
    assert r.returncode == 0, r.stderr
    rep = json.loads((tmp_path / "runs" / "T_temporal_principles_opus.json").read_text())
    assert rep["mode"] == "single" and rep["d10_agreement"] < 0.9
    assert rep["results"]["P1"]["target"]["accuracy"] == 1.0  # one case per call, the stub agrees with itself


def test_include_possible_and_nothing_to_score(tmp_path):
    env = setup(tmp_path)
    r = run(tmp_path, env, "--mode", "batch", "--include-possible", "--stamp", "S")
    assert r.returncode == 0, r.stderr
    rep = json.loads((tmp_path / "runs" / "S_temporal_principles_opus.json").read_text())
    assert rep["results"]["P1"]["target"]["n"] == 6
    (tmp_path / "elig.jsonl").write_text("")
    r = run(tmp_path, env, "--stamp", "U")
    assert r.returncode == 1 and "nothing to score" in r.stderr


def test_wilson_and_payload_guard():
    spec = importlib.util.spec_from_file_location("v", VAL)
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    assert v.wilson(0, 0) is None and v.wilson(5, 10) == [0.237, 0.763]
    c = case(1)
    text, order = v.payload([c], swapped=True)
    assert "A: drop the rule" in text and order == ["C-s:1"]
    try:
        v.guard(text + " C-s:1", [c])
        assert False
    except RuntimeError as e:
        assert "C-s:1" in str(e)
