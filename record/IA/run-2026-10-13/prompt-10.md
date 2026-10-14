# run.py bite 10: a definition and a constructor of one name kept apart, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-3e). On the second port's report
(`record/IA/slice-port-2-2026-10-14/report.md`, "The root cause"): program.lth defines `int :
Term` and a function `known`; any import reaching program.lth (probability.lth, generators.lth,
program.lth) brings them in, and in a run program.lth's `int` takes the name of tables.lth's
`Cell` constructor `int`, so every `intAt` is a `stuck match`; in check, `known` takes the name of
`SigmaTreatment`'s constructor and 4.R9 refuses `sigmaKnown`. `Loaded` keeps two files'
definitions of one name apart (`name@file`) but not a definition and a constructor. Smallest
program: tables.lth's `intAt` on `csv.parse "a:int\n7\n"` prints `7`; adding `import
"generators.lth" Level` makes it `stuck match`.

## The prompt

Read `CLAUDE.md` first, then that report section, `record/IA/run-2026-10-13/report-6.md` (the
loader `Loaded`: how names are scoped by file, how a pattern name counts as a constructor), spec
12.S22 (what an import brings in), 3.S7 and 3.R3 (constructors, where they are in scope),
`src/luthier/run.py` (`Loaded`), and `src/luthier/check.py` (`load_imports`, the typing with
imports of bite 5). Nobody else edits code now: change `src/luthier/run.py`, `src/luthier/check.py`,
`tests/test_run.py`, `tests/test_check.py`, programs under `tests/run/`.

1. In `Loaded`, a constructor of a `data` (or a label of a sum) and a definition of the same
   name in another file are different names: scope constructors by the file that defines their
   data as definitions are, and resolve a constructor reference (in a term or a pattern) by the
   same rule (the file's own data, then the imports listed, then core). The smallest program
   above prints `7` with the import; `experiment_zero.lut` is no longer stuck at 2 s (run it with
   `--set lmMaxIter=2 --set lmTol=1e-12 --set lmFloor=6.661338147750939e-15 --set
   graphDir=examples/sonolocalizacion/A/graph --set outDir=/tmp/x` in the background; it takes
   about five minutes; paste its summary line).
2. The same in check.py's typing with imports: an imported definition does not take a
   constructor's name; `luthier check examples/sonolocalizacion/experiment_zero.lut` loses the
   4.R9 on `sigmaKnown` (report what it still refuses).
3. Tests: the smallest program, and `known`/`sigmaKnown` reduced to a three-line case.

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py tests/test_check.py tests/test_lm.py
-q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message.
