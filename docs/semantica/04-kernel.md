# The kernel: the canonical presentation of Luthier

Draft 1, 2026-10-04. The constructs every Luthier program reduces to, how each one computes,
and the surface forms that translate into them. `05-static-semantics.md` states, on this
kernel, what makes a program well formed; together the two are the technical specification
of version 0. Both supersede the parts of `00`–`03` that contradict them; those documents
carry dated notes pointing here.

Luthier, like any mathematical object, admits several presentations: other choices of
primitives that are equivalent to this one (`05 §9`). This is the one chosen to start with.
The criterion of the choice is that the rules of `05` can be stated directly on it, without
going through a translation; minimality is not the criterion, and the subtype is primitive
although it is derivable.

## 0. Notation

Every symbol used in this document.

- `x : T` reads "x refines T": `x` is a subset of the inhabitants of `T`, a single one when
  `x` is a value (`05 §1`).
- `x : T := t` gives `x` the body `t`. `x : T` without `:=` is a declaration.
- `x = t` makes `x` an alias of the term `t`.
- `≡` is definitional equality: two terms that reduce to the same normal form.
- `t[a/x]` is `t` with every free occurrence of `x` replaced by `a`.
- `A`, `B`, `T` stand for terms of type `U`; `a`, `b`, `t`, `f`, `p` for terms; `x`, `y`, `l` for
  names (variables or labels).
- "Structural" means that a type is identified by its shape: two structural types that are
  written alike, up to the names of their binders, are the same type.
- "Nominal" means that a type is identified by its name: a definition makes a new type,
  distinct from every other.

## 1. Acts

A program is a set of top-level acts without order (`05 §2`). There are three, and three
directives.

| act | form | what it does |
|---|---|---|
| declaration | `x : T` | introduces `x` with its base `T` and no body: a hole |
| definition | `x : T := t`, or `x := t` filling an earlier declaration | gives `x` a body |
| alias | `x = t` | makes `x` stand for `t`; expanded before checking; no states |

A data definition `x : U := data { ... }` is a definition whose body is a `data` term
(section 2). The body of a definition is a term, a `data`, or `extern "target"` (section 4).
Two more bodies are decided, not implemented (`06`): `primitive "..."`, a type the interpreter
provides, and `axiom "..."`, a value whose laws are assumed.

Directives: `import "file" [as m]` (`03`), `test x [with n | exhaustive] [size k]` (`05 §7`),
`gen T := g` (the generator of `T`), and `operator op := f` (the meaning of an infix operator
on the argument types of `f`). Directives are not definitions and have no states.

## 2. Type formers

| former | anonymous | with names | introduction | elimination |
|---|---|---|---|---|
| universe | `U` | | every type | |
| exponential (Π) | `A -> B` | `(x : A) -> B`, `B` may mention `x` | `\ x { t }` | application `f a` |
| product (Σ) | `A * B` | `(x : A) * (y : B)`, `B` may mention `x`; n-ary `{ x : A, y : B }` | `(a, b)`; `{ x := a, y := b }` | pattern `(x, y)` in `match`; projection `e.x` |
| sum | `A + B` | `(x : A) + (y : B)`; n-ary `< x : A \| y : B >` | `x a`, by label | `match` on labels |
| empty | `Empty` | | none | `match e { }`, of any type |
| unit | `Unit` | | `unit` | none needed |
| subtype | `{ x : T \| p }` | `{ x : A, y : B \| p }` | a term of `T` for which `p` holds (an obligation) | a term of the subtype is a term of `T` |
| recursive type | `data { c1 : ... ; c2 : ... }` | constructors are named | the constructors | `match` on constructors, with recursion |
| primitives | `Int`, `R`, `String` (to become `Int`, `Real`, `Float64`, `String`: `06`) | | literals `3`, `3.0`, `"a"` | arithmetic and comparisons |

Notes on each.

- **Exponential, product, sum** are primitive and structural. Their named forms are the same
  types with names for the positions: the names are binders, like the parameter names of a
  function, and are not part of the type's identity. `{ mean : R, var : R }`, `(m : R) * (v : R)`
  and `R * R` are the same type; `{ a : A, b : B }` and `{ b : B, a : A }` are different types
  (isomorphic, not equal). The reading where labels are the identity (a record as a function
  from its set of labels) is a translation, not an equality.
- **Anonymous sums** inject with the labels `left` and `right`: `A + B` is
  `< left : A | right : B >`. A sum of more than two associates to the right, and so does a
  product: `A * B * C` is `A * (B * C)`, like the tuple `(a, b, c)`, which is `(a, (b, c))`. An alternative of
  type `Unit` is injected by its label alone: in `< true : Unit | false : Unit >`, `true` is
  `true unit`.
- **Dependence.** In `(x : A) -> B` and `(x : A) * (y : B)`, `B` may mention `x`. A sum has no
  dependent form: only one alternative is present in a value, so no alternative can depend on
  another.
- **The subtype** `{ x : T | p }` has the inhabitants of `T` for which the predicate `p` holds.
  `p` is a term of type `Bool` with `x` free, or a `Law` (section 3). A term of `T` used where
  the subtype is expected creates an obligation (`05 §7`); a term of the subtype is accepted
  where `T` is expected, without any marker (`forget` is implicit).
- **Recursive types.** `data` is for types defined in terms of themselves: at least one
  constructor mentions the type being defined (`N`, `List A`, `Tree A`). A constructor
  `c : A1 -> ... -> An -> D` builds a `D` from its arguments. The type is *freely* generated:
  distinct constructors give distinct values, and each constructor is injective. Those facts
  are not axioms to state; they hold by construction. A non-recursive sum of products is
  written with the structural formers and named with an alias (`05` R4).
- **Primitives** (2026-10-05: to be written with the body `primitive "..."`, which says what each
  one is, and `R` to be replaced by `Real`, the ideal, and `Float64 : Real`, the finite doubles;
  `06-numbers.md`) are holes of the kernel filled by the interpreter: their literals,
  arithmetic, comparisons and structural equality. `R` is an IEEE double. What can be said
  about them (epsilon, approximate equality) is library (`lib/real.lut`).

The kernel is therefore a bicartesian closed category (products, sums, exponentials, a
terminal and an initial type) with the dependent forms of the product and the exponential,
recursive types, and subtypes.

## 3. Terms

Besides the introductions and eliminations of section 2:

- **Names.** A defined name stands for its body; a declared name is a hole and does not reduce.
- **`match`.** `match t { p1 -> t1 ; ... }` with one branch per constructor or label of the
  type of `t`, none repeated and none missing, unless a variable or `_` branch catches the
  rest. Patterns: a constructor or label applied to patterns, a tuple `(p, q)`, a literal,
  a variable, `_`.
- **Recursion.** A definition with a declared type may mention itself in its body, and
  definitions may mention each other. Recursion is general: nothing guarantees termination,
  and evaluation runs with a step budget (fuel). The recursor of a `data`, the function that
  consumes it by saying what to return on each constructor given the results on the
  recursive arguments, is a library definition written with `match` and recursion:

      recN (P : U) (z : P) (s : N -> P -> P) (n : N) : P := match n { zero -> z ; succ m -> s m (recN P z s m) }

  It is the fold of the type (`foldr` for `List`). A proof layer would make it primitive and
  forbid general recursion, so that every function terminates; version 0 tests and does not
  need it.
- **Laws.** A law is a term of type `Bool`, or a function into `Bool` whose parameters are
  quantified, or a conjunction `p & q` of laws, of type `Law`. `Law` is the type of what a
  test runs (`05 §7`).
- **Extern.** `extern "python:module.function"` is a value the environment provides, with the
  type the context gives it (`05` R5). `extern provisional "..."` is the same value, marked as
  debt.

## 4. Reduction

Evaluation reduces terms by these rules, each a definitional equality:

- **beta**: `(\ x { t }) a ≡ t[a/x]`;
- **delta**: a defined name reduces to its body; aliases are expanded before checking, so they
  never reach evaluation;
- **iota**: a `match` on a constructor, a label injection or a pair reduces to the branch that
  matches, with the pattern variables substituted;
- **prim**: arithmetic and comparisons on literals of `Int`, `R`, `String`; `==` on values of
  types with structural equality (`05` R8);
- **extern**: an extern applied to as many closed arguments as its type has parameters calls the
  environment and converts the result back.

A name is unfolded in head position only when that makes progress, so a recursive function
applied to an argument that does not reduce further stays folded. A term that contains a hole
in a position the reduction needs does not reduce.

## 5. Surface forms and their translations

Everything below is sugar: each form translates into the kernel, and a form that needed a new
kernel construct would not be sugar (`02 §4`).

| surface | kernel |
|---|---|
| `f (x : A) (y : B) : C := t` | `f : (x : A) -> (y : B) -> C := \ x { \ y { t } }` |
| `(x y : A)` in a binder | `(x : A) (y : A)` |
| clauses `\| p, q := t` under a header with parameters | a `match` on the tuple of parameters |
| `if c then a else b` | `match c { true -> a ; false -> b }` |
| `a and b`, `a or b`, `p -> q` with `p : Bool` | `and a b`, `or a b`, `implies p q` |
| `[a, b, c]` | `cons a (cons b (cons c nil))`, element type from the expected type |
| `{ x := a, y := b }` | `(a, b)`, checked against a type with components `x`, `y` |
| `e.y` | a one-branch `match` on the component pattern of the type of `e` |
| `m.f`, `m` an imported module | the definition `f` of module `m`; a module is a record of its definitions (`03 §1`) |
| `{ x : A, y : B }` | `(x : A) * B`, with the last component also named |
| `< x : A \| y : B >` | `(x : A) + (y : B)` |
| `Bool` | `< true : Unit \| false : Unit >`, in `core.lut` |
| `Maybe A` | `< nothing : Unit \| just : A >` |
| `\ (x, y) { t }` | `\ p { match p { (x, y) -> t } }` |

## 6. Primitive versus derived, and native versus extern

Two different senses of "primitive" must not be confused.

- *Semantically primitive* is what the kernel has: the formers of section 2 and `Int`, `R`,
  `String`. Every other type is defined natively from them (`05` R5).
- *Primitive for performance* is an extern: a value computed by the environment because it is
  faster there. A numpy array is not a primitive type: with `Fin n = { k : Int | 0 <= k and k < n }`,
  `VecOf n` is natively the function type `Fin n -> R`, a matrix is `Fin m -> Fin n -> R`
  (a vector of vectors, by currying), and a numpy array *is* a value of that type. Nothing is
  converted and nothing about the representation needs certifying: indexing an array that was
  built from a function gives back that function's values exactly.

A value of a function type with a finite domain can therefore be a Luthier lambda or an object
of the environment, and the interpreter has three rules for it:

1. *Applying an object of the environment.* If `v : Fin n -> A` came from Python, `v i` evaluates
   as `v[i]`. The interpreter checks `0 <= i < n` itself, because that is the obligation of
   `Fin n` and Python would accept `v[-1]` silently.
2. *Passing a lambda to the environment.* A Python function that expects an array and receives a
   lambda over `Fin n` gets the array of its `n` values: the interpreter evaluates it at every
   index (it *materializes* it), which is possible only because the domain is finite. The cost
   is `n` evaluations; a materialized value is kept so it is not built twice.
3. *Representation by type.* `Fin n -> R` is a one-dimensional ndarray, `Fin m -> Fin n -> R` a
   two-dimensional one, `Fin n -> A` for a non-numeric `A` a list; a vector of unknown length,
   `(n : Int) * (Fin n -> R)`, is the pair `(arr.shape[0], arr)`. The shape is checked when the
   value crosses: an array declared `VecOf 3` must have shape `(3,)`.

4. *Each entry once.* A lambda over `Fin n` is a table: the interpreter computes each of its
   entries at most once, as it computes each argument once (call by need). The semantics does not
   change, since functions are pure; without it, an iterative algorithm written with lambdas
   (Jacobi's rotations, each a lambda over the previous one) recomputes its whole history at every
   read.

Two values of a function type, one a lambda and the other an array, are compared by an
observational equality, point by point over `Fin n` (`05` R8); since the domain is finite the
comparison is exhaustive.

The order of a sum is part of its rounding. `sumTo n f` is `f 0 + (f 1 + (... + (f (n - 1) + 0.0)))`;
written the other way it gives a result that differs in the last bits, which an optimizer
downstream amplifies. The rewrite of experiment zero reproduced its earlier results bit for bit
only once the order matched.

What does need certifying is that the operations the environment provides compute what their
native definitions say. A function may be given natively, as an extern, or both. Writing it
both ways is worth it only where the extern is in doubt; then a law compares them on generated
inputs:

    AddAgrees (ad : Vec -> Vec -> Vec) (n : Dim) (x y : VecOf n) : Bool := approxVec 0.0 (ad x y) (addDef x y)

`addDef` is the native definition; `test` runs the law with `ad` bound to the extern. The
libraries call these laws `Agrees`; the name is local to Luthier.

## 7. Status of the interpreter

Implemented on 2026-10-04 (branch `kernel-v0`): every former and term of sections 2 and 3, the
surface forms of section 5 except those noted below, the reduction of section 4, and the four
rules of section 6. `tests/spec` (the accept/reject programs) and `tests/test_kernel.py` pass.

Not yet: quote and unquote; local definitions in a block; a union `< ... >` written as the
argument of an application needs parentheses (`List (< a : A | b : B >)`), because `<` after a
term is a comparison.
