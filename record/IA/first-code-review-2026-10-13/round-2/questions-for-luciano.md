# The first code, round 2: what the reviewers leave to Luciano

2026-10-13, by Claude Opus 5.5, on the four replies of round 2 in this folder (DeepSeek's first
reply, without the files, is in git before its second). The rewrite held: all four confirm the
fixes of round 1 and the uniqueness of `derives` on `WellFormedEbnf`; Claude and Kimi checked every
case law against `luthierSyntax`. Six questions are yours; the rest is mine (at the end). Mark
under each: "ok", "no", or a comment.

## R1. `import` and `as` are keywords

All four agree: the import line binds names, which no function can do, and without `import`
reserved `import "x.lut" A` is also a datum applying a name. `as` is needed less (Claude: `lit "as"`
matches a name by its text), but reserving it keeps it from being an imported name.

Recommended: both keywords, eleven in all; 2.S21's "`import` gives a module value", stale since
12.S22, goes; and the class of "ordinary names that act as keywords in their position" (2.S2) goes
with it.

## R2. A definition has a body or clauses, never both

All four: 2.S5's `":=" body { clause }` does not derive a header followed only by clauses, which
its own prose describes. Kimi and Claude propose the same production.

Recommended: `definition ::= name { binder } [ ":" term ] ( ":=" body | clause { clause } )`; the
tree's `define` carries one or the other (a `Body` gains `clauses : List Clause -> Body`); 2.S12
gains the row "a definition by clauses is the `match` of its clauses on the tuple of its
parameters"; a tree law pins it.

## R3. Where the law that gives a `data` meaning is written

Your Q1: a `data`'s constructors mean what an observer bound to them by a law says. Claude found
that the files write the observers (`keywordText`) and their laws (`KeywordTextInjective`) but
nothing claims the laws: they are in no theory's conjunction, a `data` has no `:=` to carry them,
and 4.S14 rejects an unclaimed law. GPT adds that "told apart" is too strong: `eps` and `seq nil`
mean the same yet are two constructors.

Recommended: the law goes in the observer's type, with no new form. An observer is a function,
and a function with a law is a theory of one symbol (D-2026-10-12-aj): `keywordText : { f : Keyword
-> String | Injective f } := \ k { match k { ... } }`. The law is then claimed by the observer's
declaration, and certified as any. 4.R3 reads: every constructor of a `data` is given its meaning by
a lawful observer; injectivity is one such law where the observer is meant to tell constructors
apart, not a requirement (GPT's `eps` and `seq nil`).

## R4. An open form extends as far right as it can

Claude found texts with two trees, inherited from 2.S9: `(n : Nat) * Vec n` is either
`sigma n Nat (Vec n)` or the application `(sigma n Nat Vec) n`; likewise `(a : A) -> B c`,
`(a : A) -> B -> C`, `f if c then a else b + 1`, `\ x { ... } y`. GPT's dangling `else` is the same
family. One rule settles it, 2.S11 generalized.

Recommended: a form that ends in a term (a dependent arrow or product, `if`, `match`'s scrutinee
excepted) takes the longest term that follows; `(n : Nat) * Vec n` is `sigma n Nat (Vec n)`, and a
law per form pins it.

## R5. `and`, `or`, `mod`: names or operators

The rewrite lexes them as operators (kind "infix", constructors of `Op`), which removes the
ambiguity Claude found in round 1 (`f and` derived). Kimi: 2.S2 still calls them ordinary names
written infix, and now `and x y` as a prefix application, or `mod` as an ordinary function, does not
parse.

Recommended: operators, like `+`, given their meaning by core through the `operator` act, which
then binds `and`, `or`, `mod` besides `+ - * /`; 2.S2 drops "ordinary names".

## R6. Which states the grammar: chapter 2's EBNF or `luthierSyntax`

Claude: 2.S9's EBNF was not updated for what you decided (it still derives `f < a : A | b : B >`,
has the one-field labeled product, lacks `W`, the argument atoms, `_` in a pattern, the trailing
separators). Keeping two statements of one grammar in step is the drift L14.6 names.

Recommended: by L14.6 (the theory is the authority), `luthierSyntax` states the grammar; 2.S5 and
2.S9 keep their prose and their EBNF as an explanation that cites it, and `check_spec` or a test
compares the two until the chapter's EBNF is generated from the value.

## Mine to fix, no question

- Restore one-field record types: `{ x : A }` with no law is a record (my rule of D-2026-10-13-o,
  reversed: `Derives` and `Recognizer` did not parse, GPT and Claude); with a law it stays a subtype.
- `wellFormed` exactly the written trees (all four): clauses checked; `operatorAct` only with the
  operators the act binds; `validName` as "lexes as one name token"; a one-pattern tuple `(p)` is the
  pattern `p`, so the two tuple productions agree (Kimi).
- A tree law for each constructor still without one (all four): `floatLit`, `stringLit`, `pWild`,
  `pLit`, `pTuple`, `shapeParam`, `amp`, `eval A t` as an application, `match e { }`; laws for left
  association of application, of `and`, of `or`, for `mod` with `*`, for `-a + b`.
- The uniqueness argument rewritten (Kimi, Claude): settle the empty list first, then descend by
  length, by structure and by left calls; say which part of `WellFormedEbnf` serves what (`refsDefined`
  is hygiene) and that the domain is the equations' and the model's, not "well-formed EBNF" (GPT).
- Trailing comma in lists and `_` in a pattern: marked as additions (GPT, Claude, DeepSeek); a
  separator required between constructors of a `data` on one line, marked (Claude).
- `LayoutEndsWithNewline` excepts the empty program (GPT); the layout cases stated on `layout`
  itself, not only through `parse` (Claude); 2.S4 says a `}` at column 0 closes and does not start an
  act, and takes the `data`-brace rule (Claude).
- `NonNegativeFloat` defined with `:=`, a type with a law, not an alias (Claude, 4.R4).
- 4.R8: `==` on every `data` built from types that have it, recursive or not (Kimi).
