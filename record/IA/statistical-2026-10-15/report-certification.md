# report: certification.lth knows the statistical evidence

Commit 9a348b9 (certification.lth only; certification_model.lut needed no change: its matches on outcome use `isFailure` and `== Passed`).

Done, all [proposed]:
- `admits`: `Tested v` admits the grade `Sampled` when `v` is `Holds r`, no other (a `Fails` or `Unresolved` verdict grades nothing). It states by hand what `StatisticalByTest` plus test.lth's `grade Supported (Drawn s)` give, since `coverageOf (Tested v)` is `nothing`.
- `Outcome` gains `Unresolved : Rates -> Outcome` (rates and samples spent): not a failure, not a pass, no grade (`gradedAsOutcome` already forces that); `NotRunAddsNothing` gets its case (required by 4.R3, the checker refused without it).
- Rates of a passed statistical entry: they live in the entry's evidence `Tested (Holds r)`, with alpha, beta, delta and spent; no new field. Imports added from laws.lth: `Tested Holds Rates` (laws.lth's own `Unresolved` is not imported, so no name clash).

Accepted when: certification.lth and certification_model.lut check clean (rc 0; a deliberately broken case was refused, so the check is live); demand.lth, plan.lth, demand_model.lut and all tests/tester/*.lut check clean.

What certify.py must change:
- Store an unresolved test as `{"Unresolved": rates}` outcome, not `NotRunFor "unresolved at ..."`; read it back so.
- Its store predicate may accept `Tested` evidence with grade `sampled` only for `Holds`.
- `show_outcome` and `standing`: keep printing an unresolved test as such; it still adds nothing and has no grade.
- Keep writing alpha, beta, delta, spent in the evidence of a passed statistical entry.
