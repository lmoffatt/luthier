# term_model.lut after the review of layers 0-1: brief for Codex

Written 2026-10-13 by Claude Opus 5.5, run from the session.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` changed after
the external review of layers 0-1 (record/IA/layers-0-1-review-2026-10-13/summary.md, section A):
at cc2542d §2 `Alpha` gained `RenameBound` for every binder and the converse law `AlphaPartsAgree`;
at 2409c59 §5 `Reduction` became an exact one-step theory, `Reduction a sb : { step : Program ->
Term -> Maybe Term }`, with `reduce` a definition (the fuelled iteration) and laws `Beta`, `Delta`,
`HeadFirst`, `HolesStay`, `Iota`, `IotaPair`, `IotaSkips`, `ProjOfRecord`, `Prim`,
`ExternIsValue`, `ValuesStay`, `DatumIsInert`. Read them: `git show cc2542d 2409c59 --
src/luthier/lib/term.lth`.

Update `src/luthier/lib/term_model.lut` (yours; report record/IA/term-2026-10-13/codex.md) so that:
- `alpha` meets `AlphaPartsAgree` and the new `RenameBound`;
- the reduction model is a value `stepper : Reduction alpha substitute := { step := ... }`, one
  weak-head step, meeting every law of §5 as now stated: a defined name found wherever the program
  defines it (a `Define` after a `Declare` of the same name fills it, 3.S1); the head of an
  application, the scrutinee and the projected record step first; a match whose first arm must
  inspect a stuck scrutinee does not step (a hole is never read as a miss, nor as a nullary
  constructor); patterns are linear (no equality test between repeated variables); `Prim` on
  `Primitive` bodies only (an undefined `Var "+"` is a hole), integers `+ * - < ==`, doubles `+`,
  strings `==`, results `Var "true"` / `Var "false"`; an extern alone is a value;
- the old `reduce` model goes (term.lth's `reduce` is now a definition over any `step`).
Check every law by hand, as before, and parse with
`PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/term_model.lut`. Touch nothing but
term_model.lut and your report; another session's Codex works on src/luthier/kernel.py, term.py
and tests in this tree. Do not commit. Append a section "After the review" to the report: what
changed, any law not met.
