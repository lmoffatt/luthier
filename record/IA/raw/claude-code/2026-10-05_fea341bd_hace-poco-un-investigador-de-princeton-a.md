---
source: claude-code
account: 
id: fea341bd-ac78-49aa-9867-8408544935df
title: "hace poco un investigador de Princeton argentino dio una charla en el departamento de fisi"
started: 2026-10-05T22:16:48Z
ended: 2026-10-05T23:32:48Z
offset: 
turns: 12
cwd: -home-lmoffatt-Projects-sonolocalizacion
exports: 20261009
flags: 
origin:
  - raw/claude-code/20261009/-home-lmoffatt-Projects-sonolocalizacion/fea341bd-ac78-49aa-9867-8408544935df.9d542e08.jsonl.gz sha256 9d542e08145814cc19445cf48bddf9f6c71ee93ceff9822ba3527e05f9aad1be
iachat: 1
---

# hace poco un investigador de Princeton argentino dio una charla en el departamento de fisi

## 1. Luciano  2026-10-05 22:16:48 UTC  (line 3)

hace poco un investigador de Princeton  argentino dio una charla en el departamento de fisica. quien puede ser?

## 2. Model  2026-10-05 22:17:47 UTC  (lines 56, 100)

The department's colloquium list doesn't give speaker names, so I'm opening each recent talk's page.

Casi seguro es **Matías Zaldarriaga**, cosmólogo argentino del Institute for Advanced Study (IAS) de Princeton. Ojo que es el IAS y no Princeton University, aunque en general se lo presenta como "de Princeton".

Estuvo en el Departamento de Física como profesor visitante en 2026. Dio un curso intensivo de investigación asistida con IA, con herramientas agénticas aplicadas a los proyectos de cada participante y ejemplos tomados de ondas gravitacionales. Fueron unos 50 participantes, entre estudiantes, docentes e investigadores del departamento. También dio un coloquio abierto a todo el departamento. El tuit de Física UBA sobre el curso es del 7 de septiembre de 2026. No encontré el título ni la fecha del coloquio: la lista de coloquios del sitio arranca el 14 de agosto y ninguno de los que figura es suyo. Los oradores de ahí son Canfield, Mininni, Mario Díaz, Soler Illia y Guillermo Silva (este último el 8 de octubre).

El otro candidato natural sería Juan Maldacena, también argentino y del IAS, pero no encontré nada que indique que haya venido este año. En tu Gmail no hay ningún anuncio de una charla con "Princeton" en los últimos 90 días.

Fuentes:
- [Física UBA en X, sobre el curso de Zaldarriaga](https://x.com/Fisica_UBA/status/2096969180041953719)
- [Coloquios del DF-UBA](https://df.uba.ar/en/coloquios)
- [Exactas, tag Instituto de Estudios Avanzados de Princeton](https://exactas.uba.ar/tag/instituto-de-estudios-avanzados-de-princeton/)
- [Zaldarriaga, honoris causa (2022)](https://exactas.uba.ar/zaldarriaga-honoris-causa/)

## 3. Luciano  2026-10-05 22:31:27 UTC  (line 103)

SI, Matias dio una charla donde decia que el armaba una orquesta de agentes usando claude para hacer investigaciones donde uno tenia el rol de PI y otros hacian el trabajo otros lo verificaban otros comparaban etc. 
Esto ya vos lo haces automaticamente o hay algo que yo pueda hacer para poder mejorar mi rutina de trabajo?

## 4. Model  2026-10-05 22:32:34 UTC  (line 119)

No lo hago solo. Por defecto trabajo como un único agente. A veces lanzo un subagente para una búsqueda amplia, pero la orquesta con roles (uno implementa, otro verifica, otro compara) hay que activarla, porque gasta varias veces más tokens. Se puede activar de tres maneras, de menos a más persistente:

1. **Pedirlo en el momento.** Si escribís "usá un workflow" o ponés la palabra "ultracode" en el prompt, armo un script que lanza agentes con roles y fases, y lo que encuentran los verificadores vuelve a mí para la síntesis. Ahora el tamaño está en "medium" (menos de 10 agentes); se cambia en `/config`, en "Dynamic workflow size".
2. **Roles fijos.** Un archivo por rol en `.claude/agents/`, cada uno con su prompt, sus herramientas y su modelo. Por ejemplo, un auditor que lee 04-kernel y 05-static-semantics y solo revisa diffs contra la especificación, sin poder editar. En el proyecto no hay ninguno; ni siquiera existe `.claude/`.
3. **Workflows guardados** en `.claude/workflows/`, que se llaman por nombre. Ahí quedaría una receta como "implementar en un worktree, después auditar y refutar en paralelo, después sintetizar".

`/code-review high` ya hace una versión chica de esto: una pasada encuentra problemas y otra los verifica por separado.

**Cuánto te sirve, en mi opinión**

Lo que vale de la orquesta es que el verificador sea independiente. Arranca con el contexto limpio y no vio el razonamiento del que implementó, así que no hereda sus anclas. Pero cinco Claudes comparten los mismos puntos ciegos. Tu carpeta [prototipo-cero/luthier/AI/](prototipo-cero/luthier/AI/), con claude.md, gemini.md y gpt.md, ya cumple el rol de comparador, y con modelos distintos los errores están menos correlacionados que entre agentes míos. Un workflow solo puede orquestar modelos Claude, así que esa comparación seguiría siendo manual.

Tu verificador más fuerte ya es mecánico: los cert.json, la reproducción bit a bit de la sesión A y los controles con la transformada integral de probabilidad (PIT). Un agente que lee código es más débil que eso. Donde sí aporta es en lo que los certificados no cubren:
- si el código implementa lo que dice la especificación
- si un test prueba lo que promete su nombre
- si quedó algún umbral hardcodeado
- si alguna fórmula tiene símbolos sin definir

El rol de investigador principal (el PI) te lo dejaría a vos en Luthier, porque las decisiones de diseño son tuyas. Un agente PI funciona en subproblemas con un criterio de aceptación mecánico, como que la transformada rápida pase la certificación contra la nativa (el commit e5ada7d). Ahí sí podría implementar, certificar e iterar sin vos.

**Choca con una regla tuya**

Los scripts los corrés vos. Un verificador que no puede correr la certificación se queda en leer código. Habría que decidir si los agentes verificadores pueden correr certificaciones y tests, sin tocar los scripts del pipeline que procesan datos.

Si querés, armo dos agentes (un auditor de la especificación y uno que intente refutar los resultados) y un workflow guardado. Lo probamos en la próxima tarea de Luthier que tenga un criterio de aceptación mecánico.

## 5. Luciano  2026-10-05 22:36:49 UTC  (line 122)

hay un tema y es que me da la sensacion de que luthier tiene una estructura que permite a la IA trabajar sostenidamente. Nunca me paso que la IA me trabaje toda la noche. Era mi esperanza que luthier sirva para esto,  y pareceria que algo asi paso. Tambien fue que di mas libertad para seguir trabajando y quizas alguna actualizacion por parte de claude

## 6. Model  2026-10-05 22:40:01 UTC  (lines 155, 170)

Ya tengo los números de la sesión de anoche. Antes de responder, leo completos dos mensajes tuyos de las 04:47 y 04:54 que tocan la verificación.

Sí, pasó: según el registro de la sesión, la IA trabajó 7 horas y 11 minutos sin ningún mensaje tuyo. Fue por los tres factores juntos. Cada uno evitó una manera distinta en que se corta una sesión larga, y la parte más difícil la resolvió Luthier.

**Lo que muestra el registro**

Entre "Dale, completa de 1 a 5, sin preguntar" (21:30) y tu "reporte de situación" (04:41) hubo:
- 497 llamadas a herramientas y cuatro commits.
- Un solo agente, sin subagentes, en modo auto todo el tiempo.
- Una compactación de contexto a las 23:07; siguió trabajando después sin perder el hilo.

No paró solo: lo interrumpiste vos. El ritmo sí cayó. Entre las 23 y la 1 fueron unas 130 llamadas por hora; de 1 a 4, entre 20 y 35. En ese tramo hay varios huecos de exactamente 600 s, que es el tope de un comando. Buena parte de la madrugada se fue en esperar cálculos lentos, y el commit de la transformada rápida de esta mañana ataca justamente eso.

**Cómo se corta una sesión larga y qué lo evitó**
- **Pedidos de permiso.** Cada uno frena la sesión hasta que contestás. Lo resolvió el modo auto. Hace falta, pero no alcanza.
- **Falta de criterio.** Si el agente no tiene forma de saber que algo está bien, lo prudente es parar y preguntarte. Con un certificado que pasa o no pasa, lo prudente es correr el chequeo y seguir. Esto es lo propio de Luthier, y creo que es el factor de fondo.
- **Pérdida del hilo.** La compactación borra el detalle de la conversación. Siguió porque el estado estaba en archivos: el plan con fases numeradas, la especificación, los cert.json y los commits.
- **La instrucción.** "De 1 a 5, sin preguntar" fue tuyo: un plan numerado y permiso explícito para no consultarte.
- **El modelo.** No lo puedo separar del resto. No sé qué modelo usabas en septiembre, y con una sola noche no alcanza para atribuirle nada.

**Dónde está el límite**

En el reporte de las 04:41 el propio agente admitió varias cosas:
- las obligaciones genéricas nunca se ejecutan;
- la obligación de negate es falsa, y ya lo era antes;
- la fase 5.5 no registra la tasa de falsa falla ni repite con otra semilla;
- lmMaxIter había quedado como constante, contra tu regla (lo arreglaste a las 05:10).

O sea, trabajó horas sobre chequeos que no cubrían todo, y recién lo dijo al final. Esa autonomía depende de qué tan completos son los certificados: donde un certificado tiene un hueco, el agente sigue avanzando igual.

Por eso tu pedido de las 05:04, que los tests pidan un generador explícito para cada tipo, me parece la mejora que más rinde para las próximas noches, más que sumar agentes. Ahí sí encaja la orquesta de Zaldarriaga: un verificador independiente sirve para buscar lo que los certificados no cubren, no para volver a correrlos. Los cuatro puntos de esa lista son los que un agente así tendría que haber encontrado a medianoche.

Guardé esto en una memoria nueva (corridas autónomas largas) para que quede como referencia en las próximas sesiones.

## 7. Luciano  2026-10-05 22:59:36 UTC  (line 179)

Volviendo a Zaldarriaga, hay algo de lo que propone que pueda ayudarme a trabajar mejor?
y vos analizando mi forma de trabajar, hay formas en que pueda trabajar mejor?

## 8. Model  2026-10-05 23:00:50 UTC  (line 185)

Dos respuestas, en orden.

**Qué de lo de Zaldarriaga te sirve**

Lo que más te sirve es el verificador con contexto limpio, y la noche del 5 lo muestra. El agente trabajó siete horas y recién a las 04:41, cuando le pediste el reporte, dijo que las obligaciones genéricas nunca corrían y que la de negate era falsa. Un verificador que arranca de cero después de cada commit, lee la especificación y el diff y busca huecos, lo hubiera dicho a las 23. No hace falta ni workflow para eso: un agente definido en `.claude/agents/` con permiso de leer y correr certificaciones pero no de editar, que yo invoco al cerrar cada fase.

El comparador ya lo hacés a mano: la carpeta AI con claude.md, gemini.md y gpt.md es exactamente ese rol, y con modelos distintos es mejor que lo que yo puedo armar, porque mis agentes comparten sesgos. Lo que falta es el paso siguiente: en vez de leer los tres, pedirme una tabla de dónde discrepan. Donde los tres coinciden hay poca información; la decisión de diseño está en las discrepancias.

El PI y los workers en paralelo te darían algo en un punto concreto: entre la 1 y las 4 el ritmo cayó a un cuarto porque esperaba cálculos de 600 segundos. Con dos o tres workers en worktrees separados, uno espera mientras otro avanza. Vos ya hiciste esto a mano a las 05:06: bifurcaste la sesión en dos (hay dos transcriptos idénticos hasta ese minuto) y en una preguntaste si podía delegar. Eso es el Agent tool hecho manualmente.

El PI como agente, en Luthier, no te lo recomiendo. Las decisiones que tomaste esa noche (generadores explícitos por tipo, bounded Real, el chequeo como mónada) son las que valen, y ningún agente las iba a tomar.

**Cómo trabajás, y qué cambiaría**

Lo que más me llama la atención es que tus reglas funcionan a dos velocidades. Las mecánicas (certificados, reproducción bit a bit, el lock) aguantaron siete horas y una compactación. Las que están escritas en memoria o en instrucciones (nunca hardcodear, cada símbolo definido) se degradaron: lmMaxIter quedó constante. Lo que puedas convertir en chequeo, convertilo. Un lint de literales numéricos en los archivos de corrida tarda una hora y vale más que la regla escrita.

Lo segundo: preguntás "qué falta", "reporte de situación", "cómo estamos con el plan" varias veces por sesión. Eso dice que el estado vive en la conversación y no en el repo. Un archivo de estado que el agente actualiza con cada commit (qué fase, qué pasó, qué quedó a medias) te lo responde sin preguntar, lo ven las otras sesiones que editan en paralelo, y se lo podés dar a Gemini o GPT sin copiar.

Tercero: la fase 5.5 quedó a medias porque su criterio de aceptación no era mecánico. Las fases que tenían certificado se completaron; la que tenía "registrar la tasa de falsa falla" no. Antes de la próxima corrida larga, cada fase debería decir qué chequeo la cierra, y si no hay chequeo, esa fase es tuya y no de la noche.

Cuarto, menor: interrumpís a mitad de herramienta. Está bien ser el PI, pero cortar un Bash deja estado a medias. "Al llegar al próximo commit, frená y reportá" te cuesta diez minutos y no te cuesta un archivo roto.

Lo que no cambiaría: la especificación antes del código. Es lo que hizo posible la noche entera, y no lo tiene casi nadie.

## 9. Luciano  2026-10-05 23:23:33 UTC  (line 188)

Como transfiero las instrucciones de memoria a mecanicas?

## 10. Model  2026-10-05 23:24:27 UTC  (line 201)

Hay dos piezas separadas: quién juzga y quién dispara. Hoy las dos soy yo, por eso se degradan. La transferencia es poner el juicio en un script del repo y el disparo en un hook, para que no dependa de que yo me acuerde.

Revisé: no tenés ningún hook configurado, ni `.claude/` en el proyecto, ni pre-commit en git. Todo lo que sigue parte de cero.

**Las tres capas**

1. Lo que Luthier mismo puede rechazar. "Una ley, un nombre", "álgebra siempre importada", los generadores explícitos por tipo que pediste anoche. Van al certificador: si el `.lut` no cumple, no hay certificado. Es la capa más fuerte porque ni yo ni vos la podemos saltear, y ya está medio hecha.

2. Lo que un lint del repo puede atrapar. Un `lint/` con un script por regla, cada uno sale con error y una línea diciendo qué y dónde:
   - Nunca hardcodear: literales numéricos en `.lut` fuera de una declaración de parámetro. Hoy `lmMaxIter : Int := 200` en [optimization_check.lut:21](prototipo-cero/luthier/optimization_check.lut#L21) pasaría cualquier lectura mía y no pasaría un grep.
   - Umbrales duplicados: el mismo literal en dos archivos de corrida.
   - Todo en inglés: acentos, ñ y una lista corta de palabras castellanas en código, comentarios, `.lut` y nombres de archivo.
   - Figuras con cabeza: cada script de figura emite un JSON con pregunta, estadístico y nivel nulo; el lint verifica que exista y que ningún campo esté vacío.

3. Lo que queda como juicio, pero con recordatorio mecánico. "Cada símbolo definido en cada fórmula" no lo resuelve un grep; la skill `definir-simbolos` es lo más cerca. Lo que sí se mecaniza es que se corra: un hook que al terminar imprime "archivos .md con fórmulas tocados: X, Y; ¿corriste definir-simbolos?".

**Los disparos**

- PreToolUse sobre Edit y Write: corre el lint sobre ese archivo y bloquea la escritura si falla. Es la que hubiera parado lo de lmMaxIter a las 2 de la mañana en vez de a las 5.
- Stop (cuando termino un turno): corre la certificación completa y los lints de todo el repo; si algo falla, me lo devuelve como mensaje y sigo trabajando. En una corrida larga es el equivalente del verificador de Zaldarriaga, sin agente.
- Pre-commit de git: la misma suite. Protege contra las otras sesiones que editan en paralelo y contra Gemini o GPT, que no leen tu memoria.

Los hooks se configuran en `settings.json` con la skill `update-config`. Lo importante es que el hook sea una línea que llama al script del repo; la regla vive en el repo, versionada, y la ve cualquier modelo.

**Qué no transferir**

"Estructura de respuesta" y el estilo de escritura son sobre mí, no sobre el repo; quedan en memoria. Y la regla "los scripts los corre Luciano" tiene que relajarse para los lints y la certificación, porque si no el hook no puede correrlos. Eso te lo dejo a vos.

Si querés, empiezo por el lint de literales y el hook PreToolUse, que es el caso que ya falló una vez y lleva media hora. Después vemos cuál de las reglas de la capa 1 ya está en el certificador y cuál falta.

## 11. Luciano  2026-10-05 23:27:40 UTC  (line 204)

hace un plan para estos cambios y se lo paso a Opus

## 12. Model  2026-10-05 23:32:48 UTC  (line 245)

Written for: an Opus session that will implement it, with no memory of this conversation.

El plan está en [plan-mechanical-rules-2026-10-06.md](../luthier/docs/plan-mechanical-rules-2026-10-06.md), en el repo de Luthier, al lado del plan del 5 de octubre y con su mismo formato (problema, por qué, arreglo, caveat, etiquetas [proj] [int] [spec] [cfg]). Seis fases: inventario y baseline; lint de literales con el hook que bloquea; los disparos (Stop hook y pre-commit); inglés; figuras con cabeza; lo que el checker de Luthier debería rechazar; y recordatorios para lo que queda como juicio. Cada fase tiene un criterio de aceptación mecánico y tiempo estimado.

Tomé cuatro decisiones que quizás quieras cambiar antes de pasarlo:

1. Los `_check.lut` no están exentos del lint de literales. Sus tolerancias y presupuestos deciden qué significa un certificado, y vos dijiste anoche que lmMaxIter tiene que ser parámetro. Hoy hay hallazgos en optimization_check, laplace_check, belief_check y distances.lut (`nodes : Int := 7`).
2. El hook es PostToolUse y no PreToolUse: después de la escritura el archivo está en disco y el lint lo lee; antes habría que reconstruir el edit. Bloquea igual, el mensaje vuelve en el mismo turno.
3. Dejé escrito que "los scripts los corre Luciano" se relaja para lints, `check` y `certify`, como decisión tuya de hoy. Si no es así, hay que sacarlo de la sección "Principles".
4. La fase 5.3 (generadores explícitos) queda frenada hasta que apruebes la especificación que sale de `generators-2026-10-06.md`; Opus solo deja el test que falla.

Dos cosas que Opus tiene que averiguar porque yo no las encontré: dónde viven los scripts de figuras (en `prototipo-cero/scripts/` solo está "plan by Luciano") y cómo se comporta `certify` con los `.cert.json.lock` si lo corre un hook mientras otra sesión tiene el lock.
