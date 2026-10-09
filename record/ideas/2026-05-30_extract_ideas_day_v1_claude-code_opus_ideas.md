---
date: 2026-05-30
notes:
  - audio: WhatsApp Ptt 2026-05-30 at 18.01.53.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.01.53.md
    duration: ~05:56
    sha256: 7e30c355991d3b4aa8abde7a7075998309ea2068333226e03d7670cae02cfca9
  - audio: WhatsApp Ptt 2026-05-30 at 18.02.45.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.02.45.md
    duration: ~00:24
    sha256: 109e2d7731198a7adf1d351902e506ce4947ce698a400a9e281b91291cb35462
  - audio: WhatsApp Ptt 2026-05-30 at 18.05.22.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.05.22.md
    duration: ~02:28
    sha256: 2750b28342e33061501956b5929983710701ac9d50e1e1279ddd42d5a1112547
  - audio: WhatsApp Ptt 2026-05-30 at 18.07.21.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.07.21.md
    duration: ~01:29
    sha256: 21e46f8376b1012e5d547b87b408189f851c1ff06d864195b2ddfd88f2dae203
  - audio: WhatsApp Ptt 2026-05-30 at 18.09.57.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.09.57.md
    duration: ~02:31
    sha256: 0fd2da012f63ed283e2f9f488a17b26448b5fbc130c8a5c33796ccc5f109f30a
  - audio: WhatsApp Ptt 2026-05-30 at 18.11.30.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.11.30.md
    duration: ~01:12
    sha256: 9cd3881458e4309b14f6dcd9139f6d5990ec0f253894921eaea23e5b03331fce
  - audio: WhatsApp Ptt 2026-05-30 at 18.12.54.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.12.54.md
    duration: ~01:05
    sha256: a749a6982c88bc335742f40520e3bc0f20e7f5f1f23b5d220fa3dae2a6618727
  - audio: WhatsApp Ptt 2026-05-30 at 18.15.07.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.15.07.md
    duration: ~01:47
    sha256: 7bf082e3f24b1c703cd691c64a6c77a0eeb26a273c8762ea5f3c68d7b7b0d336
  - audio: WhatsApp Ptt 2026-05-30 at 18.16.35.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.16.35.md
    duration: ~01:27
    sha256: 4dbc58746604b55d38e98f261aba9be20416813a3328a7c08918c91e4c7aa9d3
  - audio: WhatsApp Ptt 2026-05-30 at 18.17.51.mp3
    transcript: WhatsApp Ptt 2026-05-30 at 18.17.51.md
    duration: ~00:49
    sha256: 75237e816fe3fdeba9c40dfaf302e5d1b2c3bb979d86b6f7463dccc54f947ae2
ideas: 18
quotes_found: 18/18
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### ejecucion-vs-explicitacion
- **What**: Luthier does execute (it is a program), but the emphasis is not on execution; its first stage is a language for describing the problem, the functions and the conditions under which they work.
- **Quote**: "la idea es que la primera etapa de Luthier tiene que ser como una especie de lenguaje de descripción, descripción del problema, descripción de las funciones, descripción de las condiciones de las funciones para que las funciones funcionen" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:24]`)
- **Course**: `[00:48]` of `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3`: answering the mentor's question of whether Luthier executes, says yes obviously, it is a program; `[01:11]` same note: shifts the weight to explicitation, the description of the problem; `[01:47]` same note: frames it against math, which does not execute, only verifies equivalences, so execution in Luthier would be that verification.
- **Open**: he affirms execution occurs "claramente" but leaves what exactly it is beyond verification of equivalences unsettled.

### matematica-no-ejecuta-verifica-equivalencias
- **What**: an analogy: math does not execute, all it does is verify equivalences; execution in Luthier is that verification of equivalences.
- **Quote**: "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verificación de equivalencias" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:47]`)
- **Course**: `[01:47]` of `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3`: appears as the ground for putting the emphasis on explicitation rather than execution.

### niveles-de-equivalencia
- **What**: one of Luthier's fundamental ideas is to express the different levels of equivalence (same information, isomorphic, exactly equal, same memory location), each depending on a different equivalence functor; and how distinct forms express the same thing rather than distinct things.
- **Quote**: "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[02:56]`)
- **Course**: `[02:16]` of `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3`: starts with how distinct forms express the same thing and not distinct things; `[02:35]` same note: the levels depend on a different equivalence functor, gives examples (same information, isomorphic, exactly equal, same memory); `[03:12]` same note: extends to equivalences of functions, from which the non-equivalent (decorations, efficiency, cost) can be seen; equivalence as a way of classifying.

### core-minimo-y-delegacion-a-otros-lenguajes
- **What**: there should be a clear core of Luthier in which all its operations execute, with only a few implemented in C or similar so it runs; and a facility to run other programs and compilers, so functions can be mapped and compiled to C, C++, Java; Luthier does not do the translation directly but gives the tools for others to extend it.
- **Quote**: "la idea no es hacerlo directamente, sino dar las facilidades para que eso sea posible" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[05:49]`)
- **Course**: `[03:48]` of `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3`: a seed idea of a core where all Luthier operations execute, only a few implemented in C; `[04:07]` same note: a library/facility, itself implemented in some language, to run other programs and compilers; `[04:55]` same note: describing equivalences and functions lets you map/compile functions to C, C++, Java; `[05:30]` same note: you don't do it directly, you give tools so others extend the translation to other languages.

### delegacion-facil-modelo-modelica
- **What**: what he wanted to say is that delegation should be easy; he traces the idea to Modelica, a kind of specification of a program without implementation.
- **Quote**: "Yo un poco estaba pensando en el modelo Modélica, que no sé exactamente cómo es, pero como que es una especie de especificación de un programa sin implementación. Creo que de ahí viene esta idea." (`WhatsApp Ptt 2026-05-30 at 18.02.45.mp3` `[00:10]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.02.45.mp3`: states the goal of easy delegation and attributes it to Modelica, admitting he doesn't know exactly how Modelica works.

### hott-sin-concepto-de-programa
- **What**: a defect of Homotopy Type Theory is that it has no theory of complete programs; it conceptualizes function and types but not a set of its expressions, which would be a program.
- **Quote**: "Homo etopitae teori no conceptualiza, digamos, un conjunto de expresiones de Homo etopitae teori, o sea, lo que sería un programa, no hay un concepto, hay un concepto de función, de tipos, pero de programa no me queda muy claro que esté, eso es uno de los defectos" (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[00:41]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3`: recovers an incomplete phrase about HoTT; `[00:24]` same note: names the missing theory of complete programs as a defect.

### olvido-en-hott
- **What**: forgetting is present in HoTT, in the sense that a type forgets parts of the type; he thinks it is there as a concept.
- **Quote**: "el tema del olvido está, sí está presente en Ométropeuta y Tierra y en el santuido de que vos, un tipo, olvidás partes del tipo. Eso sí, creo que está como concepto" (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:05]`)
- **Course**: `[01:05]` of `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3`: states forgetting is present in HoTT as a concept, hedged with "creo que".
- **Open**: he is unsure ("creo que está como concepto").

### probabilidades-y-tipos-a-la-par
- **What**: HoTT does not work on probabilities, but they could be built within it; his idea is that probabilities and types go almost together, the equivalences being probabilistic, with HoTT giving the universe/points where the probabilities apply.
- **Quote**: "la idea mía es de alguna manera que las probabilidades y los tipos vayan casi a la par. O sea que las equivialencias sean de alguna manera probabilísticas." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:40]`)
- **Course**: `[01:32]` of `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3`: HoTT does not work on probabilities but they could be built inside it; `[01:40]` same note: probabilities and types go almost together, equivalences become probabilistic; `[02:02]` same note: the only way he can think it is HoTT giving the universe/points/sets where the probabilities apply.
- **Open**: he calls it "un poco difícil de pensar" and offers only one tentative way to conceive it.

### minimalismo-fundante-maximalismo-construido
- **What**: against the mentor's charge of a declared minimalism and a real maximalism, he says there is no contradiction: the minimalism is in the founding components, from which a huge edifice is built; reduce everything to few minimal elements while keeping the complex concepts.
- **Quote**: "El minimalismo está en los componentes fundantes y después a partir de esos componentes fundantes vos construís un edificio enorme." (`WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:12]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.07.21.mp3`: takes up the mentor's "minimalismo declarado y maximalismo real" and denies a contradiction; `[00:25]` same note: analogy to category theory, defining functors from arrows, from basal elements; `[00:40]` same note: dependent types as a basic initial concept, wonders whether one could start only from the identity of some equivalence principle; `[01:04]` same note: reduce to a minimum but keep the complex concepts, based on few minimal elements.
- **Open**: whether one could start with only the identity of an equivalence principle is left as "puede ser, no sé".

### conmutatividad-de-statements-y-temporalidad-causal
- **What**: statements commute; temporality is not primitive but reconstructed from causality through type dependence, Prolog-style: what happens tomorrow depends on what happened today.
- **Quote**: "tiene que haber conmutatividad de statements, lo que pasa es que la temporalidad se da a lo PERL a partir de la dependencia de tipos." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:00]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.09.57.mp3`: resolves commutativity of statements, temporality from type dependence; `[00:30]` same note: causal dependence, temporality reconstructed from causality; `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3`: reaffirms there is commutativity and inclines to the DAG model.

### no-ejecutar-hasta-definido
- **What**: a principle of the execution law: you don't execute code until it is defined; undefined "dead code" can sit there without bothering anyone, and what you execute are the contradictions, or whatever is there.
- **Quote**: "vos no ejecutás el código hasta que no está definido. Entonces es como que, digamos, vos podés tener un montón de código muerto que no jode a nadie porque no está completamente definido." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:53]`)
- **Course**: `[00:46]` of `WhatsApp Ptt 2026-05-30 at 18.09.57.mp3`: offers it as a principle of the execution law just occurred to him; `[01:27]` same note: if not defined it doesn't matter, what you execute are the contradictions, "ejecutás lo que hay", noting it needs definition.
- **Open**: he says "Habría que definir un poco eso"; what exactly gets executed when things are undefined is unsettled.

### muchas-operaciones-sobre-el-codigo-de-luthier
- **What**: Luthier code is not just compiled and run; you can do many operations on it, verify it, compile it, run it; more complexity but more expressivity.
- **Quote**: "al código de Luthier vos podés hacerle muchas cosas. No es que vos lo compilás y lo corres nada más." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[01:56]`)
- **Course**: `[01:36]` of `WhatsApp Ptt 2026-05-30 at 18.09.57.mp3`: with Luthier code you can verify, compile, run, etc.; `[02:05]` same note: frames it as a principle of greater complexity but greater expressivity, many operations over the code.

### programa-funcion-vs-interaccion
- **What**: an important design question is whether a Luthier program is like a function (input to output) or has an interaction function; he leans to the function model first for simplicity, extendable later.
- **Quote**: "pensar si es un programa que es tipo una función, como si fuera una función que vos le das un input y te tira un output, o si tiene una función de interacción." (`WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:00]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.11.30.mp3`: poses the function-vs-interaction question; `[00:27]` same note: leans to the function model first, extend to the other later.
- **Open**: "Eso no sé cómo se define ni nada"; left undecided.

### luthier-opera-sobre-si-mismo
- **What**: if a Luthier program is a function, one thing it can do is work on another Luthier program; whether it can work on itself is normally impossible, but since it is our own universe it could be allowed.
- **Quote**: "dado que es nuestro propio universo, podríamos hacer que Luthier trabaje sobre sí mismo. Es una pregunta interesante." (`WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:54]`)
- **Course**: `[00:38]` of `WhatsApp Ptt 2026-05-30 at 18.11.30.mp3`: a Luthier program working on another Luthier program; `[00:50]` same note: whether it can work on itself, normally no, but as our own universe it could; `[00:19]` of `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3`: adds that a DAG does not take everything, you can have a DAG operating on DAGs operating on programs, and something operates on that static DAG and transforms it into something else with instructions of itself.
- **Open**: left as "una pregunta interesante", not settled.

### programa-como-dag-estatico
- **What**: taking the DAG model for commutativity: statically a Luthier program is a DAG; though something can operate on a DAG that operates on DAGs over programs, you can still take it as a static DAG.
- **Quote**: "estáticamente, un programa así sería como un DAG." (`WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:57]`)
- **Course**: `[00:07]` of `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3`: inclines to the DAG model for commutativity; `[00:19]` same note: notes a DAG doesn't capture everything, there are DAGs operating on DAGs over programs, but it is static; `[00:57]` same note: concludes statically a program is a DAG.

### hott-universo-de-caminos-y-filtrado-de-particulas
- **What**: HoTT as a continuous field of exploration giving a larger universe of possible paths; computationally it explodes exponentially, so you do particle filtering, running several programs in parallel with stochastic programming, replicating a "Hot basin".
- **Quote**: "vos corres varios programas en paralelos y haces una programación estocástica que van por distintos lados y entonces de esa manera estás replicando un hot basin." (`WhatsApp Ptt 2026-05-30 at 18.15.07.mp3` `[00:54]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.15.07.mp3`: HoTT as a continuous field of exploration giving a larger universe of possible paths; `[00:43]` same note: it explodes exponentially, so particle filtering with parallel programs and stochastic programming; `[01:23]` same note: distinguishes very broad priors from the case of measurement errors that propagate, says he has to work it out well.
- **Open**: "es todo un tema que sí tengo que trabajar bien"; the model is tentative.

### functores-de-olvido-y-sintesis
- **What**: forgetful functors have a whole theory to work out; the generalization of databases relates to them, and a mean is a kind of forgetful functor; summarizing/synthesizing information is the key to everything, and the first step is to express it well, then express hits and errors and choose the hits.
- **Quote**: "Una media es como una especie de funtor de olvido, si se quiere." (`WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:40]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3`: forgetful functors as a theory to develop; `[00:27]` same note: the generalization of databases relates to forgetful functors, or to means; `[00:40]` same note: a mean is a kind of forgetful functor, a way of summarizing information; `[00:56]` same note: synthesis is the key to everything; first express it well, then express hits and errors and choose the hits.

### lapiz-papel-y-base-de-datos-dos-capas
- **What**: against the mentor's claim that a pencil-and-paper language and one needing a database of empirical runs are opposite philosophies, he disagrees: you can express it with pencil and paper and then consult the database (or have someone tell you the result); they are two layers, two moments, not a concession of one to the other.
- **Quote**: "La idea básica es que vos puedas expresar las ideas con lápiz y papel y después es que vayas." (`WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:38]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-05-30 at 18.17.51.mp3`: quotes the mentor's opposition and says he disagrees; `[00:14]` same note: you can execute with pencil and paper and consult a database carefully, or have someone report the result; `[00:30]` same note: they are two layers, two moments, neither a concession, the basic idea being pencil-and-paper expression first.

## Notes

none
