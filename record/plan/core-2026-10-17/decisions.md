# The new core: what is still open

2026-10-17, Claude Fable 5.1, on the brief `prompt-design.md`. The design is in `execution.md`
beside this file. D-2026-10-17-b to -h decide the vocabulary, the names, the equality of functions,
the list library, the metric, the universal constructions and the directory; nothing of that is
asked again. Three questions remain that the design cannot settle alone, and one note.

**1. How a file reaches the list library.** `core.lut` encloses the top-level scope of every file
(12.S22: an import names what enters; `core.lut` is the one file whose names are visible unqualified).
The new `core/lists.lut` holds `map`, `filter`, `all`, `member`, `lookup`, `append` and the rest.
Either a file imports them by name, `import "core/lists.lut" map all member` (recommended: 12.S22
has no flat import, and L7.1 (a handful of primitives; everything else a library) keeps the enclosing
scope to what the interpreter provides), or lists.lut joins core.lut as a second enclosing file.
Cost of the recommendation: one import line in about 25 files. Cost of the alternative: a change to
12.S22 and to the loader, and the names `map`, `all`, `at` taken in every file's scope.

**2. The word "metric".** generators.lth already has a `Metric`: the placing of a uniform draw into an
interval (`linear`, `log`; spec 7.S2, 7.S4, 7.R1 call it a metric). D-2026-10-17-f puts the metric
space in the core under that name. Recommended: rename the generators' to `Placement`
(`LinearPlacement`, `LogPlacement`), so the word stays where mathematics uses it; the test lines keep
`SampledMode linear` unchanged. Cost: three sentences of chapter 7 reworded by the spec's agent, and
`test.lth`'s `SampledMode : Placement -> Mode`. The alternative, `MetricSpace` for the core's, costs
nothing now and leaves the wrong structure holding the word.

**3. The form of a structure.** D-2026-10-17-b says a structure is a conjunction of properties
(`Monoid = Associative & Neutral`). The tester quantifies a conjunction's variables as one law's
(tester.py, run.py's enumeration of a theory's laws), and a bare predicate `Monoid A o op e :=
Associative A o op & Neutral A o op e` leaves each conjunct with different variables. The design keeps
a record of the structure's data and one line per law applying the property to a field
(`MonoidAssociative (M) (o) (m : Monoid M o) (x y z) := Associative M o m.combine x y z`), which is
what the runner evaluates today. The property's text is written once; the cost is about sixty
one-line wrappers across the core and a longer name on each test line. The bare form needs the
tester to quantify each conjunct on its own: code, in the file another agent is changing now. Recommended:
the record form now, the bare form when the tester allows it; one commit per structure undoes it.

**Note.** D-2026-10-17-f writes the doubles' associativity within `gamma2 (|x| + |y| + |z|)`. Higham's
Lemma 3.1 puts each side within that of the exact sum, so the two sides differ by up to twice it, and
computing the difference and the magnitudes in floating point adds a factor `(1 + u)^3`; the design
claims `3 gamma2 (|x| + |y| + |z|)` and the first certification tells whether `gamma2` alone would
have been refuted (P11: the bound is the claimant's parameter, tested; L9.14 (every law with a
control): a bound too small is the control). Nothing to decide unless the smaller bound is wanted on
the record.

No conflict between principles found that the decisions do not already settle. The design's own
choices are listed in `execution.md` §8; each is undone by one commit.
