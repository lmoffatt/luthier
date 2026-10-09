# Control: python, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 2 | 0 | 5 | no |

## Candidates

- **C1** (neither): Every object that can be named has equal, first-class status: assignable, passable, storable, including types themselves.
- **C2** (neither): Variables are names referring to objects, needing no declaration, and all type checking happens at run time.
- **C3** (neither): Statements are grouped by indentation rather than by braces or keywords.
- **C4** (hit): There are no undefined result values: an exception is always raised when no correct value can be computed, and errors never pass silently.
  - states reference G13: At the same time, errors should not pass silently. *(errors should not pass silently)*
  - states reference G14: A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter. *(no undefined behavior from user bug)*
  - states reference Z10: Errors should never pass silently. *(errors never pass silently)*
- **C5** (neither): A method is just a function whose first argument, by convention self, is the instance; explicit reference is the only way to reach instance variables.
- **C6** (hit): Prefer the minimal solution that reuses existing mechanisms over adding new syntax.
  - states reference G2: "Things should be as simple as possible, but no simpler." (Einstein) *(as simple as possible)*
  - states reference Z3: Simple is better than complex. *(simple better than complex)*
- **C7** (neither): Index from 0 with half-open intervals and suitable defaults, so common slices need no +1/-1 corrections.

## Reference items no candidate states (33 of 38)

G1, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G15, Z1, Z2, Z4, Z5, Z6, Z7, Z8, Z9, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3, A4
