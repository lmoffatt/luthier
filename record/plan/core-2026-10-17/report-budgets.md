# Every budget of a test an argument of the test: report

2026-10-18, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-budgets.md` of this
folder (7.S8; P11, every criterion is a parameter; D-2026-10-15-g, fuel only cuts and is in no
identity; report-bite-1.md's question on fuel). Started at 321e394.

## Commits

- bc26cdc generators.lth §6: `fuel` a field of `Budgets`, positive like the counts; test.lth:
  `defaultBudgets.fuel := 3000000`, with the reason certify.py's `FUEL` carried, and `withFuel f b`,
  the budgets `b` with the fuel `f`.
- d1a7314 tester.py, certify.py, cli.py: `tries`, `coveringAbove`, `specialMass` and `atomAtZero`
  read from the line's budgets with no default in the code; each line runs with its budgets' fuel;
  `fuel` given to `run_tests`, `certify_file` or `certify` (`--fuel` of `luthier test` and `luthier
  certify`, default none) replaces it for the run and is written into the line's budgets, which the
  entry records. `certify.FUEL` is gone.
- c2a7b4e belief_laws.test.lut: the three fitA Maximizer lines take `withFuel 30000000
  defaultBudgets`.
- dbeef6c tests: a line's own fuel cuts it at that fuel and the entry records it; test.lth's default
  is recorded when the line gives none; `fuel=` overrides the line's and is recorded in the stored
  entry; a later run at the line's own fuel finds the outcome known (fuel out of the identity);
  `certify_file(..., fuel=100)` cuts a line the default runs. test_tester's defaults test reads the
  fuel too.
- 5c4931b spec 7.S8 `[implemented]` (its text rewritten on what holds now); 12.S15's `--fuel`.
- fca9c01 the stores after the first wave.
- 6963206 seven more lines with a fuel of their own (finding 2); 9910de0 their stores.
- this commit, the report.

## The checks

- `grep -n "2000\|20000\|3_000_000\|3000000" src/luthier/tester.py src/luthier/certify.py`: nothing,
  exit 1. Numbers that remain in tester.py and are not a test's budget: the fuel that reads a test
  line into a spec (`read_spec`, and `prepare`'s and `line_claims`'s default, 1,000,000), which runs
  before any line's budgets are known; the fuel of reading a census member as a number and of
  printing it in an entry (10,000, `_number_of`, `_value`) and of reducing test.lth's
  `grade` (100,000). Two bound what the region classifier reads from a value (`numbers`'s 4,000
  doubles, `_MOST_ENTRIES`'s 400 entries of a matrix written as a function); they are the closest
  to a budget of the test and are the question below.
- `luthier check` on the five .lth and .lut files touched: nothing, exit 0.
- First wave, `luthier certify tests/tester/*.test.lut --jobs 4`, 61 min: most lines ran (finding 1).
  No law refuted, every control passed; the fixtures printed what they are built to print
  (laws.test.lut: AndIsOr and Small refuted; cases.test.lut: Partial and RootIsNotNegative not
  run). Exit 1 for the fixtures alone.
- Second wave, the same command, 22 min: every line known but seven, cut at 3,000,000 (finding 2).
- The three fitA lines alone, from a copy of belief_laws.test.lut in tests/tester/ with only them,
  `luthier test --no-cert`, no `--fuel`: all three exhaustive, 1 case, cases grade, 17 min. They
  were known in the waves, from bite 1's entries (same identity, fuel out of it).
- After 6963206, `luthier certify` on probability_laws and sonolocalizacion_laws: the seven ran and
  passed, 34 min.
- Last wave at 6963206, `luthier certify tests/tester/*.test.lut --jobs 4`, 43 s: `0 lines ran` in
  each of the 35 programs; the fixtures' lines only ran (their stores beside them had been removed,
  as after every wave). Exit 1 for the fixtures alone.
- `python -m pytest -q tests` at 6963206: `829 passed, 6 skipped, 9 xfailed in 1497.90s`. Of the nine
  passed beyond the brief's 820, three are this work's; the rest came with other sessions' commits
  made meanwhile (81f5818 and those before it).
- `python3 scripts/check_spec.py`: its known finding only, `docs/spec/03-kernel.md:190`; "186
  implemented, 79 decided (of which 33 suspended), 8 proposed" (7.S8 moved from decided).

## Findings

1. The identity holds as the brief says (the budgets are not in it), but the first plain certify did
   not find the lines known: the code that draws a sampled entry's cases (`drawing_revision`, bite
   1's cfa7138) includes the source of `Values` and `run_spec`, and both changed where `2000` and
   `20000` were read. Every line with a parameter drawn under SampledMode got a new fingerprint and
   ran; so did the lines whose cone holds `Budgets` (certification's `Entry` has a `budgets`
   field). The draws themselves did not change. Lines on censuses under ExhaustiveMode stayed known
   (plan, plot, tables and world lines, and the fitA lines).
2. Bite 1's reading that every library line but three needs no more than 3,000,000 per case was
   wrong: seven lines on distances.lut's native likelihoods (`nativeFull`, `nativeProfile`) are cut
   at 3,000,000 and were stored only because bite 1's wave ran at 6e7. Measured at 1e8, seed
   20261014, the largest fuel per case: FullAgrees 7,754,360, ProfileAgrees 8,010,427
   (sonolocalizacion_laws); TangentShapes 4,780,218 and 4,518,452, InfoSymmetric 3,732,375 and
   3,473,361, ProfiledIsGaussianAtItsSigma 6,142,380 (probability_laws, on posModel and fullModel).
   Each now carries `withFuel 10000000 defaultBudgets`. The measurement wrapped `tester.evaluate`
   and recorded `fuel given - fuel left` after each case, on a copy of the file with only those
   lines, `run_tests(copy, fuel=100_000_000, store=False)`; the script stayed in my scratchpad.
3. tests/tester/core_instances.cert.json, untracked and not mine, was rewritten by the waves as any
   store is (its lines ran with the rest); its state before is in my scratchpad as
   core_instances.cert.json.before-budgets.
4. `withFuel` builds a `Budgets` from a `Nat`, so `withFuel 0 b` is a record that breaks the
   subtype's `0 < fuel`. Nothing checks that on a test line today.

## Decisions taken on my own (one commit undoes each)

- The fuel given (`--fuel`) is recorded by writing it into the line's budgets, so the entry's
  `budgets.fuel` is the fuel the line ran with; no separate field says it was overridden.
- `withFuel` in test.lth, since Luthier has no record update; the fitA lines and the seven others
  give `withFuel n defaultBudgets` instead of repeating every default.
- 1e7 for the seven native-likelihood lines (1.25 times the largest measured), as 3e7 is for fitA
  (1.15 times).
- The masses (`specialMass`, `atomAtZero`) are read without a default too, though the grep did not
  ask for them: their `0.0` fallbacks were constants of the same kind.
- The reading fuels (1,000,000, 100,000, 10,000) stay in tester.py: they bound the tester's own
  reading of a line, its census members and its grade, which run before or outside any line's
  budgets.
- The spec's 7.S8 now says the test line takes the budgets (`test`'s argument `budgets`) and the
  command lines take `--fuel` only; the decided text had `luthier test` take each budget as an
  option.

## Question

The region classifier reads at most 4,000 doubles of a value and 400 entries of a matrix written
as a function (tester.py's `numbers` and `_MOST_ENTRIES`). Should these two become fields of
`Budgets` like the others (P11), which changes the cone of certification's `Entry` again and re-runs
those lines once, or stay the classifier's own constants?
