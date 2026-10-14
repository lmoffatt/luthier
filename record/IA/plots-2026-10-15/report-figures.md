# figures.lut, the fit's three plots: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-figures.md; saved by the
coordinator. Commits by the agent: 8e0ab62 figures.lut (`positionsPlot`, `residualsPlot`,
`transformPlot`, pure functions of the tables, a `Canvas`, a `Style` record and each plot's
criterion: the ellipse level, the highlighted node with its palette, the band's half-width;
no constant in the file, P11); fd498a9 experiment_zero.lut (the three renders after the
tables; the summary line last; `outDir` must exist); 8a6fd7f the three PNGs under
record/runs/sonolocalizacion-2026-10-14/figures/ with the command and commits. Committed by
the coordinator: `tests/test_run.py`'s `test_fit_renders_its_figures_slow` (two runs, the
three PNGs byte-equal, 6 min).

The parameters experiment_zero.lut gives, all proposed: canvas 6×5 in at 100 dpi; point 5 pt,
text 7 pt, line 1 pt, expand 0.08; ellipse level 2.0 posterior sds; highlighted node
"parlante_A2" with palette ["#0072B2", "#D55E00"]; band level 0.05 with D = sqrt(−ln(α/2)/2) /
(√n + 0.12 + 0.11/√n), Kolmogorov's first term with Stephens's correction as in `transformTail`
(D = 0.30 for n = 19). The residuals' colour is a computed column `pair` ("touches <node>" or
"other") from the node names at `i`, `j`; the quantile plot uses the kept transforms (leverage
< 1), the quantile (rank + 1)/(n + 1) computed in Luthier, axes stated at [0, 1], equal aspect.

The run: refused in the main tree ("numpy: PinvRestricts: stale", arrays.lth changed under
another agent), so run in a worktree at 325a709: 3 min, the cone served; sigma 0.022143 m, nu
4.4711, Kolmogorov 0.17285 over 19, tail 0.579. Figures: positions.png, mic1 at the origin,
mic2 to mic5 on the 3.5 m circle, A1 inside at (1.38, −1.17), A3 and A4 at (−2.6, 7.6)
overlapping (they differ in z only), A5 at (−9.5, −15.2); the 2-sd ellipses (≤ 0.22 m) hidden
by the markers at this scale; names drawn centred on the points. residuals.png: all within
±1.2 (max 1.16, min −1.01), one colour (no A2 in this graph). transform.png: the 19 u values
near the diagonal, inside the ±0.30 band.

Findings: (1) a scope bug in the loader or the checker: a top-level definition in an imported
file captures a `match` binder of the same name in the importer even when not in the import
list (`kept`; renamed `keptRow`; minimal repro in the agent's report: a.lut defines `kept`,
b.lut imports `other` from it and matches on `kept`, refused by 4.R9): the same family as the
cone-hash finding of plots.py's report. (2) The positions figure needs label offsets or
visible ellipses; the theory has no nudge.
