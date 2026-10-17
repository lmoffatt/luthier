# Brief: the evidence of a law kept per region (3j, the theory)

You write theory in Luthier. Read `CLAUDE.md` first. Then read, in this order and no more unless a
file you edit needs it:
- `record/decisions.md` at D-2026-10-16-i and D-2026-10-16-j (the decision you implement), and
  D-2026-10-15-a (L9.14: every law carries a model it refutes), D-2026-10-15-b (the sequential
  test), D-2026-10-16-g (stretches pooled across seeds);
- `record/generators-2026-10-06.md` sections 3, 4, 5 and 10 (special values, atoms, edge cases);
- `docs/spec/05-*.md` 5.S8 and `docs/spec/07-tests.md` 7.S10, 7.S14;
- `src/luthier/lib/certification.lth` (grades, `pooledCases`, `Certifying`), `test.lth`,
  `laws.lth`, `generators.lth`;
- `src/luthier/lib/plan.lth` at `KeyReadsOnlyTheCone` and `KeyReadsTheType` (two laws no model can
  fail: `record/IA/code-follows-2026-10-16/report-controls.md`).

The decision, in short: a law's evidence is kept per binding and per region, each with its n and
its bound, not summarized; the regions that enter a grade come only from three finite sources:
(1) the type, whose theory declares its degenerate cases once (zero, rank deficient, 1x1 and 0x0
for a matrix; empty and singleton for a list); (2) the law, each cutoff parameter giving its two
sides and each premise its boundary; (3) the code, each branch of the cone (branch coverage). An
author's label is informative and enters no grade. How grades combine across regions and bindings
is the demand's choice, the weakest by default (5.S8). The generator gives the regions mass
(special values, atoms) or they are listed.

Write, in Luthier:
1. In the theory where types declare things about themselves (find where a type's theory can carry
   a list; if none fits, propose it in `generators.lth`): a way for a type's theory to declare its
   degenerate cases, and the declarations for `Mat`/`Symmetric` (arrays.lth) and `List`
   (kernel_laws.lth or core) as examples. Do not touch other theories.
2. In `certification.lth`: a region (its source: Type, Law, Code; its name); evidence per (binding,
   region) with n and bound; the grade of a law as the demand's combination over regions, the
   weakest by default; the laws that tie these (a region with no evidence leaves the law below
   `cases`; an author's label changes no grade), each with a control in a `*_controls.test.lut`
   (L9.14). Keep `Certifying`'s existing fields; add a theory beside it if needed, as `Recording`
   and `Pooling` are.
3. The law-derived regions: a function from a law's cutoff parameters and premises to its regions
   (stated, with a law on one example such as `PinvProjects`'s tolerance and rank floor).
4. Restate plan.lth's `KeyReadsOnlyTheCone` and `KeyReadsTheType` so that the planner enters them
   and a broken planner can fail them, with their controls; or, if they cannot be, say why and
   remove them from the theory's conjunction with a comment.
5. Write, for the code that follows, a short list in your report of what tester.py and
   generators.py must do (special values, classify/cover over regions, branch coverage), each item
   naming the law it implements.

Accepted when: `luthier check` is clean on every file you touched; `luthier certify` on the
`.test.lut` files you added or touched reports every law graded and controlled (or the finding);
`python -m pytest -q` passes in full (798 passed, 6 skipped, 9 xfailed before, plus yours);
`python3 scripts/check_spec.py` prints its known finding (03-kernel.md:190). You are the only agent
writing theory now; another may touch tables.cert.json and the archive. Two-line commits ending with
"Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>", staged by path; retry on
.git/index.lock. Report: `record/IA/regions-2026-10-17/report-theory.md`, by shell heredoc,
committed: what you wrote, the checks' output, decisions taken on your own, at most one question.
