# Items 1, 2 and 4 of summary-BCD.md's top screen, brief for an Opus agent

Read `CLAUDE.md`, then `summary-BCD.md` in this folder (the top screen, and the sections behind
items 1, 2, 4 and the runners-up "Posterior lets info be negative", "Strategy has no role law").
Fix in the theories, each `[proposed]`, Boolean with cutoffs as parameters (D-2026-10-14-c):
1. `IsGradient` (probability.lth ~65) and the gradient laws of `Posterior` and `Objective`: test
   along a drawn direction, as `IsJacobian` does, so a zero score is not a model.
2. plan.lth `LinearizesOn`/`placedBefore` (~79-81): a schedule places every node after what it
   reads; add acyclicity of a `Dataflow` and the locality law the summary names; the file's own
   counterexample `["d","b","c","a"]` refused; `Strategy`'s role law.
3. optimization.lth `StepRule` (~146-150) determined (the `phi := pt - 1` and even-iteration
   counterexamples refuted); belief.lth `QuadraticConverges` (~127) over settings whose budget
   suffices for the family, and `MaximizerStationary` (~111) not vacuous for a maximizer that
   gives up everywhere (a law that it converges on the quadratic family within its budget);
   `Posterior`'s information non-negative or `negate` made total.
Change only those four theory files and their models, one commit per file by path ("Co-Authored-By:
Claude Opus 5.5 <noreply@anthropic.com>"); report with a shell heredoc to `report-fix-BCD.md`
here, committed alone. Accepted when: every changed file parses and `luthier check` is clean;
`PYTHONPATH=src python3 -m luthier.cli test tests/tester/probability_laws.lut --no-cert` and
`belief_laws.lut`, `optimization_laws.lut`, `fit_laws.lut` give no refuted line (paste them;
a refutation of the host's lm.py is a finding, report it); the fit still runs
(`experiment_zero.lut` on graph_noA2 with the usual `--set`, `--accept assumed` if the store
asks): paste its summary line.
