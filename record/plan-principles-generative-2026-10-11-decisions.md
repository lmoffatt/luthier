# Rewriting the principles from generative ideas: the decisions

Draft 1, 2026-10-11. Draft 0 (85975c6) was written before the audios of 08.58 and 09.01
(45df807, 844e505); what they changed is marked "(audio 08.58)" and listed in addendum 5 of the
analysis. Written for Luciano, to answer before the execution starts. The execution is
in `plan-principles-generative-2026-10-11-execution.md`. What comes from a source is cited; the
rest is Claude's proposal. Settled in chat today and not asked again: one first principle with
deviations justified by what it costs not to depart (chat, after the floating point note); laws
accumulate and define by description (D-2026-10-11-d); W5 is a bootstrapping practice (same).

## What this is for

Luciano (`record/Lucianos ideas/principios organizadores.txt`): "un principio es un organizador y
como su nombre lo indica es el primero". Draft 1 of `docs/principles.md` lists twenty L and
fourteen W as peers. Draft 2 derives the L from his organizers, so that the list admits three
checks it cannot admit today: an L that derives from no organizer is a rule of construction or a
missing organizer; an organizer that guides no decision is a candidate, not a principle (P13, a
principle is worth the decisions it guides); a derivation that needs an extra assumption names it.
The analysis the plan rests on is `record/organizing-principles-2026-10-11.md`.

## The decisions

Answer with the number and ok, no, or a correction.

**D1. The organizers and their order.** One first principle and four deviations, each named by
what type theory lacks:

- G0 Type theory as guidance (his A): types as propositions, laws define objects, a law gives a
  quotient.
- G1 Declarative and executive are separate; the executive is the demand (his F, which generates
  his B). Type theory has no executive face.
- G2 A function is known by description, from outside; the implementation is the specimen (his C,
  as clarified: à la Russell, not constructive). A description is derived by composition of the
  laws of the parts when such a law exists (his "parte Tarski", audio 08.58 at 32:01) and observed
  otherwise; the demand says which descriptions are produced. Type theory knows a function by its
  term.
- G3 Laws are valued in [0,∞) and their cost is itself uncertain, so composition is Bayesian (his
  D, with addendum 2 of the analysis); what a run teaches is kept and accumulates across runs
  (audio 08.58 at 05:47, in his words a wish more than a principle). Type theory's truth values
  are two and a run leaves nothing.
- G4 Expressive over restrictive (his E). Type theory has one canonical form per value.
- Recommended: this order; G4 last because it decides between designs rather than describing the
  language, and the execution treats it as the tie-breaker among derivations.

**D2. The wording.** Each organizer is printed as his quote first, verbatim from the note or the
timeline, then a formulation of at most two lines by the model, marked *Proposed* until he marks
it. He marks the five formulations before any derivation is written.
- Recommended: yes. One screen, five items.

**D3. What leaves the list of the language.** L7 (minimal core executable by hand), L17 (every
criterion is a parameter) and the orchestration half of L14 move to the way of working, as W15 to
W17, because no organizer generates them. L12 (two faces) is absorbed by G1 as its statement; L1
(invariances of the disciplines) stays as the first consequence of G2.
- Recommended: yes. The move keeps their sources and their text.
- Added from the audio of 08.58 (09:20 to 13:19): a candidate L21 under G2, a certificate of
  identity of the implementation (same bits with the same seed) kept apart from a certificate of
  the law. Enters step 2 as *Proposed*; he marks it with the others.

**D4. Numbering.** The L numbers are kept (L18, L19 and L20 are cited in `record/decisions.md` and
in the spec); each L gets a tag of its organizers, and draft 2 is ordered by organizer, not by
number. Taken by the model unless he objects: renumbering would break references for nothing
(P6, every change can be undone, is served by the references holding).

**D5. The P13 check.** For each organizer, the execution lists the decisions in
`record/decisions.md` whose Kind line names an L or P it generates. An organizer with no decision
is marked "candidate" in draft 2 and stays in the list; removing it is his.
- Recommended: yes. Expected result: G3 has the fewest; that is a finding, not a defect.

**D6. Where the articulation of G3 goes.** The justification of cost-valued laws (analysis §4 and
addendum 2: Ω replaced by [0,∞), quantitative equality, graded judgments, cost = −log p, the cost
of a law over floats is itself estimated) is too long for the principles. Two lines in draft 2 and
the full text as `docs/rationale/cost-valued-laws.md`, draft 0, with its sources (prior art cluster
G, his notes of 2026-05-29 and today).
- Recommended: yes.

**D7. The record of principles P1 to P14.** `record/principles.md` is not changed. P10, P11 and
P14 are principles of the language already in the record; draft 2 cites them where an L restates
them (P14 under G2, P10 under G0 at L5, P11 at W16) and does not move them.
- Recommended: yes, for P3 (keep the original evidence; put the best reading in front).

**D8. The dependencies among organizers are printed.** The three of analysis §3 (G0's quotient
needs G1 and G3; G2's inhabitance needs G3; G1's planner is G0's proof search with G3's cost) go
in draft 2 after the organizers, as *Proposed*, so that the reader sees that G3 is load-bearing.
- Recommended: yes; it is what changes the order of work.
