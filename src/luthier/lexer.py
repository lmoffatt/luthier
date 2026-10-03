"""Tokenizer. Top-level blocks start at column 0; continuation lines are indented."""
from __future__ import annotations
from dataclasses import dataclass
import re

SYMBOLS = [":=", "->", "==", "/=", "<=", ">=", "'{", "${",
           ":", "(", ")", "{", "}", "[", "]", ",", "|", "&", "\\", "*", "+", "-", "/", "<", ">", "=", ";", "."]
KEYWORDS = {"data", "match", "extern", "test", "with", "exhaustive", "gen", "import", "forget", "U", "operator",
            "if", "then", "else"}
INFIX_NAMES = {"and", "or", "mod"}  # ordinary names that are also infix operators

TOKEN_RE = re.compile(r"""
    (?P<ws>[ \t]+)
  | (?P<comment>--[^\n]*)
  | (?P<newline>\n)
  | (?P<number>\d+(\.\d+)?([eE][+-]?\d+)?)
  | (?P<string>"(?:[^"\\]|\\.)*")
  | (?P<name>[A-Za-z_][A-Za-z0-9_']*(\.[A-Za-z_][A-Za-z0-9_']*)*(\#\d+)?)
  | (?P<symbol>:=|->|==|/=|<=|>=|'\{|\$\{|[:(){}\[\],|&\\*+\-/<>=;.])
""", re.VERBOSE)


@dataclass
class Token:
    kind: str   # name, keyword, number, string, symbol, newline, eof
    text: str
    line: int
    col: int

    def __repr__(self):
        return f"{self.kind}:{self.text!r}@{self.line}:{self.col}"


class LexError(Exception):
    pass


def tokenize(src: str) -> list[Token]:
    toks: list[Token] = []
    pos, line, col = 0, 1, 0
    while pos < len(src):
        m = TOKEN_RE.match(src, pos)
        if not m:
            raise LexError(f"line {line}, col {col}: unexpected character {src[pos]!r}")
        kind = m.lastgroup
        text = m.group(kind)
        if kind == "ws" or kind == "comment":
            pass
        elif kind == "newline":
            toks.append(Token("newline", "\n", line, col))
            line += 1
            col = -len(text)
        elif kind == "name":
            toks.append(Token("keyword" if text in KEYWORDS else "name", text, line, col))
        else:
            toks.append(Token(kind, text, line, col))
        pos = m.end()
        col += len(text)
    toks.append(Token("newline", "\n", line, col))
    toks.append(Token("eof", "", line + 1, 0))
    return toks
