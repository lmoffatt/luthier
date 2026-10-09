---
audio: WhatsApp Ptt 2026-10-04 at 10.28.34.mp3
fecha: 2026-10-04
duracion: ~24:29
ideas: 19
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### codigo-generado-no-es-luthier
- **Qué**: Está atascado porque Claude le genera código de Luthier, pero para él eso no es código, no cumple las normativas reales de Luthier; y no sabe si en el fondo las cumple o no.
- **Cita** (verbatim): "Cloud me genera todo, código de Luthier... pero para mí eso no es código, es como que no está cumpliendo con las normativas reales de Luthier, o quizás sí, eso es lo que yo no entiendo." `[00:08]`
- **Ambigüedad / tensión**: queda sin resolver qué distingue el código genuino de Luthier del que solo lo parece.

### tipos-definidos-por-invariantes
- **Qué**: La idea de Luthier es que las clases y los tipos queden definidos por sus invariantes, incluyendo las funciones.
- **Cita** (verbatim): "la idea de Luthier es que uno pueda escribir... que las clases, los tipos, queden definidos por sus... invariantes... todos los invariantes que tienen que tener los tipos, incluyendo las funciones" `[00:41]`

### objeto-matematico-definido-en-conjunto
- **Qué**: Muchas funciones y tipos van en conjunto, como los objetos matemáticos (grupo, monoide): el objeto está definido todo junto y no se puede definir una parte sola.
- **Cita** (verbatim): "si vos tenés un objeto matemático, está definido todo junto... vos no podés definir una parte sola del objeto matemático, salvo que sí lo construyas con un set más cosas" `[01:15]`

### objetos-puros-vs-derivados
- **Qué**: Hay objetos matemáticos puros, que surgen de la nada (primitivos, como el conjunto/Z), y otros derivados que se basan en otros objetos (grupos sobre sets o sobre otras cosas, como se sabe de categorías).
- **Cita** (verbatim): "podés tener objetos matemáticos que son... puros en el sentido de que surgen de la nada y otros que se basan en otros objetos, son derivados" `[01:34]`
- **Ambigüedad / tensión**: deja abierto si hace falta usar set para definir un grupo o no ("una cuestión medio abstracta de si vos necesitas usar set para definirlo o no").

### minimalismo-de-primitivas
- **Qué**: Hacer lo más general posible, no especializar más de lo necesario; lo único que se necesitaría son los operadores lógicos y la igualdad. Para estudiar categorías hace falta igualdad.
- **Cita** (verbatim): "no especializar más de lo que necesitas... lo único que necesitas probablemente son los operadores lógicos y posiblemente igualdad" `[02:52]`
- **Ambigüedad / tensión**: además de la igualdad agrega la "existencia de una única (flecha)" `[03:18]` como algo también necesario, sin integrarlo a la lista mínima.

### objetos-sin-igualdad
- **Qué**: Pregunta abierta de si puede haber objetos matemáticos sin igualdad; con los reales no tenés igualdad pero tenés equivalencia.
- **Cita** (verbatim): "No sé eso si vos podés tener objetos matemáticos sin igualdad... Pero bueno, tenés equivalencia." `[03:49]`
- **Ambigüedad / tensión**: sin resolver; igualdad vs equivalencia.

### operaciones-ideales-y-su-aproximacion
- **Qué**: Las operaciones viven en un mundo ideal sin errores y después se aproximan en la realidad (los reales con floating points); bajás a una cierta realidad con una garantía de precisión, las leyes no son exactas sino que tienen garantía.
- **Cita** (verbatim): "las operaciones son en este mundo ideal, sin errores, y después vos las aproximás... con los números reales los aproximás con floating points... tenés a lo sumo una cierta garantía de precisión" `[04:19]`
- **Ambigüedad / tensión**: calcular la garantía puede ser más complejo que calcular el valor mismo; se vuelve una cuestión de optimización, un trade-off entre la garantía y los valores que alcanzás.

### luthier-efectivo-testeo-minimo
- **Qué**: Quiere un Luthier efectivo que haga algo, por ejemplo definir en leyes que una función es la inversa de otra y ver que eso ocurra, sin tener que definir las invariantes de todos los elementos del sistema; testear lo mínimo posible e ir avanzando.
- **Cita** (verbatim): "ahora quiero hacer un luthier efectivo que haga algo, por ejemplo, que vos puedas definir en leyes... que una función sea la inversa de otra o algo así, y ver... que eso ocurra" `[05:39]`

### table-como-ejercicio-de-gramatica
- **Qué**: El ejercicio de la table, aunque aburrido y que no conduce a nada, sirve para ver cómo escribir la gramática de Luthier que exprese todas las invariantes de los tipos nuevos.
- **Cita** (verbatim): "cómo escribo yo la gramática de Luthier para expresar todas las invariantes de los tipos nuevos" `[12:39]`

### definicion-estructural-de-table
- **Qué**: Estructuralmente una table es un vector de la suma de vectores de determinado largo fijo; el vector ya trae el operador índice y aplicándolo dos veces seleccionás columna y fila. Por columna devuelve un tipo que es una suma (variante) de los tipos posibles.
- **Cita** (verbatim): "Es un vector de la suma de vectores de determinado largo fijo. Eso es una tabla estructuralmente." `[10:15]`

### table-por-dos-operadores
- **Qué**: Alternativamente, la table lo que tiene que tener son dos operadores: uno a determinada columna y otro a determinada fila, que devuelven el valor de la celda.
- **Cita** (verbatim): "dos operadores... un operador a determinada columna y un operador a determinada fila y que ahí te devuelva el verdadero de la celda" `[11:55]`
- **Ambigüedad / tensión**: convive con la definición estructural (vector de la suma de vectores); no elige entre las dos.

### clase-cerrada-vs-abierta
- **Qué**: Dos maneras de definir un tipo. Cerrada, al estilo objetos de C++: definís table junto con todas sus funciones e invariantes, y el bloque cierra el objeto. Abierta: definís table como un puntero al vacío, luego las funciones, luego los constraints, sin marcar dónde termina el bloque; es la misma información, pero como una clase abierta.
- **Cita** (verbatim): "yo defino table como un tipo, así como simplemente un puntero al vacío. Después defino todas las funciones... Y después defino los constraints... En realidad estoy haciendo lo mismo, lo único que no estoy poniendo donde termina el bloque para asegurarme que tengo una table." `[14:25]`
- **Ambigüedad / tensión**: la cerrada es "mejor para el cerebro humano", la abierta es más expresiva; no decide cuál.

### invariantes-sobre-pares
- **Qué**: Una invariante como "la suma es la inversa de la resta" quedaría definida dos veces (para suma y para resta); en realidad la invariante es para el par, así que las invariantes se definen sobre pares.
- **Cita** (verbatim): "la invariante sería para el par... las invariantes están definidas para pares" `[16:52]`

### sintaxis-libre-invariante-vs-funcion
- **Qué**: Con una especie de sintaxis libre vas definiendo distintas invariantes alegremente y después decís cuáles querés asegurar; es la lógica que sigue hoy Luthier en Claude, y es bastante expresiva.
- **Cita** (verbatim): "una especie de sintaxis libre que vos vas definiendo distintas invariantes así alegremente y después decís, bueno, ahora yo quiero... asegurarlas" `[17:27]`
- **Ambigüedad / tensión**: cómo decir que algo es una invariante o que es una función ("tengo dos posibilidades"), sin resolver.

### tipo-como-garantia
- **Qué**: Al decir que algo es de un tipo ya garantizás toda una serie de cosas; construir una table te da la garantía de acceder a una serie de métodos. Observa que así están redescubriendo los objetos.
- **Cita** (verbatim): "al decir que vos te estás diciendo que algo es de un tipo, vos ya estás garantizando toda una serie de cosas... eso tiene que estar sí o sí asociado con el tipo" `[20:45]`

### tipos-tallados-por-operaciones-definidas
- **Qué**: Los tipos se distinguen por qué operaciones están definidas sobre ellos: el cero no es un número con el que puedas dividir, así que serían dos tipos, reales incluyendo el cero y reales excluyendo el cero.
- **Cita** (verbatim): "son dos tipos, serían reales incluyendo el cero o reales excluyendo el cero" `[20:25]`
- **Ambigüedad / tensión**: qué pasa con las operaciones no definidas queda abierto ("¿qué pasa con las operaciones? No se pueden hacer... no está definida").

### declarar-y-despues-definir
- **Qué**: Primero declarás el tipo (T es universal, pero no está definido) y después lo definís (T es igual a tales características asociativas); es una forma más general porque reusás los conceptos.
- **Cita** (verbatim): "vos declarás el tipo, vos lo declarás y después lo definís... T es universal. Listo. Pero no está definido. Entonces después decís T es igual a... tales características asociativas" `[21:12]`

### tipo-declarado-no-usable
- **Qué**: Un tipo solo declarado (U) no se puede usar: sería como una clase pura que no se puede instanciar; no podés declarar que una variable es una table hasta que no esté definido qué es una table.
- **Cita** (verbatim): "si vos declaraste U, no lo podés usar U, porque sería como una especie de clase pura que no se puede instanciar, no se puede usar" `[21:49]`
- **Ambigüedad / tensión**: él mismo se pregunta qué significa "no se puede usar" ("¿Cómo no se puede usar? ¿Qué significaría?").

### objetos-como-grafos-ciclicos
- **Qué**: Cuando dos funciones se necesitan mutuamente (una para probar la otra), hay que crearlas juntas, y ahí se genera un objeto; los objetos son grafos cíclicos en su definición.
- **Cita** (verbatim): "los objetos son, digamos, son grafos circulares en cuanto a la definición... Hay una estructura de grafos cíclicos en su definición. Y esos serían los objetos." `[23:57]`
