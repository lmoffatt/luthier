# kernel.py, bite 8: `==` demands its parts, report

Claude Sonnet 5.5, 2026-10-14, for prompt-8.md. Source: term.lth §5 at 924df6b (`EqualityDemandsParts`). Changed `src/luthier/kernel.py` and `tests/test_kernel.py`; not committed.

kernel.py: new `_demand_parts`. In `==`, after the left operand is in weak head normal form and comparable, the step reduces in place, in this order: the left operand's parts (a pair's first then second part, a record value's fields in order, recursively), then the right operand, then the right operand's parts; only then does it compare. A part that cannot step (hole, lambda, extern, declared name) is passed over, so a later part still steps, and `==` stays stuck when no part steps (`EqualityStuck` unchanged).

Reading where the law is silent: parts inside injections and constructor arguments (lists) are not demanded, since the law names pairs, the right operand and record values; `==` on them stays stuck as in bite 7.

Tests: `test_equality_demands_parts` (each of the three cases, a defined name as part, leftmost order, stuck parts, runs to true/false), `test_agreement_comparison_steps` (`describe 3 == (after, x)` with `describe` returning a pair of redexes reduces to true/false). Two bite-7 stuck assertions (a pair with `1 + 1`, a pair with a defined name) now step and were removed from the stuck test; the rest is kept.

Checks: `tests/test_kernel.py tests/test_run.py` 76 passed; full suite: 448 passed, 7 xfailed in 100.45s (0:01:40)
