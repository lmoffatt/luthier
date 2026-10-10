---
date: 2026-10-08
notes:
  - audio: WhatsApp Ptt 2026-10-08 at 18.10.00.mp3
    transcript: WhatsApp Ptt 2026-10-08 at 18.10.00.md
    duration: ~33:16
    sha256: 7a837dadde5633dc6f9821c390c9fd575b5ab4dc091eedf35187787e8dfb6340
  - audio: WhatsApp Ptt 2026-10-08 at 18.37.46.mp3
    transcript: WhatsApp Ptt 2026-10-08 at 18.37.46.md
    duration: ~01:31
    sha256: 6d7bb2e33f8fac04d6fdae77d33298c26b3eb25bf7d2d397da54ddacb7a75e9c
  - audio: WhatsApp Ptt 2026-10-08 at 18.41.38.mp3
    transcript: WhatsApp Ptt 2026-10-08 at 18.41.38.md
    duration: ~00:10
    sha256: 28704513d9a7d798e3056ffc1f63730a670bbc0231f7d2a3d033e39c2650ce1b
ideas: 23
quotes_found: 23/23 (match: words)
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### semantica-base-ccc-mas-dependientes-mas-clasificador
- **What**: The basic way of writing Luthier would be a Cartesian closed category (sums, products, exponentials of types) plus dependent types, plus a kind of object classifier: predicates about types that are the laws, the names.
- **Quote**: "que usaría, bueno, lo que sería Cartesian Close Categories, más, o sea, que serían sumas de tipos, productos de tipos y exponencial de tipos. Y luego tendría las, ¿cómo se llama? Los tipos dependientes, ¿no?" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[00:27]`)
- **Course**: `[00:27]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: he states he is satisfied with the semantics, names CCC with the three type operations; `[00:42]` adds dependent types; `[00:57]` adds the object classifier as predicates about types, which are the laws and the names.

### pertenencia-de-un-valor-a-un-tipo
- **What**: The important thing for Luthier is how one knows a value belongs to a type: either by construction (given) or by hypothesis, which is like a construction by value that can fail.
- **Quote**: "lo importante para Luthier es, bueno, cómo sé que un tipo, un valor, perdón, pertenece a un tipo, ¿no? que puede ser por construcción, cuyo caso está dado, digamos, o por hipótesis," (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[01:13]`)
- **Course**: `[01:13]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: distinguishes membership by construction vs by hypothesis; `[01:42]` hypothesis as construction by value that can fail; `[01:51]` for finite values you just check the laws hold.

### certificacion-de-funciones-es-probabilistica
- **What**: For functions you cannot test membership exhaustively, so you test on a sample; the result is not a certification but a probability of a certain success.
- **Quote**: "Pero el problema es cuando los valores son fusiones. En ese caso, digamos, las funciones no son, podés probarlas extensivamente, Entonces, lo que haces es la probás en una muestra." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[02:04]`)
- **Course**: `[02:04]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: functions can't be tested exhaustively, so test on a sample; `[02:30]` it would not be a certification but a probability of success; `[30:46]` he returns to it: with this "bayesian" logic any computation in Luthier carries a posterior of how sure you are.

### modificador-de-tipos-por-uso-costo-y-probabilidad
- **What**: Beyond laws holding, a type could be parametrized by its conditions of use and environment: a cost of failure that varies by situation, and a probability (prior) of each parameter combination occurring.
- **Quote**: "la idea sería que también se parametrice con una especie de uso, Es decir, qué pasa un costo de si la función falla, por ejemplo, y con, digamos, falla de acuerdo a distintos, como se dice, situaciones." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[03:32]`)
- **Course**: `[02:50]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: a modifier of types where laws hold within a numeric range; `[03:32]` parametrize also by use and cost of failure, which depends on the situation; `[04:15]` you would sample where cost is higher, or where failure is more probable; `[06:18]` two functions: a prior of parameter combinations and a cost of failure; `[07:20]` cost depends on the degree of failure, not all errors are equal.
- **Open**: whether you search where failure is costly, where it is probable, or a combination; he leaves it as hypothetical situations "que uno no tiene por qué solucionar ahora", the point is being able to write them.

### expectativa-de-perdida-como-caracterizacion-de-la-funcion
- **What**: What is left of a function is an expected loss (plus possibly other statistics), a posterior characterization of the implementation that must be processable.
- **Quote**: "entonces vos al final lo que te queda de la función sería una expectativa de pérdidas ponerle o algo así de la función que te haría como una especie de parámetro" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[08:16]`)
- **Course**: `[07:50]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: think of it as a type with a test, a parameter generator and a cost; `[08:16]` the result is an expected loss; `[08:41]` the posterior / characterization of the implementation should be processable.

### costo-de-computo-como-eje-de-eleccion
- **What**: The characterization must also carry compute time, not only error, so one can choose a faster-and-worse or slower-and-safer function; all these functions are values of the same function type solving the same problem.
- **Quote**: "no solamente el error, sino el tiempo de cómputo, porque vos podés elegir una función que sea más rápida y más chota, o más lenta y más segura" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[09:15]`)
- **Course**: `[09:15]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: adds compute time; `[09:34]` all these functions solve the same problem, they are values of the same function type.

### mundo-exterior-como-archivos-memoria-recursos-procesadores
- **What**: What is outside Luthier: files (executables, Python code, data, plots, even sensors) are a large part of the exterior; plus mutable memory, resources and processors. Open whether there is any abstraction for interacting that is not a file.
- **Quote**: "los archivos creo que es una gran parte del mundo exterior no sé si hay otras cosas vos podrías tener sensores pero también son files yo no sé si vos tenés alguna abstracción que no sea un file para interactuar esa es una buena pregunta para hacerle ahí" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[10:38]`)
- **Course**: `[09:57]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: the other aspect is what is external to Luthier; `[10:09]` files as the way to think about it; `[10:38]` files as a large part of the exterior, question whether anything isn't a file; `[11:13]` adds mutable memory, resources, processors as the ingredients of computation.
- **Open**: "no sé si hay algo más esta habría que preguntarle"; whether there is a non-file abstraction for interacting with the outside.

### certificar-que-la-funcion-cumple-lo-que-dice
- **What**: One of the great ideas of Luthier: write what a function does with postconditions and laws, then certify those are met.
- **Quote**: "una de las grandes ideas de de Luthier es que es vos certifiques que determinada función cumple lo que dice, o sea poder escribir que es lo que la función hace con pos condiciones, con leyes y después certificar que esas cosas se cumplen, eso es." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[11:59]`)
- **Course**: `[11:48]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: he returns from the digression to say this is one of the great ideas; `[12:24]` and separately there is executing the programs, certifications occur in time.

### declarar-y-luego-definir-un-tipo
- **What**: A type is first declared (named, not yet defined because its constraints aren't all stated) and then defined; the declaration-before-definition is needed to define types recursively against each other.
- **Quote**: "vos tenés un tipo, por ejemplo vos podés enunciar un tipo, lo declarás, todavía no está definido porque todavía no declaraste todos los constraints que tiene" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[12:34]`)
- **Course**: `[12:34]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: you declare a type before it is defined; `[12:47]` this is needed to define a type recursively against another; `[13:09]` you declare types and then define them.

### no-hay-valor-sin-definicion-del-tipo
- **What**: A law: you cannot give a value to a type that has no definition; and a type's definition is not just "function from reals to reals" but the properties that function has.
- **Quote**: "vos no le podés dar un valor a un tipo que no tiene una definición. O sea, el tipo tiene que tener una definición." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[13:25]`)
- **Course**: `[13:16]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: giving a value to a type; `[13:25]` the law that the type must have a definition; `[13:37]` the definition must state properties, not just the signature; `[14:10]` a function type need not be univocal, there can be many function types you invent.

### leyes-de-costo-en-vez-de-leyes-booleanas
- **What**: Laws are functions from a type to the booleans; one could extend them to go to a cost instead, graded laws like a generalized unnormalized likelihood, asking not whether a value complies but how much it costs.
- **Quote**: "uno podría extender este concepto y que sean las leyes vayan de no a un boolean sino a un costo" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[14:47]`)
- **Course**: `[14:30]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: laws are a function from a type to the booleans; `[14:47]` extend them to a cost; `[15:16]` graded laws, a likelihood / generalized unnormalized probability; `[16:12]` better to think of them as unbounded costs than values of anything; `[17:11]` for a value under such a law the question is "cuánto me sale esta ley", how much it costs, not comply/not.
- **Open**: whether costs should be positive or can take any value; he notes "si pueden valer cualquier cosa entonces ahí un poco se complica todo".

### parte-declarativa-y-parte-ejecutiva
- **What**: Luthier has a declarative part (types that follow laws) and an executive part (running commands: read a file, execute a function); later named Luthier declarativo (types) vs Luthier ejecutivo (values).
- **Quote**: "hay una parte declarativa y después una parte ejecutiva. Entonces la parte ejecutiva claramente hay que tener una especie de run, o sea una especie de correme estos comandos, o sea leme este file, ejecutame esta función, etc." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[17:58]`)
- **Course**: `[17:58]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: declarative vs executive, the executive needs a run; `[00:03]` of `WhatsApp Ptt 2026-10-08 at 18.37.46.mp3`: names them, types are Luthier declarativo that follows laws, values are Luthier ejecutivo; `[00:23]` the executive can be internal to Luthier or external.

### ejecucion-como-cambio-de-estado-del-programa-y-del-universo
- **What**: Running a function is modeled as changing state: the program's states and the universe's states (a written file, a printed line, a sent message); changes in the universe also follow rules.
- **Quote**: "vos lo podés modelar como algo que cambia. ¿Qué cambia? El universo, es decir, cambia los estados del programa y los estados del universo, ¿no es cierto?" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[18:26]`)
- **Course**: `[18:26]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: running changes program and universe states; `[18:59]` universe changes are inferred (a file written, a message sent); `[19:19]` universe state changes also follow rules.

### lenguaje-agnostico-entre-estado-interno-y-del-universo
- **What**: The language should not distinguish types that speak of the program's internal state from those that speak of the universe's state; what matters is which actions depend on which, an order of execution given by state dependency.
- **Quote**: "En principio, el programa tendría que ser agnóstico de eso. No veo por qué habría una distinción en la lógica de una cosa y de la otra." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[19:42]`)
- **Course**: `[19:26]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: how do you distinguish internal-state types from universe-state types; `[19:42]` the language should be agnostic; `[20:02]` what matters is which actions depend on which, an order from state dependency, a graph.

### do-de-haskell-como-dependencia-de-estados
- **What**: Haskell's `do` sequencing (one thing then another) can be simulated as a data dependency: if an output needs an input that doesn't exist yet, you can't proceed; so `do` may not be strictly necessary.
- **Quote**: "ese dude que usan Haskell no sé si sería estrictamente necesario o no," (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[21:23]`)
- **Course**: `[20:31]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: Haskell's do, one thing then another; `[20:54]` simulate it as a dependency, input-output; `[21:23]` so do may not be strictly necessary.
- **Open**: whether the `do` sequencing is strictly necessary is left open.

### interprete-de-luthier-escrito-en-luthier
- **What**: He would like the implementation of the Luthier interpreter to be written in Luthier itself, with its environment of registered names, parsing a string expression into Luthier code and then evaluating it.
- **Quote**: "a mí me gustaría que lo que sea la implementación del intérprete de Luthier sea escrito en Luthier." (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[21:33]`)
- **Course**: `[21:33]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: he states the wish; `[21:55]` an interpreter with a register of names, an environment; `[22:14]` evaluating transforms a string expression into Luthier code and then executes it (he recalls two executions).

### cuando-y-como-evaluar-una-expresion
- **What**: An open question of evaluation strategy: for `A = 2+2`, do you store `A` as `2+2` or as `4`; and several ways to consume symbols (eager, consuming memory; or keeping the tree; or storing the string to recompute).
- **Quote**: "A es igual a 2 más 2, ¿qué haces con eso? ¿Lo guardás como A2 más 2 o aplicás o le asignás 2 más 2, el valor 4 y A pasa a valer 4 ¿cuánto vale A? ¿A vale 2 más 2 o A vale 4?" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[23:02]`)
- **Course**: `[22:48]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: whether evaluation is eager; `[23:02]` the A = 2+2 problem; `[23:38]` one strategy consumes symbols as it reads with little memory; `[24:17]` another keeps 2, +, 2 in memory and executes later; `[24:44]` another keeps the expression (a+b) and substitutes values at execution; `[25:09]` keeping the intermediate lets you compute different things (e.g. A with an error) from the same expression; `[25:35]` the aim is at least to be able to write all these ways.
- **Open**: whether an intermediate representation must be stored at all, since the expression kept as a string can just be recomputed.

### representar-los-pasos-de-evaluacion-en-luthier
- **What**: How to represent evaluation steps in Luthier: the states of memory (2; 2+; 2+2; 4), possibly with pointers to a partially applied function, with syntax/type errors caught along the way (arcsin of a string, a value out of range).
- **Quote**: "como eso vos lo representas en luthier, ¿no? más dos, qué sé yo sería como tenés un dos después tenés un dos más después tenés un dos más dos después tenés un cuatro, ¿no? serían, digamos, los pasos el estado de la memoria" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[26:18]`)
- **Course**: `[26:18]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: representing the steps as states of memory; `[26:57]` a step can be `2` plus the symbol `+`, or an already-built partial function filled with the 2; `[27:42]` type/range errors caught (arcsin out of range, arcsin of a string); `[28:12]` he recalls he developed this in his C++ interpreter (macro IR, Kimball) with virtual classes.

### leyes-de-los-pasos-de-interpretacion-apply-y-reduce
- **What**: Rather than reproducing compilation stages, Luthier should carry the laws of each step of interpretation; with apply and reduce he thinks he could have almost all of it, like a kind of HGER, and the laws should be written in Luthier so one can check they hold.
- **Quote**: "tendría que tener las leyes de cada uno de los pasos de la interpretación. O sea, el reduce, que creo que con el apply y reduce yo podría tener eso casi todo hecho" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[29:39]`)
- **Course**: `[28:58]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: does it make sense to interpret and generate the code in Luthier (Python does it now); `[29:39]` have the laws of each interpretation step; `[29:44]` apply and reduce give almost all of it; `[30:16]` the laws of that should be written in Luthier so one can examine that the precepts of Luthier hold.

### posterior-de-certeza-y-acumulacion-de-evidencia
- **What**: With this bayesian logic, any computation in Luthier carries a posterior of how sure you are; you can combine evidence from different programs running the same function and refine the certainty about it.
- **Quote**: "cualquier cálculo que hagas en Luthier va a tener un posterior de que tan seguro estás de ese cálculo ¿no? eso es interesante" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[30:46]`)
- **Course**: `[30:46]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: every computation carries a posterior; `[31:08]` unite different evidence, different programs running the same function, to refine the certainty.

### guardar-testigos-caros-y-por-informacion
- **What**: Since these are expensive functions, you keep the witness that a function worked or failed; cheap statistics can be aggregated, and you keep especially the values with much information, those far from the prior (unexpected); all this is parafernalia layered on top, run only at some moments.
- **Quote**: "vos vas a querer guardar el testigo de que la función funcionó, de que la función falló" (`WhatsApp Ptt 2026-10-08 at 18.10.00.mp3` `[31:45]`)
- **Course**: `[31:38]` of `WhatsApp Ptt 2026-10-08 at 18.10.00.mp3`: expensive functions, keep the witness of success/failure; `[32:06]` keep the values with much information; `[32:12]` much information means unexpected values; `[32:23]` with a prior of a function's possible values, keep what falls far from the prior; `[32:39]` it makes computation much more expensive, so test only occasionally; `[32:51]` all this is parafernalia on top, to be run at chosen moments, not always.

### modos-de-ejecucion-de-un-programa
- **What**: You would define a program and say execute/eval, with different modified evaluations: with test, with extensive test, copying everything that happens; the nice thing about such a language is having different execution modes.
- **Quote**: "hay distintos modos de ejecución que sería lo lindo de tener un lenguaje así." (`WhatsApp Ptt 2026-10-08 at 18.37.46.mp3` `[01:23]`)
- **Course**: `[00:53]` of `WhatsApp Ptt 2026-10-08 at 18.37.46.mp3`: you need to write executive code; `[01:01]` define a program and say execute or eval; `[01:14]` evaluation with test, with extensive test, copying everything; `[01:23]` different execution modes.

### luthier-declarativo-de-la-implementacion
- **What**: What is missing is a Luthier declarativo of the implementation: of how Luthier code transforms into execution code, and of how to write executive code in Luthier. The culmination would be writing Luthier's specifications in Luthier itself.
- **Quote**: "lo que faltaría hacer es hacer un Luthier declarativo de la implementación, es decir, de cómo se transforma el código Luthier en código de ejecución." (`WhatsApp Ptt 2026-10-08 at 18.37.46.mp3` `[00:35]`)
- **Course**: `[00:35]` of `WhatsApp Ptt 2026-10-08 at 18.37.46.mp3`: a Luthier declarativo of the implementation; `[00:47]` and how to write executive code in Luthier; `[00:00]` of `WhatsApp Ptt 2026-10-08 at 18.41.38.mp3`: "la idea es si se puede escribir las especificaciones de Luthier en Luthier. Eso sería lo máximo, ¿no?"

## Notes

none
