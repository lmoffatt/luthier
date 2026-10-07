# Test-value generators: prior art for Luthier

Survey written on 2026-10-06 for the design of explicit generators in Luthier's `test` command.
Documentation and source code are linked where they are cited; papers are collected in the
bibliography at the end. Quotations are verbatim from the linked pages or papers.

## Terms

Property-based testing (PBT) checks a stated property on many generated inputs. A generator
produces values of a type; Hypothesis calls it a strategy and fast-check an arbitrary. I write
`Gen A` for a generator of values of type `A`, as Luthier's `lib/random.lut` does
(`Gen A = Nat -> Int -> A * Int`: a size and a seed give a value and the next seed). Shrinking is
the search for a smaller failing input after a failure has been found.

On the Luthier side: a law is a property stated in a type; an obligation is a law applied to a
definition; `gen T := term` registers the generator of type `T`; a refinement type `{x : T | p x}`
restricts `T` to the values that satisfy the predicate `p`; `Fin n` is the type of the integers 0
to n - 1; `U` is the type of types; and a certificate entry records a law, its grade (point,
sampled n, bounded, exhaustive, witnessed, proved, assumed), the generators it drew from, and the
seed.

## 1. Explicit versus type-directed generators

QuickCheck [Claessen and Hughes 2000] ties generation to types. The `Arbitrary` class gives each
type one `arbitrary :: Gen a` and one `shrink :: a -> [a]`, and the argument types of a property
select them. Its current documentation
([Test.QuickCheck.Arbitrary](https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck-Arbitrary.html))
says that "there is no generic arbitrary implementation included because we don't know how to make
a high-quality one", and that "good generators are often the difference between finding bugs and
not finding them". A property picks another distribution for the same underlying type in one of
two ways. The first is a newtype wrapper with its own instance, the modifiers of
[Test.QuickCheck.Modifiers](https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck-Modifiers.html):
`Positive`, `NonNegative`, `NonZero`, `NonEmptyList`, `OrderedList`, `Small`, `Large` and others.
Some of them restrict the support (`Positive x` "guarantees that x > 0"). Others impose no
predicate and change how values are drawn: `Large Int` gives "values drawn from the entire range"
where plain `Int` draws from a small range, and `Small` does the opposite. The second way is
explicit quantification,
`forAll gen prop` or `forAllShrink gen shrink prop`
([Test.QuickCheck](https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck.html)), which
bypasses the class for that argument.

Hedgehog ([Hackage](https://hackage.haskell.org/package/hedgehog),
[README](https://github.com/hedgehogqa/haskell-hedgehog)) has no class of default generators. A
generator is a value handed to `forAll`, as in
`forAll (Gen.list (Range.linear 0 100) Gen.alpha)`, and numeric bounds are `Range` values
(section 2). The README's first features are "Integrated shrinking, shrinks obey invariants by
construction" and "Range combinators for full control over the scope of generated numbers and
collections". Integrated shrinking is the technical reason to attach everything to the generator.
MacIver's example [MacIver 2016]: for `even = integers().map(lambda x: 2 * x)` and a property that
fails above 4, a shrinker that only knows the type `int` reduces the failure to n = 1, which is
outside the intended domain and fails for an unrelated reason, while Hypothesis, shrinking through
the generator, reports n = 6. falsify [de Vries 2023] brings the same internal shrinking to Haskell
with explicit generators, generators of functions included.

Hypothesis ([strategies reference](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html))
makes explicit strategies the main interface and puts type-directed lookup on top. `from_type(T)`
"is used internally to fill in missing arguments to builds() and can be used interactively to
explore what strategies are available or to debug type resolution". Its lookup tries, in order: a
registered or default strategy for `T`; special rules for `typing` constructs; the union of the
strategies of registered subtypes; `builds(T)` from the constructor's annotations; and, for an
abstract class, the union of its concrete subclasses. `register_type_strategy` edits one global
table, "for example excluding NaN from floats" (NaN, "not a number", is the IEEE 754 value for
undefined results). The design argument is MacIver's "Moving Beyond
Types" [MacIver 2017]. Inferring the data from argument types "is a bad idea", because "often you
want to generate something much more specific than any value of a given type", and the Haskell
remedy of one newtype per restriction "is purely a workaround for a limitation of the API". He
anticipates the dependently typed case, which is Luthier's: the restriction could live in the type,
yet deriving the generator automatically stays hard, since "a type is effectively a predicate which
consumes a value, where a data generator is a function that produces a value, so in order to
produce a generator for a type automatically you need to basically invert the predicate". His
practical point is that people customize generation when it is easy, and when it is hard they add
preconditions (`assume`, QuickCheck's `==>`), which discard tests and skew the distribution.

The Rust library proptest makes the same comparison
([book, "Differences between QuickCheck and Proptest"](https://proptest-rs.github.io/proptest/proptest/vs-quickcheck.html),
written against the Rust port of QuickCheck): "QuickCheck can only define one generator and
shrinker per type", and one global size sets every range, so an integer in 0..100 and another in
0..1000 need two newtypes, where in proptest each is just its range expression. proptest still has
an `Arbitrary` trait for when "it makes sense to define a canonical strategy"
([book](https://proptest-rs.github.io/proptest/proptest/tutorial/arbitrary.html)). PropEr
[Papadakis and Sagonas 2011] goes the type-directed way in a dynamically typed language: it turns
Erlang type specifications into generators, next to hand-written ones.

Evidence on effectiveness. The Etna platform [Shi et al. 2023] compared, on binary search trees,
red-black trees and two typed lambda calculi, a QuickCheck generator derived from the types
(generic-random) with a hand-written generator that only produces inputs meeting each property's
precondition: "the bespoke strategy solved all tasks, while the naive strategy failed to solve 43
tasks". Interviews with 30 developers at Jane Street [Goldstein et al. 2024] found hand-written
generators (19 of 30) and type-derived ones (19 of 30) both in use, generator writing called
"tedious" or "high-effort", and one developer describing a tension "between 'I want kind of
coverage of everything' and 'I want coverage that is realistic for most inputs'". That tension is
the practical case for several generators on one type.

How a property names its generator when a type has several useful distributions. QuickCheck: by
the argument's type (a newtype) or by `forAll gen`. Hedgehog: by the generator value given to
`forAll`. Hypothesis: by the strategy given to `@given(x=...)` or `data.draw(...)`, with
`from_type` as the default; a named domain is a variable bound to a strategy
(`finite = st.floats(allow_nan=False, allow_infinity=False)`). proptest: by the strategy
expression, with `any::<T>()` for the canonical one. Every library also has the one-value
generator: Hypothesis `just(v)` and the `@example(v)` decorator, an input "which Hypothesis will
always try before generating random inputs"
([API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html)); Hedgehog
`Gen.constant`; QuickCheck `pure v`.

Applicable to Luthier: Requiring an explicit generator for every drawn type puts Luthier with
Hedgehog, Hypothesis and proptest, and with QuickCheck's own documentation, which declines to ship
a generic generator. In code it retires the fallbacks of `generators.py` (Int and Float64 uniform
in [-size, size], data types derived from their constructors, constant or affine functions), each
of which now produces values the program never asked for. Refinement types already do the job of
QuickCheck's support-restricting newtypes (`Positive`, `NonEmptyList`), and checking every
generated value against the type's predicate is Hughes's validity test (section 7) made automatic;
MacIver's remark explains why that check is needed, since a generator inverts a predicate that the
checker can only evaluate. A refinement type can't name a distribution, though: uniform and
log-uniform on one interval have the same predicate, and QuickCheck needs `Small` and `Large`
because `Int` alone can't say how to draw. With
aliases transparent (R7) and a second generator for a type rejected, Luthier today has no way to
say that a law should also be tested under a second distribution on the same support. The prior
art has two mechanisms for it: a nominal wrapper that is not an alias (`Large`), or a named
generator value that the test of a law selects per parameter (Hedgehog's `forAll gen`, Hypothesis's
`@given(x=...)`), written into the certificate. A default generator per type plus a per-test
override is what Hypothesis's `register_type_strategy` and explicit strategies amount to.

## 2. Numeric generators

Hedgehog's [Range](https://hackage.haskell.org/package/hedgehog/docs/Hedgehog-Range.html)
separates the bounds from the draw. A `Range a` has an origin and a function from the size (an
integer from 0 to 99 that grows over a run) to a pair of bounds; "as the size goes towards 0, the
values go towards the origin", and shrinking moves toward the origin. `constant 0 10` ignores the
size. `linear 0 10` has bounds (0, 0) at size 0, (0, 5) at size 50 and (0, 10) at size 99.
`exponential 1 512` has (1, 1) at size 0, (1, 2) at 11, (1, 4) at 22, (1, 128) at 77 and (1, 512)
at 99. `constantFrom`, `linearFrom` and `exponentialFrom` take an origin apart from the bounds (the
documented example is a year in [1970, 2100] with origin 2000), and `exponentialFloat` does the
same for floating point. Within the bounds of the current size the draw is uniform
([source](https://github.com/hedgehogqa/haskell-hedgehog/blob/master/hedgehog/src/Hedgehog/Internal/Gen.hs):
`Seed.nextInteger lo hi`, `Seed.nextDouble lo hi`). An exponential range therefore spreads
magnitudes over orders of magnitude across a run, while each single draw is uniform in its current
interval.

Hypothesis `integers(min_value=None, max_value=None)` shrinks toward 0. Since version 6.152.9
(2026-05-19, [pull request 4728](https://github.com/HypothesisWorks/hypothesis/pull/4728)) the draw
comes from one smooth distribution: uniform for |x| ≤ 256, and outside that a Student t on the
signed bit length, Y = sign(x) log2(1 + |x|) ~ 13 t(2), where x is the drawn integer, Y its signed
base-2 log magnitude, t(2) a Student t variable with 2 degrees of freedom, and ~ reads "is
distributed as"
([providers.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/internal/conjecture/providers.py),
[statistics.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/internal/statistics.py)).
A bounded range uses the same distribution restricted to [min_value, max_value]; the pull request
argues that "a better distribution for bounded ranges is simply the restriction of our unbounded
distribution to that domain", and explains what was wrong with the old scheme (pick a bit width
among 8, 16, 32, 64 and 128, then draw uniformly): "the bit length immediately after each cliff is
many, many orders of magnitude less likely to be sampled than right before each cliff". For
bounded ranges wider than 127 the endpoints get extra mass, 2/128 each for min and max and 1/128
each for min + 1 and max - 1
([numbers.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/strategies/_internal/numbers.py)).
With probability 0.05 the draw is instead a constant from a pool: powers of 2 from 2^16 to 2^65,
powers of 10 from 10^5 to 10^19, the factorials 9! to 20!, a few primorials, their neighbours at
±1, and all their negatives.

`floats(min_value, max_value, *, allow_nan, allow_infinity, allow_subnormal, width=64,
exclude_min=False, exclude_max=False)` has these documented semantics: bounds are inclusive unless
excluded; asking for NaN is an error once a bound is given, and asking for infinity once both are;
"where not explicitly ruled out by the bounds, subnormals, infinities, and NaNs are possible
values"; a `width` of 16 or 32 restricts the draw to values exactly representable at that
precision; "excluding either signed zero will also exclude the other"; shrinking prefers finite to
infinite and infinite to NaN. The draw itself (`draw_float` in providers.py) is a mixture. With
probability 0.15 it takes a constant the bounds allow, either from a global pool (0.5, 1.1, 1.5,
1.9, 1/3, 1e7, 1e-5, 1 - 1e-5, 2 + 1e-5, 2^53, the machine epsilons of 32- and 64-bit floats, the
smallest normal and subnormal numbers of 16-, 32- and 64-bit floats, several more 64-bit
subnormals, the largest finite 32- and 64-bit values, and the negatives of all of these) or from
the program's own literals (next paragraph).
Otherwise, with probability 0.05, it takes one of the special values the bounds allow: 0.0, -0.0,
±infinity, NaN of both signs, a signaling NaN, min, the next float above min, min + 1, max - 1, the
next float below max, and max. Otherwise it decodes 64 random bits with an encoding designed for
shrinking
([floats.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/internal/conjecture/floats.py)):
half of the bit patterns decode to integer-valued floats and the other half to floats whose
exponent bits are reordered, so magnitudes spread over the whole exponent range; a random sign is
applied and the result clamped to the bounds.

Program literals as test values. Since 6.131.1 (2025-04-17,
[changelog](https://hypothesis.readthedocs.io/en/latest/changelog.html)) "Hypothesis now looks for
constant values in the source code of your program, and sometimes uses them while generating
examples". It parses the program's own modules (leaving out the standard library and installed
packages) and keeps up to 1024 literal integers, floats, strings and byte strings per module
([constants_ast.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/internal/constants_ast.py));
they form the second constant pool above, chosen half the time a constant is drawn.

Other libraries. proptest
([proptest::num::f64](https://docs.rs/proptest/latest/proptest/num/f64/index.html)) names classes of
floats as flags that combine with `|`: `POSITIVE`, `NEGATIVE`, `NORMAL`, `SUBNORMAL`, `ZERO`,
`INFINITE`, `QUIET_NAN`, `SIGNALING_NAN`, `ANY`. "The various float classes are assigned fixed
weights", in the order "NORMAL > ZERO > SUBNORMAL > INFINITE > QUIET_NAN = SIGNALING_NAN", and the
documentation sends ordinary tests to ranges such as `-1.0..2.0`. fast-check
([numbers](https://fast-check.dev/docs/core-blocks/arbitraries/primitives/number/)) has
`fc.double({min, max, minExcluded, maxExcluded, noDefaultInfinity, noNaN, noInteger})`, and its
integer generators are biased: with probability 1/biasFactor they draw from short intervals next to
0, min and max, each about log2 of the range wide, and uniformly otherwise
([BiasNumericRange.ts](https://github.com/dubzzz/fast-check/blob/main/packages/fast-check/src/arbitrary/_internals/helpers/BiasNumericRange.ts),
[IntegerArbitrary.ts](https://github.com/dubzzz/fast-check/blob/main/packages/fast-check/src/arbitrary/_internals/IntegerArbitrary.ts)).
QuickCheck's default `Double` is a mixture too
([Arbitrary.hs](https://github.com/nick8325/quickcheck/blob/master/src/Test/QuickCheck/Arbitrary.hs)):
uniform in [0, 1) at full precision, integer values, fractions with small denominators, and two
uniform draws in [-size, size]; it never gives NaN or infinity. SmallCheck [Runciman et al. 2008]
enumerates floats by depth, defining the depth of s·2^e (s the integer mantissa, e the exponent) as
the depth of the integer pair (s, e), so the floats of depth at most 2 are -4, -2, -1, -0.5, -0.25,
0, 0.25, 0.5, 1, 2 and 4: an enumeration on a log scale.

Log-uniform sampling. A positive variable x is log-uniform on [a, b], with 0 < a < b, when ln x
(its natural logarithm) is uniform on [ln a, ln b]; its density is f(x) = 1/(x ln(b/a)) for
a ≤ x ≤ b ([scipy.stats.loguniform](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.loguniform.html),
also known as the reciprocal distribution). Every interval [c, 2c] lying inside [a, b], whatever
c, then gets the same probability, which suits a quantity whose scale is unknown. Bergstra and
Bengio [2012] call this
"drawn exponentially", use it for learning rates and penalties, and add an explicit zero where zero
is a legitimate value: a weight penalty is "either 0 (with probability 0.5), or log-uniformly from
10^-7 to 10^-4". LAPACK's test-matrix generator offers the same choice for singular values
(section 5, mode 5: random numbers in (1/COND, 1) "such that their logarithms are uniformly
distributed"). The log scale needs a strictly positive lower bound on the magnitude; a quantity
that can be zero or change sign needs a sign draw and an atom at zero, which is what Hypothesis's
signed-log integer distribution and Bergstra and Bengio's mixture provide.

Edge cases and conformance. Conformance tools for IEEE 754 arithmetic, such as IeeeCC754
[Verdonk et al. 2001], check an implementation against fixed test vectors that cover the special
operands (zeros, subnormals, infinities, NaNs) and the rounding modes. PBT libraries take the
cheaper route described above: they mix a few percent of such values into each random draw
(Hypothesis about 5% special floats and 15% constants, proptest fixed class weights, fast-check a
1/biasFactor bias), so a run of a few hundred cases meets each special value several times.

Applicable to Luthier: A numeric generator can be declared by the parameters these libraries
converge on: bounds, each closed or open (`exclude_min`, `exclude_max`); a scale, linear or
logarithmic; an origin toward which values shrink and from which a growing size starts (Hedgehog);
and the special values with their total probability. A log scale needs a positive lower bound on
the magnitude; for a quantity that can be zero or negative the declaration adds a sign and an atom
at zero, as `gen_normal_double` in `rational.py` already does (sign and binary exponent uniform,
zero 2% of the time) and as Bergstra and Bengio do for a penalty that is zero half the time. The
dimensions now carried by Luthier's types suggest defaults (a standard deviation or a distance is a
scale quantity, a coordinate is a location quantity), but under the explicit rule the declaration
should still state the scale. The special values deserve their own decision: laws about real
arithmetic up to a tolerance are false at NaN and infinity, so those values belong outside the type
(a refinement like `NormalDouble`), while laws about Float64 itself need a generator that includes
them with a stated weight. Two cheap additions come from Hypothesis: extra weight on the bounds and
their neighbours, and a small probability of drawing literals that appear in the program
(thresholds such as `zMax >= 3` or `draws >= 100`), which is where off-by-one errors sit. Today a
single `size` sets every numeric range (`genInt` and `genFloat64` are uniform in [-size, size]);
proptest's criticism of one global size applies, and with explicit bounds per generator the size
argument matters only for recursive data.

## 3. Generators of functions

Random functions. QuickCheck generated functions from the start [Claessen and Hughes 2000] through
the class `CoArbitrary`: `coarbitrary :: a -> Gen b -> Gen b` uses the argument to perturb the
random generator (with `variant`), so f(x) is a draw from `Gen b` seeded by x. Such a function is
pure and total but opaque: it can be neither printed nor shrunk. Claessen [2012] fixed that with
`Fun a b`
([Test.QuickCheck.Function](https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck-Function.html),
[source](https://github.com/nick8325/quickcheck/blob/master/src/Test/QuickCheck/Function.hs)). A
class `Function a` turns a function on `a` into a concrete data structure `a :-> c` built from
`Unit`, `Pair` (a function of pairs, curried), `:+:` (a function of a sum as two functions),
`Table [(a, c)]` (for types with equality), `Map` (through a bijection with a type already handled)
and `Nil` (no information: use the default). A function on an infinite type such as `Integer` is an
infinite tree built lazily; shrinking replaces subtrees by `Nil`, which leaves a finite table plus
a default value, and that is what gets shown: `{"elephant"->1, "monkey"->1, _->0}`. Instances come
from `functionMap` (a bijection), `functionShow`, `functionIntegral` and `functionRealFrac`
(through `Rational`). falsify [de Vries 2023] keeps the representation with a single class that
builds the concrete function directly. LeanCheck
([Test.LeanCheck.Function.Listable](https://hackage.haskell.org/package/leancheck/docs/Test-LeanCheck-Function-Listable.html))
enumerates functions as "a finite list of exceptional input-output cases to a default value", shown
as case expressions; its documented counterexample to `foldr f z xs == foldl f z xs` is
`\x _ -> case x of 0 -> 1; _ -> 0`. SmallCheck builds functions of bounded depth by case analysis
on the argument, depth being "a measure combining the depth to which arguments may be evaluated and
the depth of possible results" [Runciman et al. 2008]. Hypothesis `functions(like, returns,
pure=False)`
([reference](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html#hypothesis.strategies.functions),
[source](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/strategies/_internal/functions.py))
returns a function that draws its result from `returns` each time it is called during the test;
`pure=True` memoizes the result per argument; the failure report notes every call with its
arguments and the value returned ("Called function: ..."), or prints `lambda x: c` when `returns`
can only give one value; and the function can't be called once the test is over. Koopman and
Plasmeijer [2006] generate values of a data type whose values describe functions, plus one function
that turns each description into the function it describes, so showing the function means showing
the data. Bernardy, Jansson and Claessen [2010] show how to test a polymorphic property at a
single monomorphic instance, computed from its type, such that passing there implies passing at
every instance.

Functions taken from the program. QuickSpec [Claessen, Smallbone and Hughes 2010; Smallbone et al.
2017] starts from a signature, a list of the program's functions and constants, enumerates the
well-typed terms built from it up to a size, and tests which equations hold among them. Speculate
[Braquehais and Runciman 2017] does the same with enumerative testing and also finds conditional
equations and inequalities. Conjure ([repository](https://github.com/rudymatela/conjure))
synthesizes a function body out of "ingredients" the user lists, enumerating their combinations
and testing each candidate against a partial definition. FitSpec [Braquehais and Runciman 2016]
enumerates mutants of the function under test to see whether a set of properties tells them apart.
Jeuring, Jansson and Amaral [2012] test type class laws instance by instance with QuickCheck,
comparing functional values (state monad computations) through observations. Hypothesis resolves
an abstract class to the union of its registered concrete subclasses (section 1), a census of
implementations. The semantic footing is Reynolds's defunctionalization [Reynolds 1972]: a program
contains finitely many lambda abstractions, so every function value that can reach a higher-order
parameter is one of them closed over some captured values, and a function type can be replaced
exactly by one tag per abstraction plus an `apply` function.

The census of registered values, assessed against this. What it gains: the functions drawn are the
ones the laws are meant for, so a passing law speaks directly about the program's own functions.
Over a finite census the test can be exhaustive (section 4). Every drawn function has a name, which settles the showing problem that Claessen's paper exists to solve.
Collisions such as f = g, which Hughes [2019] shows matter for laws with several parameters, happen
often in a small population. And it is the same move as certifying theory laws per model, as
Hypothesis's resolution of abstract classes, and as testing type class laws per instance; applied
to types, a census would give obligations generic in a type parameter something to run on.

What it loses: the census is biased toward well-behaved functions. Random tables (Claessen) and
exception lists (LeanCheck) produce functions that are non-monotone, constant almost everywhere, or
that separate values a law treats as equal; the documented counterexamples look like that
(LeanCheck's `\x _ -> case x of 0 -> 1; _ -> 0`, Claessen's `{"elephant"->1, "monkey"->1, _->0}`),
and a census of tidy program functions rarely contains such functions. A census isn't closed
under composition: a law over `f` and `g` sees only registered pairs unless terms are enumerated up
to some depth, as QuickSpec does. The test's strength depends on what else the program defines, so
adding or removing an unrelated function changes what a certificate means. For many function types
the census is empty or has one member, which turns the law into a vacuous or a point check. And
closures need care: a single abstraction such as `\x -> a*x + b` stands for a family, and its
captured values (a and b here) must be drawn from their own generators, otherwise the census
counts one function where the program has infinitely many.

Applicable to Luthier: The census fits Luthier as one named generator for a function type, next to
the random tables it already draws for `Fin n` domains (the finite case of Claessen's `Table`)
and, for infinite domains, a lazily drawn function memoized per argument (Hypothesis `functions(pure=True)`, QuickCheck `Fun`) recorded as the finite
table of the calls actually made plus a default. Read as defunctionalization, the census is a list
of lambda abstractions whose captured values are drawn; the current affine fallback
(`\x -> a*x + b` on Float64) is exactly such a census of one abstraction. Because the census
changes whenever the program's function definitions change, its membership must enter the hash of
the dependency cone and the certificate's description of the generator, and an empty or one-member
census must show up in the grade. The same mechanism applied to types (the registered models or
instantiations of `Theta`) would let the obligations generic in `(Theta : U)` run, and Bernardy et
al. suggest that for parametric laws a single well-chosen instance can stand for all. Under R8 a
law comparing functions needs an observational equality, and its test draws the comparison points
from the domain's generator.

## 4. Exhaustive and bounded enumeration

SmallCheck [Runciman et al. 2008] tests "all the finitely many values up to some depth,
progressively increasing the depth used". Its motivation is a version of the small scope
hypothesis behind Alloy [Jackson 2006; Andoni et al. 2002]: "If a program fails to meet its
specification in some cases, it almost always fails in some simple case", and a passing run gives
"a clear demarcation between tested and untested cases". Lazy SmallCheck prunes the enumeration by
running the property on partially defined values. LeanCheck ([Test.LeanCheck](https://hackage.haskell.org/package/leancheck/docs/Test-LeanCheck.html);
[Braquehais 2017]) enumerates values in tiers of increasing size; `counterExample 1000 prop`
returns the smallest counterexample among the first 1000 values, and the suggested budgets are 500,
1000 or 10000 tests. Feat [Duregård, Jansson and Wang 2012] defines enumerations as bijections
between natural numbers and values, indexed by size, which supports both exhaustive testing of
small sizes and uniform random sampling of a given large size.

Etna [Shi et al. 2023] compared the enumerators with random testing. LeanCheck solved 82% of the
tasks and SmallCheck 35%; SmallCheck reaches large inputs early (trees of up to ten nodes in its
first thousand values against four for LeanCheck), and "only 1% of these thousand SmallCheck trees
are valid, compared to 13% of the LeanCheck trees" for binary search trees. LeanCheck also beat
the type-derived random generator on tasks the random one solved only sometimes, which the authors
read as "situations where a deterministic approach may be more reliable than a random
alternative". Order matters once the budget cuts the enumeration short: enumerating
`(Int, Tree, Tree)` instead of `(Tree, Tree, Int)` took SmallCheck from timing out to an almost
immediate counterexample. Mittelman et al. [2023] reorder enumeration with covering arrays from
combinatorial testing (the ACTS tool of the US National Institute of Standards and Technology) and
report speedups above 20 times.

Combinatorial testing addresses the product of several finite domains. Kuhn, Wallace and Gallo
[2004] found that the failures in the systems they studied were triggered by interactions of few
parameters, which justifies covering arrays: a test set in which every combination of values of any
t parameters appears at least once, for small t (2 for pairwise). For a fixed t and a fixed number
of values per parameter, the smallest such array grows roughly with the logarithm of the number of
parameters, far below the size of their product.

Hypothesis shows the enumeration emerging from a sampler: when its engine has explored every
distinct sequence of choices (for example a test over `sampled_from` of a short list), it stops
with the reason "nothing left to do"
([engine.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/internal/conjecture/engine.py)),
possibly well before `max_examples`.

When exhaustive is preferable: the domain is finite and its product with the other parameters fits
the budget; the claim should be categorical over that finite set; the run must reproduce without a
seed; or the interesting values are few and known (sizes 0 and 1, the members of a census).
Sampling is preferable when the domain is infinite or very large, when bugs need medium-sized
inputs that a depth bound never reaches, and when the property has several parameters whose product
explodes; its claim is then statistical and tied to the generator's distribution (section 6).

Applicable to Luthier: Luthier's grades already separate exhaustive (all of a finite domain) from
bounded (a box in an infinite one). A census needs a grade of its own: it is exhaustive over a
declared finite subset of the type and says nothing about the rest, so something like "census of
k" (k the number of members) keeps it from being read as exhaustive over the type. The product of several finite generators
grows fast (k functions times m matrices times p sizes); past the case budget, a pairwise covering
array over the parameters is a better use of the budget than sampling the product at random, by
Kuhn et al.'s evidence. When the enumeration is cut by the budget its order decides what gets
tested, and size order (LeanCheck's tiers) returns the smallest counterexample first. When a
sampler's range is small and finite, Hypothesis's behaviour is the one to copy: detect that the
space is exhausted, stop, and report the grade exhaustive. SmallCheck's depth for s·2^e gives an enumeration of small floats on a log scale, should a bounded grade over
Float64 be wanted.

## 5. Generators for vectors and matrices

Random orthogonal matrices. The Haar measure on the orthogonal group O(n) (the n×n real matrices Q
with QᵀQ = I, where I is the identity) is its unique probability measure invariant under left and
right multiplication by orthogonal matrices; it is what "uniformly random orthogonal matrix" means.
The standard recipe takes the QR factorization G = QR of an n×n matrix G with independent standard
normal entries (Q orthogonal, R upper triangular) and fixes the signs, Q ← Q diag(sign(diag(R))),
where diag(R) is the vector of R's diagonal entries and diag(v) the diagonal matrix with v on its
diagonal; in MATLAB `[Q,R] = qr(randn(n)); Q = Q*diag(sign(diag(R)));`
([Higham, "What is a random orthogonal matrix?"](https://nhigham.com/2020/04/22/what-is-a-random-orthogonal-matrix/)).
The sign correction is needed because the factorization is unique only once the signs of diag(R)
are fixed; Mezzadri [2007] shows numerically, for the complex case, that a library QR without it
returns unitary matrices whose eigenvalue statistics are wrong: "the output is not distributed with
Haar measure".
Stewart [1980] builds the same distribution as a product of n - 1 Householder reflections of growing
size, at 4n³/3 flops against 2n³ for the QR route; Higham notes that "a random Householder matrix is
not Haar distributed". SciPy offers
[`ortho_group`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ortho_group.html)
(citing Mezzadri) and
[`special_ortho_group`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.special_ortho_group.html)
(determinant +1). For test matrices with prescribed singular values the Haar property is optional:
Fasi and Higham [2021] drop it to generate extreme-scale test matrices in time linear in the number
of entries.

Symmetric positive definite (SPD) matrices. The cheap construction is BᵀB + δI, where B is an n×n
matrix with independent standard normal entries, I the n×n identity and δ > 0 a constant; PyTorch's
test utilities use AAᵀ + 10⁻⁵I and, for the Hermitian case, AAᴴ + I
([common_utils.py](https://github.com/pytorch/pytorch/blob/main/torch/testing/_internal/common_utils.py)).
The smallest eigenvalue of BᵀB + δI is at least δ, but its condition number is whatever BᵀB
happens to give, bounded only by (λ_max + δ)/δ, where λ_max is the largest eigenvalue of BᵀB. A Wishart matrix (the sum of k outer
products xxᵀ of independent normal vectors x with covariance Σ) is the statistical version
([`scipy.stats.wishart`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wishart.html),
sampled by the Bartlett decomposition, Smith and Hocking [1972]). To control the spectrum, take
Q diag(λ) Qᵀ with Q Haar orthogonal and λ a chosen vector of positive eigenvalues. Random
correlation matrices (SPD with unit diagonal) have two standard generators: Davies and Higham
[2000] for a prescribed spectrum whose eigenvalues sum to n
([`scipy.stats.random_correlation`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.random_correlation.html)),
and Lewandowski, Kurowicka and Joe [2009] for a density over all correlation matrices.

Prescribed singular values or condition number. Write A = U diag(s) Vᵀ, where A is m×n, U (m×m)
and V (n×n) are Haar orthogonal, s is the vector of the k = min(m, n) singular values, and diag(s)
is the m×n matrix with s on its diagonal and zeros elsewhere. The 2-norm condition number of A is
κ = max(s)/min(s). LAPACK's generator xLATMS
([dlatms.f](https://github.com/Reference-LAPACK/lapack/blob/master/TESTING/MATGEN/dlatms.f)), which
"generates random matrices with specified singular values (or symmetric/hermitian with specified
eigenvalues) for testing LAPACK programs", sets s from a mode and COND = κ:

- MODE = 1: s₁ = 1 and s₂ = ... = s_k = 1/COND (one large singular value);
- MODE = 2: s₁ = ... = s_{k-1} = 1 and s_k = 1/COND (one small singular value);
- MODE = 3: s_i = COND^(-(i-1)/(k-1)) for i = 1, ..., k (geometric, that is, log-spaced);
- MODE = 4: s_i = 1 - (i-1)/(k-1) (1 - 1/COND) (arithmetic);
- MODE = 5: random in (1/COND, 1) "such that their logarithms are uniformly distributed";
- MODE = 6: random from the same distribution as the rest of the matrix;
- a negative mode reverses the order, and in the symmetric case random signs are applied.

The routine also takes a bandwidth, a norm to scale to, and a packing, and "checks for consistency
among the specified matrix properties" [Demmel and McKenney 1989]. xLATMT adds a RANK argument
that zeroes s_{RANK+1}, ..., s_k
([dlatmt.f](https://github.com/Reference-LAPACK/lapack/blob/master/TESTING/MATGEN/dlatmt.f)).
Higham's `randsvd` (modes 1 to 5, default mode 3 and κ = sqrt(1/ε), with ε the machine precision)
is the MATLAB counterpart [Higham 1991; Higham 1995], now `gallery('randsvd', ...)` in MATLAB.

How LAPACK picks test matrices. The working note that introduced the generators says "thorough
testing requires test matrices with a range of condition numbers and scalings (i.e., with norms near
the overflow and underflow thresholds)" [Demmel and McKenney 1989]. The general-matrix driver uses
eleven types
([dchkge.f](https://github.com/Reference-LAPACK/lapack/blob/master/TESTING/LIN/dchkge.f),
[dlatb4.f](https://github.com/Reference-LAPACK/lapack/blob/master/TESTING/LIN/dlatb4.f)): diagonal;
upper triangular; lower triangular; general with κ = 2; general with the first column, the last
column, or the last half of the columns set to zero; κ = sqrt(0.1/ε); κ = 0.1/ε; norm scaled near
underflow; and norm scaled near overflow. The dimensions come from an input file whose default is
0, 1, 2, 3, 5, 10 and 50 for both m and n, with ranks of 30%, 50% and 90% of n for the
rank-revealing routines
([dtest.in](https://github.com/Reference-LAPACK/lapack/blob/master/TESTING/dtest.in)).

Why ill-conditioning has to be constructed. Edelman [1988] shows that an n×n matrix with independent
standard normal entries has a condition number κ of order n: the expected natural logarithm of κ is
ln n + 1.537 asymptotically. Viswanath and Trefethen [1998] show that a lower triangular matrix with
independent standard normal entries is exponentially ill-conditioned: κ_n^(1/n) → 2 almost surely,
where κ_n is the condition number at dimension n. So a "random matrix" with independent,
identically distributed entries is well conditioned when dense and badly conditioned when
triangular, and in neither case does it reach a chosen κ such as 0.1/ε.

Low rank and nearly singular matrices. The product of an m×r and an r×n matrix, both with
independent standard normal entries, has rank at most r; U diag(s) Vᵀ with s_{r+1} = ... = s_k = 0 has rank exactly r (PyTorch
`random_square_matrix_of_rank`, LAPACK xLATMT). A nearly singular matrix is mode 2 with a large COND.
PyTorch's `random_matrix(..., singular=True)` sets two singular values to zero, the second one to
"increase the order of singularity so that the pivoting in LU factorization will be non-trivial".

Named distributions in numerical libraries. PyTorch's test utilities have one function per
distribution: `random_well_conditioned_matrix` (singular values from a normal with mean 1 and
standard deviation 0.001), `make_fullrank_matrices_with_distinct_singular_values` (singular values
in [2/3, 3/2], condition number 9/4), `random_symmetric_pd_matrix`, `random_hermitian_psd_matrix`,
`random_lowrank_matrix`, `random_sparse_matrix` and others. JAX's test utilities name element
distributions and let each test pick one
([test_util.py](https://github.com/jax-ml/jax/blob/main/jax/_src/test_util.py)): `rand_default`
(normal times 3), `rand_nonzero`, `rand_positive`, `rand_small` (normal times 10⁻³),
`rand_not_small`, `rand_some_equal`, `rand_some_zero` (half the entries zero), `rand_some_inf` (10%
+infinity and 10% -infinity), `rand_some_nan`, `rand_some_inf_and_nan`, `rand_fullrange` (random bit
patterns), `rand_uniform(low, high)`. NumPy's linear algebra tests
([test_linalg.py](https://github.com/numpy/numpy/blob/main/numpy/linalg/tests/test_linalg.py)) use
a census of hand-written cases, each tagged `square`, `nonsquare` or `hermitian` (mutually
exclusive) and optionally `generalized` (stacked), `size-0` or `strided`; they cover 0×0, 1×1,
8×8 random, 8×11, 1×5, 5×1, 0×4, 4×0, several dtypes and plain nested lists, and each test selects
cases with `check_cases(require=..., exclude=...)`. Hypothesis's `arrays(dtype, shape, *, elements,
fill, unique)` ([reference](https://hypothesis.readthedocs.io/en/latest/reference/strategies.html))
separates the shape strategy from the element strategy and draws a single `fill` value for every
coordinate not drawn individually, which yields arrays with many repeated values and is "essential
if you want your tests to run in reasonable time" for large arrays.

Collections of named test matrices. Higham's Algorithm 694 [Higham 1991] (45 parametrized matrices,
the origin of MATLAB's `gallery`), Anymatrix [Higham and Mikaitis 2022] and TypedMatrices.jl
[Zhang et al. 2025], whose purpose is to "help users select test cases based on their properties",
are censuses of matrices labelled by property (symmetric, positive definite, ill conditioned,
and so on).

Tolerances for identity tests. Deadman and Higham [2016] test matrix functions through identities
such as e^(log A) = A and (A^(1/p))^p = A, and show how "a linearized perturbation analysis for a
functional identity allows the determination of a maximum residual consistent with backward
stability". The admissible residual grows with condition numbers of the functions involved, so a
fixed tolerance is either too strict on ill-conditioned inputs or too loose on well-conditioned
ones; they also note that some gallery matrices are known to be hard for the algorithms tested.

Applicable to Luthier: Luthier's array generators draw entries uniformly in [-size, size]
(`_vec`, `_mat` in `arrays.py`), SPD matrices as BᵀB + I (`gen_spd_of`), rank-deficient ones as
Gram matrices of fewer vectors (`gen_deficient_of`), and dimensions from 1 to 8 (`gen_dim`).
Edelman's result is for normal entries, and a quick simulation of the current generators at size 16
(20000 draws of 8×8 matrices, run for this survey) agrees: entries uniform in [-16, 16] give a
median κ of about 23, a 99th percentile of about 1.2·10³ and a largest value of about 6.6·10⁵,
and BᵀB + I gives a median of about 420 and a 99th percentile of about 2.4·10³, where LAPACK
tests κ = sqrt(0.1/ε) ≈ 2·10⁷ and κ = 0.1/ε ≈ 4.5·10¹⁴ (ε = 2⁻⁵² for 64-bit floats). Laws about
solving, inverting or factoring are therefore never tested where floating point hurts. The LAPACK
scheme transfers directly: a matrix generator parameterized by structure, spectrum mode (one large, one small,
geometric, arithmetic, log-uniform), κ, norm scaling (near underflow and overflow) and rank, with
orthogonal factors from QR with sign correction, and a deliberate list of sizes. Distributions that
correspond to a predicate (orthogonal, SPD, rank r, κ ≤ some bound) are refinement types, which
Luthier supports; those that differ only in distribution need the naming mechanism of section 1.
Mezzadri's example shows that checking a generator's values against the type is not enough: QR
without sign correction passes the predicate QᵀQ = I and still has the wrong distribution. A
generator that claims Haar or log-uniform could carry that claim as a distributional law and be
certified the way `Kernel` is, with a probability integral transform and a Kolmogorov-Smirnov test,
which is close to what Luciano's note in `random.lut` asks of the random library (an invariant of
stochasticity and tests of it). For tolerances, a generator that returns the dependent pair
(κ, A) lets a law state its tolerance as a function of κ, following Deadman and Higham, so the
tolerance follows the conditioning of each input.

## 6. Coverage and distribution reporting

QuickCheck ([Test.QuickCheck](https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck.html),
section "Analysing test case distribution") has `label`, `collect`, `classify` and `tabulate`, which
attach labels to test cases and print the percentage of cases per label after the run, and
`labelledExamples`, which finds a shrunk example for each label. `cover p cond name` asks that at
least p% of successful cases satisfy `cond`; by default a shortfall only prints a warning ("Only
26% non-trivial, but expected 50%"), because "the coverage varies randomly". `checkCoverage` turns
the requirements into a test: "QuickCheck uses a statistical test to account for the role of luck
in coverage failures. It will run as many tests as needed until it is sure about whether the
coverage requirements are met. If a coverage requirement is not met, the property fails." Its
parameters are `certainty` (default 10⁹: a property whose requirement is met fails spuriously at
most once in that many runs) and `tolerance` (default 0.9: a required level p is accepted when the
true level is at least 0.9 p). The implementation
([Test.hs](https://github.com/nick8325/quickcheck/blob/master/src/Test/QuickCheck/Test.hs)) checks
when the requested number of tests is reached and then at 200, 400, 800, ... tests, until it can
decide; a requirement is met when the lower Wilson score bound for the observed proportion, at
error 1/certainty, reaches tolerance times p, and fails when the upper bound falls below p. Hughes [2019] uses these tools to find that in 79% of his tests a key drawn
independently of a tree was absent from it, and fixes the key generator; the same section shows
that `x /= y` fails in 3.3% of cases with QuickCheck's default `Int` generator and in 9.3% with a
smaller key type, so the choice of generator decides how often equal values meet.

Hypothesis ([API reference](https://hypothesis.readthedocs.io/en/latest/reference/api.html)) has
`event(value, payload)`, whose percentages appear with `--hypothesis-show-statistics` next to the
counts of passing, failing and invalid cases and the reason the run stopped ("100 passing, 0
failing, and 32 invalid test cases", "Retried draw from integers().filter(...) to satisfy filter",
"Stopped because settings.max_examples=100"). `target(observation, label)` steers generation toward
inputs that maximize a numeric observation, after Löscher and Sagonas [2017]; the documentation
suggests metrics such as "floating-point error", warns that targeting is "not always a good idea",
and shows a test of associativity of float addition on [0, 10¹⁰⁰] that "almost always passes"
without `target(difference)`. Observability
([integrations reference](https://hypothesis.readthedocs.io/en/latest/reference/integrations.html#observability))
writes one JSON line per test case with its status (passed, failed, gave_up), a representation of
the input, the arguments, how it was generated, its features (events and target scores), the lines
it covered and its timing. Tyche [Goldstein et al. 2024b] displays these records and defines the
OpenPBTStats format, which has optional fields "naming the particular generator that was used to
produce a value".

Practice. Of the 30 Jane Street developers interviewed [Goldstein et al. 2024], 11 said they "did
not think as hard as they should about testing effectiveness"; those who checked their tests used
mutation testing (7 of 30), inspection of examples (8 of 30) or code coverage (2 of 30).

What a passing sampled test supports. With n independent draws from a generator and no failure,
the probability p that one more draw from the same generator fails is below p_u = 1 - 0.05^(1/n),
approximately 3/n, with 95% confidence: the rule of three [Hanley and Lippman-Hand 1983]. Here n is
the number of passing cases and p_u the upper confidence bound on p. The statement concerns the
generator's distribution only; it says nothing about values the generator gives probability zero or
almost zero.

Applicable to Luthier: The certificate already records the generator, the case count, the seed and
the first cases. Three additions follow from the prior art. Declared classifications per law
(QuickCheck's `classify` and `tabulate`, Hypothesis's `event`) with their counts, so the
certificate says what share of cases fell in each region a reader cares about (near the bounds, κ
above 10⁸, a census function versus a random table). Coverage requirements checked with
QuickCheck's sequential Wilson test, so a law fails when its generator doesn't reach a region the
author named. And the stop reason with the counts of vacuous, rejected and not-run cases, as
Hypothesis prints them, possibly as OpenPBTStats records if a viewer such as Tyche is wanted. The
sampled grade can then carry a number, the rule-of-three bound 3/n on the failure probability under
that generator, printed next to the generator's description (bounds, scale, special values), since
it covers nothing outside that distribution. For laws with tolerances, a targeted search that
maximizes residual over tolerance is a cheap way to look for near-failures. The negative controls
Luthier already writes (`offByThree` in `rational.lut`, the control runs of `experiment_zero`) are
the hand-made mutation testing that FitSpec automates and that the Jane Street developers do by
hand.

## 7. Generators that cannot reach a type

Rejection sampling draws from a base generator and keeps the values that satisfy a predicate. If a
fraction r of the base draws satisfies it, each accepted value costs 1/r draws on average, and the
accepted values follow the base distribution conditioned on the predicate, which can be far from
the distribution one wants (Etna's enumerated binary search trees: 1% valid, and the valid ones
small).

QuickCheck's `suchThat` "generates a value that satisfies a predicate": it tries sizes n to 2n,
then recurses with size n + 1 for ever
([Gen.hs](https://github.com/nick8325/quickcheck/blob/master/src/Test/QuickCheck/Gen.hs)), so an
unsatisfiable predicate never returns; `suchThatMaybe` returns `Nothing` "if it fails to do so after
enough attempts". Preconditions written with `==>` discard test cases, and a run gives up once the
discards reach `maxDiscardRatio` (default 10) times the number of tests requested (default 100),
printing "*** Gave up! Passed only" followed by the counts of passed and discarded tests.
Hedgehog's `Gen.filter` ([Hedgehog.Gen](https://hackage.haskell.org/package/hedgehog/docs/Hedgehog-Gen.html))
retries up to 100 times, growing the size by 2k at the k-th retry, then discards the case: "To avoid looping
forever, we limit the number of retries, and grow the size with each retry. If we retry too many
times then the whole generator is discarded." Hypothesis has `.filter(pred)` and `assume(cond)`;
its health check `filter_too_much` fires "when the test is filtering out too many test cases"; a
run in which fewer than 1% of cases satisfy the assumptions stops and says so ("but < 1% of test
cases satisfied assumptions"); and a test with no valid case at all raises `Unsatisfiable`. Hypothesis describes a health check as "a proactive
warning, not an error", and all but two of them concern performance.

Turning filters into construction. Hypothesis rewrites simple filters into bounds
([filtering.py](https://github.com/HypothesisWorks/hypothesis/blob/master/hypothesis/src/hypothesis/internal/filtering.py),
"Tools for understanding predicates, to satisfy them by construction", active since 6.12.0 in
2021): `integers().filter(lambda x: x > 9)` becomes `integers(min_value=10)`, and later releases
added rules for `math.isfinite` on floats, length predicates on collections and regular expressions
on text; the changelog adds "we continue to recommend using the efficient form directly wherever
possible". Hughes [2019] gives the discipline for hand-written generators: a property `prop_ArbitraryValid t = valid t`
that tests the generator itself, and the same for the shrinker, because "it is vital to test
generators and shrinkers independently of the operations under test". Luck [Lampropoulos et al.
2017] is a language where a generator is the predicate itself, annotated to say which variables to
instantiate and which to constrain, and where the distribution is controlled. QuickChick derives
generators from inductive relations [Lampropoulos, Paraskevopoulou and Pierce 2018]: from the
inductive definition of a property it builds a generator that produces only values satisfying it.
Claessen, Duregård and Pałka [2014] derive generators from a Boolean predicate that are uniform over
the satisfying values of a given size, pruning with lazy evaluation of the predicate on partial
values.

Soundness and completeness. Paraskevopoulou et al. [2015] give a generator a semantics as the set
of values it can produce with nonzero probability and prove in Coq that a generator is sound (only
values of the intended type) and complete (every such value possible). The motivation is that
incomplete testing code fails silently: "testing a weaker or just a different property can succeed
although the artifact under test is completely broken with respect to the property of interest".

Applicable to Luthier: Luthier currently sits between these libraries. A refinement without a
generator is drawn by rejection from its base type for up to 2000 tries and then reported with
"give it a `gen`"; a registered generator whose value fails the type's predicate is an error that
names the generator, which is stricter than Hypothesis and is Hughes's validity test applied to
every draw. Once every generator is explicit, rejection becomes a combinator the program writes (a
filter over a named generator), and its acceptance rate should be measured and recorded per
generator, with a threshold below which the test is an error, in the spirit of `filter_too_much`
and QuickCheck's discard ratio. The certificate should also state that a filtered generator samples
the base distribution conditioned on the predicate. Construction should be preferred wherever the
predicate permits: interval predicates can be rewritten into bounds for sampling, as `int_interval`
already does for enumeration and as Hypothesis's filter rewriting does, and refinement types
defined through constructors or inductive relations are the case QuickChick derives generators for.
Luthier checks soundness on every value, but nothing checks completeness, so each generator's reach
belongs in the certificate: a single typical value reaches one point (grade "point"), a census
reaches its k members, and a sampler reaches what its bounds, scale and special values allow.

## Bibliography

Andoni, A., Daniliuc, D., Khurshid, S. and Marinov, D. (2002). Evaluating the "small scope
hypothesis". Manuscript, MIT.
https://www.semanticscholar.org/paper/0c6d97fbc3c753f59e7fb723725639f1b18706bb

Bergstra, J. and Bengio, Y. (2012). Random search for hyper-parameter optimization. Journal of
Machine Learning Research 13, 281-305. https://jmlr.org/papers/v13/bergstra12a.html

Bernardy, J.-P., Jansson, P. and Claessen, K. (2010). Testing polymorphic properties. ESOP 2010,
LNCS 6012, 125-144. https://doi.org/10.1007/978-3-642-11957-6_8

Braquehais, R. (2017). Tools for discovery, refinement and generalization of functional properties
by enumerative testing. PhD thesis, University of York (includes LeanCheck).
https://etheses.whiterose.ac.uk/19178/

Braquehais, R. and Runciman, C. (2016). FitSpec: refining property sets for functional testing.
Haskell Symposium 2016. https://doi.org/10.1145/2976002.2976003

Braquehais, R. and Runciman, C. (2017). Speculate: discovering conditional equations and
inequalities about black-box functions by reasoning from test results. Haskell Symposium 2017,
40-51. https://doi.org/10.1145/3122955.3122961

Claessen, K. (2012). Shrinking and showing functions (functional pearl). Haskell Symposium 2012,
73-80. https://doi.org/10.1145/2364506.2364516

Claessen, K., Duregård, J. and Pałka, M. H. (2014). Generating constrained random data with uniform
distribution. FLOPS 2014, LNCS 8475; extended in Journal of Functional Programming 25 (2015).
https://doi.org/10.1007/978-3-319-07151-0_2

Claessen, K. and Hughes, J. (2000). QuickCheck: a lightweight tool for random testing of Haskell
programs. ICFP 2000, 268-279. https://doi.org/10.1145/351240.351266

Claessen, K., Smallbone, N. and Hughes, J. (2010). QuickSpec: guessing formal specifications using
testing. Tests and Proofs 2010, LNCS 6143. https://doi.org/10.1007/978-3-642-13977-2_3

Davies, P. I. and Higham, N. J. (2000). Numerically stable generation of correlation matrices and
their factors. BIT Numerical Mathematics 40, 640-651. https://doi.org/10.1023/A:1022384216930

de Vries, E. (2023). falsify: internal shrinking reimagined for Haskell. Haskell Symposium 2023,
97-109. https://doi.org/10.1145/3609026.3609733

Deadman, E. and Higham, N. J. (2016). Testing matrix function algorithms using identities. ACM
Transactions on Mathematical Software 42(1), article 4. https://doi.org/10.1145/2723157
(preprint: https://eprints.maths.manchester.ac.uk/2114/1/paper.pdf)

Demmel, J. and McKenney, A. (1989). A test matrix generation suite. LAPACK Working Note 9.
https://www.netlib.org/lapack/lawnspdf/lawn09.pdf

Duregård, J., Jansson, P. and Wang, M. (2012). Feat: functional enumeration of algebraic types.
Haskell Symposium 2012, 61-72. https://doi.org/10.1145/2364506.2364515

Edelman, A. (1988). Eigenvalues and condition numbers of random matrices. SIAM Journal on Matrix
Analysis and Applications 9(4), 543-560. https://doi.org/10.1137/0609045

Fasi, M. and Higham, N. J. (2021). Generating extreme-scale matrices with specified singular values
or condition number. SIAM Journal on Scientific Computing 43(1), A663-A684.
https://doi.org/10.1137/20M1327938

Goldstein, H., Cutler, J. W., Dickstein, D., Pierce, B. C. and Head, A. (2024). Property-based
testing in practice. ICSE 2024. https://doi.org/10.1145/3597503.3639581

Goldstein, H., Tao, J., Hatfield-Dodds, Z., Pierce, B. C. and Head, A. (2024b). Tyche: making
sense of property-based testing effectiveness. UIST 2024. https://doi.org/10.1145/3654777.3676407
(preprint: https://harrisongoldste.in/papers/uist24-tyche.pdf)

Hanley, J. A. and Lippman-Hand, A. (1983). If nothing goes wrong, is everything all right?
Interpreting zero numerators. JAMA 249(13), 1743-1745.
https://jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf

Higham, N. J. (1991). Algorithm 694: a collection of test matrices in MATLAB. ACM Transactions on
Mathematical Software 17(3), 289-305. https://doi.org/10.1145/114697.116805

Higham, N. J. (1995). The Test Matrix Toolbox for Matlab (version 3.0). Numerical Analysis Report
276, Manchester. https://nhigham.com/wp-content/uploads/2023/10/high95m.pdf

Higham, N. J. and Mikaitis, M. (2022). Anymatrix: an extensible MATLAB matrix collection.
Numerical Algorithms. https://doi.org/10.1007/s11075-021-01226-2

Hughes, J. (2019). How to specify it! A guide to writing properties of pure functions. Trends in
Functional Programming 2019, LNCS 12053. https://doi.org/10.1007/978-3-030-47147-7_4
(preprint: https://research.chalmers.se/publication/517894/file/517894_Fulltext.pdf)

Jackson, D. (2006). Software Abstractions: Logic, Language, and Analysis. MIT Press.

Jeuring, J., Jansson, P. and Amaral, C. (2012). Testing type class laws. Haskell Symposium 2012,
49-60. https://doi.org/10.1145/2364506.2364514

Koopman, P. and Plasmeijer, R. (2006). Automatic testing of higher order functions. APLAS 2006,
LNCS 4279. https://doi.org/10.1007/11924661_9

Kuhn, D. R., Wallace, D. R. and Gallo, A. M. (2004). Software fault interactions and implications
for software testing. IEEE Transactions on Software Engineering 30(6), 418-421.
https://doi.org/10.1109/TSE.2004.24

Lampropoulos, L., Gallois-Wong, D., Hriţcu, C., Hughes, J., Pierce, B. C. and Xia, L. (2017).
Beginner's luck: a language for property-based generators. POPL 2017, 114-129.
https://doi.org/10.1145/3009837.3009868

Lampropoulos, L., Paraskevopoulou, Z. and Pierce, B. C. (2018). Generating good generators for
inductive relations. Proceedings of the ACM on Programming Languages 2 (POPL), 45.
https://doi.org/10.1145/3158133

Lewandowski, D., Kurowicka, D. and Joe, H. (2009). Generating random correlation matrices based on
vines and extended onion method. Journal of Multivariate Analysis 100(9), 1989-2001.
https://doi.org/10.1016/j.jmva.2009.04.008

Löscher, A. and Sagonas, K. (2017). Targeted property-based testing. ISSTA 2017.
https://doi.org/10.1145/3092703.3092711

MacIver, D. R. (2016). Integrated vs type based shrinking. https://hypothesis.works/articles/integrated-shrinking/

MacIver, D. R. (2017). Moving beyond types. https://hypothesis.works/articles/types-and-properties/

Mezzadri, F. (2007). How to generate random matrices from the classical compact groups. Notices of
the AMS 54(5), 592-604. https://arxiv.org/abs/math-ph/0609050

Mittelman, S. E., Resnick, A., Perez, I., Goodloe, A. E. and Lampropoulos, L. (2023). Don't go down
the rabbit hole: reprioritizing enumeration for property-based testing. Haskell Symposium 2023.
https://doi.org/10.1145/3609026.3609730

Papadakis, M. and Sagonas, K. (2011). A PropEr integration of types and function specifications
with property-based testing. Erlang Workshop 2011. https://doi.org/10.1145/2034654.2034663

Paraskevopoulou, Z., Hriţcu, C., Dénès, M., Lampropoulos, L. and Pierce, B. C. (2015).
Foundational property-based testing. ITP 2015, LNCS 9236, 325-343.
https://doi.org/10.1007/978-3-319-22102-1_22

Reynolds, J. C. (1972). Definitional interpreters for higher-order programming languages.
Proceedings of the ACM Annual Conference; reprinted in Higher-Order and Symbolic Computation 11(4),
1998. https://doi.org/10.1145/800194.805852

Runciman, C., Naylor, M. and Lindblad, F. (2008). SmallCheck and Lazy SmallCheck: automatic
exhaustive testing for small values. Haskell Symposium 2008, 37-48.
https://doi.org/10.1145/1543134.1411292

Shi, J., Keleş, A., Goldstein, H., Pierce, B. C. and Lampropoulos, L. (2023). Etna: an evaluation
platform for property-based testing (experience report). Proceedings of the ACM on Programming
Languages 7 (ICFP), 218. https://doi.org/10.1145/3607860 (preprint: https://lemonidas.github.io/pdf/ETNA.pdf)

Smallbone, N., Johansson, M., Claessen, K. and Algehed, M. (2017). Quick specifications for the
busy programmer. Journal of Functional Programming 27, e18. https://doi.org/10.1017/S0956796817000090

Smith, W. B. and Hocking, R. R. (1972). Algorithm AS 53: Wishart variate generator. Applied
Statistics 21, 341-345.

Stewart, G. W. (1980). The efficient generation of random orthogonal matrices with an application
to condition estimators. SIAM Journal on Numerical Analysis 17(3), 403-409.
https://doi.org/10.1137/0717034

Verdonk, B., Cuyt, A. and Verschaeren, D. (2001). A precision- and range-independent tool for
testing floating-point arithmetic I: basic operations, square root, and remainder. ACM Transactions
on Mathematical Software 27(1), 92-118. https://doi.org/10.1145/382043.382404

Viswanath, D. and Trefethen, L. N. (1998). Condition numbers of random triangular matrices. SIAM
Journal on Matrix Analysis and Applications 19(2), 564-581. https://doi.org/10.1137/S0895479896312869

Zhang, A. et al. (2025). TypedMatrices.jl: an extensible and type-based matrix collection for
Julia. https://arxiv.org/abs/2503.11355

Recent work not used above but close to Luthier's situation: pun, a small functional language with
properties built in and automatic input generation (https://arxiv.org/abs/2309.04696); Programmable
property-based testing, which reifies properties as data separate from their runners
(https://doi.org/10.1145/3828685); Loaded Dice, which tunes generator weights against an objective
distribution (OOPSLA 2025, https://arxiv.org/abs/2508.14394); and a community bibliography of PBT
papers (https://github.com/ngernest/pbt-bibliography).
