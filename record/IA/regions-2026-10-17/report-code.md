# Report: the evidence per region, in the code (3j, j2a)

By Claude Opus 5.5, an agent of the coordinating session, on prompt-code.md, 2026-10-17. Implements
items 1, 2, 3, 4, 6, 7, 9 and 10 of report-theory.md section 5 (D-2026-10-16-i, D-2026-10-16-j,
L9.16). Items 5 (branch coverage, the third source) and 8 (`cover`, 7.S14) are left for the next
bite; the spec says so in 7.S14.

## 1. What was written

Commits on `numbers`, in order:

- bf2f204 generators.py: 7.S4's special values (`specials`, `special`: the bounds and their
  neighbours, 0, 1, -1, the literals given, and for a cutoff its double and its half) and the atom
  at zero, with the budgets' `specialMass` and `atomAtZero`; 7.S5's census of dimensions
  (`DIMENSIONS` = 0, 1, 2, 3, 5, 10, those not above the size) and the zero and rank-deficient
  families with a share (`degenerate`) in `symmetric`, `symmetricOf`, `gram` (items 1, 2).
- 02ce948 arrays.py restored (see finding 2); the families live in generators.py.
- 1335113 tester.py: the `Classifier` (items 3, 4, 9): the degenerate cases a theory declares for a
  parameter's type, counted with `casesOf`; the two sides of each cutoff parameter (`Tolerance`,
  `RankFloor`, `Sequential`); the boundary of each other parameter of a subtype; an author's
  declaration in the test program recorded as a label with its share. The entry records `regions`
  and `labels` (item 6). The census checked against its parameter's predicate (item 10). The
  numbers the tester draws take the special values, a drawn matrix its dimension from the census and
  the two families. certify.py: `certificate_grade` is `regionedGrade` (item 7): per binding the
  strongest pass, combined over the law's regions (an empty region caps at sampled), then across
  bindings, with the combination `weakest` (default) or `strongest`; `standing` names the empty
  regions that lowered a grade. run.py: `combine` a field of the run's demand, `run --combine`.
- 6cd51f1 spec 7.S4, 7.S5, 7.S9, 7.S14, 5.S8: what is implemented and what is not.
- 4f49124 tester: a subtype of a cutoff type is a cutoff (`ClearFloor`).
- 769258b tests/test_regions.py (13 tests).
- c3a70f9, 5c05cbd, 28b14c3, c1eb2dc, b3204cf, 2070458: fixes the full suite and the first
  re-certification found (the entry's fields in test_certify; a census predicate that reduces to no
  Bool passed over; `serves` keeps its two arguments and `serves_over` reads the regions, so
  test_run's spy is untouched; `Small` is first refuted at x = 552 now that special values are drawn;
  a law with no regions reads no stretch; a type parameter gives no boundary).
- d960aa3 the stores re-certified (all but arrays_model.cert.json, kept at HEAD: finding 1).
- ef6ec51, 6b3d23c evidence: arrays_model's store as the re-certification left it
  (`arrays_model.recertified.cert.json`) and the two counterexample matrices
  (`pinv-counterexamples.json`).

## 2. The checks

`python -m pytest -q` at 921403c with the stores of d960aa3 (identical files): 812 passed, 6
skipped, 9 xfailed in 1343 s (799 before, plus 13 in test_regions.py).

`python3 scripts/check_spec.py`: its known finding only (03-kernel.md:190), "185 implemented, 80
decided (of which 33 suspended), 8 proposed".

`luthier certify tests/tester/*.test.lut --deep --fuel 3000000 --jobs 5` (198 min), then
belief_laws again (its disputes, finding 4) and world_laws and world_controls again (after
2070458). Then `luthier certify` without `--deep` over the same 36 files: every line known except
arrays_laws (10 lines: their generator fingerprints changed and arrays_model is at HEAD, finding 1),
belief_laws (3 lines that spend more than 3e6 fuel, never stored, finding 7), cases.test.lut (its
2 fixture lines), laws.test.lut and weakest.test.lut (stores of test programs, removed, finding 8).
Lines it prints that are not a grade: PinvSymmetric and PinvScales refuted (finding 1), the
fixtures of laws.test.lut and cases.test.lut, and `CONTROL FAILED` for LeqTransitive on leqSlack
(finding 5). core_laws.test.lut appeared during the run and is not mine; it was not certified.

## 3. The grades that changed

Standings of the 211 laws the tester files name, read from the stores before (5a7b8f1) and after:
120 sampled, 83 cases, 7 uncertified, 1 supported before; 125 sampled, 78 cases, 7, 1 after. Law
by law, with the empty regions that caused the fall:

| file | law | before | after | empty regions |
|---|---|---|---|---|
| belief_laws | PrecisionSymmetric | cases | sampled | tol above, tol below, n boundary |
| plan_laws | Confluent | cases | sampled | empty, one element (List) |
| plot_laws | LayerOrderInvariant | cases | sampled | margin boundary |
| world_laws | HostObserveChangesNothing | cases | sampled | empty, one element |
| world_laws | HostChangesOnlyDeclared | cases | sampled | empty, one element |

In the evidence store of arrays_model (not committed): PinvSymmetric and PinvScales sampled to
refuted (finding 1), RankUnderRotation sampled to a replay disagreement (finding 4). Laws already
sampled now print their empty regions (MaximizerAscends and two others: s, n and x0 boundary;
in arrays: RankBounded, PinvProjects, PinvTraceIsRank, PinvRestricts: 0 x 0 and the sides of tol
and fl).

## 4. Findings

1. Two laws refuted in a newly drawn region, the rank-deficient family (a zero row and column).
   PinvSymmetric (arrays_laws.test.lut line 127, seed 20261014): at a 10 x 10 symmetric matrix of
   rank 9, (s p)[3,5] = 0 exactly and (s p)[5,3] = -1.75e-16, while the scale (|s| |p|)[3,5] is 0,
   so the law allows no difference there. The error of the transposed entry is bounded by
   (|s| |p|)[5,3], which the law does not add: its scale is one-sided. PinvScales (line 130, same
   seed): at a 5 x 5 matrix of rank 4 and c = 8.361370115381893, both conjuncts fail at entries of p
   that are exactly 0 (pinv(c s)[2,1] = -5.06e-19 against p[2,1] / c = 0, scale |p| / c = 0): an
   entrywise scale leaves no room for the rounding eigh leaves at a structural zero. numpy is right
   to within rounding in both; the laws' error models (11.S18) have no normwise term. Neither law was
   touched. arrays_model.cert.json is kept at HEAD, since with the refutations every run over numpy
   is refused (test_run, test_lm and test_plots fail); the re-certified store is the evidence file.
   Any `luthier certify` of arrays_laws.test.lut writes them back (its generator lines are new
   identities).
2. The 6 test_run failures the coordinator reported: the first version of item 2 edited arrays.py,
   and `host_hash` hashes the bytes of the module behind a route, so every numpy entry went stale.
   Restored in 02ce948. generators.py is the same for generators_model: editing it stales that
   model's entries and changes the fingerprint of every generator binding.
3. RankUnderRotation's sampled line is not run, before and after: `Orthogonal tol k` is drawn by
   filtering and no value comes in 2000 tries (k = 9 before, k = 3 now). The family `orthogonal`
   exists in generators.py; the line does not bind it.
4. `--deep` replays disagree wherever the tester's draws changed, since `interpreter_revision` is
   the last tag and no tag comes until after the core (D-2026-10-17-e): RankUnderRotation,
   PrecisionSymmetric and DensityPeaksAtMean (two not-runs whose reasons name another dimension).
   A second deep run resolves them (D-2026-10-15-f), done for belief_laws. Every later change to the
   drawing code will do the same.
5. The control of LeqTransitive on leqSlack failed at seed 20261015, 100 cases: the slack model is
   refuted only when x - z falls in (1, 2], and with the special values and the atom at zero taking
   mass the filtered chain never landed there. The control was not edited.
6. A tolerance bound to a census of one (1e-12) almost never has a number of the case within a
   factor 2, so its two sides stay empty and a listed or exhaustive line with a tolerance caps at
   sampled. The same for `n : Nat` bound to 3 (its boundary is 0 and 1).
7. MaximizerAscends, MaximizerStationary and MaximizerKeepsDimension on fitA (ExhaustiveMode) spend
   more than 3e6 fuel and are never stored; it predates this bite (their censuses' fingerprints had
   changed).
8. Certifying a test program that defines its own laws (laws.test.lut, cases.test.lut,
   weakest.test.lut) writes a store beside it (`law_file` falls back to the test program), against
   "a test program keeps no store". I removed the three files.
9. PinvProjects spends about 1.28e6 fuel per 10 x 10 case, above the default 1e6; the census of
   dimensions draws 10 at size 10 often, so its lines need `--fuel 3000000`.
10. The first re-certification ran with a bug (the census check raised on `Concrete`'s
    `hasStructuralEquality`, refusing the world laws); its stores were discarded before any commit
    and the run repeated.

## 5. Decisions taken on my own

- Near a cutoff c: a number of the case's other parameters in (c, 2c] is above, in [c/2, c) below;
  a cutoff of 0 has no sides; the width is `CUTOFF_WIDTH` (P11). The special values of a cutoff are
  its neighbours, its double and its half.
- The boundary of a premise stated by a cutoff: the predicate holds at the cutoff and fails at it
  times or over the width; of a premise with bounds: the bounds and their neighbours; of an exact
  premise: every case. A type parameter (`S : Concrete`) is no premise.
- A degenerate case whose witness is outside the parameter's type at every case is dropped.
- The rank-deficient family is a zero row and column (stays symmetric); the families' shares and
  the matrix shares default to `specialMass` (0.05); dimensions from the census, capped by the size.
- A declaration of degenerate cases in the test program is an author's label.
- A census predicate that reduces to no Bool is passed over.
- An agreeing replay that adds regions where the known entry had none is written in front.
- The combinations are `weakest` and `strongest`; `run --combine` and a `combine` field of run.py's
  demand, not yet in demand.lth; `certify` reads the weakest. `serves_over` beside `serves`.
- arrays_model.cert.json kept at HEAD, its re-certified store committed as evidence.
- The test programs' stores removed; the first re-certification discarded.

## 6. One question

PinvSymmetric and PinvScales fail only because their tolerance scale is entrywise (finding 1). Do
you want their error model corrected (the scale of both entries compared, plus tol times |s| |p| in
norm on every entry), after which arrays_model is re-certified and committed, or the refutations
committed now, with runs over numpy refused until the laws change?
