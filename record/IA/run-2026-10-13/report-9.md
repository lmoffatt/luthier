# run.py bite 9: a bound value demanded once (8.S4), report

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on prompt-9.md; saved by the coordinator.
Files: `src/luthier/run.py`, `tests/test_run.py`, new `tests/run/maximize_shared.lut`,
`tests/run/read_once.lut`, a comment in `maximize_quadratic.lut`. Checks: test_run, test_lm,
test_tester 90 passed, 2 skipped; the suite 565 passed; no `.run.json` left.

## What 8.S4 and term.lth say

8.S4 speaks of sharing within a run ("a term in an environment is a thunk, computed at first use
and remembered"; it cites `machine.py`, gone). The memo across runs is 8.S3 and 8.S8 (8.S10: it
does not exist); untouched. 3.S25 asks each entry of a lambda over `Fin n` be computed once
under call by need: argument sharing gives that. term.lth §5's `Zeta` is one weak-head step by
substitution and says nothing about sharing; `kernel.step` unchanged.

## What is shared and keyed by what

A `Shared` leaf (a subclass of `t.Axiom` with identity equality) holds a closed term, reduced to
weak head normal form at its first demand (`Runner.force`) and kept; the key is the object
itself (every copy substitution makes is the same cell). The kernel passes it through as an
opaque leaf; only the Runner opens it. Wrapped (`Runner.share`): a `Let`'s value; the arguments
of a lambda head; what a pattern variable binds; [proposed] the program's constants (each
`Define` whose body is not a lambda, one cell per name per Runner). Only terms that would
compute are wrapped; pairs, injections, records keep their form with their parts shared.

## Timings and counts

validate_graph.lut (`--set graphDir=...`): 246.34 s before, 32.35 s after, same output (both
with `examples/` at 5019221, finding 1). Maximizer counts of `maximize_shared.lut`: before 9/15/15
(three fits), after 3/5/5. `read_once.lut`: 2 reads before, 1 after.

## Findings

1. validate_graph.lut fails at HEAD with "stuck match" after 2 s, before and after the change;
   first at 63ee303 ("distance_graph.lut imports positions.lut"), the second port's area.
2. Checker: `match r { (w1, first) -> host.print w1 (showText first) }` with `r : W * Maybe
   String` and `showText : Maybe String -> String` fails 4.R9; with `W * String` passes.
3. Next speedup: `kernel.step` rebuilds its environment and constructor table from the whole
   program on every call; likely most of the remaining 32 s.

Decisions of the agent: pattern-bound values shared; top-level constants shared per run
([proposed]); arguments always wrapped under a lambda head; the read test's counting extern
gives `W * String`; the comment fixed.
