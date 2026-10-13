"""Hand-written domains for program.lth laws (519bdf3/a73fa4f), brief v2, no seed."""
import pytest
from luthier.parse import parse
from luthier.surface import Parsed
from luthier import check as c
from luthier.cli import main


def program(source):
    result = parse(source)
    assert isinstance(result, Parsed), result
    return result.program


CASES = [
    (1, 'x', 'x : Missing', 'x : Int'),
    (2, 'x', 'x : Int := missing', 'x : Int := 1'),
    (3, 'T', 'T : U := { x : Int | true }', 'T : U := { x : Int | x == x }'),
    (4, 'T', 'T : U := Int', 'T : U := { x : Int | x == x }'),
    (5, 'T', 'T : U := extern "T"', 'T : U := extern "T" (provisional <- true)'),
    (6, 'x', 'x : Int\nx := "bad"', 'x : Int\nx := 1'),
    (7, 'T', 'T = Int\nT : U', 'T = Int'),
    (8, 'eq', 'eq (f : Int -> Int) : Bool := f == f', 'eq (x : Int) : Bool := x == x'),
    (9, 'x', 'f (x : Int) : Int := x\nx := f "bad"', 'f (x : Int) : Int := x\nx := f 1'),
    (12, 'x', 'x := 1\nx := 2', 'x := 1'),
]


@pytest.mark.parametrize('rule,name,violating,clean', CASES)
def test_ReportsViolations(rule, name, violating, clean):
    p = program(violating)
    assert getattr(c, f'violatesR{rule}')(p, name)
    assert any(f.rule == f'4.R{rule}' and f.name == name for f in c.check(p))


@pytest.mark.parametrize('rule,name,violating,clean', CASES)
def test_ReportsNoFalseFailure(rule, name, violating, clean):
    p = program(clean)
    assert not getattr(c, f'violatesR{rule}')(p, name)
    assert not any(f.rule == f'4.R{rule}' and f.name == name for f in c.check(p))


@pytest.mark.parametrize('kind,source,name', [
    ('unclaimed', 'law : Bool := true', 'law'),
    ('provisional', 'x : Int := extern "x" (provisional <- true)', 'x'),
    ('loose', 'f (x : Int) : Int := x', 'f'),
])
def test_ReportsWhen_and_ReportsOnlyWhen(kind, source, name):
    assert any(r.kind == kind and r.name == name for r in c.report(program(source)))
    assert not any(r.kind == kind for r in c.report(program('x : Int := 1')))


def test_names_and_scopes():
    assert c.namePrefix('a.b.c') == 'a'
    assert c.nameSuffix('a.b.c') == 'c'
    assert c.namePrefix('a') == c.nameSuffix('a') == 'a'
    p = program('f (a : Int) (b : Int <- a) : Int := { x := a ; x + b }')
    assert not c.violatesR2(p, 'f')
    assert all(f.name in {'f'} for f in c.check(p))


def test_R10_R11_are_not_rejection_predicates():
    p = program('x := 1')
    assert not c.violatesR10(p, 'x')
    assert not c.violatesR11(p, 'x')


def test_block_rules():
    assert c.violatesR12(program('f := { x := 1 ; x <- 2 ; x }'), 'f')
    assert not c.violatesR12(program('f (x : Int) := { x <- 2 ; x }'), 'f')


def test_cli(tmp_path, capsys):
    path = tmp_path / 'case.lut'
    path.write_text('x : Missing\n')
    assert main(['check', str(path)]) == 1
    assert f'{path}:1: 4.R1 x:' in capsys.readouterr().out
    path.write_text('law : Bool := true\n')
    assert main(['check', '-v', str(path)]) == 0
    assert 'unclaimed law:' in capsys.readouterr().out
    path.write_text('x <- 1\n')
    assert main(['check', str(path)]) == 1
    assert ':1: syntax <parse>:' in capsys.readouterr().out


def test_Typing_laws_on_constructed_terms():
    from luthier import term as t
    q = c.Typing(program('x : Int'))
    integer = t.Var('Int'); one = t.Lit(t.IntConst(1))
    assert q.typeOf(t.Var('x')) == integer
    assert q.typeOf(one) == integer
    assert q.typeOf(t.Universe()) == t.Universe()
    assert q.typeOf(t.World()) == t.Universe()
    identity = t.Lam('x', integer, t.Var('x'))
    assert q.same(q.typeOf(identity), t.Pi('x', integer, integer))
    assert q.typeOf(t.App(identity, one)) == integer
    assert q.typeOf(t.App(one, one)) is None
    assert q.typeOf(t.Pair(one, one)) == t.Sigma('_', integer, integer)
    assert q.typeOf(t.RecordValue((('a', one),))) == t.Record((('a', integer),))
    assert q.typeOf(t.Proj(t.RecordValue((('a', one),)), 'a')) == integer
    assert q.typeOf(t.Match(one, ((t.PWild(), one),))) == integer
    assert q.typeOf(t.Let('y', integer, one, t.Var('y'))) == integer
    for ty in [t.Pi('x', integer, integer), t.Sigma('x', integer, integer),
               t.Sum((('a', integer),)), t.Record((('a', integer),)),
               t.Subtype('x', integer, t.Var('true')), t.Data('N', (('z', t.Var('N')),))]:
        assert q.typeOf(ty) == t.Universe()
    small = t.Subtype('x', integer, t.Var('true'))
    assert q.refines(small, small) and q.refines(small, integer)
    assert not q.refines(integer, small)
    assert not q.same(integer, t.Var('String'))
    assert not q.same(integer, t.Universe())
    assert not q.same(integer, t.Pi('_', integer, integer))
    assert not q.refines(t.Var('String'), integer)
    assert q.refines(t.Pi('x', integer, small), t.Pi('x', small, integer))
    for condition in [t.App(t.Var('p'), t.Var('x')),
                      t.App(t.App(t.Var('<'), one), t.Var('x'))]:
        assert q.branchContext({'x': integer}, condition, True)['x'] == t.Subtype('x', integer, condition)
        assert q.branchContext({'x': integer}, condition, False)['x'] == t.Subtype('x', integer, t.App(t.Var('not'), condition))


@pytest.mark.parametrize('predicate,rule,name,bad,clean', [
    ('violatesR2R1', '2.R1', 'x',
     'f (a : Int) : Int := a\nx := f (b <- 1)',
     'f (a : Int) : Int := a\nx := f (a <- 1)'),
    ('violatesR2R6', '2.R6', 'f',
     'f (a : Int) := { y <- a ; y <- a + 1 ; y }',
     'f (a : Int) := { y <- a ; y <- y + 1 ; y }'),
    ('violatesR13', '4.R13', 'f',
     'f : Int -> Int\ng : Int -> Int\noperator + := f\noperator + := g',
     'f : Int -> Int\ng : String -> String\noperator + := f\noperator + := g'),
    ('violates6R1', '6.R1', 'x',
     'Reference : U\nx := 1\ncite x 42',
     'Reference : U\nr : Reference\nx := 1\ncite x r'),
])
def test_new_ReportsViolations(predicate, rule, name, bad, clean):
    # The new laws require reporting violations; clean domains also exercise
    # the direction of each predicate without adding a theory biconditional.
    pred = getattr(c, predicate)
    assert pred(program(bad), name)
    assert any(f.rule == rule and f.name == name for f in c.check(program(bad)))
    assert not pred(program(clean), name)
    assert not any(f.rule == rule and f.name == name for f in c.check(program(clean)))


def test_operator_rivals_report_each_function_and_absent_declarations():
    p = program('f := 1\ng := 2\noperator + := f\noperator + := g')
    # declaredSurface returns nothing for both, equal in the literal predicate.
    assert {f.name for f in c.check(p) if f.rule == '4.R13'} == {'f', 'g'}
    assert not c.violatesR13(program('f : Int\noperator + := f\noperator + := f'), 'f')


def test_rebinding_parameters_lambdas_and_bind_reads():
    assert c.violatesR2R6(program('f (a : Int) := { a <- 2 ; a }'), 'f')
    assert not c.violatesR2R6(program('f (a : Int) := { a <- a + 1 ; a }'), 'f')
    assert c.violatesR2R6(program('f := fn a { a <- 2 ; a }'), 'f')
    assert not c.violatesR2R6(program('f (a : Int) := { x := a ; a <- 2 ; a }'), 'f')


def test_bound_dotted_names_in_scopes():
    assert c.remove_bound({'p', 'p.x', 'p.x.y', 'other.x'}, {'p'}) == {'other.x'}
    for source in [
        'f (p : Int) := p.x', 'f := fn p { p.x }',
        'f := { p := 1 ; p.x }', 'f := match 1 { p -> p.x }',
        'f : (p : Int) -> p.x',
    ]:
        p = program(source)
        a = p[0]
        assert not c.unknown(p, c.dependencies(p, a))
        if hasattr(a, 'body'): assert not c.unknown(p, c.dependencies(p, a, True))


def test_sum_labels_of_aliases_and_definitions_are_constructors():
    for source in ['T = { a : Int || b : String }', 'T := { a : Int || b : String }']:
        p = program(source + '\nf := a 1')
        assert c.constructors(p) == {'a', 'b'}
        assert not c.violatesR2(p, 'f')


def test_theory_heads_find_prior_and_later_declarations():
    for source in ['T : Int\nT := law\nlaw : Bool := helper\nhelper := true',
                   'T := law\nT : Int\nlaw : Bool := helper\nhelper := true']:
        assert 'helper' in c.law_names(program(source))


def test_extern_reads_every_type_name_and_accepts_aliases():
    assert c.violatesR5(program('T : U\nf : Int -> T := extern "f"'), 'f')
    assert c.violatesR5(program('T : U\nf : List T := extern "f"'), 'f')
    assert not c.violatesR5(program('T = Int\nf : T -> Int := extern "f"'), 'f')
    assert not c.violatesR5(program('T : U\nf : Int -> T := extern "f" (provisional <- true)'), 'f')


def test_SameSeparates_record_names_and_order():
    from luthier import term as t
    q = c.Typing(program('x : Int'))
    a = t.Record((('a', t.Var('Int')), ('b', t.Var('String'))))
    assert q.same(a, a)
    assert not q.same(a, t.Record(tuple(reversed(a.fields))))
    assert not q.same(t.Record((('a', t.Var('Int')),)), t.Record((('c', t.Var('Int')),)))


def test_citation_only_checks_datums_for_the_cited_name():
    p = program('Reference : U\nx := 1\ny := 2\ncite x 42')
    assert c.violates6R1(p, 'x')
    assert not c.violates6R1(p, 'y')
    assert not c.violates6R1(program('x := 1\ncite x'), 'x')
    assert not c.violates6R1(program('x := 1\nf := cite x 42'), 'x')


def test_R9_inline_record_return_preserves_field_names_and_order():
    assert c.violatesR9(program('f (p : { a : Int, b : Bool }) : { b : Bool, a : Int } := p'), 'f')
    assert c.violatesR9(program('f (p : { a : Int }) : { c : Int } := p'), 'f')
    assert not c.violatesR9(program('f (p : { a : Int, b : Bool }) : { a : Int, b : Bool } := p'), 'f')
