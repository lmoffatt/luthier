**probability.lth**

1. **Laws that are wrong**: None identified as false of the intended models or unsatisfiable together. GaussianPeaksAtMean holds exactly at the residual-zero point (residual term vanishes); ProfiledIsGaussianAtItsSigma matches the analytic maximizer of the full Gaussian in \(u\).

2. **Laws that do not determine what they claim**: InfoNonNegative only checks the quadratic form on a drawn direction (not full positive-semidefiniteness of the spectrum). A matrix with a negative eigenvalue in an unsampled direction can pass.

3. **Roles (L2.7)**: Kolmogorov data has no constructor-role laws beyond the five characterizing predicates; the single field `distance` is covered by KolmogorovAgrees etc. MeanModel / ScaledModel / Likelihood are records of functions with role laws (shapes + derivative / symmetry / non-negativity).

4. **The models against their theories**: probability_model.lut’s `numpySort` satisfies KolmogorovAgrees by construction (host implements the same sort+scan as kolmogorovDistanceDef). No other model is supplied.

5. **Against the specification**: Conforms to 7.R2 (quantifies over VecOf n), 11.S18 / P11 (Resolution / Tolerance / Level are parameters), 4.R10 (native agreement for Kolmogorov), 7.S17 (UniformAtLevel declares its level). Constants pi / log2pi / tailSeriesTerms are definitional, not cutoffs.

6. **Implication over a type**: None; quantified domains are already the relevant subtypes (VecOf, UnitList, UnitValue).

7. **What you would change first**: Strengthen InfoNonNegative (or add a spectral law) so that a direction with a negative eigenvalue is forced to fail, because the current sampled-direction form does not determine “Fisher information”.

8. **Cutoffs**: None; every tolerance / step / level is a parameter of the law. tailSeriesTerms is a definitional truncation, not a demand cutoff (explicitly noted).

9. **Certifying the maximizer**: N/A (no Maximizer here).

**probability_model.lut**

1–3,5–9: Empty / N/A (single extern model of Kolmogorov; no data constructors, no cutoffs, no maximizer).

4. Satisfies all five Kolmogorov laws by host implementation of the native definition.

**belief.lth**

1. **Laws that are wrong**: None. DensityPeaksAtMean correctly encodes positive-semidefiniteness via the quadratic form; QuadraticConverges is the exact statement for a strictly concave quadratic.

2. **Laws that do not determine what they claim**: MaximizerStationary / MaximizerAscends / MaximizerKeepsDimension are only “per posterior” (7.R4); a maximizer that fails on a non-quadratic posterior still passes every law that is sampled. QuadraticConverges only covers the quadratic family.

3. **Roles (L2.7)**: GaussianBelief, Settings, MaxResult, Posterior, Maximizer are records; each field’s role is stated by the corresponding law (symmetry, peak, shapes, ascent, stationarity, dimension, quadratic convergence). No bare data constructors without role laws.

4. **The models against their theories**: belief_model.lut’s `lm` is an extern; no concrete test cases are given in the model file, so no breakage can be exhibited from the file alone.

5. **Against the specification**: Conforms to 7.R2, 10.S10 (Maximizer is the type against which the host is validated), P11 (Settings are demand parameters), D-2026-10-14-a (callback record crossing). Laplace update laws are inherited, not restated (L9.2).

6. **Implication over a type**: None; Posterior laws are already quantified over the Posterior subtype.

7. **What you would change first**: Add at least one non-quadratic family (e.g. a strongly concave objective with known unique maximum) that a test can sample, so that certification of the host maximizer is not limited to the quadratic case.

8. **Cutoffs**: None; tol / maxIter / floor are fields of Settings supplied by the demand.

9. **Certifying the maximizer**: The missing law is a statement that, on a non-quadratic strongly concave objective with known unique maximizer \(x^*\), the returned point satisfies \(\|x - x^*\|\) (or the Newton decrement) within the Settings tolerance and reports converged. Generator: a parametric family of strictly concave functions on VecOf n (e.g. \(-\frac12\|x-b\|^2 + \varepsilon\sin(\omega\cdot x)\) with \(\varepsilon\) small enough to keep strict concavity) together with Positive curvature bounds, sampled over VecOf n and the Settings parameters.

**belief_model.lut**

1–3,5–8: Empty / N/A (single extern).

4. Cannot be checked from the file; host implementation is absent.

9. Same gap as above for the host lm.

**optimization.lth**

1. **Laws that are wrong**: None. DirectionDescends, StepRule and QuadraticStepAccepts match the classical LM acceptance / damping rules.

2. **Laws that do not determine what they claim**: DirectionAgrees only forces agreement with the native dampedStep; a host direction that is a positive multiple of the true Newton direction (or any other descent direction that still satisfies StepRule) can pass. QuadraticStepAccepts only checks the first step.

3. **Roles (L2.7)**: Objective, Damping, LMState, Reason, LMStep, Run are covered by the stated laws (gradient, symmetry, non-negativity, descent, damping schedule, acceptance). No bare constructors lacking role laws.

4. **The models against their theories**: optimization_model.lut supplies both native and host models of LMStep and a native lmMaximizer of Maximizer; no concrete failing case is present in the files.

5. **Against the specification**: Conforms to 7.R2, 10.S10, P11 (Damping and Settings are parameters), D-2026-10-14-a (record-of-functions crossing). Re-uses belief.lth’s decrement / Settings.

6. **Implication over a type**: None.

7. **What you would change first**: Strengthen DirectionAgrees (or replace it by a pure descent + first-order model agreement) so that the law does not hard-wire the exact native formula; otherwise the host is forced to reproduce the native floating-point expression rather than any correct damped Newton step.

8. **Cutoffs**: None; all tolerances and damping bounds are parameters.

9. **Certifying the maximizer**: Same gap as belief.lth (lmMaximizer is only forced to succeed on the quadratic family).

**optimization_model.lut**

1–3,5–8: Empty / N/A.

4. native satisfies LMStep by definition; host is an extern (unchecked here); lmMaximizer inherits the Maximizer laws of belief.lth (again only the quadratic family is forced).

9. Same missing non-quadratic law.

**arrays.lth** (imported foundation)

1. **Laws that are wrong**: None identified; the entrywise exactness laws and the relative-tolerance sum laws match 11.S14 / 3.S28.

2. **Laws that do not determine what they claim**: RankUnderRotation and the Pinv* laws rely on the host’s retainedRank / pinvSym; a host that returns a different but still correct spectral truncation on a non-diagonal matrix can still pass the diagonal / zero / identity / scaling cases. PinvRestricts is only stated on PsdAt.

3. **Roles (L2.7)**: Array / Vec / Mat are structural; the leaf record Arrays has a law for every operation. No missing constructor-role laws.

4. **The models against their theories**: arrays_model.lut is not supplied in the bundle; cannot check.

5. **Against the specification**: Conforms to 11.S9, 11.S14, 11.S18, P11 (RankFloor is a parameter), 3.S27–3.S28, 4.R10. Proposed relative-scale comparisons (approxMatOf / approxMatSlackOf) implement D-2026-10-14-c.

6. **Implication over a type**: None; ClearFloor / ClearDiagonal / Orthogonal / PsdAt are already the refined domains.

7. **What you would change first**: Make the PinvRestricts / PinvProjects generators include a modest non-diagonal PSD family so that the laws are not satisfied merely by correct behaviour on diagonals.

8. **Cutoffs**: None; every tolerance and RankFloor is a parameter of the law.

9. N/A.

**experiment_zero.lut** (use context only)

Not under review for style; it exercises the theories correctly (profiled / fixedSigma, laplaceMode, Kolmogorov distance on the transforms, Settings from demand parameters). No contradiction with the theories is visible.

**not sure**

- Whether the host implementations of kolmogorov_distance, lm.maximize, lm.damped_step and lm.step actually satisfy the Boolean laws (host source is absent).
- Whether the floating-point constants (pi, log2pi, sqrt2, tailSeriesFrom) produce any observable discrepancy under the demand tolerances that the slice will use.
- Exact interaction of the proposed approxMatOf / approxMatSlackOf with the existing within / withinOf of numbers.lth (the latter is imported but not shown).
- Whether generators.lth’s Level and the UniformAtLevel sampling distribution are strong enough for L9.6 (distribution edges).