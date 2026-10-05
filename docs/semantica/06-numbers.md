# Numbers: the ideal, its realization, and the arrays over them

Draft 1, 2026-10-05. Decided in the discussion of 2026-10-04 and 2026-10-05. Implemented the same day:
sections 2, 3, 5, 6 and the arrays over any type of section 7; not yet: the generic definitions
through a number model (section 4 and the end of section 7), which still compute with `Float64`.
It changes `04-kernel.md` (the primitive types, the bodies `primitive` and `axiom`) and
`05-static-semantics.md` (the variance of function types, the grade "assumed", the bridge with the
environment), which carry notes pointing here.

## 0. Notation

Every symbol used in this document.

- `ℤ`, `ℚ`, `ℝ`: the integers, the rationals, the reals, as mathematical objects.
- `Int`, `Rational`, `Real`, `Float64`: the Luthier types defined below.
- `u = 2^-53`: the unit roundoff of IEEE binary64, half the distance from 1 to the next double.
- `x ⊕ y`: the sum a machine computes on two doubles, the double nearest to `x + y`.
- `A <: B`: `A` refines `B`; every value of `A` is a value of `B` (`05 §1`).

## 1. The problem this settles

Until now `R` named the IEEE double, and every law over `R` read as a law of the reals while it was
a law of the doubles. Three different things were one name: the real numbers, which have the good
properties and no finite implementation; the doubles, a finite subset of them with rounded
operations; and the rationals, which can be computed exactly. Code is to be written over the real
numbers, the object with the good properties, and run over an approximation of them: the doubles
now, intervals or balls that enclose the true value later.

## 2. The types

| name | what it is | definition |
|---|---|---|
| `Int` | ℤ, without bound | `Int : U := primitive "integer"` |
| `Nat` | the integers from 0 | `{ k : Int \| 0 <= k }` |
| `Fin n` | the n indices | `{ k : Int \| 0 <= k and k < n }` |
| `Real` | ℝ, the ideal | `Real : U := primitive "real"` |
| `Float64` | the finite doubles | `Float64 : Real := primitive "ieee754-binary64"` |
| `String` | text | `String : U := primitive "unicode"` |

`R` disappears. Each primitive says, in its body, what it is.

- `Int` is ℤ. Python's `int` has no bound, so the interpreter realizes it exactly; a value that
  crosses into numpy, which computes with 64-bit integers, must fit, or the crossing is an error
  (section 6).
- `Real` is the ideal. It has no implementation of its own: its operations are not computed by the
  interpreter, and its structure is an axiom (section 3).
- `Float64 : Real`: every finite double is a real number, so the doubles refine the reals as a set.
  Infinities and NaN are not real numbers and are not values of `Float64` (section 6). The
  operations of `Float64` are the machine's (`x ⊕ y`), not those of `Real`; the refinement is of the
  values, not of the operations.

## 3. Axioms: what is assumed and never tested

    realField : CompleteOrderedField Real := axiom "the real numbers"

`axiom` is a body that gives a value whose laws are assumed: the definition is accepted, and its
obligations are recorded with the grade **assumed** instead of pending. `Real`'s structure cannot be
tested, because nothing computes the sum of two reals; it is stated, and what is stated without
proof or test is listed by `luthier check -v`, as the provisional externs are. An axiom is allowed
only in `core.lut` and in the libraries of the distribution (`lib/`).

`CompleteOrderedField` lives in `lib/algebra.lut`: the laws of a field, of a total order compatible
with it, and completeness. Completeness (every bounded set has a supremum) can be stated but not
tested; it is there so that the definition is the reals and not the rationals.

## 4. The ideal and its realizations

Code is written over `Real` wherever it means real numbers: a vector, an inner product, a likelihood,
a step of Levenberg-Marquardt. What runs is an approximation. Two kinds of declaration keep the types
honest:

- **A leaf of the environment is declared over what it really receives and returns.** numpy computes
  with doubles, so `dot : Vec Float64 -> Vec Float64 -> Float64 := extern "..."`. Its arguments must
  be accepted as declared; its result is a double, which is a real number, and is promoted to `Real`
  wherever a `Real` is expected (section 5).
- **A definition that should hold for every realization is generic in the number type.**
  `dotDef (A : U) (F : Ring A) (x : Vec A) (y : VecOf A x.n) : A`. `Real` is where its laws are
  meant; `Float64` is the instance that runs; an interval model would be another.

A law that compares a leaf with its definition states how far the realization departs from the
ideal, with a tolerance: the `...Agrees` laws of `array`. Two refinements are open (section 8): a
rounding law that makes the tolerance a consequence instead of a constant, and intervals, which make
the departure certifiable by enclosure.

Where a value of `Real` that is not known to be a double must enter a leaf, the conversion is
explicit: `toFloat64 : Real -> Float64`, the rounding to the nearest double. It is exact on values
that are already doubles.

## 5. Variance of function types

A function `f : A -> B` can be used where `A' -> B'` is expected when `A' <: A` and `B <: B'`: it
accepts every argument it will be given, and what it returns is of the expected kind. The domain
goes against the refinement, the codomain with it. So `Float64 -> Float64` can be passed where
`Float64 -> Real` is expected, and not where `Real -> Float64` is. The checker applies the rule when
a function value is checked against a function type, component by component through products and
sums; a value of a refinement passed where its base is expected needs no rule (`05 §1`).

## 6. The bridge with the environment

- **NaN is always an error.** It is not a number and means nothing in any computation here. A NaN
  that arrives from Python is an error at the crossing, and the interpreter's arithmetic fails rather
  than produce one.
- **An overflow to an infinity is an error**, as `exp 1000.0` already is.
- **An infinity that means something is asked for in the type.** The log-likelihood of an impossible
  datum is minus infinity, and that is information, not a failure:
  `ExtendedReal = < finite : Float64 | negInf : Unit | posInf : Unit >`, used only where a function
  needs it.
- **An integer that does not fit in 64 bits is an error when it crosses into numpy**, which would
  wrap it around silently (`2^62 * 4` is `0` in `int64`).

## 7. Arrays over any type

    Array (A : U) (n : Nat) = Fin n -> A
    Vec (A : U) = { n : Nat, f : Fin n -> A }
    Mat (A : U) = { m : Nat, n : Nat, f : Fin m -> Fin n -> A }

`Vec Real` is the vector of linear algebra, `Vec Float64` the one numpy computes with, `Vec Int` the
indices of a graph (which until now were vectors of doubles read with a rounding). The bridge
(`04 §6`): `Fin n -> Float64` is a one-dimensional ndarray of `float64`, `Fin n -> Int` one of
`int64` with the range check of section 6, any other element type a list.

The generic definitions receive the operations of their number type. They do so through a hole of
the file, filled by the importing file, not as an explicit parameter of every function: `array.lut`
declares `num : NumberModel` and writes over `num.T`; a program imports it with `num := float64`.
This is the file as a structure with its holes as parameters (`03 §1`).

## 8. Open

- **Rational.** ℚ exact, natively or with Python's `Fraction` as its representation. It is a model
  of an ordered field (not complete) where the laws of `+ − × /` hold exactly.
- **The rounding law.** `Float64` as a model of a field with rounding: with `toQ : Float64 ->
  Rational` the exact embedding, `|toQ (x ⊕ y) − (toQ x + toQ y)| ≤ u · |toQ x + toQ y|` away from
  overflow, testable exactly in `Rational`. From it the tolerance of a sum of n terms follows, and the
  constants of `array` (`roundingSlack`) become certified instead of supposed.
- **Intervals or balls.** A realization whose value encloses the true real; the law
  `f_Float64 x ∈ f_Interval x` certifies an approximation without computing `f` over the reals. A
  comparison of two overlapping intervals has no answer; the model answers with a probability, and a
  result that depends on it is a distribution.
- **Two levels of number theory.** `Rational` has `+ − × /` exactly and no `exp`, `log`, `sqrt` or
  `erf`; `Real`, `Float64` and intervals have them. The number model is a field, extended by the
  elementary functions where the model has them.
- **Randomness.** The generator of `lib/random.lut` states no invariant of randomness and has no use
  case beyond feeding `test`. A random library should state what randomness is (laws on the
  distribution of its output and tests of them), and the generator that a program needs, fast and in
  batches, is an extern. Notes of Luciano in `random.lut`, 2026-10-05.
