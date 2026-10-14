# The port of experiment_zero.lut, positions.lut and distances.lut: brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). After the first port
(`record/IA/slice-port-2026-10-14/report.md`: validate_graph.lut, distance_graph.lut,
positions_slice.lut at `examples/sonolocalizacion/`) and the fit's theories
(`record/IA/slice-theories-2-2026-10-14/report.md`, its last section "For the port of
experiment_zero.lut": read it whole, it lists every rename and every change beyond a rename).

## The prompt

Read `CLAUDE.md` first, then the two reports named, the first port's three files, and the
theories `probability.lth`, `belief.lth`, `optimization.lth` with their models and `arrays.lth`
(at the names the report lists). The sources, read only (change nothing there):
`/home/lmoffatt/Projects/sonolocalizacion/prototipo-cero/luthier/experiment_zero.lut`,
`positions.lut`, `distances.lut`, and `src/distance_graph.py` lines 238-284 for what
`nodeNames`, `positionsTable`, `residualsTable`, `transformTable`, `writeTable` did. Another
agent writes `src/luthier/lm.py` meanwhile; `src/luthier/*.py` and `tests/` are not yours.

Write under `examples/sonolocalizacion/`: `positions.lut` (the whole of v0.1's positions.lut over
the new arrays, absorbing `positions_slice.lut`, which you delete, updating distance_graph.lut's
and validate_graph.lut's imports), `distances.lut` (the likelihoods over `Likelihood n` as the
report says), `experiment_zero.lut` (the fit: the prior as a `GaussianBelief`, `laplaceMode`
through `lm : Maximizer` and `runSettings` with `lmTol`, `lmMaxIter`, `lmFloor` as holes filled
by `--set` (run bite 7, `record/IA/run-2026-10-13/report-7.md`), the Laplace posterior, the
residuals, the transform tail; `main (w : W) : W * Unit` printing the summary line v0.1 printed
and writing the three tables as actions: `writeTable` becomes `host.writeFile` of
`csv.render` (tables_model.lut) at paths under `outDir`, a hole; if `host` has no write action in
`world_model.lut`, write the tables' text to stdout with a header line each and say so; the two
control entries `priorWidened` and `sigmaKnown` as further `main`-like actions reachable by `run
--main`). Keep every v0.1 name the theories keep. Each file must parse (`PYTHONPATH=src python3 -m
luthier.cli parse`) and `luthier check` on each (report what it refuses, do not fix check.py).
Then try `PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/experiment_zero.lut
--set graphDir=examples/sonolocalizacion/A/graph --set outDir=/tmp/... --set lmTol=... --set
lmMaxIter=500 --set lmFloor=...` (values from v0.1's experiment_zero.lut) in the background: it
needs `src/luthier/lm.py`, which the other agent writes; if the run stops on its absence or on
anything else, report exactly where with the smallest program; if it finishes, paste the summary
line and the wall time, and copy the three output tables' first lines. Commit your files as done,
one commit each (`git add` the path; never `-A` or `.`; messages naming the spec items, ending
with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). Report to
`record/IA/slice-port-2-2026-10-14/report.md` (commit it): renames, more than renames, readings,
what stopped the run.
