Short answer: the draft is rich but over-coupled. Most redundancy is around **identity/certification/planner substitution** (L5, L7, L13, L14), and most contradictions are scope clashes (“every value” vs “only what reaches output”, “sampled edge may compose” vs “never summed into a path”). You can reduce 15 L to roughly 10 without losing concepts, but you should first freeze IDs and separate normative text from rationale/history/open questions.

## 1. Redundant or overlapping principles

**Clear overlaps**

- **G0 + G3 + L10 + L12**: all say the demand fixes what is computed/produced and that criteria are parameters. L12 is almost a corollary of G3/L10.
- **G1 + L2 + L3**: “type is theory, value is model”, membership as guarantee, certified subtype. G1 is the slogan; L2/L3 are the mechanism. Keep one principle plus one construction rule.
- **G2 + L6 + L8**: cost-valued laws, composition of costs, rounding/realization. L6 is the algebra of G2; L8 is an application of G2/L13.
- **L5 + L7 + L13 + L14**: identity equality, certificate of identity vs law, planner substitution along certified equivalence, transport along identity. This cluster repeats the same machinery.
- **L9 + L11**: pure DAG/program vs actions/effects. They are two halves of one topic: programs, execution, actions, world state.
- **L10 + L12**: demand determines computation; no hardcoded constants. L12 should be folded into demand/parameters.
- **Terms + principles**: terms define structure, law, theory, model, certificate, demand, planner; then principles restate them. Terms should be a glossary, not a parallel exposition.

**Less obvious overlap**

- **L4 and L14**: holes, axioms, externs, “no laws at all”, worlds. Both talk about what is not yet a normal certified value.
- **L15 and L4/L9**: kernel, hand execution, programs as data. L15 is mostly architectural; it could be a section rather than a principle.

**Recommendation:** keep the *concepts* but remove repeated statements. Cross-reference: “identity and transport: see L5/L7”; do not restate the weighted graph in both L5 and L13.

## 2. Missing principles or under-specified areas

The document has no clear principle for:

1. **Partiality, failure, absence**  
   `Maybe` appears in L3, but there is no principle saying how failure/absence is typed, propagated, certified, or distinguished from `assumed` holes.

2. **Termination, totality, resource bounds**  
   L13 ranks time/memory, L12 mentions budgets, but there is no principle on termination, productivity, or “total vs partial” definitions.

3. **Concurrency and scheduling**  
   L10 mentions thread count and scheduling; L11 says concurrent effects outside Luthier are audited, never verified. That is not yet a principle. Missing: “parallel evaluation preserves meaning” or “scheduling is an input to identity only for externs”.

4. **Security / trust boundaries**  
   L14 has worlds, host libraries, platform, versions. Missing: sandboxing, untrusted externs, capability limits.

5. **Reproducibility / provenance**  
   L10 has hashes, plans, seeds, versions; L14 has host version/platform. But no standalone principle: “a result is reproducible only with its provenance”.

6. **Serialization / persistence / migration**  
   The store, memo, run database, certificates by hash are central, but there is no principle on what is persisted, how it is migrated, or how stale certificates are invalidated.

7. **Modules / namespaces / imports**  
   L4 mentions theoretical modules and holes, but there is no principle on module boundaries, imports, name resolution, or dependency cycles beyond the DAG.

8. **Units and dimensions**  
   It is already listed as an open candidate L under G0. If units are core to disciplines, they probably belong in the principles, not only in “What is open”.

## 3. Contradictions and tensions

These are the main ones I would resolve before approval.

1. **L13: quotient/class vs weighted graph**  
   L13 says implementations are “the quotient … one class per mathematical function”, then says they “form a weighted graph, not a class”.  
   **Resolution:** exact identity (`Bool`) gives a class/quotient; approximate identity (`Cost`) gives a graph/relation, not a quotient. Do not call both “class”.

2. **L5 vs L13 on sampled edges**  
   L5: a sampled link holds on its sampled inputs, so composition holds on the intersection of certified domains.  
   L13: a sampled edge is admissible “only as a direct edge, never summed into a path, until a probabilistic bound exists as a law”.  
   **Resolution:** decide whether sampled edges may compose on intersection without a probabilistic bound. If not, amend L5. If yes, amend L13.

3. **L14 “every value” vs L10 “what never reaches an output”**  
   L14: certification is default for every value in the dependency cone.  
   L10: what never reaches an output needs no certificate.  
   **Resolution:** say “every demanded/output-reaching value” or “every value whose certificate is demanded”.

4. **L12 “no hardcoded constants” vs kernel/defaults**  
   L12 says every criterion is a parameter. But the kernel has `0`, `∞`, `lift`, `exact`, default plan behavior, default tolerance, etc.  
   **Resolution:** narrow to “no unrecorded policy constants”; exclude kernel primitives and mathematical constants.

5. **L8 functor vs additive defect**  
   L8 says rounding is a functor in Lawvere’s sense, then the correction says it is non-expansive only up to an additive defect, with no multiplicative constant.  
   **Resolution:** define exactly what “functor” means here. In standard Lawvere metric spaces, a functor is usually non-expansive; an additive defect is not the same. Either weaken “functor” or change the metric structure.

6. **L14 “no laws at all” vs worlds with assumed certificates**  
   L14 says a function with no laws at all is not a function to run. It also says an extern with no law yet is allowed inside a named world, with `assumed` certificates.  
   **Resolution:** distinguish “no law at all” from “law temporarily assumed inside a world”; or say world functions never enter the planner graph and are only audited actions.

7. **L9 “without effects” vs “its one effect is on the program”**  
   L9 says a program is a DAG of definitions without effects, then says its one effect is on the program: taking its name once.  
   **Resolution:** say “no effects on the world; binding has an effect on the definition map”.

8. **G1 “declare m:T declares tests” vs L2/L4 assumed holes**  
   G1 says to declare `m : T` is to declare the tests `m` will pass. L2/L4 allow `assumed` certificates and axioms that do not inhabit.  
   **Resolution:** say “declares the tests it claims/certifies at the stated grade”.

9. **Grade composition is inconsistent across L6, L7, L14**  
   L6 says with `&` take weakest; with sum of costs, costs summed, each at its grade. L7 says sampled grade depends on distribution, not just count. L14 says transport takes the weaker of two grades on the intersection.  
   **Resolution:** write one grade algebra: lattice, product, transport rule, sampled-domain rule.

## 4. Can we reduce the number of principles?

Yes. A workable reduction is from **G0–G3 + L1–L15** to roughly **10 normative principles**:

1. **G0/G3 merged**: Type theory guides; demand executes.  
2. **G1**: Type is theory; value is model.  
3. **G2/L6**: Laws are cost-valued; predicates lift to costs; composition rules.  
4. **L1**: Language expresses disciplinary invariances.  
5. **L2/L3/L4 merged**: Types, laws, certified subtypes, declarations, holes.  
6. **L5/L7 merged**: Equality, identity, verification, certificates, transport.  
7. **L8 folded into G2/L6**: Ideal/concrete realization and rounding.  
8. **L9/L11 merged**: Programs, actions, effects, world state.  
9. **L10/L12 merged**: Demand, parameters, memo, produced types.  
10. **L13**: Implementations and planner choice.  
11. **L14**: Externs, worlds, delegation.  
12. **L15**: Minimal core, hand execution, programs as data.

You could go further by folding L8 into G2 and L15 into an architecture section, reaching about **9–10 principles**. But do not merge L5/L7/L13 into one giant entry; they contain distinct mechanisms. Merge their *statements*, not their concepts.

## 5. Advice for a better document

1. **Freeze IDs.** Renumbering G and L creates record mismatch. Use stable IDs like `P-TYPE`, `P-COST`, `P-DEMAND`; keep old numbers only as aliases.

2. **Separate normative principles from rationale.** Each principle should have: Statement, Formulation, Consequences, Status, Open questions. Move history, quotes, drafts, and his notes to `record/`.

3. **One status per entry.** Right now an entry can be “settled”, “proposed”, “candidate”, “pending”, “open”. Use a controlled vocabulary and put unresolved items in “What is open”.

4. **Use cross-references, not restatements.** L5/L7/L13/L14 repeat identity, transport, sampled edges, grades. State each mechanism once.

5. **Make contradictions explicit.** Add a table: “Tension, locations, decision needed, owner”. Resolve sampled-edge composition, quotient vs graph, every-value vs output-value, functor vs additive defect.

6. **Add missing principles or mark non-goals.** Decide whether partiality, termination, concurrency, security, reproducibility, and units are principles or explicitly out of scope.

7. **Clarify scope words.** “Every value”, “no hardcoded constants”, “without effects”, “function to run” are too absolute. Qualify them.

8. **Keep examples in appendices.** The principles should be short enough for the agent building the spec to use directly.

9. **Provide a decision log link per open item.** Many open items already reference D-2026-10-11-*; make that machine-checkable.

10. **Let the record own history.** The principles file should be the projection; if it is currently “unapproved” and the record is not updated, that mismatch should be resolved before further renumbering.


does separation of G0-G3 do any good or it would be better to just list the Ls?

Short answer: **G0–G3 do some good only as a short, non-normative orientation. They should not be a second parallel list of principles with statuses, renumbering and open questions. For the agent building the spec, list the Ls. Keep the Gs, if at all, as a preface or move them to the record.**

## Why the separation currently helps

- **It gives the big picture before the details.** G0 says type theory guides; G1 says types are theories; G2 says laws are cost-valued; G3 says the demand executes. That is a useful narrative for a human reader.
- **It preserves the “eurekas.”** G2 especially is a historical/decision moment. That has value in `record/`, not necessarily in the normative principles.
- **It groups the Ls.** The guide, the declarative face, the cost logic, the executive face. But the Ls already have six topics that do this grouping.

## Why the separation currently hurts

- **G1–G3 are already decomposed into Ls.**
  - G1 = L2 + L3.
  - G2 = L6 + L8 (and parts of L13).
  - G3 = L10 + L12.
  - G0 is mostly L1 + L2 + L10 as a stance.
- **Two lists create two authorities.** If G2 says “laws are valued in cost” and L6 says how they compose, which one wins if they drift?
- **Status confusion.** The G entries have `settled`, `proposed`, `open`. Are they principles? Organizers? Decisions? The Ls also have statuses. That is a maintenance problem.
- **Renumbering overhead.** You already renumbered G1/G2/G3 and kept old tags in the record. That is exactly the kind of cost a normative list should avoid.
- **The spec agent needs one list.** An agent building the specification wants stable, actionable entries. Two parallel numbering schemes are a distraction.

## Recommendation

**Keep a short “Orientation” section at the top, with no G numbers and no statuses.** Three or four paragraphs:

1. Type theory is the guide.
2. A type is a theory; its values are models.
3. Laws are valued in cost, extending logic to the non-negative reals.
4. The demand defines what is computed and which decorated types are produced.

Then go straight to **L1–L15** as the normative principles. The six topic headings already organize them. Cross-reference the orientation where useful, but do not repeat the rules.

If you want to keep the G labels for history, move them to `record/` or `docs/rationale/`. Do not keep them as equal-status principles in `principles.md`.

## So: just list the Ls?

- **For the spec agent: yes.** The Ls are the implementable principles. G1–G3 are redundant with them.
- **For the human reader: no.** Keep a one-page orientation so the Ls do not appear as a disconnected list.
- **For the record: keep the Gs.** They document the eurekas and the renumbering history.

The cleanest structure is:

1. **Orientation** (non-normative, short, no numbers or statuses)
2. **Principles L1–L15** (normative, stable IDs)
3. **What is open**
4. **Record/history** elsewhere

That gives you the benefit of the Gs without the cost of maintaining two competing principle sets.