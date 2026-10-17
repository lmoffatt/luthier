# Brief: the evidence per region, in the code (3j, j2a)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-16-i and -j,
`record/principles-language.md` L9.16, and `record/IA/regions-2026-10-17/report-theory.md` whole
(the theory just written; its section 5 is your list). The coordinator's answer to its question:
an empty region caps a binding at `Sampled` (as built; [proposed]); a stricter demand chooses
another combination.

Build items 1, 2, 3, 4, 6, 7, 9 and 10 of that section 5 (special values and the atom at zero;
dimension lists and the zero and rank-deficient families; classify by `casesOf`; the law's regions
from its signature; (region, n) in the entry; the grade as `regionedGrade` with the demand's
combination as a field of `Demand`, weakest by default; labels recorded, never graded; census
values checked against the parameter's predicate). Leave items 5 (branch coverage) and 8 (`cover`)
for the next bite, and say so in the report.

The grades of existing certificates may fall (a law whose degenerate regions were never drawn caps
at Sampled): re-certify the library's `.test.lut` files and list, law by law, every grade that
changed, before and after, with the empty region that caused it. A fall is the point of the
decision, not a failure; a law refuted in a newly drawn region is a finding: report it with its
counterexample, do not weaken the law.

Accepted when: `python -m pytest -q` passes in full (799 passed, 6 skipped, 9 xfailed before, plus
yours); `python3 scripts/check_spec.py` prints its known finding (03-kernel.md:190) and the counts;
`luthier certify` over every `tests/tester/*.test.lut` exits with every line known after your
re-certification, or lists the findings; the spec (7.S4, 7.S5, 7.S9, 7.S14, 5.S8) says what is now
implemented. Two-line commits ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
staged by path; another agent edits tests/test_session.py, test_modes.py, test_run.py,
test_result_store.py and test_tables_cut.py at the same time (do not touch those), retry on
.git/index.lock. Report: `record/IA/regions-2026-10-17/report-code.md`, by shell heredoc, committed.
