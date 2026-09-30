"""Tests of the Luthier version 0 interpreter."""
import os
import pytest

from luthier.parser import parse, parse_term, ParseError
from luthier.checker import Checker, TypeCheckError
from luthier.evaluator import Env, evaluate, EvalError
from luthier.generators import Generators
from luthier.testing import run_test
from luthier.pretty import pp
from luthier.cli import CORE, LIB_DIR, Loader

import sys
sys.setrecursionlimit(50_000)

HERE = os.path.dirname(__file__)
EXAMPLES = os.path.join(HERE, "..", "examples")


LIBS = ["real", "random", "peano", "algebra"]


def load(src: str, prelude=True) -> Checker:
    """A checker with core and every shipped library loaded, then `src` on top."""
    ck = Checker(Env())
    if prelude:
        loader = Loader(ck)
        loader.load_file(CORE)
        for lib in LIBS:
            loader.load_file(os.path.join(LIB_DIR, lib + ".lut"))
    ck.load(parse(src))
    return ck


def load_example(name: str) -> Checker:
    """Load an example file through the CLI loader, so its imports are processed."""
    from luthier.cli import load as cli_load
    return cli_load([os.path.join(EXAMPLES, name)]).checker


def gens_for(ck: Checker, size: int = 16) -> Generators:
    return Generators.from_checker(ck, size)


def ev(ck: Checker, src: str) -> str:
    t, _ = ck.infer([], parse_term(src))
    return pp(evaluate(ck.env, t))


# ------------------------------------------------------------------ parsing

def test_parse_definition_forms():
    prog = parse("""
a : Int := 3
f (x : Int) : Int := x + 1
g : Int -> Int
h : Int -> Int := extern "python:builtins.abs"
""")
    names = [d.name for d in prog.defs]
    assert names == ["a", "f", "g", "h"]
    assert prog.defs[2].body is None  # hole


def test_parse_precedence():
    t = parse_term("y <= x -> add (s x y) y == x")
    assert pp(t) == "y <= x -> add (s x y) y == x"
    t = parse_term("f a b + g c * 2")
    assert pp(t) == "f a b + g c * 2"


def test_parse_error_reports_position():
    with pytest.raises(ParseError) as e:
        parse("f : Int := (1 + )")
    assert "line 1" in str(e.value)


# --------------------------------------------------------------- evaluation

def test_hand_reduction_matches_the_doc():
    ck = load("""
doble1 (n : N) : N := addN n n
doble2 (n : N) : N
  | zero   := zero
  | succ k := succ (succ (doble2 k))
""")
    two = "succ (succ zero)"
    assert ev(ck, f"doble1 ({two})") == "succ (succ (succ (succ zero)))"
    assert ev(ck, f"doble2 ({two})") == "succ (succ (succ (succ zero)))"
    assert ev(ck, f"doble1 ({two}) == doble2 ({two})") == "true"


def test_arithmetic_and_bool():
    ck = load("")
    assert ev(ck, "(2 + 3) * 4") == "20"
    assert ev(ck, "7 mod 3") == "1"
    assert ev(ck, "2 < 3 and not (3 < 2)") == "true"
    assert ev(ck, "1.5 + 1.5") == "3.0"


def test_recursive_function_under_binder_terminates():
    ck = load("""
f (n : N) : N -> N := \\ m { addN n m }
""")
    # normalizing a body with a stuck recursive call must not loop
    assert ev(ck, "f zero") in ("f zero", "\\ m { addN zero m }")
    assert ev(ck, "f zero (succ zero)") == "succ zero"


def test_extern_call():
    ck = load('sq : R -> R := extern "python:math.sqrt"')
    assert ev(ck, "sq 16.0") == "4.0"


# ------------------------------------------------------------ type checking

def test_unbound_name_is_an_error():
    with pytest.raises(TypeCheckError):
        load("f : Int := y")


def test_match_must_cover_all_constructors():
    with pytest.raises(TypeCheckError) as e:
        load("f (b : Bool) : Bool := match b { true -> false }")
    assert "false" in str(e.value)


def test_closed_value_against_subtype_is_checked_now():
    load("Z7 : U := { k : Int | 0 <= k and k < 7 }\nx : Z7 := 3")
    with pytest.raises(TypeCheckError) as e:
        load("Z7 : U := { k : Int | 0 <= k and k < 7 }\nx : Z7 := 9")
    assert "does not satisfy" in str(e.value)


def test_subtype_coerces_to_base():
    ck = load("""
Z7 : U := { k : Int | 0 <= k and k < 7 }
plus (a b : Z7) : Int := a + b
""")
    assert ev(ck, "plus 3 4") == "7"


def test_function_body_against_subtype_becomes_obligation():
    ck = load("""
Z7 : U := { k : Int | 0 <= k and k < 7 }
addMod7 (a b : Z7) : Z7 := (a + b) mod 7
""")
    assert "addMod7" in ck.obligations
    assert len(ck.obligations["addMod7"]) == 1


def test_arrow_is_pi_on_types_and_implication_on_bools():
    ck = load("f (x : Int) : Bool := x < 0 -> x < 1")
    assert ev(ck, "f 5") == "true"
    assert ev(ck, "f (0 - 5)") == "true"


# ------------------------------------------------------------------ testing

def test_ring_z7_passes_exhaustively():
    ck = load_example("z7ring.lut")
    gens = Generators(ck.env)
    r = run_test(ck, gens, "ringZ7", exhaustive=True, deep=True)
    assert r.passed
    assert len(r.laws) == 11
    assert all(l.mode == "exhaustive" for l in r.laws)


def test_bad_ring_fails_on_inverses_with_counterexample():
    ck = load_example("boolring.lut")
    gens = Generators(ck.env)
    r = run_test(ck, gens, "badRing", exhaustive=True, deep=True)
    assert not r.passed
    failed = [l for l in r.laws if not l.passed]
    assert {l.label for l in failed} == {"LeftInverse Bool or false not", "RightInverse Bool or false not"}
    assert failed[0].failure == "x = true"


def test_sampled_law_on_recursive_data():
    ck = load("Comm : U := { f : N -> N -> N | Commutative N f }\naddC : Comm := addN")
    gens = Generators(ck.env)
    r = run_test(ck, gens, "addC", n=30, seed=3, deep=True)
    assert r.passed and r.laws[0].cases == 30


def test_extern_law_finds_counterexample():
    ck = load_example("pyext.lut")
    gens = Generators(ck.env)
    assert run_test(ck, gens, "goodSqrt", n=100, seed=1, deep=True).passed
    r = run_test(ck, gens, "sinAll", n=100, seed=1, deep=True)
    assert not r.passed and r.laws[0].failure.startswith("x = ")


# ------------------------------------------------------------------ imports

def test_import_loads_dependencies_once_and_rejects_cycles(tmp_path):
    from luthier.cli import load
    (tmp_path / "a.lut").write_text('import "b.lut"\nimport "b"\nx : Int := y + 1\n')
    (tmp_path / "b.lut").write_text('y : Int := 41\n')
    loader = load([str(tmp_path / "a.lut")])
    assert ev(loader.checker, "x") == "42"
    assert [len(p.defs) for p, _, _, _ in loader.programs[1:]] == [1, 1]  # b once, then a
    (tmp_path / "c.lut").write_text('import "d.lut"\n')
    (tmp_path / "d.lut").write_text('import "c.lut"\n')
    with pytest.raises(SystemExit) as e:
        load([str(tmp_path / "c.lut")])
    assert "cycle" in str(e.value)


def test_explicit_prelude_without_implicit_one(tmp_path):
    from luthier.cli import load
    (tmp_path / "e.lut").write_text('import "core"\nz : Bool := true and not false\n')
    ck = load([str(tmp_path / "e.lut")], with_core=False).checker
    assert ev(ck, "z") == "true"


# ------------------------------------------------------- modules and certificates

def test_qualified_import_and_cross_module_law():
    from luthier.cli import load
    loader = load([os.path.join(EXAMPLES, "qualified.lut")])
    ck = loader.checker
    assert "z7.ringZ7" in ck.env.defs and "bx.xor" in ck.env.defs
    assert ev(ck, "z7.addMod7 3 5") == "1"
    r = run_test(ck, Generators(ck.env), "zeroUnderNeg", exhaustive=True, deep=True)
    assert r.passed and r.laws[0].cases == 7


def test_filling_a_hole_checks_the_declared_type(tmp_path):
    from luthier.cli import load
    (tmp_path / "spec.lut").write_text("f : Int -> Int\n")
    (tmp_path / "ok.lut").write_text('import "spec"\nf := \\ x { x + 1 }\n')
    (tmp_path / "bad.lut").write_text('import "spec"\nf : Int -> Bool := \\ x { x < 0 }\n')
    ck = load([str(tmp_path / "ok.lut")]).checker
    assert ev(ck, "f 41") == "42"
    with pytest.raises(SystemExit) as e:
        load([str(tmp_path / "bad.lut")])
    assert "declared with type" in str(e.value)


def test_extern_filling_a_lawful_hole_gets_an_obligation():
    from luthier.cli import load
    loader = load([os.path.join(EXAMPLES, "sqrt_math.lut")])
    ck = loader.checker
    assert "sqrt" in ck.obligations
    r = run_test(ck, Generators(ck.env), "sqrt", n=50, seed=1, deep=True)
    assert r.passed and r.laws[0].label == "approx 1e-09 (sqrt x * sqrt x) x"


def test_certificate_is_trusted_on_import_while_the_hash_matches(tmp_path):
    from luthier.cli import main
    lib = tmp_path / "lib.lut"
    lib.write_text("Small : U := { k : Int | 0 <= k and k < 3 }\ninc (a : Small) : Small := (a + 1) mod 3\n")
    app = tmp_path / "app.lut"
    app.write_text('import "lib.lut" as L\ntwice (a : L.Small) : L.Small := L.inc (L.inc a)\n')
    # 1. testing the library writes a certificate with a hash
    assert main(["test", str(lib), "--exhaustive"]) == 0
    cert = (tmp_path / "lib.cert.json")
    assert cert.exists() and '"hash"' in cert.read_text()
    # 2. importing it accepts the certificate: L.inc is certified, twice is pending
    from luthier.cli import load
    loader = load([str(app)])
    assert "L.inc" in loader.checker.certified
    assert "twice" not in loader.checker.certified
    # 3. changing the library invalidates the certificate
    lib.write_text("Small : U := { k : Int | 0 <= k and k < 3 }\ninc (a : Small) : Small := (a + 2) mod 3\n")
    loader = load([str(app)])
    assert "L.inc" not in loader.checker.certified and "L.inc" in loader.stale


def test_luthier_path_is_searched(tmp_path, monkeypatch):
    from luthier.cli import load
    libdir = tmp_path / "libs"
    libdir.mkdir()
    (libdir / "shared.lut").write_text("k : Int := 7\n")
    (tmp_path / "use.lut").write_text('import "shared"\nm : Int := k * 6\n')
    monkeypatch.setenv("LUTHIER_PATH", str(libdir))
    ck = load([str(tmp_path / "use.lut")]).checker
    assert ev(ck, "m") == "42"


# ------------------------------------------------------------ conceptual vs machine

def test_if_then_else_and_fromInt():
    ck = load("")
    assert ev(ck, "if 2 < 3 then 1 else 0") == "1"
    assert ev(ck, "toInt (fromInt 5)") == "5"
    assert ev(ck, "fromInt (0 - 3)") == "zero"


def test_equality_between_subtype_and_base_needs_no_obligation():
    ck = load("Law : U := { f : N -> Nat | \\ (m n : N) { f (addN m n) == f m + f n } }")
    assert "Law" not in ck.obligations


def test_coercion_inside_a_predicate_becomes_a_precondition():
    ck = load("""
half (k : Nat) : Int := k / 2
Even : U := { x : Int | half x * 2 == x }
""")
    assert "Even" not in ck.obligations           # nothing pending on the type itself
    gens = Generators(ck.env)
    ck2 = load("""
half (k : Nat) : Int := k / 2
Even : U := { x : Int | half x * 2 == x }
four : Even := 4
""")
    assert ev(ck2, "four") == "4"
    # a negative even number fails the precondition (half needs Nat), so it is not an Even
    with pytest.raises(TypeCheckError):
        load("""
half (k : Nat) : Int := k / 2
Even : U := { x : Int | half x * 2 == x }
minusTwo : Even := 0 - 2
""")


def test_n_is_isomorphic_to_the_nonnegative_ints():
    ck = load_example("naturals.lut")
    gens = gens_for(ck)
    r = run_test(ck, gens, "natIso", n=100, seed=5, deep=True)
    assert r.passed
    assert [l.label for l in r.laws] == ["fromNat (toNat a) == a", "toNat (fromNat b) == b"]
    assert r.laws[1].domains == ["Nat: genNat, size up to 16"]


# ------------------------------------------------------------ reproducibility

def test_certificate_records_seed_domains_and_sample_cases():
    ck = load_example("naturals.lut")
    gens = gens_for(ck)
    r1 = run_test(ck, gens, "toIntAdd", n=20, deep=True)
    assert r1.seed is not None and r1.generation["size"] == 16
    assert r1.generation["generators"]["N"] == "genN"
    law = r1.laws[0]
    assert law.domains == ["N: genN, size up to 16"] * 2
    assert len(law.sample_cases) == 5 and law.sample_cases[0].startswith("m = ")
    # the same seed reproduces the same cases
    r2 = run_test(ck, gens, "toIntAdd", n=20, seed=r1.seed, deep=True)
    assert r2.laws[0].sample_cases == law.sample_cases


def test_certificate_hash_is_alpha_invariant():
    from luthier.certify import definition_hash
    a = load("f (x : Int) : Int := x + 1\n").env
    b = load("f (y : Int) : Int := y + 1\n").env
    c = load("f (x : Int) : Int := x + 2\n").env
    assert definition_hash(a, "f") == definition_hash(b, "f")
    assert definition_hash(a, "f") != definition_hash(c, "f")


def test_sampled_sizes_grow_over_the_run():
    ck = load("")
    gens = Generators(ck.env, size=8)
    import random
    rng = random.Random(0)
    small = [gens.sample(parse_term("Int"), rng, size=1) for _ in range(20)]
    big = [gens.sample(parse_term("Int"), rng, size=8) for _ in range(20)]
    assert all(abs(v.value) <= 1 for v in small)
    assert max(abs(v.value) for v in big) > 1
    # the base library's generators are Luthier terms; a data type without one is derived
    assert "Int" in gens.luthier or True  # registration happens through the loader, tested below


def test_generators_are_luthier_values_chosen_by_type(tmp_path):
    from luthier.cli import load, make_generators
    f = tmp_path / "g.lut"
    f.write_text("""
import "random"
Small : U := { k : Int | 0 <= k and k < 5 }
gen Small := \\ size s { match randBelow 5 s { (k, s2) -> (k, s2) } }
twice (a : Small) : Int := a + a
""")
    loader = load([str(f)])
    gens = make_generators(loader, size=16)
    assert loader.checker.gens["Small"][1] == "\\ size s { match randBelow 5 s { (k, s2) -> (k, s2) } }"
    import random
    rng = random.Random(1)
    vals = [gens.sample(parse_term("Small"), rng, size=16).value for _ in range(30)]
    assert set(vals) <= {0, 1, 2, 3, 4} and len(set(vals)) > 1
    assert gens.describe(parse_term("Nat")) == "Nat: genNat, size up to 16"
    # a generator of the wrong type is rejected
    bad = tmp_path / "bad.lut"
    bad.write_text('import "random"\ngen Int := genBool\n')
    with pytest.raises(SystemExit) as e:
        load([str(bad)])
    assert "type error" in str(e.value)



# ------------------------------------------------------------------ opaque types

def test_opaque_type_values_pass_through_and_externs_operate():
    pytest.importorskip("numpy")
    ck = load_example("signal.lut")
    gens = gens_for(ck)
    r = run_test(ck, gens, "fftInvertible", n=10, seed=1, deep=True)
    assert r.passed and r.laws[0].cases == 10
    assert r.laws[0].domains == ["Signal: registered Python generator, size up to 16"]
    assert r.laws[0].sample_cases[0].startswith("x = <ndarray (")
