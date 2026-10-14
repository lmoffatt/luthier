# figures.lut: the fit's three plots rendered by experiment_zero.lut, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). Step 3 of
`record/plan/plots/plan-plots-2026-10-14-execution.md` (G4, G5 of the decisions); plot.lth with
the canvas (c6febf0), plots.py (1f5e0c6, `record/IA/plots-2026-10-15/report-host.md`: what
renders, the choices), `tests/run/plot_two_tables.lut` as the pattern of a program that builds
a `Plot` and renders it.

## The prompt

Read `CLAUDE.md` first, then the plan's G4 and G5, plot.lth §1 and §2 (the value and the
constructors), `tests/run/plot_two_tables.lut`, the host report's "Choices" (what each
geometry draws), and `examples/sonolocalizacion/experiment_zero.lut` (the three tables it
builds: positions with `x y sx sy` and `name`, residuals with `predicted`, `standardized`, `i j`,
the transform with `u`; `main`'s last actions; `outDir`). Other agents edit `arrays.lth`,
`tests/tester/arrays_laws.lut`, `src/luthier/*.py`: touch none; write
`examples/sonolocalizacion/figures.lut` (new) and change `experiment_zero.lut`, and add a
`test` program `tests/tester/figures_laws.lut` if the run needs entries beyond plot_laws.lut's.

1. `figures.lut`: three `Plot` values as pure functions of the fit's tables and a canvas (G4):
   (1) the positions in the plane: points at `x`, `y`, an ellipse from `sx`, `sy` at a level
   parameter, the name as text, equal aspect, metres on both axes; (2) the residuals:
   standardized residual against predicted distance, an abline at zero, points coloured by
   whether the pair touches A2 (a column the program computes from `i`, `j` and the node names,
   or a group column if simpler; say which); (3) the transform's quantile plot: `u` against the
   uniform quantiles (k/(n+1), computed in Luthier), with the Kolmogorov band as two ablines
   at ±D over the diagonal, D a parameter. Every cutoff (the ellipse's level, the band's D, the
   canvas) a parameter the program gives from a hole or a definition (P11), not a constant in
   figures.lut.
2. `experiment_zero.lut`: after writing the tables, `render` the three plots to `outDir/
   positions.png`, `residuals.png`, `transform.png` through `matplotlib : Renderer State`
   (plot_model.lut), the token threaded; the summary line unchanged.
3. Run the fit (`--set graphDir=examples/sonolocalizacion/A/graph_noA2 --set outDir=/tmp/figs
   --set lmMaxIter=500 --set lmTol=1e-6 --set lmFloor=5.995204332975845e-15 --fuel
   100000000000`, about 3 minutes, background): the three files exist; look at them (Read the
   PNGs) and say in one line each what they show and whether it is right (the positions should
   show mic1 at the origin, four mics on a 3.5 m circle, the speakers outside; the residuals
   within ±1.2 for noA2); if the run is refused for a law without an entry, say which and
   write the `test` lines that certify it on listed cases, certify, rerun. Then the slow test
   of the fit (`tests/test_run.py`, under LUTHIER_SLOW=1) checks the three files exist and
   their bytes are stable across two runs (`rendersTheSame`).
4. `luthier check` on both files (report what it refuses). Commit figures.lut and
   experiment_zero.lut each alone (`git add` the path; messages naming G4, G5; ending with
   "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"); copy the three PNGs to
   `record/runs/sonolocalizacion-2026-10-14/figures/` with a line in that README naming the
   command and the commit, and commit them (small files). The slow test change in
   `tests/test_run.py` stays uncommitted for the coordinator. Report in your final message.
