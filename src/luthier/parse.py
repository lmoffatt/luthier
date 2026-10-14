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
    Sigma, SigmaNamed, StringLit, Subtype, Sum, Surface, SurfaceAct,
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
    match_pending: bool = False


def _continuation_start(text: str) -> bool:
    return text in {"then", "else", "||"} or text in _BINARY_OPERATORS


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

    # A pending match belongs to its bracket level. Brackets in its scrutinee
    # shield their own braces; the first brace back at this level opens arms.
    root_match_pending = False
    prev: Token | None = None
    for tok in tokens:
        if prev is not None and tok.line > prev.line:
            next_text = tok.text
            prev_text = prev.text

            if stack:
                top = stack[-1]
                if top.opener in {"(", "["} or top.kind == "ignoring":
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
                if tok.column == 0:
                    append_token(Token("newline", "\n", tok.line, tok.column))
                    root_match_pending = False
                # An indented line continues the act.

        if tok.text in {"(", "[", "{"}:
            kind = "ignoring"
            if tok.text == "{":
                pending = stack[-1].match_pending if stack else root_match_pending
                kind = "ignoring" if pending or (prev and prev.text == "quote") else "separating"
                if pending:
                    if stack:
                        stack[-1].match_pending = False
                    else:
                        root_match_pending = False
            append_token(tok)
            stack.append(_Frame(tok.text, kind))
        elif tok.text in {")", "]", "}"}:
            append_token(tok)
            if stack:
                want = {")": "(", "]": "[", "}": "{"}[tok.text]
                # Mismatches are left for the parser; pop only a matching opener.
                if stack[-1].opener == want:
                    stack.pop()
        else:
            append_token(tok)

        if tok.text == "match":
            if stack:
                stack[-1].match_pending = True
            else:
                root_match_pending = True
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

    def _starts_atom(self) -> bool:
        if self.i >= len(self.tokens):
            return False
        t = self.tokens[self.i]
        return t.kind in {"name", "number", "string"} or t.text in {
            "U", "W", "(", "{", "[", "fn", "match", "quote"
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
        """openForm ::= dependent pi | dependent sigma | named sigma | if-form"""
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
        """appTerm ::= projTerm { projTerm }"""
        value = self.projTerm()
        while self._starts_atom():
            start = self.i
            try:
                arg = self.projTerm()
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
            for part in self._name().split("."):
                value = Proj(value, part)
        return value

    def scrutinee(self) -> Surface:
        return self._left_chain(self.sAnd, {"or"})

    def sAnd(self) -> Surface:
        return self._left_chain(self.sCmp, {"and"})

    def sCmp(self) -> Surface:
        return self._left_chain(self.sAdd, {"==", "/=", "<", "<=", ">", ">="})

    def sAdd(self) -> Surface:
        return self._left_chain(self.sMul, {"+", "-"})

    def sMul(self) -> Surface:
        return self._left_chain(self.sNeg, {"*", "/", "mod"})

    def sNeg(self) -> Surface:
        if self._peek("-"):
            self._take("-")
            return Neg(self.sNeg())
        return self.sApp()

    def sApp(self) -> Surface:
        value = self.sProj()
        while self._starts_s_atom():
            value = App(value, self.sProj())
        return value

    def sProj(self) -> Surface:
        value = self.sAtom()
        while self._peek("."):
            self._take(".")
            for part in self._name().split("."):
                value = Proj(value, part)
        return value

    def _starts_s_atom(self) -> bool:
        return self.i < len(self.tokens) and (
            self.tokens[self.i].kind in {"name", "number", "string"}
            or self.tokens[self.i].text in {"U", "W", "(", "["}
        )

    def sAtom(self) -> Surface:
        if not self._starts_s_atom():
            self._fail("scrutinee atom")
        return self.atom()

    def atom(self) -> Surface:
        """atom ::= name | number | string | U | W | parenthesized/tuple/named-arg | braces | list | lambda | match | quote"""
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
        if self._peek("fn"):
            self._take("fn")
            params = [self.lparam()]
            while not self._peek("{"):
                params.append(self.lparam())
            self._take("{")
            items, body = self.block()
            self._take("}")
            return Lambda(tuple(params), items, body)
        if self._peek("match"):
            self._take("match")
            value = self.scrutinee()
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
            self._sum_atom,
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

    def _sum_atom(self) -> Surface:
        self._take("{")
        alternatives = []
        while True:
            name = self._name()
            self._take(":")
            alternatives.append((name, self.term()))
            if not self._peek("||"):
                break
            self._take("||")
        if len(alternatives) < 2:
            self._fail("at least two sum alternatives")
        self._take("}")
        return Sum(tuple(alternatives))

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
        """item ::= name ":=" term | pattern "<-" term"""
        start = self.i
        if self._peek(kind="name"):
            name = self._name()
            if self._peek(":="):
                self._take(":=")
                return Bind(name, self.term())
            self._mark("':='")
            self.i = start
        pattern = self.pattern()
        self._take("<-")
        return Rebind(pattern, self.term())

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
    if isinstance(t, (Pi, Sigma, SigmaNamed, IfThen)):
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
    if isinstance(t, (Pi, Sigma, SigmaNamed, IfThen)):
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
            Sum,
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
    if x == 0.0:
        return "0.0"
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


def _needs_parens(child: Surface, parent_op: str, side: str) -> bool:
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


def _scrutinee_needs_parens(t: Surface) -> bool:
    if isinstance(t, Binop):
        return t.operator in {"&", "->"} or (
            _scrutinee_needs_parens(t.left) or _scrutinee_needs_parens(t.right)
        )
    if isinstance(t, Neg):
        return _scrutinee_needs_parens(t.value)
    if isinstance(t, App):
        return _scrutinee_needs_parens(t.function) or _scrutinee_needs_parens(t.argument)
    if isinstance(t, Proj):
        return _scrutinee_needs_parens(t.value)
    return not isinstance(t, (Name, Literal, Universe, World, Tuple, NamedArg, List))


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
        return "{ " + " || ".join(
            f"{k} : {_print_term(v)}" for k, v in t.alternatives
        ) + " }"
    if isinstance(t, List):
        return "[" + ", ".join(_print_term(x) for x in t.values) + "]"
    if isinstance(t, Lambda):
        params = " ".join(_print_lparam(p) for p in t.params)
        parts = [_print_item(x) for x in t.items] + [_print_term(t.body)]
        return "fn " + params + " { " + " ; ".join(parts) + " }"
    if isinstance(t, MatchOf):
        arms = " ; ".join(
            f"{_print_pattern(p)} -> {_print_term(v)}" for p, v in t.arms
        )
        subject = _print_term(t.value)
        if _scrutinee_needs_parens(t.value):
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
        return f"{_print_pattern(item.pattern)} <- {_print_term(item.value)}"
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
