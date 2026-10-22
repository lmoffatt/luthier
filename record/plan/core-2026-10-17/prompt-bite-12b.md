# Brief: the core's bite 12b, probability, belief, optimization, plot and the examples

Bite 12 of `execution.md` section 6 is split in two (the coordinator, 2026-10-22): 12a
(`prompt-bite-12a.md`) fixes the elaborator, the tester and certify, by another agent at the same
time in src/luthier/*.py and tests/test_*.py; 12b, here, the library and the examples.

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md`: the Status of 2026-10-21,
sections 0 to 5 and 6 (bite 12 with all its "Also" paragraphs); the reports `report-bite-7.md` to
`report-bite-11.md` and `report-verify-6-11.md` beside it; `record/decisions.md` at
D-2026-10-17-g and -h, D-2026-10-18-b, -f, -j, D-2026-10-21-a. Read the observations on these files
in `record/Lucianos observations/` before changing them.

Build bite 12's files as section 6 lists them (probability, belief, optimization, plot, their
models and test programs; positions.lut, distances.lut, figures.lut, distance_graph.lut;
algebra.lth's `Iso` alias), on the core's names, plus:
- `Doubles (F : U)` claimed at `Float64` (bite 12's "Also" on report-bite-8.md), the examples'
  `doubles : Doubles` becoming `Doubles Float64`.
- The "bound too small" control for arrays.lth's six summing laws (`gamma n` for `3 gamma n` on the
  real doubles), as numbers.lth has.
- Where `size` doesn't resolve at `Mat Float64` or `Table`, list the uses in the examples left on
  the old helpers.
A bound is the theory's, never tuned to pass; a refuted law is a finding with its counterexample.

Order: do the source work first, committing as you go. Then wait for 12a: its report
`report-bite-12a.md` committed is the signal (check `git log` between steps). Only after it,
re-certify every store with `/home/lmoffatt/miniconda3/bin/luthier certify`, program by program
(a loop, each with its own log under ~/.cache/luthier-12b/, not /tmp, which is wiped on reboot),
twice: the second pass prints 0 lines ran for every non-fixture program. Then run
validate_graph.run.lut and experiment_zero.run.lut and compare with their `*.run.json` records
(a changed cone is a changed key: redo the runs and compare the values with the recorded ones).

Don't edit src/luthier/*.py, tests/test_*.py or docs/spec/ (12a's). Run everything with
`/home/lmoffatt/miniconda3/bin/python`. For long runs, start them detached with their output under
~/.cache/luthier-12b/ and wait in the foreground with bounded waits (`timeout 540 bash -c 'until
[ -e DONE ]; do sleep 20; done'`, repeated); don't hand back while they run. Small commits staged
by path, never `git add -A`: subject, blank line, one body line, ending with "Co-Authored-By:
Claude Opus 5.5 <noreply@anthropic.com>".

Accepted when: section 6's criteria for bite 12 (the examples' stores re-certified;
experiment_zero and validate_graph reproduce their records; core_metrics' counts (1) to (3) at 0
or each one left named with its reason); the full suite, run file by file under `timeout 1800`
with outputs under ~/.cache/luthier-12b/, passes or each failure left is named with its cause;
`python scripts/check_spec.py` prints only its known finding. Report:
`record/plan/core-2026-10-17/report-bite-12b.md`, committed: what you built, the checks, the runs
against their records, core_metrics before and after, decisions taken on your own, at most one
question.
