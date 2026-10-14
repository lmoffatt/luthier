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
