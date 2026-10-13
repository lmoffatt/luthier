# Sums braced with ||: the parser and the programs, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session) for Luciano, who gives it to Codex in this repository. Disjoint from the kernel task
(`term.py`, `kernel.py`, `tests/test_kernel.py`), so it may run beside it.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: touch only the files listed
below; a failure from another file is someone else's, report it, do not fix it.

Luciano decided (D-2026-10-13-w in `record/decisions.md`) that a labeled sum is braced, with `||`
between alternatives: `{ circle : Float64 || square : Float64 }`, two alternatives or more; `,` and
`||` never mix at one level (a mixture nests); inside braces a line beginning with `||` continues
the item above. `< >` for sums and the form `(x : A) + (y : B)` are retired, so `<` and `>` are
comparisons only. `src/luthier/lib/grammar.lth` already says so (4c105e3: the sum alternative of
`atom`, `SumTree`, the `||` case in `ContinuationLines`, `ColumnZeroStartsAct`; `sumNamed`,
`argAtom`, `argTerm`, the `sumAlt` chain and `SumAsArgument` gone). `git show 4c105e3`.

Files you may change: `src/luthier/surface.py` (drop `SumNamed`), `src/luthier/parse.py` (lexer:
`||` by longest match; layout: no `< >` bracket, the `||` continuation; parser: the new
productions, one function per nonterminal as now; printer: sums as `{ a : A || b : B }`),
`tests/test_parse.py` (`test_sum_tree` and the changed laws transcribed; `SumAsArgument` and
`sumNamed` cases removed), `tests/test_roundtrip_trees.py` (generator: no `SumNamed`, `Sum` with two
alternatives or more), `tests/test_ebnf.py` (texts with `< >`), and `tests/spec/*.lut` with
`tests/spec/README.md`: rewrite each `< ... >` sum into braces; a one-alternative sum
(`Z7 = < z7 : Fin 7 >`) becomes a one-field record `{ z7 : Fin 7 }`, and its uses change with it
(an injection `z7 k` becomes `{ z7 := k }`, a match on the label a projection), keeping what the
program tests; say so in its header.

Check: `python3 -m pytest tests/test_parse.py tests/test_roundtrip_trees.py tests/test_ebnf.py
tests/test_spec.py tests/test_render_grammar.py -q`; `luthier parse src/luthier/lib/grammar.lth
src/luthier/lib/ebnf.lth src/luthier/lib/ebnf_model.lut tests/spec/*.lut` (the one syntax reject
excepted). Do not commit. Report in a few lines to `record/IA/sums-2026-10-13/codex.md`.
