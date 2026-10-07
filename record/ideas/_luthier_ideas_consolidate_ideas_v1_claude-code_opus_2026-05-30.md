---
fuentes: 31
ecosistemas: 10
ideas: 22
generado_por: consolidate_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

# Ideas de diseño de Luthier

## fundamentos-formales — Qué teoría sustenta el lenguaje y cómo se adapta

Las decisiones sobre qué matemática funda Luthier: HoTT como base, su extensión probabilística, y los problemas que esa elección abre.

### matrimonio-hott-bayes
- **Qué**: Luthier debería ser una fusión de Homotopy Type Theory e inferencia bayesiana. HoTT provee el espacio de tipos y equivalencias; Bayes aporta la dimensión probabilística. Las equivalencias mismas serían probabilísticas.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Fusionar dos marcos formales que casi nadie conecta — uno sobre estructura, otro sobre incertidumbre — en un solo lenguaje de programación. Si funciona, cambia la noción misma de qué significa que dos implementaciones sean "iguales". Activa **conceptual** (reorganiza qué es equivalencia), **estética** (economía al unificar dos mundos), **ética** (la incertidumbre no es un add-on sino constitutiva).
- **Material clave** (verbatim):
  - "Para mí tiene que ser una especie de matrimonio entre Homeotopy Type Theory y Valles" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[02:40]`)
  - "la idea mía es de alguna manera que las probabilidades y los tipos vayan casi a la par. O sea que las equivialencias sean de alguna manera probabilísticas." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:40]`)
  - "tendría que ser, digamos, una especie de extensión probabilística de homeotopy type theory para que funcione, ¿no? O sea, que no es que vos tenés una verdad, digamos, lógica, sino que también podés hacer una inferencia estadística de que algo funciona de alguna manera" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[02:09]`)
  - "Son Metrópita y Teori te dan los puntos del espacio, los conjuntos donde aplicas las probabilidades. Sería una cosa así." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[02:16]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[02:09]`, `[02:40]`; `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:40]`, `[02:16]`
- **Tensión / pregunta abierta**: El autor reconoce que "esto es un poco difícil de pensar". No existe un mecanismo formal que integre probabilidades en HoTT; queda como aspiración fundacional sin camino técnico trazado.

### mapeo-a-hott
- **Qué**: Luthier mapearía estrictamente los elementos de HoTT, usándola como fundamento formal. Los tipos son proposiciones; las funciones son tipos; los paths expresan equivalencia entre implementaciones.
- **Tipo**: plántula
- **Infectabilidad**: Media-alta. Es la decisión arquitectónica más estructurante del lenguaje, pero como idea es más una adopción de un marco existente que una invención. Activa **conceptual** (HoTT como base de un lenguaje de programación práctico es inusual) y **estética** (la correspondencia tipos-como-proposiciones tiene belleza propia).
- **Material clave** (verbatim):
  - "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen también funciones, funciones y funciones de orden superior" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[00:38]`)
  - "podría tratar de hacer que Luthier, ya que es un lenguaje en sí mismo, mape estrictamente los elementos de la monotópica" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:02]`)
  - "El secreto para que el UTIER funcione es que tiene que tener muy pocos tipos, pero tienen que seguir muy claramente ciertas reglas bastante bien pensadas" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:00]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[00:38]`; `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:02]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:00]`; `WhatsApp Ptt 2026-05-29 at 14.06.25.mp3` `[00:00]`
- **Tensión / pregunta abierta**: HoTT no conceptualiza qué es un programa, no trabaja nativamente con probabilidades, y el modelado de una secuencia de statements no es claro dentro de ella. El autor identifica estos tres déficits explícitamente.

### hott-sin-programa-ni-probabilidades
- **Qué**: Dos déficits identificados en HoTT como base: (1) no tiene un concepto de programa (sí de función y tipo, pero no de un conjunto de expresiones que constituya un programa completo); (2) no trabaja nativamente con probabilidades.
- **Tipo**: tensión abierta
- **Infectabilidad**: Media. Es una observación técnica precisa que condiciona todo el diseño, pero no tiene la fuerza de una propuesta. Activa **conceptual** (señala un hueco que obliga a inventar).
- **Material clave** (verbatim):
  - "Homo etopitae teori no conceptualiza, digamos, un conjunto de expresiones de Homo etopitae teori, o sea, lo que sería un programa, no hay un concepto, hay un concepto de función, de tipos, pero de programa no me queda muy claro que esté, eso es uno de los defectos." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[00:41]`)
  - "Vos tenés un programa que es una serie de statements que son todos modelables por geometría de Taitieri, pero el programa en sí, en principio no tan claramente" (`WhatsApp Ptt 2026-05-29 at 14.37.14.mp3` `[00:25]`)
  - "el otro tema es que no trabaja sobre probabilidades, pero las probabilidades se podrían construir dentro de idioma utópita y teoría." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:32]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[00:41]`, `[01:32]`; `WhatsApp Ptt 2026-05-29 at 14.37.14.mp3` `[00:25]`, `[00:37]`

## equivalencia-y-paths — El concepto central: caminos equivalentes entre implementaciones

La idea motriz de Luthier es que existen múltiples caminos (paths) para hacer lo mismo, y el lenguaje permite expresar, verificar y comparar esos caminos.

### paths-como-equivalencia-de-implementaciones
- **Qué**: Una función puede tener múltiples implementaciones (paths). Los paths de HoTT se usan para abstraer el concepto de implementación: distintas implementaciones se vinculan a través de paths que expresan equivalencia. Este es el concepto fundamental de Luthier.
- **Tipo**: plántula
- **Infectabilidad**: Muy alta. "Implementación" deja de ser una decisión opaca del programador y pasa a ser un objeto formal del lenguaje, comparable, verificable, intercambiable. Quien programa ya no elige una implementación y descarta las demás: las mantiene todas como caminos equivalentes en un espacio. Activa **conceptual** (reorganiza qué significa implementar), **estética** (la elegancia de que implementaciones distintas sean puntos del mismo espacio), **emotiva** (es la idea que más entusiasmo genera en el autor).
- **Material clave** (verbatim):
  - "tiene una función, esta función puede ser implementada de muchas maneras, son los distintos paths y cada forma tiene una precisión y una velocidad" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:26]`)
  - "abstraemos el concepto de implementación a través de los paths… yo tengo distintas implementaciones y veo la equivalencia entre implementaciones" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:18]`)
  - "el concepto fundamental es el de la equivalencia de PATH, de que los PATH sean equivalentes, que eso es lo más difícil" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:38]`)
  - "vos comparás dos caminos para hacer lo mismo" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:44]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:26]`; `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:18]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:38]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:44]`; `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:03]`
- **Tensión / pregunta abierta**: Demostrar equivalencia de paths es "lo más difícil". Requiere un demostrador interno y/o verificación empírica. La idea queda formulada como intuición sin desarrollo del mecanismo de prueba.

### niveles-de-equivalencia
- **Qué**: No hay una sola equivalencia sino distintos niveles — isomorfismo, igualdad exacta, misma ubicación en memoria, etc. — cada uno definido por un functor de equivalencia diferente. Esto permite separar lo esencial (lo equivalente) de la decoración (eficiencia, costo).
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. La idea de que "igual" no es binario sino un espectro formal de equivalencias, y que cada nivel revela una capa distinta de la computación, es poderosa. Activa **conceptual** (reorganiza qué significa igualdad en programación) y **estética** (la elegancia de un espectro de equivalencias parametrizado por functores).
- **Material clave** (verbatim):
  - "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[02:56]`)
  - "si vos tenés funciones que son equivalentes, después podés ver las cosas que no son equivalentes, que es, por ejemplo, los que son las decoraciones, que es la eficiencia, por ejemplo, el costo, lo que sea" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[03:18]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[02:56]`, `[03:18]`

### verificabilidad-y-demostrador
- **Qué**: Luthier necesita poder comprobar que una función es correcta. Para demostrar equivalencia de paths, tiene que tener internamente un demostrador (proof system), más una extensión empírica/estadística.
- **Tipo**: semilla latente
- **Infectabilidad**: Media. La idea de un demostrador interno es conocida (Coq, Lean), pero la combinación con demostración empírica/estadística es original. Activa **conceptual** (fusión de demostración formal y empírica).
- **Material clave** (verbatim):
  - "comprobas que una función es correcta, es la idea de verificabilidad, es como una especie de verificabilidad" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:52]`)
  - "como lo demostrás matemáticamente, tiene que ser internamente tener un demostrador" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:50]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:52]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:50]`, `[02:09]`

## explicitacion-sobre-ejecucion — Luthier como lenguaje de descripción antes que de ejecución

La postura de que el acto central no es ejecutar sino explicitar: describir el problema, las funciones, las condiciones, las equivalencias. La ejecución es verificación, no el fin.

### explicitar-antes-de-ejecutar
- **Qué**: Luthier ejecuta, pero el énfasis está en la explicitación — la descripción del problema, de las funciones, de las condiciones. La ejecución consiste en verificar equivalencias. Primero se expresan las ideas (con lápiz y papel), después se va a la ejecución.
- **Tipo**: plántula
- **Infectabilidad**: Muy alta. Invierte la jerarquía habitual: un lenguaje de programación no es una máquina de correr código sino un medio de pensamiento. "Si está bien escrito, debería poder ejecutarse a mano, con lápiz y papel." Eso cambia la relación del programador con su herramienta. Activa **ética** (postura sobre qué debe ser programar), **emotiva** (contacto con el deseo del autor: un lenguaje para pensar), **estética** (la elegancia de que la ejecución sea verificación, no cómputo bruto), **conceptual** (redefine qué es ejecutar).
- **Material clave** (verbatim):
  - "lo más importante no es la ejecución, sino la explicitación, la descripción del problema" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:11]`)
  - "la ejecución en Luthier sería esa verificación de equivalencias, o sea que sí ocurre, claramente, pero el énfasis en principio está puesto en la explicitación de esas equivalencias" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:55]`)
  - "si está bien escrito, Luthier tendría que ser ejecutable a mano, es decir, que uno pudiese con lápiz y papel escribir las cosas" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:13]`)
  - "la primera etapa de Luthier tiene que ser como una especie de lenguaje de descripción, descripción del problema, descripción de las funciones, descripción de las condiciones de las funciones" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:20]`)
  - "La idea básica es que vos puedas expresar las ideas con lápiz y papel y después es que vayas." (`WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:38]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:11]`, `[01:20]`, `[01:55]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:13]`; `WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:14]`, `[00:30]`, `[00:38]`

### expresividad-como-valor-primero
- **Qué**: Lo importante es que el lenguaje sea expresivo — que permita formular distintas alternativas, incluso para descartarlas. Expresar algo inútil tiene valor: permite descartar sin dudar. Primero expresar bien, después elegir los aciertos.
- **Tipo**: plántula
- **Infectabilidad**: Alta. "Aunque el uso sea convencerte de que no sirva para nada. Por lo menos no dudar." La idea de que un lenguaje vale por lo que te permite descartar tanto como por lo que te permite construir es infrecuente y poderosa. Activa **ética** (cómo se debe programar: formulando antes de optimizando), **emotiva** (la seguridad de poder eliminar sin dudar), **estética** (la limpieza de un diseño que incluye su propia basura para poder tirarla).
- **Material clave** (verbatim):
  - "en realidad no es que uno tiene que obligatoriamente hacer todo sino tener las herramientas para expresar distintas alternativas. Eso es lo importante. Que sea expresivo el lenguaje." (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:20]`)
  - "Aunque el uso sea convencerte de que no sirva para nada. Por lo menos no dudar." (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:45]`)
  - "lo primero que uno puede hacer es ver cómo expresarlo bien, después, una vez que vos lo expresás, podés expresar los aciertos y los errores y bueno, después elegís los aciertos" (`WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[01:19]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:20]`, `[01:45]`; `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[01:19]`; `WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[02:36]`, `[03:26]`

### funciones-por-propiedades
- **Qué**: Definir funciones no solo operativamente sino desde el punto de vista de sus propiedades — la proposición acerca de sus inputs y outputs. Tener ambas caras: la operativa y la declarativa.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Separar "qué hace" de "qué cumple" en la definición de toda función es una idea que existe en la verificación formal pero rara vez es nativa del lenguaje. Activa **conceptual** (doble cara de una función) y **ética** (las propiedades no son documentación: son parte de la definición).
- **Material clave** (verbatim):
  - "definición de función desde el punto de vista de las propiedades, no operativamente, o sea, o tener las dos funciones, ¿no? operativamente y las propiedades que contienen, la proposición acerca de sus inputs y outputs" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[03:42]`)
  - "de qué manera ya uno tiene unívocamente determinado que es una implementación, que lo que vos estás haciendo es una implementación de las matrices" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[02:02]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[02:02]`, `[03:42]`

## minimalismo-y-autoextension — Cuánto hay adentro y cuánto se construye desde adentro

La tensión entre tener el mínimo de primitivas y poder construir todo lo demás desde ellas, incluyendo el lenguaje mismo.

### minimalismo-radical
- **Qué**: Luthier debe tener los mínimos componentes nativos posibles. Se reduce a tipos y funciones (las funciones son de un tipo). Inspiración en Lisp (todo son listas). Los elementos básicos se definen al estilo de teoría de categorías.
- **Tipo**: plántula
- **Infectabilidad**: Alta. El minimalismo no es austeridad sino potencia: pocos elementos fundantes → edificio enorme. La formulación "solamente hay tipos y hay funciones, pero funciones son de un tipo" tiene una economía conceptual que pega. Activa **estética** (elegancia de la reducción), **conceptual** (todo se deriva de casi nada).
- **Material clave** (verbatim):
  - "yo lo que querría es que Luthier sea mínimo, o sea, que tenga los mínimos componentes nativos posibles" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[03:22]`)
  - "solamente hay tipos y hay funciones, pero funciones son de un tipo" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[02:31]`)
  - "El minimalismo está en los componentes fundantes y después a partir de esos componentes fundantes vos construís un edificio enorme" (`WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:12]`)
  - "en Lisp creo que son todas listas" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[02:08]`)
  - "vamos a tratar de reducir todo a un mínimo, pero sí, queremos tener todos esos conceptos complejos que figuran ahí, pero basados en que los elementos mínimos sean pocos" (`WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[01:04]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[02:43]`, `[03:22]`; `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[02:08]`, `[02:31]`; `WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:12]`, `[00:25]`, `[00:40]`, `[00:56]`, `[01:04]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:00]`
- **Tensión / pregunta abierta**: Qué primitivas exactamente: ¿identidad sola? ¿tipos dependientes? ¿equivalencia? El autor duda explícitamente y no cierra.

### autoextensibilidad-y-meta-recursividad
- **Qué**: Luthier debe ser completamente autoextensible (se puede escribir Luthier en Luthier) y meta-recursivo (su objeto es trabajar sobre sí mismo). El código de Luthier es el primer elemento de Luthier. Las reglas se pueden optimizar para que la manipulación de programas sea fácil, dado que es un lenguaje inventado.
- **Tipo**: plántula
- **Infectabilidad**: Muy alta. "El código es el primer elemento." No es que haya código y luego, como extensión, meta-programación: el código como objeto manipulable es constitutivo del lenguaje desde el día cero. Distinto de Lisp, donde la homoiconicidad fue "implantada después". Activa **conceptual** (el lenguaje se contiene a sí mismo como objeto), **ética** (no hay ciudadanos de segunda clase: el código es dato desde el inicio), **emotiva** (el entusiasmo de diseñar un universo auto-contenido).
- **Material clave** (verbatim):
  - "tiene que ser completamente extensible, autoextensible, es decir, que vos puedas escribir como en Luthier, todo lo de Luthier, básicamente, cosa que al final solamente termines implementando algunas cosas" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:26]`)
  - "Luthier, el objeto de Luthier es trabajar sobre Luthier. O sea, que sea meta recursivo es fundamental." (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:07]`)
  - "Luthier tiene que operar sobre Luthier también, o sea, tiene que haber una meta, meta uso, desde el vamos, como en LISP que medio que se implantó después. O sea, hay que pensar que Luthier tiene que ser, que el código de Luthier sea un elemento de Luthier ya también desde el vamos. O sea, el código es el primer elemento." (`WhatsApp Ptt 2026-05-29 at 14.36.03.mp3` `[02:16]`)
  - "dado que es un lenguaje que yo invento, digamos, sigue las reglas que yo quiero, entonces puedo optimizar las reglas para que eso sea fácil." (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:26]`)
  - "si es tipo una función, entonces una cosa que puede hacer un programa de Luthier es trabajar sobre otro programa de Luthier" (`WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:38]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:26]`, `[00:48]`; `WhatsApp Ptt 2026-05-29 at 14.36.03.mp3` `[01:56]`, `[02:16]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:07]`, `[00:26]`; `WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:38]`, `[00:54]`; `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:19]`
- **Tensión / pregunta abierta**: La auto-referencia plena (un programa que trabaja sobre sí mismo) queda como "pregunta interesante" no resuelta.

## programa-como-dag — La estructura estática de un programa Luthier

Cómo se modela un programa: DAG de definiciones, conmutatividad de statements, temporalidad como dependencia.

### conmutatividad-y-dag
- **Qué**: Los statements en Luthier son conmutativos: el orden textual no altera la semántica. Un programa se modela como un DAG (grafo dirigido acíclico) de definiciones. La temporalidad se reconstruye a partir de la causalidad (dependencia de tipos), no de la secuencia de escritura. El código no se ejecuta hasta que no está completamente definido.
- **Tipo**: plántula
- **Infectabilidad**: Alta. "La temporalidad se reconstruye a partir de la causalidad." Esto libera al programador del orden secuencial y lo fuerza a pensar en dependencias, no en pasos. Activa **conceptual** (el tiempo no es orden textual sino dependencia), **estética** (un programa como grafo, no como lista), **ética** (el lenguaje no te impone un orden arbitrario).
- **Material clave** (verbatim):
  - "la pregunta de la conmutatividad de statements es sí, sí habría conmutatividad de statements, o sea, la idea es que sí" (`WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:00]`)
  - "estoy inclinado a que sí y que sí, tomaríamos el modelo de los DAGs, que digamos como que sería un DAG, básicamente" (`WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:07]`)
  - "la temporalidad se da a lo PERL a partir de la dependencia de tipos. Lo que ocurre mañana depende de lo que ocurrió hoy. O sea que hay una dependencia causal. La temporalidad se reconstruye a partir de la causalidad." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:00]`)
  - "vos no ejecutás el código hasta que no está definido. Entonces es como que, digamos, vos podés tener un montón de código muerto que no jode a nadie porque no está completamente definido." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:53]`)
  - "que sea conmutativo en los statements, que el orden en los statements no altera el resultado, eso simplificaría mucho la composición y la manipulación de programas." (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:35]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.36.03.mp3` `[00:00]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:35]`, `[01:26]`, `[01:48]`; `WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:00]`, `[00:53]`; `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:00]`, `[00:07]`
- **Tensión / pregunta abierta**: Conmutatividad quita expresividad. DAG sobre DAGs (programas que transforman programas) queda enunciado pero no desarrollado. Qué significa exactamente "definido" (para la regla de no-ejecución) queda sin precisar.

### dag-sobre-dags
- **Qué**: Más allá del DAG estático de un programa, se puede tener un DAG que opera sobre DAGs — programas que manipulan programas, usando instrucciones de sí mismos.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Conecta la meta-recursividad con la estructura formal del DAG. Activa **conceptual** (programas como objetos algebraicos manipulables por otros programas del mismo tipo).
- **Material clave** (verbatim):
  - "vos podés tener en realidad un DAG que opera sobre DAGs, que opera sobre programas [...] pero vos lo podés tomar como un DAG estático, que después, claro, hay algo que opera sobre ese DAG y después se transforma en otra cosa con instrucciones de sí mismo" (`WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:19]`)
  - "si vos declaras dos veces un tipo, podés hacer un producto cartesiano de alguna manera, o sea que corra de dos maneras" (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[01:10]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:19]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[01:10]`; `WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[01:38]`

## olvido-y-simplificacion — El problema de la acumulación de información de tipado

Cómo manejar el crecimiento descontrolado de la información de tipo que se acumula al componer funciones con tipos dependientes.

### functores-de-olvido
- **Qué**: La composición de funciones con tipos dependientes acumula información de tipado hasta volverse monstruosa. La solución son functores de olvido: funciones no invertibles que descartan información selectivamente, manteniendo el tipo acotado. La elección de qué functor de olvido aplicar define el lenguaje que se está hablando. Son identificados como "uno de los componentes más importantes de Luthier".
- **Tipo**: semilla latente
- **Infectabilidad**: Muy alta. El "olvido" como operación constitutiva del lenguaje — no un bug sino una feature, no una pérdida sino una herramienta formal. "Luthier como contador obsesivo" que necesita aprender a olvidar. La idea de que olvidar es tan importante como recordar, y que diferentes formas de olvidar generan diferentes lenguajes, es profundamente original. Activa **conceptual** (el olvido como operación algebraica, no como pérdida), **estética** (la belleza de los diagramas conmutativos donde olvido y computación conmutan), **emotiva** (la imagen del "contador obsesivo" y el "resumen más grande que el texto"), **ética** (no toda información merece ser arrastrada).
- **Material clave** (verbatim):
  - "si Luthier es como una especie de contador obsesivo que registra cada una de las operaciones que vos haces, claro, puede ser que de repente, digamos, lo que es el decorado se vuelva muchísimo más grande que el valor que está siendo decorado" (`WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[00:36]`)
  - "tenés ahí los problemas del olvido, que tiene que ser uno de los problemas fundamentales de Luthier que tiene que solucionar" (`WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[00:24]`)
  - "los functores de olvido serían, digamos, uno de los componentes más importantes de Luthier en cuanto a la implementación y en cuanto a todo, ¿no?" (`WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[02:29]`)
  - "algún tipo de álgebra de tipado que sea un álgebra simplificadora, o sea, que no sea un monoide libre, básicamente" (`WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[01:06]`)
  - "si haces olvido compuesto con la serie de funciones, es lo mismo que serie de funciones y después olvido, ¿no? Eso tendría que ser, digamos, que conmute, que eso sea igual" (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[00:39]`)
  - "las distintas funciones de olvido de los tipos van a optimizar distintas cosas" (`WhatsApp Ptt 2026-05-29 at 15.00.11.mp3` `[00:00]`)
  - "a veces es que el resumen es más grande que el texto [...] como hay más interpretaciones de los libros de Borges que los libros de Borges en sí" (`WhatsApp Ptt 2026-05-27 at 13.51.41.mp3` `[00:12]`)
  - "Una media es como una especie de funtor de olvido, si se quiere" (`WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:40]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[00:08]`, `[00:24]`, `[00:36]`, `[01:06]`, `[02:19]`; `WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[00:09]`, `[01:27]`, `[01:51]`, `[02:29]`; `WhatsApp Ptt 2026-05-29 at 15.00.11.mp3` `[00:00]`, `[00:07]`, `[00:16]`; `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[00:00]`, `[00:39]`; `WhatsApp Ptt 2026-05-27 at 13.51.41.mp3` `[00:12]`; `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:40]`, `[00:56]`
- **Tensión / pregunta abierta**: Queda completamente abierto qué functores de olvido aplicar, cómo elegirlos, y cuáles son sus propiedades. El autor lo marca explícitamente: "Eso hay que seguir pensándolo."

### tipos-como-historia-de-composicion
- **Qué**: El tipo de un valor puede registrar la historia de funciones aplicadas. En un loop, el tipo queda como una combinación elevada a una potencia. Si las funciones son asociativas, se pueden encontrar patrones que simplifican esa historia.
- **Tipo**: semilla latente
- **Infectabilidad**: Media. Es un mecanismo técnico interesante pero derivado de la idea de functores de olvido. Activa **conceptual** (el tipo como traza algebraica del cómputo).
- **Material clave** (verbatim):
  - "el tipo te puede quedar expresado así que se yo como una combinación de tipos con una potencia y listo y eso te da una idea del tipo que es entonces ahí lo que tenés en el tipo es la historia de cómo llegaste hasta ahí" (`WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:27]`)
  - "si las funciones son todas asociativas son digamos los funciones son asociativos entonces vos encontrás un patrón por ejemplo si vos tenés un algoritmo que tiene que repite un loop va a ser una serie de funciones y después a una potencia" (`WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:04]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:04]`, `[01:27]`, `[01:51]`

## mayordomo-cross-lenguaje — Luthier como orquestador de otros lenguajes

Luthier no ejecuta directamente: coordina, compone, delega a programas y lenguajes externos.

### luthier-como-mayordomo-puente
- **Qué**: Luthier es un "mayordomo" — un lenguaje de orden superior que orquesta otros lenguajes. Es un "lenguaje puente" entre otros lenguajes. No es cross-compiler sino cross-lenguaje: agnóstico del lenguaje de implementación. Puede componer la entrada y salida de un programa con otro.
- **Tipo**: plántula
- **Infectabilidad**: Alta. La metáfora del mayordomo es precisa: no hace el trabajo, pero sabe qué hacer y a quién delegarle. Un lenguaje que no compite con otros lenguajes sino que los contiene y conecta. Activa **conceptual** (cambio de nivel: un lenguaje sobre lenguajes), **emotiva** (la imagen del mayordomo es evocadora y clara), **ética** (no reinventar la rueda, delegar con elegancia).
- **Material clave** (verbatim):
  - "me lo imagino como un mayordomo que puede correr básicamente cualquier programa y que puede comparar los outputs" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:00]`)
  - "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[03:34]`)
  - "que básicamente sea así, un lenguaje puente, ¿no? Lenguaje puente entre otros lenguajes" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[03:33]`)
  - "luthier debería ser como una cosa que es como un lenguaje no es cross compiler sino directamente cross lenguaje o sea como que sería un poco agnóstico del lenguaje" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[04:24]`)
  - "Luthier lo que tendría que hacer es poder componer la entrada y salida de un programa y otro" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:26]`)
  - "el UTIER tiene que poder secuestrar código de cualquier otro lenguaje" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:48]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[03:34]`, `[04:24]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:00]`, `[00:26]`, `[03:33]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:48]`
- **Tensión / pregunta abierta**: Queda sin definir cómo se logra concretamente la transformación entre implementaciones en distintos lenguajes (PyLuthier ↔ RLuthier ↔ CLuthier).

### core-cerrado-y-exterior
- **Qué**: Luthier se estructura como un core cerrado ("todos sus tipos perfectos") que observa el universo exterior. Todo lo externo (C++, Python, la computadora, cualquier recurso) es conceptualmente un "elemento externo". Librerías manejan la interfaz. La comunicación es un ciclo read-write: convertir Luthier en código ejecutable y datos externos en Luthier.
- **Tipo**: semilla latente
- **Infectabilidad**: Media. La imagen de Luthier como observador cerrado del universo tiene fuerza poética pero queda vaga operativamente. Activa **estética** (la pureza de un sistema cerrado que mira hacia afuera) y **conceptual** (la frontera lenguaje/mundo como interfaz explícita).
- **Material clave** (verbatim):
  - "yo lo estoy pensando como un observador y del universo, o sea, Luthier sería cerrado, como que tiene todos sus tipos así perfectos" (`WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[01:11]`)
  - "C++ o un programa de Python o la computadora o cualquier recurso no es un elemento de Luthier, es como un elemento externo" (`WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[00:37]`)
  - "convertís un código de Luthier en un código ejecutable en C o en qué sé yo, lo que sea, y a la vez vos también leés files o leés algo y lo convertís en Luthier también, ¿no? O sea, sería como un read-write" (`WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[01:21]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[00:00]`, `[00:37]`, `[01:11]`, `[01:21]`; `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[03:48]`, `[04:07]`, `[05:49]`
- **Tensión / pregunta abierta**: No se resuelve cómo se modela el "elemento externo" ni si la interfaz es compilación, I/O, o algo distinto.

## declarativo-mas-optimizacion — Luthier como herramienta de optimización transparente

La idea de que se declara qué se quiere hacer y el sistema explora implementaciones con distintos costos.

### declarativo-que-baraja-implementaciones
- **Qué**: Luthier como mapa entre un lenguaje declarativo y un lenguaje ejecutivo. Se declara lo que se quiere hacer; internamente se barajan distintas formas de implementarlo, cada path con su precisión, velocidad, memoria, hardware de ejecución.
- **Tipo**: plántula
- **Infectabilidad**: Media-alta. La idea existe en compiladores optimizadores y autotuners, pero hacer del barajado explícito y transparente una propiedad del lenguaje (no del compilador) es distintivo. Activa **conceptual** (la optimización no es un paso oculto sino parte del lenguaje), **ética** (transparencia: el sistema no decide por vos en secreto).
- **Material clave** (verbatim):
  - "que el Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización. O sea, que vos declares lo que querés hacer, que sigan las fórmulas, y después internamente baraja distintas formas de implementar eso, pero eso lo hace abiertamente" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:52]`)
  - "que Luthier permita, digamos, ser un mapa entre un lenguaje declarativo y un lenguaje ejecutivo que sería el que ejecuta las cosas" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[02:51]`)
  - "para cada path de ejecución tenés dos cosas. Tenés una estimación de distintas características, que es, por ejemplo, eso, el error y más que nada el tiempo de cómputo, pero también puede ser, qué sé yo, la memoria, también podría ser donde lo haces, si lo haces en un clúster, lo haces en una computadora" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[03:10]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:52]`, `[02:51]`, `[03:10]`, `[05:28]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[01:04]`

### estimacion-bayesiana-de-rendimiento
- **Qué**: Para evaluar la complejidad a priori de distintos cómputos, Luthier mantendría una base de datos que registra empíricamente tiempos, precisión, memoria de cada ejecución, y generalizaría esos datos con estimación bayesiana. Las funciones de estimación mismas son herramientas de Luthier.
- **Tipo**: semilla latente
- **Infectabilidad**: Media. Es una idea de ingeniería sofisticada (autotuning con base empírica) pero menos fundacional que las ideas de equivalencia o olvido. Activa **conceptual** (el lenguaje aprende de su propia ejecución).
- **Material clave** (verbatim):
  - "puede ser cualquiera y bueno, voy dándole oportunidad a distintos algoritmos para hacer lo mismo y después voy estimando los tiempos que toman para problemas parecidos a partir de la experiencia, de correrlos efectivamente" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[00:28]`)
  - "para esta función, con estos datos iniciales, y esta escala, yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión, y como lo sé, bueno, pues lo corrí, o sea, lo medí, efectivamente" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[01:21]`)
  - "Luthier es una base de datos acerca de cómo, de los programas, de cada vez que corren es como que generas un output acerca de cómo corrió" (`WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:00]`)
  - "empieza a ver funciones que son las funciones de modelado de esto que también las vas a utilizar, o sea la idea es que vos lo utilizas las funciones de estimación de la el tiempo de cómputo de la precisión de cómputo" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[03:05]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[00:28]`, `[01:21]`, `[01:42]`, `[02:16]`, `[03:05]`, `[03:34]`, `[04:11]`, `[04:26]`; `WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:00]`, `[00:32]`
- **Tensión / pregunta abierta**: Cómo generalizar mediciones puntuales a tendencias (el autor dice "estoy un poco en pelotas"). Cómo sintetizar la información acumulada sin que se vuelva "monstruosa". Exploración vs. explotación no definida.

## capas-del-lenguaje — La arquitectura en capas de Luthier

Distinción entre capas del lenguaje: una primera de equivalencias y verificabilidad, una segunda de tiempo, complejidad, recursos.

### dos-capas
- **Qué**: Primera capa: equivalencias y verificabilidad. Segunda capa: tiempo, complejidad, recursos, éxito/fracaso. La primera capa es la explicitación; la segunda es la decoración con propiedades de ejecución.
- **Tipo**: semilla latente
- **Infectabilidad**: Media. Es una decisión arquitectónica sensata pero menos sorprendente que otras ideas. Activa **conceptual** (separar esencia de accidentes) y **estética** (la limpieza de la separación).
- **Material clave** (verbatim):
  - "Pero eso me parece que es como de la segunda capa. La primera capa sería, bueno, eso." (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[04:18]`)
  - "después poder determinar los tiempos que tardan en ejecutarse algo y que dos caminos son equivalentes con distintos recorridos" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[01:04]`)
  - "Vos podés ejecutarlo con la pici papel y mirar una base de datos con cuidado o que alguien te diga de la base de datos cuál es el resultado. Podés expresarlo con lápiz y papel." (`WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:14]`)
  - "Pero sí, son dos capas, dos momentos. Y no es que uno sea una aspiración de la concesión." (`WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:30]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[01:04]`, `[04:08]`, `[04:18]`; `WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:14]`, `[00:30]`

### funciones-no-univocas-y-error-como-primitiva
- **Qué**: Modelar funciones no unívocas (con error, muestras, probabilidades) desde el lenguaje mismo, no como añadido. Decoradores para representar error y su propagación. La composición de errores debe expresar propiedades algebraicas (asociatividad, conmutatividad).
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. La idea de que el error no es un accidente sino una propiedad algebraica de las funciones, componible y verificable, es potente para la práctica científica. Activa **conceptual** (el error deja de ser ruido y se vuelve estructura), **ética** (no esconder la incertidumbre).
- **Material clave** (verbatim):
  - "que uno pueda modelar, desde el vamos, funciones no unívocas, que serían funciones con error, o sea, samples, o sea, muestras, quizás que estén ya desde el lenguaje" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[04:30]`)
  - "cómo, digamos, uno en Luthier puede hacer decoradores fáciles, ¿no? por ejemplo eso, el error de un número" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[03:05]`)
  - "si la operación de un decorador sobre el otro decorador, por ejemplo, si cumple la asociatividad, por ejemplo, o no, o si cumple [...] la conmutatividad" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[05:18]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[03:05]`, `[04:30]`, `[05:18]`; `WhatsApp Ptt 2026-05-30 at 18.15.07.mp3` `[01:31]`

## analogia-fundante — La metáfora que da horizonte al proyecto

### inventar-un-universo
- **Qué**: Inventar un lenguaje de programación es como inventar un universo. Las categorías gramaticales de los lenguajes naturales sirven de paralelo para pensar qué primitivas necesita el lenguaje.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Es la frase que abre el espacio de juego. No es una decisión técnica sino una postura que permite que todas las demás decisiones sean ambiciosas. Activa **emotiva** (el deseo de inventar un universo es lo que mueve todo el proyecto), **conceptual** (un lenguaje no es una herramienta sino un mundo).
- **Material clave** (verbatim):
  - "inventar un lenguaje es como inventar un universo" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[00:02]`)
  - "En lenguajes hay sustantivos, verbos, adjetivos, adverbios y proposiciones. En C++ hay clases, funciones." (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[00:10]`)
  - "la idea de Luthier es expresar invarianzas de las disciplinas" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[00:58]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[00:02]`, `[00:10]`; `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[00:58]`
