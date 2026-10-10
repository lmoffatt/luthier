# Recursive types, objects, and `if`: answer to Luciano's note of 2026-10-11

Source: `record/Lucianos ideas/El problema de las tipos recursivos.txt` (committed verbatim at
f0e9c5d and 0cbe437). Written by Claude in the chat of 2026-10-11, at Luciano's request. What
cites the spec is marked by its section; what is proposed here is marked *Proposed*.

## 1. `std::vector` from `std::array`

With products, sums, exponentials and their dependent forms, `Vector N` is `Fin N -> A`, the
analogue of `std::array<N>`. The analogue of `std::vector` is the dependent pair that hides `N`:

    Array (A : U) (n : Nat) = Fin n -> A
    Vec   (A : U)           = { n : Nat, f : Fin n -> A }

This is already in `docs/spec/06-numbers.md` §7, and `04-kernel.md` §6 crosses it to numpy as the
pair `(arr.shape[0], arr)`. The length leaves the type and becomes the first component of the value.

Products, sums and exponentials alone give no container of unbounded length. One needs either a
fixed point (`data List A`, the least solution of X = 1 + A * X) or a dependent pair over `Nat`,
and `Nat` is itself a fixed point (or, as `06` §2 has it, a subtype of `Int`). Neither route is
naive in the strict sense; the spec has both (`04` §2, *Recursive types*).

`List A` and `Vec A` are isomorphic, not equal: two presentations of the free monoid on `A`, by
constructors and by index. Which one a program uses follows from what is demanded of it (L19, the
demand determines the computation): `Vec` for `f i` and linear algebra, `List` for consuming
element by element.

What `std::vector` has beyond its type (`push_back`, capacity, amortized growth) is state and
representation. By L18 (a definition has no effects) it is not in the type: `push_back` is
`Vec A -> A -> Vec A`, and reusing a buffer is the business of the extern.

*Proposed.* Predicates on the length come from the subtype with nothing added to the kernel:
`{ v : Vec A | v.n > 0 }`, or two vectors of one unspecified length.

## 2. Hiding every modifier: objects

Luciano's note: "del mismo modo podriamos esconder todos los modificadores de cualquier tipo, no?
En particular los objetos matematicos?", with

    monoide : U := monoide { T : U, op : T -> T -> T | leyesdeMonoide T op }

This is the spec's definition of a theory (`05` §2: "a theory is a subtype of a labeled base") and
the reading of a file as a dependent record (`03` §1). Two remarks.

**Carrier inside or outside.** `Monoid (T : U)` is the monoids on `T`; with `T : U` inside, the
record is an existential and its user cannot see `T`, only `op`. That is the abstract data type,
the object of object-oriented programming (J. C. Mitchell and G. D. Plotkin, "Abstract types have
existential type", ACM TOPLAS 10, 1988). The record contains `U`, so it lives one universe up;
version 0 ignores universe levels and the point is noted here only.

**Hiding is forgetting.** An inner product needs the shared `n` of its two vectors; over `Vec` it
cannot be written without `v.n = w.n`. By L13 (forgetting is determined by the demand) a modifier
is hidden when no demanded value needs it, typically at a boundary, and is kept in the type while
the computation uses its equations.

## 3. The constructor into `Maybe`, and `if`

Luciano's note:

    monoide (T : U) (op : T -> T -> T) -> Maybe monoide :=
    if (leyesdeMonoide T op -> monoide { T op }

This is `refine` (`05` §5, *Checks*) with the record as `T` and the laws as `p`. It works as
written only when the condition is a `Bool`. Associativity quantifies over all of `T`: it is a
`Law` (`04` §3), and over an infinite carrier no `if` can evaluate it. Three cases:

- A predicate decidable per value (`Fin n`, a non-empty vector, a Cholesky factor): `refine`,
  `just` or `nothing`.
- A law over a finite carrier (`Fin 3`): decidable by exhaustion, as the generators of `08` do.
- A law over an infinite carrier (`Int`, `Float64`): writing `m : Monoid := { T := Int, op := plus }`
  raises the laws as obligations and `luthier test` certifies them with a grade (`05` §7). What was
  `just` or `nothing` becomes certified, failed or pending, with its `n`.

Same dependent pair, same predicate; what changes is who decides, the interpreter or the
certificate. This is where `std::vector` and a mathematical object differ: the predicate of `Vec`
is decided value by value, that of a monoid is tested.

### How `if` is written

In the spec today (`04` §5, `05` R11):

- `if c then a else b` is sugar for `match c { true -> a ; false -> b }`, with `c : Bool` and
  `Bool = < true : Unit | false : Unit >`. Both branches are required.
- Inside `a`, a variable `x` tested by `c = p x` has the type `{ x : T | p x }`; inside `b`,
  `{ x : T | not (p x) }` (R11, decided, not implemented).
- A check whose evidence must outlive the branch returns the refined value:
  `match refine p x { just y -> ... ; nothing -> ... }`.

*Proposed* (needs Luciano's decision, it changes the grammar):

1. **A one-armed `if` is a guarded value.** Luciano's note writes `if c -> v` with no `else`.
   Without effects (L18) a branch that does nothing has no meaning, so the only reading is
   `if c then just v else nothing`, of type `Maybe`. Then `refine p x` is `if p x then x`, and
   the constructor of the note is valid syntax as written.
2. **A `Law` is not a condition of `if`.** `if` takes a `Bool`. A constructor whose condition is a
   law is written without `if`: the record is built and its laws are obligations. Branching on the
   outcome of a test is a `match` on its verdict (certified with a grade, failed with a
   counterexample, pending), not on a `Bool`, because a test does not establish the fact (`05` §5,
   *A statistical verdict*).

Neither proposal adds a kernel construct: the first is sugar into `match` and `just`, the second a
restriction the type checker already makes.
