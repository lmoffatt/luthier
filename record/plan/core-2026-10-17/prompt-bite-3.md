# Brief: the core's bite 3, the metrics script

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` section 0 (the core's end,
D-2026-10-18-a) and section 6, bite 3. Build bite 3 exactly as written there: `scripts/core_metrics.py`
and `tests/test_core_metrics.py`. The accepted homonyms list starts empty unless a homonym is
required by the language (say each with its reason).

Accepted when: the script runs in under a minute over the library; its four counts at the commit you
start from are in its header and in execution.md's Status line; the test checks each count on a
fixture of three small files; `python -m pytest -q tests/test_core_metrics.py` passes. Another agent
works in tester.py, certify.py, generators.lth and test.lth now: touch none of those. Two-line
commits (subject, blank line, body) ending with "Co-Authored-By: Claude Sonnet 5.5
<noreply@anthropic.com>", staged by path; retry on .git/index.lock. Final message: the hashes and the
four counts with their top five entries each.
