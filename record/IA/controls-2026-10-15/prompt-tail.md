# The tail of the controls work, brief for an Opus agent

Read `CLAUDE.md`, `report-weak-laws.md` and `report-mutants.md` in this folder and
`record/IA/statistical-2026-10-15/report-tester.md` ("Findings"). Nobody else edits now.
1. `PinvScales` (arrays.lth) has `RankScales`' weakness (an invariance under scale sees only
   scales near one): strengthen it as 15caf52 did, with a control that the old law missed.
2. `UniformSampleIsUniform` (generators_model.lut) takes its source as a parameter so
   `SkewedSampleIsUniform` becomes its control line (one cone), and drop the duplicate of the
   `SourceIsUniform` line if both compute the same thing (say).
3. `tests/conftest.py` restores the library stores after each test, so a suite run concurrent
   with `certify` reverts certify's writes: make the restore touch only stores a test changed
   (compare to a snapshot taken by that test), or make tests write to a temporary copy of the
   library stores; a test that a store written by another process during the suite survives.
4. Re-certify with stores, alone (no suite running): `luthier certify` on arrays, generators and
   probability `_laws.lut` and `_controls.lut` (--jobs 2, --fuel 100000000); commit
   `src/luthier/lib/{arrays,generators,probability}_model.cert.json` (each alone, derived); delete
   the stray untracked `src/luthier/lib/probability.cert.json` (a store written by a tester bug,
   fixed at f0f09d7; nothing reads it).
Commit theory and .lut files each alone by path; conftest.py and the stores too; report with a
shell heredoc to `report-tail.md` here, committed alone. Accepted when: the suite passes (run
after certify, not during); `certify` lists PinvScales and UniformSampleIsUniform controlled and
no CONTROL FAILED; `git status` clean but `time_opus_low.txt`.
