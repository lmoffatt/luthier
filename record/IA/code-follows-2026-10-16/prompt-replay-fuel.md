# Brief: an exact replay, and a test that ran out of fuel (step 3c)

Read `CLAUDE.md` first, then `record/decisions.md` at D-2026-10-15-f (an exact replay is absorbed
when it agrees; when it disagrees both entries are kept and the law refused until resolved) and
D-2026-10-15-g (a not-run for lack of fuel is never memoized; fuel stays out of the identity);
`docs/spec/06-certification.md` 6.S8, 6.S15; `docs/spec/07-tests.md` 7.S9, 7.S13;
`src/luthier/lib/certification.lth` (`Identity`, `record`, `determined`, `known`, `NotRunFor`);
`src/luthier/certify.py` and `src/luthier/tester.py` (where entries are written and `--deep`).

Build:
1. Replay: when `certify --deep` (or any rerun) produces an entry whose identity the claim store
   already holds, an agreeing outcome writes nothing new; a disagreeing one is written beside the old,
   and the law is refused (a run and `check -v` say "replay disagrees" naming both entries) until a
   later agreeing pair or a manual resolution. State it in certification.lth as a law over `record`
   (the store law), with `determined` read as: one outcome per identity unless a disagreement is
   recorded, which refuses.
2. Fuel: an outcome `NotRunFor` whose reason is fuel spent is never written to a store; the next
   certify runs the line again. The fuel given stays out of the identity.
3. Spec: 6.S8 (both kept only on disagreement), 6.S15's idempotence sentence, 7.S13 ("a known outcome
   is not recomputed" except a fuel exhaustion, never stored): text and status for what you did.
Tests: an agreeing replay leaves the store byte-identical; a disagreeing replay (forged by changing
a host function's result between runs) is kept and refuses the law in run and in check -v; the
control (L9.14): a store that absorbs a disagreeing replay is refuted by the store law; a line run
with too little fuel leaves no entry, and run again with enough writes a pass.

Accepted when: `python -m pytest -q` passes in full (741 passed before, plus your tests);
`python3 scripts/check_spec.py` prints its one known finding (03-kernel.md:190) and the counts;
`luthier certify tests/tester/arrays_laws.lut` reports every line known and changes no store
(compare md5 before and after). Two-line commits ending with "Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>", staged by path; another agent commits at the same time in run.py, cli.py,
world.lth, demand.lth, plan.lth and spec chapters 8 and 10 (do not touch those), retry on
.git/index.lock. Report: `record/IA/code-follows-2026-10-16/report-replay-fuel.md` by shell heredoc,
committed: what you built, the checks' output, decisions taken on your own, at most one question.
