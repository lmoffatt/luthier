Below, items 1–9 are as in the prompt. “none” means I found no instance in that file.

## `demand.lth`

1. **Laws that are wrong**  
   `RecordsEveryCutoff` equates the recorded value to a `Record` that omits `decoration`:  
   `m.recorded d h == { entry := d.entry, cone := h, parameters := d.sets, accept := d.accepts, delta := d.delta, fuel := d.fuel, checked := d.checked, lock := d.pinned }`.  
   If the demanded type/decoration is a parameter (8.S1/8.S8), the record does not carry it. Also `bound`, `evidence`, `assumed` are declared but have no laws.

2. **Laws that do not determine what they claim**  
   `Demanding` has no law for `C`, `bound`, `evidence`, `assumed`; a wrong model can set them arbitrarily.  
   `determined` claims same `Record` gives same result, but `Record` lacks `mode`, `seed`, `plan`, `certificates`, `decoration`; a wrong model can have two runs with the same `Record` and different `plan`/result.

3. **Roles (L2.7)**  
   none; no `data` constructors here.

4. **Models against their theories**  
   I found no break in `demand_model.lut` against `Demanding` as written.

5. **Against the specification**  
   `Demand` has no type-demanded field, only `decoration`:  
   `Demand = { entry : String, decoration : Maybe Decoration, accepts : Grade, ... }`.  
   8.S1 says the demand carries the type demanded. `Record` also lacks `decoration`/tolerance required by 8.S8/12.S18.

6. **Implication over a type**  
   `NoPriceRefusesAssumed` is stated over arbitrary `Entry` with the rare premise `e.grade == just AssumedGrade`; it should quantify over assumed entries.

7. **What you would change first**  
   Add the missing identity law tying `Record` to the key and include the type/tolerance, because otherwise `Run` does not identify a result.

8. **Cutoffs**  
   none obvious in the theory; fields are parameters. `AssumedGrade` is a grade name, not a cutoff constant.

9. **Identifying a result**  
   Missing law: `Run`/`Record` vs `MemoKey`. `Run = { record : Record, result : String }` and `determined` do not mention the key under which the result is kept.

## `demand_model.lut`

1. **Laws that are wrong**  
   none; it is a model, not a theory file.

2. **Laws that do not determine what they claim**  
   none beyond the underdetermination inherited from `demand.lth`.

3. **Roles (L2.7)**  
   none.

4. **Models against their theories**  
   No break found against `Demanding` as written.

5. **Against the specification**  
   `theDemand` accepts `Sampled` but sets `delta := nothing`:  
   `{ entry := entry, decoration := nothing, accepts := accepts, delta := nothing, ... }`.  
   8.S1 and D-2026-10-12-r require δ for sampled evidence.

6. **Implication over a type**  
   none.

7. **What you would change first**  
   Same as `demand.lth`: make the record/key identity explicit.

8. **Cutoffs**  
   `accepts <- Sampled`, `fuel <- 10000000`, and `delta := nothing` are hard-coded defaults. If defaults count as file constants under D-2026-10-14-c, these are exactly the kind of cutoff that should be demand-supplied; L5.19 may excuse the root defaults, but the values are still fixed here.

9. **Identifying a result**  
   `recorded` produces a `Record` with no `decoration`/type/tolerance; no key model is given. The missing identity law is the same as in `demand.lth`.

## `plan.lth`

1. **Laws that are wrong**  
   `placedBefore`/`LinearizesOn` do not enforce topological order:  
   `subset (readsOf ns n) (addNew placed rest)` allows a node’s reads to appear later in the schedule.  
   So `LinearizesOn` accepts `["d","b","c","a"]` even though `d` reads `b,c`. As a result `Confluent`/`PlanIsConfluent` is false for intended models.  
   `KeyReadsTheType` is tautological: `(demandKey dm live).decoration == dm.decoration`.

2. **Laws that do not determine what they claim**  
   `Dataflow` has no law that `step` depends only on the names listed in `reads`; a wrong model can lie in `reads`.  
   `KeyReadsTheType` does not force the type into the key. `DemandKey` omits tolerance/`accepts`.

3. **Roles (L2.7)**  
   `Strategy : U := data { ForwardOnDemand : Strategy ; CallByNeed : Strategy ; }` has no law stating the role of its constructors.

4. **Models against their theories**  
   `plan_model.lut` breaks `PlanIsConfluent` because of the `LinearizesOn` bug. See below.

5. **Against the specification**  
   `planOf` defaults to `CallByNeed`:  
   `(strategy : Strategy <- CallByNeed)`.  
   8.S3/8.S4 and D-2026-10-10-d say the default is forward on demand.  
   `MemoKey`/`DemandKey` omit the type demanded and tolerance required by 8.S8:  
   `DemandKey = { decoration : Maybe Decoration, values : List (String * Value) }`.

6. **Implication over a type**  
   `Confluent` is stated over arbitrary `s1 s2` with the premise `LinearizesOn ... s1 and LinearizesOn ... s2`; it should quantify over linearizing schedules (or a subtype of them).

7. **What you would change first**  
   Fix `placedBefore`: require `subset (readsOf ns n) placed`, not `addNew placed rest`. This is the root of the false `Confluent` law.

8. **Cutoffs**  
   none as a cutoff constant; the default `CallByNeed` is a strategy default, but it is the wrong default per spec.

9. **Identifying a result**  
   `MemoKey` is defined, but there is no law linking it to `Run`/`Record`, and no law that equal `MemoKey` implies equal result. `Keying` only says the hash changes when inputs change.

## `plan_model.lut`

1. **Laws that are wrong**  
   none; it is a model.

2. **Laws that do not determine what they claim**  
   `agree` tests only one pair; it is not a law for all schedules.

3. **Roles (L2.7)**  
   none.

4. **Models against their theories**  
   `planning : Planning Nat eqNat := { plan := plan Nat }` breaks `PlanIsConfluent`.  
   Take `example`, live `reaches example "d"`, `s1 = ["d","b","c","a"]`, `s2 = ["a","b","c","d"]`. Both satisfy `LinearizesOn` because of the bug, but `EquivalentOn` is false at `d`: `run s1 "d" = 0`, `run s2 "d" = 4`.

5. **Against the specification**  
   Same inherited issue as `plan.lth`: default strategy and key fields.

6. **Implication over a type**  
   none beyond `plan.lth`.

7. **What you would change first**  
   Same as `plan.lth`: fix `LinearizesOn`.

8. **Cutoffs**  
   none.

9. **Identifying a result**  
   No model for `Keying`; per 8.S10 the memo does not exist, but the missing identity law is still in `plan.lth`/`demand.lth`.

## `08-demand.md`

1. **Laws that are wrong**  
   none; not a Luthier file.

2. **Laws that do not determine what they claim**  
   none.

3. **Roles (L2.7)**  
   none.

4. **Models against their theories**  
   none.

5. **Against the specification**  
   It is the specification. Its 8.S3/8.S4 default forward on demand is violated by `plan.lth`; its 8.S8 key includes type demanded and tolerance, which `plan.lth`’s `DemandKey` omits.

6. **Implication over a type**  
   none.

7. **What you would change first**  
   none.

8. **Cutoffs**  
   none.

9. **Identifying a result**  
   It states the missing law: 8.S8 key and 12.S18 record. The files do not implement the link.

## Not sure

- Whether `gradeRank`’s order makes `admitsAssumptions` correct; `test.lth` is not in the material.
- Whether `LawDemand` is accepted as certification.lth’s `Demand` by structural typing.
- Whether `C : U` and undefined `bound`/`evidence`/`assumed` are legal holes or errors.
- Whether default arguments count as “constants in a file” under D-2026-10-14-c.
- Whether cyclic `Dataflow`s are in scope; if not, some `Confluent` counterexamples need acyclic cases.
- Exact fields of 12.S18 are not fully quoted, so the record/key completeness claim is based on 8.S8 and the given chapter excerpt.