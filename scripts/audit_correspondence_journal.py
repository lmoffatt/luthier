#!/usr/bin/env python3
"""The first run of the correspondence audit was a Claude Code workflow, not a script. This turns
the journal of such a run into the outputs that scripts/audit_correspondence.py writes, and prints
the appendices of its report.

Why. Decision D-2026-10-06-x made the correspondence audit run at once, and it ran as a workflow
of the Claude Code session 8d5ce152 on 2026-10-06: twelve mappers, twelve skeptics and one report
agent. The session reached its quota while the report agent was starting, so the mappers' and
skeptics' results exist only in the workflow's journal, under
~/.claude/projects/<project>/<session>/subagents/workflows/<run>/journal.jsonl, one JSON object
per line. The script of the audit came after the workflow and reproduces its design; this adapter
gives the workflow's run the same record a run of the script would have, so that both can be
compared unit by unit (the calibration of step 5.3 of the execution plan).

What it writes, under <out-dir>/<date>_correspondence_<version>_<model>/:

  <unit>.map.json      {"meta", "output"}: the mapper's result, as the script writes it
  <unit>.verify.json   {"meta", "output"}: the skeptic's result, with map_sha256 as the script
                       computes it, so the script would take the unit as done
  workflow.js          the workflow script, which holds the prompts the agents read
  workflow.json        the run: id, commit, timestamps, the journal's path and sha256, one entry
                       per agent with its label, tokens, tool calls, duration and state

The meta of each file says what the script's meta says where the two runs can be compared
(audit, version, stage, unit, commit, model, date) and names the workflow where they cannot
(no CLI, no prompt files: the prompts are in workflow.js, cited by its sha256).

What it prints, as Markdown: the counts by direction and status, then appendices A to D in the
shape prompts/audit_correspondence_report_v1.md asks for, one row per mapped entry. Where the
skeptic gave a verdict, the row carries the skeptic's status and severity and says what the
mapper had said when they differ. The Summary and the Bites of the report are not here: a model
writes them from the same files, and the report says which.

Usage:

  python3 scripts/audit_correspondence_journal.py <journal.jsonl> --run <run.json> \\
      --date 2026-10-06 [--commit <sha>] [--model <name>] [--out-dir record/audits] \\
      [--units prompts/audit_correspondence_units_v1.json] [--appendices <file.md>]

<run.json> is the workflow's record in ~/.claude/projects/<project>/<session>/workflows/, which
holds the script, args.head (the commit) and the progress of each agent. --commit and --model
default to what that file says. Exit 0; 2 on a usage error; 1 if a unit of the units file has no
result in the journal (the files of the other units are still written).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = Path(__file__).resolve()
AUDIT = "correspondence"
DEFAULT_VERSION = "v1"
DEFAULT_UNITS = REPO_ROOT / "prompts" / "audit_correspondence_units_v1.json"
DEFAULT_OUT_DIR = REPO_ROOT / "record" / "audits"

# direction -> name of the list in the map's output, as in scripts/audit_correspondence.py
LIST_OF = {"spec": "claims", "impl": "behaviors", "docs": "claims"}

# Prefixes dropped from file references in the appendix tables, to keep the rows readable.
PREFIXES = ("src/luthier/", "docs/semantica/")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value) -> str:
    """Identical to scripts/audit_correspondence.py, so map_sha256 means the same thing."""
    return sha256_bytes(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def git_commit(sha: str) -> tuple[str, str]:
    """The full hash and the subject of a commit, or the given text and '' if git can't tell."""
    try:
        out = subprocess.run(["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%H%x00%s", sha],
                             capture_output=True, text=True, check=True).stdout.strip()
        full, subject = out.split("\x00", 1)
        return full, subject
    except (subprocess.CalledProcessError, ValueError, OSError):
        return sha, ""


def read_journal(path: Path) -> tuple[dict[str, dict], dict[str, dict], list[str]]:
    """agentId -> started line, agentId -> result (parsed), and the labels that failed."""
    started: dict[str, dict] = {}
    results: dict[str, dict] = {}
    failed: list[str] = []
    with path.open(encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{n}: not JSON: {exc}")
            kind = o.get("type")
            if kind == "started":
                started[o["agentId"]] = o
            elif kind == "result":
                r = o.get("result")
                if isinstance(r, str):
                    try:
                        r = json.loads(r)
                    except json.JSONDecodeError:
                        raise SystemExit(f"{path}:{n}: the result of {o.get('agentId')} is not JSON")
                results[o["agentId"]] = r
            elif kind == "failed":
                failed.append(started.get(o.get("agentId"), {}).get("label", o.get("agentId", "?")))
    return started, results, failed


def by_label(started: dict[str, dict], results: dict[str, dict]) -> dict[str, tuple[str, dict]]:
    """'map <unit>' / 'verify <unit>' -> (agentId, result)."""
    out = {}
    for agent, r in results.items():
        label = started.get(agent, {}).get("label")
        if label:
            out[label] = (agent, r)
    return out


def progress_of(run: dict) -> dict[str, dict]:
    return {p["agentId"]: p for p in run.get("workflowProgress", []) if p.get("type") == "workflow_agent"}


def iso(ms: int | None) -> str | None:
    if not ms:
        return None
    return dt.datetime.fromtimestamp(ms / 1000, tz=dt.timezone.utc).isoformat(timespec="seconds")


def cell(text) -> str:
    """One table cell: one line, pipes escaped, whitespace collapsed."""
    if text is None:
        return ""
    if isinstance(text, (list, tuple)):
        text = "; ".join(str(t) for t in text)
    s = str(text)
    for p in PREFIXES:
        s = s.replace(p, "")
    s = re.sub(r"\s+", " ", s).strip()
    return s.replace("|", "\\|")


def resolve(entry: dict, verdict: dict | None) -> tuple[str, str, str]:
    """(status, severity, verdict text) of a row: the skeptic's where there is one."""
    status = entry.get("status", "")
    severity = entry.get("severity", "")
    if verdict is None:
        return status, severity, "not verified"
    v = verdict.get("verdict", "")
    c_status = verdict.get("corrected_status") or status
    c_sev = verdict.get("corrected_severity") or severity
    note = []
    if c_status != status:
        note.append(f"mapper: {status}")
    if c_sev != severity:
        note.append(f"mapper severity: {severity}")
    text = v if not note else f"{v} ({', '.join(note)})"
    return c_status, c_sev, text


def table(direction: str, entries: list[dict], verdicts: dict[str, dict]) -> list[str]:
    if direction == "impl":
        head = "| Id | Behavior | Status | Code | Specification | Test | Severity | Verdict |"
    else:
        head = "| Id | Claim | Status | Specification | Code | Test | Severity | Verdict |"
    lines = [head, "|---|---|---|---|---|---|---|---|"]
    for e in entries:
        status, sev, vtext = resolve(e, verdicts.get(e.get("id")))
        text = e.get("claim") if direction != "impl" else e.get("behavior")
        spec = e.get("spec_ref")
        code = e.get("impl_refs") if direction != "impl" else e.get("impl_ref")
        tests = e.get("test_refs") or "none"
        if direction == "impl":
            mid = f"{cell(text)} | {cell(status)} | {cell(code)} | {cell(spec)}"
        else:
            mid = f"{cell(text)} | {cell(status)} | {cell(spec)} | {cell(code)}"
        lines.append(f"| {cell(e.get('id'))} | {mid} | {cell(tests)} | {cell(sev)} | {cell(vtext)} |")
    return lines


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("journal", type=Path)
    ap.add_argument("--run", type=Path, required=True, help="the workflow's run record (wf_*.json)")
    ap.add_argument("--date", required=True, help="date of the run, YYYY-MM-DD, used in the output names")
    ap.add_argument("--commit", help="commit audited; default: args.head of the run record")
    ap.add_argument("--model", help="model of the agents; default: defaultModel of the run record")
    ap.add_argument("--version", default=DEFAULT_VERSION)
    ap.add_argument("--units", type=Path, default=DEFAULT_UNITS)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--appendices", type=Path, help="write the Markdown here instead of stdout")
    args = ap.parse_args(argv)

    if not args.journal.is_file():
        print(f"journal not found: {args.journal}", file=sys.stderr)
        return 2
    if not args.run.is_file():
        print(f"run record not found: {args.run}", file=sys.stderr)
        return 2
    run = json.loads(args.run.read_text(encoding="utf-8"))
    cfg = json.loads(args.units.read_text(encoding="utf-8"))
    units = cfg["units"]
    commit_arg = args.commit or (run.get("args") or {}).get("head")
    if not commit_arg:
        print("no commit: give --commit or a run record with args.head", file=sys.stderr)
        return 2
    sha, subject = git_commit(commit_arg)
    model = args.model or run.get("defaultModel") or "unknown"
    journal_sha = sha256_bytes(args.journal.read_bytes())
    script_text = run.get("script", "")
    script_sha = sha256_bytes(script_text.encode("utf-8"))
    this_sha = sha256_bytes(SCRIPT.read_bytes())

    started, results, failed = read_journal(args.journal)
    labelled = by_label(started, results)
    progress = progress_of(run)

    tag = f"{args.date}_{AUDIT}_{args.version}_{model}"
    unit_dir = args.out_dir / tag
    unit_dir.mkdir(parents=True, exist_ok=True)

    def meta(stage: str, unit: dict, agent: str) -> dict:
        p = progress.get(agent, {})
        return {
            "audit": AUDIT, "version": args.version, "stage": stage,
            "commit": sha, "model": model,
            "unit": {k: unit[k] for k in ("label", "direction", "files")},
            "run": "claude-code-workflow",
            "run_id": run.get("runId"), "session": args.journal.resolve().parents[3].name,
            "agent_id": agent, "agent_label": started.get(agent, {}).get("label"),
            "started_at": iso(p.get("startedAt")), "finished_at": iso(p.get("lastProgressAt")),
            "tokens": p.get("tokens"), "tool_calls": p.get("toolCalls"), "duration_ms": p.get("durationMs"),
            "prompts": {"workflow.js": script_sha},
            "journal_sha256": journal_sha,
            "units_file": rel(args.units), "units_sha256": sha256_bytes(args.units.read_bytes()),
            "adapter": rel(SCRIPT), "adapter_sha256": this_sha,
            "date": args.date,
        }

    missing: list[str] = []
    rows_by_unit: dict[str, dict] = {}
    for unit in units:
        label = unit["label"]
        m = labelled.get(f"map {label}")
        v = labelled.get(f"verify {label}")
        if m is None:
            missing.append(label)
            continue
        m_agent, m_out = m
        (unit_dir / f"{label}.map.json").write_text(
            json.dumps({"meta": meta("map", unit, m_agent), "output": m_out}, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8")
        verdicts: dict[str, dict] = {}
        if v is not None:
            v_agent, v_out = v
            vm = meta("verify", unit, v_agent)
            vm["map_sha256"] = sha256_json(m_out)
            (unit_dir / f"{label}.verify.json").write_text(
                json.dumps({"meta": vm, "output": v_out}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            verdicts = {x.get("id"): x for x in v_out.get("verdicts", [])}
        rows_by_unit[label] = {"unit": unit, "entries": m_out.get(LIST_OF[unit["direction"]], []),
                               "verdicts": verdicts, "map_agent": m_agent,
                               "verify_agent": v[0] if v else None}

    (unit_dir / "workflow.js").write_text(script_text, encoding="utf-8")
    agents = []
    for p in run.get("workflowProgress", []):
        if p.get("type") != "workflow_agent":
            continue
        agents.append({k: p.get(k) for k in ("label", "agentId", "model", "state", "tokens", "toolCalls",
                                              "durationMs", "error")}
                      | {"started_at": iso(p.get("startedAt")), "finished_at": iso(p.get("lastProgressAt"))})
    (unit_dir / "workflow.json").write_text(json.dumps({
        "run_id": run.get("runId"), "name": run.get("workflowName"), "status": run.get("status"),
        "timestamp": run.get("timestamp"), "start_time": iso(run.get("startTime")),
        "duration_ms": run.get("durationMs"), "commit": sha, "commit_subject": subject,
        "args": run.get("args"), "default_model": run.get("defaultModel"),
        "total_tokens": run.get("totalTokens"), "total_tool_calls": run.get("totalToolCalls"),
        "logs": run.get("logs"), "script_sha256": script_sha, "script_path_at_the_time": run.get("scriptPath"),
        "journal_path": str(args.journal.resolve()), "journal_sha256": journal_sha,
        "agents": agents, "units_without_result": missing, "failed_agents": failed,
        "adapter": rel(SCRIPT), "adapter_sha256": this_sha,
    }, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- the Markdown ---------------------------------------------------------------------
    out: list[str] = []
    counts: dict[str, dict[str, int]] = {}
    totals = {"mapped": 0, "verified": 0, "confirmed": 0, "refuted": 0, "uncertain": 0}
    per_unit = []
    for label, r in rows_by_unit.items():
        d = r["unit"]["direction"]
        c = counts.setdefault(d, {})
        n = {"mapped": len(r["entries"]), "verified": len(r["verdicts"]),
             "confirmed": 0, "refuted": 0, "uncertain": 0}
        for e in r["entries"]:
            status, _, _ = resolve(e, r["verdicts"].get(e.get("id")))
            c[status] = c.get(status, 0) + 1
        for vv in r["verdicts"].values():
            k = vv.get("verdict")
            if k in n:
                n[k] += 1
        per_unit.append((label, d, n))
        for k in totals:
            totals[k] += n[k]

    out.append("## Counts by direction and status")
    out.append("")
    out.append("The status is the skeptic's where the entry was verified, the mapper's otherwise.")
    out.append("")
    for d, name in (("spec", "Specification to implementation"), ("impl", "Implementation to specification"),
                    ("docs", "Documentation")):
        if d not in counts:
            continue
        out.append(f"### {name}")
        out.append("")
        out.append("| Status | Entries |")
        out.append("|---|---|")
        for status, k in sorted(counts[d].items(), key=lambda kv: -kv[1]):
            out.append(f"| {cell(status)} | {k} |")
        out.append("")

    def appendix(title: str, direction: str) -> None:
        out.append(title)
        out.append("")
        out.append("File references drop the prefixes `src/luthier/` and `docs/semantica/`. The status and the "
                   "severity are the skeptic's where the entry was verified; the Verdict column says what the "
                   "mapper had said when they differ, and 'not verified' where the skeptic did not see the entry.")
        out.append("")
        for label, r in rows_by_unit.items():
            if r["unit"]["direction"] != direction:
                continue
            out.append(f"### {label}: {r['unit']['files']}")
            out.append("")
            out.extend(table(direction, r["entries"], r["verdicts"]))
            out.append("")

    appendix("## Appendix A. Specification to implementation", "spec")
    appendix("## Appendix B. Implementation to specification", "impl")
    appendix("## Appendix C. Documentation", "docs")

    out.append("## Appendix D. Counts")
    out.append("")
    out.append("| Unit | Direction | Mapped | Verified | Confirmed | Refuted | Uncertain |")
    out.append("|---|---|---|---|---|---|---|")
    for label, d, n in per_unit:
        out.append(f"| {label} | {d} | {n['mapped']} | {n['verified']} | {n['confirmed']} | {n['refuted']} | "
                   f"{n['uncertain']} |")
    out.append(f"| total | | {totals['mapped']} | {totals['verified']} | {totals['confirmed']} | "
               f"{totals['refuted']} | {totals['uncertain']} |")
    out.append("")
    if missing:
        out.append(f"Units with no result in the journal: {', '.join(missing)}.")
        out.append("")

    text = "\n".join(out)
    if args.appendices:
        args.appendices.write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")
    print(f"wrote {len(rows_by_unit)} units to {rel(unit_dir)}/" + (f"; no result for {missing}" if missing else ""),
          file=sys.stderr)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
