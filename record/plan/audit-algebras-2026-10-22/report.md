# Audit of the algebras that Luthier still needs

**Read-only report, 2026-10-22**

Luthier already has a substantial Boolean algebra of certification. The five grades, their interim order, several aggregation rules, replay, disagreement, reach and refusal are written in Luthier and implemented in Python. The principal gap is the composition of these pieces into one consistent judgment about a particular model, domain and demand.

The most immediate findings are concrete:

1. Bounded retention can erase a current refutation and restore a passing grade.
2. Serving a law through its model’s conjunction bypasses the general veto for current failures and disagreements.
3. The certificates recorded as serving a run can omit required conjuncts.
4. Some parameters that change the sampling distribution are excluded from evidence identity.
5. The store reader accepts evidence and grade combinations forbidden by the store’s own Luthier predicate.

These findings precede the larger mathematical questions. A quantale, richer grade lattice or planner cannot repair inconsistent serving and identity rules underneath it.

## Scope and evidence

The audit covered the requested principles source, specification chapters, concepts document, execution plan, relevant decisions, the six named Python modules and their associated Luthier theories. The derivation record was included, together with the subsequently recorded **D-2026-10-22-b** and **D-2026-10-22-c**.

The principles source currently contains L1 through L14 and O1 through O13. The prompt’s references to L15 and L16 have no corresponding entries in that source.

The checkout changed through other ongoing work during the audit. The initial observed HEAD was `6cb39995d51afc820a0b9a2917c89393d09a8c14`; the final observed HEAD was `d59d36461117548aaa83c498a7274168ad88add7`. Findings therefore refer to the working-tree implementations and named functions inspected here, rather than claiming an immutable repository snapshot.

For the principal Python findings, the captured SHA-256 hashes were:

| File | SHA-256 |
|---|---|
| `src/luthier/certify.py` | `ca970a949958513ed74a997d5b06bbdbbc34ac1c9a682c4a4a2f31591fe90ced` |
| `src/luthier/run.py` | `0110c7fc229e8c55d774321599bac2155d13836b20c58d31f110a3cdd39eecd5` |
| `src/luthier/tester.py` | `d63e9cf89a6a9b918a61fdf31edf5eee4185d2cfaeb751220dd67e61e9bf5e60` |

Verification consisted of source inspection and deterministic Python probes using synthetic records in memory, with `PYTHONDONTWRITEBYTECODE=1`. No file was changed. No certificate store, result store, lock or project record was written. The full test suite and scientific examples were not rerun.

Throughout this report, **proposal** marks an audit recommendation, rather than an adopted language rule.

# I. Gaps that affect decisions the implementation already makes

## 1. Grades and certificates need an algebra indexed by what the evidence concerns

### 1.1 What is already defined

**L10.1 (a certificate records a law, its domain, its bound and its evidence)** gives the principal carrier. **L10.2 (a grade summarizes the domain and evidence cost)** gives its interpretation. **L10.4 (a certificate freezes the computation and sampling identity needed to reproduce it)** supplies provenance. **L10.9 (operations cannot improve evidence, cost or domain without justification)** constrains composition.

**Spec 7.S10 (the five grades absorb the older grade vocabulary)** makes the following distinctions:

| Grade | Meaning and boundary |
|---|---|
| `Proved` | A proof or cited guarantee, subject to its hypotheses and trust obligations. |
| `ExhaustiveGrade` | Every case in the stated finite domain or bounded box was checked. |
| `Cases` | The listed cases were checked, or an existential witness was obtained. |
| `Sampled` | Evidence concerns the distribution sampled, with statistical limitations. |
| `AssumedGrade` | The assertion is accepted under a demand’s assumption policy. |

The older names do not require additional grades:

- A point is one listed case.
- A census is a collection of cases.
- Bounded exhaustiveness belongs in the domain.
- A witness is evidence for an existential claim.
- “Certified” or “known” can describe reuse or serving status.
- Refuted, unresolved, not run and disagreeing are outcomes, rather than weaker successful grades.

`test.lth` explicitly defines:

```text
AssumedGrade < Sampled < Cases < ExhaustiveGrade < Proved
```

`certify.GRADE_RANK` implements the same chain. **D-2026-10-16-k (grade rank is the Boolean slice’s stand-in for evidence cost)** already identifies its provisional role.

Thus, the missing algebra is **not the existence of an order on five names**. That order exists.

### 1.2 What the rank cannot express

The chain orders admission labels. It does not establish that one complete certificate entails another.

For example:

- Exhaustive evidence on `{0, 1}` says nothing directly about input `2`.
- Cases on a grid and samples from a continuous distribution support different judgments.
- A citation can depend on a library version, platform or condition-number bound.
- A witnessed existential and a sampled universal concern different logical forms.

A grade comparison needs a compatibility judgment over the law, subject model, hypotheses, domain and distribution. Some of this is implemented through reach and fingerprints. There is no single specified order over the resulting complete certificates.

**Missing operations and laws**

The complete carrier needs explicit definitions for:

- Restriction to a smaller domain.
- Combining checks of the same proposition.
- Combining distinct required propositions.
- Comparing different distributions.
- Transporting between models.
- Combining trust assumptions.
- Projecting a detailed certificate to a displayed grade.
- Distinguishing evidence strength from information gained by a refutation.

In particular, a counterexample adds information while destroying successful certification. One linear “better grade” order cannot represent both facts.

**Proposal.** Keep the five-grade chain as an admission policy and display projection. Define an indexed evidence judgment, schematically:

\[
\operatorname{Evidence}(\text{law},\text{model},D,\mu,H),
\]

where \(D\) is the domain, \(\mu\) the sampling distribution when relevant, and \(H\) the hypotheses and trust assumptions. Define strengthening only between compatible judgments.

A partially ordered abstract domain is a suitable starting point. A complete lattice should be claimed only after its joins and meets have been constructed. The relevant precedent is [Cousot and Cousot’s lattice treatment of program properties and sound abstractions](https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml).

**Blocks:** a sound extension beyond Boolean admission, meaningful comparison of certificates, and automatic evidence transport.

### 1.3 Required conjuncts and alternative evidence are different operations

**L12.5 (grades of conjuncts may be retained as a vector or summarized by the weakest)** and **spec 5.S8 (the demand chooses how grades of parts are presented or combined)** describe a policy boundary. **Spec 7.S22 (conjuncts run independently, each with its own quantified variables and entry)** gives the current execution form.

**D-2026-10-18-f (the tester splits bare conjunctions into independently quantified laws)** is implemented in:

- `tester.conjunction_parts`
- `tester._run_conjunction`
- `tester._conjunction_outcome`
- `certify.certificate_grade_and_empty`

There are already several distinct operations:

| Situation | Current rule |
|---|---|
| Successful entries under one binding | Keep the strongest grade. |
| Different bindings | Combine, weakest by default. |
| Required conjuncts | Every listed conjunct must have evidence; aggregate weakest by default. |
| Regions | Combine the base grade with region coverage; empty regions can cap it at sampled. |
| Run admission | Each required law or conjunct must be served at the demand’s cutoff. |
| Controls | Kept outside the law’s successful grade. |

These rules are partly specified in `certification.lth`. Calling all of them “combine” obscures their different meanings.

`_or_weakest` and `_or_strongest` both treat `None` as an accumulator unit. Elsewhere, `None` means that a required conjunct has no successful grade, which prevents certification. Those meanings are operationally distinguished by surrounding code, rather than by the carrier.

The implementation also discovers the required conjunct manifest from stored entries. The obligation set should ultimately come from the current law. Absence of an obligation from evidence cannot establish absence from the theory.

**Concrete failure scenario:** a certificate summary over alternatives, regions or bindings is reused as though it established all required conjuncts. A maximum over alternatives is legitimate; a maximum over mandatory obligations can hide a weak obligation.

**Proposal.** Specify separate operations:

- `allOf`: evidence for every required obligation.
- `alternative`: compatible evidence supporting the same obligation.
- `restrict`: evidence on a smaller domain.
- `projectGrade`: the demand’s summary.
- `admit`: whether the detailed judgment meets the demand.

Give them separate empty cases. An empty accumulator, an empty conjunction, no observations and a failed obligation should have different constructors.

This can be expressed with products of indexed evidence and explicit abstraction maps to the grade chain. It does not require choosing a universal grade lattice immediately.

### 1.4 Lines and seeds: pooling needs a distribution identity and durable negative evidence

**D-2026-10-16-g (stretches under one law, cone, binding and distribution pool into one sample)** supplies an important rule. Replays count once; a larger run of the same seed contributes its largest prefix; exhaustive or listed cases do not become new evidence merely by changing the seed.

`certify.stretches`, `pooled`, `union_key` and `continuation` implement much of this.

Three gaps remain.

#### A. Retention can erase a refutation

At [`certify.py:604`](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:604), `prune` retains four recent current entries per group. It protects unresolved disagreement pairs. It does not protect an ordinary current failure.

An in-memory probe recorded one failure followed by four passes, all under the same current law, cone and binding:

| Recorded seed | Retained seeds | Certificate grade |
|---|---|---|
| 0, failed | `[0]` | None |
| 1, passed | `[1, 0]` | None |
| 2, passed | `[2, 1, 0]` | None |
| 3, passed | `[3, 2, 1, 0]` | None |
| 4, passed | `[4, 3, 2, 1]` | `Sampled` |

This conflicts with **spec 6.S15 (a current refutation refuses the law regardless of successful entries)**. Additional passing samples cannot invalidate a counterexample to a universal claim.

The bounded-store requirement and the refutation requirement need a joint law. The append-only reference operation `recordEntry` does not supply that law for pruning.

**Proposal:** retain current negative evidence or a durable refutation summary independently of the bounded positive sample cache. Require pruning to preserve refusal and unresolved conflict.

#### B. Distribution-changing parameters are outside identity

**Spec 7.S8 (all budgets are recorded and excluded from entry identity)** generalizes the reason for excluding fuel: fuel only cuts execution.

That argument does not cover every field called a budget.

`Values.draw_base` and `Values.degenerate` use `specialMass` and `atomAtZero` to change the distribution. Classifier budgets can change observed region information. `new_entry` records budgets, while `certify.identity` excludes them.

A probe changing `specialMass` from `0.05` to `0.45` produced the **same identity**.

Consequences include:

- Reusing an outcome without running the newly requested distribution.
- Treating different sampling protocols as one stretch.
- Recording a replay disagreement caused by an omitted input.

`drawing_revision` fingerprints implementation code. It does not encode these argument values.

**Proposal:** classify parameters by semantics. Pure execution limits may remain outside evidence identity. Distribution parameters belong in the sampling identity; classification parameters need an explicit evidence-version rule.

#### C. Pooling requires more than different seed numbers

The current rule assumes that:

- A fixed seed identifies a stable prefix.
- Larger runs preserve that prefix.
- Different streams can be pooled under the declared statistical assumptions.
- The law and conjunct remain the same.
- Continuation preserves one sequential experiment.

`stretches` and `continuation` do not themselves use the conjunct as an index. Some callers prefilter entries. That precondition needs to be part of their interface, especially before statistical conjuncts or additional pooling clients are introduced.

A seed is a replay coordinate. Independence is an additional property of the sampling protocol.

**Proposal:** identify a sample by a protocol/distribution identity plus stream and prefix coordinates. Pool compatible observations, with replay idempotence and prefix inclusion as laws. Preserve the logical obligation index throughout.

For sequential extensions, [Howard, Ramdas, McAuliffe and Sekhon’s confidence sequences](https://arxiv.org/abs/1810.08240) provide a reference for guarantees valid under continued observation. Their applicability would require explicit assumptions about Luthier’s observation process.

### 1.5 Across a run’s cone: serving needs one refusal rule and a complete witness

**L10.6 (a demand requires the certificates of its live cone)** and **spec 6.S14 (each reached name owes its certificates)** establish conjunction across dependencies.

**D-2026-10-22-a (a pass concerns its model; a control concerns the law)** correctly prevents a pass for model M from serving model N.

The current model-aware serving path introduces two problems.

#### A. The model-aware path bypasses failure and disagreement vetoes

At [`certify.py:1214`](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:1214), the `byModel` branch asks whether `served` succeeds and then continues. It skips the later general checks for current failures and disagreements.

`_served_by_conjuncts` searches for successful entries. It does not apply those vetoes itself.

A probe supplied a pass and a failure for the same model and conjunct, under different seeds:

| Demand path | Result |
|---|---|
| Direct demand on the theory | Refused for the current failure |
| `byModel` demand served through the theory’s conjuncts | Accepted |

The probe included a model binding, model fingerprint and a reach containing that model. This is a model-scoped example.

**Missing law:** changing the route by which a demand locates its evidence must preserve refusal for the same subject and obligation.

**Proposal:** resolve every demand to a canonical subject and obligation set first. Apply currentness, model compatibility, conflict, failure and cutoff checks once to that resolved set.

#### B. Acceptance and recording use different evidence selections

At [`run.py:2516`](/home/lmoffatt/Projects/luthier/src/luthier/run.py:2516), the nested `serving` function selects one entry for each law. Its `byModel` branch does not restrict selection to the requested conjunct heads.

Using two required conjuncts, `P M` and `Q M`, an in-memory execution of that function produced:

```text
demand P: served True; recorded certificate P M
demand Q: served True; recorded certificate P M
```

Acceptance required both conjuncts. The recorded certificate set could contain only the first.

For an ordinary conjunction, selecting one successful entry also cannot represent the complete witness that every conjunct was served.

This affects **L5.6 (result identity includes the certificates in its live cone)** and **spec 8.S8 (the result key includes the certificates that served it)**.

**Proposal:** serving should return an explicit witness:

\[
\operatorname{Served}(d,\{e_1,\ldots,e_k\}),
\]

covering every required obligation. Admission and result identity should consume this same witness.

**Blocks:** trustworthy run certification and complete provenance of cached results. These two defects are immediate core-closing issues.

### 1.6 Under model substitution: the boundary is clear, the transport algebra is partial

**Spec 6.S11 (transport intersects the source and identity domains, composes bounds and evidence, and weakens the grade)** gives a schematic composition. **Spec 6.S12 (sampled paths compose only under related distributions)** limits it.

`certification.lth` already contains Boolean standings, links, reach intersection and path composition. The Python runner does not yet implement the general numerical substitution planner.

The remaining algebra needs to establish:

- Which law of A follows from which law of B.
- The direction of transport.
- Parameter and hypothesis substitution.
- Domain pullback when the input representation changes.
- Preservation by the operations using the substituted value.
- Distribution transport.
- Error, evidence and resource composition.
- Identity and associativity of transport.

Intersection is sufficient when both certificates use the same coordinates. A bridge \(f:A\to B\) requires a preimage such as \(f^{-1}(D_B)\), together with the bridge’s own validity domain.

**Concrete scenario:** agreement between two models on a grid is transported to an arbitrary consumer whose actual input lies outside the grid, or whose operation does not preserve that agreement.

**Proposal:** use indexed certificates with explicit reindexing along model and representation maps. Certified transformations should carry their preservation obligations. The enriched-category perspective in [Lawvere’s metric-space paper](https://raw.githubusercontent.com/mattearnshaw/lawvere/master/pdfs/1973-metric-spaces-generalized-logic-closed-categories.pdf) fits quantitative composition; Luthier must still define the indexing and transport data.

### 1.7 Controls form a separate algebra of discrimination

**L9.14 (each law needs a deliberately broken model that it refutes)** and **spec 7.S19 (controls reveal whether a law can detect wrong models)** give their meaning.

D-2026-10-22-a settles an important point: a control establishes something about the law’s discrimination. A new valid model does not need its own copy of that control.

Current code respects this separation in several places:

- `is_control` and `_laws_own` keep controls outside successful grades.
- `control_status` indexes status by law and current law-cone hash.
- A confirmed broken model reports control failure.
- A refuted broken model reports that the law is controlled.
- The conjunction tester stops a control after one conjunct is refuted.
- Recent code reads controls from the store of the file stating the law.

The unresolved operations are:

1. **Coverage of faults.** One detected defect witnesses some discrimination. It does not establish detection of all intended faults.
2. **Composite laws.** Decide whether control adequacy is required per conjunction, per constituent obligation, or per declared fault family.
3. **Statistical aggregation.** Define aggregation of detection rates, intervals and repeated controls.
4. **Admission policy.** The current command rejects failed controls but can succeed with uncontrolled laws. That is an advisory policy consistent with reporting missing controls; it differs from declaring a theory complete.
5. **Transport.** Transferring a control across an equivalent reformulation needs preservation of the tested fault and rejection judgment.

**Proposal:** keep two judgments:

\[
\operatorname{PassEvidence}(T,M)
\quad\text{and}\quad
\operatorname{DiscriminationEvidence}(T,F),
\]

where \(F\) names a fault family or control obligation. A finite fault-coverage relation can aggregate discrimination obligations without tying them to each production model.

**Blocks:** a precise completion criterion for theories and interpretable statistical power.

### 1.8 Certificate construction needs a specified trust boundary

**L10.10 (certificate construction should be abstract, following the LCF discipline)** motivates a protected carrier. The current store theory already states stronger requirements than its reader enforces.

`certification.lth` defines `heldAsRun`, including compatibility between evidence, grade and listed reach. At [`certify.py:520`](/home/lmoffatt/Projects/luthier/src/luthier/certify.py:520), `store_errors` checks required identity fields, pass/grade correspondence and a statistical special case.

A synthetic row containing drawn `Points` evidence and grade `Proved` returned:

```text
store_errors = []
```

No file was read or written for this probe.

**Concrete scenario:** a buggy certifier or migrated store emits an inconsistent grade. The reader accepts the row and serving subsequently trusts its rank.

**Missing laws:** admissible constructors for each evidence form, schema-version migration, validation at deserialization, and a declared boundary between a trusted writer and a checked certificate.

**Proposal:** make deserialization a checked construction of the indexed evidence type. Proof, exhaustive, sampled, assumed and control evidence should have distinct constructor obligations. This follows the abstract-theorem discipline described in [Gordon, Milner and Wadsworth’s LCF metalanguage paper](https://doi.org/10.1145/512760.512773).

# II. Further implicit policies affecting current runs

## 2. Demand is a record, but its policy algebra and record are incomplete

**L5.17 (the cutoff belongs to the demand and does not compose)** fixes ownership. **L5.18 (criteria are explicit parameters and are recorded)** fixes provenance. **Spec 8.S1 (demand selects the result type, decoration, tolerances, evidence and resource constraints)** gives the intended carrier.

`demand.lth` and `run.Demand` already define passing the demand inward, deriving law demands and recording the run. Two effective policy fields remain outside that declared record.

At [`run.py:1955`](/home/lmoffatt/Projects/luthier/src/luthier/run.py:1955):

```python
AXIOMS = "AssumedGrade"
```

`Demand.cutoff` can lower an axiom’s effective cutoff to this grade. The comment explicitly says the policy is absent from `demand.lth`, `demand_model.lut` and the declared defaults.

`Demand.combine` similarly affects aggregation while being omitted from `Demand.record`.

This matters because **spec 6.S10 (assumptions have a demand-supplied price with no default)** otherwise refuses an unpriced assumption.

The host-root use case is real. Its exception needs an explicit representation. A run’s record should expose why a stricter outer cutoff still admitted an observer axiom.

**Missing operations and laws**

- Equality of effective demands.
- A refinement order: which demands are stronger.
- Compatibility and combination of independently requested constraints.
- Preservation under `inner`.
- Recorded defaults and exceptions.
- A distinction between global acceptance criteria and locally derived numerical allowances.
- The fields that affect result identity, evidence identity or only execution limits.

**Proposal:** define demand as a product of typed policies with a satisfaction relation. Conflicting requirements should produce explicit incompatibility. Keep the original demand fixed while deriving local obligations from it.

For example, pulling an output tolerance backward through sensitivity derives an input obligation. It does not replace the demander’s output criterion.

**Blocks:** faithful reproduction of admission decisions and later automatic tolerance allocation.

## 3. Result identity needs completeness, equivalence and hashing to be separate

**Spec 8.S9 (reuse currently requires an equal key)** supplies a conservative rule. `result_key`, `served_by` and `store_result` implement it for pure results, including refusal when stored values disagree.

This is a useful existing algebra. Its remaining gaps are specific.

### 3.1 The key must include the complete serving witness

The omission in section 1.5 means the intended certificate field can be incomplete. Correcting its selection is necessary before treating the key as the identity of a derivation.

### 3.2 Execution identity has a documented temporary approximation

`certify.interpreter_revision` uses the last reachable tag. **D-2026-10-15-i (interpreter identity changes by development stage)** documents that policy.

`host_hash` commonly identifies installed libraries by package version. These identifiers do not by themselves describe every runtime, build, platform, thread-count or scheduling distinction contemplated by **L5.7 (host scheduling can change numerical bits)**.

This is a documented limitation, rather than an entirely unrecorded choice. It prevents a stronger claim that every behavior-changing execution input is already represented.

### 3.3 Chosen plan and executed schedule are distinct

`chosen_plan` deliberately removes the schedule before hashing. `plan.lth` states the same proposal: call-by-need discovers its schedule during execution, and the rest of the key should determine it.

The missing requirement is a precise determinacy or confluence theorem under the permitted execution model. Arbitrary host nondeterminism cannot inherit it from the pure dataflow model.

### 3.4 Hash laws overclaim mathematical injectivity

`plan.lth`’s `KeySeesThe…` and `PlanHashSeesTheSchedule` laws demand distinct hashes when their unbounded inputs differ.

A finite SHA-256 codomain cannot be injective on an unbounded key or schedule space. Finite tests can provide collision evidence; they cannot certify this universal injectivity claim.

`served_by` usefully checks the full key as well as its hash. That is a sounder basis for lookup semantics.

### 3.5 Exact cache identity does not provide semantic quotient identity

Different procedures can produce the same value or satisfy the same observations. The existing key distinguishes their code and realization.

**Proposal:** specify separately:

1. **Execution key:** the inputs identifying a reproducible realization.
2. **Lookup digest:** a finite index, with full-key comparison and collision handling.
3. **Certified equivalence:** evidence allowing transport or reuse between distinct keys.

A content-addressed record is a useful implementation of the first two. The third needs the certified transformation algebra of section 1.6.

**Blocks:** complete provenance now; semantic reuse and derivation quotients later.

# III. Algebras needed for numerical composition and the planner

## 4. Error, uncertainty, evidence and resources share interfaces, not one completed model

**D-2026-10-18-i (error, uncertainty, evidence and resources are four different roles)** is the correct starting distinction:

| Role | Intended values | Meaning |
|---|---|---|
| Error | Bounds, intervals, balls or related decorations | Deviation of a result from a reference. |
| Uncertainty | Distributions or distributional approximations | Variation in the quantity being computed. |
| Evidence | Statistical bounds and confidence, plus other evidence forms | What finite verification supports about a law. |
| Resources | Work, samples, memory, precision, time | What a realization consumes or requires. |

[`core/structures/algebraic.lth:61`](/home/lmoffatt/Projects/luthier/src/luthier/lib/core/structures/algebraic.lth:61) already declares `Quantale`, including preservation of arbitrary joins and the empty join. Its comments explicitly refrain from claiming that all four proposed bases are implemented models.

The declaration is not the gap. The concrete models and the maps between their uses are missing.

### 4.1 Order orientation must be explicit at each interface

The correction to D-2026-10-18-i is mathematically necessary:

\[
([0,\infty],+,\ge)
\]

has empty join \(\infty\), with \(a+\infty=\infty\). Ordinary numerical order with empty supremum \(0\) fails empty-join preservation.

However, admission still normally asks whether a numerical error is **at most** the demanded bound.

Luthier therefore needs an explicit relationship between:

- The quantale’s categorical order.
- The numerical order used to compare error bounds.
- The direction of certificate refinement.
- The direction of demand strengthening.

Reusing one `leq` convention silently across all four would reverse some decisions.

### 4.2 Evidence needs its own tensor

**L10.3 (sample statistics are converted to an evidence cost)** and **spec 7.S11 (the proposed conversion is \(-\log(1-\widehat\epsilon)\))** give an interface, not a complete composition law.

Under a union bound:

\[
\epsilon_{\mathrm{path}}\le
\min(1,\epsilon_1+\epsilon_2),
\qquad
\delta_{\mathrm{path}}\le
\min(1,\delta_1+\delta_2).
\]

Ordinary addition of the corresponding negative logarithms encodes multiplication of success bounds. It is not automatically the union-bound operation.

For example, two failure bounds of \(0.1\) give a conservative combined failure bound of \(0.2\). Adding \(-\log(0.9)\) twice corresponds to success \(0.81\), which requires an additional dependence argument.

Nested events can justify `max` in some cases. Independence can justify multiplication. Those hypotheses belong in the operation’s domain.

There is also a type distinction to preserve:

- Confidence failure probability, written \(\delta\) in evidence bounds.
- Alternative separation, also written `delta` in sequential testing.

They have different meanings and units.

### 4.3 Uncertainty needs joint information

Marginal distributions do not determine the distribution of a sum, product or general function of two quantities. Convolution requires assumptions such as independence; correlated inputs require a joint distribution or a conservative dependence model.

A t-norm, a Menger triangle operation, convolution and a general pushforward serve different purposes. Naming them as candidates does not make them interchangeable.

### 4.4 Resources require several composition operations

Sequential latency adds; ideal parallel latency takes a maximum. Work can add in both cases. Peak memory depends on overlap and lifetime.

Calling these the tropical semiring leaves carrier and identity choices unresolved. For example, `max` with neutral \(0\) on nonnegative numbers and ordinary `+` does not satisfy the absorbing-zero requirement of a semiring.

### 4.5 The Boolean and quantitative readings still need reconciliation

**G2 (laws are valued in cost)** and **spec 5.S2 (future laws may return a degree in C)** coexist with D-2026-10-18-i’s account of Boolean laws about quantitatively computed data.

Both interfaces can be supported. Their relationship needs specification:

- Is a quantitative observation primary, with a Boolean threshold projection?
- Is it a separate decorated computation checked by a law?
- What evidence links the observation, its bound and the Boolean verdict?

### 4.6 The proposed average conjunctions need arity information

O1 names candidates involving normalized sums and log-sum-exp. Binary averaging is not associative:

\[
\operatorname{mean}(\operatorname{mean}(0,2),4)=2.5,
\]
\[
\operatorname{mean}(0,\operatorname{mean}(2,4))=1.5.
\]

An aggregate carrying count or weight can compose associatively. A scalar normalized mean alone cannot provide that law.

**Proposal:** first implement distinct typed models with explicit operations, units, orders and boundary cases. Connect them by declared monotone maps. Use a quantale only where the complete model satisfies its laws.

Lawvere supplies the reference for metric enrichment and its order orientation. He does not supply Luthier’s four concrete models or their cross-role conversions.

**Blocks:** quantitative certificate composition, sound planner ranking and error decorations. These are deliberately deferred by **O1 (the concrete cost algebras remain library work)**.

## 5. Tolerance propagation needs compositional bound transformers

**L6.8 (substitution requires sensitivity to pull tolerances backward)** and **D-2026-10-18-j (numerical laws separate algorithmic stability from input sensitivity)** define the intended form:

\[
\epsilon_{\mathrm{out}}
\le L\,\delta_{\mathrm{in}}+\eta,
\]

where \(\eta\) is the algorithm’s own error, valid on a stated domain and perturbation radius.

There is meaningful implementation progress:

- `functions.lth` defines `NonExpansive`, `Lipschitz` and map structures.
- `numbers.lth` uses argument-dependent rounding bounds.
- `arrays.lth` defines `gammaN`, moderate-input predicates and summation ranges.
- `DotAgrees`, `MatVecAgrees`, `MatMulAgrees` and related laws use theoretical bounds rather than a freely selected flat tolerance.

The remaining gap is their composition through an actual program.

### Missing carrier and operations

A bound transformer needs at least:

- Its input and output metric levels.
- Its validity domain.
- Its admissible perturbation radius.
- A sensitivity map, possibly dependent on the input.
- Its own numerical defect.
- Its evidence.

For affine transformers,

\[
B_f(\delta)=L_f\delta+\eta_f,
\]

composition should yield:

\[
B_{g\circ f}(\delta)
=
L_gL_f\delta+L_g\eta_f+\eta_g,
\]

on a domain where both bounds apply.

This immediately shows why adding local errors without sensitivity is insufficient.

For multi-input functions, Luthier must also choose the product metric and account for reused or correlated inputs. Backward allocation can have several solutions; the planner’s resource policy must select among them.

### Boundary cases

The algebra must define:

- \(L=0\), unknown or infinite sensitivity.
- A requested tolerance below the algorithmic error floor.
- An input radius crossing a rank threshold or singularity.
- Empty validity domains.
- Bounds that overflow or are rounded downward.
- Ratio recording when residual and bound are both zero.
- Positive residual with zero bound.
- Failure of the premises required to evaluate the bound.

D-2026-10-18-j also asks certificates to record the largest observed error-to-bound ratio. The tester’s current general evidence records counts and verdicts; it does not provide a general numerical observation interface for that ratio.

**Concrete scenario:** two individually accepted approximations are composed through an ill-conditioned inverse. Their local tolerances pass, while the demanded output tolerance is exceeded.

**Proposal:** use domain-indexed monotone error transformers, with affine sensitivity/defect pairs as the first concrete model. Require composition and validity preservation laws. [Reed and Pierce’s sensitivity types](https://www.cis.upenn.edu/~bcpierce/papers/dp.pdf) provide a precedent for tracking how functions amplify distances.

**Blocks:** numerical model substitution and backward planning from an output tolerance.

## 6. Budget scaling needs a modulus with a domain and an infeasible case

**L9.17 (an algorithm should state how budget scales with the demanded bound)** and **D-2026-10-18-d (the resource law is a modulus depending on tolerance and problem features)** name the concept.

Today, `Budgets`, test parameters and execution limits provide concrete counters. They do not yet provide a general certified function predicting sufficient resources.

The intended carrier is approximately:

\[
M(\epsilon,\delta,n,\kappa,u,\ldots)
\to \operatorname{ResourceBound}.
\]

A total finite result is inappropriate. Some requests are infeasible, outside the convergence domain, or unsupported by current evidence.

### Missing laws

- Stronger accuracy or confidence demands cannot require less certified budget without an explicit reason.
- Sequential composition combines resources according to resource kind.
- Parallel composition distinguishes work, span and memory.
- A modulus states its convergence domain and numerical floor.
- Measured resource use is distinguished from a sufficient bound and from an extrapolated estimate.
- Predicted resource bounds carry their own evidence and platform scope.
- Exhausting a budget inside a promised convergence domain is distinguished from an unresolved exploratory run.

For no-failure independent sampling, the familiar sufficient count has the form:

\[
n\ge
\frac{\log\delta}{\log(1-\epsilon)},
\]

with appropriate rounding and nontrivial ranges. The boundaries \(\epsilon=0\), \(\delta=0\) and an unattainable numerical tolerance need explicit results.

The current “budget” record mixes sampling policy, classification policy and execution limits, as section 1.4 showed.

**Concrete scenario:** the planner extrapolates a convergence rate beyond its validity domain and predicts that additional iterations can achieve a tolerance below the rounding floor.

**Proposal:** define a partial or extended-valued modulus, returning a bound, an infeasibility reason or insufficient knowledge. Keep resource vectors typed. For parallel resource composition, [Blumofe and Leiserson’s separation of work and critical-path length](https://www.cs.cornell.edu/courses/cs612/2006sp/papers/blumofe94.pdf) is a useful concrete reference.

**Blocks:** informed planner estimates and interpretation of scaling experiments.

## 7. Specimens and planner identities need a domain-indexed transformation graph

**L6.5 (closeness forms a graph rather than an equivalence quotient)** and **spec 9.S5 (the planner uses certified identity edges between specimens)** give the carrier.

**Spec 9.S11 (substitution requires sensitivity)** and **spec 9.S14 (ranking is monotone and its comparison a total preorder)** constrain selection. **Spec 9.S17 (the substitution planner remains unwritten)** accurately separates this work from `plan.lth`, which concerns scheduling.

### What is missing

An edge needs:

- Source and target specimens.
- The theories and laws it preserves.
- Input and hypothesis maps.
- Validity domain.
- Error and evidence transformers.
- Resource estimates.
- Direction and, where available, an inverse.
- A certificate for those properties.

Path composition then needs associativity, identity paths, domain propagation and compatible distribution transport.

The correction to **D-2026-10-18-c (metric thresholds generally give tolerances rather than equivalences)** is decisive here. With points \(0\), \(0.75\) and \(1.5\), adjacent distances are within \(1\); the endpoints are not.

A connected component can organize candidates. It cannot license every substitution at the same tolerance.

### Ranking remains a separate policy

**Spec 9.S15 (cost plus \(w\log(\text{resources})\) is a candidate ranking)** still needs:

- Positive, dimensionless resource normalization for the logarithm.
- Treatment of zero and unknown resources.
- Multiple resource dimensions.
- Ties and deterministic choice.
- Uncertainty in measured estimates.
- A feasibility test before ranking.
- A policy for a cheaper specimen with weaker evidence.

**Concrete scenario:** connectedness is treated as interchangeable membership, or a ranking formula chooses a fast candidate whose path no longer meets the demand after accumulated error.

**Proposal:** use a category of typed, domain-restricted certified transformations, enriched by the selected quantitative model. Keep exact invertible transformations distinct from approximate directed edges. A demand first filters feasible paths and then applies its declared ranking policy.

This is an application of Lawvere’s composition perspective, with substantial Luthier-specific structure still to define.

**Blocks:** automatic model substitution. This is the main content still missing in **O4 (composition of invariances and demand selection)**.

## 8. Decorated outputs need an interpretation and preservation contract

**L5.4 (a decoration computes another model of the theory)** names derivatives, intervals and value/error pairs. **Spec 8.S2 (decorations provide functor and applicative operations and laws)** gives generic plumbing.

`demand.lth` declares `Decoration` and `decorate` as holes. `run.Demand.decoration` is currently `None`. There is no implemented general elaboration that lifts an arbitrary cone into a selected decoration.

### Missing operations

- Selecting or constructing the decorated model.
- Lifting constants, inputs and primitive operations.
- Interpreting application and branching.
- Inserting representation bridges.
- Projecting the underlying value and requested summaries.
- Combining decorations in a declared order.
- Transporting model certificates to the lifted interpretation.

Functor and applicative laws alone do not establish numerical adequacy.

Examples illustrate the additional obligations:

- Intervals require inclusion-preserving operations and controlled rounding.
- Dual numbers require differentiable operation interpretations and branch/domain rules.
- Distribution decorations require pushforwards and joint dependence.
- Certificate decorations require the complete evidence witness.
- Derivation decorations require the ancestry and projection rules discussed below.

Some decorations model a smaller theory than the original carrier. Dual numbers have nonzero nilpotents and do not inherit a field structure unchanged. Interval operations likewise do not automatically satisfy the exact laws of real arithmetic.

**Concrete scenario:** the planner chooses an interval or dual-number carrier and transfers a certificate whose algebraic laws fail on that carrier.

**Proposal:** define a decorated interpretation of a stated source theory, with preservation laws for exactly the operations it supports. Applicative functors are suitable for combining independent decorated inputs; [McBride and Paterson’s applicative interface](https://personal.cis.strath.ac.uk/conor.mcbride/IdiomLite.pdf) supplies that reference. Each numerical interpretation still needs its own adequacy laws.

**Blocks:** executable error, derivative, uncertainty and certificate outputs. This is intentional work under **O5 (decorated models and their bridges remain open)**.

## 9. The three planes need maps between levels, not just declarations at each level

**L3.5 (the core separates objects, levels of comparison and computable models)** and **D-2026-10-18-c (these form three planes, with a potentially infinite tower explored by demand)** define the architecture.

Current files already represent important parts:

- `Object` states equivalence.
- Metric, pseudometric, quasimetric and ultrametric theories are distinct.
- `ToleranceRelation` avoids claiming metric thresholds are transitive.
- `MetricWithin` expresses a bounded numerical realization.
- Probabilistic metric declarations state additional distribution laws.
- `Structural` gives the stronger substitutivity obligation for structural equality.
- `Pointwise` compares function outputs without pretending to decide equality of arbitrary functions.

The remaining algebra concerns movement between these structures.

### Missing maps and laws

- How a Boolean comparison embeds into a metric or probabilistic level.
- Which level refinements preserve which observations.
- How metrics are rescaled or pulled back.
- How a demand selects and parameterizes a level.
- How computable approximations realize an abstract distance.
- How certificates move between levels.
- How pointwise evidence becomes evidence about an operation over a domain.

Thresholding an arbitrary metric is not an equivalence-preserving map. A finite sample of function applications is not a decision procedure for extensional equality.

### Current code boundaries

`kernel.alpha_equal` and canonical hashing implement strict syntactic comparisons. `check.Typing.same` uses bounded reduction and permits unknowns. `elaborate.fits` and `refines` implement a practical compatibility judgment, including variance and subtype rules.

These are different relations. Their connection to semantic equality, verified membership and quantitative comparison needs an explicit contract.

The recent `sibling_subtype` guard is a concrete improvement: it prevents a claim for one subtype from serving an unrelated sibling. That issue should not be reported as wholly unresolved.

**Concrete scenario:** an elaboration compatibility result or a sampled pointwise comparison is used as authorization for semantic substitution.

**Proposal:** organize the planes as indexed theories and interpretations, with explicit morphisms stating preservation. Restrict enriched functor claims to the appropriate sensitivity conditions. Lawvere provides the comparison structure; the implementation still needs the realization relation and its evidence.

**Blocks:** sound bridges between Boolean certification, numerical comparison and the future probabilistic level.

# IV. Intentionally open architecture that now needs a precise algebraic question

## 10. Derivation has acquired a categorical interpretation; its quotient and projections remain open

The audit includes the new record.

**L5.22 (a derivation records the semantically relevant realization of a value)**, **L5.23 (the demand selects its carried projection)** and **L10.13 (model certificates, computation evidence and the value’s derivation remain distinct records)** introduce the commitment.

**D-2026-10-22-b (these clauses enter the principles as proposals)** preserves their status. **D-2026-10-22-c (a derivation is the realization viewed through an intensional exponential)** settles the adopted reading and the word.

The current question is therefore more specific than “what is history?”

### What is now defined conceptually

For evaluation

\[
\operatorname{ev}:B^A\times A\to B,
\]

a realized computation producing \(v\) can be represented by a procedure/input pair \((f,a)\) with:

\[
\operatorname{ev}(f,a)=v.
\]

The decision places it in the fibre over \(v\), with procedure composition composing derivations. It also preserves the distinction between procedures that compute the same extensional function while differing in resources, approximation or evidence.

### 10.1 “Intensional exponential” still requires a model

The record proposes programs as arrows and certified identities as 2-cells. That names a direction. It does not yet construct the category, its composition, its equality or its closure.

An ordinary exponential has an evaluation map and a universal currying property. The selected intensional setting must state the corresponding laws and which operational distinctions survive them.

Approximate certified transformations also need care: their error accumulates, their domains can shrink, and they need not be invertible.

**Proposal:** begin with typed procedures and composable realizations. Add graded transformations between procedures. Claim an intensional closed or higher-categorical structure only when its evaluation, composition and currying laws are specified. [Awodey’s definition of exponentials and evaluation](https://awodey.github.io/typetheory/notes/typetheory2.pdf) is a precise reference for the obligation.

### 10.2 The present key is not yet the quotient’s identity

L5.22 calls the existing result key the identity of the derivation. It also describes derivations modulo equality of consequence.

The current key distinguishes code, specimens and certificates. Two computations can have different keys while satisfying all the observations a demand permits.

The key can identify a concrete realization record. A further equivalence relation is needed to identify its observational class.

**Concrete scenario:** `(a + b) * 1.0` and `a + b` receive different execution keys, while an exact theory permits the same relevant observations. The semantic quotient cannot simply be the existing digest.

### 10.3 The quotient must be a congruence for the permitted contexts

Let \(h_1\sim_d h_2\) mean that demand \(d\) cannot distinguish their relevant derivations.

Required laws include:

- Reflexivity, symmetry and transitivity.
- Preservation under the permitted compositions.
- A relationship between equivalence at stronger and weaker demands.
- Explicit observations included in the relation.
- A decision procedure, a certified sufficient relation, or an acknowledged undecidable boundary.

An epsilon-closeness relation generally cannot supply this quotient, because it need not be transitive.

### 10.4 Projection must preserve the facts later demands rely on

For a derivation \(h\), a projection \(\pi_d(h)\) needs laws relating it to the retained ancestry.

At minimum:

- Its assertions follow from the represented realization.
- It cannot erase an assumption while continuing to claim absence of assumptions.
- It can name the certificates and bridges on which its assertions depend.
- Projection to a weaker demand agrees with projecting a sufficient stronger summary.
- An unavailable fact is reported as unknown.
- Discarding ancestry requires a certified sufficient summary or an explicit loss declaration.

The current record does not establish whether the same underlying retained graph must answer every later demand, or whether some projections may irreversibly lose capabilities.

### 10.5 A useful first model can be smaller than the final quotient

**Proposal:** use an immutable typed realization DAG, with separate identities for nodes, evidence and projected summaries. Define a small set of certified projections before attempting a canonical observational quotient.

[W3C PROV-DM](https://www.w3.org/TR/prov-dm/) provides a reference for entities, activities and derivation relations. It does not supply Luthier’s certified quotient. [Green, Karvounarakis and Tannen’s provenance semirings](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf) offer compositional annotations for positive relational computations; extending that model to ordered effects, negation or numerical approximation requires additional structure.

**Blocks:** history-sensitive demanded subtypes and derivation-preserving interoperability. These are the explicit remaining questions in **O13 (representation, quotient, summaries and bridge preservation)**.

## 11. Language crossings and world observations need preservation and feedback algebras

**L11.5 (a bridge has a joint theory for its two representations)** establishes the existing boundary. **L11.9 (roots of trust are declared and feedback limits what an action can establish)** describes observation. The new **L11.10 (a bridge declares what it preserves, adds, assumes and loses)** and **L11.11 (orchestration composes those facts across hosts)** extend that boundary to derivations.

`W`, first-action validation, callbacks and host conversion already exist. **D-2026-10-16-n (feedback depends on the kind of output place)** deliberately leaves the later grading of those observations open.

### Missing carrier and operations

A bridge needs a contract containing:

- Source and target representations.
- Value relation.
- Validity domain.
- Error or uncertainty transformer.
- Evidence and trust requirements.
- Resource contribution.
- Derivation-preservation and loss declarations.

Bridge composition must compose each of these fields with its own operation.

Action evidence additionally needs:

- The observation before and after.
- The place and feedback mechanism.
- Its scope in time.
- Interference assumptions.
- What can safely be reused.
- What is merely recorded or trusted.

**Concrete scenarios**

- A file path is retained as though it were the immutable content previously checked.
- A terminal write succeeds, and the system treats that as evidence that a person observed the intended output.
- An opaque host function changes a computation’s relevant behavior without an adequate representation of its identity or assumptions.
- Two actions are reordered because their returned values agree, although their observations or effects differ.

**Proposal:** use typed simulation/preservation contracts for bridges and indexed state transitions for actions. Observation evidence should identify the state or content observed. Combine independent actions only under a certified independence relation.

The indexed interpretation approach in section 9 and the typed derivation relations of PROV provide useful components. They do not determine action credibility or feedback policy.

**Blocks:** strong cross-language preservation and safe reuse of action evidence. The world token itself is implemented; **O3 (world-store integration and any exceptional opt-out policy)** is only partly open.

## 12. Other open items should be narrowed to their remaining obligations

Several named concepts already have enough algebra that treating them as blank areas would obscure progress.

### Checks and explanatory failures

**Spec 5.S9 (one check explains its failures and poorer outputs are projections)** and **spec 5.S11 (independent checks accumulate, dependent checks stop at failure)** have concrete definitions in `checks.lth`:

- `Failures E = List E`.
- `both` concatenates failures.
- `either` succeeds when either check succeeds.
- `reason`, `first`, `holds` and `refine` are projections.
- `andThen` expresses dependent sequencing.

The free-monoid basis of failure accumulation is present.

The remaining issue is integration and proof strength. `refine` currently returns `Maybe T`, with a law standing for the stronger subtype requested by the specification. A statistical pass must also remain distinct from exact refinement.

**Proposal:** preserve this existing algebra and specify the typed refinement constructor and witness obligations. Applicative validation and dependent reason sequencing already provide the relevant structures.

### Vacuity, empty evidence and uncovered regions

**D-2026-10-16-m (a law whose premises never hold is not run)** is stronger than older wording in spec 7.S12.

`run_spec` evaluates generated Boolean cases and records successful Boolean verdicts. It has no general extraction and counting of implication premises. Classifier premises principally concern parameter refinements. An implication whose antecedent is always false can therefore remain successful evidence without the general vacuity judgment the decision requires.

A zero requested sample also needs an explicit rule. `TestSpec.cases` is a `Nat`; the execution path can construct empty points and proceed to its ordinary verdict logic.

Uncovered-region handling has a related boundary: an empty region caps a grade at sampled. That is a policy label, rather than a statistical bound on that region. Branch coverage is a named obligation whose general collection remains incomplete.

**Proposal:** define an outcome algebra distinguishing a vacuous proposition, an empty experiment, a successful observed case, an unresolved test and an uncovered obligation. Logical truth and admissible empirical evidence should have separate projections.

**Blocks:** meaningful no-evidence cases and the completeness of region-based certification.

### O2: equality attachment

**O2 (a type carries its equality and other structures)** is partly answered by `Object`, claims and resolution.

Remaining work concerns coherence of inherited and explicit structures, equality-sensitive elaboration, and propagation of the demand’s comparison parameters. A second equality on one carrier must remain an explicit conceptual choice.

A categorical interpretation of types with selected structure fits; it should preserve the current distinction between structural and observational equality.

### O6: units

**O6 (dimensions form a group and quantities a graded algebra)** is a well-motivated future model with no present core-closing obligation.

Missing operations include dimension normalization, unit conversion and compatibility with uncertainty and numerical bounds. It should remain deferred until its scientific slice needs it.

### O7: theory cycles

**O7 (the former question about theories as cycles)** is recorded as closed. It should not appear as an unresolved algebra.

### O8: session memoization

**O8 (session demands and memoization across items)** still needs rules for changing hole assignments, invalidating dependent results, retaining evidence and crossing from pure evaluation to actions.

**Proposal:** make a session an evolving demand environment over the explicit dependency graph, with typed invalidation and reuse. This is an instance of the demand and result-key algebras above.

### O9: holes

**O9 (the kind of a hole in elaborated form)** remains an interface issue with algebraic consequences.

Unknown inference information, an unfilled program parameter and an unimplemented semantic operation have different substitution and failure behavior. Current compatibility functions often allow unknowns to agree.

**Proposal:** distinguish those cases in the elaborated carrier and specify which substitutions discharge them. An inference unknown must not silently become evidence of a semantic obligation.

### O10: citation

**O10 (citation syntax and who checked a cited guarantee)** is primarily an interface and trust-policy question. Its algebraic remainder is hypothesis instantiation, version/platform scope and transport of the cited conclusion.

A `Proved` label should retain those qualifications.

### O11: kernel theory

**O11 (the kernel’s own theory and executable models)** refers partly to older paths. Current `term.lth`, core properties and Python kernel code answer substantial portions of it.

One live implementation boundary remains visible: `term_model.lut` declares `textParts`, `textJoin` and `natDecimal` as holes. The execution plan explicitly preserves the decision about string primitives.

These holes limit execution of the Luthier reference model’s naming and canonicalization paths. They should not be replaced with invented string semantics during an algebra audit.

### O12: memo identity

**O12 (the identity of a memoized result)** now has `DemandKey`, `MemoKey`, `keyOf`, hashing and result-store operations.

Its remaining questions are those identified in section 3: complete serving evidence, execution identity, collision semantics and the distinction between exact keys and certified equivalence.

# V. Recommended sequence and verification record

The current milestone should first establish consistency of the Boolean machinery. The following order follows the dependencies found here:

1. Unify model-aware and direct refusal over the same resolved obligations.
2. Make serving return the complete evidence witness and use it in result identity.
3. Preserve current refutations through retention.
4. Put distribution-changing parameters into sampling identity.
5. Align deserialization with the store predicate and record all effective demand policies.
6. Specify empty, vacuous, conflicting and uncovered evidence outcomes.
7. Introduce one concrete numerical bound-transformer model with validity domains.
8. Add resource moduli and a first decorated interpretation.
9. Build planner transport from those operations.
10. Develop derivation projections over complete realization records.

The in-memory probes established the following limited claims:

| Probe | Inputs | Observed result |
|---|---|---|
| Retention | Failure at seed 0; passes at seeds 1–4; one current binding | Failure removed; grade became sampled |
| Model-aware refusal | One model, one conjunct, current pass and failure | Direct path refused; `byModel` accepted |
| Serving witness | Required `P M` and `Q M`, both passed | Both demands selected `P M` for recording |
| Sampling identity | Same entry; `specialMass` changed | Identity unchanged |
| Store admissibility | Drawn points carrying grade proved | `store_errors` reported no error |

These are unit-level counterexamples to the inspected functions. They do not claim that every production program reaches each path, or that the full suite currently fails.

Autonomous decisions taken for this audit were to prioritize demonstrated serving and provenance defects, include the new derivation decisions as they entered the record, and distinguish implementation defects from deliberately deferred architecture. No language design was adopted and no repository artifact was changed.

# Final inventory

| Concept | Where defined | Missing algebra | Implemented implicitly? | Blocks | Proposed structure |
|---|---|---|---|---|---|
| Complete evidence judgment | L10.1–L10.4; spec 6.S7, 7.S10 | Compatibility, strengthening, restriction, trust and distribution indices | **Yes:** grade ranks, reach and fingerprints in `certify.py` | Meaningful evidence comparison | Indexed evidence poset with grade projection |
| Required conjuncts versus alternative checks | L12.5; spec 5.S8, 7.S22; D-2026-10-18-f | Distinct combination operations, empty cases, obligation manifest | **Yes:** strongest per binding, configurable folds, per-conjunct serving | Consistent summaries and admission | Products of obligations plus compatible alternative evidence |
| Persistent refutation | Spec 6.S8, 6.S15 | Retention preserving refusal and conflict | **Yes:** `prune`, `record`; current rule loses failures | Core certification correctness | Durable negative evidence with refusal-preserving compaction |
| Samples, seeds and distribution identity | Spec 7.S8–7.S13; D-2026-10-16-g | Protocol identity, prefix and pooling laws | **Yes:** `identity`, `stretches`, `continuation`, `drawing_revision` | Replay and statistical interpretation | Protocol-indexed streams and prefix unions |
| Cone admission | L10.6; spec 6.S14–6.S15; D-2026-10-22-a | One model-scoped refusal judgment | **Yes:** `served`, `_served_by_conjuncts`, `refuse`; inconsistent paths | Core-closing run correctness | Canonical subject/obligation resolution |
| Serving witness | L5.6; spec 8.S8 | Evidence covering every accepted obligation | **Yes:** `run.certification.serving`; selection incomplete | Result provenance and identity | Explicit proof/evidence witness DAG |
| Controls | L9.14; spec 7.S19; D-2026-10-22-a | Fault coverage, statistical aggregation, adequacy policy | **Yes:** `control_status`, conjunction controls | Theory completion and measured power | Law-indexed discrimination evidence |
| Certificate construction | L10.10; `certification.lth`’s `Store` | Checked constructors and schema migration | **Yes:** `store_errors` enforces only part of the predicate | Trustworthy store consumption | Abstract evidence type with validated deserialization |
| Demand | L5.17–L5.18; spec 8.S1; `demand.lth` | Refinement, compatibility, complete recording | **Yes:** `Demand`; `axioms` and `combine` incompletely recorded | Reproduction and local obligation derivation | Typed policy product with satisfaction |
| Result identity | L5.6–L5.7; spec 8.S8–8.S10; O12 | Complete execution identity, collision semantics, certified reuse | **Yes:** `result_key`, `chosen_plan`, `served_by` | Reliable caching and derivation identity | Full execution keys plus separate digests and equivalence |
| Four quantitative roles | D-2026-10-18-i and correction; O1 | Concrete carriers, tensors, joins, orders and conversions | **Partial:** `Quantale` theory exists; concrete models incomplete | Quantitative composition | Separate ordered monoids or quantales with declared maps |
| Numerical tolerance propagation | L6.8; D-2026-10-18-j | Bound composition, validity propagation, backward allocation, observations | **Partial:** Lipschitz theories and several theoretical numerical bounds | Numerical substitution | Domain-indexed error transformers |
| Resource scaling | L9.17; D-2026-10-18-d | Moduli, infeasibility, prediction evidence, work/span/memory composition | **Partial:** budgets and counters | Planner estimates | Partial resource moduli over typed vectors |
| Specimens and planner paths | L6.5; spec 9; O4 | Typed edges, composable domains, feasible path selection and ranking | **Limited:** Boolean transport reference; general planner absent | Automatic model substitution | Domain-indexed enriched transformation category |
| Decorated outputs | L5.4; spec 8.S2; O5 | Lifted interpretations, preservation and bridge insertion | **No general implementation:** decoration holes | Error, derivative and uncertainty outputs | Applicative interpretations with numerical adequacy laws |
| Three planes and level maps | L3.5; D-2026-10-18-c; core equality theories | Realization relation and preservation between levels | **Partial:** structures, pointwise laws and practical compatibility | Cross-level reasoning | Indexed theories and certified interpretations |
| Empty, vacuous and uncovered evidence | Spec 7.S12–7.S14; D-2026-10-16-m | Outcome distinctions and admission rules | **Yes:** current verdict and region policies leave gaps | Meaningful empirical certification | Separate logical, observational and coverage outcomes |
| Derivation | L5.22–L5.23; L10.13; D-2026-10-22-b, -c; O13 | Intensional model, congruence, projections and certified summaries | **Partial:** execution records and keys; no quotient or carried projection | History-sensitive types and interoperability | Typed realization DAG, graded transformations and certified projections |
| Bridges and feedback | L11.5, L11.9–L11.11; spec 10; O3 | Preservation, loss, trust, observation scope and composition | **Partial:** bridge and first-action checks | Strong cross-language guarantees | Typed preservation contracts and indexed state transitions |
| Checks and refinement | Spec 5.S9–5.S12; `checks.lth` | Typed witness integration and exact/statistical boundary | **Mostly explicit:** projections and compositions exist | Strong refinement results | Existing failure monoid, applicative validation and dependent witnesses |
| Session, holes and citations | O8–O10 | Invalidation, hole kinds, hypothesis instantiation | **Partial:** session, elaboration and citation mechanisms | Stable incremental demands and qualified trust | Demand environments, typed substitutions and indexed cited evidence |
| Kernel reference execution | O11; `term.lth`, `term_model.lut` | String-operation contracts and executable models | **Partial:** Python implementation; Luthier string holes remain | Complete executable self-specification | Existing term algebra with explicit string models |
| Units | O6 | Dimension normalization and conversion laws | **No general implementation** | No current core milestone | Dimension group and graded quantity algebra |


