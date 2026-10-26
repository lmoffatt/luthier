# Report of agent C2: the budget law's mode and the modulus

2026-10-26, Claude Opus 5.5, on prompt-night-2026-10-26.md (b21f2da) and bite C2 of `record/plan/audit-algebras-2026-10-22/execution.md`. Committed by the coordinator from the agent's hand-back (its Write was refused). Commits: 4e1a68b, 7c0cc4f, 949289a, 207001d, ecb3a47, 5703f2b. Sources: the audit (report.md, 5b1a05e) 4.4 and 6; D-2026-10-18-i with the coordinator's correction of 2026-10-23 (resources a typed vector; Blumofe and Leiserson's work and span); D-2026-10-18-d, L9.17, D-2026-10-16-m, L13.5; D-2026-10-25-a question 3; report-C1.md. What is the agent's is marked [proposed] in the files.

## What was done

`src/luthier/lib/resources.lth` (new, beside numbers.lth):
- §1: `Resources = { work, span, memory : Nat }` and `ResourceAlgebra` (`none`, `sequence`, `parallel`): each composition a commutative monoid with `none` neutral; each part carried to the counts by its own operation through the core's `Preserving`: work adds in both; span adds in sequence and takes the larger in parallel; peak memory takes the larger in sequence and adds in parallel. Parts are `Nat`, so sums are exact. Model `workSpanMemory` and claim `WorkSpanMemoryIsAResourceAlgebra` in `resources_model.lut`.
- §2: the modulus. `Bound` a positive double; `Need = sufficient Resources || infeasible Infeasibility || unknown`, `Infeasibility = belowFloor || outsideDomain`; the order `needBelow` (cheaper below dearer, a known amount below unknown, unknown below infeasible); `Modulus F` with `need`, `floor`, `domain` and the audit's laws `StrongerNeedsNoLess`, `BelowTheFloorIsInfeasible`, `OutsideTheDomainPromisesNothing`, `InsideTheDomainSuffices`.
- §3: `Scaling F` (rate, exponent, grain) and `ScalesAs`: the least-squares slope of log(spent) on log(rate) equals the stated exponent, within E·Σ|x − x̄|/Sxx (x the log of each rate, x̄ their mean, Sxx the sum of squared deviations, E = log(n/(n − g)) for the least count n and grain g) plus a first-order room for rounding. A `Within` law whose range is its premise.

`examples/bisection.lut` (new): `bisect`, counting its steps; the features of a bracket (width, scale, whether it brackets a root); `bisectionModulus d` = `halvings L (b/(1+u) − 2a)` (L the width, b the bound, u the unit roundoff, a = ε·scale·(1+u) the rounding's room per step, derived in the comment); floor 4a(1+u); domain a sign change. Each law takes the algorithm as a parameter: `BisectionMeets` (`Within`: the root within b/2 + floor + the problem's blur), `NeedsNoMoreThanItsModulus`, `BisectionScalesAsStated` (`ScalesAs` with log₂(L/b), exponent 1, grain one step), the claim `BisectionModulusIsAModulus`.

`src/luthier/tester.py`: the scaling mode, for a numerical law with a parameter of type `Bound` bound to a census of two bounds or more: per bound, from the loosest, the cases, their worst ratio, and the fuel spent by the costliest and cheapest case (`scaling_record`), kept in `measured["scaling"]` and the entry ("fuel per case 1269 at b = 2 to 4268 at 1e-14 (9 bounds)"). It records and never judges; `ScalesAs` judges on the algorithm's own steps. `drawing_revision` unchanged (sha256:6cd60eb…); the record survives a store and a `--deep` replay.

## Acceptance

- Bisection's modulus against measured steps: `NeedsNoMoreThanItsModulus` passes on 44 cases (four problems at eleven bounds, from 2 down past the floor); its control `halvedModulus` refuted.
- Wrong exponent refuted: `BisectionScalesAsStated` passes at worst ratio 0.129 on two lists of bounds; exponent 2 refuted at ratio 4.95, exponent 1/2 at 2.48.
- `BisectionMeets` passes at worst ratio 1 − 3e-12 (tight by design); the control answering the low end of the last bracket refuted.
- `WorkSpanMemoryIsAResourceAlgebra` passes sampled (1200 cases) and on listed resources (264); eleven controls refute each of its 12 conjuncts at least once, the span that adds in parallel among them. The modulus's four conjuncts have one control each, all refuted.
- `luthier check` clean on resources.lth, resources_model.lut, examples/bisection.lut and both test programs.
- Tests: the new test in tests/test_tester.py failed before and passes after; test_tester, test_within, test_tester_conjunction 39 passed, 1 skipped; test_certify and test_regions 108 passed, 2 skipped, one deselected. Two failures predate the bite, both from 5ca7e15 (two table controls, 10 → 12): test_tester's count updated in 5703f2b; `test_certify::test_certify_lists_the_laws_of_tables_with_their_controls` left for the coordinator.
- Nothing certified (all `--no-cert`); new stores come from `tests/tester/resources_laws.test.lut` and `tests/tester/bisection_laws.test.lut`.

## Decisions taken on my own

1. resources.lth beside numbers.lth, not in the core: nothing in the core reads it, so the core's cones stay.
2. The mode recognized by the bound's type (`Bound`, through `SCALING_TYPES`, as `CUTOFF_TYPES` is), not a new constructor of test.lth's `Mode`.
3. The tester measures fuel and judges nothing; `ScalesAs` judges on the steps the algorithm counts (fuel per case is a setup cost plus about 65 per halving). Measured, sufficient and extrapolated stay apart; nothing extrapolates yet.
4. No `extrapolated` constructor in `Need` until the planner extrapolates (P8).
5. `InsideTheDomainSuffices`: a modulus promises an amount everywhere in its domain at or above its floor.
6. Bisection's floor is twice the least feasible one, so the modulus is finite at its floor; its memory is three values.
7. `sequence` stated commutative, since the record forgets order.
8. `ScalesAs`'s rounding room is first order, 4kε(1 + max|y| + |p|·max|x|), orders of magnitude below E for any count under 2^40.
