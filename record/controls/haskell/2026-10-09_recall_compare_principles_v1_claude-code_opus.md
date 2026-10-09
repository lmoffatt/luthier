# Control: haskell, from memory (no corpus), 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 5 | 0 | 2 | yes |

## Candidates

- **C1** (hit): The language should be purely functional, with no side effects in the language's core, so that a function's result depends only on its arguments.
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(purity, no side effects)*
- **C2** (hit): Lazy (non-strict) evaluation is the default, computing values only when needed, which keeps the language pure and enables modular programming with infinite data structures and separation of generation from control.
  - states reference H1: Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design." *(laziness is the default)*
- **C3** (neither): Side effects and interaction with the world are made explicit and controlled through types, using monads so that effectful computations are first-class values the type system tracks.
- **C4** (neither): A strong, static type system with Hindley-Milner type inference and principal types catches errors at compile time while rarely requiring the programmer to write types.
- **C5** (hit): Type classes provide principled, systematic overloading (ad hoc polymorphism), letting the same name denote operations across many types with constraints resolved by the compiler.
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(type classes, overloading)*
- **C6** (hit): The language should be a general-purpose, standardized common vehicle that unifies the fragmented community of non-strict functional language researchers around one design.
  - states reference C1: It should be suitable for teaching, research, and applications, including building large systems. *(general-purpose use)*
  - states reference C5: It should be based on ideas that enjoy a wide consensus. *(based on wide consensus)*
  - states reference C6: It should reduce unnecessary diversity in functional programming languages. *(reduce diversity, unify community)*
- **C7** (hit): Referential transparency and equational reasoning are preserved so that programs can be understood, transformed, and proved correct by substituting equals for equals.
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(purity gives referential transparency)*

## Reference items no candidate states (7 of 13)

H4, H5, H6, H7, C2, C3, C4
