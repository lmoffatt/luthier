# The parser, finished in the repository: brief for Codex

Written 2026-10-13 at the commit that holds this file, by Claude Opus 5.5 for Luciano, who gives it
to Codex in this repository. ChatGPT wrote the parser (`chatgpt/`, installed at 0cc793f); since
then the grammar gained two rules, and one law cannot be tested in time. Two bites, in this order;
do the first, run the tests, then the second.

## The prompt

Read `CLAUDE.md` first: its working rules bind you too. The grammar of Luthier is the value
`luthierSyntax` in `src/luthier/lib/grammar.lth`, with the laws a parser must satisfy;
`src/luthier/ebnf.py` reads it and counts derivations; `src/luthier/parse.py` is the parser,
`tests/test_parse.py` its tests, one per law. ChatGPT's report on it is
`record/IA/parser-2026-10-13/chatgpt/report.md` (section "Report" at the end).

**Bite 1, `src/luthier/ebnf.py`: a recognizer fast enough for whole files.** `count_derivations`
is cubic in the tokens, so `tests/test_parse.py::test_parses_what_derives` does not finish (the act
defining `luthierSyntax` has 1842 tokens). Replace its body by an Earley parser over the grammar
as data (`opt`, `rep`, `seq`, `alt` expanded to fresh nonterminals, or handled as items), keeping
the signatures and documented behaviour of `count_derivations`, `derives` and `derives_program`.
Counting may stop at 2 (callers ask 0, 1, or more than 1); say so in the docstring. Keep
`tests/test_ebnf.py` passing, and add a test that `derives_program` on the laid-out tokens of each
of `src/luthier/lib/grammar.lth`, `ebnf.lth`, `ebnf_model.lut` returns true in under 10 seconds.

**Bite 2, `src/luthier/parse.py` and `tests/test_parse.py`: the two new rules.** Read the
comments above `luthierSyntax` and the productions `scrutinee` to `sArgAtom` and `sumAlt` to
`sumCmp`, the law `ScrutineeTree`, and the new cases in `SumAsArgument` and `PrintParenthesizes`;
they came in at feceb90 and 4bc59f4 (`git show` them). Make the parser follow them: a `match`'s
scrutinee carries no braces outside brackets, so the first `{` after it opens the arms (D-2026-10-13-s
in `record/decisions.md`); inside `< >` a comparison by `>` and an open form go in parentheses.
Make the layout identify brackets from the tokens before them as the new comment says (this
replaces ChatGPT's readings 4, 5, 6 and 8 of its report by the rule). The printer parenthesizes
accordingly. In the tests: `test_scrutinee_tree` and the new cases, transcribed from the laws;
`test_match_followed_by_block_is_unambiguous` becomes an ordinary test that the text has one
derivation and the tree of `ScrutineeTree`; the skip on the `luthierSyntax` act is removed.

Check: `python3 -m pytest tests/ -q` passes whole, `python3 scripts/check_spec.py` and
`python3 scripts/render_grammar.py --check` pass, and `luthier parse src/luthier/lib/*.lth
src/luthier/lib/*.lut` parses the three files. Do not change `grammar.lth`, `ebnf.lth`, the
specification or the record, except your report. If a law of `grammar.lth` seems wrong or the
parser cannot meet it, do not change the law: say so. Do not commit. Report in a few lines to
`record/IA/parser-2026-10-13/codex.md`: what changed, the test counts, the time of the whole-file
check, and anything in the grammar you believe is wrong.
