"""Loading a program from Python, filling its holes, and running its laws.

    import luthier
    P = luthier.load("world.lut", "dome.lut")
    P.fill("toWorld", geodesy.to_world)       # the environment fills a hole, by name
    P.eval("GpsConsistent f p g 5.0")          # -> True
    P.test("locator")                          # runs the laws, writes the certificate

The `.lut` file is the source and Python loads it at import time; nothing is generated. A
hole is a definition without a body. `fill` gives it one: an extern the evaluator calls,
with the arity its type declares, checked against the Python signature. Values cross as
scalars, tuples, lists and callables, and a type with named components crosses as a
dataclass (`record`). Filling changes the hash of what depends on the hole, so the
certificates that depended on it are stale until `test` runs them again.
"""
from __future__ import annotations
import inspect
import os
import random
from typing import Callable, Optional

from .cli import CORE, Loader, load as _load, make_generators
from .evaluator import (Env, ExternInfo, EvalError, evaluate, to_python, record_components,
                        record_class, pi_chain, _OPAQUE)
from .syntax import Def, Var, Univ, Subtype, Term, Pi, Extern, App
from .subst import fresh
from .parser import parse_term
from .testing import run_test, TestReport
from .certify import cert_path, write_certificate, definition_hash, cone


class FillError(Exception):
    pass


def load(*paths, with_core: bool = True) -> "Program":
    """Load `.lut` files with their imports; type errors raise SystemExit as the CLI does."""
    loader = _load([os.fspath(p) for p in paths], with_core)
    return Program(loader)


class Program:
    def __init__(self, loader: Loader):
        self.loader = loader
        self.checker = loader.checker
        self.env: Env = self.checker.env
        self.filled: dict = {}            # qualified name -> the Python callable that fills it

    # ------------------------------------------------------------------ names
    def resolve(self, name: str) -> str:
        q = self.checker.resolve(name)
        if q is None or q not in self.env.defs:
            raise KeyError(f"no definition {name!r}")
        return q

    def _from_core(self, q: str) -> bool:
        path = self.loader.origin.get(q, ("",))[0]
        return bool(path) and os.path.abspath(path) == os.path.abspath(CORE)

    def is_hole(self, q: str) -> bool:
        d = self.env.defs.get(q)
        return d is not None and d.body is None and d.data is None and not self._from_core(q)

    def holes(self, include_types: bool = False) -> list:
        """The definitions without a body, in load order. Type holes (`Session : U`) only on request."""
        out = []
        for q, d in self.env.defs.items():
            if self.is_hole(q) and (include_types or not isinstance(self.checker.whnf(d.type), Univ)):
                out.append(q)
        return out

    def definitions(self) -> list:
        return [q for q in self.env.defs if not self._from_core(q)]

    # ------------------------------------------------------------------ fill
    def fill(self, name: str, fn: Callable) -> "Program":
        """Give a hole its body: `fn` is called with as many positional arguments as the hole's
        type has arrows, each marshalled by its declared type, and its result marshalled back
        by the result type. A hole whose type carries laws gets the obligation to satisfy them."""
        q = self.resolve(name)
        d = self.env.defs[q]
        if d.data is not None or (d.body is not None and q not in self.filled) or self._from_core(q):
            raise FillError(f"{q} is not a hole")
        chain = pi_chain(self.env, d.type)
        arity = 0
        c = chain
        while isinstance(c, Pi):
            arity += 1
            c = c.cod
        self._check_signature(q, fn, arity)
        target = f"fill:{q}"
        self.env.externs[target] = ExternInfo(fn, arity, chain)
        self.env.defs[q] = Def(q, d.type, Extern(target, d.type), doc=d.doc)
        self.filled[q] = fn
        w = self.checker.whnf(d.type)
        if isinstance(w, Subtype) and q not in self.checker.obligations:
            self.checker.current_def = q
            try:
                self.checker.subtype_obligation([], Var(q), w, d.type)
            finally:
                self.checker.current_def = None
        self._refresh_certificates()
        return self

    @staticmethod
    def _check_signature(q: str, fn: Callable, arity: int):
        try:
            sig = inspect.signature(fn)
        except (TypeError, ValueError):
            return
        params = list(sig.parameters.values())
        if any(p.kind == p.VAR_POSITIONAL for p in params):
            return
        positional = [p for p in params if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
        required = [p for p in positional if p.default is p.empty]
        if len(required) > arity or len(positional) < arity:
            fname = getattr(fn, "__qualname__", repr(fn))
            raise FillError(f"{q} takes {arity} argument(s) by its type, but {fname} takes {len(positional)}")

    def _refresh_certificates(self):
        for q, entry in list(self.checker.certified.items()):
            _, prefix, _ = self.loader.origin.get(q, (None, "", q))
            if entry.get("hash") != definition_hash(self.env, q, prefix):
                del self.checker.certified[q]
                if q not in self.loader.stale:
                    self.loader.stale.append(q)

    # ------------------------------------------------------------ evaluation
    def term(self, src: str):
        """Parse and type a term in the program's scope: (elaborated term, type)."""
        t = parse_term(src)
        with self.checker.silent():
            return self.checker.infer([], t)

    def eval(self, src: str):
        """Evaluate a term and marshal the result to Python; a value Python cannot hold
        (a stuck term, an opaque pair) comes back as the Luthier term."""
        t, ty = self.term(src)
        v = evaluate(self.env, t)
        py = to_python(self.env, v, ty)
        return v if py is _OPAQUE else py

    def call(self, name: str, *args):
        """Apply a definition to Python values and marshal the result to Python. Each argument
        is marshaled by the declared type of its parameter, so a record parameter takes a
        dataclass, a dict or a tuple, and an opaque one takes the Python object itself."""
        from .evaluator import from_python, pi_chain, subst
        q = self.resolve(name)
        ty = self.env.defs[q].type
        chain = pi_chain(self.env, ty)
        t: Term = Var(q)
        for x in args:
            if not isinstance(chain, Pi):
                raise EvalError(f"{name} takes fewer than {len(args)} arguments")
            a = from_python(self.env, x, chain.dom)
            t = App(t, a)
            chain = subst(chain.cod, {chain.name: a})
        v = evaluate(self.env, t)
        py = to_python(self.env, v, chain)
        return v if py is _OPAQUE else py

    # ------------------------------------------------------------------ laws
    def obligations(self) -> list:
        """The definitions that carry laws, those of the files given to `load` first."""
        tops = {path for _, _, path in self.loader.top_programs()}
        first, rest = [], []
        for q in self.checker.obligations:
            path = self.loader.origin.get(q, ("",))[0]
            (first if path in tops else rest).append(q)
        return first + rest

    def blocked_by(self, name: str) -> dict:
        """Why `test name` could not run: the unfilled holes its laws depend on, and the
        type parameters they are quantified over (version 0 cannot generate types)."""
        q = self.resolve(name)
        holes = sorted(n for n in cone(self.env, q) if self.is_hole(n))
        types = []
        for ob in self.checker.obligations.get(q, []):
            for pname, pty in ob.params:
                if isinstance(self.checker.whnf(pty), Univ) and pname not in types:
                    types.append(pname)
        return {"holes": holes, "types": types}

    def test(self, name: str, n: Optional[int] = None, seed: Optional[int] = None, size: int = 16,
             exhaustive: bool = False, deep: bool = True, certificate: bool = True) -> TestReport:
        """Run the laws of one definition. `n` defaults to the file's `test` directive, else 100.
        `deep=False` accepts a certificate whose hash still matches instead of rerunning.
        The certificate is written next to the file the definition comes from."""
        q = self.resolve(name)
        path, prefix, local = self.loader.origin.get(q, (None, "", q))
        if n is None:
            n = 100
            for tq, tn, tex, tsz, _ in self.loader.tests:
                if tq == q:
                    n, exhaustive = tn, tex or exhaustive
                    size = tsz or size
        gens = make_generators(self.loader, size)
        if seed is None:
            seed = random.randrange(2 ** 31)
        report = run_test(self.checker, gens, q, n=n, exhaustive=exhaustive, seed=seed, deep=deep,
                          prefix=prefix, size=size)
        if certificate and path is not None and not report.certified:
            keep = {lc for qq, (p, pre, lc) in self.loader.origin.items()
                    if p == path and qq in self.checker.obligations}
            write_certificate(cert_path(path), [report], {q: local}, keep)
            if report.passed and not report.provisional:
                self.checker.certified[q] = {"hash": report.hash, "when": report.when, "passed": True}
        return report

    def test_all(self, **kw) -> dict:
        return {q: self.test(q, **kw) for q in self.obligations()}

    # ----------------------------------------------------------------- types
    def record(self, name: str):
        """The dataclass for a type with named components, as a filled hole receives it."""
        q = self.resolve(name)
        ty: Term = Var(q)
        t = self.env.defs[q].type
        while isinstance(w := self.checker.whnf(t), Pi):     # a type constructor: apply it to type variables
            ty = App(ty, Var(fresh("A")))
            t = w.cod
        rc = record_components(self.env, ty)
        if rc is None:
            raise KeyError(f"{q} has no named components")
        hname, names, _ = rc
        return record_class(hname, names)
