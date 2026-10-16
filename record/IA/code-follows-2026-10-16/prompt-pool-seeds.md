# Brief: a law's samples pooled across seeds (step 3i)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-g (item 41: samples pooled across
seeds, L10.3 with n the total; each stretch keeps its seed; a statistical law continues one
sequential test) and D-2026-10-15-b (the sequential test: alpha, beta, delta, budget);
`record/IA/code-follows-2026-10-16/report-replay-fuel.md` (step 3c, just landed: the store law
`Recording`, disagreements); `src/luthier/lib/certification.lth`, `laws.lth` §4 (the sequential
test), `test.lth`; `src/luthier/certify.py`, `src/luthier/tester.py`; spec 6.S8, 7.S9, 7.S13,
7.S17, 7.S18.

Build:
1. A stretch is one run of a law under one binding and one seed; its entry keeps its seed and n.
2. The grade of a law under a binding is computed on the union of its agreeing stretches: for an
   exact law, the sum of the cases and no failure; for a statistical law, the sequential test
   continued across stretches (its statistic accumulated, the next stretch drawing with a new seed
   when the previous ones left it unresolved), up to the demand's budget, the total n recorded.
3. A replay of a stretch (same seed) is not a new stretch: step 3c's rule applies (absorbed or
   disagreeing). A disagreement in any stretch refuses the union.
4. State the union in certification.lth (a law: the grade of the union is monotone in the stretches,
   and the control: a union that counts a replay twice is refuted); spec text and status for what
   you did.
Tests: two stretches of 100 cases with different seeds give a grade over 200; a replayed seed does
not double n; a statistical law unresolved after one stretch resolved by a second with a new seed;
the control.

Accepted when: `python -m pytest -q` passes in full (count before plus yours; one known failure,
test_an_alias_or_a_constructor_is_no_model_home, may remain until the other agent lands its fix:
say if it is still there); `python3 scripts/check_spec.py` prints its known finding and the counts;
`luthier certify tests/tester/arrays_laws.lut` reports every line known and leaves the library
stores' md5 unchanged. Two-line commits ending with "Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>", staged by path; another agent commits at the same time in run.py, cli.py,
world.lth, demand.lth, plan.lth, spec 8 and 10 (do not touch those), retry on .git/index.lock.
Report: `record/IA/code-follows-2026-10-16/report-pool-seeds.md`, by shell heredoc, committed.
