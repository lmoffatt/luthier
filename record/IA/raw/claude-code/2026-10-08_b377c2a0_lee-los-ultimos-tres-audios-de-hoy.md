---
source: claude-code
account: 
id: b377c2a0-a7e1-46a8-a928-4a6d17a27aa1
title: "lee los ultimos tres audios de hoy"
started: 2026-10-08T10:44:05Z
ended: 2026-10-09T00:39:49Z
offset: 
turns: 40
cwd: -home-lmoffatt-Projects-luthier
exports: 20261009
flags: 
origin:
  - raw/claude-code/20261009/-home-lmoffatt-Projects-luthier/b377c2a0-a7e1-46a8-a928-4a6d17a27aa1.57a4cdf8.jsonl.gz sha256 57a4cdf832f2b9b6c9cd4e0fadd140c4080947b8cfa92c8da5fcfaa9f8667a8a
iachat: 1
---

# lee los ultimos tres audios de hoy

## 1. Luciano  2026-10-08 10:44:05 UTC  (line 3)

lee los ultimos tres audios de hoy

## 2. Model  2026-10-08 10:44:09 UTC  (lines 23, 34, 44, 58)

Leo las tres transcripciones nuevas de hoy.

Para ubicar lo nuevo respecto de lo ya registrado, miro las decisiones de hoy y el diff del documento de GPT.

Leo el resto de la devolución de GPT, que toca lo mismo que el audio largo, y dejo commiteados los tres audios y el documento de GPT tal como están.

Leí los tres audios y los dejé commiteados verbatim junto con la segunda devolución de GPT (1749863).

Lo que dicen, en orden. El largo (33 min) arranca conforme con el documento de elementos: categorías cartesianas cerradas más tipos dependientes más predicados sobre tipos, que son las leyes. De ahí pasa a la pregunta central, cómo se sabe que un valor pertenece a un tipo: por construcción, o por hipótesis cuando hay que probarlo, y para funciones solo se puede probar en una muestra. Ahí entra la probabilidad y aparece lo nuevo: el tipo se parametriza con un uso, que es un prior sobre las combinaciones de parámetros y un costo de falla que depende de la situación y del grado del error. Vos mismo separás dos cosas: muestrear donde el costo es alto y muestrear donde es probable que falle, y decís que una política de test combina las dos. A la caracterización de una implementación le agregás el tiempo de cómputo, y cerrás con que todas las implementaciones que resuelven el mismo problema son valores del mismo tipo de función, y uno elige por pérdida esperada y velocidad. Después, el paso más fuerte: las leyes podrían ir del tipo a un costo en vez de a Bool, graduadas, sin cota, costo y no beneficio, algo como un likelihood no normalizado. Entre medio, el mundo exterior: archivos (ejecutables, código Python, datos, plots, sensores), memoria mutable, recursos y procesadores, y una pregunta explícita para la guía sobre si hay alguna abstracción que no sea un file. Luego tipos declarados antes de definidos (hace falta para recursión) y la regla de que no se le da valor a un tipo sin definición. Y la última media: el intérprete escrito en Luthier, con las distintas estrategias de evaluación (consumir símbolos, guardar 2 + 2 e interpretarlo después, A vale 2+2 o vale 4) como cosas que se puedan escribir, el estado de la memoria paso a paso como traza universal, y las leyes de cada paso del reduce y apply escritas en Luthier. Terminás con que todo cálculo en Luthier tendría un posterior, que las evidencias de distintas corridas se pueden unir, y que conviene guardar como testigos los valores sorpresivos respecto del prior, con esos análisis como capas opcionales que corren a veces.

Los cortos reencuadran: tipos y leyes son el Luthier declarativo; los valores son el Luthier ejecutivo, interno o externo; falta un Luthier declarativo de la implementación (cómo el código se vuelve ejecución) y modos de evaluación (con test, con test extensivo, con copia de todo). El último: escribir las especificaciones de Luthier en Luthier.

Qué es nuevo respecto del registro. Lo del intérprete en Luthier ya es D-2026-10-08-c (la lista de elementos escrita para enunciar el intérprete de Luthier en Luthier), y el audio lo extiende de intérprete a especificación; el marco declarativo/ejecutivo coincide con D-2026-10-08-b (plan atemporal, ejecución temporal), solo que con nombres mejores. Lo que no está en ninguna decisión son tres cosas: el uso como prior más costo más tiempo de cómputo, la ley como costo, y los testigos por sorpresa. Sobre el uso, el audio y GPT llegan a lo mismo por separado, y los dos me corrigen en el mismo punto: yo había metido el generador adentro del uso, y vos distinguís buscar donde falla de pesar donde cuesta, que es exactamente la separación Use / TestPlan de GPT. La concedo.

Sobre la pregunta para la guía: a nivel sistema operativo casi todo es un file descriptor (sockets, pipes, dispositivos, /dev/urandom). Lo que no entra como archivo son el tiempo, la memoria y los procesadores, que son recursos que se piden y se devuelven, y la concurrencia. Lo que vos listás (files, memoria, recursos, procesadores) es la lista completa que yo conozco; nada que agregar salvo el reloj.

Una pregunta, la que cambia los elementos. Vos proponés que la ley devuelva un costo; GPT propone tres piezas: la ley computa una discrepancia, la teoría le pone un umbral (Bool) y el uso le pone un costo. Mi recomendación es la de GPT, por una razón que vos mismo diste: querés que la misma ley cueste distinto según la situación, y si el costo está en la ley, la teoría pasa a depender del uso. Con la discrepancia como invariante (P10, el objeto que mejor representa el concepto es el invariante de su tipo), Bool y costo son dos lecturas de ella y la teoría queda independiente. Toca P11 (todo criterio es parámetro) a favor y supone que toda ley tiene una discrepancia natural, que para leyes puramente lógicas es 0 o 1. ¿La ley devuelve discrepancia, con umbral en la teoría y costo en el uso, o devuelve costo directamente?

Decisión mía: commitear los tres audios y la devolución de GPT verbatim. Nada más tocado.

## 3. Luciano  2026-10-08 12:16:54 UTC  (line 63)

analisis de las nueva vision: que cambios sugiere en la documentacion

## 4. Luciano  2026-10-08 12:22:42 UTC  (line 71)

analisis de las nueva vision: que cambios sugiere en la documentacion

## 5. Luciano  2026-10-08 12:22:57 UTC  (line 79)

analisis de las nueva vision: que cambios sugiere en la documentacion

## 6. Model  2026-10-08 12:23:06 UTC  (lines 84, 116)

Para mapear la visión nueva sobre lo que hay, miro la estructura de docs y el documento de elementos.

Análisis, documento por documento. La visión nueva tiene cinco piezas: Luthier declarativo (tipos y leyes) contra Luthier ejecutivo (valores, internos o externos); el uso como prior más costo, con el tiempo de cómputo; la ley graduada; el posterior sobre todo cálculo, con evidencia que se une entre corridas y testigos guardados por sorpresa; y la especificación de Luthier escrita en Luthier, con las estrategias de evaluación como cosas que se escriben. Lo que cada una toca:

En 00 (elementos), el párrafo de marco se reescribe con tus nombres, declarativo y ejecutivo, en vez de plan y ejecución; los nombres actuales son míos. Eso trae una tensión con la lista: vos ponés los valores del lado ejecutivo, y hoy "Value, the model" está en el plan. Leído con *Declared, defined, computable*, tu corte es más limpio: declarativo es lo que se declara y se define por leyes (tipo, formadores, ley, teoría, hueco, recursión); ejecutivo es dar un cuerpo (valor, extern, apply y reduce) y correrlo. Es el cambio que mueve elementos de grupo, y no es mío.

Al plan le entran dos elementos. Uso: una distribución sobre las entradas, una pérdida sobre lo que la ley deja, un criterio de decisión. Plan de test: generador de búsqueda, estrategia, presupuesto, semilla, regla de parada. Vos los separás en el audio (buscar donde falla, pesar donde cuesta) y GPT también, así que retiro mi fusión del lunes. El plan de test ya existe casi entero: es 08 §1 a §7 sin nombre, y la métrica `cost` de `sampled m` es la semilla de la búsqueda pesada por costo. El uso es nuevo. En el elemento Valor se agrega lo que dijiste: todas las implementaciones de un problema son valores del mismo tipo, y entre ellas elige la pérdida esperada bajo un uso y el tiempo; Realization ya dice la mitad (los costos medidos eligen).

El elemento Ley cambia según tu respuesta a la pregunta de ayer, que sigue pendiente: si devuelve discrepancia, con umbral en la teoría y costo en el uso, cambia el bullet de 00 y el tipo `Law` de 04 §3; si devuelve costo, cambia también la teoría, que pasa a depender del uso.

En la ejecución, *Execution and trace* suma dos cosas: la secuencia de estados de memoria (2, 2+, 2+2, 4) como la traza universal, y la estrategia de evaluación (consumir, guardar la expresión, sustituir después) como un valor del plan, parámetro y no constante (P11). Y los modos de ejecución que pediste en el audio corto (eval, eval con test, con test extensivo, con copia de todo) son definiciones en Luthier sobre `Program`, no cosas del host; van en *The executable kernel* como lo que el host no hace. La sección 5 se extiende de "el intérprete en Luthier" a "la especificación de Luthier en Luthier": las leyes de cada paso de apply y reduce escritas como leyes, que es lo que falta para que el host sea una realización certificable de verdad. §6 tiene una frase que ahora choca: "probabilidad, creencias: librerías", cuando el certificado pasa a ser un posterior. Se concilia diciendo que el tester que usa esa librería es una definición en Luthier, y el núcleo sigue sin probabilidad.

En *What is known* el certificado se parte en dos: conocimiento, el posterior sobre la conducta de un modelo dado prior, clase de modelo y evidencia, que se une entre corridas; y certificado, una decisión para un uso, consulta sobre ese conocimiento. Es lo que hace posible "check once" entre usos sin volver a correr. Se agregan los testigos: la entrada guarda los casos sorpresivos bajo el prior, no los primeros n como hoy, con el criterio de sorpresa como parámetro, y los análisis como capas que corren a veces, con su propio costo declarado.

En 05 §7 la tabla de grados recibe la lectura bayesiana: sampled n es un posterior bajo un prior y una clase de modelo; assumed es condicionar, no probabilidad 1 (corrección de GPT que acepto); el eslabón más débil se vuelve cota de unión. La entrada registra uso, prior, clase de modelo y regla de parada, por reproducibilidad aunque la inferencia no la necesite. El tiempo por ley ya se registra desde el 6; es el costo de cómputo que pedís, ya está.

En 08, una sección Uso con la regla de transferencia entre usos, y §10 (leyes estadísticas con nivel α) queda marcada para reformular en el marco bayesiano, como D-2026-10-08-a ya anota sobre D-2026-10-06-z.

En 09, tu inventario del mundo (archivos, memoria, recursos, procesadores, sensores que son archivos) confirma la decisión 3 (File primero) y agrega algo que 09 no tiene: memoria y procesadores no son punteros que se leen sino recursos que se piden y devuelven; va a §12 abierto.

Haría falta un rationale nuevo, 10, con la cadena GPT, mi devolución, GPT y los audios, porque D-2026-10-08-a dice que la lectura bayesiana no está ni en 05 ni en 09, y ahí va la matemática (θ, Beta, cota de unión, transferencia, jerarquía de modelos de q(x)) con lo propuesto separado de lo tuyo. En principles, el audio es fuente directa de P14 propuesto (no se da valor a un tipo sin definición); se cita. Y en decisions quedan cuatro candidatas por loguear cuando las tomes: uso y plan de test como elementos, la ley graduada, conocimiento contra certificado, y el reagrupamiento declarativo/ejecutivo.

La pregunta de hoy, la que mueve la lista: ¿los valores y apply/reduce pasan al lado ejecutivo, dejando en el declarativo solo tipos, leyes, teorías, huecos y recursión? Mi recomendación es sí, porque coincide con el eje declarado/definido/computable que ya está en el documento.

No toqué ningún archivo.

## 7. Luciano  2026-10-08 13:07:06 UTC  (line 124)

como es la forma estandard de ejecutar un programa en Lisp y en otros lenguajes de programacion (por apply/reduce)

## 8. Model  2026-10-08 13:08:02 UTC  (line 128)

La forma estándar en Lisp es el par eval/apply de McCarthy (1960), que SICP escribe en una página como evaluador metacircular. Primero `read` convierte el texto en datos, listas: `(+ 2 2)` es una lista de tres símbolos. Después `eval(exp, env)` hace un `case` sobre la forma de la expresión: un número se devuelve a sí mismo; un símbolo se busca en el entorno, que es una tabla mutable de nombres a valores; las formas especiales (`quote`, `if`, `lambda`, `define`) se tratan aparte; y una aplicación `(f a b)` evalúa `f`, evalúa los argumentos, y llama a `apply(proc, args)`. `apply` distingue dos casos: si `proc` es primitiva, la aplica el host; si es una clausura (lambda más entorno), extiende el entorno ligando parámetros a argumentos y evalúa el cuerpo ahí. Eso es todo el intérprete, y es recursivo mutuo: eval llama a apply, apply llama a eval. Tu pregunta de "A vale 2+2 o vale 4" tiene respuesta fija en Lisp: `(define a (+ 2 2))` evalúa los argumentos antes (orden aplicativo) y liga `a` a 4. Guardar la expresión se hace explícitamente con `(define a '(+ 2 2))`, y después `(eval a)`. Las macros son la tercera pieza: una pasada que reescribe datos en datos antes de eval.

Visto desde el cálculo lambda, ejecutar es reducir: aplicar beta, `(\x.t) a → t[a/x]`, hasta forma normal. Church-Rosser dice que si dos órdenes terminan dan lo mismo, así que el orden es una estrategia, parámetro y no verdad. Orden aplicativo (argumentos primero: Lisp, ML, Python, C) es el que puede no terminar donde otro sí. Orden normal (el redex más a la izquierda y afuera) termina siempre que algo termine. Call by need (Haskell) es orden normal con sharing: `a = 2 + 2` guarda un thunk, se evalúa la primera vez que alguien lo pide, y el thunk se sobreescribe con 4. Tu "2+" intermedio, el más ya lleno con un 2, es exactamente una aplicación parcial, currificación. Y el `do` de Haskell es lo que sospechabas: azúcar sobre `>>=`, cada paso es una función del resultado del anterior, o sea secuencia como dependencia de datos; no hace falta una primitiva de "después".

Los lenguajes imperativos no reducen términos sino que avanzan un estado de máquina. Python parsea a un AST, compila a bytecode, y una máquina de pila lo ejecuta: para `a = 2 + 2` emite `LOAD_CONST 2`, `LOAD_CONST 2`, `BINARY_ADD`, `STORE_NAME a`, que es literalmente tu traza 2, 2 2, 4, guardado. C compila a código máquina y el estado es registros, pila y heap. Forth es tu primera estrategia pura: consume símbolos de izquierda a derecha sobre una pila, `2 2 +` deja 4, sin árbol intermedio. Prolog ejecuta por unificación y resolución, otra familia. Las planillas y los lenguajes de dataflow evalúan por el grafo de dependencias, que es tu "el orden lo da quién depende de quién".

La forma estándar de escribir las leyes de cada paso, que es lo que querés para Luthier, es la semántica operacional. Small-step: una relación `t → t'` entre términos, una regla por forma (beta, unfolding de un nombre, elección de rama de `match`), y la ejecución es la clausura transitiva; cada paso es un estado y la secuencia es la traza. Big-step: un juicio `t ⇓ v`, que es eval visto como relación. Entre las dos están las máquinas abstractas, que hacen el estado explícito: SECD de Landin, CEK (control, entorno, continuación) para orden aplicativo, Krivine para call by name. Una máquina abstracta es un intérprete cuyo estado es un dato, y por eso es la forma más cómoda de certificar un intérprete contra otro: se comparan estados paso a paso, no solo resultados.

Lo que pedís al final, que la misma expresión `A + B` se calcule con números o con números con error, es el AST como dato y cada evaluador como un fold sobre él (en Haskell lo llaman tagless final o álgebra inicial). Es la misma idea del documento: `Term` como `data`, y eval, eval con test, eval con intervalos, cada uno una función de `Term` a un tipo distinto, certificadas contra las mismas leyes de reducción. Lo que hace tu intérprete de C++ con clases virtuales es esto mismo, con el fold repartido en métodos.

## 9. Luciano  2026-10-08 13:22:51 UTC  (line 132)

bien, entonces que cambios habria que hacer en el documento 00?

## 10. Model  2026-10-08 13:23:35 UTC  (line 136)

Los cambios a 00, en el orden del documento. Marco cuál depende de una respuesta tuya pendiente.

Párrafo de marco. Reemplazar plan y ejecución por tus nombres: Luthier declarativo (lo que se declara y se define por leyes, atemporal) y Luthier ejecutivo (dar un cuerpo y correrlo, interno o externo, temporal). Citar los audios de hoy 18:37 y 18:41. Agregar la frase de que el conocimiento entre los dos es un posterior, que ya está, y que la especificación entera de Luthier, no solo el intérprete, se escribe en Luthier.

La lista del declarativo. Depende de tu respuesta a la pregunta de ayer: si los valores pasan al ejecutivo, quedan Type, Product/sum/exponential, Dependent type, Law, Subtype by law, Declaration, Recursion, Program; y Value y Apply and reduce se mudan. Si no, la lista queda como está y solo cambian los bullets de abajo.

Law. Depende de la otra pregunta pendiente: discrepancia con umbral, o costo. En cualquiera de los dos, el bullet deja de decir "a term of type Bool" como única forma y dice qué deja una ley al aplicarse a un valor.

Use, bullet nuevo en el declarativo, después de Subtype by law. Una distribución sobre las entradas de una teoría, una pérdida sobre lo que la ley deja, y un criterio de decisión. Lo que hace que una teoría sirva para algo: la misma ley cuesta distinto según el uso. Fuente: audio 18:10 [03:32] a [07:20], y GPT del 8. Test plan, bullet nuevo al lado: generador de búsqueda, estrategia, presupuesto, semilla, regla de parada; es 08 §1 a §7 con nombre, y la métrica `cost` de `sampled` es la búsqueda pesada por costo. Separados porque buscar donde falla y pesar donde cuesta son dos distribuciones (audio [04:15] a [05:30]).

Value, the model. Agregar: todas las implementaciones de un problema son valores del mismo tipo de función, y entre ellas elige la pérdida esperada bajo un uso y el costo medido, tiempo incluido (audio [09:15] a [09:51]).

Apply and reduce. Reescribirlo con lo de hoy: la regla es la relación de un paso, `t → t'`, una regla por forma (beta, unfolding, rama de `match`); la ejecución es su clausura; la estrategia (aplicativo, normal, por necesidad con sharing) es un parámetro, no una verdad, porque Church-Rosser dice que el resultado no depende de ella cuando termina. Citar que `A := 2 + 2` guarda un término y reduce cuando se pide; que guardar la expresión y evaluarla distinto después es un fold sobre `Term` (audio [22:52] a [27:12]).

Execution and trace. Agregar que la traza universal es la secuencia de estados de la máquina, cada paso un estado (los 2, 2+, 2+2, 4 del audio [26:23]), y que los modos de ejecución (eval, eval con test, con test extensivo, con copia de todo) son definiciones sobre `Program`, cada una un fold distinto sobre el mismo término (audio 18:37 [01:01]).

What is known. Partir Certificate en dos bullets. Knowledge: el posterior sobre la conducta de un modelo, dados prior, clase de modelo y evidencia; se une entre corridas; guarda como testigos los casos sorpresivos bajo el prior, con el criterio de sorpresa como parámetro (audio [31:08] a [32:39]). Certificate: una decisión para un uso, consulta sobre ese conocimiento; se transfiere entre usos cuando uno acota al otro. Assumed es condicionar, no probabilidad 1.

The executable kernel. Decir que el host es una máquina abstracta cuyo estado es un dato (CEK o similar), para que el intérprete en Luthier se certifique contra él estado por estado y no solo por resultados. Agregar a lo que el host no hace: los modos de evaluación y el tester.

Sección 5, el programa como dato. Ampliar de "el intérprete" a "la especificación de Luthier en Luthier": las leyes de cada paso de reducción como leyes de Luthier, y un Luthier declarativo de la implementación, cómo el código se vuelve ejecución (audio 18:37 [00:35]).

Sección 6. Reconciliar "probabilidad, creencias: librerías" con el posterior en el certificado: el núcleo no tiene probabilidad; el tester que la usa es una definición de Luthier.

Sección 7, de dónde viene cada pieza. Agregar McCarthy (eval/apply sobre el programa como dato), Plotkin (semántica operacional de un paso) y Landin (la máquina abstracta con el estado como dato).

Sección 9, abiertos. Agregar: la transferencia entre usos; la jerarquía de modelos de la probabilidad de falla; si memoria y procesadores son punteros o recursos.

Lo que no cambia: Declared, defined, computable (el audio lo confirma y es fuente para P14), What types are for, y la sección 8 ejecutada a mano, que ya es small-step.

Son tres cosas tuyas antes de tocar: valores al ejecutivo, ley como discrepancia o costo, y conocimiento separado de certificado. Lo demás es redacción y cita, y lo puedo aplicar en un commit que se deshace solo.

## 11. Luciano  2026-10-08 13:27:14 UTC  (line 140)

Law deberia ser como un object classifier,  quizas, que puede ser otra cosa que un bool no? podes usar un real como oject classifier?

## 12. Model  2026-10-08 13:28:05 UTC  (line 144)

Sí y no, y el no es preciso. En un topos el clasificador de subobjetos Ω es único salvo isomorfismo, y en Set es 2, el Bool: un subobjeto de X es lo mismo que una flecha X → 2, y la teoría es el pullback de `true`. Un real no puede ocupar ese lugar en Set, porque las flechas X → R son muchas más que los subconjuntos de X; no hay un "true" en R tal que cada sub-objeto sea el pullback de él por una única flecha. Así que si Law es lo que corta un subtipo en el sentido estricto de topos, es Bool y no hay vuelta.

Pero lo que vos llamás object classifier es otra cosa, y es la que te conviene. En teoría de tipos homotópica el object classifier es U, el universo: una flecha A → U clasifica cualquier familia sobre A, no solo las monos. Una ley `L : A → U` da para cada x un tipo, el tipo de la evidencia de que x la cumple, y un certificado es un habitante de `L x`. El Bool es el caso particular en que `L x` es una proposición decidible, habitada o vacía. Con eso una ley y su certificado quedan en el mismo marco que ya tiene el documento: el subtipo es un par dependiente `(x : T) * L x` con la segunda componente borrada del término, que es lo que dice hoy el bullet de Dependent type. Esa es la generalización que no cuesta nada, y es la de Curry-Howard.

Y hay una tercera lectura, que es la que responde a la pregunta de ayer sobre ley como costo, y tiene nombre: Lawvere, 1973, "Metric spaces, generalized logic and closed categories". Lawvere muestra que si uno reemplaza el Bool por el cuantal [0, ∞] con la suma como composición y 0 como verdad, las "categorías enriquecidas" en eso son exactamente los espacios métricos: la verdad es la distancia cero, el "y" es la suma, la desigualdad triangular es la transitividad. Un predicado valuado en [0, ∞] es un costo, un predicado valuado en [0, 1] con el producto es una probabilidad o un conjunto difuso de Goguen. Lo que cambia es Ω, y la condición para que las cosas sigan funcionando es que Ω sea un cuantal: un orden completo con una composición que respeta el orden. Bool, [0, ∞] con +, [0, ∞] con max (el tropical, que es tu eslabón más débil), [0, 1] con producto, son todos cuantales. La cota de unión que te escribí el lunes es la desigualdad triangular de Lawvere.

Con eso la respuesta a P10 queda así: la ley es `L : T → Ω`, con Ω un parámetro que tiene un orden y un elemento "se cumple"; la teoría es el conjunto de subnivel `{ x : T | L x ≤ ε }`, que sí es un pullback, el del umbral; y el Bool es Ω = 2 con ε = true. Ley exacta: Ω = Bool. Ley con tolerancia: Ω = [0, ∞] y el umbral es la tolerancia, en vez de esconder el `<` adentro de la ley. Ley estadística: Ω = [0, 1] y lo que sale es la probabilidad posterior. Y el costo del uso ya no es una tercera pieza separada: es una reponderación del mismo valor en Ω, o un cambio de Ω por una flecha de cuantales.

Lo que no hay que confundir: con Ω = R completo, con negativos, se pierde el orden con mínimo y deja de ser cuantal, y vos mismo lo dijiste en el audio, "costo y no beneficio, sin cota, suena mejor". Eso es exactamente pedir [0, ∞].

Entonces en 00 el bullet Law diría: una función del base del tipo a un objeto de valores de verdad Ω, cuantal, Bool en versión 0 y [0, ∞] para las leyes con tolerancia; la teoría es el subnivel bajo el umbral, que es parámetro (P11). Y como un detalle de armado: la lectura `L : A → U` y la lectura en cuantal son compatibles, porque un tipo con una medida de qué tan habitado está es lo que un cuantal enriquece. ¿Te alcanza con fijar Ω como parámetro del elemento Law y dejar U para la capa de pruebas?

## 13. Luciano  2026-10-08 13:33:46 UTC  (line 152)

entonces los reales positivos sirven como object classifier?

## 14. Model  2026-10-08 13:34:33 UTC  (line 156)

Sirven, en un sentido preciso que conviene tener claro, porque no es el de topos.

Lo que no son: clasificador de subobjetos de Set. Eso es Bool y solo Bool. Una flecha X → [0, ∞] no recorta un subconjunto de X; le asigna a cada x un grado. Hasta que no fijás un umbral ε no hay subconjunto, hay pertenencia graduada.

Lo que sí son: el objeto de valores de verdad de la lógica enriquecida en el cuantal [0, ∞]. En esa lógica los "subobjetos" de X son justamente las funciones X → [0, ∞] (Lawvere los llama espacios métricos generalizados; en la literatura de conjuntos valuados en cuantales, Höhle, Walters, son los Ω-sets con Ω = [0, ∞]). Es decir: hay una categoría, distinta de Set, donde [0, ∞] cumple el papel que Bool cumple en Set, y en esa categoría un predicado es una distancia o un costo y una teoría es un objeto con grados. Para Luthier eso es exactamente "x es un T a costo c" en vez de "x es un T".

Lo que ganás, y conviene mirar la tabla, porque toda la lógica se traduce:

| Bool | [0, ∞], verdad = 0, costo |
|---|---|
| true | 0 |
| false | ∞ |
| p ∧ q | p + q |
| p ⇒ q | q ∸ p (resta truncada) |
| ∀x. p x | sup_x p x (el peor caso) |
| ∃x. p x | inf_x p x |

Dos consecuencias para Luthier salen de ahí sin agregar nada. Primero, el encadenamiento: el costo de `g ∘ f` es la suma, que es la cota de unión y la desigualdad triangular; con max en vez de + tenés el tropical, que es el eslabón más débil de 05 §7. Las dos son cuantales, y cuál usar es un parámetro. Segundo, y esta es la que importa: el "para todo" de una ley en [0, ∞] es un sup, el peor caso, y un sup no se acota desde arriba con una muestra; las muestras lo acotan desde abajo. Esa es la razón matemática de que el test muestreado no certifique una ley universal, y de que haga falta el uso: el uso reemplaza el sup por la integral contra p_U, que sí se estima con muestras. Ley universal y ley bajo un uso son dos cuantificadores distintos sobre el mismo predicado.

Dos condiciones para que funcione. Hace falta el ∞, o sea [0, ∞] cerrado, porque el cuantal tiene que ser un reticulado completo y una falla tiene que poder valer "infinito"; Float64 lo tiene. Y la verdad tiene que ser el mínimo: con negativos algo podría ser "más verdadero que verdadero", y se rompe que `x` esté en la teoría a costo 0 sea el piso. Vos lo dijiste en el audio, costo y no beneficio, sin cota; eso es pedir [0, ∞] y no R.

Entonces, para el bullet Law de 00: `L : T → Ω`, con Ω un cuantal, Bool en versión 0, [0, ∞] para las leyes con tolerancia y costo; la teoría es el subnivel `{ x : T | L x ≤ ε }` con ε parámetro; el universal es el sup y el uso lo cambia por la esperanza. Y el U de HoTT queda para la capa de pruebas, donde la evidencia es un habitante y no un número.

## 15. Luciano  2026-10-08 22:14:21 UTC  (line 160)

o sea que seria una buena extension... Alguien lo uso en programacion?

## 16. Luciano  2026-10-08 22:14:52 UTC  (line 167)

o sea que seria una buena extension... Alguien lo uso en programacion?

## 17. Luciano  2026-10-08 22:27:57 UTC  (line 174)

o sea que seria una buena extension... Alguien lo uso en programacion?

## 18. Model  2026-10-08 22:30:21 UTC  (line 180)

Sí, varias veces y en líneas separadas, y cada pieza tuya tiene un antecedente. Lo que nadie hizo es juntarlas. De memoria, con años aproximados:

Predicados en [0, ∞] como leyes: Kozen (1985) y después McIver y Morgan (2005) reemplazan los predicados de la lógica de Hoare por "expectativas", funciones del estado a [0, ∞], y la precondición más débil pasa a ser una esperanza en vez de un Bool. Kaminski y Katoen (2016) lo usan para tiempo de ejecución esperado. Es exactamente tu ley que devuelve costo, con el "para todo" como sup y el uso como esperanza, y con veinte años de teoría de pruebas encima.

Igualdad con tolerancia: Mardare, Panangaden y Plotkin (2016), "quantitative equational theories": ecuaciones `x =_ε y` con ε ∈ [0, ∞], los axiomas de Lawvere hechos álgebra. Es tu ≡ con tolerancia para los reales, y lo aplican a programas probabilísticos con la métrica de Kantorovich.

La misma expresión evaluada en distintas semánticas: Green, Karvounarakis y Tannen (2007), "provenance semirings". Una consulta de base de datos se evalúa sobre cualquier semianillo: Bool da conjuntos, N da multiconjuntos, el tropical da el camino más barato, [0, 1] con producto da probabilidad. Una sola expresión, un fold por semianillo. Es tu `A + B` calculado con números o con números con error, y la prueba de que la elección de Ω se puede dejar como parámetro sin tocar el programa.

La búsqueda de donde falla: la semántica de robustez de la lógica temporal de señales (Fainekos y Pappas 2009; Donzé y Maler 2010). Una fórmula temporal no devuelve verdadero o falso sino un real, qué tan lejos está de fallar, con ∧ como min y ∀ como inf (el tropical). Y "falsificación" es minimizar esa robustez con un optimizador: el generador buscando donde la ley se rompe. Herramientas S-TaLiRo y Breach, usadas en sistemas ciberfísicos. Y en property-based testing, Löscher y Sagonas (2017), "targeted property-based testing" en PropEr: la propiedad devuelve una utilidad y la búsqueda es recocido simulado sobre ella.

Tipos graduados por un cuantal: Reed y Pierce (2010), Fuzz, tipos de funciones indexados por su sensibilidad en [0, ∞] para privacidad diferencial, el espacio de funciones enriquecido en distancias. Y los sistemas de efectos modernos usan cuantales por nombre: Gordon (2017), "effect quantales"; Mycroft, Orchard y Petricek (2016) sobre efectos y coefectos graduados; Granule e Idris 2 gradúan por un semianillo. Ahí la graduación es sobre el uso de las variables, no sobre la verdad, pero la estructura es la misma.

Restricciones blandas: Bistarelli, Montanari y Rossi (1997), c-semirings: satisfacción de restricciones sobre cualquier semianillo, con fuzzy, pesada y probabilística como casos. Es tu subnivel con ε, en programación por restricciones.

Lo que falta en todos ellos, y es lo que Luthier agrega: ninguno guarda el resultado como conocimiento. Las expectativas de McIver y Morgan se prueban a mano; la falsificación devuelve un contraejemplo y nada si no lo encuentra; el testing dirigido no deja certificado; los semianillos de proveniencia no tienen uso ni prior. La combinación ley en Ω, uso como esperanza, posterior guardado y transferencia entre usos no la vi en ningún lado. Lo que sí sale de esta lista es que cada pieza es terreno conocido, con teoría, así que la extensión es buena y además barata de justificar: en 00, sección 7, van McIver y Morgan, Mardare-Panangaden-Plotkin y los semianillos de proveniencia como de dónde viene la ley graduada.

Dos avisos. Los años y nombres son de memoria, no los verifiqué; si vas a citarlos en un documento, los chequeo. Y la robustez de STL usa (−∞, ∞) con min y max, no [0, ∞] con suma; las dos son cuantales y cuál conviene depende de si querés que los costos se sumen al encadenar o que mande el peor eslabón, que es la elección que ya tenés en 05 §7.

## 19. Luciano  2026-10-08 22:39:22 UTC  (line 191)

verifica toda esta informacion, baja los papers para que vayen en bibliografia

## 20. Model  2026-10-08 22:39:30 UTC  (lines 197, 203, 296, 337, 346, 387, 402, 421, 430, 448, 485)

Primero miro si el repo ya tiene un lugar para bibliografía y cómo se registra una fuente.

No hay bibliografía en el repo todavía. Reviso el remoto (si es público importa para subir PDFs de editoriales) y cargo las herramientas de búsqueda.

Voy por la mitad: verifiqué unas 25 referencias y encontré tres correcciones menores; sigo con las que faltan y después bajo los PDFs.

Verificación casi completa. Ahora bajo los PDFs, cada uno a su propio directorio en el scratchpad, y chequeo que sean el paper correcto antes de copiarlos al repo.

Quince bajaron bien. Fallaron cinco y uno es otro paper de Morgan; pruebo espejos.

Tengo 19 PDFs verificados. Estoy terminando con el libro de HoTT y después armo la bibliografía en el repo.

Verifico en los textos las afirmaciones de contenido que hice, no solo los títulos.

Quedan diez sin PDF libre a la vista. Consulto Unpaywall por DOI para ver si hay copia de acceso abierto.

ACM y Elsevier tienen copias abiertas de cinco. Intento bajarlas.

Todo verificado. Armo la bibliografía en el repo: PDFs, un archivo BibTeX y un índice con procedencia y hash de cada archivo.

Las referencias son reales y las fechas y autores aguantan, salvo nueve detalles que corregí. Quedaron 34 entradas en la bibliografía, con 20 PDFs bajados y 14 que tenés que bajar a mano.

Todo está en [record/bibliography/](record/bibliography/), commit a92c7e6. Hay tres cosas:

- **El BibTeX** con las 34 entradas.
- **Los 20 PDFs** en la carpeta pdf.
- **Un índice** con la URL de origen y el SHA-256 de cada PDF, qué sostiene cada referencia, y las correcciones.

Chequeé cada referencia contra la editorial o la página del autor. Donde tengo el PDF, chequeé también contra el texto las afirmaciones de contenido. Por ejemplo, Lawvere define literalmente [0, ∞] con + como tensor y la resta truncada como hom, Green lista el semianillo tropical y Fuzz usa sensibilidades en R>0 ∪ {∞}.

**Correcciones a lo que te dije:**

1. **Python** pliega `2 + 2` a `4` al compilar. La secuencia de dos cargas y una suma aparece solo con variables, y la instrucción es `BINARY_OP` desde la versión 3.11, no `BINARY_ADD`. Lo verifiqué con `dis`.
2. **Tagless final** es la codificación *final*. El término como `data` con cada evaluador como fold sobre él es la codificación *inicial*. Carette, Kiselyov y Shan contrastan las dos, y yo las mezclé. Para Luthier lo que describí es la inicial.
3. **Mardare, Panangaden y Plotkin** titulan "Quantitative algebraic reasoning". "Quantitative equational theory" es un término de adentro del paper, y el ε es racional.
4. **Green y coautores:** el semianillo en [0, 1] del paper es el difuso, con max y min. La probabilidad entra por tablas de eventos, no con el producto.
5. **Kaminski y coautores** son cuatro autores, no dos.
6. **Los coefectos** son de Petricek, Orchard y Mycroft en 2014. El paper de 2016 es sobre efectos.
7. **"Expectativas"** es el término de McIver y Morgan. Kozen (1985) usa fórmulas con valores reales pero no las llama así.
8. **Bistarelli y coautores:** el resumen nombra restricciones clásicas, difusas, con pesos y parciales. Lo de "probabilística" lo agregué yo y no lo pude confirmar.
9. **S-TaLiRo:** el primer autor se escribe Annapureddy.

**Lo que tenés que bajar vos.** Kozen, Goguen, Fainekos-Pappas, Morgan-McIver-Seidel y Bistarelli están en acceso abierto en Elsevier y ACM, pero esos sitios rechazan descargas por script. Con el navegador salen directo. Löscher-Sagonas, Launchbury, Donzé-Maler y Breach están en ACM o Springer sin copia abierta encontrada, así que van por la biblioteca de la UBA. La copia de S-TaLiRo del autor falló la verificación TLS desde acá y en el navegador abre. Felleisen-Friedman, Höhle, McIver-Morgan y el SICP quedan citados sin PDF. Para sumar uno, lo guardás en la carpeta pdf con su clave como nombre y agregás su fila a la tabla del índice.

**Decisiones mías.** Puse la bibliografía en record/ porque son fuentes. Subí los PDFs a git porque el repo es privado, y pesan 17 MB.

## 21. Luciano  2026-10-08 23:13:05 UTC  (line 489)

dame los links que tengo que bajar asi los bajo de a uno.

## 22. Model  2026-10-08 23:13:30 UTC  (line 493)

Guardá cada uno en `record/bibliography/pdf/` con el nombre de la izquierda. Los cinco primeros son de acceso abierto y deberían bajar directo desde el navegador:

| guardar como | link |
|---|---|
| kozen1985.pdf | https://www.sciencedirect.com/science/article/pii/0022000085900121/pdf |
| goguen1967.pdf | https://www.sciencedirect.com/science/article/pii/0022247X67901898/pdf |
| fainekos2009.pdf | https://www.sciencedirect.com/science/article/pii/S0304397509004149/pdf |
| morgan1996.pdf | https://dl.acm.org/doi/pdf/10.1145/229542.229547 |
| bistarelli1997.pdf | https://dl.acm.org/doi/pdf/10.1145/256303.256306 |
| annapureddy2011.pdf | https://home.cs.colorado.edu/~srirams/papers/sTaliro-tacas11.pdf |

Estos cuatro no tienen copia abierta que yo haya encontrado. Probablemente necesites el acceso de la UBA:

| guardar como | link |
|---|---|
| loscher2017.pdf | https://dl.acm.org/doi/pdf/10.1145/3092703.3092711 |
| launchbury1993.pdf | https://dl.acm.org/doi/pdf/10.1145/158511.158618 |
| donze2010.pdf | https://doi.org/10.1007/978-3-642-15297-9_9 |
| donze2010breach.pdf | https://doi.org/10.1007/978-3-642-14295-6_17 |

Para Felleisen-Friedman 1986, Höhle 1992, McIver-Morgan 2005 y el SICP no tengo un link verificado. Son un capítulo de actas, un capítulo de libro y dos libros.

Cuando los tengas, avisame y agrego al índice el hash y la fila de cada uno.

## 23. Luciano  2026-10-08 23:18:26 UTC  (line 497)

pasame los libros con sus titulos

## 24. Model  2026-10-08 23:18:36 UTC  (line 501)

Estos son los cuatro, con los datos ya verificados:

| guardar como | referencia |
|---|---|
| felleisen1986.pdf | Matthias Felleisen y Daniel P. Friedman, "Control operators, the SECD-machine, and the λ-calculus". Capítulo en *Formal Description of Programming Concepts III*, North-Holland, 1987. Se presentó en la conferencia de trabajo de la IFIP de agosto de 1986. |
| hohle1992.pdf | Ulrich Höhle, "M-valued sets and sheaves over integral commutative cl-monoids". Capítulo en *Applications of Category Theory to Fuzzy Subsets*, Kluwer, 1992, páginas 33 a 72. |
| mciver2005.pdf | Annabelle McIver y Carroll Morgan, *Abstraction, Refinement and Proof for Probabilistic Systems*. Springer, 2005. |
| abelson1996.pdf | Harold Abelson, Gerald Jay Sussman y Julie Sussman, *Structure and Interpretation of Computer Programs*, segunda edición. MIT Press, 1996. La parte que importa es la sección 4.1, el evaluador metacircular. |

El SICP tiene edición gratuita en línea de MIT Press. Los otros tres probablemente necesiten la biblioteca. De Felleisen-Friedman no verifiqué las páginas; si el PDF trae el rango, lo agrego a la entrada.

## 25. Luciano  2026-10-08 23:27:11 UTC  (line 509)

ahi baje todo lo que pude, renombra los files

## 26. Model  2026-10-08 23:27:21 UTC  (lines 513, 519, 529, 559, 574)

Busco dónde quedaron los archivos.

Están en la carpeta pdf con los nombres de la editorial. Antes de renombrar confirmo qué es cada uno por su primera página.

Todos son los papers correctos. Renombro, y del volumen de Höhle busco las páginas de su capítulo.

Todo identificado. El capítulo de Höhle son las páginas 33 a 72 del volumen, y lo extraje aparte. Ahora actualizo el índice y el BibTeX.

Renombré los once archivos y verifiqué cada uno contra su primera página: todos son el paper o libro correcto. Nueve ya están commiteados con su hash en el índice (a3c0ccf).

| nombre | qué es |
|---|---|
| kozen1985.pdf | A probabilistic PDL |
| goguen1967.pdf | L-fuzzy sets |
| fainekos2009.pdf | Robustness of temporal logic specifications |
| morgan1996.pdf | Probabilistic predicate transformers |
| bistarelli1997.pdf | Semiring-based constraint satisfaction |
| loscher2017.pdf | Targeted property-based testing |
| launchbury1993.pdf | A natural semantics for lazy evaluation |
| annapureddy2011.pdf | S-TaLiRo |
| abelson1996.pdf | SICP, segunda edición, licencia CC BY-SA |
| mciver2005.pdf | McIver y Morgan, el libro |
| rodabaugh1992.pdf | el volumen completo de Kluwer donde está Höhle |

Del volumen saqué el capítulo de Höhle, páginas 33 a 72, como hohle1992.pdf.

Me equivoqué al corregirme en un punto. Bistarelli y coautores sí tratan las restricciones probabilísticas, en la sección 6.3, así que lo que te dije en el chat era correcto. Retiré esa corrección del índice.

Con los PDFs completé además el volumen y las páginas de Fainekos-Pappas y las páginas de Launchbury en el BibTeX.

Siguen faltando Donzé-Maler, Breach y Felleisen-Friedman. En tu carpeta de descargas hay un archivo a medio bajar de 17 MB; si es alguno de esos, cuando termine lo renombro.

Decide vos: ¿commiteo los dos libros de Library Genesis, el de McIver-Morgan y el capítulo de Höhle, o quedan solo en tu disco? Por ahora están en la carpeta, fuera de git. El repo es privado, pero GitHub prohíbe alojar copias sin licencia, y sacar un archivo de la historia de git después es difícil. Mi recomendación es dejarlos fuera de git con una línea en el .gitignore. El volumen completo de 27 MB lo dejaría fuera en cualquier caso.

## 27. Luciano  2026-10-08 23:30:24 UTC  (line 577)

si no commiteemos pdfs ni libros. Tomemos el doi como link.

## 28. Model  2026-10-08 23:30:44 UTC  (line 582)

Decisión tuya: ningún PDF ni libro en git, y el DOI como link. Primero miro si los dos commits con PDFs ya salieron al remoto, porque eso define si se pueden sacar de la historia.

## 29. Luciano (queued)  2026-10-08 23:30:41 UTC  (line 589)

como puntero quiero decir

## 30. Model  2026-10-08 23:32:26 UTC  (lines 600, 644)

Todos los DOIs que tenía resuelven al título correcto. Los dos de LIPIcs están registrados en DataCite, no en Crossref, así que los chequeo por doi.org. También busco los DOIs que faltan.

Ya no hay ningún PDF ni libro en git, y cada referencia apunta a su fuente por el DOI. Todo quedó en un solo commit (7eb7ecd), que reemplaza a los dos anteriores. Esos dos no habían salido al remoto, así que los PDFs no están en la historia que se va a subir.

**Los DOIs.** Verifiqué cada DOI contra Crossref y resuelve al título correcto; los dos de LIPIcs, contra doi.org. Varios los había puesto de memoria y estaban bien. Sumé diez que faltaban, entre ellos el de Lawvere 1973 en Springer y el de la reedición de Plotkin en 2004. Cuatro referencias no tienen DOI: Walters, el libro de HoTT, el SICP y Felleisen-Friedman. Walters y HoTT llevan el link a la página del editor o del autor; el SICP y Felleisen-Friedman quedan sin link.

**Las copias que leí.** Siguen en tu disco, en la carpeta pdf de la bibliografía, que ahora está en el .gitignore. El índice guarda el hash de cada copia, así se sabe cuál se leyó, igual que el hash fija un File en el documento 09. También anota cuándo la copia no es la versión a la que apunta el DOI, como la de arXiv o una copia de curso.

**El log de decisiones.** Registré tu decisión como D-2026-10-09-a. Toca P7 (cada repositorio es autocontenido): para las fuentes, el repo ahora apunta en vez de contener.

Siguen sin copia Felleisen-Friedman y los dos de Donzé. En tu carpeta de descargas había un archivo de 17 MB a medio bajar; si es alguno de esos, cuando termine lo renombro y agrego su hash.

Decisión mía: guardar el hash de cada copia local en el índice.

## 31. Luciano  2026-10-08 23:37:14 UTC  (line 648)

fijate lo que es

## 32. Model  2026-10-08 23:37:40 UTC  (line 668)

El archivo a medio bajar era una segunda descarga del volumen de Höhle, y ya terminó. No es Donzé ni Felleisen.

Las cuatro copias que hay en tu carpeta de descargas son duplicados exactos, con el mismo hash, de las que ya están en la bibliografía: dos del volumen de Rodabaugh, Klement y Höhle, y dos del libro de McIver y Morgan. No hay nada nuevo para agregar, y si querés podés borrar las cuatro de descargas.

Siguen sin copia Felleisen-Friedman y los dos papers de Donzé.

## 33. Luciano  2026-10-09 00:26:50 UTC  (line 672)

bueno, quiero ahora una busqueda bibliografica para todos los aspectos de Luthier

## 34. Model  2026-10-09 00:27:05 UTC  (line 676)

Primero mapeo los aspectos de Luthier desde sus propios documentos, y miro qué literatura ya citan, para no buscar lo que ya está.

## 35. Luciano (queued)  2026-10-09 00:32:35 UTC  (line 732)

why did you think I am a physicist?

## 36. Model  2026-10-09 00:33:41 UTC  (line 736)

No me lo dijiste: lo inferí, y no tenía base suficiente para ponerlo como un hecho en las instrucciones de las búsquedas. Me apoyé en tu email de la FCEN-UBA, en que los proyectos son análisis científicos (localización de sonido y macroIR), y en las referencias a Jaynes y a la inferencia bayesiana. Eso indica que hacés ciencia cuantitativa, no que seas físico. El dominio `qi` de tu email apunta más bien al departamento de química, así que probablemente me equivoqué.

Para la búsqueda pesa poco. Solo inclina un poco hacia el software científico, que igual es el caso de uso de Luthier.

Las ocho búsquedas siguen corriendo. Cuando terminen verifico cada DOI contra Crossref y armo el relevamiento.

## 37. Luciano  2026-10-09 00:34:49 UTC  (line 740)

O sea de mi comportamiento el posterior es que soy un fisico? Es interesante saberlo.

## 38. Model  2026-10-09 00:35:02 UTC  (lines 744, 763)

Sí, en un sentido. Pero lo que hice fue peor que un posterior: tomé la moda y la escribí como un hecho, que es justo lo que Luthier no quiere que haga un certificado.

Lo que empujaba hacia "físico":

- Leés el conocimiento con Cox y Jaynes. Jaynes era físico, y en lo que leí esa tradición la cultivan sobre todo físicos.
- Pensás en invariantes, en observador y universo, en estados del mundo y en costos como likelihoods no normalizados.
- Escribiste un intérprete en C++ para tu propio análisis, macroIR, en vez de usar una herramienta hecha.
- Los dos proyectos son inferencia sobre datos experimentales.

Nada de eso separa a un físico de un fisicoquímico, un biofísico o un estadístico con formación en ciencias duras. Y el dominio de tu email apunta a química. Calibrado, el posterior era "científico experimental cuantitativo, formado en física o fisicoquímica". Elegir "físico" dentro de eso fue sobreconfianza, no evidencia.

Hay además un sesgo de fondo. En lo que leí, quien escribe así sobre Jaynes suele ser físico, así que mi prior ya venía cargado hacia ahí antes de leerte.

Llegó la primera de las ocho búsquedas, la de teorías como tipos, con 15 referencias y sus DOIs verificados. Espero las otras siete antes de armar el documento.

## 39. Luciano  2026-10-09 00:39:32 UTC  (line 769)

for the record soy biologo, pero siempre me gustaron las matematicas y mi mujer es fisica experimental. 
Mi intuicion de estudiante era que la computacion podia ocupara para la biologia el rol que la matematica ocupo para la fisica. Toda mi vida apunto a trabajar sobre esa intuicion.

## 40. Model  2026-10-09 00:39:49 UTC  (lines 779, 794, 817, 821, 867, 891, 904, 913, 921, 938, 960, 971)

Lo guardé en la memoria para las próximas sesiones: sos biólogo, te gusta la matemática, y no tengo que inferir tu campo por tu estilo.

Esa intuición no aparece en [objectives.md](record/objectives.md). Ahí están O1 a O5, pero no el porqué detrás de ellos, y lo que me dijiste es exactamente eso. Si querés que entre, la agrego como cita tuya al principio del documento, sin tocar los objetivos.

Las siete búsquedas restantes siguen corriendo.

Llegó la segunda búsqueda, la de evidencia estadística. Su hallazgo más fuerte: la regla de transferencia entre usos ya está publicada, en forma frecuentista (Bishop y Povyakalo, 2017). Guardo los dos informes en el scratchpad para no perderlos antes de armar el documento.

Llegaron dos más: elección entre implementaciones con inferencia, y legibilidad con especificaciones para código escrito por IA. Las guardo también.

Van cuatro de ocho. Faltan maquinaria de tests, intérpretes, procedencia y números.

Van siete de ocho; falta la de intérpretes. Mientras tanto verifico yo mismo los DOIs de lo que llegó, sin confiar en el chequeo de los agentes.

Todo resuelve: 138 DOIs y seis preprints de arXiv. Hago un último chequeo de que el título que devuelve Crossref coincida con el que puso cada búsqueda.

Los títulos de Crossref coinciden con los citados en las 134 referencias que tienen DOI en Crossref. Ahora genero el BibTeX de cada DOI directamente desde doi.org, para no transcribir a mano.

Los 138 BibTeX bajaron bien. Agrego a mano los catorce sin DOI y corrijo dos errores que Crossref tiene en nombres de autores.

Todo listo para escribir. Armo el relevamiento: arriba una síntesis de una pantalla, después cada aspecto con sus referencias, el DOI como link y qué toma Luthier de cada una.

Antes de commitear verifico dos cifras de la síntesis contra los resúmenes originales, porque las tomé de los informes de los agentes.

Las búsquedas dejaron dos PDFs sueltos en la raíz del repo. Miro qué son antes de tocarlos.

El relevamiento está terminado y commiteado (d25a4f0) en [survey-2026-10-09.md](record/bibliography/survey-2026-10-09.md). Tiene 146 referencias en ocho secciones, una por aspecto de Luthier. Cada referencia lleva su link y una línea sobre qué tomaría Luthier de ella. Esas líneas son propuestas de los modelos que buscaron, y el documento lo marca así.

**Verificación.** Resolví de nuevo yo mismo los 138 DOIs y el título de cada uno coincide con el citado. También verifiqué los seis preprints contra arXiv y dos cifras de la síntesis contra sus resúmenes; una de ellas la tuve que corregir. Tres datos descansan en fuentes más débiles y lo dicen en su línea. El BibTeX de las 152 entradas sale de doi.org, salvo catorce sin DOI que escribí a mano.

**Antecedentes muy cercanos.** Para estos Luthier tiene que decir qué agrega:
- Los subtipos por predicado de PVS ya ponen `{ x : T | p }` en el centro, pero con obligaciones de prueba donde Luthier tiene tests.
- PetaBricks pone varias implementaciones en el código fuente y un autotuner elige, sin leyes ni posterior.
- Darulova y Kuncak (2014) escriben sobre un `Real` ideal y compilan a una realización con precisión probada.
- Bishop y Povyakalo (2017) ya publicaron tu regla de transferencia entre usos, `p_V ≤ c·p_U`, en forma frecuentista.
- Strigini y Povyakalo (2013) tienen el prior con un átomo en cero fallas. Así un grado "probado" alimentaría un posterior muestreado.

**Lo que ninguna búsqueda encontró.** Ahí es donde Luthier podría decir algo nuevo:
1. Varias implementaciones certificadas como modelos de una teoría definida solo por sus leyes, con la tolerancia del acuerdo derivada de sus cotas de error.
2. Un posterior guardado sobre la conducta de un modelo, con cada certificado como una decisión para un uso.
3. Trazas comparadas por consecuencia y por costo, con el costo como orden parcial con varianza.
4. Un autointérprete cuyas reglas son leyes del lenguaje, con la estrategia como parámetro y certificado paso a paso contra otro anfitrión.
5. Un registro de qué texto de especificación escribió el humano y cuál el modelo.

**Resultados que tocan decisiones ya tomadas:**
- **Knight y Leveson (1986).** Versiones escritas por separado fallan juntas mucho más de lo que predice la independencia. El acuerdo entre la versión nativa y la extern vale menos de lo que parece, sobre todo si las escribió el mismo modelo.
- **Kaufman y coautores (2026).** Programadores juzgaron bien el 74% de las aserciones correctas escritas por un LLM, pero solo el 49% de las incorrectas, con la misma confianza. Las explicaciones en lenguaje natural no ayudaron. Es la tensión entre O3 (que los modelos trabajen largo) y O2 (pertenecer a un tipo es un certificado), medida.
- **Littlewood y Strigini (1993).** 1e-9 no se certifica solo testeando: el prior hace el trabajo y tiene que estar explícito.
- **Reynolds (1972).** Un intérprete metacircular hereda el orden de evaluación del anfitrión, salvo que se escriba en estilo de continuaciones. Importa para que la estrategia sea un parámetro.
- **Rule y coautores (2018).** Uno de cada cuatro notebooks no tiene ningún texto explicativo. Un campo de texto en una definición va a quedar vacío si nada lo exige.

Las búsquedas dejaron sueltos en la raíz del repo un capítulo del preprint de Jaynes y el informe técnico de ATLAS. Los moví a la carpeta de copias locales, que está fuera de git.

¿Cuál de los cinco huecos querés que trabajemos primero? Recomiendo el 1. Es el que más cerca está del uso en sonolocalización, y el resultado de Knight y Leveson dice que hace falta ya.
