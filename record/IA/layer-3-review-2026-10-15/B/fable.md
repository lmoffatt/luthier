# Review of bundle B (layer 3, round 1), at 2710cfc

## `demand.lth`

**1. Laws that are wrong**

- `Runs : U := { rs : List Run | determined rs }`, with `agreesWithRun … (not (r.record == q.record) or r.result == q.result)`: false of the intended store. `Record` holds no decoration and no seed, so a run of `main : T` and a run of `main : P T` (same entry, cone, sets, grade, fuel, checked, lock) have equal records and different results — 8.S8: "a value and its derivative have two keys". Likewise two runs that differ only in the seed, when a sampled certificate of the cone passes under one and fails under the other (the reason 8.S8 puts `s` in the key). A store holding both legitimate runs is not a `Runs`.
- `NoPriceRefusesAssumed (m : Demanding) (k : Certifying) …`: quantified over every `k : Certifying`, and `m` contributes only `m.lawDemand d law cone`, which `PassedDownNotRecomputed` pins to `{ law, cone, given := d.sets, accepts := d.accepts }`. So the law constrains nothing of `m`: if `Certifying` already says `serves` refuses an entry below `accepts`, every `m` passes; if it does not, a `k` whose `serves` ignores `accepts` fails it for every `m` and `Demanding` has no model. Which of the two is bundle A's (not sure). Either way it is a law of the wrong theory.

**2. Laws that do not determine what they claim**

- `LoweringLosesNothing … := ServesIsMonotoneInTheCutoff k (m.lawDemand d law cone) e g`: a law of `Certifying` evaluated at a fixed `LawDemand`; no `m` can fail it.
- `PassedDownNotRecomputed` and `RecordsEveryCutoff` are equations that fix `lawDemand` and `recorded` outright. `Demanding` has exactly one model, so there is no wrong model to give: the two operations are definitions (L2.7), and the "theory" is an empty record with two borrowed laws. The claim in the name `RecordsEveryCutoff` ("the record carries every cutoff and parameter the demand carries") is not what the law checks: a `Record` without the decoration is the only record there is.

**3. Roles.** No `data` in the file. Nothing.

**4. The model.** See `demand_model.lut`.

**5. Against the specification**

- `Record = { entry, cone, parameters, accept, delta, fuel, checked, lock }` omits the decoration. 8.S1 counts the type demanded among the demand's parameters (D-2026-10-13-f); L5.18 says every threshold is "recorded with it"; 12.S18 as cited records "the parameters". And "[proposed] In the Boolean draft the record is the identity of a result" contradicts 8.S8, which puts the type demanded, the seed, the mode, the plan and the certificates in the identity — the file knows this ("the key of 8.S8 … is plan.lth's") and still has `Runs` claim identity from `Record`.
- `admitsAssumptions … := gradeRank d.accepts <= gradeRank AssumedGrade` and "[proposed] Until then `run --accept assumed` is where a demand names that price": 6.S10 / L10.2 make the price of an assumption a value with no default. Here admission is a grade with a default (`Sampled`) and, once `--accept assumed` is given, assumptions enter at no stated price. A Boolean stand-in is what D-2026-10-14-c asks for, but this one drops the rule instead of parameterizing it; the `assumed : Demand -> Maybe C` hole should be the field, `nothing` by default, so 6.S10 survives the draft. (A disagreement with the draft's reading, not with the chapter.)

**6. Implication over a type**

- `NoPriceRefusesAssumed … := admitsAssumptions d or not (e.grade == just AssumedGrade) or not (k.serves …)`: a drawn `d`, `e` meets the premise about one time in |Grade|, and if `serves` compares `e` with the law and cone (not sure) a drawn `e` never matches, so the third disjunct is true and the law is never exercised. Domain: demands with `not (admitsAssumptions d)` × entries of grade `AssumedGrade` for that law and cone.
- `agreesWithRun … (not (r.record == q.record) or …)`: drawn lists of runs never share a record. If `Runs` is ever drawn, the domain is pairs of runs of one record.

**7. Change first.** Make `lawDemand` and `recorded` definitions, drop `Demanding` as a theory, and state the one law of this file a model can get wrong — determinism of the store of runs — as the law of a theory whose operation is the store, over a record that carries what the key carries (decoration, seed, mode; or `MemoKey` itself). Reason: as written no model can fail any law here, and the determinism the file does state (`Runs`) is both false (item 1) and claimed by no theory.

**8. Cutoffs.** None as constants. `accepts <- Sampled` and `fuel <- 10000000` (`demand_model.lut`) are declared defaults, the form L5.19 allows. Observation: the per-law cutoffs of D-2026-10-14-c (tolerance, resolution, rank floor, level) have no field; they travel in `sets` under the laws' parameter names (`LawDemand.given := d.sets`). That works, but nothing in `Demand` tells a cutoff from a hole value, and `DemandKey` keeps one only if the law's parameter name is in `live` (plan.lth §4) — whether the backward pass reaches laws is not written.

**9. Identifying a result.** Missing: (a) the identification law itself, claimed by a theory — "equal key, equal result"; `determined` says it for `Record`, but no theory holds a `Run`, and the record is the wrong one (item 1); (b) the bridge from `Record` to `MemoKey`: nothing maps a run's record to its key (`demandKey` needs `live`; `Record` has no decoration, seed, mode, plan hash, certificates), so this file and plan.lth identify a result by two unrelated records; a `keyOf (recorded d h) …` and the read-back law (a run read from `x.run.json` has the key of the run that wrote it) are what would make the record a memo when 8.S10 is lifted.

## `demand_model.lut`

**4.** `demanding` satisfies `PassedDownNotRecomputed` and `RecordsEveryCutoff` by construction. `NoPriceRefusesAssumed` and `LoweringLosesNothing` depend on `Certifying` alone (not sure). With `admitsAssumptions` as read, `accepts <- Sampled` refuses assumed, as the comment says.

**5.** `theDemand (entry …) (accepts …) (fuel …) (sets …) (checked …) (pinned …)` takes no `decoration` and no `delta`, and sets `decoration := nothing` always. So no run can ever ask for `P T`: 8.S1's decorated type has no way in until that argument exists. `delta` is marked [proposed]; `decoration` is not.

## `plan.lth`

**1. Laws that are wrong**

- `placedBefore`: `subset (keep placed (readsOf ns n)) placed` is a tautology (`keep placed xs` returns members of `placed`), and `subset (readsOf ns n) (addNew placed rest)` asks only that each read be *somewhere* in the schedule. So `LinearizesOn` never checks "none before what it reads". On `example`, `["d","b","c","a"]` linearizes `[d,b,c,a]`; `run` gives `d = 0` under it (b, c read `init`) against `4` under `[a,b,c,d]`; so `Confluent Nat eqNat example live [a,b,c,d] [d,b,c,a]` is false and `PlanIsConfluent` fails on a drawn pair. Intended: the reads among the schedule's names must already be placed — `subset (keep (addNew placed rest) (readsOf ns n)) placed`, or pass `live` in.
- Even fixed, `PlanIsConfluent (A) (eq) (p) (d : Dataflow A) (e) (s1 s2)` is false over `Dataflow A`: nothing ties `d.step n` to `readsOf d.nodes n`, so a `step` that reads a name outside `reads` gets different values under two linearizations. "`Confluent` … holds because a definition has no effects (8.S5)" — that premise (D-2026-10-10-c: "What is forbidden is what the graph does not show") is a law of `Dataflow`, and `Dataflow = {…}` is an alias without it. The law also never mentions `p`; it is about `d` alone.
- `PlanLinearizes` over all `Dataflow A`: a cycle (`a` reads `["b"]`, `b` reads `["a"]`) has no linearization under the intended check, so for such `d` no `p` passes. The file expects cycles ("so it ends on a cycle too"); L9 says a program is a DAG.

**2. Laws that do not determine what they claim**

- With `placedBefore` as it is, a `Planning` model whose `plan` returns the live names in reverse (readers before reads) passes `PlanIsTheLiveCone`, `PlanLinearizes`, `StrategiesAgree`, `TheDefaultsAgree`, `KeyReadsOnlyTheCone`, `KeyReadsTheType`, and fails `PlanIsConfluent` only as every model does (it ignores `p`). No law separates the right planner from that one.
- `KeyReadsOnlyTheCone` and `KeyReadsTheType` are theorems of the definition `demandKey` (`keepRead` drops `n ∉ live`; `decoration := d.decoration`), true for every `p`; `Planning` has no key operation, so §4's two claims about 8.S8 test nothing. `TheDefaultsAgree` is `PlanIsTheLiveCone` + `StrategiesAgree` at the two constructors.
- `Keying`: only `PlanHashSeesTheSchedule`; a `planHash` reading nothing but the schedule passes, though `Plan` has `strategy` and `entry` (8.S11: the key "changes when any input of 8.S8 changes", the plan being one). Whether the strategy ought to be seen is item 3.
- Minor: `reaches` includes leaves (names read, defined by no node), so `LinearizesOn` requires them in the schedule and `run` applies `step` to them; the comments "a leaf that keeps `init`" and "a name not scheduled keeps `init`" describe something else.

**3. Roles.** `Strategy : U := data { ForwardOnDemand : Strategy ; CallByNeed : Strategy ; }`: no law states what either constructor means; the laws that name them (`TheDefaultsAgree`, `StrategiesAgree`) say only that they agree. A model with `plan CallByNeed = plan ForwardOnDemand` passes every law, so by L2.7 `Strategy` is a collection. Their role is an order: forward on demand places a name as soon as everything it reads is placed, level by level (8.S3: "strictly forward, in topological order"); call by need is the first-demand, depth-first post-order. Either state those as laws of the schedule's shape, or admit that what differs is cost (which `Confluent` says is all that differs) and keep the strategy an alias until cost laws exist.

**4. The model.** See `plan_model.lut`.

**5. Against the specification**

- `planOf … (strategy : Strategy <- CallByNeed)`: 8.S3 [decided D-2026-10-10-d] "The default strategy is … forward on demand". 8.S4's "[implemented] Today … call by need" describes the host, a specimen (L14.3), not the default. The file flags it [proposed]; it still contradicts the decision.
- `DemandKey = { decoration : Maybe Decoration, values : List (String * Value) }`: 8.S9 [decided D-2026-10-13-g] "the key of 8.S8 includes the tolerance, so a hit needs equal keys". In this draft the tolerance is `accepts` ("the cutoff is the weakest grade accepted"), absent from the key: a result served under `Proved` and one under `Assumed` share a key.
- `demandKey … values := keepRead live d.sets`: 8.S2 "the key is a hash of a canonical form". List order and shadowed duplicates (`withSet` conses in front; `given` reads the first) change the key without changing what the cone reads. Same for `MemoKey.certificates : List Hash`.
- `planOf … := p.plan strategy (dataflowOf prog) d.entry`: 8.S11 asks for "a function from a demand and a program to a plan"; only `d.entry` is used. `d.sets` (a parameter "is a node with nothing read", 8.S8) and `d.decoration` (the cone rewritten over `P`, 8.S1) never reach the dataflow, so the plan of a demand with holes or a decoration is the plan of the unset, undecorated program. A hole, but `dataflowOf : Program -> Dataflow Term` needs the demand (or `init` does).

**6. Implication over a type**

- `Confluent … := not (LinearizesOn A d live s1 and LinearizesOn A d live s2) or EquivalentOn …`, with `s1 s2 : Schedule` = `List String`: a drawn list of strings never linearizes. Domain: `{ s | LinearizesOn A d live s }` (a generator: permutations of one topological order).
- `PlanIsConfluent`, `PlanLinearizes`, `StrategiesAgree`, `TheDefaultsAgree`, `PlanIsTheLiveCone` over all `Dataflow A`: the domain is the dataflows that are DAGs with unique names and honest steps — the theory of item 7.

**7. Change first.** Make `Dataflow` a theory with three laws: `step n env` depends only on `env` at `readsOf nodes n`; `names nodes` has no duplicates; acyclic (a rank, or: `LinearizesOn d (reaches d e)` satisfiable). Quantify `Planning` over it and state `Confluent` as its consequence. Reason: it is the one assumption D-2026-10-10-c names, the thing a dataflow "is certified against" (8.S11) has no theory to be a model of without it, and items 1 and 6 leave `Planning` without a model until it exists. Fix `placedBefore` on the way; it is one conjunct.

**8. Cutoffs.** None as constants. `count d.nodes` and `1 + count d.nodes` are fixpoint bounds derived from the data, not cutoffs. `strategy <- CallByNeed` is a default, not a cutoff (its value is item 5).

**9. Identifying a result.** Missing: (a) a law that equal `MemoKey`s give equal results — the memo has no theory, and demand.lth's `Runs` says it over another record; (b) 8.S9's law that a hit serves a demand only with an equal key; (c) the bridge `Record → MemoKey` (`MemoKey.demand` needs `live` and the decoration, `Record` has neither); (d) the tolerance in `DemandKey`; (e) a canonical form for `values` and `certificates`. The `KeySees*` laws cover injectivity per coordinate and are fine as far as they go.

## `plan_model.lut`

**4. The model against the theory**

- `PlanIsConfluent` fails on `example` with `s1 := needPlan.schedule`, `s2 := ["d","b","c","a"]`: `LinearizesOn` accepts the reverse (plan.lth item 1), and `run … "d"` is `0` against `4`. The file's `agree` passes only because `["a","c","b","d"]` happens to be topological.
- `PlanLinearizes` fails on a cycle, `nodes := [{a reads ["b"]}, {b reads ["a"]}]`, entry `a`: `byNeed` gives `["a","b","a"]` — the depth bound ends the visit, but `done` grows only on return, so `a` is appended twice and `noDuplicates` is false ("bounded by the count of nodes, so a cycle ends": it ends with duplicates); `forward` gives `nil`, so `sameMembers` is false. A self-read `a reads ["a"]` gives `["a","a"]`.
- `TheDefaultsAgree` / `StrategiesAgree` fail on a dataflow whose two orders differ and whose step is dishonest: `d reads [b,c]`, `b reads [x]`, `c reads nil`, `x reads nil`, entry `d`: `byNeed` = `[x,b,c,d]`, `forward` = `[c,x,b,d]`; with `step "c"` reading `env "x"`, `c` differs. Drawn only if generators draw `step` (not sure).
- On `example` both strategies give `[a,b,c,d]` and `bothLinearize`, `agree` hold — checked by hand.
- Minor: `readsIn` and `keepIn` duplicate plan.lth's `readsOf` and `keep` instead of importing them.

## Specification (separate items)

- 8.S4's "[implemented] Today there is no plan … call by need" invited the file's wrong default. The chapter could say there that the default is 8.S3's and the host's call by need is a specimen.
- 8.S8's first sentence (L5.6) lists "the tolerance" and "the model its type names"; the decided list (D-2026-10-13-g) builds the key from `key d`, `h(e)`, `m`, `s`, the plan hash and the certificates. Whether the chosen model enters through the plan hash or the cone is not said, and the file left it out.
- 8.S11's list of additions omits the two laws this review found missing: that the key identifies (equal key, equal result) and the law of `Dataflow` on which `Confluent` rests.
- D-2026-10-10-d makes the strategy "a parameter separate from the program"; D-2026-10-13-f makes the demand "the gate through which parameters change what the program does". Together they put the strategy in the demand; plan.lth's [proposed] "an argument of the plan with its default" leaves it outside both.

## Not sure

- `gradeRank`'s direction in `test.lth` (rank increasing with strength, `AssumedGrade` lowest); if inverted, `admitsAssumptions` is backwards.
- Whether `Certifying` has a law that `serves` refuses an entry whose grade is below `accepts` — decides whether `NoPriceRefusesAssumed` is vacuous or makes `Demanding` unsatisfiable.
- Whether demand.lth's `LawDemand` is accepted where certification.lth's `Demand` is expected (`k.serves`, `ServesIsMonotoneInTheCutoff`): structural aliases.
- `Entry`'s fields: `grade : Maybe Grade` is implied; whether `serves` compares an entry's law/cone with the demand's (which makes a drawn `e` never serve).
- Whether generators draw functions (`step : String -> (String -> A) -> A`); if not, the dishonest-step cases are never drawn and the gap in `Dataflow` only shows through `dataflowOf`.
- `==` on `Maybe Decoration` with `Decoration : U` a hole (`KeySeesTheDemand`, `KeyReadsTheType`).
- 12.S18's actual field list (not included): whether it names the decoration and the seed.
- Whether `Sampled` in `test.lth` carries a level or sample size; if so, L5.18 wants it in `Demand` and `Record`.
- Whether the laws of the types a cone uses are nodes of the dataflow, so that `reaches` sees the laws' parameters; if not, no per-law cutoff ever enters `DemandKey`.
- `bound`, `evidence`, `assumed` are declared over `Demand` before `Demand = …` appears; the parser accepts it, the checker's order rule I can't see.

Want this as a doc for the record?