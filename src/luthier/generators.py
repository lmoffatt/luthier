"""Values by type, for `test`.

A generator is, whenever possible, a Luthier value of type `Gen A` (size and
seed to a value and the next seed), chosen per type by a `gen T := term`
directive; the base library provides them for Int, Nat, N, R and Bool. What
remains in Python is the machine (the seed is drawn from the run's random
stream) and a fallback that derives a generator for any `data` declaration
from its constructors, until programs can inspect declarations themselves.

One parameter, `size`, bounds every generated value: the range of an Int, the
magnitude of an N, the nesting of a derived data value. A test lets it grow
over the run, as QuickCheck does.
"""
from __future__ import annotations
import random
import itertools
from typing import Optional, Callable

from .syntax import *
from .subst import subst
from .pretty import pp
from .evaluator import Env, Fuel, whnf, nf, unapply, apply, from_python, as_bool, EvalError


class GenError(Exception):
    pass


class Generators:
    def __init__(self, env: Env, size: int = 16, max_tries: int = 2000, recursive_bias: float = 0.8):
        self.env = env
        self.size = size                    # the largest size a run reaches
        self.max_tries = max_tries
        self.recursive_bias = recursive_bias
        self.luthier: dict = {}             # qualified type name -> (label, Gen term)
        self.custom: dict = {}              # qualified type name -> python fn(rng, size)

    @classmethod
    def from_checker(cls, checker, size: int = 16) -> "Generators":
        """Generators with the `gen` directives the checker saw (Luthier terms; externs by import)."""
        import importlib
        g = cls(checker.env, size=size)
        for tname, (kind, label, term) in checker.gens.items():
            if kind == "luthier":
                g.register_luthier(tname, label, term)
            else:
                spec = label.split(":", 1)[1] if label.startswith("python:") else label
                mod, attr = spec.split(":", 1) if ":" in spec else spec.rpartition(".")[::2]
                fn = importlib.import_module(mod)
                for part in attr.split("."):
                    fn = getattr(fn, part)
                g.register(tname, fn)
        return g

    def register(self, type_name: str, fn: Callable):
        self.custom[type_name] = fn

    def register_luthier(self, type_name: str, label: str, term: Term):
        self.luthier[type_name] = (label, term)

    def fuel(self) -> Fuel:
        return Fuel(self.env.fuel)

    # -------------------------------------------------------------- sample
    def registered(self, ty: Term) -> Optional[str]:
        """The name of a registered generator for `ty`, looked up on the type as written
        (before unfolding: `Nat` has its own generator, its unfolding is a subtype of Int)."""
        h, args = unapply(ty)
        if isinstance(h, Var) and not args and (h.name in self.luthier or h.name in self.custom):
            return h.name
        w = whnf(self.env, ty, self.fuel(), unfold=False)
        h, args = unapply(w)
        if isinstance(h, Var) and not args and (h.name in self.luthier or h.name in self.custom):
            return h.name
        return None

    def sample(self, ty: Term, rng: random.Random, size: Optional[int] = None, depth: int = 0) -> Term:
        if size is None:
            size = self.size
        reg = self.registered(ty)
        if reg is not None:
            if reg in self.luthier:
                return self.run_luthier(reg, rng, size, ty)
            return from_python(self.env, self.custom[reg](rng, size), whnf(self.env, ty, self.fuel()))
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        name = h.name if isinstance(h, Var) else None
        if name == "Int":
            return Lit(rng.randint(-size, size))
        if name == "R":
            return Lit(rng.uniform(-size, size))
        if name == "String":
            return Lit("".join(rng.choice("abcxyz") for _ in range(rng.randint(0, min(size, 6)))))
        if name in self.env.datas:
            return self.sample_data(name, args, rng, size, depth)
        if isinstance(w, Sigma):
            a = self.sample(w.fst, rng, size, depth)
            b = self.sample(subst(w.snd, {w.name: a}), rng, size, depth)
            return Pair(a, b)
        if isinstance(w, Subtype):
            rejected = []
            for _ in range(self.max_tries):
                v = self.sample(w.base, rng, size, depth)
                if self.satisfies(w, v):
                    return v
                if len(rejected) < 5:
                    rejected.append(pp(v))
            raise GenError(f"could not find a value of {pp(w)} in {self.max_tries} tries "
                           f"(rejected, for example: {', '.join(rejected)}); give it a `gen`")
        if isinstance(w, Pi):
            raise GenError(f"no generator for the function type {pp(w)}; give it a `gen`")
        raise GenError(f"no generator for {pp(w)}")

    def run_luthier(self, name: str, rng: random.Random, size: int, ty: Term) -> Term:
        label, gen = self.luthier[name]
        seed = rng.randrange(2 ** 31)
        try:
            r = nf(self.env, App(App(gen, Lit(size)), Lit(seed)), self.fuel())
        except EvalError as e:
            raise GenError(f"generator {label} for {pp(ty)} failed on size {size}, seed {seed}: {e}")
        if not isinstance(r, Pair):
            raise GenError(f"generator {label} for {pp(ty)} did not return a pair: {pp(r)}")
        return r.fst

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

    def sample_data(self, dname: str, targs, rng: random.Random, size: int, depth: int) -> Term:
        """Fallback for a `data` without a `gen`: random constructors, nesting bounded by size."""
        decl = self.env.datas[dname]
        cons = [c.name for c in decl.constructors]
        if not cons:
            raise GenError(f"{dname} has no constructors")
        recursive = [c for c in cons if self.is_recursive(dname, c, targs)]
        base = [c for c in cons if c not in recursive]
        if depth >= size and base:
            cons = base
        elif recursive and base and rng.random() < self.recursive_bias:
            cons = recursive          # while there is size left, prefer to grow: a coin flip stays tiny
        cname = rng.choice(cons)
        t = apply(Con(cname), targs)
        for name, dom in self.constructor_args(dname, cname, targs):
            t = App(t, self.sample(dom, rng, size, depth + 1))
        return t

    # ------------------------------------------------------------ describe
    def describe(self, ty: Term, size: Optional[int] = None) -> str:
        """How values of this type are produced, for the certificate."""
        if size is None:
            size = self.size
        reg = self.registered(ty)
        if reg is not None:
            if reg in self.luthier:
                return f"{reg}: {self.luthier[reg][0]}, size up to {size}"
            return f"{reg}: registered Python generator, size up to {size}"
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        name = h.name if isinstance(h, Var) else None
        if name == "Int":
            return f"Int in [-{size}, {size}] (Python fallback; import \"random\" for genInt)"
        if name == "R":
            return f"R uniform in [-{size}, {size}] (Python fallback; import \"random\" for genR)"
        if name == "String":
            return "String: short random strings (fallback)"
        if name in self.env.datas:
            decl = self.env.datas[name]
            if any(self.is_recursive(name, c.name, args) for c in decl.constructors):
                return f"{pp(w)}: derived from its constructors, nesting up to {size}"
            return f"{pp(w)}: all values"
        if isinstance(w, Sigma):
            return f"({self.describe(w.fst, size)}) * ({self.describe(w.snd, size)})"
        if isinstance(w, Subtype):
            return f"{self.describe(w.base, size)} where {pp(w.pred)}"
        return pp(w)

    def generation(self) -> dict:
        return {"size": self.size, "growth": "1 to size over a sampled run",
                "generators": {k: v[0] for k, v in sorted(self.luthier.items())},
                "python_generators": sorted(self.custom)}

    # ----------------------------------------------------------- enumerate
    def enumerate(self, ty: Term, size: Optional[int] = None) -> Optional[list]:
        """All values of a finite type, or None. Int is taken in [-size, size]."""
        if size is None:
            size = self.size
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        name = h.name if isinstance(h, Var) else None
        if name == "Int":
            return [Lit(i) for i in range(-size, size + 1)]
        if name in self.env.datas:
            decl = self.env.datas[name]
            out = []
            for c in decl.constructors:
                if self.is_recursive(name, c.name, args):
                    return None
                parts = []
                for _, d in self.constructor_args(name, c.name, args):
                    e = self.enumerate(d, size)
                    if e is None:
                        return None
                    parts.append(e)
                for combo in itertools.product(*parts):
                    out.append(apply(apply(Con(c.name), args), combo))
            return out
        if isinstance(w, Sigma):
            fs = self.enumerate(w.fst, size)
            if fs is None:
                return None
            out = []
            for a in fs:
                ss = self.enumerate(subst(w.snd, {w.name: a}), size)
                if ss is None:
                    return None
                out += [Pair(a, b) for b in ss]
            return out
        if isinstance(w, Subtype):
            base = self.enumerate(w.base, size)
            if base is None:
                return None
            return [v for v in base if self.satisfies(w, v)]
        return None
