"""Certificates as phase 2 of docs/plan-2026-10-05.md made them (05 §7): what an entry's hash covers
(the code of the cone, the Python behind its externs, the interpreter), when it is compared (after
the whole program is loaded and its holes filled), the three outcomes of a law, the grade of an
enumeration, provisional externs, the case count a directive asks for, pruning, and the record of
a run. Each test writes its own files in a temporary directory."""
import json
import sys

import pytest

from luthier.cli import main, load

sys.setrecursionlimit(50_000)


def write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text)
    return str(p)


def entries(path):
    data = json.loads(open(path).read())
    return {k: (v if isinstance(v, list) else [v]) for k, v in data.items()}


def test_editing_the_python_behind_an_extern_makes_its_certificate_stale(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(tmp_path))
    write(tmp_path, "certext.py", "def double(x):\n    return 2 * x\n")
    lib = write(tmp_path, "lib.lut", 'Even (f : Int -> Int) (x : Int) : Bool := f x mod 2 == 0\n'
                                     'double : { f : Int -> Int | Even f } := extern "python:certext.double"\n'
                                     'test double with 20\n')
    assert main(["test", lib]) == 0
    assert "double" in load([lib]).checker.certified
    write(tmp_path, "certext.py", "def double(x):\n    return x + x\n")
    loader = load([lib])
    assert "double" not in loader.checker.certified
    assert "Python behind" in loader.stale_why["double"]


def test_a_library_with_a_hole_is_certified_per_filling(tmp_path):
    lib = write(tmp_path, "holed.lut", "k : Int\nPositive (x : Int) : Bool := x > 0\n"
                                       "shifted (x : Nat) : { y : Int | Positive y } := x + k\n")
    app = write(tmp_path, "fill.lut", 'import "holed.lut"\nk := 1\n')
    assert main(["test", app, "--imports"]) == 0
    assert "shifted" in load([app]).checker.certified           # the filling the test ran under
    assert "shifted" not in load([lib]).checker.certified       # the library alone is another program


def test_a_law_blocked_by_a_hole_is_not_run_and_not_failed(tmp_path):
    lib = write(tmp_path, "blocked.lut", "k : Int\nAbove (x : Int) : Bool := x + k > x\n"
                                         "a : { u : Unit | \\ (x : Int) { Above x } } := unit\n")
    main(["test", lib])
    e = entries(str(tmp_path / "blocked.cert.json"))["a"][0]
    assert e["outcome"] == "not run" and e["laws"][0]["outcome"] == "not run"
    assert "holes without a value" in e["laws"][0]["error"]


def test_enumerating_int_in_a_box_is_graded_bounded(tmp_path):
    lib = write(tmp_path, "box.lut", "Small (x : Int) : Bool := x * x < 1000\n"
                                     "s : { u : Unit | \\ (x : Int) { Small x } } := unit\n"
                                     "Z3 : U := { k : Int | 0 <= k and k < 3 }\n"
                                     "t : { u : Unit | \\ (x : Z3) { x < 3 } } := unit\n"
                                     "test s exhaustive\ntest t exhaustive\n")
    main(["test", lib])
    e = entries(str(tmp_path / "box.cert.json"))
    assert e["s"][0]["laws"][0]["mode"] == "bounded"
    assert e["t"][0]["laws"][0]["mode"] == "exhaustive"


def test_a_test_over_a_provisional_extern_is_never_certified(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(tmp_path))
    write(tmp_path, "provext.py", "def same(x):\n    return x\n")
    lib = write(tmp_path, "prov.lut", 'Id (f : Int -> Int) (x : Int) : Bool := f x == x\n'
                                      'same : { f : Int -> Int | Id f } := extern provisional "python:provext.same"\n'
                                      'test same with 10\n')
    main(["test", lib])
    e = entries(str(tmp_path / "prov.cert.json"))["same"][0]
    assert e["provisional"] == ["same"]
    loader = load([lib])
    assert "same" not in loader.checker.certified and "provisional" in loader.known["same"]["outcome"]


def test_a_certificate_with_fewer_cases_than_the_directive_is_stale(tmp_path):
    lib = write(tmp_path, "few.lut", "P (x : Int) : Bool := x == x\nq : { u : Unit | \\ (x : Int) { P x } } := unit\n"
                                     "test q with 10\n")
    assert main(["test", lib]) == 0
    write(tmp_path, "few.lut", "P (x : Int) : Bool := x == x\nq : { u : Unit | \\ (x : Int) { P x } } := unit\n"
                               "test q with 50\n")
    loader = load([lib])
    assert "q" not in loader.checker.certified and "asks for 50" in loader.stale_why["q"]


def test_names_that_no_longer_exist_are_pruned(tmp_path):
    lib = write(tmp_path, "prune.lut", "P (x : Int) : Bool := x == x\n"
                                       "q : { u : Unit | \\ (x : Int) { P x } } := unit\n"
                                       "r : { u : Unit | \\ (x : Int) { P x } } := unit\n")
    main(["test", lib])
    assert set(entries(str(tmp_path / "prune.cert.json"))) == {"q", "r"}
    write(tmp_path, "prune.lut", "P (x : Int) : Bool := x == x\nq : { u : Unit | \\ (x : Int) { P x } } := unit\n")
    main(["test", lib])
    assert set(entries(str(tmp_path / "prune.cert.json"))) == {"q"}


def test_a_run_records_the_state_of_its_cone_and_can_require_it(tmp_path):
    lib = write(tmp_path, "prog.lut", "P (x : Int) : Bool := x == x\nq : { u : Unit | \\ (x : Int) { P x } } := unit\n"
                                      "main : Int := match q { u -> 7 }\n")
    with pytest.raises(SystemExit, match="require-certified"):
        main(["run", lib, "--require-certified"])
    assert main(["run", lib]) == 0
    rec = json.loads((tmp_path / "prog.run.json").read_text())["runs"][-1]
    assert rec["cone"]["not certified"] == {"q": "pending"}
    assert set(rec["fingerprint"]) == {"code", "externs", "interpreter"} and "interpreter" in rec["luthier"]
    main(["test", lib])
    assert main(["run", lib, "--require-certified"]) == 0
