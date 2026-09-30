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
    if isinstance(t, (Lit, Univ, Con, Extern)):
        return set()
    if isinstance(t, Lam):
        fv = free_vars(t.body) - set(pattern_vars(t.param))
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
    return p


def subst(t: Term, mapping: dict[str, Term]) -> Term:
    """Simultaneous substitution of free variables, renaming binders when needed."""
    if not mapping:
        return t
    if isinstance(t, Var):
        return mapping.get(t.name, t)
    if isinstance(t, (Lit, Univ, Con, Extern)):
        return t
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
    if isinstance(t, Lam):
        ann = subst(t.ann, mapping) if t.ann is not None else None
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
    return p


def map_names(t: Term, f) -> Term:
    """Apply `f` to every global name (Var, Con, constructor in patterns). Bound variables never
    carry module prefixes, so renaming them too is harmless."""
    if isinstance(t, Var):
        return Var(f(t.name))
    if isinstance(t, Con):
        return Con(f(t.name))
    if isinstance(t, (Lit, Univ, Extern)):
        return t
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
    if isinstance(t, Lam):
        return Lam(map_pattern_names(t.param, f), map_names(t.body, f),
                   map_names(t.ann, f) if t.ann is not None else None)
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
