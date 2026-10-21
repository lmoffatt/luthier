# Brief: the core's bite 8, numbers.lth and algebra.lth over the core

Read `CLAUDE.md` first, then `record/plan/core-2026-10-17/execution.md` sections 0, 4 (Metric,
bounds and the within-bound claims of numbers.lth), 6 (bite 8) and the paragraphs of 2026-10-18;
`report-bite-6.md` beside it (its mathematical findings: the quantale's orientation, MetricInteger,
the bounded Float64 claims); `record/decisions.md` at D-2026-10-17-f (Metric; every equational
property with a within-bound version; Doubles associative within a bound, Higham), D-2026-10-18-b,
D-2026-10-18-j (numerical laws relate input and output tolerances with the theory's bound and state
their range of validity), D-2026-10-21-a (`+` only for commutative additive structures).

Build bite 8 as section 6 describes it. The bounds are the theory's, never tuned to pass: if a bound
section 4 gives is refuted, that is a finding to report with its counterexample, not a bound to
widen. Each within-bound law gets its two controls (an op that rounds to a coarser grid; a bound
too small on the real doubles, which tells gamma2 from 3 gamma2) and states its range of validity as
a premise (D-2026-10-18-j). Remove the CORE_COLLISIONS entries bite 8 owns (numbers and algebra).

Accepted when: section 6's criteria for bite 8; `python -m pytest -q` passes in full; `python3
scripts/check_spec.py` prints only its known finding; `luthier certify` over every
`tests/tester/*.test.lut` prints 0 lines ran for every non-fixture program after your wave;
`python3 scripts/core_metrics.py` counts in the report. Another agent works on bite 7 at the same time
in lib/core/lists.lut, core.lut, grammar.lth, the parser and the string uses of `+`: touch none of
those, and retry a commit that fails on .git/index.lock. Small commits: a subject, a blank line, one
body line, ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", staged by path.
Report: `record/plan/core-2026-10-17/report-bite-8.md`: what you built, the checks' output, the
lines re-certified, core_metrics before and after, the bounds confirmed or refuted, decisions taken
on your own, at most one question.
