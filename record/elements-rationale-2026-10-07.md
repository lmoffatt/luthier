# The elements of the guide, and why each is said as it is

2026-10-07. A mirror of the list "The elements, in the order to think them" of
`docs/guide/00-fundamental-elements.md` at commit be7668a: one entry per bullet, with what the
bullet says, why it says it that way, where that comes from, what it rules out or costs, and what
is open. The guide is what a reader of Luthier sees; this is the record behind it. Inputs: the
specification (`docs/spec/04-kernel.md`, `05-static-semantics.md`, `06-numbers.md`) at the same
commit; the voice notes under `record/audios/`; the decisions D-2026-10-07-b to g in
`record/decisions.md`; GPT's reading of the list and the reply to it in `record/IA/`
(`2026 10 07 204138 GPT.md`, `2026 10 07 210212 reply to GPT.md`); the runs in `examples/exp.lut`
and `examples/cauchy.lut` (seed 7), and six probes of 2026-10-07 in a scratchpad, repeated here by
their text where they are cited. Written by the model. Every numbered principle and rule carries
its statement at first use; "decided" marks Luciano's decisions, "proposed" what the model put
forward and he has not marked.

## The opening paragraph

Says. A type is a concept: declared, then defined, and only then inhabited. A type has two
origins, construction and constraint. A type with a name of its own is made by laws or by
recursion; a primitive is named by the language; any other base is named, if at all, by an alias.
There are no loose functions: a function without laws of its own is written as the expression
itself, as an alias, or as the model of the theory whose law is its formula.

Why. The first sentence is P14 (proposed principle, in Luciano's words: a type is a concept,
declared, then defined, and only then inhabited; a function is a value of a defined function type,
never of a bare exponential), decided on 2026-10-07 (D-2026-10-07-e). The two origins are R4 (only
laws or recursion make a new type) said in one line, after GPT's point 19. "A new name is made in
two ways" was the earlier wording and was wrong by its own next sentence, since an alias is a new
name (GPT's point 3). The alias is R7 (an alias is written with `=` and has no state): an alias
abbreviates any term, not only a type, which is why a lawless function can be one; the checker
accepts `sq = \ (x : Float64) { x * x }` and lets it stand as a model of a theory with laws (run,
2026-10-07). The three forms follow from P14 and from a remark of Luciano's the same evening, that
one could define the square as `{ f | f x == x·x }` "y de alguna forma zafar": a function given
by a formula is the model of the singleton theory whose law is the formula. It is the honest form
and it buys something: the body satisfies the law by its own reduction, and any other model is
checked against it. Run: `sqr : Sqr := \ x { x * x }` passes 100 cases, `numpy.square` passes
100, `math.fabs` fails at x = 0.495401.

From. Luciano, chat 2026-10-07 (session 182f2465, lines 568 and 575, for P14; session d3b76232,
line 386 for the scheme and 534 for the square). GPT's points 2, 3, 14 and 19, and the reply.

Rules out. The design GPT proposes in its point 2, functions as ordinary values of the exponential
with names merely binding them. Declined on P14.

Costs. The libraries do not comply: `exp` in `real.lut` has no laws, and helpers like
`taylorFrom` in `examples/exp.lut` are recursive functions at a bare exponential. A helper either
is an alias, if it does not recurse, or carries its equations as laws, if it does. The cost
disappears when the checker grants the body's obligation by reduction, a grade `05 §7` lists as
"proved" and version 0 does not issue; P8 (no more bureaucracy than it pays for) says that
mechanism waits for its case, and the case will be the helpers of `lib/`. `check -v` reporting
loose functions is the first visible step (D-2026-10-07-e).

## Type

Says. A collection of values and, at the same time, a claim about them. `U` is the type of
types. The bases are given, not defined: the primitives, named by the language, and the type
expressions the formers build; an expression claims nothing beyond its shape and is named, if at
all, by an alias.

Why. "Collection and claim" is the type as proposition: the type is what a name claims, the body
its evidence (voice notes 2026-05-26 12.32.24 [00:51] and 2026-08-31 19.48.17 [01:02]; guide
§1). Bases given and not defined: `04 §1`, a `primitive "..."` body is a type the interpreter
provides, allowed only in the files of `06`; `06 §2` lists the five. Expressions by alias: R4
rejects a named lawless product (`r4_product_named.reject.lut`), and R7 gives the alias. GPT's
point 14 corrected the earlier wording, under which `Int` broke the rule.

From. The specification; GPT's point 14; Luciano's scheme of 2026-10-07 ("Type" first).

## Product, sum, exponential

Says. `A * B`, `A + B`, `A -> B`, with `Unit` and `Empty`, and labels for positions. The
structure of a bicartesian closed category and the bases a type is built on. A function is a
value of an exponential, with no separate category. A theory of several operations is a subtype
of a labeled product.

Why. These are the formers of the kernel (`04 §2`), and Luciano named them as the second element
of his scheme ("Cartesian Closed Categories: sum, prod exp", chat d3b76232, line 386). "No
separate category" is against C++, where functions are statements and not values (guide §7). A
theory as a subtype of a labeled product is `05 §1` (a theory is a subtype of a labeled base,
usually parameterized; its values are its models).

Open. The presentation is one among several; `U`, the dependent function and `data` would do
(guide §3; `05 §9`). Kept because the rules of `05` are stated on these formers directly.

## Dependent type

Says. `(x : A) -> B` and `(x : A) * B`: the "for all" and the "there is". A type that depends on
a value or on a type: `Fin n -> Float64`, `Exp (R : U) (m : NumberModel R)`, a record whose later
fields mention earlier ones. A quantified law is a dependent function; the subtype is a dependent
pair whose second component is erased from the term, the certificate living outside with its
grade.

Why. Luciano asked for it as an element of its own ("Otro tipo elemental que falta es el
dependent type", chat d3b76232, line 445). It is what makes a theory over a parameter possible,
and a vector of length n (guide §3). The certificate outside the term is `05 §7`: what is
certified is a law applied to particular values, recorded in a certificate file with its grade,
generators, seed and the hash of its dependency cone, and accepted by hash on import; a value of
`{ x : T | p }` is a value of `T`. GPT's point 5 asked whether the certificate is relevant,
erased or proof-irrelevant, and the earlier wording ("whose second component is the certificate")
invited the wrong answer; "every law is a dependent function" was too broad (GPT's point 7), since
`04 §3` admits a point law with no parameters.

Rules out. Proof-relevant certificates inside values, which would make `{ n : Int | n == 4 }`
have as many inhabitants as proofs.

## Law

Says. A term of type `Bool`, or a function into `Bool` over the parameters it quantifies, or a
conjunction, of type `Law`. Written over the base of the type it will define; the one place where
a base is used bare. In version 0 an executable predicate, R8 keeping it so; proofs after. A test
is evidence and not a proof; the certificate records the grade.

Why. The three shapes are `04 §3`. That a law is the one bare use of a base is the model's
reading of Hilbert and Tarski (proposed): the axioms of a theory are formulas, not objects of it;
the predicate of a subtype is written at the base because the type does not exist yet. Executable
in version 0: R8 (`==` exists only where equality is structural) is the consequence of laws being
run; the voice note 2026-10-04 10:28 [04:40] says the laws of the realization will not be exact,
they will carry a guarantee, and the tolerance as a parameter is P11 (every criterion is a
parameter, never a constant in the code). Evidence and grades: `05 §7`, point, sampled n, bounded,
exhaustive, witnessed, proved (not in version 0), assumed; the grade of a chain is that of its
weakest link. GPT's points 8 and 9 asked exactly this, and the specification already answered.

Open. A law may itself be a model of a theory of predicates (`Setoid` is a predicate with laws).
The "bare" use is the position of the predicate in the subtype, not a ban on laws over laws.

## Subtype by law, the theory

Says. `{ x : T | p }`, the way to define a type, in two acts or in one. Hilbert's implicit
definition made a type: the type is the theory, the laws an object must satisfy. The equation
signature, law, theory, model. `Exp R m`, `Ring A`, `Functor`. The pullback of `true` along `p`,
a mono with a certificate. This is what makes Luthier.

Why. The two acts are what Luciano asked for on 2026-10-04 (voice note 10:28 [21:06] to [21:36]:
declare the type, then define it with its characteristics), and R6 (the body of a declared name
is an inhabitant or a predicate) is the rule that makes the second act a definition of the type;
the checker accepts `Exp : Float64 -> Float64` followed by `Exp := Homomorphic & AtZero`. The
earlier wording had `Exp : R -> R` with `R` unbound next to the parameterized form (GPT's point
10). "Theory and model" was chosen over "postconditions" on 2026-10-07 because Luciano wanted a
mathematical name (D-2026-10-07-d); Hilbert's implicit definition is the model's naming of the
act (proposed). The laws are the equations and never "agrees with another implementation": R10 (a
law characterizes; a second implementation is not a law), which is why section 8 of the guide
defines `Double` by its recursion equations and not by agreement with `doubleA`. The equation
signature, law, theory, model is `05 §1` in GPT's words (point 12). `Functor` is a theory, not an
element: `MaybeFunctor` with `MapId` and `MapComp` at `Int` certifies 50 cases; the generic
`Functor` with `F : U -> U` checks and its law over `A : U` is not run, since nothing generates
types (`05 §7`); GPT's point 11 corrected "a functor is a theory" to "a functor is a model of it".
"This is what makes Luthier" is Luciano's note of 2026-10-06 (`funcion de los tipos en
Luthier.txt`): a check is made once, and belonging to a type is the certificate of it.

Costs. Whether the laws pin down a unique inhabitant is undecidable and never asked (`05 §1`);
"characterization" (`07`) is the aim of the laws, not a guarantee the checker gives.

## Value, the model

Says. `x : T := t`, the way to define a value. A value inhabits its type; an inhabitant of a
theory is a model of it. `expPy` and a Taylor sum as models of `Exp`; a program writes against
the theory and picks a model by name, or declares and lets another file fill. A function given by
a formula is the model of its singleton theory. `4` as `{ n : Int | n == 4 }` has exactly one
inhabitant; a procedure, one up to observations. A body that is a law defines the type instead.

Why. The type is the proposition and the body its evidence (voice notes above). Two models of one
theory is the paths idea of May 2026: one function, many implementations, each with its precision
and speed (voice note 2026-05-26 12.32.24 [01:26]; 2026-05-29 13.57.41 [03:18]). Filling from
another file is `03 §3` (a specification has as many implementations as files that fill it).
The singleton theory is the remark of 2026-10-07 on the square, above. Exactly one inhabitant:
R8 makes `n == 4` decidable on `Int`, and the certificate is outside the term, so there is no
`(4, proof)` pair to distinguish (GPT's point 6). Up to observations for a procedure is the
section *Declared, defined, computable* of the guide, from Luciano's "no se puede computar la
suma de dos reales, pero se puede definir" (2026-10-07) and the reals as Cauchy sequences in
`examples/cauchy.lut`. "A value inhabits, a model inhabits a theory" is GPT's point 16; under P14
the only types a value is not written at are the bare structural bases. The body as law: R6.

Dropped. The earlier bullet cited voice note 2026-10-04 10:28 for "a value is a type with one
inhabitant"; the idea is not in that transcript nor in any audio of the record (search of
2026-10-07). The citation was dropped and the idea kept; its source is for the fidelity audit.

## Declaration, the hole

Says. `x : T`, a name with its base and no body. Either half without the other: a concept before
its laws, a theory without a model, a parameter, an operation another file will provide. What
depends on it does not reduce until it is given a value.

Why. Declaring before defining is the voice note 2026-10-04 10:28 [21:06]. The hole as parameter
is R2 (a definition uses defined types: a hole of a defined type is a parameter, and what depends
on it does not reduce). The ideal nothing fills is `Real` and `expIdeal : Exp Real realModel`
(`06 §4`; D-2026-10-07-c, `Real` stays the ideal and the constructed reals are a realization).
Another file: `03 §3`. GPT's point 15 noted the roles differ; the act is one, and the bullet lists
the roles. An earlier wording said "forward declaration" and was removed: there is no "forward"
where the order of acts does not matter (`05 §2`).

Defect. The interpreter today requires a declared type to precede, in the file, the laws that
mention it; otherwise "unbound name" (run, 2026-10-07). That contradicts `05 §2` and is not in
the correspondence audit yet.

## Recursion

Says. The second way to make a new type, and a new function: a definition that mentions itself.
Laws restrict a space that exists; recursion generates one. Not a subtype, not an alias; its law,
freeness, has no generator, so the recursion is the definition, an initial algebra.

Why. "Or recursion" is in R4. Luciano asked whether subtype by law is the only way to define a new
name (chat d3b76232, line 386); the answer is two ways, because `data` is a subtype of nothing
earlier and a recursive alias does not close (`f = \ n { ... f (n - 1) }` fails with "unbound name
f", run of 2026-10-07). Freeness, the universal property of the initial algebra, quantifies over
every type, and `05 §7` says laws over all models have no generator and are not tested. "Restrict
and generate" is GPT's point 13.

Open. Mutually recursive data cannot be written today (correspondence audit, B02).

## Apply and reduce

Says. `f a`, and replacing the argument in the body until a datum, a procedure or a hole is
reached. Executing by hand is this.

Why. The rules of reduction are `04 §4`; executing by hand is guide §2 and Knuth (guide §7).
"Until nothing is left to do" was the earlier wording and is false for a procedure, which reduces
only when asked a question (a Cauchy real asked for a precision), and for a hole, where reduction
stops. Corrected on 2026-10-07 after the section *Declared, defined, computable*.

## The closing paragraph

Says. `U` is the type of types. Against C++ and against categories: the non-dependent fragment is
a bicartesian closed category, the dependent forms extend it to a locally cartesian closed one; a
theory is a subobject of a product of exponentials cut out by its laws, a model a global element,
`data` an initial algebra, a functor a model of a theory over `U`.

Why. The categorical reading is the model's (proposed), checked against GPT's point 17; Seely
(1984) is the reference for dependent types as locally cartesian closed categories. "Subobject
cut out by its laws" is the pullback of `true` along the predicate, with `Bool` as the classifier
of decidable subobjects, which is where R8 bites. A parenthesis "`U : U` is inconsistent and bites
only with proofs, section 9" from an earlier session was dropped on 2026-10-07 because `05 §9`
says nothing of the kind.

Open. The universe policy (`U : U` or a tower) is not stated in `04` or `05`.

## Decided and proposed

Decided by Luciano: P14 (proposed principle, his words); the scheme Type, formers, subtype by law
(D-2026-10-07-f); the dependent type as an element (same); "Theory and model" as the name
(D-2026-10-07-d); `Real` as the ideal with the constructed reals as a realization
(D-2026-10-07-c); the reply to GPT and this document (D-2026-10-07-g).

Proposed by the model: Law and Recursion as elements of their own; the three forms of a function
without laws of its own; the singleton theory as the reading of an explicit definition
(formalizing his remark on the square); the law as the one bare use of a base; the categorical
readings; the number model as the parameter of `Exp` and the direction of the arrow from the
ideal to the doubles (D-2026-10-07-b).

Open for Luciano: P14 against GPT's point 2, reaffirmed in the reply, with its cost in `lib/`;
the grade "by reduction"; laws for `exp` in `real.lut`, which invalidates the certificates of
everything that imports `real`; the order defect of the interpreter; the source of "a value is a
type with one inhabitant".
