# certify.py, the store, the tester reusing entries, `luthier certify`: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-certify.md; saved by the
coordinator. Files: `src/luthier/certify.py` (new), `src/luthier/tester.py`, `src/luthier/cli.py`,
`tests/test_certify.py` (new, 20 tests), `tests/test_tester.py`. Checks: test_certify and
test_tester 30 passed, 2 skipped; the suite 593 passed; `certify` on numbers_laws.lut under
LUTHIER_SLOW=1 in 6 s, all 42 laws graded (LeqAntisymmetric sampled).

## What is written

certify.py: §4 `canon`, `canon_code`, `cone_hash`, `Cones` (the cone of a name in a runtime
program), `host_hash`, `interpreter_revision`; §1 `store_path`, `identity`, `store_errors`,
`read_store`, `write_store`, `known`, `record`; §2 `stale`, `certificate_grade`, `state`,
`standing`, `standings`; `certify_file`, `certify` (12.S16). tester.py: `Outcome` gains `cone`,
`entry`, `known`, `stale`, `differs`; `run_tests(..., deep, store)` looks each line's identity
up before running and records each line run; `new_entry`, `settle`, `law_cones`; a line ends
`(ran)` or `(known, DATE)`. cli.py: `test --deep --no-cert`; `certify FILES [--jobs N] [--seed N]
[--deep] [--fuel N]`; `check -v` prints `certificate LAW: <standing>` for files with test lines.

## The laws met

`ConeHashing`'s four laws as pytest functions over 81 cones (alpha-variants, a module prefix, a
`@file` tag, reordered code, a literal with `@`): the hash canonicalises (`kernel.canonical`
idempotent) and sha256 runs over an injective text (canonical terms, hosts, revision); at
program level a reached change changes the hash, an unreached one or a binder's rename does
not; a host module's edit changes `host_hash`. `IdentityIsTheKey` by construction (law, cone,
binding, seed, cases). `StaleIsAnotherHash` by construction. `Store`'s `determined` and
`gradedAsOutcome` checked on every read and write (`StoreError`). `record` unchanged on a known
identity, a new seed a new entry; reuse: the second `test` runs zero cases (refuted and not-run
lines reused too); `--deep` reruns, the file byte-identical.

## Choices (each undone by one commit)

1. `cone_hash(cone)` the model's route; `cone_hash(program, name)` on the Runner's elaborated
   runtime slice (canonical form is on kernel terms). 2. The cone: every kernel act reached
   through free names, pattern constructors, a constructor's data; a definition as (type, body),
   a hole as its type; externs by route; sorted by name then text. 3. The interpreter revision:
   the last commit touching `src/luthier/**.py`, plus `+<hash>` when the tree differs; the
   package version outside git. 4. Host code: a module's source bytes; an installed package as
   `dist version`; the standard library as `python X.Y.Z`. 5. The binding expanded: a census as
   `name (coverage)` with the hash of its cone; a drawn parameter as `SampledMode <metric> (size
   s) over <type>` or `ExhaustiveMode over <type>`: size and metric in the identity. 6. Reach: a
   census its members (Number or printed); exhaustive `Support`; a sampled scalar its
   `Interval`; else none (covers nothing). 7. Evidence stored as counts, coverage, verdict. 8.
   `Unsettled` stored as `NotRunFor` with no grade. 9. The store written after each line by
   atomic replace; `run_tests` defaults to no store, the CLI stores unless `--no-cert`; `certify`
   a spawn pool, one process per file. 10. Standing per certification_model.

## Decision for Luciano

Fuel and budgets are not part of the identity, and `record` leaves the store unchanged on a
known identity (proposed 5 of the theory), so a line not run for lack of fuel stays "known not
run"; `--deep` reruns and reports the difference but cannot record the pass. Put fuel and
budgets into the identity (the agent's lean), or let `--deep` write a new entry with the same
identity (breaking `determined`)?

## Not done

The `hashing` route not validated through `luthier test` (needs a generator of `Term` and its
crossing); `Provisional`, run's refusal (§3), transport (§2), `--imports`. The interpreter
revision makes every store stale after any commit to `src/luthier/*.py` (6.S8 as written):
frequent re-certification while the interpreter changes daily.
