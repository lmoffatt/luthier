# Report: Agent K (core), a refuted model for every uncontrolled conjunct

2026-10-26, Claude Opus 5.5, on `prompt-controls.md` beside this file (03d45eb). Program touched:
tests/tester/core_controls.test.lut and its store. Commits e702573 (the 66 new lines) and 94b0192
(the stuck match). Logs under `~/.cache/luthier-controls/K/`: `check0.txt` (before),
`test1.txt`, `test2.txt` (`luthier test` on the controls program), `check2.txt` (after).

## Result

`luthier check -v tests/tester/core_laws.test.lut` before: 33 laws with uncontrolled conjuncts (the
tsv's 98, plus the `Commutative` conjuncts this file's own stores don't control, as D1's report
says of `MarkIsAMetric`). After: one law, `EmptyIsInitial`, conjunct `NoValue Empty model`.

`luthier test tests/tester/core_controls.test.lut`: exit 0, no CONTROL FAILED, and every new line
refutes the conjunct it is written for. Where a model breaks more than its target, the extra
refutations are listed below. Each premise is given a listed census inside the broken relation's
domain (a related pair, a chain), so no new conjunct depends on a rare draw.

## Per law: the controls added

Relations at Int (the instance bound to `r`, or `f` and `s`):
- IntEquivalence: `parityAwayFromZero` (parity, except that 0 relates to nothing) refutes Reflexive
  only; `near` refutes Transitive only.
- IntPreorder: `near`, Transitive only.
- IntPartialOrder: `less`, Reflexive only; `cyclic`, Transitive only.
- IntTotalOrder: `less`, Reflexive (and Total); `cyclic`, Transitive only; `always`, Antisymmetric
  only.
- IntStrictOrder: `cyclicStrict`, Transitive only.
- IntBijective: `half` with section `double`, Injective only.

`cyclic` is a tournament: for a < b, a relates to b when b − a is odd, otherwise b relates to a.
It is reflexive, total and antisymmetric, and 0, 1, 2 is a chain with 2 r 0 instead of 0 r 2.

Object (one line breaking symmetry with an order, one breaking transitivity with a tolerance):
- IntIsAnObject, NatIsAnObject, FloatIsAnObject: `x <= y` refutes Symmetric only; within 1 refutes
  Transitive only.
- StringIsAnObject: lexicographic `<=`, Symmetric only; "equal, or one of them empty", Transitive
  only.
- BoolIsAnObject: implication, Symmetric only; inequality, Transitive (and Reflexive: on two values
  a reflexive symmetric relation is always transitive).
- ListIsAnObject: by length `<=`, Symmetric only; lengths within 1, Transitive only. The old
  line's census lay outside the broken model's domain; the new lines carry their own.

Order (IntIsOrdered, NatIsOrdered, StringIsOrdered, FloatIsOrdered, BoolIsOrdered):
- A tournament refutes Transitive only (Int and Nat as above; Float, up within a unit and down
  beyond it; String, lexicographic with "" moved below "a" only). Bool has none, since every
  total antisymmetric reflexive relation on two values is an order, so inequality refutes
  Transitive there together with the other three.
- `always` (every pair related) refutes Antisymmetric only. That was the vacuous conjunct: under
  `leq := false` its premise never held.

Algebra:
- IntIsASemiring: `-` as the product refutes the product's Associative, Neutral, Distributive and
  Absorbing; one = 0 refutes Distinct (and the product's Neutral).
- IntIsACommutativeRing: `-` as the sum (sum's Associative, Neutral, plus Commutative and
  Invertible), `-` as the product (as for the semiring, plus Commutative), one = 0 (Distinct).
- NatIsAnOrderedSemiring, twelve lines. a + 2b as the sum: the sum's Associative and Neutral (and
  Commutative, Discrete). a·b² as the product: the product's Associative, Neutral and Distributive.
  a·b + 1 as the product: Absorbing (and the other product laws). one = 0: Distinct. one = 2:
  Discrete. `<`: Reflexive (and Total, Least, Discrete). The tournament: Transitive (and Least,
  Discrete). `always`: Antisymmetric only. Equality: Total (and Least). Evens before odds:
  MonotoneIn (and Discrete). Reversed order: Least only. Reversed order with a·b + 1:
  PositiveClosed, which can't fail alone, because where zero is least its conclusion `leq 0 _`
  always holds.
- StringIsAMonoid: concatenation with a mark after each join, Associative (and Neutral).
- BoolIsABooleanAlgebra and BoolIsTheBooleans, same three models: implication as the meet,
  implication as the join (together they refute both Associative, Commutative and Idempotent,
  Absorptive, both Neutral and both Distributive), and top = bottom (Distinct).

Metrics:
- IntIsAMetric: 1 + |x − y|, MetricZeroOnEqual only; 0 everywhere, MetricIndiscernible only; a step
  down costing twice a step up, Commutative only (a quasimetric); −|x − y|, MetricNonNegative (and
  Triangular: equality.lth notes the other laws imply non-negativity).
- BoolIsAMetric: 1 on the diagonal and 2 off it, MetricZeroOnEqual only; 1 one way and 2 the other,
  Commutative only; −1 on the diagonal, Triangular (and the diagonal and non-negativity: on two
  points the triangle holds whenever the diagonal is zero); −1 off the diagonal, MetricNonNegative
  (and Triangular).

Universal constructions:
- BoolIsACoproduct: both injections true, CaseRight (and CasesAreAll).
- MaybeIsACoproduct: `nothing` sent to the second branch at false, CaseLeft (and CasesAreAll).
- ListIsTheFreeMonoid: a marked join, Associative (and Neutral, FoldIsItself, Cons...); [false]
  as the neutral, FoldNeutral and NilIsNeutral; the negation injected, FoldInject.
- RecordsAreNamedProducts: the first projection reading `y`, PairFst and Pairing; the second
  reading `x`, PairSnd and Pairing. Pairing can't fail alone here, since the record built from a
  record's own two fields is that record.
- SumsAreNamedCoproducts: a case negating the first branch, CaseLeft (and CasesAreAll); negating
  the second, CaseRight (and CasesAreAll); swapped injections with swapped names, CasesAreAll only
  (at this census, where f and g are both the identity).
- FinIsACoequalizer: a projection flipping the negatives, ProjectsRelated (−4 and a positive even
  number are related but projected apart), and LiftProjects with it.
- KernelFiniteQuantifiers: `pairs` false with `every` and `some` right, QuantifiersPairs only.

The stuck match: the old `badSumsAreNamedCoproducts` gave `left := one, right := two`, bare
constructors, and its line had no census of `v`. Both are now as in the law's line (`fn u { one u }`,
`coreSumCensus`), and CasesAreAll runs on that model and holds, since the model only breaks the
names. I changed both at once, so I can't say which of the two caused the stuck match.

## Still uncontrolled

- core_laws.test.lut, EmptyIsInitial, `NoValue Empty model`: `Empty` has no value, so the law is
  vacuous on every model, broken or not, and no control can refute it. It is listed here and
  left as it is.

## Decisions taken on my own

1. Where the theory lets a conjunct fail only together with another (PositiveClosed with Least,
   Pairing with PairFst, Transitive on Bool with Reflexive, MetricNonNegative with Triangular,
   Triangular on Bool with the diagonal), the control breaks both. The comment above each model
   gives the reason.
2. The algebraic controls (semiring, ring, Boolean algebra, free monoid) use one model for
   several conjuncts (`-` as the product, implication as the meet). Each conjunct still has its
   own refuted entry. I didn't look for an "only this one" model there.
3. Transitive conjuncts get a listed census holding one chain (0, 1, 2 or its analogue). Their
   refutation then rests on that chain alone, never on a draw.
4. I fixed `badSumsAreNamedCoproducts` in place (its injections as functions, its `v` census)
   rather than removing it. It still refutes the two name laws it was written for.
5. I committed the controls program's store as `luthier test` wrote it, beside the program, so
   that `check -v` on the laws program reads the new controls before the coordinator's wave.
