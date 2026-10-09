---
note: 2022-06-28 Luciano Code style.md
note_dir: HoTTification
note_sha256: 254463b610e2919d13eba4ecd7a9576f34eeca91ae81693ff96ee6e8db8268ec
title: "Luciano Code style"
author: Luciano
created: 2022-06-28T22:25:12
ideas: 22
quotes_found: 22/22
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### code-to-understand
- **What**: The reason for coding is understanding, and understanding requires being able to manipulate the code and see how changes in it affect observables of the code.
- **Quote**: "I code to understand." (line 3)
- **Also at**: lines 5

### expressiveness-as-observable
- **What**: Expressiveness is an observable of code: the code must express its intention for both the human reader and the compiler.
- **Quote**: "Expresividad: el codigo debe expresar la intención del mismo tanto para el que leer el codigo como para el compilador." (line 9)

### expressive-reference-to-known-structures
- **What**: Code is more expressive when it refers to known structures or algorithms and the reference is real, e.g. not calling a list an array.
- **Quote**: "refiere a estructuras o algoritmos conocidos y esta referencia es real. Por ejemplo, no puedo llamar array a una lista." (line 13)

### express-extra-computational-concepts-with-verification
- **What**: Expressiveness includes expressing extra-computational concepts (e.g. probability) intuitively and truthfully, by abstracting their computational properties and providing mechanisms to verify compliance, e.g. a probability must be between 0 and 1, rejecting out-of-range values and reporting invalid results.
- **Quote**: "Expresa conceptos extra-computacionales (por ejemplo probabilidad) de forma intuitiva y veraz. La idea es abstraer las propiedades compulacionales de estos conceptos y proveer los mecanismos para verificar su cumplimiento." (line 15)

### slow-clear-algorithm-as-gold-standard
- **What**: A clear but inefficient algorithm can be optimized by a more cryptic one declared equivalent to it; the slow clear algorithm is easier to be convinced correct and serves as gold standard for the fast obscure one.
- **Quote**: "es posible que una algoritmo que es expresado de una forma clara pero computacionalmente no eficiente pueda ser optimizado con un algoritmo mas criptico. Esto se expresa claramente como un algoritmo equivalente al algoritmo lento y claro." (line 17)

### library-for-types-with-semantics
- **What**: A library that lets one express variables and types, including functional and class types, with their semantics.
- **Quote**: "Expresar variables y tipos, y tipos funcionales, de clases etc y con sus semantica." (line 21)

### semantics-live-in-own-universe
- **What**: This semantics lives in its own universe, not that of C++, even though it uses C++ structures to express it.
- **Quote**: "Esta semantica "vive" en su propio universo que no es el de C++, aunque use las estructuras de C++ para expresarlos." (line 23)

### erase-code-data-distinction
- **What**: Creating new "objects" (values or variables, of types, functions or "classes") while losing the distinction between code and data.
- **Quote**: "poder crear nuevos "objetos" (sean valores o variables, de tipos, funciones o "clases"). Al mismo tiempo perder la distincion entre codigo y dato." (line 25)

### equivalence-relations-for-optimization
- **What**: Establishing equivalence relations in quimulun matters because it allows optimizing computation times.
- **Quote**: "Es importante establecer las relaciones de equivalencia en quimulun. Esto permite optimizar los tiempos de calculo." (line 27)
- **Also at**: lines 33

### one-to-one-reasoning-code-flow
- **What**: First objective: abstract and formalize the mechanisms of semantic determination so there is a one-to-one relation between reasoning and the flow of the code, thereby verifying the validity of the reasoning; an old idea.
- **Quote**: "abstraer y formalizar los mecanismos de determnacion sematinca de forma que haya una relacion uno a uno entre el razonamiento y el flujo del codigo. De esta forma verificar la validez de los razonamientos. Es una vieja idea." (line 31)

### choose-efficient-path-after-validity
- **What**: Second objective: once semantic validity and semantic equivalence are established, one can choose the most efficient path.
- **Quote**: "una vez que se establece la validez semantica y la equivalencia semantica se puede optar por el camino mas eficiente." (line 33)

### state-multiplicity-as-sum
- **What**: Multiplicity of states is building "the channel is in one of n states" by multiplying the proposition "the channel is in a state" by a number of possibilities; the state i among N similar states has type estado x N, with N the type 1+1+...+1.
- **Quote**: "si quiero decir el estado i entre N estados "similares", el tipo del estado i seria estado x N, siendo N el tipo 1+1+1..+1 N veces. Es decir el set de N componentes." (line 49)
- **Also at**: lines 43, 79

### channel-state-isomorphic-to-one
- **What**: Defining a type channel state isomorphic with the type ONE, and a physical channel type also isomorphic with ONE.
- **Quote**: "un tipo channel state que es isomorfico con el tipo ONE" (line 53)
- **Also at**: lines 55

### type-constructor-from-natural
- **What**: A type constructor that takes a natural number and returns a set containing that number.
- **Quote**: "un constructor de tipos que toma un numero natural y te devuelve un conjunto que contiene ese numero natural." (line 57)

### type-theory-vs-category-theory
- **What**: An open question about how far to go with type theory and how far to use category theory.
- **Quote**: "aqui tengo que pensar hasta que punto sigo con type theory y hasta que punto uso category theory." (line 59)
- **Open**: the boundary between type theory and category theory for this work is left undecided.

### channels-multiplicity-as-product
- **What**: Multiplicity of channels is expressed as a product, not a sum, an exponential to a number, in contrast with multiplicity of states as sum.
- **Quote**: "multiplicidad de canales (pero como producto, no suma, exponencial a un numero)" (line 85)

### sample-probability-duality
- **What**: Sample and probability form a duality, with tests that demonstrate it holds.
- **Quote**: "muestra y probabilidad --\> dualidad y tests que demuestran que se cumple." (line 93)

### equivalence-relation-multinomial
- **What**: An equivalence relation between (state*k)^N and the sum over multi-indices of multinomial coefficients times state^a.
- **Quote**: "Relacion de equivalencia entre (state\*k)^N y Sum\_{\|a\|=k} C(n,a) \*state^a , a-\>multiindice" (line 95)

### how-to-define-values-types-variables-functions
- **What**: The problem of how to create values and their types, variables and types of variables, functions and types of functions, with the type of a variable marked uncertain.
- **Quote**: "Como creo valores (values) y sus tipos (types), variables (variables), y tipos de variables (¿?), funciones y tipos de funciones." (line 107)
- **Open**: what "tipos de variables" is remains marked with "¿?".

### primitive-value-types
- **What**: A proposed set of primitive value types: boolean, integer, real, string, nothing (or zero), one (or something), memory, size, the last two marked uncertain.
- **Quote**: "tipos de valores primitivos: boolean, integer, real, string, nothing (or zero), one (or something), memory (¿?), size (¿?)" (line 109)
- **Open**: "memory" and "size" as primitive types are marked with "¿?".

### primitive-functions
- **What**: A set of primitive functions: arithmetic, integer division, modulo, string concatenation, logical and comparison operators.
- **Quote**: "funciones primitivas: suma, resta, multiplicacion, division, division entera, modulo, concatenacion de strings...., and, or, not, greater than, equal.." (line 111)

### dependent-types
- **What**: Dependent types are types that depend on a value, which makes their cardinality that of the type of the value they take; the definition trails off unfinished.
- **Quote**: "dependent-types: son tipos que dependen de un valor, lo cual hace que su cardinalidad sea la del typo del valor que toma" (line 115)
- **Also at**: lines 117
- **Open**: the sentence "Un dependent tipe es ." (line 117) is left incomplete.
