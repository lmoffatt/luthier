---
audio: WhatsApp Ptt 2026-05-29 at 14.28.55.mp3
fecha: 2026-05-29
duracion: ~06:05
ideas: 9
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### luthier-como-relator-de-abstracciones
- **Qué**: Luthier pensado como un mecanismo de abstracción que permita expresar ideas teóricas y cotidianas —probabilidad, samples, matrices, unidades, experimentos— de manera clara.
- **Cita** (verbatim): "lo más interesante es ver cómo digamos pensarlo a luthier como un relator un mecanismo de abstracción que permita expresar ideas" `[00:13]`

### expresar-invarianzas-de-disciplinas
- **Qué**: El propósito de Luthier es expresar invarianzas propias de distintas disciplinas: biología (reproducción sexual dentro de una especie), física (fermiones vs bosones), etc.
- **Cita** (verbatim): "la idea de Luthier es expresar invarianzas de las disciplinas" `[00:58]`

### prioridad-conceptual-sobre-implementacion
- **Qué**: El primer paso es expresar conceptos en Luthier; la traducción/implementación viene después. Lo conceptual puede ser profundo aunque la implementación sea dura.
- **Cita** (verbatim): "por lo menos desde el punto de vista conceptual pensar las cosas con cierta profundidad" `[04:59]`

### funciones-como-proposiciones-sobre-inputs-y-outputs
- **Qué**: Definir funciones desde el punto de vista de sus propiedades (no solo operativamente): la proposición acerca de sus inputs y outputs que cumple una manera de hacer una función.
- **Cita** (verbatim): "definición de función desde el punto de vista de las propiedades, no operativamente, o sea, o tener las dos funciones, ¿no? operativamente y las propiedades que contienen, la proposición acerca de sus inputs y outputs" `[03:42]`

### implementacion-univocamente-determinada
- **Qué**: Que la definición en Luthier determine unívocamente que algo es una implementación de un concepto (e.g., de matrices).
- **Cita** (verbatim): "de qué manera ya uno tiene unívocamente determinado que es una implementación, que lo que vos estás haciendo es una implementación de las matrices" `[02:02]`

### funciones-no-univocas-como-primitiva
- **Qué**: Modelar funciones no unívocas (funciones con error, samples/muestras) desde el lenguaje mismo, no como añadido posterior.
- **Cita** (verbatim): "que uno pueda modelar, desde el vamos, funciones no unívocas, que serían funciones con error, o sea, samples, o sea, muestras, quizás que estén ya desde el lenguaje" `[04:30]`
- **Ambigüedad / tensión**: no queda claro si "desde el lenguaje" significa primitiva del core o librería estándar temprana.

### decoradores-y-composicion-de-error
- **Qué**: Usar decoradores para representar el error de un número y su propagación (derivadas, etc.), como ya logró en C++ con templates, pero expresado fácilmente en Luthier.
- **Cita** (verbatim): "cómo, digamos, uno en Luthier puede hacer decoradores fáciles, ¿no? por ejemplo eso, el error de un número" `[03:05]`

### propiedades-algebraicas-de-decoradores
- **Qué**: Que se pueda expresar si la operación de un decorador sobre otro cumple asociatividad, conmutatividad, etc., y representarlo en Luthier de la forma más simple.
- **Cita** (verbatim): "si la operación de un decorador sobre el otro decorador, por ejemplo, si cumple la asociatividad, por ejemplo, o no, o si cumple [...] la conmutatividad" `[05:18]`

### abc-numerico-como-punto-de-partida
- **Qué**: Empezar por lo básico: números, reales, operaciones de reales, concepto de error de los reales.
- **Cita** (verbatim): "uno tiene que empezar por el ABC, los números, los reales, las operaciones de los reales y ese tipo de cosas, y bueno, también tener un concepto de error de los reales" `[02:37]`
- **Ambigüedad / tensión**: duda sobre si algunas cosas pueden darse "de por sí" (built-in) o no: "algunas cosas tenerlas dadas de por sí, ¿no? O sea que, o no, no sé, habría que eso pensar un poco".
