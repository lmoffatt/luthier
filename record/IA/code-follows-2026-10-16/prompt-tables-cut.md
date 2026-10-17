# Brief: tables' Maybe, failures never accepted by a cutoff, run records, and cut runs (step 3h)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-h (items 8, 14, 16) and
D-2026-10-16-c (`--accept assumed:NAME`); `record/plan/code-follows-principles-2026-10-16.md` (3g',
the cut run); `src/luthier/tables.py`, `src/luthier/lib/tables.lth`, `tables_model.lut`,
`tests/tester/tables_laws.test.lut` (the law `CellsOfTheirKind`, refuted today);
`src/luthier/lib/certification.lth` (`OnlyAPassServes`, cutoffs), `src/luthier/run.py`,
`src/luthier/cli.py`; spec 6.S15, 12.S18, 3.S21 or wherever the bridge reads `Maybe`.

Build:
1. Item 14: tables.py returns the host's `Just x` or `nothing` where a `Maybe` is declared (the
   bridge strict, `--checked` refusing a bare value); re-certify the table cones (`luthier certify`
   on tables' `.test.lut` files) and say whether `CellsOfTheirKind` now holds; if it still fails,
   say why with the counterexample.
2. Item 16: no cutoff accepts a failure (the top); running past a refuted law means naming it,
   `--accept assumed:LAW`, the grade `assumed` recorded with the names downstream, a warning on
   stderr. State it in certification.lth with its control (a cutoff that accepts a failure refuted).
3. Item 8: `.gitignore` tracks the records (`*.run.json`, `*.results.json`) of `.run.lut` files under
   examples/ and ignores those under tests/.
4. The cut run: a run stopped by its time limit or its fuel appends a record marked as not finished,
   with its demand, the steps reached and the reason; it writes nothing to the result store and is
   never served.
5. Spec: text and status for what you did.
Tests: the strict `Maybe` (a bare value refused under `--checked`); a refuted law refusing a run and
accepted by `assumed:LAW` with its warning and grade; the control; a cut run's record; the
`.gitignore` lines (git check-ignore on a path under each).

Accepted when: `python -m pytest -q` passes in full (781 passed, 6 skipped, 9 xfailed before, plus
yours); `python3 scripts/check_spec.py` prints its known finding (03-kernel.md:190) and the counts;
`luthier certify` over tables' `.test.lut` files exits as you explain. Two-line commits ending with
"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", staged by path; another agent commits at
the same time in tests/tester/*controls* and the *_model.lut reference models (do not touch
certification.lth's §§ outside the cutoff, nor those files); retry on .git/index.lock. Report:
`record/IA/code-follows-2026-10-16/report-tables-cut.md`, by shell heredoc, committed.
