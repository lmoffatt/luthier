I'll read the rewritten files and the changed chapters.

`luthierSyntax` is well-formed by the file's own predicates. Now the texts the laws use, and ambiguity counts (number of distinct derivation paths of the whole text).

All acts of the three files derive under the file's layout reading, except the two one-field record types. Let me grep a few remaining syntax questions.

Everything I need is checked. Findings follow, in the order asked.

---

## 1. Was each finding fixed?

All items under "fixed" do what they claim except these:

- **Non-recursive `data` / observers bound by laws.** The observers exist (`kindName`, `keywordText`, `opText`) and the injectivity laws are written (`grammar.lth:456-458`), but nothing claims them: they are not in `Grammar`'s conjunction (`:635-649`) and a `data` has no `:=` to attach them to. Under 4.S14/4.S18 an unclaimed law "defines nothing" and `r2_unclaimed_laws.reject.lut` rejects it, so as written they are never run. The spec's new sentence in 4.R3 names no mechanism for binding a law to a `data`. See 5.
- **Trees no text gives / `WrittenProgram`.** `wellFormed` still admits unprintable trees, so `RoundTrip` is still unsatisfiable: `:278` `define x bs t b cs -> … wellFormedBody b` checks nothing in `cs`; `:281` `operatorAct o t -> wellFormed t` admits any `Op`, but `:326` prints only `+ - * /`; `:206` `validName s := s /= "" and not (isKeywordText s)` admits `"and"`, `"_"`, `"a b"`, `"1x"` — none lexes as one name token (so `pApp "_" []` is a second `pWild`, the overlap just removed for `pName`). Also `floatLit` of `+∞` (`:91`) has no spelling.
- **Trailing separators.** `:362` also allows `[a, ]`, which D-2026-10-13-o does not grant; unmarked.
- **`lex` and `layout` characterized.** `lex` now is. `layout` is pinned only by `LayoutEndsWithNewline`; every layout case goes through `parse`. A `layout` returning any fixed derivable list ending in `"\n"` whenever `parse` succeeds still passes. Stating the layout cases on `layout` itself (`g.layout` of the two lexings equal) would characterize it and cost less.

Everything else — `withStart` gone, `Derives`/`backtrack`, `Recognizer` binders, renames, `pApp`, records/subtypes, `Op`s for `and/or/mod`, `sameParse`, tree laws, final newline, `argAtom`, `import` as keyword, theory a name, fuel, `tokenCount`, `StartIsRef`, the spec fixes — checks out; I verified every case-law text against the transcribed `luthierSyntax` and the file's layout prose (all derive or fail as the laws say).

## 2. The uniqueness argument of `ebnf.lth`

- **Exactly one solution on `WellFormedEbnf`: yes.** Existence: the finite-derivation semantics satisfies all nine (`RepRounds` is Kleene star with empty rounds removed). Uniqueness: by induction on `|ts|`, and within a length on left-call depth — but not by the order the file states.
- **The order as written (`:184-187`) is not well-founded.** "A right-hand side reached without consuming" is cyclic for any right recursion: for `S ::= "x" S | eps`, `SeqSplits` mentions `seq [ref S]` at the *whole* list through the split `(nil, ts)`, so `ref S → seq [lit "x", ref S] → seq [ref S] → ref S` at one list. That dependency is dead because `derivesRhs e (lit "x") nil = false` — a fact about the solution, not the syntax. The proof must (a) first settle `ts = nil`, where every same-list cycle either runs through nullable prefixes (left recursion, excluded) or through a `false` conjunct, and (b) at longer lists count only continuations behind nullable prefixes, which is `leftCalls`. Say that, since the sentence is what a later proof will follow.
- **`nullable`, `leftCalls`, `reachesLeft` compute what they claim**, and `ruleCount` suffices: a nullable derivation need not repeat a nonterminal on a path, and a shortest left-call cycle visits distinct nonterminals, so both are bounded by the number of nonterminals ≤ `ruleCount e`; the budget decrements once per `ref` (`:74`) and once per edge (`:106`). (`k - 1` at `k : Nat` is a typing obligation, discharged by the branch under 4.R11.)
- **Domain:** right for the equations. `refsDefined` is hygiene, not needed for uniqueness (an undefined nonterminal derives nothing by `RefUnion`); say which clause serves what. The laws quantify over every `Rhs`, not just those of `e`; uniqueness still holds, since a cycle can only close through `e`'s rules.

## 3. `luthierSyntax`

- **A `WellFormedEbnf`:** yes — every nonterminal defined and used, none left-recursive by the file's own `reachesLeft`, only `program` nullable, no `rep` of a nullable body.
- **Faithful to chapter 2 as it now reads**, with unmarked differences: `:383` adds `_` to `patom` (needed, `cons _ rest`); `:362` trailing `,` in lists; `:333` requires `;` between constructors (2.S5 makes each optional); `subtypePattern` (`:373`) narrower than 2.S9's `pattern`, documented at `:220`. And chapter 2.S9's own EBNF was not updated for what the notes decide: it still derives `f < a : A | b : B >` (`term atom`), still has the one-field labeled product, lacks `W`, `argAtom`, `_` in `patom` and the trailing separators — a spec item.
- **Texts with two trees.** Beyond harmless duplicate derivations (`_` and a bare name in a pattern, two routes, one tree), two real families, both inherited from 2.S9: (i) an atom that ends in a `term` followed by an argument or operator — `(n : Nat) * Vec n` is `sigma n Nat (Vec n)` or `app (sigma n Nat Vec) n`; likewise `(a : A) -> B c`, `(a : A) -> B & C`, `(a : A) -> B -> C`, `f if c then a else b + 1`, `f match m {…} z`; `SigmaTree` pins one instance, nothing pins the rule. (ii) `(a : A) * B * C` and `(a : A) * (b : B) * C`: dependent product of `B * C`, or `times` of the atom and `C`. The rule to state is 2.S11's, generalized: the trailing term of an open form extends as far right as possible.
- **`argAtom`:** does what 2.S10 asks — verified: `f (< a : A | b : B >)` derives, `f < a : A | b : B >` does not.

## 4. The new laws of `grammar.lth`

- **Wrong:** none of the case laws; all 50-odd texts derive or fail as the law says. `BlankAndCommentLinesDropped` holds only if the prose at `:300` means a comment line is gone *with its line break* (my literal reading left a leading `"\n"`); say so.
- **No law:** application associates left (`f a b` = `(f a) b`); `and`/`or` associativity; `==` against `+`; `a mod b * c`; `-a + b`; the open-form extent of 3; a float or string literal as a tree; `pWild`, `pLit`, `pTuple` in a `match`; `shapeParam`; `amp` as a tree; clauses (finding 2); the trailing separator of a record type or a block; `match e { }`.
- **`wellFormed` is not the set of written trees.** It admits trees no text gives: clauses unchecked (`:278`), `operatorAct` with any `Op` (`:281`), `validName` without the lexer's name grammar (`:206`): `name "and"`, `name "_"`, a name with a space. One well-formed unprintable tree is enough for `RoundTrip` to have no model, so `Grammar` has none. It rejects no tree a text gives that I could find. `validName` should be "lexes as one name token" — under L14, the lexer's name grammar stated as data, or `validName` taking `g`.

## 5. Meaning of the constructors

- `Rhs`: every constructor has its law in `Derives` ✓. `Keyword`: `keywordText` plus `KeywordsLexAsKeywords`/`KeywordsReserved` (exhaustive) ✓. `TokenKind`: `kindName`, each kind named by some lexical law ✓. `Op`: `opText`; every operator appears in a precedence law ✓. `SurfaceAct`, `Binder`, `Body`, `Item`: each constructor in a tree law ✓. `Surface`: all but `literal (floatLit _)`, `literal (stringLit _)`. `SurfacePattern`: `pWild`, `pLit`, `pTuple` by no case law. `LambdaParam`: `shapeParam` by none.
- **Told apart by nothing but `RoundTrip`:** `intLit` from `floatLit` — `NumberTokens` pins the lexer, no law says `3.5` becomes `floatLit`; a model that swaps the two spellings consistently passes. Same for the pattern constructors above.
- **The injectivity laws are claimed by nothing** (see 1). 4.R3 now says a `data`'s constructors mean what "an observer bound to it by a law" says; the spec gives no form that binds a law to a `data` (a `data` has no `:=` for laws, and 4.S14 rejects a loose law). Either a `data` with laws is written as a theory over the enumeration (`KeywordText : Keyword -> String`, laws, `KeywordText := …`, `keywordText` its model), or the spec adds the binding.

## 6. The two new findings

- **`import`, `as`:** agree. 12.S22 retired `la := import "x.lut"`, so 2.S21's "`import` gives a module value" is stale and must go; `import` binds names and is the tenth keyword. `as` is not needed for derivation (`lit "as"` matches a name token by text); reserving it only keeps `as` from being an imported name. Simplest: reserve both, and drop the "acts as a keyword in its position" class for good.
- **Clauses:** agree. 2.S5 should read `definition ::= name { binder } [ ":" term ] ( ":=" body | clause { clause } )` — a body *or* clauses, never both — and then `define` (`:191`) should carry a sum of the two rather than `Body` and `List Clause` side by side, with a `ClauseTree` law.

## 7. Syntax of the files

- `ebnf.lth:133` `Derives : { derivesRhs : … }` and `:198` `Recognizer … : { accepts : … }` — one-field record types, which D-2026-10-13-o ("`{ x : A }` alone is not a form"), `SubtypeTree` (`:605`) and `luthierSyntax` (`:367-372`) all reject. Verified: the only two acts of the three files that do not derive from `luthierSyntax`. Yet `ebnf_model.lut:58` writes the one-field *value* `{ derivesRhs := … }`, which is allowed: a value whose type cannot be written.
- Every `}` at column 0 (`ebnf.lth:33,79,95,117`; `ebnf_model.lut:29`; `grammar.lth:51,…,469`) starts a new act under 2.S4 as it reads ("An act starts at column 0"); the file's prose (`:301`, "outside every bracket") and `BreakSeparatesItems` (`\n}`) fix it. 2.S4 must say it, and must take the file's `data`-brace rule (`:304`).
- `grammar.lth:91` `NonNegativeFloat = { x : Float64 | 0.0 <= x }` parses, but an alias of a subtype is a lawful type that 4.R7 never certifies; 4.R4 wants `:=`.
- Everything else parses under chapter 2 with the escapes of 2.S1 [proposed].

## 8. What I would change first

`Derives` and `Recognizer`: make them function-typed theories (`Derives : Ebnf -> Rhs -> List TokenView -> Bool`, laws over `d e r ts`, `backtrack : Derives := \ e r ts { … }`), or have the spec admit `{ x : T }` as a record without a law. Reason: these two lines are the pattern's own center, and the grammar the same files state rejects them — the first thing certifying `grammar.lth` against itself would report — and the asymmetry (one-field value writable, its type not) will bite every one-operation theory that copies them.