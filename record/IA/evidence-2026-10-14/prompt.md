# Evidence on the slice's laws: `luthier test` over the fit, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). The order after v0.2 (D-2026-10-13-ad):
evidence and certification designed on the slice's laws and on how they fail. D-2026-10-14-c
(`record/decisions.md`, end): every law Boolean, every cutoff a parameter the demand supplies.

## The prompt

Read `CLAUDE.md` first, then D-2026-10-14-c, `record/IA/tester-2026-10-14/report.md` (what
`luthier test` does: `test` lines as data, exhaustive and sampled modes, censuses as bindings,
`NotRun` reasons), `docs/spec/07-tests.md` 7.S20 and 7.R1, `src/luthier/lib/test.lth` §1 (the
`test` function and its arguments), and the theories of the slice at their laws: `arrays.lth`
(`Arrays`'s laws), `probability.lth`, `belief.lth`, `optimization.lth`, and the port
`examples/sonolocalizacion/positions.lut`, `distances.lut`, `distance_graph.lut`. Nobody else
edits now: you may add `test` lines to the model files `arrays_model.lut`, `probability_model.lut`,
`belief_model.lut`, `optimization_model.lut` and to the three example files (a `test` line is
data, D9; it changes no law), write programs under `tests/tester/`, and change
`src/luthier/tester.py` with `tests/test_tester.py` only to fix what blocks a run (say what).

1. For each theory, write the `test` lines that run its laws on its model, with the cutoffs
   bound as the demand would supply them (`tol`, `Resolution`, `RankFloor`, `Settings`, `Damping`
   as censuses of one, values from v0.1's or the fit's run: lmTol 1e-12, floor n eps) and a seed
   (20261014); sampled where the parameters have generators the tester draws (`VecOf n` with a
   bound `n`, `Positive`, `Moderate`), exhaustive where finite, `NotRun` where a parameter is a
   record of functions or a theory (7.R4: list those as the laws that need a generator or a
   listed case, and give each one listed case from the fit: the quadratic family, or
   `positionsModel` on session A's graph read through `readGraph`, if the tester can bind a
   case by a value computed in the file).
2. Run `luthier test` on each file (minutes each; in the background), and report per law: the
   grade, the cases evaluated, and for a refuted law the first refuting case and your reading
   of why (a false law, a tolerance too tight, a generator drawing outside the law's domain, a
   host leaf's rounding), without changing any law: a refuted law is a finding for its author.
3. For the fit itself, one `test` line per law of `Maximizer` and `LMStep` on the quadratic
   family (`QuadraticConverges`, `QuadraticStepAccepts`, `DirectionDescends`, `DirectionAgrees`,
   `StepRule`) with `lm` and `host` as the models, and the native `lmMaximizer` as the second
   model of `Maximizer`: do the two models agree on the same cases?

Check: `PYTHONPATH=src python3 -m pytest tests/test_tester.py -q`, then `PYTHONPATH=src python3
-m pytest tests -q`. Commit the `test` lines and the programs as you go, one file per commit
(`git add` the path; never `-A` or `.`; messages naming the laws, ending with "Co-Authored-By:
Claude Opus 5.5 <noreply@anthropic.com>"); tester.py changes are not committed (the coordinator
reviews them). Report in your final message: the table per law, the refutations and their
reading, the laws that need a generator, what the tester lacked.
