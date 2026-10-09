# Control: haskell, the blind filter, 2026-10-10

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 5 | 0 | 2 | yes |

## Candidates

- **C1** (hit): Haskell is purely functional with no side effects, a firm commitment that made it radical and elegant and shaped the whole design.
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(pure language)*
- **C2** (hit): Haskell is non-strict, using lazy (call-by-need) evaluation, prized for its tie to the lambda calculus, infinite data structures, and elegant implementation.
  - states reference H1: Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design." *(laziness/non-strict)*
- **C3** (hit): Type classes, Haskell's most distinctive feature after laziness, provide principled overloading and became the framework into which a stream of type-system extensions fitted.
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(type classes, most distinctive)*
- **C4** (neither): Effects are made explicit and tamed through monads, especially the IO monad, which gives pure code a way to do input/output while keeping deterministic semantics.
- **C5** (hit): The language was designed by a committee aiming for a conservative, consensus language that united existing groups rather than breaking new ground.
  - states reference H5: Haskell is a committee language (3.5, line 720). *(committee language)*
  - states reference C5: It should be based on ideas that enjoy a wide consensus. *(based on wide consensus)*
  - states reference C6: It should reduce unnecessary diversity in functional programming languages. *(reduce diversity, unite groups)*
- **C6** (neither): Syntax was treated as the language's user interface and worked on very hard, with the aim that expressions look like mathematics and programs look nice.
- **C7** (hit): Haskell 98 marked a deliberate commitment to long-term stability after years of a frequently changing research vehicle, tentatively credited with the community's growth.
  - states reference H7: Haskell and Haskell 98 (3.7, line 817): "The goal of using Haskell for research demands evolution, while using the language for teaching and applications requires stability." *(stability vs evolution)*

## Reference items no candidate states (6 of 13)

H4, H6, C1, C2, C3, C4
