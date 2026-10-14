# The external review of layer 3, round 1: assemble the prompt, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e), on Luciano's word ("sí, dale"):
one round of external reviewers (GPT, DeepSeek, Claude, Kimi on the web) per layer, as
D-2026-10-13-r and the execution plan say; layers 0 and 1 had theirs
(`record/IA/layers-0-1-review-2026-10-13/`). He pastes one prompt per model and downloads the
replies himself; the prompt must be one paste, small bites for the web.

## The prompt

Read `CLAUDE.md` first, then `record/IA/layers-0-1-review-2026-10-13/intro.md`, `A-prompt.md`,
`freeze.py` (how the files were frozen at a commit and inlined or attached) and `summary.md`
(what such a round found). Change nothing outside `record/IA/layer-3-review-2026-10-15/`.

Produce, by the same mechanism (reuse or copy `freeze.py`; if it inlines files, inline; if it
writes a directory to attach, write it), the round's material at the current commit:
1. `A-prompt.md`: the prompt to paste, in English, with the same seven questions as the
   layers 0-1 round (laws false of the intended model or unsatisfiable together; laws that do
   not determine what they claim, with the wrong model that passes; constructors of a `data`
   with no law of their role, L2.7; the models against their theories, with the case; where a
   file says other than its chapter or a cited decision; laws stated over a type with an
   implication a random case rarely meets instead of the subtype; what you would change first,
   one thing) plus two of this round: (8) a cutoff written as a constant where it should be a
   parameter the demand supplies (D-2026-10-14-c, stated in the prompt in one sentence); (9)
   what law is missing for the host to be certified against its description (world.lth §5's
   `agreement` and `Host`). The artifact: `src/luthier/lib/world.lth`, `world_model.lut`,
   `certification.lth`, `certification_model.lut`, and the two chapters they realize,
   `docs/spec/10-world.md` and `06-certification.md`, plus the principles' terms the prompt needs
   (`docs/principles.md`: only L2.7, L9.6, L10, L11, P11, as the old intro did). Ask for the
   answer per file, numbered, quoting the line; a claim the reviewer cannot verify in a "not
   sure" list; no rewriting.
2. A short `README.md` in the folder: the commit frozen, the four models to paste to, where
   the replies go (`A/<model>.md`, verbatim, committed by the coordinator after Luciano downloads
   them), and that the synthesis comes after.
3. Keep the paste under what a web model takes in one turn (if the inlined artifact exceeds
   about 60,000 words, split into two prompts, world and certification, as `A-prompt-world.md`
   and `A-prompt-certification.md`, each self-contained with the questions).
Commit the folder's files (`git add` the paths; message ending "Co-Authored-By: Claude Sonnet
5.5 <noreply@anthropic.com>"). Report in your final message: the files, their sizes in words,
the commit frozen.
