Review of bundle D, per file. Model files are taken under item 4 of their theory.

## `probability.lth` (with `probability_model.lut`)

1. **Wrong laws.** None false of the intended models. I checked the Gaussian formulas: `score` is the gradient of `loglik` with `u = u(t)`; `info = e^{-2u} J^T J + 2K g g^T` is E[s sᵀ] (the cross term has an odd moment, Var χ²_K = 2K), so it is the expected information; `ProfiledIsGaussianAtItsSigma` holds because `fixedSigma` zeroes the `g` term, leaving `(K/RSS) JᵀJ`. `GaussianPeaksAtMean`'s exact `>=` holds by monotone rounding as the comment says.

2. **Underdetermined.**
   - `IsGradient`: `else if nv == 0.0 then true` and `withinOf r.tol (1.0 + abs (f t) + nv) slope nv`. The slope is measured only along g's own direction and compared with g's norm, so any `g` with `dot (g t) (∇f t) == |g t|²` passes: the sphere of diameter 0…∇f, which contains `g := fn t { zeros n }` (and half the gradient plus an orthogonal vector of the same length). So `score := fn y t { zeros n }` is a model of `ScoreIsGradient`; the same hole is in `DLogSigmaIsGradient`, `PosteriorScoreIsGradient` (belief) and `GradIsGradient` (optimization). `IsJacobian` already does it right: a drawn `v`, the difference along `v` against `(j t) v̂`.
   - `Likelihood.info`: `InfoSymmetric` and `InfoNonNegative` are all that bind it. `info := fn y t { zeroMat n n }` is a model of `Likelihood n`; nothing relates it to `loglik` (a Bartlett identity needs the sampler the header defers). In the use, `laplaceAt` and `nu` in experiment_zero read it: a zero info returns the prior as posterior and is certified.
   - `InfoNonNegative` decides semidefiniteness by `dot v (matVec (l.info y t) v)` on drawn `v`. A matrix with one small negative eigenvalue fails only on the thin cone of `v` near that eigenvector, so it passes at any sampled level. arrays.lth §4 rejects this reading in its own words ("quadratic forms on a listed basis (do not decide semidefiniteness)") and states `PsdAt` through `retainedRank`; that leaf is imported here.

3. **Roles.** No `data` in the file; none.

4. **Models.** `numpySort`: `KolmogorovAgrees` is exact and `KolmogorovOfNothing` crosses an empty list; neither can be checked without `luthier.arrays.kolmogorov_distance` (not given; see "not sure"). `gaussian`, `profiled` against `Likelihood n`: pass as far as the laws go (item 1).

5. **Against the specification.**
   - 11.S14: `InfoNonNegative`'s `within tol q 0.0` is a flat tolerance on a sum of products whose rounding scales with Σ|v_i||M_ij||v_j|; arrays.lth moved its pinv laws to that scale (7032d7b). On the slice (JᵀJ of rank ≤ 22 in 30 dimensions) the null directions give q of order −eps·(K/RSS)·‖J‖²|v|²; it passes at tol = 1e-8 only because the magnitudes are modest.
   - `GaussianPeaksAtMean`, `ProfiledIsGaussianAtItsSigma`, `UniformAtLevel` are stated outside any `T :=` conjunction. By L10.6 a demand for `gaussian n m` pulls `Likelihood n`'s laws, not these, unless `test` runs every Bool definition (not sure).

6. **Implication over a type.** Only the vacuous branch of `IsGradient` (item 2). `KolmogorovOfOne`, `KolmogorovOfMultiset`, `UniformAtLevel` quantify over `UnitValue`/`UnitList` as they should. Note that `UnitList` says "in [0,1]", not "calibrated": what makes `UniformAtLevel` hold on 1 − α is the generator being uniform, which the certificate records (L9.6) and the type does not say.

7. **First change.** `IsGradient` with a drawn direction, as `IsJacobian`: the central difference along `v` against `dot (g t) v / nv`, the `nv == 0.0 → true` branch moved from `g` to `v`. Four laws across the three files pass through it and all admit a zero gradient.

8. **Cutoffs.** `tailSeriesTerms : Int := 100`, `tailSeriesFrom : Float64 := 0.2`: I agree with the file's reading. At x ≥ 0.2 the 100th term is exp(−800) and the branch at 0.2 moves the tail by 5e-13 (the theta form gives K(0.2) ≈ 5e-13, not the comment's 1e-13; immaterial); precision of a definition, not a criterion. `0.12`, `0.11` are Stephens's formula. In the use, not under review but where the parameters must arrive: `covFloor (n : Int) : RankFloor := toFloat64 n * doubles.epsilon` is a rank floor computed in the program while `lmFloor` comes by `--set`, and `bandLevel : Float64 := 0.05` is a level, which D-2026-10-14-c names explicitly.

## `belief.lth` (with `belief_model.lut`)

1. **Wrong laws.** `QuadraticConverges`: `r.converged and 0.5 * c * dot d d <= s.tol`. `d = sub r.x b` cannot fall below ≈ eps·|b| in doubles, so no maximizer satisfies the law when c > 2·tol/(eps|b|)² (tol = 1e-12, |b| ≈ 10: c ≳ 4e17), and before that LM's strict `pt < st.phi` starts rejecting, μ climbs past `most`, and the native model answers `stalled`, i.e. `converged = false`. Whether it bites depends on the generator of `Positive` (not sure). The subtype the law means is `(c, b)` with c·(eps|b|)² ≪ tol.

2. **Underdetermined.**
   - `MaximizerStationary`: `if r.converged then … else true`. A model returning `{ x := x0, converged := false }` on every posterior passes `MaximizerAscends`, `MaximizerStationary`, `MaximizerKeepsDimension` and fails only `QuadraticConverges`; a model that converges and reports `false` passes the same three. The `false` side of `converged` has no law, and `MaxResult n` carries nothing (iterations, reason) a law could tie it to. experiment_zero already assumes more than the theory gives: `"NOT CONVERGED: the maximizer ran out of its …"`, while the native driver also answers `false` for `stalled`.
   - `Posterior`: `PosteriorScoreIsGradient` (the `IsGradient` hole) and `PosteriorInfoSymmetric` only; no non-negativity, though `negate n p : Objective n` asks it of the same field. `decrement` reads `p.info`, so stationarity is relative to what the posterior claims: with `info := fn x { mscale 1e30 (identity n) }` every point is stationary, and a maximizer answering `x0` with `converged := true` passes `Maximizer` on it. Per-posterior certification is only as strong as the posterior's own laws.
   - `DensityPeaksAtMean`: the sampled quadratic form on drawn `t`, same low power on a nearly indefinite precision as probability item 2; `PsdAt` through `retainedRank` is the leaf form.

3. **Roles.** `MaxResult (n : Nat) = { x : VecOf n, converged : Bool }` is a product alias; `converged`'s role is half stated (true ⟹ decrement ≤ tol; quadratic ⟹ true). No sum `data`; none strictly.

4. **Models.** `lm` routes to `luthier.lm.maximize`, which the file says is unwritten; nothing to check, nothing contradicts the type. The native `lmMaximizer d` (optimization_model.lut) against `Maximizer`: passes `MaximizerAscends` (accepts only `pt < st.phi`, and `0.0 - p.logp x` negates exactly), `MaximizerStationary` (`finished` uses `<` on the same `decrement`; `scale (0.0 - 1.0) (p.score x)` is an exact negation, so `o.grad` gives the same value), `MaximizerKeepsDimension`, and `QuadraticConverges` in 3–4 accepted steps from `init = 1e-3`, subject to item 1's bound on `c`. With `init` near `most` it needs ~log₃(init) accepted steps before it moves; the demand's, not an error.

5. **Against the specification.** 11.S14 for `DensityPeaksAtMean`'s `within tol q 0.0`, as in probability item 5. Otherwise consistent with 7.R2, 7.R4, 10.S10, D-2026-10-14-c.

6. **Implication over a type.** `MaximizerStationary`'s premise is on the output, so no input subtype carries it; the remedy is a law for the other branch (item 9), not a subtype. `QuadraticConverges` quantifies over `(c : Positive)` correctly; item 1 for the subtype it means.

7. **First change.** Give `MaxResult` why the run stopped (optimization.lth's `Reason`, which `lmMaximizer` computes and then drops to a Bool) and the law `not converged ⟹ exhausted or stalled`, `exhausted` tied to `s.maxIter` through a count. It closes the give-up model of item 2, completes `converged`'s role, and gives experiment_zero the fact its summary already prints.

8. **Cutoffs.** None; every threshold is in `Settings`.

9. **Certifying the maximizer beyond the quadratic family.**
   - A family with a known maximum and a curvature that changes, so the damping path is exercised (on the quadratic no step is ever rejected): separable strictly concave, e.g. `logp x = −Σ c_i log cosh (x_i − b_i)`, score `−c_i tanh`, info `diag (c_i sech²)`; the Newton step overshoots for |x_i − b_i| ≳ 1, so steps are rejected and μ raised. Generators: `b, x0 : VecOf n`, `c : Positive` (or a vector of them), `n : Dim`; the law as `QuadraticConverges`, `r.converged` and |r.x − b| within what `s.tol` and the curvature at `b` give. The test checks the point, not the self-reported decrement.
   - A property of any posterior that does not go through `info`: at a stop reported converged there is no first-order ascent along a drawn direction, the central difference of `p.logp` along `v` at the demand's `Resolution` within tolerance of zero. Over the generator of `VecOf n` for `v`, per posterior for `p`. This is what `MaximizerStationary` means, read from `logp` instead of from the posterior's claimed curvature (item 2).
   - The budget law of item 7, over the generators of `MaximizerAscends`, once `MaxResult` says why it stopped.

## `optimization.lth` (with `optimization_model.lut`)

1. **Wrong laws.** None found false of the native model. `DirectionDescends` holds since `pinvSym` never retains a negative eigenvalue; `StepRule` holds of `lmStep` exactly (the same `dampedStep` expression on both sides; `mu * d.factor` and `lowered` identical); `QuadraticStepAccepts` holds from `start` while `init ≲ 1/eps` (beyond that `add st.x direction` rounds to `st.x` and `pt < phi` fails). The demand's `Damping`, so a note.

2. **Underdetermined.**
   - `StepRule`: acceptance is an implication, not an equivalence: `if s2.accepted then s2.phi < st.phi and …`. A `step` with `accepted := (o.value xt < st.phi) and (st.iter mod 2 == 0)` passes `StepRule` (the reject branch asks only that x, phi stay and mu, iter move), `DirectionDescends`, `DirectionAgrees` and `QuadraticStepAccepts` (iter is 0 at `start`). And `s2.phi` on acceptance is only bounded, never tied to the objective: `phi := pt - 1.0` passes. So the model file's "the step's laws determine the step from the direction, so agreement of the steps is a corollary" is not what the laws say: the direction and x are determined, `accepted` and `phi` are not. The rule meant is `s2.accepted == (o.value xt < st.phi)` with `xt := add st.x (m.direction …)`, and `s2.phi == o.value s2.x`.
   - `Objective.stepMatrix`: symmetric and non-negative only, by design per the header; the same low-power quadratic-form reading as the other files.

3. **Roles.** `Reason = { running : Unit || converged : Unit || exhausted : Unit || stalled : Unit }`: four constructors whose roles are stated by the branches of `finished` (a definition) and by no law; `isConverged (r : Reason) : Bool := match r { converged u -> true ; _ -> false }` is the accessor L2.7 excludes. `Run (n) = { state, reason }` likewise: no law says `(minimize …).reason == finished n s d o (minimize …).state` and is never `running`. Written as aliases, so L2.7 is formally met, but the roles exist: converged ⟺ `decrement < s.tol` at the state, exhausted ⟺ `iter >= s.maxIter`, stalled ⟺ `mu > d.most`.

4. **Models.** `native : LMStep` passes the four laws (`DirectionAgrees` trivially). `host` routes to unwritten code. `lmMaximizer`: belief item 4.

5. **Against the specification.** `optimization_model.lut`'s corollary claim (4.R10) contradicts `StepRule` as written (item 2). 11.S14 for `StepMatrixNonNegative` and `DirectionDescends`, as above.

6. **Implication over a type.** `StepRule (…) (st : LMState n)` quantifies over all states, `phi` free of `x`, `mu` free of the schedule, while it means the states a run visits: `{ st | st.phi == o.value st.x and d.least <= st.mu }`. On a random `st` the acceptance compares `o.value xt` with a number unrelated to the objective, so the branch taken is arbitrary and, since `o.value xt` is typically large against a drawn `phi`, the accept branch is the premise random cases rarely meet. `QuadraticStepAccepts`'s `norm (sub x0 b) == 0.0 or …` is a measure-zero guard, fine.

7. **First change.** `StepRule` as the equivalence of item 2 with `s2.phi == o.value s2.x`, over the subtype of item 6. It is the only law that makes the host's `step` Levenberg-Marquardt rather than a trial that sometimes accepts, and it makes the model file's corollary true.

8. **Cutoffs.** None; `Damping` and `Settings` carry every threshold. (`finished` stops at `<` where `MaximizerStationary` asks `<=`; consistent, the law weaker.)

## Not sure

- `within` / `withinOf` of numbers.lth taken as |a−b| ≤ tol(1+|a|+|b|) and |a−b| ≤ tol·scale, inferred from `approxMatSlack` and `approxMatSlackOf`; the 11.S14 items assume this.
- The generators of `VecOf n`, `Positive`, `Dim`, `UnitList`, `Level` (and that `Level` has `alpha`), and that `Settings`/`Damping` in laws are supplied by the demand rather than drawn; belief 1 and optimization 1 turn on these.
- The host code: whether `luthier.arrays.kolmogorov_distance` does `i/n` and `(i−1)/n` as the native definition (exactness of `KolmogorovAgrees`) and survives an empty list (`np.concatenate([])` raises); `luthier.lm.*` is unwritten.
- Whether Bool definitions outside a `T :=` conjunction are ever tested.
- `import "probability.lth" Kolmogorov Vec` in probability_model.lut: `Vec` is arrays.lth's; whether an import re-exports.
- `Dim` passing where `Nat` is asked (`Posterior n` with `n : Dim`).
- How a `Posterior n` built at run time (`laplacePosterior n l b y`) becomes a listed case under 7.R4.
- `profiled` at `dot r r == 0.0` (`ustar = −∞`, score NaN): unreachable on drawn `y`, reachable only if a fit reproduces every datum exactly.
- `IsGradient`'s scale `1.0 + abs (f t) + nv` adds f and |∇f| and omits 1/step, where the rounding of the quotient lives (≈ eps·|f|/step). Fine at v0.1's `cbrt eps`/`sqrt eps`; a demand that lowers `tol` without raising `step` would fail on rounding, not on the slope. A design remark, not checked against numbers.lth.

I can put this in a file (e.g. `review-D.md`) if you want it in the record.