---
audio: WhatsApp Ptt 2026-05-29 at 14.36.03.mp3
fecha: 2026-05-29
duracion: ~02:44
ideas: 4
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### conmutatividad-de-statements
- **Qué**: La pregunta de si el orden de los statements en un programa Luthier altera el programa o no — si Luthier es conmutativo.
- **Cita** (verbatim): "una de las primeras preguntas es si Luthier, digamos, como un programa de Luthier, por ejemplo, si es conmutativo o no. Si el orden de los statements, si vos al cambiar el orden de los statements cambias el programa." `[00:00]`
- **Ambigüedad / tensión**: La pregunta queda explícitamente abierta. El autor nota que "hay que decir estrictamente, bueno, es conmutativo o no lo es" pero no resuelve. Menciona que la respuesta tiene consecuencias sobre cómo evoluciona el programa, sin desarrollar cuáles.

### pseudo-conmutatividad-en-declaraciones
- **Qué**: En la zona de declaración de funciones (distinta de la zona de ejecución), se puede lograr una pseudo-conmutatividad, como en C++ con forward declarations, donde el orden de declaración de A y B es indistinto si ambas se pre-declaran.
- **Cita** (verbatim): "cuando vos declarás funciones, y no estás en un programa sino que estás en la parte del programa en que vos declarás funciones, bueno, vos tenés formas de ser casi conmutativo, por ejemplo en C++ podés hacer una forward declaration" `[00:37]`

### codigo-como-elemento-de-luthier
- **Qué**: El código de Luthier tiene que ser él mismo un elemento de Luthier, operable por Luthier — meta-uso desde el diseño inicial, no implantado después.
- **Cita** (verbatim): "Luthier tiene que operar sobre Luthier también, o sea, tiene que haber una meta, meta uso, desde el vamos, como en LISP que medio que se implantó después. O sea, hay que pensar que Luthier tiene que ser, que el código de Luthier sea un elemento de Luthier ya también desde el vamos. O sea, el código es el primer elemento." `[02:16]`

### programas-como-objetos-del-lenguaje
- **Qué**: Hay que pensar en los programas escritos en Luthier como elementos de Luthier, que a su vez son objeto de ser programados por Luthier. La decisión sobre conmutatividad afecta cómo se opera sobre esos programas-objeto.
- **Cita** (verbatim): "hay que pensar en los programas en Luthier como elementos de Luthier también, que a su vez son, digamos, son objeto de ser programados por Luthier" `[01:56]`
- **Ambigüedad / tensión**: La conexión entre conmutatividad y meta-programabilidad queda esbozada ("eso hace que la evolución del programa sea diferente") pero no desarrollada.
