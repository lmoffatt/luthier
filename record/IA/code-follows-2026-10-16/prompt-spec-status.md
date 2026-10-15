# Brief: the spec says what the code does (step 2)

Read `CLAUDE.md` first, then `record/plan/code-follows-principles-2026-10-16.md` (step 2) and
`record/IA/code-follows-2026-10-16/report-debt.md` (the classification of 131 clauses, with
evidence), and `scripts/check_spec.py` (the status grammar).

1. `scripts/check_spec.py`: accept a postponement in a status, `[decided D-x; suspended by D-y]`
   (and `[decided Ln.k; suspended by D-y]`), D-y checked like D-x; print, as information, one line
   with the counts: implemented, decided, of which suspended, proposed. Update its docstring and
   `docs/spec/00-index.md`'s description of the statuses.
2. For each clause the report classes "postponed" with a decision: add `; suspended by D-y` to its
   status. A postponement found only in a theory comment: write the comment's file and line in the
   clause's text ("Postponed in certification.lth:267 under D-2026-10-14-c"), and use the decision
   if the comment names one.
3. For each clause classed "implemented in fact": change its status to `[implemented]` only after
   you confirm the evidence the report gives (open the file at the line). If the evidence is partial,
   leave the status and say so in your report.
4. Leave "pending" clauses as they are; the report already lists them.
Do not touch chapters' wording otherwise, nor 8.S8, 8.S10, 12.S18, 10.S6, 12.S11 (done today in
1d1cef9), nor any code under `src/`.

Accepted when: `python3 scripts/check_spec.py` exits as before (one finding, 03-kernel.md:190) or 0,
and prints the counts line; every status changed is listed in your report with its evidence.
Commit `check_spec.py` and the index first, then the spec chapters, in small commits of two lines
ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"; stage by path; another agent
commits at the same time (retry on .git/index.lock). Report:
`record/IA/code-follows-2026-10-16/report-spec-status.md`, written with a shell heredoc, committed.
