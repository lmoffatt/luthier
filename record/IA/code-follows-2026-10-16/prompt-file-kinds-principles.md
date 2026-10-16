# Brief: D-2026-10-16-e (three kinds of file) into the principles record

Read `CLAUDE.md` first and `record/decisions.md` at D-2026-10-16-e. Edit only
`record/principles-language.md`; never `docs/principles.md` by hand.

1. L2.6: append, before its status mark, exactly:
   "A third kind of file is executive: it carries a demand with its entry and is never imported;
   a `*.run.lut` holds the `main` that `luthier run` applies to the world, a `*.test.lut` the `test`
   lines `luthier certify` runs; its results live beside it, while certificates live beside the
   model that makes the claim (L10.12). The suffix declares the kind and the content verifies it
   (D-2026-10-16-e)."
2. L5.1: append, before its status mark, exactly:
   "The two faces are files: the declarative face is the theories and the models, the executive
   face an executive file (L2.6) or a demand typed at the terminal, kept in its record
   (D-2026-10-16-e)."
3. Each entry's History gains "2026-10-16: ... (D-2026-10-16-e)".
Rewrap to 100 columns; change no other word.

Then `python3 scripts/project_principles.py --write` and `--check`.
Accepted when: `--check` prints ok; `git diff` touches only the two principles files and only those
two clauses and their History lines; `python -m pytest -q tests/test_project_principles.py` passes if
that file exists. Commit the record, then the projection, two-line messages ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"; stage by path; another agent commits at
the same time (retry on .git/index.lock). No report file needed: put the hashes in your final message.
