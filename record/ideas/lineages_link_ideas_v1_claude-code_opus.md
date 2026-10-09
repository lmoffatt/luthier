# Lineages of the ideas about Luthier

Written by `scripts/link_ideas.py` (link_ideas v1) for Luciano and for the distillation. Prompt `link_ideas_v1`
(sha256 df7eb949f556), model opus at effort low via claude-code (2.1.197 (Claude Code)); 1 calls. Input: `record/ideas/timeline.jsonl`, last read with sha256
b76e36b54dbd. Who said an idea first and whether Luciano adopted a model's idea are computed from the rows' times and authors, not by the model.

Rows: 2101 in the timeline; placed 181, unplaced 0, pending 1920. Lineages: 83.

| scope | first said by Luciano | first said by model |
|---|---|---|
| language | 49 | 25 |
| other | 2 | 7 |

First said by a model and then taken up by Luciano: 0.

## Lineages, by first appearance

### L-code-is-data (language)

Code is data, erasing the distinction between code and data, following the Lisp model.

first 2022-06-15 08:55 by Luciano; 6 rows, 6 witnesses, 5 days, last 2023-03-13

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 13] `written:2022-06-15_sin-titulo-2:codigo-es-dato`: "La idea de que el codigo sea dato es muy, pero muy fuerte en cuanto a la flexibilidad que ofrece pero es notable que los lenguajes modernos no sigan ese camino…"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 25] `written:2022-06-28_luciano-code-style:erase-code-data-distinction`: "poder crear nuevos "objetos" (sean valores o variables, de tipos, funciones o "clases"). Al mismo tiempo perder la distincion entre codigo y dato."
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 65] `written:2022-08-03_haskell:codigo-como-dato`: "la idea del codigo como dato, es hacer que el codigo de una funcion sea como los parametros de un tipo, solo que en lugar de tener numeros o tipos, tiene opera…"
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 73] `written:2022-08-03_haskell:modelo-lisp`: "Yo creo que tengo que seguir el modelo Lisp."
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 17] `written:2023-02-22_tapp-wish-list:code-as-data`: "Code as data. Debo poder operar sobre las definiciones de funciones. O sea que debo distinguir entre el codigo y la aplicacion del codigo."
- 2023-03-13 14:48 Luciano restates [2023-03-13 hacia Luthier.md line 81] `written:2023-03-13_hacia-luthier:code-as-data`: "Code as data."

### L-identifiers-central (language)

Identifiers are central: a simple label recovers a complex object, the dictionary joining human and machine.

first 2022-06-15 08:55 by Luciano; 3 rows, 3 witnesses, 3 days, last 2023-03-13

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 9] `written:2022-06-15_sin-titulo-2:identificadores-importan`: "con quimulun quise explorar la idea de la importancia de los identificadores."
- 2022-07-05 07:53 Luciano restates [2022-07-05 Sin título 2.md line 11] `written:2022-07-05_sin-titulo-2:etiqueta-para-objeto-complejo`: "Toda la gracia de la computacion pasa por identificar elementos complejos por una simple etiqueta."
- 2023-03-13 14:48 Luciano restates [2023-03-13 hacia Luthier.md line 15] `written:2023-03-13_hacia-luthier:diccionario-humano-maquina-literalismo`: "la estructura mas importante de la programacion es el diccionario que une el humano con la maquina, es la base del literalismo"

### L-remaking-foundations (other)

He has re-made the language many times, each time rethinking the foundations of programming more deeply.

first 2022-06-15 08:55 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-15

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 3] `written:2022-06-15_sin-titulo-2:rehacer-desde-las-bases`: "estuve re-haciendo macror muchisimas veces cada vez volviendo a repensar mas las bases de la programacion."

### L-type-carries-its-laws (language)

A type (or function) carries, as a proposition, the law its values must satisfy.

first 2022-06-15 08:55 by Luciano; 6 rows, 6 witnesses, 3 days, last 2023-02-28

- 2022-06-15 08:55 Luciano states [2022-06-15 Sin título 2 .md line 11] `written:2022-06-15_sin-titulo-2:clases-implican-predicados`: "con tapp quise explorar la idea de que las clases implican predicados y que el codigo es dato."
- 2022-08-03 11:56 Luciano restates [2022-08-03 haskell.md line 23] `written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple`: "poder indicar en cada tipo (no distingo entre tipo y funcion) cual es la proposicion que cumple. Aqui hay dos versiones: una computacional y otra escrita. La i…"
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 29] `written:2022-08-03_tapp-before:identity-with-universal-law`: "Identity id \| for_all x:a {id x = x}"
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 37] `written:2022-08-03_tapp-before:io-type-with-roundtrip-laws`: "when (for_all x: a {x\| write \| read = (Just x,\"\")}) & (forall y: s {y\| read \| write = y})"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 19] `written:2023-02-28_sin-titulo-1-w:compose-con-ley-de-asociatividad`: "function Compose (Hom(X,Y), Hom(Y,Z))-\>Hom(X,Z)=\>Associative (Compose)"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 21] `written:2023-02-28_sin-titulo-1-w:id-con-leyes-de-identidad`: "function Id(X)-\>Hom(X,X) =\> Identity_right(Id(X),Hom(X,Y)) & Identity_left(Hom(Y,X),Id(X))"

### L-code-to-understand (other)

He codes to understand, which means being able to manipulate the code and see how changes affect its observables.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 3] `written:2022-06-28_luciano-code-style:code-to-understand`: "I code to understand."

### L-create-objects-uniformly (language)

The language expresses and creates values, variables, types and functions uniformly, with their semantics.

first 2022-06-28 22:25 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 107] `written:2022-06-28_luciano-code-style:how-to-define-values-types-variables-functions`: "Como creo valores (values) y sus tipos (types), variables (variables), y tipos de variables (¿?), funciones y tipos de funciones."
- 2022-06-28 22:25 Luciano restates [2022-06-28 Luciano Code style.md line 21] `written:2022-06-28_luciano-code-style:library-for-types-with-semantics`: "Expresar variables y tipos, y tipos funcionales, de clases etc y con sus semantica."

### L-dependent-types-def (language)

Dependent types are types that depend on a value, taking the cardinality of that value's type.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 115] `written:2022-06-28_luciano-code-style:dependent-types`: "dependent-types: son tipos que dependen de un valor, lo cual hace que su cardinalidad sea la del typo del valor que toma"

### L-express-extracomputational (language)

The language expresses extra-computational concepts like probability by abstracting their properties and verifying compliance (e.g. a probability lies in [0,1]).

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 15] `written:2022-06-28_luciano-code-style:express-extra-computational-concepts-with-verification`: "Expresa conceptos extra-computacionales (por ejemplo probabilidad) de forma intuitiva y veraz. La idea es abstraer las propiedades compulacionales de estos con…"

### L-expressiveness (language)

Code must express its intention to both the human reader and the compiler, referring truthfully to known structures.

first 2022-06-28 22:25 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 13] `written:2022-06-28_luciano-code-style:expressive-reference-to-known-structures`: "refiere a estructuras o algoritmos conocidos y esta referencia es real. Por ejemplo, no puedo llamar array a una lista."
- 2022-06-28 22:25 Luciano restates [2022-06-28 Luciano Code style.md line 9] `written:2022-06-28_luciano-code-style:expressiveness-as-observable`: "Expresividad: el codigo debe expresar la intención del mismo tanto para el que leer el codigo como para el compilador."

### L-foundation-choice (language)

Open question of which foundation to build on (type theory vs category theory, HoTT vs ZMT).

first 2022-06-28 22:25 by Luciano; 2 rows, 2 witnesses, 2 days, last 2023-03-02

- 2022-06-28 22:25 Luciano questions [2022-06-28 Luciano Code style.md line 59] `written:2022-06-28_luciano-code-style:type-theory-vs-category-theory`: "aqui tengo que pensar hasta que punto sigo con type theory y hasta que punto uso category theory."
- 2023-03-02 11:27 Luciano questions [2023-03-02 estoy perdido.md line 17] `written:2023-03-02_estoy-perdido:hott-o-zmt-como-base`: "empiezo con HoTT o con ZMT?"

### L-primitives (language)

A proposed set of primitive value types and primitive functions.

first 2022-06-28 22:25 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 111] `written:2022-06-28_luciano-code-style:primitive-functions`: "funciones primitivas: suma, resta, multiplicacion, division, division entera, modulo, concatenacion de strings...., and, or, not, greater than, equal.."
- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 109] `written:2022-06-28_luciano-code-style:primitive-value-types`: "tipos de valores primitivos: boolean, integer, real, string, nothing (or zero), one (or something), memory (¿?), size (¿?)"

### L-reasoning-to-code-isomorphism (language)

There should be a one-to-one relation between reasoning and the flow of the code, so running the code verifies the reasoning.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 31] `written:2022-06-28_luciano-code-style:one-to-one-reasoning-code-flow`: "abstraer y formalizar los mecanismos de determnacion sematinca de forma que haya una relacion uno a uno entre el razonamiento y el flujo del codigo. De esta fo…"

### L-sample-probability-duality (language)

Sample and probability form a duality, with tests demonstrating it holds.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 93] `written:2022-06-28_luciano-code-style:sample-probability-duality`: "muestra y probabilidad --\> dualidad y tests que demuestran que se cumple."

### L-semantic-then-efficient (language)

Once semantic validity and equivalence are established, a clear slow algorithm can be replaced by an efficient equivalent one, enabling optimization.

first 2022-06-28 22:25 by Luciano; 5 rows, 5 witnesses, 2 days, last 2023-02-22

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 33] `written:2022-06-28_luciano-code-style:choose-efficient-path-after-validity`: "una vez que se establece la validez semantica y la equivalencia semantica se puede optar por el camino mas eficiente."
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 95] `written:2022-06-28_luciano-code-style:equivalence-relation-multinomial`: "Relacion de equivalencia entre (state\*k)^N y Sum\_{\|a\|=k} C(n,a) \*state^a , a-\>multiindice"
- 2022-06-28 22:25 Luciano restates [2022-06-28 Luciano Code style.md line 27] `written:2022-06-28_luciano-code-style:equivalence-relations-for-optimization`: "Es importante establecer las relaciones de equivalencia en quimulun. Esto permite optimizar los tiempos de calculo."
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 17] `written:2022-06-28_luciano-code-style:slow-clear-algorithm-as-gold-standard`: "es posible que una algoritmo que es expresado de una forma clara pero computacionalmente no eficiente pueda ser optimizado con un algoritmo mas criptico. Esto…"
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 29] `written:2023-02-22_tapp-wish-list:optimizacion-automatica`: "Permitir la optimizacion automatica del codigo a medida que se mide el consumo de recursos de implementaciones alternativas de distintas funciones."

### L-semantics-own-universe (language)

The semantics lives in its own universe, not that of C++, even while using C++ structures to express it.

first 2022-06-28 22:25 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 23] `written:2022-06-28_luciano-code-style:semantics-live-in-own-universe`: "Esta semantica "vive" en su propio universo que no es el de C++, aunque use las estructuras de C++ para expresarlos."

### L-states-as-type-algebra (language)

States and channels and their multiplicities are represented with type algebra (sum for states, product for channels), with a constructor from a number to a set.

first 2022-06-28 22:25 by Luciano; 4 rows, 4 witnesses, 1 days, last 2022-06-28

- 2022-06-28 22:25 Luciano states [2022-06-28 Luciano Code style.md line 53] `written:2022-06-28_luciano-code-style:channel-state-isomorphic-to-one`: "un tipo channel state que es isomorfico con el tipo ONE"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 85] `written:2022-06-28_luciano-code-style:channels-multiplicity-as-product`: "multiplicidad de canales (pero como producto, no suma, exponencial a un numero)"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 49] `written:2022-06-28_luciano-code-style:state-multiplicity-as-sum`: "si quiero decir el estado i entre N estados "similares", el tipo del estado i seria estado x N, siendo N el tipo 1+1+1..+1 N veces. Es decir el set de N compon…"
- 2022-06-28 22:25 Luciano refines [2022-06-28 Luciano Code style.md line 57] `written:2022-06-28_luciano-code-style:type-constructor-from-natural`: "un constructor de tipos que toma un numero natural y te devuelve un conjunto que contiene ese numero natural."

### L-environment-first-object (language)

The environment is the first object the language must define, since data is loaded into it.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 5] `written:2022-07-05_sin-titulo-2:environment-es-el-primer-objeto`: "tengo que definir un environment donde cargar los datos, obvio."

### L-environment-kinds (language)

There are simple environments (one value type, one identifier) and compound ones that admit multiple.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 39] `written:2022-07-05_sin-titulo-2:environments-simples-y-compuestos`: "hay environments simples (solo admiten un tipo de valor y un unico identificador) y otros compuestos que admiten multiples."

### L-environment-resources (language)

The environment needs and manages resources (memory and compute) and function execution, a problem that ties to it but exceeds it (OS, compiler).

first 2022-07-05 07:53 by Luciano; 3 rows, 3 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 21] `written:2022-07-05_sin-titulo-2:dos-recursos-del-environment`: "El environment tiene dos recursos: 1\) memoria para guardar las variables. 2\) recursos computacionales para manejar la memoria y guardar o recuperar las varia…"
- 2022-07-05 07:53 Luciano refines [2022-07-05 Sin título 2.md line 27] `written:2022-07-05_sin-titulo-2:environment-ejecuta-funciones`: "el environment tambien debe manejar 1\) la ejecución de funciones para generar nuevas variables."
- 2022-07-05 07:53 Luciano refines [2022-07-05 Sin título 2.md line 33] `written:2022-07-05_sin-titulo-2:frontera-con-el-sistema-operativo`: "Esto claramente es un problema que excede al del environment aunque esta unido indefectiblemente porque necesitas memoria y recursos computacionales para opera…"

### L-environment-stores-retrieves (language)

The environment is a map of definitions whose two mechanisms are storing and retrieving variables by name.

first 2022-07-05 07:53 by Luciano; 3 rows, 3 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 15] `written:2022-07-05_sin-titulo-2:dos-mecanismos-del-environment`: "Hay dos mecanismos fundamentales del environment"
- 2022-07-05 07:53 Luciano restates [2022-07-05 Sin título 2.md line 9] `written:2022-07-05_sin-titulo-2:environment-como-mapa-de-definiciones`: "El environment no puede ser otra cosa que un mapa de definiciones o valores (las llamaremos variables, pero pueden ser constantes, tendria que encontrar un nom…"
- 2022-07-05 07:53 Luciano refines [2022-07-05 Sin título 2.md line 37] `written:2022-07-05_sin-titulo-2:variables-descienden-del-environment`: "todas las variables decienden environment, en el sentido de que pueden guardar nuevos valores y recuperar los valores guardados, siempre que les indiques su no…"

### L-variable-is-fields (language)

A variable is a name, a memory address, a size and a type; the type contains the size and the name can be the address.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 45] `written:2022-07-05_sin-titulo-2:variable-como-nombre-direccion-tamano-tipo`: "una variable es un nombre, una direccion de memoria, un tamaño de memoria y un typo. En realidad el tipo contiene el tamaño de memoria y el nombre, si se quier…"

### L-variable-not-know-environment (language)

A variable knows its name but should not know its environment, so its resource acquisition stays predictable.

first 2022-07-05 07:53 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-07-05

- 2022-07-05 07:53 Luciano states [2022-07-05 Sin título 2.md line 43] `written:2022-07-05_sin-titulo-2:variable-no-debe-saber-su-environment`: "mejor que no sepa su environment, porque si la variable sabe su environment, entonces no hay forma de predecir si va a adquirir otros recursos, especialmente s…"

### L-code-operations (language)

The language builds in functions that operate on code: tests, errors, derivatives, finding equivalents, and timing.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 71] `written:2022-08-03_haskell:funciones-que-modifican-el-codigo`: "puedo aplicar funciones que modifican el codigo: como hacer tests o calcular errores o derivadas o encontar codigos equivalentes o estimar el tiempo de ejecuci…"
- 2022-08-03 11:56 Luciano refines [2022-08-03 haskell.md line 17] `written:2022-08-03_haskell:testeos-probabilidades-errores-tiempos-en-la-sintaxis`: "incorporar los testeos, las probabilidades, los errores y los tiempos de calculo en la sintaxis del lenguaje junto con las relaciones de equivalencia para las…"

### L-constructor-vs-function (language)

A constructor differs from a function in that a constructor plus its parameters is the element, making elements transparent, while a function involves a computation.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 57] `written:2022-08-03_haskell:diferencia-constructor-funcion`: "cual es la diferencia entre un constructor y una funcion?"

### L-constructors-in-type-space (language)

Constructors should live in each type's space rather than in the global space.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 53] `written:2022-08-03_haskell:constructores-en-el-espacio-de-cada-tipo`: "En haskell los constructores viven en el espacion global. quizas sea buena idea que vivan en el espacio de cada tipo"

### L-dynamic-naming (language)

For dynamically created types or functions, a name is really an address, so a generated numeric identifier suffices.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 35] `written:2022-08-03_haskell:nombres-como-direcciones`: "los nombres son grandes simplificadores de la programacion. La pregunta es si tengo tipos o funciones creadas dinamicamente, como creo nombres para ellas?"

### L-element-belongs-one-type (language)

Each element belongs to exactly one type but can serve to build many types.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 25] `written:2022-08-03_haskell:un-elemento-cumple-muchos-tipos`: "en la teoria de tipos tenemos la relacion elemento y tipo. El problema es que un elemento cumple con muchos tipos a la vez."
- 2022-08-03 11:56 Luciano corrects [2022-08-03 haskell.md line 47] `written:2022-08-03_haskell:un-elemento-un-tipo-sirve-a-muchos`: "cada elemento pertenece exactamente a un tipo, pero puede servir para construir una multitud de tipos (conversion implicita?)."

### L-function-holds-code (language)

A function holds its code written in the language plus a compiled simplified form.

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

Defining new types and functions should itself be programmable, the language writing itself, which requires a simple robust language with no syntactic sugar.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 15] `written:2022-08-03_haskell:proceso-de-creacion-de-tipos-programable`: "Yo lo que quiero hacer es que el proceso (2) pueda ser programable, es decir que el lenguaje se pueda escribir a sí mismo. Para lograr esto, el lenguaje debe s…"

### L-subtype-by-predicate (language)

A subtype (subObject) is the subset of a type whose values satisfy a predicate, a test.

first 2022-08-03 11:56 by Luciano; 3 rows, 3 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 115] `written:2022-08-03_haskell:subtipos-con-predicado`: "ambient\_temperature = type ambient\_temperature x: real \| (-30\<x)& x\<40"
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 7] `written:2022-08-03_tapp-before:equals-defines-subtypes-by-predicate`: "esa es mi idea: usar el igual para definir tipos subobjetos. (lo puedo indicar con guardas \"\|\")."
- 2022-08-03 11:56 Luciano restates [2022-08-03 tapp before.md line 13] `written:2022-08-03_tapp-before:subobject-as-central-concept`: "El concepto mas importante es el de subObjeto: un subconjunto del objeto algebraico que cumple con un cierto predicado, un test."

### L-two-kinds-of-definition (language)

There are two ways to define types, the constructive and the declarative.

first 2022-08-03 11:56 by Luciano; 3 rows, 3 witnesses, 3 days, last 2023-03-02

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 27] `written:2022-08-03_haskell:dos-formas-de-definir-tipos-constructivo-declarativo`: "hay dos formas de definir tipos: el constructivo (data en Haskell) y el declarativo (class en Haskell)."
- 2023-02-22 16:12 Luciano restates [2023-02-22 tapp wish list.md line 3] `written:2023-02-22_tapp-wish-list:dos-tipos-de-tipos`: "Dos tipos de tipos:"
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 25] `written:2023-03-02_estoy-perdido:definiciones-constructivas-y-declarativas`: "tenemos dos tipos de definiciones las constructivas y las declarativas"

### L-type-definition-recursive (language)

A type's definition is necessarily recursive, since the type must be universally accessible like identifiers.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 103] `written:2022-08-03_haskell:definicion-de-tipo-es-recursiva`: "la definicion de un tipo es necesariamente recursiva."

### L-types-make-code-safe (language)

Declaring a function declares the tests it must pass, so types encode preconditions and gate membership on testing, yielding self-verified programs.

first 2022-08-03 11:56 by Luciano; 4 rows, 4 witnesses, 3 days, last 2023-03-13

- 2022-08-03 11:56 Luciano states [2022-08-03 haskell.md line 19] `written:2022-08-03_haskell:declarar-funcion-es-declarar-su-test`: "La idea central del tapp es que al declarar una funcion vos declaras que es lo que la funcion debe cumplir como un test y entonces es posible generar tests aut…"
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 21] `written:2023-02-22_tapp-wish-list:unsafe-a-safe`: "convertir unsafe code en safe code (usando los tipos como codificadores de precondiciones)."
- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 25] `written:2023-02-22_tapp-wish-list:untested-a-tested`: "convertir untested code en tested code: haciendo que las implementaciones de las funciones solo pertenezcan a un tipo si han sido debidamente testeadas y que l…"
- 2023-03-13 14:48 Luciano restates [2023-03-13 hacia Luthier.md line 3] `written:2023-03-13_hacia-luthier:luthier-programas-autoverificados`: "como es Luthier el lenguaje para escribir programas autoverificados?"

### L-composition-dot (language)

Composition is written with a dot, which explains class methods.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 9] `written:2022-08-03_tapp-before:composition-with-dot`: "La composicion la indico con puntos . (esto explica los metodos de clases)"

### L-equals-assertion (language)

The equals sign is an assertion that both sides are equal, also used for pattern matching when a symbol is unknown.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 3] `written:2022-08-03_tapp-before:equals-as-assertion`: "encontre una idea que me puede servir de generadora para tapp/quimulun: la idea de que el signo \"=\" representa aserciones, es decir que un lado es igual al o…"
- 2022-08-03 11:56 Luciano refines [2022-08-03 tapp before.md line 5] `written:2022-08-03_tapp-before:equals-for-pattern-matching`: "Esto se usa para pattern matching cuando algun simbolo es desconocido."

### L-function-kinds (language)

Functions are of two kinds: predefined and user defined.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 41] `written:2022-08-03_tapp-before:two-kinds-of-functions`: "functions are of two types"

### L-function-type-expression (language)

Open question of how to express the type of a function such as write : a -> string.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano questions [2022-08-03 tapp before.md line 27] `written:2022-08-03_tapp-before:typing-a-write-function`: "como expreso el tipo de write a?"

### L-sum-types-with-bar (language)

Types are expressed as alternatives with a bar, as in maybe, either and sum.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 19] `written:2022-08-03_tapp-before:types-as-tagged-alternatives`: "maybe a = Nothing \| Just a"

### L-test-result-one-or-explanation (language)

A check returns success (one) if met or an explanation of why it failed, not just a boolean.

first 2022-08-03 11:56 by Luciano; 2 rows, 2 witnesses, 2 days, last 2023-03-13

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 15] `written:2022-08-03_tapp-before:test-succeeds-or-explains-failure`: "Ahora un test o es exitoso o hay una explicacion de porque falla."
- 2023-03-13 14:48 Luciano restates [2023-03-13 hacia Luthier.md line 13] `written:2023-03-13_hacia-luthier:condicion-devuelve-uno-o-mensaje`: "en realidad el resultado de cualquier condicion deberia ser uno si se cumplen las condiciones y un mensaje indicando porque no se cumplieron."

### L-type-autodetection (language)

Types can be handled by autodetection.

first 2022-08-03 11:56 by Luciano; 1 rows, 1 witnesses, 1 days, last 2022-08-03

- 2022-08-03 11:56 Luciano states [2022-08-03 tapp before.md line 11] `written:2022-08-03_tapp-before:type-autodetection`: "El otro criterio es usar la \"autodeteccion\" de tipos."

### L-express-math-structures (language)

The language must express mathematical structures (category, functor, group) with their laws, possibly in several declaration styles.

first 2023-02-22 16:12 by Luciano; 6 rows, 6 witnesses, 3 days, last 2023-03-02

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 13] `written:2023-02-22_tapp-wish-list:poder-definir-objetos-matematicos`: "Tengo que poder definir este tipo de objetos matematicos."
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 13] `written:2023-02-28_sin-titulo-1-w:categoria-como-clase-con-componentes`: "Category(Obj,Hom,Compose,Id)"
- 2023-02-28 18:06 Luciano questions [2023-02-28 Sin título 1 w.md line 1] `written:2023-02-28_sin-titulo-1-w:categoria-declaracion-estilos`: "como hago para declarar una categoria"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 5] `written:2023-02-28_sin-titulo-1-w:estilo-cpp-clases-funciones`: "Estilo c++"
- 2023-02-28 18:06 Luciano refines [2023-02-28 Sin título 1 w.md line 17] `written:2023-02-28_sin-titulo-1-w:object-y-hom-como-tipos-dependientes`: "type Hom(Object X, Object Y)"
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 15] `written:2023-03-02_estoy-perdido:expresar-definiciones-matematicas-como-categorias`: "como expreso las definiciones matematicas como categoria, functor, grupo etc"

### L-language-parts-compiler (language)

The language has parts: a grammar with semantic rules and a front compiler to C++.

first 2023-02-22 16:12 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-02-22

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 35] `written:2023-02-22_tapp-wish-list:partes-grammar-y-front-compiler`: "A. tapp grammar definition, semantics rules etc"

### L-learn-from-each-run (language)

From each run of the code something is learned, whether an implementation is correct or how fast it is.

first 2023-02-22 16:12 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-02-22

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 31] `written:2023-02-22_tapp-wish-list:aprender-de-cada-corrida`: "La idea es que de cada corrida del codigo algo se aprende, ya sea se sabe que una implementacion es correcta ya que se mide su velocidad."

### L-pre-postconditions (language)

Functions and types are defined by preconditions and postconditions, the postconditions defining the subtype.

first 2023-02-22 16:12 by Luciano; 6 rows, 5 witnesses, 3 days, last 2023-03-13

- 2023-02-22 16:12 Luciano refines [2023-02-22 tapp wish list.md line 9] `written:2023-02-22_tapp-wish-list:el-subtipo-de-una-funcion-como-precondicion-de-otra`: "lo cual hace que este subtipo sea usado como precondicion de otra funcion."
- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 9] `written:2023-02-22_tapp-wish-list:funciones-con-precondiciones-y-postcondiciones`: "Las funciones se definen con precondiciones (los subtipos de los argumentos) y postcondiciones (proposiciones que involucran a argumentos y valores retornados)."
- 2023-03-02 11:27 Luciano restates [2023-03-02 estoy perdido.md line 43] `written:2023-03-02_estoy-perdido:tipos-de-funciones-por-postcondiciones`: "Defino tipos de funciones, diciendo cuales son las postcondiciones."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 41] `written:2023-03-02_estoy-perdido:tipos-de-variables-por-postcondiciones`: "Defino tipos de variables, diciendo cuales son sus postcondiciones"
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 33] `written:2023-03-02_estoy-perdido:variables-funcion-con-verificacion-de-precondiciones`: "Defino variables que son funcion de otras variables o parametros. Se verifica si los argumentos de las funciones cumplen con las precondiciones ..."
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 9] `written:2023-03-13_hacia-luthier:creaciones-verifican-pre-y-pos`: "Las creaciones de objetos verifican que se cumplans las pre y pos conditions del objeto creado."

### L-simultaneous-definition (language)

When postconditions are interdependent, objects are defined together, in tuples with crossconditions, the one form of definition.

first 2023-02-22 16:12 by Luciano; 4 rows, 4 witnesses, 3 days, last 2023-03-13

- 2023-02-22 16:12 Luciano states [2023-02-22 tapp wish list.md line 11] `written:2023-02-22_tapp-wish-list:definir-funciones-en-grupo`: "Esto hace que muchas funciones se deban definir en grupo ya que las postcondiciones involucran a varias funciones a la vez (como leer y escribir o las operacio…"
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 45] `written:2023-03-02_estoy-perdido:tuplas-con-crosscondiciones`: "Defino una tupla de tipos de variables y de funciones con postcondiciones que involucran a toda la tupla. (crosscondiciones)."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 47] `written:2023-03-02_estoy-perdido:unica-forma-de-definir-es-en-tuplas`: "solo hay una forma de definir y es en tuplas, que pueden tener uno o mas identificadores."
- 2023-03-13 14:48 Luciano refines [2023-03-13 hacia Luthier.md line 11] `written:2023-03-13_hacia-luthier:asignacion-simultanea-por-interdependencia`: "En el caso que las postcondiciones de los objetos sean interdependientes, los objetos se asignan simultaneamente."

### L-forms-of-definition (language)

The language distinguishes declaration from definition and lets one define functions or variables by their type without giving the implementation or value (parameters).

first 2023-03-02 11:27 by Luciano; 4 rows, 4 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 21] `written:2023-03-02_estoy-perdido:declaration-vs-definition`: "1\) declaration: decis que algo tiene un tipo"
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 37] `written:2023-03-02_estoy-perdido:funciones-por-postconditions-sin-implementacion`: "Defino funciones que son de un tipo dado (es decir que cumplen con ciertas postconditions) sin decir cual es la implmentacion."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 39] `written:2023-03-02_estoy-perdido:implementacion-que-depende-de-implementaciones-desconocidas`: "Defino funciones y doy su implementacion que depende de funciones cuya implementacion no se."
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 31] `written:2023-03-02_estoy-perdido:parametros-variables-de-tipo-sin-valor`: "Defino variables de un tipo dado sin decir cual es el valor, es decir parametros."

### L-functor-as-implementation (language)

A functor is read as an implementation and a natural transformation as translating one implementation into another.

first 2023-03-02 11:27 by Luciano; 2 rows, 2 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 9] `written:2023-03-02_estoy-perdido:functores-como-implementaciones`: "Functores : implementaciones"
- 2023-03-02 11:27 Luciano refines [2023-03-02 estoy perdido.md line 11] `written:2023-03-02_estoy-perdido:natural-transformations-como-traduccion`: "Natural transformations: traducir una implementacion en otra"

### L-type-inference (language)

The type is deduced by type calculation, and a derived type larger than the parameter's type is flagged.

first 2023-03-02 11:27 by Luciano; 1 rows, 1 witnesses, 1 days, last 2023-03-02

- 2023-03-02 11:27 Luciano states [2023-03-02 estoy perdido.md line 35] `written:2023-03-02_estoy-perdido:tipo-deducido-por-calculo-de-tipos`: "El tipo se deduce por el calculo de tipos. Si el tipo derivado es mayor que el tipo del parametro, se indica."

### L-luthier-is-assignments (language)

Luthier is a chain of assignments, each an identifier, an equals sign and an operation that creates the object.

first 2023-03-13 14:48 by Luciano; 2 rows, 2 witnesses, 1 days, last 2023-03-13

- 2023-03-13 14:48 Luciano states [2023-03-13 hacia Luthier.md line 7] `written:2023-03-13_hacia-luthier:asignacion-identificador-igual-operacion`: "cada asignacion tiene un identificador para recuperar el objeto creado, un signo igual y una operacion para crear el objeto."
- 2023-03-13 14:48 Luciano restates [2023-03-13 hacia Luthier.md line 5] `written:2023-03-13_hacia-luthier:luthier-cadena-de-asignaciones`: "Luthier es una cadena de asignaciones."

### L-compile-time-prevents-invalid (language)

The type system prevents invalid models from being constructed, eliminating consistency violations at compile time before execution or inference.

first 2025-06-17 06:20 by model; 7 rows, 6 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 25] `written:2025-06-17_hottification-program:type-checking-prevents-invalid-models`: "Semantic modeling language prevents invalid models from being constructed."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 25] `written:2025-06-17_program-hott-dsl:types-prevent-invalid-models`: "Semantic modeling language prevents invalid models from being constructed."
- 2025-06-17 06:21 model proposes [term_hottification.md line 17] `written:2025-06-17_term-hottification:compile-time-correctness-instead-of-runtime-validation`: "Replacing external or runtime-only validation with **compile-time structural correctness**."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 14] `written:2025-06-17_vault-glossary-v1:compile-time-structural-validation`: "Compile-time structural validation of models."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 27] `written:2025-06-17_vault-glossary-v1:invalid-models-eliminated-at-type-level`: "Violations of model consistency are eliminated at the type level, prior to execution or inference."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 27] `written:2025-06-17_vault-glossary-v1:semantic-safety-enforced-by-the-language`: "Semantic safety refers to model correctness enforced by structural rules in the modeling language itself, ensuring that only structurally valid models can be c…"
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 31] `written:2025-06-17_vault-glossary-v1:semantic-safety-prevents-invalid-models-from-existing`: "Semantic safety: prevents invalid scientific models from existing."

### L-couplings-as-types (language)

Energetic couplings, binding schemes and conformational spaces are represented and certified as types.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 26] `written:2025-06-17_hottification-program:certified-binding-and-energetic-objects`: "Certified binding schemes, conformational spaces, energetic couplings."
- 2025-06-17 06:20 model proposes [Hottification program.md line 52] `written:2025-06-17_hottification-program:energetic-couplings-as-types`: "Energetic couplings as types."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 52] `written:2025-06-17_program-hott-dsl:energetic-couplings-as-types`: "Energetic couplings as types."

### L-dep-types-composition (language)

Hierarchical, algebraic model composition across subunits, pathways and scales is enforced by dependent types.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 31] `written:2025-06-17_hottification-program:algebraic-composability-across-scales`: "Algebraic model composability across subunits, pathways, and scales."
- 2025-06-17 06:20 model proposes [Hottification program.md line 32] `written:2025-06-17_hottification-program:dependent-types-for-hierarchy`: "Hierarchical model construction naturally enforced by dependent types."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 32] `written:2025-06-17_program-hott-dsl:hierarchical-models-via-dependent-types`: "Hierarchical model construction naturally enforced by dependent types."

### L-dsl-as-model-compiler (language)

The DSLs are model compilers that translate high-level mechanistic specifications into executable, inferable structures.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 33] `written:2025-06-17_hottification-program:mechanistic-to-kinetic-transition`: "Clean transitions from mechanistic theories to kinetic models."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 102] `written:2025-06-17_vault-glossary-v1:dsls-as-model-compilers`: "The DSLs you are building serve as model compilers."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 100] `written:2025-06-17_vault-glossary-v1:model-compiler`: "A system that translates high-level mechanistic model specifications into executable, inferable structures (e.g. state spaces, likelihood functions, samplers)."

### L-dsl-unifies-domains (language)

One DSL framework unifies models across channels, enzymes, networks, signaling and regulation.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 121] `written:2025-06-17_hottification-program:universality-across-biological-domains`: "The DSL framework unifies models across channels, enzymes, networks, signaling, and regulation."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 121] `written:2025-06-17_program-hott-dsl:universality-across-biological-domains`: "The DSL framework unifies models across channels, enzymes, networks, signaling, and regulation."

### L-embedded-semantic-structure (language)

Biological models carry embedded semantic structure such as symmetry groups, compositional operators and equivalence classes.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 14] `written:2025-06-17_hottification-program:models-carry-embedded-semantic-structure`: "Allow biological models to carry embedded semantic structure:"
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 14] `written:2025-06-17_program-hott-dsl:models-carry-embedded-semantic-structure`: "Allow biological models to carry embedded semantic structure:"

### L-formalize-state-energy-algebra (language)

Planned work to formalize a type system for state and energy algebra and HoTT-based state composition primitives.

first 2025-06-17 06:20 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 135] `written:2025-06-17_hottification-program:type-system-for-state-and-energy-algebra`: "Formalize type system for state and energy algebra"

### L-hott-dsl-for-biology (language)

Build a domain-specific modeling language on Homotopy Type Theory for expressing, composing and transforming biological models with access to type-level structure.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 9] `written:2025-06-17_hottification-program:language-on-hott-for-biological-models`: "Build a domain-specific modeling language based on Homotopy Type Theory (HoTT) that allows biological models to be expressed, composed, and transformed with fu…"
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 9] `written:2025-06-17_program-hott-dsl:dsl-based-on-hott-for-biological-models`: "Build a domain-specific modeling language based on Homotopy Type Theory (HoTT) that allows biological models to be expressed, composed, and transformed with fu…"

### L-hott-ingredients-sufficient (language)

Sigma-types, Pi-types, identity types and HITs suffice to encode conformational models, energetic couplings and symmetry structures.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 129] `written:2025-06-17_hottification-program:hottification-primitives-sufficiency`: "Sigma-types, Pi-types, identity types, HITs are sufficient to encode conformational models, energetic couplings, and symmetry structures."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 129] `written:2025-06-17_program-hott-dsl:hottification-feasibility`: "Sigma-types, Pi-types, identity types, HITs are sufficient to encode conformational models, energetic couplings, and symmetry structures."

### L-hott-prob-tension (language)

There is a tension between HoTT's invertible identities and univalence and probability's non-invertible uncertainty, with no fully unified model yet.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 91] `written:2025-06-17_hottification-program:foundational-tension-hott-vs-probability`: "HoTT: invertible identities, univalence, internalized equivalence."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 91] `written:2025-06-17_program-hott-dsl:foundational-tension-hott-vs-probability`: "HoTT: invertible identities, univalence, internalized equivalence."

### L-likelihood-type-propagation (other)

Likelihood recursion is encoded via type-theoretic propagation, with noise structures and model boundaries as dependent types.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 163] `written:2025-06-17_hottification-program:macroir-likelihood-via-type-propagation`: "Encode likelihood recursion via type-theoretic propagation."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 163] `written:2025-06-17_program-hott-dsl:likelihood-recursion-via-type-propagation`: "Encode likelihood recursion via type-theoretic propagation."
- 2025-06-17 06:21 model proposes [term_hottification.md line 29] `written:2025-06-17_term-hottification:likelihood-recursion-type-propagated`: "Inference engines (where likelihood recursion is type-propagated)."

### L-markov-generated (language)

Markov models become generated objects rather than arbitrary inputs.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 38] `written:2025-06-17_hottification-program:markov-models-as-generated-objects`: "Markov models become generated objects rather than arbitrary inputs."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 38] `written:2025-06-17_program-hott-dsl:markov-models-as-generated-objects`: "Markov models become generated objects rather than arbitrary inputs."

### L-meta-layer (language)

The language sits as a meta-layer above the ConformationalModel DSL, MacroIR and Bayesian pipelines.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 18] `written:2025-06-17_hottification-program:meta-layer-above-existing-dsls`: "Serve as meta-layer above ConformationalModel DSL, MacroIR, and Bayesian pipelines."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 18] `written:2025-06-17_program-hott-dsl:meta-layer-above-existing-dsls`: "Serve as meta-layer above ConformationalModel DSL, MacroIR, and Bayesian pipelines."

### L-models-as-well-typed-objects (language)

Biological models are well-typed objects where types are molecular states, identity paths are symmetries, and composition emerges from dependent type operations.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 105] `written:2025-06-17_hottification-program:types-as-molecular-states`: "Biological models can be defined as well-typed objects where types represent molecular states, identity paths represent symmetries, and model composition emerg…"
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 105] `written:2025-06-17_program-hott-dsl:models-as-well-typed-objects`: "Biological models can be defined as well-typed objects where types represent molecular states, identity paths represent symmetries, and model composition emerg…"

### L-proof-assistants-verify (language)

Proof assistants (Coq, Lean, Agda) can verify the semantic correctness of biological models via type-checking.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 125] `written:2025-06-17_hottification-program:proof-assistant-verification`: "Proof assistants (Coq, Lean, Agda) can verify semantic correctness of biological models via type-checking."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 125] `written:2025-06-17_program-hott-dsl:machine-checkable-via-proof-assistants`: "Proof assistants (Coq, Lean, Agda) can verify semantic correctness of biological models via type-checking."

### L-sampler-type-indexed (other)

Sampler state spaces and parameter manifolds are treated as type-indexed temperature-ladder manifolds.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 159] `written:2025-06-17_hottification-program:tempering-state-spaces-as-type-indexed-ladders`: "Map parameter manifolds as type-indexed temperature ladders."
- 2025-06-17 06:21 model proposes [term_hottification.md line 28] `written:2025-06-17_term-hottification:sampler-spaces-as-type-indexed-manifolds`: "Sampler spaces (parallel tempering spaces as type-indexed manifolds)."

### L-separate-structure-inference (language)

Deterministic structural validity (via HoTT) is kept separate from probabilistic inference (via Bayesian layers), probability handled downstream.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 19] `written:2025-06-17_hottification-program:separate-structural-validity-from-inference`: "Separate deterministic structural validity (via HoTT) from probabilistic inference (via Bayesian layers)."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 19] `written:2025-06-17_program-hott-dsl:separate-structural-validity-from-probabilistic-inference`: "Separate deterministic structural validity (via HoTT) from probabilistic inference (via Bayesian layers)."

### L-symmetry-as-identity-paths (language)

Symmetry reductions are path-based identities that collapse state redundancies into reduced Markov spaces.

first 2025-06-17 06:20 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 53] `written:2025-06-17_hottification-program:symmetry-reductions-as-path-identities`: "Symmetry reductions as path-based identities."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 113] `written:2025-06-17_program-hott-dsl:identity-types-collapse-redundancy`: "Identity types automatically collapse state redundancies and symmetries into reduced Markov spaces."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 53] `written:2025-06-17_program-hott-dsl:symmetry-reductions-as-path-identities`: "Symmetry reductions as path-based identities."

### L-type-safe-priors (other)

Type-safe prior spaces bridge the MacroIR likelihood engine with structural model spaces.

first 2025-06-17 06:20 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 37] `written:2025-06-17_hottification-program:type-safe-prior-spaces`: "Type-safe prior spaces for inference pipelines."

### L-types-spaces-identities-paths (language)

HoTT gives types as spaces and identities as paths, its internal equality replacing ad hoc isomorphisms.

first 2025-06-17 06:20 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:20 model proposes [Hottification program.md line 77] `written:2025-06-17_hottification-program:internal-equality-replaces-isomorphisms`: "Internal equality replaces ad hoc isomorphisms."
- 2025-06-17 06:20 model proposes [program_hott_dsl.md line 75] `written:2025-06-17_program-hott-dsl:types-as-spaces-identities-as-paths`: "Provides types as spaces, identities as paths, higher paths as equivalences."

### L-dep-types-semantic-safety (language)

Dependent typing enforces semantic safety, guaranteeing the internal consistency of model compositions.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 16] `written:2025-06-17_term-hottification:semantic-safety-via-dependent-typing`: "Enforcing **semantic safety** via dependent typing, guaranteeing internal consistency of model compositions."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 13] `written:2025-06-17_vault-glossary-v1:dependent-types-enforce-semantic-safety`: "Dependent types enforcing semantic safety."

### L-encode-as-types (language)

Model components, entities and deterministic structure are encoded as types.

first 2025-06-17 06:21 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 27] `written:2025-06-17_term-hottification:lifting-deterministic-structure-into-types`: "Probabilistic models (where deterministic structure is lifted into types)."
- 2025-06-17 06:21 model proposes [term_hottification.md line 13] `written:2025-06-17_term-hottification:model-components-as-types`: "Encoding model components as **types**."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 10] `written:2025-06-17_vault-glossary-v1:types-as-entities`: "Types as entities."

### L-higher-paths-symmetries (language)

Higher-order symmetries and transformations between equivalences are captured as higher paths.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 15] `written:2025-06-17_term-hottification:symmetries-as-higher-paths`: "Capturing higher-order symmetries and structural relations as **higher paths**."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 12] `written:2025-06-17_vault-glossary-v1:higher-paths-as-equivalence-transformations`: "Higher paths as equivalence transformations."

### L-hottification-definition (language)

HoTTification is transforming a scientific model, algorithm or modeling language into a formal structure governed by HoTT, analogous to categorification or quantization.

first 2025-06-17 06:21 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 40] `written:2025-06-17_term-hottification:analogy-to-categorification-formalization-quantization`: "Categorification** (Category Theory)"
- 2025-06-17 06:21 model proposes [term_hottification.md line 9] `written:2025-06-17_term-hottification:hottification-as-transforming-a-model-into-a-hott-structure`: "**HoTTification** is the process of transforming a scientific model, algorithm, or modeling language into a formal structure governed by the principles of **Ho…"
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 8] `written:2025-06-17_vault-glossary-v1:hottification-as-transforming-models-into-hott-structure`: "HoTTification is the process of transforming a scientific model, algorithm, or modeling language into a formal structure governed by Homotopy Type Theory (HoTT…"

### L-hottification-models-typed-objects (language)

Under HoTTification models themselves become typed mathematical objects whose equivalences, symmetries and compositions are validated by the type system.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 19] `written:2025-06-17_term-hottification:models-as-typed-mathematical-objects`: "**models themselves become typed mathematical objects**, with equivalences, symmetries, and compositions validated directly by the type system."
- 2025-06-17 06:21 model proposes [term_hottification.md line 33] `written:2025-06-17_term-hottification:unification-of-model-algebra-and-identity-preserving-transformations`: "A unification of model algebra, compositional safety, and identity-preserving transformations."

### L-identity-paths-equivalences (language)

Identity paths represent structural equivalences between model entities.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 14] `written:2025-06-17_term-hottification:equivalences-as-identity-paths`: "Representing equivalences between model structures as **identity paths**."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 11] `written:2025-06-17_vault-glossary-v1:identity-paths-as-structural-equivalences`: "Identity paths as structural equivalences."

### L-machine-verifiable-theories (other)

HoTTification offers a path toward machine-verifiable biological theories.

first 2025-06-17 06:21 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 32] `written:2025-06-17_term-hottification:path-toward-machine-verifiable-biological-theories`: "A path toward machine-verifiable biological theories."

### L-runtime-vs-semantic-safety (language)

Runtime safety prevents crashes while semantic safety, a layer above runtime, prevents invalid models from existing at all.

first 2025-06-17 06:21 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:21 model proposes [term_hottification.md line 44] `written:2025-06-17_term-hottification:semantic-safety-layer-above-runtime`: "Introduces **semantic safety layer** above runtime execution."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 30] `written:2025-06-17_vault-glossary-v1:runtime-vs-semantic-safety`: "Runtime safety: prevents crashes or numeric failures."

### L-bayesian-mapping (other)

Scientific knowledge production is mapped into explicit Bayesian structures (introduction to prior, methods to likelihood, results to observations, discussion to posterior) to make reasoning auditable and probabilistic.

first 2025-06-17 06:23 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 40] `written:2025-06-17_vault-glossary-v1:bayesianization-of-the-scientific-pipeline`: "The process of formally mapping scientific knowledge production into explicit Bayesian structures:"
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 42] `written:2025-06-17_vault-glossary-v1:paper-sections-as-bayesian-components`: "Introduction → Prior."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 47] `written:2025-06-17_vault-glossary-v1:science-made-auditable-and-probabilistic`: "The goal is to make scientific reasoning auditable, quantifiable, and explicitly probabilistic at every step."

### L-compositional-kinetic (language)

Kinetic models are built compositionally from conformational state components as an external product of degrees of freedom with energetic coupling rules and state aggregation.

first 2025-06-17 06:23 by model; 3 rows, 3 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 70] `written:2025-06-17_vault-glossary-v1:conformational-algebra`: "A compositional system for building kinetic models from conformational state components:"
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 72] `written:2025-06-17_vault-glossary-v1:external-product-of-conformational-dof`: "External product of conformational degrees of freedom."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 75] `written:2025-06-17_vault-glossary-v1:symmetry-reduction-and-state-aggregation`: "State aggregation based on equivalent coupling configurations."

### L-fisher-validation (other)

A likelihood implementation is validated by agreement between the Fisher Information Matrix from score covariance and the one from the Hessian, without full inference.

first 2025-06-17 06:23 by model; 1 rows, 1 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 90] `written:2025-06-17_vault-glossary-v1:fim-self-consistency-diagnostic`: "Agreement between these two estimates validates the correctness of likelihood implementation without requiring full inference."

### L-macroir-consumes-models (other)

MacroIR consumes structurally defined Markov models and computes interval-averaged likelihoods for macroscopic current data.

first 2025-06-17 06:23 by model; 2 rows, 2 witnesses, 1 days, last 2025-06-17

- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 60] `written:2025-06-17_vault-glossary-v1:macroir-consumes-markov-models`: "MacroIR consumes Markov models produced by ConformationalModel DSL or HoTTified model generators."
- 2025-06-17 06:23 model proposes [vault_glossary_v1.md line 57] `written:2025-06-17_vault-glossary-v1:macroirization`: "The act of feeding structurally defined kinetic models into the MacroIR likelihood recursion engine, which computes full interval-averaged likelihoods for macr…"

## Unplaced rows

