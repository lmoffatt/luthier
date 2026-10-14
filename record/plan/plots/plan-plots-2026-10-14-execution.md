# Plots: the execution, 2026-10-14

For the sessions. The decisions are `plan-plots-2026-10-14-decisions.md` (G1 to G5); until
Luciano marks them, the recommendations are the defaults. Start only after the evidence bite
of the fit (`record/IA/evidence-2026-10-14/`) has landed and been read.

## Status

- 2026-10-14, 21:30: written; nothing started.
- 2026-10-15, 06:30: the certificates done (his priority), step 1 launched: plot.lth and
  plot_model.lut by an Opus agent (brief record/IA/plots-2026-10-15/prompt-theory.md).
- 2026-10-15, 07:45: step 1 done (470a4d5, bc25d58, bb11f0b; 15 proposed readings in the
  night plan's Questions). Step 2 launched (prompt-host.md): plots.py, the canvas as a field.
- 2026-10-15, 11:00: steps 2 and 3 done: plots.py (1f5e0c6, certified), figures.lut and
  experiment_zero.lut rendering the three plots (8e0ab62, fd498a9), the figures in
  record/runs/sonolocalizacion-2026-10-14/figures/. Step 4 (evidence on plot.lth's laws) partly:
  plot_laws.lut certifies Drawing's six laws on listed plots; `agreement` for the renderer not
  run. Open: label offsets or visible ellipses in the positions figure (the theory has no nudge).

## Steps

1. *A Fable or Opus agent, the theory.* `src/luthier/lib/plot.lth`: `Plot` as G2's record over
   tables.lth's `Table`, the geometries and scales as labeled sums, the pure constructors
   (`plot`, `point`, `line`, `errorbar`, `ellipse`, `text`, `scale`, `coord`, `facet`, `labels`),
   the laws of G3 (well-formedness, invariance), each citing its spec item or the plan's G-item
   (`-- plan G3`), Boolean with the cutoffs as parameters (D-2026-10-14-c). `plot_model.lut`: the
   renderer as a model of a theory `Renderer : { render : W -> Plot -> String -> W * Unit, ... }`
   stated in world.lth's style (§5's description and `agreement`), with the route
   `python:luthier.plots.render`. Must parse and `luthier check` clean. Brief:
   `record/IA/plots-2026-10-14/prompt.md` (to write from this plan; the pattern of a brief is
   any `prompt.md` under `record/IA/`).
2. *An Opus agent, the host.* `src/luthier/plots.py`: `render(w, plot, path)` drawing a `Plot`
   value crossed by its declared type (the bridge of run.py: records, lists, sums as `(label,
   value)`, tables) with matplotlib (Agg backend, no timestamps, `metadata={'Date': None}`) to
   PNG or SVG by the extension; `tests/test_plots.py`: a plot's bytes are a function of the
   value (two renders equal), each geometry drawn once. If matplotlib is not installed, say so
   and write SVG by hand for `point`, `line`, `text`, `ellipse`.
3. *An Opus agent, the examples.* `examples/sonolocalizacion/figures.lut` with G4's three plots
   from the fit's tables; `experiment_zero.lut` renders them to `outDir` after writing the
   tables; the slow test checks the three files exist and their hashes are stable across two
   runs.
4. Evidence: `test` lines on plot.lth's laws (the tester), the renderer's `agreement` at its
   first action when world.lth's protocol is implemented in run.py.

## If the session that reads this has no memory of the chat

The rules of a theory file and of a brief are in `record/plan/luthier-from-zero/
plan-from-zero-2026-10-13-execution.md`, "Rules for every step", and the state of Luthier in
`record/handoff-2026-10-14.md`. Luciano's words on plots are quoted at the top of the decisions
document; the pattern he named is ggplot's grammar of graphics (Wickham, *A layered grammar of
graphics*, 2010), made pure: a plot is a value, rendering an action.
