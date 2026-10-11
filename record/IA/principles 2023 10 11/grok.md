**Critical analysis of Luthier principles (Draft 3): contradictions that risk hampering implementation**

The document is unusually coherent for a generative principles draft. Organizers G0–G4 are derived carefully, L-principles are mostly traced to them, and the way-of-working (W) principles are largely orthogonal and practical. The explicit load-bearing role of the least-developed G3, the P13 decision-count check, and the “candidate” flags show self-awareness. Nevertheless, several structural tensions remain that can block or severely complicate a working implementation.

### 1. G3 (cost-valued laws) vs. the rest of the kernel (most serious)

- G0, G1 and G2 all rely on G3 for soundness of quotients, graded inhabitance and planner ranking. The text itself states that without G3 the quotient collapses to exact equality and “optimización por error” becomes meaningless.
- G3 is still only a draft-0 rationale document, marked candidate by the P13 count (only one decision so far), and described by Luciano as “más un deseo que un principio”.
- Concrete consequences for implementation:
  - Every law must return a value in [0, ∞) rather than Bool.
  - Certificates must carry graded evidence (proved / exhaustive / sampled / assumed) plus uncertainty of the cost itself.
  - Composition of costs needs an algebra (Lipschitz constants, condition numbers, –log p under independence, sampled estimates).
  - The planner (L19) must search and rank by these costs.
  - Floating-point, linear algebra and statistical laws become first-class, but the Boolean fragment that the rest of the language still assumes must be recovered as the special case cost = 0 or ∞.

Until that algebra and the certificate representation exist and are executable, large parts of L10 (one function, many paths), L11 (verification exact or statistical), L12 (evaluation as verification), L15 (ideal → concrete with guarantee) and the demand-driven planner cannot be implemented without inventing ad-hoc Boolean approximations that later break the intended semantics. This is the single largest implementation risk.

### 2. “Laws characterize but need not determine” (L5 + G2) vs. inhabitance and quotients

- L5 (retouched) and G2 explicitly allow a set of laws that do **not** uniquely determine the function; uniqueness up to equality is only the limit, not a requirement.
- At the same time:
  - G0’s quotient (“values intercambiables”) and L10 treat the class of implementations as well-defined.
  - L4’s certified subtype and the “Maybe constructor + membership function” assume a predicate that carves out a clear subtype.
  - L21 distinguishes certificate-of-identity from certificate-of-the-law, but still needs a well-defined law to check against.

If laws may be incomplete, the planner has no unique mathematical object to inhabit, the quotient has no clear equivalence relation, and “validated although once” (G2) becomes ambiguous. Implementation must therefore decide, for every theory, whether the current set of laws is “enough” to generate a usable quotient or whether it must fall back to identity certificates only. That decision procedure is not specified and is likely to be ad-hoc.

### 3. Demand-driven forgetting (L13) vs. dependent history and certificates

- L13 says forgetting is determined by the demand: everything outside the dependency cone of the demanded value is discarded, both at run time and in the type.
- Yet certificates (L11) are hashed over the dependency cone and must travel with the value; grades of evidence and cost uncertainties must persist.
- L9 makes a program a DAG of definitions; L19 memoizes by hash of code + inputs + mode.

A pure “forget everything the demand does not need” rule collides with the need to keep certificates, error bounds and derivation history (W10). The language must therefore maintain two parallel structures: the live computational DAG (which forgets) and a persistent certificate store (which does not). The interaction between the two—especially when a later demand re-uses a previously forgotten intermediate—is not defined and will require careful design of the memoization key and the “what is still live” invariant.

### 4. Universal theories / models (L20) vs. concrete representation choices and bridges

- L20 makes every function universal over models of its theory; a specialization is just another representative of the same law class (L10); the orchestrator inserts bridges by cost.
- Simultaneously L15 requires that Real → Float64 (and similar) is a Lawvere-style functor that expands distances by a controlled amount, not a homomorphism.
- G4 demands that every design alternative remain expressible.

The implementation must therefore:
  - resolve models from scope (or explicit arguments),
  - decide when two models of the same theory are coherent enough to share a function,
  - insert and cost the bridges,
  - keep the error of each bridge visible in the plan.

None of the machinery for “when is a bridge legal / how is its cost composed / how does it interact with graded certificates” is present. Without it, the “write once, run on any model” claim cannot be realized beyond trivial cases.

### 5. Effects and mutability tension (L18 + L9 + L16 + L12)

- L18: definitions have no effects; effects live only in actions.
- L9: a mutable parameter is two variables (before/after); in-place mutation is only a planner optimization.
- L16 (draft 3): `:=` once, `<-` rebinding; both obey the same law “after the act the name equals the term in the equality of its type”.
- L12: execution is an action on the world that is itself verified by observing the world before and after.

The “two-variable” encoding of mutation works for pure dataflow, but once actions can observe and change the external world, the before/after observations must be part of the law of the action. That re-introduces a form of effect into the verification of the executive face. The planner must therefore treat world-observing actions specially, while still claiming that the declarative face remains pure. The boundary is thin and easy to get wrong in the implementation of the session model (still open).

### 6. Specification-first vs. real-application pressure (W1 + W4 + W3)

- W1 + W2 insist that syntax and semantics are fixed on paper with accept/reject pairs before implementation.
- W4 says the real application (sonolocalización) drives growth; only what the application cannot express is added.
- W3 is the brake: start minimal, add only what is used.

These three are in productive tension, but the document does not resolve the priority when they conflict. In practice the application will demand floating-point laws, statistical certificates and model bridges long before the G3 algebra or the full kernel_laws.lut are stable. The risk is either (a) silent patches (forbidden by W9) or (b) the specification becoming a moving target that never stabilizes enough for a trustworthy kernel.

### 7. Minor / secondary tensions

- L7 (“core minimal and executable by hand”) vs. the growing set of graded certificates, cost algebras and model bridges. The paper semantics will become hard to execute by hand once G3 is real.
- L21 (candidate) vs. L5: identity certificates are easy; law certificates require the incomplete-laws problem to be solved.
- W5 (native vs. extern as bootstrapping) vs. the claim that the native definition is “just another specimen”. While laws are incomplete the native version tends to become the de-facto oracle, contradicting the G2 “observation from outside” stance.
- Units (open candidate under G0) will interact with the cost-valued equality and the Real/Float64 functor; adding them later may force retroactive changes to the equality levels (L16).

### Summary of implementation-hampering contradictions

| Tension | Severity | Why it blocks |
|---------|----------|---------------|
| G3 underdeveloped yet load-bearing | Critical | Quotients, planner, graded verification, floats all depend on it |
| Incomplete laws vs. well-defined quotients / inhabitance | High | No clear decision procedure for “enough laws” |
| Demand-driven forgetting vs. persistent certificates | High | Two parallel lifetime regimes must be kept consistent |
| Universal models + bridges vs. missing coherence/cost rules | High | “Write once” claim cannot be realized |
| Pure definitions vs. world-observing actions | Medium | Boundary of the executive face is underspecified |
| Spec-first vs. application pressure | Medium | Risk of unstable kernel or silent patches |

The document already flags G3 and L21 as candidates and lists the open articulation work. The most productive next steps for implementation are therefore:

1. Force a minimal executable fragment of G3 (even if only for a few concrete theories) so that the dependent L-principles can be tested.
2. Define an explicit “law completeness” judgment (or a conservative default that treats incomplete laws as identity-only).
3. Specify the certificate store and its interaction with the live DAG before coding the planner.
4. Freeze a small set of model-bridge rules for the first concrete theories (Real/Float64, perhaps Z7) rather than leaving the general case open.

Until those four points are closed, the elegant organizers will remain difficult to turn into a coherent, executable language.