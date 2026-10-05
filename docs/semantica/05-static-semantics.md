# Static semantics: states, objects, rules, certification

Draft 1, 2026-10-04. What the checker decides about a program before anything runs, on the
kernel of `04-kernel.md`. It settles what the voice notes of that day asked for (10:28, 12:16,
12:17, 12:30): that declaring a type and defining it be two different acts, that a definition
verify something, that the objects of a program be the cycles of names their laws close, and
that a name claim something. Where a point stayed open it is listed in section 10.

Draft 0 of this document, of the same day, was `04-static-semantics.md`; draft 1 replaces it.
The changes: types are always defined natively and an extern only gives values (so the opaque
carrier and the style of holes filled by another file are gone, and with them the rule that
filled a cycle per file); objects are cycles of the dependency graph, not connected components
of a hypergraph; a name has three states, and certification is graded and is about
applications, not names.

## 0. Notation

Every symbol used in this document.

- `x : T`, `x : T := t`, `x = t`, `U`, `≡`: as in `04 §0`. A *hole* is a declared name with no body.
- `Bool` is `< true : Unit | false : Unit >`; `Law` is the type of a conjunction of quantified
  Bool-valued laws (`04 §3`).
- A *name* is a top-level act's name, qualified by its module prefix (`03 §2`).
- `D(n)` is the set of names that occur in the declared type of `n`; `B(n)` the set that occur
  in its body. Occurrence is syntactic, after elaboration and after expanding aliases;
  constructors and labels stand for their type; a projection `e.f` counts the names in `e`.
- An occurrence is *in type position* when the occurring term has type `U` or is a type
  operator: the declared type of a definition, the annotation of a binder, the base of a
  subtype, the parts of a product, sum or exponential, the arguments of a type operator. Every
  other occurrence is *in term position*.
- The *dependency graph* is directed: the names are its nodes and `n -> m` is an edge whenever
  `m ∈ D(n) ∪ B(n)`.
- An *object* is a strongly connected component of the dependency graph: a maximal set of
  names each reachable from each other. A name no cycle passes through is an object of one.
- A *branch* of an object `O` is a name outside `O` with an edge into `O`.
- A *law* is a Bool- or Law-valued definition, or one conjunct (split at `&`) of the predicate
  of a subtype. A law *touches* the names and labels that occur free in it.
- A *labeled base* is a product with named components, `{ x : A, y : B }`; its *labels* are the
  component names.

## 1. One relation, three states

Everything is a type; a value is a type with exactly one inhabitant. `4` is
`{ n : Int | n == 4 }`. `x : T` says that `x` is a refinement of `T`. The distinction between
types and values stays on the surface, because the reader needs to know what reduces, but it
is a difference in how far a name is determined, not in kind.

A name is in one of three states:

| state | what is known | how it is reached |
|---|---|---|
| declared | its base: `x : T` | a declaration |
| defined | its body | a definition, in the same file or another |
| certified | some of its laws passed `test`, each with a grade (section 7) | `luthier test` |

The body says what is defined, and its type decides how; no marker distinguishes the cases
(rule R6):

- `x : T := t` with `t : T` defines `x` as the inhabitant `t`.
- `x : T := p` with `p : T -> Bool`, or `p` a `Law` over a `T`, defines `x` as the subtype
  `{ y : T | p y }`, a type: `x : U`.
- `x : U := data { ... }` defines a recursive type.
- `x : T := extern "..."` defines a value whose body the environment holds (R5).

A declared type gives its base with its labels, and its laws are written over it before it is
defined. This is how an object is written:

    Codec : { parse : String -> Maybe Table, render : Table -> String, eq : Table -> Table -> Bool }
    RoundTrip (c : Codec) (t : Table) : Bool :=
      match c.parse (c.render t) { nothing -> false ; just u -> c.eq t u }
    Codec := RoundTrip & Rejects

`RoundTrip` needs `Codec` to state itself and `Codec` needs `RoundTrip` to be defined: the cycle
is the object (section 3). A value of the object is a branch:
`csv : Codec := { parse := parseTable, render := renderTable }`.

Two kinds of object, distinguished by the form of their definition and not by a marker:

- a *concrete type* is defined natively (a `data`, an exponential, a product, a sum, a subtype of
  those); its values are built by its constructors (the constructors of the `data`, the lambda,
  the pair, the injections) and observed by its eliminators;
- a *theory* is a subtype of a labeled base, usually parameterized (`Group (A : U)`); it has no
  constructors of its own: its values are its models, given as values of the labeled base.

A body computes; a law only checks. Whether laws pin down a unique inhabitant is undecidable
and is never asked. Two bodies for one meaning are two names, and their agreement is a law to test (`04 §6`).

## 2. Reading a program

A program is a set of acts without order (`00 §1`). The checker reads the whole program,
imports included, before it checks any definition:

1. parse every file and collect each name with its declared type and body; expand aliases;
2. resolve names and build the dependency graph;
3. compute the objects;
4. check the objects in an order compatible with the dependencies, each object as a block;
   inside a block, first every declared type, then every law, then every other body.

Order in the file is not significant.

## 3. Objects are cycles, branches name them

A type is an assembly of other types under laws. The laws mention the type; the type, in its
definition, names the laws; that loop is the object, and everything on it is defined together
(voice notes of 12:16 and 12:30). A definition that mentions the object without being on its
loop is a branch: a new entity that names the object and depends on it one way. `csv` is a
branch of `Codec`; a function `shape (t : Table) : Int * Int` is a branch of `Table`.

Why the cycle and not mere connection: connection would fuse into one object two types where
one only refers to the other (a law of `Codec` mentions `Table`, but `Table` does not mention
`Codec`). Direction tells an object from its branches. Two consequences: the dependency
structure of a program is read off its names, and two objects with the same cycle up to
renaming (names, signatures, laws) are candidates for an isomorphism before any implementation
is looked at. The same mathematical object, presented with other primitives, has another cycle
(section 9): the cycle belongs to the presentation.

Every object that is defined by laws has a head: a type whose body names the laws. A law that
no type claims defines nothing; it is a branch over the types it mentions, and R2 applies to it.

## 4. Dependence

In version 0, a law depends on a name when the name occurs free in it, after elaboration and
without unfolding definitions. A law that mentions a name vacuously (`g x and (y == y)`) counts as
depending on `y`.

The semantic criterion, to be added as laws a test can check (section 10):

- *`f` depends on its argument `y`* when there are `x`, `y`, `y'` with `f x y` and `f x y'` different
  under the equality of the result type. `f x y := g x` fails it.
- *A law `P` connects `x` and `y`* when it is not a conjunction of a law on `x` and a law on `y`.
  `P` separates exactly when `P x y'` and `P x' y` imply `P x y` and `P x' y'` for all `x, x', y, y'`;
  so `P` connects when there is a rectangle `x, x', y, y'` where that implication fails.
  `Q x and R y` depends on both and connects neither.

Both are existential: a test looks for a witness, not for a counterexample, and records the grade
"witnessed" (section 7). Declaring that a function depends on an argument, or that a law
connects two components, is stating such a law.

## 5. Well-formedness rules

Each rule names its files under `tests/spec/`: one program the checker must accept and one it
must reject, with the fragment of the error message the rejection carries in a `-- expect:`
comment. The suite is the specification applied to the interpreter.

**R1. A declaration mentions declared names.** Every name in `D(n)` of a declaration exists:
declared or defined. A declaration may mention types that are only declared; that is what lets
an object's laws and its head refer to each other.
Files: `r1_declaration.accept.lut`, `r1_declaration.reject.lut`.

**R2. A definition uses defined types.** For a definition `n`, every name that occurs in type
position in its declared type or its body is defined, unless it belongs to `n`'s own object. In
term position a declared name is allowed: a hole of a defined type is a parameter (`sigma : Float64`,
set by `luthier run --set`), and what depends on it does not reduce until it is filled. Code over
a type that is only declared, outside that type's object, must take the type as a parameter.
Files: `r2_definition.accept.lut`, `r2_definition.reject.lut`, `r2_unclaimed_laws.reject.lut`.

**R3. A predicate defines only what it touches.** The body of a subtype over a labeled base must
touch every label; over an unlabeled base it must touch its parameter. A predicate that touches
nothing (`\ p { true }`) defines nothing.
- `{ eq, add, mul | Associative A eq add }` is rejected: `mul` is a label no law touches, a
  semigroup juxtaposed to a bare function.
- The `| true` records of the first libraries disappear.
Files: `r3_connected.accept.lut`, `r3_dangling_label.reject.lut`, `r3_true_predicate.reject.lut`.

**R4. Only laws or recursion make a new type.** A definition `x : U := t` makes `x` a type with a
name of its own only if `t` is a subtype with a predicate (laws) or a recursive `data`. A body
that is structural (a product, a sum, an exponential, a non-recursive `data`) introduces a name
that claims nothing and is rejected: write `x = t` (an alias, R7), or write the type where it is
used, or declare `x : t` and owe it laws.
Files: `r4_product_inline.accept.lut`, `r4_recursive_data.accept.lut`,
`r4_product_named.reject.lut`, `r4_data_nonrecursive.reject.lut`.

**R5. An extern gives a value, never a type.** Types are defined natively. `x : T := extern
"..."` is accepted when `T` is defined (R2 applies to externs as to any body); `x : U := extern
"..."` is rejected. `extern provisional "..."` lifts both requirements, for working in a hurry on
a type nobody has defined yet or on a Python type nobody has described: it is accepted, recorded
in the certificate under `provisional` with the names it builds on, listed by `luthier check -v`,
and never certified.
Every refinement in the type of an extern is an obligation on the value it gives (2026-10-05): the
predicate of a subtype, the codomain of each arrow quantified over its domain (`neg : Float64 ->
NonNegative` owes `neg x >= 0.0` for every `x`), each component of a record or a pair, and each
entry of an array (`pairI : Vec (Fin nodes)` owes that every entry is below `nodes`); the dimensions
of an array are read off its shape and owe nothing. A refinement under a constructor of a sum or a
data type (the `Table` of a `Maybe Table`) is not entered yet.
Files: `r5_extern_value.accept.lut`, `r5_extern_provisional.accept.lut`,
`r5_extern_type.reject.lut`, `r5_extern_over_declared.reject.lut`.

**R6. The body of a declared name is an inhabitant or a predicate.** If `x` is declared `x : T`
and later given a body, the body has type `T`, or `T -> Bool`, or is a `Law` over `T`. Any other
type is an error, reported against the declaration.
Files: `r6_predicate_body.accept.lut`, `r6_body_type.reject.lut`.

**R7. An alias is written with `=` and has no state.** `AB = A * B` makes `AB` stand for the term
on the right everywhere; the checker expands it before anything else, so an alias is never
declared, defined or certified. A name that is an alias and is also declared or defined is an
error. A generator given to an alias is the generator of the type the alias stands for
(2026-10-05): `gen FullCoords` with `FullCoords = VecOf (freeDim + 1)` draws every `VecOf 16`, and
two aliases of one type cannot both have one. A distribution that means something (a broken graph,
a complete one) is a type with a law, `{ g : DistanceGraph | not (ValidGraph g) }`, and every value
its generator gives is checked against that law; a value outside is an error that names the
generator.
Files: `r7_alias.accept.lut`, `r7_alias_defined.reject.lut`.

**R8. `==` exists only where equality is structural.** `==` is defined on `Int`, `Float64`, `String`,
`Unit`, `Empty`, and on products, sums, recursive `data` and subtypes built from types that have
it. Not on exponentials, and not on anything containing one. A law that compares values of such a
type takes the equality it uses as a parameter or as a component of its theory: the observational
equality of the presentation. `algebra.lut` already does so (each structure carries its `eq`).
Files: `r8_equality_parameter.accept.lut`, `r8_equality_function.reject.lut`.

**R9. Function types are contravariant in the domain and covariant in the codomain** (`06 §5`). A function `A -> B` passes where `A' -> B'` is expected when
`A'` refines `A` and `B` refines `B'`.
Files: `r9_variance.accept.lut`, `r9_variance.reject.lut`.

**R10. A law characterizes; a second implementation is not a law** (decided 2026-10-05; `07`).
The laws of an object are the mathematical properties that determine its operations, up to the
equality of the presentation: bilinearity and an orthonormal basis for an inner product,
multilinearity, alternation and `det I == 1` for a determinant. A definition of the operation
written in the kernel (a sum over the indices) is a *model* of those laws, certified against
them like any other; an implementation of the environment is another model. That two models
agree (`Agrees`) is a corollary of the laws characterizing the object, useful to tighten a
tolerance, and never the law itself. An object whose only laws compare it with a second
implementation is reported as *consistent, not characterized* (section 6). The rule is not
decided by the checker: it is a rule for the one who writes the laws, and `check -v` makes the
difference visible.

Two consequences, from the same discussion. Each concept is identified with the mathematical object
that best represents it (a vector space, a ring, an inner product space, a symmetric bilinear form),
and that object is the invariant of its type: the leaf, the instance or the value is declared at the
structure, so the structure's laws are its obligations, not laws stated apart on a copy. And a law
has one name: it is written once in `lib/algebra.lut`, in its most general form, and a special case
is an application of it, never a second declaration (commutativity is `Symmetric` with result type
equal to the argument type; associativity of an operation is the law of an action of a set on itself).
Structures are built by inclusion of the ones below them. `algebra` is imported by every library
that states a property.

## 6. Reports that do not reject

`luthier check -v` reports, without rejecting (2026-10-05: also the axioms, `06 §3`):

- every `provisional` extern and what it builds on (R5);
- for each concrete type with laws, the table of observers against constructors, and the cells
  with no law: *sufficient completeness* (Guttag, 1977). A full table says everything observable
  about every constructed value. An extensionality law (two values are equal when every observer
  agrees on them) turns "same observations" into "same value";
- holes that the entry of `luthier run` depends on;
- (decided, not implemented) for each operation with laws, whether they characterize it (R10) or
  only compare it with another implementation. Version 0 can only tell the two apart by name:
  a law whose body applies the operation and another definition to the same arguments and compares
  the results is a comparison. Characterization proper is a judgement the author makes and `07`
  records.

## 7. Certification

What is certified is never a name: it is a law applied to particular values (a model, a chain of
functions), over a domain, by a mode. The grades, from weakest to strongest:

| grade | meaning |
|---|---|
| point | one case evaluated |
| sampled `n` | `n` cases from a declared generator, size growing over the run |
| exhaustive | every case of a finite domain |
| witnessed | an existential law: a case exhibited (section 4) |
| proved | universal; not in version 0 |
| assumed | an axiom: the laws are stated and taken as true, never tested (`06 §3`) |

A certificate entry records the law, the values it was applied to, the grade with its `n`, the
generators, the seed, the first cases, and the hash of the dependency cone (`03 §4`). The grade of
a chain `f (g x)` is that of its weakest link. "Certified" in `check -v` summarizes the entries of a
name; it is not a state the name has once and for all.

- The obligations of a name are the laws its type states, applied to its body, quantified over the
  laws' parameters. `test n` runs the obligations of `n`, and of every member of `n`'s object.
- An obligation raised inside a branch of `if c then a else b` carries `c` (or `not c`) as a
  precondition: `f lo` in the `else` of `if lo >= n` owes `lo < n` only where `lo >= n` fails. An
  obligation raised inside `match e { x -> t }` speaks of `e`, not of every `x`: the variable is a
  name for `e`; inside `match e { (x, y) -> t }`, `x` and `y` name the components of `e`. Without these, every recursion over indices owes laws that are false.
- An obligation is quantified only over the parameters it mentions, and those their types mention.
  `DotAgrees (d : Vec -> Vec -> Float64) (n : Dim) (x y : VecOf n)` owes `y.n == x.n` inside, which does
  not mention `d`; drawing a `d` would be both unnecessary and impossible.
- A function is drawn as its table when its domain is `Fin n`; of an infinite domain, as a constant,
  or an affine map on `Float64 -> Float64`. The second is a thin sample of the function space, and the
  certificate's description of the generator says so.
- A sampled case whose parameters cannot be drawn, because a parameter's type depends on earlier
  ones and is empty for them (`k : Fin n` with `n = 0`), holds vacuously and is skipped; a law none
  of whose cases could be drawn is reported as an error, not as passed.
- A law quantified over all models of a theory has no generator of models and stays pending; it is
  certified per model, on each concrete value that inhabits the theory.
- `run` and `eval` require every name in the cone of the entry to be defined. They do not require
  certification; a run whose cone contains uncertified or provisional names records that in its
  `.run.json`.
- Importing a file accepts its certificate entries by hash, unchanged.

## 8. Example

    -- a concrete type, defined natively: a table is a function from a column and a row to a cell
    Cell = < int : Int | real : Float64 | text : String >
    Table = { columns : List String, nRows : Int, cell : String -> Int -> Maybe Cell }

    -- a theory, declared, its laws, then defined: the cycle Codec -> laws -> Codec is the object
    Codec : { parse : String -> Maybe Table, render : Table -> String, eq : Table -> Table -> Bool }
    RoundTrip (c : Codec) (t : Table) : Bool :=
      match c.parse (c.render t) { nothing -> false ; just u -> c.eq t u }
    Rejects (c : Codec) (b : BrokenText) : Bool := match c.parse b { nothing -> true ; just t -> false }
    Codec := RoundTrip & Rejects

    -- a model: a value of the theory, built from externs over defined types (R5); a branch of Codec
    csv : Codec := { parse := extern "python:luthier.tables.parse",
                     render := extern "python:luthier.tables.render",
                     eq := sameTable }
    test csv with 200

`Table` here is an alias (R4: a product with no laws is not a new type). If tables had invariants
(the cells of a column all of one kind, rows below `nRows`), `Table` would be declared over this
base and defined by them. `Codec` carries its equality as a component (R8), because a `Table`
contains a function and has no `==`.

## 9. Presentations and translations

A mathematical object admits several presentations: other choices of primitive operations and
laws, equivalent to each other (a group by multiplication, unit and inverse, or by division
alone; a Boolean algebra by and/or/not or by nand). An operation defined from others, and also
characterized by a property, gives a theorem: a law on a branch, of the kind `04 §6` calls
`Agrees`. A translation between presentations `P` and `Q`, both type operators `U -> U`, is a pair
of functions `to : (A : U) -> P A -> Q A` and `from : (A : U) -> Q A -> P A` whose round trip is the
identity under the observational equality of each presentation. It is expressible today
(checked with De Morgan between and/not and or/not: the laws of `Q` fall on each translated model
as obligations, and pass), with two limits: it is certified per model, not for all models, and
the round trip needs the equality that R8 makes a component. Translations as a concept the
language names and certifies, and several canonical presentations of Luthier itself with their
equivalences, are for version 1 or 2.

Two models of one characterized object agree where the laws determine it: that is what the
`Agrees` laws of the libraries state, and it is where they belong, as a corollary (R10), not as a
definition.

Some presentations have no computable translation, and then their equivalence is a law. A
probability kernel from parameters to data is read three ways: a sampler, a likelihood, and the
probability integral transform of each datum. Going from the likelihood to the sampler needs an
inversion or a chain of Monte Carlo, and from the sampler to the likelihood an estimate of a density;
neither is a function one can write exactly. `Kernel` in `lib/probability.lut` is the head of the
object and the three are its components, with one law per side of the triangle: the density-pair
laws (sample and likelihood), the slope of the transform is the density (transform and likelihood),
and simulated data have a uniform transform (sample and transform). The project certifies it on the
model of the tape distances, with two negative controls, each breaking one side.

## 10. Open

- The tests for the semantic dependence of section 4: their syntax (a test mode that searches for a
  witness) and their place in the checker (do they gate the definition of an object, or report).
- `=` as alias (R7) against `=` as the identity type of `00 §4`, when the proof layer comes.
- Implicit arguments. Code over theories takes the model as a parameter, and without implicit
  arguments every use spells it out. Pending since 2026-10-03.
- Whether a file that imports a provisional definition may itself be certified, or inherits the mark.
- Generators from constructors: a concrete type's generator built by composing its constructors,
  so laws are testable without a generator written in Python that bypasses the predicate (case 9).
- Equality as a degree: for samplers, two values are equal in distribution when a test does not
  separate them; the equality component would return a verdict with its level instead of a `Bool`.
- Whether an alias may abbreviate a value (`two = 1 + 1`) as well as a type.
- Obligations under a constructor or label pattern. In `match m { just x -> t }` the variable is not
  a projection of `m` (which may be `nothing`), so an obligation in `t` is still quantified over
  every `x`; it should carry `m == just x` as a precondition, as a branch of `if` carries its
  condition. Patterns of variables, wildcards and tuples of any length already name the parts of
  the scrutinee.
