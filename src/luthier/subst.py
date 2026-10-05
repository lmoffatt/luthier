"""Substitution with capture avoidance, and free variables."""
from __future__ import annotations
import itertools
from .syntax import *

_counter = itertools.count(1)


def fresh(base: str) -> str:
    base = base.split("~")[0]
    return f"{base}~{next(_counter)}"


def free_vars(t: Term) -> set[str]:
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, (Lit, Univ, Con, Extern, NoLaw, Primitive, Axiom)):
        return set()
    if isinstance(t, Sum):
        out = set()
        for _, a in t.alts:
            out |= free_vars(a)
        return out
    if isinstance(t, Inj):
        return free_vars(t.arg) | (free_vars(t.type) if t.type is not None else set())
    if isinstance(t, Named):
        return free_vars(t.type)
    if isinstance(t, Lam):
        fv = free_vars(t.body) - set(pattern_vars(t.param))
        if t.res is not None:
            fv |= free_vars(t.res) - set(pattern_vars(t.param))
        if t.ann is not None:
            fv |= free_vars(t.ann)
        return fv
    if isinstance(t, App):
        return free_vars(t.fn) | free_vars(t.arg)
    if isinstance(t, Pi):
        return free_vars(t.dom) | (free_vars(t.cod) - {t.name})
    if isinstance(t, Sigma):
        return free_vars(t.fst) | (free_vars(t.snd) - {t.name})
    if isinstance(t, Pair):
        return free_vars(t.fst) | free_vars(t.snd)
    if isinstance(t, (Arrow, BinOp, And)):
        return free_vars(t.lhs) | free_vars(t.rhs)
    if isinstance(t, Forget):
        return free_vars(t.arg)
    if isinstance(t, RecordLit):
        out = set()
        for _, v in t.fields:
            out |= free_vars(v)
        return out
    if isinstance(t, Proj):
        return free_vars(t.term)
    if isinstance(t, Subtype):
        return free_vars(t.base) | (free_vars(t.pred) - set(pattern_vars(t.param)))
    if isinstance(t, Match):
        fv = free_vars(t.scrut)
        for p, b in t.branches:
            fv |= free_vars(b) - set(pattern_vars(p))
        return fv
    raise TypeError(f"free_vars: unknown term {t!r}")


def rename_pattern(p: Pattern, mapping: dict) -> Pattern:
    if isinstance(p, PVar):
        return PVar(mapping.get(p.name, p.name))
    if isinstance(p, PCon):
        return PCon(p.name, tuple(rename_pattern(a, mapping) for a in p.args))
    if isinstance(p, PPair):
        return PPair(rename_pattern(p.fst, mapping), rename_pattern(p.snd, mapping))
    if isinstance(p, PInj):
        return PInj(p.index, p.label, rename_pattern(p.arg, mapping))
    return p


def subst(t: Term, mapping: dict[str, Term]) -> Term:
    """Simultaneous substitution of free variables, renaming binders when needed."""
    if not mapping:
        return t
    if isinstance(t, Var):
        return mapping.get(t.name, t)
    if isinstance(t, (Lit, Univ, Con, Extern, NoLaw, Primitive, Axiom)):
        return t
    if isinstance(t, Sum):
        return Sum(tuple((l, subst(a, mapping)) for l, a in t.alts))
    if isinstance(t, Inj):
        return Inj(t.index, t.label, subst(t.arg, mapping), subst(t.type, mapping) if t.type is not None else None)
    if isinstance(t, Named):
        return Named(t.name, subst(t.type, mapping))
    if isinstance(t, App):
        return App(subst(t.fn, mapping), subst(t.arg, mapping))
    if isinstance(t, Pair):
        return Pair(subst(t.fst, mapping), subst(t.snd, mapping))
    if isinstance(t, Arrow):
        return Arrow(subst(t.lhs, mapping), subst(t.rhs, mapping))
    if isinstance(t, BinOp):
        return BinOp(t.op, subst(t.lhs, mapping), subst(t.rhs, mapping))
    if isinstance(t, And):
        return And(subst(t.lhs, mapping), subst(t.rhs, mapping))
    if isinstance(t, Forget):
        return Forget(subst(t.arg, mapping))
    if isinstance(t, RecordLit):
        return RecordLit(tuple((n, subst(v, mapping)) for n, v in t.fields))
    if isinstance(t, Proj):
        return Proj(subst(t.term, mapping), t.field)
    if isinstance(t, Lam):
        ann = subst(t.ann, mapping) if t.ann is not None else None
        if t.res is not None:
            p, both = _under_binder(t.param, Pair(t.body, t.res), mapping)
            return Lam(p, both.fst, ann, both.snd)
        p, body = _under_binder(t.param, t.body, mapping)
        return Lam(p, body, ann)
    if isinstance(t, Pi):
        dom = subst(t.dom, mapping)
        p, cod = _under_binder(PVar(t.name), t.cod, mapping)
        return Pi(p.name, dom, cod)
    if isinstance(t, Sigma):
        fst = subst(t.fst, mapping)
        p, snd = _under_binder(PVar(t.name), t.snd, mapping)
        return Sigma(p.name, fst, snd)
    if isinstance(t, Subtype):
        base = subst(t.base, mapping)
        p, pred = _under_binder(t.param, t.pred, mapping)
        return Subtype(p, base, pred)
    if isinstance(t, Match):
        scrut = subst(t.scrut, mapping)
        brs = []
        for p, b in t.branches:
            p2, b2 = _under_binder(p, b, mapping)
            brs.append((p2, b2))
        return Match(scrut, tuple(brs))
    raise TypeError(f"subst: unknown term {t!r}")


def _under_binder(p: Pattern, body: Term, mapping: dict):
    bound = set(pattern_vars(p))
    m = {k: v for k, v in mapping.items() if k not in bound}
    if not m:
        return p, body
    fv_repl = set()
    for v in m.values():
        fv_repl |= free_vars(v)
    clash = bound & fv_repl
    if clash:
        ren = {x: fresh(x) for x in clash}
        p = rename_pattern(p, ren)
        body = subst(body, {x: Var(y) for x, y in ren.items()})
    return p, subst(body, m)


def map_pattern_names(p: Pattern, f) -> Pattern:
    if isinstance(p, PCon):
        return PCon(f(p.name), tuple(map_pattern_names(a, f) for a in p.args))
    if isinstance(p, PPair):
        return PPair(map_pattern_names(p.fst, f), map_pattern_names(p.snd, f))
    if isinstance(p, PInj):
        return PInj(p.index, p.label, map_pattern_names(p.arg, f))
    return p


def map_names(t: Term, f) -> Term:
    """Apply `f` to every global name (Var, Con, constructor in patterns). Bound variables never
    carry module prefixes, so renaming them too is harmless."""
    if isinstance(t, Var):
        return Var(f(t.name))
    if isinstance(t, Con):
        return Con(f(t.name))
    if isinstance(t, (Lit, Univ, Extern, NoLaw, Primitive, Axiom)):
        return t
    if isinstance(t, Sum):
        return Sum(tuple((l, map_names(a, f)) for l, a in t.alts))
    if isinstance(t, Inj):
        return Inj(t.index, t.label, map_names(t.arg, f), map_names(t.type, f) if t.type is not None else None)
    if isinstance(t, Named):
        return Named(t.name, map_names(t.type, f))
    if isinstance(t, App):
        return App(map_names(t.fn, f), map_names(t.arg, f))
    if isinstance(t, Pair):
        return Pair(map_names(t.fst, f), map_names(t.snd, f))
    if isinstance(t, Arrow):
        return Arrow(map_names(t.lhs, f), map_names(t.rhs, f))
    if isinstance(t, BinOp):
        return BinOp(t.op, map_names(t.lhs, f), map_names(t.rhs, f))
    if isinstance(t, And):
        return And(map_names(t.lhs, f), map_names(t.rhs, f))
    if isinstance(t, Forget):
        return Forget(map_names(t.arg, f))
    if isinstance(t, RecordLit):
        return RecordLit(tuple((n, map_names(v, f)) for n, v in t.fields))
    if isinstance(t, Proj):
        return Proj(map_names(t.term, f), t.field)
    if isinstance(t, Lam):
        return Lam(map_pattern_names(t.param, f), map_names(t.body, f),
                   map_names(t.ann, f) if t.ann is not None else None,
                   map_names(t.res, f) if t.res is not None else None)
    if isinstance(t, Pi):
        return Pi(t.name, map_names(t.dom, f), map_names(t.cod, f))
    if isinstance(t, Sigma):
        return Sigma(t.name, map_names(t.fst, f), map_names(t.snd, f))
    if isinstance(t, Subtype):
        return Subtype(map_pattern_names(t.param, f), map_names(t.base, f), map_names(t.pred, f))
    if isinstance(t, Match):
        return Match(map_names(t.scrut, f),
                     tuple((map_pattern_names(q, f), map_names(b, f)) for q, b in t.branches))
    raise TypeError(f"map_names: unknown term {t!r}")


def alpha_normalize(t: Term) -> Term:
    """Rename every bound variable to _0, _1, ... in traversal order, so two alpha-equivalent
    terms print identically (used for certificate hashes)."""
    counter = [0]

    def fresh_name():
        n = f"_{counter[0]}"
        counter[0] += 1
        return n

    def go_pat(p: Pattern, env: dict) -> Pattern:
        if isinstance(p, PVar):
            new = fresh_name()
            env[p.name] = new
            return PVar(new)
        if isinstance(p, PCon):
            return PCon(p.name, tuple(go_pat(a, env) for a in p.args))
        if isinstance(p, PPair):
            return PPair(go_pat(p.fst, env), go_pat(p.snd, env))
        if isinstance(p, PInj):
            return PInj(p.index, p.label, go_pat(p.arg, env))
        return p

    def go(t: Term, env: dict) -> Term:
        if isinstance(t, Var):
            return Var(env.get(t.name, t.name))
        if isinstance(t, (Lit, Univ, Con, Extern, NoLaw, Primitive, Axiom)):
            return t
        if isinstance(t, Sum):
            return Sum(tuple((l, go(a, env)) for l, a in t.alts))
        if isinstance(t, Inj):
            # the label is a name of the position, not part of the value: hash by index
            return Inj(t.index, "", go(t.arg, env), None)
        if isinstance(t, Named):
            return Named(t.name, go(t.type, env))
        if isinstance(t, App):
            return App(go(t.fn, env), go(t.arg, env))
        if isinstance(t, Pair):
            return Pair(go(t.fst, env), go(t.snd, env))
        if isinstance(t, Arrow):
            return Arrow(go(t.lhs, env), go(t.rhs, env))
        if isinstance(t, BinOp):
            return BinOp(t.op, go(t.lhs, env), go(t.rhs, env))
        if isinstance(t, And):
            return And(go(t.lhs, env), go(t.rhs, env))
        if isinstance(t, Forget):
            return Forget(go(t.arg, env))
        if isinstance(t, RecordLit):
            return RecordLit(tuple((n, go(v, env)) for n, v in t.fields))
        if isinstance(t, Proj):
            return Proj(go(t.term, env), t.field)
        if isinstance(t, Lam):
            ann = go(t.ann, env) if t.ann is not None else None
            env2 = dict(env)
            p = go_pat(t.param, env2)
            return Lam(p, go(t.body, env2), ann, go(t.res, env2) if t.res is not None else None)
        if isinstance(t, Pi):
            dom = go(t.dom, env)
            env2 = dict(env)
            name = t.name if t.name == "_" else fresh_name()
            if t.name != "_":
                env2[t.name] = name
            return Pi(name, dom, go(t.cod, env2))
        if isinstance(t, Sigma):
            fst = go(t.fst, env)
            env2 = dict(env)
            name = t.name if t.name == "_" else fresh_name()
            if t.name != "_":
                env2[t.name] = name
            return Sigma(name, fst, go(t.snd, env2))
        if isinstance(t, Subtype):
            base = go(t.base, env)
            env2 = dict(env)
            p = go_pat(t.param, env2)
            return Subtype(p, base, go(t.pred, env2))
        if isinstance(t, Match):
            brs = []
            for q, b in t.branches:
                env2 = dict(env)
                q2 = go_pat(q, env2)
                brs.append((q2, go(b, env2)))
            return Match(go(t.scrut, env), tuple(brs))
        raise TypeError(f"alpha_normalize: unknown term {t!r}")

    return go(t, {})
