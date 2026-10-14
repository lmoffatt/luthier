# certify resolves a census member to its file; a control line apart, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). On the last Sonnet's report (the
night plan at 03:40): the fit is refused only for `csv : Codec`'s four laws, whose entries land
in `tests/tester/tables_laws.cert.json` and not in `src/luthier/lib/tables_model.cert.json`,
because the binding goes through a census list `codecs : List Codec := [csv]` defined in the
test program, so `model_homes` finds no model file; and `tables_laws.lut` holds an
expected-refuted control line (`CellsOfTheirKind` on `holeT`) that, once served, would refuse
`built`.

## The prompt

Read `CLAUDE.md` first, then `src/luthier/tester.py` at `model_homes` and `new_entry`,
`src/luthier/certify.py` at `add_entry`, `tests/tester/tables_laws.lut` (the censuses and the
holeT line), `docs/spec/07-tests.md` 7.S9 (the binding expanded: a census as a name with its
fingerprint). Another Sonnet edits `src/luthier/kernel.py` and `tests/test_kernel.py`: touch
neither. Change `src/luthier/tester.py`, `src/luthier/certify.py`, `tests/test_certify.py`,
`tests/tester/tables_laws.lut`, and a new `tests/tester/tables_controls.lut`.

1. `model_homes`: when a census is a list literal (or a definition whose body is one) of names,
   each member name defined in another non-core file is a home too (the entry goes to
   `tables_model.cert.json` for `csv`, and the law's model parameter bound to a member of the
   list is what the entry certifies); a test in `tests/test_certify.py` with a two-file fixture.
2. Move the holeT line (and any other line expected to refute) to `tests/tester/tables_controls.lut`
   with a comment that its refutations are controls (7.S19 names controls for statistical
   laws; here the same idea, [proposed]); `tables_laws.lut` keeps only lines expected to pass.
3. Then `PYTHONPATH=src python3 -m luthier.cli certify tests/tester/tables_laws.lut --fuel
   100000000` (a minute), check `src/luthier/lib/tables_model.cert.json` holds csv's entries,
   and run: `luthier run tests/run/table_cell.lut`, `host_cell_under_operator.lut`,
   `scope/label_and_definition.lut`, then the fit `examples/sonolocalizacion/experiment_zero.lut
   --set graphDir=examples/sonolocalizacion/A/graph --set outDir=/tmp/x --set lmMaxIter=2 --set
   lmTol=1e-12 --set lmFloor=6.661338147750939e-15` (five minutes, background) and
   `LUTHIER_SLOW=1 PYTHONPATH=src python3 -m pytest tests/test_run.py -q -k validate_graph`.
   Remove the `refused(...)` xfail marks of tests that now pass; report which run certified and
   which are still refused, with the laws.
4. Commit `tables_laws.lut` and `tables_controls.lut` each alone (`git add` the path, messages
   naming the laws, ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>");
   leave the Python and the stores uncommitted.

Check: `PYTHONPATH=src python3 -m pytest tests/test_certify.py tests/test_run.py -q`, then the
suite. Report in your final message.
