"""Frozen kernel data from term.lth §1 (not the surface syntax trees).

Source revision: 0a497e50b61aad3d04975bcb4ff3157c7db5bc7c.
Derivation: record/IA/kernel-2026-10-13/prompt.md v1; Codex, 2026-10-13.
Lists are tuples, Maybe is None; constructors retain the theory's argument order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True)
class IntConst:
    value: int


@dataclass(frozen=True)
class FloatConst:
    value: float


@dataclass(frozen=True)
class StringConst:
    value: str


Constant: TypeAlias = IntConst | FloatConst | StringConst


@dataclass(frozen=True)
class PVar:
    name: str


@dataclass(frozen=True)
class PWild:
    pass


@dataclass(frozen=True)
class PCon:
    name: str
    patterns: tuple[Pattern, ...]


@dataclass(frozen=True)
class PPair:
    left: Pattern
    right: Pattern


@dataclass(frozen=True)
class PLit:
    constant: Constant


@dataclass(frozen=True)
class PInj:
    label: str
    pattern: Pattern


Pattern: TypeAlias = PVar | PWild | PCon | PPair | PLit | PInj


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Lit:
    constant: Constant


@dataclass(frozen=True)
class Universe:
    pass


@dataclass(frozen=True)
class World:
    pass


@dataclass(frozen=True)
class Lam:
    name: str
    type: Term
    body: Term


@dataclass(frozen=True)
class App:
    function: Term
    argument: Term


@dataclass(frozen=True)
class Pi:
    name: str
    domain: Term
    codomain: Term


@dataclass(frozen=True)
class Sigma:
    name: str
    domain: Term
    codomain: Term


@dataclass(frozen=True)
class Pair:
    left: Term
    right: Term


@dataclass(frozen=True)
class Match:
    value: Term
    arms: tuple[tuple[Pattern, Term], ...]


@dataclass(frozen=True)
class Inj:
    label: str
    value: Term


@dataclass(frozen=True)
class Sum:
    alternatives: tuple[tuple[str, Term], ...]


@dataclass(frozen=True)
class Data:
    name: str
    constructors: tuple[tuple[str, Term], ...]


@dataclass(frozen=True)
class Subtype:
    name: str
    type: Term
    predicate: Term


@dataclass(frozen=True)
class Extern:
    route: str


@dataclass(frozen=True)
class Primitive:
    name: str


@dataclass(frozen=True)
class Axiom:
    pass


@dataclass(frozen=True)
class Hole:
    name: str


Term: TypeAlias = (
    Var | Lit | Universe | World | Lam | App | Pi | Sigma | Pair | Match | Inj |
    Sum | Data | Subtype | Extern | Primitive | Axiom | Hole
)


@dataclass(frozen=True)
class Declare:
    name: str
    type: Term


@dataclass(frozen=True)
class Define:
    name: str
    type: Term
    body: Term


@dataclass(frozen=True)
class Datum:
    value: Term


Act: TypeAlias = Declare | Define | Datum
Program: TypeAlias = tuple[Act, ...]
