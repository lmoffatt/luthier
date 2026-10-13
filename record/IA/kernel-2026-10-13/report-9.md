# kernel.py, bite 9: the primitives of the numbers and strings, report

Claude Sonnet 5.5, 2026-10-14, for prompt-9.md. Source: term.lth §5 at 681742e (`PrimInt`, `PrimFloat`, `PrimString`, `PrimConvert`), core.lut. Changed `src/luthier/kernel.py`, `src/luthier/cli.py`, `tests/test_kernel.py`; not committed.

kernel.py: `_primitive` now does Int `/` and `mod` by floor (zero divisor: no step), Int and Float64 `<=`, `>`, `>=`, `/=` (Float64 also `<`), Float64 `-`, `*`, `/` (zero divisor: no step; a NaN or infinite result, including overflow, gives no step, since the kernel has no error channel and 11.S7 says no constant), String `+`. Mixed types and String `-`/`<` stay stuck. `toFloat64` on an Int constant steps to the nearest double (an Int too big for a double: no step); its argument is reduced first. A body `primitive "<name>"` is `Primitive "<name>"` as before. New `BOOTSTRAP_PRIMITIVES` (all operators plus `toFloat64`), used by `eval_at`.

`and`/`or`: the kernel had none; added a step on `Var "and"`/`Var "or"` (only when the program does not define the name), left operand reduced first, then `true and j` -> j, `false and j` -> false, `true or j` -> true, `false or j` -> j (the right operand is not demanded when the left decides); a stuck left operand leaves it stuck. Proposed reading, term.lth is silent.

cli.py: the bootstrap defines every name of `BOOTSTRAP_PRIMITIVES` as `Primitive name`. A reversible choice for tonight; the alternative, resolving through core.lut's `operator` acts, is for a later bite.

Tests: four new tests (division/mod by floor and zero divisor, comparisons, float ops and overflow, string +, toFloat64, names through Define, and/or including stuck and a program's own `and`).

Checks: `tests/test_kernel.py tests/test_run.py` 80 passed; full suite 454 passed, 7 xfailed.

Decisions taken on my own: no step (not a raised error) for float overflow/NaN; `and`/`or` short-circuit semantics; `and`/`or` skipped when the program defines the name.
