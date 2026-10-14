# run.py bite 10: a definition and a constructor of one name kept apart, report

2026-10-14, Claude Opus 5.5, an agent of luthier-3e, on prompt-10.md; saved by the coordinator.
Files: `src/luthier/run.py`, `src/luthier/check.py`, `tests/test_run.py`, `tests/test_check.py`,
new `tests/run/scope/label_and_definition.lut`. Checks: test_run, test_check, test_lm 161
passed, 1 skipped; the suite 567 passed. `luthier check` over every tracked `.lut` and `.lth`
outside `record/`: the only difference from HEAD is the removed 4.R9 on `sigmaKnown`.

The cause: tables.lth's `int` is a label of the sum `Cell`, not a data constructor; the loader
kept labels global under their written names, and program.lth's `int : Term`, the only
definition of that name, kept the plain name, so the label's applications and patterns reduced
to it. check.py's `load_imports` brought in every transitive definition, so program.lth's
`known` did the same to `SigmaTreatment`'s label.

run.py (`Loaded`, v10): each `_File` records the labels of the sums it writes; a definition that
is not a constructor never keeps a plain name that is a label of any loaded file, a data
constructor of any file, or a built-in constructor (always `name@file`); labels keep their
written names (the elaborator and the bridge read them by name); `see` resolves the file's own
definitions, then its own labels, then what its imports list, then core; `constructor` resolves
a pattern's head. check.py: `load_imports` through `_brought`; an imported definition or
declaration is left out when its name is a constructor or label of the file or of anything
imported, kept only if the file lists that name from that same file and has no constructor or
label of the name itself; the docstring corrected.

experiment_zero.lut: `luthier check` refuses nothing (48 of 48 acts typed); the run with the
brief's `--set` values and `lmMaxIter=2` took 274 s and printed the three tables and the summary
line identical to the port's patched probe (sigma 5.88 m, NOT CONVERGED after 2 iterations, as
asked). The 4.R9 on `pairI`/`pairJ` in distances.lut is unchanged.

Decisions of the agent: the colliding definition renamed, not the labels; a definition renamed
when its name is a label or constructor anywhere loaded; check.py leaves out a colliding
imported definition rather than renaming it (moving check onto run's `Loaded` would be the full
unification); a definition the file explicitly imports from its own file kept unless the file
has such a constructor or label. Not done: whether the positions_model.lut split stays.
