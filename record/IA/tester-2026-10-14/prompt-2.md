# luthier test, bite 2: follow test.lth d54eae1, aef8d2c and generators.lth 993f200, brief

Written 2026-10-14 by the coordinating session (luthier-1b), on luthier-03's message.

## The prompt

Read `CLAUDE.md` first, then `git show aef8d2c d54eae1 993f200 4a158b0 --stat` and the diffs of
test.lth, generators.lth and numbers.lth at them. Other agents edit `run.py`, `cli.py`,
`tests/test_run.py` and `docs/guide/` meanwhile: change only `src/luthier/tester.py`,
`tests/test_tester.py`, programs under `tests/tester/`.

1. test.lth renamed the grade `Assumed` to `AssumedGrade` (as `ExhaustiveGrade`): tester.py:665
   and tests/test_tester.py:90-92 follow.
2. generators.lth renamed its theory `Exhaustive` to `Enumeration` and dropped dead imports:
   follow wherever the tester or its tests name it.
3. test.lth's `CoverageIsTheWeakest` (d54eae1): under `ExhaustiveMode` the run's coverage is
   `specCoverage` (`Bounded size` weakened by bindings) or `wholeCoverage` (`Exhaustive`
   weakened by bindings); sampled, rank at most the spec's. tester.py:547 sets `Exhaustive`
   without weakening by a `Drawn` or `Listed` binding: the law asks the weakest; mirror it with a
   test (an exhaustive law with a census binding gets the weakened coverage).
4. numbers.lth: `LeqBoth` gone, `LeqAntisymmetric (x y : Moderate) := x == y or not (leq x y and
   leq y x)`: `tests/tester/numbers_laws.lut` follows if it names them; under `LUTHIER_SLOW=1`
   the slow test should now show `LeqAntisymmetric` sampled (paste the line).

Check: `PYTHONPATH=src python3 -m pytest tests/test_tester.py -q`, then `PYTHONPATH=src python3
-m pytest tests -q` (green). Do not commit. Report in your final message.
