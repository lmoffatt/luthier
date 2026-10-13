# The theories the sonolocalización slice needs first: brief for a Fable agent

Written 2026-10-14 at the commit that holds this file, by the coordinating session (luthier-1b).
Luciano (2026-10-13, night): sonolocalización starts now and drives Luthier's development; the
plan is `record/plan/sonolocalizacion/plan-sonolocalizacion-2026-10-13-execution.md` (step 2, the
slice), and the night's order is `record/plan/night-2026-10-13.md`.

## The prompt

Read `CLAUDE.md` first, then `docs/principles.md`, then the inventory
`record/IA/sonolocalizacion-inventory-2026-10-13/inventory.md` (whole: the rows marked (v) are
what the first stage, `validate_graph.lut`, needs; §6 orders the blockers). Then the
specification it cites: `docs/spec/11-*.md` (11.R1 to 11.R3, 11.S4, 11.S8, 11.S9, 11.S18),
`docs/spec/03-kernel.md` (3.S17 Prim, 3.S22 to 3.S28, the bridge), `12-files-and-tools.md` (12.S9,
12.S22, 12.S23), and the pattern of the theories already written: `src/luthier/lib/kernel_laws.lth`
with `kernel_models.lut`, `term.lth` §5 (`Prim`), `world.lth` with `world_model.lut`,
`library.lth` (the loader's laws: where `primitive` and `axiom` are allowed).

Write the theories for items 1, 2 and 4 of the inventory's §6, in the syntax of chapter 2 as the
parser takes it today, each law citing its spec item above it (`-- spec 11.S9`):
1. Numbers and strings in the core: `Int`, `Real`, `Float64`, `String`, `Nat`, `Fin n` as 11.R1
   states them, the core's data `Bool`, `Maybe`, `List`, and the operations the slice needs
   (Float64 `+ - * /` and comparisons, Int `/` and `mod`, `toFloat64`, String `+`, `sqrt`, `log`,
   `exp`, `erf`), each with the laws that say what it is (11.S4: Float64's operations are the
   machine's rounded ones; state what can be stated: the IEEE operations as primitives, with
   laws on exact cases and a tolerance only where 11.S18 says so). Where the spec names a file
   (`core.lut`, `lib/algebra.lut`, `lib/rational.lut`), follow its name, reading Z8 (theories
   `.lth`, models `.lut`) and 12.S22 for how a theory and its model split; say what you chose.
   If term.lth's `Prim` must gain the new operations for the kernel to compute them, add the
   `gives` to term.lth §5 (luthier-03 owns it and is paused; you may append to `Prim` and its
   neighbours only, and say so in your report).
2. Arrays: `Vec`, `Mat` as 11.S9 states them, `VecOf`, `MatOf`, `Dim` if the slice's files use
   them (inventory row 8), and the operations of row 12 that `validate_graph.lut` needs
   (`transpose`, the matrix product, `retainedRank` with its rank floor as a parameter, P11 every
   criterion is a parameter), the numpy ones as externs with the laws their model must meet.
3. Tables: a theory of `Table` with its accessors and codec laws (inventory row 5), its model
   over the host code that survives in `src/luthier/tables.py` (read it) through externs.
Each file must pass `PYTHONPATH=src python3 -m luthier.cli parse FILE`, and `luthier check FILE`
as far as the checker goes today (report what it refuses and whether it is the checker's or the
file's). Do not write the specimens (kernel.py, run.py's bridge): list in your report, per
operation, what the kernel and the bridge must do for it, so the coordinator can brief them.

You may create files under `src/luthier/lib/` and append to term.lth §5 as said; touch nothing
else. Commit each theory file as it is done, alone (`git add` its path; never `-A` or `.`),
messages naming the spec items, ending with "Co-Authored-By: Claude Fable 5.1
<noreply@anthropic.com>". Where the spec is silent or contradicts itself, choose the reading that
one commit undoes, mark it `[proposed]` in a comment, and list it in the report. Report to
`record/IA/slice-theories-2026-10-14/report.md` (commit it too): what you wrote, every choice,
what the specimens need.
