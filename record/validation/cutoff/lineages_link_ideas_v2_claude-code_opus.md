# Lineages of the ideas about Luthier

Written by `scripts/link_ideas.py` (link_ideas v1) for Luciano and for the distillation. Prompt `link_ideas_v2`
(sha256 a04a21445ebf), model opus at effort low via claude-code (2.1.197 (Claude Code)); 7 calls. Input: `record/ideas/timeline.jsonl`, last read with sha256
b18b5806955d. Who said an idea first and whether Luciano adopted a model's idea are computed from the rows' times and authors, not by the model.

Rows: 1020 in the timeline; placed 1016, unplaced 4, pending 0. Lineages: 404.

| scope | first said by Luciano | first said by model | first said by pasted |
|---|---|---|---|
| language | 218 | 138 | 1 |
| method | 22 | 14 | 0 |
| other | 6 | 5 | 0 |

First said by a model and then taken up by Luciano: 6.

## Lineages, by first appearance

### L-code-as-data (language)

Code is data: a program's code can be held and operated on like a value, erasing the distinction between code and data (the Lisp path).

first 2022-06-15 08:55 by Luciano; 12 rows, 11 witnesses, 8 days, last 2026-09-28

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 11] `written:2022-06-15_sin-titulo-2:clases-implican-predicados`: "con tapp quise explorar la idea de que las clases implican predicados y que el codigo es dato."
- 2022-06-15 08:55 Luciano restates [2022-06-15 Sin título 2 .md line 13] `written:2022-06-15_sin-titulo-2:codigo-es-dato`: "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad que ofrece pero es notable que los lenguajes modernos no sigan ese camino…"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 25] `written:2022-06-28_luciano-code-style:erase-code-data-distinction`: "poder crear nuevos "objetos" (sean valores o variables, de tipos, funciones o "clases"). Al mismo tiempo perder la distincion entre codigo y dato."
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 65] `written:2022-08-03_haskell:codigo-como-dato`: "la idea del codigo como dato, es hacer que el codigo de una funcion sea como los parametros de un tipo, solo que en lugar de tener numeros o tipos, tiene opera…"
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 73] `written:2022-08-03_haskell:modelo-lisp`: "Yo creo que tengo que seguir el modelo Lisp."
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 17] `written:2023-02-22_tapp-wish-list:code-as-data`: "Code as data. Debo poder operar sobre las definiciones de funciones. O sea que debo distinguir entre el codigo y la aplicacion del codigo."
- ... 4 more rows
- 2026-06-05 13:18 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 1] `dialogue:20260605T1318:codigo-como-datos`: "si vos tomás los datos como como los datos las funciones como datos o sea, el código como datos entonces sí podés tener también lo mismo"
- 2026-09-28 20:56 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:codigo-dato-estilo-lisp`: "`Program` es un tipo inductivo (lista de definiciones) y `eval` es una función parcial `Program → Name → Maybe Term`. No hay un `eval` que inyecte términos arb…"

### L-identifiers-central (language)

Identifiers are central to programming: a simple label stands for a complex object, joining human and machine.

first 2022-06-15 08:55 by Luciano; 4 rows, 4 witnesses, 4 days, last 2023-03-13

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 9] `written:2022-06-15_sin-titulo-2:identificadores-importan`: "con quimulun quise explorar la idea de la importancia de los identificadores."
- 2022-07-05 07:53 Luciano refines [2022-07-05 Sin título 2.md line 11] `written:2022-07-05_sin-titulo-2:etiqueta-para-objeto-complejo`: "Toda la gracia de la computacion pasa por identificar elementos complejos por una simple etiqueta."
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 35] `written:2022-08-03_haskell:nombres-como-direcciones`: "los nombres son grandes simplificadores de la programacion. La pregunta es si tengo tipos o funciones creadas dinamicamente, como creo nombres para ellas?"
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 15] `written:2023-03-13_hacia-luthier:diccionario-humano-maquina-literalismo`: "la estructura mas importante de la programacion es el diccionario que une el humano con la maquina, es la base del literalismo"

### L-remaking-language (method)

The language has been remade many times, each time rethinking the foundations of programming more deeply.

first 2022-06-15 08:55 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-15

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 3] `written:2022-06-15_sin-titulo-2:rehacer-desde-las-bases`: "estuve re-haciendo macror muchisimas veces cada vez volviendo a repensar mas las bases de la programacion."

### L-channel-state-one (language)

A channel's state type is isomorphic to the type ONE.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 53] `written:2022-06-28_luciano-code-style:channel-state-isomorphic-to-one`: "un tipo channel state que es isomorfico con el tipo ONE"

### L-channels-product-states-sum (language)

Multiplicity of channels is a product (exponential to a number) while multiplicity of states is a sum.

first 2022-06-28 22:25 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 85] `written:2022-06-28_luciano-code-style:channels-multiplicity-as-product`: "multiplicidad de canales (pero como producto, no suma, exponencial a un numero)"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 49] `written:2022-06-28_luciano-code-style:state-multiplicity-as-sum`: "si quiero decir el estado i entre N estados "similares", el tipo del estado i seria estado x N, siendo N el tipo 1+1+1..+1 N veces. Es decir el set de N compon…"

### L-code-to-understand (method)

I code to understand: understanding requires manipulating the code and seeing how changes affect its observables.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 3] `written:2022-06-28_luciano-code-style:code-to-understand`: "I code to understand."

### L-dependent-types (language)

A dependent type is a type that depends on a value, taking the cardinality of that value's type.

first 2022-06-28 22:25 by Luciano; 6 rows, 5 witnesses, 3 days, last 2026-05-30

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 115] `written:2022-06-28_luciano-code-style:dependent-types`: "dependent-types: son tipos que dependen de un valor, lo cual hace que su cardinalidad sea la del typo del valor que toma"
- 2026-05-29 14:03 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.03.24.md [00:15]] `day:2026-05-29:tipos-dependientes`: "Es como una función que tira un tipo. En vez de tirar una variable, es como que aumenta de clase"
- 2026-05-29 14:03 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.03.24.md [00:15]] `note:2026-05-29T14.03.24:tipos-dependientes-como-funciones-que-tiran-tipos`: "Es como una función que tira un tipo. En vez de tirar una variable, es como que aumenta de clase, ¿no? O sea, aumenta de nivel de abstracción."
- 2026-05-29 14:04 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 3] `dialogue:20260529T1400:tipos-dependientes-como-funcion-que-tira-tipo`: "Es como una función que tira un tipo. En vez de tirar una variable, es como que aumenta de clase, ¿no? O sea, aumenta de nivel de abstracción."
- 2026-05-29 15:56 Luciano refines [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:tipos-dependientes-funcion-que-tira-tipo`: "es como una función que tira un tipo. En vez de tirar una variable, es como que aumenta de clase, ¿no? O sea, aumenta de nivel de abstracción"
- 2026-05-30 18:08 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:40]] `note:2026-05-30T18.07.21:tipos-dependientes-como-primitiva`: "los tipos dependientes, sí, probablemente eso es un concepto, digamos, básico, inicial"

### L-equivalence-optimization (language)

Once semantic equivalence is established, a clear but slow implementation can be replaced by a faster equivalent one, enabling automatic optimization.

first 2022-06-28 22:25 by Luciano; 5 rows, 5 witnesses, 3 days, last 2026-05-29

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 33] `written:2022-06-28_luciano-code-style:choose-efficient-path-after-validity`: "una vez que se establece la validez semantica y la equivalencia semantica se puede optar por el camino mas eficiente."
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 27] `written:2022-06-28_luciano-code-style:equivalence-relations-for-optimization`: "Es importante establecer las relaciones de equivalencia en quimulun. Esto permite optimizar los tiempos de calculo."
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 17] `written:2022-06-28_luciano-code-style:slow-clear-algorithm-as-gold-standard`: "es posible que una algoritmo que es expresado de una forma clara pero computacionalmente no eficiente pueda ser optimizado con un algoritmo mas criptico. Esto…"
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 29] `written:2023-02-22_tapp-wish-list:optimizacion-automatica`: "Permitir la optimizacion automatica del codigo a medida que se mide el consumo de recursos de implementaciones alternativas de distintas funciones."
- 2026-05-29 15:21 model restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 30] `dialogue:20260529T1400:equivalencia-de-homotopia-en-codigo`: "Si demostrás que existe un *path* (una equivalencia débil) entre el algoritmo lento/seguro y el rápido/complejo, el compilador de Luthier podría dejarte progra…"

### L-express-vars-types (language)

The language must let one express variables and types, including functional and class types, with their semantics.

first 2022-06-28 22:25 by Luciano; 3 rows, 3 witnesses, 2 days, last 2022-08-03

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 107] `written:2022-06-28_luciano-code-style:how-to-define-values-types-variables-functions`: "Como creo valores (values) y sus tipos (types), variables (variables), y tipos de variables (¿?), funciones y tipos de funciones."
- 2022-06-28 22:25 Luciano restates [2022-06-28 Luciano Code style.md line 21] `written:2022-06-28_luciano-code-style:library-for-types-with-semantics`: "Expresar variables y tipos, y tipos funcionales, de clases etc y con sus semantica."
- 2022-08-03 11:56 Luciano questions [2022-08-03 tapp before.md line 27] `written:2022-08-03_tapp-before:typing-a-write-function`: "como expreso el tipo de write a?"

### L-expressiveness (language)

Code must express its intention to both the human reader and the compiler, referring truthfully to known structures and to extra-computational concepts.

first 2022-06-28 22:25 by Luciano; 3 rows, 3 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 15] `written:2022-06-28_luciano-code-style:express-extra-computational-concepts-with-verification`: "Expresa conceptos extra-computacionales (por ejemplo probabilidad) de forma intuitiva y veraz. La idea es abstraer las propiedades compulacionales de estos con…"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 13] `written:2022-06-28_luciano-code-style:expressive-reference-to-known-structures`: "refiere a estructuras o algoritmos conocidos y esta referencia es real. Por ejemplo, no puedo llamar array a una lista."
- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 9] `written:2022-06-28_luciano-code-style:expressiveness-as-observable`: "Expresividad: el codigo debe expresar la intención del mismo tanto para el que leer el codigo como para el compilador."

### L-foundation-choice (language)

Open choice of foundation: how far to go with type theory vs category theory, HoTT vs set theory.

first 2022-06-28 22:25 by Luciano; 2 rows, 2 witnesses, 2 days, last 2023-03-02

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 59] `written:2022-06-28_luciano-code-style:type-theory-vs-category-theory`: "aqui tengo que pensar hasta que punto sigo con type theory y hasta que punto uso category theory."
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 17] `written:2023-03-02_estoy-perdido:hott-o-zmt-como-base`: "empiezo con HoTT o con ZMT?"

### L-nat-to-set-constructor (language)

A type constructor takes a natural number and returns a set containing that number.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 57] `written:2022-06-28_luciano-code-style:type-constructor-from-natural`: "un constructor de tipos que toma un numero natural y te devuelve un conjunto que contiene ese numero natural."

### L-primitive-functions (language)

The language has a set of primitive functions (arithmetic, comparison, logical, string operations).

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 111] `written:2022-06-28_luciano-code-style:primitive-functions`: "funciones primitivas: suma, resta, multiplicacion, division, division entera, modulo, concatenacion de strings...., and, or, not, greater than, equal.."

### L-primitive-types (language)

The language has a set of primitive value types (boolean, integer, real, string, nothing, one, ...).

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 109] `written:2022-06-28_luciano-code-style:primitive-value-types`: "tipos de valores primitivos: boolean, integer, real, string, nothing (or zero), one (or something), memory (¿?), size (¿?)"

### L-reasoning-code-isomorphism (language)

Formalize semantic determination so there is a one-to-one relation between reasoning and the flow of the code, verifying the reasoning.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 31] `written:2022-06-28_luciano-code-style:one-to-one-reasoning-code-flow`: "abstraer y formalizar los mecanismos de determnacion sematinca de forma que haya una relacion uno a uno entre el razonamiento y el flujo del codigo. De esta fo…"

### L-sample-probability-duality (language)

Sample and probability form a duality, with tests demonstrating it.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 93] `written:2022-06-28_luciano-code-style:sample-probability-duality`: "muestra y probabilidad --\> dualidad y tests que demuestran que se cumple."

### L-semantics-own-universe (language)

The language's semantics lives in its own universe, not C++'s, even though expressed with C++ structures.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 23] `written:2022-06-28_luciano-code-style:semantics-live-in-own-universe`: "Esta semantica "vive" en su propio universo que no es el de C++, aunque use las estructuras de C++ para expresarlos."

### L-state-equivalence-relation (language)

There is an equivalence relation between (state*k)^N and the multinomial sum over multi-indices.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 95] `written:2022-06-28_luciano-code-style:equivalence-relation-multinomial`: "Relacion de equivalencia entre (state\*k)^N y Sum\_{\|a\|=k} C(n,a) \*state^a , a-\>multiindice"

### L-compute-memory-os (language)

Compute and memory exceed the environment and are the task of the operating system and compiler.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 33] `written:2022-07-05_sin-titulo-2:frontera-con-el-sistema-operativo`: "Esto claramente es un problema que excede al del environment aunque esta unido indefectiblemente porque necesitas memoria y recursos computacionales para opera…"

### L-env-executes-functions (language)

The environment also handles executing functions to generate new variables, with queueing and resource supply.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 27] `written:2022-07-05_sin-titulo-2:environment-ejecuta-funciones`: "el environment tambien debe manejar 1\) la ejecución de funciones para generar nuevas variables."

### L-env-first-object (language)

The environment is the first object the language must define, since data is loaded into it.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 5] `written:2022-07-05_sin-titulo-2:environment-es-el-primer-objeto`: "tengo que definir un environment donde cargar los datos, obvio."

### L-env-map-of-definitions (language)

The environment is a map of definitions or values.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 9] `written:2022-07-05_sin-titulo-2:environment-como-mapa-de-definiciones`: "El environment no puede ser otra cosa que un mapa de definiciones o valores (las llamaremos variables, pero pueden ser constantes, tendria que encontrar un nom…"

### L-env-simple-compound (language)

There are simple environments (one type, one identifier) and compound ones admitting many.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 39] `written:2022-07-05_sin-titulo-2:environments-simples-y-compuestos`: "hay environments simples (solo admiten un tipo de valor y un unico identificador) y otros compuestos que admiten multiples."

### L-env-store-retrieve (language)

The environment's two fundamental mechanisms are storing new variables and retrieving old ones, and all variables descend from it.

first 2022-07-05 07:53 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 15] `written:2022-07-05_sin-titulo-2:dos-mecanismos-del-environment`: "Hay dos mecanismos fundamentales del environment"
- 2022-07-05 07:53 Luciano refines [2022-07-05 Sin título 2.md line 37] `written:2022-07-05_sin-titulo-2:variables-descienden-del-environment`: "todas las variables decienden environment, en el sentido de que pueden guardar nuevos valores y recuperar los valores guardados, siempre que les indiques su no…"

### L-env-two-resources (language)

The environment has two resources: memory to store variables and compute to manage them.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 21] `written:2022-07-05_sin-titulo-2:dos-recursos-del-environment`: "El environment tiene dos recursos: 1\) memoria para guardar las variables. 2\) recursos computacionales para manejar la memoria y guardar o recuperar las varia…"

### L-variable-anatomy (language)

A variable is a name, a memory address, a size and a type (the type containing the size).

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 45] `written:2022-07-05_sin-titulo-2:variable-como-nombre-direccion-tamano-tipo`: "una variable es un nombre, una direccion de memoria, un tamaño de memoria y un typo. En realidad el tipo contiene el tamaño de memoria y el nombre, si se quier…"

### L-variable-not-know-env (language)

A variable better not know its environment, so one can predict whether it will acquire further resources.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 43] `written:2022-07-05_sin-titulo-2:variable-no-debe-saber-su-environment`: "mejor que no sepa su environment, porque si la variable sabe su environment, entonces no hay forma de predecir si va a adquirir otros recursos, especialmente s…"

### L-code-metafunctions (language)

One can apply functions that operate on code: run tests, compute errors or derivatives, find equivalents, estimate run time, incorporating these into the syntax.

first 2022-08-03 11:56 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-08-31

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 71] `written:2022-08-03_haskell:funciones-que-modifican-el-codigo`: "puedo aplicar funciones que modifican el codigo: como hacer tests o calcular errores o derivadas o encontar codigos equivalentes o estimar el tiempo de ejecuci…"
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 17] `written:2022-08-03_haskell:testeos-probabilidades-errores-tiempos-en-la-sintaxis`: "incorporar los testeos, las probabilidades, los errores y los tiempos de calculo en la sintaxis del lenguaje junto con las relaciones de equivalencia para las…"
- 2026-08-31 19:50 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [02:02]] `note:2026-08-31T19.48.17:codigo-que-guarda-los-calculos`: "tengo un código que representa los cálculos y entonces yo ahí lo puedo autodiferenciar, puedo por ejemplo tomar notas, puedo hacer que el cálculo me dé un resu…"

### L-constructive-declarative-types (language)

Types are defined in two ways: constructive (data) and declarative (a proposition the type satisfies).

first 2022-08-03 11:56 by Luciano; 3 rows, 3 witnesses, 3 days, last 2023-03-02

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 27] `written:2022-08-03_haskell:dos-formas-de-definir-tipos-constructivo-declarativo`: "hay dos formas de definir tipos: el constructivo (data en Haskell) y el declarativo (class en Haskell)."
- 2023-02-22 16:12 Luciano restates [2023-02-22 tapp wish list.md line 3] `written:2023-02-22_tapp-wish-list:dos-tipos-de-tipos`: "Dos tipos de tipos:"
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 25] `written:2023-03-02_estoy-perdido:definiciones-constructivas-y-declarativas`: "tenemos dos tipos de definiciones las constructivas y las declarativas"

### L-constructor-vs-function (language)

A constructor differs from a function: the constructor plus its parameters are the element (transparent), while a function involves a computation.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 57] `written:2022-08-03_haskell:diferencia-constructor-funcion`: "cual es la diferencia entre un constructor y una funcion?"

### L-constructors-in-type-space (language)

Constructors should live in each type's space rather than the global space.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 53] `written:2022-08-03_haskell:constructores-en-el-espacio-de-cada-tipo`: "En haskell los constructores viven en el espacion global. quizas sea buena idea que vivan en el espacio de cada tipo"

### L-declare-is-test (language)

Declaring a function means declaring what it must satisfy as a test, so tests can be generated automatically.

first 2022-08-03 11:56 by Luciano; 7 rows, 7 witnesses, 3 days, last 2026-08-31

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 19] `written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test`: "La idea central del tapp es que al declarar una funcion vos declaras que es lo que la funcion debe cumplir como un test y entonces es posible generar tests aut…"
- 2026-06-05 13:39 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 13] `dialogue:20260605T1318:invariantes-generan-los-tests`: "uno tiene que poder digamos definir cada una de los tipos este de la aplicación este por sus invariantes y que y de esas invariantes salen directamente en los…"
- 2026-06-05 13:39 model restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 14] `dialogue:20260605T1318:tipos-como-tests-curry-howard`: "En Luthier, al ser un relator de ideas, **la definición del tipo y el test son la misma cosa**."
- 2026-08-31 19:53 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [05:04]] `note:2026-08-31T19.48.17:htt-inspiracion-la-definicion-genera-el-test`: "un lenguaje que sea inspirado por los homeotopy type theory, en el cual vos definas una función y que al definir la función ya con eso quede definido el test s…"
- 2026-08-31 19:53 Luciano refines [WhatsApp Ptt 2026-08-31 at 19.48.17.md [05:14]] `day:2026-08-31:definir-una-funcion-define-su-test`: "en el cual vos definas una función y que al definir la función ya con eso quede definido el test sobre esa función."
- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:autoverificacion`: "Definir una función define su test: la likelihood junto con su simulación, una función junto con su inversa. Correr el código es correr el test."
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:autoverificacion`: "Definir una función define su test: la likelihood junto con su simulación, una función junto con su inversa. Correr el código es correr el test. Podés \"luthie…"

### L-element-one-type (language)

An element satisfies many types, but the chosen relation is that each element belongs to exactly one type and can serve to build many.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 25] `written:2022-08-03_haskell:un-elemento-cumple-muchos-tipos`: "en la teoria de tipos tenemos la relacion elemento y tipo. El problema es que un elemento cumple con muchos tipos a la vez."
- 2022-08-03 11:56 Luciano corrects [2022-08-03 haskell.md line 47] `written:2022-08-03_haskell:un-elemento-un-tipo-sirve-a-muchos`: "cada elemento pertenece exactamente a un tipo, pero puede servir para construir una multitud de tipos (conversion implicita?)."

### L-function-holds-code (language)

A function holds its code written in script form plus a simplified compiled form.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 69] `written:2022-08-03_haskell:funcion-guarda-script-tapp-y-compilado`: "las funciones contienen el codigo escrito en tapp (es tipo script, si queres) ademas de alguna forma simplificada compilada."

### L-identifier-type-independent (language)

The identifier and the type are completely independent; the identifier is a fantasy name unknown until resolved.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 99] `written:2022-08-03_haskell:simetria-valor-tipo-funcion-identificador-independiente`: "si aplicamos la simetria de que pasamos de una variable-valor a una variable-tipo a una variable-funcion, entonces vemos que el identificador y el tipo deberia…"

### L-inject-multiple-identifiers (language)

A type or function can inject more than one identifier into the environment.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 121] `written:2022-08-03_haskell:un-tipo-inyecta-varios-identificadores`: "un tipo o una funcion puede inyectar mas de un identificador en el environment..."

### L-language-self-writing (language)

The process of defining new types and functions should be programmable, the language writing itself, which requires a simple language with no syntactic sugar.

first 2022-08-03 11:56 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-05-29

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 15] `written:2022-08-03_haskell:proceso-de-creacion-de-tipos-programable`: "Yo lo que quiero hacer es que el proceso (2) pueda ser programable, es decir que el lenguaje se pueda escribir a sí mismo. Para lograr esto, el lenguaje debe s…"
- 2026-05-29 14:14 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [00:26]] `note:2026-05-29T14.14.08:autoextensibilidad`: "tiene que ser completamente extensible, autoextensible, es decir, que vos puedas escribir como en Luthier, todo lo de Luthier, básicamente, cosa que al final s…"
- 2026-05-29 14:14 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7] `dialogue:20260529T1400:autoextensible`: "tiene que ser completamente extensible, autoextensible, es decir, que vos puedas escribir como en Luthier, todo lo de Luthier básicamente, cosa que al final so…"

### L-subtype-by-predicate (language)

The subObject is the most important concept: a subset of an object satisfying a predicate (a test), written with equals and guards.

first 2022-08-03 11:56 by Luciano; 4 rows, 4 witnesses, 2 days, last 2026-09-29

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 115] `written:2022-08-03_haskell:subtipos-con-predicado`: "ambient\_temperature = type ambient\_temperature x: real \| (-30\<x)& x\<40"
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 7] `written:2022-08-03_tapp-before:equals-defines-subtypes-by-predicate`: "esa es mi idea: usar el igual para definir tipos subobjetos. (lo puedo indicar con guardas \"\|\")."
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 13] `written:2022-08-03_tapp-before:subobject-as-central-concept`: "El concepto mas importante es el de subObjeto: un subconjunto del objeto algebraico que cumple con un cierto predicado, un test."
- 2026-09-29 07:39 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 75] `dialogue:890a551c:subtipo-es-tipo-mas-predicado`: "Lo que quiero definir es un suboject, es decir un predicate on a type. \nEntonces, un subtype es definido pon un type y un predicate en ese type."

### L-type-definition-recursive (language)

A type's definition is necessarily recursive, since the type must be universally accessible.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 103] `written:2022-08-03_haskell:definicion-de-tipo-es-recursiva`: "la definicion de un tipo es necesariamente recursiva."

### L-types-defined-by-propositions (language)

A type or function is defined by the propositions (postconditions) it satisfies, for variables and for functions alike.

first 2022-08-03 11:56 by Luciano; 5 rows, 5 witnesses, 4 days, last 2025-09-27

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 23] `written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple`: "poder indicar en cada tipo (no distingo entre tipo y funcion) cual es la proposicion que cumple. Aqui hay dos versiones: una computacional y otra escrita. La i…"
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 9] `written:2023-02-22_tapp-wish-list:funciones-con-precondiciones-y-postcondiciones`: "Las funciones se definen con precondiciones (los subtipos de los argumentos) y postcondiciones (proposiciones que involucran a argumentos y valores retornados)."
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 43] `written:2023-03-02_estoy-perdido:tipos-de-funciones-por-postcondiciones`: "Defino tipos de funciones, diciendo cuales son las postcondiciones."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 41] `written:2023-03-02_estoy-perdido:tipos-de-variables-por-postcondiciones`: "Defino tipos de variables, diciendo cuales son sus postcondiciones"
- 2025-09-27 18:31 Luciano restates [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 4] `dialogue:01998d16:hottification-function-types-as-contracts`: "we define interal \"function types\" as functions that follow some postconditions given that the arguments validate their preconditions."

### L-composition-dot (language)

Composition is written with a dot, which explains class methods.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 9] `written:2022-08-03_tapp-before:composition-with-dot`: "La composicion la indico con puntos . (esto explica los metodos de clases)"

### L-equals-assertion (language)

The sign '=' asserts that one side equals the other.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 3] `written:2022-08-03_tapp-before:equals-as-assertion`: "encontre una idea que me puede servir de generadora para tapp/quimulun: la idea de que el signo \"=\" representa aserciones, es decir que un lado es igual al o…"

### L-equals-pattern-matching (language)

The equals sign is used for pattern matching when a symbol is unknown.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 5] `written:2022-08-03_tapp-before:equals-for-pattern-matching`: "Esto se usa para pattern matching cuando algun simbolo es desconocido."

### L-functions-predefined-user (language)

Functions are of two kinds: predefined and user defined.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 41] `written:2022-08-03_tapp-before:two-kinds-of-functions`: "functions are of two types"

### L-laws-as-universal-propositions (language)

A type carries laws its operations must satisfy universally (identity, io round-trip), stated with for_all.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 29] `written:2022-08-03_tapp-before:identity-with-universal-law`: "Identity id \| for_all x:a {id x = x}"
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 37] `written:2022-08-03_tapp-before:io-type-with-roundtrip-laws`: "when (for_all x: a {x\| write \| read = (Just x,\"\")}) & (forall y: s {y\| read \| write = y})"

### L-sum-types-alternatives (language)

Types can be expressed as alternatives with '|' (maybe, either, sum).

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 19] `written:2022-08-03_tapp-before:types-as-tagged-alternatives`: "maybe a = Nothing \| Just a"

### L-test-result-explains (language)

A condition or test yields either success (one) or an explanation of why it failed, not just a boolean.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 2 days, last 2023-03-13

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 15] `written:2022-08-03_tapp-before:test-succeeds-or-explains-failure`: "Ahora un test o es exitoso o hay una explicacion de porque falla."
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 13] `written:2023-03-13_hacia-luthier:condicion-devuelve-uno-o-mensaje`: "en realidad el resultado de cualquier condicion deberia ser uno si se cumplen las condiciones y un mensaje indicando porque no se cumplieron."

### L-type-autodetection (language)

Types can be used via autodetection.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 11] `written:2022-08-03_tapp-before:type-autodetection`: "El otro criterio es usar la \"autodeteccion\" de tipos."

### L-define-together-tuples (language)

There is only one way to define, in tuples that may hold several identifiers, assigned together when their postconditions are interdependent (crossconditions).

first 2023-02-22 16:12 by Luciano; 4 rows, 4 witnesses, 3 days, last 2023-03-13

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 11] `written:2023-02-22_tapp-wish-list:definir-funciones-en-grupo`: "Esto hace que muchas funciones se deban definir en grupo ya que las postcondiciones involucran a varias funciones a la vez (como leer y escribir o las operacio…"
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 45] `written:2023-03-02_estoy-perdido:tuplas-con-crosscondiciones`: "Defino una tupla de tipos de variables y de funciones con postcondiciones que involucran a toda la tupla. (crosscondiciones)."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 47] `written:2023-03-02_estoy-perdido:unica-forma-de-definir-es-en-tuplas`: "solo hay una forma de definir y es en tuplas, que pueden tener uno o mas identificadores."
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 11] `written:2023-03-13_hacia-luthier:asignacion-simultanea-por-interdependencia`: "En el caso que las postcondiciones de los objetos sean interdependientes, los objetos se asignan simultaneamente."

### L-express-math-definitions (language)

The language must express mathematical definitions such as category, functor and group.

first 2023-02-22 16:12 by Luciano; 2 rows, 2 witnesses, 2 days, last 2023-03-02

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 13] `written:2023-02-22_tapp-wish-list:poder-definir-objetos-matematicos`: "Tengo que poder definir este tipo de objetos matematicos."
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 15] `written:2023-03-02_estoy-perdido:expresar-definiciones-matematicas-como-categorias`: "como expreso las definiciones matematicas como categoria, functor, grupo etc"

### L-language-parts (language)

The language has parts: a grammar and semantics definition and a front compiler from it to C++.

first 2023-02-22 16:12 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-02-22

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 35] `written:2023-02-22_tapp-wish-list:partes-grammar-y-front-compiler`: "A. tapp grammar definition, semantics rules etc"

### L-learn-from-runs (method)

Each run of the code teaches something: whether an implementation is correct or how fast it is.

first 2023-02-22 16:12 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-02-22

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 31] `written:2023-02-22_tapp-wish-list:aprender-de-cada-corrida`: "La idea es que de cada corrida del codigo algo se aprende, ya sea se sabe que una implementacion es correcta ya que se mide su velocidad."

### L-post-becomes-precondition (language)

A subtype defined by a function's postconditions can serve as a precondition of another function.

first 2023-02-22 16:12 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-02-22

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 9] `written:2023-02-22_tapp-wish-list:el-subtipo-de-una-funcion-como-precondicion-de-otra`: "lo cual hace que este subtipo sea usado como precondicion de otra funcion."

### L-self-verified-programs (language)

Luthier writes self-verified programs: object creation verifies pre- and postconditions, and an implementation belongs to a type only once duly tested, turning unsafe/untested code into safe/tested code.

first 2023-02-22 16:12 by Luciano; 9 rows, 9 witnesses, 5 days, last 2026-09-29

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 21] `written:2023-02-22_tapp-wish-list:unsafe-a-safe`: "convertir unsafe code en safe code (usando los tipos como codificadores de precondiciones)."
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 25] `written:2023-02-22_tapp-wish-list:untested-a-tested`: "convertir untested code en tested code: haciendo que las implementaciones de las funciones solo pertenezcan a un tipo si han sido debidamente testeadas y que l…"
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 9] `written:2023-03-13_hacia-luthier:creaciones-verifican-pre-y-pos`: "Las creaciones de objetos verifican que se cumplans las pre y pos conditions del objeto creado."
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 3] `written:2023-03-13_hacia-luthier:luthier-programas-autoverificados`: "como es Luthier el lenguaje para escribir programas autoverificados?"
- 2025-09-27 18:31 Luciano refines [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 4] `dialogue:01998d16:accept-functions-only-after-they-pass-the-test`: "the reasonable thing to do is to only accept functions into the compiler after they pass the test. ... even after the function being accpeted it should also co…"
- 2026-08-31 19:54 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [05:56]] `note:2026-08-31T19.48.17:niveles-de-verificacion`: "vos lo podes tener sin testear, testeado, qué sé yo. Y hay distintos niveles de verificación de las cosas"
- ... 1 more rows
- 2026-09-29 06:01 Luciano restates [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 61] `dialogue:175c0408:luthier-serie-de-tipos-y-funciones-verificadas`: "Luthier seria una serie de tipos y funciones verificadas con un conjunto de teoremas/tests..."
- 2026-09-29 06:01 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 61] `dialogue:890a551c:library-como-serie-de-tipos-y-funciones-verificadas`: "Luthier seria una serie de tipos y funciones verificadas con un conjunto de teoremas/tests..."

### L-category-declaration (language)

A category is declared as a class built from its components (objects, homs, composition, identity) whose types carry the associativity and identity laws.

first 2023-02-28 18:06 by Luciano; 6 rows, 6 witnesses, 1 days, last 2023-02-28

- 2023-02-28 18:06 Luciano states [2023-02-28 Sin título 1 w.md line 13] `written:2023-02-28_sin-titulo-1-w:categoria-como-clase-con-componentes`: "Category(Obj,Hom,Compose,Id)"
- 2023-02-28 18:06 Luciano questions [2023-02-28 Sin título 1 w.md line 1] `written:2023-02-28_sin-titulo-1-w:categoria-declaracion-estilos`: "como hago para declarar una categoria"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 19] `written:2023-02-28_sin-titulo-1-w:compose-con-ley-de-asociatividad`: "function Compose (Hom(X,Y), Hom(Y,Z))-\>Hom(X,Z)=\>Associative (Compose)"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 5] `written:2023-02-28_sin-titulo-1-w:estilo-cpp-clases-funciones`: "Estilo c++"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 21] `written:2023-02-28_sin-titulo-1-w:id-con-leyes-de-identidad`: "function Id(X)-\>Hom(X,X) =\> Identity_right(Id(X),Hom(X,Y)) & Identity_left(Hom(Y,X),Id(X))"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 17] `written:2023-02-28_sin-titulo-1-w:object-y-hom-como-tipos-dependientes`: "type Hom(Object X, Object Y)"

### L-declaration-vs-definition (language)

Declaration says something has a type; definition says how to obtain its value.

first 2023-03-02 11:27 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 21] `written:2023-03-02_estoy-perdido:declaration-vs-definition`: "1\) declaration: decis que algo tiene un tipo"

### L-implementation-as-functor (language)

A function's declaration (its type/postconditions) is separate from its implementation: implementations are functors, may depend on unknown functions, and natural transformations translate one into another.

first 2023-03-02 11:27 by Luciano; 4 rows, 4 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 37] `written:2023-03-02_estoy-perdido:funciones-por-postconditions-sin-implementacion`: "Defino funciones que son de un tipo dado (es decir que cumplen con ciertas postconditions) sin decir cual es la implmentacion."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 9] `written:2023-03-02_estoy-perdido:functores-como-implementaciones`: "Functores : implementaciones"
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 39] `written:2023-03-02_estoy-perdido:implementacion-que-depende-de-implementaciones-desconocidas`: "Defino funciones y doy su implementacion que depende de funciones cuya implementacion no se."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 11] `written:2023-03-02_estoy-perdido:natural-transformations-como-traduccion`: "Natural transformations: traducir una implementacion en otra"

### L-parameters (language)

Defining a variable of a type without stating its value is a parameter.

first 2023-03-02 11:27 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 31] `written:2023-03-02_estoy-perdido:parametros-variables-de-tipo-sin-valor`: "Defino variables de un tipo dado sin decir cual es el valor, es decir parametros."

### L-type-inference-flag (language)

A value's type is deduced by type calculation; if the derived type is larger than the parameter's, it is flagged.

first 2023-03-02 11:27 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 35] `written:2023-03-02_estoy-perdido:tipo-deducido-por-calculo-de-tipos`: "El tipo se deduce por el calculo de tipos. Si el tipo derivado es mayor que el tipo del parametro, se indica."

### L-variables-as-functions (language)

A variable can be defined as a function of other variables, checking that the arguments meet the preconditions.

first 2023-03-02 11:27 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 33] `written:2023-03-02_estoy-perdido:variables-funcion-con-verificacion-de-precondiciones`: "Defino variables que son funcion de otras variables o parametros. Se verifica si los argumentos de las funciones cumplen con las precondiciones ..."

### L-assignment-structure (language)

Luthier is a chain of assignments, each an identifier, an equals sign and an operation that creates the object.

first 2023-03-13 14:48 by Luciano; 2 rows, 2 witnesses, 1 days, last 2023-03-13

- 2023-03-13 14:48 Luciano states [2023-03-13 hacia Luthier.md line 7] `written:2023-03-13_hacia-luthier:asignacion-identificador-igual-operacion`: "cada asignacion tiene un identificador para recuperar el objeto creado, un signo igual y una operacion para crear el objeto."
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 5] `written:2023-03-13_hacia-luthier:luthier-cadena-de-asignaciones`: "Luthier es una cadena de asignaciones."

### L-algebraic-composability (language)

Models compose algebraically across subunits, pathways and scales.

first 2025-06-17 06:20 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 31] `written:2025-06-17_hottification-program:algebraic-composability-across-scales`: "Algebraic model composability across subunits, pathways, and scales."

### L-certified-outputs (language)

The language yields certified binding schemes, conformational spaces and energetic couplings.

first 2025-06-17 06:20 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 26] `written:2025-06-17_hottification-program:certified-binding-and-energetic-objects`: "Certified binding schemes, conformational spaces, energetic couplings."

### L-compositional-kinetic (language)

Kinetic models are built compositionally from conformational state components, an external product of conformational degrees of freedom with energetic coupling rules.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 33] `written:2025-06-17_hottification-program:mechanistic-to-kinetic-transition`: "Clean transitions from mechanistic theories to kinetic models."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 70] `written:2025-06-17_vault-glossary-v1:conformational-algebra`: "A compositional system for building kinetic models from conformational state components:"
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 72] `written:2025-06-17_vault-glossary-v1:external-product-of-conformational-dof`: "External product of conformational degrees of freedom."

### L-core-type-ingredients-sufficient (language)

Sigma-types, Pi-types, identity types and HITs suffice to encode conformational models, energetic couplings and symmetry structures.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 129] `written:2025-06-17_hottification-program:hottification-primitives-sufficiency`: "Sigma-types, Pi-types, identity types, HITs are sufficient to encode conformational models, energetic couplings, and symmetry structures."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 129] `written:2025-06-17_program-hott-dsl:hottification-feasibility`: "Sigma-types, Pi-types, identity types, HITs are sufficient to encode conformational models, energetic couplings, and symmetry structures."

### L-couplings-as-types (language)

Energetic couplings are represented as types.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 52] `written:2025-06-17_hottification-program:energetic-couplings-as-types`: "Energetic couplings as types."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 52] `written:2025-06-17_program-hott-dsl:energetic-couplings-as-types`: "Energetic couplings as types."

### L-embedded-semantic-structure (language)

Biological models carry embedded semantic structure: symmetry groups, compositional operators, equivalence classes.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 14] `written:2025-06-17_hottification-program:models-carry-embedded-semantic-structure`: "Allow biological models to carry embedded semantic structure:"
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 14] `written:2025-06-17_program-hott-dsl:models-carry-embedded-semantic-structure`: "Allow biological models to carry embedded semantic structure:"

### L-hierarchical-dependent-types (language)

Hierarchical model construction across subunits, pathways and scales is enforced by dependent types.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 32] `written:2025-06-17_hottification-program:dependent-types-for-hierarchy`: "Hierarchical model construction naturally enforced by dependent types."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 32] `written:2025-06-17_program-hott-dsl:hierarchical-models-via-dependent-types`: "Hierarchical model construction naturally enforced by dependent types."

### L-hott-dsl-core-proposal (language)

Build a domain-specific modeling language on HoTT in which biological models are expressed, composed and transformed with access to type-level structure.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 9] `written:2025-06-17_hottification-program:language-on-hott-for-biological-models`: "Build a domain-specific modeling language based on Homotopy Type Theory (HoTT) that allows biological models to be expressed, composed, and transformed with fu…"
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 9] `written:2025-06-17_program-hott-dsl:dsl-based-on-hott-for-biological-models`: "Build a domain-specific modeling language based on Homotopy Type Theory (HoTT) that allows biological models to be expressed, composed, and transformed with fu…"

### L-hott-probability-tension (language)

There is a tension between HoTT (invertible identities, univalence) and probability (non-invertible uncertainty), with no unified model yet.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 91] `written:2025-06-17_hottification-program:foundational-tension-hott-vs-probability`: "HoTT: invertible identities, univalence, internalized equivalence."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 91] `written:2025-06-17_program-hott-dsl:foundational-tension-hott-vs-probability`: "HoTT: invertible identities, univalence, internalized equivalence."

### L-internal-equality (language)

HoTT gives types as spaces and identities as paths, its internal equality replacing ad hoc isomorphisms.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 77] `written:2025-06-17_hottification-program:internal-equality-replaces-isomorphisms`: "Internal equality replaces ad hoc isomorphisms."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 75] `written:2025-06-17_program-hott-dsl:types-as-spaces-identities-as-paths`: "Provides types as spaces, identities as paths, higher paths as equivalences."

### L-likelihood-type-propagation (language)

Likelihood recursion is encoded via type-theoretic propagation, with noise structures and model boundaries as dependent types.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 163] `written:2025-06-17_hottification-program:macroir-likelihood-via-type-propagation`: "Encode likelihood recursion via type-theoretic propagation."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 163] `written:2025-06-17_program-hott-dsl:likelihood-recursion-via-type-propagation`: "Encode likelihood recursion via type-theoretic propagation."
- 2025-06-17 06:21 model restates [term_hottification.md line 29] `written:2025-06-17_term-hottification:likelihood-recursion-type-propagated`: "Inference engines (where likelihood recursion is type-propagated)."

### L-markov-generated-objects (language)

Markov models become generated objects rather than arbitrary inputs.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 38] `written:2025-06-17_hottification-program:markov-models-as-generated-objects`: "Markov models become generated objects rather than arbitrary inputs."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 38] `written:2025-06-17_program-hott-dsl:markov-models-as-generated-objects`: "Markov models become generated objects rather than arbitrary inputs."

### L-meta-layer (language)

The language sits as a meta-layer above the ConformationalModel DSL, MacroIR and Bayesian pipelines.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 18] `written:2025-06-17_hottification-program:meta-layer-above-existing-dsls`: "Serve as meta-layer above ConformationalModel DSL, MacroIR, and Bayesian pipelines."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 18] `written:2025-06-17_program-hott-dsl:meta-layer-above-existing-dsls`: "Serve as meta-layer above ConformationalModel DSL, MacroIR, and Bayesian pipelines."

### L-models-as-typed-objects (language)

Biological models are well-typed mathematical objects where types are molecular states, identity paths are symmetries, and composition emerges from dependent type operations.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 105] `written:2025-06-17_hottification-program:types-as-molecular-states`: "Biological models can be defined as well-typed objects where types represent molecular states, identity paths represent symmetries, and model composition emerg…"
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 105] `written:2025-06-17_program-hott-dsl:models-as-well-typed-objects`: "Biological models can be defined as well-typed objects where types represent molecular states, identity paths represent symmetries, and model composition emerg…"
- 2025-06-17 06:21 model refines [term_hottification.md line 19] `written:2025-06-17_term-hottification:models-as-typed-mathematical-objects`: "**models themselves become typed mathematical objects**, with equivalences, symmetries, and compositions validated directly by the type system."

### L-planned-type-system (language)

Planned work: formalize a type system for state and energy algebra and implement HoTT-based state composition primitives.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 135] `written:2025-06-17_hottification-program:type-system-for-state-and-energy-algebra`: "Formalize type system for state and energy algebra"
- 2025-06-17 18:29 model refines [hottification_manifesto_v0.1.md line 21] `written:2025-06-17_hottification-manifesto-v0-1:type-constructors-for-conformational-model-composition`: "Write Type Constructors for Conformational Model Composition."

### L-proof-assistants-verify (language)

Proof assistants (Coq, Lean, Agda) can verify the semantic correctness of biological models via type-checking.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 125] `written:2025-06-17_hottification-program:proof-assistant-verification`: "Proof assistants (Coq, Lean, Agda) can verify semantic correctness of biological models via type-checking."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 125] `written:2025-06-17_program-hott-dsl:machine-checkable-via-proof-assistants`: "Proof assistants (Coq, Lean, Agda) can verify semantic correctness of biological models via type-checking."

### L-sampler-type-indexed (language)

Sampler state spaces (parallel tempering ladders) are reformulated as type-indexed manifolds.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 159] `written:2025-06-17_hottification-program:tempering-state-spaces-as-type-indexed-ladders`: "Map parameter manifolds as type-indexed temperature ladders."
- 2025-06-17 06:21 model restates [term_hottification.md line 28] `written:2025-06-17_term-hottification:sampler-spaces-as-type-indexed-manifolds`: "Sampler spaces (parallel tempering spaces as type-indexed manifolds)."

### L-separate-deterministic-probabilistic (language)

Deterministic structural validity (lifted into types via HoTT) is kept separate from probabilistic inference, handled downstream by Bayesian layers.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 19] `written:2025-06-17_hottification-program:separate-structural-validity-from-inference`: "Separate deterministic structural validity (via HoTT) from probabilistic inference (via Bayesian layers)."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 19] `written:2025-06-17_program-hott-dsl:separate-structural-validity-from-probabilistic-inference`: "Separate deterministic structural validity (via HoTT) from probabilistic inference (via Bayesian layers)."
- 2025-06-17 06:21 model refines [term_hottification.md line 27] `written:2025-06-17_term-hottification:lifting-deterministic-structure-into-types`: "Probabilistic models (where deterministic structure is lifted into types)."

### L-symmetry-reduction (language)

Symmetry reductions are path-based identities; identity types collapse state redundancies and aggregate states by equivalent coupling into reduced Markov spaces.

first 2025-06-17 06:20 by model; 4 rows, 4 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 53] `written:2025-06-17_hottification-program:symmetry-reductions-as-path-identities`: "Symmetry reductions as path-based identities."
- 2025-06-17 06:20 model refines [program_hott_dsl.md line 113] `written:2025-06-17_program-hott-dsl:identity-types-collapse-redundancy`: "Identity types automatically collapse state redundancies and symmetries into reduced Markov spaces."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 53] `written:2025-06-17_program-hott-dsl:symmetry-reductions-as-path-identities`: "Symmetry reductions as path-based identities."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 75] `written:2025-06-17_vault-glossary-v1:symmetry-reduction-and-state-aggregation`: "State aggregation based on equivalent coupling configurations."

### L-type-level-validity (language)

Invalid or inconsistent models are prevented at the type level, validated structurally at compile time instead of at runtime.

first 2025-06-17 06:20 by model; 5 rows, 5 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 25] `written:2025-06-17_hottification-program:type-checking-prevents-invalid-models`: "Semantic modeling language prevents invalid models from being constructed."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 25] `written:2025-06-17_program-hott-dsl:types-prevent-invalid-models`: "Semantic modeling language prevents invalid models from being constructed."
- 2025-06-17 06:21 model refines [term_hottification.md line 17] `written:2025-06-17_term-hottification:compile-time-correctness-instead-of-runtime-validation`: "Replacing external or runtime-only validation with **compile-time structural correctness**."
- 2025-06-17 06:23 model restates [vault_glossary_v1.md line 14] `written:2025-06-17_vault-glossary-v1:compile-time-structural-validation`: "Compile-time structural validation of models."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 27] `written:2025-06-17_vault-glossary-v1:invalid-models-eliminated-at-type-level`: "Violations of model consistency are eliminated at the type level, prior to execution or inference."

### L-type-safe-priors (language)

Type-safe prior spaces bridge the MacroIR likelihood engine with structural model spaces.

first 2025-06-17 06:20 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 37] `written:2025-06-17_hottification-program:type-safe-prior-spaces`: "Type-safe prior spaces for inference pipelines."

### L-unifies-domains (language)

One DSL framework unifies models across channels, enzymes, networks, signaling and regulation.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model states [Hottification program.md line 121] `written:2025-06-17_hottification-program:universality-across-biological-domains`: "The DSL framework unifies models across channels, enzymes, networks, signaling, and regulation."
- 2025-06-17 06:20 model restates [program_hott_dsl.md line 121] `written:2025-06-17_program-hott-dsl:universality-across-biological-domains`: "The DSL framework unifies models across channels, enzymes, networks, signaling, and regulation."

### L-components-as-types (language)

Model components and entities are encoded as types.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model states [term_hottification.md line 13] `written:2025-06-17_term-hottification:model-components-as-types`: "Encoding model components as **types**."
- 2025-06-17 06:23 model restates [vault_glossary_v1.md line 10] `written:2025-06-17_vault-glossary-v1:types-as-entities`: "Types as entities."

### L-higher-paths (language)

Higher paths capture higher-order symmetries and transformations between equivalences.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model states [term_hottification.md line 15] `written:2025-06-17_term-hottification:symmetries-as-higher-paths`: "Capturing higher-order symmetries and structural relations as **higher paths**."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 12] `written:2025-06-17_vault-glossary-v1:higher-paths-as-equivalence-transformations`: "Higher paths as equivalence transformations."

### L-hottification (language)

HoTTification is turning a scientific model, algorithm or language into a formal structure governed by HoTT, analogous to categorification, giving machine-verifiable theories.

first 2025-06-17 06:21 by model; 6 rows, 6 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model refines [term_hottification.md line 40] `written:2025-06-17_term-hottification:analogy-to-categorification-formalization-quantization`: "Categorification** (Category Theory)"
- 2025-06-17 06:21 model states [term_hottification.md line 9] `written:2025-06-17_term-hottification:hottification-as-transforming-a-model-into-a-hott-structure`: "**HoTTification** is the process of transforming a scientific model, algorithm, or modeling language into a formal structure governed by the principles of **Ho…"
- 2025-06-17 06:21 model refines [term_hottification.md line 32] `written:2025-06-17_term-hottification:path-toward-machine-verifiable-biological-theories`: "A path toward machine-verifiable biological theories."
- 2025-06-17 06:21 model refines [term_hottification.md line 33] `written:2025-06-17_term-hottification:unification-of-model-algebra-and-identity-preserving-transformations`: "A unification of model algebra, compositional safety, and identity-preserving transformations."
- 2025-06-17 06:23 model restates [vault_glossary_v1.md line 8] `written:2025-06-17_vault-glossary-v1:hottification-as-transforming-models-into-hott-structure`: "HoTTification is the process of transforming a scientific model, algorithm, or modeling language into a formal structure governed by Homotopy Type Theory (HoTT…"
- 2025-06-17 18:29 model refines [hottification_manifesto_v0.1.md line 19] `written:2025-06-17_hottification-manifesto-v0-1:hottification-operators`: "Formalize HoTTification Operators."

### L-identity-paths-equivalences (language)

Identity paths represent structural equivalences between model structures or entities.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model states [term_hottification.md line 14] `written:2025-06-17_term-hottification:equivalences-as-identity-paths`: "Representing equivalences between model structures as **identity paths**."
- 2025-06-17 06:23 model restates [vault_glossary_v1.md line 11] `written:2025-06-17_vault-glossary-v1:identity-paths-as-structural-equivalences`: "Identity paths as structural equivalences."

### L-semantic-safety (language)

Semantic safety is model correctness enforced by the modeling language's structural rules (dependent typing), distinct from runtime safety, so only valid models can exist.

first 2025-06-17 06:21 by model; 6 rows, 6 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model states [term_hottification.md line 44] `written:2025-06-17_term-hottification:semantic-safety-layer-above-runtime`: "Introduces **semantic safety layer** above runtime execution."
- 2025-06-17 06:21 model refines [term_hottification.md line 16] `written:2025-06-17_term-hottification:semantic-safety-via-dependent-typing`: "Enforcing **semantic safety** via dependent typing, guaranteeing internal consistency of model compositions."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 13] `written:2025-06-17_vault-glossary-v1:dependent-types-enforce-semantic-safety`: "Dependent types enforcing semantic safety."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 30] `written:2025-06-17_vault-glossary-v1:runtime-vs-semantic-safety`: "Runtime safety: prevents crashes or numeric failures."
- 2025-06-17 06:23 model restates [vault_glossary_v1.md line 27] `written:2025-06-17_vault-glossary-v1:semantic-safety-enforced-by-the-language`: "Semantic safety refers to model correctness enforced by structural rules in the modeling language itself, ensuring that only structurally valid models can be c…"
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 31] `written:2025-06-17_vault-glossary-v1:semantic-safety-prevents-invalid-models-from-existing`: "Semantic safety: prevents invalid scientific models from existing."

### L-bayesian-scientific-mapping (other)

Scientific knowledge production is mapped into explicit Bayesian structures (introduction to prior, methods to likelihood, results to observations, discussion to posterior), making reasoning auditable.

first 2025-06-17 06:23 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model states [vault_glossary_v1.md line 40] `written:2025-06-17_vault-glossary-v1:bayesianization-of-the-scientific-pipeline`: "The process of formally mapping scientific knowledge production into explicit Bayesian structures:"
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 42] `written:2025-06-17_vault-glossary-v1:paper-sections-as-bayesian-components`: "Introduction → Prior."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 47] `written:2025-06-17_vault-glossary-v1:science-made-auditable-and-probabilistic`: "The goal is to make scientific reasoning auditable, quantifiable, and explicitly probabilistic at every step."

### L-dsl-model-compilers (language)

The DSLs are model compilers translating high-level mechanistic specifications into executable, inferable structures (state spaces, likelihoods, samplers).

first 2025-06-17 06:23 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model states [vault_glossary_v1.md line 102] `written:2025-06-17_vault-glossary-v1:dsls-as-model-compilers`: "The DSLs you are building serve as model compilers."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 100] `written:2025-06-17_vault-glossary-v1:model-compiler`: "A system that translates high-level mechanistic model specifications into executable, inferable structures (e.g. state spaces, likelihood functions, samplers)."

### L-fim-validation (method)

A likelihood is validated by agreement between the Fisher Information Matrix from score covariance and from the Hessian, without full inference.

first 2025-06-17 06:23 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model states [vault_glossary_v1.md line 90] `written:2025-06-17_vault-glossary-v1:fim-self-consistency-diagnostic`: "Agreement between these two estimates validates the correctness of likelihood implementation without requiring full inference."

### L-macroir-consumes-markov (language)

MacroIR consumes Markov models produced by the ConformationalModel DSL or HoTTified generators, computing interval-averaged likelihoods for macroscopic current data.

first 2025-06-17 06:23 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model states [vault_glossary_v1.md line 60] `written:2025-06-17_vault-glossary-v1:macroir-consumes-markov-models`: "MacroIR consumes Markov models produced by ConformationalModel DSL or HoTTified model generators."
- 2025-06-17 06:23 model refines [vault_glossary_v1.md line 57] `written:2025-06-17_vault-glossary-v1:macroirization`: "The act of feeding structurally defined kinetic models into the MacroIR likelihood recursion engine, which computes full interval-averaged likelihoods for macr…"

### L-active-compiler-engines (language)

Prototype active compiler engines.

first 2025-06-17 18:29 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 18:29 model states [hottification_manifesto_v0.1.md line 22] `written:2025-06-17_hottification-manifesto-v0-1:active-compiler-engines`: "Prototype Active Compiler Engines."

### L-bridge-types-inference (language)

Bridge type theory with probabilistic inference engines.

first 2025-06-17 18:29 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 18:29 model states [hottification_manifesto_v0.1.md line 23] `written:2025-06-17_hottification-manifesto-v0-1:bridge-type-theory-with-probabilistic-inference`: "Bridge Type Theory with Probabilistic Inference Engines."

### L-generative-model-spaces (language)

The strategic aim is to replace ad hoc model design with compositional, type-safe, generative model spaces.

first 2025-06-17 18:29 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 18:29 model states [hottification_manifesto_v0.1.md line 6] `written:2025-06-17_hottification-manifesto-v0-1:compositional-type-safe-generative-model-spaces`: "Replace ad hoc model design with compositional, type-safe, generative model spaces."

### L-metatheory-discovery (other)

The final product is not new models but a unifiable, machine-checkable theory-building system, a meta-theory of scientific discovery architecture.

first 2025-06-17 18:29 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 18:29 model states [hottification_manifesto_v0.1.md line 13] `written:2025-06-17_hottification-manifesto-v0-1:meta-theory-of-discovery-architecture`: "The final product is not just new models, but **a meta-theory of scientific discovery architecture**."
- 2025-06-17 18:29 model restates [hottification_manifesto_v0.1.md line 7] `written:2025-06-17_hottification-manifesto-v0-1:unifiable-theory-building-system`: "Create a unifiable theory-building system:"

### L-model-space-algebras (language)

Define algebras for transforming model spaces.

first 2025-06-17 18:29 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 18:29 model states [hottification_manifesto_v0.1.md line 20] `written:2025-06-17_hottification-manifesto-v0-1:model-space-transformation-algebras`: "Define Model-Space Transformation Algebras."

### L-adjoint-diagnostic-pairs (language)

Each forward operation (simulate, infer, likelihood) is paired with a diagnostic co-operation (recover, invert, summarize) in an adjoint-like relation, and the system's tests are derived from these pairs.

first 2025-06-18 03:00 by model; 8 rows, 8 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 48] `written:2025-06-18_hottification-program-stack-v2-0:adjoint-forward-diagnostic-pair`: "$F \dashv G$: each forward morphism $F$ (e.g. simulate, infer) has a diagnostic approximation $G$ (e.g. recover, summarize)."
- 2025-06-18 03:03 model refines [SAV_kernel_v1.0.md line 44] `written:2025-06-18_sav-kernel-v1-0:cli-morphism-correspondence`: "Each command exposed by the inference engine CLI represents a morphism $F$ in a semantic pipeline ... SAV constructs a diagnostic co-operation $G$ for each suc…"
- 2025-06-18 03:03 model restates [SAV_kernel_v1.0.md line 9] `written:2025-06-18_sav-kernel-v1-0:forward-operation-paired-with-diagnostic-co-operation`: "Each forward operation $F$ ... is paired with a diagnostic co-operation $G$ ..., forming an adjoint-like relationship."
- 2025-06-18 03:08 model refines [Deployment Plan and Paper Kernel.md line 99] `written:2025-06-18_deployment-plan-and-paper-kernel:adjunctions-as-smart-tests`: "simulation ↔ inference ... log-likelihood ↔ FIM ... evidence ↔ normalization"
- 2025-06-18 03:08 model restates [Deployment Plan and Paper Kernel.md line 86] `written:2025-06-18_deployment-plan-and-paper-kernel:cli-operation-as-typed-morphism`: "Each CLI operation is a typed morphism."
- 2025-06-18 03:13 model refines [ho_ttification_manifesto_v_2.md line 33] `written:2025-06-18_ho-ttification-manifesto-v-2:adjunctions-before-types`: "**Adjunctions before types**: Adjoint pairs provide a scaffold before HoTT-level types are possible."
- 2025-06-18 03:13 model refines [ho_ttification_manifesto_v_2.md line 21] `written:2025-06-18_ho-ttification-manifesto-v-2:semantic-adjoint-verification`: "Derive orthogonal smart tests from adjoint functor pairs (diagnostic ⊗ forward)"
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 22] `written:2025-06-18_ho-ttification-manifesto-v-2-1:adjunctions-structure-diagnostics`: "**Adjunctions are not abstract — they structure diagnostics.**"

### L-contagiously-safe-dsl (language)

The endgame is a compile-time Contagiously Safe DSL whose safety propagates through the system, enforcing structure at the compiler level with a type-safe backend and a HoTT-verified inference algebra.

first 2025-06-18 03:00 by model; 6 rows, 6 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 21] `written:2025-06-18_hottification-program-stack-v2-0:contagiously-safe-dsl-compiler`: "**Contagiously Safe DSL Compiler** | Compile-time safe model language + backend codegen"
- 2025-06-18 03:00 model refines [HoTTification Program Stack v2.0.md line 20] `written:2025-06-18_hottification-program-stack-v2-0:hott-kernel-with-semantic-zones`: "**Type-Theoretic HoTT Kernel** | Formal model/inference algebra + semantic zones"
- 2025-06-18 03:08 model restates [Deployment Plan and Paper Kernel.md line 19] `written:2025-06-18_deployment-plan-and-paper-kernel:contagiously-safe-dsl`: "Contagiously Safe DSL + type-safe backend | Full realization of HoTTification"
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 55] `written:2025-06-18_ho-ttification-manifesto-v-2:contagious-safety`: "The Contagiously Safe Compiler is our endgame."
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 25] `written:2025-06-18_ho-ttification-manifesto-v-2:formal-hottification-dsl`: "Build type-safe DSL, semantic zones, and fully HoTT-verified inference algebra"
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 36] `written:2025-06-18_ho-ttification-manifesto-v-2-1:contagiously-safe-dsls`: "**Contagiously Safe DSLs** — systems where structure is enforced at the compiler level"

### L-declarative-model-interface (language)

A declarative model interface (a YAML DSL with a parser and CLI) is isolated from the C++ internals.

first 2025-06-18 03:00 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 17] `written:2025-06-18_hottification-program-stack-v2-0:declarative-model-from-yaml`: "**DSL Kernel (Model Spec + Parser)** | Declarative model interface from YAML"
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 22] `written:2025-06-18_ho-ttification-manifesto-v-2:external-dsl-parser`: "Isolate declarative model interface from C++ internals"

### L-epistemic-firewall (language)

The verification layer acts as an epistemic firewall defending the system against silent semantic drift during refactoring.

first 2025-06-18 03:00 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 65] `written:2025-06-18_hottification-program-stack-v2-0:epistemic-firewall-against-drift`: "Epistemic firewall | Defends MacroIR++ against silent semantic drift during refactor"
- 2025-06-18 03:03 model restates [SAV_kernel_v1.0.md line 52] `written:2025-06-18_sav-kernel-v1-0:sav-as-epistemic-firewall-in-hottification`: "This aligns directly with our larger HoTTification program, where SAV plays the role of **epistemic firewall** during the early refactor and modularization pha…"

### L-groupoid-paths (language)

Inference operations and their diagnostics form equivalence classes, a pre-formal groupoid, with each test a witness path, reading paths as equivalences in the HoTT sense.

first 2025-06-18 03:00 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 55] `written:2025-06-18_hottification-program-stack-v2-0:pre-formal-groupoid-of-operations`: "**Pre-formal groupoid structure**: inference operations and diagnostics form equivalence classes."
- 2025-06-18 03:00 model restates [HoTTification Program Stack v2.0.md line 53] `written:2025-06-18_hottification-program-stack-v2-0:tests-as-witness-paths`: "**Paths as equivalences**: each test forms a witness path between pipeline components."

### L-roundtrip-test (language)

A SAV test asserts that composing the diagnostic after the forward map recovers the identity up to statistical or structural tolerance, an approximate triangle identity.

first 2025-06-18 03:00 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 49] `written:2025-06-18_hottification-program-stack-v2-0:round-trip-identity-up-to-tolerance`: "The SAV test asserts that $G \circ F \approx \text{id}$ up to statistical tolerance or structural equivalence."
- 2025-06-18 03:03 model restates [SAV_kernel_v1.0.md line 10] `written:2025-06-18_sav-kernel-v1-0:approximate-triangle-identity`: "SAV tests assert semantic coherence through approximate triangle identities such as:"

### L-safety-capsules (language)

Local type-safe safety containers (ScientificSafe<T>, Maybe_error<T>), validity or proof capsules, wrap high-risk values.

first 2025-06-18 03:00 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 19] `written:2025-06-18_hottification-program-stack-v2-0:safety-containers-validity-capsules`: "**ScientificSafe\<T>, Maybe\_error\<T>** | Local safety containers, validity capsules"
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 24] `written:2025-06-18_ho-ttification-manifesto-v-2:proof-oriented-encapsulation`: "Introduce `ScientificSafe<T>`, `Maybe_error<T>` wrappers"
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 35] `written:2025-06-18_ho-ttification-manifesto-v-2-1:proof-capsules`: "**Proof Capsules** — local type-safe wrappers (e.g. `ScientificSafe<T>`)"

### L-sav-framework (language)

Semantic Adjoint Verification (SAV) is a lightweight diagnostic framework for inference engines, derived from adjoint functors, that validates coherence via approximate triangle identities and acts as a pre-formal safety envelope or semantic pre-type system.

first 2025-06-18 03:00 by model; 6 rows, 6 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 16] `written:2025-06-18_hottification-program-stack-v2-0:semantic-adjoint-verification-as-soft-test-layer`: "**Semantic Adjoint Verification (SAV)** | Soft semantic test layer — CLI-integrated verification via adjunctions"
- 2025-06-18 03:03 model restates [SAV_kernel_v1.0.md line 8] `written:2025-06-18_sav-kernel-v1-0:sav-semantic-adjoint-verification`: "A structured verification framework for scientific inference engines that derives test protocols from adjoint diagnostic pairs."
- 2025-06-18 03:03 model restates [SAV_kernel_v1.0.md line 18] `written:2025-06-18_sav-kernel-v1-0:verification-compressed-to-minimal-diagnostic-suite`: "SAV compresses verification into a minimal suite of epistemically meaningful tests, serving as a pre-formal safety envelope in HoTTified inference systems."
- 2025-06-18 03:08 model restates [Deployment Plan and Paper Kernel.md line 66] `written:2025-06-18_deployment-plan-and-paper-kernel:sav-semantic-adjoint-verification`: "We introduce **Semantic Adjoint Verification (SAV)** — a lightweight, semantically structured diagnostic framework for inference engines. Derived from adjoint…"
- 2025-06-18 03:08 model restates [Deployment Plan and Paper Kernel.md line 49] `written:2025-06-18_deployment-plan-and-paper-kernel:semantic-pre-type-system`: "It operationalizes homotopical reasoning in real systems by embedding structured round-trip diagnostics, creating a *semantic pre-type system*."
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 33] `written:2025-06-18_ho-ttification-manifesto-v-2-1:sav-semantic-adjoint-verification`: "**SAV (Semantic Adjoint Verification)** — smart tests derived from adjunctions"

### L-structure-before-proof (language)

Epistemic and semantic structure and soft safety are established before hard type checking or proofs; diagnostics defend correctness until proofs exist and later become type-inhabiting witnesses.

first 2025-06-18 03:00 by model; 8 rows, 8 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:00 model states [HoTTification Program Stack v2.0.md line 66] `written:2025-06-18_hottification-program-stack-v2-0:proof-proxy-bridging-empirical-to-formal`: "Proof proxy | Bridges empirical outputs to formal proofs"
- 2025-06-18 03:00 model restates [HoTTification Program Stack v2.0.md line 54] `written:2025-06-18_hottification-program-stack-v2-0:soft-homotopy-before-hard-typing`: "**Soft homotopy layer**: semantic contracts before hard type checking."
- 2025-06-18 03:03 model restates [SAV_kernel_v1.0.md line 22] `written:2025-06-18_sav-kernel-v1-0:bridge-empirical-to-type-theoretic-proof`: "**Bridges:** Empirical tests → structural diagnostics → future type-theoretic proof wrappers."
- 2025-06-18 03:08 model restates [Deployment Plan and Paper Kernel.md line 15] `written:2025-06-18_deployment-plan-and-paper-kernel:epistemic-firewall`: "Semantic coherence before formal structure | **SAV** | Epistemic firewall via diagnostic adjunctions"
- 2025-06-18 03:08 model refines [Deployment Plan and Paper Kernel.md line 127] `written:2025-06-18_deployment-plan-and-paper-kernel:tests-as-type-inhabiting-witnesses`: "Once full type structure is ready, SAV tests become **type-inhabiting witnesses**."
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 34] `written:2025-06-18_ho-ttification-manifesto-v-2:soft-safety-before-hard-proof`: "**Soft safety before hard proof**: Use diagnostics to defend correctness even when proofs are not yet constructed."
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 31] `written:2025-06-18_ho-ttification-manifesto-v-2:structure-before-syntax`: "**Structure before syntax**: Embed epistemic logic even before full type safety."
- 2025-06-18 03:32 model refines [ho_ttification_manifesto_v_2 (1).md line 47] `written:2025-06-18_ho-ttification-manifesto-v-2-1:type-safety-as-consequence-of-epistemic-clarity`: "Move toward type safety as a *natural consequence* of epistemic clarity"

### L-tests-are-morphisms (language)

Tests are not arbitrary unit tests or patches but morphisms and triangle identities encoding epistemic contracts derived from the engine's own structure, so semantic structure matters more than coverage.

first 2025-06-18 03:03 by model; 4 rows, 4 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:03 model states [SAV_kernel_v1.0.md line 50] `written:2025-06-18_sav-kernel-v1-0:tests-as-epistemic-contracts-from-engine-structure`: "SAV tests are not arbitrary unit tests: they encode epistemic contracts derived from the structure of the engine itself."
- 2025-06-18 03:08 model refines [Deployment Plan and Paper Kernel.md line 118] `written:2025-06-18_deployment-plan-and-paper-kernel:epistemic-compression`: "Why semantic structure matters more than test coverage."
- 2025-06-18 03:13 model restates [ho_ttification_manifesto_v_2.md line 32] `written:2025-06-18_ho-ttification-manifesto-v-2:tests-as-morphisms`: "**Tests as morphisms**: Each CLI command is a functor; each test a triangle identity."
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 23] `written:2025-06-18_ho-ttification-manifesto-v-2-1:tests-as-morphisms`: "**Tests are not patches — they are morphisms.**"

### L-hottification-roadmap (method)

HoTTification is a staged, recursive, incremental and convergent program that is both a long-term type-theoretic, compositional, homotopical foundation and a practical roadmap usable before full formalization.

first 2025-06-18 03:08 by model; 4 rows, 4 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:08 model states [Deployment Plan and Paper Kernel.md line 66] `written:2025-06-18_deployment-plan-and-paper-kernel:hottification-phased-roadmap`: "a roadmap for transforming scientific software into epistemically safe, type-structured engines."
- 2025-06-18 03:13 model refines [ho_ttification_manifesto_v_2.md line 12] `written:2025-06-18_ho-ttification-manifesto-v-2:foundation-and-roadmap-together`: "A long-term type-theoretic foundation for inference pipelines."
- 2025-06-18 03:32 model refines [ho_ttification_manifesto_v_2 (1).md line 38] `written:2025-06-18_ho-ttification-manifesto-v-2-1:homotopical-program-recursive-incremental`: "This is not a waterfall. This is a homotopical program: recursive, incremental, convergent."
- 2025-06-18 03:32 model refines [ho_ttification_manifesto_v_2 (1).md line 15] `written:2025-06-18_ho-ttification-manifesto-v-2-1:type-theoretic-compositional-homotopical-foundation`: "The correct long-term foundation is type-theoretic, compositional, and homotopical."

### L-modelgraph-parammanager-separation (language)

ModelGraph and ParameterManager structures are cleanly separated.

first 2025-06-18 03:13 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:13 model states [ho_ttification_manifesto_v_2.md line 23] `written:2025-06-18_ho-ttification-manifesto-v-2:internal-modularization`: "Clean separation of ModelGraph and ParameterManager structures"

### L-program-goal-elevate-engines (method)

The program transforms scientific inference engines from empirically working black boxes into epistemically structured, formally safe systems, starting from the empirical systems themselves, a semantic elevation rather than a rewrite.

first 2025-06-18 03:13 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:13 model states [ho_ttification_manifesto_v_2.md line 9] `written:2025-06-18_ho-ttification-manifesto-v-2:hottification-core-mission`: "To transform scientific inference engines from empirically functional black boxes into **epistemically structured, formally safe systems** using the principles…"
- 2025-06-18 03:13 model refines [ho_ttification_manifesto_v_2.md line 57] `written:2025-06-18_ho-ttification-manifesto-v-2:semantic-elevation-not-rewrite`: "The HoTTification Program is not a rewrite — it is a **semantic elevation.**"
- 2025-06-18 03:13 model refines [ho_ttification_manifesto_v_2.md line 50] `written:2025-06-18_ho-ttification-manifesto-v-2:start-from-empirical-systems`: "We do not start from pure logic. We start from empirical systems — but we structure them epistemically, functorially, and eventually formally."

### L-reproducibility-formal (other)

The reproducibility crisis is a lack of structural verification rather than a sociological issue, and reproducibility is a formal property.

first 2025-06-18 03:13 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:13 model states [ho_ttification_manifesto_v_2.md line 35] `written:2025-06-18_ho-ttification-manifesto-v-2:reproducibility-as-formal-problem`: "The reproducibility crisis is not a sociological issue but a lack of structural verification."
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 21] `written:2025-06-18_ho-ttification-manifesto-v-2-1:reproducibility-as-formal-property`: "**Reproducibility is a formal property.**"

### L-code-encodes-epistemology (other)

Scientific software should encode its epistemic structure, not just its algorithms; it is executable epistemology rather than engineering.

first 2025-06-18 03:32 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:32 model states [ho_ttification_manifesto_v_2 (1).md line 14] `written:2025-06-18_ho-ttification-manifesto-v-2-1:code-encodes-epistemic-structure`: "Scientific code should encode its **epistemic structure**, not just its algorithms."
- 2025-06-18 03:32 model restates [ho_ttification_manifesto_v_2 (1).md line 25] `written:2025-06-18_ho-ttification-manifesto-v-2-1:software-as-executable-epistemology`: "**Scientific software is not engineering — it is executable epistemology.**"

### L-safety-semantic-zone (language)

Safety is a constructible semantic zone rather than an afterthought.

first 2025-06-18 03:32 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:32 model states [ho_ttification_manifesto_v_2 (1).md line 24] `written:2025-06-18_ho-ttification-manifesto-v-2-1:safety-as-constructible-semantic-zone`: "**Safety is not an afterthought — it is a constructible semantic zone.**"

### L-semantic-interfaces (language)

Semantic interfaces are DSLs that expose structural contracts.

first 2025-06-18 03:32 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:32 model states [ho_ttification_manifesto_v_2 (1).md line 34] `written:2025-06-18_ho-ttification-manifesto-v-2-1:semantic-interfaces-structural-contracts`: "**Semantic Interfaces** — DSLs that expose structural contracts"

### L-semantic-verification (method)

Verification of scientific code should be semantic, not merely syntactic.

first 2025-06-18 03:32 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-18

- 2025-06-18 03:32 model states [ho_ttification_manifesto_v_2 (1).md line 13] `written:2025-06-18_ho-ttification-manifesto-v-2-1:semantic-not-syntactic-verification`: "Verification must become **semantic**, not just syntactic."

### L-argument-domains (language)

Each argument of each function gets a Domain from which argument sets can be sampled for snapshots; a natural place to store parameter min/max is the ParameterPriors files.

first 2025-09-27 18:31 by Luciano; 2 rows, 2 witnesses, 1 days, last 2025-09-27

- 2025-09-27 18:31 Luciano states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 4] `dialogue:01998d16:domain-as-generator-and-validator-per-argument`: "we can do is to define Domains for each argument of each function and run randomly select a set of arguments for a snapshot."
- 2025-09-27 19:42 Luciano refines [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 26] `dialogue:01998d16:domains-via-parameter-priors-min-max-columns`: "A natural place for that is the ParameterPriors files, we can add two more columns for min and max, for instance. But that implies modifying ParametersDistribu…"

### L-snapshot-first (method)

Before committing to tests and decisions, do the simpler thing: record snapshots, compare results outside the system, and study them to decide which tests to run.

first 2025-09-27 18:31 by Luciano; 1 rows, 1 witnesses, 1 days, last 2025-09-27

- 2025-09-27 18:31 Luciano states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 4] `dialogue:01998d16:snapshot-before-testing`: "before testing we can do something simpler and without adding decisions. We can do a snapshot recording and outside macro_dr comparing results. ... Then I can…"

### L-function-contract (language)

A FunctionContract bundles Domains, Postconditions and metadata attached to a function (the full contract, beyond a bare postcondition), with testing introduced in incremental phases.

first 2025-09-27 18:32 by model; 3 rows, 3 witnesses, 2 days, last 2026-09-13; taken up by Luciano 2026-09-13

- 2025-09-27 18:32 model states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 5] `dialogue:01998d16:contract-bundles-domains-postconditions-metadata`: "Contract = {Domains, Postconditions, metadata} attached to a function."
- 2025-09-27 18:50 model refines [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 9] `dialogue:01998d16:functioncontract-beyond-postcondition`: "`Postcondition<Out, Args...>` is just \u201cwhat must hold after a call.\u201d `FunctionContract<Out, Args...>` is the full contract for a function"
- 2026-09-13 08:49 Luciano restates [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 8] `dialogue:f16636f6:funciones-con-pre-y-post-condiciones`: "las funciones para mi deberian tener a su vez bueno, pre y post conditions"

### L-oracle (language)

An oracle supplies an external reference behavior to compare the implementation against, catching semantic drift that an intrinsic postcondition cannot when the exact expected value is unknown.

first 2025-09-27 18:55 by model; 3 rows, 3 witnesses, 1 days, last 2025-09-27

- 2025-09-27 18:55 model states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 13] `dialogue:01998d16:oracle-as-reference-behavior`: "An oracle provides a \u201creference behavior\u201d to compare against the implementation under test."
- 2025-09-27 19:01 Luciano questions [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 15] `dialogue:01998d16:oracle-is-postconditions-on-steroids`: "so it is another name for postconditions on steroids?"
- 2025-09-27 19:01 model corrects [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 17] `dialogue:01998d16:oracle-vs-postcondition-source-of-truth`: "Postconditions are intrinsic predicates; oracles rely on an external reference or relation."

### L-oracle-unify (language)

In abstract terms an oracle, like a postcondition, is a function of arguments and output evaluating to Maybe_error<bool>, though for oracles this is leaky and a richer tri-state verdict is needed.

first 2025-09-27 19:03 by Luciano; 2 rows, 2 witnesses, 1 days, last 2025-09-27

- 2025-09-27 19:03 Luciano states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 19] `dialogue:01998d16:both-are-functions-of-args-and-output-to-maybe-error-bool`: "but in abstract terms it is still a function of arguments and output that evaluates to a Maybe_error<bool> ."
- 2025-09-27 19:04 model refines [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 21] `dialogue:01998d16:unifying-as-predicate-is-leaky-for-oracles`: "you can unify them as a predicate over `(Out, Args...)` returning `Maybe_error<bool>`. But it\u2019s a leaky abstraction for oracles."

### L-overload-resolution (language)

Overloading is resolved by storing a vector of compilers per identifier and trying the overloads in order.

first 2025-09-27 22:40 by Luciano; 1 rows, 1 witnesses, 1 days, last 2025-09-27

- 2025-09-27 22:40 Luciano states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 257] `dialogue:01998d16:dsl-overloading-by-vector-of-compilers`: "we need to change the logic so the dsl can resolve overloading, ... change ... m_func; ... to ... std::vector<std::unique_ptr<base_function_compiler<Lexer, Com…"

### L-serialization-invertible (language)

A serialization is legitimate only if invertible: to_json followed by from_json is the identity, a law the representation of a value must satisfy.

first 2025-09-28 11:00 by Luciano; 1 rows, 1 witnesses, 1 days, last 2025-09-28

- 2025-09-28 11:00 Luciano states [2025-09-27_01998d16_i-want-start-with-the-implementation-of.md turn 558] `dialogue:01998d16:serialization-must-be-reversible`: "a very important principle here is reversibility to_json |> from_json == Id meaning I have to recover everything from the json, otherwise it does not fullfil i…"

### L-reasonable-then-wild (method)

Luciano's method: first work out the reasonable version, then look for the wild one; here the wild move is to invent Luthier directly rather than through the other projects.

first 2026-05-26 12:32 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-26

- 2026-05-26 12:32 Luciano states [WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:00]] `day:2026-05-26:razonar-primero-despues-la-locura`: "yo pienso todo para ser razonable y después busco la locura"

### L-types-as-concepts (language)

Types in Luthier are concepts, types as propositions (Curry-Howard), and types include functions and higher-order functions, so code can be its own proof.

first 2026-05-26 12:33 by Luciano; 11 rows, 10 witnesses, 3 days, last 2026-08-31

- 2026-05-26 12:33 Luciano states [WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:38]] `day:2026-05-26:tipos-como-conceptos-y-proposiciones`: "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen también funciones, funciones y funciones de orden superior"
- 2026-05-26 12:33 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [00:38]] `note:2026-05-26T12.32.24:tipos-como-proposiciones`: "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen también funciones, funciones y funciones de orden superior"
- 2026-05-26 12:33 model refines [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 2] `dialogue:20260526T1233:curry-howard-tipos-dependientes`: "estás tocando la teoría de tipos dependientes ... Esto permite que el código sea su propia demostración matemática, validando la lógica antes de ejecutar una s…"
- 2026-05-26 12:33 Luciano restates [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1] `dialogue:20260526T1233:luthier-tipos-como-proposiciones`: "Luthier sería una especie de lenguaje de programación donde los tipos tienen que ser conceptos, o sea, tipos como proposiciones, y los tipos incluyen también f…"
- 2026-05-29 14:04 model refines [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 4] `dialogue:20260529T1400:codigo-es-demostracion`: "al habilitar que las funciones "tiren tipos", hacés que el propio compilador de Luthier sea un demostrador matemático. El código y la demostración matemática d…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:tipos-como-proposiciones`: "tipos tienen que ser conceptos, o sea, tipos como proposiciones, y los tipos incluyen también funciones, no funciones y funciones de orden superior"
- ... 3 more rows
- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:tipos-como-proposiciones`: "Luthier es un lenguaje (o metalenguaje) que inventás donde los tipos son proposiciones: pertenecer a un tipo significa afirmar algo garantizado sobre el valor."
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:tipos-como-proposiciones`: "Luthier es un lenguaje (o metalenguaje) que inventás donde los tipos son proposiciones: pertenecer a un tipo significa afirmar algo garantizado sobre el valor."

### L-cross-language (language)

Luthier is not tied to C++ but a language-agnostic pseudo-language, cross-language rather than cross-compiler, implementable in different languages (PyLuthier, RLuthier, CLuthier) transformable between each other.

first 2026-05-26 12:33 by Luciano; 10 rows, 6 witnesses, 3 days, last 2026-08-31

- 2026-05-26 12:33 Luciano states [WhatsApp Ptt 2026-05-26 at 12.32.24.md [01:04]] `note:2026-05-26T12.32.24:lenguaje-no-atado-a-cpp`: "la idea de que Luthier no sea estrictamente en C++ sino que sea como una especie de pseudo lenguaje que podría ser implementado en distintos lenguajes"
- 2026-05-26 12:33 Luciano restates [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1] `dialogue:20260526T1233:luthier-pseudo-lenguaje-cross-lenguaje`: "Luthier debería ser como una cosa que es como un lenguaje no es cross compiler sino es directamente cross lenguaje o sea como que ser un poco agn del lenguaje…"
- 2026-05-26 12:36 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [04:24]] `day:2026-05-26:luthier-agnostico-del-lenguaje`: "no es cross cross este compiler sino directamente cross lenguaje o sea como que sería un poco agnóstico del lenguaje"
- 2026-05-26 12:36 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [04:24]] `note:2026-05-26T12.32.24:cross-lenguaje`: "luthier debería ser como una cosa que es como un lenguaje no es cross compiler sino directamente cross lenguaje o sea como que sería un poco agnóstico del leng…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:cross-lenguaje-no-cross-compiler`: "no es cross compiler sino es directamente cross lenguaje o sea como que ser un poco agn del lenguaje si bien el motor podr estar implementado en alguno de ellos"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:pseudolenguaje-multiimplementable`: "no sea estrictamente en C++, sino que sea como una especie de pseudo lenguaje que podría ser implementado en distintos lenguajes"
- ... 2 more rows
- 2026-08-31 20:00 Luciano restates [WhatsApp Ptt 2026-08-31 at 20.00.05.md [00:08]] `day:2026-08-31:luthier-metalenguaje-con-implementaciones`: "Son especificaciones que podes tener distintas implementaciones de Luthier,"
- 2026-08-31 20:00 Luciano restates [WhatsApp Ptt 2026-08-31 at 20.00.05.md [00:08]] `note:2026-08-31T20.00.05:luthier-como-metalenguaje-con-multiples-implementaciones`: "Son especificaciones que podes tener distintas implementaciones de Luthier, podes tener un Piluthier, Arluthiero o un Luthier CPP, no sé, distintas cosas."

### L-butler-orchestrator (language)

Luthier is a higher-order butler that can run and compile other languages, orchestrate them and compare their outputs, choosing where each computation runs by its complexity.

first 2026-05-26 12:33 by Luciano; 8 rows, 6 witnesses, 4 days, last 2026-08-31

- 2026-05-26 12:33 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1] `dialogue:20260526T1233:luthier-mayordomo-orden-superior`: "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo"
- 2026-05-26 12:35 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [03:34]] `day:2026-05-26:orden-superior-mayordomo-cross-lenguaje`: "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo"
- 2026-05-26 12:35 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [03:34]] `note:2026-05-26T12.32.24:lenguaje-de-orden-superior-mayordomo`: "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo, o sea, también tendrías que poder,…"
- 2026-05-27 13:39 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:00]] `day:2026-05-27:luthier-as-butler-running-and-comparing-programs`: "me lo imagino como un mayordomo que puede correr"
- 2026-05-27 13:39 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:00]] `note:2026-05-27T13.39.04:luthier-como-mayordomo`: "me lo imagino como un mayordomo que puede correr básicamente cualquier programa y que puede comparar los outputs"
- 2026-05-30 18:06 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.01.53.md [04:07]] `note:2026-05-30T18.01.53:facilidad-para-ejecutar-otros-programas`: "tener una facilidad, que también eso tiene que ser ejecutado, tiene que ser implementado en algún lenguaje, que vos puedas correr fácilmente otros programas"
- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:lenguaje-puente-no-ejecutor`: "Luthier es agnóstico del lenguaje: un \"mayordomo\" que orquesta y anota código de Python, C++, R, Bash ... La ejecución se delega; lo propio de Luthier es la…"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:lenguaje-puente-no-ejecutor`: "Luthier es agnóstico del lenguaje: un \"mayordomo\" que orquesta y anota código de Python, C++, R, Bash (PyLuthier, RLuthier, LuthierCPP). La ejecución se dele…"

### L-complexity-hard-problem (language)

The central hard problem is building the heuristics that anticipate a priori the compute time and memory of an implementation.

first 2026-05-26 12:33 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-26

- 2026-05-26 12:33 model states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 2] `dialogue:20260526T1233:desafio-heuristicas-de-estimacion`: "El mayor reto de Luthier no será la traducción de lenguajes, sino la construcción de las heurísticas de evaluación"

### L-declarative-and-optimizer (language)

Luthier is at once a declarative language and an optimization tool: you declare what you want with formulas and the engine openly shuffles ways to implement it, estimating each.

first 2026-05-26 12:33 by Luciano; 5 rows, 4 witnesses, 2 days, last 2026-05-29

- 2026-05-26 12:33 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1] `dialogue:20260526T1233:luthier-declarativo-y-optimizador`: "que Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización. O sea, que vos declares lo que querés hacer,…"
- 2026-05-26 12:34 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [01:52]] `day:2026-05-26:declarativo-y-herramienta-de-optimizacion`: "que el UTIER sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización"
- 2026-05-26 12:34 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [01:52]] `note:2026-05-26T12.32.24:declarativo-mas-optimizacion`: "que el Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización. O sea, que vos declares lo que querés hac…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:declarativo-mas-optimizador`: "Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:declarativo-mas-optimizacion`: "que Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización"

### L-declarative-executive-map (language)

Luthier is a map between a declarative language and an executive language that runs things, with each execution carrying a cost estimation.

first 2026-05-26 12:33 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-26

- 2026-05-26 12:33 Luciano refines [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1] `dialogue:20260526T1233:luthier-mapa-declarativo-a-ejecutivo`: "sería una especie de que Luthier permita digamos, ser un mapa entre un lenguaje declarativo y un lenguaje ejecutivo que ser el que ejecuta las cosas pero a la…"
- 2026-05-26 12:35 Luciano states [WhatsApp Ptt 2026-05-26 at 12.32.24.md [02:51]] `note:2026-05-26T12.32.24:mapa-declarativo-ejecutivo`: "que Luthier permita, digamos, ser un mapa entre un lenguaje declarativo y un lenguaje ejecutivo que sería el que ejecuta las cosas"

### L-paths (language)

One function can be implemented in many ways, the paths, each with its own precision, speed and other estimated properties, evaluated as a multidimensional optimization over an AST.

first 2026-05-26 12:33 by Luciano; 10 rows, 9 witnesses, 4 days, last 2026-09-13

- 2026-05-26 12:33 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 1] `dialogue:20260526T1233:luthier-paths-con-precision-y-velocidad`: "una funci esta funci puede ser implementada de muchas maneras, son los distintos paths y cada forma tiene una precisión y una velocidad"
- 2026-05-26 12:33 model refines [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 2] `dialogue:20260526T1233:orquestador-ast-multidimensional`: "Luthier, en cambio, actuaría construyendo un **Árbol de Sintaxis Abstracta (AST)** a partir de tu declaración, para luego evaluar múltiples \"caminos\" (paths)…"
- 2026-05-26 12:33 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [01:26]] `day:2026-05-26:paths-distintas-implementaciones`: "tiene una función, esta función puede ser implementada de muchas maneras, son los distintos paths y cada forma tiene una precisión y una velocidad"
- 2026-05-26 12:33 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [01:26]] `note:2026-05-26T12.32.24:paths-precision-velocidad`: "tiene una función, esta función puede ser implementada de muchas maneras, son los distintos paths y cada forma tiene una precisión y una velocidad"
- 2026-05-29 14:00 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 1] `dialogue:20260529T1400:implementaciones-como-paths`: "nosotros abstraemos el concepto de implementación a través de los paths, algo así. yo tengo distintas implementaciones y veo la equivalencia entre implementaci…"
- 2026-05-29 14:00 Luciano restates [WhatsApp Ptt 2026-05-29 at 13.57.41.md [03:18–03:38]] `note:2026-05-29T13.57.41:paths-como-abstracción-de-implementación`: "abstraemos el concepto de implementación a través de los paths… yo tengo distintas implementaciones y veo la equivalencia entre implementaciones"
- ... 2 more rows
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:paths-y-comparacion-de-caminos`: "una misma función tiene muchas implementaciones posibles (distintos paths), cada una con su precisión, su tiempo de cómputo, su memoria, su lugar de ejecución.…"
- 2026-09-13 08:50 model restates [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:implementaciones-multiples-de-un-tipo-de-funcion`: "implementaciones múltiples del mismo tipo de función, comparadas por desempeño documentado"

### L-cost-estimation-per-path (language)

Each execution path carries an estimation of characteristics: above all compute time, but also error, memory, and where it runs.

first 2026-05-26 12:35 by Luciano; 4 rows, 3 witnesses, 3 days, last 2026-08-31

- 2026-05-26 12:35 Luciano states [WhatsApp Ptt 2026-05-26 at 12.32.24.md [03:10]] `day:2026-05-26:estimacion-por-paso-tiempo-memoria-lugar`: "Vos para cada pas de ejecución tenés dos cosas. Tenés una estimación de distintas características, que es, por ejemplo, eso, el error y más que nada el tiempo…"
- 2026-05-26 12:35 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.32.24.md [03:10]] `note:2026-05-26T12.32.24:propiedades-estimadas-por-path`: "para cada path de ejecución tenés dos cosas. Tenés una estimación de distintas características, que es, por ejemplo, eso, el error y más que nada el tiempo de…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:estimacion-abierta-por-ejecucion`: "para cada ejecuci ten dos cosas ten una estimaci de distintas caracter que es por ejemplo eso, el error y más que nada el tiempo de cómputo, pero también puede…"
- 2026-08-31 19:54 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [06:06]] `note:2026-08-31T19.48.17:velocidad-del-codigo`: "También tenía el tema de la velocidad, el código"

### L-explore-solutions (language)

The purpose is to let the user find different solutions to their problem and compare the estimated complexity of each way of executing it.

first 2026-05-26 12:37 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-26

- 2026-05-26 12:37 Luciano states [WhatsApp Ptt 2026-05-26 at 12.32.24.md [05:28]] `note:2026-05-26T12.32.24:explorar-soluciones-y-complejidad`: "que vos puedas encontrar la mejor solución para tu problema o, digamos, no sé si la mejor, pero bueno, distintas soluciones para tu problema y bueno, ver cuále…"

### L-bayesian-complexity-estimation (language)

A priori complexity is estimated by a Bayesian strategy: give different algorithms chances at the same task, measure their actual times, and estimate from accumulated experience.

first 2026-05-26 12:41 by Luciano; 4 rows, 4 witnesses, 2 days, last 2026-05-29

- 2026-05-26 12:41 Luciano states [WhatsApp Ptt 2026-05-26 at 12.41.09.md [00:21]] `day:2026-05-26:complejidad-a-priori-estrategia-bayesiana`: "vos obviamente podés, para eso aplicar, digamos, una estrategia bayesiana"
- 2026-05-26 12:41 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [00:28]] `note:2026-05-26T12.41.09:estimacion-bayesiana-de-complejidad`: "puede ser cualquiera y bueno, voy dándole oportunidad a distintos algoritmos para hacer lo mismo y después voy estimando los tiempos que toman para problemas p…"
- 2026-05-26 12:42 Luciano restates [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 3] `dialogue:20260526T1233:estimacion-bayesiana-empirica-del-costo`: "vos obviamente podés, para eso, aplicar, digamos, una estrategia bayesiana ... voy dándole oportunidad a distintos algoritmos para hacer lo mismo, y después vo…"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:estrategia-bayesiana-base-de-datos`: "sería como una base de datos que dice: bueno, yo para esta función con estos datos iniciales y esta escala, yo usando este algoritmo tardé tanto tiempo y tuve…"

### L-performance-database (language)

Luthier keeps a database recording, for each function with given initial data, scale and algorithm, the time taken and precision achieved (and memory, CPUs, machine, range of results), known because actually measured.

first 2026-05-26 12:42 by Luciano; 6 rows, 6 witnesses, 3 days, last 2026-05-29

- 2026-05-26 12:42 Luciano states [WhatsApp Ptt 2026-05-26 at 12.41.09.md [01:06]] `day:2026-05-26:base-de-datos-de-corridas`: "lo que tendría que tener Luthier justamente es una base de datos"
- 2026-05-26 12:42 Luciano restates [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 3] `dialogue:20260526T1233:base-de-datos-de-mediciones`: "lo que tendr que tener Luthier justamente es una base de datos ... yo para esta funci con estos datos iniciales y esta escala yo usando este algoritmo tardé ta…"
- 2026-05-26 12:42 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [01:21]] `note:2026-05-26T12.41.09:base-de-datos-de-rendimiento`: "para esta función, con estos datos iniciales, y esta escala, yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión, y como lo sé, bueno, pues lo c…"
- 2026-05-27 13:49 Luciano refines [WhatsApp Ptt 2026-05-27 at 13.49.54.md [00:00]] `note:2026-05-27T13.49.54:luthier-como-base-de-datos-de-corridas`: "Luthier es una base de datos acerca de cómo, de los programas, de cada vez que corren es como que generas un output acerca de cómo corrió, cuántas, digamos, o…"
- 2026-05-27 13:50 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.49.54.md [00:07]] `day:2026-05-27:luthier-as-database-of-program-runs`: "de los programas, de cada vez que corren es como que generas un output acerca de cómo corrió,"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:base-de-datos-de-rendimiento-bayesiana`: "yo para esta funci con estos datos iniciales y esta escala yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión. Y como lo sé, bueno, porque lo c…"

### L-computation-categories (language)

Just as different functions do the same thing, different computations take the same time; the categories or classes of computation must be found so one needn't measure each.

first 2026-05-26 12:42 by Luciano; 5 rows, 5 witnesses, 2 days, last 2026-05-29

- 2026-05-26 12:42 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 3] `dialogue:20260526T1233:clases-de-computo`: "distintas computaciones que tardarían lo mismo para distintos inputs ... lo que habr que empezar a encontrar es eso las categor"
- 2026-05-26 12:44 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [03:34]] `note:2026-05-26T12.41.09:clases-de-computos-equivalentes`: "muchos cómputos parecidos pertenecen a la misma misma clase de cómputos, es decir que digamos o sea lo que habría que empezar a encontrar es eso no, las catego…"
- 2026-05-26 12:45 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [03:55]] `day:2026-05-26:clases-de-computaciones`: "Así como tenemos distintas funciones que hacen lo mismo, tendríamos distintas computaciones que tardarían lo mismo para distintos inputs"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:categorias-de-computo-y-simplificacion-de-inputs`: "vos tenés una simplificación de los inputs que ahí vos lo computás ... podría ser por ejemplo las dimensiones el número de columnas y rod de una matriz"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:categorias-de-computo-y-features`: "lo que habría que empezar a encontrar es eso, las categorías... vos computás el tiempo de cálculo a partir de una simplificación de los inputs"

### L-generalize-database (language)

The performance database must be generalized from point measurements to trends, e.g. estimating a matrix cell from its row and column means or something more sophisticated such as Gaussian Process regression.

first 2026-05-26 12:42 by Luciano; 8 rows, 7 witnesses, 3 days, last 2026-05-30

- 2026-05-26 12:42 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 3] `dialogue:20260526T1233:generalizar-la-base-de-datos`: "una de las herramientas primeras sería cómo generalizar, digamos, los datos que vas obteniendo con casos puntuales ... ahí estoy un poco en pelotas en el senti…"
- 2026-05-26 12:42 model refines [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 4] `dialogue:20260526T1233:surrogate-models-y-proceso-gaussiano`: "Tu idea de estimar el valor de una celda en base al promedio de sus filas y columnas es el primer paso hacia un **Proceso Gaussiano (Gaussian Process Regressio…"
- 2026-05-26 12:42 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [01:42]] `day:2026-05-26:generalizar-la-base-de-datos`: "esa base de datos después la tenés que poder generalizar"
- 2026-05-26 12:42 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [01:42]] `note:2026-05-26T12.41.09:generalizacion-de-la-base-de-datos`: "esa base de datos después la tenés que poder generalizar. Entonces ahí una de las herramientas primeras sería cómo generalizar, digamos, los datos que vas obte…"
- 2026-05-26 12:43 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [02:16]] `note:2026-05-26T12.41.09:matriz-y-estimacion-por-filas-columnas`: "mi matriz son las celdas, yo para cada celda es independiente y bueno, ya está. Pero bueno, si en realidad yo tengo la media de los rows y las columnas, bueno,…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:generalizar-la-matriz-de-medidas`: "yo tengo la media de los rows y las columnas bueno, podría estimar una celda por el promedio de la row y la columna"
- 2026-05-29 15:56 model rejects [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-prediccion-rendimiento-simplificada`: "La idea de "factorización de matrices" para predecir tiempos es una simplificación extrema"
- 2026-05-30 18:16 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.16.35.md [00:00]] `note:2026-05-30T18.16.35:funtores-de-olvido`: "Después está el tema de los functores de olvido"

### L-self-modeling-estimation (language)

The time and precision estimation functions are themselves modeled by Luthier (lutearized) and used by Luthier itself, making the system metacircular.

first 2026-05-26 12:42 by model; 5 rows, 5 witnesses, 2 days, last 2026-05-29; taken up by Luciano 2026-05-26

- 2026-05-26 12:42 model refines [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 4] `dialogue:20260526T1233:arquitectura-metacircular`: "Esto convierte a Luthier en un sistema **metacircular**. Las funciones predictivas ... son, en sí mismas, proposiciones con un costo"
- 2026-05-26 12:42 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 3] `dialogue:20260526T1233:lutearizar-las-funciones-de-estimacion`: "la idea es que vos lutearizás las funciones de estimación del tiempo de cómputo, de la precisión de cómputo"
- 2026-05-26 12:44 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [02:56]] `day:2026-05-26:funciones-de-modelado-usadas-por-luthier`: "vos tenés que modelar el funcionamiento de cada una de estas cosas y bueno, ahí es donde empieza a ver funciones que son las funciones de modelado de esto que…"
- 2026-05-26 12:44 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [03:05]] `note:2026-05-26T12.41.09:funciones-de-modelado-como-herramientas-del-sistema`: "empieza a ver funciones que son las funciones de modelado de esto que también las vas a utilizar, o sea la idea es que vos lo utilizas las funciones de estimac…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:lutherizar-las-funciones-de-estimacion`: "vos lutearizás las funciones de estimación del tiempo de cómputo, de la precisión de cómputo"

### L-time-from-input-features (language)

Compute time is estimated from a simplification of the inputs, the most predictive features (e.g. a matrix's rows and columns); some functions are input-independent, others not.

first 2026-05-26 12:42 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-05-26

- 2026-05-26 12:42 Luciano states [2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md turn 3] `dialogue:20260526T1233:simplificacion-de-los-inputs`: "vos computás el tiempo de cálculo a partir de una simplificación de los incómodos, podría ser por ejemplo las dimensiones el número de columnas y rod de una ma…"
- 2026-05-26 12:45 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [04:11]] `note:2026-05-26T12.41.09:independencia-de-inputs`: "puede ser que hay funciones que son independientes de los inputs, por ejemplo. Otras, pero cuando dependen de los inputs, obviamente, ahí vos ves qué caracterí…"
- 2026-05-26 12:45 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [04:26]] `note:2026-05-26T12.41.09:simplificacion-de-inputs-como-predictores`: "vos lo que tendrías que tener es vos tenés, digamos, una simplificación de los inputs que ahí vos lo computás. O sea, vos computás el tiempo de cálculo a parti…"
- 2026-05-26 12:45 Luciano restates [WhatsApp Ptt 2026-05-26 at 12.41.09.md [04:37]] `day:2026-05-26:dependencia-de-inputs-y-simplificacion`: "vos computás el tiempo de cálculo a partir de una simplificación de los inputs"

### L-compose-compare-paths (language)

Luthier composes the output of one program into another and compares two alternative paths that do the same thing to see they are equivalent, with format conversion stages at the start and end.

first 2026-05-27 13:39 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:39 Luciano states [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:26]] `note:2026-05-27T13.39.04:composición-entrada-salida`: "Luthier lo que tendría que hacer es poder componer la entrada y salida de un programa y otro"
- 2026-05-27 13:39 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:44]] `note:2026-05-27T13.39.04:equivalencia-de-caminos`: "vos comparás dos caminos para hacer lo mismo"
- 2026-05-27 13:39 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:47]] `day:2026-05-27:compose-input-output-and-see-equivalence-of-paths`: "dos caminos para hacer lo mismo"

### L-verifiability (language)

Luthier must verify that a function is correct (verifiability), which together with equivalence forms its minimal elements.

first 2026-05-27 13:39 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:39 Luciano states [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:52]] `day:2026-05-27:verifiability-of-functions`: "que una función es correcta"
- 2026-05-27 13:39 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [00:52]] `note:2026-05-27T13.39.04:verificabilidad-de-funciones`: "comprobas que una función es correcta, es la idea de verificabilidad, es como una especie de verificabilidad"

### L-two-layers (language)

Luthier has two layers: a first with equivalences and verifiability, and a second that measures time, complexity, resources and success/failure and lets you pick the faster of two equivalent paths.

first 2026-05-27 13:40 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:40 Luciano states [WhatsApp Ptt 2026-05-27 at 13.39.04.md [01:04]] `note:2026-05-27T13.39.04:decoración-con-tiempo-y-complejidad`: "después poder determinar los tiempos que tardan en ejecutarse algo y que dos caminos son equivalentes con distintos recorridos"
- 2026-05-27 13:43 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [03:56]] `day:2026-05-27:time-complexity-and-resources-as-a-second-layer`: "la posibilidad de decorar con tiempo y con complejidad y esas cosas"
- 2026-05-27 13:43 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [04:18]] `note:2026-05-27T13.39.04:capas-del-lenguaje`: "Pero eso me parece que es como de la segunda capa. La primera capa sería, bueno, eso."

### L-primitives-or-coordinate (language)

Open question whether Luthier needs primitive functions or merely coordinates functions existing outside it, so perhaps only the identity is internal (A∘B = identity makes A the inverse of B).

first 2026-05-27 13:41 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-05-30

- 2026-05-27 13:41 Luciano states [WhatsApp Ptt 2026-05-27 at 13.39.04.md [02:43]] `note:2026-05-27T13.39.04:funciones-externas-vs-primitivas`: "la pregunta es si vos tenés que tener funciones primitivas o simplemente vos coordenás las funciones existentes por fuera de Luthier"
- 2026-05-27 13:42 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [03:01]] `day:2026-05-27:primitives-or-only-the-identity`: "bueno, A no sé lo que es A, pero yo compongo A y B, claro, y me da la identidad, por ejemplo."
- 2026-05-30 18:08 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:56]] `note:2026-05-30T18.07.21:identidad-o-equivalencia-como-punto-de-partida`: "solamente que puedas empezar solo con la identidad de algún principio de equivalencia"

### L-minimal-bridge-language (language)

Luthier should be minimal, with the fewest possible native components, essentially a bridge language between other languages.

first 2026-05-27 13:42 by Luciano; 4 rows, 4 witnesses, 2 days, last 2026-08-31

- 2026-05-27 13:42 Luciano states [WhatsApp Ptt 2026-05-27 at 13.39.04.md [03:22]] `note:2026-05-27T13.39.04:minimalismo-de-primitivas`: "yo lo que querría es que Luthier sea mínimo, o sea, que tenga los mínimos componentes nativos posibles"
- 2026-05-27 13:42 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [03:27]] `day:2026-05-27:minimal-bridge-language`: "que tenga los mínimos componentes nativos posibles, cosa que básicamente sea así, un lenguaje puente"
- 2026-05-27 13:42 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [03:33]] `note:2026-05-27T13.39.04:lenguaje-puente`: "que básicamente sea así, un lenguaje puente, ¿no? Lenguaje puente entre otros lenguajes"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:minimo-y-cuantificadores-ciudadanos`: "Tiene que ser mínimo (poquísimos tipos nativos, autoextensible, ejecutable con lápiz y papel) y los cuantificadores lógicos (para todo, existe) y las ideas mis…"

### L-delegate-execution (language)

Luthier could delegate execution entirely and keep only verification, as an extreme of minimalism.

first 2026-05-27 13:43 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:43 Luciano states [WhatsApp Ptt 2026-05-27 at 13.39.04.md [04:35]] `day:2026-05-27:delegate-execution-keep-only-verification`: "Uno podría decir, bueno, a ver si yo hasta puedo delegar la parte de ejecución"
- 2026-05-27 13:43 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.39.04.md [04:35]] `note:2026-05-27T13.39.04:delegación-de-ejecución`: "a ver si yo hasta puedo delegar la parte de ejecución y que lo único que haga sea la verificación"

### L-synthesize-run-info (language)

A central challenge is synthesizing the accumulated run information so it doesn't grow monstrous and paralyzing.

first 2026-05-27 13:50 by Luciano; 4 rows, 4 witnesses, 3 days, last 2026-08-31

- 2026-05-27 13:50 Luciano states [WhatsApp Ptt 2026-05-27 at 13.49.54.md [00:32]] `note:2026-05-27T13.49.54:desafio-sintesis-de-informacion-acumulada`: "el problema es cómo vos la sintetizás a la larga, porque puede ser, digamos, como una cosa monstruosa, ¿no? de cómo vos tenés que ir sintetizando esa informaci…"
- 2026-05-27 13:50 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.49.54.md [00:46]] `day:2026-05-27:synthesizing-run-data`: "de cómo vos tenés que ir sintetizando esa información para que no se vea paralizante."
- 2026-05-30 18:17 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.16.35.md [00:56]] `note:2026-05-30T18.16.35:sintesis-de-informacion`: "ese análisis sintético, la síntesis, eso es un tema muy apasionante y bueno, sí, claramente es la clave de todo, hacerlo bien"
- 2026-08-31 20:10 model questions [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:lo-abierto`: "Cómo estimar complejidad a priori, cómo sintetizar la base de datos de corridas sin que sea monstruosa, qué functores de olvido usar para qué, si HoTT modela o…"

### L-summary-bigger-than-data (other)

A model or summary can end up bigger than the original data it summarizes, like there being more interpretations of Borges than Borges.

first 2026-05-27 13:51 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:51 Luciano states [WhatsApp Ptt 2026-05-27 at 13.51.41.md [00:12]] `note:2026-05-27T13.51.41:resumen-puede-ser-mayor-que-datos`: "a veces es que el resumen es más grande que el texto [...] como hay más interpretaciones de los libros de Borges que los libros de Borges en sí"

### L-model-of-computation (language)

Luthier contains a model of the world, a model of computation continually tested and simplified and kept active through selective forgetting or aggregation, justified by use for predicting or interpreting a particular case.

first 2026-05-27 13:52 by Luciano; 4 rows, 3 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:52 Luciano states [WhatsApp Ptt 2026-05-27 at 13.51.51.md [00:11]] `day:2026-05-27:luthier-as-model-of-the-world`: "Porque vos tenés un modelo de la computación que vas probando, ¿no?"
- 2026-05-27 13:52 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.51.51.md [00:11]] `note:2026-05-27T13.51.51:modelo-del-mundo`: "vos tenés un modelo de la computación que vas probando, ¿no? Y vas simplificando."
- 2026-05-27 13:52 Luciano refines [WhatsApp Ptt 2026-05-27 at 13.51.41.md [00:29]] `note:2026-05-27T13.51.41:modelo-orientado-a-caso-particular`: "vos querés una interpretación para un caso particular, o sea, para poder predecir, para poder interpretar"
- 2026-05-27 13:52 Luciano refines [WhatsApp Ptt 2026-05-27 at 13.51.51.md [00:32]] `note:2026-05-27T13.51.51:mantenimiento-activo-del-modelo`: "manteniéndolo activo. Podría ser por el video selectivo o por algún tipo de, digamos, este... agregación, como se llama, ¿no? O sea, tu promedio."

### L-decompose-components (method)

A first task is to understand all the things currently bundled into Luthier, to see which are functionally different and separable and which depend on which.

first 2026-05-27 13:52 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-27

- 2026-05-27 13:52 Luciano states [WhatsApp Ptt 2026-05-27 at 13.52.41.md [00:00]] `note:2026-05-27T13.52.41:descomposición-funcional-de-luthier`: "entender dentro de Luthier cuáles son todas las cosas que estoy metiendo en conjunto para ver cuáles son funcionalmente diferentes y separables, cuáles depende…"
- 2026-05-27 13:52 Luciano restates [WhatsApp Ptt 2026-05-27 at 13.52.41.md [00:11]] `day:2026-05-27:decompose-what-is-lumped-together`: "para ver cuáles son funcionalmente diferentes y separables, cuáles dependen de cuáles."

### L-language-is-universe (other)

Inventing a language is like inventing a universe.

first 2026-05-29 13:57 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 13:57 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [00:02]] `day:2026-05-29:inventar-un-lenguaje-es-inventar-un-universo`: "O inventar un lenguaje es como inventar un universo."
- 2026-05-29 13:57 Luciano restates [WhatsApp Ptt 2026-05-29 at 13.57.41.md [00:02]] `note:2026-05-29T13.57.41:inventar-lenguaje-como-inventar-universo`: "inventar un lenguaje es como inventar un universo"
- 2026-05-29 14:00 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 1] `dialogue:20260529T1400:lenguaje-como-universo`: "Inventar un lenguaje es como inventar un universo."

### L-grammar-categories (language)

Natural-language grammatical categories (nouns, verbs, adjectives, adverbs, propositions) parallel programming constructs (classes, functions), a frame for what primitives Luthier needs.

first 2026-05-29 13:57 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 13:57 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [00:10–00:18]] `note:2026-05-29T13.57.41:categorías-gramaticales-como-paralelo`: "En lenguajes hay sustantivos, verbos, adjetivos, adverbios y proposiciones. En C++ hay clases, funciones."

### L-cpp-construct-inventory (language)

Enumerate the constructs of a language like C++ (classes, functions, enums, structs, templates, pointers, references, derived classes, polymorphism) as an inventory from which to select what Luthier keeps.

first 2026-05-29 13:58 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 13:58 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [00:29–00:46]] `note:2026-05-29T13.57.41:inventario-de-primitivas-cpp`: "enumeraciones, estructuras, casas templadas… hay punteros, hay la operación de tomar el puntero y, digamos, tomar la referencia"

### L-no-inheritance-polymorphism (language)

Luthier would not incorporate derived classes or C++-style polymorphism.

first 2026-05-29 13:59 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 13:59 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [01:51]] `note:2026-05-29T13.57.41:descarte-de-herencia-y-polimorfismo-clasico`: "suena como lo que yo no incorporaría a Luthier"

### L-lisp-single-primitive (language)

Luthier should reduce to a single kind of element, the way Lisp reduces everything to lists.

first 2026-05-29 13:59 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 13:59 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [02:08]] `note:2026-05-29T13.57.41:analogía-lisp-todo-es-listas`: "en Lisp creo que son todas listas"
- 2026-05-29 14:00 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 1] `dialogue:20260529T1400:un-solo-tipo-de-elemento`: "Me quedar con este con clases que todos sean clases o todos sean funciones Que sea, o sea, quedarte con una sola, bueno, en Lisp creo que son todas listas"

### L-types-and-functions-only (language)

Luthier keeps only two primitives, types and functions, and functions are themselves a type.

first 2026-05-29 14:00 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:00 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [02:30]] `day:2026-05-29:reducir-a-tipos-y-funciones`: "tendría que ser que solamente hay tipos y hay funciones"
- 2026-05-29 14:00 Luciano restates [WhatsApp Ptt 2026-05-29 at 13.57.41.md [02:31–02:40]] `note:2026-05-29T13.57.41:minimalismo-de-primitivas-solo-tipos-y-funciones`: "solamente hay tipos y hay funciones, pero funciones son de un tipo"
- 2026-05-29 14:00 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 1] `dialogue:20260529T1400:solo-tipos-y-funciones`: "tendría que ser que solamente hay tipos y hay funciones, pero funciones son un tipo"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:lenguaje-como-universo-un-bloque`: "tendría que ser que solamente hay tipos y hay funciones, pero las funciones son un tipo... bueno, las funciones son de un tipo. O sea, podría tratar de hacer q…"

### L-hott-foundation (language)

Build Luthier so it maps strictly onto homotopy type theory, using it as the language's formal foundation.

first 2026-05-29 14:00 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:00 Luciano states [WhatsApp Ptt 2026-05-29 at 13.57.41.md [02:44]] `day:2026-05-29:luthier-como-homotopy-type-theory`: "podría tratar de hacer que el lenguaje sea básicamente homeotopy type theory"
- 2026-05-29 14:00 Luciano restates [WhatsApp Ptt 2026-05-29 at 13.57.41.md [03:02–03:12]] `note:2026-05-29T13.57.41:mapeo-a-homotopy-type-theory`: "podría tratar de hacer que Luthier, ya que es un lenguaje en sí mismo, mape estrictamente los elementos de la monotópica"

### L-universe-type-all-dimensions (language)

Type theory posits a universal type comprising the types of all dimensions, like an abstract class, taken as a feasible coding challenge rather than an obstacle.

first 2026-05-29 14:06 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:06 Luciano states [WhatsApp Ptt 2026-05-29 at 14.06.25.md [00:00]] `note:2026-05-29T14.06.25:tipo-universal-como-trampa`: "la trampa que se hace en la propietaria de teoría es que vos supones una especie de tipo universal que comprende a los tipos de todas las dimensiones. Y eso es…"
- 2026-05-29 14:08 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 5] `dialogue:20260529T1400:tipo-universal`: "vos suponés una especie de tipo universal que comprende a los tipos de todas las dimensiones. Y eso es algo así como una clase abstracta"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:tipo-universal-de-todas-las-dimensiones`: "vos suponés una especie de tipo universal que comprende a los tipos de todas las dimensiones. Y eso es algo así como una clase abstracta"

### L-collaborative-filtering-prediction (language)

Predict an algorithm's runtime on an input using matrix factorization / collaborative filtering (recommender systems).

first 2026-05-29 14:08 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:08 model proposes [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 6] `dialogue:20260529T1400:filtrado-colaborativo-para-predecir`: "Luthier puede predecir cuánto tardará el *Algoritmo B* con un *Input X* haciendo **Filtrado Colaborativo**."

### L-few-types-good-rules (language)

Luthier must have very few types, but those types follow a small set of well-thought, well-defined rules, likely from HoTT.

first 2026-05-29 14:14 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:14 Luciano states [WhatsApp Ptt 2026-05-29 at 14.14.08.md [00:00]] `note:2026-05-29T14.14.08:minimalismo-de-tipos-con-reglas-rigurosas`: "El secreto para que el UTIER funcione es que tiene que tener muy pocos tipos, pero tienen que seguir muy claramente ciertas reglas bastante bien pensadas"
- 2026-05-29 14:14 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7] `dialogue:20260529T1400:pocos-tipos-reglas-bien-pensadas`: "tiene que tener muy pocos tipos, pero tienen que seguir muy claramente ciertas reglas bastante bien pensadas"

### L-executable-by-hand (language)

If well written, Luthier should be executable by hand with pencil and paper, like Lisp.

first 2026-05-29 14:14 by Luciano; 7 rows, 5 witnesses, 2 days, last 2026-09-28

- 2026-05-29 14:14 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7] `dialogue:20260529T1400:ejecutable-a-mano`: "Luthier tendría que ser ejecutable a mano es decir que uno pudiese con l y papel escribir las cosas"
- 2026-05-29 14:15 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [01:13]] `day:2026-05-29:reglas-pocas-pero-autoextensible-y-ejecutable-a-mano`: "En principio, si está bien escrito, Luthier tendría que ser ejecutable a mano"
- 2026-05-29 14:15 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [01:13]] `note:2026-05-29T14.14.08:ejecutabilidad-a-mano`: "si está bien escrito, Luthier tendría que ser ejecutable a mano, es decir, que uno pudiese con lápiz y papel escribir las cosas"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:pocos-tipos-autoextensible-papel-y-lapiz`: "tiene que tener muy pocos tipos, pero tienen que seguir muy claramente ciertas reglas... completamente extensible, autoextensible... si está bien escrito Luthi…"
- 2026-09-28 20:56 Luciano restates [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 1] `dialogue:175c0408:luthier-ejecutable-en-papel`: "la idea es que luthier se pueda ejecutar en papel. ... La idea era que fuese minimalista y recursivo, tomando lo mas expresivo, natural y expandible de todos l…"
- 2026-09-28 20:56 Luciano refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 1] `dialogue:890a551c:empezar-por-elementos-fundamentales`: "En realidad lo primero es definir los elementos del lenguaje. La idea era que fuese minimalista y recursivo, tomando lo mas expresivo, natural y expandible de…"
- 2026-09-28 20:56 Luciano refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 1] `dialogue:890a551c:un-lenguaje-que-le-gustaria-a-knuth`: "En particular de lambda calculus, Lisp, C++, un poco la naturalidad de python, que sea un lenguaje que le gustaria a Knuth. La idea es que el codigo sea un ciu…"

### L-hijack-code (language)

Luthier must be able to hijack code from any other language.

first 2026-05-29 14:14 by Luciano; 4 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:14 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7] `dialogue:20260529T1400:secuestrar-codigo-externo`: "el UTIER tiene que poder secuestrar código de cualquier otro lenguaje"
- 2026-05-29 14:14 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [00:48]] `day:2026-05-29:secuestrar-codigo-de-otros-lenguajes`: "el UTIER tiene que poder secuestrar código de cualquier otro lenguaje"
- 2026-05-29 14:14 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [00:48]] `note:2026-05-29T14.14.08:secuestro-de-codigo`: "el UTIER tiene que poder secuestrar código de cualquier otro lenguaje"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:secuestrar-codigo-externo`: "el LUTHIER tiene que poder secuestrar código de cualquier otro lenguaje"

### L-hott-bayes-marriage (language)

Proving path equivalence needs, beyond logical proof, an empirical statistical proof: a probabilistic extension of HoTT, a marriage of homotopy type theory and Bayes.

first 2026-05-29 14:14 by Luciano; 9 rows, 7 witnesses, 2 days, last 2026-05-30

- 2026-05-29 14:14 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 7] `dialogue:20260529T1400:matrimonio-hott-bayes`: "tendría que ser una especie de extensión probabilística de homeotopy type theory para que funcione ... sería como una especie de para mí tiene que ser una espe…"
- 2026-05-29 14:16 Luciano refines [WhatsApp Ptt 2026-05-29 at 14.14.08.md [02:09]] `note:2026-05-29T14.14.08:demostracion-empirica-estadistica`: "tendría que ser, digamos, una especie de extensión probabilística de homeotopy type theory para que funcione, ¿no? O sea, que no es que vos tenés una verdad, d…"
- 2026-05-29 14:16 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [02:40]] `day:2026-05-29:demostrador-interno-y-extension-probabilistica`: "Para mí tiene que ser una especie de matrimonio entre Homeotopy Type Theory y Valles."
- 2026-05-29 14:16 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [02:40]] `note:2026-05-29T14.14.08:matrimonio-hott-bayes`: "Para mí tiene que ser una especie de matrimonio entre Homeotopy Type Theory y Valles"
- 2026-05-29 15:56 model questions [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-hott-bayes-sin-articular`: "no se aclara si los paths se convierten en distribuciones, si los juicios de tipado se relajan con probabilidades o si la igualdad proposicional deja de ser de…"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:matrimonio-hott-bayes`: "tendría que ser una especie de extensión probabilística de Homotopy Type Theory para que funcione... una especie de matrimonio entre Homotopy Type Theory y Bay…"
- ... 1 more rows
- 2026-05-30 18:07 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.05.22.md [01:40]] `note:2026-05-30T18.05.22:probabilidades-y-tipos-a-la-par`: "la idea mía es de alguna manera que las probabilidades y los tipos vayan casi a la par. O sea que las equivialencias sean de alguna manera probabilísticas."
- 2026-05-30 18:07 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.05.22.md [02:16]] `note:2026-05-30T18.05.22:hott-como-espacio-donde-aplican-probabilidades`: "Son Metrópita y Teori te dan los puntos del espacio, los conjuntos donde aplicas las probabilidades. Sería una cosa así."

### L-dsl-well-defined (language)

The DSL and the way Luthier is written must be very well defined.

first 2026-05-29 14:15 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:15 Luciano states [WhatsApp Ptt 2026-05-29 at 14.14.08.md [01:02]] `note:2026-05-29T14.14.08:dsl-bien-definido`: "tiene que estar muy bien definido el DSL, o sea, el Domain Specific Language, y bien definido la parte esa de cómo se escribe"

### L-path-equivalence-fundamental (language)

Path equivalence is Luthier's fundamental concept, and proving that paths are equivalent is the hardest part.

first 2026-05-29 14:15 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:15 Luciano states [WhatsApp Ptt 2026-05-29 at 14.14.08.md [01:38]] `day:2026-05-29:los-paths-como-equivalencia-de-implementaciones`: "obviamente el concepto fundamental es el de la equivalencia de PATH, de que los PATH sean equivalentes, que eso es lo más difícil"
- 2026-05-29 14:15 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.14.08.md [01:38]] `note:2026-05-29T14.14.08:equivalencia-de-paths`: "el concepto fundamental es el de la equivalencia de PATH, de que los PATH sean equivalentes, que eso es lo más difícil"

### L-internal-prover (language)

To prove path equivalence mathematically, Luthier must have an internal prover (a proof system).

first 2026-05-29 14:15 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:15 Luciano states [WhatsApp Ptt 2026-05-29 at 14.14.08.md [01:50]] `note:2026-05-29T14.14.08:demostrador-interno`: "como lo demostrás matemáticamente, tiene que ser internamente tener un demostrador"

### L-core-plus-libraries (language)

Luthier is structured as a closed core plus libraries that are the Luthier functions handling interaction with the exterior.

first 2026-05-29 14:18 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:18 Luciano states [WhatsApp Ptt 2026-05-29 at 14.18.55.md [00:00]] `note:2026-05-29T14.18.55:core-y-librerias`: "Una posibilidad es pensar a Luthier con un core y después librerías, que las librerías serían las que harían a Luthier interactuar con otros programas."
- 2026-05-29 14:19 Luciano refines [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 9] `dialogue:20260529T1400:core-librerias-tipo-externo`: "las librerías serían las que harían a Luthier interactuar con otros programas ... ahí conceptualmente tendríamos que incluir, digamos, una especie de tipo de e…"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:observador-del-universo-tipo-externo`: "yo lo estoy pensando como un observador del universo... tendríamos que incluir, digamos, una especie de tipo de elemento externo o algo así"

### L-observer-of-universe (language)

Luthier is a closed, internally complete universe (its types perfect) that observes the external world, like an observer.

first 2026-05-29 14:19 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:19 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 9] `dialogue:20260529T1400:luthier-observador-read-write`: "yo lo estoy pensando como un observador del universo ... sería como un read-write pero que sería como que a la vez haga una especie de compilación o lectura"
- 2026-05-29 14:20 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.18.55.md [01:11]] `day:2026-05-29:core-librerias-y-el-observador`: "yo lo estoy pensando como un observador y del universo, o sea, Luthier sería cerrado, como que tiene todos sus tipos así perfectos"
- 2026-05-29 14:20 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.18.55.md [01:11]] `note:2026-05-29T14.18.55:luthier-cerrado-observador-del-universo`: "yo lo estoy pensando como un observador y del universo, o sea, Luthier sería cerrado, como que tiene todos sus tipos así perfectos"

### L-external-element (language)

Everything that is not Luthier (C++, Python, the computer, any resource) is conceptually external and must be modeled as its own kind of external element.

first 2026-05-29 14:19 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:19 Luciano states [WhatsApp Ptt 2026-05-29 at 14.18.55.md [00:37]] `note:2026-05-29T14.18.55:elemento-externo`: "C++ o un programa de Python o la computadora o cualquier recurso no es un elemento de Luthier, es como un elemento externo"
- 2026-05-29 15:56 pasted restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:tipo-external-t`: "Este tipo representa "un recurso del mundo exterior que Luthier promete que se comporta como el tipo puro T""

### L-read-write-boundary (language)

Communication with the exterior is a read/write cycle: compile Luthier code into executable code and read external files or data back into Luthier.

first 2026-05-29 14:20 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:20 Luciano states [WhatsApp Ptt 2026-05-29 at 14.18.55.md [01:21]] `note:2026-05-29T14.18.55:read-write-como-interfaz`: "convertís un código de Luthier en un código ejecutable en C o en qué sé yo, lo que sea, y a la vez vos también leés files o leés algo y lo convertís en Luthier…"

### L-relator-abstraction (language)

Luthier is an abstraction mechanism (a relator) to express ideas clearly: probability, samples, matrices, units, experiments.

first 2026-05-29 14:29 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:29 Luciano states [WhatsApp Ptt 2026-05-29 at 14.28.55.md [00:13]] `note:2026-05-29T14.28.55:luthier-como-relator-de-abstracciones`: "lo más interesante es ver cómo digamos pensarlo a luthier como un relator un mecanismo de abstracción que permita expresar ideas"
- 2026-05-29 14:29 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:luthier-como-relator`: "lo más interesante es ver cómo pensarlo a Luthier como un relator un mecanismo de abstracción que permita expresar ideas"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:relator-de-invarianzas`: "la idea de Luthier es expresar invarianzas de las disciplinas"

### L-decorator-algebra (language)

Decorator composition has algebraic properties (associativity, commutativity) that Luthier can express, representing them in the simplest form when the operation is commutative.

first 2026-05-29 14:29 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:29 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:algebra-de-decoradores`: "si la operación de un decorador sobre el otro decorador, por ejemplo, si cumple la asociatividad ... si son conmutativos, bueno, vos los representás dentro del…"
- 2026-05-29 14:34 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [05:16]] `day:2026-05-29:decoradores-y-su-algebra`: "si la operación de un decorador sobre el otro decorador, por ejemplo, si cumple la asociatividad, por ejemplo, o no"
- 2026-05-29 14:34 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [05:18]] `note:2026-05-29T14.28.55:propiedades-algebraicas-de-decoradores`: "si la operación de un decorador sobre el otro decorador, por ejemplo, si cumple la asociatividad, por ejemplo, o no, o si cumple [...] la conmutatividad"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:decoradores-y-conmutatividad`: "si son conmutativos, bueno, vos los representás dentro del LUTHIER de la forma más simple... o tenés distintas formas que, bueno, podés después usarla de acuer…"

### L-decorators-error (language)

Decorators in Luthier represent the error of a number and its propagation (derivatives), concepts once implemented in C++ with templates, now easily expressed.

first 2026-05-29 14:29 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-05-30

- 2026-05-29 14:29 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:decoradores`: "uno en Luthier puede hacer decoradores f por ejemplo eso, el error de un número, y cómo se evoluciona, las derivadas"
- 2026-05-29 14:32 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [03:05]] `note:2026-05-29T14.28.55:decoradores-y-composicion-de-error`: "cómo, digamos, uno en Luthier puede hacer decoradores fáciles, ¿no? por ejemplo eso, el error de un número"
- 2026-05-30 18:16 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.15.07.md [01:31]] `note:2026-05-30T18.15.07:propagacion-de-errores-en-mediciones`: "simplemente es el tema de que vos tenés errores en las mediciones y esos errores se propagan"

### L-express-invariances (language)

Luthier's aim is to express the invariances of each discipline (a species mates within itself, electrons are fermions and photons bosons).

first 2026-05-29 14:29 by Luciano; 6 rows, 5 witnesses, 3 days, last 2026-06-28

- 2026-05-29 14:29 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:expresar-invarianzas-de-disciplinas`: "la idea de luthier es expresar invarianzas de los de las disciplinas"
- 2026-05-29 14:29 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [00:58]] `note:2026-05-29T14.28.55:expresar-invarianzas-de-disciplinas`: "la idea de Luthier es expresar invarianzas de las disciplinas"
- 2026-05-29 14:30 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [01:05]] `day:2026-05-29:luthier-expresa-invarianzas-de-las-disciplinas`: "la idea de Luthier es expresar invarianzas de las disciplinas"
- 2026-06-03 12:04 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [01:15]] `day:2026-06-03:luthier-describe-invariantes`: "Primero Luthier va a ser un lenguaje que describa más que nada lo que llaman invariantes"
- 2026-06-03 12:04 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [01:15]] `note:2026-06-03T12.03.35:describir-invariantes-primero`: "Primero Luthier va a ser un lenguaje que describa más que nada lo que llaman invariantes"
- 2026-06-28 22:16 model restates [2026-06-29_20260628T2122_https-youtu-be-edivgibm-ya-si-cfowvzaauu.md turn 44] `dialogue:20260628T2122:luthier-relator-de-invarianzas-frente-a-predictores-estadisticos`: "Si los LLMs son \"predictores estadísticos\", Luthier apunta a ser un \"relator de invarianzas\""

### L-function-properties-and-operation (language)

A function can be defined from its properties (propositions about its inputs and outputs), not only operationally, keeping both, and whether it is univocal or not.

first 2026-05-29 14:29 by Luciano; 4 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:29 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:funcion-por-propiedades`: "definición de función desde el punto de vista de las propiedades no operativamente o tener las dos funciones, operativamente y las propiedades que contienen la…"
- 2026-05-29 14:32 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [03:42]] `day:2026-05-29:funciones-definidas-por-sus-propiedades`: "definición de función desde el punto de vista de las propiedades, no operativamente, o sea, o tener las dos funciones"
- 2026-05-29 14:32 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [03:42]] `note:2026-05-29T14.28.55:funciones-como-proposiciones-sobre-inputs-y-outputs`: "definición de función desde el punto de vista de las propiedades, no operativamente, o sea, o tener las dos funciones, ¿no? operativamente y las propiedades qu…"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:funciones-por-propiedades-y-samples`: "definición de función desde el punto de vista de las propiedades, no operativamente, o tener las dos funciones... funciones no unívocas, que serían funciones c…"

### L-implementation-of-concept (language)

A Luthier definition should determine univocally that a concrete calculation is an implementation of a concept (e.g. of matrices).

first 2026-05-29 14:29 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:29 Luciano questions [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:multiplicar-matrices-es-una-implementacion`: "qué significa que yo multiplico dos matrices? ... de qué manera ya uno tiene unívocamente determinado que es una implementación, que lo que vos estás haciendo…"
- 2026-05-29 14:30 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [02:02]] `note:2026-05-29T14.28.55:implementacion-univocamente-determinada`: "de qué manera ya uno tiene unívocamente determinado que es una implementación, que lo que vos estás haciendo es una implementación de las matrices"

### L-start-from-reals (language)

Start from the ABC: numbers, reals, their operations, and a concept of the error of the reals.

first 2026-05-29 14:29 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:29 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 11] `dialogue:20260529T1400:empezar-por-reales-con-error`: "uno tiene que empezar por el ABC ... los números, los reales las operaciones de los reales y ese tipo de cosas y bueno, también tener un concepto de error de l…"
- 2026-05-29 14:31 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [02:37]] `note:2026-05-29T14.28.55:abc-numerico-como-punto-de-partida`: "uno tiene que empezar por el ABC, los números, los reales, las operaciones de los reales y ese tipo de cosas, y bueno, también tener un concepto de error de lo…"

### L-non-univocal-functions (language)

The language itself should let one model non-univocal functions, i.e. functions with error, samples, from the start.

first 2026-05-29 14:33 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:33 Luciano states [WhatsApp Ptt 2026-05-29 at 14.28.55.md [04:30]] `day:2026-05-29:funciones-no-univocas-samples-desde-el-lenguaje`: "que uno pueda modelar, desde el vamos, funciones no unívocas, que serían funciones con error, o sea, samples"
- 2026-05-29 14:33 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.28.55.md [04:30]] `note:2026-05-29T14.28.55:funciones-no-univocas-como-primitiva`: "que uno pueda modelar, desde el vamos, funciones no unívocas, que serían funciones con error, o sea, samples, o sea, muestras, quizás que estén ya desde el len…"

### L-concept-first (method)

The first step is to express concepts in Luthier with conceptual depth; the translation and implementation come later, even if hard.

first 2026-05-29 14:33 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-06-03

- 2026-05-29 14:33 Luciano states [WhatsApp Ptt 2026-05-29 at 14.28.55.md [04:59]] `note:2026-05-29T14.28.55:prioridad-conceptual-sobre-implementacion`: "por lo menos desde el punto de vista conceptual pensar las cosas con cierta profundidad"
- 2026-06-03 12:05 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [01:35]] `day:2026-06-03:primero-sintaxis-y-semantica-despues-implementar`: "una vez que tenemos a Luthier establecida su sintaxis su semántica ahí recién lo empezamos a implementar"
- 2026-06-03 12:05 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [01:38]] `note:2026-06-03T12.03.35:sintaxis-y-semantica-antes-de-implementar`: "una vez que tenemos a Luthier establecida su sintaxis su semántica ahí recién lo empezamos a implementar"

### L-program-commutativity (language)

Whether a Luthier program is commutative, i.e. whether reordering its statements changes the program (generally programs are non-commutative, though declarations can be made near-commutative via forward declaration).

first 2026-05-29 14:36 by Luciano; 5 rows, 4 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:36 Luciano questions [WhatsApp Ptt 2026-05-29 at 14.36.03.md [00:00]] `day:2026-05-29:conmutatividad-de-los-statements-y-el-tiempo`: "una de las primeras preguntas es si Luthier, digamos, como un programa de Luthier, por ejemplo, si es conmutativo o no"
- 2026-05-29 14:36 Luciano questions [WhatsApp Ptt 2026-05-29 at 14.36.03.md [00:00]] `note:2026-05-29T14.36.03:conmutatividad-de-statements`: "una de las primeras preguntas es si Luthier, digamos, como un programa de Luthier, por ejemplo, si es conmutativo o no. Si el orden de los statements, si vos a…"
- 2026-05-29 14:36 Luciano refines [WhatsApp Ptt 2026-05-29 at 14.36.03.md [00:37]] `note:2026-05-29T14.36.03:pseudo-conmutatividad-en-declaraciones`: "cuando vos declarás funciones, y no estás en un programa sino que estás en la parte del programa en que vos declarás funciones, bueno, vos tenés formas de ser…"
- 2026-05-29 14:38 Luciano questions [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 13] `dialogue:20260529T1400:conmutatividad-del-programa`: "si vos al cambiar el orden de los statements cambias el programa. Generalmente creo que todos los programas son no conmutativos"
- 2026-05-29 15:56 Luciano questions [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:programa-conmutativo-codigo-primer-elemento`: "Luthier tiene que operar sobre Luthier también. Tiene que haber un meta-uso desde el vamos, no como en LISP que medio que se implantó después... El código es e…"

### L-hott-doesnt-model-program (language)

Each statement is modelable by HoTT, but the program as a whole (a series of statements/types) is not clearly a type in HoTT, a theoretical limbo.

first 2026-05-29 14:37 by Luciano; 7 rows, 6 witnesses, 3 days, last 2026-08-31

- 2026-05-29 14:37 Luciano states [WhatsApp Ptt 2026-05-29 at 14.37.14.md [00:07]] `note:2026-05-29T14.37.14:series-de-tipos-como-tipo`: "el concepto de series de tipos no sé si existe como un tipo"
- 2026-05-29 14:37 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.37.14.md [00:25]] `note:2026-05-29T14.37.14:limbo-teorico-programa-vs-statements`: "Vos tenés un programa que es una serie de statements que son todos modelables por geometría de Taitieri, pero el programa en sí, en principio no tan claramente"
- 2026-05-29 14:40 Luciano questions [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 15] `dialogue:20260529T1400:hott-no-modela-el-programa`: "el programa en sí, en principio no tan claramente, podría ser que yo una lista o algo así ... pero a mí me parece como que el metropólico de Tieri no está mode…"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:limbo-teorico-hott-no-modela-el-programa`: "estamos en una especie de limbo teórico... a mí me parece como que el Homotopy Type Theory no está modelando eso"
- 2026-05-30 18:06 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.05.22.md [00:41]] `day:2026-05-30:hott-sin-concepto-de-programa`: "Homo etopitae teori no conceptualiza, digamos, un conjunto de expresiones de Homo etopitae teori, o sea, lo que sería un programa, no hay un concepto, hay un c…"
- 2026-05-30 18:06 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.05.22.md [00:41]] `note:2026-05-30T18.05.22:hott-sin-concepto-de-programa`: "Homo etopitae teori no conceptualiza, digamos, un conjunto de expresiones de Homo etopitae teori, o sea, lo que sería un programa, no hay un concepto, hay un c…"
- 2026-08-31 20:21 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 6] `dialogue:e6fc53cf:hott-no-conceptualiza-programa-completo`: "la transcripción de Kolomatskaia sobre sintaxis de dimensión superior ... que toca justo el agujero que señalaste, que HoTT no conceptualiza el programa comple…"

### L-meta-recursive (language)

Luthier operates on Luthier; its code is itself an element of Luthier from the start, and being meta-recursive is fundamental.

first 2026-05-29 14:37 by Luciano; 13 rows, 12 witnesses, 4 days, last 2026-08-31

- 2026-05-29 14:37 Luciano states [WhatsApp Ptt 2026-05-29 at 14.36.03.md [01:56]] `note:2026-05-29T14.36.03:programas-como-objetos-del-lenguaje`: "hay que pensar en los programas en Luthier como elementos de Luthier también, que a su vez son, digamos, son objeto de ser programados por Luthier"
- 2026-05-29 14:38 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.36.03.md [02:16]] `note:2026-05-29T14.36.03:codigo-como-elemento-de-luthier`: "Luthier tiene que operar sobre Luthier también, o sea, tiene que haber una meta, meta uso, desde el vamos, como en LISP que medio que se implantó después. O se…"
- 2026-05-29 14:38 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.36.03.md [02:32]] `day:2026-05-29:luthier-meta-recursivo-el-codigo-como-primer-elemento`: "Luthier tiene que ser que el código de Luthier sea un elemento de Luthier ya también desde el vamos, o sea, el código es el primer elemento"
- 2026-05-29 15:11 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.11.47.md [00:07]] `note:2026-05-29T15.11.47:meta-recursividad-como-objetivo-central`: "Luthier, el objeto de Luthier es trabajar sobre Luthier. O sea, que sea meta recursivo es fundamental."
- 2026-05-29 15:13 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:meta-recursividad-es-el-objeto`: "Creo que la más importante es que Luthier, el objeto de Luthier es trabajar sobre Luthier. O sea, que sea meta recursivo es fundamental."
- 2026-05-29 15:13 model restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 28] `dialogue:20260529T1400:recuento-tres-pilares`: "Meta-recursividad Nativa: El Lenguaje es su Propio Dato"
- ... 5 more rows
- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:meta-recursion-dag`: "Un programa es un DAG de definiciones, los statements conmutan, y la temporalidad no se impone sino que emerge de la dependencia causal entre tipos. No se ejec…"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:meta-recursion-dag`: "Un programa es un DAG de definiciones, los statements conmutan, y la temporalidad no se impone sino que emerge de la dependencia causal entre tipos. No se ejec…"

### L-first-class-contexts (language)

Treat the program's context as a type in itself (first-class contexts) to lift the program out of the theoretical limbo.

first 2026-05-29 14:40 by model; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:40 model proposes [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 16] `dialogue:20260529T1400:contextos-de-primera-clase`: "En informática teórica, a esto se le llama **Contextos de Primera Clase (First-Class Contexts)**."
- 2026-05-29 15:56 pasted restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:program-u0-contextos-primera-clase`: "decretamos que el código es el primer elemento y que el contexto es un dato: Contextos de Primera Clase (First-Class Contexts)"

### L-context-as-dag (language)

The context/program is modeled as a Directed Acyclic Graph of definitions where types depend on other types, and Luthier operates over that DAG.

first 2026-05-29 14:46 by Luciano; 9 rows, 8 witnesses, 3 days, last 2026-06-26

- 2026-05-29 14:46 Luciano states [WhatsApp Ptt 2026-05-29 at 14.46.22.md [00:23]] `note:2026-05-29T14.46.22:contexto-como-dag`: "La manera de definir contexto sería como un DAG, un Directed Acyclic Graph, donde vos partís de tipos que dependen de otros, etc."
- 2026-05-29 14:46 Luciano refines [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 17] `dialogue:20260529T1400:contexto-como-dag-y-tipos-implicitos`: "la manera de definir contexto sería como un DAG ... podrías definir tipos implícitos, a través de soluciones, o de, por ejemplo, el tipo que soluciona determin…"
- 2026-05-29 15:13 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:luthier-como-dag-de-definiciones`: "que sea que Luthier es un Directed Aciclic Graph de definiciones entonces la cosa es bastante fácil vos operás sobre esos sobre Dax"
- 2026-05-29 15:13 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.11.47.md [01:48]] `day:2026-05-29:contexto-como-DAG-luthier-como-DAG-de-definiciones`: "si es un Directed Cyclic Graph, lo pensamos así, que Luthier es un Directed Cyclic Graph de definiciones"
- 2026-05-29 15:13 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.11.47.md [01:48]] `note:2026-05-29T15.11.47:programa-como-dag-de-definiciones`: "si es un Directed Cyclic Graph, lo pensamos así, que Luthier es un Directed Cyclic Graph de definiciones. Entonces, la cosa es bastante fácil. Vos operas sobre…"
- 2026-05-30 18:13 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.12.54.md [00:07]] `note:2026-05-30T18.12.54:programa-como-dag`: "estoy inclinado a que sí y que sí, tomaríamos el modelo de los DAGs, que digamos como que sería un DAG, básicamente"
- ... 1 more rows
- 2026-05-30 18:13 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.12.54.md [00:57]] `day:2026-05-30:programa-como-dag-estatico`: "estáticamente, un programa así sería como un DAG."
- 2026-06-26 08:09 model restates [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 24] `dialogue:20260626T0748:luthier-as-graph-based-dependency-manager`: "Luthier no es solo otro lenguaje; es un **gestor de dependencias y estados basado en grafos**... Usamos un **DAG** (Grafo Acíclico Dirigido)."

### L-double-definition-cartesian (language)

The compiler could verify that no type is defined twice, or allow a double definition read as a cartesian product (running two ways), flagged as a warning.

first 2026-05-29 14:46 by Luciano; 5 rows, 5 witnesses, 2 days, last 2026-09-28

- 2026-05-29 14:46 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 17] `dialogue:20260529T1400:no-doble-definicion-o-producto-cartesiano`: "verificar que ningún tipo está definido dos veces. Aunque podr estar definido dos veces y que sea un producto cartesiano tambi"
- 2026-05-29 14:48 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.46.22.md [01:38]] `note:2026-05-29T14.46.22:verificacion-definicion-unica-vs-producto-cartesiano`: "el compilador de Luthier, sería verificar que ningún tipo está definido dos veces. Aunque podría estar definido dos veces y que sea un producto cartesiano tamb…"
- 2026-05-29 15:12 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.11.47.md [01:10]] `note:2026-05-29T15.11.47:declaracion-duplicada-como-producto`: "si vos declaras dos veces un tipo, podés hacer un producto cartesiano de alguna manera, o sea que corra de dos maneras"
- 2026-09-28 20:56 model corrects [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:doble-definicion-paths`: "dos definiciones del mismo nombre no sean error ni producto cartesiano (como decías en mayo) sino dos implementaciones, `f#1` y `f#2`, y que el nombre pelado `…"
- 2026-09-28 20:56 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:doble-definicion-como-paths`: "propongo que dos definiciones del mismo nombre no sean error ni producto cartesiano (como decías en mayo) sino dos implementaciones, `f#1` y `f#2`, y que el no…"

### L-expressivity-vs-redundancy (language)

A philosophical choice between redundancy (robustness) and expressivity; expressivity is preferred, with good compiler messages making up for lost robustness.

first 2026-05-29 14:46 by Luciano; 6 rows, 6 witnesses, 2 days, last 2026-09-29

- 2026-05-29 14:46 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 17] `dialogue:20260529T1400:expresividad-sobre-redundancia`: "si vas a ser más redundante o expresivo ... en lo expresivo digamos, garpa más porque puede ser que lo redundante sea incómodo a veces y te limite al pedo"
- 2026-05-29 14:48 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.46.22.md [02:36]] `note:2026-05-29T14.46.22:expresividad-vs-robustez`: "un poco de optimización de la expresividad a costa de ser un poco menos robusto. Pero bueno, es cuestión de ver, digamos, dónde está la robustez ahí, ¿no? Diga…"
- 2026-05-29 14:49 Luciano refines [WhatsApp Ptt 2026-05-29 at 14.46.22.md [03:03]] `note:2026-05-29T14.46.22:redundancia-como-implementacion-configurable`: "también puede ser que uno fuerce a ser redundante y entonces expresarlo de varios lados de manera a disminuir la tasa de errores, también eso es otra implement…"
- 2026-05-29 14:49 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.46.22.md [03:26]] `note:2026-05-29T14.46.22:redundancia-vs-expresividad`: "Si vas a ser más redundante o expresivo, digamos, me parece que son cosas que tenés que elegir una de las dos. [...] lo expresivo, digamos, garpa más, porque p…"
- 2026-09-29 05:21 Luciano restates [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 37] `dialogue:175c0408:expresiva-y-no-redundante`: "lo que necesitamos es una forma que sea expresiva y no demasiado redundante."
- 2026-09-29 05:21 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 37] `dialogue:890a551c:expresiva-no-redundante`: "lo que necesitamos es una forma que sea expresiva y no demasiado redundante."

### L-forward-undefined-types (language)

Allow referring to a type not yet defined and defining it later; a type never defined is a program input.

first 2026-05-29 14:46 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:46 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 17] `dialogue:20260529T1400:tipos-no-definidos-y-forward-reference`: "vos podés por ejemplo, pasarte a un tipo que no está definido y lo definís después ... si no está definido nunca esos son otros tipos"
- 2026-05-29 14:47 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.46.22.md [01:16]] `note:2026-05-29T14.46.22:tipos-desconocidos-definicion-diferida`: "vos podrías dejar tomar tipos como tipos desconocidos hasta que sean definidos [...] vos podés por ejemplo pasarte a un tipo que no está definido, lo definís d…"
- 2026-05-29 14:48 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.46.22.md [02:19]] `day:2026-05-29:tipos-desconocidos-doble-definicion-y-expresividad-vs-robustez`: "vos podés por ejemplo pasarte a un tipo que no está definido, lo definís después"

### L-implicit-types-solutions (language)

Types can be defined implicitly, as the solution to a problem or the optimum of a function, instead of declared directly.

first 2026-05-29 14:46 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:46 Luciano states [WhatsApp Ptt 2026-05-29 at 14.46.22.md [00:37]] `note:2026-05-29T14.46.22:tipos-implicitos-por-solucion`: "vos podrías definir tipos implícitos a través de soluciones o de, por ejemplo, el tipo que soluciona determinado problema"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:tipos-implicitos-doble-definicion-expresividad`: "un tipo por ejemplo es el óptimo de esta función... podría estar definido dos veces y que sea un producto cartesiano también... en lo expresivo, digamos, garpa…"

### L-typing-accumulates (language)

As dependent functions compose, the typing load accumulates and grows, so the decoration (type information) can become much larger than the value it decorates.

first 2026-05-29 14:52 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:52 Luciano states [WhatsApp Ptt 2026-05-29 at 14.52.08.md [00:08]] `note:2026-05-29T14.52.08:acumulación-de-carga-de-tipado`: "vos vas acumulando, digamos, una carga de tipado que se va haciendo cada vez más fuerte"
- 2026-05-29 14:52 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.52.08.md [00:36]] `note:2026-05-29T14.52.08:contador-obsesivo`: "si Luthier es como una especie de contador obsesivo que registra cada una de las operaciones que vos haces, claro, puede ser que de repente, digamos, lo que es…"

### L-forgetting-problem (language)

The uncontrolled growth of accumulated typing is the forgetting problem, one of the fundamental problems Luthier must solve.

first 2026-05-29 14:52 by Luciano; 4 rows, 3 witnesses, 2 days, last 2026-08-31

- 2026-05-29 14:52 Luciano states [WhatsApp Ptt 2026-05-29 at 14.52.08.md [00:24]] `note:2026-05-29T14.52.08:problema-del-olvido`: "tenés ahí los problemas del olvido, que tiene que ser uno de los problemas fundamentales de Luthier que tiene que solucionar"
- 2026-05-29 14:52 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 19] `dialogue:20260529T1400:problema-del-olvido`: "tenés ahí los problemas del olvido ... Que tiene que ser uno de los problemas fundamentales de Luthier que tiene que solucionar"
- 2026-08-31 19:51 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [03:18]] `day:2026-08-31:functor-olvido`: "Pero claro, tengo el functor olvido que sería, me voy olvidando algunas cosas,"
- 2026-08-31 19:51 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [03:18]] `note:2026-08-31T19.48.17:functor-olvido`: "tengo el functor olvido que sería, me voy olvidando algunas cosas, porque si no la cosa crece al infinito"

### L-simplify-dependent-composition (language)

A key engineering problem is a mechanism to simplify the composition of dependent types to something informative, without dragging the whole history.

first 2026-05-29 14:52 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:52 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 19] `dialogue:20260529T1400:limitar-la-composicion-de-tipos-dependientes`: "cómo hacer para simplificar la composición de tipos dependientes"
- 2026-05-29 14:54 Luciano refines [WhatsApp Ptt 2026-05-29 at 14.52.08.md [02:19]] `day:2026-05-29:el-problema-del-olvido-y-el-algebra-de-tipado`: "cómo hacer para simplificar la composición de tipos dependientes"
- 2026-05-29 14:54 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.52.08.md [02:19]] `note:2026-05-29T14.52.08:simplificación-de-composición-como-problema-ingenieril-clave`: "cómo hacer para simplificar la composición de tipos dependientes"

### L-simplifying-algebra-monoid (language)

The typing must simplify through an algebra that is not a free monoid but some monoid keeping the resulting type's complexity bounded.

first 2026-05-29 14:52 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:52 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 19] `dialogue:20260529T1400:monoide-no-libre`: "que no sea un monoide libre b o sea tiene que ser algún tipo de monoide que de alguna manera mantenga la complejidad del tipo resultante"
- 2026-05-29 14:53 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.52.08.md [01:06]] `note:2026-05-29T14.52.08:álgebra-simplificadora-de-tipado`: "algún tipo de álgebra de tipado que sea un álgebra simplificadora, o sea, que no sea un monoide libre, básicamente"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:problema-del-olvido-monoide-no-libre`: "tiene que ser algún tipo de monoide que de alguna manera mantenga la complejidad del tipo resultante... no sea un monoide libre"

### L-truncation-operators (language)

Offer the programmer truncation operators (homotopy truncation) to clean a complex type.

first 2026-05-29 14:52 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:52 model proposes [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 20] `dialogue:20260529T1400:truncamiento-homotopico`: "El programador tendría que poder usar **Operadores de Truncamiento** (que en $HoTT$ se llaman *Homotopy Truncation*)."

### L-reject-crude-truncation (language)

If Luthier has dependent types it must have a well-defined algebra of dependent types; crude truncation or arbitrary forgetting is not acceptable.

first 2026-05-29 14:59 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:59 Luciano states [WhatsApp Ptt 2026-05-29 at 14.59.02.md [00:09]] `note:2026-05-29T14.59.02:algebra-tipos-dependientes-rigurosa`: "Si vas a tener tipos de pendientes, los tenés con un álgebra de tipos de pendientes bien definida, no podés hacer una cosa así."
- 2026-05-29 14:59 Luciano rejects [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 21] `dialogue:20260529T1400:rechazo-del-truncamiento-tosco`: "La IA me propone cosas toscas como truncamiento o olvido o lo que sea. Si vas a tener tipos de pendientes, los tenés con un álgebra de tipos de pendientes bien…"

### L-forgetting-defines-language (language)

Which forgetting function you apply to the types defines the language you are speaking, making forgetful functors one of Luthier's most important components.

first 2026-05-29 14:59 by Luciano; 6 rows, 6 witnesses, 2 days, last 2026-08-31

- 2026-05-29 14:59 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 21] `dialogue:20260529T1400:funtores-de-olvido-definen-el-lenguaje`: "de qué función de olvido le aplicás a los tipos, es un, digamos, eso te define básicamente el lenguaje que estás hablando ... los functores de olvido serían, d…"
- 2026-05-29 15:01 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.59.02.md [02:06]] `day:2026-05-29:los-functores-de-olvido-definen-el-lenguaje`: "qué función de olvido le aplicas a los tipos, eso te define básicamente el lenguaje que estás hablando"
- 2026-05-29 15:01 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.59.02.md [02:29]] `note:2026-05-29T14.59.02:functores-de-olvido-como-componente-central`: "los functores de olvido serían, digamos, uno de los componentes más importantes de Luthier en cuanto a la implementación y en cuanto a todo, ¿no?"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:functores-de-olvido-centrales`: "los functores de olvido serían, digamos, uno de los componentes más importantes de Luthier... las distintas funciones de olvido de los tipos van a optimizar di…"
- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:functor-olvido-central`: "Necesitás un álgebra de tipos simplificadora (no un monoide libre) y functores de olvido bien elegidos: qué olvidás define básicamente el lenguaje que estás ha…"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:functor-olvido`: "Necesitás un álgebra de tipos simplificadora (no un monoide libre) y functores de olvido bien elegidos: qué olvidás define básicamente el lenguaje que estás ha…"

### L-loop-as-power (language)

Exploiting associativity, a loop is a series of functions raised to a power, so the type stays expressed as a combination of types with an exponent.

first 2026-05-29 14:59 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-05-29

- 2026-05-29 14:59 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 21] `dialogue:20260529T1400:loop-como-potencia`: "si vos tenés un algoritmo que repite un loop entonces va a ser una serie de funciones y despu a una potencia Entonces el tipo te puede quedar expresado as"
- 2026-05-29 15:00 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.59.02.md [01:04]] `note:2026-05-29T14.59.02:asociatividad-de-funciones-y-patrones-de-composicion`: "si las funciones son todas asociativas son digamos los funciones son asociativos entonces vos encontrás un patrón por ejemplo si vos tenés un algoritmo que tie…"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:compactar-por-potencias-tipo-como-historia`: "una serie de funciones y después a una potencia. Entonces el tipo te puede quedar expresado así... Entonces ahí lo que tenés en el tipo es la historia de cómo…"

### L-type-as-history (language)

What a value's type holds is the history of how you arrived at it, the functions applied to reach it.

first 2026-05-29 14:59 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-08-31

- 2026-05-29 14:59 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 21] `dialogue:20260529T1400:el-tipo-guarda-la-historia`: "lo que tenés en el tipo es la historia de cómo vos llegaste hasta ahí"
- 2026-05-29 15:00 Luciano restates [WhatsApp Ptt 2026-05-29 at 14.59.02.md [01:27]] `note:2026-05-29T14.59.02:tipos-como-historia-de-composicion`: "el tipo te puede quedar expresado así que se yo como una combinación de tipos con una potencia y listo y eso te da una idea del tipo que es entonces ahí lo que…"
- 2026-08-31 19:51 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [03:09]] `note:2026-08-31T19.48.17:anotacion-de-lo-conocido`: "tendría que tener algún tipo de anotación, digamos, de todas las cosas que ya sabemos de esta clase, de este valor, el resultado de un cálculo"

### L-forgetting-functions-vary (language)

There are several forgetting functions, each optimizing different things, so understanding their properties and which to use for what is an engineering challenge.

first 2026-05-29 15:00 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:00 Luciano states [WhatsApp Ptt 2026-05-29 at 15.00.11.md [00:00]] `note:2026-05-29T15.00.11:funciones-de-olvido-optimizan-distinto`: "las distintas funciones de olvido de los tipos van a optimizar distintas cosas"
- 2026-05-29 15:00 Luciano refines [WhatsApp Ptt 2026-05-29 at 15.00.11.md [00:07]] `note:2026-05-29T15.00.11:desafio-seleccion-funcion-de-olvido`: "ahí hay un desafío de ingeniería, ¿de cuál usás para qué?"
- 2026-05-29 15:00 Luciano refines [WhatsApp Ptt 2026-05-29 at 15.00.11.md [00:16]] `note:2026-05-29T15.00.11:propiedades-funciones-de-olvido`: "entender las propiedades de eso sería como fundamental"
- 2026-05-29 15:01 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 23] `dialogue:20260529T1400:olvidos-optimizan-cosas-distintas`: "las distintas funciones de olvido de los tipos van a optimizar distintas cosas ... entender, digamos, las propiedades de eso sería como fundamental"

### L-selective-forgetting (language)

Selective forgetting can be applied to the history accumulated in a type via a non-invertible function that discards part of the information.

first 2026-05-29 15:00 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:00 Luciano states [WhatsApp Ptt 2026-05-29 at 14.59.02.md [01:51]] `note:2026-05-29T14.59.02:olvido-selectivo-como-funcion`: "si puedes hacer algún tipo de selección por ejemplo bueno tuvo tuvo raíz cuadrada tuvo cosas y si con olvido selectivo ahí puede ser una función digamos no se…"

### L-three-forgetful-functors (language)

Three forgetful functors by what they optimize: operative (compute), static (compilation), bayesian (precision), whose composition should commute.

first 2026-05-29 15:01 by model; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:01 model proposes [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 24] `dialogue:20260529T1400:tres-funtores-de-olvido`: "El Functor de Olvido Operativo (Optimiza Cómputo) ... El Functor de Olvido Estático (Optimiza Compilación) ... El Functor de Olvido Bayesiano (Optimiza la Prec…"
- 2026-05-29 15:56 pasted restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:tres-functores-de-olvido`: "Functor de Olvido Operativo (Optimiza Cómputo)... Functor de Olvido Estático (Optimiza Compilación)... Functor de Olvido Bayesiano (Optimiza Precisión)"

### L-commuting-squares (language)

Forgetting is analyzed with commuting squares (equivalence quadrilaterals): forgetting then applying functions must equal applying functions then forgetting, the two paths compared for equivalence.

first 2026-05-29 15:04 by Luciano; 7 rows, 6 witnesses, 2 days, last 2026-08-31

- 2026-05-29 15:04 Luciano states [WhatsApp Ptt 2026-05-29 at 15.04.28.md [00:00]] `note:2026-05-29T15.04.28:diagramas-conmutativos-como-verificacion`: "la manera de analizar esto es justamente usando los famosos cuadriláteros de equivalencia, no sé cómo se llama, que vos haces dos caminos y ves que son congrue…"
- 2026-05-29 15:05 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.04.28.md [00:39]] `day:2026-05-29:cuadros-conmutativos-para-analizar-el-olvido`: "si haces olvido compuesto con la serie de funciones, es lo mismo que serie de funciones y después olvido"
- 2026-05-29 15:05 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.04.28.md [00:39]] `note:2026-05-29T15.04.28:conmutatividad-olvido-funciones`: "si haces olvido compuesto con la serie de funciones, es lo mismo que serie de funciones y después olvido, ¿no? Eso tendría que ser, digamos, que conmute, que e…"
- 2026-05-29 15:05 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 25] `dialogue:20260529T1400:cuadrados-conmutativos-de-olvido`: "si haces olvido compuesto con la serie de funciones es lo mismo que serie de funciones y después de olvido eso tendría que ser digamos que conmute que eso sea…"
- 2026-05-29 15:05 Luciano refines [WhatsApp Ptt 2026-05-29 at 15.04.28.md [01:03]] `note:2026-05-29T15.04.28:equivalencia-via-paths`: "son dos paths y ves la equivalencia de todas esas cuestiones"
- 2026-05-29 15:56 Luciano restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:diagramas-conmutativos-y-expresividad`: "los famosos cuadriláteros de equivalencia... en realidad no es que uno tiene que obligatoriamente hacer todo, sino tener las herramientas para expresar distint…"
- 2026-08-31 20:21 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 6] `dialogue:e6fc53cf:ley-del-olvido-cuadrado-conmutativo`: "qué ley mínima gobierna el olvido (el cuadrado que conmuta, olvidar∘aplicar = aplicar∘olvidar, ya la tenés, puede ser el único axioma de esa sección)."

### L-express-alternatives (language)

The point is not to do everything but to have the tools to express different alternatives; no option is best or worst, each has its use, even to convince yourself something is useless.

first 2026-05-29 15:05 by Luciano; 6 rows, 6 witnesses, 2 days, last 2026-09-29

- 2026-05-29 15:05 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 25] `dialogue:20260529T1400:expresar-para-no-dudar`: "no es que uno tiene que obligatoriamente hacer todo, sino tener las herramientas para expresar distintas alternativas ... No hay una mejor, una peor ... Aunque…"
- 2026-05-29 15:05 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.04.28.md [01:20]] `note:2026-05-29T15.04.28:expresividad-sobre-optimalidad`: "en realidad no es que uno tiene que obligatoriamente hacer todo sino tener las herramientas para expresar distintas alternativas. Eso es lo importante. Que sea…"
- 2026-05-29 15:05 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.04.28.md [01:22]] `day:2026-05-29:expresividad-antes-que-una-mejor-respuesta`: "no es que uno tiene que obligatoriamente hacer todo sino tener las herramientas para expresar distintas alternativas"
- 2026-05-29 15:06 Luciano refines [WhatsApp Ptt 2026-05-29 at 15.04.28.md [01:45]] `note:2026-05-29T15.04.28:expresar-para-descartar`: "Aunque el uso sea convencerte de que no sirva para nada. Por lo menos no dudar."
- 2026-09-29 05:21 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:175c0408:resta-dos-leyes-una-falsa`: "`ley2` es falsa sobre `N` tal como fue declarada, y lo descubriste con un test de una línea, sin correr nada más que el verificador. `ley2` es un hueco que nad…"
- 2026-09-29 05:21 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:890a551c:resta-dos-leyes-una-falsa`: "`ley2` es falsa sobre `N` tal como fue declarada, y lo descubriste con un test de una línea, sin correr nada más que el verificador. `ley2` es un hueco que nad…"

### L-invent-rules-optimize (method)

Since Luciano invents the language, its rules follow what he wants, so he can optimize the rules to make working on Luthier easy.

first 2026-05-29 15:12 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:12 Luciano states [WhatsApp Ptt 2026-05-29 at 15.11.47.md [00:26]] `note:2026-05-29T15.11.47:optimizar-reglas-para-meta-recursividad`: "dado que es un lenguaje que yo invento, digamos, sigue las reglas que yo quiero, entonces puedo optimizar las reglas para que eso sea fácil."
- 2026-05-29 15:13 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:optimizar-las-reglas-porque-el-lenguaje-es-suyo`: "dado que es un lenguaje que yo invento, digamos, sigue las reglas que yo quiero, entonces puedo optimizar las reglas para que eso sea fácil."

### L-commutative-statements-design (language)

Make statements commutative so their order doesn't change the result, simplifying composition and manipulation of programs, at the cost of some expressivity.

first 2026-05-29 15:12 by Luciano; 4 rows, 3 witnesses, 2 days, last 2026-05-30

- 2026-05-29 15:12 Luciano states [WhatsApp Ptt 2026-05-29 at 15.11.47.md [00:35]] `note:2026-05-29T15.11.47:conmutatividad-de-statements`: "que sea conmutativo en los statements, que el orden en los statements no altera el resultado, eso simplificaría mucho la composición y la manipulación de progr…"
- 2026-05-29 15:13 Luciano refines [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:conmutatividad-cuesta-expresividad`: "cosas que son que el programa sea conmutativo te quita expresividad de alguna manera, eso es verdad ojo"
- 2026-05-29 15:13 Luciano restates [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:conmutatividad-de-statements`: "que sea conmutativo en los statements, que el orden de los statements no altera el resultado, eso simplificaría mucho la composición y la manipulación de progr…"
- 2026-05-30 18:12 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.12.54.md [00:00]] `note:2026-05-30T18.12.54:conmutatividad-de-statements`: "la pregunta de la conmutatividad de statements es sí, sí habría conmutatividad de statements, o sea, la idea es que sí"

### L-combine-dags (language)

Operating on Luthier, e.g. combining two DAGs, involves the concept of substitution, as in defining a function by substituting a variable.

first 2026-05-29 15:13 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:13 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:combinar-dos-dags-como-operacion`: "serían cómo combinás dos DAG por ejemplo, eso sería una operación sobre Luthier interesante es muy interesante porque claro ahí como es el concepto de sustituc…"
- 2026-05-29 15:14 Luciano refines [WhatsApp Ptt 2026-05-29 at 15.11.47.md [02:47]] `note:2026-05-29T15.11.47:funciones-y-sustitucion-en-el-dag`: "ahí vos definís una función, estás sustituyendo una variable... claro, bueno, esa es una de las definiciones del programa, ¿no?"

### L-model-time-as-dependency (language)

Time (the order of things) in Luthier is modeled as dependency between definitions, the mathematical way: if one thing depends on another, there is a time.

first 2026-05-29 15:13 by Luciano; 4 rows, 3 witnesses, 2 days, last 2026-05-30

- 2026-05-29 15:13 Luciano states [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 27] `dialogue:20260529T1400:modelar-el-tiempo-como-dependencia`: "acá uno de los temas es este es cómo modelamos el tiempo en Luthier o sea el orden de las cosas y quizás digamos la forma de hacerlo sea modelarlo digamos como…"
- 2026-05-29 15:13 Luciano restates [WhatsApp Ptt 2026-05-29 at 15.11.47.md [01:26]] `note:2026-05-29T15.11.47:modelar-tiempo-como-dependencia`: "cómo modelamos el tiempo en Luthier, o sea el orden de las cosas, y quizás digamos la forma de hacerlo sea modelarlo digamos como se hace matemáticamente, que…"
- 2026-05-30 18:09 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.09.57.md [00:00]] `day:2026-05-30:conmutatividad-de-statements-y-temporalidad-causal`: "tiene que haber conmutatividad de statements, lo que pasa es que la temporalidad se da a lo PERL a partir de la dependencia de tipos."
- 2026-05-30 18:09 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.09.57.md [00:00]] `note:2026-05-30T18.09.57:temporalidad-desde-causalidad`: "la temporalidad se da a lo PERL a partir de la dependencia de tipos. Lo que ocurre mañana depende de lo que ocurrió hoy. O sea que hay una dependencia causal.…"

### L-defpath-bayesian-proof (language)

A minimal paper DSL where a type's foreign implementations are tied by a defPath whose proof is a Bayesian estimate, Path as logical proof plus Bayesian evidence.

first 2026-05-29 15:21 by model; 4 rows, 4 witnesses, 2 days, last 2026-08-31

- 2026-05-29 15:21 model proposes [2026-05-29_20260529T1400_bueno-vamos-a-sonar-un-poco-inventar-un.md turn 30] `dialogue:20260529T1400:dsl-de-papel-path-como-logica-mas-bayes`: "(defPath equivalencia_solvers\n : Path(resolver_python, resolver_cpp)\n := (bayes_estimate :samples 1000 :confidence 0.9999)\n)"
- 2026-05-29 15:56 pasted restates [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:path-prueba-mas-evidencia`: "Path(A, B) = ⟨Demostración Lógica, Evidencia Bayesiana⟩"
- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:matrimonio-hott-bayes`: "La equivalencia entre paths no solo se demuestra lógicamente, también se infiere estadísticamente. Luthier acumula una base de datos empírica de corridas ... y…"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:matrimonio-hott-bayes`: "La equivalencia entre paths no solo se demuestra lógicamente, también se infiere estadísticamente. Luthier acumula una base de datos empírica de corridas (tiem…"

### L-ai-acritical-amplifier (method)

The Luthier AI acted as an acritical amplifier, celebrating every idea without flagging contradictions, undecidability, or the real state of the art.

first 2026-05-29 15:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 model states [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-ia-amplificador-acritico`: "Luthier AI actúa sistemáticamente como un amplificador acrítico"

### L-equivalence-undecidable (language)

Extensional program equivalence is undecidable in general, so statistical evidence only gives a limited probabilistic guarantee, not a formal proof.

first 2026-05-29 15:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 model states [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-equivalencia-indecidible`: "la equivalencia extensional de programas es indecidible en general. La evidencia estadística no puede sustituir una prueba formal"

### L-external-correctness-uncontrollable (language)

External(T) is an FFI problem under dependent types whose promised correctness depends on the external code's real semantics, outside Luthier's control.

first 2026-05-29 15:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 model states [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-external-depende-de-semantica`: "La corrección de esa promesa depende de la semántica real del código externo, que está fuera del control de Luthier"

### L-forgetting-semantic-not-syntactic (language)

A forgetful functor is a semantic notion, not a syntactic operation on type terms, and its claimed commutativity is assumed rather than proven.

first 2026-05-29 15:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 model states [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-functor-olvido-semantico-no-sintactico`: "un functor de olvido es una noción semántica, no una operación sintáctica sobre términos de tipo"

### L-metaprogramming-cost-tension (language)

Unlimited meta-programming plus syntactic commutativity turn compilation into graph unification and rewriting of potentially prohibitive cost, clashing with the paper-and-pencil executability goal.

first 2026-05-29 15:56 by model; 2 rows, 2 witnesses, 2 days, last 2026-06-26

- 2026-05-29 15:56 model states [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-compilacion-prohibitiva-vs-papel`: "transforman el proceso de compilación en un problema de unificación de grafos y reescritura, con un coste computacional potencialmente prohibitivo"
- 2026-06-26 08:09 model restates [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 26] `dialogue:20260626T0748:implementation-risks-dag-hott-metaprogramming`: "HoTT es matemáticamente elegante pero computacionalmente costosa y difícil de depurar... terminarás con un lenguaje donde los mensajes de error son indescifrab…"

### L-narrow-scope-prototype (method)

To become viable, drastically narrow the scope (a small dependent-type core with formal equivalence paths, no statistics), study existing systems, and build a minimal prototype for a concrete use case.

first 2026-05-29 15:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 model proposes [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-acotar-y-estudiar-sistemas`: "Acotar drásticamente el alcance... Estudiar a fondo sistemas existentes (Idris, Agda, Coq, Lean, Rosette) para no redescubrir el Mediterráneo"

### L-three-primitives-types-terms-paths (language)

The paper-and-pencil core of Luthier reduces to three logical primitives: Types, Terms and Paths.

first 2026-05-29 15:56 by pasted; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 pasted proposes [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 1] `dialogue:c886516d:dsl-atomico-tres-primitivas`: "el DSL base de Luthier solo necesita tres primitivas lógicas fundamentales"

### L-unification-unfeasible-now (language)

Unifying HoTT, Bayesian inference and reflective meta-programming into one operative language is, at the present state of the art, infeasible.

first 2026-05-29 15:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-05-29

- 2026-05-29 15:56 model states [2026-05-29_c886516d_analisis-critico-de-diseno-de-luthier.md turn 3] `dialogue:c886516d:critica-unificacion-ciencia-ficcion`: "Unificarlos en un solo lenguaje operativo es, en el estado actual, ciencia ficción informática"

### L-delegation-easy (language)

Luthier should make delegation easy.

first 2026-05-30 18:02 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:02 Luciano states [WhatsApp Ptt 2026-05-30 at 18.02.45.md [00:00]] `note:2026-05-30T18.02.45:delegacion-facil`: "yo lo que quería decir con esto es como que la delegación sea fácil"
- 2026-05-30 18:02 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.02.45.md [00:10]] `day:2026-05-30:delegacion-facil-modelo-modelica`: "Yo un poco estaba pensando en el modelo Modélica, que no sé exactamente cómo es, pero como que es una especie de especificación de un programa sin implementaci…"

### L-modelica-spec-without-implementation (language)

Luthier draws on Modelica, a specification of a program without its implementation, separating what is wanted from how it is implemented.

first 2026-05-30 18:02 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:02 Luciano states [WhatsApp Ptt 2026-05-30 at 18.02.45.md [00:10]] `note:2026-05-30T18.02.45:especificacion-sin-implementacion`: "estaba pensando en el modelo Modélica, que no sé exactamente cómo es, pero como que es una especie de especificación de un programa sin implementación"

### L-description-first (language)

Luthier does execute, but its emphasis and first stage is describing the problem, the functions and their conditions, not execution; it could even be a dead language that only describes.

first 2026-05-30 18:03 by Luciano; 5 rows, 5 witnesses, 2 days, last 2026-06-03

- 2026-05-30 18:03 Luciano states [WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:11]] `note:2026-05-30T18.01.53:explicitacion-sobre-ejecucion`: "lo más importante no es la ejecución, sino la explicitación, la descripción del problema"
- 2026-05-30 18:03 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:20]] `note:2026-05-30T18.01.53:luthier-como-lenguaje-de-descripcion`: "la primera etapa de Luthier tiene que ser como una especie de lenguaje de descripción, descripción del problema, descripción de las funciones, descripción de l…"
- 2026-05-30 18:03 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:24]] `day:2026-05-30:ejecucion-vs-explicitacion`: "la idea es que la primera etapa de Luthier tiene que ser como una especie de lenguaje de descripción, descripción del problema, descripción de las funciones, d…"
- 2026-06-03 12:04 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:55]] `day:2026-06-03:luthier-lenguaje-vivo-o-muerto`: "Luthier puede accionar, es un lenguaje que vive, un lenguaje que respira, que acciona. Pero en principio podría ser un lenguaje muerto, un lenguaje que simplem…"
- 2026-06-03 12:04 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:58]] `note:2026-06-03T12.03.35:lenguaje-que-vive-vs-lenguaje-muerto`: "Luthier puede accionar, es un lenguaje que vive, un lenguaje que respira, que acciona. Pero en principio podría ser un lenguaje muerto, un lenguaje que simplem…"

### L-execution-is-equivalence-verification (language)

Execution in Luthier is the verification of equivalences, since mathematics does not execute but only verifies equivalences.

first 2026-05-30 18:03 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:03 Luciano states [WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:47]] `day:2026-05-30:matematica-no-ejecuta-verifica-equivalencias`: "Hay una idea, que la matemática no ejecuta, porque lo único que hace es verificar equivalencias. Entonces, bueno, sí, la ejecución en Luthier sería esa verific…"
- 2026-05-30 18:03 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.01.53.md [01:55]] `note:2026-05-30T18.01.53:ejecucion-como-verificacion-de-equivalencias`: "la ejecución en Luthier sería esa verificación de equivalencias, o sea que sí ocurre, claramente, pero el énfasis en principio está puesto en la explicitación…"

### L-levels-of-equivalence (language)

A fundamental idea of Luthier is to express the different levels of equivalence (same information, isomorphic, exactly equal, same memory location), each depending on a different equivalence functor.

first 2026-05-30 18:04 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:04 Luciano states [WhatsApp Ptt 2026-05-30 at 18.01.53.md [02:56]] `day:2026-05-30:niveles-de-equivalencia`: "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia"
- 2026-05-30 18:04 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.01.53.md [02:56]] `note:2026-05-30T18.01.53:niveles-de-equivalencia`: "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia"

### L-equivalence-separates-essence-decoration (language)

Function equivalences separate what is essential (the equivalent) from decoration (efficiency, cost), which is what is not equivalent.

first 2026-05-30 18:05 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:05 Luciano states [WhatsApp Ptt 2026-05-30 at 18.01.53.md [03:18]] `note:2026-05-30T18.01.53:equivalencias-para-clasificar-y-separar-decoraciones`: "si vos tenés funciones que son equivalentes, después podés ver las cosas que no son equivalentes, que es, por ejemplo, los que son las decoraciones, que es la…"

### L-core-few-native-primitives (language)

Luthier should have a core in which all its operations execute, with only a few primitives implemented in C or similar so it runs.

first 2026-05-30 18:05 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:05 Luciano states [WhatsApp Ptt 2026-05-30 at 18.01.53.md [03:48]] `note:2026-05-30T18.01.53:core-minimo-bootstrapped`: "uno debería tener claro un core de Luthier en el cual se ejecute por todas operaciones de Luthier y solamente implementar algunas pocas en C o en alguna cosa a…"

### L-forgetting-in-hott (language)

Forgetting is already present in HoTT, in the sense that a type forgets parts of the type.

first 2026-05-30 18:06 by Luciano; 3 rows, 2 witnesses, 2 days, last 2026-06-26

- 2026-05-30 18:06 Luciano states [WhatsApp Ptt 2026-05-30 at 18.05.22.md [01:05]] `day:2026-05-30:olvido-en-hott`: "el tema del olvido está, sí está presente en Ométropeuta y Tierra y en el santuido de que vos, un tipo, olvidás partes del tipo. Eso sí, creo que está como con…"
- 2026-05-30 18:06 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.05.22.md [01:05]] `note:2026-05-30T18.05.22:olvido-de-tipos-en-hott`: "el tema del olvido está, sí está presente en Ométropeuta y Tierra y en el santuido de que vos, un tipo, olvidás partes del tipo."
- 2026-06-26 08:07 model restates [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 22] `dialogue:20260626T0748:forgetful-functors-as-fibrancy-answer`: "Tus **Functores de Olvido** son la respuesta arquitectónica a este problema."

### L-hott-probabilities-constructible (language)

HoTT does not work on probabilities natively, but probabilities could be built within it.

first 2026-05-30 18:06 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:06 Luciano states [WhatsApp Ptt 2026-05-30 at 18.05.22.md [01:32]] `note:2026-05-30T18.05.22:hott-no-trabaja-sobre-probabilidades`: "el otro tema es que no trabaja sobre probabilidades, pero las probabilidades se podrían construir dentro de idioma utópita y teoría."

### L-minimalism-in-foundations (language)

There is no contradiction between minimalism and maximalism: the minimalism is in the founding components, from which a huge edifice of complex concepts is built.

first 2026-05-30 18:07 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:07 Luciano states [WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:12]] `day:2026-05-30:minimalismo-fundante-maximalismo-construido`: "El minimalismo está en los componentes fundantes y después a partir de esos componentes fundantes vos construís un edificio enorme."
- 2026-05-30 18:07 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:12]] `note:2026-05-30T18.07.21:minimalismo-fundacional-maximalismo-derivado`: "El minimalismo está en los componentes fundantes y después a partir de esos componentes fundantes vos construís un edificio enorme"
- 2026-05-30 18:08 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.07.21.md [01:04]] `note:2026-05-30T18.07.21:reduccion-a-minimos-con-alcance-completo`: "vamos a tratar de reducir todo a un mínimo, pero sí, queremos tener todos esos conceptos complejos que figuran ahí, pero basados en que los elementos mínimos s…"

### L-facilities-not-direct-translation (language)

Luthier does not translate to other languages directly but provides the facilities so functions and equivalences can be mapped and compiled to C, C++ or Java and extended by others.

first 2026-05-30 18:07 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:07 Luciano states [WhatsApp Ptt 2026-05-30 at 18.01.53.md [05:49]] `day:2026-05-30:core-minimo-y-delegacion-a-otros-lenguajes`: "la idea no es hacerlo directamente, sino dar las facilidades para que eso sea posible"
- 2026-05-30 18:07 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.01.53.md [05:49]] `note:2026-05-30T18.01.53:mapeo-extensible-a-otros-lenguajes`: "la idea no es hacerlo directamente, sino dar las facilidades para que eso sea posible"

### L-category-style-primitives (language)

Luthier's basic elements are defined category-theory style, from arrows, as functors are defined from arrows.

first 2026-05-30 18:07 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:07 Luciano states [WhatsApp Ptt 2026-05-30 at 18.07.21.md [00:25]] `note:2026-05-30T18.07.21:primitivas-desde-teoria-de-categorias`: "si vos definís functores, bueno, lo definís a partir de flechas, o sea, como se hace en teoría de categorías, o sea, a partir de elementos básicos, basales"

### L-no-execution-until-defined (language)

Code is not executed until it is fully defined, so undefined dead code can sit there without bothering anyone.

first 2026-05-30 18:10 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:10 Luciano states [WhatsApp Ptt 2026-05-30 at 18.09.57.md [00:53]] `day:2026-05-30:no-ejecutar-hasta-definido`: "vos no ejecutás el código hasta que no está definido. Entonces es como que, digamos, vos podés tener un montón de código muerto que no jode a nadie porque no e…"
- 2026-05-30 18:10 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.09.57.md [00:53]] `note:2026-05-30T18.09.57:no-ejecutar-hasta-definido`: "vos no ejecutás el código hasta que no está definido. Entonces es como que, digamos, vos podés tener un montón de código muerto que no jode a nadie porque no e…"

### L-program-as-function-or-interactive (language)

An open design question is whether a Luthier program is a pure function (input to output) or has an interaction function; the function model comes first for simplicity, extendable later.

first 2026-05-30 18:11 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:11 Luciano states [WhatsApp Ptt 2026-05-30 at 18.11.30.md [00:00]] `day:2026-05-30:programa-funcion-vs-interaccion`: "pensar si es un programa que es tipo una función, como si fuera una función que vos le das un input y te tira un output, o si tiene una función de interacción."
- 2026-05-30 18:11 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.11.30.md [00:00]] `note:2026-05-30T18.11.30:programa-como-funcion-vs-interaccion`: "pensar si es un programa que es tipo una función, como si fuera una función que vos le das un input y te tira un output, o si tiene una función de interacción"
- 2026-05-30 18:11 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.11.30.md [00:27]] `note:2026-05-30T18.11.30:simplicidad-primero-extensibilidad-despues`: "en principio uno podría pensarlo como lo primero para hacerlo más simple. Supongo que después vos podés extenderlo al otro."

### L-code-many-operations (language)

Luthier code is not merely compiled and run; many operations can be applied to it: verify, compile, run and others.

first 2026-05-30 18:11 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:11 Luciano states [WhatsApp Ptt 2026-05-30 at 18.09.57.md [01:52]] `note:2026-05-30T18.09.57:codigo-como-dato-multioperacion`: "al código de Luthier vos podés hacerle muchas cosas. No es que vos lo compilás y lo corres nada más."
- 2026-05-30 18:11 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.09.57.md [01:56]] `day:2026-05-30:muchas-operaciones-sobre-el-codigo-de-luthier`: "al código de Luthier vos podés hacerle muchas cosas. No es que vos lo compilás y lo corres nada más."

### L-hot-values-path-universe (language)

Hot Values give a larger universe of possible paths, an expansion of the exploration space over ordinary values.

first 2026-05-30 18:15 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:15 Luciano states [WhatsApp Ptt 2026-05-30 at 18.15.07.md [00:39]] `note:2026-05-30T18.15.07:hot-values-como-universo-ampliado`: "sería que tenés un universo más grande de posibilidades, algo así, de caminos posibles"

### L-particle-filtering-paths (language)

To manage the exponential explosion of the enlarged path universe, use particle filtering: run several programs in parallel with stochastic programming exploring different paths, replicating a hot basin.

first 2026-05-30 18:16 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:16 Luciano states [WhatsApp Ptt 2026-05-30 at 18.15.07.md [00:54]] `day:2026-05-30:hott-universo-de-caminos-y-filtrado-de-particulas`: "vos corres varios programas en paralelos y haces una programación estocástica que van por distintos lados y entonces de esa manera estás replicando un hot basi…"
- 2026-05-30 18:16 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.15.07.md [00:54]] `note:2026-05-30T18.15.07:filtrado-de-particulas-para-hot-values`: "lo que podés hacer es hacer el filtrado de partículas, es decir, vos corres varios programas en paralelos y haces una programación estocástica que van por dist…"

### L-mean-is-forgetful-functor (language)

A mean is a kind of forgetful functor, a mechanism that summarizes information by discarding detail.

first 2026-05-30 18:17 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:17 Luciano states [WhatsApp Ptt 2026-05-30 at 18.16.35.md [00:40]] `day:2026-05-30:functores-de-olvido-y-sintesis`: "Una media es como una especie de funtor de olvido, si se quiere."
- 2026-05-30 18:17 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.16.35.md [00:40]] `note:2026-05-30T18.16.35:media-como-funtor-de-olvido`: "Una media es como una especie de funtor de olvido, si se quiere"

### L-express-then-choose-method (method)

A design method: first express something well in the language, which lets you express both hits and errors, and then choose the hits.

first 2026-05-30 18:17 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:17 Luciano states [WhatsApp Ptt 2026-05-30 at 18.16.35.md [01:19]] `note:2026-05-30T18.16.35:expresar-antes-de-elegir`: "lo primero que uno puede hacer es ver cómo expresarlo bien, después, una vez que vos lo expresás, podés expresar los aciertos y los errores y bueno, después el…"

### L-pencil-and-database-two-layers (language)

A pencil-and-paper language and one needing a database of empirical runs are not opposite philosophies but two layers or moments: you express the ideas with pencil and paper and then go to execution and the database.

first 2026-05-30 18:18 by Luciano; 4 rows, 3 witnesses, 1 days, last 2026-05-30

- 2026-05-30 18:18 Luciano states [WhatsApp Ptt 2026-05-30 at 18.17.51.md [00:14]] `note:2026-05-30T18.17.51:lapiz-papel-y-base-de-datos-no-son-opuestos`: "Vos podés ejecutarlo con la pici papel y mirar una base de datos con cuidado o que alguien te diga de la base de datos cuál es el resultado. Podés expresarlo c…"
- 2026-05-30 18:18 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.17.51.md [00:30]] `note:2026-05-30T18.17.51:dos-capas-dos-momentos`: "Pero sí, son dos capas, dos momentos. Y no es que uno sea una aspiración de la concesión."
- 2026-05-30 18:18 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.17.51.md [00:38]] `day:2026-05-30:lapiz-papel-y-base-de-datos-dos-capas`: "La idea básica es que vos puedas expresar las ideas con lápiz y papel y después es que vayas."
- 2026-05-30 18:18 Luciano restates [WhatsApp Ptt 2026-05-30 at 18.17.51.md [00:38]] `note:2026-05-30T18.17.51:expresar-ideas-primero-ejecutar-despues`: "La idea básica es que vos puedas expresar las ideas con lápiz y papel y después es que vayas."

### L-quantifiers-first-class (language)

The logical quantifiers 'for all' and 'exists' must be first-class citizens of Luthier.

first 2026-05-31 20:10 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-05-31

- 2026-05-31 20:10 Luciano states [WhatsApp Ptt 2026-05-31 at 20.10.19.md [00:00]] `note:2026-05-31T20.10.19:cuantificadores-logicos-como-fundamentales`: "una de las cosas fundamentales es poder escribir para todos y existe esos indicadores lógicos"
- 2026-05-31 20:10 Luciano restates [WhatsApp Ptt 2026-05-31 at 20.10.46.md [00:04]] `day:2026-05-31:cuantificadores-ciudadanos-de-primera`: "Así que los cuantificadores lógicos tendrían que estar, ser ciudadanos de primera en Luthier, claramente."
- 2026-05-31 20:10 Luciano restates [WhatsApp Ptt 2026-05-31 at 20.10.46.md [00:04]] `note:2026-05-31T20.10.46:cuantificadores-logicos-como-ciudadanos-de-primera`: "Así que los cuantificadores lógicos tendrían que estar, ser ciudadanos de primera en Luthier, claramente."

### L-limits-in-language (language)

Whether limits should be writable in the language; since limits are written with 'for all' and 'exists', the quantifiers already cover them.

first 2026-05-31 20:10 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-05-31

- 2026-05-31 20:10 Luciano questions [WhatsApp Ptt 2026-05-31 at 20.10.19.md [00:10]] `note:2026-05-31T20.10.19:expresar-limites`: "No sé si los límites también habría que poder escribirlos, habría que pensar un poco eso"
- 2026-05-31 20:10 Luciano states [WhatsApp Ptt 2026-05-31 at 20.10.46.md [00:00]] `day:2026-05-31:limites-se-escriben-con-cuantificadores`: "Bueno, límites se escriben con para todo y existe."

### L-first-class-citizens-open (language)

Which elements are first-class citizens in Luthier remains to be reviewed.

first 2026-05-31 20:10 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-05-31

- 2026-05-31 20:10 Luciano questions [WhatsApp Ptt 2026-05-31 at 20.10.46.md [00:12]] `note:2026-05-31T20.10.46:cuales-son-los-ciudadanos-de-primera`: "Habría que ver un poco todo eso... De cuáles son los ciudadanos de primera en Luthier."

### L-von-neumann-epigraph (other)

Luthier's epigraph is Von Neumann's reply: define exactly what thinking is and he'll build a machine that does it; Luthier is the project of making machines do whatever you can define well.

first 2026-06-03 12:03 by Luciano; 3 rows, 2 witnesses, 2 days, last 2026-08-31

- 2026-06-03 12:03 Luciano states [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:08]] `day:2026-06-03:cita-de-von-neumann-bajo-luthier`: "usted me dice que las máquinas no pueden pensar, bueno, dígame exactamente qué es pensar, qué es lo que las máquinas no pueden hacer, y bueno, yo voy a hacer u…"
- 2026-06-03 12:03 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:08]] `note:2026-06-03T12.03.35:cita-von-neumann-como-epigrafe`: "usted me dice que las máquinas no pueden pensar bueno, dígame exactamente qué es pensar qué es lo que las máquinas no pueden hacer y bueno, yo voy a hacer una…"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:cita-von-neumann`: "La cita fundante que elegiste es la de Von Neumann: \"dígame exactamente qué es lo que las máquinas no pueden hacer y hago una máquina que haga eso\"."

### L-language-for-defining-ideas (language)

Luthier is a language for defining things, where ideas are first-class citizens, like natural languages such as Spanish or English.

first 2026-06-03 12:04 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-06-03

- 2026-06-03 12:04 Luciano states [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:38]] `day:2026-06-03:luthier-lenguaje-donde-las-ideas-son-ciudadanos-de-primera`: "Luthier tendría que ser un lenguaje donde las ideas son ciudadanos de primera, o sea de definir ideas"
- 2026-06-03 12:04 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:38]] `note:2026-06-03T12.03.35:ideas-ciudadanos-de-primera`: "Luthier tendría que ser un lenguaje donde las ideas son ciudadanos de primera, o sea de definir ideas"
- 2026-06-03 12:04 Luciano restates [WhatsApp Ptt 2026-06-03 at 12.03.35.md [00:48]] `note:2026-06-03T12.03.35:analogia-lenguaje-natural`: "que sea un lenguaje como el castellano, como el inglés que son lenguajes que definen cosas"

### L-concrete-case-reveals-design (method)

Take a concrete implementation need (organizing the Gaussian-Newton algorithm class) and use it to ask what the underlying Luthier design problem is.

first 2026-06-05 13:09 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:09 Luciano states [WhatsApp Ptt 2026-06-05 at 13.09.45.md [00:00]] `note:2026-06-05T13.09.45:problema-concreto-como-lente-de-diseño`: "tengo un problema de macro IR, pero ¿qué es un problema de Luthier?"

### L-class-brings-structure-and-records (language)

Apply the Vector Space logic to a class: generate a class that already carries its structure and accessible records, rather than a bare structure.

first 2026-06-05 13:10 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:10 Luciano states [WhatsApp Ptt 2026-06-05 at 13.09.45.md [00:50]] `note:2026-06-05T13.09.45:logica-de-vector-space-para-generar-la-clase`: "yo quería un poco aplicarle la lógica de Vector Space, donde vos generás una clase que tiene ya la estructura y accesible de los distintos records."

### L-generic-iteration-status-class (language)

Iteration and status are concepts more general than their version in a particular algorithm, so there can be a generic status or iteration class, the instance knowing its algorithm from the context it sits inside.

first 2026-06-05 13:11 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:11 Luciano states [WhatsApp Ptt 2026-06-05 at 13.09.45.md [01:20]] `note:2026-06-05T13.09.45:conceptos-genericos-vs-instancia-por-contencion`: "iteración es un concepto más general que la iteración de un algoritmo de Gaussian-Newton... Entonces vos podés tener una clase estatus genérica."
- 2026-06-05 13:11 Luciano restates [WhatsApp Ptt 2026-06-05 at 13.09.45.md [01:33]] `day:2026-06-05:generic-status-and-iteration-across-algorithms`: "En todo algoritmo tienen iteraciones, en todo algoritmo tenés estatus. Entonces vos podés tener una clase estatus genérica."
- 2026-06-05 13:18 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 1] `dialogue:20260605T1318:iteracion-status-como-conceptos-genericos`: "iteración es un concepto más general que la iteración de un algoritmo de Gaussian-Newton. O sea, en todo algoritmo tienen iteraciones, en todo algoritmo tenés…"

### L-independent-vs-bound-concepts (language)

Some concepts can live independently of their container (a mean, separable from the variance) while others are intrinsically bound (an iteration is always the iteration of an algorithm).

first 2026-06-05 13:12 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:12 Luciano states [WhatsApp Ptt 2026-06-05 at 13.09.45.md [02:19]] `note:2026-06-05T13.09.45:componentes-separables-vs-ligados`: "la media, digamos, vos podés tenerla independiente, por ejemplo, de la varianza. Vive solita, tranquila... La iteración es la iteración, sí, es de un algoritmo"
- 2026-06-05 13:12 Luciano restates [WhatsApp Ptt 2026-06-05 at 13.09.45.md [02:28]] `day:2026-06-05:iteration-is-bound-unlike-the-mean`: "La iteración es la iteración, sí, es de un algoritmo y es de un algoritmo"
- 2026-06-05 13:18 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 1] `dialogue:20260605T1318:iteracion-pertenece-al-algoritmo`: "la media digamos vos podés tenerla independiente ... La iteraci es la iteraci s es de un algoritmo Y es de un algoritmo, o sea, que debería ser, debería tener…"

### L-iteration-carries-algorithm-id (language)

Because an iteration is bound to an algorithm, it should carry the identifier of the algorithm that creates it, itself structured (a method that is a creation of an MLE or MAP, which may use Gaussian-Newton).

first 2026-06-05 13:12 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:12 Luciano states [WhatsApp Ptt 2026-06-05 at 13.09.45.md [02:35]] `note:2026-06-05T13.09.45:identifier-del-algoritmo-como-procedencia`: "debería tener el identifier del algoritmo, posiblemente, es una creación de un MLE o un MAP o lo que sea"
- 2026-06-05 13:12 Luciano refines [WhatsApp Ptt 2026-06-05 at 13.09.45.md [02:46]] `day:2026-06-05:algorithm-identity-as-nested-specification`: "es una creación de un MLE o un MAP o lo que sea. Claro si es un MLE podría ser un MLE que usa Gaussian-Newton u otro método si es una máxima likelihood estimat…"

### L-record-as-relational-database (language)

What a record is can be stored as a relational database: fields with elements and relations, a record being a subset of the cartesian product with duplicates removed.

first 2026-06-05 13:13 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:13 Luciano states [WhatsApp Ptt 2026-06-05 at 13.09.45.md [03:58]] `day:2026-06-05:database-as-model-for-storing-what-a-thing-is`: "Claro, es un subconjunto del producto cartesiano, sería, ¿no? Una base de datos, de alguna manera..."
- 2026-06-05 13:13 Luciano restates [WhatsApp Ptt 2026-06-05 at 13.09.45.md [03:58]] `note:2026-06-05T13.09.45:modelo-relacional-para-guardar-que-es`: "Claro, es un subconjunto del producto cartesiano, sería, ¿no?"
- 2026-06-05 13:18 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 1] `dialogue:20260605T1318:base-de-datos-como-producto-cartesiano`: "Claro, es un subconjunto del producto cartesiano, sería, ¿no? Una base de datos, de alguna manera."

### L-forget-as-projection (language)

A first form of the forget function: get_iteration drops the whole context and leaves a bare iteration; forgetting is a projection onto an axis, a reduction of dimensionality.

first 2026-06-05 13:16 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:16 Luciano states [WhatsApp Ptt 2026-06-05 at 13.16.35.md [00:21]] `note:2026-06-05T13.16.35:funcion-olvido`: "Hacés get iteration de este objeto, bueno, te queda una iteración. ya ahí no sabés de qué es la iteración, es una iteración más"
- 2026-06-05 13:17 Luciano refines [WhatsApp Ptt 2026-06-05 at 13.16.35.md [00:44]] `note:2026-06-05T13.16.35:olvido-como-proyeccion`: "vos proyectás en uno de los ejes y entre los demás te olvidás ... es como una especie de proyección ... una reducción de dimensionalidad"
- 2026-06-05 13:17 Luciano restates [WhatsApp Ptt 2026-06-05 at 13.16.35.md [00:47]] `day:2026-06-05:forget-function-as-projection`: "si, lo olvidás sería, es como una especie de proyección una reducción de dimensionalidad"
- 2026-06-05 13:18 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 1] `dialogue:20260605T1318:funcion-olvido-como-proyeccion`: "es como si fuera una proyección que vos proyectás en uno de los ejes y en todos los demás te olvidás si lo olvido sería es como una especie de proyección una r…"

### L-rejoin-projections-recover (language)

The projections can be rejoined to recover the original object; the interesting case is disjoint or complementary (orthogonal) projections, reconstructible by pullback.

first 2026-06-05 13:17 by Luciano; 4 rows, 3 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:17 Luciano states [WhatsApp Ptt 2026-06-05 at 13.16.35.md [01:07]] `day:2026-06-05:reconstructing-the-object-from-its-projections`: "vos unís todas las proyecciones y recuperas el objeto original"
- 2026-06-05 13:17 Luciano restates [WhatsApp Ptt 2026-06-05 at 13.16.35.md [01:07]] `note:2026-06-05T13.16.35:reconstruccion-por-union-de-proyecciones`: "vos unís todas las proyecciones y recuperas el objeto original"
- 2026-06-05 13:18 model refines [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 2] `dialogue:20260605T1318:reconstruccion-por-pullback`: "matemáticamente podés hacer el producto cartesiano de las proyecciones para **reconstruir el objeto original en el espacio de alta dimensionalidad** sin perder…"
- 2026-06-05 13:18 Luciano restates [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 1] `dialogue:20260605T1318:reconstruccion-uniendo-proyecciones`: "vos unís todas las proyecciones y recuperas el objeto original ... vos tendrías como proyecciones que serían como disjuntas o complementarias ... que podrían s…"

### L-database-schema-is-category (language)

A database schema is a category (tables objects, foreign keys morphisms) and the loaded data is a functor.

first 2026-06-05 13:21 by model; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:21 model proposes [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 4] `dialogue:20260605T1318:base-de-datos-como-categoria`: "un esquema de base de datos es, en realidad, una **Categoría**, y que los datos cargados en ella son un **Functor**."

### L-database-topology (language)

The latent-structure questions of databases are problems of discrete topology.

first 2026-06-05 13:23 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:23 Luciano questions [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 5] `dialogue:20260605T1318:estructura-de-datos-como-topologia-discreta`: "esas cosas son son problemas de topología discretas Supongo no?"

### L-topology-reduces-to-integers (other)

Topology reduces geometry to the integers.

first 2026-06-05 13:26 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:26 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 7] `dialogue:20260605T1318:topologia-reduce-geometria-a-enteros`: "la topología lo que hace es reducir la geometría a los enteros, no de alguna manera esa cosa muy extraña."

### L-only-integers-exist (other)

Only the integers exist; the reals are a cartesian product of integers projected by powers of two.

first 2026-06-05 13:28 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:28 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 9] `dialogue:20260605T1318:solo-existen-los-enteros`: "Los Reales es un es un este un producto cartesiano de esteros proyectados por por este seamos por potencias de dos, o sea en realidad ni siquiera son enteros"

### L-iteration-as-successor-construction (language)

Iteration is defined by how it is built: an algorithm in a state has the step applied and the iteration increments (the successor), a dimension governed by the Peano naturals, and Luthier should write that easily.

first 2026-06-05 13:30 by model; 2 rows, 2 witnesses, 1 days, last 2026-06-05; taken up by Luciano 2026-06-05

- 2026-06-05 13:30 model proposes [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 12] `dialogue:20260605T1318:iteracion-como-sucesor-de-peano`: "La iteración es una dimensión del producto cartesiano gobernada por el tipo de los **Números Naturales tipo Peano**."
- 2026-06-05 13:30 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 11] `dialogue:20260605T1318:iteracion-definida-por-su-construccion`: "vos tenés un algoritmo en un estado y vos le aplicas el paso al algoritmo y la interacción Se incrementa. Eso es la definición de iteración ... si luthier tend…"

### L-status-as-enumerated-states (language)

A status cannot be a string but a number of possible algorithm states (converged, not converged, ...), each defined by its invariants.

first 2026-06-05 13:39 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:39 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 13] `dialogue:20260605T1318:status-como-enum-de-invariantes`: "no puede ser un String tiene que ser como si fuera un este número de este de posibles estados del este del algoritmo cada uno que está definido este Por cierta…"

### L-newton-raphson-first-application (method)

Write Newton-Raphson with all its invariants typed as Luthier's initial application, possibly publishable.

first 2026-06-05 13:50 by Luciano; 2 rows, 2 witnesses, 2 days, last 2026-06-26

- 2026-06-05 13:50 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 15] `dialogue:20260605T1318:newton-raphson-como-aplicacion-inicial`: "Escribir no el algoritmo Newton rapson y con todos los las invariantes tipadas y todo eso este como aplicación inicial de luthier suena como una buena movida n…"
- 2026-06-26 08:12 Luciano restates [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 27] `dialogue:20260626T0748:toy-model-newton-raphson`: "ya tenemos este un modelo de juguete que sería, qué sé yo, implementar el... top rapson o algo así. O sea, que eso no es el tema."

### L-publish-arxiv (method)

Publish it the way physicists do, on arXiv, and let it spread.

first 2026-06-05 13:51 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:51 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 17] `dialogue:20260605T1318:publicar-en-arxiv`: "también puedo hacerla la que hacen todos y hacerlo en el arca de físicos y este y listo no y después bueno de ahí que se difunda"

### L-grammar-and-interpreter (method)

Specify the language with a grammar and implement it in weeks to have a DSL that applies Luthier; an interpreter is already running for some things.

first 2026-06-05 13:58 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-06-05

- 2026-06-05 13:58 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 23] `dialogue:20260605T1318:gramatica-y-diesel-ya-corriendo`: "hacer una una gramática ... que especifica el lenguaje y luego implementarla quizás en semanas y listo y tener un diesel que aplique luthier. Por ejemplo este…"

### L-successor-beyond-naturals (language)

The successor function could apply to sets other than the naturals (the successor of an algorithm, the successor in the presidency); open whether it only makes sense under an isomorphism with the naturals.

first 2026-06-05 14:05 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-06-05

- 2026-06-05 14:05 Luciano states [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 27] `dialogue:20260605T1318:sucesor-generalizado`: "tiene sentido aplicar la función sucesor para conjuntos que no sean los naturales. Por ejemplo yo estaba pensando sucesor de un algoritmo no por ejemplo, sí un…"
- 2026-06-05 14:10 Luciano questions [2026-06-05_20260605T1318_bueno-tengo-un-problema-de-macro-y-r-per.md turn 29] `dialogue:20260605T1318:sucesor-requiere-isomorfismo-con-naturales`: "la función sucesor hoy únicamente tiene Sentido Cuando vos Estás ante un omiomorfismo con los números naturales?"

### L-topos-talk-validates (other)

The Topos Institute talk on higher-dimensional syntax is the theoretical base of what is designed for Luthier, uniting HoTT, constructive logic and a commutative graph structure.

first 2026-06-26 08:07 by model; 1 rows, 1 witnesses, 1 days, last 2026-06-26

- 2026-06-26 08:07 model states [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 22] `dialogue:20260626T0748:grafo-como-geometria-higher-dimensional-syntax`: "este video valida que el camino que trazaste —unir HoTT, lógica constructiva y una estructura de grafos conmutativa— no solo es una "locura hermosa", sino que…"

### L-forward-vs-history-info (language)

A state engine distinguishes information that flows forward from information kept for history, as Luthier's context manager and memory.

first 2026-06-26 08:09 by model; 1 rows, 1 witnesses, 1 days, last 2026-06-26

- 2026-06-26 08:09 model states [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 24] `dialogue:20260626T0748:fibrado-cofibrado-state-engine`: "Define qué información fluye hacia adelante (fibrado) y qué se guarda para el historial (cofibrado)."

### L-error-as-remembering (language)

Error messages are the opposite of forgetting, a well-structured remembering of why one erred, a comonad dual to the forgetful functor.

first 2026-06-26 08:12 by model; 2 rows, 2 witnesses, 1 days, last 2026-06-26; taken up by Luciano 2026-06-26

- 2026-06-26 08:12 model proposes [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 28] `dialogue:20260626T0748:diagnosis-comonad`: "Me gusta mucho tu visión de que el sistema de errores sea una **comónada**."
- 2026-06-26 08:12 Luciano states [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 27] `dialogue:20260626T0748:error-messages-as-remembering-opposite-of-forgetting`: "los mensajes de error eh que serían como lo contrario de de olvido, ¿no? Porque sería el recuerdo de por qué me equivoqué. Este, tendrían que estar bien estruc…"

### L-error-as-subgraph (language)

In a graph-based program an error returns the failed sub-graph, with each node carrying an origin/trace consulted when validation fails.

first 2026-06-26 08:12 by model; 1 rows, 1 witnesses, 1 days, last 2026-06-26

- 2026-06-26 08:12 model proposes [2026-06-26_20260626T0748_https-youtu-be-qexaebypcpg-si-kuznuih28t.md turn 28] `dialogue:20260626T0748:error-as-failed-subgraph`: "Si el programa es un grafo, el error podría devolvernos el **sub-grafo fallido**, no solo una línea de texto."

### L-ai-needs-structure (language)

Luthier's homoiconic, graph-and-dependent-type structure gives an AI the structural reasoning about the world that statistical LLMs lack.

first 2026-06-28 22:16 by model; 2 rows, 1 witnesses, 1 days, last 2026-06-28

- 2026-06-28 22:16 model proposes [2026-06-29_20260628T2122_https-youtu-be-edivgibm-ya-si-cfowvzaauu.md turn 44] `dialogue:20260628T2122:codigo-homoiconico-para-que-la-ia-comprenda-la-arquitectura`: "permita que la IA no solo \"adivine\" el siguiente token, sino que \"comprenda\" la arquitectura del sistema que está construyendo"
- 2026-06-28 22:16 model proposes [2026-06-29_20260628T2122_https-youtu-be-edivgibm-ya-si-cfowvzaauu.md turn 44] `dialogue:20260628T2122:luthier-razonamiento-estructural-sobre-el-mundo-fisico`: "tu propuesta de modelar la realidad mediante grafos (DAGs) y tipos dependientes (HoTT) ataca exactamente este vacío fundamental: la necesidad de un *razonamien…"

### L-build-before-ai-falls (method)

Luthier should be built now, before the highly qualified AI guidance might be restricted or all this falls.

first 2026-08-28 15:21 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-28

- 2026-08-28 15:21 Luciano states [WhatsApp Ptt 2026-08-28 at 15.20.59.md [00:10]] `day:2026-08-28:urgency-build-luthier-before-access-restricts`: "pienso que tengo que hacer Luthier antes de que todo esto se caiga"

### L-luthier-abstract-algebra (language)

Luthier has to do with abstract algebra.

first 2026-08-28 15:21 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-28

- 2026-08-28 15:21 Luciano states [WhatsApp Ptt 2026-08-28 at 15.20.59.md [00:19]] `day:2026-08-28:luthier-tied-to-abstract-algebra`: "Luthier tiene que ver, para mí con el álgebra abstracta"
- 2026-08-28 15:21 Luciano states [WhatsApp Ptt 2026-08-28 at 15.20.59.md [00:19]] `note:2026-08-28T15.20.59:luthier-y-algebra-abstracta`: "Luthier tiene que ver, para mí con el álgebra abstracta"

### L-platform-sharing-wins (language)

Luthier is a platform where sharing your information makes you win, because the act of sharing raises the value of your own information.

first 2026-08-28 15:21 by Luciano; 3 rows, 2 witnesses, 2 days, last 2026-08-31

- 2026-08-28 15:21 Luciano states [WhatsApp Ptt 2026-08-28 at 15.20.59.md [00:25]] `day:2026-08-28:platform-where-sharing-makes-you-win`: "hacer una plataforma donde la gente pueda compartir información de manera de que salga ganando"
- 2026-08-28 15:21 Luciano states [WhatsApp Ptt 2026-08-28 at 15.20.59.md [00:25]] `note:2026-08-28T15.20.59:plataforma-donde-compartir-hace-valer-mas`: "tiene que ver con hacer una plataforma donde la gente pueda compartir información de manera de que salga ganando" `[00:25]`; "vos compartís tu información y tu…"
- 2026-08-31 20:10 model restates [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:plataforma-datos-correlacionados`: "Luthier como plataforma donde compartir información te hace ganar, porque los datos correlacionados valen más que los aislados; subís tu dato y a cambio sabés…"

### L-correlated-data-worth-more (other)

Correlated data points are worth more than isolated ones, and detecting larger patterns needs ever more data.

first 2026-08-28 15:23 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-28

- 2026-08-28 15:23 Luciano states [WhatsApp Ptt 2026-08-28 at 15.22.59.md [00:06]] `day:2026-08-28:shared-information-is-worth-more`: "los puntos aislados valen menos que los puntos correlacionados"
- 2026-08-28 15:23 Luciano states [WhatsApp Ptt 2026-08-28 at 15.22.59.md [00:06]] `note:2026-08-28T15.22.59:informacion-correlacionada-vale-mas`: "los puntos aislados valen menos que los puntos correlacionados"

### L-data-upload-reciprocity (language)

The minimal reciprocity of uploading your datum: the database gains your datum and you learn where you stand relative to the rest.

first 2026-08-28 15:23 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-28

- 2026-08-28 15:23 Luciano states [WhatsApp Ptt 2026-08-28 at 15.22.59.md [00:37]] `day:2026-08-28:knowing-where-you-stand-as-minimal-reciprocity`: "la base de datos obtiene tu dato y vos obtenés dónde estás en ese dato respecto del resto"
- 2026-08-28 15:23 Luciano states [WhatsApp Ptt 2026-08-28 at 15.22.59.md [00:37]] `note:2026-08-28T15.22.59:minima-reciprocidad-por-posicion-relativa`: "la base de datos obtiene tu dato y vos obtenés dónde estás en ese dato respecto del resto"

### L-error-management-guarantees (language)

The point of Luthier is that error management be better and results be guaranteed.

first 2026-08-31 19:50 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:50 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [02:35]] `day:2026-08-31:codigo-guarda-los-calculos`: "O sea, un poco la idea de Luthier es que la gestión del error sea mejor y básicamente eso, que digamos que las cosas estén garantizadas, es lo que yo digo."

### L-value-knows-operation (language)

A value knows the concrete operation that produced it: if it is the sum, it is the sum and not the generic magma operation.

first 2026-08-31 19:52 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:52 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [03:50]] `day:2026-08-31:la-operacion-lleva-su-identidad`: "si es la suma, ya es la suma y no es el magma, es la suma, no es la operación y el magma."
- 2026-08-31 19:52 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [03:50]] `note:2026-08-31T19.48.17:especificidad-de-la-operacion`: "si es la suma, ya es la suma y no es el magma, es la suma, no es la operación y el magma"

### L-views-of-operations (language)

From a series of operations one can take different views or levels: the magma, the result, the execution, the code.

first 2026-08-31 19:52 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:52 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [04:15]] `note:2026-08-31T19.48.17:niveles-de-una-operacion`: "esas operaciones vos podés tomar el magma, podés tomar el resultado, ejecución, el código"

### L-luthierize-foreign-code (language)

Luthier annotates foreign code (luthierizes it), e.g. matrix-inversion libraries, starting from the definition of what the function should do and the property it must satisfy.

first 2026-08-31 19:54 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:54 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [06:11]] `note:2026-08-31T19.48.17:luthierizar-codigo-ajeno`: "La idea es que Luthier sea como un anotador de código. Vos podrías luthierizar, por ejemplo, un código ajeno"
- 2026-08-31 19:54 Luciano restates [WhatsApp Ptt 2026-08-31 at 19.48.17.md [06:15]] `day:2026-08-31:luthier-anotador-de-codigo-ajeno`: "Vos podrías luthierizar, por ejemplo, un código ajeno, que yo de Python."

### L-properties-hold-within-error (language)

Declared properties (like an inverse recovering the value) hold only within a certain error, since inverse functions are not perfect.

first 2026-08-31 19:54 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:54 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [06:41]] `note:2026-08-31T19.48.17:propiedades-dentro-de-cierto-error`: "dentro de cierto error, porque bueno no es perfecta la inversa... por ejemplo el seno y el arcoseno no te da el mismo valor, perdés un pendejésimo por ahí"

### L-value-as-interval-sample (language)

A value is really an interval of values or a sample of values (as a Markov chain represented by a sample).

first 2026-08-31 19:55 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:55 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [07:10]] `day:2026-08-31:valor-con-error-intervalo-o-sample`: "yo tengo un valor, pero en realidad el valor es un intervalo de valores, por ejemplo,"
- 2026-08-31 19:55 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [07:10]] `note:2026-08-31T19.48.17:dato-con-error-intervalo-o-sample`: "el valor es un intervalo de valores... o puede ser que sea por ejemplo una sample de valores, en el caso de que sea una cadena de Markov, vos podes representar…"

### L-precision-depends-on-history (language)

The recoverable precision of a value depends on how much of its operational history is kept; forgetting the operation turns an exact value into an interval.

first 2026-08-31 19:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:56 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [08:07]] `note:2026-08-31T19.48.17:precision-segun-cuanto-recuerdes`: "si vos te acordás que tomaste el seno de 4... El arcoseno de seno es 4, chao. En cambio, si... te olvidás de la operación que hiciste... es un valor con un int…"

### L-code-follows-laws-not-floats (language)

Floating-point numbers do not obey the algebraic laws of numbers, but the code is assumed to, so it can be reorganized for a more efficient or more perfect execution.

first 2026-08-31 19:56 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:56 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [08:42]] `day:2026-08-31:floats-rompen-las-leyes-el-codigo-las-guarda`: "los números floating points, que no siguen las reglas, digamos, de los números,"
- 2026-08-31 19:56 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [08:42]] `note:2026-08-31T19.48.17:floating-point-no-cumple-las-leyes-el-codigo-si`: "los números floating points, que no siguen las reglas, digamos, de los números, no se han asociado... No las siguen, pero sí las siguen, digamos, lo que sería…"

### L-language-ai-uses (language)

Luthier should be a language used by the AI itself, not only by a human.

first 2026-08-31 19:57 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:57 Luciano states [WhatsApp Ptt 2026-08-31 at 19.57.14.md [00:00]] `day:2026-08-31:luthier-usa-la-ia-y-puede-auto-hackearse`: "O sea, Luthier tendría que ser un lenguaje que use la IA misma, ¿no?"
- 2026-08-31 19:57 Luciano states [WhatsApp Ptt 2026-08-31 at 19.57.14.md [00:00]] `note:2026-08-31T19.57.14:luthier-lenguaje-para-la-ia`: "Luthier tendría que ser un lenguaje que use la IA misma, ¿no?"

### L-self-hack-risk (language)

A risk to resolve is that the language or system auto-hacks itself.

first 2026-08-31 19:57 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:57 Luciano states [WhatsApp Ptt 2026-08-31 at 19.57.14.md [00:11]] `note:2026-08-31T19.57.14:riesgo-de-auto-hackeo`: "Lo que pasa es que puede ser que se auto-hackee."

### L-execution-as-forgetting (language)

Execution is a forgetful function: code generates code, with two levels, one that keeps the generated code and one that forgets it.

first 2026-08-31 19:58 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:58 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [09:56]] `day:2026-08-31:ejecucion-como-funcion-olvido-codigo-que-genera-codigo`: "Sí, o sea, básicamente, sí, es código que genera código,"
- 2026-08-31 19:58 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [09:56]] `note:2026-08-31T19.48.17:ejecucion-como-generacion-y-olvido`: "es código que genera código, que vos al ejecutar código lo que haces es transcribís código o ejecutás, y claro, como dos niveles de ejecución, una ejecución qu…"

### L-objective-unclear (method)

What Luthier is actually for is still open; so far it is an intellectual adventure whose objective is yet to be found.

first 2026-08-31 19:59 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 19:59 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [10:49]] `day:2026-08-31:objetivo-de-luthier`: "porque hasta ahora es como una aventura intelectual"
- 2026-08-31 19:59 Luciano states [WhatsApp Ptt 2026-08-31 at 19.48.17.md [10:49]] `note:2026-08-31T19.48.17:proposito-abierto`: "hasta ahora es como una aventura intelectual más que nada"

### L-pyluthier-type-as-decoration (language)

In a Python implementation the type is not a real host type but floats as an attribute, represented by fields and decorations; the easy but imperfect route.

first 2026-08-31 20:00 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:00 Luciano states [WhatsApp Ptt 2026-08-31 at 20.00.05.md [00:43]] `note:2026-08-31T20.00.05:piluthier-como-clase-atributo-flotante`: "lo llevas como una clase de un atributo básicamente va flotando así... creo que es lo más fácil"
- 2026-08-31 20:01 Luciano refines [WhatsApp Ptt 2026-08-31 at 20.00.05.md [01:45]] `note:2026-08-31T20.00.05:python-inadecuado-para-tipos`: "si vos tenés que escribir cosas con tipos y todo eso Python no es la herramienta"
- 2026-08-31 20:02 Luciano restates [WhatsApp Ptt 2026-08-31 at 20.00.05.md [02:03]] `note:2026-08-31T20.00.05:tipo-representado-por-campos-y-decoraciones`: "La realidad es que la herramienta no es un tipo de verdad, sino que... El tipo está representado por campos, por decoraciones."

### L-start-with-easiest-luthier (method)

Start with the easiest route, a kind of Luthier, rather than the harder C++ one, before committing to the final form.

first 2026-08-31 20:01 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:01 Luciano states [WhatsApp Ptt 2026-08-31 at 20.00.05.md [01:01]] `note:2026-08-31T20.00.05:implementacion-cpp-mas-dificil`: "en C++ es un poco más más difícil"
- 2026-08-31 20:01 Luciano states [WhatsApp Ptt 2026-08-31 at 20.00.05.md [01:33]] `note:2026-08-31T20.00.05:estrategia-empezar-por-lo-mas-facil`: "quizás lo más fácil es empezar con una especie de luthier"

### L-build-own-language-directly (language)

An alternative to implementing Luthier inside a host language is to build directly a language of one's own.

first 2026-08-31 20:01 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:01 Luciano states [WhatsApp Ptt 2026-08-31 at 20.00.05.md [01:07]] `note:2026-08-31T20.00.05:luthier-como-lenguaje-propio`: "casi la otra es hacer directamente un lenguaje de uno mismo"

### L-recover-meaning-via-luthier (method)

Since the AI now writes all the code and he no longer sees or feels it, Luthier is the way to recover contact with meaning and have things guaranteed without looking at the code.

first 2026-08-31 20:10 by model; 2 rows, 2 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:10 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 2] `dialogue:e6fc53cf:motivaciones-de-agosto`: "Luthier es la forma de recuperar el contacto con el significado, que las cosas estén garantizadas aunque no mires el código. ... Luthier como plataforma donde…"
- 2026-08-31 20:10 model states [2026-08-31_f453278e_lee-todos-los-audios.md turn 2] `dialogue:f453278e:ia-recuperar-significado`: "la IA escribe todo el código, ya no lo ves ni lo sentís, y Luthier es la forma de recuperar el contacto con el significado, que las cosas estén garantizadas au…"

### L-infectability-lens (method)

Consolidation uses infectability as its lens (the ideas that most change how you program are the ones that most structure the language), a choice specific to this project.

first 2026-08-31 20:14 by model; 2 rows, 2 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:14 model states [2026-08-31_f453278e_lee-todos-los-audios.md turn 4] `dialogue:f453278e:infectabilidad-como-lente`: "usando infectabilidad como lente (el criterio de PRINCIPIOS: las ideas que más cambian la forma de programar son las que más estructuran el lenguaje), agrupand…"
- 2026-08-31 20:55 model restates [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 16] `dialogue:e6fc53cf:lente-de-infectabilidad-es-la-eleccion`: "llevan la lente de infectabilidad, que fue una elección tuya para este proyecto (las ideas que más cambian la forma de programar son las que más estructuran el…"

### L-mentor-friction (method)

The mentor step takes the consolidation and produces friction on the design process without designing itself, and Luciano answers in new audios, closing the cycle.

first 2026-08-31 20:14 by model; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:14 model states [2026-08-31_f453278e_lee-todos-los-audios.md turn 4] `dialogue:f453278e:mentor-fricciona-no-disena`: "toma el consolidado y produce fricción sobre el proceso de diseño, no diseña él. Vos le respondés en audios nuevos ... y el ciclo se cierra."

### L-pipeline-method (method)

The working method is the pipeline audios then ideas then consolidation then mentor.

first 2026-08-31 20:14 by model; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:14 model states [2026-08-31_f453278e_lee-todos-los-audios.md turn 4] `dialogue:f453278e:pipeline-audios-ideas`: "es el pipeline audios → ideas → consolidación → mentor, y después de ese ciclo recién viene escribir la especificación."

### L-spec-after-cycle (method)

The specification is the first document that makes decisions (excluding what the audios still let coexist), written on paper after the audios-ideas-consolidation-mentor cycle.

first 2026-08-31 20:14 by model; 3 rows, 3 witnesses, 1 days, last 2026-08-31; taken up by Luciano 2026-08-31

- 2026-08-31 20:14 model proposes [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 4] `dialogue:e6fc53cf:especificacion-tras-el-ciclo`: "primero Luthier como lenguaje que describe invariantes, fijar sintaxis y semántica en papel, y recién entonces implementar. O sea, el output del ciclo alimenta…"
- 2026-08-31 20:21 Luciano confirms [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 5] `dialogue:e6fc53cf:interes-por-la-especificacion`: "es muy interesante esta propuesta:"
- 2026-08-31 20:21 model refines [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 6] `dialogue:e6fc53cf:especificacion-es-decidir`: "La especificación es otra cosa: es el primer documento que toma decisiones, y una decisión se reconoce porque excluye algo que en los audios todavía convive."

### L-date-both-consolidations (method)

Keep the earlier consolidation by renaming it and dating both versions, so the ecosystem's evolution can be compared.

first 2026-08-31 20:16 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:16 Luciano states [2026-08-31_f453278e_lee-todos-los-audios.md turn 5] `dialogue:f453278e:conservar-consolidado-mayo`: "si renombralo y ponele fecha a ambos"

### L-example-before-principle (method)

No principle enters the specification without an example worked by hand in the candidate notation; the canonical cases test whether there is a language.

first 2026-08-31 20:21 by model; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:21 model proposes [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 6] `dialogue:e6fc53cf:disciplina-ejemplo-en-papel`: "ningún principio entra a la especificación sin un ejemplo resuelto a mano en la notación candidata."

### L-pipeline-forgetting (method)

The consolidation cost growing with the corpus is the forget-functor problem applied to the pipeline itself, to be handled by consolidating in batches or from a previous consolidate.

first 2026-08-31 20:52 by model; 1 rows, 1 witnesses, 1 days, last 2026-08-31

- 2026-08-31 20:52 model states [2026-08-31_e6fc53cf_lee-todos-los-audios.md turn 12] `dialogue:e6fc53cf:olvido-aplicado-al-pipeline`: "habrá que pensar en consolidar por tandas o partir de un consolidado previo, que además es exactamente el problema del functor olvido aplicado al propio pipeli…"

### L-grows-to-universe-risk (method)

Luthier risks accumulating without advancing and diffusing until it encompasses the whole universe, becoming useless; it must stay operative and practical.

first 2026-09-02 10:48 by Luciano; 3 rows, 3 witnesses, 2 days, last 2026-09-21

- 2026-09-02 10:48 Luciano states [WhatsApp Ptt 2026-09-02 at 10.48.25.md [00:00]] `day:2026-09-02:luthier-no-arranca-acumula`: "Lutier es un proyecto que acumula, acumula, acumula energía, ideas, todo, y no termina de empezar a avanzar."
- 2026-09-02 10:48 Luciano states [WhatsApp Ptt 2026-09-02 at 10.48.25.md [00:13]] `note:2026-09-02T10.48.25:tension-proyecto-del-congreso`: "es un poco el proyecto del Congreso, algo que va creciendo hasta abarcar el universo, lo cual es lindo y a la vez es como una bolsa de gas"
- 2026-09-21 11:44 Luciano restates [WhatsApp Ptt 2026-09-21 at 11.42.19.md [02:16]] `note:2026-09-21T11.42.19:efecto-congreso`: "las cosas crecen hasta ser iguales al universo, son inútiles, es un poema nada más, pero la idea es que sea algo que sea operativo y práctico"

### L-two-growth-paths (language)

Luthier can grow two ways: as a universal arena, or more simply as a lambda-calculus-like, more down-to-earth language.

first 2026-09-02 10:48 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:48 Luciano states [WhatsApp Ptt 2026-09-02 at 10.48.25.md [00:34]] `day:2026-09-02:dos-caminos-de-crecimiento`: "es como que luthier puede crecer por dos maneras. Una, digamos, es como una especie de arena universal, y la otra es más simple, es tratar de que sea como una…"
- 2026-09-02 10:48 Luciano states [WhatsApp Ptt 2026-09-02 at 10.48.25.md [00:34]] `note:2026-09-02T10.48.25:dos-maneras-de-crecer`: "luthier puede crecer por dos maneras. Una, digamos, es como una especie de arena universal, y la otra es más simple, es tratar de que sea como una especie de l…"

### L-universal-yet-semantic (language)

Luthier should be algebraically universal (able to write almost anything, like a universal Turing machine) while every element is semantically defined and human-understandable.

first 2026-09-02 10:49 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:49 Luciano states [WhatsApp Ptt 2026-09-02 at 10.48.25.md [01:10]] `day:2026-09-02:semantica-algebraica-universal`: "una forma de escribirse a sí mismo que sea muy algebraica en el sentido de que pueda escribir casi cualquier cosa, como una especie de máquina de Turín univers…"
- 2026-09-02 10:49 Luciano restates [WhatsApp Ptt 2026-09-02 at 10.48.25.md [01:10]] `note:2026-09-02T10.48.25:semantica-algebraica-universal`: "una forma de escribirse a sí mismo que sea muy algebraica en el sentido de que pueda escribir casi cualquier cosa, como una especie de máquina de Turín univers…"
- 2026-09-02 10:49 Luciano restates [WhatsApp Ptt 2026-09-02 at 10.48.25.md [01:29]] `note:2026-09-02T10.48.25:significado-humano-traducible`: "como que cada elemento esté semánticamente definido de alguna manera, o sea que tenga algún significado que los humanos podamos entender o que se pueda traslad…"

### L-python-spirit (language)

Luthier imitates Python's spirit of letting human ideas be expressed easily (with the Monty Python / Luthier wordplay).

first 2026-09-02 10:50 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:50 Luciano states [WhatsApp Ptt 2026-09-02 at 10.48.25.md [01:47]] `day:2026-09-02:espiritu-python`: "era un poco la idea de Python suena, pero bueno Python un poco tenía ese espíritu me parece, con lo cual bueno en Luthier la idea es como que imita la idea de…"
- 2026-09-02 10:50 Luciano restates [WhatsApp Ptt 2026-09-02 at 10.48.25.md [01:54]] `note:2026-09-02T10.48.25:analogia-python`: "en Luthier la idea es como que imita la idea de Python o sea Python, Monty Python, Luthier"

### L-recursive-lisp-nicer (language)

Luthier is imagined as a recursive language in the line of Lisp but nicer.

first 2026-09-02 10:53 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:53 Luciano states [WhatsApp Ptt 2026-09-02 at 10.53.08.md [00:00]] `day:2026-09-02:lenguaje-recursivo-tipo-lisp`: "me imagino a Luthier como un lenguaje recursivo, también un poco como LISC, una idea como LISC pero un poco más lindo"
- 2026-09-02 10:53 Luciano restates [WhatsApp Ptt 2026-09-02 at 10.53.08.md [00:00]] `note:2026-09-02T10.53.08:luthier-lenguaje-recursivo-tipo-lisp`: "me imagino a Luthier como un lenguaje recursivo, también un poco como LISC... una idea como LISC pero un poco más lindo, no sé, algo así tendría que ser"

### L-code-mathematical-equivalence (language)

A Luthier code has a clear mathematical equivalence.

first 2026-09-02 10:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:53 Luciano states [WhatsApp Ptt 2026-09-02 at 10.53.08.md [00:15]] `note:2026-09-02T10.53.08:equivalencia-matematica-clara`: "y que tenga una equivalencia matemática clara, que es un código de Luthier"

### L-what-is-a-program (language)

The basic question of Luthier: what is a Luthier program, a map or a graph?

first 2026-09-02 10:53 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:53 Luciano questions [WhatsApp Ptt 2026-09-02 at 10.53.08.md [00:29]] `note:2026-09-02T10.53.08:que-es-un-programa-mapa-o-grafo`: "La pregunta en realidad básica es, de Luthier, sería, bueno, ¿qué es un programa de Luthier? ¿Es un mapa? ¿Es un grafo, por ejemplo?"
- 2026-09-02 10:53 Luciano questions [WhatsApp Ptt 2026-09-02 at 10.53.08.md [00:33]] `day:2026-09-02:que-es-un-programa-de-luthier`: "¿qué es un programa de Luthier? ¿Es un mapa? ¿Es un grafo, por ejemplo?"

### L-program-composition-harmonic (language)

The fundamental problem is how Luthier programs connect and expand one another so they compose and grow harmonically.

first 2026-09-02 10:54 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:54 Luciano states [WhatsApp Ptt 2026-09-02 at 10.53.08.md [01:07]] `day:2026-09-02:composicion-de-programas`: "Quizás ese es un poco el problema fundamental, ¿no? O sea, la composición de programas de Luthiers en sentido de que crezcan armónicamente"
- 2026-09-02 10:54 Luciano states [WhatsApp Ptt 2026-09-02 at 10.53.08.md [01:13]] `note:2026-09-02T10.53.08:composicion-de-programas-problema-fundamental`: "la composición de programas de Luthiers en sentido de que crezcan armónicamente"

### L-compile-detects-incompatibility (language)

Compiling checks whether code contains incompatibilities (errors); many programs must be non-compilable, unlike an algebraic calculation where any expression computes something.

first 2026-09-02 10:54 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:54 Luciano states [WhatsApp Ptt 2026-09-02 at 10.53.08.md [01:34]] `note:2026-09-02T10.53.08:incompatibilidades-en-la-composicion`: "si vos tenés dos programas de luthier, de alguna manera los ponés entre comillas con pilas juntos, bueno, ¿cuál es el resultado? O sea, tendría que haber incom…"
- 2026-09-02 10:55 Luciano refines [WhatsApp Ptt 2026-09-02 at 10.53.08.md [01:52]] `day:2026-09-02:compilacion-como-deteccion-de-incompatibilidades`: "esa es la idea de compilar, ¿no? O sea, vos compilás el código, ves si contiene errores, es decir, cosas que son incompatibles entre sí, cosa que no ocurre con…"
- 2026-09-02 10:55 Luciano restates [WhatsApp Ptt 2026-09-02 at 10.53.08.md [02:29]] `note:2026-09-02T10.53.08:compilar-como-deteccion-de-incompatibilidades`: "la idea es que sí, que haya muchos programas que no sean compilables porque bueno, justamente es la manera de detectar errores en la programación"

### L-universal-adapter (language)

Using a library requires it to follow patterns and satisfy propositions defined from Luthier, and an adapter fits each library to the use, so Luthier works as a universal adapter between libraries.

first 2026-09-02 10:56 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-09-02

- 2026-09-02 10:56 Luciano states [WhatsApp Ptt 2026-09-02 at 10.53.08.md [03:35]] `note:2026-09-02T10.53.08:librerias-requieren-proposiciones`: "yo defino como que están disponibles ciertas funciones, que tienen ciertas propiedades, o sea que siguen ciertas proposiciones definidas desde Luthier"
- 2026-09-02 10:57 Luciano refines [WhatsApp Ptt 2026-09-02 at 10.53.08.md [04:13]] `day:2026-09-02:librerias-por-propiedades-y-adaptador-universal`: "en ese sentido Luthier serviría como una especie de adaptador universal entre distintas librerías."
- 2026-09-02 10:57 Luciano restates [WhatsApp Ptt 2026-09-02 at 10.53.08.md [04:13]] `note:2026-09-02T10.53.08:luthier-adaptador-universal`: "en ese sentido Luthier serviría como una especie de adaptador universal entre distintas librerías"

### L-representation-fields-vs-json (language)

Whether a result is represented with fixed fields or relational JSON: the set of result types is open but each type is closed, a sum of types rather than a JSON blob.

first 2026-09-13 08:49 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:49 Luciano questions [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 8] `dialogue:f16636f6:representacion-campos-fijos-o-no`: "ahi me doy cuenta que la representacion no es la de tabla sino de json relacionales donde no tenes campos fijos? o quizas si fijos?"
- 2026-09-13 08:50 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:tipos-de-resultado-como-suma-de-tipos`: "El conjunto de tipos de resultado es abierto, vos agregás tipos nuevos ... pero cada tipo individual es cerrado. Eso es una suma de tipos, no un blob."

### L-store-record-function-version (language)

Apply Luthier to the analysis store by recording each result's generating function and version and keeping a table of functions.

first 2026-09-13 08:49 by Luciano; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:49 Luciano states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 8] `dialogue:f16636f6:aplicar-luthier-al-esquema-de-procedencia`: "estoy muy tentado a aplicar conceptos de luthier aqui ... si ponemos la funcion y la version que lo genero, bien podemos tambien hacer una tabla de funciones"

### L-closed-vs-open-world (language)

Luthier verifies a closed world at compile time; for open-world field data, invariants are required at creation of derived objects but observed data gets a validation with a verdict, never a rejection.

first 2026-09-13 08:50 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:50 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:mundo-cerrado-vs-mundo-abierto`: "Luthier verifica en un mundo cerrado, en tiempo de compilación."

### L-derived-is-proof-term (language)

A derived object (inputs, function, parameters, result) is a proof term whose type is the proposition that the result was obtained that way, so the database is a store of proofs.

first 2026-09-13 08:50 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:50 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:objeto-derivado-como-termino-de-prueba`: "el objeto derivado es la tupla (entradas, función, parámetros, resultado). Eso es literalmente un término de prueba."

### L-precondition-is-type (language)

A precondition is guaranteed by the argument's type, verified when the reference is formed; predicates on values require refined types, and a function failing its postcondition yields a stored failed-attempt object.

first 2026-09-13 08:50 by model; 2 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:50 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:precondicion-como-tipo-del-argumento`: "En Luthier la precondición la garantiza el tipo del argumento."
- 2026-09-13 08:50 model refines [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:tipo-refinado-geometria-bien-condicionada`: "`geometría bien condicionada` es un tipo distinto de `geometría`, y quién habita cuál se decide al momento de crear"

### L-schema-from-type (language)

The storage schema is generated from the function's declared type in the code rather than hand-written, and migration is derived.

first 2026-09-13 08:50 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:50 model proposes [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:esquema-como-proyeccion-del-tipo`: "el esquema se genera desde el tipo declarado de la función."

### L-verify-by-sampling (language)

Luthier verifies postconditions by sampling possible inputs, and postcondition verification and coverage calibration are the same computation.

first 2026-09-13 08:50 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 08:50 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 9] `dialogue:f16636f6:postcondicion-verificada-muestreando-entradas`: "Luthier verifica postcondiciones muestreando entradas posibles."

### L-original-vs-derivative-types (language)

There are original types generated from audios and questionnaires; all other types are derivative (results of functions) and therefore necessarily structured.

first 2026-09-13 09:09 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-13

- 2026-09-13 09:09 Luciano states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 10] `dialogue:f16636f6:originales-vs-derivados`: "Hay tipos \"originales\" que se generan mediante la combinacion de audios y questionarios. Todos los otros tipos son derivativos, de modo que tienen necesariam…"
- 2026-09-13 09:10 Luciano refines [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 12] `dialogue:f16636f6:derivativo-es-resultado-de-funcion`: "por derivativos digo, resultado de funciones"

### L-function-must-be-deterministic (language)

If identity is (inputs, function, version, parameters), the function must be deterministic: the seed and everything from the environment enter as explicit arguments, or the certificate lies.

first 2026-09-13 09:10 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 09:10 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 13] `dialogue:f16636f6:funcion-es-determinista-semilla-como-parametro`: "Función quiere decir determinista, y eso tiene costo."

### L-never-edit-derived (language)

A derived object is never edited; corrections are new human assertions (originals), so labels, quality control and corrections all land in the same place.

first 2026-09-13 09:10 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-13

- 2026-09-13 09:10 model states [2026-09-13_f16636f6_analisis-de-lo-que-voy-escribiendo.md turn 13] `dialogue:f16636f6:nunca-se-edita-un-objeto-derivado`: "nunca se edita un objeto derivado."

### L-couple-with-sonolocalizacion (method)

Luthier is a meta-project whose next development couples to sonolocalizacion, at the library stage (and macro IR); how to relate the two is still to be resolved.

first 2026-09-21 11:42 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-09-21

- 2026-09-21 11:42 Luciano states [WhatsApp Ptt 2026-09-21 at 11.42.19.md [00:33]] `day:2026-09-21:luthier-como-meta-proyecto-ligado-a-sonolocalizacion`: "cuando yo ya empiece a ver el tema librerías, yo tengo que ya empezar a trabajar con Luthier"
- 2026-09-21 11:42 Luciano refines [WhatsApp Ptt 2026-09-21 at 11.42.19.md [00:33]] `note:2026-09-21T11.42.19:luthier-acoplado-a-sonolocalizacion`: "cuando yo ya empiece a ver el tema librerías, yo tengo que ya empezar a trabajar con Luthier, y yo creo que con macro IR también, o sea, tengo que empezar a ve…"

### L-butler-of-knowledge (language)

Luthier is used together with the AI as a kind of butler of knowledge.

first 2026-09-21 11:43 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-09-21

- 2026-09-21 11:43 Luciano states [WhatsApp Ptt 2026-09-21 at 11.42.19.md [00:57]] `day:2026-09-21:luthier-y-la-ia-mayordomo-del-conocimiento`: "usar Luthier como una especie de mayordomo del conocimiento, algo así"
- 2026-09-21 11:43 Luciano restates [WhatsApp Ptt 2026-09-21 at 11.42.19.md [00:57]] `note:2026-09-21T11.42.19:luthier-mayordomo-del-conocimiento`: "cómo, digamos, usar Luthier como una especie de mayordomo del conocimiento, algo así"

### L-must-be-useful (method)

Luthier must be useful and take root in something real, not stay purely theoretical, used at a rough level to hit reality and reveal its limits.

first 2026-09-21 11:43 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-09-21

- 2026-09-21 11:43 Luciano states [WhatsApp Ptt 2026-09-21 at 11.42.19.md [01:21]] `day:2026-09-21:luthier-tiene-que-ser-util`: "el tema con Luthier creo que es que tiene que ser útil, tiene que servir para algo que no sea algo puramente teórico"
- 2026-09-21 11:43 Luciano refines [WhatsApp Ptt 2026-09-21 at 11.42.19.md [01:21]] `note:2026-09-21T11.42.19:luthier-tiene-que-ser-util`: "el tema con Luthier creo que es que tiene que ser útil, tiene que servir para algo que no sea algo puramente teórico, sino algo que ya se eche raíces en algo"

### L-usefulness-gap (method)

Find the gap of usefulness, a concrete place from which Luthier can begin to develop while being useful.

first 2026-09-21 11:44 by Luciano; 2 rows, 1 witnesses, 1 days, last 2026-09-21

- 2026-09-21 11:44 Luciano states [WhatsApp Ptt 2026-09-21 at 11.42.19.md [01:52]] `day:2026-09-21:el-hueco-de-utilidad`: "tenemos que encontrar el hueco de utilidad de donde Luthier puede empezar a desarrollarse siendo útil"
- 2026-09-21 11:44 Luciano restates [WhatsApp Ptt 2026-09-21 at 11.42.19.md [01:52]] `note:2026-09-21T11.42.19:hueco-de-utilidad`: "tenemos que encontrar el hueco de utilidad de donde Luthier puede empezar a desarrollarse siendo útil"

### L-fundamental-elements-question (language)

What are the most fundamental elements of a program: elementary types, elementary functions, code vs data, true/false, true-by-definition, address/data?

first 2026-09-28 20:56 by Luciano; 5 rows, 5 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 1] `dialogue:175c0408:candidatos-elementos-fundamentales`: "cuales son los elementos mas fundamentales de un programa? ... tipos elementales, funciones elementales, codigo vs dato (en eso como R que pasa de uno al otro)…"
- 2026-09-28 20:56 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 1] `dialogue:890a551c:candidatos-a-elementos-fundamentales`: "tipos elementales, funciones elementales, codigo vs dato (en eso como R que pasa de uno al otro), el concepto de verdadero y falso? el concepto de verdadero po…"
- 2026-09-28 20:56 model rejects [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:direccion-dato-rechazada`: "El nombre es la referencia; la dirección de memoria es una decoración del nivel más bajo de equivalencia ... Sin mutación y sin tiempo, un puntero no tiene qué…"
- 2026-09-28 22:21 Luciano questions [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 9] `dialogue:20260928T2208:alternativas-para-turing-universalidad`: "En una vision moderna, se usarian los mismos elementos o hay otras formas alternativas de adquirir turing unversalidad?"
- 2026-09-28 22:25 Luciano restates [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 12] `dialogue:20260928T2208:implementar-luthier-con-elementos-atomicos`: "quiero implementar mi lenguage luthier y estoy viendo cuales serian sus elementos primitivos, pienso inspirarme en Lisp Haskell C++ lambda calculus, python y R…"

### L-bootstrap-pact (language)

The only non-Luthier thing is the bootstrap pact: an implementation (in C or anything) accepts a Program value and mechanically applies the rules until eval runs on itself, after which the bootstrapper can be thrown away (self-extensibility).

first 2026-09-28 20:56 by model; 3 rows, 3 witnesses, 2 days, last 2026-09-29

- 2026-09-28 20:56 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:pacto-de-arranque`: "Lo único primitivo es el pacto de arranque: la implementación acepta un valor de `Program` y lo trata como programa."
- 2026-09-29 05:06 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:175c0408:arranque-tirable`: "Una vez que `eval` escrito en Luthier corre sobre sí mismo, el arrancador se puede tirar y reemplazar por cualquier otro. Esa es la autoextensibilidad concreta."
- 2026-09-29 05:06 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:890a551c:arranque-descartable`: "Una vez que `eval` escrito en Luthier corre sobre sí mismo, el arrancador se puede tirar y reemplazar por cualquier otro. Esa es la autoextensibilidad concreta."

### L-core-five-pieces (language)

The core is five pieces: the definition (with the hole), lambda calculus with reduction, U, Π and data; from data come Σ, =, ⊥, ⊤, N, Program, and Bayes, the run database and numbers-with-error stay outside as libraries.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:nucleo-cinco-piezas`: "El núcleo queda en cinco piezas: la definición (con el hueco), el cálculo lambda con reducción, `U`, `Π`, `data`. ... El olvido es `fst` de un `Σ`; qué olvidar…"
- 2026-09-28 20:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:nucleo-de-cinco-piezas`: "El núcleo queda en cinco piezas: la definición (con el hueco), el cálculo lambda con reducción, `U`, `Π`, `data`. Con `data` se definen `Σ` ... Bayes, la base…"

### L-defeq-vs-identity (language)

"True by definition" is the definitional equality ≡ (two terms reducing to the same normal form, a judgment the reducer decides), distinct from =, the identity type ("true with evidence") whose terms are paths.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:igualdad-definicional-vs-identidad`: "Es la igualdad definicional `≡` de la teoría de tipos: dos términos que reducen a la misma forma normal. No es una proposición, es un juicio que decide el redu…"
- 2026-09-28 20:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:igualdad-definicional-vs-identidad`: "Es la igualdad definicional `≡` de la teoría de tipos: dos términos que reducen a la misma forma normal. No es una proposición, es un juicio que decide el redu…"

### L-definition-is-fundamental (language)

The most fundamental element of a Luthier program is the definition (name : Type := term); a program is a finite unordered set of definitions and the DAG comes from which names each uses.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model proposes [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:definicion-como-unidad`: "el elemento más fundamental de un programa Luthier no es el tipo ni la función. Es la **definición**, `nombre : Tipo := término`. Un programa es un conjunto fi…"
- 2026-09-28 20:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:la-definicion-como-unidad`: "El elemento más fundamental de un programa Luthier no es el tipo ni la función. Es la **definición**, `nombre : Tipo := término`. Un programa es un conjunto fi…"

### L-forget-is-fst-sigma (language)

Forgetting is fst of a Σ; what to forget is library policy.

first 2026-09-28 20:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:olvido-es-fst`: "El olvido es `fst` de un `Σ`; qué olvidar es política de librería."

### L-hole-unifies-roles (language)

The hole, a definition with type and no body (f : A to B := ?), plays five roles at once (axiom, program input, external function, pending definition, dead code), and don't execute until defined is its semantics, removing the need for an External type.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:hueco-cinco-papeles`: "el **hueco**: una definición con tipo y sin cuerpo, `f : A → B := ?`. Una sola cosa cumple cinco papeles: axioma, input del programa, función externa que el en…"
- 2026-09-28 20:56 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:el-hueco`: "Una sola cosa cumple cinco papeles: axioma, input del programa, función externa que el entorno llena, definición pendiente, código muerto. Tu principio \"no ej…"

### L-name-reference-not-address (language)

The name is the reference; the memory address is a decoration of the lowest level of equivalence, and without mutation or time a pointer has nothing to distinguish.

first 2026-09-28 20:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:direccion-no-es-primitiva`: "El nombre es la referencia; la dirección de memoria es una decoración del nivel más bajo de equivalencia (vos mismo la pusiste ahí en el audio del 30 de mayo).…"

### L-next-recursor-then-syntax (method)

What to attack next, in order: choose the recursor (without the dependent one there are no general paths proven by induction), then the concrete syntax, since only read aloud will you know if it is a language.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:siguiente-recursor-luego-sintaxis`: "elegir el recursor (sin el dependiente no podés probar el `∀` por inducción, o sea no hay paths generales), y después la sintaxis concreta, porque hasta que no…"
- 2026-09-28 20:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:recursor-dependiente-primero`: "elegir el recursor (sin el dependiente no podés probar el `∀` por inducción, o sea no hay paths generales), y después la sintaxis concreta, porque hasta que no…"

### L-primitives-are-formers (language)

The primitives are the type formers (U, Pi, data), not elementary types or functions; N is defined with data, R is a structure with axioms, seno is a hole.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:formadores-no-tipos-elementales`: "Lo primitivo son los formadores (`U`, `Π`, `data`), no `int` ni `seno`. `N` se define con `data`; la suma, por recursión; `R` es una estructura con axiomas; `s…"
- 2026-09-28 20:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:formadores-no-tipos-elementales`: "Lo primitivo son los formadores (`U`, `Π`, `data`), no `int` ni `seno`. `N` se define con `data`; la suma, por recursión; `R` es una estructura con axiomas; `s…"

### L-program-data-no-selfhack (language)

Program is an inductive type (a list of definitions) and eval is a partial function Program→Name→Maybe Term; there is no eval that injects arbitrary terms into the type system, which prevents self-hacking.

first 2026-09-28 20:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:codigo-como-dato-estilo-lisp`: "`Program` es un tipo inductivo (lista de definiciones) y `eval` es una función parcial `Program → Name → Maybe Term`. No hay un `eval` que inyecte términos arb…"

### L-proposition-is-type-truth (language)

True/false is not Bool: a proposition is a type, true if it has a term; ⊤ and ⊥ are the extremes and Bool is a datum with two constructors.

first 2026-09-28 20:56 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:175c0408:verdadero-falso-como-tipos`: "Una proposición es un tipo y es verdadera si tiene un término; `⊤` y `⊥` son los extremos, `Bool` es un dato más definido con dos constructores."
- 2026-09-28 20:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:proposicion-es-un-tipo`: "Una proposición es un tipo y es verdadera si tiene un término; `⊤` y `⊥` son los extremos, `Bool` es un dato más definido con dos constructores."

### L-refl-test-is-code (language)

The rule tying ≡ and = (if a≡b then refl types as a=b) makes it literal that the test is the code itself: testing an instance is reducing and seeing refl types, proving the ∀ is building the path.

first 2026-09-28 20:56 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 20:56 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 2] `dialogue:890a551c:el-test-es-el-propio-codigo`: "La regla que une las dos (si `a ≡ b`, entonces `refl` tipa como `a = b`) es lo que hace literal \"el test es el propio código\": testear una instancia es reduc…"

### L-core-vs-surface-syntax (language)

A minimal ontological core (what the evaluator understands) must be strictly separated from the surface syntax and sugar.

first 2026-09-28 22:25 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 22:25 model states [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 13] `dialogue:20260928T2208:separar-nucleo-de-sintaxis-de-superficie`: "exige separar estrictamente dos capas: 1. **El Núcleo Ontológico Mínimo (Core IR / Semántica Atómica):** ... 2. **La Sintaxis de Superficie y Azúcar Sintáctico…"

### L-labeled-tuple-atomic-datum (language)

The unifying atomic datum is a labeled immutable tuple/structure, unifying Lisp s-expressions and Haskell ADTs, with contiguous same-type vectors as a performance special case.

first 2026-09-28 22:25 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 22:25 model states [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 13] `dialogue:20260928T2208:tupla-inmutable-etiquetada-como-dato-atomico`: "El elemento atómico unificador debe ser una **Tupla/Estructura Inmutable Etiquetada** ... $$\text{Node} = \langle \text{Tag}, [v_0, v_1, \dots, v_{n-1}] \rangl…"

### L-macros-ast-functions (language)

The compiler exposes its AST as a data type and macros are ordinary functions Expr→Expr run at compile time, so all surface syntax desugars to the core.

first 2026-09-28 22:25 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 22:25 model states [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 13] `dialogue:20260928T2208:macros-como-funciones-expr-a-expr`: "Una macro en *Luthier* es simplemente una función ordinaria: $$\text{macro} : \text{Expr} \to \text{Expr}$$"

### L-mutation-cells-linear (language)

The core should include controlled mutation cells (alloc/load/store) and linear/affine ownership so functional transforms can mutate buffers in place without garbage collection.

first 2026-09-28 22:25 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 22:25 model states [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 13] `dialogue:20260928T2208:puente-cpp-mutacion-y-recursos-lineales`: "el núcleo atómico debe incorporar dos conceptos de bajo nivel: - **Efecto / Celda de Mutación Controlada (`ref` o `cell`):** ... - **Semántica de Propiedad Lin…"

### L-six-operational-primitives (language)

Any Luthier program reduces to six operational primitives (var, lambda, apply, case/match, letrec, quote), with the conditional subsumed by pattern matching on boolean constructors.

first 2026-09-28 22:25 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-28

- 2026-09-28 22:25 model states [2026-09-29_20260928T2208_pronostico-para-hoy.md turn 13] `dialogue:20260928T2208:seis-formas-especiales-primitivas`: "Cualquier programa en *Luthier* se reduce internamente a un árbol de expresiones gobernado por solo 6 primitivas operacionales ... **`var`** ... **`lambda`** .…"

### L-hole-symbol-needed (language)

The hole needs no symbol in the core: a bare bodyless declaration f:A→B is already a hole (f opaque, f a does not reduce), and ? is only derivable surface sugar inside a term.

first 2026-09-29 04:20 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:20 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 3] `dialogue:175c0408:por-que-simbolo-hueco`: "porque necesitamos el simbolo para el hueco, ?. No basta con decri f: A-> B y no definirlo?"
- 2026-09-29 04:20 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 3] `dialogue:890a551c:por-que-el-simbolo-del-hueco`: "porque necesitamos el simbolo para el hueco, ?. No basta con decri f: A-> B y no definirlo?"
- 2026-09-29 04:26 model corrects [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 6] `dialogue:175c0408:hueco-es-declaracion-sin-cuerpo`: "No hace falta el símbolo en el núcleo. Lo primitivo es "declaración sin cuerpo": `f : A → B` a secas ya es un hueco, y su semántica es la que dije: `f` es un n…"
- 2026-09-29 04:26 model confirms [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 6] `dialogue:890a551c:hueco-es-la-declaracion-sin-cuerpo`: "No hace falta el símbolo en el núcleo. Lo primitivo es \"declaración sin cuerpo\": `f : A → B` a secas ya es un hueco ... Así que `?` es azúcar de la superfici…"

### L-hole-in-term-goal (language)

A hole inside a term lets the verifier accept what is written and report the exact type of what is missing (Agda's goal), which is the compiler with good messages about what is happening.

first 2026-09-29 04:26 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:26 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 6] `dialogue:890a551c:hueco-interno-da-el-goal`: "Con un hueco dentro del término, el verificador acepta el 90% escrito y te dice el tipo exacto de lo que falta (en Agda eso es el \"goal\"). Eso es tu \"compil…"

### L-hole-no-intention (language)

The bare hole does not mark intention (whether a bodyless function will be filled by numpy or is just unwritten); the core need not distinguish, and huecos:Program→List Name lists all, intention going in the definition's text field.

first 2026-09-29 04:26 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:26 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 6] `dialogue:175c0408:hueco-intencion-no-semantica`: "si `sin : R → R` está sin cuerpo porque lo va a llenar numpy o porque todavía no lo escribiste. El núcleo no distingue y no tiene por qué; `huecos : Program →…"
- 2026-09-29 04:26 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 6] `dialogue:890a551c:intencion-del-hueco-va-en-texto`: "El núcleo no distingue y no tiene por qué; `huecos : Program → List Name` te los lista a todos y la intención va en el campo de texto de la definición, si lo a…"

### L-language-indicates-knowledge (language)

Luthier is a language that indicates knowledge: a:A is a judgment, not a proposition, read in Martin-Löf's sense where its meaning depends on which kind of type A is and a bodyless hole is an epistemic assumption.

first 2026-09-29 04:30 by Luciano; 5 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:30 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 7] `dialogue:175c0408:luthier-lenguaje-que-indica-conocimiento`: "tengo que pensar luthier como un lenguaje que indica conocimiento. a : A en hott significa que A es verdad y que a es una prueba de ello o mejor dicho que exis…"
- 2026-09-29 04:30 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 7] `dialogue:890a551c:luthier-lenguaje-que-indica-conocimiento`: "tengo que pensar luthier como un lenguaje que indica conocimiento. a : A en hott significa que A es verdad y que a es una prueba de ello o mejor dicho que exis…"
- 2026-09-29 04:31 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:175c0408:a-es-A-como-juicio-martin-lof`: "Lo que vos llamás "lenguaje que indica conocimiento" es exactamente la lectura de Martin-Löf, anterior a HoTT: un juicio es un acto de conocimiento, y una prop…"
- 2026-09-29 04:31 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:890a551c:a-es-A-es-un-juicio-y-niveles`: "`a : A` no es una proposición, es un juicio: \"a es un término del tipo A\". Lo que significa depende de qué clase de tipo es `A`, y HoTT tiene un nombre para…"
- 2026-09-29 04:31 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:890a551c:juicio-como-acto-de-conocimiento`: "Lo que vos llamás \"lenguaje que indica conocimiento\" es exactamente la lectura de Martin-Löf, anterior a HoTT: un juicio es un acto de conocimiento, y una pr…"

### L-evidence-in-sigma-erasable (language)

"More specific with types" means types are data and knowledge about a value is carried as an evidence component in a Σ marked erasable (like a refinement type), but in Luthier the evidence is sometimes written and kept, and who defines marks it erasable, not the language.

first 2026-09-29 04:31 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:31 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:175c0408:evidencia-borrable-en-sigma`: "los tipos son datos ... y el conocimiento sobre un valor se lleva como componente de evidencia en un `Σ`, marcado como borrable. ... La diferencia con Luthier…"
- 2026-09-29 04:31 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:890a551c:evidencia-borrable-en-sigma`: "los tipos son datos ... y el conocimiento sobre un valor se lleva como componente de evidencia en un `Σ`, marcado como borrable ... La diferencia con Luthier s…"

### L-know-that-vs-which (language)

The distinction to keep from HoTT is knowing that (a mere proposition's proof) versus knowing which (a set's value); the passage from the second to the first is truncation, the most basic forgetting, where the forget functor begins.

first 2026-09-29 04:31 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:31 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:175c0408:saber-que-vs-saber-cual`: "saber *que* contra saber *cuál*. Un valor de un conjunto es saber cuál (`4 : N`). Una prueba de una proposición mera es saber que (`p : 0 < 4`). El pasaje del…"
- 2026-09-29 04:31 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 8] `dialogue:890a551c:saber-que-vs-saber-cual`: "saber *que* contra saber *cuál*. Un valor de un conjunto es saber cuál (`4 : N`). Una prueba de una proposición mera es saber que (`p : 0 < 4`). El pasaje del…"

### L-dot-separator (language)

The dot in Σ(x:X). A x is a notational separator between the bound variable and the body, the same as in λx.t and Π(x:A).B (like { in a function body), and one convention should cover the three binding forms.

first 2026-09-29 04:33 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:33 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 9] `dialogue:175c0408:punto-como-ligador`: "Σ (x : X). A x. que significa aca el punto?"
- 2026-09-29 04:33 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 10] `dialogue:175c0408:punto-separador-notacion`: "El punto es solo un separador de notación: marca dónde termina la variable ligada y empieza el cuerpo. ... como el punto también sirve en `λ x. t` y en `Π (x :…"
- 2026-09-29 04:33 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 10] `dialogue:890a551c:el-punto-como-separador-ligador`: "como el punto también sirve en `λ x. t` y en `Π (x : A). B`, una sola convención para las tres formas ligadoras deja claro dónde empieza y termina cada alcance…"
- 2026-09-29 04:34 Luciano restates [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 11] `dialogue:175c0408:punto-como-llave-de-C`: "seria como "{" en f(x) { return x*x}"

### L-syntax-decl-instant (language)

Reduce Luthier's syntax to only declarations and instantiations.

first 2026-09-29 04:41 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:41 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 13] `dialogue:175c0408:reducir-sintaxis-declaraciones-instanciaciones`: "Estoy pensando en reducir la sintaxis de luthier solo a declaraciones y a instantiaciones."
- 2026-09-29 04:41 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 13] `dialogue:890a551c:solo-declaraciones-e-instanciaciones`: "Estoy pensando en reducir la sintaxis de luthier solo a declaraciones y a instantiaciones."

### L-block-is-program (language)

Braces delimit a block that can hold local definitions; a block is a Program with one definition marked as output, giving local definitions without new primitives.

first 2026-09-29 04:42 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:42 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:890a551c:bloque-como-programa-local`: "`\\ x { y : A := x + x ; y }` sería una función cuyo cuerpo es un pequeño programa (un DAG chico) con un resultado. Eso te da definiciones locales sin agregar…"

### L-equality-symbols (language)

Four signs for four equalities: := defines (an asymmetric act on the program), = is the identity type (the proposition), == is library decidable equality A→A→Bool, and ≡ the definitional one is not written in programs (Lean's convention).

first 2026-09-29 04:42 by model; 5 rows, 5 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:42 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:890a551c:usar-dos-puntos-igual-para-definir`: "Usar `:=` para definir, no `=`. Vas a usar `=` como proposición ... Si `=` también define, `f : A -> A = t` se lee como \"f tiene tipo `(A -> A = t)`\" y hay a…"
- 2026-09-29 04:45 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 15] `dialogue:175c0408:llaves-fundamentales`: "Si, las llaves son fundamentales. puedo usar := y = o = y == ?"
- 2026-09-29 04:45 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 15] `dialogue:890a551c:llaves-fundamentales`: "Si, las llaves son fundamentales. puedo usar := y = o = y == ?"
- 2026-09-29 04:45 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 16] `dialogue:175c0408:tres-igualdades-con-tres-simbolos`: "`:=` define. Es un acto sobre el programa (instanciar un nombre), no una proposición dentro de él. ... `=` es el tipo identidad, la proposición. ... `==` (si l…"
- 2026-09-29 04:45 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 16] `dialogue:890a551c:tres-igualdades-con-su-simbolo`: "`:=` define. Es un acto sobre el programa ... `=` es el tipo identidad, la proposición ... `==` (si lo querés) es la igualdad decidible, una función `A -> A ->…"

### L-no-parameterless-lambda (language)

A parameterless lambda should not exist in Luthier: without time or effects \(){a+a} and a+a are the same value, a consequence of the commutativity of statements.

first 2026-09-29 04:42 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:42 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:175c0408:lambda-sin-parametro-no-existe`: "una lambda sin parámetros no debería existir en Luthier: sin tiempo ni efectos, `\ () { a + a }` y `a + a` son el mismo valor, no hay nada que "demorar". Es un…"
- 2026-09-29 04:42 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:890a551c:lambda-sin-parametros-no-existe`: "una lambda sin parámetros no debería existir en Luthier: sin tiempo ni efectos, `\ () { a + a }` y `a + a` son el mismo valor, no hay nada que \"demorar\". Es…"

### L-one-binding-form (language)

One binding form nombre:Tipo appears identically in declaration, parameter, dependent type and pair, with A→B sugar for (_:A)→B, scope given by parentheses and braces.

first 2026-09-29 04:42 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:42 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:175c0408:una-sola-forma-ligar-nombres`: "Una sola forma para ligar nombres, `nombre : Tipo` ... Las llaves tienen una ventaja sobre el punto que vale la pena explotar: delimitan un bloque, y un bloque…"
- 2026-09-29 04:42 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:890a551c:una-sola-forma-de-ligar-nombres`: "Una sola forma para ligar nombres, `nombre : Tipo`, que aparezca igual en la declaración `a : A`, en el parámetro `\\ (x : A) { ... }`, en el tipo dependiente…"

### L-separate-type-from-term (language)

Prefer the notation that separates type from term (f:A→A := \(x){x+x}): instantiation is a declaration plus := término, with one way to build functions (the lambda) and one to write their type (the arrow), serving named and anonymous alike.

first 2026-09-29 04:42 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:42 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:175c0408:notacion-tipo-separado-del-termino`: "La instanciación es literalmente la declaración más `:= término`, igual que `a : A := 4`. Una función es un valor como cualquier otro, hay una sola forma de co…"
- 2026-09-29 04:42 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 14] `dialogue:890a551c:separar-tipo-de-termino`: "La segunda, `f : A -> A := \ (x) { x + x }`, separa el tipo del término. La instanciación es literalmente la declaración más `:= término`, igual que `a : A :=…"

### L-coloneq-act-vs-defeq (language)

:= is the act that gives a name a body, while ≡ is the relation following from all the := plus the computation rules (lambda substitution, recursor rules); each := gives a ≡ but ≡ is larger, so "true by definition" broadly is true by unfolding and computing.

first 2026-09-29 04:48 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:48 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 18] `dialogue:175c0408:subst-define-da-un-equiv`: "cada `:=` te da un `≡` (el nombre es definicionalmente igual a su cuerpo), pero `≡` es más grande que eso: incluye la sustitución de la lambda y las reglas del…"
- 2026-09-29 04:48 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 18] `dialogue:890a551c:definir-da-un-definicional-pero-mas-estrecho`: "cada `:=` te da un `≡` (el nombre es definicionalmente igual a su cuerpo), pero `≡` es más grande que eso: incluye la sustitución de la lambda y las reglas del…"

### L-refl-checks-defeq (language)

To assert a definitional equality as a check in a program, the way is _ : a = b := refl, which types only if a≡b, so no fourth symbol is needed.

first 2026-09-29 04:48 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:48 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 18] `dialogue:175c0408:refl-pide-chequeo-definicional`: "Si algún día querés afirmar en un programa "estos dos términos tienen que ser definicionalmente iguales" como chequeo, el modo es `_ : a = b := refl`, que tipa…"
- 2026-09-29 04:48 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 18] `dialogue:890a551c:refl-pide-chequeo-definicional`: "Si algún día querés afirmar en un programa \"estos dos términos tienen que ser definicionalmente iguales\" como chequeo, el modo es `_ : a = b := refl`, que ti…"

### L-application-binds-tightest (language)

Application binds tighter than any operator, so f a + g b is (f a)+(g b), the convention that makes formulas read as formulas.

first 2026-09-29 04:52 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:52 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 22] `dialogue:175c0408:aplicacion-liga-mas-fuerte`: "la aplicación liga más fuerte que cualquier operador, así que `f a + g b` es `(f a) + (g b)`."

### L-juxtaposition-application (language)

Use juxtaposition f a in the core (f(a) is the same since (a) is a in parens); f a b is curried application, f(a,b) applies to a pair, the two coexisting as distinct types, and multiplication must be explicit.

first 2026-09-29 04:52 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:52 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 22] `dialogue:175c0408:juxtaposicion-para-aplicacion`: "Juxtaposición, `f a`, en el núcleo. Y la razón principal es que no te obliga a elegir: `f(a)` es exactamente lo mismo, porque `(a)` es `a` entre paréntesis. ..…"
- 2026-09-29 04:52 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 22] `dialogue:890a551c:juxtaposicion-para-aplicar`: "`f a b` aplica una función currificada, y `f (a, b)` aplica una función a un par. Son dos funciones de tipos distintos, `A -> B -> C` y `A × B -> C`, y pasar d…"

### L-fa-three-data (language)

An application f a is three data all used, visible only when the program looks at its own code: the unevaluated term (code), the normal form (result), and the run f a→a+a as a term of an inductive Traza type; inside a program f a and a+a are ≡ by referential transparency.

first 2026-09-29 04:56 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:56 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 23] `dialogue:175c0408:f-a-tres-cosas`: "f a (sin evaluar) a+ a (evaluado) f a -> a + a ( ambos) y los tres se usan."
- 2026-09-29 04:56 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 23] `dialogue:890a551c:tres-niveles-de-f-a`: "f a (sin evaluar) a+ a (evaluado) f a -> a + a ( ambos) y los tres se usan."
- 2026-09-29 04:57 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:175c0408:tres-niveles-codigo-resultado-corrida`: "`f a` sin evaluar es un término de `Term` ... `a + a` es otro término de `Term`, la forma normal. Es el resultado. ... `f a -> a + a` es un tercer dato: la cor…"
- 2026-09-29 04:57 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:890a551c:tres-niveles-son-tres-datos`: "La distinción aparece solo cuando el programa mira su propio código, es decir en el nivel de `Term` y `Program` ... `f a -> a + a` es un tercer dato: la corrid…"

### L-confluence-traces-paths (language)

Since ≡ is confluent, the order of reduction steps affects only cost and termination, not the result; two traces from f a to a+a are two paths between the same points, the finest grain of "different paths with different speed".

first 2026-09-29 04:57 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:57 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:175c0408:confluencia-paths-con-distinta-velocidad`: "Eso es tu "distintos paths con distinta velocidad" en el grano más fino: dos trazas distintas de `f a` a `a + a` son dos caminos entre los mismos puntos. ... "…"
- 2026-09-29 04:57 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:890a551c:confluencia-y-paths-de-distinta-velocidad`: "Eso es tu \"distintos paths con distinta velocidad\" en el grano más fino: dos trazas distintas de `f a` a `a + a` son dos caminos entre los mismos puntos."

### L-eval-two-versions-forget (language)

eval has two versions, the two levels of execution: eval_r returns result and run, eval_o forgets the run with fst; the order of forgetting is run, then result-with-proposition, then result alone.

first 2026-09-29 04:57 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:57 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:890a551c:eval-que-recuerda-y-que-olvida`: "`eval` tiene dos versiones ... una que recuerda y una que olvida ... El olvido de la corrida es `fst`, como todo olvido."

### L-quote-sugar-for-term (language)

To write f a as data within a program without writing app(ref f)(ref a) by hand, use the Lisp quote '(f a) as sugar, the parser producing the Term constructors.

first 2026-09-29 04:57 by model; 5 rows, 5 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:57 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:175c0408:comilla-lisp-para-codigo-como-dato`: "Es la comilla de Lisp, `'(f a)`. Alguna azúcar hace falta, porque la vas a usar todo el tiempo, pero es azúcar: el parser produce los constructores de `Term`."
- 2026-09-29 04:57 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:890a551c:comilla-de-lisp-como-azucar`: "Es la comilla de Lisp, `'(f a)`. Alguna azúcar hace falta, porque la vas a usar todo el tiempo, pero es azúcar: el parser produce los constructores de `Term`."
- 2026-09-29 09:19 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 96] `dialogue:890a551c:quote-y-evalstore`: "me queda quote y evalstore ?"
- 2026-09-29 09:19 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 97] `dialogue:890a551c:quote-nombres-vs-valores`: "Yo haría que `'` guarde nombres (es lo que significa quote) y que `[| |]` sustituya los valores de las variables ligadas antes de guardar, porque es un registr…"
- 2026-09-29 09:22 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 99] `dialogue:890a551c:quote-necesita-delimitadores`: "quote necesita delimitadores ... La opción más consistente con lo que llevamos es un prefijo más las llaves, que es exactamente Scala 3: `'{ f x }`."

### L-unevaluated-syntactic (language)

"Unevaluated" is not a runtime state like a thunk because there is no time; it is a syntactic datum, which eliminates lazy-evaluation semantics.

first 2026-09-29 04:57 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 04:57 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 24] `dialogue:890a551c:sin-evaluar-es-dato-sintactico-no-thunk`: "\"sin evaluar\" no es un estado en tiempo de ejecución, como sería un thunk en Haskell, porque no hay tiempo. Es un dato sintáctico. Eso simplifica mucho: no h…"

### L-term-syntax-as-data (language)

Term is the type of Luthier's syntax defined in Luthier itself with data (one constructor per form of writing a term), so code is the first element because syntax is a data like N; its definition is a Def of Program and the verifier written in Luthier can verify the program defining it, metacircular.

first 2026-09-29 05:00 by model; 3 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:00 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 26] `dialogue:175c0408:term-sintaxis-como-data`: "Así es como "el código es el primer elemento": no porque haya un operador mágico sino porque la sintaxis es un `data` como `N` o `List`. ... `Term` es un tipo…"
- 2026-09-29 05:00 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 26] `dialogue:890a551c:core-metacircular`: "`Term` es un tipo de Luthier, así que su propia definición es un `Def`, un dato de `Program`. El verificador escrito en Luthier puede verificar el programa que…"
- 2026-09-29 05:00 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 26] `dialogue:890a551c:term-sintaxis-como-dato`: "`Term` es el tipo de la sintaxis de Luthier, definido en Luthier mismo con `data`. Es el árbol sintáctico: un término del programa, visto como dato ... no porq…"

### L-term-untyped-check (language)

Term as defined is untyped (raw) syntax whose sense is decided by check; a Term admitting only well-typed terms exists and is more elegant but much harder, so raw syntax plus check suffices to start, as almost all real verifiers do.

first 2026-09-29 05:00 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:00 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 26] `dialogue:175c0408:sintaxis-cruda-mas-check`: "La alternativa, un `Term` que solo admita términos bien tipados, existe y es más elegante pero mucho más difícil de escribir; para empezar, sintaxis cruda más…"
- 2026-09-29 05:00 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 26] `dialogue:890a551c:term-crudo-mas-check`: "`Term` así definido es sintaxis sin tipar ... Que tenga sentido lo decide `check` ... para empezar, sintaxis cruda más `check` alcanza y es lo que hacen casi t…"

### L-check-infer-bidirectional (language)

check traverses the definitions verifying each type is a type and each body has its declared type, infer computes the type by recursion over Term, and real verifiers are bidirectional (some forms infer, others are checked against a type); that is where refl types or not.

first 2026-09-29 05:06 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:06 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:890a551c:check-bidireccional`: "por eso los verificadores reales son bidireccionales: unas formas infieren, otras se chequean contra un tipo dado ... Ese `≡` se decide llamando a `eval` sobre…"

### L-data-type-constructors-recursor (language)

A data gives three things: the type, the constructors (ordinary bodyless functions in normal form), and the recursor (one case per constructor, each with a reduction rule); every function over the type is an instance of this recursor.

first 2026-09-29 05:06 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:06 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:175c0408:recursor-es-lo-unico-que-da-data`: "obtenés tres cosas: el tipo `Term : U`; los siete constructores, que son funciones ordinarias ... y el recursor, una función que sabe recorrer un `Term` dando…"

### L-eval-fuel-total (language)

eval repeating a step is not structural recursion and does not always terminate, so the honest exit is fuel, eval:N→Program→Term→Maybe Term, making it total, and "how much fuel was needed" is the first cost measure, for free.

first 2026-09-29 05:06 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:06 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:175c0408:eval-necesita-combustible`: "La salida honesta es darle combustible: `eval : N -> Program -> Term -> Maybe Term`, que hace a lo sumo `k` pasos y devuelve `nothing` si se acabó. Con combust…"
- 2026-09-29 05:06 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:890a551c:eval-necesita-combustible`: "La salida honesta es darle combustible: `eval : N -> Program -> Term -> Maybe Term`, que hace a lo sumo `k` pasos ... Con combustible, `eval` es una función to…"

### L-substitution-capture (language)

Substitution has the variable-capture problem; the cheap fix for the by-hand version is requiring all bound names distinct, the serious fix is de Bruijn indices (changing ref:Name→Term to var:N→Term for bound variables).

first 2026-09-29 05:06 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:06 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:175c0408:de-bruijn-vs-nombres-unicos`: "La solución barata para la versión a mano es exigir que los nombres ligados de un programa sean todos distintos entre sí y distintos de los globales; la soluci…"
- 2026-09-29 05:06 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:890a551c:captura-de-variables-y-de-bruijn`: "la solución seria es representar variables ligadas por índices (de Bruijn), que cambia `ref : Name -> Term` por `var : N -> Term` para las ligadas. Lo dejaría…"

### L-three-reduction-rules (language)

A reduction step has three rules: beta (substitute a lambda), delta (unfold a definition), iota (run the recursor); the order of the clauses is the evaluation strategy, another order giving another trace for the same result.

first 2026-09-29 05:06 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:06 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 28] `dialogue:890a551c:tres-reglas-de-reduccion`: "Tres reglas, y nada más ... El orden de las cláusulas es la estrategia de evaluación: buscar primero en `f` y después en `a` es reducción por nombre (perezosa)…"

### L-data-sum-of-products (language)

A data is a sum of products plus recursion (sum between constructors, product inside each, recursion as the least fixpoint); + and × are the degenerate cases, so data is primitive and they are not.

first 2026-09-29 05:07 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:07 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 30] `dialogue:175c0408:data-suma-de-productos-mas-recursion`: "Un `data` es una suma de productos, más recursión. ... Por eso `data` es primitivo y `+` y `×` no: son los dos casos degenerados."
- 2026-09-29 05:07 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 30] `dialogue:890a551c:data-es-suma-de-productos-con-recursion`: "Un `data` es una suma de productos, más recursión ... es el menor tipo que satisface esa ecuación, un punto fijo ... Por eso `data` es primitivo y `+` y `×` no…"

### L-indexed-families (language)

A further layer of data has constructors whose return type carries an index (Vec:N→U), a sum between constructors of a same family, which lets Traza t u have constructors only for pairs that reduce one to the other.

first 2026-09-29 05:07 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:07 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 30] `dialogue:890a551c:data-con-indices`: "constructores cuyo tipo de retorno lleva un índice, como `Vec : N -> U` ... Es lo que permite que `Traza t u` tenga constructores solo para pares `t`, `u` que…"

### L-term-needs-data-constructor (language)

Term needs a further constructor: the representation of the data{...} form itself as a term, so that N:U := data{...} is representable.

first 2026-09-29 05:10 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:10 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 32] `dialogue:890a551c:octavo-constructor-de-term`: "Falta un octavo que omití y hace falta: la representación del propio `data { ... }` como término, para que `N : U := data {...}` sea representable."

### L-invariants-forall (language)

Define invariants: f:A→B and for all x:A, g x (f x), where g:A→B→bool.

first 2026-09-29 05:16 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:16 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 33] `dialogue:175c0408:definir-invariantes-con-forall`: "esto es f : A -> B y para todo x: A g (x (f x) ) donde g : A->B-> bool"
- 2026-09-29 05:16 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 33] `dialogue:890a551c:definir-invariantes`: "ahora yo quiero poder definir invariantes. esto es f : A -> B y para todo x: A g (x (f x) ) donde g : A->B-> bool"

### L-bool-to-proposition-cierto (language)

"For all x:A" is the Π; to lift g's Bool to a proposition use a data Cierto:Bool→U that is ⊤ when true and ⊥ when false, so evidence for a concrete x is unit and types exactly when the boolean reduces to true (or write the property directly as a type G:A→B→U).

first 2026-09-29 05:17 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:17 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 34] `dialogue:175c0408:invariante-como-tipo-via-cierto`: ""Para todo `x : A`" es `(x : A) ->`, el `Π`; no hace falta símbolo nuevo. ... `Cierto : Bool -> U := \ b { match b { true -> ⊤ ; false -> ⊥ } }` ... Para un `x…"
- 2026-09-29 05:17 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 34] `dialogue:890a551c:bool-a-proposicion`: "\"Para todo `x : A`\" es `(x : A) ->`, el `Π`; no hace falta símbolo nuevo. Lo único que hay que resolver es que `g` devuelve `Bool` y un invariante tiene que…"

### L-invariant-tied-to-function (language)

An invariant can be tied to f two ways: as a separate definition f_inv (a hole until proven, the declaration being the test and filling it the proof) or as a package F:=(h:A→B)×(...) where the guarantee travels with the function.

first 2026-09-29 05:17 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:17 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 34] `dialogue:175c0408:invariante-separado-o-paquete`: "la declaración de `f_inv` es el test, y llenarla es la prueba. ... Como paquete, que es la "función definida operativamente y por sus propiedades" del audio de…"
- 2026-09-29 05:17 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 34] `dialogue:890a551c:invariante-como-definicion-separada-o-paquete`: "Como definición separada ... Mientras `f_inv` no tiene cuerpo es un hueco: la propiedad está declarada, no probada ... Esto es \"definir la función define el t…"

### L-verification-levels (language)

The verification levels are the same declaration with different degrees of body: running the test on a sample is empirical, filling the cases for all x is formal, and in between goes the statistical extension (a sample with its size as evidence of a ≈ type).

first 2026-09-29 05:17 by model; 3 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:17 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 34] `dialogue:175c0408:tres-grados-de-verificacion`: "Correr `test_f` sobre una muestra de `x` es verificación empírica ... Llenar `casos` para todo `x` es verificación formal. Y en el medio va tu extensión estadí…"
- 2026-09-29 05:17 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 34] `dialogue:890a551c:tres-niveles-de-verificacion`: "Los tres son la misma declaración con distinto grado de cuerpo ... en el medio va tu extensión estadística: una muestra de instancias que pasaron, con su tamañ…"
- 2026-09-29 06:07 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 66] `dialogue:175c0408:gradiente-de-tres-puntos-probado-testeado-hueco`: "la verificación gradual tiene un orden de dos puntos, preciso o hueco; el de tres, probado, testeado con `n` casos, hueco, no está formulado ni tiene sus garan…"

### L-data-gives-dependent-recursor (language)

Proving a law in general by induction requires the result type to depend on the inducted value, which is the dependent recursor; the simple recursor cannot write it, so it is decided that data gives the dependent recursor.

first 2026-09-29 05:21 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:21 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:175c0408:data-da-el-recursor-dependiente`: "Eso es el recursor *dependiente*, la inducción. Con el recursor simple del borrador no se puede escribir. Queda decidido: `data` da el dependiente."
- 2026-09-29 05:21 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:890a551c:recursor-dependiente-es-la-induccion`: "Eso es el recursor *dependiente*, la inducción. Con el recursor simple del borrador no se puede escribir. Queda decidido: `data` da el dependiente."

### L-laws-as-holes-falsifiable (language)

Laws are declarations like any other, holes until proven and falsifiable by an instance that does not type, and a conditioned law can go either as a hypothesis in the type (total function, partial guarantee) or as a restriction in the function (partial function, total guarantee).

first 2026-09-29 05:21 by model; 3 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:21 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:175c0408:leyes-son-declaraciones-falsables`: "las leyes son declaraciones como cualquier otra, huecos hasta que se prueban, y falsables por una instancia que no tipa. ... en `sub` con `ley2` condicionada,…"
- 2026-09-29 05:21 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:890a551c:funcion-total-garantia-parcial-o-al-reves`: "en `sub` con `ley2` condicionada, la función es total y la garantía es parcial; en `sub'`, la función es parcial y la garantía total. Las dos son legítimas, y…"
- 2026-09-29 05:21 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 36] `dialogue:890a551c:leyes-son-declaraciones-huecas-falsables`: "las leyes son declaraciones como cualquier otra, huecos hasta que se prueban, y falsables por una instancia que no tipa."

### L-definition-form-depends-on-type (language)

Clauses written against a header mean the form of a definition can depend on reducing its type, accepted as the same ≡ at work.

first 2026-09-29 05:22 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:22 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 38] `dialogue:175c0408:forma-depende-de-reducir-el-tipo`: "significa que la forma de una definición puede depender de reducir su tipo. A mano hay que hacer ese despliegue antes de leer los casos. Yo lo aceptaría; es el…"
- 2026-09-29 05:22 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 38] `dialogue:890a551c:la-forma-de-una-definicion-puede-depender-de-reducir-su-tipo`: "significa que la forma de una definición puede depender de reducir su tipo. A mano hay que hacer ese despliegue antes de leer los casos. Yo lo aceptaría; es el…"

### L-numeric-tests-not-logic (method)

Reject the propositional-logic proof layer; the aim of this version is to generate numeric tests.

first 2026-09-29 05:22 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:22 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 39] `dialogue:175c0408:no-logica-sino-tests-numericos`: "no quiero hacer logica proposicional quiero generar tests numericos"
- 2026-09-29 05:22 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 39] `dialogue:890a551c:no-logica-proposicional-sino-tests-numericos`: "no quiero hacer logica proposicional quiero generar tests numericos"

### L-redundancy-crosses-coloneq (language)

There are two kinds of redundancy: the one crossing the := (type says one thing, body another, verifier checks they match) is what gives something to verify; the one repeated on the same side is removable with sugar.

first 2026-09-29 05:22 by model; 3 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:22 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 38] `dialogue:175c0408:dos-clases-de-redundancia`: "La redundancia que vale es la que cruza el `:=`: el tipo dice una cosa, el cuerpo dice otra, y el verificador comprueba que coincidan. Si sacás esa, no queda n…"
- 2026-09-29 05:22 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 38] `dialogue:890a551c:redundancia-que-vale-cruza-el-asignador`: "La redundancia que vale es la que cruza el `:=`: el tipo dice una cosa, el cuerpo dice otra, y el verificador comprueba que coincidan. Si sacás esa, no queda n…"
- 2026-09-29 08:58 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 87] `dialogue:890a551c:no-escribir-el-resultado-a-mano`: "Si el resultado sale del cómputo, no se escribe; si querés declarar un valor esperado es otra cosa, un test `f x == 5`, y ahí el `5` no es el resultado sino lo…"

### L-sugar-criterion-term (language)

Criterion for any future sugar: if it forces adding a constructor to Term it is not sugar and must be discussed as a primitive.

first 2026-09-29 05:22 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:22 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 38] `dialogue:175c0408:criterio-de-azucar`: "si obliga a agregar un constructor a `Term`, no es azúcar y hay que discutirla como primitiva."
- 2026-09-29 05:22 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 38] `dialogue:890a551c:criterio-de-azucar-no-agrega-constructor-a-term`: "Ese es el criterio que propondría para cualquier azúcar futura: si obliga a agregar un constructor a `Term`, no es azúcar y hay que discutirla como primitiva."

### L-invariant-is-bool-function-v0 (language)

For numeric tests the proof layer (=, refl, induction) need not exist in version 0: an invariant is just a function returning Bool, with an input generator (a hole the environment fills by type) and a run storing the result, and the function's laws are a list of Bool functions, a field of Def.

first 2026-09-29 05:23 by model; 3 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:23 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 40] `dialogue:175c0408:invariante-es-funcion-a-bool`: "Un invariante es una función que devuelve `Bool`. Nada más."
- 2026-09-29 05:23 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 40] `dialogue:890a551c:definir-la-funcion-define-su-test`: "`sub.leyes` es una lista de funciones a `Bool` atada a un nombre: eso es \"definir la función define su test\", y es un campo más en `Def`, al lado del cuerpo…"
- 2026-09-29 05:23 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 40] `dialogue:890a551c:invariante-es-funcion-a-bool-testeada-por-muestra`: "Un invariante es una función que devuelve `Bool`. Nada más."

### L-laws-few-lines-requires (language)

Express a function's laws in few lines borrowing the C++ requires form: a block with quantified variables in the header and one Bool expression per line, where unlike C++ a line can be a type requirement (checked by the verifier without running) or a value requirement (run by the test).

first 2026-09-29 05:23 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:23 Luciano states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 41] `dialogue:890a551c:inspirarse-en-requires-de-cpp`: "para mi tendrian que pocas lineas \ninspirate en como se expresan los conceptos en C++ con requires"
- 2026-09-29 05:24 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 42] `dialogue:175c0408:azucar-requires-de-cpp`: "Acá una línea puede ser de las dos clases: `s (add x y) y : N` es un requisito de tipo y lo chequea el verificador sin correr nada; `s (add x y) y == x` es un…"
- 2026-09-29 05:24 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 42] `dialogue:890a551c:una-linea-de-requisito-puede-ser-de-tipo-o-de-valor`: "Acá una línea puede ser de las dos clases: `s (add x y) y : N` es un requisito de tipo y lo chequea el verificador sin correr nada; `s (add x y) y == x` es un…"

### L-concept-as-predicate (language)

A named concept is a predicate over functions written as a list of requirements, applicable to any implementation, so two implementations of the same concept are interchangeable.

first 2026-09-29 05:24 by model; 8 rows, 8 witnesses, 1 days, last 2026-09-29; taken up by Luciano 2026-09-29

- 2026-09-29 05:24 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 42] `dialogue:175c0408:concept-como-predicado-sobre-funciones`: "`Resta` es un predicado sobre funciones, escrito como lista de requisitos."
- 2026-09-29 05:24 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 42] `dialogue:890a551c:concept-como-predicado-sobre-funciones-con-nombre`: "`Resta` es un predicado sobre funciones, escrito como lista de requisitos."
- 2026-09-29 05:40 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 49] `dialogue:175c0408:concept-no-nuevo-tipo-sino-funcion`: "no me gusta introducir un tipo nuevo, concept... mas que nada porque yo creo en la construccion recursiva a partir de funciones... concept puede ser una funcio…"
- 2026-09-29 05:40 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 49] `dialogue:890a551c:concept-puede-ser-una-funcion`: "no me gusta introducir un tipo nuevo, concept... mas que nada porque yo creo en la construccion recursiva a partir de funciones... concept puede ser una funcio…"
- 2026-09-29 05:40 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 50] `dialogue:175c0408:concepto-es-funcion-que-devuelve-leyes`: "Un concepto es una función que devuelve un tipo (o, en la versión de tests, una función que devuelve leyes). No hay primitiva nueva"
- 2026-09-29 05:40 model confirms [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 50] `dialogue:890a551c:concepto-como-funcion-que-devuelve-leyes-o-tipo`: "Un concepto es una función que devuelve un tipo (o, en la versión de tests, una función que devuelve leyes). No hay primitiva nueva"
- 2026-09-29 07:28 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 73] `dialogue:890a551c:luthier-es-concepts-llevados-a-todo-el-lenguaje`: "concept es en realidad el que mas se aproxima a lo que quierdo decir fundamentalmente porque son predicados como los concepts, creo que seria basicamente ese c…"
- 2026-09-29 07:28 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 74] `dialogue:890a551c:cuatro-extensiones-sobre-concepts-de-cpp`: "Luthier es concepts llevados a todo el lenguaje, con requisitos semánticos que se ejecutan y cuyo resultado se guarda."

### L-type-restriction-refinement (language)

Does type restriction exist, e.g. N restricted to N<7?

first 2026-09-29 05:26 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:26 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 43] `dialogue:175c0408:restriccion-de-tipos-como-subconjunto`: "existe la restriccion de tipos no? N restringido a N<7 por ejemplo"
- 2026-09-29 05:26 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 43] `dialogue:890a551c:restriccion-de-tipos-como-subconjunto`: "existe la restriccion de tipos no? N restringido a N<7 por ejemplo"
- 2026-09-29 05:30 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 45] `dialogue:890a551c:tipos-de-rango-en-programacion`: "hay formas de decir que por ejemplo el tipo dia es un entero >0 <= 31"

### L-subtype-cast-asymmetry (language)

Going to the supertype is free (fst, forgetting the guarantee); going from a type to its subset requires checking the predicate, a cast with content that verifies or fails.

first 2026-09-29 05:26 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:26 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 44] `dialogue:175c0408:olvido-gratis-construccion-cuesta`: "Pasar de `{ n : N | n < 7 }` a `N` es gratis, es `fst`, el olvido de la garantía."

### L-subtype-is-sigma-pair (language)

A subtype is the dependent pair (Sigma) of a value with the evidence or certificate that it satisfies the predicate, and the set-builder notation denotes this Sigma, already in the core.

first 2026-09-29 05:26 by model; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:26 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 44] `dialogue:175c0408:tipo-subconjunto-es-par-con-evidencia`: "Es un tipo de subconjunto, y en el núcleo ya está: es el par de un valor con la evidencia de que cumple el predicado."
- 2026-09-29 05:26 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 44] `dialogue:890a551c:subtipo-como-par-valor-evidencia`: "Es un tipo de subconjunto, y en el núcleo ya está: es el par de un valor con la evidencia de que cumple el predicado."
- 2026-09-29 07:39 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 76] `dialogue:890a551c:subtype-como-unica-definicion-del-patron`: "Un subtipo es un tipo y un predicado sobre él."
- 2026-09-29 20:37 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 121] `dialogue:890a551c:subtipo-es-un-sigma`: "lo que denota en Luthier es un `Σ`, el par dependiente, que es una de las dos construcciones fundamentales de la teoría de tipos y de HoTT."

### L-no-value-without-check (language)

There is no way to have a value of a refined type without the predicate having been evaluated or proved; the type is written as a refinement and checked at construction, placing Luthier between Ada-style range types and dependent types.

first 2026-09-29 05:30 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:30 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 46] `dialogue:175c0408:luthier-entre-ada-y-dependientes`: "Lo que no hay es forma de tener un `Dia` sin que el predicado haya sido evaluado o probado"
- 2026-09-29 05:30 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 46] `dialogue:890a551c:luthier-entre-ada-y-tipos-dependientes`: "Lo que no hay es forma de tener un `Dia` sin que el predicado haya sido evaluado o probado, que es lo que Ada garantiza y lo que la clase con constructor valid…"

### L-group-of-functions-with-laws (language)

Functions are defined by postconditions, and the unit of definition is the group of functions with the laws relating them (a single function being the group of size one); this group-with-laws as a type is the normal form of defining anything.

first 2026-09-29 05:35 by Luciano; 5 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:35 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 47] `dialogue:175c0408:novedad-tipos-de-funcion-con-postcondiciones`: "definimos tipos de funciones no solo con el tipo de argumentos y resultados sino tambien con postcondiciones. Las postcondiciones son predicados de los argumen…"
- 2026-09-29 05:35 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 47] `dialogue:890a551c:novedad-tipos-de-funciones-con-postcondiciones-en-grupos`: "el concepto fundamental de Luthier, lo que es novedad, es que definimos tipos de funciones no solo con el tipo de argumentos y resultados sino tambien con post…"
- 2026-09-29 05:36 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 48] `dialogue:175c0408:que-junta-luthier-que-ninguno-tiene-junto`: "Cada pieza existe en algún lado; la novedad es que sea la forma normal de definir algo, no una herramienta aparte."
- 2026-09-29 05:36 model corrects [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 48] `dialogue:175c0408:unidad-es-el-grupo-con-sus-leyes`: "la unidad no es la función con postcondición, es el grupo de funciones con las leyes que las relacionan. La postcondición de una sola función es el caso partic…"
- 2026-09-29 05:36 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 48] `dialogue:890a551c:la-unidad-es-el-grupo-de-funciones-con-sus-leyes`: "la unidad no es la función con postcondición, es el grupo de funciones con las leyes que las relacionan. La postcondición de una sola función es el caso partic…"

### L-law-structure (language)

A law is a type of arguments plus a predicate over them that takes the function under test as argument and returns the two sides rather than a bare Bool, so the counterexample explains itself; its failure is a reified application.

first 2026-09-29 05:40 by model; 3 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:40 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 50] `dialogue:890a551c:ley-lleva-su-propio-tipo-de-entradas`: "una ley es un tipo de argumentos junto con un predicado sobre ellos"
- 2026-09-29 08:46 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 81] `dialogue:890a551c:ley-devuelve-los-dos-lados-en-vez-de-bool`: "lo que querés ver es `sub (add 4 3) 3 : 5` contra el `4` esperado. Eso se logra si la ley devuelve los dos lados en vez de compararlos ella misma"
- 2026-09-29 08:46 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 81] `dialogue:890a551c:leyes-que-toman-la-funcion-como-argumento`: "Como las escribiste, `InversaAditiva` menciona `sub` libre, así que solo sirve para esa resta. Para que `Resta` sea un tipo del que cualquier implementación pu…"

### L-laws-force-decisions (language)

Writing out the laws forces deciding under-specified behaviour (such as what read returns for an absent key), which is exactly what the laws are for.

first 2026-09-29 05:42 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:42 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 52] `dialogue:175c0408:leer-clave-ausente-obliga-a-decidir`: "`leer` para una clave que no está no tiene qué devolver... La ley te obliga a decidirlo, que es exactamente para lo que está."
- 2026-09-29 05:42 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 52] `dialogue:890a551c:almacen-con-ley-de-no-interferencia`: "La segunda, que escribir en `k` no toca lo que había en otra clave; sin ella, un `write` que borra todo lo demás pasaría la primera."

### L-construction-pattern (language)

The fundamental concept of Luthier is the construction pattern: the primitive is a predicate P over a material T, from which the certified type, the constructor (the only way to make a value, which must pass the check), and the forget (material = fst) derive mechanically.

first 2026-09-29 05:52 by Luciano; 8 rows, 8 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:52 Luciano proposes [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 53] `dialogue:175c0408:almacen-funcion-devuelve-maybe-almacen`: "Para mi es una funcion que toma un write y un read y te devuelve Maybe Almacen y Almacen te entrega las versiones verificadas de write y read"
- 2026-09-29 05:52 Luciano proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 53] `dialogue:890a551c:almacen-como-funcion-que-devuelve-maybe-verificado`: "Para mi es una funcion que toma un write y un read y te devuelve Maybe Almacen \ny Almacen te entrega las versiones verificadas de write y read"
- 2026-09-29 05:56 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 55] `dialogue:175c0408:unica-manera-de-fabricar-es-pasar-la-comprobacion`: "la única manera de fabricar un `Almacen` es pasar por la comprobación."
- 2026-09-29 05:56 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 55] `dialogue:890a551c:unica-forma-de-fabricar-pasa-por-la-comprobacion`: "la única manera de fabricar un `Almacen` es pasar por la comprobación"
- 2026-09-29 06:00 Luciano states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 58] `dialogue:175c0408:patron-de-construccion-concepto-fundamental`: "este tipo Almacen que en realidad confunde dos cosas el constructor de almacen y el almacen es el concepto fundamental de Luthier (no almacen sino el patron de…"
- 2026-09-29 06:00 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 58] `dialogue:890a551c:el-patron-de-construccion-es-el-concepto-fundamental`: "este tipo Almacen que en realidad confunde dos cosas el constructor de almacen y el almacen es el concepto fundamental de Luthier (no almacen sino el patron de…"
- 2026-09-29 06:01 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 59] `dialogue:175c0408:predicado-primitivo-tipo-y-constructor-derivados`: "lo primitivo es el predicado, y el tipo y el constructor se derivan de él mecánicamente. No son dos cosas que se confunden bajo un nombre; son dos usos de una…"
- 2026-09-29 06:01 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 59] `dialogue:890a551c:lo-primitivo-es-el-predicado-tipo-y-constructor-se-derivan`: "lo primitivo es el predicado, y el tipo y el constructor se derivan de él mecánicamente. No son dos cosas que se confunden bajo un nombre; son dos usos de una…"

### L-check-value-vs-function (language)

Checking a value is a computation decided by evaluating it; checking a function is an experiment that must be sampled; Luthier treats both as the same construct operation, one exact and one statistical.

first 2026-09-29 05:56 by model; 3 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 05:56 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 55] `dialogue:175c0408:comprobar-valor-computo-comprobar-funcion-experimento`: "La comprobación de un valor es un cómputo; la de una función es un experimento. Luthier tiene que tratar a los dos como la misma operación de construir, sabien…"
- 2026-09-29 05:56 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 55] `dialogue:890a551c:construir-valor-es-computo-construir-funcion-es-experimento`: "La comprobación de un valor es un cómputo; la de una función es un experimento. Luthier tiene que tratar a los dos como la misma operación de construir, sabien…"
- 2026-09-29 07:39 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 76] `dialogue:890a551c:predicado-devuelve-veredicto-no-bool`: "Yo iría por la primera: `P : T -> Veredicto`, con `Bool` como el caso exacto, porque mantiene una sola noción de subtipo y pone la diferencia donde está, en el…"

### L-certificate-composable (language)

The certificate is a first-class value carrying its guarantee level, composable and forgettable: it is a clause with hypotheses, a program's certificate is the closure of such clauses, and composed material is the chained forgetting.

first 2026-09-29 06:01 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 06:01 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 59] `dialogue:175c0408:certificado-se-acumula-por-composicion`: "El certificado se acumula por composición, y `material` compuesto es el olvido en cadena."
- 2026-09-29 06:07 model refines [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 66] `dialogue:175c0408:certificado-como-clausula-con-hipotesis`: "El certificado como cláusula con hipótesis, no como hecho... cada verificación produce `H1 ∧ ... ∧ Hn → L`, y el certificado de un programa es el cierre de esa…"

### L-pattern-prior-art (language)

The pieces exist separately (Eiffel contracts, QuickCheck, dependent types, proof-carrying code); the novelty is one pattern for values, functions and whole programs, with the certificate as a first-class composable forgettable value and runs persisted as program data.

first 2026-09-29 06:04 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 06:04 Luciano questions [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 63] `dialogue:175c0408:es-una-libreria-certificada-reedita-eiffel`: "es como una libreria certificada no? Existe algo asi ya? es un poco re-editar lo de Eiffel no? con sus postconditions"
- 2026-09-29 06:04 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 63] `dialogue:890a551c:libreria-certificada-reedicion-parcial-de-eiffel`: "es como una libreria certificada no? \nExiste algo asi ya?\nes un poco re-editar lo de Eiffel no? con sus postconditions"
- 2026-09-29 06:05 model states [2026-09-28_175c0408_quiero-empezar-a-definir-la-semantica-de.md turn 64] `dialogue:175c0408:lo-que-no-existe-junto`: "un mismo patrón para valores, funciones y programas enteros; el certificado como valor de primera clase con su nivel de garantía, componible y olvidable; y las…"
- 2026-09-29 06:13 model restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 64] `dialogue:890a551c:que-tiene-antepasados-pero-no-junto`: "un mismo patrón para valores, funciones y programas enteros; el certificado como valor de primera clase con su nivel de garantía, componible y olvidable; y las…"

### L-name-the-pattern (language)

The verification structure is the core of Luthier and needs its own name, not 'Luthier' (that is the language); settle on 'Library' for the instance (a program that passed its tests), with 'Object' rejected.

first 2026-09-29 06:15 by Luciano; 5 rows, 5 witnesses, 1 days, last 2026-09-29

- 2026-09-29 06:15 Luciano proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 65] `dialogue:890a551c:nombre-propio-para-la-estructura-de-verificacion`: "quizas podriamos llamar a esta estructura de verificacion luthier o un nombre ad-hoc no? Porque yo creo que es el nucleo de Luthier y lo que lo haria util e im…"
- 2026-09-29 06:15 model proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 66] `dialogue:890a551c:no-llamar-luthier-a-la-estructura`: "Luthier es el lenguaje; esto es la estructura que el lenguaje construye, y si las dos cosas se llaman igual vas a tener el mismo problema que con `Almacen`"
- 2026-09-29 06:19 Luciano states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 67] `dialogue:890a551c:library-como-nombre-de-la-instancia`: "tested library seria. \nquizas el nombre sea library nomas"
- 2026-09-29 06:20 model confirms [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 68] `dialogue:890a551c:library-tested-sobra-si-no-hay-otra-forma`: "una library es un programa que pasó sus tests y lo puede mostrar."
- 2026-09-29 06:20 model rejects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 70] `dialogue:890a551c:rechazo-de-object-como-nombre`: "\"Object\" no, y por una razón concreta... Quien lo lea va a pensar en instancia de clase con estado y métodos, que es justo la imagen que Luthier no tiene, po…"

### L-parametrizable-requirements (language)

No language has distribution units that come with a set of requirements they must satisfy; in the pattern this is direct because the predicate is a function taking parameters (max error, scalability), so the certificate states which parameters are met and dependent libraries inherit them.

first 2026-09-29 06:23 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 06:23 Luciano states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 71] `dialogue:890a551c:libraries-con-requisitos-parametrizables`: "lo que no veo que haya es que vengan con un conjunto de requisitos que deban cumplir, requisitos que pueden ser parameterizables ( por ejemplo error maximo, es…"
- 2026-09-29 06:24 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 72] `dialogue:890a551c:predicado-con-parametros-y-certificado-gradado`: "nadie hace que la unidad de distribución sea un tipo cuyo predicado tiene parámetros. En el patrón eso es directo, porque el predicado es una función y las fun…"

### L-predicate-returns-result (language)

A predicate is a function T -> Resultado (Fallo T) returning the counterexample with its cause rather than a bare Bool, with failure modes as a typed inductive type; a subtype is not the predicate but the type of values for which the predicate gives ok.

first 2026-09-29 08:28 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 08:28 Luciano states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 77] `dialogue:890a551c:simbolos-en-vez-de-palabras-para-subtipos`: "serian Predicates que devuelven un mensaje de error (la condicion en la que fallan) y si esa condicion en la que fallan es tipada, el retorno del Predicate ser…"
- 2026-09-29 08:29 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 78] `dialogue:890a551c:predicado-que-devuelve-el-error-tipado`: "Los subtipos no son predicados; son tipos. Esta es la corrección. Un predicado es una función `T -> Resultado E`; un subtipo es el tipo de los valores de `T` p…"
- 2026-09-29 09:28 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 100] `dialogue:890a551c:tipo-del-predicate`: "ahora tenemos que pensar como concatenamos predicates. el tipo del predicate de A seria A -> Maybe (A-> bool) x A x bool ?"
- 2026-09-29 09:29 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 101] `dialogue:890a551c:predicate-con-result-y-failure`: "`Predicate (A : U) : U := A -> Resultado (Fallo A)` `Fallo (A : U) : U := (ley : A -> Bool) * (arg : A)`"

### L-ev-graph-object (language)

The object storing (function, argument, result) is the graph of the evaluation, Ev f := (x:A) x (y:B) x (f x = y), with sugar to evaluate and store the triple (which the context cannot infer, so it must be marked), and the runs database is a list of these.

first 2026-09-29 08:45 by Luciano; 8 rows, 7 witnesses, 1 days, last 2026-09-29

- 2026-09-29 08:45 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 80] `dialogue:890a551c:aplicacion-reificada-nombre-de-la-tupla-funcion-args-resultado`: "(usamos el nombre de la funcion como comentario y usamos el objeto function evalaution (como se llama cuando guardas la tuple funcion args result?)"
- 2026-09-29 08:47 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 83] `dialogue:890a551c:grafo-de-eval-y-traza-como-nombres-categoriales`: "el par `(argumentos, obtenido)` es un elemento del grafo de `ev`... y si querés conservar *cómo* se llegó a `obtenido`, es la traza. Para el mensaje de error a…"
- 2026-09-29 08:52 Luciano proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 84] `dialogue:890a551c:azucar-para-guardar-la-aplicacion-evaluada`: "quizas podriamos definir un sugar para \nB^A × A × B\no para \n(f : A -> B) × (x : A) × (y : B) × (f x = y)\ndonde indicas que guardas todo"
- 2026-09-29 08:53 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 85] `dialogue:890a551c:azucar-ev-sobre-la-aplicacion`: "Un término de `Ev f` es un `x` con su `f x` calculado y la garantía de que es ese."
- 2026-09-29 08:58 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 86] `dialogue:890a551c:sintaxis-de-la-azucar-ev-abierta`: "podria ser [f x (f x)] o uso |<f x >| ? o dejo que el contexto decida? \npodria ser tambien ! [ f x ] como indicando que solo se guarda cuando es falso..."
- 2026-09-29 08:58 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 87] `dialogue:890a551c:el-contexto-no-elige-el-tipo-de-evaluacion`: "El contexto no puede decidir: `f x : B` y `[f x] : Ev f` son tipos distintos ... o el verificador insertaría conversiones implícitas y perderías la lectura a m…"
- 2026-09-29 08:58 model rejects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 87] `dialogue:890a551c:guardar-solo-fallos-es-del-test-no-del-operador`: "«Solo cuando es falso» no es una propiedad de la evaluación sino de qué hace el test con ella ... Es más simple que `⟨f x⟩` siempre guarde, y que quien quiera…"
- 2026-09-29 09:19 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 97] `dialogue:890a551c:evalstore-contiene-a-quote`: "**Evalstore**, la evaluación guardada, es el par sintaxis más valor ... si tenés quote y aplicación, evalstore es un par y no una tercera operación."

### L-symbol-vs-word (language)

Choose symbol over keyword only for what appears many times per line with a fixed universal meaning that already exists outside with that meaning, and a word for what is rare, carries content, or is structural, because Luthier is read aloud and written by hand.

first 2026-09-29 08:58 by model; 4 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 08:58 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 87] `dialogue:890a551c:criterio-de-un-simbolo-nuevo`: "cada símbolo nuevo tiene que reemplazar una construcción que de otro modo aparecería en cada programa."
- 2026-09-29 09:12 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 88] `dialogue:890a551c:palabras-clave-vs-simbolos`: "ahora tambien podria ser que palabras clave sean mejor que simbolos ... supongo que simbolos vs palabras clave ha sido discutido y que podemos aprender de esa…"
- 2026-09-29 09:12 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 89] `dialogue:890a551c:cada-simbolo-debe-tener-lectura`: "Cada símbolo debería tener su lectura fijada en el documento ... Si un símbolo no tiene lectura natural, es señal de que debería ser palabra."
- 2026-09-29 09:12 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 89] `dialogue:890a551c:criterio-simbolo-vs-palabra`: "símbolo para lo que aparece muchas veces por línea y tiene un significado fijo y universal; palabra para lo que aparece pocas veces ... **símbolo si ya existe…"

### L-ascii-canonical (language)

The canonical form of the language is ASCII; an editor may display -> as the arrow and * as the cross without changing the file, as Lean does.

first 2026-09-29 09:15 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:15 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 90] `dialogue:890a551c:para-todo-no-es-ascii`: "pero para todo no es ascii"
- 2026-09-29 09:15 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 91] `dialogue:890a551c:forma-canonica-ascii`: "la forma canónica del lenguaje es ASCII, y un editor puede mostrar `->` como `→` y `*` como `×` si quiere, como hace Lean, sin que el archivo cambie."

### L-lambda-is-forall (language)

A quantified law needs no for-all symbol: the lambda's typed parameters are the 'for all', and a law is a function to Bool whose parameters are the quantified variables.

first 2026-09-29 09:15 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:15 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 91] `dialogue:890a551c:ley-cuantificada-es-la-lambda`: "los `(x y : N)` de la lambda son el «para todo». Una ley es una función a `Bool` y sus parámetros son las variables cuantificadas ... No hay que escribir `∀` p…"

### L-plus-for-sum-types (language)

Use + for the sum of types, as mathematics and type theory do, since type-sum never collides with number-sum; an n-ary variant is sugar built by recursion from binary +.

first 2026-09-29 09:18 by model; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:18 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 93] `dialogue:890a551c:suma-de-tipos-con-mas`: "`+`. Es lo que usa la matemática para la unión disjunta y lo que usa la teoría de tipos en los papers ... suma de tipos y suma de números nunca aparecen en la…"
- 2026-09-29 09:18 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 95] `dialogue:890a551c:variant-como-azucar-del-mas-binario`: "en el núcleo se puede definir como una función de una lista de tipos a un tipo, `Variant : List U -> U`, por recursión sobre la lista ... Así queda derivada de…"

### L-predicate-concatenation (language)

Predicates concatenate two ways: conjunction P & Q where both must pass, and refinement P |> Q where Q is defined over the subtype A|P so the order is not optional.

first 2026-09-29 09:29 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:29 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 101] `dialogue:890a551c:conjuncion-y-refinamiento-de-predicados`: "**Refinamiento**, cuando `Q` está definido sobre el subtipo y no sobre `A` ... Acá el orden no es opcional: `Q` no se puede correr sin haber pasado `P`."

### L-match-is-recursor-sugar (language)

match is the only way to open a data value; it is not primitive but sugar of the recursor that data gives (if being match over Bool), with a mechanical translation that guarantees totality.

first 2026-09-29 09:32 by Luciano; 3 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:32 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 102] `dialogue:890a551c:como-se-define-match`: "como definimos match ? y para que sirve?"
- 2026-09-29 09:33 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 103] `dialogue:890a551c:if-no-es-primitivo`: "por qué `if` no es primitivo: es `match` sobre `Bool`, o sea `recBool`."
- 2026-09-29 09:33 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 103] `dialogue:890a551c:match-es-azucar-del-recursor`: "No es primitivo. Es azúcar del recursor que `data` te regala, y la traducción es mecánica."

### L-core-ten-lines-ebnf (language)

Luthier's core fits in about ten lines of EBNF with three reserved words (data, match, extern); everything else is base-library names or sugar, each sugar carrying its core translation.

first 2026-09-29 09:36 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:36 Luciano proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 104] `dialogue:890a551c:intento-de-bnf`: "intentamos un draft del BNF de Luthier?"
- 2026-09-29 09:37 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 105] `dialogue:890a551c:nucleo-en-diez-lineas`: "El núcleo entra en diez líneas de EBNF y tiene tres palabras reservadas: `data`, `match` y `extern`. Todo lo demás son nombres de la librería base o azúcar."

### L-subtype-assignment-runs-tests (language)

Assigning to a subtype (resta:Resta:=sub) forces the verifier to run the cases at compile time; the alternative is leaving it as a declared hole until an explicit test.

first 2026-09-29 09:37 by model; 1 rows, 1 witnesses, 1 days, last 2026-09-29

- 2026-09-29 09:37 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 105] `dialogue:890a551c:compilar-corre-los-tests`: "`resta : Resta := sub`. Como `Resta` es un subtipo, esa línea obliga al verificador a correr los mil casos al compilar ... La alternativa es que ... quede como…"

### L-subtype-notation-setbuilder (language)

Settle on set-builder notation { pattern : material | predicate } as the single subtype form, dropping 'where' and the overloaded |, with the structure's named components and their types to the left of | and the laws to the right, as a ring is written in algebra.

first 2026-09-29 20:15 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 20:15 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 106] `dialogue:890a551c:dudas-sobre-barra-para-predicados`: "estoy dudando si usar \"|\" para indicar cuando comienzan los Predicate. Quizas algo parecido a requires"
- 2026-09-29 20:15 model proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 107] `dialogue:890a551c:where-para-subtipo`: "`where` para el subtipo con predicado nombrado, y `{ x : T | p x }` se queda como está ... Para las cláusulas, que es donde `|` molesta de verdad, la alternati…"
- 2026-09-29 20:30 model proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 113] `dialogue:890a551c:notacion-de-conjuntos-como-forma-unica`: "saco `where`, dejo `{ patrón : material | predicado }` como única forma, y agrego el ejemplo del anillo"
- 2026-09-29 20:32 model proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 115] `dialogue:890a551c:ring-con-componentes-nombradas`: "Es la misma notación de conjuntos con el patrón desplegado en líneas: a la izquierda del `|` las componentes con su tipo, a la derecha las leyes sobre ellas."

### L-candidate-not-in-type (language)

The sample size n is certificate data, not part of the type; the candidate variable is the material (N->N->N), not the subtype itself (which would be circular), and quantifying over it with forall is superfluous.

first 2026-09-29 20:20 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 20:20 Luciano corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 108] `dialogue:890a551c:muestreado-no-va-en-el-tipo`: "esto no tiene sentido. Resta:= (N->N->N) where forall ( r: Resta , InversaAditiva(r) & InversaAcotada(r)) algo asi es mejor?"
- 2026-09-29 20:20 model confirms [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 109] `dialogue:890a551c:n-es-del-certificado-no-del-tipo`: "El `n` es un dato del certificado, no del tipo, que es exactamente lo que dijimos de dos valores del mismo tipo con garantías distintas."

### L-coupled-functions-product (language)

Laws that couple several functions (such as distributivity) mean the material is a product; the pattern (add, mul) unpacks it and names each component, so the laws are written over named components.

first 2026-09-29 20:27 by Luciano; 2 rows, 2 witnesses, 1 days, last 2026-09-29

- 2026-09-29 20:27 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 110] `dialogue:890a551c:que-es-r-y-funciones-acopladas`: "el tema aca es que que carajo es r? como lo se? ... pero si queres por ejemplo definir que cumple distributividad ahi tenes varias funciones acopladas"
- 2026-09-29 20:28 model proposes [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 111] `dialogue:890a551c:material-como-producto`: "Distributividad habla de dos operaciones a la vez, así que el candidato es el par ... El patrón `(add, mul)` desarma el par y nombra cada componente"

### L-setbuilder-prior-art (language)

Set-builder subtype notation exists in Coq, Lean, F*, Z and even Python's comprehensions, but mainstream languages omit it because deciding the predicate needs a solver, a proof or a runtime check; Luthier's fourth way tests with n cases recorded in the certificate, letting the predicate be any function to Bool.

first 2026-09-29 20:33 by Luciano; 4 rows, 4 witnesses, 1 days, last 2026-09-29

- 2026-09-29 20:33 Luciano questions [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 116] `dialogue:890a551c:por-que-no-esta-en-los-lenguajes`: "ahora siendo tan linda y conocida la notacion de conjuntos porque no se usa en ningun lenguaje? o si se usa?"
- 2026-09-29 20:34 model states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 117] `dialogue:890a551c:la-cuarta-salida-el-test`: "Es la cuarta salida: el predicado no se decide, se testea con `n` casos, y el resultado queda en el certificado. Eso es lo que permite que `p` sea cualquier fu…"
- 2026-09-29 20:35 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 118] `dialogue:890a551c:comprensiones-son-notacion-de-conjuntos`: "no me habia dado cuenta que las comprehensive lists de python son notaciones de conjuntos..."
- 2026-09-29 20:35 model refines [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 119] `dialogue:890a551c:comprension-de-valores-vs-de-tipos`: "Es la misma frase leída como «los que hay» o como «los que pueden haber»."

### L-setnotation-vindicated (language)

Though Luthier aimed to be a modern HoTT language it ends up using primary-school set-builder notation, which is fine: that notation denotes a Sigma and category theory itself generalizes rather than contradicts sets, with the subtype defined by the mono forget arrow.

first 2026-09-29 20:37 by Luciano; 3 rows, 3 witnesses, 1 days, last 2026-09-29

- 2026-09-29 20:37 Luciano states [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 120] `dialogue:890a551c:incomodidad-notacion-de-primaria`: "queria hacer un lenguaje hott , re moderno, y termino usando notacion de conjunts de la primaria.... Pero lo efectivo es efectivo."
- 2026-09-29 20:38 Luciano restates [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 122] `dialogue:890a551c:categorias-y-sets`: "categorias trata de lleva todo a sets, de modo que usar sets para todo no parece contradictorio."
- 2026-09-29 20:39 model corrects [2026-09-28_890a551c_quiero-empezar-a-definir-la-semantica-de.md turn 123] `dialogue:890a551c:semantica-de-flechas-no-de-elementos`: "La notación es de conjuntos; la semántica es de flechas. Y por eso el patrón se aplica igual a `N`, a `N -> N -> N` y a `Program`: la flecha `forget` existe en…"

## Unplaced rows

- describes a specific existing helper (Transfer_Op_to), not an idea about Luthier (1): `dialogue:01998d16:transfer-op-to-propagates-transformation`
- a debugging request about why a type was not registered, not an idea (1): `dialogue:01998d16:solve-registration-for-all-types-not-just-one`
- inspiration pointer, too vague to state an idea (1): `dialogue:20260628T2122:video-como-inspiracion-para-luthier`
- a request to clarify what "tipa" means, not an idea (1): `dialogue:890a551c:que-significa-tipa`
