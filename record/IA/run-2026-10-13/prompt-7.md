# run.py bite 7: `run --set name=value` fills a hole, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). Inventory row 14: the port's
`validate_graph.lut` defines `graphDir` as a string with a comment that `--set` replaces it.

## The prompt

Read `CLAUDE.md` first, then `docs/spec/12-files-and-tools.md` 12.S18 and `docs/spec/08-*.md`
8.S1 (a declared name is a hole the run fills; what is recorded), `docs/spec/03-kernel.md` 3.S9,
`src/luthier/run.py` (`run_file`, `Loaded`), `src/luthier/cli.py` (`run`), and
`examples/sonolocalizacion/validate_graph.lut` (`graphDir`). Another agent edits
`docs/guide/00-fundamental-elements.md` meanwhile; change only `src/luthier/run.py`,
`src/luthier/cli.py`, `tests/test_run.py`, programs under `tests/run/`, and
`examples/sonolocalizacion/validate_graph.lut` (only to turn `graphDir` back into a declaration
with its type and move the path to the slow test's `--set`).

`luthier run FILE --set name=value ...`: each `--set` fills a declared name of the file (a hole,
3.S9) with a value parsed as a Luthier literal of the declared type (`String`, `Int`, `Float64`,
`Bool`; refuse anything else with a message naming the type); a hole the run demands and no
`--set` fills is an error naming it (12.S18); a `--set` of a name that is not a declared hole of
the file is an error. The values set are printed on `--verbose` or recorded as 12.S18 says if it
names a record (`x.run.json`): read it and do the smallest thing it states, saying what you left.
Tests: a program with `graphDir : String` run with and without `--set`, a wrong type, an unknown
name; `validate_graph.lut` declares `graphDir : String` again and the slow test passes
`--set graphDir=examples/sonolocalizacion/A/graph`.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, `PYTHONPATH=src python3 -m
luthier.cli run examples/hello.lut`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not
commit. Report in your final message.
