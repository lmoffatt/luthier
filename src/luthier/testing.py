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
from .evaluator import Env, Fuel, whnf, nf, apply, as_bool, EvalError, OutOfFuel, HoleBlocked
from .checker import Checker, Obligation
from .generators import Generators, GenError, OutsideType
from .certify import definition_hash, write_certificate, fingerprint, generator_fingerprint  # noqa: F401


SAMPLE_CASES = 5


PASSED, FAILED, NOT_RUN = "passed", "failed", "not run"


@dataclass
class LawResult:
    label: str
    params: list            # ["x : Z7", ...]
    mode: str               # "exhaustive" | "bounded" | "sampled" | "certified"
    cases: int
    passed: bool
    failure: Optional[str] = None   # counterexample, as text
    error: Optional[str] = None     # evaluation or generation error, or why the law was not run
    domains: list = field(default_factory=list)       # how each parameter was generated
    sample_cases: list = field(default_factory=list)  # the first few cases evaluated, as text
    outcome: str = ""       # passed | failed (a counterexample, or an error on a case) | not run (05 §7)
    seconds: float = 0.0    # how long the law took, its cases and their generation
    skipped: int = 0        # cases of a type's obligation where the computation raised: outside it

    def __post_init__(self):
        if not self.outcome:
            self.outcome = PASSED if self.passed else FAILED
        self.passed = self.outcome == PASSED


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
    n: int = 0                # the cases asked for each law
    mode: str = "sampled"     # what was asked: sampled or exhaustive
    fingerprint: dict = field(default_factory=dict)   # what the test ran (certify.fingerprint)
    generators: dict = field(default_factory=dict)    # registered generators drawn from -> their fingerprint
    provisional: list = field(default_factory=list)   # provisional externs in its cone: never certified (05 R5)
    citation: Optional[dict] = None                   # `cite`: the reference and who checked; grade proved (05 §7)

    @property
    def outcome(self) -> str:
        """failed if a law failed; not run if none failed and some could not be run; passed when
        every law passed; proved when a citation establishes the laws and none of those run failed."""
        if self.citation is not None and not any(l.outcome == FAILED for l in self.laws):
            return "proved"
        if not self.laws:
            return "no laws"
        if any(l.outcome == FAILED for l in self.laws):
            return FAILED
        if any(l.outcome == NOT_RUN for l in self.laws):
            return NOT_RUN
        return PASSED

    @property
    def passed(self) -> bool:
        return self.outcome in (PASSED, "proved")

    def summary(self) -> str:
        lines = []
        for l in self.laws:
            head = {PASSED: "ok  ", FAILED: "FAIL", NOT_RUN: "skip"}[l.outcome]
            took = f", {l.seconds:.1f} s" if l.seconds >= 0.05 else ""
            skips = f", {l.skipped} where the computation raised" if l.skipped else ""
            lines.append(f"  {head} {l.label}   [{l.mode}, {l.cases} cases{skips}{took}]")
            if l.failure:
                lines.append(f"       counterexample: {l.failure}")
            if l.error:
                lines.append(f"       {'not run' if l.outcome == NOT_RUN else 'error'}: {l.error}")
        verdict = {PASSED: "passed", FAILED: "FAILED", NOT_RUN: "NOT RUN", "no laws": "no laws",
                   "proved": "proved by citation"}[self.outcome]
        if self.citation is not None and self.outcome == "proved":
            verdict += f" ({self.citation.get('key', '?')}, checked by {self.citation.get('checked', 'none')})"
        if self.provisional and self.outcome == PASSED:
            verdict += f", over provisional externs ({', '.join(self.provisional)}): not certified"
        if self.certified:
            verdict += f" (certified {self.when}, hash {self.hash}; not rerun)"
        elif self.seed is not None and self.run_seed is None:
            verdict += f"  [seed {self.seed}]"
        return f"{self.definition}: {verdict}\n" + "\n".join(lines)


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
    """One (label, closed law) per conjunct of the obligation's predicate, quantified only over the
    parameters it mentions (and those their types mention): a law that does not mention a
    variable needs no values of it, and a function of an infinite domain could not be drawn."""
    env = checker.env
    out = []
    for leaf in _split_and(env, ob.term):
        used = set(free_vars(leaf))
        params = []
        for name, ty in reversed(ob.params):
            if name in used:
                params.append((name, ty))
                used |= free_vars(ty)
        params.reverse()
        closed = leaf
        for name, ty in reversed(params):
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
            size: Optional[int] = None, of_type: bool = False) -> LawResult:
    """`of_type`: the obligation of a type (a coercion inside a body, or what an extern owes), a
    claim about the values a computation gives. A case where the computation raises gives no value,
    so it is outside the claim: it is skipped and counted, and an obligation every case of which
    raises is not run. A law stated in a definition's type fails on an error, as on a counterexample."""
    env = checker.env
    skipped = 0

    def raised(e) -> bool:
        return of_type and isinstance(e, EvalError) and not isinstance(e, (OutOfFuel, HoleBlocked))
    if size is None:
        size = gens.size
    try:
        params, body = peel(checker, law)
    except Exception as e:
        return LawResult(label, [], "sampled", 0, False, error=f"cannot type the law: {e}", outcome=NOT_RUN)
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

    def result(mode, cases, passed, failure=None, error=None, outcome=""):
        return LawResult(label, param_txt, mode, cases, passed, failure, error, domains, samples, outcome,
                         skipped=skipped)

    def stuck(values, r):
        """A law that does not reduce to a Bool: not run when what blocks it is a hole without a
        value (a library tested without the file that fills it), failed otherwise."""
        holes = sorted(x for x in free_vars(r) if x in env.defs and env.defs[x].body is None
                       and env.defs[x].data is None)
        if holes:
            return result(mode_now, cases, False, outcome=NOT_RUN,
                          error=f"depends on holes without a value: {', '.join(holes[:6])}")
        return result(mode_now, cases, False, error=f"did not reduce to a Bool on ({show(values)}): {pp(r)}")

    def broken(mode, e):
        """An exception while drawing or evaluating: a generator whose value is outside its type,
        or an evaluation error, fails the law; a type with no generator, a domain the draws cannot
        reach, or a reduction out of fuel leaves it not run."""
        if isinstance(e, HoleBlocked):
            names = ", ".join(e.names) if e.names else "a name"
            return result(mode, cases, False, outcome=NOT_RUN, error=f"depends on holes without a value: {names}")
        if isinstance(e, OutsideType) or (isinstance(e, EvalError) and not isinstance(e, OutOfFuel)):
            return result(mode, cases, False, error=str(e))
        return result(mode, cases, False, error=str(e), outcome=NOT_RUN)

    def evaluate(values) -> Optional[bool]:
        t = law
        for v in values:
            t = App(t, v)
        r = normalize(env, t, Fuel(env.run_fuel))
        return as_bool(r), r

    def show(values):
        return ", ".join(f"{n_} = {pp(v)}" for (n_, _), v in zip(params, values))

    cases = 0
    mode_now = "sampled"
    if exhaustive:
        gens.bounded = False
        mode_now = "exhaustive"
        # enumerate sequentially; dependent types are instantiated with earlier values
        def rec(i, acc):
            nonlocal cases
            if i == len(params):
                cases += 1
                record(acc)
                b, r = evaluate(acc)
                if b is None:
                    raise _Stuck(acc, r)
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
        except _Stuck as st:
            mode_now = "bounded" if gens.bounded else "exhaustive"
            return stuck(st.values, st.term)
        except (GenError, EvalError) as e:
            return broken("bounded" if gens.bounded else "exhaustive", e)
        mode_now = "bounded" if gens.bounded else "exhaustive"
        if bad is not None:
            return result(mode_now, cases, False, failure=show(bad))
        return result(mode_now, cases, True)

    def draw(size_i):
        """One case. A parameter whose type depends on earlier ones may be empty for them (Fin 0):
        the case is drawn again, since a law holds vacuously where it has no arguments. A
        generator whose value is outside its type is not drawn again: it is wrong."""
        for attempt in range(50):
            values = []
            try:
                for (name, ty) in params:
                    ty_i = subst(ty, {p: v for (p, _), v in zip(params, values)})
                    values.append(gens.sample(ty_i, rng, size_i))
                return values
            except OutsideType:
                raise
            except GenError:
                if not values:
                    raise
        return None     # every draw met an empty domain: this case holds vacuously

    unreachable = None
    try:
        for i in range(n):
            # size grows with the case number: small cases first, so a counterexample is minimal
            size_i = 1 + (i * size) // max(n, 1)
            try:
                values = draw(size_i)
            except OutsideType:
                raise
            except GenError as e:
                if size_i < size:
                    unreachable = e     # a type out of reach at this size (a matrix of 3 rows at size 1)
                    continue
                raise
            except EvalError as e:
                if raised(e):           # the range of a parameter is computed, and the computation raised
                    skipped += 1
                    continue
                raise
            if values is None:
                continue
            try:
                b, r = evaluate(values)
            except EvalError as e:
                if raised(e):
                    skipped += 1
                    continue
                raise
            cases += 1
            record(values)
            if b is None:
                return stuck(values, r)
            if b is False:
                return result("sampled", cases, False, failure=show(values))
    except (GenError, EvalError) as e:
        return broken("sampled", e)
    if cases == 0 and skipped > 0:
        return result("sampled", 0, False, outcome=NOT_RUN,
                      error=f"the computation raised on every case drawn ({skipped}): no value to check")
    if cases == 0 and n > 0:
        return result("sampled", 0, False, outcome=NOT_RUN,
                      error=str(unreachable) if unreachable is not None else
                      "no case could be drawn: every draw met an empty domain")
    return result("sampled", cases, True)


class _Stuck(Exception):
    def __init__(self, values, term):
        self.values, self.term = values, term


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
                                         l.get("domains", []), l.get("sample_cases", []),
                                         l.get("outcome", "")))
        return report
    report.n = n
    report.mode = "exhaustive" if exhaustive else "sampled"
    report.fingerprint = fingerprint(checker.env, name, prefix)
    from .certify import cone
    report.provisional = [x for x in cone(checker.env, name) if x in checker.provisional]
    before = {k: list(v) for k, v in gens.checked.items()}
    from . import machine
    fell_before = dict(machine.fallbacks)
    for ob in checker.obligations.get(name, []):
        try:
            pieces = flatten(checker, ob)
        except Exception as e:
            report.laws.append(LawResult(ob.label, [], "sampled", 0, False, error=f"cannot flatten: {e}",
                                         outcome=NOT_RUN))
            continue
        for label, closed in pieces:
            started = time.perf_counter()
            result = run_law(checker, gens, label, closed, n, exhaustive, rng, show_cases, size,
                             of_type=ob.kind == "type")
            result.seconds = round(time.perf_counter() - started, 3)
            report.laws.append(result)
    checked = gens.checked_since(before)
    if checked:
        report.generation["registered_values"] = checked
    fell = {k: v - fell_before.get(k, 0) for k, v in machine.fallbacks.items() if v > fell_before.get(k, 0)}
    if fell:
        # evaluations the call-by-need machine left to the substitution evaluator (plan 4.3)
        report.generation["evaluator_fallbacks"] = fell
    report.generators = {k: generator_fingerprint(checker, k) for k in sorted(checked)}
    return report


