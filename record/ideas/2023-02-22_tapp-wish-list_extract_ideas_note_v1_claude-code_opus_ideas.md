---
note: 2023-02-22 tapp wish list.md
note_dir: HoTTification
note_sha256: 727e9f485316e4495969cee34aafc3775396687979bab89b57f3987de7e05db7
title: "tapp wish list"
author: Luciano
created: 2023-02-22T16:12:49
ideas: 11
quotes_found: 11/11
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### dos-tipos-de-tipos
- **What**: Two kinds of types: constructive ones (sum, product, exponential, function composition) and declarative ones that satisfy a proposition.
- **Quote**: "Dos tipos de tipos:" (line 3)
- **Also at**: lines 5, 7

### funciones-con-precondiciones-y-postcondiciones
- **What**: Functions are defined with preconditions (the subtypes of the arguments) and postconditions (propositions over arguments and returned values); the postconditions define the function's subtype.
- **Quote**: "Las funciones se definen con precondiciones (los subtipos de los argumentos) y postcondiciones (proposiciones que involucran a argumentos y valores retornados)." (line 9)

### el-subtipo-de-una-funcion-como-precondicion-de-otra
- **What**: The subtype defined by a function's postconditions is itself usable as a precondition of another function.
- **Quote**: "lo cual hace que este subtipo sea usado como precondicion de otra funcion." (line 9)

### definir-funciones-en-grupo
- **What**: Many functions must be defined together because their postconditions involve several functions at once, as in read and write or the operations of a mathematical object.
- **Quote**: "Esto hace que muchas funciones se deban definir en grupo ya que las postcondiciones involucran a varias funciones a la vez (como leer y escribir o las operaciones en un objeto matematico como un grupo o field." (line 11)

### poder-definir-objetos-matematicos
- **What**: A wish to be able to define this kind of mathematical object.
- **Quote**: "Tengo que poder definir este tipo de objetos matematicos." (line 13)

### code-as-data
- **What**: Code as data: being able to operate on function definitions, which requires distinguishing the code from its application.
- **Quote**: "Code as data. Debo poder operar sobre las definiciones de funciones. O sea que debo distinguir entre el codigo y la aplicacion del codigo." (line 17)

### unsafe-a-safe
- **What**: Convert unsafe code into safe code, using types as encoders of preconditions.
- **Quote**: "convertir unsafe code en safe code (usando los tipos como codificadores de precondiciones)." (line 21)

### untested-a-tested
- **What**: Convert untested code into tested code: an implementation belongs to a type only if it has been duly tested, and the testing conditions ensure the code's validity.
- **Quote**: "convertir untested code en tested code: haciendo que las implementaciones de las funciones solo pertenezcan a un tipo si han sido debidamente testeadas y que las condicones de testeo aseguran la validez del codigo." (line 25)
- **Open**: what conditions of testing would "ensure the validity" is not specified.

### optimizacion-automatica
- **What**: Allow automatic optimization of the code as the resource consumption of alternative implementations of functions is measured.
- **Quote**: "Permitir la optimizacion automatica del codigo a medida que se mide el consumo de recursos de implementaciones alternativas de distintas funciones." (line 29)

### aprender-de-cada-corrida
- **What**: From each run of the code something is learned: whether an implementation is correct, or by measuring its speed.
- **Quote**: "La idea es que de cada corrida del codigo algo se aprende, ya sea se sabe que una implementacion es correcta ya que se mide su velocidad." (line 31)
- **Open**: the phrasing conflates correctness and speed ("se sabe que una implementacion es correcta ya que se mide su velocidad") without resolving how either is established.

### partes-grammar-y-front-compiler
- **What**: The language has parts: a tapp grammar definition with semantics rules, and a front compiler from tapp to C++.
- **Quote**: "A. tapp grammar definition, semantics rules etc" (line 35)
- **Also at**: line 37
