---
source: gemini
key: gemini::20260526T1233
title: "Bueno, como acostumbro, yo pienso todo para ser razonable y después busco la locura. La lo"
started: 2026-05-26T15:33:45Z
ended: 2026-05-26T15:42:22Z
thread: 2026-05-26_20260526T1233_bueno-como-acostumbro-yo-pienso-todo-par.md
thread_sha256: 7bed3c66f22b0b931d52be3e9ac01db7627f14152418361a21ea171a69a41bfc
copy: tracked
turns: 4
windows: 1
window_chars: 60000
ideas: 17
quotes_found: 16/17
generated_by: extract_ideas_dialogue_v1
prompt_sha256: 0954c180c11dae5ddb862a5d39b34f06d21364d490f686f249be18f04f740c22
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### luthier-tipos-como-proposiciones
- **Who**: Luciano
- **Turn**: 1, 2026-05-26 15:33:45 UTC
- **What**: Luthier sería un lenguaje donde los tipos son conceptos, tipos como proposiciones, y los tipos incluyen también funciones y funciones de orden superior.
- **Quote**: "Luthier sería una especie de lenguaje de programación donde los tipos tienen que ser conceptos, o sea, tipos como proposiciones, y los tipos incluyen también funciones, no funciones y funciones de orden superior"

### luthier-pseudo-lenguaje-cross-lenguaje
- **Who**: Luciano
- **Turn**: 1, 2026-05-26 15:33:45 UTC
- **What**: Luthier no sería estrictamente C++ sino un pseudo lenguaje agnóstico, cross-lenguaje más que cross-compiler, implementable en distintos lenguajes, con variantes como py-luthier, R-luthier, C-luthier transformables entre sí.
- **Quote**: "Luthier debería ser como una cosa que es como un lenguaje no es cross compiler sino es directamente cross lenguaje o sea como que ser un poco agn del lenguaje si bien el motor podr estar implementado en alguno de ellos"

### luthier-declarativo-y-optimizador
- **Who**: Luciano
- **Turn**: 1, 2026-05-26 15:33:45 UTC
- **What**: Luthier sería a la vez un lenguaje declarativo y una herramienta de optimización: declarás lo que querés con fórmulas y el motor baraja abiertamente distintas formas de implementarlo.
- **Quote**: "que Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización. O sea, que vos declares lo que querés hacer, que sigan más decir las fórmulas, y después internamente baraja distintas formas de implementar eso, pero eso lo hace abiertamente"

### luthier-paths-con-precision-y-velocidad
- **Who**: Luciano
- **Turn**: 1, 2026-05-26 15:33:45 UTC
- **What**: Una misma función puede implementarse de muchas maneras, los distintos paths, cada uno con su precisión, velocidad y otras propiedades estimadas (memoria, dónde se ejecuta).
- **Quote**: "una funci esta funci puede ser implementada de muchas maneras, son los distintos paths y cada forma tiene una precisión y una velocidad"

### luthier-mapa-declarativo-a-ejecutivo
- **Who**: Luciano
- **Turn**: 1, 2026-05-26 15:33:45 UTC
- **What**: Luthier sería un mapa entre un lenguaje declarativo y uno ejecutivo, donde cada ejecución viene acompañada de una estimación de características como error y, sobre todo, tiempo de cómputo.
- **Quote**: "sería una especie de que Luthier permita digamos, ser un mapa entre un lenguaje declarativo y un lenguaje ejecutivo que ser el que ejecuta las cosas pero a la vez no solamente ejecuta sino que vos para cada ejecuci ten dos cosas ten una estimaci de distintas caracter"

### luthier-mayordomo-orden-superior
- **Who**: Luciano
- **Turn**: 1, 2026-05-26 15:33:45 UTC
- **What**: Luthier como lenguaje de orden superior, una especie de mayordomo que podría incluso compilar lenguajes y permitir expresar en qué lenguaje hacer cada cosa según su complejidad.
- **Quote**: "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo"

### curry-howard-tipos-dependientes
- **Who**: model
- **Turn**: 2, 2026-05-26 15:33:45 UTC
- **Kind**: proposal
- **What**: El modelo nombra la teoría de tipos dependientes y el isomorfismo de Curry-Howard, proponiendo que un tipo establezca una garantía matemática y que el código sea su propia demostración.
- **Quote**: "estás tocando la teoría de tipos dependientes ... Esto permite que el código sea su propia demostración matemática, validando la lógica antes de ejecutar una sola línea de código"
- **Open**: Luciano no responde a este encuadre; queda sin confirmar.

### orquestador-ast-multidimensional
- **Who**: model
- **Turn**: 2, 2026-05-26 15:33:45 UTC
- **Kind**: proposal
- **What**: El modelo propone que Luthier construya un AST y evalúe múltiples caminos en una optimización multidimensional sobre tiempo, precisión, entorno y memoria.
- **Quote**: "Luthier, en cambio, actuaría construyendo un **Árbol de Sintaxis Abstracta (AST)** a partir de tu declaración, para luego evaluar múltiples \"caminos\" (paths) de ejecución"

### desafio-heuristicas-de-estimacion
- **Who**: model
- **Turn**: 2, 2026-05-26 15:33:45 UTC
- **Kind**: proposal
- **What**: El modelo señala que el mayor reto de implementación es construir las heurísticas que anticipen tiempo y memoria de un bloque, vía profiling o modelos predictivos.
- **Quote**: "El mayor reto de Luthier no será la traducción de lenguajes, sino la construcción de las heurísticas de evaluación"

### estimacion-bayesiana-empirica-del-costo
- **Who**: Luciano
- **Turn**: 3, 2026-05-26 15:42:22 UTC
- **What**: La complejidad a priori se estima con una estrategia bayesiana: dar oportunidad a distintos algoritmos para lo mismo e ir estimando los tiempos a partir de la experiencia de correrlos efectivamente.
- **Quote**: "vos obviamente podés, para eso, aplicar, digamos, una estrategia bayesiana ... voy dándole oportunidad a distintos algoritmos para hacer lo mismo, y después voy estimando los tiempos que toman para problemas parecidos, a partir de, digamos, de la experiencia, de correrlos efectivamente"

### base-de-datos-de-mediciones
- **Who**: Luciano
- **Turn**: 3, 2026-05-26 15:42:22 UTC
- **What**: Luthier tendría una base de datos que registra, para cada función con ciertos datos iniciales y escala, con qué algoritmo tardó tanto y tuvo tanta precisión, sabido porque se midió efectivamente.
- **Quote**: "lo que tendr que tener Luthier justamente es una base de datos ... yo para esta funci con estos datos iniciales y esta escala yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión. Y como lo sé, bueno, porque lo corrí, o sea, lo medí, efectivamente"

### generalizar-la-base-de-datos
- **Who**: Luciano
- **Turn**: 3, 2026-05-26 15:42:22 UTC
- **What**: Hay que generalizar los casos puntuales de la base de datos; con una matriz se verían tendencias, estimando una celda por el promedio de su fila y columna o algo más sofisticado. Reconoce no saber aún cómo hacerlo efectivamente.
- **Quote**: "una de las herramientas primeras sería cómo generalizar, digamos, los datos que vas obteniendo con casos puntuales ... ahí estoy un poco en pelotas en el sentido de cómo hacerlo efectivamente"
- **Open**: Cómo generalizar efectivamente la matriz de mediciones queda abierto.

### clases-de-computo
- **Who**: Luciano
- **Turn**: 3, 2026-05-26 15:42:22 UTC
- **What**: Habría que encontrar categorías: así como distintas funciones hacen lo mismo, distintas computaciones tardarían lo mismo para distintos inputs; algunas independientes de los inputs, otras dependientes.
- **Quote**: "distintas computaciones que tardarían lo mismo para distintos inputs ... lo que habr que empezar a encontrar es eso las categor"

### simplificacion-de-los-inputs
- **Who**: Luciano
- **Turn**: 3, 2026-05-26 15:42:22 UTC
- **What**: Se computa el tiempo a partir de una simplificación de los inputs, viendo qué características son las más predictivas, por ejemplo las dimensiones, número de columnas y filas de una matriz.
- **Quote**: "vos computás el tiempo de cálculo a partir de una simplificación de los incómodos, podría ser por ejemplo las dimensiones el número de columnas y rod de una matriz"

### lutearizar-las-funciones-de-estimacion
- **Who**: Luciano
- **Turn**: 3, 2026-05-26 15:42:22 UTC
- **What**: Las propias funciones de estimación de tiempo y precisión también se lutearizan, de modo que no haya que computar cada vez cuánto tarda algo.
- **Quote**: "la idea es que vos lutearizás las funciones de estimación del tiempo de cómputo, de la precisión de cómputo"

### arquitectura-metacircular
- **Who**: model
- **Turn**: 4, 2026-05-26 15:42:22 UTC
- **Kind**: proposal
- **What**: El modelo nombra como metacircular el que las funciones predictivas sean a su vez proposiciones con costo gobernadas por Luthier, que podría elegir en tiempo real un modelo de predicción ligero o uno pesado.
- **Quote**: "Esto convierte a Luthier en un sistema **metacircular**. Las funciones predictivas ... son, en sí mismas, proposiciones con un costo"

### surrogate-models-y-proceso-gaussiano
- **Who**: model
- **Turn**: 4, 2026-05-26 15:42:22 UTC
- **Kind**: proposal
- **What**: El modelo encuadra la estimación por promedio de filas y columnas como un paso hacia regresión por Proceso Gaussiano con modelos sustitutos que devuelven media y varianza, guiando exploración vs explotación.
- **Quote**: "Tu idea de estimar el valor de una celda en base al promedio de sus filas y columnas es el primer paso hacia un **Proceso Gaussiano (Gaussian Process Regression)**"
- **Open**: Luciano no responde; queda sin confirmar.
