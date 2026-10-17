# Report: three kinds of file (step 3g, D-2026-10-16-e)

Written 2026-10-17 by Claude Opus 5.5, an agent of the coordinating session, on
record/IA/code-follows-2026-10-16/prompt-file-kinds.md, from 6b23408. Commits: 6c9be06 (stores),
01e5d93 (renames), 472bc98 (references and splits), 812a262 (code and tests), 398d6a9 (spec), and
the one that adds this report.

## What was built

The rule of D-2026-10-16-e, with the coordinator's finding on 01e5d93 (the record of x.run.lut was
x.run.run.json) folded in.

- `run.py`: `file_kind` (the kind a name declares: run, test, theory, model), `base_name` (x for
  x.run.lut, x.test.lut, x.lut, x.lth), `executive_import` and `require_kind`. `record_path` and
  `results_path` use the base name, so x.run.lut keeps x.run.json and x.results.json beside it.
  The loader (`Loaded.visit`) refuses an import of an executive file when a run or a test reads it.
  `run()` refuses a file that is not a .run.lut before reading anything.
- `tester.run_tests` refuses a file that is not a .test.lut; `luthier test` says so naming itself;
  `certify` refuses the whole command, before any line runs, when one file given is not a
  .test.lut. `--prune` runs nothing and is left as it was.
- `check.py`'s `kinds` (rule 12.R2), called by `check` when it has the file's path: an import of an
  executive file from any file; a `test` line or a `main` in a .lut or .lth; a .run.lut without
  `main`; a .test.lut without `test` lines; and, as a proposal of mine, a `test` line in a .run.lut
  and a `main` in a .test.lut. Each message names the file, its kind and the rule, for example
  `12.R2 import: user.run.lut imports lib.run.lut, a run (.run.lut): an executive file is never
  imported (12.R2, D-2026-10-16-e); what it shares belongs in a .lut`.
- Messages of the commands: "`luthier run` takes a .run.lut file (12.R2, D-2026-10-16-e);
  laws.test.lut is a test program (.test.lut, for `luthier certify`)", and the converse for
  `certify` and `test`.
- Tests: 13 programs `tests/spec/kind_*` (3 accept, 10 reject; the runner now reads the kind from
  the suffix after the verdict, `x.reject.run.lut`, and `scripts/check_spec.py` accepts it), and
  `tests/test_file_kinds.py` (9 tests: the suffixes and base names; `run` on a .test.lut, .lut and
  .lth refused; `certify` and `test` on a .run.lut refused, nothing written; certify refused whole;
  a .run.lut imported by another file refused at load and by the checker, the control; a .test.lut
  imported refused; a run of x.run.lut writes x.run.json and x.results.json and nothing named
  x.run.run.json; a test program writes nothing beside itself, its entry in the model's store).
- Spec: 12.R2 (the three kinds and the refusals, with its Files line) and 12.S24 (local names,
  records beside the run, certificates beside the claim), 7.S21 (test lines live in a test
  program), all `[implemented]`; 12.S10, S15 to S18 and S23 aligned (S23's "what no file imports
  (a `main`, a local helper) may live whole in a `.lut`" now sends those demands to 12.R2). 12.S17
  said `--entry`; the flag is `--main`, corrected.

## Renames (git mv, commit 01e5d93, no content change)

- tests/tester: every `X.lut` to `X.test.lut`: the 15 `*_laws`, the 15 `*_controls`, and `laws`,
  `cases`, `weakest` (pytest fixtures with test lines).
- tests/run: every program with a `main` to `.run.lut`: callbacks, checked, connective_on_match,
  extern_arity, extern_partial, first_action_honest, first_action_liar, first_action_noisy, holes,
  host_cell_under_operator, host_function, matrix_product, maximize_quadratic, maximize_shared,
  numbers, observe, plan_cone, plot_two_tables, print_twice, read_first_line, read_once,
  record_externs, record_of_functions, table_cell, table_names, vector_norm,
  certified/provisional, certified/uses_small, scope/label_and_definition, scope/main,
  scope/missing_import, scope/unlisted. Kept as libraries: first_action_models, scope/left,
  scope/right, certified/small.
- examples/hello.lut to examples/hello.run.lut (its record hello.run.json now pairs with it).
- tests/spec: r12_block.accept.lut, cite_proved.accept.lut, cite_not_reference.reject.lut to
  `.accept.run.lut` / `.reject.run.lut` (each holds a `main`); Files lines of chapters 2, 4, 6, 12
  and tests/test_spec.py follow.

Splits and new files (472bc98):

- examples/sonolocalizacion/experiment_zero.lut stays the model (the fit, the transform, the
  tables, the report, `writeTable`, `bandHalfWidth`); experiment_zero.run.lut is new: the holes,
  `runSettings`, the figure parameters, `writeReport`, `runOn`, `runWith`, `main`,
  `priorWidened`, `sigmaKnown`. The definitions are unchanged.
- validate_graph.lut stays the model (`rankFloor`, `summary`, `report`); validate_graph.run.lut is
  new (`graphDir`, `main`).
- tests/run/certified/small.lut keeps the theory and its two models; small.test.lut is new, with
  the binding and the test line.
- fit_controls imported fit_laws (`tolerance budget cutoffs`) and plot_controls imported
  plot_laws (the plots and censuses). Those now live in two libraries both test programs import:
  tests/tester/fit_cutoffs.lut and tests/tester/plot_cases.lut. The censuses of models (`drawings`,
  `stores`) stay in plot_laws.test.lut.

References updated in tests, docs (guide, spec 2, 3, 4, 6, 7, 10, 12), src/luthier/lib comments,
examples headers, README's command list. The record was left as it is: no current plan quotes a
command for future use with an old name (the mentions are status lines of past steps).

## Checks

- `python -m pytest -q` at 398d6a9: 781 passed, 6 skipped, 9 xfailed in 418 s (before: 759 passed,
  6 skipped, 9 xfailed; the 22 more are the 13 kind programs of tests/spec and the 9 tests of
  tests/test_file_kinds.py).
- `python3 scripts/check_spec.py`: its known finding, `docs/spec/03-kernel.md:190: check-spec:
  shares a run of 10 words with docs/principles.md: "only through the bridge and never reduced by
  the kernel"`, and `185 implemented, 80 decided (of which 33 suspended), 8 proposed`.
- `python3 scripts/project_principles.py --check`: `lints: 0 unresolved references, 0 repeated
  sentences`, `ok`.
- `luthier certify --jobs 3` over the 30 files `tests/tester/*_laws.test.lut` and
  `*_controls.test.lut`: every file "0 lines ran", every line known (52, 15, 7, 4, 11, 7, 51, 12,
  13, 8, 2, 36, 6, 8, 24 known for the laws in alphabetical order, arrays to world; 35, 8, 4, 4, 6,
  8, 42, 7, 11, 8, 2, 18, 6, 8, 18 for the controls), the md5 of all 27 stores identical before and
  after. The output is the baseline's at 6b23408 line for line, but for two demand laws whose stale
  control entries were replaced (see below). Exit 1, as at the baseline: tables' `CellsOfTheirKind`
  is refuted, and five laws are uncontrolled (ANewIdentityGoesInFront, AnAgreeingReplayAddsNothing,
  AnAgreeingPairSettles, KeyReadsOnlyTheCone, KeyReadsTheType), both as before.
- The three pytest fixtures `laws.test.lut`, `cases.test.lut`, `weakest.test.lut` are not in that
  list: they were never certified, their lines ran and wrote stores (beside themselves for their
  own laws, and numbers' stores for `cases`). I removed what that run wrote; they are exercised by
  pytest only.
- The sonolocalización run, as its last record (2026-10-15T00:59:42) set it:
  `luthier run examples/sonolocalizacion/experiment_zero.run.lut --set
  graphDir=examples/sonolocalizacion/A/graph_noA2 --set outDir=<scratchpad> --set lmMaxIter=500
  --set lmTol=1e-06 --set lmFloor=5.995204332975845e-15 --time-limit 30`. Accepted as a .run.lut,
  past the certification check: it was cut while evaluating, "time limit of 30 s reached after
  2465792 steps (run --time-limit)", exit 1, nothing on standard output. The record shows nothing
  of it: experiment_zero.run.json had 23 entries before and after, the last still the run of
  2026-10-15T00:59:42; a run cut by its limit writes no record (see the question).
- validate_graph.run.lut on session A's graph gives the expected line in under 20 s, and
  hello.run.lut prints `hello, world`. Those two checks of mine wrote run entries, two locks and
  first-action entries in world_model.cert.json; I removed all of it, so nothing of them is left.

## Before the migration (6c9be06)

At 6b23408 `luthier certify` over the law and control files ran 2 lines of demand_laws.lut and 2
of demand_controls.lut: `NoPriceRefusesAssumed` and `LoweringLosesNothing` and their controls were
stale (the fingerprint of the census `anyPassModels` had changed with the pooling work). Their new
entries replaced the old ones in demand.cert.json and certification_model.cert.json; a second run
had every line known. I committed those two stores apart, so that the migration's check starts from
a state where every line is known.

## Decisions I took on my own

1. A "demand" in a .lut or .lth is read as a definition or declaration of `main`, the entry of a
   run. No other form of demand exists in a file today.
2. Each executive file carries only its own demand: a `test` line in a .run.lut and a `main` in a
   .test.lut are refused too. Marked [proposed] in 12.R2; one commit undoes it.
3. The kind is required by the functions (`run.run`, `tester.run_tests`), not only by the CLI, so
   every temporary program of the suite that is run or tested now has its suffix.
4. `certify` given one file of another kind runs nothing at all, rather than the files that are
   right.
5. What a law file and its control file share goes into a library both import (fit_cutoffs.lut,
   plot_cases.lut) rather than being copied, as pooling_controls had done (L2.8, nothing said
   twice).
6. In the splits the model keeps the original path, so its history follows the library; the run
   files are new.
7. The tests/run programs stay whole as runs with local names; only small.lut is split, since
   another file imports it.
8. `store_path` is unchanged: a test program that states its own laws (only the suite's fixtures
   do) keeps `x.test.cert.json` beside it. Written as [proposed] in 12.S24.
9. The spec programs keep the verdict before the kind (`x.reject.run.lut`); the spec runner and
   check_spec read both.

## Question

A run cut by its time limit or its fuel leaves no entry in x.run.json, so the experiment_zero
check above left no trace, and a cut run of Luciano's would leave none either. Should a cut run be
recorded, with its demand and the step it stopped at, as a run that did not finish (P2: everything
derived carries how it was derived)?
