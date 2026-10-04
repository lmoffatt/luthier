**Archivo:** WhatsApp Ptt 2026-10-04 at 10.28.34.mp3
**Duración:** ~24:29
**Hablante:** Luciano

[00:00] Bueno, estoy un poco atascado con Luthier, o sea, atascado en el siguiente sentido, o sea, la computadora, o sea, Cloud me genera todo, código de Luthier, y qué sé yo, pero para mí eso no es código, es como que no está cumpliendo con las normativas reales de Luthier, o quizás sí, eso es lo que yo no entiendo.

[00:25] Entonces, vamos a pensar, o sea, un poco la idea de Luthier es que uno pueda escribir, digamos, que las clases, los tipos, queden definidos por sus, ¿cómo se llama?

[00:41] Invariantes, ¿no? O sea, todos los invariantes que tienen que tener los tipos, incluyendo las funciones, etc.

[00:53] Entonces, una de las cosas es que muchas funciones y tipos van en conjunto, ¿no?

[01:03] O sea, como los objetos matemáticos, como el grupo, por ejemplo, el grupo que vos tenés,

[01:07] o el monoide, poner que es el más simple.

[01:15] Entonces, si vos tenés un objeto matemático, está definido todo junto.

[01:23] O sea, vos no podés definir una parte sola del objeto matemático, salvo que sí lo construyas con un set más cosas, ¿no?

[01:31] Eso pasa.

[01:34] O sea, vos podrías tener, entonces vos podés tener objetos matemáticos que son, digamos,

[01:40] puros en el sentido de que surgen de la nada y otros que se basan en otros objetos, son derivados, ¿no?

[01:50] Por ejemplo, qué sé yo, creo que Z, el objeto, conjuntos es un objeto matemático primitivo, digamos, puro,

[01:59] por llamarlo de alguna manera y quizás, qué sé yo, claro, vas a grupos, vos lo podés

[02:07] definir grupos sobre set o grupos sobre otros objetos matemáticos que no son set.

[02:11] Entonces, claro, vos podés hacer un grupo sobre set o sobre otras cosas, eso lo sabemos

[02:19] de categorías que es así.

[02:25] Pero bueno, vos podés hacer un grupo sobre sets o podés...

[02:30] Claro, eso es una cuestión medio abstracta de si vos necesitas usar set para definirlo o no.

[02:41] Y en principio la idea siempre más genética es hacer lo más general posible, ¿no?

[02:45] Digamos, que vos necesites...

[02:50] O sea, no especializar más de lo que necesitas.

[02:52] o sea que lo único que necesitas probablemente son los operadores lógicos y posiblemente

[02:59] igualdad más que nada creo que igualdad y creo que nada más en el fondo para

[03:10] Bueno, para estudiar categorías necesitas igualdad.

[03:12] Vos podés decir si dos flechas son las mismas o no.

[03:18] Y también, bueno, a veces existe una única, ponen.

[03:24] ¿Existe una única?

[03:29] ¿Qué es eso?

[03:32] ¿Existe una única, no?

[03:33] Flecha.

[03:34] Claro.

[03:40] Bueno, en fin.

[03:41] Sí, igualdad creo que lo necesitas siempre.

[03:44] Me digo que sí.

[03:45] Bueno, no sé.

[03:49] No sé eso si vos podés tener objetos

[03:52] matemáticos sin igualdad.

[03:53] De hecho pasa porque vos no tenés vueltas de reales.

[04:00] Pero bueno, tenés

[04:01] equivalencia.

[04:03] Bueno, entonces, vos ponés que tengas

[04:08] objetos o los reales

[04:10] y claro, y vos haces eso

[04:12] entonces la idea es como que vos

[04:13] yo había llegado un poco a este

[04:16] esquema mental, es que vos

[04:18] digamos las operaciones

[04:19] son en este mundo ideal, sin

[04:21] errores, y después vos las

[04:24] aproximás de alguna manera

[04:26] como por ejemplo, con los números reales

[04:28] los aproximás con floating

[04:30] points

[04:30] entonces la idea es como que vos bajás

[04:34] a una cierta realidad

[04:36] y tenés a lo sumo una cierta

[04:38] garantía de precisión

[04:40] ¿no es cierto? O sea, las leyes no se van a hacer precisas, sino que van a tener una cierta garantía.

[04:49] El tema es que calcular esa garantía puede ser más complejo que calcular el valor en sí.

[04:59] Pero bueno, vos en principio tendrías que poder calcular la garantía y después, bueno,

[05:06] es una cuestión de, vos lo podés reducir, una cuestión de optimización,

[05:10] de ver hasta cuánto vos querés, digamos, el trade-off, la garantía que tenés

[05:19] y los valores que alcanzás, cómo te manejás.

[05:30] Ese creo que sería, digamos, el ideal máximo.

[05:36] Ahora, ¿cuál es la realidad?

[05:39] Yo estaba ahí pensando, bueno, ahora quiero hacer un luthier efectivo que haga algo,

[05:44] por ejemplo, que vos puedas definir en leyes,

[05:51] por ejemplo, que una función sea la inversa de otra o algo así,

[05:59] y ver, digamos, que eso ocurra.

[06:02] Y eso hacerlo, digamos, quizás sin tanto...

[06:10] sin tener que, digamos, definir las invariantes de todos los elementos de un sistema,

[06:22] porque ya eso supuestamente está hecho por el propio software,

[06:26] y bueno, es un poco perder el tiempo.

[06:29] quizá lo sumo, digamos, testear la lógica de lutear, que no estaría mal, en realidad,

[06:37] o sea, uno tendría que testearla para después usarla más, pero bueno, es, digamos, en el orden de cosas,

[06:46] creo que primero conviene, sí, testear lo mínimo posible y después ir avanzando, ¿no es cierto?

[06:58] Bien, entonces ahora pensemos en este asunto de testear.

[07:02] Vamos a pensar con esta table, el concepto de table.

[07:06] Entonces, claro, vos podés testear de dos maneras.

[07:10] Una es, digamos, al estilo de objetos, es decir, vos definís table

[07:18] y hasta que no definís todas las funciones que operan sobre table, las esenciales,

[07:27] vos no cerrás

[07:30] no creás el objeto

[07:32] ahora

[07:34] nosotros acá

[07:35] claro

[07:38] si vos tenés un objeto table

[07:39] que es externo

[07:41] una data frame

[07:44] ponele

[07:45] y bueno

[07:48] table ponele que tenga que tener

[07:50] no sé si número de columna

[07:52] número de filas

[07:53] y algo que te diga

[07:56] el tipo que tiene cada columna y después acceder a los valores de cada columna.

[08:20] sería más o menos así, para cada columna te devuelve un tipo que sería un variante,

[08:28] o sea un tipo suma de los tipos posibles que están contemplados en esta table,

[08:35] la table tiene que estar basada en un número variable de tipos,

[08:43] O podrías pensar sobre una suma de tipos, por ejemplo.

[08:50] Y bueno, entonces lo que haces es, lo que es una suma de tipos es una suma de vectores de tipos.

[09:05] Sería básicamente, los tables es eso.

[09:10] este bueno ese es este pero no la suma de vectores de tipos es digamos es un

[09:17] es eso claro una table si lo vamos a definir más digamos con teoría y categoría sería si o sea

[09:26] vos podés definirlo constructivamente digamos teniendo vector no tenés un vector o list no

[09:40] Entonces, vector sería, claro, es un vector de, es un vector de vectores de suma, no, es

[10:10] ¿Para cómo es este asunto?

[10:13] Claro.

[10:15] Es un vector de la suma de vectores

[10:21] de determinado largo fijo.

[10:28] Eso es una tabla estructuralmente.

[10:34] Y bueno, pues vos lo que tenés, claro, sería una...

[10:50] Bueno, el vector ya tiene el operador índice o no sé, indexat.

[11:03] y después bueno

[11:06] si aplicando dos veces el operador entonces llegas a seleccionar columna y

[11:16] raw

[11:19] si el vector tiene si o sea vos podés definir todo en función de eso

[11:33] ahora

[11:38] ahora eso es una forma

[11:43] pero la table

[11:44] podría hacer que la table

[11:47] digamos

[11:49] en realidad lo que

[11:51] tiene que tener es

[11:53] claro

[11:55] dos operadores

[11:56] es este

[11:57] un operador a determinada columna

[12:01] y un operador a determinada fila

[12:03] y que ahí te devuelva

[12:06] el verdadero de la celda

[12:11] todas esas historietas

[12:12] lo que pasa es que un poco uno se aburre

[12:16] de todas esas cosas que no

[12:17] en realidad no conducen a nada

[12:20] pero de alguna manera es un ejercicio

[12:30] para ver cómo escribir

[12:33] ese es el tema

[12:36] cómo escribo yo

[12:37] la

[12:39] gramática de Luthier

[12:43] para expresar

[12:45] todas las invariantes

[12:48] de los tipos nuevos

[12:49] entonces

[12:51] volvamos a table

[12:53] yo puedo hacer de dos maneras

[12:56] una es

[12:57] yo defino a table

[12:59] junto con todas las funciones que operan sobre Table

[13:06] un poco al estilo objetos

[13:11] entonces me queda Table con la lista de funciones que tiene

[13:19] y la lista de invariantes de esas funciones

[13:23] y eso es una Table

[13:26] y después vos como la definís

[13:30] bueno, la definís con

[13:31] digamos, cada una de

[13:33] de estos elementos

[13:35] o sea, el tipo

[13:38] que tiene y todas las funciones

[13:40] que trabajan sobre ellos

[13:41] claro, esa digamos, como la

[13:50] asignás

[13:51] y entonces

[13:53] y vos eso, le pones un nombre

[13:56] y después vos llamás

[14:00] que se yo

[14:00] te llamas la table

[14:02] de python

[14:04] y te pones

[14:06] y le pones el nombre de fantasía

[14:09] que está en la

[14:10] en la definición

[14:13] de table

[14:14] es muy siguiendo

[14:17] la gramática de objetos

[14:22] de ese más más

[14:25] La otra que se puede hacer es, bueno, yo defino table como un tipo, así como simplemente un puntero al vacío.

[14:35] Después defino todas las funciones, también.

[14:40] Y después defino los constraints, ¿no?

[14:49] Los constraints sobre las funciones.

[14:51] En realidad estoy haciendo lo mismo, lo único que no estoy poniendo donde termina el bloque para asegurarme que tengo una table.

[15:01] Claro, y entonces después cuando yo tengo table, o sea, en el fondo estoy hablando de la misma información,

[15:09] el único tema es que es como una clase abierta, o sea, un objeto, los objetos en cemás más están cerrados

[15:18] en el sentido de que

[15:20] nada, vos los definís

[15:24] y te queda, digamos, todo cerrado

[15:30] y es como

[15:31] es mejor para el cerebro humano

[15:34] en el sentido de que decir, ah, esto es una tecla

[15:36] tiene tal y tal cosa, tal y tal otra

[15:38] en cambio si lo pongo así

[15:40] digamos

[15:41] con

[15:42] digamos

[15:45] definiéndolo

[15:46] primero con el puntero

[15:49] después las funciones

[15:50] que también son punteros

[15:52] funciones que se aplican

[15:54] a este puntero

[15:58] y después

[16:03] defino todas las

[16:06] invariantes

[16:07] pasa que ahí como yo defino

[16:10] que es una invariante, ahí está el tema

[16:12] tengo dos posibilidades

[16:16] además hay otro tema

[16:23] que es que

[16:25] que yo

[16:29] poner que tengo un invariante

[16:31] de que yo la suma es la inversa

[16:33] de la resta

[16:34] no sé, ponerle que

[16:35] no sé, algo así

[16:38] entonces yo tengo que definir ese invariante para suma

[16:40] y para resta, está definiendo dos veces

[16:43] o sea que en realidad

[16:45] la invariante sería para el par

[16:47] pero bueno, yo puedo poner

[16:49] una invariante para el par

[16:52] eso no sería

[16:54] tanto problema

[16:54] las invariantes están definidas para pares

[16:57] el tema también

[17:02] en realidad, a ver si

[17:04] esto un poco tiene sentido

[17:06] es como yo digo

[17:08] que algo es una invariante

[17:10] o que es una función

[17:12] ¿no es cierto?

[17:15] en realidad serían como

[17:19] nada, vos podrías hacer

[17:23] cosas bastante libres

[17:25] como una especie de

[17:27] sintaxis libre

[17:30] que vos vas definiendo

[17:31] distintas invariantes

[17:33] así alegremente

[17:34] y después decís, bueno, ahora yo quiero

[17:37] tal y tal

[17:38] asegurarlas

[17:41] me parece que esa

[17:45] es la lógica que está siguiendo ahora Luthier, digamos, Luthier en su claude. Y en cierto

[17:52] modo no está mal, es bastante expresiva, porque vos expresás las cosas, decís, bueno,

[17:58] ¿qué es una tabla? La tabla es una cosa, bueno, pero yo puedo definir estas cosas sobre

[18:04] tabla y luego defino las invariantes y finalmente bueno, claro el tema es como yo defino ponerle

[18:20] quiero asegurar ciertas cosas, no se digo bueno, claro yo tengo todas esas cosas y después

[18:32] digo bueno ahora yo cuando importo ciertas funciones, claro, el tema es a ver cómo son

[18:42] los tipos acá, porque claro si yo digo que algo es una tabla entonces, es una tabla,

[18:55] o sea, acá digamos esto sirve, o sea, este esquema que está teniendo Luthier sirve para

[19:05] lo que sería hacer test, porque vos testeás cosas alegremente todas independientes una

[19:10] de la otra, la otra cosa es decir, bueno, yo ahora construyo una tabla y ya si construyo

[19:17] una tabla con eso, yo digo, bueno, test, una tabla, entonces tengo la garantía de que

[19:23] yo puedo acceder a toda una serie de métodos, que eso es básicamente, estamos descubriendo

[19:36] la pronunciación de objetos.

[19:49] Si, es básicamente eso. Casero no sería un número por ejemplo, no podes ir por cero.

[20:00] Ahí hay un tema eso, no? Osea, que pasa con las operaciones? No se pueden hacer, bueno

[20:07] no podes hacer, no esta definida, que se yo, tanta cosa no esta definida, osea.

[20:19] Sí, bueno, reales menos el cero más el cero, ¿no?

[20:23] En fin.

[20:25] Claro, son dos tipos, serían reales incluyendo el cero o reales excluyendo el cero.

[20:32] Porque un poco la lógica que yo quería hacer era esa,

[20:45] que yo al definir, digamos, al decir que vos te estás diciendo que algo es de un tipo,

[20:50] vos ya estás garantizando toda una serie de cosas, ¿no es cierto?

[20:56] Ahora, o sea que eso tiene que estar sí o sí asociado con el tipo.

[21:06] Entonces, nada, es como que vos tenés, claro, vos declarás el tipo,

[21:12] vos lo declarás y después lo definís.

[21:14] O sea, claro, y vos cuando lo...

[21:16] Sabés, vos lo declarás.

[21:18] T es universal.

[21:20] Listo. Pero no está definido.

[21:22] Entonces después decís

[21:24] T es igual a

[21:26] qué sé yo,

[21:28] tales características asociativas,

[21:30] qué sé yo, esto, lo otro.

[21:31] Y ahí

[21:34] estaría algo así.

[21:36] Que es una forma

[21:40] más general, además,

[21:42] porque bueno, vos rehusás los conceptos, ¿no es cierto?

[21:45] Que eso es un poco lo que venimos haciendo.

[21:48] Está bien, entonces...

[21:49] Está bien, o sea que, digamos, si vos declaraste U, no lo podés usar U,

[21:58] porque sería como una especie de clase pura que no se puede instanciar, no se puede usar, digamos.

[22:06] ¿Cómo no se puede usar? ¿Qué significaría?

[22:10] Bueno, que no podés usarlas en...

[22:13] No podés declarar, por ejemplo, que una variable es una tabla hasta que vos no hayas...

[22:25] O por lo menos no podés, digamos...

[22:28] Claro, no podrías...

[22:38] Claro, si construir una tabla con el objeto array, ponerle de Python y todas las cosas de Python y que se yo y todas sus funciones, hasta que no esté definido que es una tabla.

[23:01] Entonces vos definís lo mismo con las...

[23:08] Pero entonces ahí vos cuando definís tabla, lo definís tabla junto con todas sus operaciones.

[23:14] Y claro, y vos cuando...

[23:18] Ahí está, ese es el tema.

[23:19] Vos yo ponen que tenga operaciones que sean derivadas.

[23:23] Bueno, sus invariantes van a estar definidas por otras operaciones.

[23:29] esas operaciones tienen que ya estar definidas ahora una circularidad la

[23:42] circularidad de las invariantes que vos tenés dos funciones que vos

[23:49] necesitas una para probar la otra entonces ahí vos necesitas crear las

[23:54] juntas y ahí estás generando un objeto

[23:57] O sea, los objetos son, digamos, son grafos circulares en cuanto a la definición.

[24:06] O sea, son grafos cíclicos.

[24:10] Hay una estructura de grafos cíclicos en su definición.

[24:21] Y esos serían los objetos.

[24:26] Ahí está.
