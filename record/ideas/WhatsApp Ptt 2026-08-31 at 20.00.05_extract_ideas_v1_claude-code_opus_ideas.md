---
audio: WhatsApp Ptt 2026-08-31 at 20.00.05.mp3
fecha: 2026-08-31
duracion: ~02:20
ideas: 7
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### luthier-como-metalenguaje-con-multiples-implementaciones
- **Qué**: Luthier no es una implementación sino un metalenguaje o conjunto de especificaciones, del que pueden existir varias implementaciones concretas (PyLuthier, un Luthier en C++, etc.).
- **Cita** (verbatim): "Son especificaciones que podes tener distintas implementaciones de Luthier, podes tener un Piluthier, Arluthiero o un Luthier CPP, no sé, distintas cosas." `[00:08]`

### piluthier-como-clase-atributo-flotante
- **Qué**: La implementación en Python (PyLuthier) se llevaría como una clase de un atributo que "va flotando"; el autor la señala como la opción más fácil.
- **Cita** (verbatim): "lo llevas como una clase de un atributo básicamente va flotando así... creo que es lo más fácil" `[00:43]`

### implementacion-cpp-mas-dificil
- **Qué**: Hacer Luthier en C++ es más difícil que la vía Python.
- **Cita** (verbatim): "en C++ es un poco más más difícil" `[01:01]`

### luthier-como-lenguaje-propio
- **Qué**: Alternativa a implementar Luthier dentro de un lenguaje anfitrión: hacer directamente un lenguaje propio, un Luthier que sea él mismo un lenguaje.
- **Cita** (verbatim): "casi la otra es hacer directamente un lenguaje de uno mismo" `[01:07]`
- **Ambigüedad / tensión**: Queda sin decidir entre implementar Luthier embebido (como clase/atributo en Python) o construirlo como lenguaje autónomo; el autor dice "debo ver todas las posibilidades" `[01:31]`.

### estrategia-empezar-por-lo-mas-facil
- **Qué**: Como táctica de arranque, empezar con "una especie de Luthier", la vía más fácil, antes de comprometerse con la forma final.
- **Cita** (verbatim): "quizás lo más fácil es empezar con una especie de luthier" `[01:33]`

### python-inadecuado-para-tipos
- **Qué**: Si hay que escribir cosas con tipos, Python no sería la herramienta adecuada.
- **Cita** (verbatim): "si vos tenés que escribir cosas con tipos y todo eso Python no es la herramienta" `[01:45]`
- **Ambigüedad / tensión**: El autor se contradice a sí mismo en el acto ("Ahora mira cosa que se hace más mal. Bueno, también puede ser." `[01:53]`); la inadecuación de Python para tipos queda planteada pero no cerrada.

### tipo-representado-por-campos-y-decoraciones
- **Qué**: En la vía Python el tipo no es un tipo "de verdad" del lenguaje anfitrión, sino que está representado por campos y decoraciones.
- **Cita** (verbatim): "La realidad es que la herramienta no es un tipo de verdad, sino que... El tipo está representado por campos, por decoraciones." `[02:03]`
