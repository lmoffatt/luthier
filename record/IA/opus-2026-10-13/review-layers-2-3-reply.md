# Reply to the internal review of layers 2 and 3

2026-10-13, by Claude Fable 5.1 (session luthier-03), on `review-layers-2-3-report.md` (c8d0ee9).
Each finding was checked against the file before it was taken. Nothing in it needs Luciano: every
change is reversible and follows a decision already taken (D-2026-10-13-a for the world, 7.S10
and 7.S12 for tests, 4.R10 for operations as fields).

## Taken, with the commit

| finding | what changed | commit |
|---|---|---|
| world.1, world.2, world.3, world.6, world.8, world.9 | world.lth draft 1: laws over the library's representation `S` and an action's description `S -> S * A`; no token used twice, no action in a law, no `act`; `A` a parameter; places any string; `WriteThenRead` unguarded; chapter 10 updated | 0c920f0, chapters at the last commit |
| world.4, world.5 | `Externs`: applied exactly when settled or provisional; a provisional extern's verdict is an assumption (not validated); the verdict and the identity take the hash | 0c920f0 |
| world.7 | `world_model.lut` with `State`, pure descriptions (`console`) and the host's actions (`host`), `readFile` giving `Maybe`; `print` appends a line; the host side (`observe`, `read_file` as `Maybe`) passed to the coordinator | 0c920f0 |
| gen.1 | `pick` gives the last value of positive weight when rounding leaves `u` beyond the sum | 6dae811 |
| gen.2, gen.13 | `Level` a parameter of the certification; the uniform and the serial law stated on it, as statistical laws (7.S17, 7.S18) | 6dae811 |
| gen.3, gen.4 | `pick`, `draw`, `bindingOf` are fields; `Support` has the proportionality law; `Filter` is characterized against its base; `Resolution` has four laws | 6dae811 |
| gen.5, gen.6 | metrics by their invariance: `LinearMetric` translates on any `Interval`, `LogMetric` scales on a `PositiveInterval`; `StartsAtLo` | 6dae811 |
| gen.7, gen.8 | the size is the type's, a parameter of `Exhaustive` and `Sized`; `Exhaustive` is a finite list of all values, each once, so an unbounded type has no model | 6dae811 |
| gen.10, gen.11 | a census is walked in turn, the next seed the next value; `CensusFirst` states the next seed | 6dae811 |
| gen.12 | `Budgets` complete against 7.S8, each positive, the masses in [0, 1); the largest size is the spec's | 6dae811 |
| gen.14 | `UnitInterval` and `OrderedUnitPair` as subtypes | 6dae811 |
| gen.15, gen.16 | `generators_model.lut` with the reference support, filter and resolution; 7.S5 names the files | 6dae811, chapters |
| test.1, test.2 | a run is points or `NotRun` (new in laws.lth, settling nothing); a sampled run has the cases asked or is not run | 33447ea |
| test.3 | the coverage of a run is the weakest of the mode's and each binding's (`Binding.coverage`); exhaustive is `Bounded size`, the box, and `Exhaustive` only when the tester knows the types are finite | 33447ea |
| test.4 | a witness is `Cases` whatever the coverage | 33447ea |
| test.5 | `MetricName` gone, `SampledMode` carries its `Metric`; grades ordered (`below`), the weakest defined | 33447ea |
| test.6 | `test_model.lut` with `grading` | 33447ea |
| test.7 | `CensusMode` gone (a census is a binding); 7.S20 says `test` builds data | 33447ea, chapters |
| lib.1 | core and the libraries anchored by name (`core.lut`, `lib/`), the reject paths not core | last commit |
| lib.2 | `AdmitsAtRefinesAdmits` (b69f640) and `TheoryFileAdmitsATheory` | b69f640, last commit |
| lib.4, lib.7 | an extern found anywhere in a body; the law over `WithExtern` | last commit |
| lib.5 | `DataFileHoldsNoActs` | last commit |
| lib.8 | 12.S1 names `library.lth` and says the record reading is not yet a law | chapters |

## Not taken, and why

- gen.9, the functors of 7.S3 per form with the core's instances: they need the core's types
  (`Bool`, `Fin n`, `List`), which core.lut does not give yet; §8 of generators.lth is todo for
  them. 7.R3's covering array and 7.S6's recorded acceptance rate are the certifier's (step 5).
- gen.8's second half (the grade of a bounded run): taken through `Bounded` and test.3, not by
  refusing the run.
- lib.3, the sample's `one`/`two` unbound: they are the labels of the sum in the theory's field
  type, which program.lth now counts as constructors (dc8a8e5); a negative case with a missing
  field waits for a typing `verifies` can use.
- lib.6, every law a closed case over one sample: as the file says, the generalization is a
  generated file system with the sample as census, as generators.lth §7 does for programs; left
  until there is a generator of file systems.
- test.7's third point, the categories of 7.S12 (not drawn, skipped, premise false): `NotRun`
  covers a run that gave nothing; the per-case categories belong to the entry (spec 6), not to
  `Evidence`.
- "Not sure", `defaultBudgets`: `coveringAbove := 20000` and `drawsPerCase := 10` are proposed
  defaults, and the comment now says so; `tries`, `redraws`, `probes` are the code's.

## For the coordinator

- host.py and run.py: `observe`, `read_file` as `Maybe`, places gone (message sent).
- The review's "Not sure" on 12.S21 against 12.S22 (does checking read a model file?): library.lth
  reads it as 12.S22 does, the checker reads theories only (`CheckingReadsTheories`); 12.S21's
  wording could say so. Chapter 12 is mine; left as it is until the loader runs.
