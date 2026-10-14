# run.py bite 8: functions across the bridge (report)

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on prompt-8.md and its addendum; saved by
the coordinator. Files: `src/luthier/run.py`, `src/luthier/host.py`, `tests/test_run.py`, new
`tests/run/bridge_host.py` (the host side), `callbacks.lut`, `record_of_functions.lut`,
`host_function.lut`, `extern_partial.lut`. Checks: test_run 67 passed, 1 skipped (6 added); the
suite 552 passed; `luthier check` nothing on the four programs; no `.run.json` left.

## What crosses and how

1. Callback (`CallbackGivesTheFunction`, `CallsAreCounted`): a Luthier function handed to an
   extern at a declared function type whose domain is not `Fin n` reaches the host as a Python
   callable (`function_to_host`); each call crosses the arguments in by the domain types,
   reduces the application with the Runner on the run's fuel, crosses the result out by the
   codomain; counted in `host.count(route, position)` (the receiving extern's route, the 1-based
   argument index); `x.run.json` gets `"calls": {route: {position: n}}`. Test `callbacks.lut`:
   `maximize` calls `(x-0.3)^2` ten times, prints `0.3`, count 10 checked in-process and in the
   record over two runs.
2. Record of functions (`RecordCrossesByField`): the `HostRecord` with each function field a
   callback counted under `position.label`. Test `record_of_functions.lut`: `objective.value`,
   `objective.grad` read by the host, prints `3.0`, counts `{"1.value": 3, "1.grad": 2}`.
3. Host function crossing in (`HostGivesBackAValue`, `ExternIsValue`): bite 4's `host:k`
   `TypedExtern`, applied by the bridge, never a head for `kernel.step`; new: applying it to a
   Luthier lambda crosses the lambda as a callback, counted under `host:k module.qualname`. Test
   `host_function.lut`: `3.5`, `18.0` (a host function calling a Luthier lambda twice).
4. Partial application of an extern (`ExternPartialIsValue`): inside Luthier it already worked
   (arity from the type); crossing a partial out gives `functools.partial(host_fn, *args)` with
   the arguments crossed at their domains. Test `extern_partial.lut`: `3.5`, then the partial
   twice (a bare extern and one read by eta).
A sixth test: a callback whose result is not a Float64 gives a RunError.

## Choices of the agent (each undone by reverting)

1. The counts live in host.py (reset per run), `run.record` reads them; cli.py untouched.
2. `calls` always written, `{}` when nothing called back; positions `"k"`, `"k.label"`,
   `".out"`; elements of Maybe, List, pairs, sums keep the parent's position; calls accumulate
   across invocations of one extern within a run.
3. A host function that crossed in is keyed `host:k` plus its Python `module.qualname`.
4. A partial crossing out is host to host: its later calls not counted, results not checked (no
   `--checked`); an extern with zero arguments crosses as the host function itself (a bare
   extern at a function type used to be wrapped as a Runner callback).
5. Eta: a lambda that only passes its parameters on to an extern partial is read as the partial.
6. An untyped extern receiving a lambda is still refused.
7. A RunError inside a callback propagates through the host unchanged.
8. A callback runs on the run's single fuel budget.
9. The host module is `python:run.bridge_host.*` through the namespace package `run`.

## Left open

`--checked` for host partials and callbacks; kernel.py alone reading the arity from the `Define`
(`ExternPartialIsValue`'s duty for the kernel); whether `host:k` counts belong in the record;
3.S23's "to do" sentence (the coordinator's); 12.S18's other fields as in bite 7.
