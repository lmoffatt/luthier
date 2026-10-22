# Brief: the core's bite 13b, the library's leftovers and the core's closing

Bite 13 of `execution.md` section 6 is split (the coordinator, 2026-10-22): 13a
(`prompt-bite-13a.md`), the machinery, by another agent at the same time in src/luthier/*.py,
tests/test_*.py, docs/spec/, numbers.lth, numbers_model.lut and the `doubles` lines of the
examples; 13b, here, everything else in the library, then the closing.

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` (Status, sections 0 to 6,
bite 13 with its "Also" paragraphs), the reports `report-bite-9.md`, `report-bite-10.md`,
`report-bite-12b.md` (its core_metrics section lists what is left, with reasons) and
`report-verify-6-11.md`; `record/decisions.md` at D-2026-10-18-a, -b, -f. Read the observations on
the files you change in `record/Lucianos observations/`.

The core's end is measured (section 0, D-2026-10-18-a): core_metrics' (1) homonyms, (2) list
helpers and (3) unclaimed laws at 0, or each one left named with its reason (plot's public names
wait for G1 to G5, D-2026-10-17-h, and stay); the `loose` notice only where it is real.

1. The search-style recursions bites 9 and 10 kept (program.lth 64, term_model.lut 25,
   certification.lth 20, plan.lth 14, and the rest core_metrics lists) and the test programs'
   local helpers: each moved to a core function, or kept with its reason in a comment and in the
   report. Behaviour must not change: compare old against new with `luthier eval` on terms that
   exercise each rewritten function (~/.cache/luthier-sdk/difft/run.sh is how bite 10's was done).
2. The 30 homonyms between machinery files (certification, demand, grammar, term, translation,
   program, laws, world), `Resolution`, `uniformPValue`, `pi`, and `larger` (one join of
   `Float64`'s order in the core, plan 5.1). `allUnit` (report-bite-12b.md finding 7).
3. The 21 unclaimed: each claimed by a structure, or shown not to be a law (a predicate such as
   optimization.lth's `isConverged`); `Settling` given a model and a test line so its two
   combination laws are graded.
4. The check failures report-bite-12b.md finding 5 lists: distances.lut `pairI`/`pairJ`,
   plot_cases.lut `perms`, lists_controls.test.lut (4.R3), experiment_zero.run.lut (4.R2).
5. `check.py`'s `loose` notice narrowed to the real cases, if no earlier bite did it (bite 13's
   files line).
6. Wait for 13a: its report `report-bite-13a.md` committed is the signal (check `git log` between
   steps). Then re-certify every store with `/home/lmoffatt/miniconda3/bin/luthier certify`,
   program by program, each with its own log under ~/.cache/luthier-13b/ (not /tmp), twice: the
   second pass at 0 lines ran for every non-fixture program. Run validate_graph.run.lut and
   experiment_zero.run.lut against their records. Run the suite file by file under `timeout 1800`.
7. The closing (bite 13's files line): this plan's Status, `record/plan/code-follows-principles-
   2026-10-16.md` (the core done, its queue reopened), a self-handoff in `record/handoff-*.md`,
   the notes to the spec's agent gathered (12.S4, 12.S22, 4.R13), core_metrics' counts recorded
   in the commit. The tag is Luciano's (D-2026-10-17-e): don't tag.

Run everything with `/home/lmoffatt/miniconda3/bin/python`. Long runs: start them detached with
their output under ~/.cache/luthier-13b/ and wait in the foreground with bounded waits (`timeout
540 bash -c 'until [ -e DONE ]; do sleep 20; done'`, repeated); don't hand back while they run.
Small commits staged by path, never `git add -A`: subject, blank line, one body line, ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>".

Accepted when: section 0's counts (1) to (3) at 0, or each left named with its reason; the second
certify pass at 0 lines ran; validate_graph and experiment_zero reproduce their records; the
suite passes in every file, or each failure is named with its cause; `python
scripts/check_spec.py` prints only its known finding; the plan says nothing false. Report:
`record/plan/core-2026-10-17/report-bite-13b.md`, committed (if your Write is refused for it, put
its full text in your final message): what you changed, the differential's counts, the checks,
core_metrics before and after, decisions taken on your own, at most one question.
