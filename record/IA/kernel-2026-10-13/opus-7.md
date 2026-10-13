# kernel.py, bite 7: structural `==`, report

Claude Opus 5.5, 2026-10-13, for prompt-7.md. Source: term.lth §5 at 051e6aa (`PrimStructural`,
`PrimConstructors`, `EqualityStuck`). Changed `src/luthier/kernel.py` and `tests/test_kernel.py`; not
committed.

What kernel.py does now. `Primitive "=="` steps its left operand to weak head normal form, then its
right one if the left has a head `==` can compare (a constant, pair, record value, injection or
constructor of a data of the program); otherwise it is stuck, as before. With both in weak head
normal form it gives `Var "true"` or `Var "false"` in one step when both are closed values of
concrete parts: constants (integers, strings, floats by literal equality), pairs part by part,
records by field (by label, whatever the order), injections by label then value, constructors by
constructor then part by part (lists are `cons`/`nil`, the same rule, when the program holds their
data). Constructors carry an arity counted from the Pis of their type in the data. The `==` branches
of `_primitive` were removed as dead. Every clause of the three laws has a test, plus nested values,
lists, records in another field order, operand stepping and the stuck cases.

Readings where term.lth is silent, all taken as stuck (the brief's conservative reading, and the
"stuck otherwise" of codex-equality.md for term_model.lut): a part not yet a value (`1 + 1`, or a
defined name inside a pair), a free name, a constructor applied to fewer or more parts than its
type has, two values of different types (an integer and a float, a pair and an injection,
constructors of two different data), records with different labels or a repeated label, type
formers. The whole value must be concrete before anything is decided, so `Inj l hole == Inj r 1` is
stuck, not false.

Two consequences for the coordinator. First, world.lth's `agreement` compares
`d.describe before == (after, x)`; weak head reduction leaves the parts of that pair unreduced, so
under the stuck reading it still does not step unless `describe` returns literal parts. Making
`==` demand a part in place, as a match demands what its pattern inspects, would be a change to
term.lth (and term_model.lut), not a reading. Second, run.py's program has no data for core's
`List`, `Bool` or `Maybe` (elaborate.py knows `cons`, `nil`, `true`, `false` by name only), so in a
run `==` on lists and booleans is stuck until core's data enters the program; the tests put a List
and a Bool data in the program.

Checks: `tests/test_kernel.py tests/test_run.py` 68 passed (`tests/test_eval.py` named in the brief
does not exist; the `tests/eval/` programs run through test_elaborate.py and test_parse.py, in the full suite); `pytest tests -q` 443 passed,
7 xfailed.
