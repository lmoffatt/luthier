# Draft 11 of the principles: what changed, for his marks

2026-10-12. Written for Luciano, one screen per section. Draft 11 is `docs/principles.md` at 41fcb26 (steps 1 to 4 of
`record/plan-principles-draft-11-2026-10-12-execution.md`, D-2026-10-12-g to -s). Everything the
model wrote is marked proposed in the record; this lists it. Mark each line ok, no, or a correction.

## The statements, draft 10 against draft 11

| Tag | Draft 10 | Draft 11 |
|---|---|---|
| G0 | Type theory is the guide. | Type theory is the guide. |
| G1 | A type is a theory and its values are its models. | A type is a theory and its values are its models. |
| G2 | Laws are valued in cost: one logic, extended to the non-negative reals. | Laws are valued in cost: one logic, extended to the non-negative reals. |
| L1 | Luthier expresses the invariances of the disciplines. | Luthier expresses the invariances of the disciplines. |
| L4 | Declare, then define, then inhabit. | Declare, then define, then inhabit. |
| L5 (changed) | Equality has levels, belongs to the object, and is a law that composes. | Equality has levels and belongs to the object. |
| L9 (changed) | A program is a DAG of definitions without effects, and statements commute. | A program is a DAG of definitions without effects, and statements commute; actions have effects, and are verified by observing the world before and after. |
| L10 (changed) | The demand determines the computation and the types produced. | The demand determines the computation and the types produced; the meaning of a program, its realization under a plan and its evidence are three objects, never one. |
| L13 (changed) | One function, many paths, chosen by maximizing the performance the demander chooses. | One function, many specimens, chosen by maximizing the performance the demander chooses, along certified identities. |
| L15 | The core is minimal, executable by hand, and its programs are data. | The core is minimal, executable by hand, and its programs are data. |
| L2 (changed) | A type is a proposition, and membership is a guarantee. | A type is a proposition, membership is a guarantee, and the certified subtype from a law is the fundamental construction pattern. |
| L7 (changed) | A law characterizes; it is verified by one operation, exact or statistical; and the certificate of identity is not the certificate of the law. | A law characterizes; a certifier produces its evidence, exact or statistical; and the certificate of identity is not the certificate of the law. |
| L16 (changed) | (none) | A certificate records what is known of a law, its domain, its bound and its evidence; it is frozen, it serves every demand it meets, and it transports along identity. |
| L14 (changed) | Luthier orchestrates other languages; what does not follow its way lives in a world; a foreign function is certified by delegation, and certification transports along equality. | Luthier orchestrates other languages: an extern is a specimen certified by its laws, and what does not follow Luthier's way lives in a world. |
| L6 | Laws combine, and a predicate lifts to a cost. | Laws combine, and a predicate lifts to a cost. |
| L8 | The ideal world is realized with a guarantee. | The ideal world is realized with a guarantee. |
| G3 | The demand defines what is computed. | dissolved into G0 and L10.1 |
| L3 | The certified subtype from a law is the fundamental construction pattern. | merged into L2 |
| L11 | An action is verified by observing the world before and after it. | merged into L9 |
| L12 | No hardcoded constants: every criterion is a parameter. | merged into L10 |

## The clauses that are not settled

- **L5.3** [proposed] Equality is a law of the object: Boolean where the carrier is decidable, a distance where it carries one, and the type of the identity law's result, `Bool` or `Cost`, says which (L7); how a certified identity composes along a path is L16.7.
- **L9.11** [proposed] An action on Luthier's own state, writing a certificate or running a test, is idempotent and memoizable; an action on the world never is: the world is an opaque, unique value, so an action on it is never served from the memo (D-2026-10-12-m, O3).
- **L10.4** [proposed] A decoration of the output is another model of the theory the code was written over (G1): run over dual numbers the code gives its derivative, run over intervals or over pairs of value and cost it gives its error; the demand choosing the output type is the demand choosing the model, and the planner inserts the bridges (L13). The derivative needs nothing new; the error waits for the algebra of costs (O1, O5).
- **L10.17** [proposed] The demand carries the cutoff: the minimal cutoff for a specimen to be considered, applied to the composed bound and the composed evidence cost of a path (D-2026-10-12-h, L16.5); a cutoff does not compose (L6.3), so it lives in the demand and is passed down from it, and no law carries one.
- **L10.18** [proposed] No unrecorded policy constants: thresholds, budgets, limits, statistical levels and the planner's default policies are never constants in code; they are declared, passed and recorded. The kernel's primitives (0, ∞, `lift`, `exact`) and mathematical constants are not policies (D-2026-10-12-n).
- **L13.3** [proposed] (His formula) What the planner ranks is an efficiency, exp(−w·cost) over the resources used, so that a specimen of cost zero has efficiency 1/resources and not zero, with w, the weight between cost and resources, the demand's parameter.
- **L13.5** [proposed] Semantic equivalence forms classes; certified substitutability forms a graph. In the theory the specimens of a function are the quotient by "compute the same function up to the law's equality", one class per mathematical function, the class chosen by law; in a model that carries a distance closeness is not transitive, there is no class, only the ball of the demanded radius (`11` §3), and the planner substitutes one specimen for another only along a certified identity between the two, the identity law of L5 with its result `Bool` or `Cost` (D-2026-10-11-m).
- **L13.6** [proposed] The law gives the candidates; the identity certificates say which the planner may exchange, and they form a weighted graph: a substitution is a path whose summed distance (`11` §2) and summed evidence cost (L16.7) are within the demand's cutoff, so two specimens joined through a third may each replace it and not each other; a lone specimen is never replaced.
- **L13.7** [proposed] A sampled edge is admissible on the distribution it sampled; it composes with edges sampled over the same distribution, the failure fractions summed, and not with others; the demand's evidence cutoff says whether it accepts the path (L16.8, D-2026-10-12-q).
- **L13.11** [candidate] The identity law between two specimens, with its distance, is what admits a second implementation into the planner's graph (D-2026-10-11-m); the agreement test of W5 between native and extern is this law, and the reference formula of a law evaluated over `Rational` is one more specimen, with grade exact, checked by the same law.
- **L2.3** [proposed] A value with a sampled or assumed certificate is a model of its theory with the cost its certificate records (D-2026-10-12-j); "guarantee" means what the evidence says, and the word model promises the evidence, not exactness.
- **L2.7** [proposed] Where the law is into `Cost`, the certificate records the bound it observed, and the demand's cutoff decides whether it serves (L16.5, D-2026-10-12-h); the constructor takes no tolerance.
- **L7.1** [proposed] A law is the proposition; a certifier is a method that produces evidence for it, and one law may have several: a theorem cited, an exhaustive run, chosen cases, a sample, an assumption (D-2026-10-12-k). The law is not the procedure that checks it, and a universal law over an infinite carrier has no certifier that runs it.
- **L7.7** [proposed] Verification by a theorem is `proved` by citation (D-2026-10-11-f); verification by delegation is the same certifier with the host library's guarantee as the theorem cited (LAPACK's backward-error bounds, the condition number their hypothesis) and the library's version and platform as hypotheses the certificate carries; no new grade. A function known correct by a theorem outside Luthier is certified this way, and the chain law, citation, native, identity, extern is carried by hash.
- **L16.1** [proposed] A certificate (Terms) names the law it records as checked, the domain the check covered (a subtype, the cases listed, or the distribution sampled), the bound observed (for a law into `Cost`, the worst cost seen), and the evidence: its grade and, for a sampled check, the sample's statistics converted to an evidence cost (D-2026-10-12-r).
- **L16.2** [proposed] The grade is derived from the domain and the evidence cost: proved and exhaustive have evidence cost 0 on their domain; cases, 0 on the cases listed and ∞ outside; sampled, the finite cost of its statistics on the distribution sampled; assumed, the evidence cost the demand assigns to assumptions, a parameter with no default, so that a demand that names none refuses assumed values (D-2026-10-11-n, D-2026-10-12-r). The five names stay in the certificate for the reader; the planner reads the costs.
- **L16.3** [proposed] The conversion from statistics to an evidence cost is a function with a declared shape, the sample's statistics and the demand's level in, a cost out, filled per theory (D-2026-10-12-r); the first instance is −log(1 − ε̂(n, δ)) in nats, with ε̂ the bound on the fraction of the distribution where the law's bound fails, from n samples at confidence 1 − δ, and δ the demand's parameter.
- **L16.7** [proposed] Certification transports along identity: if B is certified on inputs X with bound b and evidence cost e, and the identity A ≡ B is certified on inputs Y with distance d and evidence cost e′, then A is certified on X ∩ Y with bound b + d and evidence cost e + e′, and by nothing else; a path of identities composes the same way, link by link, the distances summed and the evidence summed (D-2026-10-12-q). (His correction, in grades) A is certified at the weaker of the two grades on X ∩ Y.
- **L16.8** [proposed] Links sampled over different distributions do not compose without a law relating the distributions; links sampled over the same distribution compose by the union bound, the failure fractions summed, which is the probabilistic bound the planner waited for (D-2026-10-12-q). The composition algebra belongs to the theory's cost type, the sum its first instance; whether a demand accepts a sampled path is its evidence cutoff, a parameter (P11).
- **L16.9** [proposed] No operation on certificates raises a grade, lowers an evidence cost or widens a domain without new evidence.
- **L14.6** [candidate] A definition or an implementation that does not follow Luthier's way, an extern with no law yet, a foreign algorithm taken as is, may execute inside a named world (L9): its certificates carry the cost of an assumption (L16.2), the plan shows the world it ran in, and nothing from it enters the planner's graph (L13) nor a certified theory until a law is certified.
- **L6.1** [proposed] Predicates combine by and, or, then, and by a quantifier over a carrier, and the result is a predicate; costs combine by sum, max and weighted sum, and the result is a cost; a combination that mixes the two is a cost, each predicate lifted.
- **L6.2** [proposed] The lift is explicit and named: `lift : Bool -> Cost` sends true to 0 and false to ∞, `exact : Cost -> Bool` is c == 0, with `exact ∘ lift = id`, so `Bool` is a retract of `Cost`, not a subtype, and the planner inserts the lift as a bridge of cost zero; whether the two are homomorphisms waits for the algebra (O1), since Boolean or has no counterpart among the operations of `Cost` yet.
- **L6.3** [proposed] The cutoff is the demand's (L10.17), passed down from it; it does not compose (two links within ε are within 2ε), so no law carries one.
- **L6.5** [proposed] The law of a theory is one law, so its certificate is one certificate; how the grades of its parts combine is the demand's parameter, the vector of grades or the weakest (D-2026-10-12-i); how the costs of its parts combine is the theory's algebra, with two candidate models, min and max, or 1/n log-sum-exp and 1/n sum (D-2026-10-12-p); the composition along a path is the sum (L16.7, D-2026-10-12-q).
- **L8.3** [mark pending] Rounding does not expand distances by at most a constant: two reals astride a rounding boundary land one ulp apart at any distance, so no multiplicative constant exists; rounding is non-expansive up to an additive defect of about ε|x|, and for subtraction and division the sensitivity is per input, the condition number (`11` §7).
- **L8.4** [mark pending] The functor reading stands with "non-expansive plus an additive term", and the cost algebra needs both parts: a multiplicative one where a Lipschitz constant exists and an additive one where rounding enters (`11` §5).

## Terms and prose written in draft 11

- Terms: the grades defined once, with the meaning each had across L2, L7 and L14; the two faces
  (declarative, executive) defined.
- The organizers cut to two sentences each; G3 dissolved (D-2026-10-12-s).
- The Precedence line.
- What is open as O1 to O12 with the clauses each blocks; the done items to the record's drafts table.
- The Keys section.
- The numbers kept from draft 10, with gaps where entries merged (L3, L11, L12) and L16 new; a
  contiguous renumbering is one mechanical commit if you prefer it.
