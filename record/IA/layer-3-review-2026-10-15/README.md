# External review of layer 3 (world and certification), round 1

Frozen at commit 055589c (see `FROZEN`; the files reviewed are `src/luthier/lib/world.lth`,
`world_model.lut`, `certification.lth`, `certification_model.lut`, `docs/spec/10-world.md`,
`docs/spec/06-certification.md`, none changed by the assembly).

Paste `A-prompt.md` (one self-contained paste, everything inlined) to four models on the web:
GPT, DeepSeek, Claude, Kimi.

The replies go to `A/<model>.md`, verbatim; the coordinator commits them after Luciano downloads
them. The synthesis comes after, as for layers 0-1 (`record/IA/layers-0-1-review-2026-10-13/summary.md`).

Made by `freeze.py` (inputs: the files above, `docs/principles.md`, `record/decisions.md`; head
text in `A-head.md`; no parameters, no seed).

## Round 1, bundles B, C and D

Three more single-paste prompts, frozen at commit 2710cfc (`FROZEN-BCD`), same nine questions as
A with question 9 changed per bundle, same four models (GPT, DeepSeek, Claude, Kimi):

- `B-prompt.md` (13,449 words): demand and plan (`demand.lth`, `plan.lth`, their models,
  `docs/spec/08-demand.md`). Question 9: what law is missing for `run`'s record and key to
  identify a result (8.S8, 12.S18). Replies to `B/<model>.md`.
- `C-prompt.md` (23,384 words): generators, test, laws (`generators.lth`, `test.lth`, `laws.lth`,
  the two models, `docs/spec/07-tests.md`, `05-laws.md`). Question 9: which generator is missing
  for a sampled law that today runs on listed cases only (7.R1, 7.R4). Replies to `C/<model>.md`.
- `D-prompt.md` (20,811 words): `probability.lth`, `belief.lth`, `optimization.lth` with their
  models, `arrays.lth` whole, and `examples/sonolocalizacion/experiment_zero.lut`; 11 section 2
  and 6.S16 as context. Question 9: what law is missing for the host's maximizer to be certified
  beyond the quadratic family. Replies to `D/<model>.md`.

Replies verbatim, committed by the coordinator after Luciano downloads them; syntheses after.
`freeze.py` now takes the bundles to build (default B C D; naming A would re-freeze A at HEAD);
head texts in `B-head.md`, `C-head.md`, `D-head.md`.
