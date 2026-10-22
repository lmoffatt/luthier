# Report: the core's bite 13a, the machinery left before the core closes

Agent: Claude Opus 5.5, brief `prompt-bite-13a.md`, 2026-10-22. Started at 70532a8, beside bite
13b's agent (its commits interleave with these; every commit here staged by path). Scratch files
under `~/.cache/luthier-13a/`, not versioned: `checkall.sh` and its outputs (`checkall-item2.txt`,
`checkall-final.txt`), `run_pytest.sh` with one log per file in `pytest/`, and the scratch programs
`plus.lut`, `v/v.lut`, `dt/d_laws.test.lut`, `m/machine.test.lut`.

## Commits, per item

1. A structure whose laws fix its carrier (the coordinator's (a) on report-bite-12b.md's question).
   - da50146, check. 4.R6 accepts, past the parameters the conjunction repeats, a predicate over
     the structure applied to as many arguments as it has parameters: `Doubles (F : U) (d : Doubles
     Float64) := ...` (`fixes_carrier` in check.py). The sentence is in 4.R6, marked as the
     coordinator's decision of 2026-10-22. The conjunction keeps `F`, so the theory's laws still
     take its parameters first and the model after them (D-2026-10-13-o), and the claim is
     `Doubles Float64 model`, which `_claim` reads as it reads every other claim. Without `F`,
     `Doubles Float64` (the record) and `Doubles d` (the law) would both take one argument and the
     elaborator recursed on the binder's type. Test:
     `test_a_structure_whose_laws_fix_its_carrier_is_accepted_and_resolves_there` (test_check.py):
     4.R6 accepts it, `plus 1.0 2.0` elaborates to the model's field, and a conjunction over another
     structure is still refused.
   - be3129a, tester. The tester didn't run the new conjunction: "F : U: a parameter of type U has
     no generator (7.R2)". `fixed_carrier` binds the parameters the model's type fixes (`F` to
     `Float64`), and the entry records the binding as "Float64 (fixed by the structure's laws)".
     Test: `test_a_structure_whose_laws_fix_its_carrier_runs_at_that_carrier` (test_tester.py). On
     numbers_laws' `Doubles` line, cut to 20 cases, all 25 conjuncts ran.
   - 6910d0b, library. numbers.lth: `Doubles (F : U)`, its laws over `Doubles Float64`.
     numbers_model.lut: `doubles : Doubles Float64` and the claim `DoublesHaveTheOperations (model
     : Doubles Float64 <- doubles) : Bool := Doubles Float64 model`, gathered in `NumberModels`.
     `luthier eval` of `plus 1.0 2.0` in a file that imports `doubles` now resolves to `doubles`'
     field and demands its laws (stale until 13b's re-certification). The other uses of `Doubles`
     as a type changed to `Doubles Float64` in the same commit: arrays.lth (`gammaN` and the six
     summing laws), docs/concepts/tape.lth, tape.test.lut, arrays_controls.test.lut,
     numbers_controls.test.lut, and test_certify.py's fixture. The examples' `doubles : Doubles` are
     import lines, where the grammar takes a single name after `:` (`importName ::= name [ ":"
     name ]`) and nothing reads it but the printer, so they stay as written. The bindings' `type :=
     just "Doubles"` stay too, since a binding matches the head of the type.
2. 009fed0. `toList Vec Float64 v` took `v` as the `Foldable` model because `is_model_type`
   accepted any record, and `Vec Float64` unfolds to one (`{ n, f }`). A record is now a model of
   `S` only when it has `S`'s fields. Sentence in 4.R13. Test:
   `test_a_container_given_to_a_core_function_is_not_taken_as_its_model` (test_elaborate.py). On
   arrays, `toList Vec Float64 v` evaluates to `cons 1.0 (cons 1.0 nil)`.
3. 6cb3999. `operator_binding` drops a binding at a subtype outside the use's bases
   (`sibling_subtype`, as claims do since 18cba7e). Sentence in 4.R13. Test:
   `test_an_operator_bound_at_a_subtype_does_not_serve_a_sibling_subtype` (test_elaborate.py): `+`
   bound at `Wide` serves `Wide` and `Inner` (declared inside it), not `Narrow`.
4. cbfa4a8. Test only: `test_a_model_certified_by_its_passes_needs_no_control_at_that_model`
   (test_certify.py). `ops` is certified by its passes, and the only control refutes `Ops` on
   `wrong`, another model. certify reads the law as controlled and `luthier run` on `ops` isn't
   refused. It passed without a fix: run.py never reads controls, and certify.py's `serves` takes
   no entry that has a kind. 012b3ce keeps controls law-level.
5. 9fd7d8d. Why the reading was wrong: the current-hash controls of `MatMulTransposes` and
   `TraceCyclic` exist (`ControlRefuted` at the law entries' cones, 6fe44043… and 9e0ad97e…), but
   they were in numbers_model.cert.json. A control line on arrays_controls' own wrong `Arrays`
   (`noSwapT`, `traceTwice`) also binds `doubles`, and `claim_file` homed the entry with the first
   library model it binds, numbers_model.lut. That went against its own docstring and L10.12 ("the
   control lives beside the claim it controls, the file that states the law"). certify's status
   only reads the stores the same invocation's lines wrote, so it saw nothing at the current hash,
   only the controls of 2026-10-17 in arrays.cert.json at the old hashes, which gave "its controls
   are at another hash". The four other summing laws read controlled because their
   bound-too-small control binds `numpy` and was homed in arrays_model.cert.json, which the laws'
   lines also write.
   A control at another hash shouldn't count, and doesn't: it was run on another text of the law or
   of what the law reaches, so it doesn't show that the current law discriminates. D-2026-10-22-a
   (a control is the law's) is about which models it serves, not about which version of the law.
   The defect was the placement and the reading. Fix: a control line's home is the file that
   states the law (`law_file`), whatever library models it binds, unless that file is the test
   program itself; and `certify_file` also reads controls from the stores of the files that state
   its laws (`Outcome.law_store`). Sentence in 7.S19, marked D-2026-10-22-a. Test:
   `test_a_control_binding_another_library_model_is_kept_with_the_law` (test_certify.py): the
   control is written to the law file's store, not the other model's, and a certify of the laws'
   program alone reads the law as controlled.

## Checks

- `python -m pytest -q` on the five files, one after another, at 9fd7d8d: test_check 96 passed;
  test_elaborate 69 passed; test_tester 24 passed, 1 skipped; test_certify 60 passed, 2 skipped;
  test_run 140 passed, 6 failed, 3 skipped, 2 xfailed.
- The 6 test_run failures are stale stores, for 13b's re-certification. Each run is refused on
  `numpy: DotAgrees / MatVecAgrees / MatMulTransposes / MatMulAgrees / TraceCyclic / TraceAgrees:
  stale`, whose cones item 1 moved through `fp : Doubles Float64`:
  `test_vector_norm_through_numpy`, `test_matrix_product_through_numpy`,
  `test_checked_refuses_a_value_that_refutes_its_refinement[refuteIndefinite-...]`,
  `test_checked_runs_an_honest_host_and_records_the_count`, `test_vector_norm_under_checked` and
  `test_a_bound_maximize_runs_once`.

- `python scripts/check_spec.py`: only its known finding (03-kernel.md:192).
- `luthier check` on every file of lib, examples, docs/concepts and tests/tester: only
  the four refusals report-bite-12b.md finding 5 lists, all of them 13b's (distances.lut `pairI`
  and `pairJ`, experiment_zero.run.lut 4.R2, lists_controls.test.lut 4.R3, plot_cases.lut `perms`).

## Cones I expect moved, for 13b's re-certification

- Item 1: everything that reaches `Doubles`. Every law of numbers.lth §2 (`DivideOne` to
  `DivideInvertibleWithin` and the `Doubles` conjunction), whose model's type changed. In
  numbers_model.lut: `doubles`, `NumberModels`, and the new claim `DoublesHaveTheOperations` (no
  line yet; see decisions). arrays.lth's `gammaN` and its six summing laws with their controls.
  docs/concepts/tape.lth's `MetresWithin`. Everything in the examples that reaches `doubles`
  (distances, validate_graph, experiment_zero), so the run records get new keys. The `Doubles`
  conjunction's entries also gain the binding of `F`, a new identity, so its 25 conjuncts run
  again.
- Item 5: control entries are now written to the law's file. numbers_controls' and
  arrays_controls' controls that bind `doubles` go to numbers.cert.json and arrays.cert.json
  instead of numbers_model.cert.json, and the bound-too-small controls (`doublesThird` with
  `numpy`) go from arrays_model.cert.json to arrays.cert.json. The old entries stay where they
  are, at old hashes.
- Items 2, 3 and 4: none expected. The full check refuses no new file, and no file in the tree
  depended on a record being read as a model or on an operator reaching a sibling subtype.

## Decisions taken on my own (one commit undoes each)

- Item 1: the conjunction keeps the structure's parameter (`Doubles (F : U) (d : Doubles Float64)`)
  rather than dropping it, so laws keep taking the theory's parameters first and the model after.
- Item 1: the tester binds a fixed carrier's parameters from the model's type, rather than asking
  each test program for a census of `F`.
- Item 1: `Doubles` changed to `Doubles Float64` in arrays.lth, tape.lth and the test programs:
  the brief's "its uses", which would no longer check otherwise. The import lines stay `doubles :
  Doubles` (single-name grammar, unread).
- Item 1: no test line of its own for `DoublesHaveTheOperations`: its body is the `Doubles`
  conjunction on `doubles`, which numbers_laws already runs. A run demands the theory's laws on
  `doubles`, not the claim.
- Item 2: a record is a model of `S` when its fields include `S`'s (a wider record still counts).
- Item 5: placement and reading both fixed, rather than only widening the reading.

## Question

None.
