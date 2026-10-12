# Brief: chapter 4, Static semantics

Read `record/spec-briefs/common.md` and `record/spec-brief-template.md` first.

## Goal

Write `docs/spec/04-static-semantics.md`, chapter 4 of the specification: what the checker decides
about a program before anything runs: the states of a name, theories as cycles, the
well-formedness rules R1 to R13 with their programs, the reports that do not reject, and the
example. The old file `docs/spec/05-static-semantics.md` is your main source and stays in place;
the integrator deletes it.

## Sources

- `docs/spec/05-static-semantics.md` at d12b554: §1 to §6 and §8 are yours. §7 (certification)
  is chapter 6: cite `spec 6` where the source relies on it and do not copy it. §9 (presentations
  and translations; Checks) is chapter 5 (Checks, `Failures E`) and chapter 9 (presentations):
  cite them. §10 (open) becomes O ids and "decided without an id" items.
- `docs/principles.md`: L2 (declare, define, inhabit), L8 (a type is a proposition, membership is
  a guarantee, the certified subtype), L3 (equality), L14, Terms (object, theory, structure).
- `tests/spec/r*_*.lut` for the files of each rule; `src/luthier/checker.py` (read only) to
  confirm what is implemented.

## What changes against the source

- Each rule is `**4.Rk. Title.** [status] text. Files: ...`, k from 1 to 13 in the source's order.
  R1 to R9, R12, R13 have files and are `[implemented]`. R10 (a law characterizes; decided
  2026-10-05) and R11 (a condition refines in its branch; decided 2026-10-06, not implemented)
  have no files and no decision id: `[proposed]`, listed in the report as "decided without an id"
  with their dates. The addition to R2 of 2026-10-07 (no loose functions) is `[decided
  D-2026-10-07-e]` if that id exists in `record/decisions.md` (check), else "decided without an id".
- "Object" means the cycle in the source; write "theory" for the cycle (D-2026-10-12-z: a theory
  is the object several names define together) and use "object" only in the sense Terms gives it,
  anything a name defines. §3's title becomes "Theories are cycles, branches name them". O7 is
  closed by this; do not cite O7 as open.
- The grades: where the source names them (§1's table, §6), use the five of Terms
  (D-2026-10-12-y) and cite `spec 6` for what a certificate records.
- "Everything is a type; a value is a type with exactly one inhabitant" (§1) stays, as the source
  says it; it is settled.
- The semantic criterion of dependence (§4) with its grade "witnessed": write it with "cases with
  a witness" (D-2026-10-12-y) and `[proposed]`, since it is not implemented.
- §6 (reports that do not reject) as statements `4.Sk` with status.
- §8 (the example) stays, as a worked example at the end of the rules, before `## Open`.
- L14: state, `[proposed]`, that R1 to R13 are the laws of a theory `WellFormed : Program ->
  Failures E` over the `Program` data of `spec 3`, to be written in `lib/program.lut`, with the
  accept and reject programs as its cases.
- `## Open`: O2 (the setoid base case, R8), O9 (the kind of a hole in the elaborated form), O8
  (the session), and the "decided without an id" items by name.

## Length

The source's §1 to §6 and §8 are about 4000 words; the chapter should be about that. Keep every
rule's words where it is implemented.
