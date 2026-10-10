# Organizing principles: analysis of Luciano's note of 2026-10-11

Source: `record/Lucianos ideas/principios organizadores.txt` (committed verbatim at fa3f972).
Written by Claude in the chat of 2026-10-11. What cites a source is marked by file or id; what is
proposed here is marked *Proposed*. Nothing in `docs/principles.md` is changed by this document.

Luciano's note: he is not happy with the list of principles (draft 1 of `docs/principles.md`, L1
to L20 and W1 to W14). A principle is an organizer and, as the word says, the first. He gives four:

- A. HoTT / category theory / type theory as guidance. From it: types as propositions, functions
  as types, functions defined as propositions (laws); laws define mathematical objects; a law
  gives a quotient, hence interchangeable values, hence optimization by time, memory or error.
- B. Compilation is triggered by external demand (a print, a value that leaves to the world); the
  demand fixes the type the print wants, and that fixes the path actually computed and the types
  actually computed.
- C. Luthier expresses ideas; a type is an idea; Luthier's idea is to help discover the invariants
  of computations. Laws must not copy the implementation (that duplicates information); they are
  properties, mathematical or not, that determine the function univocally. Functions are defined
  à la Russell and tested empirically. That an implementation is a value of a function type means
  it was validated at least once; validation is progressive.
- D. Bayes as a guide too: laws are not predicates to Bool but to a positive real cost. The least
  developed; fertile for linear algebra libraries, which give bounds instead of booleans, and for
  statistics and data. Lawvere's object classifier as the unifying frame, Bayesian statistics to
  compose it.

## 1. Where the twenty L fall

The complaint is about structure, not content: the L are consequences and the list presents them
as peers. Placed under the four organizers:

| Organizer | L it generates | Notes |
|---|---|---|
| A (type theory) | L2, L4, L5, L10, L16, L20, L6, L8 | L6 (code is data) through the universe; L8 (holes) is the hypothesis of a context |
| B (demand) | L13, L19, L12, L9, L18 | L9 (DAG) is what the demand walks; L18 (no effects) is B's precondition, not its consequence |
| C (ideas, invariants, empirical) | L1, L3, L5, L11, L14, W6 | L5 (a law characterizes, does not re-run) is C's "laws are not copies" |
| D (cost, Bayes) | L10 (choice by expected loss), L11 (statistical grade), L15 (tolerance), the "metric space" clause of L9 | |
| none | L7 (minimal core), L17 (every criterion is a parameter), L14's orchestration | engineering commitments; they belong with W |

Every L has a home except three, and those three read as rules of construction. So the four do
organize the twenty; the list was flat because draft 1 followed the evidence (what he said when),
not the derivation.

## 2. The four are not peers (*Proposed*)

If a principle is the first, only one can be. Read against standard dependent type theory (Agda,
Lean, Coq), A is that theory and B, C, D are exactly the three places where Luthier departs from
it:

- B: computation is proof search from a demanded type, choosing among inhabitants by cost, rather
  than normalization of a given term.
- C: laws are validated empirically and progressively, rather than proved; inhabitance is a
  graded claim.
- D: truth values are costs in [0,∞], rather than Bool or Prop.

So the structure is "type theory plus three deviations", and the deviations are what Luthier is.
This is sharper than four peers: it says what is borrowed and what is new, and each deviation can
be judged by what it costs relative to the theory it departs from. It also answers W13 (the
reasonable version first): A is the reasonable version, B, C, D are the wild one.

## 3. The four depend on each other

Three dependencies the note does not state:

1. A's quotient needs B and D. Two implementations are interchangeable only up to a distance (D)
   and only below the tolerance the demanded type carries (B). Without D the quotient is by exact
   equality and "optimization by error" is impossible; without B there is no tolerance to compare
   against. L9 already says the laws generate a metric space; L19 already says the demand fixes
   the mode. The note makes the quotient the heart of A, so A is not self-standing.
2. C's "validated at least once" needs D. In type theory a : A is a judgment, not a belief. If
   inhabitance means "validated at least once", the judgment carries a grade (L11), and that is
   only sound if truth itself is graded. So C's definition of inhabitance presupposes D, which is
   the least developed of the four.
3. B's "the demand fixes the type" is A's proof search with D's cost. The planner of L19 searches
   for an inhabitant of the demanded type; what distinguishes it from a proof assistant's search is
   that candidates are ranked by cost and the demanded type carries a tolerance.

Consequence: D, the least developed, is load-bearing for A and C. That is the one thing in the
note that should change the order of work.

## 4. The fourth principle, articulated (*Proposed*)

The marriage of HoTT and Bayes is from 2026-05-29 (`note:2026-05-29T14.14.08:matrimonio-hott-bayes`).
Deepseek's critique the same day (`dialogue:c886516d:critica-hott-bayes-sin-articular`) asked
three questions that were never answered: do paths become distributions, do typing judgments relax
into probabilities, does propositional equality stop being decidable. The note gives enough to
answer them, with the prior art of `record/prior-art-2026-10-09/reports/G-cost-valued-laws.md`:

- Truth values. The subobject classifier Ω (the type of propositions) is replaced by [0,∞] with
  0 = true and ∞ = false: Lawvere logic (Bacci, Mardare, Panangaden, Plotkin; G §2). A Boolean law
  is the degenerate case with two values. Luthier must fix the orientation once (G notes Caesar
  uses the dual).
- Equality. Propositional equality becomes a quantitative equation s =_ε t (quantitative
  equational logic, G table). The quotient of A becomes a pseudometric space; the class of L10 is
  the ball of radius the demanded tolerance; identity at distance 0 is the exact case. Paths do
  not become distributions; they acquire a length.
- Judgments. a : A does not relax into a probability; it carries a certificate with a grade (L11)
  and a worst cost seen with the input that reached it (G §2, from Hypothesis). The judgment stays
  a judgment; its evidence is recorded.
- Bayes. The bridge is cost = −log p. A bound ‖r‖ ≤ ε is a likelihood; a Boolean law is p ∈
  {0,1}, cost ∈ {0,∞}; under independence costs add, which is Bayesian composition; the choice
  among implementations (L10) is decision theory with expected loss; the progressive validation of
  C is posterior update as cases accumulate. This is where "Bayesian statistics to compose it" lands.

The ambiguity in "object classifier": in topos theory the classifier of propositions is the
subobject classifier Ω (Lawvere–Tierney); in HoTT the object classifier is the univalent universe
U, the type of types. The cost reading needs the first (Ω → [0,∞]); "a type is an idea" and
"code is data" (L6) need the second (types are values of U). Both fit, but they are different
objects and the note names only one.

## 5. Two things in the note to settle

- "Functions as types, defined à la Russell." Read in HoTT: a well-specified function is the type
  of implementations satisfying its laws, and the laws make it contractible up to the law's
  equality: one inhabitant up to equivalence, the "the" of a definite description. But most laws
  do not determine uniquely (associativity determines no multiplication; "monotone" determines no
  function). So there are two kinds of law: characterizing (the type is contractible, the function
  is "the f such that") and constraining (the type is a subtype of A → B with many inhabitants,
  and the implementation is one of them, chosen freely, P5). The note demands the first for every
  function. The spec and L4, L5 allow the second. This is a real difference and it decides what
  `luthier check` requires of a definition.
- "Laws must not be copies of the implementation" against W5 (native slow and extern fast, with the
  test that they agree). L5 reconciles them (the native definition is one more model certified
  against the law), but the note reads as if the oracle pattern itself were the thing to avoid.
  If so, W5 keeps its place only as a bootstrapping practice, not a principle.

## 6. What the note leaves out

L7 (minimal core executable by hand), L17 (every criterion is a parameter) and the orchestration
half of L14 are not consequences of A to D. They are commitments of construction and would move
to the way of working, next to W3 and W10. The note's "a type is an idea" restates P14 (a type is
a concept) and L1.

## 7. The question

Does he accept the structure "type theory as the first principle, with three deviations (demand,
empirical validation, cost), the twenty L placed as consequences under them, and L7, L17, L14's
orchestration moved to the way of working"? If yes, draft 2 of `docs/principles.md` is a
reordering with the sources kept, and §4 becomes the first worked text on D, which §3 shows is
load-bearing. If he wants four peers instead, the reordering is the same and only the heading
changes.

## Decisions taken by the model

- Committed his note verbatim (fa3f972) and wrote this document. No change to `docs/principles.md`.

## Addendum, same day: two more organizers in the note

Luciano added two before and after the analysis above (committed at fa3f972 and the commit
following it). The analysis above did not cover them.

- E. Expressive over restrictive: if there is more than one way to do things, all should be
  expressible in Luthier. It organizes L10 (many paths), the SSA rebinding and the default
  arguments of 2026-10-11 (D-2026-10-11-c), and P5 (a free choice is legitimate). It pulls against
  W3 (start minimal) and L7 (minimal core); the resolution already in force is that the core is
  minimal and the expressible surface is wide, through libraries (L7's second clause). *Proposed*:
  E is a rule for deciding between designs, so it belongs with the generators, and W3 is the
  order of work, not a limit on the language.
- F. Clear separation of the declarative and the executive; the executive is given by the demand,
  and the declarative becomes everything that is universal, minimally processed. He says F gave
  rise to B. So F is the generator and B its first consequence; "universal" is L20, "minimally
  processed" is L19's "the program is the synthesis and is kept", and L12 (two faces) is F
  restated. *Proposed*: in the structure of §2, F replaces B as the second deviation from type
  theory, which has no executive face at all: there computation is normalization of a term, with
  no demand.

## Addendum 2: why depart from type theory

Source: `record/Lucianos ideas/el problema de los floating point.txt` (committed verbatim, same
day): type theory works for integers and stops working for float, linear algebra and statistics;
there Boolean type theory fails, and to be strict or expressive one needs something else, hence
[0,+inf).

*Proposed* sharpening, because the diagnosis decides what D has to be. Type theory does not fail
on floats: Float64 is an ordinary inductive type, IEEE 754 operations are total functions on it,
and Flocq proves exact theorems about them in Coq. What fails is the law of the ideal object
(associativity, A·A⁻¹ = I, a probability integrates to one) when it is asserted of the concrete
realization (L15). There is a Boolean way out and it is what Flocq takes: the law becomes an error
bound, |fl(a+b) − (a+b)| ≤ ε|a+b|, a predicate parametrized by ε (P11). It is honest and it stays
inside type theory. Its cost is threefold: ε is fixed in the law, so one law per tolerance and
per representation; worst-case bounds compose into condition numbers and become useless after a
few steps; and nothing statistical can be said, which is the whole of the data case. [0,∞) is
what removes the three at once: the law states the distance, the demand states the tolerance (B),
so one law serves float32, float64, interval and exact (E, L10), and composition is of costs, not
of worst cases.

Integers are not the other side of the line; machine Int64 overflows, and the pattern is the same
(ideal ℤ, concrete realization). The difference is that for integers exactness is recoverable
(bignum) and for floats it never is, so the distance is intrinsic. The line is "the realization
satisfies the ideal law exactly" against "approximately", not int against float.

One consequence the note does not draw. Over integers a law's value is computed exactly. Over
floats the cost itself is not available: the ideal value (the real sum) is not in hand, so the
residual is estimated, by a bound, an interval, or a reference at higher precision on sampled
inputs. The value of the law is then a random variable, not a number. That, and not a preference,
is what makes "Bayesian statistics to compose it" necessary: D is not cost-valued laws alone, it is
cost-valued laws whose costs are themselves uncertain. It is the justification of D to write in
draft 2, and it is where the sentence "type theory fails for floats" would mislead a reader.

## Addendum 3: Russell settled

Decided D-2026-10-11-d (Luciano): laws accumulate; characterization is the limit, not the
requirement, because requiring it would forbid adding laws one at a time, against E. So in §2 the
third deviation (C) reads: laws constrain progressively and are validated empirically; a function
type is a subtype of A → B whose inhabitants are the implementations certified so far against the
laws it has so far; when the laws determine the function up to its equality the type is
contractible modulo that equality and the choice among inhabitants is by cost alone (L10); before
that, the choice is also free (P5). Open: W5.
