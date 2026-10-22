# Brief: `foldLeft`, `takeWhile` and `find` in the core, and the helpers they replace

After the tag v0.3 (2026-10-23), first in the queue. `record/plan/core-2026-10-17/review-close.md`
item 2 found that about 20 of the 45 list helpers kept are left folds or early-stop searches that
the core would cover if it had them; their own comments say the core lacks them.

Read `CLAUDE.md`, then review-close.md (item 2 and the cleanup section), report-bite-13b.md's list
of the recursions kept, `src/luthier/lib/core/lists.lut` and core.lut (the list library's style,
names and laws: what exists already, `foldWith` included), and `record/decisions.md` at
D-2026-10-18-b (one name per concept) and -f (bare-form conjunctions).

1. Add to the core, in lists.lut's style, the functions the kept helpers need, under the names the
   field uses (Haskell's, L7.6, unless a core name already covers it): a left fold, `takeWhile`
   and `dropWhile`, `find` (a `Maybe`), and any other the helpers show (say which). Each with its
   laws claimed and certified, and a control per law: for example a left fold against the right
   fold over the reversed list, `takeWhile p xs <> dropWhile p xs == xs`, `find p xs` the head of
   `filter p xs`.
2. Move each kept helper that one of them covers, comparing old against new with `luthier eval`
   on terms that exercise it (empty lists, the first element matching, none matching); keep the
   others with their reason.
3. Re-certify what moved, program by program, twice (second pass 0 lines ran); the suite file by
   file under `timeout 1800`; `python scripts/core_metrics.py` before and after (list helpers down,
   nothing up).

Run with `/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`;
scratch and logs under ~/.cache/luthier-searches/, not /tmp. Long runs detached, waited for in the
foreground with bounded waits. Small commits staged by path: subject, blank line, one body line,
ending with "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>". Another agent writes in
record/plan/audit-algebras-2026-10-22/ only.

Report: `record/plan/after-core-2026-10-23/report-list-searches.md`, committed: the functions and
laws added, the helpers moved and kept, the differential's counts, the checks, decisions taken on
your own, at most one question.
