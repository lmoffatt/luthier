"""The Python specimen of `Derives` (src/luthier/ebnf.py) on `luthierSyntax` read from grammar.lth."""

import re
from pathlib import Path
from time import perf_counter

import pytest

from luthier.ebnf import cats_of, count_derivations, lits_of, lits_of_names, luthier_syntax

G = luthier_syntax()
LITS = set(lits_of(G))


def views(text: str) -> list[tuple[str, str]]:
    """Tokens of a text whose tokens are separated by spaces, ended by the act's newline."""
    out = []
    for w in text.split():
        if w in LITS:
            out.append(("literal", w))
        elif re.fullmatch(r"[0-9][0-9.e-]*", w):
            out.append(("number", w))
        elif w.startswith('"'):
            out.append(("string", w))
        else:
            out.append(("name", w))
    return out + [("literal", "\n")]


def test_the_grammar_is_read_whole():
    names = {lhs for lhs, _ in G.rules}
    assert G.start == "program" and "term" in names and "arrowOpen" in names
    assert set(cats_of(G)) == {"name", "string", "number"}


def test_keywords_and_operators_are_derived():
    words = {w for w in LITS if re.fullmatch(r"[A-Za-z]+", w)}
    assert words == {"import", "as", "operator", "and", "or", "mod", "data", "if", "then", "else",
                     "match", "U", "W", "quote", "fn"}
    levels = ["ampTerm", "arrowTerm", "orTerm", "andTerm", "cmpTerm", "addTerm", "mulTerm"]
    assert lits_of_names(G, levels) == ["&", "->", "or", "and", "==", "/=", "<", "<=", ">", ">=",
                                        "+", "-", "*", "/", "mod"]


def test_one_tree_where_round_3_found_two():
    for text in ["x := U -> ( a : A ) * b & C", "x := A -> if c then y & z",
                 "x := A -> ( b : B ) -> C & D", "x := P & ( y : A ) -> Q", "x := A -> B & C",
                 "x := ( n : Nat ) * Vec n", "x := f a + g b", "x := f { a : A || b : B }", "x := if c then ( if d then y ) else b"]:
        assert count_derivations(G, views(text)) == 1, text


def test_the_dangling_else_derives_twice_and_the_parser_chooses():
    assert count_derivations(G, views("x := if a then if b then p else q")) == 2


def test_what_does_not_derive():
    for text in ["x := { a : A || b : B, c : C }", "x := fn ( y ) { y }", "x := a + if c then a else b",
                 "operator == := eqZ7", "x <- 1"]:
        assert count_derivations(G, views(text)) == 0, text


def test_a_program_derives_act_by_act():
    from luthier.ebnf import derives, derives_program
    text = views("x := A -> B") + views("y := f a")
    assert derives_program(G, text) == derives(G, text)
    assert derives_program(G, [])
    assert not derives_program(G, views("x := { a : A || b : B, c : C }") + views("y := a"))
    assert not derives_program(G, views("x := a")[:-1])


@pytest.mark.parametrize("filename", ["grammar.lth", "ebnf.lth", "ebnf_model.lut"])
def test_bootstrap_file_derives_in_under_ten_seconds(filename):
    from luthier.ebnf import derives_program
    from luthier.parse import layout, lex
    from luthier.surface import Lexed

    path = Path(__file__).parents[1] / "src/luthier/lib" / filename
    lexed = lex(path.read_text(encoding="utf-8"))
    assert isinstance(lexed, Lexed)
    tokens = list(layout(lexed.tokens))
    started = perf_counter()
    assert derives_program(G, tokens, end=("newline", "\n"))
    assert perf_counter() - started < 10


def test_earley_preserves_nullable_choices_and_consuming_repetition():
    from luthier.ebnf import Ebnf

    def count(rhs, tokens):
        return count_derivations(Ebnf("s", (("s", rhs),)), tokens)

    eps = ("eps",)
    a = ("lit", "a")
    token = [("anything", "a")]
    assert count(("seq", ()), []) == 1
    assert count(("alt", ()), []) == 0
    assert count(("opt", eps), []) == 2
    assert count(("alt", (a, a, a)), token) == 2
    assert count(("seq", (("opt", a), ("opt", a))), token) == 2
    assert count(("rep", ("opt", a)), []) == 1
    assert count(("rep", ("opt", a)), token * 3) == 1
    assert count(("rep", eps), token) == 0


def test_earley_counts_duplicate_rules_and_matches_categories():
    from luthier.ebnf import Ebnf

    grammar = Ebnf("s", (("s", ("cat", "name")), ("s", ("lit", "a"))))
    assert count_derivations(grammar, [("name", "a")]) == 2
    assert count_derivations(grammar, [("number", "a")]) == 1
    assert count_derivations(grammar, [("name", "b")]) == 1
    assert count_derivations(grammar, [("number", "b")]) == 0
    assert count_derivations(grammar, [], "missing") == 0
