# The fundamental elements of a Luthier program

Draft 2, 2026-10-26, by Claude Sonnet 5.5, brought to the project as it stands: the core rebuilt as
the prelude (tag `v0.3`; `record/plan/core-2026-10-17/execution.md`, Status), `luthier test` and
`luthier certify` with their stores of certificates, `luthier run` with its refusal and its records,
and the reader's account in `docs/concepts.md` (draft 1), to which this guide points for the tape
example, the grades and the numbers. Draft 1 (2026-10-13 and 2026-10-14, by Claude Opus 5.5 and
Claude Sonnet 5.5; git keeps it, last changed at 472bc98) had rewritten the first guide against the
specification; this draft changes the sections on theories, models, certification, the world and the
two programs, and leaves the others. Its inputs are the specification in `docs/spec/` (chapters 1 to
5, 7, 10 and 12), `docs/principles.md`, `docs/principles-for-readers.md` (draft 7), the files of
`src/luthier/lib/` and `src/luthier/lib/core/`, the programs of `examples/` and `docs/concepts/`, and
the output of `luthier --help` and of each command's `--help` on 2026-10-26. It is the reading guide
for someone meeting Luthier now: the few ideas a program is made of, in the order to think them, and
one program executed by hand, and a second walked through. The rules are in the specification. Where
this text and the specification differ, the specification holds; where the specification and a
theory file differ, the theory file holds, by L14.6 (Luthier's own theories are written first and
are the authority). Ideas that are Luciano's say so and cite their source: his voice notes in
`record/audios/`, his chats by id, his words as quoted in `record/decisions.md`. What the model adds
beyond the sources is marked *proposed*. Section 12 says what was left out of the old guide and why,
and what this draft changed.

## 0. Notation

The symbols of this guide, as spec 1 (terms and notation) fixes them.

- `x : T` reads "x refines T"; when x is a value, "x is a T" (spec 1.S1).
- `x : T := t` defines `x`, with `T` as its type and `t` as its body. Written without `:= t`,
  `x : T` is a declaration, a name with no body yet. `x = t` makes `x` an alias, another name for the term `t` (spec 1.S2).
- `U` is the universe, the type whose values are types. `W` is the world, the token that an action
  takes and gives back (section 7).
- `A -> B` is the type of functions from `A` to `B`, and `(x : A) -> B` its dependent form, where
  `B` may mention `x`. `A * B` is the product of two types and `(x : A) * B` its dependent form.
  `A + B` is their sum.
- `{ x : A, y : B }` is a record type, a product whose components have names; `{ x := a, y := b }`
  is a record value; `e.x` is the component `x` of `e`.
- `{ a : A || b : B }` is a labeled sum: each value is an `A` tagged `a` or a `B` tagged `b`
  (D-2026-10-13-w; `||` is his, because a sum is a disjunction).
- `{ x : T | p }` is the subtype: the values of `T` for which the predicate `p` holds.
- `fn x { t }` is the function with parameter `x` and body `t` (D-2026-10-13-y).
- `p & q` joins two laws into one law (spec 5.S6). `a <> b` is the operation of a semigroup, such as
  the concatenation of two lists or two strings, and `+` is kept for commutative additive structures
  (D-2026-10-21-a, one name per concept; concatenation is not commutative).
- A brace term `{ ... }` whose last item is an expression is a block; its items are `x := t` and
  `p <- t`, where the pattern `p` takes apart what an action gives (section 2). `match e { c -> t ; ... }`
  chooses an arm by the constructor of `e`.
- `import "x.lth" A B` brings the names `A` and `B` of a theory file; `import "x.lut" m : T` brings
  the model `m` of the theory `T` from a model file (spec 12.S22; section 4).
- `t[a/x]` is `t` with `a` put in place of each free occurrence of `x`.
- `≡` is definitional equality, which holds when reduction takes two terms to one normal form;
  `==` is the equality a program computes, which exists on some types only (section 5).

## 1. What a program is made of

Luthier sees a computation in two parts (Luciano, 2026-10-07 and 2026-10-08, chat:182f2465:750,
chat:893831f1:131). The *plan* is timeless: definitions, laws and the equivalence of expressions.
Nothing in it happens, so nothing in it has to be undone. The *execution* is temporal: actions in
an order, leaving a record that only grows. The two are tied both ways. The properties of actions
are values of types, under the same rules of equivalence as any other value; and every equivalence
is established by executing something: reducing a term, running a test, reading a file.

The principles name what this gives (the Terms of `docs/principles.md`; D-2026-10-13-d, -e). What
is said, the definitions, lives in `U`. What is done, the actions, acts on `W`. What is certified
ties them: a certifier is the action whose result comes back into the plan, and what it changes is
the belief that a value belongs to a type (his correction, D-2026-10-13-e). He reads the program as
an observer that updates what it knows of the world by what it observes (D-2026-10-08-a); by his
later correction, what a sampled check gives is the probability of a counterexample not yet seen,
and Bayesian evidence, a likelihood, is another thing (L12.6 (cost has two readings, a distance and
that probability); D-2026-10-13-n).

The list of ideas is written for one use: to state the interpreter of Luthier in Luthier (Luciano,
2026-10-08, chat:893831f1:158). Since D-2026-10-13-h that is also the order of work, by L14 (what
can be written in Luthier is written in Luthier): the theories come first, in Luthier, and each
Python file is a specimen certified against its theory. So every idea below is one that a theory
file of `src/luthier/lib/` states, and section 8 shows those files.

The order of what follows: the act and its graph (2), a type is a theory (3), a value is a model
(4), laws and equality (5), certification by testing (6), the world (7), the program as data and
the pattern of the first files (8), two programs, one executed by hand and one read through (9).

## 2. The unit is the definition

A program is a set of acts with no order among them (spec 3.S1, the top-level acts of a program
are unordered). An act is a declaration `x : T`, a definition `x : T := t` or an alias `x = t`;
beside them stand an `import` line, an `operator` line, and a bare term the module keeps, such as
a test (spec 2.S5; D-2026-10-13-o). There are no statements and no sequence at the top level. The
dependency between definitions is read off the names each one uses, which gives the directed graph
of definitions of the voice note 2026-05-29 15.11.47 [01:48], and by L4.1 (time is rebuilt from the
dependencies, never from the text) that graph is the only order. The checker reads the whole
program, imports included, before it checks any part of it (spec 4.S11).

The graph may have cycles, and a cycle is no error. Laws mention the type they constrain; the type,
once defined, names its laws; the loop they form, a strongly connected component of the graph (a
maximal set of names each reachable from every other), is the theory. A definition that mentions a
theory without lying on its loop is a branch: a new entity depending on the theory in one direction
(voice notes 2026-10-04 12:16 and 12:30; spec 1.S8 and 4.S12). Since this structure lives in the
names, two theories whose cycles have one shape can be recognized as candidates for an isomorphism
before any implementation is read (spec 4.S13).

A name passes through three states (spec 4.S6): *declared*, its type known; *defined*, its body
known; *certified*, some of its laws checked, each with a grade (section 6). The type is the
proposition the name claims and the body is its evidence; for a function, its implementation (voice
notes 2026-05-26 12.32.24 [00:51] and 2026-08-31 19.48.17 [01:02]). That covers the double
definition the voice note 2026-05-29 14.28.55 [03:42] asked for: "from the properties" is the type,
"operationally" the body.

Inside a block the text does fix an order. A block is a brace term whose last item is an
expression, its value (spec 2.S17); its items are `x := t`, which defines once, and `p <- t`, which
binds the names of the pattern `p` to what `t` gives, each `<-` making fresh names, so `x <- x + 1`
is allowed (L4.2 (inside a block the text says which binding a name means)). The two acts share one law, his
annotation in L4.3 (the two binding acts share one law): after the act the name equals the term, after `:=` for good and after `<-` until
the next `<-`. A block is one of three things: the body of a definition or of a lambda, the `main` of a
file, or the session. A file is never a block, and `<-` at its top level is an error
(spec 2.R5).

## 3. A type is a theory

G1 (types are theories and their values are models of them) is his first eureka: if a type is a
proposition, then "this structure follows the laws of the theory" can be said as "this structure
has the type of the theory", and Luthier checks that it does. Declaring `m : T` declares the tests
that `m` will pass, so coding and testing are one act. The words that follow are those of the Terms
of `docs/principles.md`.

- A *structure* is a type built by the kernel's formers: a product, a sum, a function type, a
  recursive type, each possibly holding the others.
- A *law* is a predicate, a function into `Bool`, or a cost, a function into `Cost` (the
  non-negative reals with infinity, 0 for true and ∞ for false). A law is a term valued in `Bool`, or in `Law`, the type of what a test runs, which also
  carries the numerical laws of section 6 (spec 5.S1). Laws valued in `Cost` are decided and
  suspended; every law today is a `Bool` or a `Law` (spec 5.S2; D-2026-10-14-c).
- A *theory* is a structure together with its law; a *model* is a value of a theory whose law has
  been certified.

How a theory is written, in the pattern of the first theory files (`src/luthier/lib/ebnf.lth`,
D-2026-10-13-r): declare it at its structure, a record type of its operations; write each law as a
predicate over a model; define the theory as the conjunction of its laws. In the core, the
properties that laws are made of are written once, generic over an operation and its equality
(D-2026-10-17-b; `lib/core/properties/operations.lth`), and a structure is the conjunction of
properties over its fields. The monoid, from `lib/core/structures/algebraic.lth`, with the two
properties it uses:

    Associative (A : U) (o : Object A) (op : A -> A -> A) (x y z : A) : Bool :=
      o.eq (op (op x y) z) (op x (op y z))
    Neutral (A : U) (o : Object A) (op : A -> A -> A) (e : A) (x : A) : Bool :=
      LeftNeutral A o op e x and RightNeutral A o op e x

    Monoid (A : U) (o : Object A) : { neutral : A, combine : A -> A -> A }
    Monoid (A : U) (o : Object A) (m : Monoid A o) :=
      Associative A o m.combine & Neutral A o m.combine m.neutral

The declaration `Monoid` takes a type `A` and an `Object A` (a type with its own equality, section
5) and gives a record type with no body: this is L2 (declare, then define, then inhabit). The
definition on the last line gives the declared name a body whose type is a law over it, and so
defines a type: the records `{ neutral, combine }` for which both properties hold at every
argument, by spec 4.R6 (the body of a declared name is a value of its type or a law over it) and
4.S7 (the type of the body decides which). The parameters before the colon are curried, so
`Associative` is `fn A { fn o { fn op { ... } } }` (spec 2.S12). A theory with parameters repeats
them in its defining line, and the model follows them (spec 4.R6; D-2026-10-13-o). The laws of a
theory file such as `ebnf.lth` or `tape.lth` mention the theory they constrain, and the loop they
form with the theory is a strongly connected component of the graph of section 2; the core's laws
are generic properties that do not mention the structure, so each structure there is a component of
one name (spec 1.S8, 4.S12). Either way the theory is Hilbert's implicit definition made a type: the
type is the theory, the conditions an object must meet (the name "theory and model" is
D-2026-10-07-d).

**The formers.** The kernel has the universe `U`; the function type, with its dependent form; the
product, with its dependent form and records; the sum, with labeled sums; `Empty` and `Unit`, the
sum and the product of nothing; the subtype; `data`, a structure freely generated by named
constructors, recursive or not (spec 3.R3); and the primitives `Int`, `Rational`, `Real`, `Float64`
and `String` (spec 3 §2, 11.R1). With them the kernel is a bicartesian closed category, closed
under products, sums and function types, extended by the dependent forms, recursive structures and
subtypes (spec 3.S8). The names of a record are its projections, the arrows `first` and `second` of
the product, so they are part of the structure, and the labels of a sum are its injections (his
framing, D-2026-10-13-x); the kernel term keeps them as `Record`, `RecordValue` and `Proj`, and
`Sum` and `Inj`. The subtype is in the kernel although it could be derived, because the rules of
spec 4 are stated directly on it (spec 3.S6). Version 0 has a single universe with `U : U`, which is
inconsistent as a logic and harmless for testing, since testing proves nothing; a hierarchy of
universes waits for proofs (spec 3.S8; D-2026-10-13-aa). This is one presentation among several: a
smaller one would keep `U`, the dependent function and `data` and derive the rest, and Luthier
should one day state the equivalence of its presentations (voice note 2026-10-04).

**Dependent types.** In `(x : A) -> B` and `(x : A) * B` the second part may mention the value of
the first: a "for all" and a "there is". A vector of length `n` is `Fin n -> Float64`, with
`Fin n` the integers from 0 to n − 1 (spec 3.S21, 11.R1); a theory with a parameter, `Monoid M`, is
a function into `U`; a law quantified over its arguments is a dependent function into `Bool`.

**Alias and definition.** L2.7 (a definition is a concept) is his: "a name is a concept, a collection
of types is not" (D-2026-10-13-p). An alias names a structure we use before we know what it is for,
`Maybe (A : U) = { nothing : Unit || just : A }`, and expands wherever it is used, with no states
(spec 4.R7; voice note 2026-10-04 12:17). A definition promotes a structure to a theory, and what
does it is a law stating the role of each part. Only laws or a `data` give a new name a type of its
own (spec 4.R4); a bare product or function type is written as an alias, or in place. A `data`
gives each constructor freedom, and freedom says nothing of what a constructor is for: a `data`
none of whose constructors has a law of its role is a collection, written as an alias of a sum, and
the checker rejects it (spec 4.R3 as decided by D-2026-10-13-aa). "Everything has laws, it is a
matter of finding them" (his, D-2026-10-13-t), usually in the place the thing holds in a known
structure: `Unit` is the terminal object, `Empty` the initial one, `Bool` a Boolean algebra, `List`
the free monoid, `Nat` an ordered commutative semiring. The files of `lib/core/structures/` state
those structures and `lib/core/core.lut` claims them for the core's types. In `ebnf.lth` the eight constructors of a
grammar's right-hand side (`eps`, `lit`, `seq`, `alt`...) get their roles from the laws of `Derives`,
one law per constructor: `EpsEmpty` says that `eps` derives exactly the empty list.

**No loose functions.** A function is a value of a defined function type, a theory, and a function
without laws of its own is written as the expression itself, as an alias, or as the model of the
singleton theory whose law is its formula (his rule, D-2026-10-07-e, and his reading,
D-2026-10-07-g). The rule is spec 4.S17, implemented as a report; helper functions in theory
files are reported and not rejected (D-2026-10-13-x). The singleton theory is a reading and is not
written out: a theory with a single model becomes a definition, with laws only for what
characterizes it (D-2026-10-13-aa).

Read as a type, a value is the type with one inhabitant: `4` is `{ n : Int | n == 4 }` (spec 4.S5).
The difference between types and values is how far a name is determined.

## 4. A value is a model

A definition `x : T := t` gives a name a body; if `T` is a theory, the value is a model of it, and
the laws of `T` are its obligations. From `lib/core/core.lut`, where the core's types claim the
theory that says what each is:

    unitIsTerminalModel : Terminal Unit (structural Unit) := { point := unit }
    boolIsABooleanAlgebraModel : BooleanAlgebra Bool (structural Bool) :=
      { top := true, bottom := false, complement := not, meet := conj, join := disj }

The second argument of each theory, `structural Bool`, is the equality the carrier is taken under,
its own structural `==`. For each model `core.lut` also writes the claim as a law, such as
`BoolIsABooleanAlgebra`, whose model is a defaulted parameter so that a test can put a broken model
in its place (the controls of section 6).

**Theory files and model files.** L2.6 (a theory file holds types, declarations and laws, and each
model lives in a file of its own) comes from his proposal to separate files with theories from
files with models, in the spirit of C++ headers and implementations, so that different models can
be written in different files (D-2026-10-13-i). A theory file has the extension `.lth`, and an `extern`,
an action or a model value written in one is an error; a model file is a `.lut` (spec 12.S23). A model's claims are certified against its theory. The design is that a file is read when some
demand needs it, a model file at the first demand for one of its names (L11.7 (a file is read
when some demand needs it), his); spec 12.S21 is decided, and the loader still reads every import at once
(spec 8.S7). An import line names what enters with its theory, `import "world_model.lut"
host : HostConsole` (L6.14 (an import line names what enters with its theory); spec 12.S22), and the
importer sees the model only through that theory, so its representation stays private and another
model can replace it (L6.12 (an importer sees a module only through the theory it gives the module as type)). An algorithm is written against a theory,
never against one model: a function of any model of it, certified for each model it is used with
(L6.13 (an algorithm is written against a theory, never against a model)). This is where L6 (one function, many specimens, chosen by the performance the demander
asks for) begins: equivalent models are specimens, and choosing among them is the planner's work
(spec 9), which comes after certification (D-2026-10-13-ad).

**One name per concept.** In the core each concept has one name, and a use is resolved by the model
the type of its arguments names (D-2026-10-18-b; spec 4.R13): `eq` of `Object`, `d` of `Metric`,
`+` and `*` at the ring of `Int` or at the doubles. A carrier with two models is two types, and the
conversion between them is explicit. A name that two models at one type leave ambiguous, or that no
model gives, is an error that names the field, the type and the models. `docs/concepts.md` section 4
gives the rule and its reasons.

**The declaration, the hole.** `x : T` with no body is at once an axiom, an input of the program, an
external function, a pending definition and dead code; nothing executes until it is defined
(L2.1 (a declaration without a body is a first-class hole)). A hole of a defined type is a parameter, `sigma : Float64`, and what depends on it does not
reduce until it gets a value (spec 4.R2); `luthier run --set sigma=2.5` gives it one, for a hole of
type `String`, `Int`, `Float64` or `Bool` (spec 12.S18). This is "you do not execute code until it is defined", of
the voice note 2026-05-30 18.09.57 [00:53]. `extern` fills a hole with a body in another language
(L2.4 (`extern` inhabits a hole with a body in another language)); it is a name of the core whose application holds a route to a host function, read when a
demand reaches it (spec 3.S39, 3.S40).

**Declared, defined, computable.** Luciano, 2026-10-07 (chat 182f2465): the sum of two reals cannot
be computed, but it can be defined. A value is of one of three kinds.

- A *hole*: a declaration, the claim with no body. `Real`, the ideal, which no interpreter fills.
  Nothing reduces; the laws are stated.
- A *procedure*: a body whose normal form is a function over an infinite domain. It answers every
  finite question and reduces when asked one. A real as a Cauchy sequence of rationals, applied to
  a precision, gives a rational, and the sum of two such reals reduces at any precision
  (`examples/cauchy.lut`, at the tag `v0.1-final`). What never computes is their equality: two
  sequences with one limit are equal by a law that no finite observation decides.
- A *datum*: a body whose normal form is a literal or a constructor, with `==`: an `Int`, a
  `Float64`, a value of a `data`, a function from a finite domain, which is a table.

The line is how many observations an answer needs, and the size of the type does not draw it.
`Int` is infinite and each of its values is a datum; what does not compute over `Int` is "for
every n", which is induction, the proof layer's, and version 0 samples it. `Bool` and `Fin n` are
finite, and over them everything computes, the equality of functions included, so a law over them
is certified on every case. Declared is defined implicitly, by properties; defined is defined
explicitly, by a body; computable is a body that reduces to a datum.

**The ideal and what runs it.** L13 (the ideal is realized with a guarantee): code is written over
`Real` and run over `Float64`, whose values refine `Real` (spec 11.R1); `Real` stays the ideal,
declared and never run, and the Cauchy reals are one more realization beside `Float64` (his choice,
D-2026-10-07-c). The arrow goes one way. A double passes where a real is expected, but a function on
doubles does not pass for a function on reals, since a function type reverses the order of refinement on
its domain (spec 4.R9), and the rounded law is a different law from the exact one. His example is the
exponential as a theory, the functions with `f (x + y) == f x * f y` and `f 0 == 1`, written once
over a number model, ideal on `Real`, run on `Float64`, with a Taylor sum and the host's `exp` as
two of its models (D-2026-10-07-b; `examples/exp.lut` at `v0.1-final`).

## 5. Laws and equality

A law states a mathematical property of the operations it constrains; a second implementation
checked against the first only shows consistency, and the native definition is one more model of
the law (L9.2 (a law states a mathematical property of an operation); spec 4.R10). That two models agree is a corollary of the laws, useful to tighten a
tolerance, and a theory whose only laws compare it with another implementation is to be reported as
consistent and not characterized (spec 4.S20, decided and not implemented). Laws accumulate, and need not determine the
operation (spec 5.S1).

**Levels of equality.** L3 (equality comes in levels, and each object carries its own): definition
`:=`, the identity proposition, decidable `==` and definitional `≡` are four things (L3.1 (definition, identity, decidable equality and definitional equality are different things)). `≡` is
what one checks with a pencil. `==` exists only where equality is structural: on `Int`, `Float64`,
`String`, `Unit`, `Empty`, and on products, sums, `data` and subtypes built from them, never on a
function type (spec 4.R8). A law that compares functions receives its equality from outside: as
an argument, or as a field of the theory it belongs to. An *object* is a type with its equality (Terms; D-2026-10-12-ak):
`Object` in `lib/core/structures/equality.lth` asks for an equality that is an equivalence relation;
`Structural`, in the same file, adds that every function respects it (`Substitutive`), which only
`==` gives; an observational equality,
such as alpha-equivalence of terms or doubles within a tolerance, is preserved by the operations of
the theory it belongs to, each one stating so (D-2026-10-13-z; `AlphaCongruent` in `term.lth`). The identity
proposition, a type whose values are proofs, belongs to the proof layer, absent from version 0; at
the level of acts `x = t` is an alias. The other equivalences his voice notes ask for (2026-05-30
18.01.53 [02:42]) are types on top: an isomorphism is two functions and two laws saying that each
undoes the other; equality within a tolerance is where cost enters (G2 (laws are valued in cost: one logic, extended to the non-negative reals), his
second eureka); equality in distribution is a test that does not tell two samplers apart. `docs/concepts.md` section 3
sets out the levels of equivalence and the three planes of the core.

**A check is made once.** Luciano, 2026-10-06 (`sonolocalizacion/Lucianos ideas dir/funcion de los
tipos en Luthier.txt`): a program should never check the same thing twice. Belonging to a type is
the certificate that a value passed the check the type states, so a check records its result by
giving the value a finer type, and nothing downstream checks it again. It is the rule of one name
per concept (`docs/rationale/07-characterizations.md`) applied to facts. It acts at three moments.
When a program is certified, a law tested on a name is recorded in a certificate and accepted by
hash afterwards (spec 6.S8). When a program runs, a condition refines the variable it tests inside
its branch (spec 4.R11, decided and not implemented), and a check is written once, in the form
that explains its failures, its poorer forms derived (spec 5.S9). At the boundary of a program, a
check about the world refines the content it read, since the file may change between check and use
(spec 5.S12, decided). How much the type of a result should say depends on what knowing it again costs. For
`y = sin x` the type can be a real, a real in [−1, 1], or `sin x` itself; the bound is useful and
cheap. For `b = mapOpt b0 f x`, the optimum of `f` on the data `x` from the start `b0`, finding it is
expensive and a local optimum depends on its start, so the right type is indexed by every input. A
cheap result carries its bound; an expensive one carries its inputs and its witness.

## 6. Certification by testing

A *certificate* records that a law was checked, with its *grade*: *proved*, by a theorem cited or a
library's guarantee; *exhaustive*, on every case; *cases*, on chosen cases; *sampled*, on a sample
from a stated distribution; *assumed*, not checked (Terms). The law is the proposition; a
*certifier* is a method that produces evidence for it, and one law may have several (L9.1 (a law is the proposition and a certifier a method that produces evidence for it)). Which
one applies depends on what the law admits: a theorem is cited, a finite domain is enumerated, an
infinite one is sampled (L9.5 (the certifier is chosen by what the law admits)). The grade names what the certifier did: in `lib/core/core.cert.json`
the claim that `Bool` is a Boolean algebra is recorded as sampled and the claim that `List` is the
free monoid as cases. `docs/concepts.md` section 6 says what a sample tells and section 6.5 how a
grade is read.

`test` is a function of `test.lth` with named arguments: the law's name, a mode, and optionally the
number of cases, the size, the seed, the bindings, the budgets and whether the line is a control
(spec 7.S20). A top-level `test` line is a datum the module keeps; running it is an action on
Luthier's own store, which may be repeated and memoized (spec 7.S20; L4.11 (an action on Luthier's
state is idempotent and an action on the world never is)). A certificate is identified by a hash
over its dependency cone, the definition and everything it refers to; it is frozen, and a later
check issues a new certificate that supersedes it, both kept (L10.4 (a certificate is identified by a hash over its dependency cone and is frozen); P3 (keep the original evidence
and its corrections)). Only a certifier can build one, as only the kernel's rules build a theorem
in the LCF provers, the Logic for Computable Functions of Milner (L10.10 (only a certifier builds a certificate)). Certification is the
default: demanding a value demands every certificate in its cone (L10.6 (certification is the default)), and `run` refuses a cone
with an uncertified name (spec 12.S17).

A test line lives in a test program, `x.test.lut`, one of the three kinds of file (section 4). From
`docs/concepts/tape.test.lut`, whose model `tape` and theory `Tape` are in the same directory:

    import "test.lth" test SampledMode
    import "generators_model.lut" linear sameOrNat
    import "tape.lth" Mark Tape MetresWithin
    import "tape.lut" tape markIsAMetricModel

    test "Tape" (SampledMode linear) (cases <- 200) (size <- 50000) (seed <- 20261021) (profile <- models)

The line names the law, gives the mode (`ExhaustiveMode`, or `SampledMode` with a generator's
placement) and, by named arguments, the cases, the size that bounds the integers drawn, the seed,
and the profile that says which model each parameter of the law is drawn from. Because `Tape` is a
conjunction of four laws, the tester runs each conjunct on its own and gives it an entry (spec
7.S22). `luthier test docs/concepts/tape.test.lut` printed, among other lines:

    Tape: conjunction of 4, 800 cases, sampled (known)
      conjunct ReadingAdds t: sampled (seed 20261021, size 50000, placement ignored), 200 cases, sampled (known, ...)
      conjunct MetresWithin t: sampled (seed 20261021, size 50000, placement ignored), 200 cases, sampled, worst ratio 0.414938 (known, ...)

`known` says the store already held the entry for this cone, seed and number of cases, so the line
was not run again unless `--deep` asks (spec 7.S13). The entries go to `tape.cert.json`, beside the
file that makes the claim, `tape.lut` (spec 12.S10; L10.12 (a store lives beside the file that
claims what it certifies)). `luthier certify` runs the lines of several test programs, each in its
own process. A law over `Int` under `ExhaustiveMode` is reported as not run, since `Int` is infinite
(spec 7.R3).

A passing law shows nothing unless it could have failed, so the same test line is repeated with a
model broken on purpose, a control, which the law must refute (L9.14 (a law is evidence of nothing
until a wrong model refutes it)). The tape's control is a tape whose hook adds one millimetre to
every reading:

    hooked : Tape := { reading := fn a b { tape.reading a b + 1.0 } }
    test "Tape" (SampledMode linear) (cases <- 200) (size <- 50000) (seed <- 20261021) (profile <- onHooked) (control <- true)

and `luthier test` prints `control of Tape: ... refuted at ReadingAdds t: t = hooked, ...: the
control passed`. `docs/concepts.md` sections 6 to 8 explain the generators, the grades, the controls
and the certificate with its cone. The numerical laws that bound a rounding error (`Within`, in
`laws.lth`) are its section 9.

## 7. The world

`W` is a keyword of the core, the counterpart of `U` (his, D-2026-10-13-b): definitions live in the
universe, timeless, copied, compared and memoized; actions act on the world. A program never
constructs a `W`; the token enters at `main` or in the session, has no `==`, and each value of it is
used once (the model's rules, accepted in D-2026-10-13-e; the idea of a value used once is Clean's
uniqueness types). There is one world (his, D-2026-10-13-a): its parts, a file or the standard
output, exist in Luthier's representation of it, and whether two parts are independent is a theory
in a library, never something the language imposes.

An *action* is a function that takes the token and gives the next token with a result, of type
`W -> ... -> W * A`; a function whose type mentions no `W` has no effect (spec 10.S3; `Action` in
§1 of `world.lth`). L4.7 (a definition's result depends only on its inputs) is what lets evaluation
proceed in any order the dependencies allow. A reading is an action too (L4.10 (an observation is itself an action)), whose law says it
changes no place: `ReadChangesNothing` in §4 of `world.lth`. Mutation is a parameter split into its
value before and its value after, and updating in place is the planner's optimization when nothing
else reads the earlier value (L4.5 (a mutable parameter is two variables, before and after)).

`examples/hello.run.lut`, the first program with an action (the comment lines of the file left out):

    import "world_model.lut" HostConsole host : HostConsole

    main (w : W) : W * Unit := host.print w "hello, world"

The import line names the model `host` and the theory `HostConsole` it is checked against (section
4). `world.lth` states the console twice. `Console S` is its description over a representation `S`
of the world, pure functions that say what `print` and `readFile` do to the state, with four laws,
among them that printing appends a line to the standard output and changes no other place
(`PrintAppendsALine`, `ReadChangesNothing`). `Host S` is the other side, the actions themselves,
with the token in front: `print : W -> String -> W * Unit`. In `world_model.lut` `console` is the
description and `host` is a record of `extern` routes to Python functions, certified against
`console` along one chain of tokens (D-2026-10-13-a; `agreement` in §5 of `world.lth`). Both
files are in the repository; reading them is the quickest way to see a theory and its two models
side by side.

`luthier run examples/hello.run.lut` gives `main` a token `w0`. Reduction looks up `host`, takes its
component `print`, an extern route, and finds it applied to two closed arguments, so the host is
called (spec 3.S18) and gives back `(w1, unit)`: the next token and the empty result. The route is
opened only now, when a demand reaches it (L11.7 (a file is read when some demand needs it)), and, since 788b7f4, a host action whose theory
states its agreement with its description (`Host` in `world.lth` §5) is first validated at its first
application in the run, with the program's own arguments, refused if the host disagrees, and recorded in
the model's store when it agrees (spec 10.S10): "si el tipo no sigue la ley no se aplica el calculo"
(his words in L11.2 (an extern is validated against the laws of its type)). The run prints `hello, world`.

Before evaluating, `luthier run` refuses to start if a name in the cone of `main` is not certified
or is provisional, and says which (spec 12.S17); `--accept GRADE` lowers the weakest grade a
certificate may have to serve, and `--accept assumed:NAME` runs a provisional extern, or runs past a
refuted law, as assumed, warned at every run. After the run it appends an entry to
`examples/hello.run.json`, beside the file: the parameters, the output, the hash of the cone, the
interpreter's revision and the certificates read (spec 12.S18). A run is cut by `--fuel` or
`--time-limit` and the cut is recorded as unfinished.

In a block, the left of `<-` is a pattern against the action's `W * A`, and a bare name binds the
token when the result is `Unit` (D-2026-10-13-ag). An example written for this guide, *proposed* and
not run (the real one is in section 9):

    main (w0 : W) : W * Unit := {
      (w1, s) <- host.readFile w0 "input.txt"
      host.print w1 (match s { nothing -> "no input" ; just t -> t })
    }

The token threads the two actions, so their order is an edge of the graph, as any dependency is.

## 8. The program as data, and the pattern of the first files

A program is a value of Luthier (L7.4 (programs build, inspect and run other programs)). `term.lth` §1
defines the kernel term as `data`: `Term` with `Var`, `Lit`, `Lam`, `App`, `Match`, `Record`, `Proj`,
`Let` and the rest; `Pattern`; `Act` with `Declare`, `Define` and `Datum`; and `Program`, a list of
acts (spec 3.S29). A block elaborates to nested `Let`s, local definitions whose name equals its
value inside the body (D-2026-10-13-aa). `quote { t }` gives the `Term` of `t` (spec 2.S20, decided).
Evaluating cannot change the running program (spec 3.S35), which answers two of his voice notes:
"code is the first element" (2026-05-29 14.36.03 [02:38]) and the impossibility of self-hacking
(2026-08-31 19.57.14 [00:11]).

The rules of reduction are a theory, `Reduction` in `term.lth` §5: a model gives `step`, which takes
a program and a term to the term one weak-head step later, and answers `nothing` once no step
applies; `reduce` iterates it within a budget of steps (spec 3.S33).
The model in `term_model.lut` is the interpreter written in Luthier; the Python evaluator
`kernel.py` is a second specimen of the same theory, by L14.3 (the host implements what Luthier
states and is certified against it). Luthier's grammar is likewise a value, `luthierSyntax :
WellFormedEbnf` in `grammar.lth`, from which the grammar of spec 2.S9 is generated; `ebnf.lth`
states what a grammar derives as the theory `Derives`, and `backtrack` in `ebnf_model.lut` is a
model of it.

These first files fixed a pattern the others follow (D-2026-10-13-r):

- a theory is declared at a record type of its operations;
- each law is a predicate over a model `(m : T)`, after the theory's own parameters;
- the theory is defined as the conjunction of its laws, `T := ...`;
- every constructor of a `data` has a law of its role (L2.7 (a definition is a concept));
- where the laws determine a function, the file states the domain on which they do and the
  argument of uniqueness (`WellFormedEbnf` and the closing comment of `ebnf.lth`);
- a law that needs related values quantifies over a subtype with its own generator, as
  `EqualPair` of `lib/core/structures/equality.lth` draws pairs that are equal.

Models are named values in `.lut` files, and the Python specimens are certified against the
theories, so their errors show (writing `kernel.py` found four defects of `term.lth`,
D-2026-10-13-ab). Many theory files open with an index of their sections, each done or to do (`numbers.lth`,
`certification.lth`, `plan.lth`).

The trust is layered, by L7.3 (four layers, each trusted in its own way). The kernel is small enough
to check by hand. The libraries and the interpreter written in Luthier are certified against the
laws of the kernel. The host is a specimen, and the planner gives advice that the plan records. The destination is everything in Luthier but a core
that reduces kernel terms, computes the primitives and calls the externs (D-2026-10-13-v, on the
model's recommendation; his aim of 2026-10-08, D-2026-10-08-c, was this minimal kernel).

## 9. Two programs

The first is executed by hand, to see reduction. The second is read through, to see what a program
that does something looks like in this language.

### 9.1 Executed by hand

`tests/eval/factorial.lut`:

    Peano : U := data { zero : Peano; succ : Peano -> Peano }
    factorial (n : Peano) : Int := match n { zero -> 1; succ k -> (countDown n) * (factorial k) }
    countDown (n : Peano) : Int := match n { zero -> 0; succ k -> 1 + countDown k }
    answer : Int := factorial (succ (succ (succ (succ zero))))

`factorial` uses `countDown`, defined after it; the order of the text does not matter (section 2).
Elaboration turns the parameters into lambdas (spec 2.S12), so `factorial` is
`fn n { match n { zero -> 1 ; succ k -> countDown n * factorial k } }`, and the infix `*` and `+` into
applications of the functions that `core.lut` binds to those operators at `Int` with `operator`, whose bodies are the host's primitives (`intTimes` is `primitive "*"`). Reduction uses four rules, each a definitional equality: *delta*, a defined name
in head position becomes its body (spec 3.S15); *beta*, a lambda applied becomes its body with the
argument for its parameter, `(fn x { t }) a ≡ t[a/x]` (spec 3.S14); *iota*, a `match` on a
constructor takes the arm that fits, its variables substituted (spec 3.S16); *prim*, a primitive
applied to literals computes (spec 3.S17), and asks for its arguments, left first, until they are
literals. The strategy is weak head: the head of an application and the scrutinee of a `match` are
reduced first, and nothing is reduced under a binder. Write `n1` for `succ zero` and `n2` for
`succ n1`.

    factorial n2
    ≡ (fn n { match n { zero -> 1 ; succ k -> countDown n * factorial k } }) n2      delta
    ≡ match n2 { zero -> 1 ; succ k -> countDown n2 * factorial k }                   beta
    ≡ countDown n2 * factorial n1                                                     iota, k := n1

`*` unfolds to its primitive (delta), which asks for its left argument:

    countDown n2
    ≡ match n2 { zero -> 0 ; succ k -> 1 + countDown k }      delta, beta
    ≡ 1 + countDown n1                                         iota, k := n1
    ≡ 1 + (1 + countDown zero)                                 the same three steps on countDown n1
    ≡ 1 + (1 + 0)                                          delta, beta, iota on countDown zero
    ≡ 1 + 1                                                prim
    ≡ 2                                                    prim

then for its right argument, by the same steps:

    factorial n1
    ≡ countDown n1 * factorial zero         delta, beta, iota
    ≡ 1 * 1                             countDown n1 as above; factorial zero by delta, beta, iota
    ≡ 1                                 prim

and the whole is `2 * 1 ≡ 2`. Each line is a definitional equality, so the chain shows that
`factorial n2 ≡ 2`; mathematics does not execute, it checks equivalences (voice note 2026-05-30
18.01.53 [01:47]). `answer` reduces the same way to 24, which is what `luthier eval tests/eval/factorial.lut answer`
prints, `24 : Int`, with a line that lists the states of the cone (`tests/test_elaborate.py`). The
evaluator runs this program without the checker (D-2026-10-13-u). `luthier check
tests/eval/factorial.lut` rejects it: `Peano` is a `data` whose constructors have no law of their
role (spec 4.R3), and `factorial` has no laws, so nothing in it could be certified. A lawful version
would use the core's `Nat`, which is the subtype `{ k : Int | 0 <= k }` of `Int`, claimed an ordered
commutative semiring in `core.lut` (`naturals`, `OrderedSemiring` of
`lib/core/structures/order.lth`), and would state what characterizes the factorial before giving its
body.

### 9.2 Read through

`examples/sonolocalizacion/validate_graph.run.lut` reads the two CSV tables of a distance graph, the
input of a fit of positions in sonolocalización, and prints the first invariant of the graph that
fails, or a summary of a valid one. It is a run, an executive file (section 4), and the definitions
it uses are in the model file `validate_graph.lut` beside it. The imports of the two files show the
layering of sections 3 and 4:

    import "world_model.lut" HostConsole host : HostConsole
    import "distance_graph.lut" readGraph
    import "validate_graph.lut" report

    import "numbers.lth" Doubles
    import "numbers_model.lut" doubles : Doubles
    import "arrays.lth" RankFloor
    import "distance_graph.lut" DistanceGraph ValidDistanceGraph ValidGraph firstViolation describe ...

The first three lines open the run, the next four open `validate_graph.lut` (the last list is
shortened). A theory file (`.lth`) gives `Doubles`, the theory of the doubles, and its model file
gives the model `doubles`; the program is written against the theory and sees only what the theory
exposes (L6.12 (an importer sees a module only through the theory it gives the module as type)).
`distance_graph.lut` is a model file that holds definitions with their own invariants, and the
importer takes them by name.

The program, in the order a reader should take it, which is not the order of the text (spec 3.S1).
In the run:

    graphDir : String

A run parameter, a hole with no body: `luthier run ... --set graphDir=examples/sonolocalizacion/A/graph`
fills it (spec 12.S18), and the run is refused without a value. In `validate_graph.lut`, a
criterion, the rank floor below which a direction counts as unseen by the distances:

    rankFloor (g : DistanceGraph) : RankFloor := toFloat64 (3 * g.nodes.nRows) * doubles.epsilon

Its comment says why it is a function of the graph and not a number in the code: a criterion is a
parameter (P11, every criterion is a parameter, never a constant in the code), here with the value
the earlier version used so that the count is the same. `graphSummary` builds the text for a valid
graph, and takes a `ValidDistanceGraph`, a subtype of the graphs, `{ g : DistanceGraph | ValidGraph g }`
(section 3); so `report` may call it only on a graph that passed `ValidGraph`, and the `if
ValidGraph g` in its branch is the refinement of section 5 (spec 4.R11), written by hand because
the checker does not yet narrow a type by a condition. `report` asks `firstViolation`, which gives
`Maybe Violation`, a sum with a record on one side (`{ schema : String || inRow : RowViolation }`),
and `match` takes it apart: `nothing` is a graph with no violation, `just v` is described by
`describe`.

The only place the world enters is `main`, in the run:

    main (w : W) : W * Unit := {
      (w1, read) <- readGraph w graphDir
      host.print w1 (match read {
        nothing -> "FAIL ReadGraph: " <> graphDir <> " has no nodes.csv and measurements.csv that read as typed tables" ;
        just g -> report g })
    }

`readGraph` is an action of `distance_graph.lut`: it takes the token, reads `nodes.csv` and
`measurements.csv` with `host.readFile` (each read an action, the token threaded through
`<-`), parses each with the codec `csv` of `tables_model.lut`, and gives `W * Maybe DistanceGraph`.
In `main` the pattern `(w1, read)` binds the new token and the result; `host.print` takes `w1`
and gives back the last token, which is what `main` returns. Everything else is a pure function of
values, so it reduces in any order the dependencies allow (L4.7 (a definition's result depends only
on its inputs)), and the order of the two actions is the order of the tokens. The reads are an
observation of the world, so a file that changes between two runs is a different input, and the
demand reads it when it reaches the extern and not before (L11.7 (a file is read when some demand needs it)). The graph in `A/graph` is a table
of nodes (a name, a prior mean `x y z` and a standard deviation per coordinate) and a table of
measured distances between pairs of nodes by row index.

The last record of this run in `validate_graph.run.json`, from 2026-10-22, holds one line of output:

    valid: 10 nodes, 22 measurements, 21 distinct pairs; directions the distances do not see: 14 (of which 10 are the heights and 3 the rigid motions of the plane)

(Luciano runs this program; this guide quotes the record and did not run it.) The ten heights and
three rigid motions of the plane are the directions the distances cannot see by construction, and
the fourteenth is left to the prior. A graph that breaks an invariant prints the first one broken,
with its row.

What the program shows. The invariants are Boolean laws over a concrete graph (`NoSelfPairs`,
`DistancesPositive`), joined by `and` in `ValidGraph`; the check that explains a failure is
`firstViolation`, the form that carries a row, and the poorer form `ValidGraph` is its derivation, as
spec 5.S9 asks; a law relates them, `ReportsValidity` (a check reports nothing exactly when the
graph is valid). The program is a plan until `main` is demanded: nothing in it ran when the file was
read, and `luthier run` gives `main` its token, after it has checked that the cone of `main` is
certified.

## 10. What stays outside the kernel, and where each piece comes from

Outside the kernel:

- Numbers beyond the primitives, vectors and matrices: libraries built from the kernel, numpy their
  representation in the host (spec 3.S21: a numpy array is a value of `Fin n -> Float64`). The
  reals by construction are a library too.
- What the host computes: values given by `extern`, never types (spec 4.R5). `provisional`, a named
  argument of `extern`, is the escape hatch for working in a hurry, recorded as debt.
- Probability, costs, the world's parts, checks: libraries, of which the core asks only an interface
  (spec 5.S10, 10.S5; L7.5 (what a library can decide, the core does not)).
- Control flow: `if` is a `match` on `Bool`, a loop is recursion, a sequence is a dependency, and
  there is no inheritance.

Where each piece comes from:

- From the lambda calculus, terms and reduction (section 9).
- From Martin-Löf type theory, the kernel: dependent functions and pairs, sums, the empty and unit
  types, inductive types, the universe; and G0 (type theory is the guide).
- From Lisp, the program as data (section 8).
- From C++, the separation of declaration and definition, here the hole, and of header and
  implementation, here theory files and model files (D-2026-10-13-i); and templates, here functions
  over `U`.
- From ML, opaque signatures, here privacy by ascription to a theory (D-2026-10-13-c).
- From the LCF provers, an abstract type of theorems, here certificates only certifiers build.
- From Haskell, actions as values composed by laws while nothing runs; from Clean, the world used
  once.
- From Knuth, that an algorithm is written for a person to follow with a pencil.

## 11. Open

- The proof layer: a recursor that guarantees termination, the identity proposition, a hierarchy
  of universes (spec 3.S8, 3.S11).
- The algebra of costs, and with it laws valued in `Cost` (O1, the algebra of costs; spec 5.S2,
  suspended). D-2026-10-25-a settled parts of it, which `docs/concepts.md` sections 6.5, 9 and 10
  report, and the execution of that audit is building on the core.
- How a type names its equality (O2, the type with its equality as the base of every theory):
  answered in part by `Object` and by resolution by type (sections 4 and 5).
- The kind of a hole in the elaborated form: input, extern, pending, axiom (O9).
- The demand and the planner (spec 8, spec 9): a demand's cutoff and the choice among specimens are
  decided and suspended (spec 8.S1, 9.S5 to 9.S12); `luthier run` takes a few options of the
  demand today (`--accept`, `--bound`, `--combine`, `--strategy`), and nothing chooses between
  specimens (spec 9.S2).
- The derivation of a value, and what two derivations share to be one for a demand (O13;
  `docs/concepts.md` section 12.4).
- *Proposed*: whether a definition carries a text field, so that a program reads as a document (an
  open item of the old guide, kept).

## 12. What this rewrite left out

The old guide is in git at e7d6f9a. Left out, each for its reason:

- The many worlds, one per pointer, with no order between them: replaced by one world whose parts
  are a representation (D-2026-10-13-a).
- A declared value filled by another file of the same name, and the program that declares `exp` for
  another file to fill: retired, a model is a named value of its theory (spec 12.S8 retired by
  D-2026-10-13-o).
- "`Program` and `Term` as data are not in version 0": they are, in `term.lth` (D-2026-10-12-x).
- The certificate read as an update of a prior that the law holds: superseded by his correction on
  what a sample gives (L12.6 (cost has two readings, a distance and that probability); D-2026-10-13-n).
- The executable kernel of three items and the reliance on a `File` type: replaced by the core of
  D-2026-10-13-v and the console of `world.lth`.
- The doubling example (`doubleA`, `doubleB`, `Double`) of the old section 8: a `data` with no law of
  its constructors' roles is rejected by spec 4.R3 now, and the example carried the old syntax; the
  hand execution moved to a program the interpreter runs today, and certification is shown on the
  kernel's own models.
- The old grades (point, bounded, witnessed): read through the five of the Terms (spec 1.S12).
- The trace, the comparison of traces by consequence and by cost, and classes of machines: left by
  spec 10.S14 to the form of the record of a run, which spec 8 decides (8.S15).

What draft 2 (2026-10-26) found stale in draft 1 and changed:

- Sections 3 and 4 quoted `kernel_laws.lth` and `kernel_models.lut`, which no longer exist, and a
  monoid without the carrier's `Object`; they now quote `lib/core/structures/`, `properties/` and
  `core.lut`, where the core's types claim their theories.
- Section 4 said the loader reads a model file when a demand first needs it; spec 12.S21 is only
  decided and the loader reads imports at once.
- Section 6 said `luthier test` had no certificate store and `run` did not refuse a cone for lack
  of one. Both exist (spec 12.S10, 12.S17); the section now shows a test program, its output and a
  control. It also said `booleans` was certified on every case; the core's store records the Boolean
  algebra of `Bool` as sampled.
- Section 7 said a host extern is validated in the language designed and not yet; since 788b7f4 it
  is validated at its first application in a run (spec 10.S10).
- Section 9.1's program, `tests/eval/factorial.lut`, now names its type `Peano`, and the core's `Nat`
  is a subtype of `Int`, no longer a `data`.
- Section 9.2 described `validate_graph.lut` as one file with `main` and a default `graphDir`; since
  D-2026-10-16-e the run is `validate_graph.run.lut` with `graphDir` a hole, and the old command
  `python3 -m luthier.cli run` was replaced by `luthier run`. The "few minutes" timing of
  2026-10-14 is dropped, since the guide has no measurement of the interpreter as it stands.
