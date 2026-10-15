# Report: the result store across runs at its smallest (v0.4's criterion c)

Claude Opus 5.5, an agent of the coordinating session, 2026-10-16, on
`record/IA/code-follows-2026-10-16/prompt-store.md` (925fe49).

## What was built

Commits: 5f2b87d (theories), 43572cd (run.py, cli.py), b8e5611 (tests), 704988f (the hole in
certification.lth), 1d1cef9 (spec and plan_model.lut's header).

1. The key of a run (8.S8, D-2026-10-15-h). plan.lth: `chosen` (the plan before its schedule),
   `modeOf`, `keyOf` (the key from a `Record`, a seed, a plan and the certificates' hashes),
   `Keying` gains `runKey` and the law `KeyIsOfTheRecord` (the key a run computes is the hash of
   `keyOf` of what it records), and `ResultsDetermined`, demand.lth's `determined` over the key's
   hash. demand.lth: `Record` carries the decoration (B1 of summary-BCD.md, now that item 5 is
   decided); §4 says the identity is the key. run.py: `result_key`, `key_hash`, computed before
   evaluating; `x.run.json` gains `key_hash`, `seed` (null: no run draws), `certificates` (the
   hash of the canonical JSON of the latest entry serving each law of the cone).
2. The store: `x.results.json` beside the program (L10.12), a list of {key hash, key, value, time};
   the value is printed as `eval` prints it, the time is the record's. A pure entry (no `W` in the
   elaborated types or bodies of its live cone, `acts`) is served when its key is there with one
   value; the record's `result_store.served` names the entry (index, key hash, the first run's
   time) and standard error says so. A cone that acts always executes.
3. `--fresh` executes whatever the store holds; agreeing, nothing is written (`agrees`); disagreeing,
   both are kept (`written`, `disagrees`), standard error says so, and the key is not served until
   the discrepancy is resolved (D-2026-10-15-f read for results).
4. `stores_read` beside `files_read`: [path, sha256 of the bytes] of each certificate store read.
5. The hole marked in certification.lth at the store and at `record`; the postponement in the text
   of 10.S6 and 12.S11 under `[decided D-2026-10-15-d]` (check_spec takes one status per item).
6. Spec: `[implemented]` paragraphs in 8.S8 and 12.S18; 8.S10's implemented part, which said the
   store did not exist, rewritten.

## Tests

tests/test_result_store.py, eight: a pure entry run twice, the second served and naming the first;
hello.lut twice, both executed, nothing stored, `stores_read` and `certificates` present; `--fresh`
agreeing; `--fresh` disagreeing, then the key not served; fuel differing, still served; a live hole
changing the key; the key recomputed from the record (fuel, time and lock out; seed, cone and
certificates in); controls (L9.14): an entry whose key differs in the seed or in the cone does not
serve, stored honestly under its own hash or forged under the run's. tests/test_run.py: the
recorded demand now has `"decoration": None`.

Acceptance: `python -m pytest -q` 737 passed, 5 skipped, 9 xfailed (729 before, plus 8);
`luthier run` twice on `a : Int := 1 + 2; main : Int := a * a` prints on the second
`served from square.results.json, entry 0 of 2026-10-15T22:48:35+00:00 (8.S9; --fresh executes it)`
and its record's `result_store.served.entry` is 0 with the first run's time;
`scripts/check_spec.py` exits 1 with the one finding it had before (03-kernel.md:190);
`scripts/project_principles.py --check` exits 0, as before.

## Decisions taken on my own (each undone by one commit)

- The plan's hash in the key is that of the plan as chosen (strategy, entry, live cone), without
  the call-by-need schedule, which exists only after evaluating; stated in plan.lth (`chosen`,
  [proposed]). The recorded plan keeps its full hash.
- The strategy is not a separate field of the key: it is in the plan, so in the plan's hash. The
  mode is `checked` or `plain`.
- Purity is read from the elaborated code: any `W` in a live name's type or body counts as acting,
  even if never applied (the safer reading, as 10.S6 treats an undeclared action).
- The store is written by `record` (the CLI's run), so `run_file` in tests writes nothing; a served
  run prints nothing on stdout (a pure run never did) and says it is served on standard error.
- `fresh` is an argument of `run`, recorded in `result_store`, not a field of demand.lth's `Demand`.
- A key whose entries disagree is not served, whether or not `--fresh` is given.
- `*.results.json` is ignored by git, as `*.run.json` is.
- The stores' bytes are hashed just before `certify.read_store` reads them (two reads; the race is
  the host's, outside `W`).

## Question

Should `fresh` be a field of the demand (demand.lth's `Demand`, declared with its default in
demand_model.lut's `theDemand`, L5.19), as every other argument of `run` is? Today it is only an
argument of `run`, recorded in `result_store`; making it a field touches demand.lth, demand_model.lut
and `DEMAND_DEFAULTS`.
