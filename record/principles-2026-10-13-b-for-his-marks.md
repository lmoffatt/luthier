# Principles, 2026-10-13 (second): five clauses for your marks

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
