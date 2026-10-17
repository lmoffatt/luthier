# Names, types, equivalences and units: an exploration, 2026-10-16/17

A dialogue between Luciano and the decision-assistant fork of the coordinating session, on item 26 of
`record/plan/decisions-pending-2026-10-15.md` (D-2026-10-17-a: the names of a record's fields are
part of its type). Nothing here is decided beyond D-2026-10-17-a; marked: (his) for what Luciano said,
(proposed) for the assistant's readings.

## The path of the dialogue

1. (his) Names are part of the type; is `Point = { x : Float64, y : Float64 }` equivalent to
   `Float64 * Float64`? If it has no more structure, should `Point` exist as a name? With more
   structure, a forgetful and a free functor; with a predicate, no, since a predicate reduces.
2. (proposed) Property, structure, stuff (Baez and Shulman): forgetting a property (a predicate, a
   subtype, L8) is full and faithful, an inclusion, with no free functor in general; forgetting a
   structure (operations with laws, a theory on the carrier) is faithful, not full, with a free
   left adjoint when the theory has free objects (`List` the free monoid).
3. (his) No keyword is needed for a labeled type without laws: that is what an alias is. But the
   type has names for its accessors; and one wants, for clarity, to give x and y particular names.
4. (his) This is the first example of what Luthier must do naturally: handle equivalences.
   (proposed) An isomorphism is not unique (`{ x, y }` against `{ lat, lon }`: two of them), so an
   equivalence is a datum with a name, not a fact deduced (HoTT: equivalence is structure).
5. (his) In his C++ library `var`, fields of a cartesian product were accessed by name: an
   equivalence with the product. Is the alias two things, a new type and an equivalence with the
   product? (proposed) The `newtype` pattern; forgetting the name implicit, giving it explicit.
6. (his) Normally one declares the type, then defines it (L2); why would a type have no law beyond
   its accessors? (proposed) It has the product's laws on named projections (D-2026-10-13-x:
   `PairFst`, `PairSnd`, `Pairing` with names); then the equivalence with the product is a theorem,
   the universal property, unique once the projections are fixed.
7. (his) Not clear yet. Second, metre, kilogram: what are they, to which type do they belong?
   (proposed) Values, not types: chosen elements (bases) of the dimension types Time, Length, Mass,
   each a one-dimensional real vector space (Tao, "A mathematical formalisation of dimensional
   analysis", 2012); 3 m is 3 times the value metre; a change of unit is a change of basis.
8. (his) How do we map this to type theory, categories, HoTT? (proposed)
   - Types: `Dim` the free abelian group on L, T, M; `Q : Dim -> U`; `+` within one `Q d`;
     `* : Q d -> Q e -> Q (d + e)`; `Q 0 ≅ ℝ`; a unit `metre : Q L` gives `Q L ≃ ℝ`.
   - Categories: each `Q d` a real line, isomorphic to ℝ but not canonically; `Q` a monoidal
     functor (`Q d ⊗ Q e ≅ Q (d + e)`); a system of units a trivialization, the choices a torsor
     under the rescalings; a law of physics a natural (equivariant) transformation, Buckingham's π
     theorem its consequence. Precedent: F# units of measure (Kennedy).
   - HoTT: `Line := Σ (V : U), ‖V ≃ ℝ‖`, merely equivalent to ℝ; choosing a unit removes the
     truncation; by univalence `Length = ℝ` along many paths, and transport along different paths
     gives different numbers: conversion of units. The type of lines is B(ℝ^×).
   - The two cases told apart by how many equivalences exist: `Point` (contractible: one, once the
     projections are fixed; a field name is a projection, no choice) against `Length` (a torsor:
     one per unit; a field `{ m : Float64 }` is the choice of a unit). A bare `Float64` is a
     coordinate without its basis.
9. (his) A name has no extra information, only that it is distinct: isomorphic to `Unit`?
   (proposed) Yes at the level of values (`{ x : Float64 } ≅ Unit × Float64 ≅ Float64`, a phantom
   tag); univalence would erase it (`Tag_x = Unit = Tag_y`), so Luthier keeps names at the strict
   level, finer than univalent equality (two-level type theory, D-2026-10-15-e). A unit carries more
   than distinction: a scale relative to the other units, in the type, not in the value.
10. (his) Declaring `metre`, `second` declares them distinct implicitly; they are types without
    semantics yet; when do time, space and mass stop being isomorphic? (proposed) Three stages:
    names or bare lines, isomorphic (even the dimension group has the automorphism swapping L and
    T); with laws that treat them differently (space three-dimensional with a metric and O(3), time
    oriented, mass positive, extensive and conserved; ½mv², Gm₁m₂/r²), no longer isomorphic; with a
    universal constant of dimension d1 − d2, canonically isomorphic again (c: t ↦ c·t; Planck units
    collapse every dimension). Constants of nature are named equivalences between types; which
    magnitudes are comparable is decided by the laws and constants a theory declares.

## What it suggests for Luthier (proposed, nothing decided)

- A name distinguishes (strict level); laws give the structure, which may break an isomorphism;
  a declared equivalence (a universal property, or a constant) identifies, canonically.
- A record with named fields declares a theory whose laws are the product's on named projections,
  defined by its representation; its equivalence with the product is its universal property.
- A quantity's type is its dimension, `Q d`, not `Float64`; units are values; a number enters with
  `3.0 * metre` and leaves with `q / metre`; laws stated over `Q` are unit-invariant by
  construction (P10: the invariant of the type).
- Equivalences between types (not only between specimens, L6, L10.7) are named values with their
  kind (exact derivable, exact certified, approximate) and certificates transport along them; a gap
  in the principles (L3 says equality has levels; nothing on type equivalences).
