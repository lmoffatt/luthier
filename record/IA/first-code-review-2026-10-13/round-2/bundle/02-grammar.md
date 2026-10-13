# 2. Grammar

Chapter 2 of the specification of Luthier, draft 0, 2026-10-12, written by Claude Sonnet 5.5 from
`docs/spec/02-grammar.md` of 2026-10-11 (the file this one replaces), `docs/spec/04-kernel.md` §5,
`docs/spec/08-tests.md` §12 and `src/luthier/parser.py` and `lexer.py`, all at commit 3445ad8.
It realizes L7 (programs are data, the core is small), L2.3 (the elaborated form records which
kind a definition is) and L14 (what can be written in Luthier is written in Luthier). The kernel
it translates into is `spec 3`; what makes a parsed program well formed is `spec 4`; the notation
of the specification is `spec 1`. The notation of the EBNF here: `::=` defines, `|` separates
alternatives, `[ ]` is optional, `{ }` repeats zero or more times, literals are in double quotes,
`--` starts a comment inside a production.

## §1 Lexical

**2.S1. Tokens.** [implemented] A name, a number, a string and a comment are:

    name     ::= letter { letter | digit | "_" | "'" } { "." letter { letter | digit | "_" | "'" } }
    number   ::= digit { digit } [ "." digit { digit } ] [ ("e" | "E") [ "+" | "-" ] digit { digit } ]
    string   ::= '"' { character } '"'
    comment  ::= "--" up to the end of the line

A dotted name `m.f` is one token, a qualified name or a projection that the checker resolves
(spec 2.S14). Names that start with a capital are types and laws by convention, not by rule.
[proposed] Inside a string, `\"`, `\\` and `\n` stand for a quote, a backslash and a line break, so
that a law can spell a text of several lines (`grammar.lth`).

**2.S2. Reserved words.** [implemented] The reserved words are `data`, `match`, `extern`,
`provisional`, `test`, `with`, `exhaustive`, `import`, `forget`, `U`, `operator`, `if`, `then`,
`else`, `cite`, `let`, `in`, `primitive` and `axiom`. The last two bodies are allowed only in
`core.lut` and the libraries of the distribution (spec 11). `as`, `checked`, `size`, `sampled`,
`under`, `where` and `profile` are ordinary names that act as keywords in their position. Here `gen` goes from the language (D-2026-10-06-ac, spec 2.S19); the parser still reads
it today. `and`, `or` and `mod` are ordinary names written infix; `Bool`, `Int`, `Float64`,
`String`, `Unit`, `Empty`, `Maybe`, `List`, `Nat` and `Fin` are definitions of `core.lut`, not
words of the grammar. Replaced: 2.S21.

**2.S3. The arrow `<-`.** [implemented] `<-` is one token (D-2026-10-11-c): `a<-1` is a binding,
and a comparison with a negative number needs a space, `a < -1`.

**2.S4. Layout.** [implemented] An act starts at column 0, and an indented line continues the act
above it. Inside `( )`, `[ ]`, `< >` and the braces of `match`, line breaks are ignored. Inside
the braces of a record type, a record value and a block (a lambda's body included) a line break
separates items and `;` is equivalent to it, so several items may share a line
(D-2026-10-11-k). A line indented deeper than the block's first item continues the item above it,
and so does a line that cannot start an item: one beginning with `else`, `then`, `in` or an
infix operator.

## §2 Acts

**2.S5. Acts.** [implemented]

    program     ::= { act }
    act         ::= declaration | definition | alias | directive

    declaration ::= name { binder } ":" term
    definition  ::= name { binder } [ ":" term ] ":=" body { clause }
    alias       ::= name { binder } "=" term
    body        ::= term
                  | "data" "{" { name ":" term [ ";" ] } "}"
                  | "extern" [ "provisional" ] string
                  | "primitive" string | "axiom" string          -- core.lut and lib/ only
    binder      ::= "(" name { name } ":" term [ "<-" term ] ")"            -- with a default
    clause      ::= "|" pattern { "," pattern } ":=" term

Binders before the colon are parameters: `f (x : A) (y : B) : C := t` is
`f : (x : A) -> (y : B) -> C := \ x { \ y { t } }`, and `(x y : A)` is `(x : A) (y : A)`.
Clauses under a header with parameters are a `match` on the tuple of the parameters.
[decided D-2026-10-13-o] Two changes to the productions above. A bare term is an act, `act ::= ... | term`: a datum
the module keeps, such as a `test` line or a citation (2.S21 makes `test` and `cite` functions);
which terms may stand there is the checker's, and no `<-` does (2.R5). A trailing separator is
allowed after the last constructor of a `data`, the last arm of a `match` and the last item of a
record or a block. A name may be
declared in one act and defined in another, in the same file or another; what the body of a
definition means depends on its type (spec 4). An alias with binders is a function on types:
`Maybe (A : U) = < nothing : Unit | just : A >`.

**2.S6. Directives.** [implemented] In `v0.1-final` the directives other than `test` were as below; the language designed keeps only `operator` as an act of its own, `import` takes the form of 12.S22 and `cite` is a function (2.S21). Replaced: 2.S21.

    directive   ::= "import" string [ "as" name ]
                  | "operator" op ":=" term
                  | "cite" name term [ "checked" ( "human" | "ai+human" | "none" ) ]   -- D-2026-10-11-f

`cite` records a `proved` certificate by citation (L9.7, O10). What `import` makes travel is
`spec 12`. The directive `test` is spec 2.S19.

**2.S7. Defaults and arguments by name.** [implemented] A parameter written `(tol : T <- d)` has
the default `d`. It is filled once every parameter without a default is given, and a default may
mention the parameters before it. An argument by name, `f a (tol <- v)`, goes to its parameter's
position; a function value has no names and no defaults (D-2026-10-11-c).

**2.R1. Named argument.** [implemented] An argument by name must name a parameter of the function,
and a default is used when its parameter is not given.
Files: r12_defaults.accept.lut, r12_named_unknown.reject.lut.

## §3 Terms

**2.S8. Precedence.** [implemented] From the loosest to the tightest:

    &   ->   or   and   == /= < <= > >=   + -   * / mod   application   .field

`&` and `->` associate to the right, the others to the left. `->` is the function type when its
left side is a type and implication when it is a `Bool`; `*` is the product type or
multiplication, `+` the sum type or addition, by the type of the left operand; `&` is the
conjunction of laws (spec 5). An `operator` directive gives `+`, `-`, `*`, `/` a meaning on the
argument types of a function, and a type names its model (D-2026-10-11-j): `the model a type names gives its operators (`spec 4.R13`), as the ring of `Z7`.

**2.R2. A type names its model.** [implemented] An operator is resolved by the type of its
operands; two models of a carrier are two types (`spec 4.R13`), and a type with two
models for one operator is rejected.
Files: r13_operator_by_type.accept.lut, r13_two_models.reject.lut.

**2.S9. Terms.** [implemented]

    term   ::= term op term
             | term atom                                      -- application
             | atom

    atom   ::= name | number | string | "U"
             | "(" term ")"
             | "(" term "," term { "," term } ")"            -- a tuple, associating to the right
             | "(" name { name } ":" term ")" "->" term       -- dependent function
             | "(" name { name } ":" term ")" "*" term        -- dependent product
             | "(" name ":" term ")" "*" "(" name ":" term ")"     -- product with both positions named
             | "(" name ":" term ")" "+" "(" name ":" term ")"     -- sum with named alternatives
             | "{" name { name } ":" term { sep name { name } ":" term } "}"            -- labeled product
             | "{" name { name } ":" term { sep name { name } ":" term } "|" term "}"   -- subtype with labels
             | "{" pattern ":" term "|" term "}"                                          -- subtype
             | "{" name ":=" term { sep name ":=" term } "}"                            -- record value
             | "{" { item sep } term "}"                                                  -- block (spec 2 §8)
             | "<" name ":" term { "|" name ":" term } ">"                                -- sum, n-ary
             | "[" [ term { "," term } ] "]"                                              -- list
             | "\" lparam { lparam } "{" { item sep } term "}"                            -- lambda; its body is a block
             | "match" term "{" { pattern "->" term [ ";" ] } "}"
             | "(" name "<-" term ")"                                                     -- named argument
             | "if" term "then" term [ "else" term ]                                     -- one arm: a Maybe or a reason
             | "let" pattern "=" term "in" term                                           -- retired (2.S21)
             | "-" term                                                                   -- negation; see below
             | "extern" [ "provisional" ] string
             | "forget" atom
             | atom "." name                                                              -- projection

    sep     ::= "," | ";" | line break
    item    ::= name ":=" term | name "<-" term                                           -- in a block
    lparam  ::= name | "(" name { name } ":" term ")" | "(" pattern { "," pattern } ")"
    pattern ::= "_" | name { patom } | patom
    patom   ::= name | number | string | "(" pattern { "," pattern } ")"

[decided D-2026-10-13-o] In the language designed: `let` is retired, replaced by blocks
(2.S21). Negation is not an atom but a level of its own, above application and below `*`, so
`-f x` is `-(f x)` and `f -x` is `f - x` (2.S15). A single labeled field with a law,
`{ x : T | p }`, is the subtype with the pattern `x`; the labeled forms take two or more names,
`{ x : A, y : B }` or `{ x y : A }`, with an optional law; so each text has one tree. A field may
carry several names, `{ x y : A, z : B }`. `quote` is a keyword (2.S21) and `eval` a name of core, so
`eval A t` is an application (2.S20).

**2.S10. Patterns.** [implemented] A pattern `name` is a constructor of the scrutinee's data type
or a label of its sum if it names one, and a variable otherwise. A label of a sum is an injection:
`circle 2.0` against `< circle : Float64 | square : Float64 >`, `true` against `Bool`. A union
`< ... >` written as the argument of an application needs parentheses, because `<` after a term is
a comparison.

**2.S11. The dangling else.** [implemented] An `else` belongs to the nearest `if` without one:
in `if a then if b then x else y` the `else` is the inner `if`'s (D-2026-10-11-b).

## §4 Translations into the kernel

**2.S12. The table.** [implemented] Each surface form is sugar: it translates into kernel terms
(spec 3), and a form that needed a new kernel construct would not be sugar. This table is the
translation; spec 3 cites it.

| surface | kernel |
|---|---|
| `f (x : A) (y : B) : C := t` | `f : (x : A) -> (y : B) -> C := \ x { \ y { t } }` |
| `(x y : A)` in a binder | `(x : A) (y : A)` |
| clauses `\| p, q := t` under a header with parameters | a `match` on the tuple of parameters |
| `if c then a else b` | `match c { true -> a ; false -> b }`; `c : Failures E` is first projected by `holds` (spec 5) |
| `if c then a`, `c : Bool` | `if c then just a else nothing`, of type `Maybe A` (D-2026-10-11-b) |
| `if c then a`, `c : Failures E` | `match c { nil -> ok a ; cons e es -> failed e }`, the reason form; a demand for `Maybe A` forgets `e` |
| `a and b`, `a or b`, `p -> q` with `p : Bool` | `and a b`, `or a b`, `implies p q` |
| `[a, b, c]` | `cons a (cons b (cons c nil))`, element type from the expected type |
| `{ x := a, y := b }` | `(a, b)`, checked against a type with components `x`, `y` |
| `e.y` | a one-branch `match` on the component pattern of the type of `e` |
| `m.f`, `m` an imported module | the definition `f` of module `m`; a module is a record of its definitions (spec 12) |
| `{ x : A, y : B }` | `(x : A) * B`, with the last component also named |
| `< x : A \| y : B >` | `(x : A) + (y : B)` |
| `Bool` | `< true : Unit \| false : Unit >`, in `core.lut` |
| `Maybe A` | `< nothing : Unit \| just : A >` |
| `Failures E` | `List E`, the failures of a check, empty when it holds (spec 5) |
| `f a (tol <- v)`, `f` with `(tol : T <- d)` | `f a v`: arguments by name are placed in their parameter's position, a parameter not given takes its default `d` once every parameter without a default is given (D-2026-10-11-c) |
| `y <- e` in a block | a fresh name `yk := e`, `k` the count of bindings of `y` so far, and every later `y` means `yk` (spec 2.S17) |
| `{ i1 ; ... ; in ; e }`, a block | the definitions of its items with fresh names, and `e`; a sub-DAG with one output (D-2026-10-11-i) |
| `w1 <- act w0 ...`, an action in a block | an ordinary binding: actions take and return the world (spec 10) |
| `\ (x, y) { t }` | `\ p { match p { (x, y) -> t } }` |
| `let p = e in body` | `match e { p -> body }` |
| `-x` | `0 - x` on an `Int`, `0.0 - x` on a `Float64` |

## §5 What the parser leaves to the checker

**2.S13. The parser decides little.** [implemented] The parser does not decide what `->`, `*` and
`+` are, nor whether a name in a pattern is a constructor, a label or a variable, nor what a
dotted name refers to. It produces the acts as written, and the checker reads the whole file
before it checks any of them (spec 4).

## §6 Dotted names

**2.S14. Projection and qualification.** [implemented] `e.position` is the component `position` of
a value whose type names its components; it elaborates to a one-branch `match` on the type's
component pattern, works after a parenthesis, `(f x).field`, and through refinements (`{ s : Scene
| p }` has the components of `Scene`). A module imported `as m` is a record of its definitions, so
`m.f` is the same dot. The resolution takes the whole name as a qualified name first; otherwise
the longest prefix that is a variable or a definition, and one projection per remaining segment.
In a dependent product the type of a later component may mention earlier ones, and the type of
`d.m` replaces them by projections of `d`.

## §7 Sugar added on 2026-10-05

**2.S15. `let` and negation.** [implemented] `let p = e in body` is `match e { p -> body }`, the
pattern a name or a tuple; retired by D-2026-10-13-o, a block does it. `-x` is negation, an error on a type other than `Int` or `Float64`. It
binds looser than application, so `-f x` is `-(f x)`, and as an argument it needs parentheses,
`f (-x)`, since `f -x` is `f - x`. Replaced: 2.S21.

**2.S16. Implicit parameters.** [implemented] `{A B : U}` before the other parameters of a
definition makes them implicit. Where the definition is applied they are inferred by matching the
types of the explicit arguments against those of the parameters (first order, through aliases and
refinements). An argument whose type is not inferable alone, an unannotated lambda, is checked once
the others have solved the unknowns. When the first argument of an application is itself a type,
the implicit parameters are taken as given explicitly. An implicit parameter is a type or a type
operator; one that no argument determines is an error that asks for it explicitly.

## §8 Blocks and the session

**2.S17. Blocks.** [implemented] A brace term whose last item is a bare expression is a block, and
that expression is its value; a brace term with no final expression is a record value
(D-2026-10-11-i). The body of a lambda and the body of a definition written with braces are
blocks. The items of a block are `x := t` (once), `x <- t` (bind or rebind) and an action with its
result bound, `w1 <- print w0 "x"`. Translation: each item becomes a definition with a fresh name
(spec 2.S12), so after it the block is a sub-DAG with one output, dependencies give the only
order, and items that do not refer to each other commute (L4, L9). Three kinds of block and no
other: the body of a definition or lambda; a block named `main` in a file, the script; the
session. A file is never a block.

**2.R3. A name is defined once.** [implemented] `:=` defines a name once. A name bound in a block
is visible from its binding to the end of that block and inside blocks nested in it. `:=` of a name
defined in an enclosing scope or at the top level is an error, not a shadowing.
Files: r12_block.accept.lut, r12_defined_twice.reject.lut.

**2.R4. What `<-` may rebind.** [implemented] `<-` may rebind only a name first bound with `<-` in
the same block, or a parameter of the enclosing definition, whose default is its first binding
(D-2026-10-11-c). A name bound with `:=` cannot be rebound.
Files: r12_block.accept.lut, r12_rebind_defined.reject.lut.

**2.R5. `<-` needs an order.** [implemented] `<-` exists only in a block, in a parameter's default
and in a named argument; at the top level of a file, where acts have no order, it is an error.
Files: r12_block.accept.lut, r12_toplevel_arrow.reject.lut.

**2.R6. Unused binding.** [implemented] A `<-` whose previous binding of the same name has no
consumer is an error in a file ("unused binding"), and is allowed and reported in a session.
Files: r12_block.accept.lut, r12_unused_rebinding.reject.lut.

**2.S18. The session.** [implemented] `luthier session [files]` (2026-10-11) types a block one item
at a time: `the items are those of a block (§8) and a bare term, which `spec 12` says how the command prints, and an unused rebinding is reported. Each line re-evaluates the block so far; what
a line re-evaluates and the memo between lines are `spec 8` and O8. The world as the implicit `w`
of the session block waits for actions (spec 10). In a session `w` is the world of the session
block; in a file, of `main`.

## §9 Tests, profiles and the removal of `gen`

**2.S19. The test directive and the profile.** [decided D-2026-10-06-ac] The grammar the model
wrote for D-2026-10-06-ab (old `08 §12`). The directive `test`
extends, the act `profile` is new, and the act `gen` and its word are removed: Replaced: 2.S21.

    directive ::= "test" name [ "with" number | "exhaustive" ] [ "sampled" name ] [ "size" number ]
                  [ "under" name ] [ "where" "{" binding { "," binding } "}" ]
    act       ::= ... | "profile" name ":=" "{" binding { "," binding } "}"
    binding   ::= name ":=" term

Here the name after `sampled` is a metric and the name after `under` a profile; their meaning is
`spec 7`. This syntax is replaced by `test` as a function with named arguments and a profile as a
record value (D-2026-10-12-ab, 2.S21), so no `profile` act remains. The parser today reads `test name [ "with" number | "exhaustive" ] [ "size" number ]` and
still reads `gen name ":=" ( term | "extern" string )`.

## §10 Terms as data

**2.S20. Quote and unquote.** [decided D-2026-10-12-ah] A term as a value of the type `Term` (D-2026-10-12-x, L7.4):
one candidate syntax,

    atom ::= ... | "quote" "{" term "}"          -- the term, as a value of Term

and `eval A t`, the value of the quoted `t` at type `A`, is an application of the core name `eval`,
not a form of the grammar (D-2026-10-13-o; `quote` is a keyword, `eval` is not, since only
`quote` must keep its argument unevaluated).

The type `Term` itself, and `Program`, belong to `spec 3`. A theory that states this grammar in
Luthier is `src/luthier/lib/grammar.lth` (L14), draft 2 written 2026-10-13. A saved evaluation, a quoted term together with
its value, stays open (spec 8).


## §11 The keywords, and what becomes Luthier

**2.S21. Keywords and names.** [decided D-2026-10-12-ab] The keywords are `W` (D-2026-10-13-b), `data`, `match`, `if`,
`then`, `else`, `U`, `operator` and `quote` (D-2026-10-13-o): `operator` binds a symbol, which no
function can take as an argument, and `quote` captures a term unevaluated. Everything else is a core or library
name: `let` and `in` give way to blocks (§8); `forget` is a function of core; `extern`,
`primitive` and `axiom` are names of core whose application the checker recognizes (`spec 3 §8`),
with `provisional` a named argument of `extern`; `test` and `cite` are functions whose options
(`with`, `exhaustive`, `size`, `sampled`, `under`, `where`, `profile`, `checked`) are named
arguments and values (`spec 7`, `spec 6`); `import` gives a module value (`spec
12.S22`). Keyword or not, what each construct means is stated in Luthier (L14.5). The parser reads the
older forms today, and the statements above that describe them say so.

## Open

- O8: the session (O8), the memo between its items (spec 2.S18).
- O9 (L2.3).
- O10: the syntax of `cite` with the bib key and who checked (spec 2.S6).
- O11: the kernel's theory stated in Luthier, which a statement of this grammar would join.
