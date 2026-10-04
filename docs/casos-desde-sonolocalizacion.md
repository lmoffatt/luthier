# Casos de diseño que trajo Sonolocalización

2026-09-30. Lo que apareció al escribir `~/Projects/sonolocalizacion/luthier/*.lut` sobre
`sonolik` (trazas, ruido, ventana, escena sintética), con el commit `49cab6e` de Luthier.
El trato de la nota de traspaso: Sonolocalización define las leyes; lo que no se puede
expresar vuelve acá. Cada caso dice qué se quiso escribir, qué se escribió en su lugar, y
qué le faltaría a Luthier. El resultado del lado de Sonolocalización: seis archivos (uno solo de
declaraciones), 33 leyes certificadas, un hallazgo sobre el dominio de una postcondición (la identidad
Cov = ρ/2 vale solo donde el template cae dentro de la ventana), y estos nueve casos.

## 1. Resolución de `extern` relativa al archivo

`luthier check luthier/traza.lut` falla con `No module named 'sonolik'` aunque se corra
desde la raíz del proyecto: el script de consola pone su propio directorio en `sys.path`,
no el de trabajo. Funciona con `PYTHONPATH=.` o con `python -m luthier.cli`. Propuesta:
agregar a `sys.path` el directorio del `.lut` que declara el `extern` (y quizás el de
trabajo), o admitir una forma relativa `extern "python:./sonolik.trace.gcc"`.

## 2. Leyes sobre arreglos

Quise escribir "la grilla de retardos es estrictamente creciente y de paso uniforme" y
"ningún bin del espectro es cero". Son `forall` sobre los elementos de un arreglo de
decenas de miles de valores. Pasarlo como `List R` lo marshalea entero a cons/nil y lo
recorre en el intérprete; con 131 072 puntos no es viable. Quedaron como predicados
`extern` (`lagsUniform : Trace -> Bool`, `psdMin : NoisePSD -> R`), o sea la ley se corre
en Python y Luthier solo la nombra. Faltaría un tipo indexado (`Vec n R` o un opaco con
`length` y `at`) y un `forall` que Luthier evalúe llamando al `at` sin desarmar el valor,
o una forma declarada de delegar el cuantificador al entorno y que el certificado lo diga.

## 3. Leyes estadísticas

Las dos postcondiciones centrales de `gcc` son sobre esperanzas: E[g(τ)] = a ρ(τ − τ₀) y
Cov[g(t₁), g(t₂)] = ρ(t₁ − t₂)/2. Una esperanza se mide promediando realizaciones del
ruido. Luthier no tiene ese cuantificador, así que el promedio lo hace Python
(`ensemble_mean_error(scene, n)`) y la ley quedó enunciada sobre el estadístico de
conjunto, `MeanLaw := { e : Scene -> Int -> R | e s 200 < 0.03 }`, no sobre el
correlador. Es honesto pero desplaza el sujeto de la ley. Lo que haría falta es la
equivalencia estadística `a ≈ b` con umbral y muestra de `00-elementos-fundamentales.md`
sección 4, como cuantificador "sobre n realizaciones de la variable aleatoria x", con `n`
registrado en el certificado.

Un intento intermedio no funcionó: pasar el correlador (`f : Signal -> ... -> Trace`) a
un `extern` de orden superior para que Python promedie llamándolo. `to_python` convierte
una lambda en un callable, pero cuando Python la llama con un arreglo, `from_python(x,
None)` no tiene el tipo y desarma el arreglo en una lista de literales; y un objeto opaco
sin tipo no vuelve. Con el tipo de la lambda a mano (lo tiene el checker) los argumentos
podrían entrar como opacos.

## 4. Contraejemplos opacos

Cuando una ley sobre `Scene` falla, el certificado dice `counterexample: s = <Scene>`. No
se puede reproducir el caso salvo repitiendo toda la corrida con `--seed` y `--show-cases`
hasta llegar a él. Dos remedios compatibles: un `show` registrable por tipo opaco (`show
Scene := extern "python:...describe_scene"`) que el certificado use al imprimir, y guardar
por caso la semilla con que el generador lo produjo, así `luthier eval` puede regenerarlo.

## 5. Leyes sobre una corrida concreta

Las etapas 00 a 04 del experimento cero corren sobre las sesiones A y B. La afirmación que
importa ("el rms horizontal contra la cinta es menor que 5 cm") es sobre esos datos, y se
comprueba una vez. Luthier v0 tiene un solo modo de comprobación, casos generados, y no
hay forma de declarar `Passes validacionA 5.0` y certificarlo como instancia, con el hash
de los datos de entrada además del de la definición. Es el `Veredicto` que la gramática
deja abierto (sección 7): el modo (muestreado con `n`, exhaustivo, instancia, demostración)
lo cierra el `test` y lo registra el certificado. Sin esto, la parte de Sonolocalización
que más pide certificación, la del campo, no se puede luthierizar.

## 6. Objetos que son archivos

La idea original de luSono: los objetos son archivos y cada sentencia es una línea de
bash (`python 02_fine_peaks.py --session A`). Para eso hace falta: un tipo con
instanciación (el mismo `Peaks` como npz, como csv), funciones que cambien la
instanciación, y un `extern` que corra un proceso con argumentos y lea su salida, con el
hash del archivo producido en el certificado. `pipeline.lut` en Sonolocalización deja
las etapas como huecos tipados para que se vea la forma; ninguna corre.

## 7. Obligación dentro de un `match`

Escribí el generador de un subtipo de `Int` como en `random.lut`:

    Oversample : U := { k : Int | 4 <= k and k <= 32 }
    genOversample : Gen Oversample := \ size s { match randBelow 29 s { (k, s2) -> (4 + k, s2) } }

La coerción de `4 + k` a `Oversample` dentro de la rama dejó la ley
`4 <= 4 + k and 4 + k <= 32` con `k` cuantificado libremente, y `test` la refutó con
`k = -1`. La obligación perdió que `k` es la primera componente de `randBelow 29 s`, que
está en `[0, 29)`. Escrito como `\ size s { genIntBetween 4 32 size s }`, la coerción cae
sobre el par entero y la ley queda sobre `size` y `s`, que es la correcta, y pasa. Es un
caso del refinamiento `|>` de la gramática (sección 5): dentro de la rama, la ley debería
poder asumir lo que el `match` estableció sobre las variables del patrón, o al menos la
obligación debería cuantificar sobre el escrutinado y no sobre las variables del patrón.

## 8. Subtipo por patrón

`{ (lo, hi) : R * R | 0.0 < lo and lo < hi }` está en la gramática (sección 4) y da
`parse error: expected 'name', got '('`. La forma con componentes nombradas
`{ lo : R, hi : R | ... }` funciona. O se implementa el patrón, o se saca de la gramática.

## 9. Un generador de Python saltea el predicado

`gen T := extern "python:..."` registra la función y `Generators.sample` devuelve lo que
produce sin evaluar el predicado de `T`. Con `Nperseg : { k : Int | 256 <= k and k <= 8192 }`
y un generador de Python, cualquier entero habría pasado como `Nperseg` sin aviso. El
generador escrito en Luthier sí deja obligación (caso 7), así que la asimetría es de
confianza: lo de Python se cree, lo de Luthier se comprueba. Dos salidas: comprobar el
predicado sobre lo que devuelve Python (y contarlo como rechazo), o marcar en el
certificado que ese dominio es una afirmación externa sin certificado.

## 10. El producto de tipos asocia distinto que la tupla

`Position : U := R * R * R` se parsea como `(R * R) * R`, pero la tupla `(x, y, z)` y el
patrón `(x, y, z)` asocian a la derecha, `(x, (y, z))`. Entonces `match p { (x, y, z) -> ... }`
sobre ese tipo falla con `tuple pattern (y, z) against non-pair type R`. Escribiendo el tipo
como `R * (R * R)` funciona. La gramática dice que el par asocia a la derecha; el `*` sobre
tipos debería hacer lo mismo, o el desazucarado de la tupla debería seguir al tipo.

(Resuelto el 2026-10-04: un producto de más de dos tipos asocia a la derecha, como la tupla;
`04 §2`.)

## 11. El orden de las definiciones importa (decidido el 2026-10-04)

`00-elementos-fundamentales.md` dice que un programa es un conjunto de definiciones sin
orden y que las dependencias se leen de los nombres. El verificador de v0 chequea en el
orden del archivo: usar `distance` antes de definirla da `unbound name distance`. O se hace
una pasada previa que junte las firmas, o se documenta que el orden es el del archivo.

Resuelto por `05-static-semantics.md §2`: la pasada previa deja de ser opcional, porque las
reglas se juzgan sobre los objetos (las componentes fuertemente conexas del grafo de
dependencias) y eso exige el programa entero. Pendiente de implementar.

## 12. Un literal de lista contra un subtipo se rechaza

`d : NormDist Position := [((0.0, 0.0, 0.0), 0.25), ((1.0, 0.0, 0.0), 0.75)]` da
`a list literal was given but { d : Dist Position | Normalised Position d } was expected`.
Declarando primero `d0 : Dist Position := [...]` y después `d : NormDist Position := d0`, el
valor cerrado se comprueba contra el predicado y se acepta. El azúcar de lista debería
coercionarse igual que un nombre.

## 13. Un predicado trivialmente verdadero deja una obligación pendiente (decidido el 2026-10-04)

`Scene : U := { frame : Frame, ... | true }` existe porque las componentes nombradas solo
se escriben en la forma de subtipo. Cada función que construye una `Scene`
(`withEmitters : Scene`) aparece como pendiente de test aunque su ley sea `true`. O se
descarga `true` al verificar, o hace falta una forma de registro sin predicado.

Resuelto por `05` en la dirección contraria a las dos propuestas: `{ ... | true }` no define
nada (R3), y el registro con etiquetas sin `|` es el producto, estructural, que se escribe
donde se usa o se nombra con un alias, `Scene = { frame : Frame, ... }`, nunca con `:=` (R4, R7).
`Scene` tiene que escribir su ley o ser un alias del producto.

## 14. Acceso a componentes con nombre (resuelto el 2026-10-01)

Sin proyección, cada tipo con componentes nombradas arrastraba una función por componente
(`positionOf`, `receiverPosition`, `clockOf`, `fsOf`...), con nombres globales que chocaban
entre tipos y un programa que parecía Java. Se implementó `e.position` como azúcar del
`match` de una rama sobre el patrón del tipo, con el mismo punto de la calificación de
módulos: un módulo es un registro cuyas componentes son sus definiciones, así que no hace
falta `::`. De paso el subtipo con componentes nombradas pasó a ser un producto dependiente.
Ver la sección 8 de la gramática.

## 14. `gen` solo acepta un nombre, y busca el generador por el tipo tal como está escrito

`gen Probability Position := genProb` es error de sintaxis, y `gen (Probability Position)`
también. Hay que definir un alias, `PositionProbability : U := Probability Position`, y
registrar `gen PositionProbability := ...`. Pero el generador se busca por el tipo tal como
está escrito en la ley: una ley sobre `p : Probability Position` no encuentra el generador
del alias, así que todo el programa tiene que escribir el alias. Dos arreglos posibles: que
`gen` acepte un término de tipo, o que la búsqueda normalice el tipo antes de comparar.

## 15. Un `extern` no puede ser un atributo de módulo

`eps : R := extern "python:sys.float_info.epsilon"` falla con `No module named
'sys.float_info'`: la resolución parte en el último punto y lo anterior tiene que ser un
módulo importable. Se resolvió con `ulp : R -> R := extern "python:math.ulp"` y `eps := ulp 1.0`.
La forma `módulo:atributo.atributo` existe en el código pero no está documentada.

## 16. Una obligación cuantificada sobre un tipo no se puede testear, y la instancia no la hereda

`pushforward (A B : U) (f : A -> B) (p : Probability A) : Probability B := mapMeasure A B f p`
deja la obligación "el resultado suma uno" cuantificada sobre `A` y `B`, y `test` falla con
`no generator for U`. Es la ley del functor y es verdadera por construcción (los pesos no se
tocan), así que es candidata a `probado` más que a `testeado`. La salida natural, declarar
una instancia `shiftBy (v : Position) (p : PositionProbability) : PositionProbability :=
pushforward ... p`, no sirve: como el cuerpo ya tiene el tipo declarado, la instancia no
genera obligación ("no laws"). Hubo que escribir la ley a mano como predicado sobre la
instancia (`ShiftSumsToOne`) y un subtipo `Functorial`. Propuesta: que una instancia de una
definición con obligaciones pendientes sobre tipos herede esas obligaciones, especializadas.

(2026-10-04: sin resolver. `05 §7` deja dicho que una ley cuantificada sobre todos los modelos
de una teoría, o sobre `U`, no tiene generador y se certifica modelo por modelo; la herencia de
obligaciones especializadas que este caso pide sigue siendo propuesta, y la ley del functor
sigue siendo candidata a `proved`.)

## 17. El costo de los valores de lista

Normalizar una lista de cuarenta celdas `(Position * Weight)` y comprobar que suma uno
tarda unos diez segundos por caso en el intérprete: dos casos de `test shift`, 23 s. Con
cien casos por ley, veinte minutos. El generador quedó en diez celdas. El evaluador reduce
por sustitución, y cada paso recorre el término entero; con listas de decenas de elementos
eso es cuadrático o peor. Es el mismo problema del caso 2 visto desde el costo: hace falta
un evaluador con entornos, o un primitivo de arreglo que no se desarme en cons.

## 18. `R` no estaba definido en ningún lado (resuelto)

`Prob`, `Density` y `Nats` son subtipos de `R`, y `R` no era una definición sino un nombre
cableado en el intérprete (`BUILTIN_TYPES`), contra la sección 1 de la gramática. Resuelto
el mismo día: `Int`, `R` y `String` son huecos declarados en `core.lut`; el intérprete los
llena con literales, aritmética y comparaciones y reserva solo `Law`. Lo que falta es lo que
pide `00-elementos` sección 3: `R` como estructura con sus operaciones como funciones y sus
leyes (aproximadas, porque es un double), de las que `eps` en `real.lut` es la primera.

## 19. El plan B, y lo que cerró (2026-10-01, noche)

`luthier.load` carga un programa desde Python; `Program.fill(nombre, fn)` llena un hueco con
una función de Python (aridad del tipo, firma chequeada); `eval`, `test`, `blocked_by`,
`record`. Los registros cruzan como dataclasses, las listas por su tipo de elemento, las
funciones como callables tipados en los dos sentidos. Al hacerlo se cerraron los casos 12 (un
literal de lista contra un subtipo se acepta y deja la obligación) y 13 (`| true` no deja
obligación), y el 3 en parte (una función de Luthier pasada a Python recibe sus argumentos
por los tipos declarados). Nuevo: cuando el predicado de un subtipo es una ley cuantificada
(`Causal waveform` en `Emitter`), el generador por rechazo no podía decidirla; ahora la prueba
con unos pocos argumentos generados y rechaza el valor ante un contraejemplo. Certificar la
ley sigue siendo tarea de la obligación, no del generador.

## 20. Evaluador con entornos: lista de deseos urgente (2026-10-02)

Decidido con Luciano al escribir `lib/array.lut`. El evaluador reduce por sustitución (caso
17) y eso limita todo lo nativo. Mientras tanto, los arreglos son opacos (`Vec`, `Mat` de
numpy) y Luthier los ve por accesores (`at`, `entry`, `length`, `rows`, `cols`) y los
construye por su dual (`tabulate`, `tabulateMat`): las definiciones nativas son recursiones
sobre un índice, no sobre una lista, y el término que se reescribe es de tamaño constante.
Regla adoptada: extern siempre; ley siempre; definición nativa solo cuando la ley no
determina la operación (dot, det, una likelihood), no cuando la caracteriza (solve, autovector).
Costo medido: las trece leyes de `array.lut` tardan 16 s, de los cuales 13 son el determinante
por Laplace con 30 casos y n <= 4, por las llamadas de ida y vuelta a Python en cada entrada
de cada menor. Un evaluador con entornos (normalización por evaluación) bajaría el costo de
lo nativo de cuadrático a lineal; sigue pendiente el caso 2 (dimensiones en el tipo).

## 21. Evaluador con entornos y llamada por necesidad (resuelto el 2026-10-02)

`machine.py` evalúa términos cerrados a valores: una función es una clausura (cuerpo y
entorno), un argumento es un thunk que se calcula la primera vez que se pide y queda
guardado, y una constante global se calcula una sola vez por corrida. Las posiciones de cola
(cuerpo de una clausura aplicada, rama elegida de un match) corren en un bucle. Lo usan los
casos de las leyes y `eval`; el checker sigue con sustitución para los tipos, que son chicos y
tienen variables libres. Lo que la máquina no maneja (variable libre, hueco sin llenar, nodo
previo a la elaboración) cae al evaluador por sustitución; con `LUTHIER_TRACE_FALLBACK=1` se
ve cada caída. Dos presupuestos: `fuel` (checker, 200 000) y `run_fuel` (ejecución, 50
millones, `--fuel`). Medido en sonolocalización:

| corrida | antes | ahora |
|---|---|---|
| intercambiabilidad, 50 casos | ~25 s | 2,5 s |
| calibración, 5 casos de 400 actualizaciones | 5 min y `--fuel` | 39 s |
| distances_python.lut completo | ~2 min | 13 s |
| tests de Luthier | 5 s | 3,4 s |

Y los `match` que forzaban argumentos en `belief.lut` dejaron de hacer falta: la versión
directa tarda lo mismo. Los casos 2 y 17 quedan resueltos en costo; falta lo de las
dimensiones en el tipo.

## 22. Dimensiones en el tipo, operadores por tipo, espectro nativo (resuelto el 2026-10-03)

- Dimensiones como refinamientos: `VecOf n`, `MatOf m n`, `SpdOf n`, `DeficientOf n` sobre los
  portadores opacos. Una hoja devuelve `Vec` o `Mat` sin forma; donde se espera un tipo con
  forma, la forma es una obligación que `test` verifica (por ejemplo `length (add a b) == n` en
  `vecSpace (n : Dim)`, en toda dimensión). Los generadores de familias de tipos reciben los
  argumentos (`gen VecOf := extern ...` se llama `fn(rng, size, n)`). Las leyes cuantifican sobre
  las dimensiones primero: desaparecieron el `Frame` y los generadores de dimensión fija.
  Los refinamientos y alias de tipos opacos se marshalean como opacos.
- Operadores: `operator + := f` registra f para los tipos de sus dos argumentos; `x + y` se
  resuelve por los tipos de los operandos y cae a la aritmética de Int y R si nada coincide.
- Espectro nativo: Jacobi (rotaciones, barridos cíclicos), funciones espectrales, subespacio
  retenido, pseudoinversa. Dos lecciones: lo de fuera de la diagonal se suma directo (restar la
  diagonal de la norma cancela debajo de sqrt eps), y el par (A, V) se fuerza en cada rotación:
  la llamada por necesidad no evita la fuga del acumulador perezoso.
- `real.lut` declara y `real_python.lut` vincula, como el resto. `--name` respeta la directiva.

Queda abierto: argumentos implícitos (hoy la dimensión se pasa explícita), y dimensiones que el
checker verifique estáticamente en lugar de por obligación.

## 23. Un tipo declarado se usa como si estuviera definido (2026-10-04)

`table.lut` declara `Table : U` sin ninguna ley, y `table_python.lut` lo llena con
`Table : U := extern "python:luthier.tables.Table"` y diez externs sueltos, `nRows : Table -> Int
:= extern ...`. El checker acepta todo: `add_def` solo pide que el tipo declarado tipe contra
`U`, y un hueco tipa. Se probó con seis archivos mínimos: `A : U` seguido de `a : A := extern`,
de `f : A -> Int := \x { 3 }`, de `a : A := b` con `b : A` hueco, y de `A : U := extern` más
`a : A := extern`; los cuatro pasan `luthier check`. Decir "esto es una Table" no garantiza nada,
que es lo que la nota de voz del 2026-10-04 señala.

Resuelto en el diseño por `04-kernel.md` y `05-static-semantics.md`: declarar y definir son dos
estados, una definición solo usa tipos definidos (R2), y un extern da valores, nunca tipos (R5),
con `extern provisional` como salida para el apuro. Los casos están en `tests/spec/` como `r2_*`
y `r5_*`. Lo que `table.lut` tiene que hacer: definir `Table` nativamente (una función de columna
y fila a celda, o un alias de producto si no tiene invariantes), y escribir el códec como una
teoría con su igualdad como componente, de la que `csv` es un modelo (`05 §8`). `Codec` y
`LawfulCodec` pasan a ser un solo nombre.

## 24. `array.lut` no ata sus accesores (2026-10-04)

`Vec : U` es un hueco opaco, `at` y `tabulate` son huecos que numpy llena, y todo lo demás
(`addDef`, `matVecDef`, `transposeDef`) está escrito con esos dos. Pero las leyes que definen a
`Vec` no están en ningún lado: falta `at (tabulate n f) i == f i` para `0 <= i < n`, falta
`length (tabulate n f) == n`, y falta la extensionalidad. Numpy podría devolver cualquier cosa en
`at` y las leyes `Agrees` seguirían comparando contra una definición escrita sobre ese mismo
`at`. Con `04` y `05`, `VecOf n` es nativamente la función `(i : { k : Int | 0 <= k and k < n }) -> R`,
la primera ley es una reducción beta, la extensionalidad se decide enumerando el dominio finito,
y un array de numpy es una representación de un valor de ese tipo, cuya ida y vuelta se certifica.
Es el piloto propuesto para probar la especificación antes de revisar las demás librerías.

(2026-10-04, más tarde: el caso se disuelve. Con `VecOf n = Fin n -> R`, `at` es aplicar y
`tabulate` es escribir una lambda, y la primera ley es beta; un array de numpy es un valor de ese
tipo por definición, y lo que falta son tres reglas del intérprete, no leyes: aplicar un objeto de
Python indexando con verificación de rango, materializar una lambda cuando Python espera un
array, y la correspondencia entre tipo y representación; `04 §6`.)

## 25. Las obligaciones de índice necesitan la rama y el "let" (2026-10-04)

Con `at (v : Vec) (k : Fin v.n)`, `sumTo` escrito como recursión debía `lo < n` en la llamada `f lo`
de la rama `else` de `if lo >= n`, cuantificado sobre todo `lo`: falso. Y `match index m.i k { i ->
... at t (3 * i + a) ... }` cuantificaba la obligación sobre todo entero `i`, olvidando que `i` es
`index m.i k`. Resuelto en el intérprete y escrito en `05 §7`: la condición de la rama es
precondición de la ley, y una variable ligada por `match e { x -> ... }` es `e`.

## 26. Una tabla perezosa en un algoritmo iterativo (2026-10-04)

Jacobi escrito sobre las definiciones nativas (`matMulDef`, una lambda) se quedó sin combustible
en matrices de 6 x 6: cada rotación es una lambda que lee la anterior, y cada entrada leída recalcula
toda la historia. Resuelto en la máquina: una lambda sobre `Fin n` se calcula una vez por índice,
la llamada por necesidad extendida a las entradas (`04 §6`, regla 4).

## 27. El orden de una suma es parte de su redondeo (2026-10-04)

La primera reescritura de `experiment_zero` dio la sesión A en 12 cifras significativas, no bit a
bit: el `sumTo` nuevo sumaba `((0 + f0) + f1) + f2` y el viejo `f0 + (f1 + (f2 + 0))`, y el LM
amplifica la diferencia del último bit. Con el orden viejo coincide exactamente: sigma
0.04868865334248189 m sin `parlante_A2`. Anotado en `04 §6`.

## 28. Lo que la reescritura no pudo certificar en el archivo puro (2026-10-04)

Las obligaciones de `table.lut` sobre tablas (`sameCells`, `sameTable`) no tienen generador ahí:
una función con dominio `String` no se genera como tabla. Se certificaron desde `table_python.lut`
con `--name ... --deep`, que escribe en el certificado de origen. Las obligaciones de funciones
cuantificadas sobre `U` (las de `probability`, `belief`) siguen sin generador y se certifican por
modelo, como dice `05 §7`.
