# The three levels of equivalence: what the principle changes, and whether it can be done

Written 2026-10-18 by Claude Fable 5.1, an agent of the coordinating session, on the brief
`prompt-explore.md` beside this file (D-2026-10-18-h). Inputs: `record/decisions.md` at e9229d6
(D-2026-10-14-c, D-2026-10-15-b, D-2026-10-16-i, -j, D-2026-10-17-f, D-2026-10-18-c, -d, -g, -h,
D-2026-10-13-m, D-2026-10-12-p, -q, -r), `record/principles-language.md` (L3, L5.17 to L5.21, L6,
L9.14 to L9.17, L10, L13, O1, O2, O5), `docs/spec/05-laws.md` §2 and §3, `06-certification.md`
6.S4 to 6.S16, `07-tests.md` 7.S8 to 7.S21, `09-planner.md` §1 to §4, `11-numbers.md`,
`docs/rationale/11-cost-valued-laws.md` §2 to §6, `record/plan/core-2026-10-17/execution.md`
(Status, sections 0, 2, 3.1, 3.5, 4, 6, 7), and the code read only to place changes:
`src/luthier/lib/{certification, laws, test, numbers, demand}.lth`, `arrays.lth` (the `approx…`
family), `src/luthier/{tester, certify, run}.py`. The papers read are listed at the end with what
of each was reached. What comes from a source is cited at the sentence; the rest is my proposal.

## 1. For Luciano

The principle (yours, D-2026-10-18-h): equivalence relation, metric and probabilistic metric are one
structure over three bases; a verdict is Boolean with a bound at one level; the cost is computed and
the demand collapses it; the budget scales with the bound. The literature backs the structure
literally: Lawvere 1973 makes a metric a category enriched over ([0, inf], +, >=) and a preorder one
enriched over truth values; Menger 1942 replaces the distance by the distribution of the distance,
with a t-norm in the triangle inequality; Mardare, Panangaden and Plotkin 2016 write the metric level
as an equational logic with indexed equations, s =_eps t, whose rules are Luthier's L10.5 (a bound
serves every looser one), 6.S11 (transport adds bounds) and L6.8 (operations non-expansive). The term
of art: categories enriched over a quantale; the bases are 2, [0, inf] and distribution functions.

What it changes, one sentence each.
- It retires the second kind of law: no law is valued in `C` (5.S2, L3.3). Every law is a Boolean
  claim at a bound; the tester records the cost it computed (the distance seen, the failure fraction
  bounded); the demand compares that cost with its own bound when served (L10.5 and L10.11's range
  field, written and suspended). `lift` and `exact` (5.S5) become one operation, the collapse.
- It closes most of O1: the algebra of costs is the choice of base. D-2026-10-12-p's two candidates
  are the two quantales on [0, inf] (+ Lawvere's, max the ultrametric); D-2026-10-13-m's three ways
  evidence composes (nested, independent, union bound) are the t-norms minimum, product, Lukasiewicz.
- It splits the word cutoff (D-2026-10-14-c, L5.17): the bound of a comparison (a ball's eps) is the
  demand's and leaves the entry's binding; a parameter of the algorithm (a rank floor, `lmTol`) stays
  in it with its two sides (D-2026-10-16-j). D-2026-10-18-g says the first; entries and regions don't.
- It makes 7.S11 (the rule of three) and 7.S17 (the sequential test) one thing: two estimators of
  Menger's F(t), the probability under the generator that the distance is within t.
- It gives D-2026-10-18-d's budget law its variable: the eps of the `Within` form the tester varies.

Feasibility. Boolean and metric: yes, now, by copying a mechanism that exists (laws.lth's
`Statistical` with its evidence `Tested`, tester.py's `run_statistical`) into a `Within` law with
evidence `Measured`. Probabilistic: recording (eps-hat, delta) per entry is one bite; the t-norm
composition has no consumer until the planner composes a path, so it is declared in the core and
built with the planner. Cost: about seven bites outside the core (two of text, startable now; two of
code after bite 13; one for the budget law's tester mode; two for the planner), half a bite of
declarations inside bite 6, and one re-certification of every store (536 entries, one night in bite 1).

Two questions only you can answer.

Q1. The identity laws between specimens (11.S18's `…Agrees`, arrays.lth's `approx…` lines,
numbers.lth's `Elementary` identities with `tol`): do they lose their tolerance parameter, the entry
recording the distance measured (normalized by the law's scale) and the demand's eps collapsing it
at serve time, while within-bound properties (`AssociativeWithin`, Higham's gamma) keep the theory's
bound and record the ratio seen? It reverses the part of D-2026-10-14-c that matched the tolerance
exactly as a law parameter (L10.5's suspension). Recommendation: yes; it is what D-2026-10-13-m said
of identities ("a description of a process, not the fit to a law"), and the only way a stricter fit
stops re-running the stores. Cost: one Opus bite and the re-certification.

Q2. Does the core absorb the principle's code now? Recommendation: no, beyond what bites 6, 8 and 11
carry already (`Metric`, `MetricWithin`, `Ball`; the probabilistic metric and the t-norm declared
beside them, no model). The recording bites, the spec and the principles go in a plan of their own
after bite 13 (D-2026-10-18-a); only the text (L3's clause, the spec's wording) runs now in parallel,
since it touches no file the core's bites write. Bites 4, 4b and 5 change by nothing.

One finding: D-2026-10-18-c says a metric gives an equivalence by a threshold. Only an ultrametric
does; otherwise the threshold gives a reflexive symmetric relation that is not transitive, L6.5's
ball. The core should declare it as the tolerance relation, and the equivalence from the ultrametric.

## 2. Per area

### 2.1 Principles (`record/principles-language.md`)

Source: L3 ("Equality has levels and belongs to the object"), L3.5 (the three planes,
D-2026-10-18-c), L9.17 (the budget law), O1, O2.

Proposed, for his marks:
- L3's statement restated to carry the principle: "Equality has three levels, one structure over
  three bases, and belongs to the object; a verdict is Boolean at a bound of one level; the cost is
  computed and the demand collapses it." A clause L3.6 with the bases named (Bool with and; [0, inf]
  with + or max; distribution functions with a t-norm), the citations (Lawvere 1973, Menger 1942,
  Mardare, Panangaden and Plotkin 2016), and the relations among levels as D-2026-10-18-c states
  them, with the correction of section 1 (threshold gives a tolerance relation; an equivalence is
  the discrete metric; order is the structure without symmetry).
- L3.3 reworded: the level is said by the law's form (a Boolean law, a `Within` law naming its
  metric, a `Statistical` law naming its distance between distributions), not by the result type.
- O1 narrowed from "the algebra of costs" to "which base and which t-norm a theory names, and how a
  bound's confidence is carried": the two candidates of D-2026-10-12-p are two quantales; the
  compositions of D-2026-10-13-m are three t-norms. It still blocks L10.8 (the t-norm chosen when
  a path is composed) and L13.4 (the additive defect, which no quantale gives; see 2.3). It no
  longer blocks L3.3, L5.4, L6.6, L10.3.
- L5.17 and L9.16: one sentence each separating the bound of the comparison (the demand's, out of
  the binding, no regions) from a parameter of the algorithm (in the binding, two sides).
- L10.1 to L10.3 read back: the bound is a value of the level's base; the evidence is the confidence
  of that bound (delta, n), which the three levels do not absorb; D-2026-10-13-m's two types stand.
- L10.8: the union bound named as the Lukasiewicz t-norm, the sum of evidence costs as the product
  t-norm (independence), the max as the minimum t-norm (nesting), each a parameter of the theory's
  cost type (P11, D-2026-10-12-q unchanged).
- L13.2 to L13.4 read back: rounding is not an enriched functor (a functor between [0, inf]-categories
  is a non-expansive map, Lawvere 1973 as presented by Baez; the doubles have an additive defect,
  L13.3); it is the separate claim `MetricWithin` of D-2026-10-17-f. The functor reading keeps its
  name as analogy, not as the structure.

Cost: one Sonnet bite of text, now; his marks after.

### 2.2 Spec

Source: 5.S1 to 5.S8, 6.S4 to 6.S16, 7.S9 to 7.S19, 8.S1, 9.S5 to 9.S11, 11.S10, 11.S16 to 11.S18.

Proposed:
- 5.S2 (a law valued in `C`) retired; 5.S3's `verdict : V -> C` replaced by the collapse, `C ->
  bound -> Bool`, one per base; 5.S4 and 5.S5 reworded (the level by the form; `lift`/`exact` the
  collapse at the Boolean base). 5.S6 and 5.S7 unchanged.
- 6.S4 and 6.S5: `C` is the base of enrichment; the table of five operations is kept and named for
  what it is (a quantale's order, unit, top, tensor, and the collapse); three models listed. 6.S6:
  the bound recorded is the worst normalized distance (metric) or the pair (eps-hat, delta)
  (probabilistic). 6.S11, 6.S12: unchanged in form; the tensor is + for distances and the t-norm
  for evidence. 6.S15: unsuspended at the metric level (bound <= the demand's eps, grade as today).
- 7.S9: the bound of a comparison leaves the binding (as 7.S17 already took the sequential cutoffs
  out). 7.S10, 7.S11: the sampled grade is a probabilistic bound on F(t) (eps-hat at delta, the rule
  of three its first estimator). 7.S14: cutoff sides only for parameters of the algorithm. 7.S17:
  the sequential test as the other estimator of F(t), under one heading with 7.S11.
- 8.S1: the cutoff table gains the demand's eps (distance) and its accepted failure fraction, beside
  the grade.
- 9.S5 to 9.S11: suspended today by D-2026-10-13-ad; the metric level makes an edge's distance a
  recorded number and a path's sum computable, so the clauses can be unsuspended when the planner
  is written, with no change of wording.
- 11.S10: the overlapping-interval comparison that "answers with a probability" is the probabilistic
  level, named. 11.S16, 11.S17: the functor reading as in 2.1. 11.S18: the `…Agrees` laws become
  identities with a measured distance (Q1).

Cost: two Sonnet bites of text, after Q1.

### 2.3 Theories (plane 2, the core; plane 3, the libraries)

Source: execution.md 3.1 (`Object`, `Metric`, its four variants, `Ball`, `Tolerance`,
`MetricWithin`), section 4 (the within-bound claims), D-2026-10-17-f.

Proposed for `lib/core/structures/equality.lth` (bite 6, declarations only, no model until a case):
- `ToleranceRelation (A : U) : { near : A -> A -> Bool }` with `Reflexive` and `Symmetric`;
  `thresholdOf (m : Metric A o) (eps : Tolerance) : ToleranceRelation A`, its law that the ball is
  reflexive and symmetric and the control that it is not transitive; `Equivalence` from an
  `Ultrametric` by a threshold, with its law.
- `TNorm : { t : Float64 -> Float64 -> Float64 }` with the four laws (commutative, associative,
  monotone, unit 1) (Schweizer and Sklar's axioms, as the history in Klement, Mesiar and Pap 2000
  gives them; I read only the publisher's description, not the book), and the three models named as
  the three compositions of D-2026-10-13-m: `minimum`, `product`, `lukasiewicz`.
- `ProbabilisticMetric (A : U) (o : Object A) : { F : A -> A -> Float64 -> Float64 }` with Menger's
  axioms as the t-norm literature states them (F x x t = 1 for t > 0; F x y = F y x;
  F x z (s + t) >= T (F x y s) (F y z t)); its first model is plane 3's: the sampled failure
  fraction of a metric law under a generator, which is what the tester estimates.
- The relations among levels: `discrete (o : Object A) : Metric A o`; `thresholdOf` above;
  `lipschitzEquivalent (m n : Metric A o) (k : Float64) : Bool` for comparing metrics
  (D-2026-10-18-c); refinement of equivalences as implication of `eq`.

Proposed for `laws.lth` (after the core, bite 9b): a constructor
`Within : (A : U) -> (A -> A -> Float64) -> (A -> A -> Float64) -> Float64 -> A -> A -> Law`
(the metric, the scale from the theory, the bound, the two values), evidence
`Measured : Float64 -> Evidence` (the normalized distance seen), `Settling` settling it by
`w <= bound`; `test.lth`'s `grade` unchanged (the grade reads the verdict and the coverage); the
pattern is `Statistical` with `Sequential` and `Tested`, lines 107, 153 and 250 of laws.lth today.

Plane 3 (bites 8, 11, 12, already planned): `within`, `withinOf`, `approxVec`, `approxMat` and
their `…Of`, `…Slack` variants (arrays.lth lines 134 to 172) defined by `Ball`; the within-bound
properties of `Doubles` as section 4 of the core's plan writes them, recording the ratio seen; the
identities of `Elementary` (numbers.lth lines 184 to 190) as kind (i) when the host's documented
ulps are cited (6.S9), as `Within` identities otherwise (Q1). Probability.lth's Kolmogorov distance
stays a `Statistical` law; Mardare, Panangaden and Plotkin 2016 single out total variation and
Kantorovich as the distances between distributions with an algebraic characterization, which is a
reason to offer them beside Kolmogorov when bite 12 comes, not a change now.

Cost: half a bite inside bite 6; the `Within` form is bite 9b (2.4).

### 2.4 Tester (`tester.py`, `generators.lth`, `test.lth`)

Source: tester.py's `run_statistical` (line 1337), `Tested` (201), `Classifier.sides` (1136),
`is_cutoff` and `CUTOFF_TYPES` (920), `new_entry` (1961), `settle` (2041); 7.S11, 7.S14, 7.S17.

Proposed, bite 9b (Opus, after the core): `run_within`, by the pattern of `run_statistical`:
evaluate the metric and the scale per case, keep the worst normalized distance per region
(D-2026-10-16-i), compare with the line's bound, write `Measured` into the evidence and the worst
into the entry; `Classifier.sides` counts sides only for parameters whose type the law takes as
the algorithm's (today `CUTOFF_TYPES` would list `Tolerance`; it stops doing so for the `Within`
bound). Bite 9c (Sonnet): the entry records eps-hat(n, delta) for every sampled law (7.S11 is
decided and not recorded, 6.S6), so the probabilistic bound exists in the store before anything
composes it. The sequential test changes by nothing; its comment says what it estimates.

Bite 9d (Opus, after 9b): the budget law of D-2026-10-18-d as a tester mode: run a `Within` law at
a list of bounds the line gives, record the resource (fuel, samples, steps) per bound, and the law
`ScalesAs` of the algorithm's theory compares the slope in log scale with the stated one. Waits for
bite 12 (the algorithms' theories) and for 9b.

### 2.5 Certification (`certification.lth`, `certify.py`, `demand.lth`, `run.py`)

Source: certification.lth's holes `C`, `entryBound`, `entryEvidence` (lines 84 to 86) and
`regionBound` (392); certify.py's `serves` (1070), `serves_over` (1082), `regioned` (727),
`pooled` (856); demand.lth's holes `bound`, `evidence`, `assumed` (65 to 68) and the field `delta`
(108); run.py's `Demand` (1693), `cutoff` (1737), `ACCEPT` (1668).

Proposed, in bite 9b: `C` filled per level (the Boolean base by `lift` of the outcome as today;
the metric base by `Float64` with `+`, `0.0` and `top` as infinity; the probabilistic base by the
pair (eps-hat, delta)); `entryBound` the worst normalized distance, per region; `serves` adds
`entryBound e <= bound d` when the law is a `Within`; `pooledCases` keeps the sum of n and the
union takes the largest worst; `Demand` gains `bound : Maybe Float64` filled by `run --bound` and
by the test line, recorded (L5.19). Transport (6.S11) and composition (6.S12) stay as laws with no
specimen until the planner. The two-entry rule of 6.S8 and D-2026-10-16-h stand: an entry failed at
its line's bound serves nothing, whatever it measured; only a passed entry serves a looser demand.

### 2.6 Planner (`09-planner.md`)

Source: 9.S2 ("today nothing chooses"), 9.S5 to 9.S11 (suspended), L6.3, L6.8.

What changes: the type of an edge's weight (a value of the level's base: 0 at the Boolean level, a
distance at the metric, (eps-hat, delta) at the probabilistic), the composition along a path (+
for distances; the theory's t-norm for evidence), and what the planner reads to predict resources
(the budget law, 9d). Fuzz's metric preservation (Reed and Pierce 2010: a function of type
`!_k tau -o sigma` magnifies distances by at most k) is L6.8 read forward; Luthier differs in that
the sensitivity is a law certified or cited per specimen, not a type the checker infers, so the
pull-back of the tolerance is computed from certificates. Duet (Near and others 2019) keeps two
languages because (eps, delta) privacy does not scale linearly as sensitivity does; that is the
reason D-2026-10-13-m's two types must not be merged into one `C` when the planner composes.

Feasible now: nothing to write; the first planner bite needs two specimens of one function with an
identity entry recording a distance, which 9b produces (the native and numpy `dot`). Cost: two
bites later, outside this plan's horizon.

## 3. Order of work against the core's plan

Core bites unchanged: 3 (landed), 4, 4b, 5, 7, 10, 13.
Core bites that gain half a bite: 6 (the declarations of 2.3: tolerance relation, t-norm,
probabilistic metric, the relations among levels; controls for the non-transitive ball).
Core bites that change by a sentence: 8 and 11 (the `approx…` and `within` lines are `Ball`
membership as planned; the identity laws keep their `tol` parameter until 9b, and the bite's
report marks each as kind (i) or (ii)); 12 (Kolmogorov noted as one distance among three).

After bite 13, the plan `three-levels-2026-10-18/execution.md`:
```
wave A (now, text, parallel with the core):  principles clause (Sonnet) | spec wording (Sonnet, after Q1)
wave B (after bite 13):                      9b the Within form, tester, certification (Opus)
wave C:                                      9c eps-hat recorded (Sonnet) | 9d the budget law's mode (Opus, after 12)
wave D (later):                              the planner's first two bites
```
Should the core absorb it: no (Q2). Three reasons: D-2026-10-18-a; 9b rewrites tester.py and
certify.py, which the budgets agent and bite 4b touch; 9b changes every sampled identity's key, so
it should run once, after the core's last re-certification and not before it.

## 4. Conflicts with principles in force

- D-2026-10-18-c's "a metric gives an equivalence by a threshold": only for ultrametrics; a word
  in the clause and a declared `ToleranceRelation`; cost nil.
- L3.3, 5.S2, 5.S4 (the result type says the level): the principle says the law's form does and no
  law is valued in `C`; three clauses reworded and `Law C` never built, a saving.
- D-2026-10-14-c and L10.5's suspension (the tolerance a law parameter matched exactly): Q1
  reverses it for identities; cost one re-certification.
- L5.17, L9.16, D-2026-10-16-j (every cutoff has two sides): the comparison's bound has none; the
  "above/below" regions of a `tol` disappear from the stores; cost inside the re-certification.
- P8 (no more bureaucracy than it pays for): two numbers per region per entry; the case that paid
  for it is D-2026-10-16-b (the fit at 1e-12 bought nothing at 1e-6) and every tolerance change
  re-running the stores.
- P6 (every change can be undone): 9b is one commit plus the stores, both kept in git; undoable,
  with the stores' churn as its price.
- L10.9 (no evidence for free): serving a looser demand from a measured entry is not free, the
  distance was measured; a failed entry still serves nothing (D-2026-10-16-h).
- L13.3 and L13.4 (the additive defect): no quantale gives it; `MetricWithin` keeps it outside the
  enriched structure, as D-2026-10-17-f decided; the principle does not absorb it and should not
  claim to.

## Papers, and what of each was reached

- Mardare, Panangaden, Plotkin, "Quantitative Algebraic Reasoning", LICS 2016, DOI
  10.1145/2933575.2934518. Read: the preprint at https://www.macs.hw.ac.uk/~rm4023/papers/QA.pdf,
  sections 1 to 3 and 5. Quantitative equations `t =_eps s` with eps a non-negative rational; rules
  (Refl) `t =_0 t`, (Symm), (Triang) `t =_e s, s =_e' u` gives `t =_{e+e'} u`, (Max) `t =_e s` gives
  `t =_{e+e'} s`, (Arch) the infimum, (NExp) operations non-expansive; a quantitative algebra is an
  algebra with a metric "possibly taking infinite values" whose operations are non-expansive
  (Definition 3.1); the induced distance on terms is a pseudometric (section 5). Hausdorff from
  quantitative semilattices, p-Wasserstein and Kantorovich from barycentric algebras, total
  variation from a variant (abstract). Gives Luthier: the form of a law at a bound, L10.5 as (Max),
  6.S11 as (Triang), L6.8 as (NExp). Differs: operations non-expansive by definition, where the
  doubles have an additive defect; equations derived, where Luthier samples them.
- Reed and Pierce, "Distance Makes the Types Grow Stronger: A Calculus for Differential Privacy",
  ICFP 2010. Read: https://www.cis.upenn.edu/~bcpierce/papers/dp.pdf, sections 1, 2 and 4.2. Every
  type carries a metric; `!_r tau` scales it by r; `tau1 (x) tau2` adds, `tau1 & tau2` takes the
  max; a c-sensitive function is a 1-sensitive one from `!_c tau` (Proposition 2.2); the metric on
  distributions is `(1/eps) max_x |ln (d1 x / d2 x)|`, and a 1-sensitive function into the monad is
  eps-differentially private (Lemma 4.2). Gives Luthier: L6.8's pull-back and the two products of
  L12's conjunctions (sum along a chain, max on one value). Differs: enforced by typing, not
  certified by testing.
- Near and others, "Duet: An Expressive Higher-Order Language and Linear Type System for Statically
  Enforcing Differential Privacy", OOPSLA 2019, arXiv 1909.02481. Read: the introduction and
  section 2 of the arXiv PDF. "Two separate, mutually embedded languages": a sensitivity language
  with metric scaling as Fuzz, a privacy language without scaling, because (eps, delta), Renyi,
  zCDP and tCDP "cannot be accurately modeled by linear type systems which permit unrestricted
  scaling". Gives Luthier: the reason distance and evidence compose by different rules.
- Barthe, Grégoire, Zanella Béguelin, "Formal Certification of Code-Based Cryptographic Proofs",
  POPL 2009 (CertiCrypt, pRHL); EasyCrypt is Barthe and others, CRYPTO 2011. Read: abstracts only
  (microsoft.com/research, iacr.org). Barthe, Köpf, Olmedo, Zanella Béguelin, "Probabilistic
  Relational Reasoning for Differential Privacy", POPL 2012. Read:
  https://users.dcc.uchile.cl/~folmedo/pubs/2012.POPL.pdf, sections 3 to 5: the alpha-distance
  between distributions with a multiplicative triangle inequality (Lemma 3.4), the (alpha,
  delta)-lifting of a relation, judgments `c1 ~_{alpha,delta} c2 : Psi => Phi`, sequencing adds the
  indices. Gives Luthier: the shape of a probabilistic bound as a pair and its composition. Differs:
  a derivation over program syntax, where Luthier's certificate carries (alpha, beta, delta, n)
  from a sequential test.
- Lawvere, "Metric Spaces, Generalized Logic, and Closed Categories", Rend. Sem. Mat. Fis. Milano
  43 (1973); reprint TAC Reprints 1 (2002). Reached: the reprint's author commentary (the 1973 body
  is scanned, no text), and Baez's presentation, https://math.ucr.edu/home/baez/act_course/
  lecture_31.html: base ([0, inf], >=, +, 0), identities `d(x, x) = 0`, composition `d(x, y) + d(y, z)
  >= d(x, z)`, the axioms dropped (symmetry, `d = 0` implies equal, finiteness); the commentary
  states the relation between truth values and distances. Gives Luthier: the one structure over
  Bool and [0, inf], and order as the structure without symmetry. Not reached: Lawvere's own text
  on functors as non-expansive maps; I take it from Baez and from Mardare's Definition 3.2.
- Menger, "Statistical Metrics", Proc. Natl. Acad. Sci. USA 28(12):535-537, 1942 (PMID 16588583,
  PMC1078534). Reached: the bibliographic record (Europe PMC); the PMC page has page images only.
  The definition and the t-norm I take from the history as the publisher's description of Klement,
  Mesiar and Pap, "Triangular Norms" (2000) gives it and from Schweizer and Sklar, "Statistical
  metric spaces", Pacific J. Math. 1960, cited there; neither read. Gives Luthier: the third base and
  the t-norm as the parameter of composition.
- Not read, named from memory, to be checked before leaning on them: Hofmann and Reis,
  "Probabilistic metric spaces as enriched categories" (2013), which would be the paper that puts the
  three bases under one definition; Flagg, "Quantales and continuity spaces" (1997).
