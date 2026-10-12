# 4. Static semantics

Chapter 4 of the specification, draft 0, 2026-10-12. Sources: `docs/spec/05-static-semantics.md` at
d12b554 (sections 1 to 6 and 8), `docs/principles.md`, `tests/spec/r*_*.lut`,
`src/luthier/checker.py` (read only), `record/decisions.md`. Written by Sonnet 5.5. It realizes L2
(declare, then define, then inhabit), L8 (a type is a proposition, membership is a guarantee), L3
(equality has levels and belongs to the object) and L14 (what can be written in Luthier is written
in Luthier). It states what the checker decides about a program before anything runs.

## §1 Notation

**4.S1. Symbols of this chapter.** [implemented] The notation, `D(n)`, `B(n)` and the hole are
`spec 1`'s; `Bool`, `Failures E` and `Law` are `spec 5`'s.

**4.S2. Type position and term position.** [implemented] As `spec 1 §3` defines them; the
rules below use both.

**4.S3. The dependency graph.** [implemented] The graph, theories as its strongly connected
components and branches are `spec 1 §3`'s (D-2026-10-12-z).

**4.S4. Laws and labels.** [implemented] What a law touches and what a labeled base is are
`spec 1 §3`'s.

## §2 One relation, three states

**4.S5. Everything is a type.** [implemented] Everything is a type; a value is a type with exactly
one inhabitant. `4` is `{ n : Int | n == 4 }`. `x : T` says that `x` is a refinement of `T`. The
distinction between types and values stays on the surface, because the reader needs to know what
reduces, but it is a difference in how far a name is determined, not in kind (L8).

**4.S6. The three states of a name.** [implemented] A name is in one of three states. It is
*declared* when its base is known, `x : T`, by a declaration. It is *defined* when its body is
known, by a definition in the same file or in another. It is *certified* when some of its laws
passed `test`, each with a grade of the five grades of Terms (; D-2026-10-12-y). What a certificate records is `spec 6`. Certification is about a law
applied to particular values, never about a name alone.

**4.S7. The body decides, and no marker distinguishes.** [implemented] The body says what is
defined, and its type decides how (4.R6):

- `x : T := t` with `t : T` defines `x` as the inhabitant `t`.
- `x : T := p` with `p : T -> Bool` or `p : T -> Failures E`, or `p` a `Law` over a `T`, defines
  `x` as the subtype `{ y : T | p y }`, a type: `x : U`.
- `x : U := data { ... }` defines a recursive type.
- `x : T := extern "..."` defines a value whose body the environment holds (4.R5).

**4.S8. Declared types carry laws before they are defined.** [implemented] A declared type gives
its base with its labels, and its laws are written over it before it is defined. This is how a
theory is written:

    Codec : { parse : String -> Maybe Table, render : Table -> String, eq : Table -> Table -> Bool }
    RoundTrip (c : Codec) (t : Table) : Bool :=
      match c.parse (c.render t) { nothing -> false ; just u -> c.eq t u }
    Codec := RoundTrip & Rejects

`RoundTrip` needs `Codec` to state itself and `Codec` needs `RoundTrip` to be defined: the cycle is
the theory (4.S12). A model of it is a branch:
`csv : Codec := { parse := parseTable, render := renderTable }`.

**4.S9. Concrete types and theories.** [decided D-2026-10-12-aj] A name defines a *concrete
type* or a *theory*. A concrete type is defined natively (a `data`, an exponential, a product, a
sum), with no law written by its author: the laws of its equality, where it has `==`, are the
kernel's (D-2026-10-12-ak); its values are built by its constructors (those of the `data`, the lambda, the
pair, the injections) and observed by its eliminators. A theory (Terms) carries a law, stated
with the kernel's subtype former, `{ x : T | p x }`, whether its law involves one name or more
(a strongly connected component, spec 1.S8); its values are its models. Positive doubles,
an idempotent function and a group are all theories. Amends D-2026-10-12-ai, which made the
subtype a third kind. [implemented] Today the checker tells the two apart by their form, and takes
as a theory in the sense of G1 a subtype of a labeled base, usually parameterized (`Group (A :
U)`), whose models are given as values of the labeled base.

**4.S10. A body computes; a law only checks.** [implemented] Whether laws pin down a unique
inhabitant is undecidable and is never asked. Two bodies for one meaning are two names, and their
agreement is a law to test (`spec 5`).

## §3 Reading a program

**4.S11. Order of work of the checker.** [implemented] A program is a set of acts without order
(`spec 2`). The checker reads the whole program, imports included, before it checks any
definition: (1) parse every file and collect each name with its declared type and body, and expand
aliases; (2) resolve names and build the dependency graph; (3) compute the theories; (4) check the
theories in an order compatible with the dependencies, each as a block; inside a block, first every
declared type, then every law, then every other body. Order in the file is not significant.

## §4 Theories are cycles, branches name them

**4.S12. The cycle is the theory.** [implemented] A type is an assembly of other types under laws.
The laws mention the type; the type, in its definition, names the laws; that loop is the theory,
and everything on it is defined together. A definition that mentions the theory without being on
its loop is a branch: a new entity that names the theory and depends on it one way. `csv` is a
branch of `Codec`; a function `shape (t : Table) : Int * Int` is a branch of `Table`. This closes
O7.

**4.S13. Why the cycle and not mere connection.** [implemented] Connection would fuse into one
theory two types where one only refers to the other (a law of `Codec` mentions `Table`, but
`Table` does not mention `Codec`). Direction tells a theory from its branches. Two consequences:
the dependency structure of a program is read off its names, and two theories with the same cycle
up to renaming (names, signatures, laws) are candidates for an isomorphism before any
implementation is looked at. The same mathematical object, presented with other primitives, has
another cycle (`spec 9`): the cycle belongs to the presentation.

**4.S14. A head, and the law no type claims.** [implemented] Every theory defined by laws has a
head: a type whose body names the laws. A law that no type claims defines nothing; it is a branch
over the types it mentions, and 4.R2 applies to it.

## §5 Dependence

**4.S15. Dependence in version 0.** [implemented] A law depends on a name when the name occurs
free in it, after elaboration and without unfolding definitions. A law that mentions a name
vacuously (`g x and (y == y)`) counts as depending on `y`.

**4.S16. The semantic criterion of dependence.** [proposed] To be added as laws a test can check.
A function `f` *depends on its argument* `y` when there are `x`, `y`, `y'` with `f x y` and
`f x y'` different under the equality of the result type; `f x y := g x` fails it. A law `P`
*connects* `x` and `y` when it is not a conjunction of a law on `x` and a law on `y`. `P` separates
exactly when `P x y'` and `P x' y` imply `P x y` and `P x' y'` for all `x, x', y, y'`; so `P`
connects when there is a rectangle `x, x', y, y'` where that implication fails. `Q x and R y`
depends on both and connects neither. Both criteria are existential: a test looks for a witness,
not for a counterexample, and certifies with the grade cases with a witness (D-2026-10-12-y;
`spec 6`). Declaring that a function depends on an argument, or that a law connects two
components, is stating such a law.

## §6 Well-formedness rules

Each rule names its files under `tests/spec/`: one program the checker must accept and one it must
reject, with the fragment of the error message the rejection carries in a `-- expect:` comment.
The suite is the specification applied to the interpreter (`spec 7`).

**4.R1. A declaration mentions declared names.** [implemented] Every name in `D(n)` of a
declaration exists: declared or defined. A declaration may mention types that are only declared;
that is what lets a theory's laws and its head refer to each other (L2.5).
Files: r1_declaration.accept.lut, r1_declaration.reject.lut.

**4.R2. A definition uses defined types.** [implemented] For a definition `n`, every name that
occurs in type position in its declared type or its body is defined, unless it belongs to `n`'s
own theory. In term position a declared name is allowed: a hole of a defined type is a parameter
(`sigma : Float64`, set by `luthier run --set`), and what depends on it does not reduce until it
is filled. Code over a type that is only declared, outside that type's theory, must take the type
as a parameter.
Files: r2_definition.accept.lut, r2_definition.reject.lut.

**4.R3. A predicate defines only what it touches.** [implemented] The body of a subtype over a
labeled base must touch every label; over an unlabeled base it must touch its parameter. A
predicate that touches nothing (`\ p { true }`) defines nothing. `{ eq, add, mul | Associative A
eq add }` is rejected: `mul` is a label no law touches, a semigroup juxtaposed to a bare function.
The `| true` records of the first libraries disappear.
Files: r3_connected.accept.lut, r3_dangling_label.reject.lut.

**4.R4. Only laws or recursion make a new type.** [implemented] A definition `x : U := t` makes
`x` a type with a name of its own only if `t` is a subtype with a predicate (laws) or a recursive
`data`. A body that is structural (a product, a sum, an exponential, a non-recursive `data`)
introduces a name that claims nothing and is rejected: write `x = t` (an alias, 4.R7), or write
the type where it is used, or declare `x : t` and owe it laws.
Files: r4_product_inline.accept.lut, r4_product_named.reject.lut.

**4.R5. An extern gives a value, never a type.** [implemented] Types are defined natively.
`x : T := extern "..."` is accepted when `T` is defined (4.R2 applies to externs as to any body);
`x : U := extern "..."` is rejected. `extern provisional "..."` lifts both requirements, for
working in a hurry on a type nobody has defined yet or on a Python type nobody has described: it
is accepted, recorded in the certificate under `provisional` with the names it builds on, listed
by `luthier check -v`, and never certified (`spec 6`). Every refinement in the type of an extern
is an obligation on the value it gives (2026-10-05): the predicate of a subtype, the codomain of
each arrow quantified over its domain (`neg : Float64 -> NonNegative` owes `neg x >= 0.0` for
every `x`), each component of a record or a pair, and each entry of an array (`pairI : Vec (Fin
nodes)` owes that every entry is below `nodes`); the dimensions of an array are read off its shape
and owe nothing. Under a constructor of a sum (the `Table` of a `Maybe Table`) each law of the
payload becomes `match v { just t -> L t ; _ -> true }`, and a law quantified over something whose
type depends on the payload (a row `r : Fin t.nRows`) is quantified over the base of that type with
its refinement as a precondition inside the match. A refinement deeper in a payload (a field of a
record in a sum) and one under a data type are not entered. `luthier run --checked` tests every
value an extern gives against the Bool laws of its type as it crosses, each entry of an array and
each component of a record included; a quantified law is left to `test`, and a function an extern
gives is tested when it is called (`spec 10`). In the language designed the checker does not resolve the target (4.S24).
Files: r5_extern_value.accept.lut, r5_extern_type.reject.lut.

**4.R6. The body of a declared name is an inhabitant or a predicate.** [implemented] If `x` is
declared `x : T` and later given a body, the body has type `T`, or `T -> Bool`, or
`T -> Failures E`, or is a `Law` over `T`. Any other type is an error, reported against the
declaration. The form with `Failures E` is designed (spec 5.S9); the checker accepts the other
three today.
Files: r6_predicate_body.accept.lut, r6_body_type.reject.lut.

**4.R7. An alias is written with `=` and has no state.** [implemented] `AB = A * B` makes `AB`
stand for the term on the right everywhere; the checker expands it before anything else, so an
alias is never declared, defined or certified. A name that is an alias and is also declared or
defined is an error. A generator given to an alias is the generator of the type the alias stands
for (2026-10-05): `gen FullCoords` with `FullCoords = VecOf (freeDim + 1)` draws every `VecOf 16`,
and two aliases of one type cannot both have one. A distribution that means something (a broken
graph, a complete one) is a type with a law, `{ g : DistanceGraph | not (ValidGraph g) }`, and
every value its generator gives is checked against that law; a value outside is an error that
names the generator (`spec 7`).
Files: r7_alias.accept.lut, r7_alias_defined.reject.lut.

**4.R8. `==` exists only where equality is structural.** [implemented] `==` is defined on `Int`,
`Float64`, `String`, `Unit`, `Empty`, and on products, sums, recursive `data` and subtypes built
from types that have it. Not on exponentials, and not on anything containing one. A law that
compares values of such a type takes the equality it uses as a parameter or as a component of its
theory: the observational equality of the presentation. `algebra.lut` already does so (each
structure carries its `eq`). How a type names its equality (O2) is O2 (the
setoid as base case).
Files: r8_equality_parameter.accept.lut, r8_equality_function.reject.lut.

**4.R9. Function types are contravariant in the domain and covariant in the codomain.** [implemented]
(`spec 3`). [implemented] A function `A -> B` passes where `A' -> B'` is expected when `A'`
refines `A` and `B` refines `B'`.
Files: r9_variance.accept.lut, r9_variance.reject.lut.

**4.R10. A law characterizes; a second implementation is not a law.** [decided D-2026-10-05-a]
The laws of a theory are the
mathematical properties that determine its operations, up to the equality of the presentation:
bilinearity and an orthonormal basis for an inner product; multilinearity, alternation and
`det I == 1` for a determinant. A definition of the operation written in the kernel (a sum over
the indices) is a model of those laws, certified against them like any other; an implementation of
the environment is another model. That two models agree (`Agrees`) is a corollary of the laws
characterizing the theory, useful to tighten a tolerance, and never the law itself. A theory
whose only laws compare it with a second implementation is reported as *consistent, not
characterized* (4.S19). The checker does not decide the rule: it is a rule for the one who writes
the laws, and `check -v` makes the difference visible. Two consequences, from the same discussion.
Each concept is identified with the mathematical object that best represents it (a vector space,
a ring, an inner product space, a symmetric bilinear form), and that object is the invariant of its
type: the leaf, the instance or the value is declared at the structure, so the structure's laws are
its obligations and not laws stated apart on a copy. And a law has one name: it is written once in
`lib/algebra.lut`, in its most general form, and a special case is an application of it, never a
second declaration (commutativity is `Symmetric` with result type equal to the argument type;
associativity of an operation is the law of an action of a set on itself). Structures are built by
inclusion of the ones below them; `algebra` is imported by every library that states a property.

**4.R11. A condition refines in its branch.** [decided D-2026-10-06-aa] Not implemented. In `if p x then a else b`,
where `x` is a variable of type `T` and `p x` is a `Bool`, `x` has the type `{ x : T | p x }`
inside `a` and `{ x : T | not (p x) }` inside `b`. A coercion of `x` to that refined type there
owes nothing: the condition is the check, made once. If `a` asks for `{ x : T | p x }` and the
condition is another predicate `q x`, the coercion owes `q x -> p x`, an obligation certified like
any other; usually it is a law the program already states about `q`, as `ReportsValidity` relates
`firstViolation` to `ValidGraph`. The same holds for a pattern: inside `match m { just y -> a ; ... }`,
`a` knows `m == just y`. The rule replaces the precondition that only weakens an obligation raised
in a branch (`spec 6`), and the textual discharge the interpreter does today (an obligation equal
to the condition of its branch). `refine` of `spec 5` is typable by this rule.

**4.R12. `:=` defines once; `<-` rebinds.** [implemented] Decided 2026-10-11 (D-2026-10-11-c;
blocks, defaults, named arguments and the session implemented the same day). A name bound with
`:=` is defined once, and a second definition of it is an error ("x is defined twice"). A name
bound with `<-` may be bound again with `<-`: each binding is a fresh name in the core, as in
static single assignment, and every later use means the latest (D-2026-10-10-e, L4.5). A name first bound with `:=` cannot be rebound with
`<-`. Rebinding needs an order, so `<-` is allowed in the three places `spec 2.R5` names, and is an error at the top level of a file, which is a set of acts without order
(4.S11). A default is the first binding of its parameter and the call rebinds it before the body
runs; the elaborated call, which is what is hashed and certified, carries the value the body sees.
A law of a function is quantified over a defaulted parameter, not tested at its default. Blocks
(D-2026-10-11-i; `spec 2`): a brace term with a final expression is a block, the body of a lambda
is one; a block's names are visible to the end of that block and in nested blocks; `:=` of
a name already defined in an enclosing scope is an error, not a shadowing; `<-` rebinds only
block-local `<-` names and the parameters of the enclosing definition; a `<-` whose previous
binding has no consumer is rejected in a file (`spec 2.R6`) and reported in a session (O8); actions take and
return the world, so their order is the dependency through it (`spec 10`). Three kinds of block: a
body, `main` in a file, the session.
Files: r12_block.accept.lut, r12_defined_twice.reject.lut.

**4.R13. An operator is resolved by the type, and a type names its model.** [implemented] Decided
2026-10-11 (D-2026-10-11-j); implemented the same day: resolution by the argument types, and a
second meaning of an operator on the same types refused. The operators on the values of a type are
those of the model the type names: `i : Int` adds with the ring of `Int`, `j : Z7` with `ringZ7`.
A carrier with two models is two types (`Int` as a ring and as the max-plus semiring; `Float64`
under two tolerances), and the conversion between them is explicit, `forget` to the carrier and a
constructor back, never silent. The operators of a wider model apply to a narrower type only
through a homomorphism stated and certified as a law: a value of `Z7` uses `Int`'s `+` after
`forget`, and the law that relates the two is `mod 7` being a ring homomorphism. Where a theory
does not fix the role of an operator (a function over a bare `Monoid` applied at `Int`, which
carries two), the model is named in the call. The subtype is the wrong relation for a quotient:
`examples/z7ring.lut` is rewritten with `Z7` as its own type.
Files: r13_operator_by_type.accept.lut, r13_two_models.reject.lut.

## §7 Statements added to the rules

The checks the old chapter added to rules 4.R2, 4.R3, 4.R12 and 4.R13 as further programs.

**4.S17. No loose functions.** [decided D-2026-10-07-e] Added to 4.R2 and 4.R4 on 2026-10-07; not
implemented. A structural type with no laws, an exponential `A -> B`, a product or a sum, is a
*base* and not a defined type for 4.R2. A value is defined at a type that has a name and laws, at
a `data` or at a primitive; a top-level definition at a bare exponential is a loose function, and
there are none: a function is a value of a defined function type, a theory (Terms). A helper
either gets its recursion as its laws or waits for local definitions (`spec 2`). The same holds
for 4.R4: a lawless `A -> B` is a base, not a type a value is written at. The libraries do not
comply yet (`exp : Float64 -> Float64` in `real.lut`, the helpers of `array.lut`): `check -v` is
to report loose functions first, as it reports *consistent, not characterized*, and the rule
rejects once local definitions exist and the certificates are reissued. Files are to be written
with the implementation: reject `s17_loose_function.reject.lut`, accept `s17_defined_function.accept.lut`
(neither exists).

**4.S18. R2 and R3 programs beyond the pair.** [implemented] Two further programs belong to the
rules above: `r2_unclaimed_laws.reject.lut` (a law no type claims, 4.S14, is a branch and 4.R2
applies to it) and `r3_true_predicate.reject.lut` (a predicate that touches nothing, 4.R3). The
programs `r12_rebind_defined.reject.lut`, `r12_unused_rebinding.reject.lut`,
`r12_toplevel_arrow.reject.lut`, `r12_defaults.accept.lut` and `r12_named_unknown.reject.lut` do
the same for 4.R12, `r4_data_nonrecursive.reject.lut` and `r4_recursive_data.accept.lut` for 4.R4,
and `r5_extern_provisional.accept.lut` and `r5_extern_over_declared.reject.lut` for 4.R5.

## §8 Reports that do not reject

**4.S19. What `luthier check -v` reports.** [implemented] Without rejecting, `luthier check -v`
reports (2026-10-05: also the axioms, `spec 6`): every `provisional` extern and what it builds on
(4.R5); for each concrete type with laws, the table of observers against constructors, and the
cells with no law: *sufficient completeness* (Guttag, 1977). A full table says everything
observable about every constructed value. An extensionality law (two values are equal when every
observer agrees on them) turns "same observations" into "same value"; holes that the entry of
`luthier run` depends on.

**4.S20. Consistent, not characterized.** [decided D-2026-10-05-b] Not implemented. For each operation with laws, `check -v` reports whether they characterize it
(4.R10) or only compare it with another implementation. Version 0 can only tell the two apart by
name: a law whose body applies the operation and another definition to the same arguments and
compares the results is a comparison. Characterization proper is a judgement the author makes.

## §9 The rules as a theory

**4.S21. R1 to R13 as the laws of `WellFormed`.** [proposed] L14 asks for the rules in Luthier.
Rules 4.R1 to 4.R13 are the laws of a theory `WellFormed : Program -> Failures E`, over the
`Program` data of `spec 3`, to be written in `lib/program.lut` (not yet present), each law one
rule and its accept and reject programs its cases. Until it exists the checker in
`src/luthier/checker.py` is the specimen, and the suite is its certificate (`spec 7`).

## §10 Example

**4.S22. A theory, its branches and the rules applied.** [implemented]

```
-- a concrete type, defined natively: a table is a function from a column and a row to a cell
Cell = < int : Int | real : Float64 | text : String >
Table = { columns : List String, nRows : Int, cell : String -> Int -> Maybe Cell }

-- a theory, declared, its laws, then defined: the cycle Codec -> laws -> Codec is the theory
Codec : { parse : String -> Maybe Table, render : Table -> String, eq : Table -> Table -> Bool }
RoundTrip (c : Codec) (t : Table) : Bool :=
  match c.parse (c.render t) { nothing -> false ; just u -> c.eq t u }
Rejects (c : Codec) (b : BrokenText) : Bool := match c.parse b { nothing -> true ; just t -> false }
Codec := RoundTrip & Rejects

-- a model: a value of the theory, built from externs over defined types (4.R5); a branch of Codec
csv : Codec := { parse := extern "python:luthier.tables.parse",
                 render := extern "python:luthier.tables.render",
                 eq := sameTable }
test csv with 200
```

`Table` here is an alias (4.R4: a product with no laws is not a new type). If tables had
invariants (the cells of a column all of one kind, rows below `nRows`), `Table` would be declared
over this base and defined by them. `Codec` carries its equality as a component (4.R8), because a
`Table` contains a function and has no `==`.


## §11 What the checker infers and what it does not open

**4.S23. Implicit arguments from the expected type.** [decided D-2026-10-12-ab] Implicit arguments
are inferred from the type the context expects as well as from the types of the explicit arguments,
since `extern` and `axiom`, as names of core, take their type from where they are used.

**4.S24. The checker does not open an extern's file.** [decided D-2026-10-12-ac] 4.R5 is checked on
the declared type alone: the checker records the target of an extern and its type, and does not
resolve it (`spec 3 §8`). Today it imports the host module and rejects a target it cannot resolve.

## Open

- O2, which 4.R8 rests on.
- O9 (4.S7, 4.R2, 4.R5).
- O8, the session as a block (4.R12).
