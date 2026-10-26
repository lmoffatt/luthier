# Report of night agent P: print and stdout (D-2026-10-16-n), and two stale core tests

2026-10-26, Claude Opus 5.5, on the coordinator's brief for agent P. Committed by the coordinator from the agent's hand-back (its Write was refused). Sources: D-2026-10-16-n, its queue item in record/plan/code-follows-principles-2026-10-16.md, L11.9, spec chapter 10, report-wave-a-2.md (A2's `roots` and the coordinator's answer that a declared list belongs to this bite), report-night-C3.md. No observations of Luciano's on these files.

## Commits

- 319bba3: tests/test_core_structures.py follows bases_controls.test.lut since 480e92c.
- 79a5649: print writes at once and fails on a rejected write; stdout observed by its connection; roots of trust in luthier.lock (host.py, run.py, cli.py, world.lth, world_model.lut, demand_model.lut, a comment in demand.lth, tests/test_run.py, the comments of world_laws and world_controls).
- acb4c86: spec 10.S7 and 10.S13 gain [implemented] passages; the queue item marked done.

## What was done

- `print` writes at once: host.py's `print_line` writes the line to the run's standard output when applied and checks what each `write()` returns; a short write goes on with the rest; an error, or a write that takes nothing, raises `host.Rejected` with the bytes accepted; run.py turns it into `ActionFailed`, a `Cut` with reason "action failed": the run exits 1 and is recorded as not finished. `luthier run hello.run.lut > /dev/full` now exits 1 with `finished: false` (before: recorded finished, Python exiting 120 at flush). cli.py no longer prints the output at the end.
- The standard output is observed by what it is connected to (host.py's `_connected`, `observed_stdout`): a regular file re-read through its own descriptor from where the run began; a pipe by the host's copy of the bytes it accepted (its tee); a terminal or another device by the bytes it accepted; a stream with no descriptor by its copy. Every run's record has `stdout`: kind, how observed, the root of trust it rests on, the bytes accepted.
- A file is checked by re-reading it: a file stdout re-read at the first action (world.lth's `agreement`) and at the end of the run (`host.check_stdout`), a difference failing the run naming where it starts. The run's record, the result store and the lock are written through `write_checked` (temporary file, replace, re-read).
- The roots of trust, named and declared by the project: world.lth §5's `ObserverIsFaithful` becomes two axioms, laws of `Host`: `FileSystemKeeps` (a file read again gives what the file system keeps) and `SystemDelivers` (the bytes the system accepted at a terminal or a pipe reach it). The project declares the roots it accepts once, in luthier.lock's `roots`; `run` reads them into the demand's `roots`, writes the defaults into a lock it writes, never rewrites an existing lock; a lock without `roots` leaves the defaults, a malformed one is refused. The record lists them in `lock.roots` and `demand.roots`; demand_model.lut's default and run.py's `DEMAND_DEFAULTS` follow.
- tests/test_core_structures.py follows bases_controls.test.lut since 480e92c (27 lines over the five claims plus `ProductIsIndependent`; the union-bound test picks the product's line by its model `badProduct`).

Seven new tests in tests/test_run.py fail at the parent's code and pass now: a rejected print fails the run (/dev/full); stdout observed by connection (file, pipe); a file that keeps other bytes is seen by re-reading; a later print checked at the end; a pipe observed by its tee and trusting the system (the record names `SystemDelivers`); the roots of trust are the project's (an empty list refuses hello, one root accepted refuses the other, a malformed list refused); the record checked by re-reading it. The roots are axioms, so they have no law line and no control (11.R3), as `ObserverIsFaithful` before them.

## Checks

pytest over test_run, test_session, test_modes, test_result_store, test_file_kinds, test_plots, test_tables_cut, test_certify, test_elaborate, test_core_structures: two failures not from this work (`test_a_bound_maximize_runs_once`, lm's stale entries, failing at baseline; `test_certify_lists_the_laws_of_tables_with_their_controls`, the table controls 10 → 12). Expectations updated: the five naming `ObserverIsFaithful`; the lock now holds `roots`; the liar's refused run has already printed its lines. `luthier check` clean on world.lth, world_model.lut, demand.lth, demand_model.lut, world_laws, world_controls, examples/hello.run.lut. `check_spec.py`: its known finding. Not certified: host.py changed, so the host's first-action entries no longer serve; world_laws, world_controls and the demand's programs need the coordinator's wave.

## Decisions taken on my own

1. The project's declaration lives in luthier.lock (`roots`), the file D-2026-10-16-n names, not in Luthier source.
2. `FileSystemKeeps` and `SystemDelivers` replace `ObserverIsFaithful`; the interpreter and the floating-point hardware (also in L11.9) get no law here (the record holds the interpreter's revision and Python's version). core/structures/algebraic.lth:134's comment still says `ObserverIsFaithful`.
3. `run` writes to `sys.stdout`'s descriptor; with none it writes through the stream, observed by its copy; `eval` and `session --world` keep the copy alone, as before.
4. A failed action is recorded as a `Cut` (`ActionFailed`), with no output.
5. The end-of-run re-read of a file stdout fails the run when it differs.
6. The record written through a temporary file that replaces it.
7. Files beyond the brief's list: host.py, cli.py, demand_model.lut, a comment of demand.lth.

## Question

A run refused at its first action has already acted (the liar's lines are on stdout), but by the existing rule nothing is recorded. Should a refused run whose action reached the world be recorded, as a run that did not finish?

Coordinator's answer (2026-10-26): yes. What reached the world is evidence (P3 keeps the original evidence; L4: an action is recorded), so the run is recorded as not finished, with what it printed and why it was refused.

Implemented 2026-10-26 by agent P (cc36845): run.py's `RefusedAfterActing`, a `Refused` and a `Cut`, raised when a refusal comes after an action was applied to the token (the Runner counts them, `acted`); `luthier run` records it with `finished` false, reason "refused", `output` the bytes accepted and `refusals`. The liar's test fails before and passes after; tests/test_run.py passes but for the known stale `test_a_bound_maximize_runs_once`. The comment at core/structures/algebraic.lth:134 now names the roots (5b20e73).
