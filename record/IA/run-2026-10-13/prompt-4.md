# run.py bite 4: arrays, tables and Maybe across the bridge, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). After host bite 3 (044297c) and the
slice's theories (report `record/IA/slice-theories-2026-10-14/report.md`, section "What the
kernel and the bridge must do", "Bridge" part: read it first, then `arrays.lth`,
`arrays_model.lut`, `tables.lth`, `tables_model.lut`, and spec 3.S22 to 3.S26, 11.S6, 11.S8, 11.S9).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (on kernel.py and cli.py, and on
theory files): change only `src/luthier/run.py`, `src/luthier/host.py`, `src/luthier/arrays.py`,
`src/luthier/tables.py` (host code kept from v0.1: read before changing, add only what the report
names, `retained_rank_at(floor, a)`), `tests/test_run.py`, programs under `tests/run/`, and write
your report; a failure from another file is someone else's.

Make the bridge of run.py carry: (1) `Vec Float64` as the record `{ n, f }` to a one-dimensional
float64 ndarray (f materialized over `Fin n`, each entry once, 3.S25) and back (an ndarray becomes
`{ n := shape, f := <host object indexed with the bounds check of 3.S22> }`); `Mat Float64` as `{
m, n, f }` likewise; `Fin n -> Float64` and `Fin n -> Int` alone as in 11.S9 and 11.S8; (2)
`Float64` as a Python float (an int with an exact double promoted; NaN or inf an error) and `Int`
as an int never a bool; (3) `Table` as the record `{ nRows, names, kinds, cell }` the way
`tables.py`'s `as_table` reads it, and a host `Table` back as that record with `cell` giving
`nothing` or `just (int k)` / `just (real x)` / `just (text s)`; `Maybe Table` from `parse`; (4)
externs inside record values (`numpy.matMul`, `csv.parse`, `elementary.sqrt` of the models) read
when the projection is applied (3.S40). A test program per item in `tests/run/` run through
`luthier run` (a vector's norm through `numpy`, a matrix product, a table's cell read through
`csv.parse` on a small CSV the test writes), with the expected printed line; the kernel may lack
Float64 `*`, `/` and `sqrt` until kernel bite 9 lands in parallel: write the tests so they need
only what exists, or mark the ones that wait for it with the reason.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, `PYTHONPATH=src python3 -m
luthier.cli run examples/hello.lut`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not
commit. Report in a few lines to `record/IA/run-2026-10-13/report-4.md`: what crosses and how,
every choice the spec left open.
