The document's own dependency note (§1, D8) is the right place to start, because the main contradictions radiate from it.

## Structural: G3 is load-bearing and undefined

**1. Status vs role.** G3 is "candidate", "a wish", guides one decision — and the doc says G0's quotient, G2's inhabitance and G1's planner all *need* it. L2/L4 (a type is a guarantee; the certified subtype) cannot be type-checked until the grade algebra exists, and that algebra is in §4 as open. As written, the kernel is blocked on the least developed organizer. The way out is already implicit in the text but denied by D8: on decidable types the exact quotient is correct and harmless, so a Boolean kernel is coherent on its own; G3 is needed only where the carrier is Float. Say that, and the kernel can proceed.

**2. Quotient vs tolerance (L10 vs G1+G3).** L10: "one class per mathematical function… equivalence is established first, the choice among paths follows." G3: equivalence is a distance; G1: the tolerance comes from the demand. A within-tolerance relation is not transitive, so there are no classes, and nothing can be "established first" if the threshold arrives with the demand. L9 already concedes this ("a metric space when they carry a distance"). Implementation question with no answer: what is the key for "same function"? Either the class is fixed at the level of the law's statement (the holotype) and distance is an attribute of each specimen, or "quotient" is dropped for floats.

**3. L4 is Boolean, G3 says laws aren't.** The "fundamental construction pattern" returns a constructor with `Maybe` and a membership function; G3's source says literally "las leyes no sean predicativos a un bool". L21 allows `Bool` or `Cost` as the result of a law; L4 does not. L4 must either be scoped to decidable predicates or get a graded constructor that takes the demand's tolerance — which makes the certified type demand-parameterized, with consequences for L13's forgetting.

**4. Three things called cost.** Under [0,∞) the doc puts (a) the distance by which a law fails on one input, (b) −log p evidence from sampling, (c) a categorical grade (proved/exhaustive/sampled/assumed). They compose differently — distances by Lipschitz/triangle, evidence by product under independence, grades by lattice. L10's "expected loss" needs (a) and (b) together; L16's binding law and L21 need (a); L11 needs (c). This is listed as open, but four L's are standing on it.

## Semantic: the planner contradicts purity and reproducibility

**5. L18 vs the stores written during evaluation.** L18: a definition has no effects, "what is forbidden is what the graph does not show", every strategy gives the same result. But evaluation writes the memo (L19), certifies externs on first demand (L14) and feeds the run database that changes future path choice (L10, G3). The run DB is exactly what the graph does not show. And since float paths differ within tolerance, "the same result" is only true up to the demanded tolerance — L18 is stated Boolean. The fix is pending in §4 under another name: `plan.lut` as a value. Until the plan and the DB snapshot are explicit inputs, L19's memo key (code, inputs, mode) returns results derived under a plan it doesn't record, which breaks W10.

**6. Certificate scope.** L11: the certificate travels with the value. L14/L21: it "stays by hash", per function. "Validated the first time an action asks" is a one-input check — precisely the "passing examples alone" that W6 says is never diagnostic. Separately, Bayesian accumulation across runs (G3) makes a function's grade depend on run history, which is not in the cone hash; so the hash no longer determines the grade. Decide: first-demand certifies the value; the function-level grade is its own action with its own record.

**7. Externs during bootstrapping.** L14: no application without a type with a law. G2 (D-2026-10-11-d): functions may have too few laws to be described. W5: the native/extern agreement test is explicitly *not* a law (acquaintance). So right now, externs with no characterizing law cannot be applied — unless the "native" certificate in L21's chain counts, which G2 says it doesn't. One rule is needed.

**8. `<-` vs L9.** "After `<-` until the next `<-`" is textual order; L9 says time is reconstructed from dependencies, not text. Blocks are already in the spec. Either a block is an SSA sub-DAG (every `<-` is a fresh name; the shared "law" with `:=` becomes trivial) or L9 is false inside blocks. Related: L19 says script and interpreter are the same, while `<-` is banned at a file's top level — a session cannot be saved as a file.

**9. Two model-resolution mechanisms (L20).** The model is the implicit first argument "resolved from the scope", *and* operators resolve by the type naming its model (D-2026-10-11-j). Which wins when a value typed over model M2 appears in a scope whose model is M1? Also the header says a module is a file "until modules are values" while L20 says modules are values.

**10. L15 overstates.** Rounding does not expand distances "by at most a constant" multiplicatively (reals at distance ε can land one ulp apart), and no per-type constant exists for subtraction or division — the condition number is per input, as §4 itself says. Per-value cost (L11) is the consistent reading; the type-level Lipschitz constant should be dropped or marked "where it exists".

**11. L7 vs the planner.** A self-interpreter (L6) with Bayesian ranking over a run database is not executable by hand. Scope L7 to kernel plus a given plan.

**12. G4's headline invites misuse.** "When the language could forbid or allow, it allows" conflicts with L18, "no coupling without a law" (L14) and the `<-` ban. Its actual role (tie-breaker among law-equivalent designs) appears only later.

## Process: the W's vs this document

W2 admits no rule without a worked example; G3 enters with its examples listed as to-do, L21 as candidate without one. W12/W14/W15 ask for few concepts, the most important first, one screen; this file is ~39 KB and buries the critical dependency at the end of §1. W7 keeps the design with Luciano, yet the G→L derivations and the D8 dependency analysis — the basis any W15 conflict resolution would use to order principles — are the model's with marks pending, and there is no stated priority order among G0–G3 at all. P13 is applied to the G's but not the W's; W3 by its own admission is "not often invoked".

Minor: "departs in three places" lists four; "what type theory lacks" sometimes names what is missing (G1) and sometimes what is being dropped (G3, G4); "Tarski" is cited both as the thing to avoid and as the derived route.

If I had to order the fixes: scope G3 to Float carriers (1, 3), make the plan an explicit input (5), decide certificate scope (6, 7), then the `<-`/model-resolution rules (8, 9). The rest can wait for the cost-valued-laws draft.