# Report: the core's bite 13c, the certification defects the audit found

Brief: `record/plan/core-2026-10-17/prompt-bite-13c.md` (c9cc615). Audit:
`record/plan/audit-algebras-2026-10-22/report.md` (5b1a05e), part I and 3.1. Agent: Claude Opus 5.5,
2026-10-22. Python: `/home/lmoffatt/miniconda3/bin/python`. Scratch: `~/.cache/luthier-13c/`.
Every item was checked against the tree at c9cc615 before it was fixed; each has a test that fails
on the commit before its fix and passes after (checked by putting the earlier `certify.py` and
`run.py` back and running the new tests).

## Per item

**1. Retention erases a refutation (audit 1.4 A).** Confirmed. `prune` kept the four latest current
entries of a group and protected only the two entries of a disagreement, so a failure followed by
four passes was dropped and the law got `Sampled` back. The same held for a control whose broken
model came out confirmed (the control failed): four refutations after it dropped it and the law read
as controlled. Fix (820f0e3): `prune` never drops a current failure or a current confirmed control
(`_negative`); a stale one still goes once a current entry exists, since only a current refutation
refuses (6.S15). Tests: `test_pruning_keeps_a_current_failure_so_passes_never_restore_the_grade`,
`test_pruning_keeps_a_confirmed_control`.

**2. Distribution-changing budgets outside identity (audit 1.4 B).** Confirmed: `identity` read
none of `budgets`, so a run of one seed under `specialMass` 0.45 was absorbed as a replay of the one
under 0.05, and the two pooled as one sample. Fix (aea4c26, tests 1910630): `certify.SAMPLING` and `certify.LIMITS`
classify the thirteen fields of `Budgets`; `sampling(entry)` enters `identity` and `union_key` (so
`stretches`, `pooled`, `pools` and `continuation`). In the identity: `specialMass`, `atomAtZero`,
`coveringAbove` (which cases a covering array picks), `levelRuns`, `seedsPerControl`,
`distributionDraws` (they size a sample, as `n` does) and the classifier's `regionNumbers` and
`regionEntries` (what the regions read). Out: `fuel`, `tries` (a value found within fewer tries is
the same value), `redraws`, `probes`, `drawsPerCase`. Spec 7.S8 says so, marked [proposed] as the
coordinator's reading of D-2026-10-16-g. Test:
`test_the_budgets_that_change_the_distribution_are_in_the_identity`.

**3. `byModel` skips the vetoes (audit 1.5 A).** Confirmed: `refuse` sent a `byModel` demand to
`served` and `continue`d, so a pass and a failure of the theory's conjunct on the run's model, two
seeds, were accepted. The same gap held for a direct demand served through its theory's conjuncts
when no entry of the law itself served. Fix (97a9527): `certify.veto(demand, entries)` reads a
disagreement, then a failure, once over every subject the demand resolves to: the law's own entries
(not for `byModel`), and, when the demand carries its theory's conjunction, the theory's entries
about the run's model (reach holds the model) for the conjuncts the law stands for (`_obligations`).
`refuse` applies it before any route serves. Test:
`test_a_law_served_through_its_theory_s_conjuncts_is_refused_by_their_failure` (also: a failure of
another conjunct, or on another model, refuses nothing; a disagreement refuses).

**4. Acceptance and recording select different evidence (audit 1.5 B, 3.1).** Confirmed on a real
run: certifying `Ops` (three conjuncts) and running on `ops`, the record listed only the
`RightNeutral` entry, for all three demands. Fix (97a9527): `certify.witness(demand, entries)`
returns one entry per obligation (the law; each conjunct; or the theory's conjuncts it stands for),
or None. `served` is `witness(...) is not None`, and `run.py` records the union of the witnesses as
`certificates`, which is what `result_key` hashes, so admission and the key read the same set (L5.6,
8.S8). Spec 7.S22 carries the rule [proposed]. Tests:
`test_the_witness_of_a_demand_covers_every_obligation`,
`test_a_run_records_the_entry_of_every_conjunct_that_served_it`.

**5. The reader accepts what `Store` forbids (audit summary item 5, section 1.8).** Confirmed for
`admits`: Drawn points graded `Proved` passed `store_errors`. Fix (bf3bc61, fixtures 4ec03c1):
`store_errors` checks `admits` (`ADMITTED`, from test.lth's `grade`) and `censusOfAtMost` for passes
over listed cases (`held_as_listed`). The audit is right on its probe, but the theory's census is
stricter than what the tester correctly writes, so a literal reader would refuse 52 entries in 7
stores (core, lists, arrays, certification_model, plan_model, distance_graph, core_instances). Two
readings the theory does not state, taken here [proposed]: a parameter enumerated whole
(`ExhaustiveMode`) reaches `Support`; a pass that evaluated no case (`EmptyIsInitial`, `x : Empty`)
bounds no census. `latestInFront` stays unchecked, as in the theory (`notBefore` is a hole). With
these, every store in the tree passes. Tests: `test_the_store_reader_refuses_a_grade_the_evidence_does_not_admit`,
`test_the_store_reader_bounds_a_listed_pass_by_its_cases`.

## Checks

`python -m pytest -q tests/test_certify.py tests/test_run.py tests/test_tester.py tests/test_check.py`
on 1910630 with 13b's working tree beside it: 55 failed, 279 passed, 6 skipped, 2 xfailed on the
first run (10 min). Three were mine (pooling tests that keyed a union by the bare binding); fixed in
1910630, now passing. The other 52 fail identically with `certify.py` and `run.py` of c9cc615 (a
copy of the package under `~/.cache/luthier-13c/base`, prepended to `PYTHONPATH`, same tests, same
moment), so none comes from this bite. They are, by cause: stale stores, mostly `console`'s four
laws (`PrintAppendsALine`, `PrintChangesOnlyStdout`, `ReadGivesThePlace`, `ReadChangesNothing`),
whose cones moved with 13b's edits of the world files, and `numpy: TraceAgrees`; then
`first_action_models.lut imports State from world_model.lut, which does not define it` (3 tests,
13b's world_model in progress); and a handful whose cause I did not chase because they fail the
same at c9cc615 (`test_the_example_plans_linearize_and_agree`, a `TimesMonotone` lookup,
`test_an_alias_or_a_constructor_is_no_model_home`). All are for 13b's re-certification or its
in-progress edits.

`python scripts/check_spec.py`: only its known finding (03-kernel.md:192 shares a run with
docs/principles.md); 187 implemented, 79 decided (33 suspended), 8 proposed.

## What moves

No stored identity moves: `identity` and `union_key` are computed on read, both sides at once, so
existing entries keep matching their replays. Real entries all record the default budgets, so no
existing pair changes status. Cones: `certification_model.lut`'s `hash` is the extern
`python:luthier.certify.cone_hash`, whose host hash is `certify.py`'s bytes, so every cone of that
file that reaches it is stale until 13b re-certifies. Refusals can be new: a run whose theory has a
current failure or disagreement of a conjunct on its model is now refused where it was accepted.

For 13b, on the Luthier side (I touched no `.lth`): `certification.lth`'s `Identity` lacks the
sampling budgets; its `censusOfAtMost` lacks the two readings of item 5; it has no law for pruning
(item 1); `certification_model`'s `refuse` has no conjunction route or witness (items 3, 4). The
specimen now says more than its theory in those four places.

## Decisions taken on my own

1. The budget classification of item 2, `tries` among the limits and the classifier's two bounds,
   `levelRuns`, `seedsPerControl` and `distributionDraws` in the identity.
2. Pruning keeps a confirmed control too, and a group may exceed four entries by its refutations.
3. The two census readings of item 5, in the reader and not the theory.
4. The conjunction-route veto also applies to a direct demand that carries its theory's
   conjunction, scoped to entries whose reach holds the run's model.
5. The direct route's failure veto is left law-wide, as before.

## Question

A direct demand (a law with a model parameter) is still refused by a failure of that law on another
model N, while a `byModel` demand is now refused only by failures on its own model. D-2026-10-22-a
says a pass on N is evidence about N only. Should a failure on N likewise refuse only runs on N
(yes: scope the direct veto by reach too), or does it refute the law for every model (no: keep it)?

## Follow-up: the direct veto scoped by reach

The coordinator answered the question above with yes (D-2026-10-22-d, ddf1160): a failure on model N
is evidence about N, as a pass is, so it refuses runs on N and not runs on another model M. There is
one exception: a failure on N of a law stated for every model of a theory, where N passes that
theory's defining laws, refutes the law as a consequence of the theory and refuses every model's run.

Done in 59da028, `certify.veto`:

- The law's own entries count only when they may be about the run's model (`_about`): for each model
  parameter of the demand, the entry's reach does not exclude the model given. An entry with no
  reach recorded for that parameter still counts, since nothing excludes it. This applies to
  disagreements as well as failures.
- The exception (`_passes_theory`): a failure of the law at its hash, on a model N its census reach
  names, refuses the demand whatever the run's model when the store has entries of the theory's law
  on N, at the theory law's hash and at a fingerprint the failure's binding recorded for N (the same
  version of N), that list conjuncts, serve every one at the demand's cutoff, and include no failure
  and no disagreement. The refusal line says why: "failed at ... on N, which passes the defining
  laws of T: L does not follow from T, so no model's run is served (D-2026-10-22-d)".
- The tester already records what tells the two cases apart (the theory's conjunct entries with
  their reach and fingerprints), so nothing was left as a stopgap refusal. The limit is the
  evidence: when the store holds no entries of the theory on N, nothing shows N is a model of it,
  and the failure stays N's. A failure whose binding recorded no fingerprint for N (or a census of
  several models under one comma-joined fingerprint that matches none of the theory's) also falls
  back to scoping.
- Spec 6.S15 carries the rule.

Tests: `test_a_failure_on_another_model_does_not_refuse_a_direct_demand` (a failure on N leaves the
run on M served; a failure on M refuses it; the run on N is refused) and
`test_a_failure_on_a_model_of_the_theory_refuses_every_model` (N passes `T` and fails `L`: the run on
M is refused with the why; when N fails `T`, or `T`'s pass is of another version of N, the run on M is
not refused). Both fail with 705138d's `certify.py` and pass with 59da028's.

Checks: `pytest -q tests/test_certify.py tests/test_run.py` run at the same moment on two copies, the
working tree (51 failed, 165 passed, 5 skipped, 2 xfailed) and the package with `certify.py` and
`run.py` of 705138d put first on `PYTHONPATH` (56 failed, 160 passed). No test fails only on the new
code. Five fail only on the old one: the two new tests, and three that are artefacts of the copy
living outside the repository (`test_interpreter_revision_is_the_last_tag`, which needs git, and two
core-collision tests in test_run.py). The 51 common failures are the ones of the first report:
stale stores (`console`'s four laws, 14 times; `numpy: TraceAgrees`) and 13b's work in progress.
`scripts/check_spec.py`: only its known finding.

Decisions taken on my own here:

1. An entry with no reach recorded for the model parameter counts against every model.
2. "The same version of N" is a shared fingerprint between the failure's binding and the theory's
   entry. N's current hash isn't known to a run on M, so its being current isn't checked.
3. The exception needs N to pass every conjunct its theory entries list, at the demand's cutoff.
4. Disagreements are scoped by reach like failures, and have no exception.
