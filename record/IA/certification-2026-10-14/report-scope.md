# Two scope findings fixed: report

2026-10-15, Claude Opus 5.5, an agent of luthier-3e, on prompt-scope.md; saved by the
coordinator. Files: `src/luthier/check.py`, `src/luthier/elaborate.py`, `src/luthier/run.py`,
`src/luthier/certify.py`, `tests/test_check.py`, `tests/test_certify.py`,
`tests/run/plot_two_tables.lut`. Checks: the three test files 190 passed; the suite 643 passed;
no store stale, no re-certification needed (every cone hash in the 20 stores unchanged; the
only cones that changed were over-reaching ones in experiment_zero.lut, session_a.lut and
scope/main.lut, each new cone a subset of the old).

Item 1, the checker: the capture fired only when the imported `kept` had a type different
from the binder's. Two places typed a match arm without its pattern variables in scope:
`Typing.applications` in check.py and `elaborate.infer`'s `Match` case (edited, the one file
outside the listed set; `h (match x { kept -> kept })` was refused even in one file). Arms
now bind their pattern names with unknown type. `load_imports` rewritten to resolve each
imported file's names in that file, as `Loaded` does: an unlisted imported definition whose
name the importer writes is typed `name@file`; `as` and re-exports become aliases; `Loaded.scoped`
and `rename` moved into a base class `FileScope` in run.py (a pure move) that check.py's
`_ImportScope` subclasses. Regression: `check` and `report` over all 194 files identical.

Item 2, the certifier: `Cones._part` stripped the `@file` tags before collecting references
and `Cones.names` expanded each plain reference to every `name@*` in the program (csv's code
mentions the label `text`, which pulled plot.lth's `text@plot` into csv's cone; `apart@plot`
pulled in the test's `apart`). References are collected by exact internal name now, tags
stripped only from the hashed code. Two tests: csv's cone and its four laws' cones equal with
and without `import "plot.lth" text`; LayerOrderInvariant's with and without a local `apart`.
plot_two_tables.lut uses plot.lth's `text` again.

Decisions of the agent: unlisted imported definitions renamed only when the importer writes
the name; pattern variables typed unknown; the `FileScope` move; the elaborator edit. Left
open: imported constructors and labels still global in the checker; two imported files
defining one unlisted name the importer never writes still collide; figures.lut's `keptRow`
rename stays.
