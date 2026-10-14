I found several real semantic failures, not just incompleteness. The most serious are: `Support` rejects one of its own reference models when weights contain duplicate values; `Tester` admits the tester that always returns `NotRun`; `Coverage` can be forged strongly enough to “prove” a false `forall`; the metric theories do not characterize the distributions they name; and the current Boolean-only decision D-2026-10-14-c is not yet reflected in `laws.lth`/`05-laws.md`. C-prompt

## `generators.lth`

1. **Laws that are wrong.** `ProportionalToWeight` is false of the reference `supportOf` when the same value occurs twice. Quote: `weightOf` sums *all* occurrences, while `before` stops at the *first* occurrence, then the law uses `before ... + weightOf ... * v`. C-prompt  
   Counterexample: weights `[(x,1),(y,1),(x,1)]`, `x != y`, `v=0.75`. Then `before(x)=0`, `weightOf(x)=2`, so the law asks `pick 1.5 == just x`; `pick 1.5` returns `y`.

2. **Laws that do not determine what they claim.** `LinearMetric` admits `place lo hi v = lo` for every `v`. It is within bounds, monotone, starts at `lo`, and commutes with translation. Likewise it is a model of the scale-invariant theory if used for `LogMetric`. Thus a generator concentrated entirely at the lower endpoint passes a theory described as “linear”/“log” sampling. C-prompt  
   Separately, `Filter` does not constrain the returned next seed: a `draw` returning the correct `Maybe T` but always returning the input seed passes both laws. C-prompt

3. **Roles (L2.7).** No locally defined `data` here, so no direct constructor-role failure.

4. **Models against theories.** See `generators_model.lut`: `supportOf` actually exposes the duplicate-value counterexample above.

5. **Against the specification.** Two concrete mismatches. First, the comment says an empty dependent component redraws the first component up to the `redraws` budget, but `dependent` has no budget, no failure case and no redraw. C-prompt Second, a census is said to be walked “each value once”, but `walk` uses `s mod length`, so it cycles forever. C-prompt

6. **Implication over a type.** `Scales ... (k : Float64)` is exactly the forbidden shape: `not (0.0 < k) or ...`. Quantify over `{ k : Float64 | 0.0 < k }` instead. C-prompt

7. **Change first.** Fix the support representation/law: either supports are duplicate-free, or proportionality must be stated per occurrence rather than aggregating duplicate weights. Right now an advertised reference model can fail its theory.

8. **Cutoffs.** None found. `0`, interval endpoints, seed modulus, etc. are domain/algebra constants, not acceptance cutoffs.

9. **Missing generator.** The important missing generic generator is the specification's `value v`. `UniformAtLevel` has a demand-supplied `l : Level`; under D-2026-10-14-c it should be bound by something like `value l : Gen Level`, not randomly chosen or hand-listed. The specification explicitly includes `value v`, but `generators.lth` does not implement it. C-prompt

## `generators_model.lut`

1. **Laws that are wrong.** No independent contradiction beyond the theory failures above.

2. **Laws that do not determine what they claim.** The clearest case is `orthogonal`: the comment claims Haar-distributed orthogonal matrices, but the only law checks `QᵀQ ≈ I`. A generator returning the identity matrix every time passes and is maximally non-Haar. C-prompt The same pattern occurs for the stated atom/log-uniform distributions of `unitList` and `clearDiagonal`: their laws check support, not those distributions. C-prompt

3. **Roles (L2.7).** No `data` defined here.

4. **Models against their theories.** `supportOf (T) (ws) : Support T` breaks `ProportionalToWeight` for `ws=[(x,1),(y,1),(x,1)]`, as above. The model is declared for arbitrary `List (T * Float64)`, so this is a genuine model failure, not merely a hypothetical bad implementation. C-prompt

5. **Against the specification.** `orthogonal` explicitly claims Haar distribution, while 7.S1/7.S5 require a family claiming a distribution to state that distribution as a law; no such law appears. C-prompt

6. **Implication over a type.** None.

7. **Change first.** Stop declaring arbitrary `supportOf ... ws` as `Support T` until duplicate support entries have defined semantics.

8. **Cutoffs.** The actual acceptance criteria are correctly parameters: `fl : RankFloor`, `tol : Tolerance`, `l : Level`. The literals `1.0` and `1000.0` are described as `ClearDiagonal`'s support bounds, not cutoffs. C-prompt

9. **Missing generator.** The three obvious demand parameters need singleton/value generators: `GramGivesPsd` needs `value fl : Gen RankFloor`; `OrthogonalGivesOrthogonal` needs `value tol : Gen Tolerance`; `UniformSampleIsUniform` needs `value l : Gen Level`. The missing generic `value` generator is therefore already blocking the correct reading of these laws. C-prompt

## `test.lth`

1. **Laws that are wrong.** The fixed `gradeRank` is not an ordering “by the evidence cost they carry”, as the comment claims. Every sampled certificate becomes the same `Sampled` rank, although L9.6 says sampled grade depends on the sampled distribution, and L10.2 derives grade from domain/evidence cost. `Cases > Sampled` is likewise not a universal comparison of evidence on different domains. C-prompt C-prompt

2. **Laws that do not determine what they claim.** A completely useless tester passes every law:
   `run = fn s { NotRun "always" }`.  
   `RunIsPointsOrNotRun` accepts it; `CoverageIsTheWeakest` returns true when coverage is absent; `CountsCases` explicitly accepts `NotRun`. C-prompt

3. **Roles (L2.7).** `SampledMode : Metric -> Mode` has no law giving the `Metric` payload a role in running the test. `modeCoverage` throws the metric away, and no `Tester` law requires `run` to draw according to it. Thus a tester ignoring the metric entirely still passes. C-prompt C-prompt

4. **Models against theories.** `test_model.lut` does not break the current `Grading` laws.

5. **Against the specification.** 7.S20 says **each option**, including mode, has a default; here `mode : Mode` has no default while cases, size, seed, bindings and budgets do. C-prompt C-prompt  
   More importantly, 7.S10 says the entry retains the reach **of each parameter** and only summarizes the grade by the weakest. `specCoverage` instead folds every binding into one `Coverage`, losing parameter/domain identity. C-prompt C-prompt

6. **Implication over a type.** None.

7. **Change first.** Close the all-`NotRun` model: a `NotRun` result needs a law tying it to an actual permitted failure to obtain a case—budget exhaustion, empty generator, etc.

8. **Cutoffs.** No violation. The numerical values in `defaultBudgets` are defaults for parameters, not law cutoffs baked into predicates. C-prompt

9. **Missing generator.** `RunIsPointsOrNotRun`, `CoverageIsTheWeakest` and `CountsCases` quantify over `s : TestSpec`; the bundle contains no `Gen TestSpec`, and the generic record functors are still TODO. Testing a `Tester` therefore needs hand-listed `TestSpec`s today. C-prompt

## `test_model.lut`

1. **Wrong laws.** None local.

2. **Underdetermination.** None additional; it simply chooses the reference functions.

3. **Roles.** No `data`.

4. **Model against theory.** `grading := { gradeOf := grade, below := ... }` satisfies the written `Grading` laws exactly. C-prompt

5. **Against specification.** No independent mismatch; it inherits the problematic fixed grade ranking from `test.lth`.

6. **Implication.** None.

7. **Change first.** No local change before fixing the meaning of `Grading` in `test.lth`.

8. **Cutoffs.** None.

9. **Missing generator.** None specific to this file.

## `laws.lth`

1. **Laws that are wrong.** `ForallOnPoints` trusts the `Exhaustive` tag without establishing that the points exhaust the domain. Since `allConfirmed nil == true`, `Points Bool nil Exhaustive` can confirm even a false `forall`. For example let `p false = Case false`; with `pts=nil`, `anyRefuted=[]` is false and `allConfirmed=[]` true, so the law demands `Confirmed`. C-prompt The dual problem lets empty `Exhaustive` points refute an `exists`. C-prompt

2. **Laws that do not determine what they claim.** `combine` is badly underconstrained. A commutative associative operation with priorities `Refuted` absorbing, then `Unsettled`, `Confirmed` neutral, and **every combination of two remaining verdicts = Assumes** satisfies the three written combination laws. It therefore allows two `Supported` pieces—or two citations—to turn into `Assumes`. Nothing forbids it. C-prompt

3. **Roles (L2.7).** `Coverage` is the clearest violation. Its purported role law is only the tag ordering, and explicitly says it holds “whatever a bound's size or a draw's seed”. Thus the payload of `Bounded n` and `Drawn s` has no role at all. That is exactly the kind of constructor-listing/order law L2.7 warns against. C-prompt

4. **Models against theories.** No `laws_model.lut` is included, so I cannot check an intended `Settling` or `Covering` model.

5. **Against the specification / decisions.** Three problems:
   - The file says `Law` will gain a cost-valued case when the cost library arrives. D-2026-10-14-c in this review says every law is Boolean. Those cannot both stand. C-prompt
   - It says the *verdict* combination of a conjunction “is the demand's” and cites 5.S8. But 5.S8 makes the **combination of grades** demand-selectable; it does not make logical settlement of `p ∧ q` demand-selectable. C-prompt
   - `ForallOnPoints` treats every non-`Exhaustive` coverage, including `Bounded`, as merely `Supported`, while 7.S10 says bounded is exhaustive on the box its domain names. `test.lth` then gives `Supported + Bounded` the exhaustive grade. The layers disagree. C-prompt C-prompt

6. **Implication over a type.** `isSymmetric`, `isAntisymmetric`, and `isTransitive` use material implication over arbitrary `x,y,z`; the file itself acknowledges their premises will rarely hold under random sampling. The actual law should quantify over the related-pair/related-chain subtype. C-prompt

7. **Change first.** Give `Coverage` actual semantics and make `Points ... coverage` valid only when the points justify that coverage. Until that is done, `Exhaustive` is a forgeable tag and the quantifier semantics are unsound.

8. **Cutoffs.** No hard-coded law cutoff found.

9. **Missing generator.** `ForallOnPoints` quantifies over `p : A -> Law`. At an infinite `A`, 7.R4 says such a function has no generic generator; testing a `Settling` model needs an explicit census/family generator for `A -> Law`, e.g. `census [from predicateFamily1, ...]`. The bundle supplies none. C-prompt

## `07-tests.md`

1. **Wrong laws.** N/A; this is specification, not a theory file.

2. **Underdetermination.** N/A.

3. **Roles.** N/A.

4. **Models.** N/A.

5. **Specification itself.** Two defects:
   - 7.S12 says a law with **no evaluated cases is `NotRun`**, then two sentences later says a law whose premises never held **passed vacuously**. If false premises do not count as evaluated cases—as the same paragraph says—those outcomes conflict. C-prompt
   - 7.S11 states `ε̂ = 3/n` at 95% confidence. The “rule of three” is an approximation; as literally written it gives `ε̂ > 1` for `n=1,2`, making `-log(1-ε̂)` undefined. The exact zero-failure upper bound, or at least clipping at 1, is needed if small `n` is allowed. C-prompt

6. **Implication over a type.** No concrete law here, but 7.S12's handling of false premises must not be taken as permission to encode a rare intended domain through implication; that contradicts the review rule.

7. **Change first.** Resolve the 7.S12 contradiction, because it changes whether a test produces no evidence or a passing certificate.

8. **Cutoffs.** No offending constant. `δ=0.05` in 7.S11 is an example instance of the rule; the general conversion explicitly takes demand-supplied `δ`. Levels, power thresholds and coverage shares are otherwise parameters. C-prompt

9. **Missing generator.** None in the specification itself; importantly, it already specifies `value v`, which is what the implementation bundle is missing. C-prompt

## `05-laws.md`

1. **Wrong laws.** N/A as executable laws.

2. **Underdetermination.** N/A.

3. **Roles.** N/A.

4. **Models.** N/A.

5. **Against the current decision.** This chapter is stale relative to D-2026-10-14-c. It explicitly says “a law may be valued in `C`”, lets equality return `C`, and later combines cost-valued laws. The review's newer decision says every law is Boolean. C-prompt C-prompt

6. **Implication over a type.** No particular sparse-domain law is written here.

7. **Change first.** Reconcile §2–§3 with D-2026-10-14-c before using this chapter as the source for `laws.lth`; otherwise the implementation is being built simultaneously toward Boolean-only and cost-valued laws.

8. **Cutoffs.** 5.S7 is consistent with the new cutoff rule: the acceptance cutoff belongs to the demand, not to the law. C-prompt

9. **Missing generator.** N/A.

## Specification-level ambiguity

One additional issue is important enough not to bury in a file finding. 7.R1 says both **“a parameter binding wins over a type binding”** and **“a binding in `where` wins over one in the profile.”** These rules conflict for a `where` **type** binding versus a **profile parameter** binding. `resolve` silently chooses the parameter binding first, hence the profile parameter wins, but the specification does not state that tie-break. C-prompt C-prompt This needs one explicit precedence order before implementations can independently agree.

## Not sure

I cannot verify from this bundle whether `Evidence` constructors are intended to become inaccessible except to the certifier; if some unseen abstraction rule seals them, the forged-`Exhaustive` problem becomes harder to exploit, although the laws as written still do not state the invariant. I also cannot verify whether generators for imported `Tolerance` and `RankFloor` already exist outside the bundle. Finally, exact `Float64` equality in `Translates`/`Scales` is likely to reject the intended floating implementations through rounding, but the precise `Float64` operational semantics needed for a concrete counterexample are outside these seven files.