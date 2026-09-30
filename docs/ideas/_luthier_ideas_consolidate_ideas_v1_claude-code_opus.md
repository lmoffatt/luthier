---
fuentes: 42
ecosistemas: 11
ideas: 44
generado_por: consolidate_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

# Ideas de diseño de Luthier

Nota de editor. Consolidé el corpus completo agrupando por convivencia, no por término. Dejé afuera, por selectividad, el material que el propio extractor marcó como aparentemente fuera de alcance (economía de datos: `plataforma-donde-compartir-hace-valer-mas`, `informacion-correlacionada-vale-mas`, `minima-reciprocidad-por-posicion-relativa`) y los callejones puramente instrumentales (organización de la clase de Gaussian-Newton, `descomposición-funcional-de-luthier`, `luthier-y-algebra-abstracta` como intuición desnuda). De ese material rescaté solo lo que alimenta una idea canónica (p. ej. "código como datos"), citado donde corresponde.

## vision-fundante — Qué es Luthier y para qué se lo inventa

La postura de arranque: qué clase de cosa es Luthier, con qué ambición se lo construye y a quién sirve. Es el marco donde el resto cobra sentido.

### inventar-lenguaje-como-inventar-universo
- **Qué**: Inventar un lenguaje de programación es como inventar un universo; como el lenguaje es propio, las reglas se eligen y se optimizan para lo que uno quiere.
- **Tipo**: semilla latente
- **Infectabilidad**: Altísima. Reencuadra el diseño de un lenguaje como cosmogonía y funda el permiso para todo lo demás (elegir reglas, cerrar el mundo, autooperar). Una frase que se queda pegada. Ejes: estética, emotiva, conceptual.
- **Material clave** (verbatim):
  - "inventar un lenguaje es como inventar un universo" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[00:02]`)
  - "dado que es un lenguaje que yo invento, digamos, sigue las reglas que yo quiero, entonces puedo optimizar las reglas para que eso sea fácil." (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:26]`)
  - "normalmente no se puede, pero en principio, dado que es nuestro propio universo, podríamos hacer que Luthier trabaje sobre sí mismo. Es una pregunta interesante." (`WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:54]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[00:02]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:26]`; `WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:54]`

### cita-von-neumann-como-epigrafe
- **Qué**: El epígrafe fundacional: si definís con precisión qué es algo, se puede construir una máquina que lo haga.
- **Tipo**: semilla latente
- **Infectabilidad**: Muy alta como divisa. Convierte "definir bien" en el trabajo central de la programación y ata la ambición filosófica a un criterio operativo. Ejes: ética, emotiva, conceptual.
- **Material clave** (verbatim):
  - "usted me dice que las máquinas no pueden pensar bueno, dígame exactamente qué es pensar qué es lo que las máquinas no pueden hacer y bueno, yo voy a hacer una máquina que haga exactamente eso que usted me dice si me lo define bien" (`WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:08]`)
- **Apariciones**: `WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:08]`

### ideas-como-ciudadanos-de-primera
- **Qué**: Luthier es un lenguaje para definir ideas, donde las ideas son ciudadanos de primera; se piensa por analogía con lenguajes naturales (castellano, inglés) que definen cosas, y en una primera etapa describe sobre todo invariantes.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Corre el eje de "un lenguaje ejecuta operaciones" a "un lenguaje define ideas". Reordena qué se pone en el centro. Ejes: ética, conceptual.
- **Material clave** (verbatim):
  - "Luthier tendría que ser un lenguaje donde las ideas son ciudadanos de primera, o sea de definir ideas" (`WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:38]`)
  - "que sea un lenguaje como el castellano, como el inglés que son lenguajes que definen cosas" (`WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:48]`)
  - "Primero Luthier va a ser un lenguaje que describa más que nada lo que llaman invariantes" (`WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[01:15]`)
- **Apariciones**: `WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:38]`, `[00:48]`, `[01:15]`; `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[00:58]` (expresar invarianzas de las disciplinas: biología, física); `WhatsApp Ptt 2026-05-31 at 20.10.19.mp3` `[00:00]` y `WhatsApp Ptt 2026-05-31 at 20.10.46.mp3` `[00:04]` (cuantificadores lógicos "para todo" y "existe" como ciudadanos de primera)
- **Tensión / pregunta abierta**: Queda planteado, sin cerrar, cuáles son en total los ciudadanos de primera de Luthier ("De cuáles son los ciudadanos de primera en Luthier", `WhatsApp Ptt 2026-05-31 at 20.10.46.mp3` `[00:12]`).

### luthier-lenguaje-para-la-ia
- **Qué**: Luthier tendría que ser un lenguaje que use la propia IA, no solo un humano; con el riesgo asociado de que el sistema se auto-hackee.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta pese al desarrollo mínimo. Cambia el destinatario del lenguaje y con eso su diseño entero; el "auto-hackeo" abre de golpe una dimensión de seguridad/reflexividad. Ejes: conceptual, emotiva.
- **Material clave** (verbatim):
  - "Luthier tendría que ser un lenguaje que use la IA misma, ¿no?" (`WhatsApp Ptt 2026-08-31 at 19.57.14.mp3` `[00:00]`)
  - "Lo que pasa es que puede ser que se auto-hackee." (`WhatsApp Ptt 2026-08-31 at 19.57.14.mp3` `[00:11]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.57.14.mp3` `[00:00]`, `[00:11]`
- **Tensión / pregunta abierta**: No se especifica en qué sentido la IA lo usaría, ni si el auto-hackeo es riesgo a evitar o capacidad a habilitar ("Le da que ver eso bien, cómo hacerlo", `[00:13]`).

### proposito-abierto
- **Qué**: Para qué sirve Luthier y si simplifica el problema de ingeniería concreto (macro IR) queda sin resolver; por ahora se lo enmarca como aventura intelectual, con las cosas que Luthier tiene que tener aún por destilar.
- **Tipo**: tensión abierta
- **Infectabilidad**: Media. No es una idea sino la honestidad sobre el estado del proyecto; vale conservarla porque enmarca todo el corpus como exploración, no como especificación. Ejes: emotiva, ética.
- **Material clave** (verbatim):
  - "hasta ahora es como una aventura intelectual más que nada" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[10:49]`)
  - "qué realmente me serviría para simplificar macro IR" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[04:55]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[04:55]`, `[10:49]`, `[12:02]`; `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[00:00]` ("tengo un problema de macro IR, pero ¿qué es un problema de Luthier?")
- **Tensión / pregunta abierta**: Recurre a lo largo del corpus y no se cierra; pendiente de "ir destilando las cosas que tiene que tener Luthier" (`[12:02]`).

## tipos-significado — El tipo como proposición: significado, garantía, autoverificación

El núcleo semántico. Un tipo no es un contenedor de datos: es una afirmación. De ahí se sigue que definir algo es afirmar sus propiedades, y que definir una función define su test.

### tipos-como-proposiciones
- **Qué**: El código tiene significado; pertenecer a un tipo equivale a afirmar una proposición. Los tipos son conceptos e incluyen funciones y funciones de orden superior. Es el origen conceptual de Luthier.
- **Tipo**: plántula
- **Infectabilidad**: Muy alta y es el principio más comprometido del corpus (aparece al inicio y al final, sin dudas). Toma la correspondencia tipos-proposiciones y la vuelve la sustancia del lenguaje, no una nota teórica. Ejes: conceptual, ética, estética.
- **Material clave** (verbatim):
  - "los tipos tienen que ser conceptos, tipos como proposiciones y los tipos incluyen también funciones, funciones y funciones de orden superior" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[00:38]`)
  - "la idea era originalmente que el código son, digamos, tiene significado, es decir, que pertenecer a un tipo, digamos, significa afirmar una proposición" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[01:02]`)
  - "definición de función desde el punto de vista de las propiedades, no operativamente [...] la proposición acerca de sus inputs y outputs" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[03:42]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[00:38]`; `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[01:02]`; `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[03:42]`

### gestion-del-error-como-garantia
- **Qué**: Un propósito de Luthier es que la gestión del error sea mejor y las cosas estén garantizadas: tener la clase de algo significa que cumple ciertas proposiciones. El valor o resultado lleva una anotación con todo lo que ya se sabe de su clase, y sabe por qué operación concreta se produjo (si fue la suma, es la suma, no el magma).
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Convierte el tipo en garantía activa y liga corrección con anotación acumulada; conecta directo con el functor olvido. Ejes: ética, conceptual.
- **Material clave** (verbatim):
  - "la idea de Luthier es que la gestión del error sea mejor... que las cosas estén garantizadas... si vos tenés una clase de algo, entonces significa que cumple ciertas proposiciones" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[02:35]`)
  - "tendría que tener algún tipo de anotación, digamos, de todas las cosas que ya sabemos de esta clase, de este valor, el resultado de un cálculo" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[03:09]`)
  - "si es la suma, ya es la suma y no es el magma, es la suma, no es la operación y el magma" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[03:50]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[02:35]`, `[03:09]`, `[03:50]`, `[04:15]` (niveles de una operación: magma, resultado, ejecución, código)
- **Tensión / pregunta abierta**: Qué son y cómo se distinguen esos "niveles" de una operación queda sin precisar ("no sé cómo distintas serían operaciones sobre un código", `[04:23]`).

### definicion-genera-el-test
- **Qué**: Luthier como autoverificación: al definir una función queda definido su test, y el test es el propio código, de modo que correr el código corre también el test (a cierto nivel). No se puede definir una función sin su inversa y su test. El valor puede estar sin testear o testeado, con distintos niveles de verificación. Tener código que representa los cálculos habilita autodiferenciar y obtener el resultado escrito paso por paso.
- **Tipo**: semilla latente
- **Infectabilidad**: Muy alta. "El test es el código" colapsa la distinción especificación/verificación/programa; es de las ideas que más reorganizan la práctica. Ejes: conceptual, estética, ética.
- **Material clave** (verbatim):
  - "un lenguaje que sea inspirado por los homeotopy type theory, en el cual vos definas una función y que al definir la función ya con eso quede definido el test sobre esa función" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[05:04]`)
  - "Luthier sería como una autoverificación del código, o sea que vos no podés definir una función sin su inversa y su test... y que el test sea el propio código entonces vos corre el código y... correr el test también sobre el código" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[11:13]`)
  - "comprobas que una función es correcta, es la idea de verificabilidad, es como una especie de verificabilidad" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:52]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[02:02]`, `[05:04]`, `[05:56]`, `[11:13]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:52]`
- **Tensión / pregunta abierta**: "A un determinado nivel" (`[11:34]`) queda sin definir; no se precisa qué nivel de verificación garantiza qué.

## paths-equivalencia — Separar el qué del cómo, y verificar que dos formas son la misma

El motor generativo de Luthier: se declara qué se quiere, hay muchas maneras de implementarlo (paths), y la capacidad central es demostrar que dos paths son equivalentes. La ejecución misma se reinterpreta como verificación de equivalencias.

### equivalencia-de-paths
- **Qué**: El concepto fundamental de Luthier es la equivalencia de paths: comparar dos caminos que hacen lo mismo y determinar que son equivalentes (con etapas de conversión de formato al principio y al final). Demostrarlo es lo más difícil del diseño. Se abstrae el concepto de implementación a través de los paths de homotopy type theory.
- **Tipo**: tensión abierta
- **Infectabilidad**: Máxima. Es el corazón conceptual del lenguaje y el que más cambia el marco: la implementación deja de ser "el código" y pasa a ser un punto entre puntos equivalentes. También el más costoso (el autor lo marca como "lo más difícil"). Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "el concepto fundamental es el de la equivalencia de PATH, de que los PATH sean equivalentes, que eso es lo más difícil" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:38]`)
  - "vos comparás dos caminos para hacer lo mismo" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:44]`)
  - "abstraemos el concepto de implementación a través de los paths… yo tengo distintas implementaciones y veo la equivalencia entre implementaciones" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:18–03:38]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:44]`; `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:18–03:38]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:38]`; `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:03]`; `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:26]` (cada path con su precisión y velocidad)
- **Tensión / pregunta abierta**: No se resuelve qué noción de equivalencia de paths se usa ni cómo se demuestra; requiere un demostrador interno (ver `demostrador-y-prueba-estadistica`).

### declarativo-mas-optimizacion
- **Qué**: Luthier es a la vez lenguaje declarativo y herramienta de optimización: uno declara qué quiere hacer y el sistema baraja abiertamente distintas formas de implementarlo, mapeando entre un lenguaje declarativo y uno ejecutivo. El énfasis no está en la ejecución sino en la explicitación (descripción del problema, de las funciones, de sus condiciones); la primera etapa es un lenguaje de descripción.
- **Tipo**: plántula
- **Infectabilidad**: Muy alta. Separar el qué del cómo con la optimización hecha "abiertamente" (no oculta en un compilador) es una postura fuerte y clara. Ejes: conceptual, ética, estética.
- **Material clave** (verbatim):
  - "que el Luthier sea, en el fondo, una forma de ser a la vez un lenguaje declarativo y una herramienta de optimización. O sea, que vos declares lo que querés hacer [...] y después internamente baraja distintas formas de implementar eso, pero eso lo hace abiertamente" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:52]`)
  - "lo más importante no es la ejecución, sino la explicitación, la descripción del problema" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:11]`)
  - "la primera etapa de Luthier tiene que ser como una especie de lenguaje de descripción, descripción del problema, descripción de las funciones, descripción de las condiciones de las funciones" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:20]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:52]`, `[02:51]`; `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:11]`, `[01:20]`; `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[04:59]` (prioridad conceptual sobre implementación); `WhatsApp Ptt 2026-05-30 at 18.02.45.mp3` `[00:10]` (Modelica: especificación sin implementación); `WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:58]` (lenguaje que vive vs lenguaje muerto)
- **Tensión / pregunta abierta**: Queda abierto si Luthier acciona o "podría ser un lenguaje muerto, un lenguaje que simplemente describa cosas" (`WhatsApp Ptt 2026-06-03 at 12.03.35.mp3` `[00:58]`).

### niveles-de-equivalencia
- **Qué**: Una idea fundamental es expresar distintos niveles de equivalencia (isomorfismo, igualdad exacta, misma ubicación en memoria, etc.), cada uno dado por un functor de equivalencia distinto. Las equivalencias permiten separar lo esencial (lo equivalente) de la decoración (eficiencia, costo, lo que no es equivalente).
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. "La equivalencia no es una, son varias, y elegir cuál define qué se está comparando" es una idea que reorganiza la noción de igualdad en programación. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[02:56]`)
  - "si vos tenés funciones que son equivalentes, después podés ver las cosas que no son equivalentes, que es, por ejemplo, los que son las decoraciones, que es la eficiencia, por ejemplo, el costo, lo que sea" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[03:18]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[02:56]`, `[03:18]`

### ejecucion-como-verificacion-de-equivalencias
- **Qué**: La ejecución en Luthier es verificación de equivalencias, análoga a cómo la matemática no "ejecuta" sino que verifica equivalencias. Ocurre, pero el énfasis está en la explicitación de esas equivalencias. La herramienta de análisis son los diagramas conmutativos ("cuadriláteros de equivalencia"): dos caminos que tienen que resultar congruentes.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Redefine qué es "correr un programa" y lo emparenta con la práctica matemática; conecta ejecución, verificación y paths en un mismo gesto. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "la ejecución en Luthier sería esa verificación de equivalencias, o sea que sí ocurre, claramente, pero el énfasis en principio está puesto en la explicitación de esas equivalencias" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:55]`)
  - "la manera de analizar esto es justamente usando los famosos cuadriláteros de equivalencia [...] que vos haces dos caminos y ves que son congruentes" (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[00:00]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[01:55]`; `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[00:00]`, `[01:03]`

## functor-olvido — Controlar el crecimiento de la anotación

Si el tipo acumula la historia de todo lo que se le hizo, crece sin límite. El functor olvido es el mecanismo para descartar información de manera controlada. El autor dice haber llegado a este concepto por Luthier mismo, y es uno de sus hallazgos más propios.

### functor-olvido
- **Qué**: Mecanismo de ir olvidando información para que las anotaciones (la carga de tipado) no crezcan al infinito. La elección de qué función de olvido se aplica define el lenguaje que se está hablando; los functores de olvido son de los componentes más importantes de Luthier, en implementación y en concepto. Hay varios, cada uno optimiza cosas distintas, y elegir cuál usar es un desafío de ingeniería.
- **Tipo**: semilla latente
- **Infectabilidad**: Máxima. Es la idea más original y personal del corpus: nombra un problema que casi ningún lenguaje enuncia (la anotación que crece) y le da un mecanismo con nombre. "Qué olvidás define qué lenguaje hablás" es profundamente infeccioso. Ejes: conceptual, estética, emotiva.
- **Material clave** (verbatim):
  - "tengo el functor olvido que sería, me voy olvidando algunas cosas, porque si no la cosa crece al infinito" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[03:18]`)
  - "los functores de olvido serían, digamos, uno de los componentes más importantes de Luthier en cuanto a la implementación y en cuanto a todo, ¿no?" (`WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[02:29]`)
  - "las distintas funciones de olvido de los tipos van a optimizar distintas cosas" (`WhatsApp Ptt 2026-05-29 at 15.00.11.mp3` `[00:00]`); "ahí hay un desafío de ingeniería, ¿de cuál usás para qué?" (`[00:07]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[01:42]`, `[03:18]`, `[10:28]`; `WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:51]`, `[02:29]`; `WhatsApp Ptt 2026-05-29 at 15.00.11.mp3` `[00:00]`, `[00:07]`, `[00:16]`; `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:00]`; `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:05]` (el olvido ya está en HoTT)
- **Tensión / pregunta abierta**: No hay criterio de qué se olvida ni cuándo; el autor lo marca explícitamente ("Eso hay que seguir pensándolo", `WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[02:44]`).

### problema-del-olvido-y-algebra-simplificadora
- **Qué**: Al componer funciones se acumula carga de tipado ("cada función va poniendo su granito de arena"); Luthier como "contador obsesivo" hace que el decorado se vuelva mucho más grande que el valor decorado. Ese crecimiento es "el olvido", uno de los problemas fundamentales a resolver. La solución sería un álgebra de tipado simplificadora: un monoide que no sea libre, que mantenga acotada la complejidad al componer.
- **Tipo**: tensión abierta
- **Infectabilidad**: Alta. Nombra con precisión el costo escondido de los tipos dependientes ricos y propone una salida algebraica elegante. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "vos vas acumulando, digamos, una carga de tipado que se va haciendo cada vez más fuerte" (`WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[00:08]`)
  - "si Luthier es como una especie de contador obsesivo que registra cada una de las operaciones que vos haces [...] lo que es el decorado se vuelva muchísimo más grande que el valor que está siendo decorado" (`WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[00:36]`)
  - "algún tipo de álgebra de tipado que sea un álgebra simplificadora, o sea, que no sea un monoide libre, básicamente" (`WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[01:06]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.52.08.mp3` `[00:08]`, `[00:24]`, `[00:36]`, `[01:06]`, `[02:19]`; `WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[00:09]` (álgebra de tipos dependientes rigurosa, no truncar de forma tosca)
- **Tensión / pregunta abierta**: No se define qué ecuaciones tendría ese monoide para dejar de ser libre, ni qué información es descartable; el autor duda incluso de si hace falta limitar ("quizás te queda una ristra de 17 funciones y está todo bien").

### tipo-como-historia-de-composicion
- **Qué**: El tipo de un valor registra la historia de las funciones que se le aplicaron. Si las funciones son asociativas, se encuentran patrones (un loop queda como una serie de funciones elevada a una potencia), y eso "te da una idea del tipo que es". El olvido selectivo es una función no invertible que descarta parte de esa historia.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. "El tipo es la historia de cómo llegaste" es una imagen potente; liga tipos, álgebra de composición y detección de patrones. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "eso te da una idea del tipo que es entonces ahí lo que tenés en el tipo es la historia de cómo llegaste hasta ahí" (`WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:27]`)
  - "si con olvido selectivo ahí puede ser una función digamos no se llama eso, no invertible, una función de olvido." (`WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:51]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.59.02.mp3` `[01:04]`, `[01:27]`, `[01:51]`

### conmutatividad-olvido-funciones
- **Qué**: Requisito mínimo sobre el olvido: olvidar y después aplicar la serie de funciones tiene que dar lo mismo que aplicar las funciones y después olvidar. El olvido debe conmutar con la composición, y eso se verifica con diagramas conmutativos (dos paths que resultan equivalentes).
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Es la ley que vuelve tratable el olvido; conecta este ecosistema con `paths-equivalencia`. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "si haces olvido compuesto con la serie de funciones, es lo mismo que serie de funciones y después olvido [...] que conmute, que eso sea igual" (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[00:39]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[00:39]`
- **Tensión / pregunta abierta**: No se define formalmente "olvido" ni las "funciones" en este contexto; se apoya en audios previos.

### olvido-como-proyeccion
- **Qué**: El olvido pensado como proyección sobre uno de los ejes (uno se olvida de los demás): una reducción de dimensionalidad. La primera forma concreta: de la iteración de un algoritmo sobre una función en cierto contexto, `get iteration` devuelve una iteración de la que ya no se sabe de qué es. Uniendo todas las proyecciones se puede reconstruir el objeto original.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Da una imagen geométrica concreta y operable del olvido (proyectar / reconstruir). Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "vos proyectás en uno de los ejes y entre los demás te olvidás ... es como una especie de proyección ... una reducción de dimensionalidad" (`WhatsApp Ptt 2026-06-05 at 13.16.35.mp3` `[00:44]`)
  - "Hacés get iteration de este objeto [...] ya ahí no sabés de qué es la iteración, es una iteración más" (`WhatsApp Ptt 2026-06-05 at 13.16.35.mp3` `[00:21]`)
  - "vos unís todas las proyecciones y recuperas el objeto original" (`WhatsApp Ptt 2026-06-05 at 13.16.35.mp3` `[01:07]`)
- **Apariciones**: `WhatsApp Ptt 2026-06-05 at 13.16.35.mp3` `[00:21]`, `[00:44]`, `[01:07]`
- **Tensión / pregunta abierta**: Sin decidir si las proyecciones son disjuntas o complementarias ("No tenés propiedades ahí, ¿no?", `[01:25]`).

### precision-segun-cuanto-recuerdes
- **Qué**: La precisión numérica recuperable depende de cuánto de la historia operacional se conserva: si recordás que tomaste el seno de 4, el arcoseno devuelve 4 exacto; si olvidás la operación, queda un valor con intervalo y se pierde precisión. Liga el functor olvido a la precisión. En el mismo movimiento: una media es una especie de functor de olvido.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Conecta un concepto abstracto (olvido) con algo palpable (error de punto flotante) de forma inesperada y convincente. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "si vos te acordás que tomaste el seno de 4... El arcoseno de seno es 4, chao. En cambio, si... te olvidás de la operación que hiciste... es un valor con un intervalo y ahora tomo la inversa y... yo ahí perdí un poco de precisión" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[08:07]`)
  - "Una media es como una especie de funtor de olvido, si se quiere" (`WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:40]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[08:07]`; `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:40]`

## hott-bayes — El matrimonio de tipos y probabilidad

La aspiración teórica: fundar Luthier en homotopy type theory pero casarla con inferencia bayesiana, de modo que las equivalencias mismas sean probabilísticas. Incluye lo que el autor ve como defectos de HoTT que Luthier tendría que cubrir.

### matrimonio-hott-bayes
- **Qué**: Luthier tiene que ser una especie de matrimonio entre Homotopy Type Theory y Bayes. La intención es que probabilidades y tipos vayan casi a la par, de manera que las equivalencias sean probabilísticas; HoTT daría el universo (los puntos, los conjuntos) sobre el que se aplican las probabilidades.
- **Tipo**: semilla latente
- **Infectabilidad**: Muy alta como visión. Cruzar prueba lógica con inferencia estadística en el mismo sistema de tipos es una apuesta conceptual grande y poco transitada. Ejes: conceptual, emotiva, estética.
- **Material clave** (verbatim):
  - "Para mí tiene que ser una especie de matrimonio entre Homeotopy Type Theory y Valles" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[02:40]`)
  - "la idea mía es de alguna manera que las probabilidades y los tipos vayan casi a la par. O sea que las equivialencias sean de alguna manera probabilísticas." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:40]`)
  - "Son Metrópita y Teori te dan los puntos del espacio, los conjuntos donde aplicas las probabilidades. Sería una cosa así." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[02:16]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[02:40]`; `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[01:32]`, `[01:40]`, `[02:16]`
- **Tensión / pregunta abierta**: El autor reconoce que "esto es un poco difícil de pensar" (`18.05.22` `[01:58]`); "Valles" es transcripción de Bayes. No hay mecanismo de integración formal.

### demostrador-y-prueba-estadistica
- **Qué**: Para demostrar equivalencia de paths, Luthier necesita internamente un demostrador (proof system). Además de la prueba lógica, necesita una demostración empírica/estadística de que algo funciona de cierta manera: una extensión probabilística de HoTT, donde en vez de una verdad lógica también se pueda hacer una inferencia estadística.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Admitir que la verificación puede ser estadística, no solo lógica, es un giro que abre el lenguaje al mundo empírico sin abandonar el rigor. Ejes: conceptual, ética.
- **Material clave** (verbatim):
  - "como lo demostrás matemáticamente, tiene que ser internamente tener un demostrador" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:50]`)
  - "tendría que ser una especie de extensión probabilística de homeotopy type theory [...] no es que vos tenés una verdad, digamos, lógica, sino que también podés hacer una inferencia estadística de que algo funciona de alguna manera" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[02:09]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:50]`, `[02:09]`
- **Tensión / pregunta abierta**: No se define cómo se integra la inferencia estadística con el sistema de tipos.

### tipos-dependientes-como-primitiva
- **Qué**: Los tipos dependientes son probablemente un concepto básico inicial del lenguaje; se entienden como una función que devuelve un tipo en vez de un valor ("aumenta de nivel de abstracción"). El tipo universal (que comprende los tipos de todas las dimensiones) se caracteriza como una "trampa" deliberada, asimilable a una clase abstracta, no un desafío de código imposible.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Es materia técnica de fundación; infecta menos por sí sola, pero es la base sobre la que se apoyan el olvido y las proposiciones. Ejes: conceptual.
- **Material clave** (verbatim):
  - "los tipos dependientes, sí, probablemente eso es un concepto, digamos, básico, inicial" (`WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:40]`)
  - "Es como una función que tira un tipo. En vez de tirar una variable, es como que aumenta de clase [...] aumenta de nivel de abstracción." (`WhatsApp Ptt 2026-05-29 at 14.03.24.mp3` `[00:15]`)
  - "la trampa que se hace [...] es que vos supones una especie de tipo universal que comprende a los tipos de todas las dimensiones. Y eso es algo así como una clase abstracta [...] no es un desafío, digamos, de código imposible." (`WhatsApp Ptt 2026-05-29 at 14.06.25.mp3` `[00:00]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:40]`; `WhatsApp Ptt 2026-05-29 at 14.03.24.mp3` `[00:15]`; `WhatsApp Ptt 2026-05-29 at 14.06.25.mp3` `[00:00]`; `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[03:02]` (mapear estrictamente los elementos de HoTT)
- **Tensión / pregunta abierta**: La caracterización de tipos dependientes se formula como pregunta ("¿Es eso?"); no es decisión cerrada.

### hott-sin-concepto-de-programa
- **Qué**: Defecto que Luthier tendría que cubrir: HoTT no conceptualiza qué es un programa. Tiene función y tipos, pero no un concepto de conjunto de expresiones que constituya un programa completo. Cada statement es modelable, pero la serie de statements (el programa como totalidad) no tiene modelado claro en la teoría, ni está claro que una "serie de tipos" exista como tipo.
- **Tipo**: tensión abierta
- **Infectabilidad**: Alta. Localiza con precisión el hueco teórico que Luthier viene a llenar; da al proyecto su razón de ser frente a la teoría existente. Ejes: conceptual.
- **Material clave** (verbatim):
  - "hay un concepto de función, de tipos, pero de programa no me queda muy claro que esté, eso es uno de los defectos." (`WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[00:41]`)
  - "Vos tenés un programa que es una serie de statements que son todos modelables [...] pero el programa en sí, en principio no tan claramente" (`WhatsApp Ptt 2026-05-29 at 14.37.14.mp3` `[00:25]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.05.22.mp3` `[00:41]`; `WhatsApp Ptt 2026-05-29 at 14.37.14.mp3` `[00:07]`, `[00:25]`
- **Tensión / pregunta abierta**: Se descarta tentativamente modelarlo como lista ("a mí me parece como que geometría de Taitieri no está modelando eso", `[00:41]`); queda abierto. Este hueco es lo que el ecosistema `programa-como-dag` intenta cubrir.

### hot-values-y-filtrado-de-particulas
- **Qué**: "Hot Values" como universo más grande de caminos posibles. Para manejar la explosión exponencial, filtrado de partículas: correr varios programas en paralelo con programación estocástica que exploran caminos distintos, replicando un "hot basin".
- **Tipo**: semilla latente
- **Infectabilidad**: Media. Trae maquinaria bayesiana computacional concreta al lenguaje; potente pero muy poco desarrollada y sin encaje definido. Ejes: conceptual.
- **Material clave** (verbatim):
  - "sería que tenés un universo más grande de posibilidades, algo así, de caminos posibles" (`WhatsApp Ptt 2026-05-30 at 18.15.07.mp3` `[00:39]`)
  - "lo que podés hacer es hacer el filtrado de partículas [...] corres varios programas en paralelos y haces una programación estocástica que van por distintos lados [...] estás replicando un hot basin" (`WhatsApp Ptt 2026-05-30 at 18.15.07.mp3` `[00:54]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.15.07.mp3` `[00:39]`, `[00:54]`
- **Tensión / pregunta abierta**: No se define cómo se integra en Luthier ni qué estructura tienen esos programas en paralelo.

## programa-como-dag — El programa como grafo de dependencias: tiempo, conmutatividad y auto-operación

Cómo se estructura un programa Luthier. La respuesta es un DAG de definiciones: el orden textual no importa, el tiempo se reconstruye de la dependencia causal, y el propio programa es un objeto de Luthier sobre el que Luthier opera.

### conmutatividad-de-statements-y-tiempo-causal
- **Qué**: Los statements de Luthier son conmutativos: el orden en que se escriben no altera el resultado, lo que simplifica la composición y manipulación de programas. Se sostiene porque la temporalidad no viene del orden textual sino de la dependencia de tipos: "lo que ocurre mañana depende de lo que ocurrió hoy", el tiempo se reconstruye a partir de la causalidad. En la zona de declaración se logra una pseudo-conmutatividad (como las forward declarations de C++).
- **Tipo**: tensión abierta
- **Infectabilidad**: Alta. "El tiempo es dependencia, no secuencia" es una reorganización fuerte de qué significa un programa. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "que sea conmutativo en los statements, que el orden en los statements no altera el resultado, eso simplificaría mucho la composición y la manipulación de programas." (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:35]`)
  - "la temporalidad se da a lo PERL a partir de la dependencia de tipos. Lo que ocurre mañana depende de lo que ocurrió hoy [...] La temporalidad se reconstruye a partir de la causalidad." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:00]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.36.03.mp3` `[00:00]`, `[00:37]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:35]`, `[01:26]`; `WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:00]`; `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:00]`
- **Tensión / pregunta abierta**: El autor reconoce que la conmutatividad quita expresividad ("te quita expresividad, de alguna manera, eso es verdad") y no resuelve el trade-off, aunque se inclina a favor.

### programa-como-dag-de-definiciones
- **Qué**: Un programa Luthier, estáticamente, es un DAG (grafo dirigido acíclico) de definiciones, donde los tipos dependen de otros tipos (esta es también la forma del contexto). Las operaciones sobre programas serían operaciones sobre DAGs (combinarlos, etc.). El DAG es lo que sostiene la conmutatividad: el orden no importa porque la dependencia la da el grafo.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Da una estructura concreta y manipulable al programa, y es el sustrato que unifica conmutatividad, contexto y meta-operación. Ejes: conceptual.
- **Material clave** (verbatim):
  - "que Luthier es un Directed Cyclic Graph de definiciones. Entonces, la cosa es bastante fácil. Vos operas sobre [...] DACs [...] serían como combinados DACs, por ejemplo, eso sería una operación sobre Luthier." (`WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[01:48]`)
  - "La manera de definir contexto sería como un DAG, un Directed Acyclic Graph, donde vos partís de tipos que dependen de otros, etc." (`WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[00:23]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[00:23]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[01:48]`; `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:07]`
- **Tensión / pregunta abierta**: El autor dice "Directed Cyclic Graph" pero la lógica sin ciclos indica DAG; no queda resuelto cómo encajan exactamente las funciones (sustitución de variables) dentro del modelo ("ahí pensándolo todo").

### meta-recursividad-codigo-como-elemento
- **Qué**: El objeto de Luthier es trabajar sobre Luthier: la meta-recursividad es fundamental. El código de Luthier tiene que ser él mismo un elemento de Luthier desde el vamos ("el código es el primer elemento"), como en Lisp pero no implantado después. Se puede tener un DAG que opera sobre DAGs (programas que manipulan programas), y tomar las funciones como datos (código como datos) para darles la misma estructura relacional.
- **Tipo**: semilla latente
- **Infectabilidad**: Muy alta. Homoiconicidad puesta como principio de origen, no como truco; con el "universo propio" habilita que Luthier se opere y transforme a sí mismo. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "Luthier tiene que operar sobre Luthier también [...] desde el vamos, como en LISP que medio que se implantó después [...] el código de Luthier sea un elemento de Luthier ya también desde el vamos. O sea, el código es el primer elemento." (`WhatsApp Ptt 2026-05-29 at 14.36.03.mp3` `[02:16]`)
  - "vos podés tener en realidad un DAG que opera sobre DAGs, que opera sobre programas [...] hay algo que opera sobre ese DAG y después se transforma en otra cosa con instrucciones de sí mismo" (`WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:19]`)
  - "Las funciones como datos, o sea, el código como datos. entonces sí podés tener también lo mismo, ¿no?" (`WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[04:34]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.36.03.mp3` `[01:56]`, `[02:16]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[00:07]`; `WhatsApp Ptt 2026-05-30 at 18.11.30.mp3` `[00:38]`, `[00:54]`; `WhatsApp Ptt 2026-05-30 at 18.12.54.mp3` `[00:19]`; `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[04:34]`
- **Tensión / pregunta abierta**: Queda sin desarrollar qué es exactamente ese "algo que opera sobre el DAG" y cómo funciona la auto-transformación; se conecta con el `riesgo-de-auto-hackeo`.

### no-ejecutar-hasta-definido
- **Qué**: El código no se ejecuta hasta que no está completamente definido, lo que permite tener código "muerto" o incompleto que no molesta porque simplemente no corre. Y al código de Luthier se le pueden aplicar muchas operaciones (verificar, compilar, correr, otras), no solo compilar y correr.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Reencuadra el código como dato multi-operación, no como algo con un único destino de ejecución. Ejes: conceptual.
- **Material clave** (verbatim):
  - "vos no ejecutás el código hasta que no está definido. Entonces [...] vos podés tener un montón de código muerto que no jode a nadie porque no está completamente definido." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:53]`)
  - "al código de Luthier vos podés hacerle muchas cosas. No es que vos lo compilás y lo corres nada más." (`WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[01:52]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.09.57.mp3` `[00:53]`, `[01:52]`
- **Tensión / pregunta abierta**: Qué significa exactamente "definido" queda sin precisar ("habría que definir un poco eso").

## minimalismo — Pocos elementos fundantes, edificio infinito, ejecutable a mano

Cómo se construye tanto con tan poco. El minimalismo está en la base (identidad, equivalencia, tipos y funciones), y de ahí se levanta todo por autoextensión. La prueba de que el core está bien es que se pueda ejecutar a mano.

### minimalismo-fundacional-maximalismo-derivado
- **Qué**: No hay contradicción entre minimalismo y maximalismo: el minimalismo está en los componentes fundantes y desde ellos se construye un edificio enorme, al estilo de la teoría de categorías (functores definidos a partir de flechas). Solo hay tipos y funciones, y las funciones son de un tipo; quizás baste empezar con la identidad o algún principio de equivalencia. El objetivo es reducir a un mínimo sin resignar la expresión de los conceptos complejos.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Disuelve una falsa oposición (poco vs mucho) con una tesis clara y estéticamente satisfactoria sobre dónde va cada cosa. Ejes: estética, ética, conceptual.
- **Material clave** (verbatim):
  - "El minimalismo está en los componentes fundantes y después a partir de esos componentes fundantes vos construís un edificio enorme" (`WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:12]`)
  - "solamente hay tipos y hay funciones, pero funciones son de un tipo" (`WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[02:31–02:40]`)
  - "vamos a tratar de reducir todo a un mínimo, pero sí, queremos tener todos esos conceptos complejos [...] basados en que los elementos mínimos sean pocos" (`WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[01:04]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.07.21.mp3` `[00:12]`, `[00:25]`, `[00:40]`, `[00:56]`, `[01:04]`; `WhatsApp Ptt 2026-05-29 at 13.57.41.mp3` `[02:08]` (Lisp: todo son listas), `[02:31–02:40]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[03:22]`; `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:00]` (muy pocos tipos con reglas rigurosas)
- **Tensión / pregunta abierta**: Cuáles son exactamente los elementos mínimos queda abierto; oscila entre "solo la identidad", "identidad más igualdad", "tipos y funciones" ("No sé, claro que solamente…", `18.07.21` `[00:56]`).

### autoextensibilidad
- **Qué**: El lenguaje tiene que ser completamente autoextensible: poder escribir todo Luthier en Luthier, de modo que al final solo haya que implementar unas pocas primitivas en C o similar (un core mínimo bootstrapped donde corren todas las operaciones).
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Es el criterio operativo del minimalismo y una meta ambiciosa clara: un core diminuto que se explica a sí mismo. Ejes: ética, estética, conceptual.
- **Material clave** (verbatim):
  - "tiene que ser completamente extensible, autoextensible, es decir, que vos puedas escribir como en Luthier, todo lo de Luthier [...] cosa que al final solamente termines implementando algunas cosas" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:26]`)
  - "uno debería tener claro un core de Luthier en el cual se ejecute por todas operaciones de Luthier y solamente implementar algunas pocas en C o en alguna cosa así, como para que corra" (`WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[03:48]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:26]`; `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[03:48]`; `WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[00:00]` (core más librerías)

### ejecutable-a-mano
- **Qué**: Si está bien escrito, Luthier tendría que ser ejecutable a mano, con lápiz y papel, lo que haría la implementación clara.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Es un test estético y epistémico fuerte: la comprensibilidad como criterio de diseño del lenguaje. Ejes: estética, ética.
- **Material clave** (verbatim):
  - "si está bien escrito, Luthier tendría que ser ejecutable a mano, es decir, que uno pudiese con lápiz y papel escribir las cosas" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:13]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[01:13]`; `WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:38]` (expresar con lápiz y papel primero, después ejecutar)
- **Tensión / pregunta abierta**: Ver `dos-capas-lapiz-y-base-de-datos` en `memoria-empirica`: cómo convive el ejecutar a mano con la consulta a una base de datos empírica.

## frontera-externa — Luthier frente a lo que no es Luthier

Luthier se piensa cerrado y perfecto por dentro, y todo lo demás (C++, Python, la computadora, cualquier recurso) es externo. El problema de diseño es la frontera: cómo orquesta, secuestra y mapea sin dejar de ser un metalenguaje agnóstico.

### metalenguaje-cross-lenguaje
- **Qué**: Luthier no es una implementación sino un metalenguaje o conjunto de especificaciones, del que pueden existir varias implementaciones (PyLuthier, RLuthier, un Luthier en C++). No es cross-compiler sino directamente cross-lenguaje: agnóstico del lenguaje de implementación, aunque el motor esté en alguno.
- **Tipo**: tensión abierta
- **Infectabilidad**: Alta. Separar la especificación del lenguaje de cualquier implementación concreta, y hacerlo agnóstico, es una postura arquitectónica fuerte. Ejes: conceptual, ética.
- **Material clave** (verbatim):
  - "Son especificaciones que podes tener distintas implementaciones de Luthier, podes tener un Piluthier, Arluthiero o un Luthier CPP, no sé, distintas cosas." (`WhatsApp Ptt 2026-08-31 at 20.00.05.mp3` `[00:08]`)
  - "luthier debería ser [...] no es cross compiler sino directamente cross lenguaje [...] sería un poco agnóstico del lenguaje si bien el motor podría estar implementado en alguno de ellos" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[04:24]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[01:04]`, `[04:24]`; `WhatsApp Ptt 2026-08-31 at 20.00.05.mp3` `[00:08]`, `[00:43]`, `[01:07]`, `[01:33]`
- **Tensión / pregunta abierta**: Sin decidir entre Luthier embebido (clase/atributo flotante en Python, "lo más fácil") y Luthier como lenguaje autónomo ("debo ver todas las posibilidades", `20.00.05` `[01:31]`). En la vía Python el tipo no es un tipo real del anfitrión sino campos y decoraciones, y Python "no es la herramienta" para tipos, afirmación que el propio autor no cierra.

### mayordomo-que-orquesta-y-compone
- **Qué**: Luthier como lenguaje de orden superior, una especie de mayordomo que puede correr básicamente cualquier programa, comparar sus outputs y componer la entrada y salida de un programa con otro, encadenando programas externos y expresando su complejidad.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. La metáfora del mayordomo es vívida y define el rol de Luthier como coordinador, no ejecutor. Ejes: emotiva, conceptual, estética.
- **Material clave** (verbatim):
  - "la idea es que Luthier sea como un lenguaje de orden superior. Entonces, si es de orden superior, una especie de mayordomo [...] esto lo hago en R, lo hago en Python o lo hago en C++ [...] y eso tiene tal y tal complejidad" (`WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[03:34]`)
  - "me lo imagino como un mayordomo que puede correr básicamente cualquier programa y que puede comparar los outputs" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:00]`)
  - "Luthier lo que tendría que hacer es poder componer la entrada y salida de un programa y otro" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:26]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[03:34]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:00]`, `[00:26]`

### secuestrar-y-luthierizar-codigo
- **Qué**: Luthier tiene que poder secuestrar código de cualquier otro lenguaje, y funcionar como anotador: "luthierizar" código ajeno (p. ej. varias librerías de Python de inversión de matriz) partiendo de la definición de qué es la operación y qué propiedad debe cumplir.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. "Anotar y secuestrar código ajeno" da a Luthier una vía de adopción concreta y una relación no imperialista con el ecosistema existente. Ejes: conceptual, ética.
- **Material clave** (verbatim):
  - "el UTIER tiene que poder secuestrar código de cualquier otro lenguaje" (`WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:48]`)
  - "La idea es que Luthier sea como un anotador de código. Vos podrías luthierizar, por ejemplo, un código ajeno" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[06:11]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.14.08.mp3` `[00:48]`; `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[06:11]`

### luthier-cerrado-observador
- **Qué**: Luthier como sistema cerrado y completo internamente ("todos sus tipos así perfectos") que observa el universo exterior; todo lo que no es Luthier es un "elemento externo" a modelar. La comunicación con afuera es un ciclo read-write: convertir código Luthier en ejecutable (C, etc.) y leer archivos o datos externos convirtiéndolos en Luthier. Se plantea incluso delegar la ejecución y quedarse solo con la verificación.
- **Tipo**: tensión abierta
- **Infectabilidad**: Media-alta. La imagen del sistema cerrado que observa (con el afuera como tipo) es conceptualmente limpia; la delegación total de la ejecución es una versión extrema y provocadora del minimalismo. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "yo lo estoy pensando como un observador y del universo, o sea, Luthier sería cerrado, como que tiene todos sus tipos así perfectos" (`WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[01:11]`)
  - "C++ o un programa de Python o la computadora o cualquier recurso no es un elemento de Luthier, es como un elemento externo" (`WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[00:37]`)
  - "a ver si yo hasta puedo delegar la parte de ejecución y que lo único que haga sea la verificación" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[04:35]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.18.55.mp3` `[00:37]`, `[01:11]`, `[01:21]`; `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[04:35]`; `WhatsApp Ptt 2026-05-30 at 18.01.53.mp3` `[04:07]` (facilidad para correr otros programas), `[05:49]` (dar las facilidades para mapear a otros lenguajes, no hacerlo directamente); `WhatsApp Ptt 2026-05-30 at 18.02.45.mp3` `[00:00]` (delegación fácil)
- **Tensión / pregunta abierta**: No se resuelve cómo se modela el "elemento externo" ("no sé eso como es exactamente", `[00:55]`), ni si el read-write es compilación, input-output u otra cosa, ni si la ejecución es parte de Luthier.

## memoria-empirica — La base de datos de corridas y la estimación de complejidad

La cara empírica de la optimización: para elegir entre paths equivalentes hace falta saber cuánto tardan y con qué precisión. Eso se aprende corriendo, se guarda en una base y se generaliza. El problema central es sintetizar esa información sin que se vuelva monstruosa.

### estimacion-bayesiana-de-complejidad
- **Qué**: Ante el problema abierto de evaluar a priori la complejidad de distintos cómputos, una estrategia bayesiana: dar oportunidad a distintos algoritmos para la misma tarea, medir sus tiempos efectivos y estimar a partir de la experiencia acumulada. Las propias funciones de modelado del tiempo y la precisión son herramientas que Luthier usa (el sistema se estima a sí mismo).
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Tratar la complejidad como algo que se aprende empíricamente, no que se deriva a priori, y que el sistema use sus propias estimaciones, es un giro reflexivo potente. Ejes: conceptual.
- **Material clave** (verbatim):
  - "voy dándole oportunidad a distintos algoritmos para hacer lo mismo y después voy estimando los tiempos que toman para problemas parecidos a partir de la experiencia, de correrlos efectivamente" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[00:28]`)
  - "la idea es que vos lo utilizas las funciones de estimación de [...] el tiempo de cómputo de la precisión de cómputo" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[03:05]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[00:28]`, `[03:05]`; `WhatsApp Ptt 2026-05-26 at 12.32.24.mp3` `[03:10]`, `[05:28]` (estimar la complejidad de distintas formas de ejecución); `WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[01:04]` (decorar los paths con tiempo, recursos, éxito/fracaso)
- **Tensión / pregunta abierta**: No se especifica cómo se balancea exploración vs. explotación. El autor se autocorrige de "la mejor solución" a "distintas soluciones" (`12.32.24` `[05:28]`), dejando abierto si Luthier elige o solo presenta opciones.

### base-de-datos-de-rendimiento-generalizable
- **Qué**: Luthier registra empíricamente, para cada combinación de función, datos iniciales, escala y algoritmo, cuánto tardó y qué precisión tuvo. Esa base hay que poder generalizarla (pasar de mediciones puntuales a tendencias): muchos cómputos parecidos pertenecen a la misma clase, y el tiempo se computa a partir de una simplificación de los inputs (las características más predictivas, p. ej. las dimensiones de una matriz), no de los inputs completos.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Convierte al lenguaje en un sistema que aprende de sí mismo; la idea de "clase de cómputos" y de predecir por características simplificadas es fértil. Ejes: conceptual.
- **Material clave** (verbatim):
  - "para esta función, con estos datos iniciales, y esta escala, yo usando este algoritmo tardé tanto tiempo y tuve tanta precisión [...] lo corrí, o sea, lo medí, efectivamente" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[01:21]`)
  - "muchos cómputos parecidos pertenecen a la misma [...] clase de cómputos [...] lo que habría que empezar a encontrar es eso [...] las categorías" (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[03:34]`)
  - "vos computás el tiempo de cálculo a partir de una simplificación de los inputs." (`WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[04:26]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-26 at 12.41.09.mp3` `[01:21]`, `[01:42]`, `[02:16]`, `[03:34]`, `[04:11]`, `[04:26]`; `WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:00]` (Luthier como base de datos de corridas: memoria, CPUs, tiempo, rango de resultados)
- **Tensión / pregunta abierta**: El autor reconoce no saber cómo generalizar efectivamente ("ahí estoy un poco en pelotas", `12.41.09` `[01:42]`); la organización en matriz con estimación por filas/columnas queda exploratoria.

### sintesis-de-informacion-acumulada
- **Qué**: El desafío central: cómo sintetizar a la larga la información acumulada de las corridas, que puede volverse "monstruosa" y paralizante. Ligado a la observación de que el resumen puede ser más grande que los datos que resume (más interpretaciones de Borges que libros de Borges), y a que el modelo se justifica por su uso para un caso particular. Es "la clave de todo, hacerlo bien".
- **Tipo**: tensión abierta
- **Infectabilidad**: Media-alta. El autor lo marca como clave; conecta con `functor-olvido` (la síntesis es olvido) y con la advertencia de que resumir puede inflar en vez de comprimir. Ejes: conceptual, emotiva.
- **Material clave** (verbatim):
  - "el problema es cómo vos la sintetizás a la larga, porque puede ser [...] como una cosa monstruosa [...] para que no se vea paralizante" (`WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:32]`)
  - "a veces es que el resumen es más grande que el texto [...] como hay más interpretaciones de los libros de Borges que los libros de Borges en sí" (`WhatsApp Ptt 2026-05-27 at 13.51.41.mp3` `[00:12]`)
  - "ese análisis sintético, la síntesis, eso es un tema muy apasionante y bueno, sí, claramente es la clave de todo, hacerlo bien" (`WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:56]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:32]`; `WhatsApp Ptt 2026-05-27 at 13.51.41.mp3` `[00:12]`, `[00:29]`; `WhatsApp Ptt 2026-05-27 at 13.51.51.mp3` `[00:11]`, `[00:32]` (modelo del mundo mantenido activo); `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[00:56]`
- **Tensión / pregunta abierta**: No se propone criterio de síntesis; el autor cierra con "es peligroso" (`13.51.41` `[00:48]`) sin desarrollar el peligro. Se cruza con el `functor-olvido` como posible mecanismo.

### dos-capas-lapiz-y-base-de-datos
- **Qué**: Ejecutar con lápiz y papel y consultar una base de datos con corridas empíricas no son filosofías opuestas: son dos capas o momentos. Primero se expresan las ideas (lápiz y papel), después se va a la ejecución/consulta empírica; ninguna es aspiración y la otra concesión.
- **Tipo**: tensión abierta
- **Infectabilidad**: Media. Reconcilia la cara formal y la empírica del lenguaje, que de otro modo parecerían en conflicto. Ejes: conceptual, ética.
- **Material clave** (verbatim):
  - "Vos podés ejecutarlo con la pici papel y mirar una base de datos [...] Podés expresarlo con lápiz y papel." (`WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:14]`)
  - "son dos capas, dos momentos. Y no es que uno sea una aspiración de la concesión." (`WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:30]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-30 at 18.17.51.mp3` `[00:14]`, `[00:30]`, `[00:38]`
- **Tensión / pregunta abierta**: No se define qué pertenece a cada capa ni cómo se articulan; la frase queda cortada ("después es que vayas").

## expresividad — Expresar es el valor, incluso para descartar

Una postura de método más que un mecanismo: lo importante no es tener la manera correcta única sino poder formular todas las alternativas, incluso las inútiles. De esta postura salen decisiones concretas sobre tipos diferidos, doble definición y el trade-off con la robustez.

### expresividad-sobre-optimalidad
- **Qué**: Lo importante no es que haya una única manera correcta de hacer las cosas sino que el lenguaje sea lo bastante expresivo para formular distintas alternativas; cada una tiene su uso, no hay mejor ni peor. Incluso expresar algo que resulta inútil tiene valor: te permite descartarlo con certeza, sin dudar. Método: primero expresar bien, después elegir los aciertos.
- **Tipo**: plántula
- **Infectabilidad**: Muy alta. "Expresar para descartar" es una tesis ética sobre para qué sirve un lenguaje, memorable y contraria al instinto optimizador. Ejes: ética, estética, emotiva.
- **Material clave** (verbatim):
  - "no es que uno tiene que obligatoriamente hacer todo sino tener las herramientas para expresar distintas alternativas. Eso es lo importante. Que sea expresivo el lenguaje." (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:20]`)
  - "Aunque el uso sea convencerte de que no sirva para nada. Por lo menos no dudar." (`WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:45]`)
  - "lo primero que uno puede hacer es ver cómo expresarlo bien [...] podés expresar los aciertos y los errores y bueno, después elegís los aciertos" (`WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[01:19]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 15.04.28.mp3` `[01:20]`, `[01:45]`; `WhatsApp Ptt 2026-05-30 at 18.16.35.mp3` `[01:19]`

### expresividad-vs-robustez
- **Qué**: Tensión de diseño: maximizar la expresividad (tipos diferidos, doble definición, flexibilidad) a costa de menor robustez, apostando a que buenos mensajes del compilador compensen. Frente a forzar redundancia (expresar lo mismo de varios lados para bajar errores). El autor se inclina por lo expresivo, porque lo redundante puede ser incómodo y limitar al pedo.
- **Tipo**: tensión abierta
- **Infectabilidad**: Media-alta. Un dilema de diseño nítido con una inclinación declarada pero no cerrada; ordena varias decisiones concretas. Ejes: ética, conceptual.
- **Material clave** (verbatim):
  - "un poco de optimización de la expresividad a costa de ser un poco menos robusto [...] con buenos mensajes de qué es lo que está ocurriendo [...] podés eso tener gran flexibilidad y no tener error" (`WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[02:36]`)
  - "lo expresivo, digamos, garpa más, porque puede ser que lo redundante sea incómodo a veces y te limite al pedo, ¿no?" (`WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[03:26]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[02:36]`, `[03:03]`, `[03:26]`
- **Tensión / pregunta abierta**: El autor no decide categóricamente y se contradice sobre si esto es filosofía o detalle de implementación ("creo que esos son más bien detalles, no hacen a la filosofía [...] Bueno, la filosofía podría ser, ¿no?", `[03:03]`).

### tipos-diferidos-e-implicitos
- **Qué**: Concreción de la expresividad: permitir tipos implícitos (definidos como solución a un problema o como el óptimo de una función), referirse a tipos aún no definidos y definirlos después (o dejarlos sin definir, funcionando como inputs del programa). El compilador debería verificar que ningún tipo esté definido dos veces, salvo que una doble definición se interprete como producto cartesiano, ganando poder expresivo.
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. Los tipos-como-solución y la doble definición como producto son movimientos expresivos originales; encajan con el DAG y la definición diferida. Ejes: conceptual.
- **Material clave** (verbatim):
  - "vos podrías definir tipos implícitos a través de soluciones o de, por ejemplo, el tipo que soluciona determinado problema" (`WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[00:37]`)
  - "vos podés [...] pasarte a un tipo que no está definido, lo definís después [...] O ese tipo [...] es un input del programa, si no está definido nunca." (`WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[01:16]`)
  - "el compilador de Luthier, sería verificar que ningún tipo está definido dos veces. Aunque podría estar definido dos veces y que sea un producto cartesiano también." (`WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[01:38]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.46.22.mp3` `[00:37]`, `[01:16]`, `[01:38]`; `WhatsApp Ptt 2026-05-29 at 15.11.47.mp3` `[01:10]` (declarar dos veces como producto cartesiano)
- **Tensión / pregunta abierta**: Queda abierto si la doble definición es error, producto cartesiano o configurable (posible warning intermedio).

## error-y-decoradores — Números con error, funciones no unívocas, samples

El terreno concreto donde Luthier probaría su valor: modelar el error de los números y las funciones que no dan un valor exacto, no como parche posterior sino desde el lenguaje. Es la bajada numérica del functor olvido y del matrimonio con Bayes.

### funciones-no-univocas-y-decoradores-de-error
- **Qué**: Modelar desde el lenguaje mismo funciones no unívocas (con error, samples/muestras), no como añadido posterior. Usar decoradores para representar el error de un número y su propagación (derivadas, etc.), y poder expresar si la operación de un decorador sobre otro cumple asociatividad, conmutatividad, etc. Empezar por el ABC: números, reales, sus operaciones y un concepto de error de los reales.
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Poner el error y la no-unicidad como ciudadanos del core (no como excepción) reordena cómo se piensa el cálculo numérico. Ejes: conceptual, ética.
- **Material clave** (verbatim):
  - "que uno pueda modelar, desde el vamos, funciones no unívocas, que serían funciones con error, o sea, samples [...] que estén ya desde el lenguaje" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[04:30]`)
  - "uno en Luthier puede hacer decoradores fáciles [...] por ejemplo eso, el error de un número" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[03:05]`)
  - "si la operación de un decorador sobre el otro decorador [...] cumple la asociatividad [...] o [...] la conmutatividad" (`WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[05:18]`)
- **Apariciones**: `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[02:37]`, `[03:05]`, `[04:30]`, `[05:18]`; `WhatsApp Ptt 2026-05-29 at 14.28.55.mp3` `[00:13]` (Luthier como relator/mecanismo de abstracción para probabilidad, samples, matrices, unidades)
- **Tensión / pregunta abierta**: Sin resolver si "desde el lenguaje" es primitiva del core o librería estándar temprana, ni qué se da built-in y qué no.

### dato-con-error-intervalo-o-sample
- **Qué**: Un valor puede ser en realidad un intervalo de valores, o una sample de valores (p. ej. una cadena de Markov representada por una sample). Las propiedades (que la inversa recupere el valor) se cumplen solo dentro de cierto error, porque muchas inversas no son perfectas (seno y arcoseno no devuelven el mismo valor exacto).
- **Tipo**: semilla latente
- **Infectabilidad**: Media-alta. "El valor no es un punto, es un intervalo o una muestra" es una generalización natural que conecta con el error, la precisión y Bayes. Ejes: conceptual.
- **Material clave** (verbatim):
  - "el valor es un intervalo de valores [...] o puede ser que sea por ejemplo una sample de valores, en el caso de que sea una cadena de Markov, vos podes representarla con una sample" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[07:10]`)
  - "dentro de cierto error, porque bueno no es perfecta la inversa [...] el seno y el arcoseno no te da el mismo valor, perdés un pendejésimo por ahí" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[06:41]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[06:41]`, `[07:10]`; `WhatsApp Ptt 2026-05-30 at 18.15.07.mp3` `[01:31]` (errores en las mediciones que se propagan)

### codigo-cumple-las-leyes-aunque-el-float-no
- **Qué**: Los floating points no cumplen las reglas algebraicas (asociatividad), pero el código sí se supone que las cumple, y por eso se lo puede reorganizar para que la ejecución sea más eficiente o más perfecta. La ejecución es código que genera código, con dos niveles: uno que guarda el código generado y otro que lo olvida (la ejecución como función olvido).
- **Tipo**: semilla latente
- **Infectabilidad**: Alta. Distinguir la legalidad algebraica del código de la del hardware, y usar esa brecha como grado de libertad para reorganizar, es una idea fina y operable; cierra el círculo con `functor-olvido` y `equivalencia-de-paths`. Ejes: conceptual, estética.
- **Material clave** (verbatim):
  - "los números floating points, que no siguen las reglas [...] No las siguen, pero sí las siguen, digamos, lo que sería el código [...] vos suponés que el código sí la sigue, de lo reorganizadas de tal manera de que [...] la ejecución sea más eficiente o más perfecta" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[08:42]`)
  - "es código que genera código, que vos al ejecutar código lo que haces es transcribís código o ejecutás [...] como dos niveles de ejecución, una ejecución que guardás el código y otra que [...] eso lo olvidás" (`WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[09:56]`)
- **Apariciones**: `WhatsApp Ptt 2026-08-31 at 19.48.17.mp3` `[08:42]`, `[09:09]`, `[09:56]`

---

Nota final de editor. Dos cosas que el corpus deja pendientes y que atraviesan varios ecosistemas, por si querés atacarlas de frente: (1) el criterio para elegir functor de olvido, que reaparece en `functor-olvido`, `sintesis-de-informacion-acumulada` y `precision-segun-cuanto-recuerdes` sin cerrarse nunca; (2) la frontera de qué es Luthier y qué es externo, que decide de golpe el minimalismo, la ejecución delegada y el estatus de la base de datos empírica. Son los dos nudos donde más ideas se tocan.
