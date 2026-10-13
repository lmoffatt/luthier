# Principles, 2026-10-13 (second): nine clauses for your marks

At the commit that holds this file. The reflections of the plan from zero, brought into the
principles before the first theory is written (D-2026-10-13-k). All five are `[proposed]` in
`record/principles-language.md` and projected into `docs/principles.md`. Mark "ok", "no" or a
comment under a line.

- L2.6, new: the theoretical module of L2.4 is a file of its own; a theory file holds types,
  declarations and laws, and is what the checker reads; each model, or each algorithm written
  against the theory, lives in its own file, read only when a demand needs it and certified
  against the theory; what a file imports has its theory in a theory file (D-2026-10-13-i, -j).
- L6.13, new: an algorithm is written against a theory, never against a model; it is a functor
  that takes any model, so each specimen can stand in for another, certified per instance unless a
  cited proof covers every model (D-2026-10-13-j).
- L6.14, new: an import line names what enters with its theory, `import "x.lut" M : T`, so the
  importer is checked against `T` without reading `x.lut`; the ascription of L6.12 happens there.
  This one follows Z5 of the plan, which also waits for your mark.
- L8.9, new: everything has laws, at the least those of its equality; there is no data without
  them; what comes from the world enters as bytes or a `String` and a check refines it once into
  its lawful type (D-2026-10-13-j).
- L14.6, new: of the two orders of bootstrapping, the theory comes first; Luthier's theories are
  written in Luthier before any implementation and are the authority, and the host's files and
  later the Luthier implementations are their specimens (D-2026-10-13-h).

Four more, from the conversation on laws and costs (D-2026-10-13-l, -m):

- L9.11, new: a law is a theory; its predicate presents it, `forall`, `exists` and the connectives
  form it, and its models are its evidence, which follows its form (a case evaluated; a `forall`
  covered exhaustively, by cases or by a sample; an `exists` by a witness with its cost; `and` by
  both, `or` by one; a citation or an assumption covers any part whole).
- L9.12, new: a `forall` is refuted exactly by a counterexample and confirmed over an infinite
  domain only by statistics; an `exists` is confirmed by a witness whose cost is determinate,
  though over the reals not zero.
- L12.6, new: cost is two things. A distance (how far an approximation is from the ideal) is the
  one logic of G2 and the value of a law; a probability (how sure a sample makes us) is the
  evidence, and how evidences combine is an assumption about dependence (nested, independent and
  rare, or the joint known). L10.1 now says the bound is the distance the `forall` gives.
- L12.7, new: `then` is material, `not (p and not q)`; conditioning is an operation on a measure,
  with the chain rule, not a connective (Lewis, 1976); for distances, `then` is the triangle
  inequality, the transport of L10.7.

