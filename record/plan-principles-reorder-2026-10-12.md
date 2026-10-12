# The L reordered by topic, with the merges proposed

2026-10-12, for Luciano to mark. Proposed by the model on his instruction in the chat of 2026-10-12
("no pongamos si derivan de G0-G3, sino un orden natural, quizás desde lo más general a lo más
particular, ordenado por tópicos; también quiero propuestas para fusionar Ls"). The statements are
those of `docs/principles.md` draft 10 (6edb543); the organizers are G0 (type theory is the guide),
G1 (a type is a theory and its values are its models), G2 (laws are valued in cost), G3 (the demand
defines what is computed). Nothing is applied until he marks it. Mark each line OK, no, or a
correction.

## The order

Six topics, from the most general to the most particular, and the same inside each topic. A line
with "+" is a merge, detailed below; "→ G1" is an absorption into the organizer.

1. What the language is for
   - L1 Luthier expresses the invariances of the disciplines.

2. Types, theories and models: the declarative face
   - L2 A type is a proposition, and membership is a guarantee.
   - L4 The certified subtype from a predicate is the fundamental construction pattern.
   - L8 Declare, then define, then inhabit.
   - L16 Equality has levels and belongs to the object.
   - L3 Defining a model defines its test. → G1, which already says it ("to declare `m : T` is
     to declare the tests `m` will pass").
   - L20 A function is declared in a theory and is universal over its models. → G1 (done, draft 9).

3. Laws and their verification
   - L5 + L11 A law characterizes, and is verified by one operation, exact or statistical.
   - L21 A certificate of identity is not a certificate of the law. (candidate; kept apart)
   - L15 The ideal world is realized with a guarantee.

4. Programs and their execution: the executive face
   - L9 + L18 A program is a DAG of definitions without effects, and statements commute.
   - L19 + L13 The demand determines the computation, and what it forgets.
   - L12 Evaluation is verification; execution is an action on the world. (shortened: the half
     now in Terms goes; what stays is that an action is verified by observing before and after)
   - L17 Every criterion is a parameter.

5. Implementations and the outside
   - L10 One function, many paths.
   - L14 + L22 Luthier orchestrates other languages; what does not follow its way lives in a world.

6. The language itself
   - L6 + L7 The core is minimal, executable by hand, and its programs are data.

From 22 to 15: five merges, two absorptions. No clause is dropped; formulations are joined.

## The merges

| Merge | Why | What the joined formulation keeps |
|---|---|---|
| L5 + L11 | What a law says and how it is checked are two halves of one thing; L5's "cases chosen by the law" is L11's method. | L5: a law states a property, a second implementation checked against the first is consistency, laws accumulate (D-2026-10-11-d), the puzzle over several functions. L11: citation, exhaustive, cases, sampled; the grade travels in the certificate; the distribution matters; delegation to a library as citation (proposed). The composed grade of a theory's one law (proposed on his note on Terms). |
| L9 + L18 | L18 (no effects) is the precondition that makes L9 (dependencies the only order) true; they are one fact seen from two sides. | L9: the DAG, time reconstructed from dependencies, blocks and `<-` (D-2026-10-11-i), a law over two operations is a node with two parents, a mutable parameter is two variables, the second structure (equivalence or metric). L18: result depends only on inputs, effects only in actions, every strategy gives the same result, `Confluent` in `lib/plan.lut`, his words on the one effect (the name, once). |
| L19 + L13 | Forgetting is the complement of the demanded cone; L13 is a corollary of L19. | L19 whole (backward plan, forward run, each node once per plan, the identity of a result, the memo, tests as actions, three objects, the chain of certificates, the session, the decorated output as a model, proposed). L13: what is forgotten is what the demanded value does not need; run time and type forgetting are one; never erase what recertifies; no overload per subtype; elaboration independent of the observer, the memo not; two caches. |
| L14 + L22 | L22 (a non-Luthier way inside a named world) is the case of L14 where the extern has no law yet. | L14 whole (extern over what it really receives, validated on first demand, refused if it fails, his words; certification the default and the opt-out, D-2026-10-11-n; the coupling language). L22: allowed inside a named world, certificates `assumed`, outside the planner's graph until a law is certified. |
| L6 + L7 | Both say what the language is made of: a small core, and programs as values of it, so the interpreter is written in Luthier. | L7: a handful of primitives, hand execution given a plan, four layers of trust. L6: a program is an element of Luthier, programs build and run programs. |

Not merged, and why: L2 and L4 (a proposition versus a construction pattern); L21 (a distinct
distinction, his wording pending); L15 (the one L of cost; it would merge into L5 + L11 only once the
algebra of costs exists); L17 (a rule of its own, P11 restated); L10 (the planner's own L).

## Two decisions for him

- D1 Numbering. D4 of the generative plan kept the L numbers because the record cites them. With
  the G renumbered today, the model proposes to renumber L1 to L15 in the order above and to keep
  the map old → new in `record/principles-language.md`, as the G mapping is kept. The alternative
  is to keep the old numbers with merged headings (L5/L11).

- D2 L21. Kept apart as a candidate until he marks its wording (graded transport), or merged into
  L5 + L11 now.

## Execution, once marked

One commit on `docs/principles.md`: the L sections replaced by the six topics, headings with the
old numbers in parentheses until the draft closes, formulations joined without rewording; then the
record updated (entries merged, History lines, the map) and the projection regenerated.
