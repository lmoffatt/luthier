# The external review, bundles B, C and D: one synthesis, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e), on Luciano's word ("quizás que
analicen todo junto"). The replies are under `B/` (demand, plan), `C/` (generators, test,
laws), `D/` (the fit's theories: probability, belief, optimization, arrays, experiment_zero),
one file per model, verbatim; Perplexity's from its PDFs; Claude's (fable.md) where present.
The pattern and the form: `summary.md` of this folder (bundle A's synthesis) and
`prompt-summary.md`.

## The prompt

Read `CLAUDE.md`, `prompt-summary.md`, `summary.md` (the form), the three heads (`B-head.md`,
`C-head.md`, `D-head.md`: the artifact and question 9 of each), then every reply under `B/`,
`C/`, `D/`. Verify each finding against the file at the lines it quotes (the frozen commit is in
`FROZEN-BCD`; `git diff <that>..HEAD -- <file>` says whether it is already fixed). Write
`summary-BCD.md` through the shell (the Write tool refuses report files): one top screen for
Luciano over the three bundles (the five things to change first by agreement and weight, the
contradictions between models), then one section per bundle in the form of `summary.md`
(per file, numbered findings with the models, the line quoted, verified, whose it is), a
"not sure" list. No rewriting of the files. Commit `summary-BCD.md` alone ("Co-Authored-By:
Claude Opus 5.5 <noreply@anthropic.com>"). Accepted when: the file exists with the three
sections and the top screen, every finding names its models and its line, and the final
message carries the top screen only.
