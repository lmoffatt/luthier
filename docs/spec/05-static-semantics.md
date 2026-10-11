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
- `Bool` is `< true : Unit | false : Unit >`; `Failures E` is `List E`, the failures a check finds,
  empty when it holds (section 9, *Checks*); `Law` is the type of a conjunction of quantified
  Bool- or Failures-valued laws (`04 §3`).
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
- A *law* is a Bool-, Failures- or Law-valued definition, or one conjunct (split at `&`) of the predicate
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
- `x : T := p` with `p : T -> Bool` or `p : T -> Failures E`, or `p` a `Law` over a `T`, defines `x` as the subtype
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
Added 2026-10-07 (D-2026-10-07-e; decided, not implemented): a structural type with no laws, an
exponential `A -> B`, a product or a sum, is a *base* and not a defined type for this rule. A value
is defined at a type that has a name and laws, at a `data` or at a primitive; a top-level definition
at a bare exponential is a loose function, and there are none: a function is a value of a defined
function type, a theory (`00`, *Function type*). A helper either gets its recursion as its laws or
waits for local definitions (`02 §8`). The libraries do not comply yet (`exp : Float64 -> Float64`
in `real.lut`, the helpers of `array.lut`): `check -v` is to report loose functions first, as it
reports *consistent, not characterized*, and the rule rejects once local definitions exist and the
certificates are reissued. Files: to be written with the implementation.

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
The same holds for an exponential (2026-10-07, D-2026-10-07-e): a lawless `A -> B` is a base, not a
type a value is written at; see R2.

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
of an array are read off its shape and owe nothing. Under a constructor of a sum (the `Table` of a
`Maybe Table`) each law of the payload becomes `match v { just t -> L t ; _ -> true }`, and a law
quantified over something whose type depends on the payload (a row `r : Fin t.nRows`) is quantified
over the base of that type with its refinement as a precondition inside the match. A refinement
deeper in a payload (a field of a record in a sum) and one under a data type are not entered.
`luthier run --checked` tests every value an extern gives against the Bool laws of its type as it
crosses, each entry of an array and each component of a record included; a quantified law is left to
`test`, and a function an extern gives is tested when it is called.
Files: `r5_extern_value.accept.lut`, `r5_extern_provisional.accept.lut`,
`r5_extern_type.reject.lut`, `r5_extern_over_declared.reject.lut`.

**R6. The body of a declared name is an inhabitant or a predicate.** If `x` is declared `x : T`
and later given a body, the body has type `T`, or `T -> Bool`, or `T -> Failures E`, or is a `Law` over `T`. Any other
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

**R11. A condition refines in its branch** (decided 2026-10-06, `00`, *What types are for*; not
implemented). In `if p x then a else b`, where `x` is a variable of type `T` and `p x` is a `Bool`,
`x` has the type `{ x : T | p x }` inside `a` and `{ x : T | not (p x) }` inside `b`. A coercion of
`x` to that refined type there owes nothing: the condition is the check, made once. If `a` asks for
`{ x : T | p x }` and the condition is another predicate `q x`, the coercion owes `q x -> p x`, an
obligation certified like any other; usually it is a law the program already states about `q`, as
`ReportsValidity` relates `firstViolation` to `ValidGraph`. The same holds for a pattern: inside
`match m { just y -> a ; ... }`, `a` knows `m == just y` (section 10). The rule replaces the
precondition of section 7, which only weakens an obligation raised in a branch, and the textual
discharge the interpreter does today (an obligation equal to the condition of its branch).
Files: to be written with the implementation.

**R12. `:=` defines once; `<-` rebinds** (decided 2026-10-11, D-2026-10-11-c; blocks, defaults, named arguments and the session implemented the same day). A
name bound with `:=` is defined once, and a second definition of it is an error ("x is defined
twice"). A name bound with `<-` may be bound again with `<-`: each binding is a fresh name in the
core, as in static single assignment, and every later use means the latest (D-2026-10-10-e, a
mutable parameter is two variables, before and after). A name first bound with `:=` cannot be
rebound with `<-`. Rebinding needs an order, so `<-` is allowed in a block, in a parameter's default
and in a named argument, and is an error at the top level of a file, which is a set of acts without
order (section 2). A default is the first binding of its parameter and the call rebinds it before
the body runs; the elaborated call, which is what is hashed and certified, carries the value the
body sees. A law of a function is quantified over a defaulted parameter, not tested at its default.
Blocks (2026-10-11, D-2026-10-11-i; `02 §9`): a brace term with a final expression is a block, the
body of a lambda is one; a name bound in a block is visible to the end of that block and in nested
blocks; `:=` of a name already defined in an enclosing scope is an error, not a shadowing; `<-`
rebinds only block-local `<-` names and the parameters of the enclosing definition; a `<-` whose
previous binding has no consumer is an error in a file and reported in a session; actions take and
return the world, so their order is the dependency through it. Three kinds of block: a body, `main`
in a file, the session.
Files: `r12_block.accept.lut`, `r12_defined_twice.reject.lut`, `r12_rebind_defined.reject.lut`,
`r12_unused_rebinding.reject.lut`, `r12_toplevel_arrow.reject.lut`, `r12_defaults.accept.lut`,
`r12_named_unknown.reject.lut`.

**R13. An operator is resolved by the type, and a type names its model** (decided 2026-10-11,
D-2026-10-11-j; implemented the same day: resolution by the argument types, and a second meaning of
an operator on the same types refused). The operators on the values of a type are those of the model the
type names: `i : Int` adds with the ring of `Int`, `j : Z7` with `ringZ7`. A carrier with two models
is two types (`Int` as a ring and as the max-plus semiring; `Float64` under two tolerances), and the
conversion between them is explicit, `forget` to the carrier and a constructor back, never silent.
The operators of a wider model apply to a narrower type only through a homomorphism stated and
certified as a law: a value of `Z7` uses `Int`'s `+` after `forget`, and the law that relates the
two is `mod 7` being a ring homomorphism. Where a theory does not fix the role of an operator (a
function over a bare `Monoid` applied at `Int`, which carries two), the model is named in the call.
The subtype is the wrong relation for a quotient: `examples/z7ring.lut` is rewritten with `Z7` as
its own type.
Files: `r13_operator_by_type.accept.lut`, `r13_two_models.reject.lut`.

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
| bounded | every case of a box of an infinite domain (`Int` in [-size, size]) |
| exhaustive | every case of a finite domain |
| witnessed | an existential law: a case exhibited (section 4) |
| proved | universal; by a proof (not in version 0), or by citation: `cite x r checked by` records that a theorem outside Luthier, the reference `r` (a `Reference` value read from a `.bib`, with DOI, ISBN or URL and hash), establishes the laws of `x`, and who checked the correspondence, `human`, `ai+human` or `none` (D-2026-10-11-f, 2026-10-11; allowed in user code) |
| assumed | an axiom: the laws are stated and taken as true, never tested, nothing recorded behind them (`06 §3`) |

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

As implemented (2026-10-05, phase 2 of `record/plan-2026-10-05.md`):

- A law has one of three outcomes: *passed*; *failed*, by a counterexample, an evaluation error on a
  case, or a registered generator whose value is outside its type; *not run*, when a parameter has no
  generator, no case could be drawn, the reduction ran out of fuel, or the law is blocked by a hole
  without a value. A definition passed when every law passed, failed when one failed, and is not run
  otherwise. Only passed is certified.
- The hash of an entry covers the code of the cone, the Python behind every extern it calls (the
  source files of the module's directory, or the installed package and its version) and the
  interpreter; the entry also records the generators it drew from, with their fingerprints, and the
  case count and mode it ran. It is trusted when all of them match and the count reaches the file's
  directive; otherwise `check -v` says which part changed.
- The comparison happens once the whole program is loaded and its holes filled. A certificate keeps
  an entry per filling of a name (up to four); `luthier test f --imports` runs the imported
  obligations with no entry for the program `f` and writes them to their own files. Names that no
  longer exist are pruned when a certificate is written.
- A test whose cone has a provisional extern records it, and is never certified (R5).
- `luthier run` prints the states of the names with laws in the cone of its entry, records them in
  `.run.json` with the fingerprint and the revision of the interpreter, and with `--require-certified`
  refuses to run unless every one is certified. `luthier certify f1 f2 ...` tests several files at
  once, each in its own process.
- The grade "bounded" is given when an enumeration took `Int` in a box; a refinement of `Int` bounded
  on both sides by closed integers is enumerated over its interval, exhaustively.

Added 2026-10-06 (phase 5 of the plan):

- An obligation is of one of two kinds. A *law* is stated by a definition's declared type
  (`fastStep : { f : Step | StepAgrees f } := pyStep`). The obligation of a *type* is a coercion
  inside a body, or a refinement of what an extern gives (R5): a claim about the values a computation
  gives. A case where the computation raises gives no value, so for the obligation of a type it is
  outside the claim: it is skipped and counted, and an obligation every case of which raises is not
  run. For a law, an error on a case is a failure, as a counterexample is. The partiality itself
  shows at run time, where the error stops the run.
- A refinement of a record bound by its pattern (a `Table`), whose laws quantify over more than the
  value (a column and a row), is one obligation per law, over the law's own parameters.
- Each law of an entry records how long it took.

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

**Checks** (decided 2026-10-06; primacy inverted 2026-10-11, D-2026-10-11-a; not implemented).
A subtype `{ x : T | p x }` is written once, by the check that explains it: `p : T -> Failures E`,
with `Failures E = List E`, the failures `p` finds in `x`, empty exactly when `x` is in the subtype.
The other forms are its forgetful projections, and the demand chooses among them (L13, forgetting is
determined by the demand). None is written by hand and no law ties them, since each is computed
from `p`:

| form | type | from `p x` |
|---|---|---|
| every failure | `T -> Failures E` | `p x` itself |
| the first `n` failures | `T -> Failures E` | its first `n` elements |
| the reason of a failure | `T -> < ok : { x : T \| p x } \| failed : E >` | `ok x` if empty, else `failed` of the first |
| the refined value, `refine p` | `T -> Maybe { x : T \| p x }` | the reason, with the failure forgotten |
| the characteristic function, `holds p` | `T -> Bool` | whether it is empty |

A Bool-valued predicate is the check that explains nothing: `Bool` is `Failures Unit` cut at one
failure (`true` the empty list, `false` one `unit`), and every rule that accepts a `Failures E`
accepts a `Bool`. A `Failures E` used where a `Bool` is expected (the condition of an `if`, an
operand of `and`) is projected by `holds` implicitly, as a subtype is forgotten into its base.

The demand carries `n` (P11, every criterion is a parameter). An action that reports (`luthier
check`, `luthier test`, a diagnostic a program prints) asks for every failure unless told otherwise,
as a compiler with no error limit; a condition (`if`, a `match` on `ok` and `failed`, `refine`) asks
for one. With dependencies explicit, "every failure" is well defined where a compiler has to guess
which errors are cascades of the first: a failure blocks only the cone of its node, and the failures
outside it are independent. Stopping the computation of `p x` at the `n`-th failure, rather than
computing them all and keeping `n`, is open (section 10).

Composition. `and` concatenates the failures: over independent checks they accumulate, which makes
the form an applicative functor. `or` holds when either operand holds, and otherwise keeps the
failures of both. `not` has no failure to report when `p` holds, so it is taken on the projection to
`Bool` and loses the explanation, unless the check carries a witness (below). Checks chained along a
dependency (read, then validate, then fit) compose by the bind of the reason form and stop at the
first failure. `refine` is written once, generically, and R11 is what makes it typable:

    refine (T E : U) (p : T -> Failures E) (x : T) : Maybe { y : T | p y } := match p x { nil -> just x ; cons e es -> nothing }

Which form a program uses depends on whether the evidence must outlive the branch. Where the result
of the check is used inside the branch, `holds` and R11 suffice. Where the value leaves it (it is
returned, stored in a record, passed on later), and at the boundary of a program (a value read from
a file or given by an extern), the evidence travels in the type: the check returns the refined value
or the reason. The pair `firstViolation` and `ReportsValidity` of the distance graph is the earlier
form, two definitions and a law between them; under this rule it is one check and its projections.

Other contexts ask for forms that are not projections of the failures:

- *A witness.* A check that computes evidence returns it: a dependent pair `(x, w)` with a law
  saying `w` attests `p x`. A Cholesky factor attests positive definiteness, the least distance
  attests separation, the seed that caught a mutant attests the control, the failing row attests a
  violation, the decrement and the final spectrum attest convergence. `refine` is the case where
  the witness is the value itself (*certifying algorithms*: R. M. McConnell, K. Mehlhorn, S. Näher
  and P. Schweitzer, Computer Science Review 5, 2011).
- *A statistical verdict.* A test with a false failure rate (`UniformDraws`, `IsDensityOf`, the
  transform of the residuals) does not establish a fact about the value, so refining by it would
  claim what the test does not show, and a Bool loses its level. It returns a verdict with its
  statistic and its level (equality as a degree, section 10).
- *A tolerance.* A check by `approx tol` refines with `tol` in the type: `approx` does not compose,
  since `a` near `b` and `b` near `c` do not make `a` near `c` within the same `tol`.

A check about the world refines the content it read. Whether a directory holds a
graph is true when it is asked and may be false when the graph is read; the check and the use are
one operation (`readGraph` returning a graph or the reason it could not), and the content is
validated after. `run --checked` is the one deliberate exception to checking once: it checks again
every value that crosses from Python, to debug the bridge.

## 10. Open

- Done 2026-10-11: `exhaustive` over `Fin n -> T` with `T` finite enumerates the tables (at most
  20000); `cite` implemented with `lib/reference.lut` and `.bib` files as modules of references
  (`cite_proved.accept.lut`, `cite_not_reference.reject.lut`).
- Eta for exponentials cannot be stated as a law, since equality of functions is not structural
  (R8); `kernel_laws.lut` states it pointwise, which is beta.
- The `Reference` type and the reading of a `.bib` as a module (`biblio.key`), for `cite`.
- The tests for the semantic dependence of section 4: their syntax (a test mode that searches for a
  witness) and their place in the checker (do they gate the definition of an object, or report).
- `=` as alias (R7) against `=` as the identity type of `00 §4`, when the proof layer comes.
- Implicit arguments. Code over theories takes the model as a parameter, and without implicit
  arguments every use spells it out. Pending since 2026-10-03.
- Whether a file that imports a provisional definition may itself be certified, or inherits the mark.
- Generators from constructors: a concrete type's generator built by composing its constructors,
  so laws are testable without a generator written in Python that bypasses the predicate (case 9).
- Stopping a check at the `n`-th failure (section 9, *Checks*). With nodes computed once and whole
  (D-2026-10-10-d), a fold that builds the failures computes them all; for `n` finite the demand has
  to reach into the fold so it stops. A rewrite of the plan, not of the program.
- Equality as a degree: for samplers, two values are equal in distribution when a test does not
  separate them; the equality component would return a verdict with its level instead of a `Bool`.
- Whether an alias may abbreviate a value (`two = 1 + 1`) as well as a type.
- Obligations under a constructor or label pattern. In `match m { just x -> t }` the variable is not
  a projection of `m` (which may be `nothing`), so an obligation in `t` is still quantified over
  every `x`; it should carry `m == just x` as a precondition, as a branch of `if` carries its
  condition. Patterns of variables, wildcards and tuples of any length already name the parts of
  the scrutinee. Decided 2026-10-06 as part of R11.
- Checks recorded in types (R11 and section 9, *Checks*), decided and not implemented: the rule in
  the checker, `refine` and its derived forms in a library, and the code that checks twice or keeps
  a check as data (`plan-2026-10-05.md`, "Added 2026-10-06").
