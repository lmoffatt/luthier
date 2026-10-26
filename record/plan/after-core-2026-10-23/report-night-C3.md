# Report of Agent C3: uncertainty's composition declared

2026-10-26, Claude Fable 5.1, on `prompt-night-2026-10-26.md` (b21f2da) and bite C3 of `record/plan/audit-algebras-2026-10-22/execution.md`. Committed by the coordinator from the agent's hand-back (its Write was refused). Commit 40f6b89 (equality.lth only). Sources: the audit's 4.3 (report.md, 5b1a05e: marginals do not determine a sum's distribution; convolution needs independence or a joint), D-2026-10-18-c and its correction, D-2026-10-18-i ("a t-norm or convolution"), D-2026-10-17-g, D-2026-10-25-a question 1, D-2026-10-13-m, equality.lth's `ProbabilisticMetric`, probability.lth §6 (`Pushforward` over `Gen`), algebraic.lth's evidence base, report-C1.md (`Affine` in functions.lth as the metric-level carrier composed along a cone). What is the agent's is marked [proposed] in the file.

## What was done

`src/luthier/lib/core/structures/equality.lth`, a new section after `ProbabilisticMetric`, declarations only (48 lines, 26 of them comment):
- `JointDistribution`: a joint cdf on two distances with its two marginals as fields, and its laws `JointGrounded` (zero on either axis), `JointRectangle` (2-increasing, over a subtype of ordered rectangles), `JointFrechet` (within the Fréchet bounds of its marginals, `larger (a + b - 1) 0` below and `smaller a b` above), `JointMarginals`.
- The two hypotheses of the audit's 4.3 as laws of a joint: `Independent` (the product, under which the sum is the convolution) and `CoupledAbove t` (the joint at least the t-norm of its marginals, Schweizer and Sklar 1983, chapters 6 and 7), each the premise of a theory of the joint, `IndependentJoint` and `CoupledJoint t`, which a theory that composes under it takes as its parameter (the pattern of `Lipschitz` and `LipschitzMap`).
- `DistanceSum j`: the sum of two distances under their joint, the composition of uncertainty along a chain, with `SumDominatesRectangle` ({D1 < s, D2 < u} within {D1 + D2 < s + u}) and the sum a `DistanceDistribution`.

The comment ties it to what exists: the t-norm `t` of `ProbabilisticMetric A o t` is the theory's hypothesis on how the uncertainties of two links depend on each other, named per theory as the evidence base's composition is (D-2026-10-25-a question 1). Łukasiewicz's t-norm is the Fréchet lower bound, so every joint is coupled above by it and that hypothesis is free; the product is independence; the minimum is one draw reused. `MengerTriangle` is then a consequence: t (F_xy s) (F_yz u) ≤ J s u ≤ F_sum (s + u) ≤ F_xz (s + u). The pushforward through a general function is probability.lth's `Pushforward` of a `Gen` of pairs (D-2026-10-17-g), so nothing is declared for it here. The first consumer named: the sequential test at the probabilistic level (D-2026-10-18-c, D-2026-10-15-b), composing a value's distance distribution along a cone as `Affine` does at the metric level; no model until then (P8).

## Checks

- `luthier check` clean on equality.lth and core/core.lut.
- 4.S14 (an unclaimed Bool definition): a first version left `Independent` and `CoupledAbove` claimed by nothing and `test_core_claimants_cross_core_file_boundaries` failed with exactly those two; `IndependentJoint` and `CoupledJoint` claim them and the test passes. `tests/test_core_structures.py`: 8 passed, 2 failed; the two failures precede this commit (confirmed at b21f2da): `test_every_base_control_is_refuted` (bases_controls.test.lut has three `ProductIsIndependent` lines since 480e92c, which the test's BASE_CLAIMS set does not expect) and `test_the_product_composition_is_below_the_union_bound` (5 refuted conjuncts of `CappedSumIsAssumptionFree` instead of 1, since 480e92c added a wrong model per conjunct).
- `python scripts/check_spec.py`: its one known finding.
- The laws exercised outside the tree (no store moves, no model in core.lut): the scratch program `c3-scratch-joint.test.lut.txt` beside this report (copied from ~/.cache/luthier-night/C3/), `luthier check` clean, run with `luthier test --no-cert`: two exponential distances of rate 1 under the product joint and under the comonotone joint `smaller`, their sum the Gamma(2, 1). Nine claims ran on listed cases; seven controls refuted, one per law (a joint of constant 1; the `larger` of the marginals; half the product, below the Fréchet lower bound at s = u = 3; the comonotone joint as independent; the product joint as coupled above the minimum; the sum claimed as an exponential of rate 0.1).

## Decisions taken on my own

1. Everything in equality.lth; probability.lth untouched (its `Pushforward` over `Gen` already is the pushforward through a general function).
2. The hypotheses are laws of the joint, claimed by theories (`IndependentJoint`, `CoupledJoint`), not premises inside `DistanceSum`; 4.S14 refuses a law no theory claims.
3. Only what a finite law can state is declared: the marginals tied to the joint by the Fréchet bounds; the sum's law the rectangle domination, its exact value a model's.
4. `MengerTriangle` is not re-derived as a law of a chain coupling; the derivation is in the comment.
5. The scratch test stays outside the tree; its text is kept beside this report as the first consumer's starting point.

## Question

When the sequential test consumes this, should Łukasiewicz's t-norm (the Fréchet lower bound, free of hypothesis) be the probabilistic level's default, as the capped sum is the evidence base's, the product only under a declared independence?

Coordinator's answer (2026-10-26): yes, as the consequence of D-2026-10-25-a question 1 (the default assumes nothing; a stronger composition is declared). Luciano told; one commit undoes it.
