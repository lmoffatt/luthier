# check.py bite 6: report

2026-10-14, Claude Opus 5.5 (an agent of luthier-1b), on `prompt-6.md` and `report-5.md`, at
ed4d958; saved by the coordinator. Files: `src/luthier/check.py`, `tests/test_check.py` (7 tests
added); `LIMITATIONS` unchanged. Tests: test_check and test_spec 128 passed, 7 xfailed; the suite
509 passed, 2 skipped, 7 xfailed.

## What changed

1. Typing act by act (`typed`, `typed_part`, `typing_for`): the file with its imports; else the
   file alone; else act by act (every act the elaborator reads alone kept; operators tested in
   context; if the kept acts fail together, added one at a time, operators last, each kept only
   if everything kept still elaborates). An alias is tested alone as a declaration of its value
   under its binders. 4.R6, 4.R8, 4.R9 and 6.R1 on a name with an untyped act say nothing, as
   before; 4.R13 falls back to the surface signature when either function is untyped.
2. `unclash`, `rename_free`, `field_labels`, `_map` removed (kernel bite 11); the `Orthogonal`
   test kept; arrays.lth still clean.
3. The `-v` line comes from `report()` as the first item, kind `typed`, reusing the typing
   `check()` computed last: `path:1: typed 38 of 42 acts: not typed: LeqPair (record refinements
   require check.py); ...`, or `the whole file elaborates.`

## Three fixes plainly the checker's

- Holes inside a record: `refines` lets a hole pass inside a record whose labels match, field by
  field (cleared algebra.lth `FieldIsOrdered`).
- A recursive data type in 4.R8: `contains_arrow` unfolds each name once per path (program.lth
  hit `RecursionError`).
- Speed: `constructors(p)` memoized on the program object: term.lth 508 s to 7 s, program.lth
  over 20 min to 12 s, kernel_laws 87 s to 3 s. Results unchanged on all 30 files.

## What the typing rules now refuse, per file

- algebra.lth (38 of 42 typed; untyped `LeqPair`, `LeqChain`, `LeqBoth`, `NonNegativePair`):
  4.R6 on `CompleteOrderedField`: the elaborator's limit (`infer` of `&` joins Boolean laws only;
  `SupIsLeast` is a `Law`; 5.S6 says a combination lifts each Boolean part). The checker refuses
  an unknown body type in 4.R6 on purpose; left.
- program.lth (192 of 195; untyped `Violating`, `Clean`, `RefinePair`): 4.R9 on `binderTypes`
  (lines 511-512): a real error of the file: `concat` (List String) on `List Surface`; should be
  `concatTerms`. For the theory's author.
- generators.lth (85 of 90), kernel_laws.lth (94 of 99; still bite 5's 4.R3 on `Initial`),
  numbers.lth (61 of 64), term.lth (104 of 108): no new refusal.
- core.lut (36 of 40): no new refusal; the same 4.R3 on `Unit`, `Bool`, `Maybe`, `List`; the
  four untyped acts are the operators bound to `floatPlus`, `floatMinus`, `floatTimes`,
  `floatDivide` ("operator needs a declared function type"): the elaborator's limit: with
  `Float64 : Real`, elaborate.py reads `Float64 -> Float64` as an implication.
Every untyped act is left out for "record refinements require check.py".

Decisions of the agent: the fallback order and the greedy step; an alias tested alone; a rule on
an untyped name answers nothing; the `-v` line through `report()`; holes field-wise; the cycle
guard; the memo; 4.R13's fallback; 4.R6's refusal of an uninferred body type kept.
