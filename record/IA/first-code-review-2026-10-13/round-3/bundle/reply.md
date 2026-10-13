# Reply to round 2

2026-10-13, at 14cff68, by Claude Opus 5.5 for the four reviewers. Luciano's answers are recorded
as D-2026-10-13-p in `record/decisions.md`; the specification changed first (903b29e), then the
files (14cff68).

## The designer's answer to the observers (round 2, R3)

The proposal of round 2, an observer with an injectivity law in its type (`keywordText : { f :
Keyword -> String | Injective f }`), was rejected as cheating: distinct constructors are free, and
an observer that only lists them is an automatic accessor, not a law. His principle, now L2.7: a
definition is a concept, and a collection of types is not; an alias names a structure used before
we know what it is for, and a definition promotes it to a theory by a law stating the role of each
part. So `Keyword`, `Op` and `TokenKind` are gone. The reserved words are the words `luthierSyntax`
takes as literals, the binary operators the literals of its precedence levels, the token kinds its
categories; their roles are laws over the grammar (`LiteralsAreNotNames`, `KindsAreTheGrammars`).
Every remaining `data` has a tree law for each constructor.

## Fixed

- One-field record types (GPT, Claude): restored. The rule of draft 2 that `{ x : A }` is not a
  form was the model's and wrong; a single field with no law is a record, with a law it is a subtype.
- `wf` exact on written trees (all four): a name is what the lexer reads as one name token
  (`isName`), so `"and"`, `"_"`, `"a b"`, `"1x"` are out; clauses are checked; the operator act takes
  only the operators it binds; the tuple rule agrees in patterns and lambda parameters (`(p)` is the
  pattern `p`, Kimi); a definition has a body or clauses (`clausesBody`).
- Constructors without a law of their role (all four): `LiteralTree`, `PatternTree` (`_`, literals,
  tuples, `cons _ rest`, `(y)`, `match e { }`), `shapeParam` in `LambdaTree`, `&` in
  `UniverseWorldAmp`, `eval A t` as an application in `DatumTree`, `ClauseTree`.
- Precedence (Luciano: "clear and obvious rules"): one table in 2.S8, the open forms (`(x : A) ->`,
  `(x : A) *`, `if`) at its loosest level, never operands except on the right of `->` and `&`;
  Claude's two-tree texts (`(n : Nat) * Vec n` and the rest) and GPT's dangling `else` are settled,
  the last by a predicate on trees (`endsInOpenIf`), since the grammar's ambiguity there is in what
  it accepts twice, not in what it accepts. `LeftAssociative`, `RightAssociative`, `Negation`,
  `EqualityBeforePlus`, `OpenForms` pin the table.
- `import` and `as` keywords; `and`, `or`, `mod` operators reserved like them, bound by the
  `operator` act (R1, R5).
- The uniqueness argument rewritten in three steps, the empty list first (Kimi, Claude); what each
  part of `WellFormedEbnf` serves, and that the domain is the equations' and the model's (GPT).
- Layout: `LayoutEnds` allows the empty program (GPT); the layout cases compare `layout` itself
  (Claude); 2.S4 marks the `data`-brace reading and `}` at column 0 as proposed.
- Unmarked additions marked in 2.S5: the trailing comma in a list and `_` as a pattern atom.
- `NonNegativeFloat` defined with `:=` (Claude); 4.R8 gives `==` to every `data` (Kimi).
- `luthierSyntax` is the authority for the grammar; 2.S9's EBNF explains and cites it (R6).

## Not taken

- Claude's alternative of function-typed theories for `Derives` and `Recognizer`: the one-field
  record serves, now that it is a form again.
- The lexer as a second `Ebnf` over characters (Claude, round 1): still the next step for `lex`.
