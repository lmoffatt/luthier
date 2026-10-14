"""Levenberg-Marquardt, the host side of optimization.lth and of belief.lth's `Maximizer`.

The successor in this repository (P7) of sonolocalización's prototipo-cero/src/lm.py, as the
fit theories' report asks (record/IA/slice-theories-2-2026-10-14/report.md, "What the bridge and
lm.py's successor must do, per extern"). Each function mirrors a definition of optimization.lth
operation for operation, through the same array leaves the definitions import from
arrays_model.lut (`dot`, `mat_vec`, `madd`, `mscale`, `pinv_sym_at`), so that the two compute
the same floats: `damped_step` is `dampedStep` (`DirectionAgrees`), `step` is `lmStep`
(`StepRule`), `decrement` is belief.lth's `decrement` (so that `MaximizerStationary` holds
exactly where `maximize` stopped), `finished` is `finished`.

What crosses (run.py, 3.S23, D-2026-10-14-a): the settings, the damping and a state arrive as
records, read here by key or by attribute; an objective as a record whose fields `value`,
`grad`, `stepMatrix` are callbacks taking a 1-d ndarray; vectors as 1-d ndarrays. A state given
back is a dict with x (ndarray), phi (float), mu (float), iter (int), accepted (bool).

Changes from the source: the pseudo-inverse at the settings' floor where the source solved the
matrix whole (belief.lth §2, [proposed] 6 and 8 of the report); the damping read from a record
(optimization.lth `Damping`) where the source held four constants; the settings one record where
the source took `tol` and `max_iter` apart ([proposed] 7).

Stopping reasons are coded as integers, as in the source: 0 running, 1 converged, 2 exhausted,
3 stalled (optimization.lth `Reason`, in the order of its alternatives).
"""
from __future__ import annotations

import os
import sys
from types import SimpleNamespace

import numpy as np

from luthier.arrays import add, dot, madd, mat_vec, mscale, pinv_sym_at, scale

# The method's own damping schedule, v0.1's muInit, muFactor, muMin, muMax (optimization.lut:29-32),
# the values `maximize` runs with ([proposed] 9 of the report: the damping is not a setting of
# the maximizer; if it becomes one, `maximize` reads it from the settings).
DAMPING = SimpleNamespace(init=0.001, factor=3.0, least=1e-15, most=1e15)

RUNNING, CONVERGED, EXHAUSTED, STALLED = 0, 1, 2, 3

# A trace of the iterations on the standard error, when the environment sets LUTHIER_LM_TRACE
# (a probe's instrument, record/IA/fit-convergence-2026-10-15/prompt.md): it reads values the
# method computes anyway and changes none.
_TRACE = bool(os.environ.get("LUTHIER_LM_TRACE"))


def _trace(*parts):
    if _TRACE:
        print("lm", *parts, file=sys.stderr, flush=True)


def _field(r, name):
    """A field of a record crossed from Luthier: a dict's key or an object's attribute."""
    return r[name] if isinstance(r, dict) else getattr(r, name)


def _vec(x):
    return np.asarray(x, dtype=float)


def start(n, o, damping, x0) -> dict:
    """optimization.lth `start`."""
    x0 = _vec(x0)
    return {"x": x0, "phi": float(o.value(x0)), "mu": float(_field(damping, "init")), "iter": 0,
            "accepted": True}


def damped_step(n, settings, o, x, mu):
    """optimization.lth `dampedStep`: -(M + mu diag M)^+ g at the settings' floor."""
    x = _vec(x)
    m = _vec(o.stepMatrix(x))
    damped = madd(m, mscale(mu, np.diag(np.diag(m))))
    return scale(0.0 - 1.0, mat_vec(pinv_sym_at(_field(settings, "floor"), damped), _vec(o.grad(x))))


def _lowered(damping, mu):
    """optimization.lth `lowered`: divided by the factor, not below the least."""
    factor, least = float(_field(damping, "factor")), float(_field(damping, "least"))
    return mu / factor if mu / factor > least else least


def step(n, settings, damping, o, s) -> dict:
    """optimization.lth `lmStep`: accept if the value falls, lowering the damping; else keep the
    point and the value and multiply the damping by the factor."""
    x, phi, mu, it = (_vec(_field(s, "x")), float(_field(s, "phi")), float(_field(s, "mu")),
                      int(_field(s, "iter")))
    dx = damped_step(n, settings, o, x, mu)
    xt = add(x, dx)
    pt = float(o.value(xt))
    _trace(f"iter={it + 1} phi={phi!r} trial={pt!r} step={float(np.linalg.norm(dx)):.6e} mu={mu:.3e}",
           "accepted" if pt < phi else "rejected")
    if pt < phi:
        return {"x": xt, "phi": pt, "mu": _lowered(damping, mu), "iter": it + 1, "accepted": True}
    return {"x": x, "phi": phi, "mu": mu * float(_field(damping, "factor")), "iter": it + 1,
            "accepted": False}


def decrement(settings, o, x) -> float:
    """belief.lth `decrement`: half of g^T M^+ g, the pseudo-inverse at the settings' floor. On
    the negated objective g is minus the score, and the value is the same to the last bit (a
    change of sign is exact and rounds symmetrically)."""
    x = _vec(x)
    g = _vec(o.grad(x))
    return 0.5 * dot(g, mat_vec(pinv_sym_at(_field(settings, "floor"), _vec(o.stepMatrix(x))), g))


def finished(settings, damping, o, s) -> int:
    """optimization.lth `finished`: converged by the decrement, exhausted by the budget, stalled
    by the damping beyond its most; running otherwise."""
    dec = decrement(settings, o, _field(s, "x"))
    _trace(f"iter={int(_field(s, 'iter'))} decrement={dec:.6e}")
    if dec < float(_field(settings, "tol")):
        return CONVERGED
    if int(_field(s, "iter")) >= int(_field(settings, "maxIter")):
        return EXHAUSTED
    if float(_field(s, "mu")) > float(_field(damping, "most")):
        return STALLED
    return RUNNING


def minimize(n, settings, damping, o, s):
    """optimization.lth `minimize`, as a loop: the final state and its stopping reason."""
    while True:
        r = finished(settings, damping, o, s)
        if r != RUNNING:
            return s, r
        s = step(n, settings, damping, o, s)


def maximize(settings, n, f, g, m, x0) -> dict:
    """belief.lth's `Maximizer`: the maximum of f on the vectors of dimension n, by minimizing its
    negative (optimization.lth `negate`) from x0 with the module's damping."""
    o = SimpleNamespace(value=lambda x: 0.0 - float(f(x)),
                        grad=lambda x: scale(0.0 - 1.0, _vec(g(x))),
                        stepMatrix=lambda x: _vec(m(x)))
    s, code = minimize(n, settings, DAMPING, o, start(n, o, DAMPING, x0))
    return {"x": s["x"], "converged": code == CONVERGED}
