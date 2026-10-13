# check.py bite 6: the typing rules on files that do not elaborate whole, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). On check bite 5's report
(`record/IA/check-2026-10-13/report-5.md`, "A gap found on the way"): six library files
(algebra.lth, generators.lth, kernel_laws.lth, numbers.lth, program.lth, term.lth) do not
elaborate as a whole ("record refinements require check.py"), so `check()` catches the
`ElaborationError` and 4.R6, 4.R8, 4.R9 and 6.R1 answer "no violation" on them: their clean
verdicts under those rules say nothing. Also: `unclash` is unnecessary since kernel bite 11
(aa198f2: substitution no longer captures a record's field).

## The prompt

Read `CLAUDE.md` first, then that report, `src/luthier/check.py` (`check`, `Typing`, the import
filter of bite 5 that drops an imported act the elaborator cannot read alone, `unclash`),
`src/luthier/elaborate.py` where it raises on record refinements. Other agents edit `tester.py`,
`cli.py`, `tests/test_tester.py` meanwhile: change only `src/luthier/check.py`,
`tests/test_check.py`, the `LIMITATIONS` table of `tests/test_spec.py`.

1. Type each file act by act: when the whole program does not elaborate, elaborate every act the
   elaborator can read alone (as the import filter does) and run 4.R6, 4.R8, 4.R9 and 6.R1 on
   those, reporting the acts left untyped by name with the elaborator's message (so a clean
   verdict says which acts it covers). Then run `luthier check` on the six files and report what
   the typing rules now refuse, by file and cause, judging whose it is (the checker's reading, the
   elaborator's limit, or the theory's); fix only what is plainly the checker's.
2. Remove `unclash` and `rename_free` if the tests pass without them on the current kernel; keep
   the `Orthogonal` test.
3. A `luthier check -v` line per file saying how many acts were typed and how many not.

Check: `PYTHONPATH=src python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message.
