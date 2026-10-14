"""Demand-driven host runner. Sources: spec 10.S2–S10, world_model.lut (0c920f0).

Derivation: user request 2026-10-13, implementation v1 (record/IA/run-2026-10-13/codex.md);
v2 for world.lth draft 1 (prompt-2.md, choices in opus-2.md): the bridge carries `Maybe`
(host.Just, host.NOTHING) and records (a dict). v4 (prompt-4.md, choices in report-4.md): the
bridge reads by the type the extern's definition declares (spec 3.S22 to 3.S26, 11.S6 to 11.S9):
`Vec`/`Mat` records and `Fin n -> Float64`/`Int` as ndarrays, `Float64` and `Int` checked,
`Table` as tables.py reads it, sums as `(label, value)`. v5 (prompt-5.md, report-5.md): every
run loads `lib/core.lut` before the file (12.S22, 11.R2), defines kernel.BOOTSTRAP_PRIMITIVES as
`eval` does, and the Runner brings the operands of a primitive and of `and`/`or` to weak head
normal form itself, with the host. v6 (prompt-6.md): the loader scopes each file's names by the
file (12.S22, `Loaded`), and an extern's arity is read from its declared type, the host's signature
only when no type is declared. v7 (prompt-7.md): `--set name=value` fills a hole of the file run
(3.S9, 12.S18), and each run appends its entry, time, parameters and output to `x.run.json`.
v8 (prompt-8.md, D-2026-10-14-a, 3.S23): a Luthier function handed to the host at a function type
over an infinite domain is a callback, each call counted per receiving route and position and
written to `x.run.json` (world.lth's `Crossing`); a record of functions crosses field by field; a
host function that crossed in is applied only through the bridge; an extern applied to fewer
arguments than its arity stays a value, and crossing out it is a `functools.partial` of the
host's function. v9 (prompt-9.md, 8.S4): a bound value is demanded once within a run (call by
need): a `Let`'s value, an argument of a lambda, a part a pattern binds and a constant of the
program stand as one `Shared` cell, reduced at the first demand and kept; `kernel.step` unchanged.
v10 (prompt-10.md, 12.S22): a constructor or a label of a sum and another file's definition of the
same name are kept apart (the definition is `name@file`). v12 (prompt-12.md): the arity a host
function's Python signature gives is read once per function. v13 (record/IA/certification-2026-10-14/
prompt-run.md, certification.lth §3, 12.S17, 7.S15): before evaluating, `run` reads the stores of
the files loaded and refuses a cone that is not certified (`certification`, `Refused`), with no
opt-out (D-2026-10-12-y); the record carries the cone's certification state (12.S18).
"""
from __future__ import annotations

import functools
import importlib
import inspect
import json
import math
import platform
from dataclasses import dataclass, field, fields, is_dataclass, replace
from pathlib import Path

import numpy as np

from . import host, kernel, surface as s, term as t
from .elaborate import elaborate_program
from .parse import parse
from .surface import Parsed


class RunError(ValueError):
    pass


# the core encloses the top-level scope of every file (12.S22); its data and `not` are read here
CORE = Path(__file__).parent / "lib" / "core.lut"


_FREE = {"extern", "primitive", "axiom", "quote"}
_BUILTIN_CONSTRUCTORS = {"true", "false", "nil", "cons", "just", "nothing", "ok", "failed"}


def _defines(act):
    """The names an act defines: its own, and a data's constructors."""
    if not isinstance(act, (s.Define, s.Declare, s.Alias)):
        return []
    names = [act.name]
    if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
        names += [n for n, _ in act.body.constructors]
    return names


def _sum_labels(value, out):
    if isinstance(value, s.Sum):
        out.update(n for n, _ in value.alternatives)
    if isinstance(value, tuple):
        for v in value:
            _sum_labels(v, out)
    elif is_dataclass(value) and not isinstance(value, type):
        for f in fields(value):
            _sum_labels(getattr(value, f.name), out)
    return out


class FileScope:
    """An act of a file with its names as a program calls them: what it defines by `internal`, each
    free name it uses by `reference`, each pattern by `pattern` (which gives the names it binds, so
    that a binder shadows a definition of the same name). `Loaded` resolves them for a run; check.py's
    `load_imports` for the typing of an importer's imports (12.S22)."""

    def scoped(self, f, act):
        """An act of the file with each name it defines and each free name it uses in the program's
        names; a name it cannot resolve is left as written and recorded against the act."""
        path = f.path
        missing = []
        if isinstance(act, (s.Define, s.Declare, s.Alias)):
            bound = set()
            binders = []
            for b in act.binders:
                b = replace(b, type=self.rename(path, b.type, bound, missing),
                            **({"default": self.rename(path, b.default, bound, missing)} if isinstance(b, s.Explicit) else {}))
                binders.append(b)
                bound |= set(b.names)
            changes = {"name": self.internal(path, act.name), "binders": tuple(binders)}
            if isinstance(act, s.Alias):
                changes["value"] = self.rename(path, act.value, bound, missing)
            else:
                changes["type"] = self.rename(path, act.type, bound, missing)
            if isinstance(act, s.Define):
                body = act.body
                if isinstance(body, s.DataBody):
                    body = s.DataBody(tuple((self.internal(path, n), self.rename(path, ty, bound, missing))
                                            for n, ty in body.constructors))
                else:
                    body = self.rename(path, body, bound, missing)
                changes["body"] = body
            result = replace(act, **changes)
            if missing:
                self.errors.setdefault(result.name, []).extend(missing)
            return result
        return self.rename(path, act, set(), missing)

    def rename(self, path, value, bound, missing):
        """`value` with its free names resolved in the file at `path`; binders followed as
        check.py's `names` follows them."""
        r = lambda v, b=bound: self.rename(path, v, b, missing)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, tuple):
            return tuple(r(v) for v in value)
        if isinstance(value, s.Name):
            root, dot, rest = value.name.partition(".")
            if root in bound:
                return value
            return s.Name(self.reference(path, root, missing) + dot + rest)
        if isinstance(value, (s.Pi, s.Sigma)):
            return replace(value, domain=r(value.domain), codomain=r(value.codomain, bound | set(value.names)))
        if isinstance(value, s.SigmaNamed):
            return replace(value, left_type=r(value.left_type), right_type=r(value.right_type, bound | {value.left_name}))
        if isinstance(value, s.Subtype):
            pattern, binds = self.pattern(path, value.pattern, missing)
            return s.Subtype(pattern, r(value.type), r(value.law, bound | binds))
        if isinstance(value, s.Record):
            inner, out = set(bound), []
            for fl in value.fields:
                out.append(replace(fl, type=r(fl.type, set(inner))))
                inner |= set(fl.names)
            return s.Record(tuple(out), r(value.law, inner))
        if isinstance(value, (s.Block, s.Lambda)):
            inner = set(bound)
            params = []
            if isinstance(value, s.Lambda):
                for q in value.params:
                    if isinstance(q, s.TypedParam):
                        q = replace(q, type=r(q.type, set(inner)))
                        inner |= set(q.names)
                    elif isinstance(q, s.PlainParam):
                        inner.add(q.name)
                    else:
                        patterns = []
                        for p in q.patterns:
                            p, binds = self.pattern(path, p, missing)
                            patterns.append(p)
                            inner |= binds
                        q = s.ShapeParam(tuple(patterns))
                    params.append(q)
            items = []
            for it in value.items:
                v = r(it.value, set(inner))
                if isinstance(it, s.Bind):
                    items.append(s.Bind(it.name, v))
                    inner.add(it.name)
                else:
                    p, binds = self.pattern(path, it.pattern, missing)
                    items.append(s.Rebind(p, v))
                    inner |= binds
            if isinstance(value, s.Block):
                return s.Block(tuple(items), r(value.value, inner))
            return s.Lambda(tuple(params), tuple(items), r(value.body, inner))
        if isinstance(value, s.MatchOf):
            arms = []
            for p, body in value.arms:
                p, binds = self.pattern(path, p, missing)
                arms.append((p, r(body, bound | binds)))
            return s.MatchOf(r(value.value), tuple(arms))
        if isinstance(value, s.Clause):
            patterns, binds = [], set()
            for p in value.patterns:
                p, b = self.pattern(path, p, missing)
                patterns.append(p)
                binds |= b
            return s.Clause(tuple(patterns), r(value.body, bound | binds))
        if isinstance(value, s.RecordValue):
            return s.RecordValue(tuple((label, r(v)) for label, v in value.fields))
        if isinstance(value, s.Sum):
            return s.Sum(tuple((label, r(v)) for label, v in value.alternatives))
        if isinstance(value, s.NamedArg):
            return s.NamedArg(value.name, r(value.value))
        if isinstance(value, s.Proj):
            return s.Proj(r(value.value), value.field)
        if is_dataclass(value) and not isinstance(value, type):
            return replace(value, **{fl.name: r(getattr(value, fl.name)) for fl in fields(value)
                                     if not isinstance(getattr(value, fl.name), str)})
        return value


@dataclass
class _File:
    path: Path
    tag: str = ""
    acts: list = field(default_factory=list)
    defined: set = field(default_factory=set)
    constructors: set = field(default_factory=set)
    labels: set = field(default_factory=set)      # the labels of the sums its acts write
    imports: dict = field(default_factory=dict)   # the name the file sees -> (file, the name there)


class Loaded(FileScope):
    """The files a run reads from `path` (and core), each act's names scoped by its file (12.S22).

    A file sees its own definitions, the names its imports list (each under its alias, a model
    under the name it is imported by), and core's, in that order; nothing else of what it imports
    or of what they import. A name two files define does not collide: each reference resolves in
    its own file. Inside the program a definition keeps its name when no other file defines it, or
    when its file is the one run (then core); otherwise it is called `name@file` (the file's stem),
    which the user never writes. A constructor (of a data, or a label of a sum) and a definition of
    the same name are different names too: the definition is then always `name@file`, the labels
    keeping their written names, global as the elaborator and the bridge read them (prompt-10.md).
    A constructor reference resolves as a definition's does: the file's own data and sums, then the
    names its imports list, then core. A reference a file cannot resolve is an error naming the
    file, raised only when a demand reaches the act that makes it (12.S21)."""

    def __init__(self, path, core=True):
        self.files = {}
        self.top = Path(path).resolve()
        self.core = CORE.resolve() if core else None
        if core:
            self.visit(self.core, set())
        self.visit(self.top, set())
        definers = {}
        for f in self.files.values():
            for n in f.defined:
                definers.setdefault(n, []).append(f.path)
        self.plain = {}
        for n, fs in definers.items():
            for owner in (self.top, self.core):
                if owner in fs:
                    self.plain[n] = owner
                    break
            else:
                if len(fs) == 1:
                    self.plain[n] = fs[0]
        self.labels = _sum_labels(tuple(a for f in self.files.values() for a in f.acts), set())
        # a definition that is not a constructor never keeps the name of a constructor or a label
        reserved = self.labels | _BUILTIN_CONSTRUCTORS | {n for f in self.files.values() for n in f.constructors}
        for n in reserved & set(self.plain):
            if n not in self.files[self.plain[n]].constructors:
                del self.plain[n]
        stems = {}
        for f in self.files.values():
            k = stems.setdefault(f.path.stem, 0)
            stems[f.path.stem] = k + 1
            f.tag = f.path.stem if k == 0 else f"{f.path.stem}~{k}"
        self.memo = {}
        self.errors = {}   # the internal name of an act -> what it cannot resolve
        # each file's acts in the program's names, imports before importers, core first
        self.by_file = {path: tuple(self.scoped(f, a) for a in f.acts) for path, f in self.files.items()}
        self.acts = tuple(a for acts in self.by_file.values() for a in acts)

    def visit(self, path, active):
        path = path.resolve()
        if path in active:
            raise RunError(f"cyclic import: {path}")
        if path in self.files:
            return
        result = parse(path.read_text(encoding="utf-8"))
        if isinstance(result, s.ParseFailed):
            raise RunError("; ".join(f"{path}:{e.line}:{e.column}: {e.message}" for e in result.errors))
        active.add(path)
        f = _File(path)
        for act in result.program:
            if isinstance(act, s.ImportAct):
                target = path.parent / act.path
                if not target.exists():
                    target = Path(__file__).parent / "lib" / act.path
                if not target.exists():
                    raise RunError(f"{path.name}: no file {act.path} to import")
                self.visit(target, active)
                for name in act.names:
                    f.imports[name.asName or name.name] = (target.resolve(), name.name)
            else:
                f.acts.append(act)
                f.defined.update(_defines(act))
                if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
                    f.constructors.update(n for n, _ in act.body.constructors)
                _sum_labels(act, f.labels)
        active.remove(path)
        self.files[path] = f

    def internal(self, path, name):
        """The program's name of the definition of `name` in the file at `path`; a label of a sum
        of the file keeps its name."""
        if self.is_label(path, name):
            return name
        return name if self.plain.get(name) == path else f"{name}@{self.files[path].tag}"

    def is_label(self, path, name):
        f = self.files[path]
        return name in f.labels and name not in f.defined

    def see(self, path, name):
        """(file, name there) of the definition a reference to `name` in the file means, None when
        the file neither defines, nor imports, nor finds it in core; RunError when an import lists a
        name its file does not give."""
        key = (path, name)
        if key in self.memo:
            if self.memo[key] is _VISITING:
                raise RunError(f"{path.name}: {name} is imported in a cycle")
            return self.memo[key]
        self.memo[key] = _VISITING
        f = self.files[path]
        try:
            if name in f.defined or name in f.labels:
                # its own definitions, then the labels of its own sums
                found = (path, name)
            elif name in f.imports:
                target, there = f.imports[name]
                found = self.see(target, there)
                if found is None:
                    raise RunError(f"{path.name} imports {there} from {target.name}, which does not define it")
            elif self.core is not None and path != self.core and name in self.files[self.core].defined:
                found = (self.core, name)
            else:
                found = None
        except RunError:
            del self.memo[key]
            raise
        self.memo[key] = found
        return found

    def name(self, path, name):
        """`name` as the file at `path` writes it, as the program calls it; None when not seen."""
        path = Path(path).resolve()
        if path not in self.files:
            return None
        try:
            found = self.see(path, name)
        except RunError:
            return None
        return None if found is None else self.internal(*found)

    def is_constructor(self, path, name):
        try:
            found = self.see(path, name)
        except RunError:
            return False
        if found is None:
            return name in _BUILTIN_CONSTRUCTORS
        return found[1] in self.files[found[0]].constructors

    def pattern(self, path, p, missing):
        """A pattern with its constructors in the program's names, and the names it binds."""
        if isinstance(p, s.PApp):
            if p.patterns or self.is_constructor(path, p.name):
                out, binds = [], set()
                for q in p.patterns:
                    q, b = self.pattern(path, q, missing)
                    out.append(q)
                    binds |= b
                return s.PApp(self.constructor(path, p.name, missing), tuple(out)), binds
            return p, {p.name}
        if isinstance(p, s.PTuple):
            out, binds = [], set()
            for q in p.patterns:
                q, b = self.pattern(path, q, missing)
                out.append(q)
                binds |= b
            return s.PTuple(tuple(out)), binds
        return p, set()

    def constructor(self, path, name, missing):
        """A pattern's head: a constructor or a label the file sees, else a label of any file (global,
        as the elaborator reads it), else whatever the name resolves to."""
        try:
            found = self.see(path, name)
        except RunError:
            found = None
        if found is not None and (found[1] in self.files[found[0]].constructors or self.is_label(*found)):
            return self.internal(*found)
        if name in self.labels:
            return name
        return self.reference(path, name, missing)

    def reference(self, path, name, missing):
        try:
            found = self.see(path, name)
        except RunError as exc:
            missing.append(str(exc))
            return name
        if found is not None:
            return self.internal(*found)
        if name not in self.labels and name not in _FREE and name not in _BUILTIN_CONSTRUCTORS \
                and name not in kernel.BOOTSTRAP_PRIMITIVES:
            missing.append(f"{path.name}: {name} is neither defined there, nor imported, nor core's")
        return name

    def demand(self, acts):
        """RunError when an act the run keeps uses a name its file cannot resolve (12.S22)."""
        for a in acts:
            for message in self.errors.get(getattr(a, "name", None), ()):
                raise RunError(message)


_VISITING = object()


@dataclass(frozen=True)
class TypedExtern(t.Extern):
    """An extern with the type its definition declares, so the bridge reads its arguments and its
    result by type (11.S6); with `obj`, a host object that crossed into the kernel (3.S22), applied
    like an extern, its route a name of this run only. `arity`, how many arguments the host's
    function takes, is read from the declared type (`Runner.typed`); None for a host object, whose
    arity is its Python signature's."""
    type: object = None
    obj: object = field(default=None, compare=False, hash=False)
    arity: int | None = field(default=None, compare=False, hash=False)


class Entries:
    """A host array as a value of `Fin n -> A` (3.S21): `v i` is `v[i]`, the interpreter checking
    `0 <= i < n` itself, since numpy would accept `v[-1]` (3.S22)."""
    def __init__(self, array):
        self.array = array

    def __call__(self, i):
        if type(i) is not int or not 0 <= i < len(self.array):
            raise RunError(f"index {i!r} outside Fin {len(self.array)}")
        return self.array[i]


class HostRecord(dict):
    """A Luthier record on the host's side: its fields by key and as attributes (tables.as_table)."""
    def __getattr__(self, label):
        try:
            return self[label]
        except KeyError:
            raise AttributeError(label) from None


@dataclass(frozen=True, eq=False, repr=False)
class Shared(t.Axiom):
    """A bound value demanded once (8.S4, call by need): a closed term the Runner reduces to weak
    head normal form at its first demand and keeps for every later one. It stands where the term
    would be substituted (a `Let`'s value, an argument of a lambda, a part a pattern binds, a
    constant of the program), so every copy the substitution makes is this one object. To the
    kernel it is an opaque leaf (`Axiom`), with no free names, so `kernel.step` and the
    substitution pass it on untouched; only the Runner looks inside. `cell` is [term, forced]."""
    cell: list = field(default_factory=list)

    __eq__ = object.__eq__
    __hash__ = object.__hash__

    def __repr__(self):
        return f"Shared({self.cell[0]!r})"


_UNTYPED = object()
_INTS = ("Int", "Nat")
_NAMED = {"Float64", "String", "Unit", "Bool"} | set(_INTS)
_INT64 = (-2 ** 63, 2 ** 63)
# the type families the bridge reads by name, never unfolded (`Fin n` is an index, 3.S21)
_READ_BY_NAME = {"Fin", "Maybe", "List"}


def _applied(ty, name):
    """The argument of `name X` (`Maybe X`, `List X`, `Fin n`), or None."""
    if isinstance(ty, t.App) and ty.function == t.Var(name):
        return ty.argument
    return None


def _arrow(ty):
    """(binder, domain, codomain) of a function type, written `Pi` or `A -> B` (`implies`)."""
    if isinstance(ty, t.Pi):
        return ty.name, ty.domain, ty.codomain
    if isinstance(ty, t.App) and isinstance(ty.function, t.App) and ty.function.function == t.Var("implies"):
        return "_", ty.function.argument, ty.argument
    return None


def _same(a, b):
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return a is b
    return a == b


def _instantiate(name, value, ty):
    return ty if name == "_" else kernel.substitute(name, value, ty)


def _extern_of(body):
    """The extern a definition's body is, or applies to exactly its parameters, or None."""
    names = []
    while isinstance(body, t.Lam):
        names.append(body.name)
        body = body.body
    args = []
    while isinstance(body, t.App):
        args.append(body.argument)
        body = body.function
    if isinstance(body, t.Extern) and not isinstance(body, TypedExtern) and args[::-1] == [t.Var(n) for n in names]:
        return body
    return None


def _parameters(body):
    """How many lambdas a definition's body opens with: the parameters an extern is applied to."""
    count = 0
    while isinstance(body, t.Lam):
        count, body = count + 1, body.body
    return count


def _family(act):
    """(parameters, body) of a type family: a definition of a function into `U` by as many
    lambdas (`VecOf (k : Int) : U := { v : Vec Float64 | v.n == k }`), or a theory declared over
    parameters (`Objective (n : Nat) : { value : VecOf n -> Float64, ... }`); None otherwise."""
    names, ty = [], act.type
    while isinstance(ty, t.Pi):
        names.append(ty.name)
        ty = ty.codomain
    if not names:
        return None
    if isinstance(act, t.Declare):
        return (names, ty) if isinstance(ty, t.Record) else None
    if ty != t.Universe():
        return None
    body = act.body
    for name in names:
        if not isinstance(body, t.Lam):
            return None
        body = kernel.substitute(body.name, t.Var(name), body.body) if body.name != name else body.body
    return None if isinstance(body, t.Data) else (names, body)


def _with_extern(body, typed):
    if isinstance(body, t.Lam):
        return replace(body, body=_with_extern(body.body, typed))
    if isinstance(body, t.App):
        return replace(body, function=_with_extern(body.function, typed))
    return typed


class Runner:
    def __init__(self, program, fuel):
        self.fuel = fuel
        # An opaque kernel leaf stands for the host-owned identity for this run.
        self.token = t.Axiom("host world token")
        self.routes = {}
        # the arity of each host function read from its Python signature (`arity`)
        self.signatures = {}
        self.objects = 0
        # the types the bridge resolves names to: a type definition's body, a theory's record
        self.types = {}
        # the type families, by their parameters: `VecOf (k : Int) : U := ...`, `Objective (n : Nat) : { ... }`
        self.families = {}
        for act in program:
            if isinstance(act, t.Define) and act.type == t.Universe() and not isinstance(act.body, t.Lam):
                self.types[act.name] = act.body
            elif isinstance(act, t.Declare) and isinstance(act.type, t.Record):
                self.types[act.name] = act.type
            if (isinstance(act, (t.Define, t.Declare)) and act.name not in _READ_BY_NAME
                    and (family := _family(act)) is not None):
                self.families[act.name] = family
        self.program = tuple(self.typed(act) for act in program)
        self.defined = {act.name for act in program if isinstance(act, (t.Define, t.Declare))}
        # [proposed] a constant (a definition whose body is not a lambda) is demanded once per run
        # too: its body is closed, so its value is one, wherever its name is reached (8.S4). The
        # first definition of a name wins, as in kernel.step's environment.
        self.constants = {}
        for act in self.program:
            if isinstance(act, t.Define) and not isinstance(act.body, t.Lam):
                self.constants.setdefault(act.name, self.share(act.body))

    def typed(self, act):
        """The definition with each extern it gives carrying its declared type: `f (x : A) : B :=
        extern "..." x`, or a record of a declared theory whose fields are externs (3.S40)."""
        if not isinstance(act, t.Define) or act.type is None or isinstance(act.type, t.Hole):
            return act  # no type declared (the elaborator's hole): the host's signature decides
        extern = _extern_of(act.body)
        if extern is not None:
            arity = _parameters(act.body) or self.arity_of(act.type)
            return replace(act, body=_with_extern(act.body, TypedExtern(extern.route, act.type, arity=arity)))
        record = self.resolve(act.type)
        if isinstance(act.body, t.RecordValue) and isinstance(record, t.Record):
            types = dict(record.fields)
            items = []
            for label, value in act.body.fields:
                extern = _extern_of(value)
                if extern is not None and label in types:
                    arity = _parameters(value) or self.arity_of(types[label])
                    value = _with_extern(value, TypedExtern(extern.route, types[label], arity=arity))
                items.append((label, value))
            return replace(act, body=t.RecordValue(tuple(items)))
        return act

    def arity_of(self, ty):
        """The arguments an extern of declared type `ty` takes when its definition binds none
        (`log := extern "python:math.log"` at `Float64 -> Float64`): the arrows of the type up to
        the first whose domain is `Fin` (what follows is an array the host gives, 3.S23), every
        arrow when the first one's is."""
        count, arrows = 0, []
        while (arrow := _arrow(self.resolve(ty))) is not None:
            arrows.append(_applied(self.resolve(arrow[1]), "Fin") is not None)
            ty = arrow[2]
        if arrows and not arrows[0]:
            while count < len(arrows) and not arrows[count]:
                count += 1
            return count
        return len(arrows)

    def arity(self, head, function):
        """How many arguments the host's function takes: the declared type's (`TypedExtern`);
        with no type declared, its Python signature; a builtin without one, one."""
        if getattr(head, "arity", None) is not None:
            return head.arity
        if isinstance(function, Entries):
            return 1  # its signature, `(i)`, read without inspect (prompt-12.md)
        # a function's signature does not change: read once per function (prompt-12.md)
        try:
            return self.signatures[function]
        except KeyError:
            pass
        except TypeError:  # an unhashable callable: read each time
            return self.signature_arity(function)
        arity = self.signatures[function] = self.signature_arity(function)
        return arity

    @staticmethod
    def signature_arity(function):
        try:
            return len(inspect.signature(function).parameters)
        except (TypeError, ValueError):
            return 1

    def resolve(self, ty):
        """A type with its names unfolded and its refinements dropped, down to what the bridge
        reads: the named primitives, `Maybe`, `List`, `Fin`, functions, pairs, sums, records."""
        while True:
            if isinstance(ty, t.Subtype):
                ty = ty.type
            elif isinstance(ty, t.Var) and ty.name not in _NAMED and ty.name in self.types:
                ty = self.types[ty.name]
            elif (applied := self.family_applied(ty)) is not None:
                ty = applied
            else:
                return ty

    def family_applied(self, ty):
        """A type family applied to as many arguments as it has parameters, its body with them put
        for the parameters (`VecOf 2` the vectors of length 2, `Objective n` its record); None for
        any other type."""
        args, head = [], ty
        while isinstance(head, t.App):
            args.append(head.argument)
            head = head.function
        if not (isinstance(head, t.Var) and head.name in self.families):
            return None
        names, body = self.families[head.name]
        if len(args) != len(names):
            return None
        for name, arg in zip(names, reversed(args)):
            body = _instantiate(name, arg, body)
        return body

    def spend(self):
        if self.fuel <= 0:
            raise RunError("fuel spent")
        self.fuel -= 1

    def route(self, head):
        if getattr(head, "obj", None) is not None:
            return head.obj
        route = head.route
        if route not in self.routes:
            if not route.startswith("python:"):
                raise RunError(f"unsupported extern route: {route}")
            module, name = route[7:].rsplit(".", 1)
            self.routes[route] = getattr(importlib.import_module(module), name)
        return self.routes[route]

    def host_object(self, obj, ty):
        """A host function or array as a kernel leaf, applied through the bridge (3.S22)."""
        self.objects += 1
        return TypedExtern(f"host:{self.objects}", ty, obj)

    def size(self, domain):
        """n of `Fin n`, evaluated, or None."""
        bound = _applied(self.resolve(domain), "Fin")
        if bound is None:
            return None
        bound = self.whnf(bound)
        if isinstance(bound, t.Lit) and isinstance(bound.constant, t.IntConst):
            return bound.constant.value
        raise RunError(f"the length of {domain!r} is not known at the crossing")

    # ------------------------------------------------------------------ to the host

    def to_host(self, value, ty=None, at=None):
        """`value` as the host receives it, at the declared type `ty` when there is one. `at` is
        (route, position): the extern receiving it and where among its arguments, the key under
        which the calls of a callback are counted (12.S18)."""
        value = self.whnf(value)
        if value is self.token or value == self.token:
            return self.token
        if isinstance(value, TypedExtern) and value.obj is not None:
            # a host object goes back as it came (an array, a method of a host table)
            return value.obj.array if isinstance(value.obj, Entries) else value.obj
        partial = self.host_partial(value)
        if partial is not None:
            return partial
        if ty is not None:
            result = self.typed_to_host(value, self.resolve(ty), at)
            if result is not _UNTYPED:
                return result
        if isinstance(value, t.Lit):
            return value.constant.value
        if value == t.Var("unit"):
            return None
        if value in (t.Var("true"), t.Var("false")):
            return value == t.Var("true")
        if value == t.Var("nothing"):
            return host.NOTHING
        if isinstance(value, t.App) and value.function == t.Var("just"):
            return host.Just(self.to_host(value.argument))
        if value == t.Var("nil"):
            return []
        if (isinstance(value, t.App) and isinstance(value.function, t.App)
                and value.function.function == t.Var("cons")):
            return [self.to_host(value.function.argument)] + self.to_host(value.argument)
        if isinstance(value, t.Pair):
            return self.to_host(value.left), self.to_host(value.right)
        if isinstance(value, t.RecordValue):
            return {label: self.to_host(field) for label, field in value.fields}
        raise RunError(f"unsupported extern argument: {value!r}")

    def typed_to_host(self, value, ty, at=None):
        name = ty.name if isinstance(ty, t.Var) else None
        if name == "Float64":
            # 11.S6: a float, an integer with an exact double promoted; 11.S7: never NaN or inf
            if isinstance(value, t.Lit) and type(value.constant.value) in (int, float):
                return self.float64(value.constant.value)
            raise RunError(f"not a Float64 at the crossing: {value!r}")
        if name in _INTS or _applied(ty, "Fin") is not None:
            if not (isinstance(value, t.Lit) and isinstance(value.constant, t.IntConst)):
                raise RunError(f"not an Int at the crossing: {value!r}")
            n = self.size(ty)
            if n is not None and not 0 <= value.constant.value < n:
                raise RunError(f"index {value.constant.value} outside Fin {n}")
            return value.constant.value
        if (element := _applied(ty, "Maybe")) is not None:
            if value == t.Var("nothing"):
                return host.NOTHING
            if isinstance(value, t.App) and value.function == t.Var("just"):
                return host.Just(self.to_host(value.argument, element, at))
        if (element := _applied(ty, "List")) is not None:
            items = []
            while (isinstance(value, t.App) and isinstance(value.function, t.App)
                   and value.function.function == t.Var("cons")):
                items.append(self.to_host(value.function.argument, element, at))
                value = self.whnf(value.argument)
            if value == t.Var("nil"):
                return items
            raise RunError(f"not a list at the crossing: {value!r}")
        if isinstance(ty, t.Sigma) and isinstance(value, t.Pair):
            return (self.to_host(value.left, ty.domain, at),
                    self.to_host(value.right, _instantiate(ty.name, value.left, ty.codomain), at))
        if isinstance(ty, t.Sum):
            # a sum crosses as (label, value): `int 3` is ("int", 3), tables.py's cells
            alternatives = dict(ty.alternatives)
            if isinstance(value, t.App) and isinstance(value.function, t.Var) and value.function.name in alternatives:
                label = value.function.name
                return label, self.to_host(value.argument, alternatives[label], at)
            if isinstance(value, t.Inj) and value.label in alternatives:
                return value.label, self.to_host(value.value, alternatives[value.label], at)
        if isinstance(ty, t.Record) and isinstance(value, t.RecordValue):
            return self.record_to_host(value, ty, at)
        if (arrow := _arrow(ty)) is not None:
            if self.size(arrow[1]) is not None:
                return self.materialize(value, ty, at)
            return self.function_to_host(value, ty, at)
        return _UNTYPED

    def float64(self, x):
        if type(x) is int:
            if abs(x) > 2 ** 1024 or int(float(x)) != x:
                raise RunError(f"the integer {x} has no exact double")
            x = float(x)
        if not math.isfinite(x):
            raise RunError(f"{x} is not a Float64 (11.S7)")
        return x

    def materialize(self, value, ty, at=None):
        """A lambda over `Fin n` handed to the host is the array of its n values (3.S23), each
        entry evaluated once (3.S25); `Fin m -> Fin n -> A` two-dimensional (3.S24). The element
        type decides the representation: `Float64` float64, `Int` int64 in range (11.S8), any other
        a list (11.S9)."""
        name, domain, codomain = _arrow(self.resolve(ty))
        n = self.size(domain)
        entries = []
        for k in range(n):
            index = t.Lit(t.IntConst(k))
            entries.append(self.to_host(t.App(value, index), _instantiate(name, index, codomain), at))
        leaf, shape = codomain, [n]
        while (arrow := _arrow(self.resolve(leaf))) is not None:
            try:
                shape.append(self.size(arrow[1]))
            except RunError:
                shape.append(None)
            leaf = arrow[2]
        leaf = self.resolve(leaf)
        if leaf == t.Var("Float64"):
            dtype = np.float64
        elif isinstance(leaf, t.Var) and leaf.name in _INTS:
            dtype = np.int64
            for x in np.ravel(np.array(entries, dtype=object)):
                if not _INT64[0] <= int(x) < _INT64[1]:
                    raise RunError(f"the integer {x} does not fit in 64 bits (11.S8)")
        else:
            return entries
        array = np.array(entries, dtype=dtype)
        if n == 0 and None not in shape:
            array = array.reshape(shape)
        return array

    def function_to_host(self, value, ty, at=None):
        """A Luthier function over an infinite domain handed to the host is a callback (3.S23,
        D-2026-10-14-a; world.lth's `CallbackGivesTheFunction`): when the host calls it, its
        arguments cross in by the domain's types, the Runner reduces the application (with the
        host, on this run's fuel), and the result crosses out by the codomain's type. Each call is
        counted under `at`, the receiving extern's route and the position (`CallsAreCounted`)."""
        route, position = at if at is not None else ("?", "?")

        def call(*args):
            host.count(route, position)
            current, result = ty, value
            for arg in args:
                arrow = _arrow(self.resolve(current))
                if arrow is None:
                    raise RunError(f"too many arguments for {value!r}")
                term = self.from_host(arg, arrow[1])
                result = t.App(result, term)
                current = _instantiate(arrow[0], term, arrow[2])
            return self.to_host(result, current, (route, position + ".out"))
        return call

    def host_partial(self, value):
        """An extern (or a host function that crossed in) applied to fewer arguments than its
        arity is a partial application, a value (term.lth's `ExternPartialIsValue`); crossing out
        it is the host's function partially applied to its arguments, crossed by their declared
        types: `functools.partial`, or the function itself when no argument was given. A lambda
        that only passes its parameters on to such an application (`add2 1.0`, `add2` defined as
        `add2 (x y : Float64) : Float64 := extern "..." x y`) is read as it, by eta. None for any
        other value."""
        while isinstance(value, t.Lam):
            if not (isinstance(value.body, t.App) and value.body.argument == t.Var(value.name)
                    and value.name not in kernel.free_names(value.body.function)):
                return None
            value = value.body.function
        args, head = [], value
        while isinstance(head, t.App):
            args.append(head.argument)
            head = head.function
        if not isinstance(head, t.Extern):
            return None
        args.reverse()
        try:
            function = self.route(head)
        except Exception as exc:
            raise RunError(f"extern {head.route} failed: {exc}") from exc
        if not callable(function) or len(args) >= self.arity(head, function):
            return None
        given, _ = self.cross_out(head, function, args)
        return functools.partial(function, *given) if given else function

    def key(self, head, function):
        """The name a receiving extern's calls are counted under: its route, and for a host
        function that crossed in (`host:k`, a name of this run only) also its Python name."""
        if getattr(head, "obj", None) is None:
            return head.route
        name = getattr(function, "__qualname__", None) or type(function).__qualname__
        module = getattr(function, "__module__", None)
        return f"{head.route} {module + '.' if module else ''}{name}"

    def cross_out(self, head, function, args):
        """The arguments of an extern crossed to the host, each at its declared domain, a later
        domain instantiated with the earlier arguments (`(n : Int) -> Fin n -> Float64`); untyped,
        by value. Gives them and the type of what remains."""
        ty, given, route = getattr(head, "type", None), [], self.key(head, function)
        for k, a in enumerate(args, 1):
            a = self.whnf(a)
            arrow = _arrow(self.resolve(ty)) if ty is not None else None
            domain, ty = (arrow[1], _instantiate(arrow[0], a, arrow[2])) if arrow else (None, None)
            given.append(self.to_host(a, domain, (route, str(k))))
        return given, ty

    def record_to_host(self, value, ty, at=None):
        """A record by its fields, a later field's type reading the earlier ones (`f : Fin n -> A`).
        A `Vec` `{ n, f }` or a `Mat` `{ m, n, f }` is the array of `f`, its shape the record's;
        a `Table` the record `tables.as_table` reads, its `cell` giving None or (label, value); a
        record whose fields are one host object's attributes is that object."""
        given = dict(value.fields)
        out, types = HostRecord(), list(ty.fields)
        for k, (label, field_type) in enumerate(types):
            if label not in given:
                raise RunError(f"the record has no field {label}")
            field_at = None if at is None else (at[0], f"{at[1]}.{label}")
            out[label] = self.to_host(given[label], field_type, field_at)
            types[k + 1:] = [(l, _instantiate(label, given[label], f)) for l, f in types[k + 1:]]
        labels = tuple(out)
        if labels in (("n", "f"), ("m", "n", "f")) and isinstance(out["f"], np.ndarray):
            shape = tuple(out[label] for label in labels[:-1])
            if out["f"].shape != shape:
                raise RunError(f"an array of shape {out['f'].shape} where the record says {shape} (3.S24)")
            return out["f"]
        owner = next((getattr(v, "__self__", None) for v in out.values() if hasattr(v, "__self__")), None)
        if owner is not None and all(_same(getattr(owner, label, None), v) for label, v in out.items()):
            return owner
        if labels == ("nRows", "names", "kinds", "cell") and not hasattr(out["cell"], "__self__"):
            cell = out["cell"]
            out["cell"] = lambda name, row: (lambda c: None if c is host.NOTHING else c.value)(cell(name, row))
        return out

    def from_host(self, value, ty=None):
        if value is self.token:
            return self.token
        if ty is not None:
            result = self.typed_from_host(value, self.resolve(ty))
            if result is not _UNTYPED:
                return result
        if value is None:
            return t.Var("unit")
        if value is host.NOTHING:
            return t.Var("nothing")
        if isinstance(value, host.Just):
            return t.App(t.Var("just"), self.from_host(value.value))
        if isinstance(value, (bool, np.bool_)):
            return t.Var("true" if value else "false")
        if isinstance(value, dict):
            # a record value, its fields in the dict's order (State: stdout, then files)
            return t.RecordValue(tuple((label, self.from_host(field)) for label, field in value.items()))
        if isinstance(value, str):
            return t.Lit(t.StringConst(value))
        if isinstance(value, (int, np.integer)):
            return t.Lit(t.IntConst(int(value)))
        if isinstance(value, (float, np.floating)):
            return t.Lit(t.FloatConst(self.float64(float(value))))
        if isinstance(value, tuple) and len(value) == 2:
            return t.Pair(self.from_host(value[0]), self.from_host(value[1]))
        if isinstance(value, list):
            result = t.Var("nil")
            for item in reversed(value):
                result = t.App(t.App(t.Var("cons"), self.from_host(item)), result)
            return result
        if isinstance(value, np.ndarray):
            return self.host_object(Entries(value), None)
        if callable(value):
            return self.host_object(value, None)
        raise RunError(f"unsupported extern result: {value!r}")

    def typed_from_host(self, value, ty):
        if isinstance(ty, t.World):
            return _UNTYPED
        name = ty.name if isinstance(ty, t.Var) else None
        if name == "Float64":
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
                raise RunError(f"the host gave {value!r} where a Float64 is declared (11.S6)")
            return t.Lit(t.FloatConst(self.float64(int(value) if isinstance(value, (int, np.integer)) else float(value))))
        if name in _INTS or _applied(ty, "Fin") is not None:
            if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
                raise RunError(f"the host gave {value!r} where an Int is declared (11.S6)")
            n = self.size(ty)
            if n is not None and not 0 <= int(value) < n:
                raise RunError(f"the host gave {value!r} outside Fin {n}")
            return t.Lit(t.IntConst(int(value)))
        if name == "Bool":
            # a bool, never an int read as one (the fit report's `converged`, 11.S6)
            if not isinstance(value, (bool, np.bool_)):
                raise RunError(f"the host gave {value!r} where a Bool is declared (11.S6)")
            return t.Var("true" if value else "false")
        if (element := _applied(ty, "Maybe")) is not None:
            # host.NOTHING or None is nothing (tables.parse gives None); host.Just or a value is just
            if value is None or value is host.NOTHING:
                return t.Var("nothing")
            inner = value.value if isinstance(value, host.Just) else value
            return t.App(t.Var("just"), self.from_host(inner, element))
        if (element := _applied(ty, "List")) is not None and isinstance(value, (list, tuple)):
            result = t.Var("nil")
            for item in reversed(value):
                result = t.App(t.App(t.Var("cons"), self.from_host(item, element)), result)
            return result
        if isinstance(ty, t.Sigma) and isinstance(value, tuple) and len(value) == 2:
            left = self.from_host(value[0], ty.domain)
            return t.Pair(left, self.from_host(value[1], _instantiate(ty.name, left, ty.codomain)))
        if isinstance(ty, t.Sum):
            alternatives = dict(ty.alternatives)
            if isinstance(value, tuple) and len(value) == 2 and value[0] in alternatives:
                return t.App(t.Var(value[0]), self.from_host(value[1], alternatives[value[0]]))
            raise RunError(f"the host gave {value!r} where one of {tuple(alternatives)} is declared")
        if isinstance(ty, t.Record):
            return self.record_from_host(value, ty)
        if (arrow := _arrow(ty)) is not None:
            if isinstance(value, np.ndarray):
                return self.host_object(Entries(self.array_from_host(value, ty)), ty)
            if callable(value):
                return self.host_object(value, ty)
            raise RunError(f"the host gave {value!r} where a function is declared")
        return _UNTYPED

    def array_from_host(self, a, ty):
        """An ndarray as a value of `Fin n -> ... -> A` (11.S6): as many dimensions as indices, the
        shape the type's where it is known (3.S24), a float dtype for `Float64` (an integer one
        promoted) with no NaN or inf (11.S7), an integer dtype for `Int`."""
        shape, leaf = [], ty
        while (arrow := _arrow(self.resolve(leaf))) is not None:
            try:
                shape.append(self.size(arrow[1]))
            except RunError:
                shape.append(None)
            leaf = arrow[2]
        leaf = self.resolve(leaf)
        if a.ndim != len(shape) and isinstance(leaf, t.Var) and leaf.name in _NAMED:
            raise RunError(f"an array of {a.ndim} dimensions where {len(shape)} are declared (11.S6)")
        for have, want in zip(a.shape, shape):
            if want is not None and have != want:
                raise RunError(f"an array of shape {a.shape} where the type says {tuple(shape)} (3.S24)")
        if leaf == t.Var("Float64"):
            if a.dtype.kind in "iu":
                a = a.astype(np.float64)
            if a.dtype.kind != "f":
                raise RunError(f"an array of dtype {a.dtype} where Float64 is declared (11.S6)")
            if not np.all(np.isfinite(a)):
                raise RunError("an array with NaN or inf crossed (11.S7)")
        elif isinstance(leaf, t.Var) and leaf.name in _INTS and a.dtype.kind not in "iu":
            raise RunError(f"an array of dtype {a.dtype} where Int is declared (11.S6)")
        return a

    def record_from_host(self, value, ty):
        """A record by the type's fields: a dict's entries, an ndarray as a `Vec` (n := its length,
        f := the array) or a `Mat` (m, n := its shape), any other object by its attributes (a
        tables.Table: nRows, names, kinds, and its method cell)."""
        labels = tuple(label for label, _ in ty.fields)
        if isinstance(value, np.ndarray):
            if labels not in (("n", "f"), ("m", "n", "f")):
                raise RunError(f"an array where the record {labels} is declared")
            if value.ndim != len(labels) - 1:
                raise RunError(f"an array of {value.ndim} dimensions where {labels} is declared (11.S6)")
        items, types = [], list(ty.fields)
        for k, (label, field_type) in enumerate(types):
            if isinstance(value, dict):
                if label not in value:
                    raise RunError(f"the host's record has no field {label}")
                component = value[label]
            elif isinstance(value, np.ndarray):
                component = value if label == "f" else value.shape[labels.index(label)]
            elif hasattr(value, label):
                component = getattr(value, label)
            else:
                raise RunError(f"the host gave {value!r} where the record {labels} is declared")
            term = self.from_host(component, field_type)
            items.append((label, term))
            types[k + 1:] = [(l, _instantiate(label, term, f)) for l, f in types[k + 1:]]
        return t.RecordValue(tuple(items))

    def demanded_pattern(self, pattern, value):
        """`value` with what `pattern` inspects in weak head normal form, and what it binds to a
        name shared (8.S4), so an arm that uses the name twice computes it once."""
        if isinstance(pattern, t.PVar):
            return self.share(value)
        if isinstance(pattern, t.PWild):
            return value
        value = self.whnf(value)
        if isinstance(pattern, t.PPair) and isinstance(value, t.Pair):
            return t.Pair(self.demanded_pattern(pattern.left, value.left),
                          self.demanded_pattern(pattern.right, value.right))
        if isinstance(pattern, t.PInj) and isinstance(value, t.Inj) and pattern.label == value.label:
            return t.Inj(value.label, self.demanded_pattern(pattern.pattern, value.value))
        if isinstance(pattern, t.PCon):
            args = []
            head = value
            while isinstance(head, t.App):
                args.append(head.argument)
                head = head.function
            args.reverse()
            if head == t.Var(pattern.name) and len(args) == len(pattern.patterns):
                return self.apply(head, [self.demanded_pattern(p, a)
                                         for p, a in zip(pattern.patterns, args)])
        return value

    def share(self, term):
        """`term` with what would be computed again at each use made a `Shared` (8.S4): an
        application, a block, a match, a projection, an extern that is a value; a pair, an
        injection or a record value keeps its form, its parts shared. Anything else (a name, a
        literal, a lambda, a leaf) is returned as it is: reaching it costs no computation, or (a
        name) is shared through `constants`."""
        if isinstance(term, (t.App, t.Let, t.Match, t.Proj)) or (
                isinstance(term, t.Extern) and getattr(term, "arity", None) == 0):
            return Shared("shared", [term, False])
        if isinstance(term, t.Pair):
            return t.Pair(self.share(term.left), self.share(term.right))
        if isinstance(term, t.Inj):
            return t.Inj(term.label, self.share(term.value))
        if isinstance(term, t.RecordValue):
            return t.RecordValue(tuple((label, self.share(f)) for label, f in term.fields))
        return term

    def force(self, shared):
        """The value of a `Shared`: reduced at the first demand, kept for every later one."""
        cell = shared.cell
        if not cell[1]:
            cell[0] = self.whnf(cell[0])
            cell[1] = True
        return cell[0]

    def whnf(self, value):
        while True:
            self.spend()
            if isinstance(value, Shared):
                return self.force(value)
            if isinstance(value, t.Var) and value.name in self.constants:
                # Delta, the constant's body shared (8.S4)
                value = self.constants[value.name]
                continue
            if isinstance(value, t.Let):
                # Zeta, kernel.step's, with the value shared: each use of the name is one Shared
                value = kernel.step(self.program, replace(value, value=self.share(value.value)))
                continue
            if isinstance(value, t.App):
                args = []
                head = value
                while isinstance(head, t.App):
                    args.append(head.argument)
                    head = head.function
                args.reverse()
                head = self.whnf(head)
                if isinstance(head, t.Lam):
                    # Beta with the arguments shared: a parameter used twice computes once
                    args = [self.share(a) for a in args]
                if isinstance(head, t.Extern):
                    try:
                        function = self.route(head)
                        arity = self.arity(head, function)
                        if len(args) < arity:
                            return self.apply(head, args)
                        given, ty = self.cross_out(head, function, args[:arity])
                        result = function(*given)
                        value = self.apply(self.from_host(result, ty), args[arity:])
                        continue
                    except RunError:
                        raise
                    except Exception as exc:
                        raise RunError(f"extern {head.route} failed: {exc}") from exc
                value = self.apply(head, self.operands(head, args))
            elif isinstance(value, t.Extern):
                try:
                    function = self.route(value)
                    if getattr(value, "arity", None) == 0:
                        # a declared value, not a function: the host's object, or what it gives
                        result = function() if callable(function) else function
                        return self.from_host(result, value.type)
                    if getattr(value, "arity", None) is None and callable(function) and self.arity(value, function) == 0:
                        return self.from_host(function(), getattr(value, "type", None))
                except Exception as exc:
                    raise RunError(f"extern {value.route} failed: {exc}") from exc
            elif isinstance(value, t.Proj):
                value = t.Proj(self.whnf(value.record), value.label)
            elif isinstance(value, t.Match):
                scrutinee = self.whnf(value.value)
                # Try arms in order; only demand what that pattern inspects.
                for pattern, body in value.arms:
                    scrutinee = self.demanded_pattern(pattern, scrutinee)
                    candidate = t.Match(scrutinee, ((pattern, body),))
                    reduced = kernel.step(self.program, candidate)
                    if reduced is not None:
                        value = reduced
                        break
                else:
                    raise RunError("stuck match")
                continue
            reduced = kernel.step(self.program, value)
            if reduced is None:
                return value
            value = reduced

    def operands(self, head, args):
        """A primitive's operands, and the left operand of `and`/`or`, brought to weak head normal
        form by the Runner, with the host, before kernel.step takes the operator's step: the
        kernel alone neither calls the host nor reads a pattern the host must first give. `==`
        compares parts, so its operands are reduced in every concrete part (value)."""
        if isinstance(head, t.Primitive):
            count = 1 if head.name == "toFloat64" else 2
            reduce = self.value if head.name == "==" else self.whnf
            return [reduce(a) for a in args[:count]] + list(args[count:])
        if isinstance(head, t.Var) and head.name in ("and", "or") and head.name not in self.defined and args:
            return [self.whnf(args[0])] + list(args[1:])
        return args

    def value(self, v):
        """`v` in weak head normal form, and so each part of a pair, a record, an injection or a
        constructor applied (a head no act defines)."""
        v = self.whnf(v)
        if isinstance(v, t.Pair):
            return t.Pair(self.value(v.left), self.value(v.right))
        if isinstance(v, t.RecordValue):
            return t.RecordValue(tuple((label, self.value(f)) for label, f in v.fields))
        if isinstance(v, t.Inj):
            return t.Inj(v.label, self.value(v.value))
        args, head = [], v
        while isinstance(head, t.App):
            args.append(head.argument)
            head = head.function
        if args and isinstance(head, t.Var) and head.name not in self.defined:
            return self.apply(head, [self.value(a) for a in reversed(args)])
        return v

    @staticmethod
    def apply(head, args):
        for arg in args:
            head = t.App(head, arg)
        return head


def runtime_slice(acts, main, roots=()):
    """Keep the entry's dependencies (and those of `roots`) and theory declarations, excluding law
    bodies.

    The bootstrap elaborator cannot elaborate all imported certification theories.
    Checking/certification remains a separate responsibility.
    """
    declarations = {a.name for a in acts if isinstance(a, s.Declare)}
    by_name = {}
    for act in acts:
        if isinstance(act, (s.Declare, s.Define, s.Alias)):
            if isinstance(act, s.Define) and act.name in declarations and act.type is None:
                continue
            by_name.setdefault(act.name, []).append(act)

    # a constructor named (in a term or a pattern) needs its data: core's `true`, `cons`, `just`
    owner = {n: act.name for act in acts
             if isinstance(act, s.Define) and isinstance(act.body, s.DataBody)
             for n, _ in act.body.constructors}

    def names(value):
        if isinstance(value, s.Name):
            yield value.name
            yield value.name.split(".")[0]
        elif isinstance(value, s.PApp):
            yield value.name
            yield from names(value.patterns)
        elif isinstance(value, tuple):
            for item in value:
                yield from names(item)
        elif is_dataclass(value):
            for field in fields(value):
                yield from names(getattr(value, field.name))

    needed = set()
    pending = [main, *roots]
    while pending:
        name = pending.pop()
        if name in needed:
            continue
        needed.add(name)
        if name in owner:
            pending.append(owner[name])
        for act in by_name.get(name, ()):
            pending.extend(names(act))
    def projections(value):
        if isinstance(value, s.Name) and "." in value.name and value.name not in by_name:
            # a dotted name is a projection, whether its root is a definition (host.print) or a
            # local binder (st.stdout); the elaborator splits neither
            parts = value.name.split(".")
            result = s.Name(parts[0])
            for part in parts[1:]:
                result = s.Proj(result, part)
            return result
        if isinstance(value, tuple):
            return tuple(projections(item) for item in value)
        if is_dataclass(value):
            return replace(value, **{f.name: projections(getattr(value, f.name)) for f in fields(value)})
        return value
    return tuple(projections(a) for a in acts
                 if a in by_name.get(getattr(a, "name", None), ()) and a.name in needed)


def core_data(loaded):
    """The program's names of core's data, a root of every run's slice (`[1, 2]` is `cons`, `if`
    reads `true`), named or not."""
    if loaded.core is None:
        return ()
    return tuple(loaded.internal(loaded.core, a.name) for a in loaded.files[loaded.core].acts
                 if isinstance(a, s.Define) and isinstance(a.body, s.DataBody))


def _primitive_body(act):
    """core's `x : A := primitive "name"`: an operation the kernel computes becomes its
    `Primitive`, a primitive type (`Int`, `Float64`, ...) a declaration the bridge reads by name."""
    if not isinstance(act, t.Define):
        return act
    body = act.body
    if (isinstance(body, t.App) and body.function == t.Var("primitive")
            and isinstance(body.argument, t.Lit) and isinstance(body.argument.constant, t.StringConst)):
        name = body.argument.constant.value
        if name in kernel.BOOTSTRAP_PRIMITIVES:
            return replace(act, body=t.Primitive(name))
        return t.Declare(act.name, act.type)
    return act


# the types a `--set` can give (12.S18): a parameter hole has one of these, by name
PARAMETER_TYPES = ("String", "Int", "Float64", "Bool")


def _show_type(ty):
    if isinstance(ty, s.Name):
        return ty.name
    if isinstance(ty, s.Binop):
        return f"{_show_type(ty.left)} {ty.operator} {_show_type(ty.right)}"
    if isinstance(ty, s.App):
        return f"{_show_type(ty.function)} {_show_type(ty.argument)}"
    return type(ty).__name__


def holes(loaded):
    """The holes of the file run (3.S9): the names it declares and does not define, each with the
    act that declares it."""
    acts = loaded.files[loaded.top].acts
    defined = {a.name for a in acts if isinstance(a, s.Define)}
    return {a.name: a for a in acts if isinstance(a, s.Declare) and a.name not in defined}


def parameter(hole, text):
    """The value `--set` gives a hole: `text` read as a literal of the hole's type (12.S18). A
    String is the text as written; an Int, a Float64 or a Bool is parsed as a Luthier literal."""
    ty = hole.type
    if not _is_parameter(hole):
        shown = " ".join(f"({' '.join(b.names)} : {_show_type(b.type)})" if hasattr(b, "names") else "?"
                         for b in hole.binders)
        raise RunError(f"--set {hole.name}: {hole.name}{' ' + shown if shown else ''} : {_show_type(ty)} "
                       f"is not a parameter; --set gives a String, an Int, a Float64 or a Bool")
    if ty.name == "String":
        return text
    parsed = parse(f"value := {text}")
    term = None
    if isinstance(parsed, Parsed) and len(parsed.program) == 1 and isinstance(parsed.program[0].body, s.TermBody):
        term = parsed.program[0].body.term
    sign = 1
    if isinstance(term, s.Neg):
        sign, term = -1, term.value
    literal = term.literal if isinstance(term, s.Literal) else None
    if ty.name == "Int" and isinstance(literal, s.IntLit):
        return sign * literal.value
    if ty.name == "Float64" and isinstance(literal, s.FloatLit):
        return sign * literal.value
    if ty.name == "Bool" and sign == 1 and isinstance(term, s.Name) and term.name in ("true", "false"):
        return term.name == "true"
    raise RunError(f"--set {hole.name}={text}: not a literal of type {ty.name}")


def _literal(value):
    if isinstance(value, bool):
        return s.Name("true" if value else "false")
    if isinstance(value, int):
        return s.Literal(s.IntLit(value))
    if isinstance(value, float):
        return s.Literal(s.FloatLit(value))
    return s.Literal(s.StringLit(value))


def fill(loaded, sets):
    """Fill the holes of the file run with the `--set name=value` of `sets` (12.S18): each hole set
    becomes a definition of its literal. Gives the values set, and the program's names of the
    parameter holes left empty."""
    found = holes(loaded)
    values = {}
    for item in sets:
        name, sep, text = item.partition("=")
        if not sep:
            raise RunError(f"--set {item}: expected name=value")
        if name not in found:
            raise RunError(f"--set {name}: {name} is not a declared hole of {loaded.top.name}")
        values[name] = parameter(found[name], text)
    internal = {loaded.internal(loaded.top, n): n for n in found}
    loaded.by_file[loaded.top] = tuple(
        s.Define(a.name, (), a.type, s.TermBody(_literal(values[internal[a.name]])))
        if isinstance(a, s.Declare) and internal.get(a.name) in values else a
        for a in loaded.by_file[loaded.top])
    loaded.acts = tuple(a for acts in loaded.by_file.values() for a in acts)
    # a declaration of another type (a theory, `Shows : { ... }`, or a function) is no parameter
    return values, {i: n for i, n in internal.items() if n not in values and _is_parameter(found[n])}


def _is_parameter(hole):
    return not hole.binders and isinstance(hole.type, s.Name) and hole.type.name in PARAMETER_TYPES


class Refused(RunError):
    """`run`'s refusal (12.S17): the cone of the entry is not certified; `refusals` lists each law
    no entry serves, and each provisional name, with its state."""

    def __init__(self, message, refusals):
        super().__init__(message)
        self.refusals = refusals


# [proposed] the grade a run accepts when it names none with `--accept`: sampled and above, so an
# assumed entry serves only a run that accepts `assumed` by name (6.S10, D-2026-10-14-c)
ACCEPT = "Sampled"


def _head_name(x):
    while isinstance(x, s.App):
        x = x.function
    return x.name if isinstance(x, s.Name) else None


def _provisional(x):
    """Whether a surface term holds an extern applied to `provisional` (4.R5, check.provisional)."""
    if isinstance(x, s.App) and isinstance(x.argument, s.NamedArg) and x.argument.name == "provisional":
        return True
    if isinstance(x, tuple):
        return any(_provisional(y) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return any(_provisional(getattr(x, f.name)) for f in fields(x))
    return False


class _Theories:
    """The theory heads of the loaded files (a name declared at a record and defined by its laws,
    `Arrays : { ... }` and `Arrays := AddPointwise & ...`), and the laws a type states (6.S1)."""

    def __init__(self, acts):
        self.declared = {a.name: a for a in acts if isinstance(a, s.Declare)}
        self.bodies, self.aliases, self.acts = {}, {}, {}
        for a in acts:
            if isinstance(a, (s.Define, s.Declare)):
                self.acts.setdefault(a.name, []).append(a)
            if isinstance(a, s.Alias):
                self.aliases[a.name] = a.value
            elif isinstance(a, s.Define) and a.type is None and isinstance(a.body, s.TermBody):
                self.bodies[a.name] = a.body.term

    def is_theory(self, name):
        d = self.declared.get(name)
        return d is not None and isinstance(d.type, s.Record) and name in self.bodies

    def theory_of(self, ty):
        """The theory head a type names, through aliases (`HostConsole = Host State`); None when
        it names none: such a type states no law."""
        name = _head_name(ty)
        for _ in range(64):
            if name is None or self.is_theory(name):
                return name
            value = self.aliases.get(name, self.bodies.get(name))
            name = _head_name(value) if value is not None else None
        return None

    def laws(self, theory):
        """The laws a theory states: the conjuncts of its definition, a conjunct that is itself a
        theory head read through, in the order written."""
        out, pending = [], [self.bodies[theory]]
        while pending:
            x = pending.pop(0)
            if isinstance(x, s.Binop) and x.operator == "&":
                pending[:0] = [x.left, x.right]
                continue
            name = _head_name(x)
            if name is None:
                continue
            if self.is_theory(name) and name != theory:
                pending[:0] = [self.bodies[name]]
            elif name not in out:
                out.append(name)
        return out

    def model_parameter(self, law, theory):
        """The parameter of a law whose type is the theory: the model the law is applied to."""
        for a in self.acts.get(law, ()):
            if isinstance(a, s.Define):
                for b in a.binders:
                    if isinstance(b, s.Explicit) and self.theory_of(b.type) == theory:
                        return b.names[0]
        return None

    def type_of(self, name):
        """The declared type of a name that takes no binders, or None."""
        for a in self.acts.get(name, ()):
            if not a.binders and a.type is not None:
                return a.type
        return None


def _given(value):
    """certification.lth's `Value` of a `--set` value: a number, or the literal printed."""
    if isinstance(value, bool):
        return {"Printed": "true" if value else "false"}
    if isinstance(value, (int, float)):
        return {"Number": float(value)}
    return {"Printed": json.dumps(value, ensure_ascii=False)}


def _elaborated(kept):
    """The runtime program of a slice, as `run` and the tester build it."""
    # a refined record (belief.lth's `Settings`) as a subtype of the record, as the tester reads
    # it: the elaborator refuses record refinements, and the bridge drops refinements (resolve)
    from .tester import _refined_records
    program = tuple(_primitive_body(a) for a in elaborate_program(_refined_records(kept)))
    # the kernel's bootstrap of the symbols, as `luthier eval` (cli.py); a file's own come first
    return program + tuple(t.Define(op, t.Universe(), t.Primitive(op)) for op in kernel.BOOTSTRAP_PRIMITIVES)


def certification(loaded, program, entry, values, accept=None):
    """What a run requires (certification.lth §3, 7.S15, 12.S17, 6.S14): the cone of the entry with,
    per name, its demands, read against the stores of the files loaded (12.S11). Gives the
    certification state the run records (12.S18); raises `Refused`, listing each refusal with its
    state, when the store refuses anything of the cone.

    Each name of the cone whose type is a theory head (through aliases) demands each law the
    theory states; a name whose type states no law is certified vacuously ([proposed] 10 of the
    theory, 6.S1). A demand: the law (as a test line names it), the current hash of the law's
    cone, the cutoff `accept`, and what the run gives the law: [proposed] the name itself to the
    law's parameter typed by the theory (printed, as a census of one prints it), and each hole the
    run filled with `--set` to the law's parameter of the same name (certification.lth's
    `Demand`); the model's own cone is compared with the fingerprint the entry's binding recorded
    (certify.at). A name built on a provisional extern is refused whole."""
    from . import certify
    accept = accept or ACCEPT
    cones = certify.Cones(program)
    names = sorted(cones.names(entry))
    theories = _Theories(loaded.acts)
    surface = {}
    for a in loaded.acts:
        if isinstance(a, (s.Define, s.Declare)):
            surface.setdefault(a.name, []).append(a)
    # each name of the cone: provisional, or the theory its type states laws of
    stating = {}
    provisional = set()
    for n in names:
        if any(_provisional(getattr(a, "body", None)) for a in surface.get(n, ())):
            provisional.add(n)
        ty = theories.type_of(n)
        theory = theories.theory_of(ty) if ty is not None else None
        if theory is not None:
            stating[n] = theory
    laws = sorted({law for theory in set(stating.values()) for law in theories.laws(theory)})
    law_cones = certify.Cones(_elaborated(runtime_slice(loaded.acts, laws[0], core_data(loaded) + tuple(laws)))) \
        if laws else None
    cone = []
    for n in names:
        demands = []
        if n in stating and n not in provisional:
            theory = stating[n]
            for law in theories.laws(theory):
                given, fingerprints = [], {}
                m = theories.model_parameter(law, theory)
                if m is not None:
                    given.append((m, {"Printed": n.partition("@")[0]}))
                    fingerprints[m] = cones.hash(n)
                params = [p for a in theories.acts.get(law, ()) if isinstance(a, s.Define)
                          for b in a.binders if isinstance(b, s.Explicit) for p in b.names]
                given += [(p, _given(values[p])) for p in params if p in values and p != m]
                demands.append({"law": law.partition("@")[0], "cone": law_cones.hash(law), "given": given,
                                "accepts": accept, "fingerprints": fingerprints})
        cone.append({"name": n.partition("@")[0], "provisional": n in provisional, "laws": demands})
    entries = sorted((e for f in loaded.files for e in certify.read_store(f)),
                     key=lambda e: e.get("date", ""), reverse=True)
    refusals = certify.refuse(entries, cone)
    if refusals:
        lines = [certify.show_refusal(r, entries) for r in refusals]
        raise Refused(f"refused: the cone of {entry.partition('@')[0]} is not certified (accepting "
                      f"{certify.GRADE_WORDS[accept]} and above; 12.S17):\n  " + "\n  ".join(lines), refusals)
    with_laws = [c for c in cone if c["laws"]]
    code_only = {"code": cones.cone(entry)["code"], "hosts": [], "interpreter": ""}
    return {"cone": cones.hash(entry), "interpreter": certify.interpreter_revision(),
            # the canonical code's hash apart from the hosts and the interpreter (12.S18): two
            # records with the same fingerprint ran the same code [proposed: certify.cone_hash of
            # the cone's code with no hosts and an empty interpreter]
            "fingerprint": certify.cone_hash(code_only),
            "python": platform.python_version(),
            "hosts": {r: h for r, h in cones.hosts(entry)},
            "accept": certify.GRADE_WORDS[accept],
            "states": {"certified": len(with_laws), "vacuous": len(cone) - len(with_laws),
                       "provisional": 0, "uncertified": 0, "stale": 0, "failed": 0},
            "laws": sum(len(c["laws"]) for c in with_laws), "not certified": []}


def refuse_provisional(kept, entry):
    """A name of the slice built on a provisional extern (4.R5) is refused whole (6.S14, 12.S17,
    `ProvisionalIsRefused`), before the slice is elaborated: the elaborator does not read the
    extern's `(provisional <- true)`. [proposed] The laws of the rest of the cone are then not
    listed: a provisional name refuses the run whatever the store holds."""
    names = sorted(dict.fromkeys(a.name for a in kept if isinstance(a, s.Define) and _provisional(a.body)))
    if names:
        refusals = [{"name": n.partition("@")[0], "law": None, "state": ("Provisional", None)} for n in names]
        from .certify import show_refusal
        lines = [show_refusal(r, []) for r in refusals]
        raise Refused(f"refused: the cone of {entry.partition('@')[0]} is not certified (12.S17):\n  "
                      + "\n  ".join(lines), refusals)


def run(path, main="main", fuel=10000, sets=(), accept=None):
    """Run `main` of the file at `path` with its holes filled by `sets`, once the store certifies
    its cone at the grade `accept` (12.S17; `Refused` otherwise, before anything is evaluated);
    gives the standard output, the values set and the certification state of the cone."""
    host.reset()
    loaded = Loaded(path)
    values, empty = fill(loaded, sets)
    entry = loaded.name(loaded.top, main) or main
    kept = runtime_slice(loaded.acts, entry, core_data(loaded))
    loaded.demand(kept)
    for a in kept:
        if isinstance(a, s.Declare) and a.name in empty:
            name = empty[a.name]
            raise RunError(f"{name} : {_show_type(a.type)} is a hole of {loaded.top.name} the run needs; "
                           f"give it with --set {name}=...")
    refuse_provisional(kept, entry)
    program = _elaborated(kept)
    definition = next((a for a in program if isinstance(a, t.Define) and a.name == entry), None)
    if definition is None:
        raise RunError(f"missing main: {main}")
    main = entry
    state = certification(loaded, program, entry, values, accept)
    runner = Runner(program, fuel)
    value = t.Var(main)
    if isinstance(definition.type, t.Pi) and isinstance(definition.type.domain, t.World):
        value = t.App(value, runner.token)
    result = runner.whnf(value)
    if isinstance(result, t.Pair):
        runner.whnf(result.left)  # Demand the final world chain, even for a lazy pair.
    state = dict(state or {}, fuel={"given": fuel, "spent": fuel - runner.fuel},
                 files_read=[list(pair) for pair in host.files_read()], lock=lock_status(path))
    return host.stdout(), values, state


LOCK = "luthier.lock"


def lock_status(path):
    """12.S13: the `luthier.lock` found in the directory of the program or the one above, which
    pins the interpreter's revision. Gives {"path", "pinned", "status"}: `matches`, `differs` (a
    warning on standard error: the run goes on, 12.S13 names no refusal and no flag that turns the
    lock off), or `absent` (`record` then writes it beside the program)."""
    from . import certify
    here = Path(path).resolve().parent
    current = certify.interpreter_revision()
    for directory in (here, here.parent):
        lock = directory / LOCK
        if lock.exists():
            try:
                pinned = json.loads(lock.read_text(encoding="utf-8"))["interpreter"]
            except (ValueError, KeyError, TypeError):
                raise RunError(f"{lock}: not a lock (a JSON object with an `interpreter`)")
            if pinned != current:
                import sys
                print(f"warning: {lock} pins interpreter {pinned}, this is {current} (12.S13)", file=sys.stderr)
            return {"path": str(lock), "pinned": pinned, "status": "matches" if pinned == current else "differs"}
    return {"path": str(here / LOCK), "pinned": None, "status": "absent"}


def run_file(path, main="main", fuel=10000, sets=(), accept=None):
    return run(path, main, fuel, sets, accept)[0]


def record_path(path):
    path = Path(path)
    return path.with_name(path.stem + ".run.json")


def record(path, main, values, output, state=None):
    """Append this run to `x.run.json` beside `x.lut` (12.S18): the entry, the time, the
    parameters, the output, the calls the host made back into Luthier during the run (`calls`:
    receiving extern's route -> position among its arguments -> count, D-2026-10-14-a), and the
    certification state of the cone (`certification`: the hash of the entry's cone, the
    interpreter's revision, the grade accepted, the counts of states of the cone's names and the
    names not certified, empty since a run starts only on a certified cone, the fingerprint of the
    cone's code, the Python's and the hosts' versions), the fuel given and spent, the files read
    with the hash of their bytes (`files_read`) and the lock (`lock`: its path, the revision it
    pins and whether the run `matches` it, `differs`, or found it `absent` and wrote it)."""
    from datetime import datetime, timezone
    where = record_path(path)
    runs = json.loads(where.read_text(encoding="utf-8")) if where.exists() else []
    item = {"entry": main, "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "parameters": values, "output": output, "calls": host.calls()}
    if state is not None:
        state = dict(state)  # a copy: the entry takes fuel, files_read and lock out of it
        for key in ("fuel", "files_read", "lock"):
            if key in state:
                item[key] = state.pop(key)
        lock = item.get("lock")
        if lock and lock["status"] == "absent":
            from . import certify
            Path(lock["path"]).write_text(json.dumps({"interpreter": certify.interpreter_revision()}) + "\n",
                                          encoding="utf-8")
            lock["pinned"], lock["status"] = certify.interpreter_revision(), "written"
        item["certification"] = state
    runs.append(item)
    where.write_text(json.dumps(runs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return where
