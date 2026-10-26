"""Runner integration tests derived from user request 2026-10-13, v1; v2 for world.lth draft 1 (prompt-2.md);
v4 for arrays, tables and numbers across the bridge (prompt-4.md); v6 for the loader's scopes and the
externs' arity (prompt-6.md); v7 for `run --set` and the run's record (prompt-7.md); v8 for functions
across the bridge (prompt-8.md, D-2026-10-14-a), the host side in tests/run/bridge_host.py; v13 for
run's refusal of a cone that is not certified (record/IA/certification-2026-10-14/prompt-run.md,
certification.lth §3, 12.S17), the programs under tests/run/certified/; v16 for the demand and the plan
as values (prompt-13.md; demand.lth, plan.lth), the program tests/run/plan_cone.run.lut."""
import json
import os
import re
from dataclasses import fields, is_dataclass
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from luthier import arrays, host, surface as s
from luthier.cli import main
from luthier.run import Loaded, Refused, RunError, parameter, record_path, run, run_file

ROOT = Path(__file__).resolve().parents[1]


def refused(models):
    """A run the store refuses since prompt-run.md (12.S17): the laws the types of `models` state
    have no entry in the stores the run reads (the x.cert.json of the files it loads, 12.S11).
    Strict, so that the test fails, and its mark is removed, once the store certifies the cone."""
    return pytest.mark.xfail(strict=True, reason=f"refused (12.S17): the laws of {models} have no entry "
                                                 f"in the stores of the files the run loads")


def first_line(text):
    return text.splitlines()[0] if text.splitlines() else ""


# host functions the bridge tests call (python:test_run.*)
def three(u):
    return 3


def ramp(n):
    return np.arange(n)


def total(n, a):
    assert isinstance(a, np.ndarray) and a.dtype == np.float64 and a.shape == (n,)
    return float(a.sum())


def total_int(n, a):
    assert a.dtype == np.int64
    return int(a.sum())


_ticks = []


def tick(k):
    _ticks.append(k)
    return 1.0


def ticks(u):
    return repr(_ticks)


def a_nan(u):
    return float("nan")


def a_bool(u):
    return True


def a_float(u):
    return 1.5


def an_int(u):
    return 1


def settings_sum(s, x):
    # a refined record read by key and by attribute, a `VecOf 2` as its ndarray
    return s["tol"] + s.maxIter + float(np.sum(x))


def matrix(u):
    return np.ones((2, 2))


_reads = []


def read_counted(w, path):
    # a file's text, each read counted (tests/run/read_once.run.lut)
    _reads.append(path)
    return w, Path(path).read_text(encoding="utf-8")


def reads(u):
    return str(len(_reads))


# the shapes and refinements at the crossing (prompt-12.md items 1 and 3)
def identity(x):
    return x


def or_zero(m):
    return m.value if isinstance(m, host.Just) else 0


def minus_one_int(u):
    return -1


def huge(u):
    return 2 ** 70


def a_string(u):
    return "red"


def a_list(u):
    return [7, 8]


def an_ndarray(u):
    return np.array([7, 8])


def unit_as_three(w, s):
    return w, 3


def token_lost(w, s):
    return None, None


def unsigned(n):
    return np.array([2 ** 64 - 1] * n, dtype=np.uint64)


def unsigned_small(n):
    return np.array([5] * n, dtype=np.uint64)


def command(path, *args, cwd=None, record=False):
    """`luthier run path args` in a process; with `record`, the result carries the run's entry of
    `x.run.json` (`result.record`), and a record that existed is left as it was."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join((str(ROOT / "src"), str(ROOT / "tests")))
    # a run appends to x.run.json beside x.lut (12.S18); a test leaves none in the repository
    where = record_path(Path(cwd or ".") / path)
    existed = where.exists()
    before = where.read_bytes() if existed and record else None
    lock = where.parent / "luthier.lock"  # `run` writes it beside the program when absent (12.S13)
    locked = lock.exists()
    try:
        result = subprocess.run([sys.executable, "-m", "luthier.cli", "run", str(path), *args],
                                cwd=cwd, env=env, capture_output=True, text=True)
        if record:
            entries = json.loads(where.read_text(encoding="utf-8")) if where.exists() else []
            result.record = entries[-1] if len(entries) > len(json.loads(before or b"[]")) else None
        return result
    finally:
        if before is not None:
            where.write_bytes(before)
        if not existed and ROOT in where.resolve().parents:
            where.unlink(missing_ok=True)
        if not locked and ROOT in lock.resolve().parents:
            lock.unlink(missing_ok=True)


def test_hello(tmp_path):
    # a copy, so that the run's record is written beside the copy and not into examples/
    hello = tmp_path / "hello.run.lut"
    hello.write_text((ROOT / "examples/hello.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    result = command(hello)
    assert (result.returncode, result.stdout, result.stderr) == (0, "hello, world\n", "")


def test_read_first_line(tmp_path):
    (tmp_path / "input.txt").write_text("first line\nsecond line\n", encoding="utf-8")
    result = command(ROOT / "tests/run/read_first_line.run.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "first line\n", "")


def test_host_observe_and_reset(tmp_path):
    host.reset()
    token = object()
    assert host.observe(token, []) == (token, {"stdout": "", "files": []})
    assert host.print_line(token, "hi") == (token, None)
    path = str(tmp_path / "data")
    absent = str(tmp_path / "absent")
    Path(path).write_text("data\n", encoding="utf-8")
    places = ["stdout", path, absent]
    assert host.observe(token, places) == (token, {"stdout": "hi\n", "files": [(path, "data\n")]})
    # nothing is remembered: no read needed, the disk is read every time, "stdout" only when asked
    assert host.observe(token, [path]) == (token, {"stdout": "", "files": [(path, "data\n")]})
    Path(path).write_text("changed\n", encoding="utf-8")
    assert host.observe(token, places)[1]["files"] == [(path, "changed\n")]
    Path(absent).write_text("now\n", encoding="utf-8")
    assert host.observe(token, places)[1]["files"] == [(path, "changed\n"), (absent, "now\n")]
    assert host.read_file(token, path) == (token, host.Just("changed\n"))
    assert host.read_file(token, str(tmp_path / "nope")) == (token, host.NOTHING)
    hello = tmp_path / "hello.run.lut"
    hello.write_text((ROOT / "examples/hello.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    assert run_file(hello) == "hello, world\n"
    assert host.observe(token, ["stdout"]) == (token, {"stdout": "hello, world\n", "files": []})


def test_observe_through_the_bridge(tmp_path):
    (tmp_path / "input.txt").write_text("first line\n", encoding="utf-8")
    result = command(ROOT / "tests/run/observe.run.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "one\none\n\n\nfirst line\n\n", "")


@pytest.mark.parametrize("source, args, message", [
    ("main :=", (), "expected"),
    ("other : Unit := unit", (), "missing main"),
    ("main : Unit := main", ("--fuel", "20"), "fuel spent"),
    ('main : Unit := extern "python:missing_luthier_module.fail" unit', (), "extern"),
])
def test_errors(tmp_path, source, args, message):
    path = tmp_path / "bad.run.lut"
    path.write_text(source, encoding="utf-8")
    result = command(path, *args)
    assert result.returncode == 1
    assert message in result.stderr
    assert result.stdout == ""


def test_relative_import_and_custom_main(tmp_path, capsys):
    (tmp_path / "local.lut").write_text('say (w : W) : W * Unit := extern "python:luthier.host.print_line" w "local"')
    path = tmp_path / "main.run.lut"
    path.write_text('import "local.lut" say\nstart (w : W) : W * Unit := say w')
    assert main(["run", str(path), "--main", "start"]) == 0
    assert capsys.readouterr().out == "local\n"


def test_unused_extern_is_not_resolved(tmp_path):
    path = tmp_path / "lazy.run.lut"
    path.write_text('unused : Unit := extern "python:missing_luthier_module.fail" unit\nmain : Unit := unit')
    assert run_file(path) == ""


def test_missing_file_is_nothing(tmp_path):
    result = command(ROOT / "tests/run/read_first_line.run.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "no input.txt\n", "")


def test_world_chain_and_undemanded_action(tmp_path):
    path = tmp_path / "chain.run.lut"
    path.write_text('''
print (w : W) (s : String) : W * Unit := extern "python:luthier.host.print_line" w s
main (w : W) : W * Unit := {
  ignored := extern "python:missing_luthier_module.fail" unit;
  match print w "one" { (next, x) -> print next "two" }
}
''')
    assert run_file(path) == "one\ntwo\n"


def test_nested_constructor_demand(tmp_path):
    path = tmp_path / "nested.run.lut"
    path.write_text('''
first (text : String) : String := extern "python:test_run.first_line" text
main (w : W) : W * Unit := match cons (first "one\\ntwo") nil {
  cons "one" rest -> extern "python:luthier.host.print_line" w "matched"
}
''')
    assert run_file(path) == "matched\n"


def test_vector_norm_through_numpy():
    result = command(ROOT / "tests/run/vector_norm.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "5.0\n", "")


def test_size_at_and_map_resolve_at_a_vector():
    # core bite 11 (execution.md §6): arrays.lth's VecIsIndexed and VecIsAFunctor bind the core's
    # `size`, `at` and `map` at `Vec Float64`, written with no qualification
    result = command(ROOT / "tests/run/vec_resolution.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "resolved\n", "")


def test_matrix_product_through_numpy():
    result = command(ROOT / "tests/run/matrix_product.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "43.0\n2\n", "")


@refused("csv : Codec, built : Codec")
def test_table_cell_through_csv(tmp_path):
    (tmp_path / "table.csv").write_text("id:int,name:str,x:float\n1,alpha,0.5\n2,beta,1.5\n", encoding="utf-8")
    result = command(ROOT / "tests/run/table_cell.run.lut", cwd=tmp_path)
    assert (result.returncode, result.stderr) == (0, "")
    assert result.stdout == "beta\n2\n1.5\na:int,b:str\n0,x\n1,x\n\n"


@refused("csv : Codec, built : Codec")
def test_table_not_parsed_is_nothing(tmp_path):
    (tmp_path / "table.csv").write_text("id:real\n1\n", encoding="utf-8")
    result = command(ROOT / "tests/run/table_cell.run.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "not a table\n", "")


def test_extern_in_a_record_is_read_when_projected():
    result = command(ROOT / "tests/run/record_externs.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "2.5\n", "")


def test_numbers_and_fin_functions():
    result = command(ROOT / "tests/run/numbers.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "3.0\n2.0\n3.0\n3.0\n", "")


PRELUDE = '''
print (w : W) (s : String) : W * Unit := extern "python:luthier.host.print_line" w s
showFloat (x : Float64) : String := extern "python:builtins.repr" x
showInt (x : Int) : String := extern "python:builtins.repr" x
'''


@pytest.mark.parametrize("source, message", [
    ('nan (u : Unit) : Float64 := extern "python:test_run.a_nan" u\n'
     'main (w : W) : W * Unit := print w (showFloat (nan unit))', "not a Float64"),
    ('yes (u : Unit) : Int := extern "python:test_run.a_bool" u\n'
     'main (w : W) : W * Unit := print w (showInt (yes unit))', "where an Int is declared"),
    ('yes (u : Unit) : Bool := extern "python:test_run.an_int" u\n'
     'main (w : W) : W * Unit := print w (if yes unit then "y" else "n")', "where a Bool is declared"),
    ('half (u : Unit) : Int := extern "python:test_run.a_float" u\n'
     'main (w : W) : W * Unit := print w (showInt (half unit))', "where an Int is declared"),
    ('ramp (n : Int) : Fin n -> Float64 := extern "python:test_run.ramp" n\n'
     'main (w : W) : W * Unit := print w (showFloat (ramp 3 3))', "outside Fin 3"),
    ('ramp (n : Int) : Fin n -> Float64 := extern "python:test_run.ramp" n\n'
     'main (w : W) : W * Unit := print w (showFloat (ramp 3 (0 - 1)))', "outside Fin 3"),
    ('ramp (n : Int) : Fin n -> Float64 := extern "python:test_run.ramp" n\n'
     'main (w : W) : W * Unit := print w (showFloat (ramp 4 0))', ""),
    ('total (n : Int) (f : Fin n -> Int) : Int := extern "python:test_run.total_int" n f\n'
     'main (w : W) : W * Unit := print w (showInt (total 2 (fn k { 9223372036854775807 + 1 })))', "64 bits"),
    ('m (u : Unit) : { n : Nat, f : Fin n -> Float64 } := extern "python:test_run.matrix" u\n'
     'main (w : W) : W * Unit := print w (showInt (m unit).n)', "dimensions"),
])
def test_crossing_errors(tmp_path, source, message):
    path = tmp_path / "bad.run.lut"
    path.write_text(PRELUDE + source, encoding="utf-8")
    result = command(path, cwd=ROOT / "tests")
    if not message:  # the control: the same program in range runs
        assert (result.returncode, result.stdout) == (0, "0.0\n")
        return
    assert result.returncode == 1, result.stdout
    assert message in result.stderr


# prompt-12.md item 1 (review A24/B18, A26/B17, A28/B19): every declared type is checked where it
# crosses, either way, and a type the bridge does not read is an error; each case with its control,
# the same program with a value of the type, which runs
SHAPES = {
    "to the host, String": (
        'len (s : String) : Int := extern "python:builtins.len" s\n'
        'main (w : W) : W * Unit := print w (showInt (len {}))', '"abc"', "3", "not a String at the crossing"),
    "to the host, Unit": (
        'three (u : Unit) : Int := extern "python:test_run.three" u\n'
        'main (w : W) : W * Unit := print w (showInt (three {}))', "unit", "1", "not unit at the crossing"),
    "to the host, Bool": (
        'same (b : Bool) : Bool := extern "python:test_run.identity" b\n'
        'main (w : W) : W * Unit := print w (if same {} then "y" else "n")', "true", "1", "not a Bool at the crossing"),
    "to the host, Nat": (
        'nat (k : Nat) : Int := extern "python:test_run.identity" k\n'
        'main (w : W) : W * Unit := print w (showInt (nat {}))', "2", "(0 - 1)", "where a Nat is declared"),
    "to the host, Int of 64 bits": (
        'int (k : Int) : Int := extern "python:test_run.identity" k\n'
        'main (w : W) : W * Unit := print w (showInt (int {}))', "9223372036854775807",
        "(9223372036854775807 + 1)", "does not fit in 64 bits"),
    "to the host, Maybe": (
        'orZero (m : Maybe Int) : Int := extern "python:test_run.or_zero" m\n'
        'main (w : W) : W * Unit := print w (showInt (orZero {}))', "(just 3)", "3", "not a Maybe at the crossing"),
    "to the host, the token": (
        'main (w : W) : W * Unit := print {} "x"', "w", "unit", "not the run's token"),
    "from the host, String": (
        'str (u : Unit) : String := extern "python:test_run.{}" u\n'
        'main (w : W) : W * Unit := print w (str unit)', "a_string", "three", "where a String is declared"),
    "from the host, Unit": (
        'say (w : W) (s : String) : W * Unit := extern "python:{}" w s\n'
        'main (w : W) : W * Unit := say w "x"', "luthier.host.print_line", "test_run.unit_as_three",
        "where Unit is declared"),
    "from the host, Nat": (
        'nat (u : Unit) : Nat := extern "python:test_run.{}" u\n'
        'main (w : W) : W * Unit := print w (showInt (nat unit))', "an_int", "minus_one_int", "where a Nat is declared"),
    "from the host, Int of 64 bits": (
        'int (u : Unit) : Int := extern "python:test_run.{}" u\n'
        'main (w : W) : W * Unit := print w (showInt (int unit))', "an_int", "huge", "does not fit in 64 bits"),
    "from the host, List": (
        'items (u : Unit) : List Int := extern "python:test_run.{}" u\n'
        'main (w : W) : W * Unit := print w (match items unit {{ nil -> "" ; cons x rest -> showInt x }})',
        "a_list", "an_ndarray", "where a List is declared"),
    "from the host, the token": (
        'say (w : W) (s : String) : W * Unit := extern "python:{}" w s\n'
        'main (w : W) : W * Unit := say w "x"', "luthier.host.print_line", "test_run.token_lost",
        "where the run's token is declared"),
    "from the host, an unsigned array": (
        'big (n : Int) : Fin n -> Int := extern "python:test_run.{}" n\n'
        'main (w : W) : W * Unit := print w (showInt (big 1 0))', "unsigned_small", "unsigned", "does not fit in 64 bits"),
    "from the host, a type the bridge does not read": (
        'Colour : U := data {{ red : Colour ; blue : Colour }}\n'
        'colour (u : Unit) : {} := extern "python:test_run.a_string" u\n'
        'main (w : W) : W * Unit := match colour unit {{ _ -> print w "seen" }}', "String", "Colour",
        "a type the bridge does not read"),
}


@pytest.mark.parametrize("case", SHAPES)
@pytest.mark.parametrize("honest", [True, False], ids=["control", "refused"])
def test_each_declared_type_is_checked_where_it_crosses(tmp_path, case, honest):
    source, good, bad, message = SHAPES[case]
    path = tmp_path / "shape.run.lut"
    path.write_text(PRELUDE + source.format(good if honest else bad), encoding="utf-8")
    result = command(path, cwd=ROOT / "tests")
    if honest:
        assert (result.returncode, result.stderr) == (0, ""), result.stderr
        assert result.stdout
        return
    assert result.returncode == 1, result.stdout
    assert message in result.stderr


# prompt-12.md items 2 and 3 (12.S18, 4.R5, 10.S11): under `run --checked` each value an extern
# gives at a declared subtype has its predicate evaluated by the Runner as it crosses; the host
# side is tests/run/checked_host.py

CHECKED = ROOT / "tests" / "run" / "checked.run.lut"


@pytest.mark.parametrize("entry, message", [
    ("refuteNegative", "--checked: negative (python:run.checked_host.minus_one) gave -1.0 where Positive is "
                       "declared: 0.0 < x is false at x = that value (12.S18, 4.R5, 10.S11)"),
    ("refuteShort", "--checked: short (python:run.checked_host.two_entries) gave { n := 2, f := [1. 2.] } where "
                    "VecOf 3 is declared: v.n == 3 is false at v = that value"),
    ("refuteIndefinite", "where PsdAt numpy 0.1 is declared: (numpy.retainedRank 0.1 (mscaleDef (0.0 - 1.0) s)) "
                         "== 0 is false"),
])
def test_checked_refuses_a_value_that_refutes_its_refinement(entry, message):
    refused = command(CHECKED, "--main", entry, "--checked", cwd=ROOT / "tests")
    assert (refused.returncode, refused.stdout) == (1, "")
    assert message in refused.stderr
    # without the flag the refinement is the certificate's obligation (4.R5): the run goes on
    unchecked = command(CHECKED, "--main", entry, cwd=ROOT / "tests")
    assert (unchecked.returncode, unchecked.stderr) == (0, "")


def test_checked_runs_an_honest_host_and_records_the_count(tmp_path):
    checked = command(CHECKED, "--checked", cwd=ROOT / "tests", record=True)
    assert (checked.returncode, checked.stdout, checked.stderr) == (0, "2.0\n3.0\n1.0\n", "")
    # Positive is Moderate's predicate and its own, PsdAt Symmetric's and its own
    assert checked.record["checked"] is True
    assert checked.record["refinements"] == {"python:run.checked_host.two": 2,
                                             "python:run.checked_host.three_entries": 1,
                                             "python:run.checked_host.identity": 2}
    unchecked = command(CHECKED, cwd=ROOT / "tests", record=True)
    assert unchecked.stdout == checked.stdout
    assert unchecked.record["checked"] is False and "refinements" not in unchecked.record


def test_vector_norm_under_checked():
    # numpy.norm gives a Float64 and takes a Vec Float64: no subtype crosses in, none is tested
    result = command(ROOT / "tests/run/vector_norm.run.lut", "--checked", record=True)
    assert (result.returncode, result.stdout, result.stderr) == (0, "5.0\n", "")
    assert (result.record["checked"], result.record["refinements"]) == (True, {})


def test_a_refined_record_and_a_type_family_cross(tmp_path):
    # the fit's crossings (record/IA/fit-host-2026-10-14/prompt.md): a record with a refinement
    # (belief.lth's `Settings`) crosses as its record, by key or attribute; a type family applied
    # (`VecOf 2`) is unfolded to the vectors of length 2 and crosses as an ndarray
    path = tmp_path / "families.run.lut"
    path.write_text(PRELUDE + '''
import "arrays.lth" VecOf vec
Opts : U := { tol : Float64, maxIter : Int | 0.0 < tol and 0 < maxIter }
total (s : Opts) (x : VecOf 2) : Float64 := extern "python:test_run.settings_sum" s x
opts : Opts := { tol := 0.5, maxIter := 2 }
main (w : W) : W * Unit := print w (showFloat (total opts (vec Float64 2 (fn k { 1.0 }))))
''', encoding="utf-8")
    result = command(path, cwd=ROOT / "tests")
    assert (result.returncode, result.stdout, result.stderr) == (0, "4.5\n", "")


def test_each_entry_once(tmp_path):
    path = tmp_path / "once.run.lut"
    path.write_text(PRELUDE + '''
tick (k : Int) : Float64 := extern "python:test_run.tick" k
ticks (u : Unit) : String := extern "python:test_run.ticks" u
total (n : Int) (f : Fin n -> Float64) : Float64 := extern "python:test_run.total" n f
main (w : W) : W * Unit :=
  match print w (showFloat (total 3 (fn k { tick k }))) { (w1, u) -> print w1 (ticks unit) }
''', encoding="utf-8")
    result = command(path, cwd=ROOT / "tests")
    assert (result.returncode, result.stdout, result.stderr) == (0, "3.0\n[0, 1, 2]\n", "")


def test_retained_rank_at():
    assert arrays.retained_rank_at(0.1, np.diag([0.0, 1.0, 5.0])) == 2
    assert arrays.retained_rank_at(0.5, np.diag([1.0, 3.0])) == 1
    assert arrays.retained_rank_at(0.1, np.zeros((3, 3))) == 0
    assert arrays.retained_rank_at(0.1, np.eye(4)) == 4


def test_connective_on_a_match_reads_core_data():
    # prompt-5.md: `and` on a match over a list; core.lut's data in every run
    result = command(ROOT / "tests/run/connective_on_match.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "yes\n", "")


def test_host_cell_under_an_operator_crosses_first():
    # prompt-5.md: the Runner reduces a primitive's operands with the host
    result = command(ROOT / "tests/run/host_cell_under_operator.run.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "8\n", "")


def test_bootstrap_primitives_and_not(tmp_path):
    # prompt-5.md: run_file defines kernel.BOOTSTRAP_PRIMITIVES; `not` is core's
    path = tmp_path / "ops.run.lut"
    path.write_text('''
print (w : W) (s : String) : W * Unit := extern "python:luthier.host.print_line" w s
main (w : W) : W * Unit := print w (if not (0 >= 3) and 7 mod 3 /= 0 and "ab" == "a" <> "b" then "ok" else "no")
''')
    assert run_file(path) == "ok\n"


def test_equality_on_strings_and_parameterized_data(tmp_path):
    # prompt-10.md: `/=` on strings, `==` and `/=` on core's Maybe and List
    path = tmp_path / "eq.run.lut"
    path.write_text('''
print (w : W) (s : String) : W * Unit := extern "python:luthier.host.print_line" w s
main (w : W) : W * Unit := print w (if "mic2" /= "mic1" and just 1 == just 1 and [1, 2] == [1, 2] and nothing /= just 1 and not ([1, 2] /= [1, 2]) then "ok" else "no")
''')
    assert run_file(path) == "ok\n"


EXPECTED_VALIDATE_GRAPH = ("valid: 10 nodes, 22 measurements, 21 distinct pairs; directions the distances do not see: "
                           "14 (of which 10 are the heights and 3 the rigid motions of the plane)\n")


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="about 5 minutes; set LUTHIER_SLOW=1")
def test_validate_graph_slow():
    # prompt-10.md item 4: the first full run of the slice
    result = command(ROOT / "examples/sonolocalizacion/validate_graph.run.lut",
                     "--set", "graphDir=examples/sonolocalizacion/A/graph", cwd=ROOT)
    assert result.returncode == 0, result.stderr
    assert result.stdout == EXPECTED_VALIDATE_GRAPH


FIGURES = ("positions.png", "residuals.png", "transform.png")


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="about 6 minutes; set LUTHIER_SLOW=1")
def test_fit_renders_its_figures_slow(tmp_path):
    # record/IA/plots-2026-10-15/prompt-figures.md item 3 (plan G4): the fit on graph_noA2 writes
    # its three figures under outDir, and two runs write the same bytes (plot.lth `rendersTheSame`,
    # across processes)
    images, plans = [], []
    for k in (1, 2):
        out = tmp_path / f"run{k}"
        out.mkdir()
        result = command(ROOT / "examples/sonolocalizacion/experiment_zero.run.lut",
                         "--set", "graphDir=examples/sonolocalizacion/A/graph_noA2", "--set", f"outDir={out}",
                         "--set", "lmMaxIter=500", "--set", "lmTol=1e-6", "--set", "lmFloor=5.995204332975845e-15",
                         "--fuel", "100000000000", cwd=ROOT, record=True)
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines()[-1].startswith("nodes 9, measurements 19, sigma ")
        assert all((out / name).is_file() for name in FIGURES)
        images.append([(out / name).read_bytes() for name in FIGURES])
        # prompt-13.md item 4: the record holds the demand, the plan and the key (12.S18, 8.S8, L5.6)
        assert {"demand", "plan", "key"} <= set(result.record)
        assert result.record["demand"]["parameters"]["outDir"] == str(out)
        assert result.record["key"]["values"]["graphDir"] == "examples/sonolocalizacion/A/graph_noA2"
        plans.append(result.record["plan"])
    assert images[0] == images[1]
    # the same program, entry and order of reduction: the same plan, its hash stable across runs
    assert plans[0]["hash"].startswith("sha256:") and plans[0] == plans[1]


@pytest.mark.skipif(not os.environ.get("LUTHIER_SLOW"), reason="about 3 minutes; set LUTHIER_SLOW=1")
def test_the_fit_runs_checked_slow(tmp_path):
    # prompt-12.md item 3: the fit of test_fit_renders_its_figures_slow under --checked (12.S18): every
    # VecOf n the maximizer gives back, or passes to the posterior's callbacks, has its length tested
    result = command(ROOT / "examples/sonolocalizacion/experiment_zero.run.lut",
                     "--set", "graphDir=examples/sonolocalizacion/A/graph_noA2", "--set", f"outDir={tmp_path}",
                     "--set", "lmMaxIter=500", "--set", "lmTol=1e-6", "--set", "lmFloor=5.995204332975845e-15",
                     "--fuel", "100000000000", "--checked", cwd=ROOT, record=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[-1].startswith("nodes 9, measurements 19, sigma ")
    assert result.record["checked"] is True
    print(json.dumps(result.record["refinements"], indent=1))
    assert result.record["refinements"].get("python:luthier.lm.maximize", 0) > 0


# ---------------------------------------------------------------- the loader scopes names by file
# (record/IA/run-2026-10-13/prompt-6.md, 12.S22)

SCOPE = ROOT / "tests" / "run" / "scope"
LIB = ROOT / "src" / "luthier" / "lib"


def test_each_file_resolves_its_own_names():
    # left.lut and right.lut both define `helper`; left.lut's `keep` is seen nowhere else
    assert run_file(SCOPE / "main.run.lut") == "3 10 false true\n"


@pytest.mark.parametrize("program, message", [
    ("unlisted.run.lut", "unlisted.run.lut: helper is neither defined there, nor imported, nor core's"),
    ("missing_import.run.lut", "missing_import.run.lut imports twice from right.lut, which does not define it"),
])
def test_only_the_names_an_import_lists_enter(program, message):
    with pytest.raises(RunError) as error:
        run_file(SCOPE / program)
    assert str(error.value) == message


def test_the_loader_reads_no_more_than_the_import_lists(tmp_path):
    loaded = Loaded(SCOPE / "main.run.lut")
    top = loaded.top
    assert loaded.name(top, "twice") == "twice" and loaded.name(top, "ten") == "tenfold"
    assert loaded.name(top, "helper") is None and loaded.name(top, "tenfold") is None
    assert loaded.name(top, "not") == "not"  # core's
    assert loaded.name(SCOPE / "left.lut", "not") == "not" and loaded.name(SCOPE / "left.lut", "keep") == "keep"
    assert {loaded.name(SCOPE / f, "helper") for f in ("left.lut", "right.lut")} == {"helper@left", "helper@right"}


# ---------------------------------------------------------------- the core is the prelude
# (the core's bite 5: record/plan/core-2026-10-17/execution.md §1, D-2026-10-18-b, 12.S22)

def test_every_core_file_is_seen_without_an_import(tmp_path):
    # `compose` is core/properties/functions.lth's, which core.lut does not import
    path = tmp_path / "composed.run.lut"
    path.write_text("import \"world_model.lut\" HostConsole host : HostConsole\n"
                    "showInt (x : Int) : String := extern \"python:builtins.repr\" x\n"
                    "succ (x : Int) : Int := x + 1\n"
                    "main (w : W) : W * Unit := host.print w (showInt (compose Int Int Int succ succ 1))\n",
                    encoding="utf-8")
    loaded = Loaded(path)
    assert loaded.name(loaded.top, "compose") == "compose" and loaded.see(loaded.top, "compose")[0] == LIB / "core" / "core.lut"
    assert run_file(path) == "3\n"


@pytest.mark.parametrize("name, where", [("not", "core/core.lut"), ("compose", "core/core.lut"),
                                          ("Object", "core/structures/equality.lth")])
def test_a_file_that_redefines_a_core_name_is_refused(tmp_path, name, where):
    path = tmp_path / "redefines.run.lut"
    path.write_text(f"{name} (b : Bool) : Bool := b\nmain (w : W) : W * Unit := (w, unit)\n", encoding="utf-8")
    with pytest.raises(RunError) as error:
        Loaded(path)
    assert f"redefines.run.lut defines {name}, which the core defines in {where}" in str(error.value)


def test_the_seven_core_collisions_have_one_definition_and_are_seen_without_an_import(tmp_path):
    from luthier.run import core_definitions, CORE_COLLISIONS
    names = "Reflexive Symmetric Transitive Associative LeftNeutral RightNeutral Idempotent".split()
    assert all(len(core_definitions()[n]) == 1 for n in names)
    assert not any(path.startswith("core/") for path in CORE_COLLISIONS)
    path = tmp_path / "unique.lut"
    path.write_text("r (x : Int) : Bool := Reflexive Int (fn a b { a == b }) x\n", encoding="utf-8")
    loaded = Loaded(path)
    assert loaded.see(loaded.top, "Reflexive") == (LIB / "core/properties/relations.lth", "Reflexive")


def _core_of(tmp_path, files):
    core = tmp_path / "core"
    for name, text in files.items():
        (core / name).parent.mkdir(parents=True, exist_ok=True)
        (core / name).write_text(text, encoding="utf-8")
    return core


def test_a_cycle_of_core_files_is_allowed_when_no_name_reaches_itself(tmp_path):
    # a.lth reads `b` from b.lth and b.lth reads `a` from a.lth (relations.lth's note: `Object`'s
    # law written over `Equivalence`, a cycle of files and not of names)
    core = _core_of(tmp_path, {
        "core.lut": "Bool : U := data { true : Bool ; false : Bool }\n",
        "a.lth": "import \"b.lth\" b\na (x : Bool) : Bool := x\naThenB (x : Bool) : Bool := b (a x)\n",
        "b.lth": "import \"a.lth\" a\nb (x : Bool) : Bool := x\nbThenA (x : Bool) : Bool := a (b x)\n"})
    user = tmp_path / "user.lut"
    user.write_text("both (x : Bool) : Bool := aThenB (bThenA x)\n", encoding="utf-8")
    loaded = Loaded(user, core=core)
    assert loaded.see(loaded.top, "aThenB") == (core / "a.lth", "aThenB")
    assert loaded.see(core / "a.lth", "b") == (core / "b.lth", "b")
    assert not loaded.errors


def test_a_name_that_reaches_itself_through_two_core_files_is_an_error_with_its_path(tmp_path):
    core = _core_of(tmp_path, {
        "core.lut": "Bool : U := data { true : Bool ; false : Bool }\n",
        "a.lth": "import \"b.lth\" x\ny (v : Bool) : Bool := x v\n",
        "b.lth": "import \"a.lth\" x\nz (v : Bool) : Bool := x v\n"})
    user = tmp_path / "user.lut"
    user.write_text("w (v : Bool) : Bool := v\n", encoding="utf-8")
    loaded = Loaded(user, core=core)
    with pytest.raises(RunError) as error:
        loaded.see(core / "a.lth", "x")
    assert str(error.value) == "a.lth: x is imported in a cycle: a.lth x -> b.lth x -> a.lth x"


def test_a_label_and_another_files_definition_of_its_name_are_kept_apart():
    # prompt-10.md: generators.lth's import brings program.lth's `int : Term`, which took the name of
    # tables.lth's Cell label `int`, and `intAt` was a stuck match
    assert run_file(SCOPE / "label_and_definition.run.lut") == "7\n"
    loaded = Loaded(SCOPE / "label_and_definition.run.lut")
    assert loaded.name(LIB / "tables.lth", "int") == "int"
    assert loaded.name(LIB / "program.lth", "int") == "int@program"


def _mentions(value, names):
    """The names of `names` that `value` refers to, as a term or as a pattern."""
    if isinstance(value, (s.Name, s.PApp)):
        found = {value.name.partition(".")[0]} & names
        return found | (_mentions(value.patterns, names) if isinstance(value, s.PApp) else set())
    if isinstance(value, tuple):
        return set().union(*(_mentions(v, names) for v in value))
    if is_dataclass(value) and not isinstance(value, type):
        return set().union(*(_mentions(getattr(value, f.name), names) for f in fields(value)))
    return set()


# the names the tester found defined by several libraries (record/IA/tester-2026-10-14/report.md,
# choice 8 and "Findings for others"), with the files that define them, and a file that uses each
# meaning. Since 993f200 generators.lth's theory is `Enumeration` and since aef8d2c test.lth's
# grade is `AssumedGrade`, so those two are no longer clashes; `LeqBoth` is gone from numbers.lth
# (4a158b0), `NonNegative` of generators.lth is `SupportNonNegative` (core bite 13b), and `LeqPair`, `LeqChain` from numbers.lth and algebra.lth (the core's bite 8, which
# states their laws by the core's `Related` and `Chain`).
CLASHES = {
    "Unresolved": ("laws.lth", "certification.lth"),
}
SEEN_FROM = {}


@pytest.fixture(scope="module")
def numbers_laws():
    return Loaded(ROOT / "tests" / "tester" / "numbers_laws.test.lut")


@pytest.fixture(scope="module")
def certification_laws():
    return Loaded(ROOT / "tests" / "tester" / "certification_laws.test.lut")


@pytest.mark.parametrize("name", CLASHES)
def test_a_name_several_libraries_define_does_not_collide(certification_laws, name):
    loaded, files = certification_laws, CLASHES[name]
    own = {f: loaded.internal((LIB / f).resolve(), name) for f in files}
    assert len(set(own.values())) == len(files), own
    every = set(own.values())
    used = 0
    for f in files:
        # each definer's references to the name are to its own definition
        mentioned = _mentions(loaded.by_file[(LIB / f).resolve()], every)
        assert mentioned <= {own[f]}, (f, mentioned)
        used += bool(mentioned)
    for user, definer in SEEN_FROM.get(name, {}).items():
        assert loaded.name(LIB / user, name) == own[definer]
        assert _mentions(loaded.by_file[(LIB / user).resolve()], every) == {own[definer]}
    assert used, f"no file uses {name}"


def test_the_numbers_laws_import_resolves_in_numbers_lth(numbers_laws):
    # the test file imports numbers.lth's TimesMonotone
    assert numbers_laws.name(numbers_laws.top, "TimesMonotone") == "TimesMonotone"
    # a name the file does not import is the core's, every core file being seen (the core's bite 5)
    assert numbers_laws.see(numbers_laws.top, "LeqPair") is None


# ---------------------------------------------------------------- an extern's arity from its type

def test_the_arity_of_an_extern_is_its_declared_types():
    # math.log has no Python signature: typed, one argument by its type; untyped, taken as unary;
    # math.pi, declared a Float64, is the host's value
    assert run_file(ROOT / "tests" / "run" / "extern_arity.run.lut") == "0.0 3.141592653589793 0.0\n"


# ---------------------------------------------------------------- run --set fills the file's holes
# (record/IA/run-2026-10-13/prompt-7.md, 3.S9, 12.S18)

HOLES = ROOT / "tests" / "run" / "holes.run.lut"


@pytest.mark.parametrize("sets, output", [
    (("graphDir=a/b", "loud=false"), "a/b\n"),
    (("graphDir=a/b", "loud=true", "unused=-3"), "a/b!\n"),
])
def test_set_fills_the_holes(sets, output):
    assert run_file(HOLES, sets=sets) == output


@pytest.mark.parametrize("sets, message", [
    ((), "graphDir : String is a hole of holes.run.lut the run needs; give it with --set graphDir="),
    (("loud=true",), "graphDir : String is a hole of holes.run.lut the run needs"),
    (("graphDir=a", "loud=yes"), "--set loud=yes: not a literal of type Bool"),
    (("graphDir=a", "loud=true", "unused=1.5"), "--set unused=1.5: not a literal of type Int"),
    (("twice=3",), "twice (n : Int) : Int is not a parameter"),
    (("nope=1",), "nope is not a declared hole of holes.run.lut"),
    (("graphDir",), "expected name=value"),
])
def test_set_refuses(sets, message):
    with pytest.raises(RunError, match=re.escape(message)):
        run_file(HOLES, sets=sets)


@pytest.mark.parametrize("type_, text, value", [
    ("String", "a b=c", "a b=c"), ("Int", "-3", -3), ("Float64", "1e-3", 0.001),
    ("Float64", "-2.5", -2.5), ("Bool", "true", True), ("Bool", "false", False),
])
def test_a_set_value_is_a_literal_of_the_holes_type(type_, text, value):
    assert parameter(s.Declare("x", (), s.Name(type_)), text) == value


def test_a_hole_of_another_type_is_refused_by_name():
    with pytest.raises(RunError, match="x : Table is not a parameter"):
        parameter(s.Declare("x", (), s.Name("Table")), "t.csv")


def test_the_run_appends_its_record(tmp_path, capsys):
    path = tmp_path / "holes.run.lut"
    path.write_text(HOLES.read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path), "--set", "graphDir=a/b", "--set", "loud=false"]) == 0
    assert main(["run", str(path), "--set", "graphDir=c", "--set", "loud=true"]) == 0
    assert main(["run", str(path)]) == 1
    assert capsys.readouterr().out == "a/b\nc!\n"
    runs = json.loads((tmp_path / "holes.run.json").read_text(encoding="utf-8"))
    assert [(r["entry"], r["parameters"], r["output"]) for r in runs] == [
        ("main", {"graphDir": "a/b", "loud": False}, "a/b\n"),
        ("main", {"graphDir": "c", "loud": True}, "c!\n")]
    assert all(r["time"] for r in runs)


# ---------------------------------------------------------------- functions across the bridge
# (record/IA/run-2026-10-13/prompt-8.md, D-2026-10-14-a, 3.S23; the laws of world.lth's Crossing
# and term.lth's extern conjuncts, record/IA/theories-2026-10-14/report.md)

RUN = ROOT / "tests" / "run"


def test_a_lambda_handed_to_the_host_is_a_callback():
    # CallbackGivesTheFunction: the host calls (x - 0.3)^2 at 0.0, 0.1, ..., 0.9 and gets Float64s
    assert run_file(RUN / "callbacks.run.lut") == "0.3\n"
    # CallsAreCounted: ten calls, keyed by the receiving extern's route and the argument
    assert host.calls() == {"python:run.bridge_host.maximize": {"1": 10}}


def test_the_calls_are_in_the_runs_record(tmp_path, capsys):
    path = tmp_path / "callbacks.run.lut"
    path.write_text((RUN / "callbacks.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    assert main(["run", str(path)]) == 0
    runs = json.loads((tmp_path / "callbacks.run.json").read_text(encoding="utf-8"))
    # each run counts its own calls (12.S18)
    assert [r["calls"] for r in runs] == [{"python:run.bridge_host.maximize": {"1": 10}}] * 2


def test_a_record_of_functions_crosses_by_field():
    # RecordCrossesByField: the host reads objective.value and objective.grad, each counted apart
    assert run_file(RUN / "record_of_functions.run.lut") == "3.0\n"
    assert host.calls() == {"python:run.bridge_host.descend": {"1.value": 3, "1.grad": 2}}


def test_a_host_function_given_back_is_applied_through_the_bridge():
    # HostGivesBackAValue and ExternIsValue: the host's closures cross in as host:k values, applied
    # by the bridge; one applied to a Luthier lambda calls it back, counted under its handle
    assert run_file(RUN / "host_function.run.lut") == "3.5\n18.0\n"
    assert host.calls() == {"host:2 run.bridge_host.twice_at.<locals>.at": {"1": 2}}


def test_an_extern_applied_to_fewer_arguments_is_a_value():
    # ExternPartialIsValue: add 1.0 waits for its second argument; handed to the host, add 1.0 is
    # a functools.partial of the host's add, written bare or with its parameters (eta)
    assert run_file(RUN / "extern_partial.run.lut") == (
        "3.5\npartial add (1.0,) 3.0\npartial add (1.0,) 3.0\n")
    assert host.calls() == {}


def test_a_callbacks_result_crosses_by_the_codomain(tmp_path):
    path = tmp_path / "bad_callback.run.lut"
    path.write_text(PRELUDE + '''
maximize (f : Float64 -> Float64) : Float64 := extern "python:run.bridge_host.maximize" f
main (w : W) : W * Unit := print w (showFloat (maximize (fn x { "no" })))
''', encoding="utf-8")
    with pytest.raises(RunError, match="not a Float64 at the crossing"):
        run_file(path)


# ---------------------------------------------------------------- a bound value is demanded once
# (record/IA/run-2026-10-13/prompt-9.md, 8.S4: call by need within a run)

def test_a_bare_name_binds_the_token_of_an_imported_models_action(tmp_path):
    # print_twice.run.lut binds `w <- host.print w "..."` twice, host imported from world_model.lut: the
    # sugar of 2.S17 binds the token, so the second print crosses with the run's token
    # (record/IA/v04-2026-10-15/prompt-sugar.md)
    result = command(ROOT / "tests/run/print_twice.run.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "first\nsecond\n", "")


@pytest.mark.parametrize("entry", ["main", "byArgument"])
def test_a_bound_read_is_made_once(tmp_path, entry):
    # read_once.run.lut observes one read twice, bound by a block or passed as an argument
    (tmp_path / "input.txt").write_text("data", encoding="utf-8")
    result = command(ROOT / "tests/run/read_once.run.lut", "--main", entry, cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "data\ndata\n1\n", "")


def test_a_bound_maximize_runs_once(tmp_path):
    # maximize_shared.run.lut projects the result three times; each entry calls back exactly as
    # maximize_quadratic.run.lut, which matches it once (test_lm.py checks those counts against lm.py)
    for name in ("maximize_quadratic.run.lut", "maximize_shared.run.lut"):
        (tmp_path / name).write_text((ROOT / "tests/run" / name).read_text(encoding="utf-8"), encoding="utf-8")
    once = command(tmp_path / "maximize_quadratic.run.lut", cwd=tmp_path)
    assert once.returncode == 0, once.stderr
    expected = json.loads((tmp_path / "maximize_quadratic.run.json").read_text(encoding="utf-8"))[-1]["calls"]
    assert set(expected["python:luthier.lm.maximize"]) == {"3", "4", "5"}
    for entry in ("main", "byArgument"):
        result = command(tmp_path / "maximize_shared.run.lut", "--main", entry, cwd=tmp_path)
        assert (result.returncode, result.stdout, result.stderr) == (0, once.stdout, "")
        runs = json.loads((tmp_path / "maximize_shared.run.json").read_text(encoding="utf-8"))
        assert runs[-1]["entry"] == entry and runs[-1]["calls"] == expected


def test_an_array_that_crossed_in_takes_one_argument():
    # prompt-12.md: the Runner reads an Entries' arity without inspect; its signature says the same
    from luthier.run import Entries, Runner
    assert Runner.signature_arity(Entries(np.zeros(2))) == 1


# ---------------------------------------------------------------- run refuses a cone not certified
# (record/IA/certification-2026-10-14/prompt-run.md; certification.lth §3; 12.S17, 12.S18, 7.S15)

CERTIFIED = RUN / "certified"


def _certified_copy(tmp_path):
    """The programs of tests/run/certified/ in tmp_path, where their stores are written."""
    for p in CERTIFIED.glob("*.lut"):
        (tmp_path / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def _certify_small(tmp_path):
    from luthier.tester import run_tests
    outcomes = run_tests(tmp_path / "small.test.lut", store=True)
    assert [o.grade for o in outcomes] == ["Cases"]


def test_hellos_cone_runs_and_records_its_state(tmp_path, capsys):
    # hello.run.lut's cone (prompt-first-action.md): `console : Console State`, whose four laws
    # tests/tester/world_laws.test.lut certifies into world_model.cert.json, and `host : HostConsole =
    # Host State`, whose laws are run at an action's first application (10.S10), its frame law on
    # the same case, and its root of trust, an axiom, accepted as assumed by the default demand
    # (prompt-run-host.md); the rest vacuous
    path = tmp_path / "hello.run.lut"
    path.write_text((ROOT / "examples/hello.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    state = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]
    assert state["accept"] == "sampled" and state["laws"] == 4 and state["not certified"] == []
    assert state["states"]["certified"] == 1 and state["states"]["at first action"] == 1
    assert state["states"]["vacuous"] > 0
    assert {f["law"] for f in state["at first action"]} == {"HostAgreesPrint", "HostAgreesReadFile",
                                                            "HostObserveChangesNothing"}
    assert {f["frame"] for f in state["at first action"]} == {"HostChangesOnlyDeclared"}
    assert [(f["action"], f["law"]) for f in state["first actions"]] == [
        ("host.print", "HostAgreesPrint"), ("host.print", "HostChangesOnlyDeclared")]
    assert {f["outcome"] for f in state["first actions"]} <= {"served", "confirmed"}
    # its roots of trust (world.lth §5, D-2026-10-16-n; ObserverIsFaithful until 2026-10-26)
    assert [(a["name"], a["law"], a["accept"]) for a in state["assumed"]] == [
        ("host", "FileSystemKeeps", "assumed"), ("host", "SystemDelivers", "assumed")]
    assert state["cone"].startswith("sha256:")


def test_an_uncertified_cone_is_refused_per_law_and_nothing_runs(tmp_path, capsys):
    # RefusalSaysWhy: no entry at all, uncertified; exit 1, nothing evaluated, no record
    path = _certified_copy(tmp_path) / "uses_small.run.lut"
    assert main(["run", str(path)]) == 1
    out, err = capsys.readouterr()
    assert out == "" and "same: FixesBool: uncertified (no entry)" in err
    assert not record_path(path).exists()


def test_a_passed_entry_serves_at_or_above_the_cutoff(tmp_path, capsys):
    # ServesAtTheCutoff and ServesIsMonotoneInTheCutoff: the entry's grade is `cases`
    path = _certified_copy(tmp_path) / "uses_small.run.lut"
    _certify_small(tmp_path)
    for accept in (None, "cases", "assumed"):
        assert main(["run", str(path)] + (["--accept", accept] if accept else [])) == 0
    assert capsys.readouterr().out == "true\n" * 3
    state = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]
    # `same`'s FixesBool and world_model's `console`, its four laws (prompt-first-action.md)
    assert state["laws"] == 5 and state["states"]["certified"] == 2 and state["not certified"] == []
    for accept in ("exhaustive", "proved"):
        with pytest.raises(Refused, match=f"same: FixesBool: passed, cases, below the grade accepted \\({accept}\\)"):
            run_file(path, accept={"exhaustive": "ExhaustiveGrade", "proved": "Proved"}[accept])


def test_an_entry_serves_only_the_model_its_reach_holds(tmp_path):
    # CertifiesOnlyUnderItsBinding: the census lists `same`, the run gives the law `also`
    path = _certified_copy(tmp_path) / "uses_small.run.lut"
    _certify_small(tmp_path)
    with pytest.raises(Refused, match="also: FixesBool: passed, but no passed entry's reach covers m = also"):
        run_file(path, main="other")


WITHIN = """\
Close : { f : Float64 -> Float64 }
NearItself (m : Close) (tol : Float64) (x : Float64) : Bool := m.f x - x <= tol
Close := NearItself
ident : Close := { f := fn x { x } }
"""
WITHIN_TEST = """\
import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "within.lut" NearItself ident
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
tols : List Float64 := [1.0e-6]
xs : List Float64 := [0.0, 1.0]
test "NearItself" ExhaustiveMode (whereBindings <- [bind "m" "ident", bind "tol" "tols", bind "x" "xs"])
"""
USES_WITHIN = """\
import "world_model.lut" HostConsole host : HostConsole
import "within.lut" Close ident
tol : Float64
main (w : W) : W * Unit := host.print w (if ident.f 1.0 == 1.0 then "yes" else "no")
"""


def test_a_per_law_cutoff_reaches_its_law_and_a_hole_reaches_none(tmp_path, capsys):
    # D-2026-10-16-k item 20: a law's cutoff is a typed field of the demand (`--cutoff LAW.PARAMETER=VALUE`,
    # read by the parameter's type), given to that law alone; a hole `--set` fills of the same name
    # reaches no law (before, `sets` reached every law with a parameter of that name)
    from luthier.tester import run_tests
    for name, text in (("within.lut", WITHIN), ("within.test.lut", WITHIN_TEST), ("uses_within.run.lut", USES_WITHIN)):
        (tmp_path / name).write_text(text, encoding="utf-8")
    assert [o.grade for o in run_tests(tmp_path / "within.test.lut", store=True)] == ["Cases"]
    path = tmp_path / "uses_within.run.lut"
    assert main(["run", str(path), "--set", "tol=1e-9"]) == 0
    assert main(["run", str(path), "--cutoff", "NearItself.tol=1e-6"]) == 0
    assert capsys.readouterr().out == "yes\n" * 2
    demand = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["demand"]
    assert demand["cutoffs"] == [{"law": "NearItself", "parameter": "tol", "value": {"Number": 1e-6}}]
    with pytest.raises(Refused, match="ident: NearItself: passed, but no passed entry's reach covers"):
        run(path, cutoffs=["NearItself.tol=1e-9"])
    with pytest.raises(RunError, match=r"--cutoff NearItself.tol=small: not a literal of type Float64"):
        run(path, cutoffs=["NearItself.tol=small"])
    with pytest.raises(RunError, match=r"--cutoff Nowhere.tol=1.0: no law Nowhere"):
        run(path, cutoffs=["Nowhere.tol=1.0"])
    capsys.readouterr()


def test_a_change_to_the_model_or_to_the_law_makes_the_entry_stale(tmp_path):
    # StaleCertifiesNothing: the model's cone against the binding's fingerprint, the law's cone
    # against the entry's hash
    _certified_copy(tmp_path)
    _certify_small(tmp_path)
    small = tmp_path / "small.lut"
    text = small.read_text(encoding="utf-8")
    small.write_text(text.replace("same : Small := { f := fn b { b } }",
                                  "same : Small := { f := fn b { if b then true else false } }"), encoding="utf-8")
    with pytest.raises(Refused, match=r"same: FixesBool: stale \(the model's code changed since its entries\)"):
        run_file(tmp_path / "uses_small.run.lut")
    small.write_text(text.replace("m.f b == b", "(m.f b == b) and true"), encoding="utf-8")
    with pytest.raises(Refused, match=r"same: FixesBool: stale \(its entries are at \w+, the cone is now at \w+\)"):
        run_file(tmp_path / "uses_small.run.lut")


def test_a_provisional_name_is_refused_whole():
    # ProvisionalIsRefused
    with pytest.raises(Refused, match=r"shout: provisional") as refusal:
        run_file(CERTIFIED / "provisional.run.lut")
    assert refusal.value.refusals == [{"name": "shout", "law": None, "state": ("Provisional", None)}]


def test_the_refusal_is_per_law_and_says_why():
    # RefusalIsPerLaw, RefusalSaysWhy, ACoveringPassServes over certify's reading of a store
    from luthier import certify
    def entry(law, cone, outcome, grade, members):
        return {"law": law, "cone": cone, "binding": [{"parameter": "m", "generator": "x", "fingerprint": "f"}],
                "reach": [{"parameter": "m", "reach": {"Members": [{"Printed": v} for v in members]}}],
                "outcome": outcome, "grade": grade}
    def demand(law, accepts="Sampled", model="x"):
        return {"law": law, "cone": "h", "given": [("m", {"Printed": model})], "accepts": accepts,
                "fingerprints": {"m": "f"}}
    entries = [entry("A", "h", "Passed", "Sampled", ["x"]), entry("B", "old", "Passed", "Proved", ["x"]),
               entry("C", "h", {"Failed": "m = x"}, None, ["x"])]
    one = {"name": "x", "provisional": False, "laws": [demand("A"), demand("B"), demand("C"), demand("D")]}
    refusals = certify.refuse(entries, [one])
    assert [(r["law"], r["state"]) for r in refusals] == [
        ("B", ("Stale", "old")), ("C", ("Current", {"Failed": "m = x"})), ("D", ("Uncertified", None))]
    split = [{"name": "x", "provisional": False, "laws": [d]} for d in one["laws"]]
    assert certify.refuse(entries, split) == refusals
    assert certify.refuse(entries, []) == [] and certify.refuse(entries, [{**one, "laws": []}]) == []
    assert certify.serves(demand("A"), entries[0]) and not certify.serves(demand("A", "Cases"), entries[0])
    assert not certify.serves(demand("A", model="y"), entries[0])
    assert certify.refuse(entries, [{**one, "provisional": True}]) == [
        {"name": "x", "law": None, "state": ("Provisional", None)}]


def test_host_table_names_and_kinds_cross_as_lists(monkeypatch):
    # the certification of csv's laws is not the question here (they are graded by tables_laws.test.lut)
    monkeypatch.setattr("luthier.run.certification", lambda *a, **k: None)
    assert run_file(ROOT / "tests/run/table_names.run.lut", fuel=10_000_000) == "same\ndifferent\nsame\n"


# ---------------------------------------------------------------- the record completed, the lock
# (record/IA/run-2026-10-13/prompt-11.md; 12.S18, 12.S13)

def _hello(tmp_path):
    path = tmp_path / "hello.run.lut"
    path.write_text((ROOT / "examples/hello.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    return path


def test_an_entry_has_every_field_of_12_S18(tmp_path, capsys):
    from luthier import certify
    path = _hello(tmp_path)
    assert main(["run", str(path), "--fuel", "123456"]) == 0
    entry = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]
    for field_name in ("entry", "time", "parameters", "output", "calls", "certification", "fuel", "files_read", "lock"):
        assert field_name in entry
    cert = entry["certification"]
    for field_name in ("cone", "interpreter", "accept", "states", "laws", "not certified",
                       "fingerprint", "python", "hosts"):
        assert field_name in cert
    assert cert["fingerprint"].startswith("sha256:") and cert["fingerprint"] != cert["cone"]
    assert cert["interpreter"] == certify.interpreter_revision()
    assert cert["python"] and isinstance(cert["hosts"], dict)
    assert entry["fuel"]["given"] == 123456 and 0 < entry["fuel"]["spent"] < 123456
    assert entry["files_read"] == []


def test_a_run_records_the_file_it_read_with_its_hash(tmp_path, monkeypatch, capsys):
    import hashlib
    path = tmp_path / "read_first_line.run.lut"
    path.write_text((RUN / "read_first_line.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "input.txt").write_bytes(b"first line\nsecond line\n")
    monkeypatch.chdir(tmp_path)
    assert main(["run", str(path)]) == 0
    entry = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]
    assert entry["files_read"] == [["input.txt", "sha256:" + hashlib.sha256(b"first line\nsecond line\n").hexdigest()]]
    assert any(r.startswith("python:test_run") for r in entry["certification"]["hosts"])


def test_the_files_read_are_listed_with_their_hash(tmp_path):
    host.reset()
    f = tmp_path / "f.txt"
    f.write_bytes(b"abc\n")
    host.read_file(None, str(f))
    host.read_file(None, str(f))
    host.observe(None, [str(f), str(tmp_path / "missing")])
    assert host.files_read() == [(str(f), "sha256:" + __import__("hashlib").sha256(b"abc\n").hexdigest())]
    host.reset()
    assert host.files_read() == []


def test_the_same_code_has_the_same_fingerprint_and_other_code_another(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(), b.mkdir()
    one = _hello(a)
    two = _hello(b)
    other = b / "other.run.lut"
    other.write_text(two.read_text(encoding="utf-8").replace("hello, world", "hello, there"), encoding="utf-8")
    for p in (one, two, other):
        assert main(["run", str(p)]) == 0
    fp = [json.loads(record_path(p).read_text(encoding="utf-8"))[-1]["certification"]["fingerprint"]
          for p in (one, two, other)]
    assert fp[0] == fp[1] != fp[2]


def test_the_lock_is_written_when_absent_matches_and_warns_when_it_differs(tmp_path, capsys):
    from luthier import certify
    path = _hello(tmp_path)
    lock = tmp_path / "luthier.lock"
    # absent: written beside the program, with the current revision and, since D-2026-10-16-n, the
    # roots of trust the run used
    assert main(["run", str(path)]) == 0
    assert json.loads(lock.read_text(encoding="utf-8")) == {"interpreter": certify.interpreter_revision(),
                                                            "roots": ["FileSystemKeeps", "SystemDelivers"]}
    first = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["lock"]
    assert first["status"] == "written" and first["pinned"] == certify.interpreter_revision()
    capsys.readouterr()
    # matches: no warning
    assert main(["run", str(path)]) == 0
    out, err = capsys.readouterr()
    assert err == "" and json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["lock"]["status"] == "matches"
    # differs: a warning on standard error, the run goes on, the lock is not rewritten
    lock.write_text(json.dumps({"interpreter": "v0.0-other"}), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    out, err = capsys.readouterr()
    assert out == "hello, world\n" and "pins interpreter v0.0-other" in err
    last = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["lock"]
    assert last["status"] == "differs" and last["pinned"] == "v0.0-other"
    assert json.loads(lock.read_text(encoding="utf-8")) == {"interpreter": "v0.0-other"}


def test_a_lock_in_the_directory_above_is_found(tmp_path, capsys):
    sub = tmp_path / "sub"
    sub.mkdir()
    path = _hello(sub)
    (tmp_path / "luthier.lock").write_text(json.dumps({"interpreter": "v0.0-other"}), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    assert "v0.0-other" in capsys.readouterr().err
    assert not (sub / "luthier.lock").exists()


# ---------------------------------------------------------------- a host action validated at its
# first action (record/IA/certification-2026-10-14/prompt-first-action.md; 10.S10, L11.2)

def _first_action_copy(tmp_path):
    """The first-action programs and their models in tmp_path, where the models' store is written."""
    for name in ("first_action_models.lut", "first_action_honest.run.lut", "first_action_liar.run.lut",
                 "first_action_noisy.run.lut"):
        (tmp_path / name).write_text((RUN / name).read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def test_a_lying_print_is_refused_at_its_first_action_naming_the_place(tmp_path, capsys):
    # liar.print writes its line twice; HostAgreesPrint (world.lth's agreement) is refuted at the
    # run's own argument, the place named; no entry written. Since D-2026-10-16-n `print` writes at
    # once, so the lines are in the world before the case is judged: each of the two runs below
    # printed them, and `luthier run` records its run as one that did not finish, with what it
    # printed and why it was refused (the coordinator's answer to agent P, 2026-10-26; P3)
    path = _first_action_copy(tmp_path) / "first_action_liar.run.lut"
    with pytest.raises(Refused, match=r"liar\.print disagrees with its description at its first action .*"
                                      r"HostAgreesPrint at s = \"twice\": the place stdout differs"):
        run_file(path)
    assert main(["run", str(path)]) == 1
    out, err = capsys.readouterr()
    assert out == "twice\n" * 4 and '(described just "twice\\n", observed just "twice\\ntwice\\n")' in err
    runs = json.loads(record_path(path).read_text(encoding="utf-8"))
    assert len(runs) == 1  # run_file records nothing; `luthier run` does
    rec = runs[0]
    assert rec["finished"] is False and rec["cut"]["reason"] == "refused"
    assert "HostAgreesPrint" in rec["cut"]["message"] and rec["output"] == "twice\ntwice\n"
    assert [(r["name"], r["law"], r["action"]) for r in rec["refusals"]] == [("liar", "HostAgreesPrint", "liar.print")]
    assert rec["stdout"]["accepted"] == len("twice\ntwice\n") and rec["demand"]["roots"]
    assert not (tmp_path / "first_action_models.cert.json").exists()


def test_a_read_that_prints_is_refused_by_the_frame_law_naming_the_place(tmp_path, monkeypatch, capsys):
    # noisy.readFile agrees with its description at the path it declares and prints a line: the
    # frame law (HostChangesOnlyDeclared), on the same case, over the places the certifier adds
    # (the standard output first), refuses it; nothing recorded, no entry (prompt-run-host.md)
    (tmp_path / "input.txt").write_text("first line\n", encoding="utf-8")
    path = _first_action_copy(tmp_path) / "first_action_noisy.run.lut"
    monkeypatch.chdir(tmp_path)
    with pytest.raises(Refused, match=r"noisy\.readFile changed a place it does not declare at its first action .*"
                                      r"HostChangesOnlyDeclared at p = \"input.txt\": the place stdout differs "
                                      r"\(before just \"\", after just \"noise\\n\"\)"):
        run_file(path)
    assert not record_path(path).exists()
    assert not (tmp_path / "first_action_models.cert.json").exists()


def test_a_first_action_is_validated_once_recorded_and_then_served(tmp_path, capsys, monkeypatch):
    from luthier import certify
    path = _first_action_copy(tmp_path) / "first_action_honest.run.lut"
    store = tmp_path / "first_action_models.cert.json"
    for k in range(2):
        assert main(["run", str(path)]) == 0
    assert capsys.readouterr().out == "once\n" * 2
    runs = json.loads(record_path(path).read_text(encoding="utf-8"))
    firsts = [r["certification"]["first actions"] for r in runs]
    # the action's law and the frame law (HostChangesOnlyDeclared) on the same case, each an entry
    laws = [("HostAgreesPrint", {"s": '"once"'}), ("HostChangesOnlyDeclared", {"s": '"once"'})]
    assert [[(f["action"], f["law"], f["arguments"], f["outcome"]) for f in fs] for fs in firsts] == [
        [("honest.print", law, a, "confirmed") for law, a in laws],
        [("honest.print", law, a, "served") for law, a in laws]]
    assert firsts[0][0]["store"] == str(store) and firsts[1][0]["entry"] == firsts[0][0]["entry"]
    entries = json.loads(store.read_text(encoding="utf-8"))
    assert len(entries) == 2
    entry = next(e for e in entries if e["law"] == "HostAgreesPrint")
    assert (entry["law"], entry["grade"], entry["outcome"], entry["cases"]) == ("HostAgreesPrint", "Cases", "Passed", 1)
    # D-2026-10-16-k item 9: the binding is the model alone, at the hash of its cone; the run's
    # argument and the places the certifier adds (the standard output and the files read so far,
    # none) are the case's evidence
    assert [(b["parameter"], b["generator"]) for b in entry["binding"]] == [("o", "honest (the run's model)")]
    assert [(c["parameter"], c["value"], c["what"]) for c in entry["evidence"]["case"]] == [
        ("s", {"Printed": '"once"'}, "the run's argument"), ("extra", {"Printed": '["stdout"]'}, "the certifier's places")]
    frame = next(e for e in entries if e["law"] == "HostChangesOnlyDeclared")
    assert [(b["parameter"], b["generator"]) for b in frame["binding"]] == [("o", "honest (the run's model)")]
    assert [(c["parameter"], c["what"]) for c in frame["evidence"]["case"]] == [
        ("h", "the action held"), ("extra", "the certifier's places")]
    assert ["python:luthier.host.print_line", certify.host_hash("python:luthier.host.print_line")] in entry["hosts"]
    before = store.read_bytes()
    assert main(["run", str(path)]) == 0 and store.read_bytes() == before
    # D-2026-10-16-k item 9: another argument at the same hash of the model's cone is served by the
    # entry confirmed at the first, its arguments evidence and not part of the demand
    other = tmp_path / "first_action_other.run.lut"
    other.write_text(path.read_text(encoding="utf-8").replace('"once"', '"again"'), encoding="utf-8")
    assert main(["run", str(other)]) == 0 and store.read_bytes() == before
    again = json.loads(record_path(other).read_text(encoding="utf-8"))[-1]["certification"]["first actions"]
    assert [(f["outcome"], f["arguments"], f["entry"]) for f in again][0] == ("served", {"s": '"again"'}, firsts[0][0]["entry"])
    # the host's code changed: the model's cone is at another hash, so validated again (10.S9)
    monkeypatch.setattr(certify, "host_hash", lambda route: "changed " + route)
    assert main(["run", str(path)]) == 0
    assert json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]["first actions"][0]["outcome"] == "confirmed"
    capsys.readouterr()


FIRST_ACTION_LAWS = """\
import "test.lth" test ExhaustiveMode
import "generators.lth" Binding
import "laws.lth" Listed
import "world.lth" Host Observed HostAgreesPrint
import "world_model.lut" WorldState
import "first_action_models.lut" honest
bind (p g : String) : Binding := { parameter := just p, type := nothing, generator := g, coverage := Listed }
Key = WorldState
states : List Concrete := [Key]
hosts : List (Host WorldState) := [honest]
once : List String := ["once"]
blank : WorldState := { stdout := "", files := nil }
cases : List (Observed WorldState Unit) := [{ before := blank, result := unit, after := { stdout := "once\\n", files := nil } }]
test "HostAgreesPrint" ExhaustiveMode (seed <- 20261015) (whereBindings <- [bind "S" "states", bind "o" "hosts",
  bind "s" "once", bind "c" "cases"])
"""


def test_a_testers_entry_on_the_model_never_serves_its_first_action(tmp_path, capsys):
    # report-e.md, finding 2: a test line certifies HostAgreesPrint on `honest` over a listed case
    # at s = "once", and its entry lands in the model's store (honest's file is its home). Its
    # reach is widened to the places the run adds, so that it covers every value the run gives:
    # at the same law cone and model hash it would serve the run's demand but for its kind. The run
    # still gathers its own case (10.S10) and writes an entry of the first action's kind.
    from luthier import certify, tester
    _first_action_copy(tmp_path)
    laws = tmp_path / "first_action_laws.test.lut"
    laws.write_text(FIRST_ACTION_LAWS, encoding="utf-8")
    assert tester.passes(tester.run_tests(laws, store=True)[0])
    store = tmp_path / "first_action_models.cert.json"
    listed, = json.loads(store.read_text(encoding="utf-8"))
    assert listed["law"] == "HostAgreesPrint" and "kind" not in listed and certify.entry_kind(listed) is None
    listed["reach"].append({"parameter": "extra", "reach": {"Members": [{"Printed": '["stdout"]'}]}})
    store.write_text(json.dumps([listed]), encoding="utf-8")
    path = tmp_path / "first_action_honest.run.lut"
    assert main(["run", str(path)]) == 0 and capsys.readouterr().out == "once\n"
    firsts = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]["first actions"]
    assert [(f["law"], f["outcome"]) for f in firsts] == [("HostAgreesPrint", "confirmed"),
                                                          ("HostChangesOnlyDeclared", "confirmed")]
    entries = json.loads(store.read_text(encoding="utf-8"))
    own = next(e for e in entries if e["law"] == "HostAgreesPrint" and e.get("kind") == certify.FIRST_ACTION)
    # the run's demand, as FirstActions makes it: without its kind the listed entry would serve it
    demand = {"law": own["law"], "cone": own["cone"], "accepts": "Cases",
              "given": [(r["parameter"], r["reach"]["Members"][0]) for r in own["reach"]],
              "fingerprints": {"o": own["binding"][0]["fingerprint"]}}
    assert certify.serves(demand, listed) and not certify.serves(demand, own)
    demand["kind"] = certify.FIRST_ACTION
    assert not certify.serves(demand, listed) and certify.serves(demand, own)


def test_the_protocols_observations_change_nothing(tmp_path, monkeypatch, capsys):
    # observe.run.lut's first print and first observe are validated (HostAgreesPrint,
    # HostObserveChangesNothing); the protocol's observations add nothing to what is printed
    (tmp_path / "input.txt").write_text("first line\n", encoding="utf-8")
    path = tmp_path / "observe.run.lut"
    path.write_text((RUN / "observe.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert main(["run", str(path)]) == 0
    assert capsys.readouterr().out == "one\none\n\n\nfirst line\n\n"
    firsts = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]["first actions"]
    assert [(f["action"], f["law"]) for f in firsts] == [
        ("host.print", "HostAgreesPrint"), ("host.print", "HostChangesOnlyDeclared"),
        ("host.observe", "HostObserveChangesNothing"), ("host.observe", "HostChangesOnlyDeclared")]


# ---------------------------------------------------------------- the demand and the plan as values
# (record/IA/run-2026-10-13/prompt-13.md; demand.lth, plan.lth, record/IA/demand-2026-10-15/report.md)

def _surface_value(x):
    """A default argument as demand_model.lut writes it, as Python reads it."""
    if isinstance(x, s.Literal):
        return x.literal.value
    if isinstance(x, s.List):
        return tuple(_surface_value(v) for v in x.values)
    return {"nil": (), "false": False, "true": True, "nothing": None}.get(x.name, x.name)


def test_the_runs_defaults_are_demand_models():
    # L5.19, P11: the default of each argument of `run` is declared in demand_model.lut's
    # `theDemand`; run.DEMAND_DEFAULTS mirrors it
    from luthier.parse import parse
    from luthier.run import DEMAND_DEFAULTS
    program = parse((LIB / "demand_model.lut").read_text(encoding="utf-8")).program
    the_demand = next(a for a in program if isinstance(a, s.Define) and a.name == "theDemand")
    declared = {b.names[0]: _surface_value(b.default) for b in the_demand.binders}
    assert declared == dict(DEMAND_DEFAULTS, pinned=None)


def test_the_demand_records_every_policy(tmp_path, capsys):
    # audit II.2, L5.18: `axioms`, `roots` and `combine` are fields of the demand with declared defaults
    # (demand_model.lut's `theDemand`), and the run's record lists them
    from luthier.run import demand_of
    d = demand_of()
    assert (d.axioms, d.roots, d.combine) == ("AssumedGrade", ("FileSystemKeeps", "SystemDelivers"), "weakest")
    rec = demand_of(axioms="Cases", roots=["R"], combine="strongest").record("sha256:c")
    assert (rec["axioms"], rec["roots"], rec["combine"]) == ("cases", ["R"], "strongest")
    # an axiom is accepted as assumed under a stricter cutoff only when its law is named
    strict = demand_of(accept="Cases")
    assert strict.law("SystemDelivers", "sha256:c", [], {}, axiom=True)["accepts"] == "AssumedGrade"
    assert strict.law("OtherAxiom", "sha256:c", [], {}, axiom=True)["accepts"] == "Cases"
    assert demand_of(accept="Cases", assumes=["OtherAxiom"]).law(
        "OtherAxiom", "sha256:c", [], {}, axiom=True)["accepts"] == "AssumedGrade"
    # and the run's record on disk
    path = tmp_path / "holes.run.lut"
    path.write_text(HOLES.read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path), "--set", "graphDir=a", "--set", "loud=false"]) == 0
    state = json.loads((tmp_path / "holes.run.json").read_text(encoding="utf-8"))[-1]
    assert state["demand"]["axioms"] == "assumed" and state["demand"]["roots"] == ["FileSystemKeeps", "SystemDelivers"]
    assert state["demand"]["combine"] == "weakest"


def test_inner_keeps_every_cutoff_and_a_law_demand_carries_the_runs():
    from luthier.run import demand_of
    d = demand_of("main", 99, {"x": 1}, "Cases", True, "v0.2")
    assert d.inner("law") == demand_of("law", 99, {"x": 1}, "Cases", True, "v0.2")
    assert d.law("L", "sha256:c", [("x", {"Number": 1.0})], {})["accepts"] == "Cases"
    # no fuel bound by default (D-2026-10-16-d)
    assert demand_of().accepts == "Sampled" and demand_of().fuel is None


def test_every_demand_on_a_law_is_passed_down_from_the_runs(tmp_path, monkeypatch, capsys):
    # PassedDownNotRecomputed (L12.3): the demand on each law of the cone and on each first action
    # carries the run's cutoff, whatever it is
    from luthier import certify
    seen = []
    serves = certify.serves

    def spy(demand, entry):
        seen.append((demand["law"], demand["accepts"]))
        return serves(demand, entry)
    monkeypatch.setattr(certify, "serves", spy)
    path = _hello(tmp_path)
    assert main(["run", str(path), "--accept", "assumed"]) == 0
    assert {law for law, _ in seen} >= {"HostAgreesPrint"} and len({law for law, _ in seen}) > 1
    assert {accepts for _, accepts in seen} == {"AssumedGrade"}


def test_the_record_holds_the_demand_the_plan_and_the_key(tmp_path, capsys):
    # RecordsEveryCutoff (12.S18, L5.18): the demand as one object; PlanIsTheLiveCone (L5.13): e is
    # not produced; the call-by-need schedule (8.S4); KeyReadsOnlyTheCone (8.S8): unusedHole is
    # recorded as given and stays out of the key; the plan's hash is the same for the same plan (L5.6)
    path = tmp_path / "plan_cone.run.lut"
    path.write_text((RUN / "plan_cone.run.lut").read_text(encoding="utf-8"), encoding="utf-8")
    for unused in ("7", "8"):
        assert main(["run", str(path), "--set", "usedHole=1", "--set", f"unusedHole={unused}", "--fuel", "5000"]) == 0
    assert capsys.readouterr().out == "5\n5\n"
    runs = json.loads(record_path(path).read_text(encoding="utf-8"))
    first, second = runs
    d = first["demand"]
    assert d == {"entry": "main", "cone": first["certification"]["cone"],
                 "parameters": {"usedHole": 1, "unusedHole": 7}, "accept": "sampled", "assumes": [], "delta": 0.05,
                 "fuel": 5000, "timeLimit": None, "checked": False, "lock": None, "decoration": None,
                 "strategy": "ForwardOnDemand", "fresh": False,
                 "axioms": "assumed", "roots": ["FileSystemKeeps", "SystemDelivers"], "combine": "weakest", "bound": 1.0,
                 "composition": "cappedSumComposition"}
    # the fields kept beside it say the same
    assert (first["entry"], first["parameters"], first["checked"], first["fuel"]["given"],
            first["certification"]["accept"]) == (d["entry"], d["parameters"], d["checked"], d["fuel"], d["accept"])
    plan = first["plan"]
    assert plan["strategy"] == "CallByNeed" and plan["entry"] == "main"
    assert {"a", "b", "c", "d", "usedHole", "main"} <= set(plan["live"])
    assert "e" not in plan["live"] and "unusedHole" not in plan["live"]
    assert plan["schedule"] == ["a", "b", "c", "d"]
    assert plan["hash"].startswith("sha256:") and plan == second["plan"]
    assert first["key"] == second["key"] == {"decoration": None, "values": {"usedHole": 1}}
    assert second["demand"]["parameters"]["unusedHole"] == 8


def test_the_plans_hash_sees_the_schedule():
    # PlanHashSeesTheSchedule (L5.6)
    from luthier.run import plan_hash
    plan = {"strategy": "CallByNeed", "entry": "main", "live": ["a", "b", "c"], "schedule": ["a", "b", "c"]}
    assert plan_hash(plan) == plan_hash(dict(plan))
    assert plan_hash(plan) != plan_hash(dict(plan, schedule=["a", "c", "b"]))


def test_a_reader_of_the_runs_reports_a_breach_of_determined(tmp_path):
    # demand.lth's `Runs` (8.S3): one demand record, one result; x.run.json is not served from
    from luthier.run import read_runs
    path = tmp_path / "x.lut"
    one = {"entry": "main", "cone": "sha256:c", "parameters": {}, "accept": "sampled", "delta": None,
           "fuel": 1, "checked": False, "lock": None}
    runs = [{"demand": one, "output": "1\n"}, {"output": "2\n"}, {"demand": dict(one, fuel=2), "output": "2\n"},
            {"demand": one, "output": "1\n"}, {"demand": one, "output": "3\n"}]
    record_path(path).write_text(json.dumps(runs), encoding="utf-8")
    assert read_runs(path) == (runs, [(0, 4), (3, 4)])
    assert read_runs(tmp_path / "none.lut") == ([], [])


def _evaluate(path, name, label=None):
    """A definition of a file (a projection of it, with `label`) reduced in every part by the Runner,
    shown; the file's imports loaded as `run` loads them, nothing certified."""
    from luthier import term as t
    from luthier.run import Runner, _elaborated, _type_shown, core_data, runtime_slice
    loaded = Loaded(path)
    entry = loaded.name(loaded.top, name)
    runner = Runner(_elaborated(runtime_slice(loaded.acts, entry, core_data(loaded))), 10_000_000)
    term = t.Var(entry) if label is None else t.Proj(t.Var(entry), label)
    return _type_shown(runner.value(term), 1000)


def test_the_example_plans_linearize_and_agree():
    # PlanIsConfluent, PlanLinearizes, TheDefaultsAgree on plan_model.lut's `example` (8.S4, 8.S5,
    # 8.S11): call by need and forward on demand each linearize the live cone, and they and a third
    # linearization by hand give every live name one value
    model = LIB / "plan_model.lut"
    assert _evaluate(model, "bothLinearize") == "true"
    assert _evaluate(model, "schedulesAgree") == "true"
    a_b_c_d = 'cons "a" (cons "b" (cons "c" (cons "d" nil)))'
    assert _evaluate(model, "needPlan", "schedule") == _evaluate(model, "forwardPlan", "schedule") == a_b_c_d


def test_a_pattern_variable_is_never_another_files_constructor(tmp_path, capsys):
    # the core's bite 4, finding 3 (2.S12: a pattern variable is a binder): a.lut's data has the
    # constructor `name`, which b.run.lut does not list; in b's `schema name ->` it is a variable.
    # The elaborator's constructors are every file's, so before the loader renamed the variable the
    # arm read the constructor, never matched, and `describe` stuck on every `schema` violation.
    (tmp_path / "a.lut").write_text(
        'Shape : U := data { name : String -> Shape }\n'
        'label : String := match name "a" { name s -> s }\n', encoding="utf-8")
    path = tmp_path / "b.run.lut"
    path.write_text(
        'import "a.lut" label\n'
        'Violation = { schema : String || other : Unit }\n'
        'describe (v : Violation) : String := match v { schema name -> name ; other u -> "other" }\n'
        'say (w : W) (x : String) : W * Unit := extern "python:luthier.host.print_line" w x\n'
        'main (w : W) : W * Unit := say w (describe (schema label))\n', encoding="utf-8")
    loaded = Loaded(path)
    arms = next(a for a in loaded.acts if getattr(a, "name", None) == "describe").body.term.arms
    assert arms[0][0] == s.PApp("schema", (s.PApp("name%var", ()),)) and arms[0][1] == s.Name("name%var")
    assert main(["run", str(path)]) == 0
    assert capsys.readouterr().out == "a\n"


# ---------------------------------------------------------------- the refusal's holes, at load
# (record/plan/core-2026-10-17/review-bite-5.md findings 1, 2a to 2c; D-2026-10-18-b, 12.S22)

def test_a_core_collision_exempts_only_the_file_it_lists_at_load(tmp_path, monkeypatch):
    import luthier.run as run
    monkeypatch.setattr(run, "CORE_COLLISIONS", {"core/properties/relations.lth": ("Reflexive", "a test")})
    path = tmp_path / "mine.lut"
    path.write_text("Reflexive : Bool := true\n", encoding="utf-8")
    with pytest.raises(RunError) as error:
        Loaded(path)
    assert "mine.lut defines Reflexive, which the core defines in core/properties/relations.lth" in str(error.value)


@pytest.mark.parametrize("text, message", [
    ("operator + := intMinus\n", "minus.lut's operator + := intMinus rebinds +, which the core binds to intPlus in core/core.lut"),
    ("S = { unit : Int || compose : Int }\n", "minus.lut defines compose, which the core defines in core/core.lut"),
    ("import \"core/structures/algebraic.lth\" Monoid as compose\n", "minus.lut defines compose, which the core defines in core/core.lut")])
def test_an_operator_a_label_and_an_import_alias_of_a_core_name_are_refused_at_load(tmp_path, text, message):
    # findings 2a to 2c: before, `luthier eval` of `5 + 2` with the first gave 7, the core's meaning
    path = tmp_path / "minus.lut"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(RunError) as error:
        Loaded(path)
    assert message in str(error.value)


@pytest.mark.parametrize("term, value", [
    ('all List String (fn x { x == "a" }) ["a"]', "true"),
    ('any List Nat (fn x { x == 2 }) [1, 2]', "true"),
    ('all List Nat (fn x { x == 1 }) [1, 2]', "false")])
def test_eval_reduces_a_term_over_the_cores_foldable_model(tmp_path, term, value):
    # the slice reached `foldList` only through a field written free or qualified by its structure,
    # not through `f.fold` of a parameter typed by it, so `all List ...` printed as `foldList ...`
    from luthier.run import evaluate
    path = tmp_path / "x.lut"
    path.write_text("x : Nat := 1\n", encoding="utf-8")
    result, _, _ = evaluate([str(path)], term)
    assert result == s_true_false(value)


@pytest.mark.parametrize("term, value", [
    ("finiteDistance 0.0 == infiniteDistance unit", "false"),
    ("infiniteDistance unit == infiniteDistance", "true"),
    ("finiteDistance 1.0 == finiteDistance 1.0", "true")])
def test_eval_of_a_bare_term_reads_the_labels_of_an_aliased_sum(tmp_path, term, value):
    # report-night-T.md item 3: the term names `Extended`'s labels and no definition typed by it, and
    # the probe's slice kept no sum to read them from, so `==` stayed stuck
    from luthier.run import evaluate
    path = tmp_path / "x.lut"
    path.write_text('import "core/structures/equality.lth" Extended\nx : Extended := infiniteDistance unit\n',
                    encoding="utf-8")
    result, _, _ = evaluate([str(path)], term)
    assert result == s_true_false(value)


def s_true_false(value):
    from luthier import term as t
    return t.Var(value)


def test_a_store_listing_two_of_three_conjuncts_does_not_serve_a_run(tmp_path, capsys):
    """Wave A, A4 follow-up (audit 1.3): the run's demand carries the law's conjuncts as its definition
    states them (`Cones.conjuncts`). A store whose entries list only two of the theory's three
    conjuncts, the third removed from them, no longer admits the run (before, the run read the
    conjuncts from the entries and was served)."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from test_certify import CONJ_THEORY, CONJ_MODELS, CONJ_TEST, CONJ_RUN_OPS
    for name, text in [("ops.lth", CONJ_THEORY), ("ops.lut", CONJ_MODELS), ("ops.test.lut", CONJ_TEST),
                       ("ops.run.lut", CONJ_RUN_OPS)]:
        (tmp_path / name).write_text(text, encoding="utf-8")
    assert main(["certify", str(tmp_path / "ops.test.lut")]) == 0
    capsys.readouterr()
    assert main(["run", str(tmp_path / "ops.run.lut")]) == 0, capsys.readouterr()
    store = tmp_path / "ops.cert.json"
    entries = json.loads(store.read_text(encoding="utf-8"))
    dropped = sorted({e["conjunct"] for e in entries})[-1]
    kept = [dict(e, conjuncts=[c for c in e.get("conjuncts") or () if c != dropped])
            for e in entries if e["conjunct"] != dropped]
    assert kept and len(kept) < len(entries)
    store.write_text(json.dumps(kept), encoding="utf-8")
    capsys.readouterr()
    assert main(["run", str(tmp_path / "ops.run.lut"), "--fresh"]) != 0


def test_the_runtime_slice_keeps_implies(tmp_path, capsys):
    """Wave A, A3 follow-up: `1 < 0 -> true` reduces to a Bool under `eval`, core's `implies` being a root
    of the slice (before, it printed `implies false true`)."""
    path = tmp_path / "imp.lut"
    path.write_text("main : Bool := 1 < 0 -> true\n", encoding="utf-8")
    assert main(["eval", str(path), "main"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("true") and "implies" not in out


# D-2026-10-16-n, night agent P (2026-10-26): `print` writes at once and checks what `write()`
# returns, failing the action when the system rejects the bytes; the standard output is observed by
# what it is connected to (a file re-read, a pipe by its tee, a terminal or a device by the bytes it
# accepted); a file is checked by re-reading it; the roots of trust are declared once per project
# (luthier.lock's `roots`) and listed in every run's record.

TWO_LINES = ('import "world_model.lut" HostConsole host : HostConsole\n\n'
             'main (w : W) : W * Unit := match host.print w "first line" { (w1, u) -> host.print w1 "second line" }\n')


def _run_into(path, out, *args):
    """`luthier run path args` in a process whose standard output is the file `out` (a path, such as
    /dev/full); its standard error and the run's last record."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join((str(ROOT / "src"), str(ROOT / "tests")))
    with open(out, "wb") as f:
        result = subprocess.run([sys.executable, "-m", "luthier.cli", "run", str(path), *args], stdout=f,
                                stderr=subprocess.PIPE, text=True, env=env, cwd=path.parent)
    runs = json.loads(record_path(path).read_text(encoding="utf-8")) if record_path(path).exists() else []
    return result, (runs[-1] if runs else None)


@pytest.mark.skipif(not Path("/dev/full").exists(), reason="no /dev/full on this system")
def test_a_print_the_system_rejects_fails_the_run(tmp_path):
    # `luthier run hello.run.lut > /dev/full` was recorded as a finished run with output "hello, world"
    # (D-2026-10-16-n's case): now the write fails, the run with it, and the record says so
    result, rec = _run_into(_hello(tmp_path), "/dev/full")
    assert result.returncode == 1 and "No space left on device" in result.stderr
    assert rec["finished"] is False and rec["cut"]["reason"] == "action failed" and "output" not in rec
    assert rec["stdout"] == {"kind": "device", "observed": "accepted", "root": "SystemDelivers", "accepted": 0}


def test_stdout_is_observed_by_what_it_is_connected_to(tmp_path):
    path = _hello(tmp_path)
    out = tmp_path / "out.txt"
    result, rec = _run_into(path, out)
    assert result.returncode == 0, result.stderr
    assert out.read_text(encoding="utf-8") == "hello, world\n" and rec["output"] == "hello, world\n"
    assert rec["stdout"] == {"kind": "file", "observed": "re-read", "root": "FileSystemKeeps", "accepted": 13}
    piped = command(path, record=True)
    assert piped.returncode == 0 and piped.stdout == "hello, world\n"
    assert piped.record["stdout"] == {"kind": "pipe", "observed": "tee", "root": "SystemDelivers", "accepted": 13}


def _corrupting(monkeypatch, which=lambda k: True):
    """The system's `write` as a file system that says it took every byte and kept other ones (each
    'l' an 'X'), on the writes `which` picks by their order."""
    real, seen = os.write, []

    def write(fd, data):
        seen.append(fd)
        data = bytes(data)
        return real(fd, data.replace(b"l", b"X")) if which(len(seen)) else real(fd, data)
    monkeypatch.setattr(host.os, "write", write)


def test_a_file_that_keeps_other_bytes_is_seen_by_rereading_it(tmp_path, monkeypatch):
    # the observation of a file is its re-read, so a write accepted and not kept refuses the run at the
    # first action (or, if an entry served that action, at the end of the run); before, the host
    # observed its own copy and the run passed
    path = _hello(tmp_path)
    _corrupting(monkeypatch)
    with open(tmp_path / "out.txt", "w", encoding="utf-8") as out:
        with pytest.raises(RunError, match="stdout"):
            run_file(path, stream=out)
    assert (tmp_path / "out.txt").read_text(encoding="utf-8") == "heXXo, worXd\n"


def test_a_later_print_is_checked_at_the_end_of_the_run(tmp_path, monkeypatch):
    # the first print is validated at its first action; the second is not, and the file's re-read at
    # the end of the run sees that it kept other bytes
    path = tmp_path / "two.run.lut"
    path.write_text(TWO_LINES, encoding="utf-8")
    _corrupting(monkeypatch, which=lambda k: k == 2)
    with open(tmp_path / "out.txt", "w", encoding="utf-8") as out:
        with pytest.raises(RunError, match=r"stdout, a file, reads back 'Xine\\n' at character 18"):
            run_file(path, stream=out)
    assert (tmp_path / "out.txt").read_text(encoding="utf-8") == "first line\nsecond Xine\n"


def test_a_pipe_is_observed_by_its_tee_and_trusts_the_system(tmp_path, monkeypatch):
    # what a pipe's reader got cannot be read back: the run observes the bytes the pipe accepted, and
    # the record names the root of trust that rests on (world.lth's `SystemDelivers`)
    path = _hello(tmp_path)
    _corrupting(monkeypatch)
    r, w = os.pipe()
    with os.fdopen(w, "w") as out:
        output, _, state = run(path, stream=out)
    with os.fdopen(r, "rb") as got:
        assert got.read() == b"heXXo, worXd\n"
    assert output == "hello, world\n"
    assert state["stdout"] == {"kind": "pipe", "observed": "tee", "root": "SystemDelivers", "accepted": 13}


def test_the_roots_of_trust_are_the_projects(tmp_path, capsys):
    from luthier import certify
    path = _hello(tmp_path)
    lock = tmp_path / "luthier.lock"
    # no lock: the run writes it, declaring the roots it used, and its record lists them
    assert main(["run", str(path)]) == 0
    roots = ["FileSystemKeeps", "SystemDelivers"]
    assert json.loads(lock.read_text(encoding="utf-8")) == {"interpreter": certify.interpreter_revision(), "roots": roots}
    rec = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]
    assert rec["lock"]["roots"] == roots and rec["demand"]["roots"] == roots
    # a project that declares none trusts nothing below its laws: the host's roots are refused
    lock.write_text(json.dumps({"interpreter": certify.interpreter_revision(), "roots": []}), encoding="utf-8")
    with pytest.raises(Refused, match="FileSystemKeeps"):
        run_file(path)
    # one it declares is accepted, and the other is refused
    lock.write_text(json.dumps({"interpreter": certify.interpreter_revision(), "roots": ["FileSystemKeeps"]}),
                    encoding="utf-8")
    with pytest.raises(Refused, match="SystemDelivers") as refusal:
        run_file(path)
    assert "FileSystemKeeps" not in str(refusal.value)
    # a lock with no `roots` leaves the demand's defaults, and the record says the lock declared none
    lock.write_text(json.dumps({"interpreter": certify.interpreter_revision()}), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    rec = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]
    assert rec["lock"]["roots"] is None and rec["demand"]["roots"] == roots
    lock.write_text(json.dumps({"interpreter": certify.interpreter_revision(), "roots": "FileSystemKeeps"}),
                    encoding="utf-8")
    with pytest.raises(RunError, match="not a list of names"):
        run_file(path)


def test_the_record_is_checked_by_rereading_it(tmp_path, monkeypatch, capsys):
    # a file system that keeps one byte less than it was given: the record's write is seen to fail
    path = _hello(tmp_path)
    assert main(["run", str(path)]) == 0
    real = Path.write_bytes

    def short(self, data):
        return real(self, data[:-1])
    monkeypatch.setattr(Path, "write_bytes", short)
    from luthier.run import record
    with pytest.raises(RunError, match="does not read back what was written"):
        record(path, "main", {}, "hello, world\n")
