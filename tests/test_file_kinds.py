"""The three kinds of file (D-2026-10-16-e, spec 12.R2): the suffix declares the kind and the
content verifies it. The checker's refusals are the programs kind_*.lut of tests/spec/; here, the
commands and the loader: `run` takes only a .run.lut, `certify` and `test` only a .test.lut, an
executive file imported is refused at load, and the results of an executive file live beside it
(x.run.json and x.results.json beside x.run.lut; nothing beside x.test.lut, whose entries go to
the store of the file that makes the claim, L10.12). Written 2026-10-16 by Claude Opus 5.5, an
agent of the coordinating session, on record/IA/code-follows-2026-10-16/prompt-file-kinds.md."""
import json
from pathlib import Path

import pytest

from luthier.cli import main
from luthier.run import RunError, base_name, file_kind, record_path, results_path, run_file

ROOT = Path(__file__).resolve().parents[1]
CERTIFIED = ROOT / "tests" / "run" / "certified"

PURE = "answer (k : Int) : Int := k + 1\nmain : Int := answer 41\n"


def test_the_suffix_declares_the_kind():
    assert [file_kind(n) for n in ("a.run.lut", "a.test.lut", "a.lut", "a.lth", "a.bib", ".run.lut")] == [
        "run", "test", "model", "theory", None, "model"]
    assert [base_name(n) for n in ("x.run.lut", "x.test.lut", "x.lut", "x.lth")] == ["x"] * 4
    assert record_path("d/x.run.lut") == Path("d/x.run.json")
    assert results_path("d/x.run.lut") == Path("d/x.results.json")


def test_run_takes_only_a_run(tmp_path, capsys):
    for name in ("x.test.lut", "x.lut", "x.lth"):
        path = tmp_path / name
        path.write_text(PURE, encoding="utf-8")
        assert main(["run", str(path)]) == 1
        err = capsys.readouterr().err
        assert "`luthier run` takes a .run.lut file (12.R2" in err and f"{name} is " in err
    assert sorted(p.name for p in tmp_path.iterdir()) == ["x.lth", "x.lut", "x.test.lut"]


def test_run_on_a_test_program_says_which_command_takes_it(capsys):
    assert main(["run", str(ROOT / "tests/tester/laws.test.lut")]) == 1
    assert "laws.test.lut is a test program (.test.lut, for `luthier certify`)" in capsys.readouterr().err


def test_certify_and_test_take_only_a_test_program(tmp_path, capsys):
    path = tmp_path / "x.run.lut"
    path.write_text(PURE, encoding="utf-8")
    assert main(["certify", str(path)]) == 1
    out = capsys.readouterr().out
    assert "`luthier certify` takes a .test.lut file (12.R2" in out and "x.run.lut is a run (.run.lut, for `luthier run`)" in out
    assert main(["test", str(path)]) == 1
    assert "`luthier test` takes a .test.lut file" in capsys.readouterr().err
    # nothing ran: no store, no record
    assert sorted(p.name for p in tmp_path.iterdir()) == ["x.run.lut"]


def test_certify_refuses_the_whole_command_before_any_line_runs(tmp_path, capsys):
    good = tmp_path / "t.test.lut"
    good.write_text('import "test.lth" test ExhaustiveMode\nExcluded (b : Bool) : Bool := b or not b\n'
                    'test "Excluded" ExhaustiveMode\n', encoding="utf-8")
    bad = tmp_path / "m.lut"
    bad.write_text(PURE, encoding="utf-8")
    assert main(["certify", str(good), str(bad)]) == 1
    out = capsys.readouterr().out
    assert "m.lut is a model or library (.lut)" in out and "t.test.lut:" not in out


def test_an_imported_run_is_refused_at_load_and_by_the_checker(tmp_path, capsys):
    # the control: a .run.lut imported by another file
    (tmp_path / "lib.run.lut").write_text(PURE, encoding="utf-8")
    user = tmp_path / "user.run.lut"
    user.write_text('import "lib.run.lut" answer\nmain : Int := answer 1\n', encoding="utf-8")
    with pytest.raises(RunError, match=r"user.run.lut imports lib.run.lut, a run \(.run.lut\): an executive file "
                                       r"is never imported \(12.R2"):
        run_file(user)
    assert main(["check", str(user)]) == 1
    assert "12.R2 import: user.run.lut imports lib.run.lut" in capsys.readouterr().out


def test_an_imported_test_program_is_refused_at_load(tmp_path):
    (tmp_path / "laws.test.lut").write_text('import "test.lth" test ExhaustiveMode\n'
                                            'Excluded (b : Bool) : Bool := b or not b\n'
                                            'test "Excluded" ExhaustiveMode\n', encoding="utf-8")
    other = tmp_path / "other.test.lut"
    other.write_text('import "test.lth" test ExhaustiveMode\nimport "laws.test.lut" Excluded\n'
                     'test "Excluded" ExhaustiveMode\n', encoding="utf-8")
    from luthier.tester import run_tests
    with pytest.raises(RunError, match="an executive file is never imported"):
        run_tests(other)


def test_a_run_writes_its_record_and_results_beside_it(tmp_path):
    # the coordinator's finding on 01e5d93: x.run.lut's record is x.run.json, never x.run.run.json
    path = tmp_path / "x.run.lut"
    path.write_text(PURE, encoding="utf-8")
    assert main(["run", str(path)]) == 0
    names = sorted(p.name for p in tmp_path.iterdir())
    assert {"x.run.json", "x.results.json"} <= set(names)
    assert not any(".run.run." in n or ".run.results." in n for n in names)
    assert json.loads((tmp_path / "x.run.json").read_text(encoding="utf-8"))[-1]["entry"] == "main"


def test_a_test_program_writes_nothing_beside_itself(tmp_path):
    # small.test.lut's entry goes to small.cert.json, the store of the file that defines the model
    for p in CERTIFIED.glob("small*.lut"):
        (tmp_path / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    from luthier.tester import run_tests
    assert [o.grade for o in run_tests(tmp_path / "small.test.lut", store=True)] == ["Cases"]
    assert sorted(p.name for p in tmp_path.iterdir() if not p.name.endswith(".lock")) == [
        "small.cert.json", "small.lut", "small.test.lut"]
