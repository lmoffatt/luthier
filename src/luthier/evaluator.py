"""Reduction: weak-head normal form, full normal form, and conversion.

Rules: beta (application of a lambda), delta (unfolding a global definition),
iota (match on a constructor), prim (arithmetic and comparison on literals),
extern (calling the environment on saturated, closed arguments).

A global is unfolded in head position only if that makes progress; a recursive
function applied to a neutral argument stays folded, so normalizing under
binders terminates.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Callable
from .syntax import *
from .subst import subst, fresh, free_vars
from .pretty import pp


class EvalError(Exception):
    pass


class OutOfFuel(EvalError):
    pass


BUILTIN_TYPES = ("Int", "R", "String", "Law")


@dataclass
class ExternInfo:
    fn: Callable
    arity: int
    type: Term


@dataclass
class Env:
    defs: dict = field(default_factory=dict)        # name -> Def (elaborated)
    datas: dict = field(default_factory=dict)       # name -> DataDecl (elaborated)
    cons: dict = field(default_factory=dict)        # constructor name -> (data name, full type)
    externs: dict = field(default_factory=dict)     # target -> ExternInfo
    fuel: int = 200_000

    def is_global(self, name: str) -> bool:
        return name in self.defs or name in self.datas or name in BUILTIN_TYPES


# ------------------------------------------------------------------ helpers

def unapply(t: Term):
    args = []
    while isinstance(t, App):
        args.append(t.arg)
        t = t.fn
    args.reverse()
    return t, args


def apply(head: Term, args) -> Term:
    for a in args:
        head = App(head, a)
    return head


def is_con_value(t: Term) -> bool:
    h, _ = unapply(t)
    return isinstance(h, Con)


def bool_con(b: bool) -> Term:
    return Con("true") if b else Con("false")


def as_bool(t: Term) -> Optional[bool]:
    if isinstance(t, Con) and t.name == "true":
        return True
    if isinstance(t, Con) and t.name == "false":
        return False
    return None


# ----------------------------------------------------------- pattern match

class NoMatch(Exception):
    """The value is a different constructor, literal or shape: this branch is out."""


class Stuck(Exception):
    """The value is neutral (a free variable, a hole, a stuck application): cannot decide."""


def is_value(t: Term) -> bool:
    return is_con_value(t) or isinstance(t, (Lit, Pair, Lam, Pi, Sigma, Univ, Subtype))


def match_pattern(env: Env, p: Pattern, v: Term, fuel, unfold: bool = True) -> dict:
    """Bindings if whnf(v) matches p; raises NoMatch on a definite mismatch, Stuck on a neutral value."""
    if isinstance(p, PWild):
        return {}
    if isinstance(p, PVar):
        return {p.name: v}
    v = whnf(env, v, fuel, unfold)
    if isinstance(p, PLit):
        if isinstance(v, Lit):
            if v.value == p.value:
                return {}
            raise NoMatch()
        raise Stuck() if not is_value(v) else NoMatch()
    if isinstance(p, PPair):
        if isinstance(v, Pair):
            b = match_pattern(env, p.fst, v.fst, fuel, unfold)
            b.update(match_pattern(env, p.snd, v.snd, fuel, unfold))
            return b
        raise Stuck() if not is_value(v) else NoMatch()
    if isinstance(p, PCon):
        h, args = unapply(v)
        if not isinstance(h, Con):
            raise Stuck() if not is_value(v) else NoMatch()
        if h.name != p.name:
            raise NoMatch()
        # skip the data parameters: they come first and are not matched
        nparams = len(env.datas[env.cons[p.name][0]].params) if p.name in env.cons else 0
        args = args[nparams:]
        if len(args) != len(p.args):
            raise NoMatch()
        b = {}
        for q, a in zip(p.args, args):
            b.update(match_pattern(env, q, a, fuel, unfold))
        return b
    raise TypeError(f"match_pattern: unknown pattern {p!r}")


# ------------------------------------------------------------------- whnf

class Fuel:
    def __init__(self, n):
        self.n = n

    def tick(self):
        self.n -= 1
        if self.n <= 0:
            raise OutOfFuel("out of fuel: the reduction did not finish")


def whnf(env: Env, t: Term, fuel: Fuel, unfold: bool = True) -> Term:
    """`unfold=False`: beta, iota and prim only; global names stay folded (for readable labels)."""
    while True:
        if isinstance(t, App):
            head, args = unapply(t)
            head = whnf(env, head, fuel, unfold)
            if isinstance(head, Lam):
                try:
                    b = match_pattern(env, head.param, args[0], fuel, unfold)
                except NoMatch:
                    raise EvalError(f"argument {pp(args[0])} does not match pattern of {pp(head)}")
                except Stuck:
                    return apply(head, args)
                fuel.tick()
                t = apply(subst(head.body, b), args[1:])
                continue
            if isinstance(head, Var) and head.name in env.defs and env.defs[head.name].body is not None \
                    and env.defs[head.name].data is None:
                body = env.defs[head.name].body
                if isinstance(body, Extern):
                    r = try_extern(env, body, args, fuel)
                    return r if r is not None else apply(head, args)
                if not unfold or len(args) < lam_arity(body):
                    return apply(head, args)   # partial applications of functions stay folded
                unfolded = try_unfold(env, head.name, args, fuel)
                if unfolded is not None:
                    return unfolded
                return apply(head, args)
            if isinstance(head, Extern):
                r = try_extern(env, head, args, fuel)
                if r is not None:
                    t = r
                    continue
            return apply(head, args)
        if isinstance(t, Var):
            if t.name in env.defs and unfold:
                d = env.defs[t.name]
                if d.body is not None and d.data is None:
                    body = d.body
                    # constants unfold freely; functions and externs unfold only when applied (see App)
                    if isinstance(body, (Lam, Extern)):
                        return t
                    fuel.tick()
                    t = body
                    continue
            return t
        if isinstance(t, Match):
            s = whnf(env, t.scrut, fuel, unfold)
            chosen = None
            try:
                for p, b in t.branches:
                    try:
                        binds = match_pattern(env, p, s, fuel, unfold)
                    except NoMatch:
                        continue
                    chosen = (b, binds)
                    break
            except Stuck:
                return Match(s, t.branches)
            if chosen is None:
                if is_value(s):
                    raise EvalError(f"no branch matches {pp(s)} in {pp(t)}")
                return Match(s, t.branches)
            fuel.tick()
            t = subst(chosen[0], chosen[1])
            continue
        if isinstance(t, BinOp):
            a = whnf(env, t.lhs, fuel, unfold)
            b = whnf(env, t.rhs, fuel, unfold)
            r = prim(env, t.op, a, b, fuel)
            return r if r is not None else BinOp(t.op, a, b)
        if isinstance(t, Forget):
            t = t.arg
            continue
        return t


def lam_arity(t: Term) -> int:
    n = 0
    while isinstance(t, Lam):
        n += 1
        t = t.body
    return n


def try_unfold(env: Env, name: str, args, fuel: Fuel) -> Optional[Term]:
    """Unfold `name args` unless the result is a match stuck on a neutral scrutinee."""
    body = env.defs[name].body
    fuel.tick()
    t = apply(body, args)
    saved = fuel.n
    try:
        r = whnf(env, t, fuel)
    except EvalError:
        raise
    if _stuck_match(env, r):
        fuel.n = saved
        return None
    return r


def _stuck_match(env: Env, t: Term) -> bool:
    h, args = unapply(t)
    return isinstance(h, Match) or (isinstance(h, Lam) and len(args) > 0)


def prim(env: Env, op: str, a: Term, b: Term, fuel: Fuel) -> Optional[Term]:
    if op in ("==", "/="):
        eq = try_equal(env, a, b, fuel)
        if eq is None:
            return None
        return bool_con(eq if op == "==" else not eq)
    if isinstance(a, Lit) and isinstance(b, Lit) and not isinstance(a.value, str) and not isinstance(b.value, str):
        x, y = a.value, b.value
        try:
            if op == "+": return Lit(x + y)
            if op == "-": return Lit(x - y)
            if op == "*": return Lit(x * y)
            if op == "/": return Lit(x // y if isinstance(x, int) and isinstance(y, int) else x / y)
            if op == "mod": return Lit(x % y)
            if op == "<": return bool_con(x < y)
            if op == "<=": return bool_con(x <= y)
            if op == ">": return bool_con(x > y)
            if op == ">=": return bool_con(x >= y)
        except ZeroDivisionError:
            raise EvalError(f"division by zero in {x} {op} {y}")
    if isinstance(a, Lit) and isinstance(b, Lit) and op == "+" and isinstance(a.value, str) and isinstance(b.value, str):
        return Lit(a.value + b.value)
    return None


def try_equal(env: Env, a: Term, b: Term, fuel: Fuel) -> Optional[bool]:
    """Decidable equality of closed values; None if either side is stuck."""
    a = whnf(env, a, fuel)
    b = whnf(env, b, fuel)
    if isinstance(a, Lit) and isinstance(b, Lit):
        return a.value == b.value
    if isinstance(a, Pair) and isinstance(b, Pair):
        e1 = try_equal(env, a.fst, b.fst, fuel)
        if e1 is None: return None
        if not e1: return False
        return try_equal(env, a.snd, b.snd, fuel)
    ha, aa = unapply(a)
    hb, ab = unapply(b)
    if isinstance(ha, Con) and isinstance(hb, Con):
        if ha.name != hb.name or len(aa) != len(ab):
            return False
        for x, y in zip(aa, ab):
            e = try_equal(env, x, y, fuel)
            if e is None: return None
            if not e: return False
        return True
    return None


# ----------------------------------------------------------------- extern

def try_extern(env: Env, head: Extern, args, fuel: Fuel) -> Optional[Term]:
    info = env.externs.get(head.target)
    if info is None or len(args) < info.arity:
        return None
    vals = []
    for a in args[:info.arity]:
        v = nf(env, a, fuel)
        if free_vars(v) - set(env.defs) - set(env.datas):
            return None
        py = to_python(env, v)
        if py is _OPAQUE:
            return None
        vals.append(py)
    fuel.tick()
    try:
        result = info.fn(*vals)
    except Exception as e:  # the environment failed: report as an evaluation error
        raise EvalError(f'extern "{head.target}" raised {type(e).__name__}: {e}')
    ret_type = result_type(info.type, info.arity)
    r = from_python(env, result, ret_type)
    return apply(r, args[info.arity:])


def result_type(ty: Term, arity: int) -> Term:
    for _ in range(arity):
        if isinstance(ty, Pi):
            ty = ty.cod
        else:
            break
    return ty


_OPAQUE = object()


def to_python(env: Env, v: Term):
    if isinstance(v, Lit):
        return v.value
    if isinstance(v, Pair):
        a = to_python(env, v.fst)
        b = to_python(env, v.snd)
        if a is _OPAQUE or b is _OPAQUE:
            return _OPAQUE
        return (a,) + (b if isinstance(b, tuple) else (b,))
    h, args = unapply(v)
    if isinstance(h, Con):
        if h.name == "true": return True
        if h.name == "false": return False
        if h.name == "zero": return 0
        if h.name == "succ":
            n = to_python(env, args[-1])
            return _OPAQUE if n is _OPAQUE else n + 1
        if h.name == "nil": return []
        if h.name == "cons":
            x = to_python(env, args[-2]); xs = to_python(env, args[-1])
            return _OPAQUE if x is _OPAQUE or xs is _OPAQUE else [x] + xs
        if h.name == "unit": return None
        if h.name == "nothing": return None
        if h.name == "just": return to_python(env, args[-1])
        return _OPAQUE
    if isinstance(v, Lam):
        # pass a Python callable that evaluates the Luthier function
        def call(*xs):
            t = v
            for x in xs:
                t = App(t, from_python(env, x, None))
            return to_python(env, nf(env, t, Fuel(env.fuel)))
        return call
    return _OPAQUE


def from_python(env: Env, x, ty: Optional[Term]) -> Term:
    """Marshal a Python value into a Luthier value, guided by the declared type when given."""
    head = None
    targs = []
    if ty is not None:
        head, targs = unapply(ty)
    tname = head.name if isinstance(head, Var) else None
    if isinstance(x, bool):
        return bool_con(x)
    if tname == "N" and isinstance(x, int):
        t = Con("zero")
        for _ in range(x):
            t = App(Con("succ"), t)
        return t
    if isinstance(x, (int, float, str)):
        return Lit(x)
    if x is None:
        if tname == "Unit":
            return Con("unit")
        if tname == "Maybe":
            return App(Con("nothing"), targs[0])
        return Con("unit")
    if isinstance(x, (list, tuple)) and tname == "List":
        elt = targs[0]
        t = App(Con("nil"), elt)
        for item in reversed(list(x)):
            t = App(App(App(Con("cons"), elt), from_python(env, item, elt)), t)
        return t
    if isinstance(x, tuple):
        if isinstance(ty, Sigma):
            a = from_python(env, x[0], ty.fst)
            rest = x[1:] if len(x) > 2 else x[1]
            return Pair(a, from_python(env, rest, ty.snd))
        t = from_python(env, x[-1], None)
        for item in reversed(x[:-1]):
            t = Pair(from_python(env, item, None), t)
        return t
    if tname == "Maybe":
        return App(App(Con("just"), targs[0]), from_python(env, x, targs[0]))
    if hasattr(x, "tolist"):  # numpy arrays
        return from_python(env, x.tolist(), ty)
    raise EvalError(f"cannot marshal Python value {x!r} into Luthier type {pp(ty) if ty else '?'}")


# --------------------------------------------------------------------- nf

def nf(env: Env, t: Term, fuel: Fuel) -> Term:
    """Full normal form (normalizes under binders)."""
    t = whnf(env, t, fuel)
    if isinstance(t, App):
        return App(nf(env, t.fn, fuel), nf(env, t.arg, fuel))
    if isinstance(t, Lam):
        return Lam(t.param, nf(env, t.body, fuel), t.ann)
    if isinstance(t, Pi):
        return Pi(t.name, nf(env, t.dom, fuel), nf(env, t.cod, fuel))
    if isinstance(t, Sigma):
        return Sigma(t.name, nf(env, t.fst, fuel), nf(env, t.snd, fuel))
    if isinstance(t, Pair):
        return Pair(nf(env, t.fst, fuel), nf(env, t.snd, fuel))
    if isinstance(t, And):
        return And(nf(env, t.lhs, fuel), nf(env, t.rhs, fuel))
    if isinstance(t, Subtype):
        return Subtype(t.param, nf(env, t.base, fuel), nf(env, t.pred, fuel))
    if isinstance(t, Match):
        return Match(nf(env, t.scrut, fuel), tuple((p, nf(env, b, fuel)) for p, b in t.branches))
    if isinstance(t, BinOp):
        return BinOp(t.op, nf(env, t.lhs, fuel), nf(env, t.rhs, fuel))
    return t


def evaluate(env: Env, t: Term, fuel: Optional[int] = None) -> Term:
    return nf(env, t, Fuel(fuel or env.fuel))


# ------------------------------------------------------------- conversion

def conv(env: Env, a: Term, b: Term, fuel: Fuel, depth: int = 0) -> bool:
    """Definitional equality: compare weak-head normal forms recursively, up to alpha."""
    if depth > 200:
        raise EvalError("conversion check too deep")
    a = whnf(env, a, fuel)
    b = whnf(env, b, fuel)
    if a == b:
        return True
    if isinstance(a, Var) and isinstance(b, Var):
        return a.name == b.name
    if isinstance(a, Lit) and isinstance(b, Lit):
        return a.value == b.value
    if isinstance(a, Univ) and isinstance(b, Univ):
        return True
    if isinstance(a, Con) and isinstance(b, Con):
        return a.name == b.name
    if isinstance(a, Extern) and isinstance(b, Extern):
        return a.target == b.target
    if isinstance(a, App) and isinstance(b, App):
        return conv(env, a.fn, b.fn, fuel, depth + 1) and conv(env, a.arg, b.arg, fuel, depth + 1)
    if isinstance(a, Pair) and isinstance(b, Pair):
        return conv(env, a.fst, b.fst, fuel, depth + 1) and conv(env, a.snd, b.snd, fuel, depth + 1)
    if isinstance(a, Pi) and isinstance(b, Pi):
        if not conv(env, a.dom, b.dom, fuel, depth + 1):
            return False
        x = Var(fresh(a.name))
        return conv(env, subst(a.cod, {a.name: x}), subst(b.cod, {b.name: x}), fuel, depth + 1)
    if isinstance(a, Sigma) and isinstance(b, Sigma):
        if not conv(env, a.fst, b.fst, fuel, depth + 1):
            return False
        x = Var(fresh(a.name))
        return conv(env, subst(a.snd, {a.name: x}), subst(b.snd, {b.name: x}), fuel, depth + 1)
    if isinstance(a, Lam) and isinstance(b, Lam):
        if isinstance(a.param, PVar) and isinstance(b.param, PVar):
            x = Var(fresh(a.param.name))
            return conv(env, subst(a.body, {a.param.name: x}), subst(b.body, {b.param.name: x}), fuel, depth + 1)
        return a == b
    if isinstance(a, Lam) or isinstance(b, Lam):
        # eta
        if isinstance(a, Lam) and isinstance(a.param, PVar):
            x = Var(fresh(a.param.name))
            return conv(env, subst(a.body, {a.param.name: x}), App(b, x), fuel, depth + 1)
        if isinstance(b, Lam) and isinstance(b.param, PVar):
            x = Var(fresh(b.param.name))
            return conv(env, App(a, x), subst(b.body, {b.param.name: x}), fuel, depth + 1)
        return False
    if isinstance(a, Subtype) and isinstance(b, Subtype):
        if not conv(env, a.base, b.base, fuel, depth + 1):
            return False
        if isinstance(a.param, PVar) and isinstance(b.param, PVar):
            x = Var(fresh(a.param.name))
            return conv(env, subst(a.pred, {a.param.name: x}), subst(b.pred, {b.param.name: x}), fuel, depth + 1)
        return a.param == b.param and conv(env, a.pred, b.pred, fuel, depth + 1)
    if isinstance(a, And) and isinstance(b, And):
        return conv(env, a.lhs, b.lhs, fuel, depth + 1) and conv(env, a.rhs, b.rhs, fuel, depth + 1)
    if isinstance(a, BinOp) and isinstance(b, BinOp):
        return a.op == b.op and conv(env, a.lhs, b.lhs, fuel, depth + 1) and conv(env, a.rhs, b.rhs, fuel, depth + 1)
    if isinstance(a, Match) and isinstance(b, Match):
        if len(a.branches) != len(b.branches) or not conv(env, a.scrut, b.scrut, fuel, depth + 1):
            return False
        for (p1, b1), (p2, b2) in zip(a.branches, b.branches):
            if p1 != p2 or not conv(env, b1, b2, fuel, depth + 1):
                return False
        return True
    return False
