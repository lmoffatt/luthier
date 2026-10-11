# What eight critiques of draft 3 agree on, and what survives

2026-10-11. Input: `docs/principles.md` draft 3 (f156aeb, 38.7 KB); the eight responses in
`record/IA/principles 2023 10 11/` (a8e28f0; the folder's date reads 2023, the files are of
2026-10-11) to Luciano's prompt "critical analysis. Focus on detecting possible contradictions
that might hamper its implementation": chatGPT, Claude high, Claude max, Claude Opus medium,
DeepSeek (English and Spanish), Gemini, Grok. Judged against draft 3, `docs/rationale/11-cost-
valued-laws.md` draft 0 (4cdcd4c) and `record/decisions.md` up to D-2026-10-11-l, which the
critics did not have. Written by Claude; every verdict below is the model's unless a source is
cited.

## 1. The claims, their support and their status

Fourteen distinct claims. "Raised by" counts responses; "Status" says whether the claim holds
against the record as it stands today.

| # | Claim | Raised by | Status |
|---|---|---|---|
| 1 | `a : A` is at once a guarantee (L2) and a graded judgment (G2, G3, L11) | 8 of 8 | Answered in the rationale (§4: the judgment stays, its evidence is graded) but not in the principles; L2 needs the split |
| 2 | A quotient up to a tolerance is not a quotient (L10, L12 vs G3): closeness is not transitive, so chained substitutions drift | 7 | Holds; the rationale gives the budget (§2, sum along a chain) but L10 still says "class" |
| 3 | Laws that do not determine the function (D-2026-10-11-d) plus choice by cost (L10) lets the planner pick the degenerate representative | 6 | Holds and is unanswered anywhere; the sharpest one |
| 4 | The memo key (code, inputs, mode) is smaller than what a result now depends on: tolerance, model, plan, seed, run database; so L18 and W10 fail | 7 | Holds; `lib/plan.lut` (a718abc, same evening) makes the order of execution a value and confluence a law, which is the vehicle; the rule naming what identifies a result is not written |
| 5 | G3 is a candidate yet load-bearing (D8); a Boolean kernel is coherent on decidable types | 8 | Holds as a wording problem of D8; the rationale §2 already has the answer (`Bool` is the two-valued `Cost`) |
| 6 | Three things called cost (distance, −log p, grade) compose by different algebras | 4 | Holds; rationale §5 names both readings, chooses "both", defines no interface |
| 7 | Rounding `Real -> Float64` is not Lipschitz; L15's "expands distances by at most a constant" is false as stated | 2 (Claude high, max) | Holds, factually: two reals astride a rounding boundary land one ulp apart at any distance. Rounding is non-expansive up to an additive defect |
| 8 | `<-` is textual order, against L9 (statements commute) | 8 | Resolved by D-2026-10-11-i (each `<-` a fresh name, actions take and return the world) and implemented (ce9221c, 8bf3f4d, the session included); draft 3 §4 still says "his decision pending" in the bullet above the one that records it as done |
| 9 | Effects do not commute; memoizing an action suppresses it | 2 (chatGPT) | Resolved by the same decision (`w1 <- print w0 "x"`); the world as input makes the memo key differ |
| 10 | Two model-resolution rules in L20 (scope vs the type naming its model) | 4 | Resolved by D-2026-10-11-j (scope rule withdrawn); L20's text still carries "resolved from the scope" |
| 11 | "A module is a file as a namespace, until modules are values" vs L20 "modules are values" | 5 | Textual; terminology states today, L20 the design |
| 12 | A hole is five things (axiom, input, extern, pending, dead) that behave differently when demanded | 2 | Holds at the level of the spec, not of the principles: the elaborated form needs the kind of a hole |
| 13 | L14 (validated the first time an action asks) and L19 (tests are actions; what never reaches an output needs no certificate) give different defaults for one event | 3 (the Claudes) | Holds; one sentence decides it |
| 14 | The holotype formula `\x {x*x}` is a term, so checking a specimen against it is consistency against a reference model, which W5 says is not a law | 2 (Claude max, Opus) | Holds as stated; dissolves under the resolution of claim 3 below |

Smaller, all accepted as corrections for draft 4: "departs in three places" lists four; G4 is
listed as a source of L10 while "generating no L"; "three elements for associativity" is the
arity of the law, not a generating set (L5); L11's line between exact and statistical is
computability, which is the wrong line (associativity over `Int` is computable and not
checkable by running; the grades already name the right line: proved, exhaustive, cases,
sampled, assumed); L7 holds for the kernel given a plan, not for the planner; a `proved`
citation about `Real` says nothing about `Float64`, so the grade attaches to the type, which
names its model (D-2026-10-11-j), and `cite` must be checked to record it. Not new: `U : U`
(sixth round). Not followed: the Spanish DeepSeek's "graded type theory from the start"
(research, not a library; Claude max says the same) and Gemini's closing question.

What the critics could not see: D-2026-10-11-i and -j, which settle claims 8, 9 and 10, were
taken after the text they read. Claims 1 and 5 are settled in substance by the rationale, which
they had access to but which the principles do not reflect. The process points (W7: every
derivation *Proposed* with his marks pending; W14: 39 KB) are true and are what his annotation
of draft 3 is for.

## 2. What survives, in order of what it blocks

**One conflict needs a decision: the planner's freedom.** D-2026-10-11-d (laws accumulate; the
implementation of an under-determined function is a free choice among the inhabitants, P5) and
L10 (one function, many paths; the class is chosen by law, the representative by cost) together
let the planner choose, by cost, among every implementation that passes the laws known so far.
If `Sqr` is known by `sqr x >= 0` alone, the constant zero is in the class and is the cheapest.
Nothing in draft 3 forbids the substitution. The free choice of P5 is the author's, once; the
planner's choice is repeated and by cost, and the two were written as one.

*Proposed* resolution, one rule: the planner substitutes one implementation for another only
along a certified equivalence between the two, the identity law of L21 (a certificate of
identity is not a certificate of the law) with its result `Bool` or `Cost`; the class of L10 is
the component connected by such certificates, and the distance of a chain of substitutions is
the sum of its links (rationale §2). Consequences: W5's agreement test between native and extern
stops being a borderline oracle and becomes the law that admits the second specimen into the
class; the holotype formula evaluated over `Rational` is one more specimen with grade exact, and
checking against it is the same pairwise law (claim 14 dissolves); claim 2's drift is bounded by
the budget the chain carries; a lone implementation is never replaced. Cost: a new
implementation is not substitutable until an equivalence test against an existing one has run,
so the planner's menu is what has been compared, not what has been written. Touches D-2026-10-
11-d and L10, both his, G4 (every path expressible: still true, every path is written; only the
substitution waits for its law) and P5.

**One default needs a sentence: does demanding a value demand its certificates?** L14 says an
extern is validated the first time an action asks for it. L19 says tests are actions and what
never reaches an output needs no certificate. For `print (f x)` with no test demanded they
differ. *Proposed*: a demand for a value demands every certificate in its dependency cone, paid
once through the memo; `test` as an action is for demanding certificates without values. The
other reading (a value may reach an output uncertified) empties L2 (membership is a guarantee)
for exactly the values that leave the program.

**Two rules already decided in substance, to be written into the principles (mine to draft,
his to mark).**

- The judgment and its evidence (claim 1): `a : A` is one judgment, structural and static for
  the kernel's types; a law's certificate carries the grade and, for a law into `Cost`, the
  worst cost seen (rationale §4). L2 keeps "guarantee" for the first; for the second it says
  what the certificate says and no more.
- The result's identity (claim 4): a result is identified by code, inputs, mode, the demanded
  type and tolerance, the model, the seed, and the plan that produced it, the plan being a value
  (`plan.lut`); the run database is read by the planner to choose the plan and is not an input of
  the result once the plan is fixed; evidence accumulates by a separate action with its own
  record, so L19's "each node once" and G3's "kept across runs" do not meet. L18 (a definition
  has no effects) then reads "every strategy gives a result in the same class, at a distance
  the plan records".

**Three corrections of wording, mine, for draft 4.** D8's dependency note: G0's quotient needs
G3 only where the carrier carries a distance; on decidable types the exact quotient is correct
and the kernel proceeds (claim 5). L10: "class" in the theory, "ball of the demanded radius" in
the model (claim 2), with the rule above. L20: drop "resolved from the scope" (claim 10);
terminology: modules are values by design, files today (claim 11); §4: the block decision is
taken (claim 8).

**One correction of his reading, proposed, not taken (claim 7).** L15 draft 3 says rounding
`Real -> Float64` expands distances by at most a constant. It does not: it is non-expansive up
to an additive defect of about ε|x|, and for subtraction and division no per-type constant
exists, the condition number is per input (as the rationale §7 says of κ(A)). The functor
reading survives if the constant is replaced by "non-expansive plus an additive term", which
the cost algebra then needs: a multiplicative part (Lipschitz where it exists) and an additive
part (rounding). This is the interface claim 6 asks for.

**Two items for the spec, not the principles.** The kind of a hole in the elaborated form:
input, external, pending, assumed (claim 12); the world as an opaque, unique value, so that an
action rerun is never served from the memo (claim 9).

## 3. Decisions taken by the model in this document

- Not editing `docs/principles.md` while his marks on draft 3 are pending; the corrections above
  wait for draft 4 (the fourth round's lesson: the original changed under him).
- Treating the three Claude responses as one voice where they coincide, since they share a
  model; counts above count responses, not models.
- Leaving the folder name `principles 2023 10 11` as he wrote it.
