# Brief: what Luthier defines conceptually but leaves without the algebra that implements it

Luciano (2026-10-22): find which principles, specification clauses or code are not described or
resolved enough. "Por ejemplo: los niveles de certificación y el álgebra de certificaciones. Qué
cosas están definidas conceptualmente pero el álgebra que las implementa no lo está."

This is a read-only audit. Change no file. Your final message is the report, in English, in
Markdown; the coordinator saves and commits it.

Read: `CLAUDE.md`; `record/principles-language.md` (the principles' source; L1 to L16, G0 to G2,
the O items, which are the open problems already known); `docs/spec/00-index.md` and every
chapter; `docs/concepts.md` (a reader's account, with its "What is open" section and its gaps);
`record/decisions.md` (latest decisions first; D-2026-10-18-c, -d, -i, -j and D-2026-10-22-a are
about planes, budgets, the algebra of costs, numerical laws and what a certificate serves);
`record/plan/core-2026-10-17/execution.md`; and the code in `src/luthier/` (certify.py, run.py,
tester.py, check.py, elaborate.py, kernel.py) where a concept is implemented.

For each concept that is named and motivated but whose operations are not fully defined, report:
- the concept, and where it is defined (clause numbers with their statements, decision ids, spec
  clauses, files and functions);
- what is defined: the carrier (what the values are) and the meaning;
- what is missing of its algebra: the operations (combine, compare, order, join, meet, compose,
  transport, project), their laws (associativity, monotonicity, units, distributivity,
  preservation), how it composes along a program (through a conjunction, a cone, a function
  application, a model substitution, a language crossing), and the boundary cases (empty, vacuous,
  infinite, disagreeing evidence);
- whether the code already implements some of it implicitly (an ad hoc rule in a function), and
  whether that rule agrees with the spec or the principles; quote the code's location;
- what it blocks or what could go wrong while it stays open (a concrete scenario);
- whether a known mathematical structure fits (a lattice, a quantale, a monoid, a Lawvere metric,
  an imprecise probability, a graded monad, a fibration...), with a reference, marked as your
  proposal.

Start with Luciano's example and treat it fully: the grades of evidence (proved, exhaustive,
cases, sampled, assumed and the others the spec names), their order, how grades combine across
the conjuncts of a law, across a law's lines and seeds, across the cone of a run, under a model
substitution, and how controls enter (D-2026-10-22-a: a pass is about its model, a control is about
the law). Then the others you find, for example: the algebra of error, uncertainty, evidence and
resources (D-2026-10-18-i and its correction to Lawvere's order); tolerances and their
propagation (D-2026-10-18-j); budgets scaling with bounds (D-2026-10-18-d); the demand and what it
selects; specimens and the planner's identities; decorated outputs; the three planes; result
identity; the new idea of a value's derivation (record/IA/gpt-2026-10-22/) if it is in the record
by the time you read.

Order the report by how much each gap blocks: first what the code already decides without a
specified rule, then what blocks the next milestone, then what is open on purpose (O items) with
what is still missing in it. End with a table: concept, where, missing, implemented implicitly
(yes/no and where), blocks, proposed structure. Write for Luciano and for the sessions that will
act on it: no em-dashes as punctuation, no "not X but Y" constructions, numbered references
carrying their statement at first use ("L10.12 (a store lives beside the file that claims it)").
