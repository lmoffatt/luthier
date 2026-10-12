# Draft 11 of the principles: the decisions

Draft 0, 2026-10-12. Written for Luciano, to answer before the execution starts. The execution
is in `plan-principles-draft-11-2026-10-12-execution.md`. Inputs: the six IA critiques
(`record/IA/principles 2026 10 12/`, 1429f35), the recommendations with his marks
(`record/recommendations-ia-principles-2026-10-12.md`, e8d7db1), draft 10 of `docs/principles.md`
(b7a7e23), `record/decisions.md` (6b729dc). What comes from a source is cited; the rest is the
model's proposal.

## Already decided by his marks, not asked again

D-2026-10-12-g (the shape of draft 11), -h (the cutoff is the demand's minimal cutoff for an
implementation to be considered), -i (the grade of a sum is parameterizable), -j (a sampled or
assumed value is a model with a cost; the statistics convert to a cost), -k (law and certifier are
distinct), -l (structure, theory, cost, resources, model, specimen), -m (actions on Luthier's own
state are memoizable), -n (L12: no unrecorded policy constants), -o (the two lints), -p (two
candidate cost algebras).

Three remain. Answer with the number and ok, no, or a correction.

## D1. Sampled links in a path (his mark on §4.2: "elaborate")

**What the two texts say.** L5 (equality has levels): identity composes as paths; under cost the
composed path costs the sum of its links, holds at the weakest grade, and a sampled link holds on
the inputs its samples cover, so the composition holds on the intersection of the certified
domains. L13 (one function, many paths): a sampled edge is admissible only as a direct edge,
never summed into a path, until a probabilistic bound exists as a law.

**What a sampled link asserts.** Let f, g be two specimens of one function, D the distribution
the samples were drawn from, n the number of samples, and c the bound observed: d(f x, g x) ≤ c
on every sampled x. Two readings exist. Under the first the certificate records the tests run:
the bound holds on the sample S. Then L5's intersection rule is exact and useless, since the
intersection of two samples over a continuous carrier is empty unless the same sample is reused.
Under the second the certificate makes a claim on D: the fraction ε of D where the bound fails is
at most ε̂(n, δ), with confidence 1 − δ, where ε̂ comes from the sample (with no failure seen,
ε̂ ≈ log(1/δ)/n, the rule of three at δ = 0.05). L7 already says the grade depends on the
distribution sampled, so the second reading is the one draft 10 takes.

**The probabilistic bound L13 waits for exists and is additive.** For a path f–g–h with both links
sampled over the same D: at every x where both bounds hold, d(f x, h x) ≤ c₁ + c₂ by the triangle
inequality; the fraction of D where either fails is at most ε₁ + ε₂ (the union bound). So the
composed link holds on D with bound c₁ + c₂, failure fraction ε₁ + ε₂, confidence 1 − δ₁ − δ₂.
Each quantity sums. With his conversion of statistics to a cost in nats (D-2026-10-12-j), the
evidence cost of a sampled link is −log(1 − ε̂) ≈ ε̂, and it sums along a path exactly as the
distance does. This is G2 applied: the sampled link is a cost, and costs along a path add.

**What stays forbidden.** A link sampled over D′ says nothing on D without a law relating the two
distributions, so two sampled links compose only when sampled over the same distribution, or over
one the demand names. And the sum is a bound, not a parameter: the 1/n normalization of
D-2026-10-12-p is sound for ranking (the planner's efficiency) and not for the guarantee, where the
union bound and the triangle inequality give the sum. The min/max model is sound only for the
Boolean lift (0 and ∞) and for a conjunction of independent laws read as a worst case; along a
path it understates.

**Proposed.** Sampled links compose along a path when sampled over the same distribution: distance
summed, failure fraction summed, confidence summed in δ. The demand's cutoff (D-2026-10-12-h)
applies to the composed distance and to the composed evidence cost alike, so refusing sampled
paths is a demand with evidence cost zero, a parameter (P11), and L13's "never summed" is
deleted. L5 keeps the composition and drops the intersection rule, which belongs to the first
reading. The choice of algebra for a conjunction of laws stays parameterizable
(D-2026-10-12-i, -p); the composition along a path is not.

This touches L5 and L13, both settled, and goes against DeepSeek, Kimi and GPT sp, who keep
L13's prohibition without naming the bound.

## D2. The conversion of statistics to a cost, and what `assumed` costs

His mark on §4.5: a is a model of A with cost C; the statistics convert to a cost; perhaps a log
cost in nats. Under it a certificate carries a law, a domain (the distribution or the subtype),
a distance bound and an evidence cost, and the grade becomes derived: proved and exhaustive have
evidence cost 0 on their domain; cases have cost 0 on the listed cases and ∞ outside; sampled has
the finite cost of D1. Only `assumed` has no evidence: at cost ∞ it is unusable, at 0 it is
indistinguishable from proved.

**Proposed.** The evidence cost of a sampled certificate is −log(1 − ε̂(n, δ)) in nats, with δ a
parameter of the demand. An `assumed` certificate carries the evidence cost the demand assigns
to assumptions, a parameter with no default, so that a demand that names none refuses assumed
values (D-2026-10-11-n stands: certification by default, opt-out in the demand). The five grades
stay as names in the certificate for the reader; the planner reads the costs.

## D3. The organizers as the precedence layer

His mark on §4.1 chooses Claude's suggestion (three G of two sentences each, each L under its G,
the G deciding between its Ls, G0 between Gs), and his mark on §3.2 accepts the orientation
paragraph with the Gs "unnumbered, no status". The two can hold together only one way.

**Proposed.** The Gs keep their numbers and their two sentences, carry no status and no mechanics,
and head the sections the Ls are listed under, so that the table of contents is the derivation.
The precedence line reads: the statement decides over its clauses; the G decides between its Ls;
G0 decides between Gs. The history of the eurekas and the P13 count go to the record.

## Settled by the model, one commit undoes each

- The changelog ("What is open" today) goes to the drafts table that
  `record/principles-language.md` already keeps before its Terms, which the projection drops.
- The examples stay attached to their entry, in a field of their own (his "ok" on §2).
- The lints enter in step 2 of the execution, after the record is current, since until then they
  fail on the known mismatch and teach nothing.
