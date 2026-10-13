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


def test_R3_claimed_laws_read_fields_through_bound_models():
    for body in ['m.parse == m.parse', '(m).parse == (m).parse']:
        p = program('T : { parse : Int }\nT := law\nlaw (m : T) : Bool := ' + body)
        assert c.law_reads(p) == {'parse'}
        assert not c.violatesR3(p, 'T')
    p = program('T : { parse : Int, print : Int }\nT := law\nlaw (m : T) : Bool := m.parse == m.parse')
    assert c.violatesR3(p, 'T')
    # the field after the first `.`: `m.a.b` reads the field `a` of `m` (program.lth 5f33db8, group 1)
    assert c.fields_read(program('f := m.a.b')[0].body.term) == {'a'}
    assert c.law_reads(program('T : { parse : Int }\nT := true\nlaw (m : T) : Bool := m.parse == m.parse')) == set()


@pytest.mark.parametrize('source', [
    'T = { field : { a : Int || b : String } }',
    'T := { field : { a : Int || b : String } }',
    'T : { field : { a : Int || b : String } } := extern "T"',
    'T : { field : { a : Int || b : String } }',
    'T (x : { a : Int || b : String }) : Int',
])
def test_nested_sum_labels_in_types_are_constructors(source):
    p = program(source + '\nf := a 1')
    assert c.constructors(p) == {'a', 'b'}
    assert not c.violatesR2(p, 'f')


def test_R9_named_subtype_bases_and_cycles():
    from luthier import term as t
    p = program('Positive : U := { x : Int | x == x }\nf (x : Int) : Int := x\ng (x : Positive) := f x')
    assert not c.violatesR9(p, 'g')
    p = program('Positive : U := { x : Int | x == x }\nf (x : Positive) : Int := 1\ng (x : Int) := f x')
    assert not c.violatesR9(p, 'g')
    assert c.violatesR9(program('Positive : U := { x : String | x == x }\nf (x : Int) := x\ng (x : Positive) := f x'), 'g')
    q = c.Typing(program('A : U := { x : B | true }\nB : U := { x : A | true }'))
    assert c.base(q, t.Var('A')) in {t.Var('A'), t.Var('B')}
    q = c.Typing(program('A = Int'))
    assert c.base(q, t.Var('A')) == t.Var('A')


def test_R9_theory_head_passes_where_the_theory_is_expected():
    # library.lth, reading 6: a helper taking the whole loader `(l : Loader)` was refused, since
    # elaborate.theory_domains reads the domain `Loader` as its record and the argument stayed `Loader`
    theory = ('T : { op : Int -> Int }\nT := law\nlaw (m : T) : Bool := m.op 1 == 1\n'
              'S : { other : String }\nS := lawS\nlawS (m : S) : Bool := m.other == m.other\n'
              'helper (m : T) (n : Int) : Bool := m.op n == n and helper m n\n')
    p = program(theory + 'user (m : T) : Bool := helper m 1')
    assert not c.violatesR9(p, 'helper')
    assert not c.violatesR9(p, 'user')
    assert c.violatesR9(program(theory + 'user (m : S) : Bool := helper m 1'), 'user')
    assert c.violatesR9(program(theory + 'user (m : Int) : Bool := helper m 1'), 'user')
    p = program('P (k : Int) : { op : Int }\nP (k : Int) := lawP k\nlawP (k : Int) (m : P k) : Bool := m.op == k\n'
                'h (k : Int) (m : P k) : Bool := m.op == k\nuser (m : P 1) : Bool := h 1 m')
    assert not c.violatesR9(p, 'user')


def test_R9_arrow_over_an_imported_name_is_an_arrow():
    # library.lth, reading 6: `f2 okAll` was refused and `f2 l.admitsAt` passed, since elaborate.py
    # reads `P -> Bool` as `implies P Bool` when `P` is imported (imports are not loaded)
    head = 'import "x.lth" P\nf2 (g : String -> P -> Bool) : Bool := true\n'
    p = program(head + 'okAll (s : String) (x : P) : Bool := true\nuse : Bool := f2 okAll')
    assert not c.violatesR9(p, 'use')
    assert c.violatesR9(program(head + 'bad (s : Int) (x : P) : Bool := true\nuse : Bool := f2 bad'), 'use')


def test_rebind_binds_its_pattern_names():
    # program.lth (87d6091): itemsNames, 4.R12 itemsFault and 2.R6 unusedRebinding read `q <- v`
    # with `q` a pattern, over every name it binds (D-2026-10-13-ag)
    ok = 'f (w : World) : World := { (w, x) <- readFile w "f" ; print w x }'
    p = program(ok)
    assert not c.violatesR12(p, 'f') and not c.violatesR2R6(p, 'f')
    assert c.dependencies(p, p[0], True) == {'readFile', 'print'}
    # itemsNames: the names the pattern binds are bound in what follows, not before
    block = program('g := { (w, x) <- h x ; x }')[0].body.term
    assert c.names(block) == {'h', 'x'}
    # 4.R12: `<-` may not rebind a name bound with `:=` in scope, here `x`
    assert c.violatesR12(program('f (w : World) : World := { x := 1 ; (w, x) <- readFile w "f" ; print w x }'), 'f')
    # 2.R6: `x` bound by the first `<-` is rebound before it is used
    assert c.violatesR2R6(program('f (w : World) : World := { (w, x) <- readFile w "f" ; (w, x) <- readFile w "g" ; print w x }'), 'f')
    assert not c.violatesR2R6(program('f (w : World) : World := { (w, x) <- readFile w "f" ; (w, y) <- readFile w x ; print w y }'), 'f')


def test_R9_core_Nat_and_Fin_are_subtypes_of_Int():
    # term_model.lut, canonicalTerm: `canonTerm ... nil 0` was refused, the literal's `Int` against
    # `Nat`; spec 11.R1 makes `Nat` and `Fin n` subtypes of `Int`, so their base is `Int` and the
    # refinement is an obligation (4.R9, program.lth's `base`), not a failure
    assert not c.violatesR9(program('f (n : Nat) : Int := 1\ng : Int := f 0'), 'g')
    assert not c.violatesR9(program('h (i : Fin 3) : Int := 1\ng : Int := h 0'), 'g')
    assert not c.violatesR9(program('f (x : Int) : Int := x\ng (m : Nat) : Int := f m'), 'g')
    assert c.violatesR9(program('f (n : Nat) : Int := 1\ng : Int := f "a"'), 'g')
    assert c.violatesR9(program('f (x : String) : Int := 1\ng (m : Nat) : Int := f m'), 'g')


def test_R9_applied_subtype_definition_is_looked_through():
    # grammar.lth, LexesWhatDerives: `tokenize d s` with `s : LexedText d g` was refused, since
    # `base` looked through a name defined as a subtype only when bare; `LexedText d g` is
    # `{ s : String | lexes d g s }`, whose base is `String`
    head = 'Pos (k : Int) : U := { s : String | s == s }\nf (x : String) : Int := 1\nh (k : Int) (y : Pos k) : Int := k\n'
    assert not c.violatesR9(program(head + 'g (k : Int) (y : Pos k) : Int := f y'), 'g')
    assert c.violatesR9(program(head + 'g (k : Int) (y : Pos k) : Int := h y k'), 'g')
    assert not c.violatesR9(program(head + 'g (k : Int) (y : String) : Int := h k y'), 'g')


# check.py bite 5 (record/IA/check-2026-10-13/prompt-5.md and its addendum)

def test_R3_chained_projection_reads_the_first_field():
    # group 1: `s.w.r` reads the field `w` of `s`, not `r`
    p = program('Inner = { r : Int }\nT : { w : Inner, k : Int }\nT := L\nL (s : T) : Bool := s.w.r == s.k')
    assert not c.violatesR3(p, 'T')
    assert c.violatesR3(program('Inner = { r : Int }\nT : { w : Inner, k : Int }\nT := L\nL (s : T) : Bool := s.k == s.k'), 'T')


def test_R3_law_binders_are_reads():
    # 1.S7, program.lth 02aa8af [proposed]: `r : Fin t.n` in a law's binder reads `n`
    head = 'T : { n : Nat, k : Int }\nT := L\n'
    assert not c.violatesR3(program(head + 'L (t : T) (r : Fin t.n) : Bool := t.k == t.k'), 'T')
    assert c.violatesR3(program(head + 'L (t : T) (r : Int) : Bool := t.k == t.k'), 'T')


def test_R3_a_claimed_laws_own_patterns_name_constructors():
    # group 2, program.lth lawNames [proposed]: a match in the law names `a` and `b`
    data = 'D : U := data { a : D ; b : D }\nT : { d : D }\nT := L\n'
    assert not c.violatesR3(program(data + 'L (t : T) : Bool := match t.d { a -> true ; b -> true }'), 'D')
    # a helper the law calls is not read (4.S15)
    helper = 'h (d : D) : Bool := match d { a -> true ; b -> true }\nL (t : T) : Bool := h t.d'
    assert c.violatesR3(program(data + helper), 'D')


@pytest.mark.parametrize('source,bad', [
    ('walk (n : Int) : Int -> Int := fn k { n }', False),  # a function, not a predicate
    ('P : Int -> Bool := fn k { true }', True),
    ('Q = Int -> Bool\nP : Q := fn k { true }', True),    # through an alias (4.R7)
    ('P : Int\nP := fn k { true }', True),                # declared at a non-function type (4.R6)
    ('P : Int -> Int\nP := fn k { 1 }', False),
    ('P := fn k { true }', True),                          # nothing written or declared
])
def test_R3_lambda_case_on_predicates_only(source, bad):
    # group 5: lambdaIsPredicate's four clauses
    name = 'walk' if source.startswith('walk') else 'P'
    assert c.violatesR3(program(source), name) == bad


def test_R3_a_projection_touches_its_variable():
    # 4.R3 with 1.S7 (program.lth 02aa8af): `v.n == k` touches `v` (arrays.lth's VecOf)
    p = program('V = { n : Nat, f : Fin n -> Float64 }\nVecOf (k : Int) : U := { v : V | v.n == k }')
    assert not c.violatesR3(p, 'VecOf')
    assert c.violatesR3(program('V = { n : Nat }\nVecOf (k : Int) : U := { v : V | k == k }'), 'VecOf')


def test_R4_primitive_makes_a_type():
    # 11.R1: `Int : U := primitive "integer"` (11.R2, which file may say so, is not read here)
    assert not c.violatesR4(program('Int : U := primitive "integer"'), 'Int')
    assert c.violatesR4(program('X : U := Int'), 'X')


def test_R13_compares_the_types_written_on_the_definitions():
    # rivalModel by the declared type with the binders' types (program.lth 02aa8af)
    two = 'intPlus (a b : Int) : Int := a\nfloatPlus (a b : Float64) : Float64 := a\noperator + := intPlus\noperator + := floatPlus'
    assert not c.violatesR13(program(two), 'intPlus')
    same = 'f (a b : Int) : Int := a\ng : Int -> Int -> Int := fn x y { x }\noperator + := f\noperator + := g'
    assert c.violatesR13(program(same), 'f') and c.violatesR13(program(same), 'g')


def test_R9_unannotated_lambda_where_an_index_function_is_expected():
    # cause (a): the hole of `fn k { ... }` is not compared with `Fin n`
    p = program('sumTo (n : Int) (f : Fin n -> Float64) : Float64 := 0.0\nzeros (n : Nat) : Float64 := sumTo n (fn k { 0.0 })')
    assert not c.violatesR9(p, 'zeros')


def test_R9_subtype_of_an_alias_with_an_arrow_passes_where_the_alias_is_expected():
    # cause (b): `Fin n -> A` inside the subtype's base is an arrow, not `implies`
    src = ('Vec (A : U) = { n : Nat, f : Fin n -> A }\nVecOf (k : Int) : U := { v : Vec Float64 | v.n == k }\n'
           'len (x : Vec Float64) : Nat := x.n\nL (k : Int) (x : VecOf k) : Bool := len x == k')
    assert not c.violatesR9(program(src), 'L')
    bad = src.replace('len (x : Vec Float64)', 'len (x : Vec Int)')
    assert c.violatesR9(program(bad), 'L')


def test_R9_substitution_stops_at_a_record_field_of_the_same_name():
    # cause (c): `identity k` keeps the field `n` of `{ m, n, f : Fin m -> Fin n -> Float64 }`
    src = ('Mat (A : U) = { m : Nat, n : Nat, f : Fin m -> Fin n -> A }\n'
           'identity (n : Nat) : Mat Float64 := { m := n, n := n, f := fn i j { 0.0 } }\n'
           'tr (a : Mat Float64) : Float64 := 0.0\nL (k : Nat) : Bool := tr (identity k) == 0.0')
    assert not c.violatesR9(program(src), 'L')


def test_R9_a_theory_head_is_a_type_at_U():
    # `Maybe T` with `T` a theory: `T` is at `U`, not its record (tables.lth's former sameParse)
    src = 'T : { n : Int }\nPos (t : T) : Bool := 0 < t.n\nT := Pos\nsame (a b : Maybe T) : Bool := true'
    assert not c.violatesR9(program(src), 'same')


def test_R9_reads_imported_subtypes(tmp_path):
    # 12.S22: `base` looks through an imported definition (the port's smallest case)
    (tmp_path / 'a.lut').write_text('R = { x : Int, y : Int }\nP (r : R) : Bool := r.x < r.y\nS : U := { r : R | P r }\n')
    b = tmp_path / 'b.lut'
    b.write_text('import "a.lut" R S\nf (r : R) : Int := r.x\ns (r : S) : Int := f r\n')
    p = program(b.read_text())
    assert any(f.rule == '4.R9' and f.name == 's' for f in c.check(p))
    assert not c.check(p, b)
    b.write_text('import "a.lut" R S\nf (r : Int) : Int := r\ns (r : S) : Int := f r\n')
    assert any(f.rule == '4.R9' and f.name == 's' for f in c.check(program(b.read_text()), b))


def test_typing_rules_run_act_by_act_when_the_file_does_not_elaborate_whole():
    # check bite 6: a record refinement (elaborate.py: "record refinements require check.py") left
    # the whole file untyped, so 4.R9 answered "no violation" on every act
    src = 'Pair : U := { x y : Int | x < y }\nf (x : Int) : Int := x\nbad := f "s"\nok := f 1\n'
    p = program(src)
    assert [(x.rule, x.name) for x in c.check(p)] == [('4.R9', 'bad')]
    line = c.report(p)[0]
    assert (line.kind, line.name) == ('typed', '3 of 4 acts')
    assert line.message == 'not typed: Pair (record refinements require check.py)'
    # a rule on an untyped act answers nothing (its verdict is not covered), as before
    assert not any(x.name == 'Pair' for x in c.check(p))


def test_acts_read_alone_but_not_together_are_kept_one_by_one():
    # each act elaborates alone, together `A` needs its argument: `x` is left out, named, with why
    p = program('A (n : Int) = Int\nx : A := 1\nf (y : Int) : Int := y\nbad := f "s"\n')
    q = c.typing_of(p)
    assert {c.label(a): m for a, m in q.untyped.items()} == {'x': 'alias A needs arguments'}
    assert any(x.rule == '4.R9' and x.name == 'bad' for x in c.check(p))


def test_an_alias_with_a_record_refinement_is_untyped():
    # read only where it is used; there it is left out and the user typed with `P` as a bare name
    p = program('P = { x y : Int | x < y }\nf (x : Int) : Int := x\n')
    assert c.report(p)[0].message == 'the whole file elaborates.'
    p = program('P = { x y : Int | x < y }\nf (p : P) : Int := p.x\ng (x : Int) : Int := x\nbad := g "s"\n')
    assert c.report(p)[0] == c.Report('typed', '3 of 4 acts', 'not typed: P (record refinements require check.py)')
    assert any(x.rule == '4.R9' and x.name == 'bad' for x in c.check(p))


def test_cli_verbose_says_how_many_acts_are_typed(tmp_path, capsys):
    path = tmp_path / 'case.lut'
    path.write_text('Pair : U := { x y : Int | x < y }\nf (x : Int) : Int := x\n')
    assert main(['check', '-v', str(path)]) == 0
    assert f'{path}:1: typed 1 of 2 acts: not typed: Pair (record refinements require check.py)' in capsys.readouterr().out
    path.write_text('x : Int := 1\n')
    assert main(['check', '-v', str(path)]) == 0
    assert f'{path}:1: typed 1 of 1 acts: the whole file elaborates.' in capsys.readouterr().out


def test_R9_a_record_value_with_fields_not_inferred_passes():
    # algebra.lth `FieldIsOrdered`: `{ ring := o.field.ring, leq := o.leq }` is `{ ring : ?, leq : ? }`
    # (a projection through a theory-typed binder is not inferred); a hole is not compared
    src = ('R : { a : Int, b : Int }\nP (r : R) : Bool := r.a < r.b\nR := P\n'
           'S : { r : R, c : Int }\nf (x : { a : Int, b : Int }) : Int := x.a\n'
           'g (s : S) : Int := f { a := s.r.a, b := s.r.b }\nh : Int := f { a := 1, b := "s" }')
    assert not c.violatesR9(program(src), 'g')
    assert c.violatesR9(program(src), 'h')


def test_R8_a_recursive_data_type_is_unfolded_once():
    # program.lth, typed act by act: `contains_arrow` recursed through a recursive data type until
    # Python's stack ran out
    src = 'T : U := data { leaf : T ; node : T -> T -> T }\nsame (a b : T) : Bool := a == b'
    assert not c.violatesR8(program(src), 'same')
    src = 'F : U := data { leaf : F ; wrap : (Int -> Int) -> F }\nsame (a b : F) : Bool := a == b'
    assert c.violatesR8(program(src), 'same')


def test_an_operator_whose_function_is_not_typed_as_a_function_is_typed_now():
    # core.lut: `Float64 : Real` with a primitive body is a type (elaborate 6, 11.R1), so
    # `Float64 -> Float64` is the arrow and the operator typed; the 4.R9 on `bad` still shows
    p = program('Real : U := primitive "real"\nFloat64 : Real := primitive "d"\nfloatNeg : Float64 -> Float64 := primitive "-"\n'
                'operator - := floatNeg\nf (x : Int) : Int := x\nbad := f "s"\n')
    assert c.report(p)[0] == c.Report('typed', '6 of 6 acts', 'the whole file elaborates.')
    assert any(x.rule == '4.R9' and x.name == 'bad' for x in c.check(p))


def test_an_operator_whose_function_has_no_declared_type_is_left_out():
    p = program('f (x : Int) : Int := x\noperator - := g\ng := f\nbad := f "s"\n')
    assert c.report(p)[0] == c.Report('typed', '3 of 4 acts', 'not typed: operator - := g (operator needs a declared function type)')
    assert any(x.rule == '4.R9' and x.name == 'bad' for x in c.check(p))


def test_Law_is_a_verdict():
    # 4.R6, 5.S6: a body typed `(F : U) -> Law` fits a declared Law
    p = program(open('src/luthier/lib/algebra.lth').read())
    assert not any(x.rule == '4.R6' for x in c.check(p))
