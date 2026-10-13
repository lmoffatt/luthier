# Review of round 3, by an external model

Answers to the eight questions, in order. Line references are quotes from the files as attached.

## 1. Was each finding fixed?

All items under "Fixed" verify against the files, except the dangling-else settlement, which is only half right (details in §4 and §6):

- **One-field record types restored** — yes. `recordFields := alt [seq [ref "fieldOne", opt (ref "sep")], seq [ref "fieldsTwo", …]]`, and `SubtypeTree` gives `{ a : Int | 0 <= a }` via the `subtypePattern` atom while `{ a : Int, b : Int | a < b }` goes to `record`. The two are disjoint (a single `fieldOne` cannot be followed by `|`), so the round-2 ambiguity is genuinely gone.
- **`wf` exact on written trees** — yes: `name s -> ok s` with `isName` (so `"and"`, `"_"`, `"a b"`, `"1x"` are out), `atLeastTwo` on tuples and `pTuple`, `allClauses` requires `nonEmpty SurfacePattern c.patterns`, `operatorAct o t -> memberString o boundOperators` (and `OperatorTree` checks `operator == := eqZ7` is rejected). Clauses checked; `pWild`, `pLit`, `(y)`, `cons _ rest`, `match e { }` all in `PatternTree`.
- **Role laws for constructors** — yes; I enumerate in §5.
- **Precedence** — yes; see §6.
- **Uniqueness argument rewritten** — yes; see §2. `LayoutEnds` allows the empty program (`isEmptyViews ts or lastIsNewline ts`); layout laws compare `layout` itself via `sameLayout`; 2.S4 in the chapter marks the `data`-brace reading and `}` at column 0 as proposed, and both files only rely on them in `BreakSeparatesConstructors`.
- **`NonNegativeFloat : U := { x : Float64 | 0.0 <= x }`** — yes, defined with `:=` and used in `floatLit`.
- **`luthierSyntax` is the authority** — yes, 2.S9 so states.

Two nits against `reply.md` itself: it names `wellFormed` and `WrittenProgram`, but the file has `wf`/`wfProgram`/`wfAct` and `ParsedIsWritten` — stale names in the reply, not in the code. And the claim "the tuple rule agrees in patterns and lambda parameters" holds only for patterns: `lparam` in `luthierSyntax` requires `(pattern, pattern, …)` with a comma, so `\(y) { t }` does not parse while `match m { (y) -> y }` does (§3).

## 2. The uniqueness argument of `ebnf.lth`

**Yes — on `WellFormedEbnf` the nine laws have exactly one solution, and the well-founded order described is correct.**

- Empty list: `derivesRhs e r nil` is `nullable e r`, by structural descent; a consumption-free chain of nonterminals is a chain of left calls (`leftCallsSeq` takes `leftCalls e r` when `nullable e r`, and `leftCalls e (ref n) = [n]`), and `noneLeftRecursive` excludes cycles. The boolean system for nullability is therefore acyclic and has one solution.
- Nonempty list: `SeqSplits` splits into (xs, ys); if xs is empty, `a`'s value is settled by the first step and `seq rs` is a structural subterm at the same list; if xs is nonempty both parts are shorter and the length induction applies. `RepRounds` forces the round to consume (`anySplit d e true …`), so its rest is shorter. `RefUnion` replacements at the same list are chains of left calls — finite on this domain.
- Bounds: `nullable`'s budget `ruleCount e` is enough — a simple consumption-free path visits each defined nonterminal once, and the number of defined nonterminals is ≤ the number of productions. Same for `reachesLeft e (ruleCount e)`: simple cycles have length ≤ #nonterminals ≤ `ruleCount`. Both definitions compute what their comments claim (one caveat: `ruleCount` counts productions, not distinct nonterminals; it is a safe over-approximation, which is all the claims need).

**Domain:** for the *model* the domain is exactly right — non-left-recursive grammars are precisely those where every cycle consumes a token, so `remainders` terminates (the `shorter` filter in `remaindersRep` handles `rep (opt a)`-style empty rounds). For *uniqueness alone* it is stricter than necessary: `S → seq [ref S, lit "x"] | eps` is left-recursive yet its equations force `derives S [x^n]` for all n and nothing else. The file says the domain is "the equations' and the model's", which is the honest statement; I would keep it and would not weaken `WellFormedEbnf`. `refsDefined` is indeed only hygiene (a missing nonterminal gives `anyRhs … nil = false`, still unique), as the comment says.

## 3. `luthierSyntax`

**It is a `WellFormedEbnf`.** Every production begins with a literal or category before any `ref`, and the forward chain `term → openForm/ampTerm → arrowTerm → … → patom` never points backward; no left calls cycle. Every nonterminal used is defined (`program` through `patom` — I checked), and `start := "program"` has a rule.

**Faithful to chapter 2**, with one divergence: 2.S9's `lparam` reads `"(" pattern { "," pattern } ")"`, but the value requires two patterns. Since the value holds where they differ, the chapter's production should be tightened to require the comma; today `\(y) { y }` is silently unwritable while its pattern counterpart parses. Minor, but it is exactly the class of text the tree laws should pin.

**Two-tree texts:** I found none beyond the known dangling-else. The overlap in `pattern ::= alt [seq [cat "name", rep patom], ref patom"]` (a bare name derives both ways) is harmless: both derivations yield the same tree `pApp n []`. Record-vs-subtype (`{ a : Int }` vs `{ a : Int | p }`), block-vs-record-value (`{ a := 1 ; a }` vs `{ a := 1 }`), and datum-vs-definition are all disjoint on first token after the initial `name`.

**`argAtom` vs `atom` does exactly what 2.S10 asks:** application arguments are `argTerm → argAtom`, which excludes the `< … >` form, so `f < a : A | b : B >` parses as a comparison (`SumAsArgument` confirms both directions).

One lexical note, not a defect: `x := --1` lexes as a comment, not negation of a negative — inherent to `--` comments and worth a tree law if anyone cares.

## 4. The new laws of `grammar.lth`

One is wrong; the rest check out.

**Wrong — `endsInOpenIf`:**
```
ifThen c a b -> match b { nothing -> true ; just e -> endsInOpenIf e } ;
```
The else branch must not be examined: `just _ -> false`. With the recursion as written, `wf` rejects the tree of a text that exists. Concretely, `x := if x then (if a then b else if c then d)` parses (parenthesized sum position) to `ifThen x (ifThen a b (just (ifThen c d nothing))) nothing`, whose then-branch has `endsInOpenIf = true`, so `wfProgram` rejects it and `ParsedIsWritten` — `match g.parse s { parsed p -> wfProgram (isName d g) p … }` — fails on that text. The designer's rule (reply.md) only forbids a then-branch ending in an if *without* an else; a then-branch whose own else is present can always be parenthesized by the printer and parses back unchanged (`… else if c then d else Y` binds inward, so the unparenthesized print is wrong, which is the printer's problem, not the tree's). One-line fix, and it makes `endsInOpenIf` settle the dangling else *exactly* (see §6).

**No missing constructor laws.** Enumerated: `Rhs` — 8 constructors, 8 laws; `Literal` — `LiteralTree` (3); `SurfacePattern` — `PatternTree` (4); `LambdaParam` — `LambdaTree` (3, `shapeParam` included); `Item` — `BlockOrRecordValue` (2); `Surface` — all 27 constructors appear in at least one tree law (`sigma` via `OpenForms`'s `(a : A) * (b : B) * C`; `world` and `&` via `UniverseWorldAmp`); `Body` — 3 laws; `SurfaceAct` — 6 constructors, 6 tree laws (`DatumTree` covers `eval A t` as an application).

**`wf` is otherwise exact:** `record fs law` enforces `namesCount fs >= 2 or law == nothing` (matching "a single labeled field with a law is a subtype"); `binop` requires `memberString o binaryOperators` where `binaryOperators` is *derived* from the grammar; names are exactly the lexer's name tokens. With the `endsInOpenIf` fix I find no tree `wf` admits that no text gives, and none it rejects that a text gives (modulo the `lparam` comma, §3, which is the grammar's own restriction). One soft spot: `lexFailed`'s role is only tested negatively (`not (lexes d g "\"abc")` in `StringTokens`); `parsed`/`parseFailed` have `ErrorsHaveLines`. A positive law for `lexFailed` (it carries line, column, message) would complete the set — sums' injections deserve the same coverage the `data` constructors now have.

## 5. Meaning of the constructors

Yes — each remaining `data` has a law per constructor, per the enumeration in §4; the removed three (`Keyword`, `Op`, `TokenKind`) are genuinely redundant: the derived sets reproduce 2.S21 exactly. The alphabetic literals of `luthierSyntax` are `import operator as data match if then else U W quote and or mod`, which is precisely the keyword list of 2.S21 plus the three operator-words; punctuation literals are sorted by `literalLexes` into `keyword`/`symbol`/`newline`. `binaryOperators = litsOfNames luthierSyntax precedenceLevels` recovers `& -> or and == /= < <= > >= + - * / mod`, and `boundOperators` recovers `+ - * / and or mod`, matching `opSymbol` and the `operator` act's restriction. `catsOf` yields exactly `name number string`, so the token kinds are the grammar's categories plus `keyword symbol newline` — as the `Token` comment claims. The derivation is sound and, more than that, load-bearing: `LiteralsAreNotNames` and `KindsAreTheGrammars` would fail loudly if the grammar drifted.

## 6. The precedence table

Clear, and the grammar realizes it level for level: level 1 open forms via `term := alt [ref "openForm", ref "ampTerm"]` with `openForm` reachable only as a whole `term` or on the right of `->` (`arrowTerm`) and `&` (`ampTerm`) — never as an operand, matching "an open form is never an operand, except on the right of `->` and `&`". Negation sits between application and `*` (`negTerm := alt [seq [lit "-", ref "negTerm"], ref "appTerm"]`), giving `-f a = -(f a)` and `f -x = f - x` as the `Negation` law states. Left associativity via `rep`, right via right recursion — `LeftAssociative`, `RightAssociative`, `OrBeforeArrow`, `ArrowBeforeAmp`, `EqualityBeforePlus` all agree with the table. Unambiguous except for the dangling `else`, and `endsInOpenIf` settles that one — exactly, once the else-branch recursion is removed (§4); as written it settles a larger set than the designer's rule and rejects writable trees.

## 7. Syntax of the files

Nothing I believe would fail to parse under chapter 2 as it now reads, with three dependencies on proposals the files already exercise — flagging them because a "no" on the proposal is a parse error here:

1. **String escapes** (2.S1, proposed): `lit "\n"` in `ebnf.lth`'s `program` rule and in `LiteralsAreNotNames`'s `w == "\n"` clause; `"x := \\ y (z : Int) { w := y ; z }"` in `LambdaTree`; `"\""` in `StringTokens`. Without `\"`, `\\`, `\n` these lines do not lex.
2. **`_` as a pattern atom** (2.S5, proposed): `match … { _ -> false }` in `wf`, and `cons _ rest` inside `PatternTree`'s string.
3. **The `data`-brace layout reading** (2.S4, proposed): relied on only by `BreakSeparatesConstructors`.

Otherwise: multi-line `&`-conjunctions (`Derives := EpsEmpty & … & OptEmptyOrOne & RepRounds`) are legal continuation lines; the trailing comma in `Grammar`'s record type is covered by `TrailingSeparators`; single-field records (`Derives : { derivesRhs : … }`, `Recognizer … : { accepts : … }`) are legal again; `data { }` with trailing `;` in `Literal` is allowed; dotted-name tokens (`m.f` in `ProjectionTree`) lex as one name. The loose functions of `ebnf_model.lut` (`remainders` etc. at bare exponentials) are knowingly non-compliant with 4.S17, which is a report, not a rejection.

## 8. What I would change first

`endsInOpenIf`: replace `just e -> endsInOpenIf e` with `just _ -> false`. It is one line, it is the only place where a *stated law* (`ParsedIsWritten`) is false on an existing text, and everything downstream of it (`Grammar`'s conjunction, any future specimen certified against it) inherits the breakage. Second would be the `lparam` comma in chapter 2.S9's text to match the value — but that is commentary, not a law.

## Separate item: disagreement with the specification

None beyond the `lparam` wording above, where the value is already the authority by 2.S9's own rule. On the substance of the round-2 rejections (`Derives`/`Recognizer` as function-typed theories, the character-level lexer grammar): the one-field record serves, and the lexer-as-`Ebnf` remains a fine next step — the rewrite did not make either worse.