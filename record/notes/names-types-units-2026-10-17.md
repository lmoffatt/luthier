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

## Points, balls and the finite map to the infinite (2026-10-18)

*Candidate for the principles: to be weighed for a clause (with D-2026-10-18-c, the three planes and
the tower cut by the demand).*

11. (his) One sees points, never lines or surfaces; a bound is a ball in the space, but parametrized
    by a pair of points: a map from the finite to the infinite, much used in category theory.
    (proposed) Four precise forms of it:
    - Generalized elements and Yoneda: an object is known by the arrows into it from test objects
      (a point is an arrow 1 → X); it is determined by all its probes.
    - Presentations and colimits: a finitely presented object (`List A`, the free monoid: two finite
      rules, an infinite set); every set is the filtered colimit of its finite subsets.
    - Point-free topology (Stone; Vickers, *Topology via Logic*, 1989): an open is a property
      confirmable from finite information; a ball with rational centre and radius is a basic open,
      an infinite set named by finite data.
    - Ball and interval arithmetic (Arb, Fredrik Johansson), computable analysis: a real is held as a
      ball that contains it, two machine numbers; L5.4 already foresees running code over intervals.
    In Luthier: theories speak of infinite objects; computation touches only points (a test draws
    points, a certificate is finite evidence of an infinite claim); a cutoff is a ball, an infinite
    object with a finite name, so the verdict can be Boolean ("does the point fall in the ball?");
    the demand chooses the probes and the ball.
12. (his) Finite theories about the infinite are nothing but abstaining from fixing a maximal bound;
    then the number of finite explorers is what the budget allows. The new point: how the budget
    scales with the bounds, which is what the laws of algorithms should say. (Taken up in
    D-2026-10-18-d if registered.)

## Topology, computability and the fourth level (2026-10-18)

*Exploration, nothing decided; partly candidate for the principles with items 11 and 12.*

13. (his) No three without four: what would generalize the probabilistic level? (proposed, then
    corrected by him) The observer's budget (computational indistinguishability), Bayesian evidence
    and bisimulation are other axes, not a level that contains the probabilistic one as a degenerate
    case (his criterion: equivalence is a metric with values 0 and ∞, a metric is a probabilistic
    metric with Dirac distributions). The candidate that does contain it is imprecise probability
    (a p-box, Ferson; lower and upper probabilities, Walley 1991; Dempster-Shafer). (his) It has no
    notable property that justifies including it. (proposed) It is not a fourth level of equality but
    the shape of the evidence about the third: ε̂ of L10.3 is an upper probability, the ternary
    verdict of D-2026-10-15-b falls out of a band, a Kolmogorov band around an empirical
    distribution (Dvoretzky-Kiefer-Wolfowitz) is a p-box.
14. (his) Something topological, but the topological lives in Boolean: it collapses metrics to
    integers; and it is also an operation to descend to a computable level. (proposed) An open is a
    predicate (point-free topology, geometric logic); the invariants are integers that survive
    deformation (winding numbers, Betti numbers, Euler characteristic), classes of an equivalence
    (homotopy), so topology re-enters level 1 as a coarser equivalence (HoTT's paths). Equality of
    reals is not computable, x < y is semidecidable, every computable function on the reals is
    continuous (Brouwer; Weihrauch): an open is a semidecidable property (Smyth 1983; Abramsky;
    Vickers), topology the logic of what is observable. A cutoff is the descent to the computable,
    and its price is a band at the boundary ("d < ε or d > ε/2" is decidable, "d ≤ ε" is not): the
    ternary verdict appears whenever one descends from the continuum, not only in statistics. In
    Luthier: `unseenDirections` collapses singular values to an integer by the rank floor; the rank
    of a real matrix is not computable, the rank with a floor is, unstable at the floor (the cases
    1e-13 and 1e-16 of `PinvProjects`); persistent homology is the general form (Betti numbers per
    scale, stable under the bottleneck distance: Cohen-Steiner, Edelsbrunner and Harer 2007).
15. (his) Perhaps something of topos would generalize probability, but the integration of topos and
    probability has not been done well. (proposed, from memory, to be checked) The obstruction:
    measurable spaces are not Cartesian closed (Aumann 1961). Lines of work: quasi-Borel spaces
    (Heunen, Kammar, Staton and Yang, LICS 2017, a quasitopos for higher-order probability); Markov
    categories (Fritz 2020); valuations on opens (Jones and Plotkin's probabilistic powerdomain,
    1989; constructive measure theory on locales, Coquand and Spitters): probability assigned only to
    observable properties, computable by construction, the line that fits Luthier; probability
    sheaves (Simpson, 2017); the quantum topos (Döring and Isham; Heunen, Landsman and Spitters).
