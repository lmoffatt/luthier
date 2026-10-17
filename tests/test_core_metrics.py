"""Tests of scripts/core_metrics.py: each of the four counts on a fixture of three small files."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "core_metrics.py"
spec = importlib.util.spec_from_file_location("core_metrics", SCRIPT)
core_metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core_metrics)

A = """\
shared : Int := 1
T : { size : Int }
T := lawA
lawA (m : T) : Bool := m.size == m.size
orphan : Bool := true
double (x : Int) : Int := x + x
"""
B = """\
shared : Int := 2
allEven (xs : List Int) : Bool := match xs { nil -> true ; cons x rest -> allEven rest }
"""
C = """\
size (xs : List Int) : Int := match xs { nil -> 0 ; cons x rest -> 1 + size rest }
"""


D = """\
shared : Int := 3
mine : Int := 4
double (x : Int) : Int := x
"""


def fixture(tmp_path):
    for name, text in (("a.lth", A), ("b.lth", B), ("c.lut", C), ("d.test.lut", D)):
        (tmp_path / name).write_text(text)
    return core_metrics.measure(["."], tmp_path)


def test_homonyms(tmp_path):
    assert fixture(tmp_path)["homonyms"] == {"shared": ["a.lth", "b.lth"]}


def test_executive_names_shadowing_are_apart(tmp_path):
    m = fixture(tmp_path)
    assert m["shadows"] == ["d.test.lut: double (also in a.lth)", "d.test.lut: shared (also in a.lth, b.lth)"]
    assert "d.test.lut" not in str(m["homonyms"]) and not any("mine" in x for x in m["shadows"])


def test_accepted_homonyms_are_left_out(tmp_path, monkeypatch):
    monkeypatch.setitem(core_metrics.ACCEPTED_HOMONYMS, "shared", "the language requires it")
    assert fixture(tmp_path)["homonyms"] == {}


def test_list_helpers(tmp_path):
    assert fixture(tmp_path)["helpers"] == ["b.lth: allEven", "c.lut: size"]


def test_unclaimed(tmp_path):
    assert fixture(tmp_path)["unclaimed"] == ["a.lth:5: orphan", "b.lth:2: allEven"]


def test_loose_real_and_the_rest(tmp_path):
    m = fixture(tmp_path)
    assert sorted(x.split(": ")[1] for x in m["loose_real"]) == ["allEven", "double"]
    assert sorted(x.split(": ")[1] for x in m["loose_rest"]) == ["lawA", "size"]


def test_command_prints_the_counts(tmp_path):
    fixture(tmp_path)
    out = subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "a.lth")], capture_output=True, text=True, check=True).stdout
    assert [l.split(" (")[0] for l in out.splitlines()] == ["homonyms 0", "executive names shadowing 0", "list helpers 0", "unclaimed 1", "loose 2"]
