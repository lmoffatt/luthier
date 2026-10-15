# Brief: the result store across runs at its smallest (v0.4's criterion c)

Read `CLAUDE.md` first. Then, in this order: `record/decisions.md` at D-2026-10-15-c (every behavior
expressible, L5.20), D-2026-10-15-d (pure only, stores' hashes recorded, the hole marked),
D-2026-10-15-g (fuel never in a key), D-2026-10-15-h (record and key apart), D-2026-10-16-a
(stores as relations, L10.11, L10.12); `record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md`
step 6.3 criterion (c); `docs/spec/08-demand.md` 8.S3, 8.S8, 8.S10; `docs/spec/12-files-and-tools.md`
12.S11, 12.S18; `src/luthier/lib/demand.lth` (`Record`, `recorded`) and `src/luthier/lib/plan.lth`
(`MemoKey`); `src/luthier/run.py` from `def run` to the end (the record, `plan_hash`, the lock).

What to build:
1. A run's key (8.S8, D-2026-10-15-h): the demand's key (decoration and live values), the cone's
   hash, the strategy, the seed, the plan's hash and the hashes of the certificates that served the
   cone; fuel, time and lock are not in it. Its hash goes in the record (`x.run.json`) as a new
   field; in the theories, a law that the key is a function of the record, the seed, the plan and
   the certificates (demand.lth or plan.lth, whichever holds `MemoKey`), with `determined` speaking
   of the key.
2. The store: `x.results.json` beside the program file (L10.12: the file that makes the claim), a
   list of {key hash, key, value printed, the record's time}. `run` writes the result of a pure entry
   under its key; a later run whose key is there is served from it without evaluating, and its
   record says so, naming the entry that served it. Pure means: the live cone performs no action
   (no `W`); a cone with any action always executes (D-2026-10-15-d).
3. `--fresh` (L5.20): executes literally whatever the store holds, and writes nothing new if the
   value agrees; if it disagrees, both are kept and the run says so (as D-2026-10-15-f for replays).
4. Each run records the hash of the bytes of every certificate store it read (a field beside
   `files_read`).
5. The hole marked (L14.4, D-2026-10-15-d): a comment in `src/luthier/lib/certification.lth` where
   the store is read and written, saying the stores are written and read by the host outside `W`
   until they become places of the world with own actions (10.S6, 12.S11); the same postponement in
   the status of 10.S6 and 12.S11 if `scripts/check_spec.py` accepts it, otherwise in their text.
6. Spec: 8.S8 / 12.S18 updated for what is now implemented (status `[implemented]` for what you
   did, the rest left as it was).

Tests (tests/): two runs of one pure entry (the second served, its record naming the first); two
runs of `examples/hello.lut` (both executed); `--fresh` on a served entry (executed); a control in
the sense of L9.14: a store that serves an entry whose key differs in one field (the seed, the
cone) is refused by the law or the test; a run whose fuel differs is still served.

Accepted when: `python -m pytest -q` passes as before plus your tests; `luthier run` twice on a pure
entry shows the second served; `python3 scripts/check_spec.py` and
`python3 scripts/project_principles.py --check` exit as before. Commit in small commits of two lines,
ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; stage your files by path
(another agent may commit at the same time; retry on .git/index.lock). Do not touch `certify.py`'s
store writes (another bite). Write your report to `record/IA/code-follows-2026-10-16/report-store.md`
with a shell heredoc: what you built, the tests, the decisions you took on your own (each undone by
one commit), and one question for the coordinator if any; commit it.
