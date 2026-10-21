# Brief: the core's bite 11, arrays and tables over the core

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md`: the status of 2026-10-21,
sections 0, 2, 3.4 (structures/containers.lth, the claims arrays makes), 4, 6 (bite 11) and the
paragraphs of 2026-10-18; `report-bite-6.md`, `report-bite-7.md` and `report-bite-8.md` beside it;
`record/decisions.md` at D-2026-10-17-f, D-2026-10-18-b (names per concept, resolved by type),
D-2026-10-18-f (bare-form conjunctions), D-2026-10-18-j (numerical laws relate input and output
tolerances and state their range), D-2026-10-21-a (`<>` for the semigroup operation). Read the
observations on these files in `record/Lucianos observations/` before changing them.

Build bite 11 as section 6 describes it. A bound is the theory's, never tuned to pass: a refuted
bound is a finding to report with its counterexample. Each law gets its controls. Remove the
CORE_COLLISIONS entries bite 11 owns (arrays and tables).

Run everything with the conda Python: `/home/lmoffatt/miniconda3/bin/python` and
`/home/lmoffatt/miniconda3/bin/luthier` (the `luthier` first on PATH is another Python whose numpy
gives other cones). Commit each finished file as you go, so an interruption loses nothing.

Accepted when: section 6's criteria for bite 11; `python -m pytest -q` passes in full, or every
failure left is shown to be a stale store of another bite's files (name the file); `python
scripts/check_spec.py` prints only its known finding; `luthier certify` over `tests/tester/arrays_*`
and `tables_*` prints 0 lines ran after your wave; `python scripts/core_metrics.py` counts in the
report, before and after.

Other agents work at the same time: bite 9 in generators, certification, world, plan, demand and
test.lth; bite 10 in ebnf, grammar, term and the self-description. Touch none of their files:
`generators_model.lut`'s two arrays import lines go in your report for the coordinator to pass on.
Retry a commit that fails on .git/index.lock. Small commits: a subject, a blank line, one body
line, ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", staged by path, never
`git add -A`.

Report: `record/plan/core-2026-10-17/report-bite-11.md`: what you built, the checks' output, the
lines re-certified, core_metrics before and after, decisions taken on your own, at most one
question. Commit it.
