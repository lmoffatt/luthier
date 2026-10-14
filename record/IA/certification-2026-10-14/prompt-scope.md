# Two scope findings: a match binder captured by an import; the cone hash and the importer's names

Written 2026-10-15 by the coordinating session (luthier-3e). From plots.py's report
(`record/IA/plots-2026-10-15/report-host.md`, finding 1) and figures.lut's
(`report-figures.md`, finding 1).

## The prompt

Read `CLAUDE.md` first, then those two findings, then `src/luthier/check.py` (`load_imports`,
`_brought`, the typing with imports: bite 5 and 10, `report-5.md`, `report-10.md`),
`src/luthier/run.py` (`Loaded`: how an act's names resolve by file; `_File.labels`; the
constructor and label rules of bite 10), `src/luthier/certify.py` (`Cones`, `cone_hash`: what
enters a name's cone), spec 12.S22 (what an import brings in), 4.R12 and 2.S12 (a match binder
is a fresh name). Nobody else edits now: change `src/luthier/check.py`, `src/luthier/run.py`,
`src/luthier/certify.py`, their tests, programs under `tests/run/`.

1. The checker: a top-level definition in an imported file captures a `match` binder of the
   same name in the importer even when the name is not in the import list (figures: a.lut
   defines `kept`; b.lut imports `other` from a.lut and has `f x := match x * 2.0 { kept -> kept
   + 1.0 }`, refused by 4.R9). An unlisted name of an imported file is not in scope (12.S22), and
   a pattern variable shadows anything (2.S12). Fix in check.py's import loading (an imported
   act not listed is typed for the listed ones' sake but never resolves a free name of the
   importer) and in the elaborator's scoping if the capture is there; the repro as a test.
2. The certifier: importing plot.lth's `text` into a run program (the name of `Cell`'s label)
   changed the hash of csv's cone and its entries read stale; defining `apart` in a test
   program (plot.lth has one) made `LayerOrderInvariant`'s entries stale. A name's cone (6.S8)
   is what the name reaches, and must not change when the importer brings in another file's
   name: find why it did (the loader renaming a colliding definition `name@file` changes the
   canonical code of acts that mention the plain name? or the cone collecting by plain name?)
   and fix at the source so that the cone of a library name is the same whatever the importer
   imports beside it; the two repros as tests (`cone_hash` of `csv`'s laws equal with and
   without `import "plot.lth" text` in the program; `LayerOrderInvariant`'s with and without a
   local `apart`).
3. Run `luthier run tests/run/vector_norm.lut` and `tests/run/plot_two_tables.lut` and the
   suite; no store may go stale from this change (the hashes of existing entries must still
   match: check `luthier check -v src/luthier/lib/arrays_model.lut` shows the laws' standing as
   before; if the fix changes the canonical cone of library names, say so, and the stores need
   one re-certification: say which).

Check: `PYTHONPATH=src python3 -m pytest tests/test_check.py tests/test_run.py tests/test_certify.py
-q`, then the suite. Do not commit. Report in your final message.
