# Audit of chapters 2 to 4 for v0.2's status flips: report

Written 2026-10-14 by Claude Sonnet 5.5, on the brief `record/IA/opus-2026-10-13/spec-audit-v0.2.md`
(an earlier Opus run never delivered). Read only on the tree at commit 4c71da3
(`git rev-parse HEAD` at the start; other agents committed meanwhile, nothing here depends on
their later changes). Inputs: `docs/spec/02-grammar.md`, `03-kernel.md`, `04-static-semantics.md`,
`tests/test_spec.py` and, by grep, `tests/spec/`, `tests/*.py`, `tests/eval/`, `tests/run/`,
`src/luthier/*.py`, `src/luthier/lib/`. `pytest tests/test_spec.py` at this commit: 51 passed, 7
xfailed (the seven of `LIMITATIONS`); `scripts/check_spec.py` prints nothing. No seed, no parameters.

## How to read it

Criterion for `[implemented]` at v0.2: a specimen runs it and a test or a program shows so. For a
rule: an accept and a reject program of `tests/spec/` that both get their verdict in
`tests/test_spec.py` (not an xfail). For a statement: a test in `tests/` or a law in a theory.
Otherwise `[decided D-...]` (keep the id the text already cites) or `[proposed]`.

Four facts the flips depend on.

1. `check.py` is the 13 predicates of `program.lth` plus 2.R1, 2.R6 and 6.R1, not a type checker.
   An accept program "passes" when no predicate fires. Probe at this commit: `asBad (x : Int) :
   Bool := x` and `r : { n : Int, b : Bool } := p` with `p : (n : Int) * (b : Bool)` give no
   failure. So an accept program of `k_*` shows the parser and the predicates tolerate it, not that
   its typing or reduction is right. Reduction is shown by `tests/test_kernel.py` and `tests/eval/`.
2. The seven xfails: `n2/n3/n4` (11.R1 to 11.R3), `cite_*` (6.R1), `r2_definition.reject` and
   `r2_unclaimed_laws.reject` (4.R2 type-position and SCC half).
3. `luthier` has four commands, `parse`, `check [-v]`, `eval` and `run`. There is no `session`, no
   `run --checked`, no `run --set`.
4. `tests/eval/` (arithmetic, factorial, data, record, block, lambda) are run by `luthier eval` in
   `tests/test_elaborate.py::test_eval` with their values compared (19, 24, 2, 7, 3, 5). This is
   what 3 §4 said did not exist.

Column key: P = program of `tests/spec/` with its verdict in `test_spec.py`; T = test; L = law in a
theory; none = nothing. "False" = a sentence the specimens contradict.

## Chapter 2

| item | now | what the specimens do | at v0.2 | false text |
|---|---|---|---|---|
| 2.S1 Tokens | impl | T: `test_name_tokens`, `test_number_tokens`, `test_string_tokens`, `test_lex_errors_have_lines`; L: grammar.lth token laws | implemented | none (the `\"` `\\` `\n` clause, D-q, is covered by the string test; both statuses can stay) |
| 2.S2 Reserved words | impl | T: `test_other_words_are_names` makes `let in test with extern primitive axiom forget cite provisional` plain names; `gen` is absent from `parse.py` | decided D-2026-10-12-ab (2.S21 holds the set) | list "data, match, extern, provisional, test, with, exhaustive, import, forget, U, operator, if, then, else, cite, let, in, primitive and axiom"; "`and`, `or` and `mod` are ordinary names" (2.S8 and 2.S21 say reserved operators); "the parser still reads it today" (gen); "Replaced: 2.S21" makes the item a history |
| 2.S3 `<-` | impl | T: `test_arrow_is_one_token`; P: `r12_*` | implemented | none |
| 2.S4 Layout | impl + decided + proposed | T: `test_layout_ends`, `test_column_zero_starts_act`, `test_indent_continues_act`, `test_brackets_ignore_breaks`, `test_layout_classifies_brackets_from_the_prefix`, `test_break_separates_items/constructors`, `test_continuation_lines`, `test_blank_and_comment_lines_dropped` | implemented (the D-q readings are tested too); the `quote` braces clause stays `[proposed]` unless `test_layout_classifies_brackets_from_the_prefix` covers `quote` (not checked) | none |
| 2.S5 Acts | impl + decided + proposed | T: `test_declaration/definition/alias/data/clause/operator/import/datum_tree`, `test_default_tree`, `test_implicit_tree`, `test_trailing_separators`; `test_Shapes` (clauses elaborate to a `match` on the tuple) | implemented; the trailing separator after a list element: `test_list_tree` (check) else stays proposed | the production block: `act ::= declaration \| definition \| alias \| directive`, `body` with `primitive`/`axiom` and `"extern"`, `binder` without the implicit `{ }` form. 2.S9 says the value of `luthierSyntax` holds, but this block is not marked as superseded |
| 2.S6 Directives | impl, "Replaced" | no `cite`, `as` or `checked` form in `parse.py`; `import` is the act of 12.S22 | decided D-2026-10-12-ab (history) | whole item: "the directives other than `test` were as below" and the `directive` production |
| 2.S7 Defaults, named args | impl | P: `r12_defaults.accept`; T: `test_default_tree`, `test_named_arg_tree`, `test_Arguments`, `test_rebinding_parameters_lambdas_and_bind_reads` | implemented | none |
| 2.R1 Named argument | impl | P: `r12_defaults.accept` and `r12_named_unknown.reject` (rule 2.R1 enforced by `EXPECTED_RULE`); `violatesR2R1` | implemented | none |
| 2.S8 Precedence | impl + decided | T: `test_plus_before_times` ... `test_open_forms`, `test_open_form_ends_its_term`; L: grammar.lth precedence section | implemented | the old one-line table that omits the open forms and negation, and "`and`, `or` and `mod`... ordinary names" in 2.S2 contradict the D-p table; the first table can go |
| 2.R2 A type names its model | impl | P: `r13_operator_by_type.accept`, `r13_two_models.reject` (4.R13); T: `test_OperatorsByType`, `test_OperatorOfTheModel` | implemented | none |
| 2.S9 Terms | impl + decided | T: `test_parses_what_derives`, `test_parses_what_derives_luthier_syntax_act`, `test_render_grammar.py`; L: `luthierSyntax` is the parser's grammar | implemented | the second EBNF (`term ::= term op term`, `"\" lparam`, `"<" name ":" term ... ">"`, `let`, `forget`, `extern` as atoms, `"(" name ":" term ")" "+" ...`, `sep ... line break`) is a grammar the parser no longer reads; "kept as an explanation" now misleads. Also "`< >` and the form `(x : A) + (y : B)` are retired" is true, but the block above still lists them |
| 2.S10 Patterns | impl | T: `test_pattern_tree`, `test_Patterns`, `test_iota*` in `test_kernel.py`; L: grammar.lth, translation.lth | implemented | none |
| 2.S11 Dangling else | impl | T: `test_dangling_else`, `test_print_parenthesizes`; L: `PrintParenthesizesOpenIf` | implemented | none |
| 2.S12 The table | impl | L: translation.lth, one law per row (its index says done); T: `test_elaborate.py` (`test_ActsCurried`, `Lists`, `TypeForms`, `Negation`, `Conditions`, `Records`, `Arguments`, `Blocks*`, `Shapes`) | implemented for the rows with a test; the `Failures E` rows (`if c then a else b` with `holds`, `if c then a` reason form, `Failures E` = `List E`) and the `m.f` module row are in `elaborate.py`/translation.lth but 3.S12 and 5.S9 call `Failures` designed; mark those rows as decided | row `let p = e in body` (retired, kept in the table); the `m.f`, "a module is a record of its definitions" row has no test I found |
| 2.S13 The parser decides little | impl | T: `test_kinds_are_the_grammars`; L: translation.lth row "a bare name otherwise a variable" | implemented | none |
| 2.S14 Projection | impl + decided | T: `test_projection_tree`, `test_Records`, `test_bound_dotted_names_in_scopes`, `test_proj_of_record`; L: program.lth dotted names | implemented | the clause "it was a one-branch `match`" is history; harmless |
| 2.S15 `let` and negation | impl, "Replaced" | `let` is an ordinary name (`test_other_words_are_names`); negation: `test_negation`, `test_negation_tree`, `test_Negation` | negation: implemented; `let`: decided D-2026-10-13-o | "`let p = e in body` is `match e { p -> body }`" stated as implemented |
| 2.S16 Implicit parameters | impl | T: `test_implicit_tree`; `elaborate.py` Implicit (infers from explicit argument types and the expected type, 4.S23); no accept program | implemented (needs one T on inference, `test_elaborate` has none by name; `translation.lth` law exists) | none |
| 2.S17 Blocks | impl + decided | T: `test_block_or_record_value`, `test_rebind_pattern_*`, `test_Blocks*`, `test_fresh_names_avoid_capture`; P: `r12_block.accept`, `r12_pattern_rebind.accept` | implemented | "A file is never a block" and the `main` block: `run.py` runs `main` (tests in `test_run.py`); fine |
| 2.R3 Defined once | impl | P: `r12_block.accept`, `r12_defined_twice.reject` | implemented | none |
| 2.R4 What `<-` may rebind | impl | P: `r12_block.accept`, `r12_rebind_defined.reject`; also `r12_pattern_rebind.accept/.reject` | implemented | none |
| 2.R5 `<-` needs an order | impl | P: `r12_block.accept`, `r12_toplevel_arrow.reject` (a syntax rejection, `SYNTAX_REJECTIONS`) | implemented | none |
| 2.R6 Unused binding | impl | P: `r12_block.accept`, `r12_unused_rebinding.reject` | implemented | "and is allowed and reported in a session": no session |
| 2.S18 The session | impl | none: `cli.py` has no `session` | decided (the session's decision of 2026-10-11; O8 is open) | the whole item, in the present tense ("`luthier session [files]` (2026-10-11) types a block") |
| 2.S19 `test` directive | decided | none: `test` is an ordinary name | decided D-2026-10-06-ac, replaced by 2.S21 | "The parser today reads `test name [...]` and still reads `gen ...`" |
| 2.S20 Quote and unquote | decided | T: `test_quote_tree`; `elaborate.py` makes `App(Var quote, ...)`; `test_eval_computes`, `test_eval_constants_and_checks` for `eval_at`; grammar.lth `quote` | decided D-2026-10-12-ah; parser and `eval_at` exist, `eval A t : Maybe A` through the language is not a program | "draft 2 written 2026-10-13" of grammar.lth: grammar.lth is the value now |
| 2.S21 Keywords and names | decided | `luthierSyntax` literals are the parser's keywords (`test_literals_are_not_names`) | implemented for the keyword set; the rest (`test`/`cite` with named arguments) has no specimen | "The parser reads the older forms today" |

## Chapter 3

| item | now | what the specimens do | at v0.2 | false text |
|---|---|---|---|---|
| 3.S1 Three acts | impl | T: `test_ActsKept`, `test_ActsCurried`; `kernel.py`/`term.lth` `Declare`, `Define`, `Datum` | implemented | none |
| 3.S2 Bodies | impl, "Replaced" | `primitive`/`axiom` are applications (`Primitive`, `Axiom` terms); `test_axiom_text_stays_literal`, `test_prim*` | decided D-2026-10-12-ab (3.S39) | "Two further bodies exist, `primitive "..."` and `axiom "..."`" (bodies in grammar; now applications) |
| 3.S3 Directives | impl, "Replaced" | `import` and `operator` are acts of `luthierSyntax`; `test`, `cite` are functions; `gen` and `profile` are gone | decided D-2026-10-12-ab | "They are `import`, `test` and `gen`, `operator` and `cite`"; the `profile` `[proposed]` sentence |
| 3.R1 Names are binders | impl + decided | P: `k_named_product.accept`, `k_label_order.reject` (rule 4.R9) both verdicts; but the probe above: `check.py` accepts a record where `(n : Int) * (b : Bool)` is given, so the new specimens do not treat "one structure" as true or false | decided D-2026-10-13-x (the second paragraph), not implemented for the first | first paragraph: "`{ n : Int, b : Bool }`, `(n : Int) * (b : Bool)` and `Int * Bool` are one structure", "names ... are not part of the identity"; D-x's clause below contradicts it in the same item |
| 3.R2 A sum is identified by shape | impl | P: `k_bool_is_sum.accept` passes (nothing is checked), reject listed is `k_label_order.reject` (about record order, not sums) | decided D-2026-10-13-x contradicts it; hold at `[proposed]` or drop | "labels are binders" and "a value of such a sum is accepted where a `Bool` is expected"; D-x says labels are injections and part of the structure (3.R1, 2.S9) |
| 3.R3 `data` is freely generated | decided | P: `r4_recursive_data.accept`; T: `test_iota_skips`, `test_iota_constructors`, `test_data_are_frozen_and_cover_every_constructor` (distinct constructors); no reject program for freedom | decided D-2026-10-13-o | none |
| 3.S4 Anonymous sums, products | impl | P: `k_sum.accept`, `k_union.accept`; `elaborate.py` line 323 (`A + B` is `Sum((left, right))`); `test_TypeForms`, `test_sum_tree` | implemented | none |
| 3.S5 Dependence | impl | P: `k_dependent_product.accept`; T: `test_sigma_named_tree`, `test_lambda_argument_dependent_expected_type` | implemented | none |
| 3.S6 The subtype | impl | T: `test_subtype_tree`, `test_R9_named_subtype_bases_and_cycles`, `test_R9_core_Nat_and_Fin_are_subtypes_of_Int`; L: `RefinesItself`/subtype refines base in program.lth | implemented for the forgetting direction; the obligation on the other ("creates an obligation") has no specimen | none |
| 3.S7 Empty and unit | impl + decided | P: `k_empty_unit.accept`; L: kernel_laws.lth terminal/initial; core.lut | implemented | none |
| 3.S8 Kernel as category | impl + decided | L: kernel_laws.lth (exponential, product, coproduct, terminal, initial); `U : U` is decided | implemented (laws) ; the decided clause stays | none |
| 3.S9 Names | impl | T: `test_delta`, `test_holes_stay` | implemented | none |
| 3.S10 Match | impl | T: `test_iota*`, `test_pattern_priority_nested_demand_and_nonlinearity`; P: `k_sum`, `k_union` | implemented; "none repeated and none missing" has no reject program (no coverage check in `check.py`) | "none repeated and none missing": enforced by nothing |
| 3.S11 Recursion, recursor | impl + decided | P: `k_recursor.accept`; T: `test_fuel_exhaustion_and_long_reductions`; `tests/eval/factorial.lut`; `luthier eval --fuel` | implemented | none |
| 3.S12 Laws as terms | impl | `check.py` `verdict_type` takes `Bool`, `Failures`, `Law`; `elaborate.py` knows `Failures`, `holds`, `ok`, `failed` | implemented for `Bool`/`Law`; `Failures E` now taken by the checker | "A law into `Failures E` ... is not taken by the checker today"; "the cost type ... which the interpreter does not have" (unverified) |
| 3.S13 Extern | impl, "Replaced" | P: `r5_extern_value.accept`, `r5_extern_provisional.accept`; T: `test_extern_is_value`, `test_extern_remains_stuck`, `test_read_first_line` | implemented | "Its validation is `spec 10`" fine |
| 3 §4 header | n/a | tests/eval plus `test_kernel.py` compare values | edit | "3.S14 to 3.S18 have none yet, and their mark stays `[implemented]` for the interpreter until those programs exist" |
| 3.S14 Beta | impl | T: `test_beta`, `test_deep_beta_substitution...`; program with a value: `tests/eval/lambda.lut` (5) | implemented | the program named (`k_recursor` `\k r { succ r }`) uses the retired backslash; write `fn k r` |
| 3.S15 Delta | impl + decided | T: `test_delta`; program: `tests/eval/factorial.lut` (24), `arithmetic.lut` | implemented | none beyond the `\` in the program text |
| 3.S16 Iota | impl | T: `test_iota`, `test_iota_pair`, `test_iota_skips`, `test_iota_constructors`; programs: `tests/eval/data.lut` (2), `factorial.lut` | implemented | none |
| 3.S17 Prim | impl | T: `test_prim`, `test_prim_structural`, `test_prim_int_division_and_comparisons`, `test_prim_float`, `test_prim_string_and_convert`; program: `tests/eval/arithmetic.lut` (19); L: numbers.lth, term.lth §5 | implemented | programs named (`k_union` arithmetic, `k_dependent_product` comparisons) are only checked, not run |
| 3.S18 Extern | impl | programs run with a compared output: `tests/run/*.lut` through `test_run.py` (`read_first_line`, `table_cell`, `record_externs`, `vector_norm`) | implemented | "No k program ... reduces one" is true of `tests/spec`, no longer of the suite |
| 3.S19 Terms with holes | impl | T: `test_holes_stay` | implemented | none |
| 3.S20 Equality in the kernel | impl | L: kernel_laws.lth `Object`, `Structural`; T: `test_reflexive`..`test_substitutive`, `test_equality_*` | implemented | none |
| 3.S21 Two senses of primitive | impl | P: `n5_arrays.accept`; L: arrays.lth; `run.py` | implemented | `Fin n = { …}` text is garbled but not false |
| 3.S22 Bridge 1 | impl | T: `test_observe_through_the_bridge`, `test_crossing_errors` ("outside Fin 3", twice: 3 and -1) | implemented | none |
| 3.S23 Bridge 2 | impl | T: `test_vector_norm_through_numpy`, `test_matrix_product_through_numpy`, `tests/run/numbers.lut` | implemented | none |
| 3.S24 Bridge 3 | impl | T: `test_crossing_errors` (dimensions), `test_numbers_and_fin_functions`, `test_matrix_product_through_numpy`; `run.py` 3.S24 shape errors | implemented for 1-D, 2-D and the pair; "`Fin n -> A` non-numeric is a list": no test found | none |
| 3.S25 Bridge 4 | impl | T: `test_each_entry_once` | implemented | none |
| 3.S26 Observational equality | impl | no program or test found for lambda against array point by point | decided/proposed until a test exists (the bridge's types are tested, the comparison is not) | none |
| 3.S27 Order of a sum | impl | L: arrays.lth `sumTo` states the right fold; `tests/run/vector_norm.lut` | implemented | none |
| 3.S28 What is certified | impl | L: arrays.lth `Arrays`, `Agrees`-style laws (§4 "The leaves") | implemented (law stated); no model is certified at `luthier test` in this chain | none |
| 3.S29 Term and Program as data | decided | L: term.lth `Term`, `Pattern`, `Act`, `Program` as `data`, with the constructors listed in the "As written" paragraph; `term_model.lut`; `kernel.py` is the model | implemented (data defined, laws stated and tested in `test_kernel.py`) | "They are not in `core.lut` yet; the host's classes in `syntax.py` are their model" (`syntax.py` gone: `surface.py`, `term.py`); the table row `Term` lists 17 constructors, the paragraph above 22 (adds `World`, `Record`, `RecordValue`, `Proj`, `Let`); the `Act` row says "declaration, definition, alias, and the directives" (no alias, no directives) |
| 3.S30 Term is the kernel term | decided | `elaborate.py` produces `term.py` terms; L: translation.lth | implemented | none |
| 3.S31 Names are strings | decided | L: term.lth `AlphaCongruent`; T: `test_alpha_*`, `test_rename_bound` | implemented | none |
| 3.S32 Quote and eval | decided | `elaborate.py` quote; `kernel.eval_at`; T: `test_eval_computes`, `test_eval_constants_and_checks` | implemented as `eval_at`; `quote`/`eval` as language values: partial | "Neither is in the interpreter" |
| 3.S33 Reduction as a function | decided | L: term.lth §5 `step`, `reduce`; `term_model.lut`; `kernel.py` second specimen (`test_kernel.py`) | implemented | "The file is not written" (`lib/term.lut` of the first paragraph; the second paragraph corrects it) |
| 3.S34 Canonical form | decided | L: term.lth §4; T: `test_canon_of_alpha`, `test_canon_idempotent`, `test_unqualify_*` | implemented | none |
| 3.S35 No self-modification | decided | nothing tests it (a `Program` is data; no action edits it) | decided | none |
| 3.S36 kernel_laws | impl + decided | L: kernel_laws.lth, kernel_models.lut; T: `test_kernel.py` laws | implemented | "`KernelLaws A B` ... `luthier test` checks its models at `Fin 3` and `Fin 2` (`examples/kernel_finite.lut`, sampled)": the file and that command do not exist at v0.2; the later paragraphs (D-aa) are the current text |
| 3.S37 What it cannot state | impl | L: kernel_laws.lth `Structural` vs functions | implemented | none |
| 3.S38 term.lut | decided | term.lth written | implemented | "Not written" before the D-aa line |
| 3.S39 Constructs as names | decided | `primitive`, `axiom`, `extern` are `App`s in `elaborate.py`; `core.lut` uses them; 11.R1..R3 (restriction to core) xfail | decided D-2026-10-12-ab | none |
| 3.S40 An extern is a route | decided | T: `test_unused_extern_is_not_resolved`, `test_extern_in_a_record_is_read_when_projected`, `test_missing_file_is_nothing` | implemented (`run.py` reads on demand; `check.py` never imports a host module) | "Today the checker resolves every extern when it checks the file" |

## Chapter 4

| item | now | what the specimens do | at v0.2 | false text |
|---|---|---|---|---|
| 4.S1 to 4.S4 | impl | pointers to `spec 1`; `check.py` builds names/dependencies (`dependencies`, `claimed_laws`) | implemented | none |
| 4.S5 Everything is a type | impl | none: the subtype `{ n : Int \| n == 4 }` for `4` is not what `elaborate.py` does (`Lit`) | decided / proposed | "`4` is `{ n : Int \| n == 4 }`" is a thesis, not behavior |
| 4.S6 Three states | impl | `check.py` and `elaborate.py` have declared and defined; no certificate state in the new specimens | decided D-2026-10-12-y for "certified"; the first two states implemented | "certified ... passed `test`": no `test` command |
| 4.S7 The body decides | impl | `check.py` R4, R5, R6; `fits`/`verdict_type` | implemented | none |
| 4.S8 Declared types carry laws | impl | P: `r2_definition.accept`, `r6_predicate_body.accept`; T: `test_theory_conjunction_keeps_declared_record`, `test_single_theory_law_keeps_declared_record` | implemented | none |
| 4.S9 Concrete types, theories | decided + impl | `violatesR3`, `violatesR4`; T: `test_R3_claimed_laws_read_fields_through_bound_models` | implemented | "Today the checker tells the two apart by their form" (accurate: R3/R4) |
| 4.S10 A body computes | impl | none (a rule for the author) | decided | none |
| 4.S11 Order of work | impl | `check()` does not order anything; it runs each predicate on every name; imports are not loaded (`check.py` line 279 says so) | decided/proposed | "reads the whole program, imports included, before it checks any definition", the four steps; "compute the theories" has no specimen |
| 4.S12 The cycle is the theory | impl | `claimed_laws`, `head`; the SCC half of 4.R2 is an xfail | decided D-2026-10-12-z; not implemented | "This closes O7" fine |
| 4.S13 Why the cycle | impl | none | decided | none |
| 4.S14 A head, and the law no type claims | impl | `violatesS14` (a `report` kind, "unclaimed"); `r2_unclaimed_laws.reject` xfails | implemented as a report; as a rejection decided | "4.R2 applies to it": the reject program is an xfail |
| 4.S15 Dependence | impl | `dependencies`, `names` | implemented | none |
| 4.S16 Semantic criterion | proposed | none | proposed | none |
| 4.R1 | impl | P: `r1_declaration.accept/.reject` pass; `violatesR1`; program.lth | implemented | none |
| 4.R2 | impl | P: `r2_definition.accept` passes, `r2_definition.reject` xfail (`violatesR2` is the existence half only, `violatesR2Exists`) | decided D-2026-10-13-ae (the half by SCC is deliberately deferred); not `[implemented]`, since the reject program does not get its verdict | "every name that occurs in type position ... is defined, unless it belongs to `n`'s own theory" (the checker tests existence only); "`luthier run --set`" (no such option) |
| 4.R3 | impl + decided | P: `r3_connected.accept`, `r3_dangling_label.reject`, `r3_true_predicate.reject`, `r4_data_nonrecursive.reject` (rule 4.R3), `r4_recursive_data.accept`; T: `test_R3_*` | implemented | "`| true` records of the first libraries disappear" fine |
| 4.R4 | decided | P: `r4_product_inline.accept`, `r4_product_named.reject` pass; `violatesR4` | implemented (both programs get their verdict; the decision D-o stays cited) | "a sum written `< ... >`" (retired syntax) |
| 4.R5 | impl | P: `r5_extern_value.accept`, `r5_extern_type.reject`, `r5_extern_provisional.accept`, `r5_extern_over_declared.reject`; `violatesR5`; T: `test_extern_reads_every_type_name_and_accepts_aliases`; `run.py` Float64/Int/Fin checks at the crossing | implemented for the declaration side; the obligation side is partial | "`luthier run --checked` tests every value an extern gives against the Bool laws of its type" (no `--checked`; the bridge checks `Float64`, `Int`, `Fin n` bounds, shapes only); "`pairI : Vec (Fin nodes)` owes that every entry is below `nodes`": checked only for a declared `Fin` codomain; "recorded in the certificate under `provisional`" (no certificates); "In the language designed the checker does not resolve the target" now true |
| 4.R6 | impl + decided | P: `r6_predicate_body.accept`, `r6_body_type.reject`; `violatesR6` with `Law`, `Failures` | implemented | "The form with `Failures E` is designed ... the checker accepts the other three today": `verdict_type` accepts `Failures` now |
| 4.R7 | impl | P: `r7_alias.accept`, `r7_alias_defined.reject`; `violatesR7` | implemented | the `gen FullCoords` / `VecOf` text (no `gen`) |
| 4.R8 | impl | P: `r8_equality_parameter.accept`, `r8_equality_function.reject`; `violatesR8`; kernel structural `==` (`test_prim_structural`, `test_equality_*`) | implemented | "`algebra.lut` already does so" (now `algebra.lth`); "How a type names its equality (O2) is O2" is circular, not false |
| 4.R9 | impl | P: `r9_variance.accept/.reject`; `violatesR9`; program.lth `RefinePair`; T: `test_R9_*` (7 tests) | implemented | none |
| 4.R10 | decided | `violatesR10` returns False; no `check -v` "consistent, not characterized" report | decided D-2026-10-05-a | "`check -v` makes the difference visible": it does not (reports are unclaimed, provisional, loose) |
| 4.R11 | decided | `violatesR11` False; `branchContext` and T: `test_Typing_laws_on_constructed_terms`; no accept/reject program | decided D-2026-10-06-aa; the typing law exists | "Not implemented" in the text; no program |
| 4.R12 | impl | P: `r12_block.accept`, `r12_defined_twice.reject` (message "defined twice"), `r12_rebind_defined.reject`, `r12_pattern_rebind.*`, `r12_defaults.accept`; T: `test_block_rules`, `test_rebind_binds_its_pattern_names` | implemented | "the session (O8)"; "the elaborated call ... carries the value the body sees" has a T (`test_Arguments`) |
| 4.R13 | impl | P: `r13_operator_by_type.accept`, `r13_two_models.reject`; `violatesR13`; T: `test_operator_rivals_report_each_function_and_absent_declarations` | implemented | `examples/z7ring.lut` is not in the tree |
| 4.S17 No loose functions | decided, "not implemented" | `looseFunction` is a `report` kind ("loose") | decided D-2026-10-07-e, reported only; the two programs it names do not exist | "`check -v` is to report loose functions first": done; `s17_*` files "neither exists" still true |
| 4.S18 R2 and R3 programs beyond the pair | impl | P: all named programs exist; `r2_unclaimed_laws.reject` is an xfail | implemented for all but `r2_unclaimed_laws.reject` | its "is rejected" claim for `r2_unclaimed_laws` |
| 4.S19 `luthier check -v` | impl | `report()` gives unclaimed, provisional, loose; `cli.py` prints them; no observers-versus-constructors table, no axioms listing | decided D-2026-10-05-b; partly implemented | "for each concrete type with laws, the table of observers against constructors": not built (4.R3 "reported besides" too); "also the axioms, `spec 6`" |
| 4.S20 Consistent, not characterized | decided | none | decided D-2026-10-05-b | none ("Not implemented" is true) |
| 4.S21 R1 to R13 as laws of `WellFormed` | proposed | L: program.lth `WellFormed`, `ReportsViolations`, `ReportsNoFalseFailure`; check.py is its specimen (`test_check.py`) | implemented for R1 to R13 (R10 and R11 as non-predicates); the 2.R1, 2.R6 and 6.R1 predicates are beyond the list | "to be written in `lib/program.lut` (not yet present)": it is `program.lth`; "Until it exists the checker in `src/luthier/checker.py` is the specimen": `check.py` |
| 4.S22 Example | impl | none: the program is not in `tests/spec/` | decided/illustration; make it a program or drop the status | "`test csv with 200`" (the `test` act is gone); `Codec` ... `extern "python:luthier.tables.parse"` fine |
| 4.S23 Implicit from expected type | decided | `elaborate.py` lines 280 to 292; translation.lth | implemented | none |
| 4.S24 Checker does not open an extern's file | decided | `check.py` has no host import; `test_unused_extern_is_not_resolved` | implemented | "Today it imports the host module" |

## Sentences to change, by chapter

Chapter 2.
- 2.S2: the list of reserved words; "`and`, `or` and `mod` are ordinary names" (against 2.S8, 2.S21);
  "the parser still reads it today" (`gen`); fold the rest into 2.S21 and flip to decided.
- 2.S5: the production block (`directive`, `primitive`/`axiom` bodies, binder without `{ }`);
  mark it superseded by `luthierSyntax` as 2.S9 does.
- 2.S6: "In `v0.1-final` the directives other than `test` were as below" and its productions.
- 2.S8: the first table (one-line) is subsumed by the D-p table.
- 2.S9: the second EBNF block (`\`, `< >`, `let`, `forget`, `extern`, `sep ... line break`).
- 2.S12: the `let` row (retired); the `m.f` row has no test.
- 2.S15: "`let p = e in body` is `match e { p -> body }`" stated as implemented.
- 2.R6 and 4.R12: "reported in a session"; 2.S18 whole (no `session` command).
- 2.S19: "The parser today reads `test name [...]` and still reads `gen`".
- 2.S20: "draft 2 written 2026-10-13".
- 2.S21: "The parser reads the older forms today".

Chapter 3.
- 3 §4 header: "3.S14 to 3.S18 have none yet, and their mark stays `[implemented]` for the interpreter".
- 3.S2 and 3.S3: bodies `primitive`/`axiom`, directives `test`, `gen`, `cite`, and the `profile`
  `[proposed]` sentence.
- 3.R1 first paragraph and 3.R2: "names are binders", "`Int * Bool` are one structure", "a value of
  such a sum is accepted where a `Bool` is expected" (D-x in the same item says the opposite).
- 3.S12: "not taken by the checker today"; "the interpreter does not have yet".
- 3.S14, 3.S15: the program text uses `\k r`.
- 3.S17, 3.S18: the programs named are checked, not run; point to `tests/eval/` and `tests/run/`.
- 3.S29: "They are not in `core.lut` yet; ... `syntax.py`"; the `Term` and `Act` table rows
  against the paragraph above.
- 3.S32, 3.S33, 3.S38: "Neither is in the interpreter", "The file is not written", "Not written".
- 3.S36: `examples/kernel_finite.lut`, the `KernelLaws A B` description and "luthier test".
- 3.S40: "Today the checker resolves every extern when it checks the file".

Chapter 4.
- 4.R2: "unless it belongs to `n`'s own theory" (existence only today) and `luthier run --set`.
- 4.R4: "a sum written `< ... >`".
- 4.R5: `luthier run --checked`; the array-entry obligation example; "recorded in the certificate".
- 4.R6: "the checker accepts the other three today".
- 4.R7: the `gen FullCoords` example.
- 4.R8: `algebra.lut` (now `algebra.lth`).
- 4.R10: "`check -v` makes the difference visible".
- 4.R13: `examples/z7ring.lut`.
- 4.S6: "passed `test`" (no `test` command).
- 4.S11: "reads the whole program, imports included"; the four steps (not what `check()` does).
- 4.S19: the observers-versus-constructors table and the axioms.
- 4.S21: `lib/program.lut`, `src/luthier/checker.py`.
- 4.S22: `test csv with 200`.
- 4.S24: "Today it imports the host module".

## Items whose programs are missing

Rules marked `[implemented]` that lack an accept or a reject program that gets its verdict:
- 4.R2: reject program is an xfail (`r2_definition.reject`; `r2_unclaimed_laws.reject` too).
  Not eligible for `[implemented]`.
- 3.R1: reject program `k_label_order.reject` gets its verdict, but under rule 4.R9, and no
  program tests the first paragraph either way (a record against a bare product).
- 3.R2: no reject program (the listed one is about record order); the accept program is accepted
  by a checker that rejects nothing about types.
- 3.R3: accept only (`r4_recursive_data.accept`); no program shows a reject for a non-free
  constructor.
- 4.R10 and 4.R11 carry no Files line; 4.R11 has the typing law but no accept or reject program.
- 4.S17: both programs it names (`s17_loose_function.reject`, `s17_defined_function.accept`) do not
  exist.
- 4.S22: its example is not a program of `tests/spec/`.
- 2.S18, 3.S26: nothing runs them (no `session`; no test of lambda against array).
- Statements with no test: 3.S10 "none repeated and none missing", 4.S5, 4.S11, 4.S12 (SCC),
  4.S19's table, 4.S20, 3.S35.

## Flips proposed at v0.2

Implemented as is (or with the false sentences above corrected): 2.S1, 2.S3, 2.S4, 2.S5, 2.S7,
2.R1 to 2.R6 (2.R6 minus the session clause), 2.S8 to 2.S11, 2.S12 (but see rows), 2.S13, 2.S14,
2.S16, 2.S17, 3.S1, 3.S4 to 3.S9, 3.S11, 3.S13 to 3.S25, 3.S27, 3.S28, 3.S29 to 3.S34, 3.S36 to
3.S38, 3.S40, 4.R1, 4.R3 to 4.R9, 4.R12, 4.R13, 4.S21, 4.S23, 4.S24.
Decided, not implemented: 2.S2, 2.S6, 2.S18, 2.S19, 2.S20 (partly), 2.S21, 3.S2, 3.S3, 3.R2 (or
proposed), 3.S26, 3.S35, 3.S39, 4.R2, 4.R10, 4.R11, 4.S5, 4.S6 (the third state), 4.S11, 4.S12,
4.S14 (as a rejection), 4.S17, 4.S19 (the table), 4.S20.
Stays proposed: 4.S16 and the `quote` brace clause of 2.S4 unless its test is found.
