"""scripts/principle_dates.py: the files a command writes (with a preceding cd), the writes found in
transcripts of several accounts, the time of a chat source, the first commit carrying a principle's
id, and UTC conversion. No model is called."""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("principle_dates", ROOT / "scripts" / "principle_dates.py")
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)


def test_bash_targets_resolve_a_preceding_cd_and_ignore_reads():
    t = pd.bash_targets("cd /home/x/.claude/projects/P/memory/ && cat > nota.md <<'EOF'\nx\nEOF")
    assert t == ["/home/x/.claude/projects/P/memory/nota.md"]
    assert pd.bash_targets("cat /home/x/a.md 2>/dev/null; ls ~/.claude/CLAUDE.md") == []
    assert pd.bash_targets("echo x >> /home/x/b.md && echo y | tee -a /home/x/c.md") == ["/home/x/b.md", "/home/x/c.md"]
    assert pd.bash_targets('cat > $M/note.md <<EOF') == []  # an unresolved variable is not guessed


def test_writes_across_accounts_and_chat_time(tmp_path):
    folder = "-home-x-Projects-sono"
    for acct, name, lines in (
        ("a", "s1aaaaaa-1", [
            {"type": "user", "timestamp": "2026-09-10T22:20:00Z", "message": {"content": "nunca hardcodear"}},
            {"type": "assistant", "timestamp": "2026-09-10T22:30:00Z", "message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": f"cd /h/{folder}/memory/ && cat > nunca.md <<'EOF'\nEvery criterion is a parameter\nEOF"}}]}},
            {"type": "assistant", "timestamp": "2026-09-11T10:00:00Z", "message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": f"cat /h/{folder}/memory/nunca.md"}}]}}]),
        ("b", "s2bbbbbb-2", [
            {"type": "assistant", "timestamp": "2026-10-01T12:00:00+08:00", "message": {"content": [
                {"type": "tool_use", "name": "Write", "input": {"file_path": f"/h/{folder}/memory/otra.md", "content": "x"}}]}}])):
        d = tmp_path / acct / "projects" / folder
        d.mkdir(parents=True)
        (d / f"{name}.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))
    accounts = [tmp_path / "a", tmp_path / "b"]
    w = pd.writes(accounts, re.compile(re.escape(folder) + r"/memory/[\w.-]+\.md"), prefilter=f"{folder}/memory")
    assert [(x["time"], Path(x["file"]).name, x["source"]) for x in w] == [
        ("2026-09-10T22:30Z", "nunca.md", "chat:s1aaaaaa:2"), ("2026-10-01T04:00Z", "otra.md", "chat:s2bbbbbb:1")]
    assert pd.chat_time("chat:s1aaaaaa:1", accounts)[0] == "2026-09-10T22:20Z"
    assert pd.chat_time("chat:s1aaaaaa:9", accounts)[0] == ""
    assert pd.chat_time("chat:ffffffff:1", accounts)[1].startswith("no transcript")


def test_first_commit_with_an_id(tmp_path):
    repo = tmp_path / "r"
    repo.mkdir()
    g = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True)
    g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t")
    (repo / "CLAUDE.md").write_text("# rules\n")
    g("add", "."); g("commit", "-q", "-m", "first")
    (repo / "CLAUDE.md").write_text("# rules\n- P11 Every criterion is a parameter.\n")
    g("add", "."); g("commit", "-q", "-m", "P11 in")
    t, src = pd.first_commit_with(repo, "- P11 ", ["CLAUDE.md"])
    assert t.endswith("Z") and src.startswith("r@")
    assert pd.first_commit_with(repo, "- P12 ", ["CLAUDE.md"]) == ("", "")
    assert pd.utc("2026-10-06T16:18:31+08:00") == "2026-10-06T08:18Z"
