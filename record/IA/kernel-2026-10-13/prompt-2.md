# kernel.py, bite 1b: named records and the equality split, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`. After `codex.md` in this folder.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only
`src/luthier/term.py`, `src/luthier/kernel.py`, `tests/test_kernel.py`, and write your report;
a failure from another file is someone else's, report it, do not fix it.

Since your first bite, `src/luthier/lib/term.lth` and `kernel_laws.lth` changed (f421684 and the
commit after it; `git log -3 -- src/luthier/lib/term.lth src/luthier/lib/kernel_laws.lth` and
`git show` them), on Luciano's D-2026-10-13-x (a record is a product whose projections are named):

1. `Term` gains `Record : List (String * Term) -> Term`, `RecordValue : List (String * Term) ->
   Term`, `Proj : Term -> String -> Term`. Add them to `term.py`, and to every function of
   `kernel.py` (free names, alpha, substitution, canonical form, reduction): `ProjOfRecord`
   reduces `Proj (RecordValue kvs) x` to the value at `x`; `Record` and `RecordValue` are values
   (`ValuesStay`). Add the new laws to `tests/test_kernel.py`, one test each, and the new
   constructors to the generator.
2. `IotaSkips` is restated (an arm that matches after the skipped one); transcribe the new law.
3. `kernel_laws.lth` §1 split `Object` (reflexive, symmetric, transitive) from `Structural`
   (`Object` plus `Substitutive` over every function); alpha-equivalence is an `Object`, respected
   by the operations of its theory (`AlphaCongruent`). Replace the strict xfail on
   `Object.Substitutive` by a test that alpha is an `Object` and that the structural equality of
   `term.py`'s dataclasses is `Substitutive` on the generated terms.

Check: `python3 -m pytest tests/test_kernel.py -q`, then `python3 -m pytest tests/ -q`. Do not
commit. Report in a few lines to `record/IA/kernel-2026-10-13/codex-2.md`: what changed, the
counts, any law not met with its counterexample, any disagreement between `term.lth` and
`term_model.lut` you notice.
