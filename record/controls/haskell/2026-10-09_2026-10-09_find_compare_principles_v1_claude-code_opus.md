# Control: haskell, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 3 | 0 | 4 | no |

## Candidates

- **C1** (hit): Keep the language pure and make every effect explicit in the type of a computation.
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(Haskell is pure)*
- **C2** (hit): Evaluate lazily, so that evaluation order follows need and infinite structures are ordinary values.
  - states reference H1: Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design." *(Haskell is lazy)*
- **C3** (neither): Because of referential transparency a program can be read as executable mathematics, equations whose specification is the program.
- **C4** (neither): Model a computation that may have effects as a first-class value of type IO a (or any monad), sequenced by bind.
- **C5** (hit): Resolve ad-hoc overloading in a principled way through type classes, constraints that qualify a polymorphic type.
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(type classes for overloading)*
- **C6** (neither): Write a library that turns the language into a domain-specific embedded language sharing its syntax, types and tools.
- **C7** (neither): Make expressions look as much like mathematics as possible, with infix operators from day one.

## Reference items no candidate states (10 of 13)

H4, H5, H6, H7, C1, C2, C3, C4, C5, C6
