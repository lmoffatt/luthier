"""`test`: run the obligations of a definition and produce a certificate.

An obligation is a closed law: a lambda over the local parameters whose body
is Bool-valued or a conjunction (`&`) of laws. Flattening gives one law per
leaf; each leaf is a function to Bool whose arguments the generators fill.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import random
import time
import json
from typing import Optional

from .syntax import *
from .subst import subst, free_vars
from .pretty import pp
from .machine import normalize
from .evaluator import Env, Fuel, whnf, nf, apply, as_bool, EvalError
from .checker import Checker, Obligation
from .generators import Generators, GenError
from .certify import definition_hash, write_certificate  # noqa: F401 (re-export)


SAMPLE_CASES = 5


@dataclass
class LawResult:
    label: str
    params: list            # ["x : Z7", ...]
    mode: str               # "exhaustive" | "sampled" | "certified"
    cases: int
    passed: bool
    failure: Optional[str] = None   # counterexample, as text
    error: Optional[str] = None     # evaluation or generation error
    domains: list = field(default_factory=list)       # how each parameter was generated
    sample_cases: list = field(default_factory=list)  # the first few cases evaluated, as text


@dataclass
class TestReport:
    definition: str
    laws: list = field(default_factory=list)
    when: str = ""
    hash: str = ""
    certified: bool = False   # taken from a certificate whose hash still matches, not rerun
    seed: Optional[int] = None
    run_seed: Optional[int] = None   # the run's seed this definition's seed was derived from
    generation: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return bool(self.laws) and all(l.passed for l in self.laws)

    def summary(self) -> str:
        lines = []
        for l in self.laws:
            head = "ok  " if l.passed else "FAIL"
            lines.append(f"  {head} {l.label}   [{l.mode}, {l.cases} cases]")
            if l.failure:
                lines.append(f"       counterexample: {l.failure}")
            if l.error:
                lines.append(f"       error: {l.error}")
        verdict = "passed" if self.passed else ("no laws" if not self.laws else "FAILED")
        if self.certified:
            verdict += f" (certified {self.when}, hash {self.hash}; not rerun)"
        elif self.seed is not None and self.run_seed is None:
            verdict += f"  [seed {self.seed}]"
        return f"{self.definition}: {verdict}\n" + "\n".join(lines)


def obligation_law(ob: Obligation) -> Term:
    t = ob.term
    for name, ty in reversed(ob.params):
        t = Lam(PVar(name), t, ann=ty)
    return t


def peel(checker: Checker, law: Term):
    """Split a closed law into ([(name, type)], body) by its Pi type."""
    with checker.silent():
        _, ty = checker.infer([], law)
    params = []
    body = law
    while True:
        w = checker.whnf(ty)
        if not isinstance(w, Pi):
            break
        name = w.name if w.name != "_" else f"x{len(params)}"
        params.append((name, w.dom))
        body = App(body, Var(name))
        ty = subst(w.cod, {w.name: Var(name)})
    return params, body


def flatten(checker: Checker, ob: Obligation) -> list:
    """One (label, closed law) per conjunct of the obligation's predicate."""
    env = checker.env
    out = []
    for leaf in _split_and(env, ob.term):
        closed = leaf
        for name, ty in reversed(ob.params):
            closed = Lam(PVar(name), closed, ann=ty)
        out.append((_label(leaf), closed))
    return out


def _label(leaf: Term) -> str:
    """A law that is a lambda is shown by its body, with the parameter names free."""
    while isinstance(leaf, Lam) and isinstance(leaf.param, PVar):
        leaf = leaf.body
    return pp(leaf)


def _split_and(env: Env, t: Term) -> list:
    """Split conjunctions. First without unfolding globals, so the leaves keep their names;
    then unfolding, in case the conjunction is behind a defined name."""
    light = whnf(env, t, Fuel(env.fuel), unfold=False)
    if isinstance(light, And):
        return _split_and(env, light.lhs) + _split_and(env, light.rhs)
    full = whnf(env, light, Fuel(env.fuel))
    if isinstance(full, And):
        return _split_and(env, full.lhs) + _split_and(env, full.rhs)
    return [light]


def run_law(checker: Checker, gens: Generators, label: str, law: Term, n: int,
            exhaustive: bool, rng: random.Random, show_cases: bool = False,
            size: Optional[int] = None) -> LawResult:
    env = checker.env
    if size is None:
        size = gens.size
    try:
        params, body = peel(checker, law)
    except Exception as e:
        return LawResult(label, [], "sampled", 0, False, error=f"cannot type the law: {e}")
    param_txt = [f"{n_} : {pp(t)}" for n_, t in params]
    try:
        domains = [gens.describe(t, size) for _, t in params]
    except Exception:
        domains = []
    samples: list = []

    def record(values):
        txt = show(values)
        if len(samples) < SAMPLE_CASES:
            samples.append(txt)
        if show_cases:
            print(f"       case {cases}: {txt}")

    def result(mode, cases, passed, failure=None, error=None):
        return LawResult(label, param_txt, mode, cases, passed, failure, error, domains, samples)

    def evaluate(values) -> Optional[bool]:
        t = law
        for v in values:
            t = App(t, v)
        r = normalize(env, t, Fuel(env.run_fuel))
        return as_bool(r), r

    def show(values):
        return ", ".join(f"{n_} = {pp(v)}" for (n_, _), v in zip(params, values))

    cases = 0
    if exhaustive:
        spaces = []
        # enumerate sequentially; dependent types are instantiated with earlier values
        def rec(i, acc):
            nonlocal cases
            if i == len(params):
                cases += 1
                record(acc)
                b, r = evaluate(acc)
                if b is None:
                    raise EvalError(f"did not reduce to a Bool on ({show(acc)}): {pp(r)}")
                if b is False:
                    return acc
                return None
            name, ty = params[i]
            ty_i = subst(ty, {p: v for (p, _), v in zip(params, acc)})
            vals = gens.enumerate(ty_i, size)
            if vals is None:
                raise GenError(f"{pp(ty_i)} is not finitely enumerable; use `with n`")
            for v in vals:
                bad = rec(i + 1, acc + [v])
                if bad is not None:
                    return bad
            return None
        try:
            bad = rec(0, [])
        except (GenError, EvalError) as e:
            return result("exhaustive", cases, False, error=str(e))
        if bad is not None:
            return result("exhaustive", cases, False, failure=show(bad))
        return result("exhaustive", cases, True)
    try:
        for i in range(n):
            # size grows with the case number: small cases first, so a counterexample is minimal
            size_i = 1 + (i * size) // max(n, 1)
            values = []
            for (name, ty) in params:
                ty_i = subst(ty, {p: v for (p, _), v in zip(params, values)})
                values.append(gens.sample(ty_i, rng, size_i))
            cases += 1
            record(values)
            b, r = evaluate(values)
            if b is None:
                return result("sampled", cases, False,
                              error=f"did not reduce to a Bool on ({show(values)}): {pp(r)}")
            if b is False:
                return result("sampled", cases, False, failure=show(values))
    except (GenError, EvalError) as e:
        return result("sampled", cases, False, error=str(e))
    return result("sampled", cases, True)


def run_test(checker: Checker, gens: Generators, name: str, n: int = 100,
             exhaustive: bool = False, seed: Optional[int] = None, deep: bool = False,
             prefix: str = "", show_cases: bool = False, size: Optional[int] = None) -> TestReport:
    """`deep=False` accepts a certificate whose hash matches instead of rerunning.
    Without a seed one is drawn and recorded, so the run can be repeated from the certificate."""
    if seed is None:
        seed = random.randrange(2 ** 31)
    rng = random.Random(seed)
    generation = dict(gens.generation())
    if size is not None:
        generation["size"] = size
    report = TestReport(name, when=time.strftime("%Y-%m-%dT%H:%M:%S"), seed=seed, generation=generation)
    if name not in checker.env.defs:
        report.laws.append(LawResult(name, [], "sampled", 0, False, error="no such definition"))
        return report
    report.hash = definition_hash(checker.env, name, prefix)
    entry = checker.certified.get(name)
    if entry is not None and not deep:
        report.certified = True
        report.when = entry.get("when", "")
        report.seed = entry.get("seed")
        report.generation = entry.get("generation", {})
        for l in entry.get("laws", []):
            report.laws.append(LawResult(l["label"], l.get("params", []), "certified",
                                         l.get("cases", 0), l.get("passed", False),
                                         l.get("failure"), l.get("error"),
                                         l.get("domains", []), l.get("sample_cases", [])))
        return report
    for ob in checker.obligations.get(name, []):
        try:
            pieces = flatten(checker, ob)
        except Exception as e:
            report.laws.append(LawResult(ob.label, [], "sampled", 0, False, error=f"cannot flatten: {e}"))
            continue
        for label, closed in pieces:
            report.laws.append(run_law(checker, gens, label, closed, n, exhaustive, rng, show_cases, size))
    return report


