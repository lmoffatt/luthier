"""Evaluation of closed terms with environments and call by need.

The substitution evaluator in evaluator.py copies an argument into every place the parameter
appears, unevaluated, so an argument used n times is computed n times, and every step rewrites
the whole term. This module evaluates instead to values: a function value is a closure, the
body together with an environment that maps each variable to a thunk, and a thunk is computed
the first time it is forced and then remembers its value. Each argument, and each global
constant, is computed once.

It handles closed terms: law cases, `eval`, values passed to and from the environment. The
checker keeps using the substitution evaluator for types, which are small and may contain
free variables. A term this machine cannot handle (a free variable, an unfilled hole, a node
that only exists before elaboration) raises NotClosed or Unsupported, and the caller falls
back to the substitution evaluator; an error of the program itself (an extern that raised, a
division by zero, a match with no branch) propagates.

Tail positions (the body of an applied closure, the chosen branch of a match) are evaluated
in a loop, so a recursion written as a tail call runs in constant Python stack.
"""
from __future__ import annotations

from typing import Optional

from .syntax import (Term, Var, Lit, Univ, Lam, App, Pi, Sigma, Pair, Arrow, BinOp, Con, Extern,
                     Subtype, Match, And, Forget, Pattern, PVar, PWild, PCon, PPair, PLit,
                     Sum, Inj, NoLaw, PInj, Primitive, Axiom, pattern_vars)
from .subst import subst, free_vars
from .pretty import pp
from .evaluator import (Env, Fuel, EvalError, OutOfFuel, HoleBlocked, ExternInfo, unapply, from_python, to_python,
                        strip_subtypes, pi_chain, result_type, _OPAQUE, nf as subst_nf,
                        is_indexable, index_foreign, fin_bound, shaped, whnf as subst_whnf, finite,
                        check_int64, _is_numpy_fn)


class NotClosed(Exception):
    """The term mentions something without a value: a free variable or an unfilled hole."""

    def __init__(self, msg: str, name: str = ""):
        super().__init__(msg)
        self.name = name


class Unsupported(Exception):
    """A node this machine does not evaluate; the substitution evaluator does."""


# ----------------------------------------------------------------- values

class Value:
    __slots__ = ()


class VLit(Value):
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value


class VCon(Value):
    """A constructor applied to some of its arguments (data parameters first)."""
    __slots__ = ("name", "args")

    def __init__(self, name, args):
        self.name = name
        self.args = args


class VPair(Value):
    __slots__ = ("fst", "snd")

    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd


class VInj(Value):
    """A value of a sum: the alternative's position, its label (for display) and its payload."""
    __slots__ = ("index", "label", "arg")

    def __init__(self, index, label, arg):
        self.index = index
        self.label = label
        self.arg = arg


class VClosure(Value):
    """A lambda with its environment. A lambda over `Fin n` is a table: each index is computed
    at most once (call by need, extended to the entries of a finite function)."""
    __slots__ = ("lam", "env", "memo")

    def __init__(self, lam, env):
        self.lam = lam
        self.env = env
        self.memo = {} if (lam.ann is not None and _is_fin(lam.ann)) else None


def _is_fin(t) -> bool:
    h, args = unapply(t)
    return isinstance(h, Var) and h.name == "Fin" and len(args) == 1


class VExtern(Value):
    """An environment function applied to fewer arguments than its arity."""
    __slots__ = ("term", "info", "args")

    def __init__(self, term, info, args):
        self.term = term
        self.info = info
        self.args = args


class VType(Value):
    """A type passed as an argument. Types are never computed with at run time; they are kept
    as terms, with the environment they were written in, for display and marshaling."""
    __slots__ = ("term", "env")

    def __init__(self, term, env):
        self.term = term
        self.env = env


class Thunk:
    """A term in an environment, computed on first use and then remembered."""
    __slots__ = ("term", "env", "value")

    def __init__(self, term=None, env=None, value=None):
        self.term = term
        self.env = env
        self.value = value

    @staticmethod
    def of(v: Value) -> "Thunk":
        return Thunk(value=v)


UNIT_V = VCon("unit", [])
TRUE = VInj(0, "true", None)
FALSE = VInj(1, "false", None)


def vbool(b: bool) -> Value:
    return TRUE if b else FALSE


# ----------------------------------------------------------------- the machine

class Machine:
    def __init__(self, env: Env, fuel: Fuel):
        self.env = env
        self.fuel = fuel
        cache = getattr(env, "_machine_globals", None)
        if cache is None:
            cache = {}
            try:
                env._machine_globals = cache
            except Exception:
                pass
        self.globals = cache

    # ------------------------------------------------------------ forcing and globals
    def force(self, th: Thunk) -> Value:
        if th.value is None:
            th.value = self.eval(th.term, th.env)
            th.term = th.env = None      # let the term and its environment be collected
        return th.value

    def global_value(self, name: str) -> Value:
        # remembered with the definition it came from: a hole filled later, or a definition
        # replaced, is a different object and is evaluated again
        d0 = self.env.defs.get(name)
        hit = self.globals.get(name)
        if hit is not None and hit[0] is d0:
            return hit[1]
        env = self.env
        if name in env.cons:
            v = VCon(name, [])
        elif name in env.defs:
            d = env.defs[name]
            if d.data is not None:
                v = VType(Var(name), {})
            elif isinstance(d.body, Primitive):
                v = VType(Var(name), {})
            elif isinstance(d.body, Axiom):
                raise NotClosed(f"{name} is an axiom: its laws are assumed and it has no computation", name)
            elif d.body is None:
                if isinstance(d.type, Univ):
                    v = VType(Var(name), {})     # a declared type: its values come from outside
                else:
                    raise NotClosed(f"{name} is declared but has no definition", name)
            elif isinstance(d.body, Extern):
                if isinstance(d.type, Univ) or self._is_universe(d.type):
                    v = VType(Var(name), {})     # an opaque type
                else:
                    v = self.extern_value(d.body)
            else:
                v = self.eval(d.body, {})
        else:
            raise NotClosed(f"unbound name {name}", name)
        self.globals[name] = (d0, v)
        return v

    def _is_universe(self, ty) -> bool:
        return isinstance(ty, Univ)

    def extern_value(self, t: Extern) -> Value:
        info = self.env.externs.get(t.target)
        if info is None:
            raise NotClosed(f'extern "{t.target}" is not registered', t.target)
        if info.arity == 0:
            return self.call_extern(t, info, [])
        return VExtern(t, info, [])

    # ------------------------------------------------------------ evaluation
    def eval(self, term: Term, env: dict) -> Value:
        fuel = self.fuel
        while True:
            fuel.tick()
            if isinstance(term, Var):
                th = env.get(term.name)
                if th is not None:
                    return self.force(th)
                return self.global_value(term.name)
            if isinstance(term, App):
                head, args = unapply(term)
                f = self.eval(head, env)
                thunks = [Thunk(a, env) for a in args]
                last = len(thunks) - 1
                i = 0
                tail = None
                while i <= last:
                    if isinstance(f, VClosure):
                        if f.memo is not None:
                            k = self.force(thunks[i])
                            key = k.value if isinstance(k, VLit) else None
                            if key is not None and key in f.memo:
                                f = f.memo[key]
                                i += 1
                                continue
                            binds = self.match(f.lam.param, Thunk.of(k))
                            env2 = dict(f.env)
                            env2.update(binds)
                            r = self.eval(f.lam.body, env2)
                            if key is not None:
                                f.memo[key] = r
                            f = r
                            i += 1
                            continue
                        binds = self.match(f.lam.param, thunks[i])
                        if binds is None:
                            raise EvalError(f"argument does not match the pattern of a lambda")
                        env2 = dict(f.env)
                        env2.update(binds)
                        if i == last:
                            tail = (f.lam.body, env2)
                            break
                        f = self.eval(f.lam.body, env2)
                    elif isinstance(f, VCon):
                        f = VCon(f.name, f.args + [thunks[i]])
                    elif isinstance(f, VExtern):
                        got = f.args + [thunks[i]]
                        if len(got) == f.info.arity:
                            f = self.call_extern(f.term, f.info, got)
                        else:
                            f = VExtern(f.term, f.info, got)
                    elif isinstance(f, VLit) and is_indexable(f.value):
                        k = self.force(thunks[i])
                        if not (isinstance(k, VLit) and isinstance(k.value, int)):
                            raise EvalError("an array is applied to something that is not an index")
                        f = self.eval(index_foreign(f.value, k.value), {})
                    elif isinstance(f, VType):
                        f = VType(App(self.quote(f), self.quote(self.force(thunks[i]))), {})
                    else:
                        raise EvalError("applying a value that is not a function")
                    i += 1
                if tail is not None:
                    term, env = tail
                    continue
                return f
            if isinstance(term, Match):
                s = Thunk.of(self.eval(term.scrut, env))
                for p, body in term.branches:
                    binds = self.match(p, s)
                    if binds is not None:
                        if binds:
                            env = dict(env)
                            env.update(binds)
                        term = body
                        break
                else:
                    raise EvalError("no branch of a match applies to its value")
                continue
            if isinstance(term, Lam):
                return VClosure(term, env)
            if isinstance(term, Lit):
                return VLit(term.value)
            if isinstance(term, Con):
                return VCon(term.name, [])
            if isinstance(term, Pair):
                return VPair(Thunk(term.fst, env), Thunk(term.snd, env))
            if isinstance(term, Inj):
                return VInj(term.index, term.label, Thunk(term.arg, env))
            if isinstance(term, BinOp):
                a = self.eval(term.lhs, env)
                b = self.eval(term.rhs, env)
                return self.prim(term.op, a, b)
            if isinstance(term, Forget):
                term = term.arg
                continue
            if isinstance(term, Extern):
                if term.type is not None and isinstance(term.type, Univ):
                    return VType(term, {})
                return self.extern_value(term)
            if isinstance(term, (Pi, Sigma, Univ, Subtype, Arrow, Sum, NoLaw)):
                return VType(term, env)
            raise Unsupported(type(term).__name__)

    # ------------------------------------------------------------ patterns
    def match(self, p: Pattern, th: Thunk) -> Optional[dict]:
        """Bindings if the value matches, None if it does not. A variable binds the thunk
        without forcing it; every other pattern forces what it inspects."""
        if isinstance(p, PVar):
            return {p.name: th}
        if isinstance(p, PWild):
            return {}
        v = self.force(th)
        if isinstance(p, PLit):
            if isinstance(v, VLit):
                return {} if v.value == p.value else None
            raise Unsupported("literal pattern on a non-literal")
        if isinstance(p, PPair):
            if not isinstance(v, VPair):
                raise Unsupported("pair pattern on a non-pair")
            a = self.match(p.fst, v.fst)
            if a is None:
                return None
            b = self.match(p.snd, v.snd)
            if b is None:
                return None
            a.update(b)
            return a
        if isinstance(p, PInj):
            if not isinstance(v, VInj):
                raise Unsupported("label pattern on a value that is not of a sum")
            if v.index != p.index:
                return None
            if isinstance(p.arg, PWild):
                return {}
            return self.match(p.arg, v.arg if v.arg is not None else Thunk.of(UNIT_V))
        if isinstance(p, PCon):
            if not isinstance(v, VCon):
                raise Unsupported("constructor pattern on a non-constructor")
            if v.name != p.name:
                return None
            nparams = len(self.env.datas[self.env.cons[p.name][0]].params) if p.name in self.env.cons else 0
            fields = v.args[nparams:]
            if len(fields) != len(p.args):
                raise Unsupported("constructor pattern with the wrong number of fields")
            out = {}
            for q, a in zip(p.args, fields):
                b = self.match(q, a)
                if b is None:
                    return None
                out.update(b)
            return out
        raise Unsupported(type(p).__name__)

    # ------------------------------------------------------------ primitives
    def prim(self, op: str, a: Value, b: Value) -> Value:
        if op in ("==", "/="):
            eq = self.equal(a, b)
            return vbool(eq if op == "==" else not eq)
        if isinstance(a, VType) or isinstance(b, VType):
            return VType(BinOp(op, self.quote(a), self.quote(b)), {})
        if not (isinstance(a, VLit) and isinstance(b, VLit)):
            raise Unsupported(f"{op} on values that are not literals")
        x, y = a.value, b.value
        if isinstance(x, str) or isinstance(y, str):
            if op == "+" and isinstance(x, str) and isinstance(y, str):
                return VLit(x + y)
            raise Unsupported(f"{op} on strings")
        try:
            if op in ("+", "-", "*", "/", "mod"):
                r = (x + y if op == "+" else x - y if op == "-" else x * y if op == "*"
                     else (x // y if isinstance(x, int) and isinstance(y, int) else x / y) if op == "/"
                     else x % y)
                return VLit(finite(r, f"{x} {op} {y}"))
            if op == "<": return vbool(x < y)
            if op == "<=": return vbool(x <= y)
            if op == ">": return vbool(x > y)
            if op == ">=": return vbool(x >= y)
        except ZeroDivisionError:
            raise EvalError(f"division by zero in {x} {op} {y}")
        raise Unsupported(op)

    def equal(self, a: Value, b: Value) -> bool:
        if isinstance(a, VLit) and isinstance(b, VLit):
            try:
                return bool(a.value == b.value)
            except Exception:
                raise EvalError("== is not decidable on these values (arrays): use an approx law")
        if isinstance(a, VCon) and isinstance(b, VCon):
            if a.name != b.name:
                return False
            nparams = len(self.env.datas[self.env.cons[a.name][0]].params) if a.name in self.env.cons else 0
            fa, fb = a.args[nparams:], b.args[nparams:]
            if len(fa) != len(fb):
                raise Unsupported("== on partially applied constructors")
            return all(self.equal(self.force(x), self.force(y)) for x, y in zip(fa, fb))
        if isinstance(a, VPair) and isinstance(b, VPair):
            return self.equal(self.force(a.fst), self.force(b.fst)) and \
                self.equal(self.force(a.snd), self.force(b.snd))
        if isinstance(a, VInj) and isinstance(b, VInj):
            if a.index != b.index:
                return False
            if a.arg is None or b.arg is None:
                return True
            return self.equal(self.force(a.arg), self.force(b.arg))
        raise Unsupported("== on these values")

    # ------------------------------------------------------------ the environment
    def call_extern(self, term: Extern, info: ExternInfo, args: list) -> Value:
        ty = info.type
        vals = []
        numpy_fn = _is_numpy_fn(info.fn)
        for th in args:
            v = self.force(th)
            dom = ty.dom if isinstance(ty, Pi) else None
            py = self.to_python(v, dom)
            if numpy_fn:
                check_int64(py, f'extern "{term.target}"')
            vals.append(py)
            if isinstance(ty, Pi):
                ty = subst(ty.cod, {ty.name: self.quote(v)}) if ty.name in free_vars(ty.cod) else ty.cod
        self.fuel.tick()
        try:
            result = info.fn(*vals)
        except EvalError:
            raise
        except Exception as e:
            raise EvalError(f'extern "{term.target}" raised {type(e).__name__}: {e}')
        rty = result_type(info.type, info.arity)
        value = self.from_python(result, rty)
        if self.env.checked and self.refined(rty):
            self.check_refinements(value, rty, f'extern "{term.target.split("@")[0]}"')
        return value

    def refined(self, ty: Term, depth: int = 0) -> bool:
        """Whether a type has a refinement `check_refinements` would test, remembered per type, so a
        run with --checked pays only where there is something to check."""
        cache = getattr(self.env, "_refined_types", None)
        if cache is None:
            cache = {}
            self.env._refined_types = cache
        hit = cache.get(id(ty))
        if hit is not None and hit[0] is ty:
            return hit[1]
        answer = False
        if depth <= 16:
            w = subst_whnf(self.env, ty, Fuel(self.env.fuel))
            if isinstance(w, Subtype):
                if not isinstance(w.pred, NoLaw) and not (isinstance(w.pred, Con) and w.pred.name == "true"):
                    answer = True
                else:
                    sh = shaped(self.env, ty)
                    if sh is not None:
                        cw = subst_whnf(self.env, sh[1], Fuel(self.env.fuel))
                        answer = isinstance(cw, Subtype)
                    else:
                        b = w.base
                        while isinstance(b, Sigma) and not answer:
                            answer = self.refined(b.fst, depth + 1)
                            b = b.snd
                        if not answer and not isinstance(b, Sigma):
                            answer = self.refined(b, depth + 1)
            elif isinstance(w, Sigma):
                answer = self.refined(w.fst, depth + 1) or self.refined(w.snd, depth + 1)
        cache[id(ty)] = (ty, answer)
        return answer

    def check_refinements(self, v: Value, ty: Term, where: str, depth: int = 0):
        """`run --checked`: the value an extern gave, tested against every refinement of its type
        whose predicate is a Bool (05 R5 at run time): the predicate of a subtype, each component of a
        record or a pair, each entry of an array of a refined type. A quantified law is left to `test`;
        a function is tested when it is called, since it crosses as an extern."""
        if depth > 16:
            return
        try:
            self._check_refinements(v, ty, where, depth)
        except Unsupported:
            pass        # a check the machine cannot make (a value it cannot quote) is skipped, not escalated

    def _check_refinements(self, v: Value, ty: Term, where: str, depth: int):
        w = subst_whnf(self.env, ty, Fuel(self.env.fuel))
        if isinstance(w, Subtype):
            if not isinstance(w.pred, NoLaw) and not (isinstance(w.pred, Con) and w.pred.name == "true"):
                # each law of the predicate (a conjunction is split) applied to the value itself, as a
                # closure: quoting a value that holds functions (a Table and its cell) is not possible,
                # and is not needed; a law that is quantified (a function) is left to `test`
                for law in _conjuncts(w.pred):
                    pred = self.eval(Lam(w.param, law, ann=w.base), {})
                    try:
                        r = self.apply1(pred, Thunk.of(v))
                    except Unsupported:
                        continue
                    if isinstance(r, VInj) and r.label == "false":
                        try:
                            shown = pp(self.quote(v))[:160]
                        except Unsupported:
                            shown = "the value"
                        raise EvalError(f"{where} gave a value outside {pp(ty)} (run --checked): "
                                        f"{shown} does not satisfy {pp(law)[:120]}")
            sh = shaped(self.env, ty)
            if sh is not None and isinstance(v, VPair):
                k, cod = sh
                arr = v
                for _ in range(k):
                    arr = self.force(arr.snd) if isinstance(arr, VPair) else arr
                if isinstance(arr, VLit) and is_indexable(arr.value):
                    cw = subst_whnf(self.env, cod, Fuel(self.env.fuel))
                    if isinstance(cw, Subtype):
                        import numpy as np
                        for e in np.asarray(arr.value).ravel():
                            self.check_refinements(VLit(e.item() if hasattr(e, "item") else e), cod, where, depth + 1)
                return
            if isinstance(w.param, PPair) and isinstance(v, VPair):
                binds = self.match(w.param, Thunk.of(v))
                cur = subst_whnf(self.env, w.base, Fuel(self.env.fuel))
                for name in pattern_vars(w.param):
                    if not isinstance(cur, Sigma):
                        self.check_refinements(self.force(binds[name]), cur, where, depth + 1)
                        break
                    self.check_refinements(self.force(binds[name]), cur.fst, where, depth + 1)
                    cur = subst_whnf(self.env, subst(cur.snd, {cur.name: self.quote(self.force(binds[name]))})
                                     if cur.name != "_" else cur.snd, Fuel(self.env.fuel))
                return
            self.check_refinements(v, w.base, where, depth + 1)
            return
        if isinstance(w, Sigma) and isinstance(v, VPair):
            a = self.force(v.fst)
            self.check_refinements(a, w.fst, where, depth + 1)
            snd = subst(w.snd, {w.name: self.quote(a)}) if w.name != "_" else w.snd
            self.check_refinements(self.force(v.snd), snd, where, depth + 1)

    def to_python(self, v: Value, ty: Optional[Term]):
        if isinstance(v, VLit):
            return v.value
        if ty is not None:
            sh = shaped(self.env, ty)
            if sh is not None and isinstance(v, VPair):
                k, cod = sh
                dims = []
                cur = v
                for _ in range(k):
                    if not isinstance(cur, VPair):
                        break
                    d = self.force(cur.fst)
                    dims.append(d.value)
                    cur = self.force(cur.snd)
                else:
                    return self.materialize(cur, dims, cod)
            w = strip_subtypes(self.env, ty)
            if isinstance(w, Pi) and fin_bound(self.env, w.dom) is not None and isinstance(v, (VClosure, VExtern)):
                dims, c = [], w
                while isinstance(c, Pi) and fin_bound(self.env, c.dom) is not None:
                    d = subst_whnf(self.env, fin_bound(self.env, c.dom), Fuel(self.env.fuel))
                    if not isinstance(d, Lit):
                        break
                    dims.append(d.value)
                    c = subst_whnf(self.env, c.cod, Fuel(self.env.fuel))
                else:
                    return self.materialize(v, dims, c)
        if isinstance(v, VInj) and v.label in ("true", "false") and (v.arg is None or True):
            from .evaluator import _sum_of
            sm = _sum_of(self.env, ty)
            if sm is None or sm.labels() == ["true", "false"]:
                return v.label == "true"
        if isinstance(v, VCon) and v.name == "true" and not v.args:
            return True
        if isinstance(v, VCon) and v.name == "false" and not v.args:
            return False
        if isinstance(v, (VClosure, VExtern)) and ty is not None and isinstance(strip_subtypes(self.env, ty), Pi):
            return self._callable(v, ty)
        t = self.quote(v)
        py = to_python(self.env, t, ty)
        if py is _OPAQUE:
            raise Unsupported("a value the environment cannot receive")
        return py

    def materialize(self, f: Value, dims: list, cod: Optional[Term]):
        """The array of a function over Fin d1 x ... x Fin dk (04 §6), kept with the value so the
        same function is not evaluated again when it crosses a second time."""
        if isinstance(f, VLit) and is_indexable(f.value):
            return f.value
        cache = getattr(self.env, "_materialized", None)
        if cache is None:
            cache = {}
            self.env._materialized = cache
        hit = cache.get(id(f))
        if hit is not None and hit[0] is f:
            return hit[1]
        import numpy as np

        def rec(g, ds):
            if not ds:
                return self.to_python(g, cod)
            return [rec(self.apply1(g, Thunk.of(VLit(i))), ds[1:]) for i in range(ds[0])]
        out = rec(f, list(dims))
        from .evaluator import _is_int_type
        if _is_int_type(self.env, cod):
            for v in np.asarray(out, dtype=object).ravel():
                check_int64(v, "an array of numpy")
            arr = np.asarray(out, dtype=np.int64)
        else:
            try:
                arr = np.asarray(out, dtype=float)
            except (TypeError, ValueError):
                arr = out
        if len(cache) > 4096:
            cache.clear()
        cache[id(f)] = (f, arr)
        return arr

    def _callable(self, f: Value, ty: Term):
        chain = pi_chain(self.env, ty)

        def call(*xs):
            v = f
            c = chain
            for x in xs:
                dom = c.dom if isinstance(c, Pi) else None
                a = self.from_python(x, dom)
                v = self.apply1(v, Thunk.of(a))
                c = c.cod if isinstance(c, Pi) else c
            return self.to_python(v, c)
        return call

    def apply1(self, f: Value, th: Thunk) -> Value:
        if isinstance(f, VClosure) and f.memo is not None:
            k = self.force(th)
            key = k.value if isinstance(k, VLit) else None
            if key is not None and key in f.memo:
                return f.memo[key]
            env2 = dict(f.env)
            env2.update(self.match(f.lam.param, Thunk.of(k)))
            r = self.eval(f.lam.body, env2)
            if key is not None:
                f.memo[key] = r
            return r
        if isinstance(f, VClosure):
            binds = self.match(f.lam.param, th)
            if binds is None:
                raise EvalError("argument does not match the pattern of a lambda")
            env2 = dict(f.env)
            env2.update(binds)
            return self.eval(f.lam.body, env2)
        if isinstance(f, VCon):
            return VCon(f.name, f.args + [th])
        if isinstance(f, VExtern):
            got = f.args + [th]
            if len(got) == f.info.arity:
                return self.call_extern(f.term, f.info, got)
            return VExtern(f.term, f.info, got)
        if isinstance(f, VLit) and is_indexable(f.value):
            k = self.force(th)
            return self.eval(index_foreign(f.value, k.value), {})
        raise EvalError("applying a value that is not a function")

    def from_python(self, x, ty: Optional[Term]) -> Value:
        return self.eval(from_python(self.env, x, ty), {})

    # ------------------------------------------------------------ back to terms
    def quote(self, v: Value) -> Term:
        if isinstance(v, VLit):
            return Lit(v.value)
        if isinstance(v, VCon):
            t = Con(v.name)
            for a in v.args:
                t = App(t, self.quote(self.force(a)))
            return t
        if isinstance(v, VPair):
            return Pair(self.quote(self.force(v.fst)), self.quote(self.force(v.snd)))
        if isinstance(v, VInj):
            arg = Con("unit") if v.arg is None else self.quote(self.force(v.arg))
            return Inj(v.index, v.label, arg)
        if isinstance(v, VClosure):
            return self._close(v.lam, v.env)
        if isinstance(v, VExtern):
            t = v.term
            for a in v.args:
                t = App(t, self.quote(self.force(a)))
            return t
        if isinstance(v, VType):
            return self._close(v.term, v.env)
        raise Unsupported("quote")

    def _close(self, t: Term, env: dict) -> Term:
        names = free_vars(t) & set(env)
        if not names:
            return t
        return subst(t, {n: self.quote(self.force(env[n])) for n in names})


# ----------------------------------------------------------------- entry points

import os
_TRACE = os.environ.get("LUTHIER_TRACE_FALLBACK")
fallbacks: dict = {}


def _conjuncts(t: Term) -> list:
    if isinstance(t, And):
        return _conjuncts(t.lhs) + _conjuncts(t.rhs)
    return [t]


def normalize(env: Env, t: Term, fuel: Fuel) -> Term:
    """The value of a closed term, as a term: closed values have this one evaluator. A name with
    no value (a hole, an axiom) is reported as HoleBlocked, with its name, instead of handing the
    term to the substitution evaluator to come back stuck. The normal form of a function value is
    under a binder, which is the substitution evaluator's: printing a function is not computing a
    value. A node the machine does not evaluate still falls back, and is counted (`fallbacks`)."""
    try:
        m = Machine(env, fuel)
        v = m.eval(t, {})
        if isinstance(v, (VClosure, VType)):
            return subst_nf(env, m.quote(v), fuel)
        return m.quote(v)
    except NotClosed as e:
        raise HoleBlocked(f"depends on {e.name or 'a name'} without a value: {e}", [e.name] if e.name else [])
    except Unsupported as e:
        key = f"{type(e).__name__}: {e}"
        fallbacks[key] = fallbacks.get(key, 0) + 1
        if _TRACE:
            import sys
            print(f"[machine fallback] {key}", file=sys.stderr)
        return subst_nf(env, t, fuel)
