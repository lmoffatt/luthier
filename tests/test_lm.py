"""lm.py, the host's Levenberg-Marquardt, against the laws of belief.lth §2 and optimization.lth §3
(record/IA/fit-host-2026-10-14/prompt.md; the report record/IA/slice-theories-2-2026-10-14/
report.md, "What the bridge and lm.py's successor must do"). The concave quadratic of belief.lth,
`quadratic n b c`, is the family with generators (`VecOf n`, `Positive`): it is sampled here with
a fixed seed. One run goes through `luthier run`, the callbacks counted in its record (12.S18)."""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from luthier import lm
from luthier.arrays import dot, mat_vec, pinv_sym_at

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261014
SETTINGS = {"tol": 1e-12, "maxIter": 100, "floor": 1e-12}


def quadratic(b, c):
    """belief.lth's `quadratic n b c`: logp, score, info of the concave quadratic with its maximum
    at b and curvature c."""
    b = np.asarray(b, dtype=float)
    return SimpleNamespace(logp=lambda x: 0.0 - 0.5 * c * dot(x - b, x - b),
                           score=lambda x: (0.0 - c) * (x - b),
                           info=lambda x: c * np.eye(b.size))


def negate(p):
    """optimization.lth's `negate`: the objective that minimizes the negative of a log posterior."""
    return SimpleNamespace(value=lambda x: 0.0 - p.logp(x), grad=lambda x: (0.0 - 1.0) * p.score(x),
                           stepMatrix=p.info)


def cases(count=40):
    """(n, b, c, x0) of the quadratic family, n a `Dim`, c `Positive`."""
    rng = random.Random(SEED)
    for _ in range(count):
        n = rng.randint(1, 6)
        b = np.array([rng.uniform(-10, 10) for _ in range(n)])
        x0 = np.array([rng.uniform(-10, 10) for _ in range(n)])
        yield n, b, 10 ** rng.uniform(-3, 3), x0


def belief_decrement(settings, p, x):
    """belief.lth's `decrement` on the log posterior itself (the score, not its negative)."""
    g = p.score(x)
    return 0.5 * dot(g, mat_vec(pinv_sym_at(settings["floor"], p.info(x)), g))


def test_pinv_sym_at_keeps_what_is_above_the_floor():
    # arrays.lth's PinvOfDiagonal, PinvOfZero: 1 / w above floor * max |w|, zero elsewhere
    d = np.array([4.0, 1e-14, -2.0, 0.5])
    assert np.array_equal(pinv_sym_at(1e-12, np.diag(d)), np.diag([0.25, 0.0, 0.0, 2.0]))
    assert np.array_equal(pinv_sym_at(1e-12, np.zeros((3, 3))), np.zeros((3, 3)))
    assert pinv_sym_at(1e-12, np.zeros((0, 0))).shape == (0, 0)


def test_quadratic_converges_and_the_decrement_is_the_beliefs():
    # QuadraticConverges, and MaximizerStationary, MaximizerAscends, MaximizerKeepsDimension on
    # the quadratic: the decrement recomputed from the posterior is the one lm stopped by, exactly
    for n, b, c, x0 in cases():
        p = quadratic(b, c)
        r = lm.maximize(SETTINGS, n, p.logp, p.score, p.info, x0)
        assert r["converged"] is True
        d = r["x"] - b
        assert 0.5 * c * dot(d, d) <= SETTINGS["tol"]
        assert belief_decrement(SETTINGS, p, r["x"]) <= SETTINGS["tol"]
        assert belief_decrement(SETTINGS, p, r["x"]) == lm.decrement(SETTINGS, negate(p), r["x"])
        assert p.logp(r["x"]) >= p.logp(x0)
        assert r["x"].shape == (n,)


def test_a_budget_spent_is_not_converged():
    p = quadratic(np.array([1.0, -2.0]), 2.0)
    r = lm.maximize({"tol": 1e-12, "maxIter": 1, "floor": 1e-12}, 2, p.logp, p.score, p.info, np.zeros(2))
    assert r["converged"] is False


def test_the_damped_step_descends_and_agrees():
    # DirectionDescends; DirectionAgrees with optimization.lth's dampedStep written out here
    rng = random.Random(SEED + 1)
    settings = SimpleNamespace(**SETTINGS)  # the settings by attribute, as by key above
    for n, b, c, x in cases():
        o = negate(quadratic(b, c))
        mu = 10 ** rng.uniform(-6, 6)
        delta = lm.damped_step(n, settings, o, x, mu)
        q = dot(o.grad(x), delta)
        assert q <= 0.0 or abs(q) <= 1e-12
        m = o.stepMatrix(x)
        native = (0.0 - 1.0) * (pinv_sym_at(SETTINGS["floor"], m + mu * np.diag(np.diag(m))) @ o.grad(x))
        assert np.array_equal(delta, native)


def test_a_step_on_the_quadratic_is_accepted():
    # QuadraticStepAccepts, and StepRule's accepted branch: the point along the direction, the
    # damping lowered by the schedule, the iteration counted
    damping = lm.DAMPING
    for n, b, c, x0 in cases():
        o = negate(quadratic(b, c))
        s = lm.start(n, o, damping, x0)
        s2 = lm.step(n, SETTINGS, damping, o, s)
        assert s2["accepted"] is True
        assert s2["phi"] < s["phi"]
        assert np.array_equal(s2["x"], s["x"] + lm.damped_step(n, SETTINGS, o, s["x"], s["mu"]))
        assert s2["mu"] == max(s["mu"] / damping.factor, damping.least)
        assert s2["iter"] == s["iter"] + 1


def test_a_step_that_does_not_fall_is_rejected():
    # StepRule's rejected branch: point and value kept, damping times the factor, iteration counted
    damping = {"init": 0.001, "factor": 3.0, "least": 1e-15, "most": 1e15}
    o = negate(quadratic(np.array([1.0, -2.0]), 2.0))
    s = {"x": np.zeros(2), "phi": -1.0, "mu": 0.5, "iter": 4, "accepted": True}
    s2 = lm.step(2, SETTINGS, damping, o, s)
    assert s2["accepted"] is False
    assert np.array_equal(s2["x"], s["x"]) and s2["phi"] == s["phi"]
    assert s2["mu"] == 1.5 and s2["iter"] == 5


def test_finished_reads_the_decrement_the_budget_and_the_damping():
    o = negate(quadratic(np.array([1.0]), 1.0))
    at = {"x": np.array([1.0]), "phi": 0.0, "mu": 1.0, "iter": 0, "accepted": True}
    away = dict(at, x=np.array([0.0]))
    assert lm.finished(SETTINGS, lm.DAMPING, o, at) == lm.CONVERGED
    assert lm.finished(SETTINGS, lm.DAMPING, o, away) == lm.RUNNING
    assert lm.finished(SETTINGS, lm.DAMPING, o, dict(away, iter=100)) == lm.EXHAUSTED
    assert lm.finished(SETTINGS, lm.DAMPING, o, dict(away, mu=1e16)) == lm.STALLED


def test_luthier_runs_the_host_maximizer_through_the_callbacks(tmp_path):
    # belief_model.lut's `lm` maximizes belief.lth's quadratic (b = (1, -2), c = 2, from the
    # origin); the host calls logp, score and info back, each call counted in x.run.json
    path = tmp_path / "maximize_quadratic.lut"
    path.write_text((ROOT / "tests/run/maximize_quadratic.lut").read_text(encoding="utf-8"), encoding="utf-8")
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    result = subprocess.run([sys.executable, "-m", "luthier.cli", "run", str(path)],
                            env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    converged, x, y = result.stdout.split()
    assert converged == "True"
    assert 0.5 * 2.0 * ((float(x) - 1.0) ** 2 + (float(y) + 2.0) ** 2) <= 1e-12
    runs = json.loads((tmp_path / "maximize_quadratic.run.json").read_text(encoding="utf-8"))
    # the same run in Python, its callbacks counted: logp at the start and at each trial; score
    # and info at each `finished` and each step
    counts = {"logp": 0, "score": 0, "info": 0}
    p = quadratic(np.array([1.0, -2.0]), 2.0)

    def counted(name, f):
        def call(x):
            counts[name] += 1
            return f(x)
        return call
    lm.maximize(SETTINGS, 2, counted("logp", p.logp), counted("score", p.score), counted("info", p.info),
                np.zeros(2))
    assert runs[-1]["calls"] == {"python:luthier.lm.maximize": {
        "3": counts["logp"], "4": counts["score"], "5": counts["info"]}}
