# The fundamental elements of a Luthier program

Rewritten on 2026-10-04 from the Spanish draft of 2026-09-29 (`00-elementos-fundamentales.md`,
in the history), against the specification of `04-kernel.md` and `05-static-semantics.md`. This
document is the reading guide: the few ideas a program is made of, in the order to think them,
and a program executed by hand. The rules are in 04 and 05; where this text and those differ,
they hold. Ideas that come from the voice notes cite the note (`record/audios/`).

## The elements, in the order to think them

A type is a concept. It is declared, then defined, and only then inhabited: a value is written at a
type that is defined, never at a bare base (P14, proposed). A type has two origins, construction
and constraint: the formers build type expressions, and a type with a name of its own is made by
laws or by recursion (`05` R4, only laws or recursion make a new type). A primitive is named by the
language; any other base claims nothing and is named, if at all, by an alias. So there are no
loose functions: a function is a value of a defined function type, and a function without laws of
its own is written as the expression itself, as an alias, or as the model of the theory whose law
is its formula, `Sqr = { f : R -> R | ∀x. f x = x·x }` (Luciano, 2026-10-07; `05` R2; the reply to
GPT of 2026-10-07 in `record/IA/`, point 2). The list follows that order: the bases, then the law,
then what the law defines.

- **Type.** A collection of values and, at the same time, a claim about them: `Nat`, `Bool`,
  `Exp`. `U` is the type of types. The bases are given, not defined: the primitives `Int`,
  `Rational`, `Real`, `Float64` and `String` (`06 §2`), and what the formers below build from
  them. A base claims nothing beyond its shape, so it is named only by an **alias**, `x = t`, an
  abbreviation expanded wherever it is used, with no states (voice note 2026-10-04 12:17):
  `Maybe (A : U) = < nothing : Unit | just : A >`, `sq = \ (x : Float64) { x * x }`.
- **Product, sum, exponential.** `A * B`, `A + B`, `A -> B`, with `Unit` and `Empty` as the
  product and the sum of nothing, and names for positions when wanted: `{ a : A, b : B }`,
  `< a : A | b : B >`. The structure of a bicartesian closed category, and the bases a type is
  built on. A function is a value of an exponential, with no separate category: it can be an
  argument and a result. A theory of several operations is a subtype of a labeled product.
- **Dependent type.** `(x : A) -> B` and `(x : A) * B`, where `B` may mention `x`: the "for all"
  and the "there is". A type that depends on a value or on a type: a vector of length `n` is
  `Fin n -> Float64`; a theory over a parameter, `Exp (R : U) (m : NumberModel R)`, is a function
  into `U`; a record whose later fields mention earlier ones, `{ nRows : Nat, cell : Fin nRows ->
  Maybe Cell }`, is a dependent pair. Every law is written at a dependent function, and the
  subtype below is a dependent pair whose second component is the certificate (Luciano,
  2026-10-07).
- **Law.** A function into `Bool` with its parameters quantified, `Homomorphic R m f x y`, or a
  conjunction `p & q`, of type `Law` (`04 §3`). It is written over the base of the type it will
  define, and it is the one place where a base is used bare: a law is the formula of a theory,
  not an object of it. `test` runs it, on drawn cases or on every case, and the certificate
  records the grade (`05 §7`).
- **Subtype by law, the theory.** `{ x : T | p }`: the values of the base `T` that satisfy the
  law `p`. The way to define a type. Declared then defined, `Exp : R -> R`, `Exp := Homomorphic &
  AtZero`, it is Hilbert's implicit definition made a type: the type is the theory, the laws an
  object must satisfy. `Exp (R : U) (m : NumberModel R)` is a theory of one operation over a
  model of `NumberModel`, as a vector space is over a field; `Ring A` has three operations;
  `Functor` is one over `U`, an object map, an arrow map and two laws, so a functor is a theory
  and not an element of its own. Categorically, the pullback of `true` along `p`: a mono with a
  certificate. This is what makes Luthier.
- **Value, the model.** `x : T := t`, or `x := t` for a name declared before: a name with a body,
  whose claim is its type. The way to define a value, and a value is a model of the theory it is
  written at: `expPy : Exp Float64 (float64Model tol) := extern "python:math.exp"`, a Taylor sum
  another, each certified against the same laws; a program writes against `Exp` and picks a model
  by name, or declares `exp : Exp ...` for another file to fill (`03 §3`; `examples/exp.lut`;
  voice note 2026-05-26 12.32.24 [01:26]). Read as a type, a value is the one with a single
  inhabitant, `4` as `{ n : Int | n == 4 }`, up to the equality its presentation has: `==` for a
  datum, observations for a procedure (*Declared, defined, computable*, below). If the body is a
  law, the act defines the type instead; the type of the body says which (`05` R6).
- **Declaration, the hole.** `x : T`: a name with its base and no body. Either half without the
  other: a concept named before its laws, `Exp : R -> R`; a theory without a model, `expIdeal :
  Exp Real realModel`, the ideal nothing fills; a hypothesis, an input, `sigma : Float64`; an
  operation another file will provide. What depends on it does not reduce until it is given a
  value.
- **Recursion.** The second way to make a new name: a definition that mentions itself, `data
  { zero : N ; succ : N -> N }`, a type generated freely by its constructors, or a recursive
  function. Neither is a subtype of something earlier nor an alias, which would expand without
  end; its law, freeness, quantifies over every type and has no generator (`05 §7`), so the
  recursion itself is taken as the definition: an initial algebra.
- **Apply and reduce.** `f a`, and replacing the argument in the body until a datum, a procedure
  or a hole is reached (*Declared, defined, computable*, below). Executing by hand is this.

`U` is the type of types; it appears when a function returns a type. Against C++: statements
are definitions, expressions are values (functions included), and types are types, plus the
dependent ones and the subtype with laws. There are no mutable variables, sequence, pointers or
inheritance. Against categories: types are objects, functions arrows; product, sum and exponential,
with their dependent forms, are the structure of a bicartesian closed category, locally so; a
theory is a subobject of a product of exponentials cut out by its laws, a model a global element of
it, `data` an initial algebra, and a functor a model of a theory over `U`.

## What types are for: a check is made once

Luciano, 2026-10-06 (`sonolocalizacion/Lucianos ideas dir/funcion de los tipos en Luthier.txt`): a
program should never check the same thing twice. Belonging to a type is the certificate that a value
passed the check the type states, so when a value is checked, the result is recorded by giving the
value a finer type, and nothing downstream checks it again. This is the reason the subtype is the
element that makes Luthier.

It is the principle of `07` (one name for each concept) applied to facts instead of names: one
check for each fact. It acts at three moments.

- When a program is certified, a law tested on a name is recorded in a certificate and accepted by
  hash afterwards (`05 §7`).
- When a program runs, a condition refines the variables it tests inside its branch (`05` R11), and a
  check whose evidence must outlive the branch returns the value at its refined type (`05 §9`,
  *Checks*). Between two different checks, as a fast one and the predicate it stands for, the
  relation is a law certified once, so at run time only one of them is made.
- At the boundary of a program a check about the world refines the content it read, since the file it
  was read from can change between the check and the use.

How much the type of a result should say depends on what it costs to know it again. For
`y = sin x` the type can be a real, a real in [-1, 1], or `sin x` itself; the bound is useful and
cheap, and `sin x` itself matters only to symbolic algebra. For `b = mapOpt b0 f x`, the optimum of
the function `f` on the data `x` from the start `b0`, the type can be a vector, an optimum, an
optimum of `f` and `x`, or an optimum of `f` and `x` from `b0`; since finding it is expensive and a
local optimum depends on its start, the last is the right one, a type indexed by every input of the
computation. A cheap result carries its bound; an expensive one carries its inputs and its witness.

## Declared, defined, computable

Luciano, 2026-10-07 (chat 182f2465): the sum of two reals cannot be computed, but it can be
defined. The body of a name, once it has one, is of one of two shapes, and with the hole that makes
three kinds of value.

- A *hole*: a declaration, the claim with no body. `Real`, the ideal, which no interpreter fills,
  and `expIdeal : Exp Real realModel`, the exponential on it. Nothing reduces; the laws are stated.
- A *procedure*: a body whose normal form is a function over an infinite domain. It answers every
  finite question, and reduces when asked one. A real as a Cauchy sequence of rationals,
  `Cauchy : U := { s : Int -> Rational | Modulus s }`, applied to a precision gives a rational, and
  the sum of two such reals, `\ n { x (n + 1) + y (n + 1) }`, is defined and reduces at any
  precision (`examples/cauchy.lut`). What never computes is its equality: two sequences with the
  same limit are equal by a law that no finite observation decides (`05` R8, `==` only where
  equality is structural).
- A *datum*: a body whose normal form is a literal or a constructor, with `==`: `Int`, `Rational`,
  `Float64`, a `data`, and a function from a finite domain, which is a table (`04 §6`).

The line is not whether the type is infinite but how many observations an answer needs. `Int` is
infinite and every value of it is a datum, with its equality decided; what does not compute over
`Int` is the "for every n", which is induction, the proof layer's job, and version 0 samples it.
`Bool` and `Fin n` are finite, and over them everything computes, equality of functions included,
and a law is certified exhaustively. Over procedures a law is tested by observations, at sampled
arguments and, for the reals, sampled precisions. A definition over a generic `A : U` computes on
each instance; what has no generator and no test is the quantification over every `A` (`05 §7`,
laws over all models).

This is the axis of the three states of a name (section 1) seen from the body: declared is defined
implicitly, by its properties; defined is defined explicitly, by a body; computable is that the
body reduces to a datum.

Between the ideal and what runs the arrow goes one way. `Float64 : Real` as values, so the ideal
applies to a double, and `realize f x = round (f x)` brings the result back; `g` realizes `f` when
`g x` stays within tolerance of it, and this runs with a `Real` that computes, the construction
above. The other direction, a function on the doubles as a function on the reals, is false: the
domain goes against the refinement (`05` R9, contravariant domain), and the approximate law with
the rounded sum is not the exact law with the sum.

## 0. Notation

Every symbol used in this document.

- `x : A` reads "x refines A"; for a value, "x is an A".
- `x : A := t` defines `x` as `t`; `x : A` alone declares it; `x = t` makes `x` an alias of `t`.
- `≡` is definitional equality: two terms that reduce to the same normal form. It is a judgement
  the reducer decides, not a proposition.
- `U` is the universe, the type whose inhabitants are types.
- `(x : A) -> B` is the type of dependent functions: to each `x : A` a term of `B`, where `B` may
  mention `x`. Without the dependence it is written `A -> B`.
- `(x : A) * B` is the type of dependent pairs; `A * B` without the dependence.
- `\ x { t }` is the function that maps `x` to `t`.
- `t[a/x]` is `t` with every free occurrence of `x` replaced by `a`.

## 1. The unit is the definition

A program is a finite set of acts: declarations, definitions and aliases, plus the directives
`import`, `test`, `gen` and `operator`. There are no statements and no sequence. The order in which
they are written does not matter: the dependency between definitions is read off the names each
one uses, which gives the directed graph of definitions of the voice note 2026-05-29 15.11.47
[01:48]. The checker reads the whole program before checking anything (`05 §2`).

The graph is not acyclic, and a cycle is not an error. A type is an assembly of other types under
laws: the laws mention the type, the type in its definition names the laws, and that loop, the
strongly connected component, is an object. A definition that mentions an object without being on
its loop is a branch: a new entity that depends on the object one way (voice notes 2026-10-04 12:16
and 12:30). That the structure is in the names is what will let two objects with the same shape
of cycle be recognized as candidates for an isomorphism.

A name passes through three states: declared (its base is known), defined (it has a body), and
certified (some of its laws passed `test`, each with a grade: a point, `n` sampled cases, every
case of a box or of a finite domain, a witness, a proof, or assumed as an axiom; `05 §7`). The
body of a defined name is, besides, a datum or a procedure (*Declared, defined, computable*,
above): a classification of bodies, not a fourth state. A definition may use only types that are
defined, except those of its own object (`05` R2); that is what makes "this is a Table" guarantee
something. A hole of a defined type is a parameter: `sigma : Float64` can be used, and what
depends on it does not reduce until it is given a value. This is the principle "you do not execute
code until it is defined" of the voice note 2026-05-30 18.09.57 [00:53].

The type is the proposition the name claims, and the body is its evidence; for a function, its
implementation (voice notes 2026-05-26 12.32.24 [00:51], 2026-08-31 19.48.17 [01:02]). This covers
the double definition the voice note 2026-05-29 14.28.55 [03:42] asked for: "from the properties"
is the type, "operationally" is the body.

## 2. Terms and reduction

A term is built from names, abstractions `\ x { t }`, applications `f a`, pairs and their
patterns, injections into sums and `match` on them, constructors of recursive types and `match` on
them. There is one rule of computation, substitution,

    (\ x { t }) a  ≡  t[a/x]

together with the unfolding of a defined name to its body and the rule that a `match` on a
constructor, an injection or a pair picks the branch that fits. `04 §4` lists them. Executing a
program by hand is choosing a definition without free variables and reducing it until nothing is
left; each step is a definitional equality. Mathematics does not execute, it checks equivalences
(voice note 2026-05-30 18.01.53 [01:47]).

## 3. The type formers

The kernel chosen to start with (`04 §2`): `U`; the exponential, with its dependent form; the
product, with its dependent form; the sum; `Empty` and `Unit`; the subtype; `data` for recursive
types; and the primitive types `Int`, `Rational`, `Real`, `Float64` and `String` (`06 §2`), of which
the interpreter fills all but `Real`, the ideal, which stays in effect declared. `Bool` is
`< true : Unit | false : Unit >`, `Maybe A` is `< nothing : Unit | just : A >`, and `Fin n`, the
type of the n indices `{ k : Int | 0 <= k and k < n }`, is in the core because a vector of length
n is a function `Fin n -> Float64`.

This is one presentation among several. A smaller one would keep only `U`, the dependent function
and `data`, deriving products, sums and the empty and unit types from `data`. The choice was made
so that the rules of 05 can be stated directly, without translation; Luthier should eventually be
able to state the equivalence of its presentations (voice note 2026-10-04; `05 §9`).

Two senses of "primitive" must not be confused (`04 §6`). Semantically primitive is the kernel.
Primitive for performance is an extern: a value computed by the environment because it is faster
there. A numpy array is not a primitive type; it is a value of `Fin n -> Float64`.

## 4. The two equalities, and the levels after them

- `a ≡ b`, definitional equality, decided by the reducer. It is what one checks with a pencil.
- `a = b`, propositional equality, a type whose terms are paths. It belongs to the proof layer,
  absent in version 0; until then `x = t` at the level of acts is an alias.

The other levels of equivalence the voice notes ask for (2026-05-30 18.01.53 [02:42]) are types on
top: an isomorphism is two functions and two laws that say they undo each other; approximate
equality with a tolerance is where probability enters; equality in distribution is a test that
does not separate two samplers. In version 0 the equality a law uses is decidable `==` only where
equality is structural; on functions it is a parameter or a component of the theory (`05` R8).
That is the line between a datum and a procedure (*Declared, defined, computable*): on a procedure
equality is a law tested by observations, at sampled arguments and, for the reals, sampled
precisions.

## 5. The program as data

A later layer: `Program` and `Term` as data types defined in Luthier, so that checking, combining
programs and evaluating are ordinary functions on that data, as in Lisp's metacircular evaluator.
The only primitive would be the bootstrap agreement, the implementation accepting a value of
`Program` as a program. "Code is the first element" (voice note 2026-05-29 14.36.03 [02:38]) and
the impossibility of self-hacking (voice note 2026-08-31 19.57.14 [00:11]) are its requirements.
Not in version 0.

## 6. What stays outside the kernel

- Numbers beyond the primitives, vectors and matrices: native types built from the kernel; numpy
  is their representation. The reals by construction (`examples/cauchy.lut`) are a library too, a
  realization of `Real` beside `Float64` and not its definition (D-2026-10-07-c, `Real` stays the
  ideal).
- What the environment computes: values given by `extern`, never types (`05` R5). `extern
  provisional` is the escape hatch for working in a hurry, recorded as debt.
- Probability, beliefs, optimization: libraries.
- Pointers, mutation, sequence, classes, inheritance, control flow: they do not exist. `if` is a
  `match` on `Bool`, a loop is recursion, a sequence is a dependency.

## 7. Where each piece comes from

- From the lambda calculus, section 2.
- From Lisp, the program as data (section 5).
- From C++, the separation of declaration and definition, here the hole; and templates, here
  functions over `U`.
- From Martin-Löf type theory, the kernel: dependent functions and pairs, sums, empty and unit
  types, inductive types, the universe.
- From Python, a surface that reads aloud and lets a type be inferred.
- From Knuth, that an algorithm is written for a person to follow with a pencil.

## 8. A program executed by hand

    N : U := data { zero : N ; succ : N -> N }

    add (m n : N) : N := match n { zero -> m ; succ k -> succ (add m k) }

    doubleA (n : N) : N := add n n
    doubleB (n : N) : N := match n { zero -> zero ; succ k -> succ (succ (doubleB k)) }

    Double : N -> N
    DoubleZero (f : Double) : Bool := f zero == zero
    DoubleSucc (f : Double) (n : N) : Bool := f (succ n) == succ (succ (f n))
    Double := DoubleZero & DoubleSucc

    doubleA' : Double := doubleA
    doubleB' : Double := doubleB

Abbreviations for the run: `1 = succ zero`, `2 = succ 1`.

    doubleA 2
    ≡ add 2 2
    ≡ succ (add 2 1)                  match on 2 = succ 1
    ≡ succ (succ (add 2 zero))        match on 1 = succ zero
    ≡ succ (succ 2)                   match on zero
    = 4

    doubleB 2
    ≡ succ (succ (doubleB 1))
    ≡ succ (succ (succ (succ (doubleB zero))))
    ≡ succ (succ (succ (succ zero)))
    = 4

`Double` is the doubling as a type: the functions that send `zero` to `zero` and a successor to
the successor of the successor of their value. `doubleA'` and `doubleB'` each claim that a double
is one; `doubleB` satisfies `DoubleSucc` by its own reduction, `doubleA` by the laws of `add`. The
checker records the obligations; `test doubleA'` draws values of `N` and reduces both sides of
each law on each, which is the same reduction as above, and writes the certificate with the
number of cases. That the two doubles agree, `doubleA n == doubleB n`, follows from the laws and
is a corollary, not a law (`05` R10, a law characterizes; a second implementation is not a law).
Proving the laws for every `n` needs induction and is the proof layer's job. `examples/exp.lut`
does the same with the exponential: a Taylor sum and the environment's `exp`, two models of
`Exp Float64 (float64Model tol)`, certified against `Homomorphic` and `AtZero`; and
`examples/cauchy.lut` gives the exponential on the reals a body, `expC`, with the terms the
precision asks.

## 9. Open

- The proof layer: a recursor that guarantees termination, propositional equality, and a verdict
  "proved" beside "sampled".
- A hierarchy of universes (`U : U` is inconsistent; it bites only when there are proofs).
- `Program` and `Term` as data.
- Whether a definition carries a text field, so a program reads as a document.
