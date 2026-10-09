# Control: python, from memory (no corpus), 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/python/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 4 | 0 | 3 | yes |

## Candidates

- **C1** (hit): There should be one, and preferably only one, obvious way to do something, so that code converges on shared idioms rather than diverging into clever variants.
  - states reference Z13: There should be one-- and preferably only one --obvious way to do it. *(one obvious way to do it)*
- **C2** (hit): Readability counts: code is read far more often than it is written, so the language should make the reader's job easy even at the writer's expense.
  - states reference Z7: Readability counts. *(readability counts)*
- **C3** (hit): Explicit is better than implicit, and simple is better than complex, so behavior should be stated plainly rather than hidden in magic.
  - states reference Z2: Explicit is better than implicit. *(explicit over implicit)*
  - states reference Z3: Simple is better than complex. *(simple over complex)*
- **C4** (neither): Executable pseudocode: the language should be clean and uncluttered enough that well-written code looks like the description of the algorithm itself.
- **C5** (neither): Batteries included: a broad standard library ships with the language so common tasks need no external machinery.
- **C6** (neither): We are all consenting adults: the language favors convention and trust over enforced access restrictions, leaving the programmer responsible rather than locked out.
- **C7** (hit): Practicality beats purity: real-world usefulness takes precedence over theoretical consistency, and special cases are tolerated when they genuinely help.
  - states reference Z9: Although practicality beats purity. *(practicality beats purity)*

## Reference items no candidate states (33 of 38)

G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13, G14, G15, Z1, Z4, Z5, Z6, Z8, Z10, Z11, Z12, Z14, Z15, Z16, Z17, Z18, Z19, A1, A2, A3, A4
