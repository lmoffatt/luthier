# Brief: the clause on null sets (D-2026-10-16-i, -j) into the principles record

Read `CLAUDE.md` first. Edit only `record/principles-language.md`. Add, after L9.15 (with its
History line "2026-10-17: clause 16 added, proposed (D-2026-10-16-i, -j)"), exactly:

L9.16  Sampling bounds the failure fraction under its distribution and says nothing of its null
       sets. The cases a law turns on come from three finite sources: the degenerate cases its
       type's theory declares once, the two sides of each cutoff and the boundary of each premise of
       the law, and each branch of the code in its cone; the generator gives them mass or they are
       listed, and the evidence is kept per region, each with its n and its bound, the demand
       combining the grades, the weakest by default. A label an author adds is informative and
       enters no grade (D-2026-10-16-i, D-2026-10-16-j). [proposed]

Rewrap to 100 columns, no other change. Then `python3 scripts/project_principles.py --write` and
`--check`. Accepted when `--check` prints ok and `git diff` touches only the two principles files.
Commit the record, then the projection, two-line messages ending with "Co-Authored-By: Claude
Sonnet 5.5 <noreply@anthropic.com>"; stage by path; retry on .git/index.lock. Final message: the
hashes and the --check output.
