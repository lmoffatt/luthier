# A host action validated at its first action (10.S10, L11.2): agreement run by run.py, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). The naive review's strongest
finding (`record/IA/review-naive-2026-10-15/for-luciano.md`: `Host S` has no law, so hello.lut's
`print` runs with no validation; A16/B25, B2) and step 6.2 of the execution plan (externs
validated at their first action through `agreement`). Luciano on the provisional extern: it
stays refused (12.S17); this bite is about the validation of a described host action.

## The prompt

Read `CLAUDE.md` first, then that screen's class 5 and the two findings, `docs/spec/10-world.md`
10.S8 to 10.S10 (an extern read at the first demand, validated against its type's laws at its
first action, refused if refuted, provisional as debt), `src/luthier/lib/world.lth` §2 to §5
(`Described`, `own`, `places`, `ChangesOnlyDeclared`, `Externs`, `Crossing`, `agreement`,
`Host`), `world_model.lut` (`console`, `theWorld`, `host`, `HostConsole`), `src/luthier/run.py`
(`certification`, `TypedExtern`, how a host action is applied: `call`, the token), `host.py`
(`observe`), `src/luthier/certify.py` (the store, `record`), `certification.lth` §3. Nobody else
edits now: change `src/luthier/lib/world.lth` and `world_model.lut` (the theory side: one commit
each, [proposed], messages ending "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"),
`src/luthier/run.py`, `src/luthier/certify.py`, `tests/test_run.py`, programs under `tests/run/`.

1. Theory: `world_model.lut` builds the `Described` values the review found missing: `print`'s
   (not own, places `["stdout"]`, describe `console.printLine`) and `readFile p`'s (not own,
   places `[p]`, describe `console.readFile p`); `Host S` becomes a theory whose law is the
   agreement of each of its actions with its description (`HostAgrees`: for the chain of
   tokens the protocol threads, `agreement d host w args` holds), stated over the `Described`
   values, so that `host.print` has a law to be certified against (L11.2). Both files parse and
   `luthier check` clean.
2. run.py: a host action whose type's theory has the agreement law is validated at its first
   application in a run (10.S10): the Runner runs `agreement` once for that action (observe the
   declared places, act once, observe again, compare with the description's answer) with the
   run's own first arguments, before applying the action for the program; a refuted agreement
   refuses the run naming the action and the place that differed; a confirmed one is recorded
   as an entry of the action's law in the model file's store (`world_model.cert.json`, grade
   `cases`, the binding the run's arguments, 7.S9) and in the run's record, so a later run
   finds it served and does not re-run the protocol (7.S13) unless the host code's hash
   changed. The agreement's own observation reads the places through `host.observe` and must
   not count as a change (the token threads through it).
3. hello.lut, read_first_line.lut, observe.lut and the fit still run: the first run of each
   validates `print` (and `readFile`) and records it; the second finds it served. Tests: a host
   action whose description lies (a test host module that prints twice) is refused at the
   first action with the place named; the entry written and reused; the record carries the
   validation. The suite and the slow tests.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py tests/test_certify.py -q`, then the
suite. Do not commit the Python or the stores (the coordinator does). Report in your final
message: the laws stated, what the protocol does in run.py, every reading taken.
