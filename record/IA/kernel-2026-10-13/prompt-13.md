# kernel.py, bite 13: == on the labels of a labeled sum, brief for a Sonnet agent

Written 2026-10-15 by the coordinating session (luthier-3e). On the last Sonnet's report: `c :
Maybe Cell := just (int 1); c == c` is stuck, because the kernel's `==` does not step on the
labels of a `||` sum (`int`, `real`, `text` of tables.lth's `Cell`), which are not constructors
of a `data`; tables.lth's `sameCell` works around it ([proposed]).

## The prompt

Read `CLAUDE.md` first, then `src/luthier/lib/term.lth` §5 `PrimStructural` (injections `Inj l
v` compared by label then value) and `NotEqualNegates`, `docs/spec/03-kernel.md` 3.S4 (a label
of a sum applied is an injection; a `Unit` alternative injected by its label alone), 3.S17,
`src/luthier/elaborate.py` at how `int 1` with `int` a label of `Cell` elaborates (an `Inj`, or
`App (Var "int") ...`?), `src/luthier/kernel.py` at `==` (bites 7 to 10: `_step`'s `==` branch,
the constructor table, `Inj`). Another Sonnet edits `tester.py`, `certify.py` and
`tests/tester/`: touch none. Change `src/luthier/kernel.py`, `src/luthier/elaborate.py` if the
cause is there, `tests/test_kernel.py`, `tests/test_elaborate.py`, one program under `tests/eval/`.

Make `==` and `/=` step on two values of a labeled sum as `PrimStructural` states for `Inj`:
same label and equal parts give true, different labels false; a label with no part (`Unit`)
compared by label alone; nested inside `Maybe` (`just (int 1) == just (int 1)` true, `just (int
1) == just (real 1.0)` false). Find whether the elaborator produces `Inj` for an applied label or
an application of a free name (then the kernel sees no injection): fix at the source and say
which. Tests in test_kernel and test_elaborate, an eval program with the three cases, and
`tests/tester/tables_laws.lut` still passing (`luthier test ... --no-cert`, a minute). Do not
touch tables.lth (its `sameCell` can go later).

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_elaborate.py tests/test_run.py
-q`, then the suite. Do not commit. Report in your final message.
