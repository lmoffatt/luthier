---
note: 2023-03-02 estoy perdido.md
note_dir: HoTTification
note_sha256: 9300733d3ba481b113f29ae95bdcfa953005bb39e777c0d35b587ab2c7ffee03
title: "estoy perdido"
author: Luciano
created: 2023-03-02T11:27:43
ideas: 15
quotes_found: 15/15
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### functores-como-implementaciones
- **What**: A functor is read as an implementation.
- **Quote**: "Functores : implementaciones" (line 9)

### natural-transformations-como-traduccion
- **What**: A natural transformation is read as translating one implementation into another.
- **Quote**: "Natural transformations: traducir una implementacion en otra" (line 11)

### expresar-definiciones-matematicas-como-categorias
- **What**: The important question is how to express mathematical definitions (category, functor, group) in the language.
- **Quote**: "como expreso las definiciones matematicas como categoria, functor, grupo etc" (line 15)
- **Open**: left as a question, not resolved.

### hott-o-zmt-como-base
- **What**: Whether to start from HoTT or from ZMT as the foundation.
- **Quote**: "empiezo con HoTT o con ZMT?" (line 17)
- **Open**: posed as an undecided choice.

### declaration-vs-definition
- **What**: Two notions kept from reading HoTT: declaration (saying something has a type) and definition (saying how to obtain the value).
- **Quote**: "1\) declaration: decis que algo tiene un tipo" (line 21)
- **Also at**: line 23

### definiciones-constructivas-y-declarativas
- **What**: Two kinds of definitions, the constructive and the declarative.
- **Quote**: "tenemos dos tipos de definiciones las constructivas y las declarativas" (line 25)

### parametros-variables-de-tipo-sin-valor
- **What**: Defining variables of a given type without stating their value, i.e. parameters.
- **Quote**: "Defino variables de un tipo dado sin decir cual es el valor, es decir parametros." (line 31)

### variables-funcion-con-verificacion-de-precondiciones
- **What**: Defining variables as functions of other variables or parameters, checking that the arguments meet the preconditions (belong to the predicted type).
- **Quote**: "Defino variables que son funcion de otras variables o parametros. Se verifica si los argumentos de las funciones cumplen con las precondiciones ..." (line 33)
- **Open**: the sentence breaks off at "En caso que", leaving the else-case unstated.

### tipo-deducido-por-calculo-de-tipos
- **What**: The type is deduced by type calculation; if the derived type is larger than the parameter's type, this is flagged.
- **Quote**: "El tipo se deduce por el calculo de tipos. Si el tipo derivado es mayor que el tipo del parametro, se indica." (line 35)

### funciones-por-postconditions-sin-implementacion
- **What**: Defining functions of a given type (meeting certain postconditions) without stating the implementation.
- **Quote**: "Defino funciones que son de un tipo dado (es decir que cumplen con ciertas postconditions) sin decir cual es la implmentacion." (line 37)

### implementacion-que-depende-de-implementaciones-desconocidas
- **What**: Defining functions and giving an implementation that depends on functions whose implementation is unknown.
- **Quote**: "Defino funciones y doy su implementacion que depende de funciones cuya implementacion no se." (line 39)

### tipos-de-variables-por-postcondiciones
- **What**: Defining variable types by stating their postconditions.
- **Quote**: "Defino tipos de variables, diciendo cuales son sus postcondiciones" (line 41)

### tipos-de-funciones-por-postcondiciones
- **What**: Defining function types by stating their postconditions.
- **Quote**: "Defino tipos de funciones, diciendo cuales son las postcondiciones." (line 43)

### tuplas-con-crosscondiciones
- **What**: Defining a tuple of variable and function types with postconditions involving the whole tuple (crossconditions).
- **Quote**: "Defino una tupla de tipos de variables y de funciones con postcondiciones que involucran a toda la tupla. (crosscondiciones)." (line 45)

### unica-forma-de-definir-es-en-tuplas
- **What**: The conclusion that there is only one way to define, in tuples, which may hold one or more identifiers.
- **Quote**: "solo hay una forma de definir y es en tuplas, que pueden tener uno o mas identificadores." (line 47)
