# kernel.py, bite 1f: matching on constructors, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only `src/luthier/kernel.py`,
`tests/test_kernel.py`, `tests/test_elaborate.py` (only to remove two xfail marks, below), and
write your report; a failure from another file is someone else's, report it, do not fix it.

`src/luthier/lib/term.lth` gained the law `IotaConstructors` (`git show 66d5cae`): a constructor is
known from the program's `Data` definitions; two distinct constructors of one data do not match, so
a `match` skips the arm; a name the program declares or defines as an act stays a hole or unfolds
by `Delta`. Make `kernel.py`'s `step` follow it, transcribe the law in `tests/test_kernel.py`, and
remove the two strict xfail marks in `tests/test_elaborate.py`'s `test_eval` (factorial must print
`24`, data `2`).

Check: `python3 -m pytest tests/test_kernel.py tests/test_elaborate.py -q`, then
`python3 -m pytest tests/ -q`; `PYTHONPATH=src python3 -m luthier.cli eval tests/eval/factorial.lut
answer` prints `24`. Do not commit. Report in a few lines to `record/IA/kernel-2026-10-13/codex-6.md`.
