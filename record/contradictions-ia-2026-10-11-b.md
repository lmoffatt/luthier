# Second round: five critiques of draft 4, what is new, what survives

2026-10-11, late. Input: `docs/principles.md` draft 4 (c7c6396); the responses in
`record/IA/principles 2023 10 11 2/` (4f4e208): chatGPT, Claude max, DeepSeek, Gemini, Grok; Kimi's
file is empty at the time of writing. Same prompt as the first round. Judged against draft 4,
`docs/rationale/11-cost-valued-laws.md` draft 0, `record/decisions.md` to D-2026-10-11-n, and the
interpreter as it ran tonight. Written by Claude; verdicts are the model's unless a source is
cited. The first round is `record/contradictions-ia-2026-10-11.md`.

## 1. What the round found that the first did not

Nine new claims; the rest repeats the first round where draft 4 already answered (G3 load-bearing,
the world token, externs with hidden state, the hole's five kinds, process).

| # | Claim | Raised by | Status |
|---|---|---|---|
| 1 | L10's class is three things: exact quotient (G0), ball (`11` §3), connected component (D-m). A component is not a ball: A to B 0.06, B to C 0.06, tolerance 0.1, A and C share a component and may not replace each other | chatGPT, Claude max, DeepSeek | Holds; the word "component" in draft 4 is mine and wrong. It is a weighted graph; a substitution is a path whose summed distance is within the tolerance. G0's "the representative is free" and L20's specialization and bridges "coherent up to the law" also still speak in classes |
| 2 | Whether an agreement test is a law is answered both ways: W5 says "agrees with the native" is not a law (it copies an implementation), then draft 4 calls it the identity law of L21. And L14's gate ("no type with a law, no application") either lets any extern with a native twin through, bypassing G2, or blocks W5's bootstrap, since every function starts with zero laws (D-d) | Claude max, DeepSeek, chatGPT | Holds; the one item that needs his word, §2 |
| 3 | The holotype is assigned backwards: in nomenclature the holotype is the name-bearing specimen and the diagnosis is the text, so the native implementation is the holotype and the law the diagnosis; and L21 has the formula "checked by the same law", against itself | Claude max | Holds; a correction of the reading of his metaphor, proposed, his mark pending |
| 4 | `assumed` means three things (a kind of hole, a grade, the opt-out of D-n) and W6 says a law not known to be true is worse than a hole. W6's mutation criterion cannot separate a transcribed law from a description; a law over the theory's signature cannot transcribe a model's code | Claude max | Holds; one meaning (a grade) resolves the first; the signature criterion goes into W6 as the discriminator mutation lacks |
| 5 | L13 (draft 4) "the cache key does not depend on the observer" against L19 (draft 4) "identified by the demanded type and tolerance" | chatGPT, Claude max, DeepSeek, Grok | Holds; both sentences are mine, from the first round. Two caches: elaboration (types, derivable laws) observer-independent, the memo of results keyed by the demand |
| 6 | The distribution and level of a sampled certificate are not in its identity | DeepSeek | Holds; added |
| 7 | `x <- 1; y := f x; x <- 2; print y`: L16 freezes y (SSA), L19's "backward over names" could propagate | Claude max | Decided by D-i and settled by the implementation tonight: `y := x + 10` after `x <- 1` stays 11 after `x <- 2`; L9 to say that inside a block the text fixes which binding a name means, then dependencies give the only order |
| 8 | `Cost` conflates a measure with a proposition: a law returning 0.037 is neither true nor false; the proposition is cost ≤ ε with ε the demand's. And the chain sum is a bound only when every link is; the worst seen on a sample is not a bound; two certificates compose pointwise only over the same sample | chatGPT, Claude max | Holds; the measure/acceptance split reconciles G0 with G3 at no cost and goes into D8 and the open items; the sample condition goes into L10 |
| 9 | `test` is an action, actions are never served from the memo, yet certificates are paid once through the memo; the extern's hash does not include the host library's version (W10); an extern declaration does not say definition or action | Claude max | Holds; three sentences in L19 and L14 |

Smaller, accepted: L8 says `external`, the keyword is `extern`; L12's kernel reading is an
interpretation of computation, not the evaluator's mechanism (chatGPT); the Boolean interim for the
application should be named (Claude max): laws of the form d(f x, g x) ≤ tol with tol a parameter,
no composition along a chain, no run database, until G3's algebra exists; Grok's sufficiency policy:
the demand states the grade it requires and a certificate serves every demand whose tolerance and
grade it meets (`11` §4).

Not accepted: Gemini's "formidable" and "intractable" without a counterexample; DeepSeek's L5
"does not re-run" as a contradiction (it means a law is not a second implementation, L5 says so);
Grok's W1 against W4 (W4 selects the increment, W1 freezes it, already in W3 and W4 draft 3).

## 2. What needs his word

**L14's gate and W5's bootstrap.** L14 says "without a type with a law to validate against it is
not applied", from his "si el tipo no sigue la ley no se aplica el calculo". The quote says: a type
with a law that the extern fails, no application. The draft's wording says more: no law, no
application, and that blocks every extern at the start, where D-2026-10-11-d puts every function.
*Proposed*: an extern is applied under its declared type; where the type has laws it is validated
against them before application and refused if it fails; where it has none yet it runs, its
certificate graded by what it has, and it may replace the native only by the identity law of L21
with its distance (D-2026-10-11-m). The description is the type's laws, when they come; the
identity law admits a specimen to the planner, it never certifies the description, so G2 is not
bypassed. Touches L14 (his quote), W5 (his), G2.

**The holotype, the other way round.** G2 draft 3 reads his "holotipos" as: the law is the holotype,
the implementation the specimen. In nomenclature the holotype is the name-bearing specimen and the
diagnosis is the text, so the reading that fits both the word and W5 is: the law is the diagnosis;
a reference implementation (the formula over `Rational`, or the native) is the holotype; every other
implementation is a specimen compared to the holotype by the identity law and to the diagnosis by
the laws. Proposed as a correction of a reading, his mark pending.

## 3. Everything else, in draft 5

Mine, each reversible by one commit, marked "(draft 5)": the weighted graph in L10, G0 and L20
(claim 1); one meaning of `assumed` and the signature criterion in W6 (claim 4); the two caches in
L13 and L19, the sample in a certificate's identity (claims 5, 6); the text fixes the binding, then
the DAG (claim 7); the measure and its acceptance in D8, the sample condition on a chain in L10
(claim 8); `test` and the memo, the host version in the extern's hash, definition or action in the
extern declaration (claim 9); `extern` in L8; L12 as interpretation; the Boolean interim; the
demand's grade.

## 4. The process point, which is right

Claude max, DeepSeek and Grok say the bottleneck is approval: dozens of *Proposed* items, L10, L12,
L15, L16 and L20 retouched twice in one day, retouches landing without W2's worked examples. True.
Draft 5 adds no new mechanism; it rewords mine. What would stop the drift is his marks on one
draft, and the two items of §2 are the only ones that cannot wait for them.

## 5. Kimi and Perplexity, added later the same night (15fcaf7)

Both read draft 4, so the weighted graph, the two caches and `assumed` as one grade (draft 5)
answer part of what they say. What was new, all propagated in draft 6 as one or two sentences each,
except the last, which is for his mark:

- Kimi: if a result's identity carries the demanded tolerance and the plan, two consumers of one
  definition make two nodes, so "each node once" and "paid once" fail. Answer: once per plan; a
  stricter demand is another node of another plan; the looser certificate still serves what it met
  (L19).
- Kimi: L2's first clause ("asserts the laws") and its draft 4 clause ("structural, laws are
  evidence") contradict inside one L. Answer: the structural proposition outright, the laws through
  the certificate at its grade, and "guarantee" means what the grade says (L2).
- Kimi: there is no root tolerance; the outermost action has no caller, and L17 forbids constants.
  Answer: the action's tolerance is a declared default argument (D-2026-10-11-c), recorded with the
  call (L17).
- Kimi: progressive validation against hash-frozen certificates. Answer: a certificate is a
  snapshot; a later test issues a new one that supersedes it, both kept, latest in front, which is
  P3 (L19).
- Kimi: an axiom is an assumed inhabitant, against "no value inhabits an undefined type". Answer:
  an axiom is a law with grade `assumed`, not a value (L8).
- Kimi: L12's "the class's name" needs a canonical form G4 refuses. Answer: scoped to the
  decidable fragment, where a normal form exists (L12).
- Kimi: accept/reject pairs cannot carry graded truth. Answer: a pair over a law into `Cost`
  carries its parameters, as the tests already do (`08`) (W2).
- Perplexity: error, time and memory are not one scalar; the planner needs a trade-off it does not
  have. Answer: the trade-off is a parameter of the demand (L10, L17).
- Perplexity: meaning, realization under a plan and evidence state must be three objects (L19);
  forgetting must mean not materializing, never erasing what reconstructs (L13); effects on owned
  state are verified, irreversible or concurrent ones are typed, logged and audited (L12); two
  sessions differing in the order of independent bindings must be provably equivalent
  (`Confluent`, L19); an extern's certificate binds version and platform (L14); the trust boundary
  in four layers (L7).
- Perplexity and Claude high: W15 reports deadlocks but gives no order among the organizers.
  Proposed, his mark pending: the order of his tiers, guide, eurekas, good use; inside a tier the
  conflict goes to him (W15).

Not accepted: Perplexity's "G3 must be a prerequisite before building the planner" (the Boolean
interim of D8 is what the planner builds on first); Kimi's "an executable suite of Boolean pairs is
incompatible with graded truth" (it is Boolean at a declared tolerance, which is the interim).
