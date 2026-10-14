Below, per file, by the prompt’s numbers; “—” means nothing to report from these files.

## `generators.lth`

1. **Laws that are wrong.**  
   `Random := UniformInUnit & SeedMoves & UniformAtLevel & IndependentAtLevel` is unsatisfiable as a universal theory: `UniformAtLevel` and `IndependentAtLevel` are statistical (`uniformPValue ... >= l.alpha`, `serialPValue ... >= l.alpha`) and false on a fraction `α` of seeds, yet they are conjoined over all `s : Seed` and `l : Level`. Also `ProportionalToWeight ... or s.pick (before ... + weightOf ... * v) == just x` is false when the same `x` occurs more than once in `ws`: `weightOf` sums all occurrences, while `before` is only before the first. And `LogScales ... := not (0.0 < k) or m.place ...` uses undefined `m`; it should be `l.metric.place`.

2. **Laws that do not determine what they claim.**  
   `Resolution := ParameterWins & WhereWins & TypeBindsEveryParameter & NothingBindsNothing` misses the precedence “profile parameter over `where` type” from 7.R1. A model that returns a `where` type binding when a profile parameter binding exists passes all four. `CensusFirst ...` and `CleanCensusFirst ...` only constrain size `0`; a model giving arbitrary programs for `n > 0` passes `RuleCases`.

3. **Roles (L2.7).** — none in this file.

4. **Models against theories.** — not here.

5. **Against the specification.**  
   `dependent ... := fn n s { match ga n s { (x, s2) -> match gb x n s2 ... } }` lacks the `redraws` budget for empty `B x` required by 7.S7.  
   `walk (T : U) (c : Census T) : Gen (Maybe T)` is not a generator of `T` as 7.S1 defines `Gen T`; a census binding should give `T`, or the `Maybe` must be accounted for.

6. **Implication over a type.** — the file itself notes the alternatives in `isSymmetric`, `isAntisymmetric`, `isTransitive` and says theories quantify over related pairs.

7. **What I would change first.**  
   Fix `Random` so the statistical laws are not universal conjuncts of the theory; otherwise no model can satisfy it. Reason: 7.S17 says a statistical law declares its level and outcome, not that it holds for every seed.

8. **Cutoffs.**  
   `byParameter (x g : String) : Binding := { ..., coverage := Drawn 0 }` hardcodes seed `0` in a helper; if the seed is a cutoff, it belongs to the demand/binding.

9. **Missing generator.**  
   `Random` for its laws `UniformInUnit`, `SeedMoves`, `UniformAtLevel`, `IndependentAtLevel`. Type: `Random`. Needed: a census of `Random` models, per 7.R4.

## `generators_model.lut`

1. **Laws that are wrong.** — none.
2. **Laws that do not determine what they claim.** — none.
3. **Roles (L2.7).** — none.
4. **Models against their theories.**  
   `supportOf (T : Concrete) (ws : List (T * Float64)) : Support T := { weights := ws, pick := fn u { pick T ws u } }` breaks `NonNegative T s` when `ws` has a negative weight. Also `UniformSampleIsUniform` is statistical; if made a law, it fails on some seeds.
5. **Against the specification.** — none.
6. **Implication over a type.** — none.
7. **What I would change first.**  
   Make `supportOf` require nonnegative weights, or take a proof, so it is actually a model of `Support T`.
8. **Cutoffs.**  
   `unitList : Gen UnitList := fn size seed { hostGenerators.unitListWith 0.2 size seed }` hardcodes the atom probability `0.2`.  
   `clearDiagonal : Gen ClearDiagonal := fn size seed { hostGenerators.clearDiagonalWith 0.25 1.0 1000.0 size seed }` hardcodes atom `0.25` and bounds `1.0`/`1000.0`. Per 7.S8 these should be budgets/parameters.
9. **Missing generator.** — none here.

## `test.lth`

1. **Laws that are wrong.** — none.
2. **Laws that do not determine what they claim.**  
   `CoverageIsTheWeakest ... _ -> rankOf c <= rankOf (specCoverage s)` only compares rank in sampled mode. A wrong model can return `Drawn 999` instead of `Drawn s.seed` and pass, if the seed is meant to be part of the coverage.
3. **Roles (L2.7).**  
   `Mode : U := data { ExhaustiveMode : Mode ; SampledMode : Metric -> Mode ; }` has no law of its constructors’ roles in the file; `CoverageIsTheWeakest` is a law of `Tester`, not of `Mode`. Similarly `Grade`’s roles are stated only in `Grading`.
4. **Models against theories.** — none.
5. **Against the specification.** — none clear; `defaultBudgets` are defaults allowed by 7.S8.
6. **Implication over a type.** — none.
7. **What I would change first.**  
   Force `CoverageIsTheWeakest` to equate the coverage exactly, including the seed for sampled mode, or explicitly state that the seed is irrelevant.
8. **Cutoffs.**  
   `defaultBudgets ... specialMass := 0.05, atomAtZero := 0.01` are constants in the file. If they are cutoffs, they should be demand parameters, not defaults.
9. **Missing generator.**  
   `Tester` for `RunIsPointsOrNotRun`, `CoverageIsTheWeakest`, `CountsCases`. Type: `Tester`. Needed: a census of `Tester` values, per 7.R4.

## `test_model.lut`

1–9. — none. `grading` satisfies `Grading`.

## `laws.lth`

1. **Laws that are wrong.**  
   `ForallOnPoints ... else if allConfirmed (pointVerdicts m A p pts) then (match c { Exhaustive -> Confirmed ; _ -> Supported })` gives `Supported` for `Bounded`, but 7.S10 says bounded is exhaustive on the box the domain names; it should be `Confirmed` on that box. Also `CostScale C := ZeroIsExact C & TopIsNotExact C & VerdictsAreExact C` uses `VerdictsAreExact` before it is defined, if forward references are not allowed.

2. **Laws that do not determine what they claim.** — none clear; `CoveragesAreOrdered` only orders ranks, but `weaker` uses the fixed `rankOf`.

3. **Roles (L2.7).**  
   `Law : U := data { ... }`, `Evidence : U := data { ... }`, `Verdict : U := data { ... }` have no `Law := ...`, `Evidence := ...`, `Verdict := ...` role laws of their own; their roles are stated only in `Settling` laws. Under L2.7 this may be a collection unless `Settling` is accepted as their role law.

4. **Models against theories.** — none here.

5. **Against the specification.**  
   `ForallOnPoints` against 7.S10, as in item 1.

6. **Implication over a type.** — none; §2 notes the implication issue and says theories quantify over related pairs.

7. **What I would change first.**  
   Fix `ForallOnPoints` to treat `Bounded` as `Confirmed` (exhaustive on the named box), matching 7.S10.

8. **Cutoffs.** — none clear.

9. **Missing generator.**  
   `Settling` for its laws (`ForallOnPoints`, `ExistsOnPoints`, `BothByPair`, etc.). Type: `Settling`. Needed: a census of `Settling` models, per 7.R4.

## `07-tests.md` and `05-laws.md`

These are specification chapters, not theory files. No file-level law issues to report beyond the contradictions already noted against them.

## Not sure

- Whether Luthier permits forward references in theory definitions (`CostScale` using `VerdictsAreExact` before definition).
- Whether `Concrete` guarantees finite types for `Enumeration`.
- Whether `Failures`/`isEmpty` import exists as used.
- Whether `walk` returning `Gen (Maybe T)` is intended to be composed with a budget, or is a type error.
- Whether `Drawn 0` in `byParameter` is a placeholder or a cutoff.
- Whether `Grade`/`Mode` role laws in `Grading`/`Tester` satisfy L2.7 or must be in the data’s own theory.