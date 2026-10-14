# After tables_laws.lut: a host list of strings crosses as a value; RoundTrip's domain, brief

Written 2026-10-15 by the coordinating session (luthier-3e). On the tables evidence (450b0d8;
the Sonnet's report in `record/plan/night-2026-10-13.md` at 01:50): `RoundTrip` refuted on a
table with no columns (`render` gives "" and `parse` rejects "no header"); `Canonical`, `Tolerant`
and `RoundTrip` on any nonempty table unsettled because a host table's `names` and `kinds` cross
as `axiom "shared"`, so `sameTable`'s `t.names == u.names` is not a Bool.

## The prompt

Read `CLAUDE.md` first, then that report (the night plan's line and
`tests/tester/tables_laws.lut`), `src/luthier/run.py` at the crossing of a host record read by
attribute (`HostRecord`, bite 4's `report-4.md` item 3: a host `Table` back as the record `{
nRows, names, kinds, cell }`) and of `List String` from the host (`from_host`, the typed `List`
path), `src/luthier/lib/tables.lth` at `Table`, `sameTable`, `RoundTrip`, `Codec`. Nobody else
edits now: change `src/luthier/run.py`, `tests/test_run.py`, `src/luthier/lib/tables.lth` (one
law's domain), `tests/tester/tables_laws.lut`.

1. A host table read back as the record crosses its `names` and `kinds` as Luthier lists of
   strings (`cons`/`nil` of `StringConst`) by the declared type `List String`, not as an opaque
   shared host value; `==` on them then steps (kernel bite 10). Test in `tests/test_run.py`: a
   program printing whether two parsed tables have the same `names`. Then `luthier test
   tests/tester/tables_laws.lut --no-cert` (a minute): `Canonical` and `Tolerant` settle; paste
   the lines.
2. `RoundTrip` on a table with no columns: the codec cannot render a header for an empty
   schema. State `RoundTrip` over tables with at least one column (a subtype `WithColumns`, or
   the premise `nCols t > 0` inside the law), marked [proposed] with 12.S23 cited, and keep
   `noColumns` in the census so the law's domain is visible; or, if tables.lth's author would
   rather have `render` of an empty schema be an empty header that `parse` accepts, say why you
   did not take it. The file must parse and `luthier check` clean.
3. Commit tables.lth and tables_laws.lut each alone (`git add` the path; messages naming the
   laws; ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"); run.py and
   its test are not committed (the coordinator reviews).

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, then `PYTHONPATH=src python3 -m
pytest tests -q`. Report in your final message.
