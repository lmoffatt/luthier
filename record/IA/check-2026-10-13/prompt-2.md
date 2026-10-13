# check.py, bite 2: follow program.lth 519bdf3 and a73fa4f, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), launched by it with `codex exec`. After `codex.md` in this folder.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (a Codex is changing
`src/luthier/elaborate.py` and `tests/test_elaborate.py`): change only `src/luthier/check.py`,
`tests/test_check.py`, `tests/test_spec.py`, and write your report; a failure from another file is
someone else's, report it, do not fix it.

`src/luthier/lib/program.lth` changed on your findings (`git show 519bdf3 a73fa4f`):
1. `remove` removes the dotted names a bound name prefixes (`c.parse` under binder `c`, `p.x`
   under parameter `p` are bound, 2.S14); `theoryHeads` searches the whole program for a
   declaration; labels of a labeled sum, alias or definition, are constructors and known;
   `violatesR5` reads every name of an extern's type, arrows included. Mirror each.
2. New predicates under `ReportsViolations`: `violatesR2R1` (a named argument names a parameter of
   the head's binders), `violatesR2R6` (a `<-` whose previous binding was never used), `violatesR13`
   (two `operator` acts binding one symbol to two functions of the same declared type, reported
   under each), `violates6R1` (a datum `cite n r ...` whose `r` does not type as `Reference`).
   Mirror each, with tests of both directions where the theory states them.
3. `Typing`'s `SameSeparates`: the identity of a record includes its names and their order, so two
   records with swapped fields, or a renamed field, are not `same`; `k_label_order.reject.lut` is
   then 4.R9's mismatch. Make the specimen's `same` on `Record` compare names positionally.
Then run `tests/test_spec.py`: every strict xfail that now passes becomes an ordinary case
(remove its mark); leave as xfail only `n2_r_gone`, `n3_primitive_outside_core`,
`n4_axiom_outside_lib` (11.R1 to 11.R3 stay out of `program.lth` for `v0.2`, pending Luciano) and
`r2_definition.reject` (4.R2's SCC half, open by design), and any case whose failure is
`elaborate.py`'s (say which). Rerun `luthier check src/luthier/lib/*.lth src/luthier/lib/*.lut` and
report the failures by file and rule.

Check: `python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then `python3 -m pytest
tests/ -q`. Do not commit. Report in a few lines to `record/IA/check-2026-10-13/codex-2.md`: the
verdict table of `tests/spec/` (pass / xfail with reason), the theory files' failures, every law of
`program.lth` not met with its case.
