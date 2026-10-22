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
from luthier.elaborate import ElaborationError, TypingError, elaborate_program, elaborate_term, apps
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
    # at Bool, since `+` at Int is the core's, which a file does not rebind (12.S22, D-2026-10-18-b)
    B = V('Bool')
    assert elaborate_program(program('operator + := addZ7\nimport "m.lut" module\naddZ7 : Bool -> Bool -> Bool')) == (t.Declare('addZ7', t.Pi('_', B, t.Pi('_', B, B))),)


def test_Atoms():
    for text, expected in [('x', V('x')), ('3', num(3)), ('"s"', t.Lit(t.StringConst('s'))), ('U', U), ('W', t.World()), ('f x', t.App(V('f'), V('x')))]: eq(text, expected, SCOPE)
    eq('module.g', V('module.g'), 'import "m.lut" module')


def test_Lambdas():
    eq('fn (x y : A) { x }', t.Lam('x', V('A'), t.Lam('y', V('A'), V('x'))), SCOPE)


def test_lambda_declared_expected_type():
    predicate = t.Lam('n', I, bin('==', bin('mod', V('n'), num(2)), num(0)))
    ty = t.Pi('_', I, V('Bool'))
    peq('Even : Int -> Bool := fn n { n mod 2 == 0 }',
        [t.Define('Even', ty, predicate)])
    peq('Even : Int\nEven := fn n { n mod 2 == 0 }',
        [t.Declare('Even', I), t.Define('Even', ty, predicate)])
    peq('f : Int -> Int\nf := fn x { x }',
        [t.Declare('f', t.Pi('_', I, I)),
         t.Define('f', t.Pi('x', I, I), t.Lam('x', I, V('x')))])


@pytest.mark.parametrize('context', [
    'twice (f : Int -> Int) (r : Int) : Int',
    'twice : (Int -> Int) -> Int -> Int',
])
def test_lambda_argument_expected_type(context):
    eq('twice (fn k { k + 1 }) 3',
       apps(V('twice'), [t.Lam('k', I, bin('+', V('k'), num(1))), num(3)]), context)


def test_lambda_argument_dependent_expected_type():
    eq('use Int (fn x { x })', apps(V('use'), [I, t.Lam('x', I, V('x'))]),
       'use (A : U) (f : A -> A) : A')
    eq('use 1 (fn x { x })',
       apps(V('use'), [I, num(1), t.Lam('x', I, V('x'))]),
       'use {A : U} (a : A) (f : A -> A) : A')


def test_lambda_block_item_expected_type():
    eq('{ f <- fn x { x }; f }',
       t.Let('g', t.Pi('x', I, I), t.Lam('x', I, V('x')), V('g')),
       'f : Int -> Int')
    eq('{ f := fn (x : Int) { x }; f <- fn y { y }; f }',
       t.Let('a', t.Pi('x', I, I), t.Lam('x', I, V('x')),
             t.Let('b', t.Pi('y', I, I), t.Lam('y', I, V('y')), V('b'))))


def test_lambda_without_expected_type_has_a_named_unknown():
    # the core's bite 4: the parameter's type is the principal type's variable, `?x1`, never the
    # old `Hole('type')`; the annotation is erased in the hash (D-2026-10-15-e)
    for text in ['fn x { x }', 'unknown (fn x { x })']:
        e = term(text, SCOPE)
        lam = e if isinstance(e, t.Lam) else e.argument
        assert isinstance(lam.type, t.Hole) and lam.type.name.startswith('?x')


def test_lambda_expected_type_renames_dependent_binders():
    peq('f : (A : U) -> A -> A := fn B x { x }',
        [t.Define('f', t.Pi('A', U, t.Pi('_', V('A'), V('A'))),
                  t.Lam('B', U, t.Lam('x', V('B'), V('x'))))])


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


WORLD = 'print : W -> String -> W * Unit\nreadFile : W -> String -> W * Maybe String\nw0 : W'
def text(x): return t.Lit(t.StringConst(x))


def test_Blocks_action_pattern():
    # translation.lth (87d6091) law Blocks, its second gives (D-2026-10-13-ag): a pattern on an action's W * A
    eq('{ (w1, s) <- readFile w0 "f"; s }',
       t.Match(apps(V('readFile'), [V('w0'), text('f')]), ((t.PPair(pv('w1'), pv('s')), V('s')),)), WORLD)


def test_Blocks_action_unit():
    # its third gives: a bare name on W * Unit binds the token and drops the unit
    eq('{ w1 <- print w0 "x"; w1 }',
       t.Match(apps(V('print'), [V('w0'), text('x')]), ((t.PPair(pv('w1'), t.PWild()), V('w1')),)), WORLD)


def test_Blocks_action_chain_rebinds_the_token():
    # each binding of `w` is a fresh name, as for a value (4.R12); the value sees the previous one
    def arm(value, q, rest): return t.Match(value, ((q, rest),))
    def unit(n): return t.PPair(pv(n), t.PWild())
    eq('{ w <- print w0 "a"; (w, s) <- readFile w "f"; w <- print w "b"; (w, s) }',
       arm(apps(V('print'), [V('w0'), text('a')]), unit('a'),
           arm(apps(V('readFile'), [V('a'), text('f')]), t.PPair(pv('b'), pv('c')),
               arm(apps(V('print'), [V('b'), text('b')]), unit('d'), t.Pair(V('d'), V('c'))))),
       WORLD)


def test_Blocks_action_unit_through_an_imported_model():
    # the sugar on an action that is a field of a model typed by a theory applied to its arguments,
    # as `host : HostConsole` with `HostConsole = Host State` over world.lth's `Host`
    # (record/IA/v04-2026-10-15/prompt-sugar.md): the field's type is read from the theory's record,
    # so `w <- host.print w "x"` binds the token, as `print` declared alone does. `(host).print` is
    # the projection that run.py makes of the dotted name `host.print` (`projections`)
    context = ('Concrete : U\nState : Concrete\n'
               'Host (S : Concrete) : { console : S, print : W -> String -> W * Unit }\n'
               'HostConsole = Host State\nhost : HostConsole\nw0 : W')
    def unit(n): return t.PPair(pv(n), t.PWild())
    action = t.Proj(V('host'), 'print')
    eq('{ w <- (host).print w0 "a"; w <- (host).print w "b"; w }',
       t.Match(apps(action, [V('w0'), text('a')]), ((unit('a'),
           t.Match(apps(action, [V('a'), text('b')]), ((unit('b'), V('b')),))),)),
       context)


def test_Blocks_pattern_on_a_value():
    # translation.lth (1665b9d) law Blocks, its fourth gives: a pattern against a value that is not
    # an action is the same one-arm match (2.S17); only a bare name on a non-action stays a Let
    eq('{ (a, b) <- n; a }', t.Match(V('n'), ((t.PPair(pv('a'), pv('b')), V('a')),)), 'n : Int * Int')


def test_Shapes():
    a, b = V('A'), V('B'); pair = t.Sigma('_', a, b)
    peq('A : U\nB : U\nh : (A * B) -> A := fn (x, y) { x }', [t.Declare('A', U), t.Declare('B', U), t.Define('h', t.Pi('_', pair, a), t.Lam('p', pair, t.Match(V('p'), ((t.PPair(pv('x'), pv('y')), V('x')),))))])
    peq('both2 (b c : Bool) : Bool\n  | true, d := d\n  | _, _ := false', [t.Define('both2', t.Pi('b', V('Bool'), t.Pi('c', V('Bool'), V('Bool'))), t.Lam('b', V('Bool'), t.Lam('c', V('Bool'), t.Match(t.Pair(V('b'), V('c')), ((t.PPair(con('true'), pv('d')), V('d')), (t.PPair(t.PWild(), t.PWild()), V('false')))))))])
    peq('nt (b : Bool) : Bool\n  | true := false\n  | false := true', [t.Define('nt', t.Pi('b', V('Bool'), V('Bool')), t.Lam('b', V('Bool'), t.Match(V('b'), ((con('true'), V('false')), (con('false'), V('true'))))))])


ROOT = Path(__file__).parents[1]
def cli(*args):
    env = os.environ.copy(); env['PYTHONPATH'] = str(ROOT / 'src')
    return subprocess.run([sys.executable, '-m', 'luthier.cli', 'eval', *map(str, args)], capture_output=True, text=True, env=env)


@pytest.mark.parametrize('file,output', [('arithmetic', '19 : Int'), ('factorial', '24 : Int'), ('data', '2 : Int'), ('record', '7 : Int'), ('block', '3 : Int'), ('lambda', '5 : Int'), ('chained_projection', '7 : Int'), ('labeled_sum', '101 : Int')])
def test_eval(file, output):
    # 12.S19: the value with its type, then the states of the term's cone
    r = cli(ROOT / 'tests/eval' / (file + '.lut'), 'answer')
    assert r.returncode == 0, r.stdout + r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == output
    assert lines[1].startswith('states of the cone')


@pytest.mark.parametrize('term,message', [('missing', 'missing is neither defined there, nor imported'), ('answer', 'fuel spent')])
def test_eval_errors(term, message):
    r = cli(ROOT / 'tests/eval/arithmetic.lut', term, '--fuel', '0' if term == 'answer' else '100')
    assert r.returncode == 1
    assert message in r.stderr


def test_eval_parse_error(tmp_path):
    path = tmp_path / 'bad.lut'; path.write_text('answer := (')
    r = cli(path, 'answer')
    assert r.returncode == 1
    assert str(path) in r.stderr


def test_eval_loads_imports():
    # 12.S19 in the context of the files as run loads them (12.S22): a name the file imports from
    # plan_model.lut evaluates to its value, not its weak head form
    r = cli(ROOT / 'tests/eval/plan_agree.lut', 'agree')
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.splitlines()[0] == 'true : Bool'
    r = cli(ROOT / 'tests/eval/plan_agree.lut', 'needPlan.schedule')
    assert r.stdout.splitlines()[0] == 'cons "a" (cons "b" (cons "c" (cons "d" nil))) : List String'


def test_eval_prints_the_states_and_demands_no_certificate():
    # 12.S19: no certificate demanded; the laws of the cone no store serves are listed, not refused.
    # plan_model.cert.json holds entries since tests/tester/plan_laws.test.lut was certified
    # (record/IA/v04-2026-10-15/report-e.md), so this test's copy of it is emptied (conftest.py)
    (Path(os.environ['LUTHIER_LIBRARY_STORES']) / 'plan_model.cert.json').unlink(missing_ok=True)
    r = cli(ROOT / 'tests/eval/plan_agree.lut', 'allHold')
    assert r.returncode == 0, r.stdout + r.stderr
    lines = r.stdout.splitlines()
    assert lines[0] == 'true : Bool'
    assert '1 uncertified' in lines[1]
    assert '  example: Acyclic: uncertified (no entry)' in lines


def test_eval_a_term_over_several_files():
    r = cli(ROOT / 'tests/eval/arithmetic.lut', ROOT / 'tests/eval/factorial.lut', 'answer + factorial (succ (succ zero))')
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.splitlines()[0] == '21 : Int'


def test_eval_records_nothing(tmp_path):
    # 12.S19, D-2026-10-12-ah: the probe writes no run record, no lock and no store
    (tmp_path / 'f.lut').write_text('answer : Int := 6 * 7\n')
    r = cli(tmp_path / 'f.lut', 'answer')
    assert r.stdout.splitlines()[0] == '42 : Int'
    assert sorted(p.name for p in tmp_path.iterdir()) == ['f.lut']


def test_fresh_names_avoid_capture():
    eq('{ y <- 1; y <- y + 1; y + y0 }',
       t.Let('a', I, num(1), t.Let('b', I, bin('+', V('a'), num(1)), bin('+', V('b'), V('y0')))),
       'y0 : Int')


def test_extern_remains_stuck():
    eq('extern "host.route" 3', t.App(t.Extern('host.route'), num(3)))


@pytest.mark.parametrize('binders,args', [('', ''), ('(A : U)', ' A')])
def test_theory_conjunction_keeps_declared_record(binders, args):
    from luthier.check import violatesR6
    source = (f'T {binders} : {{ value : Int }}\n'
              f'L1 {binders} (m : T{args}) (x : Int) : Bool := x == m.value\n'
              f'L2 {binders} (m : T{args}) : Bool := m.value == 0\n'
              f'T {binders} := L1{args} & L2{args} & L1{args}')
    p = program(source)
    result = elaborate_program(p)
    assert alpha_equal(result[0].type, result[-1].type)
    assert not violatesR6(p, 'T')
    from luthier.elaborate import context_of, infer
    assert not isinstance(infer(result[-1].body, context_of(p)), t.Hole)


def test_single_theory_law_keeps_declared_record():
    from luthier.check import violatesR6
    p = program('Codec : { parse : String -> Maybe Int, render : Int -> String }\n'
                'RoundTrip (c : Codec) (n : Int) : Bool := true\n'
                'Codec := RoundTrip')
    result = elaborate_program(p)
    assert alpha_equal(result[0].type, result[-1].type)
    assert not violatesR6(p, 'Codec')


def test_recursive_constructor_arrow_and_recursor_argument():
    from luthier.elaborate import context_of, infer
    p = program('N : U := data { zero : N; succ : N -> N }\n'
                'recN (P : U) (z : P) (s : N -> P -> P) (n : N) : P\n'
                'add (m n : N) : N := recN N m (fn k r { succ r }) n')
    c = context_of(p)
    assert c.types['succ'] == t.Pi('_', V('N'), V('N'))
    body = elaborate_program(p)[-1].body.body.body
    step = body.function.argument
    assert alpha_equal(step, t.Lam('k', V('N'), t.Lam('r', V('N'), t.App(V('succ'), V('r')))))
    assert alpha_equal(infer(step, c), t.Pi('k', V('N'), t.Pi('r', V('N'), V('N'))))


def test_conjunction_combines_model_subtypes():
    from luthier.elaborate import Context, infer
    a = t.Subtype('x', V('T'), t.App(V('L1'), V('x')))
    b = t.Subtype('y', V('T'), t.App(V('L2'), V('y')))
    c = Context(types={'a': a, 'b': b})
    expected = t.Subtype('x', V('T'), bin('&', t.App(V('L1'), V('x')), t.App(V('L2'), V('x'))))
    assert alpha_equal(infer(bin('&', V('a'), V('b')), c), expected)


def test_conjunction_with_a_law_part_is_a_law_over_the_model():
    # algebra.lth `CompleteOrderedField`: `SupIsLeast` gives a `Law` (laws.lth); by spec 5.S6 the
    # combination lifts the Boolean part, so the conjunction is a `Law` over the theory's record
    from luthier.elaborate import context_of, infer
    record = t.Record((('value', V('Int')),))
    for second, value in (('Law', 'Law'), ('Bool', 'Bool')):
        p = program('Law : U := data { Case : Bool -> Law }\n'
                    'T (F : U) : { value : Int }\n'
                    'L1 (F : U) (m : T F) (x : Int) : Bool := x == m.value\n'
                    f'L2 (F : U) (m : T F) (s : F -> Bool) : {second} := '
                    + ('Case (m.value == 0)\n' if second == 'Law' else 'm.value == 0\n')
                    + 'T (F : U) := L1 F & L2 F')
        body = elaborate_program(p)[-1].body
        assert alpha_equal(infer(body, context_of(p)),
                           t.Pi('F', t.Universe(), t.Pi('m', record, V(value))))


CORE = Path(__file__).resolve().parents[1] / 'src' / 'luthier' / 'lib' / 'core' / 'core.lut'


def test_a_primitive_refining_a_type_is_a_type_and_its_arrow_is_the_arrow():
    # 11.R1: `Float64 : Real := primitive ...` is a type, so `Float64 -> Float64` is the arrow,
    # and core.lut's four operators on `Float64` get their declared function type (4.R13)
    from luthier.elaborate import context_of
    c = context_of(program(CORE.read_text()))
    f = V('Float64')
    # (the core's bite 4: a binding the core makes elaborates to the kernel's symbol, which is what a
    # run reduces, and a value whose type names no model is refused, never the bare symbol)
    for name, op in (('floatPlus', '+'), ('floatMinus', '-'), ('floatTimes', '*'), ('floatDivide', '/')):
        assert c.types[name] == t.Pi('_', f, t.Pi('_', f, f))
        assert c.operators[(op, f)] == V(op)
        assert any(b.name == name and b.domain == f for b in c.bindings[op])
    assert c.operators[('+', V('Int'))] == V('+')
    eq('x + y', apps(V('+'), [V('x'), V('y')]), CORE.read_text() + '\nx : Float64\ny : Float64')
    # a value declared at a type is not a type, and `Real`, the ideal, has no `+`
    with pytest.raises(TypingError, match='Real names no model of'):
        term('r + s', 'Real : U := primitive "real"\nr : Real\ns : Real')


def test_an_implication_in_type_position_is_the_arrow():
    # `Fin` and `P` unknown (imported names are not loaded): in an annotation, a binder's type or
    # a field's, `A -> B` is the arrow (check.py's `arrows`, now read at the source)
    p = program('f (p : (n : Int) -> Fin n -> Bool) : P -> Bool\n'
                'g : { h : P -> Bool }\n'
                'b (c q : Bool) : Bool := c -> q')
    f, g, b = elaborate_program(p)
    assert alpha_equal(f.type, t.Pi('p', t.Pi('n', V('Int'), t.Pi('_', t.App(V('Fin'), V('n')), V('Bool'))),
                                    t.Pi('_', V('P'), V('Bool'))))
    assert g.type == t.Record((('h', t.Pi('_', V('P'), V('Bool'))),))
    # in a term, `->` on Booleans stays the implication
    assert b.body.body.body == apps(V('implies'), [V('c'), V('q')])


def test_as_type_reads_implies_as_the_arrow():
    # moved from test_check.py (`arrows`)
    from luthier.elaborate import as_type
    implies = t.App(t.App(t.Var('implies'), t.Var('P')), t.Var('Bool'))
    assert as_type(implies) == t.Pi('_', t.Var('P'), t.Var('Bool'))
    law = t.Subtype('x', t.Var('Int'), implies)
    assert as_type(law) == law


def test_chained_projection_on_a_parenthesised_expression_is_two_projections():
    ctx = 'f (k : Int) : { x : { n : Int } } := { x := { n := k } }'
    for text in ['({ x := { n := 3 } }).x.n', '(f 3).x.n']:
        e = term(text, ctx)
        assert isinstance(e, t.Proj) and e.label == 'n'
        assert isinstance(e.record, t.Proj) and e.record.label == 'x'


def test_applied_label_is_an_application_not_an_injection():
    # bite 13: the elaborator has no types, so an applied label of a `||` sum is `App (Var l) v`
    # and the alias is inlined into the types that use it; the kernel learns the labels from there
    p = elaborate_program(program('Cell = { int : Int || real : Float64 }\nc : Cell := int 1'))
    assert len(p) == 1 and isinstance(p[0], t.Define)
    assert isinstance(p[0].type, t.Sum)
    assert p[0].body == t.App(V('int'), t.Lit(t.IntConst(1)))


# ---------------------------------------------------------------------- the core's bite 4

def test_operator_resolved_under_instantiation_and_through_a_subtype():
    # 4.R13: `+` at `Nat` and at `Fin n` is `Int`'s (a subtype's base); a binding at `Box A`
    # matches `Box Int`, its type parameter applied. Lists concatenate with <> (bite 7).
    eq('i + 1', bin('+', V('i'), num(1)), 'n : Int\ni : Fin n')
    eq('xs + ys', apps(V('addBox'), [I, V('xs'), V('ys')]),
       'Box (A : U) : U\naddBox (A : U) (xs ys : Box A) : Box A\noperator + := addBox\nxs : Box Int\nys : Box Int')


def test_operator_refusals_name_the_type_and_the_candidates():
    with pytest.raises(TypingError, match='takes Int, but "a" has type String'):
        term('x + "a"', 'x : Int')
    with pytest.raises(TypingError, match='the type of the left operand is not known'):
        term('fn x { x + 1 }', '')


def test_a_claim_binds_a_model_and_a_field_resolves_by_type():
    ctx = ('Sized (C : U) : { size : C -> Int }\nlen (A : U) (xs : List A) : Int\n'
           'ListIsSized (A : U) : Bool := Sized (List A) { size := fn xs { len A xs } }\nxs : List String')
    e = term('Sized.size xs', ctx)
    assert isinstance(e, t.App) and isinstance(e.function, t.Proj) and e.function.label == 'size'
    # the model is the claim's, at `A := String`
    assert alpha_equal(e.function.record, t.RecordValue((('size', t.Lam('xs', t.App(V('List'), V('String')),
                                                                      apps(V('len'), [V('String'), V('xs')]))),)))
    # qualified, and with its model written: the same projection
    assert alpha_equal(term('Sized.size xs', ctx), e)
    m = term('Sized.size m xs', ctx + '\nm : Sized (List String)')
    assert m == t.App(t.Proj(V('m'), 'size'), V('xs'))
    with pytest.raises(TypingError, match='no model of Indexed or Sized at Int'):
        term('size 3', ctx)


def test_an_omitted_structure_parameter_is_filled_from_the_type():
    # rule 2.2.2 (D-2026-10-18-g): `(o : Object A)` omitted is the model `A` names; passed by name it
    # is the author's
    ctx = ('Object (A : U) : { eq : A -> A -> Bool }\nIntIsAnObject : Bool := Object Int { eq := fn a b { a == b } }\n'
           'member (A : U) (o : Object A) (x : A) (xs : List A) : Bool\nparity : Object Int\nxs : List Int')
    filled = term('member Int 3 xs', ctx)
    _, args = filled, []
    while isinstance(_, t.App): args.append(_.argument); _ = _.function
    assert isinstance(args[2], t.RecordValue)
    assert term('member Int parity 3 xs', ctx) == apps(V('member'), [I, V('parity'), num(3), V('xs')])
    assert term('member Int 3 xs (o <- parity)', ctx) == apps(V('member'), [I, V('parity'), num(3), V('xs')])


def test_a_bare_conjunction_of_laws_is_a_verdict():
    # D-2026-10-18-f: each conjunct a law over its own variables; bite 4b's tester splits it
    p = program(open(Path(__file__).parent / 'spec' / 'k_bare_conjunction.accept.lut').read())
    from luthier.elaborate import context_of, infer
    c = context_of(p)
    for d in elaborate_program(p, c):
        if isinstance(d, t.Define) and d.name == 'IsEquivalence':
            assert law_value_of(infer(d.body, c)) == V('Bool')


def law_value_of(ty):
    while isinstance(ty, t.Pi): ty = ty.codomain
    return ty


def library_files():
    root = Path(__file__).resolve().parents[1]
    for d in ('src/luthier/lib', 'examples', 'tests/tester'):
        yield from sorted([*(root / d).rglob('*.lth'), *(root / d).rglob('*.lut')])


def test_infer_is_total_on_the_library():
    # execution.md §6, bite 4 (a): every definition of every file of the library, the examples and
    # the test programs elaborates in its file's context (its imports and core's) and `infer` gives
    # its body a type with no `Hole('type')`, the old "not inferred"
    from luthier.check import load_imports, hidden_constructors
    from luthier.elaborate import context_of, elaborate_act, infer, has_hole
    from luthier import surface as s
    defects = []
    for path in library_files():
        r = parse(path.read_text(encoding='utf-8'))
        assert isinstance(r, Parsed), path
        own = tuple(a for a in r.program if not isinstance(a, s.ImportAct))
        imported = tuple(load_imports(r.program, path))
        names = {a.name for a in own if hasattr(a, 'name')}
        c = context_of(tuple(a for a in imported if getattr(a, 'name', None) not in names) + own)
        c.constructors -= set(hidden_constructors(r.program, imported))
        for act in own:
            if not isinstance(act, s.Define) or isinstance(act.body, s.DataBody):
                continue
            try:
                if act in c.errors:
                    raise c.errors[act]
                ty = infer(elaborate_act(act, c).body, c)
                if has_hole(ty):
                    defects.append(f'{path.name} {act.name}: {ty}')
            except ElaborationError as e:
                defects.append(f'{path.name} {act.name}: {e}')
    assert not defects, '\n'.join(defects[:20])


def test_a_subtypes_own_model_resolves_before_its_base_model():
    # Both Int and Nat claim Object and Order; Nat is also a refinement of Int.
    assert term('eq n n', 'n : Nat')
    assert term('leq n n', 'n : Nat')


# Core bite 12a, item 1: the three elaborations bite 4 kept for the hash (report-bite-4.md,
# findings 1 and 2, and the product's nesting; spec 2.S8, 4.R7, 3.S4).
SUBTYPE_OF_U = 'Concrete : U := { A : U | true }\nT : Concrete\nA : U\nB : U\nC : U'


def test_a_type_typed_by_a_subtype_of_U_makes_a_product():
    # 2.S8: `T * Float64` with `T : Concrete` is the product, as with `T : U`
    eq('T * Float64', t.Sigma('_', V('T'), V('Float64')), SUBTYPE_OF_U)
    eq('T + B', t.Sum((('left', V('T')), ('right', V('B')))), SUBTYPE_OF_U)
    eq('T -> B', t.Pi('_', V('T'), V('B')), SUBTYPE_OF_U)


def test_products_nest_to_the_right():
    # 3.S4: `A * B * C` is `A * (B * C)`, as `(a, b, c)` is `(a, (b, c))`
    right = t.Sigma('_', V('A'), t.Sigma('_', V('B'), V('C')))
    eq('A * B * C', right, SUBTYPE_OF_U)
    eq('A * (B * C)', right, SUBTYPE_OF_U)
    eq('T * A * B * C', t.Sigma('_', V('T'), right), SUBTYPE_OF_U)
    # a component that is itself a product written in parentheses stays one component
    eq('A * (B * C) * T', t.Sigma('_', V('A'), t.Sigma('_', t.Sigma('_', V('B'), V('C')), V('T'))),
       SUBTYPE_OF_U)
    # multiplication of numbers keeps its left association
    eq('i * j * i', bin('*', bin('*', V('i'), V('j')), V('i')), 'i : Int\nj : Int')


def test_an_alias_parameter_is_not_captured_by_a_record_field():
    # 4.R7: inside `F`, whose parameter is `n`, `V Int`'s field `f : Fin n -> A` reads the field `n`
    p = elaborate_program(program('V (A : U) = { n : Nat, f : Fin n -> A }\n'
                                  'F (n : Int) = { p : V Int }\nx : F 3'))
    inner = dict(dict(p[-1].type.fields)['p'].fields)
    assert alpha_equal(inner['f'], t.Pi('_', t.App(V('Fin'), V('n')), V('Int')))
    # a binder of a function type or of a dependent product is bound the same way
    p = elaborate_program(program('G (n : Int) = (n : Nat) -> Fin n\nx : G 3'))
    assert alpha_equal(p[-1].type, t.Pi('n', V('Nat'), t.App(V('Fin'), V('n'))))


# Core bite 12a, item 2: through a subtype to its base, never to a sibling subtype's claim (4.R13;
# docs/concepts.md 4.3, `d microphone speaker` landing on core.lut's IntIsAMetric).
SIBLINGS = ('Wide : U := { k : Int | k <= 100 }\nNarrow : U := { k : Int | k <= 10 }\n'
            'Inner : U := { k : Wide | 0 <= k }\n'
            'WideIsAMetric (model : Metric Wide (structural Wide) <- { d := fn x y { 0.0 } }) : Bool := '
            'Metric Wide (structural Wide) model\n'
            'a : Narrow\nb : Inner\nw : Wide\n')


def test_a_claim_at_a_subtype_serves_it_and_the_subtypes_declared_inside_it():
    for x in ('w', 'b'):
        r = term(f'd {x} {x}', SIBLINGS)
        assert isinstance(r.function.function, t.Proj) and r.function.function.label == 'd'


def test_a_claim_at_a_subtype_does_not_serve_a_sibling_subtype():
    # `Narrow`'s only candidate is core.lut's IntIsAMetric, claimed at MetricInteger, another
    # subtype of Int: refused, the candidate named
    with pytest.raises(TypingError) as e:
        term('d a a', 'Narrow : U := { k : Int | 0 <= k and k <= 10 }\na : Narrow')
    assert 'no model' in str(e.value) and 'at Narrow' in str(e.value) and 'IntIsAMetric' in str(e.value)
    with pytest.raises(TypingError) as e:
        term('d a a', SIBLINGS)
    assert 'no model' in str(e.value)


BOX = ('Box (A : U) = { item : A }\n'
       'boxFold (A M : U) (combine : M -> M -> M) (neutral : M) (f : A -> M) (b : Box A) : M := combine (f b.item) neutral\n'
       'BoxIsFoldable (model : Foldable Box <- { fold := boxFold }) : Bool := Foldable Box model\n'
       'b : Box Int\n')


def test_a_container_given_to_a_core_function_is_not_taken_as_its_model():
    # report-bite-12b.md finding 3: `toList Vec Float64 v` took `v`, a record, as the Foldable model
    # and left a function of the container; a record without the structure's fields is no model
    r = term('toList Box Int b', BOX)
    assert not isinstance(r, t.Lam)
    from luthier.elaborate import show
    assert "boxFold" in show(r) and show(r).endswith(") b)"), show(r)

