**demand.lth**

1. **Laws that are wrong**: None found that are false of the intended model or unsatisfiable together. `NoPriceRefusesAssumed` and `LoweringLosesNothing` correctly invoke `Certifying.serves` and `ServesIsMonotoneInTheCutoff` on the passed-down `LawDemand`.

2. **Laws that do not determine what they claim**: `PassedDownNotRecomputed` only checks structural equality of the record; a model that recomputes `given` or `accepts` from the law’s own cone (instead of copying `d.sets`/`d.accepts`) would still pass if the values happen to match.  
   `RecordsEveryCutoff` likewise only checks field-by-field equality; a model that omits a field or invents one still passes if the concrete values coincide.

3. **Roles (L2.7)**: No `data` constructors appear; `Demand`, `LawDemand`, `Record`, `Run` are records. No role-law violation.

4. **The models against their theories**: (N/A – theory file.)

5. **Against the specification**:  
   - `Demand` carries `accepts : Grade` as the sole cutoff (line “accepts : Grade”), while 8.S1/8.S2 require a bound + evidence cost in `C` plus an `assumed` cost with no default. The file itself marks the `C` holes and cites D-2026-10-14-c / D-2026-10-13-m, so the Boolean simplification is intentional, but the chapter still lists the richer form.  
   - `delta : Maybe Float64` is present but never used in any law; 8.S1 requires it for sampled evidence.  
   - Entry is restricted to `String`; 8.S1 allows a term.

6. **Implication over a type**: None; all quantifications are over the concrete parameters of the laws.

7. **What you would change first**: Make `PassedDownNotRecomputed` and `RecordsEveryCutoff` quantify over the fields that must be copied rather than relying on whole-record equality, so a model cannot sneak in a recomputation that happens to produce the same values.

8. **Cutoffs**: No constant cutoffs; `accepts`, `delta`, `fuel`, etc. are fields of `Demand` supplied by the caller (consistent with D-2026-10-14-c / P11). The holes for `C` are correctly left open.

9. **Identifying a result**: The `Record` and the later `MemoKey` (in plan.lth) together cover the demand side of 8.S8 / 12.S18. Missing from this file alone is any law that the `Run`’s `result` is determined solely by the `Record` plus the plan/certificate hashes (the full identity is completed in plan.lth).

**demand_model.lut**

1. **Laws that are wrong**: None.

2. **Laws that do not determine\ldots**: (N/A – model file.)

3. **Roles (L2.7)**: None.

4. **The models against their theories**:  
   - `demanding` satisfies `PassedDownNotRecomputed` and `RecordsEveryCutoff` by construction.  
   - `NoPriceRefusesAssumed` and `LoweringLosesNothing` are not exercised by any concrete `Entry`/`Certifying` value in the file; they hold only by the structural identity of `lawDemand`. No counter-example is present, so the model does not break them.

5. **Against the specification**: Defaults (`Sampled`, 10 000 000 fuel, \ldots) are declared as default arguments of `theDemand`, matching L5.18/L5.19 and 12.S18. No contradiction.

6. **Implication over a type**: None.

7. **What you would change first**: Supply an explicit test case that exercises `NoPriceRefusesAssumed` with an `AssumedGrade` entry, so the law is witnessed rather than only structurally true.

8. **Cutoffs**: All cutoffs are parameters of `theDemand`; none are constants.

9. **Identifying a result**: The model records every field of the demand into `Record`, satisfying the demand half of 12.S18. The plan/certificate half is outside this file.

**plan.lth**

1. **Laws that are wrong**:  
   - `PlanIsConfluent` quantifies over arbitrary `s1 s2 : Schedule` and asserts `Confluent` on the live set. That is true of any pure dataflow, but the law is stated as a property of a `Planning` model; a model that produces only non-linearizing schedules still satisfies it vacuously on the schedules it never emits. The intended claim (that the schedules the planner actually produces are confluent) is weaker and should be stated only for the schedules that `plan` returns.  
   - `StrategiesAgree` and `TheDefaultsAgree` rely on `EquivalentOn` which itself uses `run`; if `step` is not pure the equality can fail, but the file assumes purity (8.S5).

2. **Laws that do not determine what they claim**:  
   - `KeySeesThe*` laws only force that a change in one component changes the hash *or* the component is equal. A constant-hash model that ignores every field still passes every `KeySeesThe*` law (the “or” short-circuits). The same holds for `PlanHashSeesTheSchedule`.  
   - `KeyReadsOnlyTheCone` is an implication whose premise (`memberStr n live`) is rarely true for random `n`; a model that always returns the original key when the name is not live still passes, but so does a model that mutates the key for live names provided the concrete values happen to match.

3. **Roles (L2.7)**:  
   - `Strategy` is introduced by `data { ForwardOnDemand : Strategy ; CallByNeed : Strategy ; }` with no law stating the role of either constructor. By L2.7 / D-2026-10-13-p this should be an alias or each constructor needs an explicit role law. The rest of the file treats them only by pattern-match, confirming they currently state no role.

4. **The models against their theories**: (N/A – theory file.)

5. **Against the specification**:  
   - 8.S4 / 8.S11 require a function from demand + program to plan; the file leaves `dataflowOf` and the body of `planOf` as holes (explicitly marked).  
   - 8.S8 lists “the model its type names” and “the tolerance”; the `MemoKey` omits an explicit model name and carries only `decoration` (the type) and the live values.  
   - Default strategy in the file is `CallByNeed` (matching today’s `run.py`), while 8.S3 decides `ForwardOnDemand` as the default; the file notes the discrepancy.

6. **Implication over a type**:  
   - `Confluent`, `KeyReadsOnlyTheCone`, and all `KeySeesThe*` laws are written as implications whose premises (`LinearizesOn \ldots`, `memberStr n live`, component equality) a random sample rarely meets. The subtype of linearizing schedules (or of live names) should be the quantified domain.

7. **What you would change first**: Give `Strategy` role laws (or turn it into an alias) so that L2.7 is satisfied; without them the two constructors are free names that state no concept.

8. **Cutoffs**: None appear as constants; strategy is a parameter, live set and schedule are computed.

9. **Identifying a result**: `MemoKey` + the seven `KeySeesThe*` / `PlanHashSeesTheSchedule` laws are exactly the identity required by 8.S8 / 12.S18. The only missing piece is a law that the host’s hash function itself is collision-free on the concrete components (the file correctly leaves collisions to the host). The record side lives in demand.lth; together they cover the full key.

**plan_model.lut**

1. **Laws that are wrong**: None of the Boolean laws are false on the supplied example.

2. **Laws that do not determine\ldots**: (N/A.)

3. **Roles (L2.7)**: Inherits the missing role laws for `Strategy` from plan.lth.

4. **The models against their theories**:  
   - `planning` satisfies `PlanIsTheLiveCone`, `PlanLinearizes`, `StrategiesAgree`, `TheDefaultsAgree` and `KeyReadsOnlyTheCone` / `KeyReadsTheType` on the concrete `example`.  
   - `PlanIsConfluent` holds for the three schedules shown (`needPlan.schedule`, `forwardPlan.schedule`, and the hand-written `["a","c","b","d"]`).  
   - No model of `Keying` is supplied (explicitly because 8.S10 says the result store does not exist); therefore the `KeySeesThe*` laws are not witnessed.

5. **Against the specification**: The example correctly leaves `e` out of the live set of entry `"d"` (L5.13). Defaults match the theory’s `CallByNeed` default. No contradiction with 8.S3–8.S11 beyond the holes already noted in the theory.

6. **Implication over a type**: The concrete tests avoid the rare-premise problem by using only linearizing schedules.

7. **What you would change first**: Add a trivial `Keying` model (even a pure host hash) so that the seven key laws become witnessed rather than only postulated.

8. **Cutoffs**: None.

9. **Identifying a result**: The model demonstrates confluence and live-set correctness but supplies no `MemoKey` or hash, so the identification half of 8.S8 remains unexercised (as the theory itself notes).

**Against 08-demand.md (cross-file)**

- The Boolean reduction of cutoffs to `Grade` (demand.lth) is justified by D-2026-10-14-c but diverges from the richer `C`-based description still present in 8.S1/8.S2.  
- The open holes (`dataflowOf`, generic decoration, `C` costs) are correctly marked and match the “not written” clauses of 8.S4/8.S11.  
- Strategy default mismatch (CallByNeed in code vs ForwardOnDemand in 8.S3) is acknowledged in the files.

**not sure**

- Whether the host’s concrete hash of a `MemoKey` satisfies the seven `KeySeesThe*` laws (left to the host, as certification.lth does for cones).  
- Exact interface required of a decoration `P` beyond the functor/applicative laws listed in 8.S2 (file marks it proposed).  
- Whether a future cost-typed cutoff will still be passed down unchanged (L12.3) once `C` is filled; the Boolean draft cannot demonstrate it.