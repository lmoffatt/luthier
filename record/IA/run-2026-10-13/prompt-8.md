# run.py bite 8: functions across the bridge (D-2026-10-14-a), brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). On D-2026-10-14-a
(`record/decisions.md`, end; spec 3.S23 at 1e38cb4) and the theory agent's report
(`record/IA/theories-2026-10-14/report.md`: what the specimens must do per law). The need:
sonolocalización's fit (`record/IA/sonolocalizacion-inventory-2026-10-13/answers-2-2026-10-14.md`,
item 2: `lm.maximize` calls back three Luthier lambdas up to 500 times each; `Objective` a record
of functions; `sampleFull` a Python partial as a Luthier value; six-parameter externs applied to
four).

## The prompt

Read `CLAUDE.md` first, then the three documents above, `src/luthier/run.py` (`Runner`,
`TypedExtern`, the bridge of bites 4 and 6: `report-4.md`, `report-6.md`), and spec 12.S18 (the
run's record). Other agents edit `tester.py` and theory files meanwhile: change only
`src/luthier/run.py`, `src/luthier/host.py`, `tests/test_run.py`, programs under `tests/run/`, a
Python module under `tests/run/` for the host side of the tests.

1. A Luthier lambda over an infinite domain (not `Fin n`) passed to a host function crosses as a
   Python callable that, when the host calls it with host values, crosses the arguments in by
   the lambda's domain types, reduces the application with the Runner (the host, the fuel), and
   crosses the result out by the codomain; each call counted on the run (a counter per crossing,
   reported at the end as 12.S18's record names it, or printed under `--verbose` if the record
   does not exist yet: say which).
2. A record whose fields are functions crosses as the record (the dict with attribute access of
   bite 4) with each function a callback as in 1.
3. A host value that is a callable, crossing in at a function type, is an opaque host function:
   a `TypedExtern` holding it (bite 4's `host:k` route), applied through the bridge, never
   reduced by the kernel; applying it to a Luthier lambda passes a callback as in 1.
4. An extern applied to fewer arguments than its declared type has is a partial application: it
   stays a value until the rest arrives (the arity of bite 6), and crossing it out gives a host
   partial.
Tests, each a program under `tests/run/` with a small host module beside it: a host `maximize`
that calls a Luthier `f : Float64 -> Float64` ten times and returns the argmin of a grid (the
count checked); a record `{ value, grad }` of Luthier functions read by attribute in the host; a
host function returned to Luthier and applied; a two-parameter extern applied to one argument
then the other. `examples/hello.lut`, `validate_graph.lut` and the 32 run tests unchanged.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, then `PYTHONPATH=src python3 -m
pytest tests -q`. Do not commit. Report in your final message: what crosses and how, every
choice D-a and the theory left open.
