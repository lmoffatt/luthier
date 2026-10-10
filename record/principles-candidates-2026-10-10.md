# Candidates for docs/principles.md from the audios of 2026-10-09 and 2026-10-10

For the thread that works docs/principles.md (D-2026-10-10-b). Nothing here is applied to the
draft. Each item says where it comes from: an audio (record/audios, commit 60a10aa, with the
timestamp), a decision (record/decisions.md), or the model's proposal in the chat of 2026-10-10,
marked as such. The audio quotes are verbatim, transcription errors included.

## New principles

**C1. A definition has no effects; effects live only in the actions.** D-2026-10-10-c. Implicit
in L9 (a program is a DAG) and L12 (execution is the verification of equivalences), not stated.
It is the one assumption under which every evaluation strategy gives the same result. Source:
Luciano, chat 2026-10-10 ("lo que si es no-side effects").

**C2. The evaluation strategy is a parameter separate from the program; by default, forward on
demand.** D-2026-10-10-d. A plan backward from the actions over names, then a strict forward run
over the live subgraph. Source: Luciano, audio 2026-10-10 11.42.15, 01:51 to 04:07 ("está el
método backward, y el forward ... uno podría pensar que tenés que tener las dos formas de
trabajar, las dos tienen un rol"); chat 2026-10-10 ("Lo ideal es no elegir, es decir, poder
expresar todo, solo elegir lo que va por default").

## Retouches to existing principles

**L13 (forgetting is first-class)** gains its operational justification. Forward is Markovian:
"estás en un estado y ya está, todo lo que pasó antes lo olvidaste"; backward must keep its
history: "tenés que guardar las boletas de 5 años"; scope is backward's forgetting: "si hay cosas
que se salen de scope, ya está. Ahí se pierden para siempre". Source: audio 2026-10-10 11.42.15,
01:07 and 03:20 to 03:55. With D-2026-10-10-d the plan knows each node's last consumer, so
backward also forgets as soon as it can (the model's observation).

**L9 (a program is a DAG)** should separate two structures: the DAG of definitions, which says
what depends on what and has no cycles once operations are declared before their laws; and the
structure the laws generate over terms, an equivalence (islands, a quotient) when laws are
boolean and a metric space when laws carry a distance. L10 (one function, many paths) and L12
live in the second. Source: Luciano, chat 2026-10-10 ("las relaciones de equivalencia generan
islas separadas. Mas complejo es las relaciones de distancia: estas generarian un espacio
metrico"); the separation is the model's proposal.

**L11 (verification is one operation, exact or statistical)** should say that the grade of
evidence depends on the distribution sampled, not only on the number of samples, and that errors
concentrate at the edges (zero, empty, overflow, NaN), against the audio's assumption that an
error "te trastocarían todos los valores". Source: audio 2026-10-10 11.11.22, 03:02 to 04:12
(grades 1, 2, 3 by 100 or 200 samples); the correction is the model's, from the practice of
QuickCheck, Hypothesis, LAPACK's test matrices.

**L5 (a law characterizes; it does not re-run)** gains coherence: a law over several functions is
"una especie de rompecabezas" tested on the values actually computed, and associativity only
appears when three numbers are summed; testing every path "es un delirio". Source: audio
2026-10-10 10.12.21, 11:38 to 18:20; 11.11.22, 02:14 to 02:44. The model's addition: the cases
to test are the generators the law's theory dictates (generalized associativity, Mac Lane's
coherence), not a sample of paths.

**L4 (the certified subtype from a predicate)** receives the scope decision: types by
verification first, types by construction later, because construction "implican un mayor
conocimiento que yo tengo, pero podría ser a lo largo eso que se incorpore". A law gives three
things at once: the type, the constructor with Maybe, the membership function. Source: audio
2026-10-10 10.12.21, 05:24 to 08:10.

**L3 (defining a function defines its test)** joins D-2026-10-10-d: the tests are actions, so
verification enters the same plan as the prints.

**L10 (one function, many paths)** stated as a quotient: the implementations of a function are
the quotient by the equivalence "compute the same function up to the law's equality"; one class
per mathematical function, and inside the class the fibre of what differs: speed, error, place
of execution. "Las implementaciones de una función son el quotient sobre el predicate de las
leyes de esa función ... sería la parte que representa el grupo de equivalencia y después las
diferencias". Source: audio 2026-10-10 16.49.14 (8a4c70f), 00:04 to 01:39; the same idea without
the word on 2026-05-30 (`note:2026-05-30T18.01.53:equivalencias-para-clasificar-y-separar-decoraciones`).
The model's precision: the predicate of a law gives a subset (L4), the equivalence is between
implementations that satisfy it, and the class is chosen by law, the fibre by cost.

**L14 (Luthier orchestrates other languages)** gains the conversion cost: the same function over
lists and over vectors, in Python and in R, the same data in two file formats, are models of one
function on equivalent classes, and converting between representations has a cost, so conversion
is one more edge in the graph of paths of L10. Source: audio 2026-10-10 16.49.14, 01:39 to 03:18.
Prior art: representation independence (Reynolds).

## Ideas of the audios the draft does not have

**What never reaches an output needs no certificate.** "lo único que se ve es lo que modifica el
mundo, es decir, lo que se imprime, lo que se guarda ... son variables internas del programa que
no nos producen un output, esas no, calcularlas o no, no lo vas a saber nunca si lo verdadero o
no". Source: audio 2026-10-10 11.42.15, 02:37 to 03:05. The ground of verification on demand.

**The program is the synthesis of the computation; what is kept is the program.** "la longitud
de un programa frente a la rectitud de un cálculo. Un cálculo puede crecer mucho porque expande
las variables de búsqueda. En cambio el programa, bueno, no tanto, porque justamente está escrito
de una manera sintética ... Nunca olvidarías el programa". Source: audio 2026-10-10 11.42.15,
01:02 to 01:51. The same figure as the audio of 2026-10-09 10.43.06 on expansion and synthesis
("una especie de un ciclo de respiración", 03:14 to 03:23), reached from the other side. P2
(everything derived carries how it was derived) applied to execution.

**A synthesis can be judged; a long text cannot.** "Una síntesis uno la puede analizar, porque es
una síntesis y tiene pocos conceptos ... El problema es cuando ya es muy largo y tiene ideas que
uno no maneja del todo ... y ahí dudas de todo". Source: audio 2026-10-09 10.43.06, 04:24 to
05:06. For the way of working (P12), a criterion for what the model brings him.

**Mutable parameters as before and after.** D-2026-10-10-e.

**Decorations are demanded at the print.** The same code computes the value, the value with
error, the derivative, the test, "cualquier monad o decoración", and which one is said when the
print is asked: "cuando vos demandás, demandás con tus condiciones". The demand marks the live
path backward "como una mancha venenosa que va para atrás"; his open question is whether
decorations are forward or backward, and how an input entered as a plain real gets an error.
Source: audio 2026-10-10 16.49.14, 03:20 to 07:06; the old term "parámetro de implementación"
(05:20). Already in his writing as "funciones que modifican el codigo: tests, errores, derivadas",
and in his C++ (`Transfer_Op_to`, the forward version). Resolved as the fourth condition of
D-2026-10-10-d (D-2026-10-10-f).

**A function captures the functions it uses by hash, and is universal over the models of its
theories.** "si ya tus funciones son ciudadanos de primera, bueno, entonces vos tenés que decir
que los estás usando ... tus funciones son las funciones de funciones". Two options in the audio:
parametrize everything, or a default that can be changed. Source: audio 2026-10-10 17.00.40
(76ba165), 00:00 to 01:49. Resolved in D-2026-10-10-g: both at once, parametrization by theory
with implicit resolution; modules as parametrized values instantiated on demand; overloads and
bridges by the orchestrator. Extends L6 and L10; the bridges extend L14.

**Modules are theories; a theoretical module is a module of holes.** "los módulos
representarían justamente teorías matemáticas ... tipos y funciones, todos con sus leyes bien
marcados, todo definido pero sin valor, y después va a haber implementaciones que en lo posible
serán genéricas". Source: audio 2026-10-10 17.25.23 (7b0481d), 00:00 to 00:40 and 03:53 to 04:25.
L8 (declare, define, inhabit) at the level of the module; D-2026-10-10-g.

**Return-type polymorphism by demand.** D-2026-10-10-h. Source: the same audio, 05:49 to 07:53.

**Absorb libraries with their laws; pivot_wider and pivot_longer as the first case.**
D-2026-10-10-i. Source: the same audio, 01:44 to 03:45. "Al tratar de escribir los tésitos, se
entiende mejor cada implementación" (02:42): the pedagogical face, for O3.

**The interpreter after MacroDR.** His C++ DSL in MacroDR (two virtual classes, one compiles and
one runs; a table from identifiers to implementations) is the inspiration for Luthier's
interpreter, where an implementation is static Luthier code and what the table needs is the
output type. Source: the same audio, 04:26 to 05:49. Not a decision; to read before implementing.

**Demand solves forgetting.** "La ventaja de la ejecución en demanda es que me soluciona el
problema del olvido. Yo no tengo que tener todos los detalles que tienen una función infinitos,
sino solamente los que te piden al final ... vos podés ponerle a cada variable una decoración
infinita que vos se la pedís a demanda ... la demanda final es la que te soluciona todo el
código". Source: audio 2026-10-10 17.28.45 (c6b302c), whole. The complement of L13 (forgetting is
first-class): dependent typing accumulates history, and the demand is what chooses which part of
it to materialize; the "infinite decoration" is code, not values (the program is the synthesis,
the computation the expansion: audio 11.42.15). The strongest single statement of
D-2026-10-10-d and f, a candidate for the wording of the strategy principle (C2).

**Luthier as a coupling language.** "el uso de luthier seria el acople entre librerias no? un
lenguaje de acople, eso me parece que seria util." The joint between two libraries is a theory
(D-2026-10-10-g) of which each library is a model; the bridges, with their cost and error, live
at the joint; so do the bugs. The rule that distinguishes it from Python as glue: no coupling
without a law, "si el tipo no sigue la ley no se aplica el calculo" (Luciano, confirming the
model's "sin ley no hay acople"). What L14 (Luthier orchestrates other languages) means in
practice; for O1 (useful now, without a native FFT) and O5 (the core is what states and checks
laws by hand; the values come from the libraries). Prior art: coordination languages (Gelernter
and Carriero 1992), glue languages (Ousterhout 1998), workflow languages (Snakemake, Nextflow).
Source: chat 2026-10-10. A position on the objectives, for record/objectives.md, which is his
to mark.

**`external` is a Luthier function that inhabits a hole with a body in another language.** It
takes a name (and a file) and gives a Maybe function: found, with its signature, declared. It
is validated like any other function: the first time an action asks for it, the plan includes
its test against the type with its laws (D-2026-10-10-d), and the certificate stays in the
store under the hash of (library and version, type), so the second time only the hash is found
(L11). "Lo que haria Luthier es validar cada una de las funciones external contra un tipo ...
la primera vez que se pida se valide y luego quede un hash de validacion" (Luciano, chat
2026-10-10). Without a type with a law to validate against, the external is not applied: the
coupling rule. The language
is stated ("podría ser obvio, pero mejor decirlo, porque así no hay sorpresas"). One
environment per language, the environments communicating through bridges (D-2026-10-10-g).
Source: audio 2026-10-10 17.41.53 (0b5bd1c), whole. L8 already names "external function" as a
face of the hole. Prior art: foreign function interfaces (Haskell's foreign import, Rust's
extern), Jupyter's one kernel per language, Apache Arrow as the shared representation of tables.
The model's two conditions, proposed: the memo key of an external carries language, library and
version (P2); `external` declares pure or effectful, an effectful external being an action, not
a definition (D-2026-10-10-c), and the declaration of purity is itself tested statistically
(same inputs twice, same result), one more law under L11.

## Left open on purpose (P8: until a real case asks for it)

Laws with values in a semiring rather than in booleans: boolean (and, or), tropical (sum, min)
for costs and distances, logarithmic (sum, logsumexp) for evidence, with the temperature T as the
parameter between them. Source: audio 2026-10-10 10.12.21, 01:56 to 02:15 and 08:15 to 10:45
(costs from zero to infinity, "cuáles son las equivalencias entre costos y las operaciones
booleanas, que eso no lo tengo muy claro"); the semirings are the model's answer. Metric
equality: a certificate carrying its tolerance, function types carrying their Lipschitz constant
(condition number), numerical laws with a normalized distance and a direction (backward or
forward error). Candidate real case: linear algebra, with LAPACK's test ratios as the reference.
Uniqueness annotations. Incremental planning.
