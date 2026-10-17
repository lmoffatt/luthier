# Brief: what the principle of the three levels of equivalence changes, and whether it can be done

You explore and write one report; you change nothing else. Read `CLAUDE.md` first. Then, and keep
the reading bounded to what the report needs:
- `record/decisions.md` at D-2026-10-18-c (the three planes; the levels of equivalence as one
  structure enriched over a base: Bool with "and", [0, inf] with "+", distributions with a t-norm),
  D-2026-10-18-d (the budget scales with the bound), D-2026-10-18-h (this exploration, his words),
  D-2026-10-15-b (the sequential test), D-2026-10-16-i and -j (evidence per region), D-2026-10-17-f
  (Metric, within-bound properties), D-2026-10-14-c (Boolean first, cutoffs as parameters);
- `record/principles-language.md` L3, L5.17, L6, L9.14 to L9.17, L10, L13.5, O1 and O5 (the open
  algebra of costs);
- `docs/spec/06-certification.md` (6.S4 to 6.S16, the suspended cost parts), `07-tests.md` 7.S10 to
  7.S19, `09-planner.md` (its first screen), `11-*.md` (distances);
- the code only to locate where a change would land: `src/luthier/lib/certification.lth`, `laws.lth`,
  `test.lth`, `numbers.lth` (`approx...`), `src/luthier/tester.py`, `certify.py`, `run.py`'s serving;
  `record/plan/core-2026-10-17/execution.md` sections 2 and 3.5 (Metric in the new core).

The principle (his, D-2026-10-18-h): the three levels of equivalence (equivalence relation, metric,
probabilistic metric) are one structure over three bases, and that is the principle for costs and
for probability: a verdict is Boolean with a metric or probabilistic bound; the cost is computed and
the demand collapses it; the budget scales with the bound.

Check the literature before leaning on it (web search allowed; cite what you read, say what you
could not reach): quantitative equational theories (Mardare, Panangaden, Plotkin, LICS 2016: s =_eps t,
Kantorovich/Wasserstein and total variation as free algebras); Fuzz (Reed and Pierce, ICFP 2010) and
Duet (OOPSLA 2019) for the metric level; pRHL and EasyCrypt (Barthe et al.) for the probabilistic;
Lawvere 1973 (metric spaces as enriched categories) and Menger 1942 (statistical metrics). Say for
each what it gives Luthier and where Luthier differs (Luthier certifies by testing, not by proof).

Write `record/plan/three-levels-2026-10-18/report.md`:
1. One screen for Luciano first: what the principle changes, whether it is feasible, at what cost,
   and the one or two questions only he can answer (each with a recommendation). No menu.
2. Then, per area (principles, spec, theories, tester, certification, planner): what changes,
   concretely (the clauses, the laws, the functions by name), what is feasible now, what waits, and
   the cost in bites. Mark what comes from a source (cite it) and what you propose.
3. The order of work it implies, set against the core's plan (record/plan/core-2026-10-17/
   execution.md): which core bites it changes, which it leaves, and whether the core should absorb
   it now.
4. Conflicts with principles in force, if any, each in one sentence with what it would cost.

Accepted when the report exists and is committed alone, its first screen is under 60 lines, and every
claim about a paper names it. Two-line commit (subject, blank line, body) ending with
"Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>", staged by path. Another agent works in
tester.py, certify.py, generators.lth and test.lth: read them, do not edit. Final message: the hash,
and the first screen's questions in one line each.
