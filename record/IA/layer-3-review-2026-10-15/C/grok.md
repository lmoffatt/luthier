**generators.lth**

1. None found that are false of the intended models or unsatisfiable together.  
2. `ProportionalToWeight` only constrains the interval of positive weight; a pick that always returns the last positive-weight value (as the reference `pick` does on rounding overflow) still satisfies every law.  
3. `Mode` is defined in `test.lth`; no constructor of a `data` here lacks a role law. `Coverage` roles are stated in `laws.lth`.  
4. N/A (theory file).  
5. Matches 7.S1–7.S8, 7.R1, 7.R3–7.R4 and the cited decisions on generators, budgets and bindings.  
6. None; quantifiers are over the relevant subtypes (`UnitInterval`, `PositiveInterval`, etc.).  
7. Move the statistical laws `UniformAtLevel`/`IndependentAtLevel` (and their `Level` parameter) out of the Boolean conjunction of `Random` so that the demand’s level is not forced into every model of `Random`.  
8. None; every cutoff/budget is a field of `Budgets` or of `Level`.  
9. Missing generators for any law quantified over models of a theory that is not finite (spec 7.R4); the file itself supplies only the `Census` generator.

**generators_model.lut**

1. None.  
2. `GramGivesPsd` only checks retained rank of `-a`; a matrix that is positive-semidefinite only after a non-zero shift still passes.  
3. No `data`.  
4. `OrthogonalGivesOrthogonal` uses a free `tol : Tolerance`; the model supplies none, so the law is not closed.  
5. Matches the families of 7.S5 and the reference definitions of generators.lth.  
6. None.  
7. Supply a concrete tolerance (or make it a parameter of the model) for `OrthogonalGivesOrthogonal`.  
8. `0.2`, `0.25`, `1.0`, `1000.0` appear as constants in the host-generator wrappers; by D-2026-10-14-c they should be parameters supplied by the demand.  
9. The sampled statistical law `UniformSampleIsUniform` already names its generator; no further missing generator for a listed-cases law.

**test.lth**

1. None.  
2. `CoverageIsTheWeakest` accepts either `specCoverage` or `wholeCoverage` under `ExhaustiveMode`; a tester that always returns the weaker of the two still satisfies the law.  
3. `Mode` constructors (`ExhaustiveMode`, `SampledMode`) have no role law (L2.7). `Grade` constructors likewise lack individual role laws beyond the aggregate `GradesAsTerms`.  
4. N/A.  
5. Matches 7.S8–7.S10, 7.S12–7.S13, 7.S20 and D-2026-10-14-b.  
6. None.  
7. Add role laws for the constructors of `Mode` and `Grade`.  
8. The numeric defaults inside `defaultBudgets` are constants; by D-2026-10-14-c / P11 they should be demand parameters (the file already treats the whole record as an argument, but the literals themselves violate the cutoff rule).  
9. No sampled law over models of a theory is stated here, so none missing.

**test_model.lut**

1. None.  
2. None (the model simply re-exports the reference `grade`/`gradeRank`).  
3. No `data`.  
4. None.  
5. Matches the grading of test.lth.  
6. None.  
7. Nothing urgent.  
8. None.  
9. None.

**laws.lth**

1. None.  
2. `CombineAbsorbs` only forces the three listed absorption rules; any other combination of `Supported`/`Cites`/`Assumes` is free, so a model that maps every pair to `Unsettled` still satisfies every law.  
3. Constructors of `Law`, `Coverage`, `Evidence` and `Verdict` have role laws only via the aggregate `Settling` / `Covering` predicates; individual constructors such as `Then`, `Side`, `Assumed` receive no dedicated role statement beyond the list in `Settling`.  
4. N/A.  
5. Matches 5.S1–5.S5, D-2026-10-11-l, D-2026-10-13-l and D-2026-10-14-b.  
6. The relation templates (`isSymmetric`, `isTransitive`, \ldots) are written with implications; the comment correctly notes that a theory should quantify over the related pairs instead.  
7. Replace the implication forms of the relation templates by quantification over the subtype of related pairs (as already done for equality in kernel_laws).  
8. None.  
9. Any law that quantifies over models of a theory (e.g. a `Settling` instance itself) still lacks a census/generator; the file supplies none.

**Against the specification (cross-file)**

- generators.lth §8 (functors) is still `todo`, matching 7.S3’s open status.  
- test.lth’s `defaultBudgets` literals and generators_model.lut’s hard-coded masses violate D-2026-10-14-c / P11.  
- laws.lth’s implication-style relation templates contradict the guidance of 7.S12 and the comment already present in the file.

**not sure**

- Whether the host externs in generators_model.lut actually satisfy the statistical laws at the stated levels (requires running the Python side).  
- Exact interaction of `wholeCoverage` with an infinite type under `ExhaustiveMode` (tester.py behaviour is mentioned but not formalised).