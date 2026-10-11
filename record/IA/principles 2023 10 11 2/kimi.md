# Critical analysis — internal contradictions with implementation consequences

I read the draft as a specification and tested the L-statements against each other and against the W and G layers. The deepest single fault line: **the draft quietly converted the program from a fixed graph into a demand-indexed object, but kept every principle that assumes a fixed graph.** Most findings below descend from that. Findings are ordered by severity.

---

## 1. Demand-indexed nodes vs. the shared DAG, "each node once," and the paid-once memo

This is the systemic one; five principles cannot jointly hold:

- **L9**: "the unit is the definition; dependencies give the only order there is" — one node per definition, shared by all consumers.
- **L19**: "each node once and whole," memoized; **L14 (draft 4)**: certificates "paid once through the memo."
- **L19 (draft 4)**: a result is identified by code, inputs, mode, **demanded type and tolerance**, model, seed, **and plan**.
- **L4 (draft 4)**: the constructor takes the tolerance as a parameter; "a stricter demand asks for a new check."
- **L13**: the projection is "canonical, one per demand"; **L20**: modules "instantiated on demand with the parameter threaded down from the action."

If node identity includes demanded type, tolerance, and plan, then two consumers of the same definition create *different* nodes, needing *different* certificates — so "each node once" and "paid once" are unattainable, and the memo almost never hits across demands. The draft-4 clauses (cache key includes tolerance; stricter demand → new check) directly contradict the once-clauses they sit next to. **Implementation consequence:** the memo, the certificate cone, and the DAG are the three data structures everything else is built on; they currently have incompatible key schemes. Pick one: either tolerances flow as ordinary values and certificates carry bounds valid at all looser tolerances (requires bounds, not observations — see #5), or drop "once" claims and accept a demand-indexed multigraph.

## 2. What `a : A` means is stated two incompatible ways (inside L2 itself)

- Clause 1: "Belonging to a type asserts the propositions, **laws included**, that the value satisfies."
- Draft 4: "`a : A` is one judgment, **structural and decidable**… what a law adds is **evidence**."

If membership is structural and decidable, it does not assert the laws; if it asserts the laws (into `Cost`), it is not decidable and not one judgment. Compounding it, **L13 (draft 4)** says the type checker "do[es] not depend on the observer," while **L4 (draft 4)** makes the constructor's tolerance come from the demand — the observer. Either type checking is demand-relative (and L13's clause is false) or it isn't (and then nobody checks the `Cost` laws). The fix is to admit two judgments — inhabitation (structural, exact) and certification (graded, demand-indexed) — and rewrite L2's first clause accordingly; but this must be *decided*, because every certificate, cache key, and the L10 class machinery inherits the answer.

## 3. There is no root tolerance

G1: the demand supplies the tolerance. L17: every criterion is a declared, passed parameter — never a constant. But the outermost demand (a `print`, an action) has no caller to pass its tolerance. Either there is a default (a forbidden constant), or an infinite regress of demands. As written, **no end-to-end program can ever be certified.** This needs an explicit decision: a declared, recorded, overridable root tolerance is the minimal escape, and it is a scoped, admitted exception to L17.

## 4. "The demand defines what is computed" is false beyond the laws — and the spec suite inherits the gap

G1's slogan, qualified by L5/D-2026-10-11-d (laws accumulate and need not determine the function) and W5 (the native definition is not an oracle): when the laws under-determine, behavior on un-lawed cases is whatever the specimen does. The demand does not define that computation; the specimen does. Three principles inherit the hole:

- **W1/W2**: the spec is "accept/reject pairs… an executable suite." For under-determined functions there is no ground truth to accept/reject against, and for `Cost` laws there is no reject without a tolerance — which cannot live in the suite (L17). An executable suite of boolean pairs is incompatible with graded, tolerance-carrying truth.
- **L3**: "defining a function defines its test" — but the test derived from partial laws cannot distinguish the intended function from a mutation that preserves the laws, which is exactly what W6's mutation meta-test detects as non-diagnostic. L3 and W6 quietly conflict whenever laws are partial.

The honest resolution — declare behavior beyond accumulated laws implementation-defined, and make spec entries (program, tolerance, grade) triples with suite-level tolerance parameters — contradicts G2's "a function type is its laws" as publicly stated, so the organizers' wording must be retouched too.

## 5. `Cost`'s algebra is open, but principles already hard-commit to three incompatible composition rules

- **L2**: certificates carry "the worst cost seen" — a max-rule, order-dependent, frequentist point statistic.
- **L10 (draft 4)**: chain distance "is the sum of its links" — metric additivity.
- **G3/§4**: costs compose as Bayes composes them, "adding as −log p under independence" — needing priors and independence.

Worst-seen, additive distance, and −log p do not compose the same way, and L10 draft 4's own "closeness is not transitive" denies the metric axioms the sum rule assumes. Worse, G3 makes the cost *itself* uncertain, which worst-seen cannot represent at all. §4 correctly lists this as open — but L2 and L10 have already baked in representation choices (worst-seen, additive chains) that the open item may invalidate. Until the algebra exists, certificates should carry an explicitly *unspecified* uncertainty structure, and L10's chaining rule should be a theorem of the algebra, not a principle.

## 6. Progressive validation vs. immutable, hash-chained certificates

G2: validation "es progresiva." G3: what a run teaches "queda en algún lado." But **L11/L21**: certificates are hashed over the dependency cone, and the "chain law, citation, native, identity, extern is carried by hash"; **L19 (draft 4)**: evidence accumulates "by a separate action with its own record, so 'each node once' and G3's 'kept across runs' never meet on one node." If evidence never meets the certificate, then progress and learning can never upgrade a certificate — they live only in the planner's database, which L19 explicitly excludes from result identity. If they *do* upgrade it, every hash in the chain, every memo key, and W10's reproducibility record break. Certificates need versions and supersession edges, or "progressive" must be downgraded to "the planner's priors improve; certificates are frozen snapshots."

## 7. G0's quotient promise vs. L10's certificate-connected components

§1 (G0 formulation): "con una law tenes un cociente y por lo tanto valores intercambiables… inside a class the representative is free." L10 draft 4: the class is "the component connected by such certificates, **not** everything that passes the laws accumulated so far"; "a lone implementation is never replaced"; chain distances are charged against the tolerance. One law no longer yields interchangeability; the organizer's derivation in §1 was never updated to match the mechanism it supposedly grounds. Someone implementing from §1 builds a quotient; someone implementing from L10 builds a certificate-graph planner. These are different systems.

## 8. L12: "the value is the class's name" contradicts G4/L10

Computing f(x) "places x in its class and the value is the class's name." But naming a class requires a canonical representative, and G4 explicitly names "one canonical form per value" as what type theory has and Luthier rejects; L10's whole point is many representatives with no distinguished one. For `Cost`-carriers there is no canonical name. The slogan survives only for the decidable fragment (normal forms by reduction); as a general claim it is false and should be scoped or deleted.

## 9. Holes: axiom vs. non-inhabitant, and stuck runs

L8: a hole is "at once axiom, program input, external function, pending definition and dead code," **and** "nothing executes until it is defined, and no value inhabits an undefined type." An axiom *is* an assumed inhabitant — the two clauses contradict unless "inhabits" is redefined as "has a computed value." Meanwhile L19 allows holes at run leaves: what does a demanded run return when the leaf is a pending-definition hole (error?), an input hole (supplied by the demand's mark-map? by an action?), an assumed law (never evaluated — but laws aren't values at leaves)? The elaborated kind (L8 draft 4) must be extended to *evaluation* behavior, and "no value inhabits an undefined type" must go.

## 10. The "exactness" vocabulary survives where the mechanism is graded

Several principles state flat exactness claims whose own draft-4 retouches withdraw them: L18 "every evaluation strategy gives the same result" / "the one assumption" (its draft 4: same class *at a distance*, confluence only a certified law — sampled for floats); L9 "dependencies give the only order there is" (conceded: the planner reorders, mutates in place, and the plan is a separately chosen value); L7's person-checkable kernel (impossible the moment a kernel type carries a `Cost` law — so the kernel/user boundary, and whether `Float64` is kernel, must be fixed crisply and is not). A reader implementing from the unretouched sentences and a reader implementing from the retouches will build different languages.

## Two smaller ones worth logging

- **Action verification regresses** (L12): observing the world is an action; verifying an action requires observation; and W10's reproducibility discipline assumes repeatable tests, which irreversible world changes defeat. "Stops where the world can be read back" needs a named, trusted read-back kernel — else L3 fails for the action fragment.
- **Float memo identity** (L21): structural `==` under-certifies (different plans, different bits), law-identity isn't decidable. Listed as open in §4 — correctly, but it blocks the memo in #1, so it is not independently fixable.

---

**Summary for the record:** the draft's own history shows the pattern — each draft-4 correction (tolerance-indexed keys, certificate/identity split, connected-component classes) is sound locally, but none of the principles that assumed the pre-correction world (L2, L9, L14, L19's once-clauses, §1's G0) were rewritten to match. The work that remains is not finding more contradictions; it is propagating the corrections through the principles they contradict, starting with #1–#3, since the memo, the certificate cone, and the type judgment are the load-bearing structures everything else stands on.