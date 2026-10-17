"""Step 3h (record/IA/code-follows-2026-10-16/prompt-tables-cut.md): the bridge strict on `Maybe`
(D-2026-10-16-h item 14), a refuted law run past only by naming it (item 16), the records of
`.run.lut` files tracked under examples/ and ignored under tests/ (item 8), and a run cut by its
time limit or its fuel recorded as not finished (the coordinator's answer to 3g's question).
Written 2026-10-17 by Claude Opus 5.5, an agent of the coordinating session."""
import json
import subprocess
import uuid
from pathlib import Path

import pytest

from luthier import host, tables
from luthier.cli import main
from luthier.run import RunError, record_path, results_path, run

ROOT = Path(__file__).resolve().parents[1]


def _last(path):
    return json.loads(record_path(path).read_text(encoding="utf-8"))[-1]


# ---------------------------------------------------------------- the strict Maybe (item 14)

def _maybe_program(tmp_path, monkeypatch):
    """A host module whose functions give a bare value, None, Just and NOTHING where `Maybe String`
    is declared, and a run that reads each by the entry named."""
    module = f"maybe_host_{uuid.uuid4().hex[:8]}"
    (tmp_path / f"{module}.py").write_text(
        "from luthier import host\n"
        "def bare(u):\n    return 'x'\n"
        "def none(u):\n    return None\n"
        "def wrapped(u):\n    return host.Just('x')\n"
        "def empty(u):\n    return host.NOTHING\n", encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))
    lines = [f'{n} (u : Unit) : Maybe String := extern "python:{module}.{n}" u'
             for n in ("bare", "none", "wrapped", "empty")]
    lines += [f'{n}Main : String := match {n} unit {{ just s -> s ; nothing -> "nothing" }}'
              for n in ("bare", "none", "wrapped", "empty")]
    path = tmp_path / "maybe.run.lut"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


@pytest.mark.parametrize("checked", [True, False])
def test_a_bare_value_at_a_maybe_is_refused(tmp_path, monkeypatch, checked):
    path = _maybe_program(tmp_path, monkeypatch)
    for entry in ("bareMain", "noneMain"):
        with pytest.raises(RunError, match="where a Maybe is declared: a Maybe crosses as host.Just or host.NOTHING"):
            run(path, main=entry, checked=checked)


def test_just_and_nothing_cross(tmp_path, monkeypatch):
    path = _maybe_program(tmp_path, monkeypatch)
    assert run(path, main="wrappedMain", checked=True)[2]["result_store"]["value"] == '"x"'
    assert run(path, main="emptyMain", checked=True)[2]["result_store"]["value"] == '"nothing"'


def test_tables_gives_just_or_nothing():
    t = tables.parse("a:int\n1\n")
    assert isinstance(t, host.Just) and t.value.cell("a", 0) == host.Just(("int", 1))
    assert t.value.cell("b", 0) is host.NOTHING
    assert tables.parse("a:real\n1\n") is host.NOTHING


# ---------------------------------------------------------------- a refuted law, run past by name (item 16)

THEORY = "Counter : { next : Int -> Int }\nGrows (c : Counter) (x : Int) : Bool := c.next x > x\nCounter := Grows\n"
MODEL = 'import "counter.lth" Counter\nstuck : Counter := { next := fn x { x } }\n'
LAWS = """import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "counter.lth" Counter Grows
import "counter_model.lut" stuck
models : List Counter := [stuck]
xs : List Int := [0, 1]
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
test "Grows" ExhaustiveMode (seed <- 1) (whereBindings <- [bind "c" "models", bind "x" "xs"])
"""
USE = 'import "counter_model.lut" stuck\nmain : Int := stuck.next 41 + 1\n'


@pytest.fixture
def refuted(tmp_path, capsys):
    """A model whose law `Grows` its store refutes (at x = 0), and a run whose cone holds it."""
    for name, text in (("counter.lth", THEORY), ("counter_model.lut", MODEL), ("counter_laws.test.lut", LAWS),
                       ("use.run.lut", USE)):
        (tmp_path / name).write_text(text, encoding="utf-8")
    assert main(["test", str(tmp_path / "counter_laws.test.lut")]) == 1
    assert "refuted" in capsys.readouterr().out
    return tmp_path / "use.run.lut"


@pytest.mark.parametrize("accept", [[], ["--accept", "assumed"], ["--accept", "assumed:Other"],
                                    ["--accept", "assumed:stuck"]])
def test_a_refuted_law_refuses_the_run_whatever_the_cutoff(refuted, capsys, accept):
    # the control (L9.14): neither the weakest cutoff nor another name lets the run past a failure
    assert main(["run", str(refuted), *accept]) == 1
    err = capsys.readouterr().err
    assert "stuck: Grows: " in err and "run past it as assumed with --accept assumed:Grows" in err
    assert not record_path(refuted).exists()


def test_a_refuted_law_named_runs_as_assumed_warns_and_is_recorded(refuted, capsys):
    for _ in range(2):  # warned at every run (L5.20)
        assert main(["run", str(refuted), "--accept", "assumed:Grows"]) == 0
        out, err = capsys.readouterr()
        assert "warning: running past the refuted law Grows of stuck as assumed (--accept assumed:Grows)" in err
    from luthier.run import read_results
    assert [r["value"] for r in read_results(refuted)] == ["42"]
    entry = _last(refuted)
    assert entry["demand"]["assumes"] == ["Grows"]
    [assumed] = [a for a in entry["certification"]["assumed"] if a.get("law") == "Grows"]
    assert (assumed["name"], assumed["grade"], assumed["accept"], assumed["downstream"]) == (
        "stuck", "assumed", "assumed:Grows", ["main"])
    assert "x = 0" in assumed["refuted"]
    assert entry["certification"]["not certified"] == ["stuck"]
    assert entry["certification"]["states"]["failed"] == 1


# ---------------------------------------------------------------- item 8: the records under git

@pytest.mark.parametrize("path, ignored", [
    ("examples/sonolocalizacion/experiment_zero.run.json", False),
    ("examples/sonolocalizacion/experiment_zero.results.json", False),
    ("examples/hello.run.json", False),
    ("tests/run/table_cell.run.json", True),
    ("tests/run/table_cell.results.json", True),
])
def test_records_tracked_under_examples_and_ignored_under_tests(path, ignored):
    result = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-q", "--no-index", path])
    assert result.returncode == (0 if ignored else 1)


# ---------------------------------------------------------------- the cut run

SPIN = "spin (k : Int) : Int := if k < 0 then k else spin (k + 1)\nmain : Int := spin 0\n"


@pytest.mark.parametrize("args, reason", [(["--time-limit", "0.3"], "time limit"), (["--fuel", "5000"], "fuel")])
def test_a_cut_run_is_recorded_as_not_finished_and_never_served(tmp_path, capsys, args, reason):
    path = tmp_path / "spin.run.lut"
    path.write_text(SPIN, encoding="utf-8")
    assert main(["run", str(path), *args]) == 1
    err = capsys.readouterr().err
    assert ("time limit of 0.3 s reached after" if reason == "time limit" else "fuel spent") in err
    entry = _last(path)
    assert entry["finished"] is False and "output" not in entry
    assert entry["cut"]["reason"] == reason and entry["cut"]["steps"] > 0
    assert entry["demand"]["entry"] == "main"
    assert entry["demand"]["timeLimit" if reason == "time limit" else "fuel"] == (0.3 if reason == "time limit" else 5000)
    assert entry["fuel"]["spent"] == entry["cut"]["steps"]
    # nothing written to the store of results, and nothing served from it after
    assert entry["result_store"] == {"pure": True, "fresh": False, "written": None}
    assert not results_path(path).exists()
    assert main(["run", str(path), *args]) == 1
    runs = json.loads(record_path(path).read_text(encoding="utf-8"))
    assert [r.get("finished") for r in runs] == [False, False]
    assert not results_path(path).exists()


def test_a_cut_run_is_no_breach_of_determined():
    # one demand, finished once and cut once: the cut run has no output and enters no pair
    from luthier.run import breaches
    d = {"entry": "main", "timeLimit": 1.0}
    runs = [{"demand": d, "output": "3\n"}, {"demand": d, "finished": False, "cut": {"reason": "time limit"}},
            {"demand": d, "output": "3\n"}]
    assert breaches(runs) == []
    assert breaches(runs + [{"demand": d, "output": "4\n"}]) == [(0, 3), (2, 3)]
