# Report of agent M (machinery): a refuted model for the uncontrolled conjuncts

2026-10-26, Claude Opus 5.5, on `prompt-controls.md` beside this file (03d45eb). Committed by the coordinator from the agent's hand-back (its Write of the report was refused). Scope: the 46 conjuncts of `uncontrolled-2026-10-26.tsv` in bases (35), transformer (3), settling (4) and lists (4). Base commit 94cd82e. Everything ran in a local clone at ~/.cache/luthier-controls/M/tree (same tag v0.3, so the same cone hashes; its stores written there, never in the repository). Commits: 480e92c, 32b6fda, 7ba8def, f25f12e, 2417f8c, e9b9748. Files: `tests/tester/bases_controls.test.lut`, `lists_controls.test.lut`, `transformer_laws.test.lut`, `settling_controls.test.lut`, `settling_laws.test.lut`.

Of the 46, 32 now have a wrong model that refutes them; for the other 14 no wrong model can exist (section 2).

## 1. Controls added, per law

Each target was refuted at its own conjunct in `luthier test` (exhaustive, listed censuses). "Alone" means every other conjunct of the law held.

bases_controls.test.lut (the claims of core.lut's `CoreBases`):
- ExtendedIsAnObject: `leqEqual` (the order read as equality: reflexive, transitive, not symmetric) refutes Symmetric alone; `nearEqual` (equal within a half) refutes Transitive alone; their censuses are pairs and chains related by the wrong equality (the old `nothingEqual` relates nothing, so no census could reach those two).
- ErrorIsABase, all 13 conjuncts controlled in this file: `meanBase` (join the mean of two finite distances): Associative of the join, with Integral and the join's Pointwise2; `cubicBase` (a + b + ab(a + b)): Associative of the combination, with its Pointwise2; `shiftedUnitBase` (unit 1): Neutral of the combination, alone; `wrappedBase` (sum modulo 3, not monotone): Distributive, with Integral and Pointwise2; `minBase` (combination the smaller, unit = bottom = ∞): Absorbing and Distinct, with Integral and Pointwise2; `tolledBase` (join the smaller plus a half): Idempotent, with Integral and the join's Pointwise2; `firstFiniteBase` and `firstNonzeroBase`: the two Commutative conjuncts (controlled over the tree, not in this file's own reading before).
- CappedSumIsAssumptionFree, ProductIsAComposition, ProductIsIndependent (the evidence base; the model is only the tensor): `cubicComposition` (min(1, a + b + ab(a + b)) per part): Associative of the tensor, alone; `tolledComposition` (min(1, a + b + 1/8)): Neutral of the tensor, alone; `wrappedComposition` (the sum wrapped into (0, 1]): Distributive, Absorbing and Integral, plus the union bound for the capped sum (Integral can't fall without monotonicity failing too, since a monotone tensor with unit 0 is never below a part). ProductIsIndependent had no control line; it now has these three and `firstComposition`; its axiom conjunct `FailuresIndependent` is reported "not run", as designed. `firstComposition` also controls the capped sum's Commutative of the tensor in this file.

transformer_laws.test.lut: OnDoubles: `slackCompose` (a slack of 1/8 at each composition, sound, associative only when the third step's sensitivity is 1) refutes ComposeAssociative alone; `unknownPullsBackToZero` refutes UnknownGivesNoPullback alone.

settling_controls.test.lut: Measuring: `zeroNotExact` refutes ZeroDistanceIsExact alone; `firstRatio` refutes WorseRatioCommutes alone; `meanRatio` (the mean of two bounded ratios, an unbounded one absorbing) refutes WorseRatioAssociates alone. Settling, Associative: no new model needed; the census was wrong (3.1); with it fixed, the existing `thirdOfThree` and `twoSupportedConfirm` refute Associative, and every other control line refutes what it refuted before.

lists_controls.test.lut: ListIsTabulated: `offByOneTabulation` (right length, every entry one off) refutes AtBuild alone; the "stuck match" came from the old `badTabulation`, which builds `nil`, so `at` had nothing to index (it still refutes SizeBuild). HammingListIsAMetric: `shiftedHamming` (+1) refutes MetricZeroOnEqual alone; `squaredHamming` refutes Triangular alone; `negatedHamming` refutes MetricNonNegative together with Triangular (zero on the diagonal, symmetry and the triangle give d ≥ 0); `directedHamming` (weights 2 and 1 by direction) refutes Commutative alone.

## 2. Conjuncts still uncontrolled, and why

`luthier check -v` on the four laws programs in the clone, after the new controls ran with stores. Settling now has every conjunct controlled; Measuring 5 of 5.
- CappedSumIsAssumptionFree, ProductIsAComposition, ProductIsIndependent: Associative, Neutral, Commutative and Idempotent of the join, and Distinct (unit against bottom). They read only `evidenceDioid`'s join, bottom (1, 1) and neutral (0, 0), fixed definitions outside the model; the claim's only parameter is the tensor, so no wrong model can reach them: facts about a constant. To control them the join would have to become part of the model (a change to algebraic.lth's `EvidenceComposition`, not proposed here). 12 of the tsv's items.
- NatsIsAConversion: NatsOfNothing. The conversion's value at 1 is its own `else` branch, ∞, whatever `log` is.
- OnDoubles: UnknownComposesUnknown. `composeTransformers` returns `nothing` before it reads the model whenever a part is unknown.

## 3. For the coordinator

3.1. A binding by name reaches every conjunct, and the tester doesn't check it against the parameter's type. Bite C1 bound `x` and `y` to `ints` for `WithinIsMeasured` in settling_laws and settling_controls; in `Settling` the same names are the verdicts of `Commutative` and `Associative`, which then ran on integers (24 cases instead of 216): the law line's evidence for them was meaningless, and `thirdOfThree` got stuck instead of refuting Associative. Fixed in these files with `ofType "A" "ints"` (e9b9748). The tester gap (accepting a census value of the wrong type) is in tester.py, not touched; other programs may have the same clash.

3.2. tester.py crashes on a control line over a conjunction when some of its conjunct entries are known and the line's own entry isn't: `_conjunction_outcome` takes `base.evidence` from a reused outcome, the store's dict; `settle` then reads `.coverage` from it (AttributeError at tester.py line 2906). It happens exactly when a change of binding reaches only some conjuncts (e9b9748 does that for the 20 Settling control lines). A non-deep `luthier test` or `certify` of settling_controls.test.lut fails, and rerunning doesn't help; `--deep` (no reuse) passes. Fix `settle` or `_conjunction_outcome` to accept a reused outcome's evidence, or certify that file with `--deep`.

3.3. Per-file versus over-the-tree readings: `check -v` reads controls from the stores of the files it's given, so a conjunct controlled through a law's control in another store shows uncontrolled per file. Per-file controls were added for the four such conjuncts here.

## 4. Checks

`luthier check` clean on the five edited files. `luthier test --deep --no-cert` on bases_controls (40 s), transformer_laws (3 min), lists_controls and settling_controls (31 min): every new line refuted at the conjunct it targets, every old line still refuted. Then `luthier test` with stores in the clone for bases, lists, transformer, the settling law line and settling_controls (`--deep`, because of 3.2), followed by `check -v` on the four laws programs (section 2). Not run: certify, the suite.

## 5. Decisions taken on my own

1. Everything run in a local clone (same tag, same hashes), so no store in the repository changed before the coordinator's wave.
2. Where a conjunct can't fall alone, a model that breaks it with the fewest others, the reason in the model's comment (Integral with monotonicity in the evidence base, MetricNonNegative with Triangular, Absorbing with Distinct in the error base).
3. The conjuncts that don't read the claim's parameter are listed as unrefutable, not forced.
4. The Settling census fixed with a type binding on `A` (e9b9748), which changes the identities of the Commutative, Associative and WithinIsMeasured entries of the Settling lines.
5. Per-file controls for conjuncts already controlled over the tree (two Commutative in ErrorIsABase, the capped sum's Commutative of the tensor, Hamming's Commutative).
6. Measuring's new controls in settling_controls.test.lut, where the brief places controls.
