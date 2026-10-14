## probability.lth

1. **Laws that are wrong** — None found from the file alone; `GaussianPeaksAtMean`, `ProfiledIsGaussianAtItsSigma`, and the Kolmogorov laws match their stated definitions.

2. **Laws that do not determine what they claim** — `IsGradient` is vacuous when `g t = 0`:  
   `else if nv == 0.0 then true`.  
   A wrong model with `g t = zeros n` for every `t` passes `IsGradient` for any `f`; `ScoreIsGradient` then passes for any `loglik`.

3. **Roles (L2.7)** — None: `MeanModel`, `ScaledModel`, `Likelihood`, and `Kolmogorov` each have laws over their parts.

4. **The models against their theories** — `probability_model.lut` is the model file; see below.

5. **Against the specification** — `KolmogorovAgrees` states exact agreement with the native definition as a law:  
   `KolmogorovAgrees (d : Kolmogorov) (vs : UnitList) : Bool := d.distance vs == kolmogorovDistanceDef vs`.  
   The file cites 4.R10, which says agreement with a native definition is a corollary, not a law.

6. **Implication over a type** — `IsGradient` again: the zero-gradient branch makes the law trivial for random cases where `g t = 0`; it should quantify over a direction `v`, as `IsJacobian` does.

7. **What you would change first** — Rewrite `IsGradient` to take a drawn direction `v` and test along `v`, not along `g t`, because the current zero branch lets any zero score pass.

8. **Cutoffs** — `tailSeriesTerms : Int := 100` and `tailSeriesFrom : Float64 := 0.2` are constants. The file argues they are precision, but under D-2026-10-14-c any cutoff should be a demand parameter.

9. **Certifying the maximizer** — Not in this file.

## probability_model.lut

1–9. No law in the file; it is a model. I cannot verify the host’s `luthier.arrays.kolmogorov_distance` from the bundle, so I cannot confirm `KolmogorovAgrees` is exact. Put in “not sure”.

## belief.lth

1. **Laws that are wrong** — `QuadraticConverges` requires convergence for every `Settings`, including tiny budgets:  
   `r.converged and 0.5 * c * dot d d <= s.tol`.  
   A correct LM with `s.maxIter = 1` and a distant start will return `converged = false`; the law is false of the intended model.

2. **Laws that do not determine what they claim** — `MaximizerStationary` is vacuous when `r.converged` is false:  
   `if r.converged then decrement ... <= s.tol else true`.  
   A maximizer that always returns `converged = false` and `x = x0` satisfies this law, but not `QuadraticConverges`.

3. **Roles (L2.7)** — None: `GaussianBelief`, `Posterior`, and `Maximizer` have laws.

4. **The models against their theories** — `belief_model.lut` is the model file; see below.

5. **Against the specification** — None found.

6. **Implication over a type** — `MaximizerStationary` is an implication whose premise `r.converged` a random case rarely meets; the subtype should be the converged runs.

7. **What you would change first** — Weaken `QuadraticConverges` so it does not demand convergence for budgets that are too small, e.g. restrict it to settings with a sufficient iteration budget or state it over a fixed sufficient budget.

8. **Cutoffs** — `Settings` has `tol`, `maxIter`, `floor` as parameters; no constant cutoff found here.

9. **Certifying the maximizer** — Missing law: a convergence law on a non-quadratic family. A test could check that on a generator of non-quadratic posteriors with a known unique maximum (e.g. the nonlinear mean model of `positions.lut`, or a logistic posterior), the maximizer returns `r.converged = true` and the decrement at `r.x` is within `s.tol`, or that `p.logp r.x` is within tolerance of the known maximum.

## belief_model.lut

1–9. Model file. The host extern `luthier.lm.maximize` is not in the bundle, so I cannot verify it. If the host respects `maxIter`, it will break `QuadraticConverges` for small budgets, but that is a consequence of the law in `belief.lth`. Put host behaviour in “not sure”.

## optimization.lth

1. **Laws that are wrong** — None found in `Objective`, `Damping`, `LMStep`; `QuadraticStepAccepts` is true for the native LM on a concave quadratic.

2. **Laws that do not determine what they claim** — `GradIsGradient` inherits the `IsGradient` zero-gradient weakness:  
   `GradIsGradient (n : Nat) (o : Objective n) (r : Resolution) (x : VecOf n) : Bool := IsGradient n r o.value o.grad x`.

3. **Roles (L2.7)** — `Reason` has no law of its constructors’ roles:  
   `Reason = { running : Unit || converged : Unit || exhausted : Unit || stalled : Unit }`.  
   This is a `data` with four constructors and no role law.

4. **The models against their theories** — `optimization_model.lut` is the model file; see below.

5. **Against the specification** — None found.

6. **Implication over a type** — None major.

7. **What you would change first** — Add a law for `Reason` stating the role of `converged`, `exhausted`, `stalled`, `running`, per L2.7.

8. **Cutoffs** — `Damping` and `Settings` are parameters; no constant cutoff found here.

9. **Certifying the maximizer** — Not in this file.

## optimization_model.lut

1–9. Model file. `native` is the native LM; `host` is extern. I cannot verify the host. `lmMaximizer` breaks `QuadraticConverges` for small `maxIter` if the driver respects the budget. Put host behaviour in “not sure”.

## arrays.lth

1. **Laws that are wrong** — None found from the file alone; the laws are consistent with the definitions as written.

2. **Laws that do not determine what they claim** — `pinvSym`/`retainedRank` drop negative eigenvalues:  
   `pinvOfDiagonal ... if d.f k > fl * big then 1.0 / d.f k else 0.0`.  
   On an indefinite symmetric matrix, a wrong model that returns zero for negative-definite matrices passes `PinvProjects`, `PinvSymmetric`, and `PinvTraceIsRank` when the retained rank is zero, but it is not the pseudo-inverse.

3. **Roles (L2.7)** — None: `Vec` and `Mat` are aliases; `Arrays` has laws.

4. **The models against their theories** — `arrays_model.lut` is not in the bundle; cannot check.

5. **Against the specification** — Many laws restate exact agreement with native definitions as laws, e.g.  
   `AddPointwise ... := approxVec exact (m.add x y) (addDef x y)`.  
   The file cites 4.R10, which says agreement is a corollary, not a law.

6. **Implication over a type** — None major.

7. **What you would change first** — Restrict `Symmetric` to positive semidefinite matrices, or make `pinvSym` retain negative eigenvalues, because the current laws underdetermine the pseudo-inverse on indefinite matrices.

8. **Cutoffs** — `ClearFloor : U := { f : RankFloor | f < 0.001 }` and `ClearDiagonal` with `1.0 <= abs (d.f k) and abs (d.f k) <= 1000.0` are constants. If these are cutoffs, D-2026-10-14-c says they should be demand parameters.

9. **Certifying the maximizer** — Not in this file.

## not sure

- The host code for `luthier.arrays.kolmogorov_distance`, `luthier.lm.maximize`, `luthier.lm.damped_step`, and `luthier.lm.step` is not in the bundle, so I cannot verify exact agreement or law satisfaction.
- `arrays_model.lut` is not in the bundle, so I cannot check the `numpy` model of `Arrays`.
- Definitions of `withinOf`, `Positive`, `Tolerance`, `RankFloor`, `Level`, and the exact semantics of `pinvSym`/`retainedRank` in `numbers.lth` and `arrays.lth` are not fully given here, so some tolerance and rank statements cannot be checked to the last detail.