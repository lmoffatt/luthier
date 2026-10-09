---
source: claude-code
account: 
id: 0602f3b5-3a69-4ec7-80a3-6ac3f3d55717
title: "analsis critico de la libreria luthier en ~/Projects/luthier y su uso en ~/Projects/sonolo"
started: 2026-10-05T07:04:27Z
ended: 2026-10-05T07:46:11Z
offset: 
turns: 8
cwd: -home-lmoffatt-naive
exports: 20261009
flags: 
origin:
  - raw/claude-code/20261009/-home-lmoffatt-naive/0602f3b5-3a69-4ec7-80a3-6ac3f3d55717.60cba86f.jsonl.gz sha256 60cba86fde4216cf0507e9f6a77c2a5b03a912bd8e0b2e88dda31a3218be9a42
iachat: 1
---

# analsis critico de la libreria luthier en ~/Projects/luthier y su uso en ~/Projects/sonolo

## 1. Luciano  2026-10-05 07:04:27 UTC  (line 3)

analsis critico de la libreria luthier en ~/Projects/luthier y su uso en ~/Projects/sonolocalizacion

## 2. Model  2026-10-05 07:13:20 UTC  (lines 102, 132, 137)

Medí la corrida real (3 min) y por error dejé las salidas en `~/tmp` y un `experiment_zero.run.json` nuevo en el repo. Comparo con los resultados guardados y limpio lo que creé.

Ya tengo el panorama del lado de sonolocalización: corrí los tests y reproduje el experimento cero. Falta el informe del agente que audita el intérprete; lo espero antes de escribir el análisis.

Sigo esperando el informe del agente que audita el intérprete (soundness del checker, del testeo y de los certificados). Cuando llegue, escribo el análisis completo. Lo que ya medí, para que no se pierda:

- `distances_python.lut` y `optimization_python.lut` no pasan `check` en el estado actual del working tree: `pairI was declared with type Vec (Fin nodes), but is defined with Vec Int`.
- `luthier check` tarda unos 18 s incluso en un archivo de 38 líneas (`positions.lut`).
- `luthier run experiment_zero.lut` tarda 3 min y reproduce bit a bit `positions.csv` y `residuals.csv` de la sesión A.
- Los certificados importados de `array`, `algebra`, `positions` y `distance_graph` figuran como stale.

Por error la corrida dejó un directorio `~/tmp/...` y un `experiment_zero.run.json` sin trackear. Los borré, y antes confirmé que los dos los había creado yo.

## 3. Luciano  2026-10-05 07:26:57 UTC  (line 140)

y?

## 4. Model  2026-10-05 07:28:10 UTC  (line 144)

Todavía no llegó el informe del agente sobre el intérprete, así que la parte de soundness del checker y de los certificados queda para cuando llegue. El resto ya lo puedo decir.

## Luthier como librería

**La idea central es sólida y tiene antecedentes.** Una teoría con su igualdad como componente, modelos como registros de operaciones y leyes corridas como tests es lo que hacen las views de Maude, las `structure` de Lean y las typeclass laws de QuickCheck. Hay tres aportes propios que valen: el certificado con el hash del cono de dependencias, la R10 (caracterizar en lugar de reimplementar) y el objeto como componente fuertemente conexa. La R10 es lo más valioso que salió de esta semana.

**La especificación se mueve más rápido que cualquier uso.** El draft 1 de 04/05 es de ayer, y hoy todos los documentos de `docs/semantica` tienen cambios sin commitear. Del lado de Luthier hay 36 commits en cuatro días, guiados por notas de voz diarias. Ningún programa que use Luthier puede estabilizarse así, y sonolocalización lo muestra (más abajo).

**El costo ya choca contra el problema más chico del proyecto.**
- `luthier check positions.lut`, 38 líneas, tarda 18 s. Casi todo es re-elaborar `array`, `algebra` y el resto de las librerías importadas en cada invocación, sin caché.
- `luthier run experiment_zero.lut` tarda 3 min para un ajuste de 10 nodos y 22 distancias, que en numpy son milisegundos. Lo bueno: reproduce `positions.csv` y `residuals.csv` bit a bit.
- La parte acústica (GCC sobre trazas de 131 072 muestras, domos sobre grillas) es varios órdenes de magnitud más grande. Con este evaluador no entra.

**"Certificado" promete más de lo que hay.**
- `test laplaceCalibrated with 3`, `fullKernel with 5`, `fullPair with 5`: con 3 casos, una ley estadística es una anécdota. Puede que cada caso haga muchas actualizaciones por dentro, pero no lo pude verificar: un grep sobre los umbrales de `UniformDraws` y `CalibratedGaussian` me lo bloqueó el clasificador de permisos.
- Los generadores de Python siguen salteando el predicado del subtipo (caso 9, abierto en 05 §10).
- Los certificados importados de `array`, `algebra`, `positions` y `distance_graph` están stale, y nada lo impide: `run` corre igual (05 §7). El certificado no habilita ni bloquea nada; es un registro. Está bien que lo sea, pero entonces la palabra "certificado" sobra.

**Hay una incoherencia semántica en los generadores.** `GoodGraph = DistanceGraph`, `CompleteGraph = DistanceGraph` y `BrokenGraph = DistanceGraph` son alias, y R7 dice que un alias se expande antes de chequear y no tiene identidad. Pero la ley `RejectsDefect (v) (g : BrokenGraph)` depende de que el generador se busque por el nombre del alias. O sea, el tipo de un parámetro lleva una distribución que el sistema de tipos dice que no existe. La distribución de los casos es parte del test, no del tipo: tendría que ir en la directiva (`test validity over BrokenGraph from genBroken`) o como argumento explícito.

**La ergonomía cuesta.** No hay `let`, y `fit` en `experiment_zero.lut` termina en `} } } } } } } } } }`. Sin argumentos implícitos aparecen llamadas como `exchangeDeparture (Vec Float64) GaussianBelief (Vec Float64) (family sigma) ...`. Las dos cosas están en la lista de pendientes; las pondría antes que cualquier refinamiento del kernel.

**Un detalle trivial.** `pytest` desde la raíz junta `archive/tests-2026-10-04` y da 35 fallas. `pytest tests` da 78/78. Falta `testpaths = ["tests"]` en `pyproject.toml`.

## El uso en sonolocalización

**El trato se invirtió.** La nota de traspaso decía que Luthier solo describe (tipos, leyes, `extern` a Python, `test`) y que nada con cuerpo no trivial va en Luthier. Hoy `experiment_zero.lut` tiene el gauge, la jacobiana, el modelo, el `main`, Jacobi nativo para `pinvSym` y un LM nativo duplicado. Python pasó a ser el "lado rápido", que tiene que coincidir bit a bit con el nativo. Por eso el orden de una suma termina siendo materia de especificación (caso 27).

**Los `Agrees` exactos certifican una transliteración.** `MaximizerAgrees` y `StepAgrees` con `approxVec 0.0` prueban que `lm.py` y `optimization.lut` hacen las mismas operaciones de punto flotante en el mismo orden. Por tu propia R10 eso es "consistente, no caracterizado". Además es frágil: un cambio de BLAS, o reescribir `lm.py` con `lstsq`, lo rompe sin que el algoritmo esté mal. `StepRule`, `DescentDirection` y `Certified` sí son leyes de verdad, y se sostienen solas.

**El alcance se achicó a la parte fácil.** La capa del 10-01/10-02 tenía lo acústico (`gcc`, domo, calibración) y quedó archivada. Lo que hoy está en Luthier son las posiciones a partir de la cinta: la verdad de referencia del experimento, que ya andaba en `positions_from_distances.py`. Los 21 commits de sonolocalización desde el snapshot del 10-02 son todos de la capa Luthier, y en ese período no hubo avance acústico en este repo. Esa capa se archivó dos veces en cuatro días.

**El estado actual está roto.** `distances_python.lut` y `optimization_python.lut` no pasan `check`: `pairI` está declarado `Vec (Fin nodes)` y ligado como `Vec Int`. Es el cambio de dimensiones en los tipos a mitad de camino, y muestra cómo cada decisión del kernel se propaga a todos los archivos de abajo.

**El acoplamiento entre repos no tiene versión.** Sonolocalización depende del working tree de `~/Projects/luthier` (pip -e, con rutas como `../../luthier/src/luthier/lib/algebra.lut`), que hoy tiene cambios sin commitear. Los resultados de sonolocalización no se pueden reproducir a partir de un commit de Luthier.

**Lo que rindió, y es real:**
- `experiment_zero` ajustaba el grafo sin validarlo.
- El `same` gaussiano no era simétrico.
- Laplace mueve la media hasta 0,3 desviaciones estándar posteriores según el orden de los datos, con el error de la cinta (3 cm).
- Los controles negativos del kernel de probabilidad.

Las cuatro son leyes bien elegidas. Pero ninguna necesitaba el lenguaje: salen igual con pytest + hypothesis, que ya está en `sonolik/tests` y trae shrinking y una base de ejemplos.

## Qué haría

1. **Desacoplar.** Taggear una versión de Luthier para sonolocalización y no seguir el HEAD.
2. **Volver al trato original en sonolocalización.** La corrida es Python puro. Las definiciones nativas de Luthier quedan como oráculos de test, fuera del camino de `run`. Los `Agrees` exactos se reemplazan por leyes que caracterizan, con tolerancia.
3. **En Luthier, antes de tocar más el kernel:**
   - caché de la elaboración de los imports;
   - `let` y argumentos implícitos;
   - comprobar el predicado sobre lo que devuelve un generador de Python;
   - la distribución en la directiva `test` y no en alias;
   - un `n` mínimo, o la potencia reportada, para las leyes estadísticas;
   - que `run` avise fuerte cuando el cono tiene certificados stale.
4. **Retomar lo acústico.** Es lo que importa del proyecto, y ahí Luthier debería entrar solo como capa de leyes sobre `sonolik`.

En resumen: como diseño, Luthier mejoró mucho esta semana. Como herramienta de sonolocalización, hoy le cuesta más al proyecto de lo que le devuelve. Cuando llegue la auditoría del intérprete agrego lo que encuentre sobre el checker y los certificados.

## 5. Luciano  2026-10-05 07:45:28 UTC  (line 152)

y?

## 6. Model  2026-10-05 07:45:39 UTC  (line 156)

El agente que audita el intérprete sigue corriendo y todavía no devolvió nada, así que no tengo resultados nuevos para sumar. Cuando termine me llega el aviso y agrego lo que encuentre sobre el checker y los certificados.

Si preferís no esperar, lo freno y hago yo una revisión más acotada. Me concentraría en dos preguntas: si el hash del certificado cubre el código Python de los `extern`, y si un test puede pasar sin haber corrido ningún caso.

## 7. Luciano  2026-10-05 07:45:50 UTC  (line 159)

ojo que va a empezar a trabajar otro agente ahi

## 8. Model  2026-10-05 07:46:11 UTC  (lines 171, 186, 195)

Le avisé al agente que audita el intérprete. Le pedí que no escriba nada ni corra pytest dentro de `~/Projects/luthier`, que use solo el scratchpad, y que cierre pronto con lo que ya tenga verificado.

Hay algo que no se puede evitar: Luthier está instalado con `pip -e`. Si el otro agente toca `src/luthier/`, los programas de prueba que corra el mío van a usar el código nuevo. Por eso le pedí que ate cada hallazgo al commit `b13baa3` y que avise si ve un archivo distinto de como lo leyó antes. Cuando llegue el informe, voy a revisar que no mezcle versiones.

Yo no escribí nada en `~/Projects/luthier`. Ahí solo leí y corrí `pytest`, que puede haber actualizado `.pytest_cache` y algún `__pycache__`, los dos generados e ignorados por git.

Llegó la auditoría del intérprete. Revisé a mano tres de los hallazgos en el código y se confirman: el hash del `extern` es solo el string del target (`certify.py:87`), `run_fuel` vale 2 000 000 000 (`evaluator.py:47`) y la caché de materialización usa solo `id(f)` como clave (`machine.py:493`). El resto lo verificó el agente con programas de prueba, salvo lo que marcó como sospecha.

Una aclaración: casi todo `src/luthier/` tiene cambios sin commitear, así que esto vale para el working tree de hoy y no para `b13baa3`. Si el otro agente ya está tocando esos archivos, algo puede cambiar.

## Lo más grave

1. **El certificado no ve el código Python.** El hash cubre el texto `.lut` elaborado, y de un `extern` solo entra el nombre del target. El agente cambió `dbl` de `x + x` a `x * 3`: `check -v` siguió diciendo "certified" y `eval` dio 6. Tampoco entran en el hash los `gen`, ni `n`, ni el modo. En sonolocalización, donde casi todo el lado rápido es Python, el certificado no garantiza nada sobre lo que corre de verdad. Por el otro lado, cambiar el printer o el intérprete invalida certificados que no cambiaron de significado: por eso los 37 de las librerías están stale.

2. **Los generadores de funciones son constantes.** "Toda `f : Int -> Int` es constante" pasa 200/200, y "toda `Float64 -> Float64` es afín" también. Cualquier ley cuantificada sobre funciones, como los `Sampler`, `Objective` o `Maximizer` genéricos, se prueba sobre una muestra degenerada, y la nota del certificado no cambia el grado `sampled 200`.

3. **"Exhaustive" sobre `Int` es el rango [-16, 16].** Los floats se sortean uniformes en [-s, s] con s ≤ 16: no aparecen magnitudes grandes o chicas, ni -0.0, ni subnormales.

4. **Hay casos vacuos que cuentan como pasados.**
   - Una implicación cuyo antecedente el generador nunca alcanza pasa 100/100 sin descartes.
   - Cuando el muestreo por rechazo falla, el caso se saltea en silencio y la distribución queda sesgada hacia lo fácil: una ley falsa pasó 29/29, siempre con n = 0.
   - Un dominio exhaustivo vacío (`Fin 0`) pasa con 0 casos.

5. **Los `extern` cuyo codominio es un subtipo no se chequean.** Uno declarado `Int -> VecOf 3` que devuelve un array de largo 5 se acepta. Uno declarado `Int -> Nat` que devuelve -1 se acepta. La regla 3 de 04 §6 ("la forma se chequea al cruzar") no está implementada. Las obligaciones solo existen dentro de `test`: en `eval` y `run` no hay contrato, y un `dotDef` entre `VecOf 3` y `VecOf 4` devuelve 3.0 sin error.

6. **La caché de materialización da resultados incorrectos.** Pasar la misma función a un `extern` que espera `Fin 3` y después a otro que espera `Fin 5` da (3, 3). Es un bug de corrección, no de rendimiento.

7. **La tolerancia sale de otra hoja que también está bajo prueba.** `SolveInverts` escala la tolerancia por `cond`. Un `solve` que siempre devuelve ceros pasa 50/50 si `cond` devuelve 1e30. Además, `approx` es `|a-b| <= tol·(1+|a|+|b|)`, que para magnitudes menores que 1 es un test absoluto.

## Lo demás

- **Checker.**
  - La conversión es sintáctica en términos neutros: `VecOf (n + 0)` y `VecOf n` no convierten, y el error de tipos se vuelve una obligación pendiente.
  - No hay eliminación dependiente.
  - El `match` acepta ramas duplicadas, patrones literales de otro tipo, y matches anidados no exhaustivos que fallan en ejecución.
  - R8 deja pasar `==` sobre un `data` que tiene funciones en sus constructores.
  - La identidad posicional de productos y sumas permite intercambiar campos en silencio. Es lo que dice la spec, y es una trampa.
- **Desvíos de la spec.**
  - Las precondiciones del `if` se pierden en las obligaciones que son leyes cuantificadas: solo se conservan en las `Bool`.
  - Una ley sobre `U` sale FAILED en vez de pendiente.
  - Faltan los grados *point* y *witnessed*, y la regla del eslabón más débil.
  - `.run.json` no registra lo no certificado del cono.
  - `check -v` no muestra la tabla de completitud.
- **Rendimiento.**
  - Los 18 s de cada invocación son re-chequear las librerías.
  - Cada multiplicación-suma escalar cuesta unos 90 µs.
  - Si un término toca un hueco sin llenar, la máquina cae al evaluador por sustitución, unas 120 veces más lento.
  - El fold a la derecha que exige 04 §6 no es de cola, y `dotDef` con 10⁵ elementos revienta la pila.
  - Un test que no termina se cuelga sin salida, por el `run_fuel` de 2·10⁹.
- **Código.**
  - `checker.py` tiene 1599 líneas, con `silent()` y doble chequeo para decidir si un cuerpo es habitante o predicado.
  - La lógica está duplicada entre `evaluator.py` y `machine.py`.
  - Hay unas 24 funciones muertas en `arrays.py`.
  - Hay nombres cableados en el intérprete (`Bool`, `List`, `Maybe`, `Fin`, `Nat`): `Fin` se reconoce solo por nombre, y un alias de `Fin` pierde la representación como array y la memoización.

## Qué cambia respecto de lo anterior

Refuerza la conclusión y le pone números. Las leyes de sonolocalización que de verdad aportaron (validar el grafo antes del ajuste, la asimetría de `same`, la calibración de Laplace) siguen valiendo como hallazgos. Lo que no vale es la palabra "certificado": hoy no cubre el Python, muestrea funciones de manera degenerada y cuenta casos vacuos como éxitos.

Si el otro agente va a trabajar en Luthier, este es el orden que le pasaría:
1. Hash del código fuente de los `extern` y de las directivas `gen`/`n`/modo.
2. Arreglar la clave de la caché de materialización.
3. Chequear el codominio de los `extern` al cruzar.
4. Contar y reportar descartes y casos vacuos.
5. Bajar `run_fuel` por defecto.
6. Generadores de funciones de verdad.
7. Cachear la elaboración de los imports.
8. `testpaths` en `pyproject.toml`.

Los programas de prueba del agente quedaron en el scratchpad, en `p/`, por si querés que se los pase al otro agente como casos de regresión.

El agente mandó una segunda versión del informe, con la misma sustancia que ya te pasé. Agrega dos cosas.

Primero, confirma que terminó antes de que empezaran los cambios del otro agente, así que no mezcla versiones. Todo el informe corresponde al working tree con los cambios sin commitear sobre `b13baa3`. En el repo solo tocó `.pytest_cache`, que ya existía, y `__pycache__`, que está en el gitignore.

Segundo, hay un detalle menor nuevo. Las precondiciones solo se generan en los `match` sobre `Bool`: en los `match` por constructor o etiqueta no se genera ninguna. La spec ya lo tiene como abierto en 05 §10.

No cambia nada del análisis ni de la lista de prioridades que te dejé. Los programas de prueba siguen en el scratchpad, en `p/`, si los querés como casos de regresión para el otro agente.
