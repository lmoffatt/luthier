# Report: `luthier eval` leaves `textParts` and `textJoin` unreduced

Claude Sonnet 5.5, 2026-10-22, on `prompt-eval-text.md`. Input: 43f6d3d.

## Reproduction (`L` = `/home/lmoffatt/miniconda3/bin/luthier`, run in `src/luthier/lib`)

- `L eval term_model.lut 'freshName "x" ["x"]'` prints `term_model.lut: stuck match`.
- `L eval term_model.lut 'textParts "ab"'` prints `textParts "ab" : List String` (neutral, not an error).
- `echo 'freshName "x" ["x"]' | L session repro.test.lut` prints `session: stuck match`.
- Test program (`~/.cache/luthier-sdk/difft/repro.test.lut`: imports `test.lth` and `freshName`,
  `Fresh (u : Unit) : Bool := freshName "x" ["x"] == "x'"`, `test "Fresh" ExhaustiveMode`):
  `L test repro.test.lut` prints `Fresh: exhaustive, 0 cases, unsettled: 1 cases raised, the first at u = unit: stuck match (ran)`.
  So the three entry points agree.

## Cause

Not the slice and not a missing evaluator rule. `term_model.lut` lines 24-26 declare
`textParts : String -> List String`, `textJoin : List String -> String`, `natDecimal : Nat -> String` with
no body: holes (parameters), by its own comment ("Spec 11 gives String equality but no text
decomposition ... Parameters (holes), not invented core primitives"). Spec 3.S19: "A term that contains
a hole where the reduction needs a value does not reduce." `luthier eval` has no way to fill a hole
(12.S18 gives `--set` to `run` for holes of non-function type only; these are function holes and
12.S19's `eval` takes no `--set`). The kernel's string operations are `<>` (concatenation) and `==`; no
primitive decomposes a string. So `freshName`, `unqualified`, `canonName` (via `textAppend`) are stuck
by design wherever they reach a text hole, and the same on the old side (`appendText` had the same holes).

## Fix

None: the behaviour is the spec's (3.S19). A test that fails before and passes after cannot exist
without either a core string primitive (a decision for Luciano, spec 11) or a model of the text holes.
I added no test and changed no file under src, tests or docs.

## Checks

Differential, with a scratch model of the three holes on both sides: 241 terms, 241 equal, 0 differ, all
reduce to values; see `report-bite-10.md`, "Differential after the text fix". pytest not run: no code or
test changed. Worktrees `difft/old` and `difft/new` removed.

## Decisions taken on my own

1. Intended behaviour (spec 3.S19), so no fix; the alternative is a decision beyond one commit.
2. The scratch text model is a table plus `[s]`, adequate only for the strings in the terms.
3. No new test (none can fail before and pass after).

## Question

Should the core get a string primitive (split into Unicode scalars, join, decimal of a Nat) so that
term_model.lut's holes become definitions and `canonical`'s hash path can run in `eval`? It touches
P10 (the invariant of the type) and spec 11's "String is text".
