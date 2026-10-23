# Wave A, agent 1: bites A4, A5, A6

Claude Opus 5.5, 2026-10-23, on `prompt-wave-a.md` beside this file (f78d9ad) and `execution.md`
(A4, A5, A6). Base commit f78d9ad. Files touched: `src/luthier/certify.py`,
`src/luthier/lib/certification.lth`, `src/luthier/lib/certification_model.lut`,
`tests/test_certify.py`, `tests/tester/certification_route*.test.lut`, and two new test programs,
`tests/tester/certification_fold.test.lut` and `certification_fold_controls.test.lut`. The machine
rebooted during A6 (about 16:19); the uncommitted hunks survived and A6 was finished after it.

## A4. Obligations from the law, and the five operations (245d706)

What I did. Source: audit 1.3 (report.md, 5b1a05e); 7.S22; `Routing`.

- certification.lth §6: `Routed` and `Theory` each get a `conjuncts : List String` field, the law's
  conjunction as its definition states it. `routeSpec.obligations` and `inSubject` read those fields
  and no longer read the conjuncts the stored entries list. `refutedAsConsequence` still reads the
  conjuncts a model's entries list; a comment says why: a short listing errs toward a veto, never
  toward serving. `routing` in certification_model.lut follows.
- The route's listed cases gain a demand of `T` with a third conjunct, `R M`, that no entry lists.
  A new control (`fromListing`: the witness takes the obligations from the entries, as certify.py
  did before) is refuted at the store that lists `P M` and `Q M` only.
- certification.lth §7, new: `Held` with the constructors `EmptyFold`, `NoEntry`, `FailedObligation`
  and `HeldAt`; the reference operations `allOfWith`, `alternativeOf`, `restrictTo`, `projectGradeOf`
  and `admitAt`; the theory `Folding` with ten laws (unit, a missing obligation leaves no grade, a
  failure absorbs, alternatives keep the stronger, both folds associative, allOf never exceeds an
  alternative, restrict never raises, outside the reach nothing, an empty region at most sampled,
  admit is the cutoff on the projection). `folding` in the model is `allOf` at the weakest. The ten
  laws pass on listed cases, and three controls are refuted: a missing obligation used as the unit
  (the old double meaning of `None`), a pass that covers a failure among alternatives, and a
  restriction that ignores the reach.
- certify.py: `Held` and `all_of`, `alternative`, `restrict`, `project_grade`, `admit`. The
  certificate's folds (`certificate_held`, `_held_and_empty`, `regioned`) use them, so a conjunct
  with no grade is `NoEntry` or `FailedObligation` and never `None`. `_or_weakest` and
  `_or_strongest` keep `None` with one meaning only, the unit of a fold of grades, because
  tester.py's `_conjunction_outcome` folds from it (I found this when that test failed). New
  `obligations(demand, entries)`, the specimen of `routeSpec.obligations`, which `witness` reads;
  `_each` and `_conjunct_witness` are gone. `Cones.conjuncts(law)` gives a law's conjuncts as the
  tester names them. `certify_file` passes the conjuncts the tester split each law into, and
  `standing` says "no entry for its conjunct X" when one is missing.

Not done, needs another agent's file. run.py builds the demands, so the run path still falls back
on the stored listing; `obligations` says so in its docstring. Two lines close it: in run.py's
`certification`, `d["conjuncts"] = law_cones.conjuncts(law)` on each law's demand, and
`d["conjuncts"] = law_cones.conjuncts(theory)` in `_conjunction_demand`. A test already checks that
`Cones.conjuncts` names the conjuncts as the tester's entries do, on the tester's program. Run.py's
`law_cones` is another elaboration, so the same equality should be checked there when the lines go
in. `check -v` (cli.py's `_standings`) also still uses the fallback.

Checks. Tests that fail at f78d9ad and pass after: `test_a_store_listing_two_of_three_conjuncts_serves_nothing`,
`test_the_cones_give_a_law_s_conjuncts_as_the_tester_names_them`,
`test_the_five_operations_keep_the_laws_of_folding` (certify.py's five against the laws of
`Folding`, plus the two test programs) and `test_the_route_s_obligations_come_from_the_law_and_its_control_is_refuted`.
`tests/test_certify.py`, `test_regions.py` and `test_tester_conjunction.py`: 93 passed, 2 skipped.
`check_spec` prints only its known finding.

Stores it moves (for the coordinator's wave). The cones of the eight `Routing` laws and their nine
controls, now ten (the new `fromListing` control), changed because `Routed` and `Theory` did. The
ten `Folding` laws and their three controls are new. Both live in certification_model.cert.json
(certification_route*.test.lut and certification_fold*.test.lut). I did not run `luthier certify`
on the tree, so the acceptance "every store passes with 0 lines ran on pass 2, the `certify` output
unchanged" is the wave's to verify. By construction the output changes only where a conjunct has
no entry, and the tree has no such conjunct.

## A5. Pooling indexed by the obligation (98bb4c8)

What I did. Source: audit 1.4 C; D-2026-10-16-g; 7.S13. `union_key` (through `_without`) carries a
conjunction entry's conjunct before its sampling, and its docstring states the pooling
preconditions: one law, cone hash, binding with fingerprints, sampling identity and conjunct. It
also says that a seed is a replay coordinate and that the pooling rests on 7.S1's distribution law,
which the protocol owes and the code does not check. `stretches`, `pooled`, `pools` and
`continuation` get the conjunct through the key. `binding_evidence` and `regioned` take the
conjunct, so `certificate_held` and `witness` no longer prefilter the entries. `pools` names the
conjunct in its words when there is one. An entry with no conjunct keeps its key as before, so the
existing keys and tests are unchanged.

The theory: I left `stretchesUnder` filtering by binding alone and wrote the gap down in a comment,
so `Pooling`'s certified cones stay as they are (the acceptance says "stores unchanged"). Its laws
are about a law's own entries, where the conjunct is `nothing` for all of them.

Checks. `test_two_conjuncts_stretches_never_pool` fails at 245d706 and passes after: `P x` and `Q x`
under one binding never pool, and a statistical `Q x` does not continue `P x`'s test. The three
test files: 94 passed, 2 skipped, the pooling laws' test included. No store moves.

## A6. Checked construction at read (6cab2c2)

What I did. Source: audit 1.8; L10.10; 13c item 5. certify.py's `formed_errors`, called from
`store_errors`, checks each evidence form's own fields and names the field in its message:

- a proved entry: `evidence.Cited`, not empty;
- an exhaustive one: its mode or a finite domain (each parameter a census in `reach` or a generator
  `ExhaustiveMode ...`, or a `(Bounded n)` coverage with n above 0);
- a sampled one: `seed`, `binding.generator` for each parameter, and `budgets` holding
  `SAMPLED_REQUIRES`;
- a control: it never passed, and `binding.generator` for each parameter (with no binding, the
  law applies the broken model itself).

`SAMPLED_REQUIRES` is `SAMPLING` without `regionNumbers` and `regionEntries`: 232 sampled entries of
the tree were written before the regions and lack those two [mine]. In certification.lth,
`formedAsItsEvidence` is the same check over the theory's `Entry`, and `heldAsRun` now includes it.
The seed, the budgets and the control checks are the reader's alone: the theory's types give an
entry its seed and its full budgets, and its `Entry` has no kind. `Store` is used by no law, so no
store moves. No schema version field (P8, the plan's decision 4).

Not done:

- An assumed entry's demand. laws.lth's `Assumed` carries no field (Agent 3's file), and the tree
  has no assumed entry and no writer of one. It needs `Assumed : String -> Evidence` there first.
- `latestInFront` stays unchecked and `notBefore` stays a hole, for two reasons. The kernel has no
  order on `String` (11.R1; grammar.lth's `characters` is a hole too). And the predicate is false of
  five stores of the tree: laws.cert.json, numbers.cert.json and certification_model.cert.json in
  lib, distances.cert.json and session_a.cert.json in sonolocalizacion. The tester dates an entry
  when its line starts, and lines that run in parallel write in the order they end (gaps from 1 s to
  6 min). certify.py's `latest_in_front` reads it and is not enforced. This is the question below.

Checks. `test_each_evidence_form_is_refused_without_its_fields` (13 fixtures) fails at 98bb4c8 and
passes after. `test_the_theory_s_held_as_run_and_the_reader_agree` generates a test program with
one closed law per fixture the theory can state (eight of them) and checks that `heldAsRun` equals
the reader's verdict on each. Excluded are the four checks that are the reader's alone, and the
exhaustive fixture without a census, where the theory reaches the hole `enumeratedWhole`. Every
store of the tree passes `store_errors` (0 refused). Five older tests built sampled entries with no
budgets or with a binding written as a string. Their helpers `entry` and the admits test now record
budgets, and a binding that isn't a list is left to the identity's reading. The three test files:
96 passed, 2 skipped. `check_spec` prints only its known finding.

## Decisions taken on my own

1. The conjuncts come into certify through the demand (`conjuncts`) with a fallback to the stored
   listing until run.py gives them, so the fix waits on two lines of run.py.
2. `_or_weakest` and `_or_strongest` keep `None`, as the unit only, because tester.py folds with it.
   certify's own folds read `Held`.
3. `allOf` takes the demand's combination, and `projectGrade` is the projection alone. The vector of
   the conjuncts' grades (L12.5) is left to B3.
4. `refutedAsConsequence` and `_passes_theory` keep reading a model's listed conjuncts, because that
   errs toward a veto.
5. A5's conjunct goes into the specimen's key only. The theory's `stretchesUnder` keeps its gap,
   written down, so `Pooling`'s stores don't move.
6. `SAMPLED_REQUIRES` leaves out the two region budgets that older entries lack.
7. `latestInFront` and an assumed entry's demand are left out of A6, for the reasons above.

## Question

A store's entries are in the order they were written, but each one's date is when its line started,
so under parallel certification "the latest in front" by date is false of five stores of the tree.
Should the store's predicate read the order written, with the date kept as the run's start? Then
the theory drops `notBefore` and the predicate holds as `record` builds it. Or should the tester
date an entry when it writes it, after which those five stores pass only once they are
re-certified?

## Follow-up: the order written

The coordinator answered the question on 2026-10-23 with its first option: the store's predicate
reads the order written, since an append is the store's history, and an entry's date stays the
start of its run. In certification.lth I removed `notBefore` and `latestInFront`, so `Store` is
`gradedAsOutcome es and heldAsRun es`. A comment there says why no date is read. A new law,
`RecordingKeepsTheOrderWritten` (recording leaves the store as it was or puts the new entry in front
of it), is part of `Recording`. It has a line in certification_laws.test.lut and a control in
certification_controls.test.lut, `writingBehind`, a store that writes a new entry behind the others,
which is refuted. In certify.py I removed `latest_in_front` and updated `store_errors`'s docstring;
`record` already builds the order. `test_the_latest_in_front_is_the_order_written` checks that an
entry dated before the one behind it is no error. The five stores need no re-certification for
this, and the three test files pass (97 passed, 2 skipped). `Recording`'s conjunction gained a conjunct, so its cone moved: one more store entry for the
coordinator's wave. Pruning drops entries without reordering them, but `PruningOnlyDrops` checks
membership only; a law on the order it keeps waits for a case that needs it (P8).
