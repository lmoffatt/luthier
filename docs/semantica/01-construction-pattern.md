# The construction pattern: laws that are tested

Rewritten on 2026-10-04 from the Spanish draft of 2026-09-29 (`01-patron-de-construccion.md`, in
the history), against `04-kernel.md` and `05-static-semantics.md`. The previous document set out
the kernel; this one sets out how Luthier is used: a type with laws, a value of it, and the test
that certifies the value.

## 1. Version 0 tests, it does not prove

A law is a Bool-valued function whose parameters are quantified: `Associative A eq f x y z`.
Running it is drawing values for the parameters, evaluating, and recording a counterexample if it
gives `false`. The unit of specification is the group of functions with the laws that relate them;
a function with a postcondition is the group of size one. `read (write s k a) k == a` is not a
postcondition of `read` or of `write`: it relates both, so they are defined together.

When the proof layer comes, the same law becomes a type whose inhabitant is a proof; the concept
does not change, only the grade of its certificate.

## 2. The subtype is the definition of a type

    Codec : { parse : String -> Maybe Table, render : Table -> String, eq : Table -> Table -> Bool }
    RoundTrip (c : Codec) (t : Table) : Bool :=
      match c.parse (c.render t) { nothing -> false ; just u -> c.eq t u }
    Codec := RoundTrip & Rejects

A type is declared over a base with labels, its laws are written over that base, and the type is
defined by them. Declaration, laws and definition form a cycle of the dependency graph, which is
the object (`05 §3`). The laws must touch every label: a component no law mentions is a bare
function juxtaposed to the rest, and `{ ... | true }` defines nothing (`05` R3). The same thing
can be written in one line, `Ring (A : U) : U := { eq, add, mul, zero, one, neg | laws }`.

Two kinds of object come out of this, told apart by the form of the definition (`05 §1`):

- a *concrete type* is defined natively, from the kernel: a `data`, an exponential, a product, a
  sum, a subtype of those. Its values are built by its constructors. `Vec` is
  `{ n : Nat, f : Fin n -> Float64 }`; a value is built by giving a length and a function.
- a *theory* is a subtype of a labeled base, usually parameterized: `Group (A : U)`, `Codec`. It
  has no constructors of its own; its values are its *models*, records of operations that satisfy
  its laws. `csv : Codec := { parse := extern "...", render := extern "...", eq := sameTable }` is
  a model; so is `ringZ7 : Ring Z7`.

An implementation is always a value. The environment provides values, never types (`05` R5): a
Python implementation of a theory is a record of externs, and certifying it is testing the laws of
the theory on that record.

## 3. Equality is part of the presentation

Most laws compare two things. On `Int` and on data, `==` is structural and decidable; on functions,
and on anything that contains one, it is not (`05` R8). A theory therefore carries its own equality
as a component, as `Ring` carries `eq` and `Codec` carries `eq`: exact on `Int`, within rounding on
`Float64`, entrywise within rounding on vectors, cell by cell on tables. The laws are written against
that equality once and hold for every carrier.

## 4. The certificate

What is certified is a law applied to particular values, over a domain, by a mode (`05 §7`): one
case, `n` sampled cases, every case of a finite domain, a witness for an existential law, or a
proof. A certificate records the law, the values, the grade with its `n`, the generators, the
seed, the first cases, and the hash of the definition's dependency cone. Two values of the same type
with different certificates do not carry the same guarantee; the type does not tell them apart,
the certificate does.

Failure and certificate are the same record: a failure is a law with its counterexample.

## 5. Relation to the concepts of C++

The pattern is a C++ concept (a named predicate evaluated before use) with four extensions, all
consequences of the predicate being an ordinary function: its domain is not only types but values,
functions, groups of functions and programs; it checks semantic requirements, not only syntax; it
checks them exactly on values and statistically on functions; and what was checked is kept in the
certificate and travels with the value instead of being checked again at every use.

Short form: Luthier is concepts carried through the whole language, with semantic requirements
that run and whose result is kept.

## 6. Characterize, do not reimplement

The laws of an object say what it is, by the properties that determine its operations. The inner
product of a Euclidean space is the bilinear, symmetric, positive form for which the standard basis
is orthonormal; from that, `dot x y` as a sum of products is a theorem. A determinant is the
multilinear alternating function of the rows with `det I == 1`; Laplace's expansion is one way to
compute it. Written this way, the laws are the mathematics of the object, and any implementation
is a model of them.

What is not a law: a second implementation. "The fast `dot` equals the slow `dot`" says the two
agree, which is useful, and says nothing about what either computes; both could be wrong together.
The libraries were first written that way, with a native definition as the reference and a law
`...Agrees` per leaf, and `07-characterizations.md` records what each object's laws should be
instead. Where an object is characterized, a native definition and an extern are two models
certified against the same laws, and their agreement is a corollary (`05` R10).

Some characterizations need a witness (the maximum of a vector is an entry of it; a spectrum comes
with its eigenvectors): an existential law, which version 0 cannot run (`05 §10`). Until it can,
the law is written with the witness as one more component (`eigen` returns the vectors with the
values), or stays as the universal half with the existential noted.

## 7. Example: a store

`S` is the state, `K` the keys, `A` the values.

    Store (S K A : U) : { write : S -> K -> A -> S, read : S -> K -> Maybe A, eqA : A -> A -> Bool }

    ReadAfterWrite (S K A : U) (st : Store S K A) (s : S) (k : K) (a : A) : Bool :=
      match st.read (st.write s k a) k { nothing -> false ; just b -> st.eqA b a }

    Store (S K A : U) := ReadAfterWrite S K A

The law that a write leaves the other keys alone (`k /= k' -> read (write s k a) k' == read s k'`)
is what keeps a `write` that erases everything else from passing; it needs an equality on `K` and
on `Maybe A`, which the theory would carry as further components. And `read` on an absent key has
nothing to return, so its type is `Maybe A`: the law forces the decision.

## 8. Open

- Generators of models: a law quantified over every model of a theory has no generator and is
  certified model by model (`05 §7`).
- The semantic tests of dependence and connection (`05 §4`), with the grade "witnessed".
- Equality as a degree, for samplers (`05 §10`).
