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

if prompt.startswith("# Prompt: link_ideas_v1"):
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
elif prompt.startswith("# Prompt: distill_principles_v1"):
    blocks = prompt.split("## Lineages")[1].split("\n### ")[1:]
    cls, labels, quote, text = [], [], None, None
    for k, b in enumerate(blocks):
        lab = b.splitlines()[0].split()[0]
        labels.append(lab)
        cls.append([lab, "candidate", "C1", "recurs"] if k == 0 else [lab, "considered", "", "a smaller idea"])
        for l in b.splitlines():
            m = re.match(r'- (q\d+) \| [^|]+ \| (\w+) \| \w+ \| "(.*)"$', l)
            if k == 0 and m and quote is None and m.group(2) == "Luciano":
                quote, text = m.group(1), m.group(3)
    if bad:
        text = "words he never said"
    print(json.dumps({"candidates": [{"id": "C1", "harms": [{"consumer": "computation", "how": "a larger kernel"}],
                                      "strongest": {"consumer": "reader", "axis": "conceptual", "why": "reframes what a type is"},
                                      "also": [], "beats": {"lineage": labels[1], "why": "narrower"},
                                      "statement": "A type is a concept.", "scope": "language",
                                      "lineages": labels[:1], "quote": quote, "quote_text": text,
                                      "assumption": "concepts are what a scientist reasons with",
                                      "guides": ["D-2026-10-06-a"], "conflicts": [{"principle": "P2", "how": "x"}]}],
                      "classification": cls, "against": []}))
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
    other = tmp_path / "other_prompt.md"
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


def distill(tmp_path, env, *args):
    (tmp_path / "principles.md").write_text(PRINCIPLES)
    (tmp_path / "decisions.md").write_text(DECISIONS)
    (tmp_path / "objectives.md").write_text("# Objectives\n\n1. Be useful.\n")
    return subprocess.run([sys.executable, str(DISTILL), "--lineages", str(tmp_path / "out" / "lineages_link_ideas_v1_claude-code_opus.json"),
                           "--timeline", str(tmp_path / "timeline.jsonl"), "--principles", str(tmp_path / "principles.md"),
                           "--decisions", str(tmp_path / "decisions.md"), "--objectives", str(tmp_path / "objectives.md"),
                           "--output-dir", str(tmp_path / "dist"), "--cli", "claude", "--date", "2026-01-02", *args],
                          capture_output=True, text=True, env=env)


def test_distill_drafts_candidates_with_the_quote_and_its_author_filled_in(tmp_path):
    tl, env = setup(tmp_path)
    assert link(tmp_path, env).returncode == 0
    env["STUB_BAD_ONCE"] = "1"
    (tmp_path / "calls.jsonl.bad").unlink(missing_ok=True)
    (tmp_path / "calls.jsonl").unlink()
    r = distill(tmp_path, env)
    assert r.returncode == 0, r.stderr
    run = json.loads((tmp_path / "dist" / "2026-01-02_distill_principles_v1_claude-code_opus.json").read_text())
    # the first answer of the run carried a quote that is not in its row
    assert len(run["attempts"]) == 2 and any("the quote is not in row" in e for e in run["attempts"][0]["errors"])
    # the per-day and per-note readings of one utterance tie in time; the id breaks the tie
    assert run["answer"]["candidates"][0]["quote_row"] == "day:2026-05-29:tipos"
    assert len(run["inputs"]) == 5
    assert all(len(v["sha256"]) == 64 for v in run["inputs"].values()) and len(run["input_sha256"]) == 64
    prompt = calls(tmp_path)[0]["prompt"]
    assert "at most 7" in prompt and "## Ledger" in prompt and "### l1 L-types-are-concepts" in prompt
    assert "- q1 | 2026-05-29 14:00 | model | proposes" in prompt
    assert run["quote_labels"]["q2"] == "day:2026-05-29:tipos"
    assert run["lineage_labels"] == {"l1": "L-types-are-concepts", "l2": "L-costs-explicit"}
    assert "rows:" not in prompt.split("## Lineages")[1]  # the counts are not shown to the model
    md = (tmp_path / "dist" / "2026-01-02_distill_principles_v1_claude-code_opus.md").read_text()
    assert "C1  A type is a concept." in md and "Said by:    Luciano, 2026-05-29 14:03" in md
    assert "Source:     n.md [00:15] (row day:2026-05-29:tipos)" in md and "Mark:" in md
    assert "lineages begun by model 1" in md
    assert "-- from the rows, by the script" in md and "-- the model's reading (opus, effort low)" in md
    assert "Strongest:  the person who uses and reads it, conceptual. reframes what a type is" in md
    assert "Harms:      the computation. a larger kernel" in md
    assert "Beats:      L-costs-explicit (Costs are explicit.). narrower" in md
    assert "## Considered and left out" in md and "`L-costs-explicit`" in md and "Would have guided (for P13, later): D-2026-10-06-a" in md
    assert "Finding: infectability" in prompt and "do not choose or\nrank by them" in prompt and "Two kinds of idea" in prompt
    r = distill(tmp_path, env)
    assert r.returncode == 2 and "--force redoes it" in r.stderr


def test_distill_checks(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import distill_principles as dp
    der = {"L-a": {"members": [{"id": "r1", "quote": "los tipos tienen que ser conceptos", "who": "Luciano"}]},
           "L-b": {"members": [{"id": "r2", "quote": "otra cosa", "who": "Luciano"}]}}
    principles = {"P1": {}}
    decisions = {"D-2026-10-06-a": {}}
    cand = {"id": "C1", "statement": "s", "assumption": "a", "scope": "language", "lineages": ["L-a"],
            "harms": [], "strongest": {"consumer": "computation", "axis": "emotive", "why": "w"}, "also": [],
            "beats": {"lineage": "L-b", "why": "narrower"},
            "quote_row": "r1", "quote": "los tipos ... conceptos", "guides": ["D-2026-10-06-a"]}
    good = {"classification": [{"lineage": "L-a", "verdict": "candidate", "candidate": "C1"},
                               {"lineage": "L-b", "verdict": "considered"}],
            "candidates": [cand]}
    assert dp.check_answer(good, der, principles, decisions, 7) == []
    two = json.loads(json.dumps(good))
    two["candidates"].append({**cand, "id": "C2"})
    two["classification"][0] = {"lineage": "L-a", "verdict": "candidate", "candidate": "C1"}
    assert any("C1: above_next is missing" in e for e in dp.check_answer(two, der, principles, decisions, 7))
    bad = json.loads(json.dumps(good))
    bad["classification"] = [{"lineage": "L-x", "verdict": "covered", "principle": "P9"}]
    c = bad["candidates"][0]
    c.update(quote="conceptos ... los tipos", guides=["D-x"], harms=None, also=[{}, {}, {}],
             strongest={"consumer": "writer", "axis": "popular", "why": ""}, beats={"lineage": "L-a", "why": "x"})
    errs = "\n".join(dp.check_answer(bad, der, principles, decisions, 0))
    for e in ("1 candidates; at most 0", "unknown lineage 'L-x'", "principle 'P9'", "lineages not classified: L-a",
              "the quote is not in row r1", "guides 'D-x'", "strongest needs", "also is a list of at most 2",
              "harms must be a list", "beats must name a lineage classified considered"):
        assert e in errs, e
    w = dp.run_warnings({"candidates": [cand, {**cand, "id": "C2"}, {**cand, "id": "C3"}]},
                        "| a | few primitives, the rest derived; one kind of thing where there were several |")
    assert any("strongest axis is emotive" in x for x in w) and any("no candidate names a harm" in x for x in w)
    copy = {**cand, "strongest": {"consumer": "computation", "axis": "aesthetic",
                                  "why": "few primitives, the rest derived; one kind of thing where there were"}}
    assert any("repeats eight words of the table" in x for x in dp.run_warnings({"candidates": [copy]},
               "| a | few primitives, the rest derived; one kind of thing where there were several |"))

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
