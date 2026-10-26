# Luthier's interaction laws: inventory and classification

Written 2026-10-27 by Claude Fable 5.1 on the brief `prompt.md` of this folder (Luciano's
question: is Luthier derivable from what is already established, an exercise of a book, or does it
carry new laws that need a proof?). Read: `record/principles-language.md` (L3 to L14), `docs/spec/`
chapters 5 to 11, `record/decisions.md` (the decisions cited below), `docs/concepts.md` sections 8
to 13, the theories `certification.lth`, `laws.lth`, `test.lth`, `demand.lth`, `plan.lth`,
`world.lth`, `core/properties/functions.lth`, `core/structures/algebraic.lth`, the test programs
under `tests/tester/`, and the three reports of the week: `related-work-2026-10-27/related-work.md`
and `novelty-critique.md`, `foundations-2026-10-27/report.md`. Working tree at 990e468.

Marks: [record] is what the record states (principle, spec clause, decision, or code), [literature]
a published result, [mine] my reading, derivation or proposal. Where a sentence has no mark it is
mine.

## 1. What this inventory is

An interaction law is a statement that mentions two or more of Luthier's elements and follows from
neither alone. The elements, all established (related-work.md section 15): types as theories with
their models, refinement subtypes, property-based testing (PBT, random testing of universal laws
with explicit generators), mutation testing (wrong models broken on purpose, Luthier's controls),
the zero-failure sampling bound (the rule of three) and sequential tests, Higham's rounding-error
bounds, ball and interval arithmetic, content hashing of dependency cones, provenance, algorithmic
choice among implementations. In algebraic terms (the coordinator's frame in the brief): the free
combination of elements is a coproduct, each element kept whole and nothing shared; a gluing law
identifies something across elements, and is what makes the whole more than its parts.

The three classes of the brief:

- (a) derivable from established results: the derivation is given, with the results it uses;
- (b) a known theorem or published mechanism: cited;
- (c) new: what would have to be proved, a proof sketch, and what could make it false. Following
  the brief, a law that holds only under a premise Luthier does not enforce is (c) with that
  premise named, even when its mathematics is textbook once the premise holds.

Symbols, defined once here and used throughout. A law's sampled evidence is the pair (ε̂, δ): ε̂
is the bound on the fraction of the sampled distribution where the law fails, δ the probability
that this bound itself is wrong; n is the number of evaluated cases. A numerical step carries an
affine bound transformer (L, η, D, r): L its sensitivity (a Lipschitz constant of the ideal
function), η its own error at exact inputs (its defect), D the domain where the bound holds, r the
largest input error for which it holds; d(x, y) is a distance. A certificate has a domain X (a
subtype, a list of cases, or a distribution) and a cost (a bound and an evidence cost); ⊕ composes
costs along a path. A cone is the transitive set of definitions a name depends on, and its hash
H(canon(cone) ‖ hosts ‖ interpreter) is the certificate's identity, with canon the canonical form
(bound variables renamed, binder annotations erased) and hosts the host code behind each extern.

## 2. The table

| # | Law (short) | Elements joined | Where stated | Class | Citation or sketch (section 3) | Free combination that violates it | Certified on itself |
|---|---|---|---|---|---|---|---|
| IL1 | A pass is evidence about its model; a control is evidence about the law, and transfers to every model | PBT (pass), mutation testing (control), types as theories (model of T) | D-2026-10-22-a, -d; L9.14; concepts 8.4; spec 7.S22 | (a) | A control shows the law's predicate is not identically true on the model space, a property of the predicate; a pass is an instance. FitSpec's property adequacy vs test outcome | PBT plus mutation with no theory: a mutant killed under M's tests taken as evidence for N; a pass on M serving N | yes: `Routing` (`AnEntryAboutAnotherModelVetoesNothing`, `AConsequenceRefutesEveryModel`), `certification_route_controls.test.lut` |
| IL2 | The unit of control is the conjunct: a control refutes one conjunct and says nothing of the others | mutation testing, conjunction of laws, the store | D-2026-10-25-a q4; L9.14; spec 7.S22 | (a) | Refuting c_i on a mutant leaves c_j unconstrained (propositional logic); FitSpec's per-property kill matrix | A control that stops at the first refuted conjunct (Luthier before bite D1): a broken monoid refuted at Associative leaves Neutral uncontrolled | yes: the tester runs every conjunct of a control (7.S22); D1's list of uncontrolled conjuncts (`uncontrolled-2026-10-26.tsv`) |
| IL3 | A theory is done when every conjunct has a refuted model | mutation testing, theory as conjunction | L9.14; D-2026-10-15-a | (c), premise: every conjunct is refutable by some structure of the signature | False as a universal requirement: `EmptyIsInitial`, conjuncts fixed by a wrapper's branch (report-controls-M.md) | Counting a theory "controlled" when the unrefutable conjuncts are dropped from the count | no: `check -v` lists uncontrolled conjuncts; nothing states which are exempt |
| IL4 | A premise that never held leaves a sampled law unsettled; the evidence of P → Q counts the cases where P held | PBT, material implication, the sampling bound | spec 7.S12; L12.7; `VacuousIsUnsettled` (laws.lth); D-2026-10-16-m | (a) | The binomial bound on the conditional distribution uses k = held, not n; Beer et al. 2001 for detection; QuickCheck's `==>` discards | PBT counting discarded cases toward n (a law with held = 1 of 200 claiming ε̂ = 3/200) | partly: `VacuousIsUnsettled`, `vacuity.test.lut` with its controls (A3, A3b); ε̂ at serve time reads the region's n, not held (`certify.epsilon_hat`) |
| IL5 | A sampled pass with n cases and no failure is worth ε̂(n, δ) with (1 − ε̂)^n ≤ δ, computed at the demand's δ from the stored n | sampling bound, certificate store, demand | L10.3; spec 7.S11; `SoundAtNoFailure` (certification.lth) | (c), premise: the n draws are independent draws from the declared distribution | Textbook once the premise holds (Hanley and Lippman-Hand 1983; Clopper and Pearson 1934); the live sampler violates it (foundations report, finding 1) | PBT caching a pass with the seed and counting its rerun; a deterministic rotation counted as n independent draws | partly: `SoundAtNoFailure` on `ruleOfThree` (`bases_laws.test.lut`); `DrawsAreIndependent` is stated of `Random` (generators.lth) and not certified of the sampler in use |
| IL6 | Stretches of one law, cone, binding and distribution pool as one sample, n the total; a replay is not a new stretch | sampling bound, content hashing (identity), seeds | D-2026-10-16-g; spec 7.S13; `Pooling` (certification.lth) | (c), premise: streams under distinct seeds are independent and do not overlap | Derivable given the premise, and optional continuation is harmless for zero-failure bounds (sketch in 3.6, mine); overlap found (seeds 7 and 8 share 99 of 100 positions) | A cache that sums every entry (a replay counted twice); one that keeps only the latest stretch | partly: `TheUnionIsMonotone`, `AReplayIsNotANewStretch`, `pooling_controls.test.lut`; the premise is not certified |
| IL7 | What the hash forgets does not change the verdict: alpha-renaming, binder annotations, module prefixes, the order of definitions | content hashing, the kernel's reduction | L10.4; spec 3.S34, 6.S8; D-2026-10-15-e; `ErasureKeepsTheStep`, `HashOfTheCanonicalForm` | (a) | The alpha-equivalence lemma (Barendregt 1984, ch. 2); the erasure lemma for this kernel, certified; Unison's canonical hashing | Hashing the source text (Nix): a comment invalidates everything; or hashing less than the cone (a helper's change not seen) | yes: `ErasureKeepsTheStep` with the control `greedyErasures`; `ConeHashing` laws (`certification_laws.test.lut`) |
| IL8 | The identity captures everything that changes the verdict: a sampled pass is worth its ε̂ only then, and a disagreeing exact replay reveals an omission | content hashing, sampling bound, PBT generators, hosts | spec 7.S9, 6.S8; L9.6; D-2026-10-15-f; L5.6 (the result key) | (c), premise: the verdict is a function of (cone, hosts, interpreter, binding, seed, the budgets that change draws) | The detector is sound (contrapositive of determinism); completeness is not decidable for externs and is false today: `os.getenv` and BLAS threading change results under one hash (foundations report) | Keying a cached pass by file path and version string; a pass keyed by the cone with the generator left out (two distributions, one entry) | partly: `IdentityIsTheKey`, `ADisagreementRefutes`, `ADisagreeingReplayIsKept`, `HashSeesTheHost`, `HashSeesTheInterpreter`, controls in `certification_controls.test.lut`; completeness cannot be certified, only its violations caught |
| IL9 | Evidence along a chain composes by the capped sum min(1, a + b) in each part of (ε̂, δ); the product only under a declared independence premise | sampling bound, path composition, cost algebra (dioid) | D-2026-10-25-a q1; L10.8; `AtLeastTheUnionBound`, `FailuresIndependent` (algebraic.lth) | (a) | Boole's inequality on the union of the links' failure events and of their bound-wrong events; premise, stated in L10.8: the links are sampled over one distribution | Summing nats (multiplying success bounds) with nothing said of independence: 0.19 against 0.2 at (0.1, 0.1) | yes: `cappedSumComposition` certified `AssumptionFreeComposition`, `productComposition` refuted as its control (`bases_controls.test.lut`); the composition along a path of entries is a hole (`entryEvidence`) |
| IL10 | Transport along a certified identity: B certified on X with bound b and evidence e, A ≡ B certified on Y with distance d and evidence e′, then A is certified on X ∩ Y with bound b + d, evidence e ⊕ e′, the weaker grade, and nothing outside | types as theories, metric (triangle inequality), evidence composition, refinement (domains) | L10.7, L9.9, L12.7, L6.9; spec 6.S11, 9.S9; concepts 8.5 | (a), for a distance-valued law along a distance identity and for any law along a structural (Boolean) identity | Triangle inequality d(A, ref) ≤ d(A, B) + d(B, ref); Leibniz substitutivity for `==`; conjunction of hypotheses for the domain; Mardare, Panangaden and Plotkin 2016 (the triangle rule in place of transitivity) | Substitution with no certificate (PetaBricks' alternatives); a lookup table equal to the native on a grid used off the grid | yes, Boolean slice: `TransportNeedsTheIdentity`, `TransportTakesTheWeaker`, `TransportOnTheIntersection`, controls C7 in `certification_controls.test.lut`; the distance part is a hole |
| IL11 | A Boolean law transports along a metric identity with the distance added | Boolean laws, metric identity, transport | spec 6.S11 read literally for a Boolean law (bound `lift true` ⊕ d) | (c), premise: the law is a distance (a `Within` law), or is stable under the identity's distance (has a margin) | Counterexample: B(x) = 0.001, A(x) = −0.001, within 0.002; "positive" holds of B and not of A (novelty-critique section 4). Needs a per-law transport rule, a logical relation or a margin | Transporting any property across any agreement within tolerance (what a test suite does when it compares two implementations and then trusts the second's invariants) | no: `transport` takes any `Standing` (the Boolean slice does not see the law's value); nothing refuses a Boolean law on a metric link |
| IL12 | No evidence for free: every operation on certificates is monotone, and only a certifier builds a certificate | certificates, cost algebra, the language's abstraction | L10.9, L10.10; spec 6.S13 | (b) | LCF's abstract type `thm` (Gordon, Milner and Wadsworth 1979): induction on the constructions, each monotone | A certificate as a plain record anyone writes (a JSON file edited by hand); a cache that "upgrades" a looser certificate on a hit | partly: `NoEvidenceForFree`, `PathNeverRaises`, `PruningNeverRaisesAGrade`, `CombineNeverRaises`, `RestrictNeverRaises` with controls; L10.10 is not enforced by the language today (`x.cert.json` is written by `certify.py`) |
| IL13 | A certificate's strength is (domain, cost); Cases and Sampled are incomparable; a Cases entry serves only at the inputs it lists; a sampled one serves its distribution | certificate grades, refinement subtypes (domains), evidence cost | L10.2, L10.5; D-2026-10-25-a q2; `Folding`'s `OutsideTheReachHoldsNothing`, `ReachesAsSets` | (a) | A finite list says nothing at an unlisted input (no induction); a sample bounds a fraction; the product order on (⊆, ≥) | The chain Assumed < Sampled < Cases < Exhaustive < Proved admitting a Cases entry at an unlisted input (today's Boolean slice, listed in L10.5 as the gap) | partly: `ACoveringPassServes`, `CertifiesOnlyUnderItsBinding`, `ReachesAsSets`, `cutoff_controls.test.lut`; admission by reach at a run's input waits for the cost types |
| IL14 | A numerical law is two laws with theorems' bounds, stability at exact inputs and sensitivity to inputs, with its validity region as a premise sampled on both sides | Higham's bounds, PBT with tolerances, regions | L9.18, L13.3; D-2026-10-18-j; `Within`, `Measuring` (laws.lth); arrays.lth `DotStable`, `DotSensitive` | (b) | Higham 2002 §1.5 to 1.6 (forward error ≤ condition × backward error), §3.1 (γ_n); Rigal and Gaches 1967; Rosa (Darulova and Kuncak 2014) separates the two | An agreement test `|a − b| ≤ tol` with tol a constant of the library (numpy's `allclose`) | yes: `DotStable`, `DotSensitive` on the host's dot with the controls `doublesThird` (a bound tightened below the theorem) and `noRoom`; the law cited, the specimen tested (D-2026-10-27-b) |
| IL15 | Two transformers compose as (L₂L₁, L₂η₁ + η₂, D₁ ∩ f₁⁻¹(D₂), min(r₁, (r₂ − η₁)/L₁)); over inputs by the sum, the max where named; the pull-back is δ = (ε − η)/L, nothing below η, nothing without L | Higham's bounds, Fuzz's sensitivity typing, refinement (domains), the demand | L13.4, L6.8, L13.5; D-2026-10-25-a q3; `BoundTransformer` (functions.lth) | (a) | Triangle inequality plus Lipschitz on the second step (sketch in 3.15); Reed and Pierce 2010 for the sum over inputs; Chisel (Misailovic et al. 2014) for the backward allocation | Adding defects without the second sensitivity (η₁ + η₂, the control `dropsCarried`); a pull-back ε/L that ignores the defect | yes: nine laws, seven controls, `transformer_laws.test.lut`, on listed dyadic transformers only; the specimen's Float64 arithmetic is not sound on non-dyadic coefficients (associativity fails at 0.1, 0.2, 0.3; the pull-back overshoots by one ulp, novelty-critique section 3) |
| IL16 | A ball (midpoint m, radius ρ) through an operation has radius Lρ + η, L and η those of the step's transformer at m | ball arithmetic (Arb), bound transformers, decorations as models | decisions.md's proposal `RadiusWithinTransformer` (related-work section 3); L5.4 | (a), with L the transformer's Lipschitz bound over the whole ball (ρ ≤ r, m ∈ D), as `Realizes` defines it | d(f(x), g(m)) ≤ d(f(x), f(m)) + d(f(m), g(m)) ≤ Lρ + η for x in the ball: the mean-value form of interval analysis (Moore 1966; Neumaier 1990); Arb propagates the same way (Johansson 2017) | Reading L as the derivative at the midpoint: f(x) = x² at m = 1, ρ = 0.1 gives 0.2 against the true 0.21 (comparison-basis section 4); first-order error propagation at a point | no: no `Ball` carrier exists; `Ball` in equality.lth is a predicate "within a radius" |
| IL17 | A decoration of the output is another model of the theory the code was written over, and a certificate at the identity carries over to it | types as theories, interval and dual-number arithmetic, parametricity | L5.4; spec 8.S1 (Wadler's theorems for free); O5 | (c), premise: the decoration satisfies the theory's laws, exactly or within its own defect | True for dual numbers (forward-mode differentiation is exact, Griewank and Walther 2008); false for intervals on exact laws: [−1, 1] − [−1, 1] = [−2, 2], not 0; intervals model the enclosure version (Moore's inclusion isotonicity) | Running code written over a field on intervals and claiming the field's laws of the result | no: nothing certifies a decoration as a model; `NumberModel` does not exist (spec 11.S3) |
| IL18 | Specimens form a graph, not classes: closeness is not transitive, substitution is a path whose summed distance and evidence meet the cutoff, a lone specimen is never replaced | algorithmic choice, metric (tolerance relation), certificates | L6.5, L6.6; D-2026-10-11-m; spec 9.S5 to 9.S9 | (b) | Tolerance relations have no quotient (Zeeman 1962); quantitative equational logic replaces transitivity by the triangle rule (Mardare, Panangaden and Plotkin 2016) | An equivalence class of interchangeable algorithms (PetaBricks, an autotuner): A ~ S and B ~ S taken as A ~ B, 2ε apart | no: the planner is not built (spec 9.S2, 9.S17) |
| IL19 | The cutoff is the demand's and does not compose: no law carries a tolerance | metric (triangle), the demand, laws | L12.3, L5.17; spec 5.S7 | (a) | Two links within ε are within 2ε, so a tolerance written in a law is violated by any composite; lowering a cutoff loses nothing admitted (monotonicity) | Per-function tolerances fixed in a library (`atol = 1e-8`) | yes: `ServesIsMonotoneInTheCutoff`, `LoweringLosesNothing`, `cutoff_controls.test.lut` |
| IL20 | A kernel change transports certificates along a certified edge H_old → H_new whose domain is the programs compared | content hashing (the kernel's hash), certified identities, the kernel as a specimen | D-2026-10-27-a; L14.3; L10.4 | (c), premise: the kernel's behaviour on the certified cone is covered by the programs compared | The sound form is translation validation per cone (Pnueli, Siegel and Singerman 1998): compare the two kernels on the cone that transports. Counterexample to look for: a rule (nested `match`) no test program reaches that a user's cone does | Including the interpreter tag in every hash (everything stale at each change) or excluding it (nothing stale, nothing checked) | no: no edge store exists (`certify.py` hashes the interpreter's revision) |
| IL21 | A value carries the projection of its derivation the demand asks; a requirement on it is a certified subtype; the equality of consequence is a certified relation, with a canonical form at the Boolean level only | provenance (PROV, proof-carrying data), refinement subtypes, metric non-transitivity, the demand | L5.22, L5.23, L10.13, L11.10; D-2026-10-22-c, D-2026-10-25-a q5; O13 | (c), premise: the Boolean equality of consequence is restricted to a fragment with a confluent, terminating rewrite system of certified exact identities | The projection and the subtype are instances of L8.5 (a); the metric part is IL18; a canonical form for observational equivalence of programs does not exist (Rice 1953; Richardson 1968), only for a rewrite fragment (Baader and Nipkow 1998). Proof-carrying data (Chiesa and Tromer 2010) gives the local-predicate form of a derivation law | A trace kept whole as provenance (PROV, RO-Crate) with no law over it; or a hash taken for the quotient | no: only the result key exists (spec 8.S8); O13 open |
| IL22 | On a pure cone any order gives one result: the strategy is a parameter, forward on demand and call by need agree, and an acting cone is never served from the memo | pure definitions (no effects), dataflow, memo keyed by the plan | L5.2, L5.11, L4.7; spec 8.S3 to 8.S5, 10.S6; `Confluent`, `StrategiesAgree`, `ActionConeIsNeverServed` (plan.lth) | (b) | Determinacy of Kahn networks (Kahn 1974); confluence of pure reduction (Church and Rosser); on a finite DAG, each node a function of its inputs, every topological order computes the same values | A session with effects where order matters served from the memo; a memo serving a cone that prints | yes: `plan_laws.test.lut`, controls `plan_controls.test.lut` (a reversed schedule, a node named twice, a hidden read) |
| IL23 | An action is verified by observing the world before and after; an own action is idempotent and memoizable, a world action never; an action changes only the places it declares | Clean's unique world token, certification (laws over observations), the memo | L4.9 to L4.11; spec 10.S6, 10.S7; world.lth `OwnIsIdempotent`, `ChangesOnlyDeclared`, `HostChangesOnlyDeclared` | (a) | Uniqueness typing serializes effects (Barendsen and Smetsers 1996); an idempotent act applied twice is observationally one act, so serving the second from the store is unobservable, under the premise (stated in L5.20) that no third party writes in between | Memoizing a print; a host action trusted as a primitive with no observation (Clean's I/O) | yes: `world_laws.test.lut` with `world_controls.test.lut` (a no-op host, a print that also writes a log); the roots of trust `FileSystemKeeps`, `SystemDelivers` are axioms, assumed |
| IL24 | An extern is validated against its type's laws before it is applied; one with no law is not applied; a provisional one runs as assumed and the grade propagates downstream | refinement types at a boundary (contracts), certification, hosts | L11.2, L11.3; spec 10.S10; world.lth `Externs` | (b) | Higher-order contracts at module boundaries (Findler and Felleisen 2002); hybrid type checking (Flanagan 2006); the downstream grade is the weakest along the cone (monotone, IL12) | Calling a foreign routine on its documented signature alone; a flag that opts out of certification | yes: `AppliedWhenSettled`, `NoLawNoGrade`, `ProvisionalIsAssumed`, `IdentityCarriesHash`, with controls (a validator that applies every extern, a blanket acceptance) |
| IL25 | Test the weakest link: a chain's failure bound is the capped sum of its links, a cited link costs zero, so effort goes to the largest term, and an established result is cited, not run | evidence composition, citation (grade proved), the specimen | L9.19; D-2026-10-27-b; spec 6.R1, 6.S9 | (a), premise named: the citation matches the law, checked by the person 6.R1 records (`who`) | Corollary of IL9: minimizing Σ ε̂_i by moving effort to max ε̂_i; 0 ⊕ x = x for a proved link. The premise is a trust declaration, not a proof object (novelty-critique section 1) | Re-sampling Higham's lemma on the doubles and counting the run as evidence for the law; or citing a theorem whose hypotheses the specimen does not meet | no: the clause is new (D-2026-10-27-b); `cite` records `who`; nothing yet distinguishes a regression of the machinery from evidence of a law |

Counts: (a) 12 (IL1, IL2, IL4, IL7, IL9, IL10, IL13, IL15, IL16, IL19, IL23, IL25); (b) 5 (IL12,
IL14, IL18, IL22, IL24); (c) 8 (IL3, IL5, IL6, IL8, IL11, IL17, IL20, IL21).

## 3. The arguments

### 3.1 IL1, a pass is about its model, a control about the law

[record] D-2026-10-22-a (his words: "sirve para la teoria pero no para el modelo no?"), with
D-2026-10-22-d's exception: a failure on N of a law stated for every model of T, where N passes T's
defining laws, refutes the law for every model. [mine, (a)] Let P be a law's predicate over the
structures of T's signature. A control is a structure W with ¬P(W): it shows P is not the constant
true, which is a fact about P and holds whatever structure is later run. A pass is P(N) with its
evidence; it is a fact about N. The two cannot serve each other: a pass on M says nothing of P(N),
and a control on W says nothing of P(N) either. That is propositional logic, an exercise.
[literature] FitSpec (Braquehais and Runciman 2016) draws the same line for QuickCheck properties:
the survival of mutants is a property of the property set, the test outcome a property of the
implementation; DeMillo, Lipton and Sayward 1978 define the mutation score as a property of the
tests. [mine] The exception is the contrapositive of soundness: if T ⊢ L then every model of T
satisfies L; N ⊨ T and N ⊭ L give T ⊬ L. It is exact when "N ⊨ T" is exact (proved, exhaustive,
cases at the failing input). With sampled passes N ⊨ T holds at risk δ, so the conclusion "L does
not follow from T" holds at that risk; the record admits the exception under the Boolean slice's
chain, which accepts sampled passes, and that premise (the defining laws' passes exact) is not
enforced. I keep IL1 in (a) and flag the exception's premise.

### 3.2 IL2 and IL3, the unit of control

[record] D-2026-10-25-a question 4, L9.14's last sentences, spec 7.S22 (a control runs every
conjunct and does not stop at the first it refutes). [mine, (a)] If c₁ ∧ c₂ is refuted by W at c₁,
nothing follows about c₂(W); a theory's conjuncts are independent obligations and each needs its
own refuting structure. [literature] FitSpec's kill matrix per property is this. [mine, IL3 (c)]
The completion rule "done when every conjunct has a refuted model" needs every conjunct to be
refutable by some structure of the signature. The audit's controls reports show conjuncts that are
not: `EmptyIsInitial` (no value of `Empty` to break it with), conjuncts fixed by a wrapper's branch
before the model is consulted (`UnknownComposesUnknown`, `NatsOfNothing`;
`audit-algebras-2026-10-22/report-controls-M.md`). What would have to be proved for IL3 to be a law:
a criterion that tells a conjunct that is a consequence of the others or of typing (exempt) from one
that describes nothing (a finding), and that the criterion is decidable on the theories written.
What could make it false: a theory all of whose conjuncts are refutable by easy mutants while the
intended function is not pinned (the critique's f(x) ≥ 0, f(0) = 0 satisfied by the zero function;
L9.4 allows this, so "controlled" cannot mean "characterizes").

### 3.3 IL4, vacuity

[record] spec 7.S12 (n counts evaluated cases; a premise that never held passes vacuously and the
entry says so), L12.7 (`then` is material), bites A3 and A3b (`VacuousIsUnsettled`). [mine, (a)]
Under the sampled distribution μ, the zero-failure bound on P → Q bounds μ(P ∧ ¬Q), the failure set
of the implication, which is at most μ(P). The claim a scientist wants is about Q given P; its
failure fraction is μ(¬Q | P) = μ(P ∧ ¬Q)/μ(P), and the n draws give k = n·μ̂(P) draws from the
conditional distribution, so the bound on it is ε̂(k, δ), not ε̂(n, δ). With k = 0 the conditional
claim has no evidence. This is the binomial computation on the conditional distribution, an
exercise. [literature] Beer, Ben-David, Eisner and Rodeh 2001 define vacuity by subformula
replacement; QuickCheck's `==>` discards the cases where the premise fails and reports the count.
[record] Today `certify.epsilon_hat` reads the region's pooled n; the `held` count is written with
the entry but does not enter ε̂. So the unsettled case is certified and the conditional bound is
not implemented (the comparison-basis report, section 6, proposes it).

### 3.4 IL5, the sampled bound

[record] L10.3, spec 7.S11, `SampledBound` with `SoundAtNoFailure`: (1 − ε̂)^n ≤ δ, the model
`ruleOfThree` = min(1, −ln δ/n). [literature] Hanley and Lippman-Hand 1983 (the rule of three),
Clopper and Pearson 1934 (the exact bound 1 − δ^{1/n}; −ln δ/n is larger, so conservative), both
for n independent Bernoulli trials. [record] The premise is stated as laws of the random source,
`DrawsAreUniform` and `DrawsAreIndependent` (generators.lth, 7.S1), and the foundations report
shows the live sampler is not that source: `scrambled(s) = 1327217884·s mod 2147483647` on
consecutive seeds is a rotation, and a failure set of marginal mass 10% is missed by 100 cases with
probability about 0.87, where 100 independent draws would miss it with probability 0.9^100 ≈
2.7·10⁻⁵; the entry still records ε̂(100, 0.05) = 0.030. [mine] Class (c) by the brief's rule: the
mathematics is (b), the premise is not enforced and is false on a live path. What would have to be
proved: that each generator in use satisfies the independence law, by the statistical test the
record already names (7.S1, `DrawsAreIndependent` as a sequential test), with the generator's
certificate in the entry's cone (L9.10 already says a certifier's certificate enters the cone). A
counterexample to look for after the fix: any generator built by modular multiplication on a
counter.

### 3.5 IL7 and IL8, what the hash forgets and what it keeps

[record] L10.4, spec 6.S8 and 3.S34, D-2026-10-15-e. [mine, IL7 (a)] The verdict of a law is a
function of the reduction of its cone; reduction is invariant under alpha-renaming (Barendregt
1984, chapter 2, the variable convention) and, for this kernel, under erasing the annotations of
`Lam` and `Let`, a lemma stated and certified in Luthier (`ErasureKeepsTheStep`, with the control
that erases a binder's name and so changes the step). Module prefixes and the order of definitions
do not enter reduction. [literature] Unison's hashing of terms with de Bruijn positions; Mokhov,
Mitchell and Peyton Jones 2018 on early cutoff. [mine, IL8 (c)] The converse is completeness: the
identity must include everything the verdict depends on. For the kernel's part it follows from
L4.7 (a definition's result depends only on its inputs), a property of the language. For externs
it is a claim about host code, undecidable in general (Rice 1953) and false today: the foundations
report changed `os.getenv`'s answer under one cone hash, and BLAS threading changes numerical
results under unchanged identities; host hashes omit transitive dependencies. What Luthier has is
a detector: if two runs with equal identity disagree, something outside the identity changed the
result (D-2026-10-15-f), which is the contrapositive of determinism and is sound; it finds
omissions after the fact and does not establish completeness. What would have to be proved: that
the declared bridge of each extern (L11.10: what it reads, what it assumes) covers its inputs, with
reads of the environment, the clock and the random state either in the hash or declared as world
reads on `W`. A counterexample to look for: an extern that reads a global of its host module set by
another extern earlier in the run.

### 3.6 IL6, pooling

[record] D-2026-10-16-g, spec 7.S13, `Pooling`. [mine, (a) given the premise] n₁ independent
draws with no failure followed by n₂ more are n₁ + n₂ independent draws with no failure; the
binomial bound at n₁ + n₂ is the same computation. The objection the related-work report raised
(section 12: optional continuation inflates the risk) does not apply to zero-failure certificates,
by this argument [mine, the critique made the same point]: let p be the true failure fraction. A
false certificate at some total n means no failure through n with ε̂(n, δ) < p; since ε̂ decreases
in n, the first such n is n* = ⌈−ln δ/p⌉, and no failure through any n ≥ n* implies no failure
through n*, whose probability is (1 − p)^{n*} ≤ e^{−p·n*} ≤ δ. So adding stretches until the bound
meets a target keeps the risk at δ, because a single failure refutes exactly and a pass cannot be
undone. This holds for the ln form and for 3/n (3 > −ln 0.05). It fails as soon as failures are
tolerated (k > 0), where confidence sequences (Howard et al. 2021) are the right tool, and it fails
when a stretch is dropped after being seen. [record] What makes IL6 (c) is the other premise: that
stretches under distinct seeds are independent and do not overlap. The foundations report counted
two stretches of 100 cases at seeds 7 and 8 as 200 where the rotation gives 101 distinct positions.
What would have to be proved: that the seed-to-stream map yields disjoint, independent streams
(a property of the generator, certifiable once as in 3.4), and that `pooled` only unions stretches
whose identity shares that generator (already the law `TheUnionIsMonotone`'s scope).

### 3.7 IL9, the capped sum

[record] D-2026-10-25-a question 1, L10.8, `AtLeastTheUnionBound`, `IndependentComposition` under
the axiom `FailuresIndependent`. [mine, (a)] For an input x drawn from the one distribution μ, the
chain fails at x only if some link fails at x, so μ(chain fails) ≤ Σ μ(link i fails) ≤ Σ ε̂_i, and
the event that some bound is wrong is the union of the links' bound-wrong events, of probability at
most Σ δ_i: Boole's inequality twice, capped at 1. No independence is used, which is why it is the
default; the product 1 − Π(1 − ε̂_i) = a + b − ab is smaller and needs independence (L10.8's 0.19
against 0.2). The premise that the links are sampled over one distribution is stated in L10.8 and
6.S12; a downstream link sees the upstream output's distribution, the pushforward, and the record
requires a law relating the two before composing (not written: the hole `entryEvidence`). The
dioid laws asked of a composition (associative, unit on top, `Integral`: combining never knows more
than either part) are the axioms of an integral quantale's tensor (Lawvere 1973), and the capped
sum is the Łukasiewicz tensor on [0, 1], a textbook model. [literature] Younes and Simmons 2006
compose error probabilities the same way in statistical model checking.

### 3.8 IL10 and IL11, transport

[record] L10.7 (with his correction, the weaker grade), L9.9 (exactly where the identity is
Boolean, the distance added where it is a cost), L12.7 (for distances, `then` is the triangle
inequality, which is transport along an identity), spec 6.S11, L6.9 (a link holds only on its
subtype; a proved link carries its theorem's hypotheses). [mine, IL10 (a)] Case 1, a distance
law: B is certified as d(B(x), ref(x)) ≤ b on X, and d(A(x), B(x)) ≤ d′ on Y; then on X ∩ Y,
d(A(x), ref(x)) ≤ b + d′ by the triangle inequality. Case 2, a structural identity A == B on Y:
A(x) = B(x) for x in Y, so every law of B at x holds of A by substitutivity of equality (Leibniz,
spec 4.R8 reserves `==` for structural equality for exactly this reason). The domain is the
conjunction of the two hypotheses, X ∩ Y; the evidence composes by IL9; the grade is the projection
of (domain, cost) and so the weaker. [literature] Mardare, Panangaden and Plotkin 2016 give the
triangle rule as the deduction rule that replaces transitivity for ε-indexed equations; Goguen and
Burstall 1992's satisfaction condition is the exact-identity case along a signature morphism
(L3.4's renaming). [mine, IL11 (c)] Case 3, a Boolean law along a metric identity, is what 6.S11's
wording "bound c ⊕ c′" produces when c = `lift true` = 0: a bound c′ claimed of a law that has no
distance. The critique's counterexample: B(x) = 0.001 and A(x) = −0.001 agree within 0.002 and
"positive" holds of B only. What would have to be proved: a transport rule per law form, with a
margin (the law holds of B with room m ≥ c′ at every point of X ∩ Y, in the law's own metric),
which is Fuzz's sensitivity of the observation (Reed and Pierce 2010) applied to the law as a
function of the specimen. The Boolean slice's `transport` takes any `Standing` and does not look at
the law's value, so today nothing refuses case 3; the cost types that would carry the distance are
the hole. A counterexample to look for in the library once the planner exists: a `LandsIn` law
(the result lies in a subtype) transported along a `Within` identity.

### 3.9 IL12, no evidence for free

[record] L10.9, L10.10, spec 6.S13. [literature, (b)] LCF (Gordon, Milner and Wadsworth 1979): the
type of theorems is abstract and only the inference rules build it, so every theorem has a
derivation; Luthier's `Certificate` is the same device (L10.10 cites it). [mine] The monotonicity
is then an induction on the constructions: certifiers produce an entry with its own domain and cost;
transport intersects domains and adds costs (⊕ monotone, 6.S5); pooling adds cases; pruning only
drops; combination over regions and bindings takes the weaker. Each step is monotone, so no
composite raises a grade, lowers a cost or widens a domain. The induction needs L10.10 to hold in
the language, and today the store is a JSON file that `certify.py` writes and anyone can edit; the
laws are certified on the reference model, the enforcement is not.

### 3.10 IL13, (domain, cost)

[record] L10.2 and L10.5 after D-2026-10-25-a question 2; `Folding`'s `OutsideTheReachHoldsNothing`,
`ReachesAsSets`, `CertifiesOnlyUnderItsBinding`. [mine, (a)] A list of inputs is a finite set X;
P holds on X says nothing of P at y ∉ X without a premise linking y to X (an inductive structure, a
continuity): so a Cases entry serves at y only if y ∈ X. A sampled entry bounds μ(¬P); it serves an
input drawn from μ, in the sense that the failure fraction is bounded, and says nothing at a given
point (L9.16: nothing of null sets). The two are incomparable in the product order (X ⊆ X′, cost ≥
cost′): a sample's domain is "all of μ" with a positive cost, a list's is X with cost 0 on X and ⊤
outside. [record] The Boolean slice admits by the chain Assumed < Sampled < Cases < Exhaustive <
Proved, and L10.5 lists the case this admits wrongly (a Cases entry at an unlisted input) as to be
refused when the cost types come. [mine] A second premise, not enforced: a run at input x is
served by a sampled entry only if x is drawn from μ; a run whose input was chosen because it is
exceptional (the critique, section 4) is outside the bound. The record has the words for it (L6.9,
L9.6) and no mechanism.

### 3.11 IL14 and IL15, the transformer

[record] L9.18, L13.3, L13.4, L6.8, L13.5; D-2026-10-18-j, D-2026-10-25-a question 3; functions.lth.
[literature, IL14 (b)] Higham 2002, §1.5 to 1.6: forward error ≤ condition number × backward error,
the triad the record maps onto (η, L, and the backward form as a third law); §3.1, γ_n = nu/(1 −
nu); Rigal and Gaches 1967 for the backward error of a solve; Rosa (Darulova and Kuncak 2014)
separates the ideal function's sensitivity from the realization's rounding error with a bounded
input domain. The validity region as a premise sampled on both sides is the record's own rule
(D-2026-10-16-j) applied to the theorems' hypotheses (nu < 1, no overflow, δ below a radius).
[mine, IL15 (a)] Let g₁ realize f₁ within t₁ = (L₁, η₁, D₁, r₁) and g₂ realize f₂ within t₂. Take
x ∈ D₁ with f₁(x) ∈ D₂ and x′ with d(x′, x) = δ ≤ r₁. Then
d(g₂(g₁(x′)), f₂(f₁(x))) ≤ d(g₂(g₁(x′)), f₂(g₁(x′))) + d(f₂(g₁(x′)), f₂(f₁(x)))
≤ η₂ + L₂ · d(g₁(x′), f₁(x)) ≤ η₂ + L₂(L₁δ + η₁),
the first term by t₂'s defect at the point g₁(x′) (which needs d(g₁(x′), f₁(x)) ≤ r₂, hence the
radius clause L₁δ + η₁ ≤ r₂, that is δ ≤ (r₂ − η₁)/L₁), the second by L₂ as a Lipschitz bound of f₂
between f₁(x) and g₁(x′) (which needs both in D₂; the record's domain clause takes f₁(x) ∈ D₂ and
the radius covers the other point), the third by t₁. That is (L₂L₁, L₂η₁ + η₂, D₁ ∩ f₁⁻¹(D₂),
min(r₁, (r₂ − η₁)/L₁)). Over two inputs, d(g(x′, y′), f(x, y)) ≤ L_A δ_A + L_B δ_B + η by the same
triangle through (x, y′), the tensor product of Fuzz (Reed and Pierce 2010), and the max is the
cartesian product, a stronger claim that implies the sum. The pull-back δ = (ε − η)/L inverts the
bound; ε < η admits no δ ≥ 0, which is a refusal to certify with this transformer and not a proof
that no realization meets ε (the critique's point: the identity realized exactly admits the
conservative transformer (1, 0.25) and meets 0.125). [literature] Chisel (Misailovic et al. 2014)
allocates ε and δ backward across a DAG by the same first-order bound. [record, the gap] The nine
laws pass on listed dyadic transformers; the critique evaluated the same definitions at 0.1, 0.2,
0.3 and `ComposeAssociative` is false (floating-point products are not associative), and a
pull-back at L = 6.6258…, ε = 3.7680… returns a δ whose forward bound exceeds ε by one ulp. The
mathematics of IL15 is exact; the specimen computes it in Float64 without directed rounding. What
a sound specimen needs is outward rounding of the bounds (Rump 1999; IEEE 754 directed modes), or
`Rational` coefficients where exactness is demanded.

### 3.12 IL16 and IL17, balls and decorations

[record] decisions.md's proposal `RadiusWithinTransformer` (related-work section 3), L5.4, spec
8.S1 and 11.S10. [mine, IL16 (a)] Let the true input x lie in the ball of radius ρ around m, with
m ∈ D and ρ ≤ r, and let the step's transformer t = (L, η, D, r) hold with L a Lipschitz bound of f
on that ball (which is what `Realizes` quantifies: every x′ within r of x). Then d(f(x), g(m)) ≤
d(f(x), f(m)) + d(f(m), g(m)) ≤ Lρ + η, so the ball of radius Lρ + η around g(m) encloses the true
value: the mean-value form of interval evaluation (Moore 1966; Neumaier 1990, Interval Methods for
Systems of Equations, §2.3). Arb propagates radii by bounds of the derivative over the ball
(Johansson 2017). The law is sound exactly because the transformer's L is a bound over the radius
and not a derivative at the midpoint; read as the latter it is false (x² at m = 1, ρ = 0.1: 0.2
against 0.21). Whether Luthier's L is certified as a bound over the whole radius is the test's
business (`Realizes` samples x′), and the comparison-basis report's section 4 already names this
as the first check. Nothing is implemented. [mine, IL17 (c)] L5.4 says a decoration (dual numbers,
intervals, pairs of value and cost) is another model of the theory the code was written over.
For dual numbers it is a theorem: forward-mode differentiation is exact arithmetic in the ring
R[ε]/(ε²) (Griewank and Walther 2008, chapter 3), so the ring laws hold and the derivative is
exact. For intervals the exact laws fail: [−1, 1] − [−1, 1] = [−2, 2], not [0, 0], and x·(1/x) is
not 1, because interval arithmetic takes each occurrence independently. What intervals model is the
enclosure version of every law (Moore's fundamental theorem: the interval extension encloses the
range, inclusion isotonicity), which is the `Within` form with the decoration's own radius as
bound. So L5.4 holds for a decoration P exactly when P is a model of the theory's `Within` version
with a defect P declares, and the certificate at the identity carries over by parametricity
(Wadler 1989, as 8.S1 says) only for laws polymorphic in the type operator G, which excludes the
number laws themselves. What would have to be proved, per decoration: the list of the theory's
laws P satisfies exactly, the list it satisfies within a bound, with the bound. What could make it
false: any exact law used downstream of an interval (a branch on `x == 0` where x is a ball).

### 3.13 IL18 and IL19, the graph and the cutoff

[record] L6.5, L6.6, D-2026-10-11-m, L12.3, spec 5.S7. [literature, IL18 (b)] A relation that is
reflexive and symmetric but not transitive (closeness within ε) is a tolerance relation; its
transitive closure is the whole connected component, which loses the tolerance (Zeeman 1962; the
"physical continuum" of Poincaré). Mardare, Panangaden and Plotkin 2016 build equational logic on
exactly this: s =_ε t has the triangle rule, not transitivity, so there are no equivalence classes
of specimens, only paths with summed distance. [mine, IL19 (a)] If a law carried a tolerance τ, two
specimens each within τ of a third are within 2τ of each other and the composite of two steps each
within τ is within 2τ of the ideal; the only place a tolerance survives composition is at the end,
where the demand reads the composed bound against it. Lowering the cutoff admits a superset
(monotonicity of ≤), certified as `ServesIsMonotoneInTheCutoff`.

### 3.14 IL20, kernel edges

[record] D-2026-10-27-a: the kernel identified by a content hash; each change compared with the
previous kernel by running the test programs under both; the comparison stored as an edge with a
grade and a domain (the programs compared); certificates under H_old served under H_new through it;
later, rule families each with their hash and a cone recording the families it reaches. [mine,
(c)] The law transports a certificate of cone c from H_old to H_new on the strength of an agreement
observed on programs that are not c. For the transport to be sound the kernel's behaviour on c must
be determined by its behaviour on the compared programs, which holds when c reaches only rule
families the comparison exercised and the change touched no other, the "later" part of the decision.
Until the families exist the edge's domain is "the programs compared" and the transported cone is
outside it, so IL20 as stated serves certificates outside the edge's domain, the thing IL10 forbids.
[literature] The sound form is translation validation (Pnueli, Siegel and Singerman 1998): instead of
verifying the new kernel once, check for each cone that transports that the two kernels agree on
it, which costs one comparison per cone and gives an edge whose domain is that cone. Differential
testing (McKeeman 1998) is the sampled version with no domain. A counterexample to look for: a
change to nested `match` that no test program reaches and a user's cone does, served under the new
hash by an edge graded on the test programs. Nothing is implemented: `certify.py` hashes the
interpreter's revision.

### 3.15 IL21, the derivation

[record] L5.22, L5.23, L10.13, L11.10; D-2026-10-22-c (a derivation as a point of an intensional
exponential, the certified identities its 2-cells), D-2026-10-25-a question 5 (a certified relation,
a canonical form at the Boolean level only). [mine] Three parts. The projection and the subtype
are (a): a requirement on the derivation (no `assumed` dependence, descent from a calibrated input)
is a predicate on the realization graph, so L8.5 gives its certified subtype and forgetful
projection; a demand asking for it asks for a type, as for any decoration. [literature]
Proof-carrying data (Chiesa and Tromer 2010) is the same shape with a local compliance predicate per
node, which answers O13's question whether a summary may stand for a discarded ancestry (yes, when
the predicate is inductive). The metric part, no class and only the ball, is IL18. The Boolean
canonical form is where the (c) is: `(a + b) * 1.0` and `a + b` have one derivation because `* 1.0`
is exact on the doubles, a certified identity; a canonical form of realizations modulo certified
exact identities exists when those identities form a confluent, terminating rewrite system
(Knuth-Bendix completion, Baader and Nipkow 1998, chapter 7, and AC-normalization where the
operator is certified associative and commutative, the law-normal-form idea of 2026-10-27). For
observational equivalence of programs in general there is no canonical form (Rice 1953; for
elementary functions, Richardson 1968), so the sentence "a canonical form at the Boolean level"
is true of a fragment and false of the level. What would have to be proved: that the fragment
(the certified exact identities in use) is confluent and terminating, which Knuth-Bendix decides
case by case and can fail. Nothing is implemented beyond the result key.

### 3.16 IL22 to IL25

[record] L5.2, L5.11, L4.7, 8.S3 to 8.S5, 10.S6; L4.9 to L4.11, 10.S7; L11.2, 10.S10; L9.19,
D-2026-10-27-b. [literature, IL22 (b)] Kahn 1974: a network of deterministic processes computes a
unique fixed point whatever the schedule; on a finite DAG of pure nodes it is the trivial case, each
node's value a function of its inputs, every topological order giving the same values, the
Church-Rosser property for free. An acting cone breaks the premise (a node's value depends on the
world), so the memo must not serve it: `ActionConeIsNeverServed`. [mine, IL23 (a)] Barendsen and
Smetsers 1996 give the token; Luthier adds that an action is a function over two observations of
the world, so its law is stated over (before, after) and tested as any law; and own actions are
idempotent, so a second application is observationally equal to the first and may be served from
the store, under the premise that nobody else wrote in between, which L5.20 names and lets the
program refuse (write twice to see whether a third party writes). The roots of trust stay axioms.
[literature, IL24 (b)] Findler and Felleisen 2002 (contracts at module boundaries, blame), Flanagan
2006 (hybrid checking: what is not proved is checked at the boundary); Luthier checks ahead of the
run and refuses, instead of checking per call. The propagation of `assumed` downstream is the
weakest grade along the cone, monotone (IL12). [mine, IL25 (a)] From IL9, the chain's bound is
Σ ε̂_i capped; a proved link has ε̂ = 0, δ = 0; the derivative of the sum with respect to effort is
largest at the largest term. So an established theorem is cited (ε̂ = 0) and the run tests the
specimen, the only term left. The premise: the citation matches the law and its hypotheses hold of
the specimen; 6.R1 records who checked (`human`, `ai+human`, `none`), a trust declaration, and the
critique is right that this is not a proof object. Luthier could tie a `Proved` grade to a
machine-checked artifact by hash (Flocq, Boldo and Melquiond 2011) where one exists.

## 4. Conclusion

How much is an exercise of a book. Seventeen of the twenty-five laws are (a) or (b): once the
objects are typed as the record types them (a law with a domain, a certificate with a domain and a
cost, a numerical step as (L, η, D, r), evidence as (ε̂, δ)), each gluing law is one application
of a standard result: the triangle inequality (IL10, IL15, IL16, IL19), Boole's inequality (IL9,
IL25), the binomial bound (IL4, IL5's formula), the alpha lemma (IL7), Kahn's determinacy (IL22),
LCF's abstract type (IL12), contracts at a boundary (IL24), Higham's triad (IL14), tolerance
relations and the triangle rule (IL18), and propositional logic (IL1, IL2, IL13). That is firm
ground, and it is what D-2026-10-27-b asks: these are cited, not demonstrated again, and Luthier's
tests of them are regressions of its own machinery. [mine] What is not in any book is the
composite: that a demand served by Luthier is served soundly, with the bound and the evidence it
claims, when every link of the route is one of these laws. Each law is routine; the theorem that
their composition along an arbitrary route of certifiers, identities, transformers, decorations,
bridges and kernel versions is sound is not stated anywhere I found. It would read: if the
premises of IL3, IL5, IL6, IL8, IL11, IL17, IL20 and IL21 hold, then for every demand that Luthier
serves, the served value satisfies the demanded law within the composed bound, except with
probability at most the composed δ, on the composed domain. That is Luthier's theorem, and it is of
the kind that Mokhov, Mitchell and Peyton Jones proved for build systems (correctness given the
tracked dependencies) and Chiesa and Tromer for proof-carrying data (compliance given the local
predicate): a statement whose content is the list of premises.

How much is new and needs a proof. The eight (c) laws are where the premises live, and each is
either unenforced today or false on a live path:

- IL5 and IL6, independence and non-overlap of the draws (the sampler violates it);
- IL8, completeness of the identity (externs read what the hash does not see);
- IL11, what an identity transports (a Boolean law along a metric link is not transported);
- IL17, which laws a decoration models (intervals are not a field);
- IL20, the domain of a kernel edge (an edge graded on other programs);
- IL21, the fragment on which a Boolean canonical form exists;
- IL3, which conjuncts can be controlled at all.

Which new laws a paper would rest on. Not the (a) and (b) rows, which a reviewer will recognize,
and not the (c) rows as statements of what Luthier does, since four of them are refuted on the
current code. A paper would rest on the composite theorem above, stated with its premises as
obligations that Luthier discharges by its own laws: the identity's completeness as a declared
bridge (IL8 with L11.10), the sampler's independence as a certified generator in the entry's cone
(IL5, IL6 with L9.10), the transport rule per law form with a margin (IL11), the decoration as a
model of the `Within` version with its defect (IL17), the kernel edge as translation validation per
cone (IL20). Those five are the interaction laws Luthier adds; the rest it borrows. Of the five,
IL11 and IL17 have a proof sketch above that I believe is complete once the premise is in the type;
IL8 cannot be proved for arbitrary hosts and becomes a declared assumption per bridge; IL5, IL6 and
IL20 are mechanisms with a known sound form.

What this touches, for Luciano (one line): the novelty claim of the related-work report's section
15 should move from "the architectural unification" to "the soundness theorem of the pipeline and
the five premises it makes explicit", which is a smaller claim with a proof obligation attached and
survives the critique.

## 5. Decisions taken on my own

- The list of twenty-five laws and their boundaries (where one law ends and the next begins), in
  particular splitting IL10 from IL11, IL2 from IL3, IL7 from IL8, so that the (c) part of each
  pair is named apart from its (a) part.
- The reading of the brief's strictness rule: a law whose stated premise is unenforced is (c)
  (IL5, IL6), while a law whose premise the record states and whose mechanism is simply not yet
  built stays (a) with the gap in the last column (IL9's path hole, IL13's chain).
- The derivation in 3.6 that optional continuation keeps the risk at δ for zero-failure bounds,
  which contradicts related-work.md section 12's objection and agrees with novelty-critique.md
  section 1; it is mine and unreviewed.
- The reading of IL16 as (a) rather than the critique's "unsound": the record's L is the
  transformer's bound over the radius, not a derivative at the midpoint.
- The composite theorem of section 4 as the paper's claim: a proposal, not a decision.
