# Brief: the case against Luthier's five claims of novelty

Read-only: change no file. Your final message is the report, in English, in Markdown; the
coordinator saves and commits it. Probe in memory only (PYTHONDONTWRITEBYTECODE=1, PYTHONPATH at the
repository's src, /home/lmoffatt/miniconda3/bin/python); never run `luthier certify`, `test` or `run`.

record/plan/related-work-2026-10-27/related-work.md (section 15) states five claims of novelty:
(1) proof, exhaustive enumeration, listed cases and sampling unified as graded evidence over a
domain, persistent and composable; (2) per-conjunct negative controls and vacuity rejection inside a
theory's certificate; (3) static affine bound transformers and dynamic ball arithmetic as models of
one theory; (4) implementation substitution only along certified identities; (5) typed derivations
of values across language boundaries. Luciano (2026-10-27): for what is new, show it is not wrong,
what it gives, and why it might not be used "por alguna razón que se nos escape".

Argue the case against, claim by claim, as a hostile reviewer would: (a) is it wrong somewhere? find a
counterexample or an inconsistency in Luthier's own record (principles, spec, decisions, the code),
or a known impossibility result it runs into (no free lunch for testing; Rice; Richardson; the
statistics of sequential testing; composition of evidence under dependence; the cost of
content-addressing; provenance blow-up); (b) is it really new? name prior work that already does it,
beyond related-work.md, with verifiable references; (c) why would nobody use it? cost, friction,
false confidence, maintenance, a simpler alternative that gets most of the value. Then, for each
claim that survives, the strongest concrete case where it gives what existing tools do not, with a
small example. Read CLAUDE.md, docs/concepts.md, record/principles-language.md, the related-work
report, the audits in record/plan/audit-algebras-2026-10-22/ and record/plan/foundations-2026-10-27/
(the latter found the sampler is a rotation and identities miss runtime state). Plain English,
no em-dashes as punctuation, numbered references with their statement at first use.
