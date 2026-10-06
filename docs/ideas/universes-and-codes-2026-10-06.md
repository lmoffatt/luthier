# Universes, reflection and codes: where generic generators can live

2026-10-06. Written from a conversation between Luciano and Claude, for Luciano to correct and cut
before it feeds the second draft of `docs/semantica/08-tests.md`. It starts from a contradiction in
the first draft of 08, explains the type theory needed to resolve it (dependent types,
parametricity, reflection, universes in the styles of Russell and of Tarski, codes for recursive
types), and ends with a proposal and what it asks of the checker.

## 1. Why this came up

The first draft of `08-tests.md` records Luciano's decisions on generators, and it has gaps that an
implementer would have to fill by deciding alone. Six of them:

1. G1 says generators are values of Luthier; G2 says the generic generators are functors over the
   type. A functor that walks the structure of any type would have the type `(T : U) -> Gen T` and
   would need to ask what form `T` has. Luthier has no way to ask that (section 2), and taking a
   `T : U` goes against the rule that almost nothing should.
2. With `--imports`, a law of a library is run by the program that imports it; the draft does not
   say whether it is drawn with the library's binding or the importer's.
3. `sampled` over a recursive `data` says neither how it terminates nor how it uses the size.
4. "A metric or a cost" for numbers cannot be implemented for an arbitrary cost: sampling by the
   inverse of the cumulative cost needs the integral of the cost, and only `linear` and `log` have
   it in closed form.
5. In `where { tol := ..., TestedFull := ... }` nothing tells whether a key is a parameter or a type;
   nothing says how a binding uses earlier parameters (`a := gaussianBeliefOf n ...`), nor whether a
   parameter without a generator is an error of `check` or of `test`.
6. The reach of a compound type (a record, a vector) has no representation, so C6 cannot compare a
   run's values with it.

This document is about the first. Sections 7 and 8 also settle the third.

## 2. What Luthier can and cannot do with a type

In the kernel (`04 §2`) every type former has an introduction (how its values are built) and an
elimination (how they are used). The universe `U`, the type of types, has an introduction (every
type is a value of `U`) and no elimination. So a function can receive a type and use it: apply
`List` to it, build `VecOf n`, put it in a signature. It cannot ask a type what it is made of
(whether it is a product, or a `Float64` refined between two bounds). There is no `match` over `U`.

A generic generator needs exactly that question answered. Today the interpreter answers it in
Python, from outside the language: `generators.py` walks the structure of a type to draw a value,
as the structural `==` of R8 walks it to compare two. The language itself cannot.

## 3. Dependent types

In most languages types and values live apart: `Vec Float64` is a vector of doubles of any length.
A dependent type mentions a value. `VecOf 3` is the type of vectors of exactly three entries, and
`VecOf n` is a family of types indexed by the number `n`. Two constructions make the theory, and
Luthier has both:

- **The dependent function (Π).** `(x : A) -> B`, where the result type `B` may mention the
  argument `x`. `start (o : Objective) (x0 : VecOf o.dim) : LMState o.dim`: the type of the second
  argument and of the result depend on the value of the first, so the checker verifies that the
  start point has the objective's dimension without running anything.
- **The dependent pair (Σ).** `(x : A) * (y : B)`, where the type of the second component depends
  on the value of the first. `Vec A = { n : Nat, f : Fin n -> A }`: a length, and a function that
  accepts only indices below that length.

The universe `U` makes types into values, so a function can take and return types: `List : U -> U`,
`VecOf : Nat -> U`. This is what makes Luthier a language with full dependent types rather than one
with generics.

## 4. Parametricity, and why a `match` over `U` has a price

If a function cannot look inside a type, whatever it does with values of that type is uniform.
Reynolds (1983) made this precise and Wadler (1989) named its consequences "theorems for free": laws
that follow from a signature alone.

- `f : (A : U) -> A -> A` is the identity. It receives a value of a type it knows nothing about,
  cannot make another value of that type, and can only return what it got.
- `g : (A : U) -> List A -> List A` commutes with `map`: for every function `h`,
  `g (map h xs) = map h (g xs)`. It can reorder, duplicate or drop elements, always the same way.

G5 of 08 rests on this: for a parametric property one well-chosen instance stands for all
(Bernardy, Jansson and Claessen 2010). If a generic function cannot tell types apart, testing it at
one type says something about every type.

Add a `match` over `U`, called a *typecase*:

    f (A : U) (x : A) : A := match A { Int -> x + 1 ; _ -> x }

The type of `f` is still `(A : U) -> A -> A`, and `f` is no longer the identity. The free theorems
fall, and with them the testing at one instance. And `U` is open, since every program adds types, so
a `match` over it can never be exhaustive.

## 5. Reflection

Reflection is a language treating itself as data. It comes in two grades.

- **Inspecting types at run time.** The typecase above, or `type(x)` and `isinstance` in Python.
  Luthier's interpreter does this in Python all the time; the language does not.
- **Quoting and running code.** `quote t` gives the syntax tree of the term `t` as a value of a type
  `Term`; `unquote` (or `eval`) runs it again. Lisp has had it since 1958; Lean, Idris and Agda have
  typed versions, where `Term T` is the syntax of a term of type `T`. It is the layer `00` and
  `02 §8` leave open: `Program` and `Term` as data of Luthier, so that the checker could be written
  in Luthier.

Full reflection is the strongest tool and the most dangerous. A program can break any invariant
(make a value of a refined type without its obligation), parametricity is lost, and its semantics
needs `Term` specified inside the language. Drawing values does not need it.

## 6. Universes in the style of Russell and of Tarski

Per Martin-Löf named the two styles in his type theory (1984), the theory behind Agda, Coq, Lean and
the dependent part of Luthier. Both answer one question: if types are values of `U`, what exactly is
an element of `U`?

### 6.1 The names

- **Russell.** In Russell's theory of types (1908) a type is directly the collection of its members.
  In a universe in his style an element of `U` is a type: if `Nat : U`, then `Nat` is used as it is,
  in `n : Nat`. One object plays both roles.
- **Tarski.** Tarski (1933) separated a sentence from what it says: "snow is white" is a string of
  symbols, and it is true if and only if snow is white. His definition of truth has two levels, the
  name of a sentence and its interpretation. A universe in his style does the same with types. An
  element of `U` is a *code*, the name of a type, and a decoding function takes each code to the
  type it names. In the literature the function is written `El` (for *elements*: `El c` is the type
  of the elements of what `c` names); other texts write `T(c)` or `⟦c⟧`. This document calls it
  `Decode`, which pairs with `Code` and says its direction. A name such as `typeOf` would mislead:
  `typeOf x` usually means the type of the value `x`, and the type of a code is `Code`; `Decode c`
  is the type that `c` names.

An image: Russell is a box with the objects in it. Tarski is a catalogue of labels, with a function
that brings the object a label names.

### 6.2 The rules

With `A`, `B` types and Π the dependent function:

| | Russell | Tarski |
|---|---|---|
| an element of `U` | a type: if `A : U` then `A` is a type | a code: if `a : U` then `Decode a` is a type |
| a base type | `Nat : U` | `nat : U`, with `Decode nat ≡ Nat` |
| the dependent function | if `A : U` and `B : A -> U`, then `((x : A) -> B x) : U` | `pi : (a : U) -> (Decode a -> U) -> U`, with `Decode (pi a b) ≡ (x : Decode a) -> Decode (b x)` |
| notation | light: the type is written once | explicit: `Decode` at every use |

The equations written `≡` (the decoding equations) hold by computation: the checker reduces
`Decode (pi a b)` to the function type while it checks.

### 6.3 The differences that matter

**Unique typing and the hierarchy.** `U : U` is inconsistent as a logic: Girard (1972) built a
paradox from it, a relative of Russell's. Systems used for proofs therefore have a ladder
`U0 : U1 : U2 : ...`. In the style of Russell, when the levels are cumulative, the same `Nat` is an
element of `U0` and of `U1`: one term with many types, which complicates the metatheory. In the
style of Tarski, going up a level is an explicit function, `lift : U0 -> U1` with
`Decode1 (lift a) ≡ Decode0 a`, and each term has one type; that is why semantics and models are
usually done in this style, even where the surface of a language is Russell's. Luthier has `U : U`
today; `00` lists the hierarchy as open, since the inconsistency only matters once there are proofs.

**What can be eliminated.** This is the difference that matters here. In the style of Russell, `U`
is the collection of every type, and every program adds its own: it is open, a `match` over it
cannot be exhaustive, and Luthier's kernel gives it no elimination. In the style of Tarski, `U` can
be an ordinary `data`, a closed set of codes defined inductively, and then it has a `match`, by
induction over the codes. Such a *closed universe* is how generic programming is done in dependent
type theory (Altenkirch and McBride 2003; Benke, Dybjer and Jansson 2003).

**What a signature promises.** When both live together, a signature says what a function may do.
`(A : U) -> ...` cannot look at `A`: it is parametric and keeps its free theorems. `(c : Code) -> ...`
can look at the form of `c` and act differently in each case: it is not parametric, and its type
says so. A typecase over `U` breaks parametricity silently, since a function with a parametric
signature stops being parametric; a universe of codes makes the exception visible.

**Reach.** A closed universe describes only the types that have a code. That is the meaning of
"there are generators only of defined types": what has no code (a declared type with no definition,
a type received as a parameter) cannot be inspected, which is what is wanted.

### 6.4 What languages do

Coq, Agda and Lean present a Russell surface: one writes `Nat : Type` and uses `Nat`. Inside, or in
their metatheory, they often work in the style of Tarski. For generic programming in Agda one
defines a closed universe of one's own, a `data Code` and a `Decode : Code -> Set`, in a library,
next to Agda's Russell `Set`. The proposal of section 9 does the same in Luthier.

If the codes included a code for `U` itself, Girard's paradox would come back through `Decode`. The
codes of generators do not need one: no generator draws a type (08, G5).

## 7. A universe of codes for Luthier

    Code : U := data {
      nat    : Code ;                                -- the naturals
      real   : Float64 -> Float64 -> Code ;          -- a double between two bounds
      prod   : Code -> Code -> Code ;                -- pairs
      sum    : Code -> Code -> Code ;                -- alternatives
      vec    : Nat -> Code -> Code ;                 -- vectors of a given length
      refine : (c : Code) -> (Decode c -> Bool) -> Code   -- a subtype, with its predicate
    }

    Decode (c : Code) : U := match c {
      nat        -> Nat ;
      real lo hi -> { x : Float64 | lo <= x and x <= hi } ;
      prod a b   -> Decode a * Decode b ;
      sum a b    -> Decode a + Decode b ;
      vec n a    -> { v : Vec (Decode a) | v.n == n } ;
      refine a p -> { x : Decode a | p x }
    }

`Code` is an ordinary `data`, so it has a `match`, and the generic functor becomes a function of
Luthier:

    sampled (c : Code) (m : Metric) : Gen (Decode c) := match c {
      nat        -> natUpToSize ;
      real lo hi -> continuous m lo hi ;
      prod a b   -> pairOf (sampled a m) (sampled b m) ;
      sum a b    -> eitherOf (sampled a m) (sampled b m) ;
      vec n a    -> vectorOf n (sampled a m) ;
      refine a p -> filter p (sampled a m)
    }

This cannot be written without dependent types. The result type `Gen (Decode c)` depends on the
value `c`, so each branch returns a different type: a generator of naturals in one, of pairs in
another. Haskell needs an extension for it (GADTs); here it is the ordinary Π.

What Luthier gains:

- Parametricity stays. Only functions that take a `Code` can tell forms apart; those that take an
  `A : U` still cannot, and their free theorems hold.
- Luciano's principle becomes literal: there are generators only of types with a code, and a type
  declared without a definition has none. The checker can derive the code of a definition, since it
  knows its structure.
- What the interpreter does from outside can live inside, with laws and certificates: the structural
  equality of R8 as `eq : (c : Code) -> Decode c -> Decode c -> Bool`, the reach of a certificate as
  a function over codes, the generic generators.

`refine` mentions `Decode c` in its own constructor, so `Code` and `Decode` are defined together,
each using the other. This is induction-recursion (Dybjer 2000), and it is consistent. In Luthier's
terms the pair is a cycle, an object (`05 §3`), which is how Luthier already reads mutual
definitions.

## 8. Recursive types: the code of a fixed point

The codes of section 7 describe types of bounded shape. `List A`, trees, and `Nat` defined as zero
or a successor are defined in terms of themselves.

The idea is to separate one layer from the recursion. A list is empty, or an element followed by a
list. Writing `X` for the place where "a list" appears, a layer is

    F(X) = 1 + A × X

with `1` the type `Unit` (the empty list), `+` the sum, `×` the product and `A` the type of the
elements. `List A` is the type `X` such that `X ≅ F(X)`: a list is exactly a layer whose recursive
position holds another list. That `X` is the *fixed point* of `F`, written `μX. F(X)`, where `μ`
marks the least fixed point. Least means that only what is built in finitely many steps counts:
finite lists, not infinite ones. Other examples: `Nat = μX. 1 + X` (zero, or the successor of a
natural); a binary tree with leaves in `A` is `μX. A + X × X`.

Two more constructors of `Code` describe it:

    var : Code ;          -- the recursive position, the X
    mu  : Code -> Code    -- the type that is its own layer

A list of doubles between 0 and 1 is the code `mu (sum unit (prod (real 0.0 1.0) var))`. `Decode`
then needs to know which type stands at `var`, and for `mu` it builds the fixed point; in the
language that is a generic `data`, `Fix F := data { roll : F (Fix F) -> Fix F }`.

One condition is met by construction. `X` must not appear to the left of an arrow. The classic
example is `X ≅ X -> Bool`: such a type cannot exist (Cantor's diagonal argument), and admitting it
makes the system inconsistent. Since `Code` has no arrow constructor with `var` on its left, every
fixed point it describes is legitimate. The condition is called strict positivity.

### 8.1 Drawing a fixed point

To draw a value of `μF`, draw a layer and, at each `var`, draw again. The danger is that it never
ends. In a binary tree where each node chooses "two children" with probability `q`, a node has
`2q` children on average, and when `2q ≥ 1` the tree is infinite with positive probability: a
Galton-Watson branching process, the model of the extinction of surnames. Two known remedies:

- **A size that decreases.** Each recursive call receives a smaller size, and at size 0 only the
  alternatives without `var` are allowed. `genList` does this today with its length.
- **Weights by size.** Each value gets a weight that depends on its size. Boltzmann samplers
  (Duchon, Flajolet, Louchard and Schaeffer 2004) choose a value with probability proportional to
  `x^n`, with `n` its size and `x` a parameter that sets the expected size. Feat (Duregård, Jansson
  and Wang 2012) counts the values of each size from `F` and draws uniformly within a size by
  indexing into the cumulative counts.

The last is Luciano's idea of sampling over the cumulative sum of costs. For a fixed point the cost
is the size, and the counts per size come from the code, without looking at any value. Numbers
(with a linear or logarithmic metric), censuses and recursive types fall under one rule.

## 9. The decision, and what it asks of the checker

Three ways out of the contradiction of section 1:

| way | what it is | what it costs |
|---|---|---|
| functors of the interpreter, as `==` | generic from outside, named and recorded in the certificate | the generic generators are not Luthier; against G1 |
| typecase over `U` | a `match` over types | breaks parametricity and G5; `U` is open |
| a universe of codes | `Code` and `Decode` in a library; the functors are functions over codes | writing the universe; the checker derives codes; `mu` when it is needed |

Proposed: the third. It makes true at once "generators are citizens of Luthier" and "there are
generators only of defined types", and it leaves reflection proper (`Term`, quote and unquote) where
it is, the later layer of `00`, for when the checker is to be written in Luthier.

It asks three things of the checker.

1. **A `data` and a function defined together.** `Code` and `Decode` form a cycle, since `refine`
   mentions `Decode c`.
2. **Large elimination.** `Decode` returns a type by a `match` over data; the checker reduces
   `Decode (prod a b)` to `Decode a * Decode b` when it appears in the position of a type.
3. **A `match` that refines the expected type in each branch.** In
   `sampled (c : Code) : Gen (Decode c) := match c { prod a b -> ... }`, inside the branch the
   checker must know that `c` is `prod a b`, and therefore expect a `Gen (Decode a * Decode b)`.
   This is dependent pattern matching, and it is what R11 states for patterns: inside
   `match m { just y -> a }`, `a` knows `m == just y`. R11, already in the next round, is therefore a
   prerequisite of the universe of codes.

It can be staged. First the codes without `mu`: numbers with bounds, products, sums, vectors and
refinements, which cover almost everything the project draws. `List` can have a code of its own
(`list : Code -> Code`) until `mu`, with Boltzmann sampling, is needed for a recursive `data`.
Functions over infinite domains have no generic code for drawing: they go by census (08, G9).

## References

- T. Altenkirch and C. McBride. Generic programming within dependently typed programming. *Generic
  Programming*, IFIP TC2/WG2.1 Working Conference, 2003.
- M. Benke, P. Dybjer and P. Jansson. Universes for generic programs and proofs in dependent type
  theory. *Nordic Journal of Computing* 10, 2003.
- J.-P. Bernardy, P. Jansson and K. Claessen. Testing polymorphic properties. *ESOP*, 2010.
- P. Duchon, P. Flajolet, G. Louchard and G. Schaeffer. Boltzmann samplers for the random generation
  of combinatorial structures. *Combinatorics, Probability and Computing* 13, 2004.
- J. Duregård, P. Jansson and M. Wang. Feat: functional enumeration of algebraic types. *Haskell
  Symposium*, 2012.
- P. Dybjer. A general formulation of simultaneous inductive-recursive definitions in type theory.
  *Journal of Symbolic Logic* 65, 2000.
- J.-Y. Girard. *Interprétation fonctionnelle et élimination des coupures de l'arithmétique d'ordre
  supérieur*. Thèse d'État, Université Paris 7, 1972.
- P. Martin-Löf. *Intuitionistic Type Theory*. Bibliopolis, 1984.
- J. C. Reynolds. Types, abstraction and parametric polymorphism. *Information Processing 83*,
  IFIP, 1983.
- B. Russell. Mathematical logic as based on the theory of types. *American Journal of Mathematics*
  30, 1908.
- A. Tarski. *Pojęcie prawdy w językach nauk dedukcyjnych* (The concept of truth in the languages of
  the deductive sciences), 1933.
- P. Wadler. Theorems for free! *FPCA*, 1989.
