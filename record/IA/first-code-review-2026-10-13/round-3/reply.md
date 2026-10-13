# Reply to round 3

2026-10-13, at a858291, by Claude Opus 5.5, on the four replies in this folder (`deepseek.md`,
`gpt.md`, `kimi.md`, `claude.md`, unedited). Round 3 found only local defects, all the model's to
fix, so there is no round 4: the parser and the certification of `grammar.lth` against it test
what reading would. Luciano's answers this round: D-2026-10-13-q (string escapes, `_` as a pattern
atom and the layout readings of 2.S4 decided) and D-2026-10-13-r (who writes and reviews the next
theories). The specification changed first (d140c01), then the files (a858291).

## Fixed

- The dangling `else` in `wf` (GPT, Claude; Kimi in part): `if c then (if d then y) else b` writes
  the tree `wf` rejected, since parentheses are not in the tree. `endsInOpenIf` is gone; the
  nearest-`if` rule is the parser's on texts (2.S11, `DanglingElse`), and `PrintParenthesizes`
  asks the printer to write the parentheses back. Kimi's narrower fix (not looking into the
  `else` branch) would have kept rejecting `if c then (if d then y else if e then z) else b`.
- An open form before `&` (Claude): `U -> (a : A) * b & C` and `A -> if c then x & y` had two
  trees. A chain of `->` is now closed (`arrowTerm`, which `&` may follow) or open (`arrowOpen`,
  ending in an open form, which nothing follows); 2.S8 says an open form closes its chain and
  nothing follows it; `OpenFormEndsItsTerm` pins it. A count of derivations over the transcribed
  grammar gives one tree for each of these texts now, two at draft 3.
- Vacuous samples (Claude): `RoundTrip` quantifies over `WrittenProgram d g`, a subtype drawn with
  names from a census; `LiteralsAreNotNames` runs over every literal of `luthierSyntax`, not over
  random strings. 7.S12 already kept such a law from passing vacuously (it would not have run).
- Reserved words (GPT, Claude): every literal lexes as one token of kind `"literal"` of its own
  text, which settles what `literalLexes` left free (a word was keyword or symbol at the model's
  choice); `OtherWordsAreNames` says the retired keywords and the names of core that act like
  keywords lex as names, the half of 2.S21 ("everything else is a core or library name") that no
  law stated.
- The uniqueness argument (GPT, Claude): step one descends a `seq` only to its first element that
  is not nullable; step two names the split whose first part is the whole list.
- Cases with no law (Claude, Kimi): clauses of several patterns, `\ (a b : A)`, `{ _ : T | p }`,
  string escapes in the token and in the tree, a lexing error with its line.
- `\ (y) { y }` (DeepSeek, Kimi): not parsing is the grammar's rule, a parenthesized parameter is a
  typed name or a tuple of two or more patterns; 2.S9 now says so.
- 2.S9's stale "two or more names" (GPT, Claude): rewritten; a single labeled field without a law
  is a record type.
- `reply.md` of round 2 used old names (`wellFormed`, `WrittenProgram`) for `wf` and `wfProgram`
  (Kimi); `WrittenProgram` now exists, as the subtype above.

## Not taken

- `floatLit` of `+∞` (Claude): every `Float64` is finite (11.R1), so `NonNegativeFloat` holds none.
- `precedenceLevels` written by hand (GPT): it names the nonterminals of the levels, which the
  grammar does not mark; the operators are derived from them.
- The lexer and layout characterized by cases, not by a grammar (GPT): the lexer as an `Ebnf` over
  characters is step 1.1.d of the plan, before the parser is certified.
- `x := --1` reads as a comment (Kimi): a consequence of `--` comments, left as is.
