"""Recursive-descent parser for Luthier version 0.

Precedence, loosest to tightest:
  &  |  ->  |  or  |  and  |  == /= < <= > >=  |  + -  |  * / mod  |  application
`->` and `*` are elaborated later (Pi/implication, Sigma/multiplication).
"""
from __future__ import annotations
from .lexer import tokenize, Token, INFIX_NAMES
from .syntax import *


class ParseError(Exception):
    pass


BINOPS = [
    ("&",),
    ("->",),
    ("or",),
    ("and",),
    ("==", "/=", "<", "<=", ">", ">="),
    ("+", "-"),
    ("*", "/", "mod"),
]
RIGHT_ASSOC = {"&", "->"}


class Parser:
    def __init__(self, src: str):
        self.toks = tokenize(src)
        self.i = 0
        self.skip_newlines = 0    # depth counter: inside (), {}, [] newlines are ignored
        self.strict_newlines = 0  # while > 0, a newline always ends the current phrase (subtype components)
        self.no_brace = 0         # while > 0, '{' does not start an atom (match scrutinee)

    # ------------------------------------------------------------ helpers
    def _skippable_newline(self, j: int) -> bool:
        """A newline is skipped inside brackets, or at top level when the next line is indented
        (a continuation of the same definition). Never in strict mode."""
        if self.toks[j].kind != "newline":
            return False
        if self.skip_newlines > 0:
            return True
        if self.strict_newlines > 0:
            return False
        k = j
        while self.toks[k].kind == "newline":
            k += 1
        return self.toks[k].kind != "eof" and self.toks[k].col > 0

    def peek(self, k=0) -> Token:
        j = self.i
        seen = 0
        while True:
            if self._skippable_newline(j):
                j += 1
                continue
            t = self.toks[j]
            if seen == k:
                return t
            seen += 1
            j += 1

    def next(self) -> Token:
        while self._skippable_newline(self.i):
            self.i += 1
        t = self.toks[self.i]
        self.i += 1
        return t

    def at(self, kind, text=None) -> bool:
        t = self.peek()
        return t.kind == kind and (text is None or t.text == text)

    def at_sym(self, text) -> bool:
        return self.at("symbol", text)

    def at_kw(self, text) -> bool:
        return self.at("keyword", text)

    def expect(self, kind, text=None) -> Token:
        t = self.next()
        if t.kind != kind or (text is not None and t.text != text):
            want = text or kind
            raise ParseError(f"line {t.line}, col {t.col}: expected {want!r}, got {t.text!r}")
        return t

    def skip_nl(self):
        while self.toks[self.i].kind == "newline":
            self.i += 1

    def err(self, msg):
        t = self.peek()
        raise ParseError(f"line {t.line}, col {t.col}: {msg} (at {t.text!r})")

    # ------------------------------------------------------------ program
    def parse_program(self) -> Program:
        prog = Program()
        self.skip_nl()
        while not self.at("eof"):
            if self.at_kw("test"):
                prog.tests.append(self.parse_test())
            elif self.at_kw("gen"):
                prog.gens.append(self.parse_gen())
            elif self.at_kw("import"):
                prog.imports.append(self.parse_import())
            else:
                prog.defs.append(self.parse_def())
            self.skip_nl()
        return prog

    def parse_test(self) -> TestDirective:
        self.expect("keyword", "test")
        name = self.expect("name").text
        n, exhaustive, size = 100, False, None
        if self.at_kw("with"):
            self.next()
            n = int(self.expect("number").text)
        elif self.at_kw("exhaustive"):
            self.next()
            exhaustive = True
        if self.at("name") and self.peek().text == "size":
            self.next()
            size = int(self.expect("number").text)
        self.end_of_block()
        return TestDirective(name, n, exhaustive, size)

    def parse_import(self) -> ImportDirective:
        t = self.expect("keyword", "import")
        path = self.expect("string").text[1:-1]
        alias = None
        if self.at("name") and self.peek().text == "as":
            self.next()
            alias = self.expect("name").text
        self.end_of_block()
        return ImportDirective(path, alias, t.line)

    def parse_gen(self) -> GenDirective:
        self.expect("keyword", "gen")
        tname = self.expect("name").text
        self.expect("symbol", ":=")
        if self.at_kw("extern"):
            self.next()
            target = self.expect("string").text[1:-1]
            self.end_of_block()
            return GenDirective(tname, target=target)
        term = self.parse_term()
        self.end_of_block()
        return GenDirective(tname, term=term)

    def end_of_block(self):
        """A block ends at a newline followed by a token at column 0 (or eof)."""
        t = self.toks[self.i]
        if t.kind == "eof":
            return
        if t.kind != "newline":
            raise ParseError(f"line {t.line}, col {t.col}: unexpected {t.text!r} at end of definition")
        self.skip_nl()

    def block_continues(self) -> bool:
        """True if the next non-newline token is indented (continuation of the block)."""
        j = self.i
        while self.toks[j].kind == "newline":
            j += 1
        t = self.toks[j]
        return t.kind != "eof" and t.col > 0

    def parse_def(self) -> Def:
        name_tok = self.expect("name")
        name = name_tok.text
        binders = []
        while self.at_sym("("):
            binders.append(self.parse_binder())
        typ = None
        if self.at_sym(":"):
            self.next()
            typ = self.parse_term()
        body = None
        data = None
        if self.at_sym(":="):
            self.next()
            if self.at_kw("data"):
                data = self.parse_data(name, binders)
            elif self.at_kw("extern"):
                self.next()
                target = self.expect("string").text[1:-1]
                body = Extern(target)
            else:
                body = self.parse_term()
        # clauses: | pat, pat := body   (each on its own indented line)
        clauses = []
        while self.block_continues() and self._peek_after_nl_is("|"):
            self.skip_nl()
            self.expect("symbol", "|")
            pats = [self.parse_pattern()]
            while self.at_sym(","):
                self.next()
                pats.append(self.parse_pattern())
            self.expect("symbol", ":=")
            rhs = self.parse_term()
            clauses.append((pats, rhs))
        self.end_of_block()
        if clauses:
            if body is not None:
                self.err("definition has both a body and clauses")
            if len(binders) == 0:
                raise ParseError(f"line {name_tok.line}: clauses need parameters in the header")
            body = self.clauses_to_match(binders, clauses)
        if data is not None:
            return Def(name, typ or Univ(), None, data=data)
        # wrap binders: type becomes Pi chain, body becomes Lam chain
        for names, btype in reversed(binders):
            for n in reversed(names):
                if typ is not None:
                    typ = Pi(n, btype, typ)
                if body is not None:
                    body = Lam(PVar(n), body, ann=btype)
        if typ is None and body is None:
            self.err(f"definition {name!r} needs a type or a body")
        return Def(name, typ, body)

    def _peek_after_nl_is(self, sym) -> bool:
        j = self.i
        while self.toks[j].kind == "newline":
            j += 1
        return self.toks[j].kind == "symbol" and self.toks[j].text == sym

    def clauses_to_match(self, binders, clauses) -> Term:
        names = [n for ns, _ in binders for n in ns]
        # scrutinee: tuple of parameters; patterns: tuple patterns
        def tuple_term(xs):
            t = Var(xs[-1])
            for x in reversed(xs[:-1]):
                t = Pair(Var(x), t)
            return t

        def tuple_pat(ps):
            p = ps[-1]
            for q in reversed(ps[:-1]):
                p = PPair(q, p)
            return p
        branches = []
        for pats, rhs in clauses:
            if len(pats) != len(names):
                raise ParseError(f"clause has {len(pats)} patterns but the header has {len(names)} parameters")
            branches.append((tuple_pat(pats), rhs))
        return Match(tuple_term(names), tuple(branches))

    def parse_binder(self):
        """( x y : T )"""
        self.expect("symbol", "(")
        self.skip_newlines += 1
        names = [self.expect("name").text]
        while self.at("name"):
            names.append(self.next().text)
        self.expect("symbol", ":")
        typ = self.parse_term()
        self.skip_newlines -= 1
        self.expect("symbol", ")")
        return (names, typ)

    def parse_data(self, name, binders) -> DataDecl:
        self.expect("keyword", "data")
        self.expect("symbol", "{")
        self.skip_newlines += 1
        cons = []
        while not self.at_sym("}"):
            cname = self.expect("name").text
            self.expect("symbol", ":")
            ctype = self.parse_term()
            cons.append(Constructor(cname, ctype))
            if self.at_sym(";"):
                self.next()
        self.skip_newlines -= 1
        self.expect("symbol", "}")
        params = [(n, t) for ns, t in binders for n in ns]
        return DataDecl(name, params, cons)

    # -------------------------------------------------------------- terms
    def parse_term(self) -> Term:
        return self.parse_binop(0)

    def parse_binop(self, level: int) -> Term:
        if level >= len(BINOPS):
            return self.parse_app()
        ops = BINOPS[level]
        lhs = self.parse_binop(level + 1)
        while self._at_op(ops):
            op = self.next().text
            if op in RIGHT_ASSOC:
                rhs = self.parse_binop(level)
            else:
                rhs = self.parse_binop(level + 1)
            lhs = self.make_binop(op, lhs, rhs)
            if op in RIGHT_ASSOC:
                break
        return lhs

    def _at_op(self, ops) -> bool:
        t = self.peek()
        return (t.kind in ("symbol", "keyword", "name")) and t.text in ops

    def make_binop(self, op, lhs, rhs) -> Term:
        if op == "&":
            return And(lhs, rhs)
        if op == "->":
            return Arrow(lhs, rhs)
        return BinOp(op, lhs, rhs)

    def parse_app(self) -> Term:
        fn = self.parse_postfix(self.parse_atom())
        while self.starts_atom():
            arg = self.parse_postfix(self.parse_atom())
            fn = App(fn, arg)
        return fn

    def parse_postfix(self, t: Term) -> Term:
        """`(term).field`: projection of a named component. A dotted name `x.field` arrives as one
        name token and is resolved by the checker; this handles the dot after a closing bracket."""
        while self.at_sym(".") and self.peek(1).kind == "name":
            self.next()
            for field in self.next().text.split("."):   # `(x).a.b` arrives as the one name token `a.b`
                t = Proj(t, field)
        return t

    def starts_atom(self) -> bool:
        t = self.peek()
        if t.kind == "name" and t.text in INFIX_NAMES:
            return False
        if t.kind in ("name", "number", "string"):
            return True
        if t.kind == "keyword" and t.text in ("U", "match", "forget", "if"):
            return True
        if t.kind == "symbol" and t.text in ("(", "[", "\\"):
            return True
        if t.kind == "symbol" and t.text == "{" and self.no_brace == 0:
            return True
        return False

    def parse_atom(self) -> Term:
        t = self.peek()
        if t.kind == "name":
            self.next()
            return Var(t.text)
        if t.kind == "number":
            self.next()
            return Lit(float(t.text) if ("." in t.text or "e" in t.text or "E" in t.text) else int(t.text))
        if t.kind == "string":
            self.next()
            return Lit(bytes(t.text[1:-1], "utf-8").decode("unicode_escape"))
        if t.kind == "keyword" and t.text == "U":
            self.next()
            return Univ()
        if t.kind == "keyword" and t.text == "match":
            return self.parse_match()
        if t.kind == "keyword" and t.text == "if":
            self.next()
            c = self.parse_term()
            self.expect("keyword", "then")
            a = self.parse_term()
            self.expect("keyword", "else")
            b = self.parse_term()
            return Match(c, ((PCon("true", ()), a), (PCon("false", ()), b)))
        if t.kind == "keyword" and t.text == "forget":
            self.next()
            return Forget(self.parse_atom())
        if t.kind == "symbol" and t.text == "\\":
            return self.parse_lambda()
        if t.kind == "symbol" and t.text == "(":
            return self.parse_paren()
        if t.kind == "symbol" and t.text == "{":
            return self.parse_brace()
        if t.kind == "symbol" and t.text == "[":
            return self.parse_list()
        self.err("expected a term")

    def parse_lambda(self) -> Term:
        self.expect("symbol", "\\")
        params = []  # list of (Pattern, ann)
        while not self.at_sym("{"):
            if self.at("name"):
                params.append((PVar(self.next().text), None))
            elif self.at_sym("("):
                self.next()
                self.skip_newlines += 1
                if self.at("name") and self._binder_ahead_from(0):
                    # ( x y : T ): annotated names
                    names = [PVar(self.next().text)]
                    while self.at("name"):
                        names.append(PVar(self.next().text))
                    self.expect("symbol", ":")
                    ann = self.parse_term()
                    self.skip_newlines -= 1
                    self.expect("symbol", ")")
                    for nm in names:
                        params.append((nm, ann))
                else:
                    # ( p ) or a tuple pattern ( p, q, ... )
                    pats = [self.parse_pattern()]
                    while self.at_sym(","):
                        self.next()
                        pats.append(self.parse_pattern())
                    p = pats[-1]
                    for q in reversed(pats[:-1]):
                        p = PPair(q, p)
                    self.skip_newlines -= 1
                    self.expect("symbol", ")")
                    params.append((p, None))
            else:
                self.err("expected a lambda parameter")
        self.expect("symbol", "{")
        self.skip_newlines += 1
        body = self.parse_term()
        self.skip_newlines -= 1
        self.expect("symbol", "}")
        for p, ann in reversed(params):
            body = Lam(p, body, ann=ann)
        return body

    def parse_paren(self) -> Term:
        self.expect("symbol", "(")
        self.skip_newlines += 1
        saved_nb, self.no_brace = self.no_brace, 0
        try:
            return self._parse_paren_body()
        finally:
            self.no_brace = saved_nb

    def _parse_paren_body(self) -> Term:
        # dependent binder: ( x y : T ) -> B   or  ( x : T ) * B
        if self.at("name") and (self.peek(1).kind == "symbol" and self.peek(1).text == ":" or
                                (self.peek(1).kind == "name" and self._binder_ahead())):
            names = [self.next().text]
            while self.at("name"):
                names.append(self.next().text)
            self.expect("symbol", ":")
            dom = self.parse_term()
            self.skip_newlines -= 1
            self.expect("symbol", ")")
            if self.at_sym("->"):
                self.next()
                cod = self.parse_binop(1)
                for n in reversed(names):
                    cod = Pi(n, dom, cod)
                return cod
            if self.at_sym("*"):
                self.next()
                snd = self.parse_binop(6)
                for n in reversed(names):
                    snd = Sigma(n, dom, snd)
                return snd
            self.err("expected '->' or '*' after a dependent binder")
        first = self.parse_term()
        if self.at_sym(","):
            items = [first]
            while self.at_sym(","):
                self.next()
                items.append(self.parse_term())
            self.skip_newlines -= 1
            self.expect("symbol", ")")
            t = items[-1]
            for x in reversed(items[:-1]):
                t = Pair(x, t)
            return t
        self.skip_newlines -= 1
        self.expect("symbol", ")")
        return first

    def _binder_ahead(self) -> bool:
        """After '(' name, are we looking at `name ... :`?"""
        return self._binder_ahead_from(1)

    def _binder_ahead_from(self, k: int) -> bool:
        while self.peek(k).kind == "name":
            k += 1
        t = self.peek(k)
        return t.kind == "symbol" and t.text == ":"

    def parse_brace(self) -> Term:
        """Subtype: { x : T | p }  or  { a b : A, c : B | p }.
        Component groups are separated by ',', ';' or a line break; the predicate follows '|'."""
        self.expect("symbol", "{")
        saved = self.skip_newlines
        self.skip_newlines = 0
        self.strict_newlines += 1
        self._skip_raw_newlines()
        groups = []  # list of (names, type)
        while True:
            names = [self.expect("name").text]
            while self.at("name"):
                names.append(self.next().text)
            self.expect("symbol", ":")
            typ = self.parse_binop(1)  # stops before '|' and '&'
            groups.append((names, typ))
            self._skip_raw_newlines()
            if self.at_sym(",") or self.at_sym(";"):
                self.next()
                self._skip_raw_newlines()
                continue
            if self.at_sym("|"):
                break
            if self.at("name"):
                continue
            self.err("expected another component or '|' in a subtype")
        self.strict_newlines -= 1
        self.expect("symbol", "|")
        self.skip_newlines = saved + 1
        pred = self.parse_term()
        self.skip_newlines = saved
        self._skip_raw_newlines()
        self.expect("symbol", "}")
        names = [n for ns, _ in groups for n in ns]
        types = [t for ns, t in groups for _ in ns]
        if len(names) == 1:
            return Subtype(PVar(names[0]), types[0], pred)
        # a dependent product: a later component's type may mention the earlier names
        base = types[-1]
        for n, t in reversed(list(zip(names[:-1], types[:-1]))):
            base = Sigma(n, t, base)
        pat = PVar(names[-1])
        for n in reversed(names[:-1]):
            pat = PPair(PVar(n), pat)
        return Subtype(pat, base, pred)

    def _skip_raw_newlines(self):
        while self.toks[self.i].kind == "newline":
            self.i += 1

    def parse_list(self) -> Term:
        self.expect("symbol", "[")
        self.skip_newlines += 1
        items = []
        while not self.at_sym("]"):
            items.append(self.parse_term())
            if self.at_sym(","):
                self.next()
        self.skip_newlines -= 1
        self.expect("symbol", "]")
        # [a, b] is sugar for a list; element type is elaborated later
        t = Var("__nil__")
        for x in reversed(items):
            t = App(App(Var("__cons__"), x), t)
        return t

    def parse_match(self) -> Term:
        self.expect("keyword", "match")
        self.no_brace += 1
        scrut = self.parse_term()
        self.no_brace -= 1
        self.expect("symbol", "{")
        self.skip_newlines += 1
        branches = []
        while not self.at_sym("}"):
            pat = self.parse_pattern()
            self.expect("symbol", "->")
            rhs = self.parse_term()
            branches.append((pat, rhs))
            if self.at_sym(";"):
                self.next()
        self.skip_newlines -= 1
        self.expect("symbol", "}")
        return Match(scrut, tuple(branches))

    # ----------------------------------------------------------- patterns
    def parse_pattern(self) -> Pattern:
        t = self.peek()
        if t.kind == "name":
            self.next()
            if t.text == "_":
                return PWild()
            args = []
            while self._starts_pattern_atom():
                args.append(self.parse_pattern_atom())
            if args or t.text[0].isupper() is False and self._is_con_name(t.text):
                return PCon(t.text, tuple(args))
            return PVar(t.text)  # resolved to PCon later if it names a constructor
        return self.parse_pattern_atom()

    def _is_con_name(self, name) -> bool:
        return False  # resolved in the checker, where constructors are known

    def _starts_pattern_atom(self) -> bool:
        t = self.peek()
        return t.kind in ("name", "number", "string") or (t.kind == "symbol" and t.text == "(")

    def parse_pattern_atom(self) -> Pattern:
        t = self.peek()
        if t.kind == "name":
            self.next()
            return PWild() if t.text == "_" else PVar(t.text)
        if t.kind == "number":
            self.next()
            return PLit(float(t.text) if "." in t.text else int(t.text))
        if t.kind == "string":
            self.next()
            return PLit(t.text[1:-1])
        if t.kind == "symbol" and t.text == "(":
            self.next()
            self.skip_newlines += 1
            pats = [self.parse_pattern()]
            while self.at_sym(","):
                self.next()
                pats.append(self.parse_pattern())
            self.skip_newlines -= 1
            self.expect("symbol", ")")
            p = pats[-1]
            for q in reversed(pats[:-1]):
                p = PPair(q, p)
            return p
        self.err("expected a pattern")


def parse(src: str) -> Program:
    return Parser(src).parse_program()


def parse_term(src: str) -> Term:
    p = Parser(src)
    p.skip_newlines += 1
    return p.parse_term()
