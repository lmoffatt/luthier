# Analysis of "The principles of Luthier" (Draft 10)

## 1. Redundancies and overlaps

**Certificates and grades are defined in at least five places.**
The Terms define *certificate*, *certify*, and the five grades. L2 re-defines them ("the guarantee is what the certificate says... proved or exhaustive, cases, sampled, assumed") and adds "worst cost seen." L6 defines how grades compose. L7 defines them again in the context of verification methods. L14 adds transport of grades. L10 adds memo-gating on grades. Each new entry re-states the grade vocabulary instead of referencing it. This is the single biggest redundancy in the document.

**L5 and L13 cover the same ground twice.**
Both state: equality has levels; identity is a law; the planner substitutes implementations only along certified equivalences; paths sum distances; sampled links are restricted to their sampled domains; grade is the weakest link. The document acknowledges this ("the composition is his note... what L13 states for the planner's paths"), but acknowledgment is not a solution — one of the two should own the mechanism, the other should own the consequence.

**L4 and L14 both govern holes and externs.**
L4 defines the five hole kinds (input, external, pending, axiom, dead code) and `extern`. L14 then re-explains extern validation, the agreement test, and the world mechanism. The extern story is split across two principles with different emphasis (declaration vs. certification).

**L2 vs. L10 on what a test is.**
L2/G1: "coding and testing are one act; to declare `m : T` is to declare the tests `m` will pass." L10: "The tests are actions, so verifying is demanding." These can be reconciled (elaboration-time law-checking vs. runtime `test` action; two caches, which L10 itself notes), but as written a reader sees "testing is free" in one principle and "testing is an action you pay for" in another, three sections later.

**Terms section duplicates body content.**
*Demand*, *planner*, *certificate*, *evaluation/execution* are each re-explained in G3, L10, L11. The Terms should be pure definitions; several are miniature essays.

**L12 is nearly content-free as a standalone principle.**
One sentence ("no hardcoded constants") plus the root-tolerance note, which is really part of L10's demand story. It could be a clause of L10/G3 rather than a principle.

## 2. Contradictions and tensions

**L5 vs. L13 on composing distances (real contradiction).**
L5: identity "composes as HoTT composes paths... under cost the composed path costs the sum of its links and holds at the weakest of their grades" — stated unconditionally, with only the domain-intersection caveat.
L13: a sampled edge is "admissible only on inputs the distribution it sampled covers, and only as a direct edge, never summed into a path, until a probabilistic bound exists as a law."
These are incompatible: L5 licenses summing any links; L13 forbids summing sampled links. L5 must inherit L13's restriction, or the two principles will implement different planners.

**`within ε` has no consistent home.**
L6 says the cutoff "lives only in the demand, since it does not compose." But L3 says the certified constructor *takes the tolerance as a parameter*; L13 says "the tolerance charged at a node is the demand's pulled back through the sensitivity of the cone." Is the tolerance a demand-only object, a constructor parameter, or a per-node computed quantity? All three are asserted in different places. The pullback in L13 may resolve this (constructor/demand carry ε; nodes carry derived bounds — a different object from `within`), but the document never says so, and `within` itself is defined only by its non-composability.

**G0 vs. L13 on who ranks candidates.**
G0: "cost or execution time ranks the candidates (G2)." L13 (not G2) is the principle that ranks candidates, and G2 is about the cost logic, not ranking. Cross-reference error.

**Terms vs. L11 on "execution."**
Terms: "Execution is an action on the world (print, save)"; writing a certificate into Luthier's store is "an action on Luthier's own state." L11: "an action changes the state of the world... an effect on state Luthier owns is verified this way, an irreversible or concurrent effect outside it is typed, logged and audited, never verified." So there are actions on the world, actions on owned state, and typed-but-unverifiable actions — three categories asserted in two different terms. Luthier-own-state actions sit awkwardly between "execution" and "evaluation," and L9's "no effects, only actions" doesn't cleanly place them either.

**L10's identity vs. L10's own memo.**
"A result is identified by code, inputs, mode, demanded type and tolerance, model, seed, plan, certificate hashes..." — but "the run database is what the planner reads... and is not an input of the result once the plan is fixed." This is fine, but the same paragraph also says the runtime includes thread count and scheduling, and then that an extern whose bits depend on scheduling "is not bit-identical to itself." The identity spec implicitly excludes some sources of variation while including others; the criterion (which variations are part of identity vs. part of the cost model) is never stated. A one-sentence rule would fix it.

**Intro promises a format the body doesn't follow.**
"Each entry gives its statement, its formulation, what it derives from, and its status." The body has no labeled statement/formulation fields; derivations and statuses are woven into long paragraphs, inconsistently.

## 3. Missing principles (or missing status)

- **A principle of determinism/reproducibility at the level of L9.** L9 asserts confluence and "result depends only on inputs"; L10 handles the rest (seed, plan, scheduling). But nothing states the normative claim that *given the same identity, a run reproduces the result up to its identity law's distance* — the guarantee a user actually relies on. It's derivable from L9+L10 but is important enough to be stated once, cleanly.
- **The status of the `Cost` algebra.** G2 is "settled" as an eureka but its algebra is open (`11`), and L6 (the new combining principle) is "proposed." Yet L2, L8, L13 already build on cost-composition machinery (worst cost seen, summed links, pullback). Several principles silently depend on an unsettled foundation. The document would benefit from an explicit dependency-of-principles-on-open-items map.
- **What happens when a demanded grade cannot be met.** L10 says the memo serves only cones meeting the demanded grade, and L14 has the `assumed` opt-out. But there is no principle stating the failure mode: demand → no certificate at grade → what? Error? Escalation? Relaxation by the demander? This is a core executive-face question and currently distributed across three principles.
- **No principle covers naming/scope beyond L9's block rule.** Possibly fine, but `<-` vs `:=` is doing a lot of semantic work (L5's binding law, L9's freshness) and is only defined in the Rules of the spec (`05` R8/R12) — worth one sentence in the Terms.

## 4. Can the number of principles be reduced?

Yes — from 15 to about 10, without losing content:

| Current | Proposal |
|---|---|
| L1 | Keep, or demote to preamble (it's a motivation, not a rule) |
| L2 + L7 | **One "Certification" principle**: membership guarantee, grades, verification methods, identity-vs-law distinction |
| L3 | Keep |
| L4 + L14 | **One "The open boundary" principle**: holes, externs, worlds, delegation, transport |
| L5 + L13 | **One "Equivalence and substitution" principle**: equality levels, composition of identities, the planner's weighted graph |
| L6 | Keep (short; it's the G2 workhorse) |
| L8 | Keep |
| L9 + L11 | **One "Pure evaluation, verified action" principle** (L11 is two sentences; it is a corollary of L9 plus the world observation rule) |
| L10 + L12 | **One "The demand" principle** (L12 folds in as "every criterion the demand carries is a parameter") |
| L15 | Keep |

That leaves: preamble, Certification, Certified subtype, Open boundary, Equivalence/substitution, Laws combine, Ideal/realized, Pure evaluation & action, The demand, Core minimal. Ten principles plus the four organizers is a cleaner load-bearing structure — each principle then has exactly one question it answers.

A second, deeper reduction: **split content, not just merge.** L10 and L13 are each doing 3–4 principles' worth of work (400–600 words each, with memo identity, planning strategy, decorated outputs, and session semantics all in L10). Splitting each into "planning," "identity/memo," and "decorated outputs" would *increase* the count but make each principle testable. I would merge the certificate cluster and the equality cluster first, then split L10 and L13. Net: same or fewer principles, each single-purpose.

## 5. Advice for a better document

1. **Separate the normative text from the provenance.** Right now every entry mixes the principle, its derivation, its negotiation history, and its status in one paragraph. For the agent building the spec this is fatiguing and error-prone. Two layers: (a) the principles, clean, each under ~150 words, one claim per sentence, with labeled fields — *Statement / Formulation / Derives from / Status* (the intro already promises this format); (b) a commentary appendix holding the "his note of 2026-10-12," "the model's correction," draft history, and old-number mappings.

2. **Split the mega-paragraphs into numbered clauses.** L10, L13, and L14 are each one paragraph of 15–25 sentences. Number the clauses (L10.1, L10.2, ...) so the spec can reference, implement, and test them individually. This also exposes redundancy mechanically.

3. **Fix the grade vocabulary once, in Terms, and reference it.** "proved, exhaustive, cases, sampled, assumed" should be defined in exactly one place, including how grades compose (currently split between L2, L6, L7, L14).

4. **Resolve the L5/L13 contradiction explicitly** — decide whether summing sampled distances is ever licensed, and state the rule in exactly one principle, with the other referencing it.

5. **Give every open item exactly one home.** Statuses like "proposed," "candidate," "his mark pending" appear in body text, in Status paragraphs, and again in "What is open" (which itself duplicates the statuses of L6, L8, L14). Consolidate: one register of open items, each with the principle it blocks.

6. **Make settled vs. proposed visually unambiguous.** A reader should be able to tell in one glance whether a sentence is normative. Currently "proposed" is sometimes mid-paragraph, sometimes in the Status line, and L14 has two different status sentences in one entry ("settled by his correction... proposed, candidate").

7. **Add a dependency diagram.** G0→G2→L6→L8/L13, G3→L10, L2/L7→L14, etc. This would immediately show that four "settled" principles rest on G2's open algebra, and would help decide the reduction in (4) above.

8. **The old→new numbering map deserves a visible table.** The parenthetical "(was L16, L21)" is fine for one release, but as the record lags the draft ("the record keeps the old tags until it is updated"), a single mapping table at the top prevents mis-citation across documents.

The draft is substantively strong — the hard problems (transport, sampled edges, memo identity, graded guarantees) are all *faced*, which is rare. The main risks are structural: contradictions hiding inside very long paragraphs, one mechanism specified in two places, and status/provenance noise obscuring what is actually settled.


does separation of G0-G3 do any good or it would be better to just list the Ls?

Short answer: the separation does good, but only if the Gs are given a strictly different job from the Ls. Right now they are half worldview, half principle, and that halfway state is the source of real damage.

## What the Gs do that the Ls don't

The four organizers are the only place the document answers *why*:

- G0: type theory is the guide — but normalization of a given term vs. search for an inhabitant is Luthier's departure.
- G1: types carry semantic weight; "coding and testing are one act."
- G2: one logic extended to the non-negative reals — the intellectual core of the whole cost apparatus.
- G3: programs need an executive face; computation is driven from outside.

None of these is a rule an implementer can check. They are commitments — the fixed points the Ls are derived from. That's a legitimate layer: it tells a new reader (or the spec-writing agent) which ideas are load-bearing before encountering fifteen rules. Strip the Gs and the Ls become a list whose unifying ideas must be reverse-engineered.

## What the Gs do that the Ls already do (the problem)

Each G is currently a mechanism disguised as a eureka, and in each case an L restates the mechanism, better:

| Organizer | Restated, more precisely, by |
|---|---|
| G1 ("a type is a theory, its values are models") | L2 (membership is a guarantee) |
| G2 (laws valued in cost; lift, exact, within) | L6 (laws combine, predicate lifts to cost) — the lift/exact/within material is *admitted* to be copied from G2 |
| G3 (demand defines what is computed) | L10 (demand determines computation, decorated types, memo) |

G0's content overlaps L15 (the kernel, hand executability) and the Terms. So no L depends on its G for anything not stated in the L itself — the Gs are, empirically, motivational. And the document knows the boundary is unstable: G3's own status asks whether it is "an eureka of its own or the executive clause of the guide (G0)"; G2's extension is parked as "the third eureka or a principle of good use." These disputes exist because the category *eureka* has no job description.

The double layer has also already cost you mechanically: the 2026-10-12 renumbering (G1↔G2↔G3 swapped) desynchronized the record, decisions.md, and every cross-reference, which is exactly the maintenance burden a redundant tier creates. Note also G0's cross-reference bug from the previous analysis ("cost ranks the candidates (G2)" — that's L13's job), which happens because content lives in two tiers and references drift.

## Recommendation

Keep the separation, but make it honest. Two options, both defensible:

**Option A — strict division of labor (my preference).** Gs become "The four commitments": each ≤ 5 sentences, purely declarative, no mechanisms, no lift/exact/within, no memo, no statuses longer than the statement. One line each: *derives into L2, L6, L10.* All mechanisms live only in the Ls. This preserves the roadmap for readers while eliminating the double maintenance.

**Option B — collapse.** G1 folds into L2, G2 into L6, G3 into L10 (each gains a one-sentence "commitment" preface); G0 and the Terms become a short preamble. Fifteen Ls plus preamble, one tier. This is cleaner if the document's real audience is the spec-building agent, which doesn't need motivation, only rules.

What is not defensible is the current halfway state, where G2 carries normative content (the lift/exact/within definitions, quoted verbatim into L6) and G3 carries L10's thesis — because then every edit must be made twice, the numbering is fragile, and "settled" statuses attach to pairs of statements that can drift apart (which is precisely what the "record keeps the old tags" note is already confessing).

One test to apply, going forward, whenever a new idea arrives: *can an implementer violate it?* If yes, it's an L. If no — it's a commitment, and it belongs in the G layer with no mechanism attached.