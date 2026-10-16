# Report: a certificate lives only beside the file that makes the claim (step 3b)

Brief: `record/IA/code-follows-2026-10-16/prompt-claim-store.md`. Written 2026-10-16 by Claude Opus
5.5, an agent of the coordinating session. Sources: D-2026-10-16-b (item 7), L10.12, L2.8, 12.S11.

## What was built

`tester.claim_file` gives, for each test line, the file that makes the claim its entry certifies:
the file that defines the model of the library the line's binding names (`model_homes`), or, when
it names none, the file that states the law (`law_file`; a control file that names a law it does
not import finds it through the loader). `run_tests` looks each line up in that file's store and
writes its entry there under the lock (`certify.add_entry`); the test program's own store is
neither read nor written. Controls follow the same rule: a control on a model the test program
breaks lands in the store of the file that states the law (`arrays.lth` for `arrays_controls.lut`).

`certify` and `check -v` read the stores of the claims of the lines (`certify.read_stores`,
`tester.line_claims`); control status reads the control entries in the claims' stores of every
file given, each entry once. `run.py` is unchanged: a run reads the stores of the files it loads,
and the claims' files are among them.

Commits: 5bf4372 (code and tests), 07abbe9 and 9bcdf05 (`scripts/fold_claim_stores.py`), 38dd3c5
(the fold), 172b057 (a test that compared the stores beside the tables programs).

## The fold

`scripts/fold_claim_stores.py --write` at 9bcdf05, with `LUTHIER_LIBRARY_STORES` unset. It matches
each entry to a current test line (by law, binding without fingerprints and kind: 423; by law and
kind: 24), else computes the claim from the entry's own binding (14 entries of lines changed
since), and stops on anything unresolved. Nothing is pruned. The input stores and the sha256 of
their bytes are printed by the script.

- Before: 469 entries in 26 stores beside test programs (`tests/tester/*_laws`, `*_controls`).
  Claims' stores before: 313 entries.
- After: 250 moved into the claims' stores, 207 already there (the night's copy), 4 kept, 8
  archived; 469 accounted for. An independent check found all 469 identities in a store after
  the fold, and none of the 313 lost. Stores after: 575 entries (313 + 250 + 4 + 8).
- 24 stores removed. They were untracked (`.gitignore` has `*.cert.json`), so `git rm` did not
  apply: they were deleted, their entries kept in the claims' stores.
- Kept: `tests/tester/fit_laws.cert.json` (4 control entries of the wrappers `fit_laws.lut`
  states) and `tests/tester/sonolocalizacion_laws.cert.json` (6 entries of `LayoutFromUndoesTo`
  and `LayoutToUndoesFrom`, laws that file states with no model of the library in the binding).
- Archived: 8 entries of laws no file defines any longer (the `...OnBroken` wrappers removed
  from `generators_controls.lut` at e90e4fe, `SkewedSampleIsUniform`, `UniformAtLevel`) in
  `record/archive/stores-2026-10-16/`, beside no program, read by nothing.
- New stores beside theories in the library: `arrays`, `belief`, `demand`, `laws`, `numbers`,
  `optimization`, `plan`, `plot`, `probability`, `tables`, `world` (`.cert.json`), tracked.

## Acceptance

- `python -m pytest -q`: 735 passed, 5 skipped, 9 xfailed, 4 failed. The 4 failures are
  `tests/test_check_spec.py` and come from 6c08c32 (the other agent's `check_spec` now prints
  counts the tests do not expect); they fail on HEAD without these changes. The baseline 737 plus
  my 2 new tests is 739 = 735 + 4.
- `luthier certify tests/tester/arrays_laws.lut`: `35 laws, 0 lines ran, 52 known`, exit 0; no
  library store changed (md5 before and after), no `arrays_laws.cert.json` written. With
  `arrays_controls.lut` too: `0 lines ran, 35 known`, every law controlled.
- New tests (`tests/test_certify.py`): a law certified from `small_test.lut` is found by a run
  of a program that imports only `small_model.lut`, and no store appears beside the test program
  after `certify`; the control: the same entry moved by hand beside the test program is read by
  neither `standings`, nor the run (refused, uncertified), nor `run_tests` (the line runs again).

## Spec sentences to change (not edited: another agent holds the spec)

12.S10, first sentences. Now: "What `luthier test x.lut` writes. [implemented] The file
`x.cert.json`." Proposed: "What `luthier test` and `luthier certify` write. [implemented] Each
entry goes into the store `y.cert.json` of the file `y` that makes the claim it certifies: the
file that defines the model of the library the line's binding names, or, when it names none, the
file that states the law (L10.12, D-2026-10-16-b). A test program, which only gathers evidence,
keeps no store; a control's entry follows the same rule." The rest unchanged.

12.S11, first sentence. Now: "When a file is imported its certificate is read." Proposed: "When a
file is loaded, by a run or as the claim of a test line, its store is read; a store beside a test
program is read by nothing." The rest unchanged.

6.S6, the [implemented] sentence: "an entry of `x.cert.json` (spec 12.S10)" could read "an entry
of the store of the file that makes the claim (spec 12.S10)". Optional.

## Decisions taken on my own

1. A wrapper law the test program states, bound to a model of the library, goes to the model's
   store (`model_homes` no longer excludes it). Before, it stayed beside the test program.
2. A test program that states a law with no model of the library in its binding is that law's
   claim and keeps a store for it (`fit_laws`, `sonolocalizacion_laws`).
3. A binding naming models of several files: the file that imports the others, else the first.
   Nothing is written into two stores.
4. Control status reads the control entries in the claims' stores; so `check -v laws.lut` alone
   now reports a law controlled when its control's entry sits in the law's store (a test changed
   accordingly).
5. The fold never prunes; stale entries are moved as they are.
6. The 8 entries of removed laws archived in `record/archive/stores-2026-10-16/` (added with
   `git add -f`).
7. `run.py` untouched: a program that imported a test program would still read a store beside
   it. No such program exists.
8. The v0.1 stores in `examples/` (`cauchy`, `exp`, `kernel_finite`, `z7ring`, old format, no
   program beside them) left alone.

Finding, not acted on: 61 identities sit in more than one store (mostly `session_a`,
`distances` and `belief_model`), copies the night's copy wrote under earlier rules of
`model_homes`. L10.12 says no entry is written in two partitions; cleaning them is a fold over the
claims' stores, not asked here.

## Question

Two test programs still keep a store because they state laws: `fit_laws.lut` (the controls of its
`...OnQuadratic` wrappers) and `sonolocalizacion_laws.lut` (`LayoutFromUndoesTo`,
`LayoutToUndoesFrom`). Move those laws into the files they are about (the wrappers into
`optimization.lth`, the layout laws into `examples/sonolocalizacion/distance_graph.lut`), so that
no test program keeps one? I'd do it: it costs two small edits and the store rule then has no
exception.

## Follow-up (the coordinator's four items, 2026-10-16)

### 1. No test program states a law any longer

- The three `...OnQuadratic` wrappers moved from `tests/tester/fit_laws.lut` to `optimization.lth`.
  `MaximizersAgree` went to `belief.lth`, since it's a law about `Maximizer`, which `belief.lth`
  states.
- `nativeLM` moved to `session_a.lut`. Left in `fit_laws.lut`, it would have made that test
  program the claim of `MaximizersAgree`'s control.
- `LayoutFromUndoesTo` and `LayoutToUndoesFrom` went to `examples/sonolocalizacion/positions.lut`,
  where `layout` is defined (L2.8). The instruction said `distance_graph.lut`, which I had
  suggested by mistake: that file doesn't define the layout.
- None of the moved laws joins its theory's conjunction (`LMStep :=`, `Maximizer :=`), so what a
  run demands is unchanged.
- `tests/tester/session_a.lut` moved to `examples/sonolocalizacion/session_a.lut`. It's a file of
  session A's models with no test lines, and its store would have been one more `*.cert.json`
  beside a `tests/tester/*.lut`. Its ten importers follow the new path.
- The moves left every cone hash as it was. `luthier certify` on `fit_laws`, `fit_controls`,
  `sonolocalizacion_laws` and `sonolocalizacion_controls` gave `0 lines ran` and every line known
  (11, 6, 6, 6), with no law reported uncontrolled.

Commits: a0de6db (the move of `session_a.lut`), b92069f (the laws).

### 2. The second fold

`scripts/refold_claim_stores.py --write` at 3f37bcd went over every store in `src/luthier/lib`,
`examples` and `tests/tester`. It assigns each entry its claim through the current lines of every
test program, the same tiers as the first fold, and in tier 4 it uses the program that sees the
entry's censuses.

- **Before:** 567 entries in 27 stores, 469 identities. That's 98 copies, the 61 identities that
  sat in more than one store.
- **After:** 468 entries in 26 stores, one per identity. One more identity, a copy of
  `UniformAtLevel` in `probability_model.cert.json`, was dropped because the archive of removed
  laws already holds it. Lost: 0.
- **Moved with their claims:** `fit_laws.cert.json` and `sonolocalizacion_laws.cert.json` (4 and
  6 entries) are gone. Their entries went to `optimization.cert.json`, `session_a.cert.json` and
  the new `positions.cert.json`.
- **Left in place:** the 7 entries a run wrote at a first action (`FirstAction`, 10.S10) stay where
  the run put them.
- No `*.cert.json` is left beside any `tests/tester/*.lut`.

Commits: 3f37bcd (the script), cd01b1f (its write).

### 3. The spec

I applied the wording proposed above to 12.S10, 12.S11 and 6.S6. Two stale sentences changed:

- 12.S17 now ends "Today `run` refuses by default, and `--require-certified` no longer exists."
  The flag is gone from `cli.py`.
- 10.S7 now ends "world.lth's `HostChangesOnlyDeclared` states it, and `run` checks it at an
  action's first application (10.S10)."

Statuses are unchanged. `python3 scripts/check_spec.py` gives the single finding at
`03-kernel.md:190`. Commit: 06b7c0b.

### 4. .gitignore

The `*.cert.json` line wasn't needed any more, and it did harm: the claims' stores in
`examples/sonolocalizacion/` (`distances`, `distance_graph`, `session_a`, `positions`) were
untracked. I removed it, along with its negation for the library. `*.cert.json.lock` stays
ignored.

Two sets of old stores became visible as a result, and I archived and tracked them:

- the four v0.1 stores left in `examples/` (`cauchy`, `exp`, `kernel_finite`, `z7ring`), which
  had no program beside them. They're now in `record/archive/stores-2026-10-16/v0.1-examples/`.
- the stores under `record/archive/examples-2026-10-04/`, untracked until now.

The test suite only writes copies of the library's stores (`LUTHIER_LIBRARY_STORES`), and after a
full run `git status` showed no store changed. A `luthier certify` or `luthier run` now leaves its
writes to the stores in `examples/` visible in `git status`, as it already did for the library's.
Commit: 340214b.

### Suite

`python -m pytest -q`: 741 passed, 5 skipped, 9 xfailed. That includes `tests/test_check_spec.py`,
which passes since the other agent's ada16e0.

### Decisions taken on my own in the follow-up

1. `session_a.lut` moved to `examples/sonolocalizacion/`.
2. `nativeLM` moved to `session_a.lut`.
3. `MaximizersAgree` went to `belief.lth` and the layout laws to `positions.lut`. Both differ from
   the instruction, and the reason is the same: L2.8 puts a law with the definition it is about.
4. The moved laws stay out of their theories' conjunctions.
5. The refold leaves first-action entries in place, drops a copy the archive already holds, and in
   tier 4 picks the program that sees the entry's censuses.
6. Old stores in `examples/` and `record/archive/examples-2026-10-04/` are archived and tracked
   (P3).
