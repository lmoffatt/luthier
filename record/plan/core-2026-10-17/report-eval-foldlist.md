# Report: `luthier eval` left `all`/`any` over a list unreduced

## Reproduction (file `x.lut` = `x : Nat := 1`; `L` = `/home/lmoffatt/miniconda3/bin/luthier`)

Before the fix:
- `L eval x.lut 'all List String (fn x { x == "a" }) ["a"]'` printed
  `foldList String data { true : Bool; false : Bool } fn (a : Bool) {...} true fn (x : String) {...} (cons "a" nil) : Bool`
  (same for `any List String ...`, `all List Nat ...`).
- `L session x.lut` with the same line printed the same unreduced `foldList ...`.
- `size [1,2]` gave `2`, `map (fn x {x}) [1,2]` gave the list, and `foldList String Bool conj true (fn x {true}) ["a"]`
  gave `true`: only a term whose model the elaborator fills in (`all`, `any`, `member`...) failed.
  (Note: the brief's `all`/`any` take `F A f p c` now; `size List String [...]` is refused as a type error, `size [..]` is the form.)

After the fix: `eval` printed `true : Bool` for the first, `session` printed `true : Bool` for
`any List Nat (fn x { x == 2 }) [1,2]`.

## Cause

Not the evaluator and not an opaque `foldList`: the program `eval` runs did not contain `foldList`.
`runtime_slice` (src/luthier/run.py) keeps the cone of the entry by surface names, and reaches a
structure's claims (`ListIsFoldable`, which names `foldList`) only when a field is written free
(`size xs`) or qualified (`Indexed.size`) (rule 2.2 in its comment). `all` is written
`f.fold A Bool conj true p c`, with `f` a parameter typed `Foldable F`: the name `f.fold` matched
neither case, so the claim was cut; the elaborator later filled `f` with `{ fold := foldList }` and the
`Var foldList` had no definition, so whnf was stuck. (Dump of the program's names for the probe: no
`foldList`, no `ListIsFoldable`.) `luthier test` programs reach it because they write or import
the claim's cone otherwise.

## Fix

`runtime_slice`: a dotted name `root.field` where `field` belongs to a structure and `root` is a local
binder (or not a definition) also reaches that structure's claims. One hunk, run.py; no elaborate.py.
Test: `test_eval_reduces_a_term_over_the_cores_foldable_model` in tests/test_run.py (3 terms; failed
3/3 before, passes after).

## Checks

`python -m pytest -q tests/test_run.py tests/test_elaborate.py tests/test_check.py`:
`302 passed, 3 skipped, 2 xfailed in 467.40s`.

## Decisions taken on my own

1. The fix goes in the slice (extends rule 2.2 to `f.fold`) rather than in the elaborator; one commit undoes it.
2. The slice grows for any term using a field through a binder: it can only include more claims.

## Question

None. Bite 10's differential on term.lth and term_model.lut can now be rerun.
