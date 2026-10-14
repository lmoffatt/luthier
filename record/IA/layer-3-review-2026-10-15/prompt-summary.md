# The external review of layer 3, round 1: the synthesis, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). The replies of GPT, DeepSeek,
Perplexity (a PDF, its text extracted), Grok and Kimi are under `A/`, verbatim; Claude's (Fable
on the web) is pending and is added by a second pass when it lands. The pattern is
`record/IA/layers-0-1-review-2026-10-13/summary.md` and `reply.md`.

## The prompt

Read `CLAUDE.md` first, then `README.md` and `A-prompt.md` of this folder (the nine questions
and the artifact frozen at the commit in `FROZEN`), the five replies under `A/`, and the
layers 0-1 round's `summary.md` for the form. Then the artifact as it is now (`git diff
<FROZEN>..HEAD -- src/luthier/lib/world.lth world_model.lut certification.lth
certification_model.lut`: some findings may already be fixed). Write `summary.md` in this
folder: per file, the findings numbered, each with the models that raised it (a finding raised
by three or more models first), the line quoted, verified by you against the file (a claim you
cannot verify goes to a "not sure" list with the model), whether it is already fixed at HEAD,
and your reading of whose it is (the theory's, the model's, the specimen's, the
specification's, or a reviewer's misreading, with why); then one screen for Luciano at the
top: the five things to change first, by agreement and weight, and the contradictions between
models. Do not rewrite the files. Commit `summary.md` alone (`git add` its path; message ending
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). Report in your final message the
top screen.
