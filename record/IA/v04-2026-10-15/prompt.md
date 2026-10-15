# v0.4: its criteria written first, then `luthier eval` as 12.S19 reads it, brief for an Opus agent

Read `CLAUDE.md`, the execution plan `record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md`
(step 5.5's criteria for v0.3 as the form; step 6's "Planned" list; "After"), and Luciano's rule
that a milestone's criteria precede its work (the memory note is reflected in that step 5.5 text).
1. Write step 6.3, v0.4's criteria, in the form of v0.3's (a, b, c...: each measurable by a
   command and an expected line): `eval` and `session` as 12.S19 and 2.S18 read them; the result
   store across runs (8.S3, 8.S8) at its smallest; the layer 3 external review applied (met);
   step 6's theories each with its laws controlled (L9.14); the suite and lints. Mark which are
   met now. Commit the plan alone ("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>").
2. Then the first unmet one that needs no decision of Luciano's: `luthier eval` (12.S19) loading
   imports as `run` does (today it does not: several reports say `eval` stops at weak head
   form on imported names), recording nothing (12.S19: eval is the probe that records nothing),
   no certification demanded (say what 12.S19 says on that and follow it). Change
   `src/luthier/cli.py`, `src/luthier/run.py` (reuse `Loaded`), `tests/test_*.py` as needed; the
   Python uncommitted.
Report with a shell heredoc to `report.md` here, committed alone. Accepted when: the plan has
6.3 with each criterion's state; `PYTHONPATH=src python3 -m luthier.cli eval` on a file importing
plan_model.lut evaluates `agree` to `true`; the suite passes.
