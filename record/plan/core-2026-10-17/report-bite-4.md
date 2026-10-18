# Bite 4, typing for resolution: report

2026-10-18, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-bite-4.md` of this
folder (execution.md §2.2, §2.3 and §6, bite 4; D-2026-10-18-a, -b, -c, -f, -g). Started at
3b18771; bite 4b landed beside it (a75b220, ff84a28, dcdbab2).

## Commits

- 05360df elaborate.py: `infer` total on the library, the core as the elaborator's prelude,
  operators and the names of a structure resolved by type (rule 2.2).
- 9be2973 check.py: each act typed in the whole file's context, the typing's refusals reported,
  4.R9 reading a body against its annotation, 4.R2 knowing the fields of a structure.
- 84b327c run.py: a run's slice reaches the claims of a structure whose field it uses.
- 1fda944 elaborate.py: an operator bound under type parameters reads its domain at the left
  operand's instance.
- c60007a seven programs in tests/spec/.
- eaab3f7 tests/test_elaborate.py and tests/test_check.py.
- 19bff24 elaborate.py: a lambda applied where it is written takes its parameters' types from its
  arguments (test_certify's binder-annotation case, `(fn k { k + 1 }) x`).
- e48fa29 the 14 stores bite 4b's confirmation wave wrote against this bite's cones, with the lines
  it had not reached (arrays_laws 11, optimization_laws 3, probability_laws 18,
  sonolocalizacion_laws 5, sonolocalizacion_controls 3), run by this bite's first certify.
- this commit, the report and the plan's Status.

## What was built

(a) `infer` gives every term the library writes a type or raises `Untyped` naming it: names,
literals, lambdas, applications (a polymorphic constructor or function instantiated by matching its
domain against the argument's type, at the carrier of a subtype), projections (through a theory's
record and through a type's definition, a later field naming an earlier one), `match` (each pattern
variable typed from the scrutinee), blocks, records, tuples, subtypes, refined records (as the
subtype of their record, the form tester.py's `_refined_records` writes before a run). Where
nothing fixes a type, the parameter of a lambda with no expected type, the element of `nil`, the
type is a named unknown `?x3`, the principal type's variable; `Hole('type')` is never a result.
Expected types reach record values, tuples, lists and the branches of `match` and `if`. A `&` of
laws over different variables (core.lut's `CoreData`, bite 2's `Equivalence` written bare) is a
verdict, `Bool` or `Law` when a part is one, each conjunct quantified on its own (D-2026-10-18-f;
the coordinator's request after bite 4b, tests/spec/k_bare_conjunction.accept.lut).

The core is the elaborator's prelude (12.S22): core.lut and the files it imports are read once and
seed every context; a file sees core.lut's own names, the imported structures type them.

(b) The structure table: a structure is a name declared at a record with parameters; a claim `X
(binders) : Bool := S args m` binds the model `m` of `S` at `args`, read from every act a context
holds. No second act.

(c) A field used unqualified is resolved by the type of its discriminating argument, the first
whose type is headed by a parameter of the structure, matched against each claim under
instantiation and through the type's bases (`Nat` to `Int`); the field's leading `(A B : U)`
binders are its type arguments, written or inferred from the other arguments. `S.f` names the
structure, `S.f m` the model as well. A parameter typed by a structure applied to types, omitted
at a call (the argument in its place is not a model of it), is filled with the model its types
name; another passed by name is the author's (D-2026-10-18-g); a graded structure's bound is never
filled. Operators match their binding under instantiation (`List A` against `List Int`) and through
a subtype to its base. The elaborated term of a resolved field is the claim's model projected, what
`S.f m` with that model elaborates to.

(d) Failures are `TypingError`s with the rule check reports them under: 4.R13 for a name no model
resolves (the field, the type found, the models claimed; two structures with a model at the type
ask for qualification; two models of one structure are two types), 4.R9 for a type that does not
fit (an operator's right operand, a body against its annotation, a projection of a field the
record lacks). The bare fallback is gone: an operator whose left operand's type is unknown or names
no model is refused. Kept: a left operand the context does not name at all (an import not loaded)
stays the symbol, since 4.R2 refuses the name.

check.py elaborates every act in the context of the whole file, its imports and core (before, it
fell back act by act alone, where an act lost the types of its neighbours); `-v` says how many acts
are typed, and an act left out for a typing refusal is reported as a failure.

## The acceptance criteria

- Bite 2's three probes and item 39 refused: `r9_partial_application`, `r9_missing_field`,
  `r9_operand`, `r9_body_not_bool` (`.reject.lut`). `r13_operator_by_type` and `r13_two_models`
  still accept and reject. `r13_structure_name.accept.lut` resolves `size` and `map` at `List Int`
  and `Maybe Int`, `eq` at `Int` and `String`; `r13_structure_ambiguous.reject.lut` is refused, and
  passes once `d` is written `Metric.d` or `Ultrametric.d` (`test_a_shared_field_name_is_resolved_once_qualified`).
- Every definition of lib/, examples/ and tests/tester/ (3285) elaborates in its file's context
  and its body's type holds no `Hole('type')`: `test_infer_is_total_on_the_library`. No library
  annotation needed a fix.
- The stores do not change: the runtime elaboration of every file (each definition's type and body
  in canonical form, as the hash reads them) is the same under the old and the new elaborator on the
  tree at 3b18771, but for `CoreData`'s type, which no store or line reaches; on the current tree
  every law's and test line's cone hash is the same under both (1328 in the 17 law programs, 1277 in
  the control programs, the interpreter's revision held fixed). The lines the first certify ran were
  bite 4b's wave, unfinished when its agent stopped; a second `luthier certify tests/tester/*.test.lut`
  prints `0 lines ran` for all 38 programs, no law `not run` outside the fixture cases.test.lut.
- Suite: 847 passed, 6 skipped, 9 xfailed (25 min).
- `scripts/check_spec.py`: its known finding (03-kernel.md:190 shares ten words with principles.md).
- `scripts/core_metrics.py`: homonyms 96, executive names shadowing 112, list helpers 427,
  unclaimed 137, loose 1974 (real 1341, the rest 633), as before.
- `check` over lib/, examples/ and tests/tester/: 6 failures, 7 before. Gone: pooling_controls'
  `everyEntry`, `latestOnly` (4.R9 refused `List (Maybe Seed * Nat)` where `List (Maybe Int * Nat)`
  is asked; `Seed` refines `Int`, the old rule did not look inside `List`). New: plot_cases.lut's
  `perms` (4.R9: functions into `Int` where `Fin 3 -> Fin 3` is asked, a literal crossing into a
  subtype in a codomain, the case of distances.lut's `pairI` and `pairJ`, refused before and now).
  Unchanged: those two and experiment_zero.run.lut's three 4.R2.

## Findings, kept for the hash

Three elaborations the old elaborator wrote wrong and this bite keeps, since correcting them moves
cones; the typing reads each as what it means.

1. `T * Float64` with `T : Concrete` (a subtype of `U`) elaborates to `*` applied, not to a product
   (generators.lth's `weightOf`, `before`, `occurs`, `firstWeightOf`, `allNonNegative`;
   generators_model.lut's `supportOf`; world.lth's `stateAfter`, `resultOf`). Corrected, the
   cones of these and of what reaches them move.
2. An alias parameter captures a record's field of the same name: inside an alias with parameter
   `n`, `Vec`'s `f : Fin n -> A` reads the parameter (experiment_zero.lut's `fit` and
   `transformOf`, `predicted : { n : Nat, f : Fin (3 * ...) -> Float64 }`).
3. A pattern variable named as another file's constructor in the slice is that constructor
   (distance_graph.lut's `schema name ->`, grammar.lth's `name`): check now hides the constructors
   of an imported file the file does not list (run.py's scoping); at run time the term is unchanged
   and the typing reads the name as the variable.

Also: `Real`, the ideal, has no arithmetic; a test of check used it and now uses `Float64`.

## For the spec's agent (4.R13 and 4.R9; docs/spec/04-static-semantics.md is not this bite's)

4.R13, added: A name of a structure is resolved as an operator is (D-2026-10-18-b). A structure is
a name declared at a record with parameters; a claim `X : Bool := S T m` binds the model `m` of `S`
at `T`. A field written unqualified is resolved by the type of its first argument whose type is
headed by a parameter of the structure, under instantiation and through a subtype to its base;
`S.f` names the structure, `S.f m` the model. A parameter typed by a structure applied to types,
omitted at a call, is the model its types name; another is passed by name (D-2026-10-18-g). No
model, models of two structures at the type, or two models of one structure at it, are errors that
name the field, the type and the models claimed. An operator with no binding at its left operand's
type is an error; core's bindings elaborate to the kernel's operation of the symbol (3.S17).
Files: r13_structure_name.accept.lut, r13_structure_ambiguous.reject.lut.

4.R9, added: A definition's body fits the type written for it, an operator's right operand fits
its binding's domain, and a projection names a field its record has. A type fits through its
definition and a subtype at its base (a value crossing into a subtype is checked where it crosses,
4.R5, or owes its predicate, 4.R11); a sum by its shape (3.R2); a record as the named product of
its fields, and one written with its labels by them. An argument refines its domain one way through
a type: a list of a subtype passes for a list of its base, not the other way.
Files: r9_partial_application, r9_missing_field, r9_operand, r9_body_not_bool (`.reject.lut`).

## Decisions taken in this bite (one commit undoes each)

- Core's operator bindings elaborate to the kernel's symbol, as a run has always reduced them.
- The elaborator's prelude is core.lut with what it imports; a file sees core.lut's own names.
- A type nothing fixes is a named unknown `?x`; `Hole('type')` is not produced.
- A conjunction of laws over different variables is a verdict, each conjunct quantified on its own.
- 4.R9 reads a body against its annotation leniently through subtypes and by shape (above); the
  application half falls back to a one-way refinement where the old comparison fails.
- A structure parameter is omitted when the argument in its place is not a model of it: a lambda,
  a literal, a list, a tuple never are; an argument of unknown type is kept as the model.
- A field's discriminating argument is its first whose type is headed by a structure parameter.
- The three findings above kept for the hash.
- check hides the constructors of an imported file the file does not list.
- runtime_slice reaches the claims of a field's structures, a name the act binds and `left`,
  `right` excepted.
- A record refinement elaborates to the subtype of its record.
- A lambda applied where it is written is typed from its arguments.

## Question

Correct findings 1 and 2 (the product written as `*` applied under a `Concrete` parameter, the
alias parameter capturing a record field), at the cost of re-certifying the generators, world and
sonolocalizacion lines whose cones reach those definitions, or leave them until bite 12 touches
those files? Recommended: in bite 12, where those files are rewritten anyway.

## Addendum, 2026-10-18: the coordinator's answer

Findings 1 and 2 go to bite 12, as recommended: written into execution.md's bite 12 (789d1d1) and
marked as known defects in the clauses they break (20431ef): 2.S8 for the product written as `*`
applied under a `Concrete` parameter, 4.R7 for the alias parameter capturing a record's field. A
third defect of the same kind, found while typing tuples, is marked in 3.S4 and given to bite 12
too: product types nest to the left (`(A * B) * C`), tuples to the right, where 3.S4 says both go
right; the typing compares products flattened.

Finding 3 is fixed (e6cabf2, af14c42, f905902): a pattern variable is a binder, never another
file's constructor. The loader (run.py's `Loaded.pattern`) already knew which names of a pattern a
file sees as constructors (its own, its listed imports', core's); the elaborator reads a pattern
against the constructors of every file in the slice, so a variable named as a constructor the file
does not see was read as that constructor. The loader now renames such a variable (`name` to
`name%var`) with its uses in the arm, and the elaborator's typing workaround is gone. Two
definitions were read wrongly: distance_graph.lut's `describe` (`schema name ->`, grammar.lth's
constructor `name`), whose arm never matched, so describing a schema violation stuck, and
term_model.lut's `stepApplication` (`App (Primitive name) i ->`), whose arm never matched, so the
model's step of an applied primitive fell to `Done`. The test (tests/test_run.py,
`test_a_pattern_variable_is_never_another_files_constructor`, two files, a run printing the
variable's value) fails with the loader before the fix. It is a pytest and not a tests/spec
program: the spec runner checks one file with no imports, and the defect needs two files.

Lines re-certified: none. No law's or test line's cone moves (2704 cone hashes of the 38 test
programs compared under the loader before and after, the interpreter's revision held fixed): no
certified cone reaches `describe` or `stepApplication`, so no certified behavior changed and no law
passed by the wrong reading. The examples' runs reproduce their records in the suite: 848 passed, 6
skipped, 9 xfailed.

Check failures left for the closing bite (13): distances.lut's `pairI` and `pairJ`, and
plot_cases.lut's `perms` (4.R9: functions into `Int` where `Fin 3 -> Fin 3`, or `Fin nodes`, is
asked; a literal crossing into a subtype in a codomain); experiment_zero.run.lut's three 4.R2
(`main`, `priorWidened`, `sigmaKnown`).
