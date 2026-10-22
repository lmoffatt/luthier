# The algebra audit: what is yours to decide

2026-10-23, Claude Fable 5.1, on `record/plan/after-core-2026-10-23/prompt-audit-synthesis.md`
(e3f5cad). Inputs: the audit `report.md` (Codex, 5b1a05e), `record/principles-language.md`,
`record/decisions.md` from D-2026-10-16 on, `docs/concepts.md` 6 to 15, the tree at e3f5cad. "Audit"
marks what is the audit's, "record" what the record settles; the recommendations are mine. The
execution is in `execution.md` beside this file.

**Done.** The audit's five concrete findings (a refutation erased by retention, `byModel` skipping
the vetoes, a run recording fewer certificates than served it, distribution budgets outside the
identity, the reader accepting what `Store` forbids) were fixed in bite 13c (820f0e3 to 59da028) and
stated in certification.lth as `Routing` and `Pruning` (4f24573 to 46da7ee); D-2026-10-22-a and -d
fixed what a pass and a failure are about. Of its conceptual part the record already settles: grades
combine across conjuncts by the demand's choice, weakest by default (D-2026-10-16-i, spec 5.S8);
across seeds by pooling (D-2026-10-16-g); a control is about the law (D-2026-10-22-a); no law is
valued in a cost, the law's form says the level (D-2026-10-18-i); the error base's orientation
(bite 6's correction); a numerical law's two bounds (D-2026-10-18-j); every policy is recorded, so
run.py's unrecorded `axioms` and `combine` are a session's fix (L5.18); a projection erases nothing
(L5.23). The rest is twenty bites in execution.md. Five things only you can answer, in the order of
what they unblock.

**1. The evidence base: which tensor, which orientation.** The record holds two compositions for
sampled links on one distribution: the failure fractions summed, the union bound (D-2026-10-12-q;
L10.8, links sampled over the same distribution compose by the union bound), and the evidence cost
in nats, −log(1 − ε̂), summed as a distance is (D-2026-10-12-q; L10.3), with ε̂ the bound on the
fraction of the distribution where the law fails after n cases at confidence 1 − δ. The audit (4.2)
shows they differ: summing nats multiplies success bounds, which needs the two failures
independent; two links at ε̂ = 0.1 give 0.2 by the union bound and 0.19 by nats. And D-2026-10-18-i's
table orders evidence by ≤, where the tensor does not preserve the empty join, the defect bite 6
corrected on the error base. Question: is the evidence base the pair (ε̂, δ) under the capped sum
min(1, a + b) (the Łukasiewicz t-norm) in Lawvere's orientation ≥, the sum in nats kept only under
a declared independence premise? Implies: the union bound is L10.8's first instance, the nats
conversion a map out of the base; δ composes the same way; no entry changes, since ε̂ is computed
when served at the demand's δ (L10.3). Costs: a sentence in L10.3, L10.8 and L6.15; bites B1, B2.
Recommendation: yes; it is the bound that needs no assumption, the simplest sound one first.

**2. The order of grades: a chain, or domain and cost.** test.lth's chain `Assumed < Sampled < Cases
< Exhaustive < Proved` is the Boolean slice's stand-in for the evidence cost (D-2026-10-16-k). L10.2
(the grade is derived from the domain and the evidence cost: cases cost 0 on the cases listed and ∞
outside, sampled a finite cost on its distribution), yours to mark, makes Cases and Sampled
incomparable: three listed inputs say nothing at a fourth, where a sample says ε̂. Question: when
the cost types come, is a certificate's strength the pair (domain, cost), ordered by inclusion and
by cost, the five names a projection for the reader, so that a `Cases` certificate serves a run
only at an input it lists, as L6.9 (a link certified on a subtype is a link only at inputs in it)
says of links? Implies: Proved, Exhaustive and Cases are one kind, exact on a stated domain,
differing in the domain and the hypotheses; a run on real data is served by sampled, proved or
exhaustive evidence, since its inputs are rarely listed; the chain stays the Boolean slice's
admission until L10.5 (a certificate serves every demand whose cutoff it meets) is unsuspended.
Costs: B3 now (nothing served differently); B4 with the cost types (a run served today by a
`Cases` entry at an unlisted input is refused; listed before it changes). Recommendation: yes; it
is what L10.2 says, and the chain lets three listed points certify a run at a fourth.

**3. A numerical law as an affine bound transformer.** D-2026-10-18-j gives its content:
ε_out ≤ L·δ_in + η, L the sensitivity, η the algorithm's own error, on a domain D and below a
radius r. The audit (5) asks how it composes and what it does with several inputs; L13.3 and L13.4
(rounding is non-expansive plus an additive defect; the cost algebra needs a multiplicative and an
additive part) wait for your mark. Question: is the carrier (L, η, D, r), composed along a cone by
(L₂L₁, L₂η₁ + η₂, D₁ ∩ f₁⁻¹(D₂), min(r₁, (r₂ − η₁)/L₁)), and on several inputs by the sum
ε ≤ Σᵢ Lᵢ δᵢ + η, the max where a law names it? Implies: L13.3 and L13.4 settle in this form, the
defect in the maps of the error level and outside the quantale's tensor; L6.8's pull-back is
δ = (ε − η)/L, ε below η infeasible (L13.5), an unknown L no substitution (L6.8); the backward
allocation among inputs is under-determined and the demand's weight decides (L6.2). Costs: C1 (the
`Within` form, the ratio recorded, the transformer in the core) with the re-certification of every
agreement law; C2 after it. Recommendation: yes; it is the first-order bound every theorem of
Higham and LAPACK states, and the sum is Fuzz's product.

**4. A control per conjunct.** L9.14 (a law is evidence of nothing until a wrong model refutes it;
a theory is done when each law has its refuted model) predates D-2026-10-18-f, which split a
conjunction into conjuncts, each with its own entry (spec 7.S22). A control stops at the first
conjunct it refutes (audit 1.7): a broken monoid refuted at `Associative` leaves `Neutral`
uncontrolled, and the law reads "controlled". Question: is the unit of control the conjunct, so a
theory is done when each conjunct has a refuted model and `check -v` lists uncontrolled conjuncts?
Implies: a control runs every conjunct; more laws show as uncontrolled; a fault family as the index
(the audit's proposal) waits for a case (P8). Costs: D1; control lines run past their first
refutation. Recommendation: yes; the conjunct is the law that has the entry.

**5. The derivation's quotient as a relation, never a canonical form.** D-2026-10-22-c reads a
derivation as a point of an intensional exponential carried modulo the demand's equality of
consequence; O13 asks how that quotient is computed. The audit (10.2, 10.3) shows the result key
cannot be it: `(a + b) * 1.0` and `a + b` have different keys and one derivation where no law
separates them; and at the metric level closeness is not transitive (your correction to
D-2026-10-18-c), so there is no class, only the ball (L6.5). Question: is the equality of
consequence a certified relation between two realizations, a law over derivations computed when a
demand asks (L5.23), the result key the identity of the realization, a canonical form only at the
Boolean level? Implies: L5.22's "the key is the identity of the derivation" reads "of the
realization"; the derivation is the realization graph and its projections are laws (E1); the
2-cells are the planner's identities, so composition across hosts comes with it (D-2026-10-13-ad).
Costs: a sentence in L5.22 and O13; E1 after the planner. Recommendation: yes.

Not yours: the resources base (D-2026-10-18-i's "tropical semiring": work adds in sequence and in
parallel, span adds in sequence and takes the max in parallel, peak memory the other way round, so
resources are a typed vector and no one semiring) goes into the record as the coordinator's
correction, as bite 6's on the error base did; say so if you want it as a question.
