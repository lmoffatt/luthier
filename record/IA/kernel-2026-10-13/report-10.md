# kernel.py, bite 10: /= on every concrete type, constructors of parameterized data, report

2026-10-14, Claude Sonnet 5.5 (an agent of luthier-1b), on prompt-10.md; saved by the coordinator
from the agent's final message. Not committed by the agent.

validate_graph.lut runs to the end (run, default fuel, from the repository root) and prints
`valid: 10 nodes, 22 measurements, 21 distinct pairs; directions the distances do not see: 14 (of
which 10 are the heights and 3 the rigid motions of the plane)`. Wall time: 317 s in the
background run, 355 s through the slow test.

- kernel.py: `/=` on two StringConst steps to true/false by their difference; `/=` on pairs,
  records, injections and constructors goes through the same step as `==` (same demand of parts,
  same stuck cases) and answers the negation of `==`'s result. The constructor table reads
  constructors through a definition's Lam binders, so core's Maybe and List count for ==, /= and
  match.
- cli.py: `run`'s --fuel defaults to 10,000,000, still a parameter, help text marked [proposed];
  `eval` keeps 10,000.
- tests/test_kernel.py: test_neq_on_strings_and_structures, test_parameterized_data_constructors
  (just 1 == just 1, [1, 2] == [1, 2], nothing /= just 1, a match on just, the stuck cases, a
  constructor with no data in the program).
- tests/test_run.py: test_equality_on_strings_and_parameterized_data; test_validate_graph_slow
  runs validate_graph.lut and checks the line, skipped unless LUTHIER_SLOW=1 (no slow marker).
- term.lth §5 (luthier-03 paused; comment-marked [proposed]): beside PrimString, citing 4.R8, the
  `gives` of `/=` on two strings; beside PrimStructural three `gives` for `/=` on pairs, records
  and injections, each the negation of `==`'s. `luthier check` not run on term.lth after.

Choices of the agent: `/=` shares the `==` branch and negates; stuck where `==` is stuck; binder
unwrapping counts only Lam binders, arity the Pis of the constructor's type; the slow test's
guard; the help text names no step count.
