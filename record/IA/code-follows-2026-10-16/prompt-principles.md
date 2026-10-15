# Brief: his decisions of 2026-10-16 into the principles record

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-b and D-2026-10-14-c,
`record/principles-candidates-2026-10-15.md` (C1 to C5: the wording to use), and
`record/plan/decisions-pending-2026-10-15.md` items 22 and 29 to 33.

Edit only `record/principles-language.md` (never `docs/principles.md` by hand):
1. C1 as L2.8 [proposed], citing D-2026-10-16-b.
2. C2's sentence only, in L2.7 (no clause under P13).
3. C3 as L13.5 [proposed]; C4 as L11.8 [proposed].
4. C5's note in O1 (What is open); and in L10.5, a sentence that the clause is suspended in the
   Boolean slice by D-2026-10-14-c until the cost types (the tolerance is a law parameter and so
   part of the binding, matched exactly; certification.lth's comment at the cost cutoff of 6.S15).
5. L5.6: `lib/plan.lut` becomes `plan.lth`.
6. L5.18: one sentence with item 22's reading (D-2026-10-16-b): a domain a law states is part of the
   law, not a cutoff; a series' truncation is derived from the demand's tolerance; what a demander
   could vary is a declared default, recorded.
Each touched entry's History gets "2026-10-16: ... (D-2026-10-16-b)". Keep the record's shape
(numbered clauses, status in brackets, 100 columns).

Then run `python3 scripts/project_principles.py --write` and `--check`.
Accepted when: `--check` prints ok; each clause added cites D-2026-10-16-b; `git diff` touches only
the two principles files. Commit the record, then the projection, in two commits of two lines each,
ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>". Write your report (what
you did, any wording you had to choose, decisions taken on your own) to
`record/IA/code-follows-2026-10-16/report-principles.md` with a shell heredoc and commit it.
