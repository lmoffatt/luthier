# Report: every law of the slice refutes a wrong model (L9.14, D-2026-10-15-a)

Brief: record/IA/controls-2026-10-15/prompt-mutants.md. By Claude Opus 5.5, a subagent of the
coordinating session, 2026-10-15. The control files were split across four Claude Sonnet agents
(arrays; numbers; probability and generators; belief, optimization and fit) and written by me for
tables, world and plot; I reviewed and committed each file alone. No theory file touched.

Principles touched: L9.14 (every law carries a model it refutes), applied; P11 (every criterion a
parameter) for the budget binding; P2 (everything derived carries how it was derived) for the
two model stores committed. Assumes a control matches its law by the law's cone hash, as the
tester's report established.

## Commits

- ebdb7ff run.py: the stale docstrings now name demand.lth's `lawDemand`, `recorded` and
  `Store`'s `OneIdentityOneResult`.
- f717a7e belief_laws.lut, d74df31 fit_laws.lut: `budget` bound in the cutoffs, a census of one,
  50 [proposed], as the fix agent's probe. fit_laws.lut still passes every line with it (51 s).
- Controls, one file per commit: 24c5aff numbers, 777f7ae world, 6083774 tables
  (seven lines added to the existing one), cfd4188 plot, b777faf belief, 6f71003 optimization,
  afe6eaf fit, 331f4e3 arrays, e90e4fe generators, a14bc0c and a84e670 probability.
- fc7105d test_certify.py and 530da6a test_tester.py: the two tests that pinned
  tables_controls.lut to its single line now expect eight controls, each passing.
- efea8bb belief_model.cert.json, 71ddc7b optimization_model.cert.json: derived, the entries my
  certify run wrote at 7f718e9 (the lines whose cone changed: QuadraticConverges with `budget`, the
  steps after the B/C/D fixes).

The tables stores: the leftover `Failed: t = holeT` entry is gone from tables_laws.cert.json (a
copy of the store before is not kept in the repo; the stores are ignored) and both stores were
refreshed by `luthier certify`. tables_controls.cert.json still holds its old-form `Failed` entry
next to the eight new `Control` entries: emptying that store was refused by the session's
permission classifier, and the brief named only the laws store. It does not change any status.

## The run

`luthier certify --jobs 2 --fuel 100000000`, with stores, in two runs: every `*_laws.lut` with its
`*_controls.lut` except probability and generators, at 7f718e9, exit 0, 32 min; probability and
generators, at a84e670, exit 0, 43 min. The second ran while the agent rewriting the statistical laws
had its own edits in the tree (probability_laws.lut then already had SourceIsUniform,
NoAlternativeAtZero, RatioNonNegative; their controls came later, in d581b3b and 9219c90, and are
not in this run). `python -m pytest -q`: 708 passed, 5 skipped, 9 xfailed (that agent's uncommitted
changes to certify.py, tester.py and two test files were in the tree).

The per-law status lines, grouped; each line shortened by a script to the law, its grade and the
broken model its control was refuted on (certify printed `LAW: GRADE; controlled (refuted on its
control at BINDINGS)`).

Controlled (131 laws, every control refuted):

    arrays_laws.lut, 35 controlled:
      AddPointwise (sampled) on m = swapAdd
      SubPointwise (sampled) on m = swapSub
      ScalePointwise (sampled) on m = shiftScale
      TransposePointwise (sampled) on m = noSwapT
      MaddPointwise (sampled) on m = swapMadd
      MsubPointwise (sampled) on m = swapMsub
      MscalePointwise (sampled) on m = shiftMscale
      DotSymmetric (sampled) on m = skewDot
      DotOnBasis (sampled) on m = dropDot
      DotAgrees (sampled) on m = dropDot
      NormOfBasis (sampled) on m = norm1
      NormOfDot (sampled) on m = sqNorm
      NormScales (sampled) on m = sqNorm
      MatVecOnBasis (sampled) on m = doubleMV
      MatVecAgrees (sampled) on m = doubleMV
      MatMulIdentity (sampled) on m = doubleMM
      MatMulTransposes (sampled) on m = noSwapT
      MatMulAgrees (sampled) on m = doubleMM
      RankOfDiagonal (sampled) on m = rankFloor
      RankOfZeroAndIdentity (sampled) on m = rankPlus1
      RankBounded (sampled) on m = rankPlus1
      RankScales (sampled) on m = rankAbs
      RankUnderRotation (sampled) on m = rankDiag
      TraceOfIdentity (sampled) on m = trace1
      TraceAdditive (sampled) on m = trace1
      TraceCyclic (sampled) on m = traceTwice
      TraceAgrees (sampled) on m = trace1
      PinvOfDiagonal (sampled) on m = invDiag
      PinvOfZero (sampled) on m = ridge
      PinvOfIdentity (sampled) on m = ridge
      PinvProjects (sampled) on m = ridge
      PinvSymmetric (sampled) on m = skewPinv
      PinvTraceIsRank (sampled) on m = pinvFloor
      PinvScales (sampled) on m = ridge
      PinvRestricts (sampled) on m = ridge
    numbers_laws.lut, 42 controlled:
      PlusCommutes (sampled) on d = swapped
      TimesCommutes (sampled) on d = timesSkewed
      PlusZero (sampled) on d = plusOff
      TimesOne (sampled) on d = timesOff
      DivideOne (sampled) on d = divideOff
      TimesZero (sampled) on d = timesOff
      MinusSelf (sampled) on d = minusOff
      DivideSelf (sampled) on d = divideShifted
      MinusIsPlusNegated (sampled) on d = minusFlipped
      NegateTwice (sampled) on d = minusDoubled
      LeqReflexive (sampled) on d = leqStrict
      LeqTotal (sampled) on d = leqIsEqual
      LeqAntisymmetric (sampled) on d = leqAlways
      LeqTransitive (sampled) on d = leqSlack
      LessIsStrict (sampled) on d = lessLoose
      GreaterIsLessReversed (sampled) on d = greaterWrong
      GeqIsLeqReversed (sampled) on d = geqWrong
      UnequalIsNotEqual (sampled) on d = unequalWrong
      PlusMonotone (sampled) on d = plusFlipped
      TimesMonotone (sampled) on d = timesNegated
      EpsilonIsTheUlpOfOne (cases) on d = epsilonSmall
      DivisionAlgorithm (sampled) on m = quotientOff
      RemainderOfTheDivisorsSign (sampled) on m = remainderShifted
      QuotientOfProduct (sampled) on m = quotientOff
      ConvertZeroAndOne (cases) on c = convertDoubled
      ConvertAddsExactly (sampled) on c = convertOff
      ConvertSucceeds (sampled) on c = convertDoubled
      ConvertKeepsOrder (sampled) on c = convertNegated
      SqrtOfSquares (cases) on e = sqrtHalf
      ExpOfZero (cases) on e = expScaled
      LogOfOne (cases) on e = logShifted
      ErfOfZero (cases) on e = erfShifted
      SqrtMonotone (sampled) on e = sqrtNegated
      SqrtOfSquare (sampled) on e = sqrtHalf
      ExpPositive (sampled) on e = expNegated
      ErfOdd (sampled) on e = erfShifted
      ErfBounded (sampled) on e = erfDoubled
      SqrtSquares (sampled) on e = sqrtHalf
      ExpOfLog (sampled) on e = expScaled
      LogOfExp (sampled) on e = expScaled
      ExpAdds (sampled) on e = expScaled
      LogMultiplies (sampled) on e = logShifted
    belief_laws.lut, 8 controlled:
      PrecisionSymmetric (cases) on b = asymmetricB
      DensityPeaksAtMean (sampled) on b = negativeB
      PosteriorScoreIsGradient (sampled) on p = zeroScoreP
      PosteriorInfoSymmetric (sampled) on p = asymmetricInfoP
      QuadraticConverges (sampled) on mx = giveUp
      MaximizerAscends (sampled) on mx = jumpsAway
      MaximizerStationary (sampled) on mx = claimsAtStart
      MaximizerKeepsDimension (sampled) on mx = oneShort
    optimization_laws.lut, 6 controlled:
      GradIsGradient (sampled) on o = zeroGradO
      StepMatrixSymmetric (sampled) on o = asymmetricO
      StepMatrixNonNegative (sampled) on o = negativeO
      DirectionDescends (sampled) on m = flipped
      DirectionAgrees (sampled) on m = flipped
      StepRule (sampled) on m = phiLowered
    fit_laws.lut, 6 controlled:
      QuadraticConverges (sampled) on mx = giveUp
      MaximizersAgree (sampled) on mx = giveUp
      QuadraticStepAccepts (sampled) on m = neverAccepts
      DirectionDescendsOnQuadratic (sampled) on m = flipped
      DirectionAgreesOnQuadratic (sampled) on m = flipped
      StepRuleOnQuadratic (sampled) on m = neverAccepts
    tables_laws.lut, 8 controlled:
      RoundTrip (cases) on c = dropsLastWritten
      Canonical (cases) on c = dropsLastWritten
      Tolerant (cases) on c = dropsLastRead
      Rejects (cases) on c = lenient
      SchemaWellFormed (cases) on t = twiceNamed
      KindsKnown (cases) on t = unknownKind
      CellsOfTheirKind (cases) on t = holeT
      NoCellsOffSchema (cases) on t = answersAll
    world_laws.lut, 4 controlled:
      PrintAppendsALine (cases) on c = noNewline
      PrintChangesOnlyStdout (cases) on c = dropsFiles
      ReadGivesThePlace (cases) on c = readsNothing
      ReadChangesNothing (cases) on c = readClears
    plot_laws.lut, 8 controlled:
      FileExistsAfter (cases) on d = noFile
      FormatByExtension (cases) on d = allPng
      ImageOfTheValue (cases) on d = readsOffSchema
      RowOrderInvariant (cases) on d = firstRowApart
      LayerOrderInvariant (cases) on d = layerOrdered
      ImageSeesTheTitle (cases) on d = noTitle
      WriteThenRead (cases) on s = writesEmpty
      WriteChangesOnlyItsPlace (cases) on s = keepsOnlyIt
    probability_laws.lut, 14 controlled:
      KolmogorovOfNothing (cases) on d = kOffset
      KolmogorovOfOne (sampled) on d = kHalf
      KolmogorovOfMultiset (sampled) on d = kFirst
      KolmogorovBounded (sampled) on d = kDouble
      KolmogorovAgrees (sampled) on d = kOffset
      MeanShape (sampled) on m = badLength
      JacShape (sampled) on m = badRows
      JacIsJacobian (sampled) on m = zeroColumn
      ScaledShapes (sampled) on m = badScaledLength
      DLogSigmaIsGradient (sampled) on m = badScaledGrad
      TangentShapes (sampled) on l = badScoreLength
      ScoreIsGradient (sampled) on l = zeroScore
      InfoSymmetric (sampled) on l = asymInfo
      InfoNonNegative (sampled) on l = negInfo

Uncontrolled, with why:

    probability: GaussianPeaksAtMean, ProfiledIsGaussianAtItsSigma. Both state probability.lth's
      own construction (`gaussian`, `profiled`, `fixedSigma`) over a model, both sides reading
      the same mean and Jacobian, so no model breaks them; a wrong construction would, and passing
      one needs the construction as a parameter of the law, a new definition in the theory.
      Breaks tried: a Jacobian scaled by 1e150 (the law held: CONTROL FAILED, removed in a84e670 as
      aimed at the wrong thing), a mean one entry long and a mean of 1e200 (both raised, no verdict).
    generators: SymmetricGivesSymmetric, SymmetricOfGivesItsSize, GramGivesPsd,
      OrthogonalGivesOrthogonal, UnitListGivesUnitValues, ClearDiagonalGivesClear. Each names its
      family in its body, so no wrong family can be passed without making the family a parameter
      (generators_model.lut, not mine). generators_controls.lut has wrapper laws `XOnBroken`, the
      law's body on a broken family, each refuted; they show the predicate sees the break, but their
      cone is not the law's, so certify does not count them.
    probability: SourceIsUniform, NoAlternativeAtZero, RatioNonNegative; generators:
      UniformSampleIsUniform. The statistical law and its statistic's laws, the other agent's; their
      controls are in d581b3b and 9219c90, after this run.
    sonolocalizacion_laws.lut: LayoutFromUndoesTo, LayoutToUndoesFrom, FullAgrees, ProfileAgrees,
      ProfileIsFullAtItsSigma, ReportsValidity. Certified as the brief's item 3 asks, but not in
      item 1's list of files, so no controls were written.

CONTROL FAILED: none left.

## Findings

- LessIsStrict cannot see the most plausible bug, `less := a <= b`: it differs only at x = y,
  which the `linear` sampler essentially never draws. Its control uses `less := a /= b`. The same
  holds for any order bug confined to ties (LeqReflexive was refuted only on `leq` made strict).
  The law is fine; the sample has no ties. A tie-drawing generator for Float64 pairs would fix it.
- RankScales held on a rank with an absolute floor of 1e-3 in place of the relative one; it saw a
  floor of 1. Plain sampled RankScales and PinvSymmetric also held on their broken models, since
  the plain draw gives only 0 x 0 and 1 x 1 symmetric matrices (arrays_laws.lut's header says so);
  their controls bind the `symmetric` generator, as the twin lines do.
- The two probability laws and the six generators laws above are the cases L9.14 names: no model
  of their parameters can fail them. For the probability pair it's because they are statements
  about the theory's construction; for the generators it's because the family isn't a parameter.
- A certify run with stores writes the tracked model stores (belief, optimization and probability
  here). I committed the first two; probability_model.cert.json is left uncommitted, mixed with
  the other agent's run, and so is src/luthier/lib/probability.cert.json, untracked, theirs.
- Session A lines are slow as controls (JacIsJacobian, InfoSymmetric, InfoNonNegative over 11 min
  until the broken record bound the model's result once); arrays' rank and pinv controls on drawn
  matrices take most of that file's 3.5 min.

## Decisions taken on my own (each undone by one commit)

- `budget` 50 in belief and fit cutoffs, marked [proposed].
- Removed ProfiledIsGaussianAtItsSigma's control rather than keeping a CONTROL FAILED that blamed
  a model for what is a statement about the construction (a84e670).
- Kept generators_controls.lut's wrapper laws, though certify does not count them.
- Updated test_certify.py and test_tester.py to the eight tables controls.
- Committed belief_model.cert.json and optimization_model.cert.json as derived evidence.
