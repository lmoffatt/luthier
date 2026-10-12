I'll start by reading the uploaded file.

The document is in good shape for a draft 10 — the ideas are coherent and the hard distinctions (identity vs. law, class vs. weighted graph, grade vs. runnability) are already there. The problem isn't the count. It's that four or five rules are each stated three times in different notation, the certificate (the object every L leans on) has no principle of its own, and three entries hold half the text: L10 alone is ~880 words, a fifth of all the L prose, and contains about six principles.

## Redundancies

1. **Certification transports along identity** — stated three times: L5 (composed path: sum of costs, weakest grade, intersection of domains), L13 (paths in the weighted graph: summed distance, weakest grade, "a path exists at x only where every link does"), L14 ("A is certified at the weaker of g and h on X ∩ Y"). One rule, three notations.
2. **The demand** — G0 (execution is the search for an inhabitant), G3 (title), L10 (title). G3 and L10 are the same statement at two levels; G3's own status already asks whether it is just the executive clause of G0.
3. **G1 and L2** say the same thing ("to declare `m : T` is to declare the tests `m` will pass" / "membership is a guarantee"). L2 adds only the grade list.
4. **Decisions cited as content rather than referenced**: D-2026-10-11-n (certification by default, `test` demands certificates without values) is written out in L2, L10, L14 and the open list, five times; D-2026-10-11-m (substitution only along a certified equivalence) in L5 twice, L13, L14; D-2026-10-11-i (binding acts, session as block) in L5 via R12, L9 twice, L10, the open list. The grade list appears in full in Terms, L2 and L7.
5. **Inside single entries**: L9 says "a mutable parameter is two variables" twice; L14 says "an extern is validated against its laws before it is applied" twice and "proved by citation" twice; L10 says "program kept, computation redone" three ways (three objects; synthesis vs. expansion; "always kept, only what leaves scope is lost").
6. **The "what type theory lacks" refrain** in G1 and G3, while G0 already states the contrast ("where type theory normalizes a given term, Luthier searches for one").

## Contradictions

Real ones, in order of consequence:

1. **May a sampled link be part of a composed path?** L5: yes — a sampled link "holds only on the inputs its samples cover, so the composition holds on the intersection of the domains". L14: yes — transport at the weaker of g and h on X ∩ Y, with no restriction on h. L13: no — a sampled edge is admissible "only as a direct edge, never summed into a path, until a probabilistic bound exists". L13 even disagrees with itself one sentence earlier ("otherwise an estimate with the weakest grade and the samples it was seen on"). This is the one an agent building the planner will hit first.
2. **The grade of a sum.** L6: a sum of costs holds "each at its grade" (a vector). L13: a summed path holds "at the weakest grade" (a scalar). The open item "the grade as a lattice" is where this gets decided; until then the two Ls contradict.
3. **Where the cutoff lives.** L6: `within ε` "lives only in the demand, since it does not compose". L3: the certified-subtype constructor "takes the tolerance as a parameter", i.e. applies the cutoff. The Boolean interim puts `d(f x, g x) ≤ tol` inside laws. Either the constructor is only ever invoked from a demand (say so), or L6's "only" is false.
4. **Actions and the memo.** Terms and L10: `test` is an action; L10: a test is memoized by its certificate's identity. Open list: "the world as an opaque, unique value so that an action is never served from the memo". So actions are never memoized, except the one that is. Terms gestures at the fix (action on the world vs. action on Luthier's own state) but no principle states that the second kind is idempotent and memoizable.
5. **Free representative vs. no lone replacement.** G0: "inside the class the representative is free". L13: on a carrier with a distance there is no class, only a weighted graph, "a lone implementation is never replaced", the planner chooses only among what has been compared. L13 also keeps the quotient paragraph ("the class is chosen by law, the representative by cost") two sentences before saying closeness is not transitive, so it is not a class. G0 should say "free in the theory; in a model with a distance, free only along certified paths", and L13 should keep the quotient for the decidable regime only.
6. **"Type" has two meanings.** Terms: a structure is a type in the kernel's language; a theory is a structure *with its law*. G1: "a type is a theory". L2 confirms the two levels ("structural and decidable for the kernel's types"). Pick one: kernel types are structures, Luthier types are theories (the certified types of L3), and define *type* in Terms.
7. **"Cost" has two meanings.** Terms/G2/L6: the valuation of a law. G0: "cost or execution time ranks the candidates". L13 explicitly refuses to fold time and memory into cost, then uses "cost" for both in the same paragraph. Reserve *cost* for the law and say *resources* elsewhere. Related: L13's efficiency formula exp(−cost)/resources has no place for the weight it says the demand supplies.
8. **How many eurekas.** Intro: "the two eurekas". G2 status: "candidate". Open list: whether G2 is "the third eureka". G3 status: whether it is an eureka at all.
9. **Status lines that contradict themselves.** L14: "settled by his correction (draft 7)… proposed, candidate" on one line. L5: settled, with clauses marked candidate and proposed. The status is per-L but the content has per-clause status.

Apparent ones, resolved by reading two entries together — the fix is one sentence in one place: L7's "a second implementation checked against the first is consistency" vs. L14's transport (L7 itself allows the law's certificate to travel by the identity certificate); L9's "result depends only on its inputs" vs. L10's scheduling-dependent externs (the host runtime is an input — say it in L14); `assumed` meaning axiom-never-run (L4), opt-out-run-uncertified (L14), a world (L14) and "a hole that says so" (L2) — L4's "one meaning, the grade" is right, but whether the thing runs is decided by the hole kind and the demand, not the grade; and L3's "types are verified before they are constructed" inside an entry titled "the fundamental construction pattern" (two senses of construction).

## Missing

- **A certificate principle.** Its identity (hash over the cone: code, cases, seed, distribution, level), grade, that it is frozen and superseded rather than mutated (P3), that it serves any demand whose tolerance and grade it meets, default-in-the-cone with the opt-out, and transport along identity — all of it exists, scattered over L2, L5, L7, L10, L13, L14. One entry absorbs it and removes redundancies 1 and 4.
- **The two faces as terms.** "Declarative face" and "executive face" organize sections 2 and 4 and appear in G3 but are never defined.
- **The planner in one place.** L10 (forward on demand), L13 (choice among paths), L15 (planner outside the kernel; the plan is a value): what the planner may and may not do has three homes.
- **One word for competing inhabitants of a function.** Model, implementation, specimen, representative, path, inhabitant are all used. R13 refuses two models on one type while the planner "chooses among the models certified equivalent" (Terms) — that reads as a contradiction only because *model* is overloaded. Reserve *model* for what a type names; use *specimen* for the planner's candidates.
- **The setoid base case** is listed as open, but it's the most urgent open item: L5, L7 and L13 all rest on it.
- **A reference key.** P3, P5, P11, P13; R1, R8, R12, R13; `02`, `04`, `05`, `11`; the D- ids; "Kimi", "the third round". The agent the document is written for cannot resolve these.

## Reducing the count

Yes — 15 L → 11 without dropping a settled statement, and the L section should shrink by roughly a third in words, which matters more than the count.

- L1 → the preamble. It's the purpose, not a design principle; keep the sentence.
- G1 absorbs L2; L2's grade material goes to the certificate entry.
- L3, L4, L6, L8, L15 unchanged.
- L5 → equality has levels and belongs to the object, only. Its binding-acts clause moves to L9, its composition clause to the certificate entry.
- L7 + delegation-as-citation from L14.
- L9 + L11 → definitions have no effects; actions do, and are verified by observing before and after.
- L10 + L12 → the demand and the plan: forward on demand, once per plan, confluence, decorated outputs, identity of a result and the memo. Still the longest, but one subject. (Keep L12 separate only if "no hardcoded constants" is meant as a slogan for users; as a design principle it is a corollary of the demand carrying its tolerance.)
- **New: Certificates.**
- L13 → one function, many specimens, chosen by the demand's trade-off along certified identities; the transport math moves out.
- L14 → orchestration, extern, worlds, coupling — about half its current length.

If he also decides G3 is the executive clause of G0, that's 3 G + 11 L = 14 numbered principles against 19 now.

## Advice for the document

1. **Stop hand-writing the projection.** The header says this draft was written by hand and `--check` fails. The duplication is the symptom: each clause was pasted wherever it was last discussed. Edit the record, regenerate, and let the generator enforce one home per clause with cross-references elsewhere.
2. **Separate normative text from provenance.** "His words", "the model's", "Kimi", "third round", "(was L16, L21)" belong in `record/principles-language.md` — the header says so, then the body does the opposite. For the agent, each entry should be: statement (≤2 sentences), consequences (bullets), references (spec section, D-ids), status.
3. **Define the status vocabulary** (settled / proposed / candidate / mark pending / OK) and apply it per clause with an inline marker, or split clauses of different status into separate items.
4. **Move the worked examples** (γ_n at 48 kHz, the lookup table on a grid, doubling positives vs. sin of positives, y = 11 after rebinding) to an examples section or into `11`. They are the clearest part of the document for understanding and the heaviest for the statements.
5. **One old→new numbering table** at the end; drop "(was …)" from the headings.
6. **Split "What is open"** into open design questions, marks pending from him, and a changelog of what's done and implemented (which belongs in the record or `decisions.md`).
7. **Two checks for `project_principles.py --check`**: every cross-reference resolves (L-number, D-id, spec section), and no sentence appears in two entries — the second would have caught everything under Redundancies.

I can draft the reduced set with the 11 statements written out, or put this review in a doc for the agent — say which.

does separation of G0-G3 do any good or it would be better to just list the Ls?

Keep the layer only if it does a job the Ls can't. Right now it doesn't: the Ls are organized by six topics, the Gs organize nothing (no L is listed under a G), G1 duplicates L2, G3 duplicates L10, and G0 already contains G3 ("what governs execution is the demand"). So as written, flattening would lose nothing. But a flat list has one real cost — no precedence — and that is exactly what your document is missing, since it has contradictions and no rule for who wins.

Three jobs a G layer can do that a list of Ls can't:

1. **Precedence.** When two Ls conflict, the G they derive from decides; when Gs conflict, G0 decides. Take the sampled-link contradiction (L5 and L14 say a sampled link composes at the weakest grade on the intersection; L13 says never). Under G2 a sampled link is a cost with a grade and costs compose by sum; under the demand principle, which grade a demand accepts is the demand's. So the composed path exists at grade `sampled`, and L13's "never summed into a path" is a default policy of the planner, not a principle. Same with the cutoff (L3 vs L6): the demand fixes the tolerance, so the constructor's tolerance parameter is the demand's passed down, and L6's "only in the demand" stands with "or passed from it". Both resolve from the Gs in one line. A flat list leaves them as standoffs.

2. **Derivation as structure.** If the Gs become the section headings, you have one organization instead of two, the "(G1)" "(G2)" cross-references inside the Ls become unnecessary, and the agent reads "what this follows from" from the table of contents. The six current topics already approximate this, which is evidence the mapping works.

3. **A criterion for membership.** You already have one — "candidate by the P13 count, one decision guided so far" — but it's only visible in a status note. Stated as a rule ("a G is a principle that other principles derive from and that has decided at least N decisions"), promotion and demotion become mechanical, and the eureka count stops wobbling between one, two and three.

The proposal, then: fold G3 into G0 as its executive clause (its own status asks for this, and G0 already says it), which leaves a clean shape — a frame plus the two departures from it:

- **G0** Type theory is the guide: what is declared is read as types and propositions; what is computed is fixed by the demand, a judgment Luthier inhabits by search rather than normalization. Under it: L4 (holes), L5 (equality), L9+L11 (definitions and actions), L10+L12 (demand, plan, memo), L13 (specimens chosen by the demand's trade-off), L15 (minimal core).
- **G1** A theory is a type and its models are its inhabitants: a value is known by the law it satisfies, certified, not by its term. Under it: L2+L3 (membership, certified subtype), L7 (verification), the new certificate entry, L14 (extern certified by delegation, worlds).
- **G2** Laws are valued in cost: one logic, extended to [0, ∞], with Bool its retract. Under it: L6 (how laws combine), L8 (realization within tolerance).

Each G as two sentences — a statement and what it decides — with no mechanics (no `lift`, no `exact`, no "how laws combine is L6"); mechanics are what the Ls are for. That is what keeps the layer from drifting back into duplicates.

L13 straddles G0 and G2; put it under G0 (the choice is the demand's) and let it cite G2.

If you would rather not restructure, flattening is fine and costs little: G0 goes to the preamble, G1 → L2, G2 → L6, G3 → L10, each L names its parents, and you add one line — "a lower-numbered L decides a conflict" — so the precedence job still gets done. What I'd avoid is the present middle: a G layer that organizes nothing and restates the Ls.