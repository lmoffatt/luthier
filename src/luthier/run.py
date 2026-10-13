"""Demand-driven host runner. Sources: spec 10.S2–S10, world_model.lut (0c920f0).

Derivation: user request 2026-10-13, implementation v1 (record/IA/run-2026-10-13/codex.md);
v2 for world.lth draft 1 (prompt-2.md, choices in opus-2.md): the bridge carries `Maybe`
(host.Just, host.NOTHING) and records (a dict). No certification or extern result hashing yet.
"""
from __future__ import annotations

import importlib
import inspect
from dataclasses import fields, is_dataclass, replace
from pathlib import Path

from . import host, kernel, surface as s, term as t
from .elaborate import elaborate_program
from .parse import parse


class RunError(ValueError):
    pass


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


class Runner:
    def __init__(self, program, fuel):
        self.program = program
        self.fuel = fuel
        # An opaque kernel leaf stands for the host-owned identity for this run.
        self.token = t.Axiom("host world token")
        self.routes = {}

    def spend(self):
        if self.fuel <= 0:
            raise RunError("fuel spent")
        self.fuel -= 1

    def route(self, route):
        if route not in self.routes:
            if not route.startswith("python:"):
                raise RunError(f"unsupported extern route: {route}")
            module, name = route[7:].rsplit(".", 1)
            self.routes[route] = getattr(importlib.import_module(module), name)
        return self.routes[route]

    def to_host(self, value):
        value = self.whnf(value)
        if value is self.token or value == self.token:
            return self.token
        if isinstance(value, t.Lit):
            return value.constant.value
        if value == t.Var("unit"):
            return None
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

    def from_host(self, value):
        if value is self.token:
            return self.token
        if value is None:
            return t.Var("unit")
        if value is host.NOTHING:
            return t.Var("nothing")
        if isinstance(value, host.Just):
            return t.App(t.Var("just"), self.from_host(value.value))
        if isinstance(value, dict):
            # a record value, its fields in the dict's order (State: stdout, then files)
            return t.RecordValue(tuple((label, self.from_host(field)) for label, field in value.items()))
        if isinstance(value, str):
            return t.Lit(t.StringConst(value))
        if type(value) in (int, float):
            return t.Lit((t.IntConst if type(value) is int else t.FloatConst)(value))
        if isinstance(value, tuple) and len(value) == 2:
            return t.Pair(self.from_host(value[0]), self.from_host(value[1]))
        if isinstance(value, list):
            result = t.Var("nil")
            for item in reversed(value):
                result = t.App(t.App(t.Var("cons"), self.from_host(item)), result)
            return result
        raise RunError(f"unsupported extern result: {value!r}")

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
                        function = self.route(head.route)
                        arity = len(inspect.signature(function).parameters)
                        if len(args) < arity:
                            return self.apply(head, args)
                        result = function(*(self.to_host(a) for a in args[:arity]))
                        value = self.apply(self.from_host(result), args[arity:])
                        continue
                    except RunError:
                        raise
                    except Exception as exc:
                        raise RunError(f"extern {head.route} failed: {exc}") from exc
                value = self.apply(head, args)
            elif isinstance(value, t.Extern):
                try:
                    function = self.route(value.route)
                    if not inspect.signature(function).parameters:
                        return self.from_host(function())
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

    @staticmethod
    def apply(head, args):
        for arg in args:
            head = t.App(head, arg)
        return head


def runtime_slice(acts, main):
    """Keep the entry's dependencies and theory declarations, excluding law bodies.

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

    def names(value):
        if isinstance(value, s.Name):
            yield value.name
            yield value.name.split(".")[0]
        elif isinstance(value, tuple):
            for item in value:
                yield from names(item)
        elif is_dataclass(value):
            for field in fields(value):
                yield from names(getattr(value, field.name))

    needed = set()
    pending = [main]
    while pending:
        name = pending.pop()
        if name in needed:
            continue
        needed.add(name)
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


def run_file(path, main="main", fuel=10000):
    host.reset()
    program = elaborate_program(runtime_slice(load(Path(path)), main))
    definition = next((a for a in program if isinstance(a, t.Define) and a.name == main), None)
    if definition is None:
        raise RunError(f"missing main: {main}")
    program += tuple(t.Define(op, t.Universe(), t.Primitive(op)) for op in ("+", "-", "*", "==", "<"))
    runner = Runner(program, fuel)
    value = t.Var(main)
    if isinstance(definition.type, t.Pi) and isinstance(definition.type.domain, t.World):
        value = t.App(value, runner.token)
    result = runner.whnf(value)
    if isinstance(result, t.Pair):
        runner.whnf(result.left)  # Demand the final world chain, even for a lazy pair.
    return host.stdout()
