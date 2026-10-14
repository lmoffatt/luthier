# certify writes each entry into the store of the model's file, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). On run's refusal report
(`record/IA/certification-2026-10-14/report-run.md`, decision 1): the entries `luthier certify`
writes sit beside the test program (`tests/tester/arrays_laws.cert.json`), but a run reads only
the stores of the files it imports (12.S11), so `numpy : Arrays`, `lm : Maximizer`, `doubles`,
`elementary`, `numpySort` stay uncertified for every run. Night default, [proposed] until
Luciano marks it: an entry is written into the store of the file that defines the model named
in its binding (the test program's own store keeps a copy for its own laws).

## The prompt

Read `CLAUDE.md` first, then that report's decision 1, `docs/spec/12-files-and-tools.md` 12.S11
and 12.S16, `src/luthier/certify.py` (`store_path`, `record`, `write_store`, `certify_file`) and
`src/luthier/tester.py` (`new_entry`: the binding, which names the model and its file). Nobody
else edits code now except a Sonnet writing `tests/tester/tables_laws.lut`: change
`src/luthier/certify.py`, `src/luthier/tester.py`, `src/luthier/cli.py`, `tests/test_certify.py`.

1. When a `test` line's law is a law of a theory whose model in the binding is defined in
   another file (`numpy` in `arrays_model.lut`, `lm` in `belief_model.lut`, ...), `record` writes
   the entry into that file's store (`src/luthier/lib/arrays_model.cert.json`, which
   `.gitignore` un-ignores) as well as into the test program's; an entry's identity is the same
   in both. Reading merges as before. A test program's own laws (wrappers like
   `MaximizersAgree`) stay in its own store only.
2. Then run `PYTHONPATH=src python3 -m luthier.cli certify tests/tester/arrays_laws.lut
   tests/tester/fit_laws.lut tests/tester/belief_laws.lut tests/tester/optimization_laws.lut
   tests/tester/probability_laws.lut --jobs 4 --fuel 100000000` in the background (about 20
   minutes; `numbers_laws.lut` too, 6 s) and check that `src/luthier/lib/*_model.cert.json` now
   hold the entries; then `PYTHONPATH=src python3 -m luthier.cli run tests/run/vector_norm.lut`
   and `tests/run/maximize_quadratic.lut` run instead of being refused: remove the strict xfail
   marks of the tests that now pass (`refused(...)` in tests/test_run.py, the mark in
   tests/test_lm.py) and say which still fail and for which laws.
3. Do not commit the `.cert.json` files (the coordinator decides; list them with their sizes).

Check: `PYTHONPATH=src python3 -m pytest tests/test_certify.py tests/test_run.py tests/test_lm.py
-q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message.
