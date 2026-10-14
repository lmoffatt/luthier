# plots.py, the renderer: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-host.md; saved by the coordinator.
Commits by the agent: c6febf0 plot.lth (`Canvas`, `CanvasPositive`, `plot cv name t m`, every
constructor carrying the canvas, `samePlot` comparing it; [proposed]); 8cd67aa plot_model.lut
(header). Files committed by the coordinator with this report: `src/luthier/plots.py` (new),
`src/luthier/host.py` (files read as bytes: UTF-8 decoded as text with universal newlines, else
latin-1), `tests/test_plots.py` (25 tests), `tests/run/plot_two_tables.lut`,
`tests/tester/plot_laws.lut`, the stores `src/luthier/lib/plot_model.cert.json` and
`world_model.cert.json` (a binding of `S` to `State` writes Drawing's entries there too).
Checks: test_plots and test_run 105 passed; the suite 639 passed.

What renders: matplotlib 3.11.1, a bare `Figure`, Agg for PNG, the SVG backend for SVG,
constrained layout; all seven geometries, log scales, equal aspect, facet panels; `image`,
`format_of`, `render` (refuses outside png/svg, writes nothing then), `version()`.
`luthier run tests/run/plot_two_tables.lut` builds a Plot of two CSV tables in Luthier and
writes plot.png and plot.svg, byte-equal to plots.py's own drawing of the same plot; certified
(`plot_laws.lut`: the six Drawing laws on `matplotlibDrawing` and Persistence's two on `files`
at grade cases, four listed plots, six row permutations, margin 0.05).

Each law met: `wellFormed` evaluated in order, `NotWellFormed` naming the law; axes at
`resolved_limits` with autoscale off; determinism by `rcdefaults` in `rc_context`, a fixed
`svg.hashsalt`, DejaVu Sans, text as paths, no Date, no Software tag; rows sorted by mapped
values (lines by group, colour, x), levels, legend entries and panels sorted; layers at
z-order 2+i, the legend independent of layer order (the PNG identical after a swap, the SVG
differs as §5 expects); the title always drawn; `format_of` by signature; the file read back by
`host.observe` equals `image`.

Choices of the agent: unmapped colour and ablines black; colours over the union of levels
across layers (`PaletteCoversLevels` counts per layer: proposal to state it over the union);
facets in a grid of ceil(√n) columns; the legend outside upper right; supxlabel/supylabel; an
abline on a log axis sampled once per pixel column; no caps on error bars; scatter with size²;
text centred; labels as repr; the renderer's version in the image and in `plots.version()`,
not yet in run.py's record.

Findings: (1) name collisions change cone hashes: importing plot.lth's `text` (the name of
`Cell`'s label) into the run program changed csv's cone hash and its entries read stale (the
program uses `addLayer` and `texts` instead); defining `apart` in plot_laws.lut (plot.lth has
one) made LayerOrderInvariant's entries stale (renamed `apartLayers`): the cone hash depends on
the names the importer brings in, for the certifier. (2) The run test depends on the stores
(committed now).
