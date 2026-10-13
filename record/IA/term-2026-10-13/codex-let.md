# term_model.lut, Let and the rest of the review: brief for Codex

Written 2026-10-13 by Claude Opus 5.5, run from the session.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` changed again
since your last section of record/IA/term-2026-10-13/codex.md: read `git show fe3bdab 048cd55
23d23f4 -- src/luthier/lib/term.lth`. In short: `Term` gained `Let : String -> Term -> Term -> Term
-> Term` (name, type, value, body; the name bound in the body only) with the law `Zeta` (`Let x ty
v b` steps to `subst x v b`); `Axiom` now carries a `String`; the substitution laws cover every
constructor (`SubstGoesInside`, `SubstStopsAtShadow`, `SubstPassesBinder` over all binders, `Let`
included) and the capture case (`SubstAvoidsCapture`); in §2 a `data`'s name is compared as a
binder (`underBinderPairs`), and `renameAll` renames pattern variables at once, so the limitation
your report states (multi-variable patterns compared literally) can go.

Update `src/luthier/lib/term_model.lut` so that its four models (`alpha`, `substitute`,
`canonical`, `stepper`) handle `Let` and the new `Axiom`, and meet every law of term.lth §2 to §5 as
now stated; remove the multi-variable limitation and the literal comparison of `data` names. Check
every law by hand and parse with `PYTHONPATH=src python3 -m luthier.cli parse
src/luthier/lib/term_model.lut`. Touch nothing but term_model.lut and your report; another Codex
works on src/luthier/kernel.py, term.py and the tests in this tree. Do not commit. Append a section
"Let" to the report: what changed, any law not met.
