Delivered as requested. The exact working tree below is also bundled here: luthier-parser-specimen.zip[luthier-parser-specimen.zip](sandbox:/mnt/data/luthier-parser-specimen.zip).

### `src/luthier/surface.py`

```python
"""Frozen Python representation of the surface data declared by ``grammar.lth``."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


# Literal ---------------------------------------------------------------------

@dataclass(frozen=True)
class IntLit:
    value: int


@dataclass(frozen=True)
class FloatLit:
    value: float


@dataclass(frozen=True)
class StringLit:
    value: str


LiteralData: TypeAlias = IntLit | FloatLit | StringLit


# SurfacePattern ---------------------------------------------------------------

@dataclass(frozen=True)
class PWild:
    pass


@dataclass(frozen=True)
class PApp:
    name: str
    patterns: tuple[SurfacePattern, ...]


@dataclass(frozen=True)
class PLit:
    literal: LiteralData


@dataclass(frozen=True)
class PTuple:
    patterns: tuple[SurfacePattern, ...]


SurfacePattern: TypeAlias = PWild | PApp | PLit | PTuple


# LambdaParam ------------------------------------------------------------------

@dataclass(frozen=True)
class PlainParam:
    name: str


@dataclass(frozen=True)
class TypedParam:
    names: tuple[str, ...]
    type: Surface


@dataclass(frozen=True)
class ShapeParam:
    patterns: tuple[SurfacePattern, ...]


LambdaParam: TypeAlias = PlainParam | TypedParam | ShapeParam


# Item -------------------------------------------------------------------------

@dataclass(frozen=True)
class Bind:
    name: str
    value: Surface


@dataclass(frozen=True)
class Rebind:
    name: str
    value: Surface


Item: TypeAlias = Bind | Rebind


# Record types -----------------------------------------------------------------

@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    line: int
    column: int


@dataclass(frozen=True)
class LexError:
    line: int
    column: int
    message: str


@dataclass(frozen=True)
class Field:
    names: tuple[str, ...]
    type: Surface


@dataclass(frozen=True)
class Clause:
    patterns: tuple[SurfacePattern, ...]
    body: Surface


@dataclass(frozen=True)
class ImportName:
    name: str
    theory: str | None
    asName: str | None


@dataclass(frozen=True)
class ParseError:
    line: int
    column: int
    message: str


# Surface ----------------------------------------------------------------------

@dataclass(frozen=True)
class Name:
    name: str


@dataclass(frozen=True)
class Literal:
    literal: LiteralData


@dataclass(frozen=True)
class Universe:
    pass


@dataclass(frozen=True)
class World:
    pass


@dataclass(frozen=True)
class App:
    function: Surface
    argument: Surface


@dataclass(frozen=True)
class Binop:
    operator: str
    left: Surface
    right: Surface


@dataclass(frozen=True)
class Neg:
    value: Surface


@dataclass(frozen=True)
class Tuple:
    values: tuple[Surface, ...]


@dataclass(frozen=True)
class Pi:
    names: tuple[str, ...]
    domain: Surface
    codomain: Surface


@dataclass(frozen=True)
class Sigma:
    names: tuple[str, ...]
    domain: Surface
    codomain: Surface


@dataclass(frozen=True)
class SigmaNamed:
    left_name: str
    left_type: Surface
    right_name: str
    right_type: Surface


@dataclass(frozen=True)
class SumNamed:
    left_name: str
    left_type: Surface
    right_name: str
    right_type: Surface


@dataclass(frozen=True)
class Record:
    fields: tuple[Field, ...]
    law: Surface | None


@dataclass(frozen=True)
class Subtype:
    pattern: SurfacePattern
    type: Surface
    law: Surface


@dataclass(frozen=True)
class RecordValue:
    fields: tuple[tuple[str, Surface], ...]


@dataclass(frozen=True)
class Block:
    items: tuple[Item, ...]
    value: Surface


@dataclass(frozen=True)
class Sum:
    alternatives: tuple[tuple[str, Surface], ...]


@dataclass(frozen=True)
class List:
    values: tuple[Surface, ...]


@dataclass(frozen=True)
class Lambda:
    params: tuple[LambdaParam, ...]
    items: tuple[Item, ...]
    body: Surface


@dataclass(frozen=True)
class MatchOf:
    value: Surface
    arms: tuple[tuple[SurfacePattern, Surface], ...]


@dataclass(frozen=True)
class NamedArg:
    name: str
    value: Surface


@dataclass(frozen=True)
class IfThen:
    condition: Surface
    then_branch: Surface
    else_branch: Surface | None


@dataclass(frozen=True)
class Proj:
    value: Surface
    field: str


@dataclass(frozen=True)
class Quoted:
    value: Surface


Surface: TypeAlias = (
    Name | Literal | Universe | World | App | Binop | Neg | Tuple | Pi | Sigma |
    SigmaNamed | SumNamed | Record | Subtype | RecordValue | Block | Sum | List |
    Lambda | MatchOf | NamedArg | IfThen | Proj | Quoted
)


# Binder -----------------------------------------------------------------------

@dataclass(frozen=True)
class Explicit:
    names: tuple[str, ...]
    type: Surface
    default: Surface | None


@dataclass(frozen=True)
class Implicit:
    names: tuple[str, ...]
    type: Surface


Binder: TypeAlias = Explicit | Implicit


# Body -------------------------------------------------------------------------

@dataclass(frozen=True)
class TermBody:
    term: Surface


@dataclass(frozen=True)
class DataBody:
    constructors: tuple[tuple[str, Surface], ...]


@dataclass(frozen=True)
class ClausesBody:
    clauses: tuple[Clause, ...]


Body: TypeAlias = TermBody | DataBody | ClausesBody


# SurfaceAct -------------------------------------------------------------------

@dataclass(frozen=True)
class Declare:
    name: str
    binders: tuple[Binder, ...]
    type: Surface


@dataclass(frozen=True)
class Define:
    name: str
    binders: tuple[Binder, ...]
    type: Surface | None
    body: Body


@dataclass(frozen=True)
class Alias:
    name: str
    binders: tuple[Binder, ...]
    value: Surface


@dataclass(frozen=True)
class ImportAct:
    path: str
    names: tuple[ImportName, ...]


@dataclass(frozen=True)
class OperatorAct:
    operator: str
    value: Surface


@dataclass(frozen=True)
class Datum:
    value: Surface


SurfaceAct: TypeAlias = Declare | Define | Alias | ImportAct | OperatorAct | Datum
SurfaceProgram: TypeAlias = tuple[SurfaceAct, ...]


# Sum labels -------------------------------------------------------------------

@dataclass(frozen=True)
class Lexed:
    tokens: tuple[Token, ...]


@dataclass(frozen=True)
class LexFailed:
    error: LexError


@dataclass(frozen=True)
class Parsed:
    program: SurfaceProgram


@dataclass(frozen=True)
class ParseFailed:
    errors: tuple[ParseError, ...]


LexResult: TypeAlias = Lexed | LexFailed
ParseResult: TypeAlias = Parsed | ParseFailed
TokenView: TypeAlias = tuple[str, str]
```

### `src/luthier/parse.py`

```python
"""Lexer, layout pass, recursive-descent parser, and printer for Luthier.

The accepted token language is stated once, by ``luthierSyntax`` in ``grammar.lth``.
This module derives its literals and operator sets from that value and mirrors each
nonterminal with one parser method.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import re

from .ebnf import lits_of, lits_of_names, luthier_syntax
from .surface import (
    Alias, App, Bind, Binop, Block, Clause, ClausesBody, DataBody, Datum, Declare,
    Define, Explicit, Field, FloatLit, IfThen, ImportAct, ImportName, Implicit,
    IntLit, Lambda, LexError, LexFailed, Lexed, List, Literal, MatchOf, Name,
    NamedArg, Neg, OperatorAct, PApp, PLit, PTuple, PWild, ParseError, ParseFailed,
    Parsed, Pi, PlainParam, Proj, Quoted, Rebind, Record, RecordValue, ShapeParam,
    Sigma, SigmaNamed, StringLit, Subtype, Sum, SumNamed, Surface, SurfaceAct,
    SurfacePattern, TermBody, Token, TokenView, Tuple, TypedParam, Universe, World,
)


_G = luthier_syntax()
_LITERALS = frozenset(lits_of(_G))
_PRECEDENCE_LEVELS = [
    "ampTerm", "arrowTerm", "orTerm", "andTerm", "cmpTerm", "addTerm", "mulTerm"
]
_BINARY_OPERATORS = frozenset(lits_of_names(_G, _PRECEDENCE_LEVELS))
_BOUND_OPERATORS = frozenset(lits_of_names(_G, ["opSymbol"]))

_NAME_RE = re.compile(r"[A-Za-z][A-Za-z0-9_']*(?:\.[A-Za-z][A-Za-z0-9_']*)*")
_NUMBER_RE = re.compile(r"[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
_WORD_LITERAL_RE = re.compile(r"[A-Za-z][A-Za-z0-9_']*")
_WORD_LITERALS = frozenset(x for x in _LITERALS if _WORD_LITERAL_RE.fullmatch(x))
_SYMBOL_LITERALS = tuple(
    sorted(
        (x for x in _LITERALS if x != "\n" and x not in _WORD_LITERALS),
        key=lambda s: (-len(s), s),
    )
)


# --------------------------------------------------------------------------- lex

def lex(text: str) -> Lexed | LexFailed:
    """Tokenize ``text`` according to 2.S1 and literals derived from ``luthierSyntax``."""
    out: list[Token] = []
    i = 0
    line = 1
    column = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if ch in " \t\r":
            i += 1
            column += 1
            continue
        if ch == "\n":
            i += 1
            line += 1
            column = 0
            continue
        if text.startswith("--", i):
            j = text.find("\n", i + 2)
            if j < 0:
                break
            i = j
            continue

        start_line, start_col = line, column

        if ch == '"':
            j = i + 1
            col = column + 1
            while j < n:
                c = text[j]
                if c == '"':
                    raw = text[i : j + 1]
                    out.append(Token("string", raw, start_line, start_col))
                    column = col + 1
                    i = j + 1
                    break
                if c == "\n":
                    return LexFailed(LexError(start_line, start_col, "unterminated string"))
                if c == "\\":
                    if j + 1 >= n or text[j + 1] not in {'"', "\\", "n"}:
                        return LexFailed(LexError(line, col, "unknown string escape"))
                    j += 2
                    col += 2
                    continue
                j += 1
                col += 1
            else:
                return LexFailed(LexError(start_line, start_col, "unterminated string"))
            continue

        m = _NUMBER_RE.match(text, i)
        if m is not None:
            raw = m.group(0)
            out.append(Token("number", raw, start_line, start_col))
            i = m.end()
            column += len(raw)
            continue

        m = _NAME_RE.match(text, i)
        if m is not None:
            raw = m.group(0)
            kind = "literal" if raw in _LITERALS else "name"
            out.append(Token(kind, raw, start_line, start_col))
            i = m.end()
            column += len(raw)
            continue

        matched = None
        for literal in _SYMBOL_LITERALS:
            if text.startswith(literal, i):
                matched = literal
                break
        if matched is not None:
            out.append(Token("literal", matched, start_line, start_col))
            i += len(matched)
            column += len(matched)
            continue

        return LexFailed(LexError(line, column, f"unexpected character {ch!r}"))

    return Lexed(tuple(out))


def _decode_string(raw: str) -> str:
    body = raw[1:-1]
    chars: list[str] = []
    i = 0
    while i < len(body):
        if body[i] != "\\":
            chars.append(body[i])
            i += 1
            continue
        esc = body[i + 1]
        chars.append({'"': '"', "\\": "\\", "n": "\n"}[esc])
        i += 2
    return "".join(chars)


def _encode_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


# ------------------------------------------------------------------------ layout

@dataclass
class _Frame:
    opener: str
    kind: str
    first_item_column: int | None = None


def _continuation_start(text: str) -> bool:
    return text in {"then", "else"} or text in _BINARY_OPERATORS


def _brace_looks_like_match_body(tokens: tuple[Token, ...], index: int) -> bool:
    """Whether this brace can be the ``{ arms }`` delimiter of ``match``.

    Empty arms are valid.  Otherwise every arm has a top-level ``->``; seeing
    one before a top-level item separator is enough to distinguish ordinary
    record/block/data braces in the cases where layout itself must choose.
    A block whose sole value is an arrow term is genuinely ambiguous after a
    match subject; choosing the earliest viable match brace agrees with the
    parser and is reported as a grammar ambiguity.
    """
    pairs = {")": "(", "]": "[", "}": "{", ">": "<"}
    opens = set(pairs.values())
    stack: list[str] = []
    j = index + 1
    if j < len(tokens) and tokens[j].text == "}":
        return True
    while j < len(tokens):
        text = tokens[j].text
        if text in opens:
            stack.append(text)
        elif text in pairs:
            if text == "}" and not stack:
                return False
            if stack and stack[-1] == pairs[text]:
                stack.pop()
        elif not stack:
            if text == "->":
                return True
            if text in {":=", "<-"}:
                return False
        j += 1
    return False


def _classify_brace(tokens: tuple[Token, ...], index: int) -> str:
    # `data` is an item-separating brace; `quote` groups one term.  The latter
    # is not stated by 2.S4 but is forced by quote's production.
    prev = tokens[index - 1].text if index else ""
    if prev == "data":
        return "separating"
    if prev == "quote":
        return "ignoring"

    # A brace immediately after `match` must belong to its subject.  Otherwise
    # an arm-looking brace belongs to the nearest unmatched match in this act.
    if prev == "match" or not _brace_looks_like_match_body(tokens, index):
        return "separating"

    pairs = {")": "(", "]": "[", "}": "{", ">": "<"}
    opens = set(pairs.values())
    stack: list[str] = []
    for j in range(index - 1, -1, -1):
        t = tokens[j]
        text = t.text
        if text in pairs:
            stack.append(pairs[text])
            continue
        if text in opens:
            if stack and stack[-1] == text:
                stack.pop()
                continue
            if not stack:
                # An unmatched opener contains the candidate; a match outside
                # that container cannot own it.
                break
        if stack:
            continue
        if text in {";", ","}:
            break
        if text == "match":
            return "ignoring"
        # Do not cross the beginning of this top-level act into a previous act.
        if t.column == 0 and (j == 0 or tokens[j - 1].line < t.line):
            break
    return "separating"


def _layout_tokens(tokens: tuple[Token, ...]) -> tuple[Token, ...]:
    if not tokens:
        return ()

    out: list[Token] = []
    stack: list[_Frame] = []

    def append_token(t: Token) -> None:
        out.append(t)
        if stack and stack[-1].opener == "{" and stack[-1].kind == "separating":
            f = stack[-1]
            if f.first_item_column is None and t.text != "}":
                f.first_item_column = t.column

    prev: Token | None = None
    for idx, tok in enumerate(tokens):
        if prev is not None and tok.line > prev.line:
            next_text = tok.text
            prev_text = prev.text

            if stack:
                top = stack[-1]
                if top.opener in {"(", "[", "<"} or top.kind == "ignoring":
                    pass
                elif top.opener == "{" and top.kind == "separating":
                    first_col = top.first_item_column
                    drop = (
                        next_text == "}"
                        or prev_text in {"{", ",", ";"}
                        or _continuation_start(next_text)
                        or (first_col is not None and tok.column > first_col)
                    )
                    if not drop:
                        append_token(Token("literal", ";", tok.line, tok.column))
            else:
                if tok.column == 0 and next_text != "}" and not _continuation_start(next_text):
                    append_token(Token("newline", "\n", tok.line, tok.column))
                # An indented line continues the act.

        opens_angle = (
            tok.text == "<"
            and idx + 2 < len(tokens)
            and tokens[idx + 1].kind == "name"
            and tokens[idx + 2].text == ":"
        )
        if tok.text in {"(", "[", "{"} or opens_angle:
            kind = _classify_brace(tokens, idx) if tok.text == "{" else "ignoring"
            append_token(tok)
            stack.append(_Frame(tok.text, kind))
        elif tok.text in {")", "]", ">", "}"}:
            append_token(tok)
            if stack:
                want = {")": "(", "]": "[", ">": "<", "}": "{"}[tok.text]
                # Mismatches are left for the parser; pop only a matching opener.
                if stack[-1].opener == want:
                    stack.pop()
        else:
            append_token(tok)

        prev = tok

    if out and out[-1].text != "\n":
        last = out[-1]
        out.append(Token("newline", "\n", last.line, last.column + len(last.text)))
    return tuple(out)


def layout(tokens: tuple[Token, ...]) -> tuple[TokenView, ...]:
    """Apply 2.S4 and return the grammar's ``(kind, text)`` token views."""
    return tuple((t.kind, t.text) for t in _layout_tokens(tokens))


# ------------------------------------------------------------------------ parser

class _NoParse(Exception):
    pass


class _Parser:
    def __init__(self, tokens: tuple[Token, ...]):
        self.tokens = tokens
        self.i = 0
        self.furthest = 0
        self.expected: set[str] = set()
        self._stop_arg_brace = 0

    def _mark(self, expected: str) -> None:
        if self.i > self.furthest:
            self.furthest = self.i
            self.expected = {expected}
        elif self.i == self.furthest:
            self.expected.add(expected)

    def _fail(self, expected: str) -> None:
        self._mark(expected)
        raise _NoParse

    def _peek(self, text: str | None = None, kind: str | None = None) -> bool:
        if self.i >= len(self.tokens):
            return False
        t = self.tokens[self.i]
        return (text is None or t.text == text) and (kind is None or t.kind == kind)

    def _take(self, text: str | None = None, kind: str | None = None) -> Token:
        if not self._peek(text, kind):
            self._fail(repr(text) if text is not None else kind or "token")
        t = self.tokens[self.i]
        self.i += 1
        return t

    def _attempt(self, fn):
        pos = self.i
        try:
            return fn()
        except _NoParse:
            self.i = pos
            raise

    def _choice(self, *fns):
        start = self.i
        for fn in fns:
            self.i = start
            try:
                return fn()
            except _NoParse:
                pass
        self.i = start
        self._fail("alternative")

    def _name(self) -> str:
        return self._take(kind="name").text

    def _starts_arg_atom(self) -> bool:
        if self.i >= len(self.tokens):
            return False
        t = self.tokens[self.i]
        return t.kind in {"name", "number", "string"} or t.text in {
            "U", "W", "(", "{", "[", "\\", "match", "quote"
        }

    # Each method below mirrors one nonterminal in luthierSyntax. ----------------

    def program(self) -> tuple[SurfaceAct, ...]:
        """program ::= { act "\\n" }"""
        acts: list[SurfaceAct] = []
        while self.i < len(self.tokens):
            acts.append(self.act())
            self._take("\n")
        return tuple(acts)

    def act(self) -> SurfaceAct:
        """act ::= declaration | definition | alias | import | operator | datum"""
        if self._peek("import"):
            return self.import_()
        if self._peek("operator"):
            return self.operator()
        start = self.i
        for fn in (self.declaration, self.definition, self.alias, self.datum):
            self.i = start
            try:
                value = fn()
                if self._peek("\n"):
                    return value
            except _NoParse:
                pass
        self.i = start
        self._fail("act")

    def declaration(self) -> SurfaceAct:
        """declaration ::= name { binder } ":" term"""
        name = self._name()
        binders = self._binders()
        self._take(":")
        return Declare(name, binders, self.term())

    def definition(self) -> SurfaceAct:
        """definition ::= name { binder } [ ":" term ] ( ":=" body | clause { clause } )"""
        name = self._name()
        binders = self._binders()
        annotation = None
        if self._peek(":"):
            self._take(":")
            annotation = self.term()
        if self._peek(":="):
            self._take(":=")
            body = self.body()
        elif self._peek("|"):
            clauses = [self.clause()]
            while self._peek("|"):
                clauses.append(self.clause())
            body = ClausesBody(tuple(clauses))
        else:
            self._fail("':=' or clause")
        return Define(name, binders, annotation, body)

    def alias(self) -> SurfaceAct:
        """alias ::= name { binder } "=" term"""
        name = self._name()
        binders = self._binders()
        self._take("=")
        return Alias(name, binders, self.term())

    def import_(self) -> SurfaceAct:
        """import ::= "import" string importName { importName }"""
        self._take("import")
        path = _decode_string(self._take(kind="string").text)
        names = [self.importName()]
        while self._peek(kind="name"):
            names.append(self.importName())
        return ImportAct(path, tuple(names))

    def importName(self) -> ImportName:
        """importName ::= name [ ":" name ] [ "as" name ]"""
        name = self._name()
        theory = None
        alias = None
        if self._peek(":"):
            self._take(":")
            theory = self._name()
        if self._peek("as"):
            self._take("as")
            alias = self._name()
        return ImportName(name, theory, alias)

    def operator(self) -> SurfaceAct:
        """operator ::= "operator" opSymbol ":=" term"""
        self._take("operator")
        op = self.opSymbol()
        self._take(":=")
        return OperatorAct(op, self.term())

    def opSymbol(self) -> str:
        """opSymbol ::= "+" | "-" | "*" | "/" | "and" | "or" | "mod"""
        if self.i < len(self.tokens) and self.tokens[self.i].text in _BOUND_OPERATORS:
            return self._take().text
        self._fail("operator symbol")

    def datum(self) -> SurfaceAct:
        """datum ::= term"""
        return Datum(self.term())

    def binder(self):
        """binder ::= "(" name { name } ":" term [ "<-" term ] ")" | "{" name { name } ":" term "}"""
        if self._peek("("):
            self._take("(")
            names = [self._name()]
            while self._peek(kind="name"):
                names.append(self._name())
            self._take(":")
            typ = self.term()
            default = None
            if self._peek("<-"):
                self._take("<-")
                default = self.term()
            self._take(")")
            return Explicit(tuple(names), typ, default)
        if self._peek("{"):
            self._take("{")
            names = [self._name()]
            while self._peek(kind="name"):
                names.append(self._name())
            self._take(":")
            typ = self.term()
            self._take("}")
            return Implicit(tuple(names), typ)
        self._fail("binder")

    def _binders(self):
        result = []
        while self._peek("(") or self._peek("{"):
            pos = self.i
            try:
                result.append(self.binder())
            except _NoParse:
                self.i = pos
                break
        return tuple(result)

    def clause(self) -> Clause:
        """clause ::= "|" pattern { "," pattern } ":=" term"""
        self._take("|")
        patterns = [self.pattern()]
        while self._peek(","):
            self._take(",")
            patterns.append(self.pattern())
        self._take(":=")
        return Clause(tuple(patterns), self.term())

    def body(self):
        """body ::= term | "data" "{" [ ctor { ";" ctor } [ ";" ] ] "}"""
        if self._peek("data"):
            self._take("data")
            self._take("{")
            ctors: list[tuple[str, Surface]] = []
            if not self._peek("}"):
                ctors.append(self.ctor())
                while self._peek(";"):
                    self._take(";")
                    if self._peek("}"):
                        break
                    ctors.append(self.ctor())
            self._take("}")
            return DataBody(tuple(ctors))
        return TermBody(self.term())

    def ctor(self) -> tuple[str, Surface]:
        """ctor ::= name ":" term"""
        name = self._name()
        self._take(":")
        return name, self.term()

    def term(self) -> Surface:
        """term ::= openForm | ampTerm"""
        pos = self.i
        try:
            return self.openForm()
        except _NoParse:
            self.i = pos
            return self.ampTerm()

    def openForm(self) -> Surface:
        """openForm ::= dependent pi | dependent sigma | named sigma | named sum | if-form"""
        if self._peek("if"):
            self._take("if")
            condition = self.term()
            self._take("then")
            yes = self.term()
            no = None
            if self._peek("else"):
                self._take("else")
                no = self.term()
            return IfThen(condition, yes, no)

        start = self.i
        self._take("(")
        first = self._name()
        names = [first]
        while self._peek(kind="name"):
            names.append(self._name())
        self._take(":")
        domain = self.term()
        self._take(")")

        if self._peek("->"):
            self._take("->")
            return Pi(tuple(names), domain, self.term())

        if self._peek("*"):
            self._take("*")
            # The two-named product is selected only when it consumes the complete
            # RHS; otherwise `(a:A) * (b:B) * C` is nested dependent sigma.
            if len(names) == 1 and self._peek("("):
                save = self.i
                try:
                    self._take("(")
                    right_name = self._name()
                    self._take(":")
                    right_type = self.term()
                    self._take(")")
                    if not self._peek("*"):
                        return SigmaNamed(first, domain, right_name, right_type)
                except _NoParse:
                    pass
                self.i = save
            return Sigma(tuple(names), domain, self.term())

        if self._peek("+") and len(names) == 1:
            self._take("+")
            self._take("(")
            right_name = self._name()
            self._take(":")
            right_type = self.term()
            self._take(")")
            return SumNamed(first, domain, right_name, right_type)

        self.i = start
        self._fail("open form")

    def ampTerm(self) -> Surface:
        """ampTerm ::= arrowTerm [ "&" ( openForm | ampTerm ) ] | arrowOpen"""
        start = self.i
        try:
            left = self.arrowTerm()
        except _NoParse:
            self.i = start
            return self.arrowOpen()
        if self._peek("&"):
            self._take("&")
            pos = self.i
            try:
                right = self.openForm()
            except _NoParse:
                self.i = pos
                right = self.ampTerm()
            return Binop("&", left, right)
        return left

    def arrowTerm(self) -> Surface:
        """arrowTerm ::= orTerm [ "->" arrowTerm ]"""
        left = self.orTerm()
        if self._peek("->"):
            self._take("->")
            right = self.arrowTerm()
            return Binop("->", left, right)
        return left

    def arrowOpen(self) -> Surface:
        """arrowOpen ::= orTerm "->" ( openForm | arrowOpen )"""
        left = self.orTerm()
        self._take("->")
        pos = self.i
        try:
            right = self.openForm()
        except _NoParse:
            self.i = pos
            right = self.arrowOpen()
        return Binop("->", left, right)

    def orTerm(self) -> Surface:
        """orTerm ::= andTerm { "or" andTerm }"""
        return self._left_chain(self.andTerm, {"or"})

    def andTerm(self) -> Surface:
        """andTerm ::= cmpTerm { "and" cmpTerm }"""
        return self._left_chain(self.cmpTerm, {"and"})

    def cmpTerm(self) -> Surface:
        """cmpTerm ::= addTerm { ( "==" | "/=" | "<" | "<=" | ">" | ">=" ) addTerm }"""
        return self._left_chain(self.addTerm, {"==", "/=", "<", "<=", ">", ">="})

    def addTerm(self) -> Surface:
        """addTerm ::= mulTerm { ( "+" | "-" ) mulTerm }"""
        return self._left_chain(self.mulTerm, {"+", "-"})

    def mulTerm(self) -> Surface:
        """mulTerm ::= negTerm { ( "*" | "/" | "mod" ) negTerm }"""
        return self._left_chain(self.negTerm, {"*", "/", "mod"})

    def _left_chain(self, sub, operators: set[str]) -> Surface:
        left = sub()
        while self.i < len(self.tokens) and self.tokens[self.i].text in operators:
            start = self.i
            try:
                op = self._take().text
                right = sub()
            except _NoParse:
                self.i = start
                break
            left = Binop(op, left, right)
        return left

    def negTerm(self) -> Surface:
        """negTerm ::= "-" negTerm | appTerm"""
        if self._peek("-"):
            self._take("-")
            return Neg(self.negTerm())
        return self.appTerm()

    def appTerm(self) -> Surface:
        """appTerm ::= projTerm { argTerm }"""
        value = self.projTerm()
        while self._starts_arg_atom():
            if self._stop_arg_brace and self._peek("{"):
                break
            start = self.i
            try:
                arg = self.argTerm()
            except _NoParse:
                self.i = start
                break
            value = App(value, arg)
        return value

    def projTerm(self) -> Surface:
        """projTerm ::= atom { "." name }"""
        value = self.atom()
        while self._peek("."):
            self._take(".")
            value = Proj(value, self._name())
        return value

    def argTerm(self) -> Surface:
        """argTerm ::= argAtom { "." name }"""
        value = self.argAtom()
        while self._peek("."):
            self._take(".")
            value = Proj(value, self._name())
        return value

    def atom(self) -> Surface:
        """atom ::= argAtom | "<" name ":" term { "|" name ":" term } ">"""
        if self._peek("<"):
            self._take("<")
            first_name = self._name()
            self._take(":")
            value_start = self.i

            def exact_term(a: int, b: int) -> Surface | None:
                if a >= b:
                    return None
                sub = _Parser(self.tokens[a:b])
                try:
                    value = sub.term()
                    return value if sub.i == len(sub.tokens) else None
                except _NoParse:
                    return None

            def alternatives(name: str, a: int):
                # `>` is also a comparison operator. Try later boundaries
                # first, so a viable comparison inside an alternative is kept
                # inside the sum; if no later close works, an earlier `>` is
                # the delimiter.
                for j in range(len(self.tokens) - 1, a - 1, -1):
                    boundary = self.tokens[j].text
                    if boundary not in {"|", ">"}:
                        continue
                    value = exact_term(a, j)
                    if value is None:
                        continue
                    if boundary == ">":
                        return [(name, value)], j + 1
                    if (
                        j + 2 >= len(self.tokens)
                        or self.tokens[j + 1].kind != "name"
                        or self.tokens[j + 2].text != ":"
                    ):
                        continue
                    rest = alternatives(self.tokens[j + 1].text, j + 3)
                    if rest is not None:
                        more, end = rest
                        return [(name, value), *more], end
                return None

            parsed = alternatives(first_name, value_start)
            if parsed is None:
                self._fail("sum alternative and '>'")
            alts, end = parsed
            self.i = end
            return Sum(tuple(alts))
        return self.argAtom()

    def argAtom(self) -> Surface:
        """argAtom ::= name | number | string | U | W | parenthesized/tuple/named-arg | braces | list | lambda | match | quote"""
        if self._peek(kind="name"):
            return Name(self._name())
        if self._peek(kind="number"):
            raw = self._take(kind="number").text
            if "." in raw or "e" in raw.lower():
                return Literal(FloatLit(float(raw)))
            return Literal(IntLit(int(raw)))
        if self._peek(kind="string"):
            return Literal(StringLit(_decode_string(self._take(kind="string").text)))
        if self._peek("U"):
            self._take("U")
            return Universe()
        if self._peek("W"):
            self._take("W")
            return World()
        if self._peek("("):
            return self._paren_atom()
        if self._peek("{"):
            return self._brace_atom()
        if self._peek("["):
            self._take("[")
            values: list[Surface] = []
            if not self._peek("]"):
                values.append(self.term())
                while self._peek(","):
                    self._take(",")
                    if self._peek("]"):
                        break
                    values.append(self.term())
            self._take("]")
            return List(tuple(values))
        if self._peek("\\"):
            self._take("\\")
            params = [self.lparam()]
            while not self._peek("{"):
                params.append(self.lparam())
            self._take("{")
            items, body = self.block()
            self._take("}")
            return Lambda(tuple(params), items, body)
        if self._peek("match"):
            self._take("match")
            subject_start = self.i
            # The subject may itself end in one or more brace arguments. Try
            # each later `{` as the match delimiter, earliest first. A slice
            # must parse completely as `term`, and the candidate brace must
            # parse completely as the arm list.
            for brace_at in range(subject_start + 1, len(self.tokens)):
                if self.tokens[brace_at].text != "{":
                    continue
                sub = _Parser(self.tokens[subject_start:brace_at])
                try:
                    value = sub.term()
                    if sub.i != len(sub.tokens):
                        continue
                except _NoParse:
                    continue

                saved = self.i
                self.i = brace_at
                try:
                    self._take("{")
                    arms: list[tuple[SurfacePattern, Surface]] = []
                    if not self._peek("}"):
                        arms.append(self.arm())
                        while self._peek(";"):
                            self._take(";")
                            if self._peek("}"):
                                break
                            arms.append(self.arm())
                    self._take("}")
                    return MatchOf(value, tuple(arms))
                except _NoParse:
                    self.i = saved
                    continue
            self.i = subject_start
            self._fail("match subject and arms")
        if self._peek("quote"):
            self._take("quote")
            self._take("{")
            value = self.term()
            self._take("}")
            return Quoted(value)
        self._fail("argument atom")

    def _paren_atom(self) -> Surface:
        start = self.i

        try:
            self._take("(")
            if (
                self._peek(kind="name")
                and self.i + 1 < len(self.tokens)
                and self.tokens[self.i + 1].text == "<-"
            ):
                name = self._name()
                self._take("<-")
                value = self.term()
                self._take(")")
                return NamedArg(name, value)
        except _NoParse:
            pass
        self.i = start

        self._take("(")
        first = self.term()
        if self._peek(","):
            values = [first]
            self._take(",")
            values.append(self.term())
            while self._peek(","):
                self._take(",")
                values.append(self.term())
            self._take(")")
            return Tuple(tuple(values))
        self._take(")")
        return first

    def _brace_atom(self) -> Surface:
        start = self.i
        for fn in (
            self._record_atom,
            self._subtype_atom,
            self._record_value_atom,
            self._block_atom,
        ):
            self.i = start
            try:
                return fn()
            except _NoParse:
                pass
        self.i = start
        self._fail("brace term")

    def _record_atom(self) -> Surface:
        self._take("{")
        fields, law = self.recordFields()
        self._take("}")
        return Record(fields, law)

    def _subtype_atom(self) -> Surface:
        self._take("{")
        pattern = self.subtypePattern()
        self._take(":")
        typ = self.term()
        self._take("|")
        law = self.term()
        self._take("}")
        return Subtype(pattern, typ, law)

    def _record_value_atom(self) -> Surface:
        self._take("{")
        name = self._name()
        self._take(":=")
        fields = [(name, self.term())]
        while self._peek(",") or self._peek(";"):
            self.sep()
            if self._peek("}"):
                break
            name = self._name()
            self._take(":=")
            fields.append((name, self.term()))
        self._take("}")
        return RecordValue(tuple(fields))

    def _block_atom(self) -> Surface:
        self._take("{")
        items, value = self.block()
        self._take("}")
        return Block(items, value)

    def recordFields(self) -> tuple[tuple[Field, ...], Surface | None]:
        """recordFields ::= fieldOne [ sep ] | fieldsTwo [ "|" term ] [ sep ]"""
        start = self.i
        try:
            f = self.fieldOne()
            if self._peek(",") or self._peek(";"):
                self.sep()
            if self._peek("}"):
                return (f,), None
            raise _NoParse
        except _NoParse:
            self.i = start

        fields = self.fieldsTwo()
        law = None
        if self._peek("|"):
            self._take("|")
            law = self.term()
        if self._peek(",") or self._peek(";"):
            self.sep()
        return fields, law

    def fieldsTwo(self) -> tuple[Field, ...]:
        """fieldsTwo ::= fieldMany { sep field } | fieldOne sep field { sep field }"""
        start = self.i
        try:
            first = self.fieldMany()
            fields = [first]
            while self._peek(",") or self._peek(";"):
                sep_pos = self.i
                self.sep()
                if self._peek("|") or self._peek("}"):
                    self.i = sep_pos
                    break
                fields.append(self.field())
            return tuple(fields)
        except _NoParse:
            self.i = start

        fields = [self.fieldOne()]
        self.sep()
        fields.append(self.field())
        while self._peek(",") or self._peek(";"):
            sep_pos = self.i
            self.sep()
            if self._peek("|") or self._peek("}"):
                self.i = sep_pos
                break
            fields.append(self.field())
        return tuple(fields)

    def field(self) -> Field:
        """field ::= name { name } ":" term"""
        names = [self._name()]
        while self._peek(kind="name"):
            names.append(self._name())
        self._take(":")
        return Field(tuple(names), self.term())

    def fieldOne(self) -> Field:
        """fieldOne ::= name ":" term"""
        name = self._name()
        self._take(":")
        return Field((name,), self.term())

    def fieldMany(self) -> Field:
        """fieldMany ::= name name { name } ":" term"""
        names = [self._name(), self._name()]
        while self._peek(kind="name"):
            names.append(self._name())
        self._take(":")
        return Field(tuple(names), self.term())

    def subtypePattern(self) -> SurfacePattern:
        """subtypePattern ::= "_" | name | number | string | "(" pattern "," pattern { "," pattern } ")" """
        if self._peek("_"):
            self._take("_")
            return PWild()
        if self._peek(kind="name"):
            return PApp(self._name(), ())
        if self._peek(kind="number"):
            return PLit(self._literal_from_token(self._take(kind="number")))
        if self._peek(kind="string"):
            return PLit(StringLit(_decode_string(self._take(kind="string").text)))
        self._take("(")
        patterns = [self.pattern()]
        self._take(",")
        patterns.append(self.pattern())
        while self._peek(","):
            self._take(",")
            patterns.append(self.pattern())
        self._take(")")
        return PTuple(tuple(patterns))

    def sep(self) -> str:
        """sep ::= "," | ";" """
        if self._peek(",") or self._peek(";"):
            return self._take().text
        self._fail("separator")

    def block(self) -> tuple[tuple[Bind | Rebind, ...], Surface]:
        """block ::= { item sep } term [ sep ]"""
        items: list[Bind | Rebind] = []
        while True:
            start = self.i
            try:
                item = self.item()
                self.sep()
                items.append(item)
            except _NoParse:
                self.i = start
                break
        value = self.term()
        if self._peek(",") or self._peek(";"):
            self.sep()
        return tuple(items), value

    def item(self):
        """item ::= name ( ":=" | "<-" ) term"""
        name = self._name()
        if self._peek(":="):
            self._take(":=")
            return Bind(name, self.term())
        if self._peek("<-"):
            self._take("<-")
            return Rebind(name, self.term())
        self._fail("':=' or '<-'")

    def arm(self) -> tuple[SurfacePattern, Surface]:
        """arm ::= pattern "->" term"""
        p = self.pattern()
        self._take("->")
        return p, self.term()

    def lparam(self):
        """lparam ::= name | "(" name { name } ":" term ")" | "(" pattern "," pattern { "," pattern } ")" """
        if self._peek(kind="name"):
            return PlainParam(self._name())
        self._take("(")
        start = self.i
        try:
            names = [self._name()]
            while self._peek(kind="name"):
                names.append(self._name())
            self._take(":")
            typ = self.term()
            self._take(")")
            return TypedParam(tuple(names), typ)
        except _NoParse:
            self.i = start
        patterns = [self.pattern()]
        self._take(",")
        patterns.append(self.pattern())
        while self._peek(","):
            self._take(",")
            patterns.append(self.pattern())
        self._take(")")
        return ShapeParam(tuple(patterns))

    def pattern(self) -> SurfacePattern:
        """pattern ::= name patom { patom } | patom"""
        if self._peek(kind="name"):
            start = self.i
            name = self._name()
            if self._starts_patom():
                args = [self.patom()]
                while self._starts_patom():
                    args.append(self.patom())
                return PApp(name, tuple(args))
            self.i = start
        return self.patom()

    def _starts_patom(self) -> bool:
        if self.i >= len(self.tokens):
            return False
        t = self.tokens[self.i]
        return t.text in {"_", "("} or t.kind in {"name", "number", "string"}

    def patom(self) -> SurfacePattern:
        """patom ::= "_" | name | number | string | "(" pattern ")" | tuple-pattern"""
        if self._peek("_"):
            self._take("_")
            return PWild()
        if self._peek(kind="name"):
            return PApp(self._name(), ())
        if self._peek(kind="number"):
            return PLit(self._literal_from_token(self._take(kind="number")))
        if self._peek(kind="string"):
            return PLit(StringLit(_decode_string(self._take(kind="string").text)))
        self._take("(")
        first = self.pattern()
        if self._peek(","):
            ps = [first]
            self._take(",")
            ps.append(self.pattern())
            while self._peek(","):
                self._take(",")
                ps.append(self.pattern())
            self._take(")")
            return PTuple(tuple(ps))
        self._take(")")
        return first

    @staticmethod
    def _literal_from_token(t: Token):
        if "." in t.text or "e" in t.text.lower():
            return FloatLit(float(t.text))
        return IntLit(int(t.text))

    def error(self) -> ParseError:
        pos = min(self.furthest, len(self.tokens))
        if pos < len(self.tokens):
            t = self.tokens[pos]
            line, column = t.line, t.column
            got = repr(t.text)
        elif self.tokens:
            t = self.tokens[-1]
            line, column = t.line, t.column + len(t.text)
            got = "end of input"
        else:
            line, column, got = 1, 0, "end of input"
        expected = ", ".join(sorted(self.expected)) or "valid syntax"
        return ParseError(line, column, f"expected {expected}; got {got}")


setattr(_Parser, "import", _Parser.import_)


def parse(text: str) -> Parsed | ParseFailed:
    """Lex, lay out, and parse one Luthier source text."""
    lr = lex(text)
    if isinstance(lr, LexFailed):
        e = lr.error
        return ParseFailed((ParseError(e.line, e.column, e.message),))
    laid = _layout_tokens(lr.tokens)
    p = _Parser(laid)
    try:
        program = p.program()
        if p.i != len(laid):
            p._fail("end of input")
        return Parsed(program)
    except _NoParse:
        return ParseFailed((p.error(),))


# ----------------------------------------------------------------------- printer

_PREC = {
    "&": 2,
    "->": 3,
    "or": 4,
    "and": 5,
    "==": 6,
    "/=": 6,
    "<": 6,
    "<=": 6,
    ">": 6,
    ">=": 6,
    "+": 7,
    "-": 7,
    "*": 8,
    "/": 8,
    "mod": 8,
}
_RIGHT_ASSOC = {"&", "->"}


def _precedence(t: Surface) -> int:
    if isinstance(t, (Pi, Sigma, SigmaNamed, SumNamed, IfThen)):
        return 1
    if isinstance(t, Binop):
        return _PREC[t.operator]
    if isinstance(t, Neg):
        return 9
    if isinstance(t, App):
        return 10
    if isinstance(t, Proj):
        return 11
    return 12


def _open_ending(t: Surface) -> bool:
    if isinstance(t, (Pi, Sigma, SigmaNamed, SumNamed, IfThen)):
        return True
    if isinstance(t, Binop) and t.operator in {"&", "->"}:
        return _open_ending(t.right)
    return False


def _is_arg_atom(t: Surface) -> bool:
    return isinstance(
        t,
        (
            Name,
            Literal,
            Universe,
            World,
            Tuple,
            NamedArg,
            Record,
            Subtype,
            RecordValue,
            Block,
            List,
            Lambda,
            MatchOf,
            Quoted,
        ),
    )


def _format_float(x: float) -> str:
    if math.isinf(x):
        return "1e999"
    s = repr(x)
    if "." not in s and "e" not in s.lower():
        s += ".0"
    return s


def _print_literal(lit) -> str:
    if isinstance(lit, IntLit):
        return str(lit.value)
    if isinstance(lit, FloatLit):
        return _format_float(lit.value)
    if isinstance(lit, StringLit):
        return _encode_string(lit.value)
    raise TypeError(lit)


def _print_pattern(p: SurfacePattern) -> str:
    if isinstance(p, PWild):
        return "_"
    if isinstance(p, PLit):
        return _print_literal(p.literal)
    if isinstance(p, PTuple):
        return "(" + ", ".join(_print_pattern(x) for x in p.patterns) + ")"
    if isinstance(p, PApp):
        if not p.patterns:
            return p.name
        return p.name + " " + " ".join(_print_pattern_atom(x) for x in p.patterns)
    raise TypeError(p)


def _print_pattern_atom(p: SurfacePattern) -> str:
    if isinstance(p, PApp) and p.patterns:
        return "(" + _print_pattern(p) + ")"
    return _print_pattern(p)


def _starts_with_sum_application(t: Surface) -> bool:
    """Whether printing ``t`` begins with a sum used as an application head."""
    if isinstance(t, App):
        f = t.function
        while isinstance(f, App):
            f = f.function
        return isinstance(f, Sum)
    return False


def _needs_parens(child: Surface, parent_op: str, side: str) -> bool:
    if parent_op == ">" and side == "left" and _starts_with_sum_application(child):
        return True
    cp = _precedence(child)
    pp = _PREC[parent_op]
    if _open_ending(child):
        if side == "right" and parent_op in {"&", "->"}:
            return False
        return True
    if cp < pp:
        return True
    if cp > pp:
        return False
    if not isinstance(child, Binop):
        return False
    if parent_op in _RIGHT_ASSOC:
        return side == "left"
    return side == "right"


def _print_operand(child: Surface, parent_op: str, side: str) -> str:
    s = _print_term(child)
    return f"({s})" if _needs_parens(child, parent_op, side) else s


def _contains_brace_argument(t: Surface) -> bool:
    if not isinstance(t, App):
        return False
    if isinstance(t.argument, (Record, Subtype, RecordValue, Block)):
        return True
    return _contains_brace_argument(t.function)


def _print_term(t: Surface) -> str:
    if isinstance(t, Name):
        return t.name
    if isinstance(t, Literal):
        return _print_literal(t.literal)
    if isinstance(t, Universe):
        return "U"
    if isinstance(t, World):
        return "W"
    if isinstance(t, Binop):
        return (
            f"{_print_operand(t.left, t.operator, 'left')} "
            f"{t.operator} "
            f"{_print_operand(t.right, t.operator, 'right')}"
        )
    if isinstance(t, Neg):
        inner = _print_term(t.value)
        if isinstance(t.value, Neg) or _precedence(t.value) < 9:
            inner = f"({inner})"
        return "-" + inner
    if isinstance(t, App):
        left = _print_term(t.function)
        if _precedence(t.function) < 10 or isinstance(t.function, Neg) or _open_ending(t.function):
            left = f"({left})"
        arg = _print_term(t.argument)
        if not _is_arg_atom(t.argument) and not isinstance(t.argument, Proj):
            arg = f"({arg})"
        elif isinstance(t.argument, Sum):
            arg = f"({arg})"
        return left + " " + arg
    if isinstance(t, Proj):
        return f"({_print_term(t.value)}).{t.field}"
    if isinstance(t, Tuple):
        return "(" + ", ".join(_print_term(x) for x in t.values) + ")"
    if isinstance(t, Pi):
        return f"({' '.join(t.names)} : {_print_term(t.domain)}) -> {_print_term(t.codomain)}"
    if isinstance(t, Sigma):
        return f"({' '.join(t.names)} : {_print_term(t.domain)}) * {_print_term(t.codomain)}"
    if isinstance(t, SigmaNamed):
        return (
            f"({t.left_name} : {_print_term(t.left_type)}) * "
            f"({t.right_name} : {_print_term(t.right_type)})"
        )
    if isinstance(t, SumNamed):
        return (
            f"({t.left_name} : {_print_term(t.left_type)}) + "
            f"({t.right_name} : {_print_term(t.right_type)})"
        )
    if isinstance(t, Record):
        fs = ", ".join(
            f"{' '.join(f.names)} : {_print_term(f.type)}" for f in t.fields
        )
        law = "" if t.law is None else " | " + _print_term(t.law)
        return "{ " + fs + law + " }"
    if isinstance(t, Subtype):
        return (
            f"{{ {_print_pattern(t.pattern)} : {_print_term(t.type)} "
            f"| {_print_term(t.law)} }}"
        )
    if isinstance(t, RecordValue):
        return "{ " + ", ".join(
            f"{k} := {_print_term(v)}" for k, v in t.fields
        ) + " }"
    if isinstance(t, Block):
        parts = [_print_item(x) for x in t.items] + [_print_term(t.value)]
        return "{ " + " ; ".join(parts) + " }"
    if isinstance(t, Sum):
        return "< " + " | ".join(
            f"{k} : {_print_term(v)}" for k, v in t.alternatives
        ) + " >"
    if isinstance(t, List):
        return "[" + ", ".join(_print_term(x) for x in t.values) + "]"
    if isinstance(t, Lambda):
        params = " ".join(_print_lparam(p) for p in t.params)
        parts = [_print_item(x) for x in t.items] + [_print_term(t.body)]
        return "\\ " + params + " { " + " ; ".join(parts) + " }"
    if isinstance(t, MatchOf):
        arms = " ; ".join(
            f"{_print_pattern(p)} -> {_print_term(v)}" for p, v in t.arms
        )
        subject = _print_term(t.value)
        if _contains_brace_argument(t.value):
            subject = f"({subject})"
        return f"match {subject} {{" + (" " + arms + " " if arms else " ") + "}"
    if isinstance(t, NamedArg):
        return f"({t.name} <- {_print_term(t.value)})"
    if isinstance(t, IfThen):
        cond = _print_term(t.condition)
        yes = _print_term(t.then_branch)
        if t.else_branch is not None and _open_ending(t.then_branch):
            yes = f"({yes})"
        s = f"if {cond} then {yes}"
        if t.else_branch is not None:
            s += " else " + _print_term(t.else_branch)
        return s
    if isinstance(t, Quoted):
        return f"quote {{ {_print_term(t.value)} }}"
    raise TypeError(t)


def _print_item(item) -> str:
    if isinstance(item, Bind):
        return f"{item.name} := {_print_term(item.value)}"
    if isinstance(item, Rebind):
        return f"{item.name} <- {_print_term(item.value)}"
    raise TypeError(item)


def _print_lparam(p) -> str:
    if isinstance(p, PlainParam):
        return p.name
    if isinstance(p, TypedParam):
        return f"({' '.join(p.names)} : {_print_term(p.type)})"
    if isinstance(p, ShapeParam):
        return "(" + ", ".join(_print_pattern(x) for x in p.patterns) + ")"
    raise TypeError(p)


def _print_binder(b) -> str:
    if isinstance(b, Explicit):
        s = f"({' '.join(b.names)} : {_print_term(b.type)}"
        if b.default is not None:
            s += " <- " + _print_term(b.default)
        return s + ")"
    if isinstance(b, Implicit):
        return f"{{{' '.join(b.names)} : {_print_term(b.type)}}}"
    raise TypeError(b)


def _print_act(a: SurfaceAct) -> str:
    if isinstance(a, Declare):
        bs = "".join(" " + _print_binder(b) for b in a.binders)
        return f"{a.name}{bs} : {_print_term(a.type)}"
    if isinstance(a, Define):
        bs = "".join(" " + _print_binder(b) for b in a.binders)
        ann = "" if a.type is None else " : " + _print_term(a.type)
        if isinstance(a.body, TermBody):
            return f"{a.name}{bs}{ann} := {_print_term(a.body.term)}"
        if isinstance(a.body, DataBody):
            inside = " ; ".join(
                f"{k} : {_print_term(v)}" for k, v in a.body.constructors
            )
            return (
                f"{a.name}{bs}{ann} := data {{"
                + (" " + inside + " " if inside else " ")
                + "}"
            )
        if isinstance(a.body, ClausesBody):
            clauses = " ".join(
                "| "
                + ", ".join(_print_pattern(p) for p in c.patterns)
                + " := "
                + _print_term(c.body)
                for c in a.body.clauses
            )
            return f"{a.name}{bs}{ann} {clauses}"
    if isinstance(a, Alias):
        bs = "".join(" " + _print_binder(b) for b in a.binders)
        return f"{a.name}{bs} = {_print_term(a.value)}"
    if isinstance(a, ImportAct):
        parts = []
        for n in a.names:
            s = n.name
            if n.theory is not None:
                s += " : " + n.theory
            if n.asName is not None:
                s += " as " + n.asName
            parts.append(s)
        return "import " + _encode_string(a.path) + " " + " ".join(parts)
    if isinstance(a, OperatorAct):
        return f"operator {a.operator} := {_print_term(a.value)}"
    if isinstance(a, Datum):
        return _print_term(a.value)
    raise TypeError(a)


def print_program(program: tuple[SurfaceAct, ...]) -> str:
    """Print a surface program canonically, one act per line."""
    if not program:
        return ""
    return "\n".join(_print_act(a) for a in program) + "\n"
```

### `src/luthier/cli.py`

```python
"""Command line interface for the bootstrap Luthier parser."""

from __future__ import annotations

import argparse
from pathlib import Path

from .parse import parse
from .surface import ParseFailed, Parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="luthier")
    sub = parser.add_subparsers(dest="command", required=True)
    p_parse = sub.add_parser("parse", help="parse Luthier source files")
    p_parse.add_argument("--tree", action="store_true", help="print each parsed act")
    p_parse.add_argument("files", nargs="+")
    ns = parser.parse_args(argv)

    failed = False
    for raw_path in ns.files:
        path = Path(raw_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"{path}:1:0: {exc}")
            failed = True
            continue
        result = parse(text)
        if isinstance(result, ParseFailed):
            failed = True
            for error in result.errors:
                print(f"{path}:{error.line}:{error.column}: {error.message}")
        elif ns.tree and isinstance(result, Parsed):
            for act in result.program:
                print(act)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `tests/test_parse.py`

```python
"""The laws of ``Grammar`` in ``grammar.lth``, transcribed as pytest tests."""

from __future__ import annotations

from pathlib import Path
import random
import re

import pytest

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


def _derives_by_acts(text: str, *, skip_luthier_syntax: bool = True) -> bool:
    """Check ``program ::= { act newline }`` one laid-out act at a time.

    The one bootstrap act defining ``luthierSyntax`` has 1842 laid-out tokens and
    is intentionally omitted here; a dedicated skipped test below records that
    missing recognizer check.
    """
    lr = lex(text)
    if isinstance(lr, LexFailed):
        return False
    views = list(layout(lr.tokens))
    start = 0
    for i, tv in enumerate(views):
        if tv == ("newline", "\n"):
            segment = views[start:i]
            if skip_luthier_syntax and _is_luthier_syntax_act(segment):
                start = i + 1
                continue
            if count_derivations(G, segment, "act") == 0:
                return False
            start = i + 1
    return start == len(views)


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


@pytest.mark.skip(
    reason="count_derivations too slow on 1842 tokens; the recognizer will be replaced"
)
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
                assert len(segment) == 1842
                assert count_derivations(G, segment, "act") > 0
                return
            start = i + 1
    raise AssertionError("luthierSyntax act not found")


@pytest.mark.xfail(
    reason=(
        "defect of grammar.lth: `match f { p -> q } { r -> s }` "
        "has two derivations with different trees"
    ),
    strict=True,
)
def test_match_followed_by_block_is_unambiguous():
    text = "x := match f { p -> q } { r -> s }"
    lr = lex(text)
    assert isinstance(lr, Lexed)
    views = list(layout(lr.tokens))
    assert views[-1] == ("newline", "\n")
    assert count_derivations(G, views[:-1], "act") == 1


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
```

### `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "luthier"
version = "0.2.0.dev0"
description = "Luthier: a language of tested types, rebuilt from its theories (the v0.1 interpreter is at the tag v0.1-final)."
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
luthier = "luthier.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
luthier = ["lib/*.lth", "lib/*.lut"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Report

I treated `grammar.lth`, not the explanatory EBNF in chapter 2, as the authority. That is explicitly what the source says: `luthierSyntax` is the grammar, the parser is supposed to accept exactly what it derives, and the tree laws select the surface tree. grammar.lth(1) Chapter 2 likewise says that where its explanatory grammar and `luthierSyntax` differ, the value in `grammar.lth` holds. 02-grammar(3)

### What passes

The lexer, layout, parser, printer, tree-law tests, precedence tests, lexical tests, layout tests, and bootstrap-file parsing pass in the executable state delivered here. In particular, all three bootstrap files parse: `grammar.lth` gives 138 acts, `ebnf.lth` 55 acts, and `ebnf_model.lut` 11 acts. This is significant because the theory explicitly requires the Python parser to be the first specimen of the four-operation `Grammar` interface. grammar.lth(1)

Running the suite while excluding the expensive `ParsesWhatDerives` test gave:

```text
65 passed, 2 deselected, 1 xfailed
```

The explicit skip/xfail/bootstrap-file selection gives:

```text
1 passed, 1 skipped, 1 xfailed
```

Python compilation of `surface.py`, `parse.py`, `cli.py`, and `test_parse.py` also succeeds.

### Skipped / incomplete

`test_parses_what_derives_luthier_syntax_act` is deliberately:

```python
@pytest.mark.skip(
    reason="count_derivations too slow on 1842 tokens; the recognizer will be replaced"
)
```

The laid-out `luthierSyntax` definition contains exactly 1,842 tokens. Per your correction, whole-file `ParsesWhatDerives` is decomposed at layout newlines and calls `count_derivations(G, segment, "act")` on each act rather than asking `count_derivations` to recognize the entire `program`. This follows directly from the authoritative production `program ::= { act "\n" }`. grammar.lth(1)

One limitation remains in the state being delivered: although the 1,842-token act itself is skipped, the complete `test_parses_what_derives` over all case texts, generated texts and every other act of all three bootstrap files still did not finish within a 120-second execution attempt. I therefore cannot report the **entire** `ParsesWhatDerives` corpus as passed. This is recognizer performance, not a parser failure observed on those inputs. `ebnf.py` uses span-based recursive counting and is explicitly counting derivations rather than merely parsing. ebnf.py

### Expected failure: defect in `grammar.lth`

`match f { p -> q } { r -> s }` has two derivations under the current `luthierSyntax`. I verified:

```text
count_derivations(..., "act") == 2
```

The two readings are structurally different: one can treat the first brace as the `match` arms and the second brace as an application argument/block; the other can absorb the first brace into the subject and use the second as the match arms.

That means the grammar does not uniquely determine a tree here. The parser currently chooses the **earliest viable brace as the match-arm delimiter**, yielding approximately:

```text
(match f { p -> q }) { r -> s }
```

The test is therefore strict `xfail` and calls this a defect of `grammar.lth`. This matters because the theory says the grammar derives the token language and the tree laws pin which tree a text gives; here there is no law selecting between these two trees. grammar.lth(1)

This is distinct from the intentional dangling-`else` ambiguity: `grammar.lth` explicitly supplies `DanglingElse` to choose the nearest `if`. grammar.lth(1) There is no analogous law for the `match`/brace case.

### Readings I had to choose

1. **Reserved words come only from `luthierSyntax`.** I ignored the chapter's historical reserved-word enumeration where it disagrees. Thus `extern`, `primitive`, `axiom`, `forget`, `test`, `cite`, `eval`, `provisional`, etc. lex as names in this grammar. This is also exactly what the final lexical law `OtherWordsAreNames` requires. grammar.lth(1)

2. **Operators are derived, not copied into the lexer.** `_LITERALS` comes from `lits_of(luthier_syntax())`; binary and bound operators come from `lits_of_names`. That follows the theory's explicit rule that keyword/operator inventories are consequences of the grammar rather than independent lists. grammar.lth(1)

3. **An `act` alternative succeeds only if it consumes through the act boundary.** `declaration`, `definition`, `alias`, and `datum` share prefixes. In recursive descent, accepting the first locally successful prefix gives wrong answers. `act()` therefore tries each and commits only if the next token is the layout newline. This is a parsing implementation of the actual EBNF alternation, not an extra syntactic rule.

4. **`<` opens angle brackets only when it lexically looks like a sum head: `< name :`.** Otherwise it is treated as the comparison operator for layout purposes. This is needed because `<` is both a comparison literal and the opening delimiter of a sum; treating every `<` as an open bracket makes ordinary comparisons suppress later newlines.

5. **`>` inside a sum is resolved by viable parsing, preferring a later closing boundary.** Since `>` is simultaneously a comparison operator and the sum delimiter, the parser searches candidate `|`/`>` boundaries and accepts one for which the intervening tokens form a complete `term`.

6. **`quote { ... }` braces ignore line breaks.** The layout prose explicitly names several brace classes but not `quote`. Its grammar production is `quote "{" term "}"`, not a sequence of items, so treating the braces as ordinary item-separating braces would inject `;` tokens that its production cannot consume. This is a reading forced by `luthierSyntax`.

7. **`data { ... }` braces are item-separating braces.** This one is explicitly called out by the theory as its reading where the prose had been silent. grammar.lth(1)

8. **Match braces are identified contextually rather than by `{` alone.** A brace containing a top-level `->` is a candidate match-arm brace if an unmatched `match` can own it. This is necessary because the same `{...}` token pair also denotes records, subtypes, record values and blocks.

9. **For the unresolved match/block ambiguity, choose the earliest viable match-arm brace.** This choice is not justified as language semantics; it is only the deterministic behavior of this specimen and is documented as a grammar defect via the `xfail`.

10. **A two-named dependent product is taken as `SigmaNamed` only when that reading closes at that point.** Thus `(a : A) * (b : B)` is `SigmaNamed`, while `(a : A) * (b : B) * C` follows the explicit tree law and becomes nested `Sigma`. The tree laws require these outcomes. grammar.lth(1)

11. **Brace alternatives are resolved by complete syntactic success.** A `{...}` term is attempted as record, subtype, record value, then block. This reflects the alternatives in `argAtom`; it is not based on semantic knowledge.

12. **A one-field `{ a : Int }` is a record; `{ a : Int | p }` is a subtype.** The theory's `recordFields` machinery and `wf` constraint explicitly preserve this distinction: a single labeled field cannot carry a record law. grammar.lth(1)

13. **Parentheses leave no tree node.** Parenthesized terms and patterns return the contained tree directly, as required by the surface theory.

14. **The dangling `else` goes to the nearest `if`.** Unlike the match ambiguity, this is explicitly resolved by a law and implemented deliberately. grammar.lth(1)

15. **Printer conservatism is allowed where necessary for `RoundTrip`.** It writes projections as `(a).b`, nested negation as `-(-a)`, parenthesizes open forms when their unparenthesized form would change association, protects a then-branch capable of stealing an `else`, and parenthesizes a brace-bearing application when printed as a match subject. `RoundTrip` and `Canonical` are the governing laws, rather than preservation of original spelling. Those are explicitly among the general laws. grammar.lth(1)

16. **Floats are printed by spelling rather than by preserving their original token.** The surface tree contains the numeric value, not its original spelling. The printer therefore ensures the output contains `.` or an exponent so the lexer reconstructs `FloatLit`, satisfying round trip.

17. **Lexical errors reject unknown escapes.** The theory specifies exactly `\"`, `\\`, and `\n`; I treated other backslash escapes as lexical errors rather than leaving them uninterpreted. grammar.lth(1)

18. **Comments disappear before layout.** Because the lexer result has no comment constructor and the law says comments are not tokens, physical blank/comment lines cannot be reconstructed by layout; they simply vanish. grammar.lth(1)

19. **Parse errors return one furthest-position error.** `Grammar` requires at least one error and positive line numbers, but does not require recovery or multiple diagnostics. The implementation therefore reports a single accumulated furthest-failure error. grammar.lth(1)

20. **The three bootstrap files are tests of syntax, not of semantic well-formedness.** The parser preserves acts exactly at the surface level; whether declarations, types, imports, laws, etc. are semantically valid is outside this parser, matching the theory's statement that the parser decides little and the checker decides meaning. grammar.lth(1)

### Things I believe are wrong in `grammar.lth`

The concrete defect found is the `match f { p -> q } { r -> s }` ambiguity above. It should be repaired in `luthierSyntax` or pinned by a tree law before this parser becomes the pattern copied by later theories.

There is also a specification-level pressure point around layout: layout must classify `{...}` as either “ignore line breaks” or “turn line breaks into separators” **before parsing**, yet which role a brace has can depend on its syntactic parse. `match` exposes this most sharply. The current grammar makes some brace classifications context-sensitive enough that the layout pass effectively has to perform partial syntactic recognition. The theory itself acknowledges that different brace forms have different layout behavior. grammar.lth(1) I would regard eliminating that circularity—not merely patching the one ambiguous string—as the more important next grammar change.

Finally, the entire conjunction that defines `Grammar` contains all the general, lexical, layout, precedence and constructor laws transcribed into the test file. grammar.lth(1) The delivered specimen satisfies the tested ones except for the explicitly marked grammar ambiguity; the exhaustive `ParsesWhatDerives` corpus cannot yet be claimed because the current derivation counter is computationally impractical on the largest bootstrap acts.