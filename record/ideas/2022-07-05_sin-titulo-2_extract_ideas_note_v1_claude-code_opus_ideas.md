---
note: 2022-07-05 Sin título 2.md
note_dir: HoTTification
note_sha256: 9118555d8ad1f8499602e0e2a65e5756c0607aa3142331eda1e6710fcca26b66
title: "Sin título 2"
author: Luciano
created: 2022-07-05T07:53:28
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

### environment-es-el-primer-objeto
- **What**: Loading data requires defining an environment first, so the environment is the first object the language has to define.
- **Quote**: "tengo que definir un environment donde cargar los datos, obvio." (line 5)
- **Also at**: line 7

### environment-como-mapa-de-definiciones
- **What**: The environment is nothing but a map of definitions or values, a global variable at least where it is defined; the name for its entries (variables, constants) is still unsettled.
- **Quote**: "El environment no puede ser otra cosa que un mapa de definiciones o valores (las llamaremos variables, pero pueden ser constantes, tendria que encontrar un nombre adecuado)... Y es una variable global (al menos donde esta definido...)" (line 9)
- **Open**: what to call the entries (variables, constants, something else)

### etiqueta-para-objeto-complejo
- **What**: Computation turns on identifying complex elements by a simple label; the environment provides this, returning a complex computational object from an identifying label, which lets programs stay short.
- **Quote**: "Toda la gracia de la computacion pasa por identificar elementos complejos por una simple etiqueta." (line 11)
- **Also at**: line 13

### dos-mecanismos-del-environment
- **What**: The environment has two fundamental mechanisms: storing new variables and retrieving old ones.
- **Quote**: "Hay dos mecanismos fundamentales del environment" (line 15)
- **Also at**: lines 17, 19

### dos-recursos-del-environment
- **What**: The environment has two resources: memory to store variables and computational resources to manage that memory and store or retrieve variables.
- **Quote**: "El environment tiene dos recursos: 1\) memoria para guardar las variables. 2\) recursos computacionales para manejar la memoria y guardar o recuperar las variables." (line 21)
- **Also at**: lines 23, 25

### environment-ejecuta-funciones
- **What**: The environment must also handle the execution of functions to generate new variables, which with more than one processor brings queue management, and supplying memory and compute to the functions.
- **Quote**: "el environment tambien debe manejar 1\) la ejecución de funciones para generar nuevas variables." (line 27)
- **Also at**: lines 31, 35

### frontera-con-el-sistema-operativo
- **What**: The problem of compute and memory exceeds the environment yet is tied to it, since you need memory and compute to operate one; this is the task of the operating system and compiler.
- **Quote**: "Esto claramente es un problema que excede al del environment aunque esta unido indefectiblemente porque necesitas memoria y recursos computacionales para operar un environment. Esta es la tarea del sistema operativo y del compilador..." (line 33)

### variables-descienden-del-environment
- **What**: All variables descend from the environment, in that they can store and retrieve saved values as long as you give their name.
- **Quote**: "todas las variables decienden environment, en el sentido de que pueden guardar nuevos valores y recuperar los valores guardados, siempre que les indiques su nombre." (line 37)

### environments-simples-y-compuestos
- **What**: There are simple environments (one type of value, a single identifier) and compound ones that admit multiple.
- **Quote**: "hay environments simples (solo admiten un tipo de valor y un unico identificador) y otros compuestos que admiten multiples." (line 39)

### variable-no-debe-saber-su-environment
- **What**: A variable knows its name and could know its environment, but better it does not, because if it did there would be no way to predict whether it will acquire further resources, especially since the environment can know its own environment.
- **Quote**: "mejor que no sepa su environment, porque si la variable sabe su environment, entonces no hay forma de predecir si va a adquirir otros recursos, especialmente si consideramos que el environment puede saber su environment." (line 43)
- **Also at**: line 41
- **Open**: left as a reasoned preference rather than a fixed rule

### variable-como-nombre-direccion-tamano-tipo
- **What**: A variable is a name, a memory address, a memory size and a type; in fact the type contains the size and the name, if one wants, is the memory address.
- **Quote**: "una variable es un nombre, una direccion de memoria, un tamaño de memoria y un typo. En realidad el tipo contiene el tamaño de memoria y el nombre, si se quiere, es la direccion de memoria" (line 45)
- **Also at**: line 47
