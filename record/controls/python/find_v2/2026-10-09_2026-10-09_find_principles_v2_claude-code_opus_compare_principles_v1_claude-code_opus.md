# Control: python, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 4 | 0 | 3 | yes |

## Candidates

- **C1** (neither): Make every object that can be named a first-class citizen with equal status: assignable, passable, storable, callable. (instead of: reserving special status for functions, classes or types so some things can be named but not handled like the rest)
- **C2** (hit): Never return an undefined or silently wrong value; raise an exception whenever no correct result can be computed. (instead of: returning sentinels, undefined values or silently wrapped results that let an error pass unnoticed)
  - states reference G13: At the same time, errors should not pass silently. *(errors not silent, raise instead)*
  - states reference G14: A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter. *(no undefined behavior/result)*
  - states reference Z10: Errors should never pass silently. *(errors never pass silently)*
- **C3** (hit): Don't make users care about uninteresting implementation details. (instead of: requiring markers, suffixes or declarations that exist only to serve the implementation)
  - states reference G9: Don't bother users with details that the machine can handle. *(don't bother users with machine-handled details)*
- **C4** (hit): When several types share operations, generalize them to one common concept so the same operations work the same on all. (instead of: giving each type its own separate operations with their own names and behavior)
  - states reference Z8: Special cases aren't special enough to break the rules. *(no special cases, uniform rules)*
- **C5** (hit): Prefer the minimal solution that reuses existing constructs; don't add new syntax when an existing one will do. (instead of: inventing dedicated syntax for each new feature (a method keyword, operator declarations, a metaclass clause))
  - states reference G2: "Things should be as simple as possible, but no simpler." (Einstein) *(as simple as possible, minimal)*
  - states reference Z3: Simple is better than complex. *(simple better than complex)*
- **C6** (neither): Make a value's printed representation an expression that is valid input to the parser. (instead of: printing values in an ad-hoc display form that can't be read back as code)
- **C7** (neither): Choose the convention whose invariant makes the common cases come out clean, without +1/-1 corrections. (instead of: 1-based indexing with closed intervals that force awkward +1/-1 compensation on everyday slicing)

## Reference items no candidate states (31 of 38)

G1, G3, G4, G5, G6, G7, G8, G10, G11, G12, G15, Z1, Z2, Z4, Z5, Z6, Z7, Z9, Z11, Z12, Z13, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3, A4
