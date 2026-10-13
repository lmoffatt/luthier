# Checker audit, 2026-10-13
Sources: `program.lth` changes 519bdf3 and a73fa4f; checkout 38922767cc257f666b952d7d3b4303b17735521f. Derivation: Codex user brief 2026-10-13 v2, hand-written domains, no random parameters/seed; only check.py, test_check.py, test_spec.py and this report edited; no commit. Current program.lth SHA256: 1e3cca3e90400715f24d6957709f6a5d6b3068c90eb4dc7f46b87cd93e6714f7.

| tests/spec verdict | Cases / reason |
|---|---|
| Pass (38) | `k_bool_is_sum.accept.lut`, `k_dependent_product.accept.lut`, `k_empty_unit.accept.lut`, `k_label_order.reject.lut`, `k_named_product.accept.lut`, `k_sum.accept.lut`, `k_union.accept.lut`, `n1_numbers.accept.lut`, `n5_arrays.accept.lut`, `r12_block.accept.lut`, `r12_defaults.accept.lut`, `r12_defined_twice.reject.lut`, `r12_named_unknown.reject.lut`, `r12_rebind_defined.reject.lut`, `r12_toplevel_arrow.reject.lut`, `r12_unused_rebinding.reject.lut`, `r13_operator_by_type.accept.lut`, `r13_two_models.reject.lut`, `r1_declaration.accept.lut`, `r1_declaration.reject.lut`, `r3_connected.accept.lut`, `r3_dangling_label.reject.lut`, `r3_true_predicate.reject.lut`, `r4_data_nonrecursive.reject.lut`, `r4_product_inline.accept.lut`, `r4_product_named.reject.lut`, `r5_extern_over_declared.reject.lut`, `r5_extern_provisional.accept.lut`, `r5_extern_type.reject.lut`, `r5_extern_value.accept.lut`, `r6_body_type.reject.lut`, `r6_predicate_body.accept.lut`, `r7_alias.accept.lut`, `r7_alias_defined.reject.lut`, `r8_equality_function.reject.lut`, `r8_equality_parameter.accept.lut`, `r9_variance.accept.lut`, `r9_variance.reject.lut` |
| Strict xfail | `n2_r_gone.reject.lut`: 11.R1 remains outside program.lth v0.2, pending Luciano. |
| Strict xfail | `n3_primitive_outside_core.reject.lut`: 11.R2 remains outside program.lth v0.2, pending Luciano. |
| Strict xfail | `n4_axiom_outside_lib.reject.lut`: 11.R3 remains outside program.lth v0.2, pending Luciano. |
| Strict xfail | `r2_definition.reject.lut`: 4.R2 type-position and SCC half deliberately deferred. |
| Strict xfail | `k_recursor.accept.lut`: elaborate.py: Recursor conjunction infers Hole and add mismatches (4.R6/4.R9); also theory lawNames loses bound field reads (4.R3). |
| Strict xfail | `r2_definition.accept.lut`: elaborate.py: Codec definition overwrites its record type with RoundTrip type (4.R6); also theory lawNames loses bound field reads (4.R3). |
| Strict xfail | `r4_recursive_data.accept.lut`: elaborate.py: TreeFold conjunction infers Hole (4.R6); also theory lawNames loses bound field reads (4.R3). |
| Fail | `cite_not_reference.reject.lut`: only 4.R2 main (undeclared cite), no 6.R1: corpus uses a proposed world-threaded block call; predicate requires a top-level datum `cite n r`. |
| Fail | `cite_proved.accept.lut`: 4.R2 main, undeclared cite; no import/declaration for this library interface. |
| Fail | `r2_unclaimed_laws.reject.lut`: accepted by the literal existence half of 4.R2; type-position/SCC half is deferred. Its former unknown-projection rejection disappeared correctly. |

Checks: focused: 3 failed, 87 passed, 7 xfailed; full: 4 failed, 397 passed, 7 xfailed (55.42s). `test_check.py` alone: 41 passed; `test_spec.py` alone: 3 failed, 46 passed, 7 xfailed. System `/usr/bin/python3` has no pytest; commands ran with `PATH=/tmp/luthier-term-model-tests/bin:$PATH PYTHONPATH=src`. Logs: `/tmp/codex-2-focused.txt`, `/tmp/codex-2-full.txt`. Other-file failure: `tests/test_render_grammar.py::test_repository_is_current`: `docs/spec/02-grammar.md` generated grammar stale during concurrent `grammar.lth` edits; reported only, not fixed. The other agent subsequently changed the generated document.

| Theory/library file | Failures by rule (introduced names) |
|---|---|
| `checks.lth` | 4.R3: Check; 4.R6: Check |
| `ebnf.lth` | 4.R3: Derives, Recognizer; 4.R6: Derives, Recognizer; 4.R9: RefUnion, SeqSplits, AltUnion, RepRounds, AcceptsWhatDerives |
| `generators.lth` | 4.R3: Random, Support, Metric, Exhaustive, Sized, Filter, fromCensus, Resolution, Budgets, RuleCases |
| `grammar.lth` | 4.R3: Surface, Grammar; 4.R6: Grammar; 4.R9: LexesWhatDerives, LexFailsWhatDerivesNot, OpenForms, DefinitionTree, DefaultTree, LiteralTree, SubtypeTree, BlockOrRecordValue, ListTree, PatternTree, ScrutineeTree, NamedArgTree, NegationTree |
| `kernel_laws.lth` | 4.R3: Object, Structural, Terminal, Initial, BooleanAlgebra, TheBooleans, Monoid, FreeMonoid, Lists, OrderedSemiring, Exponential, Product, Coproduct, NamedProduct, NamedCoproduct; 4.R2: SelectByName |
| `laws.lth` | 4.R3: CostScale, Coverage, Verdict, Settling; 4.R6: CostScale, Settling |
| `library.lth` | 4.R3: Loader; 4.R6: Loader |
| `program.lth` | 4.R3: WellFormed, Typing; 4.R2: TypeOfIntroductions |
| `term.lth` | 4.R3: Alpha, Substitution, CanonicalForm, Reduction, Evaluation |
| `test.lth` | 4.R3: MetricName, Mode, Tester, Grading; 4.R6: Tester, Grading |
| `translation.lth` | 4.R3: Elaboration; 4.R6: Elaboration |
| `world.lth` | 4.R3: World, Persistence, Externs, Console; 4.R6: World, Persistence, Externs, Console |
| `kernel_models.lut` | 4.R2: recordXY, sumAB |
| `term_model.lut` | 4.R9: canonicalTerm; 4.R3: HeadStep, PatternStep, PatternListStep, ArmStep |

`luthier check src/luthier/lib/*.lth src/luthier/lib/*.lut`: exit 1, 92 failures; every unlisted file passed. Used `/tmp/luthier-grammar-render-venv/bin/luthier`, `PYTHONPATH=src`; exact diagnostics `/tmp/codex-2-library.txt`. Other files left untouched. Final run includes concurrent grammar.lth edits (SHA256 d919a4f8faf747ca179e4587256a568ba801ba76cb81b7d27fd8e6118a306098).

Law audit (observed domains, not universal certification): all constructed Typing law domains in test_check.py, new SameSeparates cases, and implemented ReportsViolations/ReportsNoFalseFailure/ReportsWhen/ReportsOnlyWhen domains pass. The four new violation predicates are mirrored literally; 4.R13 compares absent declaredSurface values as equal, as the source does. Clean directions are tested too; the theory only requires violation reporting for the four new predicates.
Remaining unmet expectations by rule/case: 4.R2 SCC/type position: r2_definition.reject and r2_unclaimed_laws.reject (not a law of v0.2 program.lth); 11.R1/11.R2/11.R3: n2/n3/n4 (outside program.lth pending Luciano); 6.R1: cite_not_reference corpus uses a different shape, while the actual datum domain passes; 4.R2 cite_proved lacks cite in its interface. 4.R3: r2_definition.accept, k_recursor.accept, r4_recursive_data.accept: remove now erases bound dotted projections from bOf/lawNames, so untouchedFields cannot see reads of parse/render, fold/eq. This is a conflict within program.lth, mirrored rather than repaired here. 4.R6 in those three cases and 4.R9 add in k_recursor are elaboration limitations (record type overwritten / conjunction type Hole / incomplete lambda domain); elaborate.py was left untouched. These are failing corpus expectations; there is no observed counterexample to the literal checker reporting laws in the tested domains. ElaborationError still suppresses type-dependent predicates when no elaboration exists, so these domains remain uncertified.
Independent decisions: mirror the new predicates literally; report inline positional record return mismatch as 4.R9 (requested); remove passing strict xfails and retain only authorized exceptions, leaving three incompatible corpus expectations visibly failing. No changes to evidence, theory files, or the other agent's work.
