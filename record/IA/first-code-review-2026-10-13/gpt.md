1. **Conformance to the specification.**

The clearest hard violations are in `grammar.lth`.

- Chapter 3 says: **“A `data` definition has at least one constructor that mentions the structure being defined. A non-recursive sum of products is written with the structural formers and named by an alias.”** 4.R4 says the checker rejects a non-recursive `data`. 03-kernel 04-static-semantics But `grammar.lth` has, for example, `"TokenKind : U := data {"`, `"Keyword : U := data {"`, `"Literal : U := data {"`, `"Op : U := data {"`, `"Binder : U := data {"`, `"Body : U := data {"`, and `"SurfaceAct : U := data {"`; none is recursively self-referential. grammar grammar grammar Those should therefore be rejected by the specified checker. `LambdaParam` and `Item` are also non-self-recursive, although they participate in mutual cycles through `Surface`; 3.R3 does not say whether mutual recursion rescues them.

- `grammar.lth` adds a top-level form:
  > `"datum : Surface -> SurfaceAct"`
  
  and then:
  > `"act" ... "datum"`  
  > `"datum", rhs := ref "term"`
  
  grammar grammar Chapter 2 says `act ::= declaration | definition | alias | directive`; it does not contain a general top-level term. 02-grammar The file cites D9, but does not mark this `proposed` or “a question for the specification”. `TopLevelDatum` therefore tests an unmarked addition, not chapter 2. grammar

- The EBNF is not exactly chapter 2. In particular, chapter 2 permits an optional trailing semicolon on every `data` constructor and every `match` arm. 02-grammar 02-grammar `luthierSyntax` instead allows separators *between* constructors/arms but no trailing `;`. grammar grammar So, for example, a final `;` in `match x { a -> b; }` is accepted by chapter 2 and rejected by `luthierSyntax`.

- `"program" := rep (seq [ref "act", lit "\n"])` adds a representation requirement that chapter 2's `program ::= { act }` does not state. grammar 02-grammar It can be equivalent only if `layout` guarantees a synthetic `"\n"` after the last act; no such law is stated.

- The import production allows arbitrarily many imported names:
  > `ref "importName", rep (ref "importName")`
  
  grammar 12.S22 only specifies the singular forms `import "x.lth" Theory` and `import "x.lut" Model : Theory [as X]`. 12-files-and-tools Multiple names may be a sensible extension, but it is not marked as one.

- There are several smaller unmarked additions: `endToken`, token line/column positions, `LexError`/`ParseError`, and the assertion that numeric spelling decides `Int` versus `Float64`. Chapter 2 specifies the lexical spelling of numbers, but not that AST classification. grammar grammar The string escapes, by contrast, are correctly marked `proposed`; `quote` as a keyword is correctly marked as a question. grammar

- There is also a conflict with 12.S23/L2.6. A theory file is said to contain **“types, declarations and laws”**, with model values in `.lut` files. 12-files-and-tools L2.6 says the same. principles(7) Yet `ebnf.lth` contains concrete helper implementations (`append`, `rulesIn`, `withStart`, `splits`, ...), and `grammar.lth` contains concrete values/functions including `keywordText`, `opText`, `tokenView`, and especially `luthierSyntax : Ebnf := ...`. ebnf grammar If definitional helpers are intended to be legal in `.lth`, S23 needs to say so; as written these files establish a pattern contrary to it.

**Disagreements inside the specification itself:** 3.R3 says all `data` must be recursive, but 3.S7 says `Unit` and `Empty` are themselves defined as `data`; those statements cannot both hold without a core exception. 03-kernel 03-kernel Also 2.S21 turns `test` and `cite` into functions, while the act grammar has no bare-expression act. 02-grammar That explains why `grammar.lth` invented `datum`, but the repair belongs in the specification first. Finally 2.S20 says the future grammar theory would be `grammar.lut`, while 12.S23 now says theories are `.lth`; that is stale prose. 02-grammar

2. **Conformance to the principles.**

`ebnf.lth` has made the right architectural move—`derives` is now a hole and its old implementation is in `ebnf_model.lut`. That matches L9.2/4.R10: the implementation should be a model, not the law. ebnf principles(7)

But `derives` is **not actually determined by its laws**. The file says its laws describe Kleene repetition as “the least fixed point”, yet `RepUnfolds` only states the fixed-point equation. ebnf ebnf Thus the selected model still decides what happens at non-well-founded fixed points. So the L9.2 problem has moved, but not disappeared: the implementation is no longer textually the law, yet the incomplete law leaves semantic choices to the implementation.

There is also an L14 failure in `grammar.lth`. L14 says the prose explains and the Luthier theory defines. principles(7) Here lexing, layout, and the mapping from syntax into `Surface` are only partly characterized by laws. `ParsesWhatDerives` characterizes *acceptance*, while `RoundTrip` merely says parser and printer agree with each other. grammar A parser/printer pair can agree perfectly while assigning the wrong `Surface` constructor to uncased syntax. On those parts, the host implementation still supplies meaning.

The concrete values/functions in `.lth` files also conflict with settled L2.6's theory/model separation unless “helper definitions needed to state a law” becomes an explicit exception. principles(7)

So: **for `luthierSyntax` specifically**, which is non-left-recursive and apparently consuming, `ebnf_model.lut` probably gives the intended answer. **For `derives` as the generic operation declared in `ebnf.lth`, the laws do not determine it.**

3. **The laws of `ebnf.lth`.**

They are neither complete nor, as written, consistent.

First, `withStart` is not fresh:

> `withStart ... := { start := "'start", rules := cons { lhs := "'start", rhs := r } e.rules }`

ebnf

Take an `e` already containing `"'start" -> lit "x"` and `ts = ["x"]`. `EpsEmpty e ts` forces `derives (withStart e eps) ts = false`. But applying `StartIsRef` to that new grammar and then `RefUnion` sees both the newly inserted `eps` rule and the old `lit "x"` rule; `LitOne` makes the latter true. Contradiction. Thus for unrestricted `Ebnf`, **there is no total model satisfying all ten laws**.

Even after fixing freshness, they do not determine a unique relation. Two minimal witnesses:

- `S ::= S`: `StartIsRef + RefUnion` reduce to `D = D`, so both true and false are fixed points.
- `rep eps`: for any nonempty `ts`, `RepUnfolds` reduces to essentially `X = X`; the equation does not choose the least fixed point.

That is exactly the distinction the comment elides when it says:

> “`RepUnfolds` makes `derives` the least fixed point only together with termination”

ebnf Termination of an evaluator is not a mathematical least-fixed-point principle.

I find no obviously redundant constructor law: `EpsEmpty`, `LitOne`, `CatOne`, `RefUnion`, `StartIsRef`, `SeqEmpty`, `SeqSplits`, `AltUnion`, `OptIsAlt`, and `RepUnfolds` each covers a distinct case. `RepUnfolds` is not *wrong* for Kleene star; it is insufficient. `withStart` is the outright broken part.

4. **The laws of `grammar.lth`.**

Of the case laws with explicit expected trees, `UnionAsArgument`, `BlockOrRecord`, and `ImportNamesWhatEnters` look correct against their corresponding specification rules. grammar `TopLevelDatum` is the exception: its expected tree may match the file's invented grammar, but the form is absent from chapter 2. grammar

Most of the two-text equality cases have another weakness: they do not assert either side parsed successfully. For example,

> `g.parse "x := a + b * c" == g.parse "x := a + (b * c)"`

is also true if both are rejected. grammar `ParsesWhatDerives` is meant to close that hole, but only if the lexer/layout laws and `luthierSyntax` are themselves right.

Large parts of chapter 2 have no law that pins their **tree representation**. In particular: declarations/definitions/aliases; explicit/default/implicit binders; clauses; data bodies; Pi/Sigma/named products and sums; records and refined records; subtypes; lists; lambdas; matches; named arguments; `if`; projection versus dotted name; quote; and most pattern forms. RoundTrip cannot substitute for those laws: it proves only that printer and parser are inverses.

Lexical coverage is also thin: there is no general law for valid/invalid names, dotted names, number spelling, strings, or symbol tokenization. Layout cases omit several stated cases—`<...>`, match braces, record braces, deeper continuation—and the claimed `OperatorContinuesLine` case is at top-level indentation, where ordinary “indented line continues the act” already explains the result. Chapter 2's full layout rule is broader. 02-grammar

`luthierSyntax` is mostly a good precedence-stratified transcription, but it is not fully faithful for the reasons in 1: trailing `;` in `data`/`match`, top-level `datum`, multiple import names, and the explicit final-newline representation. grammar

I find **no left recursion** in `luthierSyntax`. The recursive paths through parentheses, lists, etc. consume a token before returning to `term`; `ampTerm`/`arrowTerm` use right recursion and the left-associative levels use `rep`.

5. **The surface tree.**

It covers almost all current chapter-2 forms, but its bigger problem is that it contains many values that are **not surface syntax at all**, making the universal `RoundTrip` law impossible as stated.

Examples: `name : String -> Surface` admits `name "if"` or `name ""`; `tuple : List Surface -> Surface` admits zero- and one-element tuples although the tuple production requires at least two terms; `lambda : List LambdaParam -> ...` admits zero parameters; `pi`/`sigma` admit an empty name list; `Binder` admits no names; `SurfaceAct.import_` admits no imported names. grammar A particularly sharp case is `literal (intLit (-1))`: lexical numbers have no sign, so printing `-1` parses as `neg (literal (intLit 1))`, not the original tree.

`SurfacePattern` has a real constructor overlap:

> `pName : String -> SurfacePattern`  
> `pCon : String -> List SurfacePattern -> SurfacePattern`

grammar `pCon "x" []` and `pName "x"` correspond to the same written token, so both cannot satisfy RoundTrip. And calling the second form `pCon` prematurely suggests “constructor”, even though 2.S13 explicitly says the parser does **not** decide whether a pattern name is a constructor, label, or variable. 02-grammar That is the clearest pair I would collapse or otherwise distinguish structurally.

Conversely, `record`/`recordLaw`, `bind`/`rebind`, dependent versus ordinary operator forms, and record-value versus block represent genuinely distinct written forms or distinctions chapter 2 cares about; I would not object to those being separate constructors.

I would carry source positions, but **not as fields participating in `Surface`'s structural equality**. If positions are directly inside the tree, `parse(print(p)) == p` usually fails because printing changes positions. Keep positions in a located wrapper/annotation, or state RoundTrip over the tree with positions erased.

6. **Syntax of the files themselves.**

Two lines in `grammar.lth` are definite problems under its own keyword choice:

> `match : Surface -> List (SurfacePattern * Surface) -> Surface ;`

grammar

`match` is a chapter-2 keyword, while a `data` constructor position requires a `name`. 02-grammar So that line cannot parse as written.

Likewise:

> `operator : Op -> Surface -> SurfaceAct ;`

grammar

The specification says `operator` is “possibly” a keyword, but `grammar.lth` explicitly chooses to keep it as one and its own `KeywordsReserved` law enforces that choice. grammar grammar Under that choice it cannot simultaneously be a constructor name.

`quote : Surface -> Surface` has the same self-conflict **if** the file's proposed/questioned decision to reserve `quote` is adopted; under chapter 2 as currently written, `quote` is not yet in 2.S21, so I would not call that one a definite parse failure.

Finally, these two import lines depend on an unstandardized extension:

> `import "ebnf.lth" Ebnf Rhs TokenView derives ...`  
> `import "ebnf.lth" Ebnf Rhs Production TokenView derives ...`

ebnf_model grammar 12.S22 specifies one named theory/model per import and never specifies a space-separated list. 12-files-and-tools I would therefore classify these as **not licensed by the specification**, rather than definitively syntactically impossible, because 12.S22 lacks a formal production.

I found no corresponding definite parse failure in `ebnf.lth` itself.

7. **The model file.**

For ordinary terminating, non-left-recursive grammars, `ebnf_model.lut` is a reasonable backtracking implementation of conventional EBNF: alternatives union remainders, sequences thread them, and repetition only recurses after consuming input. ebnf_model

It is not a model of the ten laws over *all* `Ebnf`, for two independent reasons. First, because the `withStart` collision makes the laws themselves inconsistent. Second, on left recursion it diverges exactly where

> `ref n -> remaindersAny e (rulesOf e n) ts`

recurses before consuming input. ebnf_model Indirect left recursion has the same problem.

Is that acceptable for sampled certification? **Only with the limited meaning Luthier assigns to a sampled certificate.** L8.3 explicitly allows a model with sampled evidence to be called a model with the evidence/cost recorded. principles(7) So sampling may legitimately say “this implementation passed this distribution of grammars.” It may not justify the stronger claim that this is a total recognizer for arbitrary `Ebnf`. A sampled generator that happens not to draw left recursion simply has no evidence about left recursion. If it does draw one, fuel exhaustion must not be silently counted as a passing Boolean case.

For `luthierSyntax` itself, the left-recursion problem does not appear to arise.

8. **What I would change first.**

`withStart`.

The line

> `{ start := "'start", rules := cons { lhs := "'start", rhs := r } e.rules }`

claims freshness that its type cannot guarantee. ebnf As a result the foundational theory can be **inconsistent**, which is worse than merely incomplete: there may be no model to certify at all. Make that freshness claim true or explicit before building more theories on `derives`. Immediately after that, the next issue is the missing least-fixed-point characterization.