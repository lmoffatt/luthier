# Control: haskell, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 4 | 0 | 3 | yes |

## Candidates

- **C1** (hit): Control effects on principle and make them explicit, even at the cost of convenience. (instead of: effects by default, unrestricted side effects)
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(purity is controlling effects on principle)*
- **C2** (neither): Capture any notion of computation as an abstract value you sequence, rather than wiring each effect into the language. (instead of: a single built-in notion of computation and sequencing)
- **C3** (hit): Solve overloading with one principled general mechanism, constraints on types, rather than ad hoc special cases. (instead of: ad hoc operator overloading)
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(type classes as principled overloading)*
- **C4** (hit): Keep the language referentially transparent so programs read as executable mathematics. (instead of: programs as sequences of state changes)
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(referential transparency = purity)*
- **C5** (neither): Make notation follow mathematical usage and the reader's eye. (instead of: the syntactic tradition of other programming languages)
- **C6** (neither): Prefer the simplest expression that carries the complexity, the form that recurs naturally across problems. (instead of: bespoke machinery built per problem)
- **C7** (hit): Embody tried-and-true consensus rather than break new ground. (instead of: including novel, unproven features)
  - states reference C5: It should be based on ideas that enjoy a wide consensus. *(based on wide consensus)*

## Reference items no candidate states (10 of 13)

H1, H4, H5, H6, H7, C1, C2, C3, C4, C6
