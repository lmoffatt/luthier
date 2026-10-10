---
date: 2026-10-10
notes:
  - audio: WhatsApp Ptt 2026-10-10 at 10.12.21.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 10.12.21.md
    duration: ~21:44
    sha256: 09337b28408314b6e29b8f558d4b118b98d3969f47ef422c726b363eeaaa7abf
  - audio: WhatsApp Ptt 2026-10-10 at 10.12.35.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 10.12.35.md
    duration: ~00:11
    sha256: 467e31fa2e6585cf07654adf6b5f2114386574063dc7d6417bb70662d2c234d8
  - audio: WhatsApp Ptt 2026-10-10 at 11.11.22.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 11.11.22.md
    duration: ~04:30
    sha256: 2e9165614708d96b053ffa05efd342bc7ec8141dc396bc2662e04ac9ae7fa783
  - audio: WhatsApp Ptt 2026-10-10 at 11.42.15.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 11.42.15.md
    duration: ~04:12
    sha256: d6617493d99b78df57deeeb435064ec2561fa7198482a0e41e6842bc4810fd72
  - audio: WhatsApp Ptt 2026-10-10 at 16.49.14.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 16.49.14.md
    duration: ~07:09
    sha256: 17d626cf5f996df7ceaa12512b8648a78d7f42dbbb464b3db0ecd65ca9b3b899
  - audio: WhatsApp Ptt 2026-10-10 at 17.00.40.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 17.00.40.md
    duration: ~02:05
    sha256: 89e5c7af42677199a64f1664ccd1f51684af3e3074b24e78d8d3bbc443dcbe55
  - audio: WhatsApp Ptt 2026-10-10 at 17.25.23.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 17.25.23.md
    duration: ~08:03
    sha256: cf669d4cd55ec87c977ed68850a7bde080f8957cc22add332ff9e7861d6f4389
  - audio: WhatsApp Ptt 2026-10-10 at 17.28.45.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 17.28.45.md
    duration: ~01:40
    sha256: 867894bfe15c341ee601099d9bb2e133fbeb0d38592207b21a6e77e9da2581aa
  - audio: WhatsApp Ptt 2026-10-10 at 17.41.53.mp3
    transcript: WhatsApp Ptt 2026-10-10 at 17.41.53.md
    duration: ~02:39
    sha256: 151c9a92f18c7fb3ef2d93b3228643c954e8522c502ade2efca2d5c46751b6ca
ideas: 27
quotes_found: 27/27 (match: words)
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### tipos-son-invariantes
- **What**: The first principle: types are the invariants of a discipline, and Luthier's hard part is discovering those invariants, not assuming them known.
- **Quote**: "el primer principio, por supuesto, es que los tipos son invariantes," (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[00:06]`)
- **Course**: `[00:06]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: states the principle and calls it very strong; `[00:42]`-`[00:57]`: if you already knew the invariants everything is solved, so "lo importante sería descubrirlas."

### invariantes-como-leyes-predicados
- **What**: Invariants are represented by laws, and laws are predicates: statements that something occurs, is feasible, is the case.
- **Quote**: "leyes que vienen a ser predicados, es decir, esto ocurre, esto es factible," (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[01:34]`)
- **Course**: `[01:26]`-`[01:47]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: invariants represented with laws that are predicates.

### costo-como-invariante-relajada
- **What**: A laxer version of an invariant: instead of a predicate, a cost (from zero to infinity). It yields a type-with-cost rather than a verified type, and it fits reals, where equality is really a distance.
- **Quote**: "Habría una versión, digamos, más laxa de invariantes, que sería, esto tiene un costo, ¿no?" (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[01:56]`)
- **Course**: `[01:56]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: introduces cost, important for verifying functions; `[08:41]`: "Lo que te daría no sería un tipo verificado, sino un tipo con costo."; `[11:14]`: cost as a kind of distance for reals, "y eso se parece un poco a un costo."
- **Open**: how costs combine under the boolean operations (sum, minimum, maximum, arithmetic or geometric average) is left undecided (`[09:01]`-`[10:08]`).

### tipos-como-proposiciones
- **What**: Types are propositions: a type is an assertion about something.
- **Quote**: "O sea que un tipo es una afirmación acerca de algo." (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[02:26]`)
- **Course**: `[02:20]`-`[02:29]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: types as propositions, a type asserts something.

### tipos-naturales-vs-predicativos
- **What**: Two kinds of types: natural (by construction, arising from a function) and predicative (checked by verification). Luthier starts from verification because construction demands more knowledge than he has.
- **Quote**: "Están los tipos naturales, es decir, tipos que surgen de una función, digamos." (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[02:41]`)
- **Course**: `[02:36]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: names the two kinds; `[03:24]`-`[05:13]`: by-construction (mathematical, dependent) types are harder, example of minimum known by construction; `[05:24]`: "la idea de Luthier es que los tipos proposicionales serían por testeo, por verificación."
- **Open**: whether by-construction types may be incorporated later is left undecided (`[05:46]`).

### ccc-y-leyes-construyen-tipos
- **What**: Types are built from the operations of Cartesian Closed Categories (sum, product, exponential, dependent types, booleans as elements) plus predicatives; predicatives build laws, and laws combine with or/and/if.
- **Quote**: "va a tener las operaciones de Cartesian Close Categories," (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[05:58]`)
- **Course**: `[05:58]`-`[06:10]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: the CCC operations; `[06:21]`-`[07:07]`: predicatives build laws, laws are themselves predicates over a Luthier type and combine with or/and.

### object-classifier-mas-alla-de-booleans
- **What**: Open question of whether the object classifier uses only the booleans 0 and 1, or extends to integers and positive reals.
- **Quote**: "la pregunta es si vos usás solamente como object classifier los 0 y 1 en los booleans o si también usás los enteros los reales positivos" (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[07:13]`)
- **Course**: `[07:13]`-`[07:31]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: raises it as an extension under discussion.
- **Open**: left unresolved.

### ley-genera-constructor-y-pertenencia
- **What**: One law is three things at once: it generates a type, a type constructor (with maybe), and a function telling whether a candidate belongs to the type.
- **Quote**: "o sea, son tres cosas de lo mismo" (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[08:10]`)
- **Course**: `[07:38]`-`[08:10]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: a law generates the type, the constructor with maybe, and the membership function.

### verificar-una-ley-es-un-rompecabezas
- **What**: Verifying a law (like the field laws for sum) is like a jigsaw: the law relates many elements, so checking it requires computing combinations you aren't otherwise computing, trying to complete the circles of verification by generating and testing examples.
- **Quote**: "es como una especie de reumpecabezas la ley, ¿no?" (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[13:23]`)
- **Course**: `[11:34]`-`[13:02]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: sum as a property of the whole subset, verifying needs uncomputed sums; `[14:21]`-`[14:40]`: "completar los círculos de verificación"; `[15:00]`-`[15:24]`: generate examples from the objects you name and test them; `[02:14]` of `WhatsApp Ptt 2026-10-10 at 11.11.22.mp3`: full verification is "un delirio," so prove associativity only at some point going backward.

### una-ley-se-invoca-solo-cuando-una-derivacion-la-necesita
- **What**: A law is only needed when a derivation actually invokes it: adding two numbers doesn't test associativity, three do; this calls for a record of the variables that were derived.
- **Quote**: "Vos recién, cuando sumas tres números, ves la asociatividad" (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[16:14]`)
- **Course**: `[15:56]`-`[16:14]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: two numbers don't need associativity, three do; `[16:16]`: "tener un registro de las variables que vos tuviste derivadas."
- **Open**: he toys with whether 1+2 already needs associativity (since 2 is 1+1) and leaves it half-settled (`[18:08]`-`[18:20]`).

### lazy-evaluation-y-el-problema-del-olvido
- **What**: Make evaluation lazy so expressions stay as code until demanded; the final demand (a print, a saved value) defines what to compute and pulls backward only what is needed, which solves the problem of having to remember everything.
- **Quote**: "Estoy pensando que la Lazy Evaluation sería la mejor manera de definir qué es lo que quiero exactamente definir." (`WhatsApp Ptt 2026-10-10 at 11.11.22.mp3` `[00:00]`)
- **Course**: `[19:15]`-`[19:30]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: with lazy iter the sum and everything stays code; `[19:56]`: only on evaluation (with error, with registro, with testeo) "ahí es donde las cosas se forman"; `[00:00]` of `WhatsApp Ptt 2026-10-10 at 11.11.22.mp3`: lazy eval as the best way to define what to compute, going backward from the saved value; `[01:02]` of `WhatsApp Ptt 2026-10-10 at 11.42.15.mp3`: recomputing A (with and without error) is tolerable, "Nunca olvidarías el programa, siempre tenés que acordarte de todo"; `[00:00]` of `WhatsApp Ptt 2026-10-10 at 17.28.45.mp3`: "La ventaja de la ejecución en demanda es que me soluciona el problema del olvido."

### evaluar-modifica-la-funcion
- **What**: Since functions are values, evaluating f(x) can modify f (now you know f works), giving a tested function distinct from the naive one; or you test f first so it is already tested when built.
- **Quote**: "cuando yo hago f de x, claro, yo modifico f, o sea, porque ahora sé que f funciona, por ejemplo." (`WhatsApp Ptt 2026-10-10 at 10.12.21.mp3` `[21:08]`)
- **Course**: `[21:00]`-`[21:19]` of `WhatsApp Ptt 2026-10-10 at 10.12.21.mp3`: f(x) as a side effect on f; `[21:35]`: the easier alternative, "Yo testeo a F, entonces ahora está F testeada."

### longitud-del-programa-vs-del-calculo
- **What**: A program stays short because it is written synthetically, while a computation can grow large because it expands the search variables.
- **Quote**: "lo que es, digamos, la longitud de un programa frente a la rectitud de, digamos, un cálculo." (`WhatsApp Ptt 2026-10-10 at 11.42.15.mp3` `[01:25]`)
- **Course**: `[01:25]`-`[01:43]` of `WhatsApp Ptt 2026-10-10 at 11.42.15.mp3`: the computation expands, the program stays synthetic.

### forward-vs-backward
- **What**: Two modes of work: backward (determine what to compute from what's demanded, keeping all past history, like keeping five years of receipts) and forward (compute everything, markovian and past-less, more wasteful but reduces complexity by consumption). Both have a role.
- **Quote**: "está el método backward, y el forward." (`WhatsApp Ptt 2026-10-10 at 11.42.15.mp3` `[01:51]`)
- **Course**: `[01:58]`-`[02:30]` of `WhatsApp Ptt 2026-10-10 at 11.42.15.mp3`: forward computes unused things, only what modifies the world is seen; `[03:07]`-`[03:57]`: forward as markovian/past-less, backward must keep its whole history; `[04:03]`: "tenés que tener las dos formas de trabajar, las dos tienen un rol."

### implementaciones-como-quotient-sobre-el-predicado
- **What**: Defining types with predicates gives an equivalence relation; the implementations of a function are the quotient over the predicate of its laws, which lets you swap implementations proven equal (the basis for optimization).
- **Quote**: "Las implementaciones de una función son el quotient sobre el predicate de las leyes de esa función." (`WhatsApp Ptt 2026-10-10 at 16.49.14.mp3` `[00:47]`)
- **Course**: `[00:04]`-`[00:39]` of `WhatsApp Ptt 2026-10-10 at 16.49.14.mp3`: predicates define a subset / equivalence, members replaceable by one another; `[00:47]`: implementations as the quotient; `[01:14]`-`[01:39]`: the quotient's remainder is speed or error, the basis for optimizing.

### equivalencia-por-functor-o-modelo
- **What**: Beyond exact equality, two functions can be a functor/model of each other, living in different but equivalent (isomorphic) models (lists vs vectors, Python vs R), with a conversion cost.
- **Quote**: "vos podés tener funciones que no implementen exactamente lo mismo, pero que sean, digamos, una functor de la otra, una modelo de la otra." (`WhatsApp Ptt 2026-10-10 at 16.49.14.mp3` `[01:45]`)
- **Course**: `[01:45]`-`[02:37]` of `WhatsApp Ptt 2026-10-10 at 16.49.14.mp3`: different models, isomorphic classes, Python/R with a conversion cost.

### igualdad-de-datos-y-costo-de-representacion
- **What**: Another grade of equivalence: the same data represented differently; functions rest on a particular representation, so there is a cost to transforming data from one format to another.
- **Quote**: "la igualdad de los datos son los mismos datos pero están representados de distintas maneras" (`WhatsApp Ptt 2026-10-10 at 16.49.14.mp3` `[02:50]`)
- **Course**: `[02:47]`-`[03:18]` of `WhatsApp Ptt 2026-10-10 at 16.49.14.mp3`: same data, different representations, all modeling the same function, with a transformation cost.

### decoracion-por-demanda-contaminacion
- **What**: One single code can be run to compute the value, the value with error, the derivative, or any monad/decoration; what you compute is fixed only at the final demand (the print), which propagates backward like a poisonous stain. On demand you demand with your conditions.
- **Quote**: "sería como una especie de contaminación, vos lo tocas y es como una mancha venenosa que va para atrás" (`WhatsApp Ptt 2026-10-10 at 16.49.14.mp3` `[04:27]`)
- **Course**: `[03:30]`-`[04:15]` of `WhatsApp Ptt 2026-10-10 at 16.49.14.mp3`: the print at the end defines which branch and which calculation applies; `[05:14]`: "con cualquier monad o decoración que yo quiera poner, lo que yo llamaba el parámetro de implementación"; `[05:27]`: "Cuando vos demandás, demandás con tus condiciones"; `[00:47]` of `WhatsApp Ptt 2026-10-10 at 17.28.45.mp3`: every variable can carry an infinite decoration requested on demand; `[01:25]` of `WhatsApp Ptt 2026-10-10 at 17.28.45.mp3`: "la demanda final es la que te soluciona todo el código para adelante, para atrás."
- **Open**: how to attach error to an input that entered as a plain real with no error (`[05:54]`-`[06:11]` of `16.49.14`); and whether these decorations are forward or backward, to be discussed with the AI (`[06:51]`-`[07:06]` of `16.49.14`).

### funciones-como-valores-captura-de-dependencias
- **What**: If functions are values, they can change, so a function that uses other functions must capture them somehow: either parametrize everything (the used functions are input parameters) or have a default that can be swapped (e.g. which FFT implementation).
- **Quote**: "cuando uno ya considera que las funciones son variables, o sea, son valores, entonces los valores pueden cambiar." (`WhatsApp Ptt 2026-10-10 at 17.00.40.mp3` `[00:00]`)
- **Course**: `[00:13]`-`[00:56]` of `WhatsApp Ptt 2026-10-10 at 17.00.40.mp3`: parametrize all used functions as inputs; `[00:58]`-`[01:42]`: or a default value you can change (FFTW/GSL implementations); `[01:49]`: asks how this is normally done, since functions are first-class.

### modulos-como-teorias-matematicas
- **What**: Modules represent mathematical theories (linear algebra, reals, Fourier transforms), carrying types and functions with their laws, defined without value, with implementations that are generic where possible.
- **Quote**: "los módulos representarían justamente teorías matemáticas, como que se llama algebra lineal o reales o, no sé, transformadas de Fourier" (`WhatsApp Ptt 2026-10-10 at 17.25.23.mp3` `[00:00]`)
- **Course**: `[00:00]`-`[00:46]` of `WhatsApp Ptt 2026-10-10 at 17.25.23.mp3`: theory with types and functions, all with laws, defined without value, then generic implementations.

### el-modulo-define-la-sintaxis
- **What**: A module's type fixes a single syntax: the names of its functions and types and how they are represented, like Python/R libraries but with all their laws, with dotted names.
- **Quote**: "los módulos tendrían una única sintaxis que está dada por justamente cuando vos definís el tipo del módulo" (`WhatsApp Ptt 2026-10-10 at 17.25.23.mp3` `[00:49]`)
- **Course**: `[00:49]`-`[01:02]` of `WhatsApp Ptt 2026-10-10 at 17.25.23.mp3`: the module type defines function and type names and representation; `[01:21]`-`[01:44]`: dotted names like Python's np., libraries but with laws.

### luthier-absorbe-librerias-reescribiendo-sus-leyes
- **What**: An immediate application: have the AI take a Python/R library and generate Luthier code that writes each function with all the laws it satisfies, a way to suck in other languages' implementations while understanding what each does; writing the tests reveals bad design.
- **Quote**: "el primer trabajo que podría hacer Luthier es agarrar y decirle a la IA, bueno, ahora vos agarrame toda esta librería de Python" (`WhatsApp Ptt 2026-10-10 at 17.25.23.mp3` `[01:46]`)
- **Course**: `[01:46]`-`[02:17]` of `WhatsApp Ptt 2026-10-10 at 17.25.23.mp3`: generate a Luthier with the laws of a library's functions; `[02:21]`-`[03:03]`: pedagogical, understand what libraries do; `[03:23]`: pivot_wide/pivot_long "y una no es la inversa de la otra y tendrían que ser una inversa de la otra," revealing bad design.

### modulo-teorico-vs-modulo-de-implementacion
- **What**: In general you write a theoretical module and the implementation module(s), the latter possibly in Python, in R, and so on, with conversions between them.
- **Quote**: "vos vas a hacer un módulo teórico y el módulo de la implementación" (`WhatsApp Ptt 2026-10-10 at 17.25.23.mp3` `[04:05]`)
- **Course**: `[04:03]`-`[04:22]` of `WhatsApp Ptt 2026-10-10 at 17.25.23.mp3`: theoretical module plus implementation modules in different languages.

### interprete-tabla-de-implementaciones
- **What**: The Luthier interpreter: inspired by his own C++ DSL in MacroDR (virtual Compile classes), it would keep a table of identifiers with the implementations of each function; in Luthier the implementation is static Luthier code, and you need to know the output type.
- **Quote**: "lo que habría que tener es, digamos, una tabla de identificadores con las implementaciones de las distintas funciones" (`WhatsApp Ptt 2026-10-10 at 17.25.23.mp3` `[05:10]`)
- **Course**: `[04:30]`-`[05:10]` of `WhatsApp Ptt 2026-10-10 at 17.25.23.mp3`: inspiration from the MacroDR DSL with virtual classes; `[05:30]`-`[05:46]`: the implementation is the static Luthier code, you need the output type.

### tipo-de-salida-polimorfico-por-demanda
- **What**: A function can have multiple output types (sin as a real, a real in [-1,1], etc.), with the output type fixed by the required input type: a polymorphism in both the function and its return, possible under on-demand execution.
- **Quote**: "Una función podría tener multiplicidad de tipos de salida y que el tipo de salida queda definido por el tipo de entrada que es requerido." (`WhatsApp Ptt 2026-10-10 at 17.25.23.mp3` `[07:20]`)
- **Course**: `[05:49]`-`[06:21]` of `WhatsApp Ptt 2026-10-10 at 17.25.23.mp3`: sin has several result types; `[06:38]`: "Hacemos implementación por demanda"; `[07:20]`-`[07:53]`: output type set by required input type, possible with on-demand execution.

### external-como-funcion-de-luthier
- **What**: Turn external into a Luthier function that takes, say, a file and returns a maybe function: it finds the function (written in another language), stores it in the registry under its name ready to run, and must declare which language it is in.
- **Quote**: "Una tentación que yo tenía es convertir external en una función de Python de alguna manera," (`WhatsApp Ptt 2026-10-10 at 17.41.53.mp3` `[00:00]`)
- **Course**: `[00:08]`-`[01:01]` of `WhatsApp Ptt 2026-10-10 at 17.41.53.mp3`: external fetches the foreign function and stores it in the registry under its name; `[01:48]`: "el external tendría que decir en qué lenguaje está," better declared than guessed so there are no surprises.

### un-environment-por-lenguaje
- **What**: The interpreter would hold a registry of variables and functions, one environment per language in use, running several languages that communicate with each other.
- **Quote**: "tendríamos una especie de registro de variables y de funciones, un environment por cada uno de los lenguajes que usemos." (`WhatsApp Ptt 2026-10-10 at 17.41.53.mp3` `[02:16]`)
- **Course**: `[01:05]`-`[01:39]` of `WhatsApp Ptt 2026-10-10 at 17.41.53.mp3`: the interpreter has beds ("camitas") to run Python, R and others, with inter-program communication; `[02:16]`-`[02:28]`: one environment per language, several languages communicating.

## Notes

- `WhatsApp Ptt 2026-10-10 at 10.12.35.mp3`: "Un poco.", a fragment with no idea about Luthier.
