# Report of bite C1: the `Within` form and the bound transformer

2026-10-26, Claude Opus 5.5 (agent C1), on `prompt-wave-bc.md` (77f56b9) and bite C1 of
`execution.md`. Sources: D-2026-10-25-a question 3 (the carrier (L, η, D, r), composed along a cone,
summed over inputs), D-2026-10-18-j, L9.18, L6.8, L13.5, the audit's section 5 and its boundary cases
(report.md, 5b1a05e), the three-levels report 2.3 to 2.5 (2f9c42b). What is mine is marked
[proposed] in the files and listed at the end.

## What was done

laws.lth (§5, new). `Within : (A : U) -> (A -> A -> Float64) -> Float64 -> A -> A -> Law`, the
metric, the theory's bound at the case, and the two values; evidence `Measured dist bound`; the
settling law `WithinIsMeasured` (confirmed within the bound, refuted past it, evidence that is not the
law's own distance and bound settles nothing), in `Settling` and in laws_model.lut. The ratio's
boundary cases are a theory, `Measuring` (`ratioOf`: zero distance is ratio 0 at any bound, a bound of
zero included; a positive distance at a bound of zero or below has no finite ratio; `worseRatio`, an
unbounded one absorbing), certified with two controls. The verdict is the comparison, the ratio a
record: a quotient can round to 1 one ulp past the bound.

tester.py. A law whose result is `Law` and whose body applies `Within` runs case by case like a
`Bool` law (`Case b` outside its range); each case's distance and bound are measured, and the outcome
and the entry keep `measured`: the cases measured, the worst ratio with the distance and bound it came
from, and the worst per region. A conjunct that is a numerical law keeps the type `Law`. The premise
reader takes `if p then Within ... else Case true` as a premise, so vacuity (A3) covers numerical laws.
`run_spec` and `conjunction_parts` keep their text: the measures pass through the runner, so
`drawing_revision` is unchanged (sha256:6cd60eb…) and no sampled entry outside the moved cones went
stale. Lines show "worst ratio r".

certify.py. `entry_bound` (certification.lth's `entryBound` at the metric level), `within_cap`, and
`serves` requires the worst ratio within the demand's cap; `serves_over` reads the worst over the
union of stretches (`pooled_worst`, the largest). The two-entry rule stands.

demand.lth, demand_model.lut, run.py, cli.py. The hole `bound : Demand -> C` becomes the field
`bound : Float64`, declared default 1 (`theDemand`), passed down by `inner`, recorded by `recorded`
and by `RecordKeepsThePolicies` (control `dropBound`), `run --bound RATIO`. plan.lth's `withSet`
follows the record.

core/properties/functions.lth. `Affine A` = (lipschitz, defect, radius, domain), `Transformer A` its
`Maybe` (no sensitivity, no bound, L6.8), `transform`, `admissible`, `Realizes`; `composeAffine`
(L₂L₁, L₂η₁ + η₂, D₁ ∩ f₁⁻¹(D₂), min(r₁, (r₂ − η₁)/L₁), r₁ when L₁ = 0 and η₁ fits, negative and so
empty when η₁ exceeds r₂); `pullback` (nothing below the defect, L13.5; the radius at L = 0); two
inputs by the sum `transformSum` and the max `transformMax`. The theory `BoundTransformer` with nine
laws (sound composition, associativity, empty domain, the radius, unknown composes unknown and pulls
back nothing, infeasible below the defect, the pull-back meets its tolerance, max below sum), model
`affineTransformers`, certified on listed dyadic transformers in tests/tester/transformer_laws.test.lut
with five controls refuted, the composition that drops L₂η₁ among them.

arrays.lth. `DotAgrees` is `DotStable` (a `Within` law, the same 3γₙ bound); `DotSensitive` is new:
|dot(x′, y) − dot(x, y)| ≤ transform(dotTransformer, ‖x′ − x‖), L = (1 + γ₂ₙ₊₈)‖y‖ (Cauchy and
Schwarz, the computed norms widened), η = 3γₙ(Σ|x′y| + Σ|xy|), domain the moderate vectors. Both
claimed in `Arrays`. `NormOfDot`, `NormScales` and `TraceAdditive` lose `tol` for 3γ bounds.

numbers.lth. `Elementary` gains `ulps`, the model's declared accuracy (1 in numbers_model.lut;
measured at most 0.502 ulp for exp and 0.500 for log, erf and sqrt on this host's glibc 2.43,
c1-ulps.py, seed 1). `SqrtSquares`, `ExpOfLog`, `LogOfExp`, `ExpAdds`, `LogMultiplies` lose `tol`:
`Within` laws whose bounds are derived in the comment, widened by `elementaryRoom` (second-order terms
and the bound's own roundings).

## Acceptance

- `dot`'s stability and sensitivity laws certified at ratio ≤ 1: DotStable worst ratio 0.116,
  DotSensitive 1 (tight at n = 1, where Cauchy and Schwarz is an equality), both sampled, 100 cases.
  Controls refuted: `dropDot` and `doublesThird` (the bound a third as large) for DotStable,
  `scaledDot` (the product 1 % too large, just past the bound) for DotSensitive.
- `compose`'s law certified on listed transformers, the L₂η₁-dropping control refuted (above).
- Worst ratios of the identities: SqrtSquares 0.66, ExpOfLog 0.35, LogOfExp 0, ExpAdds 0.97,
  LogMultiplies 0.38, NormOfDot 0, NormScales 0.14, TraceAdditive 0.06. ExpAdds is tight by design:
  over 500 000 draws in Python its worst was 0.988, at |x + y| just above 512, where the sum's
  rounding is exactly u|x + y|.
- Tests: tests/test_within.py (5, failing before C1); test_tester, test_certify, test_regions,
  test_tester_conjunction green; test_run green after the re-certification (its 6 failures before it
  were the arrays stores, stale by the moved cones).
- Re-certification: one pass over the 48 test programs (B2's bases_* left to B2), six at a time,
  logs in ~/.cache/luthier-wave-bc/C1/pass1. 47 ended; probability_laws.test.lut was cut by its
  3600 s timeout and its stores are not re-certified. Non-zero exits: laws and cases (fixtures that
  refute by design), vacuity (its vacuous fixtures, by design), and belief_laws: `PrecisionSymmetric`
  raised maximum recursion depth at one case, not checked against HEAD before C1. The second pass
  (0 lines ran) was not run: this agent's budget ran out. It is the coordinator's.
- `check_spec.py`: its one known finding. `core_metrics.py`: see "Counts".

## Counts (core_metrics.py, before C1 at 77f56b9 and after)

unclaimed 8 → 9: `within` (numbers.lth) lost its last claimed use there, the identities that used it
being `Within` laws now; arrays' pinv laws still use it. Loose real up by 11: the transformer's
definitions in functions.lth (`composeAffine`, `transform`, `admissible`, `Realizes`,
`transformSum`, `transformMax`, `noBound`, `affineTransformers`, `composeTransformers`,
`BoundTransformer`), `Measuring`, `dotTransformer`, `elementaryRoom`, against `Pointwise2` and
`Monotone`, which the new laws name and so moved to the rest. The brief's "no count up" is not met;
every new name is a definition a law of its theory reads, and a theory's own predicate counts as
loose for every theory of the tree (`Settling` does too).

## Not done, and why

- The pseudo-inverse's laws (`PinvOfDiagonal`, `PinvOfIdentity`, `PinvProjects`, `PinvSymmetric`,
  `PinvRestricts`, `PinvTraceIsRank`, `PinvScales`) and `RankUnderRotation`'s `Orthogonal tol` keep
  their `tol`: their bound needs the perturbation theory D-2026-10-18-j names (the radius below the
  smallest retained singular value), a bite of its own. probability.lth's `tol` laws are outside C1's
  files.
- `MatVecAgrees`, `MatMulAgrees`, `MatMulTransposes`, `TraceCyclic`, `TraceAgrees` keep their
  theorem bounds as `Bool` entrywise balls: a `Within` over a matrix needs the worst entrywise ratio
  as its distance, a small follow-up.
- The test line does not carry a `bound` (test.lth is outside C1's files): a line passes at ratio ≤ 1,
  the law's own content.
- certification.lth's holes `C` and `entryBound` are left as holes; certify.py's `entry_bound` is
  their metric-level specimen.

## Decisions taken on my own

1. The demand's `bound` is a cap on the worst ratio, default 1, not an output tolerance in the law's
   units: the law's bound is the theory's (D-2026-10-18-j), and a tolerance in output units is
   pulled back through the transformer by the planner (L6.8), not compared with a certificate.
2. `Within` has no `scale` beside the bound (the three-levels report had one): the theory's bound
   already carries the scale.
3. A positive distance at a zero bound has no finite ratio (`nothing`), a zero distance ratio 0 at any
   bound; the verdict is the comparison.
4. The measures pass through the runner so that `run_spec`'s source, part of every sampled entry's
   fingerprint, keeps its text.
5. `Elementary.ulps` a field of the model, 1 ulp, from a measurement on this host, glibc's table to
   be cited.
6. `Affine` keeps a `Float64` radius with a negative one meaning empty, and `Maybe` for an unknown
   sensitivity; B2's `Extended` [0, ∞] (core.lut) could replace both when the planner composes them.
7. `DotSensitive`'s radius is the moderate range (the product is bilinear), its sensitivity widened by
   γ₂ₙ₊₈ for the computed norms.
8. The settling law's values renamed `x y` (a binding clash with `CaseIsEvaluated`'s `b`).

## Question

None for Luciano. For the coordinator: pass 2, probability_laws, and belief_laws' recursion.
