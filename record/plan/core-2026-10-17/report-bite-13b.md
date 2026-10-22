# Report: the core's bite 13b, the library's leftovers and the closing

Agent: Claude Sonnet 5.5, brief `prompt-bite-13b.md`, 2026-10-22, with one fork (group P, the
self-description files: program, library, translation, term, term_model, grammar, ebnf, ebnf_model).
Scratch under `~/.cache/luthier-13b/` (not versioned): `metrics-*.txt`, `q/` (the differential's
script and terms), `p/` (the fork's), `pass1/`, `pass2/` (one log per program), `pytest/`,
`pytest2/`, `runs/`. Commits: fa25afe, d66f04e, 9d4595c, 09182bb (the fork), 9df8066, then the
agent's own up to the stores and the run records.

## What changed

- Homonyms (30 between machinery files and the rest): renamed `Demand` to `ConeDemand` and
  `Drawing` to `DrawnParameter` (certification.lth), `Record` to `RunRecord` and `Store` to
  `RunStore` (demand.lth), `State` to `WorldState` and `World` to `ReadableWorld` (world files,
  plot), `Resolution` to `StepResolution` and `uniformPValue` to `kolmogorovPValue` (probability),
  generators' `Support`, `Interval`, `NonNegative` to `WeightedSupport`, `ProperInterval`,
  `SupportNonNegative`, laws' `Pair` to `EvidencePair` and `exact` to `holdsExactly`,
  certification_model's `identity`, `grade`, `contains`, `disputed`, `isFailure` to
  `entryIdentity`, `certificateGrade`, `reachContains`, `certificateDisputed`, `entryFailed`,
  plan_model's `agree` to `schedulesAgree`, the fixture core_instances' `identity`, `larger`,
  `smaller`, `first`, `square`, `absDistance`, `gamma2` with an `Int` or `Float` suffix. The fork
  renamed the self-description side (grammar `Field`, `pi`, `record`, `kindOf`, `RoundTrip`,
  `Canonical`; translation `bin`, `Negation`; program `known`, `lit`, `isProvisional`,
  `pairNames`; term `withData`). `larger` and `smaller` are now one definition each in the core
  (core/structures/equality.lth, plan 5.1), `determined` of certification.lth is gone (unused), and
  demand.lth's `C` is certification.lth's. Count (1): 44 to 0 with two accepted, each with its
  reason in `ACCEPTED_HOMONYMS`: `Unresolved` (a constructor the host's Python reads in two places,
  `tester.SETTLED_BY_TEST` and `certify.py`, so a rename changes the store format) and `scale`
  (arrays_model's name for the extern of the `Arrays` record against plot's public name, which waits
  for G1 to G5).
- List helpers (2): 185 to 48. The fork took the self-description files from 114 to 29. Mine:
  plan.lth (`readsOf`, `readsOfAll`, `keep`, `readyIn`, `atIndex`, `headOr`, `tailOf`, `highest`,
  `keepRead`), plan_model.lut `round`, certification.lth (`latestWith`, `disputeAt`,
  `latestInFront`, `failureAt`, `largestAt`, `overBindings`, `reachOf`, `coversAll`,
  `withSupport`, `latestOf`, `latestAt`, `eraseProgram`), certification_model.lut (`passes`,
  `bestUnder`, `weakestOfBests`, `meetReaches`, `anyFailure` to `hasFailure`), generators.lth
  (`firstWeightOf`, `firstBinding`), world (`appendStr` gone for `<>`) and the helpers of eight test
  programs. Kept, each with a comment "kept as a recursion (bite 13b)": certification `behind`,
  `disputes`, `prepend`, `sumOfLargest`, `overRegions`, `bindingsFrom`, `along`; demand
  `determined`; generators `pick`, `before`; plan `addNew`, `placedBefore`, `runFrom`, `byLevels`,
  `demandAll`; plot `swapAt`; probability `allUnit` (generators_model.lut and tests/test_tester.py
  import it); lists_controls `emptyPredicate`, `distinctPredicate` (broken controls that ignore the
  list, whose match 4.R3 asks); and the fork's 29 (telescopes, state threaded left to right, left
  folds, early-stop searches, tree traversals, the tokenizer's fuel).
- Unclaimed (3): 21 to 7. Gathered in the file that states them, as 12b did: `DemandPassesDown`,
  `FamilyLaws` (six generator laws), `ExampleFacts` and `ResultsStore`. Left, none a law: `withinOf`
  (numbers.lth), `isConverged` (optimization), `hasColumn` and `sameTable` (tables), `controlPasses`
  (test.lth), `top` and `bottom` (core_instances' Bool constants). `check` reports any Bool-typed
  definition no other body of its file mentions; these are predicates and elements used by other files.
- `Settling` has a model, `laws_model.lut` (`settle`, `combineVerdicts`), and two test programs,
  `settling_laws.test.lut` and `settling_controls.test.lut`: its 18 conjuncts, the two of the
  combination among them, graded (11,534 cases) and 18 controls refuted, one broken model per
  conjunct. The four `forall`/`exists` laws name their quantified law `body` instead of `p` so that
  one census can bind it beside the conjunction laws' `p`.
- Bite 13c's four places (coordinator's addition): `Identity` carries `Sampling` (the eight budgets
  of 13c's item 2) with `samplingOf`, its law `IdentityIsTheKey` has a law line and a control
  (an identity that reads no budget); `censusOfAtMost` has the two readings (a parameter enumerated
  whole reaches its support, through a hole `enumeratedWhole` because strings are opaque to the
  kernel; a pass with no case bounds no census); a theory `Pruning` with three laws
  (`PruningKeepsACurrentFailure`, `PruningOnlyDrops`, `PruningNeverRaisesAGrade`), a reference
  `keepCurrent` in certification_model.lut and three controls refuted (forgets failures, drops
  a disagreement's entries, invents entries). NOT done: the conjunction route and witness of
  `refuse` (13c's items 3 and 4). It needs `ConeDemand` to carry the theory's conjunction and the
  model the run gives, and the exception of D-2026-10-22-d, which is a design of its own; the
  specimen says more than the theory there. A confirmed control, which certify.py also keeps, has no
  `Outcome` in the theory and is not stated either.
- Check refusals (item 4): distances.lut `pairI`/`pairJ` (`firstFrom` returns `Fin nodes`),
  plot_cases.lut `perms` (named permutations typed `Fin 3 -> Fin 3`), lists_controls (the broken
  predicates match `nil` and `cons`), experiment_zero.run.lut (imports `eliminated` and `known`).
  `luthier check` is clean on every file of lib, examples and tests/tester.
- check.py `loose` (item 5): reported only for a function no theory of its file names (a theory's
  fields and the names in its laws' bodies). core_metrics' split follows; test_core_metrics updated.
- Tests that followed the renames: test_run (CLASHES is now `Unresolved`, `WorldState`,
  `schedulesAgree`), test_tester, test_certify (the four new laws and controls), test_elaborate,
  test_core_metrics, tests/eval/plan_agree.lut, tests/run/first_action_models.lut.

## Differential (old 70532a8 against the working tree, `luthier eval`)

Plan: 49 terms, 49 equal. Certification and its model: 64 terms (`latestWith`, `disputeAt`,
`disputes`, `failureAt`, `latestOf/At`, `largestAt`, `sumOfLargest`, `reachOf`, `coversAll`,
`withSupport`, `passes`, `bestUnder`, `weakestOfBests`, `meetReaches`, `certifying.grade`,
`transport`, `bindingsOf`, `pooledCases`, `refuted`, `eraseProgram`, edge cases of empty lists and
repeated identities): 61 equal, 3 differ only in print, all of `latestInFront`, whose `notBefore` is a
declared hole, so both sides are stuck (old prints the `and` chain, new `stuck match` through `conj`).
Not evaluated: `overBindings` and `overRegions` through their region arguments (covered by
regions_laws and regions_controls certifying again with no change), `sumOfLargest` kept. The fork's:
5,210 terms, all equal (report in its hand-back: program.lth 4,375, term_model 457, others 378).
The old tree needed `larger`/`smaller` removed from its certification_model and probability to load
beside the new core; nothing else was edited in it.

## Checks

- Certification, `luthier certify --jobs 1`, three programs at a time, a log per program: pass 1
  593 lines ran (no refutation but the fixtures' AndIsOr and Small and the known not-run lines
  RootIsNotNegative, Partial and PrecisionSymmetric); pass 2: 0 lines ran for all 42 programs. Exit 1
  only for cases, laws (fixtures) and belief_laws (PrecisionSymmetric not run, 7.R4).
- validate_graph prints the same line as its record; experiment_zero on A (record 17's parameters)
  and on A without A2: the output equals the previous record's line for line but the header paths; the
  keys are new (the cones moved).
- Suite, file by file under `timeout 1800`: 42 files; first run 5 failed (stale expectations of my
  renames and the new laws, listed above); after the fixes test_certify 70 passed, test_run 146,
  test_tester 24, test_core_metrics 7, test_elaborate 69; the other 37 files passed in the first run.
  test_check_private collects nothing (rc 5).
- `python scripts/check_spec.py`: only its known finding (03-kernel.md:192).

## core_metrics (scripts/core_metrics.py)

| count | before (70532a8) | after |
|---|---:|---:|
| (1) homonyms | 44 | 0 (2 accepted) |
| executive shadows | 107 | 113 |
| (2) list helpers | 185 | 48 |
| (3) unclaimed | 21 | 7 |
| loose | 1979 (real 1334) | 1411 (real 1343, rest 68) |

The shadows rose by the renames' new names meeting executive files' locals (not counted in (1) to
(3)). The 1343 real loose functions are the library's functions at a bare exponential no theory names;
they are too many to list, and bringing them under theories is the queue's work, not this bite's.

## Notes for the spec's agent

4.S17: the loose report is narrowed as above (the sentence "a top-level definition at a bare
exponential is a loose function" stands; the report skips what a theory of the file names).
7.S8 and 7.S13 already say the sampling budgets enter the identity (13c). 12.S4 and 12.S22 are
as built (every file under lib/core/ is the prelude). 4.R13: the claim at a subtype and the operator
bindings no longer reach a sibling subtype (12a, 13a). `Settling` now has a reference model; the
spec's chapter 7 may cite laws_model.lut.

## Decisions taken on my own (one commit undoes each)

- Accepted `Unresolved` and `scale` as homonyms, each with its reason, rather than changing the store
  format or plot's public name.
- Renamed the non-Python-visible side of each homonym pair (generators' `Support` and `Interval`,
  not certification's constructors).
- Gathered unclaimed laws in unannotated conjunctions in their own file, and left seven predicates
  and constants named, not forced.
- `Settling`'s model reads `At` as the law's argument without a check against its type, since the
  kernel does not check it; `body` for the quantified law's name.
- `Pruning` is of one law's store (the reference `keepCurrent`), not per group as certify.py's.
- Narrowed `loose` by the file's own theories only (cross-file theories do not absorb it).
- Edited tests/test_run.py, test_tester.py, test_certify.py, test_elaborate.py and
  test_core_metrics.py where my renames made their expectations stale.

## Question

The 1343 real loose functions and the missing conjunction route in `refuse` are the two things the
core leaves: do they go in the queue before the tag, or after it?
