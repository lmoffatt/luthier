# Brief: the core's bite 4, typing for resolution

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` sections 0, 2 (rule 2.2 and
its parts) and 6 (bite 4), `decisions.md` beside it, and `record/decisions.md` at D-2026-10-18-a,
-b, -c (the core alone; names per concept resolved by the model the type names; the three planes).
Build bite 4 exactly as section 6 describes it. Part (c)'s filling of an omitted structure parameter
from the table (2.2.2) follows question 4's recommendation, which Luciano has not answered yet:
build it in its own commit so it can be undone alone.

Where `infer` now raises on a library file, fix the library's annotation if the error is the
library's, and list each such fix in the report; if a fix would change a law's meaning, stop and
report it instead.

Accepted when: everything section 6 lists for bite 4; `python -m pytest -q` passes in full (run it
in the background; the count before is in execution.md's Status or the last report, plus yours);
`python3 scripts/check_spec.py` prints its known finding; `python3 scripts/core_metrics.py` runs and
its counts go in the commit message of your last code commit. You are the only agent in code.
Two-line commits (subject, blank line, body) ending with "Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>", small, staged by path. Report: `record/plan/core-2026-10-17/report-bite-4.md`,
by shell heredoc, committed.
