# Brief: `luthier eval` leaves terms over the core's `foldList` unreduced

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/report-bite-10.md` (its question: `luthier
eval` and `luthier session` don't reduce a top-level term over core's `foldList`, which blocks
differential testing of anything using `all` or `any`), `execution.md` section 1 (the core as a
prelude) and bite 13's paragraph of 2026-10-21, and the spec chapters on evaluation that
`docs/spec/00-index.md` points to.

Find why, and fix it if the fix is the evaluator's or the loader's:
1. Reproduce with a minimal file: `all`, `any`, `size` or `map` of a literal list, through `luthier
   eval` and `luthier session`, and the same term inside a test program through `luthier test`
   (which does reduce it, per bite 10's tests). Record each command and its output.
2. Find the cause (the prelude not loaded into eval's environment, `foldList` treated as opaque, a
   primitive missing at the top level, or something else) and say where in the code.
3. If the cause is a defect, fix it with a test that fails before and passes after. If it is
   intended by a spec clause, quote the clause and stop: that is the answer to bite 10's question.

Bite 11's agent works in arrays, tables and elaborate.py's alias handling, and runs the suite;
another agent writes docs/concepts.md. If your fix needs elaborate.py, keep to your own hunks and
stage only them. Run everything with `/home/lmoffatt/miniconda3/bin/python` and
`/home/lmoffatt/miniconda3/bin/luthier`.

Accepted when: the reproduction is written in the report; if fixed, the new test passes and
`python -m pytest -q tests/test_run.py tests/test_elaborate.py tests/test_check.py` passes or every
failure left is shown to fail the same way without your change. Small commits staged by path: a
subject, a blank line, one body line, ending with "Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>". Report: `record/plan/core-2026-10-17/report-eval-foldlist.md`, committed:
the reproduction, the cause, the fix or the clause, the checks' output, decisions taken on your own,
at most one question.
