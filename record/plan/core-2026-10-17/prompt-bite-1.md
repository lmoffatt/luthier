# Brief: the core's bite 1, the code fixes and the directory

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` sections 1, 6 (bite 1 and
its additions) and 8, `report-bite-2.md` beside it (bite 2 landed: its three files import `Object`
from kernel_laws.lth, which this bite repoints), and `record/decisions.md` at D-2026-10-15-e (the
hash erases binder annotations) and D-2026-10-15-i (the interpreter's revision by stage).

Build bite 1 exactly as section 6 and its additions describe: the hash's erasure with its law and
control; the census fingerprint over members built by an expression; the drawing code (tester.py's
sampling, generators.py) in a sampled entry's identity; certify's fuel default read against
PinvProjects (derived or raised, never an unrecorded constant, P11); the moves into lib/core/
without renaming any law, every import repointed (bite 2's three files included); the stores moved
with their files; then one full re-certification of `tests/tester/*.test.lut` (run it in the
background; the last one took over three hours with --deep: do it without --deep, with the fuel the
lines need). A law refuted in that wave is a finding: report it, do not weaken it.

Accepted when, besides the common criteria of section 6: the erasure law exists with a refuted
control; a census built by an expression changes its fingerprint when its members change (a test);
every store entry is at its new cone hash (count before and after); `luthier certify` over every
`tests/tester/*.test.lut` reports every line known after the wave, or lists the findings;
`python -m pytest -q` passes in full (813 passed, 6 skipped, 9 xfailed before, plus yours; run in
the background); `python3 scripts/check_spec.py` prints its known finding (03-kernel.md:190);
`luthier run examples/sonolocalizacion/experiment_zero.run.lut` with the `--set` values of its last
record passes the certification check and runs (stop it with `--time-limit 120` and say what the
record shows; the whole fit is not required). You are the only agent in code, theories, the spec and
the stores. Small two-line commits (subject, blank line, body) ending with "Co-Authored-By: Claude
Opus 5.5 <noreply@anthropic.com>", the moves apart from the edits. Report:
`record/plan/core-2026-10-17/report-bite-1.md`, by shell heredoc, committed.
