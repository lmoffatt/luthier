# Report: two findings of criterion e (and the 4.R9 refusal at `Hash`)

Written 2026-10-15 by Claude Opus 5.5, an agent of the coordinating session, on
`prompt-findings-e.md` in this folder, from fba9460. The Python is left uncommitted: tester.py,
run.py, certify.py, check.py and three test files. Suite: 717 passed, 5 skipped, 9 xfailed (4 min
41 s). Findings 1 to 3 below are those of `report-e.md`.

## 1. Model homes (tester.py)

`model_homes` now reads a home as the prompt states it: a file, other than the test program and
core, that defines a value whose type has as its head the theory head of the parameter the binding
binds. A theory head is a name declared at a record in the runner's program (`Host (S : Concrete) :
{ ... }`). Its definition by laws is pruned from a runner's program, so the declaration alone is
read [proposed]. The census the binding names is a candidate when it is itself such a value
(`numpySort : Kolmogorov`), and so is each member of a list literal census (`hosts := [host]`). A
type alias (`State`, demand.lth's `Record`), a type, a constructor (`Sampled`), a label of a sum,
and any census bound to a parameter whose type is no theory head (`S : U`, `accepts : Grade`) give
no home. `_is_type` is gone; `_theory_head`, `_is_model` and `_program_head` replace it.

Test: `test_an_alias_or_a_constructor_is_no_model_home` (tests/test_tester.py) puts demand_laws.lut
and world_laws.lut back in their first form in a scratch directory (`[Record]`, `[Sampled]`, the
Host lines on `states`), and binds the Host lines to world_model.lut's `host` to show a model home.
OneIdentityOneResult and AppliedWhenSettled have no home (they had demand.lth and test.lth); the
Host and Console lines have world_model.lut; NoPriceRefusesAssumed has certification_model.lut.

I compared the homes of every line of tests/tester/*.lut before and after. Besides the two cases
of the report, these homes go away: generators_model.lut for the six `...Gives...` laws (their
model is a generator function, not a theory's model); distances.lut through `pitResolution`;
session_a.lut through `dimA`, `settingsA` and `dampingA`; distance_graph.lut through
`firstViolation` (ReportsValidity); world_model.lut for plot_laws.lut, through the alias `State`.
None of them is read by a run: run.py's `certification` demands only the laws of a theory that a
name's type states, and the entry serves only a demand whose model its reach lists by name. The
entries already in generators_model.cert.json (tracked), in world_model.cert.json for the plot laws,
and in the ignored stores of examples/sonolocalizacion stay as they are and are no longer
refreshed. The homes that a run reads (arrays, numbers, tables, plan, belief, optimization,
probability, plot_model, certification_model, world_model for Console and Host, session_a through
`priorA`) are unchanged.

## 2. A tester's entry and a first action (run.py, certify.py)

Entries written by a first-action validation now have their own kind, `"kind": "FirstAction"`
(`certify.FIRST_ACTION`), as controls have `Control`; it is part of the entry's identity. The
demands `FirstActions` makes carry that kind, and `certify.serves` requires the entry's kind to be
the demand's: a first action is served only by an entry a first action wrote, and any other demand
only by an entry with no kind [proposed]. The seven first-action entries already in
world_model.cert.json have no kind. `certify.entry_kind` reads them as FirstAction by their
evidence's `protocol` ("first action (10.S10)"), so they keep serving and no run rewrites that
store for them [proposed].

What I found while testing: today the hole does not open by itself. The run gives the action's law
the places it adds (`extra`) as well as the model and its own arguments, for HostAgreesReadFile too,
and a tester line's reach never holds `extra`, so `covers_all` already refused the tester's entry.
I checked this: a tester entry on `honest` at s = "once" did land in the model's store, and the run
still confirmed its own case. The kind closes the hole by construction, whatever a reach covers.

Test: `test_a_testers_entry_on_the_model_never_serves_its_first_action` (tests/test_run.py). A test
line certifies HostAgreesPrint on `honest` over a listed case at s = "once", and its entry goes into
first_action_models.cert.json. The test widens that entry's reach to the places the run adds. The
run then confirms both laws on its own case and writes FirstAction entries. The test also asserts
that, without its kind, the run's demand would have been served by the tester's entry (same law
cone, same model hash), and that with it, it is not.

## 3. 4.R9 at an imported alias `Hash` (check.py)

This was plainly the checker's. demand_laws.lut's imports bring kernel_laws.lth's alias
`Selected (A B : U)` and term_model.lut's sum label `Selected` (through certification_model.lut).
Flattened together, they do not elaborate ("alias Selected needs 2 arguments"). `typed` then fell
back to the file alone, which drops every imported alias, so `Hash` became an opaque name and a
string literal's `String` did not refine it. Inside `List Hash` no application is compared, which is
why that literal passed. The fix is in `load_imports`: an imported alias follows the rule that
imported definitions already followed, and is left out when its name is a constructor or a label of
a sum, unless the file lists it. The test `test_an_imported_alias_does_not_take_a_labels_name`
(tests/test_check.py) builds the three-file case; it fails without the fix. demand_laws.lut with
`(h : Hash)` checks clean now.

What remains: when any imported act still fails to elaborate with the rest, `typed` falls back to
the file alone and loses all imported aliases at once, silently. I left that as it was.

## Left as they are

The local workarounds in the test files (`Key`, `sampledCutoff`, `HostState`, `listedHost`,
`(h : String)` in demand_laws.lut) are no longer needed but still work; the prompt scoped the change
to the Python, so I did not touch the .lut files. `listedHost` still keeps listed cases off `host`'s
store, which the fix no longer requires.

## Decisions taken on my own (each undone by reverting the Python)

- A theory head is read as a name declared at a record in the runner's program; the census itself
  counts as a model only when its type has the theory head (a list census in another file is no
  home, only its members are).
- The homes that went away (section 1) go away, since no run reads them.
- The kind `FirstAction` for first-action entries and their demands, exact kind match in `serves`,
  and the old first-action entries read by their protocol.
- check.py leaves out an imported alias named like a constructor or label, rather than renaming it
  `name@file` as run.py's `Loaded` renames definitions.

## Accepted when

- The suite passes: 717 passed, 5 skipped, 9 xfailed.
- `luthier certify tests/tester/demand_laws.lut --no-cert` ran its 3 laws (cases) and wrote no
  store: no `.cert.json` under src, tests or examples changed, and none sits beside a `.lth`.
