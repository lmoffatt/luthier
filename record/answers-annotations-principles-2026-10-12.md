# Answer to his observation on draft 7: the order of the eurekas, and a third eureka

Source: Luciano's observation on draft 7 (cd314a4), committed verbatim at 66f0bef under G2 in
`docs/principles.md`. Written by Claude in the chat of 2026-10-12. Two questions; both decisions
are his, since the organizers are his (D1 of
`record/plan-principles-generative-2026-10-11-decisions.md`).

## 1. Why the demand (G1) before the function type (G2)

> no entiendo porque el orden de primero la demanda y luego el valor y tipo funcion, cuando el
> orden en que tuve los eurekas fue al reves? Hay alguna razon?

No reason from his sources. In the audio of 09.19 the function type comes first and is called the
trigger ("el disparador es darme cuenta de eso, que los tipos de funciones son las leyes que las
definen. Esa fue mi eureka moment. Y el otro eureka moment es ... la demanda"). The order G1, G2
was the model's, recommended in D1 and never argued there; drafts 5 to 7 list "the order of the
organizers" among the items waiting for his mark. The one argument the model could give is weak:
G2's *Proposed* formulation mentions the demand ("the demand says which descriptions are
produced", D1), so G1 was placed first to be cited. But that clause belongs to a derived L (L13,
the forgetful functor), not to the eureka; the eureka itself, laws as the type of a function, is
the step from G0 and needs no demand. By generation the order is G0, then function type, then
demand; the step from G0 to the function type is one move, the demand is the second.

*Proposed*: print the eurekas in his order. Keep the tags G1 and G2 as they are, since the
record cites them (32 occurrences in `record/`, among them Kind lines of `record/decisions.md`),
exactly as L numbers were kept by D4; only the presentation order changes, and §2 of the file
swaps its two sections "From the demand, G1" and "From description, G2". Cost: one commit.

## 2. A third eureka: objects as models of theories

> Un tercer momento eureka fue cuando me di cuenta que necesitaba los objetos ya que hay
> funciones que se testean mutuamente, o sea que "la programacion basada en objetos" tiene una
> base matematica, solo que las clases (o interfases) serian las Teorias y los objetos serian los
> modelos de las teorias. ... Probablemente esto ya exista en la programacion funcional solo que
> no se lo relaciona con objetos? En realidad, las funciones aisladas serian, si existieran,
> modelos de teorias simples? Podemos tomar los modelos y teorias como el elemento de Luthier?

Three answers.

**It exists, under other names.** The model's references, from memory, to be checked against the
texts before any of them is cited in `docs/`:

- In logic it is model theory itself: a theory is a signature with axioms, a model is a
  structure that satisfies them. His "entomólogo" is the model-theoretic stance.
- In programming the line is algebraic specification: Guttag (1975) on abstract data types as
  algebras; the ADJ group (Goguen, Thatcher, Wagner, Wright, 1978), "abstract data types as
  initial algebras"; the languages OBJ, Maude, CafeOBJ, where a specification is a theory and a
  module is a model. Goguen and Malcolm's hidden algebra (1990s) was written precisely as "a
  mathematical foundation for objects": hidden sorts for state, and two objects are equal when no
  observation distinguishes them, which is his "desde afuera".
- In ML (Standard ML, OCaml): a signature is a theory without its laws (the laws live in
  comments), a structure is a model, a functor is a function from models to modules, which is
  L20's "a parametrized module is a function from models to definitions" word for word.
- In Haskell: a type class with laws (Functor, Monoid, Monad) is a theory and an instance is a
  model; the compiler checks the signature, not the laws, and the laws are tested empirically
  (QuickCheck, `quickcheck-classes`). That is "se testean empíricamente" in practice.
- In Agda, Lean, Coq: a record or structure with law fields (`IsMonoid`, Mathlib's `Monoid`) is
  the theory, an instance carrying proofs is the model; there the laws are proven, not tested.
- The link with objects is discussed by Cook, "On understanding data abstraction, revisited"
  (2009): an abstract data type has one representation and operations over it, many
  implementations may exist but each is closed; an object is an interface with behavior, and
  representations mix. What he describes (laws declared, models interchangeable, L10 and L20) is
  the abstract data type side. What does not carry over from object-oriented programming is
  mutable state and identity; the interface as theory and the instance as model carry over whole.

So the functional world has it, but as a mechanism (type classes, modules, structures) rather
than as the organizing idea; his step is to make it the unit.

**Isolated functions are models of one-symbol theories, and draft 7 already says so.** D-2026-10-07-e
(no loose functions: a definition at a bare exponential is not a defined type) and his correction
of L14 (a function with no laws is a theory's hole) exclude the isolated function. `Sqr` is a
theory with one symbol whose laws are written over `*` of Real; it is simple in having one symbol,
never alone, since it imports the theory its laws are stated in. What makes the theory, and not
the function, the unit is his own observation: a law such as `inverse x * x = unit` or
`decode (encode x) = x` relates two or three symbols, and no single function can carry it. That is
the definition of *object* in `05 §3`: a strongly connected component of the dependency graph, the
names that refer to each other through their laws.

**Yes, and it is already the terminology; the question is whether it is an organizer.** Draft 7
fixed "theory", "model", "object" as terms and derives L20 (a function is declared in a theory and
is universal over its models), D-2026-10-07-e (no loose functions), D-2026-10-11-j (a carrier with
two models is two types) and `05 §3` from G0 and G1. Read as a third eureka, those four follow
from one idea instead of being scattered, which is what an organizer is for (P13). It is distinct
from G2: G2 says the type of one function is its laws; the third says laws relate several
functions, so the unit declared is a theory and the unit valued is a model. By his own words it
would pass the P13 check at once (three decisions and one spec section).

The cost he names, "muy demandante para crear objetos", is answered in L20 as it stands: the
concrete types (products, sums, exponentials, `data`) belong to the kernel's theory, whose laws
are β, η and recursion, so a plain record has its laws without declaring any; only a type with
meaning beyond its shape pays for laws, and that is where the laws are the meaning.

*Proposed*, for his mark, a formulation of at most two lines (D2):

**G5. Laws relate functions, so the unit is a theory and its value a model.** A theory is a
signature with its laws; a model is a value of it; a function alone is a theory of one symbol over
the theories it imports; a module is a function from models to definitions. What type theory
lacks: nothing here; this is model theory, placed in the language as its unit.

Tag G5 rather than renumbering, for the same reason as above. Printed after the two eurekas, as
the third. The derivations that move under it: L20, `05 §3`, D-2026-10-07-e, D-2026-10-11-j.

## For his answer

1. Order of the eurekas: his order (function type, then demand), tags kept. ok / no.
2. G5 as the third eureka, with the formulation above or his correction. ok / no / corrected.
