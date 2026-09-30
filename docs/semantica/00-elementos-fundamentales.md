# Elementos fundamentales de un programa Luthier

Borrador 0, 2026-09-29. Propuesta para discutir, no decisión tomada. Sale de leer los 42 audios, la consolidación de ideas, los informes del mentor, la charla con Gemini, y del pedido de esta sesión: nombrar los ciudadanos de primera y comprobar que el núcleo se ejecuta a mano. Donde una idea está en los audios se cita el audio; donde es una propuesta nueva se dice que es propuesta.

## Los elementos, en el orden para pensar

Diez palabras. Con las cinco primeras se lee cualquier programa; con las tres siguientes se fabrican tipos; las dos últimas son lo que corre.

- **Tipo.** Un objeto: `N`, `Bool`, `N -> N`. Una colección de valores y a la vez una afirmación sobre ellos.
- **Valor.** Un elemento de un tipo, `4 : N`. El juicio `a : A` ("a es un A") es la relación básica.
- **Función.** Una flecha entre tipos, `f : A -> B`. Es un valor del tipo `A -> B`, sin categoría aparte: puede ser argumento y resultado.
- **Definición.** Darle nombre a un valor, `nombre : Tipo := valor`. El único acto del lenguaje. Un programa es un conjunto de definiciones sin orden; las dependencias entre nombres dan el grafo.
- **Hueco.** Una definición sin valor, `nombre : Tipo`. Una hipótesis: input, función externa, pendiente. Lo que depende de un hueco no se ejecuta.
- **Función dependiente.** `(x : A) -> B x`: el tipo del resultado depende del argumento. Es el "para todo". Sin dependencia, la flecha común.
- **Dato.** `data { ... }`: un tipo definido por sus constructores. Suma de productos con recursión. De acá salen `Bool`, `N`, listas, pares, `Result`.
- **Subtipo.** `{ x : T | p x }`: los valores de `T` que cumplen `p`, con certificado. `p` es cualquier función a `Bool`, incluidas leyes sobre funciones; cumplir se comprueba con `test` y queda registrado. `Ring`, `Subtraction`, `Library` son subtipos. Es lo que hace a Luthier.
- **Aplicar.** `f a`.
- **Reducir.** Reemplazar el argumento en el cuerpo hasta que no quede nada por hacer. Ejecutar a mano es esto.

`U` es el tipo de los tipos; hace falta solo cuando una función devuelve un tipo. `Term`, `Program`, `eval` son un dato y funciones como cualquier otro, y sirven para que un programa mire programas: están arriba, no abajo. Lo que sigue en este documento es el detalle, y empieza por la definición.

Frente a C++: statements son definiciones; expressions son valores, funciones incluidas; tipos son tipos, más el dependiente y el subtipo con leyes. No hay variables mutables, secuencia, punteros ni herencia. Frente a categorías: tipos son objetos, funciones flechas, aplicar es componer, el subtipo es un mono con certificado y `forget` es el mono.

## 0. Notación

Todo símbolo que aparece en el documento se define acá.

- `x : A` se lee "x es un término del tipo A".
- `x : A := t` define `x` como el término `t`, de tipo `A`.
- Un hueco es una definición con tipo y sin cuerpo, `f : A`. El símbolo `?` aparece solo como azúcar dentro de un término (sección 1) y no es parte del núcleo.
- `≡` es igualdad definicional: dos términos que se reducen a la misma forma normal. No es una proposición; es un juicio que decide el reductor.
- `=` es el tipo identidad: la proposición "a y b son iguales". Sus términos son caminos (paths).
- `U` es el universo: el tipo cuyos términos son tipos.
- `Π (x : A). B` es el tipo de las funciones dependientes: a cada `x : A` le asignan un término de `B`, donde `B` puede mencionar a `x`. Si `B` no menciona a `x` se escribe `A → B`.
- `Σ (x : A). B` es el tipo de los pares dependientes: un `x : A` junto con un término de `B`, donde `B` puede mencionar a `x`.
- `λ x. t` es la función que a `x` le asigna `t`.
- `t[a/x]` es `t` con toda ocurrencia de `x` reemplazada por `a`.
- `⊥` es el tipo vacío (ningún término). `⊤` es el tipo con exactamente un término.
- `data { ... }` declara un tipo inductivo dando sus constructores.

## 1. La unidad es la definición

Un programa Luthier es un conjunto finito de definiciones. No hay statements ni secuencia. El orden en que se escriben no importa: la dependencia entre definiciones se lee de los nombres que cada una usa, y eso da el grafo dirigido acíclico (DAG) de definiciones del audio 2026-05-29 15.11.47 [01:48]. Un ciclo de dependencia es un error del programa.

Cada definición tiene la forma `nombre : Tipo := término`. El tipo es la proposición que el nombre afirma (audio 2026-05-26 12.32.24 [00:51]; audio 2026-08-31 19.48.17 [01:02]); el término es la evidencia, que en el caso de una función es su implementación. Esto cubre la doble definición que pide el audio 2026-05-29 14.28.55 [03:42]: "desde las propiedades" es el tipo, "operativamente" es el cuerpo.

Hay tres grados de completitud:

1. `f : A → B := t`. Definición completa.
2. `f : A → B`. Declarada, sin cuerpo. Es un hueco. No hace falta ningún símbolo: la ausencia de `:=` es el hueco.
3. `f := t`. Sin tipo. El tipo se infiere. Es la concesión a la naturalidad de Python; ejecutando a mano el tipo se escribe siempre.

El hueco es una sola cosa que cumple cinco papeles: axioma, input del programa, función externa que el entorno provee, definición pendiente, código muerto. El audio 2026-05-29 14.46.22 [02:26] ya lo dice: "ese tipo es un input del programa si no está definido nunca". Y el principio "no ejecutás el código hasta que no está definido" (audio 2026-05-30 18.09.57 [00:53]) es exactamente la semántica del hueco: un término que contiene un hueco no se reduce; todo lo que no depende de él se reduce normalmente. Con esto no hace falta un tipo `External` en el núcleo: `sin : R → R` sin cuerpo es una función que el entorno llena con numpy, con libm o con una tabla, y Luthier solo sabe su tipo.

Un hueco también puede aparecer dentro de un término, cuando el cuerpo está casi entero y falta un pedazo. Ahí sirve un símbolo, `?`, para que el verificador acepte lo que está y calcule el tipo de lo que falta. Pero eso es azúcar, no primitiva: un `?` dentro de un término equivale a un nombre nuevo declarado sin cuerpo, con tipo `Π` sobre las variables locales que el hueco veía, y aplicado a esas variables. Por ejemplo,

    g : Π (n : N). P n := ind n base (λ n. λ ih. ?)

es el mismo programa que

    paso : Π (n : N). P n → P (succ n)
    g : Π (n : N). P n := ind n base paso

La única diferencia es quién escribe el tipo de `paso`: el verificador o la persona. A mano lo escribe la persona, así que el núcleo tiene una sola noción de hueco.

El núcleo tampoco distingue entre un hueco que el entorno va a llenar y uno que todavía no se escribió. Es una diferencia de intención, y va en el campo de texto de la definición (sección 7) si se adopta.

Propuesta (no está en los audios): dos definiciones con el mismo nombre no son un error ni un producto cartesiano (el audio 2026-05-29 14.46.22 [01:51] proponía el producto). Son dos implementaciones del mismo nombre, es decir dos caminos. Se distinguen como `f#1` y `f#2`. El nombre pelado `f` se puede usar solo si existe un camino `f#1 = f#2` en el programa, o si quien lo usa elige uno. Esto pone la idea de paths en la gramática sin agregar ninguna primitiva.

## 2. Los términos: cálculo lambda y reducción

Un término se construye con tres cosas: una variable (un nombre), una abstracción `λ x. t`, y una aplicación `f a`. Hay una sola regla de cómputo, la sustitución:

    (λ x. t) a  ≡  t[a/x]

A esa regla se suman las reglas de reducción de cada tipo inductivo (sección 3), que también son sustituciones.

Ejecutar un programa a mano es elegir una definición sin variables libres y reducirla hasta que no quede nada por reducir. Cada paso es una igualdad definicional. Eso es todo lo que "ejecutar" significa en el núcleo, y coincide con el audio 2026-05-30 18.01.53 [01:47]: la matemática no ejecuta, verifica equivalencias. Verificar un programa a mano es comprobar que el cuerpo de cada definición tiene el tipo declarado. Las dos operaciones se hacen con lápiz.

## 3. Los formadores de tipos

Tres primitivas: `U`, `Π` y `data`. Todo lo demás se define en Luthier.

- `U`, el universo. Hace falta para que una función devuelva un tipo, que es lo que el audio 2026-05-29 14.03.24 [00:15] identifica como tipo dependiente. Detalle conocido: `U : U` es inconsistente; el remedio estándar es una jerarquía `U₀ : U₁ : ...`. Es la "trampa" del audio 2026-05-29 14.06.25 [00:00]. A mano se ignora hasta que muerde.
- `Π`, la función dependiente. Es el cuantificador "para todo" (audio 2026-05-31 20.10.46 [00:04]: los cuantificadores tienen que ser ciudadanos de primera).
- `data`, los tipos inductivos. Se declaran los constructores y se obtiene el recursor con sus reglas de reducción.

Con `data` se definen, en Luthier mismo:

- `⊥ : U := data { }` y `⊤ : U := data { unit }`.
- `Bool : U := data { true ; false }`.
- `Σ`, el par dependiente. Es el cuantificador "existe". Un valor decorado es un `Σ`: un real con error es `Σ (x : R). Error x`. Los decoradores del audio 2026-05-29 14.28.55 [03:05] son esto.
- `=`, el tipo identidad, con un único constructor `refl : Π (A : U). Π (a : A). a = a`. Sus términos son los caminos.
- `N`, `List`, y cualquier estructura de datos.
- `Program` y `Term` (sección 5).

Qué pasa con los candidatos que se nombraron al abrir esta sesión:

| Candidato | Veredicto | Dónde cae |
|---|---|---|
| Tipos elementales (int, real, bool) | No son primitivos | Se definen con `data`. `N` es un inductivo de dos constructores. `R` es una estructura con sus operaciones y axiomas, algunos como huecos. |
| Funciones elementales (suma, seno) | No son primitivas | La suma sobre `N` se define por recursión. El seno sobre `R` es un hueco que el entorno llena. |
| Código como dato | Primitivo, en una forma precisa | `Program` es un tipo inductivo y `eval` una función parcial (sección 5). |
| Verdadero y falso | No como `Bool` | Una proposición es un tipo. Es verdadera si tiene un término. `⊤` y `⊥` son los dos extremos. `Bool` es un dato más. |
| Verdadero por definición | Primitivo | Es la igualdad definicional `≡`. Es lo que se ejecuta a mano (sección 4). |
| Dirección y dato (puntero) | No es primitivo | El nombre es la referencia. La dirección de memoria es una decoración del nivel más bajo de equivalencia (audio 2026-05-30 18.01.53 [02:48]). Sin mutación ni tiempo, el puntero no tiene qué distinguir. |

## 4. Las dos igualdades, y los niveles que vienen después

El candidato "verdadero por definición" apunta a una distinción que la teoría de tipos ya tiene y que es el corazón de los paths.

- `a ≡ b`, igualdad definicional. La decide el reductor: ambos lados llegan a la misma forma normal. No requiere evidencia; es un juicio. Es lo que uno comprueba con lápiz.
- `a = b`, igualdad proposicional. Es un tipo. Requiere un término que la habite, un camino. Ese término puede ser `refl` cuando `a ≡ b`, puede necesitar inducción, o puede quedar como hueco.

La relación entre ambas es la regla que hace funcionar todo: si `a ≡ b`, entonces `refl a : a = b` tipa. Así, "el test es el propio código" (audio 2026-08-31 19.48.17 [05:04]) se vuelve literal: comprobar una instancia `f 2 = g 2` es reducir ambos lados y ver que `refl` tipa. Probar `Π (n : N). f n = g n` es construir el camino general.

Los demás niveles de equivalencia que piden los audios (2026-05-30 18.01.53 [02:42]) se definen como tipos encima de estos dos, sin tocar el núcleo:

- `A ≃ B`, isomorfismo: dos funciones y dos caminos que dicen que se cancelan.
- `a ≈ b` con umbral ε y muestra: equivalencia estadística, que es donde entra Bayes.
- misma representación en memoria, mismo costo, etc.: decoraciones sobre caminos.

Si `A ≃ B` implica `A = B` (univalencia) es una decisión posterior. Se puede postular como hueco, `ua : (A ≃ B) → (A = B)` sin cuerpo, con la consecuencia conocida: lo que depende de ese hueco no reduce.

## 5. El programa como dato

`Program` es un tipo inductivo definido en Luthier: una lista de definiciones, donde una definición es un nombre, un término que es su tipo, y un cuerpo opcional. La sintaxis de los términos es otro tipo inductivo, `Term`, con un constructor por cada forma de la sección 2 y de la sección 3. Con eso, las operaciones sobre programas son funciones ordinarias de Luthier:

- `huecos : Program → List Name`, qué falta definir.
- `check : Program → Maybe Errors`, cada cuerpo tiene el tipo declarado, no hay ciclos, no hay nombres repetidos sin `#`.
- `combinar : Program → Program → Maybe Program`, la operación "combinar DAGs" del audio 2026-05-29 15.11.47 [02:09]. Falla si hay conflicto. Eso es compilar, y es lo que hace que existan programas no compilables (audio 2026-09-02 10.53.08 [02:30]).
- `eval : Program → Name → Maybe Term`, reducir una definición a forma normal.

Lo único primitivo acá es el pacto de arranque: la implementación (lo poco que se escribe en C, audio 2026-05-30 18.01.53 [03:48]) acepta un valor de `Program` y lo trata como programa. Todo lo demás es metacircular, como el evaluador de Lisp.

`eval` es parcial y devuelve un dato. No hay un `eval` que inyecte términos arbitrarios dentro del sistema de tipos. Esa restricción es la que impide el auto-hackeo del audio 2026-08-31 19.57.14 [00:11] y mantiene el núcleo consistente. "El código es el primer elemento" (audio 2026-05-29 14.36.03 [02:38]) se cumple porque `Program` es un dato desde el arranque, sin necesidad de un operador `quote`.

## 6. Lo que queda fuera del núcleo, y por qué

- Números concretos (`R`, punto flotante, matrices): estructuras definidas con `data` y con huecos para lo que el entorno provee. El error, el intervalo y la muestra son `Σ`.
- El functor olvido: es la primera proyección de un `Σ`, o cualquier función no inyectiva. El audio 2026-06-05 13.16.35 [00:44] ya lo dice: olvidar es proyectar. Qué olvidar y cuándo es política de librería. La ley del audio 2026-05-29 15.04.28 [00:39] (olvidar y aplicar da lo mismo que aplicar y olvidar) es un camino que se prueba caso por caso.
- Lo externo: un hueco que el entorno llena. Cómo lo llena (protocolo, serialización) es asunto de cada implementación de Luthier.
- Probabilidad, base de datos de corridas, estimación de costo: librerías que decoran caminos con `Σ`.
- Punteros, mutación, secuencia, clases, herencia, control de flujo: no existen. `if` es el recursor de `Bool`. `while` es recursión. La secuencia es dependencia.

## 7. De dónde viene cada pieza

- Del cálculo lambda: la sección 2 completa.
- De Lisp: la sección 5. El código es dato porque la sintaxis es un dato, y `eval` es una función sobre ese dato.
- De C++: la separación entre declaración y definición, que acá es el hueco. Y los templates, que acá son `Π` sobre `U`.
- De Python: el tipo se puede omitir y se infiere. La superficie tiene que leerse en voz alta.
- De Knuth: dos cosas. El criterio de que un algoritmo se escribe para que una persona lo siga con lápiz. Y la programación literaria: cada definición lleva su explicación. Propuesta: la definición tiene un cuarto campo, el texto en prosa, y `Program` lo conserva. Un programa Luthier se lee como un documento.

## 8. Ejemplo ejecutado a mano

Un programa de siete definiciones. El orden es arbitrario.

    N : U := data { zero : N ; succ : N → N }

    recN : Π (P : U). P → (N → P → P) → N → P
      con reglas   recN P z s zero      ≡ z
                   recN P z s (succ n)  ≡ s n (recN P z s n)

    add : N → N → N := λ m. λ n. recN N m (λ _. λ k. succ k) n

    doble#1 : N → N := λ n. add n n
    doble#2 : N → N := λ n. recN N zero (λ _. λ k. succ (succ k)) n

    test_2 : doble#1 2 = doble#2 2 := refl N 4

    dobles_iguales : Π (n : N). doble#1 n = doble#2 n

Abreviaturas para la corrida: `1 := succ zero`, `2 := succ 1`, `4 := succ (succ 2)`, `s := λ _. λ k. succ k`, `t := λ _. λ k. succ (succ k)`.

Reducción de `doble#1 2`:

    doble#1 2
    ≡ add 2 2
    ≡ recN N 2 s 2
    ≡ s 1 (recN N 2 s 1)              regla succ, con 2 = succ 1
    ≡ succ (recN N 2 s 1)             dos sustituciones
    ≡ succ (s 0 (recN N 2 s 0))       regla succ, con 1 = succ 0
    ≡ succ (succ (recN N 2 s 0))
    ≡ succ (succ 2)                   regla zero
    ≡ 4

Reducción de `doble#2 2`:

    doble#2 2
    ≡ recN N zero t 2
    ≡ t 1 (recN N zero t 1)
    ≡ succ (succ (recN N zero t 1))
    ≡ succ (succ (t 0 (recN N zero t 0)))
    ≡ succ (succ (succ (succ (recN N zero t 0))))
    ≡ succ (succ (succ (succ zero)))
    ≡ 4

Verificación de `test_2`: el tipo declarado es `doble#1 2 = doble#2 2`. Como `doble#1 2 ≡ 4` y `doble#2 2 ≡ 4`, ese tipo es definicionalmente `4 = 4`, y `refl N 4 : 4 = 4`. Tipa. Ese es el test de la instancia, y correrlo fue reducir.

`dobles_iguales` no tiene cuerpo: es un hueco. Llenarlo exige inducción sobre `n` (el recursor dependiente, que la sección 3 todavía no fija) y un lema, `add (succ m) n = succ (add m n)`. Mientras es hueco, el programa entero sigue siendo válido: `test_2` y todo lo demás reducen; solo lo que dependa de `dobles_iguales` queda quieto. Y mientras es hueco, `doble` a secas no se puede usar; hay que elegir `doble#1` o `doble#2`. Cuando se llene, `doble` queda disponible y elegir cuál correr es una decisión de costo, que es la capa empírica de los audios.

Olvido, en tres líneas sobre el mismo programa:

    Anotado : U := Σ (v : N). (v = doble#1 2)
    a : Anotado := (4, refl N 4)
    olvidar : Anotado → N := fst

`olvidar a ≡ 4`. La anotación se fue; el valor quedó.

## 9. Lo que este núcleo deja abierto

- La sintaxis concreta. Lo de arriba es notación matemática; hay que elegir una superficie que se lea.
- Recursor simple o dependiente para `data`. Para probar caminos por inducción hace falta el dependiente.
- Universo con niveles o sin ellos.
- Univalencia: postulada, computable, o ausente.
- El protocolo con que una implementación llena huecos y reporta corridas.
- Si el campo de texto de la definición es obligatorio.
