# luthier test, bite 1: report

2026-10-14, Claude Opus 5.5 (an agent of luthier-1b), on `prompt.md` at 4438a51; saved by the
coordinator from the agent's final message. Files: `src/luthier/tester.py` (new), the `test`
command of `cli.py`, `tests/test_tester.py`, `tests/tester/{laws,cases,numbers_laws}.lut`.
Checks: test_tester and test_run 40 passed, 2 skipped; the suite 508 passed, 2 skipped, 7
xfailed; the numbers-laws test under `LUTHIER_SLOW=1` (2.5 min).

## What runs

`luthier test FILE [--seed N] [--fuel N]` (`--fuel` per case, default 1,000,000 [proposed]). The
file is loaded as `run` loads it (core, imports, host routes, run.py's Runner). Each top-level
`test` line (D9) becomes a definition reduced to test.lth's `TestSpec` with its defaults. The law
is a definition whose arrows are the quantified parameters; each case is the law applied to
values and reduced to `true`/`false`. ExhaustiveMode enumerates `Bool`, `Unit`, `Fin k`, `Int`
subtypes with literal bounds, non-recursive data, pairs, records and sums of those (a dependent
type reads the earlier values); else `NotRun` with the reason (7.R3 infinite, 7.R4 functions and
theories, 7.R2 `U`). SampledMode draws `n` cases from `random.Random(seed)`: Int and Float64
within literal bounds else [-s, s], Nat in [0, s], String up to length s, Bool, Fin, data, lists,
pairs, records; subtypes by a filter; the metric ignored (said on the line). Bindings follow
generators.lth's `resolve`; a binding's generator names a census (one value or a list's
elements). Evidence is laws.lth's `Points` or `NotRun`; the verdict `ForallOnPoints`; the grade
from reducing test.lth's `grade`. One line per test; a host failure, stuck match or spent fuel
reported on its case; exit 1 when a test has no grade.

## Points test.lth or spec 7 did not decide (the agent's choices)

1. Exhaustive coverage `Exhaustive` for fully enumerated finite types, as `specCoverage`'s
   comment and `ForallOnPoints` say; this contradicts test.lth's `CoverageIsTheWeakest`, which
   wants `Bounded size`: for test.lth's author.
2. A case whose reduction raises is not counted toward `n` (7.S12), reported, `Unsettled` unless
   another case refutes; not redrawn.
3. A filter giving nothing within `tries` makes the law `NotRun` (7.S6); `drawsPerCase`,
   `redraws` not read.
4. All `n` cases run after a refutation (`CountsCases`), no early stop.
5. A binding names a census; generators, covering arrays, size schedules, list enumeration under
   exhaustive, recursive data other than `List`, the entry store (7.S9, 7.S13) are later bites.
6. Coverage weakened by every binding in `where` and the profile, as `specCoverage` does.
7. `{ x y : A | p }` turned into a subtype of the record inside tester.py (the elaborator refuses
   record refinements).
8. Name clashes: run.py's `load` flattens imports whole, so names defined by several libraries
   collide (`LeqPair`, `LeqChain`, `LeqBoth`; `PlusCommutes`; `NonNegative`). tester.py's `Scope`
   renames each clashing name `name@file` and resolves per file; a workaround that belongs in
   run.py's loader (`luthier run` has the same latent problem).
9. The String alphabet [proposed]; `--fuel` per case; a missing upper bound defaults to s above
   the lower bound.

## Findings for others

- One name, two meanings: generators.lth imports `Exhaustive` (a `Coverage` constructor) and
  defines a theory `Exhaustive`; test.lth's `Grade` constructor `Assumed` clashes with laws.lth's
  `Evidence` constructor `Assumed`.
- run.py's Runner calls `inspect.signature`, which fails on `math.log`; every law using
  `elementary.log` raises on every case: run.py's (take the arity from the declared type).
- The Runner is slow, 10 to 20 ms per case.

## What numbers.lth's laws gave (tests/tester/numbers_laws.lut: each model a census of one,
`tol` 1e-12 [proposed], seed 0, n = 100, sizes 10 and 1,000,000)

Nothing refuted. Sampled: all 20 `Doubles` laws with parameters but `LeqAntisymmetric`;
`DivisionAlgorithm`, `RemainderOfTheDivisorsSign`, `QuotientOfProduct`; `ConvertAddsExactly`,
`ConvertSucceeds`, `ConvertKeepsOrder`; `SqrtMonotone`, `SqrtOfSquare`, `ExpPositive`, `ErfOdd`,
`ErfBounded`, `SqrtSquares`, `ExpAdds`. Cases: `EpsilonIsTheUlpOfOne`, `ConvertZeroAndOne`,
`SqrtOfSquares`, `ExpOfZero`, `ErfOfZero`. Not run: `LeqAntisymmetric` (its `LeqBoth`, `x <= y and
y <= x` over continuous doubles, has zero acceptance: "no value of LeqBoth in 2000 tries (7.S6)";
7.S6 says such a subtype is built constructively: a finding for numbers.lth's author). Unsettled:
`LogOfOne`, `ExpOfLog`, `LogOfExp`, `LogMultiplies`, only by the `math.log` failure. Caveat: with
the metric ignored, `Moderate` is drawn uniformly in [-s, s]; magnitudes near 1e-150 and 1e150
never reached.
