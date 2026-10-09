---
note: 2022-08-03 haskell.md
note_dir: HoTTification
note_sha256: ba05fbf8c4440b8f9f4ae8a6ffc9499c7db1ba4c6229877af86a340d5f9e6456
title: "haskell"
author: Luciano
created: 2022-08-03T11:56:18
ideas: 18
quotes_found: 18/18
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### proceso-de-creacion-de-tipos-programable
- **What**: Luciano wants the user-level process of defining new types and functions to be itself programmable, the language writing itself; this requires a simple, robust language with no syntactic sugar.
- **Quote**: "Yo lo que quiero hacer es que el proceso (2) pueda ser programable, es decir que el lenguaje se pueda escribir a sí mismo. Para lograr esto, el lenguaje debe ser simple y robusto no tener sintactic sugar." (line 15)

### testeos-probabilidades-errores-tiempos-en-la-sintaxis
- **What**: A wish to build tests, probabilities, errors and computation times into the language's syntax, together with equivalence relations for alternative functions, aiming at automatic self-optimization.
- **Quote**: "incorporar los testeos, las probabilidades, los errores y los tiempos de calculo en la sintaxis del lenguaje junto con las relaciones de equivalencia para las funciones alternativas. La idea es tener una forma de auto-optimizacion automatica." (line 17)

### declarar-funcion-es-declarar-su-test
- **What**: The central idea of tapp: declaring a function means declaring what it must satisfy as a test, so automatic tests can be generated.
- **Quote**: "La idea central del tapp es que al declarar una funcion vos declaras que es lo que la funcion debe cumplir como un test y entonces es posible generar tests automaticos." (line 19)

### proposicion-que-cada-tipo-cumple
- **What**: Each type (no distinction between type and function) should indicate the proposition it satisfies, in two versions, a computational one and a written one derived from it; propositions provable by static tests (from the algebra of propositions) or dynamic ones (checked element by element).
- **Quote**: "poder indicar en cada tipo (no distingo entre tipo y funcion) cual es la proposicion que cumple. Aqui hay dos versiones: una computacional y otra escrita. La idea es que la escrita sea derivada de la computacional. Las proposiciones pueden ser probadas con tests estaticos o dinamicos. Los test estaticos surjen del algebra de proposiciones. Los dinamicos se prueban uno a uno con los elementos de cada tipo." (line 23)

### un-elemento-cumple-muchos-tipos
- **What**: In type theory an element relates to a type, but the problem is that one element satisfies many types at once.
- **Quote**: "en la teoria de tipos tenemos la relacion elemento y tipo. El problema es que un elemento cumple con muchos tipos a la vez." (line 25)

### dos-formas-de-definir-tipos-constructivo-declarativo
- **What**: Two ways to define types, constructive (Haskell's data) and declarative (Haskell's class); a contrast with C++ concepts as predicates over types evaluated at compile time.
- **Quote**: "hay dos formas de definir tipos: el constructivo (data en Haskell) y el declarativo (class en Haskell)." (line 27)
- **Also at**: lines 31

### nombres-como-direcciones
- **What**: Names simplify programming; for dynamically created types or functions, a name is really an address or pointer, so a generated numeric identifier suffices.
- **Quote**: "los nombres son grandes simplificadores de la programacion. La pregunta es si tengo tipos o funciones creadas dinamicamente, como creo nombres para ellas?" (line 35)
- **Also at**: lines 37

### un-elemento-un-tipo-sirve-a-muchos
- **What**: The chosen element-type relation: each element belongs to exactly one type but can serve to build many types, possibly via implicit conversion.
- **Quote**: "cada elemento pertenece exactamente a un tipo, pero puede servir para construir una multitud de tipos (conversion implicita?)." (line 47)
- **Open**: whether this works by implicit conversion is left as a question.

### constructores-en-el-espacio-de-cada-tipo
- **What**: Unlike Haskell where constructors live in the global space, perhaps they should live in each type's space (maybe.just vs just).
- **Quote**: "En haskell los constructores viven en el espacion global. quizas sea buena idea que vivan en el espacio de cada tipo" (line 53)
- **Open**: `maybe.just y maybe.nothing o just y nothing ?` left undecided (line 55).

### diferencia-constructor-funcion
- **What**: The difference between a constructor and a function: a function involves a computation (a further step) so no pattern matching; the constructor plus its parameters are the element, making elements transparent as if they had public members.
- **Quote**: "cual es la diferencia entre un constructor y una funcion?" (line 57)
- **Also at**: lines 59, 61, 63
- **Open**: starts as an unclear point ("Una cosa que no me queda clara").

### codigo-como-dato
- **What**: Code as data: a function's code is like a type's parameters, except that instead of numbers or types it holds operations; computation is running the functions.
- **Quote**: "la idea del codigo como dato, es hacer que el codigo de una funcion sea como los parametros de un tipo, solo que en lugar de tener numeros o tipos, tiene operaciones." (line 65)
- **Also at**: lines 67

### funcion-guarda-script-tapp-y-compilado
- **What**: A function holds its code written in tapp (script-like) plus some simplified compiled form.
- **Quote**: "las funciones contienen el codigo escrito en tapp (es tipo script, si queres) ademas de alguna forma simplificada compilada." (line 69)

### funciones-que-modifican-el-codigo
- **What**: Being able to apply functions that modify code: run tests, compute errors or derivatives, find equivalent codes, or estimate execution time.
- **Quote**: "puedo aplicar funciones que modifican el codigo: como hacer tests o calcular errores o derivadas o encontar codigos equivalentes o estimar el tiempo de ejecucion." (line 71)

### modelo-lisp
- **What**: An inclination to follow the Lisp model, which would put a function's whole body into its parameters.
- **Quote**: "Yo creo que tengo que seguir el modelo Lisp." (line 73)
- **Also at**: lines 75
- **Open**: `habria que pensar si tiene alguna contra grande` (line 77); then concludes it is not really necessary, keeping classic syntax while taking parameter declaration and implementation as parameters (line 79).

### simetria-valor-tipo-funcion-identificador-independiente
- **What**: By the symmetry between variable-value, variable-type and variable-function, the identifier and the type should be completely independent; the identifier is a fantasy name unknown until resolved.
- **Quote**: "si aplicamos la simetria de que pasamos de una variable-valor a una variable-tipo a una variable-funcion, entonces vemos que el identificador y el tipo deberian ser completamente independientes. El identificador es un nombre de fantasia que hasta que no lo resuelvo no deberia saber cual es." (line 99)

### definicion-de-tipo-es-recursiva
- **What**: A type must be universally accessible, like identifiers, so the definition of a type is necessarily recursive (temperature = type temperature ...).
- **Quote**: "la definicion de un tipo es necesariamente recursiva." (line 103)
- **Also at**: lines 105, 109, 111

### subtipos-con-predicado
- **What**: Subtypes defined by a predicate over the value, as in ambient temperature constrained to a range.
- **Quote**: "ambient\_temperature = type ambient\_temperature x: real \| (-30\<x)& x\<40" (line 115)

### un-tipo-inyecta-varios-identificadores
- **What**: A type or function can inject more than one identifier into the environment; being ultra-explicit about how names are injected requires some mechanism, e.g. variable binds [Maybe, Just, Nothing].
- **Quote**: "un tipo o una funcion puede inyectar mas de un identificador en el environment..." (line 121)
- **Also at**: lines 123
- **Open**: the note breaks off mid-sentence at `haciendo que` (line 125), leaving the mechanism unresolved.
