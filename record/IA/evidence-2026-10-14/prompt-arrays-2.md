# arrays.lth: PinvRestricts' slack scaled by the magnitudes, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). On the generator bite's report
(`record/IA/tester-2026-10-14/report-3.md`): `PinvRestricts` refuted 2/100 on full-rank PSD
matrices from the `gram` family (condition 4.6e4 and 3.4e3): `approxMatSlack` compares each
entry with a flat `tol (1 + |a| + |b|)`, and an entry near 0 carries rounding of cond × eps ×
|s|; its siblings `PinvProjects`, `PinvSymmetric`, `PinvScales` use the magnitude-scaled
`approxMatOf` since 7032d7b.

## The prompt

Read `CLAUDE.md` first, then that report's finding, `src/luthier/lib/arrays.lth` at
`PinvRestricts`, `approxMatSlack`, `approxMatOf`, `absMat`, `PsdAt`, and the comment of
7032d7b (`git show 7032d7b`), `docs/spec/11-*.md` 11.S14, D-2026-10-14-c. Other agents edit
`tests/tester/` programs for plots and `src/luthier/*.py`: change only `src/luthier/lib/arrays.lth`
and `tests/tester/arrays_laws.lut` (its PinvRestricts lines only).

State `PinvRestricts` with the comparison scaled as its siblings are (`approxMatOf tol scale`
with the scale `|s||p||s|` or the one 7032d7b's reasoning gives), `tol` still a parameter
(D-2026-10-14-c), citing 11.S14, [proposed]; keep `PsdAt` as the domain. Run
`PYTHONPATH=src python3 -m luthier.cli test tests/tester/arrays_laws.lut --no-cert --fuel
100000000` in the background (about 20 minutes) and paste the PinvRestricts lines (listed and
sampled) before and after. arrays.lth must parse and `luthier check` clean. Commit each file
alone (`git add` its path), messages naming the law and 11.S14, ending with "Co-Authored-By:
Claude Sonnet 5.5 <noreply@anthropic.com>". Report in your final message.
