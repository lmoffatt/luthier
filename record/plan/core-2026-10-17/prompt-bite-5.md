# Brief: the core's bite 5, the prelude, the refusal, qualified access, and Placement

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` sections 0, 1, 6 (bite 5)
and the 2026-10-18 answers; `report-bite-4.md` beside it (bite 4 made the core the elaborator's
prelude as core.lut plus what it imports: this bite makes it the whole lib/core/ directory, for the
loader and the checker alike); `record/decisions.md` at D-2026-10-18-b (the whole core the
prelude; a file may not redefine a core name, refused; `Functor.map` qualifies) and D-2026-10-18-e
(generators.lth's `Metric` becomes `Placement`, `LinearPlacement`, `LogPlacement`; test lines keep
`SampledMode linear`).

Build bite 5 exactly as section 6 describes it, plus the rename of D-2026-10-18-e: generators.lth,
test.lth (`SampledMode : Placement -> Mode`), generators_model.lut, tester.py where it reads the
names, and chapter 7's three sentences (7.S2, 7.S4, 7.R1) reworded. The rename moves cones; re-certify
what moves (one wave, without --deep) and report the lines that ran; a refuted law is a finding.

Accepted when: everything section 6 lists for bite 5; `grep -rn "\bMetric\b" src/luthier/lib/generators.lth
src/luthier/lib/test.lth` finds no generators' Metric left; `python -m pytest -q` passes in full
(848 passed, 6 skipped, 9 xfailed before, plus yours; in the background); `python3 scripts/check_spec.py`
prints its known finding; `luthier certify` over every `tests/tester/*.test.lut` prints 0 lines ran
for every non-fixture program after the wave; `python3 scripts/core_metrics.py`'s counts in the last
code commit's message. You are the only agent in the repository. Small two-line commits (subject,
blank line, body) ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", staged by
path. Report: `record/plan/core-2026-10-17/report-bite-5.md`, by shell heredoc, committed.
