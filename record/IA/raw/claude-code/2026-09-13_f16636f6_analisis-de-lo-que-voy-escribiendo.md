---
source: claude-code
account: 
id: f16636f6-5641-4546-9840-19f5f5471d40
title: "analisis de lo que voy escribiendo"
started: 2026-09-13T11:15:08Z
ended: 2026-09-14T00:07:54Z
offset: 
turns: 17
cwd: -home-lmoffatt-Projects-sonolocalizacion
exports: 20261009
flags: 
origin:
  - raw/claude-code/20261009/-home-lmoffatt-Projects-sonolocalizacion/f16636f6-5641-4546-9840-19f5f5471d40.48910792.jsonl.gz sha256 48910792adc25501735766cc6ef2649b0ce1864aebcc81762751a7c75587379a
iachat: 1
---

# analisis de lo que voy escribiendo

## 1. Luciano  2026-09-13 11:15:08 UTC  (line 3)

analisis de lo que voy escribiendo

## 2. Luciano  2026-09-13 11:15:31 UTC  (line 47)

focalizate solo en este texto

## 3. Model  2026-09-13 11:16:46 UTC  (line 51)

Análisis del archivo, no lo toqué.

**El agujero más grande: `point` no existe como tipo.** `distance measurement` tiene `start point` y `end point`, y no hay nada a qué apunten. Y ahí hay dos cosas distintas que se te van a mezclar si no las separás ahora:

- el **marcador físico**: la cabeza del trípode, la cápsula del micrófono, el clip, la marca en el piso. Es una cosa que existe, que se puede tocar, y entre dos de esas cosas medís con la cinta.
- la **coordenada**: un vector en algún marco de referencia. Eso no se mide, se estima resolviendo el conjunto de distancias.

Si `point` es una sola cosa, en algún momento vas a tener una fila donde el "punto" tiene coordenadas que en realidad son la salida del ajuste, y perdiste la distinción entre dato y resultado. Marcador es entidad observada; coordenada es objeto derivado, con incertidumbre y con procedencia (qué mediciones lo produjeron, con qué método, qué versión).

**Falta el arreglo.** `registro` tiene un `listening device` singular. Pero lo que se analiza nunca es un registro solo: es el conjunto de registros simultáneos de varios dispositivos en posiciones conocidas. Ese conjunto necesita nombre propio (despliegue, sesión, arreglo): un sitio, un intervalo de tiempo, un conjunto de dispositivos, cada uno montado en un marcador. La geometría vive ahí, no en el registro individual.

**Falta separar medido de derivado.** Tus cuatro tipos son todos del mundo observado. El pipeline produce otras dos cosas que son tan "tipo" como las demás y que hoy no figuran:

- la **geometría estimada** del arreglo (coordenadas de cada marcador, con su covarianza)
- la **alineación de relojes** entre dispositivos (offset y deriva de cada uno respecto de una línea de tiempo común)

Las dos son resultado de un ajuste, las dos tienen incertidumbre, y las dos son lo único que convierte un montón de WAVs en una likelihood sobre el domo. Si no las tipás, van a terminar como variables sueltas en un script.

**`measurement` como campo es vacío, y le falta la incertidumbre.** Necesita valor, unidad, y algo que diga cuánto vale. Ahí tenés una decisión de diseño que conviene tomar explícita: o la incertidumbre es campo de la medición, o se deriva del par (hardware, técnica). Yo iría por lo segundo como default (el instrumento y la técnica llevan el modelo de error) con la opción de que la medición individual lo pise cuando hiciste algo raro. Pero un proyecto que se apoya entero en la verosimilitud no puede tener un tipo "medición" sin ruido.

**`datetime` no alcanza para el tiempo.** En `registro` necesitás inicio y duración, no un instante. Y sobre todo: el timestamp que te da el celular es el reloj del celular, que tiene offset y deriva propios. Toda la localización pasa por diferencias de submilisegundo entre dispositivos. O sea que hay dos tiempos distintos, el local del dispositivo (medido, crudo) y el común (estimado, derivado de los chirps), y el tipo tiene que decir cuál es cuál.

**GPS y geometría local son dos sistemas de coordenadas, no uno.** GPS en metros, el arreglo en centímetros. Tres órdenes de magnitud. El GPS es propiedad del sitio o del despliegue (dónde en el mundo), no de cada registro, y la transformación entre los dos marcos es su propio objeto (posición y orientación del arreglo en el mundo, con su propia incertidumbre, mucho peor que la interna).

**En hardware estás mezclando clase e instancia.** `type` y `model` son propiedades del modelo (respuesta en frecuencia, frecuencia de muestreo, sensibilidad), `unique hardware identifier` es de la unidad individual, que además tiene su calibración propia. Son dos tablas. Lo mismo va a pasar con (4): una cinta métrica y un telémetro láser tienen modelos de error distintos, y esa es justamente la razón de que el tipo exista.

**`unique_id` vs `unique hardware identifier`:** bien que los hayas distinguido en micrófono, pero conviene que sea una regla general. El `unique_id` es tuyo, es clave interna, no significa nada afuera. El identificador del mundo (número de serie, MAC, Android ID) es evidencia, y es exactamente lo que sostiene tu idea de registro no falsificable. Son roles distintos y los dos hacen falta.

**Sobre "¿tipo relational database?":** sí para el mundo observado (equipos, sitios, despliegues, mediciones). Ahí lo relacional es lo correcto y las filas deberían ser inmutables, se agregan, no se corrigen. Pero la parte derivada no es relacional en el mismo sentido, es un grafo dirigido de derivaciones: cada objeto derivado apunta a sus entradas, al método y a la versión. Entra en un esquema relacional igual, pero con otra disciplina. Crudo: se escribe una vez. Derivado: se recalcula, y tiene que poder decir de qué salió.

**Una última, sobre el encuadre.** Arrancás con "definir mi lenguaje sonolik" y seguís con tipos. Un lenguaje son verbos, un esquema son sustantivos, y lo que estás listando son sustantivos de adquisición y procedencia. Los sustantivos de inferencia ya existen en el paquete (`Trace`, la hipótesis, la ventana). Son dos vocabularios distintos y está bien que lo sean. Se tocan en un solo lugar: geometría estimada más alineación de relojes. Ese es el puente, y conviene que sea angosto y explícito.

Si querés te escribo el esquema completo con estos tipos agregados, en el mismo estilo de lista para que lo sigas editando.

## 4. Luciano  2026-09-13 11:23:03 UTC  (line 54)

a ver
vamos definiendo cosas
1) los registros existen por si mismos,  y pueden o no saber a que arreglos pertenencen. yo creo que no deben saberlo porque si son inmutables tengo que decidir al momento de crearlos a cuales arreglos pertenecen los registros y eso seria una decision prematura.  Si podrian referir a una sesion por ejemplo pero en realidad eso ya esta definido justamente por tiempo y lugar...

## 5. Model  2026-09-13 11:23:55 UTC  (line 58)

De acuerdo con la conclusión, pero cambiaría la razón, porque la razón que des ahora te va a decidir los diez casos siguientes.

"Prematuro" es cierto pero es circunstancial. La regla que generaliza es: **un objeto crudo lleva solamente lo que el instrumento supo en el momento de capturar.** El celular sabía su identidad, su reloj, su GPS, y el audio. No sabía que era parte de un arreglo, porque eso no lo sabe nadie hasta después. Con esa regla el registro queda decidido solo, y además te decide de una que la línea de tiempo común tampoco va adentro del registro (es estimada), y que el GPS sí (el aparato lo midió, aunque sea malo).

Y ojo que inmutable no prohíbe referenciar. Un objeto inmutable puede apuntar a algo que ya existía. El problema no es que no se pueda, es que le estarías metiendo adentro de la evidencia una cosa interpretada y revisable. Por eso la regla es sobre el origen del dato, no sobre la mutabilidad.

Ahora, donde sí discrepo: **"ya está definido por tiempo y lugar" no es cierto, y conviene que no lo sea.**

Tiempo y lugar te dan co-ocurrencia, que es otra cosa que pertenencia. Dos celulares a diez metros grabando al mismo tiempo, sin un chirp en común, están co-ubicados y no forman un arreglo, porque no podés alinearles los relojes ni resolverles la geometría. Lo que pertenencia significa realmente es: estos registros son mutuamente alineables. Eso es el resultado de un procedimiento, con un criterio y un umbral, y el umbral es argumento, no constante. O sea que la pertenencia es un objeto derivado con procedencia, igual que la geometría. Eso refuerza tu punto en vez de contradecirlo: no va adentro del registro, pero tampoco queda implícita en una consulta por tiempo y lugar. Es un objeto propio, y podés tener dos agrupamientos distintos de los mismos registros y compararlos.

Aparte, el "lugar" te va a fallar justo donde trabajás. GPS de celular bajo vegetación son cinco a quince metros, a veces peor, a veces no hay. El criterio robusto de agrupamiento no es la posición: **es el chirp compartido.** Dos registros son del mismo arreglo si aparece el mismo chirp de calibración en los dos. Y eso es lindo porque es exactamente la misma operación que te da el offset de reloj. El agrupamiento y la alineación son una sola cosa, no dos pasos.

Falta algo que tu regla deja afuera y que hay que poner en algún lado. **El montaje.** Qué dispositivo estaba sobre qué marcador, entre qué momento y qué momento. Eso es un hecho del mundo en el momento de grabar, no se infiere del audio, y si nadie lo anota la geometría es irrecuperable. No va adentro del registro (el celular no lo sabe), pero es crudo e inmutable igual, solo que el instrumento que lo captura es una persona con una libreta. Ese es un tercer tipo de cosa: hecho observado, anotado por un humano, contemporáneo. Yo lo haría entidad propia, `montaje` o `colocación`, con dispositivo, marcador, intervalo, y quién lo anotó.

Con eso el arreglo queda como derivado de tres cosas: registros que comparten chirp, montajes vigentes en ese intervalo, y la alineación que efectivamente convergió.

Sobre sesión: la tendría igual, pero como nombre humano de un agrupamiento, no como referencia dentro del registro. Sirve para que puedas decir "la sesión del charco chico" en vez de recitar seis identificadores. Y permitiría que una sesión se declare a mano, porque en el campo vos sabés lo que pasó y la consulta automática puede fallar.

## 6. Luciano  2026-09-13 11:32:32 UTC  (line 64)

si tenemos un objeto, como un registro de audio, luego lo vamos decorando con analsis como ubicacion, fuentes de sonido que se yo lo que sea. 
La idea es que cada resultado de un analisis tenga sus propios campos y los ids de los objetos que los originaron?

## 7. Model  2026-09-13 11:33:16 UTC  (line 68)

Sí, esa es la forma correcta. Dos correcciones y una trampa.

**"Decorar" es la palabra peligrosa.** Sugiere que el resultado se pega al registro y que el registro crece. No crece, queda exactamente igual, y aparece al lado un objeto nuevo que lo referencia. La diferencia práctica es grande: así podés tener dos localizaciones distintas del mismo registro, hechas con distinto método o distinto umbral, conviviendo sin pisarse. Si "decorás", la segunda sobrescribe a la primera y perdiste la comparación, que es justamente lo que más vas a querer hacer.

**Los ids de las entradas no alcanzan.** El objeto derivado necesita, como mínimo:

- ids de las entradas
- qué función lo produjo, y en qué versión
- con qué parámetros (que por tu propia regla son todos explícitos, ninguno hardcodeado)
- el resultado y su incertidumbre

Sin el método y los parámetros, dos resultados distintos de las mismas entradas son indistinguibles y no tenés forma de saber cuál creer. Y con eso gratis te llevás algo que después no se puede retrofitear: la terna (entradas, método, parámetros) es una clave. Si la hasheás, el mismo cálculo pedido dos veces devuelve el resultado guardado, y cambiar un parámetro genera un objeto nuevo en vez de pisar el viejo. Procedencia y caché terminan siendo el mismo mecanismo.

**Cada derivado apunta a sus entradas inmediatas, no a las originales.** Una localización no depende del registro, depende de (registros, geometría estimada, alineación de relojes). Si apunta al audio crudo salteando los intermedios, perdiste la capacidad de invalidar: recalculás la geometría y no sabés qué quedó viejo. La cadena hasta el crudo se reconstruye caminando el grafo. Si querés el crudo a mano para consultar rápido, guardalo como campo redundante, nunca como la referencia canónica.

Sobre invalidar: cuando recalculás la geometría, todos los derivados viejos siguen apuntando a la v1 y los nuevos a la v2. Eso está bien, no se borra nada. "Cuál es el resultado vigente" es una consulta, no un estado del objeto. Si le metés un campo `vigente` adentro, volviste a hacerlo mutable y perdiste todo.

**La trampa está en "fuentes de sonido".** Ahí hay dos cosas distintas y es el mismo error que marcador contra coordenada:

- la **detección**: en este registro, entre estos dos instantes, hay energía con esta forma. Es una afirmación sobre una grabación.
- la **fuente**: hay un bicho en el mundo, tal vez un individuo, que produjo eso. Varias detecciones en varios registros pueden ser de la misma fuente.

La asignación de detecciones a fuentes es otro derivado, con su método y su incertidumbre, y es donde vive lo difícil (cuántos bichos hay, cuál cantó cuál sílaba). Si colapsás detección y fuente en un solo tipo, esa pregunta deja de poder formularse.

Última, sobre granularidad: no todo intermedio merece persistirse. La traza de cada par en cada ventana es enorme y barata de recalcular. Yo persistiría lo que es caro de recomputar o lo que es una afirmación sobre el mundo (geometría, alineación, detección, localización, asignación). Lo que es puro intermedio de cómputo vive en memoria y se reconstruye. Y cuando persistas, campos tipados por tipo de análisis, no una tabla genérica con un JSON adentro, porque el día que quieras preguntar "todas las localizaciones con sigma menor a cinco centímetros" el JSON te deja a pie.

## 8. Luciano  2026-09-13 11:49:39 UTC  (line 71)

bien, estoy muy tentado a aplicar conceptos de luthier aqui
si ponemos la funcion y la version que lo genero, bien podemos tambien hacer una tabla de funciones. ahi me doy cuenta que la representacion no es la de tabla sino de json relacionales donde no tenes campos fijos?
o quizas si fijos?
las funciones para mi deberian tener a su vez bueno, pre y post conditions

## 9. Model  2026-09-13 11:50:58 UTC  (line 86)

Luthier encaja acá mejor de lo que parece, y no por analogía suelta. Fijate lo que ya tenés: el objeto derivado es la tupla (entradas, función, parámetros, resultado). Eso es literalmente un término de prueba. Su tipo es la proposición "este resultado se obtuvo aplicando esta función a estas entradas". La base de datos no es un registro de resultados, es un almacén de pruebas, y cada fila es el certificado de su propia derivación. Que es exactamente lo que venís buscando con el registro no falsificable, pero extendido a toda la cadena de análisis, no solo al audio. El audio certifica que la medición ocurrió; el grafo de derivaciones certifica que la conclusión se sigue de la medición.

**Precondiciones: en buena parte ya las tenés gratis.** En Luthier la precondición la garantiza el tipo del argumento. Acá el argumento es una referencia a un objeto almacenado que tiene tipo, así que la precondición se verifica al formar la referencia. `localizar` toma un conjunto de registros alineados más una geometría estimada, y no podés ni construir la llamada si esos objetos no existen. Precondición como clave foránea.

Lo que no sale gratis son las precondiciones que son predicados sobre valores: que el arreglo tenga al menos cuatro micrófonos, que la alineación haya convergido, que la geometría no esté mal condicionada. Ahí necesitás tipos refinados, y la consecuencia práctica es buena: `geometría bien condicionada` es un tipo distinto de `geometría`, y quién habita cuál se decide al momento de crear. Con eso una función que falla su postcondición no produce un resultado malo, produce un objeto de tipo `intento fallido`, que igual guardás, porque un fracaso también es evidencia. Tu 03b con dos parlantes es justo eso: no es un agujero en la base, es un objeto de ese tipo, con sus entradas y su diagnóstico.

**Postcondiciones: ya tenés el verificador construido y creo que no lo estás viendo como tal.** Luthier verifica postcondiciones muestreando entradas posibles. Tu muestreador es `synth`, el generador sintético, el instrumento que mide al instrumento. Y la postcondición de una función de localización no es "devuelve un número", es una afirmación sobre cobertura: la región al noventa y cinco por ciento contiene la verdad el noventa y cinco por ciento de las veces sobre entradas sintéticas. O sea que la verificación de postcondiciones y la calibración de cobertura son el mismo cómputo. Lo que ya pensaste como módulo `coverage` es el compilador de Luthier corriendo sobre tu función.

**Y eso justifica tu tabla de funciones**, que es la parte donde tu intuición va más rápido que la pregunta que hiciste. Lo que Luthier te da que ningún esquema de procedencia común te da es implementaciones múltiples del mismo tipo de función, comparadas por desempeño documentado. Vos tenés ese caso servido: apareo de picos contra verosimilitud completa, una fuente contra dos, PHAT contra el pesado óptimo. Todas son implementaciones de la misma firma. La tabla de funciones entonces lleva firma, implementación, versión, registro de verificación y registro de desempeño. Y la pregunta "cuál uso" deja de ser una decisión que alguien recuerda y pasa a ser una consulta.

**Ahora la pregunta concreta: campos fijos.** La tentación del JSON sin esquema viene de que cada análisis devuelve cosas distintas, pero eso es precisamente lo que resuelve un sistema de tipos, y renunciar ahí es renunciar a Luthier justo en el punto donde te sirve. Cada función declara su tipo de resultado, con campos fijos. El conjunto de tipos de resultado es abierto, vos agregás tipos nuevos cuando se te ocurre un análisis nuevo, pero cada tipo individual es cerrado. Eso es una suma de tipos, no un blob.

Lo mismo con los parámetros, que es donde más va a tirar el JSON: cada función declara su tipo de parámetros, campos fijos. Si los metés como JSON opaco, el día que quieras preguntar "todas las corridas con umbral mayor que tal" para comparar dos implementaciones, no podés, y comparar implementaciones era el punto.

La objeción real al esquema fijo es que durante la exploración cada análisis nuevo te pide una migración, y eso duele. La salida es no escribir el esquema a mano: **el esquema se genera desde el tipo declarado de la función.** Declarás el tipo en el código, la tabla sale de ahí. Agregar un análisis es agregar un tipo, y la migración es derivada. Es el movimiento de Luthier aplicado al almacenamiento, el esquema como proyección del sistema de tipos y no como un artefacto separado que hay que mantener sincronizado.

JSON está bien como formato de serialización de un valor tipado. Lo que hay que rechazar es JSON como "no tengo campos fijos".

**Una advertencia sobre el trasplante.** Luthier verifica en un mundo cerrado, en tiempo de compilación. Tus datos de campo son un mundo abierto que sigue llegando, y la realidad puede violar un invariante: un celular con el reloj roto, un micrófono saturado, un registro con la mitad del audio. Ahí la idea de clase como tupla de tipos que cumplen invariantes, todos fallan o todos pasan juntos, no se transfiere tal cual. Yo lo partiría así: sobre objetos derivados los invariantes se exigen al crear, porque vos controlás el cómputo; sobre objetos observados los invariantes son validaciones que producen un veredicto, nunca un rechazo. Si la elegancia del sistema de pruebas te hace tirar datos feos, perdiste campo, y el campo no se repite.

## 10. Luciano  2026-09-13 12:09:23 UTC  (line 89)

Pensemos de forma pragmatica: 
Hay tipos "originales" que se generan mediante la combinacion de audios y questionarios. 
Todos los otros tipos son derivativos, de modo que tienen necesariamente estructura.

## 11. Model  2026-09-13 12:10:12 UTC  (line 94)

De acuerdo con el corte, y lo mejor que tiene es lo que implica: si todo derivado tiene la misma estructura forzada, el trabajo de diseño está solamente en los originales. El resto es una sola forma, escrita una vez.

**La forma única del derivado.** Concreta, estos campos y nada más:

```
id
entradas          (ids de los objetos inmediatos, con su tipo)
funcion           (id en la tabla de funciones, con versión)
parametros        (tipado, según la firma de esa función)
resultado         (tipado, según la firma de esa función)
estado            (produjo resultado / falló, con diagnóstico)
cuando            (momento del cómputo, no del campo)
```

Lo único que varía entre derivados es el tipo de `parametros` y el de `resultado`, y los dos los declara la función. O sea que agregar un análisis nuevo es declarar un par de tipos, no diseñar una tabla.

**Los originales son dos formas, no muchas.** Esto es lo que me parece más útil de tu corte, porque "audios y cuestionarios" se generaliza limpio:

*Captura de aparato*: un instrumento registró algo, con lo que el instrumento sabía en ese momento. Ahí entra el audio, pero también la emisión (este celular emitió este chirp a este tiempo local, que en tu protocolo es un dato central y no es audio grabado), el GPS, y cualquier sensor. Campos: qué aparato, qué firmware, reloj local, el contenido, y el hash del contenido.

*Afirmación humana*: una persona afirmó algo en tal momento. Ahí entra todo lo que venga de formulario, y son más cosas de las que parece:

- montaje: el aparato X estuvo sobre el marcador M entre t1 y t2
- medición de distancia: entre el marcador A y el B, tanto, con este instrumento y esta técnica
- inventario: este aparato es tal modelo, número de serie tal
- condiciones: temperatura, humedad, viento, lluvia, sustrato
- observación biológica: vi o escuché tal cosa

Las dos formas son inmutables, las dos llevan cuándo y quién o qué las produjo.

**Los formularios tienen versión, igual que las funciones.** Vas a cambiar el cuestionario, es inevitable, y una respuesta sin saber a qué versión del formulario contestaba es basura en tres meses. O sea que la definición del formulario es un objeto almacenado, hermano de la tabla de funciones. Y ahí aparece la unificación que hace que todo esto sea un solo mecanismo y no tres: **cada fila dice qué la produjo.** Para un audio, un aparato más su firmware. Para una respuesta, un formulario más una persona. Para un derivado, una función más sus parámetros. Misma columna, tres clases de productor, y todos versionados.

**Una que se te va a colar si no la ponés en los originales ahora: la temperatura.** La velocidad del sonido cambia alrededor de 0,6 m/s por grado, o sea 0,17% por grado. En treinta metros eso son centímetros, y vos estás validando a 2,79 y 3,2 cm. La temperatura es un dato original de primera clase, y si no tiene lugar en el esquema va a terminar como un 343 escrito adentro de un script, que es justo lo que no querés. Puede venir de formulario o de sensor, y por suerte las dos opciones ya tienen forma en el esquema de arriba.

Si querés escribo esto como reemplazo de tu archivo, en el mismo formato de lista que venías usando, para que lo sigas editando vos.

## 12. Luciano  2026-09-13 12:10:12 UTC  (line 96)

por derivativos digo, resultado de funciones

## 13. Model  2026-09-13 12:10:39 UTC  (line 103)

Sí, eso es lo que entendí y está bien cerrado así. Dos consecuencias que sí muerden.

**Las anotaciones humanas son originales, no derivados.** Si derivado significa resultado de función, entonces "esta detección es espuria", "esto es Hypsiboas", "este registro salió mal, descartar" no tienen lugar en la capa derivada. Y no hay que forzarlos: son afirmaciones humanas, entran como originales, con su autor y su momento. La consecuencia práctica es la que importa: **nunca se edita un objeto derivado.** Si una localización está mal, no se corrige, se agrega una afirmación humana que dice que está mal, y esa afirmación es entrada de la función siguiente. Así las etiquetas de entrenamiento, el control de calidad y las correcciones caen todas en el mismo lugar y ninguna ensucia el grafo.

**Función quiere decir determinista, y eso tiene costo.** Si la identidad es (entradas, función, versión, parámetros) entonces las mismas entradas tienen que dar el mismo resultado, o el hash como clave no sirve y el certificado miente. Eso obliga a que la semilla sea parámetro explícito en todo lo que sortea: inicializaciones, MCMC, bootstrap, y el sorteo de posiciones que ya tenés. Y obliga a que nada se lea del ambiente por la ventana: ni la hora actual, ni una ruta de archivo, ni una variable de entorno, ni un valor de configuración que no esté declarado. Todo lo de afuera entra como argumento. Es la misma regla que ya tenés de no hardcodear, pero ahora con una razón más fuerte que la prolijidad: sin eso el objeto derivado no es un certificado de nada.

Con esas dos, el mundo queda cerrado: toda hoja del grafo es un original (captura de aparato o afirmación humana) y todo nodo interno es un resultado de función. No queda nada flotando, y de cualquier conclusión podés bajar hasta los originales que la sostienen.

## 14. Luciano  2026-09-13 12:12:35 UTC  (line 106)

estuve soñando acerca del viento, cambia la velocidad del sonido o lo su transmicion?

## 15. Model  2026-09-13 12:13:46 UTC  (line 110)

El viento no cambia la velocidad del sonido. Cambia el medio de lugar. Esa distinción es la que resuelve tu pregunta, y tiene consecuencias muy concretas para tu arreglo.

**Lo que fija la velocidad es la temperatura.**

$$c(T) = 331{,}3\sqrt{1 + T/273{,}15} \approx 331{,}3 + 0{,}606\,T$$

donde $c$ es la velocidad del sonido en aire en metros por segundo, $T$ es la temperatura en grados Celsius, y $331{,}3$ es la velocidad a cero grados. La humedad agrega algo, del orden de 0,1 a 0,3 por ciento en aire cálido y saturado. El viento no entra en esta fórmula en absoluto.

**Lo que hace el viento es advección.** En el marco del aire el sonido siempre viaja a $c$. Pero el aire se mueve respecto del suelo, y tus micrófonos están clavados al suelo. Entonces la velocidad efectiva a lo largo de un rayo es

$$c_{\text{ef}} = c + \vec{u}\cdot\hat{n}$$

donde $c_{\text{ef}}$ es la velocidad efectiva de propagación vista desde el suelo en metros por segundo, $c$ es la velocidad del sonido en el aire quieto de la fórmula anterior, $\vec{u}$ es el vector velocidad del viento en metros por segundo, $\hat{n}$ es el versor que apunta de la fuente al receptor, y el punto es producto escalar. O sea que solo cuenta la componente del viento a lo largo del camino: viento cruzado perpendicular al rayo no hace casi nada a primer orden, viento a favor acelera, viento en contra frena.

Con dos metros por segundo, que es una brisa suave que ni notás, $\vec{u}\cdot\hat{n}/c$ vale 0,58 por ciento. Sobre treinta metros eso son 0,5 milisegundos de tiempo de vuelo, que en distancia equivalente son diecisiete centímetros. Vos estás validando a 2,79 centímetros.

**Y acá está lo que te va a doler: el viento rompe la reciprocidad.** Tu calibración se apoya en que ida y vuelta tardan lo mismo, y con viento no tardan lo mismo:

$$t_{AB} = \frac{d}{c + \vec{u}\cdot\hat{n}}, \qquad t_{BA} = \frac{d}{c - \vec{u}\cdot\hat{n}}$$

donde $t_{AB}$ es el tiempo de vuelo en segundos de A a B, $t_{BA}$ el de B a A, $d$ la distancia entre A y B en metros, $c$ la velocidad del sonido en aire quieto, $\vec{u}$ el vector viento y $\hat{n}$ el versor de A hacia B. La diferencia vale

$$t_{BA} - t_{AB} \approx \frac{2\,d\,(\vec{u}\cdot\hat{n})}{c^2}$$

con los mismos símbolos. Para treinta metros y dos metros por segundo a favor del camino, eso da un milisegundo. Es enorme comparado con tu precisión.

**Pero la misma ecuación te regala la solución.** Si medís los dos sentidos, la suma es

$$t_{AB} + t_{BA} \approx \frac{2d}{c}\left(1 + \frac{(\vec{u}\cdot\hat{n})^2}{c^2}\right)$$

mismos símbolos. El término de viento entra al cuadrado, o sea 0,0034 por ciento con esa brisa, tres microsegundos sobre treinta metros, un milímetro. **La ida y vuelta te da la distancia inmune al viento a segundo orden, y la diferencia te da la componente del viento sobre ese camino.** Eso es exactamente cómo funciona un anemómetro sónico comercial. Tu calibración recíproca, hecha en los dos sentidos, te mide el viento gratis, con la resolución de tu propio arreglo y sobre los caminos que realmente te importan. No necesitás un anemómetro aparte, y el que comprarías mediría el viento en un punto, que no es el que te afecta.

**Después hay dos efectos más, que no son advección.**

*Refracción por cizalladura.* El viento no es uniforme, crece con la altura de forma aproximadamente logarítmica cerca del suelo. Eso hace que los rayos se curven: a favor del viento se curvan hacia abajo y el sonido llega más lejos, en contra se curvan hacia arriba y aparece una zona de sombra. Es la razón física de que escuches mejor a favor del viento, y no tiene nada que ver con que el sonido "vaya más rápido". Para tu arreglo, con aperturas de metros y fuentes cerca del suelo, es un efecto de segundo orden, pero deja de serlo si querés localizar bichos a cincuenta o cien metros.

*Turbulencia.* Este es el que te va a limitar de verdad. El viento es turbulento, y los remolinos hacen fluctuar el índice efectivo a lo largo del camino, lo que produce fluctuaciones aleatorias de fase y amplitud. El efecto sobre vos no es sesgo, es pérdida de coherencia entre micrófonos, y la pérdida de coherencia es justo lo que degrada el GCC. Crece con la distancia, con la frecuencia y con la intensidad de la turbulencia. Y no se corrige, porque no es un parámetro que puedas estimar y restar: es ruido. Lo que sí podés es que aparezca en tu modelo donde corresponde, inflando $N(f)$, que es el ruido que ya tenés en la verosimilitud. Un día ventoso no te sesga la localización, te ensancha la región, y está bien que así sea.

*Y el cuarto, que es el que arruina sesiones de campo en la práctica:* el viento pegando en la cápsula genera ruido que no es acústico, es presión turbulenta sobre el diafragma. Es de baja frecuencia, casi todo por debajo de unos pocos cientos de hercios, y es brutalmente fuerte. Los cantos de rana están típicamente entre uno y cinco kilohercios, así que un pasaalto te salva bastante, pero necesitás peludos en los micrófonos igual, porque si te satura la entrada el pasaalto llega tarde.

**Para el esquema:** temperatura es escalar, viento es vector y además tiene curso temporal, así que no es un campo de formulario, es una serie. Y la conclusión práctica es linda: el viento no hay que medirlo aparte, hay que medirlo con el propio arreglo, haciendo los chirps de calibración en los dos sentidos. Eso convierte un dato ambiental molesto en un derivado más, con sus entradas y su incertidumbre, estimado exactamente sobre los caminos donde importa.

## 16. Luciano  2026-09-14 00:07:20 UTC  (line 113)

Idle 11h 51m. The prompt cache has likely expired, so your next message will re-cache about 69k tokens.
explain this message

## 17. Model  2026-09-14 00:07:54 UTC  (line 129)

Es un aviso del harness sobre costo y latencia, no sobre el estado de la conversación.

La API de Anthropic guarda del lado del servidor el prefijo de la conversación (el prompt de sistema, tus instrucciones globales, el índice de memoria, todo nuestro intercambio, las salidas de las herramientas). Como la API es sin estado, cada turno le manda de nuevo la conversación entera. El caché evita que la tenga que volver a procesar: si el prefijo coincide byte a byte con lo guardado, se lee del caché en vez de recomputarse.

Ese caché tiene vencimiento. Esta sesión usa el de una hora, y estuvo quieta once horas y media, así que venció. En el próximo pedido se reprocesan los 69 mil tokens desde cero y se vuelven a escribir al caché.

Lo que cuesta, con números: leer del caché sale alrededor del 10 por ciento del precio del token de entrada, escribirlo sale alrededor del doble con vencimiento de una hora. A 5 dólares por millón de tokens de entrada, esos 69 mil son unos 3,5 centavos si salían del caché y unos 70 centavos ahora que hay que reescribirlos. Una vez sola, y después vuelve a estar caliente mientras sigamos hablando. También tarda un poco más en empezar a responder.

Lo que no significa: no se perdió nada. El caché no es la memoria de la conversación, es solo una optimización de cómputo. Todo lo que hablamos del esquema, de Luthier y del viento sigue igual de presente. Lo único que cambió es que este turno se paga a precio completo en vez de a precio de caché.
