"""`luthier test`: the specimen of test.lth's `Tester`, exhaustive and sampled.

Sources: spec 7.S1, 7.S3, 7.S7, 7.S8, 7.S10, 7.S12, 7.S20, 7.R1 to 7.R4 (docs/spec/07-tests.md);
src/luthier/lib/test.lth (`TestSpec`, `test`, `Tester`, `grade`), laws.lth (`Evidence`, `Points`,
`NotRun`, `Coverage`, `Verdict`, `ForallOnPoints`), generators.lth (`Seed`, `Binding`, `resolve`,
`Budgets`). Derivation: record/IA/tester-2026-10-14/prompt.md, bite 1 (step 5.2 of the plan from
zero), by a Claude agent of the coordinating session, 2026-10-14.

A file's top-level `test` lines are data (D9): each is reduced with run.py's Runner to the
`TestSpec` test.lth's `test` builds, with its defaults. The law it names is a definition whose
parameters are the quantified variables and whose result is `Bool`; each case gives a value to
every parameter and is reduced with the same Runner (core, imports, the host) to `true` or
`false`. Under `ExhaustiveMode` the cases are every value of the parameters' types when they are
finite; under `SampledMode` `n` cases are drawn from the seed. The evidence is laws.lth's: the
points evaluated with the coverage reached, or `NotRun` with the reason. The verdict over the
points is laws.lth's `ForallOnPoints`, and the grade is test.lth's `grade`, reduced by the Runner.

Not in this bite (each says so where it applies): the metric of `SampledMode` (draws are uniform
between the bounds, 7.S4's special values and atom at 0 too); the sized generators of recursive
data other than `List` (7.S3's [proposed] row); enumeration of lists under `ExhaustiveMode`;
covering arrays (7.R3: above `coveringAbove` cases the test is not run); bindings to a generator
(a binding here names a census: one value, or a list of values, of the program); a size schedule
(every case is drawn at the spec's size); the store of entries (7.S9, 7.S13). Of the budgets
(7.S8) only `tries` and `coveringAbove` are read: a draw a filter cannot give within `tries`
makes the law not run (7.S6), so `drawsPerCase` and `redraws` have nothing to bound yet. A case
whose reduction raises (the host failed, a match stuck, the fuel spent) is not evaluated
(7.S12); it is reported on that case and leaves the law unsettled unless another case refutes it.
Names that two libraries define are scoped per file here (`Scope`), not in run.py's `load`.
"""
from __future__ import annotations

import random
import string
from dataclasses import dataclass, field, fields, is_dataclass, replace
from pathlib import Path

from . import host, kernel, surface as s, term as t
from .elaborate import elaborate_program, show_term
from .parse import parse
from .run import (Runner, RunError, _applied, _arrow, _core_acts, _instantiate, _primitive_body,
                  runtime_slice)

TRUE, FALSE = t.Var("true"), t.Var("false")
_TEST_LTH = (Path(__file__).parent / "lib" / "test.lth").resolve()
_LETTERS = string.ascii_letters + string.digits + " "  # [proposed] the alphabet of a drawn String


class NoGenerator(Exception):
    """A parameter's type has no generator under the mode: the test is not run (7.R2 to 7.R4)."""


class Unfit(Exception):
    """A filter gave no value within its budget of tries: the law is not run (7.S6)."""


# ---------------------------------------------------------------------- the spec (test.lth §1)

@dataclass
class Binding:
    """generators.lth's `Binding`: the generator named for a parameter or a type, with its coverage."""
    parameter: str | None
    type: str | None
    generator: str
    coverage: t.Term


@dataclass
class Spec:
    """test.lth's `TestSpec`, read from the value the `test` line reduces to."""
    law: str
    sampled: bool
    metric: t.Term | None
    cases: int
    size: int
    seed: int
    where: list
    profile: list
    budgets: dict


# ---------------------------------------------------------------------- the evidence (laws.lth)

@dataclass
class Points:
    """laws.lth's `Points A pts c`: each case (the values of the parameters) with its evidence,
    `Evaluated b`, and the coverage reached."""
    cases: list
    coverage: t.Term


@dataclass
class NotRun:
    reason: str


@dataclass
class Outcome:
    spec: Spec
    evidence: object
    verdict: str            # a constructor of laws.lth's `Verdict`, or "NotRun"
    grade: str | None       # a constructor of test.lth's `Grade`, or None
    evaluated: int          # cases evaluated to a verdict (7.S12)
    refuting: tuple | None  # the first refuting case
    raised: list = field(default_factory=list)  # (case, message): the host failed or the reduction stuck
    parameters: tuple = ()


# ---------------------------------------------------------------------- loading

def _refined_records(value):
    """A record type with a refinement, `{ x y : A | p }`, as a subtype of the record, so the
    elaborator takes it and the tester filters by it: `{ r : { x y : A } | (fn x y { p }) r.x r.y }`
    (the elaborator refuses record refinements, which check.py reads)."""
    if isinstance(value, tuple):
        return tuple(_refined_records(v) for v in value)
    if not is_dataclass(value) or isinstance(value, type):
        return value
    value = replace(value, **{f.name: _refined_records(getattr(value, f.name)) for f in fields(value)})
    if isinstance(value, s.Record) and value.law is not None:
        names = [n for f in value.fields for n in f.names]
        predicate = s.Lambda(tuple(s.PlainParam(n) for n in names), (), value.law)
        for n in names:
            predicate = s.App(predicate, s.Proj(s.Name("record%"), n))
        return s.Subtype(s.PApp("record%", ()), replace(value, law=None), predicate)
    return value


def _string_literals(value):
    if isinstance(value, s.StringLit):
        yield value.value
    elif isinstance(value, tuple):
        for v in value:
            yield from _string_literals(v)
    elif is_dataclass(value) and not isinstance(value, type):
        for f in fields(value):
            yield from _string_literals(getattr(value, f.name))


def collect_tests(path):
    """The file's own top-level `test` lines (D9), not those of what it imports."""
    result = parse(Path(path).read_text(encoding="utf-8"))
    if isinstance(result, s.ParseFailed):
        raise RunError("; ".join(f"{path}:{e.line}:{e.column}: {e.message}" for e in result.errors))
    lines = []
    for act in result.program:
        if isinstance(act, s.Datum):
            head = act.value
            while isinstance(head, s.App):
                head = head.function
            if head == s.Name("test"):
                lines.append(act.value)
    return lines


def _named(act):
    return act.name if isinstance(act, (s.Define, s.Declare, s.Alias)) else None


def _defines(act):
    """The names an act defines: its own, and a data's constructors."""
    names = [act.name] if _named(act) is not None else []
    if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
        names += [n for n, _ in act.body.constructors]
    return names


_BINDERS = (s.Explicit, s.Implicit, s.TypedParam, s.Field, s.Pi, s.Sigma)


def _bound(value, out):
    """Every name a binder in `value` introduces (conservative: scope is not followed)."""
    if isinstance(value, tuple):
        for v in value:
            _bound(v, out)
    elif is_dataclass(value) and not isinstance(value, type):
        if isinstance(value, _BINDERS):
            out.update(value.names)
        elif isinstance(value, (s.PlainParam, s.Bind)):
            out.add(value.name)
        elif isinstance(value, s.ShapeParam):
            out.add(value.right_name)
        elif isinstance(value, s.SigmaNamed):
            out.update((value.left_name, value.right_name))
        for f in fields(value):
            _bound(getattr(value, f.name), out)
    return out


class Scope:
    """The files a test file reaches, flattened as run.py's `load` flattens them, with each name
    that two of them define resolved per file: a file's own definition, else the one of the file
    it imports the name from, else the first file of its imports that defines it. `load` flattens
    every import whole, so two libraries that define one name (`LeqPair` in kernel_laws.lth,
    algebra.lth and numbers.lth; `Exhaustive` a theory in generators.lth and a constructor of
    laws.lth's `Coverage`) would otherwise both reach one program. Such a name is renamed `name@file`
    in each file that defines it, and so is every reference to it, except in an act where a binder
    has the same name."""

    def __init__(self, path, seen):
        self.top = Path(path).resolve()
        self.pairs, self.imports, self.defined = [], {}, {}
        self.visit(self.top, set(), seen)
        definers = {}
        for f, act in self.pairs:
            for n in _defines(act):
                definers.setdefault(n, set()).add(f)
        self.clashing = {n for n, fs in definers.items() if len(fs) > 1}
        self.memo = {}

    def visit(self, p, active, seen):
        p = p.resolve()
        if p in active:
            raise RunError(f"cyclic import: {p}")
        if p in seen:
            return
        result = parse(p.read_text(encoding="utf-8"))
        if isinstance(result, s.ParseFailed):
            raise RunError("; ".join(f"{p}:{e.line}:{e.column}: {e.message}" for e in result.errors))
        active.add(p)
        self.imports[p], self.defined[p] = [], set()
        for act in result.program:
            if isinstance(act, s.ImportAct):
                target = p.parent / act.path
                if not target.exists():
                    target = Path(__file__).parent / "lib" / act.path
                self.visit(target, active, seen)
                self.imports[p].append((target.resolve(), {n.name for n in act.names}))
                for name in act.names:
                    if name.asName:
                        self.pairs.append((p, s.Alias(name.asName, (), s.Name(name.name))))
            else:
                self.pairs.append((p, act))
                self.defined[p].update(_defines(act))
        active.remove(p)
        seen.add(p)

    def owner(self, f, name):
        """The file whose definition of `name` a reference in `f` means, or None."""
        key = (f, name)
        if key not in self.memo:
            self.memo[key] = None
            if name in self.defined.get(f, ()):
                self.memo[key] = f
            else:
                found = next((self.owner(g, name) for g, names in self.imports.get(f, ()) if name in names), None)
                if found is None:
                    queue, met = [g for g, _ in self.imports.get(f, ())], set()
                    while queue and found is None:
                        g = queue.pop(0)
                        if g in met:
                            continue
                        met.add(g)
                        found = g if name in self.defined.get(g, ()) else None
                        queue.extend(h for h, _ in self.imports.get(g, ()))
                self.memo[key] = found
        return self.memo[key]

    def renamed(self, f, name):
        if name not in self.clashing:
            return name
        owner = self.owner(f, name)
        return f"{name}@{owner.stem}" if owner is not None else name

    def name(self, name):
        """A name as the test file writes it (a law, a census), as the program calls it."""
        return self.renamed(self.top, name)

    def acts(self):
        out = []
        for f, act in self.pairs:
            bound = _bound(act, set()) & self.clashing
            out.append(self.rename(f, act, bound, top=True))
        return tuple(out)

    def rename(self, f, value, bound, top=False):
        if isinstance(value, tuple):
            return tuple(self.rename(f, v, bound) for v in value)
        if isinstance(value, s.Name):
            root, dot, rest = value.name.partition(".")
            return value if root in bound else s.Name(self.renamed(f, root) + dot + rest)
        if isinstance(value, s.PApp):
            name = value.name if value.name in bound else self.renamed(f, value.name)
            return s.PApp(name, self.rename(f, value.patterns, bound))
        if isinstance(value, s.DataBody):
            return s.DataBody(tuple((self.renamed(f, n), self.rename(f, ty, bound)) for n, ty in value.constructors))
        if not is_dataclass(value) or isinstance(value, type):
            return value
        changes = {fl.name: self.rename(f, getattr(value, fl.name), bound) for fl in fields(value)
                   if not isinstance(getattr(value, fl.name), str)}
        if top and _named(value) is not None:
            changes["name"] = self.renamed(f, value.name)
        return replace(value, **changes)


def load_program(path, fuel, extra=()):
    """The runtime program of the file as `run` loads it (core, imports, the host's routes), its
    names scoped per file (`Scope`), with each test line as a definition `test%k`, the laws and
    censuses its string literals name (and `extra`), and test.lth's `grade` as roots; the Runner
    over it, the names of the test lines and the scope."""
    host.reset()
    seen = set()
    scope = Scope(path, seen)
    own = scope.acts()
    core = _core_acts(seen, own)
    lines = collect_tests(path)
    specs = tuple(s.Define(f"test%{k}", (), None, s.TermBody(scope.rename(scope.top, v, set())))
                  for k, v in enumerate(lines))
    named = tuple(dict.fromkeys(scope.name(n) for v in lines for n in _string_literals(v)))
    data = tuple(a.name for a in core if isinstance(a, s.Define) and isinstance(a.body, s.DataBody))
    grading = tuple(scope.renamed(_TEST_LTH, n) for n in ("grade", "Coverage", "Verdict", "Grade"))
    roots = data + tuple(d.name for d in specs) + named + tuple(scope.name(n) for n in extra) + grading
    acts = _refined_records(runtime_slice(core + own + specs, specs[0].name if specs else "main", roots))
    program = tuple(_primitive_body(a) for a in elaborate_program(acts))
    program += tuple(t.Define(op, t.Universe(), t.Primitive(op)) for op in kernel.BOOTSTRAP_PRIMITIVES)
    return Runner(program, fuel), [d.name for d in specs], scope


# ---------------------------------------------------------------------- reading the spec

def _int(v):
    if isinstance(v, t.Lit) and isinstance(v.constant, t.IntConst):
        return v.constant.value
    raise RunError(f"not an integer: {show_term(v)}")


def _text(v):
    if isinstance(v, t.Lit) and isinstance(v.constant, t.StringConst):
        return v.constant.value
    raise RunError(f"not a string: {show_term(v)}")


def _list(runner, v):
    items = []
    v = runner.whnf(v)
    while isinstance(v, t.App) and isinstance(v.function, t.App) and v.function.function == t.Var("cons"):
        items.append(v.function.argument)
        v = runner.whnf(v.argument)
    if v != t.Var("nil"):
        raise RunError(f"not a list: {show_term(v)}")
    return items


def _maybe_text(v):
    if v == t.Var("nothing"):
        return None
    if isinstance(v, t.App) and v.function == t.Var("just"):
        return _text(v.argument)
    raise RunError(f"not a Maybe String: {show_term(v)}")


def read_spec(runner, value):
    runner.fuel = 1_000_000
    record = dict(runner.value(value).fields)
    mode = record["mode"]
    if _base(mode) == "ExhaustiveMode":
        sampled, metric = False, None
    elif isinstance(mode, t.App) and _base(mode) == "SampledMode":
        sampled, metric = True, mode.argument
    else:
        raise RunError(f"not a Mode: {show_term(mode)}")
    def bindings(v):
        out = []
        for b in _list(runner, v):
            b = dict(runner.value(b).fields)
            out.append(Binding(_maybe_text(b["parameter"]), _maybe_text(b["type"]), _text(b["generator"]),
                               b["coverage"]))
        return out
    budgets = {label: v.constant.value for label, v in record["budgets"].fields}
    return Spec(_text(record["law"]), sampled, metric, _int(record["cases"]), _int(record["size"]),
                _int(record["seed"]), bindings(record["whereBindings"]), bindings(record["profile"]), budgets)


# ---------------------------------------------------------------------- coverage (test.lth §2)

def _rank(c):
    """test.lth's `rankOf`."""
    return {"Exhaustive": 3, "Bounded": 2, "Listed": 1, "Drawn": 0}[_base(c)]


def _weaker(c, d):
    return c if _rank(c) <= _rank(d) else d


def resolve_binding(spec, parameter, type_name):
    """generators.lth's `resolve`: a parameter's binding in `where`, then in the profile, then a
    binding of its type in `where`, then in the profile."""
    for bs, by_parameter in ((spec.where, True), (spec.profile, True), (spec.where, False), (spec.profile, False)):
        for b in bs:
            if by_parameter and b.parameter == parameter:
                return b
            if not by_parameter and b.parameter is None and b.type == type_name:
                return b
    return None


# ---------------------------------------------------------------------- types and their values

def _mentions(term, name):
    if term == t.Var(name):
        return True
    if isinstance(term, tuple):
        return any(_mentions(x, name) for x in term)
    if is_dataclass(term) and not isinstance(term, type):
        return any(_mentions(getattr(term, f.name), name) for f in fields(term))
    return False


def _conjuncts(p):
    if isinstance(p, t.App) and isinstance(p.function, t.App) and p.function.function == t.Var("and"):
        return _conjuncts(p.function.argument) + _conjuncts(p.argument)
    return [p]


def _head_name(ty):
    while isinstance(ty, t.App):
        ty = ty.function
    return ty.name.partition("@")[0] if isinstance(ty, t.Var) else None


class Values:
    """The values of a type as kernel terms: every one (exhaustive) or one drawn (sampled)."""

    def __init__(self, runner, rng, size, budgets, fuel):
        self.runner, self.rng, self.size, self.budgets, self.fuel = runner, rng, size, budgets, fuel

    def whnf(self, term):
        self.runner.fuel = self.fuel
        return self.runner.whnf(term)

    def form(self, ty):
        """The type unfolded and its refinements collected: (base, [(name, predicate), ...])."""
        predicates = []
        while True:
            ty = self.whnf(ty)
            if isinstance(ty, t.Subtype):
                predicates.append((ty.name, ty.predicate))
                ty = ty.type
            elif isinstance(ty, t.Var) and ty.name in self.runner.types and self.runner.types[ty.name] != ty:
                ty = self.runner.types[ty.name]
            else:
                return ty, predicates

    def holds(self, predicates, value):
        for name, p in predicates:
            r = self.whnf(kernel.substitute(name, value, p))
            if r == FALSE:
                return False
            if r != TRUE:
                raise RunError(f"a refinement gave {show_term(r)}, not a Bool")
        return True

    def bounds(self, predicates, kind):
        """The interval a refinement states with literal bounds (7.S6), each side or None."""
        lo = hi = None
        for name, p in predicates:
            for c in _conjuncts(p):
                if not (isinstance(c, t.App) and isinstance(c.function, t.App) and isinstance(c.function.function, t.Var)):
                    continue
                op, left, right = c.function.function.name, c.function.argument, c.argument
                if op not in ("<=", "<", ">=", ">"):
                    continue
                if left == t.Var(name) and not _mentions(right, name):
                    bound, upper = right, op in ("<=", "<")
                elif right == t.Var(name) and not _mentions(left, name):
                    bound, upper = left, op in (">=", ">")
                else:
                    continue
                try:
                    bound = self.whnf(bound)
                except RunError:
                    continue
                if not (isinstance(bound, t.Lit) and isinstance(bound.constant, (t.IntConst, t.FloatConst))):
                    continue
                b = bound.constant.value
                if kind == "Int" and op in ("<", ">"):
                    b = b - 1 if upper else b + 1
                if upper:
                    hi = b if hi is None else min(hi, b)
                else:
                    lo = b if lo is None else max(lo, b)
        return lo, hi

    # ---------------------------------------------------------- exhaustive (7.S3, 7.R3)

    def every(self, ty, limit):
        """Every value of a finite type, at most `limit + 1` of them; NoGenerator when infinite."""
        base, predicates = self.form(ty)
        if isinstance(base, t.Var) and base.name == "Int":
            lo, hi = self.bounds(predicates, "Int")
            if lo is None or hi is None:
                raise NoGenerator(f"{show_term(ty)} is infinite: ExhaustiveMode needs its bounds or a census (7.R3)")
            values = (t.Lit(t.IntConst(k)) for k in range(lo, hi + 1))
        else:
            values = self.every_base(base, limit)
        out = []
        for v in values:
            if self.holds(predicates, v):
                out.append(v)
                if len(out) > limit:
                    break
        return out

    def every_base(self, ty, limit):
        if isinstance(ty, t.Universe):
            raise NoGenerator("a parameter of type U has no generator (7.R2)")
        if isinstance(ty, t.Data):
            return self.every_constructor(ty, limit)
        if isinstance(ty, t.Sigma):
            out = []
            for left in self.every(ty.domain, limit):
                for right in self.every(_instantiate(ty.name, left, ty.codomain), limit):
                    out.append(t.Pair(left, right))
                    if len(out) > limit:
                        return out
            return out
        if isinstance(ty, t.Record):
            return [t.RecordValue(tuple(items)) for items in self.every_fields(list(ty.fields), limit)]
        if isinstance(ty, t.Sum):
            return [t.Inj(label, v) for label, a in ty.alternatives for v in self.every(a, limit)]
        if _applied(ty, "List") is not None:
            raise NoGenerator("a list under ExhaustiveMode: its enumeration up to the size is a later bite")
        if _arrow(ty) is not None:
            raise NoGenerator(f"a function {show_term(ty)}: bind a census (7.R4)")
        raise NoGenerator(f"{show_term(ty)} has no finite enumeration (7.R3)")

    def every_fields(self, types, limit):
        if not types:
            return [[]]
        (label, ty), rest = types[0], types[1:]
        out = []
        for v in self.every(ty, limit):
            later = [(l, _instantiate(label, v, f)) for l, f in rest]
            for items in self.every_fields(later, limit):
                out.append([(label, v)] + items)
                if len(out) > limit:
                    return out
        return out

    def every_constructor(self, data, limit):
        out = []
        for name, ty in data.constructors:
            domains = self.domains(data, ty)
            combos = [[]]
            for d in domains:
                combos = [c + [v] for c in combos for v in self.every(d, limit)]
                if len(combos) > limit:
                    break
            out.extend(Runner.apply(t.Var(name), c) for c in combos)
            if len(out) > limit:
                break
        return out

    def domains(self, data, ty):
        """The argument types of a constructor; NoGenerator when one is the data itself."""
        domains = []
        while (arrow := _arrow(ty)) is not None:
            if _mentions(arrow[1], data.name):
                raise NoGenerator(f"recursive data {data.name}: its sized generator is a later bite (7.S3)")
            domains.append(arrow[1])
            ty = arrow[2]
        return domains

    # ---------------------------------------------------------- sampled (7.S3, 7.S6)

    def draw(self, ty):
        base, predicates = self.form(ty)
        kind = base.name if isinstance(base, t.Var) else None
        lo, hi = self.bounds(predicates, kind) if kind in ("Int", "Float64") else (None, None)
        for _ in range(self.budgets.get("tries", 2000)):
            v = self.draw_base(base, lo, hi)
            if self.holds(predicates, v):
                return v
        raise Unfit(f"no value of {show_term(ty)} in {self.budgets.get('tries', 2000)} tries (7.S6)")

    def draw_base(self, ty, lo, hi):
        rng, n = self.rng, self.size
        if isinstance(ty, t.Var) and ty.name in ("Int", "Float64"):
            # 7.S3: the bounds of the type, otherwise [-s, s]; a missing side at s from the other
            lo = -n if lo is None else lo
            hi = (max(lo, 0) + n) if hi is None else hi
            if hi < lo:
                raise Unfit(f"an empty interval [{lo}, {hi}]")
            if ty.name == "Int":
                return t.Lit(t.IntConst(rng.randint(int(lo), int(hi))))
            return t.Lit(t.FloatConst(float(rng.uniform(float(lo), float(hi)))))
        if ty == t.Var("String"):
            return t.Lit(t.StringConst("".join(rng.choice(_LETTERS) for _ in range(rng.randint(0, n)))))
        if isinstance(ty, t.Universe):
            raise NoGenerator("a parameter of type U has no generator (7.R2)")
        if isinstance(ty, t.Data):
            name, cty = ty.constructors[rng.randrange(len(ty.constructors))]
            return Runner.apply(t.Var(name), [self.draw(d) for d in self.domains(ty, cty)])
        if isinstance(ty, t.Sigma):
            left = self.draw(ty.domain)
            return t.Pair(left, self.draw(_instantiate(ty.name, left, ty.codomain)))
        if isinstance(ty, t.Record):
            items, types = [], list(ty.fields)
            for k, (label, fty) in enumerate(types):
                v = self.draw(fty)
                items.append((label, v))
                types[k + 1:] = [(l, _instantiate(label, v, f)) for l, f in types[k + 1:]]
            return t.RecordValue(tuple(items))
        if isinstance(ty, t.Sum):
            label, a = ty.alternatives[rng.randrange(len(ty.alternatives))]
            return t.Inj(label, self.draw(a))
        if (element := _applied(ty, "List")) is not None:
            result = t.Var("nil")
            for _ in range(rng.randint(0, n)):
                result = t.App(t.App(t.Var("cons"), self.draw(element)), result)
            return result
        if _arrow(ty) is not None:
            raise NoGenerator(f"a function {show_term(ty)}: bind a census (7.R4)")
        raise NoGenerator(f"no generator of {show_term(ty)}")


# ---------------------------------------------------------------------- running (test.lth §2)

def parameters(runner, law):
    """The law's quantified variables: (name, type) of its definition's arrows, its result Bool."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == law), None)
    if definition is None:
        return None
    ty, params = definition.type, []
    while isinstance(ty, t.Pi):
        params.append((ty.name, ty.domain))
        ty = ty.codomain
    return params


def census(runner, binding, ty, name):
    """The values a binding names (7.R4): a definition of the program, `name` there, its elements
    when it is a list and the parameter is not."""
    definition = next((a for a in runner.program if isinstance(a, t.Define) and a.name == name), None)
    if definition is None:
        raise NoGenerator(f"the binding names {binding.generator}, which is not defined")
    if _applied(runner.resolve(definition.type), "List") is not None and _applied(runner.resolve(ty), "List") is None:
        values = _list(runner, t.Var(name))
        if not values:
            raise NoGenerator(f"the census {binding.generator} is empty")
        return values
    return [t.Var(name)]


def evaluate(runner, law, case, fuel):
    runner.fuel = fuel
    r = runner.whnf(Runner.apply(t.Var(law), list(case)))
    if r == TRUE:
        return True
    if r == FALSE:
        return False
    raise RunError(f"the law gave {show_term(r)}, not a Bool")


def run_spec(runner, spec, fuel, scope=None):
    """test.lth's `Tester.run`: the evidence of the law the spec names, with its verdict and grade."""
    law = scope.name(spec.law) if scope else spec.law
    params = parameters(runner, law)
    if params is None:
        return _not_run(spec, f"no definition {spec.law}")
    names = tuple(n for n, _ in params)
    values = Values(runner, random.Random(spec.seed), spec.size, spec.budgets, fuel)
    limit = spec.budgets.get("coveringAbove", 20000)
    # each parameter: a census its binding names, or the mode's functor over its type
    con = _constructor(scope)
    plan, coverage = [], (t.App(con("Drawn"), t.Lit(t.IntConst(spec.seed))) if spec.sampled else con("Exhaustive"))
    try:
        for name, ty in params:
            b = resolve_binding(spec, name, _head_name(ty))
            plan.append(census(runner, b, ty, scope.name(b.generator) if scope else b.generator) if b else None)
    except (NoGenerator, RunError) as exc:
        return _not_run(spec, str(exc), names)
    for b in spec.where + spec.profile:  # test.lth's specCoverage: every binding weakens it
        coverage = _weaker(b.coverage, coverage)

    cases = []
    try:
        if not spec.sampled:
            cases = _every_case(values, params, plan, limit)
            if len(cases) > limit:
                return _not_run(spec, f"more than {limit} cases (coveringAbove); covering arrays are a later bite (7.R3)", names)
        else:
            # 7.S6: a draw that a filter cannot give within its tries makes the law not run
            cases = [_draw_case(values, params, plan, k) for k in range(spec.cases)]
    except (NoGenerator, Unfit) as exc:
        return _not_run(spec, str(exc), names)
    except RunError as exc:
        return _not_run(spec, f"drawing the cases: {exc}", names)

    points, raised, refuting = [], [], None
    for case in cases:
        try:
            ok = evaluate(runner, law, case, fuel)
        except (RunError, RecursionError, ValueError, KeyError, TypeError) as exc:
            raised.append((case, str(exc) or type(exc).__name__))
            continue
        points.append((case, ok))
        if not ok and refuting is None:
            refuting = case
    evidence = Points(points, coverage)
    # laws.lth's ForallOnPoints; a case that raised settles nothing (its evidence is NotRun)
    if refuting is not None:
        verdict = "Refuted"
    elif raised:
        verdict = "Unsettled"
    else:
        verdict = "Confirmed" if _base(coverage) == "Exhaustive" else "Supported"
    return Outcome(spec, evidence, verdict, grade_of(runner, verdict, coverage, scope), len(points), refuting,
                   raised, names)


def _every_case(values, params, plan, limit, prefix=()):
    """The product of every parameter's values in order, a later type reading the earlier values."""
    if len(prefix) == len(params):
        return [prefix]
    k = len(prefix)
    ty = params[k][1]
    for (name, _), v in zip(params, prefix):
        ty = _instantiate(name, v, ty)
    out = []
    try:
        every = plan[k] if plan[k] is not None else values.every(ty, limit)
    except NoGenerator as exc:
        raise NoGenerator(f"{params[k][0]} : {show_term(params[k][1])}: {exc}") from exc
    for v in every:
        out.extend(_every_case(values, params, plan, limit, prefix + (v,)))
        if len(out) > limit:
            break
    return out


def _draw_case(values, params, plan, walked):
    case = []
    for k, (name, ty) in enumerate(params):
        for (earlier, _), v in zip(params, case):
            ty = _instantiate(earlier, v, ty)
        # a census is walked in turn, each value once per round (generators.lth's `walk`, gen.10)
        try:
            case.append(plan[k][walked % len(plan[k])] if plan[k] is not None else values.draw(ty))
        except (NoGenerator, Unfit) as exc:
            raise type(exc)(f"{name} : {show_term(params[k][1])}: {exc}") from exc
    return tuple(case)


def grade_of(runner, verdict, coverage, scope=None):
    """test.lth's `grade`, reduced: the grade's constructor, or None."""
    runner.fuel = 100000
    con = _constructor(scope)
    g = runner.value(Runner.apply(con("grade"), [con(verdict), t.App(t.Var("just"), coverage)]))
    if isinstance(g, t.App) and g.function == t.Var("just"):
        return _base(g.argument)
    return None


def _constructor(scope):
    """A name of test.lth or laws.lth as the program calls it."""
    return lambda n: t.Var(scope.renamed(_TEST_LTH, n) if scope else n)


def _base(term):
    """The name at the head of a term, without the file a clash renamed it by (`Scope`)."""
    while isinstance(term, t.App):
        term = term.function
    return term.name.partition("@")[0] if isinstance(term, t.Var) else None


def _not_run(spec, reason, names=()):
    return Outcome(spec, NotRun(reason), "NotRun", None, 0, None, parameters=names)


# ---------------------------------------------------------------------- the command

_GRADE_WORDS = {"Proved": "proved", "ExhaustiveGrade": "exhaustive", "Cases": "cases", "Sampled": "sampled",
                "Assumed": "assumed"}


def show_case(names, case):
    return ", ".join(f"{n} = {show_term(v)}" for n, v in zip(names, case))


def line(outcome):
    """One line per test: the law, the mode, the cases evaluated, the grade, the refuting case."""
    spec = outcome.spec
    mode = f"sampled (seed {spec.seed}, size {spec.size}, metric ignored)" if spec.sampled else "exhaustive"
    head = f"{spec.law}: {mode}, {outcome.evaluated} cases"
    if isinstance(outcome.evidence, NotRun):
        return f"{head}, not run: {outcome.evidence.reason}"
    if outcome.verdict == "Refuted":
        return f"{head}, refuted at {show_case(outcome.parameters, outcome.refuting)}"
    if outcome.verdict == "Unsettled":
        case, message = outcome.raised[0]
        return (f"{head}, unsettled: {len(outcome.raised)} cases raised, the first at "
                f"{show_case(outcome.parameters, case)}: {message}")
    return f"{head}, {_GRADE_WORDS.get(outcome.grade, outcome.grade)}"


def run_tests(path, seed=None, fuel=1_000_000):
    """Run every `test` line of the file; the outcomes in order."""
    runner, names, scope = load_program(path, fuel)
    specs = [read_spec(runner, t.Var(name)) for name in names]
    # the laws and censuses the specs name, when a definition (a profile) holds their names
    defined = {a.name for a in runner.program if isinstance(a, (t.Define, t.Declare))}
    wanted = {n for spec in specs for n in [spec.law] + [b.generator for b in spec.where + spec.profile]}
    missing = sorted(n for n in wanted if scope.name(n) not in defined)
    if missing:
        runner, names, scope = load_program(path, fuel, missing)
        specs = [read_spec(runner, t.Var(name)) for name in names]
    outcomes = []
    for spec in specs:
        if seed is not None:
            spec.seed = seed
        outcomes.append(run_spec(runner, spec, fuel, scope))
    return outcomes
