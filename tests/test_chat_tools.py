"""scripts/select_chats.py and scripts/extract_chat_ideas.py with stubs in place of `iachat` and
of the `claude` command line. No model is called and the real archive is not read: the stub
archive answers `fetch --dry-run` and `show --path` with canned threads, and the stub `claude`
answers from the prompt it receives, recording each call."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SELECT = ROOT / "scripts" / "select_chats.py"
EXTRACT = ROOT / "scripts" / "extract_chat_ideas.py"

THREAD_A = """---
source: claude-code
account:
id: aaaaaaaa-1111-2222-3333-444444444444
title: "quiero empezar a definir la semantica de luthier"
started: 2026-09-28T23:56:04Z
ended: 2026-09-30T12:24:49Z
turns: 4
cwd: {cwd}
---

# quiero empezar a definir la semantica de luthier

## 1. Luciano  2026-09-28 23:56:04 UTC  (line 1)

quiero empezar a definir la semantica de luthier.

## 2. Model  2026-09-28 23:56:12 UTC  (lines 19, 38)

{model_long}

## 3. Tool  2026-09-28 23:57:00 UTC

[tool output: 12 files read]

## 4. Luciano  2026-09-29 07:20:11 UTC  (line 50)

porque necesitamos el simbolo para el hueco?
"""

THREAD_B = """---
source: gemini
account:
id: 20260626T0607
title: "Https://www.youtube.com/live/x"
started: 2026-06-26T06:07:00Z
ended: 2026-06-26T06:30:00Z
turns: 2
cwd:
---

# Https://www.youtube.com/live/x

## 1. Luciano  2026-06-26 06:07:00 UTC

mira este video, y de paso decime si sirve para luthier

## 2. Model  2026-06-26 06:07:30 UTC

El video trata de otra cosa.
"""

IACHAT_STUB = r'''#!PYTHON
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
if args[0] == "fetch":
    assert "--dry-run" in args and "--query" in args, args
    print("would copy  claude-code:-:aaaaaaaa-1111-2222-3333-444444444444  quiero empezar a definir la semantica de luthier  -> claude-code/a.md")
    print("would copy  gemini:-:20260626T0607  Https://www.youtube.com/live/x  -> gemini/b.md")
    print("withheld  claude-code:-:cccccccc-1111-2222-3333-444444444444  lee los audios de hoy  (private words: secretword)")
    print("would copy  claude-code:-:dddddddd-1111-2222-3333-444444444444  lee los audios de macro  -> claude-code/d.md")
    print("3 to copy, 1 withheld; target repository /x has a remote")
elif args[0] == "show":
    assert args[-1] == "--path"
    key = args[1]
    name = {"claude-code:-:aaaaaaaa-1111-2222-3333-444444444444": "a.md",
            "gemini:-:20260626T0607": "b.md",
            "claude-code:-:cccccccc-1111-2222-3333-444444444444": "c.md",
            "claude-code:-:dddddddd-1111-2222-3333-444444444444": "d.md"}[key]
    print(root / "archive" / name)
else:
    sys.exit("unknown " + args[0])
'''

CLAUDE_STUB = r'''#!PYTHON
import json, os, sys
from pathlib import Path
prompt = sys.stdin.read()
log = Path(os.environ["STUB_LOG"])
with log.open("a", encoding="utf-8") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "prompt": prompt}) + "\n")
if "select_chats_v1" in prompt:
    if "youtube" in prompt:
        print('{"verdict": "no", "reason": "a video about something else", "turns": [], "topics": []}')
    else:
        print('{"verdict": "partial", "reason": "some turns", "turns": [1, 4, 99], "topics": ["types"]}')
else:
    win = [l for l in prompt.splitlines() if l.startswith("window:")]
    print("---\ngenerated_by: x\n---\n\n## Ideas\n\n### idea-" + (win[0].split()[1] if win else "0")
          + "\n- **Who**: Luciano\n- **Turn**: 1, 2026-09-28 23:56:04 UTC\n- **Kind**: idea\n- **What**: x\n- **Quote**: \"y\"\n")
'''


def make_env(tmp_path: Path) -> dict:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    stub = bin_dir / "claude"
    if not stub.exists():
        stub.write_text(CLAUDE_STUB.replace("PYTHON", sys.executable), encoding="utf-8")
        stub.chmod(0o755)
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env.get('PATH', '')}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    return env


def make_archive(tmp_path: Path, cwd: str = "-home-lmoffatt-Projects-luthier") -> Path:
    root = tmp_path / "IA_chat"
    (root / "tools").mkdir(parents=True)
    (root / "archive").mkdir()
    tool = root / "tools" / "iachat.py"
    tool.write_text(IACHAT_STUB.replace("PYTHON", sys.executable), encoding="utf-8")
    (root / "archive" / "a.md").write_text(THREAD_A.format(cwd=cwd, model_long="x" * 2000), encoding="utf-8")
    (root / "archive" / "b.md").write_text(THREAD_B, encoding="utf-8")
    (root / "archive" / "c.md").write_text(THREAD_A.format(cwd="", model_long="private").replace("aaaaaaaa", "cccccccc"), encoding="utf-8")
    (root / "archive" / "d.md").write_text(THREAD_B.replace("20260626T0607", "dddddddd-1111-2222-3333-444444444444")
                                           .replace("gemini", "claude-code").replace(", y de paso decime si sirve para luthier", "")
                                           .replace("El video trata de otra cosa.", "Luthier is a language (said by the model only)."), encoding="utf-8")
    return root


def calls(tmp_path: Path) -> list[dict]:
    p = tmp_path / "calls.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def run(script: Path, tmp_path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True,
                          env=make_env(tmp_path), cwd=tmp_path)


# --- select_chats -------------------------------------------------------------------------------

def test_select_judges_with_the_model_and_by_cwd_and_reports_withheld(tmp_path):
    root = make_archive(tmp_path)
    out = tmp_path / "sel"
    r = run(SELECT, tmp_path, "--iachat", str(root), "--output-dir", str(out), "--date", "2026-01-02",
            "--cli", "claude", "--to", str(tmp_path / "raw"))
    assert r.returncode == 0, r.stderr
    rows = {json.loads(l)["key"]: json.loads(l) for l in (out / "2026-01-02_select_chats_v1_claude-code_opus.jsonl").read_text().splitlines()}
    assert rows["claude-code:-:aaaaaaaa-1111-2222-3333-444444444444"]["verdict"] == "yes"
    assert rows["claude-code:-:aaaaaaaa-1111-2222-3333-444444444444"]["judged_by"] == "rule"
    assert rows["claude-code:-:aaaaaaaa-1111-2222-3333-444444444444"]["turns"] == [1, 4]
    assert rows["gemini:-:20260626T0607"]["verdict"] == "no"
    c = rows["claude-code:-:cccccccc-1111-2222-3333-444444444444"]
    assert c["verdict"] == "partial" and c["withheld"].startswith("private words") and c["turns"] == [1, 4]
    d = rows["claude-code:-:dddddddd-1111-2222-3333-444444444444"]
    assert d["verdict"] == "no" and d["judged_by"] == "rule" and "0 times" in d["reason"]
    assert all("thread_sha256" in r and "prompt_sha256" in r for r in rows.values())
    cs = calls(tmp_path)
    assert len(cs) == 2  # neither the cwd thread nor the one where Luciano never says luthier went to the model
    assert "a video about something else" in r.stdout  # the reason is printed as it is made
    assert "x" * 601 not in cs[0]["prompt"] + cs[1]["prompt"]  # model turns are cut
    assert "[tool output" not in cs[0]["prompt"] + cs[1]["prompt"]
    md = (out / "2026-01-02_select_chats_v1_claude-code_opus.md").read_text()
    assert "iachat fetch --ids claude-code:-:aaaaaaaa-1111-2222-3333-444444444444 --to" in md
    assert "cccccccc" in md.split("## Judged relevant but withheld")[1]


def test_select_is_idempotent_and_no_cwd_rule_asks_the_model(tmp_path):
    root = make_archive(tmp_path)
    out = tmp_path / "sel"
    common = ["--iachat", str(root), "--output-dir", str(out), "--date", "2026-01-02", "--cli", "claude",
              "--to", str(tmp_path / "raw")]
    assert run(SELECT, tmp_path, *common).returncode == 0
    n = len(calls(tmp_path))
    r = run(SELECT, tmp_path, *common)
    assert r.returncode == 0 and len(calls(tmp_path)) == n
    assert "already judged: 4" in r.stdout
    r = run(SELECT, tmp_path, *common, "--force", "--no-cwd-rule", "--min-mentions", "0")
    assert r.returncode == 0 and len(calls(tmp_path)) == n + 4


def test_select_dry_run_calls_nothing(tmp_path):
    root = make_archive(tmp_path)
    r = run(SELECT, tmp_path, "--iachat", str(root), "--output-dir", str(tmp_path / "sel"), "--dry-run",
            "--to", str(tmp_path / "raw"))
    assert r.returncode == 0 and "candidates: 4" in r.stdout and calls(tmp_path) == []
    assert not (tmp_path / "sel").exists()


# --- extract_chat_ideas -------------------------------------------------------------------------

def test_extract_writes_one_file_per_thread_with_windows_and_frontmatter(tmp_path):
    raw = tmp_path / "raw" / "claude-code"
    raw.mkdir(parents=True)
    (raw / "2026-09-28_aaaaaaaa_x.md").write_text(THREAD_A.format(cwd="", model_long="m" * 3000), encoding="utf-8")
    (tmp_path / "raw" / "manifest.jsonl").write_text("{}\n")
    out = tmp_path / "ideas"
    r = run(EXTRACT, tmp_path, str(tmp_path / "raw"), "--output-dir", str(out), "--cli", "claude",
            "--window-chars", "3200")
    assert r.returncode == 0, r.stderr
    files = list(out.glob("*.md"))
    assert [f.name for f in files] == ["claude-code_2026-09-28_aaaaaaaa_extract_ideas_dialogue_v1_claude-code_opus_ideas.md"]
    text = files[0].read_text()
    head = text.split("---")[1]
    assert "windows: 2" in head and "turns: 4" in head and "ideas: 2" in head
    assert "thread_sha256:" in head and "prompt_sha256:" in head and "generated_by: extract_ideas_dialogue_v1" in head
    assert "## Window 1 of 2: turns 1 to 2" in text and "## Window 2 of 2: turns 4 to 4" in text
    cs = calls(tmp_path)
    assert len(cs) == 2
    assert "## 3. Tool" not in cs[0]["prompt"] + cs[1]["prompt"]
    assert "window: 1 of 2; turns 1 to 2 of 4" in cs[0]["prompt"]
    assert "window: 2 of 2; turns 4 to 4 of 4" in cs[1]["prompt"]


def test_extract_skips_done_threads_and_dry_run_calls_nothing(tmp_path):
    raw = tmp_path / "raw" / "gemini"
    raw.mkdir(parents=True)
    (raw / "b.md").write_text(THREAD_B, encoding="utf-8")
    out = tmp_path / "ideas"
    r = run(EXTRACT, tmp_path, str(tmp_path / "raw"), "--output-dir", str(out), "--dry-run")
    assert r.returncode == 0 and calls(tmp_path) == [] and "pending: 1" in r.stdout
    r = run(EXTRACT, tmp_path, str(tmp_path / "raw"), "--output-dir", str(out), "--cli", "claude")
    assert r.returncode == 0 and len(calls(tmp_path)) == 1
    assert (out / "gemini_2026-06-26_20260626_extract_ideas_dialogue_v1_claude-code_opus_ideas.md").exists()
    r = run(EXTRACT, tmp_path, str(tmp_path / "raw"), "--output-dir", str(out), "--cli", "claude")
    assert r.returncode == 0 and len(calls(tmp_path)) == 1 and "done: 1 | pending: 0" in r.stdout
    r = run(EXTRACT, tmp_path, str(tmp_path / "raw"), "--output-dir", str(out), "--cli", "claude", "--force")
    assert r.returncode == 0 and len(calls(tmp_path)) == 2
