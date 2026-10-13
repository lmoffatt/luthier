"""Elaboration laws at 5d7963b; derived from user prompt 2026-10-13 v1.

All inputs are independent source texts parsed by luthier.parse.parse.
"""
from pathlib import Path
import os
import subprocess
import sys

import pytest
from luthier import term as t
from luthier.surface import Parsed, TermBody
from luthier.parse import parse
from luthier.elaborate import elaborate_program, elaborate_term, apps
from luthier.kernel import alpha_equal


def program(text):
    r = parse(text)
    assert isinstance(r, Parsed), r
    return r.program


def term(text, context=''):
    p = program(context + '\nresult := ' + text)
    assert isinstance(p[-1].body, TermBody)
    return elaborate_term(p[-1].body.term, p[:-1])


def eq(text, expected, context=''):
    assert alpha_equal(term(text, context), expected)


def peq(text, expected):
    actual = elaborate_program(program(text))
    assert len(actual) == len(expected)
    for a, b in zip(actual, expected):
        assert type(a) is type(b)
        if isinstance(a, t.Datum): assert alpha_equal(a.value, b.value)
        else:
            assert a.name == b.name
            assert alpha_equal(a.type, b.type)
            if isinstance(a, t.Define): assert alpha_equal(a.body, b.body)


V = t.Var
U = t.Universe()
I = V('Int')
def num(n): return t.Lit(t.IntConst(n))
def bin(op, a, b): return apps(V(op), [a, b])
def con(n, *ps): return t.PCon(n, ps)
def pv(n): return t.PVar(n)
SCOPE = 'A : U\nB : U\nx : Int\ny : Int\nf : Int -> Int\nm : Maybe Int\nn : Int * Int\nk : Int'
TYPES = 'A : U\nB : U\ni : Int\nj : Int\nc : Bool\nq : Bool\nf : Failures E'


def test_ActsCurried():
    peq('f (x : A) (y z : B <- w) : C := x', [t.Define('f', t.Pi('x', V('A'), t.Pi('y', V('B'), t.Pi('z', V('B'), V('C')))), t.Lam('x', V('A'), t.Lam('y', V('B'), t.Lam('z', V('B'), V('x')))))])


def test_ActsKept():
    peq('A : U\nB : U\nP = A * B\nx : P\ntest x', [t.Declare('A', U), t.Declare('B', U), t.Declare('x', t.Sigma('_', V('A'), V('B'))), t.Datum(t.App(V('test'), V('x')))])
    assert elaborate_program(program('operator + := addZ7\nimport "m.lut" module\naddZ7 : Int -> Int -> Int')) == (t.Declare('addZ7', t.Pi('_', I, t.Pi('_', I, I))),)


def test_Atoms():
    for text, expected in [('x', V('x')), ('3', num(3)), ('"s"', t.Lit(t.StringConst('s'))), ('U', U), ('W', t.World()), ('f x', t.App(V('f'), V('x')))]: eq(text, expected, SCOPE)
    eq('module.g', V('module.g'), 'import "m.lut" module')


def test_Lambdas():
    eq('fn (x y : A) { x }', t.Lam('x', V('A'), t.Lam('y', V('A'), V('x'))), SCOPE)


def test_Patterns():
    eq('match m { r -> 1; _ -> 2 }', t.Match(V('m'), ((con('r'), num(1)), (t.PWild(), num(2)))), 'C : U := data { r : C; s : C }\nm : C')
    eq('match m { just y -> y; w -> k }', t.Match(V('m'), ((con('just', pv('y')), V('y')), (pv('w'), V('k')))), SCOPE)
    eq('match n { (p, q) -> p }', t.Match(V('n'), ((t.PPair(pv('p'), pv('q')), V('p')),)), SCOPE)
    eq('match k { 0 -> x; _ -> y }', t.Match(V('k'), ((t.PLit(t.IntConst(0)), V('x')), (t.PWild(), V('y')))), SCOPE)


def test_Lists():
    eq('[x, y]', apps(V('cons'), [V('x'), apps(V('cons'), [V('y'), V('nil')])]), SCOPE)


def test_TypeForms():
    fs = (('x', V('A')), ('y', V('B')))
    eq('{ x : A || y : B }', t.Sum(fs), SCOPE)
    eq('{ x : A, y : B }', t.Record(fs), SCOPE)
    peq('C : U := data { r : C; s : List C -> C }', [t.Define('C', U, t.Data('C', (('r', V('C')), ('s', t.Pi('_', t.App(V('List'), V('C')), V('C'))))))])
    peq('A : U\nP (T : U) = T * T\nz : P A', [t.Declare('A', U), t.Declare('z', t.Sigma('_', V('A'), V('A')))])


def test_OperatorsByType():
    for text, expected in [('A -> B', t.Pi('_', V('A'), V('B'))), ('A * B', t.Sigma('_', V('A'), V('B'))), ('A + B', t.Sum((('left', V('A')), ('right', V('B'))))), ('i * j', bin('*', V('i'), V('j'))), ('i + j', bin('+', V('i'), V('j'))), ('c -> q', bin('implies', V('c'), V('q'))), ('c and q', bin('and', V('c'), V('q'))), ('c or q', bin('or', V('c'), V('q')))]: eq(text, expected, TYPES)


def test_Negation():
    eq('-i', bin('-', num(0), V('i')), TYPES)
    eq('-r', bin('-', t.Lit(t.FloatConst(0.0)), V('r')), 'r : Float64')


def test_Conditions():
    arms = ((con('true'), V('i')), (con('false'), V('j')))
    eq('if c then i else j', t.Match(V('c'), arms), TYPES)
    eq('if c then i', t.Match(V('c'), ((con('true'), t.App(V('just'), V('i'))), (con('false'), V('nothing')))), TYPES)
    eq('if f then i else j', t.Match(t.App(V('holds'), V('f')), arms), TYPES)
    eq('if f then i', t.Match(V('f'), ((con('nil'), t.App(V('ok'), V('i'))), (con('cons', pv('x'), pv('xs')), t.App(V('failed'), V('x'))))), TYPES)


def test_OperatorOfTheModel():
    eq('z + z', bin('addZ7', V('z'), V('z')), 'Z7 : U\nz : Z7\naddZ7 : Z7 -> Z7 -> Z7\noperator + := addZ7')


def test_Records():
    eq('{ x := u, y := v }', t.RecordValue((('x', V('u')), ('y', V('v')))), 'A : U\nB : U\nu : A\nv : B')
    eq('(r).y', t.Proj(V('r'), 'y'), 'A : U\nB : U\nr : { x : A, y : B }')


def test_Arguments():
    ctx = 'g (x : Int) (tol : Int <- 1) : Int\ni : Int\nj : Int'
    eq('g i (tol <- j)', apps(V('g'), [V('i'), V('j')]), ctx)
    eq('g i', apps(V('g'), [V('i'), num(1)]), ctx)
    eq('id i', apps(V('id'), [I, V('i')]), 'id {T : U} (y : T) : T\ni : Int')


def test_Blocks():
    eq('{ x := 1; x }', t.Let('x', I, num(1), V('x')))
    eq('{ w1 <- act w0; w1 }', t.Let('w1', t.World(), t.App(V('act'), V('w0')), V('w1')), 'act : W -> W\nw0 : W')
    eq('{ y <- 1; y <- y + 1; y }', t.Let('y0', I, num(1), t.Let('y1', I, bin('+', V('y0'), num(1)), V('y1'))))


def test_Shapes():
    a, b = V('A'), V('B'); pair = t.Sigma('_', a, b)
    peq('A : U\nB : U\nh : (A * B) -> A := fn (x, y) { x }', [t.Declare('A', U), t.Declare('B', U), t.Define('h', t.Pi('_', pair, a), t.Lam('p', pair, t.Match(V('p'), ((t.PPair(pv('x'), pv('y')), V('x')),))))])
    peq('both2 (b c : Bool) : Bool\n  | true, d := d\n  | _, _ := false', [t.Define('both2', t.Pi('b', V('Bool'), t.Pi('c', V('Bool'), V('Bool'))), t.Lam('b', V('Bool'), t.Lam('c', V('Bool'), t.Match(t.Pair(V('b'), V('c')), ((t.PPair(con('true'), pv('d')), V('d')), (t.PPair(t.PWild(), t.PWild()), V('false')))))))])
    peq('nt (b : Bool) : Bool\n  | true := false\n  | false := true', [t.Define('nt', t.Pi('b', V('Bool'), V('Bool')), t.Lam('b', V('Bool'), t.Match(V('b'), ((con('true'), V('false')), (con('false'), V('true'))))))])


ROOT = Path(__file__).parents[1]
def cli(*args):
    env = os.environ.copy(); env['PYTHONPATH'] = str(ROOT / 'src')
    return subprocess.run([sys.executable, '-m', 'luthier.cli', 'eval', *map(str, args)], capture_output=True, text=True, env=env)


@pytest.mark.parametrize('file,output', [('arithmetic', '19'), ('factorial', '24'), ('data', '2'), ('record', '7'), ('block', '3'), ('lambda', '5')])
def test_eval(file, output):
    r = cli(ROOT / 'tests/eval' / (file + '.lut'), 'answer')
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.strip() == output


@pytest.mark.parametrize('name,fuel,message', [('missing', '100', 'unknown definition'), ('answer', '0', 'fuel spent')])
def test_eval_errors(name, fuel, message):
    r = cli(ROOT / 'tests/eval/arithmetic.lut', name, '--fuel', fuel)
    assert r.returncode == 1
    assert message in r.stdout


def test_eval_parse_error(tmp_path):
    path = tmp_path / 'bad.lut'; path.write_text('answer := (')
    r = cli(path, 'answer')
    assert r.returncode == 1
    assert str(path) in r.stdout


def test_fresh_names_avoid_capture():
    eq('{ y <- 1; y <- y + 1; y + y0 }',
       t.Let('a', I, num(1), t.Let('b', I, bin('+', V('a'), num(1)), bin('+', V('b'), V('y0')))),
       'y0 : Int')


def test_extern_remains_stuck():
    eq('extern "host.route" 3', t.App(t.Extern('host.route'), num(3)))
