# Fourth round: dead rebindings, separators, order as a value, the kernel's laws, references, mutation

Source: Luciano's feedback on the third round, committed verbatim at c167022 inside
`record/answers-annotations-principles-2026-10-11-c.md`. Written by Claude in the chat of
2026-10-11. His closing "Si" under the pending list is read as accepting the two pending decisions,
the six rules of blocks and operators by type; logged as D-2026-10-11-i and -j, reversible by one
line from him if he meant otherwise.

## Rebinding without dependence

> analiza si hay usos legitimos del caso de la no dependencia, porque si no los hay seria un code
> smell.

In a file, none. The cases that look legitimate elsewhere do not arise here: a conditional
rebinding (`if c then x <- a`) does not exist, because `if` is an expression and a block item is a
binding; a rebinding of a parameter that ignores the caller's value (`tol <- 1e-3` as the first use
of `tol`) overrides the caller silently and is worse than a smell. The one legitimate case is the
session: a name bound to a provisional value for inspection and then rebound after looking at it,
which is what a REPL is for. So the rule: a `<-` whose previous binding of the same name has no
consumer is an error in a file and allowed in a session, where the lint says "unused binding".
Goes with the six rules (D-2026-10-11-i) as rule 3a.
    OK


## `;` or line break

> aca cabe la pregunta somos C (siempre ;) o somos Python (supongo que ; es equivalente a line
> break)

Today the spec is mixed: at the top level an act starts at column 0 and an indented line continues
it (Python-like layout, `02 §1`); inside the braces of a lambda or a `match` line breaks are
ignored, so items need `;` (C-like); inside the braces of a record type a line break separates
components. The separator rule already lists `,`, `;` and line break (`02 §3`). *Proposed*: Python.
In a block a line break separates items and `;` is equivalent to it, so several items may share a
line; inside parentheses and brackets line breaks are ignored as today. This changes one line of
`02 §1` (the braces of a lambda stop ignoring line breaks, since a lambda body is a block) and
nothing else. Decision for you; recommended yes, since every block will otherwise end its lines
with `;` for no information.
    OK



## Expressing an order of execution in Luthier

> deberiamos tener una forma de expresar en Luthier un orden de ejecucion, lo cual es util para la
> fase de ejecucion, ya que permite expresar que dos ordenes son equivalentes. Porque la fase de
> ejecucion se expresa en Luthier, como dijimos.

Yes, and the pieces are there. The program is a DAG (L9) and code is data (L6), so the DAG is a
value, `Plan`; an order of execution is a linearization of it, `Schedule`, a list of nodes; the law
`Linearizes (p : Plan) (s : Schedule)` says that every node comes after its dependencies; and two
orders are equivalent when running them gives the same outputs, `Equivalent p s1 s2 := eq (run p
s1) (run p s2)`. L18 (no effects) is the theorem that every linearization is equivalent, and under
the world-threading rule (third round, rule 5) two actions are unordered exactly when they do not
share a `w`, so running them in parallel is one more schedule the law covers. The evaluation
strategy being a parameter (L19) is this `Schedule` passed in. What it buys: the execution phase
gets laws like the declarative one, a scheduler is a model certified against `Linearizes`, and
"these two orders are equivalent" is a law tested on the values actually computed, the puzzle of
L5. *Proposed* as a library, `plan.lut`, after the session is in the spec; it is the first thing
G3 will need too, since the cost of a schedule is where expected loss is computed (L10).
    OK


## The kernel's laws, defined

> OK. pero para ilustrar el poder de Luthier deberiamos definir estas leyes.

Done: `src/luthier/lib/kernel_laws.lut` states beta for exponentials, the two projections and
surjective pairing for products, the case rules on `Bool` and `Maybe` for sums, and the recursion
principle of `List` witnessed by a fold, each law with its types and equalities first and the
quantified variables last, and bundles them as the theory `KernelLaws A B`. The example
`examples/kernel_finite.lut` gives a model at `Fin 3`, `Fin 2` and tests it:

    luthier test examples/kernel_finite.lut
    kernelFin: passed; 10 laws, 200 sampled cases each; certificate examples/kernel_finite.cert.json

Two things learned writing it, both for the spec. Functions over `Fin n` are drawn as tables but
not enumerated, so `exhaustive` skips every law quantified over a function and the test had to be
sampled; enumerating `Fin n -> Fin m` (m^n tables) is finite and should be allowed. And eta
(`\ y { f y } == f`) cannot be stated, because equality of functions is not structural (`05` R8);
observed pointwise it is beta, which is what the file says. Since every concrete type belongs to
this theory, `KernelLaws` is also the first candidate for `assumed` outside `core.lut`: the
interpreter's conformance is what a user takes on trust, and now a user can also test it.
          assumed or proved? 


## Where the laws live

> ahora las leyes de asociatividad, simetria etc deberian definirse en un modulos laws o algebra o
> un nombre mejor?

Today they are in `algebra.lut`, which holds both the generic laws (Reflexive, Symmetric,
Transitive, Associative, the identities, distributivity) and the structures built from them
(Setoid, Monoid, Group, Ring, Field). *Proposed*: split them, `laws.lut` for the laws of relations
and actions, imported by `algebra.lut`, `kernel_laws.lut` and anything that states a law over an
operation it does not own; `algebra.lut` keeps the structures. The name `laws` is plain and says
what G2 says, that laws come first. Decision for you; it is a move of definitions with no change of
meaning, one commit.
           Agreed



## References as values

> kantorovich1948 debe ser entonces un valor de un tipo reference o algo asi que tiene posiblemente
> un hash, un file un doi o lo que te parezca conveniente. quizas kantorovich sea
> optim.biblio.kantorovich o quizas estemos en optim y solo biblio. ... podemos usar el .bib para
> la citation tambien, si

Agreed on all three. *Proposed*: a type in the library,

    Reference : U := { key : String, doi : Maybe String, isbn : Maybe String, url : Maybe String,
                       sha256 : Maybe String | Resolvable }

with the law `Resolvable`, at least one identifier present and resolved (today `checkdoi.py`
does the resolving; it becomes an extern of the library). A `.bib` file is the source: `biblio :=
extern "bib:record/bibliography/luthier.bib"` reads it as a module of `Reference` values, so
`biblio.kantorovich1948` is a name like any other, prefixed as `03 §2` prefixes imports, and a
library such as `optim` carries its own `optim.biblio`. The directive then takes a value:

    cite sqrtNewton biblio.kantorovich1948 checked ai+human

and the certificate records the reference's identifiers and hash, so a reader finds the source
from the certificate alone (W10). Goes with D-2026-10-11-f as its syntax; amended again below.

        OK


## Mutation: how to mutate a program

> El problema es como mutamos un programa, me parece que eso es toda una caja de pandora.

It is, and the box is kept small by three rules. First, a mutant is a function `Term -> Term`
applied to a body (L6, code is data), so mutation is a library, not a feature of the kernel.
Second, the catalogue of mutation operators is a parameter (P11) and starts with four, the ones
the literature finds most informative: replace a constant (0 by 1, 1 by 0, c by c + 1), replace an
arithmetic or relational operator by a neighbour (`+` by `-`, `<` by `<=`), negate a branch
condition, delete an item of a block. Third, the problem that makes the box deep, the equivalent
mutant (a change that does not change the function, so no law can fail), has an answer in Luthier
that it has nowhere else: the identity test of L21. A mutant that passes every law is run against
the original on sampled inputs; if the outputs agree, the mutant is equivalent and the report says
so; if they differ, the laws are weak at exactly those inputs, and the report shows them. So the
check distinguishes weak laws from equivalent mutants instead of leaving the user to guess, and
that is what makes D-2026-10-11-h implementable without opening the whole box. The plan for it
comes with the session and `plan.lut`, after the spec.

## Logged

- D-2026-10-11-i: blocks, the six rules of the third round plus 3a (a rebinding whose previous
  binding has no consumer is an error in a file, allowed in a session).
- D-2026-10-11-j: operators resolved by the type, the type naming its model; a carrier with two
  models is two types; cross-model use through a certified homomorphism; `z7ring.lut` to be
  rewritten.
- D-2026-10-11-f amended: the citation is a `Reference` value, read from a `.bib`, with its
  identifiers and hash in the certificate.
- Pending his decision: Python-like separators in blocks; `laws.lut` split from `algebra.lut`.

## Fifth round, one question

> assumed or proved? (on `KernelLaws` as a candidate for `assumed` outside `core.lut`)

`assumed`, and tested. `proved` by citation needs a theorem outside Luthier that establishes the
laws for this definition; for the kernel's rules there is none: `04 §4` is the definition of the
rules, not a theorem about the interpreter, and that the interpreter realizes them is exactly what
`00` (*What is known*) lists as the base of trust, "the host realizes the rules of reduction". So
the grade of the kernel's conformance is `assumed`, as for the reals. What `kernel_laws.lut` adds
is a control on the assumption: the laws can be run on finite types, and `examples/kernel_finite.lut`
records `sampled 200` for ten of them. The reals cannot be tested; the kernel can. An assumption
with a control is the strongest thing a base of trust can be, and the certificate shows both: the
`assumed` axiom and the test that, so far, agrees with it. Everything else in the round: OK.

## Sixth round: which kernel laws cannot be proved

Source: his copy `answers-annotations-principles-2026-10-11-d_mod.md` (f8e5b03; he wrote in a copy
because this file changed under him): "which kernel laws cannot be proved? Elaborate." Three
things are called "the kernel's laws" and the answer differs for each.

**The rules of the calculus** (`04 §4`: beta, delta, iota, prim, extern). These are definitions,
not theorems: `(\ x { t }) a ≡ t[a/x]` holds by fiat, there is nothing to prove, and that is why
`kernel_laws.lut` states them as laws to be *checked*, not derived. The theorems *about* the
calculus are four, and they split:

- Confluence, that the order of reduction does not change the result: provable for the pure part
  by the standard method (Tait and Martin-Löf, parallel reduction), and true of the whole only if
  externs are pure, which is L18 as an assumption on the environment. Per program it is testable:
  two schedules of the same plan give the same outputs, the law `Equivalent` of `plan.lut` (fourth
  round), so a theorem no one has proved for Luthier is a certificate any program can earn.
- Type preservation, that a well-typed term reduces to a well-typed term: provable, a metatheory
  project of the size of a thesis (MetaCoq did it for Coq's kernel); not done, and until done it
  is `assumed`, with the accept/reject suite (`tests/spec`) as its control.
- Termination: false. Recursion is general (`04 §3`: "nothing guarantees termination"), so a
  program may not terminate, `≡` is semi-decidable, and "every program terminates" is not a law of
  this kernel. Per run it is a fact of the trace (it terminated on these inputs), never a law.
- Consistency as a logic: unprovable, and today false. The kernel has one universe, `U : U`,
  which is inconsistent (Girard, Hurkens; the guide lists the hierarchy of universes as a later
  layer, `00 §4`: "it bites only when there are proofs"). As a programming language this is
  harmless, Haskell lives with it; for an internal prover it is fatal, since every type has an
  inhabitant that does not terminate. Hence the grade `proved` cannot come from a proof inside
  Luthier until universe levels and a total fragment exist, and `05 §7` is right to say "not in
  version 0". `proved` by citation (D-2026-10-11-f) is the only `proved` there is.

**Eta.** Not a rule of `04 §4` at all, and the one law of the kernel's types that is neither
provable from the rules nor testable: `\ y { f y } == f` needs equality of functions, which is not
structural (`05` R8) and is not observable; pointwise it collapses to beta. HoTT adds function
extensionality as an axiom (or derives it from univalence); Luthier either adds it as `assumed`
when the proof layer comes or does without, and today does without. This is the precise answer to
"which cannot be proved": eta, consistency, termination; the first for lack of an equality, the
second for lack of universe levels, the third because it is false.

**The interpreter.** "The Python program realizes `04 §4`" is provable in principle (CakeML and
CompCert are proofs of exactly this kind) and will not be proved for a Python implementation,
whose meaning rests on CPython, the operating system and the processor; it is the base of trust of
`00`, `assumed`, with two controls: the accept/reject suite and `kernel_laws.lut` on finite types.
Below it, the primitives: `Int` unbounded (Python's integers, by construction), `Float64` IEEE 754
(the processor, assumed), each extern's conformance to its declared type (tested at first demand,
L14). Every certificate's chain ends in these, and `check -v` lists them.

So, in one line: the rules need no proof; confluence and preservation are provable and unproved,
with controls; termination is false by design; consistency is unprovable until universe levels;
eta is unstatable; the interpreter is trusted with controls. "Nice!" on mutation, noted.
