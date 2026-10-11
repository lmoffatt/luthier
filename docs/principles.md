# The principles of Luthier and the way it is built

Draft 5, 2026-10-11, unapproved. Draft 4 (c7c6396) was read by five models with the same prompt
(`record/IA/principles 2023 10 11 2/`, 4f4e208; synthesis
`record/contradictions-ia-2026-10-11-b.md`);
draft 5 rewords what that round caught, each retouch marked "(draft 5)"; two items wait for his
mark (L14's gate, the holotype). Draft 3 (f156aeb) was read by eight models asked for the
contradictions that would hamper implementation (`record/IA/principles 2023 10 11/`, a8e28f0;
synthesis `record/contradictions-ia-2026-10-11.md`, his marks 0d6932d); draft 4 incorporates
what that round settled, D-2026-10-11-m and -n, and the corrections it exposed, each retouch
marked "(draft 4)". Draft 2 (cd24137) was annotated by Luciano (2c18c41), answered
(`record/answers-annotations-principles-2026-10-11.md`), replied to (18da042) and answered again
(`...-b.md`); draft 3 incorporates what those two rounds settled, each retouch marked "(draft 3)".
Terminology fixed in this draft: a *theory* is a type with laws, usually parameterized; a *model*
is a value of a theory; a *module* is a file as a namespace today and a value by design (L20); an
*object*
is the cycle of a type and its laws (`05 §3`). Draft 1 (d6a4ff5)
listed twenty principles of the language and fourteen of the way of working as peers. Draft 2
derives the twenty from his organizers, as he asked in `record/Lucianos ideas/principios
organizadores.txt` ("un principio es un organizador y como su nombre lo indica es el primero"),
following `record/plan-principles-generative-2026-10-11-decisions.md` (D1 to D8, taken as
recommended on his instruction to write the file; his marks pending) and the analysis
`record/organizing-principles-2026-10-11.md` (addenda 1 to 8). The organizers are his, quoted
verbatim; each formulation of at most two lines, each derivation and each move is the model's and
is marked *Proposed*. Statements and sources of the L and W are those of draft 1 unless a retouch
is marked. L numbers are kept (D4); the order follows the organizers. The record of the principles
in force, P1 to P14, stays `record/principles.md` and is cited where an L restates one (D7).

The check of P13 (a principle is worth the decisions it guides), over the 56 entries of
`record/decisions.md` by the L and P named in their Kind lines (D5):

| Organizer | Decisions guided |
|---|---|
| G0 the guide | 15 |
| G1 demand | 5 |
| G2 description | 8 |
| G3 cost | 1 (D-2026-10-10-g) |
| G4 expressive | 4 |

G3 guides one decision so far and is marked candidate, as D5 says; §3 below says why it is
load-bearing anyway.

## 1. The guide, the two eurekas, the principles of good use

Three tiers, in his words (`record/audios/WhatsApp Ptt 2026-10-11 at 09.19.36.md`, 00:00 to
00:53): the guide, two eureka moments, and after them "principios de buen uso".

### The guide

**G0. Type theory is the guide.** Source: "Un principio es hott/Category theory/ type theory
guidance. De ahi sale types as propositions y funcions as types y por ende functions defined as
propositions, laws. De ahi sale que las laws definen objetos matematicos. y tambien que con una
law tenes un cociente y por lo tanto valores intercambiables y por lo tanto optimizacion por
tiempo y costo en memoria o por error." (note, fa3f972); "la guía es la te[o]ría de tipos" (audio
09.19, 00:00).
*Proposed* formulation: a type is a proposition and a value its proof; a law is a proposition
over terms, so it defines a mathematical object and a quotient, and inside a class the
representative is free; (draft 5) free in the theory, where the law is exact; in a model the
planner's freedom is what L10 states. What follows departs from type theory in four places, each
named below
by what type theory lacks.

### The two eurekas

**G1. The demand defines what is computed.** Source: "la demanda de un valor por el mundo externo
me define todos los tipos necesarios para obtener eso" (audio 09.19, 00:24); "la compilacion se
dispara por la demanda externa (es decir un print o un valor que sale al mundo), y la demanda
determina el tipo que quiere el print, y eso determinan 1) el camino que efectivamente se computa
y los tipos que efectivamente se computan" (note); its root, "la clara separacion entre lo
declarativo y lo ejecutivo. Esto dio lugar a la idea de que lo ejecutivo se da por la demanda. Y
lo declarativo pasa a ser todo lo universal posible, minimamente procesado" (note, 1c7a284); "lo
que se sabe, que es un poco como la idea del prior" (audio 08.58, 08:59).
*Proposed* formulation: the declarative face states what is known, universal and minimally
processed; the executive face is a demand from outside, and the demanded type fixes the path, the
types and the tolerances actually produced. What type theory lacks: an executive face; there,
computation is the normalization of a given term, with no demand.

**G2. A function type is its laws; a function is known by description.** Source: "el disparador es
darme cuenta de eso, que los tipos de funciones son las leyes que las definen. Esa fue mi eureka
moment" (audio 09.19, 00:00 to 00:14); "Las leyes deben ser propiedades (matematicas o no) que
determinen univocamente la funcion que estamos definiendo. Las funciones se definen a lo Russel.
Y se testean empiricamente. Que una implementacion sea valor de un tipo de funcion siginfica que
ya fue validada aunque sea una vez. Y la validacion de las funciones es progresiva" (note); "no
ser a lo tarski (constructivo) sino a lo matematico (desde afuera, como un entomologo observa un
bicho)" (chat, D-2026-10-11-d); the composition of invariances as "la parte Tarski" (audio 08.58,
32:01 to 34:07).
*Proposed* formulation: the laws are what is known of a function, and the implementation, native
or extern, is the specimen under observation. A description is derived by composition of the
laws of the parts when such a law exists, and observed otherwise; laws accumulate, and a set of
laws that determines the function up to its equality is the limit a definition may reach, not what
it must reach (D-2026-10-11-d). (Draft 3) A law is written over the signature of its theory, an
implementation over a model; the first is the holotype, `\ x { x * x }` as the formula of `Sqr`,
the second a specimen checked against it (his "holotipos", second round §3; `00`, *Value, the
model*; `05` R10). (Draft 5, correction of this reading proposed, his mark pending) In nomenclature
the holotype is the name-bearing specimen and the diagnosis is the text, so: the law is the
diagnosis; a reference implementation, the formula over `Rational` or the native, is the holotype;
every other implementation is a specimen compared to the holotype by the identity law (L21) and to
the diagnosis by the laws. What type theory lacks: it knows a function by acquaintance, as its term.

### Principles of good use

**G3. Laws are valued in cost, and what a run teaches is kept.** Source: "queremos que Luthier use
Bayes como guia tambien. Esto implica que las leyes no sean predicativos a un bool sino a un costo
real positivo. Esta parte es la menos desarrollada ... Usar un object classifier de Lavwere seria
el marco unificador. Y usar estadistica bayesiana para componerlo" (note); "El problema de la
teoria de tipos es que funciona para enteros y deja de funcionar para float y para linear algebra
o estadistica. Ahi la teoria de tipos booleana falla y si queres ser estricto o expresivo,
necesitas otra cosa. De ahi el [0, +inf)" (`el problema de los floating point.txt`, 5cc41fa);
"cuando vos corres un programa aprendés algo y eso que aprendés queda en algún lado ... es como un
deseo más que un principio" (audio 08.58, 05:47 to 06:08).
*Proposed* formulation: a law is valued in [0,∞), 0 true and ∞ false, so that one law serves every
representation and the demand supplies the tolerance; over floats the cost of a law is itself
estimated, so its value is uncertain and evidence composes as Bayes composes it, and is kept
across runs. What type theory lacks: two truth values, and a run that leaves nothing. The reason
to depart is not that type theory fails on floats (Flocq proves exact theorems about them) but
what the Boolean way costs: a tolerance fixed in each law, worst-case bounds that compose into
condition numbers, and nothing to say about data (`record/organizing-principles-2026-10-11.md`,
addendum 2). Articulated in `docs/rationale/11-cost-valued-laws.md`, draft 0 (D6). Candidate by
the P13 check, in his words a wish.

**G4. Expressive over restrictive; it decides between designs.** Source: "Luthier debe ser expresivo
mas que restrictivo: si hay
mas de una forma de hacer las cosas, todas deberian poder ser expresadas en Luthier" (note).
*Proposed* formulation: when the language could forbid or allow, it allows and asks for the law
that makes the alternatives equivalent; a free choice among equivalents is legitimate (P5). It
decides between designs rather than describing the language: when G0 to G3 allow two designs
equally, G4 chooses the one that allows both and asks for the law that makes them equivalent, so
it generates no L of its own and appears as the reason behind decisions (section 2, last part) and
inside L10.
What type theory lacks: one canonical form per value.

### How the organizers depend on each other (*Proposed*, D8)

1. G0's quotient needs G1 and G3 where the carrier carries a distance: there two implementations
   are interchangeable only up to a distance and below the tolerance the demanded type carries.
   (Draft 4) On decidable carriers the exact quotient is correct and the kernel proceeds without
   G3; "optimización por error" has no meaning there and needs none. The interface that lets G3
   arrive without a rewrite: every law returns a `Cost`, and `Bool` is the two-valued case, the
   type of the result saying which (`11` §2, L21). (Draft 5) A law into `Cost` returns a measure;
   the proposition is cost ≤ ε with ε the demand's, so G0's "a law is a proposition" holds once the
   tolerance is supplied. Until G3's algebra exists the application runs on this Boolean interim:
   laws of the form d(f x, g x) ≤ tol with tol a parameter (L17), no composition of tolerances
   along a chain, no run database.
2. G2's inhabitance needs G3: "validada aunque sea una vez" gives the certificate of a : A a
   grade, which is sound only if truth is graded. (Draft 4) The judgment itself stays one and
   structural; the grade is its evidence (L2, `11` §4).
3. G1's planner is G0's proof search with G3's cost: it searches for an inhabitant of the
   demanded type and ranks candidates by cost.

So G3, the least developed, is load-bearing for G0 and G2 over carriers with a distance, whatever
the P13 count says today; over decidable carriers the Boolean kernel stands on its own.

## 2. The language

Each L keeps its number and source from draft 1. "From" names the organizers it derives from
and the derivation, *Proposed*. Order: by first organizer.

### From the guide, G0

**L2. A type is a proposition, and membership is a guarantee.** Belonging to a type asserts the
propositions, laws included, that the value satisfies; function types carry their laws the same
way. (Draft 4) `a : A` is one judgment, structural and decidable for the kernel's types; what a
law adds is evidence, and the certificate of the law carries its grade (proved, exhaustive, cases,
sampled, assumed) and, for a law into `Cost`, the worst cost seen (`11` §4). The guarantee is what
the certificate says and no more, and what leaves the program carries one (L19, D-2026-10-11-n).
From G0 directly; the second clause is the step to G2. Source: Luciano, 2022-08-03
(`written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple`); restated 2026-05-26
(`day:2026-05-26:tipos-como-conceptos-y-proposiciones`).

**L4. The certified subtype from a predicate is the fundamental construction pattern.** From a
material type and a predicate come the certified type, its only constructor and the forgetful
projection; the same pattern builds values, functions and programs. A law gives the three at
once: the type, the constructor with Maybe, the membership function; (draft 4) where the law is
into `Cost`, the constructor takes the tolerance as a parameter (L17) and the certificate records
the tolerance it was checked at, so a stricter demand asks for a new check (`11` §4). Types are
verified before
they are constructed: Luthier starts from types by verification, and types by construction may
come in later. From G0 (a predicate is a proposition; its subtype is the type of its proofs) with
G2 (verified, not constructed). Source: Luciano, 2022-08-03
(`written:2022-08-03_haskell:subtipos-con-predicado`); named fundamental 2026-09-29
(`record/distillation/2026-10-09_find_principles_v2_claude-code_opus.md`, C3); the three things and
the scope 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 10.12.21.md`, 05:24 to 08:10).

**L5. A law characterizes; it does not re-run.** A law states a mathematical property of an
operation; a second implementation checked against the first is consistency, and the native
definition is one more model certified against the law. A law over several functions is tested
on the values actually computed, as a puzzle whose pieces must fit; the cases to test are
chosen by the law, its arity (three elements for associativity) and the distribution sampled
(L11), never every path.
Retouched (D-2026-10-11-d): laws accumulate, and a law need not determine the operation; when
the laws do determine it up to the presentation's equality, that is the limit. From G0 (a law
defines the object) and G2 (a law that transcribes the specimen is acquaintance, not
description). Source: Luciano, 2026-10-05 ("La idea en realidad es buscar el objeto matematico
que mejor lo represente y decirlo"); extends P10 (the mathematical object that best represents a
concept is the invariant of its type); the puzzle 2026-10-10 (`WhatsApp Ptt 2026-10-10 at
10.12.21.md`, 11:38 to 18:20); the generators are the model's addition.

**L6. Code is data.** A Luthier program is an element of Luthier; programs build, inspect and run
other programs, and the interpreter is meant to be written in the language it interprets. From
G0 through the universe, the type of types (the object classifier of HoTT; the note's "object
classifier" names this when it means types as values, and the subobject classifier when it means
G3's truth values). Source: Luciano, 2022-06-15 (`written:2022-06-15_sin-titulo-2:codigo-es-dato`).

**L7. The core is minimal and executable by hand.** A handful of well-specified primitives, so
that a program can be run with pencil and paper; everything else is a library whose translation to
the core is mechanical. (Draft 4) Hand execution is of the kernel given a plan, an order of
execution that is a value (`lib/plan.lut`); the planner's choice among plans is outside the kernel.
From G0 (a type theory is a few rules whose judgments a person checks; a
small trusted kernel) and G2 (the paper semantics is the description, and every interpreter is a
specimen certified against it). Source: Luciano, 2026-05-29 ("Luthier tendría que ser ejecutable a
mano"). Draft 0 of the plan proposed moving it to the way of working; withdrawn (D3).

**L8. Declare, then define, then inhabit.** A declaration without a body is a first-class hole: at
once axiom, program input, external function, pending definition and dead code; nothing executes
until it is defined, and no value inhabits an undefined type. (Draft 4) To the type checker the five
are one, and
the elaborated form records which it is, since the demand treats them differently: an input asks
for a value, an external calls the host, a pending definition is an error, an axiom is a law with
grade `assumed`, reasoned with and never run (an item for the spec; (draft 5) `assumed` has one
meaning, the grade). `extern` is the operation that
inhabits a hole with a body in another language, naming the language; a theoretical module (types,
functions, laws, no values) is a module of holes. From G0 (a hole is a hypothesis of the context)
with G1 (nothing is produced until demanded). Source: Luciano, 2026-05-29
(`dialogue:20260529T1400:tipos-no-definidos-y-forward-reference`); the hole named 2026-09-29;
`external` and the theoretical module 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 17.41.53.md`;
`WhatsApp Ptt 2026-10-10 at 17.25.23.md`, 00:00 to 00:40).

**L10. One function, many paths.** A function has many equivalent implementations, each with its
precision, speed, memory and place of execution; equivalence is established first, and the choice
among paths follows expected loss and cost, estimated from a database of measured runs. Stated as
a quotient: the implementations of a function are the quotient by "compute the same function up to
the law's equality", one class per mathematical function, and inside the class the fibre of what
differs; the class is chosen by law, the representative by cost. (Draft 4, D-2026-10-11-m) The class is
exact in the theory (`Real`); in a model that carries a distance it is the ball of the demanded
radius (`11` §3), and closeness is not transitive, so the planner substitutes one implementation
for another only along a certified equivalence between the two, the identity law of L21 with its
result `Bool` or `Cost`. (Draft 5) The law gives the candidates; the identity certificates say
which the planner may exchange, and they form a weighted graph, not a class: a substitution is a
path whose summed distance (`11` §2) is within the demanded tolerance, so two specimens joined
through a third may each replace it and not each other; the sum is a bound only when every link
is one (proved, exhaustive), otherwise an estimate with the weakest grade and the samples it was
seen on; a lone implementation is never replaced. The author's free choice among the inhabitants of
an under-determined function
(D-2026-10-11-d, P5) stays; the planner's choice is only among what has been compared. From G0
(the quotient), G3 (the choice by cost and the database of runs) and G4 (every path expressible,
the reason behind the decision). Source: Luciano,
2022-06-28 (`written:2022-06-28_luciano-code-style:choose-efficient-path-after-validity`); the
quotient 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 16.49.14.md`, 00:04 to 01:39), the same idea
without the word 2026-05-30
(`note:2026-05-30T18.01.53:equivalencias-para-clasificar-y-separar-decoraciones`).

**L12. Evaluation is verification; execution is an action on the world.** Luthier first describes
the problem and its equivalences; evaluating is checking them, as mathematics verifies rather
than runs. (Draft 3, his annotation) Executing is the executive face: an action changes the state
of the world, and it is verified too, by observing the world before and after it; the laws over
actions are stated over those two observations, as a mutable parameter is two variables (L9);
(draft 4) an observation is itself an action, so this stops where the world can
be read back (a file written and reread), and says nothing beyond.
Retouched (addenda 7 and 8): every function induces an equivalence on its domain, its kernel, so
computing f(x) is placing x in its class and the value is the class's name, (draft 5) an
interpretation of computation, not the evaluator's mechanism; a predicate is the
two-class case and `Maybe T` places x in one of them. This equivalence on the domain is distinct
from the equivalence between terms that a law induces, which is L10's quotient. From G0 (identity
is the first proposition; his "path equivalence is the fundamental concept", 2026-05-29); the
two faces are G1's statement; the verification of actions from G2 (observation) and G1. Source:
Luciano, 2026-05-30 ("la matemática no ejecuta ... la
ejecución en Luthier sería esa verificación de equivalencias"); the kernel reading 2026-10-11
(chat: "una funcion genera equivalencias f(a)==f(b) ==> a~b y mas si f(a)=true"); the actions
2026-10-11 (annotation on draft 2: "las ejecuciones tambien se verifican observando el mundo antes
y despues del acto").

**L16. Equality has levels and belongs to the object.** Definition (`:=`), the identity
proposition (`=`), decidable equality (`==`) and definitional equality by reduction (`≡`) are
different things, and each object carries the observational equality that fits it. (Draft 3, his
annotation) The binding acts are two, `:=` once and `<-` rebinding, and they share one law: after
the act the name equals the term in the equality its type has, structural `==` where it exists
(`05` R8), observational otherwise, a distance under G3; after `:=` for all time, after `<-` until
the next `<-` (`05` R12). (Draft 4) In the kernel the binding is exact: the name denotes the term,
and reduction does not depend on a tolerance; the distance enters when the planner realizes the
term by another representative, which it does only along a certified equivalence carrying its
distance (L10, D-2026-10-11-m). From G0 (the identity type and its levels) with G3 (under cost, the
identity proposition acquires a distance). Source: Luciano, 2026-05-30
(`day:2026-05-30:niveles-de-equivalencia`); the law of a binding 2026-10-11 (reply: "luego de <-
lh == rh, de hecho creo que es la ley de <-").

**L20. A function is declared in a theory and is universal over its models.** (Draft 3, reworded
after his annotation.) A function belongs to a theory (Real, Field, LinearAlgebra) and takes its
model as its first, often implicit, argument, so it is written once for every model; (draft 4) the
model is
named by the type of the argument (D-2026-10-11-j) and can be passed explicitly. A theory over a
model of another theory is
a theory. Every type belongs to a theory; the concrete types (products, sums, exponentials,
`data`) belong to the kernel's, whose laws are the β and η rules and the recursion principle,
stated in `lib/kernel_laws.lut` (third and fourth rounds). Operators are resolved by the type, the
type naming its model; a carrier with two models is two types (D-2026-10-11-j). Modules are values
by design, files today: a parametrized module is a function from models to
definitions, applicative because definitions have no effects (L18), instantiated on demand with
the parameter threaded down from the action. A specialization is one more representative of the
law's class (L10), valid on a subtype, certified against the same law; where representations
differ, the orchestrator inserts bridges by cost, coherent up to the law, carrying their error,
visible in the plan; (draft 5) a specialization and a bridge each enter the planner's graph by an
identity certificate with its distance (L10, D-2026-10-11-m). From G0 (a theory is a type, a model
its inhabitant) and G1 ("lo declarativo
pasa a ser todo lo universal posible"; instantiated on demand). Source: Luciano, 2026-10-10 ("el
codigo seria, en principio universal a los valores de funciones que cumplan las leyes requeridas",
chat; `WhatsApp Ptt 2026-10-10 at 17.00.40.md`; `WhatsApp Ptt 2026-10-10 at 17.25.23.md`, 00:00 to
04:25; D-2026-10-10-g). The conditions on bridges are the model's, accepted.

### From the demand, G1

**L9. A program is a DAG and statements commute.** The unit is the definition; dependencies give
the only order there is, and time is reconstructed from them rather than from the text; (draft 5)
inside a block the text fixes which binding a name means, each `<-` a fresh name (D-2026-10-11-i),
and then dependencies give the only order: after `x <- 1`, `y := x + 10`, `x <- 2`, y is 11, as
the session answers.
Operations are declared before their laws, so a law that binds two operations is a node with two
parents, not a cycle; a mutable parameter is two variables, before and after, and mutation in
place is the planner's optimization when the earlier one has no other consumer. The DAG says what
depends on what; the structure the laws generate over terms (an equivalence when laws are boolean,
a metric space when they carry a distance) is a second structure, where L10 and L12 live. From G1
(the DAG is what the demand walks backward) with G3 (the second structure's metric). Source:
Luciano, 2026-05-29 (`note:2026-05-29T14.46.22:contexto-como-dag`); the unordered set of
definitions already in 2023-03-13 (`written:2023-03-13_hacia-luthier`); the two structures and the
mutable parameters 2026-10-10 (chat; D-2026-10-10-e); the separation of the second structure is
the model's proposal.

**L13. Forgetting is determined by the demand.** Dependent typing accumulates history, so the
language needs non-invertible forgetful projections, and the demand chooses them: what is
forgotten is everything the demanded value does not need, the complement of its dependency cone,
so the projection is canonical, one per demand, and the language being spoken is what was asked
for. Forgetting at run time (a node freed after its last consumer) and forgetting in the type (how
much history a certificate keeps) are one; the program is never forgotten, only what leaves scope
is lost. Retouched (audios 09.01 and 09.21): a function on a type applied to a subtype does not
produce one overload per subtype; the demanded return type selects which law to derive by
composition (G2), and the rest is forgotten: doubling positives is positive only when positivity
is demanded and derivable, sin of positives forgets to Real because no law composes. (Draft 4)
What is derivable is a property of the expression, independent of the demand; the demand chooses
which of it is derived, certified and carried, so the elaboration (types, derivable laws) does not
depend on the observer; (draft 5) the memo of results does (L19), and they are two caches. From G1
directly, with G2 for what is derived. Source: Luciano, 2026-05-29
(`note:2026-05-29T14.52.08:problema-del-olvido`); resolved 2026-10-10 ("olvidar esta determinado
por todo lo que no hay que recordar, es decir lo que pide el valor demandado. Eso soluciona el
tema de los functores de olvido", chat; `WhatsApp Ptt 2026-10-10 at 11.42.15.md`, 01:07 and 03:20
to 03:55; `WhatsApp Ptt 2026-10-10 at 17.28.45.md`); the overloads 2026-10-11 (`WhatsApp Ptt
2026-10-11 at 09.21.05.md`, 00:00 to 00:29; `09.01.13.md`).

**L17. Every criterion is a parameter.** Thresholds, budgets, limits and statistical levels are
never constants in code; they are declared, passed and recorded. From G1 (the tolerance belongs to
the demand) and G3 (a law states a distance, not a threshold), so a constant in the code has no
place to live; restates P11 (every criterion is a parameter, never a constant in the code).
Source: P11, in force; first applied as a rule of the language 2026-10-05
(`dialogue:c7437496:lmmaxiter-should-be-a-parameter`). Draft 0 of the plan proposed moving it to
the way of working; withdrawn (D3).

**L18. A definition has no effects.** Its result depends only on its inputs; effects live only in
the actions (print, save). A mutable parameter written as before and after is not an effect, the
dependence is an edge; what is forbidden is what the graph does not show. It is the one assumption
under which every evaluation strategy gives the same result; (draft 4) over a carrier with a
distance, a result in the same class at a distance the plan records, and for the Boolean case this
is `Confluent` in `lib/plan.lut`, a law a dataflow is certified against rather than a theorem
assumed. From G1 as its precondition rather
than its consequence: the declarative face can be universal and minimally processed only if
definitions have no effects. Source: Luciano, 2026-10-10 ("lo que si es no-side effects", chat;
D-2026-10-10-c).

**L19. The demand determines the computation.** The evaluation strategy is a parameter separate
from the program (L17); by default, a plan backward from the actions over names, evaluating
nothing, then a strict forward run over the live subgraph, each node once and whole: forward on
demand. What the action asks for flows backward along the plan and is produced forward: the
value, its error, its derivative, its test, the type of its result; at the leaves a value lifts on
its own, takes a mark given with the demand, or is a hole. The tests are actions, so verifying is
demanding.
What never reaches an output needs no certificate, and what reaches one carries its cone's
certificates (D-2026-10-11-n; `test` demands certificates without values). (Draft 4) A result is
identified by code, inputs, mode, the demanded type and tolerance, the model its type names, the
seed, and the plan that produced it, the plan being a value (`lib/plan.lut`); the run database is
what the planner reads to choose the plan and is not an input of the result once the plan is
fixed; evidence accumulates by a separate action with its own record, so "each node once" and
G3's "kept across runs" never meet on one node. (Draft 5) A test is an action whose result is a
certificate, memoized by the certificate's identity (code, cases, seed, the distribution and level
sampled, L11) and rerun when asked or when that identity changed; the demand states the grade it
requires (P11), and a certificate serves every demand whose tolerance and grade it meets (`11` §4).
The program is the synthesis and is kept, the
computation is the expansion and is redone. From G1 directly; the audio of 08.58 (15:35 to 17:12,
30:37 to 31:21) adds the
iteration step, read every demand, run, collapse to the outputs, write, and asks whether the code
object is consumed or stable: kept. Script and interpreter are the same under this L, one batch
of demands or demands one at a time with the memo between them (08.58, 17:12 to 23:35; an item
for the spec, 04 §7); a session is a block and a file is never one, so a session saved to a file
becomes its `main` block (D-2026-10-11-i). Source: Luciano, 2026-10-10 (`WhatsApp Ptt 2026-10-10 at
11.11.22.md`, 00:00;
`WhatsApp Ptt 2026-10-10 at 11.42.15.md`, 01:02 to 04:07; `WhatsApp Ptt 2026-10-10 at 16.49.14.md`,
03:20 to 07:06; `WhatsApp Ptt 2026-10-10 at 17.25.23.md`, 05:49 to 07:53; `WhatsApp Ptt 2026-10-10
at 17.28.45.md`; D-2026-10-10-d, f, h). The three cases at the leaves and the memo key are the
model's, accepted.

### From description, G2

**L1. Luthier expresses the invariances of the disciplines.** What moves the language: a species
mates within itself, electrons are fermions, a probability integrates to one. A definition states
the invariances that determine a concept, and the language exists so that stating them is natural.
From G2 (what is known of a thing is its description; "la idea de luthier es ayudar a descubrir
las invariantes de los calculos", note), with P14 (a type is a concept). Source: Luciano,
2026-05-29 (`dialogue:20260529T1400:expresar-invarianzas-de-disciplinas`).

**L3. Defining a function defines its test.** Declaring what a function must satisfy is declaring
the test that will be run on it, so definition and verification are one act. From G2 directly:
the eureka of 09.19 in its 2022 form. Source: Luciano, 2022-08-03
(`written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test`).

**L11. Verification is one operation, exact or statistical.** (Draft 4) What is known by a theorem is
cited, what can be enumerated is checked exhaustively, what has chosen cases is checked on them,
what can only be sampled is checked statistically, and the grade of the evidence (proved,
exhaustive, cases, sampled at a level, assumed) travels with the value in a certificate hashed over
its dependency cone; the line is the method, since associativity over `Int` is computable and
cannot be checked by running. The grade of a sampled certificate depends on the distribution
sampled, not only
on the number of samples, because errors concentrate at the edges. From G2 (observation is how a
description is verified) and G3 (the grade is the uncertainty of the cost). Source: Luciano,
2022-08-03 and 2023-02-22 (`written:2023-02-22_tapp-wish-list:untested-a-tested`); the grades by
samples 2026-10-10 (`WhatsApp Ptt 2026-10-10 at 11.11.22.md`, 03:02 to 04:12); the dependence on
the distribution is the model's correction, from the practice of property-based testing.

**L14. Luthier orchestrates other languages.** Types and laws are native; values may come through
`extern` from Python or any host, declared over what they really receive and return, with
description and verification kept on Luthier's side. An external function is validated like any
other, against its type with its laws, the first time an action asks for it, and its certificate
stays by hash; without a type with a law to validate against it is not applied. (Draft 5, retouch
proposed, his mark pending) His words are "si el tipo no sigue la ley no se aplica el calculo": an
extern is applied under its declared type; where the type has laws it is validated against them
first and refused if it fails; where it has none yet, as every function starts (D-2026-10-11-d), it
runs with its certificate graded by what it has and may replace the native only by the identity
law of L21 (D-2026-10-11-m), which admits a specimen and never certifies the description, so G2 is
not bypassed. The extern's hash includes the host library's version (W10), and its declaration
says whether it is a definition or an action (L12, L18). (Draft 4,
D-2026-10-11-n) This is the default for every value: demanding a value demands every certificate
in its dependency cone, paid once through the memo, unless the demand asks otherwise by a
mechanism to be named, which leaves a certificate of grade `assumed` (draft 5), since what could
be done Luthier gives a way to do (G4); `test` is the action that demands certificates without
values (L19). Luthier is in use
a coupling language: the joint between two libraries is a theory of which each is a model, the
bridges between representations live at the joint with their cost and error, and no coupling
without a law. From G2: an absorbed library is a specimen known by its description, and its code
is not needed; "que la IA pueda ... extraer de librerías ajenas, chuparlas y usar las funciones
con sus propias invarianzas" (audio 08.58, 31:25 to 32:00). Source: Luciano, 2026-05-26
(`note:2026-05-26T12.32.24:lenguaje-no-atado-a-cpp`); the validation on first demand and the
coupling language 2026-10-10 (chat: "si el tipo no sigue la ley no se aplica el calculo";
`WhatsApp Ptt 2026-10-10 at 17.41.53.md`; `WhatsApp Ptt 2026-10-10 at 16.49.14.md`, 01:39 to
03:18). Draft 0 of the plan proposed moving its orchestration half to the way of working;
withdrawn (D3).

**L21. A certificate of identity is not a certificate of the law.** *Proposed*, candidate. Checking
that an implementation gives the same bits as before, with the same seed, certifies that the
implementation has not changed; checking it against its laws, by chosen or sampled cases,
certifies the description. Both are kept, apart, and the certificate of the law travels by the
certificate of identity (his annotation): exactly where the identity is boolean (`==` structural,
`05` R8: integers, decidable types, the same implementation rerun), and with the observed distance
added where it is a cost (G3), since two implementations over floats are almost never
bit-identical. The type of the identity law's result says which (`Bool` or `Cost`). (Draft 4,
D-2026-10-11-m)
The identity law between two specimens, with its distance, is what admits a second implementation
into the class the planner moves in (L10); the agreement test of W5 between native and extern is
this law, and the holotype formula of G2 evaluated over `Rational` is one more specimen, with grade
exact, checked by the same law. A function
known correct by a theorem outside Luthier is certified `proved` by citation (D-2026-10-11-f),
and the chain law, citation, native, identity, extern is carried by hash. From G2 (the specimen
can be recognized as the same specimen, or described). Source: Luciano, 2026-10-11 (`WhatsApp Ptt
2026-10-11 at
08.58.46.md`, 09:20 to 13:19: "verificar bit a bit que sea igual ... por lo menos sabés que no
cambia la implementación"; the statistical kind for "prueba científica").

### From cost, G3

**L15. The ideal world is realized with a guarantee.** Code is written over ideal objects (Real)
and realized by concrete ones (Float64); the realization's laws hold within a stated tolerance,
and the error of each step is itself a law rather than a false claim of exactness. From G3
directly: the realization's distance to the ideal law is the law's value, and the tolerance is the
demand's (G1). (Draft 3, his reading) Rounding `Real -> Float64` is a functor in Lawvere's sense,
and each law of `Real` is projected onto `Float64` with its cost; it is not a homomorphism, and
the exact map is the inclusion the other way. (Draft 4, correction proposed, his mark pending)
Rounding does not expand distances by at most a constant: two reals astride a rounding boundary
land one ulp apart at any distance, so no multiplicative constant exists; rounding is
non-expansive up to an additive defect of about ε|x|, and for subtraction and division the
sensitivity is per input, the condition number (`11` §7). The functor reading stands with
"non-expansive plus an additive term", and the cost algebra needs both parts: a multiplicative one
where a Lipschitz constant exists and an additive one where rounding enters (`11` §5, open). Source:
Luciano, 2026-05-29; the floats note of 2026-10-11 (5cc41fa); the functor 2026-10-11
(annotation: "un functor que va de Real--> Float64 y que ahi vemos algunas propiedades de Real
proyectadas en Float").

### Decided by G4

G4 generates no L of its own and decides between designs: `:=` once and `<-` for rebinding with
default arguments (D-2026-10-11-c), `if` without `else` as a guarded value (D-2026-10-11-b), many
paths expressible (L10), accumulating laws rather than required characterization (D-2026-10-11-d).

## 3. The way of working

Unchanged from draft 1 except W5, restated.

**W1. The specification comes before the implementation.** Syntax and semantics are fixed on paper
first, and the implementation passes the specification instead of silently defining the language.
(Draft 3) The implementation may return a counterexample to the specification, a program it
accepts and nothing can run, or two rules that cannot both hold; the specification then changes by
a recorded decision, never silently (W9 is what the implementation does meanwhile). Source:
Luciano, 2026-06-03 (`day:2026-06-03:primero-sintaxis-y-semantica-despues-implementar`).

**W2. No rule enters without a worked example.** Each principle is tried by hand in the candidate
notation before it enters, and each rule of the specification is written as accept/reject pairs,
so the specification is an executable suite. (Draft 3) "El ejercicio clears the mind": a worked
example shows contradictions that are not obvious. Source: the model from Luciano's audios,
2026-08-31
(`dialogue:e6fc53cf:disciplina-ejemplo-en-papel`); the pairs 2026-10-04
(`dialogue:52d3e68e:short-cascade-with-pilot-spec-as-tests`).

**W4. The real application drives the growth.** Luthier must take root in something useful
(sonolocalización) and grow only where the application finds something it cannot express; kernel
work without real pressure moves the specification for nothing. (Draft 3) The motor of growth; W3
is its brake. Source: Luciano, 2026-09-21
(`day:2026-09-21:luthier-tiene-que-ser-util`).

**W3. Start minimal and add only what is used.** Begin from zero with the indispensable, do each
step in detail before scaling, and reduce until removing more would break something needed. (Draft
3) Its job is to stop the proliferation of abstractions; a brake, not a motor, and in his words
not often invoked. The order of work, not a limit on the language (G4). Source: Luciano, 2026-10-02
(`dialogue:51cca364:empezar-de-cero-con-luthier-liviano`).

**W5. Concepts live in Luthier, execution in the host; native against extern is bootstrapping.**
The `.lut` is designed before the Python; each concept is written native (slow, conceptual) and
extern (fast, pragmatic) with the test that they agree, and work has gone astray whenever something
that belongs in Luthier sits in Python. Restated (D-2026-10-11-d, G2): the native definition is
not an oracle, since "agrees with the native" would be a law that copies an implementation; it is
one more specimen (L5), the agreement test is a consistency check between specimens, (draft 4) which
is the identity
law of L21 that admits the second specimen into the planner's class (D-2026-10-11-m), and the
practice holds while a function has too few laws to be known by description. Source: Luciano,
2026-09-30.

**W6. A test must fail when the thing is wrong.** Laws are written before the algorithm; a law not
known to be true is worse than a hole, (draft 5, proposed) that is, one asserted without a grade,
since a law with grade `assumed` visible is a hole that says so; negative controls and reproduced
numbers, never passing
examples alone, are what make a test diagnostic. (Draft 3, his words) A meta-test that must always
exist: the test must fail where it must fail, not only pass where it must pass; realized today by
negative controls on the input and, to implement (D-2026-10-11-h), by mutation of the
implementation: a law that no mutation fails is not diagnostic; (draft 5) mutation cannot tell a
law transcribed from the implementation from a description, since every mutation fails the
transcription; what tells them apart is that a law is stated over the theory's signature and
cannot transcribe a model's code (G2, L20). For G2. Source: Luciano, 2025-09-27
(snapshots
before tests); the control stated 2026-10-02 (`dialogue:51cca364:a-test-needs-a-negative-control`).

**W7. The design stays with Luciano.** The model describes and waits; AI work comes in scoped
steps whose results he can interpret and check, because wholesale delegation cannot be judged.
For P1 (Luciano's part stays discernible). Source: Luciano, 2026-10-07
(`day:2026-10-07:chaining-ai-output-you-can-interpret`); the PI role 2026-10-05
(`dialogue:fea341bd:el-pi-de-diseño-queda-en-luciano`).

**W8. Every phase closes on a mechanical check.** A phase of a plan names the check that closes
it; a phase without one belongs to Luciano, and every rule that can become a check becomes one
(certifier, lint, test). State lives in files, never in a conversation. Source: the model,
2026-10-05 (`dialogue:fea341bd:cada-fase-con-su-chequeo-o-es-de-luciano`), adopted by Luciano.

**W9. A patch is named as a patch.** What compensates for a missing piece is logged as such and
kept out of the specification until the piece exists. Source: the model, 2026-10-05
(`dialogue:aa680014:tres-parches-reconocidos`), adopted by Luciano.

**W10. What is derived carries how it was derived.** Inputs by hash, the script or prompt with its
version, every parameter and the seed; certificates and the record are the same discipline. P2 in
force. Source: `record/principles.md`.

**W11. Every change can be undone.** Small commits, one decision per commit, tags for what is
reproduced, ownership declared between concurrent sessions. P6 in force. Source:
`record/principles.md`.

**W12. Reports are concepts, the most important first.** What failed and what limit was hit come
first; a count says nothing. For P12 (Luciano's attention is the scarce resource); (draft 3) in his
words, "muy importante para la interacción con la IA". Source: Luciano, 2026-09-30
(`dialogue:ac750929:answers-at-concept-level`).

**W13. The foundations are rethought, the reasonable version first.** The language has been remade
many times (quimulun, tapp, macror, Luthier), each time deeper; the method is to work out the
reasonable version and then look for the wild one. G0 is the reasonable version; G1 to G3 the
wild one. (Draft 3, his words) This is the meta-method: it destabilizes the system and makes it
grow, and the art is not to destabilize it before its time. Source: Luciano, 2022-06-15
(`written:2022-06-15_sin-titulo-2:rehacer-desde-las-bases`)
and 2026-05-26 (`day:2026-05-26:razonar-primero-despues-la-locura`).

**W14. What reaches Luciano has few, rich concepts.** A synthesis can be judged because it has few
concepts; a long text with ideas he does not fully handle makes him doubt everything, and that is
what to avoid. For P12 (Luciano's attention is the scarce resource), as a criterion for what the
model brings him. (Draft 3, his annotation) His engagement is served when his cognition goes to the
strategic direction of the project, optimal by these principles; so adherence to them must be
cheap to compute (P15, proposed in his words, `record/principles.md`). Source: Luciano, 2026-10-09
(`WhatsApp Ptt 2026-10-09 at 10.43.06.md`, 04:24 to 05:06); the annotation of 2026-10-11.

**W15. A long analysis is reported as such.** (Draft 3, new, D-2026-10-11-g.) When an analysis
revisits the same decision twice without new evidence, or exceeds what one screen can carry, the
session stops and reports which it is: a delicate question, or a conflict between principles,
naming them; either goes to Luciano as one question (P12), and the second is the signal that a
principle is missing or two must be ordered (P4, P13). Source: Luciano, 2026-10-11 (annotation on
W14: "deadlocks ... legitimos ... o ilegitimos: hay una contradiccion entre los principios"; reply:
"agree"); the trigger is the model's.

## 4. What is open

- The articulation of G3, `docs/rationale/11-cost-valued-laws.md` draft 0 (D6): Ω replaced by [0,∞),
  quantitative equality, graded judgments, cost as −log p or as distance, how the uncertainty of
  a cost is represented in a certificate; the algebra of composition (second round §16): a
  Lipschitz constant per function type where known (sensitivity types, Reed and Pierce 2010;
  condition numbers), a sampled cost where not, costs adding as −log p under independence; worked
  examples the sum of n floats, a matrix inverse with κ(A), a sampled probability integrating to one.

- The composition of invariances (G2's derived route): which laws compose and how the demand
  selects them (audio 08.58, 32:01 to 34:07; audio 09.21).

- The session as a block over the dataflow of L19: `<-` to explore, `:=` to lock, a file may
  contain a block, `<-` banned at the top level of a file (decided, D-2026-10-11-i); the spec's
  `04 §7` and a section on the session.
- Done 2026-10-11, in the spec: blocks (`02 §9`, `04 §5`, `05` R12, D-2026-10-11-i); operators by
  the type naming its model (`05` R13, D-2026-10-11-j; `examples/z7ring.lut` rewritten, Z7 its own
  type and `mod 7` a certified homomorphism); Python-like separators (`02 §1`, D-2026-10-11-k);
  `cite` and `proved` by citation (`05 §7`, D-2026-10-11-f); `lib/laws.lut` split from `algebra.lut`
  (D-2026-10-11-l). Implemented 2026-10-11 in the interpreter: blocks and the session (`luthier
  session`), defaults and named arguments, R13's refusal of two models on one type, `cite` with
  `.bib` modules, exhaustive tables of `Fin n -> T`; `lib/plan.lut` states an order of execution as a
  value and confluence as a law, checked exhaustively in `examples/plan_confluence.lut`. Pending:
  actions and the world as a value; the memo between the items of a session.
- (Draft 4) From the round of critiques: the interface of `Cost` in a certificate (a
  multiplicative constant where it exists, an additive defect where rounding enters, the grade as
  a lattice, the worst cost seen; `11` §5, §6); the identity of a result in the memo (L19) and
  `plan.lut` as its carrier; the opt-out of certification in a demand (D-2026-10-11-n, syntax
  open); the kind of a hole in the elaborated form (L8); the world as an opaque, unique value so
  that an action is never served from the memo (L18, L19); L15's rounding, his mark pending.
- The kernel's theory stated in Luthier: `src/luthier/lib/kernel_laws.lut`, tested on `Fin 3`,
  `Fin 2` (`examples/kernel_finite.lut`, 10 laws, sampled); eta not statable (`05` R8), functions
  over `Fin n` not enumerated by `exhaustive` (to fix).
- `proved` by citation: the citation a `.bib` key with a resolved DOI, ISBN or URL, and who
  checked (human, ai+human, none) recorded; syntax `cite name bibkey checked ai+human` proposed,
  allowed in user code (D-2026-10-11-f as amended; to `05 §7`).
- Units as a candidate L under G0: a dimension is a proposition, dimensions form a group under
  multiplication, the quantities of one dimension a one-dimensional vector space, the whole a
  graded algebra; addition inside a dimension, multiplication across (second round §18). Precedent
  quimulun (his repository); pressure from sonolocalización (metres, seconds, the speed of sound).
