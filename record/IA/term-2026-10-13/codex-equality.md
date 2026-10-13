# term_model.lut, structural equality: brief for Codex

Written 2026-10-13 by Claude Fable 5.1, run from the session.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` §5 gained three
laws at 360b4d4 and 051e6aa (`git show 360b4d4 051e6aa -- src/luthier/lib/term.lth`):
`PrimStructural` (`==` on pairs, records by field, injections by label, floats, giving
`Var "true"` / `Var "false"` in one step), `PrimConstructors` (`==` on constructors of a `data` of
the program, by constructor then part by part; lists are `cons`/`nil` of core, the same rule) and
`EqualityStuck` (`==` does not step on lambdas, externs, a declared name, or a value with a hole in
a part). The operator is the body `Primitive "=="` applied to two values, as `Prim` writes it.

Update `src/luthier/lib/term_model.lut` (yours; report record/IA/term-2026-10-13/codex.md) so
that `stepper` meets the three, and still every other law of §5: equality is structural, part by
part, on closed values of concrete parts, and stuck otherwise. Check by hand; parse with
`PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/term_model.lut`. Touch nothing but
term_model.lut and your report; another agent works on src/luthier/kernel.py in this tree. Do not
commit. Append a section "Equality" to the report.
