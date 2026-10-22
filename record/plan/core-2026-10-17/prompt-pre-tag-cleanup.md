# Brief: the cleanup review-close.md asks for before the tag

Read `CLAUDE.md`, then `record/plan/core-2026-10-17/review-close.md` (eda8d7c), its section
"Before the tag". Do exactly that, one small commit each:
1. Delete `allUnit` (probability.lth:269): its importers (generators_model.lut,
   tests/test_tester.py) use the core's `all ... unitVec` directly.
2. `overRegions` (certification.lth:463) in the `fold` form over `filter grades rs`, as
   `overBindings` does; `prepend` (certification.lth:323) as a fold too if it is a one-line change.
3. The stale comments and docstrings that still name an old name: the list in review-close.md
   item 5 (distances.lut:11; run.py:2012, 3188, 3319, 2367, 3399; tester.py:2097; certify.py:809;
   demand.lth:37, 116; tests/test_tester.py:407; tests/tester/world_laws.test.lut:6, 109).
Then re-certify what moved with `/home/lmoffatt/miniconda3/bin/luthier certify`, program by
program (probability_*, generators_*, certification_*, regions_*, world_*, demand_*, and any other
the cone reaches), twice: the second pass at 0 lines ran. Run the suite file by file under
`timeout 1800` with outputs under ~/.cache/luthier-cleanup/ (not /tmp); all files pass.
`python scripts/core_metrics.py`: list helpers 48 to 45 or 46, nothing up. Record the counts and the
commits in a section "Before the tag: cleanup" appended to review-close.md, committed. Small
commits staged by path: subject, blank line, one body line, ending with "Co-Authored-By: Claude
Sonnet 5.5 <noreply@anthropic.com>". Long runs: detached with bounded foreground waits.
