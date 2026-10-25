# Bite B2: the evidence and error bases in the core

Claude Fable 5.1, 2026-10-25, on `prompt-wave-bc.md` beside this file (77f56b9) and `execution.md` (B2), after D-2026-10-25-a. Base commit 77f56b9, with Agent C1 working in the same tree. Commits a9f8f8a, 6ff2051. Committed by the coordinator from the agent's hand-back (its Write of the report was refused). Files: `src/luthier/lib/core/structures/algebraic.lth`, `src/luthier/lib/core/core.lut`, its store `core/core.cert.json`, two new test programs `tests/tester/bases_laws.test.lut` and `tests/tester/bases_controls.test.lut`, and `tests/test_core_structures.py`. Scratch and logs under `~/.cache/luthier-wave-bc/B2/`.

Sources: audit 4.1 and 4.2 (`report.md`, 5b1a05e); D-2026-10-18-i with its two corrections; D-2026-10-25-a (question 1, with Luciano's addition: any reasonable choice of composition, none that can loop); D-2026-10-13-m; D-2026-10-12-q; L10.3, L10.8, L6.15; spec 6.S4, 6.S15; certification.lth §3 `serves`.

## What was built (a9f8f8a)

algebraic.lth, the theories:
- At `Quantale`, the comment on the two orders that meet at a base and share no `leq` (audit 4.1). The categorical order is Lawvere's (y above x when it knows at least as much: a smaller error, a smaller failure bound; the unit on top, the empty join at the bottom, the tensor preserving it). The numerical order is admission's: the demand's cutoff is met when the entry's value is at most it (certification.lth §3 `serves`, 6.S15's cutoff in 6.S4's `C`), which reads the categorical order backwards. Refinement of a certificate and strengthening of a demand both go up the categorical order.
- `Dioid`: an idempotent semiring (Gondran and Minoux 2008), over `Semiring` with the join as `plus` and the tensor as `times`, so the laws are operations.lth's and the order is the join's. `Integral`: the unit is the top (composing never knows more than either part), the property both of Lawvere's bases have.
- The evidence base: `EvidenceBound = { failure, risk }`, the pair (ε̂, δ), its names kept apart from sequential testing's `delta` (audit 4.2). `EvidenceComposition` is a record with one field, the tensor: the composition is the parameter (P11, D-2026-10-25-a); any `EvidenceComposition` is a dioid with the join "the stronger of two" (componentwise min), the bottom (1, 1), the unit (0, 0), and `Integral`, since the union of two failure events is at least as likely as either. That is what "reasonable" means here; totality is the language's. `AtLeastTheUnionBound` (Boole's inequality: a composition that assumes nothing is at least min(1, a + b) in each part) and `AssumptionFreeComposition`, the structure of the default. `FailuresIndependent`, an axiom (11.R3) about the links a composition combines, and `IndependentComposition`, the structure of the product a + b − ab (the sum in nats pulled back to [0, 1]) under that hypothesis, which a demand accepts by name as it accepts `ObserverIsFaithful` (run.py's `axioms`, L5.18).
- `ErrorBase`: ([0, ∞], +, ≥) over equality.lth's `Extended`, whose laws say its dioid is a dioid, integral, and that its tensor and join are the extended sum and the smaller distance.
- `NatsConversion`: L10.3's conversion to nats is claimed as a map of the orders (`Monotone` into `extendedLeq`) carrying certainty to 0 and no evidence to ∞; the comment says it is a map of dioids for the product tensor only, not for the capped sum (audit 4.2).

core.lut, models and claims (plane 3, gathered in `CoreBases`, a conjunction no run roots): `extendedObject` (the equality of `Extended` by cases: the kernel's `==` does not reduce on injections, a finding below), `extendedLeq`, `extendedPlus`, `extendedSmaller`, `errorDioid`, `errorBase`, `cappedSumComposition` (the default), `productComposition`; the claims `ExtendedIsAnObject`, `ErrorIsABase`, `CappedSumIsAssumptionFree`, `ProductIsAComposition`, `NatsIsAConversion` (its `log` a parameter the test binds to numbers_model.lut's `elementary.log`, since the core has no elementary functions).

The test programs: the laws on listed cases, `ExhaustiveMode` over the lists. The evidence cases are dyadic (multiples of 1/8) so every sum and product is exact in Float64 and the laws hold on the nose; at arbitrary doubles the capped sum is associative to an ulp only, a `...Within` law not claimed here (the program's header says so). The error cases include ∞. The controls: an equality relating nothing; the product dioid on [0, ∞] (min, ∞, ×, 1), a dioid whose unit is not the top, refuted at `Integral` alone; the join the wrong way round (max with bottom ∞), refuted at the join's neutral law; the product composition as a model of `CappedSumIsAssumptionFree`, refuted at `AtLeastTheUnionBound` with x = y = (0.1, 0.1), the audit's 0.19 against 0.2; a projection as a composition, refuted at the unit; a falling log, refuted at `Monotone`.

## Checks

- `luthier check` clean on the four files.
- `luthier test`: the five claims graded `cases` (ExtendedIsAnObject 3 conjuncts, 10 cases; ErrorIsABase 13 conjuncts, 521 cases; CappedSumIsAssumptionFree 12 conjuncts, 817 cases; ProductIsAComposition 11 conjuncts, 781 cases; NatsIsAConversion 3 conjuncts, 8 cases); the six controls refuted where the header says. `luthier certify --jobs 1`, each program with its own log under `~/.cache/luthier-wave-bc/B2/certify/`, twice: both passes "0 lines ran, 5 known" and "0 lines ran, 6 known". The store's diff is the five laws only.
- pytest: `test_core_structures.py` (three new tests), `test_check.py`, `test_core_metrics.py`: 118 passed. The new tests fail before a9f8f8a and pass after (6ff2051).
- `scripts/check_spec.py`: its one known finding.
- `scripts/core_metrics.py` (with C1's uncommitted work in the tree, so totals mix the two agents): this bite's part adds homonyms 0, executive shadows 0, list helpers 0, unclaimed 0, loose helpers 0. The "real loose" list gains 12 names that are not helpers (the theories `EvidenceComposition`, `ErrorBase`, `NatsConversion`, the laws `AtLeastTheUnionBound`, `FailuresIndependent`, the conjunctions `AssumptionFreeComposition`, `IndependentComposition`, and the five claims); the metric counts every parametrized definition no record theory names, so `Semigroup`, `Quantale`, `TheBooleans` and `IntIsASemiring` are in its baseline the same way.

## Findings for other bites

- The tester leaves an axiom conjunct unsettled ("the law gave (axiom ...), not a Bool"), while run.py grades a law whose body is an axiom `AssumedGrade` when the demand accepts it. So `IndependentComposition productComposition` is not a line a test program can certify; the product is certified as an `EvidenceComposition` (`ProductIsAComposition`) and its hypothesis is the demand's. tester.py is C1's file; the question below.
- The kernel's `==` does not reduce on injections of a labeled sum (`finiteDistance 0.0 == infiniteDistance unit` stays stuck in `luthier eval`), so `structural Extended` has no computable equality and `Extended` gets its `Object` by cases in core.lut. A kernel bite.
- A profile cannot bind a parameter by the name of an alias type (`Extended`, `EvidenceBound`): the alias unfolds and `_head_name` sees the sum or record. Binding by parameter name works.
- The default of a claim's `<-` parameter is not used by the tester when the profile does not bind it ("bind a census"), so `NatsIsAConversion` takes `log` and builds its model inline.
- B1 can take `EvidenceBound` and `cappedSumComposition` from core.lut for `evidence : Demand -> C`; E2's edges name an `EvidenceComposition` per path, `cappedSumComposition` when none is named.
- The sentences in L10.3, L10.8 and L6.15 that question 1 costs are the record's, not touched here.

## Decisions taken on my own

1. The bases are claimed as dioids, not as `Quantale` models: a quantale's `supremum : (I : U) -> (I -> Q) -> Q` has nothing to apply `f` to for an arbitrary `I`, so no total model can be written and no finite test sees a complete join. `Dioid` is the finitary part; `Quantale` stays as the ideal, said in its comment.
2. The composition is a one-field record theory, `EvidenceComposition`, with the join, bottom and unit fixed by `evidenceDioid`: only the tensor varies among reasonable choices, and a reasonable choice is a dioid with the unit on top.
3. The independence premise is an axiom conjunct of `IndependentComposition`, accepted by a demand by name.
4. `EvidenceBound`'s fields are `failure` and `risk`, and it is an alias (4.R4 asks a law of a record at `U`); `Evidence` is laws.lth's.
5. The nats conversion is claimed as a map of orders with its two endpoints, with `log` a parameter of the claim.
6. The models live in core.lut, the file algebraic.lth's header names for models.
7. The cases are listed dyadics; no sampled line over arbitrary doubles.
8. Two controls for `ErrorIsABase`, so `Integral` is refuted apart from `Dioid`.
9. Helpers reworked into theory-named functions and `levels` renamed, for core_metrics.

## Question

Should the tester grade an axiom conjunct `AssumedGrade` (as run.py's `axioms` does for a law whose body is an axiom), so a claim like `IndependentComposition productComposition` can be a certified line whose grade says "assumed" rather than an unsettled one?

Coordinator's answer (2026-10-25): yes, in the bite that follows C1 in tester.py (with B1, B3 and D1).
