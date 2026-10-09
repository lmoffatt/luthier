---
audio: WhatsApp Ptt 2026-10-08 at 18.10.00.mp3
fecha: 2026-10-08
duracion: ~33:16
ideas: 35
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### semantica-base-cartesian-closed-categories
- **Qué**: La escritura básica de Luthier se apoya en Cartesian Closed Categories: sumas de tipos, productos de tipos y exponenciales de tipos.
- **Cita** (verbatim): "lo que sería Cartesian Close Categories, ... que serían sumas de tipos, productos de tipos y exponencial de tipos." `[00:27]`

### tipos-dependientes
- **Qué**: A la base categórica le suma los tipos dependientes.
- **Cita** (verbatim): "Y luego tendría las, ¿cómo se llama? Los tipos dependientes, ¿no?" `[00:42]`

### object-classifier-como-leyes
- **Qué**: Una especie de object classifier: predicados acerca de tipos, que serían las leyes y los nombres.
- **Cita** (verbatim): "como una especie de object classifier, que serían los predicados acerca de tipos, con los cuales esos serían las leyes, los nombres." `[00:57]`

### pertenencia-por-construccion-o-hipotesis
- **Qué**: Cómo sabés que un valor pertenece a un tipo: por construcción (el caso está dado) o por hipótesis, una especie de construcción por valor que puede fallar.
- **Cita** (verbatim): "que puede ser por construcción, cuyo caso está dado, digamos, o por hipótesis, que en realidad sería como una especie de construcción por valor, pero que puede fallar" `[01:30]`

### certificacion-probabilistica-de-funciones
- **Qué**: Con funciones no podés probar extensivamente; las probás en una muestra, y ahí entra la probabilidad. No es una certificación sino una probabilidad de cierto éxito.
- **Cita** (verbatim): "no sería una certificación, porque justamente vos no llegarías a una seguridad, sino que sería una probabilidad de tener cierto éxito." `[02:30]`

### parametrizar-leyes-por-entorno-y-costo-de-uso
- **Qué**: Un modificador de los tipos donde las leyes se parametrizan por su entorno numérico de validez (ya implícito en las leyes con reales que tienen bound) y por un "uso": el costo de que la función falle según distintas configuraciones de parámetros.
- **Cita** (verbatim): "pero la idea sería que también se parametrice con una especie de uso, Es decir, qué pasa un costo de si la función falla, por ejemplo" `[03:32]`
- **Ambigüedad / tensión**: dónde muestrear queda abierto: en los lugares de costo mayor, o donde es más probable que falle, o una combinación de ambos.

### poder-escribir-no-resolver-ahora
- **Qué**: Postura de diseño: estas son situaciones hipotéticas que no hay que solucionar ahora; lo importante es tener una forma de expresar las condiciones de uso, el entorno de validez de la ley, las funciones de costo y las de probabilidad.
- **Cita** (verbatim): "esas son todas situaciones hipotéticas que uno no tiene por qué solucionar ahora. Lo importante es poder escribirlas" `[05:35]`

### prior-y-costo-de-falla-como-dos-funciones
- **Qué**: Para un programa, dos funciones sobre los parámetros de la función: un prior (frecuencia o expectativa de encontrarse con esas circunstancias) y un costo de falla.
- **Cita** (verbatim): "la función de frecuencia, de expectativa de encontrarse con esas circunstancias, una especie de prior de esas combinaciones de parámetros y una especie de costo de falla" `[06:53]`
- **Ambigüedad / tensión**: el costo depende también del grado de la falla, porque hay errores más grandes y más chicos.

### funcion-caracterizada-como-expectativa-de-perdidas
- **Qué**: Todo esto se puede pensar como un tipo en sí mismo: un generador de parámetros, un test y un costo; lo que queda de la función es una expectativa de pérdidas, como un parámetro de la función.
- **Cita** (verbatim): "lo que te queda de la función sería una expectativa de pérdidas ponerle o algo así de la función" `[08:16]`
- **Ambigüedad / tensión**: hay que ver cómo tener libertad para que el posterior o la caracterización de esa implementación quede procesable.

### tiempo-de-computo-como-dimension-de-eleccion
- **Qué**: Además del error, el tiempo de cómputo: podés elegir una función más rápida y más chota o más lenta y más segura. Todas resuelven el mismo problema y son valores del mismo tipo de función.
- **Cita** (verbatim): "vos podés elegir una función que sea más rápida y más chota, o más lenta y más segura" `[09:15]`

### mundo-exterior-son-archivos
- **Qué**: Lo que está fuera de Luthier, una manera de pensarlo, son archivos: ejecutables, funciones de Python, datos, plots, incluso sensores. Los archivos son una gran parte del mundo exterior.
- **Cita** (verbatim): "los archivos creo que es una gran parte del mundo exterior" `[10:38]`
- **Ambigüedad / tensión**: pregunta abierta, para hacerle a la guía: "yo no sé si vos tenés alguna abstracción que no sea un file para interactuar, esa es una buena pregunta" `[10:54]`

### recursos-memoria-y-procesadores
- **Qué**: Además de los files, la memoria (variables mutables), los recursos y los procesadores; podés pedir procesadores, memoria. También hacen a la computación.
- **Cita** (verbatim): "tenés files, tenés memoria, tenés recursos y tenés procesadores" `[11:19]`

### idea-central-certificar-lo-que-la-funcion-dice
- **Qué**: Una de las grandes ideas de Luthier: poder escribir qué hace la función, con pos-condiciones y leyes, y después certificar que esas cosas se cumplen.
- **Cita** (verbatim): "vos certifiques que determinada función cumple lo que dice, o sea poder escribir que es lo que la función hace con pos condiciones, con leyes y después certificar que esas cosas se cumplen" `[12:04]`

### declarar-vs-definir-tipos
- **Qué**: Las certificaciones ocurren en el tiempo: primero declarás un tipo (lo enunciás, todavía sin todos sus constraints) y después lo definís.
- **Cita** (verbatim): "vos tenés los tipos que los declarás y después los definís." `[13:09]`
- **Ambigüedad / tensión**: a veces necesitás declarar sin definir para poder definir un tipo recursivamente respecto de otro.

### no-hay-valor-sin-definicion
- **Qué**: Ley propuesta: no podés darle un valor a un tipo que no tiene definición. Y la definición no es la firma (una función de reales en reales) sino las propiedades que tiene esa función.
- **Cita** (verbatim): "vos no le podés dar un valor a un tipo que no tiene una definición." `[13:25]`

### tipos-de-funcion-no-univocos
- **Qué**: El tipo de función no tiene por qué ser único; podés tener muchos tipos de función que se te ocurran (por ejemplo, funciones positivas que van de los reales a los reales positivos).
- **Cita** (verbatim): "no tiene por qué ser única univoca la función, el tipo de función, o sea vos podes tener muchos tipos de función que se te ocurren" `[14:18]`

### leyes-como-funcion-a-booleans
- **Qué**: Las leyes son una función de un tipo a los booleans.
- **Cita** (verbatim): "las leyes en realidad son una función de un tipo a los booleans" `[14:35]`

### leyes-de-costo-en-vez-de-booleanas
- **Qué**: Extender el concepto para que las leyes vayan no a un boolean sino a un costo: leyes de costo graduadas, como una likelihood o probabilidad generalizada sin normalizar, en vez de verdadero/falso.
- **Cita** (verbatim): "leyes de costo, no leyes de que pasa o no pasa, o sea, es verdadera, falsa, sino leyes de costo, que sería como una especie de likelihood" `[15:16]`
- **Ambigüedad / tensión**: no sabe si deben ser positivas o pueden valer cualquier cosa; si valen cualquier cosa se complica todo, así que quizás convenga pensarlas como costos sin bound ("costos sin bound ... eso suena mejor" `[16:37]`).

### costo-de-un-valor-segun-la-ley
- **Qué**: Con leyes de costo, lo que preguntás por un valor no es si cumple o no cumple, sino cuánto te sale esa ley.
- **Cita** (verbatim): "cuál es el costo de este valor, este valor según esta ley no sería si cumple o no cumple, sino cuánto me sale esta ley" `[17:27]`

### parte-declarativa-vs-parte-ejecutiva
- **Qué**: Hay una parte declarativa y una parte ejecutiva; la ejecutiva necesita una especie de run: correr comandos, leer un file, ejecutar una función.
- **Cita** (verbatim): "la parte ejecutiva claramente hay que tener una especie de run, o sea una especie de correme estos comandos, o sea leme este file, ejecutame esta función" `[18:04]`

### ejecucion-como-cambio-del-universo
- **Qué**: Correr una función se modela como algo que cambia los estados del programa y los estados del universo. Los cambios del universo se infieren (escribiste un file, mandaste un mensaje) y también siguen reglas.
- **Cita** (verbatim): "¿Qué cambia? El universo, es decir, cambia los estados del programa y los estados del universo, ¿no es cierto?" `[18:49]`

### programa-agnostico-entre-estado-interno-y-universo
- **Qué**: Cómo distingue el lenguaje los tipos que hablan de estados internos del programa de los que hablan de estados del universo. En principio el programa debería ser agnóstico; no ve por qué habría una distinción en la lógica de una cosa y de la otra.
- **Cita** (verbatim): "En principio, el programa tendría que ser agnóstico de eso. No veo por qué habría una distinción en la lógica de una cosa y de la otra." `[19:42]`

### orden-por-dependencia-de-estados
- **Qué**: Lo que importa es qué acciones dependen de cuáles: hay un orden de ejecución que tiene que ver con la dependencia de estados, un grafo (definir funciones en función de otras genera un grafo).
- **Cita** (verbatim): "hay un orden de ejecución que tiene que ver con la dependencia de estados." `[20:16]`

### simular-el-do-de-haskell-por-dependencia
- **Qué**: El "do" de Haskell (hacer una cosa y después otra) se puede simular como una dependencia input-output: si el input no existe no podés generar el siguiente output. Por eso el do no sería estrictamente necesario.
- **Cita** (verbatim): "ese dude que usan Haskell no sé si sería estrictamente necesario o no" `[21:23]`

### interprete-de-luthier-escrito-en-luthier
- **Qué**: Le gustaría que la implementación del intérprete de Luthier esté escrita en Luthier.
- **Cita** (verbatim): "a mí me gustaría que lo que sea la implementación del intérprete de Luthier sea escrito en Luthier." `[21:33]`

### eager-vs-lazy-cuando-evaluar
- **Qué**: Problema de cuándo evaluar: con A = 2+2, ¿lo guardás como "A = 2+2" o le asignás el valor 4? ¿Cuánto vale A?
- **Cita** (verbatim): "¿cuánto vale A? ¿A vale 2 más 2 o A vale 4? eso es un problema" `[23:16]`

### representacion-de-la-evaluacion-pasos-y-aplicacion-parcial
- **Qué**: Cómo representás la evaluación de una expresión en Luthier. Una forma consume los símbolos con poca memoria (un "más" ya es una función que suma 2 a lo siguiente); otra guarda los tres símbolos y después ejecuta. Los pasos serían el estado de la memoria (un 2, después 2+, después 2+2, después 4), y eso cree que es universal. Dos tipos de cosas: el símbolo + con su 2, o ya una función + rellena del 2 (aplicación parcial), o un puntero a F(A,B).
- **Cita** (verbatim): "serían, digamos, los pasos el estado de la memoria eso creo que es universal" `[26:43]`

### recomputar-desde-la-expresion-guardada
- **Qué**: Guardar la expresión (como string, o como programa a+b) permite recomputar con distintos supuestos: con la misma expresión podés calcular varias cosas distintas (a vale 2, o a vale 2 con un error de tanto).
- **Cita** (verbatim): "yo con la misma expresión puedo calcular varias cosas distintas." `[25:27]`
- **Ambigüedad / tensión**: queda abierto "si tengo que guardar algo intermedio o no".

### errores-de-tipo-y-sintaxis-en-la-interpretacion
- **Qué**: Durante la interpretación chequeás qué es F: si es una función conocida, los rangos (arcoseno entre 0 y 1, si se escapa tira error) y los errores de tipo (arcoseno de un string no puede ser).
- **Cita** (verbatim): "si hago arcoseno de un string no puede ser, por ejemplo, ahí tiene un error" `[28:04]`

### antecedentes-de-interpretes-en-cpp
- **Qué**: Ya desarrolló este tipo de intérprete o compilador en C++, en Macro-IR y en Kimball (guardando en clases virtuales). La pregunta es si tiene sentido hacer algo así en Luthier, que interprete el código y lo vaya generando, porque ahora lo hace en Python.
- **Cita** (verbatim): "la pregunta es tiene sentido hacer algo así en luthier, que vos interpretes el código y lo vayas generando, porque ahora lo que hace es lo hace en Python." `[28:51]`

### leyes-de-cada-paso-de-interpretacion-en-luthier
- **Qué**: Tener las leyes de cada paso de la interpretación (reduce, apply) escritas en Luthier, para poder examinar que las leyes, los preceptos de Luthier, se cumplen. Con apply y reduce cree que tendría casi todo hecho.
- **Cita** (verbatim): "las leyes de eso deberían estar escritas en Luthier así uno puede examinar que las leyes se cumplen básicamente los preceptos de Luthier" `[30:16]`

### posterior-bayesiano-de-cada-calculo
- **Qué**: Con esta lógica "bayesiana", cualquier cálculo que hagas en Luthier va a tener un posterior de qué tan seguro estás de ese cálculo.
- **Cita** (verbatim): "cualquier cálculo que hagas en Luthier va a tener un posterior de que tan seguro estás de ese cálculo" `[30:46]`

### unir-evidencia-de-varios-programas
- **Qué**: Unir distintas evidencias, distintos programas que corren la misma función, para ir refinando la certeza que tenemos en una determinada función.
- **Cita** (verbatim): "distintas evidencias, distintos programas que corren la misma función y ir refinando, digamos, la, ¿cómo se dice? La certeza que tenemos en una determinada función." `[31:17]`

### guardar-testigos-y-valores-informativos
- **Qué**: Como son funciones caras, guardar el testigo de que la función funcionó o falló; y dar prioridad a los valores con mucha información, es decir los inesperados: si tenés un prior de los valores posibles y el resultado sale muy lejos del prior, lo guardás.
- **Cita** (verbatim): "vos tenés un prior de los valores posibles de una función, entonces si él te sale muy lejos del prior vos lo guardás, por ejemplo." `[32:23]`

### analisis-probabilistico-opcional-y-parametrizable
- **Qué**: Todo este aparato encarece mucho el cálculo; es parafernalia por encima. Uno tendría que poder decir que quiere hacer esos análisis solo en algunos momentos, no siempre (por ejemplo, testear cada tanto).
- **Cita** (verbatim): "uno tendría que poder decir, bueno, quiero hacer todos estos análisis por encima, los hago en algunos momentos, no siempre" `[33:03]`
