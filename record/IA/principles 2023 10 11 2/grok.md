**Critical analysis: contradictions and tensions that could hamper implementation of Luthier principles (Draft 4)**

The document is a careful, iterative synthesis. Many apparent tensions are acknowledged and partially resolved (especially in draft-4 retouches around G3, L10, L15, L19, L21). The remaining risks are real and structural. They cluster into a few load-bearing areas.

### 1. G3 (cost-valued laws) is load-bearing yet underdeveloped
The text itself marks G3 as “candidate” by the P13 decision-count test and “the least developed,” yet simultaneously asserts it is load-bearing for G0’s quotient and G2’s graded inhabitance whenever the carrier has a distance.

- On decidable carriers the Boolean kernel can stand alone. On continuous carriers (floats, linear algebra, statistics) the whole story of interchangeability, certificates, and planner choice depends on a cost algebra that is still open (`docs/rationale/11-cost-valued-laws.md` draft 0).
- Concrete open problems listed in §4: representation of uncertain cost inside a certificate, composition algebra (multiplicative Lipschitz + additive rounding defect), and how evidence accumulates across runs without colliding with “each node once.”
- Implementation risk: any early kernel that hard-codes Boolean laws will require a later rewrite of the certificate and planner interfaces; any early attempt to implement full cost will be building on an incomplete theory. The interface proposed (every law returns `Cost`, `Bool` as the two-valued special case) is a good bridge, but the algebra itself is still missing.

This is the single highest-risk item for implementation.

### 2. Exactness vs. distance (L10, L15, L16, L21)
Several principles require both an exact mathematical object and a tolerance-bearing realization:

- L10: the class of a function is exact in the theory (`Real`); in a model with distance it becomes a ball of demanded radius. Substitutions are allowed only along certified equivalences whose distances sum and are charged against tolerance. Closeness is not transitive.
- L15: rounding `Real → Float64` is “non-expansive plus an additive defect,” not a true homomorphism; condition numbers appear for subtraction/division.
- L16: kernel binding is exact; distance enters only when the planner substitutes a representative.
- L21: identity certificates are either `Bool` (bit-identical / structural) or `Cost` (observed distance).

**Tension**: the planner must reason about a non-transitive, non-equivalence relation while the kernel and the type-checker treat judgments as structural and decidable. The draft-4 language (“the class is the component connected by such certificates”) is an attempt to keep the planner’s relation separate from the kernel’s, but the concrete data structures that will carry both the exact law and the accumulated distance (and decide when a chain is still inside the demanded ball) are not yet specified. This is fertile ground for subtle bugs in memoization, substitution, and certificate validity.

### 3. Demand-driven forgetting vs. universal declaration (G1 / L13 vs. G0 / L20 / L2)
- L13: what is forgotten is everything outside the dependency cone of the demanded value; the demanded return type selects which laws are derived.
- L20 / L2: functions are universal over models; a type is a proposition that includes its laws; membership is a guarantee.

**Tension**: the type-checker and cache key are required to be independent of the observer (draft-4 clarification), yet the set of derived laws that actually appear in a certificate depends on the demand. If two different demands on the same expression produce different sets of certificates, either the cache must key on the demand (complicating memoization) or the language must compute the full derivable set and then discard (costly, and contrary to “minimally processed”). The claim that “what is derivable is a property of the expression” is necessary for consistency but not yet demonstrated for non-trivial composition of laws (itself still open in §4).

### 4. Verification grades and progressive validation (L11, L2, L5, L21)
- Laws accumulate; a set of laws need not uniquely determine the function.
- Certificates carry grades: proved, exhaustive, cases, sampled, assumed, with worst cost seen.
- Identity certificates and law certificates are kept separate; the former can carry the latter.
- “Validated at least once” is enough for inhabitance under G2.

**Tension**: progressive, graded evidence is attractive for scientific and floating-point work, but the kernel must still decide, at each demand, whether a certificate is sufficient for the demanded tolerance. Without a clear policy for when a lower-grade certificate may be reused, upgraded, or rejected, the planner can oscillate or silently accept insufficient evidence. The draft correctly separates “the judgment itself stays one and structural” from “the grade is its evidence,” yet the operational rules that turn grades + costs into a yes/no for a given demand are still missing.

### 5. Effects, the world, and memoization (L18, L19)
- Definitions have no effects; effects live only in actions.
- An observation is itself an action; the world is an opaque unique value so that actions are never served from the memo.
- Evidence accumulates by a separate action; “each node once” and “kept across runs” never meet on one node.

**Tension**: the clean separation is elegant on paper. In practice any useful scientific or sonolocation workload will need to read sensors, write intermediate files, or query external services inside what looks like a pure dataflow. The requirement that the world be a unique opaque value forces every observation to be an explicit action; the planner must therefore treat every such action as non-memoizable. This is correct but can easily explode the size of the live subgraph or force awkward staging. The interaction between session blocks (`<-` for exploration, `:=` for locking) and the world-as-value is still open.

### 6. Expressivity vs. minimality / bootstrap (G4, L7, W3, W5)
G4 insists that every alternative be expressible and that the language ask for the equivalence law. L7 and W3 insist on a minimal hand-executable core and “start minimal, add only what is used.” W5 requires dual native/extern implementations with an agreement test that is itself an identity law (L21).

**Tension**: the bootstrap path (native slow conceptual vs. extern fast pragmatic) is essential, yet every new path introduced under G4 must be accompanied by a law that makes it equivalent to existing ones. Early in development the set of laws will be thin; the identity-law test will therefore be the main (and weak) criterion. This is acknowledged, but it means the language will, for a long time, be operating in a regime where G2’s ideal (“known by description”) is not yet achieved and G4’s permissiveness is constrained only by pragmatic agreement tests. That regime is fertile for accidental divergence between native and extern.

### 7. Specification-first vs. real-application pressure (W1, W2, W4)
W1/W2 require paper specification and worked examples before implementation; W4 says growth is driven by the real application (sonolocalización). The document already records several places where the specification was adjusted after implementation feedback (blocks, operators by model, etc.).

This is healthy, but the process itself creates a mild meta-contradiction: the principles demand that the specification lead, yet the only way to discover whether G3’s cost algebra or the composition of invariances actually work is to pressure them with the real application. The risk is either (a) an over-constrained early kernel that later has to be rewritten, or (b) an under-specified kernel that silently acquires semantics from the Python host.

### Summary of highest-priority risks for implementation

| Rank | Tension | Why it hampers implementation |
|------|---------|-------------------------------|
| 1 | G3 algebra still open while being load-bearing | Certificate and planner interfaces cannot be finalized |
| 2 | Exact class vs. non-transitive distance balls (L10/L15/L21) | Substitution and memoization become subtle and error-prone |
| 3 | Demand-dependent derivation vs. observer-independent cache (L13) | Either expensive over-derivation or demand-keyed caches |
| 4 | Graded progressive evidence without a sufficiency policy | Planner may accept insufficient certificates or re-verify excessively |
| 5 | World-as-unique-value + pure dataflow | Practical observation-heavy workloads become awkward or non-memoizable |

The draft-4 retouches have already removed several earlier contradictions (especially around identity certificates, binding exactness, and the interface of `Cost`). The remaining ones are not fatal, but they are concentrated in the continuous, cost-aware, demand-driven core that is precisely the part of Luthier that is meant to go beyond ordinary type theory. Until the open items in §4 (especially the cost algebra and the composition of invariances) are closed with concrete worked examples, any substantial implementation work on the planner or the certificate system risks being built on shifting ground.