# Brief: is Luthier derivable from what is already established? The interaction laws

Luciano (2026-10-27), his reasoning: a paper that is A + B + C, with A, B and C known, adds nothing if
the + is free (the combination was known to be possible); it adds something if the combination was
not known to be possible a priori and carries a new law. "La idea es analizar Luthier desde este
punto de vista. Los elementos de Luthier están probados. Ahora, cómo Luthier los enhebra en un
conjunto, ¿está también probado o dicho en algún lado? O sea, ¿es derivable Luthier a partir de
elementos ya dichos? ¿Es un ejercicio de un libro? Igual, si lo es, mejor: estamos en tierra firme.
Si no lo es, bueno, tenemos que demostrarlo."

The coordinator's frame: Luthier's elements are established (types as theories, refinement types,
property testing, mutation testing, the rule of three and sequential tests, Higham's bounds, ball
and interval arithmetic, content hashing, provenance, algorithmic choice; see
record/plan/related-work-2026-10-27/related-work.md). What is Luthier's own is how it joins them: the
interaction laws, equations that mention two or more elements and follow from neither alone. In
algebraic terms, the free combination is a coproduct; a gluing law makes it something else.

Do, reading the record first (record/principles-language.md, docs/spec/, record/decisions.md,
docs/concepts.md, the theories of Luthier's own machinery in src/luthier/lib: certification.lth,
demand.lth, plan.lth, laws.lth, test.lth, world.lth, and core/structures):
1. Inventory every interaction law Luthier states or relies on: a law that ties two or more
   elements (for example: a pass is about its model and a control about the law, D-2026-10-22-a;
   sampled evidence is worth its ε̂ only if its identity captures what changes the result; a ball
   through an operation is the operation's transformer at its midpoint; substitution along a
   certified identity keeps the grade within the identity's domain; a kernel change transports
   certificates along a certified edge, D-2026-10-27-a; evidence along a chain composes by the
   capped sum, D-2026-10-25-a; the demand selects the projection of a derivation, L5.23; a
   certificate is keyed by the cone, L10.4). Give each a number, its statement, the elements it
   joins, and where the record states it (or that it is only implicit in code).
2. For each, classify, with the argument: (a) derivable from established results: give the
   derivation, a textbook exercise, citing the results it uses (a theorem, a book's chapter);
   (b) a known theorem in the literature: cite it; (c) new: say what would have to be proved, try a
   proof sketch, and say what could make it false (a counterexample to look for). Be strict: a law
   that holds only under a premise Luthier does not enforce is (c) with that premise named.
3. For each, the free combination that should violate it (the naive joining of the same elements,
   for example substitution without certificates, property tests without a complete identity), as
   the control of the interaction law; and whether Luthier certifies the law on itself today (a law
   line and a control in its own test programs) or not.

Write `record/plan/interaction-laws-2026-10-27/inventory.md`: the table (number, law, elements,
where stated, class, citation or proof sketch, the free combination that violates it, certified on
itself: yes/no/where) and a short conclusion: how much of Luthier is "an exercise of a book", how
much is new and needs a proof, and which new laws a paper would rest on. Mark what is the record's,
what is the literature's, and what is yours. Plain English, no em-dashes as punctuation, every
symbol defined at first use, numbered references with their statement. Touch only that folder.
Commit staged by path (subject, blank line, one body line, ending with "Co-Authored-By: Claude
Fable 5.1 <noreply@anthropic.com>"). In your final message: the counts per class and the laws of
class (c), one line each.
