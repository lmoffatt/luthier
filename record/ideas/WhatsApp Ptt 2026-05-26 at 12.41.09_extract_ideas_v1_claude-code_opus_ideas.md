---
audio: WhatsApp Ptt 2026-05-26 at 12.41.09.mp3
fecha: 2026-05-26
duracion: ~04:53
ideas: 8
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### estimacion-bayesiana-de-complejidad
- **Qué**: Ante el problema abierto de evaluar la complejidad a priori de distintos cómputos, Luthier aplicaría una estrategia bayesiana: dar oportunidad a distintos algoritmos para la misma tarea, medir sus tiempos efectivos, y estimar a partir de la experiencia acumulada.
- **Cita** (verbatim): "puede ser cualquiera y bueno, voy dándole oportunidad a distintos algoritmos para hacer lo mismo y después voy estimando los tiempos que toman para problemas parecidos a partir de la experiencia, de correrlos efectivamente" `[00:28]`
- **Ambigüedad / tensión**: no se especifica cómo se balancea exploración vs. explotación en esa estrategia bayesiana.

### base-de-datos-de-rendimiento
- **Qué**: Luthier tendría una base de datos interna que registra, para cada combinación de función, datos iniciales, escala y algoritmo, el tiempo que tardó y la precisión obtenida, medidos empíricamente.
- **Cita** (verbatim): "para esta función, con estos datos iniciales, y esta escala, yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión, y como lo sé, bueno, pues lo corrí, o sea, lo medí, efectivamente" `[01:21]`

### generalizacion-de-la-base-de-datos
- **Qué**: La base de datos de rendimiento necesita ser generalizable: pasar de mediciones puntuales a tendencias. Esa capacidad de generalización sería una de las herramientas primeras del sistema.
- **Cita** (verbatim): "esa base de datos después la tenés que poder generalizar. Entonces ahí una de las herramientas primeras sería cómo generalizar, digamos, los datos que vas obteniendo con casos puntuales." `[01:42]`
- **Ambigüedad / tensión**: el autor reconoce no saber cómo hacerlo efectivamente ("ahí estoy un poco en pelotas").

### matriz-y-estimacion-por-filas-columnas
- **Qué**: Una forma posible de organizar los datos de rendimiento es una matriz donde cada celda es independiente, pero se podría estimar una celda vacía a partir del promedio de su fila y su columna, o algo más sofisticado que modere ambas dimensiones.
- **Cita** (verbatim): "mi matriz son las celdas, yo para cada celda es independiente y bueno, ya está. Pero bueno, si en realidad yo tengo la media de los rows y las columnas, bueno, podría estimar una celda por el promedio de la row y la columna" `[02:16]`
- **Ambigüedad / tensión**: la idea queda exploratoria; el autor no cierra cómo ponderar filas y columnas ni qué representan exactamente los ejes.

### funciones-de-modelado-como-herramientas-del-sistema
- **Qué**: Las funciones que modelan el tiempo y la precisión de cómputo no son externas al sistema: son herramientas que Luthier mismo utiliza. Es decir, el sistema usa sus propias capacidades de estimación para planificar cómputos.
- **Cita** (verbatim): "empieza a ver funciones que son las funciones de modelado de esto que también las vas a utilizar, o sea la idea es que vos lo utilizas las funciones de estimación de la el tiempo de cómputo de la precisión de cómputo" `[03:05]`

### clases-de-computos-equivalentes
- **Qué**: Muchos cómputos parecidos pertenecerían a una misma clase de cómputos, es decir, tardarían lo mismo para distintos inputs. Lo que habría que encontrar son esas categorías.
- **Cita** (verbatim): "muchos cómputos parecidos pertenecen a la misma misma clase de cómputos, es decir que digamos o sea lo que habría que empezar a encontrar es eso no, las categorías" `[03:34]`

### simplificacion-de-inputs-como-predictores
- **Qué**: El tiempo de cálculo se computaría a partir de una simplificación de los inputs — no los inputs completos sino las características más predictivas (por ejemplo, dimensiones de una matriz). Qué características son relevantes depende de cada caso.
- **Cita** (verbatim): "vos lo que tendrías que tener es vos tenés, digamos, una simplificación de los inputs que ahí vos lo computás. O sea, vos computás el tiempo de cálculo a partir de una simplificación de los inputs." `[04:26]`

### independencia-de-inputs
- **Qué**: Algunas funciones tienen un tiempo de cómputo independiente de los inputs; otras no — y para las que dependen, hay que identificar qué características de los inputs son las más predictivas.
- **Cita** (verbatim): "puede ser que hay funciones que son independientes de los inputs, por ejemplo. Otras, pero cuando dependen de los inputs, obviamente, ahí vos ves qué características de los inputs son las que son los más predictivos." `[04:11]`
