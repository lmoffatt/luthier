# A naive review of the world, with and without the principles: brief for three Sonnet agents

Written 2026-10-15 by luthier-5d (a fork of the coordinating session, Claude Fable 5.1) on
Luciano's proposal of the same morning ("revisar las implementaciones con dos agentes naive:
uno que siga estrechamente los principles y otro que los ignore y simplemente mire las
implementaciones, y un tercero que analice la diferencia") and luthier-3e's design, with the
guard of `record/principles-candidates-2026-10-15.md` C2: the judge classifies and attributes,
it does not rank, and "a law that could have been stated and was not" is a class of its own.
The coordinator launches A and B in parallel, then C; all three are Sonnet; one run is a pilot.

## The artifact (the same for A, B and C)

The world of Luthier as written in his absence: `src/luthier/lib/world.lth` and
`world_model.lut`; `src/luthier/host.py`; and of `src/luthier/run.py` only the bridge and the
gate: lines 400 to 460 (`TypedExtern`, `HostRecord`), 680 to 1060 (`to_host`, `typed_to_host`,
`function_to_host`, `host_partial`, `cross_out`, `record_to_host`, `from_host`,
`typed_from_host`, `array_from_host`, `record_from_host`) and 1510 to 1600 (`certification`,
`refuse_provisional`). Read these with `sed -n`, not the whole file. The programs that run on
it: `examples/hello.lut`, `tests/run/callbacks.lut`, `tests/run/record_of_functions.lut`,
`tests/run/host_function.lut`, `tests/run/observe.lut`.

The specification items world.lth cites: `docs/spec/10-world.md` (10.S1 to 10.S10, 10.S12,
10.S13), `docs/spec/03-kernel.md` 3.S23 and 3.S40, `docs/spec/12-files-and-tools.md` 12.S18
and 12.S23, `docs/spec/04-static-semantics.md` 4.R5, `docs/spec/06-certification.md` 6.S8 and
6.S10, `docs/spec/02-grammar.md` 2.S17. Read them by grep of the item number, not the chapters.

Every agent: read only; change no file; write exactly one file, named below, and do not commit
(the coordinator commits). Do not read `record/`, the other agents' reports, or the plans. Do not
read `git log`. Be economical: the artifact whole, the spec items by grep, nothing else beyond
what your consigna names.

## Consigna A (verbatim; write `record/IA/review-naive-2026-10-15/A.md`)

Read `CLAUDE.md` and `docs/principles.md` whole, then the artifact and the specification items
named above. Then review the artifact. List what you would change and why, numbered, each item
with the file and the line, one paragraph each, in the order you found them. Include anything:
a wrong behaviour, a missing case, a reading of the specification you disagree with, something
stated that should not be, something not stated that should be, a cost paid for nothing, a name
that misleads. Say for each what the change would be. Do not rank. Do not group. Do not write an
introduction or a conclusion: the list is the report.

## Consigna B (verbatim; write `record/IA/review-naive-2026-10-15/B.md`)

Read the artifact and the specification items named above. Then review the artifact. List what
you would change and why, numbered, each item with the file and the line, one paragraph each,
in the order you found them. Include anything: a wrong behaviour, a missing case, a reading of
the specification you disagree with, something stated that should not be, something not stated
that should be, a cost paid for nothing, a name that misleads. Say for each what the change
would be. Do not rank. Do not group. Do not write an introduction or a conclusion: the list is
the report.

## Consigna C (verbatim; write `record/IA/review-naive-2026-10-15/C.md`; launched after A and B)

Read `docs/principles.md` whole (its Terms, the organizers G0 to G2, the principles L1 to L14
with their clauses), then the two reports `record/IA/review-naive-2026-10-15/A.md` and `B.md`,
then the artifact and the specification items named above only where you need them to tell
whether two items say the same thing. You do not rank and you do not say which report is
better: that judgment is Luciano's. You classify every item of both reports into exactly one of
these classes, and you write one table with one row per item (the item's number in its report,
its line in the artifact, its class, and one sentence):

1. Found by both (name the two items; count once).
2. Only by A, and attributable to a principle: name the clause (as `L11.2`, `L5.18`) whose
   reading produces the item; say in one sentence how.
3. Only by A, not attributable to any clause of the principles.
4. Only by B.
5. A law that could have been stated and was not: an item, from either report, that asks for a
   law (a property the theory could state and the specimen could be certified against) which
   world.lth does not state. This class takes precedence over the others: an item that is a
   missing law goes here whoever found it, with the class it would otherwise have in the
   sentence.

Then, for each item, one more column: whether it would change a decision recorded in the
artifact's comments or in the specification items (say which, by its number), or is a change
with no decision behind it (a fix, a rename, a comment). Do not call anything cosmetic or
minor. After the table: three lines of counts (per class, per report) and nothing else. No
recommendation, no summary, no introduction.

## What the coordinator does with the three files

Commits them verbatim under this directory (P3). Puts in front of Luciano one screen: C's
counts, the items of class 5, and the items of class 2 with their clauses; the rest stays in
the files. The ranking and whether to repeat on `optimization.lth` with `lm.py` are his.
