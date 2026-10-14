# The fit converges linearly, halving each iteration: find the cause, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). Luciano, 05:10: "400
iteraciones? suena muchísimo, para un esquema de optimización de distancias euclidianas la
última vez eran no más de 10. Bad smell." The second port's report
(`record/IA/slice-port-2-2026-10-14/report.md`, "Behind it") said: the fit on session A's graph
converged in 59 Levenberg-Marquardt iterations and "the change halves each iteration from
iteration 26 on". Linear convergence with factor one half on a near-zero-residual problem,
where LM should be quadratic (v0.1: at most 10 iterations), smells of a factor of two between
the gradient and the step matrix (the Newton step halved), or of a damping that never falls.

## The prompt

Read `CLAUDE.md` first, then that report section, `src/luthier/lm.py` (the step, `lowered`,
the damping, `decrement`, `finished`), `src/luthier/lib/optimization.lth` §2 (`dampedStep`,
`lmStep`), `belief.lth` (`laplaceMode`, `laplacePosterior`, `gaussianLogDensity`, `decrement`),
`probability.lth` (`gaussian`, `profiled`: the score and the information of the Gaussian
likelihood; `IsGradient`, `IsJacobian`), `examples/sonolocalizacion/experiment_zero.lut`
(`laplaceMode`'s arguments: the log posterior, its score, its information; `runSettings`) and
`positions.lut` / `distances.lut` (the mean model and its Jacobian). Read only in
sonolocalización: `prototipo-cero/src/lm.py` (v0.1's maximizer) and v0.1's `belief.lut`,
`probability.lut` at the tag `v0.1-final` here (`git show v0.1-final:src/luthier/lib/belief.lut`)
for how the score and the information were built there. Nobody else edits now: you may change
`src/luthier/lm.py`, `tests/test_lm.py`, and write a probe under the session scratchpad; the
theories and the port only if the cause is plainly a wrong factor there (then one commit per
file with explicit paths, `[proposed]`, saying why; else report).

1. Instrument: run the fit on `graph_noA2` (`--set graphDir=examples/sonolocalizacion/A/graph_noA2
   --set outDir=/tmp/x --set lmMaxIter=500 --set lmTol=1e-12 --set lmFloor=5.995204332975845e-15
   --fuel 100000000000`, 2 to 4 minutes) with lm.py printing per iteration (to stderr, behind an
   environment variable): iteration, phi, |step|, mu, the decrement, accepted or not. Paste the
   table (abridged). How many iterations until convergence, and how does |step| fall?
2. Check consistency at the converged point and at the start: cross the three callbacks out of
   the Runner (or recompute them in Python from the port's definitions through `luthier eval`,
   or through a probe calling the Runner): is the information matrix the negative Hessian of
   the log posterior? Compare `info(x)` with the finite-difference Jacobian of `score(x)`, and
   `score(x)` with the finite-difference gradient of `logp(x)`; report the ratios (a clean
   factor of 2 in one of them is the smell). Check the prior's precision enters both the score
   and the information, and the likelihood's `1/sigma²` enters both the same way, including the
   profiled sigma (`profiled`: with sigma eliminated the score and information change).
3. Check the damping: with an accepted step mu is divided by 3 from 0.001; how does mu evolve in
   the table? Is the step ever the full Gauss-Newton step? Compare with v0.1's lm.py (its mu
   schedule and its step).
4. Report the cause with the evidence, and what fixes it (which file, which law); if it is a
   bug in lm.py, fix it with a test that a near-zero-residual quadratic-like problem converges
   in few iterations (the quadratic family converges in one step from anywhere under LM with mu
   small: assert the iteration count), and rerun the fit: paste the iteration count and the
   summary line.

Check: `PYTHONPATH=src python3 -m pytest tests/test_lm.py -q`. Report in your final message.
