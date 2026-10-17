"""Demand-driven host runner. Sources: spec 10.S2–S10, world_model.lut (0c920f0).

Derivation: user request 2026-10-13, implementation v1 (record/IA/run-2026-10-13/codex.md);
v2 for world.lth draft 1 (prompt-2.md, choices in opus-2.md): the bridge carries `Maybe`
(host.Just, host.NOTHING) and records (a dict). v4 (prompt-4.md, choices in report-4.md): the
bridge reads by the type the extern's definition declares (spec 3.S22 to 3.S26, 11.S6 to 11.S9):
`Vec`/`Mat` records and `Fin n -> Float64`/`Int` as ndarrays, `Float64` and `Int` checked,
`Table` as tables.py reads it, sums as `(label, value)`. v5 (prompt-5.md, report-5.md): every
run loads `lib/core/core.lut` before the file (12.S22, 11.R2), defines kernel.BOOTSTRAP_PRIMITIVES as
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
opt-out (D-2026-10-12-y); the record carries the cone's certification state (12.S18). v14
(record/IA/certification-2026-10-14/prompt-first-action.md, 10.S10, L11.2): a host action whose
model's theory holds it to a law that takes the token (world.lth's `Host` laws) is validated at its
first application in a run (`FirstActions`): served by the model file's store, or the law run once
with the run's arguments, the protocol's application of the action being the program's; refuted, the
run is refused naming the action and the place; confirmed, an entry in the store and in the record.
v15 (record/IA/run-2026-10-13/prompt-12.md; 12.S18, 4.R5, 10.S11): every declared type is checked
where it crosses, either way (`String`, `Unit`, `Bool`, `Nat` not negative, `Int` in 64 bits, `Maybe`,
the token's slot only the run's token), and a type the bridge does not read is an error, never the
untyped reading (review A24/B18, A26/B17, A28/B19); under `run --checked` the predicate of each
subtype a value crosses in at is evaluated by the Runner before the program sees it (`refine`), a
refuted one refusing the run, and the record counts them per route. v16 (prompt-13.md; demand.lth,
plan.lth, record/IA/demand-2026-10-15/report.md): `run` builds one `Demand` from its arguments and
demand_model.lut's defaults, from which every law's demand and the record derive; the record holds
the demand (`demand`), the plan (the live cone, the call-by-need schedule of the Runner's shared
constants and its hash, `plan`) and the demand's key (`key`); `read_runs` reads `x.run.json` back and
reports the breaches of `determined`. v17 (record/IA/layer-3-review-2026-10-15/prompt-run-host.md, after
world.lth's 2ac8f12): the laws of `Host` are predicates over an observed case; at an action's first
application `FirstActions` gathers the case by world.lth's `agreement` with the `Held` the law
builds and the places the certifier adds, evaluates the law and the frame law
(`HostChangesOnlyDeclared`) on it, and gives the program the token and the case's result; a law
whose body is an axiom (`ObserverIsFaithful`) is accepted as assumed by default (`AXIOMS`).
"""
from __future__ import annotations

import functools
import importlib
import inspect
import json
import math
import platform
import sys
import time
from dataclasses import dataclass, field, fields, is_dataclass, replace
from pathlib import Path

import numpy as np

from . import host, kernel, surface as s, term as t
from .elaborate import elaborate_program
from .parse import parse
from .surface import Parsed


class RunError(ValueError):
    pass


class Cut(RunError):
    """A run stopped by its time limit or its fuel (D-2026-10-16-d): it did not finish. `reason`
    is "fuel" or "time limit", `steps` the reduction steps reached; `values` and `state` are what
    `record` needs to append it to `x.run.json` as a run that did not finish (the coordinator's
    answer to 3g's question, record/plan/code-follows-principles-2026-10-16.md g'). Nothing of it
    goes to the store of results, and it is never served."""
    def __init__(self, message, reason, steps, values=None, state=None):
        super().__init__(message)
        self.reason, self.steps, self.values, self.state = reason, steps, values, state


# The three kinds of file (D-2026-10-16-e, spec 12.R2): a theory (`.lth`), a model or library
# (`.lut`), and an executive file, which carries a demand with its entry and is never imported:
# `x.run.lut` (the `main` that `luthier run` applies to the world) or `x.test.lut` (the `test`
# lines `luthier certify` runs). The suffix declares the kind; the checker (check.py's `kinds`),
# the loader (an import of an executive file) and the commands (`require_kind`) verify it.
EXECUTIVE = {"run": ".run.lut", "test": ".test.lut"}
SUFFIX = {"theory": ".lth", "model": ".lut", **EXECUTIVE}
KIND_NAME = {"theory": "a theory", "model": "a model or library", "run": "a run", "test": "a test program"}
COMMAND_OF = {"run": "luthier run", "test": "luthier certify"}


def file_kind(path):
    """The kind a file's name declares: `run`, `test`, `theory` or `model`; None for another file
    (a `.bib`)."""
    name = Path(path).name
    for kind, suffix in EXECUTIVE.items():
        if name.endswith(suffix) and len(name) > len(suffix):
            return kind
    if name.endswith(".lth"):
        return "theory"
    if name.endswith(".lut"):
        return "model"
    return None


def base_name(path):
    """A file's name without the suffix of its kind: `x` for x.run.lut, x.test.lut, x.lut and x.lth
    (so that the record of x.run.lut is x.run.json and its results x.results.json, L10.12)."""
    kind = file_kind(path)
    name = Path(path).name
    return name[:-len(SUFFIX[kind])] if kind else Path(path).stem


def executive_import(importer, target):
    """Why an import of `target` by `importer` is refused (12.R2): an executive file is never
    imported; None when it is not one."""
    kind = file_kind(target)
    if kind not in EXECUTIVE:
        return None
    return (f"{Path(importer).name} imports {Path(target).name}, {KIND_NAME[kind]} ({EXECUTIVE[kind]}): an "
            f"executive file is never imported (12.R2, D-2026-10-16-e); what it shares belongs in a .lut")


def require_kind(path, kind, command=None):
    """`luthier run` takes a .run.lut, `luthier certify` and `luthier test` a .test.lut (12.R2):
    a RunError naming the suffix wanted, and what the file is, otherwise."""
    has = file_kind(path)
    if has == kind:
        return
    what = (f"{KIND_NAME[has]} ({SUFFIX[has]}" + (f", for `{COMMAND_OF[has]}`)" if has in COMMAND_OF else ")")
            if has else "no Luthier file")
    raise RunError(f"`{command or COMMAND_OF[kind]}` takes a {EXECUTIVE[kind]} file (12.R2, D-2026-10-16-e); "
                   f"{Path(path).name} is {what}")


# the core encloses the top-level scope of every file (12.S22); its data and `not` are read here
CORE = Path(__file__).parent / "lib" / "core" / "core.lut"


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
                refusal = executive_import(path, target)
                if refusal:
                    raise RunError(refusal)
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
    arity is its Python signature's. `name`, the definition that gives it (`neg`, `numpy.norm`),
    for a refusal at the crossing to name (10.S11)."""
    type: object = None
    obj: object = field(default=None, compare=False, hash=False)
    arity: int | None = field(default=None, compare=False, hash=False)
    name: str | None = field(default=None, compare=False, hash=False)


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
    substitution pass it on untouched; only the Runner looks inside. `cell` is [term, forced], and
    for a constant of the program [term, forced, its name] (`Runner.schedule`)."""
    cell: list = field(default_factory=list)

    __eq__ = object.__eq__
    __hash__ = object.__hash__

    def __repr__(self):
        return f"Shared({self.cell[0]!r})"


_INTS = ("Int", "Nat")
_NAMED = {"Float64", "String", "Unit", "Bool"} | set(_INTS)
_INT64 = (-2 ** 63, 2 ** 63)
# the type families the bridge reads by name, never unfolded (`Fin n` is an index, 3.S21)
_READ_BY_NAME = {"Fin", "Maybe", "List"}


def _integer(x, name, where):
    """An integer at a declared `Int`, `Nat` or `Fin n` as it crosses, either way: 64 bits (11.S8,
    scalars as arrays, review A26/B17), not negative at `Nat`."""
    if name == "Nat" and x < 0:
        raise RunError(f"{x} {where} where a Nat is declared")
    if not _INT64[0] <= x < _INT64[1]:
        raise RunError(f"the integer {x} {where} does not fit in 64 bits (11.S8)")
    return x


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
    def __init__(self, program, fuel, checked=False, time_limit=None):
        # the demand's limits (D-2026-10-16-d): `fuel` the reduction steps left, None for no bound;
        # `time_limit` the seconds the run may take, None for none; `steps` the steps taken
        self.fuel, self.time_limit, self.steps = fuel, time_limit, 0
        self.deadline = None if time_limit is None else time.monotonic() + time_limit
        # why the run was cut, once a limit cut it: (reason, message), the reason "fuel" or "time
        # limit"; read by `run` whatever wrapped the error on its way out (a host, a callback)
        self.cut = None
        # the provisional externs the demand runs as assumed, by route: (names, reason); each warns
        # on standard error at its first application in the run (D-2026-10-16-c)
        self.provisional, self.warned = {}, set()
        # `run --checked` (12.S18, 4.R5): each value crossing in at a declared subtype has its
        # predicate evaluated here; `tested` counts them per route, for the run's record
        self.checked, self.tested = checked, {}
        # An opaque kernel leaf stands for the host-owned identity for this run.
        self.token = t.Axiom("host world token")
        self.routes = {}
        # the actions validated at their first application (10.S10): route -> what `validate`
        # (run's `FirstActions`) needs; `validating` while a law runs, `trace` the host's calls then
        self.first, self.validate, self.validating, self.trace = {}, None, False, None
        # `luthier session --world` (12.S20, 2.S18): the session's hook on each application of an
        # extern to the token, which serves an action the session already performed (`Session`)
        self.actions = None
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
            if isinstance(act, t.Define) and not isinstance(act.body, t.Lam) and act.name not in self.constants:
                shared = self.constants[act.name] = self.share(act.body)
                if isinstance(shared, Shared):
                    shared.cell.append(act.name)
        # the call-by-need schedule (plan.lth's `Schedule`, 8.S4): each constant's name when its
        # first reduction ends, so after the constants it demanded on the way (plan_model.lut's
        # `byNeed`). [proposed] Only a constant whose body is a computation is a cell (`share`):
        # a function, a literal, a record or a name costs nothing to reach and is not scheduled.
        self.schedule = []

    def typed(self, act):
        """The definition with each extern it gives carrying its declared type: `f (x : A) : B :=
        extern "..." x`, or a record of a declared theory whose fields are externs (3.S40)."""
        if not isinstance(act, t.Define) or act.type is None or isinstance(act.type, t.Hole):
            return act  # no type declared (the elaborator's hole): the host's signature decides
        extern = _extern_of(act.body)
        shown = act.name.partition("@")[0]
        if extern is not None:
            arity = _parameters(act.body) or self.arity_of(act.type)
            return replace(act, body=_with_extern(act.body, TypedExtern(extern.route, act.type, arity=arity,
                                                                        name=shown)))
        record = self.resolve(act.type)
        if isinstance(act.body, t.RecordValue) and isinstance(record, t.Record):
            types = dict(record.fields)
            items = []
            for label, value in act.body.fields:
                extern = _extern_of(value)
                if extern is not None and label in types:
                    arity = _parameters(value) or self.arity_of(types[label])
                    value = _with_extern(value, TypedExtern(extern.route, types[label], arity=arity,
                                                            name=f"{shown}.{label}"))
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

    def refinements(self, ty):
        """The subtypes `ty` names down to what the bridge reads, as `resolve` unfolds them, each
        (binder, predicate), the innermost first (`Positive` gives `Moderate`'s predicate, then its
        own): the predicates a value crossing in at `ty` owes (4.R5). The refinements of a named
        primitive (`Nat`) are the bridge's shape checks, not listed here."""
        found = []
        while True:
            if isinstance(ty, t.Subtype):
                found.append((ty.name, ty.predicate))
                ty = ty.type
            elif isinstance(ty, t.Var) and ty.name not in _NAMED and ty.name in self.types:
                ty = self.types[ty.name]
            elif (applied := self.family_applied(ty)) is not None:
                ty = applied
            else:
                return found[::-1]

    def refine(self, term, ty, at):
        """`run --checked` (12.S18, 4.R5, 10.S11): the predicate of each subtype of `ty` evaluated
        by the Runner on `term`, the value that crossed in, before the program sees it; each counted
        under `at`'s route. A refuted one refuses the run naming the extern, the route, the type and
        the value."""
        for binder, predicate in self.refinements(ty):
            name, route = at if at is not None else (None, "?")
            self.tested[route] = self.tested.get(route, 0) + 1
            holds = self.whnf(kernel.substitute(binder, term, predicate))
            if holds == t.Var("true"):
                continue
            who = route if name is None or name == route else f"{name} ({route})"
            declared, law, value = _type_shown(ty), _type_shown(predicate), _type_shown(term)
            if holds != t.Var("false"):
                raise RunError(f"--checked: the refinement {law} of {declared} gave {_type_shown(holds)}, "
                               f"not a Bool, on what {who} gave")
            raise Refused(f"--checked: {who} gave {value} where {declared} is declared: {law} is false "
                          f"at {binder} = that value (12.S18, 4.R5, 10.S11)",
                          [{"name": name, "route": route, "type": declared, "predicate": law, "value": value}])

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
        if self.fuel is not None:
            if self.fuel <= 0:
                self.cut = ("fuel", "fuel spent")
                raise RunError("fuel spent")
            self.fuel -= 1
        self.steps += 1
        # the clock read every 4096 steps, so that a limit costs nothing measurable
        if self.deadline is not None and not self.steps & 4095 and time.monotonic() > self.deadline:
            message = f"time limit of {self.time_limit:g} s reached after {self.steps} steps (run --time-limit)"
            self.cut = ("time limit", message)
            raise RunError(message)

    def route(self, head):
        if getattr(head, "obj", None) is not None:
            return head.obj
        route = head.route
        if route not in self.routes:
            if not route.startswith("python:"):
                raise RunError(f"unsupported extern route: {route}")
            if route in self.provisional and route not in self.warned:
                self.warned.add(route)
                names, reason = self.provisional[route]
                print(f"warning: applying provisional extern {', '.join(names)} as assumed ({route}): "
                      f"{reason or 'no reason given'} (D-2026-10-16-c)", file=sys.stderr)
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
            return self.typed_to_host(value, self.resolve(ty), at)
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
        """`value` crossed out at the resolved declared type `ty`, its shape checked (11.S6 to 11.S8;
        prompt-12.md item 1): a type the bridge does not read is an error, never the untyped
        reading (review A28/B19)."""
        name = ty.name if isinstance(ty, t.Var) else None
        if isinstance(ty, t.World):
            # `to_host` gave the run's token already; anything else in its slot is refused (10.S4)
            raise RunError(f"not the run's token at the crossing: {_shown(value)} (10.S4)")
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
            return _integer(value.constant.value, name, "at the crossing")
        if name == "String":
            if isinstance(value, t.Lit) and isinstance(value.constant, t.StringConst):
                return value.constant.value
            raise RunError(f"not a String at the crossing: {_shown(value)}")
        if name == "Unit":
            if value == t.Var("unit"):
                return None
            raise RunError(f"not unit at the crossing: {_shown(value)}")
        if name == "Bool":
            if value in (t.Var("true"), t.Var("false")):
                return value == t.Var("true")
            raise RunError(f"not a Bool at the crossing: {_shown(value)}")
        if (element := _applied(ty, "Maybe")) is not None:
            if value == t.Var("nothing"):
                return host.NOTHING
            if isinstance(value, t.App) and value.function == t.Var("just"):
                return host.Just(self.to_host(value.argument, element, at))
            raise RunError(f"not a Maybe at the crossing: {_shown(value)}")
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
        raise RunError(f"{_shown(value)} at the crossing where {_type_shown(ty)} is declared: "
                       f"not a value of that type the bridge reads (prompt-12.md, A28/B19)")

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
                # what the host passes the callback crosses in as a result does, its refinements
                # tested under --checked, counted under the receiver's route and position
                term = self.from_host(arg, arrow[1], (None, f"{route} callback {position}"))
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
        a `Table` the record `tables.as_table` reads, its `cell` giving host.Just (label, value) or
        host.NOTHING as tables.py's `Table.cell` does (D-2026-10-16-h); a
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
        return out

    def from_host(self, value, ty=None, at=None):
        """`value` the host gave, as a kernel term: read by the declared type `ty` when there is one
        (`typed_from_host`), its refinements then tested under `run --checked` (`refine`); by value
        otherwise. `at` is (name, route): the extern it came from, or the callback's receiver."""
        if value is self.token:
            return self.token
        if ty is not None:
            result = self.typed_from_host(value, self.resolve(ty), at)
            if self.checked:
                self.refine(result, ty, at)
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

    def typed_from_host(self, value, ty, at=None):
        """The host's `value` read at the resolved declared type `ty`, its shape checked (11.S6 to
        11.S8); a type the bridge does not read is an error, never the untyped reading (prompt-12.md
        item 1, review A28/B19). The refinements are `refine`'s."""
        if isinstance(ty, t.World):
            # `from_host` took the run's token already: anything else in its slot is refused (10.S4,
            # review A24/B18)
            raise RunError(f"the host gave {value!r} where the run's token is declared (10.S4)")
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
            return t.Lit(t.IntConst(_integer(int(value), name, "from the host")))
        if name == "String":
            if not isinstance(value, str):
                raise RunError(f"the host gave {value!r} where a String is declared")
            return t.Lit(t.StringConst(str(value)))
        if name == "Unit":
            if value is not None:
                raise RunError(f"the host gave {value!r} where Unit is declared")
            return t.Var("unit")
        if name == "Bool":
            # a bool, never an int read as one (the fit report's `converged`, 11.S6)
            if not isinstance(value, (bool, np.bool_)):
                raise RunError(f"the host gave {value!r} where a Bool is declared (11.S6)")
            return t.Var("true" if value else "false")
        if (element := _applied(ty, "Maybe")) is not None:
            # strict (D-2026-10-16-h, item 14): host.NOTHING is nothing and host.Just x is just x;
            # a bare value, None included, is refused, with or without `--checked`
            if value is host.NOTHING:
                return t.Var("nothing")
            if isinstance(value, host.Just):
                return t.App(t.Var("just"), self.from_host(value.value, element, at))
            raise RunError(f"the host gave {value!r} where a Maybe is declared: a Maybe crosses as "
                           f"host.Just or host.NOTHING (D-2026-10-16-h)")
        if (element := _applied(ty, "List")) is not None:
            if not isinstance(value, (list, tuple)):
                raise RunError(f"the host gave {value!r} where a List is declared")
            result = t.Var("nil")
            for item in reversed(value):
                result = t.App(t.App(t.Var("cons"), self.from_host(item, element, at)), result)
            return result
        if isinstance(ty, t.Sigma):
            if not (isinstance(value, tuple) and len(value) == 2):
                raise RunError(f"the host gave {value!r} where a pair is declared")
            left = self.from_host(value[0], ty.domain, at)
            return t.Pair(left, self.from_host(value[1], _instantiate(ty.name, left, ty.codomain), at))
        if isinstance(ty, t.Sum):
            alternatives = dict(ty.alternatives)
            if isinstance(value, tuple) and len(value) == 2 and value[0] in alternatives:
                return t.App(t.Var(value[0]), self.from_host(value[1], alternatives[value[0]], at))
            raise RunError(f"the host gave {value!r} where one of {tuple(alternatives)} is declared")
        if isinstance(ty, t.Record):
            return self.record_from_host(value, ty, at)
        if (arrow := _arrow(ty)) is not None:
            if isinstance(value, np.ndarray):
                return self.host_object(Entries(self.array_from_host(value, ty)), ty)
            if callable(value):
                return self.host_object(value, ty)
            raise RunError(f"the host gave {value!r} where a function is declared")
        raise RunError(f"the host gave {value!r} where {_type_shown(ty)} is declared, a type the bridge "
                       f"does not read (prompt-12.md, A28/B19)")

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
        elif isinstance(leaf, t.Var) and leaf.name in _INTS:
            if a.dtype.kind not in "iu":
                raise RunError(f"an array of dtype {a.dtype} where Int is declared (11.S6)")
            # an unsigned array may hold what int64 does not (11.S8, review B17); a Nat no negative
            if a.size and a.dtype.kind == "u" and int(a.max()) >= _INT64[1]:
                raise RunError(f"an array of dtype {a.dtype} with an entry that does not fit in 64 bits (11.S8)")
            if a.size and leaf.name == "Nat" and a.dtype.kind == "i" and int(a.min()) < 0:
                raise RunError(f"an array with the entry {int(a.min())} where Nat is declared")
        return a

    def record_from_host(self, value, ty, at=None):
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
            term = self.from_host(component, field_type, at)
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
            if len(cell) > 2:
                self.schedule.append(cell[2])
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
                        if self.actions is not None and not self.validating:
                            args = [self.share(a) for a in args]
                            value = self.apply(self.actions(self, head, function, args[:arity]), args[arity:])
                            continue
                        value = self.apply(self.act(head, function, args[:arity]), args[arity:])
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
                        return self.from_host(result, value.type, (value.name, value.route))
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

    def act(self, head, function, args):
        """The extern `head` (the host's `function`) applied to as many arguments as it takes."""
        if self.first and not self.validating and head.route in self.first:
            # the action's first application in the run (10.S10): validated, the protocol's own
            # application being the program's when it ran; the arguments shared, so that the
            # validation and the program compute each once (8.S4)
            args = [self.share(a) for a in args]
            acted = self.validate(self, self.first.pop(head.route), head, args)
            if acted is not None:
                return acted
        given, ty = self.cross_out(head, function, args)
        result = function(*given)
        value = self.from_host(result, ty, (getattr(head, "name", None), self.key(head, function)))
        if self.trace is not None:
            self.trace.append((head.route, given, value))
        return value

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

    # rule 2.2 (the core's bite 4): a field of a structure used free (`size xs`) or qualified
    # (`Indexed.size`) is resolved through the claims of its structures, so a name reaching it
    # reaches them; a structure is a name declared at a record with parameters, a claim `X : Bool
    # := S T m` names it at the head of its body
    fields_of = {}
    for act in acts:
        if isinstance(act, s.Declare) and act.binders and isinstance(act.type, s.Record):
            for f in act.type.fields:
                for n in f.names:
                    fields_of.setdefault(n, set()).add(act.name)
    claims = {}
    for act in acts:
        if isinstance(act, s.Define) and act.type == s.Name("Bool") and isinstance(act.body, s.TermBody):
            h = act.body.term
            while isinstance(h, s.App):
                h = h.function
            if isinstance(h, s.Name) and any(h.name in owners for owners in fields_of.values()):
                claims.setdefault(h.name, []).append(act.name)

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
            written = list(names(act))
            pending.extend(written)
            bound = _bound_names(act)
            for n in written:
                if n in by_name or n in bound or n in ("left", "right"):
                    continue
                root, _, rest = n.partition(".")
                for structure in fields_of.get(n, set()) | ({root} if rest and root in claims else set()):
                    pending.extend(claims.get(structure, ()))
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


def _bound_names(value):
    """The names an act binds itself (its binders, a lambda's parameters, a block's names, a
    pattern's variables): a field of a structure written as one of them is no use of the field."""
    out = set()
    def visit(x):
        if isinstance(x, (s.Explicit, s.Implicit, s.TypedParam)):
            out.update(x.names)
        elif isinstance(x, (s.PlainParam, s.Bind)):
            out.add(x.name)
        elif isinstance(x, s.PApp) and not x.patterns:
            out.add(x.name)
        if isinstance(x, tuple):
            for y in x:
                visit(y)
        elif is_dataclass(x) and not isinstance(x, type):
            for f in fields(x):
                visit(getattr(x, f.name))
    visit(value)
    return out


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

# demand_model.lut's `theDemand`: the default of each argument of `run` (L5.19, P11), declared there
# and mirrored here; tests/test_run.py checks the two agree. `pinned` has no default to mirror: it
# is read from the lock (12.S13). No fuel bound and no time limit (D-2026-10-16-d); forward on
# demand asked, which call by need computes as its specimen (`TheDefaultsAgree`, 8.S4); no
# provisional run as assumed (D-2026-10-16-c).
DEMAND_DEFAULTS = {"entry": "main", "accepts": ACCEPT, "assumes": (), "fuel": None, "timeLimit": None, "sets": (),
                   "checked": False, "strategy": "ForwardOnDemand", "fresh": False}

# the strategy that computes a demand, by the strategy it asks (demand.lth's `Ran`,
# `RanIsASpecimenOfTheAsked`): run.py reduces by call by need whatever is asked
RAN = {"ForwardOnDemand": "CallByNeed", "CallByNeed": "CallByNeed"}

# [proposed, Luciano to mark; record/IA/layer-3-review-2026-10-15/prompt-run-host.md] the grade a run
# accepts, by default, for a law whose body is an `axiom` (world.lth's `ObserverIsFaithful`, 11.R3):
# assumed, so that an axiom no entry serves is accepted as the assumption it states and the run's
# certification lists it (`assumed`, 6.S10, 10.S13). Without it every program with a host would
# need `--accept assumed`, which would lower the cutoff of every other law too. The demand prices
# assumptions (6.S10): this is the price accepted by default for the observer. Not yet declared in
# demand.lth or demand_model.lut (`theDemand`), so not in DEMAND_DEFAULTS.
AXIOMS = "AssumedGrade"


@dataclass(frozen=True)
class Demand:
    """demand.lth's `Demand` (8.S1): what a run asks of the program, built once by `run` from its
    arguments and `DEMAND_DEFAULTS` before anything is evaluated; every law's demand, the inner
    demand of a first action and the run's record derive from it (L12.3; demand.lth's `lawDemand` and
    `recorded`). `entry` the name as the user writes it; `accepts` the weakest grade
    accepted (test.lth's `Grade`, by constructor name); `sets` each hole's value (`--set`, parsed by
    the hole's type, `fill`), in the order given; `pinned` the interpreter's revision the lock pins,
    None when none does. `decoration` and `delta` are `nothing` in this draft (demand.lth §1).
    `assumes` the provisional externs run as assumed, by name (`--accept assumed:NAME`,
    D-2026-10-16-c); the modes of running (D-2026-10-16-d): `fuel` the reduction steps, None for no
    bound; `time_limit` in seconds, None for none; `strategy` the strategy asked, by constructor
    name; `fresh` whether the store of results is bypassed (L5.20)."""
    entry: str
    accepts: str
    fuel: int | None
    sets: tuple
    checked: bool
    pinned: str | None
    decoration: None = None
    delta: float | None = None
    axioms: str = AXIOMS
    assumes: tuple = ()
    time_limit: float | None = None
    strategy: str = DEMAND_DEFAULTS["strategy"]
    fresh: bool = False
    # [proposed, 3j j2a] how a law's grades combine over its regions and bindings (5.S8,
    # D-2026-10-16-i; certify.COMBINATIONS), the weakest by default (`run --combine`). Not yet
    # declared in demand.lth or demand_model.lut (`theDemand`), as `axioms`, so not in DEMAND_DEFAULTS
    # nor in the record
    combine: str = "weakest"

    def inner(self, entry):
        """demand.lth's `inner`: the demand an inner action receives, every cutoff kept (L12.3)."""
        return replace(self, entry=entry)

    def law(self, law, cone, given, fingerprints, axiom=False):
        """demand.lth's `lawDemand` as certify.serves reads it (certification.lth §3): the law, its
        cone, what the run gives its parameters, and this demand's cutoff, never recomputed.
        [proposed] `given` is what the caller binds: the model parameter and the sets the law
        takes (`certification`), or the model and the action's arguments (`FirstActions`). For a law
        whose body is an axiom (`axiom`), the cutoff is the weaker of `accepts` and `axioms`."""
        return {"law": law, "cone": cone, "given": given, "accepts": self.cutoff(axiom), "fingerprints": fingerprints,
                "combine": self.combine}

    def cutoff(self, axiom=False):
        """The weakest grade accepted for a law: `accepts`, or for an axiom the weaker of it and
        `axioms` (`AXIOMS`)."""
        from . import certify
        if axiom and certify.GRADE_RANK[self.axioms] < certify.GRADE_RANK[self.accepts]:
            return self.axioms
        return self.accepts

    def record(self, cone):
        """demand.lth's `Record` (`recorded`, 12.S18, L5.18): the demand as the run's entry keeps
        it, on the cone it ran. [proposed] the grade by its `--accept` word, as `certification`'s
        `accept`; the parameters as an object, as the entry's `parameters`."""
        from . import certify
        return {"entry": self.entry, "cone": cone, "parameters": dict(self.sets),
                "accept": certify.GRADE_WORDS[self.accepts], "assumes": list(self.assumes), "delta": self.delta,
                "fuel": self.fuel, "timeLimit": self.time_limit, "checked": self.checked, "lock": self.pinned,
                "decoration": self.decoration, "strategy": self.strategy, "fresh": self.fresh}

    def key(self, live_holes):
        """plan.lth's `demandKey` (8.S8, `KeyReadsOnlyTheCone`, `KeyReadsTheType`): the decoration,
        always read, and the values of the holes the live cone reads (`live_holes`, by the names the
        user writes); a hole set that the cone does not read stays in `sets` and the record, not here."""
        return {"decoration": self.decoration, "values": {n: v for n, v in self.sets if n in live_holes}}


def demand_of(main=None, fuel=None, values=(), accept=None, checked=None, pinned=None, assumes=None,
              time_limit=None, strategy=None, fresh=None, combine=None):
    """The run's demand from its arguments, a missing one given its default (`DEMAND_DEFAULTS`,
    demand_model.lut's `theDemand`); `pinned` is what the lock pins (`lock_status`, 12.S13)."""
    d = DEMAND_DEFAULTS
    if strategy is not None and strategy not in RAN:
        raise RunError(f"unknown strategy {strategy}: one of {', '.join(RAN)}")
    from . import certify
    if combine is not None and combine not in certify.COMBINATIONS:
        raise RunError(f"unknown combination {combine}: one of {', '.join(certify.COMBINATIONS)}")
    return Demand(entry=d["entry"] if main is None else main, accepts=accept or d["accepts"],
                  fuel=d["fuel"] if fuel is None else fuel, sets=tuple(dict(values).items()),
                  checked=d["checked"] if checked is None else checked, pinned=pinned,
                  assumes=tuple(dict.fromkeys(d["assumes"] if assumes is None else assumes)),
                  time_limit=d["timeLimit"] if time_limit is None else time_limit,
                  strategy=d["strategy"] if strategy is None else strategy,
                  fresh=d["fresh"] if fresh is None else fresh,
                  combine=certify.COMBINATION if combine is None else combine)


def _head_name(x):
    while isinstance(x, s.App):
        x = x.function
    return x.name if isinstance(x, s.Name) else None


def _provisional_of(x):
    """The provisional externs a surface term holds, as (route, reason) pairs: the reason the
    declaration gives (`(provisional <- "why")`, D-2026-10-16-c), None for `(provisional <- true)`."""
    found = []
    def walk(y):
        if isinstance(y, s.App) and isinstance(y.argument, s.NamedArg) and y.argument.name == "provisional":
            head, route = y.function, None
            while isinstance(head, s.App):
                if isinstance(head.argument, s.Literal) and isinstance(head.argument.literal, s.StringLit):
                    route = head.argument.literal.value
                head = head.function
            value = y.argument.value
            reason = (value.literal.value if isinstance(value, s.Literal) and isinstance(value.literal, s.StringLit)
                      else None)
            found.append((route, reason))
        if isinstance(y, tuple):
            for z in y:
                walk(z)
        elif is_dataclass(y) and not isinstance(y, type):
            for f in fields(y):
                walk(getattr(y, f.name))
    walk(x)
    return found


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

    def theory_args(self, ty):
        """The arguments a type gives its theory head, through aliases (`HostConsole = Host State`:
        [State]); [] when it names none."""
        for _ in range(64):
            name = _head_name(ty)
            if name is None:
                return []
            if self.is_theory(name):
                args = []
                while isinstance(ty, s.App):
                    args.append(ty.argument)
                    ty = ty.function
                return args[::-1]
            ty = self.aliases.get(name, self.bodies.get(name))
            if ty is None:
                return []
        return []

    def _parameters(self, law):
        """The law's definition and its explicit parameters, (name, surface type) in order."""
        define = next((a for a in self.acts.get(law, ()) if isinstance(a, s.Define)), None)
        if define is None or not isinstance(define.body, s.TermBody):
            return None, []
        return define, [(n, b.type) for b in define.binders if isinstance(b, s.Explicit) for n in b.names]

    def _case_shape(self, law, theory):
        """(define, params, k, case): the law's model parameter at `k` ahead of its one parameter
        typed by world.lth's `Observed` at `case`; None when the law has no such shape."""
        define, params = self._parameters(law)
        cases = [k for k, (_, ty) in enumerate(params) if _plain_head(ty) == "Observed"]
        model = self.model_parameter(law, theory)
        if define is None or len(cases) != 1 or model is None:
            return None
        k = next(i for i, (n, _) in enumerate(params) if n == model)
        return (define, params, k, cases[0]) if k < cases[0] else None

    def _projected_actions(self, define, model, theory):
        record = self.declared[theory].type
        actions = {n for f in record.fields for n in f.names if _takes_token(f.type)}
        read = {x.partition(".")[2].split(".")[0] for x in _dotted(define.body.term) if x.startswith(model + ".")}
        return sorted(read & actions)

    def action_law(self, law, theory):
        """[proposed] A law of the theory over a case of one of the model's actions, world.lth's
        `HostAgrees*` and `HostObserveChangesNothing` (a parameter typed by `Observed`, the case
        `agreement` gathers): run at the first application of its action in a run (10.S10, L11.2),
        never by a sampler. Gives {model: the parameter typed by the theory, before: the parameters
        ahead of it (the theory's own), arguments: those between it and the case (the action's, in
        order), field: the one action of the model the law's body projects (a field whose type takes
        the token), case: the case's parameter}; None for any other law."""
        shape = self._case_shape(law, theory)
        if shape is None:
            return None
        define, params, k, case = shape
        model = params[k][0]
        fields_ = self._projected_actions(define, model, theory)
        if len(fields_) != 1:
            return None
        return {"model": model, "before": [n for n, _ in params[:k]],
                "arguments": [n for n, _ in params[k + 1:case]], "field": fields_[0], "case": params[case][0]}

    def frame_law(self, law, theory):
        """[proposed] A law of the theory over a case of any action of the model, world.lth's
        `HostChangesOnlyDeclared` (10.S7): a parameter typed by `Observed`, one typed by `Held` (the
        action the case was gathered from), the places the certifier adds, and no action of the model
        projected. Run on the case of every first action validated (`FirstActions`). Gives {model,
        before, between: the parameters between the model and the case, each with its role ("held",
        "type" for the held's result type, "extra" for the certifier's places), case}; None for any
        other law."""
        shape = self._case_shape(law, theory)
        if shape is None:
            return None
        define, params, k, case = shape
        model = params[k][0]
        if self._projected_actions(define, model, theory):
            return None
        held = [(n, ty) for n, ty in params[k + 1:case] if _plain_head(ty) == "Held"]
        if len(held) != 1:
            return None
        args = []
        ty = held[0][1]
        while isinstance(ty, s.App):
            args.append(ty.argument)
            ty = ty.function
        args.reverse()
        result_type = args[1].name if len(args) > 1 and isinstance(args[1], s.Name) else None
        between = []
        for n, _ in params[k + 1:case]:
            between.append((n, "held" if n == held[0][0] else "type" if n == result_type else "extra"))
        if [r for _, r in between].count("extra") != 1:
            return None
        return {"model": model, "before": [n for n, _ in params[:k]], "between": between, "case": params[case][0]}

    def case_law(self, law, theory):
        """Whether the law is over an observed case (`action_law` or `frame_law`): run by the
        certifier at a first action, never demanded of the store before the run."""
        return self.action_law(law, theory) is not None or self.frame_law(law, theory) is not None

    def axiom_of(self, law):
        """[proposed] The statement of the `axiom` a law's body is, through the definitions its body
        applies (world.lth's `ObserverIsFaithful` is `readsTheWorld S o p`, whose body is an axiom,
        11.R3); None when the body is not an axiom."""
        name = law
        for _ in range(16):
            define, _ = self._parameters(name)
            if define is None:
                return None
            body = define.body.term
            if (isinstance(body, s.App) and isinstance(body.function, s.Name)
                    and body.function.name.partition("@")[0] == "axiom" and isinstance(body.argument, s.Literal)):
                return body.argument.literal.value
            name = _head_name(body)
            if name is None:
                return None
        return None


def _plain_head(ty):
    """The head name of a surface type without the loader's `@file`."""
    name = _head_name(ty)
    return name.partition("@")[0] if name is not None else None


def _takes_token(ty):
    """Whether a surface type is a function whose first argument is the token (an action)."""
    if isinstance(ty, s.Binop) and ty.operator == "->":
        return ty.left == s.World()
    if isinstance(ty, s.Pi):
        return ty.domain == s.World()
    return False


def _dotted(x):
    """The dotted names a surface term mentions (`o.print`)."""
    if isinstance(x, s.Name):
        if "." in x.name:
            yield x.name
    elif isinstance(x, tuple):
        for y in x:
            yield from _dotted(y)
    elif is_dataclass(x) and not isinstance(x, type):
        for f in fields(x):
            yield from _dotted(getattr(x, f.name))


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


def certification(loaded, program, entry, demand, refuse=True):
    """What a run requires (certification.lth §3, 7.S15, 12.S17, 6.S14): the cone of the entry with,
    per name, its demands, read against the stores of the files loaded (12.S11). Gives the
    certification state the run records (12.S18); raises `Refused`, listing each refusal with its
    state, when the store refuses anything of the cone.

    Each name of the cone whose type is a theory head (through aliases) demands each law the
    theory states; a name whose type states no law is certified vacuously ([proposed] 10 of the
    theory, 6.S1). A demand: the law (as a test line names it), the current hash of the law's
    cone, the run's cutoff passed down (`Demand.law`, L12.3), and what the run gives the law:
    [proposed] the name itself to the law's parameter typed by the theory (printed, as a census of
    one prints it), and each hole the run filled with `--set` to the law's parameter of the same
    name (certification.lth's `Demand`); the model's own cone is compared with the fingerprint the
    entry's binding recorded (certify.at). A name built on a provisional extern is refused whole,
    unless the demand names it (`Demand.assumes`, D-2026-10-16-c): then no law of it is demanded and
    it is listed under `assumed` with its reasons and the names of the cone downstream of it, each
    of grade assumed, since the grade propagates to everything built on it. No cutoff accepts a
    failure (D-2026-10-16-h, item 16): a law refuted or in disagreement at the current hash is
    refused whatever the cutoff, unless the demand names the law (`--accept assumed:LAW`); then
    its refusal is lifted, it is listed under `assumed` with the refutation, grade assumed and the
    names downstream of the name that states it, the name counts as failed and not certified, and
    the run warns on standard error (certification.lth's `standingRefusals`, `assumedPast`). A
    name the demand assumes that is neither a provisional nor a refuted law of the cone is warned.

    A law over an observed case (`_Theories.case_law`, world.lth's `Host` laws but the root of
    trust) is run at the action's first application (`FirstActions`), not read here. A law whose
    body is an axiom (`_Theories.axiom_of`, world.lth's `ObserverIsFaithful`) is demanded at the
    demand's cutoff for axioms (`Demand.cutoff`); [proposed] when that cutoff is assumed and no entry
    serves it, it is accepted as the assumption it states and listed under `assumed`, so that the
    run's certificate says under what hypothesis it holds (6.S10, 10.S13).

    With `refuse` false (`eval`, 12.S19, which demands no certificate) nothing is refused: the
    state counts each name of the cone by its state and lists under `refused` each line a refusal
    would have printed. [proposed] A name with several laws not served takes the state of the
    first; a law whose latest entry at the current hash passed but does not serve the cutoff counts
    as uncertified, its line saying why."""
    from . import certify
    accept, values = demand.accepts, dict(demand.sets)
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
    laws = sorted({law for theory in set(stating.values()) for law in theories.laws(theory)
                   if not theories.case_law(law, theory)})
    law_cones = certify.Cones(_elaborated(runtime_slice(loaded.acts, laws[0], core_data(loaded) + tuple(laws)))) \
        if laws else None
    cone, firsts, axioms = [], [], {}
    for n in names:
        demands = []
        if n in stating and n not in provisional:
            theory = stating[n]
            frames = [(law, f) for law in theories.laws(theory) if (f := theories.frame_law(law, theory)) is not None]
            for law in theories.laws(theory):
                action = theories.action_law(law, theory)
                if action is not None:
                    # validated at the action's first application in the run, not before (10.S10)
                    spec = _first_action_spec(loaded, program, cones, theories, n, theory, law, action, frames)
                    if spec is not None:
                        firsts.append(spec)
                    continue
                if theories.frame_law(law, theory) is not None:
                    # run on the case of each first action of the model (`FirstActions`)
                    continue
                given, fingerprints = [], {}
                m = theories.model_parameter(law, theory)
                if m is not None:
                    given.append((m, {"Printed": n.partition("@")[0]}))
                    fingerprints[m] = cones.hash(n)
                params = [p for a in theories.acts.get(law, ()) if isinstance(a, s.Define)
                          for b in a.binders if isinstance(b, s.Explicit) for p in b.names]
                given += [(p, _given(values[p])) for p in params if p in values and p != m]
                axiom = theories.axiom_of(law)
                d = demand.law(law.partition("@")[0], law_cones.hash(law), given, fingerprints, axiom is not None)
                if axiom is not None:
                    axioms[id(d)] = axiom
                demands.append(d)
        cone.append({"name": n.partition("@")[0],
                     "provisional": n in provisional and n.partition("@")[0] not in demand.assumes, "laws": demands})
    stores_read = _stores_read(loaded.files)
    entries = sorted((e for f in loaded.files for e in certify.read_store(f)),
                     key=lambda e: e.get("date", ""), reverse=True)
    # an axiom no entry serves, at a cutoff of assumed: accepted as its assumption (6.S10)
    assumed = []
    for c in cone:
        kept_laws = []
        for d in c["laws"]:
            if (id(d) in axioms and d["accepts"] == "AssumedGrade"
                    and not any(certify.serves_over(d, e, entries) for e in entries)):
                assumed.append({"name": c["name"], "law": d["law"], "axiom": axioms[id(d)],
                                "accept": certify.GRADE_WORDS[d["accepts"]]})
            else:
                kept_laws.append(d)
        c["laws"] = kept_laws
    # a provisional extern the demand names: run as assumed, the grade propagating downstream
    for n in sorted(n for n in provisional if n.partition("@")[0] in demand.assumes):
        plain = n.partition("@")[0]
        reasons = [r or "no reason given" for a in surface.get(n, ()) for _, r in _provisional_of(getattr(a, "body", None))]
        downstream = sorted({m.partition("@")[0] for m in names if m != n and n in cones.names(m)})
        assumed.append({"name": plain, "provisional": reasons, "accept": f"assumed:{plain}", "grade": "assumed",
                        "downstream": downstream})
    refusals = certify.refuse(entries, cone)
    # a refuted law the demand names is run past as assumed, and only by its name: no cutoff
    # accepts a failure (D-2026-10-16-h, item 16; certification.lth's `standingRefusals` and
    # `assumedPast`, `NoCutoffAcceptsAFailure`)
    past = [r for r in refusals if _named_past(demand.assumes, r)]
    refusals = [r for r in refusals if not _named_past(demand.assumes, r)]
    for r in past:
        here = [m for m in names if m.partition("@")[0] == r["name"]]
        downstream = sorted({m.partition("@")[0] for m in names
                             if m not in here and any(h in cones.names(m) for h in here)})
        shown = certify.show_refusal(r, entries)
        assumed.append({"name": r["name"], "law": r["law"], "refuted": shown, "accept": f"assumed:{r['law']}",
                        "grade": "assumed", "downstream": downstream})
        if refuse:
            print(f"warning: running past the refuted law {r['law']} of {r['name']} as assumed "
                  f"(--accept assumed:{r['law']}): {shown}", file=sys.stderr)
    if refuse:
        named = {n.partition("@")[0] for n in provisional} | {r["law"] for r in past}
        for n in demand.assumes:
            if n not in named:
                print(f"warning: --accept assumed:{n} names no provisional extern and no refuted law of the cone",
                      file=sys.stderr)
    if refusals and refuse:
        lines = [certify.show_refusal(r, entries) + (f"; run past it as assumed with --accept assumed:{r['law']}"
                                                      if _refutes(r) else "") for r in refusals]
        raise Refused(f"refused: the cone of {entry.partition('@')[0]} is not certified (accepting "
                      f"{certify.GRADE_WORDS[accept]} and above; 12.S17):\n  " + "\n  ".join(lines), refusals)
    # each refused name by the state of its first refusal (none when `refuse`: they were raised);
    # a name run past a refuted law is not certified, and counts as failed
    refused = {r["name"]: "failed" for r in past}
    for r in refusals:
        kind, what = r["state"]
        refused.setdefault(r["name"], {"Provisional": "provisional", "Stale": "stale"}.get(
            kind, "failed" if kind == "Current" and isinstance(what, dict) and "Failed" in what else "uncertified"))
    with_laws = [c for c in cone if c["laws"] and c["name"] not in refused]
    # the certificates that served the cone (8.S8): for each law demanded, the latest entry that
    # serves it, by the hash of its canonical JSON
    served = {_entry_hash(e) for c in with_laws for d in c["laws"]
              if (e := next((e for e in entries if certify.serves_over(d, e, entries)), None)) is not None}
    at_first = {f["name"] for f in firsts}
    code_only = {"code": cones.cone(entry)["code"], "hosts": [], "interpreter": ""}
    return {"cone": cones.hash(entry), "interpreter": certify.interpreter_revision(),
            # the canonical code's hash apart from the hosts and the interpreter (12.S18): two
            # records with the same fingerprint ran the same code [proposed: certify.cone_hash of
            # the cone's code with no hosts and an empty interpreter]
            "fingerprint": certify.cone_hash(code_only),
            "python": platform.python_version(),
            "hosts": {r: h for r, h in cones.hosts(entry)},
            "accept": certify.GRADE_WORDS[accept],
            "states": {"certified": len(with_laws), "at first action": len(at_first - {c["name"] for c in with_laws}),
                       "vacuous": len([c for c in cone if not c["laws"] and c["name"] not in at_first
                                       and c["name"] not in refused]),
                       **{k: list(refused.values()).count(k) for k in ("provisional", "uncertified", "stale", "failed")}},
            "laws": sum(len(c["laws"]) for c in with_laws), "not certified": sorted(refused),
            # the laws validated at their action's first application (10.S10): what `run` checks
            # as the program asks, and records under "first actions"
            "at first action": [{"action": f["action"], "law": f["law"], "route": f["route"],
                                 "frame": f["frame"]["law"] if f["frame"] else None} for f in firsts],
            # the axioms accepted as assumptions, with no entry (6.S10, 10.S13)
            "assumed": assumed,
            # the certificates that served the cone and the stores read, by hash (8.S8, D-2026-10-15-d)
            "certificates": sorted(served), "stores_read": stores_read,
            "_firsts": firsts,
            # what a refusal would have listed, for `eval` only: a run that starts has none
            **({} if refuse else {"refused": [certify.show_refusal(r, entries) for r in refusals]})}


def _refutes(refusal):
    """certification.lth's `refutes`: a refusal for a failure or a disagreement at the current hash."""
    kind, what = refusal["state"]
    return kind == "Disagrees" or (kind == "Current" and isinstance(what, dict) and "Failed" in what)


def _named_past(assumes, refusal):
    """certification.lth's `namedPast`: a refusal of a refuted law whose name the demand assumes."""
    return refusal["law"] is not None and refusal["law"] in assumes and _refutes(refusal)


def _stores_read(files):
    """The certificate stores a run reads (12.S11), each as [path, sha256 of its bytes], in the
    order of the files loaded, a file with no store left out (D-2026-10-15-d: each run records the
    hash of the stores it read). [proposed] The bytes are hashed just before `certify.read_store`
    reads them; a store written between the two reads is the host's race, outside `W` (L14.4)."""
    import hashlib
    from . import certify
    read = []
    for f in files:
        where = certify.store_path(f)
        if where.exists():
            read.append([str(where), "sha256:" + hashlib.sha256(where.read_bytes()).hexdigest()])
    return read


def _entry_hash(entry):
    """The hash of a certificate's entry (8.S8: the certificates' hashes): sha256 of its canonical
    JSON, as `plan_hash` hashes a plan."""
    from . import certify
    return certify._sha(json.dumps(entry, sort_keys=True, ensure_ascii=False, separators=(",", ":")))


def _first_action_roots(loaded, kept):
    """The action laws (`_Theories.action_law`) of the theories the names of a slice are models of:
    roots of the run's slice, so that the Runner can run them at the action's first application."""
    theories = _Theories(loaded.acts)
    roots = []
    for a in kept:
        if not isinstance(a, (s.Define, s.Declare)) or a.binders:
            continue
        ty = theories.type_of(a.name)
        theory = theories.theory_of(ty) if ty is not None else None
        if theory is None:
            continue
        roots += [law for law in theories.laws(theory)
                  if theories.case_law(law, theory) and law not in roots]
        protocol = _protocol(loaded, theory)
        if protocol is not None and protocol not in roots:
            roots.append(protocol)
    return tuple(roots)


def _protocol(loaded, theory):
    """[proposed] The protocol that gathers a case of the theory's actions: `agreement` of the file
    that declares the theory (world.lth §5); None when that file defines none."""
    home = _home(loaded, theory)
    acts = loaded.by_file.get(home, ()) if home is not None else ()
    return next((a.name for a in acts if isinstance(a, s.Define) and a.name.partition("@")[0] == "agreement"), None)


def _home(loaded, name):
    """The file that defines the program's name `name`: its store keeps the model's entries (12.S11)."""
    for path, acts in loaded.by_file.items():
        if any(getattr(a, "name", None) == name for a in acts):
            return path
    return None


def _first_action_spec(loaded, program, cones, theories, name, theory, law, action, frames=()):
    """What `FirstActions` needs to validate the action of model `name` that `law` holds to its
    description: the route of the model's field, the theory's arguments for the law's leading
    parameters (`S`), the hashes of the law's cone and of the model's (its hosts' code inside,
    6.S8), the file whose store keeps the entry, the protocol (`agreement`) that gathers the case,
    and the frame law run on the same case (`frames`, `_Theories.frame_law`; the first, by order
    written), with its cone's hash."""
    definition = next((a for a in program if isinstance(a, t.Define) and a.name == name), None)
    route = None
    if definition is not None and isinstance(definition.body, t.RecordValue):
        value = dict(definition.body.fields).get(action["field"])
        extern = _extern_of(value) if value is not None else None
        route = extern.route if extern is not None else None
    if route is None:
        # [proposed] an action the model writes in Luthier is not a route: the externs it applies
        # are validated as theirs
        return None
    args = [t.Var(a.name) if isinstance(a, s.Name) else t.Universe()
            for a in theories.theory_args(theories.type_of(name))]
    if len(args) != len(action["before"]):
        raise RunError(f"{law.partition('@')[0]}: {len(action['before'])} parameters before the model, "
                       f"the type of {name.partition('@')[0]} gives its theory {len(args)}")
    plain = name.partition("@")[0]
    protocol = _protocol(loaded, theory)
    if protocol is None:
        raise RunError(f"{law.partition('@')[0]}: no `agreement` beside {theory.partition('@')[0]} gathers its case")
    frame = None
    if frames:
        f_law, f = frames[0]
        if len(f["before"]) != len(args):
            raise RunError(f"{f_law.partition('@')[0]}: {len(f['before'])} parameters before the model, "
                           f"the type of {plain} gives its theory {len(args)}")
        frame = {"law": f_law.partition("@")[0], "internal": f_law, "between": f["between"],
                 "cone": cones.hash(f_law)}
    return {"name": plain, "internal": name, "law": law.partition("@")[0], "law internal": law,
            "action": f"{plain}.{action['field']}", "field": action["field"], "route": route,
            "model": action["model"], "arguments": action["arguments"], "type args": args,
            "law cone": cones.hash(law), "model hash": cones.hash(name), "hosts": cones.hosts(name),
            "home": _home(loaded, name), "protocol": protocol, "frame": frame}


def _printed(value):
    """An argument the host received, as certification.lth's `Value` (`_given`); a value JSON does
    not print, by its repr."""
    try:
        return _given(value)
    except (TypeError, ValueError):
        return {"Printed": repr(value)}


_INFIX = {"+", "-", "*", "/", "==", "/=", "<", "<=", ">", ">=", "and", "or", "mod"}


def _type_shown(term, width=120):
    """A type, a predicate or a value as a refusal at the crossing shows it: `VecOf 3`,
    `0.0 < x`, `{ n := 2, f := [1. 2.] }` (a host array by its entries); cut at `width`."""
    def show(x, inner=False):
        if isinstance(x, Shared):
            return show(x.cell[0], inner)
        if isinstance(x, TypedExtern) and x.obj is not None:
            if isinstance(x.obj, Entries):
                return np.array2string(x.obj.array, threshold=8, separator=" ").replace("\n", "")
            return x.route
        if isinstance(x, t.Lit):
            return json.dumps(x.constant.value, ensure_ascii=False)
        if isinstance(x, t.Var):
            return x.name.partition("@")[0]
        if isinstance(x, t.Proj):
            return f"{show(x.record, True)}.{x.label}"
        if isinstance(x, t.App):
            args, head = [], x
            while isinstance(head, t.App):
                args.append(head.argument)
                head = head.function
            args.reverse()
            if isinstance(head, (t.Var, t.Primitive)) and getattr(head, "name", None) in _INFIX and len(args) == 2:
                text = f"{show(args[0], True)} {head.name} {show(args[1], True)}"
            else:
                text = " ".join([show(head, True)] + [show(a, True) for a in args])
            return f"({text})" if inner else text
        if isinstance(x, t.Pair):
            return f"({show(x.left)}, {show(x.right)})"
        if isinstance(x, t.RecordValue):
            return "{ " + ", ".join(f"{label} := {show(v)}" for label, v in x.fields) + " }"
        if isinstance(x, t.Subtype):
            return f"{{ {x.name} : {show(x.type)} | {show(x.predicate)} }}"
        from .elaborate import show_term
        try:
            return show_term(x)
        except Exception:
            return repr(x)
    text = show(term)
    return text if len(text) <= width else text[:width - 3] + "..."


def _shown(term, width=60):
    """A kernel value as a refusal shows it: a string literal quoted, a constructor applied with its
    arguments, a pair, a record; cut at `width` characters."""
    def show(x):
        if isinstance(x, Shared):
            return show(x.cell[0])
        if isinstance(x, t.Lit):
            return json.dumps(x.constant.value, ensure_ascii=False)
        if isinstance(x, t.Var):
            return x.name.partition("@")[0]
        if isinstance(x, t.App):
            argument = show(x.argument)
            return f"{show(x.function)} ({argument})" if isinstance(x.argument, t.App) else f"{show(x.function)} {argument}"
        if isinstance(x, t.Pair):
            return f"({show(x.left)}, {show(x.right)})"
        if isinstance(x, t.RecordValue):
            return "{ " + ", ".join(f"{label} := {show(v)}" for label, v in x.fields) + " }"
        return repr(x)
    text = show(term)
    return text if len(text) <= width else text[:width - 3] + "..."


class FirstActions:
    """The validation of a host action at its first application in a run (10.S10, L11.2): run's
    model of world.lth's `Host` laws over observed cases (`_Theories.action_law`, `frame_law`). At
    the first application of an action whose model's theory holds it to a law over its case, with
    the run's own arguments: if entries of the model file's store serve the law and the frame law at
    those arguments and the places added (the laws' cones, the model's cone with its hosts' code,
    the grade accepted; certify.serves), the action is applied as usual. [proposed] Only an entry a
    first action wrote serves (its kind, `certify.FIRST_ACTION`, as a control has its own): a
    tester's entry of listed cases on the same model is never the run's own case. Otherwise the Runner
    gathers one case by world.lth's `agreement` (observe the declared places and the places added,
    act once, observe again), with the `Held` the law's body builds (its action the program's, at
    the program's arguments), evaluates the law on the case and the frame law on the same case
    (`HostChangesOnlyDeclared`, over the places added), and hands the program the token `agreement`
    gives back with the case's result: the action is applied once (10.S6). A refuted law refuses the
    run naming the action and the place that differed; confirmed, each law is recorded in the store
    of the file that defines the model (grade `cases`, one case, the binding the model, the run's
    arguments and the places added, 7.S9) and in the run's record (`done`).

    [proposed] The places the certifier adds (world.lth's `extra`, the frame law's parameter): the
    model's standard output (`console.stdout`) and the files the run has read so far
    (host.files_read), in that order, each once; recorded in the entries' binding. A refuted law
    writes no entry; the observations of the protocol pass the token on and change no place
    (`HostObserveChangesNothing`)."""

    def __init__(self, loaded, specs, demand):
        self.loaded, self.demand = loaded, demand
        self.by_route = {}
        for spec in specs:
            # [proposed] two models of the cone with one route: the first, by name, is validated
            self.by_route.setdefault(spec["route"], spec)
        self.done = []

    def entries(self):
        from . import certify
        return sorted((e for f in self.loaded.files for e in certify.read_store(f)),
                      key=lambda e: e.get("date", ""), reverse=True)

    def extra(self, runner, spec):
        """The places the certifier adds to the observation (see the class)."""
        places = []
        try:
            out = runner.whnf(t.Proj(t.Proj(t.Var(spec["internal"]), "console"), "stdout"))
            if isinstance(out, t.Lit) and isinstance(out.constant.value, str):
                places.append(out.constant.value)
        except RunError:
            pass
        for p, _ in host.files_read():
            if p not in places:
                places.append(p)
        return places

    def __call__(self, runner, spec, head, args):
        from . import certify
        function = runner.route(head)
        given, _ = runner.cross_out(head, function, args)
        if len(given) - 1 != len(spec["arguments"]):
            raise RunError(f"{spec['law']}: {len(spec['arguments'])} arguments, {spec['action']} was given "
                           f"{len(given) - 1}")
        printed = [(p, _printed(v)) for p, v in zip(spec["arguments"], given[1:])]
        extra = self.extra(runner, spec)
        frame = spec["frame"]
        extra_name = next((n for n, r in frame["between"] if r == "extra"), "extra") if frame else "extra"
        places = (extra_name, {"Printed": json.dumps(extra, ensure_ascii=False)})
        model = (spec["model"], {"Printed": spec["name"]})
        shown = {p: certify._shown_value(v) for p, v in printed}
        at = ", ".join(f"{p} = {v}" for p, v in shown.items())
        # each validation is an inner action whose entry is the law: it receives the run's demand
        # with every cutoff kept (demand.lth's `inner`, L12.3)
        demands = [(spec["law"], spec["law cone"], self.demand.inner(spec["law"]).law(
            spec["law"], spec["law cone"], [model] + printed + [places], {spec["model"]: spec["model hash"]}))]
        if frame is not None:
            held_name = next(n for n, r in frame["between"] if r == "held")
            held_shown = {"Printed": f"{spec['action']} at {at or 'no argument'}"}
            demands.append((frame["law"], frame["cone"], self.demand.inner(frame["law"]).law(
                frame["law"], frame["cone"], [model, (held_name, held_shown), places],
                {spec["model"]: spec["model hash"]})))
        # [proposed] a first action's demand is served only by an entry a first action wrote: a
        # tester's entry of listed cases on the same model never stands for the run's own case
        # (10.S10; report-e.md, finding 2)
        for _, _, d in demands:
            d["kind"] = certify.FIRST_ACTION
        entries = self.entries()
        served = [next((e for e in entries if certify.serves_over(d, e, entries)), None) for _, _, d in demands]
        if all(e is not None for e in served):
            for (law, _, _), e in zip(demands, served):
                self.done.append({"action": spec["action"], "law": law, "arguments": shown,
                                  "outcome": "served", "entry": e["date"]})
            return None
        values = spec["type args"] + [t.Var(spec["internal"])] + list(args[1:])
        parts = _held_parts(runner.program, spec["law internal"], values)
        if parts is None:
            raise RunError(f"{spec['law']} builds no `held` of {spec['action']}")
        held_term, (S, A, m, act, d), predicate = parts
        extra_term = t.Var("nil")
        for p in reversed(extra):
            extra_term = t.App(t.App(t.Var("cons"), t.Lit(t.StringConst(p))), extra_term)
        gather = t.Var(spec["protocol"])
        for a in (S, A, m, t.Var(spec["internal"]), held_term, extra_term, args[0]):
            gather = t.App(gather, a)
        runner.validating = True
        try:
            pair = runner.whnf(gather)
            if not isinstance(pair, t.Pair):
                raise RunError(f"agreement gave no pair: {_shown(pair)}")
            case = runner.share(pair.right)
            law = t.Var(spec["law internal"])
            for a in values + [case]:
                law = t.App(law, a)
            verdict = runner.whnf(law)
            frame_verdict = t.Var("true")
            if frame is not None:
                roles = {"held": held_term, "type": A, "extra": extra_term}
                applied = t.Var(frame["internal"])
                for a in spec["type args"] + [t.Var(spec["internal"])] + [roles[r] for _, r in frame["between"]] + [case]:
                    applied = t.App(applied, a)
                frame_verdict = runner.whnf(applied)
            result = runner.whnf(t.Proj(case, "result"))
        finally:
            runner.validating = False
        for name, v in ((spec["law"], verdict), (frame and frame["law"], frame_verdict)):
            if v not in (t.Var("true"), t.Var("false")):
                raise RunError(f"{name} gave no Bool: {_shown(v)}")
        if verdict == t.Var("false"):
            where = self.disagreement(runner, m, d, case, predicate)
            refusal = {"name": spec["name"], "law": spec["law"], "state": ("Refuted", where), "action": spec["action"]}
            raise Refused(f"refused: {spec['action']} disagrees with its description at its first action "
                          f"(10.S10, L11.2): {spec['law']} at {at or 'no argument'}: {where}", [refusal])
        if frame_verdict == t.Var("false"):
            where = self.undeclared_change(runner, m, d, case, extra)
            refusal = {"name": spec["name"], "law": frame["law"], "state": ("Refuted", where), "action": spec["action"]}
            raise Refused(f"refused: {spec['action']} changed a place it does not declare at its first action "
                          f"(10.S7, 10.S10): {frame['law']} at {at or 'no argument'}: {where}", [refusal])
        for (law, cone, demand), e in zip(demands, served):
            if e is not None:
                self.done.append({"action": spec["action"], "law": law, "arguments": shown,
                                  "outcome": "served", "entry": e["date"]})
                continue
            entry = self.entry(spec, law, cone, demand)
            where = certify.add_entry(spec["home"], entry) if spec["home"] is not None else None
            self.done.append({"action": spec["action"], "law": law, "arguments": shown,
                              "outcome": "confirmed", "entry": entry["date"],
                              "store": str(where) if where is not None else None})
        return t.Pair(pair.left, result)

    def entry(self, spec, law, cone, demand):
        """certification.lth's `Entry` of a law confirmed at a first action, of its own kind
        (`certify.FIRST_ACTION`): one case, grade `cases`;
        each parameter the run gives a census of one, its value printed in the generator so that two
        arguments are two groups of the store (certify.prune) and its hash its fingerprint; the
        places the certifier added last."""
        from . import certify
        binding = [{"parameter": spec["model"], "generator": f"{spec['name']} (the run's model)",
                    "fingerprint": spec["model hash"]}]
        given = demand["given"]
        for k, (p, v) in enumerate(given[1:], 1):
            what = "the certifier's places" if k == len(given) - 1 else \
                "the action held" if law != spec["law"] else "the run's argument"
            binding.append({"parameter": p, "generator": f"{certify._shown_value(v)} ({what})",
                            "fingerprint": certify._sha(json.dumps(v, sort_keys=True, ensure_ascii=False))})
        return {"law": law, "cone": cone, "binding": binding, "seed": None, "cases": 1, "kind": certify.FIRST_ACTION,
                "budgets": {}, "reach": [{"parameter": p, "reach": {"Members": [v]}} for p, v in demand["given"]],
                "evidence": {"Points": {"evaluated": 1, "raised": 0, "coverage": "Listed", "verdict": "Supported"},
                             "protocol": "first action (10.S10)", "route": spec["route"]},
                "grade": "Cases", "outcome": "Passed", "date": certify.now(),
                "interpreter": certify.interpreter_revision(), "hosts": [list(h) for h in spec["hosts"]]}

    @staticmethod
    def _strings(runner, xs):
        out = []
        xs = runner.whnf(xs)
        while isinstance(xs, t.App) and isinstance(xs.function, t.App) and runner.whnf(xs.function.function) == t.Var("cons"):
            p = runner.whnf(xs.function.argument)
            if isinstance(p, t.Lit):
                out.append(p.constant.value)
            xs = runner.whnf(xs.argument)
        return out

    @staticmethod
    def _read(runner, m, st, p):
        return t.App(t.App(t.Proj(m, "read"), st), t.Lit(t.StringConst(p)))

    def _differs(self, runner, m, a, b, p, said):
        ra, rb = self._read(runner, m, a, p), self._read(runner, m, b, p)
        if runner.whnf(t.App(t.App(t.Var("=="), ra), rb)) == t.Var("false"):
            return f"the place {p} differs ({said[0]} {_shown(runner.value(ra))}, {said[1]} {_shown(runner.value(rb))})"
        return None

    def disagreement(self, runner, m, d, case, predicate):
        """Where a refuted case differed from the description: each declared place (`d.places`) at
        which the world the description gives reads otherwise than the world observed after the
        action, then the result; for an observation (world.lth's `observes`), each place at which
        its result or the world after reads otherwise than the world before."""
        declared = self._strings(runner, t.Proj(d, "places"))
        before, after, result = (t.Proj(case, f) for f in ("before", "after", "result"))
        differing = []
        if predicate == "observes":
            for p in declared:
                w = self._differs(runner, m, before, result, p, ("before", "observed"))
                w = w or self._differs(runner, m, before, after, p, ("before", "after"))
                if w:
                    differing.append(w)
            return "; ".join(differing) or "the law is refuted"
        described = runner.whnf(t.App(t.Proj(d, "describe"), before))
        if not isinstance(described, t.Pair):
            return "the law is refuted"
        for p in declared:
            w = self._differs(runner, m, described.left, after, p, ("described", "observed"))
            if w:
                differing.append(w)
        if runner.whnf(t.App(t.App(t.Var("=="), described.right), result)) == t.Var("false"):
            differing.append(f"the result differs (described {_shown(runner.value(described.right))}, "
                             f"given {_shown(runner.value(result))})")
        return "; ".join(differing) or "the law is refuted"

    def undeclared_change(self, runner, m, d, case, extra):
        """Where a refuted frame law differed: each place added and not declared at which the world
        after reads otherwise than the world before (world.lth's `undeclared`)."""
        declared = self._strings(runner, t.Proj(d, "places"))
        before, after = t.Proj(case, "before"), t.Proj(case, "after")
        differing = [w for p in extra if p not in declared
                     if (w := self._differs(runner, m, before, after, p, ("before", "after")))]
        return "; ".join(differing) or "the law is refuted"


def _held_parts(program, law_internal, values):
    """The application of world.lth's `held` in the law's body, its parameters but the case given
    the run's values: (the application, its five arguments S A m act d, the predicate it is handed
    to, `agrees` or `observes`); None when the body applies none."""
    law = next((a for a in program if isinstance(a, t.Define) and a.name == law_internal), None)
    if law is None:
        return None
    body = law.body
    for v in values:
        if not isinstance(body, t.Lam):
            return None
        body = kernel.substitute(body.name, v, body.body)

    def spine(x):
        head, xs = x, []
        while isinstance(head, t.App):
            xs.append(head.argument)
            head = head.function
        xs.reverse()
        name = head.name.partition("@")[0] if isinstance(head, t.Var) else None
        return name, xs

    def find(x, outer):
        name, xs = spine(x)
        if name == "held" and len(xs) >= 5:
            return x, tuple(xs[:5]), outer
        if name in ("agrees", "observes"):
            outer = name
        if isinstance(x, tuple):
            for y in x:
                if (r := find(y, outer)) is not None:
                    return r
        elif is_dataclass(x) and not isinstance(x, type):
            for f in fields(x):
                if (r := find(getattr(x, f.name), outer)) is not None:
                    return r
        return None
    return find(body, None)


def provisionals(kept):
    """The names of the slice built on a provisional extern (4.R5), as the user writes them, each
    with its routes and reasons (`_provisional_of`)."""
    found = {}
    for a in kept:
        if isinstance(a, s.Define) and _provisional(a.body):
            found.setdefault(a.name.partition("@")[0], []).extend(_provisional_of(a.body))
    return found


def refuse_provisional(kept, entry, assumes=()):
    """A name of the slice built on a provisional extern (4.R5) is refused whole (6.S14, 12.S17,
    `ProvisionalIsRefused`), before the slice is elaborated: the elaborator does not read the
    extern's `(provisional <- ...)`, unless the demand names it among those it runs as assumed
    (`assumes`, `run --accept assumed:NAME`; world.lth's `AppliedWhenSettled`, D-2026-10-16-c).
    A bare `--accept assumed` accepts none. [proposed] The laws of the rest of the cone are then
    not listed: a provisional name not named refuses the run whatever the store holds. Gives the
    provisional names accepted, each with its routes and reasons."""
    found = provisionals(kept)
    names = sorted(n for n in found if n not in assumes)
    if names:
        refusals = [{"name": n, "law": None, "state": ("Provisional", None)} for n in names]
        lines = [f"{n}: provisional ({'; '.join(r or 'no reason given' for _, r in found[n])}); "
                 f"run it as assumed with --accept assumed:{n}" for n in names]
        raise Refused(f"refused: the cone of {entry.partition('@')[0]} is not certified (12.S17):\n  "
                      + "\n  ".join(lines), refusals)
    # a name that is neither a provisional nor a refuted law of the cone is warned by `certification`
    return {n: found[n] for n in sorted(found)}


def run(path, main=None, fuel=None, sets=(), accept=None, checked=None, fresh=None, assumes=None,
        time_limit=None, strategy=None, combine=None):
    """Run `main` of the file at `path` with its holes filled by `sets`, once the store certifies
    its cone at the grade `accept` (12.S17; `Refused` otherwise, before anything is evaluated);
    gives the standard output, the values set and the certification state of the cone. `checked`
    (`run --checked`, 12.S18): each value an extern gives at a declared subtype has its predicate
    evaluated as it crosses (4.R5), a refuted one refusing the run; the state then says so and
    counts the refinements tested per route. An argument not given takes demand_model.lut's
    default (`DEMAND_DEFAULTS`).

    The run's demand (demand.lth's `Demand`) is built once, as soon as the values of `--set` are
    read by their holes' types, and everything after derives from it: the demand on each law and
    on each first action (demand.lth's `lawDemand`), and the record (`recorded`). The
    state carries the demand as recorded (`demand`), the plan (`plan`: the strategy, the live cone,
    the call-by-need schedule and its hash, plan.lth's `Plan`, L5.6) and the demand's key (`key`,
    plan.lth's `DemandKey`, `KeyReadsOnlyTheCone`).

    The store of results (8.S3, 8.S8, 8.S10; D-2026-10-15-d): the run's key (`result_key`, plan.lth's
    `keyOf`) is computed before anything is evaluated, and its hash is recorded (`key_hash`). When the
    live cone performs no action (`acts`) and `x.results.json` holds the key with one value, the run
    is served from it without evaluating; its state names the entry (`result_store`'s `served`). A
    cone that acts always executes. `fresh` (`run --fresh`, L5.20) executes whatever the store holds;
    `record` then writes nothing if the value agrees and keeps both if it does not.

    The modes of running are fields of the demand (D-2026-10-16-d), each recorded: `fuel` (reduction
    steps) and `time_limit` (seconds) cut the run, neither bound by default; `strategy` the one
    asked, forward on demand by default, which call by need computes as its specimen (`RAN`; the
    plan records the strategy that ran, `TheDefaultsAgree`); `fresh`. `assumes` names the
    provisional externs the run applies as assumed (`refuse_provisional`, D-2026-10-16-c); each
    warns on standard error at its first application, and the certification lists it under
    `assumed` with the names of the cone downstream of it, whose grade is then assumed. It names
    too the refuted laws the run goes past as assumed (`certification`, D-2026-10-16-h). The file is
    a run (`x.run.lut`, 12.R2), refused otherwise before anything is read.

    A run cut by its time limit or its fuel raises `Cut`, which carries the values and the state
    `record` appends as a run that did not finish; it writes nothing to `x.results.json`."""
    require_kind(path, "run")
    host.reset()
    lock = lock_status(path)
    loaded = Loaded(path)
    values, empty = fill(loaded, sets)
    demand = demand_of(main, fuel, values, accept, checked, lock["pinned"], assumes, time_limit, strategy, fresh,
                       combine)
    entry = loaded.name(loaded.top, demand.entry) or demand.entry
    kept = runtime_slice(loaded.acts, entry, core_data(loaded))
    roots = _first_action_roots(loaded, kept)
    if roots:
        kept = runtime_slice(loaded.acts, entry, core_data(loaded) + roots)
    loaded.demand(kept)
    for a in kept:
        if isinstance(a, s.Declare) and a.name in empty:
            name = empty[a.name]
            raise RunError(f"{name} : {_show_type(a.type)} is a hole of {loaded.top.name} the run needs; "
                           f"give it with --set {name}=...")
    accepted = refuse_provisional(kept, entry, demand.assumes)
    program = _elaborated(kept)
    definition = next((a for a in program if isinstance(a, t.Define) and a.name == entry), None)
    if definition is None:
        raise RunError(f"missing main: {demand.entry}")
    state = certification(loaded, program, entry, demand) or {}
    live = live_cone(kept)
    live_holes = {n for n, _ in demand.sets if loaded.internal(loaded.top, n) in set(live)}
    # the strategy that ran, the specimen of the one asked (demand.lth's `Ran`, 8.S4)
    plan = {"strategy": RAN[demand.strategy], "entry": demand.entry, "live": list(live), "schedule": []}
    pure = not acts(program, live)
    seed = None  # [proposed] a run draws nothing today; the seed of 8.S8 is `nothing`
    certificates = state.pop("certificates", [])
    known = {"demand": demand.record(state.get("cone")), "key": demand.key(live_holes)}
    key = result_key(known, seed, plan, certificates)
    common = dict(lock=lock, checked=demand.checked, demand=known["demand"], key=known["key"], seed=seed,
                  certificates=certificates, key_hash=key_hash(key))
    if pure and not demand.fresh:
        results = read_results(path)
        i = served_by(results, key)
        if i is not None:
            state.pop("_firsts", None)
            plan["hash"] = plan_hash(plan)
            return "", values, dict(state, fuel={"given": demand.fuel, "spent": 0}, **{"first actions": []},
                                    files_read=[], plan=plan, **common,
                                    result_store={"pure": True, "fresh": False, "served": {
                                        "store": str(results_path(path)), "entry": i,
                                        "key hash": results[i]["key hash"], "time": results[i]["time"]}})
    runner = Runner(program, demand.fuel, demand.checked, demand.time_limit)
    for n, pairs in accepted.items():
        for route, reason in pairs:
            if route is not None:
                names, why = runner.provisional.get(route, ((), reason))
                runner.provisional[route] = (names + (n,), why)
    firsts = FirstActions(loaded, state.pop("_firsts", []) if state else [], demand)
    runner.first = firsts.by_route
    runner.validate = firsts
    value = t.Var(entry)
    if isinstance(definition.type, t.Pi) and isinstance(definition.type.domain, t.World):
        value = t.App(value, runner.token)
    try:
        result = runner.whnf(value)
        if isinstance(result, t.Pair):
            runner.whnf(result.left)  # Demand the final world chain, even for a lazy pair.
    except Exception as exc:
        if runner.cut is None:
            raise
        # cut by its time limit or its fuel: recorded as a run that did not finish, with its demand,
        # the steps reached and the reason; nothing goes to the store of results
        reason, message = runner.cut
        plan["schedule"] = list(runner.schedule)
        plan["hash"] = plan_hash(plan)
        cut_state = dict(state, fuel={"given": demand.fuel, "spent": runner.steps},
                         **{"first actions": firsts.done}, files_read=[list(pair) for pair in host.files_read()],
                         plan=plan, **common, result_store={"pure": pure, "fresh": demand.fresh, "written": None})
        raise Cut(message, reason, runner.steps, values, cut_state) from exc
    plan["schedule"] = list(runner.schedule)
    plan["hash"] = plan_hash(plan)
    spent = runner.steps
    store = {"pure": pure, "fresh": demand.fresh}
    if pure:
        # the value printed, as `eval` prints it (12.S19), what the store keeps under the key
        store.update(key=key, value=_type_shown(runner.value(result), sys.maxsize))
    state = dict(state, fuel={"given": demand.fuel, "spent": spent},
                 **{"first actions": firsts.done}, files_read=[list(pair) for pair in host.files_read()],
                 plan=plan, **common, result_store=store)
    if demand.checked:
        state["refinements"] = dict(runner.tested)
    return host.stdout(), values, state


def live_cone(kept):
    """plan.lth's `reaches` as `run` computes it: the names of the slice `runtime_slice` keeps for
    the entry (the backward pass over names, 8.S3, L5.13), each once, in the program's order (core
    first, then each file after its imports). [proposed] The roots of the slice are in it: core's
    data, which every run may read, and the laws run at a first action (10.S10)."""
    return tuple(dict.fromkeys(a.name for a in kept if isinstance(a, (s.Define, s.Declare, s.Alias))))


def _holds_world(x):
    """Whether a kernel term holds the world `W` anywhere."""
    if isinstance(x, t.World):
        return True
    if isinstance(x, tuple):
        return any(_holds_world(y) for y in x)
    if is_dataclass(x) and not isinstance(x, type):
        return any(_holds_world(getattr(x, f.name)) for f in fields(x))
    return False


def acts(program, live):
    """Whether the live cone performs an action (D-2026-10-15-d): a name of it whose type or
    definition holds the world `W`. [proposed] Read from the elaborated code before anything is
    evaluated, so a name that holds `W` and is never applied counts too, the safer reading (10.S6:
    an action with no declaration counts as one on the world)."""
    live = set(live)
    return any(_holds_world(a) for a in program if isinstance(a, (t.Define, t.Declare)) and a.name in live)


def chosen_plan(plan):
    """plan.lth's `chosen`: the plan as chosen before it runs, its schedule empty; call by need
    writes the schedule as it runs (8.S4), and a key read before evaluating cannot hold it."""
    return {"strategy": plan["strategy"], "entry": plan["entry"], "live": list(plan["live"]), "schedule": []}


def result_key(record, seed, plan, certificates):
    """plan.lth's `keyOf` (8.S8, D-2026-10-15-h): the key of a run from its record (`demand`,
    demand.lth's `Record`, and `key`, plan.lth's `demandKey` of it on the plan's live cone, which
    holds the decoration from the record), its seed, its plan, as chosen, and the hashes of the
    certificates that served its cone. The fuel, the time and the lock are in the record and not
    here (D-2026-10-15-g). `record` is an entry of `x.run.json` or anything with those two fields."""
    return {"demand": record["key"], "cone": record["demand"]["cone"],
            "mode": "checked" if record["demand"]["checked"] else "plain", "seed": seed,
            "plan": plan_hash(chosen_plan(plan)), "certificates": list(certificates)}


def key_hash(key):
    """plan.lth's `Keying.key`: sha256 of the key's canonical JSON, as `plan_hash` hashes a plan."""
    from . import certify
    return certify._sha(json.dumps(key, sort_keys=True, ensure_ascii=False, separators=(",", ":")))


def results_path(path):
    """`x.results.json` beside `x.run.lut` (L10.12: in the store of the file that makes the claim;
    `base_name`, 12.R2)."""
    path = Path(path)
    return path.with_name(base_name(path) + ".results.json")


def read_results(path):
    """The entries of `x.results.json` beside `x.lut` (or at `path` itself): each {"key hash",
    "key", "value", "time"}, in the order written; [] when there is none."""
    path = Path(path)
    where = path if path.name.endswith(".results.json") else results_path(path)
    if not where.exists():
        return []
    results = json.loads(where.read_text(encoding="utf-8"))
    if not isinstance(results, list):
        raise RunError(f"{where}: not a list of results")
    return results


def served_by(results, key):
    """The index of the entry that serves `key` (8.S9: a hit needs an equal key): the first whose
    key equals it and hashes to the hash it is stored under, when every entry of that hash holds
    one value; None when there is none, or when they disagree (`results_breaches`, plan.lth's
    `ResultsDetermined` broken: not served until the discrepancy is resolved, D-2026-10-15-f)."""
    h = key_hash(key)
    same = [i for i, r in enumerate(results) if r.get("key hash") == h]
    if not same or len({json.dumps(results[i].get("value")) for i in same}) != 1:
        return None
    return next((i for i in same if results[i].get("key") == key and key_hash(results[i]["key"]) == h), None)


def results_breaches(results):
    """plan.lth's `ResultsDetermined` as the pairs (i, j), i < j, that break it: one key hash, two
    values."""
    return [(i, j) for j, b in enumerate(results) for i, a in enumerate(results[:j])
            if a.get("key hash") == b.get("key hash") and a.get("value") != b.get("value")]


def store_result(path, store, key_h, time):
    """Write a pure run's value under its key in `x.results.json` (D-2026-10-15-d), unless an entry
    of that key already holds it; gives what the record says: `agrees` (the entry that already
    held it, nothing written) or `written` (its index), with `disagrees` (the entries of the key
    holding another value: both kept, D-2026-10-15-f)."""
    where = results_path(path)
    results = read_results(path)
    same = [i for i, r in enumerate(results) if r.get("key hash") == key_h]
    agree = [i for i in same if results[i].get("value") == store["value"]]
    if agree:
        return {"agrees": agree[0]}
    results.append({"key hash": key_h, "key": store["key"], "value": store["value"], "time": time})
    tmp = where.with_name(where.name + ".tmp")
    tmp.write_text(json.dumps(results, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(where)
    said = {"written": len(results) - 1}
    if same:
        said["disagrees"] = same
    return said


def plan_hash(plan):
    """plan.lth's `planHash` (L5.6, `PlanHashSeesTheSchedule`): sha256 of the plan's strategy,
    entry, live cone and schedule, as `certify.cone_hash` hashes a cone (canonical JSON)."""
    from . import certify
    payload = {k: plan[k] for k in ("strategy", "entry", "live", "schedule")}
    return certify._sha(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


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


def run_file(path, main=None, fuel=None, sets=(), accept=None, checked=None, fresh=None, assumes=None,
             time_limit=None, strategy=None):
    return run(path, main, fuel, sets, accept, checked, fresh, assumes, time_limit, strategy)[0]


def record_path(path):
    """`x.run.json` beside `x.run.lut` (12.S18; `base_name`, 12.R2)."""
    path = Path(path)
    return path.with_name(base_name(path) + ".run.json")


def record(path, main, values, output, state=None, cut=None):
    """Append this run to `x.run.json` beside `x.lut` (12.S18): the entry, the time, the
    parameters, the output, the calls the host made back into Luthier during the run (`calls`:
    receiving extern's route -> position among its arguments -> count, D-2026-10-14-a), and the
    certification state of the cone (`certification`: the hash of the entry's cone, the
    interpreter's revision, the grade accepted, the counts of states of the cone's names and the
    names not certified, empty since a run starts only on a certified cone, the fingerprint of the
    cone's code, the Python's and the hosts' versions), the fuel given and spent, the files read
    with the hash of their bytes (`files_read`) and the lock (`lock`: its path, the revision it
    pins and whether the run `matches` it, `differs`, or found it `absent` and wrote it), whether
    it ran `--checked` (`checked`) and then the refinements tested per route (`refinements`).

    The demand as one object (`demand`, demand.lth's `Record`: entry, cone, parameters, accept,
    assumes, delta, fuel, timeLimit, checked, lock, decoration, strategy, fresh), the plan (`plan`,
    with the strategy that ran) and the demand's key (`key`). [proposed] The
    fields that were there before are kept beside it, with the same values: `entry`, `parameters`,
    `checked` and `certification.accept`, which tests and readers of the record read; `fuel` and
    `lock`, which hold the run's part too (the fuel spent, the lock's path and status).

    The store of results (D-2026-10-15-d, D-2026-10-15-h): the hash of the run's key (`key_hash`),
    with the seed and the certificates that served the cone (`seed`, `certificates`), from which
    and from `demand`, `key` and `plan` the key is computed again (`result_key`); the hash of the
    bytes of each certificate store read (`stores_read`); and `result_store`: whether the cone is
    pure, whether the run was `--fresh`, and the entry of `x.results.json` that served it
    (`served`), or, for a pure run executed, what `store_result` did with its value under the
    record's time. Each is said on standard error.

    A run cut by its time limit or its fuel (`cut`, a `Cut`) is appended as a run that did not
    finish: `finished` false, `cut` with the reason, the steps reached and the message, its demand,
    plan and certification as for any run, no `output`; nothing is written to `x.results.json`,
    and `breaches` and the store of results never read it."""
    from datetime import datetime, timezone
    where = record_path(path)
    runs = json.loads(where.read_text(encoding="utf-8")) if where.exists() else []
    item = {"entry": main, "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "parameters": values, "output": output, "calls": host.calls()}
    if cut is not None:
        del item["output"]
        item["finished"] = False
        item["cut"] = {"reason": cut.reason, "steps": cut.steps, "message": str(cut)}
    if state is not None:
        state = dict(state)  # a copy: the entry takes fuel, files_read and lock out of it
        for key in ("demand", "plan", "key", "key_hash", "seed", "certificates", "fuel", "files_read",
                    "stores_read", "lock", "checked", "refinements", "result_store"):
            if key in state:
                item[key] = state.pop(key)
        store = item.get("result_store")
        if store is not None and cut is None:
            item["result_store"] = store = dict(store)
            _say_store(path, store, item)
        lock = item.get("lock")
        if lock and lock["status"] == "absent":
            from . import certify
            Path(lock["path"]).write_text(json.dumps({"interpreter": certify.interpreter_revision()}) + "\n",
                                          encoding="utf-8")
            lock["pinned"], lock["status"] = certify.interpreter_revision(), "written"
        item["certification"] = state
    runs.append(item)
    where.write_text(json.dumps(runs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if cut is not None:
        print(f"{where.name}: recorded as a run that did not finish ({cut.reason}, {cut.steps} steps); "
              f"nothing stored in {results_path(path).name}", file=sys.stderr)
    return where


def _say_store(path, store, item):
    """`record`'s part for the store of results: a pure value executed is stored (`store_result`)
    and the key and the value move out of the record's `result_store` (the record keeps the key's
    hash); what happened is said on standard error."""
    name = results_path(path).name
    if "served" in store:
        served = store["served"]
        print(f"served from {name}, entry {served['entry']} of {served['time']} (8.S9; --fresh executes it)",
              file=sys.stderr)
        return
    if not store.get("pure"):
        return
    key, value = store.pop("key"), store.pop("value")
    store.update(store_result(path, {"key": key, "value": value}, item["key_hash"], item["time"]))
    if "disagrees" in store:
        print(f"{name}: this run's value differs from entries {store['disagrees']} under the same key; both kept "
              f"(entry {store['written']}), and the key is not served until the discrepancy is resolved",
              file=sys.stderr)
    elif "agrees" in store and store.get("fresh"):
        print(f"--fresh: the value agrees with entry {store['agrees']} of {name}; nothing written", file=sys.stderr)
    elif "agrees" in store:
        print(f"{name}: not served, its entries under this key disagree; this run agrees with entry "
              f"{store['agrees']}", file=sys.stderr)


def read_runs(path):
    """The runs `x.run.json` holds beside `x.lut` (or at `path` itself), and the breaches of
    demand.lth's `determined` among them (its `Store`'s `OneIdentityOneResult`, 8.S3): each pair
    (i, j), i < j, of runs with one demand record (`demand`) and two outputs. Nothing is served from them yet (8.S10). [proposed] A
    run recorded before the demand was (no `demand`) is in the list and in no pair."""
    path = Path(path)
    where = path if path.name.endswith(".run.json") else record_path(path)
    runs = json.loads(where.read_text(encoding="utf-8")) if where.exists() else []
    return runs, breaches(runs)


def breaches(runs):
    """demand.lth's `determined`, as the pairs that break it: two runs with an equal `demand` and
    different `output`s. A run that did not finish (`finished` false, cut by a limit) gave no
    output and enters no pair."""
    found = []
    for j, b in enumerate(runs):
        for i, a in enumerate(runs[:j]):
            if a.get("finished", True) is False or b.get("finished", True) is False:
                continue
            if "demand" in a and a.get("demand") == b.get("demand") and a.get("output") != b.get("output"):
                found.append((i, j))
    return found


class Probe(Loaded):
    """`luthier eval files term`'s context (12.S19): the files loaded with their imports and core
    exactly as `run` loads one (`Loaded`), and the term as the one definition of a file of its own,
    `<eval>`, beside the first of them, which sees what each of the files sees (its definitions,
    its constructors and labels, the names its imports list) and nothing else. [proposed] A name two
    of the files give is the first file's; the term's definition takes the first of `it`, `it1`,
    ... that none of the files sees, so the term cannot name itself."""

    NAME = "<eval>"

    def __init__(self, files, term, core=True):
        self.context = tuple(Path(f).resolve() for f in files)
        self.term = term
        self.it = None
        # [proposed] with no file (a session's, 12.S20), the term sees core alone, from the
        # current directory
        super().__init__((self.context[0].parent if self.context else Path.cwd().resolve()) / self.NAME, core)

    def visit(self, path, active):
        if path.resolve() != self.top:
            return super().visit(path, active)
        active.add(path)
        f = _File(path)
        for target in self.context:
            if not target.exists():
                raise RunError(f"no file {target}")
            self.visit(target, active)
            g = self.files[target]
            for name in sorted(g.defined | g.labels | set(g.imports)):
                f.imports.setdefault(name, (target, name))
        k = 0
        while (it := "it" + (str(k) if k else "")) in f.imports:
            k += 1
        result = parse(f"{it} := {self.term}")
        if isinstance(result, s.ParseFailed):
            raise RunError("; ".join(f"the term: {e.message}" for e in result.errors))
        if len(result.program) != 1 or not isinstance(result.program[0], s.Define):
            raise RunError("the term is not one term")
        self.it = it
        f.acts.extend(result.program)
        f.defined.add(it)
        _sum_labels(result.program, f.labels)
        active.remove(path)
        self.files[path] = f


def evaluate(files, term, fuel=None):
    """`luthier eval files term` (12.S19): the value of `term` in the context of `files` (`Probe`),
    its inferred type, and the states of its cone. The probe that records nothing (D-2026-10-12-ah):
    no `x.run.json`, no lock, no store written, no certificate demanded; the states are read from
    the stores of the files loaded, as `run` reads them, and printed beside the value so that it is
    never taken for a certified result. The value is reduced in every concrete part
    (`Runner.value`); a function, or a computation stuck on a hole, stays as it is. [proposed] The
    states are read at the demand's default cutoff (`DEMAND_DEFAULTS`), and a law the stores do not
    serve is listed, not refused; the first actions of 10.S10 are not validated, since `eval` gives
    its term no world and so performs no action. Gives (value, type, states), the states as
    `certification` gives them with `refused` set, or {"error": why} when they cannot be read."""
    if not files:
        raise RunError("eval needs a file")
    host.reset()
    loaded, program, entry, definition, demand, states = _probed(files, term, fuel)
    states.pop("_firsts", None)
    runner = Runner(program, demand.fuel)
    value = runner.value(t.Var(entry))
    return value, definition.type, states


def _probed(files, term, fuel=None, actions=False):
    """The probe's context, its elaborated program, the term's internal name and definition, the
    demand and the states of the term's cone (`evaluate`). With `actions`, the laws run at a first
    action (10.S10) are roots of the slice as in `run`, and the states keep their `_firsts`."""
    loaded = Probe(files, term)
    entry = loaded.internal(loaded.top, loaded.it)
    kept = runtime_slice(loaded.acts, entry, core_data(loaded))
    roots = _first_action_roots(loaded, kept) if actions else ()
    if roots:
        kept = runtime_slice(loaded.acts, entry, core_data(loaded) + roots)
    loaded.demand(kept)
    program = _elaborated(kept)
    definition = next(a for a in program if isinstance(a, t.Define) and a.name == entry)
    demand = demand_of(loaded.it, fuel)
    try:
        states = certification(loaded, program, entry, demand, refuse=False)
    except (RunError, OSError, RecursionError) as exc:
        states = {"error": str(exc)}
    return loaded, program, entry, definition, demand, states


def show_states(states):
    """The lines `eval` prints after the value (12.S19): the counts of the states of the cone's
    names that are not zero, then each law or name not certified with its state."""
    if "error" in states:
        return [f"states: not read ({states['error']})"]
    counts = ", ".join(f"{n} {k}" for k, n in states["states"].items() if n) or "no names"
    lines = [f"states of the cone, accepting {states['accept']} and above: {counts}"]
    lines += [f"  {line}" for line in states.get("refused", ())]
    return lines


class Session:
    """`luthier session [files]` (12.S20, 2.S18, 8.S12, 8.S13): a block built one item per line
    over the files, loaded with their imports and core as `eval` loads them (`Probe`). An item
    (`x := t`, `p <- t`) joins the block when it evaluated; a bare term is evaluated as the block
    so far ending in it, `{ items ; term }`, and printed with its type and the states of its cone
    as `eval` prints them; it does not join. Each line re-evaluates the block so far, with no memo
    (8.S13). The session's own rules, which `eval` does not read: `:=` defines once (2.R3), `<-`
    rebinds only a name first bound with `<-` or the block's parameter `w` (2.R4), and a rebinding
    whose previous binding had no consumer is a note, not a refusal (2.R6). Nothing is recorded:
    no `x.run.json`, no lock (12.S19's probe).

    [proposed] With `world` (`--world`; 12.S20 is silent on actions, 2.S18 and 10.S2 put the world
    of the session block in `w`), the block is the body of `fn (w : W)` applied to the run's token,
    and an action's first application in the session is validated as `run` validates it (10.S10,
    `FirstActions`), served by the stores but writing no entry. An action is performed once, when
    the line that applies it is entered: re-evaluating the block serves the actions already
    performed from the session's log, in the order of the token's chain, so a print is not printed
    again. Without `world` there is no token in the session, and no action can be applied."""

    def __init__(self, files, world=False, fuel=None):
        self.files, self.world, self.fuel = list(files), world, fuel
        self.items = []              # the source of the items joined, in order
        self.defined = set()         # the names bound with `:=` (2.R3)
        self.rebindable = {"w"} if world else set()   # first bound with `<-`, or the parameter (2.R4)
        self.pending = {"w"} if world else set()      # bound with `<-` and not consumed since (2.R6)
        self.log = []                # the actions performed: (route, literal arguments, result)
        self.validated = set()       # the routes validated at their first action (10.S10)
        self.done = []               # what the validations did (FirstActions.done)
        host.reset()
        self.printed = 0             # the length of the host's standard output already shown
        self.context = Probe(self.files, "0")

    def _sees(self, name):
        return self.context.name(self.context.top, name) is not None

    def _binds(self, pattern):
        from .check import pattern_binds
        return {n for n in pattern_binds(pattern, frozenset())
                if not self.context.is_constructor(self.context.top, n)}

    @staticmethod
    def classify(text):
        """The line as an item (`s.Bind` or `s.Rebind`) or a term (its surface form)."""
        result = parse(f"it := {{ {text} ; 0 }}")
        if isinstance(result, s.Parsed) and len(result.program) == 1:
            body = getattr(result.program[0].body, "term", None)
            if isinstance(body, s.Block) and len(body.items) == 1:
                return body.items[0]
        result = parse(f"it := {text}")
        if isinstance(result, s.ParseFailed):
            raise RunError("; ".join(e.message for e in result.errors))
        if len(result.program) != 1 or not isinstance(result.program[0], s.Define):
            raise RunError("not an item of a block nor a term")
        return result.program[0].body.term

    def term(self, final, item=None):
        """The block so far, with the line's `item` when there is one, ending in `final`, as the
        probe's term."""
        items = self.items + ([item] if item is not None else [])
        body = "; ".join(items + [final])
        if self.world:
            return f"fn (w : W) {{ {body} }}"
        return f"{{ {body} }}" if items else final

    def line(self, text):
        """One line of the session: gives the lines to print (notes, the standard output the
        line's actions gave, a term's value with its type and the states); RunError when the line
        is refused, the block then unchanged."""
        from .check import names
        text = text.strip().rstrip(";").strip()
        if not text or text.startswith("--"):
            return []
        if text == ":items":
            return list(self.items) or ["(no items)"]
        if text.startswith(":"):
            raise RunError(f"{text.split()[0]}: not a command (:items, :quit)")
        parsed = self.classify(text)
        notes = []
        if isinstance(parsed, (s.Bind, s.Rebind)):
            used = names(parsed.value)
            if isinstance(parsed, s.Bind):
                x = parsed.name
                if x in self.defined or x in self.rebindable or self._sees(x):
                    raise RunError(f"{x} is already defined: `:=` defines a name once (2.R3)")
                binds = {x}
            else:
                binds = self._binds(parsed.pattern)
                for x in sorted(binds):
                    if x in self.defined:
                        raise RunError(f"{x} was defined with `:=` and cannot be rebound (2.R4)")
                    if x not in self.rebindable and self._sees(x):
                        raise RunError(f"{x} is a name of the files, not a name first bound with `<-` "
                                       f"in the session (2.R4)")
                unused = sorted(binds & (self.pending - used))
                notes = [f"note: unused rebinding of {x}: its binding before this line has no consumer "
                         f"(2.R6, reported and allowed in a session)" for x in unused]
            final = "(" + ", ".join(sorted(binds)) + ")" if len(binds) > 1 else next(iter(binds), "0")
            value, ty, states, out = self.evaluate(self.term(final, text), item=True, hint=used)
            self.items.append(text)
            if isinstance(parsed, s.Bind):
                self.defined.add(parsed.name)
            else:
                self.rebindable |= binds
            self.pending = (self.pending - used) | (binds if isinstance(parsed, s.Rebind) else set())
            return notes + out
        used = names(parsed)
        value, ty, states, out = self.evaluate(self.term(text), item=False, hint=used)
        # [proposed] a bare term that reads a name consumes it, for 2.R6's note
        self.pending -= used
        return out + [f"{_type_shown(value, sys.maxsize)} : {_type_shown(ty, sys.maxsize)}"] + show_states(states)

    def evaluate(self, term, item, hint=()):
        """The probe's value of the block ending in `term` (`evaluate`), with the session's
        actions (see the class); gives (value, type, states, the lines to print first)."""
        try:
            loaded, program, entry, definition, demand, states = _probed(self.files, term, self.fuel, self.world)
        except RunError as exc:
            if not self.world and "w" in hint:
                raise RunError(f"{exc} (the world `w` is the session's only with --world)") from exc
            raise
        specs = states.pop("_firsts", None) or []
        for spec in specs:
            spec["home"] = None   # [proposed] the session writes no entry in a store
        runner = Runner(program, demand.fuel)
        ty = definition.type
        before = len(self.log)
        if self.world:
            firsts = FirstActions(loaded, specs, demand)
            runner.first = {r: spec for r, spec in firsts.by_route.items() if r not in self.validated}
            runner.validate = firsts
            self._k = 0
            runner.actions = self.act
            target = t.App(t.Var(entry), runner.token)
            if isinstance(ty, t.Pi):
                ty = ty.codomain
        else:
            target = t.Var(entry)
        try:
            value = runner.value(target)
            if not item and len(self.log) > before:
                raise RunError("the term acted on the world without binding the token it gives: an action is "
                               "an item with its result bound, `(w, a) <- ...` (10.S2); it is not kept in the "
                               "block")
        except (RunError, ValueError, RecursionError) as exc:
            # the line is refused and leaves the block as it was; what its actions did in the world
            # is still shown (`out`, printed before the refusal)
            del self.log[before:]
            if self.world:
                self.validated |= set(firsts.by_route) - set(runner.first)
            exc.out = self.shown(firsts.done if self.world else [])
            raise
        if self.world:
            self.validated |= set(firsts.by_route) - set(runner.first)
            self.done += firsts.done
        return value, ty, states, self.shown(firsts.done if self.world else [])

    def shown(self, done):
        """The lines a line prints before its value: the first actions it validated (10.S10), then
        what the host printed since the last line."""
        out = [f"note: {d['action']} at its first action (10.S10): {d['law']} {d['outcome']}" for d in done]
        printed = host.stdout()
        if len(printed) > self.printed:
            out += printed[self.printed:].rstrip("\n").split("\n")
            self.printed = len(printed)
        return out

    def act(self, runner, head, function, args):
        """The Runner's hook (`Runner.actions`) on an extern applied with the session's world: the
        token's chain is demanded first, so the k-th action of a re-evaluation is the k-th the
        session performed; that one is served from the log, a new one performed and logged."""
        if runner.whnf(args[0]) != runner.token:
            return runner.act(head, function, args)
        shown = tuple(v if isinstance(v, t.Lit) else None for v in (runner.whnf(a) for a in args[1:]))
        k, self._k = self._k, self._k + 1
        if k < len(self.log):
            route, given, result = self.log[k]
            if (route, given) != (head.route, shown):
                raise RunError(f"the session's action {k + 1} was {route} and is now {head.route} with other "
                               f"arguments: a token used twice? (10.S3, a token is used once)")
            return result
        result = runner.value(runner.act(head, function, args))
        self.log.append((head.route, shown, result))
        return result
