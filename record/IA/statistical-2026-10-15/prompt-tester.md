# The sequential tester (D-2026-10-15-b, L9.15), brief for an Opus agent

Read `CLAUDE.md`, then `report-theory.md` in this folder (its last section, "Tester, one line
per definition", is this brief's list), laws.lth §4, generators.lth §1, probability.lth §5 and
the two models as committed (2d4519e to 1283a12), `record/IA/controls-2026-10-15/report-tester.md`
(controls), and `src/luthier/tester.py`, `certify.py`. Another agent writes `*_controls.lut`
under tests/tester and binds `budget` in belief_laws.lut and fit_laws.lut: do not touch those.

Do the list: a `Statistical` law at its bindings runs Wald's `sequential` through the Runner
with the spec's seed and the `Sequential` cutoffs bound as a census of one (never drawn);
`Tested v` is the entry's evidence with alpha, beta, delta and spent recorded; the grade by
`StatisticalByTest`; a statistical control (`control <- true`) passes on `Fails`; rewrite
`probability_laws.lut`'s `UniformAtLevel` lines and `generators_laws.lut`'s
`UniformSampleIsUniform` line with `c` bound (alpha 0.01, beta 0.01, delta 0.5, initial and
budget your call, recorded), add the two controls (`SkewedSampleIsUniform`, `LumpIsUniform`)
in the controls files of those two programs, and drop `Level` from the importers if nothing
else needs it (say). Change tester.py, certify.py, tests/test_tester.py, tests/test_certify.py,
the two `_laws.lut` and their `_controls.lut`; commit the .lut files each alone; the Python
uncommitted. Report with a shell heredoc to `report-tester.md` here, committed alone.
Accepted when: the suite passes; `luthier certify tests/tester/generators_laws.lut
tests/tester/generators_controls.lut tests/tester/probability_laws.lut
tests/tester/probability_controls.lut --no-cert --fuel 100000000` shows the uniform laws
Supported (Sampled) with spent and rates, the two controls refuted; paste those lines.
