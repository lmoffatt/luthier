# Brief: the core's bite 13c, the certification defects the audit found

An audit of the algebras (Codex, read-only, `record/plan/audit-algebras-2026-10-22/report.md`,
5b1a05e) found concrete defects in what certify and run already decide. The audit calls the
serving ones "immediate core-closing issues". 13b (the library and the closing) waits for this
bite's report before it re-certifies.

Read `CLAUDE.md` first, then the audit's summary and its part I (sections 1.1 to 1.8) and section
3.1; `record/plan/core-2026-10-17/report-bite-12a.md` (with its follow-up, 012b3ce) and
`report-bite-13a.md`; spec chapters 6 and 7 (6.S14, 6.S15, 7.S8, 7.S19); `record/decisions.md` at
D-2026-10-16-g and D-2026-10-22-a. Verify each finding yourself before fixing it: the audit probed
in memory, and the tree moved while it read.

Fix, each with a test that fails before and passes after:
1. Retention erases a refutation (audit 1.4 A): `prune` keeps four recent entries per group and can
   drop a current failure, after which passes restore a grade. Pruning must preserve refusal and
   unresolved conflict (spec 6.S15: a current refutation refuses the law regardless of passes).
2. Distribution-changing parameters outside identity (1.4 B): `specialMass`, `atomAtZero` and any
   other field that changes what is drawn belong in the sampling identity; pure execution limits
   (fuel, time) stay out. Classify each budget field and say so in 7.S8's text, marked as the
   coordinator's reading of D-2026-10-16-g.
3. The `byModel` path skips the failure and disagreement vetoes (1.5 A): a demand served through
   its model's conjuncts must be refused by a current failure or disagreement on the same model
   and conjunct, exactly as a direct demand is. Resolve a demand to its subject and obligations
   first, then apply the vetoes once, as the audit proposes, if that is the smallest sound fix.
4. Acceptance and recording select different evidence (1.5 B, 3.1): `serving` in run.py records
   one entry per law, so a run accepted on `P M` and `Q M` can record only `P M`. Serving returns
   the witness covering every required obligation, and both admission and the result key use it
   (L5.6, spec 8.S8).
5. The store reader accepts evidence and grade combinations the store's own Luthier predicate
   forbids (the audit's summary item 5; find its section). Make the reader enforce the predicate,
   or show the audit wrong.

Run everything with `/home/lmoffatt/miniconda3/bin/python` and `/home/lmoffatt/miniconda3/bin/luthier`;
scratch under ~/.cache/luthier-13c/, not /tmp. Your files: src/luthier/*.py, tests/test_*.py,
docs/spec/. 13b edits the library's .lth/.lut files: touch none. Don't re-certify the stores: 13b
does it after you. Small commits staged by path, never `git add -A`: subject, blank line, one body
line, ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".

Accepted when: each item's test passes; `python -m pytest -q tests/test_certify.py
tests/test_run.py tests/test_tester.py tests/test_check.py` passes, or each failure left is a
stale store (name it) for 13b's re-certification; `python scripts/check_spec.py` prints only its
known finding. Report: `record/plan/core-2026-10-17/report-bite-13c.md`, committed (if your Write is
refused, put its full text in your final message): per item what you found (confirmed or not), the
fix, the checks, which identities or cones move, decisions taken on your own, at most one question.
