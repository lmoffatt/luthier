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


class HoleBlocked(EvalError):
    """A closed evaluation reached a name without a value: a hole not filled, an axiom, an extern not
    registered. Not a failure of what is evaluated: it cannot be evaluated in this program."""

    def __init__(self, msg: str, names=()):
        super().__init__(msg)
        self.names = list(names)


class OutOfFuel(EvalError):
    pass


# `Law` is the interpreter's own: the type of a conjunction of quantified laws. Int, R and
# String are declared in core.lut as holes the environment fills; the interpreter supplies
# their literals, arithmetic and comparisons.
BUILTIN_TYPES = ("Law",)


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
    fuel: int = 200_000                 # steps per reduction in the checker (types, conversion)
    run_fuel: int = 2_000_000_000       # steps per evaluation of a closed term (law cases, eval, run)
    checked: bool = False               # `run --checked`: every value an extern gives is tested against its type


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


UNIT = Con("unit")


def finite(x, what: str = ""):
    """A float result must be a real number: NaN and an overflow to infinity are errors (06 §6)."""
    if isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
        kind = "NaN" if x != x else "an overflow to infinity"
        raise EvalError(f"{kind} in {what}" if what else kind)
    return x


INT64_MAX = 2 ** 63 - 1


def check_int64(x, where: str):
    """An integer crossing into numpy must fit in 64 bits, which numpy would wrap around (06 §6)."""
    if isinstance(x, int) and not isinstance(x, bool) and not (-INT64_MAX - 1 <= x <= INT64_MAX):
        raise EvalError(f"{x} does not fit in 64 bits and cannot cross into {where}")
    return x


def _from_environment_number(x):
    """A number from the environment: NaN and infinities are not values of Float64 (06 §6)."""
    if hasattr(x, "item") and not hasattr(x, "shape") or (hasattr(x, "shape") and getattr(x, "shape", None) == ()):
        x = x.item()
    if isinstance(x, float):
        finite(x, "a value from the environment")
    return x


def _check_array_finite(x):
    """NaN and infinities are not values of Float64, inside an array either (06 §6). An array of
    objects is read entry by entry."""
    import numpy as np
    a = np.asarray(x)
    if a.dtype.kind == "f":
        if a.size and not np.isfinite(a).all():
            raise EvalError("NaN or an infinity in an array from the environment")
    elif a.dtype.kind == "O":
        for e in a.ravel():
            if isinstance(e, (float, np.floating)) and not np.isfinite(e):
                raise EvalError("NaN or an infinity in an array from the environment")


SCALARS = ("Int", "Float64", "Real", "String")
DOUBLE_EXACT = 2 ** 53


def scalar_kind(env: "Env", ty: Optional[Term]) -> Optional[str]:
    """The primitive a type refines (`Nat` and `Fin n` refine Int, `NonNegative` refines Float64),
    or None. What a value of the environment must be to cross as a value of the type."""
    if ty is None:
        return None
    w = strip_subtypes(env, ty)
    if isinstance(w, Var) and w.name in SCALARS:
        return w.name
    return None


def _scalar_from_python(x, kind: str, ty: Term) -> Term:
    """A value of the environment as a value of a primitive type, checked against it (06 §6):
    an Int is a Python int (not a bool); a Float64 is a float, or an int that has an exact double,
    promoted; a String is a str. Anything else is an error at the crossing, so the arithmetic of
    the interpreter never sees a value of the wrong kind."""
    if kind == "Int":
        if isinstance(x, bool) or not isinstance(x, int):
            raise EvalError(f"{x!r} ({type(x).__name__}) from the environment is not a value of "
                            f"{pp(ty)}: an Int crosses as a Python int")
        return Lit(x)
    if kind in ("Float64", "Real"):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise EvalError(f"{x!r} ({type(x).__name__}) from the environment is not a value of "
                            f"{pp(ty)}: a Float64 crosses as a Python float")
        if isinstance(x, int):
            if abs(x) > DOUBLE_EXACT:
                raise EvalError(f"{x} from the environment has no exact double, so it is not a value of {pp(ty)}")
            x = float(x)
        return Lit(finite(x, "a value from the environment"))
    if not isinstance(x, str):
        raise EvalError(f"{x!r} ({type(x).__name__}) from the environment is not a value of "
                        f"{pp(ty)}: a String crosses as a Python str")
    return Lit(x)


def _array_for(env: "Env", x, k: int, cod: Optional[Term], ty: Term):
    """An array of the environment as a value of a function over k indices (04 §6, 06 §7): with
    entries of Int it is an int64 array, with entries of Float64 a float64 array (an integer array
    is promoted, when its entries have exact doubles), finite; with entries of a primitive type
    it has exactly k dimensions. Other entries (strings, records) are kept as given."""
    import numpy as np
    kind = scalar_kind(env, cod)
    if kind is None or kind == "String":
        return x
    a = np.asarray(x)
    if a.ndim != k:
        raise EvalError(f"an array of shape {a.shape} cannot be a value of {pp(ty)}: "
                        f"its entries are {kind}, so it has {k} dimension(s)")
    if kind == "Int":
        if a.size == 0:
            return a.astype(np.int64)
        if a.dtype.kind not in "iu":
            raise EvalError(f"an array of {a.dtype} cannot be a value of {pp(ty)}: its entries are Int")
        if a.dtype.kind == "u" and int(a.max()) > INT64_MAX:
            raise EvalError(f"an array of {a.dtype} does not fit in 64 bits as a value of {pp(ty)}")
        return a if a.dtype == np.int64 else a.astype(np.int64)
    if a.dtype.kind == "f":
        a = a if a.dtype == np.float64 else a.astype(np.float64)
    elif a.dtype.kind in "iu" or a.size == 0:
        if a.size and int(np.abs(a).max()) > DOUBLE_EXACT:
            raise EvalError(f"an integer array with entries beyond 2^53 cannot be a value of {pp(ty)}")
        a = a.astype(np.float64)
    else:
        raise EvalError(f"an array of {a.dtype} cannot be a value of {pp(ty)}: its entries are {kind}")
    if a.size and not np.isfinite(a).all():
        raise EvalError("NaN or an infinity in an array from the environment")
    return a


def _is_structured(env: "Env", ty: Term) -> bool:
    """Whether a type is known to have structure (a product, a function, a record, an array, a
    data), so a bare number or string from the environment cannot be one of its values. A type
    variable or a declared type without a body says nothing, and stays permissive."""
    w = strip_subtypes(env, ty)
    if isinstance(w, (Sigma, Pi)):
        return True
    if record_components(env, ty) is not None:
        return True
    h, _ = unapply(w)
    return isinstance(h, Var) and h.name in env.datas and h.name != "Unit"
BOOL_TYPE = Sum((("true", Var("Unit")), ("false", Var("Unit"))))


def bool_con(b: bool) -> Term:
    """`Bool` is `< true : Unit | false : Unit >` (04 §5)."""
    return Inj(0, "true", UNIT, Var("Bool")) if b else Inj(1, "false", UNIT, Var("Bool"))


def as_bool(t: Term) -> Optional[bool]:
    """A value of `Bool`, by its label: an alternative of another sum is not a truth value."""
    if isinstance(t, Inj) and t.label in ("true", "false"):
        return t.label == "true"
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
    return is_con_value(t) or isinstance(t, (Lit, Pair, Lam, Pi, Sigma, Univ, Subtype, Sum, Inj, NoLaw))


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
    if isinstance(p, PInj):
        if isinstance(v, Inj):
            if v.index != p.index:
                raise NoMatch()
            return match_pattern(env, p.arg, v.arg, fuel, unfold)
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
            head0 = head
            head = whnf(env, head, fuel, unfold)
            if isinstance(head, App) and head != head0:
                # the head unfolded to an application (a constant defined as a partial
                # application): merge its arguments with ours and reduce the whole
                t = apply(head, args)
                continue
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
                    and env.defs[head.name].data is None \
                    and not isinstance(env.defs[head.name].body, (Primitive, Axiom)):
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
            if isinstance(head, Lit) and is_indexable(head.value):
                i = whnf(env, args[0], fuel, unfold)
                if isinstance(i, Lit) and isinstance(i.value, int):
                    fuel.tick()
                    t = apply(index_foreign(head.value, i.value), args[1:])
                    continue
            return apply(head, args)
        if isinstance(t, Var):
            if t.name in env.defs and unfold:
                d = env.defs[t.name]
                if d.body is not None and d.data is None and isinstance(d.body, (Primitive, Axiom)):
                    return t
                if d.body is not None and d.data is None:
                    body = d.body
                    # constants unfold freely; functions and externs unfold only when applied (see App),
                    # except an extern of arity zero, which is a constant the environment provides
                    if isinstance(body, Extern):
                        info = env.externs.get(body.target)
                        if info is not None and info.arity == 0:
                            r = try_extern(env, body, [], fuel)
                            if r is not None:
                                t = r
                                continue
                        return t
                    if isinstance(body, Lam):
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
            if op in ("+", "-", "*", "/", "mod"):
                r = (x + y if op == "+" else x - y if op == "-" else x * y if op == "*"
                     else (x // y if isinstance(x, int) and isinstance(y, int) else x / y) if op == "/"
                     else x % y)
                return Lit(finite(r, f"{x} {op} {y}"))
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
        try:
            return bool(a.value == b.value)
        except Exception:      # opaque values (arrays) have no decidable equality here: stuck
            return None
    if isinstance(a, Pair) and isinstance(b, Pair):
        e1 = try_equal(env, a.fst, b.fst, fuel)
        if e1 is None: return None
        if not e1: return False
        return try_equal(env, a.snd, b.snd, fuel)
    if isinstance(a, Inj) and isinstance(b, Inj):
        if a.index != b.index:
            return False
        return try_equal(env, a.arg, b.arg, fuel)
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
    ty = info.type
    for a in args[:info.arity]:
        v = nf(env, a, fuel)
        if free_vars(v) - set(env.defs) - set(env.datas):
            return None
        dom = ty.dom if isinstance(ty, Pi) else None
        py = to_python(env, v, dom)
        if py is _OPAQUE:
            return None
        if _is_numpy_fn(info.fn):
            check_int64(py, f'extern "{head.target}"')
        vals.append(py)
        ty = subst(ty.cod, {ty.name: v}) if isinstance(ty, Pi) else ty
    fuel.tick()
    try:
        result = info.fn(*vals)
    except Exception as e:  # the environment failed: report as an evaluation error
        raise EvalError(f'extern "{head.target}" raised {type(e).__name__}: {e}')
    ret_type = result_type(info.type, info.arity)
    r = from_python(env, result, ret_type)
    return apply(r, args[info.arity:])


def _is_numpy_fn(fn) -> bool:
    mod = getattr(fn, "__module__", None) or ""
    return mod.startswith("numpy") or type(fn).__name__ == "ufunc"


def result_type(ty: Term, arity: int) -> Term:
    for _ in range(arity):
        if isinstance(ty, Pi):
            ty = ty.cod
        else:
            break
    return ty


_OPAQUE = object()

_RECORD_CLASSES: dict = {}


def record_class(name: str, fields: list):
    """The Python class for a Luthier type with named components: a dataclass with those
    fields, made once per (name, fields). What a filled hole receives and may return."""
    import dataclasses
    key = (name, tuple(fields))
    cls = _RECORD_CLASSES.get(key)
    if cls is None:
        cls = dataclasses.make_dataclass(name.split(".")[-1], list(fields))
        cls.__luthier_type__ = name
        _RECORD_CLASSES[key] = cls
    return cls


def record_components(env: Env, ty: Optional[Term]):
    """For a type whose unfolding is a subtype with named components, (head name, [names], base),
    where base is the Sigma chain of the components; None for any other type."""
    if ty is None:
        return None
    head, _ = unapply(ty)
    w = whnf(env, ty, Fuel(env.fuel))
    while isinstance(w, Subtype) and not isinstance(w.param, PPair):
        w = whnf(env, w.base, Fuel(env.fuel))
    if not isinstance(w, Subtype):
        return None
    names = [n.split("~")[0] for n in pattern_vars(w.param)]
    hname = head.name if isinstance(head, Var) else "Record"
    return hname, names, w.base


def unfold_aliases(env: Env, ty: Term, limit: int = 64) -> Term:
    """The type an alias stands for, through any chain of aliases (05 R7); every other name stays."""
    for _ in range(limit):
        h, args = unapply(ty)
        if not isinstance(h, Var):
            return ty
        d = env.defs.get(h.name)
        if d is None or not d.alias or d.body is None:
            return ty
        body, rest = d.body, list(args)
        while rest and isinstance(body, Lam) and isinstance(body.param, PVar):
            body = subst(body.body, {body.param.name: rest.pop(0)})
        if isinstance(body, Lam):
            return ty                   # an alias of a type operator, not applied fully
        ty = apply(body, rest) if rest else body
    return ty


def generator_key(env: Env, ty: Term):
    """What a generator is attached to: a type, with its aliases unfolded, so an alias and the type
    it stands for share one generator (05 R7). Returns (key, family, args): `key` names the type
    exactly (`VecOf 16` for `ThetaFull = VecOf (freeDim + 1)`, the type itself for a record alias),
    and `family`, `args` name the type operator and its arguments when it is an application, for a
    generator given to the whole family (`gen VecOf`)."""
    t = unfold_aliases(env, ty)
    h, args = unapply(t)
    if isinstance(h, Var) and not args:
        return h.name, None, []
    if isinstance(h, Var):
        shown = []
        for a in args:
            try:
                shown.append(pp(nf(env, a, Fuel(env.fuel))))
            except EvalError:
                shown.append(pp(a))
        return h.name + " " + " ".join(f"({s})" if " " in s else s for s in shown), h.name, list(args)
    return pp(t), None, []


def strip_subtypes(env: Env, ty: Term) -> Term:
    w = whnf(env, ty, Fuel(env.fuel))
    while isinstance(w, Subtype):
        w = whnf(env, w.base, Fuel(env.fuel))
    return w


def pi_chain(env: Env, ty: Term) -> Term:
    """The function type with each arrow exposed (a subtype of a function type is seen as the
    function type), so arity can be read. Domains and the final result keep their declared
    types: a record stays a record, a subtype keeps its laws."""
    w = strip_subtypes(env, ty)
    if isinstance(w, Pi):
        return Pi(w.name, w.dom, pi_chain(env, w.cod))
    return ty


def to_python(env: Env, v: Term, ty: Optional[Term] = None):
    """Marshal a Luthier value into Python, guided by the declared type when given: a record
    becomes a dataclass, a list keeps its element type, a function receives its arguments by
    their declared types. Without a type: literals, flat tuples, lists, callables."""
    if ty is not None and not is_opaque_type(env, ty):
        sh = shaped(env, ty)
        if sh is not None:
            k, cod = sh
            dims = []
            t = whnf(env, v, Fuel(env.fuel))
            for _ in range(k):
                if not isinstance(t, Pair):
                    return _OPAQUE
                d = whnf(env, t.fst, Fuel(env.fuel))
                if not isinstance(d, Lit):
                    return _OPAQUE
                dims.append(d.value)
                t = t.snd
            return materialize(env, whnf(env, t, Fuel(env.fuel)), dims, cod)
        wf = strip_subtypes(env, ty)
        if isinstance(wf, Pi):
            b0 = fin_bound(env, wf.dom)
            if b0 is not None:
                dims, c = [], wf
                while isinstance(c, Pi) and fin_bound(env, c.dom) is not None:
                    d = whnf(env, fin_bound(env, c.dom), Fuel(env.fuel))
                    if not isinstance(d, Lit):
                        break
                    dims.append(d.value)
                    c = whnf(env, c.cod, Fuel(env.fuel))
                else:
                    return materialize(env, v, dims, c)
        rc = record_components(env, ty)
        if rc is not None:
            hname, names, base = rc
            cur = whnf(env, base, Fuel(env.fuel))
            t = v
            vals = []
            for i, name in enumerate(names):
                if i < len(names) - 1:
                    if not isinstance(t, Pair):
                        return _OPAQUE
                    comp_ty = cur.fst if isinstance(cur, Sigma) else None
                    vals.append(to_python(env, t.fst, comp_ty))
                    if isinstance(cur, Sigma):
                        cur = whnf(env, subst(cur.snd, {cur.name: t.fst}), Fuel(env.fuel))
                    t = t.snd
                else:
                    vals.append(to_python(env, t, cur))
            if any(x is _OPAQUE for x in vals):
                return _OPAQUE
            return record_class(hname, names)(*vals)
        w = strip_subtypes(env, ty)
        h, targs = unapply(w)
        if isinstance(h, Var) and h.name == "List" and len(targs) == 1:
            items = []
            t = v
            while True:
                hh, aa = unapply(t)
                if isinstance(hh, Con) and hh.name == "cons":
                    x = to_python(env, aa[-2], targs[0])
                    if x is _OPAQUE:
                        return _OPAQUE
                    items.append(x)
                    t = aa[-1]
                    continue
                if isinstance(hh, Con) and hh.name == "nil":
                    return items
                return _OPAQUE
        if isinstance(w, Pi):
            # any function value (a lambda, a global function, a partial application, an extern)
            # crosses as a Python callable that applies it and marshals by the declared types
            chain = pi_chain(env, ty)

            def call_typed(*xs):
                t = v
                c = chain
                for x in xs:
                    dom = c.dom if isinstance(c, Pi) else None
                    a = from_python(env, x, dom)
                    t = App(t, a)
                    c = subst(c.cod, {c.name: a}) if isinstance(c, Pi) else c
                return to_python(env, nf(env, t, Fuel(env.fuel)), c)
            return call_typed
    if isinstance(v, Inj):
        return _inj_to_python(env, v, ty)
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


# ------------------------------------------------------ arrays of the environment (04 §6)

def is_indexable(x) -> bool:
    """An object of the environment that is a value of a function type over `Fin n`."""
    return hasattr(x, "shape") and hasattr(x, "__getitem__") and getattr(x, "ndim", 0) >= 1 \
        or isinstance(x, list)


def index_foreign(x, i: int) -> Term:
    """`v i` for an array or a list of the environment: the interpreter checks the range itself,
    because Python would accept a negative index silently."""
    n = len(x)
    if not (0 <= i < n):
        raise EvalError(f"index {i} is outside Fin {n}")
    e = x[i]
    if hasattr(e, "ndim") and getattr(e, "ndim", 0) >= 1:
        return Lit(e)
    if hasattr(e, "item"):
        e = e.item()
    if isinstance(e, bool):
        return bool_con(e)
    if isinstance(e, float):
        return Lit(finite(e, f"entry {i} of an array"))
    if isinstance(e, (int, str)):
        return Lit(e)
    return Lit(e)


def fin_bound(env: Env, dom: Term) -> Optional[Term]:
    """`n` if `dom` is `Fin n`, as written (before unfolding), else None."""
    h, args = unapply(dom)
    if isinstance(h, Var) and h.name == "Fin" and len(args) == 1:
        return args[0]
    return None


def shaped(env: Env, ty: Optional[Term]):
    """For a type `{ n1 : Int, ..., nk : Int, f : Fin n1 -> ... -> Fin nk -> C }` (a vector, a
    matrix), (k, C); else None. Its values cross to Python as one k-dimensional array."""
    if ty is None:
        return None
    w = strip_subtypes(env, ty)
    names = []
    while isinstance(w, Sigma):
        fw = strip_subtypes(env, w.fst)
        if not (isinstance(fw, Var) and fw.name == "Int"):
            return None
        names.append(w.name)
        w = strip_subtypes(env, w.snd)
    if not names:
        return None
    for n in names:
        if not isinstance(w, Pi):
            return None
        b = fin_bound(env, w.dom)
        if not (isinstance(b, Var) and b.name == n):
            return None
        w = whnf(env, w.cod, Fuel(env.fuel))
    return len(names), w


def materialize(env: Env, f: Term, dims: list, cod: Optional[Term]):
    """The array of the values of a function over Fin d1 x ... x Fin dk."""
    import numpy as np
    if isinstance(f, Lit) and is_indexable(f.value):
        return f.value

    def rec(t, ds):
        if not ds:
            v = nf(env, t, Fuel(env.run_fuel))
            py = to_python(env, v, cod)
            return py
        return [rec(App(t, Lit(i)), ds[1:]) for i in range(ds[0])]
    out = rec(f, list(dims))
    if _is_int_type(env, cod):
        flat = np.asarray(out, dtype=object).ravel()
        for v in flat:
            check_int64(v, "an array of numpy")
        return np.asarray(out, dtype=np.int64)
    try:
        arr = np.asarray(out, dtype=float)
        return arr
    except (TypeError, ValueError):
        return out


def _is_int_type(env: Env, t: Optional[Term]) -> bool:
    if t is None:
        return False
    w = strip_subtypes(env, t)
    return isinstance(w, Var) and w.name == "Int"


def _sum_of(env: Env, ty: Optional[Term]):
    """The sum a type unfolds to, or None."""
    if ty is None:
        return None
    w = strip_subtypes(env, ty)
    return w if isinstance(w, Sum) else None


def _inj_to_python(env: Env, v: Inj, ty: Optional[Term]):
    """A value of a sum in Python: a Bool is a bool; `nothing` is None and `just x` is x (the
    Maybe convention); any other alternative is the pair (label, payload)."""
    sm = _sum_of(env, ty)
    labels = sm.labels() if sm is not None else None
    alt_ty = sm.alts[v.index][1] if sm is not None and v.index < len(sm.alts) else None
    label = labels[v.index] if labels is not None and v.index < len(labels) else v.label
    if label in ("true", "false") and (labels is None or labels == ["true", "false"]):
        return label == "true"
    payload = None
    if not (isinstance(v.arg, Con) and v.arg.name == "unit"):
        payload = to_python(env, v.arg, alt_ty)
        if payload is _OPAQUE:
            return _OPAQUE
    if labels == ["nothing", "just"] or (labels is None and label in ("nothing", "just")):
        return payload
    return (label, payload)


def _sum_from_python(env: Env, x, sm: Sum, ty: Term) -> Term:
    labels = sm.labels()
    if labels == ["finite", "negInf", "posInf"] and isinstance(x, (int, float)) and not isinstance(x, bool):
        # ExtendedReal: an infinity that means something (06 §6); NaN is still an error
        x = float(x)
        if x != x:
            raise EvalError("NaN from the environment is not a value of ExtendedReal")
        if x == float("inf"):
            return Inj(2, "posInf", UNIT, ty)
        if x == float("-inf"):
            return Inj(1, "negInf", UNIT, ty)
        return Inj(0, "finite", Lit(x), ty)
    unit_alts = [i for i, (_, a) in enumerate(sm.alts) if _is_unit_type(env, a)]
    if isinstance(x, bool) and labels == ["true", "false"] and len(unit_alts) == 2:
        i = 0 if x else 1
        return Inj(i, labels[i], UNIT, ty)
    if isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], str) and x[0] in labels:
        i = labels.index(x[0])
        arg = UNIT if i in unit_alts else from_python(env, x[1], sm.alts[i][1])
        return Inj(i, labels[i], arg, ty)
    if x is None and unit_alts:
        i = unit_alts[0]
        return Inj(i, labels[i], UNIT, ty)
    payload = [i for i in range(len(sm.alts)) if i not in unit_alts]
    if len(payload) == 1:
        i = payload[0]
        return Inj(i, labels[i], from_python(env, x, sm.alts[i][1]), ty)
    raise EvalError(f"cannot read {x!r} as a value of {pp(ty)}: give (label, value)")


def _is_unit_type(env: Env, t: Term) -> bool:
    w = whnf(env, t, Fuel(env.fuel))
    return isinstance(w, Var) and w.name == "Unit"


def is_opaque_type(env: Env, ty: Optional[Term]) -> bool:
    """A type declared `T : U := extern "..."`: its values are Python objects that pass through
    Luthier untouched; only externs operate on them."""
    if ty is None:
        return False
    # a refinement of an opaque type (`VecOf n`, `{ v : Vec | ... }`) holds the same values
    w = ty
    for _ in range(32):
        if isinstance(w, Subtype):
            w = w.base
            continue
        h0, a0 = unapply(w)
        if a0 and isinstance(h0, Var) and h0.name in env.defs and env.defs[h0.name].body is not None \
                and not isinstance(env.defs[h0.name].body, Extern):
            w2 = whnf(env, w, Fuel(env.fuel))
            if w2 == w:
                break
            w = w2
            continue
        break
    ty = w
    head, _ = unapply(ty)
    if not isinstance(head, Var):
        return False
    d = env.defs.get(head.name)
    if d is not None and isinstance(d.body, Extern) and isinstance(d.type, Univ):
        return True
    # an alias of an opaque type (`ThetaPos : U := Vec`) is opaque too
    if d is not None and d.body is not None and not isinstance(d.body, Extern) and isinstance(d.type, Univ):
        return is_opaque_type(env, d.body)
    # a declared type without a body (an interface's carrier) holds environment values
    return d is not None and d.body is None and d.data is None and isinstance(d.type, Univ)


def _component(x, name: str, i: int):
    if isinstance(x, dict):
        return x[name]
    if isinstance(x, (tuple, list)):
        return x[i]
    return getattr(x, name)


def from_python(env: Env, x, ty: Optional[Term]) -> Term:
    """Marshal a Python value into a Luthier value, guided by the declared type when given.
    A type with named components accepts a dataclass, any object with those attributes, a
    dict, or a tuple in order; a function type accepts a Python callable, registered as an
    extern the evaluator calls."""
    if is_opaque_type(env, ty):
        return Lit(x)
    if ty is not None and isinstance(x, Extern):
        return x
    sm = _sum_of(env, ty)
    if sm is not None:
        return _sum_from_python(env, x, sm, ty)
    if isinstance(x, float) or (hasattr(x, "dtype") and getattr(x, "shape", None) == ()):
        x = _from_environment_number(x)
    elif hasattr(x, "shape") and hasattr(x, "dtype"):
        _check_array_finite(x)
    kind = scalar_kind(env, ty)
    if kind is not None:
        return _scalar_from_python(x, kind, ty)
    if ty is not None and _is_unit_type(env, strip_subtypes(env, ty)):
        if x is not None:
            raise EvalError(f"{x!r} from the environment is not a value of {pp(ty)}: Unit crosses as None")
        return Con("unit")
    if is_indexable(x) or hasattr(x, "shape"):
        sh = shaped(env, ty)
        if sh is not None:
            k, cod = sh
            import numpy as np
            shape = np.shape(x)
            if len(shape) < k:
                raise EvalError(f"an array of shape {shape} cannot be a value of {pp(ty)}")
            x = _array_for(env, x, k, cod, ty)
            t: Term = Lit(x)
            for d in reversed(shape[:k]):
                t = Pair(Lit(int(d)), t)
            return t
        wf = strip_subtypes(env, ty) if ty is not None else None
        if isinstance(wf, Pi) and fin_bound(env, wf.dom) is not None:
            dims, c = [], wf
            while isinstance(c, Pi) and fin_bound(env, c.dom) is not None:
                dims.append(whnf(env, fin_bound(env, c.dom), Fuel(env.fuel)))
                c = strip_subtypes(env, c.cod)
            d = dims[0]
            if isinstance(d, Lit) and len(x) != d.value:
                raise EvalError(f"an array of length {len(x)} cannot be a value of {pp(ty)}")
            return Lit(_array_for(env, x, len(dims), c, ty))
    rc = record_components(env, ty)
    if rc is not None and not isinstance(x, (int, float, str, bool)):
        hname, names, base = rc
        cur = whnf(env, base, Fuel(env.fuel))
        comps = []
        for i, name in enumerate(names):
            try:
                piece = _component(x, name, i)
            except (KeyError, IndexError, AttributeError, TypeError) as e:
                raise EvalError(f"cannot read component {name} of {hname} from {x!r}: {e}")
            if i < len(names) - 1:
                if not isinstance(cur, Sigma):
                    raise EvalError(f"{hname}: expected a pair type for component {name}")
                val = from_python(env, piece, cur.fst)
                comps.append(val)
                cur = whnf(env, subst(cur.snd, {cur.name: val}), Fuel(env.fuel))
            else:
                comps.append(from_python(env, piece, cur))
        t = comps[-1]
        for c in reversed(comps[:-1]):
            t = Pair(c, t)
        return t
    if callable(x) and not isinstance(x, type) and ty is not None and isinstance(strip_subtypes(env, ty), Pi):
        chain = pi_chain(env, ty)
        n = 0
        c = chain
        while isinstance(c, Pi):
            n += 1
            c = c.cod
        target = f"python:{getattr(x, '__module__', 'callable')}.{getattr(x, '__qualname__', 'fn')}#{id(x)}"
        env.externs[target] = ExternInfo(x, n, chain)
        return Extern(target, ty)
    head = None
    targs = []
    if ty is not None:
        head, targs = unapply(ty)
    tname = head.name if isinstance(head, Var) else None
    if isinstance(x, (bool, int, float, str)) and ty is not None and tname not in ("N", "Maybe") \
            and _is_structured(env, ty):
        raise EvalError(f"{x!r} ({type(x).__name__}) from the environment is not a value of {pp(ty)}")
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
        ws = strip_subtypes(env, ty) if ty is not None else None
        if isinstance(ws, Sigma):
            if len(x) < 2:
                raise EvalError(f"{x!r} from the environment is not a value of {pp(ty)}: a pair has two parts")
            a = from_python(env, x[0], ws.fst)
            rest = x[1:] if len(x) > 2 else x[1]
            snd = ws.snd if ws.name == "_" else subst(ws.snd, {ws.name: a})
            return Pair(a, from_python(env, rest, snd))
        if ty is not None and _is_structured(env, ty):
            raise EvalError(f"a tuple from the environment is not a value of {pp(ty)}")
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
        return Lam(t.param, nf(env, t.body, fuel), t.ann, t.res)
    if isinstance(t, Pi):
        return Pi(t.name, nf(env, t.dom, fuel), nf(env, t.cod, fuel))
    if isinstance(t, Sigma):
        return Sigma(t.name, nf(env, t.fst, fuel), nf(env, t.snd, fuel))
    if isinstance(t, Pair):
        return Pair(nf(env, t.fst, fuel), nf(env, t.snd, fuel))
    if isinstance(t, Inj):
        return Inj(t.index, t.label, nf(env, t.arg, fuel), t.type)
    if isinstance(t, Sum):
        return Sum(tuple((l, nf(env, a, fuel)) for l, a in t.alts))
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
    """The value of a closed term: by environments and call by need (machine.py), falling back
    to substitution for what that does not handle."""
    from .machine import normalize
    return normalize(env, t, Fuel(fuel or env.run_fuel))


# ------------------------------------------------------------- conversion

def conv(env: Env, a: Term, b: Term, fuel: Fuel, depth: int = 0) -> bool:
    """Definitional equality: compare weak-head normal forms recursively, up to alpha."""
    if depth > 200:
        raise EvalError("conversion check too deep")
    a = whnf(env, a, fuel)
    b = whnf(env, b, fuel)
    # a labeled product is the product: its labels are binders (04 §2)
    while isinstance(a, Subtype) and isinstance(a.pred, NoLaw):
        a = whnf(env, a.base, fuel)
    while isinstance(b, Subtype) and isinstance(b.pred, NoLaw):
        b = whnf(env, b.base, fuel)
    if a == b:
        return True
    if isinstance(a, Var) and isinstance(b, Var):
        return a.name == b.name
    if isinstance(a, Sum) and isinstance(b, Sum):
        # structural and positional: labels do not count
        return len(a.alts) == len(b.alts) and all(
            conv(env, x, y, fuel, depth + 1) for (_, x), (_, y) in zip(a.alts, b.alts))
    if isinstance(a, Inj) and isinstance(b, Inj):
        return a.index == b.index and conv(env, a.arg, b.arg, fuel, depth + 1)
    if isinstance(a, NoLaw) and isinstance(b, NoLaw):
        return True
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
            pass
        else:
            ok = True
            for (p1, b1), (p2, b2) in zip(a.branches, b.branches):
                ren = _pattern_renaming(p1, p2)
                if ren is None or not conv(env, b1, subst(b2, {k: Var(v) for k, v in ren.items() if k != v}),
                                           fuel, depth + 1):
                    ok = False
                    break
            if ok:
                return True
    # a definition whose body is stuck on a variable stays folded in whnf; to compare, unfold it
    for x, y, flip in ((a, b, False), (b, a, True)):
        ux = _delta(env, x)
        if ux is not None:
            return conv(env, ux, y, fuel, depth + 1) if not flip else conv(env, y, ux, fuel, depth + 1)
    return False


def _delta(env: Env, t: Term) -> Optional[Term]:
    """One unfolding of the global definition at the head of `t`, beta-reduced, or None."""
    h, args = unapply(t)
    if not isinstance(h, Var) or h.name not in env.defs:
        return None
    d = env.defs[h.name]
    if d.body is None or d.data is not None or isinstance(d.body, (Extern, Primitive, Axiom)):
        return None
    body = d.body
    out = body
    rest = list(args)
    while rest and isinstance(out, Lam) and isinstance(out.param, PVar):
        out = subst(out.body, {out.param.name: rest.pop(0)})
    if rest and isinstance(out, Lam):
        return None
    return apply(out, rest)


def _pattern_renaming(p1, p2) -> Optional[dict]:
    """A renaming of the variables of p2 to those of p1 if the two patterns have the same shape."""
    if isinstance(p1, PVar) and isinstance(p2, PVar):
        return {p2.name: p1.name}
    if isinstance(p1, PWild) and isinstance(p2, PWild):
        return {}
    if isinstance(p1, PLit) and isinstance(p2, PLit):
        return {} if p1.value == p2.value else None
    if isinstance(p1, PPair) and isinstance(p2, PPair):
        a = _pattern_renaming(p1.fst, p2.fst)
        b = _pattern_renaming(p1.snd, p2.snd)
        if a is None or b is None:
            return None
        a.update(b)
        return a
    if isinstance(p1, PCon) and isinstance(p2, PCon):
        if p1.name != p2.name or len(p1.args) != len(p2.args):
            return None
        out = {}
        for x, y in zip(p1.args, p2.args):
            r = _pattern_renaming(x, y)
            if r is None:
                return None
            out.update(r)
        return out
    if isinstance(p1, PInj) and isinstance(p2, PInj):
        if p1.index != p2.index:
            return None
        return _pattern_renaming(p1.arg, p2.arg)
    return None
