# elaborate.py, bite 6: & over a Law, an arrow over a declared subtype, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). On check bite 6's report
(`record/IA/check-2026-10-13/report-6.md`, "What the typing rules now refuse"): two limits of
the elaborator named there.

## The prompt

Read `CLAUDE.md` first, then that report section, `docs/spec/05-laws.md` 5.S6 (a combination of
laws lifts each Boolean part), `docs/spec/04-static-semantics.md` 4.R6, `src/luthier/lib/translation.lth`
where it states the type of `&` (grep `Conjunction`, `&`) and of an arrow in type position, and
`src/luthier/elaborate.py` (`infer` of `&`, the reading of `A -> B` as the Bool implication, the
operator's declared function type). Other agents edit `run.py`, `tester.py` and their tests
meanwhile: change only `src/luthier/elaborate.py`, `tests/test_elaborate.py`, the `LIMITATIONS`
table of `tests/test_spec.py`.

1. `infer` of `&` joins Boolean laws only, so a conjunction with a `Law` part (`SupIsLeast` in
   algebra.lth's `CompleteOrderedField`) types as `(F : U) -> ?` and 4.R6 refuses the theory. By
   5.S6 and translation.lth, give the conjunction its type when a part is a `Law` (laws.lth) as
   when all are Bool: say what translation.lth states and mirror it; if it is silent, state the
   reading in a comment marked [proposed] and cite 5.S6.
2. With `Float64 : Real` declared (core.lut), `Float64 -> Float64` in type position is read as the
   Bool implication, so core.lut's `operator + := floatPlus` and the three others get no declared
   function type. A name declared at a type that is itself a type (`Real : U`, `Float64 : Real`
   refining it, 11.R1) is a type; an arrow between types is the arrow (check.py's bite 3b part 1
   already reads `implies A B` in type position as the arrow: do it at the source instead, and
   say whether check.py's `arrows` can then go). Test with core.lut's four operators, and with the
   port's `examples/sonolocalizacion/*.lut` still elaborating as before.

Check: `PYTHONPATH=src python3 -m pytest tests/test_elaborate.py tests/test_check.py
tests/test_spec.py -q`, `PYTHONPATH=src python3 -m luthier.cli check src/luthier/lib/algebra.lth
src/luthier/lib/core.lut` (paste the result), then `PYTHONPATH=src python3 -m pytest tests -q`.
Do not commit. Report in your final message.
