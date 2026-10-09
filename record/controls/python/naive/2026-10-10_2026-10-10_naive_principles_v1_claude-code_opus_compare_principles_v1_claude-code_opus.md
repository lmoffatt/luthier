# Control: python, the blind filter, 2026-10-10

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 6 | 0 | 1 | yes |

## Candidates

- **C1** (hit): Python is dynamically typed: the compiler ignores declarations and all type checking happens at run time, a deliberate corner-cutting simplification that stays safe because every type error is still caught before the interpreter can malfunction.
  - states reference G14: A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter. *(type errors never corrupt the interpreter)*
- **C2** (hit): Prefer the simplest possible implementation and let features fall out of it rather than be specially designed in, cutting corners wherever the gap to a fuller design is small.
  - states reference G2: "Things should be as simple as possible, but no simpler." (Einstein) *(as simple as possible)*
  - states reference G6: Don't try for perfection because "good enough" is often just that. *(good enough suffices)*
  - states reference G7: (Hence) it's okay to cut corners sometimes, especially if you can do it right later. *(okay to cut corners)*
  - states reference Z3: Simple is better than complex. *(simple better than complex)*
- **C3** (neither): Everything nameable in Python (functions, classes, methods, modules, types, even the type structure itself) is a first-class, introspectable object that can be passed around, stored, and inspected at run time.
- **C4** (hit): Errors are handled through exceptions and no operation ever returns a silently undefined value: when no correct result can be computed, an exception is raised rather than letting a bad value pass.
  - states reference G13: At the same time, errors should not pass silently. *(errors should not pass silently)*
  - states reference Z10: Errors should never pass silently. *(errors never pass silently)*
- **C5** (hit): Syntax should be clean and human-readable, using indentation (with a clarifying colon) for grouping instead of braces, so program text looks neat and suggests its meaning.
  - states reference G15: Punctuation characters should be used conservatively, in line with their common use in written English or high-school algebra. *(conservative punctuation)*
  - states reference Z1: Beautiful is better than ugly. *(beautiful over ugly)*
  - states reference Z7: Readability counts. *(readability counts)*
- **C6** (hit): Don't make users care about uninteresting implementation details: unify related concepts (sequences, numbers, statements) into a single general mechanism that behaves consistently.
  - states reference G9: Don't bother users with details that the machine can handle. *(don't bother users with handled details)*
  - states reference Z8: Special cases aren't special enough to break the rules. *(special cases don't break rules)*
- **C7** (hit): Preserve backwards compatibility and evolve the language gradually, introducing changes through opt-ins (from __future__), deprecation campaigns, and reluctantly added keywords.
  - states reference A4: An evolutionary path with user participation, users encouraged to look under the hood (ABC was "a closed system"). *(evolutionary path with user participation)*

## Reference items no candidate states (25 of 38)

G1, G3, G4, G5, G8, G10, G11, G12, Z2, Z4, Z5, Z6, Z9, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3
