# elaborate.py, bite 2: the types of untyped lambda parameters, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`. After check.py (record/IA/check-2026-10-13/codex.md).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (another session may change
`src/luthier/lib/program.lth`): change only `src/luthier/elaborate.py` and
`tests/test_elaborate.py`, and write your report; a failure from another file is someone else's,
report it, do not fix it.

`luthier check` (`src/luthier/check.py`) fails 4.R6 and 4.R9 on three programs of `tests/spec/`
(`r6_predicate_body.accept.lut`, `k_recursor.accept.lut`, `r12_block.accept.lut`) because
`elaborate.py` leaves the domain of an untyped lambda parameter as `Hole`: in
`Even : Int -> Bool := fn n { n mod 2 == 0 }` the parameter `n` should get `Int` from the declared
type, and in `twice (fn k { k + 1 }) r` the parameter `k` should get the domain that `twice`
expects. Give elaboration this checking direction, as `translation.lth` allows (its laws compare up
to alpha and leave the elaborator free where the table does not fix the type): a lambda elaborated
against a known function type (a definition's declared type, an argument position whose parameter
type is known, a block item with a type) takes its parameters' domains from it; otherwise `Hole`
as now. Add tests for each source of the expected type, and keep every law test of
`tests/test_elaborate.py` passing.

Check: `python3 -m pytest tests/test_elaborate.py tests/test_check.py tests/test_spec.py -q`, then
`python3 -m pytest tests/ -q`; report which strict xfails of `tests/test_spec.py` now pass (they
would fail as XPASS; do not change `test_spec.py`, list them). Do not commit. Report in a few lines
to `record/IA/elaborate-2026-10-13/codex-2.md`.
