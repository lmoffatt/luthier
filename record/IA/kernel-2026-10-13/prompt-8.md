# kernel.py, bite 8: `==` demands its parts, brief for a Claude agent

Written 2026-10-13 at the commit that holds this file, by the coordinating session (luthier-1b),
for a Sonnet or Opus agent launched by it. After bite 7 (opus-7.md, 0e1f69c).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only
`src/luthier/kernel.py`, `tests/test_kernel.py`, and write your report; a failure from another file
is someone else's, report it, do not fix it.

term.lth §5 (`git log -1 -- src/luthier/lib/term.lth`) adds `EqualityDemandsParts`: `==` reduces a
compared part in place before comparing, leftmost first, as a match demands what its patterns
inspect; its cases are a redex inside a pair on the left, one on the right of a value, and one
inside a record value. `EqualityStuck` is unchanged: a part that cannot become a value (a hole, a
lambda, an extern) leaves `==` stuck. Today (bite 7) kernel.py makes `==` stuck on any part not yet
a value. Mirror the new law exactly, with a test for each of its cases and for the order (leftmost
first), keeping bite 7's tests. Then check that world.lth §5's `agreement` comparison, `d.describe
before == (after, x)`, now steps in a small program you write in the test (a description returning
a pair whose parts are redexes).

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_run.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in a few lines to
`record/IA/kernel-2026-10-13/report-8.md`.
