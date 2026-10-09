# Control: haskell, the blind filter, 2026-10-09

Written by `scripts/compare_principles.py` (compare_principles v1); judge prompt `compare_principles_v1` (sha256 a69f0e1f6e17),
model opus at effort low. List A is `record/controls/haskell/reference.md`; list B is Luthier's P1 to P14 and F1 to F16;
the judge was not told which is which. Rules fixed in record/controls/README.md before any run.

| candidates | hits | leaks | neither | passes |
|---|---|---|---|---|
| 7 | 4 | 0 | 3 | yes |

## Candidates

- **C1** (hit): Keep the language pure and make every effect explicit in the types, rather than allowing effects by default. (instead of: effects-by-default)
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(keeping the language pure)*
- **C2** (hit): Evaluate lazily by default, so values are computed only when needed and infinite structures and new abstractions become ordinary. (instead of: strict, call-by-value evaluation)
  - states reference H1: Haskell is lazy (3.1, line 579): "Laziness was undoubtedly the single theme that united the various groups that contributed to Haskell's design." *(lazy by default)*
- **C3** (hit): Preserve referential transparency so programs read as equations, as executable mathematics where the specification can become the program. (instead of: programs as sequences of state-changing commands)
  - states reference H2: Haskell is pure (3.2, line 610): "Haskell is, therefore, a pure language"; "laziness kept us pure" (line 637). *(referential transparency is purity)*
- **C4** (hit): Solve overloading with a principled, type-directed abstraction of classes and instances, not ad hoc special-casing. (instead of: ad hoc operator overloading)
  - states reference H3: Haskell has type classes (3.3, line 639): overloading, "now regarded as Haskell's most distinctive characteristic". *(type classes for overloading)*
- **C5** (neither): Model effects and other notions of computation as first-class values, reasoning about computations abstractly rather than wiring their details by hand. (instead of: built-in, hard-wired notions of sequencing and effects)
- **C6** (neither): Build abstractions as combinator libraries that turn the language itself into a domain-specific language, instead of inventing a new language and tooling each time. (instead of: writing a standalone parser, type checker and interpreter per domain)
- **C7** (neither): Prefer solutions that are minimal surfaces: simple expressions carrying significant complexity, in forms that feel natural and recur across problems. (instead of: accidental complexity and one-off special forms)

## Reference items no candidate states (10 of 13)

H4, H5, H6, H7, C1, C2, C3, C4, C5, C6
