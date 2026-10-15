# Report: v0.4 criterion (e), step 6's theories with their laws controlled (L9.14)

Brief: record/IA/v04-2026-10-15/prompt-e.md. By Claude Opus 5.5, a subagent of the coordinating
session, 2026-10-15. No theory file touched. Each .lut and each store committed alone.

Principles touched: L9.14 (a law is evidence of nothing until a wrong model refutes it), applied to
world.lth, demand.lth, plan.lth and the port's laws; P2 (everything derived carries how it was
derived) for the two model stores; P11 (every criterion a parameter) for the cutoff of
`AppliedWhenSettled`, a census of one. Assumes, as the earlier control reports did, that a control
matches its law by the law's cone hash.

## Commits

- d97a369 plan_laws.lut, fa9cf99 plan_controls.lut.
- 97e614c demand_laws.lut, a4a171e demand_controls.lut; 1fab70a (the key type renamed locally, see
  finding 1).
- fbad28b world_laws.lut, d7c0480 world_controls.lut (lines added to both; the four `Console`
  lines unchanged); 0cd18cc (the cutoff and the Host lines' state type renamed locally, finding 1).
- ba0971e sonolocalizacion_laws.lut [proposed]: `LayoutFromUndoesTo` and `LayoutToUndoesFrom`
  take the layout as a parameter `lay`, bound to positions.lut's `layout`. With `layout` named in
  their bodies no wrong layout could be passed, so they could have no control. Their cone changed;
  they were certified again. d660067 sonolocalizacion_controls.lut.
- a7aff0f plan_model.cert.json, 89d42f1 certification_model.cert.json: derived, new, the entries
  certify wrote at d660067 for the lines whose census names `planning`, `example`, `eqNat` and
  `certifying`.
- 07b10af test_elaborate.py: `test_eval_prints_the_states_and_demands_no_certificate` expected
  plan_model.lut's cone uncertified; plan_model.cert.json now has entries, so the test empties its
  own copy of that store (conftest.py's `LUTHIER_LIBRARY_STORES`) and keeps what it tested.

## What the lines are

plan.lth, on plan_model.lut. `Dataflow`'s three laws on `example` plus two written in the test file:
`uneven` (first demand from `d` is not by levels) and `leafy` (a read of a name no node defines).
`Confluent` on listed schedules, `Planning`'s seven on `planning`, and the two statements of
`demandKey`. There is no generator of dataflows, so everything is listed (ExhaustiveMode). Controls:
a node named twice, two names that read each other, `hidden` (a step that reads a name its node does
not list), and five broken planners (live set = the whole graph, schedule reversed, forward plan
missing its first name, forward in first-demand order, call by need in forward order).
`Confluent` and `PlanIsConfluent` are refuted on `hidden`: their planner is right, and the break
they catch is in the dataflow.

demand.lth. `OneIdentityOneResult` on stores written here, keyed by `Record` with structural
equality. No model file gives a store, because `x.run.json` is never read back (8.S10). Which
identity to use is item 5 of summary-BCD.md, still his. Control: one identity, two results.
`NoPriceRefusesAssumed` and `LoweringLosesNothing` (predicates for `Certifying`) on
certification_model.lut's `certifying`, over `theDemand` at three cutoffs and entries written by
hand. Controls: a `serves` that ignores the cutoff, and one that serves only at the cutoff exactly.

world.lth. `Described` on the console's three descriptions and on `lockWrite`, an own action
written here, since no own action has a model yet. Controls: an own action that appends to the store
where it should set, and a `print` that also writes log.txt. `Externs` on `validator` and
`Crossing` on `bridge`. Both are written here the way run.py works, because the real ones are
Python. The cutoff is a census of one, `Sampled`, demand_model.lut's default [proposed]. Controls:
apply every extern, grade an extern with no laws, validate a provisional one, identity by route
alone; a bridge that reverses the values, one that counts one call per crossing, and one that calls
the first field whatever the label (the review's W5). `Host`'s four laws over listed `Observed`
cases (the ones a faithful host gathers by `agreement`) on `listedHost`. That is world_model.lut's
`host` under another name, see finding 2. A Host law reads only the console of the host model, and
that console is never the host's own (W1). So a host broken on purpose can only show in the cases
it gathers, and each control lists such a case: print without the newline, a readFile that finds
nothing, an observation that empties stdout, a print that also overwrites input.txt.

The port (sonolocalizacion_laws.lut). Controls: a layout whose `from` reads the vector row by row
(identical to the real one at one node, wrong from two on); both native likelihoods with K/2 log 2π
dropped (K the number of pairs), score and information kept; a graph check that sees the schema
and no row.

## The run

`PYTHONPATH=src python3 -m luthier.cli certify --jobs 2 --fuel 100000000 tests/tester/*_laws.lut
tests/tester/*_controls.lut`, with stores, no suite running. First at d660067 (exit 0, 9 min 9 s),
then again at 1fab70a after the renames of finding 1 (exit 0, 38 s; every line known but the 8
renamed Host and AppliedWhenSettled lines). Second run: 177 laws in 13 files, 175 controlled, 2
uncontrolled, CONTROL FAILED 0 times. Those 175 are 18 more than the earlier 157 (142 plus the
tail's): 13 plan, 3 demand, 13 world, 6 port. Then `python3 -m pytest -q`, alone: 714 passed,
5 skipped, 9 xfailed (4 min 36 s). The tracked stores did not change.

The new files' lines, as certify printed them (grade; control status; model refuted):

    demand_laws.lut   OneIdentityOneResult (cases) controlled, st = twoResults
                      NoPriceRefusesAssumed (cases) controlled, k = servesAnyPass
                      LoweringLosesNothing (cases) controlled, k = servesAtExactly
    plan_laws.lut     NamesAreUnique, Acyclic, StepIsLocal, Confluent (cases) controlled on twice,
                      cyclic, hidden, hidden; PlanIsTheLiveCone, PlanLinearizes, StrategiesAgree,
                      TheDefaultsAgree, ForwardIsByLevels, ByNeedIsFirstDemand (cases) controlled on
                      wholeGraph, reversedSchedule, forwardDropsFirst (twice), forwardAsNeed,
                      needAsForward; PlanIsConfluent (cases) controlled on d = hidden
                      KeyReadsOnlyTheCone, KeyReadsTheType (cases) uncontrolled
    world_laws.lut    the four Console laws (cases) controlled, as before; OwnIsIdempotent,
                      ChangesOnlyDeclared (cases) controlled on appendsLock, printLogs;
                      AppliedWhenSettled, NoLawNoGrade, ProvisionalIsAssumed, IdentityCarriesHash
                      (cases) controlled on appliesEvery, gradesWithoutLaws, validatesProvisional,
                      identityByRoute; CallbackGivesTheFunction, CallsAreCounted,
                      RecordCrossesByField (cases) controlled on reversesCalls, countsOnce,
                      callsFirstField; HostAgreesPrint, HostAgreesReadFile,
                      HostObserveChangesNothing, HostChangesOnlyDeclared (cases) controlled on the
                      broken hosts' cases
    sonolocalizacion  LayoutFromUndoesTo, LayoutToUndoesFrom (sampled) controlled, lay = rowMajor;
                      FullAgrees, ProfileAgrees, ProfileIsFullAtItsSigma (sampled) controlled on
                      noConstantFull, noConstantProfile; ReportsValidity (cases) controlled,
                      f = schemaOnly

## Every law of the brief's theories, and those without a control

Controlled with a line: all of the above.

Uncontrolled, with why:

- plan.lth `KeyReadsOnlyTheCone`, `KeyReadsTheType`: they have lines and they pass, but both follow
  from `demandKey`'s definition for every planner, so no model can fail them. plan.lth says so
  itself (B13: kept as statements of the definition and not claimed by `Planning`). A control
  would need the key function to be a parameter of the law, which means a new definition.
- plan.lth `Keying`'s seven laws (`KeySeesTheDemand/Cone/Mode/Seed/Plan/Certificates`,
  `PlanHashSeesTheSchedule`): no line. The brief said "where a model exists", and none does
  (8.S10: the result store doesn't exist; plan_model.lut says `Keying` waits for the host's hash of
  a key). A model written in the test file would certify no real key. Criterion (c) builds the
  store and its key, which is the model these laws should run on.
- world.lth `ObserverIsFaithful`: no line. It is an axiom (11.R3) whose body reads nothing of the
  model, so it has nothing to sample and nothing to break. Its evidence is a citation or an
  assumption (6.S9, 6.S10). run.py accepts it as assumed by default.
- world.lth `WriteThenRead`, `WriteChangesOnlyItsPlace` (`Persistence`): controlled in
  tests/tester/plot_laws.lut on plot_model.lut's `files` (writesEmpty, keepsOnlyIt). I didn't
  duplicate them in world_laws.lut.

## Findings

1. tester.py's `model_homes` reads some census members of other files as models. A type alias
   (`State = {...}`, demand.lth's `Record`) isn't seen as a type by `_is_type`, and a constructor
   (`Sampled`) is taken for a model. The first run wrote `src/luthier/lib/demand.cert.json` (beside
   a theory), `src/luthier/lib/test.cert.json`, and the Host lines' entries into
   world_model.cert.json. I renamed them locally in the test files (0cd18cc, 1fab70a), deleted the
   two new stores, put world_model.cert.json back to its committed bytes, and certified again. The
   fix belongs in tester.py and I left it alone.
2. A latent hole in run.py's validation at first action. `FirstActions` serves a Host law from any
   entry of the model's store whose reach covers the run's given values. The case isn't one of
   them. For `HostAgreesReadFile` the given values are the model and `p` only, so a tester entry
   of listed cases bound to `host` at `p = "input.txt"` would serve a run that reads input.txt,
   and the run would skip gathering its own case (10.S10). That's why the Host lines bind
   `listedHost`. Anyone who certifies Host laws on `host` from a test file would trigger this
   silently.
3. The checker refuses (4.R9) a string literal passed to a parameter typed by the imported alias
   `Hash` (`entry (l : String) (h : Hash) ...` applied to `"sha256:cccc"`). It accepts the same
   literal in `cones : List Hash := [...]`. I worked around it with `String`.
4. A line already known does not write its model's store again. world_model.cert.json therefore
   has no entries for the Described lines (bound to `theWorld`), whose first entries I removed
   with the rest in finding 1. Nothing a run reads depends on them.
5. The port's three likelihood laws run out of fuel at `luthier test`'s default fuel (1,000,000
   per case) and pass at certify's 100,000,000. That was already true before this task.

## Decisions taken on my own (each undone by one commit)

- Host lines on `listedHost`, not `host` (fbad28b, finding 2).
- The layout laws take the layout as a parameter (ba0971e) [proposed].
- `validator` and `bridge` written in world_laws.lut as the models of `Externs` and `Crossing`.
  The cutoff `Sampled` is a census of one [proposed].
- No line for `Keying` or for `ObserverIsFaithful`. `Persistence` left to plot_laws.lut.
- Lines for `Confluent`, `NoPriceRefusesAssumed` and `LoweringLosesNothing`, although no theory
  claims them.
- Local names for census members of other files (0cd18cc, 1fab70a). Deleted demand.cert.json and
  test.cert.json (mine, untracked), and restored world_model.cert.json to HEAD.
- Committed plan_model.cert.json and certification_model.cert.json as new derived stores.
- test_elaborate.py's test empties its copy of plan_model.cert.json (07b10af).

## For him

Criterion (e) is met except for `Keying`'s seven laws, which have no model to run on yet. They get
one when (c) builds the result store's key. Until then they read uncontrolled for the reason
above.
