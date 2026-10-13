# The lexer as a grammar over characters: brief for a Claude session

Written 2026-10-13 at the commit that holds this file, by Claude Fable 5.1 (the coordinating
session), for a Claude Fable 5.1 subagent it launches. Step 1.1.d of
`record/plan/luthier-from-zero/plan-from-zero-2026-10-13-execution.md`.

## The brief

Read `CLAUDE.md` first: its working rules bind you. Then `docs/principles.md` (Terms, L2, L14),
`docs/spec/02-grammar.md` §1 (2.S1 to 2.S4, 2.S21), `src/luthier/lib/ebnf.lth` whole, and
`src/luthier/lib/grammar.lth` whole, with its lexical laws (`LiteralsAreNotNames`,
`OtherWordsAreNames`, `KindsAreTheGrammars`, `NameTokens`, `NumberTokens`, `StringTokens`,
`CommentDropped`, `ArrowIsOneToken`, `LexErrorsHaveLines`). Other agents work in this repository
at the same time (another Claude session on `src/luthier/lib/world.lth` and other theories; Codex
on `src/luthier/check.py`, `tests/`, `tools/vscode-luthier/`): you may change only
`src/luthier/lib/grammar.lth` and, if a sentence of 2.S1 must change, `docs/spec/02-grammar.md`
§1; nothing else. Commit your own work with explicit paths (`git add <file>`; never `-A` or `.`),
small commits, the message naming the spec items; the coordinator reads them.

The goal: today `lex` of the theory `Grammar` is pinned only by case laws (a few texts), so a lexer
that reserves an extra word or reads an unusual number differently can still pass. State the
lexicon as data, as `luthierSyntax` states the syntax (L14: what can be written in Luthier is
written in Luthier): a value `luthierLexicon : WellFormedEbnf` over characters, whose token views
are single characters (`kind` a character class the lexer can decide: `"letter"`, `"digit"`,
`"space"`, `"newline"`, `"quote"`, `"other"`, or the character itself as a literal where 2.S1 names
it), with one nonterminal per token kind of 2.S1 (`name` with its dotted form, `number`, `string`
with the escapes of D-2026-10-13-q, `comment`), plus the literals of `luthierSyntax` (reuse
`litsOf luthierSyntax`: a symbolic literal is a sequence of its characters, by longest match), and
a law `LexesWhatDerives` saying that `g.lex` produces exactly the token list that the lexicon
derives, maximal munch and the classification of a word as `"literal"` when it is in `litsOf
luthierSyntax` and `"name"` otherwise. Then the case laws stay as examples, and `lex` is
characterized by the grammar. Keep the laws on the subtype they mean, not on an implication a
random string rarely meets (7.S12, L9.6). If `ebnf.lth` lacks something the lexicon needs (a
character class as a category is already `cat`), say so in your report rather than changing it.
Where the specification is silent (for instance on which characters a `name` may contain beyond
2.S1's `letter`), take the reading that keeps the current three files lexing as they do and mark
it `[proposed]` in a comment with the spec item it would amend.

Checks: `PYTHONPATH=src python3 -m luthier.cli parse src/luthier/lib/grammar.lth` passes;
`python3 scripts/check_spec.py`, `python3 scripts/render_grammar.py --check` (regenerate with
`--write` if you changed `luthierSyntax`, which you should not need) and
`python3 -m pytest tests/test_ebnf.py tests/test_render_grammar.py -q` pass. Do not touch
`parse.py`: the coordinator briefs Codex to make the lexer follow the lexicon.

Report, as your final message: what you added (the nonterminals and the laws), every reading you
took where the spec was silent, what `ebnf.lth` lacked if anything, and the commits.
