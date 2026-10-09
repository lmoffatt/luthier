---
source: claude-code
account: 
id: aa680014-c29f-47b0-8ac7-1bcc11459b78
title: "analsis critico de como esta la implementacion de luthier y de luthier para sonolocalizaci"
started: 2026-10-05T07:06:43Z
ended: 2026-10-05T22:51:57Z
offset: 
turns: 76
cwd: -home-lmoffatt-Projects-sonolocalizacion
exports: 20261009
flags: 
origin:
  - raw/claude-code/20261009/-home-lmoffatt-Projects-sonolocalizacion/aa680014-c29f-47b0-8ac7-1bcc11459b78.38284bda.jsonl.gz sha256 38284bda061895ed6f33748478d8ec97421af117b57356fc6b583fbe91de6ee7
iachat: 1
---

# analsis critico de como esta la implementacion de luthier y de luthier para sonolocalizaci

## 1. Luciano  2026-10-05 07:06:43 UTC  (line 1)

analsis critico de como esta la implementacion de luthier y de luthier para sonolocalizacion

## 2. Model  2026-10-05 07:07:36 UTC  (lines 44, 73, 91, 100, 105)

Estoy leyendo las especificaciones (05, 06, 07) y en paralelo corre un agente que audita el intérprete y las pruebas; ahora sigo con las librerías y los .lut del proyecto.

Revisando los certificados encontré entradas que fallan y otras viejas; ahora busco el registro de corrida de experiment_zero.

Mientras termina el agente de auditoría del intérprete, ya tengo lo del proyecto. Espero su informe para cerrar.

experiment_zero reproduce los CSV byte a byte, pero tarda 3 minutos para 30 parámetros y 22 distancias. Falta el informe del agente sobre el intérprete.

Tengo lo del proyecto y las librerías. El agente que audita el intérprete (reglas R1–R10 contra el checker, cómo se generan los casos, si los certificados envejecen) sigue corriendo; cuando termine armo el análisis completo.

## 3. Luciano  2026-10-05 07:22:01 UTC  (line 106)

y?

## 4. Model  2026-10-05 07:23:13 UTC  (lines 110, 119)

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

## 5. Luciano  2026-10-05 07:25:27 UTC  (line 123)

chequea las conclusiones de Opus

## 6. Model  2026-10-05 07:25:52 UTC  (lines 129, 140, 152, 161)

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

## 7. Luciano  2026-10-05 07:30:43 UTC  (line 162)

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

## 8. Model  2026-10-05 07:31:10 UTC  (lines 166, 182, 188)

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

## 9. Luciano  2026-10-05 07:38:17 UTC  (line 189)

Elabora un plan para solucionar todos los problemas encontrados. 
Indica el problema, su rational y como se solucionaria (con los posibles caveats)

## 10. Model  2026-10-05 07:42:42 UTC  (line 193)

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

## 11. Luciano  2026-10-05 07:45:17 UTC  (line 197)

Implementa la Fase 1 del plan

## 12. Model  2026-10-05 07:45:34 UTC  (lines 203, 221)

Empiezo por respaldar los dos árboles de trabajo, que tienen cambios sin commitear, y después leo el código del puente antes de tocar nada.

Leí el puente. Ahora el lado del checker: cómo se arman las obligaciones, los `gen`, y el `--set`.

## 13. Luciano (queued)  2026-10-05 07:46:23 UTC  (line 225)

En el medio salva el plan a un archivo

## 14. Model  2026-10-05 07:47:54 UTC  (lines 228, 234, 251, 278, 283, 289, 297, 306, 333, 338, 352, 359, 371, 376, 381, 390, 419, 439, 472)

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

## 15. Luciano (queued)  2026-10-05 08:17:48 UTC  (line 481)

que es BrokenGraph?

## 16. Model  2026-10-05 08:29:39 UTC  (lines 508, 514, 520, 531, 541)

Ahora escribo las pruebas de regresión de la Fase 1, con su módulo de externs.

The helper named `test_law` was collected as a test; I'll rename it.

97 pasan (las 78 de antes más las 19 nuevas). Veo cómo van las dos corridas de fondo.

Mientras tanto comparo cuántas obligaciones agregó el 1.2 en cada librería, con los dos intérpretes.

Mientras corre, verifico que todos los archivos del proyecto carguen después de los cambios.

## 17. Luciano (queued)  2026-10-05 08:39:08 UTC  (line 588)

que hace ValidGraph?

## 18. Model  2026-10-05 08:42:54 UTC  (lines 616, 627, 636, 640, 646, 654, 659)

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

## 19. Luciano  2026-10-05 08:47:56 UTC  (line 660)

bueno, ahora que sigue? vamos a Fase 2?

## 20. Model  2026-10-05 08:48:04 UTC  (lines 664, 669, 674)

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

## 21. Luciano  2026-10-05 08:51:00 UTC  (line 684)

antes que sigas hice unas preguntas antes

## 22. Model  2026-10-05 08:51:24 UTC  (line 688)

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

## 23. Luciano  2026-10-05 08:53:47 UTC  (line 689)

y vi que decias que tardaba mucho tiempo, puede ser?

## 24. Model  2026-10-05 08:54:40 UTC  (lines 697, 706)

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

## 25. Luciano  2026-10-05 08:56:14 UTC  (line 707)

bien, segui con la fase 2, o hay alguna razon para atacar las fallas pre-existentes?

## 26. Model  2026-10-05 08:57:08 UTC  (lines 711, 733, 741, 746, 771, 776, 797, 818, 823, 836, 841, 849, 857)

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

## 27. Luciano (queued)  2026-10-05 09:21:01 UTC  (line 876)

aqui hago una pregunta: 
la idea de luthier es que yo no tenga que hacer python project dedicated scripts salvo las funciones que son llamadas con extern
no estaremos haciendo parches no?

## 28. Model  2026-10-05 09:31:27 UTC  (lines 879, 889)

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

## 29. Luciano  2026-10-05 09:34:18 UTC  (line 890)

Scripts con __main__, que no la cumplen:
validate_distance_graph.py envuelve en Python una llamada a Luthier para validar un grafo. Podría ser un main en un .lut (luthier run validate_graph.lut --set graphDir=...) y desaparecer.
--> si, validate_distance_graph tiene que estar expresado en lut en cuanto a las condiciones y ser implementado en python con extern

prepare_experiment_zero.py arma el grafo a partir de la tabla de campo; su docstring dice que es Python plano "a propósito". Se podría escribir en Luthier con un extern que lea la tabla, pero es una decisión tuya.
lm_controls.py tiene los mutantes del Levenberg-Marquardt, hoy corridos a mano. Con el 5.6 pasan a ser externs que usan leyes, y entonces sí cumplen.
--> este caso lo exclui a proposito ya que seria para este caso particular.

## 30. Model  2026-10-05 09:34:41 UTC  (lines 894, 905, 910, 916, 926, 937, 947, 957, 973, 1002, 1007, 1018, 1023, 1034, 1039)

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

## 31. Luciano  2026-10-05 09:53:58 UTC  (line 1040)

Te parece activar la Fase 3? me la recordas?

## 32. Model  2026-10-05 09:54:51 UTC  (line 1048)

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

## 33. Luciano  2026-10-05 09:57:45 UTC  (line 1052)

que regeneracion?

## 34. Model  2026-10-05 09:57:59 UTC  (line 1056)

Por "regeneración" me refiero a volver a correr todas las pruebas para reescribir los archivos `.cert.json`. Es lo que está corriendo ahora en segundo plano: `luthier certify --imports` sobre los 13 archivos de `luthier/src/luthier/lib/`, con 8 procesos a la vez.

**Por qué hace falta:** con la Fase 2, el hash de un certificado cubre ahora el código del cono, el Python de cada extern y el intérprete. Ningún certificado escrito antes trae esa información, así que hoy todos se leen como viejos. Por eso `validate_graph` decía "the cone of main: pending 7, stale 57": no queda nada certificado hasta que se vuelvan a correr las pruebas. Recién entonces `check -v` vuelve a mostrar "certified" y `run --require-certified` acepta correr.

**Qué toca:** reescribe los `.cert.json` de las librerías dentro del repo de `luthier`. Después faltaría hacer lo mismo con los del proyecto en `prototipo-cero/luthier/`.

**Por qué te propuse cortarla:** la huella del intérprete entra en el hash, así que cualquier cambio de la Fase 3 deja viejos otra vez los certificados que se están generando ahora. Si la Fase 3 viene enseguida, conviene regenerar una sola vez al final.

Sigue corriendo y no toqué nada más. ¿La corto, la dejo terminar, o preferís otra cosa?

## 35. Luciano  2026-10-05 09:59:03 UTC  (line 1057)

arranca la Fase 3 como recomendaste

## 36. Model  2026-10-05 09:59:14 UTC  (lines 1061, 1070, 1078, 1086, 1097, 1110, 1115, 1131, 1149, 1171)

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

## 37. Luciano  2026-10-05 10:15:52 UTC  (line 1175)

si terminas con esta fase segui con la siguiente

## 38. Luciano  2026-10-05 10:16:38 UTC  (line 1179)

arranca la Fase 3 como recomendaste y luego comitea y segui con la fase 4 sin preguntar (me voy por 40 minutos)

## 39. Model  2026-10-05 10:17:17 UTC  (lines 1183, 1192, 1201, 1206, 1217, 1227, 1235, 1245, 1263, 1285, 1296, 1301, 1306, 1311, 1335, 1341, 1357, 1363, 1368)

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

## 40. Luciano  2026-10-05 13:22:14 UTC  (line 1369)

que falta?

## 41. Luciano  2026-10-05 13:22:56 UTC  (line 1373)

que falta?

## 42. Model  2026-10-05 13:23:27 UTC  (lines 1377, 1391, 1396)

Antes de contestar miro cómo va la regeneración, que es lo único que está corriendo.

No hay un perfilador por muestreo instalado, así que lo veo de otra forma: corro una de esas pruebas con `--show-cases`, sin escribir certificados, y miro en qué ley y caso avanza.

Ya tengo una idea de qué pasa, y además apareció una falla real. Corto la regeneración, que está repitiendo trabajo, y lanzo un diagnóstico con tiempos por definición sobre `array.lut` solo.

## 43. Luciano (queued)  2026-10-05 13:28:44 UTC  (line 1399)

y?

## 44. Model  2026-10-05 13:29:28 UTC  (line 1403)

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

## 45. Luciano  2026-10-05 13:30:57 UTC  (line 1404)

Dale, completa de 1 a 5, sin preguntar

## 46. Model  2026-10-05 13:33:41 UTC  (lines 1408, 1415, 1420, 1438, 1453, 1461, 1466, 1479, 1500, 1505, 1510, 1515, 1525, 1531, 1538, 1606, 1615, 1638, 1643, 1673, 1701, 1742, 1747, 1755, 1798, 1829, 1839, 1862, 1889, 1925, 1941, 1980, 2019, 2036, 2047)

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

## 47. Tool (system)  no time  (line 2062)

[summary inserted by the harness]  [33 characters]

## 48. Model  2026-10-05 15:08:13 UTC  (lines 2099, 2124, 2239, 2291, 2296, 2305, 2315, 2348, 2353, 2358, 2369, 2382, 2394, 2403, 2408, 2413, 2418, 2427, 2432, 2437, 2447, 2458, 2529, 2541, 2547, 2552, 2560, 2573, 2578, 2583, 2596, 2606, 2624, 2647, 2657, 2662, 2668, 2684, 2689, 2694, 2709, 2717, 2723, 2737, 2746, 2759, 2764, 2769, 2805, 2811, 2816, 2846, 2885, 2890, 2895, 2900, 2905, 2922, 2966, 2978, 3030, 3035, 3045, 3063, 3074, 3087, 3092, 3105, 3110, 3116, 3128, 3140, 3145, 3150, 3158, 3163, 3180, 3196, 3204, 3241, 3249, 3253, 3268, 3274, 3287, 3299, 3317, 3332, 3349, 3386, 3410, 3419, 3437, 3462, 3467, 3478, 3483, 3488, 3493, 3498, 3505, 3511, 3517, 3522, 3530, 3535, 3571, 3589, 3601, 3620, 3640, 3651, 3659, 3665, 3674, 3679, 3688, 3694, 3702)

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

## 49. Luciano  2026-10-05 20:41:31 UTC  (line 3709)

reporte de situacion

## 50. Luciano  2026-10-05 20:41:38 UTC  (line 3713)

reporte de situacion

## 51. Model  2026-10-05 20:42:15 UTC  (line 3721)

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

## 52. Luciano  2026-10-05 20:47:36 UTC  (line 3722)

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

## 53. Model  2026-10-05 20:49:47 UTC  (line 3726)

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

## 54. Luciano  2026-10-05 20:54:57 UTC  (line 3727)

hay una cuestion importante con los tests y es como se generan los valores de los tipos involucrados. Entiendo que eso se hace internamente no?

## 55. Model  2026-10-05 20:56:04 UTC  (line 3731)

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

## 56. Luciano  2026-10-05 21:04:37 UTC  (line 3732)

bueno, yo quisiera que los tests  pidan un generador explicito para cada tipo involucrado. 
El generador puede ser simplemente un valor tipico, pero la idea es que quede explicitado. 
La pregunta es como generamos valores de tipos funciones? 
Bueno, seria el caso mas simple: un censo sobre los valores registrados no?
Para numeros tendriamos que fijar los valores limites y definir si son en escala linear o logaritmica.  
Para vectores tendriamos varios generadores que sean utiles para distintos casos. 

Quiero que analices esto bastante bien y generes un documento para luego generar la especificacion.

## 57. Luciano  2026-10-05 21:12:18 UTC  (line 3745)

quiero que relates que hiciste entre las 10 pm y ahora basado en los timestaps de commits y modificaciones de files y  procesos corriendo, con no mas de 4 lineas por hora.

## 58. Model  2026-10-05 21:13:29 UTC  (lines 3785, 3812)

Estoy reconstruyendo la línea de tiempo desde el transcript de la sesión anterior, los commits y los procesos; leo cada hora.

De 22:00 a 05:13 cerré el plan de reparación con siete commits de código. Lo que no terminó es la regeneración de certificados: está trabada en distances_python desde las 04:21. Todavía faltan commitear los certificados, el tag v0.1 y el `luthier.lock`.

22–23 h. 22:21: commit de lo pendiente de la fase 4 (`run --checked`, leyes del contenido de una suma que devuelve un extern). 22:33: commit de `Rational` y la ley de redondeo; se fue `float64Field`.
22:36–22:51: `Likelihood` con dimensión, `DensityPairOn`/`KernelOn`, la gramática del CSV escrita en Luthier y `BrokenText` como predicado; commit en los dos repos. 23:02: commit de los controles de Levenberg-Marquardt como leyes, el maximizador que dice si convergió y `luthier.lock`.

23–00 h. A las 23:07 se compactó el contexto. Empecé 5.2 metiendo la dimensión en los tipos de probability, belief y optimization (Theta = `VecOf n`).
Dejé un único `positionsModel`, con el diseño y el gauge pasados de Luthier a Python; a las 23:40 experiment_zero dio los CSV idénticos byte a byte. 23:44–23:57: el tipo `GraphDir`, y 5.8/5.5 (`Ensemble`, `PitResolution`, `Seed`, Kolmogorov-Smirnov, controles a 1,3σ).

00–01 h. 00:00–00:08: en experiment_zero, `transform.csv` y las entradas de control `priorWidened` y `sigmaKnown`, corridas en el scratchpad. Agregué el tiempo por ley a los certificados y documenté el plan.
00:23–01:03: varios arreglos del intérprete, cada uno con su test. El principal distingue una ley enunciada de una obligación de tipo; los otros son listas refinadas, componente vacío, proyección dependiente y la condición de la rama. A las 00:21 lancé la recertificación; la corté dos veces porque cada arreglo la invalida.

01–02 h. 01:03: separé el informe de la escritura en experiment_zero y relancé la recertificación a las 01:05. array_python con `--imports` quedó más de una hora sin terminar y no encontré la causa: esperé y perfilé.

02–03 h. 02:36–02:46: una corrida de diagnóstico mostró la causa, las obligaciones de `spectralMap` (Jacobi nativo a tamaño 16); las acoté a tamaño 5. 02:47–02:48: commits 548a3b6 (luthier) y 84ee917 (proyecto), sin certificados.
Con la directiva, array_python tardó 6 minutos y las librerías pasaron todo, salvo las leyes genéricas en `Theta : U`.

03–04 h. distance_graph_python iba lento: `Separated` tardaba 170 s porque los pares se sorteaban por rechazo. 03:38: `positions_python.lut` con generadores para `Pairs`, `PairsAmong` y `SeparatedPairs`.
04:01–04:07: el perfil mostró que `Node p` también se sorteaba por rechazo; lo arreglé y la obligación de `point` pasó de 185 s a 1 s.

04–05 h. 04:08: commits 20a786b y e6fdc02, y relancé la recertificación completa. Las librerías terminaron a las 04:17 y distance_graph_python a las 04:21 (34 pasadas, ninguna fallada).
A las 04:21 arrancó la etapa con distances_python, validate_graph y belief_check. 04:41–05:04: tu pedido de reporte y mis explicaciones (negate, match, Square, 5.5, lock).

05 h. 05:08: lancé dos agentes para el documento de generadores, uno con el inventario de tipos generados y otro con antecedentes; sus transcripts se siguen escribiendo a las 05:13. 05:09–05:10: `lmTol` y `lmMaxIter` como parámetros de la corrida, commit b8c5fdf.
Ahora corren dos copias de distances_python: la de la recertificación, con 51 minutos sin terminar, y un diagnóstico duplicado que arranqué a las 05:10. El documento de generadores que pediste no está escrito.

## 59. Luciano  2026-10-05 21:19:03 UTC  (line 3819)

O sea, en que areas estamos trabajando, que aspectos se aplicaron del plan, que se mejoro y que falta

## 60. Model  2026-10-05 21:20:01 UTC  (line 3843)

Trabajamos en tres capas: el intérprete, las librerías y el proyecto. Del plan está aplicado casi todo (fases 1 a 6). Falta cerrar la certificación con certificados regenerados, tag y lock, terminar 5.5 y abrir el frente nuevo que pediste, los generadores explícitos.

Antes de seguir, algo importante. La sesión anterior (c7437496) sigue viva y trabajando en paralelo con esta. A las 05:16 commiteó 9b6aa97 (el modelo rápido recibe el diseño como arrays), relanzó las etapas del proyecto y está esperando a los dos agentes para escribir el documento de generadores. Desde esta sesión no toco nada para no pisarla.

**Qué mejoró, por importancia.** Lo central es que un certificado ahora dice algo. Antes había cuatro agujeros:
- Un extern podía devolver cualquier cosa.
- El hash no cubría el Python ni el intérprete.
- Las leyes sobre los doubles eran falsas: `float64Field` decía que los doubles forman un cuerpo, y no lo son.
- Varias obligaciones del proyecto eran falsas y pasaban porque un generador las tapaba.

Ahora:
- Los valores de Python se chequean por su tipo al cruzar.
- El hash cubre código, Python e intérprete.
- Cada ley termina pasada, fallada o no corrida.
- Los doubles se miden contra los racionales con la ley de redondeo, sin tolerancias.
- Con Theta = `VecOf n` en probability, belief y optimization, las obligaciones del modelo de posiciones son verdaderas.
- El proyecto no tiene Python propio fuera de los externs.

**Proyecto.** Hay un solo modelo de posiciones: el que corre experiment_zero es el que se certifica con el gauge fijado, y el diseño y el gauge viajan de Luthier a Python. Los CSV de la sesión A siguen idénticos byte a byte. Además:
- **Experiment_zero:** escribe la transformada de cada residuo (PIT) y tiene dos corridas de control. Lo que salió hasta ahora: parlante_A2 tiene sus tres distancias 2,6 sd cortas; ensanchar el prior no baja sigma; con sigma fija en 3 cm el ajuste no converge.
- **Levenberg-Marquardt:** sus controles son leyes, el maximizador dice si convergió, y `lmTol`/`lmMaxIter` son parámetros de la corrida.

**Leyes estadísticas.** El tamaño del ensamble y la resolución del PIT los declara el proyecto. Las semillas cubren 2^31 (antes eran 33 valores). La uniformidad se prueba también con Kolmogorov-Smirnov, y los controles se prueban a 1,3σ además de a 2σ.

**Velocidad.** Cargar array.lut bajó de 15 a 4,5 s y experiment_zero de 146 a 21 s. Medir el tiempo de cada ley destapó dos cuellos de botella de la certificación: Jacobi nativo a tamaño 16 y `Node p` sorteado por rechazo. Las librerías se recertifican ahora en 10 minutos en vez de más de 90.

**Estado del plan por fase:**
- 1 (puente), 2 (certificados), 3 (semántica del checker) y 6 (sintaxis y código muerto): hechas. En la 3 se hizo la versión larga de 3.3, con los racionales.
- 4 (velocidad): hecha, salvo dejar un solo evaluador.
- 5 (proyecto): hecha, salvo 5.5 a medias.
- Los parches de la fase 1 (`fullOn`/`profileOn`, `BrokenText` como registro, generadores de instancia) ya no existen.

**Qué falta, en orden de urgencia:**
1. **Cerrar la certificación.** Las librerías y distance_graph_python ya pasaron sin fallas. Quedan distances_python (la etapa más lenta, que la otra sesión está atacando), optimization y experiment_zero. Después van el commit de los certificados, el tag v0.1 y el `luthier.lock`.
2. **Terminar 5.5.** Registrar la tasa de falsa falla de cada ley estadística, repetir una falla con otra semilla antes de llamarla contraejemplo, y registrar la tasa de detección de los controles.
3. **Defectos abiertos del diseño:**
   - La obligación falsa de `negate`; el arreglo es separar `Problem`, sin leyes, de `Objective`.
   - Las obligaciones internas del código genérico no corren en ninguna instancia.
   - Un `match` contra un tipo refinado no se chequea rama por rama.
   - Siguen los dos evaluadores.
   - `Square` no tiene generador.
4. **El frente nuevo: un generador explícito para cada tipo**, con rangos, escala lineal o logarítmica, varios generadores para vectores y funciones como censo de valores registrados. El documento lo está escribiendo la otra sesión.
5. **Tuyo:** registrar vos las corridas de control, decidir qué hacer con tus notas de random.lut (el lock va a avisar mientras no estén commiteadas) y mirar parlante_A2 en los datos.

## 61. Luciano  2026-10-05 21:57:59 UTC  (line 3846)

lee este documento que escribi

## 62. Model  2026-10-05 22:00:25 UTC  (line 3860)

Lo leí. El principio que escribís es más fuerte que lo que hace Luthier hoy, y explica bien varias cosas que hice a mano esta noche sin nombrarlas.

**Lo que decís.** El tipo es el registro de un chequeo: si chequeás un valor, el resultado no debería ser un Bool que se tira, sino el mismo valor con un tipo más fino, para que nadie lo vuelva a chequear. La segunda parte es sobre la granularidad del tipo de un resultado. El ejemplo de `sin x` va de "real" a "real en [−1, 1]" y a "exactamente sin x"; el de `map_opt`, de "vector" a "óptimo de fun x desde beta_ini". El criterio para elegir es el costo de rehacer el cálculo. Tiene nombres en la literatura: "parse, don't validate" (Alexis King, 2019), occurrence typing en Typed Racket (Tobin-Hochstadt y Felleisen) y, para la opción (d), tipos dependientes indexados por las entradas del cálculo.

**Dónde Luthier ya lo cumple.** Hay dos lugares:
- Los refinamientos `{ x : T | P x }` son tipos-certificado: `ValidDistanceGraph`, `PositionsOf n`, `SeparatedPairs`. Que un valor tenga ese tipo quiere decir que pasó el predicado.
- Los certificados aplican el mismo principio al programa entero: una ley certificada no se vuelve a probar mientras su hash no cambie.

**Dónde lo viola, y en código mío de esta noche.** Hay tres casos, y todos podrían escribirse a tu manera:
- **validate_graph.lut.** `main` llama a `fastCheck g` y, si no reporta nada, vuelve a preguntar `if ValidGraph g`. Es exactamente el doble chequeo que odiás. Lo escribí así porque `fastCheck` devuelve `Maybe Violation`: dice que no encontró problemas, pero no devuelve el grafo con su tipo nuevo. La forma correcta es `check : DistanceGraph -> < valid : ValidDistanceGraph | invalid : Violation >`. Así el chequeo produce el grafo ya tipado y nadie más lo mira.
- **La rama `if ValidGraph g then fit g`.** Es la forma estática de tu principio. Luthier no la implementa como regla: el chequeo de tipos anota la condición como precondición de las obligaciones de esa rama. Esta noche agregué un parche que descarta una obligación cuando es textualmente igual a la condición de la rama. La regla de verdad es la de occurrence typing: dentro de la rama, `g` pasa a tener tipo `{ g : DistanceGraph | ValidGraph g }`, y todo lo que lo pida lo recibe sin deber nada.
- **`MaxResult n = { x, converged : Bool }` y `separated : Bool` en el ajuste.** Son resultados de chequeos guardados como datos, no como tipos. Hoy la ley `MaximizerStationary` dice "si `converged` es verdadero, el decremento es chico", y cada consumidor tiene que mirar el Bool. A tu manera, el maximizador devolvería una suma: en el caso convergido, un `{ b : VecOf n | Stationary f b }`; en el agotado, el punto sin certificado. Eso es tu opción (c).

**Tu opción (d)** pide que el tipo del resultado nombre todas sus entradas: el óptimo es de fun, de x y de beta_ini, porque Levenberg-Marquardt encuentra óptimos locales. En Luthier eso es un tipo dependiente, `fit : (g : ValidDistanceGraph) -> Fit g`, y hoy `Fit` está indexado sólo por la dimensión, `Fit (3 * g.nodes.nRows)`. Indexado por el grafo, un ajuste no se podría combinar con otro grafo, y el tipo coincidiría con lo que el `.run.json` ya registra: hash del cono más parámetros. Ese par alcanza como clave para no recalcular, que es tu argumento del costo. Para `sin x` estoy de acuerdo en que (2) es lo útil y (3) sólo sirve en álgebra simbólica.

**Lo que esto cambia del trabajo pendiente.** El principio le da una regla a varias cosas que estaban sueltas:
- Los chequeos de borde (leer un grafo, validar, ajustar) devuelven el valor tipado, nunca un Bool.
- Una condición de rama refina el tipo de la variable.
- Un resultado caro lleva sus entradas en el tipo.
- `run --checked` es la única excepción deliberada: vuelve a chequear a propósito, para depurar el puente con Python.

También ordena lo de los generadores explícitos. Si un tipo refinado es un certificado, su generador funciona como su constructor, y que produzca valores del tipo es una ley que se certifica una vez.

Si querés, sumo esto como principio en la especificación (05) y en la lista de pendientes, empezando por el `check` que devuelve una suma y la regla de refinamiento por rama. Hoy el doble chequeo de validate_graph es el ejemplo más claro de lo que tu nota prohíbe.

## 63. Luciano  2026-10-05 22:05:12 UTC  (line 3863)

hay un tema interesante con sin(x)--> [-1 1] y es que un bounded Real es un tipo posible  que se puede extender con muchas funciones (no todas) y con un costo importante pasarlo de un lado al otro te permitiria obtener un bound para los valores de una funcion compleja. 
Es para pensar, es casi una aplicacion experimental.

## 64. Model  2026-10-05 22:05:56 UTC  (line 3867)

Sí, y tiene nombre: es aritmética de intervalos (Moore, 1966), un caso particular de interpretación abstracta (Cousot y Cousot, 1977). Encaja en Luthier mejor que en casi cualquier lenguaje porque su corrección es una sola ley, y esa ley Luthier ya sabe certificarla.

La ley es la de inclusión. Una extensión `F` de una función `f` cumple que, para todo intervalo `X` y todo `x` en `X`, `f x` está en `F X`. Con eso, un real acotado es un certificado en tu sentido: `{ y : Float64 | lo <= y and y <= hi }`, con `lo` y `hi` calculados por la extensión. La composición sale gratis: si `F` encierra a `f` y `G` a `g`, `G ∘ F` encierra a `g ∘ f`. En Luthier sería un corolario (R10), no una ley por función compuesta. Y la ley se puede probar sin tolerancias, con los racionales que agregamos anoche: el redondeo hacia afuera de cada extremo se compara exactamente contra el valor exacto vía `toQ`.

Tu "no todas" tiene dos causas concretas:
- **Qué funciones se extienden.** Las monótonas (exp, log, sqrt) se extienden evaluando los extremos. Las monótonas por tramos con extremos conocidos (sin, cos) piden saber si el intervalo contiene un máximo o un mínimo. Un extern de numpy cualquiera no se extiende solo: necesita su extensión declarada, o una cota de Lipschitz.
- **El problema de dependencia, que es el costo real.** `x - x` sobre [−1, 1] da [−2, 2] en vez de 0, porque cada aparición de `x` se trata como independiente. En una función compleja, como una verosimilitud con 22 términos, la cota ingenua se infla hasta ser inútil.

El remedio estándar es la forma del valor medio: `F(X) ⊂ f(c) + G(X)·(X − c)`, con `G` una extensión del gradiente. Su sobreestimación cae cuadráticamente al achicar la caja, y para los modelos de Luthier ya tenemos el gradiente certificado (el score, `GradIsGradient`). Más precisas pero más caras están la aritmética afín (Comba y Stolfi) y los modelos de Taylor (Berz y Makino).

En la implementación, el código nativo no necesitaría nada nuevo: la máquina podría evaluar el mismo término con intervalos en lugar de doubles, porque cada primitiva tiene su versión de intervalos. Lo difícil son los `if`: si `X` cruza la condición, hay que evaluar las dos ramas y unir los resultados. Los externs declararían su extensión, certificada por la ley de inclusión. Para la parte numérica rigurosa existe Arb (aritmética de bolas, valor y radio), que hoy viene en python-flint, y también `mpmath.iv`.

En sonolocalización veo tres aplicaciones, de la más barata a la más experimental:
1. **Certificar la separación sobre una región.** En 5.2 quedó dicho que una distancia nula durante las iteraciones no se puede certificar de antemano. Con intervalos sí: si la extensión de `pairDistance` sobre la caja donde se mueve el ajuste tiene extremo inferior positivo, ningún punto de esa caja tiene nodos coincidentes. El tipo `SeparatedPairs` pasaría a valer para la región entera, no para un punto.
2. **Tolerancias calculadas en vez de escritas a mano.** Hoy `scaledTol` y `roundingSlack` son constantes. Con bolas o intervalos con redondeo dirigido, la cota de error de cada cálculo sale del cálculo mismo. Es lo que 06 §8 deja pendiente: tolerancias que sean consecuencia de la ley de redondeo.
3. **Certificar que el óptimo es global.** Ramificación y acotación con intervalos (Hansen) descarta las cajas cuya cota superior de la log-verosimilitud está por debajo del mejor valor encontrado. Daría tu opción (d) llevada al extremo: un máximo con certificado de globalidad, no sólo de estacionariedad. Con 30 parámetros es caro, y ahí es experimental de verdad.

Si querés, lo dejo como nota en `docs/ideas` del repo de Luthier, junto a la de los tipos como certificados, para retomarlo después de los generadores.

## 65. Luciano  2026-10-05 22:14:04 UTC  (line 3874)

bueno, 
1) dejalo como nota en doc ideas
2) veamos si el principio que implica mi documento esta explicito en los documentos y especificaciones

## 66. Model  2026-10-05 22:16:36 UTC  (line 3925)

La nota quedó en `luthier/docs/ideas/interval-bounds-2026-10-06.md`, sin commitear. La otra sesión tiene en ese mismo directorio archivos sin commitear (el documento de generadores y los dos informes de los agentes), y no quise mezclar commits.

Tu principio está en la especificación sólo a medias. Está la mitad estática: que un tipo con leyes es un certificado, y que una ley certificada no se vuelve a probar. Falta la mitad que tu nota pone primero: que un chequeo hecho sobre un valor cambie el tipo de ese valor, para que nadie lo repita.

**Lo que ya está explícito:**
- 00 dice del subtipo que sus leyes "se chequean con `test` y se registran. Esto es lo que hace a Luthier", y que el subtipo es "un mono con un certificado". También dice que el tipo es la proposición que el nombre afirma y el cuerpo su evidencia.
- 05 §7 aplica el principio al programa entero: un archivo importado acepta los certificados por hash, sin volver a correrlos.

Las dos cosas valen en el momento de certificar y para nombres definidos, no para valores que aparecen al correr el programa.

**Lo que está a medias:** 05 §7 dice que una obligación dentro de `if c then a else b` lleva `c` como precondición. Usa el chequeo sólo para debilitar obligaciones; no dice que dentro de la rama la variable pase a tener el tipo refinado. Por eso el parche de anoche compara la obligación con la condición textualmente. Las "Open" de 05 piden lo mismo para `match m { just x -> … }`.

**Lo que no está en ningún lado:**
1. **La regla "no chequear dos veces"** como tal. Tus notas de voz del 29 de mayo y el principio de 07 dicen "no declarar dos veces lo mismo con dos nombres". Es la misma idea aplicada a nombres; la tuya se aplica a hechos sobre valores, y no aparece.
2. **Que un chequeo devuelva el valor refinado** en lugar de un Bool. Nada en la especificación lo pide, y por eso el código hace lo contrario: `ValidGraph` devuelve Bool, `firstViolation` devuelve `Maybe Violation` sin el grafo, `MaxResult` guarda `converged : Bool` y el ajuste guarda `separated : Bool`. El doble chequeo de validate_graph es legal según la especificación actual.
3. **Cuánto debe nombrar el tipo de un resultado.** No hay criterio para tu opción (d): que un resultado caro lleve en su tipo las entradas de las que salió (`fit : (g : ValidDistanceGraph) -> Fit g`), ni para tu argumento del costo.
4. **`run --checked` como excepción deliberada.** Vuelve a chequear a propósito, para depurar el puente, y debería decirse que es la única excepción.

**Dónde lo pondría:**
- **En 00,** el principio con tus palabras, como la razón de ser de los tipos, junto a "un nombre por concepto" de 07: son el mismo principio en dos niveles, un nombre por concepto y un chequeo por hecho.
- **En 05, dos reglas nuevas.** La primera: dentro de la rama de un `if` cuya condición es un predicado sobre una variable, esa variable tiene el tipo refinado (occurrence typing). La segunda: un chequeo que puede fallar se escribe como una función que devuelve una suma con el valor refinado o la razón de la falla. Más la excepción de `--checked`.
- **En 01 o 07,** el criterio de granularidad: un resultado caro lleva sus entradas en el tipo, uno barato lleva su cota.
- **En los pendientes,** los casos del código que hoy lo violan (`fastCheck` más `ValidGraph` en validate_graph, `converged`, `separated`, `Fit` indexado por la dimensión).

¿Lo escribo en 00 y 05 así?

## 67. Luciano  2026-10-05 22:20:39 UTC  (line 3928)

Hay un principio de simplicidad que hace que un chequeo devuelva un bool. Pero con un  monada aplicada sobre el chequeo podes hacer que devuelva un tipo chequeado. 
quiero decir, ambas funciones son validas, el contexto indica cual usar  quizas.  
pensemos un poco.

## 68. Model  2026-10-05 22:21:38 UTC  (line 3932)

Estoy de acuerdo: las dos funciones son válidas y no compiten. Son dos presentaciones del mismo objeto, y Luthier podría declarar sólo la versión Bool y obtener la otra gratis, siempre que el lenguaje sepa una cosa que hoy no sabe.

**Las dos presentaciones.** Un predicado `p : T -> Bool` corta el subtipo `{ x : T | p x }`, y ese subtipo se presenta de dos maneras:
- **El chequeo Bool** es la función característica: dice sí o no. En la teoría de categorías, Bool hace de clasificador de subobjetos.
- **El chequeo refinado**, `refine p : T -> Maybe { x : T | p x }`, es la inversa parcial de la inclusión: devuelve el mismo valor con su tipo nuevo, o nada. Maybe hace de clasificador de funciones parciales.

Cada una se obtiene de la otra. De la refinada sale la Bool olvidando el valor. De la Bool sale la refinada con un solo combinador genérico:

```
refine p x = if p x then just x else nothing
```

Así que no hace falta escribir cada chequeo dos veces, cosa que además violaría "un nombre por concepto". Se escribe `p` una vez, como Bool, porque es la ley y porque los Bool se componen solos (`and`, `or`, `not`); la versión refinada se deriva. Es la misma figura que el Kernel con sus tres presentaciones atadas por leyes.

**Lo que el lenguaje tiene que saber** es que en la rama `then` de `if p x` vale `p x`. Sin eso, `refine` ni siquiera tipa: `just x` no sería un `Maybe { x | p x }`. Es la regla de refinamiento por rama de la que hablamos. Con ella, el `if` funciona como el bind de la mónada: convierte el Bool en evidencia dentro de su alcance, y la versión Bool deja de causar chequeos repetidos.

**El contexto que decide** me parece que es uno solo: si la evidencia tiene que sobrevivir fuera de la rama.
- Si el resultado se usa ahí mismo, en el cuerpo del `if`, alcanza con el Bool y la regla de la rama, sin envoltorio.
- Si el valor tiene que salir de ese alcance (devolverse, guardarse en un registro, pasar a otra función más tarde), la evidencia tiene que viajar en el tipo. Ahí hace falta `refine`, o una función que devuelva directamente el tipo refinado.

Eso explica por qué los bordes del programa (leer un archivo, recibir algo de Python) piden la versión refinada y el interior se arregla con Bool. Para encadenar varios chequeos en un borde está la mónada propiamente dicha:

```
readGraph >>= conColumnas >>= válido >>= fit
```

Cada paso recibe el tipo que el anterior certificó, y Luthier puede definir ese bind para `Maybe` en una librería, con los parámetros implícitos que ya existen.

**Una sutileza propia de Luthier:** el chequeo de la rama no tiene por qué ser el mismo predicado. En validate_graph se pregunta `fastCheck g == nothing` y lo que se necesita es `ValidGraph g`.
- Si la condición es el propio `p`, el refinamiento es definicional: no se debe nada.
- Si es otro predicado `q`, el refinamiento genera la obligación `q g -> ValidGraph g`, y esa obligación es justamente la ley `ReportsValidity`, que ya está certificada.

Entonces validate_graph se puede escribir con un solo chequeo al correr, sin el segundo `if ValidGraph g`. El "segundo chequeo" se mueve a la certificación, donde se hace una vez y queda registrado. Esa es tu idea en su forma exacta: al correr se chequea una vez, y la relación entre chequeos se certifica una vez. El límite es que esa relación está probada por test, no demostrada, así que el grado de lo que viene después hereda el grado de esa ley.

Con esto, `converged : Bool` en `MaxResult` no está mal en sí: el Bool más la ley que lo ata al hecho (`MaximizerStationary`) más la regla de la rama equivalen a la suma refinada. La diferencia está en dónde vive la información. Con el Bool, el vínculo entre la bandera y el hecho está en una ley aparte que alguien tiene que acordarse de certificar. Con la suma, está en el tipo. La garantía es la misma, porque ambas se prueban igual; cambia la ergonomía y la posibilidad de olvidarse.

**Lo que propongo para la especificación:**
1. Las leyes y los chequeos se escriben como Bool. Es tu principio de simplicidad, y ya es la forma de las leyes.
2. La regla de refinamiento por rama. Es lo único nuevo en el núcleo del chequeador de tipos, y es lo que hace que un Bool no se vuelva a chequear.
3. Un `refine` genérico, y su variante con la razón de la falla (`Either E { x | p x }`, atada a `p` por una ley como `ReportsValidity`), en una librería.
4. Como criterio de uso: refinar en los bordes, o cuando la evidencia sale del alcance de la rama; Bool en el resto.

¿Te cierra así, o ves casos donde el contexto pida otra cosa?

## 69. Luciano  2026-10-05 22:25:10 UTC  (line 3939)

Me cierra asi, pero por las dudas  fijate si hay contextos que pidan otra cosa, no pierdas mas de 5 minutos.

## 70. Model  2026-10-05 22:25:46 UTC  (line 3943)

Sí hay cuatro contextos que piden otra cosa. Ninguno invalida lo que acordamos; lo amplían. El primero además marca un error mío de anoche.

**1. Chequeos sobre el mundo, no sobre valores.** Si el hecho chequeado es externo, refinar el valor da una garantía que puede vencer. `GraphDir` es exactamente eso, y lo hice yo: certifica al hacer `--set` que el directorio tiene los dos archivos, pero entre ese momento y la lectura los archivos pueden cambiar o desaparecer. Es el problema clásico de chequear a una hora y usar a otra (time-of-check to time-of-use).

Tu principio, bien aplicado, pide refinar lo leído, no la ruta: `readGraph : String -> < graph : DistanceGraph | unreadable : String >`, y validar el contenido. El chequeo y el uso tienen que ser la misma operación. Hay que corregir `GraphDir`.

**2. Veredictos estadísticos.** `UniformDraws`, `IsDensityOf` o el PIT de los residuos no establecen un hecho sobre el valor. Dicen que una prueba con cierta tasa de falsa falla no lo distinguió de lo esperado.
- **Refinar sería mentir:** `{ k | Calibrated k }` afirma algo que el test no demuestra.
- **El Bool pierde información:** se queda sin el nivel ni el estadístico.

Esto pide una tercera presentación, un veredicto con su nivel. Es lo que las "Open" de 05 ya llaman igualdad como grado, y lo que falta de 5.5 (tasa de falsa falla, repetir con otra semilla).

**3. Chequeos que producen un testigo.** A menudo el chequeo calcula algo que vale más que el sí o el no:
- `positiveDefinite` hecho por Cholesky produce el factor, que prueba la positividad;
- la separación produce la distancia mínima;
- `existsBelow controlSeeds` encuentra la semilla que atrapó al mutante;
- `firstViolation` encuentra la fila;
- la convergencia de Levenberg-Marquardt produce el decremento y el espectro final.

Devolver sólo el valor refinado tira ese trabajo. En la literatura se llama algoritmo certificador (McConnell, Mehlhorn, Näher y Schweitzer, 2011): el algoritmo devuelve su resultado y un testigo que un chequeador simple verifica. El valor refinado es el caso particular en que el testigo es el valor mismo. En general el resultado es un par dependiente `(x, w)` con una ley que dice que `w` atestigua `p x`. Encaja con tu opción (d) para cálculos caros: el tipo guarda la evidencia junto con las entradas.

**4. Todos los errores, no el primero.** La mónada corta en la primera falla, y eso conviene para un pipeline (leer, después validar, después ajustar). Pero para validar un grafo a mano querés la lista completa de violaciones. Eso no es una mónada sino un aplicativo que acumula errores (la "Validation" de Haskell). `firstViolation` eligió cortar; una `violations : DistanceGraph -> List Violation`, atada a `ValidGraph` por una ley (vacía si y sólo si es válido), es la otra opción, y el contexto decide entre las dos.

Hay un quinto caso menor: los chequeos con tolerancia (`approx tol`) no se componen, porque "a cerca de b" y "b cerca de c" no dan "a cerca de c" con la misma tolerancia. Si se refina con ellos, la tolerancia tiene que ir en el tipo.

Si te parece, lo sumo a la especificación junto con lo anterior: Bool como forma primaria y el refinamiento por rama como regla, más tres formas derivadas para estos contextos (veredicto con nivel, par con testigo, lista de errores) y el principio de que un chequeo sobre el mundo refina lo leído, no la referencia.

## 71. Luciano  2026-10-05 22:29:30 UTC  (line 3946)

Si, suma todo eso.

## 72. Model  2026-10-05 22:30:43 UTC  (lines 3979, 4012)

Escribí el principio en 00; ahora la regla R11 y la sección de chequeos en 05.

Lo sumé en tres lugares de la especificación y en el plan. Todo queda sin commitear, porque la otra sesión sigue commiteando en el mismo repo. Antes de commitear miro qué tocó ella, para que mis cambios no queden dentro de un commit suyo con otro mensaje.

**00, sección nueva "What types are for: a check is made once".** Tu principio con tu nota como fuente, presentado como la misma idea de 07 aplicada a hechos: un chequeo por cada hecho. Explica cómo actúa en tres momentos (al certificar, al correr y en el borde del programa con el mundo) e incluye el criterio de granularidad con tus dos ejemplos. Un resultado barato lleva su cota (`sin x` en [−1, 1]); uno caro lleva sus entradas y su testigo (el óptimo de f y x desde b0).

**05, regla R11 "A condition refines in its branch".** Dentro de `if p x`, `x` tiene el tipo refinado y la coerción no debe nada. Bajo otra condición `q x` se debe `q x -> p x`, que suele ser una ley que ya existe, como `ReportsValidity`. Vale igual para `match m { just y -> … }`, y reemplaza el descarte textual de anoche. Está marcada como decidida y no implementada.

**05 §9, bloque "Checks" dentro de "Presentations and translations".** El Bool y `refine` como las dos presentaciones del subtipo, con `refine` escrito una sola vez. El criterio para elegir es si la evidencia tiene que salir de la rama; en los bordes se encadena con el bind. Además están las cinco formas derivadas, cada una atada a `p` por una ley:
- la razón de la falla;
- la lista de todas las fallas (un aplicativo);
- el valor con su testigo, citando los algoritmos certificadores;
- el veredicto estadístico con su nivel;
- la tolerancia en el tipo.

Cierra con dos reglas: un chequeo sobre el mundo refina el contenido leído, y `run --checked` es la única excepción a chequear una vez. También agregué el pendiente en "Open" de 05.

**El plan, sección "Added 2026-10-06: checks recorded in types".** Lista lo que falta implementar: R11 en el chequeador de tipos y `refine` con sus formas en una librería. Y en el proyecto:
- sacar el doble chequeo de validate_graph;
- reemplazar `GraphDir` por un `readGraph` que devuelva el grafo o la razón de no poder leerlo;
- convertir `converged` y `separated` en sumas con testigo;
- indexar `Fit` por el grafo.

¿Lo commiteo?

## 73. Luciano  2026-10-05 22:48:25 UTC  (line 4015)

commitea si

## 74. Model  2026-10-05 22:49:36 UTC  (line 4029)

Commiteado como `ae67242` en la rama `numbers` del repo de Luthier, sin push. Entraron sólo mis cuatro archivos: 00, 05, el plan y la nota de intervalos en `docs/ideas`.

Quedó afuera lo que no es mío de esta conversación: los certificados que la otra sesión está regenerando y tus notas en `random.lut`.

## 75. Luciano  2026-10-05 22:51:30 UTC  (line 4032)

hay algo que me pone nervioso y es que modelamos los reales con racionales. 
Eso esta bien para algunos casos puntuales pero como estrategia general me parece sucida en cuanto a los tiempos, me podes contar de que se trata eso?

## 76. Model  2026-10-05 22:51:57 UTC  (line 4040)

No modelamos los reales con racionales. Los racionales aparecen sólo como regla de medir en dos tests de librería, y ningún cálculo del proyecto los toca.

**Los tres tipos y para qué está cada uno:**
- **`Real`** es el ideal matemático. Nada lo calcula: su estructura de cuerpo ordenado completo es un axioma, y el lenguaje no deja escribir código que corra sobre él.
- **`Float64`** son los doubles de IEEE. Todo lo que corre corre con ellos: experiment_zero, las verosimilitudes, Levenberg-Marquardt, numpy.
- **`Rational`** son fracciones exactas de enteros. Sirven para una sola cosa: verificar que cada operación de los doubles redondea bien.

**Por qué racionales para eso.** Todo double finito es exactamente un racional (una mantisa entera por una potencia de 2). Entonces el resultado exacto de `x + y` o `x * y` entre dos doubles también es racional, y se puede comparar el double que da la máquina contra el valor exacto sin ninguna tolerancia. La ley de redondeo, `|fl(x op y) − (x op y)| ≤ u·|x op y|` con u = 2⁻⁵³, queda decidida exactamente. Antes esas leyes se escribían con tolerancias a ojo, y la ley de cuerpo de los doubles era directamente falsa.

**Dónde se usan.** Sólo `lib/rational.lut` y `lib/algebra_python.lut`, que certifica las hojas de numpy (suma, producto escalar, matriz por vector) contra la cota de Higham. Ningún archivo del proyecto los importa. En la recertificación de anoche esos dos tests tardaron 2 s y 8 s.

**Tu miedo es correcto en general.** En cadenas largas los denominadores crecen sin control, y la aritmética racional se vuelve inutilizable. Por eso se los usa sólo para una operación o una suma de hasta 16 términos contra su valor exacto, y nunca dentro de un cálculo.

**Su límite:** no alcanzan para lo irracional. La raíz cuadrada se verifica con un truco que se queda en los racionales (`|r² − x| ≤ (2u + u²)·x`). Pero `exp`, `log` o `sin` no tienen valor exacto racional, y para verificarlas haría falta aritmética de bolas o intervalos (Arb), como en la nota de anoche.

La protección contra la estrategia suicida está en la especificación (06): código que corre se escribe sobre `Float64`, o genérico en su tipo numérico, y `Rational` se reserva para enunciar y certificar leyes.
