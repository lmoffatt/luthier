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
                     Subtype, Match, And, Forget, Pattern, PVar, PWild, PCon, PPair, PLit)
from .subst import subst, free_vars
from .evaluator import (Env, Fuel, EvalError, OutOfFuel, ExternInfo, unapply, from_python, to_python,
                        strip_subtypes, pi_chain, result_type, _OPAQUE, nf as subst_nf)


class NotClosed(Exception):
    """The term mentions something without a value: a free variable or an unfilled hole."""


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


class VClosure(Value):
    __slots__ = ("lam", "env")

    def __init__(self, lam, env):
        self.lam = lam
        self.env = env


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


TRUE = VCon("true", [])
FALSE = VCon("false", [])


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
            elif d.body is None:
                if isinstance(d.type, Univ):
                    v = VType(Var(name), {})     # a declared type: its values come from outside
                else:
                    raise NotClosed(f"{name} is declared but has no definition")
            elif isinstance(d.body, Extern):
                if isinstance(d.type, Univ) or self._is_universe(d.type):
                    v = VType(Var(name), {})     # an opaque type
                else:
                    v = self.extern_value(d.body)
            else:
                v = self.eval(d.body, {})
        else:
            raise NotClosed(f"unbound name {name}")
        self.globals[name] = (d0, v)
        return v

    def _is_universe(self, ty) -> bool:
        return isinstance(ty, Univ)

    def extern_value(self, t: Extern) -> Value:
        info = self.env.externs.get(t.target)
        if info is None:
            raise NotClosed(f'extern "{t.target}" is not registered')
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
            if isinstance(term, (Pi, Sigma, Univ, Subtype, Arrow)):
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
            if op == "+": return VLit(x + y)
            if op == "-": return VLit(x - y)
            if op == "*": return VLit(x * y)
            if op == "/": return VLit(x // y if isinstance(x, int) and isinstance(y, int) else x / y)
            if op == "mod": return VLit(x % y)
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
        raise Unsupported("== on these values")

    # ------------------------------------------------------------ the environment
    def call_extern(self, term: Extern, info: ExternInfo, args: list) -> Value:
        ty = info.type
        vals = []
        for th in args:
            v = self.force(th)
            dom = ty.dom if isinstance(ty, Pi) else None
            py = self.to_python(v, dom)
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
        return self.from_python(result, result_type(info.type, info.arity))

    def to_python(self, v: Value, ty: Optional[Term]):
        if isinstance(v, VLit):
            return v.value
        if v is TRUE or (isinstance(v, VCon) and v.name == "true" and not v.args):
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


def normalize(env: Env, t: Term, fuel: Fuel) -> Term:
    """The value of a closed term, as a term. Falls back to the substitution evaluator for
    what the machine does not handle; a function value is normalized there too, since its
    normal form is under a binder."""
    try:
        m = Machine(env, fuel)
        v = m.eval(t, {})
        if isinstance(v, (VClosure, VType)):
            return subst_nf(env, m.quote(v), fuel)
        return m.quote(v)
    except (NotClosed, Unsupported) as e:
        key = f"{type(e).__name__}: {e}"
        fallbacks[key] = fallbacks.get(key, 0) + 1
        if _TRACE:
            import sys
            print(f"[machine fallback] {key}", file=sys.stderr)
        return subst_nf(env, t, fuel)
