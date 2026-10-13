# kernel.py, bite 1e: the alpha fixes and Axiom's string, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec` after bite 1d (`codex-4.md`).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only `src/luthier/term.py`,
`src/luthier/kernel.py`, `tests/test_kernel.py`, and write your report; a failure from another file
is someone else's, report it, do not fix it.

Two changes in `src/luthier/lib/term.lth` since your last bite (`git show 23d23f4 048cd55`):
1. 23d23f4 fixes the two conflicts your bite 1c reported (`codex-3.md`): a data's name is a binder,
   compared by `AlphaPartsAgree` through `underBinderPairs`; and `renameAll` renames pattern
   variables simultaneously (`swapNames`). Follow the theory in `kernel.py`, and turn the two
   strict xfails of `tests/test_kernel.py` into ordinary tests of the laws as now stated.
2. 048cd55: `Axiom : String -> Term` (the text of 3.S2's `axiom "..."`); `HolesStay` uses `Axiom f`.
   Update `term.py`, every function of `kernel.py` and the generator.

Check: `python3 -m pytest tests/test_kernel.py -q`, then `python3 -m pytest tests/ -q`. Do not
commit. Report in a few lines to `record/IA/kernel-2026-10-13/codex-5.md`: what changed, the
counts, any law not met with its counterexample.
