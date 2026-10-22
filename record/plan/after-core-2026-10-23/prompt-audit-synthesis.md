# Brief: the algebra audit, synthesized for Luciano and planned for the sessions

The audit (`record/plan/audit-algebras-2026-10-22/report.md`, Codex, 5b1a05e) has four parts.
Part I's concrete defects were fixed in bite 13c (`record/plan/core-2026-10-17/report-bite-13c.md`
with its follow-ups) and stated in certification.lth's `Routing` (report-bite-13b.md, "Before the
tag"); D-2026-10-22-a and -d decided what a pass and a failure are about. The rest (parts I's
conceptual sections, II, III, IV) is what Luthier defines without the algebra that implements it.

Read `CLAUDE.md`; the audit whole; `record/principles-language.md` at the clauses it cites, O1 to
O13; `record/decisions.md` from D-2026-10-16 on; `docs/concepts.md` sections 6 to 15. Grep before
reasoning: a gap the record already settles or defers is cited, not reopened.

Write a plan in two documents, as the project does (CLAUDE.md):
1. `record/plan/audit-algebras-2026-10-22/decisions.md`, for Luciano: one screen. What the audit
   found that is already done (one paragraph). Then at most five questions, the ones only he can
   answer, ordered by what they unblock; each answerable after reading it, with what it implies,
   what it costs, and your recommendation. A question is his only if it changes a principle or a
   decision of his, or picks between mathematical structures with different consequences (for
   example the grades' order and how evidence combines across conjuncts, lines and a cone; the
   orientation and tensor of the error and evidence quantales; tolerance propagation as bound
   transformers; the intensional exponential for derivations). Everything else is not his.
2. `record/plan/audit-algebras-2026-10-22/execution.md`, for the sessions: every remaining gap of
   the audit, each with its source (audit section, clause or decision), what to build, what it
   depends on (which question of document 1, if any), its acceptance criteria, and its order;
   grouped in bites small enough for one agent each, the model fit for each (Sonnet for reading
   and mechanical code, Opus for code with judgment, Fable for theory).

Mark what is the audit's, what is the record's, and what is yours. Write for Luciano: no
em-dashes as punctuation, no "not X but Y" constructions, numbered references with their
statement at first use, every symbol defined at first use. Touch nothing outside that folder.
Commit both, staged by path (subject, blank line, one body line, ending with "Co-Authored-By:
Claude Fable 5.1 <noreply@anthropic.com>"). Another agent changes the core's list library now.
In your final message: the five questions in one line each, and decisions taken on your own.
