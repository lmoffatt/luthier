# The fit's host side: report

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on `prompt.md`; saved by the coordinator.
Files: `src/luthier/lm.py` (new), `src/luthier/arrays.py` (`pinv_sym_at`), `src/luthier/run.py`
(three bridge gaps), `tests/test_lm.py` (new), `tests/test_run.py`, `tests/run/maximize_quadratic.lut`.
Checks: test_lm and test_run 77 passed, 1 skipped; the suite 562 passed. The source is
sonolocalización's `prototipo-cero/src/lm.py` (read only).

## What runs

- `pinv_sym_at(floor, a)`: eigh, keep `w > floor * max|w|`, none for an empty matrix.
- `lm.py`: `damped_step`, `step`, `decrement`, `finished`, `maximize`, plus `start`, `minimize`;
  mirrors optimization.lth operation for operation through arrays.py's leaves (`dot`, `mat_vec`,
  `madd`, `mscale`, `scale`, `add`, `pinv_sym_at`); settings, damping and state read by key or
  attribute; `DAMPING` (0.001, 3.0, 1e-15, 1e15) as [proposed] 9; `maximize` returns `{"x":
  ndarray, "converged": bool}`.
- `tests/run/maximize_quadratic.lut`: `lm` maximizes `quadratic 2 b 2.0` from the origin;
  `luthier run` prints `True`, `0.9999996671106302`, `-1.9999993342212603`; `x.run.json` records
  `{"python:luthier.lm.maximize": {"3": 3, "4": 5, "5": 5}}` (logp, score, info calls), equal to a
  direct Python run.
- No `test` lines in belief_model.lut or optimization_model.lut; nothing run by `luthier test`.

## Bridge gaps fixed in run.py (the port needs them)

1. Refined records (`Settings : U := { ... | law }`) stopped the run ("record refinements require
   check.py"): `run()` turns a refined record into a subtype of the record before elaborating,
   as the tester does (`tester._refined_records` imported lazily; belongs in run.py).
2. Type families: `resolve` did not unfold `VecOf n`; `family_applied` unfolds families defined
   into `U` and theories declared over parameters (`Objective n`, `Posterior n`); `Fin`, `Maybe`,
   `List` left alone (the bridge reads them by name).
3. A host result that is not a bool where `Bool` is declared is refused (11.S6).

## Each law, met and how (test_lm.py; seed 20261014, tol and floor 1e-12, 40 quadratics)

QuadraticConverges (every case, c|x-b|²/2 ≤ tol); MaximizerStationary (belief.lth's `decrement`
recomputed at the result ≤ tol, bit-equal to `lm.decrement` on the negated objective);
MaximizerAscends, MaximizerKeepsDimension (with `maxIter := 1` not converged); DirectionDescends
(mu from 1e-6 to 1e6); DirectionAgrees (bit-equal to dampedStep's formula in numpy; not against
the native definition, which needs the certification of `host : LMStep`); StepRule (both
branches); QuadraticStepAccepts; `finished`'s four reasons.

## Finding worth attention

The runner passes arguments unevaluated: with `r := lm.maximize ...` and `r` projected three
times, the maximizer ran three times (counts 9/15/15); only `match <call> { r -> ... }` evaluates
it once. In the experiment_zero port every projection of a `laplaceMode` result would rerun the
fit. (For run.py: a `Let`-bound call demanded once, 8.S4's call by need.)

Choices of the agent: integer codes in `finished` (no route reaches it); `DAMPING` a namespace;
`start` and `minimize` kept, `trace` dropped; `n` taken and ignored; the gradient and matrix
evaluated again at the same x as the source does (caching would change the counts); the run
program forces the result once with `match`; the three run.py changes.
