"""scripts/audit_correspondence.py with a stub in place of the claude and codex command lines (step
5.3 of record/plan-working-method-execution-2026-10-06.md). No model is called: the stub is first on
the PATH, answers each stage with canned JSON, and records where and how it was run."""
import hashlib
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "audit_correspondence.py"
PROMPT_FILES = [ROOT / "prompts" / f"audit_correspondence_{n}_v1.md"
                for n in ("common", "map_spec", "map_impl", "map_docs", "verify", "report")]
REAL_UNITS = ROOT / "prompts" / "audit_correspondence_units_v1.json"
DATE = "2026-01-02"
OUT = Path("record/audits") / f"{DATE}_correspondence_v1_opus"
REPORT = Path("record/audits") / f"{DATE}_correspondence_v1_opus.md"

STUB = r'''#!PYTHON
import json, os, re, subprocess, sys, time
from pathlib import Path

args = sys.argv[1:]
name = Path(sys.argv[0]).name
log = Path(os.environ["STUB_LOG"])


def record(entry):
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def opt(flag):
    return args[args.index(flag) + 1] if flag in args else None


if "--version" in args:
    record({"stage": "version", "cli": name})
    print("9.9.9 (stub " + name + ")")
    sys.exit(0)

prompt = sys.stdin.read()
if name == "claude":
    schema, scratch = opt("--json-schema") or "", opt("--add-dir")
else:
    schema, scratch = (Path(opt("--output-schema")).read_text() if opt("--output-schema") else ""), None
if '"verdicts"' in schema:
    stage, unit = "verify", re.search(r'mapper "([^"]+)"', prompt).group(1)
elif schema:
    stage, unit = "map", re.search(r"Your label: ([A-Za-z0-9_-]+)\.", prompt).group(1)
else:
    stage, unit = "report", "report"
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
record({"cli": name, "stage": stage, "unit": unit, "cwd": os.getcwd(), "head": head, "argv": args,
        "pid": os.getpid(), "scratch": scratch, "prompt": prompt,
        "PYTHONPATH": os.environ.get("PYTHONPATH", ""), "LUTHIER_PATH": os.environ.get("LUTHIER_PATH", "")})
if os.environ.get("STUB_SLEEP"):
    time.sleep(float(os.environ["STUB_SLEEP"]))

key = unit + "." + stage
invalid = key in os.environ.get("STUB_FAIL", "").split(",")
if key in os.environ.get("STUB_INVALID_ONCE", "").split(","):
    marker = Path(os.environ["STUB_STATE"]) / key
    if not marker.exists():
        marker.touch()
        invalid = True
mode = dict(kv.split("=", 1) for kv in os.environ.get("STUB_MODE", "").split(",") if "=" in kv).get(key)
if mode in ("grandchild", "lingering"):     # a process the CLI started holds its output open
    child = subprocess.Popen(["sleep", "300"])
    record({"stage": "child", "unit": unit, "pid": child.pid})
    if mode == "grandchild":                # ... and the CLI hangs
        time.sleep(300)
if mode == "write_repo":                    # a call that breaks its rules and writes in the user's tree
    (Path(os.environ["STUB_REPO"]) / "stray.txt").write_text("x\n")
if mode == "error_exit":                    # claude gave up (out of turns), after spending something
    print(json.dumps({"type": "result", "subtype": "error_max_turns", "is_error": True, "total_cost_usd": 0.25,
                      "result": ""}))
    sys.exit(1)


def claim(i, status, severity):
    return {"id": f"{unit}#{i}", "spec_ref": "docs/semantica/00.md:1", "claim": "a claim", "status": status,
            "impl_refs": ["src/luthier/x.py:1"], "test_refs": [], "evidence": "read", "severity": severity}


def behavior(i, status):
    return {"id": f"{unit}#{i}", "impl_ref": "src/luthier/x.py:1", "behavior": "it prints", "spec_ref": "none",
            "status": status, "test_refs": [], "evidence": "read", "severity": "low"}


if stage == "map" and '"claims"' in schema:
    data = {"sections": ["all"], "notes": "", "claims": [
        claim(1, "implemented_tested", "low"), claim(2, "contradicts", "high"),
        claim(3, "spec_open_or_nonnormative", "low")]}
elif stage == "map":
    data = {"sections": ["all"], "notes": "", "behaviors": [behavior(1, "covered"), behavior(2, "not_in_spec")]}
elif stage == "verify":
    ids = re.findall(r'"id": "([^"]+)"', prompt.split("Entries:")[-1])
    data = {"notes": "", "verdicts": [{"id": i, "verdict": "confirmed", "corrected_status": "contradicts",
                                       "corrected_severity": "high", "evidence": "checked"} for i in ids]}
else:
    data = "# A title of its own\n\n## Summary\nStub summary.\n\n## Bites\nNone.\n"
if mode == "empty":
    data["claims" if "claims" in data else "behaviors"] = []

text = data if stage == "report" else json.dumps(data)
if name == "claude":
    if invalid:
        print("this is not json")
        sys.exit(0)
    out = {"type": "result", "subtype": "success", "is_error": False, "total_cost_usd": 0.5,
           "num_turns": 2, "result": text}
    if stage != "report":
        out["structured_output"] = data
    print(json.dumps(out))
else:
    Path(opt("-o")).write_text("not json" if invalid else text)
'''

UNITS = {
    "about": "units of the test",
    "audited_paths": ["src", "docs/semantica"],
    "verify": json.loads(REAL_UNITS.read_text(encoding="utf-8"))["verify"],
    "units": [
        {"label": "spec-a", "direction": "spec", "files": "docs/semantica/00.md"},
        {"label": "impl-b", "direction": "impl", "files": "src/luthier/x.py"},
        {"label": "docs", "direction": "docs", "files": "README.md"},
    ],
}


def load_module():
    spec = importlib.util.spec_from_file_location("audit_correspondence", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module          # its dataclasses look the module up while it loads
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=test", "-c", "user.email=test@example.com",
         "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
        check=True, capture_output=True, text=True).stdout.strip()


def commit(repo: Path, files: dict[str, str], message: str) -> str:
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def make_repo(tmp_path: Path) -> tuple[Path, str]:
    """A repository holding a copy of the script and its prompts, and a small Luthier."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / "scripts").mkdir()
    shutil.copy(SCRIPT, repo / "scripts" / SCRIPT.name)
    (repo / "prompts").mkdir()
    for p in PROMPT_FILES:
        shutil.copy(p, repo / "prompts" / p.name)
    sha = commit(repo, {
        "prompts/audit_correspondence_units_v1.json": json.dumps(UNITS, indent=1),
        "src/luthier/x.py": "x = 1\n",
        "src/luthier/lib/a.lut": "-- a library\n",
        "docs/semantica/00.md": "# Fundamentals\n\nA rule.\n",
        "README.md": "# Luthier\n",
    }, "first")
    bindir = tmp_path / "bin"
    bindir.mkdir()
    for name in ("claude", "codex"):
        (bindir / name).write_text(STUB.replace("PYTHON", sys.executable, 1), encoding="utf-8")
        (bindir / name).chmod(0o755)
    (tmp_path / "tmp").mkdir()
    (tmp_path / "state").mkdir()
    return repo, sha


def env_for(tmp_path: Path, **extra: str) -> dict:
    env = dict(os.environ)
    env.update(PATH=f"{tmp_path / 'bin'}{os.pathsep}{env.get('PATH', '')}", TMPDIR=str(tmp_path / "tmp"),
               STUB_LOG=str(tmp_path / "calls.jsonl"), STUB_STATE=str(tmp_path / "state"))
    env.update(extra)
    return env


def run(tmp_path: Path, *args: str, script: Path | None = None, timeout: float = 120,
        **extra: str) -> subprocess.CompletedProcess:
    script = script or tmp_path / "repo" / "scripts" / SCRIPT.name
    return subprocess.run([sys.executable, str(script), "--cli", "claude", *args], cwd=tmp_path,
                          capture_output=True, text=True, env=env_for(tmp_path, **extra), timeout=timeout)


def start(tmp_path: Path, *args: str, **extra: str) -> subprocess.Popen:
    return subprocess.Popen([sys.executable, str(tmp_path / "repo" / "scripts" / SCRIPT.name), "--cli", "claude",
                             *args], cwd=tmp_path, env=env_for(tmp_path, **extra),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def children(tmp_path: Path) -> list[int]:
    log = tmp_path / "calls.jsonl"
    entries = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
    return [e["pid"] for e in entries if e["stage"] == "child"]


def alive(pids: list[int], wait: float = 10) -> list[int]:
    """The processes of pids still running after at most wait seconds."""
    deadline = time.monotonic() + wait
    while True:
        left = [p for p in pids if Path(f"/proc/{p}").exists()
                and "zombie" not in Path(f"/proc/{p}/status").read_text(errors="replace").lower()]
        if not left or time.monotonic() > deadline:
            return left
        time.sleep(0.1)


def calls(tmp_path: Path) -> list[dict]:
    log = tmp_path / "calls.jsonl"
    if not log.exists():
        return []
    entries = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
    return [e for e in entries if e["stage"] not in ("version", "child")]


def clear_calls(tmp_path: Path) -> None:
    (tmp_path / "calls.jsonl").unlink(missing_ok=True)


def worktrees(repo: Path) -> list[str]:
    return [l for l in git(repo, "worktree", "list", "--porcelain").splitlines() if l.startswith("worktree ")]


def test_full_run_is_pinned_and_writes_outputs_and_report(tmp_path):
    repo, sha = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE)
    assert proc.returncode == 0, proc.stderr
    cs = calls(tmp_path)
    assert sorted((c["stage"], c["unit"]) for c in cs) == sorted(
        [("map", u) for u in ("spec-a", "impl-b", "docs")] + [("verify", u) for u in ("spec-a", "impl-b", "docs")]
        + [("report", "report")])
    # Every call ran in one worktree of the commit, in the temporary directory, not in the repository.
    cwds = {c["cwd"] for c in cs}
    assert len(cwds) == 1
    wt = Path(cwds.pop())
    assert wt.is_relative_to(tmp_path / "tmp") and not wt.is_relative_to(repo)
    assert {c["head"] for c in cs} == {sha}
    assert {c["PYTHONPATH"].split(os.pathsep)[0] for c in cs} == {str(wt / "src")}
    assert {c["LUTHIER_PATH"] for c in cs} == {str(wt / "src" / "luthier" / "lib")}
    # ... and it is gone.
    assert not wt.exists()
    assert len(worktrees(repo)) == 1
    assert list((tmp_path / "tmp").iterdir()) == []
    # Each call has its own scratch folder, where alone it may write; nobody may certify.
    scratches = [c["scratch"] for c in cs]
    assert len(set(scratches)) == len(scratches)
    for c in cs:
        argv = c["argv"]
        assert argv[argv.index("--permission-mode") + 1] == "dontAsk"
        assert argv[argv.index("--setting-sources") + 1] == "project,local"   # not the user's allow rules
        assert not any("certify" in a for a in argv)
        assert f"Write(/{c['scratch']}/**)" in argv
        assert c["scratch"] in c["prompt"] and str(wt) in c["prompt"] and sha in c["prompt"]
    # Outputs.
    out = repo / OUT
    for unit in ("spec-a", "impl-b", "docs"):
        m = json.loads((out / f"{unit}.map.json").read_text())
        v = json.loads((out / f"{unit}.verify.json").read_text())
        assert m["meta"]["commit"] == v["meta"]["commit"] == sha
        assert m["meta"]["model"] == "opus" and m["meta"]["cli_version"] == "9.9.9 (stub claude)"
        assert v["meta"]["entries_without_verdict"] == []
    # The skeptic sees the gaps and the spot-checks, not what the specification leaves open.
    assert json.loads((out / "spec-a.verify.json").read_text())["meta"]["entries"] == ["spec-a#2", "spec-a#1"]
    assert json.loads((out / "impl-b.verify.json").read_text())["meta"]["entries"] == ["impl-b#2", "impl-b#1"]
    verify_prompt = next(c["prompt"] for c in cs if c["stage"] == "verify" and c["unit"] == "spec-a")
    assert "spec-a#3" not in verify_prompt
    # The report: a header by the script, then the model's body from its Summary on.
    report = (repo / REPORT).read_text()
    assert report.startswith("# Correspondence audit of Luthier\n")
    assert f"- Commit audited: `{sha}`" in report
    for p in PROMPT_FILES:
        digest = hashlib.sha256((repo / "prompts" / p.name).read_bytes()).hexdigest()
        assert f"`prompts/{p.name}`, sha256 `{digest}`" in report
    assert "- CLI: `claude`, 9.9.9 (stub claude)" in report
    assert "- Model: `opus`" in report
    assert "- Units run: 3 of 3: spec-a, impl-b, docs" in report
    assert "- Units failed: none" in report
    assert "A title of its own" not in report and "## Summary\nStub summary." in report


def test_a_second_run_skips_and_force_redoes(tmp_path):
    repo, _ = make_repo(tmp_path)
    assert run(tmp_path, "--date", DATE).returncode == 0
    clear_calls(tmp_path)
    proc = run(tmp_path, "--date", DATE)
    assert proc.returncode == 0, proc.stderr
    assert calls(tmp_path) == []
    assert "Nothing to do." in proc.stdout
    proc = run(tmp_path, "--date", DATE, "--force")
    assert proc.returncode == 0, proc.stderr
    assert len(calls(tmp_path)) == 7


def test_commit_pins_the_audit(tmp_path):
    repo, first = make_repo(tmp_path)
    second = commit(repo, {"src/luthier/x.py": "x = 2\n"}, "second")
    assert first != second
    proc = run(tmp_path, "--date", DATE, "--commit", first[:8])
    assert proc.returncode == 0, proc.stderr
    assert {c["head"] for c in calls(tmp_path)} == {first}
    assert f"`{first}`" in (repo / REPORT).read_text()
    assert len(worktrees(repo)) == 1


def test_outputs_of_another_commit_stop_the_run(tmp_path):
    repo, first = make_repo(tmp_path)
    assert run(tmp_path, "--date", DATE).returncode == 0
    commit(repo, {"src/luthier/x.py": "x = 2\n"}, "second")
    clear_calls(tmp_path)
    proc = run(tmp_path, "--date", DATE)
    assert proc.returncode == 2
    assert "made differently" in proc.stderr and "commit" in proc.stderr
    assert calls(tmp_path) == []
    # HEAD moved since the first run (another session committed): the message says how to resume it
    # at its commit, not only how to pay for it again with --force.
    assert f"add --commit {first[:12]}" in proc.stderr
    proc = run(tmp_path, "--date", DATE, "--commit", first[:12])
    assert proc.returncode == 0, proc.stderr
    assert "Nothing to do." in proc.stdout and calls(tmp_path) == []
    # --only doesn't let one unit at the new commit join the others at the old one in one report.
    assert run(tmp_path, "--date", DATE, "--only", "impl-b").returncode == 2
    proc = run(tmp_path, "--date", DATE, "--only", "impl-b", "--force")
    assert proc.returncode == 0, proc.stderr
    report = (repo / REPORT).read_text()
    assert "- Units run: 1 of 3: impl-b" in report and "- Units not run: spec-a, docs" in report
    assert run(tmp_path, "--date", DATE, "--force").returncode == 0
    assert "- Units run: 3 of 3" in (repo / REPORT).read_text()


def test_only_limits_the_units(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, "--only", "impl-b")
    assert proc.returncode == 0, proc.stderr
    assert {(c["stage"], c["unit"]) for c in calls(tmp_path)} == {("map", "impl-b"), ("verify", "impl-b"),
                                                                 ("report", "report")}
    report = (repo / REPORT).read_text()
    assert "- Units run: 1 of 3: impl-b" in report and "- Units not run: spec-a, docs" in report
    assert not (repo / OUT / "spec-a.map.json").exists()
    assert run(tmp_path, "--only", "nope").returncode == 2


def test_dry_run_calls_nothing(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, "--dry-run")
    assert proc.returncode == 0, proc.stderr
    assert not (tmp_path / "calls.jsonl").exists()      # not even --version
    assert not (repo / "record" / "audits").exists()
    assert len([l for l in proc.stdout.splitlines() if l.startswith("[dry] map ")]) == 3
    assert len(worktrees(repo)) == 1


def test_an_invalid_answer_is_retried_and_a_failing_unit_does_not_stop_the_others(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, STUB_INVALID_ONCE="spec-a.map", STUB_FAIL="impl-b.map")
    assert proc.returncode == 1
    cs = calls(tmp_path)
    assert len([c for c in cs if (c["stage"], c["unit"]) == ("map", "spec-a")]) == 2
    assert len([c for c in cs if (c["stage"], c["unit"]) == ("map", "impl-b")]) == 2
    assert not any(c["stage"] == "verify" and c["unit"] == "impl-b" for c in cs)
    out = repo / OUT
    assert json.loads((out / "spec-a.map.json").read_text())["meta"]["attempts"] == 2
    assert (out / "docs.verify.json").exists()
    assert not (out / "impl-b.map.json").exists()
    assert "this is not json" in (out / "impl-b.map.error.txt").read_text()
    report = (repo / REPORT).read_text()
    assert "- Units failed: impl-b" in report and "- Units run: 2 of 3: spec-a, docs" in report
    report_prompt = next(c["prompt"] for c in cs if c["stage"] == "report")
    assert 'Units that returned nothing: ["impl-b"]' in report_prompt
    # Running it again resumes: only the failed unit, then the report.
    clear_calls(tmp_path)
    proc = run(tmp_path, "--date", DATE)
    assert proc.returncode == 0, proc.stderr
    assert {(c["stage"], c["unit"]) for c in calls(tmp_path)} == {("map", "impl-b"), ("verify", "impl-b"),
                                                                 ("report", "report")}
    assert not (out / "impl-b.map.error.txt").exists()
    assert "- Units failed: none" in (repo / REPORT).read_text()


def test_codex_is_the_alternative(tmp_path):
    repo, sha = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, "--cli", "codex")
    assert proc.returncode == 0, proc.stderr
    cs = calls(tmp_path)
    assert len(cs) == 7 and {c["cli"] for c in cs} == {"codex"} and {c["head"] for c in cs} == {sha}
    wt = cs[0]["cwd"]
    assert all(c["argv"][c["argv"].index("-C") + 1] == wt for c in cs)
    assert (repo / "record" / "audits" / f"{DATE}_correspondence_v1_gpt-5-4.md").exists()


def test_ctrl_c_removes_the_worktree_and_stops_the_calls(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = subprocess.Popen([sys.executable, str(repo / "scripts" / SCRIPT.name), "--cli", "claude", "--date", DATE],
                            cwd=tmp_path, env=env_for(tmp_path, STUB_SLEEP="60"),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    deadline = time.monotonic() + 30
    while len(calls(tmp_path)) < 3 and time.monotonic() < deadline:
        time.sleep(0.1)
    cs = calls(tmp_path)
    assert len(cs) == 3
    proc.send_signal(signal.SIGINT)
    _, err = proc.communicate(timeout=60)
    assert proc.returncode == 130, err
    assert not Path(cs[0]["cwd"]).exists()
    assert len(worktrees(repo)) == 1
    deadline = time.monotonic() + 10
    alive = [c["pid"] for c in cs]
    while alive and time.monotonic() < deadline:
        alive = [p for p in alive if Path(f"/proc/{p}").exists()
                 and "zombie" not in Path(f"/proc/{p}/status").read_text(errors="replace").lower()]
        time.sleep(0.1)
    assert alive == []


def test_usage_errors(tmp_path):
    repo, _ = make_repo(tmp_path)
    assert run(tmp_path, "--commit", "deadbeef").returncode == 2
    assert run(tmp_path, "--jobs", "0").returncode == 2
    assert run(tmp_path, "--date", "today").returncode == 2
    assert calls(tmp_path) == []


def test_uncommitted_changes_are_warned_about(tmp_path):
    repo, _ = make_repo(tmp_path)
    (repo / "src" / "luthier" / "x.py").write_text("x = 3\n")
    proc = run(tmp_path, "--date", DATE, "--dry-run")
    assert proc.returncode == 0
    assert "WARNING: uncommitted changes" in proc.stderr and "src/luthier/x.py" in proc.stderr


def test_validator():
    m = load_module()
    good = {"verdicts": [{"id": "a", "verdict": "confirmed", "corrected_status": "x",
                          "corrected_severity": "low", "evidence": "e"}], "notes": ""}
    assert m.validate(good, m.SCHEMAS["verdicts"]) == []
    bad = {"verdicts": [{"id": "a", "verdict": "sure", "corrected_status": "x", "evidence": 3, "extra": 1}]}
    errors = m.validate(bad, m.SCHEMAS["verdicts"])
    assert any("notes" in e for e in errors)
    assert any("'sure'" in e for e in errors)
    assert any("corrected_severity" in e for e in errors)
    assert any("evidence" in e and "string" in e for e in errors)
    assert any("extra" in e for e in errors)
    assert m.validate([], m.SCHEMAS["claims"]) == ["$: expected object, got list"]


def test_the_real_units_and_prompts():
    m = load_module()
    cfg = m.load_units(REAL_UNITS)
    assert [u["label"] for u in cfg["units"]] == [
        "spec-00-01", "spec-02-03", "spec-04", "spec-05", "spec-06", "spec-07", "spec-08",
        "impl-checker", "impl-eval", "impl-front", "impl-tools", "docs"]
    prompts = m.load_prompts("v1")
    assert set(prompts) == set(m.PROMPT_NAMES)
    # Not only the worktree: the model can find the repository it was checked out from.
    assert "Write nothing outside {scratch}/" in prompts["common"].text
    assert "in the repository it was checked out from" in prompts["common"].text
    # The README shows "pip install -e .": run in the worktree, it would point Luciano's install at a
    # folder that is then removed.
    assert '"pip install"' in prompts["map_docs"].text
    for p in list(prompts.values()) + [REAL_UNITS]:
        text = p.text if hasattr(p, "text") else p.read_text(encoding="utf-8")
        assert "\u2014" not in text


def test_dry_run_on_this_repository_lists_the_twelve_units(tmp_path):
    make_repo(tmp_path)          # for the stub on the PATH; the script and the commit are this repository's
    out = tmp_path / "out"
    proc = run(tmp_path, "--dry-run", "--out-dir", str(out), script=SCRIPT)
    assert proc.returncode == 0, proc.stderr
    assert len([l for l in proc.stdout.splitlines() if l.startswith("[dry] map ")]) == 12
    assert len([l for l in proc.stdout.splitlines() if l.startswith("[dry] verify ")]) == 12
    assert not (tmp_path / "calls.jsonl").exists()
    assert not out.exists()


# ----------------------------------------------------------------------------------------------
# Found by an adversarial check of the script.

def test_a_timeout_kills_the_call_and_what_it_started(tmp_path):
    """A process the CLI started holds its output open and the CLI hangs: the timeout must still
    end the call (it used to wait for that output forever), and kill that process too."""
    repo, _ = make_repo(tmp_path)
    started = time.monotonic()
    proc = run(tmp_path, "--date", DATE, "--only", "spec-a", "--timeout", "1", timeout=60,
               STUB_MODE="spec-a.map=grandchild")
    assert proc.returncode == 1, proc.stderr
    assert time.monotonic() - started < 40
    assert (repo / OUT / "spec-a.map.error.txt").read_text().count("timed out after 1 s") == 2
    assert len(children(tmp_path)) == 2 and alive(children(tmp_path)) == []
    assert len(worktrees(repo)) == 1


def test_a_call_that_ends_while_its_child_holds_the_output_is_kept(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, "--only", "spec-a", "--timeout", "30", "--no-report", timeout=60,
               STUB_MODE="spec-a.map=lingering")
    assert proc.returncode == 0, proc.stderr
    assert json.loads((repo / OUT / "spec-a.map.json").read_text())["meta"]["attempts"] == 1
    assert alive(children(tmp_path)) == []


def test_sighup_stops_the_run_like_ctrl_c(tmp_path):
    """The terminal closed: the calls are killed and the worktree removed; the message gives the date
    to resume on another day."""
    repo, _ = make_repo(tmp_path)
    proc = start(tmp_path, STUB_SLEEP="60")
    deadline = time.monotonic() + 30
    while len(calls(tmp_path)) < 3 and time.monotonic() < deadline:
        time.sleep(0.1)
    cs = calls(tmp_path)
    assert len(cs) == 3
    proc.send_signal(signal.SIGHUP)
    _, err = proc.communicate(timeout=60)
    assert proc.returncode == 130, err
    assert not Path(cs[0]["cwd"]).exists() and len(worktrees(repo)) == 1
    assert alive([c["pid"] for c in cs]) == []
    import datetime
    assert f"add --date {datetime.date.today().isoformat()}" in err


def test_two_runs_at_once_do_not_both_pay(tmp_path):
    repo, _ = make_repo(tmp_path)
    first = start(tmp_path, "--date", DATE, STUB_SLEEP="2")
    deadline = time.monotonic() + 30
    while not calls(tmp_path) and time.monotonic() < deadline:
        time.sleep(0.1)
    second = run(tmp_path, "--date", DATE)
    assert second.returncode == 2 and "another run is writing" in second.stderr
    _, err = first.communicate(timeout=120)
    assert first.returncode == 0, err
    cs = calls(tmp_path)
    assert len(cs) == 7 and len({c["cwd"] for c in cs}) == 1
    assert not [p for p in (repo / OUT).iterdir() if p.name.endswith(".tmp")]


def test_a_typo_in_the_units_file_stops_the_run(tmp_path):
    repo, _ = make_repo(tmp_path)
    good = json.loads((repo / "prompts" / "audit_correspondence_units_v1.json").read_text())

    def units_with(change) -> str:
        cfg = json.loads(json.dumps(good))
        changed = change(cfg)
        path = tmp_path / "units.json"
        path.write_text(json.dumps(cfg if changed is None else changed))
        return str(path)

    typos = {
        "a list": lambda c: [],
        "verify as a list": lambda c: c.update(verify=[]),
        "audited_path": lambda c: c.update(audited_path=c.pop("audited_paths")),
        "a unit key": lambda c: c["units"][0].update(lable="x"),
        "an excluded status": lambda c: c["verify"]["claims"].update(
            exclude_statuses=["implemented_test", "spec_open_or_nonnormative"]),
        "the spot-check status": lambda c: c["verify"]["behaviors"].update(spot_check_status="coverd"),
        "spot_checks true": lambda c: c["verify"]["claims"].update(spot_checks=True),
        "spot_checks negative": lambda c: c["verify"]["claims"].update(spot_checks=-1),
        "audited_paths a string": lambda c: c.update(audited_paths="src"),
    }
    for name, change in typos.items():
        proc = run(tmp_path, "--date", DATE, "--units", units_with(change))
        assert proc.returncode == 2, (name, proc.stderr)
        assert proc.stderr.startswith("ERROR: ") and "Traceback" not in proc.stderr, (name, proc.stderr)
    assert calls(tmp_path) == []
    proc = run(tmp_path, "--date", DATE, "--dry-run", "--units", units_with(lambda c: c.update(audited_paths=["srcc"])))
    assert proc.returncode == 0 and "WARNING: audited_paths not in commit" in proc.stderr and "srcc" in proc.stderr


def test_a_spot_check_is_not_sent_twice():
    m = load_module()
    from types import SimpleNamespace
    ctx = SimpleNamespace(cfg={"verify": {"claims": {"exclude_statuses": ["spec_open_or_nonnormative"],
                                                     "spot_check_status": "implemented_tested", "spot_checks": 4}}})
    output = {"claims": [{"id": "a", "status": "implemented_tested"}, {"id": "b", "status": "contradicts"}]}
    entries = m.select_entries(ctx, {"direction": "spec"}, output)
    assert [e["id"] for e in entries] == ["a", "b"]


def test_an_empty_map_is_named_in_the_report_header(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, STUB_MODE="spec-a.map=empty")
    assert proc.returncode == 0, proc.stderr
    assert "the map found no claims" in proc.stderr
    assert "- Units whose map found nothing (a map that finds nothing has probably failed): spec-a" in \
        (repo / REPORT).read_text()


def test_the_cost_of_a_failed_call_is_in_its_error_file(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, "--only", "spec-a", "--no-report", STUB_MODE="spec-a.map=error_exit")
    assert proc.returncode == 1
    assert "cost reported by the CLI: 0.5 USD" in (repo / OUT / "spec-a.map.error.txt").read_text()


def test_a_change_to_the_tree_during_the_run_is_reported(tmp_path):
    repo, _ = make_repo(tmp_path)
    proc = run(tmp_path, "--date", DATE, STUB_MODE="spec-a.map=write_repo", STUB_REPO=str(repo))
    assert proc.returncode == 1
    assert "tree changed during the run" in proc.stderr and "stray.txt" in proc.stderr
    assert "stray.txt" in (repo / REPORT).read_text()
    clear_calls(tmp_path)
    (repo / "stray.txt").unlink()
    assert run(tmp_path, "--date", DATE, "--force").returncode == 0     # a clean run says nothing


def test_luthier_test_and_run_are_allowed_only_in_scratch(tmp_path):
    make_repo(tmp_path)
    assert run(tmp_path, "--date", DATE, "--only", "spec-a", "--no-report").returncode == 0
    for c in calls(tmp_path):
        rules = c["argv"][c["argv"].index("--allowedTools") + 1:]
        assert "Bash(luthier test *)" not in rules and "Bash(luthier run *)" not in rules
        assert f"Bash(luthier test {c['scratch']}/*)" in rules

