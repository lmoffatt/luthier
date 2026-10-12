# Draft 11 of the principles: the execution

Draft 0, 2026-10-12. Written for the sessions that carry it out. The choices it rests on are
D-2026-10-12-g to -p in `record/decisions.md` (6b729dc) and D1 to D3 of
`plan-principles-draft-11-2026-10-12-decisions.md`; where a step depends on one of the latter it
says which, and what it assumes until Luciano answers. Inputs: `docs/principles.md` draft 10
(b7a7e23), `record/principles-language.md` (at 72cc7be or later), `scripts/project_principles.py`
(v1), `docs/principles-for-readers.md`, the six critiques (`record/IA/principles 2026 10 12/`,
1429f35), the recommendations with his marks (e8d7db1).

## Rules for every step

- Commit before every change; one step, at least one commit; the message names the decision.
- Luciano's notes and marks are never edited; a quote is copied verbatim.
- Every clause the model writes is marked *proposed* until he marks it; his marks are committed
  verbatim before the text that incorporates them.
- `docs/principles.md` is never edited by hand again: every change goes to the record and is
  projected with `--write` (D-2026-10-12-d).
- No step changes the spec (`docs/spec/`) or `docs/way-of-working.md`.

## Step 1. The record current with draft 10

Bring `record/principles-language.md` to draft 10: the organizers renumbered (G1 theory and
model, G2 cost, G3 the demand), the L reordered in six topics and merged (72cc7be), his marks
on the reorder plan (14ea9f0), the status words fixed (25f9c5e, b7a7e23). The History field of
each entry records the move with the old tag. Add the draft 10 row to the drafts table. Run
`--write`; done when `--check` passes with the projection equal to draft 10 up to the header.
Nothing of draft 11 enters here.

## Step 2. The projector for the new shape, and the lints (D-2026-10-12-g, -o)

Extend `scripts/project_principles.py` (version to v2):

- Entry fields: `Statement` (one or two sentences, the head line), numbered clauses `1.`, `2.`
  under `Clauses:`, each ending with its status in brackets (`[settled]`, `[proposed]`,
  `[candidate]`, `[mark pending]`); `Example:`; `References:` (spec sections, D ids);
  `From:` (its G and the Ls it derives from); `Rests on:` (the open item, if any).
- Projection: statement, clauses with their status, example, references, from, rests on. Quote,
  Source and History stay in the record.
- The two lints in `--check`: every `G\d+`, `L\d+`, `L\d+\.\d+`, `D-\d{4}-\d{2}-\d{2}-[a-z]` and
  spec section cited in the record resolves (the Ds against `record/decisions.md`, the spec
  sections against `docs/spec/`); no sentence of more than eight words appears in two entries.
  Both are informational on the record at draft 10 and blocking from step 4 on.
- A `## Numbering` section generated from the History fields: the old-to-new table (his mark).

Tests in `tests/` for the parser, the two lints and the table. Done when `--check` passes on the
record of step 1 with the lints reporting, as information, the duplicates and the dangling
references of draft 10 (expected: the transport rule in L5, L13, L14; D-2026-10-11-n five times;
G0's reference to G2 for the ranking).

## Step 3. The shape applied to the record (D-2026-10-12-g; D3 assumed as proposed)

In `record/principles-language.md`, without changing what any clause says:

1. The purpose sentence (today L1) before the organizers; L1's entry retired, its History kept.
2. G0, G1, G2 as two sentences each, no mechanics, no status; G3's content moved to L10's
   statement (its own status asked for it). The Ls listed under their G; the six topics become
   subsections. The P13 count and the eureka history to the record's prose, out of the entries.
3. Terms: each term in one category (structure, theory, model, specimen, law, certifier,
   certificate, cost, resources, plan, demand, action, world), defined once; the grades defined
   here and deleted from L2, L6, L7, L14, which cite Terms; nothing marked proposed or open
   stays in Terms (the setoid clause moves to What is open).
4. Each entry rewritten into statement and numbered clauses, each clause with the status its
   sentence had in draft 10; the examples (γ_n at 48 kHz, the lookup table, doubling positives,
   y = 11) into `Example:`; the provenance phrases ("his note of…", "the model's correction",
   "Kimi", "the third round") into History; "(was …)" out of the headings, into the table.
5. One home per mechanism: the transport rule in the certificate entry (step 4), cited from L5,
   L13, L14; D-2026-10-11-n, -m, -i cited by id where they were written out.
6. The precedence line after the organizers.
7. What is open split: open design questions, each with the principle it blocks (Kimi's map:
   which settled clauses rest on which open item, as `Rests on:`); his pending marks in a list;
   the done and implemented items to the drafts table.

Project; run `--check` with the lints blocking. Done when the projection reads with no sentence
in two entries, no dangling reference, no mixed status, and Luciano has the diff of statements
(one screen: the new statements only) to mark.

## Step 4. His decisions applied (D-2026-10-12-h to -p; D1, D2 as proposed until he answers)

Content changes, each its own commit, each clause marked proposed:

1. New entry, Certificates (under G1): identity hashed over the cone; law, domain, distance bound,
   evidence cost (D2); frozen and superseded, never mutated (P3); serves any demand whose cutoff
   it meets; default in the cone with the demand's opt-out (D-2026-10-11-n); transport along
   identity: distance summed, evidence summed, domain intersected (D1). Absorbs the transport
   text of L5, L13, L14 and the grade text of L2, L7.
2. L5: equality has levels and belongs to the object; the binding-acts clause to L9; the
   composition clause to Certificates; the intersection rule deleted (D1).
3. L13: specimens chosen by the demand's trade-off along certified identities; "never summed into
   a path" deleted (D1); quotient only for the decidable regime, "semantic equivalence forms
   classes; certified substitutability forms a graph" (GPT sp's wording); *cost* for the law and
   *resources* for time and memory; the efficiency formula with the demand's weight named.
4. L3 and L6: the cutoff is the demand's minimal cutoff for an implementation (D-2026-10-12-h);
   L3's constructor takes no tolerance; L6 says "the cutoff is the demand's" and drops "only".
   L6: `lift` and `exact` called a retraction, not a homomorphism, until the algebra is fixed;
   the grade of a sum as the demand's parameter, vector or weakest (-i); the two candidate
   algebras named (-p), with the path composition fixed as the sum (D1).
5. L7: law and certifier distinct (-k); the delegation-by-citation text of L14 joins it.
6. L9 + L11 merged: definitions have no effects; actions do and are verified where observable,
   audited otherwise; actions on Luthier's own state idempotent and memoizable (-m).
7. L10 + L12 merged: the demand and the plan, statement "meaning, realization, evidence: three
   objects, never one"; memo identity, decorated outputs and sessions as clauses; L12's content as
   the clause "no unrecorded policy constants" (-n).
8. L14 halved: orchestration, extern, worlds, coupling; an extern without a law executes inside a
   world and enters neither the planner's graph nor a certified theory.
9. L2 absorbed into G1's L2+L3 entry (membership, certified subtype); L4 unchanged; L8 and L15
   unchanged.
10. Vocabulary pass over every entry (-l): structure, theory, model, specimen, cost, resources.

Project; `--check`; `docs/principles-for-readers.md` revised against the new numbering and its
cited entries; the numbering table checked by eye. Done when the projection passes and the diff
of statements and the list of proposed clauses are in front of Luciano.

## Step 5. His marks, and draft 11 tagged

His marks committed verbatim; applied in the record; projected. The P13 count recounted over
`record/decisions.md` for the three Gs. Tag `principles-draft-11`. Done when he says so.

## What each step assumes

- Step 3 assumes D3 as proposed (Gs numbered, heading their sections, precedence by G). If he
  answers "unnumbered", the Gs become the orientation paragraph and the precedence line reads
  "the lower-numbered L decides"; step 3.2 changes, nothing else.
- Step 4.1 to 4.4 assume D1 and D2 as proposed. If he keeps L13's prohibition, 4.2 and 4.3 keep
  "never summed" as a clause of Certificates and the evidence cost of a sampled link is not
  composed; if he rejects the evidence-cost conversion, the grades stay as the lattice of
  draft 10 and Certificates carries grade instead of evidence cost.
