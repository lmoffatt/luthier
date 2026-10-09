# Control: python, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 3 | 0 | 4 | no |

## Candidates

- **C1** (neither): Give every nameable thing equal status, assignable, passable and storable, rather than privileging some kinds of object. (instead of: privileged built-ins that can't be passed or stored like ordinary values)
- **C2** (hit): When no correct value can be computed, raise rather than return an undefined or silently clipped result, and reject inconsistent constructions outright. (instead of: silent sentinels, truncation or undefined behavior as in C)
  - states reference G13: At the same time, errors should not pass silently. *(don't clip silently)*
  - states reference G14: A bug in the user's Python code should not be allowed to lead to undefined behavior of the Python interpreter. *(no undefined behavior/result)*
  - states reference Z10: Errors should never pass silently. *(errors never pass silently)*
  - states reference Z12: In the face of ambiguity, refuse the temptation to guess. *(refuse to guess, reject inconsistent)*
- **C3** (neither): Make a value's printed form a valid expression that reconstructs it, rather than a free-form description. (instead of: arbitrary, unparseable string descriptions of objects)
- **C4** (neither): Index from zero with half-open intervals and suitable defaults so adjacent slices meet without off-by-one corrections. (instead of: 1-based closed intervals needing +1/-1 adjustments)
- **C5** (hit): Make the instance an explicit first argument and explicit attribute access the only way to reach its state, rather than implicit resolution. (instead of: implicit this and hidden instance-variable lookup as in C++)
  - states reference Z2: Explicit is better than implicit. *(explicit over implicit)*
- **C6** (neither): Generalize related types under a shared concept so the same core operations work uniformly across them, rather than per-type operations. (instead of: separate, incompatible operations for each container type)
- **C7** (hit): Prefer the minimal solution that reuses existing syntax over introducing new syntax for a new feature. (instead of: adding dedicated grammar for each new capability)
  - states reference G2: "Things should be as simple as possible, but no simpler." (Einstein) *(as simple as possible)*
  - states reference Z3: Simple is better than complex. *(simple over complex)*

## Reference items no candidate states (31 of 38)

G1, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G15, Z1, Z4, Z5, Z6, Z7, Z8, Z9, Z11, Z13, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3, A4
