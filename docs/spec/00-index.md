# The specification of Luthier

Twelve chapters, one document (settled 2026-10-12; `record/plan-spec-2026-10-12-decisions.md`,
D-2026-10-12-y). It describes the language designed, not only what runs: every rule and every
statement carries its status. The principles it realizes are `docs/principles.md`; the record of
how each chapter was written is `record/spec-drafts.md`.

## How to read a rule

A rule is `**N.Rk. Title.** [status] text. Files: a.accept.lut, b.reject.lut.`, where N is the
chapter, k the rule's number in it, and the files are programs in `tests/spec/` that the checker
must accept and reject. A statement, `**N.Sk.**`, is a behaviour no single program decides. The
status is one of:

- `[implemented]`: in the interpreter, with its two programs passing; a rule of evaluation also
  needs a program whose value is compared (D-2026-10-12-ah);
- `[decided D-YYYY-MM-DD-x]`: taken by that entry of `record/decisions.md`, not yet implemented;
- `[proposed]`: the model's, awaiting Luciano's mark.

Citations: `spec 4.R3` is rule 3 of chapter 4, `spec 8 §2` section 2 of chapter 8; `L5`, `L5.3`,
`G1`, `O3` are entries, clauses, organizers and open questions of `docs/principles.md`;
`D-2026-10-11-c` a decision; `W5` the way of working; `P11` the method. `scripts/check_spec.py`
verifies that every citation resolves, that every item has a status, that implemented rules have
their programs, and that no run of eight words is repeated across chapters or copied from the
principles.

## The chapters

| Chapter | Realizes | Status |
|---|---|---|
| [1. Terms and notation](01-terms.md) | Terms of the principles | draft 0, 2026-10-12 |
| [2. Grammar](02-grammar.md) | L7 | draft 0, 2026-10-12 |
| [3. Kernel](03-kernel.md) | L7, L14 | draft 0, 2026-10-12 |
| [4. Static semantics](04-static-semantics.md) | L2, L8 | draft 0, 2026-10-12 |
| [5. Laws](05-laws.md) | L12, L3 | wave 2 |
| [6. Certification](06-certification.md) | L9, L10 | wave 2 |
| [7. Tests and generators](07-tests.md) | L10.3, L5.18 | draft 0, 2026-10-12 |
| [8. The demand and the plan](08-demand.md) | L5 | wave 3 |
| [9. Specimens and the planner](09-planner.md) | L6 | wave 3 |
| [10. Actions and the world](10-world.md) | L4, L11 | wave 3 |
| [11. Numbers](11-numbers.md) | L13 | draft 0, 2026-10-12 |
| [12. Files and tools](12-files-and-tools.md) | L5, L10, L14 | draft 0, 2026-10-12 |

The six files of 2026-10-04 to 2026-10-11 (`02` grammar, `03` libraries, `04` kernel, `05` static
semantics, `06` numbers, `08` tests) were replaced by chapters 2, 12, 3, 4, 11 and 7 on 2026-10-12;
git keeps them, and `record/spec-drafts.md` says what each chapter took from them.
