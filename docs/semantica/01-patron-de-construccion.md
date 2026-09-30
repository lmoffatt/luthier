# El patrón de construcción y las decisiones de sintaxis

Borrador 0, 2026-09-29. Recoge lo decidido en las sesiones posteriores al borrador `00-elementos-fundamentales.md`, que queda como base del núcleo pero cambia de centro: la versión 0 de Luthier no demuestra, testea; y el concepto organizador es el patrón de construcción de la sección 2.

## 0. Notación nueva respecto de `00`

- `:=` define. `=` es la proposición de igualdad (reservada para la capa de demostraciones, ausente en la versión 0). `==` es la igualdad decidible, una función a `Bool` que existe para algunos tipos.
- `\ x { t }` es la función que a `x` le asigna `t`. Las llaves delimitan el alcance de `x` y, más adelante, un bloque con definiciones locales.
- `f a` es aplicación por yuxtaposición, asocia a la izquierda y liga más fuerte que cualquier operador; `f(a)` es lo mismo. `f (a, b)` aplica `f` a un par.
- `(x : A) -> B` es el tipo de función, con `B` pudiendo mencionar a `x`; `A -> B` cuando no. `(x : A) × B` es el par dependiente.
- `f (x : A) (y : B) : C := t` es azúcar de `f : (x : A) -> (y : B) -> C := \ x { \ y { t } }`. Los nombres se escriben una vez.
- Cláusulas por patrones, `| zero := ... | succ n := ...`, son azúcar del recursor de `data`.
- `{ x : T | p x }` es azúcar de `(x : T) × Certificado (p x)`: el subconjunto de `T` donde vale `p`.
- `requires (x y : N) { e1 ; e2 }` es azúcar de una lista de leyes, sección 1.

## 1. Versión 0: leyes que se testean

Un invariante es una función a `Bool`. Una ley es un tipo de entradas junto con un predicado sobre ellas:

    Ley : U := (A : U) × (A -> Bool)

Un concepto es una función ordinaria que devuelve leyes. No es una primitiva ni una palabra clave:

    Resta (s : N -> N -> N) : List Ley := [
      (N × N, \ (x, y) { s (add x y) y == x }),
      (N × N, \ (x, y) { y <= x -> add (s x y) y == x })
    ]

`Resta sub` es una lista de dos tests concretos. Correrlos es generar `n` entradas del tipo de cada ley y evaluar el predicado; una entrada donde da `false` es un contraejemplo. El generador por tipo, `muestra : (A : U) -> N -> List A`, es un hueco que el entorno llena. El registro de una corrida (ley, entradas, fallos, tiempo) es un dato, y es la base de corridas de los audios.

La unidad de especificación es el grupo de funciones con las leyes que las relacionan; una función sola con postcondición es el grupo de tamaño uno. `read (write s k a) k == a` no es postcondición de `read` ni de `write`: es una relación entre ambas, y por eso se definen juntas.

Para reales, las leyes usan tolerancia: `a ≈[tol] b := abs (a - b) < tol`.

Cuando se agregue la capa de demostraciones, la misma función devuelve un tipo en lugar de una lista: una ley testeada `(A, p)` se vuelve `(a : A) -> Cierto (p a)`, con `Cierto : Bool -> U` que manda `true` a `⊤` y `false` a `⊥`. El concepto no cambia.

## 2. El patrón de construcción: subtipos

Todo el patrón es una definición. Un subtipo es un tipo y un predicado sobre él:

    Subtype (T : U) (P : T -> Report) : U := (x : T) × Report

    subtype T P : T -> Resultado (Subtype T P)     comprobar P y empaquetar con el certificado
    forget      : Subtype T P -> T := fst          olvidar el certificado

`{ x : T | P x }` es la azúcar de `Subtype T P`. El nombre es el estándar: subobjeto en teoría de categorías (un predicado `T -> Ω` clasifica un mono `S -> T`; acá `fst` es el mono), subset type o `sig` en teoría de tipos.

`P` devuelve un `Veredicto`, no un `Bool`, porque hay dos formas de comprobar: para un valor de `N` el predicado se evalúa y el veredicto es exacto; para una función el predicado son leyes que se muestrean con `n` casos y el veredicto es estadístico. `Bool` es el caso exacto. El certificado es el veredicto guardado con sus parámetros (leyes, `n`, generador, rango, máquina, fecha). Poner la diferencia en el veredicto y no en dos nociones de subtipo es lo que mantiene una sola definición.

Un concepto es el predicado `P` cuando `T` es un tipo de funciones. No hace falta la palabra.

Fallo y certificado son un solo tipo, un árbol:

    Report : U := data {
      node : (what : Term) -> (arg : Term) -> (verdict : Verdict) -> (children : List Report) -> Report
    }
    Verdict : U := data { ok ; fail ; sampled : (n : N) -> Verdict ; proved }

Cada nodo dice qué se comprobó (`what`, un quote del predicado o subtipo, como `'{ Associative add }`), sobre qué (`arg`), con qué resultado, y de qué sub-comprobaciones dependió. Un fallo de `Ring` es un nodo `Ring` con un hijo por ley, y cada hijo con su argumento. Un certificado es el mismo árbol con `ok` o `sampled n` en los nodos. `Result A := ok A + fail Report`, sin parámetro de error.

Versión 0: `Failure := String`, el `Maybe_error` de macro_dr. Es el árbol aplastado por el olvido máximo, y mientras el reporte solo lo lee una persona no se distingue. Dos reglas para que la migración al árbol sea mecánica: `Result` y `Failure` son tipos con nombre y ninguna firma menciona `String`; y el mensaje se construye siempre con `report what arg`, nunca concatenando a mano. El árbol se adopta cuando haga falta filtrar fallos por ley o reproducir un contraejemplo sin parsear texto.

La combinatoria vive en el valor, no en el tipo: hay un solo tipo de fallo y todo el manejo (imprimir, filtrar por etiqueta, olvidar niveles) es una función sobre el árbol. Lo que el tipo deja de decir (qué puede fallar) está en las leyes de la definición, que son datos del programa. Las etiquetas son quotes, no strings: se comparan, se buscan en el programa y se re-ejecutan para reproducir el fallo. Esta es la respuesta a la explosión de tipos de los templates de C++: la estructura del error va en el dato, con una forma común, y el tipo queda fijo.

El certificado dice qué significa "verificado": cuántos casos, con qué generador, en qué rango, cuándo. Dos valores del mismo tipo con certificados distintos no tienen la misma garantía; el tipo no lo distingue, el certificado sí.

Instancias:

- `Dia := Subtype N (\ n { 0 < n and n <= 31 })`; `subtype` evalúa el predicado.
- `Almacen S K A := Subtype ((S -> K -> A -> S) × (S -> K -> A)) (leyes de write y read)`; `subtype` muestrea. Sección 3.
- Una library. Es el patrón aplicado a `Program`, y es el nombre elegido para la instancia: un programa que pasó sus tests y lleva el certificado. El adjetivo "tested" sobra porque en Luthier no hay otra forma de que una library exista.

      Library := Subtype Program P_luthier

  con `P_luthier` = cada cuerpo tiene su tipo, no hay ciclos, y cada ley atada a una definición pasó sus tests. `subtype` es `check` seguido de `correr` sobre todas las leyes. El certificado dice, definición por definición, en qué nivel está: sin leyes, con leyes sin correr, con `n` casos pasados, o demostrada cuando exista esa capa. Una library es una serie de tipos y funciones verificadas con su conjunto de tests, y los teoremas son la misma declaración con otra clase de certificado. `Program` sigue siendo el tipo sin verificar.

  `combinar` de dos libraries no da una library: las leyes de uno pueden mencionar funciones del otro, y las que cruzan la frontera se vuelven a correr. El verificador es a su vez un programa Luthier, sujeto a su propio predicado.

La comprobación de un valor es un cómputo exacto; la de una función es un experimento con `n` casos. Luthier trata a las dos como la misma operación de construir, con certificados distintos.

El patrón se aplica a sí mismo: el tipo certificado de una etapa es el tipo base de la siguiente (un real, un real con error, una muestra, un estimador). El certificado se acumula por composición y `forget` compuesto es el olvido en cadena. Las leyes del patrón se testean como cualquier otra:

    forget (subtype x) == x          cuando subtype x tiene éxito
    subtype (forget y)               siempre tiene éxito

Un nombre, dos usos: el nombre es del subtipo. En posición de tipo significa `Subtype T P`; aplicado a un valor de `T` significa `subtype T P`. El verificador siempre sabe cuál espera.

En el núcleo esto no agrega nada: usa `×`, funciones, dos `data` (`Resultado`, `Ley`) y el generador como hueco.

## 2b. Relación con los concepts de C++

El patrón es un concept de C++ (un predicado con nombre, evaluado antes de usar) con cuatro extensiones, todas consecuencia de que el predicado es una función ordinaria:

- Dominio: no solo tipos, sino valores, funciones, grupos de funciones y programas enteros.
- Qué chequea: C++ verifica sintaxis y tipos, y deja los requisitos semánticos en la documentación. Acá van en el mismo bloque y se corren.
- Cómo: exacto para valores, estadístico con `n` casos para funciones; de ahí el certificado.
- Parámetros: cualquier valor (`eps`, `n_max`, otra library), no solo tipos y constantes.

De C++ se copian la subsunción (un concepto que implica a otro es más específico y gana al elegir implementación), la composición (`&&` es concatenar listas de leyes) y la forma `requires (x y : N) { ... }`. Diferencia: C++ chequea en cada uso; acá lo comprobado queda en el certificado y viaja con el valor.

Frase corta: Luthier es concepts llevados a todo el lenguaje, con requisitos semánticos que se ejecutan y cuyo resultado se guarda.

Nombres de unidades en otros lenguajes, para referencia: `namespace` (agrupa nombres), `unit`/`package`/`module`/`crate` (compilación y carga), `spec`+`body` en Ada y `signature`+`structure` en ML (interfaz con tipos; Ada admite `Pre`/`Post` parametrizables por genéricos), `type class`/`trait`/`protocol`/`concept` (grupo de funciones con leyes en documentación; en Lean y Coq, con demostración). Ninguno hace que la unidad de distribución sea un tipo cuyo predicado tiene parámetros.

## 3. Ejemplo: Almacen

`S` es el estado, `K` el tipo de las claves, `A` el de los valores.

    leyes_almacen (S K A : U) (write : S -> K -> A -> S) (read : S -> K -> A) : List Ley := [
      ( S × K × A,      \ (s, k, a)     { read (write s k a) k == a } ),
      ( S × K × K × A,  \ (s, k, k', a) { k /= k' -> read (write s k a) k' == read s k' } )
    ]

    Almacen (S K A : U) : U :=
        (write : S -> K -> A -> S) × (read : S -> K -> A) × Certificado

    almacen (S K A : U) (write : S -> K -> A -> S) (read : S -> K -> A) (n : N)
      : Resultado (Almacen S K A) :=
      match correr (leyes_almacen S K A write read) n {
        ok cert -> ok (write, read, cert)
        fallo c -> fallo c
      }

Quien necesita un almacén pide `Almacen S K A` y no puede recibir un par que no haya pasado por `almacen`. Las funciones que salen son las mismas que entraron; lo verificado es el par.

La segunda ley es la que hace falta para que un `write` que borra todo lo demás no pase. Y `read` sobre una clave ausente no tiene qué devolver: `read : S -> K -> Maybe A`, un valor por defecto en `S`, o `K` restringido a las claves presentes. La ley obliga a decidirlo.

## 4. Lo que queda abierto

- El campo de leyes en `Def`: si es un campo más junto al cuerpo y al texto, o si las leyes van siempre en definiciones aparte y se atan por nombre.
- Igualdad decidible como concepto (`Eq A`) que otros conceptos reciben o exigen.
- Generadores: filtrado sobre el tipo base o definidos por el usuario, y cómo se declara el rango.
- Si el doble uso del nombre (tipo y constructor) se mantiene o se separa con mayúscula y minúscula.
- Cómo se compone el `Report` al anidar subtipos y al iterar: cortar en el primer fallo, acumular todos, o decorar el valor con el registro y seguir (las tres formas de propagación que MCMC necesita).


## 5. Nombres

Nombres del lenguaje y de la librería en inglés (`Ring`, `Field`, `forget`, `Result`, `ok`, `fail`, `Predicate`, `Law`, `Certificate`, `test`); documentación en castellano. "Material" fue un nombre para explicar el patrón y no aparece en programas: lo que aparece es el tipo concreto, con sus componentes nombradas a la izquierda del `|`.
