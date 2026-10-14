# plots.py, the renderer as the model of plot.lth's Drawing and Renderer, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). Step 2 of
`record/plan/plots/plan-plots-2026-10-14-execution.md`, on plot.lth and plot_model.lut
(470a4d5, bc25d58, bb11f0b; the theory agent's report in `record/plan/night-2026-10-13.md` at
07:40 and its section "What plots.py must do, per law", copied below).

## The prompt

Read `CLAUDE.md` first, then `src/luthier/lib/plot.lth` whole (§1 the value, §3 reading a
plot: `aesOf`, the ranges, `resolvedLimits`; §4 the laws; §5 `Drawing`, `drawn`, the six laws;
§6 `renderAgrees`, `rendersTheSame`), `plot_model.lut`, `src/luthier/run.py` at the crossing of
records, sums (`(label, value)`), lists and tables (`report-4.md`), `src/luthier/host.py`
(`observe`, `read_file`: a binary file read as latin-1 for `agreement`), `tables.py` (`as_table`,
cells). Another Opus edits `tester.py`, `generators_model.lut`, `arrays.py` and `tests/tester/`:
touch none. Change `src/luthier/plots.py` (new), `src/luthier/host.py` (binary read only),
`tests/test_plots.py` (new), programs under `tests/run/`, and `src/luthier/lib/plot.lth` for one
thing only: the canvas.

0. The canvas (the theory agent's open item, P11): add to `Plot` a field `canvas : Canvas`
   with `Canvas = { width : Float64, height : Float64, dpi : Float64 }` in inches and dots, a
   law `CanvasPositive`, and `plot` taking the canvas as its first argument (no default: the
   demand states it); update the constructors and plot_model.lut if they build a `Plot`; one
   commit of plot.lth and one of plot_model.lut by their paths, [proposed], messages ending
   "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; both must parse and `luthier
   check` clean.
1. `src/luthier/plots.py` with matplotlib (Agg for png, the SVG backend for svg; if matplotlib
   is not installed say so and write SVG by hand for points, lines, texts, ellipses, ablines):
   `image(plot, ext)` the bytes as a latin-1 string; `format_of(content)`; `render(w, plot,
   path)` writing exactly `image(plot, ext)` and returning `(w, unit)`, refusing an extension
   outside png and svg; matplotlib's version reported for the record. Meet each law as the
   theory agent listed: refuse a plot that is not `wellFormed` (the inheritance rule of
   `aesOf`); axes exactly at `resolvedLimits` (no autoscale, no margins); no timestamps
   (`metadata={'Date': None}`, a fixed `svg.hashsalt`, `rcdefaults` in a context, fixed fonts);
   rows drawn in canonical order (sorted by mapped values; `lines` by group, colour, x; colour
   levels, legend entries and facet panels in sorted order); layers in list order; the title
   always drawn.
2. `tests/test_plots.py`: two renders of one value give the same bytes (`ImageOfTheValue`,
   `rendersTheSame`); a row permutation gives the same bytes (`RowOrderInvariant`); swapping
   two non-overlapping layers gives the same PNG (`LayerOrderInvariant`, png only); a changed
   title changes the bytes (`ImageSeesTheTitle`); `format_of` on both outputs; a plot that is
   not well formed is refused with the law's name. One program under `tests/run/` building a
   `Plot` of two tables in Luthier (a small CSV written by the test, parsed by `csv`) with
   points, a line and a text, rendered through `luthier run` to png and svg in a temp directory
   (the run reads the model's store: if `matplotlib : Renderer` has laws without entries, the
   run is refused: then say so, and write the `test` lines that certify `Drawing`'s laws on
   listed plots in `tests/tester/plot_laws.lut`, certify it, and run).

Check: `PYTHONPATH=src python3 -m pytest tests/test_plots.py tests/test_run.py -q`, then the
suite. Do not commit the Python or the stores (the coordinator does). Report in your final
message: what renders, each law met and how, every choice the theory left open.
