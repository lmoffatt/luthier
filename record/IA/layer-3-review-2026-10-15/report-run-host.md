# run.py after world.lth's new Host (2ac8f12, 44578c4). Report

2026-10-15, Claude Opus 5.5, an agent of the coordinating session, on `prompt-run-host.md` of this
folder, and on the coordinator's addendum (certify.py's `refuse` after C5, 262d3d3 and 82c4cb4).
Inputs: `report-fix-host.md` (its list "What run.py's first-action validation must change, one line
per law" is followed item by item below), world.lth §4-§5 and world_model.lut at 5d39c6d, run.py at
5d39c6d (`FirstActions`, `_Theories.action_law`, `disagreement`, `certification`),
`report-fix-certification.md` ("certify.py and C5") and certification_model.lut's `refuseLaws` at
82c4cb4. Commit: 10fa2e2 plot.lth. Left uncommitted for the coordinator: `src/luthier/run.py`,
`src/luthier/certify.py`, `tests/test_run.py`, `tests/test_certify.py`,
`tests/run/first_action_models.lut`, `tests/run/first_action_noisy.lut` (new),
`tests/run/lying_host.py`, `tests/tester/world_laws.lut` (one comment), and the store
`src/luthier/lib/world_model.cert.json`. `belief_model.cert.json` is modified in the tree by another
agent's certification of `QuadraticConverges`, not by this work. `examples/luthier.lock` is the
lock the acceptance run of hello.lut wrote (untracked).

## Accepted when

- `PYTHONPATH=src python3 -m pytest tests -q`: 696 passed, 5 skipped, 9 xfailed. Midway, three
  tests failed on `QuadraticConverges` stale (optimization.lth changed at ffc7d31, its store not yet
  re-certified); they pass since another agent's re-certification landed in the tree.
- `luthier run examples/hello.lut`: prints `hello, world` twice over; the first run's record has
  `HostAgreesPrint` and `HostChangesOnlyDeclared` confirmed, the second has both served.
- The lying host: `first_action_liar.lut` is refused with "liar.print disagrees with its description
  at its first action (10.S10, L11.2): HostAgreesPrint at s = "twice": the place stdout differs
  (described just "twice\n", observed just "twice\ntwice\n")" (the test unchanged, and by the CLI).
- `luthier check src/luthier/lib/plot.lth`: clean (also plot_model.lut, tests/tester/plot_laws.lut).
- `world_model.cert.json`: `luthier certify tests/tester/world_laws.lut` reports the four `Console`
  laws known (their cones did not change), so the store was restored to HEAD and certify added
  nothing; the `Host` laws over cases cannot be certified that way (a drawn case is no observation,
  world.lth §5), so their current entries are the ones the two runs of hello.lut wrote. The old
  `HostAgrees*` entries stay, stale against the new cones (12.S11).

## What changed, per law of `Host`

- `HostAgreesPrint`, `HostAgreesReadFile`, `HostObserveChangesNothing`: `_Theories.action_law`
  recognizes a law by its one parameter typed `Observed` (was: a `W` parameter); the model, the
  action's arguments between model and case, and the one action field the body projects as before.
  At the first application, `FirstActions` takes the `held S A m act d` application from the law's
  body (`_held_parts`, the law's parameters but the case substituted with the run's values), applies
  `agreement S A m o (held ...) extra w` (the `agreement` of the file that declares the theory,
  `_protocol`), evaluates the law at the case, and hands the program `(w3, c.result)`: the action is
  applied once, inside the protocol. For `readFile` at `console.stdout` the law is true by its
  premise and the case still gives the program its result.
- `HostChangesOnlyDeclared`: recognized as a frame law (`_Theories.frame_law`: an `Observed`
  parameter, a `Held` one, one more for the certifier's places, no action projected). It is run on
  the case of every first action validated, `h` the held of that case, its `A` the held's result
  type. Refuted, the run is refused naming each undeclared place that differs before and after.
  Each first action now writes two entries (the action's law and the frame law), both with the
  places added in their binding, and is served only when both serve.
- `extra` [proposed]: the model's `console.stdout` and the files the run has read so far
  (`host.files_read()`), in that order, each once. At hello's first `print` it is `["stdout"]`, which
  the action declares, so the frame law is vacuous there; it bites on a `readFile`, where the
  standard output is undeclared. A new test does that: `noisy.readFile` (tests/run/lying_host.py,
  `read_and_print`) agrees with its description at the path and prints a line, and is refused by
  `HostChangesOnlyDeclared` "at p = "input.txt": the place stdout differs (before just "", after
  just "noise\n")".
- `ObserverIsFaithful`: see the next section.
- `disagreement`: reads `m` and `d` from the `held` application, and the case's `before`, `after`,
  `result`; compares at `d.places` by `m.read`, then the result. For an observation (`observes` in
  the body) it compares the result and the world after with the world before, at the places.
- `certification()`: laws over a case (action or frame) are not demanded of the store before the
  run; the state's `at first action` items name their `frame` law.
- plot.lth `renderAgrees` (10fa2e2): takes `extra`, builds `held S Unit m (fn w { r.render w p
  (pathOf stem ext) }) (drawn S r.drawing p stem ext)`, gives `W * Observed S Unit`; the import of
  world.lth adds `Observed held`. Nothing applies `renderAgrees` today.
- tests/run/first_action_models.lut: `honest` and `liar` carry `console := console`; `noisy` added.

## The default price of the observer [proposed, Luciano to mark]

Touches 6.S10 (the demand prices assumptions) and P11 (every criterion is a parameter), in the
direction of fewer flags on every run; assumes that the observer's fidelity is the one axiom every
host program shares. `run`'s demand gets a cutoff for laws whose body is an axiom (`Demand.axioms`,
default `AXIOMS = "AssumedGrade"` in run.py); such a law (`_Theories.axiom_of`, following the body's
head through definitions to `axiom "..."`) is demanded at the weaker of `--accept` and that cutoff.
When the cutoff is assumed and no entry serves it, the law is accepted as the assumption it states
and listed in the run's record under `certification.assumed` (name, law, the axiom's statement, the
grade accepted), so that the certificate says under what hypothesis it holds (10.S13). An entry that
serves (a citation, 6.S9) still serves. The other laws keep the `--accept` cutoff (sampled by
default). This is the price "accepted" by default for the observer.

A conflict left open: the cutoff is a field of run.py's `Demand` and not yet of demand.lth's
`Demand` nor of demand_model.lut's `theDemand` (outside this brief's files), so `DEMAND_DEFAULTS`
does not hold it and `demand.record` does not show it; the run's record shows it only through
`assumed`. It should be declared there before Luciano marks it.

## The addendum: certify.py's `refuse` after C5

`certify.refuse` now looks first for a failure of the law at the demand's hash (`at`, so the model's
fingerprint counts too) and refuses the law with state `("Current", that failure's outcome)`
whatever serves; `show_refusal` prints "failed at ...". `_failed` is certification.lth's
`isFailure` (`Failed`, not `NotRunFor`). New test `test_a_current_failure_is_refused_whatever_serves`
(tests/test_certify.py): a passed, serving entry (seed 1) in front of a failure of the same law and
hash (seed 2) is refused with the failure; the failure at another hash leaves the pass serving.
`test_the_refusal_is_per_law_and_says_why` passes unchanged.

Also in tests/test_certify.py: `test_an_import_beside_a_library_name_leaves_its_cone` failed at HEAD
since world.lth imports term.lth (2ac8f12), which loads grammar.lth with its own `RoundTrip` and
`Canonical`; tables.lth's are then `RoundTrip@tables`. The test now takes Codec's laws by the names
the loader gives them (`Loaded.internal`); what it asserts is unchanged.

## Decisions of my own

- A first action writes one entry per law (the action's law and the frame law), each with its own
  cone; the frame law's binding names the held action as `"honest.print at s = "once""`.
- `extra` as above, recorded in each entry's binding and reach, so a run that has read other files
  validates again.
- The frame law used is the first of the theory's, by the order written; a theory with none
  validates the action's law alone.
- `agreement` is found in the file that declares the theory (`_protocol`); the type names
  `Observed` and `Held` are read by name, as `W` and `agreement` were before.
- `test_run.py` expectations updated for the two entries and the `assumed` list; the hello test now
  also asserts the frame law and the assumed observer.
- I did not log the observer's default in record/decisions.md; it is the coordinator's to log when
  Luciano marks it.
