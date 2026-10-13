"""Specimen of program.lth through 02aa8af; user brief 2026-10-13, v3; bite 5 (prompt-5.md).

Deterministic, no seed. R2 implements existence only; SCC/type-position checking
is deferred. Typing is deliberately partial, with unknown types kept unknown.
R10 is author judgement, R11 a typing law, S23 is an elaboration law.
"""
from functools import lru_cache
from dataclasses import dataclass, fields, is_dataclass
from . import surface as s, term as t
from .elaborate import elaborate_program, context_of, walk, infer, parameters, curry, theory_domains, ElaborationError
from .kernel import alpha_equal, substitute, reduce, free_names


@dataclass(frozen=True)
class Failure:
    rule: str
    name: str
    message: str


@dataclass(frozen=True)
class Report:
    kind: str
    name: str
    message: str


# Chosen chapter 3/11 vocabulary, including their constructors and directives;
# library interfaces (Law, Failures, cite) must be imported or declared.
coreNames = frozenset('Int Real Float64 Rational String Nat Fin Bool Unit Empty List Maybe true false unit nil cons just nothing left right not and or implies extern primitive axiom toFloat64 fromInt'.split())


def namePrefix(n):
    return n.split('.', 1)[0]


def nameSuffix(n):
    return n.rsplit('.', 1)[-1]


def nodes(x):
    yield x
    if isinstance(x, tuple):
        for y in x:
            yield from nodes(y)
    elif is_dataclass(x):
        for f in fields(x):
            yield from nodes(getattr(x, f.name))


def constructors(p):
    result = set()
    for a in p:
        if isinstance(a, s.Define) and isinstance(a.body, s.DataBody):
            result.update(n for n, _ in a.body.constructors)
        u = a.value if isinstance(a, s.Alias) else a.body.term if isinstance(a, s.Define) and isinstance(a.body, s.TermBody) else None
        roots = [u]
        if isinstance(a, s.Define): roots.append(a.type)
        if isinstance(a, s.Declare): roots.extend([a.type, *(b.type for b in a.binders)])
        for root in roots:
            for node in term_nodes(root):
                if isinstance(node, s.Sum): result.update(n for n, _ in node.alternatives)
    return result


def remove_bound(ns, bound):
    return {n for n in ns if n not in bound and namePrefix(n) not in bound}


def pattern_binds(q, k):
    if isinstance(q, s.PApp):
        return ({q.name} if not q.patterns and q.name not in k else set()) | set().union(*(pattern_binds(x, k) for x in q.patterns))
    if isinstance(q, s.PTuple):
        return set().union(*(pattern_binds(x, k) for x in q.patterns))
    return set()


def item_binds(it, k):
    """The names a block item binds: `x := v` binds x, `q <- v` what its pattern binds (itemsNames)."""
    return {it.name} if isinstance(it, s.Bind) else pattern_binds(it.pattern, k)


def param_binds(ps, k):
    result = set()
    for q in ps:
        if isinstance(q, s.PlainParam): result.add(q.name)
        elif isinstance(q, s.TypedParam): result.update(q.names)
        else:
            for x in q.patterns: result.update(pattern_binds(x, k))
    return result


def names(x, k=frozenset()):
    """namesIn, preserving scope and dotted surface names, not field labels."""
    if x is None: return set()
    if isinstance(x, s.Name): return {x.name}
    if isinstance(x, (s.Pi, s.Sigma)):
        return names(x.domain, k) | remove_bound(names(x.codomain, k), set(x.names))
    if isinstance(x, s.SigmaNamed):
        return names(x.left_type, k) | remove_bound(names(x.right_type, k), {x.left_name})
    if isinstance(x, s.Subtype): return names(x.type, k) | remove_bound(names(x.law, k), pattern_binds(x.pattern, k))
    if isinstance(x, s.Record):
        bound = set(); result = set()
        for f in x.fields:
            result |= remove_bound(names(f.type, k), bound); bound.update(f.names)
        return result | remove_bound(names(x.law, k), bound)
    if isinstance(x, (s.Block, s.Lambda)):
        bound = set(); result = set()
        if isinstance(x, s.Lambda):
            for q in x.params:
                if isinstance(q, s.TypedParam): result |= remove_bound(names(q.type, k), bound)
                bound |= param_binds((q,), k)
        for it in x.items:
            result |= remove_bound(names(it.value, k), bound); bound |= item_binds(it, k)
        return result | remove_bound(names(x.value if isinstance(x, s.Block) else x.body, k), bound)
    if isinstance(x, s.MatchOf):
        return names(x.value, k) | set().union(*(remove_bound(names(b, k), pattern_binds(q, k)) for q, b in x.arms))
    if isinstance(x, s.Clause):
        return remove_bound(names(x.body, k), set().union(*(pattern_binds(q, k) for q in x.patterns)))
    if isinstance(x, tuple): return set().union(*(names(y, k) for y in x))
    if is_dataclass(x): return set().union(*(names(getattr(x, f.name), k) for f in fields(x)))
    return set()


def dependencies(p, a, body=False):
    k = constructors(p); bound = set(); result = set()
    for b in a.binders:
        result |= remove_bound(names(b.type, k) | names(getattr(b, 'default', None), k), bound)
        bound.update(b.names)
    if body: return remove_bound(names(a.body, k), bound)
    return result | remove_bound(names(a.value if isinstance(a, s.Alias) else a.type, k), bound)


def acts(p, n, cls=None):
    return [a for a in p if getattr(a, 'name', None) == n and (cls is None or isinstance(a, cls))]


def unknown(p, ns):
    known = coreNames | constructors(p) | {a.name for a in p if hasattr(a, 'name')} | {i.asName or i.name for a in p if isinstance(a, s.ImportAct) for i in a.names}
    return {x for x in ns if x not in known and namePrefix(x) not in known}


def declared(p, n):
    return next((a.type for a in acts(p, n, s.Declare)), None)


def type_of_act(p, a):
    return a.type if a.type is not None else declared(p, a.name)


def head(x):
    while isinstance(x, s.App): x = x.function
    return x


def provisional(x):
    return isinstance(x, s.App) and (isinstance(x.argument, s.NamedArg) and x.argument.name == 'provisional' or provisional(x.function))


def conjuncts(x):
    if isinstance(x, s.Binop): return conjuncts(x.left) | conjuncts(x.right) if x.operator == '&' else set()
    x = head(x)
    return {x.name} if isinstance(x, s.Name) else set()


def claimed_laws(p):
    # theoryHeads searches the whole program.
    claimed = set()
    for a in p:
        if isinstance(a, s.Define) and isinstance(a.body, s.TermBody):
            u = a.body.term
            if isinstance(u, s.Binop) and u.operator == '&' or acts(p, a.name, s.Declare): claimed |= conjuncts(u)
    return claimed


def pattern_named(q, k):
    """patternNamed: the constructors a pattern names, given the constructors `k`."""
    if isinstance(q, s.PApp):
        return ({q.name} if q.name in k else set()) | set().union(*(pattern_named(x, k) for x in q.patterns))
    if isinstance(q, s.PTuple): return set().union(*(pattern_named(x, k) for x in q.patterns))
    return set()


def matched_in(u, k):
    """matchedIn: the constructors named by the patterns of the matches in a term."""
    return set().union(*(pattern_named(q, k) for node in term_nodes(u) if isinstance(node, s.MatchOf) for q, _ in node.arms))


def body_matched(b, k):
    """bodyMatched: the constructors the patterns of a body's matches and clauses name."""
    if isinstance(b, s.TermBody): return matched_in(b.term, k)
    if isinstance(b, s.ClausesBody):
        return set().union(*(pattern_named(q, k) | matched_in(c.body, k) for c in b.clauses for q in c.patterns))
    return set()


def law_names(p):
    """lawNames (program.lth 5f33db8): the names the claimed laws' bodies mention, and [proposed] the
    constructors named by the patterns of their own matches and clauses (group 2)."""
    claimed = claimed_laws(p); k = constructors(p)
    return set().union(*(dependencies(p, a, True) | body_matched(a.body, k)
                         for a in p if isinstance(a, s.Define) and a.name in claimed))


def fields_read(u):
    """fieldsRead: of a dotted name, the field after the first `.` (`s.world.read` reads `world`,
    program.lth 5f33db8, group 1); of a projection, its field; following children."""
    return {namePrefix(node.name.split('.', 1)[1]) if isinstance(node, s.Name) else node.field
            for node in term_nodes(u)
            if isinstance(node, s.Name) and '.' in node.name or isinstance(node, s.Proj)}


def binders_reads(bs):
    """bindersReads (program.lth 02aa8af, [proposed]): a binder's type and default are occurrences (1.S7)."""
    return set().union(*(fields_read(b.type) | fields_read(getattr(b, 'default', None)) for b in bs))


def law_reads(p):
    claimed = claimed_laws(p)
    result = set()
    for a in p:
        if not isinstance(a, s.Define) or a.name not in claimed: continue
        result |= binders_reads(a.binders)
        if isinstance(a.body, s.TermBody): result |= fields_read(a.body.term)
        elif isinstance(a.body, s.ClausesBody):
            for clause in a.body.clauses: result |= fields_read(clause.body)
    return result


def violatesR1(p, n):
    """4.R1: a declaration mentions only existing names."""
    return any(unknown(p, dependencies(p, a)) for a in acts(p, n, s.Declare))


def violatesR2Exists(p, n):
    """4.R2 (existence half): every name a definition mentions exists."""
    return any(unknown(p, dependencies(p, a) | dependencies(p, a, True)) for a in acts(p, n, s.Define))


violatesR2 = violatesR2Exists


def violatesR3(p, n):
    """4.R3: predicates touch all labels/binders, theories all fields, data all constructors through claimed laws."""
    laws = law_names(p)
    d = declared(p, n)
    if isinstance(d, s.Record) and acts(p, n, s.Define) and {x for f in d.fields for x in f.names} - law_reads(p): return True
    for a in acts(p, n, s.Define):
        b = a.body
        if isinstance(b, s.DataBody) and {x for x, _ in b.constructors} - laws: return True
        if not isinstance(b, s.TermBody): continue
        u = b.term; labels = None; law = None
        if isinstance(u, s.Record) and u.law is not None: labels = {x for f in u.fields for x in f.names}; law = u.law
        if isinstance(u, s.Subtype):
            labels = pattern_binds(u.pattern, constructors(p)); law = u.law
            if not labels: return True
        if isinstance(u, s.Lambda) and lambda_is_predicate(p, a):
            labels = param_binds(u.params, constructors(p)); law = s.Block(u.items, u.body)
        if labels is not None and labels - touched(names(law, constructors(p))): return True
    return False


def touched(ns):
    """4.R3 with 1.S7 (program.lth 02aa8af, [proposed]): a projection `v.n` touches `v`."""
    return set(ns) | {namePrefix(x) for x in ns}


def ends_in_verdict(p, u, fuel=8):
    """endsInVerdict, with an alias looked through (4.R7: the checker expands aliases first)."""
    if isinstance(u, s.Binop): return u.operator == '->' and ends_in_verdict(p, u.right, fuel)
    if isinstance(u, s.Pi): return ends_in_verdict(p, u.codomain, fuel)
    h = head(u)
    if isinstance(h, s.Name):
        if h.name in ('Bool', 'Law') or isinstance(u, s.App) and h.name == 'Failures': return True
        alias = next((a.value for a in acts(p, h.name, s.Alias)), None)
        if alias is not None and fuel: return ends_in_verdict(p, alias, fuel - 1)
    return False


def is_arrow(p, u, fuel=8):
    if isinstance(u, s.Binop): return u.operator == '->'
    if isinstance(u, s.Pi): return True
    h = head(u)
    alias = next((a.value for a in acts(p, h.name, s.Alias)), None) if isinstance(h, s.Name) else None
    return alias is not None and fuel > 0 and is_arrow(p, alias, fuel - 1)


def lambda_is_predicate(p, a):
    """lambdaIsPredicate (program.lth 5f33db8, group 5): the type written ends in a verdict; with
    none written, the declared type is not a function, or ends in a verdict; or nothing is written
    or declared."""
    if a.type is not None: return ends_in_verdict(p, a.type)
    d = declared(p, a.name)
    return d is None or not is_arrow(p, d) or ends_in_verdict(p, d)


def violatesR4(p, n):
    """4.R4: a new type at U is data, a subtype, a record with a law, an extern or a primitive."""
    for a in acts(p, n, s.Define):
        if type_of_act(p, a) != s.Universe(): continue
        b = a.body
        if isinstance(b, s.DataBody): continue
        if isinstance(b, s.TermBody) and (isinstance(b.term, s.Subtype) or isinstance(b.term, s.Record) and b.term.law is not None or head(b.term) in (s.Name('extern'), s.Name('primitive'))): continue
        return True
    return False


def violatesR5(p, n):
    """4.R5: a nonprovisional extern gives no type and mentions only defined, alias, constructor or core types."""
    for a in acts(p, n, s.Define):
        if not isinstance(a.body, s.TermBody) or head(a.body.term) != s.Name('extern') or provisional(a.body.term): continue
        ty = type_of_act(p, a)
        known = coreNames | constructors(p) | {a.name for a in p if isinstance(a, (s.Define, s.Alias))}
        if ty == s.Universe() or names(ty, constructors(p)) - known: return True
    return False


def violatesR7(p, n):
    """4.R7: an alias is neither declared nor defined."""
    return bool(acts(p, n, s.Alias) and (acts(p, n, s.Declare) or acts(p, n, s.Define)))


def block_fault(u, defined):
    if isinstance(u, (s.Block, s.Lambda)):
        defined = set(defined)
        for it in u.items:
            if item_binds(it, frozenset()) & defined or block_fault(it.value, defined): return True
            if isinstance(it, s.Bind): defined.add(it.name)
        return block_fault(u.value if isinstance(u, s.Block) else u.body, defined)
    if isinstance(u, (s.Record, s.Subtype, s.Sum, s.Pi, s.Sigma, s.SigmaNamed)): return False
    if isinstance(u, tuple): return any(block_fault(v, defined) for v in u)
    if is_dataclass(u): return any(block_fault(getattr(u, f.name), defined) for f in fields(u))
    return False


def violatesR12(p, n):
    """4.R12: define once; a block may neither redefine an enclosing name nor rebind a := name."""
    return len(acts(p, n, s.Define)) > 1 or any(isinstance(a.body, s.TermBody) and block_fault(a.body.term, {x.name for x in p if hasattr(x, 'name')}) for a in acts(p, n, s.Define))


def arrows(u):
    """Read `implies A B` in type position as the arrow `A -> B`.

    elaborate.py reads `A -> B` as the Bool implication when it cannot infer that `A` is a type,
    as for a name brought in by an import (imports are read for typing only, given the file's path). An implication is never a
    type, so where a type is expected it can only be that arrow. Predicates of subtypes and terms
    are not entered: there `implies` is the implication.
    """
    if isinstance(u, t.App) and isinstance(u.function, t.App) and u.function.function == t.Var('implies'):
        return t.Pi('_', arrows(u.function.argument), arrows(u.argument))
    if isinstance(u, t.Pi): return t.Pi(u.name, arrows(u.domain), arrows(u.codomain))
    if isinstance(u, t.Sigma): return t.Sigma(u.name, arrows(u.domain), arrows(u.codomain))
    if isinstance(u, t.Record): return t.Record(tuple((n, arrows(x)) for n, x in u.fields))
    if isinstance(u, t.Sum): return t.Sum(tuple((n, arrows(x)) for n, x in u.alternatives))
    if isinstance(u, t.Subtype): return t.Subtype(u.name, arrows(u.type), u.predicate)
    if isinstance(u, t.App): return t.App(arrows(u.function), arrows(u.argument))
    return u


def _map(u, f):
    """Rebuild a term with `f` applied to each child (tuples and dataclasses), strings kept."""
    if isinstance(u, tuple): return tuple(f(x) for x in u)
    if is_dataclass(u) and not isinstance(u, type): return type(u)(*(f(getattr(u, x.name)) for x in fields(u)))
    return u


def field_labels(u):
    return {n for node in nodes(u) if isinstance(node, t.Record) for n, _ in node.fields}


def rename_free(u, old, new):
    """Rename the free `old` to `new`, stopping at a binder of `old` and at a record field labeled
    `old`, which binds it for the fields after it."""
    if isinstance(u, t.Var): return t.Var(new) if u.name == old else u
    if isinstance(u, (t.Pi, t.Sigma, t.Lam, t.Subtype)):
        first, second = (u.domain, u.codomain) if isinstance(u, (t.Pi, t.Sigma)) else (u.type, u.body if isinstance(u, t.Lam) else u.predicate)
        return type(u)(u.name, rename_free(first, old, new), second if u.name == old else rename_free(second, old, new))
    if isinstance(u, t.Record):
        result = []; bound = False
        for n, ty in u.fields:
            result.append((n, ty if bound else rename_free(ty, old, new))); bound = bound or n == old
        return t.Record(tuple(result))
    return _map(u, lambda x: rename_free(x, old, new))


def unclash(u):
    """Rename a Pi or Sigma binder that a record in its codomain also has as a field label, so that
    substituting an argument for the binder (kernel.substitute, which takes record fields for free
    names) cannot capture the field: `identity (n : Nat) : Mat Float64` applied to `k` keeps the
    field `n` of `{ m, n, f : Fin m -> Fin n -> Float64 }` (cause c of the leftovers report)."""
    if isinstance(u, (t.Pi, t.Sigma)) and u.name in field_labels(u.codomain):
        taken = {x for node in nodes(u) for x in ([node.name] if isinstance(node, t.Var) else [])} | field_labels(u)
        fresh = u.name + "'"
        while fresh in taken: fresh += "'"
        return type(u)(fresh, unclash(u.domain), unclash(rename_free(u.codomain, u.name, fresh)))
    return _map(u, unclash)


class Typing:
    """Small rules-needed typing; no unification or complete dependent checking."""
    def __init__(self, p):
        self.program = elaborate_program(p)
        self.context = context_of(p)
        # Preserve written declarations: context_of currently overwrites them with
        # a Hole for a later unannotated definition.
        declarations = {}
        for a in p:
            if isinstance(a, s.Declare):
                inner = self.context.child()
                ps = parameters(a.binders, inner)
                declarations[a.name] = curry(t.Pi, ps, walk(a.type, inner))
        self.program = tuple(t.Declare(a.name, arrows(declarations[a.name]))
                             if isinstance(a, t.Declare) else a for a in self.program)
        self.types = {a.name: arrows(unclash(a.type)) for a in self.program if isinstance(a, (t.Declare, t.Define))}

    def same(self, a, b):
        # Reduction is bounded; recursive definitions cannot hang checking.
        a = reduce(self.program, len(self.program) + 1, a) or a
        b = reduce(self.program, len(self.program) + 1, b) or b
        if isinstance(a, t.Record) and isinstance(b, t.Record):
            return len(a.fields) == len(b.fields) and all(
                n == m and self.same(x, y) for (n, x), (m, y) in zip(a.fields, b.fields))
        return alpha_equal(a, b)

    def refines(self, a, b):
        # a hole is a type not inferred (an unannotated lambda parameter): unknown, never compared
        if isinstance(a, t.Hole) or isinstance(b, t.Hole): return True
        if self.same(a, b): return True
        if isinstance(a, t.Subtype): return self.refines(a.type, b)
        if a == t.Var('Float64') and b == t.Var('Real'): return True
        if isinstance(a, t.Pi) and isinstance(b, t.Pi):
            return self.refines(b.domain, a.domain) and self.refines(a.codomain, substitute(b.name, t.Var(a.name), b.codomain))
        return False

    def typeOf(self, u, ctx=None):
        c = self.context.child(); c.types.update(self.types); c.types.update(ctx or {})
        ty = infer(u, c)
        return None if isinstance(ty, t.Hole) else arrows(ty)

    def theory_record(self, u):
        """The record a theory head stands for, as elaborate.theory_domains reads a domain."""
        c = self.context.child(); c.types.update(self.types)
        domain = theory_domains(t.Pi('_', u, t.Var('Bool')), c).domain
        return domain if isinstance(domain, t.Record) else None

    def branchContext(self, ctx, condition, truth):
        law = condition if truth else t.App(t.Var('not'), condition)
        mentioned = free_names(condition)
        return {n: t.Subtype(n, ty, law) if n in mentioned else ty
                for n, ty in ctx.items()}

    def applications(self, u, ctx=None):
        ctx = dict(ctx or {})
        if isinstance(u, t.App):
            yield ctx, u.function, u.argument
            yield from self.applications(u.function, ctx); yield from self.applications(u.argument, ctx)
        elif isinstance(u, (t.Lam, t.Pi, t.Sigma, t.Subtype, t.Let)):
            annotation = u.domain if isinstance(u, (t.Pi, t.Sigma)) else u.type
            yield from self.applications(annotation, ctx)
            if isinstance(u, t.Let): yield from self.applications(u.value, ctx)
            ctx[u.name] = annotation
            body = u.codomain if isinstance(u, (t.Pi, t.Sigma)) else u.predicate if isinstance(u, t.Subtype) else u.body
            yield from self.applications(body, ctx)
        elif isinstance(u, t.Pair):
            yield from self.applications(u.left, ctx); yield from self.applications(u.right, ctx)
        elif isinstance(u, t.Inj): yield from self.applications(u.value, ctx)
        elif isinstance(u, t.Match):
            yield from self.applications(u.value, ctx)
            for _, b in u.arms: yield from self.applications(b, ctx)

    def body(self, n):
        return next((a.body for a in self.program if isinstance(a, t.Define) and a.name == n), None)


@lru_cache(maxsize=8)
def _typing(p):
    return Typing(p)


class Program(tuple):
    """A file's acts, with the acts its imports bring (12.S22), read for typing only: the rules are
    still checked on the file's own names, and the surface rules see the file alone."""
    imported = ()
    typing = None


def resolve(path, name):
    """12.S4: next to the importing file, then each directory of LUTHIER_PATH, then lib/; the
    extension `.lut` may be omitted."""
    import os
    from pathlib import Path
    dirs = [Path(path).parent] + [Path(d) for d in os.environ.get('LUTHIER_PATH', '').split(os.pathsep) if d] + [Path(__file__).parent / 'lib']
    for d in dirs:
        for candidate in (d / name, d / (name + '.lut')):
            if candidate.is_file(): return candidate.resolve()
    return None


def load_imports(program, path, seen=None):
    """The acts that `program`'s imports bring, transitively, as run.py's loader reads them: a name
    imported `as` another becomes an alias. Unreadable files are skipped (4.R2 names what is
    missing); operators and data are left out, being the imported file's own business."""
    from .parse import parse
    seen = set() if seen is None else seen
    result = []
    for act in program:
        if not isinstance(act, s.ImportAct): continue
        target = resolve(path, act.path)
        if target is not None and target not in seen:
            seen.add(target)
            try: parsed = parse(target.read_text(encoding='utf-8'))
            except OSError: parsed = None
            if isinstance(parsed, s.Parsed):
                result.extend(load_imports(parsed.program, target, seen))
                result.extend(a for a in parsed.program if isinstance(a, (s.Declare, s.Define, s.Alias)))
        result.extend(s.Alias(i.asName, (), s.Name(i.name)) for i in act.names if i.asName)
    return tuple(result)


def elaborates(a):
    """An imported act the elaborator reads alone (record refinements it does not, `LeqPair`)."""
    try: elaborate_program((a,)); return True
    except ElaborationError: return False


def typing_of(p):
    """The typing of a file read with its imports (12.S22, so that `base` sees an imported
    subtype's definition); of the file alone when the two do not elaborate together."""
    if not isinstance(p, Program) or not p.imported: return _typing(tuple(p))
    if p.typing is None:
        own = {a.name for a in p if hasattr(a, 'name')}
        imported = tuple(a for a in p.imported if a.name not in own and elaborates(a))
        try: p.typing = Typing(imported + tuple(p))
        except ElaborationError: p.typing = _typing(tuple(p))
    return p.typing


def verdict_type(u):
    return u == t.Var('Bool') or isinstance(u, t.App) and u.function == t.Var('Failures') or isinstance(u, t.Pi) and verdict_type(u.codomain)


def fits(typing, ty, bt):
    if bt is None: return False
    if isinstance(ty, t.Pi) and isinstance(bt, t.Pi):
        return typing.same(ty.domain, bt.domain) and fits(typing, ty.codomain, substitute(bt.name, t.Var(ty.name), bt.codomain))
    return typing.same(ty, bt) or isinstance(bt, t.Pi) and typing.same(ty, bt.domain) and verdict_type(bt.codomain) or isinstance(bt, t.App) and typing.same(bt, t.App(t.Var('Law'), ty))


def violatesR6(p, n):
    """4.R6: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters."""
    if not acts(p, n, s.Declare) or not acts(p, n, s.Define): return False
    q = typing_of(p); ty = next(a.type for a in q.program if isinstance(a, t.Declare) and a.name == n)
    return not fits(q, ty, q.typeOf(q.body(n)))


def contains_arrow(q, u, fuel):
    if isinstance(u, t.Pi): return True
    if isinstance(u, t.Var) and fuel:
        body = q.body(u.name)
        if body is None:
            body = q.types.get(u.name)
            if not isinstance(body, t.Record): return False
        return contains_arrow(q, body, fuel - 1)
    if isinstance(u, t.Data):
        for _, ty in u.constructors:
            while isinstance(ty, t.Pi):
                if contains_arrow(q, ty.domain, fuel): return True
                ty = ty.codomain
        return False
    if isinstance(u, t.Subtype): return contains_arrow(q, u.type, fuel)
    if isinstance(u, t.Sigma): return contains_arrow(q, u.domain, fuel) or contains_arrow(q, u.codomain, fuel)
    if isinstance(u, (t.Sum, t.Record)): return any(contains_arrow(q, ty, fuel) for _, ty in (u.alternatives if isinstance(u, t.Sum) else u.fields))
    if isinstance(u, t.App): return contains_arrow(q, u.function, fuel) or contains_arrow(q, u.argument, fuel)
    return False


def violatesR8(p, n):
    """4.R8: structural == is forbidden on a type containing an exponential."""
    q = typing_of(p)
    return any(isinstance(f, t.App) and f.function == t.Var('==') and contains_arrow(q, q.typeOf(f.argument, c), len(q.program)) for c, f, _ in q.applications(q.body(n)))


# Spec 11.R1: core's `Nat` is `{ k : Int | 0 <= k }` and `Fin n` is `{ k : Int | 0 <= k and k < n }`.
# Core is not in the elaborated program, so `base` reads these two subtypes of `Int` from here.
CORE_SUBTYPE_BASES = {'Nat': t.Var('Int'), 'Fin': t.Var('Int')}


def core_subtype_base(q, u):
    """The base of a core subtype (11.R1) the program does not define itself, or None."""
    h = u
    while isinstance(h, t.App): h = h.function
    if not isinstance(h, t.Var) or h.name not in CORE_SUBTYPE_BASES or q.body(h.name) is not None: return None
    return CORE_SUBTYPE_BASES[h.name] if (h.name == 'Fin') == isinstance(u, t.App) else None


def base(q, u, fuel=None):
    """Look through literal subtypes, names defined as subtypes (applied, when they take parameters),
    core's subtypes, and theory heads.

    A theory head `T : { ... }` defined by laws is its record refined by them (4.R6: the body is a
    predicate over the record), and elaborate.theory_domains already reads a domain `T` (or `T a
    b`) as that record; the argument side is read the same way, so `(l : T)` passes where `T` is
    expected (library.lth, reading 6 of the file-policies report).
    """
    if fuel is None: fuel = len(q.program)
    # A subtype's base is read in type position (`arrows`): inside it, an alias's `Fin n -> A` is
    # elaborated as `implies (Fin n) A` (cause b of the leftovers report, as in bite 3b part 1).
    if isinstance(u, t.Subtype): return base(q, arrows(u.type), fuel)
    if isinstance(u, t.Var) and fuel:
        body = q.body(u.name)
        if isinstance(body, t.Subtype): return base(q, arrows(body.type), fuel - 1)
    if isinstance(u, t.App) and fuel:
        # a name defined as a subtype with parameters, applied (`LexedText d g`, grammar.lth): its
        # body under the parameters is a subtype, looked through as the bare name is
        h = u
        while isinstance(h, t.App): h = h.function
        body = q.body(h.name) if isinstance(h, t.Var) else None
        while isinstance(body, t.Lam): body = body.body
        if isinstance(body, t.Subtype):
            unfolded = reduce(q.program, len(q.program) + 1, u)
            if isinstance(unfolded, t.Subtype): return base(q, arrows(unfolded.type), fuel - 1)
    if isinstance(u, (t.Var, t.App)) and core_subtype_base(q, u) is not None: return core_subtype_base(q, u)
    if isinstance(u, (t.Var, t.App)):
        record = q.theory_record(u)
        if record is not None: return record
    return u


def theory_head(q, u):
    """A theory head, `T` (or `T a`) declared at a record and defined by laws, used as a type (`Maybe
    T`): a type, at `U`; its declared record is the type of a model, not of `T` itself."""
    while isinstance(u, t.App): u = u.function
    return (isinstance(u, t.Var) and isinstance(q.body(u.name), (t.Lam, t.App, t.Var)) and
            any(isinstance(a, t.Declare) and a.name == u.name for a in q.program) and q.theory_record(u) is not None)


def violatesR9(p, n):
    """4.R9: application argument bases must refine domain bases, with function variance."""
    q = typing_of(p)
    for a in acts(p, n, s.Define):
        if isinstance(a.type, s.Record):
            expected = q.types.get(n); actual = q.typeOf(q.body(n))
            while isinstance(expected, t.Pi) and isinstance(actual, t.Pi):
                actual = substitute(actual.name, t.Var(expected.name), actual.codomain)
                expected = expected.codomain
            if isinstance(actual, t.Record) and isinstance(expected, t.Record) and not q.refines(actual, expected): return True
    for c, f, x in q.applications(q.body(n)):
        ft = q.typeOf(f, c); at = t.Universe() if theory_head(q, x) else q.typeOf(x, c)
        if isinstance(ft, t.Pi) and at is not None and not q.refines(base(q, at), base(q, ft.domain)): return True
    return False


def violatesR10(p, n):
    """4.R10: whether a law characterizes is author judgement; no rejection predicate in the theory."""
    return False


def violatesR11(p, n):
    """4.R11: branch refinement is a Typing law, not a rejection predicate in the theory."""
    return False


def violatesS14(p, n):
    """4.S14: an explicit Bool definition mentioned by no other body's names is unclaimed."""
    other = set().union(*(dependencies(p, a, True) for a in p if isinstance(a, s.Define) and a.name != n))
    return any(a.type == s.Name('Bool') and n not in other for a in acts(p, n, s.Define))


def provisionalExtern(p, n):
    return any(isinstance(a.body, s.TermBody) and head(a.body.term) == s.Name('extern') and provisional(a.body.term) for a in acts(p, n, s.Define))


def looseFunction(p, n):
    return any(a.binders or isinstance(a.type, s.Binop) and a.type.operator == '->' for a in acts(p, n, s.Define))


def term_nodes(u):
    """anyTerm/children: lambda annotations and match patterns are not children."""
    yield u
    if isinstance(u, s.Lambda):
        children = tuple(it.value for it in u.items) + (u.body,)
    elif isinstance(u, s.MatchOf):
        children = (u.value,) + tuple(b for _, b in u.arms)
    elif isinstance(u, tuple): children = u
    elif is_dataclass(u): children = tuple(getattr(u, f.name) for f in fields(u))
    else: children = ()
    for child in children: yield from term_nodes(child)


def body_nodes(body):
    # inBody visits terms and clause bodies, never constructor types/patterns.
    if isinstance(body, s.TermBody): yield from term_nodes(body.term)
    elif isinstance(body, s.ClausesBody):
        for clause in body.clauses: yield from term_nodes(clause.body)


def violatesR2R1(p, n):
    """2.R1: a named argument names a parameter of its head's binders."""
    introduced = {a.name for a in p if hasattr(a, 'name')}
    for a in acts(p, n, s.Define):
        for u in body_nodes(a.body):
            h = head(u)
            if not isinstance(h, s.Name) or h.name not in introduced: continue
            params = next(({x for b in a.binders for x in b.names} for a in p
                           if getattr(a, 'name', None) == h.name and
                           (isinstance(a, s.Declare) or isinstance(a, s.Define) and a.binders)), set())
            while isinstance(u, s.App):
                if isinstance(u.argument, s.NamedArg) and u.argument.name not in params: return True
                u = u.function
    return False


def violatesR2R6(p, n):
    """2.R6: a rebinding whose previous binding was never used is an unused binding."""
    for a in acts(p, n, s.Define):
        for u in body_nodes(a.body):
            if not isinstance(u, (s.Block, s.Lambda)): continue
            pending = param_binds(u.params, frozenset()) if isinstance(u, s.Lambda) else {x for b in a.binders for x in b.names}
            for it in u.items:
                pending -= names(it.value)
                if isinstance(it, s.Rebind):
                    if pattern_binds(it.pattern, frozenset()) & pending: return True
                    pending |= pattern_binds(it.pattern, frozenset())
    return False


def surface_signature(p, n):
    """signatureOf (program.lth 02aa8af, [proposed]): the binders' types in order, and the type
    written on the definition or else declared."""
    a = next(iter(acts(p, n, s.Define)), None)
    if a is None: return ((), declared(p, n))
    return (tuple(b.type for b in a.binders for _ in b.names), type_of_act(p, a))


def violatesR13(p, n):
    """4.R13: two functions of the same declared type bind one operator."""
    bindings = [(a.operator, a.value.name) for a in p if isinstance(a, s.OperatorAct) and isinstance(a.value, s.Name)]
    rivals = [g for o, f in bindings for o2, g in bindings if f == n and o == o2 and g != n]
    if not rivals: return False
    # The elaborated declared types, binders included (curried), compared up to renaming; the
    # surface signature when the program does not elaborate.
    try:
        q = typing_of(p)
        return any(n in q.types and g in q.types and alpha_equal(q.types[g], q.types[n]) for g in rivals)
    except ElaborationError:
        return any(surface_signature(p, g) == surface_signature(p, n) for g in rivals)


def violates6R1(p, n):
    """6.R1: a citation datum's reference must type as Reference."""
    q = typing_of(p)
    for a in q.program:
        if not isinstance(a, t.Datum): continue
        u = a.value; args = []
        while isinstance(u, t.App):
            args.append(u.argument); u = u.function
        args.reverse()
        if u == t.Var('cite') and len(args) >= 2 and args[0] == t.Var(n):
            ty = q.typeOf(args[1])
            if ty is None or not q.same(ty, t.Var('Reference')): return True
    return False


def check(program, path=None) -> list[Failure]:
    """Report each implemented program.lth predicate on each introduced name; with the file's
    `path`, its imports are read for typing (12.S22)."""
    result = []
    if path is not None:
        program = Program(program); program.imported = load_imports(program, path)
    for n in dict.fromkeys(a.name for a in program if isinstance(a, (s.Declare, s.Define, s.Alias))):
        for rule, predicate in [(f'4.R{k}', globals()[f'violatesR{k}']) for k in range(1, 14)] + [('2.R1', violatesR2R1), ('2.R6', violatesR2R6), ('6.R1', violates6R1)]:
            try:
                bad = predicate(program, n)
            except ElaborationError:
                # Surface rules still run; missing elaboration is recorded by the audit.
                bad = False
            if bad:
                message = predicate.__doc__.split(': ', 1)[1]
                if rule == '4.R12': message = 'defined twice: ' + message
                result.append(Failure(rule, n, message))
    return result


def report(program) -> list[Report]:
    result = []
    for n in dict.fromkeys(a.name for a in program if isinstance(a, (s.Declare, s.Define, s.Alias))):
        for kind, pred, message in [('unclaimed', violatesS14, 'No other definition claims this Bool law.'), ('provisional', provisionalExtern, 'Provisional extern.'), ('loose', looseFunction, 'Top-level function; reported pending local definitions.')]:
            if pred(program, n): result.append(Report(kind, n, message))
    return result
