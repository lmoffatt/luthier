# Brief: the core's bite 4b, the tester splits a conjunction of laws

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-18-f (question 3: no one-line
wrappers per law and structure; the tester first learns to split a conjunction of laws into its
conjuncts, each a partially applied law with its missing variables quantified on its own; then the
structures and composite properties are written bare) and D-2026-10-18-a (the core's end);
`record/plan/core-2026-10-17/execution.md` sections 0, 2 and the 2026-10-18 answers;
`report-bite-2.md` (why the composites could not be a `&`: the kernel does not reduce the `&` of
partially applied laws); `report-budgets.md` (its question on the classifier's bounds);
`src/luthier/tester.py`, `src/luthier/run.py`'s enumeration of a theory's laws, `certification.lth`
(how a claim's grade combines, 5.S8, the weakest by default).

Build:
1. A law whose body is a conjunction (`&`) of partially applied laws is split by the tester into its
   conjuncts; each conjunct is tested as a law of its own, its missing variables quantified
   independently by the generators of their types (bindings by name as today, 7.R1, G6); the
   conjunction's grade is the demand's combination of the conjuncts' grades, the weakest by default;
   each conjunct has its entry, and a control refutes the conjunction when it refutes one conjunct.
   If the elaborator must change for this (elaborate.py is another agent's now), stop and report
   what it needs.
2. The classifier's bounds (`numbers` reads at most 4,000 doubles, `_MOST_ENTRIES` 400) become fields
   of `Budgets` with declared defaults (P11), as the budgets bite did for fuel.
3. Tests: a conjunction of two properties with different variables (bite 2's `Equivalence` written
   bare in a test program) is split and graded; a control that breaks one conjunct refutes it; the
   classifier bounds read from a line's budgets.
4. Spec: 7.S-text and status for what you did.
Then re-certify what changes (one wave, without --deep), and report the lines that ran.

Accepted when: the tests pass; `python -m pytest -q` passes in full (829 passed, 6 skipped, 9
xfailed before, plus yours; in the background); `python3 scripts/check_spec.py` prints its known
finding; `luthier certify` over every `tests/tester/*.test.lut` reports every non-fixture line known
after the wave, with no law refuted (a refutation is a finding: report it, do not weaken the law);
`python3 scripts/core_metrics.py`'s counts in the last code commit's message. Another agent works in
elaborate.py, check.py, run.py's loader and tests/spec now: touch none of those. Two-line commits
(subject, blank line, body) ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
small, staged by path; retry on .git/index.lock. Report: `record/plan/core-2026-10-17/report-bite-4b.md`,
by shell heredoc, committed.
