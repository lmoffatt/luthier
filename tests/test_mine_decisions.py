"""scripts/mine_decisions.py on a small transcript: what counts as a turn of Luciano's, what counts
as an action, how a commit is found and its files read from git, events repeated across files,
and the withholding of private words. No model is called."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MINE = ROOT / "scripts" / "mine_decisions.py"


def ev(n, kind, content, **kw):
    return {"type": kind, "uuid": f"u{n}", "timestamp": f"2026-10-01T10:{n:02d}:00Z", "sessionId": "abcdef12-0000",
            "message": {"role": kind, "content": content}, **kw}


def tool(name, tid, **inp):
    return {"type": "tool_use", "id": tid, "name": name, "input": inp}


def result(tid, text):
    return [{"type": "tool_result", "tool_use_id": tid, "content": text}]


def make_repo(tmp: Path) -> tuple[Path, str]:
    repo = tmp / "repo"
    (repo / "docs" / "spec").mkdir(parents=True)
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout
    git("init", "-q"); git("config", "user.email", "t@t"); git("config", "user.name", "t")
    (repo / "docs" / "spec" / "05.md").write_text("R1\n")
    (repo / "record").mkdir()
    (repo / "record" / "decisions.md").write_text("D\n")
    git("add", "."); git("commit", "-q", "-m", "R1 added")
    return repo, git("rev-parse", "--short", "HEAD").strip()


def transcript(h: str) -> list[dict]:
    return [
        {"type": "queue-operation", "timestamp": "2026-10-01T10:00:00Z", "sessionId": "abcdef12-0000"},
        ev(1, "user", "quiero que las reglas de la spec tengan identificadores"),
        ev(2, "assistant", [{"type": "text", "text": "Propongo R1 a R9 en 05."},
                             tool("Edit", "t1", file_path="/home/x/luthier/docs/spec/05.md")]),
        ev(3, "user", result("t1", "ok")),
        ev(4, "user", [{"type": "text", "text": "<task-notification>done</task-notification>"}]),
        ev(5, "assistant", [{"type": "text", "text": "¿Commiteo?"}]),
        ev(6, "user", "dale"),
        ev(7, "assistant", [tool("Bash", "t2", command="git add . && git commit -q -m 'R1' && git log --oneline -1")]),
        ev(8, "user", result("t2", f"{h} R1 added")),
        ev(9, "user", "mirá el archivo de databaum"),
        ev(10, "assistant", [tool("Bash", "t3", command="cat > /home/x/luthier/record/notes.md <<'EOF'\nx\nEOF")]),
        ev(11, "user", "y esto qué es?"),
        ev(12, "assistant", [tool("Read", "t4", file_path="/home/x/luthier/README.md"),
                              tool("Bash", "t5", command="ls /home/x 2>/dev/null > /tmp/list.txt")]),
        ev(13, "user", "ok"),
        ev(14, "assistant", [tool("Write", "t6", file_path="/tmp/claude-1000/x/scratchpad/a.py")]),
    ]


def test_units_actions_commits_and_withholding(tmp_path):
    repo, h = make_repo(tmp_path)
    tdir = tmp_path / "t"
    tdir.mkdir()
    lines = transcript(h)
    (tdir / "abcdef12-0000.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    # a resumed session repeats the first events; they count once
    (tdir / "abcdef12-0001.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines[:4]))
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(MINE), "--transcripts", str(tdir), "--output-dir", str(out),
                        "--repos", str(repo), "--projects", "luthier"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rows = [json.loads(l) for l in (out / "decision_units.jsonl").read_text().splitlines()]
    assert [x["luciano"]["line"] for x in rows] == [2, 7, 10]  # the read-only turn and the scratch write are not units
    a, b, c = rows
    assert a["luciano"]["text"] == "quiero que las reglas de la spec tengan identificadores" and a["form"] == "long"
    assert a["areas"] == ["language"] and a["proposal"] is None
    assert b["luciano"]["text"] == "dale" and b["form"] == "short" and b["heuristic_confirmation"] is True
    assert b["proposal"]["text"] == "¿Commiteo?"
    assert b["commits"][0]["hash"] == h and set(b["commits"][0]["files"]) == {"docs/spec/05.md", "record/decisions.md"}
    assert b["areas"] == ["language", "method"]
    assert c["withheld"] == "private words (1)" and c["luciano"]["text"] == "[withheld]"
    assert c["files"] == ["/home/x/luthier/record/notes.md"] and c["areas"] == ["method"]
    md = (out / "decision_units.md").read_text()
    assert "Units: 3; with a commit 1; withheld 1; reversals 0 " in md and "databaum" not in md


def test_a_later_commit_that_removes_added_lines_is_a_reversal(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout
    git("init", "-q"); git("config", "user.email", "t@t"); git("config", "user.name", "t")
    (repo / "docs" / "a.md").write_text("intro line\n")
    git("add", "."); git("commit", "-q", "-m", "base")
    (repo / "docs" / "a.md").write_text("intro line\nrule one says this\nrule two says that\nrule three says more\n")
    git("add", "."); git("commit", "-q", "-m", "rules in")
    h1 = git("rev-parse", "--short", "HEAD").strip()
    (repo / "docs" / "a.md").write_text("intro line\nthe rules were dropped\n")
    git("add", "."); git("commit", "-q", "-m", "rules out")
    h2 = git("rev-parse", "--short", "HEAD").strip()
    lines = [
        ev(1, "user", "ponemos las tres reglas en el documento"),
        ev(2, "assistant", [tool("Bash", "t1", command="git commit -q -m 'rules in' && git log --oneline -1")]),
        ev(3, "user", result("t1", f"{h1} rules in")),
        ev(4, "user", "mejor sacamos las reglas, no sirven"),
        ev(5, "assistant", [tool("Bash", "t2", command="git commit -q -m 'rules out' && git log --oneline -1")]),
        ev(6, "user", result("t2", f"{h2} rules out")),
    ]
    tdir = tmp_path / "t"
    tdir.mkdir()
    (tdir / "abcdef12-0000.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, str(MINE), "--transcripts", str(tdir), "--output-dir", str(out),
                        "--repos", str(repo), "--projects", "luthier"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    a, b = [json.loads(l) for l in (out / "decision_units.jsonl").read_text().splitlines()]
    assert a["reversed_by"] == [{"unit": b["id"], "commit": h2, "lines": 3}]
    assert b["reverses"] == [{"unit": a["id"], "commit": h1, "lines": 3}]
    assert "reversals 1 " in (out / "decision_units.md").read_text()


def test_files_under_an_account_folder_are_written_with_its_number():
    import importlib.util
    spec = importlib.util.spec_from_file_location("mine_decisions", MINE)
    md = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(md)
    home = Path.home()
    assert md.label_path(f"{home}/.claude-databaum/projects/P/memory/n.md") == "[account 2]/projects/P/memory/n.md"
    assert md.label_path(f"{home}/.claude/projects/P/memory/n.md") == "[account 1]/projects/P/memory/n.md"
    assert md.label_path("/home/x/luthier/docs/a.md") == "/home/x/luthier/docs/a.md"
    assert md.account_of(home / ".claude-databaum" / "projects" / "P" / "s.jsonl", {}) == 2
    pinned = md.IACHAT / "raw" / "claude-code" / "d" / "P" / "s.x.jsonl.gz"
    assert md.account_of(pinned, {"raw/claude-code/d/P/s.x.jsonl.gz": f"{home}/.claude/projects/P/s.jsonl"}) == 1
