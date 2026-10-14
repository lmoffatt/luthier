# plot.lth and plot_model.lut: a plot as a pure value, rendering an action, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). Step 1 of
`record/plan/plots/plan-plots-2026-10-14-execution.md`; the decisions (G1 to G5, the night's
defaults until Luciano marks them) in `plan-plots-2026-10-14-decisions.md`, with his words at
the top. Read both whole first.

## The prompt

Read `CLAUDE.md`, the two plan documents, `docs/principles.md` (P10, P11, L2.7, L7), then the
pattern of a theory with a host model: `src/luthier/lib/world.lth` §3 to §5 (externs as routes,
a host action, `agreement`) with `world_model.lut`, `tables.lth` with `tables_model.lut` (a
record with a codec as the host's model), `arrays.lth` at `Vec`, `Mat`, and D-2026-10-14-c
(`record/decisions.md`, end: Boolean laws, cutoffs as parameters). Another Sonnet edits
`certify.py` and the stores: touch no `.py`. Write `src/luthier/lib/plot.lth` and
`plot_model.lut`, one commit each (`git add` its path; never `-A` or `.`; messages naming G1 to
G5 and the spec items, ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>").

plot.lth, in the syntax the parser takes (`PYTHONPATH=src python3 -m luthier.cli parse FILE`):
- G2's `Plot` record over tables.lth's `Table`: the data (one or more tables, named), the
  mapping (aesthetic to column name: x, y, colour, size, group, label), the layers (a list; each
  a geometry as a labeled sum: `point`, `line`, `errorbar`, `ellipse`, `text`, `segment`, with
  the parameters each needs, over a mapping and a table's name), the scales (per aesthetic: a
  labeled sum `linear`, `log`, `palette`, with limits as parameters, P11), the coordinates
  (`cartesian`, `equal`), the facets (`Maybe` a column), the labels (title, axes). Every list
  a `List`, every kind a labeled sum, so a new geometry or scale is a new label (G2).
- The pure constructors: `plot t`, `point m`, `line m`, `errorbar m`, `ellipse m`, `text m`,
  `segment m`, `scale a s`, `coord c`, `facet col`, `labels ...`, each `Plot -> Plot`, so they
  compose as ggplot's `+` (G2); cite G2 above each.
- G3's laws, Boolean with cutoffs as parameters: well-formedness (every aesthetic of a layer
  names a column of its table of the kind the geometry asks: `hasColumn`, `kinds` of
  tables.lth); a scale's limits contain the data or are stated (a parameter); invariance under
  the order of rows not ordered by a layer and under a permutation of non-overlapping layers
  (state what "the same plot" means: structural `==` on the value, 4.R8); each citing G3 and the
  spec item, `[proposed]` where you read beyond the plan.
- The theory `Renderer` in world.lth's style: `render : W -> Plot -> String -> W * Unit` (G1,
  10.S3), with its description (what places it changes: the file at the path) and the laws of
  G3's rendering: the file exists after, its format by the extension, its bytes a function of
  the plot's value and the renderer's version (deterministic: two renders of one value give
  the same bytes), stated the way world.lth states `Host`'s actions and `agreement`.
plot_model.lut: `matplotlib : Renderer` with the route `python:luthier.plots.render` (the host
module does not exist yet; step 2 writes it) and what crosses (the `Plot` record by its
declared type, as tables cross), and the three plots of G4 as values if they fit in a model file
(else leave them for `examples/sonolocalizacion/figures.lut`, step 3, and say so).
Both files must parse and `luthier check` clean (report what it refuses if not yours). Report in
your final message: what is stated, every `[proposed]`, and what `plots.py` must do per law.
