"""`luthier session [files]` (12.S20, 2.S18, 8.S12, 8.S13), from record/IA/v04-2026-10-15/
prompt-session.md: a block one item per line over the files, a bare term printed with its type and
the states of its cone as `eval` prints them, the unused rebinding a note (2.R6), nothing recorded;
the world only with `--world` ([proposed]), its actions performed once and validated at their first
action (10.S10) with no entry written."""
import os
import subprocess
import sys
from pathlib import Path

from luthier import certify

ROOT = Path(__file__).resolve().parents[1]
ARITHMETIC = ROOT / "tests/eval/arithmetic.lut"
HELLO = ROOT / "examples/hello.run.lut"


def session(lines, *args, cwd=None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run([sys.executable, "-m", "luthier.cli", "session", *map(str, args)],
                          input="".join(line + "\n" for line in lines), capture_output=True, text=True,
                          env=env, cwd=cwd)


def test_a_definition_then_a_term_with_no_file():
    # the brief's acceptance: core alone, the session's definition visible to the next line
    r = session(["x := 3", "x + 1"])
    assert r.returncode == 0, r.stdout + r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == "4 : Int"
    assert lines[1].startswith("states of the cone, accepting sampled and above:")
    assert len(lines) == 2  # an item prints nothing


def test_unused_rebinding_is_a_note():
    # v0.4's criterion (b): 2.R6 in a session, reported and not refused
    r = session(["x <- 1", "x <- 2", "x", ":quit"], ARITHMETIC)
    assert r.returncode == 0, r.stdout + r.stderr
    lines = r.stdout.splitlines()
    assert lines[0].startswith("note: unused rebinding of x")
    assert "2.R6" in lines[0]
    assert lines[1] == "2 : Int"
    assert lines[2].startswith("states of the cone")


def test_a_consumed_binding_is_no_note_and_quit_ends():
    r = session(["x <- 1", "x <- x + 1", "x", ":quit", "x <- 5"], ARITHMETIC)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "note" not in r.stdout
    assert r.stdout.splitlines()[0] == "2 : Int"


def test_files_names_and_8S12():
    # the files' names are visible; 8.S12: y depends on the first x and stays 11
    r = session(["x <- 1", "y := x + 10", "x <- 2", "y", "answer + x"], ARITHMETIC)
    assert r.returncode == 0, r.stdout + r.stderr
    values = [l for l in r.stdout.splitlines() if not l.startswith("states")]
    assert values == ["11 : Int", "21 : Int"]


def test_defines_once_and_what_may_be_rebound():
    # 2.R3 and 2.R4: a refused line leaves the block as it was, the session goes on, exit 1
    r = session(["y := 1", "y := 2", "y <- 3", "answer := 4", "answer <- 4", "y"], ARITHMETIC)
    assert r.returncode == 1
    assert r.stdout.splitlines()[0] == "1 : Int"
    errors = r.stderr.splitlines()
    assert len(errors) == 4
    assert "2.R3" in errors[0] and "2.R4" in errors[1] and "2.R3" in errors[2] and "2.R4" in errors[3]


def test_items_lists_the_block_and_a_refused_line_does_not_join():
    r = session(["x := 1", "z := nothere", "p <- (x, 2)", ":items"], ARITHMETIC)
    assert r.returncode == 1
    assert r.stdout.splitlines() == ["x := 1", "p <- (x, 2)"]
    assert "nothere" in r.stderr


def test_records_nothing(tmp_path):
    program = tmp_path / "a.lut"
    program.write_text("answer : Int := 6 * 7\n")
    r = session(["answer"], program, cwd=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.splitlines()[0] == "42 : Int"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.lut"]


def test_no_world_without_the_flag():
    r = session(['(w, u) <- host.print w "hi"'], HELLO)
    assert r.returncode == 1
    assert "--world" in r.stderr
    assert "hi" not in r.stdout


def _stores():
    where = Path(os.environ[certify.LIBRARY_STORES])
    return {p.name: p.read_text() for p in where.glob("*.cert.json")}


def test_world_actions_run_once_validated_and_unrecorded():
    before = _stores()
    r = session(['(w, u) <- host.print w "one"', "1 + 1", '(w, v) <- host.print w "two"', "n := 5", "n"],
                "--world", HELLO)
    assert r.returncode == 0, r.stdout + r.stderr
    lines = [l for l in r.stdout.splitlines() if not l.startswith("states")]
    # validated at its first action (10.S10), then each print printed once, though each line
    # re-evaluates the block so far
    assert lines[0].startswith("note: host.print at its first action (10.S10): HostAgreesPrint")
    assert [l for l in lines if not l.startswith("note")] == ["one", "2 : Int", "two", "5 : Int"]
    assert sum("first action" in l for l in lines) == 2  # the law and the frame law, once
    assert _stores() == before  # [proposed] the session writes no entry


def test_world_read_and_an_unbound_action_is_refused():
    r = session([f'(w, s) <- host.readFile w "{ARITHMETIC}"', "s", 'host.print w "lost"', "1"],
                "--world", HELLO)
    assert r.returncode == 1
    lines = r.stdout.splitlines()
    assert any(l.startswith('just "answer : Int') for l in lines)
    # the action happened and is shown, but the term is refused: an action is an item (10.S2)
    assert "lost" in lines
    assert "10.S2" in r.stderr
    assert lines[-2] == "1 : Int"
