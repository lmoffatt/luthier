"""Check the generated vocabulary against the source value, without VS Code."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

from luthier.ebnf import GRAMMAR_LTH, lits_of, lits_of_names, luthier_syntax

EXTENSION = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('gen_grammar', EXTENSION / 'scripts/gen_grammar.py')
GEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GEN)


def test_vocabulary():
    generated = json.loads(GEN.OUTPUT.read_text())
    grammar = luthier_syntax()
    literals = set(lits_of(grammar))
    words = {v for v in literals if re.fullmatch(GEN.NAME, v)}
    levels = json.loads(re.search(r'^precedenceLevels\s*:[^\n]*:=\s*(\[[^\n]*\])',
                                 GRAMMAR_LTH.read_text(), re.M)[1])
    operators = set(lits_of_names(grammar, levels))
    patterns = generated['patterns']
    keywords = [p['match'] for p in patterns if p['name'].startswith('keyword.')]
    operator_patterns = [p['match'] for p in patterns if p['name'] == 'keyword.operator.luthier']
    for word in words:
        assert sum(bool(re.fullmatch(p, word)) for p in keywords) == 1, word
    for operator in operators:
        assert sum(bool(re.fullmatch(p, operator)) for p in operator_patterns) == 1, operator
    # Decode the emitted literal alternatives: equality catches extra entries too.
    emitted = []
    for pattern in keywords:
        start = pattern.index('(?:') + 3
        end = pattern.index(')', start)
        emitted.extend(re.sub(r'\\(.)', r'\1', v) for v in re.split(r'(?<!\\)\|', pattern[start:end]))
    assert len(emitted) == len(set(emitted))
    assert set(emitted) == words | operators
    for name in ['ordinary', 'dataX', 'm.data', 'data.m', *GEN.coreNames - words]:
        assert not any(re.fullmatch(p, name) for p in keywords), name


def test_check():
    subprocess.run([sys.executable, 'scripts/gen_grammar.py', '--check'],
                   cwd=EXTENSION, check=True)
    assert GEN.OUTPUT.read_text() == GEN.generate()


def test_lexical_patterns():
    patterns = json.loads(GEN.OUTPUT.read_text())['patterns']
    name = next(p['match'] for p in patterns if p['name'] == 'variable.other.luthier')
    assert re.fullmatch(name, "module.value'")
    escape = patterns[1]['patterns'][0]['match']
    for value in [r'\"', r'\\', r'\n']:
        assert re.fullmatch(escape, value)
    assert not re.fullmatch(escape, r'\t')
