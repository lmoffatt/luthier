# Brief: a control for every uncontrolled law (L9.14)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-15-a (every law carries a model it
refutes) and `record/principles-language.md` L9.14; look at two existing controls first:
`tests/tester/certification_controls.test.lut` and `tests/tester/pooling_controls.test.lut`, and
their reference models in `src/luthier/lib/certification_model.lut`.

Task: run `luthier check -v` over every `tests/tester/*_laws.test.lut` with its `*_controls.test.lut`
and list each law reported uncontrolled. For each, except those in tables (another agent works there
now), write a control: a model broken on purpose so that the law fails on it (one wrong behavior,
the smallest), in the theory's reference model file, and a `control` line in the matching
`*_controls.test.lut`. Known today: `ANewIdentityGoesInFront`, `AnAgreeingReplayAddsNothing`,
`AnAgreeingPairSettles` (certification), and others `certify` lists. If a law cannot be failed by any
model you can build, do not force it: say so, it is a finding against the theory (L9.14).
Then `luthier certify` the files you touched.

Accepted when: `luthier check -v` lists no uncontrolled law outside tables, except those you report
as findings with the reason; `python -m pytest -q` passes in full (781 passed before, plus none
removed); the stores you touched are committed. Two-line commits ending with "Co-Authored-By: Claude
Sonnet 5.5 <noreply@anthropic.com>", staged by path; another agent commits at the same time in
tables, run.py, cli.py, .gitignore and certification.lth's cutoff (do not touch those); retry on
.git/index.lock. Report: `record/IA/code-follows-2026-10-16/report-controls.md`, by shell heredoc,
committed: each law, its control, and the findings.
