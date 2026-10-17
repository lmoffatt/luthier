# Report: step 3h, tables' Maybe, failures never accepted by a cutoff, run records, cut runs

Brief: record/IA/code-follows-2026-10-16/prompt-tables-cut.md (D-2026-10-16-h items 8, 14, 16; the
coordinator's answer to 3g's question). Written 2026-10-17 by Claude Opus 5.5, an agent of the
coordinating session. Commits: 227065a, 0f14ee5, e0dcae9, 36ee25a, 26b997d, and this report.

## What was done

Item 14, strict `Maybe` (227065a). tables.py's `parse` gives `host.Just table` or `host.NOTHING`,
`Table.cell` gives `Just (label, value)` or `NOTHING`; `read_file` follows `parse`; Python callers
use `parse_or_raise`. run.py's bridge reads a declared `Maybe` only as `Just`/`NOTHING`: a bare
value, `None` included, is refused with or without `--checked`. A table built in Luthier crosses out
with its `cell` as it is (the wrapper that turned it into None or a pair is gone), and
`tables.as_table` refuses a column whose cell is `NOTHING`. test_plots.py follows.

Item 16 (0f14ee5, e0dcae9, 36ee25a). certification.lth draft 4, in §3 and §5 only: `refutes`,
`namedPast`, `standingRefusals`, `assumedPast` (a refusal of a failure or a disagreement is lifted
only when the demand names its law), and the law `NoCutoffAcceptsAFailure` of `Certifying` (a failed
entry, drawn covering and graded proved, serves no demand at any cutoff). It is certified on
`certifying` (cases, certification_laws.test.lut) and controlled by `acceptsAFailure`, a model whose
weakest cutoff accepts anything of the law at its hash (tests/tester/cutoff_controls.test.lut),
refuted at `g = AssumedGrade` on the failed entry. In run.py, `--accept assumed:LAW` lifts the
refusal of a refuted law: the record lists it under `certification.assumed` with the refutation,
grade assumed and the names downstream of the name that states it; that name counts as failed and
not certified; every such run warns on stderr. A refusal line of a refuted law suggests the flag. A
name that is neither a provisional nor a refuted law of the cone is warned (the warning moved from
`refuse_provisional` to `certification`, its text now "names no provisional extern and no refuted
law of the cone").

Item 8 (e0dcae9). `.gitignore` keeps `*.run.json` and `*.results.json` ignored and un-ignores them
under `examples/**`. `git check-ignore`: examples/sonolocalizacion/experiment_zero.run.json and
examples/hello.results.json not ignored (the negations at .gitignore:7, :8); tests/run/table_cell.run.json
and tests/run/scope/x.results.json ignored (.gitignore:4, :5).

The cut run (e0dcae9). The Runner remembers why it stopped (`cut`: fuel or time limit) whatever
wraps the error on its way out; `run` raises `Cut` with the state; `luthier run` exits 1, says why,
and `record` appends an entry with `finished: false`, `cut` (reason, steps, message), the demand,
plan and certification, no `output`, and `result_store` `{"pure", "fresh", "written": null}`.
Nothing goes to x.results.json, and `breaches` skips a run that did not finish.

Spec (26b997d): 6.S15, 8.S1, 11.S6, 12.S18, 12.S24, each with an [implemented] sentence.

Tests: tests/test_tables_cut.py (17): the bare value and None refused under `--checked` and
without, Just and NOTHING crossing, tables.py's answers; a refuted law refusing the run with no
`--accept`, a bare `assumed`, another name and the model's name (the control), and running as
assumed with its warning at each of two runs, grade, downstream and record; the `.gitignore` lines;
a cut run by time and by fuel recorded twice, nothing stored; a cut run in no breach.
test_modes.py follows the new warning text.

## Acceptance

- `python -m pytest -q` at 10d09e8 (my commits and the controls agent's): 798 passed, 6 skipped, 9 xfailed
  in 452 s (before: 781 passed; 17 are tests/test_tables_cut.py). A first run failed one test of
  test_certify.py that the controls agent updated during it (10d09e8, which lists
  NoCutoffAcceptsAFailure); it passes now.
- `python3 scripts/check_spec.py`: its known finding, `docs/spec/03-kernel.md:190: ... "only through
  the bridge and never reduced by the kernel"`, and `185 implemented, 80 decided (of which 33
  suspended), 8 proposed`.
- `luthier certify tests/tester/tables_laws.test.lut tests/tester/tables_controls.test.lut`:
  exit 1. Every law `cases` and controlled, every control refuted, but `CellsOfTheirKind: refuted
  at t = holeT`. After the change the four codec lines and the four codec controls ran again (their
  cones reach tables.py); with `--deep` all 16 lines replayed and agreed; a last plain run had all
  16 known and left both stores byte for byte.

## Does `CellsOfTheirKind` now hold?

On its census, yes: the replay of its line at the current hash passed. It is still reported refuted
because tables.cert.json holds `Failed: t = holeT` of 2026-10-14T18:02:13 at the law's current
cone (sha256:7bdd74d3), binding `holes (Listed)`: the control line, run when it lived in
tables_laws and before controls had their own kind of entry (report-tester.md of 2026-10-15 found
it). `holeT` has a `nothing` cell in an int column, so that failure is right about `holeT`; it is
the law's evidence only by accident of history. The strict `Maybe` did not change it and could not:
the law's cone reaches no host. Under D-2026-10-15-f a failure at the current hash refutes until
removed by hand with its reason; I left it.

## Findings

1. The fingerprint of a listed census that mixes names and applications covers the names only.
   `tables` in tables_laws is `[emptyT, noColumns, oneRow, threeRows, parsed nodesTextA, ...]`;
   tester.py's `_list_members` gives the four names and the fingerprint is their hashes, so the
   change of tables.py, which the four parsed members cross, left SchemaWellFormed, KindsKnown and
   CellsOfTheirKind known. I replayed them with `--deep` (they agree). A fix: fall back to the
   census's own cone when a member is not a name; it changes fingerprints, so a re-certification
   wave. Not done.
2. The existing records under examples/ (hello.run.json, validate_graph.run.json,
   experiment_zero.run.json) now show as untracked. I did not add them: the brief told me to leave
   untracked files I did not create alone. Adding them is the rest of item 8.
3. A pure run past an assumed law is served from x.results.json at its next run (the key has no
   field for `assumes`); the record still lists the assumption and warns, since certification is
   read before serving.

## Decisions I took on my own (each undone by one commit)

1. The bridge is strict on `Maybe` always, not only under `--checked` (D-2026-10-16-h says strict;
   the shape checks of 11.S6 run always).
2. `tables.as_table` refuses a `NOTHING` cell of a column, where it put None in the row before.
3. `assumed:LAW` lifts only a refusal for a failure or a disagreement, not stale or uncertified, and
   names the law by its plain name, so it lifts that law on every name of the cone that states it.
4. A name run past a refuted law counts as `failed` in `states` and is listed in `not certified`.
5. The control lives in a new file, cutoff_controls.test.lut, since another agent was editing
   certification_controls.test.lut; one commit moves it.
6. A cut run's record has `finished: false` and no `output`; finished runs carry no `finished` field
   (absent reads as finished). The lock is written beside the program if absent, as for any run.
7. The refusal line of a refuted law suggests `--accept assumed:LAW`.
