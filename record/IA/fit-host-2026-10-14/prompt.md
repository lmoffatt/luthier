# The fit's host side: lm.py and pinv_sym_at in this repository, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). On the fit theories' report
(`record/IA/slice-theories-2-2026-10-14/report.md`, sections "What the bridge and lm.py's
successor must do" and the `[proposed]` items 1, 6 to 9).

## The prompt

Read `CLAUDE.md` first, then that report's two sections whole, then `src/luthier/lib/belief.lth`
(§2: `Settings`, `MaxResult`, `decrement`, `Maximizer`'s laws), `optimization.lth` (§2, §3:
`Damping`, `LMState`, `dampedStep`, `lmStep`, `LMStep`'s laws), `belief_model.lut`,
`optimization_model.lut`, `arrays_model.lut` (the routes), and, read only, sonolocalización's
`/home/lmoffatt/Projects/sonolocalizacion/src/lm.py` (the Levenberg-Marquardt to succeed; change
nothing there). Another agent ports the slice's `.lut` files to `examples/sonolocalizacion/`
meanwhile: change only `src/luthier/lm.py` (new), `src/luthier/arrays.py` (add `pinv_sym_at`
only), `tests/test_lm.py` (new), and if the bridge lacks a case the report names (a Python bool
read at `Bool` never an int; `Settings` by attribute or key; a `List (Vec Float64)` as a list of
ndarrays) `src/luthier/run.py` with a test in `tests/test_run.py`, saying so.

Write `src/luthier/lm.py` as the report specifies: `damped_step(n, settings, o, x, mu)`,
`step(n, settings, damping, o, s)`, `decrement(settings, o, x)`, `finished(settings, damping, o,
s)`, `maximize(settings, n, f, g, m, x0)`, with `pinv_sym_at(floor, a)` in arrays.py (eigh,
keep `w > floor * max|w|`, none when empty), the decrement by the same leaf and formula as
belief.lth's `decrement` so that `MaximizerStationary` holds exactly where the host stops; the
module's damping (0.001, 3.0, 1e-15, 1e15) as its own values ([proposed] 9). `tests/test_lm.py`:
the concave quadratic `quadratic n b c` of belief.lth converges to its maximum from a start, with
the decrement at or under `tol` at the end (`QuadraticConverges`); `damped_step` descends
(`DirectionDescends`) on it; a step on a quadratic is accepted (`QuadraticStepAccepts`); and one
run through `luthier run` of a small program under `tests/run/` that imports `belief_model.lut
lm : Maximizer` and maximizes a quadratic through the callback crossing (run.py bite 8,
`record/IA/run-2026-10-13/report-8.md`), printing the maximum and reading the callback counts
in `x.run.json`. Then `luthier test` on `belief_model.lut` and `optimization_model.lut` if they
carry `test` lines (if not, say so; do not write theory files).

Check: `PYTHONPATH=src python3 -m pytest tests/test_lm.py tests/test_run.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message: what
runs, each law met and how, every choice the theory left open.
