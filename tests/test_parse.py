"""The laws of ``Grammar`` in ``grammar.lth``, transcribed as pytest tests."""

from __future__ import annotations

from pathlib import Path
import random
import re

from luthier.ebnf import cats_of, count_derivations, lits_of, lits_of_names, luthier_syntax
from luthier.parse import layout, lex, parse, print_program
from luthier.surface import (
    Alias, App, Binop, Bind, Block, Clause, ClausesBody, DataBody, Datum, Declare,
    Define, Explicit, Field, FloatLit, IfThen, ImportAct, ImportName, Implicit,
    IntLit, Lambda, LexFailed, Lexed, List, Literal, MatchOf, Name, NamedArg, Neg,
    OperatorAct, PApp, PLit, PTuple, PWild, ParseFailed, Parsed, Pi, PlainParam,
    Proj, Quoted, Rebind, Record, RecordValue, ShapeParam, Sigma, SigmaNamed,
    StringLit, Subtype, Sum, SumNamed, TermBody, Tuple, TypedParam, Universe, World,
)

G = luthier_syntax()
LITS = set(lits_of(G))
LIB = Path(__file__).parents[1] / "src" / "luthier" / "lib"
FILES = [LIB / "grammar.lth", LIB / "ebnf.lth", LIB / "ebnf_model.lut"]


def nm(s: str):
    return Name(s)


def numeral(n: int):
    return Literal(IntLit(n))


def defx(t):
    return Parsed((Define("x", (), None, TermBody(t)),))


def parsed(text: str):
    r = parse(text)
    assert isinstance(r, Parsed), (text, r)
    return r


def same_parse(a: str, b: str) -> None:
    assert parsed(a) == parsed(b)


def same_layout(a: str, b: str) -> None:
    la, lb = lex(a), lex(b)
    assert isinstance(la, Lexed) and isinstance(lb, Lexed)
    assert layout(la.tokens) == layout(lb.tokens)
    assert isinstance(parse(a), Parsed)


CASE_TEXTS = [
    '"a b"', '"abc', '"a\\"b"', 'x -- a comment', 'x', 'a<-1',
    'f (a : Int) : Bool := a < -1', 'f (a : Int) : Bool := a < (-1)',
    'f (a : Int) : Int :=\n  a + 1', 'f (a : Int) : Int := a + 1',
    'x := f (a,\n  b)', 'x := f (a, b)', 'x := [a,\n  b]', 'x := [a, b]',
    'x := < a : A\n  | b : B >', 'x := < a : A | b : B >',
    'x := match m {\n  a -> b ;\n  c -> e }', 'x := match m { a -> b ; c -> e }',
    'f := {\n  a := 1\n  b := 2\n  a + b\n}', 'f := { a := 1 ; b := 2 ; a + b }',
    'x := {\n  a := 1\n  b := 2\n}', 'x := { a := 1 ; b := 2 }',
    'R = {\n  a : Int\n  b : Int\n}', 'R = { a : Int ; b : Int }',
    'C : U := data {\n  r : C\n  s : C\n}', 'C : U := data { r : C ; s : C }',
    'f := {\n  a := 1\n    + 2\n  a }', 'f := { a := 1 + 2 ; a }',
    'f := {\n  a := if c\n  then 1\n  else 2\n  a }', 'f := { a := if c then 1 else 2 ; a }',
    'f := {\n  a := x\n  + 2\n  a }', 'f := { a := x + 2 ; a }',
    '-- a header\n\nx : Int\n\n-- between\ny : Int', 'x : Int\ny : Int',
    'x := match m { a -> b ; }', 'x := match m { a -> b }',
    'C : U := data { r : C ; }', 'C : U := data { r : C }',
    'x := { a := 1, }', 'x := { a := 1 }',
    'x := { a : Int, b : Int, }', 'x := { a : Int, b : Int }',
    'x := { a := 1 ; a ; }', 'x := { a := 1 ; a }',
    'x := [a, b,]', 'x := [a, b]',
    'x := a + b * c', 'x := a + (b * c)', 'x := a < b and c', 'x := (a < b) and c',
    'x := a or b and c', 'x := a or (b and c)', 'x := a or b -> c', 'x := (a or b) -> c',
    'x := A -> B & C', 'x := (A -> B) & C', 'x := a + b == c', 'x := (a + b) == c',
    'x := A -> B -> C', 'x := A -> (B -> C)', 'x := A & B & C', 'x := A & (B & C)',
    'x := a - b - c', 'x := (a - b) - c', 'x := a / b * c', 'x := (a / b) * c',
    'x := a < b == c', 'x := (a < b) == c', 'x := a or b or c', 'x := (a or b) or c',
    'x := a and b and c', 'x := (a and b) and c', 'x := a mod b * c', 'x := (a mod b) * c',
    'x := f a b', 'x := (f a) b', 'x := f a + g b', 'x := (f a) + (g b)',
    'x := f (p).field', 'x := f ((p).field)', 'x := -f a', 'x := -(f a)',
    'x := f -a', 'x := f - a', 'x := -a * b', 'x := (-a) * b', 'x := -a + b', 'x := (-a) + b',
    'x := (n : Nat) * Vec n', 'x := (a : A) -> B c', 'x := (a : A) * (b : B) * C',
    'x := if c then a else b + 1', 'x := A -> (b : B) -> C', 'x := P & (y : A) -> Q',
    'x := A -> if c then a', 'x := a + if c then a else b',
    'x := U -> (a : A) * b & C', 'x := A -> (b : B) -> C & D',
    'x := if c then (if d then y) else b', 'x := if a then if b then p else q',
    'x := f (< a : A | b : B >)', 'x := f < a : A | b : B >',
    'f (a : Int) : Int', 'x : Int := 1', 'f (a b : Int) (t : Int <- 1) : Int := t',
    'id {A : U} (y : A) : A := y', 'Pair (A : U) = A * A',
    'Color : U := data { red : Color ; green : Color }', 'Empty : U := data { }',
    'neg (b : Bool) : Bool\n  | true := false\n  | false := true',
    'f (a b : Bool) : Bool\n  | true, _ := a\n  | _, y := y',
    'f (b : Bool) : Bool := b\n  | true := false',
    'operator + := addZ7', 'operator and := boolAnd', 'operator == := eqZ7',
    'import "linear_algebra.lth" LinearAlgebra',
    'import "la_numpy.lut" Numpy : LinearAlgebra as LA Helpers', 'import "x.lut"',
    'test f', 'eval A t', 'x <- 1', 'x := 3', 'x := 3.5', 'x := "a"',
    'x := (a b : Int) -> Int', 'x := (a : A) * (b : B)', 'x := (a : A) + (b : B)',
    'x := { a : Int }', 'x := { a b : Int, c : Float64 }', 'x := { a : Int, b : Int | a < b }',
    'x := { a : Int | 0 <= a }', 'x := { a b : Int | a < b }', 'x := { (p, q) : P | p < q }',
    'x := { _ : T | p }', 'x := { a := 1 ; a }', 'x := { a := 1 }',
    'x := { a <- 1, a <- a + 1, a }', 'x := (a, b, c)', 'x := [1, 2]', 'x := []',
    'x := \\ y (z : Int) { w := y ; z }', 'x := \\ (p, q) { p }', 'x := \\ (a b : A) { a }',
    'x := \\ (y) { y }',
    'x := match m { just y -> y ; _ -> 0 ; 1 -> 2 ; (a, b) -> a ; cons _ rest -> rest }',
    'x := match m { (y) -> y }', 'x := match e { }', 'x := f (tol <- 1)',
    'x := if c then a', 'x := if c then a else b', 'x := (f y).z', 'x := m.f',
    'x := quote { a + b }', 'x := U -> W', 'x := P & Q', 'x := -1', 'x := )',
]


def _grammar_generated_texts(count: int = 36) -> list[str]:
    """Generate derivable acts; at the depth bound choose a shortest alternative."""
    rules = {n: G.rules_of(n) for n, _ in G.rules}
    inf = 10**9
    costs = {n: inf for n in rules}

    def cost(r):
        k = r[0]
        if k == "eps":
            return 0
        if k in ("lit", "cat"):
            return 1
        if k == "ref":
            return costs[r[1]]
        if k == "seq":
            return sum(cost(x) for x in r[1])
        if k == "alt":
            return min(cost(x) for x in r[1])
        if k in ("opt", "rep"):
            return 0
        raise AssertionError(k)

    for _ in range(100):
        changed = False
        for name, rhss in rules.items():
            c = min(cost(r) for r in rhss)
            if c < costs[name]:
                costs[name] = c
                changed = True
        if not changed:
            break

    cats = {"name": "x", "number": "1", "string": '"s"'}

    def shortest(r):
        k = r[0]
        if k == "eps":
            return []
        if k == "lit":
            return [r[1]]
        if k == "cat":
            return [cats[r[1]]]
        if k == "ref":
            return shortest(min(rules[r[1]], key=cost))
        if k == "seq":
            return sum((shortest(x) for x in r[1]), [])
        if k == "alt":
            return shortest(min(r[1], key=cost))
        if k in ("opt", "rep"):
            return []
        raise AssertionError(k)

    rng = random.Random(20261013)

    def expand(r, depth):
        if depth <= 0:
            return shortest(r)
        k = r[0]
        if k == "eps":
            return []
        if k == "lit":
            return [r[1]]
        if k == "cat":
            return [cats[r[1]]]
        if k == "ref":
            return expand(rng.choice(rules[r[1]]), depth - 1)
        if k == "seq":
            return sum((expand(x, depth - 1) for x in r[1]), [])
        if k == "alt":
            return expand(rng.choice(r[1]), depth - 1)
        if k == "opt":
            return expand(r[1], depth - 1) if rng.randrange(2) else []
        if k == "rep":
            return sum(
                (
                    expand(r[1], depth - 1)
                    for _ in range(rng.choice((0, 0, 1, 1, 2)))
                ),
                [],
            )
        raise AssertionError(k)

    def source(tokens):
        return "".join("\n" if t == "\n" else t + " " for t in tokens)

    return [
        source(expand(("ref", "act"), 7 + (i % 5)) + ["\n"])
        for i in range(count)
    ]


GENERATED_TEXTS = _grammar_generated_texts()


def _all_texts():
    yield from CASE_TEXTS
    for p in FILES:
        yield p.read_text(encoding="utf-8")
    yield from GENERATED_TEXTS


def _is_parsed(r) -> bool:
    return isinstance(r, Parsed)


def _is_luthier_syntax_act(segment: list[tuple[str, str]]) -> bool:
    return (
        len(segment) >= 2
        and segment[0] == ("name", "luthierSyntax")
        and segment[1] == ("literal", ":")
    )


def _derives_by_acts(text: str) -> bool:
    """Check every laid-out act, including the grammar's own definition."""
    from luthier.ebnf import derives_program

    lr = lex(text)
    if isinstance(lr, LexFailed):
        return False
    return derives_program(G, list(layout(lr.tokens)), end=("newline", "\n"))


# ---------------------------------------------------------------- general laws

def test_round_trip():
    for text in _all_texts():
        r = parse(text)
        if isinstance(r, Parsed):
            assert parse(print_program(r.program)) == r


def test_canonical():
    for text in _all_texts():
        r = parse(text)
        if isinstance(r, Parsed):
            assert parse(print_program(r.program)) == r


def test_parsed_is_written():
    for text in _all_texts():
        r = parse(text)
        if isinstance(r, Parsed):
            assert parse(print_program(r.program)) == r


def test_parses_what_derives():
    for text in _all_texts():
        assert _is_parsed(parse(text)) == _derives_by_acts(text), text


def test_parses_what_derives_luthier_syntax_act():
    text = (LIB / "grammar.lth").read_text(encoding="utf-8")
    lr = lex(text)
    assert isinstance(lr, Lexed)
    views = list(layout(lr.tokens))
    start = 0
    for i, tv in enumerate(views):
        if tv == ("newline", "\n"):
            segment = views[start:i]
            if _is_luthier_syntax_act(segment):
                assert count_derivations(G, segment, "act") > 0
                return
            start = i + 1
    raise AssertionError("luthierSyntax act not found")


def test_match_followed_by_block_is_unambiguous():
    text = "x := match f { p -> q } { r -> s }"
    lr = lex(text)
    assert isinstance(lr, Lexed)
    views = list(layout(lr.tokens))
    assert views[-1] == ("newline", "\n")
    assert count_derivations(G, views[:-1], "act") == 1
    assert parse(text) == defx(
        App(MatchOf(nm("f"), ((PApp("p", ()), nm("q")),)),
            Block((), Binop("->", nm("r"), nm("s"))))
    )


def test_errors_have_lines():
    for text in _all_texts():
        r = parse(text)
        if isinstance(r, ParseFailed):
            assert r.errors and all(e.line >= 1 for e in r.errors)


# ---------------------------------------------------------------- lexical laws

def test_literals_are_not_names():
    for w in lits_of(G):
        if w == "\n":
            continue
        r = lex(w)
        assert isinstance(r, Lexed)
        assert [(t.kind, t.text) for t in r.tokens] == [("literal", w)]


def test_other_words_are_names():
    for w in [
        "let", "in", "test", "with", "extern", "primitive", "axiom", "forget",
        "cite", "eval", "provisional", "Bool",
    ]:
        r = lex(w)
        assert isinstance(r, Lexed)
        assert [(t.kind, t.text) for t in r.tokens] == [("name", w)]


def test_kinds_are_the_grammars():
    known = set(cats_of(G)) | {"literal", "newline"}
    for text in _all_texts():
        r = lex(text)
        if isinstance(r, Lexed):
            assert all(t.kind in known - {"newline"} for t in r.tokens)
            assert all(k in known for k, _ in layout(r.tokens))


def test_name_tokens():
    r = lex("x_1 a' m.f")
    assert isinstance(r, Lexed)
    assert [(t.kind, t.text) for t in r.tokens] == [
        ("name", "x_1"),
        ("name", "a'"),
        ("name", "m.f"),
    ]
    assert not (
        isinstance(lex("1x"), Lexed)
        and len(lex("1x").tokens) == 1
        and lex("1x").tokens[0].kind == "name"
    )
    assert not (
        isinstance(lex("a b"), Lexed)
        and len(lex("a b").tokens) == 1
        and lex("a b").tokens[0].kind == "name"
    )
    assert not (
        isinstance(lex("_"), Lexed)
        and len(lex("_").tokens) == 1
        and lex("_").tokens[0].kind == "name"
    )


def test_number_tokens():
    r = lex("42 3.5 1e3 2.0e-1")
    assert isinstance(r, Lexed)
    assert [(t.kind, t.text) for t in r.tokens] == [
        ("number", x) for x in ["42", "3.5", "1e3", "2.0e-1"]
    ]


def test_string_tokens():
    r = lex('"a b"')
    assert isinstance(r, Lexed)
    assert [(t.kind, t.text) for t in r.tokens] == [("string", '"a b"')]
    assert isinstance(lex('"abc'), LexFailed)
    r = lex('"a\\"b"')
    assert isinstance(r, Lexed)
    assert [(t.kind, t.text) for t in r.tokens] == [("string", '"a\\"b"')]
    assert parse('x := "a\\"b\\\\c\\nd"') == defx(
        Literal(StringLit('a"b\\c\nd'))
    )


def test_lex_errors_have_lines():
    for text in list(_all_texts()) + ['"abc', "§"]:
        r = lex(text)
        if isinstance(r, LexFailed):
            assert r.error.line >= 1


def test_comment_dropped():
    a, b = lex("x -- a comment"), lex("x")
    assert isinstance(a, Lexed) and isinstance(b, Lexed)
    assert [(t.kind, t.text) for t in a.tokens] == [
        (t.kind, t.text) for t in b.tokens
    ]


def test_arrow_is_one_token():
    r = lex("a<-1")
    assert isinstance(r, Lexed)
    assert [(t.kind, t.text) for t in r.tokens] == [
        ("name", "a"),
        ("literal", "<-"),
        ("number", "1"),
    ]
    same_parse(
        "f (a : Int) : Bool := a < -1",
        "f (a : Int) : Bool := a < (-1)",
    )


# ---------------------------------------------------------------- layout laws

def test_layout_ends():
    for text in _all_texts():
        r = lex(text)
        if isinstance(r, Lexed):
            v = layout(r.tokens)
            assert not v or v[-1][0] == "newline"


def test_column_zero_starts_act():
    assert parse("x := a\n-b") == Parsed((
        Define("x", (), None, TermBody(nm("a"))), Datum(Neg(nm("b"))),
    ))
    assert parse("x := a\n< c : U >") == Parsed((
        Define("x", (), None, TermBody(nm("a"))), Datum(Sum((("c", Universe()),))),
    ))


def test_zero_float_prints_without_a_sign():
    for value in (0.0, -0.0):
        program = (Datum(Literal(FloatLit(value))),)
        assert print_program(program) == "0.0\n"
        assert parse(print_program(program)) == Parsed(program)
        pattern_program = (Datum(MatchOf(nm("a"), ((PLit(FloatLit(value)), nm("b")),))),)
        assert print_program(pattern_program) == "match a { 0.0 -> b }\n"
        assert parse(print_program(pattern_program)) == Parsed(pattern_program)


def test_indent_continues_act():
    same_layout(
        "f (a : Int) : Int :=\n  a + 1",
        "f (a : Int) : Int := a + 1",
    )


def test_brackets_ignore_breaks():
    same_layout("x := f (a,\n  b)", "x := f (a, b)")
    same_layout("x := [a,\n  b]", "x := [a, b]")
    same_layout(
        "x := < a : A\n  | b : B >",
        "x := < a : A | b : B >",
    )
    same_layout(
        "x := match m {\n  a -> b ;\n  c -> e }",
        "x := match m { a -> b ; c -> e }",
    )


def test_layout_classifies_brackets_from_the_prefix():
    same_layout("x := quote {\n a\n b\n}", "x := quote { a b }")
    same_layout(
        "x := match (f {\n a := 1\n a\n}) {\n p -> q\n}",
        "x := match (f { a := 1 ; a }) { p -> q }",
    )
    same_layout(
        "x := match [match m {\n p -> q\n}] {\n r -> s\n}",
        "x := match [match m { p -> q }] { r -> s }",
    )
    same_layout(
        "x := < a : (A >\n b)\n > b > c\ny := d",
        "x := < a : (A > b) > b > c\ny := d",
    )
    lr = lex("x := < a : A > b > c\ny := d")
    assert isinstance(lr, Lexed)
    assert sum(text == "\n" for _, text in layout(lr.tokens)) == 2
    # Match arms suppress the break; a following block inserts a separator.
    same_layout(
        "x := match f {\n p -> q\n} {\n a := 1\n a\n}",
        "x := match f { p -> q } { a := 1 ; a }",
    )


def test_break_separates_items():
    same_layout(
        "f := {\n  a := 1\n  b := 2\n  a + b\n}",
        "f := { a := 1 ; b := 2 ; a + b }",
    )
    same_layout(
        "x := {\n  a := 1\n  b := 2\n}",
        "x := { a := 1 ; b := 2 }",
    )
    same_layout(
        "R = {\n  a : Int\n  b : Int\n}",
        "R = { a : Int ; b : Int }",
    )


def test_break_separates_constructors():
    same_layout(
        "C : U := data {\n  r : C\n  s : C\n}",
        "C : U := data { r : C ; s : C }",
    )


def test_continuation_lines():
    same_layout(
        "f := {\n  a := 1\n    + 2\n  a }",
        "f := { a := 1 + 2 ; a }",
    )
    same_layout(
        "f := {\n  a := if c\n  then 1\n  else 2\n  a }",
        "f := { a := if c then 1 else 2 ; a }",
    )
    same_layout(
        "f := {\n  a := x\n  + 2\n  a }",
        "f := { a := x + 2 ; a }",
    )


def test_blank_and_comment_lines_dropped():
    same_layout(
        "-- a header\n\nx : Int\n\n-- between\ny : Int",
        "x : Int\ny : Int",
    )


def test_trailing_separators():
    for a, b in [
        ("x := match m { a -> b ; }", "x := match m { a -> b }"),
        ("C : U := data { r : C ; }", "C : U := data { r : C }"),
        ("x := { a := 1, }", "x := { a := 1 }"),
        ("x := { a : Int, b : Int, }", "x := { a : Int, b : Int }"),
        ("x := { a := 1 ; a ; }", "x := { a := 1 ; a }"),
        ("x := [a, b,]", "x := [a, b]"),
    ]:
        same_parse(a, b)


# ---------------------------------------------------------------- precedence laws

def test_plus_before_times():
    same_parse("x := a + b * c", "x := a + (b * c)")


def test_comparison_before_and():
    same_parse("x := a < b and c", "x := (a < b) and c")


def test_and_before_or():
    same_parse("x := a or b and c", "x := a or (b and c)")


def test_or_before_arrow():
    same_parse("x := a or b -> c", "x := (a or b) -> c")


def test_arrow_before_amp():
    same_parse("x := A -> B & C", "x := (A -> B) & C")


def test_equality_before_plus():
    same_parse("x := a + b == c", "x := (a + b) == c")


def test_right_associative():
    same_parse("x := A -> B -> C", "x := A -> (B -> C)")
    same_parse("x := A & B & C", "x := A & (B & C)")


def test_left_associative():
    for a, b in [
        ("x := a - b - c", "x := (a - b) - c"),
        ("x := a / b * c", "x := (a / b) * c"),
        ("x := a < b == c", "x := (a < b) == c"),
        ("x := a or b or c", "x := (a or b) or c"),
        ("x := a and b and c", "x := (a and b) and c"),
        ("x := a mod b * c", "x := (a mod b) * c"),
        ("x := f a b", "x := (f a) b"),
    ]:
        same_parse(a, b)


def test_application_tightest():
    same_parse("x := f a + g b", "x := (f a) + (g b)")


def test_projection_tightest():
    same_parse("x := f (p).field", "x := f ((p).field)")


def test_negation():
    same_parse("x := -f a", "x := -(f a)")
    same_parse("x := f -a", "x := f - a")
    same_parse("x := -a * b", "x := (-a) * b")
    same_parse("x := -a + b", "x := (-a) + b")


def test_open_forms():
    assert parse("x := (n : Nat) * Vec n") == defx(
        Sigma(("n",), nm("Nat"), App(nm("Vec"), nm("n")))
    )
    assert parse("x := (a : A) -> B c") == defx(
        Pi(("a",), nm("A"), App(nm("B"), nm("c")))
    )
    assert parse("x := (a : A) * (b : B) * C") == defx(
        Sigma(("a",), nm("A"), Sigma(("b",), nm("B"), nm("C")))
    )
    assert parse("x := if c then a else b + 1") == defx(
        IfThen(nm("c"), nm("a"), Binop("+", nm("b"), numeral(1)))
    )
    assert parse("x := A -> (b : B) -> C") == defx(
        Binop("->", nm("A"), Pi(("b",), nm("B"), nm("C")))
    )
    assert parse("x := P & (y : A) -> Q") == defx(
        Binop("&", nm("P"), Pi(("y",), nm("A"), nm("Q")))
    )
    assert parse("x := A -> if c then a") == defx(
        Binop("->", nm("A"), IfThen(nm("c"), nm("a"), None))
    )
    assert isinstance(parse("x := a + if c then a else b"), ParseFailed)


def test_open_form_ends_its_term():
    assert parse("x := U -> (a : A) * b & C") == defx(
        Binop(
            "->",
            Universe(),
            Sigma(("a",), nm("A"), Binop("&", nm("b"), nm("C"))),
        )
    )
    assert parse("x := A -> (b : B) -> C & D") == defx(
        Binop(
            "->",
            nm("A"),
            Pi(("b",), nm("B"), Binop("&", nm("C"), nm("D"))),
        )
    )


def test_print_parenthesizes():
    trees = [
        MatchOf(App(nm("f"), Block((), nm("a"))), ((PApp("p", ()), nm("q")),)),
        Sum((("a", Binop(">", nm("A"), nm("b"))),)),
        Sum((("a", Pi(("x",), nm("A"), nm("B"))),)),
        IfThen(nm("c"), IfThen(nm("d"), nm("y"), None), nm("b")),
        IfThen(
            nm("c"),
            IfThen(nm("d"), nm("y"), IfThen(nm("e"), nm("z"), None)),
            nm("b"),
        ),
        Binop(
            "&",
            Binop("->", Universe(), Sigma(("a",), nm("A"), nm("b"))),
            nm("C"),
        ),
    ]
    for t in trees:
        p = (Define("x", (), None, TermBody(t)),)
        assert parse(print_program(p)) == Parsed(p)
    assert parse("x := if c then (if d then y) else b") == defx(
        IfThen(nm("c"), IfThen(nm("d"), nm("y"), None), nm("b"))
    )


def test_dangling_else():
    assert parse("x := if a then if b then p else q") == defx(
        IfThen(nm("a"), IfThen(nm("b"), nm("p"), nm("q")), None)
    )


def test_sum_as_argument():
    assert parse("x := f (< a : A | b : B >)") == defx(
        App(nm("f"), Sum((("a", nm("A")), ("b", nm("B")))))
    )
    assert isinstance(parse("x := f < a : A | b : B >"), ParseFailed)
    assert parse("x := < a : A > b > c") == defx(
        Binop(">", App(Sum((("a", nm("A")),)), nm("b")), nm("c"))
    )
    assert parse("x := < a : (A > b) >") == defx(
        Sum((("a", Binop(">", nm("A"), nm("b"))),))
    )


def test_sum_alternative_precedence_and_parentheses():
    for value in [
        "A & B -> C or D and E == F + G * H",
        "(if c then A else B)", "((x : A) -> B)", "(A > b)",
    ]:
        text = f"x := < a : {value} >"
        assert _derives_by_acts(text)
        result = parsed(text)
        assert parse(print_program(result.program)) == result
    for value in ["if c then A else B", "(x : A) -> B"]:
        text = f"x := < a : {value} >"
        assert isinstance(parse(text), ParseFailed)
        assert not _derives_by_acts(text)


# ---------------------------------------------------------------- tree laws

def test_declaration_tree():
    assert parse("f (a : Int) : Int") == Parsed(
        (
            Declare(
                "f",
                (Explicit(("a",), nm("Int"), None),),
                nm("Int"),
            ),
        )
    )


def test_definition_tree():
    assert parse("x : Int := 1") == Parsed(
        (Define("x", (), nm("Int"), TermBody(numeral(1))),)
    )


def test_default_tree():
    assert parse("f (a b : Int) (t : Int <- 1) : Int := t") == Parsed(
        (
            Define(
                "f",
                (
                    Explicit(("a", "b"), nm("Int"), None),
                    Explicit(("t",), nm("Int"), numeral(1)),
                ),
                nm("Int"),
                TermBody(nm("t")),
            ),
        )
    )


def test_implicit_tree():
    assert parse("id {A : U} (y : A) : A := y") == Parsed(
        (
            Define(
                "id",
                (
                    Implicit(("A",), Universe()),
                    Explicit(("y",), nm("A"), None),
                ),
                nm("A"),
                TermBody(nm("y")),
            ),
        )
    )


def test_alias_tree():
    assert parse("Pair (A : U) = A * A") == Parsed(
        (
            Alias(
                "Pair",
                (Explicit(("A",), Universe(), None),),
                Binop("*", nm("A"), nm("A")),
            ),
        )
    )


def test_data_tree():
    assert parse("Color : U := data { red : Color ; green : Color }") == Parsed(
        (
            Define(
                "Color",
                (),
                Universe(),
                DataBody((("red", nm("Color")), ("green", nm("Color")))),
            ),
        )
    )
    assert parse("Empty : U := data { }") == Parsed(
        (Define("Empty", (), Universe(), DataBody(())),)
    )


def test_clause_tree():
    assert parse(
        "neg (b : Bool) : Bool\n"
        "  | true := false\n"
        "  | false := true"
    ) == Parsed(
        (
            Define(
                "neg",
                (Explicit(("b",), nm("Bool"), None),),
                nm("Bool"),
                ClausesBody(
                    (
                        Clause((PApp("true", ()),), nm("false")),
                        Clause((PApp("false", ()),), nm("true")),
                    )
                ),
            ),
        )
    )
    assert parse(
        "f (a b : Bool) : Bool\n"
        "  | true, _ := a\n"
        "  | _, y := y"
    ) == Parsed(
        (
            Define(
                "f",
                (Explicit(("a", "b"), nm("Bool"), None),),
                nm("Bool"),
                ClausesBody(
                    (
                        Clause((PApp("true", ()), PWild()), nm("a")),
                        Clause((PWild(), PApp("y", ())), nm("y")),
                    )
                ),
            ),
        )
    )
    assert isinstance(
        parse("f (b : Bool) : Bool := b\n  | true := false"),
        ParseFailed,
    )


def test_operator_tree():
    assert parse("operator + := addZ7") == Parsed(
        (OperatorAct("+", nm("addZ7")),)
    )
    assert parse("operator and := boolAnd") == Parsed(
        (OperatorAct("and", nm("boolAnd")),)
    )
    assert isinstance(parse("operator == := eqZ7"), ParseFailed)


def test_import_tree():
    assert parse('import "linear_algebra.lth" LinearAlgebra') == Parsed(
        (
            ImportAct(
                "linear_algebra.lth",
                (ImportName("LinearAlgebra", None, None),),
            ),
        )
    )
    assert parse(
        'import "la_numpy.lut" Numpy : LinearAlgebra as LA Helpers'
    ) == Parsed(
        (
            ImportAct(
                "la_numpy.lut",
                (
                    ImportName("Numpy", "LinearAlgebra", "LA"),
                    ImportName("Helpers", None, None),
                ),
            ),
        )
    )
    assert isinstance(parse('import "x.lut"'), ParseFailed)


def test_datum_tree():
    assert parse("test f") == Parsed(
        (Datum(App(nm("test"), nm("f"))),)
    )
    assert parse("eval A t") == Parsed(
        (Datum(App(App(nm("eval"), nm("A")), nm("t"))),)
    )
    assert isinstance(parse("x <- 1"), ParseFailed)


def test_literal_tree():
    assert parse("x := 3") == defx(numeral(3))
    assert parse("x := 3.5") == defx(Literal(FloatLit(3.5)))
    assert parse('x := "a"') == defx(Literal(StringLit("a")))


def test_pi_tree():
    assert parse("x := (a b : Int) -> Int") == defx(
        Pi(("a", "b"), nm("Int"), nm("Int"))
    )


def test_sigma_named_tree():
    assert parse("x := (a : A) * (b : B)") == defx(
        SigmaNamed("a", nm("A"), "b", nm("B"))
    )
    assert parse("x := (a : A) + (b : B)") == defx(
        SumNamed("a", nm("A"), "b", nm("B"))
    )


def test_record_tree():
    assert parse("x := { a : Int }") == defx(
        Record((Field(("a",), nm("Int")),), None)
    )
    assert parse("x := { a b : Int, c : Float64 }") == defx(
        Record(
            (
                Field(("a", "b"), nm("Int")),
                Field(("c",), nm("Float64")),
            ),
            None,
        )
    )
    assert parse("x := { a : Int, b : Int | a < b }") == defx(
        Record(
            (
                Field(("a",), nm("Int")),
                Field(("b",), nm("Int")),
            ),
            Binop("<", nm("a"), nm("b")),
        )
    )


def test_subtype_tree():
    assert parse("x := { a : Int | 0 <= a }") == defx(
        Subtype(
            PApp("a", ()),
            nm("Int"),
            Binop("<=", numeral(0), nm("a")),
        )
    )
    assert parse("x := { a b : Int | a < b }") == defx(
        Record(
            (Field(("a", "b"), nm("Int")),),
            Binop("<", nm("a"), nm("b")),
        )
    )
    assert parse("x := { (p, q) : P | p < q }") == defx(
        Subtype(
            PTuple((PApp("p", ()), PApp("q", ()))),
            nm("P"),
            Binop("<", nm("p"), nm("q")),
        )
    )
    assert parse("x := { _ : T | p }") == defx(
        Subtype(PWild(), nm("T"), nm("p"))
    )


def test_block_or_record_value():
    assert parse("x := { a := 1 ; a }") == defx(
        Block((Bind("a", numeral(1)),), nm("a"))
    )
    assert parse("x := { a := 1 }") == defx(
        RecordValue((("a", numeral(1)),))
    )
    assert parse("x := { a <- 1, a <- a + 1, a }") == defx(
        Block(
            (
                Rebind("a", numeral(1)),
                Rebind("a", Binop("+", nm("a"), numeral(1))),
            ),
            nm("a"),
        )
    )


def test_tuple_tree():
    assert parse("x := (a, b, c)") == defx(
        Tuple((nm("a"), nm("b"), nm("c")))
    )


def test_list_tree():
    assert parse("x := [1, 2]") == defx(
        List((numeral(1), numeral(2)))
    )
    assert parse("x := []") == defx(List(()))


def test_lambda_tree():
    assert parse("x := \\ y (z : Int) { w := y ; z }") == defx(
        Lambda(
            (
                PlainParam("y"),
                TypedParam(("z",), nm("Int")),
            ),
            (Bind("w", nm("y")),),
            nm("z"),
        )
    )
    assert parse("x := \\ (p, q) { p }") == defx(
        Lambda(
            (ShapeParam((PApp("p", ()), PApp("q", ()))),),
            (),
            nm("p"),
        )
    )
    assert parse("x := \\ (a b : A) { a }") == defx(
        Lambda(
            (TypedParam(("a", "b"), nm("A")),),
            (),
            nm("a"),
        )
    )
    assert isinstance(parse("x := \\ (y) { y }"), ParseFailed)


def test_pattern_tree():
    assert parse(
        "x := match m { "
        "just y -> y ; _ -> 0 ; 1 -> 2 ; "
        "(a, b) -> a ; cons _ rest -> rest }"
    ) == defx(
        MatchOf(
            nm("m"),
            (
                (PApp("just", (PApp("y", ()),)), nm("y")),
                (PWild(), numeral(0)),
                (PLit(IntLit(1)), numeral(2)),
                (PTuple((PApp("a", ()), PApp("b", ()))), nm("a")),
                (
                    PApp("cons", (PWild(), PApp("rest", ()))),
                    nm("rest"),
                ),
            ),
        )
    )
    assert parse("x := match m { (y) -> y }") == defx(
        MatchOf(nm("m"), ((PApp("y", ()), nm("y")),))
    )
    assert parse("x := match e { }") == defx(
        MatchOf(nm("e"), ())
    )


def test_scrutinee_tree():
    assert parse("x := match g.lex s { a -> b }") == defx(
        MatchOf(App(nm("g.lex"), nm("s")), ((PApp("a", ()), nm("b")),))
    )
    assert parse("x := match f { p -> q } { r -> s }") == defx(
        App(MatchOf(nm("f"), ((PApp("p", ()), nm("q")),)),
            Block((), Binop("->", nm("r"), nm("s"))))
    )
    assert parse("x := match (f { a := 1 ; a }) { r -> s }") == defx(
        MatchOf(App(nm("f"), Block((Bind("a", numeral(1)),), nm("a"))),
                ((PApp("r", ()), nm("s")),))
    )
    assert isinstance(parse("x := match f { a := 1 ; a } { r -> s }"), ParseFailed)


def test_named_arg_tree():
    assert parse("x := f (tol <- 1)") == defx(
        App(nm("f"), NamedArg("tol", numeral(1)))
    )


def test_if_tree():
    assert parse("x := if c then a") == defx(
        IfThen(nm("c"), nm("a"), None)
    )
    assert parse("x := if c then a else b") == defx(
        IfThen(nm("c"), nm("a"), nm("b"))
    )


def test_projection_tree():
    assert parse("x := (f y).z") == defx(
        Proj(App(nm("f"), nm("y")), "z")
    )
    assert parse("x := m.f") == defx(nm("m.f"))


def test_quote_tree():
    assert parse("x := quote { a + b }") == defx(
        Quoted(Binop("+", nm("a"), nm("b")))
    )


def test_universe_world_amp():
    assert parse("x := U -> W") == defx(
        Binop("->", Universe(), World())
    )
    assert parse("x := P & Q") == defx(
        Binop("&", nm("P"), nm("Q"))
    )


def test_negation_tree():
    assert parse("x := -1") == defx(Neg(numeral(1)))


def test_broken_text_fails():
    assert isinstance(parse("x := )"), ParseFailed)


def test_three_files_parse():
    for p in FILES:
        assert isinstance(parse(p.read_text(encoding="utf-8")), Parsed), p
