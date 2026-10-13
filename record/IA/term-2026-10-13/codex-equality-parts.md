# term_model.lut, equality demands its parts: brief for Codex

Written 2026-10-13 by Claude Fable 5.1, run from the session.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` §5 gained the
law `EqualityDemandsParts` (git log -1 -- src/luthier/lib/term.lth): when `==` (the body
`Primitive "=="` applied to two operands) compares a part that is not yet a value, the step
reduces that part in place, leftmost first, as a match demands what its patterns inspect; the
operands' heads step first as `HeadFirst` says, then their parts. `EqualityStuck` stays: a part
that cannot become a value (a hole, a lambda, an extern) leaves `==` stuck.

Update `src/luthier/lib/term_model.lut` (yours; report record/IA/term-2026-10-13/codex.md) so that
`stepper` meets it and every other law of §5. Check by hand; parse with `PYTHONPATH=src python3 -m
luthier.cli parse src/luthier/lib/term_model.lut`. Touch nothing but term_model.lut and your
report; do not commit. Append a section "Equality demands parts" to the report.
