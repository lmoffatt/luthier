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
from .subst import subst, free_vars
from .pretty import pp
from .evaluator import (unfold_aliases, to_python, Env, Fuel, whnf, nf, unapply, apply, from_python, as_bool, EvalError,
                        fin_bound, strip_subtypes, generator_key, scalar_kind)


class GenError(Exception):
    pass


class EmptyDomain(GenError):
    """A type with no values (`Fin 0`, `Empty`): a law quantified over it holds vacuously (05 §7)."""


class OutsideType(GenError):
    """A registered generator gave a value outside its type: the generator is wrong, and a law
    drawing from it fails rather than goes unrun."""


class Generators:
    def __init__(self, env: Env, size: int = 16, max_tries: int = 2000, recursive_bias: float = 0.8,
                 checker=None, law_probes: int = 5):
        self.env = env
        self.size = size                    # the largest size a run reaches
        self.max_tries = max_tries
        self.recursive_bias = recursive_bias
        self.checker = checker              # to type a quantified predicate when a subtype's law is one
        self.law_probes = law_probes        # how many arguments such a law is probed on before a value is accepted
        self.luthier: dict = {}             # generator key (generator_key) -> (label, Gen term)
        self.custom: dict = {}              # generator key -> python fn(rng, size)
        self.checked: dict = {}             # generator key -> [values drawn, values outside the type]
        self.bounded = False                # set when an enumeration took Int in a box

    @classmethod
    def from_checker(cls, checker, size: int = 16) -> "Generators":
        """Generators with the `gen` directives the checker saw (Luthier terms; externs by import)."""
        import importlib
        g = cls(checker.env, size=size, checker=checker)
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
    def registered(self, ty: Term):
        """The registered generator for `ty` and the arguments it receives. A type with a name of
        its own (`Nat`, not its unfolding to a subtype of Int) or an instance (`VecOf 16`) is looked
        up first, with its aliases unfolded, since an alias is the type it stands for (05 R7); then
        the family (`gen VecOf`), which receives the arguments."""
        tables = (self.luthier, self.custom)
        key, family, args = generator_key(self.env, ty)
        if any(key in t for t in tables):
            return key, []
        if family is not None and any(family in t for t in tables):
            return family, args
        w = whnf(self.env, ty, self.fuel(), unfold=False)
        h, args = unapply(w)
        if isinstance(h, Var) and any(h.name in t for t in tables):
            return h.name, args
        return None

    def laws_of(self, ty: Term) -> list:
        """The subtypes with a predicate that `ty` unfolds through, outermost first: what a value
        must satisfy to be of the type."""
        out = []
        w = whnf(self.env, ty, self.fuel())
        for _ in range(32):
            if not isinstance(w, Subtype):
                break
            if not isinstance(w.pred, NoLaw) and not (isinstance(w.pred, Con) and w.pred.name == "true"):
                out.append(w)
            if isinstance(w.param, PPair):
                break
            w = whnf(self.env, w.base, self.fuel())
        return out

    def from_registered(self, reg: str, ty: Term, make, rng: random.Random, size: int, depth: int) -> Term:
        """A value of a registered generator, checked against the predicate of its type. A generator
        is a claim that its values are of the type, so a value outside is an error that names the
        generator: drawing again would hide the disagreement between the generator and the type's
        laws, which is often what a law over the type is there to see (a negative control drawn
        from `BrokenGraph`, say). Case 9 of the sonolocalización notes."""
        laws = self.laws_of(ty)
        tally = self.checked.setdefault(reg, [0, 0])
        v = make()
        tally[0] += 1
        bad = next((sub for sub in laws if not self.satisfies(sub, v, rng, size, depth)), None)
        if bad is not None:
            tally[1] += 1
            raise OutsideType(f"the generator {reg} gave a value outside {pp(ty)}: {pp(v)[:200]} does not "
                              f"satisfy {pp(bad)[:200]}")
        return v

    def sample(self, ty: Term, rng: random.Random, size: Optional[int] = None, depth: int = 0) -> Term:
        if size is None:
            size = self.size
        fb = fin_bound(self.env, ty)
        if fb is None:
            # an alias of Fin (`Node p = Fin (p.n / 3)`) is Fin: drawn from its range, and empty when
            # the range is, instead of by rejection over Int, which takes its every try to find that out
            fb = fin_bound(self.env, unfold_aliases(self.env, ty))
        if fb is not None:
            d = whnf(self.env, fb, self.fuel())
            if isinstance(d, Lit) and isinstance(d.value, int):
                if d.value <= 0:
                    raise EmptyDomain(f"Fin {d.value} has no values")
                return Lit(rng.randrange(d.value))
        found = self.registered(ty)
        if found is not None:
            reg, targs = found
            if reg in self.luthier:
                return self.from_registered(reg, ty, lambda: self.run_luthier(reg, rng, size, ty, targs),
                                            rng, size, depth)
            pyargs = [to_python(self.env, nf(self.env, a, self.fuel())) for a in targs]
            wty = whnf(self.env, ty, self.fuel())
            return self.from_registered(
                reg, ty, lambda: from_python(self.env, self.custom[reg](rng, size, *pyargs), wty), rng, size, depth)
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        name = h.name if isinstance(h, Var) else None
        if name == "Int":
            return Lit(rng.randint(-size, size))
        if name == "Float64":
            return Lit(rng.uniform(-size, size))
        if name == "Rational":
            from fractions import Fraction
            return Lit(Fraction(rng.randint(-size * 10 ** 6, size * 10 ** 6), rng.randint(1, 10 ** 6)))
        if name == "String":
            return Lit("".join(rng.choice("abcxyz") for _ in range(rng.randint(0, min(size, 6)))))
        if name in self.env.datas:
            return self.sample_data(name, args, rng, size, depth)
        if isinstance(w, Sigma):
            # a second component whose type is empty for the first (entries of Fin 0 in a vector of some
            # length, a record whose matrix has no columns) is drawn again with another first one, as a
            # case is drawn again when one of its parameters is empty
            for attempt in range(10):
                a = self.sample(w.fst, rng, size, depth)
                try:
                    b = self.sample(subst(w.snd, {w.name: a}) if w.name != "_" else w.snd, rng, size, depth)
                except EmptyDomain:
                    if attempt == 9 or w.name == "_":
                        raise
                    continue
                return Pair(a, b)
        if isinstance(w, Sum):
            if not w.alts:
                raise EmptyDomain("Empty has no values")
            i = rng.randrange(len(w.alts))
            label, alt = w.alts[i]
            return Inj(i, label, self.sample(alt, rng, size, depth + 1), ty)
        if isinstance(w, Subtype) and isinstance(w.pred, NoLaw):
            return self.sample(w.base, rng, size, depth)
        if isinstance(w, Subtype):
            rejected = []
            for _ in range(self.max_tries):
                v = self.sample(w.base, rng, size, depth)
                if self.satisfies(w, v, rng, size, depth):
                    return v
                if len(rejected) < 5:
                    rejected.append(pp(v))
            raise GenError(f"could not find a value of {pp(w)} in {self.max_tries} tries "
                           f"(rejected, for example: {', '.join(rejected)}); give it a `gen`")
        if isinstance(w, Pi) and fin_bound(self.env, w.dom) is not None:
            # a function over a finite domain is its table (04 §6)
            d = whnf(self.env, fin_bound(self.env, w.dom), self.fuel())
            if isinstance(d, Lit) and isinstance(d.value, int):
                n = max(d.value, 0)
                cod = w.cod
                vals = [self.sample(cod if w.name == "_" else subst(cod, {w.name: Lit(i)}), rng, size, depth + 1)
                        for i in range(n)]
                if all(isinstance(v, Lit) and isinstance(v.value, (int, float)) and not isinstance(v.value, bool)
                       for v in vals):
                    import numpy as np
                    # the table of a function to Int is an int64 array, as the bridge reads it (06 §7)
                    kind = scalar_kind(self.env, w.cod if w.name == "_" else subst(w.cod, {w.name: Lit(0)}))
                    return Lit(np.asarray([v.value for v in vals], dtype=np.int64 if kind == "Int" else float))
                if all(isinstance(v, Lit) and hasattr(v.value, "ndim") for v in vals) and vals:
                    import numpy as np
                    return Lit(np.stack([v.value for v in vals]))
                x = "i"
                branches = tuple((PLit(i), v) for i, v in enumerate(vals))
                return Lam(PVar(x), Match(Var(x), branches), None)
        if isinstance(w, Pi) and w.name == "_":
            # a function of an infinite domain: a constant, or an affine map when both sides are
            # numbers. A thin sample of the function space, and the certificate says so.
            dw = whnf(self.env, w.dom, self.fuel())
            cw = whnf(self.env, w.cod, self.fuel())
            if isinstance(dw, Var) and dw.name == "Float64" and isinstance(cw, Var) and cw.name == "Float64" and rng.random() < 0.5:
                a = self.sample(w.cod, rng, size, depth + 1)
                b = self.sample(w.cod, rng, size, depth + 1)
                return Lam(PVar("x"), BinOp("+", BinOp("*", a, Var("x")), b), w.dom)
            c = self.sample(w.cod, rng, size, depth + 1)
            return Lam(PWild(), c, w.dom)
        if isinstance(w, Pi):
            raise GenError(f"no generator for the function type {pp(w)}; give it a `gen`")
        raise GenError(f"no generator for {pp(w)}")

    def run_luthier(self, name: str, rng: random.Random, size: int, ty: Term, targs=()) -> Term:
        label, gen = self.luthier[name]
        seed = rng.randrange(2 ** 31)
        for a in targs:
            gen = App(gen, a)
        try:
            # on the machine the laws run on, with the fuel of a run
            from .machine import normalize
            r = normalize(self.env, App(App(gen, Lit(size)), Lit(seed)), Fuel(self.env.run_fuel))
        except EvalError as e:
            raise GenError(f"generator {label} for {pp(ty)} failed on size {size}, seed {seed}: {e}")
        if not isinstance(r, Pair):
            raise GenError(f"generator {label} for {pp(ty)} did not return a pair: {pp(r)}")
        return r.fst

    def satisfies(self, sub: Subtype, v: Term, rng: Optional[random.Random] = None,
                  size: Optional[int] = None, depth: int = 0) -> bool:
        """Whether `v` satisfies the subtype's predicate. Exhaustive enumeration calls this
        without a random stream; a quantified law is then probed with a fixed one."""
        rng = rng if rng is not None else random.Random(0)
        size = size if size is not None else self.size
        try:
            return self.law_holds(App(Lam(sub.param, sub.pred), v), rng, size, depth, sub, v)
        except EvalError as e:
            raise GenError(f"evaluating the predicate of {pp(sub)} on {pp(v)}: {e}")

    def decide(self, law: Term) -> Optional[bool]:
        """The Bool a closed predicate evaluates to, on the machine the laws run on, with the fuel
        of a run; None when it is not a Bool (a quantified law, a conjunction of laws) or the machine
        does not evaluate it, and the substitution evaluator is asked instead."""
        from .machine import Machine, Unsupported, NotClosed, VInj, VCon
        try:
            v = Machine(self.env, Fuel(self.env.run_fuel)).eval(law, {})
        except (Unsupported, NotClosed):
            return None
        if isinstance(v, VInj) and v.label in ("true", "false"):
            return v.label == "true"
        if isinstance(v, VCon) and v.name in ("true", "false") and not v.args:
            return v.name == "true"
        return None

    def applied_type(self, r: Term) -> Optional[Term]:
        """The type of a named law applied to some of its arguments (`NamesDistinct t`), read off its
        declared type with those arguments substituted; None for anything else. Inferring it with the
        checker instead costs a full check for every value a generator gives."""
        h, args = unapply(r)
        if not isinstance(h, Var):
            return None
        d = self.env.defs.get(h.name)
        if d is None or d.type is None:
            return None
        ty = d.type
        for a in args:
            w = whnf(self.env, ty, self.fuel())
            if not isinstance(w, Pi):
                return None
            ty = w.cod if w.name == "_" else subst(w.cod, {w.name: a})
        return ty

    def probe_annotated(self, r: Lam, rng: random.Random, size: int, depth: int, sub) -> bool:
        """A quantified law that is an elaborated lambda carries the types of its parameters, so it
        is probed by drawing from them, with no type inference per value (what made checking a
        generated Table cost a second)."""
        for _ in range(self.law_probes):
            t = r
            try:
                while True:
                    w = whnf(self.env, t, self.fuel())
                    if isinstance(w, Lam) and w.ann is not None and isinstance(w.param, PVar):
                        t = App(w, self.sample(w.ann, rng, size, depth + 1))
                        continue
                    break
            except EmptyDomain:
                continue        # no arguments for this probe: the law holds on it vacuously
            rb = self.decide(t)
            if rb is None:
                rb = as_bool(whnf(self.env, t, self.fuel()))
            if rb is None:
                raise GenError(f"the law of {pp(sub)} did not reduce to a Bool when probed: {pp(t)[:200]}")
            if rb is False:
                return False
        return True

    def law_holds(self, law: Term, rng: random.Random, size: int, depth: int, sub, v) -> bool:
        """A predicate that reduces to a Bool decides; one that is a quantified law (a record
        whose component must be causal, say) is probed on a few generated arguments: a
        counterexample rejects the value, none found accepts it. Certifying the law is the
        obligation's job, not the generator's."""
        b = self.decide(law)
        if b is not None:
            return b
        r = whnf(self.env, law, self.fuel())
        b = as_bool(r)
        if b is not None:
            return b
        if isinstance(r, And):
            return self.law_holds(r.lhs, rng, size, depth, sub, v) and self.law_holds(r.rhs, rng, size, depth, sub, v)
        if isinstance(r, Lam) and r.ann is not None and isinstance(r.param, PVar):
            return self.probe_annotated(r, rng, size, depth, sub)
        ty = self.applied_type(r)
        if ty is None and self.checker is None:
            raise GenError(f"the predicate of {pp(sub)} did not reduce to a Bool on {pp(v)}: {pp(r)}")
        if ty is None:
            with self.checker.silent():
                _, ty = self.checker.infer([], r)
        if not isinstance(whnf(self.env, ty, self.fuel()), Pi):
            raise GenError(f"the predicate of {pp(sub)} did not reduce to a Bool on {pp(v)}: {pp(r)}")
        for _ in range(self.law_probes):
            t, tyc = r, ty
            try:
                while isinstance((pw := whnf(self.env, tyc, self.fuel())), Pi):
                    a = self.sample(pw.dom, rng, size, depth + 1)
                    t = App(t, a)
                    tyc = subst(pw.cod, {pw.name: a})
            except EmptyDomain:
                continue        # no arguments for this probe: the law holds on it vacuously
            rb = self.decide(t)
            if rb is None:
                rb = as_bool(whnf(self.env, t, self.fuel()))
            if rb is None:
                raise GenError(f"the law {pp(r)} of {pp(sub)} did not reduce to a Bool when probed: {pp(t)}")
            if rb is False:
                return False
        return True

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
        found = self.registered(ty)
        if found is not None:
            reg, _ = found
            if reg in self.luthier:
                return f"{reg}: {self.luthier[reg][0]}, size up to {size}"
            return f"{reg}: registered Python generator, size up to {size}"
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        name = h.name if isinstance(h, Var) else None
        if name == "Int":
            return f"Int in [-{size}, {size}] (Python fallback; import \"random\" for genInt)"
        if name == "Float64":
            return f"Float64 uniform in [-{size}, {size}] (Python fallback; import \"random\" for genFloat64)"
        if name == "String":
            return "String: short random strings (fallback)"
        if name in self.env.datas:
            decl = self.env.datas[name]
            if any(self.is_recursive(name, c.name, args) for c in decl.constructors):
                return f"{pp(w)}: derived from its constructors, nesting up to {size}"
            return f"{pp(w)}: all values"
        if isinstance(w, Sigma):
            return f"({self.describe(w.fst, size)}) * ({self.describe(w.snd, size)})"
        if isinstance(w, Pi) and fin_bound(self.env, w.dom) is not None:
            return f"{pp(w)}: drawn as its table"
        if isinstance(w, Pi):
            return f"{pp(w)}: constant functions (affine on R -> R), a thin sample"
        if isinstance(w, Sum):
            return " | ".join(f"{l} ({self.describe(a, size)})" for l, a in w.alts)
        if isinstance(w, Subtype) and isinstance(w.pred, NoLaw):
            return self.describe(w.base, size)
        if isinstance(w, Subtype):
            return f"{self.describe(w.base, size)} where {pp(w.pred)}"
        return pp(w)

    def generation(self) -> dict:
        return {"size": self.size, "growth": "1 to size over a sampled run",
                "generators": {k: v[0] for k, v in sorted(self.luthier.items())},
                "python_generators": sorted(self.custom),
                "checked_against_type": "every value of a registered generator is tested against the "
                                        "predicate of its type; a value outside is an error"}

    def checked_since(self, before: dict) -> dict:
        """For each registered generator used since `before` (a copy of `checked`), how many of its
        values were drawn and how many fell outside their type."""
        out = {}
        for reg, (drawn, outside) in sorted(self.checked.items()):
            d0, o0 = before.get(reg, (0, 0))
            if drawn > d0:
                out[reg] = {"drawn": drawn - d0, "outside_type": outside - o0}
        return out

    # ----------------------------------------------------------- enumerate
    def enumerate(self, ty: Term, size: Optional[int] = None) -> Optional[list]:
        """All values of a finite type, or None. Int is taken in [-size, size], and then the
        enumeration is of a box, not of the type: `bounded` records it, so the grade says
        "bounded" and not "exhaustive" (05 §7)."""
        if size is None:
            size = self.size
        fb = fin_bound(self.env, ty)
        if fb is None:
            # an alias of Fin (`Node p = Fin (p.n / 3)`) is Fin: drawn from its range, and empty when
            # the range is, instead of by rejection over Int, which takes its every try to find that out
            fb = fin_bound(self.env, unfold_aliases(self.env, ty))
        if fb is not None:
            d = whnf(self.env, fb, self.fuel())
            if isinstance(d, Lit) and isinstance(d.value, int):
                return [Lit(i) for i in range(max(d.value, 0))]
        w = whnf(self.env, ty, self.fuel())
        h, args = unapply(w)
        name = h.name if isinstance(h, Var) else None
        if name == "Int":
            self.bounded = True
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
        if isinstance(w, Sum):
            out = []
            for i, (label, alt) in enumerate(w.alts):
                vs = self.enumerate(alt, size)
                if vs is None:
                    return None
                out += [Inj(i, label, v, ty) for v in vs]
            return out
        if isinstance(w, Subtype) and isinstance(w.pred, NoLaw):
            return self.enumerate(w.base, size)
        if isinstance(w, Subtype):
            interval = self.int_interval(w)
            if interval is not None:
                lo, hi = interval        # the predicate bounds the integer: every value is in [lo, hi)
                return [Lit(i) for i in range(lo, hi) if self.satisfies(w, Lit(i))]
            base = self.enumerate(w.base, size)
            if base is None:
                return None
            return [v for v in base if self.satisfies(w, v)]
        return None

    def int_interval(self, sub: Subtype):
        """For a refinement of Int whose predicate is a conjunction bounding its parameter on both
        sides by closed integers (`0 <= k and k < n`), the interval [lo, hi) holding every value;
        else None. What makes enumerating such a type exhaustive and not bounded."""
        if not isinstance(sub.param, PVar):
            return None
        bw = whnf(self.env, sub.base, self.fuel())
        if not (isinstance(bw, Var) and bw.name == "Int"):
            return None
        k = sub.param.name
        lo, hi = None, None

        def closed_int(t):
            if k in free_vars(t):
                return None
            try:
                r = whnf(self.env, t, self.fuel())
            except EvalError:
                return None
            return r.value if isinstance(r, Lit) and isinstance(r.value, int) and not isinstance(r.value, bool) else None

        def walk(t):
            nonlocal lo, hi
            h, args = unapply(t)
            if isinstance(h, Var) and h.name == "and" and len(args) == 2:
                walk(args[0])
                walk(args[1])
                return
            if not isinstance(t, BinOp) or t.op not in ("<", "<=", ">", ">="):
                return
            op, a, b = t.op, t.lhs, t.rhs
            if isinstance(b, Var) and b.name == k:           # c op k  is  k (flipped op) c
                op, a, b = {"<": ">", "<=": ">=", ">": "<", ">=": "<="}[op], b, a
            if not (isinstance(a, Var) and a.name == k):
                return
            c = closed_int(b)
            if c is None:
                return
            if op == "<":
                hi = c if hi is None else min(hi, c)
            elif op == "<=":
                hi = c + 1 if hi is None else min(hi, c + 1)
            elif op == ">":
                lo = c + 1 if lo is None else max(lo, c + 1)
            else:
                lo = c if lo is None else max(lo, c)
        walk(sub.pred)
        if lo is None or hi is None:
            return None
        return lo, max(lo, hi)
