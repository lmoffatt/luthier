# run.py bite 12: --checked and the shape checks at the crossing: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-12.md; saved by the coordinator.
Files: `src/luthier/run.py`, `src/luthier/cli.py`, `tests/test_run.py`, new `tests/run/checked.lut`,
`tests/run/checked_host.py`. Checks: test_run 124 passed; the suite 687 passed; the fit under
`--checked` 176 s, validate_graph's slow test passes.

Shapes, always on: `String`, `Unit`, `Bool` both ways; `Nat` ≥ 0; scalar `Int`, `Nat`, `Fin` in
64 bits (11.S8); `Maybe` outbound; `List` and pairs inbound; the token slot accepts only the
run's token (A24/B18); an unsigned array in 64 bits and an `Int` array at `Nat` non-negative
(B17); a declared type matching no branch raises instead of falling through (A28/B19). The
tester shares the Runner, so it gets them too.

`run --checked` (12.S18): `from_host` runs `Runner.refine`, which collects the subtype
predicates as `resolve` unfolds them (named subtypes, families like `VecOf n` and `PsdAt m fl`,
refined records) and evaluates each on the crossed value before the program sees it; a refuted
predicate raises `Refused` naming the extern, the route, the type, the predicate and the value
(`--checked: negative (python:run.checked_host.minus_one) gave -1.0 where Positive is declared:
0.0 < x is false ...`); `TypedExtern` gained `name`; the record carries `checked` and, under the
flag, `refinements` (route to count); the flag off by default, the help says it is the demand's
parameter (P11). The fit on graph_noA2 under `--checked` tested 179 refinements (the three
callbacks 36, 71, 71; the maximizer's result 1).

Open for Luciano: a bare value at `Maybe` is still read as `just` ([proposed] in the code):
`tables.py`'s `parse` returns a table or None and `Table.cell` a pair or None, and the fit and
validate_graph read their CSVs through them; refusing would break both unless tables.py
returns `host.Just`. Decide: strict bridge with tables.py changed, or the docstring saying a
bare value is `just`.

Choices of the agent: a callback's arguments tested under `--checked` like a result, counted
under "<route> callback <position>"; array entries tested when the program reads them, the
`VecOf n` predicate at the crossing; theory laws (`Table`'s, `Plot`'s) not tested, only subtype
predicates; `Nat`'s refinement a shape check, not counted; `_type_shown` for the messages;
`command(record=True)` in the tests. Left: 4.R5, 10.S10 and 11.S8's text ("run --checked"
proposed or missing; 11.S8 arrays only), for the coordinator.
