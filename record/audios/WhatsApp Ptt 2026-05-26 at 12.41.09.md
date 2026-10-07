**Archivo:** WhatsApp Ptt 2026-05-26 at 12.41.09.mp3
**Duración:** ~04:53
**Hablante:** Luciano

[00:00] La IA me pregunta cuál sería el lenguaje, lo inicial, ¿no es cierto?, para esto.

[00:06] Porque dice, claro, lo más difícil es cómo vos evaluás la complejidad a priori de distintas cosas, ¿no?

[00:14] Y bueno, y eso, sí, obviamente es un problema abierto, re difícil,

[00:21] pero bueno, vos obviamente podés, para eso aplicar, digamos, una estrategia bayesiana de...

[00:28] Y decir, bueno, no sé, puede ser cualquiera y bueno, voy dándole oportunidad a distintos algoritmos para hacer lo mismo y después voy estimando los tiempos que toman para problemas parecidos a partir de la experiencia, de correrlos efectivamente.

[00:52] O sea, que al principio sería como una especie de, digamos, Luthier funcionaría.

[01:06] O sea, lo que tendría que tener Luthier justamente es una base de datos, de alguna manera,

[01:15] sería como una base de datos

[01:16] que dice, bueno, yo

[01:19] para este tipo

[01:21] para esta función

[01:22] con estos datos iniciales

[01:24] y esta escala

[01:26] yo usando

[01:29] este algoritmo tardé tanto tiempo

[01:30] y tuve tanta precisión

[01:32] y como lo sé, bueno, pues lo corrí

[01:34] o sea, lo medí, efectivamente

[01:36] entonces, claro

[01:37] después vas ahí teniendo una base

[01:41] de datos, entonces, claro, después

[01:42] esa base de datos después la tenés que poder generalizar.

[01:49] Entonces ahí una de las herramientas primeras sería cómo generalizar, digamos,

[01:57] los datos que vas obteniendo con casos puntuales.

[02:03] Vas a tener una matriz y, bueno, de esa matriz vas viendo las tendencias en general.

[02:11] Y ahí ya no sé, ahí estoy un poco en pelotas en el sentido de cómo hacerlo efectivamente.

[02:16] Pero uno podría empezar a decir, bueno, mi matriz son las celdas, ¿no?

[02:22] Yo para cada celda es independiente y bueno, ya está.

[02:25] Pero bueno, si en realidad yo tengo la media de los rows y las columnas,

[02:32] bueno, podría estimar una celda por el promedio de la row y la columna

[02:39] o digamos

[02:40] una cosa un poco más sofisticada

[02:43] donde si las dos

[02:45] son

[02:46] importantes puedo

[02:48] sí, no sé

[02:53] moderarlo de alguna manera

[02:56] el tema es que sí, claramente vos tenés que

[02:59] modelar el funcionamiento

[03:01] de cada una de estas cosas

[03:03] y bueno, ahí es donde

[03:05] empieza a ver

[03:07] funciones que son las funciones de modelado de esto que también las vas a utilizar o sea la idea

[03:14] es que vos lo utilizas las funciones de estimación de la el tiempo de cómputo de la precisión de

[03:25] cómputo con la idea de que muchos digamos o sea no tenéis que hacer un cómputo para calcular cuánto

[03:34] tiempo tarda o sea quizás muchos cómputos parecidos pertenecen a la misma misma clase de cómputos es

[03:43] decir que digamos o sea lo que habría que empezar a encontrar es eso no las las categorías de así

[03:55] Así como tenemos distintas funciones que hacen lo mismo, tendríamos distintas computaciones

[04:05] que tardarían lo mismo para distintos inputs.

[04:11] También puede ser que hay funciones que son independientes de los inputs, por ejemplo.

[04:16] Otras, pero cuando dependen de los inputs, obviamente.

[04:20] ahí vos ves qué características de los inputs son las que son los más predictivos.

[04:26] Entonces vos lo que tendrías que tener es vos tenés, digamos, una simplificación de los inputs

[04:34] que ahí vos lo computás.

[04:37] O sea, vos computás el tiempo de cálculo a partir de una simplificación de los inputs.

[04:41] Podría ser, por ejemplo, las dimensiones, el número de columnas y Rho de una matriz,

[04:48] pero puede ser en otros casos otro tipo de cosas.
