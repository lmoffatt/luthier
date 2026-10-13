# kernel.py, the evaluator: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session) for Luciano, who gives it to Codex in this repository. Step 2.5 of
`record/plan-from-zero-2026-10-13-execution.md` (D-2026-10-13-u: `kernel.py` brought forward).
`term.lth` §1 is stable (its owner, the session luthier-03, 2026-10-13); §2 to §6 may still
change after review. Two bites; this brief is bite 1. Bite 2, `luthier eval` on parsed files,
waits for `translation.lth` (step 2.4).

## The prompt

Read `CLAUDE.md` first. Other agents work in this repository at the same time: do not touch
`src/luthier/lib/`, `docs/`, `record/` (except your report), `tests/spec/`, or the parser files
(`parse.py`, `surface.py`, `ebnf.py`, `cli.py` and their tests). A test failure that comes from a
file you did not touch is someone else's: report it, do not fix it.

`src/luthier/lib/term.lth` is the theory of Luthier's kernel terms: §1 the data (`Constant`,
`Pattern`, `Term`, `Act`, `Program`), §2 names and alpha-equivalence (`Alpha`), §3 `Substitution`,
§4 `CanonicalForm`, §5 `Reduction` with fuel, §6 quote and eval. `src/luthier/lib/term_model.lut`
is a model of §2 to §5 written in Luthier; its report is `record/IA/term-2026-10-13/codex.md`.
Write the Python specimen of the same theories, a second model certified against the same laws
(L14.3 in `docs/principles.md`).

1. `src/luthier/term.py`: the data of §1 as frozen dataclasses, one per constructor, naming as in
   `src/luthier/surface.py` (a constructor `c` is the class `C`; `List A` a tuple, `Maybe A`
   `A | None`).
2. `src/luthier/kernel.py`: `alpha_equal(a, b)`, `free_names(t)`, `substitute(x, s, t)`,
   `canonical(t)`, `unqualify(name)`, `reduce(program, fuel, t) -> Term | None`, each following
   its theory's laws and, where the laws leave a choice, `term_model.lut`'s choice (its report
   lists them). Iterative where Python's recursion limit would bite on long reductions; fuel as
   the theory states it (each transition spends one unit).
3. `tests/test_kernel.py`: one test per law of §2 to §5, named after the law in snake case,
   evaluating the law on hand-written cases and on random terms from a seeded, size-bounded
   generator of `Term` (at size 0 only constructors with no recursive argument, otherwise the
   size less one split among the recursive arguments). Laws whose parameters need a `Program`
   draw small programs too. A law your code cannot meet: `xfail(strict=True)` with the reason, and
   in the report.

Check: `python3 -m pytest tests/test_kernel.py -q`, then `python3 -m pytest tests/ -q`. Do not
commit. Report in a few lines to `record/IA/kernel-2026-10-13/codex.md`: what you wrote, the test
counts, every law not met with a counterexample, and every place where `term.lth` and
`term_model.lut` disagree or where the theory did not decide.
