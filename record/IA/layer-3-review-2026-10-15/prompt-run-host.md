# run.py follows world.lth's new Host (2ac8f12, 44578c4), brief for an Opus agent

The suite is red: world.lth's `Host` laws are now predicates over an `Observed` case and
`agreement` returns `W * Observed`; run.py's first-action validation still expects the old
shape, so hello.lut is refused. Read `CLAUDE.md`, then `report-fix-host.md` in this folder
(its section "What run.py must change, one line per law" is this brief's list, and its
"Beyond run.py" names plot.lth 562 `renderAgrees` and `tests/run/first_action_models.lut`),
then world.lth §4-§5 and world_model.lut as they are, and run.py's `FirstActions`,
`_Theories.action_law`, `disagreement`, `certification`.

Change `src/luthier/run.py`, `tests/test_run.py`, `tests/run/first_action_models.lut`, and
`src/luthier/lib/plot.lth` at `renderAgrees` only (one commit of plot.lth by its path, message
ending "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"). `ObserverIsFaithful` is an
assumed law: a run accepts it with no entry only under the demand's `--accept assumed`; since
every program with a host would then need that flag, make the default demand of `run` accept
assumed entries for laws whose body is an `axiom` and say so in the record and in the report
([proposed], 6.S10: the demand prices assumptions; this is the price "accepted" by default for
the observer, Luciano to mark). Regenerate `src/luthier/lib/world_model.cert.json` by
`luthier certify tests/tester/world_laws.lut` (adapt world_laws.lut to the new names if needed).

Write your report with a shell heredoc to `report-run-host.md` in this folder and commit it
alone. Accepted when: `PYTHONPATH=src python3 -m pytest tests -q` passes; `luthier run
examples/hello.lut` prints `hello, world` (first run validates print, second serves it); the
lying host is still refused naming the place; `luthier check src/luthier/lib/plot.lth` clean.
The Python, tests and store stay uncommitted for the coordinator.
