# kernel.py and run.py, bite 12: the Runner's speed, report

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on prompt-12.md; saved by the coordinator.
Files: `src/luthier/kernel.py`, `src/luthier/run.py`, `tests/test_kernel.py`, `tests/test_run.py`
(3 tests added, none touched). Checks: the three test files pass; the suite 570 passed.

Result: the two-iteration run of experiment_zero.lut went from 264.1 s to 20.1 s wall (13x);
each iteration from about 87 s to 4.8 s; peak memory 61.6 to 63.6 MB; output identical byte for
byte. validate_graph's slow test from 33.6 s to 5.0 s. With 6 iterations the fit keeps improving
(sigma 2.649 m, nu 15.28).

Profile before (cProfile at 69684d7, 819.7 s): `kernel.step` 426 s tottime (796 s cumulative)
rebuilding its environment and constructor table from the whole program on every call (about
700 of 820 s); `isinstance` 216 s; `free_names` 44 s, called by `_substitute` at every level;
`materialize` (the native Jacobian entry by entry) 644 s, almost all inside `step`. After (56 s):
the generator stack, `_substitute`, `whnf`, `_step`: reduction itself, no pure recomputation.

What was memoized, no law, order, sharing or stuck case changed: (1) `kernel.step`'s tables,
built once per program (`_build_tables`, the last program matched by identity, as check.py
memoizes `constructors`): about 85% of the time; (2) free names inside substitution
(`_memo_free_names`, bottom-up by subterm, keyed by the term object's identity with the term
kept alive, kept across substitutions, emptied above `FREE_NAMES_MEMO_LIMIT = 1 << 12` terms, a
module parameter, P11; 2^12, 2^14, 2^16 gave the same time and 63, 71, 103 MB; unlimited 224 MB;
public `free_names` unchanged): 118 s to 58 s profiled; (3) `Runner.arity` cached per function
for signature-read arities; a host array that crossed in (`Entries`) answers 1 directly.

Left alone: the information and the score asked twice at the same point (`finished`, then
`step`): roughly half of each 4.8 s iteration (`lm.finished` 19.1 s over 3 calls, `lm.step` 14.9 s
over 2, of 34.9 s in `maximize`, from the profile's proportions). For lm.py and belief.lth.

Decisions of the agent: the memo kept across substitutions with a limit; the limit 2^12 as a
parameter; the `Entries` shortcut; the signature arity cache. Profiles in the session scratchpad.
