# The grammar of Luthier

Rewritten on 2026-10-04 from the Spanish draft of 2026-09-29 (`02-gramatica.md`, in the history).
This is the concrete syntax the parser of the interpreter accepts (`src/luthier/parser.py`). The
kernel it translates into is `04-kernel.md`; what makes a parsed program well formed is
`05-static-semantics.md`.

Notation: EBNF, `::=` defines, `|` separates alternatives, `[ ]` is optional, `{ }` repeats zero
or more times, and literals of the language are between double quotes.

## 1. Lexical

    name     ::= letter { letter | digit | "_" | "'" } { "." letter { letter | digit | "_" | "'" } }
    number   ::= digit { digit } [ "." digit { digit } ] [ ("e" | "E") [ "+" | "-" ] digit { digit } ]
    string   ::= '"' { character } '"'
    comment  ::= "--" up to the end of the line

A dotted name `m.f` is one token; it is a qualified name or a projection, resolved by the checker
(section 6). Names that start with a capital are types and laws by convention, not by rule.

Reserved words: `data`, `match`, `extern`, `provisional`, `test`, `with`, `exhaustive`, `gen`,
`import`, `forget`, `U`, `operator`, `if`, `then`, `else`. `and`, `or` and `mod` are ordinary names
written infix; `Bool`, `Int`, `R`, `String`, `Unit`, `Empty`, `Maybe`, `List`, `Nat`, `Fin` are
definitions of `core.lut`.

Layout: an act starts at column 0, and an indented line continues the act above it. Inside
`( )`, `[ ]`, `< >` and the braces of `match` and of a lambda, line breaks are ignored; inside the
braces of a record type, a line break separates components.

## 2. Acts

    program     ::= { act }
    act         ::= declaration | definition | alias | directive

    declaration ::= name { binder } ":" term
    definition  ::= name { binder } [ ":" term ] ":=" body { clause }
    alias       ::= name { binder } "=" term
    body        ::= term
                  | "data" "{" { name ":" term [ ";" ] } "}"
                  | "extern" [ "provisional" ] string
    binder      ::= "(" name { name } ":" term ")"
    clause      ::= "|" pattern { "," pattern } ":=" term

    directive   ::= "import" string [ "as" name ]
                  | "test" name [ "with" number | "exhaustive" ] [ "size" number ]
                  | "gen" name ":=" ( term | "extern" string )
                  | "operator" op ":=" term

Binders before the colon are parameters: `f (x : A) (y : B) : C := t` is
`f : (x : A) -> (y : B) -> C := \ x { \ y { t } }`, and `(x y : A)` is `(x : A) (y : A)`.
Clauses under a header with parameters are a `match` on the tuple of the parameters. A name may
be declared in one act and defined in another, in the same file or another; what the definition's
body means depends on its type (`05` R6). An alias with binders is a function on types:
`Maybe (A : U) = < nothing : Unit | just : A >`.

## 3. Terms

Precedence, from the loosest to the tightest:

    &   ->   or   and   == /= < <= > >=   + -   * / mod   application   .field

`&` and `->` associate to the right, the others to the left. `->` is the function type when its
left side is a type and implication when it is a `Bool`; `*` is the product type or multiplication,
`+` the sum type or addition, by the type of the left operand; `&` is the conjunction of laws.
An `operator` directive gives `+`, `-`, `*`, `/` a meaning on the argument types of a function.

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
             | "<" name ":" term { "|" name ":" term } ">"                                -- sum, n-ary
             | "[" [ term { "," term } ] "]"                                              -- list
             | "\" lparam { lparam } "{" term "}"                                         -- lambda
             | "match" term "{" { pattern "->" term [ ";" ] } "}"
             | "if" term "then" term "else" term
             | "extern" [ "provisional" ] string
             | "forget" atom
             | atom "." name                                                              -- projection

    sep     ::= "," | ";" | line break
    lparam  ::= name | "(" name { name } ":" term ")" | "(" pattern { "," pattern } ")"
    pattern ::= "_" | name { patom } | patom
    patom   ::= name | number | string | "(" pattern { "," pattern } ")"

A pattern `name` is a constructor of the scrutinee's data type or a label of its sum if it names
one, and a variable otherwise. A label of a sum is an injection: `circle 2.0` against
`< circle : R | square : R >`, `true` against `Bool`. A union `< ... >` written as the argument of
an application needs parentheses, because `<` after a term is a comparison.

## 4. Translations into the kernel

`04 §5` gives the table: binders and clauses, `if`, `and`/`or`/implication, list literals, record
values and projections, labeled products and sums, `Bool` and `Maybe`, tuple patterns in a lambda.
Each translation produces kernel terms; a surface form that needed a new kernel construct would not
be sugar.

## 5. What the parser leaves to the checker

The parser does not decide what `->`, `*` and `+` are, nor whether a name in a pattern is a
constructor, a label or a variable, nor what a dotted name refers to. It produces the acts as
written, and the checker reads the whole file before it checks any of them (`05 §2`).

## 6. Dotted names

`e.position` is the component `position` of a value whose type names its components; it elaborates
to a one-branch `match` on the type's component pattern, and works after a parenthesis,
`(f x).field`, and through refinements (`{ s : Scene | p }` has the components of `Scene`). A module
imported `as m` is a record whose components are its definitions, so `m.f` is the same dot. The
resolution: the whole name as a qualified name first; otherwise the longest prefix that is a
variable or a definition, and one projection per remaining segment. In a dependent product the type
of a later component may mention earlier ones, and the type of `d.m` replaces them by projections
of `d`.

## 7. Open

- Quote and unquote: the syntax of a term as a value of `Term`.
- Local definitions in a block, `{ x := t ; u }`.
- A saved evaluation, a quoted term together with its value.
