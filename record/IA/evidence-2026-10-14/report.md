# Evidence on the slice's laws: report

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on `prompt.md`; saved by the coordinator.
The `test` programs under `tests/tester/` (bac688f session_a.lut, d7089d7 arrays_laws.lut,
568e3ea fit_laws.lut, f368286 optimization_laws.lut, 90847d9 belief_laws.lut, 5eeabd2
probability_laws.lut, e55bbe3 sonolocalizacion_laws.lut), committed by the agent; tester.py's
three fixes committed by the coordinator with this report. Cutoffs as censuses of one: tol
1e-12 [proposed], rank floor 30 eps, settingsA {1e-12, 500, 30 eps}, dampingA lm.py's, Resolution
distances.lut's `pitResolution`, Level {alpha 0.01, n 200}; seed 20261014; fuel 1e8 per case.
Session A as a value: its two CSVs as text in session_a.lut (git blobs cited), parsed by the
codec, since a census cannot run an action.

## Findings

Two laws refuted, both for arrays.lth's author: `PinvRestricts` is false on indefinite
matrices (`pinvSym` drops negative eigenvalues: s p s differs from s by the negative part;
holds on positive semidefinite ones: the domain should be PSD, or the slack include the dropped
part); `PinvProjects`, `PinvSymmetric`, `PinvScales` fail only on Hilbert 5 (condition 4.8e5):
relative deviations 2.5e-12, 7.6e-12, 1.1e-12 against tol 1e-12, rounding of order cond × eps:
the comparison does not scale with the conditioning (under D-2026-10-14-c, a scale factor in
the law or a demand with tol ≥ cond × eps). `MaximizerKeepsDimension` unevaluable: a chained
projection on a parenthesised expression (`(e).x.n`) does not reduce (parse.py or the
elaborator), not the law. Every other law confirms on what it ran on. Both maximizers, `lm` and
the native `lmMaximizer`, agree on all 100 drawn quadratic cases (`MaximizersAgree`, proposed).

## Table per law (S sampled, C cases; numbers are cases evaluated)

Arrays on numpy: the pointwise, dot, norm, matVec, matMul, rank and trace laws S 100 each;
RankOfDiagonal, PinvOfDiagonal S 100 (no zero entry drawn: the not-retained branch untested);
the laws over drawn `Symmetric` S 100 but only 0×0 and 1×1 pass the filter (PinvRestricts
refuted 36/100); on 7 listed symmetric matrices RankBounded C 7, PinvTraceIsRank C 7, RankScales
S 100, refuted PinvProjects 1/7, PinvSymmetric 1/7, PinvRestricts 2/7, PinvScales 12/100;
RankUnderRotation sampled not run (the `Orthogonal` filter accepts nothing), listed C 18.
Probability: KolmogorovOfNothing C 1, KolmogorovOfOne S 100, KolmogorovOfMultiset/Bounded/Agrees
C 6 on listed unit lists (sampled not run), UniformAtLevel C 3 on calibrated lists; MeanShape,
JacShape, JacIsJacobian S 20 on session A and on posModel; ScaledShapes, DLogSigmaIsGradient S 20;
TangentShapes, ScoreIsGradient, InfoSymmetric, InfoNonNegative S 20 on session A's profile
likelihood, S 5 on the native models; GaussianPeaksAtMean S 5; ProfiledIsGaussianAtItsSigma S 20
and S 5. Belief: PrecisionSymmetric C 1 on priorA (drawn: no generator of GaussianBelief, 7.R4);
DensityPeaksAtMean S 100; PosteriorScoreIsGradient, PosteriorInfoSymmetric S 100 on listed
quadratics, S 20 on session A; QuadraticConverges S 100; MaximizerAscends, MaximizerStationary S
100 on quadratics, C 1 each on session A's fit from the prior mean (420 s, 347 s);
MaximizerKeepsDimension unsettled (101). Optimization: GradIsGradient, StepMatrixSymmetric,
StepMatrixNonNegative S 100 on quadratics, S 20 on session A; DirectionDescends, DirectionAgrees,
StepRule on session A native S 20, host S 20. The fit on the drawn quadratic family (n in [1,
11]): QuadraticConverges lm S 100, native S 100; MaximizersAgree S 100; QuadraticStepAccepts,
DirectionDescendsOnQuadratic, DirectionAgreesOnQuadratic, StepRuleOnQuadratic host and native S
100 each. The port: LayoutFromUndoesTo, LayoutToUndoesFrom S 100; FullAgrees, ProfileAgrees,
ProfileIsFullAtItsSigma S 5; ReportsValidity C 9 (session A plus 8 graphs broken on one
invariant each).

## Laws that need a generator (today listed cases only)

Symmetric matrices (RankBounded, RankScales, PinvProjects, PinvSymmetric, PinvRestricts,
PinvTraceIsRank, PinvScales; `gen_symmetric` exists in arrays.py but a binding cannot name a
generator); orthogonal matrices (RankUnderRotation, 7.S5); unit lists (the Kolmogorov laws,
UniformAtLevel with a calibrated uniform sampler); `ClearDiagonal` (an atom at 0); records of
functions or theories (7.R4: MeanModel, ScaledModel, Likelihood, GaussianBelief, Posterior,
Objective, the Maximizer and LMStep laws, distances.lut's l, ReportsValidity's f and g).

## The tester

Fixed (tester.py, test_tester.py): `Fin n -> A` drawn as a host array entry by entry (`Entries`);
`VecOf n`, `MatOf r c`, `Square` built, not filtered (a field a refinement equates to a value or
another field); a census of lists bound to a list parameter lists its elements (`_list_depth`).
Not fixed: a refined `List` (`UnitList`) stops on "recursive data"; a binding names only a
census, never a generator; a census cannot come from an action; censuses walk in lockstep while
exhaustive takes their product; one fuel for every line (the 7-node native likelihood costs 80 s
per case); a refuting case shows arrays as `extern "host:N"`; results print only at the end.

Decisions of the agent: the test lines in programs under tests/tester/, not in the model files
(they need censuses and imports); the wrapper laws; the listed cases; fewer cases on heavy
lines; size 5 for distances.lut. It overwrote `scratchpad/probe.py` in the shared scratchpad.
