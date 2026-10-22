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

## Before the tag: refuse's route and witness

Brief: `record/plan/core-2026-10-17/prompt-refuse-theory.md`. Agent: Claude Sonnet 5.5, 2026-10-22.
Python: `/home/lmoffatt/miniconda3/bin/python`. Scratch: `~/.cache/luthier-refuse/` (the comparison
script `compare.py`, the certify outputs). Commits: 4f24573 (the theory), c05fbf9 (the model), 55a05d7 (laws,
controls and stores), be84185 (the rework that kept core_metrics' counts down), 79f606d (the lines moved
into their own files), 46da7ee (their stores).

### What was missing

13c's items 3 and 4 and D-2026-10-22-d put in certify.py a route (a demand resolved to its subject
and obligations), a witness (one entry per obligation) and a veto (read once over every subject,
scoped by reach, with the refuted-consequence exception). `certification.lth` said nothing of
them: `refuse` takes a `ConeDemand`, which has no place for the theory's conjunction or the model the
run gives. [proposed] Rather than widen `ConeDemand` (every law of §5 builds one), §6 is a theory
beside `Certifying`: `Routing k` with `headOf`, `witness : Routed -> List Entry -> Maybe (List Entry)`
and `veto : Routed -> List Entry -> Maybe Veto`, where `Routed` holds a `ConeDemand`, `byModel`, the
model parameters and the theory's conjunction (`Theory`: its demand and the names that head the
conjuncts the law stands for).

### The laws (certification.lth §6, `Routing`; the specification is `routeSpec`, one record of
operations with local helpers)

1. `AWitnessCoversEveryObligation`: each obligation the demand resolves to has, in the witness, an
   entry of the store that serves it (and carries its conjunct); a demand with no open route is
   never witnessed.
2. `AWitnessIsOneEntryPerObligation`: the witness has as many entries as the demand has obligations.
3. `AnEntryForEveryObligationWitnesses`: a demand whose obligations each have an entry is witnessed;
   one with an obligation without an entry, or with no route, is not.
4. `AVetoNamesItsCause`: a veto is a disagreement between two entries of a subject, or a failure of
   one (or, for the exception, of the law's own entry at its hash).
5. `AFailureInASubjectVetoes`: a failure in any subject, the law's own or the theory's for the run's
   model, vetoes whatever route would serve.
6. `ADisagreementInASubjectVetoesFirst`: a disagreement in any subject is read before any failure.
7. `AnEntryAboutAnotherModelVetoesNothing`: an entry of the law whose reach excludes the run's model
   adds nothing, unless the law is refuted as a consequence (D-2026-10-22-d's scope).
8. `AConsequenceRefutesEveryModel`: a failure on a model that passes the theory's defining laws vetoes
   every model's run (D-2026-10-22-d's exception).

Resolution (`routeSpec.obligations`): the law's own conjuncts when its entries at the hash list
some; else the law itself when an entry serves it (not for `byModel`); else the theory's conjuncts
headed by one of the law's names. Admission is "the witness is something"; the run's record lists
the witnesses of its demands and the result key hashes that record (L5.6, 8.S8), so the one set is
read by all three: that last link lives in run.py, the theory states the set.

The laws are in `tests/tester/certification_route.test.lut` (a file of its own: test_certify lists
the lines of certification_laws.test.lut one by one, and adding to it broke that list), over 7 listed
demands (two `byModel`, `T` whole, `P` direct, `L` on `M` with and without its theory, `L` on `N`)
and 16 stores (passes, a conjunct failing, in disagreement, a failure on another model, with the
other model passing the theory, failing it, passing another version of it). All eight laws are
graded `cases` (ExhaustiveMode over the listed cases) and controlled.

### The controls (`certification_route_controls.test.lut`), each refuted

| wrong model | law refuted | first counterexample |
|---|---|---|
| a witness that keeps the first entry only (drops an obligation) | `AWitnessCoversEveryObligation` | `T` whole over `[tpM, tqM]` |
| a witness that serves `byModel` from the law's own entries | `AWitnessCoversEveryObligation` | `P` byModel over `[pM]` |
| a witness that adds an entry the demand does not need | `AWitnessIsOneEntryPerObligation` | `P` byModel over `[tpM, tqM]` |
| a witness that never serves | `AnEntryForEveryObligationWitnesses` | `P` byModel over `[tpM, tqM]` |
| a veto that invents a failure | `AVetoNamesItsCause` | the empty store |
| a route that skips a veto (reads only the law's own entries) | `AFailureInASubjectVetoes` | `P` byModel, `P M` fails on `M` |
| a veto that reads failures before disagreements | `ADisagreementInASubjectVetoesFirst` | `P` byModel, `P M` in disagreement |
| a veto not scoped by reach | `AnEntryAboutAnotherModelVetoesNothing` | `T` on `M`, a failure of `T` on `N` |
| a veto scoped by reach with no exception: it passes the defining laws of `N` and still refutes only `N`'s runs | `AConsequenceRefutesEveryModel` | `L` on `M`, `L` fails on `N` and `T` passes on `N` |

### The model (certification_model.lut, `routing`) and its agreement with certify.py

`routing` follows certify.py's `witness`, `_each`, `_obligations`, `_conjunct_witness` and `veto`,
`_about`, `_passes_theory`, in the order the code reads them, written as a record with the helpers
local (so the section adds no loose function). `headOf` is the host's `certify._text_head` through
`extern`. Compared on the 16 demand/store pairs of tests/test_certify.py that exercise these paths
(`_by_model`, `whole`, `_direct`, with the stores of the 13c and 13c follow-up tests), the model and
`certify.witness`/`certify.veto` agree on all 16: whether the demand is witnessed, how many entries
the witness holds (1,1,1,1,1,1,1,0,2,0,1,1,1,1,1,1 in both), and what the veto is (none, Current,
Disagrees, or the exception, whose flag is the "why" certify.py words). Cases: the 5 of 13c's item 3
(passes only, the conjunct failing, another conjunct failing, a failure on another model, a
disagreement), the 5 of item 4 (`P`, `Q`, `Q` lacking its entry, `T` whole, `T` whole lacking one),
the 6 of D-2026-10-22-d (a failure on `N` with the run on `M`, on `M`, on `N`; the exception; `N`
failing `T`; another version of `N`).

Where they differ, by design, and the theory says so in its header:
- fingerprints: certify.py's `at` compares the fingerprints of the models a demand names, and
  `_passes_theory` intersects the comma-separated sets of a census; the theory reads an entry's hash
  only (as `serves` does) and compares a fingerprint whole.
- regions: certify.py's witness reads an entry's grade over the law's regions (`serves_over`); the
  model reads the entry's own grade (`Regioning` states the other).
- a control's entries (`_laws_own`) are not entries in the theory; the demand a refusal names and
  the words of the exception are not modelled.
- `witness` order: the model lists the entries in the order of the conjuncts, as certify.py does;
  the laws do not constrain the order.

### Checks

- `luthier check`: clean on certification.lth, certification_model.lut, certification_route.test.lut
  and certification_route_controls.test.lut (and on the two older certification test files).
- Certified twice (laws, then controls, then both again): second pass 0 lines ran on all of
  certification_laws, certification_controls, certification_route and certification_route_controls.
- `python -m pytest -q tests/test_certify.py tests/test_tester.py`: 94 passed, 3 skipped (7 min 57 s; run on the tree before the last rename of a helper in the two route files, which test_certify and test_tester do not read).
- core_metrics (before c44d0e5 / after): homonyms 0 / 0; executive shadows 113 / 113; list helpers
  48 / 48; unclaimed 7 / 7; loose 1411 / 1408 (real 1343 / 1331, the rest 68 / 77: the rest are the
  functions a theory names, and the new `routeSpec` and `routing` records name some that were real).
  No count is up except the "rest" part of loose, whose total is down.

### Decisions taken on my own (one commit undoes each)

1. A theory beside `Certifying` (`Routing`) rather than a wider `ConeDemand` or a change to `refuse`.
2. The specification (`routeSpec`) and the model (`routing`) written as records with local helpers,
   after a first version with top-level helpers raised core_metrics' loose count by 43 and the
   list-helper and homonym counts: the cost is less readable code, the gain is that no count rises.
3. A fingerprint is opaque and compared whole in the theory (certify.py intersects sets).
4. The laws and their controls live in `certification_route.test.lut` and
   `certification_route_controls.test.lut`, not in the two existing files, because test_certify.py
   enumerates those files' lines (I was told to touch only certification_* files, so I did not edit it).
5. The exception law and the scope law quantify over listed stores that contain the case (N passing
   `T` at the fingerprint the failure recorded); a store the census does not name is not drawn.
6. Gaps (fingerprints, regions, controls' entries, the refusal's `by` and `why`) left out of the theory
   and named in its header and in the model's.
