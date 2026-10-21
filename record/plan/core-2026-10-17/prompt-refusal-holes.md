# Brief: close the holes in the core-name refusal (review-bite-5.md)

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/review-bite-5.md` (the findings),
`execution.md` sections 0, 2 and 6 (bite 5) and its status of 2026-10-21, `report-bite-5.md`,
`record/decisions.md` at D-2026-10-18-b (names per concept; the core is visible without an import;
a redefinition of a core name is refused), and spec 12.S22 in `docs/spec/`.

Close findings 1, 2a, 2b and 2c, each with a test that fails before the fix and passes after:

1. `redefinitions` (src/luthier/run.py) exempts a CORE_COLLISIONS name for every file. Exempt only
   the (file, name) pairs listed: a non-core file gets no exemption.
2a. An `operator` act that rebinds a core operator (`operator + := intMinus`) is refused like any
   other redefinition, naming the core file.
2b. A label of a sum alias (`S = { unit : Int || compose : Int }`) that is a core name is refused.
2c. An import alias (`import "..." Monoid as compose`) that is a core name is refused.

Finding 2d is the coordinator's decision (2026-10-21, one commit undoes it): record fields,
parameters and pattern variables stay free, since D-2026-10-18-b is about top-level names; write
that sentence into spec 12.S22 and add one test that shows a field `map` and a parameter `compose`
are accepted.

Leave the CORE_COLLISIONS entries themselves alone: bite 11's agent removes the arrays and tables
entries in run.py at the same time; retry an edit or commit that conflicts, and stage by path.
Bite 10 works in ebnf, grammar and term; bite 11 in arrays and tables. Touch none of their files.
If a fix makes an existing library or example file refused, that is a finding: list it, don't
exempt it.

Run everything with `/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`.

Accepted when: the four new tests and the 2d test pass; `python -m pytest -q tests/test_check.py
tests/test_elaborate.py tests/test_run.py` passes, or every failure left is shown to be a stale
store of another bite's files (name it); `python scripts/check_spec.py` prints only its known
finding; `luthier check` over `src/luthier/lib` and `examples` refuses nothing new, or the report
lists each file refused. Small commits: a subject, a blank line, one body line, ending with
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", staged by path, never `git add -A`.

Report: `record/plan/core-2026-10-17/report-refusal-holes.md`: what you changed, the checks'
output, files newly refused, decisions taken on your own, at most one question. Commit it.
