I'll read the files that aren't in my context yet.

Confirmed three of my suspicions. Now the fresh-start contradiction and a left-recursion/nullable check of `luthierSyntax`.

Everything I need is verified. Here is the review.

---

## 1. Conformance to the specification

**Contradictions.**

- **`derives` is defined by its own laws yet used as a function** (`ebnf.lth:67`, `:111`). Under 4.S7, `x : T := p` with `p` a Law "defines `x` as the subtype `{ y : T | p y }`, a type: `x : U`". So after `derives := EpsEmpty & … & RepUnfolds`, `derives` is a type, and `derives (withStart e a) xs` (`:59`, `:62`, `:71` … `:121`) applies a type to arguments. Moreover the body is not "a Law over T" in 4.R6's sense: no law binds a value of `Ebnf -> List TokenView -> Bool`; they mention the name `derives` free. 4.R3 then rejects it ("over an unlabeled base it must touch its parameter"). Compare `Recognizer`/`AcceptsWhatDerives` (`:119-122`) and `Grammar` (`grammar.lth:248-378`), which follow 4.S8's Codec pattern correctly: the law takes `(r : Recognizer e)`, `(g : Grammar)`. The three files thus teach two patterns for "theory and model", and the one for `derives` is the ill-formed one.
- **Non-recursive `data`.** 3.R3: "A `data` definition has at least one constructor that mentions the structure being defined"; 4.R4 rejects "a non-recursive `data`". `TokenKind` (`grammar.lth:34`), `Keyword` (`:49`), `Literal` (`:65`), `Op` (`:72`), `Body` (`:140`), `Binder` (`:131`), `SurfaceAct` (`:150`) are all non-recursive and must be sums named by aliases. `Item`, `LambdaParam` (`:92`, `:98`) recurse only through `Surface`; 3.R3 as worded does not cover that either.
- **`ebnf_model.lut:53` redefines a defined name.** `derives` already has a body in `ebnf.lth:111`; 2.R3/4.R12: a second `:=` is "defined twice", not a fill of a hole. 12.S8's "declare in one file, define in another" applies only if ebnf.lth stops at the declaration (with the laws in its type).
- **Layout.** `grammar.lth:171-175` makes a line break a `;` only "between the items of a block"; 2.S4 says the same holds "inside the braces of a record type, a record value and a block".
- **`luthierSyntax` vs 2.S5/2.S9.** `:200` (data) and `:228` (match) forbid the trailing `;` that chapter 2's `[ ";" ]` allows; `:233` (block) drops `","` from `sep`; `:190` allows several names per `import`, which 12.S22 does not show.

**Unmarked additions.** The `datum` act (`:156`, `:194`) — cited to "D9 of the superseded plan", not in 2.S5. Infix `and`/`or`/`mod` "parse as applications of those names" (`:70-71`): chapter 2.S12 makes that a *kernel* translation; the surface tree is to keep "the acts as written" (2.S13). `Literal` splitting int from float "by its spelling" (`:63`). `ImportName.theory : Maybe Surface` (`:145`) admits any term where 12.S22 names a theory. `eval` of 2.S20 silently dropped; `let`/`in` dropped (right, by 2.S21, but say so). `endToken`/`newlineToken` (`:40-41`) have no counterpart in 2.S1. `ErrorsHaveLines` (`:367`) states a requirement no chapter states.

**4.S17 (decided, not R1–R8).** Every helper here is a "loose function" at a bare exponential: `append`, `rulesOf`, `splits`, `anySplit`, `keywordText`, `opText`, `tokenView`, `remainders`, … The libraries don't comply either, but these are meant to be the pattern; mark it.

**Where I disagree with the specification itself** (separate items):

- 2.S9 lists `"-" term` as an *atom*, so `f -x` would be `f (-x)`; 2.S15 says it is `f - x`. The file follows 2.S15 (`:209`). Chapter 2 must fix 2.S9.
- 2.S10 ("a union as an argument needs parentheses") is not a property of 2.S9's EBNF: `term atom` with `< … >` an atom derives `f < a : A | b : B >`. Checked: `derives luthierSyntax` accepts it. So an EBNF-faithful `derives` and 2.S10 cannot both be laws of the same `parse`.
- 2.S9's two subtype productions overlap on `{ x : T | p }` (one-field labeled subtype vs. pattern subtype). Two trees, one text.
- 2.S4 says nothing about line breaks inside `data { }` braces, nor whether a break after `,`/`;` is itself a separator. Every multi-line `data` in these files and `Grammar : { …, … }` (`:248-252`) depend on an answer.
- 3.R3 should read "mentions a structure of its own cycle" (1.S8); and 3.R2 + 4.R4 together force every enumeration into a unit-sum identified by shape, so `Keyword` is the same type as any other nine-case enumeration. Decide whether that is wanted for surface trees.
- 12.S8 ([implemented], same-name fill across files) and 12.S22/23 ([decided], a model is a named value imported "with its theory") do not compose: nothing says how a `.lut` names the hole it fills or how an importer reaches it. Both `derives` files sit on this seam.
- 12.S22 knows only theories and models; these files import an alias (`Ebnf`), a `data`, constructors (`eps lit …`), helpers (`append`) and a hole (`derives`), `grammar.lth:26`, `ebnf_model.lut:13`.
- 12.S23 "types, declarations and laws" vs L2.4 "no values": is `luthierSyntax : Ebnf := …` (a datum the laws need) a "model value"?
- 2.S1 strings have no escapes, so no law can spell a two-line text. The file's proposal (`:32-33`) is right; the chapter should take it.

## 2. Conformance to the principles

- **4.R10 / L9.2.** The ten laws of ebnf.lth are the equations of the regular operations, not an implementation — good. But `AcceptsWhatDerives` (`:120`) is "agrees with `derives`"; if `derives` is a hole filled by whichever file, that is 4.S20's *consistent, not characterized*. In grammar.lth, `lex` and `layout` are characterized by nothing but their appearance inside `ParsesWhatDerives` (`:269`): a model whose `layout` returns a fixed accepted list when `parse` succeeds and `[")"]` otherwise passes every law. 4.R3 is met (each label touched), L9.2 is not.
- **L14.** The grammar is data — good. The lexer (2.S1) is not stated in Luthier though it can be: a second `Ebnf` over characters (`TokenView` with kind `"char"`) and a `LexesWhatDerives`. The layout pass (2.S4) is stated only by cases. `desugar` deferred to `term.lth` is marked.
- **L10.1 / L9.6.** `RoundTrip` (`:259`) quantifies over all of `SurfaceProgram`, including trees no text denotes (see 4/5); the certificate's domain must be a stated subtype. Likewise the `Ebnf` generator will draw left-recursive grammars, on which the model exhausts fuel; the honest domain is `{ e : Ebnf | NotLeftRecursive e }`, a predicate worth writing in ebnf.lth.
- **Is `derives` determined by the laws?** No, three ways. (i) The equations admit non-least fixed points: for `S ::= S`, RefUnion is a tautology; for `rep a` with `a` nullable, `derives (rep a) = true everywhere` satisfies RepUnfolds. (ii) The fresh symbol is not fresh (see 3). (iii) Structurally, since the laws name `derives` rather than quantify over a model, `Grammar`'s `ParsesWhatDerives` and `Recognizer`'s law run against whatever file fills the hole — and no file imports one, so `ParsesWhatDerives` never reduces (3.S19). The model's behaviour (fuel on left recursion) would leak into `Grammar`'s certificate. For the one grammar that matters, `luthierSyntax`, the laws *do* determine `derives` by induction on length: it has no left recursion and no `rep` of a nullable body (checked).

## 3. The laws of `ebnf.lth`

- **Inconsistent, through `withStart`.** `:49` uses the fixed name `"'start"`. Take `e₀ = { start := "S", rules := [{ lhs := "'start", rhs := eps }] }` and `e₁ = withStart e₀ (lit "y")`. `LitOne e₀ "y" []` demands `derives e₁ [] == false`. But `StartIsRef e₁ []`, `RefUnion e₁ "'start" []` and `EpsEmpty e₁ []` give `derives e₁ [] == true`. No model satisfies all ten on grammars that use `'start`; the model in ebnf_model.lut gives `true` there. A sample will not see it unless the generator draws that string — exactly the kind of flaw a pattern must not carry. Fix at the root: declare the operation over right-hand sides, `derivesRhs : Ebnf -> Rhs -> List TokenView -> Bool`, with `derives e ts = derivesRhs e (ref e.start) ts`; then no fresh symbol is needed and `withStart` disappears.
- **Incomplete.** Least-ness is unstated (above). The characterizing form is a witness: a `Derivation` data with `valid : Ebnf -> Derivation -> Bool` and `yields`, and `derives e ts == exists d. valid e d and yields d == ts` (L9.11/12); the ten equations then become theorems.
- **Redundant:** none; `SeqEmpty` is the base `SeqSplits` lacks, `OptIsAlt`/`RepUnfolds` are the definitions of `opt`/`rep`.
- **Wrong, mildly:** `lit s` (`:75`) matches by text only, so `lit "import"` also matches the string literal `"import"` if the lexer strips quotes from `text`; say which.

## 4. The laws of `grammar.lth`

**Case laws inconsistent with `ParsesWhatDerives`** (verified with the transcribed grammar and model):

- `:354` `not (isParsed (g.parse "import \"x.lut\""))` — but `datum ::= term` derives `import "x.lut"` as an application (`import` is a name under 2.S21). Likewise `import "x.lth" A` derives twice (import act and datum).
- `:323` `not (isParsed (g.parse "x := f < a : A | b : B >"))` — derives (see 1).
- `cat "name"` includes `and`, `or`, `mod`, `as`, `import`, so `x := a or` and `x := f and` derive; a parser reading `or` as infix must then fail `ParsesWhatDerives`.
- `:185` `rep (seq [ref "act", lit "\n"])` demands a `"\n"` after the *last* act, and nothing consumes `endToken` (`:41`); a text with no trailing newline, a blank line between acts, or a leading comment line (all three files) does not derive unless the layout pass is specified to add/collapse `"\n"`. It isn't.
- `:334` (`{\n  a := 1 …`) needs the break right after `{` dropped; neither 2.S4 nor `:171-175` says so.
- `:332` `x := [a,\nb]` with `b` at column 0: right by 2.S4, but `:172` ("a line break at column 0 … ends an act") says the opposite.

Expected trees themselves look right; `:358` uses an option name `n` that is none of 2.S21's.

**Rules with no law:** 2.S1 number spellings, dotted name as one token, `'` in names, unterminated string; 2.S5 binders, clauses, `data` bodies, alias with binders; 2.S6 `operator`; 2.S7 defaults `(tol : T <- d)`; 2.S8 `/= <= >= mod`, left-association of `* /` and comparisons; 2.S9 tuples, the four dependent/named forms, subtype, sum, list, lambda forms, `match`; 2.S10 pattern shapes; 2.S14; 2.S16 `{A B : U}`; 2.S20 `quote`; 2.S4 "indented deeper than the first item" and the match-braces rule; nothing observes `lex` or `layout` directly.

**`luthierSyntax`:** no left recursion, including through nullable prefixes; every nonterminal defined and used; precedence strata match 2.S8. Unfaithful on: trailing `;`, `,` in blocks, end of input, multi-name import, `eval`, and over-acceptance via `cat "name"`.

## 5. The surface tree

Complete for chapter 2 except `eval` (2.S20) and, deliberately, `let`. Trees no text denotes make `RoundTrip` unsatisfiable: `intLit (-3)` (`:66`, the grammar has no signed number — use `Nat`), `name "if"`, empty `tuple`/`record`/`sum`/`lambda []`/`pi []`, `pCon s []` vs `pName s`, `recordLaw [(x,T)] p` vs `subtype (pName x) T p` (one text), `proj (name "a") "b"` vs `name "a.b"` (printer must write `(a).b`), `neg (neg x)` (`--x` lexes as a comment), `floatLit` NaN. Either a `WellFormedSurface` predicate as the law's domain, or tighten the types. One constructor where two: `record`/`recordLaw` should mirror `ifThen`'s `Maybe`; `subtype` with a bare-name pattern duplicates one-field `recordLaw`. Two where one: `and`/`or`/`mod` as `app` loses "as written" and precedence; make them `Op`s. Positions: yes — 2.R3/2.R6/4.R6 report errors *against the declaration*, which needs a place. Cheapest and cleanest: keep `Surface` pure and return spans beside it, `ParseResult` carrying `program` and `spans : List (Path * Span)` keyed by tree path; `RoundTrip` compares `program` only and survives untouched, and a separate law binds each span to the text it covers.

## 6. Syntax of the files themselves

- `grammar.lth:124` `match : Surface -> …` — `match` is a keyword (2.S21); not a name.
- `:128` `quote : Surface -> Surface` and `:155` `operator : Op -> …` — keywords by the file's own `:49-51`.
- `:348`, `:351`, `:354` — `\"` ends the string under 2.S1; the rest of the line is garbage. `:185` `"\n"`, `:227` `"\\"`, `:329-337` — two characters each under 2.S1, so the laws don't mean what they say until the escape proposal is accepted.
- `:248-252` `Grammar : {` … `,` + line break — under 2.S4 two separators; chapter 2's record grammar has no empty item. Every multi-line `data` (`ebnf.lth:22-30`; `grammar.lth:34-41, 49-51, 65-68, 72-76, 84-89, 92-95, 98-100, 103-128, 131-133, 140-142, 150-156`) assumes a rule 2.S4 does not give.
- `grammar.lth:26`, `ebnf_model.lut:13` — multi-name imports of aliases, constructors, helpers and a hole: 12.S22 shows none of these forms.
- `ebnf_model.lut:47` `length`, `ebnf.lth:38` `append`, `grammar.lth:75` `eq`, `div`, `plus` … — if `core.lut` defines any, 2.R3 refuses the redefinition (core encloses the scope, 12.S22). Can't verify without core.lut.
- `ebnf.lth:111`, `grammar.lth:372-378` — continuation lines starting with `&`: parse (indented).

## 7. The model file

Where it terminates, `remainders` is exactly the least fixed point: each arm is the right inverse of one law, `shorter` (`:44`) makes `rep` of a nullable body terminate and still yields the lfp, `opt`/`seq`/`alt` are sound. So it is a correct model of the intended semantics. It diverges on left recursion including through nullable prefixes (`seq [opt x, ref S]`), and, as above, it is the *wrong* value on grammars using `'start` because the theory is. Three defects as a file: `:53` redefines a name that already has a body (should be `backtrack : Derives := …`, named, 12.S23); `:13` imports `derives` to overwrite it; `length` likely collides with core. Acceptable for a sampling certifier only if the certificate's domain is the subtype of non-left-recursive grammars (L10.1, L9.6) and the generator is that subtype's (4.R7): random small grammars are often left-recursive, so otherwise fuel exhaustion, not failure, dominates the sample and nothing is certified.

## 8. What I would change first

Give `derives` the shape `Recognizer` and `Grammar` already have: a theory `Derives` declared over right-hand sides, laws quantified over `(d : Derives)`, `Derives := laws`, the model a named value `backtrack : Derives` in its own file, and `Grammar`/`Recognizer` taking their model of `Derives` as a parameter. Reason: it is the one defect that is a *pattern*, not a slip. It cures at once the 4.S7/4.R6/4.R3 ill-formedness, the defined-twice collision, the never-reducing `ParsesWhatDerives`, and — by stating the operation over an `Rhs` — removes `withStart` and with it the inconsistency of 3. Everything downstream will copy whichever of the two shapes these files leave standing.