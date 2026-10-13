# The theories' own refusals and program.lth's two rules: brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b), on
`record/IA/theory-leftovers-2026-10-14/report.md` (f8c5f40), section "The seven files added after
e2590af". luthier-03 is paused; by Luciano's word the night continues with agents.

## The prompt

Read `CLAUDE.md` first, then that report section and its "Per group". Other agents edit
`src/luthier/*.py`, `tests/` and `docs/spec/` meanwhile: touch none. You may change
`src/luthier/lib/program.lth`, `algebra.lth`, `tables.lth`, `arrays.lth` only, one commit per
file (`git add` its path; never `-A` or `.`; no `git stash` or `git checkout`), messages naming
the rule, ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".

1. program.lth: (a) 4.R3 `untouched`: a projection `e.f` counts as touching `e` (1.S7: count
   `namePrefix`); (b) 4.R13 `rivalModel` compares `typeOfAct`, not `declaredSurface`; (c) 4.R4
   `makesAType` accepts `primitive` as it accepts `extern` (11.R1, 11.R2); (d) 4.R3 `lawReadsIn`
   counts a law's binders as reads (1.S7), so `(r : Fin t.nRows)` reads `nRows`. Each with its
   spec item cited above the law, marked [proposed] where the spec is read rather than quoted.
2. algebra.lth `OrderedField`: inline the record in `FieldIsOrdered` so the fields are read by
   the law itself (4.S15), as the report says.
3. tables.lth `Codec`: `eq` read by a law itself, not only through `sameParse` (inline or add the
   reading law); `Table`'s `nRows` is cleared by 1(d).
4. arrays.lth: nothing unless 1(a) leaves a shape refinement refused by the rule's own reading;
   if the `Orthogonal` capture (report, 4.R9 cause c) is the file's, rename the bound field or the
   parameter so no capture can happen, and say so.
Every file must still parse (`PYTHONPATH=src python3 -m luthier.cli parse FILE`). Report in your
final message (the harness may refuse a report file; the coordinator saves it): per change the
spec item and whether check.py must mirror it.
