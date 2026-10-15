# Review of layer 3, bundles B, C and D (demand and plan; generators, test and laws; the fit's theories): what the replies say

2026-10-15, by Claude Sonnet 5.5, an agent of the coordinating session, on the brief
`prompt-summary-BCD.md` of this folder. Inputs: the replies under `B/` (deepseek, gpt, grok,
perplexity; `B/fable.md` is empty, 0 bytes, so Claude did not answer B), `C/` (deepseek, fable,
gpt, grok) and `D/` (deepseek, fable, gpt, grok, perplexity), read whole; Perplexity's from its
derived `.md` (the PDF is the original). Kimi is in none of the three bundles. The reviewed files
at the frozen commit 2710cfc (`FROZEN-BCD`). `git diff 2710cfc..HEAD` over every reviewed file
(demand, plan, generators, test, laws, probability, belief, optimization, arrays, their models,
`docs/spec/`, `examples/`) is empty: nothing is fixed at HEAD, every line number below is the same
at the frozen commit and at HEAD. All paths below are under `src/luthier/lib/`.

"Verified" means I read the file at the line quoted and the claim holds as stated. Where I only
repeat a reply's quotation without re-reading, I say "quoted". Whose: the theory's (the `.lth`),
the model's (the `.lut`), the specimen's (the host), the specification's (a chapter or decision),
or a misreading.

## For Luciano: the five things to change first

1. **`IsGradient` accepts a zero gradient for every function** (D: DeepSeek, GPT, Perplexity,
   Fable; Grok sees nothing). `probability.lth` 65: `else if nv == 0.0 then true`; and the test
   direction is `g t` itself (lines 67-69), so any `g` with `dot g (grad f) == |g|^2` passes, zero
   included. `score := zeros`, `info := zeros` is then a model of `Likelihood`; the same hole is in
   `PosteriorScoreIsGradient` (belief 85) and `GradIsGradient` (optimization). Verified. Fix: a
   drawn direction `v`, as `IsJacobian` already does. One law, four consumers.
2. **`LinearizesOn` accepts a schedule that computes a node before what it reads** (B: DeepSeek,
   GPT, Perplexity; Grok misses it). `plan.lth` 79-81: the first conjunct `subset (keep placed
   (readsOf ns n)) placed` is true by construction and the second accepts reads found later in
   `rest`. On the file's own `example`, `["d","b","c","a"]` passes and gives `d = 0`, against 4.
   So `Confluent` (line 101) is false of the intended model. Verified. Perplexity adds that
   `Planning` also quantifies over unrestricted `Dataflow`: no law makes `step` read only what
   `reads` lists, and a one-node self-cycle has no linearization (verified in the same lines).
3. **`Random` cannot be certified: its statistical laws are universal over seeds** (C: Fable,
   DeepSeek, Grok as its first change; D: Perplexity on the same `UniformAtLevel` of
   probability.lth 290). `generators.lth` 72-74: `UniformAtLevel` is `p-value >= alpha` over every
   seed, so a correct source fails on a fraction alpha of seeds and, one failing seed refuting a
   `forall`, a 100-seed sample at alpha 0.05 refutes it with probability about 0.994 (Fable's
   arithmetic). Verified as written. Every generator rests on `Random`. Needs 7.S17's statistical
   form, which `Law` does not have (laws.lth, Fable).
4. **The maximizer and the step have laws that a wrong model passes or a right one fails** (D:
   GPT, Perplexity, Fable on `StepRule`; DeepSeek, GPT, Perplexity on `QuadraticConverges`; all
   five on the maximizer's gap). `optimization.lth` 146-150: acceptance is an implication and
   `s2.phi` is only bounded, never `o.value s2.x`; `phi := pt - 1` and "accept only on even
   `iter`" both pass every `LMStep` law. `belief.lth` 127-131: `QuadraticConverges` is over every
   `Settings`, `maxIter = 1` included, where a correct LM ends `converged = false` (see the
   contradiction below). And `MaximizerStationary` (111) is vacuous when `converged = false`, so a
   maximizer that gives up everywhere passes all but the quadratic law. Fix: `StepRule` as an
   equivalence with `s2.phi == o.value s2.x`; `MaxResult` carrying why it stopped (Fable).
5. **A run's record and the key of a result are two unconnected identities** (B: all four answer
   question 9 the same way). `demand.lth` 107-108: `Record` has no decoration, seed, plan or
   certificate hashes; `plan.lth` 151: `MemoKey` has them, nothing relates the two, and
   `determined` (119) forbids two runs with one record and two results, which a stochastic run
   with another seed legitimately breaks (GPT). Verified. The question for you: is the record the
   key, or does `x.run.json` carry the key's hash?

Runners-up: `Posterior` lets information be negative so `negate` (optimization 65) is not total
(D: GPT, Perplexity, Fable); `ForallOnPoints` settles no multi-parameter sampled law (C: Fable
alone, heavy, laws.lth 187-191); `NotFlips` and `CitedWhole` are unsatisfiable together (C: Fable
alone, laws.lth 208, 213); `Strategy` has no role law (B: GPT, DeepSeek, Grok).

Contradictions between the models, and my reading:
- Does `QuadraticConverges` fail at `maxIter = 1`? DeepSeek, GPT, Perplexity say yes (Perplexity
  and GPT give the 1-d case, one step to 0.5, decrement 0.125). Fable says the native model
  converges in 3-4 steps and the law bites only when c is about 4e17 (floating rounding of
  `d`). Both can hold: the law is false for a drawn small budget, and Fable assumes the demand
  supplies `Settings`. Whether `Settings` is drawn or bound is the open point (Fable's not sure).
  The law is over every `Settings` as written (belief 127), so I side with the three.
- Does `planning` break `PlanIsConfluent`? DeepSeek and GPT: yes, with `["d","b","c","a"]`.
  Perplexity: the example's own schedules pass and do not expose the bug; it breaks only on a
  hidden-dependency dataflow. These agree: the law is false, the listed cases of the model do not
  reach it. Perplexity's opening line ("rejects the supplied example's topological schedules") is
  contradicted by its own check below it.
- Is anything wrong in `plan.lth`? Grok: only that `Strategy` has no role and the laws have rare
  premises; it misses item 2. Grok on D (all of it conforms) misses item 1 too. Grok's replies are
  the weakest of the round; I weigh them last.
- `Reason` (optimization 109) needs role laws: DeepSeek, GPT, Perplexity yes; Grok none needed;
  Fable: it is an alias, L2.7 is formally met, the roles still exist. Fable's reading is the
  accurate one; `isConverged` (110) is the observer L2.7 excludes.
- Is `Bounded` exhaustive? DeepSeek: `ForallOnPoints` should give `Confirmed` (7.S10). GPT: the two
  files disagree. Fable: `test.lth` 125 gives `Confirmed` with `Bounded` the exhaustive grade,
  which `ForallOnPoints` can never produce. Not settled; a question for the specification (7.S10).
- `tailSeriesTerms`/`tailSeriesFrom` (probability 272-273) as cutoffs: DeepSeek, GPT, Perplexity
  say they break D-2026-10-14-c; Grok and Fable say they are precision of a definition. Fable's
  check (the 100th term is exp(-800)) supports the file's reading. A criterion of yours.

## B: demand and plan

### demand.lth

B1. **The record drops the type demanded** (DeepSeek, GPT, Perplexity; the three also on seed, plan
and certificates). `Record` (107-108) has no `decoration`; `RecordsEveryCutoff` (150-152) equates
`recorded` to exactly those fields. Two demands that differ in decoration have one record.
Verified. Whose: the theory's, with the key (item 5).

B2. **`determined` is too strong for the record it reads** (GPT; Perplexity that it only checks
consistency inside a list). Lines 119-121. Verified: with seed, plan and certificates absent from
`Record`, two legitimate results share a record. Whose: the theory's; goes away if B1 is closed.

B3. **`NoPriceRefusesAssumed` has no price** (GPT; DeepSeek on its rare premise; Perplexity on
vacuity). Lines 141-142: `admitsAssumptions d` reads only `accepts` (91), and `Demand` (71-72)
has no assumption price, though 8.S1 and 6.S10 say it has no default. Verified. The premise
`e.grade == just AssumedGrade` over arbitrary `Entry` is rare (quoted); the subtype is assumed
entries. Whose: the theory's, under D-2026-10-14-c (the price waits for the cost types).

B4. **`delta` fixed to `nothing`, `decoration` fixed to `nothing`** (DeepSeek, GPT, Perplexity).
`demand_model.lut` 23: neither is an argument of `theDemand`, unlike `entry`, `accepts`, `fuel`.
`demand.lth` 67-68 says delta is `nothing` in this draft on purpose [proposed]. Verified. Whose:
the model's; the file already states the reason, so a decision, not an error.

B5. **`delta` is not passed down** (Perplexity). `LawDemand` (85) has no delta. Verified. A law
that needs the sampling level cannot get it through the passing-down. Whose: the theory's.

B6. **Defaults as cutoffs** (DeepSeek, as not sure; GPT, Grok, Perplexity say no). `Sampled` and
10000000 are declared default arguments (L5.18, L5.19). No finding.

### plan.lth

B7. **`LinearizesOn` / `placedBefore`** (DeepSeek, GPT, Perplexity). Item 2 of the top screen.
DeepSeek's fix (`subset (readsOf ns n) placed`) would reject a read outside the live set, which
the comment at line 76-77 allows as a leaf; keep the reads inside `s` only. Whose: the theory's.

B8. **`Planning` quantifies over any `Dataflow`** (GPT, Perplexity; DeepSeek as the missing
locality law). No law says `step n` reads only `readsOf n`; no law excludes cycles (a self-cycle
has no linearization). Perplexity's counterexample: `a` reads `c` though it declares no reads, so
`byNeed` and `forward` disagree and `StrategiesAgree` fails. Verified in the lines 84-85, 190-205.
Whose: the theory's (a domain, or a locality law). GPT also asks 8.S5 to state completeness of
`reads`.

B9. **`Strategy` has no role law** (GPT, DeepSeek, Grok). Lines 112-114. `StrategiesAgree` and
`TheDefaultsAgree` say the strategies agree, not what makes one forward and the other by need: a
planner returning one schedule for both passes. Verified. Whose: the theory's (L2.7).

B10. **Default strategy `CallByNeed`** (DeepSeek, GPT, Grok) against 8.S3's forward on demand.
`planOf` line 129. Verified, and the file marks it `[proposed]` and says why (run.py's today).
Whose: the specification's decision against the specimen; the file is honest about it.

B11. **`Confluent` is an implication over arbitrary schedules** (DeepSeek, GPT, Perplexity, Grok).
Line 102. Random `String` lists almost never linearize. Verified. Quantify over linearizations
of the live cone. Whose: the theory's.

B12. **The `KeySees*` laws are one-coordinate** (GPT, Perplexity; Grok says they are exactly the
identity needed). Lines 171-176: a hash that is XOR-like passes all six and collides when two
fields change together; Grok's "or short-circuits" reading is wrong (the law fails when the hash
does not change). `planHash` sees the schedule only (179; GPT, Perplexity). Verified. Whose: the
theory's; the same host hash question as certification's `hashing`.

B13. **`KeyReadsTheType` is a tautology** (DeepSeek). Line 211-212 with `demandKey` (140):
`(demandKey dm live).decoration == dm.decoration` is the definition. Verified. DeepSeek's other
point (the key omits tolerance and `accepts`) is also in GPT and Perplexity: `DemandKey` (137) has
only decoration and live values. Whose: the theory's; waits on B3's price.

B14. **No law ties the key's parts to the run** (GPT, Perplexity, DeepSeek). `MemoKey` (151) fields
(plan is the hash of the chosen plan; certificates are the live cone's) have no provenance law.
The question-9 answer: a law `recorded`/`memoKeyOf` relating Record and MemoKey, and a store law
equal key gives equal result (GPT, Perplexity, DeepSeek). Whose: the theory's.

B15. **`Strategy`'s model and `KeyReadsOnlyTheCone`** (Grok): the model "demonstrates" only the
example; no `Keying` model exists (Grok, GPT, DeepSeek; the file says 8.S10). Not a defect.

### plan_model.lut

B16. **`planning` is not a model of `Planning`** (DeepSeek, GPT; Perplexity with a different
case). See the contradictions. Also `byNeed` on a cycle returns `["a","b","a"]` (GPT, Perplexity
for the self-cycle), a duplicate. Whose: the model's, because of B7 and B8.

### 08-demand.md

B17. **The chapter is stale against D-2026-10-14-c** (GPT, Grok): 8.S1/8.S2 still carry cost-valued
cutoffs and an assumption cost; 8.S4/8.S11 say the key is unwritten while `plan.lth` has it. Not
re-read here. Whose: the specification's.

B18. **"Call by need computes the same live subgraph"** (Perplexity): equal demanded output is not
equal evaluated nodes. Quoted. Whose: the specification's.

## C: generators, test and laws

### generators.lth

G1. **`Random` conjoins statistical laws universal over seeds** (Fable, DeepSeek, Grok; Perplexity
on the sibling in D). Item 3. Fable adds that `l : Level` is a quantified parameter and so drawn
unless bound. Whose: the theory's, and the specification's 7.S17.

G2. **`Translates` and `Scales` use exact `==` on `Float64`** (Fable alone). Lines 126, 135 (quoted
for the body). Fable's numbers: 22% and 40% of random cases fail for the two reference metrics.
Against 5.S4 and D-2026-10-14-c; GPT's not-sure says the same likely. Not re-run. Whose: the
theory's (a tolerance from the demand).

G3. **`Metric` laws do not separate linear from log** (Fable, GPT). `place lo hi v := lo` passes
all of them; `linear` satisfies `Scales` in the reals. Missing: `place 0 1 v == v`, and for log the
conjugacy with `log`. Quoted. Whose: the theory's.

G4. **`ProportionalToWeight` is false for duplicate keys** (Fable, GPT, DeepSeek). Lines 104-106:
`weightOf` sums all occurrences, `before` stops at the first. Counterexample `[(x,1),(y,1),(x,1)]`.
Verified by reading; `supportOf` (generators_model.lut 20) takes any list, so it is a model that
breaks its theory. Whose: the theory's (distinct keys) or the model's. Two replies call it the
first change (Fable's CM4-like, GPT's item 7).

G5. **`Filter` does not constrain the seed** (Fable, GPT): `draw tries n s := (..., s)` passes.
Quoted. Whose: the theory's.

G6. **`Resolution` leaves open a `where` type binding against a profile parameter** (Fable, DeepSeek,
GPT as a specification item). 7.R1 says both a parameter binding wins over a type and a `where`
over the profile; the combination is unstated. Three models, so I would raise it (specification).

G7. **`dependent` has no redraw budget; `walk` gives `Gen (Maybe T)` and cycles** (Fable, GPT,
DeepSeek). Lines 191, 205. Against 7.S7 and 7.R4. Verified in the signatures. Whose: the
theory's, or the section is `todo` (§8).

G8. **`CensusFirst`, `CleanCensusFirst`, `Scales`, `ProportionalToWeight` quantify over a rare
premise** (Fable; GPT on `Scales`; DeepSeek on `CensusFirst`). A seed below the census length is
a 1e-9 fraction. Whose: the theory's.

G9. **`Budgets` admits masses above 1** (Fable alone). Quoted. Whose: the theory's.

G10. **`LogScales` uses an undefined `m`** (DeepSeek alone). Not checked; if true it is a typing
slip. Not sure.

G11. **Missing generators** (question 9). `Gen Interval`, `Gen PositiveInterval`,
`Gen OrderedUnitPair`, `Gen String`, `Gen` of weighted supports (Fable); `value v` so that `Level`,
`Tolerance`, `RankFloor` are bound to the demand's value, not drawn (GPT); a census of `Random`,
`Tester`, `Settling` models (DeepSeek, which names the theory and not the type quantified, a
weaker answer); a census of `Mode` and `Gen TestSpec`, `Gen Law`, `Gen Evidence` (GPT, Fable).
`Gen String` and `Gen TestSpec` have two models each; `value v` is in the specification (7.R1)
and not in the file.

### generators_model.lut

GM1. **Masses fixed in the value** (Fable, DeepSeek, Grok; GPT says no cutoff). Lines 75, 80:
`0.2`, `0.25`, `1.0`, `1000.0`. 7.S8 says they are budgets recorded in the entry; the file says
P11. Verified. Whose: the model's. Fable's first change.

GM2. **Families claim more than they state** (Fable, GPT: `orthogonal` Haar, the atoms, `gram`
rank deficient in most draws). The identity matrix passes `OrthogonalGivesOrthogonal`. Quoted.
Whose: the theory's (7.S1: a family that claims a distribution states it as a law).

GM3. **`UniformSampleIsUniform` is Boolean** (Fable, DeepSeek): as G1.

### test.lth and test_model.lut

T1. **`specCoverage` is not the weakest reach of each parameter** (Fable, GPT; DeepSeek on the
seed). Lines 80-81: it folds every binding, even ones `resolve` overrides, and the mode even when
every parameter is bound. Fable's case: exhaustive mode, `x` from census (`Listed`) against profile
`Drawn 0`: the correct tester is refuted by `CoverageIsTheWeakest` (94-97). Verified by reading.
Whose: the theory's. Fable's first change.

T2. **The always-`NotRun` tester passes every law** (GPT; Fable on `CoverageIsTheWeakest` sampled
branch). Quoted. Whose: the theory's.

T3. **`RunIsPointsOrNotRun` refutes a correct tester on a non-`forall` law** (Fable alone). Line 89
(body quoted). Not re-run. Whose: the theory's.

T4. **`grade` gives `Confirmed` with `Bounded n` the exhaustive grade** (Fable; GPT, DeepSeek on
the layer disagreement). `test.lth` 125 and `laws.lth` 190: `ForallOnPoints` returns `Confirmed`
only under `Exhaustive`. Verified that the two lines disagree. Whose: the specification's 7.S10,
then the files.

T5. **`gradeRank` is not "by evidence cost"** (GPT, Fable). Line 121: a fixed order, where L10.2
orders without a domain. Whose: the specification's.

T6. **`Grading` restates `grade` case by case** (Fable, against D-2026-10-13-aa Q5). Quoted. Whose:
the theory's.

T7. **`mode` has no default** (GPT, Fable), against 7.S20. Whose: the theory's.

T8. **`defaultBudgets` are constants** (DeepSeek, Grok say yes; Fable, GPT say they are defaults
7.S8 asks for). Line 51. Fable and GPT are right on the text of 7.S8; DeepSeek's and Grok's
reading is a misreading unless a default counts as a constant, which is a criterion of yours.

T9. **`Mode` and `Grade` constructors have no role laws** (DeepSeek, Grok, Fable on `SampledMode`,
GPT on `SampledMode`'s `Metric`). `modeCoverage` drops the metric. Verified in outline. Whose: the
theory's (L2.7).

### laws.lth

L1. **`NotFlips` and `CitedWhole`/`AssumedWhole` are unsatisfiable together** (Fable alone).
Lines 208, 213-214: at `p := Not q`, `Cited r` gives `Cites r` by one and `flip (Cites r)` by
the other. Verified given the comment at 207 (what is only supported stays unsettled). `Settling`
then has no model. Whose: the theory's; Fable's one-line fix.

L2. **`ForallOnPoints` settles no multi-parameter sampled law** (Fable alone). Lines 187-191: the
inner points are `Supported`, `allConfirmed` fails, the outer is `Unsettled`. Heavy, because it
reaches nearly every law. Verified by reading the code; whether the tester nests or flattens
`Points` is Fable's not sure. Whose: the theory's.

L3. **`Exhaustive` is a forgeable tag** (GPT): `Points Bool nil Exhaustive` confirms a false
`forall`. Verified: `allConfirmed nil` is true. Whose: the theory's.

L4. **`combine` is underdetermined** (GPT, Fable, Grok). Line 222: two citations may give
`Confirmed`, or everything `Unsettled`, and pass. Whose: the theory's.

L5. **`Settling` laws quantify `(A : U)` inside the law** (Fable): static error by 7.R2. Whose: the
specification's (Fable asks it to state the rule, with D-2026-10-13-l).

L6. **`isSymmetric`, `isTransitive` are implications over arbitrary pairs** (Fable, GPT, Grok,
DeepSeek). Line 60. The file says so itself. Whose: the theory's.

L7. **`Coverage` payloads have no role** (GPT, Fable). `Bounded n`, `Drawn s`. Verified in outline.
Whose: the theory's (L2.7).

L8. **The file and 05-laws.md are older than D-2026-10-14-c** (GPT; Grok says they match). Quoted.
Whose: the specification's.

### 07-tests.md

S7-1. **7.S12 contradicts itself on a law whose premises never held** (GPT alone): `NotRun` and
"passed vacuously". Quoted. Whose: the specification's. S7-2. **7.S11's 3/n exceeds 1 for n = 1, 2**
(GPT alone). Quoted. Whose: the specification's.

## D: the fit's theories

### probability.lth

P1. **`IsGradient`** (DeepSeek, GPT, Perplexity, Fable). Item 1.

P2. **`Likelihood.info` is bound only by symmetry and non-negativity** (GPT, Perplexity, Fable;
Grok on `InfoNonNegative`). Line 126-129: `info := zeros` is a model; `laplaceAt` and `nu` in
experiment_zero read it, so a zero information returns the prior. Verified. Whose: the theory's
(the Bartlett identity waits on the sampler, per the header).

P3. **`InfoNonNegative` is a sampled quadratic form** (Fable, Grok): low power on a nearly
indefinite matrix; arrays.lth §4 says quadratic forms do not decide semidefiniteness. Fable adds a
flat tolerance (11.S14). Verified at line 126-128 in outline. Whose: the theory's.

P4. **`profiled` at zero residual or k = 0** (GPT, Perplexity). `ustar = -inf`, score NaN, against
finite `Float64`. Fable: unreachable on drawn data, reachable if a fit reproduces every datum.
Quoted. Whose: the theory's (a subtype); Fable's reading limits the weight.

P5. **`KolmogorovAgrees` as a law against 4.R10** (DeepSeek, Perplexity; Grok, GPT, Fable find it
fine). Line 263-264. 4.R10 not re-read. Not sure. Whose: the specification's reading.

P6. **`tailSeries*` as cutoffs** (DeepSeek, GPT, Perplexity yes; Grok, Fable no). See the
contradictions. Lines 272-273.

P7. **`UniformAtLevel` is the G1 law** (Perplexity), with the empty-sample case (`p = 1`). Line 290.
Whose: as G1.

P8. **Laws outside a `T :=` conjunction are not pulled by a demand** (Fable alone):
`GaussianPeaksAtMean`, `ProfiledIsGaussianAtItsSigma`, `UniformAtLevel`. Whose: the specification's
(L10.6) or the file's; whether `test` runs every Bool definition is Fable's not sure.

### belief.lth

BE1. **`QuadraticConverges`** (DeepSeek, GPT, Perplexity; Fable on the floating bound). Item 4 and
the contradictions. Lines 127-131.

BE2. **`MaximizerStationary` vacuous on `converged = false`** (DeepSeek, GPT, Perplexity, Fable).
Line 111. The give-up model passes. Fable's fix: `MaxResult` carries `Reason`. Whose: the theory's.

BE3. **`Posterior` allows negative info; `negate` not total** (GPT, Perplexity, Fable). Lines 85-87
and optimization 65. A model `logp = 0, score = 0, info = -I` is a `Posterior` and not an
`Objective`. Verified. Whose: the theory's.

BE4. **Laplace functions take `y : Vec Float64`, laws are over `VecOf l.k`** (GPT, Perplexity).
Quoted. Whose: the theory's.

BE5. **`laplaceUpdate` drops `converged`** (Perplexity); **the precision is information, not the
Hessian** (Perplexity: Fisher against the negative Hessian for a nonlinear mean). Quoted. Whose:
the theory's; the second a design question for you (Laplace by information or by curvature).

BE6. **The damping schedule is "the host's own"** (GPT, Perplexity), against P11. `belief_model.lut`
comment, `experiment_zero` supplies none. Quoted. Whose: the model's.

BE7. **Question 9, the maximizer beyond the quadratic family.** DeepSeek: a nonlinear mean or
logistic posterior with a known maximum. GPT: `logp = -(c/2)|r|^2 - (d/4)|r|^4`, known maximum
`b`, check convergence and `logp(b) - logp(x)` within the demand's tolerance. Perplexity: the same
quartic family with analytic score and information, plus eligible settings from the demand. Grok:
`-1/2|x-b|^2 + eps sin(omega . x)`, weaker (concavity needs eps small). Fable: separable
`-sum c_i log cosh (x_i - b_i)`, whose Newton step overshoots so the damping path is exercised, a
point-based check (not the self-reported decrement), plus an independent law: at a reported
converged stop, the central difference of `p.logp` along a drawn `v` is near zero, and the budget
law of BE2. Common to four: a known-maximum family, checked at the returned point, parameters
from bounded generators. Fable's two additions (the family must reject steps; check from `logp`,
not from `info`) are the ones the others lack.

### optimization.lth

O1. **`StepRule`** (GPT, Perplexity, Fable). Item 4. Lines 146-150. The model file's claim that the
laws determine the step (4.R10) is therefore false (Perplexity, Fable).

O2. **`StepRule` over arbitrary states** (Perplexity, Fable): `phi` unrelated to `x`. Whose: the
theory's (the subtype of states a run visits).

O3. **`Reason` and `isConverged`** (DeepSeek, GPT, Perplexity, Fable). See the contradictions.
Lines 109-110. `Run` has no law tying `reason` to `finished` (Fable).

O4. **`QuadraticStepAccepts` is false in floating point** (Perplexity: `init = most = 1e20`; Fable:
beyond `init` about 1/eps). Both agree the demand's `Damping` bounds it. Quoted. Whose: the
theory's (an eligibility subtype).

O5. **`DirectionAgrees` hard-wires the native expression** (Grok alone): the host must reproduce
the native floating-point order. That is what 4.R10 and the specimen rule want. Not a finding.

### optimization_model.lut

OM1. **`lmMaximizer` against `QuadraticConverges`** (Perplexity, GPT; DeepSeek as conditional).
See the contradictions. Whose: the law's, not the model's (Perplexity: legitimate exhaustion).

OM2. **`native : LMStep` fails `QuadraticStepAccepts` at large damping** (Perplexity); passes (Fable,
DeepSeek, Grok). Same as O4.

### arrays.lth

A1. **`RankUnderRotation` asks exact integer rank from approximate orthogonality** (Perplexity
alone). Line 245. Counterexample at `tol = 1` with a threshold 0.5 against 0.405. Quoted. Whose:
the theory's. A2. **`RankScales` underflows; `TraceAdditive` cancels** (Perplexity alone). Quoted.
A3. **`RankOfDiagonal`/`ClearFloor` are fixed eligibility constants** (DeepSeek, Perplexity as a
cutoff: `f < 0.001`, `1.0 <= |d| <= 1000.0`, lines 235-236; Grok, Fable no). Verified as written.
They are domains of a generator, not acceptance cutoffs; a criterion of yours (P11, D-2026-10-14-c).
A4. **`pinvSym` on an indefinite matrix** (DeepSeek alone): a wrong model returning zero passes.
Quoted. A5. **Models and generators exercise diagonals only** (Perplexity, Grok): add a
non-diagonal PSD family. Whose: the theory's.

### experiment_zero.lut (use only)

E1. **`covFloor` is a rank floor computed in the program; `bandLevel` a level** (GPT, Perplexity,
Fable). `lmFloor` comes by `--set`; these two do not. D-2026-10-14-c names both kinds. Quoted.
Whose: the program's.

## Not sure

- Whether `Settings` and `Damping` in the laws are bound by the demand or drawn (Fable; decides
  the weight of BE1 and O4).
- Whether Bool definitions outside a `T :=` conjunction are tested (Fable, P8).
- Whether the tester nests `Points` for several parameters (Fable; decides L2).
- The host code: `luthier.arrays.kolmogorov_distance` (exact agreement, empty list), `luthier.lm.*`
  (unwritten) (DeepSeek, GPT, Perplexity, Fable, Grok).
- Whether `Hash` is finite-width, so the `KeySees*` laws are impossible for large domains
  (Perplexity, B).
- Whether duplicate or reordered `--set` arguments are canonicalized before `DemandKey` (GPT, B).
- `LogScales` using an undefined `m` (DeepSeek, G10); `CostScale` using `VerdictsAreExact` before
  its definition (DeepSeek, Fable): whether forward references parse.
- Whether `Seed` passes where `Nat` is asked (Fable), and `Dim` where `Nat` is (Fable).
- 4.R10 itself: whether native agreement is a corollary or a law (P5, O1).
- I did not re-read `docs/spec/` chapters; every "against the specification" is the reply's quote.
- I did not re-run the floating-point cases of G2 and P3 (Fable's numbers).
