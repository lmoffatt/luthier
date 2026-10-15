# Brief: a certificate lives only beside the file that makes the claim (step 3b)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-a and D-2026-10-16-b (item 7),
`record/principles-language.md` L10.12 (the stores mirror the files where the claims are made),
L2.8; `docs/spec/12-files-and-tools.md` 12.S11; `src/luthier/certify.py` (where entries are written:
the store beside the test program and the copy into the model file's store), `tests/conftest.py`
(LUTHIER_LIBRARY_STORES, the temporary copy of the stores).

Build:
1. `certify` writes an entry only into the store of the file that makes the claim: the file that
   defines the model named in the law's binding (as the night's copy does today), or, for a law with
   no model of the library in its binding (a theory's own law tested on a census), the file that
   states the law. A test program keeps no store of its own.
2. The stores beside test programs (`tests/tester/*.cert.json`, `examples/*.cert.json` if any) are
   folded: every entry not already in the claiming file's store is moved there; then the files are
   removed with `git rm`. Count the entries before and after and say both numbers.
3. A run and `certify` read only the claiming files' stores; nothing reads a store beside a test
   program any longer. Controls entries (kind Control) follow the same rule: they live beside the
   claim they control.
4. Tests: a law certified from a test program is found by a run that imports only the model file; no
   store file appears beside the test program after `certify`; a control (L9.14): a store written
   beside the test program by hand is not read.
Do not touch the spec's statuses (another agent edits them now); list in your report the sentences
of 12.S11 or chapter 6 that must change, with the new wording you propose.

Accepted when: `python -m pytest -q` passes as before (737 passed, 5 skipped, 9 xfailed) plus your
tests; `luthier certify tests/tester/arrays_laws.lut` writes only into
`src/luthier/lib/arrays_model.cert.json` and reports every line known; the entry counts before and
after the fold match (none lost). Small commits of two lines ending with "Co-Authored-By: Claude Opus
5.5 <noreply@anthropic.com>"; stage by path; another agent commits at the same time (retry on
.git/index.lock). Report: `record/IA/code-follows-2026-10-16/report-claim-store.md`, written with a
shell heredoc and committed: what you built, the counts, decisions taken on your own, at most one
question.
