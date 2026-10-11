The draft often resolves a tension by adding a clause, but the clause creates a second semantic layer without a rule for how the two layers interact. The implementation-hampering contradictions are mostly there, not in the high-level G0–G3 story.

### 1. Demand-dependent computation vs demand-independent type checking/cache

- **L13 (draft 4)** says what is derivable is independent of the demand, and “the type checker and the cache key do not depend on the observer.”
- But **L19** says a result is identified by code, inputs, mode, **the demanded type and tolerance**, the model, the seed, and the plan.
- **L20** says modules are instantiated on demand with the parameter threaded down from the action.
- **L4** says the constructor takes the tolerance as a parameter and the certificate records the tolerance it was checked at.

If type checking and cache keys are observer-independent, then the demanded type/tolerance cannot determine the path, types, certificates, and memo identity. If they do, L13 is false. This directly affects memoization, incremental type checking, reproducible builds, and session replay. A clean split is needed: an observer-independent elaboration/type cache, and a separate demand-dependent run/memo cache.

### 2. Membership as guarantee vs graded, tolerance-relative, sampled laws

- **L2** says `a : A` is one judgment, structural and decidable for the kernel’s types; what a law adds is evidence.
- **G3/L4/L11/L15** make laws `Cost`-valued, tolerance-relative, statistically sampled, and uncertain over floats.

For certified subtypes, membership is therefore not decidable and not absolute. Worse, if the type does not include the tolerance, two values of the same certified type can carry different guarantees. The implementation must decide whether certified types are indexed by tolerance, whether the value carries an existential certificate, or whether only kernel types are decidable. Otherwise the type checker and the certificate system will disagree about what “`a : A`” means.

### 3. L10’s “class” is three different things

**L10** says:

- the class is exact in the theory (`Real`);
- in a model with distance it is the ball of the demanded radius;
- the class is the component connected by identity-law certificates;
- closeness is not transitive, so planner substitution follows certified links with distances summed.

An exact quotient, a ball, and a connected component are not the same relation. A ball is not transitive; a connected component is a transitive closure; an exact quotient is exact. The planner cannot operate on all three. The implementation needs one operational relation: exact equivalence in the kernel, an approximate preorder with certificates in models, and a planner rule that only substitutes along chains whose summed distance is within the demanded tolerance and whose certificate grade is sufficient.

### 4. L14 external validation vs W5 native/extern bootstrapping

- **L14** says an external function is validated against its type with its laws; “without a type with a law to validate against it is not applied.”
- **W5** says native and extern are written together with an agreement test, and “the practice holds while a function has too few laws to be known by description.”

If there are too few laws, L14 forbids the external function, but W5 depends on it. If identity agreement is enough, then L14’s law requirement is false. This blocks external-library integration and the bootstrapping story.

### 5. Sampled certificates depend on distribution, but the memo key does not include it

- **L11** says the grade of a sampled certificate depends on the distribution sampled, not only on the number of samples.
- **L4** records tolerance, but not distribution.
- **L19** identifies a result by code, inputs, mode, demanded type and tolerance, model, seed, and plan — but not sampling distribution.

A certificate sampled under one distribution can be reused under another, where it may not hold. The distribution or level must be part of the certificate, the law instance, or the demand, and must appear in the memo key if it affects validity.

### 6. L18 confluence vs L9/L12/L16 actions and rebinding

- **L18** says a definition has no effects, and “every evaluation strategy gives the same result.”
- **L9** says statements commute.
- **L12** says execution is an action on the world.
- **L16** introduces `<-` rebinding.
- **L19** says tests are actions.

Pure definitions may commute, but actions and rebinding do not. Over floats, different evaluation orders produce different results unless “same result” means “same class at a recorded distance.” The confluence claim must be scoped to the pure kernel and to a stated tolerance; action order and session rebinding need their own semantics.

### 7. L8’s hole is one thing and five things

**L8** says a declaration without a body is “at once axiom, program input, external function, pending definition and dead code,” but the demand treats them differently: input asks for a value, external calls the host, pending definition is an error, assumed law is reasoned with and never run. It also says nothing executes until the hole is defined, yet an external hole calls the host.

The type checker cannot treat these as one while the demand must distinguish them. The elaborator needs explicit hole kinds and resolution rules. Otherwise external typing, `assumed`, `pending`, and `input` will be conflated in the implementation.

### 8. L15’s rounding/cost algebra is not closed

**L15** says rounding `Real -> Float64` is a functor in Lawvere’s sense, then corrects that no multiplicative constant exists, so rounding is “non-expansive up to an additive defect,” and the cost algebra needs both multiplicative and additive parts. But standard Lawvere functors for metric spaces require a Lipschitz constant. A non-expansive-plus-additive map is not automatically a functor in that category.

The composition of costs — when to add, multiply, use `−log p`, condition numbers, or tolerance — is left open. Without that algebra, L10’s planner cannot rank paths or charge error along substitution chains.

### 9. Certificate hash over dependency cone vs demand-driven forgetting

- **L11** says the certificate is hashed over its dependency cone.
- **L13** says the demand forgets everything the demanded value does not need; the projection is canonical, one per demand.
- **L19** says what never reaches an output needs no certificate, and what reaches one carries its cone’s certificates.

If the hash covers the full dependency cone, forgetting changes the hash. If it covers only the demanded cone, then certificate invalidation and cache reuse become demand-relative. This must be resolved before implementing certificates, memoization, or incremental rechecking.

### 10. L5 “laws do not re-run” vs verification as running

**L5** says a law characterizes and “does not re-run.” But **L3** says defining a function defines its test, **L11** makes verification exhaustive or statistical, and **L19** says tests are actions, so verifying is demanding. The implementation needs a clear distinction between a law as a proposition and a verification method as a run. “Does not re-run” probably means a law is not an oracle or a duplicate implementation, but that must be stated operationally.

### 11. L7 minimal hand-executable kernel vs L19 planner/database/Bayes

**L7** wants a minimal kernel executable by hand, with the planner outside the kernel. **L19** makes the plan a value, includes it in result identity, and has the planner read a run database to choose plans. **G3** adds Bayesian evidence kept across runs.

If the planner can change the plan, and the plan is part of result identity, then the “same program” can produce different identified results. The kernel semantics must be independent of the planner; otherwise hand execution and reproducibility are not well-defined.

### 12. L20 model/type/module coherence is underspecified

**L20** says a function is universal over models, the model is named by the argument type, a carrier with two models is two types, modules are values, and parametrized modules are functions from models to definitions instantiated on demand. This creates several implementation questions: operator resolution, implicit model arguments, coherence when bridges and specializations exist, module identity, and how module instantiation interacts with the action that threads the parameter.

The document decides some of this by fiat (`D-2026-10-11-j`), but the elaboration rules are not yet specified. This will directly affect the type checker and module system.

### 13. Governance contradiction: candidate principles are load-bearing

- **G3** guides one decision so far and is marked candidate, but §1 says it is load-bearing for G0 and G2 over carriers with a distance.
- **L21** is proposed and candidate.
- **L15**’s correction is pending his mark.
- The whole draft is unapproved.

Implementation cannot safely depend on unapproved or candidate principles. Either G3 must be approved, or the implementation must have a Boolean-only fallback for the kernel and certified types.

### 14. Process tension: W1 spec first vs W4 application drives growth

**W1** says syntax and semantics are fixed on paper first. **W4** says Luthier grows only where the real application cannot express something. This is not a semantic contradiction, but it can deadlock work: do you wait for the application pressure, or freeze the spec first? The practical order should be stated: application pressure selects the increment; W1 freezes that increment before implementation.

### Most dangerous for implementation

The highest-risk contradictions are **1–3, 5, 8, and 9**. They touch the type checker, certificates, memoization, planner substitution, and cost propagation. Before coding much further, the project needs explicit decisions on:

1. exact kernel vs approximate certified layer;
2. whether tolerance lives in the type, the value, or the certificate;
3. one operational equivalence relation for L10;
4. the memo/result key and whether sampling distribution is part of it;
5. external validation: law required, identity enough, or provisional;
6. a complete cost algebra for L15/G3;
7. certificate scope and forgetting.

Without those, the implementation will either hard-code unapproved choices or produce unsound reuse and planner substitutions.