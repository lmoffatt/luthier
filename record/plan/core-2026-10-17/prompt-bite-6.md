# Brief: the core's bite 6, the structures and core's claims

Read `CLAUDE.md` first (the repository's working rules; you are a Codex agent, so where it says
Claude, read the agent). Then `record/plan/core-2026-10-17/execution.md`: section 0 (the core's end),
sections 2 and 3 (the forms and the files), section 6 bite 6, the paragraphs of 2026-10-18 (his
answers; the frame of the three planes; Quantale; after bite 5: the collisions list and chapter 7's
leftovers); and `report-bite-2.md`, `report-bite-4b.md`, `report-bite-5.md` beside it. In
`record/decisions.md`: D-2026-10-17-b to -g, D-2026-10-18-a to -c, -f, -g, -i.

Build bite 6 as section 6 describes it, with these decided changes:
1. Bare form (D-2026-10-18-f): structures and composite properties are conjunctions of properties
   (`Monoid = Associative & Neutral`), no one-line wrapper per law; bite 4b's tester splits them.
   Rewrite bite 2's composites (Equivalence, Preorder, PartialOrder, TotalOrder, StrictOrder,
   Isomorphism, Bijective) to the bare form.
2. The three planes (D-2026-10-18-c): structures only declare and state laws with their mathematical
   references; nothing that computes goes into a theory file.
3. Declarations of D-2026-10-18-i: `Quantale` in structures (the base of the levels of equivalence),
   with its four models named in comments (error [0, inf] with + and <=; uncertainty, distribution
   functions with a t-norm; evidence [0, 1] with + or max; resources, + in sequence and max in
   parallel); `NonExpansive` and `Lipschitz` in properties/functions.lth beside `Monotone`.
4. Beside `Metric`: the tolerance relation a threshold on a metric gives (reflexive, symmetric, not
   transitive; an equivalence only for an ultrametric), a t-norm, and the probabilistic metric
   (Menger), declared with laws and controls, no model yet [proposed, his question 2 of the
   three-levels report is open].
5. The seven names two core files define leave run.py's `CORE_COLLISIONS` (one definition each).
6. Chapter 7's remaining "metric" for placement (opening list, table of modes, three rows of the
   generators table, 7.S20) reworded to "placement".

Every law gets a control that refutes it (L9.14). Re-certify what moves (`luthier certify` over the
touched test programs, then over every `tests/tester/*.test.lut`, without --deep); a refuted law is a
finding to report, never weakened.

Accepted when: section 6's criteria for bite 6; `python -m pytest -q` passes in full (862 passed, 6
skipped, 9 xfailed before, plus yours); `python3 scripts/check_spec.py` prints only its known finding
(03-kernel.md:190); `luthier certify` over every `tests/tester/*.test.lut` prints 0 lines ran for
every non-fixture program after the wave; `python3 scripts/core_metrics.py` counts in the last commit.
Small commits: subject, blank line, one body line, ending with "Co-Authored-By: Codex
<noreply@openai.com>", staged by path. Leave untracked files you did not create alone. Report:
`record/plan/core-2026-10-17/report-bite-6.md`: what you built, the checks' output, the lines
re-certified, core_metrics before and after, decisions you took on your own, at most one question.
