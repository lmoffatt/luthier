# kernel.py and run.py, bite 12: the Runner's speed, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). The fit (`examples/sonolocalizacion/
experiment_zero.lut`) runs at HEAD (69684d7) but at about 95 s per Levenberg-Marquardt iteration
(the second port's report, `record/IA/slice-port-2-2026-10-14/report.md`, "Behind it": the native
22 x 30 Jacobian crossing to the host entry by entry; the information and the score each asked
twice at the same point) and run 9's finding 3 (`record/IA/run-2026-10-13/report-9.md`:
`kernel.step` rebuilds its environment and constructor table from the whole program on every
call). Luciano's call between speeding the Runner and giving the Jacobian as one extern is
pending; the night does the first.

## The prompt

Read `CLAUDE.md` first, then those two report sections, `src/luthier/kernel.py` (`step`, what it
builds per call: the environment of definitions, the constructor table, `BOOTSTRAP_PRIMITIVES`),
`src/luthier/run.py` (`Runner.whnf`, `force`, `Shared`, `function_to_host`, the materialization of
a lambda over `Fin n` at the crossing). Nobody else edits code now: change `src/luthier/kernel.py`,
`src/luthier/run.py`, `tests/test_kernel.py`, `tests/test_run.py`.

1. Measure first: `PYTHONPATH=src python3 -m luthier.cli run examples/sonolocalizacion/experiment_zero.lut
   --set graphDir=examples/sonolocalizacion/A/graph --set outDir=/tmp/x --set lmMaxIter=2 --set
   lmTol=1e-12 --set lmFloor=6.661338147750939e-15` under `python3 -m cProfile -o /tmp/prof` (or
   with the Runner's own counters): where the time goes (kernel.step's setup, substitution,
   the crossing, the host). Paste the top of the profile in the report.
2. Then, in order of what the profile says, without changing any law: memoize per program what
   `kernel.step` builds (the environment, the constructor table; keyed by the program object, as
   `constructors` was memoized in check.py), and whatever else the profile names as pure
   recomputation (for instance the arity of a `TypedExtern`, the resolution of a route). Do not
   change reduction order, sharing, or what is stuck; every test stays as it is.
3. Measure again the same run; paste the wall time before and after, and the time per iteration.
   The score and the information asked twice at the same point (`finished`, then `step`) is
   lm.py's and belief.lth's business, not this bite's: leave it, note the cost.

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_run.py tests/test_lm.py
-q`, then `PYTHONPATH=src python3 -m pytest tests -q`; `LUTHIER_SLOW=1` validate_graph's slow
test (its wall time before and after). Do not commit. Report in your final message.
