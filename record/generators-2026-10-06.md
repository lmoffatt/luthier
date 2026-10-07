# Generators named by the test: an analysis for the specification

2026-10-06. Luciano's decision, in two parts. A type has no single generator: the same type is drawn
one way for one purpose and another way for another (a typical value, a census, a distribution with
these bounds or with a logarithmic scale). Therefore every test names the generator it used for each
type it draws, and the certificate records it. A generator may be as simple as one typical value, but
it is written down.

This fits the principle of his note on what types are for in Luthier (`Lucianos ideas
dir/funcion de los tipos en Luthier.txt`): belonging to a type is a certificate that a value passed
the type's check, and a costly result carries in its type what produced it (the vector `map_opt`
returns is "optimal for beta_ini, fun and x", not only "a vector"). A certificate of a law is such a
result: it says that the law passed on cases drawn by these generators, and without the generators
it says less than it seems to.

He also raised three questions: how to generate values of function types (his proposal: in the
simplest case, a census of the registered values), how to declare numbers (fixed limits, and a linear
or a logarithmic scale), and how to have several generators for vectors, useful for different cases.

This document analyses the decision and the questions against the interpreter as it is and against
the prior art, so that a specification can be written from it. Each section ends with what it
proposes; section 14 lists what remains to decide.

Sources: an inventory of what the tester draws today and how
(`docs/ideas/generators-inventory-2026-10-06.md`, with file and line references), and a survey of
property-based testing (`docs/ideas/generators-prior-art-2026-10-06.md`, with its bibliography); both
were written for this document. References in brackets point to that bibliography.

## 0. Terms

- A *test* evaluates a law on *cases*. A *case* gives a value to each parameter the law mentions.
- A *generator* of a type `T` gives values of `T`. In `lib/random.lut` it is
  `Gen T = Nat -> Int -> T * Int`: a *size* and a *seed* give a value and the next seed. A generator
  is a value with a name, like any other definition.
- The *support* of a generator is the set of values it can give with nonzero probability; its
  *distribution* is how likely each one is. A refinement type `{ x : T | P x }` (with `P` its
  predicate) names a support and says nothing of a distribution.
- A *binding* maps each type a test draws to the generator the test uses for it. A *profile* is a
  named binding, declared once and used by several tests.
- A *census* is a finite list of values given explicitly; testing over it can be exhaustive.
- The *grade* of a certified law says how it was tested (`05 §7`: point, sampled, bounded,
  exhaustive, and the others).
- The *reach* of a generator is what a certificate can say it covered: one point, the k members of a
  census, or the bounds, scale and special values of a distribution.
- A *domain type* is a named refinement whose predicate says where a law is claimed to hold, such as
  `TestedFull` (positions within 5 m, sigma between 1 and 10 cm) in `distances.lut`.

## 1. Where things stand

Today a type has at most one generator. `gen T := g` registers it (05 R7: a generator given to an
alias is the generator of the type the alias stands for, and a second generator for one type is an
error), and a type without one is drawn by the first of fifteen structural rules that applies
(`generators.py`, `sample`). There are 29 `gen` declarations, 19 in the libraries and 10 in the
project. What the tester draws, by kind of type:

- Numbers: integers uniform on [-s, s] and doubles on a grid of spacing s·10^-6 over [-s, s], with s
  the size, at most 16; rationals with denominators up to 10^6; strings of the letters a, b, c, x, y,
  z. `NormalDouble`, with a uniform binary exponent, is the only generator that spans magnitudes.
- Vectors and matrices: lengths from a `Nat` (zero with probability 1/(s+1)), dimensions up to 8,
  entries independent and uniform on [-s, s]; SPD matrices (symmetric positive definite) as BᵀB + I,
  every eigenvalue at least 1; deficient ones as Gram matrices of fewer vectors, with a clean gap at
  the retention threshold.
- Records: one component at a time, unless registered (`Table`, the graphs).
- Refinements: by rejection, up to 2000 draws; quantified laws inside a type (the record laws of
  `Table`, `Objective`) probed five times.
- Functions over infinite domains: constants, or affine maps on `Float64 -> Float64`; dependent
  function types (`Step`, `Maximizer`) and `U`: nothing, the law is not run.

The inventory orders the problems by how much they weaken what a certificate means. The five that
bear on this design:

1. A passed law can rest on few cases and say nothing about it. A case whose later parameter cannot
   be drawn is dropped after 50 redraws; a case of a type obligation whose computation raises is
   skipped; and premises a generator never meets make laws pass vacuously. `drawGaussian` passed on
   24 counted cases of 100, because a precision drawn as a random matrix is not a precision;
   `firstViolation` on graphs that never have the columns its premises ask for; `parseTable` on
   strings none of which parses. A certificate is accepted by the `n` its test requested, not by the
   cases it counted.
2. The drawn domains stop short of where numerical code fails and of the experiment's own inputs.
   Tolerances, steps and the settings of Levenberg-Marquardt are drawn on (0, 16] or [-16, 16], far
   from the 10^-6 to 10^-16 in use; no matrix is ill conditioned; no layout is nearly degenerate; and
   the graph generator (3 to 8 nodes, prior sds from 0.01 to 2 m, a measurement error that is always
   positive) never reaches session A (10 nodes, prior sds from 0.001 to 3 m).
3. A registered generator draws a well-behaved part of its type and nothing measures how much: valid
   graphs only for `GraphWithColumns`, never more than five columns for `Table`, exactly one defect
   for `BrokenGraph`.
4. Records drawn one component at a time are mostly not members of the concept their laws are about:
   a `GaussianBelief` with a non-symmetric precision, a `MapInput` with negative standard deviations,
   an `LMState` with negative damping and a negative iteration count, an `Objective` only at
   dimension 0, an `Ensemble` never (it needs at least 100 draws, and a `Nat` stops at 16).
5. Which generator drew a type depends on the program that ran the test. `VecOf` has a generator only
   where `array_python.lut` is loaded, `TestedFree` only where `distances_python.lut` is,
   `ValidDistanceGraph` only where `distance_graph_python.lut` is. Tested in their own files,
   `distances.lut`'s domains are unreachable (an acceptance of about 1.5·10^-9) and every law of
   `distance_graph.lut` over a valid graph times out; through `--imports`, a certificate carries
   whichever context ran it.

The others: functions are constants (18 laws), generic laws over `U` are never run (30 laws), the
certificate misdescribes some draws (a `Fin` parameter is reported as a rejection over `Int`, and the
five sample cases kept are always the smallest), and cost (nested rejection, predicates that run
code) pushes the directives toward few cases and small sizes, which feeds problems 1 and 2.

Problems 2 to 5 have one root: the generator is treated as a property of the type, chosen once,
implicitly, and the certificate does not say which one it was.

## 2. The principle: the test names its generators

Statement.

- A generator is a named value. A type may have any number of them, and none is *the* generator of
  the type. Libraries and projects define the generators they find useful: a typical value, a census,
  uniform or logarithmic distributions with bounds, the structured families of matrices of section 5.
- A test states, for every type it draws, the generator it uses: its binding. Two parameters of the
  same type that need different generators are bound per parameter. A type the binding leaves out
  makes the law not run, with the type named. The interpreter has no structural default of its own.
- The certificate of a law is the claim "the law passed on n evaluated cases drawn by these
  generators", and its identity includes the binding (each generator's name and fingerprint). One law
  has as many certificates as bindings it was tested under. "Certified" is always "certified under a
  binding".

A sketch, with a profile so that naming every generator does not mean repeating it in each test:

    -- the generators of the project's tape model, used by its tests
    profile tape := {
      Seed        := uniformSeed,
      TestedFull  := scaledPositionsWithin freeDim positionBox (log sigmaLow) (log sigmaHigh),
      TestedFree  := positionsWithin freeDim positionBox,
      Float64     := linearFloat (0.0 - 10.0) 10.0 }

    test fullPair with 5 under tape
    test addRounds with 300 under { NormalDouble := logDouble 1.0e-150 1.0e150 either 0.02 }

What changes with respect to today:

- `gen T := g`, one per type, goes. In its place a generator is an ordinary definition of type
  `Gen T` (or of a generator family, a function from the type's arguments to a `Gen`), and the rule of
  R7 about generators of aliases, with the error for two of them, has nothing left to regulate.
- Problem 5 of section 1 disappears: a test draws with what it names, whatever files the program
  loaded.
- Domain types keep their role. A domain type says where a law is claimed to hold (its support); the
  binding says how the evidence was gathered inside it (the distribution, or a census, or one value).
  Changing the first changes the claim; changing the second changes the certificate.
- Composition is a generator like any other. A record without laws, a pair, a sum, a function over
  `Fin n`: a binding may map them to `byComponents`, which draws each component with the binding's
  generator for its type, dependent components after the ones they depend on. It is never applied
  without being named, since composing declared generators can still give values nobody meant, as a
  `MapInput` with random standard deviations, some of them negative.

Why. The prior art agrees: Hedgehog, Hypothesis and proptest make the generator a value the test
names (`forAll gen`, `@given(x = ...)`, a strategy expression), and QuickCheck, which ties one
generator to each type, needs a new type (`Small`, `Large`) for each other distribution of the same
values, a workaround its critics point to. MacIver gives the reason that applies to a language with
refinement types: a type is a predicate that consumes a value and a generator produces one, so a
generator is not determined by its type. And the distribution is part of what a passing test
establishes (section 3): the same law passing under a typical-value generator and under a generator
of ill-conditioned matrices are different pieces of evidence, and the certificate has to say which
it is.

Proposal: generators as named values, many per type; every test binds each type it draws, by a
profile or inline; the binding part of the certificate's identity; `gen T :=` removed.

## 3. Kinds of generators, and the grade each earns

Four kinds, by what they give:

| kind | gives | grade of a law that passes |
|---|---|---|
| value | one typical value | point |
| census | each of k listed values, in order | census of k |
| enumeration | every value of a finite type (`Fin n`, `Bool`, a small product) | exhaustive |
| distribution | random draws, with declared bounds, scale and special values | sampled n |

and three ways of combining them: a mixture (draw from one of several generators, with weights), a
construction (draw arguments from their generators and apply a function, as `objectiveAt t seed`
builds an objective from a layout and a seed), and a filter (draw from a generator and keep the
values that satisfy a predicate). A filter samples the base distribution conditioned on the
predicate, which may be far from the distribution wanted, and costs the inverse of its acceptance
rate in draws; it is written explicitly, its acceptance rate is recorded, and below a threshold the
law is not run.

The value generator is the least a test can declare: Hypothesis's `just(v)` and `@example(v)`,
Hedgehog's `Gen.constant`. A law tested on one value is an example, and its grade says so.

The census needs a grade of its own. It is exhaustive over a declared finite part of the type and
says nothing of the rest, so reading it as exhaustive over the type would overstate it. When a law
has several census parameters, their product may exceed the budget of cases; a covering array, which
contains every pair of values of any two parameters, is a better use of the budget than a random
sample of the product [Kuhn et al. 2004].

A sampled grade can carry a number: with n evaluated cases and no failure, the probability that one
more draw from the same generators fails is below about 3/n at 95% confidence (the rule of three
[Hanley and Lippman-Hand 1983]). It concerns the generators' distribution only, which is one more
reason the certificate must name them.

Every value a generator gives is still checked against the predicate of its type, as today: Hughes's
validity test of a generator, applied to every draw. Completeness, that every value of the type can
be drawn, cannot be tested; the certificate states the reach of each generator instead.

Proposal: the four kinds and three combinations; grades point, census of k, sampled n (with 3/n),
exhaustive, bounded; the reach of each generator in the certificate.

## 4. Numbers

A numeric generator is declared by the parameters the libraries converge on [Hedgehog Range,
Hypothesis `integers` and `floats`, proptest, fast-check]:

- bounds, each closed or open;
- a scale: *linear*, uniform between the bounds, or *logarithmic*, uniform in the logarithm of the
  magnitude, which gives every interval [c, 2c] inside the bounds the same probability;
- for a logarithmic scale, a positive lower bound on the magnitude, a sign (positive, negative or
  either) and, when zero is a legitimate value, an atom at zero with its probability; this is what
  `NormalDouble`'s generator does today (sign and binary exponent uniform, zero 2% of the time), and
  what Bergstra and Bengio do for a penalty that is zero half the time;
- special values with their total probability: the bounds and their neighbours, zero, one, minus one,
  and the literals of the program itself (Hypothesis has drawn the program's literals since 2025, and
  thresholds such as `zMax >= 3` or `draws >= 100` are where off-by-one errors sit);
- for `Float64`, a continuous draw (any double between the bounds); the grid of `genFloat64`
  (2 000 001 points) is an accident of its implementation.

NaN and the infinities are not values of `Float64` in Luthier (`core.lut`), so they never enter a
generator; laws about the doubles near their limits draw from refinements such as `NormalDouble`.

Integers follow the same declaration: bounds, linear or logarithmic (a signed bit length, as
Hypothesis now does), special values. A seed is an integer drawn uniformly over its whole range
(`Seed`, 2^31 values, already so).

Scale follows meaning. A standard deviation, a distance, a tolerance and a condition number are scale
quantities, naturally logarithmic; a coordinate, a residual or a log-likelihood is a location
quantity, naturally linear. `TestedFull` already draws sigma on a logarithmic scale (log sigma
uniform between log 0.01 and log 0.1). The generator still states its scale.

Size. With bounds declared per generator, the global size (1 to 16, growing over the run) stops
deciding numeric ranges; it keeps a role for lengths of vectors and lists and the depth of recursive
data, where "small first" gives small counterexamples. proptest's criticism of a single global size
applies to the current `genInt` and `genFloat64`, uniform in [-size, size].

A sketch of the library, in `random.lut`:

    linearFloat (lo hi : Float64) : Gen Float64
    logFloat (lo hi : Float64) (sign : Sign) (zero : Float64) : Gen Float64   -- zero: probability of 0
    linearInt (lo hi : Int) : Gen Int
    withSpecials (p : Float64) (values : List A) (g : Gen A) : Gen A        -- p: probability of a special
    value (v : A) : Gen A
    census (vs : List A) : Gen A

Proposal: numeric generators declared by bounds, scale (linear or logarithmic, with sign and zero for
the logarithmic), and special values with a probability; continuous doubles; the size out of numeric
ranges.

## 5. Vectors and matrices

A vector generator is a dimension generator and an entry generator. The dimensions deserve a list as
much as a range: LAPACK tests every routine at 0, 1, 2, 3, 5, 10 and 50, and the empty and the
one-dimensional cases are where shapes break. Entries come from a numeric generator of section 4.

Structured families, each a generator in its own right, for what each is for:

| family | construction | what it tests |
|---|---|---|
| entries iid | each entry from a numeric generator | the generic case |
| unit vector | a Gaussian vector divided by its norm | directions, uniform on the sphere |
| probability vector | Dirichlet | weights, simplices |
| positions in a box | uniform coordinates within bounds | the layouts of the project |
| symmetric | B + Bᵀ | spectral routines |
| SPD, spectrum given | Q diag(λ) Qᵀ, Q Haar orthogonal, λ positive | inversion, square roots, Cholesky |
| orthogonal | QR of a Gaussian matrix, signs fixed by diag(R) | rotations, the factors of the others |
| prescribed singular values | U diag(s) Vᵀ, s by a mode and a condition number κ | conditioning |
| low rank r | U diag(s) Vᵀ with s_{r+1} = ... = 0 | rank, pseudo-inverses |
| nearly singular | the smallest singular value 1/κ | solves near singularity |
| scaled | any of the above times a power of two near under- or overflow | scaling |
| diagonal, triangular | by structure | the special paths of routines |

where B is a matrix of iid standard normal entries, Q, U and V are Haar orthogonal matrices (the
uniform distribution on orthogonal matrices, obtained from the QR factorization G = QR of a Gaussian
G with Q multiplied by the signs of the diagonal of R), diag(λ) is the diagonal matrix of a vector λ,
and κ = max(s)/min(s) is the condition number. The modes of s are LAPACK's (xLATMS): one large value,
one small value, geometric, arithmetic, log-uniform.

Why ill-conditioning has to be built. A matrix with iid Gaussian entries has a condition number of
the order of its dimension [Edelman 1988]. The survey measured the current generators: 8 x 8 matrices
with entries uniform in [-16, 16] have a median κ of about 23 and a largest κ of about 6.6e5 in
20 000 draws; `SpdOf`, built as BᵀB + I, a median of about 420. LAPACK tests κ = sqrt(0.1/ε) ≈ 2e7
and κ = 0.1/ε ≈ 4.5e14, with ε = 2^-52. The laws of solving, inverting and factoring in `array.lut`
are never tested where floating point hurts.

This is where several generators for one type matter most. `solve` is one leaf with one law; it is
certified once under a well-conditioned generator, and once more under an ill-conditioned one, and
the two certificates say different things, both true. A domain type would be wrong here, since the
law is claimed for every matrix.

Two refinements. A generator that claims a distribution (Haar, log-uniform singular values) can be
wrong in a way the type cannot see: Mezzadri shows that QR without the sign correction passes
QᵀQ = I and still gives the wrong distribution. Such a claim is a law of the generator, certified as
a kernel is, with a probability integral transform and a Kolmogorov distance; this is the invariant
of stochasticity Luciano's note in `random.lut` asks of the random library. And a generator can give
the pair (κ, A), so that a law states its tolerance as a function of κ [Deadman and Higham 2016]
instead of one fixed tolerance, too strict on ill-conditioned inputs and too loose on the others.

Proposal: vector and matrix generators parameterized by a dimension generator (a list, by default
0, 1, 2, 3, 5, 10) and an entry generator; the structured families of the table in `array.lut` and
`array_python.lut`; the condition number as a parameter where it applies; distributional laws for
the generators that claim a distribution.

## 6. Several certificates for one law

With generators named by the test, a law has a certificate per binding, and three things need rules.

- What a name's state is. `check -v` lists, for each law, its certificates by binding, each with its
  grade and reach. "Certified" alone stops being a state of a name.
- What a run requires. `luthier run` reports, for each law in the cone of its entry, the bindings it
  is certified under. A project states what its runs require, as a profile (the tape's), and
  `--require-certified` checks the cone against it.
- Domain types and bindings, kept apart. When the claim changes (the law holds only inside a box), the
  place is the law's type: a domain type, as `DensityPairOn D at` already does. When only the
  evidence changes (the same claim tested with typical values, with edge values, on a linear or a
  logarithmic scale), the place is the binding. A predicate cannot tell these apart: uniform and
  log-uniform on one interval have the same support, which is why QuickCheck needs `Small` and
  `Large`.

Proposal: certificates keyed by law and binding; `check -v` and the run record list them; projects
declare the profile their runs require.

## 7. Function types

Functions over finite domains are drawn as their tables, from the binding's generator for the
codomain; that is Claessen's `Table`, and it is `byComponents` for a function over `Fin n`.

For infinite domains, Luciano's proposal is the census of the registered values: a function type is
drawn from the functions of that type the program registers, each case one of them, and the law can be
tested exhaustively over that census. It has close relatives: QuickSpec enumerates terms from a
signature of the program's functions, Conjure from listed "ingredients", Hypothesis resolves an
abstract class to the union of its registered subclasses, and type-class laws are tested instance by
instance. Its footing is Reynolds's defunctionalization: a program contains finitely many lambda
abstractions, so every function that can reach a higher-order parameter is one of them, closed over
some captured values.

What it gains. The functions drawn are the ones the laws are about, so a passing law speaks of the
program's own functions: the likelihoods it defines, the maximizers it runs. Every function has a
name, so a counterexample is shown by name. The test over a finite census can be exhaustive. And it is
what certifying a theory's laws per model already does.

What it loses. A census is biased toward well-behaved functions; the counterexamples that random tables
find are non-monotone, or constant almost everywhere, or separate values a law treats as equal, and a
program rarely defines such functions. It is not closed under composition: a law over f and g sees only
the listed pairs. An empty census makes the law vacuous and a census of one makes it a point check,
which the grade shows.

Three decisions follow.

- What "registered" means. Either every value of that type the program defines, collected by the
  checker, or an explicit list. Under this document's principle the list is explicit, and a census is
  one more named generator; `check -v` can show the candidates the program defines, for the author to
  choose from:

      likelihoods : Gen (Likelihood FullCoords (Vec Float64)) := census [fastFull, nativeFull]

  An implicit census would also make a certificate's meaning depend on unrelated definitions, since
  adding a function of the same type would change it.
- Families. A census member may be an abstraction with captured values: `objectiveAt t seed` is a
  family of objectives indexed by a layout and a seed. Its captured values are drawn by the binding's
  generators for their types, so the member stands for the whole family; the current fallback
  `\ x { a * x + b }` is this, a census of one abstraction with a and b drawn.

      objectives : Gen Objective := census [from objectiveAt]          -- t and seed drawn by the binding

- Records with function fields and laws (`Objective`, `Likelihood`, `Sampler`, `BeliefFamily`,
  `Maximizer`): these are the case the census serves best, since random functions almost never satisfy
  their laws (a constant gradient is not the gradient of a constant), which is why the laws over them
  stay not run today.

Random functions remain useful for laws that must hold for every function (the laws of a fold, of a
map): a function drawn lazily, memoized per argument, and shown as the finite table of the calls a case
made plus a default (QuickCheck's `Fun`, Hypothesis's `functions(pure = True)`). It is another
generator for the same function type, chosen by the binding.

Equality of functions is not structural (R8), so a law that compares two functions compares their
values at points drawn by the binding's generator for the domain.

Proposal: functions over finite domains as tables; over infinite domains, a census given as an explicit
list of names and families; random memoized functions as a later generator.

## 8. Type parameters

An obligation of code generic in `(Theta : U)` is never run today: there is no generator of types. The
census applies one level up: a binding may map `U` to `census [Int, Float64, VecOf 3]`, the types a
generic law is tested at, and the binding then needs a generator for each of them. Bernardy, Jansson
and Claessen show that for a parametric property a single well-chosen instance can stand for all of
them. For the libraries this means that the internal obligations of `diagnose`, `ShiftComposes` or
`IsGradient` run at the types the census lists, instead of nowhere.

Proposal: a census of types as the generator of `U` in a binding, where a library wants its generic
obligations run.

## 9. Refinements and dependent types

Construction first. A refinement is drawn by a generator that builds its values (positions within a
box, a valid graph, a vector of nodes apart from the first ones); a filter is the explicit exception
(section 3). Interval predicates on integers and doubles can be rewritten into bounds, as
`int_interval` already does for enumeration and Hypothesis does for sampling. Every value is checked
against the predicate.

Families. A generator of a family of types is a function of the family's arguments: the generator of
`VecOf k` receives k, the generator of `Pairs p i` receives p and i. Today the arguments reach a Python
generator converted without their types, so a vector arrives as the pair of its length and its
entries; a generator's arguments should be converted by their declared types, as an extern's are.

Aliases. A binding's key is a type with its aliases unfolded (R7), so `Node p`, an alias of
`Fin (p.n / 3)`, is drawn by the binding's generator for `Fin`; that alias went through rejection over
`Int` until this week, and the obligation of `point` took 185 s instead of 1.

Dependent records. Components are drawn in order, each with the earlier ones in its type; when a
component's type is empty for the earlier ones (entries of `Fin 0` in a vector of length three), the
earlier ones are drawn again (done this week).

Proposal: constructive generators for refinements; filters only explicit; generator arguments
converted by type.

## 10. Edge cases, coverage, and the laws of generators

Edge cases enter through the special values of the numeric generators (section 4) and the dimension
lists of section 5. Beyond them, a law can name regions of its input space and ask for them:

- *classify*: a law, or a generator, labels each case (near a bound, κ above 1e8, a census member);
  the certificate records the share of cases per label;
- *cover*: a law asks that a label hold in at least a given share of the cases; the requirement is
  checked statistically, as QuickCheck's `checkCoverage` does with a sequential Wilson bound, so a law
  fails when the generators it is bound to do not reach a region its author named;
- the certificate records why a run stopped and how many cases were vacuous, filtered or not run.

A generator that claims a distribution has a law of it (section 5): the probability integral transform
of its values is uniform, tested with the moments and the Kolmogorov distance already in
`probability.lut`. This gives the random library the invariant Luciano's note asks for.

Proposal: classify and cover, with the statistical check; distributional laws for generators that
claim a distribution.

## 11. Size, enumeration, budgets

The size keeps the role of section 4: lengths, dimensions when a generator draws them from a range,
depth of recursive data, growing over the run so that a counterexample is small. A test directive
bounds it (`size k`), and a generator may ignore it. The schedule should reach the largest size even
with few cases (today a run of 5 cases stops at size 13 of 16). When the cases a census or an
enumeration offers number fewer than the directive asks, the test stops when they are exhausted and
reports the census or exhaustive grade. When the product of finite parameters exceeds the budget, a
pairwise covering array chooses the cases.

## 12. What a certificate records

For each law: the binding (for each type or parameter, the generator, its kind and parameters: bounds,
scale, special values and their probability; the members of a census; the predicate and acceptance
rate of a filter; and its fingerprint), which is part of the entry's identity; the grade (point, census
of k, sampled n with the bound 3/n, exhaustive, bounded); the labels and their shares; the stop reason
and the counts of vacuous, filtered and not-run cases. A reader of a certificate can then say where a
law was tested, and where it was not.

The n of a sampled grade counts the cases that were evaluated to a verdict. Cases dropped because a
parameter could not be drawn, skipped because the computation of a type obligation raised, and cases in
which a premise was false are counted apart, and a certificate is accepted only if its evaluated cases
reach the n of the directive. A premise (the left side of an implication, the condition of a branch
that carries the obligation) is a label in the sense of section 10, so the certificate says how often
it held; a law whose premises never held passed vacuously and is reported so.

## 13. Migration

Every type of the inventory's section 4 needs at least one generator, named, and every test a binding.
Most generators exist or are compositions of ones that do; the 29 `gen` declarations become named
generators. Grouped by what each needs:

- Scalars (`Int`, `Nat`, `Float64`, `Rational`, `String`, `Bool`, `Seed`): the generators of
  `random.lut`, rewritten with declared bounds, scale and special values (section 4). `String` needs
  more than six letters: digits, separators, quotes, line breaks, so the laws of the table format see
  texts that parse.
- Quantities that are scales (a tolerance, a step, the settings of Levenberg-Marquardt, a widening, a
  sigma): logarithmic generators over the range in use (for a tolerance, 10^-16 to 10^-1). Today they
  are drawn on (0, 16].
- Dimensions, vectors and matrices (`Dim`, `VecOf`, `MatOf`, `MatRows`, `Square`, `SymmetricSquare`,
  `SpdOf`, `DeficientOf`): the generators of `array_python.lut` with a list of dimensions that reaches
  0 and 10, and the structured families of section 5, the condition number among their parameters.
- Records with laws: `Table` (its generator, with more columns and rows); `Objective`, `Likelihood`,
  `Sampler`, `BeliefFamily`, `Maximizer` (censuses of the program's instances and families, section
  7); `Ensemble` and `PitResolution` (censuses of the values the project uses, or a value).
- Records without laws that stand for a concept: a generator that builds a member of the concept.
  `GaussianBelief n`: a mean and an SPD precision. `LMState n`: a point, its value, a damping on a
  logarithmic scale between the schedule's bounds, an iteration count from 0. `MapInput` and `Design`:
  from a valid graph (`toMapInput`, `designOf`). `LMSettings`: a tolerance on a logarithmic scale and a
  budget. `Fit n` is better not drawn at all: `transformOf` can take the graph and the settings and
  compute the fit it needs.
- Sums and data (`Maybe`, `List`, `Cell`, `SigmaTreatment`): `byComponents`, named in the binding.
- Functions over infinite domains and dependent function types: censuses (section 7). The 18 laws drawn
  today with constant functions name the census they need: the leaves `add`, `sub`, `scale` for the
  operations of `algebra_python.lut`; the maps 1/√x and the pseudo-inverse for `spectralMap`; the
  project's samplers, likelihoods and maximizers for theirs.
- Type parameters: a census of types where a library wants its generic obligations run (section 8).
- The project's domain types: `Positions` built (a multiple of three coordinates, not a rejection);
  `Pairs`, `SeparatedPairs`, `PairsAmong`, `PositionsWithin`, `ScaledPositionsWithin`, `GraphDir` as
  they are; for `ValidDistanceGraph` and `CompleteGraph`, a second generator that reaches session A (up
  to a dozen nodes, prior standard deviations from 0.001 to 3 m, a measurement error of either sign);
  for `GraphWithColumns`, one that includes graphs with bad rows; for `BrokenGraph`, one with several
  defects.

Each test file gets the profiles its tests use: `array_python.lut` a profile of the leaves (and a
second, ill-conditioned one for the solvers), `distances_python.lut` the tape's, `distance_graph_python`
the graphs'. A pure library (`array.lut`) whose generators are written in Python declares its
profiles in its binding file, so its own tests run where the profile is visible, and report the
missing generator anywhere else.

Order of work: first make the certificate honest (counted cases, the reasons of the others, premises as
labels, the binding in the identity), since that shows where each law stands; then the numeric and
array generators of the libraries, as named generators; then profiles for every test file; then the
records and the censuses; last, remove `gen T :=` and the structural defaults, with `check -v`
listing, until then, the laws whose types the binding leaves out.

## 14. Open questions for the specification

1. The syntax of a binding: per type, per parameter, or both; profiles as declarations or as values of
   a record type, and whether a profile can extend another.
2. The census: how families with captured values are written (`from objectiveAt`), and whether a census
   of a type includes members of its subtypes.
3. What a run requires: one profile per project, or a profile per law, and what `--require-certified`
   checks when a law has certificates under several bindings.
4. What counts toward n, and what minimum share of evaluated cases a sampled grade asks for.
5. Size: whether generators ignore it unless they declare otherwise, and the schedule that reaches the
   largest size with few cases.
6. Generators in Luthier or in Python. Luthier generators are visible and certifiable but slow; Luciano's
   note in `random.lut` asks for an extern random generator, in batches, with laws of stochasticity.
7. Distributional laws of generators: which generators must carry one (Haar orthogonal, log-uniform, the
   random generator itself), and how many draws certify it.
8. Special values: the default weights, and whether the program's literals join them.
9. The quantified laws of a type are checked on a generator's values with five probes; whether that is
   enough for a value the generator claims, or the generator's laws must be certified with their own
   test.
10. Shrinking, which named generators make possible (Hedgehog's integrated shrinking); left for later.
