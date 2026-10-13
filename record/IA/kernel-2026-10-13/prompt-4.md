# kernel.py, bite 1d: Let and the substitution laws, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec` after bite 1c (`codex-3.md`).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only `src/luthier/term.py`,
`src/luthier/kernel.py`, `tests/test_kernel.py`, and write your report; a failure from another file
is someone else's, report it, do not fix it.

`src/luthier/lib/term.lth` gained a local definition (Luciano, D-2026-10-13-aa Q1; `git show
fe3bdab`):
- `Term` gains `Let : String -> Term -> Term -> Term -> Term` (name, type, value, body); the name is
  bound in the body only. Add it to `term.py` and to every function of `kernel.py`: free names,
  swap, head (`"Let"`), alpha (`RenameBound`: `Let x ty s t ~ Let y ty s (swap x y t)`;
  `AlphaCongruent`, `AlphaPartsAgree`: type and value alpha-equal, bodies under the binder),
  substitution, canonical form.
- Substitution laws restated: `SubstGoesInside` over `App`, `Pair`, `Inj`, `Proj`, `Sum`, `Record`,
  `RecordValue`, `Match` (a wildcard arm); `SubstStopsAtShadow` over `Lam`, `Pi`, `Sigma`,
  `Subtype`, `Let`, a `PVar` arm; `SubstPassesBinder` over `Lam`, `Pi`, `Sigma`, `Subtype`, `Let`;
  new `SubstAvoidsCapture` over `CaptureCase` (`y` free in `s`, `z` fresh for `s` and `b`):
  `subst x s (Lam y ty b)` is alpha-equal to `Lam z (subst x s ty) (subst x s (swap y z b))`.
- Reduction: new `Zeta`, `step p (Let x ty v b)` steps to `subst x v b`; `Delta` unfolds a defined
  name in head position always (Q7).
Transcribe every new or changed law in `tests/test_kernel.py`, one test each, and add `Let` to the
generator.

Check: `python3 -m pytest tests/test_kernel.py -q`, then `python3 -m pytest tests/ -q`. Do not
commit. Report in a few lines to `record/IA/kernel-2026-10-13/codex-4.md`: what changed, the
counts, any law not met with its counterexample.
