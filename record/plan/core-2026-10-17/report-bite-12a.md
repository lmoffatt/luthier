# Report: the core's bite 12a, the machinery before the library's re-certification

Agent: Claude Opus 5.5, brief `prompt-bite-12a.md`, 2026-10-22. Started at 76818b6, beside bite
12b's agent (its commits interleave with these). Scratch under `~/.cache/luthier-12a/` (not
versioned): `checkall.sh` and its output, `run_pytest.sh` and `pytest/*.log`, `prof/` (the one-line
test program, the cProfile output, the timing scripts and their outputs).

## Commits, per item

1. c054d5f. The three elaborations bite 4 kept for the hash (report-bite-4.md, findings 1 and 2, and
   the products' nesting). In `walk`, a left operand whose type is `U` or a subtype of it
   (`T : Concrete`) makes `->`, `*` and `+` the function type, the product and the sum (2.S8). A
   chain `A * B * C` whose first operand is a type is nested to the right, `A * (B * C)` (3.S4,
   `right_product`). A record's field name is bound in the types after it over an alias parameter of
   the same name (4.R7), and so are the binders of `(n : A) -> B`, `(n : A) * B` and the named sigma,
   as a lambda's parameters already were. The known-defect marks of 2.S8, 3.S4 and 4.R7 are replaced
   by the rule. Tests in test_elaborate.py: `test_a_type_typed_by_a_subtype_of_U_makes_a_product`,
   `test_products_nest_to_the_right`, `test_an_alias_parameter_is_not_captured_by_a_record_field`.
2. 18cba7e. A claim at a subtype serves a value of that subtype or of a subtype declared inside it,
   never a sibling (4.R13; docs/concepts.md 4.3). `solve` compares two subtypes by their bases alone,
   which is how `d` at `Mark` reached `IntIsAMetric` at `MetricInteger`; `claim_matches` now drops
   a claim whose instantiated carrier is a subtype not among the use's bases (`sibling_subtype`).
   The refusal is the existing "no model of Metric ... at Narrow; the models claimed: ...", which
   names the candidates. Sentence added to 4.R13. Tests:
   `test_a_claim_at_a_subtype_serves_it_and_the_subtypes_declared_inside_it`,
   `test_a_claim_at_a_subtype_does_not_serve_a_sibling_subtype`.
3. ee5f06f. A theory's laws demanded by name are served by its conjunction's entries
   (D-2026-10-18-f; report-verify-6-11.md, failure 2). The run demands each law of `Doubles` by its
   own name (`Neutral`, `TotalOrder`); the tester stores the entries under `Doubles` with the
   conjunct's text. Each demand now carries the theory law's demand for the model the run gives
   (run.py `_conjunction_demand`, with the conjunct heads the law stands for, `_Theories.leaves`, so
   `TotalOrder` reads through to `Reflexive`, `Transitive`, `Antisymmetric`, `Total`), and
   certify.py's `served` falls back to it when no entry of the law itself serves
   (`_served_by_conjuncts`). Sentence added to 7.S22, marked [proposed]. Test:
   `test_a_theory_s_laws_are_served_by_its_conjunction_s_entries` (test_certify.py), with another
   model of the theory left uncertified to show it is still refused. On the real case,
   `luthier eval` of `doubles.plus 1.0 2.0` now reads "1 certified, 15 vacuous", where `doubles:
   Neutral / Absorbing / Involutive / TotalOrder` were uncertified.
4. 3671c17, b8e427d. The spec was silent on whether an `operator` act travels with its file
   (2.S6, 2.S21, 4.R13 and 12.S22 read for it). I implemented export and wrote it into 12.S22 as
   [proposed]: check's `load_imports` brings the imported files' operator acts, scoped, and the
   run's `runtime_slice` keeps every operator act outside the core with the function it binds. The
   core's own bindings stay the prelude's. Test: `test_an_operator_act_is_exported_with_its_file`
   (test_check.py), with check and `eval` of `o + o` in a file that imports only the type. With
   arrays_model.lut, `a * a` and `v + v` now check in an importer, and `(v + v).f 1` evaluates to
   3.0.
5. 4f619bd. The per-case cost. cProfile of `TheThreeSourcesGrade` alone (270 exhaustive cases, no
   store): 711 s under the profiler, 699 s of them the reduction of the law's body
   (`run.whnf`, 8.2 million `kernel.step`, about 30,000 steps a case), and 475 s of it is
   `kernel.substitute`, 267 s of that computing free names. The same line, timed without the
   profiler at four commits: 132 s at 3e523d5 (which wrote the test), 147 s at 9e2857d (just before
   bite 9), 277 s at 8ef6389 (bite 9: certification.lth and test.lth on the core's folds), 284 s at
   7180f7b. So bite 9 doubled it, from about 0.5 s a case to 1 s, and the file was already slow
   before (bite 8's report saw it cut at 10 minutes). Raising the free-names memo's cap
   (`FREE_NAMES_MEMO_LIMIT`, 2^12 to 2^16 and 2^18) changes nothing (302, 292, 294 s): the terms
   are fresh at each step. The cost is the kernel's substitution on the longer reductions the folds
   give, in files that are neither mine nor 12b's; a faster kernel is a task of its own. The test
   is marked `LUTHIER_SLOW`, with the figures in a comment.

## Checks

- `python -m pytest -q tests/test_check.py tests/test_elaborate.py tests/test_run.py
  tests/test_certify.py tests/test_tester.py`, file by file at 3671c17 (before item 5's marker; the
  regions test deselected): test_check 95 passed; test_elaborate 66 passed, 1 failed; test_run 100
  passed, 46 failed, 3 skipped, 2 xfailed; test_certify 54 passed, 3 failed, 1 skipped; test_tester
  21 passed, 2 failed, 1 skipped.
- Every failure is one of two causes, neither a defect of these items:
  - Stale store, for 12b's re-certification: `src/luthier/lib/world.cert.json`'s console laws
    (`PrintAppendsALine`, `PrintChangesOnlyStdout`, `ReadGivesThePlace`, `ReadChangesNothing`), whose
    cones item 1 moved through world.lth's `stateAfter` and `resultOf`. That accounts for all 46 of
    test_run (each refused on those four lines alone, checked by running six of the programs) and
    the 3 of test_certify.
  - 12b's 61c14fa removed `allUnit` from probability.lth while generators_model.lut still imports
    it: test_elaborate's `test_infer_is_total_on_the_library` and test_tester's
    `test_a_binding_names_a_generator` and `test_a_generator_threads_its_seed_and_its_entry_names_it`.
    For 12b's agent.
- `python scripts/check_spec.py`: only its known finding (03-kernel.md:192).
- `luthier check` over the 105 files of lib, examples, docs/concepts and tests/tester after item 2:
  five refused, four the same at 76818b6 (distances.lut 4.R9, experiment_zero.run.lut 4.R2,
  lists_controls.test.lut 4.R3, plot_cases.lut 4.R9) and probability.lth, refused on 12b's
  uncommitted edit of `pooled` at the time, the same with the base's code. No file is newly refused
  by items 1 and 2.

## Cones I expect moved (for 12b's re-certification)

- Item 1, the product under a subtype of `U`: generators.lth's `weightOf`, `before`, `occurs`,
  `firstWeightOf`, `allNonNegative`; generators_model.lut's `supportOf`; world.lth's `stateAfter`,
  `resultOf`; and every law whose cone reaches them (the console laws seen stale above, the
  generators laws and their controls, and what reaches world_model.lut's console in the examples).
- Item 1, the nesting: every definition whose type has a product of three or more components
  written as a chain; its type is now `A * (B * C)`, so its cone moves wherever such a type occurs.
  I did not enumerate them.
- Item 1, the binders: experiment_zero.lut's `fit` and `transformOf` (and `Fit`'s users).
- Items 2, 3 and 4 move no existing cone: item 2 refuses no file of the tree, item 3 is on the
  serving side, and item 4 adds operators at types where uses were refused before.

## Findings left

- arrays_model.lut binds `* := matVec` and `* := matMul`, both keyed by the first operand's type
  (`Mat Float64`), so the second replaces the first: `a * v` is read as `matMul`. Bindings keyed
  by both operands would settle it; not done here.
- A law demanded with no model parameter (`doubles: Commutative`) is served by any passed entry of
  that law at its cone, whichever model the entry was about; this is why `Commutative` was never
  refused for `doubles`. Item 3 keeps that path first and adds the conjunction's. See the question.

## Decisions taken on my own (one commit undoes each)

- Item 1: the binders of a function type, a dependent product and a named sigma shadow an alias
  parameter too, beyond the record fields the brief named.
- Item 1: the parser keeps no parentheses, so a product chain is the left spine of `*`; an explicit
  `(A * B) * C` is read as `A * (B * C)`, and a parenthesized product on the right stays one
  component.
- Item 2: the restriction is in the claims' resolution; operator bindings (`operator_binding`) still
  go through a subtype's bases unrestricted.
- Item 3: the conjunction's entries serve in addition to the law's own, not in place of them.
- Item 4: an operator travels transitively and without being listed; a core binding is recognized
  by its function's name.
- Item 5: marked slow rather than rewriting the kernel's substitution.

## Question

Should a law demanded without a model parameter (`doubles: Commutative`) be served only by entries
about the model the run gives (its theory's conjunction entries), refusing what entries about other
models serve today? It closes a hole in what a run's certificate means; it costs refusals wherever
a model's theory has not been certified as a conjunction yet, until 12b's re-certification covers
them.

## Follow-up: serving by the run's model

The coordinator's answer to the question (2026-10-22): yes. 012b3ce, with 7.S22's [proposed]
sentence corrected in the commit after it. A demand whose law takes no model parameter is marked
`byModel` in run.py; certify.py's `served` serves it only by its theory's conjunction entries
about the model the run gives, and `refuse` reads its state from those entries, so another model's
entries of the law (core's own `Commutative` lines) neither serve it nor refuse it. The run's
record names, for such a demand, the conjunction entry that served it. Test:
`test_a_law_without_a_model_parameter_is_served_only_by_the_run_s_model` (test_certify.py): with
`ops` certified and `other`, another model of the same theory, never certified, `luthier run` of a
program on `ops` runs, and the one on `other` is refused naming `other: Commutative`, `Neutral` and
`Unital` (before, `Commutative` was served by entries about other models). `doubles` stays
certified (`luthier eval` of `doubles.plus 1.0 2.0`: 1 certified, 15 vacuous).

Checks, with the change: tests/test_certify.py 55 passed, 3 failed, 2 skipped; tests/test_run.py
100 passed, 46 failed, 3 skipped, 2 xfailed. The failing tests are the same ones as before the change
(compared by name), each refused on world.cert.json's four stale console laws, for 12b's
re-certification. `scripts/check_spec.py`: only its known finding.

Item 2's leftover, for bite 13: operator bindings (`operator_binding` in elaborate.py) still go
through a subtype's bases unrestricted, so an operator bound at one subtype can serve a sibling.
