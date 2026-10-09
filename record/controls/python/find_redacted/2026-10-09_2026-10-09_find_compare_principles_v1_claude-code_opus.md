# Control: python, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 3 | 0 | 4 | no |

## Candidates

- **C1** (hit): When no correct value can be computed, raise an exception; never return an undefined value or let an error pass silently.
  - states reference G13: At the same time, errors should not pass silently. *(errors not pass silently)*
  - states reference G14: A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter. *(no undefined behavior)*
  - states reference Z10: Errors should never pass silently. *(errors never pass silently)*
- **C2** (neither): Every object that can be named has equal status: it can be assigned, passed, returned and stored like any other.
- **C3** (hit): Prefer the minimal solution that reuses existing mechanisms; do not add new syntax when an existing construct will serve.
  - states reference G2: "Things should be as simple as possible, but no simpler." (Einstein) *(as simple as possible)*
  - states reference Z3: Simple is better than complex. *(simple better than complex)*
- **C4** (neither): Variables are names that refer to objects, needing no declaration; all type checking happens at run time.
- **C5** (neither): Every value, when printed or converted to a string, should read back as a valid expression to the parser.
- **C6** (neither): Generalize related types to a common concept so core operations work the same on all of them.
- **C7** (hit): Do not require users to care about uninteresting implementation details.
  - states reference G9: Don't bother users with details that the machine can handle. *(don't bother users with handled details)*

## Reference items no candidate states (32 of 38)

G1, G3, G4, G5, G6, G7, G8, G10, G11, G12, G15, Z1, Z2, Z4, Z5, Z6, Z7, Z8, Z9, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3, A4
