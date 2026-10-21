# Brief: the old-against-new differential on term.lth and term_model.lut (bite 10's open check)

Read `CLAUDE.md`, then `report-bite-10.md` (its Differential testing: term.lth and term_model.lut
could not be compared because `luthier eval` left terms over `foldList` unreduced) and
`report-eval-foldlist.md` (fixed at a182ed5), both in `record/plan/core-2026-10-17/`.

Run the differential bite 10 could not: for the functions of term.lth and term_model.lut that bite
10 rewrote on the core's list functions, evaluate the same terms on the version before bite 10
(010d17c^, in a `git worktree` under your scratchpad) and on HEAD, with
`/home/lmoffatt/miniconda3/bin/luthier eval`, and compare. Pick terms that exercise each rewritten
function (at least one per function, edge cases: empty lists, duplicates, names a binder prefixes).
A disagreement is a finding: give the term, both values, and the commit that changed it; fix it
only if the fix is a one-line slip in bite 10's rewrite, with a test.

Another agent re-certifies the stores and runs the suite; touch no store and no other file. Report:
append a section "Differential after a182ed5" to `report-bite-10.md` with the terms, the values and
the verdict, and commit it staged by path (subject, blank line, one body line, ending with
"Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"). Remove your worktree when done.
