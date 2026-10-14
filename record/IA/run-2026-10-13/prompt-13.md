# run.py bite 13: the demand built as demand.lth says, the plan's live cone and schedule as values, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). On demand.lth and plan.lth
(5df0c75 to a18c4a9; the report `record/IA/demand-2026-10-15/report.md`, section "What run.py
must change, one line per law": read it first, it is the brief's list).

## The prompt

Read `CLAUDE.md` first, then that report whole, `src/luthier/lib/demand.lth` (`Demand`,
`LawDemand`, `inner`, `Record`, `Runs`, the four laws), `demand_model.lut` (`theDemand`, the
defaults), `plan.lth` §1 to §4 (`Dataflow`, `reaches`, `Schedule`, `Plan`, `planOf`, `DemandKey`,
`MemoKey`, the laws of `Planning`), `plan_model.lut` (`byNeed`, `forward`, `example`), and
`src/luthier/run.py` (`run`, `holes`, `fill`, `certification`, `FirstActions`, `record`,
`runtime_slice`, `Runner.force`), `src/luthier/cli.py` (`run`'s arguments). Nobody else edits
now: change `src/luthier/run.py`, `src/luthier/cli.py`, `src/luthier/certify.py` (readers),
`tests/test_run.py`, programs under `tests/run/`.

1. `PassedDownNotRecomputed`, `RecordsEveryCutoff`: `run` builds one `Demand` (a Python object
   mirroring demand.lth's record: entry, decoration none, accepts, delta none, fuel, sets,
   checked, pinned) from its arguments and demand_model.lut's defaults before anything else;
   `certification`, `FirstActions` and every law's demand derive from it (`inner`), `accept`
   resolved once; `record` writes the demand as one object `demand` in the entry (the model's
   `Record`), keeping the existing fields where other readers use them (say which you keep as
   duplicates and why, or drop with a test updated).
2. `PlanIsTheLiveCone`, `PlanLinearizes`: the plan as a value in the run: `runtime_slice`
   exposed as the plan's live cone (the names the entry reaches), and the schedule as the order
   in which `Runner.force` first reduces the shared cells (the call-by-need schedule), recorded
   in the entry as `plan` with its hash (`certify.cone_hash`-like over the schedule, L5.6) and
   the strategy name; `KeyReadsOnlyTheCone`: the record's `key` (plan.lth's `DemandKey`) keeps
   only the sets whose hole is in the live cone, while `parameters` still lists every set given.
3. `Runs` (`determined`): a reader of `x.run.json` (`certify.read_runs` or in run.py) that
   checks `determined` (one record, one result) and reports a breach; not yet served from.
4. `PlanIsConfluent`: a test running plan_model.lut's `example` under `byNeed` and `forward`
   (through `luthier eval` or the Runner) and checking both linearize and agree; the fit's slow
   test checks the record's `demand`, `plan` and `key` are present and the plan's hash stable
   across two runs.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py tests/test_certify.py -q`, then the
suite. Do not commit. Report in your final message: each law of the list met and how, what was
left, every reading taken.
