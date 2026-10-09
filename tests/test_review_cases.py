"""scripts/review_cases.py: the frozen stratified sample, the exposure judge on a stub, the review
document, and the application of Luciano's committed marks. No model is called."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "scripts" / "review_cases.py"


def case(i, decided="luciano_choice", status="explicitly_discussed", areas=("method",), repo="luthier", **kw):
    return {"id": f"C-s:{i}", "unit": f"s:{i}", "time": "2026-09-20T10:00:00Z", "is_decision": True, "question": f"Q{i}?",
            "A": "keep", "B": "drop", "actual": "A", "decided_by": decided, "counterfactual_status": status,
            "areas": list(areas), "session_repo": repo, "account": 1, "commits": [], "approved": False,
            "evidence": {"chosen": "mantengamos", "counterfactual": "quitemos", "decided_by": "mantengamos"}, **kw}


def cases_file(tmp_path):
    cs = [case(i) for i in range(10)] + [case(10 + i, decided="luciano_confirmation", areas=("language",)) for i in range(6)]
    cs += [case(20, status="constructed"), case(21, decided="model_margin"), case(22, decided="model_margin", reverses=[{"unit": "s:1"}]),
           {"id": "C-s:23", "unit": "s:23", "is_decision": False}]
    p = tmp_path / "cases.jsonl"
    p.write_text("".join(json.dumps(c) + "\n" for c in cs))
    return p


def run(*args, env=None):
    return subprocess.run([sys.executable, str(REVIEW), *map(str, args)], capture_output=True, text=True, env=env)


def test_draw_is_stratified_frozen_and_keeps_every_reversal(tmp_path):
    p = cases_file(tmp_path)
    r = run("draw", "--cases", p, "--output-dir", tmp_path, "--n", "8", "--date", "2026-01-02")
    assert r.returncode == 0, r.stderr
    s = json.loads((tmp_path / "sample_2026-01-02.json").read_text())
    assert len(s["cases"]) == 8 and "C-s:22" in s["cases"]  # the reversal, though model_margin
    assert not {"C-s:20", "C-s:21", "C-s:23"} & set(s["cases"])  # constructed, model_margin, no decision
    assert any(c in s["cases"] for c in (f"C-s:{10 + i}" for i in range(6)))  # the smaller stratum is represented
    r = run("draw", "--cases", p, "--output-dir", tmp_path, "--n", "8", "--date", "2026-01-03")
    assert r.returncode == 2 and "never redrawn" in r.stderr


def test_write_then_apply_only_committed_marks(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    g = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True)
    g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t")
    p = cases_file(repo)
    (repo / "sample_2026-01-02.json").write_text(json.dumps({"date": "2026-01-02", "seed": 1, "cases": ["C-s:1", "C-s:2", "C-s:3"]}))
    (repo / "exposure_2026-01-02.jsonl").write_text(json.dumps({"case": "C-s:2", "answer": {"exposure": [
        {"principle": "P11", "level": "possible", "quote": "nunca hardcodear"}, {"principle": "P10", "level": "none", "quote": ""}]}}) + "\n")
    r = run("write", "--cases", p, "--output-dir", repo, "--sample", repo / "sample_2026-01-02.json")
    assert r.returncode == 0, r.stderr
    md = (repo / "review_2026-01-02.md").read_text()
    assert "## C-s:1" in md and "Exposure P11 (possible): \"nunca hardcodear\"" in md and "Exposure P10" not in md
    md = md.replace("## C-s:1", "## C-s:1", 1)
    marked = []
    for block in md.split("\n## "):
        if block.startswith("C-s:1"):
            block = block.replace("Mark: ", "Mark: ok").replace("Tradeoff: ", "Tradeoff: speed against clarity")
        elif block.startswith("C-s:2"):
            block = block.replace("Mark: ", "Mark: no").replace("Exposure P11: ", "Exposure P11: ok")
        elif block.startswith("C-s:3"):
            block = block.replace("Mark: ", "Mark: the alternative should be to postpone")
        marked.append(block)
    (repo / "review_2026-01-02.md").write_text("\n## ".join(marked))
    r = run("apply", "--cases", p, "--review", repo / "review_2026-01-02.md")
    assert r.returncode == 2 and "commit the marked review first" in r.stderr
    g("add", "."); g("commit", "-q", "-m", "marks")
    r = run("apply", "--cases", p, "--review", repo / "review_2026-01-02.md")
    assert r.returncode == 0, r.stderr
    cs = {c["id"]: c for c in map(json.loads, p.read_text().splitlines())}
    assert cs["C-s:1"]["approved"] is True and cs["C-s:1"]["review"]["tradeoff"] == "speed against clarity"
    assert cs["C-s:2"]["approved"] is False and cs["C-s:2"]["review"]["exposure"] == {"P11": "ok"}
    assert cs["C-s:3"]["approved"] is False and cs["C-s:3"]["review"]["verdict"] == "correction"
    assert cs["C-s:4"]["approved"] is False and "review" not in cs["C-s:4"]


JUDGE_STUB = r'''#!PYTHON
import json, os, re, sys
from pathlib import Path
if "--version" in sys.argv:
    print("9.9.9"); sys.exit(0)
prompt = sys.stdin.read()
Path(os.environ["STUB_LOG"]).open("a").write(json.dumps({"prompt": prompt}) + "\n")
bad = Path(os.environ["STUB_LOG"] + ".bad")
quote = "un criterio no se hardcodea" if bad.exists() else "words nobody said"
bad.write_text("x")
ps = re.findall(r"^- (P\d+):", prompt, re.M)
print(json.dumps({"exposure": [{"principle": p, "level": "explicit" if p == "P11" else "none",
                                "quote": quote if p == "P11" else ""} for p in ps]}))
'''


def test_exposure_judge_reads_the_session_up_to_the_decision(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "claude").write_text(JUDGE_STUB.replace("PYTHON", sys.executable))
    (bin_dir / "claude").chmod(0o755)
    t = tmp_path / "s.jsonl"
    t.write_text("".join(json.dumps(x) + "\n" for x in [
        {"type": "user", "message": {"content": "un criterio no se hardcodea"}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "entendido"}]}},
        {"type": "user", "message": {"content": "mantengamos la regla"}},
        {"type": "user", "message": {"content": "esto viene despues y no lo ve el juez"}}]))
    (tmp_path / "units.jsonl").write_text(json.dumps({"id": "s:3", "source": str(t), "luciano": {"line": 3}}) + "\n")
    (tmp_path / "cases.jsonl").write_text(json.dumps(case(3)) + "\n" + json.dumps(case(4)) + "\n")
    (tmp_path / "elig.jsonl").write_text("".join(json.dumps(x) + "\n" for x in [
        {"unit": "s:3", "principle": "P11", "eligible": True}, {"unit": "s:3", "principle": "P10", "eligible": True},
        {"unit": "s:4", "principle": "P11", "eligible": False}]))
    (tmp_path / "dates.json").write_text(json.dumps({"principles": {
        "P11": {"statement": "Every criterion is a parameter.", "quote": "nunca hardcodear"},
        "P10": {"statement": "The invariant of its type.", "quote": "invariante"}}}))
    (tmp_path / "sample_2026-01-02.json").write_text(json.dumps({"date": "2026-01-02", "seed": 1, "cases": ["C-s:3", "C-s:4"]}))
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env['PATH']}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    r = run("exposure", "--cases", tmp_path / "cases.jsonl", "--output-dir", tmp_path, "--sample", tmp_path / "sample_2026-01-02.json",
            "--units", tmp_path / "units.jsonl", "--eligibility", tmp_path / "elig.jsonl", "--dates", tmp_path / "dates.json",
            "--cli", "claude", env=env)
    assert r.returncode == 0, r.stderr
    out = [json.loads(l) for l in (tmp_path / "exposure_2026-01-02.jsonl").read_text().splitlines()]
    assert [o["case"] for o in out] == ["C-s:3"]  # C-s:4 is eligible for nothing
    assert {e["principle"]: e["level"] for e in out[0]["answer"]["exposure"]} == {"P11": "explicit", "P10": "none"}
    assert len(out[0]["attempts"]) == 2 and "not in the session" in out[0]["attempts"][0]["errors"][0]
    prompt = json.loads((tmp_path / "calls.jsonl").read_text().splitlines()[0])["prompt"]
    assert "mantengamos la regla" in prompt and "esto viene despues" not in prompt
