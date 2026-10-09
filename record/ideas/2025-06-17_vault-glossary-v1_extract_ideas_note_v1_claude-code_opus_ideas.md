---
note: vault_glossary_v1.md
note_dir: HoTTification-2025-06
note_sha256: 12a518f2fed86c3fd5b8a5e1dcd1ce68a912e7e744cee6f5745c64044f83b755
title: "vault_glossary_v1"
author: model (ChatGPT)
created: 2025-06-17T06:23:58
ideas: 21
quotes_found: 21/21
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### hottification-as-transforming-models-into-hott-structure
- **What**: HoTTification is defined as turning a scientific model, algorithm or modeling language into a formal structure governed by Homotopy Type Theory.
- **Quote**: "HoTTification is the process of transforming a scientific model, algorithm, or modeling language into a formal structure governed by Homotopy Type Theory (HoTT)." (line 8)

### types-as-entities
- **What**: Among the HoTT ingredients, types stand for the entities of the model.
- **Quote**: "Types as entities." (line 10)

### identity-paths-as-structural-equivalences
- **What**: Identity paths are read as structural equivalences between entities.
- **Quote**: "Identity paths as structural equivalences." (line 11)

### higher-paths-as-equivalence-transformations
- **What**: Higher paths stand for transformations between equivalences.
- **Quote**: "Higher paths as equivalence transformations." (line 12)

### dependent-types-enforce-semantic-safety
- **What**: Dependent types are what enforce semantic safety in the structure.
- **Quote**: "Dependent types enforcing semantic safety." (line 13)

### compile-time-structural-validation
- **What**: Models are validated structurally at compile time.
- **Quote**: "Compile-time structural validation of models." (line 14)

### semantic-safety-enforced-by-the-language
- **What**: Semantic safety is model correctness enforced by structural rules in the modeling language itself, so only structurally valid models can be constructed.
- **Quote**: "Semantic safety refers to model correctness enforced by structural rules in the modeling language itself, ensuring that only structurally valid models can be constructed." (line 27)

### invalid-models-eliminated-at-type-level
- **What**: Violations of model consistency are removed at the type level, before execution or inference.
- **Quote**: "Violations of model consistency are eliminated at the type level, prior to execution or inference." (line 27)

### runtime-vs-semantic-safety
- **What**: Runtime safety keeps a model running numerically; semantic safety keeps a model structurally meaningful, valid and well-posed before it runs; the contrast is framed as preventing crashes versus preventing invalid models from existing.
- **Quote**: "Runtime safety: prevents crashes or numeric failures." (line 30)
- **Also at**: lines 31, 113, 114

### semantic-safety-prevents-invalid-models-from-existing
- **What**: Semantic safety is cast as preventing invalid scientific models from existing at all.
- **Quote**: "Semantic safety: prevents invalid scientific models from existing." (line 31)

### bayesianization-of-the-scientific-pipeline
- **What**: Mapping scientific knowledge production into explicit Bayesian structures, section of a paper to component of inference.
- **Quote**: "The process of formally mapping scientific knowledge production into explicit Bayesian structures:" (line 40)

### paper-sections-as-bayesian-components
- **What**: Introduction maps to prior, methods to likelihood, results to observations, discussion to posterior.
- **Quote**: "Introduction → Prior." (line 42)
- **Also at**: lines 43, 44, 45

### science-made-auditable-and-probabilistic
- **What**: The aim of the Bayesian mapping is to make scientific reasoning auditable, quantifiable and explicitly probabilistic at every step.
- **Quote**: "The goal is to make scientific reasoning auditable, quantifiable, and explicitly probabilistic at every step." (line 47)

### macroirization
- **What**: Feeding structurally defined kinetic models into the MacroIR likelihood recursion engine, which computes full interval-averaged likelihoods for macroscopic current data.
- **Quote**: "The act of feeding structurally defined kinetic models into the MacroIR likelihood recursion engine, which computes full interval-averaged likelihoods for macroscopic current data." (line 57)

### macroir-consumes-markov-models
- **What**: MacroIR consumes Markov models produced by the ConformationalModel DSL or by HoTTified model generators.
- **Quote**: "MacroIR consumes Markov models produced by ConformationalModel DSL or HoTTified model generators." (line 60)

### conformational-algebra
- **What**: A compositional system for building kinetic models from conformational state components.
- **Quote**: "A compositional system for building kinetic models from conformational state components:" (line 70)

### external-product-of-conformational-dof
- **What**: Models are built as an external product of conformational degrees of freedom, with energetic coupling rules.
- **Quote**: "External product of conformational degrees of freedom." (line 72)
- **Also at**: line 73

### symmetry-reduction-and-state-aggregation
- **What**: Symmetry reduction and aggregation of states by equivalent coupling configurations as mechanisms of the algebra.
- **Quote**: "State aggregation based on equivalent coupling configurations." (line 75)
- **Also at**: line 74

### fim-self-consistency-diagnostic
- **What**: Validating a likelihood by comparing the Fisher Information Matrix from score covariance against the one from the Hessian; agreement validates the implementation without full inference.
- **Quote**: "Agreement between these two estimates validates the correctness of likelihood implementation without requiring full inference." (line 90)

### model-compiler
- **What**: A system translating high-level mechanistic model specifications into executable, inferable structures such as state spaces, likelihood functions and samplers.
- **Quote**: "A system that translates high-level mechanistic model specifications into executable, inferable structures (e.g. state spaces, likelihood functions, samplers)." (line 100)

### dsls-as-model-compilers
- **What**: The DSLs being built are themselves model compilers, with pipelines from DSL to Markov models to engine, and from HoTT DSL to validated model spaces to inference.
- **Quote**: "The DSLs you are building serve as model compilers." (line 102)
- **Also at**: lines 105, 106
