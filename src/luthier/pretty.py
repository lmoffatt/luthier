"""Pretty printer for terms and patterns."""
from __future__ import annotations
from .syntax import *


def pp_pat(p) -> str:
    if isinstance(p, PVar):
        return p.name
    if isinstance(p, PWild):
        return "_"
    if isinstance(p, PLit):
        return repr(p.value) if isinstance(p.value, str) else str(p.value)
    if isinstance(p, PCon):
        if not p.args:
            return p.name
        return p.name + " " + " ".join(_pat_atom(a) for a in p.args)
    if isinstance(p, PPair):
        items = []
        while isinstance(p, PPair):
            items.append(p.fst)
            p = p.snd
        items.append(p)
        return "(" + ", ".join(pp_pat(x) for x in items) + ")"
    return str(p)


def _pat_atom(p) -> str:
    s = pp_pat(p)
    return f"({s})" if isinstance(p, PCon) and p.args else s


def _projected_name(p):
    """The one variable of a tuple pattern whose other components are wildcards, or None."""
    if not isinstance(p, PPair):
        return None
    names = []
    def walk(q):
        if isinstance(q, PVar):
            names.append(q.name)
            return True
        if isinstance(q, PWild):
            return True
        if isinstance(q, PPair):
            return walk(q.fst) and walk(q.snd)
        return False
    if not walk(p) or len(names) != 1:
        return None
    return names[0]


PREC = {"&": 0, "->": 1, "or": 2, "and": 3, "==": 4, "/=": 4, "<": 4, "<=": 4, ">": 4, ">=": 4,
        "+": 5, "-": 5, "*": 6, "/": 6, "mod": 6}
APP = 7
RIGHT = {"&", "->"}


def _infix(op, lhs, rhs, prec) -> str:
    lv = PREC[op]
    ls = pp(lhs, lv if op in RIGHT else lv + 1) if op not in RIGHT else pp(lhs, lv + 1)
    rs = pp(rhs, lv if op in RIGHT else lv + 1)
    s = f"{ls} {op} {rs}"
    return f"({s})" if prec > lv else s


def pp(t, prec: int = 0) -> str:
    """prec: the binding power of the context; parenthesize when the term binds looser."""
    if isinstance(t, Var):
        return t.name
    if isinstance(t, Con):
        return t.name
    if isinstance(t, Lit):
        v = t.value
        if isinstance(v, str):
            return repr(v)
        if isinstance(v, (int, float)):
            return str(v)
        shape = getattr(v, "shape", None)
        return f"<{type(v).__name__}{' ' + str(shape) if shape is not None else ''}>"
    if isinstance(t, Univ):
        return "U"
    if isinstance(t, Extern):
        return f'extern "{t.target}"'
    if isinstance(t, Lam):
        params = []
        while isinstance(t, Lam):
            params.append(pp_pat(t.param))
            t = t.body
        return "\\ " + " ".join(params) + " { " + pp(t) + " }"
    if isinstance(t, App):
        if isinstance(t.fn, App) and isinstance(t.fn.fn, Var) and t.fn.fn.name in ("and", "or", "implies"):
            op = {"and": "and", "or": "or", "implies": "->"}[t.fn.fn.name]
            return _infix(op, t.fn.arg, t.arg, prec)
        s = pp(t.fn, APP) + " " + pp(t.arg, APP + 1)
        return f"({s})" if prec > APP else s
    if isinstance(t, Pi):
        if t.name == "_":
            return _infix("->", t.dom, t.cod, prec)
        s = f"({t.name} : {pp(t.dom)}) -> " + pp(t.cod, PREC["->"])
        return f"({s})" if prec > PREC["->"] else s
    if isinstance(t, Sigma):
        if t.name == "_":
            return _infix("*", t.fst, t.snd, prec)
        s = f"({t.name} : {pp(t.fst)}) * " + pp(t.snd, PREC["*"])
        return f"({s})" if prec > PREC["*"] else s
    if isinstance(t, Pair):
        items = []
        while isinstance(t, Pair):
            items.append(t.fst)
            t = t.snd
        items.append(t)
        return "(" + ", ".join(pp(x) for x in items) + ")"
    if isinstance(t, Arrow):
        return _infix("->", t.lhs, t.rhs, prec)
    if isinstance(t, BinOp):
        return _infix(t.op, t.lhs, t.rhs, prec)
    if isinstance(t, And):
        return _infix("&", t.lhs, t.rhs, prec)
    if isinstance(t, Forget):
        s = "forget " + pp(t.arg, APP + 1)
        return f"({s})" if prec > APP else s
    if isinstance(t, RecordLit):
        return "{ " + ", ".join(f"{n} := {pp(v)}" for n, v in t.fields) + " }"
    if isinstance(t, Subtype):
        return "{ " + pp_pat(t.param) + " : " + pp(t.base) + " | " + pp(t.pred) + " }"
    if isinstance(t, Proj):
        return pp(t.term, APP + 1) + "." + t.field
    if isinstance(t, Match) and len(t.branches) == 1:
        pat, body = t.branches[0]
        name = _projected_name(pat)
        if name is not None and isinstance(body, Var) and body.name == name:
            return pp(t.scrut, APP + 1) + "." + name.split("~")[0]
    if isinstance(t, Match):
        br = " ; ".join(pp_pat(p) + " -> " + pp(b) for p, b in t.branches)
        s = "match " + pp(t.scrut, APP) + " { " + br + " }"
        return f"({s})" if prec > APP else s
    return repr(t)
