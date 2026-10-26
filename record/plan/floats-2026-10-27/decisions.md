# Floating point as Luthier's flagship case: the design, and what is yours to decide

2026-10-27, Claude Fable 5.1, on `prompt-design.md` beside this file (9d53f79). Inputs: numbers.lth
and numbers_model.lut, core/properties/functions.lth (the transformer), report-bite-8, report-bite-11,
report-C1, report-B2, D-2026-10-17-f, D-2026-10-18-j, D-2026-10-25-a, L13, spec 11, concepts.md 9,
rational.py, kernel.py's `_primitive`. "Record" marks what the record settles, "literature" what a
book states (Higham 2002, Goldberg 1991, Muller et al. 2018, Johansson 2017 for Arb, Moore 1966),
"mine" what I propose. The execution is in `execution.md` beside this file.

## The design in plain words

Three objects, three names (record, 11.S1). The reals ℝ are a theory: the complete ordered field
(`realField`, an axiom, 11.R3) with the elementary functions `exp`, `log`, `sqrt`, `erf` added by
their defining identities. It has no total exact model: every computable realization decides
`x == y` only for some pairs, or rounds (mine, after Bishop's constructive reals, where equality is
undecidable). Its specimens, and where each is exact: the integers ℤ, exact everywhere; the rationals
ℚ, an ordered field exact on all of ℚ for the four operations and the comparisons, with no
completeness and no `exp` (11.S10); the doubles F, a finite subset of ℚ (every double is a rational,
`toQ` exact, 11.S12) with rounded operations, a model of `Doubles` and not of `Field` (11.S15).

The relation between ℝ and F is two maps and one law (literature; record 11.S13). The inclusion
ι : F → ℝ is exact. Rounding fl : ℝ → F takes a real to the nearest double, ties to even, on
[−Ω, Ω], Ω ≈ 1.8·10³⁰⁸ the largest double; it is monotone, odd, and fl ∘ ι is the identity. The
law: for x, y in F and op one of + − × /, x ⊕ y = fl(ι x op ι y) exactly, bit for bit (IEEE 754
§5.4.1: each operation is the correctly rounded exact one). From it and the rounding bound
|fl(t) − t| ≤ u|t|, u = 2⁻⁵³ the unit roundoff, on the normal range (2⁻¹⁰²² ≤ |t| ≤ Ω) follows the
standard model fl(x op y) = (x op y)(1 + δ), |δ| ≤ u (Higham 2002, eq. 2.4), and from the standard
model every bound Luthier states today (Lemma 3.1's γₙ = nu/(1 − nu), the 3γ₂ of numbers.lth, the
3γₙ of arrays.lth). The boundary, stated as the domain and never hidden: above Ω the result overflows
(IEEE gives ±∞; Luthier gives no value, 11.S7); below 2⁻¹⁰²² the relative bound fails and an absolute
one of 2⁻¹⁰⁷⁵ holds, sums and differences being exact there (Higham §2.5); 0/0, ∞ − ∞, `sqrt` of a
negative give NaN, an error (11.S7); the signed zero −0.0 is identified with 0.0 by `==` and no
operation of the core tells them apart, which is the right reading of ℝ (mine, to be confirmed by a
listed test). `Moderate` and `Tame` (numbers.lth) are the premises that keep every law inside.

The format as the parameter (his addition of 2026-10-27, "Float N debería ser, con Float64 y
Float32 como aliases"; the reading is the coordinator's and mine). An IEEE 754 binary format is
fixed by three integers, the precision p in bits and the exponent range (emin, emax) (IEEE 754-2008
§3.3; Muller et al. 2018 ch. 2), and everything above follows from them: u = 2⁻ᵖ, the smallest
normal 2^emin, Ω = (2 − 2¹⁻ᵖ)·2^emax, the spacing of 1 (`epsilon` = 2u), the absolute bound below the
normal range 2^(emin − p). The bit count alone does not fix a format: float16 and bfloat16 are both
16 bits with p = 11 and p = 8. So the theory is `Floats (fmt : Format)`, `Format = { p, emin, emax }`,
and `Float64` (53, −1022, 1023), `Float32` (24, −126, 127), `Float16` (11, −14, 15), `BFloat16`
(8, −126, 127) and the fp8 formats (e4m3: 4, e5m2: 3) are aliases at their parameters; every law of
numbers.lth is stated once over `fmt` with the bounds written from `fmt.p`, and `Moderate` and `Tame`
are functions of (emin, emax). The specimens: the kernel computes binary64 only (Python's float), so
the other formats are leaves (11.S2, a leaf is declared over what it receives): numpy's float32,
float16 and longdouble, and float32, float16, bfloat16 and fp8 on a GPU through PyTorch or JAX. The
exact reference below covers them all at no extra cost, every finite float of every binary format
being a rational, and it is where a format earns or loses its laws: a GPU that truncates instead of
rounding, or an fp8 unit, fails the correct-rounding law bit for bit and keeps only a widened bound
(mine; what the certification shows). Mixed precision (accumulate in one format, store in another,
the common case of GPU and machine-learning code) is a composition across formats: the conversion
fl_B : F_A → F_B is itself an operation with the transformer (1, u_B|x|) on the range of B, so a chain
that accumulates in Float32 and stores in BFloat16 composes as the accumulation's transformer then the
conversion's by the formula above, and its domain shrinks to B's range (overflow of the store is the
boundary). A decorated float carries it the same way: the ball's midpoint is converted and its radius
grows by the conversion's rounding, with the radius held in whichever format is wide enough for it
(Arb keeps a short radius; its precision is a parameter, P11).

The exact reference (mine; the brief's question). Since every double is a rational, the exact
x op y is computable in ℚ, and the law x ⊕ y = fl(ι x op ι y) is a Boolean law tested bit for bit:
`nearest (toQ x + toQ y) == x + y`. The textbook bounds then become testable exactly: a sum of n
doubles against its exact sum within γₙ₋₁ Σ|xᵢ| (Higham eq. 4.4), the dot product within γₙ Σ|xᵢyᵢ|
(eq. 3.5), each association of three within γ₂ of the exact sum, with no factor 3. The 3 of today's
laws is the price of measuring the error in floating point (report-bite-8): with the reference in ℚ
the distance and the bound are exact and the worst ratio is the theory's own tightness; the witness
(1, 2⁻⁵³, 2⁻⁵³) reaches a ratio near 1 against γ₂. What it costs: `Rational` constants and the four
operations in the kernel (today `Rational` is a primitive with no arithmetic; rational.py has the
host's `Fraction` and `nearest` unused), so a kernel edge under D-2026-10-27-a (the kernel in the
cone by content hash, changes transported by certified edges); a form `WithinExact` beside `Within`
with distance and bound in ℚ; and time, exact sums being bignum sums, so the exact lines list sizes
up to 10⁵. The old laws stay; the exact ones are the flagship's.

Three numbers of a computation, as Luthier objects (literature, Higham §1.5 and §1.6; record for the
first two). Let f be the ideal function and g its specimen. The forward error |g(x) − f(x)| at exact
inputs is the defect η of the transformer (L, η, D, r) of D-2026-10-25-a: a stability law states it
(`DotStable`). The condition number is the sensitivity L of the ideal f on D below the radius r: a
sensitivity law states it (`DotSensitive`); the relative condition number is L|x|/|f(x)|, a function
of the arguments like every bound (P11, every criterion is a parameter). The backward error is the
smallest β with g(x) = f(x′) for some x′ within β of x: a third form, mine, stated as a law of the
specimen with a constructed witness (for a sum, x′ᵢ = xᵢ(1 + θᵢ) with θᵢ read off the actual
roundings in ℚ) or, for linear algebra, by the residual formula LAPACK uses (Rigal and Gaches 1967:
‖Aŷ − b‖/(‖A‖‖ŷ‖ + ‖b‖) ≤ γ). The theorem "forward ≤ condition × backward" is then no new law: it
is `ComposeSound` (functions.lth) with the backward error as the input distance. This is the form
for the pseudo-inverse's laws, which keep a `tol` today because their forward error has no theorem
(report-C1): the backward error has one, the sensitivity is κ, and the forward claim holds only where
κu < 1, the radius D-2026-10-18-j (every numerical law states its range as a premise) already names.

The two compositions and where they meet. Static (record, D-2026-10-25-a question 3): a whole
computation is one transformer, composed along its cone, (L₂L₁, L₂η₁ + η₂, D₁ ∩ f₁⁻¹(D₂),
min(r₁, (r₂ − η₁)/L₁)); it is known before running and pulls a demand's ε back to the inputs' δ
(L6.8, the tolerance charged at a node is the demand's pulled back through the sensitivity).
Dynamic (literature): a decorated float carries its error with its value, a midpoint m and a radius
ρ with the exact value in [m − ρ, m + ρ] (ball arithmetic, Johansson 2017; intervals, Moore 1966,
IEEE 1788; affine forms, Stolfi and de Figueiredo 2004); each operation gives the new radius from the
actual values, |m₂|ρ₁ + |m₁|ρ₂ + ρ₁ρ₂ for a product plus the midpoint's rounding. The meeting
(mine): the ball through an operation is that operation's transformer evaluated at the actual point,
radius L(m)·ρ + η(m); the static transformer is the same bound taken as a function over D. Both are
sound; the ball is sharper where L varies over D (cancellation: the relative sensitivity of x − y is
(|x| + |y|)/|x − y|), the transformer is a priori and is the only one that can plan (a pull-back needs
the bound before the value exists). One law relates them, `RadiusWithinTransformer`: the radius a ball
reaches is at most the composed transformer's bound at its midpoint.

Whether he is right (mine). Yes, in this form: a concluded computation hands over a value with a
radius, a ball, and composing it with a further computation applies the next transformer to that
ball, L·ρ + η; so the decorated float is the interface between concluded computations. Two functions
not yet run compose without decoration (`composeAffine`), except that the domain D₂ is checked at
f₁(x) and a value-dependent L is read at the actual value, and that evaluation at the point is the
ball. So the theory applies to both; the ball is the theory at a point, and it is what the user of a
simulation receives: a number and how far to trust it.

The failures, shown. Cancellation is sensitivity, a law whose L grows without bound near x = y, and
a relative demand there pulls back to an infeasible δ (L13.5, a cutoff is read against the
realization's defect at the point where it is met; the tape of concepts 9.4). Ill-conditioning is κu
reaching 1: the backward law holds, the forward claims nothing, the region sampled on both sides of
the boundary. Accumulation is γₙ growing with n: three specimens of one theory `Summation`, the
recursive sum (γₙ₋₁), the pairwise sum (γ_⌈log₂ n⌉, Higham §4.2) and Kahan's compensated sum (2u plus
a second-order term, §4.3), each certified exactly, and a demand that only one of them meets.
Non-associativity is the listed witness at ratio near 1. What the theory cannot bound, said as such:
outside the domain (overflow, NaN) the kernel refuses; an unknown L (a host routine with no theorem)
composes to nothing and permits no substitution (L6.8); a branch whose test a ball straddles has no
bound (IEEE 1788's decoration; 11.S10's comparison answering with a probability); a chaotic
iteration has a bound, L^k, that is honest and useless past k ≈ log(1/u)/log L, about 27 steps of the
logistic map at r = 3.9: the bound tells how far the simulation can be trusted, which is the itch
his words name. And there is no exact run of such an iteration: ℚ is exact for a dozen steps, beyond
that the reference is the same program at a smaller u (200 digits), a specimen of the same theory.

The same shape elsewhere (mine, answering his second point). A discretization (Euler for an ODE) is a
specimen with η = Chᵖ (h the step, p the order) and L = e^{Λt} (Grönwall, Λ the field's Lipschitz
constant); a Monte Carlo estimate has η = cσ/√n at risk δ, the pair composing in the evidence base of
report-B2; a surrogate has η the error on D and nothing outside D. The theory of D-2026-10-25-a covers
them with two changes: the defect takes a budget (h, n, bits of precision) as a parameter, which is
L9.17 (the law of an algorithm states how its budget scales with the bound) with the floats as its
cleanest instance, bits = log₂(1/ε); and the bound may carry a risk, a second coordinate composed by
the capped sum. Proposed as a clause L13.6.

The flagship (mine). A chapter `docs/guide/floating-point.md` a scientist reads in an hour, with its
programs in `examples/floats/`: the sum (three specimens, accumulation, a demand choosing), the dot
product (stability, sensitivity, the exact reference), one Newton step for √a (composition and the
pull-back of a demand), and a small simulation, Euler on the harmonic oscillator for the
discretization's defect and the logistic map for the explosion, each run plainly and over balls, with
the static bound beside the radius; a section on what Luthier could not bound. concepts.md 9 stays
the concept; spec 11 is corrected where it says rational.lut exists.

## What only you can answer

**1. The exact reference in the kernel.** Give `Rational` its arithmetic in the kernel (`Fraction`
constants, the four operations and comparisons, `toQ`, `nearest`, `ratio`) and a `WithinExact` form,
so the textbook bounds are tested exactly? Implies: a kernel change with its edge (D-2026-10-27-a,
the kernel in the cone by content hash); the correct-rounding law as a Boolean law bit for bit; the
flagship's bounds without the factor 3. Costs: one Opus bite in the kernel, one in laws.lth and
tester.py; exact lines limited to 10⁵ terms. Recommendation: yes; it is the only place where the
relation between ℝ and F can be stated with no measurement error at all.

**2. Decorated floats now.** Build `Ball` (midpoint, radius) as a model of a generic number theory
(11.S3's `NumberModel`, not written), with +, −, ×, /, `sqrt`, no comparison, so that a program
generic in its numbers runs over balls unchanged (L5.4, a decoration of the output is another model
of the theory the code was written over)? Implies: O5 (the decorated output) opens before the cost
types; the soundness law tested against ℚ; `RadiusWithinTransformer` as the law joining the two
compositions. Costs: two Opus bites and the generic form of the examples' code. It does not touch
D-2026-10-14-c (first everything Boolean): balls are values, their laws are Boolean. Recommendation:
yes, limited to those operations; the simulation example needs it.

**3. The backward error as a third form.** Adopt LAPACK's triple for linear algebra, a backward law
of the specimen (residual-based), a sensitivity law of the ideal with κ, the forward bound by
composition only where κu < 1, and so retire the pseudo-inverse's `tol` laws? Implies: a form beside
stability and sensitivity; the perturbation theory cited (Higham ch. 7, Wedin for the pseudo-inverse).
Costs: one Opus bite in arrays.lth and its re-certification. Recommendation: yes; D-2026-10-18-j
already names the radius, and it is the honest form for the fit of sonolocalización.

**4. The chapter and its examples.** A new `docs/guide/floating-point.md` with the four examples above
and the failures as its last section, written for a scientist who has never seen Luthier? Implies: a
document of its own beside concepts.md; the failures shown by name, as his words ask. Costs: one
Fable bite for the text after the examples run, one Sonnet bite for spec 11 and concepts 9.
Recommendation: yes, with the simulation as the closing example; if one example must go, the Newton
step.

**5. The clause for the other approximate models.** State L13.6 now (a specimen within a bound of an
ideal on a domain; the defect takes the budget as a parameter and may carry a risk), with Euler on the
oscillator as its first case in the chapter, or wait for a second case outside floating point? P8 (no
more bureaucracy than it pays for) against P13 (a principle is worth the decisions it guides): the
clause guides the shape of `Ball`'s laws and of the transformer's defect in the simulation bite.
Recommendation: propose it now; the Euler example is the case.
