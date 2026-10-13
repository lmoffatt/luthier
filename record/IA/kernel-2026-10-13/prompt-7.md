# kernel.py, bite 7: structural `==` on values, brief for a Claude agent

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session, luthier-1b), for an Opus agent launched by it. After bite 6 (codex-6.md).

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only
`src/luthier/kernel.py`, `tests/test_kernel.py`, and write your report; a failure from another file
is someone else's, report it, do not fix it.

`src/luthier/lib/term.lth` (`git log -1 -- src/luthier/lib/term.lth`) states in §5 the law
`PrimStructural`: `==` on two values of a structural type (pairs, records, injections, that is
constructors applied, with concrete parts) steps to `Var "true"` or `Var "false"` comparing part by
part, labels included (spec 3.S17, 4.R8, D-2026-10-12-ak). Today `kernel.py` reduces `==` only on
`Int` and `String` literals (`_OPERATORS`, the `Prim` case) and gets stuck on anything else, which
stops world.lth §5's `agreement` (a comparison of records and pairs). Mirror the law exactly as
term.lth states it: which heads compare, what a differing part or a differing label gives, when
`==` does not step (a lambda, an extern, an open term, a part not yet a value: say what term.lth
says for each, and if it is silent on one, choose the conservative reading, stuck, and report it).
Tests in `tests/test_kernel.py` for each clause of the law, including nested values and the
stuck cases; `tests/eval/` and `tests/test_run.py` still pass.

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_eval.py tests/test_run.py
-q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in a few lines to
`record/IA/kernel-2026-10-13/opus-7.md`.
