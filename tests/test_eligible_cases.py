"""scripts/eligible_cases.py on fixtures: the window between a principle's explicit date and the time
it became operative for an account and a repository, Luciano's marks, boundaries, the lexical flag,
the candidates for drafting. No model is called."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ELIG = ROOT / "scripts" / "eligible_cases.py"

DATES = {"principles": {"P11": {
    "statement": "Every criterion is a parameter, never a constant in the code.",
    "quote": "nunca hardcodear un criterio", "explicit": "2026-09-10T22:20Z",
    "operative": {"luthier": {"claude_md": {"time": "2026-10-06T08:18Z", "source": "luthier@x"},
                              "memory_candidates": []},
                  "sonolocalizacion": {"claude_md": {"time": "2026-10-06T08:18Z", "source": "sono@x"},
                                       "memory_candidates": [{"note": "nunca-hardcodear.md", "account": 1,
                                                              "first_written": "2026-09-10T22:30Z", "source": "chat:x:1", "shared": 7}]}},
    "global_claude_md": {}}}}


def unit(uid, time, repo, account=1, line=3, **kw):
    return {"id": uid, "time": time, "session_repo": repo, "account": account, "source": "SRC",
            "luciano": {"line": line, "text": "x"}, **kw}


def setup(tmp_path, mark="ok; memory nunca-hardcodear.md"):
    t = tmp_path / "s.jsonl"
    t.write_text("".join(json.dumps(x) + "\n" for x in [
        {"type": "user", "message": {"content": "cada criterio del codigo tiene que ser un parameter, nunca una constante"}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "ok"}]}},
        {"type": "user", "message": {"content": "dale"}}]))
    units = [
        unit("a:1", "2026-09-10T22:20:00Z", "luthier"),            # at the explicit boundary: not eligible
        unit("a:2", "2026-09-20T10:00:00Z", "luthier"),            # in the window, luthier has no memory note
        unit("a:3", "2026-09-20T10:00:00Z", "sonolocalizacion"),   # after the memory note of account 1
        unit("a:4", "2026-09-20T10:00:00Z", "sonolocalizacion", account=2),  # account 2 never read that note
        unit("a:5", "2026-10-06T08:18:00Z", "luthier"),            # at the operative boundary: not eligible
        unit("a:6", "2026-10-07T10:00:00Z", "luthier", reverses=[{"unit": "a:2"}]),  # late, but a reversal
        unit("a:7", "2026-09-20T11:00:00Z", "luthier", withheld="private words (1)"),
    ]
    for u in units:
        u["source"] = str(t)
    (tmp_path / "units.jsonl").write_text("".join(json.dumps(u) + "\n" for u in units))
    (tmp_path / "dates.json").write_text(json.dumps(DATES))
    (tmp_path / "dates.md").write_text(f"# Dates\n\n## P11 Every criterion\n\n- explicit: ...\n\nMark: {mark}\n")
    return tmp_path


def run(tmp_path, *args):
    return subprocess.run([sys.executable, str(ELIG), "--units", str(tmp_path / "units.jsonl"), "--dates", str(tmp_path / "dates.json"),
                           "--marks", str(tmp_path / "dates.md"), "--timeline", str(tmp_path / "none.jsonl"),
                           "--output-dir", str(tmp_path / "out"), *args], capture_output=True, text=True)


def test_window_per_account_and_repository(tmp_path):
    setup(tmp_path)
    r = run(tmp_path)
    assert r.returncode == 0, r.stderr
    pairs = {p["unit"]: p for p in map(json.loads, (tmp_path / "out" / "eligibility.jsonl").read_text().splitlines())}
    assert [u for u, p in sorted(pairs.items()) if p["eligible"]] == ["a:2", "a:4", "a:7"]
    assert pairs["a:1"]["reason"] == "before the principle was formulated"
    assert pairs["a:3"]["operative"] == "2026-09-10T22:30Z" and not pairs["a:3"]["eligible"]
    assert pairs["a:4"]["operative"] == "2026-10-06T08:18Z"
    assert pairs["a:5"]["reason"].startswith("after the principle was operative")
    flag = pairs["a:2"]["lexical_exposure"]
    assert flag["lines"] == [1] and flag["share"] > 0
    cands = json.loads((tmp_path / "out" / "draft_candidates.json").read_text())["candidates"]
    assert [c["unit"] for c in cands] == ["a:2", "a:4", "a:6"]  # a:7 withheld; a:6 only as a reversal
    assert cands[2]["reasons"] == ["reversal"]


def test_marks_are_required_and_read(tmp_path):
    setup(tmp_path, mark="")
    r = run(tmp_path)
    assert r.returncode == 2 and "P11: no mark" in r.stderr
    r = run(tmp_path, "--provisional")
    assert r.returncode == 0 and "PROVISIONAL" in (tmp_path / "out" / "eligibility.md").read_text()
    setup(tmp_path, mark="ok; memory otra-nota.md; whatever")
    r = run(tmp_path)
    assert r.returncode == 2 and "not among the listed candidates" in r.stderr and "cannot read the mark 'whatever'" in r.stderr


def test_candidates_count_from_their_quote_and_inherit_a_principle_in_force(tmp_path):
    setup(tmp_path, mark="")  # the principles in force unmarked: they only lend operative dates, read as proposed
    (tmp_path / "timeline.jsonl").write_text(json.dumps({"id": "row-1", "time_utc": "2026-09-15T00:00:00Z"}) + "\n")
    (tmp_path / "find.json").write_text(json.dumps({"answer": {"candidates": [
        {"id": "C1", "statement": "Criteria are parameters.", "quote": "nunca hardcodear", "quote_row": "row-1"},
        {"id": "C2", "statement": "Something new.", "quote": "algo", "quote_row": "row-1"}]}}))
    (tmp_path / "match.json").write_text(json.dumps({"answer": {"matches": [
        {"candidate": "C1", "verdict": "extends", "principle": "P11"}, {"candidate": "C2", "verdict": "new", "principle": ""}]}}))
    r = subprocess.run([sys.executable, str(ELIG), "--units", str(tmp_path / "units.jsonl"), "--dates", str(tmp_path / "dates.json"),
                        "--marks", str(tmp_path / "dates.md"), "--timeline", str(tmp_path / "timeline.jsonl"),
                        "--output-dir", str(tmp_path / "out"), "--candidates", str(tmp_path / "find.json"),
                        "--match", str(tmp_path / "match.json")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    pairs = [json.loads(l) for l in (tmp_path / "out" / "eligibility.jsonl").read_text().splitlines()]
    c1 = {p["unit"]: p for p in pairs if p["principle"] == "C1"}
    c2 = {p["unit"]: p for p in pairs if p["principle"] == "C2"}
    assert c1["a:2"]["explicit"] == "2026-09-15T00:00Z" and c1["a:2"]["eligible"]          # after its quote, before P11's CLAUDE.md
    assert c1["a:1"]["reason"] == "before the principle was formulated"                    # 2026-09-10 is before the quote
    assert not c1["a:6"]["eligible"] and c1["a:6"]["operative"] == "2026-10-06T08:18Z"     # inherited from P11
    assert c2["a:6"]["eligible"] and c2["a:6"]["operative"] is None                        # new: never operative
    st = json.loads((tmp_path / "out" / "statements.json").read_text())["candidates"]
    assert st["C1"]["inherits"] == "P11" and st["C2"]["inherits"] is None
