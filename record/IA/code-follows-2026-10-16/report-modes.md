# Report: provisional externs refused by default, the modes of running as fields of the demand (step 3f)

By Claude Opus 5.5, an agent of the coordinating session, 2026-10-16, on
`record/IA/code-follows-2026-10-16/prompt-modes.md` (D-2026-10-16-c, D-2026-10-16-d).

## What was built

Commits: cc883f1 (world.lth), f5a8f02 (demand.lth, demand_model.lut, plan.lth), c19d8f0 (check -v,
elaborator), e60339c (run.py, cli.py, tests), e4fce14 (spec), ed18afa (certification_model's store).

1. Provisional (D-2026-10-16-c). `world.lth`: a route carries `provisional : Maybe String`, the
   reason; `Externs.applied` takes the demand's cutoff and the names it runs as assumed;
   `AppliedWhenSettled` says a provisional is applied exactly when named, whatever the cutoff. A new
   control in world_controls.lut, `blanketAssumed` (a bare assumed cutoff applies a provisional), is
   refuted, as L9.14 asks. `run` refuses a provisional not named, with its reason and the hint
   `--accept assumed:NAME`; `--accept` is repeatable, takes at most one grade, and a bare
   `--accept assumed` names no provisional. A named one is applied unvalidated, warns on stderr at its
   first application (name, route, reason), and is listed in `certification.assumed` with grade
   assumed and the names of the cone downstream of it. `check -v` prints each provisional with its
   reason. The declaration form is `extern "..." (provisional <- "why")`.
2. Modes (D-2026-10-16-d). `Demand` and `Record` gain `assumes`, `fuel : Maybe Nat`,
   `timeLimit : Maybe Float64`, `strategy : Strategy`, `fresh : Bool`; `theDemand` declares the
   defaults: no provisional assumed, no fuel bound, no time limit, forward on demand, not fresh.
   `Strategy` moved from plan.lth to demand.lth (plan.lth imports it; a cycle otherwise). run.py
   mirrors the defaults (`DEMAND_DEFAULTS`), records the asked strategy in `demand.strategy` and the
   one that ran, call by need, in `plan.strategy`. A new theory `Ran` in demand.lth,
   `RanIsASpecimenOfTheAsked`, says which may compute which, certified with a control.
   New flags: `--strategy`, `--time-limit SECONDS`; `--fuel` now optional; `--fresh` a field.
   `certify` keeps its budget.
3. Spec: 8.S1 (the demand's fields as implemented), 8.S3, 8.S4, 10.S10, 10.S12, and two clauses the
   change made false, 12.S17 and 12.S18. 6.S14 is not edited: chapter 6 was the other session's.

Tests: tests/test_modes.py (8): refused without naming, with its reason; named, run as assumed,
warning on stderr, grade assumed and downstream in the record; bare `--accept assumed` refusing (the
control); `--accept` with two grades or a name not in the cone; `check -v` with the reason; no fuel
bound finishing a program of 10,150,016 steps (about 90 s); `--time-limit 0.5` stopping a loop and
saying so; strategy, fresh and limits recorded. test_run.py and test_tester.py follow the new
record and the new census in world_laws.lut.

## Checks

    python -m pytest -q
    755 passed, 5 skipped, 9 xfailed in 517.13s (0:08:37)        (741 before)

    python3 scripts/check_spec.py
    docs/spec/03-kernel.md:190: check-spec: shares a run of 10 words with docs/principles.md: ...
    check-spec (information): 182 implemented, 80 decided (of which 33 suspended), 8 proposed

    python3 scripts/project_principles.py --check
    ok

    luthier check -v tests/run/certified/provisional.lut
    tests/run/certified/provisional.lut:7: provisional shout: Provisional extern: str stands in for
    a shout not written yet; run refuses it unless named by --accept assumed:shout.

`luthier certify` of world, demand and plan laws and controls: every law current and controlled
but KeyReadsOnlyTheCone and KeyReadsTheType, uncontrolled as before.

## Decisions taken on my own

- `Strategy` declared in demand.lth, imported by plan.lth.
- The theory `Ran` [proposed]: 4.R3 asks a law of demand.lth to touch Strategy's constructors, and
  it makes "say which ran" a law the record is held to.
- Record keys mirror demand.lth's fields: `assumes`, `timeLimit`, `strategy`, `fresh`.
- `(provisional <- true)` still reads, shown as "no reason given"; no migration forced.
- The elaborator drops named arguments of `extern` (a named provisional could not elaborate before).
- The warning is given once per route at its first application; a name in `assumed:NAME` that is
  no provisional of the cone warns too.
- Downstream propagation is recorded per provisional (`downstream`), with no run-level grade.
- A named provisional's own laws, if its type states any, are not demanded.
- The time limit is read every 4096 steps; `eval` and `session` take the demand's default fuel,
  now none, and have no `--time-limit`.
- The test past 10,000,000 steps stays in the default suite (about 90 s).
- I removed entries my scratch runs had written to world_model.cert.json before committing.

## Question

The test that shows no fuel bound costs about 90 s per suite (10 million steps at about 120,000
steps per second). Keep it in the default suite, or move it under LUTHIER_SLOW?
