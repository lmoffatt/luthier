"""Mechanisms of the interpreter under the specification of 04 and 05: parsing, evaluation,
obligations, `test`, certificates, imports, projections, operators, the bridge with Python.
Self-contained: every program here loads only core.lut."""
import math
import os
import random

import pytest

import luthier
from luthier import FillError
from luthier.parser import parse, parse_term, ParseError
from luthier.checker import Checker, TypeCheckError
from luthier.evaluator import Env, evaluate
from luthier.generators import Generators
from luthier.testing import run_test
from luthier.pretty import pp
from luthier.cli import CORE, Loader

import sys
sys.setrecursionlimit(50_000)


def load(src: str) -> Checker:
    """A checker with core.lut loaded, then `src` on top."""
    ck = Checker(Env())
    Loader(ck).load_file(CORE)
    ck.load(parse(src))
    return ck


def ev(ck: Checker, src: str) -> str:
    with ck.silent():
        t, _ = ck.infer([], parse_term(src))
    return pp(evaluate(ck.env, t))


def write(tmp_path, name, src):
    p = tmp_path / name
    p.write_text(src)
    return str(p)


PEANO = """
N : U := data { zero : N ; succ : N -> N }
addN (m n : N) : N := match n { zero -> m ; succ k -> succ (addN m k) }
"""

LAWS = """
Associative (A : U) (eq : A -> A -> Bool) (f : A -> A -> A) (x y z : A) : Bool := eq (f (f x y) z) (f x (f y z))
Commutative (A : U) (eq : A -> A -> Bool) (f : A -> A -> A) (x y : A) : Bool := eq (f x y) (f y x)
RightIdentity (A : U) (eq : A -> A -> Bool) (f : A -> A -> A) (e : A) (x : A) : Bool := eq (f x e) x
RightInverse (A : U) (eq : A -> A -> Bool) (f : A -> A -> A) (e : A) (inv : A -> A) (x : A) : Bool := eq (f x (inv x)) e
Group (A : U) : U := { eq : A -> A -> Bool, add : A -> A -> A, zero : A, neg : A -> A |
  Associative A eq add & Commutative A eq add & RightIdentity A eq add zero & RightInverse A eq add zero neg }
"""


# ------------------------------------------------------------------ parsing

def test_parse_definition_forms():
    prog = parse("""
a : Int := 3
f (x : Int) : Int := x + 1
g : Int -> Int
h : Int -> Int := extern "python:builtins.abs"
S = Int + Bool
""")
    assert [d.name for d in prog.defs] == ["a", "f", "g", "h", "S"]
    assert prog.defs[2].body is None
    assert prog.defs[4].alias


def test_parse_precedence():
    assert pp(parse_term("y <= x -> add (s x y) y == x")) == "y <= x -> add (s x y) y == x"
    assert pp(parse_term("f a b + g c * 2")) == "f a b + g c * 2"


def test_parse_error_reports_position():
    with pytest.raises(ParseError) as e:
        parse("f : Int := (1 + )")
    assert "line 1" in str(e.value)


# ------------------------------------------------------------------ evaluation

def test_arithmetic_bool_and_if():
    ck = load("")
    assert ev(ck, "(2 + 3) * 4") == "20"
    assert ev(ck, "7 mod 3") == "1"
    assert ev(ck, "2 < 3 and not (3 < 2)") == "true"
    assert ev(ck, "1.5 + 1.5") == "3.0"
    assert ev(ck, "if 2 < 3 then 1 else 0") == "1"


def test_recursion_on_data_and_clauses():
    ck = load(PEANO + """
double (n : N) : N
  | zero   := zero
  | succ k := succ (succ (double k))
""")
    two = "succ (succ zero)"
    assert ev(ck, f"addN ({two}) ({two})") == "succ (succ (succ (succ zero)))"
    assert ev(ck, f"double ({two}) == addN ({two}) ({two})") == "true"


def test_sums_inject_by_label_and_match_on_labels():
    ck = load("""
Shape = < circle : R | square : R >
area (s : Shape) : R := match s { circle r -> 3.0 * r * r ; square a -> a * a }
c : Shape := circle 2.0
S = Int + Bool
s : S := right true
""")
    assert ev(ck, "area c") == "12.0"
    assert ev(ck, "area (square 3.0)") == "9.0"
    assert ev(ck, "match s { left n -> n ; right b -> 0 }") == "0"
    assert ev(ck, "c == circle 2.0") == "true"


def test_maybe_and_bool_are_sums_from_core():
    ck = load("""
safeDiv (a b : Int) : Maybe Int := if b == 0 then nothing else just (a / b)
orZero (m : Maybe Int) : Int := match m { nothing -> 0 ; just k -> k }
""")
    assert ev(ck, "orZero (safeDiv 7 2)") == "3"
    assert ev(ck, "orZero (safeDiv 7 0)") == "0"
    _, ty = ck.infer([], parse_term("true"))
    assert pp(ty) == "Bool"


def test_extern_call():
    ck = load('sq : R -> R := extern "python:math.sqrt"')
    assert ev(ck, "sq 16.0") == "4.0"


def test_order_in_the_file_does_not_matter():
    ck = load("""
b : Int := a + 1
a : Int := 41
isEven (n : Int) : Bool := if n == 0 then true else isOdd (n - 1)
isOdd (n : Int) : Bool := if n == 0 then false else isEven (n - 1)
""")
    assert ev(ck, "b") == "42"
    assert ev(ck, "isEven 10") == "true"


# ------------------------------------------------------------ type checking

def test_unbound_name_is_an_error():
    with pytest.raises(TypeCheckError):
        load("f : Int := y")


def test_match_must_cover_every_label():
    with pytest.raises(TypeCheckError) as e:
        load("f (b : Bool) : Bool := match b { true -> false }")
    assert "false" in str(e.value)


def test_closed_value_against_subtype_is_checked_now():
    load("Z7 : U := { k : Int | 0 <= k and k < 7 }\nx : Z7 := 3")
    with pytest.raises(TypeCheckError) as e:
        load("Z7 : U := { k : Int | 0 <= k and k < 7 }\nx : Z7 := 9")
    assert "does not satisfy" in str(e.value)


def test_subtype_coerces_to_base_and_bodies_become_obligations():
    ck = load("""
Z7 : U := { k : Int | 0 <= k and k < 7 }
plus (a b : Z7) : Int := a + b
addMod7 (a b : Z7) : Z7 := (a + b) mod 7
""")
    assert ev(ck, "plus 3 4") == "7"
    assert len(ck.obligations["addMod7"]) == 1


def test_arrow_is_pi_on_types_and_implication_on_bools():
    ck = load("f (x : Int) : Bool := x < 0 -> x < 1")
    assert ev(ck, "f 5") == "true"


def test_a_declared_type_defined_by_its_laws_has_their_obligations():
    ck = load("""
Codec : { parse : String -> Maybe Int, render : Int -> String }
RoundTrip (c : Codec) (n : Int) : Bool := match c.parse (c.render n) { nothing -> false ; just m -> m == n }
Codec := RoundTrip
show : Int -> String := extern "python:builtins.str"
read (s : String) : Maybe Int := just 0
bad : Codec := { parse := read, render := show }
""")
    assert "bad" in ck.obligations
    r = run_test(ck, Generators(ck.env), "bad", n=50, seed=1, deep=True)
    assert not r.passed


# ------------------------------------------------------------------ testing

def test_a_group_passes_exhaustively_and_a_wrong_one_fails_with_a_counterexample():
    ck = load(LAWS + """
Z3 : U := { k : Int | 0 <= k and k < 3 }
eqZ (a b : Z3) : Bool := a == b
z3 : Group Z3 := (eqZ, \\ a b { (a + b) mod 3 }, 0, \\ a { (3 - a) mod 3 })
eqB (a b : Bool) : Bool := a == b
xorB (a b : Bool) : Bool := not (a == b)
badGroup : Group Bool := (eqB, or, false, not)
""")
    gens = Generators(ck.env)
    r = run_test(ck, gens, "z3", exhaustive=True, deep=True)
    # the four group laws, and the closure of the two lambdas into Z3
    assert r.passed and all(l.mode == "exhaustive" for l in r.laws) and len(r.laws) == 6
    r = run_test(ck, gens, "badGroup", exhaustive=True, deep=True)
    failed = [l for l in r.laws if not l.passed]
    assert [l.label for l in failed] == ["RightInverse Bool eqB or false not"]
    assert failed[0].failure == "x = true"


def test_sampled_law_on_recursive_data():
    ck = load(PEANO + LAWS + """
eqN (a b : N) : Bool := a == b
Comm : U := { f : N -> N -> N | Commutative N eqN f }
addC : Comm := addN
""")
    r = run_test(ck, Generators(ck.env), "addC", n=30, seed=3, deep=True)
    assert r.passed and r.laws[0].cases == 30


def test_laws_over_sums_are_enumerated():
    ck = load("""
Dir = < north : Unit | south : Unit | east : Unit | west : Unit >
flip (d : Dir) : Dir := match d { north -> south ; south -> north ; east -> west ; west -> east }
Involution : U := { f : Dir -> Dir | \\ (d : Dir) { f (f d) == d } }
flipI : Involution := flip
""")
    r = run_test(ck, Generators(ck.env), "flipI", exhaustive=True, deep=True)
    assert r.passed and r.laws[0].cases == 4


def test_certificate_records_seed_and_cases_and_the_seed_repeats_them():
    ck = load("Pos : U := { f : Int -> Int | \\ (x : Int) { f x * f x >= 0 } }\nsq : Pos := \\ x { x * x }")
    gens = Generators(ck.env)
    r1 = run_test(ck, gens, "sq", n=20, deep=True)
    assert r1.seed is not None and len(r1.laws[0].sample_cases) == 5
    r2 = run_test(ck, gens, "sq", n=20, seed=r1.seed, deep=True)
    assert r2.laws[0].sample_cases == r1.laws[0].sample_cases


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
    rng = random.Random(0)
    small = [gens.sample(parse_term("Int"), rng, size=1) for _ in range(20)]
    big = [gens.sample(parse_term("Int"), rng, size=8) for _ in range(20)]
    assert all(abs(v.value) <= 1 for v in small)
    assert max(abs(v.value) for v in big) > 1


# ------------------------------------------------------------------ imports

def test_import_loads_dependencies_once_and_rejects_cycles(tmp_path):
    from luthier.cli import load as cli_load
    write(tmp_path, "a.lut", 'import "b.lut"\nimport "b"\nx : Int := y + 1\n')
    write(tmp_path, "b.lut", 'y : Int := 41\n')
    loader = cli_load([str(tmp_path / "a.lut")])
    assert ev(loader.checker, "x") == "42"
    write(tmp_path, "c.lut", 'import "d.lut"\n')
    write(tmp_path, "d.lut", 'import "c.lut"\n')
    with pytest.raises(SystemExit) as e:
        cli_load([str(tmp_path / "c.lut")])
    assert "cycle" in str(e.value)


def test_filling_a_hole_checks_the_declared_type(tmp_path):
    from luthier.cli import load as cli_load
    write(tmp_path, "spec.lut", "f : Int -> Int\n")
    write(tmp_path, "ok.lut", 'import "spec"\nf := \\ x { x + 1 }\n')
    write(tmp_path, "bad.lut", 'import "spec"\nf : Int -> Bool := \\ x { x < 0 }\n')
    assert ev(cli_load([str(tmp_path / "ok.lut")]).checker, "f 41") == "42"
    with pytest.raises(SystemExit) as e:
        cli_load([str(tmp_path / "bad.lut")])
    assert "declared with type" in str(e.value)


def test_certificate_is_trusted_on_import_while_the_hash_matches(tmp_path):
    from luthier.cli import main, load as cli_load
    lib = tmp_path / "lib.lut"
    lib.write_text("Small : U := { k : Int | 0 <= k and k < 3 }\ninc (a : Small) : Small := (a + 1) mod 3\n")
    app = tmp_path / "app.lut"
    app.write_text('import "lib.lut" as L\ntwice (a : L.Small) : L.Small := L.inc (L.inc a)\n')
    assert main(["test", str(lib), "--exhaustive"]) == 0
    assert '"hash"' in (tmp_path / "lib.cert.json").read_text()
    loader = cli_load([str(app)])
    assert "L.inc" in loader.checker.certified and "twice" not in loader.checker.certified
    lib.write_text("Small : U := { k : Int | 0 <= k and k < 3 }\ninc (a : Small) : Small := (a + 2) mod 3\n")
    loader = cli_load([str(app)])
    assert "L.inc" not in loader.checker.certified and "L.inc" in loader.stale


def test_luthier_path_is_searched(tmp_path, monkeypatch):
    from luthier.cli import load as cli_load
    libdir = tmp_path / "libs"
    libdir.mkdir()
    (libdir / "shared.lut").write_text("k : Int := 7\n")
    write(tmp_path, "use.lut", 'import "shared"\nm : Int := k * 6\n')
    monkeypatch.setenv("LUTHIER_PATH", str(libdir))
    assert ev(cli_load([str(tmp_path / "use.lut")]).checker, "m") == "42"


def test_a_declared_type_of_one_file_is_defined_by_its_laws_in_another(tmp_path):
    from luthier.cli import load as cli_load
    write(tmp_path, "theory.lut", "Even : Int\n")
    write(tmp_path, "model.lut", 'import "theory"\nEven := \\ k { k mod 2 == 0 }\nfour : Even := 4\n')
    ck = cli_load([str(tmp_path / "model.lut")]).checker
    assert ev(ck, "four") == "4"


# ------------------------------------------------------------------ projections

def test_projection_of_named_components():
    ck = load("""
P = { x : R, y : R }
pt : P := (1.0, 2.0)
f (p : P) : R := p.x + p.y
""")
    assert ev(ck, "f pt") == "3.0"
    t, ty = ck.infer([], parse_term("pt.y"))
    assert pp(t) == "pt.y" and pp(ty) == "R"


def test_projection_through_refinements_aliases_and_parentheses():
    ck = load("""
Id (A : U) = A
Box (F : U -> U) = { v : F R, w : F R }
b : Box Id := (1.0, 2.0)
S : U := { inner : Box Id, k : R | k > 0.0 and inner.v <= inner.w }
Small : U := { s : S | s.k < 10.0 }
s : Small := ((1.0, 2.0), 3.0)
pick (q : Small) : R := q.inner.w + q.k
mk (x : R) : S := ((x, x), x)
""")
    assert ev(ck, "b.w") == "2.0"
    assert ev(ck, "pick s") == "5.0"
    assert ev(ck, "(mk 4.0).k") == "4.0"


def test_projection_of_a_dependent_component_types_against_the_value():
    ck = load("""
D = { n : Int, m : { k : Int | k <= n } }
d : D := (3, 2)
g (x : D) : Int := x.m + x.n
""")
    assert ev(ck, "g d") == "5"
    _, ty = ck.infer([], parse_term("d.m"))
    assert pp(ty) == "{ k : Int | k <= d.n }"


def test_projection_errors():
    with pytest.raises(TypeCheckError) as e:
        load("P = { x : R, y : R }\npt : P := (1.0, 2.0)\nz : R := pt.z")
    assert "no component z" in str(e.value)


# ------------------------------------------------------------------ operators by type

def test_operator_resolves_by_operand_types():
    ck = load("""
P = { a : Int, b : Int }
addP (p q : P) : P := (p.a + q.a, p.b + q.b)
scaleP (k : Int) (p : P) : P := (k * p.a, k * p.b)
operator + := addP
operator * := scaleP
firstOf (p : P) : Int := p.a
x : P := (1, 2)
y : P := 3 * x + x
z : Int := 3 * 4 + 1
""")
    assert ev(ck, "firstOf y") == "4"
    assert ev(ck, "z") == "13"


# ------------------------------------------------------------------ provisional

def test_provisional_externs_are_listed_and_never_certified(tmp_path, capsys):
    from luthier.cli import main
    path = write(tmp_path, "p.lut", '''
Signal : U := extern provisional "python:builtins.list"
duration : Signal -> Int := extern provisional "python:builtins.len"
''')
    assert main(["check", path, "-v"]) == 0
    out = capsys.readouterr().out
    assert "2 provisional" in out and "provisional duration: builds on Signal" in out


# ------------------------------------------------------------------ the Python side

def test_a_filled_hole_evaluates_and_its_laws_are_certified(tmp_path):
    path = write(tmp_path, "sq.lut", '''
Positive : U := { x : R | x > 0.0 }
close (a b : R) : Bool := a - b < 0.000000001 and b - a < 0.000000001
Sqrt : U := { f : Positive -> R | \\ (x : Positive) { close (f x * f x) x } }
root : Sqrt
twice (x : Positive) : R := root x + root x
''')
    P = luthier.load(path)
    assert P.holes() == ["root"]
    P.fill("root", math.sqrt)
    assert P.eval("twice 16.0") == 8.0
    r = P.test("root", n=50, seed=1)
    assert r.passed and r.laws[0].cases == 50
    assert os.path.exists(str(tmp_path / "sq.cert.json"))


def test_the_signature_is_checked_against_the_type(tmp_path):
    P = luthier.load(write(tmp_path, "f.lut", 'f : R -> R -> R\n'))
    with pytest.raises(FillError):
        P.fill("f", lambda a: a)
    P.fill("f", lambda a, b: a * b)
    assert P.eval("f 2.0 3.5") == 7.0


def test_records_and_sums_cross_both_ways(tmp_path):
    path = write(tmp_path, "pt.lut", '''
Pt = { x : R, y : R }
norm : Pt -> R
mk : R -> Pt
far (r : R) : R := norm (mk r)
Shape = < circle : R | square : R >
describe : Shape -> String
classify : R -> Shape
positive : R -> Bool
firstPositive : List R -> Maybe R
''')
    P = luthier.load(path)
    seen = []

    def norm(p):
        seen.append(p)
        return math.hypot(p.x, p.y)
    P.fill("norm", norm)
    assert P.eval("norm (3.0, 4.0)") == 5.0
    assert type(seen[0]).__name__ == "Pt"
    P.fill("mk", lambda r: (r, r))
    assert abs(P.eval("far 3.0") - math.sqrt(18.0)) < 1e-12
    P.fill("describe", lambda s: f"{s[0]} of {s[1]}")
    assert P.eval("describe (square 2.0)") == "square of 2.0"
    P.fill("classify", lambda r: ("circle", r) if r > 0 else ("square", -r))
    assert P.eval("classify 1.5") == ("circle", 1.5)
    P.fill("positive", lambda r: r > 0)
    assert P.eval("positive 2.0") is True and P.eval("if positive (0.0 - 1.0) then 1 else 2") == 2
    P.fill("firstPositive", lambda xs: next((x for x in xs if x > 0), None))
    assert P.eval("firstPositive [0.0 - 1.0, 2.0]") == 2.0
    assert P.eval("firstPositive [0.0 - 1.0]") is None


def test_a_luthier_function_passed_to_python_receives_typed_arguments(tmp_path):
    path = write(tmp_path, "fn.lut", '''
Pt = { x : R, y : R }
applyAt : (Pt -> R) -> R -> R
norm2 (p : Pt) : R := p.x * p.x + p.y * p.y
''')
    P = luthier.load(path)
    P.fill("applyAt", lambda f, r: f((r, r)))
    assert P.eval("applyAt norm2 3.0") == 18.0
