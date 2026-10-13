"""Python specimen of translation.lth (5d7963b), user prompt 2026-10-13 v1.

Until check.py exists, typing is approximated by declarations, binder annotations,
expected lambda types and local structural inference. Unknown types remain Hole;
this is not the theory's rejection of every ill-typed term. In particular there is
no unification, dependent checking, overload ambiguity or exhaustiveness check.
Numbers default to Int/Float64; *, + and -> inspect the left operand's inferred
type. Implicits infer direct type parameters from explicit argument types.
Imports retain qualified names but do not load modules. Applied externs remain
stuck kernel terms: no host calls are performed. Fresh names are deterministic.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from . import surface as s, term as t
from .kernel import alpha_equal, substitute


class ElaborationError(ValueError):
    pass


def apps(f, args):
    for a in args:
        f = t.App(f, a)
    return f


def pairs(values, cls=t.Pair):
    if not values:
        raise ElaborationError('empty tuple has no kernel representation')
    result = values[-1]
    for value in reversed(values[:-1]):
        result = cls(value, result)
    return result


def constant(value):
    return {s.IntLit: t.IntConst, s.FloatLit: t.FloatConst,
            s.StringLit: t.StringConst}[type(value)](value.value)


@dataclass
class Context:
    types: dict = field(default_factory=dict)
    signatures: dict = field(default_factory=dict)
    aliases: dict = field(default_factory=dict)
    operators: dict = field(default_factory=dict)
    constructors: set = field(default_factory=lambda: {'true', 'false', 'nil', 'cons', 'just', 'nothing', 'ok', 'failed'})
    names: dict = field(default_factory=dict)
    used: set = field(default_factory=set)

    def child(self):
        return Context(self.types.copy(), self.signatures, self.aliases,
                       self.operators, self.constructors, self.names.copy(), self.used)

    def fresh(self, name):
        candidate = name
        while candidate in self.used:
            candidate += "'"
        self.used.add(candidate)
        return candidate


def infer(v, c):
    match v:
        case t.Var(n):
            if n in {'List', 'Maybe', 'Failures'}:
                return t.Pi('_', t.Universe(), t.Universe())
            ty = c.types.get(n, t.Universe() if n in {'Int', 'Float64', 'Bool', 'String', 'Nat', 'Unit'} else t.Hole('type'))
            return theory_domains(ty, c)
        case t.Lit(k):
            return t.Var({t.IntConst: 'Int', t.FloatConst: 'Float64', t.StringConst: 'String'}[type(k)])
        case t.Universe() | t.World() | t.Pi() | t.Sigma() | t.Sum() | t.Record() | t.Data() | t.Subtype():
            return t.Universe()
        case t.Lam(n, a, b):
            inner = c.child(); inner.types[n] = a
            return t.Pi(n, a, infer(b, inner))
        case t.App(f, a):
            if isinstance(f, t.App) and f.function == t.Var('&'):
                left = infer(f.argument, c)
                right = infer(a, c)
                if (isinstance(left, t.Subtype) and isinstance(right, t.Subtype)
                        and alpha_equal(left.type, right.type)):
                    law = substitute(right.name, t.Var(left.name), right.predicate)
                    return t.Subtype(left.name, left.type,
                                     apps(t.Var('&'), [left.predicate, law]))
                # Laws may quantify different arguments after their model.
                # Their conjunction is still a predicate over that model.
                if isinstance(left, t.Pi) and isinstance(right, t.Pi):
                    if (boolean_law(left) and boolean_law(right)
                            and alpha_equal(left.domain, right.domain)):
                        return theory_domains(t.Pi(left.name, left.domain, t.Var('Bool')), c)
                if left == right:
                    return left
                return t.Hole('type')
            ty = infer(f, c)
            if isinstance(ty, t.Pi):
                return substitute(ty.name, a, ty.codomain)
            head = f
            while isinstance(head, t.App):
                head = head.function
            if isinstance(head, t.Var):
                if head.name in {'==', '<', 'and', 'or', 'implies', 'holds'}:
                    return t.Var('Bool')
                if head.name in {'+', '-', '*', '/', 'mod'}:
                    return infer(f.argument if isinstance(f, t.App) else a, c)
            return t.Hole('type')
        case t.RecordValue(fs):
            return t.Record(tuple((n, infer(x, c)) for n, x in fs))
        case t.Proj(r, n):
            ty = infer(r, c)
            return dict(ty.fields).get(n, t.Hole('type')) if isinstance(ty, t.Record) else t.Hole('type')
        case t.Let(n, a, _, b):
            inner = c.child(); inner.types[n] = a
            return infer(b, inner)
        case t.Match(_, arms):
            return infer(arms[0][1], c) if arms else t.Hole('type')
        case t.Pair(a, b):
            return t.Sigma('_', infer(a, c), infer(b, c))
    return t.Hole('type')


def theory_domains(ty, c):
    """Keep a law's model domain tied to the declared theory record."""
    if isinstance(ty, t.Pi):
        domain = ty.domain
        head = domain
        args = []
        while isinstance(head, t.App):
            args.append(head.argument); head = head.function
        if isinstance(head, t.Var):
            declared = c.types.get(head.name)
            for arg in reversed(args):
                declared = substitute(declared.name, arg, declared.codomain) if isinstance(declared, t.Pi) else None
            if isinstance(declared, t.Record):
                domain = declared
        return t.Pi(ty.name, domain, theory_domains(ty.codomain, c))
    return ty


def boolean_law(ty):
    while isinstance(ty, t.Pi):
        ty = ty.codomain
    return ty == t.Var('Bool')


def pattern(p, c, fresh=False):
    """A surface pattern as in a `match` arm; `fresh` renames its variables, as a block item does."""
    match p:
        case s.PWild(): return t.PWild()
        case s.PLit(k): return t.PLit(constant(k))
        case s.PTuple(ps): return pairs([pattern(x, c, fresh) for x in ps], t.PPair)
        case s.PApp(n, ps):
            if ps or n in c.constructors:
                return t.PCon(n, tuple(pattern(x, c, fresh) for x in ps))
            m = c.fresh(n) if fresh else n
            c.names[n] = m
            return t.PVar(m)
    raise ElaborationError(f'unsupported pattern {p!r}')


def bare_name(p, c):
    """The name of a pattern that is a bare variable, else None."""
    if isinstance(p, s.PApp) and not p.patterns and p.name not in c.constructors:
        return p.name
    return None


def pattern_types(q, ty, c):
    """Give the variables of `q` the components of `ty` where its shape follows the pattern."""
    match q:
        case t.PVar(n): c.types[n] = ty
        case t.PPair(a, b) if isinstance(ty, t.Sigma):
            pattern_types(a, ty.domain, c)
            pattern_types(b, ty.codomain if ty.name == '_' else t.Hole('type'), c)


def is_action(ty):
    """An action's result: `W * A` for the world `W` (D8, D-2026-10-13-ag)."""
    return isinstance(ty, t.Sigma) and isinstance(ty.domain, t.World)


def block(items, body, c, expected):
    """translation.lth (87d6091) law `Blocks`: each item in order, the rest of the block under it.

    `x := t` and a bare name on a value that is not an action are a `Let` on a fresh name (4.R12);
    a pattern on `<-` is a `match` with one arm (on an action's `W * A`), a bare name on `W * Unit` binding
    the token and dropping the unit (D-2026-10-13-ag). A pattern that is not a bare name is that
    one-arm `match` whatever the value's type (1665b9d, 2.S17); only a bare name on a non-action
    stays a `Let`.
    """
    if not items:
        return walk(body, c, expected)
    item, rest = items[0], items[1:]
    name = item.name if isinstance(item, s.Bind) else bare_name(item.pattern, c)
    if name is not None:
        previous = walk(s.Name(name), c)
        value = walk(item.value, c, infer(previous, c))
    else:
        value = walk(item.value, c)
    ty = infer(value, c)
    if isinstance(item, s.Rebind) and (is_action(ty) or name is None):
        inner = c.child()
        if name is not None and ty.codomain == t.Var('Unit'):
            n = inner.fresh(name); inner.names[name] = n
            q = t.PPair(t.PVar(n), t.PWild())
        else:
            q = pattern(item.pattern, inner, fresh=True)
        pattern_types(q, ty, inner)
        return t.Match(value, ((q, block(rest, body, inner, expected)),))
    inner = c.child()
    n = inner.fresh(name); inner.names[name] = n; inner.types[n] = ty
    return t.Let(n, ty, value, block(rest, body, inner, expected))


def parameters(binders, c):
    result = []
    for b in binders:
        a = walk(b.type, c)
        for n in b.names:
            result.append((n, a)); c.types[n] = a; c.names[n] = n
    return result


def curry(cls, params, body):
    for n, a in reversed(params):
        body = cls(n, a, body)
    return body


def application(v, c):
    def apply(result, arguments):
        ty = infer(result, c)
        for arg in arguments:
            value = walk(arg, c, ty.domain if isinstance(ty, t.Pi) else None)
            result = t.App(result, value)
            ty = substitute(ty.name, value, ty.codomain) if isinstance(ty, t.Pi) else None
        return result

    arguments = []
    head = v
    while isinstance(head, s.App):
        arguments.append(head.argument); head = head.function
    arguments.reverse()
    if (head == s.Name('extern') and arguments
            and isinstance(arguments[0], s.Literal)
            and isinstance(arguments[0].literal, s.StringLit)):
        return apps(t.Extern(arguments[0].literal.value),
                    [walk(x, c) for x in arguments[1:]])
    if isinstance(head, s.Name) and head.name in c.aliases:
        alias = c.aliases[head.name]
        ns = [n for b in alias.binders for n in b.names]
        if len(arguments) < len(ns):
            raise ElaborationError(f'alias {head.name} needs {len(ns)} arguments')
        inner = c.child()
        for n, arg in zip(ns, arguments):
            inner.names[n] = walk(arg, c)
        return apply(walk(alias.value, inner), arguments[len(ns):])
    if not isinstance(head, s.Name) or head.name not in c.signatures:
        return apply(walk(head, c), arguments)
    bs = c.signatures[head.name]
    slots = [(n, b) for b in bs for n in b.names]
    named = {x.name: x.value for x in arguments if isinstance(x, s.NamedArg)}
    positional = iter(x for x in arguments if not isinstance(x, s.NamedArg))
    given = {}
    for n, b in slots:
        if isinstance(b, s.Explicit):
            arg = named.pop(n, None)
            if arg is None:
                arg = next(positional, None)
            if arg is not None:
                given[n] = arg
    if named:
        raise ElaborationError(f'unknown named argument {next(iter(named))}')
    inner = c.child()
    # Earlier arguments instantiate dependent parameter types. Infer direct
    # implicit type arguments while visiting the corresponding explicit slot.
    implicit_names = {n for n, b in slots if isinstance(b, s.Implicit)}
    for n, b in slots:
        if isinstance(b, s.Explicit) and n in given:
            given[n] = walk(given[n], c, walk(b.type, inner))
            inner.names[n] = given[n]
            if isinstance(b.type, s.Name) and b.type.name in implicit_names:
                given[b.type.name] = infer(given[n], c)
                inner.names[b.type.name] = given[b.type.name]
    for n, b in slots:
        if isinstance(b, s.Implicit):
            if n not in given:
                raise ElaborationError(f'cannot infer implicit {n}')
    complete = all(n in given or isinstance(b, s.Explicit) and b.default is not None for n, b in slots)
    result = walk(head, c)
    for n, b in slots:
        if n not in given and complete and isinstance(b, s.Explicit) and b.default is not None:
            given[n] = walk(b.default, inner, walk(b.type, inner))
        if n not in given:
            break
        result = t.App(result, given[n]); inner.names[n] = given[n]
    return apply(result, positional)


def walk(v, c, expected=None):
    match v:
        case s.Name(n):
            if n in c.names:
                value = c.names[n]
                return t.Var(value) if isinstance(value, str) else value
            if n in c.aliases:
                if c.aliases[n].binders:
                    raise ElaborationError(f'alias {n} needs arguments')
                return walk(c.aliases[n].value, c)
            return t.Var(n)
        case s.Literal(k): return t.Lit(constant(k))
        case s.Universe(): return t.Universe()
        case s.World(): return t.World()
        case s.App(): return application(v, c)
        case s.Binop(op, a, b):
            left = walk(a, c); right = walk(b, c)
            ty = infer(left, c)
            if isinstance(ty, t.Universe) and op in {'->', '*', '+'}:
                return t.Sum((('left', left), ('right', right))) if op == '+' else (t.Pi if op == '->' else t.Sigma)('_', left, right)
            op = 'implies' if op == '->' else op
            target = c.operators.get((op, ty), t.Var(op))
            return apps(target, [left, right])
        case s.Neg(x):
            value = walk(x, c)
            zero = t.FloatConst(0.0) if infer(value, c) == t.Var('Float64') else t.IntConst(0)
            return apps(t.Var('-'), [t.Lit(zero), value])
        case s.Tuple(xs): return pairs([walk(x, c) for x in xs])
        case s.Pi(ns, a, b) | s.Sigma(ns, a, b):
            inner = c.child(); domain = walk(a, c)
            for n in ns: inner.types[n] = domain
            return curry(t.Pi if isinstance(v, s.Pi) else t.Sigma, [(n, domain) for n in ns], walk(b, inner))
        case s.SigmaNamed(n, a, m, b):
            return t.Record(((n, walk(a, c)), (m, walk(b, c))))
        case s.Record(fs, law):
            result = t.Record(tuple((n, walk(f.type, c)) for f in fs for n in f.names))
            if law is not None: raise ElaborationError('record refinements require check.py')
            return result
        case s.RecordValue(fs): return t.RecordValue(tuple((n, walk(x, c)) for n, x in fs))
        case s.Sum(xs): return t.Sum(tuple((n, walk(x, c)) for n, x in xs))
        case s.List(xs):
            result = t.Var('nil')
            for x in reversed(xs): result = apps(t.Var('cons'), [walk(x, c), result])
            return result
        case s.Proj(x, n): return t.Proj(walk(x, c), n)
        case s.Block(items, body): return block(tuple(items), body, c.child(), expected)
        case s.Lambda(params, items, body):
            inner = c.child(); ps = []; shapes = []; exp = expected
            for p in params:
                a = walk(p.type, inner) if isinstance(p, s.TypedParam) else exp.domain if isinstance(exp, t.Pi) else t.Hole('type')
                if isinstance(p, s.ShapeParam):
                    n = inner.fresh('p'); q = pattern(s.PTuple(p.patterns), inner); shapes.append((n, q)); ns = [n]
                else: ns = p.names if isinstance(p, s.TypedParam) else [p.name]
                for n in ns:
                    ps.append((n, a)); inner.types[n] = a; inner.names[n] = n
                    if isinstance(exp, t.Pi): exp = substitute(exp.name, t.Var(n), exp.codomain)
            result = walk(s.Block(items, body), inner, exp) if items else walk(body, inner, exp)
            for n, q in reversed(shapes): result = t.Match(t.Var(n), ((q, result),))
            return curry(t.Lam, ps, result)
        case s.MatchOf(x, arms):
            result = []
            for p, b in arms:
                inner = c.child(); q = pattern(p, inner); result.append((q, walk(b, inner)))
            return t.Match(walk(x, c), tuple(result))
        case s.IfThen(cond, yes, no):
            value = walk(cond, c); a = walk(yes, c); ty = infer(value, c)
            failures = isinstance(ty, t.App) and ty.function == t.Var('Failures')
            if no is None and failures:
                x = c.fresh('x'); xs = c.fresh('xs')
                return t.Match(value, ((t.PCon('nil', ()), t.App(t.Var('ok'), a)), (t.PCon('cons', (t.PVar(x), t.PVar(xs))), t.App(t.Var('failed'), t.Var(x)))))
            if failures: value = t.App(t.Var('holds'), value)
            b = walk(no, c) if no is not None else t.Var('nothing')
            if no is None: a = t.App(t.Var('just'), a)
            return t.Match(value, ((t.PCon('true', ()), a), (t.PCon('false', ()), b)))
        case s.Subtype(s.PApp(n, ()), a, law): return t.Subtype(n, walk(a, c), walk(law, c))
        case s.Quoted(x): return t.App(t.Var('quote'), walk(x, c))
    raise ElaborationError(f'unsupported surface form {v!r}')


def context_of(program):
    c = Context()
    # Reserve source names as well as generated names to avoid capturing a free name.
    from dataclasses import fields, is_dataclass
    def reserve(v):
        if isinstance(v, str): c.used.add(v)
        elif isinstance(v, tuple):
            for x in v: reserve(x)
        elif is_dataclass(v):
            for f in fields(v): reserve(getattr(v, f.name))
    reserve(program)
    for act in program:
        if isinstance(act, s.Alias): c.aliases[act.name] = act
        if isinstance(act, (s.Declare, s.Define)):
            c.signatures[act.name] = act.binders
            if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
                c.constructors.update(n for n, _ in act.body.constructors)
    for act in program:
        if isinstance(act, (s.Declare, s.Define)):
            inner = c.child(); ps = parameters(act.binders, inner)
            annotation = walk(act.type, inner) if act.type is not None else t.Hole('type')
            if act.type is not None or act.name not in c.types:
                c.types[act.name] = curry(t.Pi, ps, annotation)
            if isinstance(act, s.Define) and isinstance(act.body, s.DataBody):
                inner.types[act.name] = c.types[act.name]
                for n, ty in act.body.constructors: c.types[n] = walk(ty, inner)
    for act in program:
        if isinstance(act, s.OperatorAct):
            target = walk(act.value, c); ty = infer(target, c)
            if not isinstance(ty, t.Pi): raise ElaborationError('operator needs a declared function type')
            c.operators[(act.operator, ty.domain)] = target
    return c


def elaborate_term(surface: s.Surface, context: s.SurfaceProgram | Context) -> t.Term:
    """Elaborate in a surface program (or an internal Context); see typing limits above.

    Raises ElaborationError for unsupported/inferentially unresolved cases, rather
    than returning the theory's Maybe. It does not certify well-typedness.
    """
    return walk(surface, context if isinstance(context, Context) else context_of(context))


def elaborate_program(surface_program: s.SurfaceProgram) -> t.Program:
    c = context_of(surface_program); result = []
    for act in surface_program:
        if isinstance(act, (s.Declare, s.Define)):
            inner = c.child(); ps = parameters(act.binders, inner)
            annotation = c.types[act.name]
            if isinstance(act, s.Declare): result.append(t.Declare(act.name, annotation)); continue
            expected = annotation
            for _ in ps:
                if isinstance(expected, t.Pi): expected = expected.codomain
            # A separate base declaration admits a predicate body (4.R6).
            if (act.type is None and isinstance(act.body, s.TermBody)
                    and isinstance(act.body.term, s.Lambda)
                    and not isinstance(expected, (t.Pi, t.Hole))):
                expected = t.Pi('_', expected, t.Var('Bool'))
            match act.body:
                case s.TermBody(v): body = walk(v, inner, expected)
                case s.DataBody(xs): body = t.Data(act.name, tuple((n, walk(x, inner)) for n, x in xs))
                case s.ClausesBody(clauses):
                    arms = []
                    for clause in clauses:
                        local = inner.child(); pats = [pattern(p, local) for p in clause.patterns]
                        arms.append((pairs(pats, t.PPair), walk(clause.body, local)))
                    body = t.Match(pairs([t.Var(n) for n, _ in ps]), tuple(arms))
            body = curry(t.Lam, ps, body)
            if act.type is None:
                inferred = infer(body, c)
                # A theory's declaration supplies its record, while its body
                # supplies the laws (4.R6, 4.S9).
                declared = expected
                if not isinstance(declared, t.Record):
                    annotation = inferred
                c.types[act.name] = annotation
            result.append(t.Define(act.name, annotation, body))
        elif isinstance(act, s.Datum): result.append(t.Datum(walk(act.value, c)))
    return tuple(result)


def show_term(v):
    """Readable surface-style rendering; no promise of parser round-tripping."""
    match v:
        case t.Var(n) | t.Primitive(n): return n
        case t.Lit(k): return json.dumps(k.value, ensure_ascii=False)
        case t.Universe(): return 'U'
        case t.World(): return 'W'
        case t.App(f, a): return f'({show_term(f)} {show_term(a)})'
        case t.Lam(n, a, b): return f'fn ({n} : {show_term(a)}) {{ {show_term(b)} }}'
        case t.Pi(n, a, b): return f'({n} : {show_term(a)}) -> {show_term(b)}'
        case t.Sigma(n, a, b): return f'({n} : {show_term(a)}) * {show_term(b)}'
        case t.Pair(a, b): return f'({show_term(a)}, {show_term(b)})'
        case t.Record(fs) | t.RecordValue(fs):
            sep = ' : ' if isinstance(v, t.Record) else ' := '
            return '{ ' + ', '.join(n + sep + show_term(x) for n, x in fs) + ' }'
        case t.Proj(r, n): return f'({show_term(r)}).{n}'
        case t.Let(n, _, x, b): return f'{{ {n} := {show_term(x)}; {show_term(b)} }}'
        case t.Sum(xs): return '{ ' + ' || '.join(n + ' : ' + show_term(x) for n, x in xs) + ' }'
        case t.Data(_, xs): return 'data { ' + '; '.join(n + ' : ' + show_term(x) for n, x in xs) + ' }'
        case t.Match(x, arms): return 'match ' + show_term(x) + ' { ' + '; '.join(show_pattern(p) + ' -> ' + show_term(b) for p, b in arms) + ' }'
        case t.Inj(n, x): return f'{n} {show_term(x)}'
        case t.Hole(n): return '?' + n
        case t.Extern(n): return 'extern ' + json.dumps(n)
        case t.Axiom(n): return 'axiom ' + json.dumps(n)
        case t.Subtype(n, a, p): return f'{{ {n} : {show_term(a)} | {show_term(p)} }}'
    raise TypeError(v)


def show_pattern(p):
    match p:
        case t.PVar(n): return n
        case t.PWild(): return '_'
        case t.PLit(k): return json.dumps(k.value)
        case t.PCon(n, ps): return n + ''.join(' (' + show_pattern(x) + ')' for x in ps)
        case t.PPair(a, b): return f'({show_pattern(a)}, {show_pattern(b)})'
        case t.PInj(n, x): return n + ' ' + show_pattern(x)
    raise TypeError(p)
