# Layers 0 and 1: four questions for Luciano

2026-10-13, by Claude Opus 5.5 (the coordinating session), from the questions the session writing
the theories (luthier-03) raised on `term.lth`, `translation.lth`, `program.lth` and
`kernel_laws.lth`, before their external review. Each is undone by one commit; each carries the
recommendation of both sessions. Mark under each: "ok", "no", or a comment. The answers go to
`record/decisions.md`.

## Q1. Records in the kernel keep their names

`Term`'s dependent product (`Sigma`) names only its first component, so a record type
`{ x : A, y : B }` loses the name `y` when it is translated into the kernel, though 2.S12 says the
last component is named too. Either `Term` gains a record former,
`Record : List (String * Term) -> Term`, whose names are part of the term and of its hash, or the
translation keeps the names outside the term.

Recommended: the record former. The names of the fields are part of the type, so they belong in
the term, not beside it.

La idea es la siguiente: en teoria de categorias un producto tiene las flechas first y second, aqui las flechas 
serian   .x  y .y  o sea forman parte del product. 
lo mismo de la suma pero como funcion inyectiva. 
Responde eso a tu pregunta?


## Q2. A block is a lambda applied

The kernel has no `let`, so `translation.lth` translates the block `{ x := a ; e }` as
`(\ x { e }) a`. 2.S12 calls a block "a sub-DAG with one output". The alternative is a `Let` in
`Term`, which makes the sharing explicit for the planner (spec 8).

Recommended: keep the lambda applied, no new kernel construct, by L7 (the core is small); the
planner sees that `x` is shared all the same.

ok, aqui estamos hablando de bloques de ejecucion, esta bien, es lo que leo. 
la pregunta es si no usar la notacion de C++ para los lambdas [](e:X, j:J) { e+j ;} 
y si no usar el return ? 
discutime. 
O sea nos apartamos de lo muy lambda y vamos a algo mas entendible?


## Q3. Helper functions in theory files are reported, not rejected

Every theory file has helper definitions with parameters (`member`, `concat`, `freeVars`), which
12.S23 allows ("the definitions its laws need"); `program.lth` reports them as loose functions
(4.S17, D-2026-10-07-e) without rejecting them.

Recommended: keep reporting them; decide, once local definitions exist in the language, whether a
helper that a law needs is exempt or must become local to the law.

yes because we want that everything has an underlying law. 



## Q4. The laws of `Nat`

You said "Nat tiene las suyas" (D-2026-10-13-t). `kernel_laws.lth` §5 states an ordered commutative
semiring: `+` and `*` with their units, associativity, commutativity and distribution, and the
order laws (total, compatible with `+`, `0` the least), the order marked proposed.

Recommended: accept as written. The coordinating session asked that the successor have its role
and that no other naturals exist; done at 0381962: `Nat` is `{ k : Int | 0 <= k }` (11.R1), with no
`succ` constructor, so the role is the successor `x + 1`, and `SuccessorIsNext` (nothing strictly
between `x` and `x + 1`) with `ZeroLeast` says every natural is reached from `0` by successors.
Induction itself quantifies over predicates and cannot be tested, the same limit as `List`'s fold.

Ok


## Q5. Substitutivity belongs to the structural equality

Raised by the session writing the theories, from a counterexample of the Codex writing `kernel.py`:
`\ x { x }` and `\ y { y }` are alpha-equal, yet a function that reads the binder's name tells
them apart. It is not peculiar to alpha: no observational equality (alpha-equivalence of terms,
doubles within a tolerance) is substitutive over every function. Your D-2026-10-12-ak says an
object is a type with its equality, whose laws (reflexive, symmetric, transitive, substitutive)
the kernel guarantees for a structural `==` and the author states for an observational one.

Recommended, as `kernel_laws.lth` §1 now reads (9a89873): an object's laws are reflexive,
symmetric, transitive; substitutivity over every function is the structural equality's; an
observational equality is respected by the operations of its own theory, each stating it as a
congruence (`AlphaCongruent` in `term.lth`). 3.S36 and 5.S4 would say so. No cost in code; the
setoid of O2 becomes the textbook one, an equivalence with congruence for the theory's operations.


