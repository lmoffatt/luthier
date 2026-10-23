# Wave A, Agent 2 (Sonnet 5.5): bites A2 and A7

2026-10-23. Sources: audit II.2, 3.3, 3.4 (report.md, 5b1a05e); execution.md A2, A7.

## A2. The demand records every policy (02146ad)
- demand.lth: `Demand`, `RunRecord`, `inner`, `recorded` gain `axioms : Grade`, `roots : List String`, `combine : String`; plan.lth's `withSet` carries them. New law `RecordKeepsThePolicies` (over the record-making function), gathered as `RecordLaws`. `demandKey` unchanged (comment cites 8.S8: no result's value changes).
- demand_model.lut `theDemand` declares the defaults: `AssumedGrade`, `["ObserverIsFaithful"]` (the project's root of trust, L11.9), `"weakest"`.
- run.py: `AXIOMS` removed; `Demand.axioms/roots/combine` take their defaults from `DEMAND_DEFAULTS`; `cutoff(axiom, law)` lowers the cutoff only for an axiom law named in `roots` or by `--accept assumed:NAME`; `record` lists the three; the "names no provisional" warning no longer fires for a named axiom law.
- Checks: tests/test_run.py (new `test_the_demand_records_every_policy`, record-equality test extended, defaults-mirror test reads list literals); demand_laws passes, demand_controls refutes `RecordKeepsThePolicies` (three broken recorders).
- For Luciano: the examples' run records (`x.run.json`) lack the three new fields until regenerated.

## A7. The key's laws (see commit after 02146ad)
- plan.lth §4: the hash laws renamed `DigestSeparatesThe*` and `PlanDigestSeparatesTheSchedule`, restated as collision evidence on listed cases; the comment says a finite digest cannot be injective and the lookup compares the full key. `Keying` gains `serves : Bool -> MemoKey -> MemoKey -> Bool` (pure cone, stored key, asked key) and laws `LookupComparesTheFullKey` and `ActionConeIsNeverServed`. `Planning` gains `PureConeIsDeterminate` (conditional on `StepIsLocal` over listed environments, L4.7). No injectivity claim is left.
- plan_model.lut: first model of `Keying` (`keying`), the digest an extern (run.py `memo_digest`, `record_digest`) over values flattened because the bridge reads no `data` value. It hashes another serialization than run.py's `key_hash`.
- Tests: plan_laws (20 lines, all Cases) and plan_controls (all refuted, one broken model per new law, forward-drops-first for the determinacy law). Run with store off.
- Pytest: tests/test_run.py and tests/test_result_store.py 155 passed. check_spec prints only its known finding.

## Not done / for the coordinator
- Stores not re-certified: demand, demand_model, plan, plan_model (and anything importing them; certification stores of files whose cone includes demand.lth) are stale. `Planning` and `Keying` changed shape, so `plan_model.cert.json` needs a pass; `Keying` laws now have lines.
- Semantic quotient (audit 3.5) untouched, waits for question 5.
- certify.py and certification.lth hunks in the tree are Agent 1's.

## Decisions taken on my own
1. `roots` as a list of axiom-law names, and `--accept assumed:NAME` extending it (reuses `assumes`); the alternative was a new CLI flag.
2. Renamed the six `KeySeesThe*` laws and `PlanHashSeesTheSchedule` (no store entries existed, so no churn).
3. Dropped the "digest is a function" law: a function gives it (8.S2).
4. `Keying` model uses a distinct serialization from run.py's JSON key; real runs are covered by test_result_store.

## Question
Should `--accept assumed:NAME` be the only way to extend `roots`, or does a root of trust deserve its own declared list in the program (L11.9)?

## Follow-ups from the coordinator (after the report)
- A4 follow-up: `run.py` gives each law's demand `conjuncts` (`law_cones.conjuncts(law)`) and `_conjunction_demand` the theory's. New test `test_a_store_listing_two_of_three_conjuncts_does_not_serve_a_run` fails without the change, passes with it.
- A3 follow-up: `core_data` now includes core's `implies`, so every runtime slice keeps it and `eval` of `1 < 0 -> true` gives a Bool. Test `test_the_runtime_slice_keeps_implies` fails before, passes after.
- tests/test_run.py: 149 passed, 3 skipped, 2 xfailed.
- Question answered by the coordinator: `--accept assumed:NAME` stays; a declared list belongs to D-2026-10-16-n's bite.
