# Decisions cited by the files of bundle C

From record/decisions.md at 869fc4cb3434a4583d19a9a6870ab43e6d2a1238.

D-2026-10-11-l  The laws of relations and actions (Reflexive, Symmetric, Antisymmetric,
                Transitive, Total, Associative, the identities, inverses, commutativity,
                distributivity, homomorphism) move from lib/algebra.lut to lib/laws.lut;
                algebra.lut imports it and keeps the structures (Setoid, Monoid, Group, Ring,
                Field and their instances). No change of meaning.
Author:     Luciano for the question; Claude for the split and the name; accepted ("Si a todo")
Quote:      "ahora las leyes de asociatividad, simetria etc deberian definirse en un modulos laws
            o algebra o un nombre mejor?" (c167022)
Source:     record/answers-annotations-principles-2026-10-11-d.md
Kind:       libraries (03). For G2 (laws come first, stated once over the signature they need)
Status:     current; done 2026-10-11 (addff54)

D-2026-10-13-l  A law is a theory: its predicate presents it, `forall` (Π) and `exists` (Σ) and the
                connectives form it, and its models are its evidence, which follows its form: a case
                is evaluated; a `forall` is modelled exhaustively, by listed cases or by a sample; an
                `exists` by a witness with its cost; `and` by a pair, `or` by one side; a citation or
                an assumption models any part whole. A `forall` is refuted exactly by a
                counterexample and over an infinite domain confirmed only by statistics; an `exists`
                is confirmed by a witness whose cost is determinate, not statistical, though over the
                reals not zero. `then` is material, `not (p and not q)`; conditioning is not a
                connective (Lewis, 1976) but an operation on a measure, with the chain rule.
Author:     Luciano for the question, `forall` and `exists`, the certifiers as models of the
            quantifier and citation of the whole law, and the inexact witness over the reals; the
            model for the rest
Quote:      "Las leyes a su vez son teorias o son  modelos?"
            "Tenes ambos el Forall y el Exist (para optimizacion o inversas por ejemplo)"
            "yo estoy tentado a pensar que el exhaustive y el sampled son modelos del Forall , el cite
            es modelo de toda la Ley."
            "Si, me cierra."
Source:     chat:f15ae1b6:2245
            chat:f15ae1b6:2273
            chat:f15ae1b6:2273
            chat:f15ae1b6:2311
Kind:       principles (L9.11, L9.12, L12.1) and spec (5, 6.S7). For L8.1, L9, G2
Status:     current; the clauses proposed in their wording
