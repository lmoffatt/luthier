The largest defect is in `plan.lth`: the current definition of `LinearizesOn` accepts schedules in which a node is evaluated **before** its dependencies. That alone makes the stated `Confluent` law false, and `plan_model.lut` consequently does not model `Planning` even on its own acyclic example. The second major defect is that the run record and memo key are two disconnected notions of result identity. B-prompt B-prompt

## `demand.lth`

1. **Laws that are wrong.**  
   `"two runs with one record have one result"` (`determined`) is too strong because `Record` omits several fields that 8.S8 says distinguish results: seed, plan, certificate hashes, and demanded type/decoration. Two stochastic runs can therefore have identical `Record`s and different legitimate results, yet `Runs` forbids them. B-prompt B-prompt

   `NoPriceRefusesAssumed` does not test the proposition its name states. `"admitsAssumptions d"` is derived solely from `accepts : Grade`; there is no assumption-price field in `Demand`. Thus `--accept assumed` admits an assumption without the evidence price which 6.S10/8.S1 says has **no default**. B-prompt B-prompt

2. **Laws that do not determine what they claim.**  
   `"RecordsEveryCutoff"` does not record every parameter of the demand. In particular, two demands differing only in `decoration` produce identical `Record`s. The law exactly determines `recorded`, but the structure it determines has already discarded information. B-prompt B-prompt

3. **Roles (L2.7).**  
   No `data` constructors are introduced here, so I find no L2.7 constructor-role violation.

4. **Models against their theories.**  
   Deferred to `demand_model.lut`; no model is declared here.

5. **Against the specification.**  
   8.S1 says the demand carries the **type demanded**, cutoff, confidence, and assumption cost. `Demand` has only a `decoration`, a grade `accepts`, and optional `delta`; it has no demanded type and no assumption-price parameter. `Record` then drops even the decoration. B-prompt B-prompt

6. **Implication over a type.**  
   `NoPriceRefusesAssumed` quantifies over every `Entry` and hides its useful domain behind  
   `"or not (e.grade == just AssumedGrade) or ..."`.  
   It should be a law over assumed entries—and, once represented, demands with no assumption price—not random entries of every grade. B-prompt

7. **What I would change first.**  
   Make the run record a lossless representation of the actual result identity—preferably by carrying the canonical result key or its hash—instead of independently choosing a partial set of demand fields.

8. **Cutoffs.**  
   `accepts` itself is a demand parameter, so it is not a forbidden constant. The defect is that the assumption cutoff is inferred from that grade instead of being independently supplied, although the cited decision says it has no default. B-prompt

9. **Identifying a result.**  
   A cross-law is missing:
   `recorded demand/cone` must correspond to the **same** `MemoKey` used to store the result. Current `Record` cannot satisfy such a law because seed, plan and certificate hashes do not occur in it.

---

## `demand_model.lut`

1. **Laws that are wrong.**  
   None are defined in this file.

2. **Laws that do not determine what they claim.**  
   The model exposes a concrete underdetermination:  
   `"accepts : Grade <- Sampled"` together with `"delta := nothing"` is accepted by `Demanding`. Thus the theory allows a sampled demand with no sampled-evidence level, despite the specification saying the demand carries δ. B-prompt

3. **Roles (L2.7).**  
   None; no `data` is introduced.

4. **The model against its theory.**  
   `lawDemand` and `recorded` satisfy `PassedDownNotRecomputed` and `RecordsEveryCutoff` literally. I cannot establish a direct failure of `NoPriceRefusesAssumed` or `LoweringLosesNothing` without the omitted `Certifying.serves` semantics.

5. **Against the specification.**  
   The root demand defaults to `Sampled` while recording `delta = nothing`; 8.S1 says confidence δ is carried for sampled evidence. It also cannot supply the required no-default assumption cost because `Demand` has no such field. B-prompt B-prompt

6. **Implication over a type.**  
   None introduced here.

7. **What I would change first.**  
   Do not provide a `Sampled` root demand without its required sampling level. Either make δ an argument when `Sampled` is selected or make the sampled demand a subtype whose constructor requires it.

8. **Cutoffs.**  
   `Sampled` and `fuel = 10000000` are declared defaults of parameters, so they are not hidden constants in the sense of P11. The problematic item is the **absence** of δ, not a hard-coded δ.

9. **Identifying a result.**  
   `recorded` merely instantiates the incomplete `Record`; consequently this model records no seed, plan hash or certificate hashes. B-prompt

---

## `plan.lth`

1. **Laws that are wrong.**  
   The central error is:

   `"subset (keep placed (readsOf ns n)) placed"`

   This is tautological: `keep placed ...` is by construction a subset of `placed`. The other conjunct merely requires dependencies to occur somewhere in `placed ++ rest`. Therefore `LinearizesOn` accepts a dependency **after** its consumer. B-prompt

   Concrete counterexample using the file's own `example`: the schedule

   `["d", "b", "c", "a"]`

   passes current `LinearizesOn`: `d` sees `b,c` later, and `b,c` see `a` later. But it computes `d = 0`, whereas `["a","b","c","d"]` computes `d = 4`. Thus `Confluent` is false. B-prompt B-prompt

   There is a second domain defect: `Planning` quantifies over arbitrary `Dataflow A`, but `Dataflow.step` is not constrained to depend only on the names in `Node.reads`, nor is the graph constrained to be acyclic. Hence `PlanIsConfluent` is in general unsatisfiable independently of `p`; indeed `p` is not used in that law. B-prompt B-prompt

2. **Laws that do not determine what they claim.**  
   `Keying` does not determine a collision-free result identity. Each `KeySees...` only checks a change in **one coordinate while the others remain fixed**. A hash such as an XOR-like combination can change after either individual coordinate change yet return to the original hash after two coordinates change. Thus two unequal `MemoKey`s may collide while every stated law passes. B-prompt

   `planHash` is even less determined: its only law observes `schedule`. A model may ignore `strategy`, `entry`, and `live` completely and still satisfy `PlanHashSeesTheSchedule`. B-prompt

3. **Roles (L2.7).**  
   `Strategy` has two constructors,

   `"ForwardOnDemand"` and `"CallByNeed"`,

   but no law states their distinct roles. `TheDefaultsAgree` says they agree; it does not say what makes one forward-on-demand and the other call-by-need. A model using exactly the same schedule algorithm for both can satisfy the strategy laws. This is precisely the L2.7 problem. B-prompt B-prompt

4. **The models against their theories.**  
   See `plan_model.lut`; it definitely breaks `Planning`.

5. **Against the specification.**  
   `planOf` defaults to `CallByNeed`:

   `"strategy : Strategy <- CallByNeed"`

   while 8.S3 settles **ForwardOnDemand** as the default. The comment itself acknowledges the contradiction. B-prompt B-prompt

   More importantly, `DemandKey` contains only `decoration` and live `--set` values. 8.S8 explicitly puts the tolerance/cutoff in result identity, but `accepts`/δ are absent from `DemandKey` and `MemoKey`. B-prompt B-prompt

6. **Implication over a type.**  
   This is the clearest occurrence in the bundle:

   `Confluent ... := not (LinearizesOn ... s1 and LinearizesOn ... s2) or EquivalentOn ...`

   Random schedules almost never linearize. The law should quantify over the subtype of schedules that linearize the chosen live graph. B-prompt

   Independently, `Planning` should quantify over a well-formed/acyclic dataflow subtype rather than every arbitrary `Dataflow`.

7. **What I would change first.**  
   Fix `LinearizesOn`. Until it actually means topological order, every confluence result downstream is unreliable.

8. **Cutoffs.**  
   No cutoff is hard-coded here. The problem is the opposite: the result key omits the cutoff/tolerance that 8.S8 says participates in identity.

9. **Identifying a result.**  
   Three laws/functions are missing:
   `memoKeyOf` constructing the canonical key from demand/cone/mode/seed/plan/certificates; full-key collision freedom/injectivity; and a law relating that key to `demand.lth.Record`. The six `withX` tests do not establish any of these.

---

## `plan_model.lut`

1. **Laws that are wrong.**  
   None are declared here.

2. **Laws that do not determine what they claim.**  
   The model illustrates that the theory has no semantic role for the strategy beyond choosing some schedule; nothing proves that `byNeed` actually has call-by-need's role or `forward` forward-on-demand's role.

3. **Roles (L2.7).**  
   No new `data`.

4. **The model against its theory.**  
   `planning` is **not** a model of `Planning Nat eqNat`.

   The simplest witness uses its own `example`. Current `LinearizesOn` accepts both the proper schedule and `["d","b","c","a"]`; they produce different values, so:

   `PlanIsConfluent Nat eqNat planning example "d" proper reverse`

   is false. Since `PlanIsConfluent` is one of the conjuncts defining `Planning`, `planning` fails its theory. B-prompt B-prompt

   There is also an independent cyclic witness. For `a -> b -> a`, `byNeed`'s bounded recursion returns `["a","b","a"]`: duplicate `a`, hence not a `LinearizesOn` schedule. `forward` leaves the cycle unplaced. Yet `Planning` currently quantifies over such a `Dataflow`. B-prompt

5. **Against the specification.**  
   The opening description calls call-by-need `"the default plan"` although 8.S3's settled default is forward-on-demand. The runtime may currently use call-by-need, but that is implementation status, not the decided default. B-prompt B-prompt

6. **Implication over a type.**  
   No new law here. Its cycle handling is evidence that the theory should instead restrict the domain to valid acyclic dataflows.

7. **What I would change first.**  
   After repairing `LinearizesOn`, make the model consume a certified well-formed/acyclic dataflow—or explicitly return failure on a cycle. Bounded recursion that emits a duplicate schedule is not a semantic treatment of cycles.

8. **Cutoffs.**  
   None.

9. **Identifying a result.**  
   The file deliberately supplies no `Keying` model. Consequently none of the result-identity machinery is tested by the reference model. Given how central 8.S8 is, that is a significant missing specimen. B-prompt

---

## `08-demand.md`

1. **Laws that are wrong / inconsistent.**  
   8.S2 says `"The core uses these operations, and no others"`, but its table has no operation for resource limits or hole values even though 8.S1 says a demand carries both. Either 8.S1 names things the core cannot access, or 8.S2's interface is incomplete. B-prompt

2. **Laws that do not determine what they claim.**  
   8.S8 says what identifies a result, and 12.S18 supplies a run record, but there is no stated equivalence between **the identity recorded by a run** and **the key used by the memo**. O12 explicitly remains open. Thus two nominally authoritative representations of identity coexist without a law connecting them. B-prompt B-prompt

3. **Roles (L2.7).**  
   Not applicable; this chapter defines no `data` constructors.

4. **Models against theories.**  
   Not applicable.

5. **Against the specification / cited decisions.**  
   The chapter is now stale relative to D-2026-10-14-c. 8.S1 and 8.S2 still specify a cutoff as bound/evidence costs in `C` and an assumption evidence cost, whereas the later current decision says: first make every tested law Boolean and expose cutoff parameters; `Distance`/`Evidence` come later. B-prompt B-prompt

   Its implementation-status statements are also stale: 8.S4/8.S11 say the memo key has not been written, while this bundle's `plan.lth` now contains `MemoKey` and `Keying`. B-prompt B-prompt

6. **Implication over a type.**  
   No executable law here, but 8.S11 should specify the intended domain directly: unequal complete result keys, not a collection of local “change one input” implications.

7. **What I would change first.**  
   Make **one canonical result identity** part of the specification: the memo stores it, the run record records it, and the hash certifies it. Then `demand.lth` and `plan.lth` cannot silently choose incompatible subsets.

8. **Cutoffs.**  
   No cutoff value is hard-coded. The problem is that §2 still uses the superseded cost-shaped version rather than the current Boolean-slice formulation.

9. **Identifying a result.**  
   The missing normative law should amount to:

   `same result identity ⇔ same canonical ResultKey`

   together with, for the certified hash model,

   `hash(k1) = hash(k2) ⇒ k1 = k2`.

   And `x.run.json` must carry that `ResultKey` or enough canonical information to reconstruct exactly the same one. 8.S11's current `"key ... changes when any input ... changes"` is not precise enough to force this. B-prompt

## Separate issue with the specification itself

8.S5's inference from purity to confluence needs two premises made explicit: the dependency graph must be **complete**—`reads` must contain every value that `step` can observe—and the live graph must admit a topological order. Purity alone does not establish order-independence if the graph lies about dependencies. `plan.lth` currently makes both assumptions implicit, which is why arbitrary `Dataflow` values refute `PlanIsConfluent`. B-prompt B-prompt

## Not sure

I cannot verify the orientation and complete semantics of `gradeRank`, `Certifying.serves`, or `ServesIsMonotoneInTheCutoff` because `test.lth` and `certification.lth` are explicitly outside this bundle. Therefore I have not asserted that `demand_model.lut` breaks those imported laws.

I also cannot verify whether an earlier layer already certifies every program dataflow as acyclic and proves that its `reads` relation is complete. Even if it does, the present `Planning` theory still quantifies over unrestricted `Dataflow A`, so the domain error in this file remains. B-prompt

Finally, I cannot tell from this bundle whether duplicate/reordered `--set` arguments and certificate lists are canonicalized elsewhere. If they are not, the use of raw `List` values in `DemandKey` and `MemoKey.certificates` creates additional identity instability.