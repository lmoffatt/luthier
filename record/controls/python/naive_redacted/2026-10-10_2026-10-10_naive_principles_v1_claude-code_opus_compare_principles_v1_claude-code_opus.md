# Control: python, the blind filter, 2026-10-10

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 5 | 0 | 2 | yes |

## Candidates

- **C1** (hit): L is dynamically typed: variables are untyped names bound to objects and all type checking happens at run time rather than at a separate compile step, a deliberate corner-cutting simplification that keeps safety because every type error is still caught before the interpreter can malfunction.
  - states reference G7: (Hence) it's okay to cut corners sometimes, especially if you can do it right later. *(cut corners, fix later)*
  - states reference G14: A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter. *(user bug no interpreter undefined behavior)*
- **C2** (neither): Every object nameable in L (integers, strings, functions, classes, methods, modules, types) is first-class with equal status, assignable, passable, storable and introspectable at run time, made uniform by basing all objects on one common C structure whose type is itself a run-time object.
- **C3** (hit): The implementation consistently chooses the simplest design that works, cutting corners and letting useful features fall out of the mechanism rather than being designed in, even for subsystems like classes added late as an afterthought.
  - states reference G2: "Things should be as simple as possible, but no simpler." (Einstein) *(as simple as possible)*
  - states reference G6: Don't try for perfection because "good enough" is often just that. *(good enough)*
  - states reference G7: (Hence) it's okay to cut corners sometimes, especially if you can do it right later. *(cut corners)*
  - states reference Z3: Simple is better than complex. *(simple better than complex)*
- **C4** (hit): Errors are handled through exceptions rather than undefined or silently-clipped results: no operation returns an undefined value, an exception is always raised when no correct value can be computed, and inconsistent situations are rejected rather than resolved silently.
  - states reference G12: Errors should not be fatal. *(errors not fatal via exceptions)*
  - states reference G13: At the same time, errors should not pass silently. *(errors not silent)*
  - states reference Z10: Errors should never pass silently. *(errors never pass silently)*
  - states reference Z12: In the face of ambiguity, refuse the temptation to guess. *(refuse to guess, reject ambiguity)*
- **C5** (neither): A data type's printed representation should be a valid parser input that reconstructs it, and related indexable types are unified under common abstractions (the sequence; half-open 0-based slicing) so operations behave uniformly and compose without off-by-one corrections.
- **C6** (hit): Syntax uses indentation for grouping with a colon introducing the block, inherited from the predecessor B, dispensing with braces and semicolons, while borrowing keywords and operator meanings from C and Algol-family languages.
  - states reference G1: Borrow ideas from elsewhere whenever it makes sense. *(borrow from B and Algol/C)*
  - states reference G15: Punctuation characters should be used conservatively, in line with their common use in written English or high-school algebra. *(punctuation conservative)*
- **C7** (hit): The language evolves without needlessly breaking working code: new built-ins and features are added back-compatibly (new keywords only reluctantly, via __future__ opt-ins and deprecation), favoring the designer's own coding time and users' existing code over premature optimization.
  - states reference G4: Don't fret too much about performance--plan to optimize later when needed. *(optimize later, not premature)*
  - states reference A4: An evolutionary path with user participation, users encouraged to look under the hood (ABC was "a closed system"). *(evolutionary path, back-compat)*

## Reference items no candidate states (25 of 38)

G3, G5, G8, G9, G10, G11, Z1, Z2, Z4, Z5, Z6, Z7, Z8, Z9, Z11, Z13, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3
