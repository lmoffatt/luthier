**Archivo:** WhatsApp Ptt 2026-10-10 at 17.25.23.mp3
**Duración:** ~08:03
**Hablante:** Luciano

[00:00] Aquí está el tema de los módulos. Bueno, los módulos representarían justamente teorías matemáticas, como que se llama algebra lineal o reales o, no sé, transformadas de Fourier, no sé cómo llamar los nombres que correspondan,

[00:14] que van a tener, digamos, justamente tipos y funciones, todos con sus leyes bien marcados,

[00:22] todo en teoría ahí, todo definido pero sin valor, y después va a haber implementaciones

[00:31] que en lo posible serán genéricas, usando otros tipos, otros módulos, o sea,

[00:38] usando otros módulos genéricos

[00:40] y así sería

[00:44] todo

[00:46] porque la idea es que

[00:49] como los módulos tendrían

[00:50] una única sintaxis

[00:52] que está dada por

[00:54] justamente cuando vos definís

[00:56] el tipo del módulo

[00:57] definís cómo se llaman las funciones

[01:00] cómo se llaman los tipos, etc.

[01:02] cómo se representan

[01:05] lo que sea

[01:05] y entonces vos

[01:07] nada

[01:08] usás

[01:13] eso, quizás hasta los nombres

[01:16] puedan

[01:16] tratar de que

[01:20] no, podrían ser con puntos

[01:21] le podés poner, qué sé yo, módulo

[01:23] como hace Python

[01:25] que pone np.no sé cuánto

[01:28] y van a tener las funciones de tal librería

[01:30] está bien

[01:32] entonces

[01:33] sería algo así

[01:35] y serían como las librerías de Python o de DR,

[01:39] pero con, digamos, todas leyes,

[01:42] o sea, todas con sus leyes.

[01:44] Por lo cual, digamos, en realidad,

[01:46] el primer trabajo que podría hacer Luthier

[01:49] es agarrar y decirle a la IA,

[01:51] bueno, ahora vos agarrame toda esta librería de Python,

[01:56] de yo DataFrame,

[01:58] y bueno, ahora generame un Luthier

[02:01] que simplemente escriba la función

[02:05] y que ponga, digamos, en el lenguaje de Luthier

[02:08] todas las leyes que cumplen todas las funciones de, qué sé yo,

[02:15] de data frame o de lo que carajo sea.

[02:17] Y bueno, y ahí vas viendo, digamos, ¿no?

[02:21] O sea, como una forma de, digamos, de chupar, digamos,

[02:30] las implementaciones de otros lenguajes,

[02:34] pero ponerlos en un contexto de saber de qué se trata cada cosa.

[02:42] Al tratar de escribir los tésitos, se entiende mejor cada implementación.

[02:48] Que esa sería, digamos, una aplicación de Luthier prácticamente inmediata,

[02:56] por lo menos desde el punto de vista, si se quiere, pedagógico,

[02:59] de entender qué carajo hacen las distintas librerías.

[03:03] O por ejemplo, yo estoy seguro que, yo me acuerdo, no sé, creo que vos podés hacer pivot wide y pivot long, creo, en R, en tdverse.

[03:23] y una no es la inversa de la otra

[03:25] y tendrían que ser una inversa de la otra

[03:27] o tendrían que ser pivot wide

[03:29] seguido compuesto

[03:31] de pivot

[03:32] pivot long, tendrían que darte

[03:35] la identidad y no te da

[03:37] la identidad porque no

[03:38] se te chotea todo

[03:41] y ahí te das cuenta que está mal diseñada

[03:43] la librería para mi gusto

[03:45] en fin

[03:47] bien

[03:53] lo importante es eso

[03:55] que los módulos entonces definen

[03:57] sí, la citaxis

[03:59] el nombre de las funciones

[04:01] y después las implementaciones

[04:03] en general vos vas a hacer

[04:05] un módulo teórico y el módulo

[04:07] de la implementación

[04:08] de una

[04:09] que claro, está bien, a veces puede ser

[04:12] la implementación en Python

[04:14] la implementación en R, qué sé yo, no sé

[04:16] y bueno, después

[04:18] claro, si Python y R vos tenés que pasar

[04:20] de un lado al otro, lo que sea

[04:22] o sé, qué sé yo, lo que carajo sea

[04:25] este

[04:26] ah, y la otra cosa es

[04:30] bueno, cómo va a ser el intérprete

[04:32] de Luthier

[04:35] o sea, la parte de implementación

[04:37] en eso, digamos

[04:40] una fuente de inspiración

[04:42] es mi propia

[04:44] implementación

[04:46] de un lenguaje

[04:49] un DSL que hice

[04:51] en C++, en el programa MacroDR, hay una implementación que usa, bueno,

[04:58] usa clases virtuales y, sí, usa clases virtuales, dos, digamos,

[05:05] una como que se lo llama Compile y otra, no me acuerdo cuánto,

[05:09] que uno lo llama la otra y todo eso.

[05:10] En fin, lo que habría que tener es, digamos, una tabla de,

[05:20] identificadores con las implementaciones de las distintas funciones,

[05:26] que en el caso de Luthier sería básicamente la implementación,

[05:32] es el código Luthier estático de cómo es cada una,

[05:37] y ahí vos lo que tenés que saber es el tipo de salida,

[05:42] porque generalmente lo que necesitas es una función,

[05:46] cuál es el tipo de salida,

[05:49] Y acá hay otro tema que es fundamental, que es el tema del resultado de una función.

[06:02] Porque el resultado de una función, que eso ya lo hablé en otro momento, ¿no?

[06:05] El resultado de seno, que es el seno de un número, es un real entre menos uno y uno, es un real.

[06:19] Bueno, puede ser cualquiera de las cosas, ¿no?

[06:21] Pero entonces ahí vos tenés tres funciones seno

[06:24] definidas por cuál es el valor que toma.

[06:33] Entonces ahí uno podría, ya que hacemos,

[06:36] ahí estoy inventando algo, ¿no?

[06:38] Hacemos implementación por demanda.

[06:43] Vos podrías decir, bueno, yo tomo un,

[06:46] si acá entro con un real, bueno.

[06:48] Entonces el seno me va a instanciar un real.

[06:52] Si entro con un 0,1, bueno, voy a entrar con un 0,1, ¿no?

[06:58] O sea, si tomo un 0,1 como entrada.

[07:00] Es decir, o puedo tomar, digamos, como entrada una función.

[07:07] No, esta función tiene que ser el seno de un ángulo, ponele.

[07:13] Entonces lo que define, digamos, es como que vos no estarías...

[07:20] Una función podría tener multiplicidad de tipos de salida

[07:27] y que el tipo de salida queda definido por el tipo de entrada que es requerido.

[07:36] Esa sería una forma de solucionar este tema.

[07:43] Y claro, vos tendrías como si varias, o sea una función tendría varias salidas.

[07:49] O sea que habría un polimorfismo en las funciones y un polimorfismo en la función de retorno.

[07:53] Fíjate vos que eso lo podés hacer si vos haces ejecución en demanda.
