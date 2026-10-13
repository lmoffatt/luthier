# kernel.py, bite 11: substitution does not capture a record's field, brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). On check bite 5's report
(`record/IA/check-2026-10-13/report-5.md`, cause (c)): `kernel.substitute` takes a record's field
labels as free names, so applying `identity (n : Nat) : Mat Float64` to `k`, with `Mat` the
record `{ m : Nat, n : Nat, f : Fin m -> Fin n -> Float64 }`, rewrote the field `n`.

## The prompt

Read `CLAUDE.md` first, then that report section, `src/luthier/lib/term.lth` §2 (substitution,
3.S31: which names a record's fields bind, `Record` and `RecordValue` in term.lth's `Term`, and
the law of substitution under binders) and `src/luthier/kernel.py` (`substitute`, `free_names`,
`alpha_equal`). Other agents edit `tester.py`, `cli.py` and their tests meanwhile: change only
`src/luthier/kernel.py` and `tests/test_kernel.py`.

Make `substitute` and `free_names` treat a dependent record type's field labels as binders of
the later fields (and a record value's labels as labels, never names), as term.lth states it; if
term.lth is silent on records, state the reading in a comment marked [proposed] and cite 3.S31.
Tests: the `identity` case above (the field `n` untouched, the parameter substituted in `Fin m
-> Fin n -> Float64` only where `n` is the parameter), a record whose later field reads an
earlier one, `free_names` on both. `check.py`'s `unclash` becomes unnecessary: leave it (the
checker's agent removes it in its next bite) but say so.

Check: `PYTHONPATH=src python3 -m pytest tests/test_kernel.py tests/test_run.py tests/test_check.py
-q`, then `PYTHONPATH=src python3 -m pytest tests -q`. Do not commit. Report in your final message.
