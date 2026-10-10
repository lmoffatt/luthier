**Archivo:** WhatsApp Ptt 2026-10-10 at 16.49.14.mp3
**Duración:** ~07:09
**Hablante:** Luciano

[00:00] Hay un par de ideas que siempre estuvieron en mi cabeza que no sé si están en los audios.

[00:04] La primera idea muy importante es que uno definir los tipos con predicates.

[00:14] Los predicates, al ser una función que tira un booleano, lo que te genera es,

[00:19] vos podés hacer un cociente, es decir, todos los que siguen el predicate te definen un subconjunto.

[00:29] Tenés una relación de equivalencia.

[00:31] Entonces vos podés juntar a todos los que siguen un predicate

[00:36] y los podés uno reemplazar por el otro.

[00:39] Y ese es el principio con el quotient para separar las implementaciones.

[00:47] Las implementaciones de una función son el quotient sobre el predicate

[00:54] de las leyes de esa función.

[00:57] Y entonces, nada, eso, vos elegís la...

[01:01] Y, digamos, el cogent te da, bueno, una parte y otra parte, ¿no?

[01:06] O sea, que no es el numerador, el denominador, no sé cómo sería.

[01:08] O sea, sería la parte que representa el grupo de equivalencia

[01:13] y después las diferencias.

[01:14] Y las diferencias estarían en, bueno, la velocidad de implementación

[01:18] y, bueno, puede llegar a ser, en algunos casos, el error

[01:21] o lo que carajo sea que caracteriza a las distintas implementaciones.

[01:27] Eso, digamos, es la base un poco de por qué uno podría optimizar con eso.

[01:32] O sea, al tener, digamos, algo que te defina, que te iguala una función,

[01:36] allí estas dos funciones implementan lo mismo, entonces las puedo usar.

[01:39] Después, otra cosa es que vos podés tener funciones que no implementen exactamente lo mismo,

[01:45] pero que sean, digamos, una functor de la otra, una modelo de la otra.

[01:49] Es decir, por ejemplo, que estén en distintos modelos reales,

[01:53] en distintos modelos, una esté sobre listas y otra sobre vectores, no sé.

[01:57] Algo que, digamos, las funciones sean sobre clases diferentes,

[02:03] pero clases que puedan ser isomórficas o no sé,

[02:08] digamos que las puedas, clases que sean equivalentes unas a las otras, ¿no?

[02:16] Entonces, ese es el otro grado de equivalencia.

[02:21] Por ejemplo, una equivalencia puede ser que una son en código Python, la otra en código R.

[02:26] Y vos tenés que pasar de un formato R a un formato Python, por ejemplo.

[02:35] Y ahí podés tener un coste o algo.

[02:37] O sea, tenés que transformar las cosas o pasarlo a un file.

[02:40] Y después de un file, los datos pueden estar representados de distintas maneras.

[02:47] Y esa es otra cosa.

[02:50] la igualdad de los datos

[02:52] son los mismos datos pero están representados de distintas maneras

[02:56] y vos tenés

[02:59] al final las funciones

[03:02] se basan en una representación particular de los datos

[03:06] pero todas

[03:09] de alguna manera modelan la misma función

[03:12] y entonces hay un coste ahí

[03:15] de transformar los datos de un formato al otro

[03:18] esa es otra cosa

[03:20] y la otra cosa que quería decir

[03:23] que ella me olvidé

[03:24] es muy importante

[03:26] una de las cosas que más me preocupaba

[03:29] es este tema de

[03:30] yo tengo toda una función, un código

[03:33] y ese código yo lo puedo hacer

[03:35] para calcular el valor

[03:37] puede ser para calcular el valor con error

[03:39] puede ser para calcular la derivada

[03:41] puede ser para calcular muchas cosas

[03:43] y eso se define cuando yo

[03:46] al último hago el print

[03:47] entonces ahí cuando pido el print

[03:50] pido el print y ahí defino

[03:52] el print de qué, si es de la derivada

[03:54] o de lo que sea

[03:55] o del valor con error y todo

[03:57] entonces ahí digamos yo puedo

[03:59] calcular para atrás

[04:01] qué es lo que

[04:03] quiero también, o sea no solamente

[04:05] defino

[04:07] qué rama

[04:09] está activa del cálculo

[04:11] del DAG, sino que además

[04:13] qué cálculo aplico

[04:15] o sea

[04:15] del que sea

[04:20] que pueden ser

[04:21] distintos cosas

[04:22] eso es, porque digamos

[04:24] que es medio extraño, sería como una especie

[04:28] de contaminación, vos lo

[04:29] tocas y es como una mancha venenosa

[04:31] que va para atrás, vos tocas y decís

[04:33] bueno, esto ahora es derivada

[04:35] y bueno, todo vuelve

[04:36] y todo lo que era

[04:38] un código normal se transforma

[04:41] en un código que calcula la derivada

[04:43] y como es código

[04:45] digamos este eso se puede se puede hacer en principio en vez de declararlo desde movida

[04:53] no desde entrada sino que bueno lo declaras este al final no sé si es una idea digamos una ventaja

[05:01] de esto de forward como que no tenés que crear pues sino la otra cosa que tengo que hacer es bueno

[05:07] tengo toda esta función ahora yo defino esto es este ponele el cálculo con error con la derivada o

[05:14] o con cualquier monad o decoración que yo quiera poner,

[05:20] lo que yo llamaba el parámetro de implementación,

[05:23] o sea, el tipo de implementación de la función.

[05:27] Esa es la ventaja de hacerlo por demanda.

[05:33] Cuando vos demandás, demandás con tus condiciones.

[05:35] Entonces, nada, ahí ya todo quedaría claro.

[05:40] Lo que sí tiene que ser es que, bueno,

[05:42] si vos demandas con ciertas condiciones, vos los parámetros iniciales tenés que poder, digamos,

[05:47] ponerlos con todas las condiciones necesarias, ¿no? Eso no sé, eso habría que ver bien cómo es,

[05:54] porque puede ser que no lo tengas, o sea, si ya es un parámetro, entró como un número real y no

[06:04] tiene error, y bueno, ¿cómo le enchufas el error a eso? Ahí me queda una pequeña duda, ¿no?

[06:11] de cómo es porque la otra es este bueno lo que lo que contamina es el input de entrada no si yo

[06:19] entro que es como si yo entro con una derivada bueno calculo todas derivadas es a todo el código

[06:25] te usa la derivada si yo entro con error se contamina todo con error si entro con con conseguir

[06:33] digamos la con que te copie todo el código de copia todo el código no sé esa es otra manera

[06:42] que sea este pesado con él con el parámetro y la otra es bueno si yo quiero hacer texto

[06:51] y ahí cuando es contest también esté como hago como testeo no nada esta es una pregunta no si

[07:00] si estas decoraciones son forward o backward, y acá estoy un poquito en la duda de cuál de las dos sería mejor,

[07:06] y estaría bueno que lo discutamos con la IA.
