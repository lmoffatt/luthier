# check.py bite 5: array shape refinements, subtypes across imports, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). On the port's report
(`record/IA/slice-port-2026-10-14/report.md`, "What check says") and the slice theories' report
(`record/IA/slice-theories-2026-10-14/report.md`, the refusals it names as the checker's). To
launch after the leftovers agent's report (`record/IA/theory-leftovers-2026-10-14/report.md`)
lands, which may add what check.py must mirror.

## The prompt

Read `CLAUDE.md` first, then the three reports named above (their check sections), then
`docs/spec/04-static-semantics.md` (4.R3, 4.R4, 4.R9, 4.R11, 4.R13) and `src/luthier/lib/program.lth`
for the predicates named. Other agents edit `run.py`, `docs/spec/` and theory files meanwhile:
change only `src/luthier/check.py`, `tests/test_check.py`, the `LIMITATIONS` table of
`tests/test_spec.py`, and write your report.

Judge each and fix what is the checker's, with a test:
1. 4.R3 refuses a refinement on a vector's length that does not touch `f` (`VecOf`, `MatOf`,
   `MatRows`, `Square` in arrays.lth; `Positions`, `Pairs`, `PairsAmong` in the port): is a
   subtype's predicate a "law" for 4.R3's untouched-fields rule, or is 4.R3 about theories only?
   Read 4.R3 and program.lth's `untouchedFields`; if the spec restricts it to theories (records
   defined by laws), the checker over-applies it; if the spec means every record refinement, say
   so and leave it, naming the sentence.
2. 4.R9 across imports: an imported subtype not seen as refining its imported base, and 4.R11's
   flow refinement not seen across an import (the port's smallest case: `a.lut` with `R`, `P`,
   `S : U := { r : R | P r }`; `b.lut` importing `R S` with `f (r : R)` and `s (r : S) : Int := f
   r` refused). `base` must look through imported definitions as it looks through the file's own.
3. 4.R4 on `primitive` bodies (check.py lists `extern`, not `primitive`; 11.R2, 3.S39) and 4.R13
   on `operator` targets whose definition is typed inline (`declared(p, g)` None): both named as
   the checker's by the slice report.
4. The gap `x : Int := "three"` passes: which rule refuses a body whose type is not the declared
   one (4.R6 or 4.R9 on a literal)? If check.py has that rule and misses literals, fix; if no
   rule covers it, say so (the typing bite is after v0.2).
Then run `luthier check` on `src/luthier/lib/*.lth src/luthier/lib/*.lut examples/hello.lut
examples/sonolocalizacion/*.lut` and list what is left, by cause.

Check: `PYTHONPATH=src python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then
`PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report to
`record/IA/check-2026-10-13/report-5.md`.

## Addendum (after the leftovers report, f8c5f40)

`record/IA/theory-leftovers-2026-10-14/report.md` names what check.py must mirror from
program.lth at 5f33db8, and more of the checker's: read it whole first. In order:
- group 1: `fields_read` takes the field after the first `.` (`namePrefix(name.split('.', 1)[1])`);
- group 2: `law_names` counts the constructors named by the patterns of a claimed law's own
  matches and clauses (program.lth `lawNames`, [proposed]);
- group 5: the lambda case of `violatesR3` applies only when `lambdaIsPredicate` holds (mirror
  its four clauses);
- 4.R3 `untouched`: a projection `e.f` counts as touching `e` (1.S7; count `namePrefix`), which
  clears arrays.lth's shape refinements (item 1 above is answered: the checker's and program.lth's;
  a theory agent adds the same to program.lth in parallel, do not touch it);
- 4.R13 `rivalModel`: compare `typeOfAct`, not `declaredSurface` (clears every `operator` target);
- 4.R4: `primitive` accepted as `extern` is (11.R1, 11.R2);
- 4.R9 in arrays.lth, three causes: (a) an unannotated `fn k { ... }` where `Fin n -> T` is
  expected, the hole must not be compared as a type; (b) a `Fin n -> A` inside a subtype's base
  elaborated as `implies`, the same `arrows` reading as bite 3b part 1; (c) substituting `n := k`
  into `{ m, n, f : Fin m -> Fin k -> Float64 }` captured the record's own field `n`;
- 4.R9 `sameParse` in tables.lth: `Maybe Table` with the theory head read as its record, not `U`;
- `base` and `Concrete`: read an imported name's definition when computing `base` (12.S22), if
  the loader gives you the imported file; if check.py loads no imports today, say what it would
  take and leave group 3's two cases listed.
Item 2 above (subtypes across imports) belongs with that last point.
