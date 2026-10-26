# Report: B1, B3, D1 and the tester's assumed grade

2026-10-26, Claude Opus 5.5, on `prompt-b1-b3-d1.md` beside this file (d7223e1), bites B1, B3 and D1
of `execution.md` and item 4 of the brief, after D-2026-10-25-a. Base d7223e1; another session
committed three unrelated files meanwhile (a55ae64, 5793494, 382cfc9). Logs and scratch under
`~/.cache/luthier-b1b3d1/`. What is mine is marked [proposed] in the files and listed at the end.

## 0. plan_model.lut's three 4.R5 errors (5d060de)

The externs `keyDigest`, `planDigest`, `recordDigest` had their types; 4.R5 counted only the file's
own definitions as defined, and their types mention `Hash` (certification.lth's alias) and `Seed`
(generators.lth's subtype), both imported. check.py now counts a definition or an alias an import
brings as defined (an imported declaration still is not), as 4.R5 reads ("accepted when T is
defined"). `luthier check plan_model.lut` is clean; a test in tests/test_check.py.

## 1. B1, ε̂ at serve time (714184f, 3c261d4)

- certification.lth: `SampledBound` (a bound on the failure fraction, with the logarithm it is
  read with) and its law `SoundAtNoFailure`, (1 − ε̂)^n ≤ δ in logarithms; a bound of 1 is always
  sound. certification_model.lut: `ruleOfThree`, min(1, −log δ / n) (7.S11's rule of three at
  δ = 0.05; 1 for n = 0 or δ = 0), claimed as `RuleOfThreeIsSound`; its control, one over n, is
  refuted at n = 2, δ = 0.01 (tests/tester/evidence_laws.test.lut).
- certify.py: `epsilon_hat` (the specimen), `entry_evidence` (a sample's pair from the n of the
  union of its stretches, `pooled`; (0, 0) for a pass exact on its domain; none for a statistical
  or an assumed pass), `region_evidence` (per region, from its own cases), `obligation_evidence`,
  and the compositions of core.lut by name (`cappedSumComposition`, the default, and
  `productComposition`). Nothing is stored: ε̂ is computed when an entry is read.
- The demand: `delta : ProbabilityLevel`, default 0.05, and `composition : String`, default
  `cappedSumComposition` (demand.lth, demand_model.lut, plan.lth's `withSet`, run.py's `Demand`,
  `run --delta`, `run --composition`), both recorded and in `RecordKeepsThePolicies`. The product
  is refused unless the demand accepts `FailuresIndependent` by name.
- `certify` and `check -v` print, for a sampled law, ε̂ at δ per obligation and the pair the
  conjuncts compose to. The tape example (acceptance):
  `Tape: sampled, ε̂ 0.015 at δ 0.05 in each of 4 conjuncts (200 cases), (0.06, 0.2) composed by the capped sum`.
- The run's record carries `certification.evidence`: the cone's pair at the demand's δ by its
  composition, with each witness's pair, cases and per-region ε̂ (run.py's `_cone_evidence`).
- Tests in tests/test_certify.py (soundness of the formula, pooled n, the tape line, the demand's
  fields, the run's record).

## 2. B3, the grade as a projection of (domain, cost) (f6a5be7, 26043b0)

- certification.lth: `Domain` (listed, box, whole type, under a citation's hypotheses,
  distribution, asserted), `EvidenceCost` (exact, statistical, priced), `Strength`, `strengthOf`,
  `gradeOfStrength`, `derivedGrade`; `admits` holds of the derived grade only. L10.2's table is the
  law `ProjectsTheFiveGrades` of `StrengthProjection`, claimed for `projection` and controlled by
  `sampleAsCases` (a sample read as listed cases, the audit's 1.2), refuted. The comment says the
  chain stays the Boolean slice's admission until the cost types (L10.5) and B4 then restricts
  `Cases`.
- certify.py: `strength`, `grade_of_strength`, `derived_grade`; `admits` from them (a drawn
  coverage no longer admits `Cases`, an exhaustive one no longer `Cases`).
- Reader check (`test_every_stored_grade_is_the_derived_one`): over every store of the tree
  outside record/, each stored grade equals the derived one (more than 1000 passes) and every store
  keeps its predicate. Before the change the stores held only the pairs the derivation gives
  (Drawn sampled 978, Listed cases 392, Exhaustive exhaustive 3, Tested sampled 3).
- The run's record: `certification.grades`, the vector of the cone's laws with the grade each is
  served at, and `certification.grade`, their combination by the demand's `combine`.
- Nothing served differently: serving still reads the chain; the re-certification's grades are
  unchanged (the only change in `certify`'s lines is B1's ε̂ and D1's conjuncts).

## 3. D1, a control per conjunct (71941e4)

- tester.py: a control line on a conjunction runs every conjunct on the broken model, each with
  its own control entry (`conjunct` in its identity), and keeps the line's entry (first
  refutation, as before) so that a line refuting no conjunct still fails loudly. A conjunct that
  holds on the broken model says "held: this conjunct does not see the break", no control failure.
  `conjunct_heads`/`line_conjuncts` give each conjunct the law it applies and that law's cone.
- certify.py: `conjunct_control` (controlled by its own refutation, by a refuted control of the law
  it applies at that law's cone, or by a pre-D1 line entry naming it; an axiom conjunct has no
  control; otherwise uncontrolled with why), the detection rate as refuted seeds over seeds run
  (said when below one), `control_status` and `control_standing` read the line's entry only.
  `certify` and `check -v` add "k of m conjuncts controlled; uncontrolled (L9.14): …". Admission
  unchanged.
- The tape example: `Tape` 3 of 4 (`hooked` now refutes `ReadingSteps` too, and `MetresWithin t`
  is controlled by `noRoom`), uncontrolled `ReadingSymmetric t`; `MarkIsAMetric` 1 of 5 in the tape
  file's own `certify` (2 of 5 read over every store: core's control of `Commutative` is at the same
  cone), uncontrolled `MetricIndiscernible` (its control vacuous), `Triangular`, `MetricNonNegative`
  (and `Commutative` per file). So five per file, four over the tree, against docs/concepts.md
  §7.1's six: §7.1 counted from the old entries, before `hooked` ran `ReadingSteps`.
- Tests: per-conjunct status, the rate, a control running past its first refutation, the tape
  example's list.

## 4. The tester's assumed grade (1158d43)

tester.py's `axiom_of` reads a law whose body is an axiom through the definitions it applies;
such a line (or conjunct) runs no case and is graded `AssumedGrade` with evidence
`{"Assumed": statement}` (`AssumedAxiom`); a control reports it not run. test.lth's
`RunIsPointsOrNotRun` now allows an assumption (a spec cannot say its law is an axiom). core.lut
claims `ProductIsIndependent` (`IndependentComposition productComposition`), in `CoreBases`, and
bases_laws.test.lut certifies it: assumed, its eleven algebraic conjuncts at cases and
`FailuresIndependent` assumed. Test in tests/test_tester_conjunction.py.

## Checks

- Re-certification of the 52 test programs (tests/tester/*.test.lut and docs/concepts/tape.test.lut)
  six at a time, `--jobs 1`, logs in ~/.cache/luthier-b1b3d1/pass1 and pass2: pass 1 ran 162 lines;
  pass 2 ran 0 lines in every program. Stores committed in c9635ef. Non-zero exits in both passes:
  cases, laws and vacuity (fixtures refuted or vacuous by design) and belief_laws
  (`PrecisionSymmetric`: maximum recursion depth, as in C1's report, not touched here).
  evidence_laws re-certified twice again after the rename in daf0855 (second 0 lines).
- Suite file by file under `timeout 1800` (logs in ~/.cache/luthier-b1b3d1/suite): all pass after
  daf0855 but test_check_private.py, which collects no test (exit 5, as before). test_core_structures
  and test_run failed on the first round (the new claim, the demand's two fields) and pass after.
- `scripts/check_spec.py`: its one known finding.
- `scripts/core_metrics.py` against d7223e1 (git archive in the scratchpad): homonyms 1 = 1,
  executive shadows 118 = 118, list helpers 34 = 34, unclaimed 9 = 9, loose 1471 → 1480 (real
  1389 → 1398): the new theory names and claims (`SampledBound`, `StrengthProjection`, `strengthOf`,
  `gradeOfStrength`, `derivedGrade`, `coverageDomain`, `RuleOfThreeIsSound`, `GradeIsAProjection`,
  `ProductIsIndependent`), counted as B2's and C1's were.

## Uncontrolled conjuncts (D1), read over every store of the tree

162 conjuncts of 56 laws have no refuted model. Why: held on every broken model (119); the
control's census is outside the conjunct's domain, so the control did not run it (25: e.g. the
`Object` laws' controls bind `p` to related pairs, and `Symmetric`, `Transitive` need others);
vacuous (6); no control line at all (10: `ProductIsIndependent`'s, which has none, and
`EmptyIsInitial`'s `NoValue`); stuck matches (2). Per law, the conjuncts by the law each applies:

- arrays_laws.test.lut, VecIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- arrays_laws.test.lut, VecIsAFunctor: MapCompose (held)
- arrays_laws.test.lut, VecIsTabulated: AtBuild (held)
- arrays_laws.test.lut, MatIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- arrays_laws.test.lut, MatIsAFunctor: MapCompose (held)
- arrays_laws.test.lut, SymmetricIsAnEqualizer: Equalizes (held)
- bases_laws.test.lut, ExtendedIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- bases_laws.test.lut, ErrorIsABase: Associative x2 (held), Neutral (held), Distributive (held), Absorbing (held), Distinct (held), Idempotent (held)
- bases_laws.test.lut, CappedSumIsAssumptionFree: Associative x2 (held), Neutral x2 (held), Distributive (held), Absorbing (held), Distinct (held), Idempotent (held), Integral (held)
- bases_laws.test.lut, ProductIsAComposition: Associative x2 (held), Neutral (held), Distributive (held), Distinct (held), Idempotent (held), Integral (held)
- bases_laws.test.lut, ProductIsIndependent: Associative x2 (no control line), Neutral x2 (no control line), Distributive (no control line), Absorbing (no control line), Distinct (no control line), Idempotent (no control line), Integral (no control line)
- bases_laws.test.lut, NatsIsAConversion: NatsOfNothing (held)
- core_laws.test.lut, IntEquivalence: Reflexive (held), Transitive (held)
- core_laws.test.lut, IntPreorder: Transitive (held)
- core_laws.test.lut, IntPartialOrder: Reflexive (held), Transitive (held)
- core_laws.test.lut, IntTotalOrder: Reflexive (held), Transitive (held), Antisymmetric (held)
- core_laws.test.lut, IntStrictOrder: Transitive (held)
- core_laws.test.lut, IntBijective: Injective (held)
- core_laws.test.lut, EmptyIsInitial: NoValue (no control line)
- core_laws.test.lut, BoolIsTheBooleans: Associative x2 (held), Idempotent x2 (held), Absorptive (held), Distributive x2 (held), Distinct (held)
- core_laws.test.lut, BoolIsACoproduct: CaseRight (held)
- core_laws.test.lut, MaybeIsACoproduct: CaseLeft (held)
- core_laws.test.lut, ListIsTheFreeMonoid: Associative (held), FoldNeutral (held), FoldInject (held), NilIsNeutral (held)
- core_laws.test.lut, IntIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- core_laws.test.lut, NatIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- core_laws.test.lut, BoolIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- core_laws.test.lut, StringIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- core_laws.test.lut, FloatIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- core_laws.test.lut, IntIsASemiring: Associative (held), Neutral (held), Distributive (held), Absorbing (held), Distinct (held)
- core_laws.test.lut, IntIsACommutativeRing: Associative x2 (held), Neutral x2 (held), Distributive (held), Absorbing (held), Distinct (held)
- core_laws.test.lut, IntIsOrdered: Transitive (not run (the control's census is outside the conjunct's domain)), Antisymmetric (not run (vacuous))
- core_laws.test.lut, NatIsOrdered: Transitive (not run (the control's census is outside the conjunct's domain)), Antisymmetric (not run (vacuous))
- core_laws.test.lut, BoolIsOrdered: Transitive (not run (the control's census is outside the conjunct's domain)), Antisymmetric (not run (vacuous))
- core_laws.test.lut, StringIsOrdered: Transitive (not run (the control's census is outside the conjunct's domain)), Antisymmetric (not run (vacuous))
- core_laws.test.lut, FloatIsOrdered: Transitive (not run (the control's census is outside the conjunct's domain)), Antisymmetric (not run (vacuous))
- core_laws.test.lut, NatIsAnOrderedSemiring: Associative x2 (held), Neutral (held), Distributive (held), Absorbing (held), Distinct (held), Reflexive (held), Transitive (held), Antisymmetric (held), Total (held), MonotoneIn (held), Least (held), Discrete (held), PositiveClosed (held)
- core_laws.test.lut, StringIsAMonoid: Associative (held)
- core_laws.test.lut, BoolIsABooleanAlgebra: Associative x2 (held), Idempotent x2 (held), Absorptive (held), Neutral x2 (held), Distributive x2 (held), Distinct (held)
- core_laws.test.lut, IntIsAMetric: MetricZeroOnEqual (held), MetricIndiscernible (held), MetricNonNegative (held)
- core_laws.test.lut, BoolIsAMetric: MetricZeroOnEqual (held), Triangular (held), MetricNonNegative (held)
- core_laws.test.lut, RecordsAreNamedProducts: PairFst (held), PairSnd (held), Pairing (held)
- core_laws.test.lut, SumsAreNamedCoproducts: CaseLeft (held), CaseRight (held), CasesAreAll (not run (stuck))
- core_laws.test.lut, ListIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- core_laws.test.lut, FinIsACoequalizer: ProjectsRelated (held)
- core_laws.test.lut, KernelFiniteQuantifiers: QuantifiersPairs (held)
- lists_laws.test.lut, ListIsTabulated: AtBuild (not run (stuck))
- lists_laws.test.lut, HammingListIsAMetric: MetricZeroOnEqual (held), Triangular (held), MetricNonNegative (held)
- numbers_laws.test.lut, AbsDistanceIsAMetricWithin: WithinZeroOnEqual (held), WithinSymmetric (held)
- settling_laws.test.lut, Settling: Associative (held)
- settling_laws.test.lut, Measuring: ZeroDistanceIsExact (held), WorseRatioCommutes (held), WorseRatioAssociates (held)
- sonolocalizacion_laws.test.lut, JoinOnFirstEnd: PullbackUnique (held)
- sonolocalizacion_laws.test.lut, JoinOnSecondEnd: PullbackUnique (held)
- tables_laws.test.lut, TableIsAnObject: Symmetric (not run (the control's census is outside the conjunct's domain)), Transitive (not run (the control's census is outside the conjunct's domain))
- transformer_laws.test.lut, OnDoubles: ComposeAssociative (held), UnknownComposesUnknown (held), UnknownGivesNoPullback (held)
- tape.test.lut, Tape: ReadingSymmetric (held)
- tape.test.lut, MarkIsAMetric: MetricIndiscernible (not run (vacuous)), Triangular (held), MetricNonNegative (held)

The full list with each conjunct's text and reason is ~/.cache/luthier-b1b3d1/uncontrolled.tsv,
from the scratchpad script `uncontrolled.py` over `programs.txt` at c9635ef.

## For the coordinator

- docs/concepts.md §6.3's `certify` output and §7.1's "six" are stale (B1's ε̂, D1's five per file);
  the doc is a draft under his marks, so not touched here.
- `certify` reads controls from the stores of the files it is given; a conjunct whose own law's
  control lives in another store reads uncontrolled there and controlled over the tree
  (`Commutative` of `MarkIsAMetric`). Left as is.
- execution.md's status line for B1, B3, D1 is the coordinator's.

## Decisions taken on my own

1. 4.R5: fixed in check.py (an imported definition is defined) rather than retyping the three
   externs, which already had types.
2. ε̂ = min(1, −log δ / n), the spec's rule of three generalized, not the exact 1 − δ^(1/n)
   (smaller by about ε̂²/2); its soundness a law with a control.
3. A statistical (`Tested`) or an assumed pass gives no (ε̂, δ) pair; an exact pass gives (0, 0).
4. `delta` a `ProbabilityLevel` with default 0.05; `composition` a name of a core model (as
   `combine` is), the product refused unless `FailuresIndependent` is accepted by name.
5. Two bindings of one obligation compose as two obligations (by the demand's composition).
6. `certify`'s line shows ε̂ per conjunct and the composed pair; per-region ε̂ only in the run's
   record.
7. B3's law is L10.2's table (`ProjectsTheFiveGrades`), needed too so that 4.R3 sees the new data's
   constructors in a claimed law; `admits` admits one grade only.
8. D1 keeps the line's own control entry beside the conjuncts', so CONTROL FAILED keeps its meaning;
   a conjunct holding on a broken model is no control failure.
9. A conjunct is controlled also by a refuted control of the law it applies, at that law's cone,
   and by a pre-D1 line entry that names it; an axiom conjunct is exempt.
10. The detection rate is shown only when below one.
11. An axiom line or conjunct is graded assumed with evidence `{"Assumed": statement}`; test.lth's
    `RunIsPointsOrNotRun` relaxed accordingly; `ProductIsIndependent` claimed in core.lut.
12. The two new claims gathered in `EvidenceClaims`, and evidence_laws' lists renamed, to keep
    core_metrics' counts.

## Question

None for Luciano.
