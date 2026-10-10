---
date: 2026-08-31
notes:
  - audio: WhatsApp Ptt 2026-08-31 at 19.48.17.mp3
    transcript: WhatsApp Ptt 2026-08-31 at 19.48.17.md
    duration: ~12:07
    sha256: 4a4816f84e1c0b53528c5943b59ac2bbbc2c6418eb56faf6c617a655f56f6f31
  - audio: WhatsApp Ptt 2026-08-31 at 19.57.14.mp3
    transcript: WhatsApp Ptt 2026-08-31 at 19.57.14.md
    duration: ~00:16
    sha256: cdabbb9c47733dbe6fde33d40b734f2dfb3c85f19e5d8d2fc48facc2d5b66cfc
  - audio: WhatsApp Ptt 2026-08-31 at 20.00.05.mp3
    transcript: WhatsApp Ptt 2026-08-31 at 20.00.05.md
    duration: ~02:20
    sha256: 5471f498921a9f9b888b2572943198edfa6eb5ed81c5e6271f5713e39e10bfa3
ideas: 12
quotes_found: 11/12 (match: words)
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### tipo-afirma-una-proposicion
- **What**: The core of Luthier: code has meaning, and belonging to a type means asserting a proposition that the value satisfies.
- **Quote**: "O sea, si vos tenés una clase de algo, entonces significa que cumple ciertas proposiciones." (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[02:52]`)
- **Course**: `[01:02]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: he recalls the original idea that code "tiene significado" and that belonging to a type means affirming a proposition; `[02:52]`: restates it as a class meaning the value fulfills certain propositions.

### codigo-guarda-los-calculos
- **What**: If the code represents the calculations, you can autodifferentiate it, produce a step-by-step result, and get better error management; the point of Luthier is that error management be better and that things be guaranteed.
- **Quote**: "O sea, un poco la idea de Luthier es que la gestión del error sea mejor y básicamente eso, que digamos que las cosas estén garantizadas, es lo que yo digo." (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[02:35]`)
- **Course**: `[02:02]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: code representing the calculations lets him autodifferentiate, take notes, get a step-by-step result; `[02:35]`: names better error management and guarantees as the point.

### functor-olvido
- **What**: A value carries an annotation of everything already known about it, and a forgetful functor drops some of it so the record does not grow to infinity; he says he reached the forgetful functor through Luthier.
- **Quote**: "Pero claro, tengo el functor olvido que sería, me voy olvidando algunas cosas," (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[03:18]`)
- **Course**: `[01:40]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: recalls arriving at the "Funtor Olvido" through Luthier; `[03:09]`: a value/result would carry an annotation of all we already know about it; `[03:18]`: the forgetful functor drops some of it, `[03:23]` "porque si no la cosa crece al infinito"; `[10:28]`: "ver los distintos functores de olvido" as still to be worked out.
- **Open**: which forgetful functors there are is left for later.

### la-operacion-lleva-su-identidad
- **What**: Once a value is the result of a specific operation, it is that operation and not the generic one: the sum is the sum, not the magma.
- **Quote**: "si es la suma, ya es la suma y no es el magma, es la suma, no es la operación y el magma." (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[03:50]`)
- **Course**: `[03:32]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: a datum summed to another is "la suma de estos dos"; `[03:50]`: the result is the sum, not the generic operation/magma; `[04:07]`: a series of operations, from which you can take the magma, the result, the execution, the code.

### definir-una-funcion-define-su-test
- **What**: A language inspired by homotopy type theory in which defining a function already defines the test over it; you cannot define a function without its inverse and its test, and the test is the code itself. There are different levels of verification.
- **Quote**: "en el cual vos definas una función y que al definir la función ya con eso quede definido el test sobre esa función." (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[05:14]`)
- **Course**: `[05:04]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: Luthier as a language inspired by homotopy type theory; `[05:14]`: defining a function defines its test; `[05:26]`: the likelihood as a leitmotiv example; `[05:56]`: "vos lo podes tener sin testear, testeado"; `[06:00]`: "hay distintos niveles de verificación de las cosas"; `[11:17]`: "vos no podés definir una función sin su inversa"; `[11:23]`: "que el test sea el propio código", running the code runs the test, at a chosen level.

### luthier-anotador-de-codigo-ajeno
- **What**: Luthier as an annotator of code: you could "luthierize" foreign code, e.g. several Python matrix-inversion libraries, starting from the definition of what an inversion is and the property it must satisfy, within a certain error.
- **Quote**: "Vos podrías luthierizar, por ejemplo, un código ajeno, que yo de Python." (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[06:15]`)
- **Course**: `[06:11]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: "Luthiera sea como un anotador de código"; `[06:15]`: luthierize foreign Python code; `[06:22]`: take matrix-inversion libraries and luthierize them; `[06:33]`: start from the definition of inversion and the property it must satisfy, `[06:41]` "dentro de cierto error" because the inverse is not perfect.

### valor-con-error-intervalo-o-sample
- **What**: A value is really an interval of values, or a sample of values (as in a Markov chain); the seno/arcoseno case shows how precision is kept or lost depending on whether the operation is remembered.
- **Quote**: "yo tengo un valor, pero en realidad el valor es un intervalo de valores, por ejemplo," (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[07:10]`)
- **Course**: `[07:10]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: a value as an interval; `[07:16]`: or a sample of values, as a Markov chain represented by a sample; `[07:41]`: seno of 4 gives a value with an interval, arcoseno gives 4 plus an interval; `[08:00]`: if you remember you took the seno of 4, arcoseno of seno is 4 exactly; `[08:16]`: if you forget the operation, you keep a value with an interval and lose precision on inversion.

### floats-rompen-las-leyes-el-codigo-las-guarda
- **What**: Floating-point numbers do not follow the laws of numbers (associativity, etc.), but the code does; you assume the code follows them and reorganize it so execution is more efficient or more perfect.
- **Quote**: "los números floating points, que no siguen las reglas, digamos, de los números," (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[08:42]`)
- **Course**: `[08:36]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: recalls the idea; `[08:42]`: floats don't follow the number laws; `[08:56]`: the code does, you suppose it does and reorganize it so execution is more efficient/perfect.

### ejecucion-como-funcion-olvido-codigo-que-genera-codigo
- **What**: Execution understood as a forgetful function: code that generates code, with two levels of execution, one that keeps the generated code and one that forgets it; you can keep the original function or regenerate the intermediate calculations.
- **Quote**: "Sí, o sea, básicamente, sí, es código que genera código," (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[09:56]`)
- **Course**: `[09:09]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: "la idea de la ejecución como una función olvido"; `[09:16]`: an execution that remembers the original function, or one plus a forgetful function; `[09:31]`: a more generic function where you forget what is inside but can regenerate the intermediate calculations; `[09:56]`: code that generates code; `[10:07]`: two levels of execution, one keeping the generated code and one forgetting it.

### objetivo-de-luthier
- **What**: Open question of what Luthier is actually for: whether it would simplify macro IR, and the admission that so far it is an intellectual adventure whose objective he still has to find.
- **Quote**: "porque hasta ahora es como una aventura intelectual" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[10:49]`)
- **Course**: `[00:50]` of `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3`: "¿para qué carajo serviría Luthier?"; `[04:55]`: confusion over many ideas and whether it would help simplify macro IR; `[10:47]`: he will go see what objective it would have, "hasta ahora es como una aventura intelectual"; `[12:02]`: "tengo que ir destilando las cosas que tiene que tener Luthier".
- **Open**: the objective of Luthier and whether it helps macro IR is unresolved.

### luthier-usa-la-ia-y-puede-auto-hackearse
- **What**: Luthier should be a language that uses the AI itself, with the risk that it self-hacks.
- **Quote**: "O sea, Luthier tendría que ser un lenguaje que use la IA misma, ¿no?" (`WhatsApp Ptt 2026-08-31 at 19.57.14.mp3` `[00:00]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-08-31 at 19.57.14.mp3`: Luthier as a language that uses the AI itself; `[00:11]`: "puede ser que se auto-hackee", to be worked out.
- **Open**: how to do it so it doesn't self-hack is left unresolved.

### luthier-metalenguaje-con-implementaciones
- **What**: Luthier as a metalanguage, a specification with different implementations (PyLuthier, RLuthier, Luthier CPP); the easiest start is a PyLuthier carrying the type as a class/attribute, though Python is not the right tool and the type ends up represented by fields and decorations rather than a true type.
- **Quote**: "Son especificaciones que podes tener distintas implementaciones de Luthier," (`WhatsApp Ptt 2026-08-31 at 20.00.05.mp3` `[00:08]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-08-31 at 20.00.05.mp3`: Luthier as a metalanguage; `[00:08]`: specifications with different implementations; `[00:16]`: PyLuthier, RLuthier, Luthier CPP; `[00:34]`: it will likely have to be a PyLuthier, carrying the type as a class of an attribute "flotando"; `[01:51]`: "Python no es la herramienta"; `[02:03]`: the tool is not a real type; `[02:09]`: "El tipo está representado por campos, por decoraciones."
- **Open**: whether to start with a PyLuthier, do C++, or build a language of his own is left among "todas las posibilidades".

## Notes

none.
