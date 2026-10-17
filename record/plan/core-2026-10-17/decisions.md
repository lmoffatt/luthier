# The new core: what is still open

2026-10-17, Claude Fable 5.1, on the brief `prompt-design.md`; revised 2026-10-18 for
D-2026-10-18-a (the core alone, to its measurable end) and D-2026-10-18-b (the whole core a prelude,
names per concept resolved by the type's model, no collisions), which decided question 1 of the
first version otherwise than recommended; that question is closed. The design is in `execution.md`
beside this file. Questions 2 and 3 are still with him; 4 and 5 are what D-2026-10-18-b leaves open.

**2. The word "metric".** generators.lth already has a `Metric`: the placing of a uniform draw into an
interval (`linear`, `log`; spec 7.S2, 7.S4, 7.R1 call it a metric). D-2026-10-17-f puts the metric
space in the core under that name, and in the prelude the two cannot coexist. Recommended: rename
the generators' to `Placement` (`LinearPlacement`, `LogPlacement`), so the word stays where
mathematics uses it; the test lines keep `SampledMode linear` unchanged. Cost: three sentences of
chapter 7 reworded by the spec's agent, and `test.lth`'s `SampledMode : Placement -> Mode`. The
alternative, `MetricSpace` for the core's, costs nothing now and leaves the wrong structure holding
the word.

**3. The form of a structure.** D-2026-10-17-b says a structure is a conjunction of properties
(`Monoid = Associative & Neutral`). The kernel does not reduce a `&` of partially applied laws
(report-bite-2.md: `luthier eval` leaves it stuck) and the tester quantifies a conjunction's variables
as one law's, so the design keeps a record of the structure's data and one line per law applying the
property to a field (`MonoidAssociative (M) (o) (m : Monoid M o) (x y z) := Associative M o m.combine
x y z`). The property's text is written once; the cost is about sixty one-line wrappers across the
core and a longer name on each test line. The bare form needs the tester to split a `&` into its
conjuncts, each with its own variables: code. Recommended: the record form now, the bare form when
the tester allows it; one commit per structure undoes it.

**4. Generic functions over a structure.** D-2026-10-18-b resolves the names of a structure (`map`,
`size`, `d`, `plus`) by the type's model. The functions written once over a structure (`all p xs`,
`member x xs`, `lookup k kvs`, `sum xs`, written against `Foldable` and `Object`, L7.6) are not
fields; for them to be called as the fields are, a parameter whose type is a structure (`(f :
Foldable F)`, `(o : Object A)`) must be filled from the type's model when the call omits it, and
passed by name (`(o <- parity)`, the surface's named argument) when it is not the type's own.
Recommended: yes, this is Haskell's instance resolution and it is what removes `(o : Object A)` from
every call of a property; cost: the typing bite (execution.md, bite 4) must infer the type of the
container at every call, which it must do for the fields anyway. The alternative, passing the
structure by hand (`all listFoldable p xs`), is the manner of Java D-2026-10-18-a names.

**5. The list's append.** The monoid operation of `List A` is `combine` (the one name of `Monoid`).
`String`'s monoid is already written `+` in core.lut. Recommended: `operator + := combine` at
`List A` too, so `xs + ys` reads as `s + t` does and `combine` stays for a generic law; cost: one
operator act in lists.lut and `+` meaning concatenation on a third type. The alternative keeps
`combine xs ys` at every use (about 30 places today).

**Note.** D-2026-10-17-f writes the doubles' associativity within `gamma2 (|x| + |y| + |z|)`. Higham's
Lemma 3.1 puts each side within that of the exact sum, so the two sides differ by up to twice it, and
computing the difference and the magnitudes in floating point adds `(1 + u)^3`; bite 2 certified the
instance at `3 gamma2 (|x| + |y| + |z|)` (report-bite-2.md), and bite 8's control of a bound too
small will show whether `gamma2` alone holds (P11: the bound is the claimant's parameter, tested;
L9.14 (every law with a control)). Nothing to decide unless the smaller bound is wanted on the record.

No conflict between principles found that the decisions do not settle. The design's own choices are
listed in `execution.md` §8; each is undone by one commit. One finding for the order of work, not a
question: resolution by type needs the elaborator to infer the type of an argument at every call,
and today it falls back silently when it cannot (`x + "a"` passes `check`), so the typing bite that
item 39 deferred until after the next tag is now the core's next code bite (execution.md, 2.3 and
bite 4).
