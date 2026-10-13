"""Runner integration tests derived from user request 2026-10-13, v1."""
import os
from pathlib import Path
import subprocess
import sys

import pytest

from luthier import host
from luthier.cli import main
from luthier.run import RunError, run_file

ROOT = Path(__file__).resolve().parents[1]


def first_line(text):
    return text.splitlines()[0] if text.splitlines() else ""


def command(path, *args, cwd=None):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join((str(ROOT / "src"), str(ROOT / "tests")))
    return subprocess.run([sys.executable, "-m", "luthier.cli", "run", str(path), *args],
                          cwd=cwd, env=env, capture_output=True, text=True)


def test_hello():
    result = command(ROOT / "examples/hello.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "hello, world\n", "")


def test_read_first_line(tmp_path):
    (tmp_path / "input.txt").write_text("first line\nsecond line\n", encoding="utf-8")
    result = command(ROOT / "tests/run/read_first_line.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "first line\n", "")


def test_host_token_places_and_reset(tmp_path):
    host.reset()
    token = object()
    assert host.print_line(token, "hi") == (token, None)
    path = str(tmp_path / "data")
    Path(path).write_text("data\n", encoding="utf-8")
    assert host.read_file(token, path) == (token, "data\n")
    assert host.places() == ["stdout", path]
    assert host.read_place(path) == "data\n"
    assert run_file(ROOT / "examples/hello.lut") == "hello, world\n"
    assert host.places() == ["stdout"]


@pytest.mark.parametrize("source, args, message", [
    ("main :=", (), "expected"),
    ("other : Unit := unit", (), "missing main"),
    ("main : Unit := main", ("--fuel", "20"), "fuel spent"),
    ('main : Unit := extern "python:missing_luthier_module.fail" unit', (), "extern"),
])
def test_errors(tmp_path, source, args, message):
    path = tmp_path / "bad.lut"
    path.write_text(source, encoding="utf-8")
    result = command(path, *args)
    assert result.returncode == 1
    assert message in result.stderr
    assert result.stdout == ""


def test_relative_import_and_custom_main(tmp_path, capsys):
    (tmp_path / "local.lut").write_text('say (w : W) : W * Unit := extern "python:luthier.host.print_line" w "local"')
    path = tmp_path / "main.lut"
    path.write_text('import "local.lut" say\nstart (w : W) : W * Unit := say w')
    assert main(["run", str(path), "--main", "start"]) == 0
    assert capsys.readouterr().out == "local\n"


def test_unused_extern_is_not_resolved(tmp_path):
    path = tmp_path / "lazy.lut"
    path.write_text('unused : Unit := extern "python:missing_luthier_module.fail" unit\nmain : Unit := unit')
    assert run_file(path) == ""


def test_missing_file_extern(tmp_path):
    path = tmp_path / "read.lut"
    path.write_text('main (w : W) : W * String := extern "python:luthier.host.read_file" w "does-not-exist"')
    with pytest.raises(RunError, match="extern.*failed"):
        run_file(path)


def test_world_chain_and_undemanded_action(tmp_path):
    path = tmp_path / "chain.lut"
    path.write_text('''
print (w : W) (s : String) : W * Unit := extern "python:luthier.host.print_line" w s
main (w : W) : W * Unit := {
  ignored := extern "python:missing_luthier_module.fail" unit;
  match print w "one" { (next, x) -> print next "two" }
}
''')
    assert run_file(path) == "one\ntwo\n"


def test_nested_constructor_demand(tmp_path):
    path = tmp_path / "nested.lut"
    path.write_text('''
first (text : String) : String := extern "python:test_run.first_line" text
main (w : W) : W * Unit := match cons (first "one\\ntwo") nil {
  cons "one" rest -> extern "python:luthier.host.print_line" w "matched"
}
''')
    assert run_file(path) == "matched\n"
