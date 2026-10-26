# Night of 2026-10-26, Agent V: convergence and vacuity (D-2026-10-16-m)

Claude Opus 5.5, on `prompt-night-2026-10-26.md` beside this file, on the queue item of record/plan/code-follows-principles-2026-10-16.md (line 167) and on D-2026-10-16-m. Vacuity itself was done by wave A's A3 (report-wave-a-3.md, 7e06717); this bite uses it. Base commit b21f2da. Commits: bc4e274 (theories, models, host and consumers), c450af7 (test programs), 5929f41 (the queue item marked done). Scratch under `~/.cache/luthier-night/V/` (the stress script and run outputs). Committed by the coordinator from the agent's hand-back (its Write was refused).

## What changed

- belief.lth, the result type: `StopReason` moved here from optimization.lth, without `running` (a run that has not stopped has no reason): `converged || exhausted || stalled`, with `isConverged`. `MaxResult n` is `{ x, reason, steps }` (was `{ x, converged }`); every result records its step count (D-2026-10-16-m, L6.3). `Maximizer` gains `quadraticSteps : Settings -> Float64 -> Nat`, the iterations within which the method stops converged on the concave quadratic family, as a function of the start's decrement: each method states its own cost (Newton 1, LM a handful, gradient about kappa log(dec/tol)), never a constant (P11: every criterion is a parameter).
- `MaximizerStationary` lost its `else true`: it checks every reason against the posterior, recomputed: converged, the decrement within the tolerance; exhausted, the budget spent and the decrement not within it; stalled, the budget not spent and the decrement not within it; always no more steps than the budget. No case is vacuous any more, so a maximizer that gives up everywhere is refuted.
- `QuadraticConverges` lost `if s.maxIter < budget then true` and the demand's `budget` (50). Its domain is `quadraticReachable fp s n b c` (`c epsilon^2 |b|^2 / 2 < tol`: the quadratics whose decrement within one ulp of b is below the tolerance), `fp` the doubles bound by census to numbers_model.lut's `doubles`. [proposed] On that domain a maximizer stops within `mx.quadraticSteps` at the start's decrement: converged at b within the tolerance, or, when the budget is below the bound, exhausted at the budget; a stall is a failure. The premise is on the drawn problem, so the held count measures how much the law was asked: 100 of 100 on every line.
- optimization.lth: `finished` gives `Maybe StopReason`; `minimizeBy` drives any model's step, `minimize` is `minimizeBy lmStep`. A new §4 [proposed]: `lmQuadraticSteps d tol dec mu k`, the count derived from the definitions (on c I the damped step multiplies the distance by mu/(1+mu) and the decrement by its square, the damping lowered by the schedule); `lmQuadraticBound d s dec` that count plus one step for rounding; the law `LMStepsOnQuadratic` (claimed in `LMStepOnQuadratic`) drives a model of the step on the domain with the budget above the bound and asks the run to stop converged within one step of the count either way, so a padded bound is refuted as well as a slow run.
- Models: `lmMaximizer d` gives the run's reason and iterations and declares `lmQuadraticBound d`; belief_model.lut's `lm` declares `lmQuadraticBound hostDamping`, `hostDamping` writing lm.py's `DAMPING` (0.001, 3, 1e-15, 1e15) in Luthier, so a drift between the two shows in `LMStepsOnQuadratic` on `hostStep` and `QuadraticConverges` on `lm`.
- Consumers changed with `MaxResult`: lm.py's `maximize` returns `reason` as `(label, None)` (how a sum crosses in run.py) and `steps`; examples/sonolocalizacion/experiment_zero.lut reads `isConverged mode.reason` (one line); tests/run/maximize_quadratic.run.lut and maximize_shared.run.lut print `isConverged r.reason`; tests/test_lm.py checks the reason and the steps, its constant `iter <= 3` replaced by the derived count within one step.

## Checks

- Before and after, on a baseline worktree at 4e1a68b: the control `giveUp` on `MaximizerStationary` gave "not run: vacuous: no premise held in the 20 cases" (the old law could not see a maximizer that gives up); now refuted. `QuadraticConverges` under a budget of one iteration passed "sampled" with nothing asked; now it asks the run to stop exhausted at the budget, which holds on `lm`.
- belief_laws.test.lut: every line gives the same outcome as before; the two new lines (`QuadraticConverges`, `MaximizerStationary` under `settingsOne`) supported over 100 cases; the three session A fit lines supported. belief_controls.test.lut: all 11 controls refuted, new ones `slowLM`, `giveUp` and `stallsAtMaximum`. fit_laws.test.lut: all 13 lines supported, including `LMStepsOnQuadratic` on `hostStep` and `native`. fit_controls.test.lut: all 8 controls refuted (`neverAccepts` under `settingsTwenty`, finding 2; `newtonStep`, one undamped step, fewer than the count). optimization_laws/controls: all supported but `StepMatrixSymmetric` on session A, unsettled with 0 cases (finding 1); all 7 controls refuted.
- Stress test of the derivation in Python against lm.py (stress.py): 20000 draws (dimensions 1 to 30, b, c and the start over 16 decades, tolerances 1e-14 to 1e-2), and two runs with 70% of tolerances just above the floor: no failure; steps equal the count except, in the tightest run, 49 cases at +1 and 62 at -1, hence the one-step allowance either way.
- `luthier check` clean on every file touched. pytest: test_lm.py 9 passed, 1 failed; test_run.py maximize selection 37 passed, 1 failed: both `luthier run` refusing an uncertified cone (`lm` stale since bc4e274, numpy since 40f6b89); with the gate off in a scratch script the three fixture runs print the same output as before. Both should pass after re-certification.

## Findings

1. Recursion-depth errors on session A: `PrecisionSymmetric` (on `priorA`) and `PosteriorInfoSymmetric` (on `posteriorA`) raise "maximum recursion depth exceeded" under `luthier test --no-cert`, the same at 4e1a68b; `StepMatrixSymmetric` on session A's objective is unsettled with 0 cases, probably the same failure on the same 30 by 30 matrices.
2. The native driver recurses once per iteration; a run of 500 iterations exceeds the evaluator's depth (hence the never-accepting control under a budget of 20).
3. experiment_zero.lut's summary says "the maximizer ran out of its N iterations" whenever the fit did not converge; the result now says exhausted or stalled and after how many steps, but `Fit` keeps neither: a one-line follow-up.
4. Stale comments in tester.py at the vacuity judge (around lines 1342 and 1388) still cite `MaximizerStationary`'s `else true`.
5. No gradient maximizer exists, so the kappa log(dec/tol) bound is only a comment.

## Decisions taken on my own

1. The cost bound is a field of the model (`Maximizer.quadraticSteps`), not a census parameter of the law.
2. `StopReason` has no `running` and lives in belief.lth; `finished` gives `Maybe StopReason`.
3. `MaxResult` replaces `converged` with `reason` and `steps`; consumers updated.
4. The domain is the format's floor at b, with `fp : Doubles Float64` as a law parameter.
5. The rounding allowance is one step (bound the count plus one; `LMStepsOnQuadratic` accepts count ± 1), derived in comments and stress-tested.
6. A new law `LMStepsOnQuadratic` over `LMStep` through `minimizeBy`.
7. `MaximizerStationary` keeps its name though it now checks every reason.
8. `hostDamping` repeats lm.py's constants.
9. New test lines `settingsOne` and `settingsTwenty`.

## Question

Should the cost bound stay a field of each maximizer, or be a function the demand binds per method?

Coordinator's answer (2026-10-26): the field. The model states its own scaling (D-2026-10-18-d: the laws of the algorithms say how the budget scales), and a law like `LMStepsOnQuadratic` guards each method's bound against padding.
