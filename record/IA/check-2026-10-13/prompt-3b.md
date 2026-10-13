# check.py, bite 3b: name the leftovers and the 4.R9 refusals of library.lth, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session, luthier-1b), launched by it with `codex exec`. The second half of `prompt-3.md`, which a
previous run left undone when its quota ended (its first half landed at f282156), plus a finding
of the library.lth subagent (`record/IA/opus-2026-10-13/library-file-policies-report.md`, reading 6).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time (a Claude agent on `parse.py` and
`surface.py` for the pattern on `<-`; Codex on the inventory of another repository): change only
`src/luthier/check.py`, `tests/test_check.py`, the `LIMITATIONS` table of `tests/test_spec.py`, and
write your report; a failure from another file is someone else's, report it, do not fix it.

1. The library.lth subagent reports (reading 6) that `luthier check src/luthier/lib/library.lth`
   raises 4.R9 on a helper that takes `(l : Loader)`, and on a helper passed as a function
   argument when its parameters use the imported alias `SurfaceProgram` (`f2 okAll` fails, `f2
   l.admitsAt` passes). Reproduce both on the file as it is (b69f640 or later), say whether the
   refusal is the checker's (4.R9 in `docs/spec/04-static-semantics.md` and `program.lth`'s `base`
   read strictly) or the theory's, and if the checker's, fix it with a test for each case.
2. Run `luthier check src/luthier/lib/*.lth src/luthier/lib/*.lut examples/hello.lut` (it takes a
   few minutes) and, for every failure left, print what the theory's author needs to judge whose
   it is: for 4.R9 the application and the two bases compared; for 4.R3 the field and the record;
   for 4.R2 the name reported and where it is read; for 4.R6 the body's inferred type and the
   declared one. Put that in the report, by file, grouped by the cause you see (one line per
   group, the cases listed under it), so the coordinator can send each group to program.lth or to
   the theory with one message.

Check: `python3 -m pytest tests/test_check.py tests/test_spec.py -q`, then `python3 -m pytest
tests/ -q`. Do not commit. Report to `record/IA/check-2026-10-13/codex-3b.md`.
