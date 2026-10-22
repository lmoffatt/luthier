# Report: the combined verification after the core's bites 6 to 11

Agent: Claude Sonnet 5.5, brief `prompt-verify-6-11.md`, 2026-10-22. Outputs under
`~/.cache/luthier-verify/` (not versioned): `pass1/`, `pass2/` (one log per program), `pytest/`
(one log per test file), `run_pass.sh`, `run_pytest.sh`.

## Commands

- Certify, per area (laws, then controls, then the plain program), four areas in parallel, each
  program its own process: `/home/lmoffatt/miniconda3/bin/luthier certify --jobs 1 tests/tester/X.test.lut`
  for the 40 `tests/tester/*.test.lut` (script `run_pass.sh N`). The fixtures `core_instances.lut`,
  `fit_cutoffs.lut`, `plot_cases.lut` are not test programs and are not run.
- Suite: `/home/lmoffatt/miniconda3/bin/python -m pytest -v -p no:cacheprovider tests/test_X.py`, one
  file at a time under `timeout 1800` (`run_pytest.sh`; pytest-timeout is not installed).
- `luthier run` of the two examples, with the `--set` values of their headers.

## Counts

Before: the stores were stale (bite reports: 45+ test_run failures, 59 in bite 11's full suite).
After pass 1 (the stores were already written by the killed first wave) and pass 2: every one of
the 40 programs prints `0 lines ran`, all known (pass2/*.log). Exit 1 only for `cases.test.lut` and
`laws.test.lut` (fixtures that refute on purpose: AndIsOr, Small, RootIsNotNegative) and
`belief_laws.test.lut` (below).

Pytest, 42 files: every file passes (about 1,000 tests; 0 failed). `test_check_private.py` collects 0
tests (rc 5, not a failure). `test_certify.py`: 56 passed, 1 skipped with the regions test
deselected; that one test did not finish (below). `test_run.py::test_bootstrap_primitives_and_not`
passes. `test_validate_graph_slow` and the other LUTHIER_SLOW tests are skipped by their own marker
(they would fail: see the doubles refusal).

Stores committed: a0342be (library, with the three new core/ stores), 5079f83 (tests/tester),
49582e5 (examples/sonolocalizacion).

## Failures and open points

1. test_certify's `test_the_regions_hold_on_the_references_and_their_controls_refute_the_broken_ones`
   did not finish in 25 minutes of CPU (96% of one core, no lock wait, no I/O). It is slow, not
   looping: `tester.run_tests` on regions_laws.test.lut and regions_controls.test.lut runs every line
   without a store (270 to 405 exhaustive cases per line); one line alone
   (`TheThreeSourcesGrade`, 270 cases) took 4m15 at HEAD with `certify --no-cert`, about 1 s a case,
   and the file has several such lines plus their controls. `luthier test` over the same file
   with the store takes 9 s. Owner: regions' tests are bite 5's (record/IA/regions-2026-10-17); the
   cost per case is the elaborated certification model's, which bites 9 (certification and test.lth on
   the core's folds, 8ef6389) and 10 touched; bite 8's report saw the same test cut at its 10 minutes,
   so it was slow before bite 9. I did not bisect the per-case cost (the old file has other laws).
   For the coordinator: run the test through the store, or mark it slow.
2. `examples/sonolocalizacion/validate_graph.run.lut` and `experiment_zero.run.lut` are refused,
   both for the same four lines: `doubles: Neutral / Absorbing / Involutive / TotalOrder: uncertified
   (no entry)`. Cause, read in certify.py (`served`, `refuse`): numbers.lth's `Doubles` claim is a
   conjunction of the core's properties (`Neutral Float64 ... d.plus 0.0`, ...), and its entries in
   numbers.cert.json are stored under law `Doubles` with `conjunct` = the full applied text, passed,
   sampled, controlled. The cone of `doubles` demands the laws by the bare property names `Neutral`,
   `Absorbing`, `Involutive`, `TotalOrder`; `served` finds no entry of law `Neutral`, so the
   conjunct fallback does not apply. `Commutative` (also a conjunct) is not refused. Not mechanical:
   it is the elaboration of a claim's conjuncts into demands (D-2026-10-18-f), the cone side against the
   entry side. Owner: bite 8 (Doubles as a conjunction of core properties; present already at 7180f7b
   per bite 11's report) and bite 6 (ranges). validate_graph therefore does not reproduce its record
   (valid: 10 nodes, 22 measurements, 21 distinct pairs; ...); it is refused before running.
3. experiment_zero: `luthier check` fails with three 4.R2 (lines 90, 91, 94: `main`, `priorWidened`,
   `sigmaKnown`, a name they mention does not exist): the known failure, bite 13's. Its run is
   refused for the doubles as above (and `lmTol`, `lmMaxIter`, `lmFloor` must be set).
4. `belief_laws.test.lut` exits 1: `PrecisionSymmetric: not run: no generator of
   (PrecisionSymmetric 2) & (DensityPeaksAtMean 2)`, the plain sampled line, controlled and refuted.
   Not new: record/IA/evidence-2026-10-14/report.md:39 records the same ("drawn: no generator of
   GaussianBelief, 7.R4"); belief.lth and the test file have not changed since 2026-10-16
   (c2a7b4e, 472bc98).
5. The coordinator's sighting of a hang at tests 55-56 of the first full run did not recur when the
   files ran one at a time: test_certify's other 56 tests pass in 4 minutes. Its cause was the regions
   test (point 1) in the same file.

## Decisions taken on my own

- Stores committed in three commits by area, as the brief says; `tests/run/luthier.lock`,
  `time_opus_low.txt` and `record/IA/...` left untracked.
- test_certify run with the regions test deselected to see the rest of the file; no test or source
  file changed.
- `luthier run` of the examples done in the tree: it wrote no record (both refused); the files
  `*.run.json` are unchanged.

## Question

Should the regions test run through the store (seconds) or be marked slow like `test_validate_graph_slow`
(LUTHIER_SLOW), given it recomputes about 1,500 exhaustive cases at 1 s each?
