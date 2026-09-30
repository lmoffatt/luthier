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
from .evaluator import Env, Fuel, whnf, nf, apply, as_bool, EvalError
from .checker import Checker, Obligation
from .generators import Generators, GenError
from .certify import definition_hash, write_certificate  # noqa: F401 (re-export)


@dataclass
class LawResult:
    label: str
    params: list            # ["x : Z7", ...]
    mode: str               # "exhaustive" | "sampled"
    cases: int
    passed: bool
    failure: Optional[str] = None   # counterexample, as text
    error: Optional[str] = None     # evaluation or generation error


@dataclass
class TestReport:
    definition: str
    laws: list = field(default_factory=list)
    when: str = ""
    hash: str = ""
    certified: bool = False   # taken from a certificate whose hash still matches, not rerun

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
            exhaustive: bool, rng: random.Random) -> LawResult:
    env = checker.env
    try:
        params, body = peel(checker, law)
    except Exception as e:
        return LawResult(label, [], "sampled", 0, False, error=f"cannot type the law: {e}")
    param_txt = [f"{n_} : {pp(t)}" for n_, t in params]

    def evaluate(values) -> Optional[bool]:
        t = law
        for v in values:
            t = App(t, v)
        r = nf(env, t, Fuel(env.fuel))
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
                b, r = evaluate(acc)
                if b is None:
                    raise EvalError(f"did not reduce to a Bool on ({show(acc)}): {pp(r)}")
                if b is False:
                    return acc
                return None
            name, ty = params[i]
            ty_i = subst(ty, {p: v for (p, _), v in zip(params, acc)})
            vals = gens.enumerate(ty_i)
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
            return LawResult(label, param_txt, "exhaustive", cases, False, error=str(e))
        if bad is not None:
            return LawResult(label, param_txt, "exhaustive", cases, False, failure=show(bad))
        return LawResult(label, param_txt, "exhaustive", cases, True)
    try:
        for _ in range(n):
            values = []
            for (name, ty) in params:
                ty_i = subst(ty, {p: v for (p, _), v in zip(params, values)})
                values.append(gens.sample(ty_i, rng))
            cases += 1
            b, r = evaluate(values)
            if b is None:
                return LawResult(label, param_txt, "sampled", cases, False,
                                 error=f"did not reduce to a Bool on ({show(values)}): {pp(r)}")
            if b is False:
                return LawResult(label, param_txt, "sampled", cases, False, failure=show(values))
    except (GenError, EvalError) as e:
        return LawResult(label, param_txt, "sampled", cases, False, error=str(e))
    return LawResult(label, param_txt, "sampled", cases, True)


def run_test(checker: Checker, gens: Generators, name: str, n: int = 100,
             exhaustive: bool = False, seed: Optional[int] = None, deep: bool = False,
             prefix: str = "") -> TestReport:
    """`deep=False` accepts a certificate whose hash matches instead of rerunning."""
    rng = random.Random(seed)
    report = TestReport(name, when=time.strftime("%Y-%m-%dT%H:%M:%S"))
    if name not in checker.env.defs:
        report.laws.append(LawResult(name, [], "sampled", 0, False, error="no such definition"))
        return report
    report.hash = definition_hash(checker.env, name, prefix)
    entry = checker.certified.get(name)
    if entry is not None and not deep:
        report.certified = True
        report.when = entry.get("when", "")
        for l in entry.get("laws", []):
            report.laws.append(LawResult(l["label"], l.get("params", []), "certified",
                                         l.get("cases", 0), l.get("passed", False),
                                         l.get("failure"), l.get("error")))
        return report
    for ob in checker.obligations.get(name, []):
        try:
            pieces = flatten(checker, ob)
        except Exception as e:
            report.laws.append(LawResult(ob.label, [], "sampled", 0, False, error=f"cannot flatten: {e}"))
            continue
        for label, closed in pieces:
            report.laws.append(run_law(checker, gens, label, closed, n, exhaustive, rng))
    return report


