# Brief: bites B1, B3 and D1, and the tester's assumed grade, in one agent

These four touch certify.py and tester.py, so one agent does them in order. B2 and C1 have landed
(report-B2.md, report-C1.md beside this file); Luciano's answers are D-2026-10-25-a, now in the
principles (L10.2, L10.3, L10.5, L10.8, L9.14).

1. B1 of `execution.md`: ε̂ at serve time, at the demand's δ, computed from the entry and stored
   nowhere new (L10.3); use B2's `EvidenceBound` and `cappedSumComposition` (core.lut) for the
   demand's evidence, the composition a parameter of the demand with the capped sum as default.
2. B3 of `execution.md`: the grade as the projection of (domain, cost) (L10.2), nothing served
   differently yet (the chain stays the admission until the cost types come, L10.5).
3. D1 of `execution.md`: a control per conjunct (L9.14): a control runs every conjunct; a theory is
   done when each conjunct has a refuted model; `check -v` lists the uncontrolled conjuncts. Run it
   over the tree and list in the report every conjunct that becomes uncontrolled (docs/concepts.md
   §7.1 expects six in the tape example).
4. The tester grades an axiom conjunct `AssumedGrade` with no cases, as run.py's `axioms` does
   (report-B2.md's question, answered yes by the coordinator), so `IndependentComposition
   productComposition` can be a certified line graded assumed.
Also: plan_model.lut fails check with three 4.R5 errors (`keyDigest`, `planDigest`, `recordDigest`:
non-provisional externs without a type, from bite A7); give them their types.

Read `CLAUDE.md`, `execution.md` (B1, B3, D1), report-B2.md, report-C1.md, decisions.md with his
answers. Each with a test that fails before and passes after, committed as it passes. Then
re-certify every test program six at a time (`xargs -P6`, `--jobs 1`, each its own log under
~/.cache/luthier-b1b3d1/, never /tmp), twice, the second at 0 lines ran; run the suite file by file
under `timeout 1800`. Long runs waited for in the foreground with bounded waits. Never git stash,
checkout or reset files that are not yours. Small commits staged by path: subject, blank line, one
body line, ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Report:
`report-b1-b3-d1.md` beside this file, committed (if your Write is refused, give its full text in
your final message): per item what you did, commits, checks, the uncontrolled conjuncts D1 lists,
decisions taken on your own, at most one question.
