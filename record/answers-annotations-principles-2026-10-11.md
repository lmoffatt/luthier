# Answers to Luciano's annotations on docs/principles.md draft 2

Source: his annotations, committed verbatim at 2c18c41 on draft 2 (cd24137). Written by Claude in
the chat of 2026-10-11. Each item quotes the annotation, answers it, and says what changes in
draft 3 or what needs his decision. What cites the spec is marked by section; the rest is
*Proposed*. Order follows the file.

## 1. L12, the executive face

> Esto es incompleto, ya que esto es valido en la cara declarativa de Luthier, en la cara ejecutiva
> de luthier execution es una modificacion del estado del mundo

Right, and the defect is in the words. L12 says "execution is the verification of equivalences"
and then names two faces; the statement covers only the declarative one. The spec already keeps
two words apart in practice: a definition is *evaluated* (L18, no effects) and an action is
*executed* (L19, print, save). The executive face is also where the world enters: data read, the
demand itself. Draft 3: "L12. Evaluation is verification; execution is an action on the world."
Evaluating a term places it in its class (the kernel reading, addendum 8); executing an action
changes the state of the world, and the only things that do so are the actions. The two faces
then read as G1's statement, which is where I had placed them. Change taken as routine.

## 2. L16, is `<-` missing?

> aqui no estaria faltado "<-" que incluimos para el caso de argumentos por default, un sugar muy
> importante para tener interfases amigables.?

`<-` is not an equality; it is a binding (D-2026-10-11-c: `:=` defines once, `<-` binds and
rebinds, each rebinding a fresh name in the core). L16 lists `:=` among the levels of equality
because "defined as" is the first way two names come to denote the same thing, so by the same
reasoning `<-` belongs next to it, as the second binding form, and neither asserts a proposition.
Draft 3 adds one sentence to L16: "The binding forms are two, `:=` once and `<-` rebinding; they
make names, they assert nothing." The default-argument sugar itself (`(tol : T <- d)`, call
`f a (tol <- v)`) is already listed under G4 as a decision it took (D-2026-10-11-c); on "muy
importante para interfaces amigables" I agree, and it is what made P11 livable
(`record/default-arguments-2026-10-11.md`).

## 3. L20, functions and theories

> aca no entiendo bien que queres decir. una funcion es declarada generalmente dentro de una
> theoria (que quizas pueda ser el nombre luthier para objeto/modulo/clase)

Two notions are in play and the spec keeps them apart. A *module* is a namespace, a file with
prefixed names (`03 §1`), not yet a value. A *theory* is a type with laws, usually parameterized
(`Group (A : U)`), and a *model* is a value of it (`05 §3`, `03`): `Field` is a theory, `float64`
a model. L20 as written says a function is parametrized by theories: `sum : (F : Field) -> ...`,
with the model supplied from the scope or passed. Your reading says a function is declared *inside*
a theory, as a member. Both are the same thing seen from two sides, as in ML: a member of a
signature is a function whose first argument is the structure it belongs to. So yes, "theory" can
be Luthier's word for what other languages call object, module or class, with one difference that
matters: a theory carries its laws, and a model is certified against them, so "a function declared
inside a theory" is universal over every model of the theory at once. That is what L20 wanted to
say. Draft 3 rewrites it: "L20. A function is declared in a theory and is universal over its
models." A Luthier module as a value (`fft : FFTLib := import "fft.lut"`) is still open in the
spec (`03`, last section); when it comes, a module is a model of the theory that is its signature,
and the two notions meet.

## 4. L21, the certificate travels

> si, me gusta el certificado de la law se transporta por el certificado de identity.

Taken, with one condition that decides where it works. A certificate of identity transports the
certificate of the law only where identity is exact: integers, decidable types, or the same
implementation rerun with the same seed. Over floats two different implementations are almost
never bit-identical (a different order of operations rounds differently), so the transport is up
to a distance, and that is G3's quantitative identity: the cost of the identity certificate is the
observed distance, and the law's certificate travels with that cost added. Draft 3 states the
transport and the condition in L21. See item 11 for the chain you propose with `axiom`.

## 5. L15, a functor Real → Float64?

> Esto es un testigo de la idea de que tenemos un functor que va de Real--> Float64 y que ahi
> vemos algunas propiedades de Real proyectadas en Float, seria eso?

Yes, in Lawvere's sense and not in the strict one. Strictly, rounding `fl : Real → Float64` is not
a homomorphism (it does not preserve `+`) and `Float64` is not a field, so there is no functor of
fields; the exact map goes the other way, the inclusion `Float64 → Real`, with `fl` as its
retraction. In the enriched reading of G3, where a type with a distance is a category enriched in
[0,∞), a functor is a map that does not expand distances more than a constant, and `fl` is one:
every law of `Real` is projected onto `Float64` with a cost, |fl(a + b) − (a + b)| ≤ ε|a + b|. So
"some properties of Real projected on Float" is exactly right, with the projection carrying the
cost of each property. This is the same object as item 16: the algebra that says how the cost
moves through application. Draft 3 adds the sentence to L15 as your reading, with the two caveats.

## 6. G4, "under the tie-breaker"

> Explicame esto, no se que queres decir, explicame la logica de under the tie-braaker.

A tie-breaker is the rule applied when the others leave a choice open. G0 to G3 describe what the
language is; they often allow two designs equally (both typed, both demand-driven, both described
by laws). G4 is the rule for choosing between them: allow both ways and ask for the law that makes
them equivalent, instead of forbidding one. It therefore generates no statement about the
language (no L of its own) and shows up as the reason behind decisions: `<-` rebinding and defaults
(D-2026-10-11-c), `if` without `else` as a guarded value (D-2026-10-11-b), many paths (L10), laws
that accumulate instead of required characterization (D-2026-10-11-d). The heading was bad. Draft
3: "G4 decides between designs", with that paragraph.

## 7. W1, the implementation may complain

> Si, la implementacion puede quejarse y decir "esto no hay forma de hacerlo" (con una forma mas
> tecnica de decirlo quizas?)

The technical form: the implementation returns a counterexample to the specification, a program
the specification accepts and no interpreter can run, or two rules that cannot both hold. The
specification then changes by a recorded decision, never silently. Draft 3 adds the sentence to
W1. There is a related mechanism already in force: W9 (a patch is named as a patch) is what the
implementation does while the specification has not yet answered.

## 8. W2, the example clears the mind

> si, el ejercicio clears the mind, un ejemplo puede mostrar contradicciones no obvias

Added to W2 in your words: a worked example shows contradictions that are not obvious. It is also
the reason W2 sits with G2: an example is an observation of the rule.

## 9 and 10. W3 and W4

> bueno, no estaria usando mucho este criterio, pero es un buen criterio para frenar la
> proliferacion de abstracciones
> Misma linea que arriba

W3 restated in your words: its job is to stop the proliferation of abstractions; and the record
agrees you do not invoke it often, so it is a brake and not a motor. W4 is the motor: growth
comes from the application. Draft 3 writes the pair that way, W4 before W3.

## 11. W5, native as a test of the external, and `axiom`

> Si, esto es clave. Luthier tiene que ser expresivo para todo. Ahora, aqui hay un principio que
> sugiere que debo escribir la implementacion en Luthier y luego usar eso para testear la
> implementacion externa. No se si es un principio constructivo. Puede serlo para ingenieria
> reversa ... o cuando sabemos por ejemplo que una implementacion es correcta por teorema
> matematico conocido (esto seria algo que requeriria una palabra clave nueva, quizas axiom ?) y
> luego por identidad bitwise con valores conocidos se verifica una implementacion externa. Esto
> es una idea nueva que merece discusion.

Three things in this note.

First, the doubt: W5 as a principle of construction says "write it native, then test the extern
against the native", and that is the oracle pattern G2 rejects, because "agrees with the native"
is a law that copies an implementation. So W5 is not a principle of the language, and draft 2
already demoted it to bootstrapping. Your note agrees and adds the two cases where it is
legitimate, which are not bootstrapping at all.

Second, the two legitimate cases. Reverse engineering: the native is a hypothesis about what the
foreign code does, and bit identity on known values is the test of the hypothesis; the certificate
says "the extern computes what this native computes", which is a description after all, since
the native is readable and the extern is not. And the theorem case: a native implementation
known correct by a known theorem, and the extern verified against it by identity on known values.

Third, `axiom`. The spec already has the grade: `assumed`, "an axiom: the laws are stated and
taken as true, never tested" (`05 §7`, `06 §3`), and `luthier check -v` reports the axioms. What
it does not have is an axiom *about an implementation*: today `assumed` attaches to a law, and
your case attaches to a function, "this definition is correct by theorem T". That is a new
construct and the right word is probably not `axiom` but a certificate with grade `proved` and a
citation instead of a test, since the theorem is outside Luthier and the claim is that a human
checked the correspondence. The chain then is: law, stated; native, certified `proved` by
citation; extern, certified by identity against the native on known values (L21), exact over
integers, up to a cost over floats (item 4). The certificate of the extern carries the whole
chain by hash, and anyone can see that its root is a citation, not a test.

This is a decision for you, since it adds a grade or a construct to the spec: (a) `proved` by
citation as a grade of a function's certificate, with the citation recorded; (b) the identity
test as the transport, with its cost over floats. If you say yes, it goes to `05 §7` and to L21,
and W5 is rewritten with the two legitimate cases named. Recommended: yes to both; the spec's
grades were made for this.

## 12. W6, the meta-test

> Esto es un meta-test que tiene que existir siempre: el test debe fallar donde debe fallar, no
> solo debe pasar cuando debe pasar.

Taken in your words as the statement of W6. The literature's name for the mechanical version is
mutation testing: alter the implementation and check that some law fails; a law that no
alteration can fail is not a law. This can become a `luthier` check later (W8), but under the
rule of `CLAUDE.md` it waits for a case it would have caught; the negative controls of 2026-10-02
are that case for tests, not yet for laws.

## 13. W12

> esto es muy importante para la interaccion con la IA

Added as the reason of W12.

## 14. W13, the meta-method

> Esto hace al meta-metodo, desestabiliza el sistema y lo hace crecer. El arte esta en no
> desestabilizarlo antes de tiempo.

Taken in your words. It also names the risk of today's work: the rewrite from generators
destabilized the list of principles on purpose; the sign that it was not before time is that every
L found a generator and three that I had moved out came back (D3).

## 15. W14, engagement and deadlocks

> Clave: no sobrecalentemos el cerebro de Luciano ... La IA tiene una directiva de mantener mi
> engagement, hay que cambiar esa directiva en el siguiente sentido: mi engagement va a ser mejor
> cuando mi capacidad cognitiva es usada para el desarrollo optimo del proyecto. Optimo en base a
> que? En base a los principios de este documento, por lo que algo clave es que el computo de la
> adhesion a los principios de este documento sea eficiente, que no de lugar a deadlocks ... Estos
> pueden ser legitimos ... o ilegitimos: hay una contradiccion entre los principios que impide una
> resolucion. Tenemos que analizar si es uno u otro y en eso mi asistencia es fundamental.

On the premise: I do not run under a directive to keep you engaged as a product metric. What is
true is that assistant models are shaped toward agreeableness and completeness, and both spend
your attention: agreeableness by validating instead of deciding, completeness by bringing you
everything instead of the one question. Your instruction is the correction and it is operational,
so I have saved it as a standing rule for this project: engagement is measured by how much of your
cognition goes to the strategic direction, and nothing else.

On the mechanism. Adherence to the principles must be cheap to compute, which is why a flat list
of thirty-four could not work and five organizers can. A deadlock is a long analysis that does
not converge. Your distinction is the right one and it maps onto principles in force: a
legitimate deadlock is a delicate question, and it goes to you as one question (P12); an
illegitimate one is a contradiction between principles, and by P4 (principles are found as the
work goes) and P13 it is the signal that a principle is missing or that two must be ordered, and
that also goes to you, as the pair in conflict. `CLAUDE.md` already says "raise a latent conflict
between principles when what it could cost is worth his attention". What it lacks is the
trigger: when an analysis revisits the same decision twice without new evidence, or exceeds what
one screen can carry, the session stops and reports which of the two it is, naming the principles.
That is a rule of behaviour, not a detector with a recurring cost, so it can enter now. *Proposed*
W15: "A long analysis is reported as such, as a delicate question or as a conflict between
principles, and goes to Luciano as one question." Your mark decides.

## 16. Open, the composition of judgments

> Aqui hay un concepto fundamental y es la composicion de judments. Como se transfiere la
> quantitative equality a traves la aplicacion de funciones, cual es el algebra. Esto es lo que
> define la practicabilidad de esta extension. Y eso se va a ver con ejemplos probablemente.

Agreed that this decides whether G3 is practicable, and the algebra is known in two forms,
which are the two readings of a cost still open in the rationale.

As distance: if `f` expands distances by at most `L` (Lipschitz, or the condition number in
numerical analysis), then `d(f a, f b) ≤ L · d(a, b)`, and composition multiplies the constants.
This is backward error analysis (Higham), and there is a type system that carries it: sensitivity
types, where a function type records its constant, `f : A ⊸_L B`, and application multiplies
(Reed and Pierce, "Distance makes the types grow stronger", 2010, the Fuzz language). Quantitative
equational logic (Mardare, Panangaden, Plotkin) has the same rule as an axiom: operations are
nonexpansive, so `s =_ε t` gives `f s =_ε f t`.

As likelihood, cost = −log p: costs add under independence, which is the Bayesian composition
you named, and a chain of judgments has the cost of the sum; a bound on a sum of n rounded terms
is n·ε in the worst case and about √n·ε in expectation, which is the difference between the two
readings in one example.

The practicable version is probably both: a Lipschitz constant per function type when it is
known (it is, for the arithmetic of IEEE and for linear algebra by condition numbers), and a
sampled cost when it is not. Examples for the rationale (D6): the sum of n floats, a matrix
inverse with κ(A), and a probability that must integrate to one after sampling. I write them
there.

## 17. Interpreter or script

> Aqui claude le esquivo al bulto, no tomo la discusion de si Luthier debia ser tipo interprete de
> comandos (como es macroir) o monolitico (como es un programa de C, y decirme cual es el nombre
> de la tecnica alternativa al interprete de comandos si es que existe alternativa)

Fair. The discussion, then.

Names. The command interpreter is a REPL (read, evaluate, print, loop): an environment of named
values that persists between commands, each command evaluated against it. The monolithic form is
whole-program, ahead-of-time compilation: the program is read entire, dead code is eliminated,
and the executable runs and exits; a script run by `python file.py` is the interpreted version of
the same shape (batch). There is a third shape, and it is the one L19 already describes: the
incremental build system, or dataflow: definitions are rules, demands are targets, every result is
memoized by the hash of its inputs, and asking for a target reruns only what changed (Nix and
Bazel for files, Shake and Salsa for computations, reactive notebooks such as Pluto and Observable
for interactive use). The REPL is a build system driven one target at a time; the batch run is
the same build system given every target at once. MacroDR is a REPL; a C program is batch; Luthier
as specified is the third.

Recommendation: the environment, as in MacroDR and R, as the user-facing model, because you know
how to build it, because sonolocalización is worked interactively, and because inspection of
intermediate values is G1 applied by a person (each inspection is a demand). Implemented as the
dataflow of L19, so the script is one batch of demands and the dead-code elimination you want
from the monolithic shape is what the backward plan does for every demand anyway. Costs: (a) the
environment must be a block, since a REPL redefines names and D-2026-10-11-c forbids `<-` at the
top level of a file; the session is then the body of a block, each command a `<-`, and the file
form stays pure; (b) what persists between commands is not only values but certificates, and the
memo keyed by hash (L19) already gives that; (c) the "collapse" of the audio of 08.58 (read every
demand, run, write) is the batch case and loses nothing. Decision for you: the session as a block
with `<-`. Recommended: yes; then it goes to the spec as the status of `04 §7` and a section on
the session.

## 18. Units

> Es quimulun. (es un repositorio en mi maquina y en github) Y si unidades (metros, segundos)
> hacen a los types y no se pueden suman metros y segundos (salvo que tengas velocidades que
> conviertan unos en otros).

Spelling corrected to quimulun in draft 3. On substance, units are a case of G0 without a new
idea: a dimension is a proposition about a quantity ("this is a length"), dimensions form a group
under multiplication (the free abelian group on the base units), and a velocity is the type
`Length / Time`, which is why multiplying by it converts. Addition is defined only inside one
dimension; that is the law. It is not yet an L because no application has demanded it (W4), but
sonolocalización has metres, seconds and a speed of sound, so the pressure exists. Draft 3 lists
it in the open items as a candidate L under G0 with that derivation, and the quimulun repository
as its precedent.

## What changes in draft 3 without a decision

L12 reworded (item 1); L16 the binding sentence (2); L20 reworded (3); L21 the transport and its
condition (4); L15 your functor reading (5); G4 heading and paragraph (6); W1, W2, W3, W4, W6,
W12, W13 in your words (7 to 10, 12 to 14); quimulun (18); open items extended (16, 18).

## What needs your decision

- Item 11: `proved` by citation as a grade of a function's certificate, and identity as the
  transport (exact, or with cost over floats). Recommended yes.
- Item 15: W15, a long analysis is reported as a delicate question or as a conflict between
  principles. Recommended yes.
- Item 17: the session as a block, `<-` per command, over the dataflow of L19. Recommended yes.
