# Second round: answers to Luciano's replies on the annotations

Source: his replies, committed verbatim at 18da042 inside
`record/answers-annotations-principles-2026-10-11.md`. Written by Claude in the chat of
2026-10-11. Numbers follow the first round. What cites the spec is marked by section; the rest is
*Proposed*. Draft 3 of `docs/principles.md` is made in the same commit series.

## 1. Executions are verified too

> las ejecuciones tambien se verifican observando el mundo antes y despues del acto y las leyes
> sobre las ejecuciones hablan sobre esto. Me parece que esto deberia estar mencionado en los
> principios o convenceme de que surge de ellos.

It follows, and it is mentioned anyway, because you are right that it shows how Luthier speaks of
invariants over executions. Where it follows from: the guide already says "over procedures a law
is tested by observations" and that propositions are of three kinds, a timeless law, a fact of
the trace, a statement about the world now that ages (`00`, *What is known*). And the pattern is
the one of L9: a mutable parameter is two variables, before and after. An action is a function
from the world before to the world after, its laws are laws of that function, and the two
observations are the demand of the world's state. So L12 in draft 3: "Evaluation is verification;
execution is an action on the world, verified by observing the world before and after it, and the
laws over actions are stated over those two observations." From G2 (observation) and G1 (the
action is the executive face).

## 2. `:=` is a binding too, and the law of `<-`

> me estas caminando. := es binding tambien, luego de <- lh == rh, de hecho creo que es la ley de
> <-, aunque eso vale para cosas que tienen eq, pero supongo que siempre hay formas mas suaves de
> equality

Yes. Both are bindings, and the law of a binding is the one you state: after the act the name
equals the term, in the equality the type has, structural `==` where it exists (`05` R8),
observational otherwise, a distance under G3; that is the "softer forms" you suppose. The
difference between the two is only for how long the law holds: after `:=` for all time (the name
reduces to its body, so it is definitional equality `≡` made by an act); after `<-` until the next
`<-` on that name, and in the core each rebinding is a fresh name, so on its own name it also
holds for all time (R12). L16 in draft 3 says so, with the two binding acts and their one law,
next to the levels of equality.

## 3. Terminology, theories in theories, operators, free types, what a law is

> tenemos que fijar una terminologia para Luthier ... Theory and model asi planteadas suenan
> perfecto.

Fixed: *theory* (a type with laws, usually parameterized; `05 §3`) and *model* (a value of it).
*Module* stays the name of a file as a namespace (`03 §1`) until modules are values, when a module
is a model of the theory that is its signature. *Object* keeps the spec's meaning, the cycle of a
type and its laws (`05 §3`), and is not used for a theory. Draft 3 uses these four words and no
others; a glossary line goes in the header.

> una theory que contiene otras theories. Supongo que seguira siendo theory.

Yes. A theory over a model of another is still a theory (`Exp R m` over a `NumberModel`, a vector
space over a field, `00`), and a theory with a component that is a theory is a theory whose
signature has that component. Nothing new.

> Para acceder a los tipos y funciones de una teoria usamos los prefixed names, y podriamos usar
> el infame criterio de C++ de que los operadores + /* etc se resuelven por el tipo pero serian
> los definidos por la teoria. Discutir sobre esto.

Access by prefix, yes: `m.op` is the projection of a component of the model (`02 §3`), and the
grammar already has `operator + := term` as a directive. The C++ criterion, resolving `+` by the
types of its arguments, has one defect that matters here: two models of the same theory on the
same carrier (the integers as a ring and the integers mod n as a ring, both over `Int`; `Float64`
with two tolerances) are indistinguishable by type, and resolving by type would pick one
silently. L20 already says where the model comes from: the scope, or passed explicitly. So the
rule I propose: an operator belongs to a theory, and the model it applies is the one in scope for
that theory, never inferred from the arguments' types; a program that wants another model names
it. It is a decision of the spec (`05 §10`, implicit arguments), and it is yours.

> si vamos a dejar que existan tipos libres, tipos que no pertenezcan a ninguna teoria.

Yes, and the spec has them: the concrete types, `data`, products, sums, exponentials, subtypes of
those, with constructors and eliminators (`05 §1`). Under G2 their laws are the free ones, the
equations of their constructors, and they are the initial models of the theories built on them.
P14 (a type is a concept; a function is a value of a defined function type, never of a bare
exponential) binds functions, not every type. So a free type is allowed and a bare function is
not. Recommended as is.

> que carajo es una Ley? aqui estamos en el caso de que una ley es un valor? Podemos definir
> simetria de otra forma que por su implementacion? El principio de la leyes se aplica a todo
> menos a la formulacion de las propias leyes? Esto en realidad lo resolvi con square:={x:A|
> square x== x*x} ... como los holotipos de las especies de insectos ... para las funciones usamos
> un object classifier que es distinto a una implementacion.

A law is a value: a term of type `Bool`, or a function into `Bool` over what it quantifies, of
type `Law` (`04 §3`, `00`). Your holotype is the spec's own rule, stated in the guide: "a function
given by a formula is the model of the singleton theory whose law is that formula, `sqr : Sqr :=
\ x { x * x }`", and any other model is checked against it. And the line between a holotype and a
transcription is formal, which answers "does the principle of laws exempt the laws themselves".
A law is written over the signature of its theory: `x * x` uses `*` as an operation the theory
assumes, with no algorithm for it. An implementation is written over a concrete model: a sum over
indices for a determinant is a body that computes with `Float64`'s `*`. R10 draws exactly that
line (a definition in the kernel is a model of the laws, certified like any other, never the law).
So the principle does apply to laws: a law may use the operations of its signature freely, and
what it may not do is compute the answer with a model. The object classifier for functions is the
type of function types with their laws, which is where `Sqr` lives; the holotype `\ x { x * x }` is
a value of it, not the type. G2 in draft 3 gains the sentence: "a law is written over the signature
of its theory; an implementation over a model; the first is the holotype, the second a specimen."

## 11. `assumed` against `proved`, and how to indicate the identity

> cuando usariamos assumed y cuando proved? ... assumed (probably unsafely taken as true,
> something useful as an algorithm proving point, like when we start a test)

Exactly that. `assumed` is the `axiom` body (`06 §3`): the laws are taken as true and never
tested, no justification is recorded, `check -v` lists it, and today it is allowed only in
`core.lut` and `lib/`, for what nothing can compute (the reals are a complete ordered field). It
is the base of trust where every chain of evidence ends (`00`, *What is known*), and it is the
unsafe starting point you describe: assume, build, test what is built. `proved` is the grade of
a law established by a proof, "not in version 0" in the spec. Your addition makes it available
now in one form: *proved by citation*, a human asserts that a theorem outside Luthier establishes
the law for this definition, and the citation is recorded in the certificate. The difference is
what a reader finds: behind `assumed`, nothing; behind `proved`, a citation to check. Both are
untested; a chain whose weakest link is `assumed` is weaker than one whose weakest is `proved`,
and the certificate of the chain says which. *Proposed* syntax, a directive next to `test`:

    cite sqrtNewton "Kantorovich 1948, quadratic convergence of Newton's method; checked by hand, L.M., 2026-10-11"

which records grade `proved` with that string. Allowed in user code, unlike `axiom`. Decided yes
in your reply; it goes to `05 §7` with this syntax unless you prefer another word.

> La identity habria que indicarla de alguna forma? podria ser identity sensu boolean o sensu
> lawvere, aqui como seria la forma de indicarlo en codigo?

The type of the law's result says which, and no keyword is needed. Sensu boolean, a law into
`Bool`, which `05` R8 allows only where `==` is structural: `Identical f g := \ x { f x == g x }`.
Sensu Lawvere, a law into `Cost` (the type for [0,∞), to be added by G3's rationale):
`Dist f g := \ x { dist (f x) (g x) }`, and the demand supplies the tolerance. Version 0 has the
intermediate form, a boolean law with the tolerance as a parameter (`Close f g tol`), which is P11
and is what `algebra.lut` does with `eq`. The certificate records, for the first, the grade; for
the second, the grade and the worst cost seen with the input that reached it (prior art G). The
transport of item 4 then reads off the certificate: exact when the identity law is boolean, with
that cost when it is a distance.

## 12. W6, the difference

> no entiendo la diferencia

Your meta-test, "the test must fail where it must fail", can be realized two ways. A negative
control feeds a case known to violate the law and checks that the test rejects it: it checks the
test's input side, and it has been in force since 2026-10-02. Mutation testing alters the
implementation and checks that some law fails: it checks the law's power to detect a wrong
implementation. The second is not in place, and the rule of `CLAUDE.md` (a mechanism with a
recurring cost enters after a case it would have caught) makes it wait for a law that passed a
wrong implementation. That was the whole difference: control of the input against mutation of
the implementation, and one is in force and the other waits.

## 15. W15 and a principle on the cost of adherence

> agree. I think that making the principle adherence manageable to calculate is key and should be
> a guiding principle. what is manageable is something to be discovered.

W15 enters draft 3. The guiding principle you state is of the kind that lives in
`record/principles.md`, and it is yours: *P15 Adherence to the principles must be cheap to
compute; what is cheap is found as the work goes.* Logged as proposed by you, with that wording,
for your mark; it is the reason behind five organizers instead of thirty-four peers, and behind
W14 and W15.

## 17. `<-` at the top level, and the session as a block, expanded

> Lets revisit D-2026-10-11-c forbids `<-` at the top level of a file. Lets continue understanding
> this, expand the explanations

Why the ban exists. A file is a set of acts without order (`05 §2`, L9): order in the file is not
significant, dependencies give the only order there is. `<-` rebinds, and "the latest binding"
has no meaning without an order. So at the top level of a file `<-` cannot mean anything, and
allowing it would mean giving files an order, which breaks L9 and the DAG, and with it the memo by
hash and the plan backward. That is the cost of lifting the ban, and I would not pay it.

What a session is. A REPL has an order: the order in which you type. So a session is a block, the
one place where `<-` is allowed (R12), typed incrementally. Concretely:

- The environment is the block's bindings so far, each a node of the DAG; a command is one more
  act appended to the block.
- A command that prints or asks for a value is a demand; the planner runs backward from it over
  the whole block so far and forward over the live subgraph (L19); the memo by hash of code,
  inputs and mode means that what was computed for an earlier command is not recomputed, and
  that what changed is.
- Rebinding a name with `<-` adds a fresh node; the earlier node stays, reachable by its hash,
  inspectable until nothing refers to it, which is the forgetting of L13 at run time.
- `:=` in a session defines once, so a name you expect to revise is bound with `<-` and a name you
  want locked with `:=`. That gives the session a discipline for free: exploration binds with
  `<-`; when a definition is stable it is promoted to `:=` and moved to a file, where only `:=`
  exists. The audio of 08.58 ("copiándolo y corriéndolo de nuevo", 16:36) is this promotion.
- Certificates persist across commands by hash, so a function certified in one command is
  certified in the next, and a rebinding of one of its inputs invalidates exactly the cone that
  depends on it.
- A script is the block run as one batch: all demands at once, the collapse of the audio (read
  every demand, run, write). A file of acts plus one block named `main` is the script form, and
  that block is where `<-` lives in a file.

So the ban on `<-` at the top level of a file stays, the session is a block, and a file may
contain a block. Decision for you: the session as a block, with this discipline (`<-` to explore,
`:=` to lock). If yes, it goes to the spec as a section on the session and the status of `04 §7`.

## 18. Units multiply and invert but do not add

> units can be multiplied and inverted but not summed, it is kind of weird?

Not weird once the two levels are separated. Dimensions form a group under multiplication, which
is why every dimension has an inverse (per second, per metre); addition is not an operation on
dimensions at all. Addition is an operation on quantities, and the quantities of one dimension
form a one-dimensional vector space over the reals: 3 m + 2 m is in it, 3 m + 2 s is not, because
there is no space they share. Multiplication maps quantities of dimension d and e to quantities
of dimension d·e. The name of this structure is a graded algebra, graded by the group of
dimensions, and the type-level picture is the one of L4: the type carries the proposition "this
quantity has dimension d", addition is defined inside the subtype, multiplication across subtypes
by the group law. G0 generates it with nothing added.

## Settled in this round

Yes to `proved` by citation and to the identity transport (item 11, D-2026-10-11-f). Yes to W15
(item 15, D-2026-10-11-g), with P15 proposed in his words for his mark. Pending his decision:
operators resolved by the model in scope, not by argument types (item 3); the session as a block
with `<-` to explore and `:=` to lock (item 17).
