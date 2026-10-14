"""Runner integration tests derived from user request 2026-10-13, v1; v2 for world.lth draft 1 (prompt-2.md);
v4 for arrays, tables and numbers across the bridge (prompt-4.md); v6 for the loader's scopes and the
externs' arity (prompt-6.md); v7 for `run --set` and the run's record (prompt-7.md); v8 for functions
across the bridge (prompt-8.md, D-2026-10-14-a), the host side in tests/run/bridge_host.py; v13 for
run's refusal of a cone that is not certified (record/IA/certification-2026-10-14/prompt-run.md,
certification.lth §3, 12.S17), the programs under tests/run/certified/; v16 for the demand and the plan
as values (prompt-13.md; demand.lth, plan.lth), the program tests/run/plan_cone.lut."""
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
from luthier.run import Loaded, Refused, RunError, parameter, record_path, run_file

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
    # a file's text, each read counted (tests/run/read_once.lut)
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


def test_hello():
    result = command(ROOT / "examples/hello.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "hello, world\n", "")


def test_read_first_line(tmp_path):
    (tmp_path / "input.txt").write_text("first line\nsecond line\n", encoding="utf-8")
    result = command(ROOT / "tests/run/read_first_line.lut", cwd=tmp_path)
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
    assert run_file(ROOT / "examples/hello.lut") == "hello, world\n"
    assert host.observe(token, ["stdout"]) == (token, {"stdout": "hello, world\n", "files": []})


def test_observe_through_the_bridge(tmp_path):
    (tmp_path / "input.txt").write_text("first line\n", encoding="utf-8")
    result = command(ROOT / "tests/run/observe.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "one\none\n\n\nfirst line\n\n", "")


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


def test_missing_file_is_nothing(tmp_path):
    result = command(ROOT / "tests/run/read_first_line.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "no input.txt\n", "")


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


def test_vector_norm_through_numpy():
    result = command(ROOT / "tests/run/vector_norm.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "5.0\n", "")


def test_matrix_product_through_numpy():
    result = command(ROOT / "tests/run/matrix_product.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "43.0\n2\n", "")


@refused("csv : Codec, built : Codec")
def test_table_cell_through_csv(tmp_path):
    (tmp_path / "table.csv").write_text("id:int,name:str,x:float\n1,alpha,0.5\n2,beta,1.5\n", encoding="utf-8")
    result = command(ROOT / "tests/run/table_cell.lut", cwd=tmp_path)
    assert (result.returncode, result.stderr) == (0, "")
    assert result.stdout == "beta\n2\n1.5\na:int,b:str\n0,x\n1,x\n\n"


@refused("csv : Codec, built : Codec")
def test_table_not_parsed_is_nothing(tmp_path):
    (tmp_path / "table.csv").write_text("id:real\n1\n", encoding="utf-8")
    result = command(ROOT / "tests/run/table_cell.lut", cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "not a table\n", "")


def test_extern_in_a_record_is_read_when_projected():
    result = command(ROOT / "tests/run/record_externs.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "2.5\n", "")


def test_numbers_and_fin_functions():
    result = command(ROOT / "tests/run/numbers.lut")
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
    path = tmp_path / "bad.lut"
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
    path = tmp_path / "shape.lut"
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

CHECKED = ROOT / "tests" / "run" / "checked.lut"


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
    result = command(ROOT / "tests/run/vector_norm.lut", "--checked", record=True)
    assert (result.returncode, result.stdout, result.stderr) == (0, "5.0\n", "")
    assert (result.record["checked"], result.record["refinements"]) == (True, {})


def test_a_refined_record_and_a_type_family_cross(tmp_path):
    # the fit's crossings (record/IA/fit-host-2026-10-14/prompt.md): a record with a refinement
    # (belief.lth's `Settings`) crosses as its record, by key or attribute; a type family applied
    # (`VecOf 2`) is unfolded to the vectors of length 2 and crosses as an ndarray
    path = tmp_path / "families.lut"
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
    path = tmp_path / "once.lut"
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
    result = command(ROOT / "tests/run/connective_on_match.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "yes\n", "")


def test_host_cell_under_an_operator_crosses_first():
    # prompt-5.md: the Runner reduces a primitive's operands with the host
    result = command(ROOT / "tests/run/host_cell_under_operator.lut")
    assert (result.returncode, result.stdout, result.stderr) == (0, "8\n", "")


def test_bootstrap_primitives_and_not(tmp_path):
    # prompt-5.md: run_file defines kernel.BOOTSTRAP_PRIMITIVES; `not` is core's
    path = tmp_path / "ops.lut"
    path.write_text('''
print (w : W) (s : String) : W * Unit := extern "python:luthier.host.print_line" w s
main (w : W) : W * Unit := print w (if not (0 >= 3) and 7 mod 3 /= 0 and "ab" == "a" + "b" then "ok" else "no")
''')
    assert run_file(path) == "ok\n"


def test_equality_on_strings_and_parameterized_data(tmp_path):
    # prompt-10.md: `/=` on strings, `==` and `/=` on core's Maybe and List
    path = tmp_path / "eq.lut"
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
    result = command(ROOT / "examples/sonolocalizacion/validate_graph.lut",
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
        result = command(ROOT / "examples/sonolocalizacion/experiment_zero.lut",
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
    result = command(ROOT / "examples/sonolocalizacion/experiment_zero.lut",
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
    # left.lut and right.lut both define `helper`; left.lut's `not` is not core's elsewhere
    assert run_file(SCOPE / "main.lut") == "3 10 false true\n"


@pytest.mark.parametrize("program, message", [
    ("unlisted.lut", "unlisted.lut: helper is neither defined there, nor imported, nor core's"),
    ("missing_import.lut", "missing_import.lut imports twice from right.lut, which does not define it"),
])
def test_only_the_names_an_import_lists_enter(program, message):
    with pytest.raises(RunError) as error:
        run_file(SCOPE / program)
    assert str(error.value) == message


def test_the_loader_reads_no_more_than_the_import_lists(tmp_path):
    loaded = Loaded(SCOPE / "main.lut")
    top = loaded.top
    assert loaded.name(top, "twice") == "twice" and loaded.name(top, "ten") == "tenfold"
    assert loaded.name(top, "helper") is None and loaded.name(top, "tenfold") is None
    assert loaded.name(top, "not") == "not"  # core's
    assert loaded.name(SCOPE / "left.lut", "not") == "not@left"
    assert {loaded.name(SCOPE / f, "helper") for f in ("left.lut", "right.lut")} == {"helper@left", "helper@right"}


def test_a_label_and_another_files_definition_of_its_name_are_kept_apart():
    # prompt-10.md: generators.lth's import brings program.lth's `int : Term`, which took the name of
    # tables.lth's Cell label `int`, and `intAt` was a stuck match
    assert run_file(SCOPE / "label_and_definition.lut") == "7\n"
    loaded = Loaded(SCOPE / "label_and_definition.lut")
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
# (4a158b0).
CLASHES = {
    "LeqPair": ("kernel_laws.lth", "algebra.lth", "numbers.lth"),
    "LeqChain": ("kernel_laws.lth", "algebra.lth", "numbers.lth"),
    "LeqBoth": ("kernel_laws.lth", "algebra.lth"),
    "PlusCommutes": ("kernel_laws.lth", "numbers.lth"),
    "NonNegative": ("generators.lth", "numbers.lth"),
}
SEEN_FROM = {}


@pytest.fixture(scope="module")
def numbers_laws():
    return Loaded(ROOT / "tests" / "tester" / "numbers_laws.lut")


@pytest.mark.parametrize("name", CLASHES)
def test_a_name_several_libraries_define_does_not_collide(numbers_laws, name):
    loaded, files = numbers_laws, CLASHES[name]
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
    # the test file imports numbers.lth's PlusCommutes; kernel_laws.lth's is another definition
    assert numbers_laws.name(numbers_laws.top, "PlusCommutes") == "PlusCommutes@numbers"
    assert numbers_laws.name(numbers_laws.top, "LeqPair") is None


# ---------------------------------------------------------------- an extern's arity from its type

def test_the_arity_of_an_extern_is_its_declared_types():
    # math.log has no Python signature: typed, one argument by its type; untyped, taken as unary;
    # math.pi, declared a Float64, is the host's value
    assert run_file(ROOT / "tests" / "run" / "extern_arity.lut") == "0.0 3.141592653589793 0.0\n"


# ---------------------------------------------------------------- run --set fills the file's holes
# (record/IA/run-2026-10-13/prompt-7.md, 3.S9, 12.S18)

HOLES = ROOT / "tests" / "run" / "holes.lut"


@pytest.mark.parametrize("sets, output", [
    (("graphDir=a/b", "loud=false"), "a/b\n"),
    (("graphDir=a/b", "loud=true", "unused=-3"), "a/b!\n"),
])
def test_set_fills_the_holes(sets, output):
    assert run_file(HOLES, sets=sets) == output


@pytest.mark.parametrize("sets, message", [
    ((), "graphDir : String is a hole of holes.lut the run needs; give it with --set graphDir="),
    (("loud=true",), "graphDir : String is a hole of holes.lut the run needs"),
    (("graphDir=a", "loud=yes"), "--set loud=yes: not a literal of type Bool"),
    (("graphDir=a", "loud=true", "unused=1.5"), "--set unused=1.5: not a literal of type Int"),
    (("twice=3",), "twice (n : Int) : Int is not a parameter"),
    (("nope=1",), "nope is not a declared hole of holes.lut"),
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
    path = tmp_path / "holes.lut"
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
    assert run_file(RUN / "callbacks.lut") == "0.3\n"
    # CallsAreCounted: ten calls, keyed by the receiving extern's route and the argument
    assert host.calls() == {"python:run.bridge_host.maximize": {"1": 10}}


def test_the_calls_are_in_the_runs_record(tmp_path, capsys):
    path = tmp_path / "callbacks.lut"
    path.write_text((RUN / "callbacks.lut").read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    assert main(["run", str(path)]) == 0
    runs = json.loads((tmp_path / "callbacks.run.json").read_text(encoding="utf-8"))
    # each run counts its own calls (12.S18)
    assert [r["calls"] for r in runs] == [{"python:run.bridge_host.maximize": {"1": 10}}] * 2


def test_a_record_of_functions_crosses_by_field():
    # RecordCrossesByField: the host reads objective.value and objective.grad, each counted apart
    assert run_file(RUN / "record_of_functions.lut") == "3.0\n"
    assert host.calls() == {"python:run.bridge_host.descend": {"1.value": 3, "1.grad": 2}}


def test_a_host_function_given_back_is_applied_through_the_bridge():
    # HostGivesBackAValue and ExternIsValue: the host's closures cross in as host:k values, applied
    # by the bridge; one applied to a Luthier lambda calls it back, counted under its handle
    assert run_file(RUN / "host_function.lut") == "3.5\n18.0\n"
    assert host.calls() == {"host:2 run.bridge_host.twice_at.<locals>.at": {"1": 2}}


def test_an_extern_applied_to_fewer_arguments_is_a_value():
    # ExternPartialIsValue: add 1.0 waits for its second argument; handed to the host, add 1.0 is
    # a functools.partial of the host's add, written bare or with its parameters (eta)
    assert run_file(RUN / "extern_partial.lut") == (
        "3.5\npartial add (1.0,) 3.0\npartial add (1.0,) 3.0\n")
    assert host.calls() == {}


def test_a_callbacks_result_crosses_by_the_codomain(tmp_path):
    path = tmp_path / "bad_callback.lut"
    path.write_text(PRELUDE + '''
maximize (f : Float64 -> Float64) : Float64 := extern "python:run.bridge_host.maximize" f
main (w : W) : W * Unit := print w (showFloat (maximize (fn x { "no" })))
''', encoding="utf-8")
    with pytest.raises(RunError, match="not a Float64 at the crossing"):
        run_file(path)


# ---------------------------------------------------------------- a bound value is demanded once
# (record/IA/run-2026-10-13/prompt-9.md, 8.S4: call by need within a run)

@pytest.mark.parametrize("entry", ["main", "byArgument"])
def test_a_bound_read_is_made_once(tmp_path, entry):
    # read_once.lut observes one read twice, bound by a block or passed as an argument
    (tmp_path / "input.txt").write_text("data", encoding="utf-8")
    result = command(ROOT / "tests/run/read_once.lut", "--main", entry, cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, "data\ndata\n1\n", "")


def test_a_bound_maximize_runs_once(tmp_path):
    # maximize_shared.lut projects the result three times; each entry calls back exactly as
    # maximize_quadratic.lut, which matches it once (test_lm.py checks those counts against lm.py)
    for name in ("maximize_quadratic.lut", "maximize_shared.lut"):
        (tmp_path / name).write_text((ROOT / "tests/run" / name).read_text(encoding="utf-8"), encoding="utf-8")
    once = command(tmp_path / "maximize_quadratic.lut", cwd=tmp_path)
    assert once.returncode == 0, once.stderr
    expected = json.loads((tmp_path / "maximize_quadratic.run.json").read_text(encoding="utf-8"))[-1]["calls"]
    assert set(expected["python:luthier.lm.maximize"]) == {"3", "4", "5"}
    for entry in ("main", "byArgument"):
        result = command(tmp_path / "maximize_shared.lut", "--main", entry, cwd=tmp_path)
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
    outcomes = run_tests(tmp_path / "small.lut", store=True)
    assert [o.grade for o in outcomes] == ["Cases"]


def test_hellos_cone_runs_and_records_its_state(tmp_path, capsys):
    # hello.lut's cone (prompt-first-action.md): `console : Console State`, whose four laws
    # tests/tester/world_laws.lut certifies into world_model.cert.json, and `host : HostConsole =
    # Host State`, whose laws are run at an action's first application (10.S10); the rest vacuous
    path = tmp_path / "hello.lut"
    path.write_text((ROOT / "examples/hello.lut").read_text(encoding="utf-8"), encoding="utf-8")
    assert main(["run", str(path)]) == 0
    state = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]
    assert state["accept"] == "sampled" and state["laws"] == 4 and state["not certified"] == []
    assert state["states"]["certified"] == 1 and state["states"]["at first action"] == 1
    assert state["states"]["vacuous"] > 0
    assert {f["law"] for f in state["at first action"]} == {"HostAgreesPrint", "HostAgreesReadFile",
                                                            "HostObserveChangesNothing"}
    assert [(f["action"], f["outcome"]) for f in state["first actions"]] in (
        [("host.print", "served")], [("host.print", "confirmed")])
    assert state["cone"].startswith("sha256:")


def test_an_uncertified_cone_is_refused_per_law_and_nothing_runs(tmp_path, capsys):
    # RefusalSaysWhy: no entry at all, uncertified; exit 1, nothing evaluated, no record
    path = _certified_copy(tmp_path) / "uses_small.lut"
    assert main(["run", str(path)]) == 1
    out, err = capsys.readouterr()
    assert out == "" and "same: FixesBool: uncertified (no entry)" in err
    assert not record_path(path).exists()


def test_a_passed_entry_serves_at_or_above_the_cutoff(tmp_path, capsys):
    # ServesAtTheCutoff and ServesIsMonotoneInTheCutoff: the entry's grade is `cases`
    path = _certified_copy(tmp_path) / "uses_small.lut"
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
    path = _certified_copy(tmp_path) / "uses_small.lut"
    _certify_small(tmp_path)
    with pytest.raises(Refused, match="also: FixesBool: passed, but no passed entry's reach covers m = also"):
        run_file(path, main="other")


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
        run_file(tmp_path / "uses_small.lut")
    small.write_text(text.replace("m.f b == b", "(m.f b == b) and true"), encoding="utf-8")
    with pytest.raises(Refused, match=r"same: FixesBool: stale \(its entries are at \w+, the cone is now at \w+\)"):
        run_file(tmp_path / "uses_small.lut")


def test_a_provisional_name_is_refused_whole():
    # ProvisionalIsRefused
    with pytest.raises(Refused, match=r"shout: provisional") as refusal:
        run_file(CERTIFIED / "provisional.lut")
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
    # the certification of csv's laws is not the question here (they are graded by tables_laws.lut)
    monkeypatch.setattr("luthier.run.certification", lambda *a, **k: None)
    assert run_file(ROOT / "tests/run/table_names.lut", fuel=10_000_000) == "same\ndifferent\nsame\n"


# ---------------------------------------------------------------- the record completed, the lock
# (record/IA/run-2026-10-13/prompt-11.md; 12.S18, 12.S13)

def _hello(tmp_path):
    path = tmp_path / "hello.lut"
    path.write_text((ROOT / "examples/hello.lut").read_text(encoding="utf-8"), encoding="utf-8")
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
    path = tmp_path / "read_first_line.lut"
    path.write_text((RUN / "read_first_line.lut").read_text(encoding="utf-8"), encoding="utf-8")
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
    other = b / "other.lut"
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
    # absent: written beside the program, with the current revision
    assert main(["run", str(path)]) == 0
    assert json.loads(lock.read_text(encoding="utf-8")) == {"interpreter": certify.interpreter_revision()}
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
    for name in ("first_action_models.lut", "first_action_honest.lut", "first_action_liar.lut"):
        (tmp_path / name).write_text((RUN / name).read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def test_a_lying_print_is_refused_at_its_first_action_naming_the_place(tmp_path, capsys):
    # liar.print writes its line twice; HostAgreesPrint (world.lth's agreement) is refuted at the
    # run's own argument, the place named; nothing is recorded, no entry written
    path = _first_action_copy(tmp_path) / "first_action_liar.lut"
    with pytest.raises(Refused, match=r"liar\.print disagrees with its description at its first action .*"
                                      r"HostAgreesPrint at s = \"twice\": the place stdout differs"):
        run_file(path)
    assert main(["run", str(path)]) == 1
    out, err = capsys.readouterr()
    assert out == "" and '(described just "twice\\n", observed just "twice\\ntwice\\n")' in err
    assert not record_path(path).exists()
    assert not (tmp_path / "first_action_models.cert.json").exists()


def test_a_first_action_is_validated_once_recorded_and_then_served(tmp_path, capsys, monkeypatch):
    from luthier import certify
    path = _first_action_copy(tmp_path) / "first_action_honest.lut"
    store = tmp_path / "first_action_models.cert.json"
    for k in range(2):
        assert main(["run", str(path)]) == 0
    assert capsys.readouterr().out == "once\n" * 2
    runs = json.loads(record_path(path).read_text(encoding="utf-8"))
    firsts = [r["certification"]["first actions"] for r in runs]
    assert [[(f["action"], f["law"], f["arguments"], f["outcome"]) for f in fs] for fs in firsts] == [
        [("honest.print", "HostAgreesPrint", {"s": '"once"'}, "confirmed")],
        [("honest.print", "HostAgreesPrint", {"s": '"once"'}, "served")]]
    assert firsts[0][0]["store"] == str(store) and firsts[1][0]["entry"] == firsts[0][0]["entry"]
    entries = json.loads(store.read_text(encoding="utf-8"))
    assert len(entries) == 1
    entry = entries[0]
    assert (entry["law"], entry["grade"], entry["outcome"], entry["cases"]) == ("HostAgreesPrint", "Cases", "Passed", 1)
    assert [(b["parameter"], b["generator"]) for b in entry["binding"]] == [
        ("o", "honest (the run's model)"), ("s", '"once" (the run\'s argument)')]
    assert ["python:luthier.host.print_line", certify.host_hash("python:luthier.host.print_line")] in entry["hosts"]
    before = store.read_bytes()
    assert main(["run", str(path)]) == 0 and store.read_bytes() == before
    # another argument is another case, validated again
    other = tmp_path / "first_action_other.lut"
    other.write_text(path.read_text(encoding="utf-8").replace('"once"', '"again"'), encoding="utf-8")
    assert main(["run", str(other)]) == 0
    assert json.loads(record_path(other).read_text(encoding="utf-8"))[-1]["certification"]["first actions"][0]["outcome"] == "confirmed"
    # the host's code changed: the model's cone is at another hash, so validated again (10.S9)
    monkeypatch.setattr(certify, "host_hash", lambda route: "changed " + route)
    assert main(["run", str(path)]) == 0
    assert json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]["first actions"][0]["outcome"] == "confirmed"
    capsys.readouterr()


def test_the_protocols_observations_change_nothing(tmp_path, monkeypatch, capsys):
    # observe.lut's first print and first observe are validated (HostAgreesPrint,
    # HostObserveChangesNothing); the protocol's observations add nothing to what is printed
    (tmp_path / "input.txt").write_text("first line\n", encoding="utf-8")
    path = tmp_path / "observe.lut"
    path.write_text((RUN / "observe.lut").read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert main(["run", str(path)]) == 0
    assert capsys.readouterr().out == "one\none\n\n\nfirst line\n\n"
    firsts = json.loads(record_path(path).read_text(encoding="utf-8"))[-1]["certification"]["first actions"]
    assert [(f["action"], f["law"]) for f in firsts] == [("host.print", "HostAgreesPrint"),
                                                         ("host.observe", "HostObserveChangesNothing")]


# ---------------------------------------------------------------- the demand and the plan as values
# (record/IA/run-2026-10-13/prompt-13.md; demand.lth, plan.lth, record/IA/demand-2026-10-15/report.md)

def _surface_value(x):
    """A default argument as demand_model.lut writes it, as Python reads it."""
    if isinstance(x, s.Literal):
        return x.literal.value
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


def test_inner_keeps_every_cutoff_and_a_law_demand_carries_the_runs():
    from luthier.run import demand_of
    d = demand_of("main", 99, {"x": 1}, "Cases", True, "v0.2")
    assert d.inner("law") == demand_of("law", 99, {"x": 1}, "Cases", True, "v0.2")
    assert d.law("L", "sha256:c", [("x", {"Number": 1.0})], {})["accepts"] == "Cases"
    assert demand_of().accepts == "Sampled" and demand_of().fuel == 10_000_000


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
    path = tmp_path / "plan_cone.lut"
    path.write_text((RUN / "plan_cone.lut").read_text(encoding="utf-8"), encoding="utf-8")
    for unused in ("7", "8"):
        assert main(["run", str(path), "--set", "usedHole=1", "--set", f"unusedHole={unused}", "--fuel", "5000"]) == 0
    assert capsys.readouterr().out == "5\n5\n"
    runs = json.loads(record_path(path).read_text(encoding="utf-8"))
    first, second = runs
    d = first["demand"]
    assert d == {"entry": "main", "cone": first["certification"]["cone"],
                 "parameters": {"usedHole": 1, "unusedHole": 7}, "accept": "sampled", "delta": None,
                 "fuel": 5000, "checked": False, "lock": None}
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
    assert _evaluate(model, "agree") == "true"
    a_b_c_d = 'cons "a" (cons "b" (cons "c" (cons "d" nil)))'
    assert _evaluate(model, "needPlan", "schedule") == _evaluate(model, "forwardPlan", "schedule") == a_b_c_d
