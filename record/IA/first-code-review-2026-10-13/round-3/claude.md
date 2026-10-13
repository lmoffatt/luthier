Round 3. I'll read the rewritten `grammar.lth` and the chapters that changed.

Now the harness for this round: the new grammar, the lexer with the derived keyword set, and the layout prose as rewritten.

Random token soup is mostly undrivable; a better search generates sentences *from* the grammar and counts how many ways each derives.

The generator's depth bound was too small for the 13-deep precedence chain; it only produced import lines. Retry with a sensible depth.

All three files derive from `luthierSyntax` under the file's layout reading, act by act, each with one derivation. Here are the findings.

---

## 1. Was each finding fixed?

All items under "Fixed" do what they claim except these:

- **Precedence / the dangling `else` by a predicate.** `endsInOpenIf` is in `wf` (`grammar.lth:336-337`), but parentheses erase the condition in the tree: `x := if c then (if d then y) else b` derives, with exactly one tree, `ifThen c (ifThen d y nothing) (just b)`, which `wf` rejects. So `ParsesWhatDerives` forces the parse to succeed while `ParsedIsWritten` forbids its only honest tree. The one escape is a parser that returns `ifThen c (ifThen d y (just b)) nothing` for that text — wrong, yet it passes every law (its print re-parses to itself). See 6.
- **The grammar unambiguous but for the dangling `else`.** No: an open form on the right of `->` inside the left operand of `&` still derives two ways (`:191-192`). See 3 and 6.
- **The uniqueness argument.** Right in structure, one step still short. See 2.
- **One-field record restored.** In the grammar and laws, yes (`:218`, `RecordTree`); but 2.S9's note still says "the labeled forms take two or more names … so each text has one tree", contradicting D-2026-10-13-p. A spec item.

Everything else checks out: every lexical, layout, precedence and tree law's text derives, or fails, exactly as the law says (verified against the transcribed `luthierSyntax` and the layout prose); `wf` is exact apart from the point above; `import`/`as`/`and`/`or`/`mod` reserved and bound as claimed; `NonNegativeFloat` with `:=`; the layout laws compare `layout`.

## 2. The uniqueness argument of `ebnf.lth`

- **Exactly one solution on `WellFormedEbnf`: yes.** `nullable`, `leftCalls`, `reachesLeft` compute what they claim, and `ruleCount` bounds both a shortest nullable derivation and a shortest left-call cycle. The domain is right for these equations and this model, and the paragraph at `:150-156` now says which clause serves what.
- **One sentence still missing, in step one.** "A cycle of such descents would be a left-call cycle" holds only if the descent into a `seq` stops at its first non-nullable element: descending into every element, `ref S → seq [lit "x", ref S] → ref S` at `nil` is a cycle and not a left call. It is harmless because `derivesRhs e (lit "x") nil = false` settles the conjunction, which is exactly `leftCallsSeq`'s rule — say so, since a later proof will follow the sentence. Step two is right; it would be tighter to add that the split with empty first part counts only when that part is nullable, which step one settled.

## 3. `luthierSyntax`

- **A `WellFormedEbnf`:** yes — 42 rules, all defined and used, none left-recursive by the file's own predicates, only `program` nullable.
- **Faithful to chapter 2 as it now reads:** yes; the chapter now defers to it. The table of 2.S8 is realized level by level.
- **Two trees left.** Exhaustive search to 3 tokens and ~1.5 M random and ~0.4 M grammar-generated acts found one family besides the dangling `else`: `A -> O & B` with `O` an open form — `U -> (a : A) * b & C` is `binop "->" U (sigma a A (binop "&" b C))` or `binop "&" (binop "->" U (sigma a A b)) C`; likewise `A -> if c then x & y`, `(f) -> (b : B) -> C & D`. Cause: `arrowTerm` (`:192`) admits an open form on its right, and `arrowTerm` is the left operand of `&` (`:191`), so the open form's trailing term may or may not swallow `& …`. No law pins it (`OpenForms` has only `A -> (b : B) -> C`). The table's exception "except on the right of `->` and `&`" is the same ambiguity in words; the rule that removes it is "an open form is the last operand of its term": split `arrowTerm` into a closed chain and an open-ended one that nothing may follow.
- **`argAtom`:** does what 2.S10 asks; verified both ways.

## 4. The new laws of `grammar.lth`

- **Wrong:** none of the case laws. `wf` is exact except the `endsInOpenIf` clause (rejects a written tree) and `floatLit`/`pLit` of `+∞`, which `NonNegativeFloat` admits and no spelling gives.
- **No law:** the `->`-open-form-`&` extent of 3; `P & (x : A) -> Q`; `if` on the right of `->`/`&`; a clause with several patterns `| p, q := t`; `\ (a b : A) { … }`; `{ _ : T | p }`; and, on the lexer, that a word *not* among the literals lexes as a name — `NameTokens` has three positives, so a lexer may reserve `let` and still pass everything.
- **Sampling.** `RoundTrip` (`:388`) and `LiteralsAreNotNames` (`:416`) are implications over `SurfaceProgram` and `String`; a random tree almost never has every name lexing as a name, and a random string is almost never a literal, so nearly every sample is vacuous (L9.6). State each domain as the type quantified, with its generator (4.R7): `WrittenProgram d g` as a subtype, and `LiteralsAreNotNames` exhaustive over `litsOf luthierSyntax`.

## 5. Meaning of the constructors

- Every `data` left has a law naming each constructor's role: `Literal` (`LiteralTree`), `SurfacePattern` (`PatternTree`), `LambdaParam` (`LambdaTree`), `Item` (`BlockOrRecordValue`), all 24 of `Surface`, `Binder`, `Body`, `SurfaceAct`, and `Rhs` by the laws of `Derives`. The collections are aliases, as L2.7 wants.
- **The derivation is sound as a lower bound, not exact.** `LiteralsAreNotNames` says every literal is reserved; nothing says only they are (above). `literalLexes` lets each literal be keyword *or* symbol — harmless, since the grammar matches by text. `binaryOperators` and `boundOperators` compute the right lists (`& -> or and == /= < <= > >= + - * / mod`; `+ - * / and or mod`); `catsOf` is `name number string`.

## 6. The precedence table

Clear, and the realization matches it, with two defects: the exception in level 1 is the ambiguity of 3, and `endsInOpenIf` does not settle the dangling `else` exactly — it is a fact about the text, and parentheses remove it from the tree. The nearest-`if` rule belongs to the parser (`DanglingElse` already pins it); drop the clause from `wf` and have the printer parenthesize a then-branch that ends in an open `if` under an `else`, beside `(a).b` and `-(-a)` at `:386-387`. With that, the unparenthesized text keeps its one tree and the parenthesized one its own.

## 7. Syntax of the files

Every act of the three files derives from `luthierSyntax`, each in one way, under 2.S4 with its [proposed] readings. Nothing fails. One note: `ebnf.lth:70-79` and the like pass `k - 1` where a `Nat` is expected, a typing obligation on the `k == 0` branch (4.R11), not a parse matter.

## 8. What I would change first

Remove the `endsInOpenIf` clause from `wf` (`grammar.lth:336-337`) and move the rule to the printer: as it stands `Grammar` has a model only if its parser misreads `if c then (if d then y) else b`, and a text whose only tree is forbidden is the one defect here that no test will ever report as a failure.