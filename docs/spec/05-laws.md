# 5. Laws

Chapter 5 of the specification, draft 0, 2026-10-13. Sources: `docs/spec/05-static-semantics.md` §9 at bd4537e (presentations, translations, checks); `docs/rationale/11-cost-valued-laws.md` §2 and §5; `docs/principles.md` L3, L9.2 to L9.4 and L12 at 2b79c02; the decisions D-2026-10-11-a, -d, -l, D-2026-10-12-h, -i, -p, -al and -am; `src/luthier/checker.py` and `lib/laws.lut`, read only. Written by Claude Opus 5.5, the session integrating the specification. Since `Cost` is a library (D-2026-10-12-al), this chapter states what a law is over the cost type `C` of spec 6 and leaves the algebra to the library; the same holds for checks and their failures. It realizes L12 and the part of L3 on equality as a law. What a certificate of a law records is spec 6; how a law is tested, spec 7; which bodies the checker accepts as laws, spec 4.R6.

## §1 Notation

`C`, `≤`, `0`, `⊤`, `⊕` and `lift` are those of spec 6 §1, with the laws of spec 6.S5. `T` is a type, `x` a value of it, `p` a predicate over `T`. `E` is a type of failures, the reasons a check can give. `V` is the type a law's body is valued in: `Bool`, `C`, or a check type (§4).

## §2 What a law is

**5.S1. A law is a term with a verdict.** [implemented] A law is a term valued in `Bool`, or the type `Law` of what a test runs, possibly a function whose parameters are quantified, or a conjunction of such terms (spec 3.S12). Laws accumulate: a function may carry laws that constrain it without determining it, and the laws that determine it up to its equality are the limit a definition may reach, not a requirement (D-2026-10-11-d). Which laws to write is spec 4.R10: the properties that characterize, never a second implementation.

**5.S2. A law may be valued in `C`.** [decided D-2026-10-12-al] A law whose body is valued in `C` states a degree: `0` holds exactly, `⊤` fails, and what lies between is how far it is from holding. Such a law needs no cutoff to be stated; whether its cost is good enough is the demand's (5.S7). The interpreter has no `C` yet, and every law today is valued in `Bool`.

**5.S3. What the core asks of a law's value.** [decided D-2026-10-13-g] One operation, so that the certificate of spec 6 can be written over any of them:

| operation | laws |
|---|---|
| `verdict : V -> C` | for `V = Bool`, `verdict` is `lift`; for `V = C`, the identity; for a check type, `lift` of `holds` (5.S9) |

A law into a type with no `verdict` is not a law. The theory `LawValue V` that states this would live in `lib/laws.lut`, beside the laws of relations (D-2026-10-11-l), and is not written.

**5.S4. Equality is a law of the object.** [decided D-2026-10-11-f] The identity of two values is a law, and the type of its result says what kind: `Bool` where equality is decidable and structural (spec 4.R8), `C` where the carrier has a distance, the distance observed being the cost. An object's equality is the base of every theory over it (D-2026-10-12-ak), and its laws (reflexive, symmetric, transitive, substitutive) are stated in Luthier: for a structural `==`, in `lib/kernel_laws.lut` (spec 3.S36); for an observational one, by the author of the object, with the relations of `lib/laws.lut`.

## §3 Lifting and combining

**5.S5. The lift and its retraction.** [decided D-2026-10-12-am] A Boolean law reads as a cost by `lift` (spec 6.S5). Its retraction `exact : C -> Bool` is `exact c = c ≤ 0`, so it needs nothing beyond the operations already asked. `exact (lift b) = b` holds for both values of `b`: `lift true = 0` and `0 ≤ 0`; `lift false = ⊤`, and `⊤ ≤ 0` must be false. [decided D-2026-10-13-g] That last condition, `⊤ ≤ 0` is false, is the sixth law of spec 6.S5, so that a library cannot take `0 = ⊤`: the trivial algebra satisfies the five laws there and breaks the retraction L12.2 settles. The planner inserts `lift` where a Boolean law meets a cost, at no cost.

**5.S6. How laws combine.** [implemented] Today `&` joins laws, and it is the Boolean and; the conjunction of a theory's laws is one law with one certificate. [decided D-2026-10-12-al] Beyond that, the core asks nothing: Boolean laws combine by and, or, implication and quantifiers into a Boolean law; laws valued in `C` combine by whatever conjunction the library of costs provides, of which the two candidates of D-2026-10-12-p are examples; a combination of both lifts each Boolean part. The composition along a path is `⊕` (spec 6.S12), which is not the conjunction of two laws on one value and need not be the same operation.

**5.S7. No law carries a cutoff.** [decided D-2026-10-12-h] A law states a property or its degree, never a tolerance to accept it at: a tolerance does not survive composition, since two steps each within ε end up within 2ε, so the cutoff belongs to the demand, which hands it to whatever it asks for. The tolerances written in the libraries today are spec 11.S18.

**5.S8. Grades of parts.** [decided D-2026-10-12-i] When a law is a conjunction certified part by part, how the grades of the parts combine (the vector of grades, or the weakest) is the demand's choice.

## §4 Checks

**5.S9. A check is written once, explaining.** [decided D-2026-10-11-a] A predicate is written in the form that explains its failures, `p : T -> Failures E`, the list of failures it finds in `x`, empty exactly when `x` belongs to the subtype. The poorer forms are projections of it, chosen by the demand and never written by hand: every failure; the first `n`; the reason of the first, `T -> { ok : { x : T | p x } || failed : E }`; the refined value, `refine p : T -> Maybe { x : T | p x }`; and `holds p : T -> Bool`, whether the list is empty. `Bool` is the check that explains nothing, `Failures Unit` cut at one failure. A report (`check`, `test`, a diagnostic) asks for every failure, a condition (`if`, `refine`) for one, and the number is the demand's (P11). Not implemented: the checker accepts `Bool` and `Law` as law types and nothing else (`checker.py`), so spec 3.S12 and spec 4.R6 describe `Failures E` as designed, not as running.

**5.S10. Checks belong to a library.** [decided D-2026-10-13-g] By the rule of D-2026-10-12-al, `Failures E`, its projections and their composition live in a library, `lib/checks.lut`, not in the core. The core asks of a check type only the `verdict` of 5.S3, through `holds`, and that a condition can project it to `Bool` (spec 2 §4 translates `if` with a check as its condition). `WellFormed : Program -> Failures E` of spec 4.S21 is then a client of that library.

**5.S11. How checks compose.** [decided D-2026-10-11-a] `and` concatenates the failures of independent checks, which makes the explaining form an applicative functor; `or` holds when either holds and otherwise keeps both lists; `not` has nothing to explain when `p` holds and is taken on `holds`. Checks chained along a dependency (read, then validate, then fit) compose by the bind of the reason form and stop at the first failure. With the dependencies explicit, every failure is well defined: a failure blocks only the cone of its node.

**5.S12. Forms that are not projections.** [decided D-2026-10-13-g] Three contexts ask for more than the failures. A check that computes evidence returns it with the value, a dependent pair whose law says the witness attests `p x` (a Cholesky factor for positive definiteness; *certifying algorithms*, McConnell, Mehlhorn, Näher and Schweitzer, 2011); `refine` is the case where the witness is the value. A statistical check returns its statistic and its level (spec 7.S17), never a refinement, since a passing test does not establish the fact. A check within a tolerance keeps the tolerance in the type of what it refines. A check about the world refines the content it read, not the path it read it from (spec 10).

## §5 Presentations

**5.S13. Translations between presentations.** [decided D-2026-10-13-g] One mathematical object admits several presentations, equivalent choices of primitive operations and laws (a group by product, unit and inverse, or by division alone). A translation between presentations `P` and `Q`, type operators over `U`, is a pair `to : (A : U) -> P A -> Q A` and `from : (A : U) -> Q A -> P A` whose round trip is the identity under the equality each presentation carries (5.S4). The source records it as expressible in version 0 and checked once on De Morgan's laws, certified per model and not for every model; translations as a concept the language names and certifies are later work.

**5.S14. Presentations with no computable translation.** [implemented] Where no translation can be computed, the equivalence of the presentations is a law, one per pair of presentations. `Kernel` in `lib/probability.lut` reads one probability kernel as a sampler, a likelihood and the transform of each datum, with a law on each side of the triangle (the density pair; the slope of the transform; the uniformity of simulated transforms), certified on the model of the tape distances with negative controls that break one side each.

## Open

- O1, for the conjunction of costs and the algebra, now the library's (5.S6).
- O2, for the equality an object carries (5.S4).
- O4, for which laws compose under translation (5.S13).
