# run.py bite 13: the demand as a value, the plan's live cone and schedule: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-13.md; saved by the coordinator.
Files: `src/luthier/run.py`, `src/luthier/cli.py`, `tests/test_run.py`, new `tests/run/plan_cone.lut`.
Checks: test_run and test_certify pass (7 new tests); the suite 694 passed; the fit's slow test
7.5 min; the new fixture checks clean.

`PassedDownNotRecomputed` (L12.3): `run` builds one frozen `Demand` (`demand_of`: entry,
accepts, fuel, sets, checked, pinned; decoration and delta none) with `DEMAND_DEFAULTS`
mirroring demand_model.lut's `theDemand` (a test parses that file and checks they agree);
`accept` resolved once; `certification` and `FirstActions` derive every law's demand from it
(`demand.law`, `demand.inner(law).law`); a test spies on `certify.serves` under `--accept
assumed`. `RecordsEveryCutoff`: the entry gets one `demand` object (the model's `Record`); the
old fields kept as duplicates where readers use them, a test checks they agree.
`PlanIsTheLiveCone`, `PlanLinearizes`: the entry gets `plan` with strategy `CallByNeed`, the
entry, `live` (the names of `runtime_slice`), `schedule` (each constant's `Shared` cell appends
its name when its first reduction ends: byNeed's order) and `hash` (sha256 of canonical JSON);
`PlanHashSeesTheSchedule` tested; the plan and hash equal across two runs (plan_cone.lut and
the fit). `KeyReadsOnlyTheCone`: `key` `{decoration, values}` with only the sets whose hole is
in the live cone. `Runs`/`determined`: `read_runs(path)` returns the runs and the breaches
(equal `demand`, different `output`); nothing served from it. `PlanIsConfluent`,
`TheDefaultsAgree`: plan_model.lut's `bothLinearize` and `agree` evaluated through the Runner,
both true, both schedules a, b, c, d. cli: `--main`, `--fuel`, `--checked` default to None so
the demand's defaults apply.

Readings: the demand built after `fill` (the sets need the holes' types); the schedule holds
only the constants `share` makes cells for (a subset of `live`; thin for world-threading
programs); `live` the static slice, roots included; internal names in `live` and `schedule`;
a law's `given` only the sets it has a parameter for; `run()`'s Python default fuel
10,000,000. Store incident: a smoke run wrote a first-action entry into world_model.cert.json;
restored from HEAD.

For the coordinator: demand.lth's `Record` has neither the files read nor a seed, so two runs
of one demand with a changed input file or a nondeterministic host read as breaches of
`determined` though 8.S8's key includes inputs; demand.lth's to decide.
