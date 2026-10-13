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
    """`pattern <- value`: the left of `<-` is a pattern (D-2026-10-13-ag)."""
    pattern: SurfacePattern
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
    SigmaNamed | Record | Subtype | RecordValue | Block | Sum | List |
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