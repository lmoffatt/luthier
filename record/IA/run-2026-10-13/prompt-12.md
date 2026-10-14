# run.py bite 12: --checked, the refinements of an extern's type tested at the crossing, brief for an Opus agent

Written 2026-10-15 by the coordinating session (luthier-3e). 12.S18: "`--checked` tests every
value an extern returns against the refinements of its type as it crosses the bridge (L11.2)";
4.R5 (each refinement in an extern's type is an obligation on its value); 10.S11. The naive
review (`record/IA/review-naive-2026-10-15/C.md`, A28/B19, A26/B17, B25) found typed crossings
that fall through unchecked (`String`, `Unit`, a bare value at `Maybe`, `Nat` negative, scalar
`Int` out of 64 bits) and the refinements (`RankFloor`, `Positive`, `VecOf n`'s length) read as
their bases.

## The prompt

Read `CLAUDE.md` first, then 12.S18, 4.R5, 10.S11, L11.2 in `docs/principles.md`, the review's
rows named above (C.md and the items in A.md and B.md), `src/luthier/run.py` (`typed_from_host`,
`typed_to_host`, `record_from_host`, `array_from_host`, the `TypedExtern`'s declared type and
how a subtype's predicate could be evaluated by the Runner), `src/luthier/elaborate.py` at
`Subtype` (the predicate as a term). Nobody else edits now: change `src/luthier/run.py`,
`src/luthier/cli.py`, `tests/test_run.py`, programs under `tests/run/`.

1. Always (not only under `--checked`, since these are shapes, not laws): a declared `String`,
   `Unit`, `Nat`, scalar `Int` (64 bits, 11.S8) and `Maybe` (no bare value) are checked at the
   crossing in both directions as `Float64`, `Int` and `Bool` are; a declared type that matches
   no branch raises instead of falling through to the untyped reader (A28/B19); the token slot
   accepts only the run's token (A24/B18).
2. Under `run --checked` (12.S18): every value an extern returns at a declared subtype
   (`{ x : T | p x }`, including the named ones `Positive`, `RankFloor`, `VecOf n`, `PsdAt`) has
   its predicate evaluated by the Runner on the crossed value, before the value enters the
   program; a refuted predicate refuses the run naming the extern, the route, the type and the
   value (10.S11); the run's record carries `checked: true` and the count of refinements
   tested per route. Without the flag, as today (the refinement an obligation the certificate
   of the extern's laws covers, 4.R5). The default of the flag is a parameter of the demand
   (P11): off, say so in the help.
3. Tests: each shape check in both directions with a control; `--checked` on a host returning
   a negative where `Positive` is declared (refused, the message), on a `VecOf 3` returning two
   entries (refused), on an honest one (runs, the record's count); `vector_norm.lut` and the
   fit's slow test under `--checked` (paste the count of refinements tested for the fit).

Check: `PYTHONPATH=src python3 -m pytest tests/test_run.py -q`, then the suite. Do not commit.
Report in your final message.
