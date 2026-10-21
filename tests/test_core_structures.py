"""Bite 6: controls and certification of the bare structures (prompt-bite-6.md, 2859815)."""
from pathlib import Path

import pytest

from luthier import tester
from luthier.check import violatesS14
from luthier.parse import parse
from luthier.run import CORE, core_files
from luthier.surface import Define

TESTER = Path(__file__).parent / 'tester'


@pytest.fixture(scope='module')
def controls():
    return tester.run_tests(TESTER / 'core_controls.test.lut')


def test_each_new_mathematical_control_is_refuted(controls):
    witnesses = [o for o in controls if o.spec.law.startswith('Refute')]
    assert len(witnesses) >= 60
    assert all(o.verdict == 'Refuted' for o in witnesses), [(o.spec.law, (o.verdict, o.raised[:1], o.conjunct)) for o in witnesses if o.verdict != 'Refuted']


def test_the_four_metric_controls_are_refuted(controls):
    witnesses = [o for o in controls if o.spec.law == 'MetricCandidate']
    assert len(witnesses) == 4
    assert all(o.verdict == 'Refuted' for o in witnesses), [(o.verdict, o.raised[:1], o.conjunct) for o in witnesses]


def test_core_claimants_cross_core_file_boundaries():
    unclaimed = []
    for path in core_files(CORE):
        program = parse(path.read_text()).program
        for a in program:
            if isinstance(a, Define) and violatesS14(program, a.name):
                unclaimed.append((path.name, a.name))
    assert not unclaimed


def test_bare_theory_applies_its_model_to_every_conjunct():
    from luthier.elaborate import elaborate_program
    from luthier import term as t
    source = """T : { value : Int }
Positive (m : T) (x : Int) : Bool := m.value <= x
Negative (m : T) (y : Int) : Bool := y <= m.value
T (m : T) := Positive m & Negative m
Claim := T { value := 0 }
"""
    program = elaborate_program(parse(source).program)
    parts = tester.conjunction_parts(program, 'Claim')
    assert len(parts) == 2
    assert [ty.name for ty, _, _ in parts] == ['x', 'y']
    assert all(isinstance(ty, t.Pi) and ty.domain == t.Var('Int') for ty, _, _ in parts)


def test_explicit_model_binder_preserves_the_theory_record():
    from luthier.elaborate import elaborate_program
    from luthier.kernel import alpha_equal
    source = """T (A : U) : { value : A }
T (A : U) (m : T A) (x : A) : Bool := m.value == x
"""
    program = elaborate_program(parse(source).program)
    assert alpha_equal(program[0].type, program[1].type)


def test_every_core_control_refutes_its_candidate(controls):
    assert all(o.verdict == 'Refuted' for o in controls), [
        (o.spec.law, (o.verdict, o.raised[:1], o.conjunct)) for o in controls if o.verdict != 'Refuted']


def test_core_import_cycle_keeps_the_global_type_identities():
    from luthier.check import check
    path = CORE / 'lists.lut'
    assert not check(parse(path.read_text()).program, path)
