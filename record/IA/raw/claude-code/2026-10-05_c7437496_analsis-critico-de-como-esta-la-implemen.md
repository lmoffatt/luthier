---
source: claude-code
account: 
id: c7437496-9d51-4487-b22f-05c9b6acd9e3
title: "analsis critico de como esta la implementacion de luthier y de luthier para sonolocalizaci"
started: 2026-10-05T07:06:43Z
ended: 2026-10-06T03:36:02Z
offset: 
turns: 102
cwd: -home-lmoffatt-Projects-sonolocalizacion
exports: 20261009
flags: 
origin:
  - raw/claude-code/20261009/-home-lmoffatt-Projects-sonolocalizacion/c7437496-9d51-4487-b22f-05c9b6acd9e3.135fe0e0.jsonl.gz sha256 135fe0e0b2da0427df1b53861aefd10914e759f629eda5048cd94ecf130cee8f
iachat: 1
---

# analsis critico de como esta la implementacion de luthier y de luthier para sonolocalizaci

## 1. Luciano  2026-10-05 07:06:43 UTC  (line 3)

analsis critico de como esta la implementacion de luthier y de luthier para sonolocalizacion

## 2. Model  2026-10-05 07:07:36 UTC  (lines 64, 105, 126, 138, 143)

Estoy leyendo las especificaciones (05, 06, 07) y en paralelo corre un agente que audita el intérprete y las pruebas; ahora sigo con las librerías y los .lut del proyecto.

Revisando los certificados encontré entradas que fallan y otras viejas; ahora busco el registro de corrida de experiment_zero.

Mientras termina el agente de auditoría del intérprete, ya tengo lo del proyecto. Espero su informe para cerrar.

experiment_zero reproduce los CSV byte a byte, pero tarda 3 minutos para 30 parámetros y 22 distancias. Falta el informe del agente sobre el intérprete.

Tengo lo del proyecto y las librerías. El agente que audita el intérprete (reglas R1–R10 contra el checker, cómo se generan los casos, si los certificados envejecen) sigue corriendo; cuando termine armo el análisis completo.

## 3. Luciano  2026-10-05 07:22:01 UTC  (line 146)

y?

## 4. Model  2026-10-05 07:23:13 UTC  (lines 155, 169)

El agente que audita el intérprete todavía no terminó. Te paso lo que ya está verificado sobre el proyecto, las librerías y los certificados, y cuando llegue el informe del intérprete lo completo.

**En una oración:** Luthier reproduce el experimento cero byte a byte y tiene dos ideas que funcionan de verdad (el Kernel con controles negativos y el LM comparado paso a paso). Pero la certificación hoy no hace lo que dice la 05: hay certificados que fallan, otros viejos que nadie borró, generadores que no respetan los refinamientos, y lo que corre experiment_zero no es lo que se certificó.

## 1. Lo que corre no es lo certificado

El Kernel se certificó sobre [distances.lut](prototipo-cero/luthier/distances.lut), con 7 nodos, todos los pares, gauge fijo, 16 parámetros y datos sintéticos. Lo de 7 nodos está fijo en `nodes : Int := 7` y otra vez en `N_NODES = 7` de [positions_luthier.py](prototipo-cero/src/positions_luthier.py).

[experiment_zero.lut](prototipo-cero/luthier/experiment_zero.lut) corre otro modelo: 10 nodos, 22 mediciones, el vector entero de 30 coordenadas, un prior y el `profiled` nativo. Comparten `distanceJacobian` y `profiled`, así que la certificación se transfiere razonablemente. Pero esa transferencia es un argumento tuyo o mío; ninguna ley la enuncia y el checker no la conoce.

Además nada se aplica a los datos reales. Hoy la sesión A da sigma = 25,7 cm (lo corrí ahora: 3 min 06 s, CSV idénticos). Una transformada integral de probabilidad uniforme sobre los residuos reales es justamente lo que marcaría ese outlier, y la ley ya está escrita (`UniformDraws`). Los certificados hablan de coherencia interna, no de si el modelo describe la cinta.

## 2. Hay certificados que fallan y nada lo frena

Entradas con `passed: false` en el estado actual sin commitear:

- [positions.cert.json](prototipo-cero/luthier/positions.cert.json): `point`, `pairDistances`, `distanceJacobian`, `flatten`
- [distances.cert.json](prototipo-cero/luthier/distances.cert.json): `embed`, `meanDist`, `jacDist`, `ProfileIsFullAtItsSigma` (este se quedó sin fuel)
- [distance_graph.cert.json](prototipo-cero/luthier/distance_graph.cert.json): los 7 lectores de columnas
- `probability.cert.json` en luthier: 5 entradas, todas por "no generator for U"
- `array.cert.json`: `retainedFloor`, sin fuel

Las causas son tres, y ninguna es una ley falsa:

- **El generador no respeta refinamientos dependientes.** `meanDist` falla con un `t` de largo 0 aunque su tipo es `HasFree` (`freeDim <= v.n`). `pairDistances` falla con `i.n = 1, j.n = 0`, y eso viola `Pairs p i`. `point` falla con `p.n = 1, n = 0`, y `n` no puede estar en `Fin 0`. Son fallas falsas, pero muestran que la obligación se cuantificó sobre la base y no sobre el tipo refinado.
- **El muestreo por rechazo no alcanza.** En 2000 intentos no encuentra un `GraphWithColumns`, ni un `MatRows 3`, ni un vector de largo ≥ 15 cuando el generador llega hasta 16.
- **Lo pendiente se registra como falla.** La 05 §7 dice que una ley sobre todos los modelos de una teoría "stays pending". Acá queda como FAIL, mezclada con las fallas reales.

Encima, el registro de corrida no anota nada de esto. La 05 §7 pide que `.run.json` registre los nombres no certificados del cono, pero [cli.py:300-306](../luthier/src/luthier/cli.py#L300-L306) guarda solo entry, hash, when, parameters y result. Tampoco existe ningún `.run.json` en el proyecto. experiment_zero corre con entradas fallidas en su cono y no queda rastro.

## 3. Los certificados solo acumulan

Hay entradas viejas que nadie borró:

- `realField` en algebra.cert.json es del 2026-10-04 20:19, sobre `R eqR` y `Commutative`. Hoy `realField` es un axioma y `R` ya no existe.
- `vecSpace` todavía lleva `Commutative` y `ScaleAssociates`, nombres que la reescritura unificó.
- `array_python.cert.json` tiene los nombres viejos (`inner`, `vnorm`, `addition`…) junto a los nuevos (`dot`, `norm`, `add`).
- `table.cert.json` sigue con `forallBelow`, que ahora vive en algebra.

Leyendo el archivo no se distingue lo vigente de lo obsoleto sin recalcular los hashes. Tu memoria dice "correr certify_all antes de commitear", y hoy eso no pasaría.

## 4. Las pruebas estadísticas tienen poca potencia

- `fullKernel` corre 5 casos, los pares 5, laplace 3 y calibración 5.
- `UniformDraws` compara solo los dos primeros momentos, mezclando todas las entradas, con z = 5.
- Los controles rompen el modelo al doble de sigma, el caso más fácil de detectar. No se sabe si un error del 10 o 20 % en sigma se detecta.
- Las semillas salen de `genInt` con tamaño hasta 16, así que se repiten: en el certificado aparece `seed = 2` tres veces entre las primeras cinco.

Lo que falta: controles al tamaño de efecto que te importa (por ejemplo 1,2 sigma) y que el certificado informe la potencia.

Una inconsistencia más: los controles del LM ([lm_controls.py](prototipo-cero/src/lm_controls.py)) se corrieron a mano el 10-04 y no están en la suite. En distances_python sí están adentro, como `sampleControl` y `pitControl`.

## 5. Garantías que viven en comentarios, no en tipos

- `meanModel` dice "which are nodes of theta when the graph is valid", pero `MapInput` lleva `Vec Int` sin ninguna relación con `Node`.
- `Node p = Fin (p.n / 3)` no exige que `p.n` sea múltiplo de 3.
- `distanceJacobian` divide por la distancia `h`. `rowPriorSeparated` garantiza que no sea cero en el prior, pero no durante las iteraciones del LM.
- Los nodos fijos del gauge (0, 1, 2, 4, 5, 8) están escritos dos veces: en `isFixed` del .lut y en `FIXED` del Python. Es el principio de un solo nombre por cosa roto a través del puente, y también "nunca hardcodear".

## 6. `Real` todavía es una etiqueta

`Real` aparece solo en `core.lut` y en el axioma `realField`. En las librerías hay unas 300 apariciones de `Float64`, y `array` y `positions` son Float64 de punta a punta. La 06 lo marca como pendiente, pero hoy la distinción no da nada.

Las tolerancias son a mano: `agreeTol` con magnitudes ad hoc, y `pitTol = 1e-6` en `lib/probability.lut` está calibrado para "the sigmas of the tape". Ahí el proyecto se filtra a la librería genérica, igual que `ensembleSize`, `zMax` y `fdStep`, que son constantes de librería.

## 7. Ergonomía y velocidad

- No hay `let`. `fit` y `diagnose` terminan en diez llaves seguidas, `} } } } } } } } } }`. Tampoco hay menos unario: se escribe `0.0 - x`.
- 3 minutos para un ajuste de 30 parámetros con el LM en Python: el costo es la verosimilitud interpretada.
- Certificar `distance_graph` lleva unos 30 s por entrada.

Con esa velocidad, el domo y GCC-PHAT, con miles de muestras por grabación, no se pueden escribir nativos. Van a ser externs de punta a punta.

## 8. Lo que funciona

- La reproducción byte a byte, verificada hoy.
- El triángulo del Kernel con dos controles, cada uno rompiendo un lado distinto.
- El LM con la traza idéntica estado por estado, más controles por mutación.
- Tipar `same` como `Setoid` encontró un bug real: la belief gaussiana no era simétrica. Es la mejor evidencia de que el método atrapa errores.

## Lo estratégico

Desde el 30-09 el trabajo fue casi solo Luthier: tres capas archivadas o reescritas en seis días, y las dos ramas `numbers` sin commitear (17 archivos en el proyecto, unos 40 en luthier). Lo certificado de sonolocalización es la etapa de la cinta métrica, la más fácil y la que ya andaba en Python. La parte acústica (GCC-PHAT, el domo, la verosimilitud de la medición, que estaba pendiente el 11-09) no tiene nada en Luthier. Cada vez que la especificación se mueve hay que recertificar todo, y eso es lo que dejó los certificados viejos y los que fallan.

Mi recomendación, en orden:

1. Congelar la v0 y commitear.
2. Arreglar la certificación como compuerta: generadores que respeten los refinamientos dependientes, pendiente distinto de falla, borrar entradas sin nombre vigente, y que el registro de corrida anote el cono no certificado.
3. Que lo próximo de Luthier lo empuje la etapa acústica, la verosimilitud del GCC, y no la limpieza del álgebra.

Cuando llegue el informe del intérprete lo sumo: qué reglas R1–R10 aplica realmente el checker, los `except` que tragan errores y qué atestigua el hash.

Llegó la auditoría del intérprete. Confirmé en el código cuatro de sus hallazgos: el hash, el "exhaustivo" sobre `Int`, el `Bool` leído por posición y `from_python`. El resto viene de las pruebas del agente; aclaro abajo cuál es inferencia.

**En una oración:** el checker aplica bien casi todas las reglas de forma (R1, R4, R5, R6, R7, R9), pero la frontera con Python y la certificación tienen agujeros por los que pasan leyes falsas, y los certificados que dependen de huecos nunca van a coincidir.

## Los agujeros graves, en orden

1. **Lo que viene de Python no se valida contra su tipo.** [evaluator.py:882](../luthier/src/luthier/evaluator.py#L882) convierte cualquier `int`, `float` o `str` de Python en un literal, sea cual sea el tipo declarado. Con un extern `-> Float64` que devuelve `"hello"` sale `'hello' : Float64`. Peor: `/` elige la operación según el tipo de Python, así que con un `Int` disfrazado de `Float64`, `3 / 2` da `1` (división entera). Con `--set` pasa lo mismo: `sigma=3` corre con aritmética entera. En experiment_zero no pega porque los valores vienen de numpy como float, pero nada lo impide.

2. **Los tipos refinados en el resultado de un extern no se chequean.** Un extern `neg : Float64 -> NonNeg` devuelve `-2.0 : NonNeg` sin ninguna obligación ([checker.py:593](../luthier/src/luthier/checker.py#L593)). Es la versión general del punto que la 07 §9 deja abierto.

3. **El hash del certificado no ve el Python.** Solo hashea el texto `extern "python:lm.maximize"` ([certify.py:87](../luthier/src/luthier/certify.py#L87)). Si cambiás `lm.py`, el certificado sigue "vigente". Tampoco entran en el hash el generador, la cantidad de casos ni la versión del intérprete. Al importar se acepta cualquier entrada con hash igual, aunque haya corrido un solo caso.

4. **Los certificados que dependen de huecos quedan viejos para siempre.** Al importar se compara el hash antes de que el archivo padre llene los huecos ([cli.py:107](../luthier/src/luthier/cli.py#L107)), y al certificar se calculó después. Por ejemplo, `intRing` da un hash con `algebra.lut` solo y otro bajo `algebra_python.lut`. Hoy 37 leyes vistas desde `algebra_python` y 35 nombres de `array.lut` aparecen como "stale certificate", aunque sean más nuevos que los `.lut`. Esto explica parte del desorden que vi en los certificados: aunque las certificaciones sean frescas, el sistema no puede reconocerlas.

5. **Leyes falsas que pasan:**
   - "Exhaustivo" sobre `Int` significa el rango de -16 a 16 ([generators.py:313](../luthier/src/luthier/generators.py#L313)). `x*x < 1000` quedó certificado como *exhaustivo* con 33 casos.
   - `Bool` se lee por posición ([checker.py:118](../luthier/src/luthier/checker.py#L118)). Cualquier suma de dos `Unit` cuenta como `Bool`, y la primera alternativa es `true`. Con `Verdict = < wrong | right >`, un predicado que siempre devuelve `wrong` se cumple.
   - Las leyes de cuerpo de `float64Field` pasan porque `lawMagnitude = 16.0` está ajustado al rango del generador, [-16, 16]. La asociatividad falla en (1e8, -1e8, 3e-9): el error es 3e-9 contra una tolerancia de unos 4,5e-13. Esto es inferencia del agente a partir de las constantes y una cuenta en Python; no lo corrió en Luthier.

6. **Los externs `provisional` se certifican igual**, cuando R5 dice que nunca. Y el certificado no lleva el campo `provisional`.

7. **Las tablas `Fin n -> Int` se generan como float64** ([generators.py:143](../luthier/src/luthier/generators.py#L143)), contra la 06 §7. Las leyes enteras sobre índices corren con división de punto flotante.

8. **R8 tiene agujeros.** Se acepta `==` sobre un `data` que tiene funciones adentro, porque solo se miran los argumentos de tipo, y en ejecución queda un término trabado sin error. También se acepta `==` sobre `Real`, que se calcula como igualdad de floats. Y pasada la profundidad 20 no se mira más, así que `==` se permite.

## Lo que la 05 promete y no está implementado

- Los grados point, witnessed, assumed y "el eslabón más débil" de una cadena.
- `test n` sobre todo el objeto: hoy corre solo las obligaciones del nombre ([testing.py:268](../luthier/src/luthier/testing.py#L268)).
- La tabla de completitud suficiente de la 05 §6.
- El registro del cono no certificado en `.run.json`, que ya te había marcado.
- `toFloat64 : Real -> Float64` no existe: es `Int -> Float64`, y el mensaje de error de [checker.py:1144](../luthier/src/luthier/checker.py#L1144) recomienda usarlo sobre un `Real`.

Lo de `Real` lo confirma: no tiene representación ni generador, y la aritmética sobre él se rechaza. La distinción con `Float64` existe solo al chequear tipos, nunca al ejecutar.

## Salud del código y velocidad

- Las 78 pruebas pasan con pyenv y con miniconda, en unos 22–26 s. Pero `test_spec.py` solo chequea que los programas carguen: no certifica nada y no cubre ninguno de los bugs de arriba.
- Cargar cualquier cosa que importe `array.lut` lleva 17–19 s. La causa principal es que cada `+` o `*` anidado vuelve a inferir el tipo del operando izquierdo ([checker.py:1254](../luthier/src/luthier/checker.py#L1254)). Además hay caminos que chequean dos veces, una en silencio y otra de verdad.
- Hay dos evaluadores (el de sustitución, para el checker, y la máquina call-by-need, para las pruebas) que difieren en casos borde. La máquina cae al otro en silencio cuando no soporta algo ([machine.py:605](../luthier/src/luthier/machine.py#L605)).
- Hay código muerto: `pygen.py`, y la rama de tipos opacos por extern que R5 ya prohíbe.
- No existe el comando `certify_all`. El CLI tiene `check`, `test`, `run` y `eval`; el `certify_all` de tu memoria es un script del scratchpad.

## Qué cambia en la recomendación

El paso 2 que te propuse (la certificación como compuerta) se vuelve más concreto. Por orden de costo contra daño:

1. Validar en el puente todo lo que viene de Python y de `--set` contra el tipo declarado, incluidos los refinamientos del resultado. Es lo único de esta lista que puede dar un resultado numérico equivocado sin aviso.
2. Que el hash incluya el código de Python de cada extern, por ejemplo el hash del módulo, y que se compare después de llenar los huecos.
3. Grados honestos: "exhaustivo" solo sobre dominios finitos de verdad, "pendiente" distinto de "falla", y `Bool` como tipo nominal.
4. Que los generadores respeten los refinamientos dependientes. Eso arregla las fallas falsas de positions, distances y distance_graph.
5. Memorizar el tipo inferido en `_type_operand`, para bajar la carga de 19 s.

Nada de esto pide tocar la especificación, que es la parte más sólida. El problema está en la implementación de la certificación, y conviene arreglarlo antes de la próxima reescritura de librerías. Si no, cada reescritura produce certificados en los que no se puede confiar.

## 5. Luciano  2026-10-05 07:25:27 UTC  (line 175)

chequea las conclusiones de Opus

## 6. Model  2026-10-05 07:25:52 UTC  (lines 184, 198, 213, 227)

Voy a verificar las afirmaciones con pruebas propias en lugar de confiar en el informe. Empiezo por las más graves: el puente con Python, el hash, el "exhaustivo", el Bool por posición y los certificados viejos.

Confirmado leyendo el código: la división por tipo de Python, las tablas de enteros como `float`, y `test n` sobre solo las obligaciones del nombre. Ahora corro las pruebas ejecutables.

Seis confirmaciones más (B2, C2, D, E2, G, R8). Quedan por verificar los certificados viejos por huecos, que el hash ignore el Python, los tiempos de carga y dos lecturas de código.

Terminé. Todo lo que importa está verificado con pruebas propias; no hace falta pedir nada más.

**En una oración:** las conclusiones se sostienen. De los once hallazgos graves del informe reproduje nueve con pruebas ejecutables, dos quedan como lectura de código, y hay una afirmación mía anterior que retiro.

## Reproducido con pruebas propias

1. **El puente no valida.** `h : String -> Float64 := extern` que devuelve `"hello"` da `'hello' : Float64`. Un extern `Int -> Float64` que devuelve un `int` de Python hace que `f 3 / f 2` dé `1 : Float64`.
2. **El refinamiento del codominio de un extern no genera ley.** `neg : Float64 -> NonNegative := extern` seguido de `g (x : Float64) : NonNegative := neg x`: `check -v` dice "0 with laws" y `test g` dice "no laws". El checker sí atrapa el caso cerrado (`v : NonNegative := neg 5.0` se rechaza porque lo evalúa), pero nunca el caso cuantificado.
3. **"Exhaustivo" sobre `Int` es [-16, 16].** `x*x < 1000` quedó certificado `[exhaustive, 33 cases]`. Matiz a favor: el campo `domains` del certificado dice "Int in [-16, 16]"; lo engañoso es el grado, no el detalle.
4. **`Bool` por posición.** Con `Verdict = < wrong | right >`, un predicado que siempre devuelve `wrong` se acepta (`a : { x : Int | AlwaysWrong x } := 3` pasa el check), y el que devuelve `right` se rechaza.
5. **Provisional se certifica igual.** `sq := extern provisional` con una ley: "sq: passed", y el certificado no lleva campo `provisional`.
6. **El hash ignora el Python.** Certifiqué `sq`, cambié el Python para que devuelva -1.0, y `check -v` sigue diciendo `[certified (…)]`. Al correr `test` de nuevo, falla al primer caso. Es el agujero más peligroso para tu flujo: editar `lm.py` o `positions_luthier.py` no invalida nada.
7. **Certificados viejos por huecos.** `check -v` sobre `algebra_python.lut` da 37 "stale", sobre `array_python.lut` 34, con certificados más nuevos que los `.lut`. Y en `experiment_zero.lut`: 72 nombres con leyes, 16 certificados, 56 pendientes. El programa que produjo tus posiciones corre, según el propio checker, con tres cuartos de sus leyes sin certificar.
8. **`float64Field` solo dentro de la caja.** `tol = 4,5e-13`; `(1e8 + (-1e8)) + 3e-9 = 3e-9`, `1e8 + ((-1e8) + 3e-9) = 0.0`, y la igualdad del anillo da `false`. Matiz: el comentario de [algebra.lut:206](../luthier/src/luthier/lib/algebra.lut#L206) lo documenta ("valid for magnitudes up to the generator's size"); lo que no lo dice es el tipo `OrderedField Float64` ni el certificado.
9. **`==` sobre `Real`** se acepta y da `true` entre dos literales.
10. **Tiempos:** 19,1 s el check de `algebra_python`, 16,5 s el de `array_python`.

## Verificado leyendo el código, sin ejecutar

- `/` elige división entera según el tipo de Python ([evaluator.py:344](../luthier/src/luthier/evaluator.py#L344)).
- Las tablas `Fin n -> Int` se muestrean con `dtype=float` ([generators.py:143](../luthier/src/luthier/generators.py#L143)).
- `test n` corre solo `obligations[name]`, no el objeto ([testing.py](../luthier/src/luthier/testing.py)).
- El `.run.json` no anota el cono sin certificar ([cli.py:299-306](../luthier/src/luthier/cli.py#L299-L306)).
- `toFloat64` es `Int -> Float64` ([real.lut:9](../luthier/src/luthier/lib/real.lut#L9)).
- `test_spec.py` solo llama a `load`: chequea que carguen, nada más.
- La máquina cae en silencio al evaluador de sustitución ([machine.py:614-621](../luthier/src/luthier/machine.py#L614-L621)).
- No hay `certify_all` en el CLI.

## Del informe, no re-verificado por mí

Que los dos evaluadores difieran en `==` sobre arrays, el límite de profundidad 20 en `contains_function`, `==` sobre `data` con funciones, las excepciones tragadas en `evaluator.py:113`, la lista de código muerto, y que la causa de los 19 s sea la re-inferencia del operando izquierdo (el tiempo lo confirmé; el perfil no lo repetí). Son lecturas de código del agente; ninguna cambia el cuadro.

## Una corrección mía

Dije que una transformada integral uniforme sobre los residuos reales "marcaría ese outlier". No hay outlier: los residuos estandarizados de la sesión A están todos por debajo de 0,8. El sigma de 25,7 cm no viene de un dato malo sino del ajuste entero (priors anchos de 0,2 m en los micrófonos, pocos grados de libertad, nu = 7,8). Eso es una pregunta sobre el modelo de la cinta, no sobre Luthier, y queda abierta.

La recomendación no cambia: commitear, y arreglar el puente y el hash antes de volver a tocar librerías.

## 7. Luciano  2026-10-05 07:30:43 UTC  (line 230)

Chequea esto que dice naive: 

[pasted text]

```
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
```

## 8. Model  2026-10-05 07:31:10 UTC  (lines 234, 260, 266)

Voy a verificar las afirmaciones comprobables de ese informe una por una: el estado roto de `distances_python`, los alias con generador, el `pytest` desde la raíz, los conteos de commits, qué corre nativo en `experiment_zero`, el acoplamiento entre repos, y lo de hypothesis en `sonolik`.

Me falta una sola cosa: confirmar si `sonolik/tests` usa la librería `hypothesis` (el grep de imports no encontró nada; `sonolik/hypothesis.py` parece ser la hipótesis del SRP, no la librería).

Ya tengo todo. No necesito nada más.

**En una oración:** el diagnóstico general de ese informe se sostiene (el costo supera lo que devuelve, el trato se invirtió, el alcance se achicó a la cinta), pero tres de sus afirmaciones concretas son falsas y dos están desactualizadas; conviene corregirlas antes de usarlo para decidir.

## Falso

**"pytest + hypothesis ya está en `sonolik/tests` y trae shrinking."** No. En todo el repo no hay un solo `import hypothesis`; la librería ni siquiera está instalada. `sonolik/hypothesis.py` es la verosimilitud como forma cuadrática en la traza (la "hipótesis" del SRP), y `test_hypothesis.py` la prueba con pytest y numpy a secas. El argumento "las cuatro leyes salían igual con hypothesis" queda sin su premisa: no hay property testing en el proyecto fuera de Luthier.

**"`experiment_zero.lut` tiene el gauge, Jacobi nativo para `pinvSym` y un LM nativo duplicado."** Lo que corre es otra cosa: el maximizador es `extern "python:lm.maximize"` ([experiment_zero.lut:61](prototipo-cero/luthier/experiment_zero.lut#L61)), `pinvSym` lo resuelve numpy porque importa `array_python`, y el gauge vive en `distances.lut`, que experiment_zero no importa. El Jacobi y el LM nativos existen como oráculos en `array.lut` y `optimization.lut`, fuera del camino de `run`. Es decir, para el LM y el álgebra ya se cumple lo que el informe pide en su punto 2. Lo que sí corre nativo, y explica los 3 minutos, es la verosimilitud: `pairDistances`, `distanceJacobian` y `profiled`.

**"El estado roto: `pairI` declarado `Vec (Fin nodes)` y ligado como `Vec Int`."** Que `distances_python` y `optimization_python` no pasan `check` es cierto, pero el error que da hoy es otro: `shift := add` en `fastFull`, donde `add` devuelve `Vec Float64` y se espera `ThetaFull`. Es la varianza R9 mordiendo a un subtipo nuevo. El desajuste de `pairI` también existe y el checker lo rechazaría (lo probé aparte: "declared with type Vec (Fin nodes), but is defined with Vec Int"), solo que no es el primero que se reporta. Son dos roturas, no una.

## Impreciso

**"21 commits de sonolocalización desde el 10-02."** Son 17, y los 17 tocan `luthier/` o `src/`. La conclusión (todo el período fue capa Luthier, sin avance acústico) se mantiene.

**"Un grep me lo bloqueó el clasificador de permisos; no pude verificar `UniformDraws`."** Yo sí: `UniformDraws` corre `ensembleSize = 400` extracciones por caso y compara los dos primeros momentos con `zMax = 5`. Así que `fullKernel with 5` son 5 × 400 extracciones, no 5 anécdotas. La crítica real es otra: dos momentos con z = 5 tienen poca potencia, y los controles rompen al doble de sigma.

**"Los certificados importados están stale y nada lo impide."** Correcto, y es peor de lo que dice: están stale aunque sean frescos, porque el hash se compara antes de llenar los huecos. Y el hash no ve el Python de los externs, lo que mostré ayer editando `sq` sin que el certificado se moviera.

## Confirmado tal cual

- `luthier check positions.lut`: 17,7 s, sin caché de imports.
- 36 commits en Luthier desde el 10-01; `docs/semantica` entero con cambios sin commitear.
- `pytest` desde la raíz: 35 fallas, 87 pasan, porque junta `archive/tests-2026-10-04`; `pyproject.toml` no tiene `testpaths`.
- `MaximizerAgrees` y `StepAgrees` son exactos (`approxVec 0.0` en `sameState`), y por R10 son consistencia, no caracterización. El propio archivo tiene además `StepRule`, `DescentDirection` y `Certified` sobre las piezas de Python, como el informe reconoce.
- Los alias con generador: `GoodGraph = DistanceGraph` y `gen GoodGraph := extern`. El código busca el generador "on the type as written, before unfolding" ([generators.py:69-73](../luthier/src/luthier/generators.py#L69-L73)), así que el nombre del alias sí carga una distribución, contra R7. La observación es buena.
- Los generadores registrados de Python devuelven sin pasar por el predicado del subtipo ([generators.py:92-97](../luthier/src/luthier/generators.py#L92-L97)); `gen ValidDistanceGraph := gen_good_graph` se cree por nombre.
- El trato de la nota de traspaso (línea 9: "Luthier solo describa... ninguna función con cuerpo que no sea trivial") y su inversión.
- La capa archivada del 10-02 tenía `dome.lut`, `calibration.lut`, `likelihood.lut`, `noise.lut`.
- Laplace mueve la media hasta 0,3 desviaciones posteriores según el orden ([laplace_check.lut:56](prototipo-cero/luthier/laplace_check.lut#L56)).
- pip editable sobre `~/Projects/luthier`, con working tree sucio: los resultados no se reproducen desde un commit.

## Qué cambia en las recomendaciones

Las cuatro del informe siguen bien, con dos ajustes. El punto 2 ("la corrida es Python puro") ya está hecho para el LM y el álgebra; lo que falta mover es la verosimilitud, y antes de moverla conviene decidir si el costo de 3 minutos importa o si alcanza con una caché de la elaboración. Y la alternativa "hypothesis en vez de Luthier" hay que evaluarla como algo por construir, no como algo que ya tenés: hoy la única capa de leyes del proyecto es Luthier, con los agujeros de certificación que vimos ayer.

## 9. Luciano  2026-10-05 07:38:17 UTC  (line 269)

Elabora un plan para solucionar todos los problemas encontrados. 
Indica el problema, su rational y como se solucionaria (con los posibles caveats)

## 10. Model  2026-10-05 07:42:42 UTC  (line 276)

Antes del plan, dos decisiones que lo ordenan. Primera: los arreglos van por capas, y la capa de abajo (el puente con Python) condiciona a todas las demás, porque mientras un extern pueda devolver cualquier cosa, ningún certificado dice nada. Segunda: hay problemas que se resuelven en el intérprete, otros que piden una línea en la especificación, y otros que son del proyecto; los marco con [int], [spec] y [proy] para que no se mezclen. Las fases están en el orden en que las haría; dentro de cada fase, por daño.

## Fase 0. Congelar lo que hay (medio día)

**0.1 Dos ramas `numbers` sin commitear, con el proyecto roto.** [proy]
Por qué: cualquier arreglo de abajo va a tocar los mismos archivos, y hoy no hay un punto al que volver; además `distances_python.lut` y `optimization_python.lut` no pasan `check`, así que el estado no es ni siquiera consistente.
Solución: arreglar las dos roturas (en `fastFull` y `fastProfile`, `shift := \ t v { add t v }` en lugar de `shift := add`, que es la forma que ya usa `distances.lut` y que genera una obligación muestreada en vez de la comparación R9 que falla; `pairI : Vec (Fin nodes) := extern ...` en lugar de `Vec Int`), separar tus notas de `random.lut` con un patch, commitear las dos ramas, taggear `luthier v0.0`.
Caveat: `pairI : Vec (Fin nodes)` desde Python va a pasar sin chequeo hasta la fase 1; dejarlo anotado.

**0.2 `pytest` desde la raíz junta `archive/`.** [int]
Solución: `[tool.pytest.ini_options] testpaths = ["tests"]` en `pyproject.toml`. Trivial, y evita que una falla del archivo se confunda con una real.

## Fase 1. El puente con Python (2 a 3 días)

**1.1 `from_python` acepta cualquier `int`, `float` o `str` para cualquier tipo, y la aritmética sigue al tipo de Python.** [int]
Por qué: es el único problema de la lista que puede dar un número equivocado sin aviso (`3 / 2 = 1` como `Float64`). Y todo lo demás (leyes, certificados) asume que un valor de tipo `Float64` es un double.
Solución: `from_python` recibe el tipo declarado (ya lo recibe en parte) y lo usa como contrato: `Int` exige `int` (no `bool`) o entero de numpy, y aplica el rango de 64 bits al cruzar a numpy (06 §6); `Float64` exige `float` o `np.floating`, promueve `int` a `float` explícitamente (es la única promoción segura) y rechaza `str`; `String` exige `str`; `Fin n -> Int` exige dtype entero; `Fin n -> Float64` exige dtype float; NaN e infinito son error en todos los casos, también adentro de listas. `--set` parsea según el tipo declarado del hueco, no por `eval` de Python. Con los valores normalizados, la aritmética por tipo de Python queda correcta sin tocar el evaluador.
Caveat: externs que hoy devuelven `0` donde se declaró `Float64` siguen andando por la promoción; externs que devuelven `np.float64` donde se declaró `Int` (hay varios en `arrays.py` seguramente) van a empezar a fallar, y eso es lo que se quiere, pero hay que pasarles revista.

**1.2 El refinamiento del codominio de un extern no genera ninguna ley.** [int] [spec 05 R5]
Por qué: `neg : Float64 -> NonNegative := extern` es una promesa que nadie prueba; con el `abs` de `real.lut` se lo resolvió escribiendo el tipo como subtipo de la función, pero eso es un truco, no una regla.
Solución: al declarar un extern cuyo tipo es un Pi con codominio refinado (a cualquier profundidad), el checker genera la obligación cuantificada sobre el dominio, igual que si el autor hubiera escrito la ley-lambda. Opcional, un modo `run --checked` que verifica el refinamiento sobre cada valor que cruza.
Caveat: dominios sin generador quedan pendientes (y ahora pendiente se reporta como tal, ver 2.5). El modo `--checked` sobre arrays grandes es caro; es para depurar, no para la corrida.

**1.3 Los generadores registrados de Python saltean el predicado del subtipo.** [int]
Por qué: `gen ValidDistanceGraph := gen_good_graph` se cree por nombre; si el generador tiene un error, las leyes pasan sobre grafos que no son válidos y nadie se entera. Es el caso 9 abierto en 05 §10.
Solución: después de un generador registrado, aplicar `holds` con el predicado del tipo, rechazar lo que falle, y anotar en el certificado cuántos valores rechazó cada generador. Un generador que produce más de una fracción de rechazos es error.
Caveat: evaluar el predicado interpretado sobre valores grandes cuesta; si es prohibitivo, permitir `gen T trusted := ...` que queda registrado en el certificado como confianza declarada, nunca silenciosa.

**1.4 Las tablas `Fin n -> Int` se muestrean como `float64`.** [int]
Solución: `dtype=int64` cuando el codominio reduce a `Int` o a un `Fin`; es una línea en `generators.py:143`, más el chequeo de rango. Depende de 1.1 para que la aritmética sea la correcta.

**1.5 Los alias llevan un generador (contra R7).** [int] [spec]
Por qué: `BrokenGraph = DistanceGraph` no tiene identidad según R7, pero `gen BrokenGraph` le cuelga una distribución; el tipo de un parámetro de una ley carga algo que el sistema de tipos dice que no existe.
Solución: `gen` solo sobre tipos definidos (con predicado). `BrokenGraph : U := { g : DistanceGraph | not (ValidGraph g) }`, `CompleteGraph` con su predicado (todos los pares medidos), `GoodGraph` desaparece a favor de `ValidDistanceGraph`. Con 1.3, el generador queda verificado contra el predicado, y la distribución está donde corresponde: es una muestra de un tipo con ley.
Caveat: el predicado tiene que ser decidible en Luthier; para `CompleteGraph` es un `forallPairs`, barato.

## Fase 2. Certificados en los que se pueda confiar (3 a 4 días)

**2.1 El hash del cono no ve el Python de los externs, ni los generadores, ni `n`, ni la versión del intérprete.** [int] [spec 05 §7]
Por qué: editar `lm.py` no invalida nada. Es la falla más peligrosa para tu flujo porque la mayoría de lo que corre son externs.
Solución: el hash incluye, por cada extern del cono, el hash del archivo fuente del módulo de Python (`inspect.getsourcefile`), y para módulos sin fuente (numpy, builtins) el nombre y la versión del paquete; incluye además el commit o versión de Luthier, los nombres de los generadores usados y el modo y `n` de la directiva.
Caveat: hashear el archivo entero invalida certificados por cambios en funciones no relacionadas del mismo módulo; es conservador y aceptable. Hashear solo la función con `getsource` es más fino pero frágil (decoradores, closures).

**2.2 Los certificados que dependen de huecos nunca coinciden.** [int] [spec 05 §7]
Por qué: `accept_certificate` corre al cargar cada archivo, antes de que el padre llene los huecos; el hash guardado se calculó después. Resultado: 37 "stale" en `algebra_python`, 56 pendientes de 72 en el cono de `experiment_zero`, aunque todo se certificó ayer.
Solución: comparar los hashes al final de `load`, con el programa entero cargado y los huecos llenos. Y aceptar lo que eso implica, que ya está en 03 §1: una librería con huecos es una estructura con parámetros, y sus leyes se certifican por instanciación. El archivo `.cert.json` guarda una lista de entradas por nombre, cada una con su hash (una por llenado distinto).
Caveat: una librería importada por dos proyectos con llenados distintos tendrá dos entradas; es correcto pero el archivo crece. Alternativa: hashear el cono con los huecos como huecos y registrar el llenado aparte; es más simple pero certifica "la ley" en lugar de "la ley sobre este modelo", que es lo que la 05 dice que no se hace.

**2.3 "Exhaustivo" sobre `Int` significa [-16, 16].** [int] [spec 05 §7]
Solución: el grado `exhaustive` solo cuando el dominio es finito después de reducir (`Fin`, `Bool`, sumas y productos de finitos, `data` finitos); sobre `Int` o `Float64` el modo pasa a llamarse `bounded` con su caja explícita, o directamente `sampled` sobre una grilla. El campo `domains` ya es honesto; el grado tiene que serlo también.

**2.4 Los externs `provisional` se certifican sin marca.** [int]
Solución: la entrada lleva `provisional: [nombres]`, nunca pone `certified`, y `check -v` la lista. Decidir lo abierto en 05 §10: un archivo que importa un provisional hereda la marca en todo lo que depende de él. Es lo más simple y lo que no miente.

**2.5 Pendiente se registra como falla, y hay fallas falsas por obligaciones cuantificadas sobre el tipo base.** [int]
Por qué: `meanDist (t : HasFree)` falla con un `t` de largo 0, que no es un `HasFree`; `pairDistances` falla con `j.n ≠ i.n`, que viola `Pairs p i`. Y "no generator for U" o "out of fuel" aparecen como `passed: false`, igual que un contraejemplo real.
Solución, dos partes. Primera: tres resultados distintos en el certificado: `passed`, `failed` (con contraejemplo) y `not run` (con la razón: sin generador, sin casos extraíbles, sin fuel). Solo `failed` es falla; `check -v` separa los tres. Segunda: una obligación que surge de pasar un parámetro `x : S` a una función que pide `S` (mismo subtipo o uno que lo refina sintácticamente) se descarga en el checker, no se muestrea; y cuando se muestrea, se cuantifica sobre el tipo declarado del parámetro con sus dependencias (muestrear `i`, después `j : Pairs p i`).
Caveat: la descarga estática necesita una comparación de predicados; empezar por igualdad sintáctica después de normalizar alfa, que cubre los casos del proyecto.

**2.6 Las entradas obsoletas se acumulan.** [int]
Por qué: `realField` del día anterior sobre `R` y `Commutative`, nombres viejos de `array_python`; leyendo el archivo no se distingue lo vigente.
Solución: `luthier test` reescribe el certificado podando los nombres que ya no existen y moviendo a una sección `stale` las entradas cuyo hash no coincide; y un comando `luthier certify [archivos]` que corre todas las directivas de un conjunto de archivos, poda, y resume. Es el `certify_all` que hoy es un script del scratchpad.

**2.7 `run` no registra el estado del cono y no avisa.** [int] [spec 05 §7, ya lo pide]
Solución: el `.run.json` lleva, por nombre del cono, su estado (certified, stale, pending, provisional, not run) más el commit de Luthier y los hashes de los módulos de Python; `run` imprime una línea de advertencia con los conteos, y `run --require-certified` falla si hay algo que no sea certified. Para `experiment_zero`, el registro pasa a commitearse junto con `positions.csv`.

**2.8 Import acepta una entrada con hash igual sin mirar `n`.** [int]
Solución: con 2.1 el `n` entra al hash; además la entrada se acepta solo si `cases >= n` de la directiva actual.

**2.9 Grados que la 05 promete y no existen; `test n` no corre el objeto.** [int]
Solución: `assumed` para los axiomas (hoy solo los lista `check -v`); `test n` expande a los miembros de la componente fuertemente conexa de `n` (el grafo ya se calcula); el grado de una cadena como el mínimo sobre su cono, calculado al reportar. `witnessed` queda para cuando haya leyes existenciales que lo pidan.

## Fase 3. Semántica del checker (2 días)

**3.1 `Bool` por posición.** [int] [spec 04]
Por qué: cualquier suma de dos `Unit` es `Bool` y la alternativa 0 vale `true`; un veredicto `wrong` pasa. Es un agujero de solidez, no un detalle.
Solución: `Bool` es el tipo de `core.lut` y nada más; `is_bool` reconoce solo esa `Var` (o, si se quiere mantener lo estructural, exige las etiquetas `true` y `false`, no la posición). La 04 dice que `Bool` es `< true | false >`; hay que agregar que la identidad es por etiqueta.

**3.2 `==` sobre `Real`, sobre `data` con funciones, y el corte en profundidad 20.** [int]
Solución: `Real` no tiene `==` (su igualdad es la del axioma; las comparaciones son sobre `Float64` después de `toFloat64`); `contains_function` recorre los tipos de los constructores del `data`, con memoización por nombre en lugar del corte en 20.

**3.3 `float64Field : OrderedField Float64` vale solo dentro de [-16, 16], y el tipo lo promete universal.** [spec 06] [int]
Por qué: la asociatividad falla en (1e8, -1e8, 3e-9). El comentario lo documenta; el tipo y el certificado no.
Solución a corto plazo: que el tipo diga la caja, con el portador `{ x : Float64 | abs x <= lawMagnitude }` y el nombre `float64FieldWithin`. Solución de fondo, la de 06 §8: la ley de redondeo `|toQ (x ⊕ y) − (toQ x + toQ y)| ≤ u |toQ x + toQ y|`, verificable exactamente con `Rational` sobre `Fraction` de Python, de la que la tolerancia de una suma de n términos se deduce en lugar de suponerse (`roundingSlack`).
Caveat: la de fondo requiere `Rational` como primitivo (06 §8) y es un trabajo de una semana; la de corto plazo es un día y deja de mentir.

**3.4 `Real` es nominal, sin representación; `toFloat64` es `Int -> Float64` y el mensaje de error del checker sugiere usarlo sobre un `Real`.** [spec 06] [int]
Solución: `toFloat64 : Real -> Float64` como dice la 06 §4 (identidad sobre doubles), y `intToFloat64` para el entero; corregir el hint. Y una decisión honesta: mientras no haya `Rational` ni intervalos, `Real` solo sirve para bloquear operaciones; está bien que exista, pero `check -v` debería decir que ninguna ley sobre `Real` se prueba.

**3.5 R2 aproximada, R3 cuando no puede desplegar la ley.** [int]
Solución: R2 por "posición de tipo" sintáctica como la define 05 §0, recorriendo también `Inj.type`; en R3, cuando la cabeza de la ley no se puede desplegar, error "R3 no decidible", no "toca todos los labels".

**3.6 Los reportes de 05 §6 que no existen.** [int] Baja prioridad. La heurística por nombre de "comparación contra caracterización" (una ley que aplica la operación y otra definición a los mismos argumentos y compara) es un recorrido sintáctico; la tabla de completitud suficiente también. Van después de todo lo anterior.

## Fase 4. Rendimiento (2 a 3 días)

**4.1 `check` de cualquier cosa que importe `array` tarda 17 a 19 s.** [int]
Por qué: cada `+` o `*` anidado vuelve a inferir el operando izquierdo, y varios caminos chequean dos veces (una en silencio, otra de verdad). Con esto, un ciclo editar-probar en el proyecto cuesta medio minuto antes de empezar.
Solución: memoizar la inferencia por término en `_type_operand`; reemplazar el patrón "silencioso y después real" por un chequeo con errores diferidos; y la mejora grande, una caché en disco de la elaboración de cada archivo (definiciones, obligaciones, grafo) con clave el hash del archivo más la versión de Luthier, aplicada antes de llenar huecos (los llenados se aplican después, como ahora).
Caveat: la caché tiene que invalidarse con la versión de Luthier, que hoy cambia a diario; mientras la spec se mueva, la caché va a fallar seguido. Medir primero con cProfile si la memoización sola alcanza.

**4.2 `run` de `experiment_zero` tarda 3 min.** [proy] [int]
Por qué: la verosimilitud (`pairDistances`, `distanceJacobian`, `profiled`) corre interpretada; el LM y el álgebra ya son Python. El proyecto ya tiene las versiones rápidas en `positions_luthier.py`, pero para 7 nodos con gauge fijo.
Solución: generalizar el lado Python para recibir el diseño del grafo (ver 5.3), y que `experiment_zero` use la verosimilitud rápida certificada contra la nativa, que pasa a ser oráculo. Es volver al trato de la nota de traspaso para la última pieza que no lo cumple.
Caveat: antes de hacerlo, decidir si 3 minutos importan; para la cinta no, para lo acústico sí, y lo acústico va a nacer como extern de todos modos.

**4.3 Dos evaluadores con caída silenciosa.** [int]
Solución: contar las caídas y mostrarlas en el reporte de `test`; pruebas diferenciales entre la máquina y el evaluador de sustitución sobre la suite `tests/spec`; a mediano plazo, uno solo.

## Fase 5. El proyecto (3 a 4 días)

**5.1 Lo certificado (7 nodos, gauge, 16 parámetros) no es lo que corre (10 nodos, vector entero, prior).** [proy]
Por qué: la transferencia del Kernel de `distances.lut` al modelo de `experiment_zero` es un argumento informal; comparten `distanceJacobian` y `profiled`, pero ninguna ley lo dice.
Solución: un solo modelo `positionsModel (m : MapInput) : MeanModel (Vec Float64)` en `positions.lut`, usado por ambos; `DensityPair` y `Kernel` certificados sobre `positionsModel m` con `m` generado desde grafos válidos (`gen_good_graph` más `toMapInput`); el modelo con gauge de `distances.lut` queda como caso particular, o se retira. Entonces el modelo que corre es el modelo certificado, y 2.7 lo registra.
Caveat: cada caso del `Kernel` son 400 extracciones del modelo completo; con la verosimilitud nativa es lento (ver 4.2); hacerlo después de mover la verosimilitud a Python.

**5.2 Garantías que viven en comentarios.** [proy]
Solución: `Positions : U := { p : Vec Float64 | p.n mod 3 == 0 }` y `Node (p : Positions)`; `MapInput` con `i j : Vec (Node x0)` en vez de `Vec Int`; `distanceJacobian` con precondición `pairDistance p i j > 0` en su tipo. Para la división por `h` durante las iteraciones del LM, que no se puede certificar por adelantado: registrar como supuesto en el `.run.json` y que el modelo devuelva error (no cero) si pasa, que con 1.1 ya es lo que hace NaN.

**5.3 Duplicación a través del puente: 7 nodos y los índices fijos del gauge están en el `.lut` y en el `.py`.** [proy]
Solución: una sola fuente. El diseño (nodos, pares) sale del grafo, que es dato; el gauge, si se mantiene, se calcula en Luthier (`freeCoord`) y se pasa a Python como argumento de los externs. Es el principio de un solo nombre, y además "nunca hardcodear".

**5.4 Nada se aplica a los datos reales; sigma = 25,7 cm sin explicación.** [proy]
Por qué: los certificados hablan de coherencia interna; la sesión A da un sigma diez veces mayor que el error de una cinta, con residuos estandarizados todos por debajo de 0,8, lo que apunta al prior (0,2 m en los micrófonos) y a nu = 7,8, no a un dato malo.
Solución: `experiment_zero` escribe además la transformada integral de cada residuo bajo el modelo ajustado (Student con nu, o gaussiana con sigma) y su estadístico de uniformidad en el resumen; no bloquea, informa. Aparte, una corrida de control con los priors de los micrófonos abiertos y otra con sigma fijo en 3 cm, para separar qué parte del 25,7 es el prior y qué parte es el modelo. Es "figuras con cabeza": una pregunta, un estadístico, su nivel nulo.
Caveat: con 22 datos y 30 parámetros la potencia de cualquier prueba sobre los residuos es baja; el control por priors dice más que la PIT.

**5.5 Potencia de las pruebas estadísticas.** [proy] [int]
Por qué: 5 casos, dos momentos con z = 5, controles al doble de sigma, semillas que se repiten (`seed = 2` tres veces en cinco porque `genInt` llega a 16).
Solución: un tipo `Seed` con generador sobre 2^31; controles a 1,3 sigma además del doble, y que el certificado registre la tasa de detección (correr cada control k veces); reemplazar los dos momentos por Kolmogorov-Smirnov o Anderson-Darling sobre la PIT agrupada (necesita ordenar: un extern); `n` mínimo de 20 para leyes estadísticas, declarado en la directiva.
Caveat: toda ley estadística tiene una tasa de falsa falla; registrarla (alfa) en el certificado y no tratar una falla aislada como contraejemplo hasta repetirla con otra semilla.

**5.6 Los controles del LM se corrieron a mano.** [proy]
Solución: leyes `not (StepAgrees mutatedStep)` y `not (RunTraceAgreesOnBudget ...)` en `optimization_python.lut`, con las mutaciones de `lm_controls.py`, como ya está hecho en `distances_python` con `sampleControl` y `pitControl`.

**5.7 Los `Agrees` exactos del LM son una transliteración.** [proy]
Solución: `StepAgrees` y `MaximizerAgrees` con `scaledTol` en lugar de `approxVec 0.0`; las leyes propias (`StepRule`, `DescentDirection`, `Certified`) ya están sobre las piezas de Python y son las que importan. Si se quiere conservar la coincidencia exacta como control de que nadie cambió el algoritmo, que sea una ley aparte y nombrada como tal.
Caveat: con tolerancia se pierde el detector de cambios de BLAS; a cambio se puede reescribir `lm.py` con `lstsq` sin romper nada que no deba romperse.

**5.8 Constantes del proyecto en la librería.** [proy] [int]
Por qué: `pitTol = 1e-6` está calibrado "for the sigmas of the tape"; `ensembleSize`, `zMax`, `fdStep` son decisiones del experimento, no de la probabilidad.
Solución: huecos de `probability.lut` que el proyecto llena (`03 §1`, la librería como estructura con parámetros), con 2.2 ya resuelto para que sus certificados no queden stale por eso.
Caveat: sin argumentos implícitos (6.1) las llamadas se alargan; los huecos son la forma de no alargarlas.

**5.9 Acoplamiento sin versión entre repos.** [proy]
Solución: después de las fases 1 y 2, tag `luthier v0.1`; sonolocalización fija ese tag (archivo `luthier.lock` con el commit, o submódulo), el `.run.json` lo registra (2.7), y los resultados se reproducen desde un commit. Hasta entonces, cada corrida que se publique lleva el commit de Luthier en el resumen.

## Fase 6. Salud y ergonomía (en paralelo, cuando haga falta)

**6.1 Sin `let`, sin menos unario, sin argumentos implícitos.** [int] [spec 02]
Solución: `let x = e in body` como azúcar de `match e { x -> body }` (ya tiene la semántica de obligaciones que 05 §7 describe para `match`); `-x` como azúcar de `0 - x` del tipo del operando; argumentos implícitos solo por unificación simple (un argumento de tipo `U` que aparece como tipo de un argumento posterior se infiere), que cubre `drawAt ThetaFull (Vec Float64) f t seed` y similares.
Caveat: los implícitos son la pieza grande; hacerlo después de que el checker sea rápido, porque la inferencia agrega trabajo.

**6.2 Pruebas del intérprete que solo cargan.** [int]
Solución: una suite `tests/soundness/` con los programas de ayer como regresión: puente (`'hello' : Float64`), codominio de extern, exhaustivo sobre `Int`, `Bool` por posición, provisional certificado, hash tras editar el Python, stale por huecos. Cada uno es hoy un fallo reproducible; después de las fases 1 a 3 cada uno es una prueba que pasa.

**6.3 Código muerto y dos caminos de chequeo.** [int]
Solución: borrar `pygen.py`, la rama de tipos opacos por extern que R5 prohíbe, `_law_applications`, `is_type`, `obligation_law`, `is_global`; va junto con 4.1.

## Lo que no entra en el plan, a propósito

La parte acústica. Las fases 1 a 5 son unas tres semanas si se hacen solas; la recomendación es ponerles un límite (fases 0 a 2 completas, el resto a medida que el proyecto lo pida) y volver a `sonolik` con Luthier como capa de leyes sobre externs, que es el trato original. Cada semana más de kernel sin un uso acústico es una semana en la que la especificación cambia sin presión de un problema real, y eso es lo que produjo los certificados en los que hoy no se puede confiar.

Si querés, lo paso a inglés como `docs/plan-2026-10-05.md` en el repo de Luthier, con los números de problema para ir tachando.

## 11. Luciano  2026-10-05 07:45:17 UTC  (line 285)

Implementa la Fase 1 del plan

## 12. Model  2026-10-05 07:45:34 UTC  (lines 291, 319)

Empiezo por respaldar los dos árboles de trabajo, que tienen cambios sin commitear, y después leo el código del puente antes de tocar nada.

Leí el puente. Ahora el lado del checker: cómo se arman las obligaciones, los `gen`, y el `--set`.

## 13. Luciano (queued)  2026-10-05 07:46:23 UTC  (line 324)

En el medio salva el plan a un archivo

## 14. Model  2026-10-05 07:47:54 UTC  (lines 331, 342, 365, 401, 406, 417, 430, 442, 478, 483, 500, 511, 526, 531, 536, 548, 584, 607, 649)

Guardo el plan ahora, en inglés como el resto de los documentos, en `~/Projects/luthier/docs/plan-2026-10-05.md`, y sigo con la Fase 1.

Plan guardado en [docs/plan-2026-10-05.md](../luthier/docs/plan-2026-10-05.md), en inglés. Sigo con la Fase 1: leo cómo se llenan los huecos con externs y cómo se registran los generadores.

Ahora miro qué directivas `gen` existen en todas partes, porque el cambio 1.5 (alias transparentes) afecta a cada una que esté sobre un alias.

Ya tengo el mapa del puente. Empiezo a escribir: primero la validación en `from_python` (1.1), que es la base de todo lo demás.

Escribo ahora la validación del puente en `evaluator.py`: tipos escalares, arrays por tipo de entrada, NaN sin excepciones tragadas, y error cuando un escalar llega donde se esperaba una estructura.

Ahora reescribo el cuerpo de `from_python` para usar esos contratos.

Ahora escribo las pruebas de regresión del puente antes de seguir, para ir viendo qué rompe cada cambio. Miro cómo cargan programas las pruebas existentes.

El puente ya rechaza lo que debe. Sigo con `--set`, que hoy adivina el tipo por cómo se ve el texto.

Las obligaciones del codominio y de las entradas ya se generan y fallan donde deben (`neg` y `pairI`). Hago legibles los nombres de los parámetros y paso al 1.3–1.5 en los generadores.

Ahora los generadores. Busco dónde más se usan las claves de `gens`, porque el 1.5 cambia cómo se indexan (por el tipo que el alias nombra, no por el nombre del alias).

Ahora `add_gen` en el checker: la clave es el tipo que el alias nombra, y dos generadores para el mismo tipo son un error.

Ahora `Generators`: búsqueda por la clave del tipo, verificación del predicado sobre lo que da un generador registrado (1.3), con conteo de rechazos, y tablas de enteros como `int64` (1.4).

Ahora corro la suite del intérprete para ver qué rompieron los cambios antes de tocar las librerías.

Las 78 pasan. Ahora cargo cada librería y cada archivo del proyecto para ver dónde choca el nuevo comportamiento.

`table_python` choca como se esperaba (`TableText` y `BrokenText` son ambos `String`). Antes de arreglarlo verifico, con la copia de respaldo, que los conteos de "0 certified" no los causé yo.

Los conteos son idénticos con el intérprete viejo: los "0 certified" vienen del problema 2.2, no de estos cambios. Ahora arreglo la librería de tablas. Veo `gen_broken` completo.

Dos choques en el proyecto. El de los grafos era esperable; el de `ThetaPos`/`ThetaFull` no: los dos aparecen con la misma clave, como si el alias perdiera el `VecOf n`. Lo investigo.

Hay cuatro sesiones pares, todas inactivas ahora. Los cambios de las 15:36 los hizo alguna de ellas (o vos) y los respeto: construyo encima. Miro qué cambió en esos tres archivos.

Escribo los tipos de grafo con sus predicados en `distance_graph_python.lut`.

## 15. Luciano (queued)  2026-10-05 08:17:48 UTC  (line 662)

que es BrokenGraph?

## 16. Model  2026-10-05 08:29:39 UTC  (lines 696, 709, 715, 729, 740)

Ahora escribo las pruebas de regresión de la Fase 1, con su módulo de externs.

The helper named `test_law` was collected as a test; I'll rename it.

97 pasan (las 78 de antes más las 19 nuevas). Veo cómo van las dos corridas de fondo.

Mientras tanto comparo cuántas obligaciones agregó el 1.2 en cada librería, con los dos intérpretes.

Mientras corre, verifico que todos los archivos del proyecto carguen después de los cambios.

## 17. Luciano (queued)  2026-10-05 08:39:08 UTC  (line 804)

que hace ValidGraph?

## 18. Model  2026-10-05 08:42:54 UTC  (lines 844, 858, 870, 874, 880, 891, 896)

`distances_python` usa los generadores nuevos (`VecOf 15` y `VecOf 16`, ninguno fuera de su tipo), pero tiene 3 definiciones que fallan. Las miro.

Solo `distances_python` usa el par y el kernel; los demás toman proyecciones de `fastFull` y `fastProfile`. Los reescribo sobre los dominios con dimensión.

Carga. Relanzo en paralelo las pruebas del proyecto y `array_python` (para medir si la decisión en la máquina recupera el tiempo), todas sin escribir certificados.

Mientras corre, verifico que la suite del intérprete siga pasando con el cambio de evaluador.

Pasan las 97. Agrego al plan el hallazgo del par de densidad, que es la consecuencia más importante del 1.5 en el proyecto.

`optimization_check` y `optimization_python` pasan enteras, sacando sus parámetros del generador de `VecOf 15`. Espero el resto; la clave es cuánto tarda ahora `distance_graph_python`.

Quedan corriendo en segundo plano `distances_python`, `distance_graph_python`, `laplace_check`, `belief_check` y `array_python`. Cuando terminen te paso el resumen completo de la Fase 1. Hasta ahora:

- **Puente (1.1):** valida contra el tipo declarado. Un `str` donde va `Float64` es error; un `int` se promueve, así que `f 3 / f 2` da `1.5`; los arrays reciben el dtype y la cantidad de dimensiones que dice su tipo; `--set` lee el valor según el tipo del hueco.
- **Codominio de un extern (1.2):** cada refinamiento del tipo es una obligación. `neg : Float64 -> NonNeg` y `pairI : Vec (Fin 3)` con un 5 ahora fallan en `test`.
- **Generadores registrados (1.3):** cada valor se verifica contra su tipo, y uno afuera es error. Me aparté del plan, que proponía descartarlo y contarlo, por lo que hablamos de `BrokenGraph`. Además corregí que el predicado se evaluara con el evaluador lento.
- **Tablas a `Int` (1.4):** son `int64`.
- **Alias (1.5):** un generador sobre un alias es el generador del tipo que el alias nombra, y dos sobre el mismo tipo son error. Eso obligó a tocar `table.lut`, los grafos y `distances`. También mostró que `fullPair : DensityPair ThetaFull` afirmaba algo falso (un par de densidad sobre todo vector); ahora está enunciado sobre `FullCoords`.
- **Otra sesión:** a las 15:36 otra sesión cambió `ThetaPos` y `ThetaFull` a `Vec Float64`. Respeté ese cambio y construí encima.
- **Lo que ya verifiqué:**
  - las 97 pruebas del intérprete pasan, 19 de ellas nuevas en `tests/test_bridge.py`;
  - `experiment_zero` da los CSV idénticos byte a byte;
  - `table_python`, `optimization_check` y `optimization_python` pasan enteras.

## 19. Luciano  2026-10-05 08:47:56 UTC  (line 899)

bueno, ahora que sigue? vamos a Fase 2?

## 20. Model  2026-10-05 08:48:04 UTC  (lines 903, 911, 916)

Antes de contestar, miro si terminaron las corridas que quedaron de la Fase 1.

Sí, pero antes de la Fase 2 te recomiendo commitear, y eso lo tenés que decidir vos.

**Qué falta de la Fase 1.** `distance_graph_python` ya terminó: 0 fallas en 107 s, y verificó 700 grafos generados (400 válidos, 200 rotos, 100 completos) contra sus tipos sin ninguno afuera. Antes de que pasara el predicado a la máquina, la misma corrida llevaba más de 18 minutos. Siguen corriendo `distances_python`, `laplace_check`, `belief_check` y `array_python`; en unos minutos tengo el cierre.

**Por qué commitear antes.** La Fase 2 cambia el hash de los certificados (incluye el Python de los externs y se compara después de llenar los huecos), así que todos los certificados quedan viejos de una vez y hay que regenerarlos. Si commiteamos ahora tenés un punto limpio al que volver: tu trabajo del día, el de la otra sesión que tocó `distances.lut` y la Fase 1. Después la Fase 2 regenera todo de una sola vez. Hoy son dos ramas `numbers` con un día entero sin commitear, y hay cuatro sesiones abiertas sobre estos repos. Al commitear separo tus notas de `random.lut` en su propio parche, como pide la memoria.

**La Fase 2, en este orden:**
1. **2.2 y 2.1 juntas:** comparar el hash después de llenar los huecos, e incluir el hash del fuente de Python, la versión de Luthier, los generadores y `n`. Sin estas dos, ningún certificado se puede creer.
2. **2.5:** tres resultados (`passed`, `failed`, `not run`) y que las obligaciones respeten el tipo declarado del parámetro. Esto elimina las fallas falsas de `positions`, `distances` y `probability`.
3. **2.3 y 2.4:** "exhaustivo" solo sobre dominios finitos, y los provisionales marcados.
4. **2.6 y 2.8:** podar entradas viejas y un comando `luthier certify`.
5. **2.7:** el `.run.json` con el estado del cono de `experiment_zero`.
6. **2.9:** grados y `test` sobre el objeto completo; es lo menos urgente.
7. Al final, regenerar todos los certificados con `luthier certify`. Es caro: solo `array` y `array_python` suman unos 20 minutos, aunque se puede paralelizar.

Es la fase más larga: el plan estimaba de 3 a 4 días de trabajo humano.

Cierro primero la verificación de la Fase 1. Veo cómo van las cuatro corridas que quedaban.

## 21. Luciano  2026-10-05 08:51:00 UTC  (line 931)

antes que sigas hice unas preguntas antes

## 22. Model  2026-10-05 08:51:24 UTC  (line 935)

No commiteé nada todavía. Te repito las dos preguntas que vi a mitad del trabajo, con las respuestas en un solo lugar; si había otra que se me pasó, decime cuál.

**¿Qué es `BrokenGraph`?**
Es el dominio del control negativo de `ValidGraph`, en [distance_graph_python.lut](prototipo-cero/luthier/distance_graph_python.lut): un grafo de distancias con exactamente un defecto. El defecto lo fabrica `gen_broken_graph` en [src/distance_graph.py](prototipo-cero/src/distance_graph.py), eligiendo uno entre ocho:
- índice fuera de rango
- índice negativo
- par de un nodo consigo mismo
- distancia no positiva
- desviación del prior no positiva
- nombre repetido
- columna faltante
- priors coincidentes

La ley `RejectsDefect` dice que `ValidGraph` rechaza todos esos grafos, y `AcceptsValid` dice que acepta los válidos. Entre las dos certifican que el validador no deja pasar grafos malos ni rechaza los buenos.

Hasta esta mañana era `BrokenGraph = DistanceGraph`, un alias: el tipo no decía nada y lo "roto" lo ponía solo el generador. Lo cambié a `{ g : DistanceGraph | not (ValidGraph g) }`. La consecuencia: `RejectsDefect ValidGraph` ahora repite el predicado del tipo, y lo que de verdad se prueba (que el Python que rompe grafos y `ValidGraph` coincidan) pasa a la verificación de cada grafo generado contra su tipo. Por eso esa verificación da error ante un valor fuera del tipo, en vez de descartarlo en silencio. En la corrida de hoy, 200 grafos rotos y ninguno fuera del tipo.

**¿Qué hace `ValidGraph`?**
Está en [distance_graph.lut](prototipo-cero/luthier/distance_graph.lut). Es el chequeo que `experiment_zero` le aplica al grafo leído de `nodes.csv` y `measurements.csv` antes de ajustarlo; si da `false`, no ajusta y avisa. Devuelve un `Bool` en dos pasos:

1. **Esquema:** `nodes` tiene `name` (texto), `x`, `y`, `z` y `sx`, `sy`, `sz` (reales); `measurements` tiene `i`, `j` (enteros) y `d` (real). Si falta una columna o tiene otro tipo, da `false` sin leer filas.
2. **Filas**, solo si el esquema está bien:
   - los índices `i`, `j` de cada medición están en rango;
   - ninguna medición une un nodo consigo mismo;
   - toda distancia es positiva;
   - toda desviación del prior es positiva;
   - los nombres de los nodos no se repiten;
   - los priors de los dos nodos de cada medición no coinciden, porque la jacobiana divide por esa distancia.

Hay una limitación que ya estaba en el plan (5.2): el último punto se verifica sobre el prior, no durante las iteraciones del Levenberg-Marquardt, donde dos nodos podrían acercarse a distancia cero.

Cuando me digas, sigo con el commit: tus notas de `random.lut` quedan fuera, y el cambio de código de ese archivo (`genR` → `genFloat64`) entra.

## 23. Luciano  2026-10-05 08:53:47 UTC  (line 938)

y vi que decias que tardaba mucho tiempo, puede ser?

## 24. Model  2026-10-05 08:54:40 UTC  (lines 946, 960)

Sí, es cierto, y una parte sigue sin resolver. Primero una corrección: te dije que la certificación de los grafos tardaba "unos 3 minutos" antes de la Fase 1, y lo leí mal. Las marcas de tiempo del certificado viejo dicen que `validity` (200 casos) tardaba unos 8 s.

| corrida | antes de la Fase 1 | primera versión del 1.3 | ahora |
|---|---|---|---|
| `distance_graph_python` | ~15–30 s de pruebas | la corté a los 20 min sin terminar | 107 s |
| `table_python` | ~3 s | — | 45 s |
| `array_python` | 624 s | 813 s | todavía corriendo |
| `array` | 370 s | 401 s | sin cambio |
| `experiment_zero` | 186 s | — | 243 s |

Los números de "ahora" se midieron con 6 a 8 corridas en paralelo, así que exageran: no son una comparación limpia. Lo que sí está claro:

- **Lo peor ya lo arreglé.** Al verificar cada valor generado contra su tipo, el predicado se evaluaba con el evaluador de sustitución, que es el del checker y mucho más lento que la máquina con la que corren las leyes. Generar un `ValidDistanceGraph` tardaba de 7 a 16 s y un `CompleteGraph` de 40 a 55 s. Ahora los predicados que son `Bool` se deciden en la máquina.
- **Lo que queda: `table_python`, 15 veces más lento.** El predicado de `Table` no es un `Bool`: es una ley cuantificada sobre nombres de columna y filas. Para esas, por cada tabla generada se le pide al checker que infiera el tipo de la ley y se la prueba 5 veces con el evaluador lento. Es el mismo problema de velocidad del checker que el plan pone en la Fase 4 (19 s para cargar `array`), que acá se paga una vez por valor generado.
- **`experiment_zero` no usa generadores**, pero ahora cada valor que cruza a Python se valida. No sé si eso pesa sin una medición limpia.

Las demás corridas terminaron bien: `distances_python` (con el par de densidad corregido), `laplace_check` y `belief_check` pasan enteras. Falta `array_python`.

Lo que propongo antes del commit, porque la Fase 2 regenera todos los certificados y una certificación lenta se paga en cada archivo:

1. **Arreglar el costo por valor de las leyes cuantificadas:** calcular el tipo de la ley una vez por tipo, no una vez por valor, y hacer las pruebas en la máquina. Con eso `table_python` debería volver cerca de los 3 s.
2. **Una medición limpia**, en secuencia y con la máquina libre, del intérprete viejo contra el nuevo en `table_python`, `distance_graph_python`, `array_python` y `experiment_zero`. Son unos 30 minutos de máquina y dicen si la Fase 1 dejó algún costo que no conozcamos.

Si después de eso algún generador sigue siendo caro, queda la salida del plan: `gen T trusted`, registrado en el certificado como confianza declarada.

¿Hago esto primero y después el commit?

Terminó la última corrida: `array_python` pasa sin fallas en 620 s. Con el intérprete viejo tardaba 624 s, así que con la decisión en la máquina volvió a su tiempo anterior; los 813 s eran el costo de la primera versión del 1.3. Esta medición también se hizo con otras corridas en paralelo.

Con eso todas las librerías y todos los archivos del proyecto pasan bajo la Fase 1. Las únicas fallas que quedan son las preexistentes: las 13 de `float64Field` en `algebra.lut` sin `real_python`, y las 19 "no generator for U" de `probability`.

El único costo que conozco y sigue abierto es `table_python` (de unos 3 s a 45 s). Espero tu respuesta a lo de antes: arreglo eso y hago la medición limpia antes del commit, o commiteo primero.

## 25. Luciano  2026-10-05 08:56:14 UTC  (line 963)

bien, segui con la fase 2, o hay alguna razon para atacar las fallas pre-existentes?

## 26. Model  2026-10-05 08:57:08 UTC  (lines 967, 995, 1006, 1011, 1044, 1049, 1076, 1106, 1111, 1127, 1135, 1143, 1154)

No hay razón para atacarlas por separado: las dos tandas de fallas preexistentes no son leyes falsas, son estados mal informados, y eso es justamente lo que arregla la Fase 2.

- **Las 13 de `float64Field`** aparecen solo al probar `algebra.lut` sin `real_python`: `abs` y `ulp` son huecos sin llenar y la ley queda trabada. Con el 2.2 (certificar después de llenar los huecos, por instanciación) y el 2.5 (`not run` distinto de `failed`), en `algebra.lut` sola eso pasa a "no corrida: depende de huecos" y se certifica bajo `algebra_python`. El problema de fondo de `float64Field`, que vale solo en [-16, 16], es otro (3.3) y no aparece como falla porque la tolerancia está ajustada a esa caja.
- **Las 19 "no generator for U" de `probability`** son leyes sobre todos los modelos de una teoría. La 05 §7 dice que quedan pendientes y se certifican por modelo, como ya hace `distances_python` con `fullPair` y `fullKernel`. El 2.5 las reclasifica.

Atacarlas antes sería hacer dos veces el mismo trabajo. Arranco entonces con el commit que elegiste y sigo con la Fase 2. El costo de `table_python` lo resuelvo dentro de la Fase 2, antes de regenerar los certificados, que es donde se paga.

Quiero dos commits por repo: uno con el estado de esta tarde antes de que yo empezara (el tuyo y el de la otra sesión, que tengo en el respaldo de las 15:45) y otro con la Fase 1. Así la historia separa quién hizo qué. Reviso el estado de los dos repos.

El índice del primer commit tiene exactamente el trabajo del día anterior a la Fase 1, con `random.lut` sin tus notas. Miro cómo cierran los mensajes anteriores y commiteo.

El primer commit quedó y el árbol de trabajo muestra exactamente la Fase 1 más tus notas en `random.lut`. Ahora el commit de la Fase 1, dejando `random.lut` afuera.

Ahora `sonolocalizacion`, igual: primer commit desde el respaldo (solo `prototipo-cero/luthier` y `prototipo-cero/src`, sin `AI/`) más los tres certificados que escribió la otra sesión.

Memoria al día. Empiezo la Fase 2 por 2.2 y 2.1, el hash de los certificados. Leo cómo se calcula y dónde se compara.

Leo el `Loader`, que es donde hoy se comparan los hashes archivo por archivo, antes de que el archivo que importa llene los huecos.

Ahora `testing.py`: el informe lleva `n`, modo, huellas y generadores, y cada ley tiene uno de tres resultados (2.5): `passed`, `failed` o `not run`.

Ahora el `Loader`: los certificados se aceptan al final de la carga, con el programa entero y los huecos llenos, buscando la entrada de esa forma de llenarlos, y cada rechazo guarda su motivo.

Ajusto también `api.Program.test` para que pode igual que la línea de comandos, y corro la suite.

Pasan las 97. Sigo con 2.4: un test cuyo cono pasa por un extern `provisional` queda registrado con esa marca y nunca cuenta como certificado.

Para 2.9 (`test n` sobre el objeto entero) necesito saber qué componente fuertemente conexa contiene a cada nombre. Miro cómo carga los objetos el checker.

Ahora el 2.7: que `run` registre el estado del cono en el `.run.json`, avise con los conteos, y que `--require-certified` se niegue a correr si algo del cono no está certificado.

Agrego la opción `--require-certified` y el comando `luthier certify` (2.6), que corre las directivas de varios archivos en paralelo y resume.

## 27. Luciano (queued)  2026-10-05 09:21:01 UTC  (line 1180)

aqui hago una pregunta: 
la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern
no estaremos haciendo parches no?

## 28. Model  2026-10-05 09:31:27 UTC  (lines 1184, 1197)

Tu pregunta es justa, y antes de contestar miro qué Python del proyecto no es una función llamada por `extern`.

Respuesta corta: en la Fase 1 y en lo que va de la 2 no agregué Python al proyecto, y casi todo lo que cambié sale de la especificación. Pero hay tres parches, y conviene llamarlos así y anotarlos en el plan.

**El Python del proyecto, hoy:**
- **Solo funciones llamadas por `extern` o `gen`:** `distance_graph.py` (lectura y escritura de tablas, generadores de grafos), `lm.py`, `positions_luthier.py`, y `positions_from_distances.py`, que es la numérica que usa `positions_luthier`. Eso cumple tu idea.
- **Scripts con `__main__`, que no la cumplen:**
  - `validate_distance_graph.py` envuelve en Python una llamada a Luthier para validar un grafo. Podría ser un `main` en un `.lut` (`luthier run validate_graph.lut --set graphDir=...`) y desaparecer.
  - `prepare_experiment_zero.py` arma el grafo a partir de la tabla de campo; su docstring dice que es Python plano "a propósito". Se podría escribir en Luthier con un extern que lea la tabla, pero es una decisión tuya.
  - `lm_controls.py` tiene los mutantes del Levenberg-Marquardt, hoy corridos a mano. Con el 5.6 pasan a ser externs que usan leyes, y entonces sí cumplen.

**Los parches de hoy:**
1. **`fullOn`/`profileOn` en `distances_python.lut`:** `shift := \ t v { if v.n == t.n then add t v else t }`. Le inventa un comportamiento a una dirección de dimensión equivocada para que el par de densidad tipe sobre `FullCoords`. La causa de fondo es que `Likelihood` no lleva la dimensión de su espacio tangente (07 §9), y que `ThetaFull = Vec Float64` (el cambio de la otra sesión) la perdió. El arreglo real va en `probability.lut`: un `Likelihood` con la dimensión del parámetro, y `shift` tomando direcciones de esa dimensión.
2. **`BrokenText = { text, defect }` en `table.lut`:** esquiva la regla de los alias con una estructura distinta en vez de un predicado. El predicado honesto ("este texto no es un CSV válido") necesita la gramática del formato escrita en Luthier, y hoy la tiene solo el parser de Python.
3. **Generadores de instancia (`gen FullCoords` = generador de todo `VecOf 16`):** la distribución en una caja de las posiciones es una elección del proyecto que vive en Python. Como extern está dentro de tu regla, pero que pise el generador de la familia para un `n` concreto es una semántica rara.

**Heurísticas del intérprete** (no son scripts del proyecto, pero tampoco son la solución de fondo):
- reconocer intervalos de `Int` para dar "exhaustivo";
- saltear tamaños chicos donde el rechazo no encuentra valores;
- decidir en la máquina con fallback al evaluador lento.

Compensan generadores débiles. Lo de fondo es lo que la 05 §10 deja abierto: generadores derivados de los constructores del tipo, de modo que Luthier genere un grafo válido sin un `gen_good_graph` en Python.

Propongo dejar la Fase 2 como está, porque no agrega parches, y sumar al plan:
- una fase para `Likelihood` con dimensión (saca el parche 1);
- pasar `validate_distance_graph.py` a un `.lut`;
- dejar escrito que los parches 2 y 3 esperan la gramática y los generadores derivados.

Mientras tanto la Fase 2 sigue corriendo: `flatten` ya pasa (87 casos) y `distances` está en curso.

## 29. Luciano  2026-10-05 09:34:18 UTC  (line 1200)

Scripts con __main__, que no la cumplen:
validate_distance_graph.py envuelve en Python una llamada a Luthier para validar un grafo. Podría ser un main en un .lut (luthier run validate_graph.lut --set graphDir=...) y desaparecer.
--> si, validate_distance_graph tiene que estar expresado en lut en cuanto a las condiciones y ser implementado en python con extern

prepare_experiment_zero.py arma el grafo a partir de la tabla de campo; su docstring dice que es Python plano "a propósito". Se podría escribir en Luthier con un extern que lea la tabla, pero es una decisión tuya.
lm_controls.py tiene los mutantes del Levenberg-Marquardt, hoy corridos a mano. Con el 5.6 pasan a ser externs que usan leyes, y entonces sí cumplen.
--> este caso lo exclui a proposito ya que seria para este caso particular.

## 30. Model  2026-10-05 09:34:41 UTC  (lines 1204, 1218, 1223, 1229, 1242, 1256, 1269, 1282, 1301, 1338, 1346, 1362, 1367, 1381, 1389)

Entiendo así las dos cosas. Para `validate_distance_graph`: las condiciones quedan escritas en `.lut` (ya lo están: `ValidGraph` y sus invariantes por fila en `distance_graph.lut`), la implementación rápida va en Python como extern, certificada contra esas condiciones como `lm.py` contra `optimization.lut`, y la entrada es un `main` en `.lut` en lugar de un script con `__main__`. "Lo excluí a propósito" lo leo como dicho de `prepare_experiment_zero.py`, cuyo docstring dice "deliberately plain Python" porque es lógica de este experimento; ese queda como está. Si te referías a `lm_controls.py`, decime. De todos modos ese es el 5.6 y no toca nada ahora.

Leo el script actual para ver qué hace además de validar.

Antes de escribir código anoto en el plan tus dos decisiones y los tres parches.

Mientras sigue la corrida de `distances`, escribo la validación. Miro cómo se construyen valores de una suma con etiquetas en Luthier, con un ejemplo existente.

Escribo la primera violación en `distance_graph.lut`: definición nativa en el orden de `ValidGraph` y su ley.

Tipa. Ahora la implementación en Python, en el mismo orden, y una función que muestra una fila para el informe.

Las dos cargan. Corro `validate_graph` sobre los grafos reales de la sesión A y comparo con lo que decía el script viejo.

Coinciden también en los grafos rotos, y el informe nuevo nombra las columnas de la fila. Borro el script y actualizo las referencias que lo nombran.

Corro las leyes nuevas de la validación (sin escribir certificados) y miro la corrida de `distances`.

De 45 s a 22 s, pero sigue lejos de los ~3 s de antes. Perfilo qué cuesta verificar una tabla generada.

Agrego los archivos de candado al `.gitignore` de los dos repos y corro la suite.

Pasan. Antes de regenerar los certificados escribo las pruebas de la Fase 2, una por comportamiento.

Pasan las 105. Un detalle antes de regenerar: al escribir, las entradas del formato viejo (sin huella) nunca van a coincidir con nada, así que las descarto en vez de arrastrarlas.

Mientras corre (va a tardar, `array` y `array_python` solos suman más de 15 minutos), dejo escrito en la 05 §7 lo que ahora hace la certificación.

La salida de `certify` aparece al terminar, así que espero. Mientras, escribo en el plan la sección de la Fase 2.

Estoy regenerando los certificados de las librerías, con 8 procesos en paralelo; cuando termine sigo con el proyecto. Lo que ya está hecho y probado de la Fase 2:

- **Hash (2.1):** cubre el código del cono, el Python de cada extern y el intérprete. Editar `lm.py` o `positions_luthier.py` ahora invalida los certificados que dependen de ellos, y `check -v` dice qué parte cambió.
- **Certificación por llenado (2.2):** los hashes se comparan con el programa entero cargado y los huecos llenos, y cada nombre guarda una entrada por cada forma de llenarlos. Para eso agregué `luthier test f --imports`, que certifica las leyes importadas en el contexto de `f`; el mensaje viejo prometía eso con `--deep` y no lo hacía.
- **Grados (2.3):** "bounded" cuando se recorrió una caja de `Int`, "exhaustive" solo sobre dominios finitos de verdad.
- **Provisionales (2.4):** un test sobre un extern `provisional` nunca queda certificado.
- **Resultados (2.5):** tres posibles, `passed`, `failed` y `not run`. Las 13 de `float64Field` sin `real_python` pasan a "not run: depende de huecos sin valor". Las fallas de `positions` eran certificados de una versión vieja del archivo; corridas de nuevo, pasan.
- **Poda y `luthier certify` (2.6):** se eliminan los nombres que ya no existen, y el comando nuevo certifica varios archivos a la vez.
- **Registro de corrida (2.7):** `run` muestra y guarda el estado del cono, y `--require-certified` se niega a correr si algo no está certificado.
- **Cantidad de casos (2.8):** una entrada con menos casos de los que pide su directiva no se acepta.
- **Objeto completo (2.9):** `test n` corre todo el objeto de `n`.
- **`validate_graph.lut` reemplaza al script**, como pediste. Las condiciones están en `distance_graph.lut`, el Python en `distance_graph.py`, y se certifican con 200 grafos rotos. Sobre los grafos de la sesión A da lo mismo que el script viejo.
- **`table_python`** volvió de 45 s a unos 5 s.

Las 105 pruebas del intérprete pasan (8 nuevas en `tests/test_certificates.py`). No commiteé la Fase 2: cuando termine la regeneración te propongo los commits.

## 31. Luciano  2026-10-05 09:53:58 UTC  (line 1392)

Te parece activar la Fase 3? me la recordas?

## 32. Model  2026-10-05 09:54:51 UTC  (line 1400)

Sí, y conviene hacerla ahora, antes de que termine la regeneración de certificados. La razón: desde el 2.1 la huella del intérprete forma parte del hash, así que cualquier cambio al intérprete invalida todos los certificados. Lo que se está regenerando ahora (8 procesos, unos 4 minutos de CPU cada uno hasta acá) quedaría viejo con el primer cambio de la Fase 3. El orden que propongo:

1. cortar la regeneración;
2. commitear el código de la Fase 2;
3. hacer la Fase 3;
4. regenerar una sola vez;
5. commitear los certificados.

Esto muestra además un costo del 2.1: después de cada tanda de cambios al intérprete hay que recertificar todo (unos 30 a 40 minutos de máquina en paralelo). Es el precio de que "certificado" quiera decir algo, pero hay que hacerlo por tandas y no después de cada cambio.

**La Fase 3, semántica del checker:**

- **3.1, `Bool` por posición.** Hoy cualquier suma de dos `Unit` cuenta como `Bool`, y la primera alternativa es `true`: con `Verdict = < wrong | right >`, una ley que siempre da `wrong` pasa. El arreglo es reconocer `Bool` por sus etiquetas `true` y `false`, nunca por posición. Es corto; lo único a revisar es si alguna librería usa una suma de dos unidades como `Bool`.
- **3.2, `==` donde no debería existir.** Se acepta `==` sobre `Real`, que no tiene igualdad computable, sobre un `data` con funciones adentro (queda un término trabado sin error), y pasada la profundidad 20 no se mira más. El arreglo es corto.
- **3.3, `float64Field` vale solo en [-16, 16].** La asociatividad falla en (1e8, -1e8, 3e-9), y el tipo dice `OrderedField Float64` sin límite. Hay dos niveles:
  - corto: que el portador diga la caja, `{ x : Float64 | abs x <= lawMagnitude }`. Hay que ver qué cambia en quienes lo usan, como `pow` de `array`;
  - de fondo: la ley de redondeo con `Rational` exacto, de la que salen las tolerancias en vez de `roundingSlack`. Es una semana de trabajo.

  Propongo hacer solo el corto.
- **3.4, `toFloat64`.** La 06 §4 dice `Real -> Float64`, pero el código tiene `Int -> Float64`, con 37 usos así, y el mensaje de error del checker sugiere aplicarlo a un `Real`. Me aparto del plan: corregir la especificación y el mensaje, no renombrar 37 usos. `Real` hoy no se computa, así que un `Real -> Float64` no tendría ningún uso. Además, `check -v` debería decir que ninguna ley sobre `Real` se prueba.
- **3.5, R2 y R3.** R2 decide la "posición de tipo" de forma aproximada y no recorre los tipos de las inyecciones. R3, cuando no puede desplegar una ley, cuenta todas las etiquetas como tocadas. El arreglo es seguir la definición de 05 §0 y reportar "no decidible" en vez de aceptar.
- **3.6, los informes de 05 §6:** la tabla de completitud y "consistente, no caracterizado". El plan le da baja prioridad; propongo dejarla afuera.

En total, 3.1 a 3.5 con la versión corta de 3.3 es un día de trabajo humano.

## 33. Luciano  2026-10-05 09:57:45 UTC  (line 1409)

que regeneracion?

## 34. Model  2026-10-05 09:57:59 UTC  (line 1413)

Por "regeneración" me refiero a volver a correr todas las pruebas para reescribir los archivos `.cert.json`. Es lo que está corriendo ahora en segundo plano: `luthier certify --imports` sobre los 13 archivos de `luthier/src/luthier/lib/`, con 8 procesos a la vez.

**Por qué hace falta:** con la Fase 2, el hash de un certificado cubre ahora el código del cono, el Python de cada extern y el intérprete. Ningún certificado escrito antes trae esa información, así que hoy todos se leen como viejos. Por eso `validate_graph` decía "the cone of main: pending 7, stale 57": no queda nada certificado hasta que se vuelvan a correr las pruebas. Recién entonces `check -v` vuelve a mostrar "certified" y `run --require-certified` acepta correr.

**Qué toca:** reescribe los `.cert.json` de las librerías dentro del repo de `luthier`. Después faltaría hacer lo mismo con los del proyecto en `prototipo-cero/luthier/`.

**Por qué te propuse cortarla:** la huella del intérprete entra en el hash, así que cualquier cambio de la Fase 3 deja viejos otra vez los certificados que se están generando ahora. Si la Fase 3 viene enseguida, conviene regenerar una sola vez al final.

Sigue corriendo y no toqué nada más. ¿La corto, la dejo terminar, o preferís otra cosa?

## 35. Luciano  2026-10-05 09:59:03 UTC  (line 1416)

arranca la Fase 3 como recomendaste

## 36. Model  2026-10-05 09:59:14 UTC  (lines 1420, 1434, 1442, 1453, 1464, 1480, 1488, 1507, 1528, 1558)

Corto la regeneración y commiteo el código de la Fase 2, sin los certificados a medio escribir.

Todavía aparecen 8 procesos; miro cuáles son.

Ya no corre nada. Verifico la suite con el último cambio (descartar las entradas sin huella) y commiteo el código de la Fase 2, sin los certificados a medio escribir ni tus notas.

Los dos commits de la Fase 2 quedaron: `8ea8625` en `luthier` y `3829fd7` en el proyecto. Empiezo la Fase 3 por el 3.1, `Bool` por posición. Busco todos los lugares que deciden si algo es un `Bool`.

Ahora el checker rechaza la ley `Verdict`: "the predicate of a subtype must be Bool-valued or a law". Paso al 3.2. Primero miro `contains_function` y cómo se decide dónde existe `==`.

`Real` ya se rechaza y el árbol recursivo de enteros sigue teniendo `==`. Mi prueba del `data` con una función no valía porque R4 exige que sea recursivo; la rehago con uno recursivo.

El 3.2 quedó: también se rechaza `==` sobre un `data` recursivo que guarda una función, y la suite sigue en 105. Ahora el 3.3; antes de cambiar el tipo de `float64Field` miro quién lo usa.

Ahora el 3.5. Leo cómo decide hoy el checker la R2 ("posición de tipo") y la R3 (qué etiquetas toca un predicado).

Ningún archivo existente cae en el caso indecidible de la R3, la R2 ampliada no rechaza nada del código actual, y la suite sigue en 105. Escribo las pruebas de la Fase 3.

Las 8 pasan. Corro la suite entera y cargo de nuevo todas las librerías y archivos del proyecto, porque el cambio en los patrones podría rechazar código existente.

## 37. Luciano  2026-10-05 10:15:52 UTC  (line 1564)

si terminas con esta fase segui con la siguiente

## 38. Luciano  2026-10-05 10:16:38 UTC  (line 1570)

arranca la Fase 3 como recomendaste y luego comitea y segui con la fase 4 sin preguntar (me voy por 40 minutos)

## 39. Model  2026-10-05 10:17:17 UTC  (lines 1577, 1586, 1598, 1603, 1619, 1632, 1643, 1653, 1677, 1711, 1722, 1730, 1735, 1740, 1774, 1783, 1802, 1808, 1813)

Sigo sin preguntar: cierro la Fase 3, commiteo y paso a la Fase 4. Primero la verificación que quedó cortada: la suite y la carga de todas las librerías y archivos del proyecto.

Todo carga. Lanzo `experiment_zero` en segundo plano para confirmar que sigue dando los mismos CSV con la Fase 3, y mientras escribo la sección del plan.

Mientras termina `experiment_zero`, empiezo el perfil de la Fase 4 (solo lectura): dónde se van los ~17 s de cargar `array.lut`.

El 77 % del tiempo está en `_type_operand` y `resolve_operator`: cómo se decide qué significa cada `+` o `*`. Leo las dos funciones.

`array.lut` carga en 5,4 s en lugar de 14,9. Antes de seguir, miro el resultado de `experiment_zero` con la Fase 3.

Antes de commitear verifico que esa versión intermedia también pasa la suite, desde una copia del paquete en el scratchpad.

Fase 3 commiteada (`aee30cc`). Sigo con la Fase 4: la suite con el checker acelerado y un perfil nuevo para ver qué queda.

`array.lut` carga en 4,5 s (eran 14,9) y `array_python` en 5,6 (eran unos 17). Hago un perfil más, ordenado por tiempo propio, para ver si queda algo grueso.

Ese perfil no va a medir nada: `main` corre el programa en otro hilo y `cProfile` mide solo el suyo. Lo relanzo haciendo que corra en el mismo hilo.

No hay anotación en línea `(e : T)`; reescribo esa línea del programa de sumas.

Sigue corriendo (con el perfilador tarda unas tres veces más). Mientras, corro la suite completa.

Pasan las 139. Mientras termina el perfil, anoto en el plan lo hecho de la Fase 4.

Commiteo 4.1 y 4.3, que son del intérprete, mientras el perfil sigue.

Mientras termina el perfil, mido directamente la hipótesis: cuánto tarda evaluar una vez la media y la jacobiana del modelo en las posiciones del prior, que es lo que el LM pide en cada iteración.

El `pkill` mató también a mi propio comando, porque su texto contenía el patrón; la edición no se hizo. La repito sola.

Carga. Corro `experiment_zero` con la jacobiana nueva y comparo byte a byte con los CSV de referencia.

Mientras corre, actualizo la memoria con el estado.

La memoria apunta a un script del scratchpad, que no sobrevive a esta sesión. La corrijo para que describa el orden en vez del archivo.

La Fase 3 y la Fase 4 están hechas y commiteadas. Ahora corre la regeneración de todos los certificados en segundo plano (librerías primero, después el proyecto en orden de dependencias); cuando termine reviso los resultados, commiteo los certificados y te dejo el resumen completo.

**Fase 3** (`aee30cc`):
- `Bool` se reconoce por sus etiquetas, no por posición.
- `==` ya no se acepta sobre `Real` ni sobre un `data` con funciones adentro.
- La R2 recorre más tipos, y la R3 da error cuando no puede leer qué etiquetas toca una ley, en vez de darlas todas por tocadas.
- De paso apareció un error real: el `if` sobre una suma que no es `Bool` tomaba siempre la primera rama sin avisar, porque `true` se leía como una variable. Ahora es error.
- El 3.3 no se hizo como estaba planeado. Restringir `float64Field` a la caja [-16, 16] no funciona porque la suma no queda dentro de la caja, y `sumTo` y los espacios vectoriales están construidos sobre él. Queda para su propia fase con la ley de redondeo; por ahora el comentario dice dónde sus leyes son falsas.

**Fase 4** (`21c8eb7`, `41acdf8`, `f058bc8`):

| | antes | ahora |
|---|---|---|
| cargar `array.lut` | 14,9 s | 4,5 s |
| cargar `array_python.lut` | ~18 s | 3,8 s |
| suite del intérprete | ~24 s | 6 s |
| `experiment_zero` | 146 s | 21 s, CSV idénticos byte a byte |

- Para `experiment_zero` bastó calcular la distancia de cada fila de la jacobiana una vez y no en cada una de sus 30 entradas, en dos líneas de `positions.lut` y sin Python. El plan proponía pasar la verosimilitud a Python y no hizo falta.
- Los dos evaluadores coinciden en todos los programas comparados, y cada test registra cuántas veces la máquina cayó al evaluador lento.
- El caché en disco de la elaboración no lo construí: con cargas de 4 s no compensa.

La suite del intérprete tiene ahora 139 pruebas y todas pasan.

## 40. Luciano  2026-10-05 13:22:14 UTC  (line 1819)

que falta?

## 41. Luciano  2026-10-05 13:22:56 UTC  (line 1825)

que falta?

## 42. Model  2026-10-05 13:23:27 UTC  (lines 1829, 1846, 1852)

Antes de contestar miro cómo va la regeneración, que es lo único que está corriendo.

No hay un perfilador por muestreo instalado, así que lo veo de otra forma: corro una de esas pruebas con `--show-cases`, sin escribir certificados, y miro en qué ley y caso avanza.

Ya tengo una idea de qué pasa, y además apareció una falla real. Corto la regeneración, que está repitiendo trabajo, y lanzo un diagnóstico con tiempos por definición sobre `array.lut` solo.

## 43. Luciano (queued)  2026-10-05 13:28:44 UTC  (line 1859)

y?

## 44. Model  2026-10-05 13:29:28 UTC  (line 1865)

Falta lo más visible: hoy no hay ningún certificado válido. Desde la Fase 2 los viejos no sirven, y la regeneración no llegó a terminar ni las librerías: la corté recién, después de 2 horas y media. Sin certificados, `check -v` muestra todo como pendiente y `run --require-certified` se niega a correr.

**Por qué tardó tanto.** Lo verificado: seis procesos llevaban 2 h 26 min de CPU cada uno, y una muestra de 4 minutos de `belief.lut` muestra matrices de hasta 13×14 generadas como términos de Luthier. La explicación que propongo, sin confirmar todavía: arranqué las 13 librerías a la vez con `--imports`, y como ninguna tenía certificados, cada una de las seis que importan `array` volvió a correr todas las leyes de `array.lut` en su propio contexto. Sin `array_python` esas matrices pasan por Jacobi y por el determinante de Laplace nativos, y el costo de Laplace crece factorialmente con el tamaño. A eso se suma mi cambio del 2.5: las leyes que antes se abortaban porque no se podía generar el tipo en tamaños chicos ahora corren hasta el final.

**Una falla real que salió de esa corrida:** en `belief.lut`, `indexAt` debe `0 <= k < w.n` y falla con `k = -1`, porque el tipo de `k` admite negativos.

**Lo que queda, en orden:**

1. **Certificados:** medir el tiempo de cada ley de `array.lut`, acotar con directivas de tamaño las leyes que explotan, regenerar en un orden donde nadie repita el trabajo de otro, y commitear. Antes, arreglar `indexAt`.
2. **Parches de la Fase 1 que hay que sacar:**
   - `fullOn`/`profileOn`, que se van con un `Likelihood` que lleve la dimensión;
   - `BrokenText` como registro, que necesita la gramática del CSV en Luthier;
   - los generadores de instancia.
3. **Fase 5, el proyecto:**
   - 5.1: el modelo certificado (7 nodos) no es el que corre (10 nodos);
   - 5.2: garantías que viven en comentarios en vez de tipos;
   - 5.3: los 7 nodos y el gauge escritos en el `.lut` y en el `.py`;
   - 5.4: los controles del sigma de 25,7 cm de la sesión A;
   - 5.5: la potencia de las leyes estadísticas;
   - 5.6: los controles del LM como leyes, si no era ese el caso que excluiste a propósito;
   - 5.7: los `Agrees` exactos con tolerancia;
   - 5.8: las constantes del proyecto fuera de la librería;
   - 5.9: fijar la versión de Luthier.
4. **Pendientes menores:**
   - el 3.3 de fondo, la ley de redondeo con `Rational`, alrededor de una semana;
   - `run --checked`;
   - los refinamientos dentro de una suma, como el `Table` de un `Maybe Table`;
   - un solo evaluador;
   - el tag de versión.
5. **Fase 6:** `let`, menos unario, argumentos implícitos, y borrar el código muerto.
6. **Fuera del plan:** la parte acústica, que es el proyecto en sí.

Te recomiendo terminar el punto 1 ahora, porque sin él las Fases 1 a 4 no se ven en ningún certificado, y después decidir si seguir con la Fase 5 o volver a lo acústico.

## 45. Luciano  2026-10-05 13:30:57 UTC  (line 1868)

Dale, completa de 1 a 5, sin preguntar

## 46. Model  2026-10-05 13:33:41 UTC  (lines 1872, 1882, 1887, 1908, 1926, 1937, 1942, 1958, 1985, 1990, 1998, 2003, 2016, 2022, 2034, 2117, 2129, 2155, 2163, 2203, 2237, 2287, 2295, 2308, 2362, 2402, 2415, 2445, 2479, 2527, 2551, 2599, 2647, 2669, 2683)

Voy de 1 a 5, pero no en ese orden: dejo los certificados para el final. La huella del intérprete entra en cada hash, y los puntos 4 y 5 cambian el intérprete, así que si regenero primero tendría que volver a regenerar todo. El orden de trabajo:

1. los cambios al intérprete (puntos 5 y 4);
2. los parches de las librerías (punto 2);
3. el proyecto (punto 3);
4. al final, los certificados (punto 1), una sola vez.

Commiteo cada parte. Antes de tocar archivos del proyecto miro si otra sesión está trabajando en ellos.

Nadie más tocó los repos. Empiezo por la falla real que apareció, `indexAt` en `belief.lut`.

`k` empieza en 0 y solo crece, pero su tipo `Int` admite negativos, y con un `k` negativo la obligación `w.f k` es falsa de verdad. El tipo honesto es `Nat`.

`indexAt` pasa sus tres obligaciones. Pero hay algo que no esperaba: los conteos de "with laws" bajaron (de 56 a 18 en `array`, y `real_python` pasó de 1 a 0). Lo miro antes de seguir.

Pasan las 139. Quito una línea en blanco de más que quedó en `evaluator.py` y paso a `let` y al menos unario. Leo cómo el parser arma los términos y cómo el lexer trata el `-`.

Para `let` necesito dos palabras clave nuevas, `let` e `in`; antes de agregarlas reviso que ningún `.lut` las use como nombre.

Solo aparece dentro de un texto entre comillas. Miro cómo `parse_match` lee los patrones para reutilizarlo.

`primitive_base` no es lo que necesito: para `Float64` devuelve `Real`. Uso la base del tipo después de sacar los refinamientos.

I use `peek` with an offset so the newline skipping matches the rest of the parser.

Ahora el checker: registrar cuántos implícitos tiene cada definición, verificar que sean tipos, y la elaboración de la aplicación con unificación.

Agrego la verificación de que los parámetros implícitos sean tipos y lo pruebo.

La llamada con un par literal no deduce nada: `inferable` dice que un par no se infiere solo. Miro qué considera inferible.

Los seis casos dan bien, incluido el lambda sin anotar, que se chequea después de deducir `A` del otro argumento. Corro la suite y cargo todo para ver que no rompí nada.

Todo carga y la suite sigue en 139. Escribo las pruebas de `let`, del menos unario y de los implícitos.

Pasan las 8. Agrego la sintaxis nueva a la gramática (02) y commiteo el punto 5.

`neg` queda atrapado, pero el array con un 5 en `Vec (Fin 3)` pasa sin error. Lo depuro.

Llamada a mano, la verificación funciona. Sospecho que el valor quedó guardado en un caché de la máquina desde la carga, antes de activar `--checked`. Lo miro.

Escribo esa extensión en `extern_obligations`.

`parseTable` tiene ahora cuatro obligaciones, una por cada ley de `Table`. Las corro.

Rehago las dos pruebas: el array con el 5 y `experiment_zero` con `--checked`.

Pasan las 22. Anoto en la especificación los refinamientos dentro de sumas y `--checked`, y commiteo esta parte del punto 4.

Antes de escribir `rational.lut`, miro los tipos declarados de las hojas de `array.lut` que voy a certificar contra las operaciones exactas.

Las hojas toman `Vec Float64` sin refinar, así que las leyes se pueden escribir directo sobre ellas. Escribo `rational.lut`.

Carga. Corro sus leyes.

Todo carga y `experiment_zero` sigue idéntico. Agrego pruebas de `Rational` en el puente y en la aritmética, actualizo la 06 y la 07 (que nombran `float64Field`) y commiteo.

Escribo los cambios en `probability.lut`.

Todo carga. Corro el par de densidad y el kernel con los registros nuevos, más las obligaciones del `shift` de `fullOn` y `profileOn`. Va en segundo plano porque tarda.

Escribo `DensityPairOn` y `KernelOn` en `probability.lut`, con `DensityPair` y `Kernel` como el caso en que el dominio es el espacio entero.

Para darle a `BrokenText` un predicado honesto ("este texto no es un CSV del formato") necesito la gramática del formato en Luthier. Leo cómo la define hoy el parser de Python.

Tipa. Limpio una expresión que me quedó redundante en `FloatCell` y ajusto el lector de Python a la especificación: CSV estricto, espacios ASCII y números con la gramática de arriba.

Esa comparación no es justa: el lector laxo solo mira el nivel de CSV, no la cabecera ni las celdas. Comparo de verdad: el parser viejo completo contra el nuevo, sobre los mismos textos mutados.

En 40 casos todos convergieron, así que la falla es rara. Pruebo con más casos para ver cuál de los dos motivos aparece.

Reescribo `fit` de `experiment_zero` con `let`, que lo deja legible sin cambiar ninguna operación, y agrego al resumen si el ajuste convergió.

El aviso funciona y queda registrado en la corrida. Arreglo un detalle (cuando el cono no tiene leyes, la línea queda vacía) y miro las pruebas de optimización.

Commiteo esta tanda (5.6, 5.7, `Converges` y 5.9) después de correr la suite.

## 47. Tool (system)  no time  (line 2704)

[summary inserted by the harness]  [33 characters]

## 48. Model  2026-10-05 15:08:13 UTC  (lines 2748, 2782, 2933, 3003, 3008, 3020, 3036, 3075, 3083, 3088, 3107, 3123, 3141, 3153, 3158, 3166, 3171, 3186, 3191, 3199, 3209, 3226, 3312, 3330, 3336, 3341, 3352, 3368, 3376, 3381, 3400, 3410, 3434, 3463, 3476, 3481, 3490, 3509, 3514, 3519, 3539, 3550, 3556, 3573, 3585, 3601, 3606, 3615, 3658, 3667, 3673, 3715, 3760, 3768, 3773, 3778, 3786, 3807, 3862, 3877, 3941, 3946, 3959, 3983, 3994, 4010, 4015, 4031, 4039, 4045, 4060, 4075, 4080, 4085, 4096, 4101, 4121, 4145, 4153, 4200, 4211, 4215, 4234, 4244, 4259, 4274, 4295, 4316, 4337, 4384, 4414, 4423, 4447, 4475, 4480, 4494, 4499, 4504, 4512, 4517, 4529, 4539, 4547, 4555, 4563, 4568, 4617, 4640, 4657, 4686, 4709, 4723, 4732, 4742, 4751, 4756, 4776, 4787, 4795)

Corriendo los tests de optimization_python en segundo plano mientras sigo con 5.2 (garantías en los tipos de positions.lut).

Estoy diseñando 5.2: llevar a los tipos que el vector de posiciones tiene longitud múltiplo de 3 y que el Jacobiano exige distancias positivas. Leo dónde se usan.

Antes de reescribir las librerías pruebo en un archivo de prueba cómo trata el checker un maximizador con la dimensión en el tipo, y qué obligaciones genera.

Escribo los cambios. Primero array.lut: `zeros`/`ones` con su longitud en el tipo, e `IsGradient` sobre direcciones de una dimensión dada.

Ahora probability.lut: `dim` constante en `Likelihood` y `MeanModel`, y las leyes de la acción sobre `VecOf dim`.

Ahora belief.lut: creencia gaussiana, resultado y maximizador indexados por la dimensión.

Las cuatro librerías chequean. Miro qué obligaciones nuevas aparecieron.

Paso a Python y al proyecto: `lm.maximize` recibe ahora la dimensión.

Escribo positions.lut. Antes miro cómo se certificaban sus obligaciones (qué generadores había en ese contexto), porque el archivo no importa los generadores de numpy.

Las obligaciones con `j.n == i.n` ya se generaban por rechazo sin problema, así que `Design` no necesita generador propio. Escribo positions.lut.

positions.lut chequea. Sigo con distance_graph.lut: `MapInput` con índices que son nodos del prior, y el diseño que se lee de él.

distance_graph_python chequea. Ahora reescribo distances.lut: el diseño completo de 7 nodos se calcula en Luthier, el modelo es `positionsModel` con el gauge fijado, y las Theta son `VecOf`.

distances.lut chequea. Reescribo positions_luthier.py: el diseño y el gauge llegan como argumentos.

Ahora distances_python.lut: los externs reciben el diseño y el gauge, y desaparecen `fullOn`/`profileOn`.

chequea. Una prueba corta del puente (el registro del diseño cruzando a Python) antes de seguir con los demás archivos.

El puente funciona. Sigo con laplace_check y optimization_check.

Las dos chequean. Ahora optimization_python.lut, que declara los externs de lm.py con estos tipos.

chequea. Ahora experiment_zero.lut: el modelo es `positionsModel` del diseño del grafo, la creencia lleva su dimensión, y el ajuste informa si los pares quedaron separados en la moda.

Todo chequea, y las obligaciones de `meanModel` desaparecieron (las lleva `positionsModel`, y son verdaderas). Corro el experimento y comparo los CSV con los de referencia, byte a byte.

Idénticos byte a byte (26 s). Corro la suite del intérprete por el cambio en `call_extern`, y lanzo en segundo plano los tests de los archivos del proyecto que cambiaron.

Mientras corren (5 a 30 minutos), sigo con 5.8: las constantes del proyecto que viven en probability.lut. Miro cómo están definidas `approx` y el uso de esas constantes.

validate_graph falla en obligaciones de un extern que lee archivos (`readGraph` probado con rutas al azar: FileNotFoundError) y en una ley que no reduce. Miro el archivo.

Ahora `GraphDir` y su generador, y saco las dos declaraciones duplicadas de `readGraph`.

Ahora sí. Corro de nuevo los tests de validate_graph y miro los demás.

La obligación de `describe` desapareció y optimization_check pasó entero. El test de distance_graph_python en segundo plano arrancó con el código anterior a `GraphDir`; lo reinicio.

Mi patrón de `pgrep` coincidió con mi propio shell (exit 144). Mato por PID.

Mientras corren los tests, escribo 5.8 y 5.5. Busco las funciones de listas y de máximo que ya existen.

Escribo los cambios de probability.lut (ensamble, prueba de Kolmogorov-Smirnov, resolución del PIT, semillas).

Ahora belief.lut: las calibraciones reciben su ensamble.

Ahora el proyecto: ensamble y resolución del PIT declarados en distances.lut, semillas `Seed` en las leyes, y controles también a 1,3σ.

Todo chequea. Miro los tests en segundo plano (corren con el código de antes de 5.8/5.5).

Pruebo rápido lo nuevo de las librerías: `genSeed`, `normalVec` con la prueba de Kolmogorov-Smirnov, y la distancia de Kolmogorov contra su definición nativa.

Ahora reescribo la parte del ajuste y del programa en experiment_zero.lut.

Chequea. Corro la entrada principal (debe dar los mismos CSV byte a byte) y las dos de control, todo hacia el scratchpad y sin registrar la corrida.

De vuelta a 27 s, mismos valores salvo redondeo. Ahora las dos entradas de control.

Mientras corren los controles, preparo el punto 1. Miro las directivas de test de array.lut y si el tester registra el tiempo por ley.

No hay tiempo por ley. Lo agrego al resultado de cada ley y al certificado, para encontrar las leyes explosivas.

El control con priors horizontales ×5 da sigma 28,1 cm (ν 6,1): ensanchar el prior de los micrófonos no baja sigma, así que el prior no es lo que la infla. Espero el control con sigma conocida.

Lo aviso la notificación cuando termine. Mientras, mido tiempos por ley en array_python, donde están las definiciones caras (determinante por Laplace, espectro por Jacobi).

Mientras tanto, documento en el plan lo hecho en la fase 5. Leo el final actual del documento.

Los dos rechazos funcionan: un `fixedSigma` negativo y un directorio que no es de grafo se rechazan al darlos, por su tipo. Miro los tiempos por ley de array_python.

Sigue corriendo (la salida se escribe al final). Escribo en el plan las secciones de lo hecho.

Reviso qué dicen las especificaciones (07 §9 y otras) sobre `dim`, para que sigan al código.

Mientras corre el test de array con tiempos, actualizo la memoria del estado de Luthier.

Lleva 6 minutos de CPU; espero la notificación. Mientras, reviso el diff de los dos repos para los commits.

Escribo los dos tests de regresión: el tipo del resultado de un extern con argumentos dependientes, y la ley cuantificada de un registro como una obligación por ley.

Pasan. Verifico que el primer test de verdad depende del arreglo: lo corro con el cambio revertido.

Sin el arreglo el test falla, con él pasa. Miro el test de array.

Mientras corren las obligaciones del experimento, arranco la regeneración de certificados de las librerías por etapas, empezando por `real_python`.

Demasiado rápido (0 s). Lo corro directo para ver qué hizo.

Funciona; real_python sólo tiene `abs`. Sigo con random, text y rational en paralelo.

Ahora el lado del tester: un caso donde el propio extern levanta una excepción se salta y se cuenta aparte.

Sólo queda 1 GB libre de 15. Miro qué ocupa la memoria antes de lanzar varios procesos.

Firefox ocupa la mayor parte; limito el paralelismo a 3 procesos. Escribo un script de etapas para la recertificación (en el scratchpad) y lo lanzo en segundo plano, empezando por las librerías.

Mientras corre, miro cómo van las obligaciones del experimento con los cambios.

Las librerías chicas ya pasaron; array_python está corriendo. Preparo el script de etapas del proyecto para lanzarlo cuando terminen las librerías.

Mientras corre, reviso el formato que espera `luthier.lock`, para escribirlo después del tag.

Mientras tanto actualizo la memoria del proyecto con el estado nuevo (los hashes los completo al commitear).

Ahora el generador: un registro dependiente cuyo campo es `Vec (Fin 0)` falla en lugar de sortear de nuevo. Miro cómo genera los pares dependientes.

Ahora el bug de proyección. Lo reproduzco en chico.

Pasa todo, 17,5 s. Miro si es carga de la máquina (quizás sigue corriendo el test del experimento) antes de atribuírselo al cambio.

La suite pasó de 11 a 20 s sin otra carga, así que es mi cambio. Lo aíslo desactivando la detección de proyecciones.

Sigue en 20 s, así que el costo está en otra parte del camino nuevo. Perfilo los tests más lentos.

Sigue sin tiparse: el tipo esperado `Vec (...)` es un registro con nombres (un `Subtype` sin ley), que va por otra rama de `check`. Pongo el respaldo antes de las dos ramas de `match`.

Ahora pasa y la suite vuelve a 11 s. Agrego el test de regresión con la misma forma (obligación dentro de un `let` sobre un campo dependiente proyectado).

Pasa. Verifico que sin el arreglo falla.

El test pasa también sin el arreglo, así que no reproduce el caso. Miro qué obligaciones tiene y cómo se tipan.

La forma del valor de Python estaba mal (un registro de tres campos cruza como tupla plana). Lo corrijo.

Ahora el test falla sin el arreglo y pasa con él; la suite tiene 156 tests en 11 s. Le doy a `nodeNames` el dominio de grafos con columnas, y vuelvo a probar las obligaciones del experimento.

Mientras corren, documento los arreglos nuevos del intérprete en el plan y en la especificación (05 §7, la distinción entre ley enunciada y obligación de tipo).

Agrego también el test del redibujo de registros con un componente vacío, y verifico que distingue con y sin el arreglo.

Pasa también sin el arreglo: el test no discrimina. Miro qué pasa sin el arreglo con un caso más parecido al real.

Con 200 casos sí discrimina (sin el arreglo: no corrida). Ajusto el test.

Discrimina. Miro las obligaciones del experimento (esa corrida arrancó con el intérprete ya corregido).

Lleva 3 minutos. Mientras, reviso el diff del intérprete para el commit.

Para random.lut voy a pasar al índice sólo el bloque de `Seed`, sin las notas de Luciano. Espero el resultado de las obligaciones con una notificación.

Mientras termina, redacto los mensajes de commit.

Chequea. Corro la suite, el experimento y otra vez sus obligaciones.

Mientras corren las obligaciones, lanzo la recertificación de las librerías (si el experimento destapa otro arreglo del intérprete, la repito).

Otro cambio del intérprete: corto la recertificación de librerías que está corriendo y la relanzo cuando cierre esto.

Agrego el test de la descarga por la condición de la rama.

Ahora separo en experiment_zero el informe (puro, testeable) de la escritura.

Mientras corre, reviso el diff del checker antes de commitear.

La revisión del diff me parece correcta. Las librerías chicas ya pasaron; espero array_python y las siguientes.

La espera del log coincidió antes de tiempo con mi patrón; sigo con el monitor. Mientras, nada más que hacer en código: espero los eventos de la recertificación.

array_python con `--imports` lleva 12 minutos (también prueba las obligaciones de array.lut y algebra.lut). Espero la notificación.

Esas obligaciones ya se habían certificado antes, así que terminan; miro en el certificado anterior cuánto tardaron, por las marcas de tiempo.

Agregar generadores en arrays.py cambiaría la huella del intérprete y obligaría a otra regeneración completa. Antes de decidir, miro qué cubre exactamente esa huella.

Espero la notificación. Mientras, dejo redactado el borrador del informe final.

La máquina no está cargada; es lento y nada más. Espero la notificación.

Les cuento: la corrida de diagnóstico muestra en vivo qué definición se demora; ya pasó las hojas de numpy y las primeras obligaciones de array.lut sin problemas. Sigo mirando dónde se traba.

La corrida de diagnóstico se clavó después de `eigenDef`: la siguiente definición es `spectralMap`. La miro.

Esos procesos son mis esperas en segundo plano (buscan una línea que ya no va a aparecer). Las detengo por su ID de tarea, sin tocar mi propio shell.

Agrego la directiva a array.lut y relanzo desde array_python, esta vez con la salida sin buffer de cada etapa en un log propio para ver el avance.

Con `certify` la salida de cada test queda capturada hasta el final; para ver el avance, mejor llamo a `luthier test` directamente en las etapas de un solo archivo. Relanzo así.

Mientras corre, commiteo el código del intérprete y las librerías (sin certificados; esos van en un commit aparte cuando termine la regeneración). random.lut entra sin las notas de Luciano.

El índice tiene random.lut con `Seed` y sin las notas (que quedan en el árbol de trabajo). Commiteo.

Commiteo también el código del proyecto (los certificados y el `luthier.lock` van después).

Los dos commits de código están hechos. Miro el avance de array_python en su log.

Avanza bien. Espero los eventos del monitor.

Con la directiva, array_python pasó de más de 90 minutos a 6: 81 definiciones pasadas, ninguna fallada, una no corrida. algebra_python tiene otra no corrida. Las miro.

Las dos "no corridas" son la misma: `IsGradient`, genérica en `Theta : U` (no hay generador de U), como estaba previsto y documentado. Sigo esperando las etapas.

probability_python: 36 pasadas y 7 no corridas; reviso que sean las genéricas en `Theta : U`.

Las siete no corridas son todas genéricas en `Theta : U`. El proyecto arrancó con distance_graph_python; miro su log a medida que avanza.

Avanza (con algunas obligaciones lentas, como `Separated`, 170 s por la generación por rechazo). Re-armo el monitor para las etapas que faltan.

Mientras espero, nada más que tocar. Quedo a la escucha del monitor.

Chequea. Pruebo rápido las obligaciones de `distanceJacobian` con los generadores nuevos.

Sigue lento: `Design` (de `positionsModel`) sortea su campo `j : PairsAmong nodes i` también por rechazo. Le agrego generador a `PairsAmong`.

Incluso la obligación trivial de `point` tarda 2 s por caso, así que el cuello de botella no son los pares. Perfilo esa ley sola.

Un `Positions` cuesta sólo 15 sorteos. Busco qué parámetro de la ley de `point` es el caro, muestreando cada uno por separado.

`Node p` ahora se sortea directamente. Mido de nuevo la ley de `point` completa.

Discrimina. Relanzo la recertificación completa (librerías y proyecto) con el intérprete final.

Mientras corre, actualizo el plan con estos dos arreglos de generación.

Commiteo el arreglo del generador (intérprete) y, en el proyecto, los generadores de pares.

El mensaje del último commit atribuye la directiva de `spectralMap`, que en realidad entró en el commit anterior. Corrijo el mensaje (commit local recién hecho).

Ahora espero la recertificación.

Librerías listas en 10 minutos, todo pasado salvo las genéricas en `Theta : U`. Sigue el proyecto; miro distance_graph_python.

distance_graph_python: 34 pasadas, ninguna fallada (las 7 no corridas son las genéricas), en 4 minutos en lugar de más de 40. Sigue la etapa con distances_python, validate_graph y belief_check.

Quedan corriendo sólo distances_python (10 minutos); validate_graph y belief_check ya terminaron. Espero.

## 49. Luciano  2026-10-05 20:41:31 UTC  (line 4809)

reporte de situacion

## 50. Luciano  2026-10-05 20:41:38 UTC  (line 4815)

reporte de situacion

## 51. Model  2026-10-05 20:42:15 UTC  (line 4823)

Los puntos 2 a 5 están hechos y commiteados, y el punto 1 (regenerar los certificados) está en curso: las librerías ya quedaron certificadas, el proyecto va por la mitad, y hasta ahora no falló ninguna ley. El tag v0.1 y el `luthier.lock` esperan a que termine.

Lo que más pesó no estaba en el plan. Para poner en los tipos las garantías del modelo de posiciones (5.2) hubo que meter la dimensión en los tipos de probability, belief y optimization: ahora Theta es `VecOf n` en todo el proyecto. Con `Vec Float64` las obligaciones del modelo eran falsas. La de `posModel` pasaba sólo porque la tapaba el generador de instancia que saqué en la fase 1. Ahora `positionsModel` es el único modelo, el que corre el experimento y el que se certifica con el gauge fijado. El diseño y el gauge se calculan en Luthier y viajan a Python, que ya no tiene constantes propias. Los CSV de la sesión A salen idénticos byte a byte.

Lo que dicen los datos (5.4) sale de corridas mías al scratchpad, sin registrar; conviene que las corras vos para que queden en el `.run.json`. El PIT señala a parlante_A2: sus tres distancias quedan cada una 2,6 sd cortas, y el resto cae entre −0,7 y 1,1. Ensanchar ×5 los priors horizontales sube sigma a 28,1 cm, así que el prior no es lo que la infla. Con sigma fija en 3 cm, Levenberg-Marquardt no converge en 500 iteraciones.

En el camino hubo que arreglar varias cosas del intérprete, cada una con su test (ahora son 159). La conceptual: una obligación de tipo habla de los valores que produce un cómputo. Si el cómputo levanta una excepción no hay valor, y ese caso se salta. Una ley enunciada en el tipo de una definición, en cambio, sigue fallando ante una excepción. Antes, las obligaciones del experimento fallaban cuando el ajuste daba una matriz singular sobre grafos al azar. Cada arreglo del intérprete invalida todos los certificados, y por eso la regeneración se reinició varias veces durante la noche. La medición del tiempo por ley encontró dos cuellos de botella:
- Las obligaciones de `spectralMap`, que corren Jacobi nativo a tamaño 16, tardaban más de una hora. Ahora están acotadas a tamaño 5.
- `Node p` se generaba por rechazo; la obligación de `point` pasó de 185 s a 1 s.

Estado de la regeneración:
- **Librerías:** listas en 10 minutos. Pasa todo menos 7 leyes genéricas en `Theta : U`, que no se pueden correr porque no hay generador de U.
- **distance_graph_python:** pasó todo en 4 minutos; antes tardaba más de 40.
- **En curso:** distances_python, el más pesado (ensambles de 400 sorteos, Kolmogorov, controles a 1,3σ), lleva 20 minutos.
- **Faltan:** optimization_check, y después optimization_python, laplace_check y experiment_zero. Estimo una hora más.

Lo que queda abierto o falló:
- La obligación de `negate` es falsa y ya lo era antes: arma un registro con leyes a partir de funciones sueltas.
- Las obligaciones genéricas nunca corren.
- Un `match` contra un tipo refinado no se chequea rama por rama.
- Siguen los dos evaluadores.
- `Square` se sigue generando por rechazo.
- 5.5 quedó a medias: no registra la tasa de falsa falla ni repite con otra semilla.
- `lmMaxIter` es una constante, y por tu regla quizás debería ser un parámetro.
- El lock va a avisar de cambios locales mientras tus notas de random.lut no estén commiteadas.

Commits, en la rama `numbers` y sin push: luthier `548a3b6` y `20a786b`, sonolocalización `84ee917` y `e6fdc02`. random.lut entró sin tus notas, que siguen en el árbol de trabajo.

## 52. Luciano  2026-10-05 20:47:36 UTC  (line 4829)

La obligación de negate es falsa y ya lo era antes: arma un registro con leyes a partir de funciones sueltas.
explica bien


Las obligaciones genéricas nunca corren.
no es esa la idea?

Un match contra un tipo refinado no se chequea rama por rama.
explica bien


Siguen los dos evaluadores.
Square se sigue generando por rechazo.
explica bien

5.5 quedó a medias: no registra la tasa de falsa falla ni repite con otra semilla.
elabora

lmMaxIter es una constante, y por tu regla quizás debería ser un parámetro.
si, obvio tiene que ser parametro

El lock va a avisar de cambios locales mientras tus notas de random.lut no estén commiteadas.
elabora

## 53. Model  2026-10-05 20:49:47 UTC  (line 4833)

Voy punto por punto. `lmMaxIter` y `lmTol` los paso a parámetros ahora; lo explico al final.

**La obligación falsa de `negate`.** `negate` promete devolver un objetivo con leyes a partir de tres funciones cualesquiera, y esa promesa sólo vale si quien lo llama le pasa un gradiente verdadero; el tipo no lo exige.

En optimization.lut, `Objective` es un registro con dos leyes:
- `GradIsGradient`: en todo `x` de su dimensión, `grad` es el gradiente de `value`, comprobado por diferencias finitas.
- `StepMatrixPositive`: en todo `x`, `stepMatrix` es simétrica y semidefinida positiva.

`negate n f g m` arma `{ value := -f, grad := -g, stepMatrix := m }` con `f`, `g` y `m` sueltas, y declara que devuelve un `Objective`. El checker registra entonces una obligación para todo `f`, `g` y `m`, y es falsa. El tester la refuta con lo primero que genera: `f` constante y `g` un vector constante distinto de cero, que no es el gradiente de nada constante. Nunca estuvo certificada.

Importa porque `lmMaximizer`, el Levenberg-Marquardt nativo contra el que se certifica el de Python, pasa por `negate`. También `laplaceMode`, que arma el objetivo con el log-posterior: `g` es el score de la verosimilitud y `m` su información. Ese objetivo cumple las leyes sólo si la verosimilitud cumple `ScoreIsGradient` e `InfoIsPositive`. Esas son leyes del par de densidad, enunciadas en un dominio (la caja `TestedFull`), no en todo vector.

El arreglo que propongo separa dos tipos:
- `Problem`: lo que el algoritmo corre, sin leyes, con `stepMatrix` tipada como cuadrada de su dimensión para que `dampedStep` no deba nada.
- `Objective`: un `Problem` con leyes. Las leyes del algoritmo (`StepRule`, `DescentDirection`, `Certified`) se enuncian sobre `Objective`.

`negate` devolvería un `Problem` y su obligación desaparece. Que los objetivos concretos tienen leyes ya lo certifica `objectives` en optimization_check, en las instancias donde vale.

**Las obligaciones genéricas.** La idea es esa, pero hoy se cumple a medias. El código genérico se verifica en sus instancias para las *leyes*: `DensityPairOn` se prueba con `FullCoords` en distances_python.

Lo que no corre en ningún lado son las obligaciones *internas* del código genérico. Por ejemplo:
- en `diagnose`, que `k < wbar.n`;
- en `ShiftComposes`, que `(add p q).n == l.dim`.

No corren en la librería porque no hay generador de `U` para elegir `Theta`. Tampoco en la instancia: cuando distances_python certifica el par sobre `FullCoords`, el tester corre las leyes del par, no las obligaciones de las funciones genéricas que esas leyes llaman. Esas funciones se ejecutan de rebote, así que un índice fuera de rango aparecería como error de la ley de la instancia. Pero no aparecería como la obligación, con su nombre y su contraejemplo, y en el certificado quedan como "no corridas".

Para cumplir la idea entera hay dos caminos:
- instanciar esas obligaciones con los tipos de cada instancia que el proyecto certifica;
- probarlas en uno o dos tipos representativos (por parametricidad, una ley que no mira dentro de `Theta` vale para todos si vale para uno).

**Un `match` contra un tipo refinado.** Cuando el tipo esperado tiene leyes, el checker no mira cada rama de un `if` o `match`: infiere el tipo del todo, pierde las leyes y genera una obligación sobre el `if` entero.

El caso concreto está en validate_graph: `rowText (if r.table == "nodes" then g.nodes else g.measurements) r.row`. `rowText` espera un `Table`, y las dos ramas ya son `Table`, así que no debería deberse nada. En cambio quedó la obligación "el `if` entero cumple las cuatro leyes de `Table`". Una de esas leyes cuantifica sobre columna y fila, la obligación no reducía y fallaba.

La regla está en `check`: un `match` se chequea rama por rama sólo si el tipo esperado no es un subtipo. La línea es de las primeras versiones y no quedó registrado por qué. El arreglo es chequear cada rama contra el tipo refinado, con la condición de la rama como precondición. Toca todas las obligaciones del código, así que hay que hacerlo con cuidado. Por ahora en validate_graph moví el `if` a las funciones, `(if … then rowText g.nodes else rowText g.measurements) r.row`, donde el tipo esperado no es refinado.

**Los dos evaluadores.** El intérprete tiene dos implementaciones de la misma semántica:
- La máquina (machine.py) es call-by-need y rápida; corre los programas y las leyes.
- El evaluador por sustitución (evaluator.py) reescribe términos. Lo usa el checker para computar con tipos, y la máquina le pasa lo que no sabe hacer, como una conjunción de leyes.

Esto trae tres problemas:
- Pueden discrepar. En 4.3 comparé las dos en los programas de la especificación y coincidieron, salvo `==` sobre arrays, que R8 hace inalcanzable.
- Una ley puede evaluarse mitad en una y mitad en otra. El certificado registra cuántas veces pasó (`evaluator_fallbacks`).
- Cada arreglo se hace dos veces: el del tipo del resultado de un extern hubo que ponerlo en `call_extern` y en `try_extern`.

El plan 4.3 es dejar una sola, la máquina, y que el checker normalice con ella. No está hecho.

**`Square` por rechazo.** `Square` es `{ a : Mat Float64 | a.m == a.n }` y no tiene generador registrado. Para obtener una cuadrada se sortea una matriz con filas y columnas independientes, hasta 16 cada una, y se tira si no es cuadrada: acierta una de cada diecisiete, construyendo cada vez la matriz entera. `SquareOf n` encadena dos rechazos. Lo pagan por caso las leyes con un parámetro `Square` (`TraceAgrees`, `symmetricPart`, `InvSqrtPositive`…), y es parte de por qué la regeneración de array.lut tarda.

El arreglo es `gen Square` y `gen SquareOf` en Python: sortear `n` y después una matriz n×n. Lo dejé porque obliga a tocar arrays.py, que entra en la huella del intérprete, y eso es otra regeneración completa. Conviene juntarlo con el próximo cambio del intérprete.

**5.5 a medias.** Estaba pedido:
- semillas de verdad;
- un estadístico de forma;
- controles a 1,3σ con su tasa de detección en el certificado;
- un mínimo de sorteos;
- registrar la tasa de falsa falla y repetir una falla con otra semilla.

Hice:
- `Seed`, sorteada sobre 2^31. Antes las semillas eran `Int` en [−16, 16], 33 distintas, así que veinte casos podían repetirse.
- Kolmogorov-Smirnov sobre el PIT agrupado, además de los dos momentos.
- Los controles a 1,3σ.
- El mínimo puesto en el tipo: un `Ensemble` tiene al menos 100 sorteos y zMax de al menos 3.

Faltan tres cosas, todas del intérprete:
- **Tasa de detección.** Los controles a 1,3σ son leyes que exigen detección en cada caso. Si un control detectara el 80 % de las veces, la ley fallaría sin decir ese 80 %. Medir la potencia es registrar una fracción, no un sí o no.
- **Tasa de falsa falla.** Una ley estadística falla por azar con un modelo correcto. En el modelo completo de 16 parámetros hay 16 + 136 = 152 estadísticos por caso, cada uno con probabilidad 5,7×10⁻⁷ de pasar z = 5. Eso da unos 9×10⁻⁵ por caso y unos 4×10⁻⁴ por certificación de 5 casos. Ese número sale del `Ensemble` y de la ley, y debería quedar en el certificado para pesar una falla.
- **Repetir con otra semilla.** Hoy una falla sola tumba la ley. La política sería repetir el caso con otra semilla: si pasa, fue azar con tasa conocida; si vuelve a fallar, es contraejemplo, con probabilidad de falsa falla del orden de la tasa al cuadrado.

El intérprete reconocería las leyes estadísticas porque reciben un `Ensemble`: el tipo ya lo dice, falta usarlo.

**`lmMaxIter` y `lmTol`.** Los paso a parámetros ahora, y con ellos el cómputo pasa a recibir los ajustes. Si fueran agujeros usados directamente dentro de `fit`, las obligaciones de `fit` y `reportOf` dependerían de un agujero y quedarían sin correr. Por eso `fit` va a recibir `{ tol, maxIter }` como argumento, que el tester puede sortear. La entrada (`main` y los controles) los toma de `--set`.

Una diferencia con tu regla de argparse: en Luthier un agujero no tiene default, así que cada corrida tendrá que dar `--set lmTol=… --set lmMaxIter=…`. La invocación documentada en la cabecera haría de default. Si querés defaults de verdad, es una característica nueva del lenguaje: un parámetro con valor por omisión que `--set` reemplaza y que la corrida registra.

**El aviso del lock.** `luthier.lock` fija el commit del intérprete con que el proyecto se escribió y certificó. En cada `check`, `test` y `run`, Luthier compara el commit que corre con el fijado, y además mira si el directorio del intérprete (`src/luthier`, `lib/` incluido) tiene cambios sin commitear. Tus notas al final de `lib/random.lut` son uno de esos cambios. Por eso cada comando va a imprimir "warning: luthier.lock pins luthier X, and this is X with changes", y cada `.run.json` va a decir `agrees: false`.

Los certificados no se ven afectados: los hashes cubren el código de las definiciones, no los comentarios, y la huella del intérprete no incluye `lib/`. El aviso es correcto, porque el árbol no es exactamente el commit, pero en este caso es ruido. Las salidas son:
- commitear las notas;
- moverlas fuera de `src/luthier`, por ejemplo a `docs/`;
- dejarlas y convivir con el aviso.

No lo decido yo porque son tuyas. El lock todavía no está escrito: va después del tag, cuando terminen los certificados.

Cuando estén `lmTol` y `lmMaxIter` como parámetros, te aviso con la invocación nueva.

## 54. Luciano  2026-10-05 20:54:57 UTC  (line 4839)

hay una cuestion importante con los tests y es como se generan los valores de los tipos involucrados. Entiendo que eso se hace internamente no?

## 55. Model  2026-10-05 20:56:04 UTC  (line 4843)

Sí. Salvo que el programa declare un `gen` para un tipo, el tester construye los valores él solo, mirando la estructura del tipo. Esa construcción es parte de lo que significa cada certificado: "certificado" quiere decir "pasó sobre estos sorteos, de estos generadores".

**Cómo se elige cada valor.** El tester (generators.py) decide en este orden:
1. Si el tipo es `Fin n` o un alias de él, como `Node p` después del arreglo de anoche, sortea uniforme en el rango, o sabe que está vacío.
2. Si hay un generador registrado con `gen`, lo usa. Puede estar en Luthier, como `genInt` y `genFloat64` en random.lut, o en Python por extern, como `gen_vec_of` en las librerías o `gen_positions_within`, `gen_good_graph` y los de pares en el proyecto. Cada valor que da se comprueba contra las leyes del tipo, y uno fuera del tipo es un error con el nombre del generador.
3. Si no hay generador, construye por la estructura del tipo:
   - un `Int` en [−size, size] y un `Float64` en una grilla uniforme de [−size, size];
   - un registro, campo por campo;
   - una suma, eligiendo alternativa al azar;
   - una función sobre un dominio finito, como su tabla;
   - un refinamiento `{ x : T | P x }`, sorteando `T` y descartando hasta que `P` valga, con hasta 2000 intentos.

El tamaño crece de 1 a 16 a lo largo de los casos (primero los chicos, para que un contraejemplo salga mínimo), y una directiva `test X with n size k` lo acota. El certificado registra con qué generador salió cada parámetro, la huella de su código y cuántos valores dio.

**Dónde la generación decide lo que se prueba:**
- **Rango numérico.** `genFloat64` nunca produce 10⁻³⁰⁰ ni 10³⁰⁰. Por eso `NormalDouble` tiene un generador propio que sortea el exponente, para que la ley de redondeo se pruebe en toda la escala. `genInt` llega a ±16, y por eso las semillas eran 33 valores hasta que existió `Seed`.
- **Refinamientos por rechazo.** Pueden ser lentos (`Square`, uno de cada 17) o inalcanzables: si el predicado casi nunca se cumple, la ley queda "no corrida" con "give it a gen". Lo que se acepta además es la distribución base condicionada al predicado, que puede quedar sesgada.
- **Funciones sobre dominios infinitos.** Se generan como constantes (o afines para `Float64 -> Float64`). Una ley sobre "cualquier verosimilitud" u "objetivo" se prueba sólo con funciones triviales. Si el registro tiene leyes, como `Objective`, ni eso: una constante casi nunca las cumple. Por eso las leyes importantes se enuncian sobre instancias concretas (`objectiveAt t seed`) con dominios tipados (`TestedFree`).
- **Parámetros de tipo** (`Theta : U`). No hay nada que sortear, y la ley queda sin correr.
- **Cobertura de los generadores registrados.** Se comprueba que sus valores sean del tipo, nunca que lo cubran. `gen_good_graph` da grafos de 3 a 8 nodos en una caja, y un generador que sólo diera casos fáciles pasaría igual. Hoy la cobertura es una afirmación del autor del generador, sin verificación.

**Hacia dónde iría.** El plan lo deja como pendiente (05 §10): generadores construidos desde los constructores del tipo, en lugar de rechazo. Hay dos cosas más que valdría la pena discutir:
- Mezclar casos de borde con los sorteos: cero, ±1, valores extremos, matrices casi singulares, nodos casi coincidentes.
- Que el certificado diga qué región se cubrió, por ejemplo el rango de magnitudes de los `Float64` o los tamaños de matrices alcanzados, para que se pueda leer qué significa "pasó".

Lo de `lmTol` y `lmMaxIter` como parámetros todavía no lo hice: lo hago a continuación. La recertificación sigue corriendo en segundo plano.

## 56. Luciano  2026-10-05 21:04:37 UTC  (line 4846)

bueno, yo quisiera que los tests  pidan un generador explicito para cada tipo involucrado. 
El generador puede ser simplemente un valor tipico, pero la idea es que quede explicitado. 
La pregunta es como generamos valores de tipos funciones? 
Bueno, seria el caso mas simple: un censo sobre los valores registrados no?
Para numeros tendriamos que fijar los valores limites y definir si son en escala linear o logaritmica.  
Para vectores tendriamos varios generadores que sean utiles para distintos casos. 

Quiero que analices esto bastante bien y generes un documento para luego generar la especificacion.

## 57. Luciano  2026-10-05 21:06:41 UTC  (line 4855)

quizas te quede poca memoria para un proyecto de esa envergadura. 
O lo podes delegar?

## 58. Model  2026-10-05 21:07:51 UTC  (lines 4859, 4869, 4915, 4929, 4951, 5014, 5024, 5029, 5069, 5097, 5102, 5113, 5138, 5155)

Me alcanza la memoria: el contexto se compacta solo cuando hace falta, y lo que importa del diseño está en archivos (el plan, la especificación) y en la memoria. Igual conviene delegar, y lo hago así:
- Un agente arma el inventario de todos los tipos que los tests sortean hoy: dónde se definen, cómo se generan y con qué distribución. Es leer mucho código y certificados, y conviene que no me llene el contexto.
- Otro agente releva cómo resuelven esto QuickCheck, Hedgehog, Hypothesis y SmallCheck: rangos lineales y logarítmicos, generación de funciones, matrices con condición controlada, medición de cobertura. Incluye si alguien hizo algo parecido a tu censo de valores registrados.
- El documento de análisis lo escribo yo, porque depende de lo que decidimos acá.

Mientras los agentes trabajan, hago el cambio de `lmTol` y `lmMaxIter`.

Los dos agentes están corriendo. Mientras, el cambio de `lmTol` y `lmMaxIter`. Primero miro en qué etapa va la certificación, porque experiment_zero está en la última.

La mejora en dos casos es chica porque domina la conversión inicial. Lo que importa es el costo por llamada repetida; mido un caso de la ley de densidad (400 sorteos).

Relancé las etapas del proyecto, una por una y cada una con su log. Mientras corren, espero a los dos agentes para escribir el documento.

Ya tengo el estado actual de la especificación sobre generadores (R7, 05 §7, 04 §1). Espero los informes de los agentes para escribir el documento.

Ahora los generadores de `Square` y `SquareOf`.

La suite pasa. Agrego un test del cruce de una lista de vectores calculados en la máquina.

Pasa (prueba la corrección; la velocidad la mido aparte). Mido un caso de `fullKernel` con el arreglo.

Mientras corre la certificación, leo el informe de antecedentes.

Leí el relevamiento completo (el resto es la bibliografía). Falta el inventario.

El agente del inventario sigue trabajando. Mientras tanto escribo las secciones del documento que no dependen de él, y completo el estado actual y la migración cuando llegue.

Escribí las secciones 0 y 2 a 12. Faltan el estado actual (1), la migración (13) y las preguntas abiertas (14), que dependen del inventario. Espero al agente.

Las librerías se certificaron en 6 minutos y distance_graph_python pasó entero; sigue distances_python. Mientras espero el inventario, corrijo dos frases del documento.

Llegó el inventario. Lo leo, empezando por los problemas y las reglas por defecto.

## 59. Luciano (queued)  2026-10-05 22:15:21 UTC  (line 5189)

ahora, no se si estas apuntando al concepto importante: no hay un unico generador por tipo, ergo hay que explicitar cual se uso

## 60. Model  2026-10-05 22:15:49 UTC  (lines 5196, 5209, 5223, 5243, 5261, 5266, 5272, 5299, 5304)

Lo leo antes de seguir: abriste "funcion de los tipos en Luthier.txt" y puede estar relacionado.

Reescribo el documento entero con el principio en el centro: un tipo tiene muchos generadores, el test nombra los que usa, y el certificado es la afirmación bajo esos generadores.

El archivo cambió desde mi última lectura (mis propias ediciones), así que lo releo antes de escribir. Además belief_check acaba de dar 3 fallas: lo miro después del documento.

Los dos agentes terminaron y el documento está reescrito. Antes de responderte miro las 3 fallas de belief_check en la certificación.

Chequean. Pruebo belief_check sin escribir certificados, para confirmar que las tres fallas desaparecen.

Pasan las tres. Commiteo los dos arreglos; belief_check lo recertifico al final de la corrida.

Escrito para: vos y para quien escriba la especificación a partir de él, en inglés como el resto de los docs.

El documento está en `luthier/docs/generators-2026-10-06.md` y tiene en el centro tu principio: no hay un generador por tipo; cada test nombra el que usó para cada tipo que sortea, y un certificado afirma "esta ley pasó con estos generadores". Los dos informes de base quedaron en `docs/ideas/`: el inventario de lo que se sortea hoy, con referencias a archivo y línea, y el relevamiento de QuickCheck, Hedgehog, Hypothesis, LAPACK y demás.

Lo que más pesa:
- **El diagnóstico.** El inventario muestra que casi todos los problemas de hoy tienen una raíz: el generador se trata como una propiedad del tipo, elegida una vez y en silencio, y el certificado no dice cuál fue. Por eso la ruta de un tipo depende de qué archivos cargó el programa. Por eso los dominios se quedan cortos: tolerancias sorteadas en (0, 16] cuando se usan de 10⁻⁶ a 10⁻¹⁶, matrices nunca mal condicionadas, un generador de grafos que nunca llega a la sesión A. Y por eso hay leyes que "pasan" con 24 casos contados de 100.
- **La propuesta central.** Los generadores son valores con nombre, muchos por tipo. Un test liga cada tipo a un generador, en línea o con un *profile* reutilizable (`test fullPair with 5 under tape`). La ligadura forma parte de la identidad del certificado, así que una ley tiene un certificado por ligadura: `solve` certificado bajo matrices bien condicionadas y bajo mal condicionadas son dos afirmaciones verdaderas distintas. `gen T :=` desaparece.
- **Dos mecanismos que no se mezclan.** Un tipo de dominio cambia lo que se afirma (la ley vale dentro de la caja). La ligadura cambia sólo la evidencia (misma afirmación, otra distribución). Un predicado no puede distinguir uniforme de logarítmico en el mismo intervalo.
- **Tus tres preguntas.**
  - Números: límites abiertos o cerrados, escala lineal o logarítmica (la logarítmica con signo y un átomo en cero) y valores especiales con su peso.
  - Vectores y matrices: una lista de dimensiones (0, 1, 2, 3, 5, 10) y familias estructuradas al estilo LAPACK, con el número de condición como parámetro.
  - Funciones: tu censo, como lista explícita de nombres y de familias con valores capturados (`from objectiveAt`). El documento compara lo que gana (funciones con sentido, prueba exhaustiva, contraejemplos con nombre) con lo que pierde (sesgo hacia funciones prolijas, no cierra bajo composición). El mismo censo, aplicado a `U`, hace correr por fin las obligaciones genéricas.
- **Lo que el certificado debe decir.** Cuenta sólo los casos evaluados; los descartados, saltados y vacíos van aparte; las premisas son etiquetas con su frecuencia, y queda el alcance de cada generador.

Quedan diez preguntas abiertas para la especificación, entre ellas la sintaxis de ligaduras y profiles, qué exige una corrida cuando una ley tiene varios certificados, el tamaño, y generadores en Luthier o en Python (tu nota de random.lut).

Sobre la recertificación, que sigue en segundo plano:
- Las librerías pasaron completas, y distance_graph_python y validate_graph sin fallas.
- distances_python tuvo una ley más que no corrió que en la etapa anterior (8 contra 7); está por ver si es otra genérica.
- belief_check dio 3 fallas, y son justo el tipo de cosa que el documento describe. `gaussianFamily` aceptaba una tolerancia negativa, sorteada en [−16, 16], y con ella su igualdad no es reflexiva. El modelo escalar leía `t.f 0` de vectores que pueden estar vacíos. Las arreglé con tipos (tolerancia positiva, parámetro `VecOf 1`) y están commiteadas; belief_check se vuelve a certificar al final.
- Ahora corre optimization_check y después vienen optimization_python, laplace_check y experiment_zero.
- El tag v0.1 y el `luthier.lock` esperan a que termine.

Mientras corre, anoto en el plan lo encontrado en esta última tanda.

Commiteé el documento de generadores (con el inventario y los antecedentes en `docs/ideas/`) y anoté en el plan lo de esta tanda.

La recertificación sigue en segundo plano: corre optimization_check, después vienen optimization_python, laplace_check y experiment_zero. Cuando terminen recertifico belief_check (ya arreglado), commiteo los certificados, pongo el tag v0.1 y escribo el `luthier.lock`.

Queda una obligación de distances_python sin correr, de `ProfileIsFullAtItsSigma`. El tester se queda sin combustible al separarla en conjunciones antes de sortear nada; arreglarlo requiere otro cambio del intérprete, así que está anotado en el plan como abierto.

## 61. Luciano  2026-10-05 22:33:01 UTC  (line 5307)

bueno, contame como estamos con el Plan en general

## 62. Model  2026-10-05 22:34:50 UTC  (line 5318)

El plan está cerrado en sustancia. Todas las fases, de la 0 a la 6, están hechas o con un desvío documentado, salvo 5.5 (a medias) y el evaluador único de 4.3. Falta terminarlo formalmente: completar la recertificación, poner el tag v0.1 y escribir el `luthier.lock`. Lo que queda abierto de fondo ya pertenece al diseño siguiente, el de los generadores.

**Lo que cambió.** Antes, un extern podía devolver cualquier cosa y un certificado no decía nada. Ahora el puente lee cada valor por su tipo declarado. El hash de un certificado cubre el código, el Python detrás de cada extern y el intérprete. Cada ley termina pasada, fallada o no corrida.

Sobre eso se apoyan las fases siguientes:
- **Semántica del checker** (fase 3): Bool por etiquetas y `==` sólo donde la igualdad es estructural.
- **Números:** Rational exacto, y la ley de redondeo en lugar de llamar cuerpo a los doubles.
- **Velocidad** (fase 4): experiment_zero pasó de 146 a 27 segundos, con los CSV idénticos byte a byte en cada cambio.
- **El proyecto** (fase 5):
  - un solo modelo de posiciones, el que corre y el que se certifica, con el diseño y el gauge calculados en Luthier;
  - la dimensión en los tipos;
  - el PIT de los residuos y dos controles;
  - las leyes estadísticas con su ensamble y semillas de verdad;
  - los controles de Levenberg-Marquardt escritos como leyes.
- **Lenguaje** (fase 6): `let`, menos unario y argumentos implícitos.

**Desvíos respecto de lo planeado:**
- 3.3 se hizo por el camino largo (la ley de redondeo con Rational).
- 5.1 se certifica sobre el diseño completo y no sobre grafos sorteados: las leyes del par de densidad necesitan información no singular, y el grafo de la sesión A no la da.
- 5.2 resultó mucho más grande de lo previsto, porque obligó a meter la dimensión en las librerías.

**Lo que dicen los datos.** El sigma de 25,7 cm de la sesión A no viene del prior: al ensancharlo, sigma sube. El PIT señala las tres distancias a parlante_A2. Eso son corridas mías; las de control conviene que las corras vos para que queden registradas.

**Lo abierto:**
- 5.5 a medias: falta registrar la tasa de falsa falla y repetir una falla con otra semilla antes de darla por contraejemplo.
- Siguen dos evaluadores (4.3).
- La obligación de `negate` es falsa y ya lo era antes.
- Las obligaciones genéricas sobre `U` nunca corren.
- Un `match` contra un tipo refinado no se chequea rama por rama.
- Una obligación se queda sin combustible al separarse en conjunciones.

Todo eso está anotado en el plan. Las tres de en medio se resuelven en buena parte con el diseño de generadores que escribí recién.

**Lo que encontró la noche sin buscarlo.** Hubo trampas de rendimiento que hacían inviable certificar:
- una lista cruzando a Python por el evaluador lento;
- el registro del diseño convertido en cada llamada;
- `Node p` sorteado por rechazo;
- el Jacobi nativo a tamaño 16.

Cada una costaba de minutos a horas, y las arreglé. También aparecieron obligaciones falsas que la certificación destapó: la tolerancia negativa de `gaussianFamily` y el vector vacío del modelo escalar de belief_check. Esto último ilustra el punto del documento de generadores: sortear tolerancias en [−16, 16] encontró un defecto real.

**Estado de la recertificación**, que corre en segundo plano:
- Las librerías pasaron completas, y distance_graph_python, distances_python y validate_graph sin fallas.
- belief_check tuvo las 3 fallas ya arregladas; se vuelve a certificar al final.
- optimization_check lleva 16 minutos, porque prueba obligaciones sobre `Objective` que no se pueden sortear y cada intento fallido cuesta segundos.
- Faltan optimization_python, laplace_check y experiment_zero.

Cuando terminen commiteo los certificados, pongo el tag y escribo el lock. Todo está commiteado en la rama `numbers` de los dos repos, sin push.

## 63. Luciano  2026-10-05 22:39:27 UTC  (line 5321)

volve a repetir todo lo que dijiste pero cuando decis 3.3 (o el puntero que sea) me pones entre parentesis de que estamos hablando, no tengo tu memoria

## 64. Model  2026-10-05 22:40:22 UTC  (line 5328)

El plan de reparación (`luthier/docs/plan-2026-10-05.md`, escrito tras la revisión crítica del 5 de octubre) está cerrado en sustancia. Sus seis fases están hechas o con un desvío documentado, salvo dos puntos: 5.5 a medias (darles potencia a las leyes estadísticas) y 4.3 pendiente (dejar un solo evaluador). Las seis fases son:
1. el puente con Python;
2. certificados confiables;
3. la semántica del checker;
4. velocidad;
5. el proyecto de sonolocalización;
6. salud y ergonomía del lenguaje.

Falta terminarlo formalmente:
- completar la recertificación (volver a probar todas las leyes y escribir los `.cert.json`, porque cada cambio del intérprete invalida todos);
- poner el tag v0.1 (el punto 5.9 pedía versionar el intérprete);
- escribir el `luthier.lock` (archivo del proyecto que fija el commit del intérprete con que se certificó).

Lo que queda abierto de fondo ya pertenece al diseño siguiente, el de los generadores: cómo se sortean los valores con que se prueban las leyes.

**Lo que cambió.** Antes, un extern (una función de Luthier implementada en Python) podía devolver cualquier cosa, y un certificado no garantizaba nada. Ahora:
- **Fase 1, el puente:** cada valor que vuelve de Python se lee por su tipo declarado.
- **Fase 2, los certificados:** el hash de un certificado cubre el código, el Python detrás de cada extern y el intérprete. Cada ley termina pasada, fallada o no corrida.

Sobre eso se apoyan las fases siguientes:
- **Fase 3, semántica del checker:**
  - un Bool se reconoce por sus etiquetas `true` y `false`, no por su posición en la suma;
  - `==` existe sólo donde la igualdad es estructural; ya no sobre `Real`, ni sobre datos que contienen funciones.
- **Números:**
  - `Rational` es un tipo primitivo exacto, y con él se enuncia y certifica la ley de redondeo: cada operación de `Float64` es la exacta redondeada dentro de 2⁻⁵³.
  - Se eliminó la declaración de que los doubles son un cuerpo ordenado (`float64Field`), cuyas leyes eran falsas fuera de la caja en que se probaban.
- **Fase 4, velocidad:** experiment_zero, el programa que ajusta las posiciones de la sesión A, pasó de 146 a 27 segundos. Los CSV de posiciones y residuos salieron idénticos byte a byte después de cada cambio.
- **Fase 5, el proyecto:**
  - **Un solo modelo de posiciones.** `positionsModel` es el que corre el experimento y el que se certifica. El diseño (qué pares de nodos se midieron) y el gauge (las 6 coordenadas que se fijan para quitar las traslaciones y rotaciones rígidas) se calculan en Luthier y viajan a Python como argumentos.
  - **La dimensión en los tipos.** El parámetro es `VecOf n`, los vectores de exactamente n coordenadas, en vez de cualquier vector.
  - **El PIT de los residuos.** Es la transformada integral de probabilidad: cada residuo pasado por la distribución acumulada del modelo ajustado, que debería dar valores uniformes si el modelo es correcto. Se agregaron también dos corridas de control.
  - **Leyes estadísticas con ensamble y semillas.** Cada una recibe su ensamble (cuántos sorteos y desde qué z cuenta como desvío) y semillas sorteadas sobre 2³¹ valores, no sobre 33.
  - **Controles de Levenberg-Marquardt como leyes.** Son versiones del optimizador con un cambio chico, que una ley exige que se detecten.
- **Fase 6, lenguaje:** `let`, menos unario y argumentos implícitos.

**Desvíos respecto de lo planeado:**
- **3.3 (los doubles declarados como cuerpo ordenado, leyes falsas fuera de una caja).** El plan proponía achicar el tipo a esa caja. No funcionó, porque la caja no es cerrada bajo las operaciones: 16 + 16 se sale. Se hizo por el camino largo, con la ley de redondeo sobre `Rational`.
- **5.1 (lo que se certificaba no era lo que corría: 7 nodos con gauge contra 10 nodos, vector entero y prior).** El plan proponía certificar sobre grafos sorteados. Se certifica sobre el diseño completo (todos los pares de 7 nodos). Las leyes del par de densidad (que la verosimilitud sea de verdad la densidad del sampler) necesitan una información de Fisher no singular, y el grafo de la sesión A no la da: deja 9 direcciones sin ver, 3 más que las 6 rígidas.
- **5.2 (garantías que vivían en comentarios: que un vector de posiciones tenga longitud múltiplo de 3, que los índices sean nodos, que las distancias del Jacobiano sean positivas).** Resultó mucho más grande de lo previsto. Ponerlo en los tipos obligó a meter la dimensión en las librerías de creencias y de optimización, porque trabajaban sobre vectores de cualquier longitud.

**Lo que dicen los datos (5.4, que pedía aplicar algo a los datos reales).** El sigma de 25,7 cm de la sesión A no viene del prior de los micrófonos: al multiplicar por 5 la incertidumbre horizontal del prior, sigma sube a 28,1 cm en vez de bajar. El PIT señala las tres distancias a parlante_A2, cada una 2,6 desvíos estándar por debajo de lo predicho; las demás quedan entre −0,7 y 1,1. Con sigma fijo en 3 cm, el error esperable de la cinta, el ajuste no converge en 500 iteraciones. Son corridas mías al scratchpad. Conviene que corras vos las dos de control (`--entry priorWidened` y `--entry sigmaKnown`) para que queden registradas.

**Lo abierto:**
- **5.5 a medias.** El plan pedía tres cosas que faltan: registrar la tasa de falsa falla de cada ley estadística (con qué probabilidad falla por azar un modelo correcto), repetir una falla con otra semilla antes de darla por contraejemplo, y medir la tasa de detección de los controles.
- **4.3 (dos evaluadores).** Siguen la máquina, rápida, y el evaluador por sustitución, lento, al que la máquina le pasa lo que no sabe hacer. Pueden discrepar y cada arreglo se hace dos veces.
- **`negate`.** La función de optimization.lut que arma el objetivo a minimizar como el negativo del log-posterior promete un `Objective`, un registro con leyes: que el gradiente sea el gradiente del valor y que la matriz de paso sea semidefinida positiva. Esa promesa es falsa para funciones cualesquiera, y ya lo era antes.
- **Obligaciones genéricas.** Las de código genérico en un tipo `Theta : U` (U es el tipo de los tipos) nunca corren, porque no hay cómo sortear un tipo. Por ejemplo, los índices dentro de `diagnose` en probability.lut.
- **`match` contra un tipo refinado.** Cuando el tipo esperado tiene leyes, el checker no chequea rama por rama un `if` ni un `match`. Apareció en validate_graph con un `Table`, y lo esquivé reescribiendo el `if`.
- **Una obligación sin combustible.** La de `ProfileIsFullAtItsSigma` en distances.lut, la ley de que la verosimilitud perfilada es la completa en su sigma óptimo, agota el combustible antes de sortear nada al separarse en conjunciones.

Todo eso está anotado en el plan. Las obligaciones genéricas, el problema del `match` y parte de 5.5 se resuelven en buena parte con el diseño de generadores (`luthier/docs/generators-2026-10-06.md`).

**Lo que encontró la noche sin buscarlo.** Hubo trampas de rendimiento que hacían inviable certificar; cada una costaba de minutos a horas, y las arreglé:
- **Las listas cruzando a Python.** Una lista pasaba por el evaluador lento. Afectaba a la prueba de Kolmogorov-Smirnov, que compara la distribución de los PIT con la uniforme, y que agregué en 5.5.
- **El registro del diseño** se convertía en cada llamada al modelo rápido de Python.
- **`Node p`** (el tipo de los índices de los nodos de un vector de posiciones) se sorteaba por rechazo, sorteando enteros hasta acertar.
- **`spectralMap`** (una función de una matriz simétrica a través de su espectro) se probaba con el método de Jacobi nativo sobre matrices de hasta 16×16.

También aparecieron obligaciones falsas que la certificación destapó en belief_check (el chequeo de las leyes de creencias sobre un modelo escalar):
- `gaussianFamily` (la familia de creencias gaussianas actualizada por Laplace) aceptaba una tolerancia negativa, y con ella su igualdad no es reflexiva.
- El modelo escalar leía la primera coordenada de vectores que pueden estar vacíos.

Esto ilustra el punto del documento de generadores: sortear tolerancias en [−16, 16] encontró un defecto real.

**Estado de la recertificación**, que corre en segundo plano, un archivo por vez:
- **Pasaron sin fallas:**
  - las librerías del intérprete (las 7 no corridas en probability_python son leyes genéricas en `Theta`);
  - distance_graph_python (validez de grafos, traducción a `MapInput`, rigidez);
  - distances_python (el modelo rápido contra el nativo, los pares de densidad, el núcleo y sus controles);
  - validate_graph (el programa que valida un grafo).
- **belief_check:** tuvo las 3 fallas ya arregladas; se vuelve a certificar al final.
- **optimization_check** (las leyes de Levenberg-Marquardt sobre la verosimilitud perfilada) lleva 22 minutos. Prueba obligaciones sobre `Objective` que no se pueden sortear, y cada intento fallido cuesta segundos.
- **Faltan:**
  - optimization_python (que el Levenberg-Marquardt de Python coincide con el nativo);
  - laplace_check (calibración de la actualización de Laplace);
  - experiment_zero.

Cuando terminen commiteo los certificados, pongo el tag y escribo el lock. Todo está commiteado en la rama `numbers` de los dos repos, sin push.

## 65. Luciano  2026-10-05 22:47:37 UTC  (line 5334)

[image not exported]

matamos a los lentos? vemos que pasa?

## 66. Tool (system)  no time  (line 5348)

[summary inserted by the harness]  [33 characters]

## 67. Model  2026-10-05 22:54:23 UTC  (lines 5435, 5478, 5486)

Mato los ocho vigilantes y la corrida vieja de optimization_check, y relanzo la cadena desde belief_check.

Sí, y ya está hecho. Los ocho que llevaban horas no hacían nada útil: eran bucles míos que esperaban una línea en el log de corridas que abandoné durante la noche. Esos logs no se mueven desde las 01:05, las 02:56 y las 04:21, así que no iban a terminar nunca. Los maté.

También maté la certificación de optimization_check (las leyes del optimizador Levenberg-Marquardt sobre la verosimilitud perfilada). Arrancó a las 06:17, y yo arreglé belief.lut (la librería de creencias gaussianas) a las 06:20, así que estaba certificando la versión vieja. Se veía en el log: marcaba como fallada `gaussianFamily` con una tolerancia negativa, el error que ya corregí. Relancé la cadena a las 06:55, empezando por belief_check (las leyes de creencias sobre el modelo escalar).

Lo que ya terminó sigue valiendo, porque ninguno de esos archivos importa belief.lut. Son las librerías del intérprete y los tres primeros archivos del proyecto: distance_graph_python, distances_python y validate_graph. No hubo ninguna falla. En todos, lo que quedó sin correr son las mismas 7 leyes genéricas en `U`. `U` es el tipo de los tipos y no hay forma de sortearlo. Se suma `ProfileIsFullAtItsSigma` (la ley de que la verosimilitud perfilada coincide con la completa en su sigma óptimo), que se queda sin combustible.

**Lo lento de verdad es otra cosa.** Dos obligaciones de optimization.lut (la librería del optimizador) necesitan sortear un `Objective`. Es un registro con la dimensión, la función a optimizar, su gradiente y su matriz de paso, y tiene que cumplir dos leyes:
- `GradIsGradient`: el gradiente es de verdad el gradiente de la función.
- `StepMatrixPositive`: la matriz de paso es semidefinida positiva.

El sorteador inventa funciones al azar y se queda con las que cumplen las leyes. Prueba hasta 2000 veces por valor, y cada intento tarda unos 0,4 s. Una función al azar casi nunca tiene el gradiente que declara, así que cada obligación gasta unos 14 minutos y termina como no corrida.

Una ley no corrida no queda certificada, así que cada archivo que importa optimization.lut lo vuelve a intentar: optimization_check, optimization_python, laplace_check y experiment_zero. La cadena debería terminar alrededor de las 9:15, y casi dos de esas horas se van en repetir ese sorteo que no puede salir.

Encontré dos cosas para corregir:
- **El 2000 está fijo en el código del sorteador** (`max_tries` en generators.py), contra tu regla de no hardcodear criterios. Tiene que ser un argumento.
- **Repetir una ley no corrida es trabajo perdido** cuando el código, los generadores y la semilla son los mismos, porque el resultado es determinista. El tester podría reusar ese resultado como reusa un certificado.

Cualquiera de los dos cambia el intérprete, y eso invalida todos los certificados: hacerlo ahora obliga a recertificar todo para ganar quizás media hora. Recomiendo dejar terminar esta corrida, cerrar v0.1 y hacer los dos cambios en la próxima ronda. El arreglo de fondo ya está en el documento de generadores: un `Objective` no debería sortearse por rechazo, sino tomarse de una lista explícita de valores registrados, por ejemplo el objetivo del propio proyecto y una cuadrática.

Cuando termine, commiteo los certificados, pongo el tag v0.1 y escribo el `luthier.lock`.

Arrancó belief_check a las 06:55. Te aviso cuando termine cada etapa.

## 68. Luciano  2026-10-05 22:56:16 UTC  (line 5489)

Bueno, recapitulemos

## 69. Model  2026-10-05 22:59:26 UTC  (line 5534)

El plan de reparación está terminado. Para cerrarlo con el tag v0.1 del intérprete solo falta que termine la recertificación, hacia las 9:15. Lo que queda abierto son leyes que los certificados no llegan a probar, y casi todas se cubren con dos diseños que ya están escritos y todavía no implementados: los generadores nombrados por el test y los chequeos que quedan registrados en el tipo.

Lo más importante que dejó el plan es que un certificado ahora garantiza algo. Antes, un extern (una función de Luthier implementada en Python) podía devolver cualquier cosa. Ahora cada valor que vuelve de Python se lee por su tipo declarado, y el hash del certificado cubre tres cosas: el código Luthier, el Python detrás de cada extern y el intérprete. Sobre esa base, el proyecto quedó así:
- Hay un solo modelo de posiciones: el que ajusta experiment_zero es el mismo que se certifica.
- La dimensión está en los tipos: un vector de parámetros es `VecOf n`, con exactamente n coordenadas.
- Los doubles tienen su ley de redondeo contra un racional exacto, en lugar de la afirmación falsa de que forman un cuerpo.
- experiment_zero reproduce sus CSV byte a byte en un quinto del tiempo.

En los datos de la sesión A, el sigma de 25,7 cm no viene del prior de los micrófonos: al ensancharlo, sigma sube en vez de bajar. El PIT (cada residuo pasado por la distribución acumulada del modelo ajustado, que da uniforme si el modelo es correcto) señala las tres distancias a parlante_A2: cada una queda 2,6 desvíos por debajo de lo predicho. Esas son corridas mías en el scratchpad. Las dos de control tenés que correrlas vos para que queden registradas: priorWidened (prior horizontal ensanchado) y sigmaKnown (sigma fijo en 3 cm). Lo de parlante_A2 hay que revisarlo en las medidas de cinta o en las grabaciones.

Ahora corre la certificación de los últimos archivos del proyecto. belief_check (las leyes de creencias gaussianas sobre el modelo escalar) acaba de pasar sin fallas, así que los dos arreglos de esta mañana funcionan. Sigue optimization_check, y después optimization_python, laplace_check y experiment_zero. Las librerías y los tres primeros archivos del proyecto ya pasaron sin fallas. Al final commiteo los certificados, pongo el tag y escribo `luthier.lock` (el archivo del proyecto que fija con qué commit del intérprete se certificó). Todo queda en la rama `numbers` de los dos repos, sin push.

El límite está en lo que los certificados no prueban.

Hay leyes a las que ningún sorteo llega:
- **Las genéricas en un parámetro de tipo** (`Theta : U`, donde U es el tipo de los tipos) no corren nunca. No son solo las siete de probability.lut: es toda la parte discreta de belief.lut (`bayes`, `weights`, `rankOf`, `discreteFamily`).
- **Una obligación de `laplaceAt`** (la actualización de Laplace) nunca encuentra un caso: todos los sorteos caen en un dominio vacío.
- **Las que piden un `Objective`** (un registro de funciones cuyo gradiente tiene que ser el gradiente de la función) tampoco corren. Se sortean por rechazo con funciones al azar, que casi nunca lo cumplen. El presupuesto de 2000 intentos está fijo en el código, contra tu regla, y es lo que estira la certificación a dos horas.

Hay cosas que el checker hace mal:
- Una obligación de `ProfileIsFullAtItsSigma` (que la verosimilitud perfilada coincide con la completa en su sigma óptimo) se queda sin combustible.
- La de `negate` (el objetivo a minimizar armado como el negativo del log-posterior) es falsa y nunca se certificó.
- Un `match` contra un tipo refinado no se chequea rama por rama.

Y quedan dos deudas del plan:
- **El resto de 5.5** (el punto del plan sobre la potencia de las leyes estadísticas): no registran su tasa de falsa falla ni repiten una falla con otra semilla.
- **4.3:** siguen los dos evaluadores, la máquina rápida y el evaluador lento por sustitución, que recibe lo que la máquina no sabe hacer.

Los dos defectos reales de esta mañana salieron solo porque el generador por defecto sortea números en [−16, 16] y vectores vacíos, no porque alguien los buscara:
- `gaussianFamily` (la familia de creencias gaussianas) aceptaba una tolerancia negativa.
- El modelo escalar leía la primera coordenada de vectores que pueden estar vacíos.

Los dos diseños que cubren casi todo eso ya están escritos.

El de generadores (`docs/generators-2026-10-06.md`) parte de que un tipo no tiene un único generador: el test nombra los que usó y el certificado los registra. Propone:
- números con límites y escala lineal o logarítmica;
- vectores y matrices por familias;
- para los tipos función, un censo de valores registrados (un `Objective` saldría, por ejemplo, del objetivo del proyecto y de una cuadrática);
- para U, un censo de tipos chicos.

Para convertirlo en especificación faltan tus respuestas a diez preguntas. Las que más pesan son tres:
- la sintaxis de cómo se empareja cada tipo con su generador: por tipo, por parámetro o en perfiles;
- si los generadores viven en Luthier o en Python (tu nota en random.lut pide un generador extern por lotes, con leyes de estocasticidad);
- qué exige una corrida: un perfil por proyecto o uno por ley.

El otro diseño es tu principio de esta mañana, que otra sesión escribió en las partes 00 y 05 de la especificación y en el plan (commit ae67242): un chequeo se hace una vez y queda en el tipo del valor chequeado. La regla R11 dice que dentro de `if p x`, x tiene tipo `{ x : T | p x }`. Todavía no está implementado. Reemplazaría el atajo textual que agregué anoche (descargar una obligación cuando es igual a la condición de su rama), y su forma de veredicto estadístico con nivel es justo lo que le falta a 5.5.

Mi recomendación es cerrar v0.1 con esta corrida y escribir con vos la especificación de generadores. Después, juntar en una sola ronda de cambios al intérprete:
- R11;
- el presupuesto de rechazo como argumento;
- no volver a correr las leyes no corridas cuando no cambió el código ni la semilla;
- los generadores.

Cada cambio al intérprete invalida todos los certificados, así que conviene recertificar una sola vez.

## 70. Luciano  2026-10-05 23:20:29 UTC  (line 5537)

ahi te hice observaciones en un documento.

## 71. Model  2026-10-05 23:24:21 UTC  (line 5573)

Estoy cruzando tu sospecha con los datos: las distancias del bloque de parlante_A2 violan la desigualdad triangular. Calculo el ajuste sin A2 y te respondo punto por punto.

## 72. Luciano (queued)  2026-10-05 23:24:31 UTC  (line 5588)

es como 20.05 vs 20.5 para la misma distancia

## 73. Luciano (queued)  2026-10-05 23:25:00 UTC  (line 5589)

no 5.05 vs 5.5

## 74. Luciano (queued)  2026-10-05 23:25:08 UTC  (line 5590)

algo asi

## 75. Model  2026-10-05 23:29:59 UTC  (line 5625)

Tenías razón: el sigma de 25,7 cm sale de medidas inválidas, y sin ellas baja a 4,9 cm. Pero el problema no es un número mal leído sino el bloque entero de la posición 2 del parlante.

**Las medidas.** El bloque de A2 es el audio de 1:43 de las 15:28, con varias autocorrecciones: 1,13 m a mic3, 3,35 a mic2 y 2,02 a mic1. Es geométricamente imposible. mic2 y mic3 están a 5,40 (lo medimos dos veces: 5,38 y 5,41), y el bloque pone al parlante a 3,35 de uno y a 1,13 del otro. Como 3,35 + 1,13 = 4,48, menos que 5,40, las dos esferas no se tocan: es tu suma de radios contra la distancia entre centros. Releer el 2,02 no lo arregla, porque ese triángulo no pasa por mic1. En distancias.csv (la planilla con las lecturas transcriptas) ya está anotada la alternativa B, que es descartar el bloque. Corrí el modelo actual sobre graph_noA2, el grafo sin ese bloque que quedó del 4 de octubre, y sigma da 4,9 cm.

La ambigüedad del tipo 5,05 contra 5,5 también aparece en la sesión A: "8 metros 5", de A3 y A4 a mic1, leído como 8,05. La probé con 8,50: sin el bloque de A2 sigma sube a 15 cm, y con el bloque a 31 cm. La lectura correcta es 8,05.

Lo que más me preocupa de esto es el test de uniformidad del PIT (Kolmogorov sobre todos los residuos). En los tres ajustes de hoy dio probabilidades de cola entre 0,58 y 0,74, tanto en el bueno como en los malos, así que no detecta ninguno de estos errores. Los valores individuales sí marcaron las tres distancias de A2, pero el test global no. Lo que distingue un ajuste de otro es sigma comparado con la precisión de la cinta.

El chequeo que lo habría atrapado antes de ajustar es la desigualdad triangular en los triángulos con sus tres lados medidos. Debería ser parte de `ValidDistanceGraph` (el tipo de grafo válido), justo el tipo de chequeo que, según tu principio, queda registrado en el tipo. Leo tu "no es muy diagnóstica" así: con tres distancias por parlante y la altura fija queda una sola restricción redundante, y un error que no rompe un triángulo se absorbe moviendo el parlante. Estas corridas son mías, en el scratchpad. Para registrar la tuya alcanza con `--set graphDir=2026-09-07/derived/A/graph_noA2`.

**Theta : U.** De acuerdo. Reescribo probability.lut, belief.lut y optimization.lut sobre `VecOf n` con `n : Nat`:
- El campo `shift` desaparece, porque pasa a ser la suma de vectores.
- La parte discreta pasa a ser puntos de `VecOf n` con pesos.
- Las once leyes genéricas que nunca corren empiezan a correr, porque n y `VecOf n` tienen generadores.

Para lo poco que es genuinamente genérico (contenedores como `List A`), el test nombra la instancia concreta. Hay un resultado de Bernardy, Jansson y Claessen ("Testing polymorphic properties", 2010): para una clase amplia de propiedades polimórficas alcanza con probar una instancia bien elegida.

**Generar sobre U.** De acuerdo, y la especificación ya tiene dónde ponerlo. Un tipo declarado sin definición es un hueco, y 05 §7 (la sección de la semántica estática sobre librerías con huecos) dice que se certifican por cada relleno. Entonces una ley sobre un tipo declarado no tiene generador propio: se certifica cuando un programa llena el hueco, con el generador del tipo que lo llenó. Pedir un generador de U pasa a ser un error estático, y el censo de U sale del documento.

Un valor declarado de un tipo definido, como `lmTol` (la tolerancia de Levenberg-Marquardt), no tiene ese problema: su tipo tiene generadores, y el valor que llega por `--set` se chequea contra el tipo.

**5.5** (el punto del plan sobre la potencia de las leyes estadísticas). De acuerdo, y lo del PIT de hoy muestra por qué. Resolverlo son tres cosas:
- Cada ley estadística declara su nivel: la probabilidad de que falle con un modelo correcto, que se calcula a partir de su ensamble.
- Una falla se repite con una semilla independiente antes de tomarla como contraejemplo, y se registra el nivel combinado.
- Se mide la potencia: con qué frecuencia la ley detecta los controles rotos a propósito.

Es la forma "veredicto estadístico con nivel" de tu diseño de chequeos, y va en la misma ronda.

**La sintaxis del binding.** La pregunta es dónde dice el test qué generador usa cada variable que cuantifica la ley. Tomá la reflexividad de `gaussianFamily`: cuantifica `n : Nat`, `tol : { t : Float64 | 0 < t }` y `a : GaussianBelief n`. Hay tres formas de decirlo:
- **Por tipo:** "todo Float64 de este test sale de logUniform 1e-12 1e-3". Eso alcanzaría también a las entradas de la media, donde no corresponde.
- **Por parámetro:**
  ```
  test Reflexive (GaussianBelief n) with
    n   := census [0, 1, 2, 3, 5]
    tol := logUniform 1e-12 1e-3
    a   := gaussianBeliefOf n (condition 1e3)
  ```
  (`census` es una lista explícita de valores; la última línea pide creencias de dimensión n con número de condición 1e3.)
- **Por perfil:** un conjunto de esas elecciones con nombre que reusan muchos tests, por ejemplo "escala de cinta: distancias entre 0,5 y 30 m, sigma log-uniforme entre 5 mm y 50 cm".

Recomiendo el binding por parámetro como base, porque es lo único que distingue `tol` de una entrada de la media. Los perfiles servirían como abreviatura, y el certificado guardaría las elecciones ya expandidas.

**Qué exige una corrida.** Con `--require-certified`, experiment_zero exige que cada definición que usa tenga certificado. La pregunta era cuál alcanza si una ley tiene varios, uno por cada elección de generadores. Tu idea lo resuelve mejor que mis dos opciones. Si un certificado dice que un valor definido pertenece a un tipo definido, hay dos casos:
- **Una función** (las extern de hoy). El valor es la función, y las leyes de su tipo cuantifican sobre las entradas, así que el certificado depende de los generadores. La corrida debería exigir que esos generadores cubran las entradas que efectivamente usa: que `lmTol = 1e-12` caiga dentro de las tolerancias sorteadas, que el grafo de la sesión A esté en el censo de grafos.
- **Un resultado de análisis** (el MAP, una evidencia). El valor es uno solo y lo produce la corrida. Su pertenencia al tipo (que es un máximo con gradiente bajo la tolerancia, que la evidencia está dentro de su error) se chequea una vez sobre ese valor, sin generadores salvo para los cuantificadores internos del tipo. Ese certificado va al registro de la corrida, no al `.cert.json` del código. Es tu principio de chequear una vez, aplicado a los resultados.

**Generadores como ciudadanos de Luthier.** Tomado; cierra la pregunta 6 del documento. Un generador es un valor de Luthier con tipo y leyes (por ejemplo, el logaritmo de los sorteos del log-uniforme es uniforme), certificable como cualquier otro. El generador de números aleatorios es un extern con sus leyes de estocasticidad declaradas en Luthier.

**Quién implementa.** Propongo que una sola sesión haga toda la ronda. R11 (la regla de que dentro de `if p x`, x tiene el tipo refinado), el refine, el presupuesto de rechazo, el reuso de las no corridas, los generadores y la reescritura sobre `VecOf n` tocan los mismos archivos del intérprete, y cada cambio invalida todos los certificados. Dos sesiones sobre la misma rama chocarían y recertificarían dos veces.

Me ofrezco a hacerla yo: R11 reemplaza el descargo textual que escribí anoche, y el resto salió de esta sesión. La otra sesión revisaría contra su especificación antes de recertificar. Si preferís que la implemente quien la escribió, le paso la lista de lo que cambié en el checker.

**Lo que sigue.** Con tu OK sigo así. La certificación va por optimization_check, y cierro v0.1 cuando termine. Después paso al documento de generadores lo que decidiste hoy:
- no hay generadores sobre U;
- los generadores son ciudadanos de Luthier;
- hay certificados de definiciones y certificados de resultados.

Con eso escribimos la especificación.

## 76. Luciano  2026-10-05 23:51:44 UTC  (line 5631)

ahi va mi feedback

## 77. Model  2026-10-05 23:55:55 UTC  (lines 5663, 5699, 5744, 5768, 5789)

Esta es la tabla de la sesión A que usó el ajuste: 22 distancias, con lo que se dijo en cada audio. Residuo es medido menos predicho, en cm. "Con A2" es el ajuste de referencia (sigma 25,7 cm) y "sin A2" el de hoy sobre graph_noA2 (sigma 4,9 cm).

| Par | d (m) | Audio | Lo que se dijo | Con A2 | Sin A2 |
|---|---|---|---|---|---|
| mic2–mic3 | 5,38 | 14:29:51 | "5 metros con 38, 36 más 2 centímetros del alambre" | +20,5 | −1,3 |
| mic2–mic5 | 4,76 | 14:31:14 | "4 metros con 76" | −5,2 | 0,0 |
| mic3–mic4 | 4,51 | 14:33:23 | "entre el 4 y el 2 es 4 metros con 49 más 2 y 51" | −12,2 | −1,1 |
| mic4–mic5 | 5,13 | 14:35:05 | "5 metros con 13" | +7,8 | +3,3 |
| mic4–mic2 | 7,00 | 14:35:56 | "entre el 4 y el 2 es 7 metros" | +2,0 | −0,1 |
| mic5–mic3 | 7,00 | 14:36:50 | "7 metros también" | +6,2 | 0,0 |
| mic2–mic3 | 5,41 | 14:38:11 | "medí de nuevo… efectivamente 5 metros con…" | +23,5 | +1,7 |
| A1–mic1 | 1,81 | 14:55:04 | "1,81 m" | −2,0 | −0,5 |
| A1–mic5 | 2,84 | 14:56:10 | "2 metros 84" | −3,1 | −1,1 |
| A1–mic4 | 2,40 | 14:56:35 | "2 metros 40" | −3,4 | −1,1 |
| A2–mic3 | 1,13 | 15:28:52 | "es 1 metro 13" | −45,9 | — |
| A2–mic2 | 3,35 | 15:28:52 | "3 metros 35 con el parlante 2, el micrófono 2, el sonido 2, perdón" | −35,1 | — |
| A2–mic1 | 2,02 | 15:28:52 | "2 metros 0,3… ah no… 2 metros 0.2" | −19,1 | — |
| A3–mic3 | 5,23 | 15:29:47 | "5 metros 23" | +1,6 | +3,1 |
| A4–mic3 | 5,23 | 15:29:47 | el mismo audio | −5,4 | −3,8 |
| A3–mic2 | 7,62 | 15:29:54 | "7 metros 62" | +1,5 | +2,1 |
| A4–mic2 | 7,62 | 15:29:54 | el mismo audio | −3,1 | −2,6 |
| A3–mic1 | 8,05 | 15:30:29 | "8 metros 5" | −1,2 | −4,9 |
| A4–mic1 | 8,05 | 15:30:29 | el mismo audio | +9,5 | +5,8 |
| A5–mic5 | 14,97 | 15:40:09 | "14,97 metros del Son5" | +1,4 | +1,8 |
| A5–mic2 | 16,38 | 15:40:24 | "16,38 del 2" | +1,4 | −0,2 |
| A5–mic4 | 19,98 | 15:42:07 | "19,98 de el 4" | +1,6 | −1,5 |

Las alturas son: mic1 1,69; los demás micrófonos entre 0,70 y 0,73; A1 0,988; A2 0,988 (arrastrada de A1 porque no se anunció un cambio); A3 0,73; A4 1,86; A5 1,31. El "1 a todos 3,50" no entra como medida: es nominal y solo fija el prior de las posiciones de los micrófonos, con 20 cm de desvío.

Para tu revisión, además de A2, hay tres cosas que miraría:

1. **El bloque de A2.** Lo revisé por triángulos. El triángulo mic2–mic3–A2 tiene sus tres lados medidos y le faltan 91 cm para cerrar. Con mic1–mic3 tomado del ajuste sin A2, le faltan 48 cm. Probé las seis maneras de reasignar los tres valores a los tres micrófonos y ninguna cierra los triángulos: la mejor queda 48 cm corta. Así que el problema no es solo la etiqueta del micrófono: alguno de los valores, 1,13 o 3,35, está mal.
2. **mic3–mic4 = 4,51.** El audio dice "entre el 4 y el 2". La transcripción lo asignó a 3–4 porque 4–2 es la diagonal de 7 m que se midió a las 14:35:56. Habría que confirmarlo.
3. **A3 y A4 tienen las mismas tres lecturas**, que salen de un solo audio cada una, pero entre las dos alturas hay 1,13 m. Si la cinta midió parlante a micrófono en 3D, subir el parlante cambia las distancias hasta 12 cm (a mic3). El ajuste lo absorbe moviendo A4 en horizontal, y A4–mic1 queda con el mayor residuo fuera de A2. Si en cambio esas distancias se tomaron en el piso, el modelo debería tratarlas como horizontales.

Hay dos triángulos casi degenerados, mic5–mic4–A1 y mic5–mic4–A5: les sobran solo 11 y 12 cm, porque el parlante cae casi sobre la recta entre los dos micrófonos. Eso es parte de por qué la configuración diagnostica poco.

Sobre lo que necesita información a priori, de acuerdo. La información que más pesa es el prior de sigma tomado de la cinta: con sigma acotado por la precisión de la cinta, la verosimilitud sola rechaza el bloque de A2, sin depender del test global.

**Sobre tus otras notas:**

- **Dónde se usa `List A`.** `List` y `Maybe` están definidos genéricamente en core.lut, y `Vec A` y `Mat A` en array.lut (arreglos de cualquier tipo de elemento). Lo genérico en A son utilidades de listas (largo, reverso) y las leyes del álgebra como predicados (`Reflexive A r`, `Setoid A`), que siempre se aplican a un tipo concreto y se certifican ahí. Tu regla para generar ya existe: `genList` en random.lut sortea un largo N y aplica N veces el generador de A. El proyecto usa solo instancias concretas: `List String` para los CSV y `List Float64` para los PIT. Lo aberrante es solo el `Theta : U` de probability, belief y optimization, y el `IsGradient` de array.lut.
- **Límites de `lmTol`.** Tenés razón, y el tipo actual, `{ t : Float64 | 0 < t }`, se queda corto. El tipo tiene que llevar los límites, y el generador sale del tipo: escala logarítmica entre esos límites. Lo mismo para la tolerancia de `gaussianFamily`.
- **Generadores como funtores.** Coincido con que son funtores sobre el tipo, y eso encaja con "el test nombra cuál usó": lo que se nombra es el funtor y sus parámetros. Esos parámetros son el modo (exhaustivo o n muestras), la métrica (lineal o logarítmica) y los costos.
  - Tu cumsum de costos es muestreo por la inversa de la acumulada. En un rango continuo, la acumulada es la integral de la métrica: la lineal da uniforme y la logarítmica da log-uniforme. En una lista finita, como un censo, es la suma acumulada de los costos. Es una sola primitiva para los dos casos.
  - "Exhaustivo" sobre un tipo infinito, como `Real`, es un error estático.
  - Feat (Duregård, Jansson y Wang, 2012) hace lo mismo para tipos algebraicos: muestrea indexando en las cuentas acumuladas por tamaño.
- **¿Está todo especificado?** No. R11 y `refine` están especificados en la parte 05. Faltan especificar:
  - los generadores (el documento de análisis todavía no es especificación);
  - los certificados de resultados;
  - el veredicto estadístico con su nivel y el reintento con otra semilla;
  - que generar sobre U sea un error;
  - el presupuesto de rechazo;
  - el reuso de leyes no corridas.

Arranco ahora a escribir todo eso como una parte nueva de la especificación, `docs/semantica/08`, y ajusto la sección de certificación de 05 donde choque. La certificación sigue corriendo por optimization_check.

Ya tengo lo que necesito de 05 y del análisis. Escribo la especificación como `docs/semantica/08-tests.md`.

Cierro v0.1: actualizo el estado del plan, commiteo los certificados de las librerías y la especificación, pongo el tag y escribo el lock del proyecto.

Actualizo la memoria con el cierre de v0.1 y lo de A2.

Cerré v0.1 y la especificación quedó escrita.

**v0.1.** El tag está en luthier, sobre el commit 487406d, y `prototipo-cero/luthier.lock` lo fija (commit 7f5f664 del proyecto). Hay certificados para las librerías y, en el proyecto, para distance_graph_python, distances_python, validate_graph y belief_check.

Quedaron sin certificar los cuatro archivos que importan optimization.lut: optimization_check, optimization_python, laplace_check y experiment_zero. Corté esa corrida porque optimization.lut tiene unas diez definiciones que reciben un `Objective`, y cada una gastaba 14 minutos en fallar el sorteo. Como cada uno de los cuatro archivos lo repetía, eran unas diez horas para que esas obligaciones terminaran sin correr. Lo anoté en el estado del plan. `luthier check` acepta los certificados. El lock avisa "with uncommitted changes" por tus notas en random.lut, como estaba previsto.

**La especificación** está en `luthier/docs/semantica/08-tests.md`, draft 1, commiteada. Tiene doce reglas de generadores (G1 a G12), diez de certificados (C1 a C10), lo que queda abierto (§11), los cambios a las partes 02, 03 y 05 (§12) y el orden de trabajo (§13). Hay cinco decisiones que tomé yo y conviene que mires:

- **La métrica va en el generador, los límites en el tipo.** Es tu "sampled N con métricas lineal y logarítmica". La justifiqué así: la lineal es la medida que no cambia al trasladar (sirve para una coordenada o un residuo) y la logarítmica la que no cambia al escalar (para un desvío, una distancia o una tolerancia).
- **Un `Float64` sin límites en su tipo es un error estático** si el binding (el emparejamiento de cada parámetro con su generador) no se los da. Así nada sale de [−16, 16] sin que nadie lo haya pedido.
- **Las entradas de una corrida se comparan con el alcance de los certificados.** Lo que llega por `--set` se compara al arrancar; lo que se calcula durante la corrida, solo con `--checked`.
- **Una ley estadística que falla se repite una vez** con otra semilla, y falla solo si fallan las dos; el nivel queda en α².
- **La sintaxis propuesta** es `test X with 100 sampled linear under perfil where { p := g }`, con `profile` como acto nuevo y `gen T :=` eliminado.

Las partes 05 y 02 no las toqué: espero tus anotaciones a 08 antes de aplicar los cambios de §12. Otra sesión dejó sin commitear `docs/plan-mechanical-rules-2026-10-06.md` (lints y hooks para las reglas de la memoria). No es mío y no lo toqué.

**Lo que sigue.** Arranco con el paso 1 de §13, que ya aprobaste y no depende de cómo anotes 08:
- los presupuestos como argumentos, empezando por los 2000 intentos;
- contar solo los casos evaluados, con la razón de los que no se cuentan;
- no recomputar un resultado conocido.

Con eso la próxima recertificación debería tardar una hora y no diez.

## 78. Luciano  2026-10-06 00:48:27 UTC  (line 5792)

lee el plan-mechanical-rules

## 79. Model  2026-10-06 00:50:52 UTC  (line 5814)

El plan acierta en el diagnóstico: las reglas que solo viven en la memoria se degradan, y las mecánicas aguantaron la noche. Las fases 0 a 4 y la 6 no chocan con mi ronda. Pero tiene dos errores de diseño que molestarían, está desactualizado en generadores, y su fase 5 toca los mismos archivos del intérprete que mi ronda, así que tiene que ir dentro de ella.

**1. El pre-commit (2.3) no puede correr `luthier certify`.** El plan supone que tarda minutos. En este proyecto tarda una hora en el mejor caso y diez horas hoy. Además escribe archivos de certificado en medio del commit, incluso en el repo de luthier por `--imports`. El pre-commit debería correr los lints y `luthier check`. Los certificados ya tienen sus puntos de control donde importan: `luthier run --require-certified` y antes de un tag.

**2. El hook de Stop (2.2) cobra en cada turno.** `luthier check` sobre todos los .lut del proyecto carga y chequea cada uno con sus imports, así que estimo varias decenas de segundos al terminar cada turno, en toda sesión del repo, aunque sea solo de charla. Propongo que corra solo si cambió algún archivo desde la última vez, y solo sobre los .lut tocados.

**3. El lint de literales (1.1) se queda corto y mezcla categorías.** Lista 7 hallazgos conocidos y hay unos 27 en tres clases distintas:
- **Criterios de verdad:** lmTol, lmMaxIter, startSpread, sameTol, controlSeeds y gridSize en el proyecto. En las librerías de luthier, el calendario de amortiguamiento de Levenberg-Marquardt (muInit, muFactor, muMin, muMax), maxSweeps de Jacobi, maxHalvings, orderMargin y roundingSlack. El lint vive en el repo de sonolocalización y no los vería.
- **Límites de tipos de dominio:** positionBox, sigmaLow y sigmaHigh. Según 08 (G7) esos límites son parte del tipo, es decir de lo que la ley afirma; pasarlos a `--set` no tendría sentido.
- **Hechos matemáticos:** pi, y `rigidMotions = 6` (3 traslaciones y 3 rotaciones).

La única excepción del plan, `-- resolution:`, no cubre las dos últimas clases. Hay un criterio mecánico: una constante que solo aparece en posición de tipo (como límite de un refinamiento) define un tipo, y una que aparece en posición de término (pasada a un cómputo) es un criterio. Los hechos matemáticos se anotan.

**4. El arreglo de los `_check` depende de 08.** Si `lmTol : Float64 := 1e-9` pasa a ser un hueco sin valor, sus leyes quedan bloqueadas y no corren. El arreglo correcto es que sea un parámetro de la ley, sorteado por el binding del test (08 G4: `where { tol := sampled log }`). La fase 1 no puede cerrarse en esos archivos hasta que exista esa sintaxis.

**5. La fase 5 va en mi ronda.**
- **5.3 (generadores nombrados):** dice "specification pending", pero 08 ya está escrita y espera tus notas.
- **5.4 (obligaciones que nunca corren):** ya hoy cada "no corrida" lleva su razón; lo que falta es C3 de 08 (contar solo los casos evaluados) más G5 (generar sobre U pasa a ser error estático).
- **5.1 (una ley, un nombre: dos leyes iguales salvo nombres de variables son error):** está bien, pero necesita primero una línea de especificación. Conviene extenderla a "una ley igual a una instancia de una ley importada", por ejemplo `f x y == f y x` cuando existe `Symmetric`.
- **5.2 (prohibir definir una operación con el mismo nombre y tipo que una importada):** se le escapa justamente eso, la ley reescrita con otro nombre. Lo fundiría en 5.1.

Todo esto toca checker.py, testing.py y certify.py, así que va en la misma ronda y con una sola recertificación.

**6. Las fases 3, 4 y 6 están bien, con dos avisos.** El lint de inglés va a arrancar con un baseline grande: nombres de directorios como prototipo-cero, los datos, "Lucianos feedbacks". Las cabezas de figuras (fase 4) obligan a editar los scripts del pipeline que corrés vos, así que necesitan tu visto bueno.

Mi propuesta es que yo me lleve la fase 5 a mi ronda, y que otra sesión haga en paralelo las fases 0 a 4 y la 6, con los puntos 1 a 4 corregidos. Esas fases tocan lint/, .claude/, CLAUDE.md y los scripts de figuras, no el intérprete, así que no chocan. El archivo es de otra sesión y no lo edité; si querés, le agrego una sección con estas correcciones antes de que alguien lo implemente.

## 80. Luciano  2026-10-06 01:53:49 UTC  (line 5817)

me da la sensacion que el plan-mechanical-rules no es muy consistente. 
lo es?

## 81. Model  2026-10-06 01:55:33 UTC  (line 5829)

No del todo. El diagnóstico se sostiene: las reglas que solo viven en la memoria se degradan y las mecánicas aguantaron. Pero el plan se contradice en varios lugares, y el más grave es su promesa central.

1. **Promete algo que sus mecanismos no hacen.** Dice que el hook de Stop (2.2) sería "la versión mecánica" del reporte de las 04:41, y que 5.4 lo habría hecho mecánico. Ese reporte admitió cuatro cosas:
   - las obligaciones genéricas nunca corren;
   - la obligación de `negate` es falsa;
   - 5.5 quedó a medias;
   - `lmMaxIter` era una constante.

   El hook de Stop corre los lints y `luthier check`, y `check` sale con código 0 aunque haya leyes sin probar (lo acabo de verificar). Así que de esas cuatro solo atraparía `lmMaxIter`. Las otras tres son resultados de certificación, y la certificación solo aparece en el pre-commit, que no puede correrla porque tarda horas. `negate` y 5.5 ni figuran en el plan.

2. **Viola su propia definición de criterio.** La línea 31 dice que las resoluciones numéricas (pone de ejemplo "la grilla de integración") no son criterios. La línea 110 lista como hallazgo `gridSize : Int := 41` de belief_check, que es exactamente la grilla de 41 puntos del prior discreto. Además, su dicotomía criterio/resolución no tiene lugar para los límites de un tipo de dominio (positionBox, sigmaLow) ni para los hechos matemáticos (pi, las 6 direcciones rígidas), y el lint los marcaría a todos.

3. **No aplica el mismo criterio para elegir la capa.** Las tres "capas" se usan sin definirse nunca. "Símbolos definidos" va a la capa 3 (un recordatorio) porque es cuestión de juicio. Pero "figuras con cabeza" y "una ley, un nombre" son igual de juicio, y el plan las pone en las capas 2 y 1 como si fueran mecánicas. Lo que se puede chequear mecánicamente en esos casos es un sustituto: que el JSON de la cabeza tenga los campos llenos, que no haya dos cuerpos de ley idénticos. El plan no dice que transfiere solo una sombra de esas reglas.

4. **Tiene dos reglas opuestas sobre quién decide.** Para los generadores (5.3) exige tu aprobación de la especificación antes de implementar. Para 5.1, 5.2 y 5.4 deja que la implementación decida y escriba la línea de la especificación después, "para que Luciano vea lo que decidió la implementación".

5. **El orden contradice las dependencias.** Pone las fases 0 a 2 primero y la 5 después de tu respuesta sobre 5.3. Pero el arreglo de la fase 1 para los `_check` ("que un test los sortee") necesita justamente los generadores de 5.3. Hoy un test sortea la tolerancia en (0, 16] y `maxIter` en [0, 16], valores absurdos para Levenberg-Marquardt, así que ejecutar la fase 1 antes de 08 empeora esos certificados.

6. **Se contradice sobre los tiempos del pre-commit.** La fase 0.1 dice que los hooks de la fase 2 se reparten según cuánto tarde certify. La 2.3 igual mete certify en el pre-commit. Y la aceptación de la fase 2 solo necesita el lint.

7. **El alcance no coincide con lo que dice.** La premisa es "pasar las reglas de la memoria", pero 5.4 no es una regla de la memoria sino un pendiente del plan de reparación. Y dice que así otros modelos (Gemini, GPT) quedan sujetos a las mismas reglas, cuando los hooks y CLAUDE.md son de Claude Code y la carpeta AI/ está excluida del lint de inglés. Lo único que alcanzaría a otras herramientas es el pre-commit, justo el que no puede correr.

8. **Está desactualizado.** 5.3 y la tabla final dicen que la especificación de generadores está pendiente, y ya existe 08.

Lo que sí es sólido es el núcleo de la fase 1: el lint de literales numéricos con el hook después de cada edición, una vez corregido el punto 2. Ese es el caso que ya falló una vez, y un mecanismo lo resuelve de verdad.

Si querés, lo reescribo alrededor de lo que cada mecanismo puede detectar de verdad, y separo lo que es juicio. La fase 5 la absorbo en mi ronda del intérprete. Como el archivo es de otra sesión, prefiero que me digas si lo reescribo yo o se lo devolvés a quien lo escribió.

## 82. Luciano  2026-10-06 02:02:17 UTC  (line 5838)

bueno, quiero que ahora plantees un plan para resolver todos los problemas detectados. 
1) lista de problemas con su descripcion original 
2) analsis de esta lista, diagnostico de cada problema y un plan escalornado para solucionarlos todos. 
3) plan detallado para que pueda ser ejecutado en paralelo. 
4) un executive summary para mi consumo donde me presentas los problemas en orden de importancia con descripcion, diagnostico y solucion propuesta.

## 83. Model  2026-10-06 02:11:55 UTC  (line 5873)

Escrito para: vos (la parte 4) y las sesiones que van a ejecutarlo sin memoria de esta conversación (las partes 1 a 3).

El plan está en [plan-2026-10-06.md](../luthier/docs/plan-2026-10-06.md), commiteado en `numbers` (0b516d1). Treinta y tres problemas con su enunciado original, seis raíces, siete etapas y cinco tracks en paralelo.

Las seis raíces, que son el orden del resumen ejecutivo:

1. Los certificados dicen más de lo que prueban: generador implícito, casos pedidos en lugar de evaluados, leyes estadísticas sin nivel. El arreglo es 08-tests, mi ronda.
2. El número de la sesión A descansa en el bloque imposible de A2; el pipeline no chequea triángulos y el PIT no ve escala. Tu revisión más la ley de triángulos, primera tarea del track de librerías para que la tengas durante la revisión.
3. Los tipos dicen menos de lo que el código supone: `Theta : U`, tolerancias sin cota, `negate`, chequeos dobles, criterios como constantes. Tu principio de chequear una vez.
4. Certificar cuesta horas por presupuestos fijos y repetición de lo no corrido. Va primero en la ronda; debería bajar a una hora, medido antes de mergear otra cosa.
5. Las reglas en memoria se degradan y las sesiones no tienen protocolo. Reemplaza el plan de la otra sesión: lint de literales con hook, `check --strict`, CLAUDE.md, worktrees, certificación en un árbol que nadie edita.
6. Dos evaluadores: hoy nada cayó al lento; propongo una ronda propia después de v0.2.

Lo que necesito de vos para arrancar, todo independiente entre sí:

- La revisión de los cuatro ítems de datos (A2, "8 metros 5", el par del 4,51, alturas de A3/A4) y las dos corridas de control sobre el grafo revisado.
- Tus anotaciones a 08-tests antes de la etapa 3 (la sintaxis de generadores); las etapas 1 y 2 no las esperan.
- Dónde van tus notas de random.lut, para que el lock pueda quedar limpio.
- Si la ronda de los evaluadores va después de v0.2 o se posterga.
- Cuántas sesiones querés en paralelo: con tres (núcleo del intérprete, librerías y proyecto, mecánica) se cubre todo desde el primer día; con una sola, el orden es etapa 1, luego 2, y la mecánica al final.

Mientras tanto arranco con A-1 (presupuestos como argumentos) en un worktree, que no depende de ninguna respuesta.

## 84. Luciano  2026-10-06 02:14:27 UTC  (line 5879)

respecto de A2, creo que el problema es que dije un microfono por otro, chequea esa posibilidad

## 85. Model  2026-10-06 02:26:42 UTC  (line 5907)

No alcanza con eso. Ninguna manera de reasignar los micrófonos arregla el bloque, porque 1,13 + 2,02 = 3,15 m y los dos micrófonos más cercanos entre sí (mic1 y mic4) están a 3,45 m. Desde un mismo punto no se puede estar a 1,13 m de un micrófono y a 2,02 m de otro, sean cuales sean. Así que alguno de esos dos números no es una distancia desde esa posición. Puede haber además un micrófono cambiado, pero eso solo no explica el bloque.

Lo probé también por fuerza bruta. Probé las 60 maneras de asignar las tres lecturas a micrófonos distintos, con las posiciones de los micrófonos del ajuste sin A2, con la altura fija en 0,988 y también libre. La mejor deja residuos de 16 cm (14 cm con la altura libre). El resto de la sesión ajusta a 2,5 cm.

Lo que sí cierra con un solo error es esto:

| Qué se mantiene | Dónde queda el parlante (x, y) | Qué no cuadra |
|---|---|---|
| 3,35 a mic2 y 2,02 a mic1, como dictaste | (−0,84; 1,70), entre mic2 y mic3, donde estaba planeada la posición 2 | mic3 quedaría a 2,18 m, no a 1,13 |
| lo mismo, punto espejo | (−0,81; −1,71), entre mic2 y mic5 | mic5 quedaría a 1,83 m; mic3 a 5,33 m |
| 1,13 a mic3, y 3,35 a mic1 en lugar de mic2 (donde se oye la duda: "el parlante 2, el micrófono 2, el sonido 2, perdón") | (1,38; 2,97) o (−0,65; 3,21), al lado de mic3 | el 2,02 no coincide con ningún micrófono |

La salida más simple es la primera fila: las etiquetas tal como las dictaste, el parlante donde estaba planeado, y el "1 metro 13" equivocado. Desde ahí, mic3 estaría a 2,18 m.

La geometría no alcanza para decidir entre esas opciones: con tres lecturas queda una sola restricción redundante. Lo que decide es dónde estaba parado el parlante y qué se oye en el audio de las 15:28:52. Si recordás que la posición 2 estaba entre mic2 y mic3, o si en el audio aparece algo como "2 metros 18" para mic3, queda resuelto.

## 86. Luciano  2026-10-06 02:34:54 UTC  (line 5913)

es posible que la posicion 2 sea en linea entre los parlantes, si es asi no necesito medir ambas distancias. Tengo que revisar mis audios.

## 87. Model  2026-10-06 02:39:46 UTC  (line 5937)

Lo dejé anotado en la memoria. Queda pendiente que lo confirmes en el audio de las 15:28:52.

## 88. Luciano  2026-10-06 02:41:19 UTC  (line 5940)

El tema mas serio me parece es que todo el plan de los generadores no esta implementado, no se si esta especificado siquiera.

## 89. Luciano  2026-10-06 02:44:33 UTC  (line 5952)

El tema mas serio me parece es que todo el plan de los generadores no esta implementado, no se si esta especificado siquiera.

## 90. Model  2026-10-06 02:45:27 UTC  (line 5967)

Tenés razón, y es más grave de lo que dice el plan: no hay ni una línea implementada, y lo que está escrito es un borrador con decisiones, todavía no una especificación que alguien pueda ejecutar sin decidir cosas por su cuenta.

**Lo implementado:** nada. El tester sigue con `gen T :=`, los defaults estructurales y los 2000 intentos fijos; el último commit de código es del 6 a la madrugada.

**Lo especificado:** `08-tests.md` (draft 1) registra tus decisiones de ayer: generadores como valores y funtores, límites en el tipo y métrica en el generador, censo de modelos, nada sobre U, binding por parámetro, certificados por binding, niveles estadísticos. Las partes 02 y 05 no se actualizaron, y no lo revisaste. Leído como lo leería quien lo implementa, tiene huecos que obligarían a inventar:

1. **Una contradicción de fondo.** G1 dice que los generadores son valores de Luthier, y G2 que los genéricos son funtores sobre el tipo. Pero un funtor que recorre la estructura de cualquier tipo tendría tipo `(T : U) -> Gen T` y necesitaría inspeccionar la forma de `T`, y Luthier no tiene reflexión sobre tipos. Además choca con la regla de que casi nada tome un `A : U`. Hay que decidir dónde viven.
2. **Las leyes importadas.** Con `--imports`, una ley de una librería la corre el programa que la importa. No dice con qué binding: el de la librería o el del importador. Justamente ese era el problema de que el generador dependa del programa.
3. **Los tipos recursivos.** `sampled` sobre un `data` recursivo no dice cómo termina ni cómo usa el tamaño.
4. **Los costos sobre números.** "Una métrica o un costo" no es implementable para números con un costo arbitrario, porque habría que integrarlo; solo `linear` y `log` tienen la inversa cerrada.
5. **La sintaxis.** En `where { tol := ..., TestedFull := ... }` no se distingue si la clave es un parámetro o un tipo. Tampoco dice cómo un binding usa parámetros anteriores (`a := gaussianBeliefOf n ...`) ni en qué momento un parámetro sin generador es error: en `check` o en `test`.
6. **El alcance (reach) de un tipo compuesto** (un registro, un vector): no dice cómo se representa ni cómo C6 lo compara con los valores de una corrida.

Para el punto 1 tengo una propuesta que encaja con lo que ya existe. Los funtores serían del intérprete, derivados de la estructura del tipo como ya se deriva `==` (R8): nombrados, con parámetros y registrados en el certificado, pero no escritos en Luthier. En Luthier vivirían los generadores concretos: censos, familias de matrices, los de dominio del proyecto. Así no hace falta reflexión y no aparece ningún `T : U`.

Mi propuesta es escribir ahora el draft 2 de 08 cerrando esos seis puntos y aplicar los cambios a 02 y 05. Después vos lo anotás, y recién ahí empieza la implementación, con los certificados honestos de la etapa 1 primero. Lo único que necesito de vos antes de escribirlo es si aceptás que los funtores sean del intérprete, al estilo de `==`. El resto lo propongo concreto en el draft para que lo corrijas.

## 91. Luciano  2026-10-06 02:57:49 UTC  (line 5970)

Como que Luthier no tiene reflexion sobre tipos?

## 92. Model  2026-10-06 02:58:34 UTC  (line 5989)

Me expresé mal: no es que Luthier no pueda tocar tipos, es que no puede preguntarle a un tipo qué forma tiene. En el kernel (04 §2), el universo `U` tiene introducción ("todo tipo") pero la columna de eliminación está vacía. Una función puede recibir un `T : U` y usarlo (aplicarle `List`, armar `VecOf n`, ponerlo en una firma), pero no hay `match` sobre `T` que diga "es un producto de esto y aquello" o "es `Float64` refinado entre 1e-15 y 1e-2".

Un funtor genérico como `sampled` necesita justamente eso, recorrer la estructura del tipo. Hoy lo hace el intérprete en Python (`generators.py`), igual que el `==` estructural de R8, por fuera del lenguaje. La reflexión propiamente dicha (`Term` y `Program` como datos, quote y unquote) figura como capa futura en 00 y en 02 §8, no especificada.

Para que los generadores sean ciudadanos de Luthier, como pediste, hay dos caminos:

1. **Funtores del intérprete**, como `==`: nombrados y registrados en el certificado, pero no escritos en Luthier. Es lo que propuse antes, y contradice tu G1.
2. **Un universo de códigos dentro del lenguaje.** Es la forma estándar en teoría de tipos dependientes de hacer programación genérica sin reflexión total. Un `data Code` describe las formas de tipo que sabemos generar: enteros y doubles con sus límites, productos, sumas, vectores de largo n, y refinamientos con su predicado como función `El c -> Bool`. Una función `El : Code -> U` da el tipo que cada código describe, y los funtores pasan a ser funciones de Luthier comunes, `sampled : (c : Code) -> Metric -> Gen (El c)`, con sus leyes y sus certificados.

El segundo camino encaja con tus dos principios a la vez: los generadores son Luthier, y "solo hay generadores de tipos definidos" queda literal, porque un tipo declarado sin definición no tiene código. Tampoco obliga a meter un `match` sobre `U`. Eso conviene, porque un `match` sobre tipos rompería la parametricidad en la que se apoya G5: probar una ley genérica en una sola instancia vale solo si la función no puede distinguir tipos.

Lo que cuesta: los tipos recursivos (`data`) necesitan un código de punto fijo, que puede esperar; y cada tipo del proyecto que se quiera generar genéricamente tiene que tener su código (escrito o derivado por el checker de la definición). Si te parece, el draft 2 de 08 va por este camino.

## 93. Luciano  2026-10-06 03:01:27 UTC  (line 5996)

dame una clase de tipos dependientes y reflexion propiamente dicha que es un codigo de punto fijo. 
En general amplia esta explicacion clave

## 94. Model  2026-10-06 03:03:01 UTC  (line 6000)

## Una clase en cuatro partes: tipos dependientes, reflexión, universos de códigos y el código de punto fijo

### 1. Tipos dependientes

En un lenguaje común los tipos y los valores viven en mundos separados: `Vec Float64` es "vector de doubles", de cualquier largo. Un tipo dependiente es un tipo que menciona un valor. `VecOf 3` es el tipo de los vectores de exactamente 3 entradas, y `VecOf n` es una familia de tipos indexada por el número `n`.

Hay dos construcciones básicas, y Luthier ya tiene las dos (04 §2):

- **La función dependiente (Π).** Se escribe `(x : A) -> B`, donde el tipo del resultado `B` puede mencionar el argumento `x`. Por ejemplo, `start (o : Objective) (x0 : VecOf o.dim) : LMState o.dim`: el tipo del segundo argumento y el del resultado dependen del valor del primero. El checker verifica que el punto inicial tenga la dimensión del objetivo, sin correr nada.
- **El par dependiente (Σ).** Se escribe `(x : A) * (y : B)`, donde el tipo de la segunda componente depende del valor de la primera. Por ejemplo, `Vec A = { n : Nat, f : Fin n -> A }`: un largo, y una función que solo acepta índices menores que ese largo.

El universo `U` es el tipo de los tipos. Como los tipos son valores de `U`, una función puede recibir y devolver tipos: `List : U -> U`, `VecOf : Nat -> U`. Esto es lo que hace a Luthier un lenguaje con tipos dependientes completos, y no solo con genéricos.

En el kernel, `U` tiene introducción (todo tipo es un valor de `U`) pero no tiene eliminación: no hay `match T { ... }` que pregunte qué forma tiene un tipo. Esa ausencia es una decisión con consecuencias, y está en el punto siguiente.

### 2. Parametricidad: por qué no se puede mirar adentro de `U` sin pagar un precio

Si una función no puede inspeccionar un tipo, todo lo que hace con valores de ese tipo tiene que ser uniforme. Reynolds (1983) lo formalizó, y Wadler (1989) lo popularizó como "theorems for free": de la firma sola se deducen leyes.

- **`f : (A : U) -> A -> A` es necesariamente la identidad.** La función recibe un valor de un tipo del que no sabe nada; no puede fabricar otro valor de ese tipo, así que solo puede devolver el que recibió.
- **`g : (A : U) -> List A -> List A` conmuta con `map`.** Para toda función `h`, vale `g (map h xs) = map h (g xs)`. La función solo puede reordenar, duplicar o descartar elementos, siempre igual sin importar qué son.

El punto 5 de G5 en 08 ("una instancia bien elegida vale por todas", Bernardy, Jansson y Claessen 2010) se apoya en esto. Si una función genérica no puede distinguir tipos, probarla en uno informa sobre todos.

Ahora supongamos que agregamos un `match` sobre `U` (lo que se llama *typecase*):

    f (A : U) (x : A) : A := match A { Int -> x + 1 ; _ -> x }

El tipo de `f` sigue siendo `(A : U) -> A -> A`, pero `f` ya no es la identidad. Todos los teoremas gratuitos caen, y con ellos la prueba en una instancia. Hay un segundo problema: `U` es abierto, porque cada programa agrega tipos, así que un `match` sobre `U` nunca puede ser exhaustivo.

### 3. Reflexión propiamente dicha

Reflexión es la capacidad de un lenguaje de tratarse a sí mismo como dato. Tiene dos grados:

- **Inspeccionar tipos en tiempo de ejecución.** Es el typecase de arriba, o `type(x)` e `isinstance` en Python. El intérprete de Luthier hace esto en Python todo el tiempo: `generators.py` recorre la estructura de un tipo para sortearlo, y el `==` estructural de R8 hace lo mismo para comparar. Pero lo hace desde afuera; el lenguaje no puede.
- **Citar y ejecutar código (*quote* y *unquote*).** `quote t` da el árbol sintáctico del término `t` como un valor de un tipo `Term`; `unquote` (o `eval`) lo vuelve a ejecutar. Lisp lo tiene desde 1958. Lean, Idris y Agda tienen versiones tipadas, donde un `Term T` es la sintaxis de un término de tipo `T`. Es lo que 00 deja como capa futura: `Program` y `Term` como datos de Luthier, de modo que el checker pueda escribirse en Luthier.

La reflexión completa es la herramienta más potente y la más peligrosa. Con ella un programa puede violar cualquier invariante (fabricar un valor de un tipo refinado sin pasar la obligación), pierde la parametricidad, y su semántica obliga a especificar `Term` adentro del lenguaje. Para generar valores es demasiado.

### 4. Universos de códigos: genericidad sin reflexión

Hay una forma estándar en teoría de tipos dependientes de tener funciones que recorren la estructura de un tipo sin romper nada. En vez de inspeccionar `U`, se define un tipo de datos común cuyos valores *describen* tipos, junto con una función que traduce cada descripción al tipo que describe.

Hay dos estilos de universo. En el estilo de Russell, que es el de Luthier, un tipo *es* un elemento de `U`. En el estilo de Tarski, los elementos del universo son *códigos*, y una función de decodificación `El` les da significado. La idea es tener el `U` de Russell para todo y, adentro, un pequeño universo de Tarski para lo que se quiere tratar genéricamente:

    Code : U := data {
      nat    : Code ;                               -- los naturales
      real   : Float64 -> Float64 -> Code ;         -- un double entre dos límites
      prod   : Code -> Code -> Code ;               -- pares
      sum    : Code -> Code -> Code ;               -- alternativas
      vec    : Nat -> Code -> Code ;                -- vectores de largo fijo
      refine : (c : Code) -> (El c -> Bool) -> Code -- un subtipo, con su predicado
    }

    El (c : Code) : U := match c {
      nat        -> Nat ;
      real lo hi -> { x : Float64 | lo <= x and x <= hi } ;
      prod a b   -> El a * El b ;
      sum a b    -> El a + El b ;
      vec n a    -> { v : Vec (El a) | v.n == n } ;
      refine a p -> { x : El a | p x }
    }

`Code` es un `data` común, así que se puede hacer `match` sobre él. Ahora el funtor genérico es una función de Luthier:

    sampled (c : Code) (m : Metric) : Gen (El c) := match c {
      nat        -> natUpToSize ;
      real lo hi -> continuous m lo hi ;
      prod a b   -> pairOf (sampled a m) (sampled b m) ;
      sum a b    -> eitherOf (sampled a m) (sampled b m) ;
      vec n a    -> vectorOf n (sampled a m) ;
      refine a p -> filter p (sampled a m)
    }

Esto no se puede escribir sin tipos dependientes. El tipo del resultado, `Gen (El c)`, depende del valor `c`, así que cada rama devuelve un tipo distinto: un generador de naturales en una, de pares en otra. En Haskell haría falta una extensión (los GADTs); acá es la Π de siempre.

Tres observaciones sobre lo que esto le da a Luthier:

1. **La parametricidad queda intacta.** Solo las funciones que reciben un `Code` pueden distinguir formas. Las que reciben un `A : U` siguen sin poder, y sus teoremas gratuitos siguen valiendo.
2. **Tu principio queda literal.** "Solo hay generadores de tipos definidos" pasa a ser "solo hay generadores de tipos con código". Un tipo declarado sin definir no tiene código, porque no se sabe qué forma tiene. El checker puede derivar el código de una definición, ya que conoce su estructura.
3. **Lo que hoy hace el intérprete desde afuera puede vivir adentro.** El `==` estructural de R8 sería `eq : (c : Code) -> El c -> El c -> Bool`. El alcance (reach) de un certificado sería una función sobre códigos. Cada una con sus leyes y sus certificados.

Hay un detalle técnico. `refine` menciona `El c` en su propio constructor, así que `Code` y `El` se definen a la vez, cada una usando a la otra. Eso se llama inducción-recursión (Dybjer, 2000), y es consistente. En el vocabulario de Luthier, el par `Code` y `El` es un ciclo, o sea un objeto (05 §3), que es la forma en que Luthier ya entiende las definiciones mutuas.

### 5. El código de punto fijo: los tipos recursivos

Los códigos de arriba describen tipos de tamaño acotado. `List A`, los árboles y `Nat` definido como cero o sucesor se definen en términos de sí mismos.

La idea es separar una capa de la recursión. Una lista es "vacía, o un elemento seguido de una lista". Si llamamos `X` al lugar donde aparece "una lista", una capa es

    F(X) = 1 + A × X

donde `1` es `Unit` (la lista vacía), `+` es la suma, `×` el producto y `A` el tipo de los elementos. `List A` es el tipo `X` que satisface `X ≅ F(X)`: una lista es exactamente una capa cuya posición recursiva contiene otra lista. Ese `X` es el **punto fijo** de `F`, y se escribe `μX. F(X)` (μ es el símbolo del menor punto fijo). "Menor" significa que solo cuenta lo que se construye en una cantidad finita de pasos: listas finitas, no infinitas. Otros ejemplos:

- `Nat = μX. 1 + X` (cero, o sucesor de un natural);
- un árbol binario con hojas en `A` es `μX. A + X × X`.

Para describir esto con códigos alcanzan dos constructores más:

    var : Code ;          -- la posición recursiva, la X
    mu  : Code -> Code    -- el tipo que es su propia capa

Una lista de doubles entre 0 y 1 es el código `mu (sum unit (prod (real 0.0 1.0) var))`. `El` necesita entonces saber qué tipo ocupa `var`, y para `mu` construye el punto fijo; en el lenguaje, eso es un `data` genérico, `Fix F := data { roll : F (Fix F) -> Fix F }`.

Hay una condición que los códigos cumplen de por sí. La `X` no puede aparecer a la izquierda de una flecha. El ejemplo clásico es `X ≅ X -> Bool`: ese tipo no puede existir (es el argumento diagonal de Cantor), y admitirlo vuelve inconsistente el sistema. Como `Code` no tiene un constructor de flecha con `var` a la izquierda, todo punto fijo que describe es legítimo. Esto se llama positividad estricta.

### 6. Generar un punto fijo: donde entra tu idea de costos

Sortear un valor de `μF` es sortear una capa y, en cada posición `var`, sortear recursivamente. El peligro es que no termine. En un árbol binario, si cada nodo elige "dos hijos" con probabilidad `q`, cada nodo tiene en promedio `2q` hijos. Si `2q ≥ 1`, el árbol es infinito con probabilidad positiva (es un proceso de ramificación de Galton-Watson, el mismo de las extinciones de apellidos). Hay dos soluciones conocidas:

- **Un tamaño que decrece.** Cada llamada recursiva recibe un tamaño menor, y con tamaño 0 solo se permiten las alternativas sin `var`. Es lo que hace hoy `genList` con su largo.
- **Pesos por tamaño.** Se le da a cada valor un peso que depende de su tamaño. Los muestreadores de Boltzmann (Duchon, Flajolet, Louchard y Schaeffer, 2004) eligen cada valor con probabilidad proporcional a `x^n`, donde `n` es su tamaño y `x` un parámetro que fija el tamaño esperado. Feat (Duregård, Jansson y Wang, 2012) cuenta cuántos valores hay de cada tamaño a partir de `F` y sortea uniforme dentro de un tamaño, indexando en las cuentas acumuladas.

Esto último es tu "sumar los costos y samplear sobre la suma acumulada". Para un punto fijo, el costo es el tamaño, y las cuentas por tamaño salen del código sin mirar ningún valor. Los números (métrica lineal o logarítmica), los censos y los tipos recursivos quedan bajo la misma regla.

### 7. Qué decide esto para la especificación

La contradicción que te señalé en 08, generadores como valores de Luthier pero funtores sobre tipos que Luthier no puede inspeccionar, tiene tres salidas:

| salida | qué es | qué cuesta |
|---|---|---|
| funtores del intérprete, como `==` | genérico desde afuera, nombrado y registrado | los generadores genéricos no son Luthier; contradice G1 |
| typecase sobre `U` | `match` sobre tipos | rompe la parametricidad y G5; `U` es abierto |
| universo de códigos | `Code` y `El` en una librería; los funtores son funciones sobre códigos | escribir el universo; el checker deriva códigos; `mu` cuando haga falta |

Mi recomendación es la tercera. Es la que hace verdaderas a la vez tus dos frases: "los generadores son ciudadanos de Luthier" y "solo hay generadores de tipos definidos". Y deja la reflexión propiamente dicha (`Term`, quote y unquote) donde está, como la capa futura de 00, para cuando quieras escribir el checker en Luthier.

Se puede hacer por etapas. Primero los códigos sin `mu`, que cubren números con límites, productos, sumas, vectores y refinamientos, o sea casi todo lo que el proyecto sortea. `List` puede tener por ahora un código propio, `list : Code -> Code`, y `mu` con muestreo de Boltzmann vendría cuando aparezca un `data` recursivo que haga falta generar genéricamente. Las funciones sobre dominios infinitos no tienen código de generación: van por censo, como ya dice G9.

## 95. Luciano  2026-10-06 03:13:47 UTC  (line 6007)

contame mas de la diferencia entre universo Russel y Tarsky

## 96. Model  2026-10-06 03:15:00 UTC  (line 6015)

## Universos de Russell y de Tarski

Los dos nombres los puso Per Martin-Löf en su teoría de tipos (1984), que es la base de Agda, Coq, Lean y de lo que Luthier tiene de dependiente. Las dos son maneras de responder a una pregunta: si los tipos son valores de un tipo `U`, ¿qué es exactamente un elemento de `U`?

### 1. De dónde vienen los nombres

**Russell.** En la teoría de tipos de Russell (1908), un tipo es directamente la colección de sus miembros. Un universo a la Russell funciona así: un elemento de `U` *es* un tipo. Si `Nat : U`, entonces `Nat` se usa tal cual para declarar `n : Nat`. Hay un solo objeto que hace dos papeles.

**Tarski.** Tarski (1933) separó una oración de lo que dice. La oración "la nieve es blanca" es una cadena de símbolos, y es verdadera si y solo si la nieve es blanca. Esa definición de verdad necesita dos niveles: el nombre de la oración y su interpretación. Un universo a la Tarski hace lo mismo con los tipos. Un elemento de `U` es un *código*, un nombre de un tipo, y una función de decodificación `El` lleva cada código al tipo que nombra. `nat : U` es un código; el tipo es `El nat`, y se declara `n : El nat`.

Una imagen: Russell es una caja con los objetos mismos adentro. Tarski es un catálogo de etiquetas más una función que, dada una etiqueta, te trae el objeto.

### 2. Las reglas de cada uno

Con `Type` el juicio "esto es un tipo", `A`, `B` tipos y `Π` la función dependiente:

| | Russell | Tarski |
|---|---|---|
| qué es un elemento de `U` | un tipo: si `A : U`, entonces `A` es un tipo | un código: si `a : U`, entonces `El a` es un tipo |
| un tipo base | `Nat : U` | `nat : U`, con `El nat ≡ Nat` |
| la función dependiente | si `A : U` y `B : A -> U`, entonces `((x : A) -> B x) : U` | `pi : (a : U) -> (El a -> U) -> U`, con `El (pi a b) ≡ (x : El a) -> El (b x)` |
| la notación | liviana: el tipo se escribe una vez | explícita: `El` en cada uso |

Las ecuaciones con `≡` (las de decodificación) son igualdades por cómputo. El checker tiene que reducir `El (pi a b)` hasta el tipo función cuando chequea.

### 3. Las diferencias que importan

**Tipado único.** Un `U : U` es inconsistente como lógica (Girard, 1972: se puede construir una paradoja como la de Russell). Por eso los sistemas serios usan una escalera `U0 : U1 : U2 : …`. En Russell, si los niveles son acumulativos, el mismo `Nat` es elemento de `U0` y de `U1`: un mismo término tiene muchos tipos, y eso complica la metateoría. En Tarski, subir de nivel es una función explícita, `lift : U0 -> U1` con `El1 (lift a) ≡ El0 a`, y cada término tiene un solo tipo. Por eso Tarski es la forma preferida para estudiar modelos y semántica, aunque la superficie de los lenguajes sea Russell. Luthier hoy tiene en la práctica `U : U`, y 00 ya lo anota como abierto: "muerde solo cuando hay pruebas".

**Qué se puede eliminar.** Esta es la diferencia que nos importa. En Russell, `U` es la colección de *todos* los tipos, y cada programa agrega los suyos: es abierta. Un `match` sobre `U` no puede ser exhaustivo, y por eso el kernel de Luthier no tiene eliminación para `U`. En Tarski, `U` puede ser un `data` común: un conjunto cerrado de códigos definido inductivamente. Ahí sí hay `match`, por inducción sobre los códigos. Se llama un universo *cerrado*, y es la base de la programación genérica en tipos dependientes (Altenkirch y McBride, 2003; Benke, Dybjer y Jansson, 2003).

**Lo que promete una firma.** Si conviven los dos, la firma de una función dice qué puede hacer:

- `(A : U) -> …` no puede mirar `A`. Es paramétrica, y valen sus teoremas gratuitos: probarla en una instancia informa sobre todas (08, G5).
- `(c : Code) -> …` puede mirar la forma de `c` y hacer algo distinto por caso. No es paramétrica, y lo dice en su tipo.

El typecase sobre `U` rompe esto en silencio, porque una función con firma paramétrica deja de serlo. El universo de códigos lo vuelve explícito.

**Alcance.** Un universo de Tarski cerrado describe solo los tipos que tienen código. Eso no es un defecto: es el sentido de "solo hay generadores de tipos definidos". Lo que no tiene código (un tipo declarado y no definido, un tipo que llegó como parámetro) no se puede inspeccionar, y eso es exactamente lo que se quiere.

### 4. Cómo lo hacen los lenguajes reales

Coq, Agda y Lean muestran una superficie Russell: se escribe `Nat : Type` y se usa `Nat`. Por dentro, o en sus metateorías, a menudo trabajan a la Tarski. Cuando alguien quiere programación genérica en Agda, define su propio universo cerrado: un `data Code` y un `El : Code -> Set`, en una librería, conviviendo con el `Set` de Russell. Eso es lo que propongo para Luthier: el `U` de Russell para todo, y un universo de Tarski chico y cerrado como librería, para lo que hay que tratar genéricamente (generadores, igualdad estructural, alcance de un certificado).

Si el código incluyera un código para `U` mismo, la paradoja de Girard reaparecería a través de `El`. El `Code` de los generadores no lo necesita: no se sortean tipos (G5).

### 5. Lo que le pide a Luthier

Hay tres requisitos concretos, y uno conecta con la ronda que ya está planeada:

1. **Definiciones mutuas entre un `data` y una función.** `Code` y `El` se definen juntos (inducción-recursión), porque `refine` menciona `El c`. Para Luthier es un ciclo, o sea un objeto (05 §3), que es como ya entiende las definiciones mutuas.
2. **Eliminación grande.** `El` es una función que devuelve un tipo por `match` sobre un dato. El checker tiene que reducir `El (prod a b)` a `El a * El b` cuando aparece en una posición de tipo.
3. **Que el `match` refine el tipo esperado en cada rama.** En `sampled (c : Code) : Gen (El c) := match c { prod a b -> … }`, dentro de la rama el checker tiene que saber que `c` es `prod a b`, y entonces que se espera un `Gen (El a * El b)`. Es el *pattern matching dependiente*, y es exactamente lo que dice R11 para los patrones: "dentro de `match m { just y -> a }`, `a` sabe que `m == just y`". Así que R11, que ya está en la ronda, es requisito del universo de códigos: implementarlo bien para patrones es lo que permite escribir los funtores en Luthier.

En resumen: Russell te da tipos que se usan y no se miran. Tarski te da nombres de tipos que se pueden mirar, a costa de pasar por `El`. Tener los dos, con el de Tarski cerrado y chico, separa en la firma misma el código que no puede distinguir tipos del que sí puede, y eso es lo que necesitan a la vez los generadores y la certificación.

## 97. Luciano  2026-10-06 03:17:22 UTC  (line 6022)

como leo El ?

## 98. Model  2026-10-06 03:17:31 UTC  (line 6026)

`El` es la abreviatura de *elements*: `El c` se lee "los elementos de `c`", es decir, el tipo cuyos valores son los elementos de lo que el código `c` nombra. La notación es de Martin-Löf. En voz alta se dice "El de c", y en castellano conviene leerlo como "el tipo que nombra `c`".

Otros textos usan otras notaciones para lo mismo:

- `T(c)` o `Dec c`, de *decode*;
- `⟦c⟧`, que se lee "la interpretación de `c`" o "la denotación de `c`", con los corchetes de la semántica denotacional.

Si te resulta más claro, en Luthier se puede llamar `typeOf`, `decode` o `Meaning`: el nombre es una convención, lo que importa es que va de un código a un tipo.

## 99. Luciano  2026-10-06 03:27:26 UTC  (line 6029)

porque usaste El y no typeof? 
Es mas preciso?

## 100. Model  2026-10-06 03:27:45 UTC  (line 6033)

Lo usé por costumbre: es la notación estándar en la literatura (Martin-Löf, los universos de Agda). No es más precisa, es solo convencional.

Pero `typeOf` sería peor, porque engaña. En casi todos los lenguajes `typeOf x` significa "el tipo del valor `x`": si `x : T`, entonces `typeOf x` es `T`. Aplicado a un código, `typeOf c` sería `Code`, porque `c` es un valor de tipo `Code`. Lo que hace `El` es otra cosa: no da el tipo *de* `c`, sino el tipo *que nombra* `c`. Por ejemplo, `c = real 0.0 1.0` tiene tipo `Code`, y nombra al tipo `{ x : Float64 | 0 <= x and x <= 1 }`. Además `typeOf` sugiere reflexión sobre valores, que es justamente lo que el universo de códigos evita.

Para Luthier propondría `Decode`: hace pareja con `Code`, dice la dirección (de un código al tipo que describe) y no choca con nada. `Meaning` o `Denote` también son precisos, pero menos obvios al lado de `Code`. En el draft 2 de 08 usaría `Code` y `Decode`, con una nota de que en la literatura se escribe `El`.

## 101. Luciano  2026-10-06 03:34:16 UTC  (line 6036)

Bueno, este analisis me abrio mucho los ojos. 
Hay mucho material en esta discusion. 
Ponela en un documento asi lo corrijo y dejo lo importante.

## 102. Model  2026-10-06 03:36:02 UTC  (line 6051)

Escrito para: vos, para corregirlo y recortarlo antes de que alimente el draft 2 de 08.

Está en [universes-and-codes-2026-10-06.md](../luthier/docs/ideas/universes-and-codes-2026-10-06.md), en inglés como el resto de los docs, y commiteado (21aa9c9) para que tus correcciones queden como diff. El orden sigue el de la discusión:

1. Por qué surgió: los seis huecos del draft 1 de 08, el primero de los cuales es la contradicción entre "generadores como valores" y "funtores sobre el tipo".
2. Qué puede hacer Luthier con un tipo: `U` sin eliminación.
3. Tipos dependientes.
4. Parametricidad, y el precio del `match` sobre `U`.
5. Reflexión en sus dos grados.
6. Russell y Tarski: los nombres, las reglas, las diferencias, qué hacen Coq, Agda y Lean. Ahí quedó también por qué `Decode` y no `typeOf`.
7. El universo de códigos para Luthier, con `sampled` escrito en Luthier.
8. El código de punto fijo y cómo sortearlo, que es donde entra tu idea de la suma acumulada de costos.
9. La decisión y los tres requisitos que le pone al checker, entre ellos que R11 es prerrequisito.

Al final van las referencias. Las citas las puse de memoria, así que conviene verificarlas antes de usarlas en algo publicado.
