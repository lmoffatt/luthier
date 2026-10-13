# term_model.lut, the models of term.lth: brief for Codex

Written 2026-10-13 by Claude Opus 5.5 for Luciano, at the commit that holds this file (§7 of
`src/luthier/lib/term.lth`; step 2.2 of `record/plan-from-zero-2026-10-13-execution.md`; Z9).

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. `src/luthier/lib/term.lth` states the
kernel term as data and the theories `Alpha`, `Substitution`, `CanonicalForm`, `Reduction` and
`Evaluation`, with their laws; `src/luthier/lib/kernel_models.lut` and `ebnf_model.lut` show how a
model file is written. Write `src/luthier/lib/term_model.lut`, in Luthier, with one model of each
of the first four theories:

- `alpha : Alpha`, alpha-equivalence by walking both terms with a list of pairs of bound names;
- `substitute : Substitution alpha`, capture-avoiding: under a binder whose name is free in the
  substituted term, rename the binder to a fresh name (say, the name with `'` appended until it is
  free in both) before going in;
- `canonical : CanonicalForm alpha`, bound variables renamed `x0`, `x1`, ... in order of binding,
  and `unqualify` dropping everything up to the last `.` of a name (write the string functions it
  needs from core's `String` operations, or declare them as holes with a comment if spec 11 names
  none);
- `reduce : Reduction alpha substitute`, the interpreter of 3.S33: weak head reduction to a value
  under fuel, `nothing` when the fuel runs out, implementing beta, delta (a defined name in head
  position unfolds; a declared one is a hole and stays), iota (the first arm whose pattern
  matches), prim (`+`, `*`, `==`, `<` on integer constants, giving `Var "true"` or `Var "false"`
  for comparisons), an extern staying a value (spec 10 calls the host; no call here).

Each model must satisfy every law of its theory in term.lth; read each law and check your code
against it by hand, since no checker can run it yet. Keep helpers in the same file. Check with
`PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/term_model.lut` and run
`python3 -m pytest tests/ -q`. Do not change term.lth or any other file except your report; if a
law seems wrong or unsatisfiable, say so. Do not commit. Report in a few lines to
`record/IA/term-2026-10-13/codex.md`: what you wrote, any law you could not meet, any choice the
laws left open.
