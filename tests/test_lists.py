"""Bite 7: grammar fixity, model resolution, list laws and their wrong models."""
from pathlib import Path

import pytest

from luthier import surface as s, term as t, tester
from luthier.check import check
from luthier.ebnf import count_derivations, luthier_syntax
from luthier.elaborate import TypingError, elaborate_term, elaborate_act, context_of, parameters, infer
from luthier.kernel import alpha_equal
from luthier.parse import parse, print_program, layout, lex
from luthier.run import evaluate

ROOT = Path(__file__).parent


def expression(source):
    result = parse('answer := ' + source)
    assert isinstance(result, s.Parsed), result
    return result.program[-1].body.term


@pytest.mark.parametrize('source', [
    'a <> b <> c', '(a <> b) <> c', '(a + b) <> c', 'a <> (b - c)',
    '(a <> b) + c', 'a + (b <> c)', 'a <> b * c',
    'match a <> b <> c { nil -> 0 ; cons x rest -> x }',
    '{ x := a\n  <> b\n  x }',
])
def test_semigroup_fixity_roundtrip_and_unique_grammar_tree(source):
    result = parse('answer := ' + source)
    assert isinstance(result, s.Parsed), result
    printed = print_program(result.program)
    assert parse(printed) == result
    assert count_derivations(luthier_syntax(), list(layout(lex(printed).tokens))) == 1


def test_semigroup_associates_right_at_the_additive_level():
    a, b, c = map(s.Name, 'abc')
    assert expression('a <> b <> c') == s.Binop('<>', a, s.Binop('<>', b, c))
    for source in ['a + b <> c', 'a <> b + c', 'a - b <> c', 'a <> b - c',
                   'match a <> b + c { nil -> 0 }']:
        assert isinstance(parse('answer := ' + source), s.ParseFailed)


@pytest.mark.parametrize('carrier', ['String', 'List Int'])
def test_plus_refuses_concatenation_and_names_the_semigroup_operation(carrier):
    source = f'bad (x y : {carrier}) : {carrier} := x + y'
    failures = check(parse(source).program)
    assert any(f.rule == '4.R13' and '<>' in f.message for f in failures)


def test_semigroup_uses_a_generic_models_combine_and_checks_both_operands():
    context = parse('generic (A : Concrete) (m : Semigroup A (structural A)) (x y : A) : A := x <> y').program
    c = context_of(context).child()
    parameters(context[0].binders, c)
    value = elaborate_term(expression('x <> y'), c)
    expected = t.App(t.App(t.Proj(t.Var('m'), 'combine'), t.Var('x')), t.Var('y'))
    assert alpha_equal(value, expected)
    with pytest.raises(TypingError):
        elaborate_term(expression('true <> false'), ())
    assert check(parse('bad : String := "a" <> 1').program)


def test_list_library_without_imports_executes_every_public_operation():
    path = ROOT / 'spec/lists_unimported.accept.lut'
    assert not check(parse(path.read_text()).program, path)
    result, _, _ = evaluate([path], 'allFunctions')
    assert result == t.Var('true')


@pytest.mark.parametrize('program, verdict', [('lists_laws', 'Supported'), ('lists_controls', 'Refuted')])
def test_list_claims_grade_and_their_controls_refute(program, verdict):
    outcomes = tester.run_tests(ROOT / 'tester' / (program + '.test.lut'))
    assert len({o.spec.law for o in outcomes}) == 20
    assert all(o.verdict == verdict for o in outcomes), [
        (o.spec.law, o.verdict, o.raised[:1], o.conjunct) for o in outcomes if o.verdict != verdict]


def test_tabulated_claim_binds_its_model_before_the_laws_indexed_witness():
    c = context_of(())
    claims = c.claims['Tabulated']
    claim = next(x for x in claims if x.name == 'ListIsTabulated')
    assert isinstance(claim.model, t.RecordValue)
    assert [name for name, _ in claim.model.fields] == ['build']
    path = ROOT.parent / 'src/luthier/lib/core/lists.lut'
    program = parse(path.read_text()).program
    claim_act = next(a for a in program if getattr(a, 'name', None) == 'ListIsTabulated')
    ty = infer(elaborate_act(claim_act, c).body, c)
    while isinstance(ty, t.Pi):
        ty = ty.codomain
    assert ty == t.Var('Bool')
    # Testing one ordinary value is not a claim of the structure at the whole carrier.
    single_case = parse('SingleCase (A : U) : { element : A }\n'
                        'SingleCase (A : U) (m : SingleCase A) (x : A) : Bool := m.element == x\n'
                        'OnlyZero : Bool := SingleCase Int { element := 0 } 0').program
    assert not context_of(single_case).claims.get('SingleCase')
