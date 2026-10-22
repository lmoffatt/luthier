# Brief: the core's bite 12a, the machinery bite 12 needs before its library re-certification

Bite 12 of `execution.md` section 6 is split in two (the coordinator, 2026-10-22): 12a, here, the
fixes in the elaborator, the tester and certify that move cones; 12b, the library and the examples
(`prompt-bite-12b.md`), done by another agent at the same time in .lth/.lut files only. 12b
re-certifies once, after 12a lands.

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md`: the Status of 2026-10-21,
sections 0 to 4 and 6 (bite 12 with all its "Also" paragraphs, and bite 13's); the reports
`report-bite-8.md`, `report-bite-11.md`, `report-verify-6-11.md` and `report-refusal-holes.md`
beside it; `record/decisions.md` at D-2026-10-18-b (names resolved by type), D-2026-10-18-f
(bare-form conjunctions, the tester splits them), D-2026-10-18-j.

Build, each with a test that fails before and passes after:
1. The three elaboration defects bite 4 kept for the hash (bite 12's first "Also": `T * Float64`
   as the product, an alias parameter captured by a record field, products nesting right as 3.S4
   says). Remove the spec's known-defect marks (2.S8, 4.R7, 3.S4) when each is fixed.
2. Resolution through a subtype to its base never lands on a sibling subtype's claim (bite 12's
   "Also" of 2026-10-21 on the concepts document's question).
3. A demand for a bare property name (`doubles: Neutral`) is served by the entries the tester
   records for that conjunct under the conjunction's law (`Doubles`, `conjunct` text), per
   D-2026-10-18-f (report-verify-6-11.md, failure 2: `served` in certify.py falls back to conjuncts
   only when entries exist under the demanded name). validate_graph.run.lut and experiment_zero
   are refused on exactly this.
4. Whether an `operator` act is exported with its file (bite 12's "Also" (2) on report-bite-11.md:
   arrays_model's bindings don't reach an importer). Read the spec on operator acts first; if the
   spec says they are exported, make it so; if it is silent, implement export, write the clause
   as [proposed] in the spec, and say so in the report.
5. The per-case cost of exhaustive cases: report-verify-6-11.md failure 1 measured about 1 s a
   case (TheThreeSourcesGrade, 270 cases, 4m15 with `certify --no-cert`), so
   test_certify's regions test no longer finishes. Profile one line (cProfile), say where the time
   goes and since which commit (bisect between 7180f7b and HEAD if cheap), and fix it if the cause
   is a regression of bites 6 to 11. If it can't be fixed here, mark the test with the existing
   `LUTHIER_SLOW` marker and say why in the report.

Run everything with `/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`.
Commit each fix as it passes. 12b's agent edits probability, belief, optimization, plot, their
models and tests, arrays.lth's controls and the examples: touch none of those; your files are
src/luthier/*.py, tests/test_*.py and docs/spec/. Don't re-certify the stores: 12b does it after
you. Small commits staged by path, never `git add -A`: subject, blank line, one body line, ending
with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".

Accepted when: each item's test passes; `python -m pytest -q tests/test_check.py
tests/test_elaborate.py tests/test_run.py tests/test_certify.py tests/test_tester.py` passes, or
each failure left is a stale store (cones moved by items 1 and 2; name the file) for 12b's
re-certification; `python scripts/check_spec.py` prints only its known finding. Report:
`record/plan/core-2026-10-17/report-bite-12a.md`, committed: per item what you did, the checks,
the cones you expect to have moved, decisions taken on your own, at most one question.
