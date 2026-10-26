# The case against Luthier’s five novelty claims

## Overall judgment

The five claims in section 15 of [the related-work report](/home/lmoffatt/Projects/luthier/record/plan/related-work-2026-10-27/related-work.md:408) are stronger than the evidence supports.

None currently establishes a new general mathematical mechanism. Several ingredients have closer precedents than the report acknowledges. More seriously, two foundations already implemented in Luthier are unsound in demonstrated cases: the statistical interpretation of some sampling protocols, and the completeness of certificate identities. This review also found counterexamples to two of the implemented bound-transformer laws.

That does not eliminate the possibility of a useful systems contribution. It changes what must be claimed and demonstrated.

| Claim | Hostile reviewer’s judgment | What might survive |
|---|---|---|
| 1. Persistent, composable graded evidence | Important precedents are omitted; current sampling bounds are unsupported on some live paths | A precise admission system that preserves domains, distributions, assumptions and evidence kinds |
| 2. Controls and vacuity inside certificates | Useful integration, but the universal requirement for a refuted model per conjunct is untenable | Persistent, separately qualified evidence about specification discrimination |
| 3. Static transformers and dynamic balls as models of one theory | Established numerical ideas; the “same theory” qualification matters; current transformer laws have counterexamples | A checked relationship between static planning bounds and dynamic enclosures |
| 4. Substitution only along certified identities | Certified transformations and approximate relational verification already exist; the proposed transport rule is too general | Demand-driven selection using persistent, explicitly scoped transformation evidence |
| 5. Typed derivations across languages | Typed provenance and boundary-sensitive reasoning have substantial precedents; Luthier’s mechanism remains largely unspecified | Scientific contracts that jointly constrain ancestry, numerical error and trust across bridges |

The strongest defensible thesis is therefore an integration claim: Luthier might make a particular combination practical for scientific software. The present record does not establish either that the combination is unprecedented or that its guarantees hold end to end.

## Scope and evidence

I read the requested prompt, `CLAUDE.md`, the concepts document, the principles source, the related-work report, the foundations report, and the relevant algebra-audit reports, decisions and execution record. I inspected the corresponding specification and implementation paths and verified additional literature through primary sources.

The initial checkout was:

```text
698dccfe1993ae90b8eb5a5094180f0ff67a0941
```

During this review, independent activity advanced HEAD to:

```text
c57d0fcd733fd2a5fb801e99961f3a97c7d5071e
```

That commit added two comparison documents. The implementation files used for the probes retained the hashes recorded below. Existing certificate-store modifications were present before the review; a deletion of `BRIEF.md` appeared during it. This review changed no file.

All Python probes operated in memory using:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/home/lmoffatt/Projects/luthier/src \
/home/lmoffatt/miniconda3/bin/python
```

The interpreter was CPython 3.12.9. I did not invoke `luthier certify`, `luthier test`, `luthier run`, or pytest.

The distinction between historical and current defects matters. The algebra-audit decisions report that its original five concrete serving, retention, identity and reader defects were repaired. I do not count those historical findings as current failures. The findings below either concern surviving design problems, current source inspection, or direct in-memory counterexamples.

## 1. Persistent, composable graded evidence over a domain

### Where it is wrong or incomplete

**Sampling supports a distributional statement, not universal membership.**

L10.2, **the grade is derived from the domain and evidence cost**, correctly distinguishes exact evidence on listed inputs from statistical evidence under a distribution. But the concepts document also presents a model as the subtype

\[
\{m:S\mid \ell(m)\}.
\]

That mathematical subtype contains precisely the structures satisfying the law. A structure that passes a finite sample may still violate it.

These statements can coexist only if Luthier distinguishes actual satisfaction from acceptance under an evidence policy. Otherwise, ordinary subtype reasoning can silently turn an empirical judgment into a universal premise. Calling the structure a model “with a cost” does not by itself supply sound inference rules for that distinction.

The elementary obstruction needs no sophisticated theorem. Given finitely many observations on an unbounded domain, two functions can agree on every observed input and disagree elsewhere. No certificate format removes that ambiguity.

For arbitrary foreign programs, complete automatic semantic certification also encounters [1, Rice’s result that nontrivial semantic properties of partial computable programs are undecidable](https://www.ams.org/journals/tran/1953-074-02/S0002-9947-1953-0053041-6/S0002-9947-1953-0053041-6.pdf). This limits completeness, not the usefulness of restricted proof procedures or explicit empirical judgments.

**The current sampler can invalidate the advertised confidence bound.**

The [foundations audit, which demonstrates dependence in the live generator protocol](/home/lmoffatt/Projects/luthier/record/plan/foundations-2026-10-27/report.md), is decisive. The current definitions still include:

```text
scrambled(s) = 1327217884*s mod 2147483647
nextSeed(s)  = (s + 1) mod 2147483648
```

Multiplying consecutive seeds modulo \(m\) produces a rotation. It does not produce independent trials.

I independently checked the arithmetic behind its fixed counterexample. Let

\[
u_j=\operatorname{frac}\left(\frac{a(s+j)}m\right),
\qquad
A=\{u:\operatorname{frac}(1597u)<0.1\},
\]

where \(a=1327217884\) and \(m=2147483647\). The failure set \(A\) has approximately 10% marginal mass. In the transformed coordinate, consecutive observations advance by only

\[
d=\frac{1597a\bmod m}{m}
 =0.000279936473947.
\]

For 100 observations, the probability of missing this set under a uniform starting phase is approximately

\[
1-(0.1+99d)=0.8722862891.
\]

Grid and counter-wrap corrections are negligible at this scale. Under independent sampling, the corresponding probability would be

\[
0.9^{100}=0.0000265614.
\]

Nevertheless, the current function returns

\[
\widehat\varepsilon(100,0.05)
=\frac{-\log 0.05}{100}
=0.0299573227.
\]

Thus, a predicate failing on about 10% of the advertised marginal distribution can frequently receive a bound below 3%. Persistence makes this unsupported conclusion reusable.

**Pooling can count overlapping source coordinates as new evidence.**

The current pooling code retains the largest stretch per starting seed. That handles exact prefix replays, but distinct seed numbers do not establish distinct streams.

An in-memory call counted two 100-case stretches starting at seeds 7 and 8 as 200 cases. Under the consecutive-seed protocol, their union contains only 101 source coordinates.

This is not the ordinary repetition of values that occurs during independent sampling with replacement. It is reuse of the same positions in the deterministic stream.

**Evidence composition needs two distinct probability spaces.**

The default capped sum is a sound conservative choice when its inputs are valid bounds:

\[
\varepsilon_{\mathrm{combined}}
 \le \min(1,\varepsilon_1+\varepsilon_2),
\]

\[
\delta_{\mathrm{combined}}
 \le \min(1,\delta_1+\delta_2).
\]

But \(\varepsilon\) bounds failures under the distribution of future inputs, while \(\delta\) concerns the certification experiment. Their premises differ.

In particular:

- Independent certification runs do not imply independent deployment failures.
- Identical distribution names do not establish that certificates concern the same underlying input experiment.
- A downstream operation sees an upstream output distribution, which may differ from the distribution used to certify it.
- Selecting a promising law, implementation or region after examining many experiments needs a selection-aware argument.

An algebraic interface is useful here, but associativity and monotonicity alone do not establish probabilistic soundness.

**The existing report overstates the optional-stopping objection.**

Section 12 of the related-work report treats optional continuation of fixed-sample bounds too broadly.

For one fixed predicate under independent Bernoulli trials, suppose every observed failure permanently prevents a successful zero-failure certificate. Repeatedly inspecting the zero-failure bound does not automatically invalidate it. If \(p\) is the true failure probability, crossing

\[
p>\frac{-\log\delta}{n}
\]

while still observing no failures requires surviving a sufficiently long initial failure-free prefix. Its probability is at most \(\delta\).

That argument does not justify selective restarts, discarded failures, adaptive predicate selection, or the current dependent streams. It does mean that “samples accumulate over time” is insufficient by itself to establish a statistical defect.

[2, Howard, Ramdas, McAuliffe and Sekhon’s confidence sequences provide general time-uniform inference under specified assumptions](https://arxiv.org/abs/1810.08240). They are relevant, but should not be prescribed without first stating the actual experiment.

**“Proved” also hides a trust distinction.**

Specification 6.R1 permits proof by citation and records who checked the match, including `none`. That is an explicit trust mechanism. It is not the same as a proof object checked by a small kernel.

Assigning both zero statistical evidence cost can be a convention, provided the trust obligation remains visible and enforceable. It cannot establish that the two have equal assurance.

### Is it new?

The report’s contrast between proof assistants and testing tools is too coarse.

[3, Cruanes, Hamon, Owre and Shankar’s *Tool Integration with the Evidential Tool Bus* (2013) constructs claims supported by evidence, composes tool workflows, and maintains evidence as inputs change](https://link.springer.com/chapter/10.1007/978-3-642-35873-9_18). This directly anticipates persistent heterogeneous evidence orchestration.

[4, Bulwahn’s *The New Quickcheck for Isabelle* (2012) combines random, exhaustive and symbolic testing inside a theorem prover](https://link.springer.com/chapter/10.1007/978-3-642-35308-6_10). Integrating testing strategies with theorem proving is therefore established.

The blanket description of PBT as ephemeral is also false. [5, Hypothesis’s official documentation describes persistent failing-example databases, explicit examples and replay](https://hypothesis.readthedocs.io/en/latest/settings.html). That is not Luthier’s proposed composable probability accounting, but it defeats persistence alone as a differentiator.

These precedents do not establish that another system already implements Luthier’s complete proposed admission semantics. They do establish that the broad unification claim needs a much narrower comparison.

### Why might users reject it?

A scientist may reasonably prefer tests, a few runtime checks and a reproducible environment because:

- Choosing a deployment distribution is difficult and must be maintained.
- Numerical bounds, confidence risks and citation trust are easy to confuse.
- A dependency update can invalidate expensive evidence.
- Conservative composition can rapidly exhaust an evidence budget.
- Many workflows need confidence in one concrete result more than a statistical statement about an abstract distribution.

For illustration, summing a per-obligation risk of 0.05 across twenty obligations reaches the trivial bound 1. The system then needs deliberate allocation, stronger individual evidence, or a justified dependence treatment.

### What survives, with a concrete example

A useful surviving contribution would be **an admission system that preserves exactly what each piece of evidence covers**.

Consider an eight-sensor calibration pipeline:

```text
ADC conversion:
    exhaustive evidence over all 256 input codes

Numerical fit:
    sampled evidence under an explicit distribution μ

Error theorem:
    cited evidence under hypotheses H

Calibration table:
    listed evidence at specified calibration settings
```

A demand using an unlisted calibration setting must remain unsupported, even if another obligation has a strong sampled certificate. A demand whose data do not satisfy \(H\) must not inherit the theorem.

The potential advantage over the cited tools is having these distinctions govern one scientific execution automatically. That remains a candidate systems contribution. It requires repairing the sampler and identity foundations and completing domain-sensitive admission.

## 2. Per-conjunct negative controls and vacuity rejection

### Where it is wrong or incomplete

**The universal completion rule is false for some legitimate theories.**

L9.14, **a theory is done when every conjunct has a refuted model**, is stronger than the available model interfaces can support.

The control audits already provide counterexamples:

- `EmptyIsInitial` includes `NoValue Empty model`. There is no well-typed value of `Empty` with which to refute it.
- Several evidence-base conjuncts concern a fixed join, bottom or unit. The model parameter exposes only the tensor, so no replacement model can change those conjuncts.
- `UnknownComposesUnknown` follows from a wrapper returning `nothing` before consulting the model.
- `NatsOfNothing` follows from a fixed branch, independently of the supplied logarithm.

These are documented in [the machinery controls report, which identifies conjuncts unreachable by model mutation](/home/lmoffatt/Projects/luthier/record/plan/audit-algebras-2026-10-22/report-controls-M.md:20), and [the core controls report, which leaves the empty-type law uncontrolled for a mathematical reason](/home/lmoffatt/Projects/luthier/record/plan/audit-algebras-2026-10-22/report-controls-K.md).

Such conjuncts do not necessarily “describe nothing.” Some are consequences of definitions or typing. An unqualified control requirement makes completion depend on how the theory is presented and where its interface permits mutation.

A defensible replacement would distinguish:

- an obligation requiring a discrimination control;
- a consequence of other obligations;
- a property enforced by construction;
- an untestable or unresolved control obligation.

Those distinctions would themselves need justification. Marking everything controlled would defeat the purpose.

**One killed mutant proves very little about adequacy.**

A law can kill an easy wrong implementation while admitting scientifically useless ones.

Suppose the intended function is \(f(x)=x^2\), but the specification states only:

\[
f(x)\ge0,\qquad f(0)=0.
\]

Suitable controls can be refuted for both conjuncts. The constant-zero function still satisfies the complete specification.

That is not an inconsistency in the declared theory: L9.4, **laws accumulate and need not determine an operation**, permits underdetermination. It is a limit on what “controlled” can mean. The label cannot establish that the laws capture the scientist’s intention.

Likewise, “detected on every recorded seed” is not a general power guarantee unless the seeds and fault model support that interpretation.

**Vacuity detection depends on syntax.**

The current `_premise_split` recognizes implication, certain conditionals, and disjunctions with exactly one negated disjunct. Its comments explicitly decline to choose a premise when multiple disjuncts are negated.

Consequently, logically equivalent formulations can receive different premise accounting. This is a practical restriction, but it prevents a claim of semantic vacuity detection over arbitrary laws.

**Rejecting total vacuity does not establish adequate conditional coverage.**

For a law \(P\Rightarrow Q\), one case satisfying \(P\) is enough to avoid the current all-vacuous outcome.

If only one of 1,000 cases satisfies \(P\), the 1,000 observations can support a bound on failure of the implication under the original distribution. They do not support an equally strong bound on failure of \(Q\) conditional on \(P\).

Those are different claims. The `held` count is valuable precisely because a non-vacuous label alone is too weak.

### Is it new?

FitSpec and model-checking vacuity research are already acknowledged. The missing comparison is broader specification coverage.

[6, Chockler, Kupferman and Vardi’s *Coverage Metrics for Temporal Logic Model Checking* (2006, extending their TACAS 2001 work) studies mutations that reveal which parts of a system matter to successful verification](https://link.springer.com/article/10.1007/s10703-006-0001-6).

That research already asks whether a successful specification meaningfully constrains its subject. Luthier’s possible distinction is the persistent placement of discrimination evidence beside individual theory obligations and its use in normal reporting. The underlying adequacy question is established.

### Why might users reject it?

Controls introduce a second maintained artifact for each law. Redundant conjuncts, fixed definitions and parametricity can make suitable controls difficult or impossible.

There is also a risk of optimizing the wrong target: authors can write easy mutants to satisfy a completion metric while leaving realistic faults uncovered. Requiring more controls can produce paperwork without proportionate assurance.

A simpler alternative is a targeted mutation suite over a few important scientific contracts, with explicit premise-coverage requirements.

### What survives, with a concrete example

The useful contribution is **persistent evidence about discrimination, kept separate from evidence about the production model**.

For a monoid theory:

```text
Associative(op)
Neutral(op, zero)
```

one control might expose associativity failure, while

```text
op(x, y) = x + y + 1
```

is associative but fails neutrality with `zero = 0`.

The report should show the two obligations separately. A control entry for one must not make the whole theory appear adequately exercised.

This is already a concrete improvement over a single green mutation indicator. Its value survives if “controlled” means the recorded fault was detected, with explicit exemptions or unresolved status where mutation cannot reach a conjunct.

## 3. Static affine transformers and dynamic ball arithmetic

### Where it is wrong or incomplete

**The mathematical formula is useful, but its current floating-point realization does not satisfy its stated laws.**

The implementation uses `Float64` fields and ordinary arithmetic in [the transformer definitions](/home/lmoffatt/Projects/luthier/src/luthier/lib/core/properties/functions.lth:90). Its associativity law compares coefficients with exact `==`.

I evaluated the actual repository definitions through `Runner.value`, using `tester.load_program` only to load and elaborate the existing source.

For three transformers with sensitivities \(0.1,0.2,0.3\), zero defects, radius 16 and universally true domains:

```text
left-associated sensitivity:  0.006000000000000001
right-associated sensitivity: 0.006
ComposeAssociative:           false
```

This refutes the general exact law for the declared floating-point carrier. The listed dyadic examples were deliberately chosen to make their arithmetic exact. Their passing evidence does not extend the law beyond those cases.

**The computed pullback can violate its own tolerance.**

A second direct evaluation used:

```text
L       = 6.625806177666277
η       = 0
radius  = 100
ε       = 3.768059371243392
```

The implementation returned:

```text
δ = 0.5686944758427219
```

But its forward calculation gave:

```text
L*δ + η = 3.7680593712433925 > ε
PullbackMeets = false
```

The overshoot is one ulp. Its small size does not make it compatible with a claimed upper-bound guarantee.

Sound implementation needs a treatment of rounding in the bounds themselves. Forward bounds generally need conservative outward rounding; a backward allowance must be conservative in the opposite direction. A larger test census is not a substitute for those rules.

**The carrier omits necessary constraints.**

`Affine` stores its sensitivity and defect as unrestricted `Float64` values. For example, a transformer with sensitivity \(-1\), zero defect and radius 100 is structurally admitted, and the current `PullbackMeets` evaluates to false at tolerance 1.

If negative sensitivities are invalid, that restriction belongs in the carrier or the law’s premises. The prose meaning of “Lipschitz constant” cannot supply a missing executable precondition.

**An upper error bound is not an impossibility lower bound.**

L13.4, **transformers compose and pull output tolerances backward**, says that a demand below \(\eta\) is infeasible. The implementation accordingly returns no pullback.

That is a sound refusal to certify using this transformer. It does not establish that the computation cannot meet the tolerance.

The identity function, implemented exactly, admits the conservative transformer

\[
L=1,\qquad \eta=0.25.
\]

A requested tolerance of \(0.125\) is below that bound, yet the actual implementation has zero error.

Luthier must distinguish “this bound cannot establish the demand” from “no realization or budget can achieve it.” The latter requires a lower-bound argument.

**Balls do not automatically model the same exact algebraic theory.**

L5.4, **a decoration is another model of the source theory**, needs qualification.

With ordinary interval operations,

\[
[-1,1]-[-1,1]=[-2,2],
\]

rather than the singleton zero. Thus, treating the two interval occurrences independently does not preserve the additive-inverse law of a field.

Balls can provide a sound enclosure interpretation of real computations. That interpretation needs an enclosure relation and preservation theorems. It cannot simply inherit every exact equality of the real-number theory.

Even the runtime formula \(L(m)\rho+\eta(m)\) needs care. For \(f(x)=x^2\), midpoint \(m=0\) and radius \(\rho=1\), the derivative at the midpoint is zero while the output ranges over \([0,1]\). A certified \(L(m)\) must bound variation over the admitted neighborhood; it cannot merely mean the derivative at the center.

**The proposed connection is not implemented end to end.**

The source currently contains a `Ball` predicate meaning “distance is within a radius.” That is different from a midpoint-radius arithmetic carrier.

I found no implementation of `RadiusWithinTransformer`. The related-work report itself lists ball decorations as unfinished. The novelty claim should therefore describe a proposed interface, not an implemented unification.

### Is it new?

The static/dynamic separation is less absolute than the report suggests.

[7, Daumas and Melquiond’s *Certification of Bounds on Expressions Involving Rounded Operators* uses interval arithmetic, forward error analysis and independently checkable proofs to certify numerical bounds](https://guillaume.melquiond.fr/doc/09-toms.pdf). Gappa already connects executable enclosure calculations to formal statements about rounded and exact expressions.

[8, Müller’s *The iRRAM: Exact Arithmetic in C++* (2001) provides a real-number programming abstraction implemented through controlled approximation](https://link.springer.com/chapter/10.1007/3-540-45335-0_14).

These do not duplicate Luthier’s proposed evidence store and planner. They do undermine a broad suggestion that numerical programs, error bounds and executable approximations previously lived in disconnected worlds.

### Why might users reject it?

Global bounds can be pessimistic. Local bounds require domains, radii and branch conditions that are expensive to derive and maintain. Dynamic balls can add enough runtime cost to erase the benefit of a faster specimen.

For many numerical workflows, a residual check or a dedicated verified-numerics library offers a simpler route to confidence in the concrete result.

### What survives, with a concrete example

The surviving opportunity is **a checked relationship between the bound used to choose a computation and the enclosure returned by that computation**.

In illustrative exact arithmetic, suppose:

\[
B_1(\delta)=\delta+0.01,\qquad
B_2(\delta)=2\delta+0.02.
\]

Their composition is:

\[
B_2(B_1(\delta))=2\delta+0.04.
\]

An output demand of \(0.10\) permits input radius \(0.03\). If the actual input ball has radius \(0.02\), the corresponding output bound is \(0.08\).

A useful implementation would ensure that the static planner and the dynamic ball model use compatible laws, domains and arithmetic conventions. Existing tools cover substantial pieces; the proposed advantage is a shared, enforceable contract across the scientific workflow.

## 4. Implementation substitution only along certified identities

### Where it is wrong or incomplete

**Closeness does not transport arbitrary properties.**

L10.7, **certification transports along an identity with accumulated distance and evidence**, and specification 6.S11 are too general if read as rules for arbitrary laws.

Let two constant implementations return:

\[
B(x)=0.001,\qquad A(x)=-0.001.
\]

Their outputs are uniformly within \(0.002\). The exact law \(B(x)>0\) does not transfer to \(A\).

For approximate output agreement, the triangle inequality can justify adding distances. For an arbitrary predicate, transport needs an appropriate preservation theorem, margin, logical relation or sensitivity of the observation.

Therefore an edge must state which observations and laws it preserves. A distance between returned values is not a universal substitution license.

**The consumer’s sensitivity is essential.**

If two implementations differ by \(10^{-6}\), applying a consumer \(h(y)=10^9y\) can produce a difference of \(10^3\).

L6.8, **the demand’s tolerance is pulled backward through the consumer’s sensitivity**, correctly recognizes this. That principle must qualify every shorthand statement that path distances merely add. A graph with weighted edges is insufficient without the contextual transport rules.

**A sampled edge is not a pointwise identity.**

An implementation can agree with a reference almost everywhere under \(\mu\) and fail at the one input used by a demand.

Luthier may allow the demand to accept distributional risk, but then deployment must be related to \(\mu\). Choosing an input because it is exceptional, or selecting an implementation after examining favorable certificate results, changes the argument.

**Runtime identity is currently incomplete.**

I independently reproduced a small version of the foundations finding:

```text
readContext(key : String) : String :=
    extern "python:os.getenv" key
```

Changing one process-local environment variable from `"first"` to `"second"` changed the returned value through the actual bridge. The cone hash remained:

```text
sha256:d560902f7502f7ea9fe236d1e04230d85117bc7b20bdf77b8264b44481cebe29
```

The variable was restored afterward.

This directly limits the claim that a certificate continues to identify the behavior it certified. The foundations audit additionally demonstrates numerical changes under unchanged BLAS-threading identities. A certificate graph built on incomplete identities inherits those omissions.

**The selection mechanism remains unbuilt.**

The concepts document says that today a name has one binding and nothing chooses among specimens. Specification 9.S17 explicitly identifies the substitution planner as unwritten.

An architectural rule for a future planner is not yet evidence of a working optimizer.

### Is it new?

The comparison with PetaBricks omits closer work on verified transformations.

[9, Nötzli and Brown’s *LifeJacket* (2016) verifies precise floating-point transformations in LLVM using SMT reasoning](https://arxiv.org/abs/1603.09290).

More directly, [10, Carbin, Kim, Misailovic and Rinard’s *Proving Acceptability Properties of Relaxed Nondeterministic Approximate Programs* (2012) provides relational proof rules for approximate programs, including selectable implementations, with soundness verified in Coq](https://dspace.mit.edu/entities/publication/8415a1bb-3c5d-4f06-b205-e7eac2f5eb2c).

Luthier’s heterogeneous empirical evidence is a possible distinction. “Substitution requires certified relationships” is not.

Complete discovery of numerical identities also has known limits. [11, Richardson’s undecidability results apply to identity and sign questions in sufficiently expressive elementary-function languages](https://www.math.tecnico.ulisboa.pt/~lgodin/Seminario/richardson.pdf). They do not prohibit useful restricted rewrite systems or proof checking. They prohibit treating general identity discovery as a solved normalization problem.

### Why might users reject it?

With \(k\) specimens, maintaining direct pairwise relationships can require quadratically many comparisons. A reference specimen reduces the number of edges, but may give looser bounds through composed paths.

Further costs include domain partitions, distribution compatibility, resource estimates and invalidation after numerical-library updates. The cheapest certified route may also be slower than a simple hand-selected implementation once planning overhead is included.

A practical alternative is a small dispatch rule with a trusted fallback and a result-specific residual check.

### What survives, with a concrete example

The useful surviving contribution is **selection whose justification remains inspectable and scoped after the choice**.

Suppose certified output distances are:

```text
A to B: 0.003
B to C: 0.004
A to C: 0.004
```

A downstream consumer has sensitivity 100, and the final tolerance is 0.5.

The route through B permits a bound of 0.7 and must be refused. The direct A-to-C certificate permits 0.4 and can be admitted, subject to its domain and evidence conditions.

The advantage would be automatic selection using persistent mixed evidence, with an explanation naming the exact admissible route. Approximate relational verification already supplies much of the reasoning. Luthier must demonstrate the integrated workflow.

## 5. Typed derivations of values across language boundaries

### Where it is wrong or incomplete

**A hash of a realization is not a verified account of its ancestry.**

L5.22, **a value’s derivation records its semantically relevant realization**, and L5.23, **the demand selects the carried projection**, describe a useful objective. The concepts document says that today the result key is what exists of that derivation, while its representation and bridge declarations remain open.

The environment-variable probe shows why a complete key is already difficult. Host mutation, callbacks, native-library state, numerical controls and aliasing can all matter.

For example:

1. A bridge exposes a NumPy array.
2. Foreign code mutates that array in place.
3. The value returns with an old derivation reference.

A stored reference cannot establish that the current contents still satisfy the recorded account. The bridge needs ownership, immutability, copying, content validation, or another enforceable rule.

Non-adversarial scientific software can violate this contract accidentally.

**A small projection cannot answer every future provenance question.**

If only an error bound was materialized, a later question about calibration ancestry needs either the retained underlying graph or an explicit “unknown.”

This is consistent with L5.23’s qualification that what is not carried is not erased. It also means the costs have moved to retained storage and retrieval rather than disappeared.

A summary sufficient for one demand is not automatically sufficient for a stronger one. Replacing ancestry with a compact summary needs a theorem about the supported future observations.

**Provenance has real growth costs.**

Expanding a trace as a tree can duplicate shared ancestry exponentially. An immutable DAG avoids that duplication, but still needs storage, garbage collection, availability, invalidation and queries over retained dependencies.

At the time inspected, the 44 certificate stores under `src`, `docs`, `examples` and `tests` already occupied 17,972,988 bytes, about 17.1 MiB. This is not a performance benchmark or evidence of excessive overhead. It does show that persistence already has a tangible footprint before general carried derivations exist.

Hashing large mutable arrays may also require repeated full reads. Hashes reduce reference size; they do not make the referenced bytes free to identify or preserve.

**Boolean equality does not imply computable semantic canonicalization.**

The decision to avoid metric equivalence classes is sound. However, “a canonical form at the Boolean level” needs a restricted meaning.

Equality of integer values is decidable. Equality of arbitrary functions from integers to Booleans is a different problem. A complete computable canonical representation of their extensional behavior would exceed the limits discussed under claim 1.

A canonical form for syntax, or for a certified terminating rewrite fragment, is defensible. A canonical form for all Boolean semantic consequences is not established.

**The categorical description does not discharge the implementation obligations.**

Representing a computation by \((f,a)\) with \(\mathrm{ev}(f,a)=v\) is a useful organizing view. Calling the structure an intensional exponential and its transformations 2-cells does not specify:

- what a host mutation does to the object;
- how evidence attaches to the current bytes;
- how projections preserve their assertions;
- how bridge losses compose;
- which evaluation and composition laws hold.

Those remain necessary semantic contracts.

### Is it new?

The comparison with passive provenance standards misses language-based precedents.

[12, Swamy, Corcoran and Hicks’s *Fable: A Language for Enforcing User-defined Security Policies* (2008) uses dependent labels and protected policy operations, including dynamic provenance tracking](https://www.cs.umd.edu/~mwh/papers/fable.pdf). Its type discipline prevents ordinary application code from freely forging or severing label-value associations.

[13, Green, Karvounarakis and Tannen’s *Provenance Semirings* (2007) gives compositional provenance annotations and maps to different interpretations](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf). It does not cover arbitrary numerical foreign functions, but semantic provenance composition and projection are established ideas.

For language boundaries specifically, [14, Patterson and Ahmed’s *Linking Types for Multi-Language Software* (2017) addresses how types expose boundary behavior so programmers can reason about components linked with more expressive languages](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SNAPL.2017.12).

Together, these precedents defeat “provenance was passive until Luthier.” They do not establish that an existing tool provides Luthier’s complete proposed combination of numerical bounds, empirical evidence and scientific ancestry.

### Why might users reject it?

The application developer must maintain bridge contracts, trust declarations, data identities and provenance retention alongside the numerical program. Foreign-library updates can affect all of them.

A lighter alternative is an immutable result artifact with a manifest, environment lock, explicit calibration identifiers and runtime numerical checks. That may capture most of the scientific value without a new language or a derivation algebra.

There is no adoption study here. These are plausible reasons for rejection that the project should test with users.

### What survives, with a concrete example

The strongest surviving application is **a consumer contract that jointly constrains ancestry, error and trust across a heterogeneous pipeline**.

For example:

```text
Python calibration
    -> numerical fit
    -> C numerical library
    -> lower-precision export
```

The consumer requests:

```text
descends from calibration CAL-42
contains no assumed dependency
total certified numerical error <= 0.02
```

Suppose the upstream error bound is 0.015 and the export bridge adds 0.010, with unit sensitivity for this example. The result must be refused because the composed bound is 0.025.

A different bridge adding 0.001 permits 0.016. An opaque step that loses ancestry must leave the calibration requirement unsupported.

A manifest can record these facts; typed provenance can enforce related policies; verified numerical tools can establish bounds. Luthier’s possible contribution is making the entire contract govern one execution with one explanation. That capability is still to be built.

## What the novelty argument should claim instead

The report should retire claims of first invention for the individual mechanisms. A narrower statement would be:

> Luthier investigates an execution model for scientific software in which admission depends on persistent, explicitly scoped evidence, numerical bounds and selected provenance facts. Its proposed contribution is their integration across native and foreign implementations.

That is a research claim with identifiable obligations.

Before presenting stronger guarantees, the project needs to establish:

1. **Valid sampling semantics.** Identify the protocol and its assumptions, prevent overlap from masquerading as new evidence, and preserve failures.
2. **Complete execution identity.** Include or explicitly effect-track the state that changes certified behavior.
3. **Sound numerical implementation.** Repair the transformer carrier and laws, account for bound arithmetic, and distinguish conservative refusal from impossibility.
4. **Qualified control obligations.** Separate discrimination evidence from properties guaranteed by construction or derivation.
5. **Law-specific transport.** State what each substitution preserves and under which contexts, domains and distributions.
6. **An enforceable bridge model.** Bind derivation facts to current values and specify retention, mutation and projection.

The strongest evaluation would then compare a complete Luthier workflow with a small existing stack: scientific Python, property tests, targeted mutation testing, a reproducible environment, dedicated numerical checks and a result manifest.

The question is practical: does Luthier catch consequential mistakes that this simpler stack misses, while requiring less total maintenance to obtain the same assurance? The current record contains promising examples, but no comparative evidence answering that question.

## Reproduction and limits of this review

The direct implementation probes established:

| Probe | Inputs | Observed result |
|---|---|---|
| Transformer associativity | Sensitivities 0.1, 0.2, 0.3; zero defects; radius 16; true domains | `ComposeAssociative = false` |
| Pullback tolerance | \(L=6.625806177666277\), \(\eta=0\), radius 100, \(\varepsilon=3.768059371243392\) | Returned radius overshoots tolerance; `PullbackMeets = false` |
| Invalid sensitivity carrier | \(L=-1\), \(\eta=0\), radius 100, tolerance 1 | Structurally admitted transformer; `PullbackMeets = false` |
| Mode identity | Same law, cone, binding, seed 7 and requested cases 100; different modes | Equal entry identities |
| Overlapping stretches | Two synthetic drawn stretches of 100 cases, seeds 7 and 8 | Pool counted 200; rotation coordinates total 101 |
| Ambient host input | Same `os.getenv` extern and argument; environment values `"first"` and `"second"` | Different values, identical cone hashes |
| Rotation arithmetic | \(a=1327217884\), \(m=2147483647\), multiplier 1597, 100 cases | Approximately 0.872286 probability of missing the fixed 10% failure set |

The numerical counterexample was found using a deterministic scalar search with seed `20261027`, then reproduced with the pinned coefficients above through the repository’s definitions. The associativity and pullback evaluations used direct kernel-term applications loaded from `tests/tester/transformer_laws.test.lut`; they did not execute its test directives.

A supplementary `ComposeSound` probe stopped with `stuck match`. I draw no conclusion from that unsuccessful probe.

The prompt’s SHA-256 was:

```text
df3a2b3a84991a1ac7a8dbff72c2c103d6968e56216d59094fef7487130f1660
```

The principal implementation hashes, unchanged at the final check, were:

```text
src/luthier/lib/core/properties/functions.lth
f103d436bf91bf5335b1b352cb7365bf757b9770feea8613ca176695500401a7

src/luthier/lib/generators.lth
857af5f96250de7071ddf5756ff437b5f63e17f7e0ea12e42a29dc6f7d83e3a1

src/luthier/certify.py
4bb65734100ec18e0b33eecece4e7824719ee0901c1d7b3617a5a3e941ad7e5b
```

These findings refute particular general claims and implementation laws. They do not establish that every scientific program reaches the failing paths, nor that every stored certificate is invalid.

The decisions taken independently for this review were the selection of additional literature, the construction of the in-memory probes, and the separation of demonstrated defects from proposed capabilities. No language decision was adopted, and no repository or memory file was changed.
