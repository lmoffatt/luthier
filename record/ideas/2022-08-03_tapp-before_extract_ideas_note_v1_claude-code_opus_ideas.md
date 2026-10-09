---
note: 2022-08-03 tapp before.md
note_dir: HoTTification
note_sha256: 46814474895251258a1fa0ca46d811f67e974d28ef7cfe7df76ecc53d00464d7
title: "tapp before"
author: Luciano
created: 2022-08-03T11:56:32
ideas: 12
quotes_found: 12/12
generated_by: extract_ideas_note_v1
prompt_sha256: ac79a499254c8de3dca716216dd9c31ce764157b507b66a3aebe4329199d1f49
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### equals-as-assertion
- **What**: The sign "=" is read as an assertion that one side equals the other; this is taken as a generating idea for tapp/quimulun.
- **Quote**: "encontre una idea que me puede servir de generadora para tapp/quimulun: la idea de que el signo \"=\" representa aserciones, es decir que un lado es igual al otro." (line 3)

### equals-for-pattern-matching
- **What**: The equals sign is used for pattern matching when some symbol is unknown.
- **Quote**: "Esto se usa para pattern matching cuando algun simbolo es desconocido." (line 5)

### equals-defines-subtypes-by-predicate
- **What**: His proposal: use equals for assertions with predicates, to define subobject types, possibly indicated with guards "|".
- **Quote**: "esa es mi idea: usar el igual para definir tipos subobjetos. (lo puedo indicar con guardas \"\|\")." (line 7)
- **Open**: whether equals is in fact used for predicate assertions is left uncertain ("No se si se usa para aserciones con predicados").

### composition-with-dot
- **What**: Composition is written with a dot ".", and this is said to explain class methods.
- **Quote**: "La composicion la indico con puntos . (esto explica los metodos de clases)" (line 9)

### type-autodetection
- **What**: Another criterion is to use "autodetection" of types.
- **Quote**: "El otro criterio es usar la \"autodeteccion\" de tipos." (line 11)

### subobject-as-central-concept
- **What**: The most important concept is the subObject: a subset of the algebraic object satisfying a predicate, a test.
- **Quote**: "El concepto mas importante es el de subObjeto: un subconjunto del objeto algebraico que cumple con un cierto predicado, un test." (line 13)

### test-succeeds-or-explains-failure
- **What**: A test either succeeds or there is an explanation of why it fails.
- **Quote**: "Ahora un test o es exitoso o hay una explicacion de porque falla." (line 15)

### types-as-tagged-alternatives
- **What**: Types expressed as alternatives with "|", shown through maybe, either, and sum.
- **Quote**: "maybe a = Nothing \| Just a" (line 19)
- **Also at**: lines 21, 23

### typing-a-write-function
- **What**: How to express the type of a function write a : a->string is raised as an open question.
- **Quote**: "como expreso el tipo de write a?" (line 27)
- **Open**: the question is posed, not answered.

### identity-with-universal-law
- **What**: Identity is given with a universal law that id x equals x for all x.
- **Quote**: "Identity id \| for_all x:a {id x = x}" (line 29)

### io-type-with-roundtrip-laws
- **What**: An io type carries write and read functions and laws that writing then reading recovers the value, and reading then writing recovers the string.
- **Quote**: "when (for_all x: a {x\| write \| read = (Just x,\"\")}) & (forall y: s {y\| read \| write = y})" (line 37)
- **Also at**: lines 33, 35, 39
- **Open**: the io definition line 39 trails off ("= forall T t:") unfinished.

### two-kinds-of-functions
- **What**: Functions are of two types: predefined types and user defined.
- **Quote**: "functions are of two types" (line 41)
- **Also at**: lines 43, 45
