# Report: an exact replay, and a test that ran out of fuel (step 3c)

Brief: `record/IA/code-follows-2026-10-16/prompt-replay-fuel.md`. By Claude Opus 5.5, an agent of the
coordinating session, 2026-10-16. Commits: af07d24 (theory, model, test programs), 8c89b06 (certify.py,
tester.py, tests), 3a3328b (spec 6.S8, 6.S15, 7.S13; one more paragraph of certification.lth).

## What was built

Replay (D-2026-10-15-f). certification.lth draft 2 states the store law as a theory, `Recording`
(a model is a way of writing a store: `record : Entry -> List Entry -> List Entry`), with five
laws: a new identity goes in front; an agreeing replay of a settled identity writes nothing; a
disagreeing one is written in front and leaves the identity in disagreement; one that agrees with the
latest of an identity in disagreement is written and settles it; a not-run for fuel is never written.
`recordEntry` is the reference (certification_model.lut's `recording`), certify.py's `record` the
specimen. `determined` is now read as "the latest two entries of each identity agree" and is out of
`Store`'s predicate; `disputes`/`disputeAt` find the disagreements. A disagreement at the current hash
leaves the certificate with no grade and is refused first, as a new state `Disagrees e f` naming
both entries (laws `ADisagreementRefutes`, `ADisagreementIsRefused`; the fold laws, `NotRunAddsNothing`,
`RefusalSaysWhy` and `ACurrentFailureIsRefused` adjusted to read it). In Python: `store_errors` no
longer rejects two outcomes for one identity; `prune` never drops the two entries of a disagreement at
the current stamp; `certificate_grade`, `standing`, `refuse`, `show_refusal` and the test line say
"replay disagrees at seed S, n N: the entry of DATE (outcome) and the entry of DATE (outcome)".

Fuel (D-2026-10-15-g). `fuelSpent`/`outOfFuel` in the theory; the tester marks a line cut by its fuel
(the Runner's fuel at zero when a case, a draw or the sequential test raised, however the message was
wrapped) unless a case refuted the law; its outcome is `NotRunFor "fuel spent"`, the line says the fuel
given, nothing is written (tester and `record` both refuse it), and the next run runs it again. Fuel
was already in no identity; a test checks it.

Tests (tests/test_certify.py): `certify --deep` leaves the store byte-identical; a disagreement forged
by flipping a host function's result between two runs (same file, same cone hash) is kept and refuses
the law in `luthier run`, `check -v`, the test line and a reused known line; a later agreeing pair
settles a disagreement (forged by the host raising); a disagreement survives pruning; the store law on
the reference and its controls (tests/tester/certification_laws.lut, certification_controls.lut: a
store that absorbs a disagreeing replay, one that keeps a fuel not-run, a `certifying` blind to
disagreements, each refuted, L9.14); a line run with fuel 100 leaves no entry, runs again, and with
enough fuel writes a pass of the same identity.

## Checks

- `python -m pytest -q`: 1 failed, 754 passed, 5 skipped, 9 xfailed. The failure is
  `tests/test_tester.py::test_an_alias_or_a_constructor_is_no_model_home`, which asserts on the text of
  tests/tester/world_laws.lut; it fails since cc883f1 (the other agent's world.lth commit), not on
  anything of this step.
- `python3 scripts/check_spec.py`: the one known finding, 03-kernel.md:190; counts 182 implemented, 80
  decided (33 suspended), 8 proposed (7.S13 moved from decided to implemented).
- `luthier certify tests/tester/arrays_laws.lut`: "35 laws, 0 lines ran, 52 known"; md5 of every
  src/luthier/lib/*.cert.json identical before and after.

## Decisions taken on my own

1. The store law is its own theory `Recording` beside `Certifying`, so that `Certifying`'s fields stay
   as they are (demand_controls.lut builds `Certifying` records by hand).
2. A fuel exhaustion is the exact outcome `NotRunFor "fuel spent"` (the kernel has no string prefix to
   read a longer reason); the detail goes in the printed line, which is all that remains of it.
3. A run is "cut by its fuel" when any case raised with the Runner's fuel at zero and no case refuted;
   a refutation is stored at any fuel.
4. A disagreement is refused before a failure, so a pass-against-failure replay says "replay disagrees".
5. [proposed in spec 6.S8] A later agreeing pair settles the disagreement but not a failure among its
   entries: the counterexample still refutes the law until removed by hand (6.S3, L10.3).
6. Manual resolution is removing the wrong entry from the store by hand; no command for it.
7. The new test programs were not certified into the library's stores: certification_model.cert.json
   is also written by demand_laws.lut, which the other agent is changing now.
8. `identity` reads a missing field as null (a test of run.py builds entries in part).

## Question

Decision 5: after a disagreement between a pass and a failure, should two later passes certify the law
again (the failure read as noise from outside the identity), or should the failure keep refuting it
until removed by hand, as now?
