# Brief: `luthier eval` leaves `textParts` and `textJoin` unreduced

Read `CLAUDE.md`, then in `record/plan/core-2026-10-17/`: `report-eval-foldlist.md` (the slice fix
at a182ed5, the same family of defect) and `report-bite-10.md`'s section "Differential after
a182ed5" (terms over `textParts` and `textJoin` stay unreduced, so `freshName`, `unqualified`,
`canonName` and the renaming paths of `substTerm`, `canonicalTerm`, `applyBindings` went unchecked).

1. Reproduce with a minimal term through `luthier eval` and `luthier session`, and the same term in
   a test program through `luthier test`; record commands and outputs.
2. Find the cause (the slice again, a host primitive with no evaluator rule, or else) and fix it
   with a test that fails before and passes after, or quote the spec clause that makes it intended.
3. Rerun the differential: the script and terms are in `~/.cache/luthier-sdk/difft/` (`run.sh`
   compares `010d17c^` in a worktree against HEAD; rebuild the worktree under your scratchpad with
   bite 10's two renames applied to the old side, as the earlier run did; add terms that exercise
   `freshName`, `unqualified`, `canonName` and the renaming paths). Append the result to
   `report-bite-10.md` as "Differential after the text fix".

Another agent re-certifies the stores and runs the suite; touch no store. Run with
`/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`. Accepted when:
the new test passes; `python -m pytest -q tests/test_run.py tests/test_elaborate.py` passes or
every failure left fails the same way without your change. Small commits staged by path (subject,
blank line, one body line, "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"). Report:
`report-eval-text.md` beside this brief, committed: reproduction, cause, fix, checks, decisions
taken on your own, at most one question. Remove your worktree when done.
