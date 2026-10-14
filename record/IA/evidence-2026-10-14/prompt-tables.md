# tables_laws.lut: listed cases for Codec and Table, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). On run's refusal report
(`record/IA/certification-2026-10-14/report-run.md`): the only laws in the slice's cone no entry
serves are `csv : Codec`'s four (`RoundTrip`, `Canonical`, `Tolerant`, `Rejects`) and `Table`'s
four, because there is no tables laws file and `Table`, `Perturbed`, `BrokenText` have no
generator (7.R4): listed case entries certify them.

## The prompt

Read `CLAUDE.md` first, then `src/luthier/lib/tables.lth` (the laws and their parameters),
`tables_model.lut`, one of the evidence agent's test programs as the pattern
(`tests/tester/arrays_laws.lut`: the imports, the censuses of one, the `test` lines with listed
cases) and `record/IA/evidence-2026-10-14/report.md` ("The tester": what a census can be).
Another Sonnet edits `certify.py`, `tester.py`: touch no `src/`; write `tests/tester/tables_laws.lut`
only.

Write the `test` lines for every law of `Codec` on `csv` and of `Table` on listed tables: a
census of tables built in Luthier (`built`-style records with `nRows`, `names`, `kinds`, `cell`:
an empty table, one row, three rows with int, real and text columns, a table with a `nothing`
cell) and parsed from listed CSV texts (session A's `nodes.csv` and `measurements.csv` as text,
as `tests/tester/session_a.lut` holds them; a CSV with CRLF and spaces for `Tolerant`); for
`Rejects`, listed `BrokenText` values (an unknown type, a repeated column, a wrong cell count, an
unparsable number, a non-finite float: the readings of
`record/IA/sonolocalizacion-inventory-2026-10-13/answers-2026-10-14.md` item 2); seed 20261014.
Run `PYTHONPATH=src python3 -m luthier.cli test tests/tester/tables_laws.lut --no-cert` (minutes)
and paste the lines; a refuted law is a finding for tables.lth's author, do not change the
theory. Commit the file alone (`git add` its path), message naming the laws, ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>". Report in your final message.
