#!/usr/bin/env python3
"""Correspondence audit of Luthier: is the specification (docs/semantica/) a faithful reflection of
the implementation (src/luthier/) and of the documentation (README.md, examples/)?

Step 5.3 of record/plan-working-method-execution-2026-10-06.md. Luciano runs it; each unit costs
model calls.

For each unit of prompts/audit_correspondence_units_v1.json, one call of the `claude` (or `codex`)
command line maps one direction over the unit's files, and as soon as it is done a second call, a
skeptic, tries to refute what the first found. Units run in parallel (--jobs). When every unit is
done, one more call writes the report for Luciano. The prompts are
prompts/audit_correspondence_{common,map_spec,map_impl,map_docs,verify,report}_v1.md.

The audit is pinned to one commit (--commit, default HEAD). The script checks that commit out as a
detached git worktree in a temporary directory and runs every call there, with PYTHONPATH and
LUTHIER_PATH pointing into the worktree (the `luthier` command is an editable install of the
working tree; without PYTHONPATH it would run the working tree, not the commit). Each call gets its
own scratch folder for the programs it writes. The worktree is removed at the end, also on error,
Ctrl-C, SIGTERM or SIGHUP (the terminal closed). Each call runs in its own session; a timeout or a
stop kills it with every process it started. Luciano's tree is read for the prompts and written
only for the outputs.

What a claude call may do is a list of permission rules (CLAUDE_RULES): read anything; run
`luthier check|test|eval|run`, `git log|show|grep|blame`, grep, ls, wc, and python3 on files of its
scratch folder; write with its Write and Edit tools only in that folder. `luthier certify` and git
commands that change state are not on the list. The calls load no user settings, so the user's own
allow rules and hooks don't apply to them. These rules are not a sandbox, and they do not make a
call read-only: python3 runs code the model wrote, `git log|show --output=FILE` writes a file,
`git grep -O<cmd>` runs a command, and `luthier test|run` write a .cert.json or .run.json next to
the file they are given. What keeps Luciano's tree untouched is the prompt (write nothing outside
the scratch folder), and that the audit reads a disposable worktree. The codex calls run in
codex's workspace-write sandbox: they can write in the worktree and the temporary directory, not in
Luciano's tree.

Outputs, under record/audits/:
  <date>_correspondence_v1_<model>/<unit>.map.json, <unit>.verify.json   {"meta", "output"}
  <date>_correspondence_v1_<model>/<unit>.<stage>.error.txt              a call that failed twice
  <date>_correspondence_v1_<model>.md                                    the report
The report's header is written here (commit, prompt files with their sha256, model, CLI and its
version, date, units run and failed); its body is the model's.

Idempotent: a unit whose outputs exist is skipped unless --force, so a run that stopped half way
is resumed by running it again (on another day, with --date of the first run). Outputs made at
another commit, or with other prompts or another unit definition, stop the run (use --force, or
--commit to resume an audit at the commit it was made at). A second run on the same outputs while
one is going stops at once.

Exit status: 0 every unit and the report succeeded; 1 some unit or the report failed; 2 usage
error, outputs made differently, or another run on the same outputs; 130 interrupted.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = Path(__file__).resolve()
PROMPTS_DIR = REPO_ROOT / "prompts"
DEFAULT_OUT_DIR = REPO_ROOT / "record" / "audits"
AUDIT = "correspondence"
DEFAULT_VERSION = "v1"

DEFAULT_CLAUDE_MODEL = "opus"
DEFAULT_CODEX_MODEL = "gpt-5.4"
DEFAULT_TIMEOUT = 3600.0
ATTEMPTS = 2                       # an invalid output is retried once

# direction -> (map prompt, name of the list in the map's output, which is also its schema)
DIRECTIONS = {
    "spec": ("map_spec", "claims"),
    "impl": ("map_impl", "behaviors"),
    "docs": ("map_docs", "claims"),
}
PROMPT_NAMES = ("common", "map_spec", "map_impl", "map_docs", "verify", "report")
PLACEHOLDERS = {
    "common": ("commit", "worktree", "scratch"),
    "map_spec": ("unit", "files"),
    "map_impl": ("unit", "files"),
    "map_docs": ("unit", "files"),
    "verify": ("unit", "direction", "entries"),
    "report": ("failed", "results"),
}
PLACEHOLDER_RE = re.compile(r"\{([a-z_]+)\}")

# What a claude call may do. Reading is free; running is limited to luthier (never certify),
# git commands that read, and python3 on files of its own scratch folder, where alone its Write and
# Edit tools may write. The calls load no user settings (--setting-sources project,local), so the
# user's own allow rules and hooks don't widen this; the worktree has no .claude/ of its own. These
# are permission rules, not a sandbox: see the docstring for the ways around them.
CLAUDE_TOOLS = "Read,Grep,Glob,Bash,Write,Edit"
CLAUDE_RULES = [
    "Read", "Grep", "Glob",
    "Bash(luthier check *)", "Bash(luthier eval *)",
    "Bash(git log *)", "Bash(git show *)", "Bash(git grep *)", "Bash(git blame *)",
    "Bash(grep *)", "Bash(ls *)", "Bash(wc *)",
]


def claude_rules(scratch: str) -> list[str]:
    # luthier test and run write a .cert.json or .run.json next to the file they are given, so they
    # are allowed only on files of the scratch folder.
    return CLAUDE_RULES + [f"Bash(luthier test {scratch}/*)", f"Bash(luthier run {scratch}/*)",
                           f"Bash(python3 {scratch}/*)", f"Write(/{scratch}/**)", f"Edit(/{scratch}/**)"]


def tree_state(out_dir: Path) -> dict:
    """What a call could change in Luciano's tree: HEAD, the refs, and the status of the working tree,
    the audit's own outputs left out. The permission rules are not a sandbox, so the run compares this
    before and after, and says so if it changed."""
    skip = rel(out_dir)
    lines = git("status", "--porcelain=v1", "--untracked-files=all", check=False).stdout.splitlines()
    return {"head": git("rev-parse", "HEAD", check=False).stdout.strip(),
            "refs": git("for-each-ref", "--format=%(refname) %(objectname)", check=False).stdout,
            "status": sorted(l for l in lines if not l[3:].strip('"').startswith(skip))}


def tree_changes(before: dict, after: dict) -> list[str]:
    out = []
    if before["head"] != after["head"]:
        out.append(f"HEAD moved from {before['head'][:12]} to {after['head'][:12]}")
    if before["refs"] != after["refs"]:
        out.append("the refs changed (git for-each-ref)")
    b, a = set(before["status"]), set(after["status"])
    out += [f"new in git status: {l}" for l in sorted(a - b)]
    out += [f"gone from git status: {l}" for l in sorted(b - a)]
    return out


# ----------------------------------------------------------------------------------------------
# Schemas of the outputs (the same as the workflow of the first run), and a validator for the
# subset of JSON Schema they use: type, properties, required, additionalProperties, items, enum.

SEVERITY = {"type": "string", "enum": ["high", "medium", "low"]}
CLAIM = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "description": 'unique within your output, prefixed by your label, e.g. "05#12"'},
        "spec_ref": {"type": "string", "description": "docs/semantica/<file>:<line>"},
        "claim": {"type": "string", "description": "the normative claim in one line"},
        "status": {"type": "string", "enum": [
            "implemented_tested", "implemented_untested", "not_implemented_declared",
            "not_implemented_undeclared", "partial", "contradicts", "spec_open_or_nonnormative"]},
        "impl_refs": {"type": "array", "items": {"type": "string"}},
        "test_refs": {"type": "array", "items": {"type": "string"}},
        "evidence": {"type": "string", "description": "what the code does, in one to three lines; for contradicts "
                     "or partial, the minimal program and its actual result if you ran one"},
        "severity": SEVERITY,
    },
    "required": ["id", "spec_ref", "claim", "status", "impl_refs", "test_refs", "evidence", "severity"],
    "additionalProperties": False,
}
BEHAVIOR = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "impl_ref": {"type": "string", "description": "src/luthier/<file>:<line>"},
        "behavior": {"type": "string", "description": "what the code accepts, rejects, computes or prints, in one line"},
        "spec_ref": {"type": "string", "description": 'the specification line that names it, or "none"'},
        "status": {"type": "string", "enum": ["covered", "covered_differently", "not_in_spec", "internal"]},
        "test_refs": {"type": "array", "items": {"type": "string"}},
        "evidence": {"type": "string"},
        "severity": SEVERITY,
    },
    "required": ["id", "impl_ref", "behavior", "spec_ref", "status", "test_refs", "evidence", "severity"],
    "additionalProperties": False,
}
VERDICT = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "verdict": {"type": "string", "enum": ["confirmed", "refuted", "uncertain"]},
        "corrected_status": {"type": "string", "description": "the status you would give it, same vocabulary as the mapper"},
        "corrected_severity": SEVERITY,
        "evidence": {"type": "string", "description": "what you checked and found: file:line, program and result"},
    },
    "required": ["id", "verdict", "corrected_status", "corrected_severity", "evidence"],
    "additionalProperties": False,
}


def _list_schema(name: str, item: dict, extra: tuple = ("sections",)) -> dict:
    props = {k: {"type": "array", "items": {"type": "string"}} for k in extra}
    props[name] = {"type": "array", "items": item}
    props["notes"] = {"type": "string"}
    return {"type": "object", "properties": props, "required": [*extra, name, "notes"],
            "additionalProperties": False}


SCHEMAS = {
    "claims": _list_schema("claims", CLAIM),
    "behaviors": _list_schema("behaviors", BEHAVIOR),
    "verdicts": _list_schema("verdicts", VERDICT, extra=()),
}

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool}


def validate(value, schema: dict, path: str = "$") -> list[str]:
    """The ways value departs from schema, one line each; empty when it conforms."""
    t = schema.get("type")
    if t in ("number", "integer"):
        ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        if ok and t == "integer":
            ok = isinstance(value, int)
        if not ok:
            return [f"{path}: expected {t}"]
    elif t is not None and not isinstance(value, _TYPES[t]):
        return [f"{path}: expected {t}, got {type(value).__name__}"]
    errors: list[str] = []
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if t == "object":
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key!r}")
        for key, sub in value.items():
            if key in props:
                errors += validate(sub, props[key], f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected {key!r}")
    elif t == "array" and "items" in schema:
        for i, item in enumerate(value):
            errors += validate(item, schema["items"], f"{path}[{i}]")
    return errors


# ----------------------------------------------------------------------------------------------
# Small helpers.

class UsageError(Exception):
    pass


class CallError(Exception):
    """A call that failed or gave an output we can't use; raw is what it printed."""

    def __init__(self, message: str, raw: str = ""):
        super().__init__(message)
        self.raw = raw


class Interrupted(Exception):
    pass


class StageFailed(Exception):
    def __init__(self, stage: str, failures: list[tuple[int, str, str]], cost_usd: float | None = None):
        super().__init__(f"{stage} failed {len(failures)} times: " + "; ".join(f[1] for f in failures))
        self.stage = stage
        self.failures = failures
        self.cost_usd = cost_usd


_PRINT = threading.Lock()


def say(message: str, err: bool = False) -> None:
    with _PRINT:
        print(message, file=sys.stderr if err else sys.stdout, flush=True)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def slug(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.strip().lower())
    return text.strip("-") or "x"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def fill(template: str, values: dict) -> str:
    """Replace {name} by values[name] in one pass; a value is never scanned again, and a {name}
    with no value is left as it is."""
    return PLACEHOLDER_RE.sub(lambda m: str(values[m.group(1)]) if m.group(1) in values else m.group(0),
                              template)


def write_atomic(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(tmp, 0o644)                 # mkstemp makes it 0600
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def lock_dir(path: Path) -> int | None:
    """An exclusive lock on the output folder for the life of this process, or None if another run
    holds it. Two runs on the same outputs would pay for every call twice and write the same files."""
    fd = os.open(path, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(fd)
        return None
    return fd


def write_json(path: Path, value) -> None:
    write_atomic(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def json_from_text(text: str):
    """The JSON object in a model's text answer, with or without a fence around it."""
    body = text.strip()
    body = re.sub(r"\A```[a-zA-Z]*\s*\n", "", body)
    body = re.sub(r"\n```\s*\Z", "", body)
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        start, end = body.find("{"), body.rfind("}")
        if 0 <= start < end:
            try:
                return json.loads(body[start:end + 1])
            except json.JSONDecodeError:
                pass
    raise CallError("the answer is not JSON", text)


# ----------------------------------------------------------------------------------------------
# Inputs: the units file and the prompts.

@dataclass
class Prompt:
    name: str
    path: Path
    text: str
    sha256: str


UNITS_KEYS = {"about", "audited_paths", "verify", "units"}
UNIT_KEYS = {"label", "direction", "files"}
SELECTION_KEYS = {"exclude_statuses", "spot_check_status", "spot_checks"}


def statuses(kind: str) -> list[str]:
    """The statuses an entry of a map's list may have, from its schema."""
    return SCHEMAS[kind]["properties"][kind]["items"]["properties"]["status"]["enum"]


def load_units(path: Path) -> dict:
    """The units file, checked: a typo must stop the run, since a misspelt key or status would
    otherwise change silently what is audited or what the skeptic sees."""
    if not path.is_file():
        raise UsageError(f"units file not found: {path}")
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise UsageError(f"{path}: not JSON: {exc}") from exc
    if not isinstance(cfg, dict):
        raise UsageError(f"{path}: must be a JSON object with {', '.join(sorted(UNITS_KEYS))}")
    if set(cfg) - UNITS_KEYS:
        raise UsageError(f"{path}: unknown key(s) {', '.join(sorted(set(cfg) - UNITS_KEYS))}; "
                         f"the keys are {', '.join(sorted(UNITS_KEYS))}")
    units = cfg.get("units")
    if not isinstance(units, list) or not units:
        raise UsageError(f"{path}: no units")
    seen = set()
    for u in units:
        if not isinstance(u, dict) or not all(isinstance(u.get(k), str) and u.get(k) for k in UNIT_KEYS):
            raise UsageError(f"{path}: a unit needs label, direction and files: {u!r}")
        if set(u) - UNIT_KEYS:
            raise UsageError(f"{path}: unit {u['label']}: unknown key(s) {', '.join(sorted(set(u) - UNIT_KEYS))}")
        if u["direction"] not in DIRECTIONS:
            raise UsageError(f"{path}: unit {u['label']}: direction must be one of {sorted(DIRECTIONS)}")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", u["label"]) or u["label"] == "report":
            raise UsageError(f"{path}: unit label {u['label']!r}: letters, digits, '-' and '_' only, not 'report'")
        if u["label"] in seen:
            raise UsageError(f"{path}: unit {u['label']} appears twice")
        seen.add(u["label"])
    verify = cfg.get("verify")
    if not isinstance(verify, dict) or set(verify) != {"claims", "behaviors"}:
        raise UsageError(f"{path}: verify needs exactly claims and behaviors")
    for kind in ("claims", "behaviors"):
        p = verify[kind]
        if not (isinstance(p, dict) and set(p) == SELECTION_KEYS and isinstance(p["exclude_statuses"], list)
                and isinstance(p["spot_check_status"], str) and type(p["spot_checks"]) is int
                and p["spot_checks"] >= 0):
            raise UsageError(f"{path}: verify.{kind} needs exactly exclude_statuses (a list), spot_check_status "
                             "and spot_checks (an integer, 0 or more)")
        unknown = [s for s in p["exclude_statuses"] + [p["spot_check_status"]] if s not in statuses(kind)]
        if unknown:
            raise UsageError(f"{path}: verify.{kind}: unknown status(es) {', '.join(map(repr, unknown))}; "
                             f"the statuses are {', '.join(statuses(kind))}")
    audited = cfg.setdefault("audited_paths", ["src", "docs/semantica"])
    if not (isinstance(audited, list) and audited and all(isinstance(a, str) and a for a in audited)):
        raise UsageError(f"{path}: audited_paths must be a list of paths")
    cfg["_sha256"] = sha256_bytes(path.read_bytes())
    cfg["_path"] = path
    return cfg


def load_prompts(version: str) -> dict[str, Prompt]:
    prompts = {}
    for name in PROMPT_NAMES:
        path = PROMPTS_DIR / f"audit_{AUDIT}_{name}_{version}.md"
        if not path.is_file():
            raise UsageError(f"prompt not found: {path}")
        data = path.read_bytes()
        text = data.decode("utf-8")
        missing = [p for p in PLACEHOLDERS[name] if "{" + p + "}" not in text]
        if missing:
            raise UsageError(f"{path}: missing placeholders {', '.join('{' + m + '}' for m in missing)}")
        prompts[name] = Prompt(name, path, text, sha256_bytes(data))
    return prompts


# ----------------------------------------------------------------------------------------------
# git: the commit, the worktree, the warnings.

def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {(proc.stderr or proc.stdout).strip()}")
    return proc


def resolve_commit(rev: str) -> str | None:
    proc = git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}", check=False)
    return proc.stdout.strip() if proc.returncode == 0 else None


def commit_line(sha: str) -> str:
    subject, date = git("log", "-1", "--format=%s%x00%cs", sha).stdout.rstrip("\n").split("\x00")
    return f"`{sha}`, \"{subject}\", {date}"


def warn_uncommitted(paths: list[str], sha: str) -> None:
    absent = [p for p in paths if git("cat-file", "-e", f"{sha}:{p}", check=False).returncode != 0]
    if absent:
        say(f"WARNING: audited_paths not in commit {sha[:12]} (a typo?): {', '.join(absent)}", err=True)
    proc = git("status", "--porcelain", "--", *paths, check=False)
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    if lines:
        say(f"WARNING: uncommitted changes in {', '.join(paths)} are not audited; the audit reads "
            f"commit {sha[:12]}:", err=True)
        for line in lines[:10]:
            say(f"  {line}", err=True)
        if len(lines) > 10:
            say(f"  ... and {len(lines) - 10} more", err=True)


def add_worktree(path: Path, sha: str) -> None:
    git("worktree", "add", "--detach", "--quiet", str(path), sha)


def remove_worktree(path: Path) -> None:
    git("worktree", "remove", "--force", "--force", str(path), check=False)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    git("worktree", "prune", check=False)


# ----------------------------------------------------------------------------------------------
# The command line of the model.

def resolve_cli(choice: str) -> str:
    if choice in ("claude", "codex"):
        if shutil.which(choice) is None:
            raise RuntimeError(f"{choice} is not on the PATH")
        return choice
    for name in ("claude", "codex"):
        if shutil.which(name):
            return name
    raise RuntimeError("neither claude nor codex is on the PATH")


def cli_version(cli: str) -> str:
    try:
        proc = subprocess.run([cli, "--version"], capture_output=True, text=True, timeout=60)
        return (proc.stdout or proc.stderr).strip().splitlines()[0] if proc.returncode == 0 else "unknown"
    except (OSError, subprocess.TimeoutExpired, IndexError):
        return "unknown"


def cli_argv(cli: str, model: str, schema_name: str | None, worktree: str, scratch: str,
             schema_file: str, last_file: str) -> list[str]:
    if cli == "claude":
        argv = ["claude", "-p", "--model", model, "--output-format", "json", "--no-session-persistence",
                "--setting-sources", "project,local", "--permission-mode", "dontAsk",
                "--tools", CLAUDE_TOOLS, "--add-dir", scratch,
                "--allowedTools", *claude_rules(scratch)]
        if schema_name:
            argv += ["--json-schema", json.dumps(SCHEMAS[schema_name], separators=(",", ":"))]
        return argv
    argv = ["codex", "exec", "--skip-git-repo-check", "--color", "never", "--sandbox", "workspace-write",
            "-C", worktree, "-o", last_file, "-m", model]
    if schema_name:
        argv += ["--output-schema", schema_file]
    return argv + ["-"]


GRACE_S = 5.0                      # from SIGTERM to SIGKILL, and the longest wait for what a killed call printed
POLL_S = 1.0                       # how often a waiting call looks at the stop flag


def signal_group(proc: subprocess.Popen, sig: int) -> None:
    """Send sig to every process of the call's group: the CLI and what it started (each call is
    the leader of its own session)."""
    try:
        os.killpg(proc.pid, sig)
    except (ProcessLookupError, PermissionError):
        pass


class Runner:
    """Runs the calls, and stops them all on Ctrl-C.

    Each call runs in its own session, so that a timeout or a stop kills the CLI and every process
    it started: a tool's process that outlived a killed CLI could keep its output open, and reading
    it would then never end."""

    def __init__(self):
        self.lock = threading.Lock()
        self.procs: set[subprocess.Popen] = set()
        self.stop = threading.Event()

    def run(self, argv: list[str], *, cwd: Path, env: dict, stdin: str, timeout: float) -> tuple[int, str, str]:
        with self.lock:
            if self.stop.is_set():
                raise Interrupted()
            proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, start_new_session=True)
            self.procs.add(proc)
        deadline = time.monotonic() + timeout
        data: str | None = stdin
        try:
            while True:
                try:
                    out, err = proc.communicate(data, timeout=max(0.0, min(POLL_S, deadline - time.monotonic())))
                    break
                except subprocess.TimeoutExpired:
                    data = None                    # the input is sent once; a retry must not pass it again
                    if self.stop.is_set():
                        self.end(proc)
                        raise Interrupted() from None
                    if proc.poll() is not None:   # the CLI is done; a process it started still holds its output
                        out, err = self.end(proc)
                        break
                    if time.monotonic() >= deadline:
                        out, _ = self.end(proc)
                        raise CallError(f"timed out after {timeout:.0f} s", out) from None
        except (CallError, Interrupted):   # the call is already ended
            raise
        except BaseException:          # Ctrl-C while the main thread waits: the call must not outlive us
            self.end(proc)
            raise
        finally:
            with self.lock:
                self.procs.discard(proc)
        if self.stop.is_set():
            raise Interrupted()
        return proc.returncode, out, err

    @staticmethod
    def end(proc: subprocess.Popen) -> tuple[str, str]:
        """Stop one call and its group: SIGTERM, then SIGKILL after GRACE_S. Returns what it printed,
        or nothing if a process outside its group still holds its output."""
        if proc.returncode is None:
            signal_group(proc, signal.SIGTERM)
            try:
                proc.wait(timeout=GRACE_S)
            except subprocess.TimeoutExpired:
                pass
        signal_group(proc, signal.SIGKILL)
        try:
            out, err = proc.communicate(timeout=GRACE_S)
            return out or "", err or ""
        except (subprocess.TimeoutExpired, ValueError, OSError):
            for f in (proc.stdout, proc.stderr):
                try:
                    f.close()
                except (OSError, AttributeError):
                    pass
            return "", ""

    def stop_all(self) -> None:
        self.stop.set()
        with self.lock:
            procs = list(self.procs)
        for p in procs:
            signal_group(p, signal.SIGTERM)
        deadline = time.monotonic() + GRACE_S
        for p in procs:
            while p.poll() is None and time.monotonic() < deadline:
                time.sleep(0.05)
        for p in procs:
            signal_group(p, signal.SIGKILL)


# ----------------------------------------------------------------------------------------------
# The audit.

@dataclass
class Ctx:
    args: argparse.Namespace
    cfg: dict
    prompts: dict[str, Prompt]
    sha: str
    cli: str
    model: str
    date: str
    unit_dir: Path
    report_path: Path
    cli_version: str = "unknown"
    script_sha256: str = ""
    tmp: Path | None = None
    worktree: Path | None = None
    env: dict = field(default_factory=dict)
    runner: Runner = field(default_factory=Runner)


@dataclass
class Outcome:
    label: str
    ran: bool = False
    failed: str | None = None
    interrupted: bool = False


def map_path(ctx: Ctx, label: str) -> Path:
    return ctx.unit_dir / f"{label}.map.json"


def verify_path(ctx: Ctx, label: str) -> Path:
    return ctx.unit_dir / f"{label}.verify.json"


def stage_prompts(ctx: Ctx, stage_prompt: str) -> dict[str, str]:
    return {rel(ctx.prompts[n].path): ctx.prompts[n].sha256 for n in ("common", stage_prompt)}


def expected_key(ctx: Ctx, unit: dict, stage: str) -> dict:
    """What an existing output must have been made with to count as done."""
    prompt = DIRECTIONS[unit["direction"]][0] if stage == "map" else "verify"
    key = {"commit": ctx.sha, "cli": ctx.cli, "model": ctx.model, "prompts": stage_prompts(ctx, prompt),
           "unit": {k: unit[k] for k in ("label", "direction", "files")}}
    if stage == "verify":
        key["selection"] = ctx.cfg["verify"][DIRECTIONS[unit["direction"]][1]]
    return key


def stale_reason(ctx: Ctx, unit: dict, stage: str, doc: dict) -> str | None:
    meta = doc.get("meta", {})
    for k, v in expected_key(ctx, unit, stage).items():
        if meta.get(k) != v:
            return f"{k} was {json.dumps(meta.get(k))[:120]}, now {json.dumps(v)[:120]}"
    return None


def done(path: Path) -> dict | None:
    doc = read_json(path)
    return doc if isinstance(doc, dict) and isinstance(doc.get("output"), dict) else None


def select_entries(ctx: Ctx, unit: dict, output: dict) -> list[dict]:
    kind = DIRECTIONS[unit["direction"]][1]
    p = ctx.cfg["verify"][kind]
    items = output.get(kind, [])
    gaps = [e for e in items if e.get("status") not in p["exclude_statuses"]]
    if p["spot_check_status"] not in p["exclude_statuses"]:
        return gaps                   # every entry of that status is already among the gaps
    spot = [e for e in items if e.get("status") == p["spot_check_status"]][:p["spot_checks"]]
    return gaps + spot


def needs_verify(ctx: Ctx, unit: dict) -> bool:
    m, v = done(map_path(ctx, unit["label"])), done(verify_path(ctx, unit["label"]))
    return v is None or m is None or v["meta"].get("map_sha256") != sha256_json(m["output"])


def needs_work(ctx: Ctx, unit: dict) -> bool:
    return ctx.args.force or done(map_path(ctx, unit["label"])) is None or needs_verify(ctx, unit)


def compose(ctx: Ctx, stage_prompt: str, values: dict) -> str:
    return fill(ctx.prompts["common"].text, values).rstrip() + "\n\n" + fill(ctx.prompts[stage_prompt].text, values)


def run_call(ctx: Ctx, *, stage: str, label: str, prompt_name: str, schema_name: str | None,
             values: dict) -> tuple[object, dict, int]:
    """One stage of one unit: the call, its output parsed and validated, a second attempt if not.
    The cost it reports is summed over the attempts."""
    failures: list[tuple[int, str, str]] = []
    costs: list[float] = []
    for attempt in range(1, ATTEMPTS + 1):
        if ctx.runner.stop.is_set():
            raise Interrupted()
        scratch = ctx.tmp / "scratch" / f"{label}.{stage}.{attempt}"
        scratch.mkdir(parents=True)
        schema_file = ctx.tmp / "scratch" / f"{label}.{stage}.{attempt}.schema.json"
        last_file = ctx.tmp / "scratch" / f"{label}.{stage}.{attempt}.last.txt"
        if schema_name:
            schema_file.write_text(json.dumps(SCHEMAS[schema_name]), encoding="utf-8")
        prompt = compose(ctx, prompt_name, dict(values, commit=ctx.sha, worktree=str(ctx.worktree),
                                                scratch=str(scratch)))
        argv = cli_argv(ctx.cli, ctx.model, schema_name, str(ctx.worktree), str(scratch), str(schema_file),
                        str(last_file))
        started = time.monotonic()
        raw = ""
        try:
            code, out, err = ctx.runner.run(argv, cwd=ctx.worktree, env=ctx.env, stdin=prompt,
                                            timeout=ctx.args.timeout)
            raw = out
            obj = None
            if ctx.cli == "claude":
                try:
                    obj = json.loads(out)
                except json.JSONDecodeError:
                    pass
                # a call that failed may still have cost something: count it before anything else
                if isinstance(obj, dict) and isinstance(obj.get("total_cost_usd"), (int, float)):
                    costs.append(obj["total_cost_usd"])
            if code != 0:
                raise CallError(f"{ctx.cli} exited {code}: {(err or out).strip()[:300]}", out + err)
            info: dict = {"duration_s": round(time.monotonic() - started, 1)}
            if ctx.cli == "claude":
                if obj is None:
                    raise CallError("claude printed no JSON", out)
                if not isinstance(obj, dict):
                    raise CallError("claude printed JSON that is not an object", out)
                if obj.get("is_error"):
                    raise CallError(f"claude reported an error ({obj.get('subtype')}): "
                                    f"{str(obj.get('result'))[:300]}", out)
                if obj.get("num_turns") is not None:
                    info["num_turns"] = obj["num_turns"]
                if schema_name:
                    result = obj.get("structured_output")
                    if result is None:
                        result = json_from_text(str(obj.get("result") or ""))
                else:
                    result = str(obj.get("result") or "")
            else:
                text = last_file.read_text(encoding="utf-8") if last_file.is_file() else ""
                raw = text or out
                result = json_from_text(text) if schema_name else text
            if schema_name:
                problems = validate(result, SCHEMAS[schema_name])
                if problems:
                    more = f" (and {len(problems) - 3} more)" if len(problems) > 3 else ""
                    raise CallError("the answer does not fit the schema: " + "; ".join(problems[:3]) + more, raw)
            elif "## Summary" not in result:
                raise CallError('the report has no "## Summary"', raw)
            if costs:
                info["cost_usd"] = round(sum(costs), 4)
            return result, info, attempt
        except CallError as exc:
            failures.append((attempt, str(exc), exc.raw or raw))
            say(f"  {stage} {label}: attempt {attempt} failed: {exc}", err=True)
    raise StageFailed(stage, failures, round(sum(costs), 4) if costs else None)


def write_error(ctx: Ctx, label: str, exc: StageFailed) -> Path:
    path = ctx.unit_dir / f"{label}.{exc.stage}.error.txt"
    parts = [f"{label} {exc.stage}: failed at commit {ctx.sha}, {ctx.cli} {ctx.model}, "
             f"{dt.datetime.now().isoformat(timespec='seconds')}"]
    if exc.cost_usd is not None:
        parts.append(f"cost reported by the CLI: {exc.cost_usd} USD")
    for attempt, message, raw in exc.failures:
        parts.append(f"\n--- attempt {attempt}: {message}\n--- output:\n{raw}")
    write_atomic(path, "\n".join(parts) + "\n")
    return path


def clear_error(ctx: Ctx, label: str, stage: str) -> None:
    (ctx.unit_dir / f"{label}.{stage}.error.txt").unlink(missing_ok=True)


def base_meta(ctx: Ctx, unit: dict, stage: str) -> dict:
    meta = {"audit": AUDIT, "version": ctx.args.prompt_version, "stage": stage}
    meta.update(expected_key(ctx, unit, stage))
    meta.update({"cli_version": ctx.cli_version, "script_sha256": ctx.script_sha256,
                 "units_file": rel(ctx.cfg["_path"]), "units_sha256": ctx.cfg["_sha256"],
                 "date": dt.datetime.now().astimezone().isoformat(timespec="seconds")})
    return meta


def run_unit(ctx: Ctx, unit: dict) -> Outcome:
    label, direction = unit["label"], unit["direction"]
    prompt_name, kind = DIRECTIONS[direction]
    outcome = Outcome(label)
    try:
        mpath = map_path(ctx, label)
        if ctx.args.force or done(mpath) is None:
            say(f"[map] {label} ...")
            result, info, attempts = run_call(ctx, stage="map", label=label, prompt_name=prompt_name,
                                              schema_name=kind, values={"unit": label, "files": unit["files"]})
            meta = base_meta(ctx, unit, "map") | {"attempts": attempts} | info
            write_json(mpath, {"meta": meta, "output": result})
            clear_error(ctx, label, "map")
            outcome.ran = True
            say(f"[map] {label}: {len(result[kind])} {kind}, attempt {attempts}")
            if not result[kind]:
                say(f"[map] {label}: WARNING: the map found no {kind}; it is kept, and the report header "
                    "names it", err=True)
        mdoc = done(mpath)
        vpath = verify_path(ctx, label)
        if ctx.args.force or outcome.ran or needs_verify(ctx, unit):
            entries = select_entries(ctx, unit, mdoc["output"])
            meta = base_meta(ctx, unit, "verify") | {"map_sha256": sha256_json(mdoc["output"]),
                                                     "entries": [e.get("id") for e in entries]}
            if not entries:
                result = {"verdicts": [], "notes": "nothing to verify"}
                meta["called"] = False
            else:
                say(f"[verify] {label}: {len(entries)} entries ...")
                result, info, attempts = run_call(
                    ctx, stage="verify", label=label, prompt_name="verify", schema_name="verdicts",
                    values={"unit": label, "direction": direction, "files": unit["files"],
                            "entries": json.dumps(entries, indent=1, ensure_ascii=False)})
                seen = {v["id"] for v in result["verdicts"]}
                meta |= {"called": True, "attempts": attempts,
                         "entries_without_verdict": [e.get("id") for e in entries if e.get("id") not in seen]}
                meta |= info
            write_json(vpath, {"meta": meta, "output": result})
            clear_error(ctx, label, "verify")
            outcome.ran = True
            say(f"[verify] {label}: {len(result['verdicts'])} verdicts")
    except Interrupted:
        outcome.interrupted = True
    except StageFailed as exc:
        if ctx.runner.stop.is_set():
            outcome.interrupted = True
        else:
            path = write_error(ctx, label, exc)
            outcome.failed = f"{exc.stage} failed twice, see {rel(path)}"
            say(f"[{exc.stage}] {label}: FAILED, see {rel(path)}", err=True)
    except Exception as exc:  # noqa: BLE001  one unit's accident must not stop the others
        outcome.failed = f"{type(exc).__name__}: {exc}"
        say(f"{label}: FAILED: {outcome.failed}", err=True)
    return outcome


def unit_results(ctx: Ctx) -> tuple[list[dict], list[str]]:
    """The results of every unit of the units file with both outputs made as this run would make
    them (same commit, prompts, model, unit), and the labels without."""
    results, missing = [], []
    for unit in ctx.cfg["units"]:
        m, v = done(map_path(ctx, unit["label"])), done(verify_path(ctx, unit["label"]))
        if (m is None or v is None or v["meta"].get("map_sha256") != sha256_json(m["output"])
                or stale_reason(ctx, unit, "map", m) or stale_reason(ctx, unit, "verify", v)):
            missing.append(unit["label"])
            continue
        results.append({"label": unit["label"], "direction": unit["direction"], "files": unit["files"],
                        "out": m["output"], "verify": v["output"]})
    return results, missing


def kept_costs(ctx: Ctx) -> list[float]:
    """The cost each kept output reports, over every unit of the units file."""
    costs = []
    for unit in ctx.cfg["units"]:
        for path in (map_path(ctx, unit["label"]), verify_path(ctx, unit["label"])):
            doc = done(path)
            if doc and isinstance(doc["meta"].get("cost_usd"), (int, float)):
                costs.append(doc["meta"]["cost_usd"])
    return costs


def report_header(ctx: Ctx, results: list[dict], failed: list[str], not_run: list[str],
                  report_cost: float | None) -> str:
    n = len(ctx.cfg["units"])
    costs = kept_costs(ctx)
    if isinstance(report_cost, (int, float)):
        costs.append(report_cost)
    lines = [
        "# Correspondence audit of Luthier",
        "",
        f"Draft 0, {ctx.date}. Status: for Luciano; the bites need his answer.",
        "Written for Luciano: is the specification (docs/semantica/) a faithful reflection of the "
        "implementation (src/luthier/) and of the documentation (README.md, examples/)?",
        f"Sources: the repository at `{ctx.sha[:7]}`; for each unit one model call mapped one direction and "
        "a second call, a skeptic, tried to refute each finding. This header is written by "
        "`scripts/audit_correspondence.py`; the rest is the model's.",
        "",
        f"- Commit audited: {commit_line(ctx.sha)}",
        f"- Script: `{rel(SCRIPT)}`, sha256 `{ctx.script_sha256}`",
        "- Prompts:",
        *[f"  - `{rel(p.path)}`, sha256 `{p.sha256}`" for p in ctx.prompts.values()],
        f"- Units: `{rel(ctx.cfg['_path'])}`, sha256 `{ctx.cfg['_sha256']}`",
        f"- CLI: `{ctx.cli}`, {ctx.cli_version}",
        f"- Model: `{ctx.model}`",
        f"- Date: {ctx.date}",
        f"- Units run: {len(results)} of {n}: {', '.join(r['label'] for r in results) or 'none'}",
        f"- Units failed: {', '.join(failed) or 'none'}",
    ]
    if not_run:
        lines.append(f"- Units not run: {', '.join(not_run)}")
    empty = [r["label"] for r in results if not r["out"].get(DIRECTIONS[r["direction"]][1])]
    if empty:
        lines.append(f"- Units whose map found nothing (a map that finds nothing has probably failed): "
                     f"{', '.join(empty)}")
    lines.append(f"- Unit outputs: `{rel(ctx.unit_dir)}/`")
    if costs:
        lines.append(f"- Cost reported by the CLI: {sum(costs):.2f} USD, over the {len(costs)} stages whose "
                     "output is kept and this report (failed stages are in their .error.txt)")
    return "\n".join(lines)


def clean_report(text: str) -> str:
    body = text.strip()
    body = re.sub(r"\A```[a-zA-Z]*\s*\n", "", body)
    body = re.sub(r"\n```\s*\Z", "", body)
    i = body.find("## Summary")
    return body[i:].strip() if i > 0 else body.strip()


def write_report(ctx: Ctx, failed: list[str]) -> bool:
    results, missing = unit_results(ctx)
    if not results:
        say("No unit has results; no report written.", err=True)
        return False
    not_run = [l for l in missing if l not in failed]
    say(f"[report] from {len(results)} units ...")
    try:
        body, info, _ = run_call(ctx, stage="report", label="report", prompt_name="report", schema_name=None,
                                 values={"failed": json.dumps(missing),
                                         "results": json.dumps(results, ensure_ascii=False)})
    except StageFailed as exc:
        if ctx.runner.stop.is_set():
            raise Interrupted() from exc
        path = write_error(ctx, "report", exc)
        say(f"[report] FAILED, see {rel(path)}", err=True)
        return False
    header = report_header(ctx, results, [l for l in failed if l in missing], not_run, info.get("cost_usd"))
    write_atomic(ctx.report_path, f"{header}\n\n{clean_report(body)}\n")
    clear_error(ctx, "report", "report")
    say(f"[report] {rel(ctx.report_path)}")
    return True


# ----------------------------------------------------------------------------------------------
# Dry run.

def dry_run(ctx: Ctx, units: list[dict]) -> None:
    wt, tmp = "<tmp>/worktree", "<tmp>"
    if ctx.cli == "claude":
        say(f"Allowed to the claude calls ({{scratch}} is the call's own folder): "
            + " ".join(claude_rules("{scratch}")))
    else:
        say("The codex calls run in its workspace-write sandbox rooted at the worktree.")

    def show(stage: str, label: str, schema_name: str | None, prompt: str, note: str = "") -> None:
        scratch = f"{tmp}/scratch/{label}.{stage}.1"
        argv = cli_argv(ctx.cli, ctx.model, schema_name, wt, scratch, f"{scratch}.schema.json", f"{scratch}.last.txt")
        shown, skip = [], 0
        for i, a in enumerate(argv):
            if skip:
                skip -= 1
                continue
            if a == "--allowedTools":
                shown.append("--allowedTools <the rules above>")
                skip = len(claude_rules(scratch))
            elif i > 0 and argv[i - 1] == "--json-schema":
                shown.append(f"<{schema_name} schema, {len(a)} chars>")
            else:
                shown.append(a)
        name = stage if stage == label else f"{stage} {label}"
        say(f"[dry] {name}: {' '.join(shown)}  (cwd {wt}; prompt {len(prompt):,} chars{note})")

    for unit in units:
        label = unit["label"]
        prompt_name, kind = DIRECTIONS[unit["direction"]]
        values = {"commit": ctx.sha, "worktree": wt, "unit": label, "files": unit["files"],
                  "direction": unit["direction"]}
        mdoc = done(map_path(ctx, label))
        if mdoc is not None and not ctx.args.force:
            say(f"[dry] map {label}: done, skipped")
        else:
            show("map", label, kind, compose(ctx, prompt_name, values | {"scratch": f"{tmp}/scratch/{label}.map.1"}))
        vals = values | {"scratch": f"{tmp}/scratch/{label}.verify.1"}
        if mdoc is not None and not ctx.args.force and not needs_verify(ctx, unit):
            say(f"[dry] verify {label}: done, skipped")
        elif mdoc is not None and not ctx.args.force:
            entries = select_entries(ctx, unit, mdoc["output"])
            show("verify", label, "verdicts",
                 compose(ctx, "verify", vals | {"entries": json.dumps(entries, indent=1, ensure_ascii=False)}),
                 f", {len(entries)} entries")
        else:
            show("verify", label, "verdicts", compose(ctx, "verify", vals | {"entries": ""}),
                 " plus the entries its map selects; no call if none")
    if ctx.args.no_report:
        say("[dry] report: not written (--no-report)")
    else:
        show("report", "report", None,
             compose(ctx, "report", {"commit": ctx.sha, "worktree": wt, "scratch": f"{tmp}/scratch/report.report.1",
                                     "failed": "[]", "results": ""}),
             " plus the results of every unit")


# ----------------------------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--commit", default="HEAD", help="Commit to audit (default HEAD).")
    p.add_argument("--only", action="append", metavar="UNIT", default=[],
                   help="Run only this unit (repeatable). The report still covers every unit with results.")
    p.add_argument("--units", type=Path, default=None,
                   help=f"Units file (default prompts/audit_{AUDIT}_units_<prompt version>.json).")
    p.add_argument("--prompt-version", default=DEFAULT_VERSION,
                   help=f"Version of the prompts and of the units file (default {DEFAULT_VERSION}).")
    p.add_argument("--cli", choices=("auto", "claude", "codex"), default="auto",
                   help="Command line to call. 'auto' prefers claude and falls back to codex.")
    p.add_argument("--model", default=None,
                   help=f"Model (default {DEFAULT_CLAUDE_MODEL} for claude, {DEFAULT_CODEX_MODEL} for codex).")
    p.add_argument("--jobs", type=int, default=4, help="Units run at the same time (default 4).")
    p.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help=f"Where outputs go (default {rel(DEFAULT_OUT_DIR)}).")
    p.add_argument("--date", default=None, help="Date in the output names, YYYY-MM-DD (default today); "
                                                 "give the first run's to resume it on another day.")
    p.add_argument("--force", action="store_true", help="Redo the units (and the report) even if done.")
    p.add_argument("--no-report", action="store_true", help="Run the units only.")
    p.add_argument("--dry-run", action="store_true", help="Print the calls it would make, and make none.")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Timeout per call, in seconds (default {DEFAULT_TIMEOUT:.0f}).")
    return p.parse_args(argv)


def _interrupt(signum, frame):
    raise KeyboardInterrupt()


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        if args.jobs < 1:
            raise UsageError("--jobs must be at least 1")
        if args.date is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
            raise UsageError("--date must be YYYY-MM-DD")
        cfg = load_units(args.units or PROMPTS_DIR / f"audit_{AUDIT}_units_{args.prompt_version}.json")
        prompts = load_prompts(args.prompt_version)
        labels = [u["label"] for u in cfg["units"]]
        unknown = [o for o in args.only if o not in labels]
        if unknown:
            raise UsageError(f"unknown unit(s): {', '.join(unknown)}; the units are {', '.join(labels)}")
        sha = resolve_commit(args.commit)
        if sha is None:
            raise UsageError(f"commit not found: {args.commit}")
    except UsageError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    try:
        cli = resolve_cli(args.cli)
    except RuntimeError as exc:
        if not args.dry_run:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        cli = "claude" if args.cli == "auto" else args.cli
        print(f"WARNING: {exc}; the dry run shows {cli}", file=sys.stderr)

    model = args.model or (DEFAULT_CLAUDE_MODEL if cli == "claude" else DEFAULT_CODEX_MODEL)
    date = args.date or dt.date.today().isoformat()
    tag = f"{date}_{AUDIT}_{args.prompt_version}_{slug(model)}"
    out_dir = args.out_dir.resolve()
    ctx = Ctx(args=args, cfg=cfg, prompts=prompts, sha=sha, cli=cli, model=model, date=date,
              unit_dir=out_dir / tag, report_path=out_dir / f"{tag}.md",
              script_sha256=sha256_bytes(SCRIPT.read_bytes()))
    units = [u for u in cfg["units"] if not args.only or u["label"] in args.only]

    warn_uncommitted(cfg["audited_paths"], sha)

    if args.dry_run:
        return audit(ctx, units)
    ctx.unit_dir.mkdir(parents=True, exist_ok=True)
    lock = lock_dir(ctx.unit_dir)
    if lock is None:
        print(f"ERROR: another run is writing {rel(ctx.unit_dir)}/ now; let it end, or use another --date "
              "or --out-dir.", file=sys.stderr)
        return 2
    try:
        return audit(ctx, units)
    finally:
        os.close(lock)


def audit(ctx: Ctx, units: list[dict]) -> int:
    args, sha, date = ctx.args, ctx.sha, ctx.date
    resume = f" --date {date}" if not args.date else ""
    if not args.force:        # every unit, not only the selected ones: the report reads them all
        stale, commits = [], set()
        for unit in ctx.cfg["units"]:
            for stage, path in (("map", map_path(ctx, unit["label"])), ("verify", verify_path(ctx, unit["label"]))):
                doc = done(path)
                reason = doc and stale_reason(ctx, unit, stage, doc)
                if reason:
                    stale.append(f"  {rel(path)}: {reason}")
                    commits.add(str(doc["meta"].get("commit")))
        if stale:
            print("ERROR: these outputs were made differently from this run:", file=sys.stderr)
            print("\n".join(stale), file=sys.stderr)
            old = sorted(c for c in commits if c != sha and resolve_commit(c) == c)
            if len(old) == 1:
                print(f"They were made at commit {old[0][:12]}: to resume that audit, add --commit {old[0][:12]}.",
                      file=sys.stderr)
            print("To redo them at this commit, use --force; to keep them, use another --date or --out-dir.",
                  file=sys.stderr)
            return 2

    todo = [u for u in units if needs_work(ctx, u)]
    print(f"Commit: {sha} | CLI: {ctx.cli} | model: {ctx.model} | jobs: {args.jobs}")
    print(f"Outputs: {rel(ctx.unit_dir)}/ | report: {rel(ctx.report_path)}")
    print(f"Units: {len(units)} | done: {len(units) - len(todo)} | to run: {len(todo)}")
    if args.dry_run:
        dry_run(ctx, units)
        return 0
    report_wanted = not args.no_report and (args.force or not ctx.report_path.exists())
    if not todo and not report_wanted:
        print("Nothing to do.")
        return 0

    ctx.cli_version = cli_version(ctx.cli)
    ctx.tmp = Path(tempfile.mkdtemp(prefix="luthier-audit-"))
    ctx.worktree = ctx.tmp / "worktree"
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(p for p in (str(ctx.worktree / "src"), env.get("PYTHONPATH", "")) if p)
    env["LUTHIER_PATH"] = str(ctx.worktree / "src" / "luthier" / "lib")
    ctx.env = env

    # SIGTERM and SIGHUP (the terminal closed) stop the run as Ctrl-C does: the calls are killed and
    # the worktree removed. Each call runs in its own session, so none of them gets these signals.
    old_handlers = {s: signal.signal(s, _interrupt) for s in (signal.SIGTERM, signal.SIGHUP)}
    before = tree_state(ctx.report_path.parent)
    outcomes: dict[str, Outcome] = {}
    report_ok = True
    status = 0
    try:
        add_worktree(ctx.worktree, sha)
        pool = cf.ThreadPoolExecutor(max_workers=args.jobs)
        try:
            futures = {pool.submit(run_unit, ctx, u): u["label"] for u in todo}
            for fut in cf.as_completed(futures):
                outcomes[futures[fut]] = fut.result()
        except BaseException:
            ctx.runner.stop_all()
            raise
        finally:
            pool.shutdown(wait=True, cancel_futures=True)
        failed = [u["label"] for u in units if u["label"] in outcomes and outcomes[u["label"]].failed]
        ran = any(o.ran for o in outcomes.values())
        if not args.no_report and (report_wanted or ran):
            report_ok = write_report(ctx, failed)
        elif not args.no_report:
            print(f"Report up to date: {rel(ctx.report_path)}")
        n_run = sum(1 for o in outcomes.values() if o.ran and not o.failed)
        print(f"\nUnits run: {n_run} | skipped (done): {len(units) - len(todo)} | failed: {len(failed)}")
        for label in failed:
            print(f"  - {label}: {outcomes[label].failed}", file=sys.stderr)
        if failed or not report_ok:
            again = f" (on another day add{resume})" if resume else ""
            print(f"Run the same command again to retry what failed{again}.", file=sys.stderr)
            status = 1
    except (KeyboardInterrupt, Interrupted):
        ctx.runner.stop_all()
        again = f" (on another day add{resume})" if resume else ""
        print(f"\nInterrupted. What finished is kept; run the same command again to resume{again}.",
              file=sys.stderr)
        status = 130
    except (RuntimeError, OSError) as exc:
        ctx.runner.stop_all()
        print(f"ERROR: {exc}", file=sys.stderr)
        status = 1
    finally:
        # a second signal must not cut the cleaning short
        ignored = {s: signal.signal(s, signal.SIG_IGN) for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
        try:
            ctx.runner.stop_all()
            remove_worktree(ctx.worktree)
            shutil.rmtree(ctx.tmp, ignore_errors=True)
        finally:
            signal.signal(signal.SIGINT, ignored[signal.SIGINT])
            for s, h in old_handlers.items():
                signal.signal(s, h)
    changes = tree_changes(before, tree_state(ctx.report_path.parent))
    if changes:
        note = ("Luciano's tree changed during the run. It may be his own work, or a call that broke "
                "its rules:\n" + "\n".join(f"  - {c}" for c in changes))
        print(f"WARNING: {note}", file=sys.stderr)
        if ctx.report_path.exists():
            with open(ctx.report_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n## Note written by the script\n\n{note}\n")
        status = status or 1
    return status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
