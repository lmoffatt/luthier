"""Spec runner v2: semantic verdicts, cited rules and current diagnostic fragments."""

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Callable

import pytest

from luthier.parse import parse
from luthier.surface import Parsed, ParseFailed

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'tests/spec'
# Exact filenames, each justified by a current item; other syntax failures are bugs.
SYNTAX_REJECTIONS = {
    'r12_toplevel_arrow.reject.lut': 'spec 2.R5: top-level <- is excluded by luthierSyntax',
}


@dataclass(frozen=True)
class ExpectedMessage:
    provenance: str  # specified, v0.1, or proposed
    fragment: str


@dataclass(frozen=True)
class SpecCase:
    path: Path
    verdict: str
    expectations: tuple[ExpectedMessage, ...]
    source: str


def read_case(path: Path, source: str | None = None) -> SpecCase:
    """Read leading comments, including comments after blank lines before the first act."""
    source = path.read_text(encoding='utf-8') if source is None else source
    match = re.search(r'\.(accept|reject)\.lut$', path.name)
    if match is None:
        raise ValueError(f'{path}: missing accept/reject filename verdict')
    verdict = match[1]
    expectations = []
    overrides = []
    for line in source.splitlines():
        if not line.strip():
            continue
        if not line.startswith('--'):
            break
        expectation = re.fullmatch(r'-- expect(?: \((v0\.1|proposed)\))?:\s*(.+)', line)
        if expectation:
            expectations.append(ExpectedMessage(expectation[1] or 'specified', expectation[2]))
        elif line.startswith('-- expect'):
            raise ValueError(f'{path}: malformed expectation header: {line}')
        override = re.fullmatch(r'-- verdict:\s*(accept|reject)(?:\s+\(.*\))?\s*', line)
        if override:
            overrides.append(override[1])
        elif line.startswith('-- verdict:'):
            raise ValueError(f'{path}: malformed verdict override: {line}')
    if len(overrides) > 1:
        raise ValueError(f'{path}: multiple verdict overrides')
    return SpecCase(path, overrides[0] if overrides else verdict, tuple(expectations), source)


@dataclass(frozen=True)
class CheckerResult:
    accepted: bool
    message: str


# Adapter uses the semantic checker; syntax failures are distinct verdicts.
def checker(path):
    from luthier.check import check
    result = parse(path.read_text(encoding='utf-8'))
    if isinstance(result, ParseFailed):
        return CheckerResult(False, 'syntax: ' + '; '.join(e.message for e in result.errors))
    failures = check(result.program)
    return CheckerResult(not failures, '; '.join(f'{f.rule} {f.name}: {f.message}' for f in failures))


CHECKER: Callable[[Path], CheckerResult] | None = checker

# Fixed inventory: strict xfails become failures when a missing behavior is supplied.
LIMITATIONS = {
    'r6_predicate_body.accept.lut': 'Untyped predicate lambda domain remains Hole in existing elaboration.',
    'cite_proved.accept.lut': 'Literal dotted binder subtraction; cite is not a chapter 3/11 core interface.',
    'cite_not_reference.reject.lut': '6.R1 citation typing is outside program.lth.',
    'k_label_order.reject.lut': '3.R1/3.R2 checking of inline definitions is absent.',
    'k_recursor.accept.lut': 'Literal dotted binder subtraction and incomplete inferred lambda typing.',
    'k_union.accept.lut': 'Constructors of alias sums are not in knownWhole.',
    'n2_r_gone.reject.lut': '11.R1 is detected as unknown name 4.R2, not a numeric rule.',
    'n3_primitive_outside_core.reject.lut': '11.R2 file policy is absent; 4.R4 alone rejects.',
    'n4_axiom_outside_lib.reject.lut': '11.R3 file policy is absent.',
    'r12_block.accept.lut': 'Literal dotted binder subtraction and incomplete inferred lambda typing.',
    'r12_named_unknown.reject.lut': '2.R1 elaboration failure has no program.lth rejection predicate.',
    'r12_unused_rebinding.reject.lut': '2.R6 use-before-rebinding analysis is absent.',
    'r13_operator_by_type.accept.lut': 'Literal dotted binder subtraction rejects rep.',
    'r13_two_models.reject.lut': '4.R13 ambiguity is an elaboration law, not implemented here.',
    'r2_definition.accept.lut': 'theoryHeads suffix loses prior declaration; dotted binder subtraction; incomplete theory body typing.',
    'r2_definition.reject.lut': '4.R2 type-position and SCC half deliberately deferred.',
    'r4_product_inline.accept.lut': 'Literal dotted binder subtraction rejects first.',
    'r4_recursive_data.accept.lut': 'Literal dotted binder subtraction rejects fold laws.',
    'r5_extern_over_declared.reject.lut': '4.R5 literal predicate checks only a bare named type, not arrow components.',
    'r7_alias.accept.lut': 'Literal dotted binder subtraction rejects first.',
}

EXPECTED_RULE = {
    'cite_not_reference.reject.lut': '6.R1',
    'k_label_order.reject.lut': '3.R1',
    'n2_r_gone.reject.lut': '11.R1',
    'n3_primitive_outside_core.reject.lut': '11.R2',
    'n4_axiom_outside_lib.reject.lut': '11.R3',
    'r12_named_unknown.reject.lut': '2.R1',
    'r12_rebind_defined.reject.lut': '4.R12',
    'r12_unused_rebinding.reject.lut': '2.R6',
    'r12_toplevel_arrow.reject.lut': 'syntax',
    'r13_two_models.reject.lut': '4.R13',
    'r4_data_nonrecursive.reject.lut': '4.R3',
}


def compare_checker_verdict_and_message(case: SpecCase, result: CheckerResult,
                                        *, enforce_proposed: bool = False) -> None:
    """Enforce current diagnostics, never historical wording.

    Proposed diagnostics stay visible but require an explicit policy to enforce.
    Historical fragments are preserved without prescribing checker wording.
    """
    assert result.accepted == (case.verdict == 'accept'), (
        f'{case.path.name}: checker expected {case.verdict}; got {result}'
    )
    if case.verdict == 'reject':
        for expected in case.expectations:
            if expected.provenance == 'specified' or (
                enforce_proposed and expected.provenance == 'proposed'
            ):
                assert expected.fragment in result.message, (
                    f'{case.path.name}: missing {expected.provenance} fragment '
                    f'{expected.fragment!r} in {result.message!r}'
                )


CASES = tuple(read_case(path) for path in sorted(SPEC.glob('*.lut')))


@pytest.mark.parametrize('case', [pytest.param(c, marks=pytest.mark.xfail(strict=True, reason=LIMITATIONS[c.path.name])) if c.path.name in LIMITATIONS else c for c in CASES], ids=lambda case: case.path.name)
def test_spec_program_syntax(case, record_property):
    result = parse(case.source)
    record_property('intended_verdict', case.verdict)
    for expectation in case.expectations:
        record_property(f'expect_{expectation.provenance}', expectation.fragment)
    if case.path.name in SYNTAX_REJECTIONS:
        assert case.verdict == 'reject', case
        assert isinstance(result, ParseFailed), (case.path.name, result)
        record_property('syntax_rejection_reason', SYNTAX_REJECTIONS[case.path.name])
        compare_checker_verdict_and_message(case, CHECKER(case.path))
    else:
        # Semantic rejects must parse too, unless explicitly justified above.
        assert isinstance(result, Parsed), (case.path.name, case.verdict, result)
        if CHECKER is None:
            record_property('checker_status', 'pending: semantic verdict and diagnostic unverified')
        else:
            verdict = CHECKER(case.path)
            compare_checker_verdict_and_message(case, verdict)
            if case.verdict == 'reject':
                rule = EXPECTED_RULE.get(case.path.name)
                if rule is None:
                    rule = re.search(r'spec (4\.R\d+)', case.source)[1]
                assert rule + ' ' in verdict.message, (rule, verdict)


def test_suite_and_syntax_exception_inventory():
    assert CASES, 'No current spec programs found'
    assert (SPEC / 'README.md').is_file()
    assert set(SYNTAX_REJECTIONS) <= {case.path.name for case in CASES}
    assert all(reason for reason in SYNTAX_REJECTIONS.values())


def test_every_files_line_resolves_to_current_or_retired_suite():
    missing = []
    for chapter in sorted((ROOT / 'docs/spec').glob('*.md')):
        for number, line in enumerate(chapter.read_text(encoding='utf-8').splitlines(), 1):
            if line.startswith('Files:'):
                names = re.findall(r'([\w.-]+\.(?:lut|lth))', line)
                assert names, (chapter, number, line)
                for name in names:
                    if not (SPEC / name).is_file() and not (SPEC / 'v0.1' / name).is_file():
                        missing.append(f'{chapter.name}:{number}: {name}')
    assert not missing, '\n'.join(missing)


def test_header_preserves_diagnostic_provenance_and_verdict_override():
    case = read_case(Path('example.reject.lut'), '''-- spec 4.R4
-- expect: current wording
-- expect (v0.1): old wording

-- expect (proposed): proposed wording
-- verdict: accept (the rule changed)
x := 1
-- expect: body comment, not header metadata
''')
    assert case.verdict == 'accept'
    assert case.expectations == (
        ExpectedMessage('specified', 'current wording'),
        ExpectedMessage('v0.1', 'old wording'),
        ExpectedMessage('proposed', 'proposed wording'),
    )


@pytest.mark.parametrize('header', ['-- verdict: maybe', '-- verdict: accept\n-- verdict: reject',
                                    '-- expect (unknown): error', '-- expect:'])
def test_malformed_headers_fail_explicitly(header):
    with pytest.raises(ValueError):
        read_case(Path('example.reject.lut'), header + '\nx := 1\n')


def test_future_checker_hook_compares_verdict_and_current_message():
    case = read_case(Path('example.reject.lut'), '''-- expect: current wording
-- expect (v0.1): old wording
-- expect (proposed): proposed wording
x := 1
''')
    compare_checker_verdict_and_message(case, CheckerResult(False, 'has current wording'))
    with pytest.raises(AssertionError):
        compare_checker_verdict_and_message(case, CheckerResult(True, 'current wording'))
    with pytest.raises(AssertionError):
        compare_checker_verdict_and_message(case, CheckerResult(False, 'old wording only'))
    with pytest.raises(AssertionError):
        compare_checker_verdict_and_message(case, CheckerResult(False, 'current wording'),
                                           enforce_proposed=True)
