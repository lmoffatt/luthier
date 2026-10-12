# 7. Tests and generators

Chapter 7 of the specification, draft 0, 2026-10-12. It rewrites `docs/spec/08-tests.md` (draft 1 of 2026-10-06, commit d12b554 as the brief names it), which turned the analysis `record/generators-2026-10-06.md` into rules with the decisions Luciano took on it the same day (`sonolocalizacion/Lucianos feedbacks/oct 6 0703.txt` and `oct 6 0734.txt`); the grades and the evidence cost follow `docs/principles.md` (L10, L9, L5.18) at its projection of 2026-10-12, and the code read is `src/luthier/generators.py`, `testing.py`, `certify.py`, `cli.py` and `lib/random.lut`. Written by Claude Sonnet 5.5. It realizes L10.3 and L5.18. The grammar changes of the source's section 12 are applied by chapter 2, not here. The decisions of 2026-10-06 have no ids, so the items that rest on them are `[proposed]` unless implemented:

- A type has no single generator, so every test says which generators it used, and its certificate records them.
- Generators are values of Luthier like any other. The random source is an extern whose laws of stochasticity are stated in Luthier; what is heavy runs as an extern.
- Generators are functors over types: when a type is well defined, its generator is obvious. So the generic generators are few (exhaustive, and sampled with a linear or a logarithmic metric), and sampling by a weight puts numbers and lists under one rule.
- Drawing a type is an error. There are generators only of defined types.
- The bounds of a number are part of its type, decided when the type is defined.
- A certificate says that a defined value belongs to a defined type. For a function the value is the function, and a run must use it inside what the certificate's generators covered. For the result of an analysis the value is the result, checked once, when it is produced.
- A statistical law declares its level and its power.

## §1 Notation

The notation of the specification is `spec 1`; what follows is local to this chapter.

`T`, `A`, `B` are types, `x : T` says that `x` has type `T`, and the subtype is as `spec 1` writes it. `U` is the type of types. A *case* gives a value to each parameter of a law, the parameters being the variables it quantifies over. A *test* evaluates the laws of a name on cases; `n` is the number of cases its directive asks for. `Gen T` is the type of the generators of `T` (spec 7.S1). The *size* `s : Nat` bounds lengths and depths. A *seed* is a value of `Seed`, an integer in [0, 2^31). The *support* of a generator is the set of values it gives with nonzero probability; its *measure* says how likely each part of the support is.

A *weight* `c : T -> Float64` is a non-negative function on the values of `T`: the density of a measure, with respect to counting on a finite support and to length on an interval of numbers. The source called it a cost; that word is kept for the values of laws (Terms), so a weight and a cost are different things here. `C` is the total weight of a support. A *binding* maps parameters, or types, to generators; a *profile* is a binding with a name. A *census* is a finite list of values given explicitly. The *reach* of a certificate entry is what its generators covered, parameter by parameter: one value, the `k` values of a census, a whole finite type, or an interval with its measure.

`α` is the *level* of a statistical law: the probability that it fails when the model it tests is correct. `β` is its *power* against a given wrong model: the probability that it fails then. `Φ` is the distribution function of the standard normal. `κ` is the condition number of a matrix, its largest singular value over its smallest. `ε̂(n, δ)` is the bound on the fraction of a distribution where a law fails, given `n` samples and the confidence 1 - δ (spec 7.S11).

## §2 Generators are values

**7.S1. A generator is a value of type `Gen T`.** [proposed] `Gen T = Nat -> Seed -> T * Seed`: a size and a seed give a value and the next seed, as in `lib/random.lut` today with `Seed` in place of `Int` (the file defines `Gen` over `Int` and defines `Seed` beside it). A generator is defined, typed and certified like any other value (L14.2), and its type states what it promises. Validity: every value it gives belongs to `T`; for `g : Gen { x : T | p x }` this is the obligation that `p` holds of the value `g` gives, for every size and seed, tested as the obligation of an extern is (spec 4). Distribution, when the generator claims one (orthogonal matrices drawn uniformly, a log-uniform number, the random source itself): a law that the probability integral transform of its values is uniform, certified as a statistical law is (spec 7.S17), with its own count of draws (spec 7.S8). The random source is an extern that gives seeds in batches; its laws (uniform values, independent successive draws) are stated in Luthier and certified like those of any extern. The act `gen T := g`, which made `g` the generator of `T`, is removed: no type owns a generator (spec 7.R1). Today the interpreter still registers generators by type with `gen`.

## §3 Generic generators are functors over the type

A generic generator takes a type and builds a generator of it by following the type's structure, the same way for every type. There are four, each with its parameters.

| generic generator | parameters | gives |
|---|---|---|
| `value v` | a value | `v`, always |
| `census vs` | a list of values; optionally a weight | each value of the list in turn, or draws from it by its weight |
| `exhaustive` | none | every value of a finite type |
| `sampled m` | a metric: `linear`, `log`, or a weight | draws by the inverse of the cumulative weight |

**7.S2. Sampling inverts a cumulative weight.** [proposed] To draw from a support with weight `c`, draw `u` uniform in [0, C) and return the first value at which the cumulative weight exceeds `u`. Over a finite list `v1, ..., vk` the cumulative weight at `vi` is the running sum `c(v1) + ... + c(vi)`. Over an interval [lo, hi] of numbers it is the integral of `c` from `lo` to `x`. The two metrics of numbers are two weights: `linear` is `c(x) = 1`, uniform between the bounds, and `log` is `c(x) = 1/|x|`, uniform in the logarithm of the magnitude, which needs a positive lower bound on the magnitude. A census with weights and a range of numbers are drawn by the same rule. Feat [Duregård, Jansson and Wang 2012] draws values of algebraic types in this way, indexing into the cumulative counts of the values of each size.

**7.S3. How the functors follow a type.** [proposed] `exhaustive` and `sampled m` apply to a type by its form, as the table gives.

| form of the type | `exhaustive` | `sampled m` |
|---|---|---|
| `Unit`, `Bool`, `Fin n` | every value | by weight, equal unless given |
| `Int`, `Nat` with bounds | every value between them | the metric over the bounds |
| `Int`, `Nat` without bounds | error (spec 7.R3) | the metric over [-s, s] or [0, s] |
| `Float64`, `Rational` | error (spec 7.R3) | the metric over the bounds, continuous; without bounds, error (spec 7.S4) |
| product, record | the product of the components | each component, dependent ones in order (spec 7.S7) |
| sum | each constructor with each payload | a constructor by weight, then its payload |
| `List A`, `Vec A` | every length up to the size, entries exhaustive | a length (spec 7.S5), then that many entries |
| function over `Fin n` | every table, when the codomain is finite | a table, each entry from the codomain |
| function over an infinite domain | error: bind a census (spec 7.R4) | error: bind a census (spec 7.R4) |
| the models of a theory | error: bind a census (spec 7.R4) | error: bind a census (spec 7.R4) |
| `{ x : T \| p x }` | the values of `T` where `p` holds | bounds when `p` is an interval, otherwise a filter (spec 7.S6) |
| `U` | error (spec 7.R2) | error (spec 7.R2) |

Today `generators.py` enumerates the tables of a function over `Fin n` up to a fixed count and draws by registered generators; the table is the design.

**7.R1. A test names its generators.** [proposed] The directive of a test names the functor it applies to every parameter (`with n` is `sampled` with `n` cases; `exhaustive`), the metric of `sampled`, and may bind single parameters, or types, to other generators, inline or through a profile:

    profile tape := { Seed := sampled linear, TestedFull := scaledPositionsWithin freeDim positionBox }

    test gaussianFamily with 100 sampled linear under tape where {
      n   := census [0, 1, 2, 3, 5],
      tol := sampled log }

A binding keyed by a parameter applies to that parameter in every law of the test; one keyed by a type applies to every parameter of that type, aliases expanded (spec 4). A parameter binding wins over a type binding, and a binding in `where` over one in the profile. A parameter that the functor cannot generate and that nothing binds is a static error, which names the parameter and the kind of binding it needs. The certificate records, for every parameter of every law, the generator that drew it, expanded (spec 7.S9). Binding by parameter is the base because it is the only form that tells two parameters of one type apart: in the example, `tol` and the entries of the mean are both `Float64`, and need different metrics. Today the directive is `test name [with n | exhaustive] [size k]`, with no bindings and no profile.

**7.R2. No generator gives a type.** [proposed] A binding of a parameter of type `U`, and a test of a law quantified over a parameter of type `U`, are static errors. A law over a declared type is certified per filling of the hole (spec 4), with the generators of the type that fills it, and a law over the models of a theory is certified per model (spec 7.R4). Few definitions should take a type as a parameter. The legitimate ones are containers (`List A`, `Vec A`) and the laws of `algebra.lut`, which are predicates applied at a concrete type where they are used. A test of a container names the instance it runs at; for a parametric property one well-chosen instance can stand for all of them [Bernardy, Jansson and Claessen 2010]. The libraries that quantify over a type where they mean a vector (`Theta : U` in `probability.lut`, `belief.lut` and `optimization.lut`, and `IsGradient` in `array.lut`) are to be rewritten over `VecOf n` with `n : Nat`, whose generators exist.

**7.R3. `exhaustive` applies to finite types only.** [proposed] Under `exhaustive`, a parameter of an infinite type (an integer without bounds, any `Float64`, `Rational` or `Real`) is a static error unless it is bound to a census. Lists are enumerated up to the size. When the product of the finite parameters exceeds a budget (spec 7.S8), the cases are a covering array of pairs [Kuhn et al. 2004], which contains every pair of values of any two parameters, and the grade says so (spec 7.S10). Today a type that cannot be enumerated stops the test with a message asking for `with n`.

## §4 Numbers

**7.S4. The bounds of a number are in its type; its metric is in its generator.** [proposed] The bounds of a numeric parameter belong to its type and are decided when the type is defined: a tolerance of Levenberg-Marquardt is not any positive double. `lmTol : { t : Float64 | 0.0 < t }` becomes a type with both bounds, and so do the tolerances of the libraries. A double without bounds in its type needs them from its binding (`sampled log in [1.0e-15, 1.0e-2]`). The metric is chosen by the generator. `linear` is the measure that does not change under translation, for quantities whose meaning does not change when they are shifted: a coordinate, a residual, a log-likelihood. `log` is the measure invariant under scaling, for quantities that keep their meaning under multiplication: a standard deviation, a distance, a tolerance, a condition number. A `log` metric over a type that contains 0 draws 0 as an atom, with a probability that is a parameter, and draws a sign when both signs are allowed. Special values join every numeric generator with a total probability (spec 7.S8): the bounds and their neighbours, 0, 1 and -1 when they are in the support, and the literals of the program that fall inside the bounds (thresholds such as `zMax >= 3` are where off-by-one errors sit). Doubles are drawn continuously between the bounds. NaN and the infinities are not values of `Float64` (`core.lut`), and no generator gives them.

## §5 Vectors and matrices

**7.S5. Dimensions from a census, entries from a numeric generator, structure from a family.** [proposed] A vector generator is a dimension generator and an entry generator. The dimensions default to the census 0, 1, 2, 3, 5, 10 (LAPACK tests at these and at 50), which a binding can change. Matrices with structure are drawn by named families, each a generator: unit vectors, uniform on the sphere; probability vectors (Dirichlet); positions in a box; symmetric; symmetric positive definite with a given spectrum; orthogonal, drawn uniformly (the Haar measure, from the QR factorization of a Gaussian matrix with the signs of the diagonal of R); prescribed singular values with a condition number `κ` and a mode (one large value, one small value, geometric, arithmetic, log-uniform), as LAPACK's xLATMS; low rank; nearly singular; scaled near underflow or overflow; diagonal and triangular. The constructions are those of section 5 of `record/generators-2026-10-06.md`. A family that claims a distribution states it as a law (spec 7.S1); Mezzadri shows that a QR without the sign correction gives orthogonal matrices with the wrong distribution, which their type cannot see. A family can give the pair (`κ`, A), so that a law states its tolerance as a function of `κ`.

The generic generators (spec 7.S2, spec 7.S3) and the families are to be written in Luthier (L14.2): the functors and the numeric generators in `lib/generators.lut`, the families in `lib/array.lut`, both `[proposed]` and not written. What exists is `lib/random.lut`: `Gen`, the congruential source `nextSeed`, `randBelow`, the generators `genInt`, `genNat`, `genBool`, `genFloat64`, `genList`, `genSeed`, and the type `Seed`; it has no census, no metric, no family.

## §6 Functions and theories

**7.R4. A function over an infinite domain is drawn from a census of models.** [proposed] A function over `Fin n` is a table (spec 7.S3). A function over an infinite domain, and a value of a theory (a labeled base with laws whose components are functions, such as `Objective`, `Likelihood`, `Sampler`, `Maximizer`), has no generic generator: a test binds it to a census, an explicit list of the program's values of that type.

    likelihoods : Gen (Likelihood FullCoords) := census [fastFull, nativeFull]
    objectives  : Gen Objective := census [from objectiveAt]

A member of a census may be a family, `from f`, where `f` builds a value from its arguments; the arguments are drawn by the binding's generators for their types, so the member stands for the family. This is the certification per model of spec 4, with the models listed. The census is explicit: an implicit one, every value of the type the program defines, would change a certificate's meaning when an unrelated definition is added. `check -v` lists the candidates the program defines. Random functions, drawn lazily and memoized per argument, are a later generator, for laws that must hold for every function (those of a fold or a map). Equality of functions is not structural (spec 4), so a law that compares two functions compares their values at points its binding draws.

## §7 Subtypes and dependent records

**7.S6. A subtype is drawn within its bounds or through a filter.** [proposed] An interval predicate (`lo <= x and x <= hi`, strict or not, on an integer or a double) gives the bounds of spec 7.S4, with no rejection. A subtype with any other predicate is drawn by its base's generator filtered by the predicate. The filter's acceptance rate is recorded, and the draw of one value gives up after a budget of tries (spec 7.S8), which makes the law not run with that reason. A subtype that a filter reaches too rarely is defined constructively, as the image of a construction whose arguments the functor draws, or bound to a named family. Every value a generator gives is checked against the predicate of its type; `generators.py` does this today, with the tries fixed in the code.

**7.S7. Dependent components are drawn in order.** [proposed] The components of a record or a pair are drawn in the order of their dependencies, each with the earlier ones in its type. When a component's type is empty for the earlier ones (the entries of `Fin 0`), the earlier ones are drawn again, up to a budget (spec 7.S8). Today `testing.py` redraws such a case a fixed number of times and counts it as holding vacuously when every draw meets an empty domain.

## §8 Budgets

**7.S8. Every budget is an argument of the test, recorded in the entry.** [proposed] This is L5.18 applied to tests: the interpreter holds no fixed number for any of these (today it holds some, named here). The budgets are the tries per value of a filter (2000 in the code); the redraws of a dependent record (50 in the code); the probes of a quantified law inside a type (5 in the code); the draws per evaluated case, as a multiple of `n`; the largest size, with a schedule that reaches it within the `n` cases; the product of finite parameters above which a covering array chooses the cases; the total probability of special values, and of the atom at 0 of a `log` metric; the runs that estimate a level (spec 7.S17), and the seeds per control that measure power (spec 7.S19); the count of draws that certifies the distribution of a generator (spec 7.S1). `luthier test` takes each as an option with a default, and every entry records the values it ran with. The source named 10 redraws; the code at the commit read has 50, and the figure is the code's.

## §9 Certificates of definitions

For a definition with laws, the value a certificate speaks of is the definition (a function, an extern, a model) and the type is its declared type. Its laws quantify over parameters, so the evidence is a sample, and the certificate says what the sample was drawn from. What a certificate is, its identity, its transport and certification by default are spec 6 (L10.4 to L10.7); this section keeps what is about the test.

**7.S9. The identity of an entry includes its binding.** [proposed] An entry is identified by the law, the hash of its cone (spec 6) and its binding, expanded: for each parameter, the generator that drew it, as a functor with its parameters or as a name with its fingerprint. One law has as many entries as bindings it was tested under, and "certified" is always "certified under a binding". An entry also records the seed, the budgets (spec 7.S8), the counts of spec 7.S12, the reach, the labels (spec 7.S14) and the time. Today the entry records the hash of the cone, the seed, the generation record (generators used, sizes) and the fingerprints of the generators; the binding is not yet in the hash.

**7.S10. Grades.** [decided D-2026-10-12-y] The grades are the five of Terms: proved, exhaustive, cases, sampled, assumed, with the domain and the evidence cost carrying what the older list said. A point is cases with one case; a census of `k` is cases; bounded is exhaustive on the box the domain names; witnessed is cases with a witness; sampled carries its evidence cost. When the parameters of a law are drawn differently, its entry lists the reach of each, and the grade is summarized by the weakest. The fields of the certificate are spec 6. Today `testing.py` labels a law exhaustive, bounded, sampled or certified, the last for a result taken from a stored entry.

**7.S11. The evidence cost of a sampled law.** [decided D-2026-10-12-r] A sampled law costs -log(1 - ε̂(n, δ)) nats of evidence, where ε̂ bounds the failure fraction and δ is the demand's parameter (D-2026-10-12-h). With no failure seen in `n` cases, ε̂ is 3/n at δ = 0.05 [Hanley and Lippman-Hand 1983], the rule of three: the probability that one more draw from the same generators fails is at most 3/n at 95% confidence. The conversion has a declared shape (statistics and δ in, a cost out) and is filled per theory (L10.3); the file that would state it in Luthier is `lib/evidence.lut`, `[proposed]` and not written. How these costs combine along a path is O1.

**7.S12. `n` counts evaluated cases.** [proposed] A case counts toward `n` when the law was evaluated to a verdict on it. Counted apart: cases whose parameters could not be drawn, cases skipped because the computation of a type obligation raised (spec 4), and cases where a premise was false (the left side of an implication, or the condition of the branch that carries the obligation). A test draws until `n` cases are evaluated or the budget of draws is spent, and an entry is accepted only if its evaluated cases reach the directive's `n`. A law none of whose cases evaluates is not run, with the counts as its reason. A law whose premises never held passed vacuously, and its entry says so. Today `testing.py` counts the evaluated cases and the skipped ones, and marks a law not run when no case evaluates; it does not count premises.

**7.S13. A known outcome is not recomputed.** [proposed] A test is deterministic given its code, its binding, its seed and `n`. An entry whose identity, seed and `n` match is reused whatever its outcome: a passed entry certifies, and a failed or not-run one is reported as known, with its date and reason, and not run again. `--deep` runs it again, and a new seed makes a new entry. Today the match is on the hash of the cone and `--deep` exists.

**7.S14. Labels and coverage.** [proposed] A law or a generator can label its cases (`classify`: near a bound, `κ` above 10^8, a member of a census, a premise that held), and the entry records the share of each label. A law can ask that a label hold in at least a given share of its cases (`cover`). The request is checked statistically, with a sequential Wilson bound as QuickCheck's `checkCoverage` does, and the law fails when its generators do not reach a region its author named.

**7.S15. What a run requires.** [proposed] `luthier run` requires, for each law in the cone of the entry, a passed entry whose reach covers what the run gives that law; certification is the default and has no opt-out (D-2026-10-12-y, L10.6), so a cone with an uncertified name is refused. The values the run receives (the holes filled by `--set`, such as `lmTol = 1e-12` or the directory of a graph) are compared with the reach when the run starts: inside the interval, or a member of the census. Values computed during the run are compared at each call when the run is `--checked`, and recorded as not compared otherwise. A reach equal to the support of the parameter's type contains every value the type admits, so a run whose values type-check is inside the reach of a test that sampled the whole type.

## §10 Certificates of results

**7.S16. A result is checked once, when it is produced.** [proposed] The result of an analysis (the maximum of a posterior, an evidence, a fit) is one value, produced by a run, and its type says what it is: an optimum of this function on these data from this start; an expensive result carries its inputs and its witness. Its membership in that type is checked once, where it is produced, by the forms of spec 5: the refined value, a witness, or a statistical verdict with its level. The check needs no generator, except for quantifiers inside the type (that no direction increases the function within a step of the optimum, say), which the check draws with generators it names. The outcome goes to the record of the run, `.run.json`, with the hash of the inputs that index the result (L5.6). Certificates of code, the `.cert.json` files, never hold results.

## §11 Statistical laws

A statistical law (the uniformity of draws, a density pair, the transform of residuals) does not settle a fact about its value: a correct model fails it with some probability, and a wrong one passes it with some probability. Its outcome is a verdict with its level, in the form spec 5 gives. The level `α` and the power `β` are parameters of the demand, never constants of the code (L5.18).

**7.S17. A statistical law declares its level.** [proposed] It returns its statistic, its level `α` and its outcome. `α` is computed from the law's parameters: from the null distribution of the statistic when it is known (for a statistic standardized to z and compared with the threshold `zMax`, `α = 2(1 - Φ(zMax))`; for a Kolmogorov distance, the tail probability it is compared with), and otherwise estimated by running the law on the model it tests, with the number of runs an argument (spec 7.S8), and recorded with its interval.

**7.S18. A failure is repeated once.** [proposed] A statistical law that fails is evaluated again, with an independent seed derived from the first, and fails when both evaluations fail. The entry records the first failure, and the level of the whole procedure: `α²` for a single-run level `α`, since the two evaluations are independent.

**7.S19. Power is measured on controls.** [proposed] A statistical law that has controls (models broken on purpose, as the negative controls of the kernel) records, for each control, its rate of detection over `k` seeds, with `k` an argument and a Wilson interval. With the repetition of spec 7.S18 that rate estimates `β²` for a single-run power `β`. A law whose rate on a control is below a threshold (an argument) is reported as weak, and a control it never detects as undetected. The data of 2026-10-06 show why power has to be measured. Fitted to session A, the Kolmogorov test of the transform of the residuals gave tail probabilities between 0.58 and 0.74 for fits whose sigma was 4.9, 15 and 31 cm. The transform is computed with the fitted sigma, so it does not see a problem of scale, and what does see one is an informative prior on sigma. The law passed each time, and nothing in its certificate said that it could not have failed.

## Open

- O1: the conversion of a sample's statistics to a cost and the algebra of costs (spec 7.S11, spec 7.S17 to spec 7.S19).
- O5: the decorated output, for the error of a result that carries one (spec 7.S16).
