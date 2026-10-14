I treated the six `probability/belief/optimization` theory/model files as the review targets; `arrays.lth` as a dependency and `experiment_zero.lut` as the required use-site, as the prompt instructs. D-prompt

## `probability.lth`

1. **Laws that are wrong.**  
   The serious one is the declared totality of `profiled` and `ProfiledIsGaussianAtItsSigma`. The file admits every `MeanModel.k : Nat`, including zero, and every `y : VecOf m.k`; but `profiled` divides by both `k` and `RSS = dot r r`, and the comparison law computes `log(RSS/k)`. At an exact fit, `RSS = 0`; at `k = 0`, both are zero. The score has `k/RSS`, and `ustar` is `0.5 * log(RSS/k)`. Thus an exact fit does not produce a valid `Float64` score/information and the claimed `Likelihood` is not defined on its whole stated domain. D-prompt `Float64` is explicitly the **finite** IEEE doubles, so `-inf`/`NaN` cannot silently be values of the declared type. D-prompt

2. **Laws that do not determine what they claim.**  
   "`else if nv == 0.0 then true`" in `IsGradient` is fatal. A proposed gradient identically equal to zero passes for *every function*, including a nonconstant one. D-prompt Therefore a completely wrong likelihood can pass all of `Likelihood`: let `loglik(y,t)=t₀`, `score(y,t)=0`, and `info(y,t)=0`. Shapes pass; `ScoreIsGradient` passes through the zero branch; zero information is symmetric and nonnegative. D-prompt

   Independently, the laws call `info` “Fisher information” but only require symmetry and nonnegativity; no law connects it to the likelihood/score. So even after fixing `IsGradient`, `info ≡ 0` remains a legal “Fisher information” for every likelihood. D-prompt

   A smaller domain hole: `Kolmogorov.distance` has domain `List (Vec Float64)`, while its characterizing agreement law covers only `UnitList`. A specimen may behave arbitrarily on values outside `[0,1]` and still satisfy every law. If the intended concept only exists on uniform-valued inputs, the field itself should expose that domain. D-prompt

3. **Roles (L2.7).**  
   No offending `data` constructor in this file.

4. **The model against the theory.**  
   I cannot establish a break of `numpySort : Kolmogorov` from the supplied material because the Python body of `luthier.arrays.kolmogorov_distance` is not included. The exact-agreement requirement is therefore unverified, not disproved.

5. **Against the specification.**  
   The singular profile likelihood conflicts with the finite-`Float64` specification as above. Also the tail approximation deliberately keeps cutoffs in the file, contrary to D-2026-10-14-c/P11; see item 8.

6. **Implication over a type.**  
   No main instance of the specific “rare premise → true otherwise” anti-pattern. The `nv == 0 -> true` branch is worse: it is an output-controlled escape hatch, but the right repair is to change the gradient test, not merely introduce a subtype.

7. **What I would change first.**  
   `IsGradient`. It currently invalidates the meaning of `MeanModel`, `ScaledModel`, `Likelihood`, `Posterior`, and `Objective` downstream. Test the claimed gradient against an independently generated direction, as `IsJacobian` already does, rather than choosing the test direction from the claimed gradient itself.

8. **Cutoffs.**  
   "`tailSeriesTerms : Int := 100`" and "`tailSeriesFrom : Float64 := 0.2`" are precisely truncation/switch cutoffs controlling the approximation. The comment argues that they are not demand criteria, but D-2026-10-14-c says cutoffs are parameters and “never a constant in a file.” D-prompt D-prompt

9. **Certifying the maximizer.**  
   N/A here.

---

## `probability_model.lut`

1. **Laws wrong.** None in the model file itself.

2. **Underdetermination.** Inherited from `Kolmogorov`; the model does not cause it.

3. **Roles.** None.

4. **Model against theory.** No failure can be demonstrated without the Python implementation. In particular, `KolmogorovAgrees` demands exact equality, so the claim that the host performs exactly the same operations remains something certification must actually establish.

5. **Against specification.** None independently established.

6. **Implication over type.** None.

7. **Change first.** Nothing here before fixing `probability.lth`; otherwise the model would be certified against the wrong contract.

8. **Cutoffs.** None.

9. **Maximizer.** N/A.

---

## `belief.lth`

1. **Laws that are wrong.**  
   "`QuadraticConverges`" is too strong. Its own comment says convergence occurs with a budget “that is not tiny,” yet the law quantifies over every `Settings`, whose only budget restriction is `maxIter > 0`. Thus `maxIter = 1` is included. D-prompt D-prompt A genuine iterative LM need not converge from an arbitrary start in one iteration.

   There is also a type-level error in the Laplace constructors: `laplacePosterior`, `laplaceMode`, `laplaceAt`, and `laplaceUpdate` accept `y : Vec Float64`, although the laws of a `Likelihood` are guaranteed only for `y : VecOf l.k`. Therefore these definitions claim `Posterior`/`GaussianBelief` results for inputs on which the premises required to establish those theories are absent. D-prompt

2. **Laws that do not determine what they claim.**  
   `Posterior.info` is required only to be symmetric. A posterior with `info = 0`, or even `info = -I`, can satisfy the stated `Posterior` laws. Yet `decrement` treats it as curvature/information. D-prompt

   More importantly, a “maximizer” that genuinely solves the quadratic family but, on every other posterior, simply returns `x0` with `converged=false` passes the entire theory: `MaximizerAscends` passes by equality, `MaximizerStationary` becomes `true`, dimension is preserved, and quadratics are handled specially. D-prompt So the present laws do **not** establish that a `Maximizer` can maximize a nonquadratic problem at all.

3. **Roles (L2.7).**  
   No `data` constructor here needing a role law.

4. **Models against their theories.**  
   The intended LM model conflicts with `QuadraticConverges` for small budgets; the explicit case is under `optimization_model.lut` below.

5. **Against the specification.**  
   The unrestricted `y : Vec Float64` in the Laplace API steps outside the very subtype on which `Likelihood` is certified. Also `Posterior` is too weak for its use by `optimization.lth`: optimization requires a nonnegative step matrix, whereas `Posterior` supplies only symmetry.

6. **Implication over a type.**  
   "`if r.converged then ... else true`" in `MaximizerStationary` is exactly the forbidden vacuity pattern. A bad maximizer controls the premise by returning `converged=false`. D-prompt The test domain needs cases in which convergence is required/known, rather than sampling arbitrary problems and letting the specimen opt out.

7. **What I would change first.**  
   Strengthen `Posterior` before using it as an optimizer objective: at minimum require its information to be nonnegative; preferably state what relation the information has to the local curvature. Otherwise the next file's `negate : Posterior -> Objective` is simply not type-correct semantically.

8. **Cutoffs.**  
   The visible `tol`, `maxIter`, and `floor` are parameters, so this part follows P11.

9. **Certifying the maximizer beyond quadratics.**  
   Add a generated **nonquadratic concave family with a known optimum**. A minimal useful family is, with `r=x-b`,

   `logp(x) = -(c/2)|r|² -(d/4)|r|⁴`, with `c,d > 0`.

   Its unique maximum is known exactly at `b`; its score and information can be supplied analytically. For the **demanded `Settings`**, generate `n`, `b`, `c`, `d`, and `x0`, call the host maximizer, and check both that it reports convergence and that `logp(b)-logp(r.x)` is within the demanded tolerance (or an equivalent known bound). That catches the quadratic-specialist countermodel while requiring no second optimizer as an oracle. The sampling distribution over `n,b,c,d,x0` must of course be recorded, by L9.6. D-prompt

---

## `belief_model.lut`

1. **Laws wrong.** Inherited from the theory.

2. **Underdetermination.** Inherited from `Maximizer`.

3. **Roles.** None.

4. **Model against theory.**  
   The actual host implementation cannot yet be checked because the file explicitly says `src/luthier/lm.py` “does not exist yet.” D-prompt But an LM implementation respecting `maxIter` will fail the current `QuadraticConverges`: take `n=1`, `b=0`, `c=1`, `x0=1`, `tol=10^-12`, `maxIter=1`, `floor=0`, and damping `μ=1`. One LM step goes to `x=1/2`; its quadratic decrement is `1/8`, not `10^-12`, so the runner exhausts its one iteration and returns `converged=false`, while `QuadraticConverges` requires `true`.

5. **Against the specification.**  
   The comment says “the damping schedule of the method is the host's own … not a setting of the maximizer,” and the extern indeed receives only `Settings`, not `Damping`. D-prompt But `optimization.lth` explicitly moved the damping schedule out of hard-coded LM constants and made it a parameter under P11. D-prompt The current host interface gives the demand no route to supply that parameter.

6. **Implication over type.** Inherited from `MaximizerStationary`.

7. **What I would change first.**  
   Expose the damping schedule in the configured host maximizer rather than leaving it “the host's own.” Otherwise the native and host specimens are not even parameterized by the same algorithm.

8. **Cutoffs.**  
   No literal damping constants appear in this `.lut`; the problem is worse structurally: the cutoff/schedule parameter is absent from the interface.

9. **Maximizer.** The missing nonquadratic law belongs in `belief.lth`, not here.

---

## `optimization.lth`

1. **Laws/definitions that are wrong.**  
   "`negate (n : Nat) (p : Posterior n) : Objective n`" is not valid for every `Posterior`. `Objective` requires the step matrix to be symmetric **and nonnegative**, whereas `Posterior` requires only symmetry. `p.info = -I` is therefore a valid candidate under the latter's stated information law but makes `negate p` fail `StepMatrixNonNegative`. D-prompt

   "`posteriorOf ... : Posterior n`" is also overclaimed: it accepts arbitrary `f`, `g`, and `m` and immediately packages them as a theory model without requiring the gradient or information laws. D-prompt

2. **Laws that do not determine what they claim.**  
   `StepRule` never checks that `s2.phi` is actually `o.value s2.x`, nor that `accepted` corresponds to the objective at the trial point. D-prompt

   A wrong model passing **every `LMStep` law** is easy: use the correct/native `direction`; let `step` always set

   `x = st.x + direction`,  
   `phi = st.phi - 1`,  
   `accepted = true`,  
   the prescribed lower damping, and `iter+1`.

   It passes `DirectionDescends`, `DirectionAgrees`, `StepRule`, and `QuadraticStepAccepts`, even on an objective for which the trial point has a *higher* actual `o.value`. Thus the law's phrase “an accepted step lowers the value” is not what it tests.

3. **Roles (L2.7).**  
   "`Reason = { running | converged | exhausted | stalled }`" introduces four constructors, but no law states their roles. `isConverged` merely pattern-matches the constructors, exactly the kind of constructor-listing observer that L2.7 says is **not** a role law. D-prompt L2.7 is explicit that distinct constructors carry no role by themselves and an observer listing them does not solve this. D-prompt

4. **Models against theories.**  
   `native : LMStep` is compatible with the written, weak `StepRule`; the problem is that the law is too weak. `lmMaximizer` breaks the maximizer theory as described below.

5. **Against the specification.**  
   The cross-theory `Posterior -> Objective` mismatch is the concrete specification-level defect here: the dependency's laws do not entail the target theory's laws.

6. **Implication over a type.**  
   No major rare-premise implication in this file's own laws. `StepRule`'s accepted/rejected split is exhaustive rather than a rare-case filter.

7. **What I would change first.**  
   Fix `StepRule`: make the resulting stored `phi` agree with `o.value s2.x`, and make acceptance correspond to the comparison of the actual trial value with the old value. That removes an explicit false implementation that currently certifies as `LMStep`.

8. **Cutoffs.**  
   The damping schedule is parameterized as `Damping`, and the convergence/rank cutoffs come from `Settings`; no offending literal cutoff here. D-prompt

9. **Maximizer.** N/A; its missing general law belongs to `belief.lth`.

---

## `optimization_model.lut`

1. **Laws wrong.** Inherited from `belief.lth`.

2. **Underdetermination.** `native` and `host` are judged by the weak `StepRule`, so passing it would not establish correct acceptance.

3. **Roles.** None.

4. **Models against their theories.**  
   `lmMaximizer(d) : Maximizer` is a definite counterexample to the present universal `QuadraticConverges` for sufficiently small `maxIter`. It calls `minimize`, then reports convergence only when `finished` returns `converged`. D-prompt The `maxIter=1` one-dimensional case above therefore breaks its declared `Maximizer` type.

   The two host step functions cannot be checked because the prompt says their `lm.py` target is “not yet written.” D-prompt

5. **Against specification.** No additional independent contradiction beyond those above.

6. **Implication over type.** None locally.

7. **What I would change first.**  
   Do not try to make `lmMaximizer` satisfy the current `QuadraticConverges`; correct the law's domain/settings first. Otherwise an implementation would have to ignore its iteration budget to satisfy the theory.

8. **Cutoffs.** `d : Damping` is correctly explicit here.

9. **Maximizer.** The nonquadratic generated-family law should certify both this native specimen and the host specimen.

## Use-site consequences

Two of these defects reach `experiment_zero.lut` directly. The experiment really uses `profiled`, so the `RSS=0` singularity is in the path the theory must support. It also supplies `lmTol`, `lmMaxIter`, and `lmFloor` from the demand, but supplies **no damping schedule** to the imported host `lm`, confirming the interface mismatch. D-prompt D-prompt

There is also one use-site P11 issue worth recording even though the experiment itself is not a style-review target: "`covFloor (n) := toFloat64 n * doubles.epsilon`" internally chooses another `RankFloor` instead of obtaining it from the demand. D-prompt That is hard to reconcile with the settled rule that a rank floor is a demand-supplied cutoff. D-prompt

### Not sure

I cannot verify `numpySort : Kolmogorov`, `belief_model.lut`'s `lm`, or `optimization_model.lut`'s host `direction/step` against their laws because the relevant Python implementations are not in this bundle; in the LM case the prompt explicitly says the file does not yet exist. I therefore have not asserted any numerical/bitwise failure of those host routines themselves.

The three changes I would put ahead of implementation are, in order: **fix `IsGradient`; make `Posterior.info` strong enough that `Posterior -> Objective` is valid; fix `StepRule` and the maximizer convergence laws.** Those are semantic holes that currently permit false models to certify, rather than merely missing tests.