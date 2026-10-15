# The token sugar on an imported model's action, and 2.S18's wording, brief for an Opus agent

Read `CLAUDE.md`, `report-session.md` in this folder (findings 1 and 3), 2.S17 and 2.S18 in
`docs/spec/02-grammar.md`, translation.lth's `Blocks` (a bare name on `W * Unit` binds the token
and drops the unit), and `src/luthier/elaborate.py`'s block elaboration (bite 4 and 5 reports in
`record/IA/elaborate-2026-10-13/`). The bug: `w <- host.print w "x"` with `host` an imported
model binds `w` to the pair, so the next action fails "not the run's token at the crossing", in
`run` and in `session`; `(w, u) <- host.print w "x"` works. Likely the elaborator cannot infer
the action's type through the imported model's field and takes the `Let` branch. Fix at the
source (the type of a projection of a model typed by an imported theory), with a test in
test_elaborate.py and a run program under tests/run/ using `w <- host.print w "x"` twice. Then
2.S18's stale sentences (cli.py has no session; the world waits for actions): rewrite to what is
true, one commit of the chapter alone. Change elaborate.py, tests, the chapter; Python
uncommitted. Report with a shell heredoc to `report-sugar.md` here, committed alone. Accepted
when: the suite passes; the run program prints both lines; `check_spec.py` prints nothing.
