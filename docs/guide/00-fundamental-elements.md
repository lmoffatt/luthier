# The fundamental elements of a Luthier program

Rewritten on 2026-10-13 by Claude Opus 5.5 and finished on 2026-10-14 by Claude Sonnet 5.5 from the guide of 2026-10-04 (last changed at e7d6f9a;
git keeps it), against the specification in `docs/spec/` (chapters 1 to 5, 10 and 12),
`docs/principles.md`, the theory files of `src/luthier/lib/` and the two programs of `examples/` the rebuilt interpreter runs, at commit 2d7e495. The old guide
was written before the specification: it cited chapters by numbers that have since changed, used a
syntax that was replaced (`\` lambdas, `< >` sums, `let`), and described an interpreter that was
started again from zero (D-2026-10-13-h). This one is the reading guide for someone meeting
Luthier now: the few ideas a program is made of, in the order to think them, and one program
executed by hand, and a second walked through. The rules are in the specification. Where this text and the specification
differ, the specification holds; where the specification and a theory file differ, the theory file
holds, by L14.6 (Luthier's own theories are written first and are the authority). Ideas that are
Luciano's say so and cite their source: his voice notes in `record/audios/`, his chats by id, his
words as quoted in `record/decisions.md`. What the model adds beyond the sources is marked
*proposed*. Section 12 says what was left out of the old guide and why.

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
and Bayesian evidence, a likelihood, is another thing (L12.6, cost has two readings, a distance and
that probability; D-2026-10-13-n).

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
is allowed (L4.2, the text says which binding a name means). The two acts share one law, his
annotation in L4.3: after the act the name equals the term, after `:=` for good and after `<-` until
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
  non-negative reals with infinity, 0 for true and ∞ for false). Today every law is Boolean; costs
  wait for a library and a case that needs them (spec 5.S1, 5.S2; D-2026-10-13-aa).
- A *theory* is a structure together with its law; a *model* is a value of a theory whose law has
  been certified.

How a theory is written, in the pattern of the first theory files (`src/luthier/lib/ebnf.lth`,
D-2026-10-13-r): declare it at its structure, a record type of its operations; write each law as a
predicate over a model; define the theory as the conjunction of its laws. The monoid, from §4 of
`kernel_laws.lth`:

    Monoid (M : U) : { neutral : M, combine : M -> M -> M }
    LeftNeutral (M : U) (m : Monoid M) (x : M) : Bool := m.combine m.neutral x == x
    RightNeutral (M : U) (m : Monoid M) (x : M) : Bool := m.combine x m.neutral == x
    Associative (M : U) (m : Monoid M) (x y z : M) : Bool :=
      m.combine (m.combine x y) z == m.combine x (m.combine y z)
    Monoid (M : U) := LeftNeutral M & RightNeutral M & Associative M

The first line declares `Monoid`, a function from a type `M` to a record type, with no body: this is
L2 (declare, then define, then inhabit). The three laws mention `Monoid` while it is only declared,
which spec 4.R1 allows (a declaration may refer to names that are merely declared). Their parameters
before the colon are curried, so `LeftNeutral` is `fn M { fn m { fn x { ... } } }` (spec 2.S12).
The last line gives the declared name a body whose type is a law over it, and so defines a type:
the records `{ neutral, combine }` for which the three laws hold at every argument, by spec 4.R6
(the body of a declared name is a value of its type or a law over it) and 4.S7 (the type of the
body decides which). A theory with parameters repeats them in that last line, and each law takes
them first and the model after (spec 4.R6; D-2026-10-13-o). `&` joins laws (spec 5.S6). The loop
`Monoid`, its laws, `Monoid` is the theory of section 2. It is Hilbert's implicit definition made a
type: the type is the theory, the conditions an object must meet (the name "theory and model" is
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
the free monoid, `Nat` an ordered commutative semiring. `kernel_laws.lth` states those structures and
`kernel_models.lut` makes the core's types their models. In `ebnf.lth` the eight constructors of a
grammar's right-hand side (`eps`, `lit`, `seq`, `alt`...) get their roles from the laws of `Derives`,
one law per constructor: `EpsEmpty` says that `eps` derives exactly the empty list.

**No loose functions.** A function is a value of a defined function type, a theory, and a function
without laws of its own is written as the expression itself, as an alias, or as the model of the
singleton theory whose law is its formula (his rule, D-2026-10-07-e, and his reading,
D-2026-10-07-g). The rule is spec 4.S17, decided and not implemented; helper functions in theory
files are reported and not rejected (D-2026-10-13-x). The singleton theory is a reading and is not
written out: a theory with a single model becomes a definition, with laws only for what
characterizes it (D-2026-10-13-aa).

Read as a type, a value is the type with one inhabitant: `4` is `{ n : Int | n == 4 }` (spec 4.S5).
The difference between types and values is how far a name is determined.

## 4. A value is a model

A definition `x : T := t` gives a name a body; if `T` is a theory, the value is a model of it, and
the laws of `T` are its obligations. From `kernel_models.lut`:

    unitTerminal : Terminal Unit := { point := unit }
    booleans : BooleanAlgebra Bool := {
      top := true, bottom := false,
      complement := fn b { not b },
      meet := fn a b { a and b },
      join := fn a b { a or b },
    }

**Theory files and model files.** L2.6 (a theory file holds types, declarations and laws, and each
model lives in a file of its own) comes from his proposal to separate files with theories from
files with models, in the spirit of C++ headers and implementations, so that different models can
be written in different files (D-2026-10-13-i). A theory file has the extension `.lth`, and an `extern`,
an action or a model value written in one is an error; a model file is a `.lut` (spec 12.S23). The checker reads theory files; a model file is read only when a demand first needs one of
its names, and its models are certified against their theories (L11.7, his: a file is read when
some demand needs it). An import line names what enters with its theory, `import "world_model.lut"
host : HostConsole` (L6.14, the import names the theory it is checked against; spec 12.S22), and the
importer sees the model only through that theory, so its representation stays private and another
model can replace it (L6.12, privacy is ascription). An algorithm is written against a theory,
never against one model: a function of any model of it, certified for each model it is used with
(L6.13). This is where L6 (one function, many specimens, chosen by the performance the demander
asks for) begins: equivalent models are specimens, and choosing among them is the planner's work
(spec 9), which comes after certification (D-2026-10-13-ad).

**The declaration, the hole.** `x : T` with no body is at once an axiom, an input of the program, an
external function, a pending definition and dead code; nothing executes until it is defined
(L2.1). A hole of a defined type is a parameter, `sigma : Float64`, and what depends on it does not
reduce until it gets a value (spec 4.R2). This is "you do not execute code until it is defined", of
the voice note 2026-05-30 18.09.57 [00:53]. `extern` fills a hole with a body in another language
(L2.4); it is a name of the core whose application holds a route to a host function, read when a
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
the law (L9.2; spec 4.R10). That two models agree is a corollary of the laws, useful to tighten a
tolerance, and a theory whose only laws compare it with another implementation is reported as
consistent and not characterized (spec 4.S20). Laws accumulate, and need not determine the
operation (spec 5.S1).

**Levels of equality.** L3 (equality comes in levels, and each object carries its own): definition
`:=`, the identity proposition, decidable `==` and definitional `≡` are four things (L3.1). `≡` is
what one checks with a pencil. `==` exists only where equality is structural: on `Int`, `Float64`,
`String`, `Unit`, `Empty`, and on products, sums, `data` and subtypes built from them, never on a
function type (spec 4.R8). A law that compares functions receives its equality from outside: as
an argument, or as a field of the theory it belongs to. An *object* is a type with its equality (Terms; D-2026-10-12-ak):
`Object` in §1 of `kernel_laws.lth` asks for a reflexive, symmetric and transitive equality;
`Structural` adds that every function respects it, which only `==` gives; an observational equality,
such as alpha-equivalence of terms or doubles within a tolerance, is preserved by the operations of
the theory it belongs to, each one stating so (D-2026-10-13-z; `AlphaCongruent` in `term.lth`). The identity
proposition, a type whose values are proofs, belongs to the proof layer, absent from version 0; at
the level of acts `x = t` is an alias. The other equivalences his voice notes ask for (2026-05-30
18.01.53 [02:42]) are types on top: an isomorphism is two functions and two laws saying that each
undoes the other; equality within a tolerance is where cost enters (G2, laws valued in cost, his
second eureka); equality in distribution is a test that does not tell two samplers apart.

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
(spec 5.S12). How much the type of a result should say depends on what knowing it again costs. For
`y = sin x` the type can be a real, a real in [−1, 1], or `sin x` itself; the bound is useful and
cheap. For `b = mapOpt b0 f x`, the optimum of `f` on the data `x` from the start `b0`, finding it is
expensive and a local optimum depends on its start, so the right type is indexed by every input. A
cheap result carries its bound; an expensive one carries its inputs and its witness.

## 6. Certification by testing

A *certificate* records that a law was checked, with its *grade*: *proved*, by a theorem cited or a
library's guarantee; *exhaustive*, on every case; *cases*, on chosen cases; *sampled*, on a sample
from a stated distribution; *assumed*, not checked (Terms). The law is the proposition; a
*certifier* is a method that produces evidence for it, and one law may have several (L9.1). Which
one applies depends on what the law admits: a theorem is cited, a finite domain is enumerated, an
infinite one is sampled (L9.5). `booleans` above is certified on every case, since `Bool` has two
values; `lists A : FreeMonoid A (List A)` can only be sampled.

`test` is a function of the core with named arguments, and a top-level `test` line is a datum the
module keeps; running it is an action on Luthier's own store, which may be repeated and memoized
(spec 7.S20; L4.11, an action on Luthier's state is idempotent and an action on the world never is).
A certificate is identified by a hash over its dependency cone, the definition and everything it
refers to; it is frozen, and a later check issues a new certificate that supersedes it, both kept
(L10.4; P3, keep the original evidence and its corrections). Only a certifier can build one, as only
the kernel's rules build a theorem in the LCF provers, the Logic for Computable Functions of Milner
(L10.10). Certification is the default: demanding a value demands every certificate in its cone
(L10.6), and `run` refuses a cone with an uncertified name (spec 12.S17).

Where this stands. L9.13 is his: to design certificates, first see how the law fails
(D-2026-10-13-ad). So after `v0.2` execution comes first: the world, the externs and `run`, so that
sonolocalización runs uncertified; certificates are then designed on its laws and on how they fail.
The theories of tests and evidence are written (`test.lth`, `laws.lth`), and `luthier test` is their
first specimen: it reads the `test` lines of a file and runs each law either on every case or on a
sample. From `tests/tester/laws.lut`:

    import "test.lth" test ExhaustiveMode SampledMode
    import "generators_model.lut" linear

    NotInvolutive (b : Bool) : Bool := not (not b) == b
    PlusCommutes (x y : Int) : Bool := x + y == y + x

    test "NotInvolutive" ExhaustiveMode
    test "PlusCommutes" (SampledMode linear) (cases <- 200) (seed <- 7)

Each law is a definition whose parameters are what it quantifies over and whose result is `Bool`; the
line names it, gives the mode and, by named arguments, the number of cases and the seed. The command
has no certificate store yet, so it reports the evidence of the run and does not record it, and
`run` does not yet refuse a cone for lack of one.

`luthier test tests/tester/laws.lut` prints one line per test line, for example `AndIsOr: exhaustive,
4 cases, refuted at a = true, b = false` and `PlusCommutes: sampled (seed 7, ...), 200 cases,
sampled`. A law over `Int` under `ExhaustiveMode` is reported as not run, since `Int` is infinite
(spec 7.R3).

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
proceed in any order the dependencies allow. A reading is an action too (L4.10), whose law says it
changes no place: `ReadChangesNothing` in §4 of `world.lth`. Mutation is a parameter split into its
value before and its value after, and updating in place is the planner's optimization when nothing
else reads the earlier value (L4.5).

`examples/hello.lut`, the first program with an action (the comment lines of the file left out):

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

`luthier run examples/hello.lut` gives `main` a token `w0`. Reduction looks up `host`, takes its
component `print`, an extern route, and finds it applied to two closed arguments, so the host is
called (spec 3.S18) and gives back `(w1, unit)`: the next token and the empty result. The route is
opened only now, when a demand reaches it (L11.7), and in the language designed it is first
validated against the laws of its type, and refused if they fail: "si el tipo no sigue la ley no se
aplica el calculo" (his words in L11.2). The run prints `hello, world`.

In a block, the left of `<-` is a pattern against the action's `W * A`, and a bare name binds the
token when the result is `Unit` (D-2026-10-13-ag). An example written for this guide, *proposed* and
not run (the real one is in section 9):

    main (w0 : W) : W * Unit := {
      (w1, s) <- host.readFile w0 "input.txt"
      host.print w1 (match s { nothing -> "no input" ; just t -> t })
    }

The token threads the two actions, so their order is an edge of the graph, as any dependency is.

## 8. The program as data, and the pattern of the first files

A program is a value of Luthier (L7.4, programs build, inspect and run programs). `term.lth` §1
defines the kernel term as `data`: `Term` with `Var`, `Lit`, `Lam`, `App`, `Match`, `Record`, `Proj`,
`Let` and the rest; `Pattern`; `Act` with `Declare`, `Define` and `Datum`; and `Program`, a list of
acts (spec 3.S29). A block elaborates to nested `Let`s, local definitions whose name equals its
value inside the body (D-2026-10-13-aa). `quote { t }` gives the `Term` of `t` (spec 2.S20).
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
- every constructor of a `data` has a law of its role (L2.7);
- where the laws determine a function, the file states the domain on which they do and the
  argument of uniqueness (`WellFormedEbnf` and the closing comment of `ebnf.lth`);
- a law that needs related values quantifies over a subtype with its own generator, as
  `EqualPair` of `kernel_laws.lth` draws pairs that are equal.

Models are named values in `.lut` files, and the Python specimens are certified against the
theories, so their errors show (writing `kernel.py` found four defects of `term.lth`,
D-2026-10-13-ab). Each theory file opens with an index of its sections, each done or to do.

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

    Nat : U := data { zero : Nat; succ : Nat -> Nat }
    factorial (n : Nat) : Int := match n { zero -> 1; succ k -> (count n) * (factorial k) }
    count (n : Nat) : Int := match n { zero -> 0; succ k -> 1 + count k }
    answer : Int := factorial (succ (succ (succ (succ zero))))

`factorial` uses `count`, defined after it; the order of the text does not matter (section 2).
Elaboration turns the parameters into lambdas (spec 2.S12), so `factorial` is
`fn n { match n { zero -> 1 ; succ k -> count n * factorial k } }`, and the infix `*` and `+` into
applications of names whose bodies are the host's primitives (`core.lut` names them). Reduction uses four rules, each a definitional equality: *delta*, a defined name
in head position becomes its body (spec 3.S15); *beta*, a lambda applied becomes its body with the
argument for its parameter, `(fn x { t }) a ≡ t[a/x]` (spec 3.S14); *iota*, a `match` on a
constructor takes the arm that fits, its variables substituted (spec 3.S16); *prim*, a primitive
applied to literals computes (spec 3.S17), and asks for its arguments, left first, until they are
literals. The strategy is weak head: the head of an application and the scrutinee of a `match` are
reduced first, and nothing is reduced under a binder. Write `n1` for `succ zero` and `n2` for
`succ n1`.

    factorial n2
    ≡ (fn n { match n { zero -> 1 ; succ k -> count n * factorial k } }) n2      delta
    ≡ match n2 { zero -> 1 ; succ k -> count n2 * factorial k }                   beta
    ≡ count n2 * factorial n1                                                     iota, k := n1

`*` unfolds to its primitive (delta), which asks for its left argument:

    count n2
    ≡ match n2 { zero -> 0 ; succ k -> 1 + count k }      delta, beta
    ≡ 1 + count n1                                         iota, k := n1
    ≡ 1 + (1 + count zero)                                 the same three steps on count n1
    ≡ 1 + (1 + 0)                                          delta, beta, iota on count zero
    ≡ 1 + 1                                                prim
    ≡ 2                                                    prim

then for its right argument, by the same steps:

    factorial n1
    ≡ count n1 * factorial zero         delta, beta, iota
    ≡ 1 * 1                             count n1 as above; factorial zero by delta, beta, iota
    ≡ 1                                 prim

and the whole is `2 * 1 ≡ 2`. Each line is a definitional equality, so the chain shows that
`factorial n2 ≡ 2`; mathematics does not execute, it checks equivalences (voice note 2026-05-30
18.01.53 [01:47]). `answer` reduces the same way to 24, which is what `luthier eval
tests/eval/factorial.lut answer` prints (`tests/test_elaborate.py`). The evaluator runs this
program without the checker (D-2026-10-13-u). The checker would reject it: its `Nat` is a `data`
whose constructors have no law of their role (spec 4.R3), and `factorial` has no laws, so nothing
in it could be certified. A lawful version would use the core's `Nat`, whose roles `OrderedSemiring`
gives (`kernel_laws.lth` §5), and would state what characterizes the factorial before giving its
body.

### 9.2 Read through

`examples/sonolocalizacion/validate_graph.lut` reads the two CSV tables of a distance graph, the
input of a fit of positions in sonolocalización, and checks the graph's invariants before any
fit. Its first lines are the imports, and they show the layering of sections 3 and 4:

    import "world_model.lut" HostConsole host : HostConsole
    import "numbers.lth" Doubles
    import "numbers_model.lut" doubles : Doubles
    import "arrays.lth" RankFloor
    import "distance_graph.lut" DistanceGraph ValidDistanceGraph ValidGraph firstViolation describe readGraph ...

A theory file (`.lth`) gives `Doubles`, the theory of the doubles, and its model file gives the model
`doubles`; the program is written against the theory and sees only what the theory exposes (L6.12,
privacy is ascription). `distance_graph.lut` is a program file, not a theory file: it holds
definitions with their own invariants, and the importer takes them by name.

The program, in the order a reader should take it, which is not the order of the text (spec 3.S1):

    graphDir : String := "examples/sonolocalizacion/A/graph"

A run parameter: a name with a body here that `run --set graphDir=...` replaces (spec 12.S18). It
is the hole of section 4 given a default. The next definition is a criterion, the rank floor below
which a direction counts as unseen by the distances:

    rankFloor (g : DistanceGraph) : RankFloor := toFloat64 (3 * g.nodes.nRows) * doubles.epsilon

Its comment says why it is a function of the graph and not a number in the code: a criterion is a
parameter (P11, every criterion is a parameter, never a constant in the code), here with the value
the earlier version used so that the count is the same. `summary` builds the text for a valid graph,
and takes a `ValidDistanceGraph`, a subtype of the graphs, `{ g : DistanceGraph | ValidGraph g }`
(section 3); so `report` may call it only on a graph that passed `ValidGraph`, and the `if
ValidGraph g` in its branch is the refinement of section 5 (spec 4.R11), written by hand because
the checker does not yet narrow a type by a condition. `report` asks `firstViolation`, which gives
`Maybe Violation`, a sum with a record on one side (`{ schema : String || inRow : RowViolation }`),
and `match` takes it apart: `nothing` is a graph with no violation, `just v` is described by
`describe`.

The only place the world enters is `main`:

    main (w : W) : W * Unit := {
      (w1, read) <- readGraph w graphDir
      host.print w1 (match read {
        nothing -> "FAIL ReadGraph: " + graphDir + " has no nodes.csv and measurements.csv that read as typed tables" ;
        just g -> report g })
    }

`readGraph` is an action of `distance_graph.lut`: it takes the token, reads `nodes.csv` and
`measurements.csv` with `host.readFile` (each read an action, the token threaded through
`<-`), parses each with the codec `csv` of `tables_model.lut`, and gives `W * Maybe DistanceGraph`.
In `main` the pattern `(w1, read)` binds the new token and the result; `host.print` takes `w1`
and gives back the last token, which is what `main` returns. Everything else in the file is a
pure function of values, so it reduces in any order the dependencies allow (L4.7), and the order
of the two actions is the order of the tokens. The reads are an observation of the world, so a
file that changes between two runs is a different input, and the demand reads it when it reaches
the extern and not before (L11.7). The graph in `A/graph` is a table of nodes (a name, a prior
mean `x y z` and a standard deviation per coordinate) and a table of measured distances between
pairs of nodes by row index.

Run from the root of the repository, `PYTHONPATH=src python3 -m luthier.cli run
examples/sonolocalizacion/validate_graph.lut` took a few minutes on 2026-10-14 (the interpreter
reduces term by term and has had no optimization) and printed one line:

    valid: 10 nodes, 22 measurements, 21 distinct pairs; directions the distances do not see: 14 (of which 10 are the heights and 3 the rigid motions of the plane)

The ten heights and three rigid motions of the plane are the directions the distances cannot see by
construction, and the fourteenth is left to the prior. A graph that breaks an invariant prints the
first one broken, with its row.

What the program shows. The invariants are Boolean laws over a concrete graph (`NoSelfPairs`,
`DistancesPositive`), joined by `and` in `ValidGraph`; the check that explains a failure is
`firstViolation`, the form that carries a row, and the poorer form `ValidGraph` is its derivation, as
spec 5.S9 asks; a law relates them, `ReportsValidity` (a check reports nothing exactly when the
graph is valid). The program is a plan until `main` is demanded: nothing in it ran when the file was
read, and `luthier run` gives `main` its token.

## 10. What stays outside the kernel, and where each piece comes from

Outside the kernel:

- Numbers beyond the primitives, vectors and matrices: libraries built from the kernel, numpy their
  representation in the host (spec 3.S21: a numpy array is a value of `Fin n -> Float64`). The
  reals by construction are a library too.
- What the host computes: values given by `extern`, never types (spec 4.R5). `provisional`, a named
  argument of `extern`, is the escape hatch for working in a hurry, recorded as debt.
- Probability, costs, the world's parts, checks: libraries, of which the core asks only an interface
  (spec 5.S10, 10.S5; L7.5, what a library can decide the core does not).
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
- The algebra of costs, and with it laws valued in `Cost` (O1, the algebra of costs).
- How a type names its equality (O2, the type with its equality as the base of every theory).
- The kind of a hole in the elaborated form: input, extern, pending, axiom (O9).
- Certificates, designed on sonolocalización's laws and on how they fail (D-2026-10-13-ad); then the
  demand and the planner (spec 8, spec 9).
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
  what a sample gives (L12.6; D-2026-10-13-n).
- The executable kernel of three items and the reliance on a `File` type: replaced by the core of
  D-2026-10-13-v and the console of `world.lth`.
- The doubling example (`doubleA`, `doubleB`, `Double`) of the old section 8: a `data` with no law of
  its constructors' roles is rejected by spec 4.R3 now, and the example carried the old syntax; the
  hand execution moved to a program the interpreter runs today, and certification is shown on the
  kernel's own models.
- The old grades (point, bounded, witnessed): read through the five of the Terms (spec 1.S12).
- The trace, the comparison of traces by consequence and by cost, and classes of machines: left by
  spec 10.S14 to the form of the record of a run, which spec 8 decides (8.S15).
