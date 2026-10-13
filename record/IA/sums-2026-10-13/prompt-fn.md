# Lambdas with fn: the parser and the programs, brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 (the coordinating
session), launched by it with `codex exec`.

## The prompt

Read `CLAUDE.md` first. Other agents work here at the same time: change only the files listed;
a failure from another file is someone else's, report it, do not fix it.

Luciano decided (D-2026-10-13-y in `record/decisions.md`) that a lambda is written with the keyword
`fn` in place of `\`: `fn e (j : J) { e + j }`; nothing else about lambdas changes, and there is no
`return`. `src/luthier/lib/grammar.lth` already says so (5d81039: `lit "fn"` in `atom`, the
`LambdaTree` texts); `fn` is a keyword because the grammar takes it as a literal.

Files you may change: `src/luthier/parse.py` (the lambda production; the printer writes `fn`; the
lexer needs nothing if it derives its literals from the grammar, check), `tests/test_parse.py`
(`LambdaTree` transcribed anew; any other text with `\`), `tests/test_roundtrip_trees.py` if it
spells lambdas, and `tests/spec/*.lut` with `tests/spec/README.md` (each `\` lambda becomes `fn`).

Check: `python3 -m pytest tests/test_parse.py tests/test_roundtrip_trees.py tests/test_ebnf.py
tests/test_spec.py tests/test_render_grammar.py -q`; `luthier parse src/luthier/lib/grammar.lth
src/luthier/lib/ebnf.lth src/luthier/lib/ebnf_model.lut tests/spec/*.lut` (the one syntax reject
excepted). The other theory files in `src/luthier/lib/` are being rewritten to `fn` by their owner;
do not touch them. Do not commit. Report in a few lines to `record/IA/sums-2026-10-13/codex-fn.md`.
