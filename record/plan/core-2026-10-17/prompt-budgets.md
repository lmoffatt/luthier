# Brief: every budget of a test is an argument of the test (7.S8, P11)

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/report-bite-1.md` (its question on fuel),
`record/IA/code-follows-2026-10-16/report-debt.md` (7.S8 pending: tester.py hard-codes 2000 and
20000), `record/decisions.md` at D-2026-10-15-g (fuel only cuts; a not-run for fuel never stored),
`docs/spec/07-tests.md` 7.S8, `src/luthier/lib/generators.lth` (`Budgets`), `test.lth`
(`defaultBudgets`), `src/luthier/tester.py`, `src/luthier/certify.py` (`FUEL`).

The coordinator's answer to bite 1's question: a test line carries its fuel in its budget, a field of
`Budgets` with its default declared in generators.lth (or test.lth's `defaultBudgets`) and recorded
with the entry; `--fuel` on certify overrides it for a run, recorded too. The same for every number
tester.py or certify.py holds as a budget today (2000, 20000, certify.FUEL = 3e6): each becomes a
declared default of `Budgets`, none stays a constant in the code. The fitA Maximizer lines get a fuel
budget of 3e7 in their test lines (MaximizerAscends spends about 2.6e7 per case), so a plain
`luthier certify` runs them.

Accepted when: `grep -n "2000\|20000\|3_000_000\|3000000" src/luthier/tester.py src/luthier/certify.py`
shows no budget constant left (say what remains and why); a test that a line's fuel budget is used
and recorded, and that `--fuel` overrides it; `luthier certify` over every `tests/tester/*.test.lut`
without `--fuel` reports every line known (the budget's fields are not in the identity, D-2026-10-15-g,
so nothing re-runs; say if that does not hold); `python -m pytest -q` passes in full (820 passed,
6 skipped, 9 xfailed before, plus yours, in the background); `python3 scripts/check_spec.py` prints
its known finding and 7.S8 goes to `[implemented]`. You are the only agent in code. Two-line commits
(subject, blank line, body) ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".
Report: `record/plan/core-2026-10-17/report-budgets.md`, by shell heredoc, committed.
