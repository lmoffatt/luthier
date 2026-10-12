# Laws valued in cost

Draft 0, 2026-10-11, unapproved; citations moved to draft 11 of `docs/principles.md` on 2026-10-12,
the text otherwise as written. Status 2026-10-12: this is the working note of O1 (the algebra of
costs); since it was written Luciano decided that the algebra has two candidate models, min and max
or 1/n log-sum-exp and 1/n sum (D-2026-10-12-p), that composition along a path is the sum
(D-2026-10-12-q), that a sample's statistics convert to an evidence cost by a function declared per
theory, −log(1 − ε̂(n, δ)) in nats first (D-2026-10-12-r), that the cutoff is the demand's
(D-2026-10-12-h), and that an `assumed` certificate may carry a cost formula such as p(n)·ε·κ(A)
(D-2026-10-12-t); §4 to §6 below predate those and are superseded where they differ. The
articulation of the organizer G2 of `docs/principles.md`
(laws are valued in cost), asked for by D6 of
`record/plan-principles-generative-2026-10-11-decisions.md`. Sources: Luciano's notes
`record/Lucianos ideas/principios organizadores.txt` (fa3f972) and `el problema de los floating
point.txt` (5cc41fa); his voice note of 2026-05-29 (`note:2026-05-29T14.14.08:matrimonio-hott-bayes`)
and Deepseek's critique of the same day (`dialogue:c886516d:critica-hott-bayes-sin-articular`);
the prior art of cluster G (`record/prior-art-2026-10-09/reports/G-cost-valued-laws.md`); the
analysis `record/organizing-principles-2026-10-11.md` (§4, addenda 2 and 7) and the second round of
answers (`record/answers-annotations-principles-2026-10-11-b.md`, §16). What cites a source is
marked; the rest is proposed by the model. Symbols: ε is the unit roundoff of the doubles
(2⁻⁵³); κ(A) the condition number of a matrix; d a distance; L a Lipschitz constant; p a
probability; n a number of terms or of samples.

## 1. The problem

Luthier writes code over ideal objects and runs it on concrete ones (L13): `Real` and `Float64`,
a probability and a sample of it, a linear map and a matrix of doubles. The laws of the ideal
(associativity, A·A⁻¹ = I, a probability integrates to one) are false of the concrete realization,
so a type theory that asserts them of `Float64` lies, and one that refuses them says nothing.

The Boolean way out exists and is honest: the law becomes a bound, |fl(a + b) − (a + b)| ≤ ε|a + b|,
a predicate with ε as a parameter (P11). Flocq proves such theorems in Coq, and Luthier's
`rational.lut` certifies `sumTo` within γ_n of the exact sum this way. Its three costs are what
force G2 (Luciano: "si queres ser estricto o expresivo, necesitas otra cosa. De ahi el [0, +inf)"):
the tolerance is fixed in each law, so there is one law per tolerance and per representation;
worst-case bounds compose into condition numbers and say nothing after a few steps; and about
data, where the property itself is a likelihood, nothing can be said at all.

## 2. Truth values in [0,∞)

A law returns a cost in [0,∞), 0 for true and ∞ for false, the orientation of Lawvere's
generalized logic (Bacci, Mardare, Panangaden, Plotkin; G §2 notes that Caesar uses the dual, and
that Luthier must fix one: fixed here, 0 = true). A Boolean law is the case with two values. Two
conjunctions exist and both are needed: the maximum, "both hold up to ε", for laws that must hold
together on one value; and the sum, for a chain, since the distance across a chain is at most the
sum of the distances of its links. The type is `Cost`, proposed as the non-negative doubles with
infinity (`core.lut` already has `ExtendedReal` with `posInf`); a law into `Bool` and a law into
`Cost` are both laws, and the type of the result says which (second round §11).

## 3. Equality as distance

Propositional equality becomes a quantitative equation, s =_ε t (quantitative equational logic,
Mardare, Panangaden, Plotkin; G table): the quotient of G0 becomes a pseudometric space, the class
of L6 is the ball of radius the demanded tolerance, and identity at distance 0 is the exact case.
This answers Deepseek's first question: paths do not become distributions, they acquire a length.
A function pulls the distance of its codomain back to its domain, d_f(a, b) = d(f a, f b), so the
kernel reading of the former L12 (computing is classifying, kept in the record of L4) survives: the classes become "indistinguishable
by f up to ε" (addendum 8).

## 4. Judgments

a : A stays a judgment, which answers Deepseek's second question: typing does not relax into a
probability. What changes is its evidence: the certificate carries the grade (spec 6), and for a
law into `Cost` the worst cost seen with the input that reached it, as Hypothesis prints and
discards (G §2). The demand supplies the tolerance, so one certificate serves every demand whose
tolerance is above the worst cost recorded, and a stricter demand asks for more cases or a better
implementation (L6). What cannot be decided stays a hole (L2).

## 5. How cost moves through application

This is what decides whether G2 is practicable (Luciano, annotation on draft 2: "la composicion de
judgments, como se transfiere la quantitative equality a traves de la aplicacion de funciones, cual
es el algebra"). Two known forms.

As distance. If f expands distances by at most L, d(f a, f b) ≤ L·d(a, b); composition
multiplies the constants, and L is the condition number in numerical analysis (backward error
analysis, Higham). There is a type system that carries it: sensitivity types, where a function type
records its constant, `f : A ⊸_L B`, and application multiplies (Reed and Pierce, "Distance makes
the types grow stronger", 2010). Quantitative equational logic has the same as an axiom: operations
are nonexpansive, so s =_ε t gives f s =_ε f t. In Luthier the constant is a law of the function,
`Lipschitz L f`, Boolean with L as a parameter in version 0, and the certificate of a chain
multiplies the constants it finds, as it takes the weakest grade today (spec 6).

As likelihood. With cost = −log p, costs add under independence: a chain of judgments costs the
sum, which is the Bayesian composition Luciano named ("usar estadistica bayesiana para
componerlo"). A bound ‖r‖ ≤ ε is a uniform likelihood on the ball, cost 0 inside and ∞ outside,
the Boolean limit; a Gaussian error of width σ is the quadratic cost d²/2σ², monotone in d, so a
distance reading is a likelihood reading under a noise model whose width is the demanded
tolerance. The choice among implementations (L6) is then decision theory, expected loss against
cost of computing; the progressive validation of G1 is the posterior over "the law holds" updated
case by case, the reading `00` (*What is known*) already proposes and D-2026-10-08-a left open.

The practicable version is both: a constant per function type where it is known, which it is for
IEEE arithmetic and for linear algebra by condition numbers, and a sampled cost where it is not.

## 6. The cost itself is uncertain

Over integers a law's value is computed exactly. Over floats it is not available: the ideal value
(the real sum) is not in hand, so the residual is estimated by a bound, an interval, or a reference
at higher precision on sampled inputs; Luthier's reference is `Rational` ("what the doubles are
compared against", spec 11, `rational.lut`). The value of the law is then a random variable, not a
number, and that, not a preference, is why Bayes is needed: G2 is cost-valued laws whose costs are
themselves uncertain (addendum 2). The certificate records the summary of what was seen (worst,
mean, the number of cases, the generators, the seed), and composition of uncertain costs is the
composition of §5 under the likelihood reading.

## 7. Three worked examples

**The sum of n doubles.** The worst case is γ_n ≈ nε relative error (Higham), which `rational.lut`
certifies as a Boolean law with γ_n as its parameter; the typical error is about √n·ε. As a cost
law, `sumTo` returns the measured |fl(Σ) − Σ| / |Σ| against the rational sum, the certificate keeps
the worst seen, and a demand for 1e-9 on n = 10⁶ terms is served by the same certificate that a
demand for 1e-6 is, or refused by it. The difference between the two readings of §5 is this
example in one line: the worst case adds the n roundoffs, the expectation adds their variances.

**A matrix inverse.** ‖A·A⁻¹ − I‖ is bounded by a constant times n·κ(A)·ε; the Lipschitz constant
of the inverse is κ(A), which is a property of the input, not of the implementation. As a cost law
the residual is returned, and the demand with its tolerance decides, through L6, whether float32,
float64 or one step of iterative refinement is the representative: the class is fixed by the law,
the representative by the cost at this κ(A). Linear algebra libraries publish bounds rather than
booleans (Luciano's note), and this is where they enter.

**A probability that integrates to one.** A sampled density gives an estimate of ∫p with error
about 1/√n; the Boolean version is the statistical test at a declared level and power (spec 7, a
statistical law declares its level and its power); the cost version is the −log-likelihood of the
estimate under the sampling distribution, with n from the demand (P11). Two estimators of the same
density are equivalent up to the tolerance the demand sets, which is L6 again, for data.

## 8. Open

- The type `Cost` and the two conjunctions in the kernel, or in a library over `ExtendedReal`.
- How a certificate stores the distribution of a cost beyond the worst seen.
- Whether function types carry their constant (sensitivity types) or the constant stays a law.
- The prior on "the law holds" as a parameter (D-2026-10-08-a) and its update by cases.
- An implementation of Lawvere logic exists nowhere (G §2); the decision procedure for the affine
  fragment would give a `proved` grade to laws whose cost is linear in other costs.
