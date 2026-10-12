# 1. Terms and notation

Chapter 1 of the specification of Luthier, draft 0, 2026-10-12. Sources: the notation sections of
`docs/spec/04-kernel.md`, `docs/spec/05-static-semantics.md`, `docs/spec/06-numbers.md`,
`docs/spec/08-tests.md` and `docs/rationale/09-extern-and-the-world.md`, all at d12b554, merged so
that each symbol appears once; the words of the language are those of the Terms of
`docs/principles.md`. Written by Claude Sonnet 5.5. It realizes the Terms and D-2026-10-12-z.

The words structure, predicate, cost, law, theory, model, function, dependences, certificate,
grade, evaluation, execution, demand, planner, declarative face, executive face, object, specimen,
resources and world are defined in the Terms of `docs/principles.md` and nowhere in the
specification; a chapter uses them as the Terms give them. This chapter holds the symbols.

## §1 The judgment and the acts

**1.S1. The judgment.** [implemented] `x : T` reads "x refines T": x is a subset of the inhabitants
of T, a single one when x is a value, so that for a value it reads "x is a T" (the refinement
order is `A <: B` of 1.S10; the rules that check it are in `spec 4`). `U` is the type of types.

**1.S2. The acts.** [implemented] `x : T := t` gives the name x the type T and the body t.
`x : T` alone declares x with no body: a hole. `x = t` makes x an alias of the term t. A top-level
act is one of these three, and the name it introduces is qualified by its module prefix (`spec 12`).

## §2 Terms

**1.S3. Equality and substitution.** [implemented] `≡` is definitional equality: two terms that
reduce to the same normal form (`spec 3`). `t[a/x]` is t with every free occurrence of x replaced
by a. The equality a type comes with, as opposed to `≡`, is O2.

**1.S4. Binders and types.** [implemented] `\ x { t }` is the function with parameter x and body t.
`(x : A) -> B` is the dependent function type, B possibly mentioning x, and `A -> B` when it does
not. `(x : A) * B` is the dependent product, `A * B` when B does not mention x. `{ x : A, y : B }`
is a product with labels x and y (its labeled base), and `{ x : T | p x }` is the subtype of T
where the predicate p holds (`spec 4`).

**1.S5. Letters.** [implemented] A, B, T stand for types, that is for terms of type U; a, b, t, f,
p for terms (p usually a predicate); x, y, l for names, variables or labels. A letter outside this
list is defined where it first appears in a chapter.

**1.S6. Structural and nominal.** [implemented] A type is structural when its shape identifies it:
two structural types written alike, up to the names of their binders, are the same type. It is
nominal when its name identifies it: a definition makes a new type, distinct from every other.

## §3 The dependency graph

**1.S7. Dependence sets and occurrence.** [implemented] D(n) collects the names found in the
declared type of the name n, and B(n) those found in its body. Occurrence is read on the syntax
once elaborated and with aliases expanded; a constructor or a label counts as its type, and a
projection `e.f` counts what e contains. An occurrence is in type position when the occurring term
has type U or is a type operator: the declared type of a definition, the annotation of a binder,
the base of a subtype, the parts of a product, sum or function type, the arguments of a type
operator. Every other occurrence is in term position.

**1.S8. The graph, theories and branches.** [implemented] The dependency graph has the names as
nodes and an edge `n -> m` whenever m is in D(n) or B(n). A theory is a strongly connected
component of this graph: a maximal set of names each reachable from each other, and a name no cycle
passes through is a theory of one name, the one-symbol function type included. Where a source says
"object" for the cycle, this chapter writes "theory" (D-2026-10-12-z); the word
object keeps the wider sense of the Terms. A branch of a theory O is a name outside O with an edge into O. A law touches the
names and labels that occur free in it.

## §4 Numbers and measures

**1.S9. Sets and constants.** [implemented] ℤ, ℚ, ℝ are the integers, the rationals and the reals
as mathematical objects; `Int`, `Rational`, `Real`, `Float64` are the Luthier types that
represent them (`spec 11`). `u = 2^-53` is the unit roundoff of IEEE binary64, half the distance
from 1 to the next double. `x ⊕ y` is the sum a machine computes on two doubles, the double
nearest to x + y.

**1.S10. Refinement.** [implemented] `A <: B` reads "A refines B": every value of A is a value of
B.

**1.S11. Symbols across chapters.** [proposed] The merged sources defined only some of these; the
rest are fixed here so that no chapter redefines them.

| Symbol | Meaning | Used most in |
|---|---|---|
| ε | the cutoff (tolerance) of a demand, a parameter of the demand (D-2026-10-12-h) | `spec 8` |
| d | a distance, the equality of a metric space read as a cost (O2); laws have the form d(f x, g x) ≤ ε | `spec 5` |
| κ | the condition number of a matrix: largest singular value over smallest | `spec 11` |
| L | a Lipschitz constant, the bound of a cost's change per unit of its argument | `spec 5` |
| p | a predicate in a subtype; in a statistical law, a probability | `spec 4`, `spec 7` |
| n | the number of cases a test asks for, or of samples drawn | `spec 7` |
| α | the level of a statistical law: its probability of failing when the model it tests is correct | `spec 7` |
| β | the power of a statistical law against a given wrong model: its probability of failing then | `spec 7` |
| δ | the confidence parameter of a sampled certificate, the demand's parameter; confidence is 1 − δ (D-2026-10-12-r) | `spec 6` |
| ε̂ | the bound on the failure fraction from n samples at confidence 1 − δ; a sample converts to the evidence cost −log(1 − ε̂(n, δ)) in nats (D-2026-10-12-r) | `spec 6` |
| Φ | the distribution function of the standard normal | `spec 7` |

**1.S12. Cost and grades.** [decided D-2026-10-12-y] `Cost` is the type of the costs defined in the Terms (`spec 5` gives its algebra). The grades of a certificate are the five of
the Terms (proved, exhaustive, cases, sampled, assumed); the domain and the evidence cost carry
what the older grades point, census of k, bounded and witnessed said, and the grades of `05 §7`
(point, sampled, bounded, exhaustive, witnessed, proved, assumed) are read through that
correspondence. What an `assumed` certificate records is D-2026-10-12-t.

## §5 Tests and certificates

**1.S13. Words of tests.** [implemented] Each is used and defined in full by `spec 7`.
`Gen T` is the type of generators of T (G1). A case gives a value to each parameter of a law, its
parameters being the variables it quantifies over. The size `s : Nat` bounds lengths and depths. A
seed is a value of `Seed`, an integer in [0, 2^31). The support of a generator is the set of values
it gives with nonzero probability, and its measure says how likely each part of the support is. A
binding maps parameters, or types, to generators, and a profile is a binding with a name. A census
is a finite list of values given explicitly. The reach of a certificate entry is what its
generators covered, parameter by parameter: one value, the k values of a census, a whole finite
type, or an interval with its measure. A cost `c : T -> Float64` used as a weight is the density of
a measure, with respect to counting on a finite support and to length on an interval of numbers,
and C is the total cost of a support.

**1.S14. Words of the world.** [implemented] A pointer is a value that designates a part of the
world; a token is the value of a pointer after an operation on it, carrying the order of the
operations; a trace is the record of a run, its operations partially ordered by their
dependencies, with their results and costs; an observation is a function from a part of the world
to a value, and a functor of observation is one that commutes with composition of operations
(`spec 10`).

## §6 Accept and reject programs

**1.S15. The two kinds of program.** [implemented] A rule names programs in `tests/spec/`. A file
`<name>.accept.lut` must load without error. A file `<name>.reject.lut` must fail to load, and
carries a line `-- expect: <fragment>`, the text the failure message must contain; a reject file
without that line is itself a failure of the suite (`tests/test_spec.py`). A rule ends with
`Files: <name>.accept.lut, <name>.reject.lut.`, naming one program of each kind; a chapter's
statements (`N.Sk`) name none.

## Open

O2 (the equality a type comes with) is the one open point that touches the notation: 1.S3 uses `≡`
and the structural equality, and which equality a type names is not settled.
