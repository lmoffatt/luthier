"""Runner integration tests derived from user request 2026-10-13, v1; v2 for world.lth draft 1 (prompt-2.md);
v4 for arrays, tables and numbers across the bridge (prompt-4.md); v6 for the loader's scopes and the
externs' arity (prompt-6.md)."""
import os
from dataclasses import fields, is_dataclass
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from luthier import arrays, host, surface as s
from luthier.cli import main
from luthier.run import Loaded, RunError, run_file

ROOT = Path(__file__).resolve().parents[1]


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


def matrix(u):
    return np.ones((2, 2))


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


def test_table_cell_through_csv(tmp_path):
    (tmp_path / "table.csv").write_text("id:int,name:str,x:float\n1,alpha,0.5\n2,beta,1.5\n", encoding="utf-8")
    result = command(ROOT / "tests/run/table_cell.lut", cwd=tmp_path)
    assert (result.returncode, result.stderr) == (0, "")
    assert result.stdout == "beta\n2\n1.5\na:int,b:str\n0,x\n1,x\n\n"


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
    result = command(ROOT / "examples/sonolocalizacion/validate_graph.lut", cwd=ROOT)
    assert result.returncode == 0, result.stderr
    assert result.stdout == EXPECTED_VALIDATE_GRAPH


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
# meaning: test.lth imports laws.lth's `Exhaustive`, generators.lth means its own theory
CLASHES = {
    "LeqPair": ("kernel_laws.lth", "algebra.lth", "numbers.lth"),
    "LeqChain": ("kernel_laws.lth", "algebra.lth", "numbers.lth"),
    "LeqBoth": ("kernel_laws.lth", "algebra.lth", "numbers.lth"),
    "PlusCommutes": ("kernel_laws.lth", "numbers.lth"),
    "NonNegative": ("generators.lth", "numbers.lth"),
    "Exhaustive": ("laws.lth", "generators.lth"),
    "Assumed": ("laws.lth", "test.lth"),
}
SEEN_FROM = {"Exhaustive": {"test.lth": "laws.lth", "generators.lth": "generators.lth"}}


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
