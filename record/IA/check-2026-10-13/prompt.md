# check.py and luthier check: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`. Step 4.1 of
`record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md`; with it, milestone `v0.2`
is in reach.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (a Codex is changing
`src/luthier/kernel.py`, `tests/test_kernel.py` and `tests/test_elaborate.py`): change only the
files listed below; a failure from another file is someone else's, report it, do not fix it.

`src/luthier/lib/program.lth` states the checker of chapter 4 (`docs/spec/04-static-semantics.md`)
as the theory `WellFormed (a : Alpha) (sb : Substitution a) (e : Elaboration a) (t : Typing a sb) :
{ check : SurfaceProgram -> List Failure, report : SurfaceProgram -> List Report }`, with
`Failure = { rule, name, message }` and `Report = { kind, name, message }`. The rules are the
predicates `violatesR1` to `violatesR12`, which the specimen mirrors; the laws are
`ReportsViolations` over `Violating violatesRk` and `ReportsNoFalseFailure` over `Clean violatesRk`
for the complete predicates (4.R1, 4.R4, 4.R5, 4.R7), and reports "unclaimed" (4.S14),
"provisional", "loose". It uses two holes the specimen supplies: `coreNames : List String` (the
names of core: take them from chapter 3 and 11 and say which list you chose) and
`namePrefix`/`nameSuffix` (the part of a dotted name before its first `.`, after its last). The
theory is stable at ba322cd (later commits only touch comments). Left open on purpose, to be
reported as your choices: 4.R2's type-position half and the full reading by strongly connected
components; `Typing` covers what the rules need, not a whole type checker; 4.R13 and 4.S23 are
elaboration laws of `translation.lth`, not predicates here.

Write its Python specimen, over the existing `luthier.parse`, `luthier.elaborate` and
`luthier.kernel` (do not change them; say in the report what they lack):
1. `src/luthier/check.py`: `check(program) -> list[Failure]` and `report(program) -> list[Report]`,
   one function per predicate `violatesRk`, named after it, its statement in the docstring.
2. `luthier check FILE...` in `src/luthier/cli.py`: `path:line: rule name: message` per failure,
   reports with `-v`, exit 1 on any failure (a parse error counts as one).
3. `tests/test_check.py`: per rule, the laws `ReportsViolations` and `ReportsNoFalseFailure` on
   hand-written violating and clean programs, plus the reports.
4. Connect the hook `CHECKER` of `tests/test_spec.py` to `check.py`, so that every program of
   `tests/spec/` gets its verdict: an `.accept.lut` has no failure, a `.reject.lut` has the failure
   of its rule, with its `-- expect:` fragment where the specification gives one (read
   `tests/spec/README.md` for `-- expect (v0.1)`, `-- expect (proposed)` and `-- verdict`). A
   program whose verdict your checker gets wrong: keep the case, mark it `xfail(strict=True)` with
   the reason, and list it in the report.

Check: `python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then `python3 -m pytest
tests/ -q`; `luthier check src/luthier/lib/*.lth src/luthier/lib/*.lut` (the theory files
themselves; report what it says of them). Do not commit. Report in a few lines to
`record/IA/check-2026-10-13/codex.md`: what you wrote, the counts, the verdict of each program of
`tests/spec/` (a table), every law of `program.lth` not met with its case, and every place where
the theory did not decide.
