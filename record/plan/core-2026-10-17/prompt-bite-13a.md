# Brief: the core's bite 13a, the machinery left before the core closes

Bite 13 of `execution.md` section 6 is split (the coordinator, 2026-10-22): 13a, here, the fixes in
check, the elaborator and certify; 13b (`prompt-bite-13b.md`), the library's leftovers and the
closing, by another agent at the same time in .lth/.lut files. 13b re-certifies once, after 13a.

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` (Status, sections 0 to 4,
bite 12's and bite 13's "Also" paragraphs), the reports `report-bite-12a.md` and
`report-bite-12b.md`, and `record/decisions.md` at D-2026-10-18-b, -f, -j and D-2026-10-22-a.

Build, each with a test that fails before and passes after:
1. A structure whose laws fix its carrier (report-bite-12b.md finding 1 and its question; the
   coordinator took (a), 2026-10-22): check accepts `Doubles (F : U)` with its conjunction written at
   `Doubles Float64`, so `plus` and `times` resolve at `Float64` and the within-bound laws keep their
   ranges (D-2026-10-18-j). Change 4.R6 in check.py and its sentence in the spec, marked as the
   coordinator's. Then numbers.lth's `Doubles` and its uses (numbers_model.lut, the examples'
   `doubles : Doubles` to `Doubles Float64`): these .lth/.lut edits are yours, tell 13b's agent
   nothing, it stays off numbers and the `doubles` lines of the examples.
2. The core's generic functions reach a container's claims (report-bite-12b.md finding 3):
   `toList Vec Float64 v` takes `v` as the `Foldable` model instead of filling the model.
3. Operator bindings never serve a sibling subtype (report-bite-12a.md, item 2's leftover), as
   claims already don't (18cba7e).
4. D-2026-10-22-a: a test that a model certified by its passes is not refused for lacking controls
   run at that model, a law's controls serving every model of its theory; fix 012b3ce if it fails.
5. The "uncontrolled ... its controls are at another hash of its cone" reading of arrays' summing
   laws (report-bite-12b.md finding 2): say why a control at another hash doesn't count and whether
   it should (D-2026-10-22-a says a control is the law's); fix if it is a defect.

Run everything with `/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`;
keep scratch files under ~/.cache/luthier-13a/, not /tmp. Commit each item as it passes. Your files:
src/luthier/*.py, tests/test_*.py, docs/spec/, numbers.lth, numbers_model.lut and the `doubles`
lines of the examples. Don't re-certify the stores: 13b does it after you. Small commits staged by
path, never `git add -A`: subject, blank line, one body line, ending with "Co-Authored-By: Claude
Opus 5.5 <noreply@anthropic.com>".

Accepted when: each item's test passes; `python -m pytest -q tests/test_check.py
tests/test_elaborate.py tests/test_run.py tests/test_certify.py tests/test_tester.py` passes, or
each failure left is a stale store for 13b's re-certification (name it); `python
scripts/check_spec.py` prints only its known finding. Report:
`record/plan/core-2026-10-17/report-bite-13a.md`, committed (if your Write is refused for it, put
its full text in your final message): per item what you did, the checks, the cones you expect
moved, decisions taken on your own, at most one question.
