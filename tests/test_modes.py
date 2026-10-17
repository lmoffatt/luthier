"""A provisional extern refused unless the demand names it, and the modes of running as fields of
the demand (D-2026-10-16-c, D-2026-10-16-d; world.lth's `AppliedWhenSettled`, demand.lth's
`Demand` and `Ran`). Written 2026-10-16 by Claude Opus 5.5, an agent of the coordinating session,
on record/IA/code-follows-2026-10-16/prompt-modes.md."""
import json
import os
from pathlib import Path

import pytest

from luthier.cli import main
from luthier.run import DEMAND_DEFAULTS, Refused, record_path, run

ROOT = Path(__file__).resolve().parents[1]

# a provisional extern in the cone of an action; "hello, world" so that the first action's
# validation is the one examples/hello.run.lut's runs already keep in world_model.cert.json
SHOUT = ('import "world_model.lut" HostConsole host : HostConsole\n\n'
         'shout : String -> String := extern "python:builtins.str" '
         '(provisional <- "str stands in for a shout not written yet")\n'
         'main (w : W) : W * Unit := host.print w (shout "hello, world")\n')
REASON = "str stands in for a shout not written yet"


def _shout(tmp_path):
    path = tmp_path / "shout.run.lut"
    path.write_text(SHOUT, encoding="utf-8")
    return path


def _last(path):
    return json.loads(record_path(path).read_text(encoding="utf-8"))[-1]


# ---------------------------------------------------------------- provisional externs (D-2026-10-16-c)

def test_a_provisional_not_named_is_refused_with_its_reason(tmp_path):
    with pytest.raises(Refused, match=r"shout: provisional \(" + REASON + r"\); run it as assumed with "
                                      r"--accept assumed:shout") as refusal:
        run(_shout(tmp_path))
    assert refusal.value.refusals == [{"name": "shout", "law": None, "state": ("Provisional", None)}]


def test_a_provisional_named_runs_as_assumed_warns_and_is_recorded(tmp_path, capsys):
    path = _shout(tmp_path)
    assert main(["run", str(path), "--accept", "assumed:shout"]) == 0
    out, err = capsys.readouterr()
    assert out == "hello, world\n"
    # the warning names it and its reason, at its first application
    assert f"warning: applying provisional extern shout as assumed (python:builtins.str): {REASON}" in err
    entry = _last(path)
    assert entry["demand"]["assumes"] == ["shout"]
    assumed = [a for a in entry["certification"]["assumed"] if a["name"] == "shout"]
    # its grade is assumed, and so is that of everything downstream of it
    assert assumed == [{"name": "shout", "provisional": [REASON], "accept": "assumed:shout", "grade": "assumed",
                        "downstream": ["main"]}]
    assert entry["certification"]["not certified"] == []


def test_a_bare_accept_assumed_still_refuses_a_provisional(tmp_path, capsys):
    # the control (L9.14): what lets the named run through is the name, not the cutoff
    path = _shout(tmp_path)
    assert main(["run", str(path), "--accept", "assumed"]) == 1
    err = capsys.readouterr().err
    assert "shout: provisional" in err and "--accept assumed:shout" in err
    assert not record_path(path).exists()


def test_accept_takes_one_grade_and_names(tmp_path, capsys):
    path = _shout(tmp_path)
    assert main(["run", str(path), "--accept", "sampled", "--accept", "cases"]) == 1
    assert "--accept names two grades" in capsys.readouterr().err
    assert main(["run", str(path), "--accept", "assumed:shout", "--accept", "assumed:nobody"]) == 0
    assert "--accept assumed:nobody names no provisional extern of the cone" in capsys.readouterr().err


def test_check_v_lists_the_provisionals_with_their_reasons(tmp_path, capsys):
    path = _shout(tmp_path)
    main(["check", "-v", str(path)])
    assert f"provisional shout: Provisional extern: {REASON}" in capsys.readouterr().out


# ---------------------------------------------------------------- the modes of running (D-2026-10-16-d)

def test_the_default_demand_records_no_fuel_bound_and_fuel_records_its_bound(tmp_path, capsys):
    path = tmp_path / "small.run.lut"
    path.write_text("main : Int := 1 + 2\n", encoding="utf-8")
    assert main(["run", str(path)]) == 0
    assert _last(path)["demand"]["fuel"] is None and _last(path)["fuel"]["given"] is None
    assert main(["run", str(path), "--fuel", "7000", "--fresh"]) == 0
    assert _last(path)["demand"]["fuel"] == 7000 and _last(path)["fuel"]["given"] == 7000


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="about 90 seconds; set LUTHIER_SLOW=1")
def test_no_fuel_bound_by_default_finishes_past_the_old_bound_slow(tmp_path, capsys):
    # the old default cut a run at 10,000,000 steps; this one takes about 10,150,000 (35 a turn)
    path = tmp_path / "count.run.lut"
    path.write_text("count (n : Int) (k : Int) : Int := if k == 0 then n else if n < 0 then 0 "
                    "else count (n + 1) (k - 1)\nmain : Int := count 0 290000\n", encoding="utf-8")
    assert DEMAND_DEFAULTS["fuel"] is None
    assert main(["run", str(path)]) == 0
    entry = _last(path)
    assert entry["demand"]["fuel"] is None and entry["fuel"]["given"] is None
    assert entry["fuel"]["spent"] > 10_000_000


def test_a_time_limit_stops_a_loop_and_says_so(tmp_path, capsys):
    path = tmp_path / "spin.run.lut"
    path.write_text("spin (k : Int) : Int := if k < 0 then k else spin (k + 1)\nmain : Int := spin 0\n",
                    encoding="utf-8")
    assert main(["run", str(path), "--time-limit", "0.5"]) == 1
    assert "time limit of 0.5 s reached after" in capsys.readouterr().err


def test_the_strategy_fresh_and_the_limits_are_recorded_in_the_demand(tmp_path, capsys):
    path = tmp_path / "pure.run.lut"
    path.write_text("main : Int := 1 + 2\n", encoding="utf-8")
    assert main(["run", str(path)]) == 0
    d, plan = _last(path)["demand"], _last(path)["plan"]
    # the defaults declared in demand_model.lut's `theDemand`
    assert (d["strategy"], d["fresh"], d["fuel"], d["timeLimit"], d["assumes"]) == (
        "ForwardOnDemand", False, None, None, [])
    # the record says which strategy ran: call by need, the specimen of forward on demand (`Ran`)
    assert plan["strategy"] == "CallByNeed"
    assert main(["run", str(path), "--strategy", "call-by-need", "--fresh", "--fuel", "5000",
                 "--time-limit", "60"]) == 0
    d, plan = _last(path)["demand"], _last(path)["plan"]
    assert (d["strategy"], d["fresh"], d["fuel"], d["timeLimit"]) == ("CallByNeed", True, 5000, 60.0)
    assert plan["strategy"] == "CallByNeed" and _last(path)["result_store"]["fresh"] is True
