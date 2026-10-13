# check.py bite 5: report

Written 2026-10-14 by a Claude agent (Claude Opus 5.5) on `prompt-5.md` (the prompt and its
addendum) plus two precisions of the coordinator (4.R13 compares the elaborated declared types
with the binders; the `Orthogonal` capture is the checker's); saved verbatim by the coordinator.
Inputs: the tree at 8376a42, program.lth at 02aa8af. Files: `src/luthier/check.py`,
`tests/test_check.py` (16 tests added, one assertion updated); one line of `cli.py`
(`check(result.program, path)`) went in with 14c9b98. Tests: test_check and test_spec 121 passed,
7 xfailed; the suite 493 passed, 1 skipped, 7 xfailed.

## Mirrored from program.lth (5f33db8, 02aa8af)

- Group 1 `fields_read`: a dotted name reads the field after the first `.`.
- Group 2 `law_names`: the constructors named by the patterns of a claimed law's own matches
  and clause patterns (`pattern_named`, `matched_in`, `body_matched`); a helper is still unread.
- Group 5 `lambda_is_predicate`: the lambda case of 4.R3 only when the written type ends in
  `Bool`, `Law` or `Failures E`; or no type written and the declared type is not a function or
  ends in a verdict; or nothing written or declared. Looks through an alias (4.R7), which
  program.lth cannot.
- 4.R3 `untouched`: `v.n` touches `v` (1.S7, [proposed] in program.lth). Law reads: binders'
  types and defaults count (`binders_reads`, [proposed]).
- 4.R4: a `primitive` body makes a type (11.R1). 11.R2 not read (`n3_primitive_outside_core`
  stays pending Luciano in `LIMITATIONS`).
- 4.R13 `rivalModel`: rivals when the elaborated declared types, binders included, are
  alpha-equal; the surface signature when the program does not elaborate.

## The brief's four items

1. Shape refinements (arrays.lth's seven, the port's three): pass with a projection touching
   its variable.
2. 4.R9 across imports: `check(program, path)` reads the file's imports for typing only (12.S4
   lookup: next to the file, `LUTHIER_PATH`, `lib/`; transitive; `as` as aliases); the rules run
   on the file's own names; an imported act the elaborator cannot read alone is dropped; if the
   whole still does not elaborate, the file is typed alone. Clears world.lth `agreement`,
   generators_model.lut `supportOf`, validate_graph.lut `summary` and `report`, arrays.lth
   `RankScales`.
3. 4.R4 on `primitive`, 4.R13 on inline-typed targets: fixed.
4. `x : Int := "three"`: no rule of chapter 4 refuses a body whose type differs from the type
   written on its own definition (4.R6 is the declared-then-bodied case, refused); the typing
   bite, after v0.2.

## 4.R9 in arrays.lth, three causes, and `Maybe Table`

(a) `refines` passes when either side is a hole. (b) `base` reads a subtype's base through
`arrows`. (c) `kernel.substitute` takes a record's field labels as free names (applying
`identity (n : Nat) : Mat Float64` to `k` rewrote the field `n`): fixed in check.py by `unclash`
and `rename_free` since kernel.py was outside the brief; the kernel's own substitution still
captures. `Maybe Table`: a theory head used as an argument is a type at `U` (`theory_head`).
All 41 of arrays.lth's 4.R9 refusals are gone.

## What `luthier check` still refuses (30 files, 27 clean)

| cause | file | names |
| --- | --- | --- |
| 4.R3 read on one file while the roles are elsewhere (question for Luciano) | core.lut | `Unit`, `Bool`, `Maybe`, `List` |
| same | laws.lth | `Coverage` |
| 4.R3 vacuous law, group 6 (the author's call) | kernel_laws.lth | `Initial` |

## A gap found on the way

Six library files do not elaborate as a whole (algebra, generators, kernel_laws, numbers,
program, term: "record refinements require check.py"); on them `check()` catches the
`ElaborationError` and 4.R6, 4.R8, 4.R9, 6.R1 answer "no violation": their clean verdicts under
those rules say nothing. The per-act filter used for imports could type the rest; a later bite.

Decisions of the agent: imports read for typing only and only with a path; a hole passes
`refines`; `unclash` in check.py; 4.R13's fallback; `lambda_is_predicate` through aliases; 11.R2
left unread.
