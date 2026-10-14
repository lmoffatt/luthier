# Review, round 1, bundle C (2710cfc)

## `generators.lth`

**1. Wrong**
- `Random := UniformInUnit & SeedMoves & UniformAtLevel & IndependentAtLevel`. `UniformAtLevel … := uniformPValue (draws r s l.n) >= l.alpha` is a Boolean law over every `s : Seed`, and a correct source fails it on a fraction α of seeds by construction; under laws.lth's `ForallOnPoints` one failing seed refutes, so at α = 0.05 a 100-seed sample refutes the correct source with probability ≈ 0.994. The comment "they hold on a fraction `1 - alpha` of seeds, which is what their certificate says" is not what the law says. Same for `IndependentAtLevel`. And `l : Level` is a quantified parameter: unless the demand binds it to `value`, the functor draws α uniformly in (0, 1).
- `Translates … := m.place (i.lo + c) (i.hi + c) v == m.place i.lo i.hi v + c` and `Scales … == k * m.place i.lo i.hi v`: exact `==` on `Float64`. Both reference metrics fail by rounding (cases under generators_model.lut §4). 5.S4: equality on doubles is a cost or carries a tolerance, and the tolerance is the demand's (D-2026-10-14-c).
- `Budgets … | positiveBudgets … and budgetMasses specialMass atomAtZero`: admits `specialMass = 0.9, atomAtZero = 0.9`, two masses whose sum exceeds 1 and leaves nothing for the continuous draw.

**2. Not determining**
- `Metric := WithinBounds & Grows & StartsAtLo`, `LinearMetric := LinearTranslates & LinearWithinAny`, `LogMetric := LogScales`: `place lo hi v := lo` is a model of all three (within bounds, grows weakly, starts at lo, translates, scales). And `linear` satisfies `Scales` exactly in the reals (`k·lo + v(k·hi − k·lo) = k(lo + v(hi − lo))`), so scaling does not separate log from linear, against the file's "What tells the two apart is the invariance that represents each". Missing: a normalisation (`place 0 1 v == v`, or that `place lo hi` fills [lo, hi)), and for log the conjugacy `log (place lo hi v) == log lo + v (log hi − log lo)`, which is what "uniform in the logarithm" says.
- `DrawIsTheFirstKept … := match f.draw tries n s { (m, s2) -> m == firstKept … }`: `s2` is discarded. `draw tries n s := (firstKept T base keep tries n s, s)` passes `Filter` and never advances the seed.
- `Resolution := ParameterWins & WhereWins & TypeBindsEveryParameter & NothingBindsNothing`: two wrong models pass all four — one that searches `whereBs` whole (parameter, then type) before `profile` (no law pits a type binding in `where` against a parameter binding in the profile), and one that ignores type bindings in `whereBs` altogether (`TypeBindsEveryParameter` only ever puts the type binding in the profile: `r.bindingOf nil [byType t g] x t`).
- `uniformPValue : List Float64 -> Float64`, `serialPValue`: declared outside `Random`; a host whose p-value is the constant `1.0` makes every source a model (gen.3 applies to them as it did to `pick`).
- `walk (T : U) (c : Census T) : Gen (Maybe T)`: the census generator has no theory; "walked in turn, each value once" is a comment, and nothing tells a wrong one apart.
- `Binding = { …, generator : String, coverage : Coverage }`, `byParameter x g := { …, coverage := Drawn 0 }`: nothing ties `coverage` to what `generator` names, and test.lth's `specCoverage` reads it as true.

**3. Roles**: no `data` in the file. None.

**4. Models**: see generators_model.lut.

**5. Against the specification**
- 7.S17 / 5.S12: a statistical law "returns its statistic, its level α and its outcome", never a refinement; `UniformAtLevel : Bool`, and 7.S18's repeat with an independent seed has nowhere to go (laws.lth's `Law` has no statistical form; see there).
- 7.R4 types a census binding `Gen T` (`likelihoods : Gen (Likelihood FullCoords) := census […]`); `walk` gives `Gen (Maybe T)`, and `from f` members are absent.
- 7.S7 "the earlier ones are drawn again, up to a budget": `dependent … := fn n s { match ga n s { (x, s2) -> match gb x n s2 …` has no redraw and no budget, and `gb : (x : A) -> Gen (B x)` has no value when `B x` is empty.
- 7.R3 "Lists are enumerated up to the size" and `Bounded n`: `Enumeration … : { all : List T }` with `ReachesEvery` needs a finite `all`, so a bounded enumeration of `List A` has no theory here (§8's todo may be where it lands; say so).
- 7.S6 / 7.S12: `draw : Nat -> Nat -> Seed -> Maybe T * Seed` records neither the acceptance rate nor the reason the law is not run.
- 7.S8: `Level : U := { alpha : Float64, n : Nat | … }` carries the count of draws that `Budgets.distributionDraws` also carries; one budget, two homes.

**6. Implication over a type**
- `ProportionalToWeight … := not (occurs T s.weights x) or 0.0 == weightOf T s.weights x or …` over `x : T`: for a support of three values of a large `T` the premise is almost never met; quantify over the entries of `s.weights` (an index below its length).
- `Scales … (k : Float64) … := not (0.0 < k) or …`: over `{ k : Float64 | 0.0 < k }`.
- `CensusFirst … (i : Seed) := match nth (Violating v) c.census i { nothing -> true ; …`: a seed below the census's length is a 10⁻⁹ fraction of `Seed`; quantify over an index below `lengthOf c.census`. Same for `CleanCensusFirst`.

**7. First**: restate `UniformAtLevel` / `IndependentAtLevel` so that the intended source is a model — as the law of the fraction of seeds a certificate records, or as 7.S17's statistical form once `Law` has one. Every generator rests on `Random`, and as written the reference source cannot be certified.

**8. Cutoffs**: none; `Level` and `tries` are parameters.

**9. Missing generators**
- `Grows` over `OrderedUnitPair`; `WithinBounds`, `StartsAtLo`, `Scales` over `PositiveInterval`; `Translates`, `WithinAnyBounds` over `Interval`: records of two unbounded `Float64` with a predicate relating them — not an interval predicate on one field (7.S6), and an unbounded double is a static error (7.S4). Need `Gen Interval`, `Gen PositiveInterval`, `Gen OrderedUnitPair` (a bounded `lo`, a positive gap drawn `log`, `hi := lo + gap`); `c`, `k : Float64` need bounds likewise.
- `ParameterWins` … `NothingBindsNothing` over `x t g h : String` and `List Binding`: 7.S3's table has no `String`; need `Gen String` (names from a small pool, as §7 describes for programs).
- `NonNegative`, `PickedHasWeight`, `ProportionalToWeight` over `s : Support T`: a model of a theory, so today a census of the supports a test lists (7.R4); `Gen { ws : List (T * Float64) | allNonNegative T ws }` would make `supportOf` a family (`from supportOf`).

## `generators_model.lut`

**1. Wrong**: `UniformSampleIsUniform (l : Level) (size : Nat) (seed : Seed) : Bool` — same as `Random` above: a correct `uniformSample` fails on a fraction α of seeds and one seed refutes it.

**2. Not determining**: `ClearDiagonalGivesClear … d.f k == 0.0 or (1.0 <= abs (d.f k) and abs (d.f k) <= 1000.0)` restates the type's predicate, which the tester already checks on every value (7.S1). What the families claim beyond their type has no law: `clearDiagonal`'s atom at 0.25 and log-uniform magnitude, `unitList`'s atom at 0.2, `gram`'s "rank deficient in most draws", `orthogonal`'s Haar (7.S5 cites Mezzadri precisely because the type cannot see it; 7.S1: "a family that claims a distribution states it as a law").

**3. Roles**: none (no `data`).

**4. Models against theories** (the first two checked numerically)
- `linearMetric` vs `LinearTranslates`: `i = {lo := 0.1, hi := 0.7}`, `c = 0.2`, `v = 0.5`: `linear.place 0.3 0.9 0.5 = 0.6`, `linear.place 0.1 0.7 0.5 + 0.2 = 0.6000000000000001`. About 22% of random cases fail.
- `logMetric` vs `LogScales`: `i = {lo := 0.1, hi := 1.0}`, `k = 3.0`, `v = 0.5`: `0.9486832980505139` vs `0.948683298050514`. About 40% fail.
- `supportOf` vs `ProportionalToWeight`: `weights := [(true, 1.0), (false, 1.0), (true, 1.0)]`, `x := true`, `v := 0.6`. `weightOf` sums both occurrences (2.0), `before` stops at the first (0.0), so the law asks `pick 1.2 == just true`; `pick` gives `just false`. Either `Support` needs a law that the keys are distinct, or `before` and `weightOf` must agree on which occurrence they mean.
- `filterOf`, `resolution`: hold by construction.

**5. Against the specification**
- 7.S5: dimensions come from the census `0, 1, 2, 3, 5, 10`, changeable by a binding; `symmetric` draws "a size between 1 and the size" inside the extern.
- 7.S8: the atom masses are budgets of the test, "recorded in the entry"; `unitList := fn size seed { hostGenerators.unitListWith 0.2 size seed }` and `clearDiagonalWith 0.25 1.0 1000.0` fix them in the value while the comment claims P11.
- 7.S17: `UniformSampleIsUniform` as a `Bool`, as in generators.lth 5.

**6.** None.

**7. First**: lift `0.2`, `0.25`, `1.0`, `1000.0` out of `unitList`, `clearDiagonal` and `ClearDiagonalGivesClear` into arguments the budgets and the type supply. These are the families sonolocalización's tests will bind, and a mass fixed in a value cannot be recorded in the entry (7.S8, L5.18).

**8. Cutoffs**: `hostGenerators.unitListWith 0.2`, `clearDiagonalWith 0.25 1.0 1000.0`, and `1.0 <= abs (d.f k) and abs (d.f k) <= 1000.0`. The masses are 7.S8 budgets; the bounds are the type's (7.S4) and should be read from `ClearDiagonal`, not repeated. `tol : Tolerance`, `fl : RankFloor`, `l : Level` are parameters, as they should be.

**9.** None missing (`size : Nat`, `seed : Seed`, `k : Dim` are generic). But `tol`, `fl`, `l` are cutoffs the law quantifies: unless bound to `value`, a tolerance drawn linear in its interval makes each case a different test.

## `test.lth`

**1. Wrong**
- `RunIsPointsOrNotRun … := match t.run s { Points A pts c -> true ; NotRun r -> true ; _ -> false }`: a law that is not a top-level `forall` (a `Case`, 5.S1's "term valued in Bool"; a `Both`; an `Exists`) gives `Evaluated`, `Pair`, `At`, and the correct tester is refuted on it. With it `CountsCases`: for such a law under `SampledMode`, `pointCount (t.run s) == s.cases` reads `0 == cases`.
- `specCoverage s := bindingsCoverage s.profile (bindingsCoverage s.whereBindings (modeCoverage …))` is not 7.S10's "weakest of the reach of each parameter": it folds every binding present, including a profile binding `resolve` overrides and bindings of parameters the law does not have, and the mode even when every parameter is bound. Case: `ExhaustiveMode`, `whereBindings = [byParameter "x" "census"]` with coverage `Listed`, `profile = [byParameter "x" "sampled"]` with `Drawn 0`; `x` resolves to the census, the run's coverage is `Listed`, `specCoverage` and `wholeCoverage` are both `Drawn 0`, and `CoverageIsTheWeakest` (`c == specCoverage s or c == wholeCoverage s`) refutes the correct tester. The equality is structural, so with `seed ≠ 0` a tester reporting `Drawn seed` against a binding's `Drawn 0` is refuted on the seed alone.

**2. Not determining**
- `Grading : { gradeOf : Verdict -> Maybe Coverage -> Maybe Grade, … }`: the grade of `Confirmed` depends on the law's form (a `forall` over `Exhaustive` is exhaustive; an `exists` on the same points is a witness, cases, as the file says), which `gradeOf` does not receive. `GradesAsTerms` leaves `Confirmed` with `Bounded n` and `Listed` unstated; the reference `grade` picks `just ExhaustiveGrade` for the first, which is wrong: under laws.lth's `ForallOnPoints` a `forall` on bounded points is `Supported`, so `Confirmed` with `Bounded` only ever comes from a witness.
- `CoverageIsTheWeakest`, sampled branch `rankOf c <= rankOf (specCoverage s)`: `specCoverage` under `SampledMode` is always `Drawn`, so a tester reporting `Drawn` for a run whose every parameter came from a census (7.S10: cases) passes.
- `CountsCases` through `pointCount`: counts the outer `Points` only; if a two-parameter law's evidence is nested `Points`, it counts values of the first parameter, not cases; and it counts points whose evidence is `NotRun` (7.S12 counts evaluated cases).

**3. Roles**: `SampledMode : Metric -> Mode`: the `Metric` carried has no law in the file (`modeCoverage` drops it: `SampledMode k -> Drawn s`); 7.R1 gives it the role of drawing every numeric parameter.

**4. Models**: see test_model.lut.

**5. Against the specification**
- D-2026-10-13-aa Q5 / 4.R10: `Grading` is a theory with one model whose laws (`GradesAsTerms`, `GradesAreOrdered`) restate `grade` and `gradeRank` case by case — the pattern laws.lth §1 explicitly refuses for the verdicts.
- 7.S12: `pointCount` counts points, not evaluated cases; nothing counts the cases whose premise was false.
- 7.S20 "each option is a named argument with a default": `test (law : String) (mode : Mode) …` gives `mode` none.
- "The grades are ordered by the evidence cost they carry (L10.2 …)": L10.2 gives `cases` cost ∞ outside its listed points and `sampled` a finite cost on its distribution; neither is below the other without a domain, so the total order is the file's, not L10.2's.

**6.** `CountsCases … := match s.mode { SampledMode k -> … ; _ -> true }`: vacuous on every exhaustive spec; quantify over sampled specs. Minor.

**7. First**: compute the run's coverage per parameter of the law as `resolve` binds it (7.R1), the mode counting only for the parameters it draws, and compare coverages by `rankOf` everywhere. The grade is read from this value; as written a correct tester is refuted and a wrong coverage is certified.

**8. Cutoffs**: none; `defaultBudgets` are the defaults 7.S8 asks `test` to take, not cutoffs in D-2026-10-14-c's list.

**9.** `RunIsPointsOrNotRun`, `CoverageIsTheWeakest`, `CountsCases` over `s : TestSpec`: `String` fields, a `Mode` carrying a `Metric` (a model of a theory, 7.R4), `Budgets` with `Float64` fields unbounded in their types (7.S4) — no functor applies. Need `Gen TestSpec` as a family from `Gen String`, a census of `Mode` (`ExhaustiveMode`, `SampledMode linear`, `SampledMode logarithmic`) and `Gen Budgets`. `GradesAsTerms (g) (s n : Nat) (r : String)`: `Gen String`.

## `test_model.lut`

**1–3.** None.
**4.** `grading` satisfies `GradesAsTerms` and `GradesAreOrdered` by construction; what it decides beyond them (`Confirmed` with `Bounded n` → `ExhaustiveGrade`) is the wrong choice, test.lth 2.
**5–6.** None.
**7.** `grade`'s `Bounded n -> just ExhaustiveGrade` under `Confirmed` → `just Cases`, until `grade` receives the law's form.
**8–9.** None.

## `laws.lth`

**1. Wrong**
- `NotFlips … := m.settles (Not p) e == flip (m.settles p e)` and `CitedWhole (m) (p : Law) (r) := m.settles p (Cited r) == Cites r` are unsatisfiable together: at `p := Not q`, `CitedWhole` gives `settles (Not q) (Cited r) == Cites r`, while `NotFlips` gives `flip (settles q (Cited r)) == flip (Cites r) == Unsettled`. Same with `AssumedWhole` (`flip Assumes == Unsettled`). `Settling` has no model. (`NotRunIsUnsettled` is consistent: `flip Unsettled == Unsettled`.)
- `ForallOnPoints`: `else if allConfirmed (pointVerdicts …) then (match c { Exhaustive -> Confirmed ; _ -> Supported })`. A law with two quantified parameters is `Forall A (fn a -> Forall B …)` and its evidence `Points A [(a, Points B … c')]`; unless `c'` is `Exhaustive` every inner point is `Supported`, `allConfirmed` fails, and the outer is `Unsettled`. No sampled or bounded law with more than one parameter settles anything, where 7.S10 grades it by the weakest reach. `EitherBySide`'s `isConfirmed` drops `Supported` the same way.
- `EitherRefutedByBoth`: `Pair e f` where `e` confirms `p` gives `Unsettled`; a confirming side is sound evidence for the disjunction, and "or by one side" is a shape, not a reason to discard it. Lesser.

**2. Not determining**
- `Settling` leaves evidence of another form free: nothing states `settles (Forall A p) (Evaluated b)`, `settles (Case c) (Points …)`, `settles (Both p q) (Side …)`, `settles (Exists A p) (Pair …)`. The model that returns `Confirmed` for every mismatched pair passes every law; "evidence cannot lie" needs `settles l e == Unsettled` when `e` does not fit `l`'s form.
- `CombineAbsorbs` leaves `combine (Cites r) (Cites r')` and `combine Assumes v` free, so a model may turn two citations into `Confirmed` — a grade raised without evidence (L10.9).

**3. Roles**
- `Bounded : Nat -> Coverage ; Drawn : Nat -> Coverage`: the `Nat` carried has no law ("whatever a bound's size or a draw's seed") and `rankOf` discards it; `Drawn`'s is a seed typed `Nat` where generators.lth's is `Seed`. Either the payload gets a role (the box `Bounded` names; the seed L10.4 hashes) or it goes.
- `Then : Law -> Law -> Law` has a role (`ThenIsMaterial`), but the role says it *is* `Not (Both p (Not q))`: a definition, not a constructor (L2.7).

**4.** No model file in the bundle.

**5. Against the specification**
- 7.R2: "a test of a law quantified over a parameter of type `U` [is a] static error". `ForallAtOnePoint (m : Settling) (A : U) (p : A -> Law) …`, `ForallOnPoints`, `ExistsAtOnePoint`, `ExistsOnPoints`, and `VerdictsAreExact (C : U) (s : CostScale C) (b : Bool) (E : U) (fs : Failures E)` quantify `A` and `E` in the law, not in the theory's parameters (`Settling` has none; `CostScale C` has `C`, not `E`). They cannot be tested as written.
- 7.S12 "A law whose premises never held passed vacuously, and its entry says so": `Evidence` and `Verdict` have no place for a premise that was false (`Then` with `p` refuted is `Confirmed`, indistinguishable from a checked case), nor for 7.S12's counts.
- 7.S17 / 7.S18: `Law` has no statistical form (statistic, level, outcome; the repeat with an independent seed), which is why generators.lth's source laws had to be Boolean.
- D-2026-10-13-aa Q5: `Covering : { rank : Coverage -> Nat }` with `CoveragesAreOrdered` is a one-model theory restating `rankOf`; test.lth reads `rankOf` and `weaker` directly, so `Covering` has no client.

**6.** §2: `isSymmetric … := not (r x y) or r y x`, `isAntisymmetric`, `isTransitive` are implications over `x y (z) : A`. The file says the client must quantify over related pairs; the template could take `(p : { x y : A | r x y })` and leave the client no way to get it wrong.

**7. First**: make `ForallOnPoints` give `Supported` when every point confirms or supports, `Confirmed` only when all confirm under `Exhaustive`. Without it no multi-parameter sampled law can be supported, and that is nearly every law in the bundle. (The `NotFlips`/`CitedWhole` conflict is a one-line fix — restrict `NotFlips` to evidence that is not `Cited`, `Assumed` — but the `forall` change is what every certificate's meaning turns on.)

**8. Cutoffs**: none.

**9.** `BothByPair`, `EitherBySide`, `EitherRefutedByBoth`, `NotFlips`, `ThenIsMaterial`, `CitedWhole`, `AssumedWhole`, `NotRunIsUnsettled` over `p q : Law`, `e f : Evidence`: both `data` carry `(A : U)` (`Forall`, `Exists`, `At`, `Points`), so no functor draws them (7.R2). Need a sized generator of `Law` and of `Evidence` over a census of carriers (`Bool`, `Fin 3`) — the first instance of 7.S3's proposed rule for recursive `data`. `CitedWhole (r : String)`, `NotRunIsUnsettled (r : String)`: `Gen String`. `VerdictsAreExact` over `fs : Failures E`: a generator of `Failures` at a fixed `E`.

## On the specification itself

- 7.R1 does not say which wins between a type binding in `where` and a parameter binding in the profile; `resolve` chooses the parameter, and the laws say nothing (generators.lth 2).
- 7.S10 orders the five grades; L10.2's evidence costs do not order `cases` against `sampled` without a domain (test.lth 5).
- 7.R2's static error on `(A : U)` meets D-2026-10-13-l's `Forall : (A : U) -> …`: as stated, the spec makes the laws of `Law` itself untestable unless "certified per filling of the hole" extends to an `A` quantified inside a law. The rule should be stated.

## Not sure

- `power`, `uniformPValue`, `serialPValue` are declared with no body; `StartsAtLo` for `logarithmic` needs `power x 0.0 == 1.0` exactly, true of the host's `pow`, not of the file.
- `GramGivesPsd … numpy.retainedRank fl (mscaleDef (0.0 - 1.0) a) == 0`: if `retainedRank` counts singular values above the floor, `-a` has the same ones as `a` and the law demands `gram ≈ 0`, false of the model; if it counts eigenvalues above the floor it reads as intended. arrays.lth is not in the bundle.
- generators_model.lut imports `UniformAtLevel` from probability.lth and `Level` from generators.lth, whose own `UniformAtLevel` it does not import: whether the two `Level`s are one type; `l.n` is unused by a test on a given `vs`.
- `Seed` is a subtype of `Int` and is passed where `Nat` is expected: `nth (Violating v) c.census i`, `Drawn s` in `modeCoverage`, `walk`'s `s mod lengthOf T c`. Type-checking is out of scope.
- `CostScale (C : U) := … & VerdictsAreExact C` names `VerdictsAreExact` before its definition; it parses, whether order matters I cannot tell.
- `WithinBounds` for `linear` and `logarithmic`: no overshoot of `hi` in 10⁶ random cases with `v` within 10⁻¹⁵ of 1; not proved.
- Whether the tester nests `Points` for multi-parameter laws or flattens them to one `Points` over a product. laws.lth 1 and test.lth 2 assume nesting (D-2026-10-13-l, "evidence follows the form", and `Forall` binds one variable); under flattening `pointCount` is right and `ForallOnPoints` holds.
- What `symmetric` gives at size 0 ("a size between 1 and the size").
- Who sets `Binding.coverage`, the author of the binding or the tester from the generator's kind; 7.R1 does not say.