# Floating point as the flagship case: execution

2026-10-27, Claude Fable 5.1, on `prompt-design.md` beside this file (9d53f79). The decisions are in
`decisions.md` (questions 1 to 5, and his addition on the format as the parameter). Each bite names
its source (record, literature or "mine"), what to build, what it depends on, when it is accepted,
and the model fit: Sonnet for reading and mechanical code, Opus for code with judgment, Fable for
theory and text with bounded reading. Every bite: commit before the change, small commits staged by
path, never `git stash`; the stores it moves re-certified twice (second pass 0 lines ran); the suite
file by file under `timeout 1800`; `python scripts/check_spec.py` with its one known finding;
`scripts/core_metrics.py` with no count up that a theory's own names do not explain; a report
`report-<bite>.md` in this folder ending with the decisions taken on its own and at most one
question. No law carries a constant (P11); every bound is a function of the arguments and of the
format; every numerical law states its range as a premise (D-2026-10-18-j).

Status, 2026-10-27: designed; nothing started. F1 and F0 can start now in two worktrees (they touch
different files); the rest waits for the questions each names.

## Notation used in the bites

p the precision in bits, u = 2⁻ᵖ the unit roundoff, (emin, emax) the exponent range, Ω the largest
finite float, fl the rounding to nearest (ties to even), ι the inclusion of the floats in ℚ (`toQ`),
γₙ = nu/(1 − nu) (Higham 2002, Lemma 3.1), the transformer (L, η, D, r) of D-2026-10-25-a (L the
sensitivity, η the defect at exact inputs, D the domain, r the radius of the input error).

## Wave F. The theory, exact

### F1. `Rational` computes (Opus; kernel.py, term.lth, host.py, core.lut, a new lib/rational.lut) [question 1]

Source: record 11.S4 (`Rational` is a primitive represented by the host's fractions), 11.S12, 11.S13
(the laws named `Rounds`, `RootRounds`, `offByThree`, `NormalDouble`; stated for a rational.lut that
does not exist), 11.S19 (says it exists: wrong, to be corrected in F10); rational.py (`ratio`,
`nearest`, `gen_normal_double`, unused); kernel.py `_primitive` (no `RationalConst`);
D-2026-10-27-a (a kernel change is an edge by content hash).
Build: a `RationalConst` in term.lth and kernel.py with `+ − × /` and the comparisons exact (Python's
`Fraction`; a zero divisor no step); the primitives `toQ : Float64 -> Rational` (exact), `nearest :
Rational -> Float64` (round to nearest, ties to even, no value past Ω: 11.S7), `ratio : Int -> Int ->
Rational`, `fromInt : Int -> Rational`; the bridge crosses a `Fraction` as a `Rational` and refuses a
float there. `lib/rational.lut`: the laws `Rounds` (for each of the four operations, `nearest (toQ x
op toQ y) == x op y`, a Boolean law bit for bit, over the format's normal range drawn uniform in the
exponent: rational.py's generator, lifted to a `Gen` of generators.lth), `RoundsRelative`
(|toQ (nearest q) − q| ≤ u |q| for a rational q in the normal range), `RootRounds` (the square root
correctly rounded, IEEE 754 §5.4.1), and the control `offByThree` (an addition three units off in
the last place, refuted wherever the result is not zero). The kernel edge of D-2026-10-27-a recorded
(the comparison of the test programs under the old and the new kernel).
Depends: question 1. Nothing in numbers.lth.
Accepted when: the four `Rounds` and `RootRounds` certified sampled at 10⁵ cases over the whole
exponent range, every control refuted; `luthier eval` reduces `ratio 1 3 + ratio 1 6 == ratio 1 2`
to `true`; the kernel edge stored with 0 cones differing; the suite.

### F0. The format as the parameter (Opus; numbers.lth, numbers_model.lut, every importer of `Doubles`, tape.lth, arrays.lth's `fp`) [his addition, no question]

Source: his words of 2026-10-27 ("Float N debería ser, con Float64 y Float32 como aliases"), read as
the format (p, emin, emax) in decisions.md; IEEE 754-2008 §3.3; Muller et al. 2018 ch. 2; record
11.S4, D-2026-10-17-f, numbers.lth §1 and §2.
Build: `Format : U := { p emin emax : Int | 2 <= p and emin < 0 and 0 < emax }` in numbers.lth;
`unitRoundoff`, `epsilonOf`, `largest` (Ω), `smallestNormal`, `absoluteFloor` (2^(emin − p)) as
functions of a `Format`; `Floats (fmt : Format) (F : U)` in place of `Doubles (F : U)`, the record
with `format : Format` in place of `epsilon`; `Moderate fmt`, `Tame fmt`, `NonZero fmt` and the
rest as functions of the format (the bounds today's 1e±150 and 1e±100 become the format's: a
product or quotient of two moderate values normal, of three tame values normal); every within-bound
law written once over `fmt` with its bound from `unitRoundoff fmt`; the aliases `Binary64 : Format`,
`Binary32`, `Binary16`, `BFloat16`, `E4M3`, `E5M2` as values, and `Doubles` kept as the name of
`Floats Binary64 Float64` so the examples' cones move once. numbers_model.lut's `doubles` gains
`format := Binary64`. `elementaryRoom` and the `Elementary` identities over `fmt` too.
Depends: nothing; it moves every cone that reads `Doubles` (arrays, tape, probability, optimization,
the sonolocalización programs), so it lands in one worktree and one re-certification wave.
Accepted when: `luthier check` clean on every importer; numbers_laws and numbers_controls certified
at `Binary64` with the same worst ratios as before (report-bite-8's table, within 5 %); a control
with a wrong format (`Binary64` with p = 54, the bound too small, refuted at report-bite-8's
witnesses; a format with a smaller p gives a larger bound and refutes nothing, so it is no control); one wave re-certifies every moved cone, second pass 0 lines
ran; the suite.

### F2. `WithinExact` and the textbook bounds (Opus; laws.lth §5, laws_model.lut, tester.py, certify.py, numbers.lth, arrays.lth) [question 1, after F1 and F0]

Source: record laws.lth §5 (`Within`, `Measured`, `Measuring`), report-C1 (the ratio), report-bite-8
(why 3γ₂: the error measured in floating point); literature Higham 2002 Lemma 3.1, eq. (3.5) (dot
product, γₙ Σ|xᵢyᵢ|), eq. (4.4) (recursive summation, γₙ₋₁ Σ|xᵢ|), §4.2 for pairwise summation (γ_⌈log₂ n⌉); the agent
cites each equation number from the book, not from memory.
Build: `WithinExact : (A : U) -> (A -> A -> Rational) -> Rational -> A -> A -> Law`, evidence
`MeasuredExact dist bound` in ℚ, the ratio recorded as the `Float64` nearest to the exact quotient
(a record, the verdict the exact comparison); tester.py runs it as it runs `Within`; certify.py's
`entry_bound` reads it. The exact laws, beside today's (which stay): in numbers.lth,
`PlusAssociativeExact` (each association within γ₂ Σ|·| of the exact sum, two laws), `SumStable`
over a `Vec` of the format (γₙ₋₁ Σ|xᵢ|, recursive order, n ≤ 10⁵ as the premise), `TimesExact`,
`DistributiveExact`; in arrays.lth, `DotExact` (γₙ Σ|xᵢyᵢ|) beside `DotStable`. The witness
(1, 2⁻ᵖ, 2⁻ᵖ) and the edges of the range as listed cases. Controls: the 26-bit rounding of
report-bite-8 (`coarse`), and the bound halved on the real floats, refuted at the witness.
Depends: F1, F0, question 1.
Accepted when: every exact law certified at ratio ≤ 1 on sampled and listed lines; the witness at a
ratio ≥ 0.9 against γ₂; `DotExact`'s worst ratio reported beside `DotStable`'s 0.116 (report-C1);
controls refuted; exact lines at 10⁵ terms under 60 s each; the suite.

### F3. Three sums of one theory (Opus; a new lib/summation.lth and summation_model.lut, examples/floats/sum.lut) [question 1, after F2]

Source: literature Higham 2002 §4.2 (recursive and pairwise), §4.3 (Kahan 1965's compensated
summation, |ŝ − s| ≤ (2u + O(nu²)) Σ|xᵢ|: the second-order constant written in the file from the
derivation, as `elementaryRoom` does, and marked mine); record L9.17 (the law of an algorithm states
how its budget scales with the bound), D-2026-10-18-j, concepts 13 (specimens and the planner).
Build: the theory `Summation (fmt) : { sum : Vec F -> F }` with the law `SumStable` taking the
specimen's own bound as a function of (n, u) from a field `defect : Int -> Format -> Rational`; the
specimens `recursive` (in Luthier), `pairwise` (in Luthier), `kahan` (in Luthier), `hostFsum`
(numpy's or Python's `math.fsum`, correctly rounded: Shewchuk 1997, defect u Σ|xᵢ|... the agent states
the bound fsum guarantees, u|s| with the exact sum s, and tests it exactly); the transformer of each
as a value of `Affine` (L = 1 on the sum of the inputs' errors, η the defect); `examples/floats/
sum.lut` runs the four on one vector with a `--bound` demand that `recursive` fails and `kahan` meets.
Controls: `recursive` claimed with `kahan`'s bound, refuted; `kahan` with its compensation dropped.
Depends: F2.
Accepted when: four specimens certified exactly with their own bounds; the demand's run refused for
`recursive` and served by `kahan` and `hostFsum` with the certificate named in the run record; the
ratio of each specimen against its bound in the report; the suite.

### F4. The backward error as a third form (Opus; laws.lth §5 or numbers.lth, arrays.lth, the pseudo-inverse's laws) [question 3, after F2]

Source: literature Higham 2002 §1.5 and §1.6 (forward, backward, condition), ch. 7 (perturbation
theory for linear systems), Rigal and Gaches 1967 (the residual backward error), Wedin 1973 (the
perturbation of the pseudo-inverse; Stewart and Sun 1990 ch. 3 for the statement); record
D-2026-10-18-j (the radius below the smallest retained singular value), report-C1 (pinv keeps `tol`),
functions.lth `ComposeSound`.
Build: a backward law is a `WithinExact` (or `Within`) on the input space with a constructed witness:
for a sum, `SumBackward`, the perturbed inputs xᵢ(1 + θᵢ) with θᵢ read from the actual partial sums
in ℚ, within γₙ₋₁ of the inputs entrywise, and `fl(Σxᵢ) == Σ xᵢ(1 + θᵢ)` exactly (Higham eq. 4.3);
for `pinvSym` and `solve`, the residual form ‖Aŷ − b‖/(‖A‖‖ŷ‖ + ‖b‖) ≤ c(n)γ with the constant from
Higham's theorem for the factorization numpy uses (the agent reads LAPACK's documentation of the
routine and cites it); the sensitivity law with κ = ‖A‖‖A⁺‖ and the radius ‖ΔA‖ < σ_min retained; the
forward claim derived by `ComposeSound`, stated as a law with the premise κu < 1 and nothing outside
it, the region sampled on both sides (D-2026-10-16-j). The seven pseudo-inverse laws of report-C1
lose their `tol`.
Depends: F2, question 3.
Accepted when: `SumBackward` certified exactly; the residual law of `pinvSym` certified with a worst
ratio reported; the forward law's region shows the boundary (cases inside pass, cases past κu = 1 are
outside the premise and counted as such); every `tol` gone from arrays.lth except `Orthogonal`'s if
its bound is not written (said in the report); controls: a solver that returns b (refuted at the
residual), κ claimed as 1 (refuted at the sensitivity); the suite.

## Wave G. The dynamic side

### G1. Balls as a number model (Opus; a new lib/ball.lth and ball_model.lut; lib/number_model.lut for 11.S3) [question 2, after F1 and F0]

Source: literature Johansson 2017 ("Arb: efficient arbitrary-precision midpoint-radius interval
arithmetic", IEEE Trans. Computers 66(8)), van der Hoeven 2009 (ball arithmetic), Moore 1966,
IEEE 1788-2015 (decorations); record 11.S3 (`NumberModel`, not written), 11.S10, L5.4 (a decoration
of the output is another model), O5, D-2026-10-14-c (laws Boolean; balls are values).
Build: `NumberModel (F : U) : { plus minus times divide : F -> F -> F, sqrt : F -> F, fromInt : Int ->
F, zero one : F }` in number_model.lut, with `floats : NumberModel Float64` and `rationals :
NumberModel Rational` (no `sqrt`: a `Maybe`, or the model partial, the agent says which); `Ball fmt =
{ mid : F, rad : F | 0 <= rad }` and `balls : NumberModel (Ball fmt)`, the radius after each operation
the literature's formula widened for round-to-nearest (the kernel has no directed rounding: the
radius times (1 + k u) with k from the number of roundings, derived in the file), `sqrt` by the mean
value bound; no comparison on balls (11.S10's probability waits). The theory `Enclosure`: `Sound`
(the exact result of the operation on the midpoints, in ℚ, lies within the new radius of the new
midpoint: a `WithinExact`), `MidpointIsTheFloat` (the midpoint is the plain float operation, bit for
bit), and `RadiusWithinTransformer` (the radius after an operation at most the operation's transformer
at the midpoint applied to the inputs' radii: decisions.md's meeting of the two compositions).
Controls: a radius that forgets the midpoint's rounding (refuted by `Sound` at a case where the
rounding is the whole error); a product radius without the cross term.
Depends: F1, F0, question 2.
Accepted when: the three laws certified exactly over `Moderate` balls; `recursive` of F3 run over
`balls` by substituting the model and nothing else (the generic form, 11.S3), its final radius at
most `SumStable`'s bound at the result; controls refuted; the suite.

### G2. Formats as specimens, and mixed precision (Opus; numbers_model.lut or a new lib/formats_model.lut, host externs, examples/floats/mixed.lut) [his addition, after F0, F1, F2]

Source: his addition of 2026-10-27; record 11.S2 (a leaf declared over what it receives), 11.S6 (the
bridge checks the dtype), D-2026-10-25-a's composition formula; literature IEEE 754-2008 §3.3, §5.4.1
(correct rounding), Muller et al. 2018 ch. 2 and ch. 3; the bfloat16 and fp8 formats as PyTorch and
JAX document them (the agent cites the page it read).
Build: leaves for numpy's float32 and float16 (`extern "python:..."` over arrays of that dtype, the
bridge extended to those dtypes with the same checks as 11.S6) and, where the host has them, torch's
bfloat16 and fp8 (declared, run only on a host that has torch; the certificate records the host, L5.6);
each claimed as a model of `Floats fmt` at its format with the laws of F0 and the `Rounds` of F1 run
exactly in ℚ (`toQ` extended to every format: a float of any binary format is a dyadic rational, the
conversion in the host); a conversion `convert : (a b : Format) -> F_a -> F_b` with the law
`ConvertRounds` (correctly rounded, exact when b is wider) and its transformer (1, u_b |x|) on b's
range; `examples/floats/mixed.lut`: a dot product accumulated in Float32 and stored in BFloat16, its
transformer the composition (F3's accumulation then the conversion), certified exactly against ℚ, and
the same over balls (G1) with the radius converted.
Depends: F0, F1, F2; G1 for the balls' half.
Accepted when: float32's four `Rounds` certified bit for bit on numpy (and the result of the same lines
on the GPU formats recorded, pass or refuted, as the report's finding: a format that does not round to
nearest fails `Rounds` and is claimed with a widened bound instead); `mixed.lut`'s composed bound
certified at ratio ≤ 1 with the overflow of the store as the domain's boundary sampled on both sides;
the suite.

### G3. The simulation (Opus; examples/floats/newton.lut, oscillator.lut, logistic.lut; lib/iteration.lth for the k-fold transformer) [questions 2 and 5, after G1]

Source: literature Higham 2002 ch. 1 (Newton, the examples of instability), Hairer, Nørsett and Wanner
1993 ch. II (Euler's global error Chᵖ e^{Λt}), the Grönwall bound; record functions.lth
(`composeAffine`), L9.17, L13.5 (a cutoff read against the defect), D-2026-10-16-m (an iteration
converges within a bound derived from its theory).
Build: `iterate : Nat -> Affine A -> Affine A` (the k-fold composition, closed form (Lᵏ, η(Lᵏ − 1)/
(L − 1)) when L ≠ 1, kη when L = 1) with the law that it equals `composeAffine` folded k times;
`newton.lut`: one step x ↦ (x + a/x)/2 for √a, its transformer (L = 1/2 near the root, η from the
three roundings), composed over k steps, and the pull-back of a demand's ε to the starting error;
`oscillator.lut`: explicit Euler on x″ = −x with step h over n steps; the agent derives the
discretization's defect (first order in h) and the amplification (1 + h²)^(n/2) and the rounding's
accumulation, states them as the transformer's η and L in terms of (h, n, u), and certifies the error
against the exact solution (cos, sin at machine precision, the reference's own error in the bound);
`logistic.lut`: xₖ₊₁ = r xₖ(1 − xₖ) at r = 3.9, the transformer (3.9ᵏ, ...) and the step k past which
the bound exceeds 1, the honest failure; the reference in ℚ for k ≤ 12 and a 200-digit specimen
(Python's `decimal`, its own u stated) beyond; each example run over balls (G1), the radius plotted
against the static bound per step (plot.lth).
Depends: G1; question 5 for the clause the oscillator illustrates.
Accepted when: `iterate`'s law certified on listed transformers; the Newton pull-back's law certified
(a demand's ε at k steps met from the pulled-back starting error, refuted at one step fewer); the
oscillator's bound certified at ratio ≤ 1 against the exact solution for h in a listed range; the
logistic map's certificate shows the region boundary at the step where the bound passes 1, the
ball's radius within the static bound at every step; the suite.

## Wave H. The flagship text

### H1. The chapter (Fable; docs/guide/floating-point.md; bounded reading: decisions.md, the reports of F and G, Higham ch. 1 to 4) [question 4, after G3]

Source: decisions.md (the design in plain words); the reports of F1 to G3; Goldberg 1991 ("What every
computer scientist should know about floating-point arithmetic") for the pitch to a scientist.
Build: the chapter in the order of decisions.md: three objects; the format and the two maps and the
one law; the exact reference and what it buys; the sum (four specimens, the demand that chooses); the
dot product (stability, sensitivity, backward); the Newton step (composition, pull-back); the
simulation (static bound and ball, the step where trust ends); the failures by name (cancellation,
ill-conditioning, accumulation, non-associativity, the unbounded cases); mixed precision; the same
shape elsewhere (Euler as the case, Monte Carlo and surrogates named). Every number in it from a
certificate named by hash; every bound with its citation; symbols defined at first use; no
em-dashes, no "not X but Y".
Accepted when: a reader with Higham but no Luthier can run each example from the chapter's text alone;
every claim traces to a certificate or a citation; `check_spec.py` unaffected; Luciano's read.

### H2. Spec, concepts and principles (Sonnet; docs/spec/11-numbers.md, docs/concepts.md 9, record/principles-language.md, scripts/project_principles.py --write) [questions 1 to 5, after H1]

Source: the record's three principles documents (D-2026-10-12-d); spec 11.S10, 11.S13, 11.S16,
11.S19 (says rational.lut exists); concepts 9.
Build: 11.S19 corrected (rational.lut written in F1, its laws named); 11.S13's range moved to the
format's parameters; a clause for the format as the parameter of the floats' theory; 11.S10 updated
by G1 (balls exist, the comparison still waits); 11.S16 and 11.S17 updated by F2 and the transformer;
a 11.S20 for the backward form if question 3 is yes; concepts 9 gains the exact reference, the
format, the backward form and the balls with their hashes; the principles: L13.6 proposed (question
5), the backward form under L13.3, the format under L13.1, projected with `--write` and linted with
`--check`.
Accepted when: `check_spec.py` with its one known finding; `project_principles.py --check` clean;
every new clause marked proposed with its source; Luciano's mark.

## Order and parallelism

F1 and F0 first, in two worktrees (kernel and laws against numbers.lth and its importers), each with
its re-certification wave; F2 after both; F3 and F4 after F2, in parallel; G1 after F1 and F0, in
parallel with F3 and F4; G2 after F2 and G1; G3 after G1; H1 after G3; H2 last. At most three agents at
a time (the pace rule of 2026-10-14). Questions 1 and 2 gate wave F past F0 and wave G; question 3
gates F4; question 4 gates H1; question 5 gates the clause in H2 and the oscillator's framing in G3
(the example is built either way).

## What is mine in this plan, beyond the decisions' questions

The names (`Format`, `Floats`, `WithinExact`, `Enclosure`, `RadiusWithinTransformer`, `iterate`,
`Summation`); `Doubles` kept as an alias so the cones move once; the exact lines capped at 10⁵
terms; the balls' radius widened for round-to-nearest, with no directed rounding added to the kernel; the 200-digit specimen as the reference past twelve steps; the oscillator and the logistic
map as the two simulations; the order above.
