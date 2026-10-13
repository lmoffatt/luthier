# elaborate.py, bite 5: a pattern on `<-` against any value, brief for a Claude agent

Written 2026-10-14 at the commit that holds this file, by the coordinating session (luthier-1b).
After bite 4 (opus-4.md, ff16b60), which refused a pattern that is not a bare name on a value that
is not an action and asked whether translation.lth should make it a match.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (on check.py, kernel.py,
term_model.lut, new theory files): change only `src/luthier/elaborate.py` and
`tests/test_elaborate.py`, and write your report; a failure from another file is someone else's.

translation.lth's law `Blocks` now says (1665b9d, `git show 1665b9d`): a pattern on `<-` against a
value that is not an action is the one-arm match too: `{ (a, b) <- n ; a }` with `n : Int * Int`
gives `Match (Var "n") [(PPair (PVar "a") (PVar "b"), Var "a")]`; only a bare name on a non-action
stays a `Let`. Replace bite 4's refusal by that translation, with the law's `gives` as a test, and
remove the Hole-typed special case of bite 4 if the new rule makes it unnecessary (a non-bare
pattern is a match whatever the type). Read `record/IA/elaborate-2026-10-13/opus-4.md` first.

Check: `PYTHONPATH=src python3 -m pytest tests/test_elaborate.py tests/test_run.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in a few lines to
`record/IA/elaborate-2026-10-13/report-5.md`.
