# The rest of the external review that does not wait for Luciano, brief for an Opus agent

Read `CLAUDE.md`, then `summary.md` and `summary-BCD.md` in this folder, and the fix reports
already done here (`report-fix-certification.md`, `report-fix-host.md`, `report-run-host.md`,
`report-fix-BCD.md`) and `record/IA/controls-2026-10-15/report-*.md`, to know what is closed.
Then do every remaining finding that is plainly the theory's or the file's and does not touch
one of Luciano's open questions (listed in `record/plan/night-2026-10-13.md` "Questions" and in
the two summaries' top screens: the replay and the budget in the identity, the one-case first
action, the record as memo key, the observer assumed, the provisional extern, 7.S10's Bounded,
the tailSeries cutoffs). Known candidates: laws.lth `ForallOnPoints` settling no multi-parameter
sampled law, `NotFlips` and `CitedWhole` unsatisfiable together (summary-BCD C section);
certification.lth `transport` taking any standing as the identity (summary.md C6); the spec
sentences the summaries name as stale (10.S5 "two applications to one token", 6.S16 "the file
is not written", chapter 6 before D-2026-10-14-c, 10.S13's heading). Each fix `[proposed]`, one
commit per file by path, controls kept refuted (L9.14). Report with a shell heredoc to
`report-second-line.md` here, committed alone: a table of every finding of the two summaries
with its state (fixed here with commit, fixed before, waiting for Luciano, a reviewer's
misreading, left with why). Accepted when: changed files parse and check clean, `python3
scripts/check_spec.py` prints nothing, the suite passes (not during a certify), and `luthier
certify` on any `_laws.lut`/`_controls.lut` whose theory changed shows no CONTROL FAILED.
