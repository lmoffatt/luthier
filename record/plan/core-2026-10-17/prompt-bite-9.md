# Brief: the core's bite 9

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` sections 0, 5 (the
migration map: the rows for your files) and 6 (bite 9), and the reports of bites 6 and 7 beside it
(report-bite-6.md, report-bite-7.md: the core's structures, the list library in lib/core/lists.lut,
`<>` for every semigroup, the temporary local renames bite 6 made such as `mapKernelList`).
In `record/decisions.md`: D-2026-10-18-a, -b, -f (no one-line wrappers per law: where section 6
says "as wrappers", write the bare form), D-2026-10-21-a.

Build bite 9 as section 6 describes it: every row of section 5 for your files migrated to the
core's names and generic functions, the local reinventions removed in favour of lists.lut's, every
renamed law graded and controlled (L9.14), the lines whose cones move re-certified (one wave,
without --deep). A law refuted after the migration is a finding to report, never weakened.

Use /home/lmoffatt/miniconda3/bin/luthier and /home/lmoffatt/miniconda3/bin/python for every
luthier and pytest command (conda; the luthier first on PATH is another Python and stales the
stores). Other agents work at the same time: bite 8 in numbers.lth, numbers_model.lut, algebra.lth
and their test programs; bite 10 in term.lth, term_model.lut, program.lth, grammar.lth, ebnf.lth, library.lth, translation.lth. Touch none of their files; stage only yours by path; retry a commit that
fails on .git/index.lock.

Accepted when: section 6's criteria for bite 9; `python -m pytest -q` passes in full (887
passed, 6 skipped, 9 xfailed at bite 7, plus yours; a failure in another bite's files is reported,
not fixed); `python3 scripts/check_spec.py` prints only its known finding; `python3
scripts/core_metrics.py` counts before and after. Small commits: a subject, a blank line, one body
line, ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>". Report:
`record/plan/core-2026-10-17/report-bite-9.md`.
