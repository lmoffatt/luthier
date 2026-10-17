# Brief: D-2026-10-18-d into the principles record (L9.17)

Read `CLAUDE.md` first. Edit only `record/principles-language.md`. After L9.16, add, with the History
line "2026-10-18: clause 17 added, proposed (D-2026-10-18-d); a candidate for a principle of its own",
exactly:

L9.17  (His words, a candidate for a fundamental principle) The law of an algorithm states how its
       budget scales with the bound demanded: the resource (steps, samples, memory, bits of
       precision) as a function of the bound and of the problem's features (size, condition, unit
       roundoff), with the floor below which no budget suffices (L13.5). It is the modulus of
       Bishop's constructive analysis, what LAPACK states in its error bounds and operation counts,
       and what the laws of floating point state for each operation; it is tested by measuring the
       resource at several bounds, the slope in log scale part of the law, and read by the planner
       to predict a specimen's resources before running (L6.3) (D-2026-10-16-m, D-2026-10-18-d).
       [proposed]

Rewrap to 100 columns, no other change. Then `python3 scripts/project_principles.py --write` and
`--check`. Accepted when `--check` prints ok and `git diff` touches only the two principles files.
Commit the record, then the projection, two-line messages (subject, blank line, body) ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"; stage by path; another agent commits in
code at the same time (retry on .git/index.lock). Final message: the hashes and the --check output.
