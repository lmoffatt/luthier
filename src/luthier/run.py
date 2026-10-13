"""Demand-driven host runner. Sources: spec 10.S2–S10, world_model.lut (0c920f0).

Derivation: user request 2026-10-13, implementation v1 (record/IA/run-2026-10-13/codex.md);
v2 for world.lth draft 1 (prompt-2.md, choices in opus-2.md): the bridge carries `Maybe`
(host.Just, host.NOTHING) and records (a dict). v4 (prompt-4.md, choices in report-4.md): the
bridge reads by the type the extern's definition declares (spec 3.S22 to 3.S26, 11.S6 to 11.S9):
`Vec`/`Mat` records and `Fin n -> Float64`/`Int` as ndarrays, `Float64` and `Int` checked,
`Table` as tables.py reads it, sums as `(label, value)`. v5 (prompt-5.md, report-5.md): every
run loads `lib/core.lut` before the file (12.S22, 11.R2), defines kernel.BOOTSTRAP_PRIMITIVES as
`eval` does, and the Runner brings the operands of a primitive and of `and`/`or` to weak head
normal form itself, with the host. No certification or result hashing yet.
"""
from __future__ import annotations

import importlib
import inspect
import math
from dataclasses import dataclass, field, fields, is_dataclass, replace
from pathlib import Path

import numpy as np

from . import host, kernel, surface as s, term as t
from .elaborate import elaborate_program
from .parse import parse


class RunError(ValueError):
    pass


# the core encloses the top-level scope of every file (12.S22); its data and `not` are read here
CORE = Path(__file__).parent / "lib" / "core.lut"


def load(path: Path, seen=None, active=None):
    """Flatten imports before elaboration; local paths precede bundled libraries."""
    seen = set() if seen is None else seen
    active = set() if active is None else active
    path = path.resolve()
    if path in active:
        raise RunError(f"cyclic import: {path}")
    if path in seen:
        return ()
    result = parse(path.read_text(encoding="utf-8"))
    if isinstance(result, s.ParseFailed):
        raise RunError("; ".join(f"{path}:{e.line}:{e.column}: {e.message}" for e in result.errors))
    active.add(path)
    acts = []
    for act in result.program:
        if isinstance(act, s.ImportAct):
            target = path.parent / act.path
            if not target.exists():
                target = Path(__file__).parent / "lib" / act.path
            acts.extend(load(target, seen, active))
            for name in act.names:
                if name.asName:
                    acts.append(s.Alias(name.asName, (), s.Name(name.name)))
        else:
            acts.append(act)
    active.remove(path)
    seen.add(path)
    return tuple(acts)


@dataclass(frozen=True)
class TypedExtern(t.Extern):
    """An extern with the type its definition declares, so the bridge reads its arguments and its
    result by type (11.S6); with `obj`, a host object that crossed into the kernel (3.S22), applied
    like an extern, its route a name of this run only."""
    type: object = None
    obj: object = field(default=None, compare=False, hash=False)


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


_UNTYPED = object()
_INTS = ("Int", "Nat")
_NAMED = {"Float64", "String", "Unit", "Bool"} | set(_INTS)
_INT64 = (-2 ** 63, 2 ** 63)


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
        self.objects = 0
        # the types the bridge resolves names to: a type definition's body, a theory's record
        self.types = {}
        for act in program:
            if isinstance(act, t.Define) and act.type == t.Universe() and not isinstance(act.body, t.Lam):
                self.types[act.name] = act.body
            elif isinstance(act, t.Declare) and isinstance(act.type, t.Record):
                self.types[act.name] = act.type
        self.program = tuple(self.typed(act) for act in program)
        self.defined = {act.name for act in program if isinstance(act, (t.Define, t.Declare))}

    def typed(self, act):
        """The definition with each extern it gives carrying its declared type: `f (x : A) : B :=
        extern "..." x`, or a record of a declared theory whose fields are externs (3.S40)."""
        if not isinstance(act, t.Define) or act.type is None:
            return act
        extern = _extern_of(act.body)
        if extern is not None:
            return replace(act, body=_with_extern(act.body, TypedExtern(extern.route, act.type)))
        record = self.resolve(act.type)
        if isinstance(act.body, t.RecordValue) and isinstance(record, t.Record):
            types = dict(record.fields)
            items = []
            for label, value in act.body.fields:
                extern = _extern_of(value)
                if extern is not None and label in types:
                    value = _with_extern(value, TypedExtern(extern.route, types[label]))
                items.append((label, value))
            return replace(act, body=t.RecordValue(tuple(items)))
        return act

    def resolve(self, ty):
        """A type with its names unfolded and its refinements dropped, down to what the bridge
        reads: the named primitives, `Maybe`, `List`, `Fin`, functions, pairs, sums, records."""
        while True:
            if isinstance(ty, t.Subtype):
                ty = ty.type
            elif isinstance(ty, t.Var) and ty.name not in _NAMED and ty.name in self.types:
                ty = self.types[ty.name]
            else:
                return ty

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

    def to_host(self, value, ty=None):
        value = self.whnf(value)
        if value is self.token or value == self.token:
            return self.token
        if isinstance(value, TypedExtern) and value.obj is not None:
            # a host object goes back as it came (an array, a method of a host table)
            return value.obj.array if isinstance(value.obj, Entries) else value.obj
        if ty is not None:
            result = self.typed_to_host(value, self.resolve(ty))
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

    def typed_to_host(self, value, ty):
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
                return host.Just(self.to_host(value.argument, element))
        if (element := _applied(ty, "List")) is not None:
            items = []
            while (isinstance(value, t.App) and isinstance(value.function, t.App)
                   and value.function.function == t.Var("cons")):
                items.append(self.to_host(value.function.argument, element))
                value = self.whnf(value.argument)
            if value == t.Var("nil"):
                return items
            raise RunError(f"not a list at the crossing: {value!r}")
        if isinstance(ty, t.Sigma) and isinstance(value, t.Pair):
            return (self.to_host(value.left, ty.domain),
                    self.to_host(value.right, _instantiate(ty.name, value.left, ty.codomain)))
        if isinstance(ty, t.Sum):
            # a sum crosses as (label, value): `int 3` is ("int", 3), tables.py's cells
            alternatives = dict(ty.alternatives)
            if isinstance(value, t.App) and isinstance(value.function, t.Var) and value.function.name in alternatives:
                label = value.function.name
                return label, self.to_host(value.argument, alternatives[label])
            if isinstance(value, t.Inj) and value.label in alternatives:
                return value.label, self.to_host(value.value, alternatives[value.label])
        if isinstance(ty, t.Record) and isinstance(value, t.RecordValue):
            return self.record_to_host(value, ty)
        if (arrow := _arrow(ty)) is not None:
            if self.size(arrow[1]) is not None:
                return self.materialize(value, ty)
            return self.function_to_host(value, ty)
        return _UNTYPED

    def float64(self, x):
        if type(x) is int:
            if abs(x) > 2 ** 1024 or int(float(x)) != x:
                raise RunError(f"the integer {x} has no exact double")
            x = float(x)
        if not math.isfinite(x):
            raise RunError(f"{x} is not a Float64 (11.S7)")
        return x

    def materialize(self, value, ty):
        """A lambda over `Fin n` handed to the host is the array of its n values (3.S23), each
        entry evaluated once (3.S25); `Fin m -> Fin n -> A` two-dimensional (3.S24). The element
        type decides the representation: `Float64` float64, `Int` int64 in range (11.S8), any other
        a list (11.S9)."""
        name, domain, codomain = _arrow(self.resolve(ty))
        n = self.size(domain)
        entries = []
        for k in range(n):
            index = t.Lit(t.IntConst(k))
            entries.append(self.to_host(t.App(value, index), _instantiate(name, index, codomain)))
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

    def function_to_host(self, value, ty):
        """A Luthier function the host calls: its arguments cross back by the domain's types and
        its result to the host by the codomain's."""
        def call(*args):
            current, result = ty, value
            for arg in args:
                arrow = _arrow(self.resolve(current))
                if arrow is None:
                    raise RunError(f"too many arguments for {value!r}")
                term = self.from_host(arg, arrow[1])
                result = t.App(result, term)
                current = _instantiate(arrow[0], term, arrow[2])
            return self.to_host(result, current)
        return call

    def record_to_host(self, value, ty):
        """A record by its fields, a later field's type reading the earlier ones (`f : Fin n -> A`).
        A `Vec` `{ n, f }` or a `Mat` `{ m, n, f }` is the array of `f`, its shape the record's;
        a `Table` the record `tables.as_table` reads, its `cell` giving None or (label, value); a
        record whose fields are one host object's attributes is that object."""
        given = dict(value.fields)
        out, types = HostRecord(), list(ty.fields)
        for k, (label, field_type) in enumerate(types):
            if label not in given:
                raise RunError(f"the record has no field {label}")
            out[label] = self.to_host(given[label], field_type)
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
        if name == "Bool" and isinstance(value, (bool, np.bool_)):
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
        if isinstance(pattern, (t.PVar, t.PWild)):
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

    def whnf(self, value):
        while True:
            self.spend()
            if isinstance(value, t.App):
                args = []
                head = value
                while isinstance(head, t.App):
                    args.append(head.argument)
                    head = head.function
                args.reverse()
                head = self.whnf(head)
                if isinstance(head, t.Extern):
                    try:
                        function = self.route(head)
                        arity = len(inspect.signature(function).parameters)
                        if len(args) < arity:
                            return self.apply(head, args)
                        # each argument crosses at its declared type, a later type reading the
                        # earlier arguments (`(n : Int) -> Fin n -> Float64`); untyped, by value
                        ty, given = getattr(head, "type", None), []
                        for a in args[:arity]:
                            a = self.whnf(a)
                            arrow = _arrow(self.resolve(ty)) if ty is not None else None
                            domain, ty = (arrow[1], _instantiate(arrow[0], a, arrow[2])) if arrow else (None, None)
                            given.append(self.to_host(a, domain))
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
                    if not inspect.signature(function).parameters:
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


def _core_acts(seen, own):
    """core.lut's acts, those a file of the run defines left out (the file's own shadows the core,
    12.S22). Its `operator` acts never reach the program: runtime_slice keeps definitions,
    declarations and aliases only, so `a + b` stays `Var "+"`, bound below to the kernel's
    primitive, and `a and b` stays `Var "and"`, the kernel's connective."""
    defined = {a.name for a in own if isinstance(a, (s.Define, s.Declare, s.Alias))}
    return tuple(a for a in load(CORE, seen)
                 if not (isinstance(a, (s.Define, s.Declare, s.Alias)) and a.name in defined))


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


def run_file(path, main="main", fuel=10000):
    host.reset()
    seen = set()
    own = load(Path(path), seen)
    core = _core_acts(seen, own)
    # core's data is in every run, named or not (`[1, 2]` is `cons`, `if` reads `true`)
    data = tuple(a.name for a in core if isinstance(a, s.Define) and isinstance(a.body, s.DataBody))
    program = tuple(_primitive_body(a) for a in elaborate_program(runtime_slice(core + own, main, data)))
    definition = next((a for a in program if isinstance(a, t.Define) and a.name == main), None)
    if definition is None:
        raise RunError(f"missing main: {main}")
    # the kernel's bootstrap of the symbols, as `luthier eval` (cli.py); a file's own come first
    program += tuple(t.Define(op, t.Universe(), t.Primitive(op)) for op in kernel.BOOTSTRAP_PRIMITIVES)
    runner = Runner(program, fuel)
    value = t.Var(main)
    if isinstance(definition.type, t.Pi) and isinstance(definition.type.domain, t.World):
        value = t.App(value, runner.token)
    result = runner.whnf(value)
    if isinstance(result, t.Pair):
        runner.whnf(result.left)  # Demand the final world chain, even for a lazy pair.
    return host.stdout()
