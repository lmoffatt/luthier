# kernel.py, bite 1c: exact alpha and one-step reduction, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`. After `codex-2.md` in this folder.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (another Codex is changing
`src/luthier/lib/term_model.lut` for the same theory changes): change only `src/luthier/term.py`,
`src/luthier/kernel.py`, `tests/test_kernel.py`, and write your report; a failure from another file
is someone else's, report it, do not fix it.

`src/luthier/lib/term.lth` changed after the layers 0-1 review (`git show cc2542d 2409c59`):

1. §2 `Alpha`: `RenameBound` covers `Lam`, `Pi`, `Sigma`, `Subtype` and a `PVar` arm; new law
   `AlphaPartsAgree`, the converse of congruence (alpha-equal wholes have the same head, equal
   constants, labels and free names, alpha-equal parts, binders and match arms as the law states).
   A reviewer showed that `head s == head t and same free names` passed every former law; make
   sure `alpha_equal` meets the new one and add a test that the weak model fails it.
2. §5 `Reduction`: the theory's field is `step : Program -> Term -> Maybe Term`, one weak-head step
   (`nothing` is weak head normal form); `reduce` is now the fuelled iteration of `step`, defined in
   the theory. `agree` is gone; the laws compare `step` exactly up to alpha (`stepsTo`) or require
   normal form (`isNormal`): `Delta` (a bare `Var f` defined anywhere in the program, also after a
   `Declare`), `HeadFirst`, `HolesStay`, `Iota` with `PLit` and `PVar` arms, `IotaPair` both
   orders, `Prim` on `Primitive` bodies only (`App (App (Primitive "+") i) j`; Int `+ * - < ==`,
   Float64 `+`, String `==`; results `Var "true"`/`Var "false"`), `ValuesStay` with `Pair`, `Inj`,
   `Primitive`, `DatumIsInert`. Give `kernel.py` a `step(program, t)` and make `reduce` its
   iteration exactly as the theory defines it; transcribe every changed or new law in
   `tests/test_kernel.py` (one test each), drop the tests of laws that are gone.

Check: `python3 -m pytest tests/test_kernel.py -q`, then `python3 -m pytest tests/ -q`. Do not
commit. Report in a few lines to `record/IA/kernel-2026-10-13/codex-3.md`: what changed, the
counts, any law not met with its counterexample, any place where the theory did not decide.
