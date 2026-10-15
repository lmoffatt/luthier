# The sequential tester (D-2026-10-15-b, L9.15): report

2026-10-15, by Claude Opus 5.5, an agent of the coordinating session, on `prompt-tester.md` of this
folder. Inputs: CLAUDE.md, `report-theory.md` (its last section is the list done here), laws.lth §4,
generators.lth §1, probability.lth §5 and the two models as committed (2d4519e to 1283a12),
record/IA/controls-2026-10-15/report-tester.md, src/luthier/tester.py and certify.py at ac04700.

Principles touched: L9.15 (a statistical law is valued by Wald's sequential test, its seed the
test's), applied; P11 (every criterion a parameter): the cutoffs are a census in the test file,
never a constant in the tester, and a line without them is refused; L9.14 and 7.S19 (a control per
law), applied to the statistical law and to the two laws of its statistic; P2 (what is derived
carries how): each entry records alpha, beta, delta, the samples spent, the sample size and the
budget. It assumes the theory's reading that `initial` is the size of every sample.

## What changed

Committed, each file alone:

- 7f718e9 tests/tester/generators_laws.lut: `UniformSampleIsUniform` with `c` bound to
  `wald := { alpha 0.01, beta 0.01, delta 0.5, initial 50, budget 400 }`; `level` and the `Level`
  import dropped.
- e0a58de tests/tester/probability_laws.lut: the two `UniformAtLevel` lines (listed and drawn) are
  one line of `SourceIsUniform` with `d` numpySort, `source` uniformSample and `c` wald, each a
  census of one (the listed lists were no stream, so they have no line in this form);
  `NoAlternativeAtZero` and `RatioNonNegative` run on `uniformValues numpySort` over drawn unit
  lists, `S` bound to the census `[UnitList]`; `level`, `Level`, `uniformLists`, `listedUniform`,
  `drawnUniform` dropped.
- 9219c90 tests/tester/generators_controls.lut: `SkewedSampleIsUniform (control <- true)` at
  `wald`.
- d581b3b tests/tester/probability_controls.lut: `SourceIsUniform` on the source `lump`
  `(control <- true)`; controls of `NoAlternativeAtZero` (a ratio of 2) and `RatioNonNegative` (a
  ratio of `1 - 3 delta`, negative at 0.5).

Uncommitted, as the brief asks: src/luthier/tester.py, src/luthier/certify.py, tests/test_tester.py,
tests/test_certify.py.

tester.py. A law whose result type is `Law` is run by `run_statistical`: every parameter must be
bound by a census of one (a binding that names a `Gen T` is the stream as a value, not a generator
of the parameter); the body at the bindings must reduce to `Statistical S T l draw c` with `T` the
`Seed`; the cutoffs are checked against `Sequential`'s predicate; then laws.lth's `sequential S T l
draw c seed` runs once through the Runner from the line's seed. Its result is the evidence
`Tested`, with alpha, beta, delta, spent, initial and budget. The verdict is `StatisticalByTest`'s
(Holds supported, Fails refuted, Unresolved unsettled) and the grade test.lth's `grade` over
`Drawn seed`, so a pass is sampled. Refused, each with its reason as `NotRun`: the cutoffs unbound
("never drawn; bind them as a census of one"), a census of more than one value, cutoffs that break
`Sequential`'s predicate, a stream whose state is not `Seed`, a `Law` that reduces to another form.
The entry's evidence is `{"Tested": {...}, "coverage": "(Drawn seed)"}`; its outcome `Passed` with
grade `Sampled`, `Failed` with the samples and rates, or `NotRunFor` beginning "unresolved at" (the
`Outcome` of certification.lth has no unresolved constructor). A statistical control passes on
`Fails` (`ControlRefuted`) and fails on `Holds` (`ControlConfirmed`). A known entry with `Tested`
evidence is read back with its verdict and spent. Separately: a census that lists a type
(`[UnitList]`) no longer makes the type's file a model home (see the findings).

certify.py. `tested_text` prints a sequential verdict; `standing` of a law whose latest pass at the
current hash is `Tested` reads "supported, sampled: held at N samples of K by the sequential test
(alpha, beta, delta, budget)"; `show_outcome` prints an unresolved test as such.

Tests: four in test_tester.py (constant streams of p-values: 0 fails at 8 samples, 1 holds at 2,
0.5 is unresolved at the budget of 400, as report-theory.md computed by hand; the lines printed and
each refusal; a statistical control is its own kind; a listed type is no model home) and one in
test_certify.py (certify with stores twice: the rates in the grade, the control matched by the
law's cone, the second run known and the same).

Suite: 708 passed, 5 skipped, 9 xfailed (`python -m pytest -q`, 5m15s).

## Acceptance

`luthier certify tests/tester/generators_laws.lut tests/tester/generators_controls.lut
tests/tester/probability_laws.lut tests/tester/probability_controls.lut --no-cert --fuel 100000000
--jobs 4` at e0a58de (`--jobs 4` added to run the files at once; the output is the same), exit 0,
55 min, the lines asked for:

    tests/tester/generators_laws.lut: 7 laws, 7 lines ran, 0 known
      UniformSampleIsUniform: supported, sampled: held at 144 samples of 50 by the sequential test (alpha 0.01, beta 0.01, delta 0.5, budget 400); uncontrolled: untested against any wrong model (7.S19)
    tests/tester/generators_controls.lut: 0 laws, 7 controls, 7 lines ran, 0 known
      control of SkewedSampleIsUniform on wald (Listed): refuted at 12 samples of 50 by the sequential test (alpha 0.01, beta 0.01, delta 0.5, budget 400): the control passed
    tests/tester/probability_laws.lut: 19 laws, 37 lines ran, 0 known
      SourceIsUniform: supported, sampled: held at 144 samples of 50 by the sequential test (alpha 0.01, beta 0.01, delta 0.5, budget 400); controlled (refuted on its control at 12 samples of 50 by the sequential test (alpha 0.01, beta 0.01, delta 0.5, budget 400))
      NoAlternativeAtZero: sampled; controlled (refuted on its control at S = UnitList, l = twoAtZero, x = ...)
      RatioNonNegative: sampled; controlled (refuted on its control at S = UnitList, l = negativeAtHalf, c = wald, x = ...)
    tests/tester/probability_controls.lut: 0 laws, 17 controls, 17 lines ran, 0 known
      control of SourceIsUniform on numpySort (Listed), lump (Listed), wald (Listed): refuted at 12 samples of 50 by the sequential test (alpha 0.01, beta 0.01, delta 0.5, budget 400): the control passed

Every other law of the four files had a grade and every other control was refuted. Another agent
changed the non-statistical lines of generators_laws.lut and generators_controls.lut after e0a58de
(8c6aef6 to 7aeab97); the generators pair, run again at cde1618, gives the same two statistical
lines, exit 0.

## Level

Dropped from the two `_laws.lut`, the only importers among my files; nothing of mine needs it.
`Level` is still declared in generators.lth §1 and imported by
tests/run/scope/label_and_definition.lut (whose test_run.py assertion needs some name of
generators.lth; `Seed` serves). Removing both is one commit each, outside this brief.

## Findings

- certification.lth's `admits` does not know `Tested`: `coverageOf (Tested v)` is `nothing`, so
  `heldAsRun` would refuse a statistical pass graded `Sampled`. The Python store predicate checks
  only `determined` and `gradedAsOutcome`, so nothing breaks; the theory is behind the Python here
  (a case `Tested (Holds r) -> g == Sampled` in `admits` would close it).
- `UniformSampleIsUniform` reads uncontrolled: its control `SkewedSampleIsUniform` is another law
  with its own cone, and the source is baked into both. In probability_controls.lut I wrote the
  lump control as `SourceIsUniform` at the binding `source <- lump` (the body of `LumpIsUniform`),
  so that it has the law's cone and `SourceIsUniform` reads controlled. Making the source a
  parameter of `UniformSampleIsUniform` in generators_model.lut would do the same there.
- `UniformSampleIsUniform` and the `SourceIsUniform` line are the same computation (the same source,
  seed and cutoffs, 144 samples each, some 35 s each); one of the two lines could go.
- A stray store, src/luthier/lib/probability.cert.json (untracked, 10:42), and changes to
  src/luthier/lib/probability_model.cert.json were written by a run with stores of
  probability_laws.lut that was not mine (all my runs were `--no-cert`), through my uncommitted
  tester.py: the census `[UnitList]` made probability.lth a model home. Fixed in tester.py
  (`_is_type`: a type a census lists is no model); the stray file is left, being evidence, for
  whoever owns that run to keep or delete.
- Not done, as outside the brief's list: the observed beta of a control over `seedsPerControl`
  seeds (7.S19), and `DrawsAreUniform`, `DrawsAreIndependent` and their controls, which wait for a
  host of `uniformPValue`, `serialPValue` and a host `Random`.
- Under the null at delta 0.5 the log ratio drifts by about -0.045 per sample with a standard
  deviation of about 0.31 (my computation over the tilt), so the test holds after some 100 samples
  and is still unresolved at 400 with a probability of roughly 1 to 2%. The thresholds bound alpha
  and beta only approximately (Wald), and the budget truncates the test; the rates recorded are the
  ones asked, not ones measured.

## Decisions taken on my own

Each is one commit to undo and nothing depends on it yet.

- `initial := 50`, `budget := 400` in `wald` (the brief left them to me).
- A statistical line binds every parameter by a census of one; a `Gen` binding there is the stream
  itself; more than one value is refused; a `Law` of another form is not run; the line's mode is
  ignored and its coverage is `Drawn seed`.
- Cutoffs checked against `Sequential`'s predicate at run time.
- The entry's evidence shape `{"Tested": {...}, "coverage": ...}`; an unresolved test stored as
  `NotRunFor "unresolved at ..."`.
- The lump control written as `SourceIsUniform` at `source <- lump` instead of the line
  `LumpIsUniform` the brief names, for the cone match.
- `NoAlternativeAtZero`, `RatioNonNegative` and their two controls added (from report-theory.md's
  list); `S : U` bound by the census `[UnitList]`, since `unitListType : U := UnitList` is refused
  by 4.R4.
- A type a census lists is no model home (tester.py `model_homes`).
