The document's most serious problem is that it never decides what a typing judgment *is*. G0 says a value is a proof, so membership is static and certain. G2 and G3 say membership is an observation: graded, revisable, and accumulated across runs. Most of the specific contradictions below come from not choosing between these, or from not stating how the two coexist. I've ordered them by how early they would block an implementation.

## Contradictions that block a first implementation

**1. Membership is both a guarantee and a graded observation.** L2 says "membership is a guarantee." Dependency note 2 in §1 says G2's "validada aunque sea una vez" makes `a : A` "a judgment with a grade." L11 then lists the grades: proved, exhaustive, sampled, assumed. These cannot all hold. A judgment with a grade of "sampled at a level" or "assumed" is not a guarantee.

The practical consequence is that type checking cannot be a pass that runs before execution. It becomes a runtime, demand-dependent process whose verdict can change as evidence accumulates, which is what G3 intends.

L14 and L19 then disagree on when that process runs. L14 says an extern is validated "the first time an action asks for it," so validation is mandatory. L19 says "the tests are actions, so verifying is demanding" and "what never reaches an output needs no certificate." So if a `print` demands an extern's result but no test action is demanded, the two principles give opposite answers about whether validation happens. If it doesn't happen, the printed value carries no certificate, and L2's guarantee is empty.

A way out is to split the judgment in two. `a : A` would be structural, static and decidable, covering the kernel types. `a ⊨_g law` would be a graded certificate. L2 would then claim a guarantee only for the first. You would also need to decide explicitly whether demanding a value implies demanding its certificate.

**2. "Every evaluation strategy gives the same result" is false under L10 and G3.** L18 sells "no effects" as the assumption under which every evaluation strategy agrees. But L10 lets the planner choose among representatives of a class by cost, using a database of measured runs that G3 says persists and grows. Over floats, representatives agree only within tolerance. So the output is a function of code, inputs, mode, the demanded tolerance, the state of the run database and, per L10's "place of execution," the hardware.

This causes three further problems:

- L19's memo key (hash of code, inputs and mode) is incomplete.
- W10's provenance cannot be reproduced.
- L21's identity certificate ("same bits, same seed") fails whenever the planner picks a different representative.

L19's "each node once and whole" also clashes with tolerance. If the chosen representative does not meet the demanded tolerance, something has to be recomputed at higher precision.

The minimal fix has four parts:

- Restate L18 as "every strategy gives a result in the same class."
- Add the demanded tolerance and the chosen plan to the memo key. The `plan.lut` idea from the fourth round is the natural vehicle for this.
- Freeze a snapshot of the run database per execution.
- Allow re-evaluation when the tolerance is not met.

**3. G3 is a candidate and a wish, yet load-bearing.** By the P13 count it guides one decision, and W3 and W4 say to add only what is used. Yet the document itself says G0's quotient and G2's graded inhabitance need it. L9, L10, L11, L15 and L16 all derive partly from it. And its algebra (Lipschitz constants, error propagation, cost composition) is listed as open in §4.

This leaves an implementer with two bad options. One is to build Boolean laws now and later rework the judgment, the quotient, the certificates and L16's equality, which amounts to rewriting the kernel. The other is to wait.

There is a cheap way out that the document almost takes in L21, where the identity law's result type is `Bool` or `Cost`. Fix the interface now: a law returns a `Cost`, and `Bool` is the degenerate cost taking values in {0, ∞}. Then G3 can be filled in later without changing any signature, and it no longer needs to count as load-bearing for the first implementation.

**4. `<-` breaks commutativity.** L9 says statements commute and that time is reconstructed "from dependencies rather than from the text." L16 says the law of `<-` holds "until the next `<-`." The word "next" is textual. Take `x <- x + 1`: read literally, L16's law states `x == x + 1`. It only makes sense after renaming into versions (`x₁ == x₀ + 1`), and that renaming follows text order.

So inside any block that contains `<-`, statements do not commute. The pending decision to keep `<-` banned at top level and allow it in blocks is a reasonable patch. But by W9 it should be named as one: "L9 holds between definitions; inside a block, order is textual."

## Contradictions that will bite later

**5. A quotient up to a distance is not a quotient.** G0 promises classes whose representatives are interchangeable. L10 says "one class per mathematical function," and L12 reads every function as inducing a kernel equivalence. Under G3, though, "within ε" is not transitive. If a ~ b and b ~ c, then a and c are only within 2ε. A planner that chains k bridges "coherent up to the law" can drift by kε, with nothing in the principles bounding k.

L9 already separates the two structures (an equivalence for Boolean laws, a metric space for costs). L10 and L12 still talk as if classes exist in both cases.

A consistent reading would be:

- The quotient lives over the ideal theory (`Real`), where laws are exact.
- The metric lives only in the realization (L15).
- The planner carries an explicit error budget.

That budget needs the composition algebra from §4. So L10's planner effectively depends on G3's articulation, which point 3 shows is unfinished.

**6. The holotype reintroduces what L5 forbids.** Draft 3 makes `\ x { x * x }` the law of `Sqr`. That law is a term. To check a `Float64` specimen against it, the formula has to be evaluated in some model: floats again, or exact rationals or intervals. That is exactly the "second implementation checked against the first" that L5 calls consistency rather than characterization, and that W5 says is not an oracle.

The signature/model distinction doesn't save it, because the formula cannot be evaluated over `Real` itself. Two honest options:

- Distinguish equational laws (which characterize) from defining formulas (which are checked by consistency against an exact model).
- Or say plainly that holotype checks are consistency checks against an exact reference model.

**7. Theories, universes and model resolution.** Three related problems sit in L6 and L20.

The first is the universe. "A theory is a type, a model its inhabitant" (L20's derivation from G0), together with "every type belongs to a theory" and L6's type of types, heads toward Type : Type. That is inconsistent (Girard's paradox). Since laws are propositions, inconsistency would make every law provable and every `proved` certificate worthless. You need universe levels or some stratification, and that has to be fitted into L7's "handful of primitives."

The second is resolution. L20 says the model is "resolved from the scope," but also that "operators are resolved by the type, the type naming its model." When the two disagree, nothing says which wins. D-2026-10-11-j suggests the type should win; if so, the scope clause should go or be restricted.

The third is terminology. The preamble defines a module as "a file as a namespace, until modules are values," while L20 asserts "modules are values."

**8. Holes mean five things that behave differently when demanded.** L8 makes a body-less declaration simultaneously an axiom, a program input, an external function, a pending definition and dead code. Demand distinguishes them:

| Kind | What happens when demanded |
|---|---|
| Input | Requests a value |
| External | Calls the host |
| Pending | Should be an error |
| Axiom | Can be reasoned with but not run |
| Dead code | Never reached |

L19's "at the leaves … a value … is a hole" doesn't say which of these happens.

W6 compounds this. It says "a law not known to be true is worse than a hole," but holes used as axioms *are* laws assumed without being known. And under G3 no law over floats is ever simply "known to be true," only graded. W6 needs restating in G3's terms, for example as "a law with no grade, or with no negative control." L8 needs the kind of a hole to be a declared attribute.

**9. Verifying actions regresses.** L12 (draft 3) verifies an action by observing the world before and after it. Observing is itself an action, so the observations need verifying too. And laws over actions need world state as a value, which L18 confines to actions. This can be implemented for actions whose target can be read back, such as a file written and then reread. It cannot be done in general, and the principle should say where it stops.

## Document-level issues

The document violates its own working principles in ways that matter for implementation, not just for style.

W14 asks for few, rich concepts, and W15 asks for anything beyond one screen to be reported as such. Yet this document carries 5 organizers, 21 L's, 14 W's and references to P1 to P15, all densely cross-cited. P15 (via W14) asks that adherence be cheap to compute, but checking a single design decision against this web is not cheap.

More concretely, W7 says the design stays with Luciano. Yet D1 to D8 are "taken as recommended … his marks pending," and every derivation is marked *Proposed*. An implementation started now would build on derivations that have not been approved. Several of the contradictions above, notably 1, 3 and 5, sit exactly in those proposed derivations, not in his quoted organizers.

## What to decide first

If I had to choose the smallest set of decisions that would unblock an implementation:

1. **Split the judgment** into static structural typing and graded law certificates, and say whether demanding a value demands its certificate.
2. **Make `Cost` the result type of every law**, with `Bool` as its degenerate case, so G3 can arrive later without a kernel rewrite.
3. **Make the plan and the demanded tolerance part of the identity of a result** (memo key, provenance, certificates).
4. **Declare that blocks are ordered.**

The rest can be settled by worked examples, as W2 prescribes. For point 5, a good worked example would be a float-heavy pipeline from sonolocalización, such as GCC-PHAT on a few microphone pairs with a demanded tolerance on the delay estimate. It would expose the quotient-under-a-metric problem and the error budget within a page.