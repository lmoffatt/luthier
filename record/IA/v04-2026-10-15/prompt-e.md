# v0.4 criterion (e): step 6's theories with their laws controlled (L9.14), brief for an Opus agent

Read `CLAUDE.md`, step 6.3 of the execution plan (criterion e: 142 of 148 law lines controlled;
world.lth has lines only for `Console`'s four laws; demand.lth and plan.lth have none; the six
uncontrolled in `sonolocalizacion_laws.lut`), `record/IA/controls-2026-10-15/report-mutants.md`
and `report-tail.md` (how controls are written and certified), `tests/tester/world_laws.lut`
and `plan_model.lut`'s `example`. Write `tests/tester/{world,demand,plan,sonolocalizacion}_laws.lut`
lines for every law of world.lth (the `Host` laws over listed `Observed` cases; `Described`,
`Externs`, `Crossing` with listed models), demand.lth, plan.lth (`Dataflow`, `Planning`,
`Keying` where a model exists), and a control line for each in a sibling `_controls.lut` (a
model broken on purpose the law refutes; a law no wrong model can reach without a new
definition gets a line in the report saying why). Touch no theory file; if a law turns out too
weak (CONTROL FAILED), report it as a finding. Commit each .lut alone by path; run `luthier
certify` on the new files with stores, alone (no suite during it), and commit the model stores
that changed (each alone); report with a shell heredoc to `report-e.md` here, committed alone.
Accepted when: `certify` on all `tests/tester/*_laws.lut` and `*_controls.lut` lists every law
controlled or uncontrolled with a reason in the report; no CONTROL FAILED unexplained; the suite
passes, run after.
