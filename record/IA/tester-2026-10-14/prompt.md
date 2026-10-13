# luthier test, bite 1: a tester over test.lth, exhaustive and sampled, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). Step 5.2 of
`record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md`, at its smallest, by the
order after v0.2 (D-2026-10-13-ad): a tester enough to run the laws of the slice's theories and,
next bite, to validate an extern at its first action.

## The prompt

Read `CLAUDE.md` first, then `docs/spec/07-tests.md` (7.S1, 7.S7, 7.S8, 7.S10, 7.S12, 7.S13, 7.S20,
7.R1), `src/luthier/lib/test.lth` (§1 to §3 whole), `laws.lth` (`Evidence`, `Points`, `At`,
`NotRun`, `Coverage`, `Verdict`), `generators.lth` only where test.lth imports from it (`Seed`,
`Binding`, `Budgets`, `Metric`; the sized generators of recursive data are a later bite), and
`src/luthier/run.py` for how a program is loaded and reduced with the host. Other agents edit
`check.py` and `tests/test_check.py` meanwhile: change only `src/luthier/tester.py` (new), the
`test` command in `src/luthier/cli.py`, `tests/test_tester.py` (new), programs under
`tests/tester/` (new), and write your report.

Write `luthier test FILE [--seed N]`: the specimen of test.lth's `Tester`. It loads the file as
`run` does (core, imports, the host), collects its top-level `test` lines (D9: a `test` line is
data, a `TestSpec` built by test.lth's `test` with its defaults: read how `test` names its law,
mode, `n`, size, seed, bindings and budgets, 7.S20), and runs each: for `ExhaustiveMode` every
value of the law's parameter types when they are finite (`Bool`, `Fin k`, `Unit`, a `data` with
nullary constructors, products and sums of those; otherwise `NotRun` with the reason); for
`SampledMode` `n` cases drawn by a generator per parameter type from the seed (Int, Float64,
String, Bool, Fin, lists and pairs and records of those, bounded by the size; the metric ignored
tonight, say so), each case reduced with the Runner to the law's verdict; the evidence as
laws.lth states it (`Points` with each case's verdict, the coverage the weakest reached, `NotRun`
when a budget gave nothing, 7.S12: `n` counts evaluated cases), the grade read as test.lth §3
reads it, printed one line per test: the law's name, the mode, cases evaluated, the grade, and
the first refuting case if any. A failure of the host or a stuck reduction on a case is reported
on that case, not as a crash. Tests: a file with an exhaustive law on `Bool` that holds, one that
is refuted (the case printed), a sampled law on `Int` that holds, one refuted at a size, a `NotRun`
(an infinite type under `ExhaustiveMode`); then `luthier test src/luthier/lib/numbers_model.lut`
and `tables_model.lut` if they carry `test` lines (if not, say which laws of numbers.lth you ran
by hand through a test file under `tests/tester/`, and what they gave: a refuted law of
numbers.lth is a finding for its author, report it, do not change the theory).

Check: `PYTHONPATH=src python3 -m pytest tests/test_tester.py tests/test_run.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message (the
harness may refuse a report file; the coordinator saves it): what runs, every point where test.lth
or spec 7 did not decide and what you chose, what the laws of numbers.lth gave.
