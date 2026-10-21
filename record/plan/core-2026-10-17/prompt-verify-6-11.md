# Brief: the combined verification after the core's bites 6 to 11

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` (its Status of 2026-10-21
and section 6) and the reports `report-bite-6.md` to `report-bite-11.md` and
`report-refusal-holes.md` beside it: their Checks sections list what each left red and why.

Bites 6 to 11 landed one beside another, and each left the full suite and the full certify wave red
on stores the others made stale. Your job is to bring the tree to green and commit the stores:

1. Re-certify every store with `/home/lmoffatt/miniconda3/bin/luthier certify` (never the `luthier`
   first on PATH: its numpy gives other cones): every `tests/tester/*.test.lut` that is not a
   fixture, the library's and the examples' stores. Run it twice; the second pass must print
   0 lines ran for every non-fixture program. Known: world_model's `console:` laws (bite 9),
   numbers' `doubles: Neutral/Absorbing/Involutive/TotalOrder: uncertified` (blocks
   validate_graph), arrays' numpy stores.
2. Run the full suite with `/home/lmoffatt/miniconda3/bin/python -m pytest -q` (about 50 minutes;
   run it in the foreground or wait for it, and keep its output in your scratchpad).
3. For each failure left: if it is a stale store, re-certify it; if it is a defect, find which bite's
   change caused it (git log, the reports) and fix it only when the fix is small and mechanical
   (a count in a test, a renamed name); otherwise list it with its cause for the coordinator.
   Check `test_bootstrap_primitives_and_not` in particular (seen failing on 2026-10-20).
4. `examples/sonolocalizacion/validate_graph.run.lut` and `experiment_zero.run.lut`: run them and
   say whether they reproduce their records (experiment_zero is known to fail check, bite 13's).

Another agent investigates `luthier eval` over `foldList` and may edit run.py, elaborate.py and
test_run.py; the uncommitted hunks in those files are its, so leave them unstaged and say if a
failure comes from them. Another writes docs/concepts.md. Stage by path, never `git add -A`.
Commit the stores in a few commits grouped by area (library, tests/tester, examples), each with a
subject, a blank line, one body line naming the certify command, ending with "Co-Authored-By:
Claude Sonnet 5.5 <noreply@anthropic.com>". Leave `tests/run/luthier.lock`, `time_opus_low.txt`
and `record/IA/...` untracked files alone.

Accepted when: the second certify pass prints 0 lines ran for every non-fixture program; the full
suite passes, or every failure left is listed with its cause and the bite that owns it; the stores
committed. Report: `record/plan/core-2026-10-17/report-verify-6-11.md`, committed: the commands,
the counts before and after, each failure and what you did, decisions taken on your own, at most
one question.
