"""scripts/link_ideas.py and scripts/distill_principles.py with a stub in place of the `claude`
command line. The stub answers from the prompt it receives, records every call, and can answer
wrongly once (STUB_BAD_ONCE) to exercise the checks and the retry with the errors appended."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = ROOT / "scripts" / "link_ideas.py"
DISTILL = ROOT / "scripts" / "distill_principles.py"

STUB = r'''#!PYTHON
import json, os, re, sys
from pathlib import Path
if "--version" in sys.argv:
    print("9.9.9 (stub)")
    sys.exit(0)
prompt = sys.stdin.read()
log = Path(os.environ["STUB_LOG"])
with log.open("a", encoding="utf-8") as f:
    f.write(json.dumps({"argv": sys.argv[1:], "prompt": prompt, "thinking": os.environ.get("MAX_THINKING_TOKENS", "")}) + "\n")
bad_marker = Path(os.environ["STUB_LOG"] + ".bad")
bad = os.environ.get("STUB_BAD_ONCE") and not bad_marker.exists()
if bad:
    bad_marker.write_text("x")

if prompt.startswith("# Prompt: link_ideas_v"):
    ex = prompt.split("## Existing lineages")[1].split("## Rows to place")[0]
    existing = [l.split(" | ")[0] for l in ex.splitlines() if " | " in l]
    rows = [l.split(" | ") for l in prompt.split("## Rows to place")[1].splitlines() if l.count(" | ") >= 5]
    if os.environ.get("STUB_LIMIT") and len(rows) > 2:
        print("API Error: Claude's response exceeded the 32000 output token maximum. To configure this behavior, set the CLAUDE_CODE_MAX_OUTPUT_TOKENS environment variable.")
        sys.exit(0)
    new, assign, unplaced = [], [], []
    target = existing[0] if existing else "L-types-are-concepts"
    if not existing:
        new.append({"id": target, "scope": "language", "statement": "Types are concepts."})
    if any("OTHER" in r[4] for r in rows) and "L-costs-explicit" not in existing:
        new.append({"id": "L-costs-explicit", "scope": "language", "statement": "Costs are explicit."})
    for r in rows:
        if "UNPLACE" in r[4]:
            unplaced.append([r[0], "not about Luthier"])
        elif "OTHER" in r[4]:
            assign.append([r[0], "L-costs-explicit", "states"])
        else:
            rel = "proposes" if r[2] == "model" else ("confirms" if "confirm" in r[3] else "restates")
            assign.append([r[0], target, rel])
    if bad:
        assign = assign[1:]
    print(json.dumps({"new_lineages": new, "assign": assign, "unplaced": unplaced}))
elif prompt.startswith("# Prompt: find_principles_v"):
    blocks = prompt.split("## Input")[1].split("\n### ")[1:]
    cls, labels, quote, text = [], [], None, None
    for k, b in enumerate(blocks):
        lab = b.splitlines()[0].split()[0]
        labels.append(lab)
        cls.append([lab, "candidate", "C1", "recurs"] if k == 0 else [lab, "considered", "", "a smaller idea"])
        for l in b.splitlines():
            m = re.match(r'- (q\d+) \| [^|]+ \| ([^|]+) \| \w+ \| "(.*)"$', l)
            if k == 0 and m and quote is None and m.group(2).strip() not in ("model", "pasted"):
                quote, text = m.group(1), m.group(3)
    if bad:
        text = "words he never said"
    print(json.dumps({"candidates": [{"id": "C1", "harms": ["a larger kernel"],
                                      "strongest": {"axis": "conceptual", "why": "reframes what a type is"},
                                      "also": [], "beats": {"lineage": labels[1], "why": "narrower"},
                                      "statement": "A type is a concept.", "instead_of": "a type as a mere label",
                                      "scope": "language", "lineages": labels[:1], "quote": quote, "quote_text": text}],
                      "classification": cls}))
elif prompt.startswith("# Prompt: match_principles_v1"):
    print(json.dumps({"matches": [{"candidate": "C1", "verdict": "extends", "principle": "P2", "change": "adds types",
                                   "assumption": "a", "guides": ["D-2026-10-06-a"], "conflicts": []}], "against": []}))
elif prompt.startswith("# Prompt: compare_principles_v1"):
    cs = re.findall(r"^- (C\d+):", prompt.split("## List C")[1].split("## List A")[0], re.M)
    first_a = re.search(r"^- ([A-Z]\d+):", prompt.split("## List A")[1], re.M).group(1)
    print(json.dumps({"judgments": [{"candidate": c, "A": [{"item": first_a, "why": "same"}] if k == 0 else [],
                                     "B": [{"item": "P1", "why": "echo"}] if k == 1 else []} for k, c in enumerate(cs)]}))
elif prompt.startswith("# Prompt: naive_principles_v1"):
    rs = re.findall(r"^(r\d+) \| ", prompt.split("## Ideas")[1], re.M)
    rows = ["r999"] if bad else rs[1:3]
    print(json.dumps({"candidates": [{"id": "C1", "statement": "Types are concepts.", "rows": rows},
                                     {"id": "C2", "statement": "Costs are explicit.", "rows": rs[-2:-1]}]}))
elif prompt.startswith("# Prompt: recall_principles_v1"):
    print(json.dumps({"candidates": [{"id": "C1", "statement": "Readability counts."},
                                     {"id": "C2", "statement": "Your part stays discernible."}]}))
else:
    print("?")
'''


def rows_fixture():
    return [
        {"id": "dialogue:aaaa:paths", "time_utc": "2026-05-29T17:00:30Z", "time_local": "2026-05-29 14:00:30",
         "who": "model", "kind": "proposal", "what": "A path between implementations.", "quote": "podrías definir un Path",
         "source": "t.md turn 2", "extractor": "dialogue"},
        {"id": "note:2026-05-29T14.03.24:tipos", "time_utc": "2026-05-29T17:03:39Z", "time_local": "2026-05-29 14:03:39",
         "who": "Luciano", "kind": "idea", "what": "Types are concepts.", "quote": "los tipos tienen que ser conceptos",
         "source": "n.md [00:15]", "extractor": "note"},
        {"id": "day:2026-05-29:tipos", "time_utc": "2026-05-29T17:03:39Z", "time_local": "2026-05-29 14:03:39",
         "who": "Luciano", "kind": "idea", "what": "Types are concepts.", "quote": "los tipos tienen que ser conceptos",
         "source": "n.md [00:15]", "extractor": "day"},
        {"id": "dialogue:aaaa:ok", "time_utc": "2026-05-29T17:10:00Z", "time_local": "2026-05-29 14:10:00",
         "who": "Luciano", "kind": "confirmation of turn 2", "what": "He accepts the paths.", "quote": "dale, eso",
         "source": "t.md turn 3", "extractor": "dialogue"},
        {"id": "note:2026-05-30T10.00.00:costs", "time_utc": "2026-05-30T13:00:00Z", "time_local": "2026-05-30 10:00:00",
         "who": "Luciano", "kind": "idea", "what": "OTHER: every cost is explicit.", "quote": "los costos tienen que ser explicitos",
         "source": "c.md [00:05]", "extractor": "note"},
        {"id": "dialogue:aaaa:weather", "time_utc": "2026-06-01T10:00:00Z", "time_local": "2026-06-01 07:00:00",
         "who": "Luciano", "kind": "idea", "what": "UNPLACE the weather today.", "quote": "va a llover",
         "source": "t.md turn 9", "extractor": "dialogue"},
    ]


def setup(tmp_path: Path, rows=None):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    stub = bin_dir / "claude"
    stub.write_text(STUB.replace("PYTHON", sys.executable), encoding="utf-8")
    stub.chmod(0o755)
    tl = tmp_path / "timeline.jsonl"
    tl.write_text("".join(json.dumps(r) + "\n" for r in (rows or rows_fixture())), encoding="utf-8")
    env = dict(os.environ)
    env.update(PATH=f"{bin_dir}{os.pathsep}{env.get('PATH', '')}", STUB_LOG=str(tmp_path / "calls.jsonl"))
    env.pop("STUB_BAD_ONCE", None)
    return tl, env


def calls(tmp_path):
    p = tmp_path / "calls.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def link(tmp_path, env, *args):
    return subprocess.run([sys.executable, str(LINK), "--timeline", str(tmp_path / "timeline.jsonl"),
                           "--output-dir", str(tmp_path / "out"), "--cli", "claude", *args],
                          capture_output=True, text=True, env=env)


def test_link_places_every_row_in_windows_and_computes_who_said_it_first(tmp_path):
    tl, env = setup(tmp_path)
    r = link(tmp_path, env, "--window-chars", "300")
    assert r.returncode == 0, r.stderr
    state = json.loads((tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.json").read_text())
    assert set(state["assign"]) | set(state["unplaced"]) == {x["id"] for x in rows_fixture()}
    assert state["unplaced"]["dialogue:aaaa:weather"]["reason"] == "not about Luthier"
    assert sorted(state["lineages"]) == ["L-costs-explicit", "L-types-are-concepts"]
    cs = calls(tmp_path)
    assert len(cs) == len(state["calls"]) >= 2
    assert all(c["argv"][c["argv"].index("--tools") + 1] == "" and "--no-session-persistence" in c["argv"] for c in cs)
    assert all(c["argv"][c["argv"].index("--effort") + 1] == "low" for c in cs)
    assert "(none yet)" in cs[0]["prompt"] and "L-types-are-concepts | language | 2026-05-29" in cs[1]["prompt"]
    assert all(c["input_sha256"] and c["accepted"] and c["attempts"][0]["answer_sha256"] for c in state["calls"])
    md = (tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.md").read_text()
    assert "first 2026-05-29 14:00 by model; 4 rows, 3 witnesses, 1 days" in md  # note+day of one utterance: one witness
    assert "taken up by Luciano 2026-05-29" in md
    assert "First said by a model and then taken up by Luciano: 1." in md
    assert "- not about Luthier (1)" in md


def test_link_is_incremental_and_pinned_to_its_prompt(tmp_path):
    tl, env = setup(tmp_path)
    assert link(tmp_path, env).returncode == 0
    n = len(calls(tmp_path))
    r = link(tmp_path, env)
    assert r.returncode == 0 and len(calls(tmp_path)) == n and "pending: 0" in r.stdout
    rows = rows_fixture() + [{"id": "note:2026-06-02T10.00.00:tipos2", "time_utc": "2026-06-02T13:00:00Z",
                              "time_local": "2026-06-02 10:00:00", "who": "Luciano", "kind": "idea",
                              "what": "Types again.", "quote": "un tipo es un concepto", "source": "m.md [00:01]",
                              "extractor": "note"}]
    tl.write_text("".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")
    r = link(tmp_path, env)
    assert r.returncode == 0 and len(calls(tmp_path)) == n + 1 and "pending: 1" in r.stdout
    assert "L-types-are-concepts" in calls(tmp_path)[-1]["prompt"].split("## Rows to place")[0]
    (tmp_path / "edited").mkdir()
    other = tmp_path / "edited" / "link_ideas_v1.md"  # same prompt id, other content
    other.write_text((ROOT / "prompts" / "link_ideas_v1.md").read_text() + "\nchanged\n")
    r = link(tmp_path, env, "--prompt", str(other))
    assert r.returncode == 2 and "--force starts over" in r.stderr


def test_link_rejects_a_bad_answer_and_asks_again_with_the_errors(tmp_path):
    tl, env = setup(tmp_path)
    env["STUB_BAD_ONCE"] = "1"
    r = link(tmp_path, env)
    assert r.returncode == 0, r.stderr
    state = json.loads((tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.json").read_text())
    att = state["calls"][0]["attempts"]
    assert len(att) == 2 and "rows of the window not placed" in att[0]["errors"][0] and att[1]["errors"] == []
    assert "## Your previous answer was rejected" in calls(tmp_path)[1]["prompt"]
    assert len(state["assign"]) + len(state["unplaced"]) == 6


PRINCIPLES = """# Principles

```
P1  Luciano's part stays discernible.
Quote:      "x"
Status:     current

P2  Everything derived carries how it was derived.
Quote:      "y"
Status:     current
```
"""
DECISIONS = """# Decisions

D-2026-10-06-a  First.
Kind:       principle. For P1
Status:     current
"""
FIND = ROOT / "scripts" / "find_principles.py"
MATCH = ROOT / "scripts" / "match_principles.py"
COMPARE = ROOT / "scripts" / "compare_principles.py"


def find(tmp_path, env, *args):
    return subprocess.run([sys.executable, str(FIND), "--lineages", str(tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.json"),
                           "--timeline", str(tmp_path / "timeline.jsonl"), "--output-dir", str(tmp_path / "dist"),
                           "--cli", "claude", "--date", "2026-01-02", "--var", "language=Luthier",
                           "--var", "designers=Luciano Moffatt", *args], capture_output=True, text=True, env=env)


def test_find_is_blind_checks_its_quotes_and_fills_in_whose_words(tmp_path):
    tl, env = setup(tmp_path)
    assert link(tmp_path, env).returncode == 0
    env["STUB_BAD_ONCE"] = "1"
    (tmp_path / "calls.jsonl.bad").unlink(missing_ok=True)
    (tmp_path / "calls.jsonl").unlink()
    r = find(tmp_path, env, "--redact", "tipos=TYPES")
    assert r.returncode == 0, r.stderr
    run = json.loads((tmp_path / "dist" / "2026-01-02_find_principles_v2_claude-code_opus.json").read_text())
    assert len(run["attempts"]) == 2 and any("quote_text is not in" in e for e in run["attempts"][0]["errors"])
    prompt = calls(tmp_path)[0]["prompt"]
    body = prompt.split("## Input")[1]
    # blind: nothing of the principles, the log or the objectives; no counts; names redacted
    for absent in ("Principles in force", "Decision log", "Ledger", "objectives", "rows:", "witnesses",
                   "type carries", "certificate", "P13"):
        assert absent not in prompt, absent
    assert "Luthier" in prompt.split("## Input")[0] and "TYPES" in body and "los tipos" not in body
    assert run["answer"]["candidates"][0]["quote_row"] in ("day:2026-05-29:tipos", "note:2026-05-29T14.03.24:tipos")
    md = (tmp_path / "dist" / "2026-01-02_find_principles_v2_claude-code_opus.md").read_text()
    assert "-- from the rows, by the script" in md and "Said by:    Luciano" in md
    assert "Strongest:  conceptual. reframes what a type is" in md and "Harms:      a larger kernel" in md
    assert "Instead of: a type as a mere label" in md
    assert "## Considered and left out" in md and "`L-costs-explicit`" in md
    r = find(tmp_path, env)
    assert r.returncode == 2 and "--force redoes it" in r.stderr


def test_match_sets_the_blind_candidates_against_what_is_in_force(tmp_path):
    tl, env = setup(tmp_path)
    assert link(tmp_path, env).returncode == 0 and find(tmp_path, env).returncode == 0
    (tmp_path / "principles.md").write_text(PRINCIPLES)
    (tmp_path / "decisions.md").write_text(DECISIONS)
    (tmp_path / "objectives.md").write_text("# Objectives\n\n1. Be useful.\n")
    r = subprocess.run([sys.executable, str(MATCH), "--found", str(tmp_path / "dist" / "2026-01-02_find_principles_v2_claude-code_opus.json"),
                        "--principles", str(tmp_path / "principles.md"), "--decisions", str(tmp_path / "decisions.md"),
                        "--objectives", str(tmp_path / "objectives.md"), "--output-dir", str(tmp_path / "dist"),
                        "--cli", "claude", "--date", "2026-01-02"], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    prompt = calls(tmp_path)[-1]["prompt"]
    assert "## Principles in force" in prompt and "## Ledger" in prompt and "### C1" in prompt
    md = (tmp_path / "dist" / "2026-01-02_match_principles_v1_claude-code_opus.md").read_text()
    assert "C1  A type is a concept." in md and "Against:    extends P2: adds types" in md
    assert "Would have guided (for P13, later): D-2026-10-06-a" in md and "Mark:" in md


def test_find_and_match_checks():
    sys.path.insert(0, str(ROOT / "scripts"))
    import find_principles as fp
    import match_principles as mp
    der = {"L-a": {"members": [{"id": "r1"}]}, "L-b": {"members": [{"id": "r2"}]}}
    cand = {"id": "C1", "statement": "s", "scope": "language", "lineages": ["L-a"], "harms": [],
            "strongest": {"axis": "emotive", "why": "w"}, "also": [], "beats": {"lineage": "L-b", "why": "n"},
            "quote_label": "q1", "quote_row": "r1", "quote": "los tipos ... conceptos"}
    good = {"classification": [{"lineage": "L-a", "label": "l1", "verdict": "candidate", "candidate": "C1"},
                               {"lineage": "L-b", "label": "l2", "verdict": "considered", "candidate": None}],
            "candidates": [cand]}
    qtext = {"q1": "los tipos tienen que ser conceptos"}
    assert fp.check_answer(good, der, qtext, 7) == []
    assert any("instead_of is missing" in e for e in fp.check_answer(good, der, qtext, 7, needs_alternative=True))
    bad = json.loads(json.dumps(good))
    bad["candidates"][0].update(quote="conceptos ... los tipos", harms=None, also=[{}, {}, {}],
                                strongest={"axis": "popular", "why": ""}, beats={"lineage": "L-a", "why": "x"}, scope="x")
    errs = "\n".join(fp.check_answer(bad, der, qtext, 0))
    for e in ("1 candidates; at most 0", "quote_text is not in q1", "strongest needs", "also is at most 2",
              "harms must be a list", "beats must name", "scope 'x'"):
        assert e in errs, e
    principles, decisions = {"P1": {}}, {"D-2026-10-06-a": {}}
    m = {"matches": [{"candidate": "C1", "verdict": "extends", "principle": "P9", "change": "", "assumption": "",
                      "guides": ["D-x"], "conflicts": [{"principle": "P7"}]}], "against": [{"principle": "P3", "evidence": ["C9"]}]}
    errs = "\n".join(mp.check(m, {"C1": {}, "C2": {}}, principles, decisions))
    for e in ("names 'P9'", "extends without a change", "empty assumption", "guides 'D-x'", "conflicts with",
              "C2: matched 0 times", "against: 'P3'", "evidence 'C9'"):
        assert e in errs, e


def test_compare_scores_hits_and_leaks_without_telling_the_judge_which_list_is_which(tmp_path):
    tl, env = setup(tmp_path)
    ref = tmp_path / "reference.md"
    ref.write_text("# Reference\n\n- Z7 Readability counts.\n- Z2 Explicit is better than implicit.\n")
    r = subprocess.run([sys.executable, str(COMPARE), "--reference", str(ref), "--recall", "--var", "language=Python",
                        "--var", "designers=Guido van Rossum", "--cli", "claude", "--date", "2026-01-02"],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    judge = calls(tmp_path)[-1]["prompt"]
    assert "## List A" in judge and "## List B" in judge and "reference" not in judge.lower().split("## input")[1]
    assert "Luthier" not in judge.split("## Input")[1].split("## List B")[0]
    run = json.loads((tmp_path / "2026-01-02_recall_compare_principles_v1_claude-code_opus.json").read_text())
    assert run["score"] == {**run["score"], "candidates": 2, "hits": 1, "leaks": 1, "neither": 0, "passes": False}
    md = (tmp_path / "2026-01-02_recall_compare_principles_v1_claude-code_opus.md").read_text()
    assert "| 2 | 1 | 1 | 0 | no |" in md and "states reference Z7" in md and "echoes Luthier P1" in md
    assert "Reference items no candidate states (1 of 2)" in md


def test_link_splits_a_window_whose_answer_hits_the_output_limit(tmp_path):
    tl, env = setup(tmp_path)
    env["STUB_LIMIT"] = "1"
    r = link(tmp_path, env)
    assert r.returncode == 0, r.stderr
    assert "the window is split in two" in r.stderr
    state = json.loads((tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.json").read_text())
    assert len(state["assign"]) + len(state["unplaced"]) == 6
    splits = [c for c in state["calls"] if c["split"]]
    assert splits and all("output limit" in c["attempts"][0]["error"] for c in splits)
    assert all(c["rows"] <= 2 for c in state["calls"] if c["accepted"])


def test_link_refuses_a_timeline_with_repeated_ids_and_passes_the_thinking_cap(tmp_path):
    rows = rows_fixture()
    tl, env = setup(tmp_path, rows + [dict(rows[1])])
    r = link(tmp_path, env)
    assert r.returncode == 2 and "repeats 1 row ids" in r.stderr and calls(tmp_path) == []
    tl.write_text("".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")
    r = link(tmp_path, env, "--max-thinking-tokens", "2000")
    assert r.returncode == 0 and {c["thinking"] for c in calls(tmp_path)} == {"2000"}


def test_link_refuses_a_second_run_on_the_same_state(tmp_path):
    import fcntl
    tl, env = setup(tmp_path)
    (tmp_path / "out").mkdir()
    held = open(tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.lock", "w")
    fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
    r = link(tmp_path, env)
    assert r.returncode == 2 and "holds" in r.stderr and calls(tmp_path) == []
    held.close()
    assert link(tmp_path, env).returncode == 0


def test_link_until_a_cutoff_reads_only_earlier_rows(tmp_path):
    tl, env = setup(tmp_path)
    r = link(tmp_path, env, "--until", "2026-05-30T00:00:00Z")
    assert r.returncode == 0, r.stderr
    state = json.loads((tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.json").read_text())
    placed = set(state["assign"]) | set(state["unplaced"])
    assert "dialogue:aaaa:weather" not in placed and "note:2026-05-30T10.00.00:costs" not in placed
    assert state["until"] == "2026-05-30T00:00:00Z"
    assert "2026-06-01" not in "".join(calls(tmp_path)[0]["prompt"].split("## Rows to place")[1:])


NAIVE = ROOT / "scripts" / "naive_principles.py"


def write_reference(tmp_path):
    ref = tmp_path / "reference.md"
    ref.write_text("# Reference\n\n- Z7 Readability counts.\n")
    return ref


def test_naive_shows_every_row_checks_rows_and_feeds_the_judge(tmp_path):
    tl, env = setup(tmp_path)
    env["STUB_BAD_ONCE"] = "1"
    args = [sys.executable, str(NAIVE), "--timeline", str(tl), "--output-dir", str(tmp_path / "naive"), "--cli", "claude",
            "--date", "2026-01-02", "--var", "language=L", "--var", "designers=the designer", "--redact", "tipos=TYPES"]
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    run = json.loads((tmp_path / "naive" / "2026-01-02_naive_principles_v1_claude-code_opus.json").read_text())
    assert len(run["attempts"]) == 2 and any("unknown rows r999" in e for e in run["attempts"][0]["errors"])
    prompt = calls(tmp_path)[0]["prompt"]
    body = prompt.split("## Ideas")[1]
    assert body.count(" | ") == 3 * len(rows_fixture()) and "infectab" not in prompt.lower()
    c1 = run["answer"]["candidates"][0]
    assert c1["quote_row"] == "note:2026-05-29T14.03.24:tipos" and c1["quote"] == "los tipos tienen que ser conceptos"
    assert c1["who"] == "Luciano"
    r = subprocess.run([sys.executable, str(COMPARE), "--reference", str(write_reference(tmp_path)), "--candidates",
                        str(tmp_path / "naive" / "2026-01-02_naive_principles_v1_claude-code_opus.json"),
                        "--cli", "claude", "--date", "2026-01-02"], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    assert r.returncode == 2 and "--force redoes it" in r.stderr
