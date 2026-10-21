# Brief: the core's bite 7, the list library and `<>`

Read `CLAUDE.md` first (if you are not Claude, read "the agent" where it says Claude), then
`record/plan/core-2026-10-17/execution.md` sections 0, 3 (3.7 the list library), 6 (bite 7) and the
paragraphs of 2026-10-18; `report-bite-6.md` beside it (bite 6 already put the minimal list bodies
in `lib/core/lists.lut` and named the internal map `mapKernelList`); `record/decisions.md` at
D-2026-10-18-b (names per concept), D-2026-10-21-a (the semigroup's operation is `<>`).

Build bite 7 as section 6 describes it, with D-2026-10-21-a:
1. `<>` is the operation of every semigroup and monoid: lists, strings and any other. Add it to the
   grammar (grammar.lth's precedence levels, at the level of `+`, associating like Haskell's `<>`,
   to the right) and to the parser through the grammar, with its spec text in chapter 2; it
   resolves by type through the structure's model (rule 2.2). `+` stays only for commutative
   additive structures; `+` on `String` or `List` is refused by check with a message naming `<>`.
2. Every use of `+` on strings in src/luthier/lib, examples and tests moves to `<>`; re-certify
   what moves.
3. The list library of section 3.7, written once over the container structures; `ListIsTheFreeMonoid`
   over its model; `appendList` and `foldInto` gone; the accept program of section 6 uses `<>`
   where it said `+`.

Accepted when: section 6's criteria for bite 7 (with `<>` for `+`); a reject program for `+` on
strings; `python -m pytest -q` passes in full (the count of the last full run, in report-bite-6.md or
the coordinator's verification, plus yours); `python3 scripts/check_spec.py` prints only its known
finding; `luthier certify` over every `tests/tester/*.test.lut` prints 0 lines ran for every
non-fixture program after your wave; `python3 scripts/core_metrics.py` counts in the report. Another
agent works on bite 8 at the same time in numbers.lth, numbers_model.lut, algebra.lth and their test
programs: touch none of those, and retry a commit that fails on .git/index.lock. Small commits: a
subject, a blank line, one body line, and a Co-Authored-By line naming you, staged by path. If you
cannot write to .git, do not commit: list the commits to make in your report. Report:
`record/plan/core-2026-10-17/report-bite-7.md`.
