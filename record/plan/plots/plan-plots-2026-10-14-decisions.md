# Plots: the decisions, 2026-10-14

Written by Claude Fable 5.1 (luthier-3e, the coordinator) on Luciano's word of 2026-10-14
evening: "generar gráficos que representen los datos. Tratá de hacer una teoría simple pero que
luego se pueda extender ... Un patrón posible es el de ggplot pero, claro, puro ... los gráficos
solo después de terminar lo otro". Each item below is a decision for him, with the
recommendation first; the execution is `plan-plots-2026-10-14-execution.md`. Until he marks
them, the recommendations are the night's defaults, each one commit to undo.

## G1. A plot is a value, rendering is an action

A plot is a pure value of a theory `Plot` (P10: the object is the invariant of its type), built
from a table and a mapping, with no side effect: it can be quoted, hashed, compared and
certified like any value (L7, 6.S8). Rendering it to a file or a screen is an action of the
world (10.S3): `render (w : W) (p : Plot) (path : String) : W * Unit`, a host leaf (matplotlib
or an SVG writer in `src/luthier/plots.py`, P7) reached as every extern is (3.S40). What the
laws certify is the value; what the host draws is validated against the value's description
at its first action (10.S8 to 10.S10), as `print` is in world.lth §5.

Recommended: yes. Alternative: a plot as an action from the start (what v0.1's figures did in
Python), which cannot be a law's subject.

## G2. The grammar: ggplot's layers, pure

A `Plot` is a record: the data (a `Table` of tables.lth, or several), the aesthetic mapping
(which column gives x, y, colour, size, group: names of columns, checked against the table's
schema by a law), the layers (each a geometry applied to a mapping and a table: `point`,
`line`, `errorbar`, `ellipse`, `text`, `segment`), the scales (per aesthetic, a map from data
to the drawing: linear, log, a palette for colours, with their limits as parameters, P11), the
coordinates (cartesian, equal aspect for positions in metres), the facets (a column that splits
the panels), the labels. Adding a layer or a scale is a pure function `Plot -> Plot`, so that
`plot t |> point x y |> errorbar ...` composes as ggplot's `+` does.

Recommended: this, at its smallest for the first plots (G4), with the record extensible
(every list a `List`, every kind a labeled sum, so a new geometry or scale is a new label and
one model, not a change of type). Alternative: a fixed set of plot kinds (`scatter`, `lines`),
simpler now, not extensible.

## G3. What the laws say

- Well-formedness: every aesthetic names a column of its layer's table, of the kind the
  geometry asks (a number for x, y; any for colour, group); a scale's limits contain the data
  or are stated by the demand (P11).
- Invariance: a plot's value does not depend on the order of rows that are not ordered by a
  layer (`line` orders by x); a plot is the same under a permutation of its layers that do not
  overlap (a role law of the layers, L2.7).
- Rendering (the host's description, 10.S10): the file exists after `render`, its format is
  what the path's extension says, and the file's bytes are a function of the plot's value and
  the renderer's version alone (the hash recorded in the run's record, 12.S18, P2); a second
  render of the same value gives the same bytes (deterministic rendering: matplotlib with a
  fixed backend and no timestamps).

Recommended: these three, Boolean with their cutoffs as parameters (D-2026-10-14-c).

## G4. The first plots, from the fit

From `experiment_zero.lut`'s three tables, as its last action: (1) the positions in the plane
with their uncertainty (points at `x`, `y`; an ellipse from `sx`, `sy`; the name as text;
equal aspect); (2) the residuals (standardized residual against predicted distance, a
horizontal line at zero, points coloured by whether the pair touches A2); (3) the transform's
quantile plot (`u` against the uniform quantiles, with the Kolmogorov band). Each a `Plot`
value written to `outDir` by `render`.

Recommended: the three, (1) first. Alternative: only (1) until the theory settles.

## G5. Where the plots live

`src/luthier/lib/plot.lth` with `plot_model.lut` (the host renderer as the model) in the
library; the three plots of G4 in `examples/sonolocalizacion/figures.lut`, imported by
`experiment_zero.lut`; the host code `src/luthier/plots.py`. The port of sonolocalización's
Python figures (its `analisis/*_plots.py`) is not in scope: those are stages Luthier does not
run (inventory §1).

Recommended: this layout. Alternative: the plots inside experiment_zero.lut.
