# Control: haskell, the blind filter, 2026-10-10

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 4 | 1 | 2 | no |

## Candidates

- **C1** (hit): L is non-strict, purely functional with lazy (call-by-need) evaluation as its defining core, embracing both the power (infinite structures, elegant combinators) and the cost (unpredictable space and evaluation order) that laziness brings.
  - states reference H1: Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design." *(laziness as defining theme)*
- **C2** (hit): Purity, meaning no side effects, is held to firmly, which makes controlled handling of effects (I/O, state, exceptions) through monads the central design achievement and L's conscious long-term bet.
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(purity, no side effects)*
- **C3** (hit): Type classes, with their generalisations to higher kinds (constructor classes), multi-parameter classes, and functional dependencies, are L's most distinctive feature after laziness and the principled solution to overloading.
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(type classes, most distinctive)*
- **C4** (neither): L has strong static polymorphic typing with Hindley-Milner inference, inherited from ML via Miranda and extended anarchically into a laboratory for type-system research.
- **C5** (leak): Algebraic data types defined as a sum of products, together with top-to-bottom left-to-right pattern matching, are fundamental to the language and its readability.
  - echoes Luthier F12: Dependent types, a universe, structural and nominal types, `data` as initial algebras. *(data as initial algebras)*
- **C6** (neither): Syntax was treated as the user interface and worked very hard: layout/offside rule, infix operators and sections, currying by juxtaposition, few keywords, aiming for programs that look like mathematics and read nicely.
- **C7** (hit): L was built by committee as a conservative common standard embodying consensus (ideally tried-and-true ideas) to unite the scattered lazy-functional community, with stability (L 98) and a growing community taken as both goal and measure of success.
  - states reference H5: Haskell is a committee language (3.5, line 720). *(committee language)*
  - states reference H7: Haskell and Haskell 98 (3.7, line 817): "The goal of using Haskell for research demands evolution, while using the language for teaching and applications requires stability." *(stability goal)*
  - states reference C5: It should be based on ideas that enjoy a wide consensus. *(wide consensus)*
  - states reference C6: It should reduce unnecessary diversity in functional programming languages. *(reduce diversity, unite community)*

## Reference items no candidate states (6 of 13)

H4, H6, C1, C2, C3, C4
