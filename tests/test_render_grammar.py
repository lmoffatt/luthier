"""Read chapter notation independently and compare it with the authoritative value."""

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from luthier.ebnf import luthier_syntax

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/render_grammar.py"
spec = importlib.util.spec_from_file_location("render_grammar", SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def read_rendering(text):
    productions = re.split(r"^    ([A-Za-z][A-Za-z0-9_]*) ::=", text, flags=re.M)
    assert not productions[0].strip()
    rules = []
    for name, body in zip(productions[1::2], productions[2::2]):
        tokens = re.findall(r'"(?:\\.|[^"\\])*"|[A-Za-z][A-Za-z0-9_]*|[|()\[\]{}]', body)
        assert re.sub(
            r'"(?:\\.|[^"\\])*"|[A-Za-z][A-Za-z0-9_]*|[|()\[\]{}]|\s+', '', body
        ) == ''
        pos = 0

        def expression():
            nonlocal pos
            alternatives = [sequence()]
            while pos < len(tokens) and tokens[pos] == "|":
                pos += 1
                alternatives.append(sequence())
            return alternatives[0] if len(alternatives) == 1 else ("alt", tuple(alternatives))

        def sequence():
            nonlocal pos
            items = []
            while pos < len(tokens) and tokens[pos] not in ("|", ")", "]", "}"):
                token = tokens[pos]
                pos += 1
                if token in ("(", "[", "{"):
                    inner = expression()
                    assert tokens[pos] == {"(": ")", "[": "]", "{": "}"}[token]
                    pos += 1
                    items.append(inner if token == "(" else
                                 ("opt" if token == "[" else "rep", inner))
                elif token.startswith('"'):
                    items.append(("lit", json.loads(token)))
                elif token == "newline":
                    items.append(("lit", "\n"))
                else:
                    items.append(("cat" if token in {"name", "number", "string"} else "ref", token))
            assert items
            return items[0] if len(items) == 1 else ("seq", tuple(items))

        rules.append((name, expression()))
        assert pos == len(tokens)
    return tuple(rules)


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True)


def test_rendering_round_trips_every_rule():
    grammar = luthier_syntax()
    rendered = renderer.render(grammar)
    assert all(len(line) <= 100 for line in rendered.splitlines())
    assert read_rendering(rendered) == grammar.rules


def test_repository_is_current():
    result = run("--check")
    assert result.returncode == 0, result.stderr


def test_write_copy_is_idempotent(tmp_path):
    chapter = tmp_path / "chapter.md"
    chapter.write_bytes(renderer.CHAPTER.read_bytes())
    assert run("--write", "--chapter", chapter).returncode == 0
    first = chapter.read_bytes()
    assert run("--write", "--chapter", chapter).returncode == 0
    assert chapter.read_bytes() == first
    assert run("--check", "--chapter", chapter).returncode == 0


@pytest.mark.parametrize("content", ["no markers\n", renderer.END + "\n" + renderer.BEGIN + "\n"])
def test_check_reports_missing_or_invalid_markers(tmp_path, content):
    chapter = tmp_path / "chapter.md"
    chapter.write_text(content)
    result = run("--check", "--chapter", chapter)
    assert result.returncode == 1
    assert "marker" in result.stderr


def test_check_reports_stale_block_and_write_preserves_surroundings(tmp_path):
    chapter = tmp_path / "chapter.md"
    prefix = "Original prose.\n\n" + renderer.BEGIN + "\n"
    suffix = renderer.END + "\n\nOriginal productions.\n"
    chapter.write_text(prefix + "stale\n" + suffix)
    result = run("--check", "--chapter", chapter)
    assert result.returncode == 1 and "stale" in result.stderr
    assert run("--write", "--chapter", chapter).returncode == 0
    assert chapter.read_text() == prefix + renderer.generated_block()[1:] + suffix
