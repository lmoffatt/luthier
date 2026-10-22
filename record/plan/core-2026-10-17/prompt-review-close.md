# Brief: a naive review of the core's close, before the tag

Read-only. Change no file but your report. Luciano tags after this review (D-2026-10-17-e).

Read `CLAUDE.md`, then `record/plan/core-2026-10-17/execution.md` section 0 (the core's end,
D-2026-10-18-a: 0 homonyms, 0 reinvented list helpers, 0 unclaimed laws, the loose notice only
where real, the suite green, the stores re-certified) and its Status, and `report-bite-13b.md`.
Then check the close yourself, with `/home/lmoffatt/miniconda3/bin/python scripts/core_metrics.py`
and the files it names:

1. The 2 accepted homonyms (`Unresolved`, `scale`): is each reason true (read tester.py and
   certify.py for `Unresolved`; plot.lth and arrays_model.lut for `scale`)?
2. The 48 list helpers kept: for each, does its comment's reason hold, or does a core function in
   `src/luthier/lib/core/lists.lut` (or core.lut, the structures) already do it? List each one
   that could go, with the core function.
3. The 7 unclaimed: is each really not a law?
4. The loose notice's narrowing (check.py, 4.S17): does it now hide anything that was a real
   finding? Look at a sample of 20 of the 1343, chosen at random with a seed you record.
5. Spot-check three renames of bite 13b for a missed use (grep the old name across src, examples,
   tests, docs).

Report: `record/plan/core-2026-10-17/review-close.md`, committed by you (staged by path; subject,
blank line, one body line, "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"); if your
Write is refused, give its full text in your final message. Per item: what you checked, what holds,
what doesn't, with file and line. End with what must change before the tag, if anything, and what
can wait. Another agent edits certification.lth, certification_model.lut and their tests now:
read them, don't judge their in-progress state.
