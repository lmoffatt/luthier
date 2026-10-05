"""Abstract syntax of Luthier terms, patterns and definitions.

The interpreter keeps the syntax as Python dataclasses. The language-level
`Term` datatype (code as data inside Luthier) is not part of version 0.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


class Term:
    pass


@dataclass(frozen=True)
class Var(Term):
    name: str

    def __repr__(self): return self.name


@dataclass(frozen=True)
class Lit(Term):
    value: object  # int, float or str

    def __repr__(self):
        return repr(self.value) if isinstance(self.value, str) else str(self.value)


@dataclass(frozen=True)
class Univ(Term):
    def __repr__(self): return "U"


@dataclass(frozen=True)
class Lam(Term):
    param: "Pattern"
    body: Term
    ann: Optional[Term] = None  # optional annotation of the parameter type
    res: Optional[Term] = None  # the result type the body was checked against, kept by elaboration


@dataclass(frozen=True)
class App(Term):
    fn: Term
    arg: Term


@dataclass(frozen=True)
class Pi(Term):
    name: str
    dom: Term
    cod: Term


@dataclass(frozen=True)
class Sigma(Term):
    name: str
    fst: Term
    snd: Term


@dataclass(frozen=True)
class Primitive(Term):
    """`primitive "description"`: a type the interpreter provides (06 §2). `base` is the type it
    refines (`Float64 : Real`), None for a type of its own."""
    desc: str
    base: Optional[Term] = None


@dataclass(frozen=True)
class Axiom(Term):
    """`axiom "description"`: a value whose laws are assumed, never tested (06 §3)."""
    desc: str


@dataclass(frozen=True)
class Sum(Term):
    """`< a : A | b : B >`, `(a : A) + (b : B)`, `A + B`: the primitive sum (04 §2). Structural:
    the labels are binders and two sums with the same alternative types, in order, are the
    same type. `alts` is a tuple of (label, type)."""
    alts: tuple

    def labels(self) -> list:
        return [l for l, _ in self.alts]


@dataclass(frozen=True)
class Inj(Term):
    """Injection into alternative `index` of a sum, written with its label. `type` is the sum
    type it was elaborated against, kept so an elaborated term can be typed again."""
    index: int
    label: str
    arg: Term
    type: Optional[Term] = None


@dataclass(frozen=True)
class NoLaw(Term):
    """The predicate of a labeled product: `{ a : A, b : B }` is `Subtype((a, b), A * B, NoLaw())`.
    It states nothing; the subtype is the product with names for its positions."""
    def __repr__(self): return "nolaw"


@dataclass(frozen=True)
class Named(Term):
    """`(x : A)` alone, before elaboration: a named position of a product or a sum."""
    name: str
    type: Term


@dataclass(frozen=True)
class Pair(Term):
    fst: Term
    snd: Term


@dataclass(frozen=True)
class Arrow(Term):
    """`a -> b` before elaboration: Pi if `a` is a type, implication if `a : Bool`."""
    lhs: Term
    rhs: Term


@dataclass(frozen=True)
class BinOp(Term):
    """Infix operator before elaboration. `*` may become Sigma."""
    op: str
    lhs: Term
    rhs: Term


@dataclass(frozen=True)
class Con(Term):
    """Reference to a data constructor."""
    name: str

    def __repr__(self): return self.name


@dataclass(frozen=True)
class Extern(Term):
    """A hole filled by the environment, by name. `provisional`: written `extern provisional`,
    exempt from the requirement that the types it builds on be defined (05 R5)."""
    target: str
    type: Optional[Term] = None
    provisional: bool = False


@dataclass(frozen=True)
class Subtype(Term):
    """{ pat : base | pred }"""
    param: "Pattern"
    base: Term
    pred: Term


@dataclass(frozen=True)
class Match(Term):
    scrut: Term
    branches: tuple  # tuple[tuple[Pattern, Term], ...]


@dataclass(frozen=True)
class And(Term):
    """Conjunction of quantified laws: `p & q`."""
    lhs: Term
    rhs: Term


@dataclass(frozen=True)
class Forget(Term):
    """`forget x`: the value of a subtype, seen in its base type."""
    arg: Term


@dataclass(frozen=True)
class RecordLit(Term):
    """`{ a := x, b := y }`: a value of a type with named components, given by name. It takes
    its shape from the type it is checked against and elaborates to the pair chain."""
    fields: tuple  # of (name, Term)


@dataclass(frozen=True)
class Proj(Term):
    """`t.field` before elaboration: a component of a value whose type names its components.
    Elaborates to a one-branch match on the type's component pattern."""
    term: Term
    field: str


# ---------------------------------------------------------------- patterns

class Pattern:
    pass


@dataclass(frozen=True)
class PVar(Pattern):
    name: str

    def __repr__(self): return self.name


@dataclass(frozen=True)
class PWild(Pattern):
    def __repr__(self): return "_"


@dataclass(frozen=True)
class PCon(Pattern):
    name: str
    args: tuple  # tuple[Pattern, ...]


@dataclass(frozen=True)
class PPair(Pattern):
    fst: Pattern
    snd: Pattern


@dataclass(frozen=True)
class PLit(Pattern):
    value: object


@dataclass(frozen=True)
class PInj(Pattern):
    """A label of a sum applied to a pattern for its payload (`PWild` for a Unit alternative)."""
    index: int
    label: str
    arg: Pattern


def pattern_vars(p: Pattern) -> list[str]:
    if isinstance(p, PVar):
        return [p.name]
    if isinstance(p, PCon):
        out = []
        for a in p.args:
            out += pattern_vars(a)
        return out
    if isinstance(p, PPair):
        return pattern_vars(p.fst) + pattern_vars(p.snd)
    if isinstance(p, PInj):
        return pattern_vars(p.arg)
    return []


# ------------------------------------------------------------- definitions

@dataclass
class Constructor:
    name: str
    type: Term  # as written, with the data's parameters in scope


@dataclass
class DataDecl:
    name: str
    params: list  # list[tuple[str, Term]]
    constructors: list  # list[Constructor]


@dataclass
class Def:
    name: str
    type: Optional[Term]  # None: to be inferred
    body: Optional[Term]  # None: hole
    data: Optional[DataDecl] = None
    doc: str = ""
    alias: bool = False   # `name = term`: expanded wherever it is used; no states (05 R7)
    line: int = 0
    pending: bool = False  # a declared type `T : base` whose laws are not given yet: its body is
                           # the labeled base, so the laws can be written over it (05 §1)


@dataclass
class TestDirective:
    name: str
    n: int = 100
    exhaustive: bool = False
    size: Optional[int] = None    # largest size of generated values; None: the runner's default


@dataclass
class OperatorDirective:
    """`operator + := f`: the binary function f gives `+` its meaning for the types of f's two
    arguments. Kept in the order of the definitions, so later definitions can use it."""
    op: str
    term: Term
    line: int = 0

    @property
    def name(self) -> str:
        return f"operator {self.op}"


@dataclass
class GenDirective:
    """`gen T := term` chooses a Luthier generator (of type Gen T) for values of T;
    `gen T := extern "python:mod.fn"` a Python one, called as fn(rng, size)."""
    type_name: str
    target: Optional[str] = None
    term: Optional[Term] = None


@dataclass
class ImportDirective:
    path: str
    alias: Optional[str] = None   # `import "x" as m`: definitions are reached as m.name
    line: int = 0


@dataclass
class Program:
    defs: list = field(default_factory=list)
    tests: list = field(default_factory=list)
    gens: list = field(default_factory=list)
    imports: list = field(default_factory=list)

    def find(self, name: str) -> Optional[Def]:
        for d in self.defs:
            if d.name == name:
                return d
        return None
