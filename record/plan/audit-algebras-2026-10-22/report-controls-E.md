# Report of Agent E (examples and arrays): a refuted model for each uncontrolled conjunct

Brief: prompt-controls.md; list: uncontrolled-2026-10-26.tsv. Claude Sonnet 5.5, 2026-10-26.
Run: `luthier test --no-cert` on the new lines only (a scratch copy of arrays_controls with the old
`test` lines removed, ~/.cache/luthier-controls/E/scr/arrays_new.test.lut, 6 s; the full
arrays_controls file ran 14 minutes without finishing and was stopped), and on the whole of
tape.test.lut, numbers_controls and tables_controls. Nothing re-certified; no store written (certify
of the tape was run on a copy in ~/.cache/luthier-controls/E/concepts for the printed output).
Every new control below is refuted at the conjunct it targets, and the other conjuncts record "held"
except where said.

## Per law, the controls added

arrays_controls.test.lut (commit "Arrays: controls ...")
- VecIsAnObject, Symmetric: `noLongerVec` (x equal to y when x.n <= y.n; reflexive, transitive, not
  symmetric), pair (1-vector, 2-vector). Refuted at Symmetric alone.
- VecIsAnObject, Transitive: `nearLengthVec` (lengths differ by at most 1), chain of lengths 0, 1, 2.
  Refuted at Transitive alone.
- MatIsAnObject, Symmetric and Transitive: the same two equalities on the number of rows
  (`noFewerRowsMat`, `nearRowsMat`). Each alone.
- VecIsAFunctor, MapCompose and MatIsAFunctor, MapCompose: `valueOneVecFunctor`,
  `valueOneMatFunctor`, maps that read an entry equal to 1 as "the first entry". MapId holds on the
  census (5, -1) and (1) and MapCompose is refuted with g = twice, h = negated: (5, -1) goes to
  (-10, -10), not (-10, 2). Each alone. A total, value-blind model cannot do this (see decisions).
- VecIsTabulated, AtBuild: `zeroEntriesTabulation` (right length, entries 0). Alone (SizeBuild held).
- SymmetricIsAnEqualizer, Equalizes: `bumpedInclusion` (include adds 1 at (0, 1), restrict takes it
  off). Alone: RestrictIncludes and IncludeRestricts held. The restriction's result is then not
  symmetric, and the tester did not check the refinement of the equalizer's object.

numbers_controls.test.lut: AbsDistanceIsAMetricWithin, WithinZeroOnEqual (`distanceOffDiagonal`, 1
added on the diagonal) and WithinSymmetric (`distanceOneWay`, doubled when a > b), each alone.

tables_controls.test.lut: TableIsAnObject, Symmetric (`noMoreRows`, tables by row count) and
Transitive (`nearRows`), each alone, with a pair and a chain inside the relation.

docs/concepts/tape.test.lut (commit f56bbf1):
- Tape, ReadingSymmetric: `lopsided` (reading times 1 + 2^-52 when a > b); alone (MetresWithin's
  bound has room for one epsilon).
- MarkIsAMetric: `flatMetric` (d = 0), refuted at MetricIndiscernible alone (the old vacuity was the
  premise: `hookedMetric` never gives a zero distance); `oneWayMetric` at Commutative alone;
  `squaredMetric` at Triangular alone; `negativeMetric` at MetricNonNegative and at Triangular.
  Commutative was not in the tsv but `hookedMetric` is symmetric and did not see it, so I gave it a
  model too.

Docs: docs/concepts.md 6.3 (the certify output, from the 8-control run: "2 laws, 8 controls, 10
lines ran"; the entries' text is the real one, shortened to the first three lines), the controls
paragraph of 7 and 7.1 (the stale count); docs/spec/07-tests.md 7.R1 now names the directive that
exists and `--seed --fuel --deep --no-cert` (12.S15).

## Conjuncts still uncontrolled, with why
- sonolocalizacion JoinOnFirstEnd and JoinOnSecondEnd, PullbackUnique: no total model breaks it
  without breaking PullbackProjects too. Projects at the listed agreeing pairs forces `first` to be
  onto the rows (every row agrees with a node), hence a bijection, and `pair` its inverse on them;
  then `pair (first k, second k) = k`. So Unique follows from Projects here (an axiom-level
  consequence at this census, argued, not run). Listed, not forced.
- Nothing else of E's: the tsv's other 16 conjuncts have a refuted model. `check -v` cannot show the
  count until the coordinator's wave writes the stores.

## Decisions taken on my own (none needs Luciano; all undone by one commit)
1. MapCompose models are value-aware (they test an entry against 1). MapCompose follows from MapId by
   the free theorem of the type for any model that does not look at values, so no other model could
   refute it. The census of the control (xs, g, h) is the control's own, not the laws' (the law's
   census cannot trigger the break).
2. `negativeMetric` is accepted for MetricNonNegative although it is also refuted at Triangular
   (non-negativity follows from the other four; stated in the core only "for the negative control").
3. `lopsided` relies on one epsilon of room in MetresWithin (2^-52 relative); it holds with the
   present doubles bound and would stop isolating ReadingSymmetric if that bound were tightened.
4. Spec 7.R1's sentence rewritten, not just trimmed: it said "there are no bindings and no profile".
5. The tape's printed certify output is from a copy, so the repo's tape.cert.json is untouched and
   stale until the wave (it lacks the 5 new control entries).
