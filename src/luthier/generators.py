"""Generators of values by type, for `test`.

Random sampling and, for finite types, exhaustive enumeration. A type can
have a registered Python generator (`gen T := extern "python:mod.fn"`), which
takes a `random.Random` and returns a Python value marshalled by the type.
"""
from __future__ import annotations
import random
import itertools
from typing import Optional, Callable

from .syntax import *
from .subst import subst
from .pretty import pp
from .evaluator import Env, Fuel, whnf, unapply, apply, from_python, as_bool, EvalError


class GenError(Exception):
    pass


class Generators:
    def __init__(self, env: Env, int_range=(-16, 16), float_range=(-10.0, 10.0), max_depth=4, max_tries=2000):
        self.env = env
        self.custom: dict[str, Callable] = {}
        self.int_range = int_range
        self.float_range = float_range
        self.max_depth = max_depth
        self.max_tries = max_tries

    def register(self, type_name: str, fn: Callable):
        self.custom[type_name] = fn

    def fuel(self) -> Fuel:
        return Fuel(self.env.fuel)

    # -------------------------------------------------------------- sample
    def sample(self, ty: Term, rng: random.Random, depth: int = 0) -> Term:
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        if isinstance(h, Var) and h.name in self.custom:
            return from_python(self.env, self.custom[h.name](rng), w)
        if isinstance(h, Var) and h.name == "Int":
            return Lit(rng.randint(*self.int_range))
        if isinstance(h, Var) and h.name == "R":
            return Lit(rng.uniform(*self.float_range))
        if isinstance(h, Var) and h.name == "String":
            return Lit("".join(rng.choice("abcxyz") for _ in range(rng.randint(0, 4))))
        if isinstance(h, Var) and h.name in self.env.datas:
            return self.sample_data(h.name, args, rng, depth)
        if isinstance(w, Sigma):
            a = self.sample(w.fst, rng, depth)
            b = self.sample(subst(w.snd, {w.name: a}), rng, depth)
            return Pair(a, b)
        if isinstance(w, Subtype):
            for _ in range(self.max_tries):
                v = self.sample(w.base, rng, depth)
                if self.satisfies(w, v):
                    return v
            raise GenError(f"could not find a value of {pp(w)} in {self.max_tries} tries; register a generator")
        if isinstance(w, Pi):
            raise GenError(f"no generator for the function type {pp(w)}; register one with `gen`")
        raise GenError(f"no generator for {pp(w)}")

    def satisfies(self, sub: Subtype, v: Term) -> bool:
        try:
            r = whnf(self.env, App(Lam(sub.param, sub.pred), v), self.fuel())
        except EvalError as e:
            raise GenError(f"evaluating the predicate of {pp(sub)} on {pp(v)}: {e}")
        b = as_bool(r)
        if b is None:
            raise GenError(f"the predicate of {pp(sub)} did not reduce to a Bool on {pp(v)}: {pp(r)}")
        return b

    def constructor_args(self, dname: str, cname: str, targs):
        """Argument types of a constructor, with the data parameters instantiated."""
        _, full = self.env.cons[cname]
        cty = full
        for a in targs:
            cty = subst(cty.cod, {cty.name: a})
        doms = []
        while isinstance(cty, Pi):
            doms.append((cty.name, cty.dom))
            cty = cty.cod
        return doms

    def is_recursive(self, dname: str, cname: str, targs) -> bool:
        for _, d in self.constructor_args(dname, cname, targs):
            h, _ = unapply(whnf(self.env, d, self.fuel()))
            if isinstance(h, Var) and h.name == dname:
                return True
        return False

    def sample_data(self, dname: str, targs, rng: random.Random, depth: int) -> Term:
        decl = self.env.datas[dname]
        cons = [c.name for c in decl.constructors]
        if not cons:
            raise GenError(f"{dname} has no constructors")
        if depth >= self.max_depth:
            base = [c for c in cons if not self.is_recursive(dname, c, targs)]
            if base:
                cons = base
        cname = rng.choice(cons)
        t = apply(Con(cname), targs)
        for name, dom in self.constructor_args(dname, cname, targs):
            v = self.sample(dom, rng, depth + 1)
            t = App(t, v)
        return t

    # ----------------------------------------------------------- enumerate
    def enumerate(self, ty: Term) -> Optional[list]:
        """All values of a finite type, or None if it is not finitely enumerable here."""
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        if isinstance(h, Var) and h.name in self.custom:
            return None
        if isinstance(h, Var) and h.name == "Int":
            return [Lit(i) for i in range(self.int_range[0], self.int_range[1] + 1)]
        if isinstance(h, Var) and h.name in self.env.datas:
            decl = self.env.datas[h.name]
            out = []
            for c in decl.constructors:
                doms = self.constructor_args(h.name, c.name, args)
                if any(self.is_recursive(h.name, c.name, args) for _ in [0]):
                    return None
                parts = []
                for _, d in doms:
                    e = self.enumerate(d)
                    if e is None:
                        return None
                    parts.append(e)
                for combo in itertools.product(*parts):
                    out.append(apply(apply(Con(c.name), args), combo))
            return out
        if isinstance(w, Sigma):
            fs = self.enumerate(w.fst)
            if fs is None:
                return None
            out = []
            for a in fs:
                ss = self.enumerate(subst(w.snd, {w.name: a}))
                if ss is None:
                    return None
                out += [Pair(a, b) for b in ss]
            return out
        if isinstance(w, Subtype):
            base = self.enumerate(w.base)
            if base is None:
                return None
            return [v for v in base if self.satisfies(w, v)]
        return None
