# term_model.lut, the record constructors: brief for Codex

Written 2026-10-13 by Claude Opus 5.5 at the commit that holds this file; run by the session
(Luciano's authorization to launch Codex from it).

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` gained three
constructors of `Term` at f421684 (`Record`, `RecordValue`, `Proj`: a record is a product whose
projections are named, D-2026-10-13-x in record/decisions.md), the law `ProjOfRecord` in §5, and
`Record`, `RecordValue` in `ValuesStay`; at 9a89873 `IotaSkips` changed (it is now stated with a
matching arm after the skipped one). Read `git show f421684 9a89873 -- src/luthier/lib/term.lth`.

Update `src/luthier/lib/term_model.lut` (yours from before; your report is
record/IA/term-2026-10-13/codex.md) so that its four models handle the three constructors and meet
every law of term.lth as it now reads: `alpha` (fields compared by name and in order), `substitute`
(into the fields), `canonical` (names of fields kept: they are part of the term), and `reduce`
(`Proj (RecordValue kvs) x` reduces to the value at `x`, the first field of that name;
`Proj r x` with `r` reducing to a `RecordValue` likewise; `Record` and `RecordValue` are values).
Check that `IotaSkips` holds as now stated. Check with
`PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/term_model.lut`. Touch nothing but
term_model.lut and your report; another session and another Codex work in this tree (they own
src/luthier/term.py, kernel.py and the tests). Do not commit. Append a short section "Records" to
`record/IA/term-2026-10-13/codex.md`: what changed, any law not met.
