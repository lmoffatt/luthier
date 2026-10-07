---
audio: WhatsApp Ptt 2026-05-30 at 18.01.53.mp3
fecha: 2026-05-30
duracion: ~05:56
ideas: 8
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### explicitacion-sobre-ejecucion
- **Qué**: Luthier ejecuta, pero el énfasis no está en la ejecución sino en la explicitación — la descripción del problema, de las funciones, de las condiciones para que funcionen.
- **Cita** (verbatim): "lo más importante no es la ejecución, sino la explicitación, la descripción del problema" `[01:11]`

### ejecucion-como-verificacion-de-equivalencias
- **Qué**: La ejecución en Luthier consiste en verificar equivalencias, análogo a cómo la matemática no "ejecuta" sino que verifica equivalencias.
- **Cita** (verbatim): "la ejecución en Luthier sería esa verificación de equivalencias, o sea que sí ocurre, claramente, pero el énfasis en principio está puesto en la explicitación de esas equivalencias" `[01:55]`

### niveles-de-equivalencia
- **Qué**: Una idea fundamental de Luthier es expresar distintos niveles de equivalencia — isomorfismo (contiene la misma información), igualdad exacta, misma ubicación en memoria, etc. — que dependen de algún tipo de functor de equivalencia diferente.
- **Cita** (verbatim): "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia" `[02:56]`

### equivalencias-para-clasificar-y-separar-decoraciones
- **Qué**: Las equivalencias de funciones permiten identificar qué es esencial (lo equivalente) y qué es decoración (eficiencia, costo) — lo que no es equivalente.
- **Cita** (verbatim): "si vos tenés funciones que son equivalentes, después podés ver las cosas que no son equivalentes, que es, por ejemplo, los que son las decoraciones, que es la eficiencia, por ejemplo, el costo, lo que sea" `[03:18]`

### core-minimo-bootstrapped
- **Qué**: Debería haber un core de Luthier donde se ejecuten todas las operaciones del lenguaje, implementando solo unas pocas primitivas en C o similar para que corra.
- **Cita** (verbatim): "uno debería tener claro un core de Luthier en el cual se ejecute por todas operaciones de Luthier y solamente implementar algunas pocas en C o en alguna cosa así, como para que corra" `[03:48]`

### facilidad-para-ejecutar-otros-programas
- **Qué**: Luthier necesita una facilidad (quizás vía Bash o similar) para correr otros programas y compiladores externos, como capacidad fundamental.
- **Cita** (verbatim): "tener una facilidad, que también eso tiene que ser ejecutado, tiene que ser implementado en algún lenguaje, que vos puedas correr fácilmente otros programas" `[04:07]`
- **Ambigüedad / tensión**: no está decidido el mecanismo concreto ("no sé si será en principio con Bash o algo así").

### mapeo-extensible-a-otros-lenguajes
- **Qué**: La idea es poder describir funciones y equivalencias y luego mapearlas a otros lenguajes (C, C++, Java), pero no directamente sino dando las herramientas para que otros extiendan esa traducción.
- **Cita** (verbatim): "la idea no es hacerlo directamente, sino dar las facilidades para que eso sea posible" `[05:49]`

### luthier-como-lenguaje-de-descripcion
- **Qué**: La primera etapa de Luthier es ser una especie de lenguaje de descripción — del problema, de las funciones, de las condiciones.
- **Cita** (verbatim): "la primera etapa de Luthier tiene que ser como una especie de lenguaje de descripción, descripción del problema, descripción de las funciones, descripción de las condiciones de las funciones" `[01:20]`
