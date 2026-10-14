# A host action validated at its first action (10.S10, L11.2): report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-first-action.md; saved by the
coordinator. Commits by the agent: 2727b41 world.lth (`Host` a theory), 08d9548 world_model.lut
(the `Described` values, the `host` model), 9c3684b (a premise on `ReadGivesThePlace`),
33d1d48 (a binder renamed). Committed by the coordinator: `src/luthier/run.py`,
`tests/test_run.py`, `tests/conftest.py` (the library stores restored after each test),
`tests/tester/world_laws.lut`, `tests/run/{lying_host.py, first_action_models.lut,
first_action_honest.lut, first_action_liar.lut}`, the store `world_model.cert.json`. Checks:
test_run and test_certify 117 passed; the suite 652 passed; the slow tests pass (350 s).

## The laws (world.lth §5, [proposed])

`Host (S)` is a theory: `world`, `observe`, `print`, `readFile`, `printDescribed : String ->
Described S Unit world`, `readFileDescribed : String -> Described S (Maybe String) world`; laws
`HostAgreesPrint` and `HostAgreesReadFile` (the Bool of `agreement` on the described action
with the program's own arguments and the token) and `HostObserveChangesNothing` (two
observations at the same places read the same); `Host := ... & ... & ...`. The laws end in
Bool (4.R6); the observation law also meets 4.R3 (every field read). `appendStr` has a body
(`a + b`; review finding A12). world_model.lut: `printDescribed s` not own, places `["stdout"]`,
describes `console.printLine s`; `readFileDescribed p` not own, places `[p]`; `host` carries
both and `world := theWorld`. `ReadGivesThePlace` gained the premise `p == c.stdout or`
(refuted at `p = "stdout"` on the listed cases). Both files check clean.

## What run.py does

`_Theories.action_law` finds a law taking `W` (the model, the action's arguments, the one
action field the body projects). `certification()` leaves these laws out of the upfront
refusal and lists them "at first action" (the route, the law's cone hash, the model's cone
hash including `host_hash`). At the first application of that route (`FirstActions`): the
arguments shared; a demand built from the model and the run's own arguments; if an entry in a
loaded store serves it, the action is applied as usual; else the Runner evaluates the law
once, the action applied inside the law being the program's own application (so `print`
prints once). Refuted: `Refused`, naming the action, the law, the argument and each declared
place where the described and the observed worlds differ; no entry, no record. Confirmed:
`certify.add_entry` writes an entry to the model's file store (grade Cases, one case, the
binding the model with its cone hash and each argument as a one-value census) and the run's
record gets `certification["first actions"]`. Nested validation off during the law;
observations through `host.observe` with the token passed on.

Runs: hello, read_first_line, observe each confirmed at the first run and served at the
second, output unchanged; the lying host (prints twice) refused: "liar.print disagrees with its
description at its first action (10.S10, L11.2): HostAgreesPrint at s = "twice": the place
stdout differs (described just "twice\\n", observed just "twice\\ntwice\\n")".

## Decision for Luciano

Binding each entry to the run's arguments (7.S9) makes the model's store grow by one entry per
distinct argument of every action (the fit prints computed numbers), and an entry for `print
"0.3"` says little about `print "0.4"`. The agent's lean: validate once per hash of the model's
cone (host code included), the arguments kept as evidence and not as identity.

Readings and choices of the agent: the descriptions as fields of the `Host` model; one law per
action plus the observation law; the protocol's application is the program's (a refused run
shows nothing because stdout is buffered; a file write would already have happened); a refuted
law writes no entry; two models sharing a route: only the first validated; an action written in
Luthier skipped; `observe` validated only at the program's own first observe; `ok` renamed
`holds` (a core constructor matched as one: a checker gap); the test hygiene in conftest.py.
