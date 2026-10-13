# check.py bite 7: Law as a verdict, walk_type, the pinned limit, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). On elaborate bite 6's report
(`record/IA/elaborate-2026-10-13/report-6.md`).

## The prompt

Read `CLAUDE.md` first, then that report, then `src/luthier/check.py` at `verdict_type`, `fits`,
`arrows`, `Typing.__init__` (line ~385), and `tests/test_check.py` at lines ~278 and ~486. Other
agents edit `run.py`, `tester.py` and their tests meanwhile: change only `src/luthier/check.py`,
`tests/test_check.py`, `tests/test_elaborate.py` (one moved test).

1. `verdict_type` accepts `Law` (laws.lth's, no argument) as a verdict codomain beside `Bool` and
   `Failures E` (4.R6, 5.S6); `check src/luthier/lib/algebra.lth` becomes clean; a test.
2. `Typing.__init__` reads its declarations with `elaborate.walk_type`; `arrows` removed from
   check.py; its test at line ~278 moves to `tests/test_elaborate.py` as a test of `as_type`.
3. The test at line ~486 (`test_an_operator_whose_function_is_not_typed_as_a_function_is_left_out`)
   pinned a limit elaborate 6 removed: make it expect `6 of 6 acts`, `the whole file elaborates.`
   with the 4.R9 on `bad`, or replace it by a test of what is still left out (an operator whose
   function has no declared type at all), whichever still tests something.

Check: `PYTHONPATH=src python3 -m pytest tests/test_check.py tests/test_elaborate.py
tests/test_spec.py -q`, `PYTHONPATH=src python3 -m luthier.cli check src/luthier/lib/algebra.lth`,
then `PYTHONPATH=src python3 -m pytest tests -q` (must be green). Do not commit. Report in your
final message.
