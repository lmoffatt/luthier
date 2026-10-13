# 11. Numbers

Chapter 11 of the specification, draft 0, 2026-10-12. Sources: `docs/spec/06-numbers.md` (commit 3445ad8, whole), `docs/principles.md` (L13, L12, L3, L14), `tests/spec/n1_numbers.accept.lut` to `n5_arrays.accept.lut` with their reject programs, `src/luthier/lib/rational.lut`, `src/luthier/evaluator.py` (read only). Written by Claude Sonnet 5.5. It realizes L13, with L12, L3 and L14. The notation (ℤ, ℚ, ℝ, the unit roundoff u, the rounded sum) is that of `spec 1`.

## §1 The ideal and its realizations

**11.S1. Three things under one name.** [implemented] The real numbers (good properties, no finite implementation), the finite doubles (a finite subset of them with rounded operations) and the rationals (computable exactly) are three objects with three names. Code is written over the real numbers and run over an approximation of them: the doubles today, intervals or balls later (11.S10). This is L13.1.

**11.S2. A leaf is declared over what it receives.** [implemented] A leaf of the environment (an `extern`) is declared over the type it really receives and returns: numpy computes with doubles, so `dot` is declared over `Vec Float64`. Its result is a double, hence a real number, and is promoted where a `Real` is expected (11.R4).

**11.S3. A definition meant for every realization is generic in the number type.** [decided D-2026-10-12-ah] Such a definition takes the operations of its number type; `Real` is where its laws are meant, `Float64` the model that runs, an interval model another. The file states this through a hole `num : NumberModel` filled by the importing file (`num := float64`), which is the file as a theory with its holes as parameters (`spec 3`). The theory `NumberModel` would live in `lib/number_model.lut`, which does not exist yet; `array.lut` still computes with `Float64`.

## §2 The primitive types

**11.R1. The number types and the end of `R`.** [implemented] `Int` is ℤ without bound, `Real` is the ideal, `Float64` is the finite doubles and refines `Real` (every finite double is a real number), `String` is text. `Nat` is `{ k : Int | 0 <= k }` and `Fin n` is `{ k : Int | 0 <= k and k < n }`. A value of `Float64` passes where a `Real` is expected. `R` names no type. Each primitive states in its body what it is: `Int : U := primitive "integer"`, `Real : U := primitive "real"`, `Float64 : Real := primitive "ieee754-binary64"`, `String : U := primitive "unicode"`.
Files: n1_numbers.accept.lut, n2_r_gone.reject.lut.

**11.R2. Only the core says what the interpreter provides.** [implemented] The body `primitive` is allowed only in `core.lut`.
Files: n1_numbers.accept.lut, n3_primitive_outside_core.reject.lut.

**11.S4. What a primitive is.** [implemented] `Int` is realized exactly by the host's unbounded integers. `Real` has no implementation of its own: the interpreter computes none of its operations, and its structure is an axiom (11.R3). The operations of `Float64` are the machine's rounded ones, not those of `Real`: the refinement is of the values, not of the operations. `Rational : Real` is a primitive of `core.lut`, represented by the host's fractions, with `+ − × /` and the comparisons exact and no `mod`; its values come from `fromInt`, `ratio` and `toQ` of `lib/rational.lut`.

**11.S5. The conversion from an integer.** [implemented] `toFloat64 : Int -> Float64` is the nearest double to an integer, exact below 2^53; the name stays with the integers (D-2026-10-05-c). A value of `Real` that is not known to be a double enters a leaf only through an explicit rounding to the nearest double, exact on doubles. [decided D-2026-10-12-ah] That rounding waits for a `Real` that computes (11.S10): until then no value of `Real` is not a double and no law over `Real` is tested.

## §3 Axioms

**11.R3. An axiom is assumed and allowed only in the core and the libraries.** [implemented] `axiom "<text>"` is a body whose value has its laws assumed: the definition is accepted and its obligations carry the grade `assumed` (`spec 6`), listed by `luthier check -v` together with the provisional externs. An axiom outside `core.lut` and `lib/` is refused. The structure of `Real`, `realField : CompleteOrderedField Real`, is stated this way, since nothing computes the sum of two reals; `CompleteOrderedField` (in `lib/algebra.lut`) holds the laws of a field, of a compatible total order, and completeness, which can be stated and not tested. What an `assumed` certificate carries is D-2026-10-12-t.
Files: n5_arrays.accept.lut, n4_axiom_outside_lib.reject.lut.

## §4 Variance of function types

**11.R4. A function type is contravariant in its domain and covariant in its codomain.** [implemented] A function `f : A -> B` is accepted where `A' -> B'` is expected when `A' <: A` and `B <: B'`, where `<:` is refinement (`spec 4`). So `Float64 -> Float64` is accepted where `Float64 -> Real` is expected, and refused where `Real -> Float64` is. The checker applies the rule when a function value is checked against a function type, component by component through products and sums; a value of a refinement passed where its base is expected needs no rule.
Files: r9_variance.accept.lut, r9_variance.reject.lut.

## §5 The bridge with the host

**11.S6. A value is checked against its declared type when it crosses.** [implemented] An `Int` is a host integer, never a boolean or a float; a `Float64` is a float, or an integer with an exact double, promoted; a `String` is a string; `Unit` is the empty value. An array as a value of `Fin n -> Int` has an integer dtype, and as one of `Fin n -> Float64` a float dtype (an integer array is promoted), with exactly as many dimensions as indices. A number where a record, a pair or a function is expected is an error. `luthier run --set name=value` reads the value by the declared type of the hole (`spec 12`).

**11.S7. NaN and overflow are errors.** [implemented] NaN is not a number and is always an error, at the crossing and in the interpreter's arithmetic, inside arrays as well. An overflow to an infinity is an error. An infinity that means something is asked for in the type: `ExtendedReal = { finite : Float64 || negInf : Unit || posInf : Unit }`, used only where a function needs it, as the log-likelihood of an impossible datum.

**11.S8. An integer that does not fit in 64 bits is an error when it crosses into the host's arrays.** [implemented] The host would otherwise wrap it silently.

## §6 Arrays over any type

**11.S9. Arrays.** [implemented] `Array A n = Fin n -> A`, `Vec A = { n : Nat, f : Fin n -> A }`, `Mat A = { m : Nat, n : Nat, f : Fin m -> Fin n -> A }`, over any type `A`. The bridge reads `Fin n -> Float64` as a one-dimensional float64 ndarray, `Fin n -> Int` as one of int64 with the range check of 11.S8, any other element type as a list. A program using them is `n5_arrays.accept.lut`, which declares a `Vec Int` and a `Vec Float64`.

**11.S10. Intervals, balls and the two levels of number theory.** [decided D-2026-10-12-ah] A realization whose value encloses the true real would certify an approximation by a law of the form "the double result lies in the interval result" without computing over the reals; two overlapping intervals have no ordering, so a comparison answers with a probability and a result that depends on it is a distribution. This waits for the algebra of costs (O1) and the error by intervals as a decorated output (O5). `Rational` has `+ − × /` exactly and no `exp`, `log`, `sqrt` or `erf`; the number model would be a field extended by the elementary functions where the model has them (O1).

**11.S11. Randomness.** [decided D-2026-10-12-ah] The generator of `lib/random.lut` states no invariant of randomness. What randomness is, as laws on the distribution of its output with tests of them, is spec 7.S1.

## §7 The rounding law

**11.S12. The inclusion of the doubles into the rationals.** [implemented] `toQ : Float64 -> Rational` is the inclusion of the finite doubles: exact (`nearest (toQ x) == x`) and order-preserving. The comparison of a double with the exact result is made in `Rational`, so the law needs no tolerance. Stated in Luthier in `lib/rational.lut` (L14).

**11.S13. Each operation rounds the exact one.** [implemented] For the sum, difference, product and quotient, `|toQ (x op y) − (toQ x op toQ y)| ≤ u · |toQ x op toQ y|`, with `u` the unit roundoff of `spec 1`; the square root satisfies `|r² − x| ≤ (2u + u²) x`. They are certified over `NormalDouble`, the doubles of magnitude between 1e-150 and 1e150 (zero included), drawn uniformly in the exponent so that every scale is tested; a negative control, an addition three units off in the last place, fails the law wherever its result is not zero. Stated in `lib/rational.lut` (`Rounds`, `float64Add`, `offByThree`, `RootRounds`). The range 1e-150 to 1e150 and the unit `u` are parameters of the statement in the sense of `P11`; today they are written in the library. [decided D-2026-10-12-ah] The range moves to the demand's parameters (D-2026-10-12-h); the library is not changed yet.

**11.S14. What follows for sums.** [implemented] A sum of n terms is within `gamma n = n u / (1 − n u)` of the exact sum, relative to the sum of the absolute values; an inner product likewise (Higham 2002, §3.1 and §4.2). Certified for `sumTo` and for the host's `total`, `dot` and `matVec`, whatever order they sum in.

**11.S15. The doubles are not a field.** [implemented] `float64Field` does not exist: under cancellation no fixed relative tolerance makes addition associative, and a box is not closed under the operations. The folds of the doubles are `foldWith`, a fold with no laws claimed, in the same order, so every result is the same bit for bit. What the doubles have instead is 11.S13.

**11.S16. Rounding does not expand distances, up to an additive defect.** [proposed] Following L13.3: rounding has no multiplicative constant bounds the expansion of rounding; rounding `Real -> Float64` is non-expansive up to an additive defect `δ(x)`, about `ε |x|`, where `ε` is the demand's parameter (D-2026-10-12-h) and never a constant of the code. The per-input sensitivity of subtraction and division is L13.3's, given by a condition number `κ` that the law of the operation takes as a parameter. The rounding law of 11.S13 is the worked instance: there `δ(x) = u |x|` and the result is exact in `Rational`. The status follows D-2026-10-12-y: the correction stays reversible, nothing about `ε` is fixed.

**11.S17. The functor reading and the algebra of costs.** [proposed] Following L13.4: the reading of rounding as a functor stands with "non-expansive plus an additive term". The `Cost` of `spec 5` then carries the two parts L13.4 names, Lipschitz where a constant exists and additive where rounding enters: O1.

**11.S18. The tolerances of the libraries return a measured cost.** [decided D-2026-10-12-ah] The laws `...Agrees` of `lib/array.lut` and `roundingSlack` of `lib/real.lut` compare a numpy leaf with its native definition with a tolerance written in the library, and stay so where 11.S13 gives no bound by itself (the determinant, the spectrum, solving, the pseudo-inverse, whose error depends on the conditioning of the matrix). The cutoff is the demand's (D-2026-10-12-h, L12.3): the law returns the measured cost and the certificate records it (`spec 5`, `spec 6`). Changing the libraries accordingly is proposed and not done.

**11.S19. The theories of this chapter in Luthier.** [decided D-2026-10-12-ah] `lib/rational.lut` states 11.S12 to 11.S15 and exists. `lib/number_model.lut`, stating `NumberModel` and the generic definitions of 11.S3, does not exist. The statement of 11.S16 as a theory (a map with a defect and a condition number as parameters) would live in `lib/rational.lut` beside the instance and is not written.

## Open

Costs and the additive defect: O1. Intervals as a decoration of the output: O5.
