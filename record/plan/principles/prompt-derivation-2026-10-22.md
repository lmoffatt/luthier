# Brief: a value's derivation, and its crossing of language boundaries, in the principles

Luciano (2026-10-22), on his dialogue with GPT: "me parecen buenas propuestas para cambiar los
principios". The sources, committed verbatim at c312464 in `record/IA/gpt-2026-10-22/`:
`dialogo.md` (his questions and audio lines, and GPT's answers) and
`luthier_computational_history_prompt.md` (GPT's instruction for this revision). His own words in
the dialogue are the authority; GPT's text is a proposal to weigh, not an order. Where GPT's
instruction conflicts with the record, the record wins and you say so.

The idea, in his words: "el tipo tiene un poco la historia del cómputo y [...] este tipo con la
historia del cómputo tendría que poder atravesar las fronteras de lenguajes"; and Luthier as "un
manejador de lenguajes [...] un director de orquesta, de velar por la integridad teórica de las
teorías y de los datos".

Read first: `CLAUDE.md`; `record/principles-language.md` whole (the source; `docs/principles.md`
is its projection, never edited by hand); `docs/principles-for-readers.md`; `docs/concepts.md`
(sections 8, 12 to 14: certificate and cone, demand, specimens, claim/evidence/execution);
`record/decisions.md` on L5, L10, L11, G0, G1, decorated outputs, result identity, and D-2026-10-22-a
(a pass serves its model; a control serves the law), which already separates evidence about a model
from evidence about a theory, the same cut GPT's "certificate of model / of computation /
derivation of value" makes. Grep before writing: "derivation", "decorat", "provenance",
"identity", "extern", "orchestrat", "coupling", "history" in principles, spec and decisions; what is
already settled is cited, not restated.

Do:
1. Decide, with reasons, where the commitment lives: new clauses in L5, L10 and L11, a new
   principle, or a new organizer. GPT suggests deriving it from G0 and G1 without a new organizer;
   check that against the record.
2. Write the clauses into `record/principles-language.md` in its own format, each marked
   [proposed], each with its source (Luciano's lines in `dialogo.md`, cited; what is GPT's, marked
   as GPT's; what is yours, marked as yours). Keep the distinctions the dialogue draws: a
   derivation is not a trace and not a certificate; a demand selects the projection of a
   derivation that is materialized (as it selects the cone); a derivation is quotiented by
   semantic relevance; language crossings must not erase it. Keep it at the level of principles:
   no syntax, no `History<T>`, no kernel change. Say in the clauses what is deferred and to which
   version, as GPT's roadmap suggests, only where the record agrees.
3. `python3 scripts/project_principles.py --write`, then `--check`: it must pass.
4. A one-screen note for Luciano, `record/plan/principles/derivation-2026-10-22-decisions.md`: what
   changed (by clause number with its statement), and at most three questions he must answer, each
   answerable after reading a screen, with your recommendation. Commit it before he annotates it.

The core's rebuild is running in other agents (src/, the library, the examples, the spec,
`record/plan/core-2026-10-17/`): touch none of those. Write the principles in the record's style:
no em-dashes as punctuation, no "not X but Y" constructions, no inflated vocabulary; every symbol
and abbreviation defined at first use. Small commits staged by path: subject, blank line, one body
line, ending with "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>".

Accepted when: `project_principles.py --check` passes; every clause cites its source and carries
[proposed]; the note is committed. Report in your final message: the clauses added or changed
(number and first line), where GPT's instruction was followed and where not and why, the
consequences for docs/concepts.md and the spec (listed, not done), decisions taken on your own.
