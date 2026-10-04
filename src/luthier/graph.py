"""The dependency graph of a file and its objects (05 §2, §3).

A file is read whole before anything is checked. Its entries are grouped by name (a
declaration and a later definition of the same name are one node), the names each node
mentions give the edges, and the strongly connected components of that graph are the objects,
returned so that every dependency comes before what depends on it. Order in the file does not
matter.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from .syntax import *


@dataclass
class Member:
    kind: str                       # "entry", "alias" or "operator"
    name: str
    line: int = 0
    decl: Optional[Def] = None      # the declaration: a type and no body (or the definition, if it has both)
    defn: Optional[Def] = None      # the definition: a body, a data, or an extern
    alias: Optional[Def] = None
    pending: bool = False           # a declared type whose laws define it later in the same object
    refs: set = field(default_factory=set)
    base_ctx: list = field(default_factory=list)
    base: Optional[Term] = None


@dataclass
class Obj:
    members: list


class GraphError(Exception):
    pass


def file_objects(checker, prog: Program) -> list:
    members: dict = {}
    order = []

    def entry(name, line):
        m = members.get(name)
        if m is None:
            m = Member("entry", name, line)
            members[name] = m
            order.append(name)
        return m

    for i, d in enumerate(prog.defs):
        if isinstance(d, OperatorDirective):
            key = f"operator {d.op}#{i}"
            members[key] = Member("operator", key, d.line, defn=d)
            order.append(key)
            continue
        m = entry(d.name, d.line)
        if d.alias:
            if m.alias is not None:
                checker.err(f"{d.name} is an alias and cannot be defined twice")
            m.alias = d
            m.kind = "alias"
            continue
        has_body = d.body is not None or d.data is not None
        if has_body:
            if m.defn is not None:
                checker.current_def = checker.qualify(d.name)
                try:
                    checker.err(f"{d.name} is defined twice")
                finally:
                    checker.current_def = None
            m.defn = d
            if d.type is not None and m.decl is None:
                m.decl = d
        else:
            if m.decl is not None and m.decl.body is None and m.decl is not m.defn:
                checker.current_def = checker.qualify(d.name)
                try:
                    checker.err(f"{d.name} is declared twice")
                finally:
                    checker.current_def = None
            if m.decl is None or m.decl is m.defn:
                m.decl = d if m.decl is None else m.decl
                if m.decl is not d:
                    # a declaration after a definition that carried its own type: keep the declaration
                    m.decl = d
    # an alias name that is also declared or defined is reported when the alias is checked
    local = set(members)
    constructors = {}
    labels = {}
    for name, m in members.items():
        if m.defn is not None and getattr(m.defn, "data", None) is not None:
            for c in m.defn.data.constructors:
                constructors[c.name] = name
        if m.alias is not None:
            b = m.alias.body
            while isinstance(b, Lam):
                b = b.body
            if isinstance(b, Sum):
                for l, _ in b.alts:
                    labels.setdefault(l, name)
    ops = {}
    for name, m in members.items():
        if m.kind == "operator":
            ops.setdefault(m.defn.op, []).append(name)

    def resolve(n: str, bound: set) -> Optional[str]:
        if n in bound:
            return None
        if n in local:
            return n
        if n in constructors:
            return constructors[n]
        if n in labels:
            return labels[n]
        if "." in n:
            first = n.split(".")[0]
            if first in bound:
                return None
            if first in local:
                return first
        return None

    for name, m in members.items():
        terms = []
        if m.kind == "operator":
            terms.append(m.defn.term)
        if m.alias is not None:
            terms.append(m.alias.body)
        for d in (m.decl, m.defn):
            if d is None or isinstance(d, OperatorDirective):
                continue
            if d.type is not None:
                terms.append(d.type)
            if d.body is not None:
                terms.append(d.body)
            if d.data is not None:
                for _, t in d.data.params:
                    terms.append(t)
                for c in d.data.constructors:
                    terms.append(c.type)
        refs = set()
        for t in terms:
            _refs(t, set(), resolve, refs, ops)
        if m.defn is not None and getattr(m.defn, "data", None) is not None:
            refs.discard(name)  # a data type refers to itself through its constructors
            if _mentions(m.defn, name):
                refs.add(name)
        m.refs = refs

    # names used as types anywhere in the file: a declared name over a base that is used as a type
    # is a declared type (05 §1), defined later by its laws or never (then only declared)
    def param_is_type(fname: str, i: int) -> bool:
        t = None
        m = members.get(fname)
        if m is not None and m.decl is not None and m.decl.type is not None:
            t = m.decl.type
        elif m is not None and m.alias is not None:
            b = m.alias.body
            for _ in range(i):
                if not isinstance(b, Lam):
                    return False
                b = b.body
            return isinstance(b, Lam) and isinstance(b.ann, Univ)
        else:
            q = checker.resolve(fname)
            d = checker.env.defs.get(q) if q is not None else None
            if d is not None:
                t = d.type
        for _ in range(i):
            if not isinstance(t, Pi):
                return False
            t = t.cod
        return isinstance(t, Pi) and isinstance(t.dom, Univ)

    heads = set()
    for d in prog.defs:
        if isinstance(d, OperatorDirective):
            continue
        if d.type is not None:
            _type_heads(d.type, heads, param_is_type)
        if d.body is not None:
            _annotation_heads(d.body, heads, param_is_type)
        if d.data is not None:
            for c in d.data.constructors:
                _type_heads(c.type, heads, param_is_type)
    for name, m in members.items():
        if m.kind == "entry" and m.decl is not None and m.decl is not m.defn and m.decl.type is not None \
                and not _ends_in_universe(m.decl.type) and name in heads:
            m.pending = True

    comps = _tarjan(order, {n: members[n].refs for n in order})
    objs = []
    for comp in comps:
        ms = sorted((members[n] for n in comp), key=lambda m: m.line)
        objs.append(Obj(ms))
    return objs


def _ends_in_universe(t: Term) -> bool:
    while isinstance(t, Pi):
        t = t.cod
    return isinstance(t, Univ)


def _mentions(d: Def, name: str) -> bool:
    for c in d.data.constructors:
        if name in _plain_names(c.type):
            return True
    return False


def _plain_names(t: Term) -> set:
    out = set()
    _refs(t, set(), lambda n, b: n if n not in b else None, out, {})
    return out


def _refs(t: Term, bound: set, resolve, out: set, ops: dict):
    if t is None:
        return
    if isinstance(t, Var):
        r = resolve(t.name, bound)
        if r is not None:
            out.add(r)
        return
    if isinstance(t, (Lit, Univ, Con, Extern, NoLaw)):
        return
    if isinstance(t, Lam):
        if t.ann is not None:
            _refs(t.ann, bound, resolve, out, ops)
        _refs(t.body, bound | set(pattern_vars(t.param)), resolve, out, ops)
        _pattern_refs(t.param, bound, resolve, out)
        return
    if isinstance(t, Pi):
        _refs(t.dom, bound, resolve, out, ops)
        _refs(t.cod, bound | {t.name}, resolve, out, ops)
        return
    if isinstance(t, Sigma):
        _refs(t.fst, bound, resolve, out, ops)
        _refs(t.snd, bound | {t.name}, resolve, out, ops)
        return
    if isinstance(t, Subtype):
        _refs(t.base, bound, resolve, out, ops)
        names = set(pattern_vars(t.param))
        # in a labeled base `{ n : Int, m : { k : Int | k <= n } }`, later types see earlier names
        _refs(t.pred, bound | names, resolve, out, ops)
        return
    if isinstance(t, Match):
        _refs(t.scrut, bound, resolve, out, ops)
        for p, b in t.branches:
            _pattern_refs(p, bound, resolve, out)
            _refs(b, bound | set(pattern_vars(p)), resolve, out, ops)
        return
    if isinstance(t, BinOp):
        for o in ops.get(t.op, ()):
            out.add(o)
        _refs(t.lhs, bound, resolve, out, ops)
        _refs(t.rhs, bound, resolve, out, ops)
        return
    if isinstance(t, (Arrow, And)):
        _refs(t.lhs, bound, resolve, out, ops)
        _refs(t.rhs, bound, resolve, out, ops)
        return
    if isinstance(t, App):
        _refs(t.fn, bound, resolve, out, ops)
        _refs(t.arg, bound, resolve, out, ops)
        return
    if isinstance(t, Pair):
        _refs(t.fst, bound, resolve, out, ops)
        _refs(t.snd, bound, resolve, out, ops)
        return
    if isinstance(t, Forget):
        _refs(t.arg, bound, resolve, out, ops)
        return
    if isinstance(t, RecordLit):
        for _, v in t.fields:
            _refs(v, bound, resolve, out, ops)
        return
    if isinstance(t, Proj):
        _refs(t.term, bound, resolve, out, ops)
        return
    if isinstance(t, Sum):
        for _, a in t.alts:
            _refs(a, bound, resolve, out, ops)
        return
    if isinstance(t, Named):
        _refs(t.type, bound, resolve, out, ops)
        return
    if isinstance(t, Inj):
        _refs(t.arg, bound, resolve, out, ops)
        return


def _pattern_refs(p: Pattern, bound: set, resolve, out: set):
    """A constructor or label in a pattern refers to its type."""
    if isinstance(p, PCon):
        r = resolve(p.name, bound)
        if r is not None:
            out.add(r)
        for a in p.args:
            _pattern_refs(a, bound, resolve, out)
    elif isinstance(p, PPair):
        _pattern_refs(p.fst, bound, resolve, out)
        _pattern_refs(p.snd, bound, resolve, out)
    elif isinstance(p, PVar):
        # a bare name in a pattern may be a constructor or a label of a local type
        pass


def _type_heads(t: Term, out: set, param_is_type):
    """Names used as types in a type expression: the heads, and the arguments a type operator
    takes as types (`List Codec`), not those it takes as values (`VecOf n`)."""
    if isinstance(t, Var):
        out.add(t.name)
    elif isinstance(t, App):
        h, args = _unapply(t)
        if isinstance(h, Var):
            out.add(h.name)
            for i, a in enumerate(args):
                if param_is_type(h.name, i):
                    _type_heads(a, out, param_is_type)
        else:
            _type_heads(h, out, param_is_type)
    elif isinstance(t, Pi):
        _type_heads(t.dom, out, param_is_type)
        _type_heads(t.cod, out, param_is_type)
    elif isinstance(t, Sigma):
        _type_heads(t.fst, out, param_is_type)
        _type_heads(t.snd, out, param_is_type)
    elif isinstance(t, (Arrow, BinOp)):
        _type_heads(t.lhs, out, param_is_type)
        _type_heads(t.rhs, out, param_is_type)
    elif isinstance(t, Sum):
        for _, a in t.alts:
            _type_heads(a, out, param_is_type)
    elif isinstance(t, Subtype):
        _type_heads(t.base, out, param_is_type)
    elif isinstance(t, Named):
        _type_heads(t.type, out, param_is_type)


def _unapply(t):
    args = []
    while isinstance(t, App):
        args.append(t.arg)
        t = t.fn
    return t, list(reversed(args))


def _annotation_heads(t: Term, out: set, param_is_type):
    """Types written inside a body: binder annotations and subtype bases."""
    if isinstance(t, Lam):
        if t.ann is not None:
            _type_heads(t.ann, out, param_is_type)
        _annotation_heads(t.body, out, param_is_type)
    elif isinstance(t, Subtype):
        _type_heads(t.base, out, param_is_type)
    elif isinstance(t, App):
        _annotation_heads(t.fn, out, param_is_type)
        _annotation_heads(t.arg, out, param_is_type)
    elif isinstance(t, Match):
        _annotation_heads(t.scrut, out, param_is_type)
        for _, b in t.branches:
            _annotation_heads(b, out, param_is_type)
    elif isinstance(t, (BinOp, And, Arrow)):
        _annotation_heads(t.lhs, out, param_is_type)
        _annotation_heads(t.rhs, out, param_is_type)
    elif isinstance(t, Pair):
        _annotation_heads(t.fst, out, param_is_type)
        _annotation_heads(t.snd, out, param_is_type)


def _tarjan(nodes: list, edges: dict) -> list:
    """Strongly connected components, each emitted after every component it depends on."""
    index = {}
    low = {}
    stack = []
    on = set()
    out = []
    counter = [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in sorted(edges.get(v, ())):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(comp)

    for v in nodes:
        if v not in index:
            visit(v)
    return out
