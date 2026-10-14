# The fit's theories: report

By Claude Fable 5.1, an agent of the coordinating session, 2026-10-14, on `prompt.md` of this
directory (committed at 57ec030). Sources read: v0.1's `probability.lut`, `belief.lut`,
`optimization.lut`, `probability_python.lut` and the leaves of `array.lut` at the tag
`v0.1-final`; the first slice's `arrays.lth`, `numbers.lth`, their models and report; the spec
items named (7.R2, 11.S18, 3.S23, 6.S5, 7.S17, 10.S8 to 10.S10); D-2026-10-14-a and
answers-2-2026-10-14 item 2; sonolocalización's `experiment_zero.lut` (70-130, 149-170),
`positions.lut`, `distances.lut`, `src/lm.py`, read only, nothing changed there. Files touched:
the six new ones under `src/luthier/lib/` and `arrays.lth` with `arrays_model.lut` for `trace`
and `pinvSym`. Each committed alone, by path.

## What was written

| file | commit | states |
|---|---|---|
| `arrays.lth`, `arrays_model.lut` | 2f8e7c2 | `traceDef`; `trace` as a field of `Arrays` with `TraceOfIdentity` (exact), `TraceAdditive`, `TraceCyclic`, `TraceAgrees` (within the demand's tolerance, 11.S14, 11.S18); route `luthier.arrays.trace` |
| `arrays.lth`, `arrays_model.lut` | e94b82f | `frobDef`, `pinvOfDiagonal`, `approxMatSlack`; `pinvSym : RankFloor -> Mat Float64 -> Mat Float64` as a field of `Arrays` with `PinvOfDiagonal`, `PinvOfZero` (exact), `PinvOfIdentity`, `PinvProjects` (P S P = P), `PinvSymmetric` (P and S P), `PinvRestricts` (S P S = S up to the discarded part, slack `floor * frob S`), `PinvTraceIsRank`, `PinvScales`; route `luthier.arrays.pinv_sym_at` |
| `probability.lth` | 4c072e7 | `Resolution` (step and tolerance of a central difference), `IsGradient`, `IsJacobian` over `VecOf n` (7.R2); `MeanModel n`, `ScaledModel n`, `Likelihood n` as theories with their laws (`MeanShape`, `JacShape`, `JacIsJacobian`; `ScaledShapes`, `DLogSigmaIsGradient`; `TangentShapes`, `ScoreIsGradient`, `InfoSymmetric`, `InfoNonNegative`); `gaussian`, `profiled`, `fixedSigma`, `outerDef`, `GaussianPeaksAtMean`, `ProfiledIsGaussianAtItsSigma`; `normalCdf`, `normalTail`, `valueSums`, the native Kolmogorov distance, `Kolmogorov` as a theory of one leaf (`KolmogorovOfNothing`, `KolmogorovOfOne`, `KolmogorovOfMultiset`, `KolmogorovBounded`, `KolmogorovAgrees`, all exact), `kolmogorovTail`, `uniformPValue`, `UniformAtLevel` at generators.lth's `Level` (7.S17) |
| `probability_model.lut` | 1c9f9e6 | `numpySort : Kolmogorov` (route `luthier.arrays.kolmogorov_distance`), `kolmogorovDistance` by name |
| `belief.lth` | 2ec1693 | `GaussianBelief n` as a theory (`PrecisionSymmetric`, `DensityPeaksAtMean`), `gaussianLogDensity`; `Settings` (tol, maxIter, floor), `MaxResult n`, `Posterior n` as a theory (`PosteriorScoreIsGradient`, `PosteriorInfoSymmetric`), `decrement` (half of g^T M^+ g at the floor); `Maximizer` as a theory with `MaximizerAscends`, `MaximizerStationary`, `MaximizerKeepsDimension`, `QuadraticConverges` on the family `quadratic n b c`; `laplacePosterior`, `laplaceMode`, `laplaceAt`, `laplaceUpdate` |
| `belief_model.lut` | 8d72771 | `lm : Maximizer` (route `luthier.lm.maximize`), `maximize` by name |
| `optimization.lth` | 262c400 | `Objective n` as a theory (`GradIsGradient`, `StepMatrixSymmetric`, `StepMatrixNonNegative`), `negate`, `posteriorOf`; `Damping` (init, factor, least, most), `LMState n`, `start`, `diagOf`, `dampedStep`, `lowered`, `lmStep`, `Reason`, `isConverged`, `finished`, `Run n`, `minimize`; `LMStep` as a theory (`DirectionDescends`, `DirectionAgrees`, `StepRule`, `QuadraticStepAccepts`), `quadraticObjective` |
| `optimization_model.lut` | 655b0a0 | `native : LMStep` (the definitions), `host : LMStep` (routes `luthier.lm.damped_step`, `luthier.lm.step`), `lmMaximizer (d : Damping) : Maximizer` (the native driver) |

Every file passes `PYTHONPATH=src python3 -m luthier.cli parse`, and `luthier check` prints
nothing on any of the eight: the checker refuses nothing, the file's or its own (the 4.R3 and
4.R9 refusals the first slice's report listed on arrays.lth are gone, bite 3b having landed).

Not written, and why: v0.1's sampler (`Draw`, `Sampler`, `gaussianSampler`, `normalVec`), the
probability integral transform (`gaussianPit`, `Kernel`) and the ensemble diagnostics
(`IsDensityOf`, the Bartlett identities, `DensityPair`), which need a generator of standard
normals; generators.lth has `Random.uniform` only, and v0.1's `normalVec` was an extern with no
theory. `BeliefFamily`, `Discrete`, `Exchangeable`, `EvidenceChains`, `Calibrated`,
`laplaceEvidence` (a log-determinant no leaf gives), `ConvergesAtOrder`, which the slice's two
stages do not use. `runTrace`, `reasonCode`, `Certified` of optimization.lut: the trace was
v0.1's certification of the whole path, replaced by the laws of one step and the decrement at the
end (`MaximizerStationary`); the codes were for a host that could not build a `Reason`, and the
record crossing now reads a labeled sum.

## The choices where the specification or v0.1 was silent (all marked `[proposed]` in the files)

1. `pinvSym` takes its floor as its first argument, as `retainedRank` does (P11; v0.1
   `array.lut:157` held `n eps` inside `retainedFloor`). The host needs `pinv_sym_at(floor, a)`
   beside `pinv_sym`. (arrays_model.lut)
2. The theory files use the imported models, `elementary` of numbers_model.lut and the leaves
   `add sub scale dot norm matVec matMul madd mscale transpose pinvSym` of arrays_model.lut by
   name, as arrays.lth takes its square root (the first report's choice 12). The alternative is
   a parameter `(a : Arrays) (e : Elementary)` on every definition, which the port of
   experiment_zero.lut would have to thread through `gaussian`, `laplaceMode` and the rest.
   (probability.lth header)
3. `MeanModel n` and `Likelihood n` carry `k : Nat`, the number of observations, as a field;
   v0.1 had none and stated the shapes as a law on the data's length. It lets the laws quantify
   the data over `VecOf l.k`, which has a generator. The port sets `k := i.n` in
   `positionsModel`, and `gaussian` reads `k` off the model. (probability.lth §2, §3)
4. The data of a likelihood are `Vec Float64`: v0.1's `(Y : U)` is fixed, which is what the
   slice has and what 7.R2 asks of type parameters. (probability.lth §3)
5. The truncation of Kolmogorov's series (100 terms, from x = 0.2, v0.1 `probability.lut:81`) is
   written as two named constants and not taken as a parameter: it is the precision of a
   definition, below what a double resolves, not a criterion a demand would set. If P11 is read
   on every number, `kolmogorovTail` takes a `Series` record and the port passes it.
   (probability.lth §5)
6. `Settings` of a maximizer has three fields: `tol` (the decrement at which it has converged),
   `maxIter` and `floor : RankFloor` (the spectrum floor of the step matrix, below which a
   direction is not stepped nor counted in the decrement). v0.1 had two and `solve`d the matrix
   whole. The port's `runSettings` gains `floor := ...`, from the run's parameters. (belief.lth
   §2)
7. `Maximizer` is a theory of one function, `maximize : Settings -> (n : Nat) -> ... ->
   MaxResult n`, so that the host's is validated against its laws at the first action (10.S10);
   v0.1 had a bare function type with the laws in optimization.lut. The route takes the
   settings as its first argument (v0.1's took `tol` and `maxIter` apart). (belief.lth §2,
   belief_model.lut)
8. The stationarity law uses the Newton decrement with `pinvSym` at the settings' floor and asks
   `decrement <= s.tol` at a converged `x`, with no slack: the host's successor must stop by the
   same decrement computed by the same leaf (it can, P7), and then the law is exact on it.
   (belief.lth §2)
9. The damping schedule is `Damping` (init, factor, least, most), a parameter of the step and of
   the native driver (P11; v0.1 held four constants). It is not a setting of the maximizer: the
   host's `lm.maximize` carries its damping as the module's own values, listed below, and
   `lmMaximizer (d : Damping)` takes it. If the damping should be the demand's at the run, it
   joins `Settings` and the host's `maximize` reads it there. (optimization.lth §2,
   optimization_model.lut)
10. The laws over a record of functions (`Posterior n`, `Objective n`, the three laws of
    `Maximizer` over any posterior, `StepRule` over any objective and state) have no generator
    and are certified per problem, as listed cases (7.R4); the concave quadratic `quadratic n b
    c` is the family with generators (`VecOf n`, `Positive`), on which `QuadraticConverges` and
    `QuadraticStepAccepts` are sampled. (belief.lth §2, optimization.lth §3)
11. `GaussianBelief n` is a theory, not an alias: its precision is symmetric and its log density
    is greatest at the mean, which is positive semidefiniteness read through the density. The
    prior experiment_zero.lut builds as a literal is certified per value. (belief.lth §1)
12. The laws of the Gaussian construction are two: the log-likelihood is greatest at the mean
    (exact) and the profile likelihood is the full one at u* = log sigma* held fixed, in value,
    score and information (distances.lut stated it for its model). The Fisher identities wait for
    the sampler. `fixedSigma n m u` is the scaled model with sigma known, what
    experiment_zero.lut:89 builds inline. (probability.lth §4)
13. `Kolmogorov`'s agreement with the native definition is stated exact, as v0.1's certification
    found it (the same operations on the same sorted values in the same order); the laws
    quantify over `UnitList`, a subtype of `List (Vec Float64)` by the predicate `allUnit`, not
    a list of a subtype, so that it refines the leaf's domain. (probability.lth §5)
14. `IsGradient` compares the slope with the norm of the gradient relative to `1 + |f t| + |g|`
    (v0.1 scaled its tolerance by `1 + |f t|`), since the difference of two values of f loses
    the digits they share; `IsJacobian` compares entry by entry with `approxVec`. The step and
    the tolerance are the demand's `Resolution` (P11; v0.1 `fdStep`, `fdTol`). (probability.lth
    §1)

Four forms the checker refuses were sidestepped rather than kept and reported, since each had a
reading that is also better: a lambda whose body is a value of a subtype where `Fin n ->
Float64` is expected (`fn k { u }` with `u : UnitValue`; now `single u`, `u` passed to a
`Float64` parameter); a variable bound by a tuple pattern passed to an `Int` parameter (`count`
of `valueSums`; now `lengthOf`); a record literal passed where a theory type is expected
(`gaussian n { model := ... }`; now `fixedSigma`, and `posteriorOf` in optimization.lth); `List
UnitVec` passed where `List (Vec Float64)` is expected (now `UnitList`). The first three are
the checker's (4.R9 on a lambda's result, on a pattern variable's base, on a literal at a
theory type); the fourth the spec does not state (4.R9 names function variance only). Each was
reproduced on a three-line variant before the sidestep.

## What the bridge and lm.py's successor must do, per extern

The bridge (run.py, 3.S22 to 3.S25, D-2026-10-14-a as implemented at dda4192):

| extern | in | out |
|---|---|---|
| `luthier.arrays.trace` | a `Mat Float64` record, `f` materialized over `Fin m x Fin n` (3.S23) | a float |
| `luthier.arrays.pinv_sym_at` | a float (the `RankFloor`, a subtype of `Float64`), then the matrix as above | a 2-d ndarray read at `Mat Float64` as `{ m, n, f }` |
| `luthier.arrays.kolmogorov_distance` | a Luthier `List (Vec Float64)`: a Python list, each element the ndarray of the vector's `f` (the same as a `Vec Float64` crossing, once per element; `nil` the empty list) | a float |
| `luthier.lm.maximize` | the `Settings` record as three numbers (float, int, float) read by attribute or key; `n` an int; the three lambdas over `VecOf n` as callbacks, each called by the host with a 1-d ndarray and answering a float (`logp`), a 1-d ndarray (`score`, read from a `Vec Float64` record) or a 2-d ndarray (`info`); the start as a 1-d ndarray; every callback call counted per route and position and recorded in `x.run.json` (12.S18) | a record `{ x, converged }`: a 1-d ndarray read at `VecOf n` and a Python bool read at `Bool`, never an int |
| `luthier.lm.damped_step` | `n`; `Settings`; the `Objective n` record with its three fields as callbacks (D-2026-10-14-a); `x` an ndarray; `mu` a float | a 1-d ndarray at `Vec Float64` |
| `luthier.lm.step` | `n`; `Settings`; `Damping` as four floats; the objective as above; the `LMState n` record (`x` ndarray, `phi` float, `mu` float, `iter` int, `accepted` bool) | a record read at `LMState n` with the same five fields |

The host code, in this repository (P7):

- `src/luthier/arrays.py`: `pinv_sym_at(floor, a)`: `w, V = eigh(a)`; `keep = w > floor *
  max(|w|)` (none when `w` is empty); `(V[:, keep] / w[keep]) @ V[:, keep].T`. `trace` and
  `kolmogorov_distance` exist as they are. `retained_rank_at` exists (landed by run.py bite 8).
- `src/luthier/lm.py`, the successor of sonolocalización's `src/lm.py`, which does not exist
  here yet: `damped_step(n, settings, o, x, mu)` computing `-(pinv_sym_at(settings.floor, M +
  mu * diag(diag M)) @ g)` with `M = o.stepMatrix(x)`, `g = o.grad(x)`, by the same
  `pinv_sym_at` as the leaf, so that `DirectionAgrees` is within rounding; `step(n, settings,
  damping, o, s)` as sonolocalización's `step` with the damping's `factor`, `least`, `most`
  read from the record; `decrement(settings, o, x)` as `0.5 * g @ pinv_sym_at(settings.floor,
  M) @ g`, the same formula as belief.lth's `decrement`, so that `MaximizerStationary` holds
  exactly where the host stopped; `finished(settings, damping, o, s)` by that decrement, the
  budget and `damping.most`; `maximize(settings, n, f, g, m, x0)` negating `f` and `g` as
  sonolocalización's does, with the module's damping (0.001, 3.0, 1e-15, 1e15, v0.1's) as its
  own values until choice 9 is reversed, returning `{"x": s["x"], "converged": code ==
  CONVERGED}`. A zero-length `x` does not arise (`Dim` is 1 or more).
- Nothing in `host.py` or `tables.py` is touched by these theories.

## For the port of experiment_zero.lut, positions.lut and distances.lut (not done here)

Names kept from v0.1: `MeanModel`, `ScaledModel`, `Likelihood`, `gaussian`, `profiled`,
`normalCdf`, `kolmogorovDistance`, `kolmogorovTail`, `valueSums`, `GaussianBelief`,
`laplaceMode`, `laplaceAt`, `Maximizer`, `MaxResult`, `pinvSym`, `trace`. Beyond renames:
`MeanModel (PositionsOf n)` becomes `MeanModel (3 * n)` with `k := i.n` and no `dim`, `shift`;
`Likelihood (PositionsOf n) (Vec Float64)` becomes `Likelihood (3 * n)`; `gaussian T { model,
logSigma, dLogSigma }` for `known s` becomes `gaussian n (fixedSigma n (meanModel m) (log s))`;
`fastMaximizer : Float64 -> Int -> Maximizer := extern ...` goes, replaced by `import
"belief_model.lut" lm : Maximizer` and `runSettings : Settings := { tol := lmTol, maxIter :=
lmMaxIter, floor := lmFloor }`; `laplaceMode (3 * m.x0.n) (Vec Float64) (fastMaximizer lm.tol
lm.maxIter) lik prior m.d` becomes `laplaceMode (3 * m.x0.n) lm runSettings lik prior m.d`;
`laplaceAt (3 * m.x0.n) (Vec Float64) lik prior m.d mode.x` drops the `(Vec Float64)`;
`pinvSym post.precision` and `pinvSym b.precision` take the floor first; `trace (f * cov)` is
`trace (matMul f cov)` or the operator of arrays_model.lut; the prior's precision matrix is
built by `mat Float64 s.n s.n (fn a b { ... })` (the first report's choice 11); `match valueSums
kept { (s1, s2, count) -> ... }` is unchanged; `transformTail` is `uniformPValue numpySort`
applied to `kept`, or stays as written with `kolmogorovTail` and the correction inline.
distances.lut's `IsGradient Theta ...` calls become `IsGradient n r` with a `Resolution` from
its parameters (`pitResolution` already is one).

## Decisions taken on my own

The fourteen `[proposed]` items above and the four sidesteps of the checker. Each is undone by
one commit, and nothing depends on them yet beyond the port, which has not started.
