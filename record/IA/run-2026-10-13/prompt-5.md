# run.py bite 5: core in every run, the primitives' operands reduced by the Runner, brief

Written 2026-10-14 by the coordinating session (luthier-1b). On the port's report
(`record/IA/slice-port-2026-10-14/report.md`, "What stopped the run"), after run bite 4 (2821823)
and kernel bite 9 (c2a63d0).

## The prompt

Read `CLAUDE.md` first, then the port's report (that section and "What was more than a rename"),
`record/IA/run-2026-10-13/report-4.md`, `src/luthier/run.py` (`Runner.whnf`, `run_file`, the
bootstrap) and `src/luthier/lib/core.lut`. Other agents edit `check.py`, `docs/spec/` and theory
files meanwhile: change only `src/luthier/run.py`, `src/luthier/host.py`, `tests/test_run.py`,
programs under `tests/run/`, and write your report.

`luthier run examples/sonolocalizacion/validate_graph.lut` reads the graph and stops with `stuck
match` at the first invariant. Four causes, one root: `Runner.whnf` hands an operator's
application to `kernel.step`, which steps the operands without the host and without core's data.
Fix: (1) every run loads `src/luthier/lib/core.lut` (the core's data `Bool`, `Maybe`, `List`,
`Nat`, `Fin`, `not`, the primitives) into the program before the file's own acts, as library.lth
and 11.R2 read the core (say how an `operator` act of core is or is not used tonight; the kernel's
bootstrap of the symbols stays until that is decided); (2) `run_file` defines every name of
`kernel.BOOTSTRAP_PRIMITIVES`, as `eval` does; (3) the Runner reduces the operands of primitives
and of `and`/`or`/`not` itself, with the host, so a host cell under an operator (`intAt t "a" 0 +
1`) crosses before the operator steps. The port's smallest program (in the report) and
`showInt (intAt t "a" 0 + 1)` on a parsed table become tests in `tests/test_run.py`. Then run
`validate_graph.lut` from the repository root and report where it stops next, with the smallest
program, if it does; if it reaches the end, paste its output line. Keep the 29 run tests passing.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, then `PYTHONPATH=src python3 -m
pytest tests -q`. Do not commit. Report in a few lines to `record/IA/run-2026-10-13/report-5.md`.
