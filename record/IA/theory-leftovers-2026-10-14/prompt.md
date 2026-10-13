# The checker's 18 leftovers on the theory files: brief for a Claude agent

Written 2026-10-14 by the coordinating session (luthier-1b). luthier-03, the theories' session,
is paused until Luciano wakes; by his word the night continues with agents.

## The prompt

Read `CLAUDE.md` first, then `record/IA/check-2026-10-13/opus-3b.md`, section "Part 2", "Left, by
cause (18 failures)": six groups, each saying whose it is. Then `docs/spec/04-static-semantics.md`
(4.R2, 4.R3, 4.R9) and `src/luthier/lib/program.lth` (the predicates named: `fieldsRead`,
`nameSuffix`, `lawNames`, `armsNames`, `predicateUntouched`, `base`). Other agents work on
kernel.py, cli.py, run.py, host.py, arrays.py, tables.py and their tests: touch none of them. You
may change `src/luthier/lib/*.lth` and `*.lut` only, one commit per file (`git add` its path;
never `-A` or `.`; no `git stash` or `git checkout`), messages naming the rule and the group,
ending with "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".

Resolve each group by the smallest change that follows the spec, in the file the report names:
- group 1 (chained projection): program.lth's `fieldsRead` reads the field after the first `.`
  of a dotted name rooted at the model's binder, not the last; state it so.
- group 2 (a `data` no claimed law mentions): for each case decide by L2.7 (every constructor has
  a law of its role): a model's internal step results (`HeadStep`, `PatternStep`, ...) become
  aliases of sums as 4.R3 says; a theory's `data` whose constructors only a helper or a pattern
  reaches gets the role law stated on the law's body (or the helper inlined) if that is what the
  spec means; if the spec's reading would rather count helpers, say so and do not change
  program.lth without a reason you cite.
- group 3 (`Concrete` where `U` is expected): read kernel_laws.lth's `Concrete` and spec 3; if
  the spec has a sub-universe, state the refinement; if not, mark `[proposed]` the reading that
  one commit undoes and say so.
- group 4: `PWild` into program.lth's import; `one`, `two` of kernel_models.lut: name the sum in
  kernel_laws.lth and import it, unless program.lth should say an imported theory's sum labels
  come with it (then say which and why).
- group 5 (unused lambda parameter): program.lth's 4.R3 lambda case restricted to predicates, as
  the spec reads, or the parameter read; choose by the spec, cite it.
- group 6 (`Initial`'s vacuous law): leave it, note why in the report.
Also the files added after e2590af and not checked (algebra.lth, arrays.lth, arrays_model.lut,
core.lut, numbers_model.lut, tables.lth, tables_model.lut): run `PYTHONPATH=src python3 -m
luthier.cli check FILE` on each (minutes each; background them) and list what it refuses, by
cause, saying whose it is (the slice report, `record/IA/slice-theories-2026-10-14/report.md`,
already names some as the checker's: 4.R4 on `primitive`, 4.R13 on `operator` targets, 4.R3
through helpers, 4.R9 on `Nat` where `Int`). Do not fix check.py. Every file you change must
still parse. Report to `record/IA/theory-leftovers-2026-10-14/report.md` (commit it): per group
what you changed and what check.py must now mirror, and the list for the new files.
