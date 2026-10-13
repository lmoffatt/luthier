# Checker specimen, 2026-10-13

Sources: `program.lth` at ba322cd (later comments read at workspace HEAD c62837203d3fc6f09af290b52f4430756caa8128), chapters 3, 4 and 11, `tests/spec/README.md`, existing parse/elaborate/kernel. Derivation: user brief 2026-10-13, Codex checker v1; deterministic, no seed or generation parameters. No commits, as requested. Only the five authorized files changed.

Implemented surface predicates, partial rules-needed `Typing`, three reports, CLI failures and verbose reports, handwritten violation/clean law domains, and CHECKER integration with cited-rule checks and strict xfails. Parse errors reject once at the adapter level; CLI prints their diagnostics. Current `-- expect:` is enforced; historical and proposed fragments are preserved without prescribing wording; verdict overrides are read.

Validation: dedicated suite 64 passed, 20 strict xfailed. Full suite: 368 passed, 20 strict xfailed in 53.89 seconds. System python lacks pytest; commands use PATH=/tmp/luthier-grammar-render-venv/bin:$PATH and PYTHONPATH=src. No failures in other agents files in the completed full run.

## Choices and undecided places

- Proposal: use exactly this chapter 3/11 core vocabulary: `Bool Empty Fin Float64 Int List Maybe Nat Rational Real String Unit and axiom cons extern false fromInt implies just left nil not nothing or primitive right toFloat64 true unit`. Library names such as cite, Law and Failures are not implicitly added. W and U are surface constructors, not free names. Chapter 11 conversion names included only where it identifies them as core; Array/Vec/Mat remain aliases supplied by libraries/programs. The core is unwritten, so this list is an explicit choice.
- namePrefix splits before the first dot; nameSuffix after the last; undotted names remain unchanged.
- R2 implements existence only. Type-position checking and the full SCC reading are deferred, including theory membership/exceptions. No filename heuristics are used by the checker.
- Literal namesIn subtracts exact binders, so c does not remove c.parse. Literal theoryHeads recurses on a suffix: a prior declaration does not make a single-law head claim its law. Both are theory/specimen disagreements with intended fixtures; see strict xfails below. Neither was silently repaired.
- R5 uses its complete written predicate: only a bare named undefined extern type is tested, not undefined arrow components. provisional is presence of the named argument, irrespective of its value, as written.
- R3 touches syntactic names, not whether a law states a constructor role. R10 remains author judgement; R11 has branchContext and its constructed law cases, no rejection predicate. R13 and S23 remain translation.lth elaboration laws. R12 follows blockFault exactly, without the separate 2.R6 use-before-rebinding rule. Loose functions are reports even though local blocks parse: the theory expressly reports them.
- Typing uses bounded weak-head reduction (number of acts + 1) then alpha equality; this is a finite approximation to definitional equality. No full normalization, unification, dependent checking, refinement proof discharge, exhaustive matching or generic structural equivalence. Function variance includes Float64 refining Real. Unknown inferred types stay unknown. Match applications retain the theory applications traversal without pattern contexts; branchContext exists but elaborated match contexts do not reconstruct surface conditions.
- Existing parse supplies no source spans on acts: CLI locates the first matching unindented name line (fallback line 1). Existing elaborate overwrites an earlier declaration with Hole on a later unannotated definition: specimen reconstructs the written declaration for comparison. It still leaves untyped predicate lambda domains as Hole, lacks overload ambiguity and library/citation interfaces, and raises for unknown named arguments. ElaborationError suppresses only type-dependent predicates so surface rules still run; no new rejection rule is invented. Existing kernel supplies substitution, alpha and reduction, no typing, complete equality decision, module loading, or host interface validation.

## Laws

All WellFormed ReportsViolations laws have handwritten positive cases; ReportsNoFalseFailure has clean cases for all rejection predicates (the theory requires it only for R1/R4/R5/R7). ReportsOnItsNames and ReportsWhen/ReportsOnlyWhen have cases. R10/R11 have no violating domain in program.lth. The constructed Typing cases exercise every named Typing law; no observed failure of those finite law cases. This is not universal certification. None of the fixture discrepancies is waived as a passing test.

Unmet intended verdicts and rule attribution are listed below. R6 cannot meet the intended predicate-body case `r6_predicate_body.accept.lut` with an untyped lambda domain; it produces R6 Even. Complete SCC/type-position behavior remains unmet in r2_definition.reject and r2_unclaimed_laws.reject (the latter rejects through the separate literal dotted-name problem). R5 arrow completeness remains unmet in r5_extern_over_declared.reject. These are limits of the specimen/spec reading, not claims that the finite WellFormed laws failed. Full definitional SameIsAlpha/equality and all quantified Typing laws beyond the constructed domains remain unproved under bounded reduction.

## Every specification program

| Program | Intended | Actual failures (accept if empty) | Status / reason |
|---|---|---|---|
| cite_not_reference.reject.lut | reject | 4.R2 Resolvable: every name a definition mentions exists.; 4.R2 main: every name a definition mentions exists. | strict xfail: 6.R1 citation typing is outside program.lth. |
| cite_proved.accept.lut | accept | 4.R2 Resolvable: every name a definition mentions exists.; 4.R2 main: every name a definition mentions exists. | strict xfail: Literal dotted binder subtraction; cite is not a chapter 3/11 core interface. |
| k_bool_is_sum.accept.lut | accept | accept | pass |
| k_dependent_product.accept.lut | accept | accept | pass |
| k_empty_unit.accept.lut | accept | accept | pass |
| k_label_order.reject.lut | reject | accept | strict xfail: 3.R1/3.R2 checking of inline definitions is absent. |
| k_named_product.accept.lut | accept | accept | pass |
| k_recursor.accept.lut | accept | 4.R6 Recursor: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters.; 4.R2 RecZero: every name a definition mentions exists.; 4.R2 RecSucc: every name a definition mentions exists.; 4.R9 add: application argument bases must refine domain bases, with function variance. | strict xfail: Literal dotted binder subtraction and incomplete inferred lambda typing. |
| k_sum.accept.lut | accept | accept | pass |
| k_union.accept.lut | accept | 4.R2 c: every name a definition mentions exists. | strict xfail: Constructors of alias sums are not in knownWhole. |
| n1_numbers.accept.lut | accept | accept | pass |
| n2_r_gone.reject.lut | reject | 4.R2 x: every name a definition mentions exists. | strict xfail: 11.R1 is detected as unknown name 4.R2, not a numeric rule. |
| n3_primitive_outside_core.reject.lut | reject | 4.R4 Money: a new type at U is data, a subtype, a record with a law, or an extern. | strict xfail: 11.R2 file policy is absent; 4.R4 alone rejects. |
| n4_axiom_outside_lib.reject.lut | reject | accept | strict xfail: 11.R3 file policy is absent. |
| n5_arrays.accept.lut | accept | accept | pass |
| r12_block.accept.lut | accept | 4.R2 shift: every name a definition mentions exists.; 4.R9 main: application argument bases must refine domain bases, with function variance. | strict xfail: Literal dotted binder subtraction and incomplete inferred lambda typing. |
| r12_defaults.accept.lut | accept | accept | pass |
| r12_defined_twice.reject.lut | reject | 4.R12 f: defined twice: define once; a block may neither redefine an enclosing name nor rebind a := name. | pass |
| r12_named_unknown.reject.lut | reject | accept | strict xfail: 2.R1 elaboration failure has no program.lth rejection predicate. |
| r12_rebind_defined.reject.lut | reject | 4.R12 f: defined twice: define once; a block may neither redefine an enclosing name nor rebind a := name. | pass |
| r12_toplevel_arrow.reject.lut | reject | syntax: expected ':', ':=' or clause, '='; got '<-' | pass |
| r12_unused_rebinding.reject.lut | reject | accept | strict xfail: 2.R6 use-before-rebinding analysis is absent. |
| r13_operator_by_type.accept.lut | accept | 4.R2 rep: every name a definition mentions exists. | strict xfail: Literal dotted binder subtraction rejects rep. |
| r13_two_models.reject.lut | reject | 4.R2 rep: every name a definition mentions exists. | strict xfail: 4.R13 ambiguity is an elaboration law, not implemented here. |
| r1_declaration.accept.lut | accept | accept | pass |
| r1_declaration.reject.lut | reject | 4.R1 nRows: a declaration mentions only existing names. | pass |
| r2_definition.accept.lut | accept | 4.R3 Codec: predicates touch all labels/binders, theories all fields, data all constructors through claimed laws.; 4.R6 Codec: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters.; 4.R2 RoundTrip: every name a definition mentions exists. | strict xfail: theoryHeads suffix loses prior declaration; dotted binder subtraction; incomplete theory body typing. |
| r2_definition.reject.lut | reject | accept | strict xfail: 4.R2 type-position and SCC half deliberately deferred. |
| r2_unclaimed_laws.reject.lut | reject | 4.R2 RoundTrip: every name a definition mentions exists. | pass |
| r3_connected.accept.lut | accept | accept | pass |
| r3_dangling_label.reject.lut | reject | 4.R3 Semi: predicates touch all labels/binders, theories all fields, data all constructors through claimed laws. | pass |
| r3_true_predicate.reject.lut | reject | 4.R3 Tagged: predicates touch all labels/binders, theories all fields, data all constructors through claimed laws.; 4.R6 Tagged: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters. | pass |
| r4_data_nonrecursive.reject.lut | reject | 4.R3 Color: predicates touch all labels/binders, theories all fields, data all constructors through claimed laws. | pass |
| r4_product_inline.accept.lut | accept | 4.R2 first: every name a definition mentions exists. | strict xfail: Literal dotted binder subtraction rejects first. |
| r4_product_named.reject.lut | reject | 4.R4 Stats: a new type at U is data, a subtype, a record with a law, or an extern. | pass |
| r4_recursive_data.accept.lut | accept | 4.R6 TreeFold: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters.; 4.R2 FoldLeaf: every name a definition mentions exists.; 4.R2 FoldNode: every name a definition mentions exists. | strict xfail: Literal dotted binder subtraction rejects fold laws. |
| r5_extern_over_declared.reject.lut | reject | accept | strict xfail: 4.R5 literal predicate checks only a bare named type, not arrow components. |
| r5_extern_provisional.accept.lut | accept | accept | pass |
| r5_extern_type.reject.lut | reject | 4.R5 Signal: a nonprovisional extern gives no type and needs a defined named type. | pass |
| r5_extern_value.accept.lut | accept | accept | pass |
| r6_body_type.reject.lut | reject | 4.R6 Even: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters. | pass |
| r6_predicate_body.accept.lut | accept | 4.R6 Even: a separately declared body's type fits T, a predicate over T, or Law T; peel common parameters. | strict xfail: Untyped predicate lambda domain remains Hole in existing elaboration. |
| r7_alias.accept.lut | accept | 4.R2 first: every name a definition mentions exists. | strict xfail: Literal dotted binder subtraction rejects first. |
| r7_alias_defined.reject.lut | reject | 4.R2 Stats: every name a definition mentions exists.; 4.R3 Stats: predicates touch all labels/binders, theories all fields, data all constructors through claimed laws.; 4.R7 Stats: an alias is neither declared nor defined. | pass |
| r8_equality_function.reject.lut | reject | 4.R8 Same: structural == is forbidden on a type containing an exponential. | pass |
| r8_equality_parameter.accept.lut | accept | accept | pass |
| r9_variance.accept.lut | accept | accept | pass |
| r9_variance.reject.lut | reject | 4.R9 z: application argument bases must refine domain bases, with function variance. | pass |

## Theory files themselves

`luthier check src/luthier/lib/*.lth src/luthier/lib/*.lut`: exit 1, 329 failures; 4.R2: 281, 4.R3: 20, 4.R6: 10, 4.R9: 18. No syntax failures. These diagnostics reject the current theories; they are not acceptance evidence.

| File | Failures by rule |
|---|---|
| checks.lth | 4.R2: 5, 4.R6: 1, 4.R9: 1 |
| ebnf.lth | 4.R2: 22, 4.R3: 1, 4.R6: 2, 4.R9: 5 |
| ebnf_model.lut | 4.R2: 1 |
| generators.lth | 4.R2: 20, 4.R3: 3 |
| generators_model.lut | accept |
| grammar.lth | 4.R2: 37, 4.R3: 1, 4.R6: 1, 4.R9: 11 |
| kernel_laws.lth | 4.R2: 59, 4.R3: 5 |
| kernel_models.lut | 4.R2: 3 |
| laws.lth | 4.R2: 20, 4.R3: 2, 4.R6: 2 |
| library.lth | 4.R2: 10, 4.R6: 1 |
| program.lth | 4.R2: 38 |
| term.lth | 4.R2: 46 |
| term_model.lut | 4.R3: 4, 4.R9: 1 |
| test.lth | 4.R2: 3, 4.R3: 4, 4.R6: 2 |
| translation.lth | 4.R2: 17, 4.R6: 1 |

## Input hashes

SHA-256 of the source files read for the specimen (records concurrent workspace contents, not a claim of a clean checkout):

- `src/luthier/lib/program.lth`: `9c8475dc9c287df0f4167835e014f94aed9a504e046cabea1cb6e28547d7c959`
- `src/luthier/parse.py`: `9f548b917e8784ac39e7e529f9a09013333203bcd7881e10d161a9c43ece16ce`
- `src/luthier/elaborate.py`: `c8a88a14212fa3b4e04d8a12674b538d4f860541b374b453503c376292f35e77`
- `src/luthier/kernel.py`: `57df94afdc0bc43f336083cb333a278d514eb9d57718834c0377293e85c5e164`
- `docs/spec/03-kernel.md`: `1a2138fe327d564af5d6ec50bbe51a122691c0fbcd122ecd762d2868c9c3c606`
- `docs/spec/04-static-semantics.md`: `939182844835642a9727affc1541346effa989dbf36380827011b91973cba0b9`
- `docs/spec/11-numbers.md`: `6723507ffb5dad5898254c4429098f9f58fb0e75b2fa47823557c07314ac56ff`
- `tests/spec/README.md`: `4e8715d986aafaa75b1cbb22fd50272f0d9996fb70ea16a66f39a7283fa3016e`

Own decisions: finite core vocabulary; literal predicates including their scope limitations; bounded type equality; preserve unknowns instead of inventing failure rules; static strict-xfail inventory; first act-name source line fallback. No other-agent files edited.
