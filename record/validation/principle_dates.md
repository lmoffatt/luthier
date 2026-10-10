# Dates of the principles, for Luciano to mark

Written by `scripts/principle_dates.py` (principle_dates v1), no model. Times in UTC. `explicit` is the earliest source of the
principle's entry in record/principles.md; an earlier row of his is listed when it shares terms with the principle, for
you to say whether it already decides (D1). `operative` is the first commit putting the principle's id in that
repository's CLAUDE.md, the first write of ~/.claude/CLAUDE.md carrying its statement, and the memory notes that may
state it (candidates, by shared terms).

How to mark, under each principle, on its `Mark:` line, separated by `;`:
`ok` (the explicit date as proposed, no memory note counts); `earlier <row id>` (that earlier row of yours already
decides, so the principle counts from it); `memory <note.md>` (that note states the principle; it counts from the time
it was first written, in the repository it is listed under). Example: `earlier day:2026-10-04:x; memory nunca-hardcodear.md`.

## P1 Luciano's part stays discernible.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:74 2026-10-06T06:39Z)
  - earlier? 2026-10-05T09:21:01Z `dialogue:aa680014:python-del-proyecto-solo-externs`: "la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern" No, esta es otra idea, es que luthier sirva de un orquestador con testing
  - earlier? 2026-10-05T09:21:01Z `dialogue:ba3fd298:sin-python-del-proyecto-salvo-externs`: "la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern / no estaremos haciendo parches no?" idem arriba
  - earlier? 2026-10-05T09:21:01Z `dialogue:c7437496:no-python-de-proyecto-salvo-externs`: "la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern\nno estaremos haciendo parches no?" misma idea de antes
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 6 shared terms)
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 5 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 4 shared terms)
  - memory? `sonolocalizacion-encuadre-estrategico.md` of account 1, first written 2026-09-09T15:57Z (chat:b66f1892:66, 3 shared terms)
  - memory? `luthier-objeto-matematico-como-invariante.md` of account 1, first written 2026-10-05T03:38Z (chat:52d3e68e:2805, 3 shared terms)

Mark: esta idea no representa que se discerne la parte humana de la agentica, sino que luthier sea una forma de escribir scripts que sean semanticamente autocontenidos y autotesteabless

## P2 Everything derived carries how it was derived.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:96 2026-10-06T06:39Z)
  - earlier? 2026-06-05T16:14:19Z `day:2026-06-05:code-as-data-same-treatment-as-records`: "Las funciones como datos, o sea, el código como datos. entonces sí podés tener también lo mismo, ¿no?" no es que los datos indiquen de donde provienen, sino que al ser el codigo como datos, podes modificar el codigo como se modifican datos. 
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 6 shared terms)
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 5 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f

Mark: 

## P3 Keep the original evidence and its corrections; put the best reading in front.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:61 2026-10-06T06:39Z)
  - earlier? 2026-10-05T03:26:50Z `dialogue:88936d99:un-concepto-un-nombre`: "el principio es no declarar lo mismo con dos nombres distintos"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf si, pero no incluye la parte del best reading at front
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 6 shared terms)
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f

Mark: 

## P4 Decisions follow guiding principles, found as the work goes, which give them one coherent direction toward the objectives of the project.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:234 2026-10-06T06:39Z; luthier@efd8143:docs/plan-working-method-2026-10-06.md:255 2026-10-06T08:07Z)
  - earlier? 2026-10-05T09:21:01Z `dialogue:ba3fd298:sin-python-del-proyecto-salvo-externs`: "la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern / no estaremos haciendo parches no?"
  - earlier? 2026-10-05T09:21:01Z `dialogue:c7437496:no-python-de-proyecto-salvo-externs`: "la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern\nno estaremos haciendo parches no?"
  - earlier? 2026-10-05T09:21:01Z `dialogue:aa680014:python-del-proyecto-solo-externs`: "la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 12 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 11 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 9 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 17 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 11 shared terms)
  - memory? `experimento-cero-equipamiento.md` of account 1, first written 2026-09-01T18:12Z (chat:93ba9996:197, 6 shared terms)

Mark: 

## P5 A free choice is a legitimate principle, for Luciano and, within margins, for a model.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:235 2026-10-06T06:39Z)
  - earlier? 2026-10-06T04:28:56Z `dialogue:ba3fd298:types-testing-optimization-as-one`: "juntas testing y tipos en una sola cosa y tambien ... la optimizacion porque si vos tenes un conjunto de implementaciones {f} de F, ejegis la f mas rapida para tu caso particular. Y eso se guarda tamb"
  - earlier? 2026-05-29T17:46:56Z `dialogue:20260529T1400:expresividad-sobre-redundancia`: "si vas a ser más redundante o expresivo ... en lo expresivo digamos, garpa más porque puede ser que lo redundante sea incómodo a veces y te limite al pedo"
  - earlier? 2026-09-30T03:50:20Z `dialogue:890a551c:tipos-semanticos-error-arbol-recursivo`: "Yo creo que los tipos deben ser semanticos es decir definidos por un numero o etiqueta y manteniendo una estructura comun. Porque en definitiva va a ser una predicado que falla y eso se puede represen"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 7 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 5 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 4 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 9 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 7 shared terms)
  - memory? `luthierizacion-estado.md` of account 1, first written 2026-09-30T13:32Z (chat:1e377538:284, 5 shared terms)

Mark: 

## P6 Every change can be undone.

- explicit: 2026-10-06T06:18Z (chat:7217f251:196 2026-10-06T06:18Z)
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 7 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 4 shared terms)
  - memory? `feedback-numbered-references.md` of account 1, first written 2026-10-06T07:19Z (chat:7217f251:460, 4 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 8 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 8 shared terms)
  - memory? `definir-simbolos-en-cada-formula.md` of account 1, first written 2026-09-11T15:37Z (chat:68ab54e1:94, 5 shared terms)

Mark: 

## P7 Each repository is self-contained.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:303 2026-10-06T06:39Z)
  - earlier? 2022-08-03T14:56:18Z `written:2022-08-03_haskell:proposicion-que-cada-tipo-cumple`: "poder indicar en cada tipo (no distingo entre tipo y funcion) cual es la proposicion que cumple. Aqui hay dos versiones: una computacional y otra escrita. La idea es que la escrita sea derivada de la "
  - earlier? 2023-02-22T19:12:49Z `written:2023-02-22_tapp-wish-list:aprender-de-cada-corrida`: "La idea es que de cada corrida del codigo algo se aprende, ya sea se sabe que una implementacion es correcta ya que se mide su velocidad."
  - earlier? 2026-05-30T21:07:38Z `note:2026-05-30T18.05.22:hott-como-espacio-donde-aplican-probabilidades`: "Son Metrópita y Teori te dan los puntos del espacio, los conjuntos donde aplicas las probabilidades. Sería una cosa así."
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 5 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 9 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 6 shared terms)
  - memory? `nunca-hardcodear.md` of account 1, first written 2026-09-10T22:30Z (chat:b66f1892:1030, 3 shared terms)

Mark: 

## P8 No more bureaucracy than it pays for.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:306 2026-10-06T06:39Z; luthier@efd8143:docs/plan-working-method-2026-10-06.md:295 2026-10-06T08:07Z)
  - earlier? 2026-05-30T21:10:50Z `note:2026-05-30T18.09.57:no-ejecutar-hasta-definido`: "vos no ejecutás el código hasta que no está definido. Entonces es como que, digamos, vos podés tener un montón de código muerto que no jode a nadie porque no está completamente definido."
  - earlier? 2022-07-05T10:53:28Z `written:2022-07-05_sin-titulo-2:environment-ejecuta-funciones`: "el environment tambien debe manejar 1\) la ejecución de funciones para generar nuevas variables."
  - earlier? 2022-08-03T14:56:18Z `written:2022-08-03_haskell:proceso-de-creacion-de-tipos-programable`: "Yo lo que quiero hacer es que el proceso (2) pueda ser programable, es decir que el lenguaje se pueda escribir a sí mismo. Para lograr esto, el lenguaje debe ser simple y robusto no tener sintactic su"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 6 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 9 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 7 shared terms)
  - memory? `experimento-cero-equipamiento.md` of account 1, first written 2026-09-01T18:12Z (chat:93ba9996:197, 4 shared terms)

Mark: 

## P9 What Luciano hasn't fully understood may come in, contained.

- explicit: 2026-10-06T06:39Z (luthier@2a660c8:docs/working-method.md:110 2026-10-06T06:39Z; luthier@efd8143:docs/plan-working-method-2026-10-06.md:304 2026-10-06T08:07Z)
  - earlier? 2026-09-30T10:54:02Z `dialogue:890a551c:disaggregate-prelude`: "no me gusta prelude. me parece que deberia ser disgregado en sus componentes y que todo vaya a examples quizas? o hay algo fundamental? yo creo que sonolocalization no va a usar nada de esto no?"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 8 shared terms)
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 4 shared terms)

Mark: 

## P10 The mathematical object that best represents a concept is the invariant of its type.

- explicit: 2026-10-05T03:35Z (chat:52d3e68e:2760 2026-10-05T03:35Z; chat:52d3e68e:2772 2026-10-05T03:35Z)
  - earlier? 2026-10-04T23:32:58Z `dialogue:52d3e68e:choose-best-math-object-for-r`: "No tiene sentido reescribir la aritmetica pero si usamos algebra podemos elegir el objeto matematico que mejor representa a R"
  - earlier? 2026-10-04T23:32:58Z `dialogue:88936d99:choose-best-math-object-for-r-via-algebra`: "No tiene sentido reescribir la aritmetica pero si usamos algebra podemos elegir el objeto matematico que mejor representa a R"
  - earlier? 2023-02-22T19:12:49Z `written:2023-02-22_tapp-wish-list:definir-funciones-en-grupo`: "Esto hace que muchas funciones se deban definir en grupo ya que las postcondiciones involucran a varias funciones a la vez (como leer y escribir o las operaciones en un objeto matematico como un grupo"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 8 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 4 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `luthier-objeto-matematico-como-invariante.md` of account 1, first written 2026-10-05T03:38Z (chat:52d3e68e:2805, 11 shared terms)
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 5 shared terms)
  - memory? `luthier-estado-2026-10-05.md` of account 1, first written 2026-10-05T06:57Z (chat:52d3e68e:3667, 4 shared terms)

Mark: 

## P11 Every criterion is a parameter, never a constant in the code.

- explicit: 2026-09-10T22:20Z (chat:6878a98d:1148 2026-09-10T22:20Z; chat:6878a98d:1175 2026-09-10T22:29Z)
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 6 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 4 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 3 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 9 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 8 shared terms)
  - memory? `nunca-hardcodear.md` of account 1, first written 2026-09-10T22:30Z (chat:b66f1892:1030, 7 shared terms)

Mark: 

## P12 Luciano's attention is the scarce resource; what reaches him is synthesized according to the objectives of the project.

- explicit: 2026-10-06T07:10Z (luthier@daa5b95:docs/plan-working-method-2026-10-06.md:37 2026-10-06T07:10Z; luthier@efd8143:docs/plan-working-method-2026-10-06.md:323 2026-10-06T08:07Z)
  - earlier? 2026-09-21T14:42:52Z `day:2026-09-21:luthier-como-meta-proyecto-ligado-a-sonolocalizacion`: "cuando yo ya empiece a ver el tema librerías, yo tengo que ya empezar a trabajar con Luthier"
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 6 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 4 shared terms)
  - memory? `feedback-numbered-references.md` of account 1, first written 2026-10-06T07:19Z (chat:7217f251:460, 4 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 6 shared terms)
  - memory? `sonolocalizacion-donde-vive.md` of account 1, first written 2026-08-30T21:38Z (chat:4adb5dd2:41, 4 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 4 shared terms)
- operative in every repository of account 1: its global CLAUDE.md, 2026-10-06T08:19Z (chat:8d5ce152:340)

Mark: 

## P13 A principle is worth the decisions it guides or helps interpret.

- explicit: 2026-10-06T07:10Z (luthier@daa5b95:docs/plan-working-method-2026-10-06.md:117 2026-10-06T07:10Z; luthier@efd8143:docs/plan-working-method-2026-10-06.md:272 2026-10-06T08:07Z)
  - earlier? 2026-10-05T22:20:39Z `dialogue:aa680014:chequeo-bool-y-chequeo-refinado-dos-presentaciones`: "Hay un principio de simplicidad que hace que un chequeo devuelva un bool. Pero con un monada aplicada sobre el chequeo podes hacer que devuelva un tipo chequeado. quiero decir, ambas funciones son val"
  - earlier? 2022-08-03T14:56:32Z `written:2022-08-03_tapp-before:equals-as-assertion`: "encontre una idea que me puede servir de generadora para tapp/quimulun: la idea de que el signo \"=\" representa aserciones, es decir que un lado es igual al otro."
  - earlier? 2023-03-02T14:27:43Z `written:2023-03-02_estoy-perdido:funciones-por-postconditions-sin-implementacion`: "Defino funciones que son de un tipo dado (es decir que cumplen con ciertas postconditions) sin decir cual es la implmentacion."
- operative in luthier: CLAUDE.md 2026-10-06T08:18Z luthier@fea45bf
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 5 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 4 shared terms)
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 4 shared terms)
- operative in sonolocalizacion: CLAUDE.md 2026-10-06T08:18Z sonolocalizacion@ede219f
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 9 shared terms)
  - memory? `protocolo-y-registro.md` of account 1, first written 2026-09-09T19:10Z (chat:b66f1892:289, 9 shared terms)
  - memory? `experimento-cero-equipamiento.md` of account 1, first written 2026-09-01T18:12Z (chat:93ba9996:197, 3 shared terms)

Mark: 

## P14 A type is a concept: declared, then defined, and only then inhabited; a function is a value of a defined function type, never of a bare exponential.

- explicit: 2026-10-07T11:16Z (chat:182f2465:568 2026-10-07T11:16Z; chat:182f2465:575 2026-10-07T11:18Z)
  - earlier? 2026-10-04T03:10:29Z `dialogue:88936d99:dos-estados-declarado-definido`: "habria dos estados de un tipo: declarado (equivalente al forward declared de C++) definido (es decir con sus invariantes declaradas) La idea es que si vos decir a: A:= extern .... o a: A:= \a .... A t"
  - earlier? 2026-05-29T17:46:56Z `dialogue:20260529T1400:contexto-como-dag-y-tipos-implicitos`: "la manera de definir contexto sería como un DAG ... podrías definir tipos implícitos, a través de soluciones, o de, por ejemplo, el tipo que soluciona determinado problema"
  - earlier? 2026-05-29T17:46:56Z `dialogue:20260529T1400:tipos-no-definidos-y-forward-reference`: "vos podés por ejemplo, pasarte a un tipo que no está definido y lo definís después ... si no está definido nunca esos son otros tipos"
- operative in luthier: CLAUDE.md never
  - memory? `luthier-fase-semantica.md` of account 1, first written 2026-09-29T00:08Z (chat:175c0408:122, 15 shared terms)
  - memory? `luthier-ideas-pipeline.md` of account 1, first written 2026-08-31T23:13Z (chat:f453278e:48, 4 shared terms)
  - memory? `luthier-working-method.md` of account 1, first written 2026-10-06T06:12Z (chat:7217f251:179, 4 shared terms)
- operative in sonolocalizacion: CLAUDE.md never
  - memory? `domo-srp-pipeline.md` of account 1, first written 2026-09-09T15:56Z (chat:b66f1892:62, 6 shared terms)
  - memory? `luthier-objeto-matematico-como-invariante.md` of account 1, first written 2026-10-05T03:38Z (chat:52d3e68e:2805, 5 shared terms)
  - memory? `corridas-autonomas-largas.md` of account 1, first written 2026-10-05T22:40Z (chat:fea341bd:164, 5 shared terms)

Mark: 

