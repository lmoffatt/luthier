# The tester knows controls: a law with no refuted wrong model is reported (L9.14, D-2026-10-15-a)

Read `CLAUDE.md`, then L9.14 in `docs/principles.md`, D-2026-10-15-a at the end of
`record/decisions.md`, 7.S19 in `docs/spec/07-tests.md` as now written, and the pattern of a
control today: `tests/tester/tables_controls.lut` (lines expected to refute). Then
`src/luthier/tester.py`, `certify.py`, `src/luthier/lib/test.lth` §1 (`TestSpec`).

1. A `test` line can be a control: a law tested on a model broken on purpose, expected to be
   refuted (state how in test.lth: a field `control : Bool`, or a form `control law ...`; the
   least change, [proposed], cited to 7.S19; commit test.lth alone if it changes).
2. The tester and `certify` record a control's outcome as its own entry kind: refuted is the
   control passing; confirmed is the control failing (a law too weak), reported loudly.
3. `luthier certify` and `check -v` report per law its control status: controlled (a control
   refuted at the current hash), uncontrolled ("untested against any wrong model", 7.S19), or
   control failed. A law's grade is unchanged by this (the demand's business later); the report
   is the point.
4. Tests, and `tables_controls.lut` read as controls of `tables.lth`'s laws.
Change test.lth (if needed), tester.py, certify.py, cli.py, tests/test_tester.py,
tests/test_certify.py, tests/tester/tables_controls.lut. Write your report with a shell heredoc
to `record/IA/controls-2026-10-15/report-tester.md` and commit it alone; the Python stays
uncommitted. Accepted when: the suite passes; `luthier certify tests/tester/tables_laws.lut
tests/tester/tables_controls.lut --no-cert` (or with stores, then restored) lists `CellsOfTheirKind`
as controlled and the other laws as uncontrolled; paste that listing.
