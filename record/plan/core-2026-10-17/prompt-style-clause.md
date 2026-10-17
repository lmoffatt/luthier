# Brief: the style clause (D-2026-10-18-a) into the principles record

Read `CLAUDE.md` first. Edit only `record/principles-language.md`. After L7.5, add, with the History
line "2026-10-18: clause 6 added, proposed (D-2026-10-18-a)", exactly:

L7.6   (His words, on the core's rebuild) Luthier is written in the manner of Haskell, not of Java:
       a property is said once, generic over the operation and its equality, and each type claims
       it; a helper is written once, generic over the container, and every type uses it; the same
       thing restated per type or per file is a defect of the library. It is measured: no name
       defined in two files, no list helper reinvented, no law unclaimed (D-2026-10-18-a).
       [proposed]

Rewrap to 100 columns, no other change. Then `python3 scripts/project_principles.py --write` and
`--check`. Accepted when `--check` prints ok and `git diff` touches only the two principles files.
Commit the record, then the projection, two-line messages (subject, blank line, body) ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"; stage by path; another agent commits in
code at the same time (retry on .git/index.lock). Final message: the hashes and the --check output.
