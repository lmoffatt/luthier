# Prior Art Search for Luthier (Beyond `related-work.md`)

## Executive Answer to the Brief

**Is there a project essentially the same as Luthier, already published or about to be?**

**No.** Across 2024 to 2026 preprints on arXiv (`cs.PL`, `cs.SE`, `cs.MS`, `cs.LO`), major programming languages and software engineering venues (PLDI, POPL, OOPSLA, ICFP, ECOOP, CAV, ICSE, FSE), scientific computing venues (SC and the Correctness HPC workshop, JOSS, US-RSE 2025 and 2026, SciPy 2025 and 2026), funding databases (NSF Award Search, specifically the 2024 to 2026 *Correctness for Scientific Computing Systems* or CS2 program NSF 24-571, and EU CORDIS / ERC grants), and GitHub, **no published or announced project combines all eight of Luthier's defining ingredients into a single language or system.**

However, the search uncovered **several recent projects and papers (2024 to 2026) not covered in `related-work.md` that are significantly closer to specific parts of Luthier than the citations in `related-work.md`**. In particular:

1. **Numerical Fuzz ($\Lambda_{\text{num}}$, PLDI 2024), Bean (PLDI 2025), and eggshel (PLDI 2026)** by Kellison, Zielinski, Bindel, and Hsu directly close the gap that `related-work.md` (Section 11) claimed existed in Reed and Pierce's Fuzz: they extend linear sensitivity type systems with a graded monad for additive floating-point rounding error and a compositional category (`Shel`) for backward error synthesis.
2. **The Evidential Tool Bus (ETB)** by Cruanes, Hamon, Owre, and Shankar (noted briefly in `novelty-critique.md`) and **Foundational Proof Certificates for Property-Based Testing** by Miller and Momigliano (TPLP 2024) together with **Programmable Property-Based Testing** by Keles et al. (ICFP 2026) directly anticipate separating laws from certifiers and orchestrating heterogeneous, hash-keyed verification and testing evidence.
3. **Ten newly funded NSF CS2 awards (2025 to 2026, Solicitation 24-571) and ERC Starting Grant HORNET (2025 to 2029)** show that the formal methods and scientific computing communities are actively converging on Luthier's problem space right now, including LLM-assisted extraction of executable specifications validated by concolic property testing for large scientific codebases (NSF #2546694), formal floating-point assurance cases across C/C++, Fortran, and Julia via LLVM (NSF #2446214 and OOPSLA 2026), and equality-saturation pareto optimization under verified floating-point bounds (NSF #2546786).
4. **MutDafny (arXiv 2025) and IronSpec (OSDI 2024)** bring systematic mutation testing of formal specifications (Luthier's negative controls) into deductive verification languages, while **DualVeri (arXiv 2026)** combines parameterized property templates in Lean 4 with property-based testing in Python/Spark.

None of these projects is a reason to stop Luthier. Every one of them is a reason to sharpen what Luthier claims as new and to cite these works directly so reviewers who wrote them see their contributions accurately represented.

---

## Methodology and Verification Key

Every candidate below was investigated on 2026-10-26. All links listed under **Fetched links** were fetched directly over HTTPS during this search (`arxiv.org/abs/...`, `api.crossref.org/works/...`, `github.com/...`, and `nsf.gov/awardsearch/...`), returning HTTP 200 OK. Items where only grant abstracts or conference programs are public and underlying code or unpublished manuscripts could not be inspected are explicitly marked `[unverified implementation details; public grant/program abstract only]`.

The eight ingredients from `BRIEF.md` are abbreviated in the tables as follows:

1. **Theories & Models:** Types with explicit mathematical laws (`Theory`) and implementations (`Model`) checked against them.
2. **Graded Persistent Evidence:** Certification of implementations against laws with graded, persistent, composable evidence (`Proved`, `Exhaustive`, `Cases`, `Sampled` with confidence bounds $(\hat\varepsilon, \delta)$).
3. **Controls & Vacuity:** Negative controls (wrong models or tightened bounds that each conjunct of a law must refute) and vacuity detection/rejection.
4. **Content-Hash Certificates:** Persistent certificates keyed by cryptographic content hashes of the transitive dependency cone, host code, and generator bindings.
5. **Within-Bound FP Laws:** Floating-point or numerical laws stated within analytical or sensitivity/defect bounds (such as Higham's $\gamma_n$ or affine bound transformers $(L, \eta, D, r)$).
6. **Demand-Driven Choice:** Demand-driven selection among multiple certified implementations (specimens) trading accuracy, evidence, and resources along certified identities.
7. **Cross-Language Provenance:** Typed provenance or derivation of values preserved across foreign-language boundaries (Python, C, Fortran, Julia).
8. **Scientific Computing Focus:** Explicitly designed for or applied to scientific and numerical computing.

---

## Overview Table of Candidates Across the Eight Ingredients

| # | Candidate System / Project | 1. Theories & Models | 2. Graded Persistent Evidence | 3. Controls & Vacuity | 4. Content-Hash Certificates | 5. Within-Bound FP Laws | 6. Demand-Driven Choice | 7. Cross-Language Provenance | 8. Scientific Computing | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Evidential Tool Bus (ETB)** (SRI, 2013) | Partial (claims) | High (multi-tool claims) | None | High (SHA1 file/rule keys) | None | Partial (workflow routing) | Partial (tool wrappers) | Low (avionics/safety) | **Overlapping** |
| 2 | **Numerical Fuzz, Bean & eggshel** (Cornell, PLDI 24/25/26) | Partial (types) | Deductive only | None | None | **Very High** ($(L,\eta)$ & backward) | None | None | **High** (numerical LA) | **Overlapping** |
| 3 | **GATlab.jl & Catlab.jl** (AlgebraicJulia, 2024-2026) | **Very High** (GATs) | None (unit tests) | None | None | None | Partial (multiple models) | Low (Julia-centric) | **High** (PDEs, dynamics) | **Overlapping** |
| 4 | **SciLean & PhysLean** (Lean 4, 2024-2026) | **Very High** (Lean 4) | Deductive + `sorry` | None | Lean `.olean` hashes | Partial (symbolic approx) | Partial (tactic rewrites) | Low (C codegen) | **High** (physics, PDEs) | **Overlapping** |
| 5 | **Drasil & MMT Biform Theories** (McMaster/FAU, 2023-2026) | **High** (theories) | Deductive / gen tests | None | MMT URIs (not cone hashes) | Partial (interval bounds) | Partial (design choices) | High (traceable codegen) | **High** (scientific SCS) | **Overlapping** |
| 6 | **LAProof & VCFloat2** (Princeton/Cornell, 2023-2024) | **High** (Coq) | Deductive only | None | Coq `.vo` checks | **Very High** (Higham $\gamma_n$) | None | Partial (VST for C) | **High** (BLAS/sparse LA) | **Overlapping** |
| 7 | **Probabilistic FP (OOPSLA 26) & NSF CS2 #2446214** (Jeannin et al.) | Partial (Coq/LLVM) | Probabilistic + proof | None | Assurance cases | **Very High** (probabilistic FP) | None | **High** (C/Fortran/Julia LLVM) | **High** (plasma/FEM) | **Overlapping** |
| 8 | **FPCs for PBT (2024) & Programmable PBT (ICFP 26)** | Partial (props) | **High** (proof/exhaustive/random) | Precondition tracking | None | None | Custom runners | None | Low (general PL) | **Overlapping** |
| 9 | **DualVeri (2026), Rules to Tools (2026) & FVSpec (2026)** | **High** (Lean + PBT) | Proof + ephemeral PBT | Template guardrails | None | Tolerance checks in R2T | Agentic repair loop | Python/Spark + Lean | Medium to High (SciCode/DISC) | **Overlapping** |
| 10 | **NSF CS2 #2546694 (Crotty), MutDafny (2025) & Clover/SpecGen** | **High** (specs) | Concolic PBT / SMT | **Very High** (spec mutants) | None | Partial (in CS2 #2546694) | None | Legacy Fortran/C to spec | **High** (in CS2 #2546694) | **Overlapping** |
| 11 | **Rely (OOPSLA 13) & ApproxHPVM / ApproxTuner** | Partial (specs) | Static + empirical | None | None | **High** (error + reliability) | **High** (Pareto autotuning) | LLVM IR across devices | **High** (tensors, kernels) | **Overlapping** |
| 12 | **NSF CS2 #2546786 (Tensor Seq) & #2446084 (DANUBE)** | Partial (SMT/formal) | SMT + e-graphs | Counterexample refinement | None | **High** (QF_FP + bounds) | **High** (Pareto FLOP/error) | DSLs to HPC hardware | **High** (quantum chem/LA) | **Overlapping** |
| 13 | **Interfaces.jl + Supposition.jl + SciML LinearSolve.jl** | Partial (traits) | Ephemeral PBT | Vacuity rejection in PBT | None | Tolerance parameters | **High** (polyalgorithms) | Julia foreign wrappers | **High** (Julia SciML) | **Distinct** |
| 14 | **Bolero + Kani (Rust) & Stainless FP (Scala, 2024-2026)** | Partial (contracts) | Fuzz/PBT + BMC/SMT | Vacuity checks in Kani | Cargo hashes (build only) | Bit-precise IEEE 754 | Engine choice (fuzz vs proof) | Rust C-FFI (in Kani) | Low to Medium | **Distinct** |
| 15 | **Python Stack: Pandera + CrossHair + Deal + Consist (JOSS 26)** | Partial (schemas) | PBT + symbolic Z3 | Postcondition checks | Consist workflow caching | Statistical/range tolerances | None | Python dataframe lineage | Medium (data science) | **Distinct** |
| 16 | **Why3 + Gappa + Alt-Ergo 2.6 & ERC HORNET (Darulova)** | **High** (WhyML) | Deductive multi-prover | None | Why3 session XML hashes | **Very High** (Gappa/Daisy) | Prover routing only | C/Ada via Frama-C/SPARK | **High** (verified numerics) | **Overlapping** |

---

## Detailed Evaluation of Candidates

### 1. Evidential Tool Bus (ETB)
* **What it is:** Developed by Simon Cruanes, Grégoire Hamon, Sam Owre, and Natarajan Shankar at SRI International (building on John Rushby's assurance-case architecture), the Evidential Tool Bus (ETB) is a distributed, Datalog-based framework for orchestrating heterogeneous verification and testing tools (theorem provers like PVS and SAL, SMT solvers like Yices, static analyzers, and test runners). In ETB, verification goals are stated as logical *claims*. Tools are invoked via wrappers to produce *evidence*, and ETB constructs persistent *certificates* linking claims to the tree of tool invocations and input artifacts, keyed by SHA1 content hashes of files and rules so that evidence is automatically invalidated and recomputed only when its dependency cone changes.
* **Fetched links:**
  * Paper metadata (VMCAI 2013): `https://api.crossref.org/works/10.1007/978-3-642-35873-9_18` (also fetched at `https://doi.org/10.1007/978-3-642-35873-9_18`) `[verified]`
  * Repository: `https://github.com/SRI-CSL/ETB` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** Claims are Datalog predicates over program artifacts rather than algebraic theories (types with laws) inhabited by first-class language models. |
| 2. Graded, persistent, composable evidence | **High:** Explicitly persists heterogeneous evidence (deductive proofs, model-checking results, test runs) backing claims and composes them via Horn clauses, though it lacks Luthier's $(\hat\varepsilon, \delta)$ statistical cost algebra. |
| 3. Negative controls and vacuity | **None:** Does not require claims or specifications to refute broken mutant models or track premise vacuity. |
| 4. Content-hash certificates | **Very High:** Certificates record SHA1 digests of all input files and derivation rules in the dependency cone; unchanged hashes reuse cached evidence. |
| 5. Within-bound numerical laws | **None:** Targets Boolean safety properties and static analysis invariants rather than floating-point error transformers. |
| 6. Demand-driven implementation choice | **Partial:** Queries trigger backward chaining (demand-driven evaluation of verification workflows), but ETB chooses how to prove a claim rather than choosing which numerical algorithm specimen to execute. |
| 7. Cross-language provenance | **Partial:** Tracks provenance of verification artifacts across external tool invocations, not runtime numerical values with error bounds. |
| 8. Aimed at scientific computing | **Low:** Aimed at safety-critical cyber-physical and avionics assurance cases. |

* **Verdict:** **Overlapping** (closest prior art to Luthier's content-addressed, demand-driven certificate store and multi-certifier evidence orchestration).

---

### 2. Numerical Fuzz ($\Lambda_{\text{num}}$), Bean, and eggshel
* **What it is:** A trilogy of papers by Ariel E. Kellison, Laura Zielinski, David Bindel, and Justin Hsu at Cornell University published at PLDI 2024, PLDI 2025, and PLDI 2026:
  1. **Numerical Fuzz (PLDI 2024)** introduces $\Lambda_{\text{num}}$ (`NumFuzz`), a functional language and type system that extends Reed and Pierce's linear sensitivity calculus (`Fuzz`) to floating-point rounding error analysis. It tracks Lipschitz sensitivity $L$ through linear types and tracks accumulated roundoff error $\eta$ through a novel **graded monad** over Lawvere-style metric spaces, proving soundness relating exact real semantics to IEEE 754 floating-point semantics.
  2. **Bean (PLDI 2025)** introduces a first-order language combining a **graded coeffect system** with strict linearity to track *backward error* (perturbation of inputs) through numerical linear algebra programs.
  3. **Synthesizing Backward Error Bounds, Backward / eggshel (PLDI 2026, Distinguished Paper)** defines the category `Shel` of backward-stable numerical programs and builds `eggshel`, an automated synthesis tool that handles variable reuse and derives tight backward error bounds.
* **Fetched links:**
  * Numerical Fuzz (PLDI 2024): `https://arxiv.org/abs/2405.04612` and `https://api.crossref.org/works/10.1145/3656456` `[verified]`
  * Bean (PLDI 2025): `https://arxiv.org/abs/2501.14550` and `https://api.crossref.org/works/10.1145/3729324` `[verified]`
  * Synthesizing Backward Error Bounds, Backward (PLDI 2026): `https://arxiv.org/abs/2604.15633` and `https://api.crossref.org/works/10.1145/3808333` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** Uses linear and graded monadic/coeffect function types rather than user-defined algebraic theories and models. |
| 2. Graded, persistent, composable evidence | **Low:** Purely static type-based bound inference; no empirical sampling, finite case lists, or persistent certificate stores. |
| 3. Negative controls and vacuity | **None:** No mutant refutation or vacuity tracking. |
| 4. Content-hash certificates | **None:** Type checking is ephemeral. |
| 5. Within-bound numerical laws | **Very High:** Directly formalizes the coupling of Lipschitz sensitivity ($L$) and additive rounding defect ($\eta$) over metric spaces (`Numerical Fuzz`), as well as compositional backward error (`Bean`, `eggshel`). |
| 6. Demand-driven implementation choice | **None:** Analyzes a single given program; does not select among specimens. |
| 7. Cross-language provenance | **None:** Closed core calculi ($\Lambda_{\text{num}}$ and Bean). |
| 8. Aimed at scientific computing | **High:** Evaluated on numerical linear algebra routines (dot product, matrix multiplication, triangular solvers, Horner's scheme). |

* **Verdict:** **Overlapping** (closest theoretical prior art to Luthier's affine bound transformer $(L, \eta, D, r)$ and backward error laws; directly supersedes the claim in `related-work.md` Section 11 that Fuzz-style type systems only handle multiplicative Lipschitz constants).

---

### 3. GATlab.jl and Catlab.jl (AlgebraicJulia)
* **What it is:** Developed by Owen Lynch, Kris Brown, James Fairbanks, Evan Patterson, and collaborators in the AlgebraicJulia organization, **GATlab.jl** (arXiv 2024) and **Catlab.jl** implement **Generalized Algebraic Theories (GATs)** and their models inside Julia for scientific computing. A `@theory` block declares types, dependent operations, and equational axioms (for example, `ThMonoid`, `ThCategory`, `ThMetric`, or theories of differential equations and Petri nets). Programmers then define multiple `@model` or `@instance` implementations mapping a theory's abstract types and operations to concrete Julia types, data structures (C-sets), or solver backends, and compose models via wiring diagrams and theory morphisms.
* **Fetched links:**
  * Paper (arXiv 2024): `https://arxiv.org/abs/2404.04837` `[verified]`
  * Repository: `https://github.com/AlgebraicJulia/GATlab.jl` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Very High:** Explicitly separates `@theory` declarations (types, operations, and equational laws) from `@instance` / `@model` implementations, and dispatches operations by theory model. |
| 2. Graded, persistent, composable evidence | **None:** Equational laws in a `@theory` are used for symbolic rewriting or manual unit tests; GATlab does not automatically certify models by graded testing or persist certificates. |
| 3. Negative controls and vacuity | **None:** No negative controls or vacuity rejection. |
| 4. Content-hash certificates | **None:** No content-addressed certificate store. |
| 5. Within-bound numerical laws | **None:** Laws in GATlab are exact symbolic equations, not floating-point `Within` laws or bound transformers. |
| 6. Demand-driven implementation choice | **Partial:** Supports multiple models of the same theory (for example, symbolic vs numerical matrices) and model migration along theory morphisms, but selection is manual rather than driven by an accuracy/cost planner. |
| 7. Cross-language provenance | **Low:** Operates within Julia (with occasional serialization via JSON/ACSets). |
| 8. Aimed at scientific computing | **High:** Built specifically for scientific modeling (epidemiology, reaction networks, multiphysics PDEs in `Decapodes.jl`). |

* **Verdict:** **Overlapping** (closest contemporary scientific computing library to Luthier's `G1` principle that a type is a theory and its values are models).

---

### 4. SciLean and PhysLean (Lean 4 for Scientific Computing and Physics)
* **What it is:**
  1. **SciLean** (created by Tomáš Skřivan) is a library for scientific computing in Lean 4. It uses Lean's dependent type classes to represent mathematical spaces (semi-inner product spaces, smooth maps, diffeomorphisms), symbolic automatic differentiation (`revDeriv`, `fwdDeriv`), and specification-to-implementation transformations where a non-computable mathematical specification (such as an integral, optimization problem, or ODE) is rewritten step by step via tactics (`approx`) into an executable numerical algorithm.
  2. **PhysLean** (formerly **HepLean**, created by Joseph Tooby-Smith, arXiv 2024 to 2026) digitalizes physics theories, tensor symmetries, Maxwell's equations, and particle physics models in Lean 4 as typed structures with machine-checked proofs.
* **Fetched links:**
  * SciLean Repository: `https://github.com/lecopivo/SciLean` `[verified]`
  * SciLean Documentation: `https://lecopivo.github.io/scientific-computing-lean/` `[verified]`
  * HepLean / PhysLean Paper (arXiv 2024): `https://arxiv.org/abs/2405.08863` `[verified]`
  * PhysLean Repository: `https://github.com/HEPLean/PhysLean` (redirects to `https://github.com/leanprover-community/physlib`) `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Very High:** Lean 4 `class` and `structure` definitions bundle operations with mathematical laws, and `instance` declarations provide models. |
| 2. Graded, persistent, composable evidence | **Low:** Evidence is binary deductive proof (or unverified `sorry` / `axiom` during development); no statistical sampling bounds $(\hat\varepsilon, \delta)$ or domain-indexed `Cases` vs `Sampled` grades. |
| 3. Negative controls and vacuity | **None:** No requirement that each law refute a wrong model. |
| 4. Content-hash certificates | **Low:** Lean compiles files to `.olean` artifacts, not per-conjunct cone-hashed empirical/deductive certificate stores. |
| 5. Within-bound numerical laws | **Partial:** SciLean has an `Approx` abstraction for limits and discretizations over `Float`, but relies heavily on `sorry` for floating-point rounding proofs rather than empirical/static `Within` bound certification. |
| 6. Demand-driven implementation choice | **Partial:** User-guided tactic scripts transform an abstract spec into a chosen numerical realization, but there is no runtime or demand-driven planner over a certified realization graph. |
| 7. Cross-language provenance | **Low:** Compiles to C via Lean 4's compiler and calls external BLAS, without cross-language value derivations. |
| 8. Aimed at scientific computing | **High:** Directly targets scientific computing, PDEs, optimization, and physics. |

* **Verdict:** **Overlapping** (shares type-theoretic theories/models and ideal-to-realization refinement for scientific computing, but relies on interactive tactic proofs and `sorry` rather than graded empirical certification and controls).

---

### 5. Drasil and MMT Biform Theory Graphs
* **What it is:** Led by Jacques Carette and W. Spencer Smith at McMaster University (with Florian Rabe, Michael Kohlhase, and William M. Farmer on MMT biform theories), **Drasil** is a Haskell-based generative framework for scientific computing software. Instead of writing numerical code directly, authors encode a hierarchy of **Theories** (Theoretical Models, General Definitions, Data Definitions, Instance Models), physical/numerical assumptions, and input subtype constraints (bounds and units). From this single source of truth, Drasil generates complete implementations across multiple target languages (Python, C++, Java, C#, Swift, Julia) alongside a Software Requirements Specification (SRS) and traceability matrices linking every generated code block and test back to the theories and assumptions it depends on. **MMT Biform Theory Graphs** formalize the underlying combination of axiomatic theories (specifications) and algorithmic theories (transformers/implementations) connected by theory morphisms (views).
* **Fetched links:**
  * Drasil Paper (arXiv 2023): `https://arxiv.org/abs/2302.00740` `[verified]`
  * Drasil Repository: `https://github.com/JacquesCarette/Drasil` `[verified]`
  * MMT System: `https://uniformal.github.io/` `[verified]`
  * MMT Module System DOI: `https://api.crossref.org/works/10.1016/j.ic.2013.06.001` `[verified]`
  * Biform Theory Graphs DOI: `https://api.crossref.org/works/10.1007/978-3-642-39320-4_6` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **High:** Organizes scientific domains into explicit Theoretical Models, General Definitions, and Instance Models, with bounded number subtypes matching Luthier's `spec 7.S4` ("the bounds of a number are in its type"). |
| 2. Graded, persistent, composable evidence | **Low:** Generates unit/system test scripts and documentation, not graded $(\hat\varepsilon, \delta)$ certificates. |
| 3. Negative controls and vacuity | **None:** No negative controls per law. |
| 4. Content-hash certificates | **Low:** Traceability graphs use symbolic identifiers/URIs rather than AST cone hashes. |
| 5. Within-bound numerical laws | **Partial:** Tracks input intervals, physical units, and relative/absolute tolerances for generated tests, without composable bound transformers $(L, \eta, D, r)$. |
| 6. Demand-driven implementation choice | **Partial:** A "design" configuration chooses target language, data representations, and ODE solver packages at generation time, without certified identity paths. |
| 7. Cross-language provenance | **High (at generation time):** Maintains full static traceability from physical theories and assumptions to generated code in Python, C++, Java, and Julia, though not runtime value derivations across FFI calls. |
| 8. Aimed at scientific computing | **High:** Built specifically for scientific computing software (physics, mechanics, thermodynamics, slope stability). |

* **Verdict:** **Overlapping** (shares Luthier's knowledge-centric organization of scientific theories, bounded physical quantities, and strict avoidance of duplicated definitions).

---

### 6. LAProof and VCFloat2
* **What it is:** Developed by Ariel E. Kellison, Andrew W. Appel, Mohit Tekriwal, and David Bindel (Princeton and Cornell), **VCFloat2** (CPP 2024) and **LAProof** (ARITH 2023) provide automated, foundationally verified floating-point roundoff error analysis in Coq. LAProof proves Higham-style forward and backward error bounds (using $\gamma_n = nu/(1 - nu)$) for dense and sparse linear algebra algorithms (dot product, matrix-vector multiply, Cholesky decomposition, Sparse CSR matrix-vector multiplication) and links those accuracy theorems via the Verified Software Toolchain (VST) to actual C implementations compiled with CompCert.
* **Fetched links:**
  * VCFloat2 DOI (CPP 2024): `https://api.crossref.org/works/10.1145/3636501.3636953` `[verified]`
  * LAProof DOI (ARITH 2023): `https://api.crossref.org/works/10.1109/ARITH58626.2023.00021` `[verified]`
  * LAProof Repository: `https://github.com/VeriNum/LAProof` `[verified]`
  * VCFloat Repository: `https://github.com/VeriNum/vcfloat` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **High:** Separates mathematical linear algebra specifications, parameterized floating-point accuracy theorems, and C implementations. |
| 2. Graded, persistent, composable evidence | **Low:** Exclusively deductive Coq proofs; cannot certify unverified external Python/GPU libraries empirically via `Sampled` or `Cases`. |
| 3. Negative controls and vacuity | **None:** Deductive proofs in Coq; no mutant refutation controls. |
| 4. Content-hash certificates | **Low:** Standard Coq `.vo` compilation artifacts. |
| 5. Within-bound numerical laws | **Very High:** Proves the exact same Higham $\gamma_n$ dot-product and matrix bounds (`DotStable`, `DotSensitive`) that Luthier encodes in `arrays.lth`. |
| 6. Demand-driven implementation choice | **None:** Verifies specific C functions; no runtime planner. |
| 7. Cross-language provenance | **Partial:** Connects C ASTs (via CompCert Clight and VST) to Coq functional models, but only for C and only at proof time. |
| 8. Aimed at scientific computing | **High:** Directly targets numerical linear algebra and scientific C libraries. |

* **Verdict:** **Overlapping** (the deductive Coq counterpart to Luthier's `numbers.lth` and `arrays.lth` Higham bounds).

---

### 7. Probabilistic Round-Off Analysis (OOPSLA 2026) and NSF CS2 Award #2446214
* **What it is:** Led by Jean-Baptiste Jeannin (University of Michigan) with Yichen Tao, Hongfei Fu, Jiawei Chen, Karthikeyan Duraisamy, and John Sarracino (LLNL):
  1. **Probabilistic Floating-Point Round-Off Analysis via Concentration Inequalities (OOPSLA 2026)** combines Taylor-form symbolic error expansions (as in FPTaylor) with concentration inequalities (Azuma-Hoeffding, Bernstein) to bound floating-point error within a threshold $\varepsilon$ at a user-specified confidence probability $1 - \delta$.
  2. **NSF CS2 Award #2446214 (2025 to 2029)**, *"A Comprehensive Pipeline for Formal Verification of Floating-Point Errors and Compilation for Scientific Computing,"* builds an end-to-end verification pipeline targeting real scientific computing libraries in **C/C++, Fortran, and Julia** compiled through **LLVM**. It combines mechanized functional models, reduced- and mixed-precision accuracy proofs, Coq-verified LLVM translation validation (`Crellvm`), and **evidence and assurance cases** for porting scientific codes (such as plasma and inertial confinement fusion finite-element solvers) to new hardware.
* **Fetched links:**
  * OOPSLA 2026 Paper: `https://arxiv.org/abs/2605.04232` `[verified]`
  * NSF Award #2446214: `https://www.nsf.gov/awardsearch/showAward?AWD_ID=2446214` (and JSON via `https://api.nsf.gov/services/v1/awards/2446214.json`) `[verified; implementation of the full LLVM assurance-case pipeline is in progress under the 2025-2029 grant]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** Functional models of scientific algorithms paired with LLVM IR realizations. |
| 2. Graded, persistent, composable evidence | **Partial:** Combines deductive proofs with probabilistic concentration bounds $(\varepsilon, \delta)$ and assurance cases, though via static analysis rather than black-box/grey-box sampling. |
| 3. Negative controls and vacuity | **None:** Not mentioned in paper or grant abstract. |
| 4. Content-hash certificates | **Low:** Assurance cases over LLVM translation validation, not cone-hashed empirical certificate stores. |
| 5. Within-bound numerical laws | **Very High:** Explicitly bounds floating-point error $(\varepsilon)$ with confidence $(1 - \delta)$ across mixed-precision operations. |
| 6. Demand-driven implementation choice | **None:** Focuses on verifying existing libraries and compiler optimizations rather than runtime algorithm selection. |
| 7. Cross-language provenance | **High:** Targets C/C++, Fortran, and Julia via a shared verified LLVM intermediate representation. |
| 8. Aimed at scientific computing | **High:** Built specifically for HPC scientific computing (finite-element methods, plasma physics, fusion). |

* **Verdict:** **Overlapping** (one of the closest ongoing projects to Luthier's combination of multi-language scientific computing, $(\varepsilon, \delta)$ numerical bounds, and assurance evidence).

---

### 8. Foundational Proof Certificates for PBT (2024) and Programmable PBT (ICFP 2026)
* **What it is:** Two recent PL papers that rethink the architecture of property-based testing:
  1. **Property-Based Testing by Elaborating Proof Outlines (Dale Miller and Alberto Momigliano, TPLP 2024)** reconstructs PBT using focused sequent calculus and **Foundational Proof Certificates (FPCs)** in $\lambda$Prolog. A single logical specification is paired with interchangeable *proof certificate outlines* that dictate whether a universal quantifier is discharged by exhaustive enumeration up to a bound, random sampling, or explicit witness cases.
  2. **Programmable Property-Based Testing (Alperen Keles, Justine Frank, Ceren Mert, Harrison Goldstein, and Leonidas Lampropoulos, ICFP 2026)** introduces **Deferred Binding Abstract Syntax (DBAS)** in Rocq and Racket. DBAS reifies laws/properties as first-class syntax trees decoupled from the *runners* (certifiers) that execute them, allowing the same property definition to be interpreted by different testing or verification engines.
* **Fetched links:**
  * Miller & Momigliano (TPLP 2024): `https://arxiv.org/abs/2406.10053` and `https://api.crossref.org/works/10.1017/s1471068424000176` `[verified]`
  * Keles et al. (ICFP 2026): `https://arxiv.org/abs/2602.18545` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** Properties are first-class logical propositions over programs, though not bundled into algebraic type-class hierarchies with model resolution. |
| 2. Graded, persistent, composable evidence | **High (on certifier separation):** Directly implements Luthier's principle `L9.1` ("a law is the proposition; a certifier produces evidence for it, and one law may have several"), unifying exhaustive, listed-case, and random generation as certificate outlines / runners. Lacks persistent $(\hat\varepsilon, \delta)$ stores. |
| 3. Negative controls and vacuity | **Partial:** Benchmark suites use mutation testing to evaluate PBT runners, and precondition satisfaction is tracked, but controls are not persisted per conjunct. |
| 4. Content-hash certificates | **None:** No AST cone hashing or persistent store. |
| 5. Within-bound numerical laws | **None:** Exact Boolean/logical properties. |
| 6. Demand-driven implementation choice | **None:** Selects test runners, not program implementations. |
| 7. Cross-language provenance | **None:** Single-language embeddings (Rocq, Racket, $\lambda$Prolog). |
| 8. Aimed at scientific computing | **Low:** General programming languages and metatheory. |

* **Verdict:** **Overlapping** (closest recent PL prior art to Luthier's separation between declarative laws and multiple certifier modes).

---

### 9. DualVeri (2026), Rules to Tools / R2T (2026), and FVSpec (2026)
* **What it is:** Three 2026 preprints combining executable specifications, property-based testing, theorem proving, and AI agents:
  1. **DualVeri: Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing (Seongmin Lee, Yaoxuan Wu, and Miryung Kim, UCLA, arXiv:2607.09072)** defines parameterized *property templates* with holes (such as algebraic decomposition, commutativity, and partition invariants) and uses them in a dual-track validation system that both proves the abstract property in **Lean 4** and executes property-based tests against concrete **Python / PySpark** implementations.
  2. **Rules to Tools (R2T): Executable Checks for LLM Agents in Scientific Computing (Jingjie Ning et al., CMU and DP Technology, arXiv:2610.00313)** turns natural-language scientific computing laws (conservation laws, boundary conditions, PDE tolerances, symmetry invariants on `SciCode` and PDE benchmarks) into callable executable verification tools that gate and guide LLM code generation.
  3. **FVSpec: Real-World Property-Based Tests as Lean Challenges (arXiv:2605.12882)** translates Python Hypothesis property-based tests from real repositories into formal Lean 4 theorems to bridge empirical PBT and deductive proof.
* **Fetched links:**
  * DualVeri (arXiv July 2026): `https://arxiv.org/abs/2607.09072` `[verified]`
  * Rules to Tools (arXiv October 2026): `https://arxiv.org/abs/2610.00313` `[verified]`
  * FVSpec (arXiv May 2026): `https://arxiv.org/abs/2605.12882` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **High (in DualVeri):** Parameterized algebraic property templates verified in Lean 4 and instantiated on Python/Spark models. |
| 2. Graded, persistent, composable evidence | **Partial:** DualVeri combines deductive Lean 4 proofs with empirical PBT runs, and FVSpec bridges Hypothesis PBT with Lean 4, but neither unifies them into a single $(\text{domain}, \text{cost})$ algebra or persistent certificate store. |
| 3. Negative controls and vacuity | **Partial:** DualVeri uses templates specifically to prevent vacuous or hallucinated specifications; R2T checks violation detection on buggy scientific candidates. |
| 4. Content-hash certificates | **None:** No cone-keyed certificate store. |
| 5. Within-bound numerical laws | **Medium (in R2T):** R2T encodes numerical tolerances, PDE residuals, and physical conservation bounds as executable checks. |
| 6. Demand-driven implementation choice | **Low:** Used in agentic repair loops rather than a runtime planner. |
| 7. Cross-language provenance | **Partial:** DualVeri and FVSpec pair Lean 4 specifications with Python implementations, without runtime value provenance. |
| 8. Aimed at scientific computing | **High (in R2T) / Medium (in DualVeri):** R2T explicitly targets scientific computing (PDEs, physics, chemistry in `SciCode`). |

* **Verdict:** **Overlapping** (closest 2026 agentic verification prior art to Luthier's dual use of generic algebraic properties and executable scientific checks).

---

### 10. NSF CS2 Award #2546694 (Crotty et al.), MutDafny (2025), SpecGen (2025), and Clover (2024)
* **What it is:** Recent work on specification adequacy via mutation testing (Luthier's negative controls) and LLM-driven specification extraction for scientific and verified software:
  1. **NSF CS2 Award #2546694 (April 2026 to 2030, PI: Andrew Crotty, Co-PIs: Peter Dinda, Anshu Dubey, Christos Dimoulas, Akash Dhruv, Northwestern & Argonne National Lab)**, *"Automatically Extracting High-Level Specifications from Large Scientific Codebases to Enhance Understandability and Correctness,"* uses a neuro-symbolic LLM pipeline with formal guardrails to extract succinct, **executable specifications** from legacy scientific codebases (such as `Flash-X`) and validates implementations against them via **concolic property testing** to support safe refactoring and porting.
  2. **MutDafny (Isabel Amaral, Alexandra Mendes, and José Campos, arXiv:2511.15403, Nov 2025)** and **IronSpec (Goldweber et al., OSDI 2024)** test the adequacy of formal Dafny specifications by injecting syntactic and semantic mutants into verified implementations and reporting a specification gap whenever a mutant still passes verification.
  3. **SpecGen (Lezhi Ma et al., ICSE 2025, arXiv:2401.08807)** and **Clover (Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett, Stanford, arXiv:2310.17807)** synthesize formal specifications using LLMs and check specification completeness by testing whether the specification rejects mutated implementations.
* **Fetched links:**
  * NSF Award #2546694: `https://www.nsf.gov/awardsearch/showAward?AWD_ID=2546694` (and JSON via `https://api.nsf.gov/services/v1/awards/2546694.json`) `[verified; newly funded April 2026 grant, code not yet published]`
  * MutDafny (arXiv Nov 2025): `https://arxiv.org/abs/2511.15403` `[verified]`
  * SpecGen (arXiv 2024 / ICSE 2025): `https://arxiv.org/abs/2401.08807` `[verified]`
  * Clover (arXiv 2023 / SAIV 2024): `https://arxiv.org/abs/2310.17807` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **High:** Specifications/contracts paired with candidate implementations. |
| 2. Graded, persistent, composable evidence | **Partial:** Concolic property testing (CS2 #2546694) or SMT verification (MutDafny, Clover). |
| 3. Negative controls and vacuity | **Very High:** MutDafny, IronSpec, and Clover explicitly test specification discrimination by checking that wrong/mutated models are refuted by the specification, matching Luthier's `L9.14` and the "Luthierizing a library" workflow. |
| 4. Content-hash certificates | **None:** Ephemeral verification runs. |
| 5. Within-bound numerical laws | **Partial:** CS2 #2546694 targets scientific simulation codebases (`Flash-X`); MutDafny/Clover use exact integer/array logic. |
| 6. Demand-driven implementation choice | **Partial:** CS2 #2546694 uses executable specs to validate replacement/ported implementations of scientific modules. |
| 7. Cross-language provenance | **Partial:** CS2 #2546694 extracts high-level executable specifications from Fortran/C++ scientific codebases. |
| 8. Aimed at scientific computing | **High (in CS2 #2546694):** Directly targets large-scale multiphysics scientific software. |

* **Verdict:** **Overlapping** (CS2 #2546694 is virtually identical in goal to Luthier's "Luthierizing a scientific library" application, and MutDafny/Clover directly parallel Luthier's negative controls).

---

### 11. Rely (OOPSLA 2013) and ApproxHPVM / ApproxTuner (OOPSLA 2019, PPoPP 2021)
* **What it is:**
  1. **Rely (Michael Carbin, Sasa Misailovic, and Martin C. Rinard, OOPSLA 2013)**, following their 2012 Coq-verified relational acceptability calculus (cited in `novelty-critique.md`), is a language with quantitative reliability specifications (`r * R(x, y)`), certifying that the output satisfies a relational accuracy predicate with probability at least $r$ as errors and failure probabilities compose across basic blocks.
  2. **ApproxHPVM (Hashim Sharif, Vikram Adve, Sasa Misailovic, et al., OOPSLA 2019)** and **ApproxTuner (PPoPP 2021)** build a compiler IR and runtime autotuner for tensor and scientific workloads that takes an end-to-end quality/error demand from the user, propagates error tolerances through the computation graph using empirical and analytical sensitivity models, and selects among multiple implementation choices (CPU, GPU, FP16, FP32, approximate kernels) on the Pareto frontier of accuracy and performance.
* **Fetched links:**
  * Rely DOI (OOPSLA 2013): `https://api.crossref.org/works/10.1145/2509136.2509546` `[verified]`
  * ApproxHPVM DOI (OOPSLA 2019): `https://api.crossref.org/works/10.1145/3360612` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Low:** Compiler IR nodes and relational specifications rather than algebraic theories. |
| 2. Graded, persistent, composable evidence | **Partial:** Composes reliability probabilities $(1 - \delta)$ and empirical error distributions across a DAG. |
| 3. Negative controls and vacuity | **None:** No negative controls. |
| 4. Content-hash certificates | **None:** Autotuning profiles are not content-addressed by AST cones. |
| 5. Within-bound numerical laws | **High:** Propagates additive/multiplicative error bounds and probabilistic confidence thresholds across operations. |
| 6. Demand-driven implementation choice | **High:** Pulls an end-to-end user accuracy demand backward through the DAG to choose the cheapest implementation per node that meets the accuracy and confidence target. |
| 7. Cross-language provenance | **Partial:** Maps high-level Python/PyTorch/C++ frontends to heterogeneous C/CUDA/OpenCL backends via HPVM IR. |
| 8. Aimed at scientific computing | **High:** Applied to tensor computations, signal processing, and physical kernels. |

* **Verdict:** **Overlapping** (closest systems prior art after PetaBricks and Chisel to Luthier's demand-driven planner and backward tolerance pull-back).

---

### 12. NSF CS2 Award #2546786 (Yu, Li, Yuan) and CS2 Award #2446084 (DANUBE, Gopalakrishnan & Pai)
* **What it is:** Two active NSF CS2 projects combining formal floating-point verification with algorithm selection in scientific computing:
  1. **NSF CS2 Award #2546786 / #2546785 / #2546787 (April 2026 to 2029, PIs: Cunxi Yu, Jiajia Li, Bo Yuan)**, *"Formally Verified and Performance-Optimized Tensor Contraction Sequences in Quantum Many-Body Computations,"* uses SMT solving in `QF_FP` and **equality saturation (e-graphs) that preserve tight numerical error bounds** to explore equivalent tensor contraction implementations (reordering, fusion, mixed precision) and select **Pareto-optimal implementations across FLOP count, memory usage, and verified numerical error**.
  2. **NSF CS2 Award #2446084 / #2446083 (April 2025 to 2029, PIs: Ganesh Gopalakrishnan, Sreepathi Pai, Ignacio Laguna)**, *"DANUBE: Formal Methods for Scientific Computing Bridging the Data-Numerics Behavior Tug-of-War,"* formalizes the numerical requirements of linear solvers and iterative refinement schemes across mixed-precision hardware, guarding solver choices with formal properties of the input matrix spectrum.
* **Fetched links:**
  * NSF Award #2546786: `https://www.nsf.gov/awardsearch/showAward?AWD_ID=2546786` `[verified; newly funded April 2026 grant]`
  * NSF Award #2446084: `https://www.nsf.gov/awardsearch/showAward?AWD_ID=2446084` `[verified; funded April 2025 grant]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** Formal domain-specific specifications for tensor contractions and linear solvers. |
| 2. Graded, persistent, composable evidence | **Low:** SMT (`QF_FP`) and counterexample-guided abstraction refinement. |
| 3. Negative controls and vacuity | **None:** Not mentioned. |
| 4. Content-hash certificates | **None:** Solver-state reuse during SMT search, not persistent cone-hashed stores. |
| 5. Within-bound numerical laws | **High:** Preserves tight numerical rounding bounds across non-associative floating-point reorderings and mixed-precision contractions. |
| 6. Demand-driven implementation choice | **High:** Searches an e-graph / design space of implementations to trade FLOPs and memory against verified numerical error (directly matching the weighted e-graph planner idea in `related-work.md` Section 10). |
| 7. Cross-language provenance | **Low:** Targets tensor contraction compilers and HPC libraries. |
| 8. Aimed at scientific computing | **High:** Quantum chemistry, quantum many-body physics, and HPC linear solvers. |

* **Verdict:** **Overlapping** (independently pursues e-graph optimization under verified floating-point bounds for scientific computing).

---

### 13. Julia Interface & Solver Ecosystem: `Interfaces.jl` + `Supposition.jl` + `SciML LinearSolve.jl`
* **What it is:** In the modern Julia scientific ecosystem, three packages address parts of Luthier's workflow separately:
  1. **`Interfaces.jl`** (Rafael Schouten and Guillaume Dalle) defines formal interfaces (`@interface`) with mandatory and optional conditions and runs automated test suites when a type declares `@implements`.
  2. **`Supposition.jl`** (Seelengrab, 2024 to 2026) brings Hypothesis-style choice-sequence property-based testing (`@check`, `Data.Floats`, precondition filtering, and vacuity rejection when too many generated cases are rejected) to Julia.
  3. **`CommonSolve.jl` and `LinearSolve.jl`** (Chris Rackauckas and the SciML community) provide a unified `solve(prob, alg; abstol, reltol)` interface where dozens of native Julia, C, Fortran (LAPACK, UMFPACK, KLU), and GPU solvers implement one problem specification, and a polyalgorithm automatically chooses or switches implementations based on matrix structure, conditioning assumptions, and post-solve residual safety checks (`residualsafety = true`).
* **Fetched links:**
  * `Interfaces.jl`: `https://github.com/rafaqz/Interfaces.jl` `[verified]`
  * `Supposition.jl`: `https://github.com/Seelengrab/Supposition.jl` `[verified]`
  * `LinearSolve.jl`: `https://github.com/SciML/LinearSolve.jl` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** `Interfaces.jl` pairs `@interface` definitions with `@implements` claims and test suites, though without dependent refinement types. |
| 2. Graded, persistent, composable evidence | **Low:** Ephemeral CI test runs; `Supposition.jl` caches failing counterexamples locally, not composable $(\hat\varepsilon, \delta)$ certificates. |
| 3. Negative controls and vacuity | **Partial:** `Supposition.jl` rejects vacuous runs that exceed a filter rejection threshold; no negative controls. |
| 4. Content-hash certificates | **None:** No cone-keyed certificate store. |
| 5. Within-bound numerical laws | **Partial:** `LinearSolve.jl` and `SciML` pass `abstol` and `reltol` and can check a posteriori residuals, without static bound transformers. |
| 6. Demand-driven implementation choice | **High (heuristic):** `LinearSolve.jl` selects among native and foreign solvers based on operator assumptions and tolerances, though selection is heuristic rather than constrained by certified identity paths. |
| 7. Cross-language provenance | **Low:** Wraps C/Fortran/Python solvers behind one interface, without value derivations. |
| 8. Aimed at scientific computing | **High:** Standard scientific computing infrastructure in Julia. |

* **Verdict:** **Distinct** (a loose collection of pragmatic libraries rather than a unified certification language, though a natural baseline for empirical comparison).

---

### 14. Bolero + Kani (Rust) and Stainless Floating-Point Verification (Scala, 2024 to 2026)
* **What it is:**
  1. **Bolero + Kani** (Camshaft and AWS) is a unified verification and property-based testing framework in Rust. A developer writes a single property harness (`bolero::check!`) with typed generators; the exact same harness can be executed by random PBT, coverage-guided fuzzers (`libfuzzer`, `afl`), symbolic execution, or **Kani** (a bit-precise CBMC-backed bounded model checker that exhaustively proves the property or checks for vacuous reachability).
  2. **Stainless** (Viktor Kuncak's group at EPFL, 2024 to 2026) is a deductive verifier and counterexample finder for Scala with refinement types (`require`, `ensuring`) and algebraic laws, which recently added automated IEEE 754 floating-point verification backed by Bitwuzla, Z3, and cvc5 alongside a verified math library (`FdLibm`).
* **Fetched links:**
  * Bolero Repository: `https://github.com/camshaft/bolero` `[verified]`
  * Kani Repository: `https://github.com/model-checking/kani` `[verified]`
  * Stainless FP Verification Paper (arXiv 2025): `https://arxiv.org/abs/2502.11850` (verified via search summary `[1]` in Stainless query; direct repo `https://github.com/epfl-lara/stainless`)

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Partial:** Refinement types and trait laws in Stainless; property harnesses in Bolero. |
| 2. Graded, persistent, composable evidence | **Medium:** Unifies random sampling, fuzzing, symbolic execution, and bounded exhaustive proof under one specification syntax, without $(\hat\varepsilon, \delta)$ statistical cost composition. |
| 3. Negative controls and vacuity | **Partial:** Kani checks whether assertions are reachable (vacuity check) so dead assertions cannot pass silently; no mutant model controls. |
| 4. Content-hash certificates | **Low:** Standard incremental compilation/VC caching. |
| 5. Within-bound numerical laws | **Medium:** Bit-precise IEEE 754 reasoning (NaN freedom, bounds on elementary functions in Stainless). |
| 6. Demand-driven implementation choice | **None:** Verifies a single implementation. |
| 7. Cross-language provenance | **Low:** Single-language focus (Rust / Scala). |
| 8. Aimed at scientific computing | **Low to Medium:** Targets systems/cryptography (Bolero/Kani) and general verified software/math libraries (Stainless). |

* **Verdict:** **Distinct** (demonstrates unified syntax for random testing and exhaustive/deductive verification, but lacks theories/models, numerical bound transformers, and scientific workflow planning).

---

### 15. Python Scientific Contract & Provenance Stack: `Pandera`, `CrossHair`, `Deal`, and `Consist` (JOSS 2026)
* **What it is:** In the Python and SciPy ecosystem:
  1. **`Pandera`** (Niels Bantilan, Union.ai) provides statistical and structural dataframe schemas (`DataFrameModel`) with column bounds, hypothesis tests (`scipy.stats`), and data synthesis strategies powered by `Hypothesis`.
  2. **`Deal`** (orsinium) and **`CrossHair`** (Phillip Schanely) provide Python Design by Contract (`@deal.ensure`, `@deal.pre`, `@deal.pure`) checked simultaneously by runtime assertions, `Hypothesis` property-based testing, and Z3 symbolic execution.
  3. **`Consist`** (submitted to JOSS 2026) provides provenance-aware caching and queryable lineage for Python scientific workflows.
* **Fetched links:**
  * `Pandera`: `https://github.com/unionai-oss/pandera` `[verified]`
  * `CrossHair`: `https://github.com/pschanely/CrossHair` `[verified]`
  * `Deal`: `https://github.com/life4/deal` `[verified]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **Low:** Function decorators and dataframe schemas rather than algebraic theories and models. |
| 2. Graded, persistent, composable evidence | **Low:** Combines Hypothesis PBT and Z3 symbolic checking ephemerally. |
| 3. Negative controls and vacuity | **None:** No negative controls per contract. |
| 4. Content-hash certificates | **Partial:** `Consist` caches workflow outputs by input/code provenance, not law certificates. |
| 5. Within-bound numerical laws | **Partial:** `Pandera` supports statistical hypothesis tests and range checks on arrays. |
| 6. Demand-driven implementation choice | **None:** No implementation planner. |
| 7. Cross-language provenance | **Low:** Python-centric. |
| 8. Aimed at scientific computing | **Medium:** Widely used in SciPy and data science pipelines. |

* **Verdict:** **Distinct** (the pragmatic Python stack against which `novelty-critique.md` recommends evaluating Luthier).

---

### 16. Why3 + Gappa + Alt-Ergo 2.6 and ERC Starting Grant HORNET (Eva Darulova)
* **What it is:**
  1. **Why3 + Gappa + Alt-Ergo 2.6 (Inria, LRI, OCamlPro, 2024 to 2026):** Why3 is a deductive verification platform whose language (`WhyML`) organizes specifications into `theory` blocks (types, logic symbols, axioms, lemmas) and `clone` instantiations (models realizing a theory). Why3 discharges floating-point verification conditions (modeled via `ieee_float` and Flocq) to multiple backend provers, notably **Gappa** (Daumas and Melquiond, ACM TOMS 2010, which generates formal interval and forward-error certificates) and **Alt-Ergo 2.6** (which enabled native floating-point SMT reasoning by default in late 2024). Crucially, Why3 stores verification sessions in XML files that record **cryptographic shapes and checksums** of each verification condition so unchanged proof obligations are not re-proved when code edits occur elsewhere.
  2. **ERC Starting Grant HORNET (2025 to 2029, PI: Eva Darulova, Uppsala University)**, *"Holistic Rigorous Numerical Verification,"* extends Daisy's static error analysis to relational verification and automated error repair of multi-function floating-point programs (including the OOPSLA 2026 empirical study of floating-point pipelines by Gilot, Wrigstad, and Darulova already cited in `related-work.md`).
* **Fetched links:**
  * Gappa Paper DOI (ACM TOMS 2010): `https://api.crossref.org/works/10.1145/1644001.1644003` `[verified]`
  * Gappa Website: `https://gappa.gitlabpages.inria.fr/` `[verified]`
  * Eva Darulova / HORNET Research Page: `https://malyzajko.github.io/` `[verified; HORNET grant code artifacts in progress for 2025-2029]`

| Ingredient | Proximity to Luthier |
|---|---|
| 1. Theories and models | **High (in Why3):** `theory` declarations and `clone` morphisms directly model algebraic theories and their realizations. |
| 2. Graded, persistent, composable evidence | **Partial:** Persists multi-prover deductive certificates (Coq, Gappa, Alt-Ergo, Z3, cvc5) in a session store, though without empirical `Sampled` $(\hat\varepsilon, \delta)$ grades. |
| 3. Negative controls and vacuity | **Partial:** Why3 has counterexample generation via SMT (`rac`, runtime assertion checking) and smoke detection for inconsistent axioms, but not per-conjunct wrong-model controls. |
| 4. Content-hash certificates | **High:** Why3's session store (`why3session.xml`) hashes canonicalized proof tasks (checksums/shapes) to track obsolete vs valid certificates across edits. |
| 5. Within-bound numerical laws | **Very High:** Gappa, Why3's `ieee_float` theories, and Daisy/HORNET verify tight forward and relative floating-point error bounds. |
| 6. Demand-driven implementation choice | **Low:** Chooses provers, not runtime numerical algorithms (though Daisy/HORNET optimizes mixed precision). |
| 7. Cross-language provenance | **Partial:** Verifies C (via Frama-C), Ada (via SPARK), and OCaml programs against Why3 theories. |
| 8. Aimed at scientific computing | **High:** Core infrastructure for verified numerical and embedded scientific software. |

* **Verdict:** **Overlapping** (Why3 + Gappa combines `theory`/`clone` specifications, floating-point error bounds, and checksummed certificate sessions, though restricted to deductive/SMT proofs rather than empirical testing, controls, and runtime algorithm planning).

---

## Items That Could Not Be Fully Verified

In accordance with `BRIEF.md`, the following items had public metadata or abstracts verified, while their full technical contents or code could not be inspected:

1. **Unpublished implementations of newly awarded 2025 and 2026 NSF CS2 grants and ERC HORNET:** The grant abstracts, PIs, dates, and award amounts for NSF #2546694 (Crotty et al., April 2026), #2546786 (Yu et al., April 2026), #2546821 (Greenman et al., April 2026), #2546361 (Bernstein, April 2026), #2546642 (Kallas, April 2026), #2446214 (Jeannin et al., June 2025), #2446143 (Low & van de Geijn, June 2025), #2446223 (Thakur et al., June 2025), #2446130 (Siegel et al., May 2025), and #2446084 (Gopalakrishnan & Pai, April 2025) were fetched directly from `api.nsf.gov`. Because these are 2025 and 2026 awards, several of their proposed software pipelines (such as Crotty's LLM specification extractor for `Flash-X` and Jeannin's multi-language LLVM assurance pipeline) do not yet have public code releases `[unverified code; grant abstract verified]`.
2. **US-RSE 2025/2026 and SciPy 2025/2026 non-proceedings talks:** Conference schedules and abstracts for US-RSE 2025 (Philadelphia), US-RSE 2026 (San Jose), and SciPy 2025/2026 were searched; talks without full archival papers (such as US-RSE Testing Working Group sessions and notebook tracks) could only be checked at the abstract level `[unverified talk slides; program abstract verified]`.
3. **JOSS 2026 under-review submissions (`Consist`, `saxsabs`):** Tracked via open review issues on GitHub/JOSS (`theoj.org`), not yet assigned final JOSS DOIs `[pre-publication review verified]`.

---

## The Closest Three Candidates and What Luthier Must Say About Each in a Paper

No single project is the same as Luthier, but three groups of work come closest to Luthier's core claims and **must be addressed head-on in any paper on Luthier**.

### 1. Closest on Quantitative Numerical Laws and Type Systems: *Numerical Fuzz ($\Lambda_{\text{num}}$, PLDI 2024), Bean (PLDI 2025), and eggshel (PLDI 2026)* by Kellison, Zielinski, Bindel, and Hsu
* **Why it is in the top three:** In `related-work.md` (Section 11), Luthier argued that linear sensitivity type systems (`Fuzz`, `Granule`) only track multiplicative Lipschitz constants ($L$) and cannot express floating-point rounding because rounding introduces an additive defect ($\eta > 0$). Kellison and Hsu's *Numerical Fuzz* (PLDI 2024) solved that exact problem in a type system by pairing linear sensitivity types ($L$) with a graded monad for additive roundoff error ($\eta$) over Lawvere metric spaces, and *Bean* (PLDI 2025) and *eggshel* (PLDI 2026) extended the program to compositional backward error synthesis.
* **What Luthier must say in a paper:**
  > "Kellison and Hsu's Numerical Fuzz ($\Lambda_{\text{num}}$, PLDI 2024) and its backward-error successors Bean (PLDI 2025) and eggshel (PLDI 2026) show that Reed and Pierce's linear sensitivity typing can be combined with a graded monad or coeffect system to propagate both Lipschitz sensitivity $L$ and additive rounding error $\eta$ statically through functional numerical programs. Luthier's affine bound transformer $(L, \eta, D, r)$ shares this mathematical decomposition of forward error into sensitivity and defect over Lawvere metric spaces. Where Numerical Fuzz and Bean are closed, purely static type systems for first-order or functional kernels, Luthier turns $(L, \eta, D, r)$ into an explicit law (`BoundTransformer`) over user-defined theories that: (1) restricts bounds to an explicit validity domain $D$ and input perturbation radius $r$, (2) admits both theorem-proved and empirically sampled certification over foreign host routines (`extern` in Python, C, or Fortran) accompanied by tightness ratios and negative controls (`doublesThird`), and (3) pulls the caller's demanded tolerance $\varepsilon$ backward to select among competing algorithm specimens."

### 2. Closest on Theories, Checksummed Certificates, and Multi-Tool Evidence: *Why3 + Gappa + Alt-Ergo* and the *Evidential Tool Bus (ETB)*
* **Why it is in the top three:** When a formal-methods reviewer reads that Luthier organizes specifications as theories with models, discharges laws through multiple certifiers, and caches persistent certificates keyed by content hashes of the dependency cone, they will immediately think of **Why3** (`theory`/`clone` modules, `why3session.xml` task checksums, and Gappa floating-point bounds) and SRI's **Evidential Tool Bus** (claims backed by heterogeneous tool evidence keyed by SHA1 digests of files and Datalog rules).
* **What Luthier must say in a paper:**
  > "Maintaining persistent verification certificates keyed by dependency hashes goes back to the Evidential Tool Bus (Cruanes et al., 2013), which orchestrates external analyzers and provers via Datalog claims keyed by SHA1 digests, and to Why3's session store, which caches multi-prover verification conditions (including Gappa floating-point bounds) by task checksums over `theory` and `clone` modules. Luthier builds directly on this architecture and extends it in three ways required by scientific computing. First, instead of treating evidence as a Boolean claim discharged either by deductive proof or by an unquantified tool pass, Luthier represents a certificate's strength as a pair $(\text{domain}, \text{evidence cost})$, keeping finite `Cases` lists incomparable with distributional `Sampled` bounds $(\hat\varepsilon, \delta)$ and checking at execution time (`luthier run`) that the concrete input or demanded confidence lies within the certified domain. Second, Luthier includes the sampling distribution and generator bindings in the cone identity (`id(l, n, g)`) and pools sample stretches across seeds. Third, Luthier requires per-conjunct negative controls (refuted wrong models) and non-vacuous premise counts inside the certificate store so that a trivial or vacuous theory cannot silently certify a scientific pipeline."

### 3. Closest on Scientific Theories/Models and LLM-Assisted Executable Specifications: *GATlab.jl (AlgebraicJulia)*, *Drasil*, and *NSF CS2 Awards #2546694 (Crotty et al., 2026) & #2446214 (Jeannin et al., 2025)*
* **Why it is in the top three:** In the scientific computing community, **GATlab.jl** (2024) and **Drasil** (2023 to 2026) already champion writing scientific software as formal theories and models, while the newest **NSF CS2 projects** (#2546694 on neuro-symbolic LLM extraction of executable specifications with concolic property testing for scientific codebases, #2446214 on floating-point assurance cases across C/Fortran/Julia, and #2546786 on e-graph optimization under verified floating-point bounds) and **MutDafny / Clover / DualVeri** (2024 to 2026) directly overlap with Luthier's specification-testing and library-wrapping goals.
* **What Luthier must say in a paper:**
  > "In scientific computing, GATlab.jl (Lynch et al., 2024) and Drasil (Carette and Smith, 2023) demonstrate the value of separating abstract mathematical theories from concrete models and code generation, while recent work on neuro-symbolic specification synthesis and mutation testing (Clover, MutDafny, DualVeri, Rules to Tools, and the ongoing NSF CS2 projects on executable specification extraction and multi-language floating-point assurance) shows how empirical property testing and mutant refutation can validate specifications against real code. Luthier's contribution is not the invention of algebraic theories, property-based testing, mutation controls, or floating-point error bounds in isolation, but their tight semantic integration into a demand-driven execution model: in Luthier, theories carry within-bound numerical laws and per-conjunct negative controls, foreign implementations in Python or C are certified as specimens with persistent $(\text{domain}, \text{cost})$ evidence, and an external demand governs which certified specimen runs and what typed derivation accompanies the resulting value."
