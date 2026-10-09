# Control: haskell, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 3 | 0 | 4 | no |

## Candidates

- **C1** (neither): Control effects on principle and make them explicit, against the mainstream default of effects everywhere.
- **C2** (hit): Because of referential transparency, a program can be read and manipulated as mathematics.
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(referential transparency is purity)*
- **C3** (hit): Evaluate lazily, embracing infinite structures and abstraction from evaluation order as the language's organising choice.
  - states reference H1: Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design." *(both: evaluate lazily)*
- **C4** (neither): Model a computation as a first-class value with return and bind, so effects can be captured and sequenced abstractly.
- **C5** (hit): Resolve overloading on principle through type classes, typing a value for any type that is an instance of a class.
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(overloading via type classes)*
- **C6** (neither): Seek solutions that feel like minimal surfaces: the simplest expression that spans the needed complexity.
- **C7** (neither): Make expressions look as much like mathematics as possible.

## Reference items no candidate states (10 of 13)

H4, H5, H6, H7, C1, C2, C3, C4, C5, C6
