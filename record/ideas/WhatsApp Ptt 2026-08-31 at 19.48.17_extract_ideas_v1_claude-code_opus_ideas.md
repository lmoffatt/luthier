---
audio: WhatsApp Ptt 2026-08-31 at 19.48.17.mp3
fecha: 2026-08-31
duracion: ~12:07
ideas: 18
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### tipos-como-proposiciones
- **Qué**: El código tiene significado; pertenecer a un tipo equivale a afirmar una proposición. Es el origen conceptual de Luthier.
- **Cita** (verbatim): "la idea era originalmente que el código son, digamos, tiene significado, es decir, que pertenecer a un tipo, digamos, significa afirmar una proposición" `[01:02]`

### functor-olvido
- **Qué**: Mecanismo de ir olvidando información para que las anotaciones no crezcan al infinito. El autor dice haber llegado a este concepto a través de Luthier ("al Funtor Olvido llegué por Luthier" `[01:42]`).
- **Cita** (verbatim): "tengo el functor olvido que sería, me voy olvidando algunas cosas, porque si no la cosa crece al infinito" `[03:18]`
- **Ambigüedad / tensión**: no define criterio de qué se olvida ni cuándo; más adelante menciona "los distintos functores de olvido" `[10:28]` como algo a explorar.

### codigo-que-guarda-los-calculos
- **Qué**: Tener un código que representa los cálculos habilita autodiferenciación, tomar notas y obtener el resultado escrito paso por paso.
- **Cita** (verbatim): "tengo un código que representa los cálculos y entonces yo ahí lo puedo autodiferenciar, puedo por ejemplo tomar notas, puedo hacer que el cálculo me dé un resultado, digamos, escrito paso por paso" `[02:02]`

### gestion-del-error-como-garantia
- **Qué**: Uno de los propósitos de Luthier: mejor gestión del error y cosas garantizadas, porque tener una clase implica cumplir ciertas proposiciones.
- **Cita** (verbatim): "la idea de Luthier es que la gestión del error sea mejor... que las cosas estén garantizadas... si vos tenés una clase de algo, entonces significa que cumple ciertas proposiciones" `[02:35]`

### anotacion-de-lo-conocido
- **Qué**: Un valor o resultado de cálculo debería llevar algún tipo de anotación con todo lo que ya se sabe de su clase.
- **Cita** (verbatim): "tendría que tener algún tipo de anotación, digamos, de todas las cosas que ya sabemos de esta clase, de este valor, el resultado de un cálculo" `[03:09]`

### especificidad-de-la-operacion
- **Qué**: Un valor sabe por qué operación concreta se produjo; si fue la suma, es la suma, y no la operación genérica de un magma.
- **Cita** (verbatim): "si es la suma, ya es la suma y no es el magma, es la suma, no es la operación y el magma" `[03:50]`

### niveles-de-una-operacion
- **Qué**: De una serie de operaciones se pueden tomar distintas vistas o niveles: el magma, el resultado, la ejecución, el código.
- **Cita** (verbatim): "esas operaciones vos podés tomar el magma, podés tomar el resultado, ejecución, el código" `[04:15]`
- **Ambigüedad / tensión**: qué son y cómo se distinguen esos niveles queda sin precisar ("no sé cómo distintas serían operaciones sobre un código" `[04:23]`).

### htt-inspiracion-la-definicion-genera-el-test
- **Qué**: Luthier como lenguaje inspirado en homotopy type theory, donde al definir una función queda ya definido el test sobre esa función.
- **Cita** (verbatim): "un lenguaje que sea inspirado por los homeotopy type theory, en el cual vos definas una función y que al definir la función ya con eso quede definido el test sobre esa función" `[05:04]`

### niveles-de-verificacion
- **Qué**: Leitmotiv de definir la likelihood y que eso genere un test; el valor puede estar sin testear o testeado, con distintos niveles de verificación.
- **Cita** (verbatim): "vos lo podes tener sin testear, testeado, qué sé yo. Y hay distintos niveles de verificación de las cosas" `[05:56]`

### velocidad-del-codigo
- **Qué**: El tema de la velocidad del código como una de las preocupaciones de Luthier.
- **Cita** (verbatim): "También tenía el tema de la velocidad, el código" `[06:06]`
- **Ambigüedad / tensión**: aparece mencionado al pasar y no se desarrolla.

### luthierizar-codigo-ajeno
- **Qué**: Luthier como anotador de código: se podría "luthierizar" código ajeno de Python (p. ej. tres o cuatro librerías de inversión de matriz), partiendo de la definición de qué es una inversión y qué propiedad debe cumplir.
- **Cita** (verbatim): "La idea es que Luthier sea como un anotador de código. Vos podrías luthierizar, por ejemplo, un código ajeno" `[06:11]`

### propiedades-dentro-de-cierto-error
- **Qué**: Las propiedades (p. ej. que la inversa recupere el valor) se cumplen solo dentro de cierto error, porque muchas funciones inversas no son perfectas.
- **Cita** (verbatim): "dentro de cierto error, porque bueno no es perfecta la inversa... por ejemplo el seno y el arcoseno no te da el mismo valor, perdés un pendejésimo por ahí" `[06:41]`

### dato-con-error-intervalo-o-sample
- **Qué**: Un valor puede en realidad ser un intervalo de valores, o una sample de valores (por ejemplo una cadena de Markov representada por una sample).
- **Cita** (verbatim): "el valor es un intervalo de valores... o puede ser que sea por ejemplo una sample de valores, en el caso de que sea una cadena de Markov, vos podes representarla con una sample" `[07:10]`

### precision-segun-cuanto-recuerdes
- **Qué**: La precisión recuperable depende de cuánto de la historia operacional se conserva: si recordás que tomaste el seno de 4, el arcoseno devuelve 4 exacto; si olvidás la operación, queda un valor con intervalo y se pierde precisión. Liga el functor olvido a la precisión numérica.
- **Cita** (verbatim): "si vos te acordás que tomaste el seno de 4... El arcoseno de seno es 4, chao. En cambio, si... te olvidás de la operación que hiciste... es un valor con un intervalo y ahora tomo la inversa y... yo ahí perdí un poco de precisión" `[08:07]`

### floating-point-no-cumple-las-leyes-el-codigo-si
- **Qué**: Los floating points no cumplen las reglas algebraicas (asociatividad), pero el código sí se supone que las cumple, y por eso se lo puede reorganizar para que la ejecución sea más eficiente o más perfecta.
- **Cita** (verbatim): "los números floating points, que no siguen las reglas, digamos, de los números, no se han asociado... No las siguen, pero sí las siguen, digamos, lo que sería el código... vos suponés que el código sí la sigue, de lo reorganizadas de tal manera de que... la ejecución sea más eficiente o más perfecta" `[08:42]`

### ejecucion-como-generacion-y-olvido
- **Qué**: Código que genera código: ejecutar es transcribir código o ejecutarlo, con dos niveles de ejecución, uno que guarda el código generado y otro que lo olvida. También lo formula como "la ejecución como una función olvido" `[09:09]`.
- **Cita** (verbatim): "es código que genera código, que vos al ejecutar código lo que haces es transcribís código o ejecutás, y claro, como dos niveles de ejecución, una ejecución que guardás el código y otra que, digamos, eso lo olvidás" `[09:56]`

### autoverificacion-inversa-y-test-es-codigo
- **Qué**: Luthier como autoverificación: no se puede definir una función sin su inversa y su test, y el test es el propio código, de modo que correr el código corre también el test (a un determinado nivel, `[11:34]`).
- **Cita** (verbatim): "Luthier sería como una autoverificación del código, o sea que vos no podés definir una función sin su inversa y su test... y que el test sea el propio código entonces vos corre el código y... correr el test también sobre el código" `[11:13]`

### proposito-abierto
- **Qué**: Tensión sobre para qué sirve Luthier y si simplifica macro IR; el autor lo enmarca como aventura intelectual sin objetivo claro todavía.
- **Cita** (verbatim): "hasta ahora es como una aventura intelectual más que nada" `[10:49]`
- **Ambigüedad / tensión**: recurre a lo largo del audio ("qué realmente me serviría para simplificar macro IR" `[04:55]`); queda sin resolver, pendiente de "ir destilando las cosas que tiene que tener Luthier" `[12:02]`.
