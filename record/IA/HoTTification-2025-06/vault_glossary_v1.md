# Vault Glossary v1.0 — Formal Term Definitions

---

## 1️⃣ HoTTification

**Definition:**  
HoTTification is the process of transforming a scientific model, algorithm, or modeling language into a formal structure governed by Homotopy Type Theory (HoTT). This includes:

- Types as entities.
- Identity paths as structural equivalences.
- Higher paths as equivalence transformations.
- Dependent types enforcing semantic safety.
- Compile-time structural validation of models.

**Programs using term:**  
- Program 5: Probabilistic Semantic HoTT DSL
- Program 4: ConformationalModel DSL
- MacroIR HoTTification
- Parallel Tempering HoTTification

---

## 2️⃣ Semantic Safety

**Definition:**  
Semantic safety refers to model correctness enforced by structural rules in the modeling language itself, ensuring that only structurally valid models can be constructed. Violations of model consistency are eliminated at the type level, prior to execution or inference.

**Contrast:**  
- Runtime safety: prevents crashes or numeric failures.
- Semantic safety: prevents invalid scientific models from existing.

**Related terms:** HoTTification, Type-Safe Modeling

---

## 3️⃣ Bayesianization (of the Scientific Pipeline)

**Definition:**  
The process of formally mapping scientific knowledge production into explicit Bayesian structures:

- Introduction → Prior.
- Methods → Likelihood.
- Results → Observations.
- Discussion → Posterior.

The goal is to make scientific reasoning auditable, quantifiable, and explicitly probabilistic at every step.

**Program using term:**  
- Program 1: Bayesianize the Scientific Pipeline

---

## 4️⃣ MacroIRization (Implicit DSL concept)

**Definition:**  
The act of feeding structurally defined kinetic models into the MacroIR likelihood recursion engine, which computes full interval-averaged likelihoods for macroscopic current data.

**Note:**  
MacroIR consumes Markov models produced by ConformationalModel DSL or HoTTified model generators.

**Program using term:**  
- Program 3: MacroIR

---

## 5️⃣ Conformational Algebra

**Definition:**  
A compositional system for building kinetic models from conformational state components:

- External product of conformational degrees of freedom.
- Energetic coupling rules.
- Symmetry reduction mechanisms.
- State aggregation based on equivalent coupling configurations.

**Program using term:**  
- Program 4: ConformationalModel DSL

---

## 6️⃣ FIM Self-Consistency Diagnostic

**Definition:**  
An internal validation method for likelihood functions based on comparing:

- Fisher Information Matrix estimated via score covariance.
- Fisher Information Matrix estimated via Hessian of the likelihood.

Agreement between these two estimates validates the correctness of likelihood implementation without requiring full inference.

**Program using term:**  
- Program 3: MacroIR (Validation infrastructure)

---

## 7️⃣ Model Compiler

**Definition:**  
A system that translates high-level mechanistic model specifications into executable, inferable structures (e.g. state spaces, likelihood functions, samplers).

- The DSLs you are building serve as model compilers.

**Example:**  
- ConformationalModel DSL → Markov models → MacroIR engine
- HoTT DSL → Validated model spaces → Inference pipelines

---

## 8️⃣ Runtime vs Semantic Safety Distinction

**Definition:**  
- **Runtime Safety:** Ensuring the model runs numerically.
- **Semantic Safety:** Ensuring the model is structurally meaningful, valid, and scientifically well-posed before execution.

**Conceptual Core of:**  
- HoTTification
- Program 5

---

✅ **Vault Glossary v1.0 complete.**

