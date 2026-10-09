---
source: gemini
key: gemini::20260529T1400
title: "Bueno, vamos a soñar un poco. Inventar un lenguaje es como inventar un universo. O inventa"
started: 2026-05-29T17:00:30Z
ended: 2026-05-29T18:21:51Z
thread: 2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md
thread_sha256: a1e40ca891848934ffc214b7af85cdeac035d3aef84c4b0a8cf1a17ed843a2d4
copy: tracked
turns: 30
windows: 2
window_chars: 60000
ideas: 62
quotes_found: 61/62
generated_by: extract_ideas_dialogue_v1
prompt_sha256: 0954c180c11dae5ddb862a5d39b34f06d21364d490f686f249be18f04f740c22
mode: editor
agent: claude-code
model: opus
effort: low
---

## Window 1 of 2: turns 1 to 26

## Ideas

### lenguaje-como-universo
- **Who**: Luciano
- **Turn**: 1, 2026-05-29 17:00:30 UTC
- **Kind**: idea
- **What**: Inventing a programming language is like founding a universe with its own laws.
- **Quote**: "Inventar un lenguaje es como inventar un universo."

### un-solo-tipo-de-elemento
- **Who**: Luciano
- **Turn**: 1, 2026-05-29 17:00:30 UTC
- **Kind**: idea
- **What**: Minimalism: keep a single kind of element (all classes, or all functions), the way Lisp is all lists.
- **Quote**: "Me quedar con este con clases que todos sean clases o todos sean funciones Que sea, o sea, quedarte con una sola, bueno, en Lisp creo que son todas listas"

### solo-tipos-y-funciones
- **Who**: Luciano
- **Turn**: 1, 2026-05-29 17:00:30 UTC
- **Kind**: idea
- **What**: Base Luthier on homotopy type theory: only types and functions exist, and functions are themselves a type.
- **Quote**: "tendría que ser que solamente hay tipos y hay funciones, pero funciones son un tipo"

### implementaciones-como-paths
- **Who**: Luciano
- **Turn**: 1, 2026-05-29 17:00:30 UTC
- **Kind**: idea
- **What**: Abstract implementation through paths: one function has many implementations, and one sees the equivalence between them.
- **Quote**: "nosotros abstraemos el concepto de implementación a través de los paths, algo así. yo tengo distintas implementaciones y veo la equivalencia entre implementaciones"
- **Also in**: turns 5, 7

### tipos-dependientes-como-funcion-que-tira-tipo
- **Who**: Luciano
- **Turn**: 3, 2026-05-29 17:04:51 UTC
- **Kind**: idea
- **What**: A dependent type understood as a function that returns a type instead of a value, raising a level of abstraction.
- **Quote**: "Es como una función que tira un tipo. En vez de tirar una variable, es como que aumenta de clase, ¿no? O sea, aumenta de nivel de abstracción."

### codigo-es-demostracion
- **Who**: model
- **Turn**: 4, 2026-05-29 17:04:51 UTC
- **Kind**: proposal
- **What**: With dependent types the Luthier compiler is a mathematical prover; code and its proof become the same thing.
- **Quote**: "al habilitar que las funciones "tiren tipos", hacés que el propio compilador de Luthier sea un demostrador matemático. El código y la demostración matemática de que ese código funciona se vuelven la misma cosa."

### tipos-como-proposiciones
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Types are concepts, types as propositions, and types also include functions and higher-order functions.
- **Quote**: "tipos tienen que ser conceptos, o sea, tipos como proposiciones, y los tipos incluyen también funciones, no funciones y funciones de orden superior"

### pseudolenguaje-multiimplementable
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Luthier is not strictly in C++ but a pseudo-language implementable in different languages.
- **Quote**: "no sea estrictamente en C++, sino que sea como una especie de pseudo lenguaje que podría ser implementado en distintos lenguajes"

### declarativo-mas-optimizador
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Luthier is at once a declarative language and an optimization tool: you declare what you want and it openly shuffles implementations.
- **Quote**: "Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización"

### estimacion-abierta-por-ejecucion
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Each execution carries an estimate of its characteristics: error, compute time, memory, where it runs (cluster or computer).
- **Quote**: "para cada ejecuci ten dos cosas ten una estimaci de distintas caracter que es por ejemplo eso, el error y más que nada el tiempo de cómputo, pero también puede ser, qué sé yo, la memoria, también podría ser donde lo haces, si lo haces en un clúster, si lo haces en una computadora"

### cross-lenguaje-no-cross-compiler
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Luthier is not a cross-compiler but directly cross-language, agnostic of the language though its engine lives in one.
- **Quote**: "no es cross compiler sino es directamente cross lenguaje o sea como que ser un poco agn del lenguaje si bien el motor podr estar implementado en alguno de ellos"

### variantes-por-lenguaje
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: There could be a pi-Luthier, an R-Luthier, a C-Luthier, convertible one into another.
- **Quote**: "podés tener un, claro, un pi luthier, un ar luthier, un si luthier, donde podés transformar de uno en otro"

### base-de-datos-de-rendimiento-bayesiana
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Estimate complexity a priori with a Bayesian strategy, building a performance database of measured runs (function, inputs, scale, algorithm, time, precision).
- **Quote**: "yo para esta funci con estos datos iniciales y esta escala yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión. Y como lo sé, bueno, porque lo corrí, o sea, lo medí"

### generalizar-la-matriz-de-medidas
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Generalize the measured data to fill empty cells, e.g. estimate a cell from the row and column averages, or something more sophisticated.
- **Quote**: "yo tengo la media de los rows y las columnas bueno, podría estimar una celda por el promedio de la row y la columna"
- **Open**: how to do it effectively is left unresolved ("ahí estoy un poco en pelotas").

### filtrado-colaborativo-para-predecir
- **Who**: model
- **Turn**: 6, 2026-05-29 17:08:53 UTC
- **Kind**: proposal
- **What**: Use matrix factorization / collaborative filtering (recommender systems) to predict runtime of an algorithm on an input.
- **Quote**: "Luthier puede predecir cuánto tardará el *Algoritmo B* con un *Input X* haciendo **Filtrado Colaborativo**."

### lutherizar-las-funciones-de-estimacion
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: The time- and precision-estimation functions are themselves expressed in Luthier ("lutherized").
- **Quote**: "vos lutearizás las funciones de estimación del tiempo de cómputo, de la precisión de cómputo"

### categorias-de-computo-y-simplificacion-de-inputs
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: Find categories of computations that take the same time for different inputs, and predict from a simplification of the inputs (e.g. matrix dimensions).
- **Quote**: "vos tenés una simplificación de los inputs que ahí vos lo computás ... podría ser por ejemplo las dimensiones el número de columnas y rod de una matriz"

### tipo-universal
- **Who**: Luciano
- **Turn**: 5, 2026-05-29 17:08:53 UTC
- **Kind**: idea
- **What**: A universal type comprising the types of all dimensions, like an abstract class, taken as a feasible coding challenge.
- **Quote**: "vos suponés una especie de tipo universal que comprende a los tipos de todas las dimensiones. Y eso es algo así como una clase abstracta"

### pocos-tipos-reglas-bien-pensadas
- **Who**: Luciano
- **Turn**: 7, 2026-05-29 17:14:54 UTC
- **Kind**: idea
- **What**: The secret is very few types following well-thought, well-defined rules (HoTT-like).
- **Quote**: "tiene que tener muy pocos tipos, pero tienen que seguir muy claramente ciertas reglas bastante bien pensadas"

### autoextensible
- **Who**: Luciano
- **Turn**: 7, 2026-05-29 17:14:54 UTC
- **Kind**: idea
- **What**: Luthier must be completely self-extensible: you write all of Luthier in Luthier, so in the end only a few things are actually implemented as primitives.
- **Quote**: "tiene que ser completamente extensible, autoextensible, es decir, que vos puedas escribir como en Luthier, todo lo de Luthier básicamente, cosa que al final solamente termines implementando algunas cosas"

### secuestrar-codigo-externo
- **Who**: Luciano
- **Turn**: 7, 2026-05-29 17:14:54 UTC
- **Kind**: idea
- **What**: Luthier must be able to hijack code from any other language, with a well-defined DSL.
- **Quote**: "el UTIER tiene que poder secuestrar código de cualquier otro lenguaje"

### ejecutable-a-mano
- **Who**: Luciano
- **Turn**: 7, 2026-05-29 17:14:54 UTC
- **Kind**: idea
- **What**: If well written, Luthier should be executable by hand, with paper and pencil, like Lisp.
- **Quote**: "Luthier tendría que ser ejecutable a mano es decir que uno pudiese con l y papel escribir las cosas"

### matrimonio-hott-bayes
- **Who**: Luciano
- **Turn**: 7, 2026-05-29 17:14:54 UTC
- **Kind**: idea
- **What**: Path equivalence is the fundamental concept; proving it needs an internal prover plus empirical statistical demonstration, a probabilistic extension of HoTT, a marriage of HoTT and Bayes.
- **Quote**: "tendría que ser una especie de extensión probabilística de homeotopy type theory para que funcione ... sería como una especie de para mí tiene que ser una especie de matrimonio entre etapa y type theory y valles"

### core-librerias-tipo-externo
- **Who**: Luciano
- **Turn**: 9, 2026-05-29 17:19:26 UTC
- **Kind**: idea
- **What**: Luthier has a core plus libraries; libraries are Luthier functions connecting it to what is external (C++, Python, the machine), which calls for a type of external element.
- **Quote**: "las librerías serían las que harían a Luthier interactuar con otros programas ... ahí conceptualmente tendríamos que incluir, digamos, una especie de tipo de elemento externo"

### luthier-observador-read-write
- **Who**: Luciano
- **Turn**: 9, 2026-05-29 17:19:26 UTC
- **Kind**: idea
- **What**: Luthier as a closed observer of the universe that communicates by a read/write which is also a compilation/reading.
- **Quote**: "yo lo estoy pensando como un observador del universo ... sería como un read-write pero que sería como que a la vez haga una especie de compilación o lectura"

### luthier-como-relator
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: idea
- **What**: The most interesting first step is Luthier as a relator, an abstraction mechanism to express ideas (probability, sample, matrix, units, experiment).
- **Quote**: "lo más interesante es ver cómo pensarlo a Luthier como un relator un mecanismo de abstracción que permita expresar ideas"

### expresar-invarianzas-de-disciplinas
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: idea
- **What**: Luthier's aim is to express the invariances of the disciplines (a species must mate within itself; electrons are fermions, photons bosons).
- **Quote**: "la idea de luthier es expresar invarianzas de los de las disciplinas"

### multiplicar-matrices-es-una-implementacion
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: question
- **What**: What it means to multiply two matrices, and how a concrete calculation is uniquely an implementation of matrices, to be defined within Luthier.
- **Quote**: "qué significa que yo multiplico dos matrices? ... de qué manera ya uno tiene unívocamente determinado que es una implementación, que lo que vos estás haciendo es una implementación de las matrices"

### empezar-por-reales-con-error
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: idea
- **What**: Start from the ABC: reals, their operations, and a concept of error of the reals.
- **Quote**: "uno tiene que empezar por el ABC ... los números, los reales las operaciones de los reales y ese tipo de cosas y bueno, también tener un concepto de error de los reales"

### decoradores
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: idea
- **What**: Decorators in Luthier for the error of a number and its evolution, derivatives, etc., concepts he had implemented in C++ with templates, now easily expressible.
- **Quote**: "uno en Luthier puede hacer decoradores f por ejemplo eso, el error de un número, y cómo se evoluciona, las derivadas"

### funcion-por-propiedades
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: idea
- **What**: Define a function by its properties, not operationally, or both: the operation plus the propositions its inputs and outputs satisfy; and whether it is univocal or not.
- **Quote**: "definición de función desde el punto de vista de las propiedades no operativamente o tener las dos funciones, operativamente y las propiedades que contienen la proposición acerca de sus inputs y outputs"

### algebra-de-decoradores
- **Who**: Luciano
- **Turn**: 11, 2026-05-29 17:29:33 UTC
- **Kind**: idea
- **What**: Decorator composition has algebraic properties (associativity, commutativity); when commutative, represent it inside Luthier in the simplest form.
- **Quote**: "si la operación de un decorador sobre el otro decorador, por ejemplo, si cumple la asociatividad ... si son conmutativos, bueno, vos los representás dentro del UTIER de la forma más simple"

### conmutatividad-del-programa
- **Who**: Luciano
- **Turn**: 13, 2026-05-29 17:38:05 UTC
- **Kind**: question
- **What**: Whether a Luthier program is commutative in the order of its statements; generally programs are non-commutative, though declarations can be near-commutative (forward declaration).
- **Quote**: "si vos al cambiar el orden de los statements cambias el programa. Generalmente creo que todos los programas son no conmutativos"

### codigo-es-el-primer-elemento
- **Who**: Luciano
- **Turn**: 13, 2026-05-29 17:38:05 UTC
- **Kind**: idea
- **What**: A Luthier program is itself an element of Luthier; meta-use is native from the start, not a later graft as in Lisp. Code is the first element.
- **Quote**: "Hay que pensar que el código de Luthier sea un elemento de Luthier ya también desde el vamos. El código es el primer elemento."

### hott-no-modela-el-programa
- **Who**: Luciano
- **Turn**: 15, 2026-05-29 17:40:27 UTC
- **Kind**: question
- **What**: Doubt whether HoTT models a program as a type: the statements are modelable but the program itself is not clearly a type, a theoretical limbo.
- **Quote**: "el programa en sí, en principio no tan claramente, podría ser que yo una lista o algo así ... pero a mí me parece como que el metropólico de Tieri no está modelando eso"

### contextos-de-primera-clase
- **Who**: model
- **Turn**: 16, 2026-05-29 17:40:27 UTC
- **Kind**: proposal
- **What**: Treat the context as a type in itself, what in theory is called first-class contexts, to lift the program out of the limbo.
- **Quote**: "En informática teórica, a esto se le llama **Contextos de Primera Clase (First-Class Contexts)**."

### contexto-como-dag-y-tipos-implicitos
- **Who**: Luciano
- **Turn**: 17, 2026-05-29 17:46:56 UTC
- **Kind**: idea
- **What**: HoTT models the program as a context defined like a DAG; one could define implicit types through solutions, e.g. the type that solves a problem or the optimum of a function.
- **Quote**: "la manera de definir contexto sería como un DAG ... podrías definir tipos implícitos, a través de soluciones, o de, por ejemplo, el tipo que soluciona determinado problema"

### no-doble-definicion-o-producto-cartesiano
- **Who**: Luciano
- **Turn**: 17, 2026-05-29 17:46:56 UTC
- **Kind**: idea
- **What**: A grammar rule verifying no type is defined twice; or allow a double definition read as a Cartesian product, with a "cartesian expansion" warning in case it was an error.
- **Quote**: "verificar que ningún tipo está definido dos veces. Aunque podr estar definido dos veces y que sea un producto cartesiano tambi"

### tipos-no-definidos-y-forward-reference
- **Who**: Luciano
- **Turn**: 17, 2026-05-29 17:46:56 UTC
- **Kind**: idea
- **What**: Allow passing an as-yet-undefined type and defining it later; a type never defined is a program input.
- **Quote**: "vos podés por ejemplo, pasarte a un tipo que no está definido y lo definís después ... si no está definido nunca esos son otros tipos"

### expresividad-sobre-redundancia
- **Who**: Luciano
- **Turn**: 17, 2026-05-29 17:46:56 UTC
- **Kind**: idea
- **What**: A philosophical choice between redundancy (robustness) and expressivity; expressivity is preferred, with good messages for robustness, since redundancy can needlessly limit.
- **Quote**: "si vas a ser más redundante o expresivo ... en lo expresivo digamos, garpa más porque puede ser que lo redundante sea incómodo a veces y te limite al pedo"

### problema-del-olvido
- **Who**: Luciano
- **Turn**: 19, 2026-05-29 17:52:47 UTC
- **Kind**: idea
- **What**: Dependent types accumulate a growing typing load; the forgetting problem, where the decoration outgrows the value, is one of Luthier's fundamental problems to solve.
- **Quote**: "tenés ahí los problemas del olvido ... Que tiene que ser uno de los problemas fundamentales de Luthier que tiene que solucionar"

### monoide-no-libre
- **Who**: Luciano
- **Turn**: 19, 2026-05-29 17:52:47 UTC
- **Kind**: idea
- **What**: The typing must simplify: not a free monoid but some monoid that keeps the resulting type's complexity bounded.
- **Quote**: "que no sea un monoide libre b o sea tiene que ser algún tipo de monoide que de alguna manera mantenga la complejidad del tipo resultante"

### limitar-la-composicion-de-tipos-dependientes
- **Who**: Luciano
- **Turn**: 19, 2026-05-29 17:52:47 UTC
- **Kind**: idea
- **What**: A key engineering problem: a mechanism to limit the composition of dependent functions to something informative, i.e. how to simplify the composition of dependent types.
- **Quote**: "cómo hacer para simplificar la composición de tipos dependientes"

### truncamiento-homotopico
- **Who**: model
- **Turn**: 20, 2026-05-29 17:52:47 UTC
- **Kind**: proposal
- **What**: Offer the programmer truncation operators (homotopy truncation) to clean a complex type.
- **Quote**: "El programador tendría que poder usar **Operadores de Truncamiento** (que en $HoTT$ se llaman *Homotopy Truncation*)."
- **Open**: rejected by Luciano in turn 21 as crude.

### rechazo-del-truncamiento-tosco
- **Who**: Luciano
- **Turn**: 21, 2026-05-29 17:59:38 UTC
- **Kind**: rejection of turn 20
- **What**: Rejects crude truncation/forgetting: with dependent types you must have a well-defined algebra of dependent types, you cannot do that.
- **Quote**: "La IA me propone cosas toscas como truncamiento o olvido o lo que sea. Si vas a tener tipos de pendientes, los tenés con un álgebra de tipos de pendientes bien definida, no podás hacer una cosa así."

### loop-como-potencia
- **Who**: Luciano
- **Turn**: 21, 2026-05-29 17:59:38 UTC
- **Kind**: idea
- **What**: Exploit associativity and patterns: a loop is a series of functions to a power, so the type stays expressed as a combination of types with an exponent.
- **Quote**: "si vos tenés un algoritmo que repite un loop entonces va a ser una serie de funciones y despu a una potencia Entonces el tipo te puede quedar expresado as"

### el-tipo-guarda-la-historia
- **Who**: Luciano
- **Turn**: 21, 2026-05-29 17:59:38 UTC
- **Kind**: idea
- **What**: What the type holds is the history of how you arrived at it.
- **Quote**: "lo que tenés en el tipo es la historia de cómo vos llegaste hasta ahí"

### funtores-de-olvido-definen-el-lenguaje
- **Who**: Luciano
- **Turn**: 21, 2026-05-29 17:59:38 UTC
- **Kind**: idea
- **What**: Selective forgetting via a non-invertible forgetting function; which forgetting function you apply to the types defines the language you speak, making forgetful functors one of Luthier's most important components.
- **Quote**: "de qué función de olvido le aplicás a los tipos, es un, digamos, eso te define básicamente el lenguaje que estás hablando ... los functores de olvido serían, digamos, uno de los componentes más importantes de Luthier"

### olvidos-optimizan-cosas-distintas
- **Who**: Luciano
- **Turn**: 23, 2026-05-29 18:01:42 UTC
- **Kind**: idea
- **What**: Different forgetting functions optimize different things, so knowing their properties and which to use for what is fundamental.
- **Quote**: "las distintas funciones de olvido de los tipos van a optimizar distintas cosas ... entender, digamos, las propiedades de eso sería como fundamental"

### tres-funtores-de-olvido
- **Who**: model
- **Turn**: 24, 2026-05-29 18:01:42 UTC
- **Kind**: proposal
- **What**: Three forgetful functors by what they optimize: operative (compute), static (compilation), bayesian (precision), whose composition should commute.
- **Quote**: "El Functor de Olvido Operativo (Optimiza Cómputo) ... El Functor de Olvido Estático (Optimiza Compilación) ... El Functor de Olvido Bayesiano (Optimiza la Precisión)"

### cuadrados-conmutativos-de-olvido
- **Who**: Luciano
- **Turn**: 25, 2026-05-29 18:05:19 UTC
- **Kind**: idea
- **What**: Analyze forgetting with commutative squares: forget-then-apply-functions must equal apply-functions-then-forget; the two paths are compared for equivalence.
- **Quote**: "si haces olvido compuesto con la serie de funciones es lo mismo que serie de funciones y después de olvido eso tendría que ser digamos que conmute que eso sea igual y bueno, podés comparar ahí también son dos paths y ves la equivalencia"

### expresar-para-no-dudar
- **Who**: Luciano
- **Turn**: 25, 2026-05-29 18:05:19 UTC
- **Kind**: idea
- **What**: The point is not to do everything but to have the tools to express alternatives; no one is best or worst, each has its use, and expressivity is what matters, even if the use is to convince yourself something is useless.
- **Quote**: "no es que uno tiene que obligatoriamente hacer todo, sino tener las herramientas para expresar distintas alternativas ... No hay una mejor, una peor ... Aunque el uso sea convencerte de que no sirva para nada. Por lo menos no dudar."

## Window 2 of 2: turns 27 to 30

## Ideas

### meta-recursividad-es-el-objeto
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: idea
- **What**: The object of Luthier is to work on Luthier; being meta-recursive is fundamental to it.
- **Quote**: "Creo que la más importante es que Luthier, el objeto de Luthier es trabajar sobre Luthier. O sea, que sea meta recursivo es fundamental."

### optimizar-las-reglas-porque-el-lenguaje-es-suyo
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: idea
- **What**: Since he invents the language it follows the rules he wants, so he can optimize the rules to make working on Luthier easy.
- **Quote**: "dado que es un lenguaje que yo invento, digamos, sigue las reglas que yo quiero, entonces puedo optimizar las reglas para que eso sea fácil."

### conmutatividad-de-statements
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: idea
- **What**: Make statements commutative so that their order doesn't change the result, which would simplify composition and manipulation of programs.
- **Quote**: "que sea conmutativo en los statements, que el orden de los statements no altera el resultado, eso simplificaría mucho la composición y la manipulación de programas."

### conmutatividad-cuesta-expresividad
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: tension
- **What**: Making the program commutative takes away expressivity; a type declared twice could be read as a cartesian product running two ways.
- **Quote**: "cosas que son que el programa sea conmutativo te quita expresividad de alguna manera, eso es verdad ojo"
- **Open**: How a twice-declared type would run ("de dos maneras", "habría que ver bien exactamente") is left undecided.

### modelar-el-tiempo-como-dependencia
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: open question
- **What**: How to model time, i.e. the order of things, in Luthier; perhaps as mathematical dependency, where one thing depending on another is what gives a time.
- **Quote**: "acá uno de los temas es este es cómo modelamos el tiempo en Luthier o sea el orden de las cosas y quizás digamos la forma de hacerlo sea modelarlo digamos como se hace matemáticamente que vos dec que esto depende del otro entonces ah hay un tiempo"
- **Open**: Left as a tentative route ("quizás"), not settled.

### luthier-como-dag-de-definiciones
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: idea
- **What**: Think of Luthier as a Directed Acyclic Graph of definitions, over which you operate.
- **Quote**: "que sea que Luthier es un Directed Aciclic Graph de definiciones entonces la cosa es bastante fácil vos operás sobre esos sobre Dax"

### combinar-dos-dags-como-operacion
- **Who**: Luciano
- **Turn**: 27, 2026-05-29 18:13:07 UTC
- **Kind**: idea
- **What**: Combining two DAGs would be an operation on Luthier, where the concept of substitution (as in defining a function by substituting a variable) comes into play.
- **Quote**: "serían cómo combinás dos DAG por ejemplo, eso sería una operación sobre Luthier interesante es muy interesante porque claro ahí como es el concepto de sustitución"
- **Open**: How substitution and module composition become graph operations is left unworked ("estoy un poco ahí pensándolo todo").

### recuento-tres-pilares
- **Who**: model
- **Turn**: 28, 2026-05-29 18:13:07 UTC
- **Kind**: proposal
- **What**: The model recounts Luciano's closing as three interconnected pillars, naming the first native meta-recursivity (the language is its own data).
- **Quote**: "Meta-recursividad Nativa: El Lenguaje es su Propio Dato"

### equivalencia-de-homotopia-en-codigo
- **Who**: model
- **Turn**: 30, 2026-05-29 18:21:51 UTC
- **Kind**: proposal
- **What**: In the consolidated document, the model formulates that proving a path (weak equivalence) between a slow/safe and a fast/complex algorithm lets you program thinking in the simple model but compile and run the fast one with mathematical certainty.
- **Quote**: "Si demostrás que existe un *path* (una equivalencia débil) entre el algoritmo lento/seguro y el rápido/complejo, el compilador de Luthier podría dejarte programar pensando en el modelo simple (A), pero compilar y ejecutar el modelo rápido (B) con la certeza matemática absoluta de que no va a romper nada."
- **Open**: Appears inside turn 30's verbatim consolidation of the earlier session, not a fresh move.

### dsl-de-papel-path-como-logica-mas-bayes
- **Who**: model
- **Turn**: 30, 2026-05-29 18:21:51 UTC
- **Kind**: proposal
- **What**: The model sketches a minimal paper DSL where a type's foreign implementations are tied by a defPath whose proof is a Bayesian estimate, i.e. Path as logical proof plus Bayesian evidence.
- **Quote**: "(defPath equivalencia_solvers\n    : Path(resolver_python, resolver_cpp)\n    := (bayes_estimate :samples 1000 :confidence 0.9999)\n)"
- **Open**: Appears inside turn 30's verbatim consolidation of the earlier session.

Note: turn 29 is a request ("Podés copiar Verbatim todo este diálogo"), not an idea. Turn 30 is a verbatim re-transcription of the whole session, heavily elided here; its substantive ideas belong to window 1 and are not re-listed except for the two model formulations above that appear as full text.
