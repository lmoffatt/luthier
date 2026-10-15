# The statistical law's form, theory side: report

2026-10-15, by Claude Fable 5.1, an agent of the coordinating session, on `prompt-theory.md` of
this folder. Inputs: CLAUDE.md, L9.14 and L9.15 (docs/principles.md at aa41e90), D-2026-10-15-a
and -b (record/decisions.md), 7.S17 to 7.S19 (docs/spec/07-tests.md at aa41e90), item 3 and the C
section of record/IA/layer-3-review-2026-10-15/summary-BCD.md, the five files at 6083774.
Commits, one per file: 2d4519e laws.lth, f442e00 generators.lth, 2da386c probability.lth,
f35b275 probability_model.lut, 1283a12 generators_model.lut. No Python changed. The scratch
programs that exercised the form are in the session's scratchpad (`sprt/`), not in the repo;
their lines and results are quoted below so that they can be rewritten.

## The form (laws.lth §4)

The verdict. `StatisticalVerdict = Holds r | Fails r | Unresolved r`, each carrying `Rates`:
`alpha`, `beta`, `delta` and `spent`, the samples the test used. `Rates` is a type alias (4.R4
refuses a plain record at `U`). [proposed] `delta` travels with the rates: `beta` means nothing
without the alternative it is measured against.

The cutoffs. `Sequential = { alpha beta delta : Float64, initial budget : Nat | ... }`, every one
the demand's (D-2026-10-14-c): `alpha + beta < 1` so that Wald's thresholds bracket one; `delta`
in (0, 1) so that the reference alternative is a density with no zero; `initial` the size of each
sample; `budget` the most samples. [proposed] "the initial size" of L9.15 is read as the size of
each sample: the test grows by samples of that size, one more per step, which is Wald's test and
7.S18's repetition continued.

The law as a theory. `StatisticalLaw S = { statistic : S -> Float64, ratio : Float64 -> Float64
-> Float64 }`: the statistic of one sample, and `ratio delta v`, the likelihood of the
statistic's value `v` under the alternative at distance `delta` against the null. Two Boolean
laws, `NoAlternativeAtZero` (`ratio 0 v == 1`) and `RatioNonNegative`. The stream of samples is
not the law's: the form `Statistical S T l draw c` in `Law` carries `draw : Nat -> T -> S * T`
beside the law, as `Forall` carries its type (the seed is the test's, L9.15). The first draft had
`draw` as a field; 4.R3 refused it (no law touched the field), and the spec reads better this way.

The reference alternative, for a law whose statistic is a p-value: density `1 + delta (1 - 2p)`,
`tilt`, and `byPValue` builds the law. [proposed] 7.S17 names an alternative at distance delta and
no form. This one is a density for every `delta` in (0, 1), keeps the ratio within
`[1 - delta, 1 + delta]` so that no single sample settles the test, needs neither `log` nor
`power` (laws.lth imports no model), and lies at Kolmogorov distance `delta / 4` from the uniform.
Drift of the log ratio per sample under the null: about -0.045 at `delta = 0.5` (some 100 samples
to hold at `alpha = beta = 0.01`), -0.19 at `delta = 0.9` (some 24); against a source whose
p-values are all near zero, `log (1 + delta)` per sample (8 samples to fail at 0.9).

The test. `sequential S T l draw c t`: the product of the ratios fails the law at
`(1 - beta) / alpha`, holds it at `beta / (1 - alpha)`, draws one more sample of size `initial`
between the two, and gives `Unresolved` when `spent` reaches `budget`. Evidence gains `Tested :
StatisticalVerdict -> Evidence`; `Settling` gains `StatisticalByTest`: Holds settles Supported (a
sample never confirms, 7.S10, so the grade is Sampled), Fails settles Refuted, Unresolved settles
Unsettled.

Checked on constant streams through `luthier test` (five Boolean laws in a scratch file, all
held): at alpha = beta = 0.01, delta = 0.9, budget 100, a stream of p = 0 fails at 8 samples, p = 1
holds at 2, p = 0.5 is unresolved at 100, p alternating 0.25 / 0.75 holds at 42; all four as
computed by hand.

## The laws rewritten

generators.lth §1. `UniformAtLevel` and `IndependentAtLevel`, Bool laws over every seed, are
replaced by `DrawsAreUniform (r : Random) (c : Sequential) : Law` and `DrawsAreIndependent`, the
form over the stream of draws from a seed (`drawsFrom`, `pairsFrom` give the seed after the
sample); `Random := UniformInUnit & SeedMoves & DrawsAreUniform & DrawsAreIndependent` (a
conjunction with a `Law` part is a `Law`, 5.S6). `uniformPValue` and `serialPValue` stay leaves
declared until a host gives them, as before. `Level` is no longer read by any law; kept this bite
for its importers (tests/tester/generators_laws.lut, probability_laws.lut,
tests/run/scope/label_and_definition.lut, whose test_run.py assertion would otherwise fail), to go
with them [proposed].

probability.lth §5. `UniformAtLevel (d) (l : Level) (vs : UnitList) : Bool` is replaced by
`uniformValues d : StatisticalLaw UnitList` (the p-value of Kolmogorov's tail, the tilt) and
`SourceIsUniform (d : Kolmogorov) (source : Gen UnitList) (c : Sequential) : Law`. The file now
imports `Gen Seed` from generators.lth and the form from laws.lth.

The controls (L9.14), each a model broken on purpose. generators_model.lut: `skewedSample`, the
host's calibrated sample with every value squared (distribution function the square root,
Kolmogorov distance 1/4 from the uniform), and `SkewedSampleIsUniform` beside
`UniformSampleIsUniform (c : Sequential) : Law`; for `Random`, `skewedSource` (a linear
congruential source, values squared) and `rampSource` (seeds step by one, successive draws on the
diagonal), with `SkewedSourceIsUniform` and `RampSourceIsIndependent`, stated until the leaves
have a host. probability_model.lut: `lump`, every value 0.9 (the lump probability_laws.lut already
names as no sample of the uniform), and `LumpIsUniform`.

Checked on the host through `luthier test` (a scratch file, the verdict's code as the refuting
case of a Boolean law over a bounded `Nat`): at alpha = beta = 0.01, delta = 0.9, initial 5, budget
60, seed 20261014, `sequential` on `uniformSample` holds at 7 samples, on `skewedSample` fails at
14, on `lump` fails at 8. The chain runs end to end today with no change to the tester, when the
cutoffs and the seed are given by hand.

## Accepted when

- Every changed file parses and `luthier check` is clean: yes, the five.
- `luthier check` on the importers: clean on every tests/tester/*_laws.lut, the other tests/tester
  files, src/luthier/lib/{test,certification,plan,belief,optimization}.lth and
  examples/sonolocalizacion/*.lut, except distances.lut:46-47 (4.R9 `pairI`, `pairJ`), which was
  the same before this work (baseline at 6083774). `check` does not verify that an imported name
  exists, so nothing breaks at check; at run time: tests/tester/probability_laws.lut's two
  `test "UniformAtLevel"` lines name a law that no longer exists (the file loads; those lines
  cannot run), and tests/tester/generators_laws.lut's `UniformSampleIsUniform` line gives
  "not run: c : Sequential: no value of Sequential in 2000 tries (7.S6)", the tester drawing a
  cutoff it should bind (verified by running the file; its other six lines ran as before).
- No Python changed: none.

## Decisions taken on my own

The alternative's form (the tilt) and its place in laws.lth; the stream outside the law
(`Statistical` carries `draw`); `delta` in `Rates`; `initial` read as the sample size; `delta < 1`
strict; `Level` kept this bite; the names `DrawsAreUniform`, `DrawsAreIndependent`,
`SourceIsUniform`, `Tested`, `StatisticalByTest`; the four controls. Each is one commit to undo
and nothing depends on it yet; each is marked `[proposed]` in the file where the spec leaves the
reading.

## What the tester must do, one line per definition (the next bite)

- `Sequential`: never drawn; bound by the demand as a census of one in the profile, as `tol` and
  `level` are today (`cutoffs : Sequential := { alpha := 0.01, beta := 0.01, delta := 0.9,
  initial := 200, budget := 60 }` is a reasonable first demand; refuse a line that leaves it
  unbound rather than report "no value in 2000 tries").
- `Statistical S T l draw c`: when a definition's result type is `Law` and its body, at the
  bindings, reduces to this constructor, run `sequential S T l draw c seed` with the spec's seed
  as the state (`T` must be `Seed`; refuse another `T`), once per line, no cases to draw.
- `sequential`: run in Luthier through the Runner (it is a definition, and ran in 7 s for three
  lines on the host at size 5); `spent` and the rates come back in the verdict.
- `Tested v`: the line's evidence, with `alpha`, `beta`, `delta` and `spent` written in the
  entry (7.S17: the verdict carries its error rates in the certificate).
- `StatisticalByTest`: Holds gives Supported and the grade Sampled over `Drawn seed`; Fails gives
  Refuted; Unresolved gives Unsettled, no grade, the budget spent in the entry.
- `NoAlternativeAtZero S`, `RatioNonNegative S`: Boolean laws of `StatisticalLaw S` with a type
  parameter; run with `l` bound to `uniformValues numpySort` and `x` to `unitList`.
- Controls: `SkewedSampleIsUniform`, `LumpIsUniform` with `(control <- true)` pass on Fails; the
  rate of Holds over `seedsPerControl` seeds is the observed beta of 7.S19.
- `DrawsAreUniform`, `DrawsAreIndependent`, `SkewedSourceIsUniform`, `RampSourceIsIndependent`:
  wait for a host for `uniformPValue`, `serialPValue` and a host `Random` (next, uniform); the
  host's source today gives samples, not a seed's successor.
- Test lines: generators_laws.lut's `UniformSampleIsUniform` with `c` bound to the cutoffs;
  probability_laws.lut's two `UniformAtLevel` lines replaced by `SourceIsUniform` with `d`
  (numpySort), `source` (uniformSample; lump as the control) and `c` bound; then drop `level :
  Level` and the `Level` imports, `Level` from generators.lth, and label_and_definition.lut's
  `Level` import (any other name of generators.lth serves its purpose, `Seed`).
