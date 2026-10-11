# Third round: blocks, operators and models, theories everywhere, citations

Source: Luciano's feedback on the second round, committed verbatim at 9d65118 inside
`record/answers-annotations-principles-2026-10-11-b.md`. Written by Claude in the chat of
2026-10-11. What cites the spec is marked by section; the rest is *Proposed*. Two items are
decisions for him (blocks, operators); one he decided (mutation testing); one amends a decision
(citations).

## Blocks: the help he asked for

> si aceptamos la falta de orden de los statements, <- no podria tener lugar, porque dos <- suponen
> un orden. pero por otro lado, tambien dijimos que el orden esta dado por las dependencias, esto
> implica algo ligeramente complejo: el segundo <- deberia depender del primer valor asignado por
> el <- o estar en otro bloque ... Lo cual nos introduce al concepto de bloques. Y ahi te pido ayuda.

The tension dissolves once the two orders are kept apart: the textual order inside a block is
used for one thing only, to decide which binding a name refers to; after that, the block is
translated to a set of definitions with fresh names (`04 §5`: `y <- e` in a block is a fresh name
`y1 := e`, and every later `y` means `y1`; `05` R12), and from then on dependencies give the only
order, as everywhere else. So two `<-` do suppose an order, the order of reading, and that order
is consumed by the translation and does not survive into the program. Your alternative, that the
second `<-` must depend on the first, is the common case (the mutable parameter, `x <- f x`,
D-2026-10-10-e) but not a requirement: `x <- 1 ; x <- 2` translates to `x1 := 1 ; x2 := 2`, where
`x1` is dead and is freed (L13); legal, and a lint may say "unused binding".

         analiza si hay usos legitimos del caso de la no dependencia, porque si no los hay seria un code smell. 


*Proposed* semantics of a block, in six rules:

1. **Form.** A block is a brace term `{ s1 ; s2 ; ... ; e }` whose items are separated by `;` or
   line breaks, and whose last item is a bare expression, its value. A brace term with no final
   expression, `{ x := a ; y := b }`, is a record value, as today. That settles the collision of
   `02 §8` by the last item, with no new keyword. The body of a lambda, `\ x { ... }`, is already a
               aca cabe la pregunta somos C (siempre ;) o somos Python (supongo que ; es equivalente a line break)

   block in this sense (`02 §3`), and so is the body of a definition written with braces.
2. **Items.** `x := t` (once), `x <- t` (bind or rebind), an action with its result bound
   (`w <- print w "..."`, below), and nothing else. `<-` exists only here, in a parameter's default
   and in a named argument (R12). The top level of a file stays a set of acts.
3. **Translation.** Each item becomes a definition with a fresh name; `x <- t` becomes `xk := t`
   with k the number of bindings of `x` so far in the block, and every later `x` means `xk`. The
   result is a sub-DAG with one output, the value of the last expression. Order among items that do
   not refer to each other is not significant, so items commute after translation, as L9 says.
4. **Scope.** A name bound in a block is visible from its binding to the end of that block, and
   inside blocks nested in it, not outside. A `:=` of a name already defined in an enclosing scope
   or at the top level is an error (defined twice), not a shadowing; definitions are unique. A
   `<-` may rebind only a name first bound with `<-` in the same block or a parameter of the
   enclosing definition, since a parameter is `<-`-bound (its default is its first binding and the
   call rebinds it, D-2026-10-11-c). That is exactly what the mutable parameter needs and nothing
   more.
5. **The world.** Actions take and return the world: `w1 <- print w0 "x"`. The order among actions
   is then the dependency chain through `w`, not the text, which is what L12 (draft 3) asks for:
   an action is a function from the world before to the world after, and its laws speak of the
   two. Two actions that do not share a world value are unordered and may run in any order or at
   once. In a session the world is the implicit `w` of the session block; in a file, of `main`.
6. **Boundaries.** Three kinds of block and nothing else: the body of a definition or lambda; a
   `main` block in a file (the script); the session (a block typed incrementally, second round
   §17). A file is never a block.

What this gives: `<-` has a place without giving files an order; the mutable parameter, defaults
and named arguments are one mechanism; actions are ordered by data, not by text; the session and
the script are the same object. What it costs: the record-against-block rule by the last item,
which a reader must learn, and the no-shadowing rule, which makes some names longer. Decision for
you, by rule; the six go to the spec (`02 §3`, `04 §5`, `05` R12) if you accept them.

            Aqui estoy pensando que deberiamos tener una forma de expresar en Luthier un orden de ejecucion, lo cual es util para la fase de ejecucion, ya que permite expresar que dos ordenes son equivalentes. Porque la fase de ejecucion se expresa en Luthier, como dijimos. 



## Operators and models

> te parece que i:Int vs j: Ring 7 son el mismo tipo? claramente no lo son, por mas que
> internamente sean integer... un valor pertenece a un tipo de un modelo, y ese modelo tiene sus
> operadores. Claro que podrias tener operadores para modelos mas amplios, pero ahi entiendo que
> deberia haber coincidencia de leyes, cosa que no ocurre en otros lenguajes de programacion...

You are right and my scope proposal was wrong; I withdraw it. The example in the repository shows
the problem exactly (`examples/z7ring.lut`): `Z7` is a subtype of `Int`, `ringZ7 : CommutativeRing
Z7` is a value with its own `add`, and `a + b` on two values of `Z7` means `Int`'s addition, with
a result in `Int`, which the example then reduces `mod 7`. So today a value of `Z7` does not carry
its ring, and that is the defect you name. Mathematically `Z7` is not a subring of `Int` but a
quotient of it: the inclusion of representatives is not a homomorphism, the projection `mod 7`
is. A subtype is the wrong relation for it.

*Proposed* rule, which is yours stated in the spec's words: a type is the carrier of a model, and
the operators on its values are the model's. `i : Int` has the ring of `Int`; `j : Z7` has
`ringZ7`. Resolution of `+` is by the type, where the type names the model; this is what `02 §3`
already says ("an `operator` directive gives `+`, `-`, `*`, `/` a meaning on the argument types of
a function") and what Haskell calls coherence, one instance per type. Two consequences and one
limit:

- A carrier with two models is two types. `Int` as a ring and `Int` as the max-plus semiring are
  two types over one representation, as Haskell's `Sum` and `Product` are over one `Int`;
  `Float64` with two tolerances likewise. Converting between them is explicit (`forget` to the
  carrier, L13, and a constructor back), never silent.
- Operators of a wider model apply to a narrower type only through a homomorphism, which is your
  "coincidencia de leyes": `Z7`'s values may use `Int`'s `+` only after `forget`, and the law that
  relates the two is the projection being a ring homomorphism, stated and certified like any law.
  Other languages skip this and that is where their overloading lies.
- The limit, which your `Sqr` note hits (below): resolution by type works when the theory fixes
  the role of each operator (`Ring` says `+` is `add.op` and `*` is `mul.op`); it cannot work for a
  function over a bare `Monoid`, because `Int` carries two monoids and the type does not say
  which. There the model is named, `Twice intMul x`, or the type is one of the two wrappers.

Decision for you: operators by type, the type naming its model; a carrier with two models is two
types; cross-model use only through a certified homomorphism. Recommended yes, and `z7ring.lut`
is rewritten as the first example once it is in the spec.

## Everything belongs to a theory

> No es cierto. products, sum exponentials pertencen a category theory. data no se bien a que pero
> tambien. Podriamos tirar esos nombres como un using category_theory de C++, pero creo que todo
> pertenece a una teoria.

Conceded. Products, sums and exponentials are the universal constructions of a cartesian closed
category, their laws the β and η rules (`04 §4`), and `data` is an initial algebra, its law the
recursion principle. So "free" meant "with no laws beyond the universal ones", and the theory they
belong to is the kernel's, `core.lut`, imported implicitly (`03 §2`), which is your `using`. Its
laws are the one theory certified by conformance of the interpreter and not by test, the base of
trust of `00` (*What is known*). The second round's sentence on free types is replaced: every type
belongs to a theory; the concrete types belong to the kernel's. L20 and the open item in draft 3
are corrected accordingly.
         OK. pero para ilustrar el poder de Luthier deberiamos definir estas leyes. 

> un module podria ser un conjunto de tipos y operadores sin una teoria unificadora quizas?

It can, and it is still a theory: `03 §1` reads a file as a value of a dependent record type, "a
file is the same kind of thing as `Ring`", so a module of unrelated types and operators is the
product of their theories, whose unifying theory is that product, with no law joining the
components. Nothing to add; the word module stays for the file as a namespace.
         ahora las leyes de asociatividad, simetria etc deberian definirse en un modulos laws o algebra o un nombre mejor? 


## `Sqr` over `*`, `Double` over `+`

> Square deberia ir sobre una funcion * que sea multiplicativa y no sumativa, ahi seria Double ...
> luego el tipo de Sqr se deduce por overloading quizas?

Yes: both are one law, `Twice (m : Monoid A) (x : A) := m.op x x`, and `Sqr` is `Twice` over the
multiplicative monoid, `Double` over the additive one. The type of `Sqr` is not deduced by
overloading, for the reason above: `Int` carries both monoids, so the monoid must be named or
fixed by a theory whose roles are fixed (`Sqr (r : Ring A) := Twice r.mul`). This is the cleanest
case for the rule "by type where the theory fixes the role, by name otherwise", and it goes into
the rationale as the example.



## `assumed`, citations, checking

> Assumed es como el estado inicial de una demostracion recursiva, quizas?

Yes: the hypotheses one starts from, the base case and the induction hypothesis in a proof, the
axioms of the reals in `core.lut`, and in a test the generators' claim that they cover the domain.
Every chain of evidence ends there (`00`).



> La citation deberia ser mejor que eso, con un paper fisico o libro o pagina de wikipedia quizas?
> checked by hand cuando puede ser chequeado por IA + human in the loop (o su ausencia, tambien
> vale, pero registrado)?

Agreed, and the repository already has the discipline: `record/bibliography/README.md` takes the
DOI as the pointer to a source, `checkdoi.py` resolves it, and where there is no DOI the link is
the publisher's or the author's page. So D-2026-10-11-f is amended: the citation is a key into a
`.bib` whose entry carries a DOI, ISBN or URL that `checkdoi.py` has resolved, and the certificate
records who checked the correspondence between the theorem and the definition: `human`,
`ai+human`, or `none`. *Proposed* syntax:

    cite sqrtNewton kantorovich1948 checked ai+human

pero kantorovich1948 debe ser entonces un valor de un tipo reference o algo asi que tiene posiblemente un hash, un file un doi o lo que te parezca conveniente. quizas kantorovich sea 
optim.biblio.kantorovich o quizas estemos en optim y solo bilblio.

`none` is allowed and is what it says. The grade is `proved` in the three cases; what differs is
recorded, and a reader of the certificate sees it. 
      OK

## Mutation testing

> Mutation test es un principio o working trait que deberia ser implementado, buena sugerencia.

Taken as your decision (D-2026-10-11-h): it enters W6 as a check to implement, `luthier test
--mutate`, which alters an implementation (a constant, an operator, a branch) and reports every law
that still passes; a law no mutation fails is reported as not diagnostic. You chose to add it
before a case; the rule of `CLAUDE.md` yields to your instruction, and the decision says so.
         El problema es como mutamos un programa, me parece que eso es toda una caja de pandora. 


## Block boundaries and name scopes

> tenemos que definir las boundaries para los blocks y los name scopes.

Rules 4 and 6 above are the proposal; the summary: three kinds of block (body, `main`, session); a
name is visible from its binding to the end of its block and in nested blocks; no shadowing of
`:=`; `<-` rebinds only block-local `<-` names and parameters; a file is a namespace of unique
names (`03 §2`), qualified by import, never a block.



## Settled, amended, pending

- Decided by him: mutation testing to implement (D-2026-10-11-h).
- Amended: D-2026-10-11-f, citation as a `.bib` key with a resolved identifier, and who checked.
      podemos usar el .bib para la citation tambien, si

- Conceded: every type belongs to a theory; the scope rule for operators withdrawn.
- Pending his decision: the six rules of blocks; operators by type with the type naming its model.
         Si