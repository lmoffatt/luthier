# Brief: the suite never writes a tracked file

Read `CLAUDE.md` first. Since a7f344c the run records under examples/ are tracked (D-2026-10-16-h,
item 8), and a suite run now modifies examples/hello.run.json (one record at 2026-10-17T05:22:05
appeared during a suite run). Find every test that runs or certifies a file under examples/ or
src/luthier/lib/ in place and writes beside it (tests/test_session.py, test_modes.py, test_run.py,
test_result_store.py, test_tables_cut.py name examples/hello.run.lut). Make each copy the program
to tmp_path first (as test_result_store.py already does), or redirect what it writes; keep each
test's intent. Then decide whether the 05:22:05 record of examples/hello.run.json came from a
test (rerun the suspects and compare); if so, restore the file with `git checkout`; if not, leave it
and say so.

Accepted when: `git status --short` is the same before and after `python -m pytest -q` (record
both), and the suite passes in full. Two-line commits ending with "Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>", staged by path; another agent edits tester.py, certify.py, generators.py,
the spec and the stores at the same time (do not touch those), retry on .git/index.lock. Final
message: the hash, the two status listings, the suite line.
