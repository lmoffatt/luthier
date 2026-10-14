# run.py bite 7: `run --set name=value` fills a hole (report)

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on prompt-7.md; saved by the coordinator.
Files: `src/luthier/run.py`, `src/luthier/cli.py`, `tests/test_run.py`,
`examples/sonolocalizacion/validate_graph.lut`, new `tests/run/holes.lut`. Checks: test_run 61
passed, 1 skipped; hello prints; the suite 546 passed; the slow test under LUTHIER_SLOW=1 with
`--set graphDir=examples/sonolocalizacion/A/graph` passed in 3 min 56 s; `luthier check` on
validate_graph.lut reports nothing.

## What changed

- run.py: `holes(loaded)`, the names the file declares and does not define; `parameter(hole,
  text)` reads a `--set` value (a `String` as written; an `Int`, `Float64`, `Bool` through the
  parser as a literal, a leading `-` accepted); refusals: a hole of another type or with binders,
  a wrong literal, a name that is not a hole, a `--set` without `=`; `fill` replaces each set
  hole by a definition before the runtime slice; a parameter hole the slice keeps and nobody
  set is an error naming it (a hole the demand never reaches is not); `run(...)` returns output
  and values set; `record(path, main, values, output)` appends to `x.run.json` beside `x.lut`.
- cli.py: `run --set NAME=VALUE`, repeatable; writes the record after a successful run.
- validate_graph.lut: `graphDir : String` a declaration again; the path in the header's run
  instructions and in the slow test's `--set`.
- Tests on `tests/run/holes.lut`: runs with `--set`, the error without, wrong types, an unknown
  name, a function hole, every literal type, a `Table` hole refused, the record (two runs append
  two entries, a failed run none), the slow test.

## What is left of 12.S18's record

Each entry: the entry, the time (UTC), the parameters, the output. Not yet: the cone's hash and
fingerprint, the interpreter's revision, the lock status, the counts of states with the
uncertified names. A failed run writes no entry. No `--verbose`; `--checked`, `--no-record`
untouched.

## Choices of the agent (each undone by reverting)

1. Only a declaration of `String`, `Int`, `Float64` or `Bool` without binders is a parameter
   hole; another declared type in the cone is not an error at run time.
2. A `String` is the raw text; `Float64` refuses `3`.
3. A name declared and defined in the file is not a hole.
4. `x.run.json` is a JSON array read, appended, rewritten.
5. The record is written by cli.py: `run_file` in-process and the tester record nothing.
6. The test helper deletes a `.run.json` a test created in the repository.

Decision for the coordinator: `*.run.json` tracked or ignored. The coordinator's default:
ignored, as `*.cert.json` is (`.gitignore`), a question for Luciano under P2.
