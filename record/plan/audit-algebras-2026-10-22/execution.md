# The algebra audit: execution

2026-10-23, Claude Fable 5.1, on `record/plan/after-core-2026-10-23/prompt-audit-synthesis.md`
(e3f5cad). The decisions are in `decisions.md` beside this file (questions 1 to 5). Each bite below
names its source ("audit" with the section of `report.md`, 5b1a05e; "record" with the clause or
decision), what to build, what it depends on, when it is accepted, and the model fit for it: Sonnet
for reading and mechanical code, Opus for code with judgment, Fable for theory. What is neither the
audit's nor the record's is marked "mine". Every bite: small commits staged by path, the stores it
moves re-certified twice (second pass 0 lines ran), the suite file by file under `timeout 1800`,
`python scripts/check_spec.py` with its one known finding, `scripts/core_metrics.py` with no count
up; a report `report-<bite>.md` in this folder ending with the decisions taken on its own.

Status, 2026-10-23: written; nothing started. Wave A runs now, alongside the core's list searches
(`prompt-list-searches.md`), which touches lists.lut and the helpers only; A4 and A5 touch
certify.py, so they wait until that agent lands. Waves B to D wait for the question each names.

Three bites of the three-levels report (`record/plan/three-levels-2026-10-18/report.md`, 2f9c42b,
section 3: 9b the `Within` form, 9c ε̂ recorded, 9d the budget law's mode) are planned there with
no execution document; the audit's numerical gaps are theirs, so they appear here as B1, C1 and C2
with that report as a source [mine: the folding].

## Status, 2026-10-26 morning (coordinator)

Luciano answered the five questions (D-2026-10-25-a), all as recommended, with question 1's
addition: the evidence composition is a parameter, any reasonable choice definable, none that can
loop. Done since: B2 (report-B2.md), C1 (report-C1.md), B1, B3, D1 and the tester's assumed grade
(report-b1-b3-d1.md), each re-certified with the suite green; the principles carry the answers
(L10.2, L10.3, L10.5, L10.8, L6.15, L9.14, L13.3, L13.4, L5.22, O13). D1 found 162 conjuncts across
56 laws with no refuted model (uncontrolled-2026-10-26.tsv); three agents write their controls now
(prompt-controls.md). Next: C2 (after C1), C3, then wave E with the planner.

## Status, 2026-10-23 evening (coordinator)

Wave A done: A1 (03723fa, b395a05), A8 (ac2c7b8), A2 and A7 (report-wave-a-2.md), A4, A5, A6 and the
order written (report-wave-a-1.md), A3, A9 (report-wave-a-3.md) and A3b, `q or not p` as a premise
with generators of related pairs (report-wave-a-3b.md); the run path's conjuncts and `implies` in
the runtime slice (1e3bd6f). The re-certification wave runs after it. Left by wave A for later
bites, none blocking B to E:
- comparisons are not typed (`x == "a"` with `x : Int` passes check): a typing bite, it moves cones;
- a name capture in elaborate.py's `solve` when a type parameter is named like the pattern's binder
  (`size` on a `List A` with a parameter `A`), worked around in `pickFrom`;
- premises seen in only 2 of 100 cases (`IntAntisymmetric`, `IntInjective`, `IntBijective`,
  `IntPartialOrder`) and 2 of 4 to 6 (the plan digest laws): their lines need related-pair
  generators too;
- certification.lth's `Outcome` has no `Vacuous` constructor (the tester writes `NotRunFor` with
  the count);
- roots of trust declared in the program go with D-2026-10-16-n's bite of the queue (the
  coordinator's answer to report-wave-a-2.md);
- pruning keeps the order but no law says so; added when a case needs it (P8).

## Wave A. Now, no question of his

### A1. The record's corrections (Sonnet; record only)

Source: audit 4.4, 4.6, 12 (O7); record D-2026-10-18-i, D-2026-10-12-p, L10.11.
Build: in `record/decisions.md`, a correction note after D-2026-10-18-i, the coordinator's, as bite
6's was: the resources are a typed vector (work, span, peak memory), work adding in sequence and in
parallel, span adding in sequence and taking the max in parallel, peak memory taking the max in
sequence and adding in parallel (Blumofe and Leiserson's work and span, the audit's reference); the
name "tropical semiring" does not fit (max with neutral 0 and + has no absorbing zero). In O1 of
`record/principles-language.md`, one sentence: the 1/n mean of D-2026-10-12-p composes only as an
aggregate carrying its count, (sum, n), the mean its projection, since the binary mean is not
associative (audit 4.6; L10.11's aggregates are summed across rows). O7 is closed and stays so.
Then `scripts/project_principles.py --write` and `--check`.
Depends: nothing.
Accepted when: `--check` prints ok; the two notes cite the audit by hash; `docs/` changed only by
the projection; the record and the projection committed apart.

### A2. The demand records every policy (Sonnet; run.py, demand.lth)

Source: audit II.2; record L5.18 (no unrecorded policy constants: thresholds, budgets, limits and
the planner's defaults are declared, passed and recorded), L5.19, D-2026-10-16-c, D-2026-10-16-d.
Build: run.py's `AXIOMS = "AssumedGrade"` and `Demand.combine` become fields of `Demand` in
demand.lth with declared defaults, recorded by `Demand.record` and listed in `RunRecord`; the
host-root exception (an axiom such as `ObserverIsFaithful` accepted as assumed under a stricter
outer cutoff) is represented as what the demand accepts by name, the mechanism of `--accept
assumed:NAME`, with the project's roots of trust as its declared default (L11.9), so a run's record
says why a stricter cutoff admitted an axiom. `Demand.key` unchanged (the two fields change no
result's value; say so in a comment citing 8.S8).
Depends: nothing.
Accepted when: a test reads `axioms` and `combine` from a run's record; demand.lth's record law
lists them and a control (a record that drops one) is refuted; the stores of demand.lth's cone
re-certified; the examples' run records are Luciano's to regenerate (CLAUDE.md), noted in the report.

### A3. Vacuity and the empty experiment (Opus; tester.py, laws.lth)

Source: audit 12 (vacuity, zero cases); record D-2026-10-16-m (a law all of whose cases are vacuous
is not run, its premise count the reason), spec 7.S12 (`n` counts evaluated cases), L12.7 (`then`
is material).
Build: the tester counts, per law, the cases where every premise held: a premise stated as a
subtype is counted already (regions "premise held"); a premise stated as `then` or as an `if p
then q else true` body is not, and the audit shows such a law passes with an antecedent never
true. A law with zero premise-held cases ends as `Vacuous` with the count, an outcome beside
`Passed`, `Failed`, `Unresolved` and `NotRun` in laws.lth's outcome data, never a pass and never
served. A line with `cases <- 0` is refused by `certify` as an empty experiment, with its reason;
listed cases that are empty likewise (`EmptyIsInitial`'s pass, 13c item 5, is the one exception,
kept and cited). An uncovered region stays what D-2026-10-16-j and L9.16 say (a cap at Sampled), and
the report says in one line what it does not claim (audit 12: a policy label, not a bound).
Depends: nothing.
Accepted when: tests for the three cases; a control (`x < 0 then x > 0` over `Nat`) reported
vacuous; the report lists every law of the tree that becomes vacuous or empty (a finding for the
coordinator, expected none); stores unchanged.

### A4. Obligations from the law, and the five operations (Opus; certification.lth, certify.py)

Source: audit 1.3 (the obligation set comes from the current law, not from stored entries; `allOf`,
`alternative`, `restrict`, `projectGrade`, `admit` with distinct empty cases); record 7.S22,
`Routing` (report-bite-13b.md, "Before the tag"), D-2026-10-18-f.
Build: `Routing`'s `obligations` reads the law's conjunction from the elaborated theory (the heads
tester.py's `conjunction_parts` gives), with the stored entries only as evidence; a store listing
two of three conjuncts serves nothing. The five operations named in certification.lth over the
evidence of one demand: `allOf` over required obligations (weakest by default, 5.S8), `alternative`
over entries of one obligation under one binding (strongest, as `_or_strongest` does), `restrict`
to a smaller domain (reach, regions), `projectGrade` (the demand's `combine`), `admit` (the cutoff).
Their empty cases are constructors (`NoEntry`, `FailedObligation`, `EmptyFold`), and certify.py's
`_or_weakest` and `_or_strongest` stop using `None` for two meanings. `certification_model.lut`
follows.
Depends: A5 may share the commit window; wait for the list-searches agent (certify.py).
Accepted when: the control (two of three conjuncts listed) is refuted; every store of the tree
passes `luthier certify` with 0 lines ran on pass 2; `certify`'s output on the tree unchanged.

### A5. Pooling indexed by the obligation (Sonnet; certify.py)

Source: audit 1.4 C (a seed is a replay coordinate; independence is the protocol's; the conjunct
must be part of the pooling key); record D-2026-10-16-g, 7.S13, 13c item 2 (`sampling` in the
identity).
Build: `stretches`, `pooled`, `pools` and `continuation` take the conjunct in `union_key`; callers
stop prefiltering; a docstring states the pooling preconditions (one law, cone, binding, sampling
identity and conjunct; the generator's distribution law of 7.S1 is what makes the stretches one
sample).
Depends: after the list-searches agent lands; may go with A4.
Accepted when: a test where two conjuncts' stretches under one seed never pool; the pooling laws of
certification.lth still certified; stores unchanged.

### A6. Checked construction at read (Sonnet; certify.py, certification.lth)

Source: audit 1.8 (constructors per evidence form, validation at deserialization); record L10.10
(only a certifier builds a certificate), 13c item 5 (`store_errors` enforces `admits` and the listed
census), `heldAsRun`.
Build: `store_errors` checks each evidence form's own fields: a `Proved` entry carries its citation
or the library guarantee it names (O10's syntax when it comes; today the name), an `Exhaustive` one
its mode or finite domain, a `Sampled` one its seed, generators and sampling budgets, an `Assumed`
one the demand that named it, a control its broken model; `latestInFront` checked once `notBefore`
is defined over the entries' ISO dates (a definition, not a hole). No schema version field until a
migration happens (P8; a real case first) [mine].
Depends: nothing.
Accepted when: a fixture per form is refused with a message naming the field; every store of the
tree passes; the theory's `heldAsRun` and the reader agree on every fixture of test_certify.

### A7. The key's laws say what finite tests can show (Sonnet; plan.lth, demand.lth)

Source: audit 3.3, 3.4 (`KeySeesThe…` and `PlanHashSeesTheSchedule` claim injectivity of SHA-256;
determinacy under call by need is asserted, not stated as a law); record L5.6, 8.S8, 8.S9,
`served_by` (compares the full key), L4.7 (a definition's result depends only on its inputs),
D-2026-10-15-d.
Build: restate the hash laws as: the key is the identity, the hash a digest, and a lookup compares
the full key (what `served_by` does), over listed cases; the determinacy of a pure cone under any
strategy as a law conditional on L4.7 (no `W` in the cone), with a control (a cone with an action is
never served from the memo). The semantic quotient (audit 3.5) is question 5 and waits (E1).
Depends: nothing.
Accepted when: check_spec ok; controls refuted; the restated laws certified; no claim of
injectivity left in plan.lth.

### A8. The planes' relations stated in the spec (Sonnet; docs/spec 3 or 4)

Source: audit 9 (the code's comparison relations and their contract); record L3.4 (the hash is the
strict level), L3.5 (the three planes), D-2026-10-17-d (pointwise equality of functions, sampled),
D-2026-10-17-f (`MetricWithin` is a separate claim), the correction to D-2026-10-18-c (a threshold
gives a tolerance relation).
Build: one clause with a table: `kernel.alpha_equal` and the canonical hash (the strict level);
`check.Typing.same` (the checker's definitional comparison, unknowns allowed, no semantic claim);
`elaborate.fits` and `refines` (compatibility for elaboration, never an authorization to
substitute; the `sibling_subtype` guard cited); `Object.eq` (the type's equality, plane 1);
`Metric`, `ToleranceRelation`, `ProbabilisticMetric` (plane 2); `MetricWithin` (the realization
relation, plane 3); `Pointwise` (sampled extensionality). Each row names what it preserves and what
it does not decide.
Depends: nothing.
Accepted when: check_spec ok; each row cites its function and its clause; no wording that lets a
sampled pointwise pass stand for extensional equality.

### A9. The kinds of a hole (Opus; elaborate.py, check.py; after the typing work is verified)

Source: audit 12 (O9: an inference unknown, an unfilled program parameter and an unimplemented
operation substitute and fail differently; compatibility functions let unknowns agree); record O9,
L2.3 (the elaborated form records which of the five a hole is).
Build: first verify what bite 4 of the core (typing for resolution) left: whether `x + "a"` still
passes `check` (record/plan/core-2026-10-17/decisions.md's finding); then the elaborated form marks
each hole's kind, and `fits`/`refines` never let an inference unknown discharge a semantic
obligation (a law's premise, a claim).
Depends: nothing of this plan; after the typing work.
Accepted when: a test per kind; `check` refuses the mixed term or the report says bite 4 already
does; the suite.

## Wave B. After questions 1 and 2

### B1. ε̂ at serve time (Sonnet; certify.py, demand.lth) [question 1]

Source: audit 4.2, 12; record L10.3 (ε̂(n, δ) with δ the demand's parameter), 7.S11 (suspended by
D-2026-10-14-c), D-2026-10-16-i (per region), 8.S1's `delta`, L5.19; three-levels report 9c.
Build: certify computes ε̂(n, δ) from the pooled n per region at the demand's δ when a sampled
entry serves, and `certify` and the run's record print it; `delta` gets a declared default
(L5.19) instead of `nothing`; `evidence : Demand -> C` filled for the sampled case as the pair
(ε̂, δ). Nothing new is stored: the entry already keeps n per region and δ is the demand's, so
recording ε̂ in the entry would bake in a δ [mine, against 9c's "recorded per entry"].
Depends: question 1 (the pair as the carrier).
Accepted when: the tape example reports ε̂ = 0.015 at δ = 0.05 for 200 cases per conjunct
(docs/concepts.md 6.4); a test; stores unchanged.

### B2. The evidence and error bases in the core (Fable; core/structures) [question 1]

Source: audit 4.1, 4.2; record D-2026-10-18-i with its correction, L6.15, `Quantale` in
algebraic.lth, `TNorm` in equality.lth, D-2026-10-13-m (nested: max; independent: product; union
bound).
Build: `Evidence` as the pair (ε̂, δ) with the capped sum per component, claimed as a `Quantale`
under ≥ and certified on listed cases; its control the sum in nats (the product t-norm) as a wrong
model of the law "the tensor is at least the union bound", refuted at (0.1, 0.1); the nats
conversion −log(1 − ε̂) kept as a map to [0, ∞], a quantale map only for the product tensor, said
in a comment. The error base ([0, ∞], +, ≥) claimed and certified likewise. One place (algebraic.lth
at `Quantale`, cited from spec 6.S4) states the two orders: the categorical ≥ of the base and the
numerical ≤ of admission (the demand's bound is met when the entry's value is ≤ it), so no `leq` is
reused silently across them (audit 4.1).
Depends: question 1.
Accepted when: both claims certified with their controls refuted; the comment on the two orders
cited from certification.lth's `serves`; core_metrics with no count up.

### B3. The grade as a projection of domain and cost (Opus; certification.lth, certify.py) [question 2]

Source: audit 1.2 (the chain orders admission labels, not certificates), 1.3; record L10.2, 6.S7
(the grade is a view of domain and evidence), D-2026-10-16-k (gradeRank the stand-in), test.lth's
`grade`.
Build: certification.lth derives `grade` from coverage and evidence (exact on a finite listed
domain, exact on a bounded box, exact under cited hypotheses, a statistical bound on a distribution,
assumed at the demand's price), `admits` from it; the chain stays the Boolean slice's admission and
the theory says so with its decision; the run's record carries the vector of its cone's grades
beside the weakest (5.S8 extended to the cone by the demand's `combine`).
Depends: question 2.
Accepted when: a reader check over every store finds the stored grade equal to the derived one;
tests; nothing served differently (the `certify` output on the tree unchanged).

### B4. Serving checks the domain (Opus; certify.py, run.py) [question 2; with the cost types, after C1]

Source: audit 1.2 (restriction to a smaller domain), 1.5; record L10.2, L6.9, L10.5 (suspended),
7.S3 (a number's bounds are part of its type).
Build: a listed-cases entry serves a run only at an input it lists (equality of the type's
`Object`); a sampled entry at inputs inside the generator's type (7.S3's bounds); exhaustive on its
box; proved under its hypotheses as parameters (L6.9). First a dry run that lists every run of the
examples served today by a `Cases` entry at an unlisted input, reported to the coordinator before
the change lands. L10.5 unsuspended at the metric level in the same bite (three-levels 2.5).
Depends: question 2; C1 (the bound recorded); B3.
Accepted when: the dry run's list is in the report; a test per kind of domain; the examples' runs
still served or refused with the reason named.

## Wave C. After question 3

### C1. The `Within` form and the bound transformer (Opus; laws.lth, tester.py, certify.py, core) [question 3]

Source: audit 5 (the carrier: metric levels, domain, radius, sensitivity, defect, evidence; the
composition; the boundary cases), 1.6; record D-2026-10-18-j, L9.18 (the ratio recorded, the range
as a premise), L6.8, L13.5, D-2026-10-16-j (the radius a region); three-levels report 2.3 to 2.5
(bite 9b).
Build: laws.lth's `Within` (metric, scale, bound, two values), evidence `Measured` (the worst
normalized distance, the ratio of error to bound), tester's `run_within` keeping the worst per
region, certify's `entryBound` and `serves` comparing it with the demand's `bound`, demand.lth's
`bound` filled by `run --bound` and the test line. In the core, beside `Lipschitz`
(properties/functions.lth): `BoundTransformer` = (L, η, D, r) with `compose` and its law
(L₂L₁, L₂η₁ + η₂, D₁ ∩ f₁⁻¹(D₂), min(r₁, (r₂ − η₁)/L₁)), the sum over several inputs and the max as
a named alternative, the boundary cases as laws (L unknown or ∞ gives no substitution; ε < η
infeasible, L13.5; an empty domain composes to an empty domain). `dot`'s two laws (D-2026-10-18-j)
claimed with their transformer; the identity laws lose their `tol` (D-2026-10-18-j).
Depends: question 3.
Accepted when: `dot`'s stability and sensitivity laws certified at ratio ≤ 1 and a control just
below the bound refuted; `compose`'s law certified on listed transformers with a control (a
composition that drops L₂η₁); the suite; one re-certification pass of every agreement law, its count
in the report.

### C2. The budget law's mode and the modulus (Opus; tester.py, a theory of resources) [question 3, after C1]

Source: audit 6 (a modulus with a domain and an infeasible case; measured, sufficient and
extrapolated distinguished; resources by kind), 4.4; record L9.17, D-2026-10-18-d, D-2026-10-16-m,
L6.2; three-levels report 2.4 (bite 9d); A1's correction.
Build: a tester mode running a `Within` law at a list of bounds the line gives, the resource (fuel,
samples, steps) per bound recorded, and a law `ScalesAs` of the algorithm's theory comparing the
slope in log scale with the stated one. The modulus as a partial function in a theory
(`Modulus : Bound -> Features -> Sufficient Resources | Infeasible Reason | Unknown`), with the laws
the audit lists (a stronger bound never needs less; a floor; a convergence domain). `Resources` a
typed record (work, span, memory) with its two compositions as laws (sequence, parallel), certified
on listed cases; no planner consumer yet.
Depends: C1; question 3.
Accepted when: bisection's modulus log₂(L/tol) certified against measured steps and a wrong exponent
refuted; the resource laws certified with controls (a span that adds in parallel); the suite.

### C3. Uncertainty's composition declared (Fable; core/structures/equality.lth; small) [after C1]

Source: audit 4.3 (marginals do not determine a sum's distribution; convolution needs
independence or a joint); record D-2026-10-18-c (the probabilistic level after, on the sequential
test), `ProbabilisticMetric`, D-2026-10-17-g (the pushforward of measures).
Build: declare the pushforward of a distribution through a function with its hypothesis as a
premise (independence, or a joint given), and the t-norm named per theory; no model until the
sequential test consumes it (P8).
Depends: C1 for the form; nothing else.
Accepted when: the declarations check; a comment names the first consumer; no store moves.

## Wave D. After question 4

### D1. A control per conjunct (Sonnet; tester.py, certify.py, cli) [question 4]

Source: audit 1.7 (coverage of faults, composite laws, statistical aggregation, admission policy);
record L9.14, 7.S19 (the rate of detection over several seeds, building), 7.S22, D-2026-10-22-a.
Build: a control runs every conjunct and records a refutation entry per conjunct; `control_status`
indexed by conjunct; `check -v` and `certify` list uncontrolled conjuncts; the detection rate over
seeds recorded as refuted seeds over seeds run (7.S19). Admission unchanged: an uncontrolled law
is listed, not refused (the audit's reading of the current policy, kept).
Depends: question 4; after A4 (the obligations come from the law).
Accepted when: the tape example lists its controls per conjunct; the report lists every
uncontrolled conjunct of the tree (the debt of D-2026-10-16-f (e), now per conjunct); the suite.

## Wave E. With the planner (D-2026-10-13-ad: after evidence), after question 5

### E1. The realization graph and its projections (Fable; demand.lth, plan.lth) [question 5]

Source: audit 10 (the quotient a congruence; projections preserve what later demands rely on; a
realization DAG first); record L5.22, L5.23, L10.13, D-2026-10-22-b (no syntax, no kernel change),
D-2026-10-22-c, O13.
Build: a derivation node is the result key with its inputs' keys, the specimens, the bridges, the
certificates by hash and the roots of trust (L5.22's list); the projection laws: a projection's
assertions follow from the record, it names the certificates it depends on, an unavailable fact is
`Unknown`, nothing is erased (L5.23); the equality of consequence as a law between two derivations
(certified, a relation), exact at the Boolean level (alpha-equal keys) and a ball at the metric
level (L6.5).
Depends: question 5; the planner's first bite.
Accepted when: the laws certified on listed derivations (two realizations of `a + b`) with controls
refuted (a projection that invents a certificate); no kernel change.

### E2. Transport as typed edges (Opus; planner.lut, certification.lth) [questions 1 and 3; with the planner]

Source: audit 1.6 (the direction, parameter and hypothesis substitution, domain pullback,
distribution transport, identity and associativity), 7 (an edge's fields; feasibility before
ranking; the ranking's normalization, ties, unknown resources); record 9.S5 to 9.S17 (suspended),
L6.5 to L6.9, L10.7, L10.8, D-2026-10-18-c's correction (a tolerance relation, no class), 6.S11,
6.S12 (suspended).
Build: an edge record (source, target, laws preserved, domain, bound transformer, evidence pair,
resources, direction, inverse where exact); path composition laws (associativity, identity paths,
domain pullback, L10.8's same-distribution rule); the planner filters feasible paths at the demand's
bound and evidence, then ranks by 9.S15 with its normalization, zero and unknown resources and ties
as declared parameters (L5.18). Unsuspend 9.S5 to 9.S11.
Depends: C1 (the transformer), B2 (the evidence base), the planner's first bite.
Accepted when: two specimens of `dot` (native, numpy) with an identity entry, and the planner
substitutes one for the other under a demand that names a bound, refusing it under a tighter one.

### E3. Decorations, bridges and feedback (later; O5, O3)

Source: audit 8 (a decoration's adequacy laws beyond functor and applicative), 11 (a bridge's
contract; action evidence); record L5.4, 8.S2 (suspended), O5, L11.10, L11.11, D-2026-10-16-n
("later, not in the initial version").
Build, when O1 is done: the first decoration (intervals) as a model of the theory with inclusion
laws and controlled rounding, the order of combining decorations the demand's; the bridge's
declaration of what it preserves, adds, assumes and loses, written for the first bridge that loses
something; each place's kind of feedback and the grade an action earns, as D-2026-10-16-n deferred.
Not scheduled.

## Cited, not reopened

- O7 (theories as cycles): closed by D-2026-10-12-z; the audit agrees.
- O11's string holes (`textParts`, `textJoin`, `natDecimal` in term_model.lut): Luciano's, after the
  core (record/handoff-2026-10-22.md item 5); nothing here touches them.
- O8 (the session's memo across items) and O10 (citation syntax): when their bites come, O10's
  `Proved` label carries the theorem's hypotheses as parameters (L6.9 already says so of links).
- O6 (units): blocks nothing; untouched.
- The audit's note that L15 and L16 do not exist: the audit's brief named them in error; the
  principles run L1 to L14 (CLAUDE.md's P numbers are the method's).

## Order

A1, A2, A3, A6, A7, A8 now, any order, one agent each (A1 and A8 text, no code; A2, A3, A6, A7 touch
disjoint files); A4 then A5 after the list-searches agent lands; A9 when the typing work is verified.
B1 and B2 after question 1; B3 after question 2; C1 after question 3, then C2 and C3; B4 after C1 and
B3; D1 after question 4 and A4; E1 after question 5 and the planner's first bite; E2 after C1, B2 and
the planner; E3 not scheduled. At most three agents at once (his rule of 2026-10-14).

## Decisions taken on my own (this plan)

1. The three-levels report's bites 9b, 9c and 9d are executed here (B1, C1, C2), since that plan
   has no execution document and the audit's numerical gaps are theirs.
2. B1 computes ε̂ at serve time at the demand's δ and stores nothing new (L10.3), against 9c's
   "recorded per entry".
3. The resources correction (A1) goes to the record as the coordinator's, with a line offering it
   as a question (decisions.md's last paragraph).
4. No schema version field (A6) and no fault families (D1) until a real case (P8).
5. Four audit items are the sessions' and not his: the unrecorded `axioms` and `combine` (L5.18),
   the obligation manifest (7.S22), the hash laws (8.S9), the planes' table (L3.5).
