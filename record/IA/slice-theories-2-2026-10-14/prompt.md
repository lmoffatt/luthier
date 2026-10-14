# The fit's theories: probability, belief, optimization over the new arrays, brief for a Fable agent

Written 2026-10-14 by the coordinating session (luthier-3e). Inventory §6 item 7 and §2 rows 21,
22, 24 (`record/IA/sonolocalizacion-inventory-2026-10-13/inventory.md`); the function-valued
crossings decided by D-2026-10-14-a (`record/decisions.md`, end; answers-2-2026-10-14.md item 2).
The second stage of the slice, `experiment_zero.lut`, needs these before its port.

## The prompt

Read `CLAUDE.md` first, then `docs/principles.md` (L2, L9, L10, L11, P11), the inventory rows
named, then the slice's first theories as the pattern to follow: `src/luthier/lib/arrays.lth` with
`arrays_model.lut`, `numbers.lth` with `numbers_model.lut`, and their report
(`record/IA/slice-theories-2026-10-14/report.md`). The sources to translate are v0.1's libraries at
the tag `v0.1-final` here (`git show v0.1-final:src/luthier/lib/probability.lut`, `belief.lut`,
`optimization.lut`, and their `*_python.lut`; if the paths differ, `git ls-tree -r v0.1-final
--name-only | grep lut`), and, read only, how sonolocalización uses them:
`/home/lmoffatt/Projects/sonolocalizacion/prototipo-cero/luthier/experiment_zero.lut` (lines
70-130, 149-170), `positions.lut`, `distances.lut`, `src/lm.py` (the host's Levenberg-Marquardt:
what it reads from the objective record and what it returns). Change nothing there. Spec: 7.R2
(libraries over `VecOf n`, not `(Theta : U)`), 11.S18 (tolerances as measured costs), 3.S23 as it
stands (the callback crossing), 6.S5 and 7.S17 (statistical laws declare their level).

Write, in the syntax of chapter 2 as the parser takes it (`PYTHONPATH=src python3 -m luthier.cli
parse FILE` on each), citing the spec item above each law:
1. `src/luthier/lib/probability.lth` and `probability_model.lut`: `MeanModel`, `ScaledModel`,
   `Likelihood`, `gaussian`, `profiled` (row 21), `normalCdf` by `erf`, `kolmogorovDistance`,
   `kolmogorovTail`, `valueSums` (row 24), over `VecOf n` and `Mat Float64` of arrays.lth, their
   laws (what a likelihood is, the Gaussian's density and its score and information as the
   derivatives arrays.lth can state, the Kolmogorov distance's bounds), the numpy or math leaves
   as externs with the laws their model must meet (as arrays_model.lut does).
2. `src/luthier/lib/belief.lth` and `belief_model.lut`: `GaussianBelief`, `laplaceMode`,
   `laplaceAt`, `Maximizer`, `MaxResult` (row 22): `Maximizer` takes the objective, its score and
   its information as functions over `VecOf n` and gives `MaxResult n = { x : VecOf n, converged
   : Bool }`; its model is the host's `lm.maximize` reached through the callback crossing of
   D-2026-10-14-a (3.S23): state the laws a maximizer must meet (stationarity within a tolerance
   at a converged `x`, the objective not smaller than at the start) so that the host's can be
   validated at its first action (10.S8 to 10.S10), with the tolerance a parameter (P11).
3. `src/luthier/lib/optimization.lth` and `optimization_model.lut`: `Objective` (a record whose
   fields are functions, crossing as D-a says), `LMState`, `Step`, the laws of a Levenberg-Marquardt
   step (the damping, the decrease), `pinvSym` and `trace` as leaves if arrays.lth lacks them
   (then add them to arrays.lth and its model instead, one commit each, saying so).
Each file must parse; run `luthier check FILE` on each and report what it refuses (the checker's
or the file's). Do not write Python. Where the spec or v0.1 is silent, choose the reading one
commit undoes, mark it `[proposed]` with a comment, list it in the report. Commit each theory
file as it is done, alone (`git add` its path; never `-A` or `.`; no `git stash` or `git
checkout`), messages naming the spec items, ending with "Co-Authored-By: Claude Fable 5.1
<noreply@anthropic.com>". Report to `record/IA/slice-theories-2-2026-10-14/report.md` (commit
it): what you wrote, every `[proposed]`, and per extern what the bridge and `lm.py`'s successor
in this repository must do (P7: the host code of the fit lives here, not in sonolocalización).
