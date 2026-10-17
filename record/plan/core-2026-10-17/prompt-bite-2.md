# Brief: the core's bite 2, the properties

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` sections 1, 2, 3.1 to 3.3, 6
(bite 2) and 8, and `record/decisions.md` at D-2026-10-17-b, -c, -d, -f (the within-bound versions).
Build bite 2 exactly as section 6 describes it: the three files under `src/luthier/lib/core/properties/`
and the two test programs, each property with a confirmed instance and a refuted control (L9.14).
If a signature of section 3 does not check, fix it and say how in your report; do not change the
names D-2026-10-17-c fixes.

Accepted when: `luthier check` is clean on the three files; `luthier certify` on the two test
programs grades every property and refutes every control; `python -m pytest -q` passes in full
(run it in the background, it takes over 15 minutes; 799 passed before plus any the other agent
adds); `python3 scripts/check_spec.py` prints its known finding (03-kernel.md:190). Another agent
works in tester.py, certify.py, generators.py, the spec and the stores now: touch none of those.
Two-line commits (subject, blank line, body) ending with "Co-Authored-By: Claude Fable 5.1
<noreply@anthropic.com>", staged by path; retry on .git/index.lock. Report:
`record/plan/core-2026-10-17/report-bite-2.md`, by shell heredoc, committed.
