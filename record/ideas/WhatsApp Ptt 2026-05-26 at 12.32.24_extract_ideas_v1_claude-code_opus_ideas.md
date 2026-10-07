---
audio: WhatsApp Ptt 2026-05-26 at 12.32.24.mp3
fecha: 2026-05-26
duracion: ~06:09
ideas: 9
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### tipos-como-proposiciones
- **Qué**: Los tipos en Luthier son conceptos, siguiendo la correspondencia tipos-como-proposiciones. Los tipos incluyen funciones y funciones de orden superior.
- **Cita** (verbatim): "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen también funciones, funciones y funciones de orden superior" `[00:38]`

### lenguaje-no-atado-a-cpp
- **Qué**: Luthier no debería ser estrictamente C++ sino un pseudo-lenguaje implementable en distintos lenguajes.
- **Cita** (verbatim): "la idea de que Luthier no sea estrictamente en C++ sino que sea como una especie de pseudo lenguaje que podría ser implementado en distintos lenguajes" `[01:04]`

### paths-precision-velocidad
- **Qué**: Una función puede ser implementada de muchas maneras (paths), y cada path tiene una precisión y una velocidad distintas.
- **Cita** (verbatim): "tiene una función, esta función puede ser implementada de muchas maneras, son los distintos paths y cada forma tiene una precisión y una velocidad" `[01:26]`

### declarativo-mas-optimizacion
- **Qué**: Luthier como lenguaje que es a la vez declarativo y herramienta de optimización: se declara lo que se quiere hacer y el sistema baraja distintas formas de implementarlo.
- **Cita** (verbatim): "que el Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización. O sea, que vos declares lo que querés hacer, que sigan las fórmulas, y después internamente baraja distintas formas de implementar eso, pero eso lo hace abiertamente" `[01:52]`

### mapa-declarativo-ejecutivo
- **Qué**: Luthier como mapa entre un lenguaje declarativo y un lenguaje ejecutivo.
- **Cita** (verbatim): "que Luthier permita, digamos, ser un mapa entre un lenguaje declarativo y un lenguaje ejecutivo que sería el que ejecuta las cosas" `[02:51]`

### propiedades-estimadas-por-path
- **Qué**: Cada path de ejecución tiene una estimación de características: error, tiempo de cómputo, memoria, dónde se ejecuta (clúster, computadora local, etc.).
- **Cita** (verbatim): "para cada path de ejecución tenés dos cosas. Tenés una estimación de distintas características, que es, por ejemplo, eso, el error y más que nada el tiempo de cómputo, pero también puede ser, qué sé yo, la memoria, también podría ser donde lo haces, si lo haces en un clúster, lo haces en una computadora" `[03:10]`

### lenguaje-de-orden-superior-mayordomo
- **Qué**: Luthier como lenguaje de orden superior, una especie de mayordomo que orquesta otros lenguajes, pudiendo compilar y expresar ejecución en R, Python, C++, etc.
- **Cita** (verbatim): "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo, o sea, también tendrías que poder, por ejemplo, compilar lenguajes y podés expresar, digo, bueno, a ver, esto lo hago en R, lo hago en Python o lo hago en C++ y bueno, y eso tiene tal y tal complejidad" `[03:34]`

### cross-lenguaje
- **Qué**: Luthier no es solo cross-compiler sino cross-lenguaje: agnóstico del lenguaje de implementación. Podría haber un "PyLuthier", un "RLuthier", un "CLuthier", transformables entre sí.
- **Cita** (verbatim): "luthier debería ser como una cosa que es como un lenguaje no es cross compiler sino directamente cross lenguaje o sea como que sería un poco agnóstico del lenguaje si bien el motor podría estar implementado en alguno de ellos" `[04:24]`
- **Ambigüedad / tensión**: Queda sin definir cómo se logra concretamente la transformación entre implementaciones (PyLuthier ↔ RLuthier ↔ CLuthier); lo menciona como analogía con herramientas existentes ("como hace un poco de restan y todo eso") pero no lo desarrolla.

### explorar-soluciones-y-complejidad
- **Qué**: El propósito final es que el usuario pueda encontrar distintas soluciones para su problema/ecuación y estimar la complejidad de cada forma de ejecución.
- **Cita** (verbatim): "que vos puedas encontrar la mejor solución para tu problema o, digamos, no sé si la mejor, pero bueno, distintas soluciones para tu problema y bueno, ver cuáles son las soluciones que hay, tu problema, tu ecuación y ver maneras de estimar la complejidad con distintas formas de ejecución" `[05:28]`
- **Ambigüedad / tensión**: El autor se autocorrige de "la mejor" a "distintas", dejando abierto si Luthier elige automáticamente o solo presenta opciones.
