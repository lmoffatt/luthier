# Gramática de Luthier, borrador 0

2026-09-29. Notación EBNF: `::=` define, `|` alterna, `[ ]` opcional, `{ }` repetición (cero o más), `" "` literal. Para no confundir con los símbolos del lenguaje, los literales van siempre entre comillas.

Dos capas. El núcleo es lo que `Term` representa y lo que se ejecuta a mano. La azúcar es todo lo demás, y cada regla trae su traducción al núcleo. Regla de admisión: una azúcar que exigiera un constructor nuevo en `Term` no es azúcar.

## 1. Léxico

    nombre    ::= letra { letra | dígito | "_" | "'" }     -- los que empiezan en mayúscula son tipos y predicados por convención, no por regla
    número    ::= dígito { dígito } [ "." dígito { dígito } ]
    string    ::= '"' { carácter } '"'
    comentario ::= "--" hasta fin de línea

Palabras reservadas: `data`, `match`, `extern`, `test`. Nada más. `U`, `Unit`, `Bool`, `N`, `R`, `List`, `Maybe`, `Resultado` son nombres de definiciones de la librería base, no palabras reservadas.

(2026-10-04: lo anterior quedó corto. Las reservadas del intérprete son quince: `data`, `match`, `extern`, `test`, `with`, `exhaustive`, `gen`, `import`, `forget`, `U`, `operator`, `if`, `then`, `else`, y `provisional` como calificador de `extern`. `and`, `or`, `mod` son nombres comunes con tratamiento infijo.)

## 2. Núcleo

    programa  ::= { definición }

    definición ::= nombre ":" término [ ":=" término ]         -- sin ":=" es un hueco
                 | nombre "=" término                           -- (2026-10-04) alias: se expande antes de verificar, no tiene estados; 05 R7
                 | nombre ":" término ":=" "extern" [ "provisional" ] string
                                                                -- hueco que el entorno llena por ese nombre
                 | nombre ":" "U" ":=" "data" "{" { constructor } "}"     -- (2026-10-04) solo para tipos recursivos; 05 R4

(2026-10-04: la forma no cambia, cambia lo que acepta. `nombre : T` declara; un `nombre := t` posterior lo define, y si `t : T` es un habitante, si `t : T -> Bool` o es una `Law` sobre `T`, `nombre` es el subtipo `{ x : T | t x }`. El mismo `:` para "es un valor de" y "es un subtipo de": la relación es refinamiento y el cuerpo decide; `05` R6. Un `extern` da un valor de un tipo definido, nunca un tipo; `provisional` levanta las dos exigencias y queda como deuda; `05` R5. El núcleo completo, con su reducción, está en `04-kernel.md`; esta sección queda como su primera versión.)

    constructor ::= nombre ":" término                          -- el término es el tipo del constructor; su codominio es el data que se define

    término   ::= átomo
                | término átomo                                 -- aplicación, asocia a la izquierda
                | "\" nombre "{" término "}"                    -- lambda
                | "(" nombre ":" término ")" "->" término       -- Π
                | término "->" término                          -- Π no dependiente, asocia a la derecha

    átomo     ::= nombre | número | string | "U" | "(" término ")"

Eso es todo el núcleo: siete constructores de `Term` (`ref`, `lam`, `app`, `pi`, `univ`, `con`, `rec`) más la declaración de `data`. Los constructores y el recursor de un `data` son nombres ordinarios en el programa una vez declarado el `data`.

Precedencias, de mayor a menor: aplicación; operadores de usuario según su declaración; `*` y `+` sobre tipos; `->`; `:=`.

## 3. Azúcar sobre definiciones

    definición ::= nombre { binder } ":" término ":=" término
        -- f (x : A) (y : B) : C := t   ≡   f : (x : A) -> (y : B) -> C := \ x { \ y { t } }

    binder    ::= "(" nombre { nombre } ":" término ")"
        -- (x y : N)   ≡   (x : N) (y : N)

    definición ::= nombre { binder } ":" término { cláusula }
        -- cláusulas por patrones; se traducen a match anidados sobre los parámetros

    cláusula  ::= "|" patrón { "," patrón } ":=" término

    definición ::= nombre ":=" término
        -- tipo inferido; a mano se escribe siempre

## 4. Azúcar sobre términos

    término   ::= "\" "(" nombre { nombre } [ ":" término ] ")" "{" término "}"
        -- \ (x y) { t }   ≡   \ x { \ y { t } };  el tipo, si se da, sirve al verificador

    término   ::= "match" término "{" { rama } "}"
        -- recursor del data del término; una rama por constructor, sin repetir ni faltar
    rama      ::= patrón "->" término
    patrón    ::= nombre { patrón } | "(" patrón { "," patrón } ")" | "_"
        -- constructor aplicado a subpatrones; el par (a, b); comodín

    término   ::= "if" término "then" término "else" término
        -- match sobre Bool

    término   ::= término "*" término        -- (_ : A) × B; tipo de pares no dependiente
              | "(" nombre ":" término ")" "*" término     -- Σ dependiente
              | "(" nombre ":" término ")" "*" "(" nombre ":" término ")"   -- (2026-10-04) producto con las dos posiciones nombradas
              | término "+" término           -- suma; con más de dos sumandos es Variant. (2026-10-04) primitiva; inyecta con left y right
              | "(" nombre ":" término ")" "+" "(" nombre ":" término ")"   -- (2026-10-04) suma con nombres
              | "<" nombre ":" término { "|" nombre ":" término } ">"      -- (2026-10-04) suma con nombres n-aria; inyección por etiqueta, match sobre etiquetas
              | "(" término "," término { "," término } ")"    -- par, asocia a la derecha
              | "{" patrón ":" término "|" término "}"         -- subtipo: { x : T | p }  ≡  Subtype T (\ x { p })
              | "{" { nombre ":" término } "|" término "}"     -- subtipo con componentes nombradas; ≡ { (a, b, ...) : A * B * ... | p }
              | "{" { nombre ":" término } "}"                 -- (2026-10-04) producto con etiquetas, sin ley: es A * B * ... con nombres para sus posiciones
              | "[" [ término { "," término } ] "]"            -- lista
              | "'" "{" término "}"           -- quote: la sintaxis como Term
              | "$" "{" término "}"           -- unquote, solo dentro de un quote
              | término operador término      -- operadores de usuario, declarados con precedencia

    término   ::= "{" { definición } término "}"
        -- bloque: definiciones locales y un resultado; es un Program chico con salida
        -- (propuesta; no decidido)

## 5. Predicados y subtipos, como librería

Nada de esto es gramática; son definiciones de la librería base que la azúcar `|` y `{ | }` usan.

    Result (E : U) : U := data { ok : Result E ; fail : E -> Result E }
    Failure (A : U) : U := (law : A -> Bool) * (arg : A)
    Predicate (A : U) : U := A -> Result (Failure A)
    Subtype (T : U) (P : Predicate T) : U := (x : T) * Certificate (P x)
    forget : Subtype T P -> T := fst

    (P & Q)  := \ a { match P a { fail e -> fail e ; ok -> Q a } }        -- conjunción, para en el primero
    (P |> Q) := \ a { match P a { fail e -> fail e ; ok c -> Q (a, c) } }  -- refinamiento: Q sobre el subtipo
    sampled (n : N) (law : A -> Bool) : Predicate A                          -- genera n casos, devuelve el primer fallo

Nombres del lenguaje y de la librería en inglés; la documentación en castellano.

`{ x : T | p }` es `Subtype T (\ x { p })`. Cuando el predicado acopla varias funciones, las componentes se nombran a la izquierda del `|`, una por línea, y es azúcar del subtipo sobre el producto. Es la forma en que un libro de álgebra escribe una estructura: operaciones con su tipo, y las leyes que cumplen. El `n` de `muestreado` no va en el tipo: va en el certificado, y lo fija el `test` que lo produce.

## 6. Ejemplo completo en esta gramática

    N : U := data { zero : N ; succ : N -> N }

    add (m n : N) : N
      | m, zero   := m
      | m, succ n := succ (add m n)

    sub (m n : N) : N
      | m,      zero   := m
      | zero,   succ _ := zero
      | succ m, succ n := sub m n

    AdditiveInverse (s : N -> N -> N) (x y : N) : Bool := s (add x y) y == x
    BoundedInverse  (s : N -> N -> N) (x y : N) : Bool := y <= x -> add (s x y) y == x

    Subtraction := { r : N -> N -> N | AdditiveInverse r & BoundedInverse r }

    subtraction : Subtraction := sub     -- hueco hasta que un test produzca el certificado; lo que depende de él espera
    test subtraction with 1000           -- corre las leyes con 1000 casos; ok: certificado n = 1000; fail: contraejemplo

(2026-10-04: con `05`, `Subtraction` puede escribirse como un nombre declarado y después definido por sus leyes. Declarado, `Subtraction : N -> N -> N`, con las leyes como definiciones sobre él, `AdditiveInverse (s : Subtraction) (x y : N) : Bool := ...`; y definido, `Subtraction := AdditiveInverse & BoundedInverse`. Declaración, leyes y definición forman un ciclo, que es el objeto; `subtraction` es una rama, un valor de él. La forma de esta sección, el subtipo escrito de una vez, sigue valiendo. En `Ring`, la base con etiquetas es un producto; si las leyes no tocan todas sus etiquetas, la definición se rechaza; `05` R3.)

    Ring (A : U) := {
      add  : A -> A -> A
      mul  : A -> A -> A
      zero : A
      one  : A
      |
      Associative add & Commutative add & Identity add zero
      & Associative mul & Identity mul one
      & Distributive add mul
    }

    Field (A : U) := { r : Ring A, inv : A -> A | Inverse r.mul inv r.one }     -- subtipo sobre subtipo

Las leyes son predicados con la operación primero y las variables cuantificadas después, para que la aplicación parcial sea el predicado sobre el que el `test` genera casos:

    Associative (A : U) (f : A -> A -> A) (x y z : A) : Bool := f (f x y) z == f x (f y z)

`Associative A` es a la vez el predicado sobre `A -> A -> A` y, por el doble uso del nombre, el subtipo `{ f : A -> A -> A | Associative A f }`. Dentro del `|` está en posición de predicado. `add in Associative A` sería azúcar de `Associative A add`; no adoptada todavía.

Alternativa a evaluar: la ley en el tipo de la componente en vez de en el `|`, `add : Associative A & Commutative A`, `zero : Identity add`, dejando el `|` para las leyes que cruzan componentes (`Distributive add mul`). Más compacto; cuesta un `forget` implícito en cada uso de la componente.

## 7. Abierto

(2026-10-04: lo que `04` y `05` cierran de esta lista: la forma de `test` (directiva del archivo y comando; corre las obligaciones del nombre y de su objeto, y certifica con un grado, `05 §7`), el acceso a componentes (punto, `§8`), la declaración de operadores (`operator`, `§8`), y el modo de comprobación, que vive en el certificado y no en el tipo. Sigue abierto lo demás.)

- Cómo una ley con variables cuantificadas (`InversaAditiva r : N -> N -> Bool`) se vuelve un `Predicate` sin fijar `n`: el modo de comprobación (muestreo con `n`, exhaustivo, demostración) queda abierto en el tipo y lo cierra el `test`, registrándolo en el certificado. Es la forma de `Veredicto`.
- Sintaxis para la evaluación guardada `(quote, valor)`; candidatos `[| f x |]` o un prefijo con llaves.
- Acceso a componentes de un subtipo con nombres (`r.mul`): notación de punto o funciones proyección generadas.
- Forma exacta de `test`: si es una definición más (produce el certificado como dato) o un comando fuera del programa.
- Declaración de operadores de usuario y sus precedencias.
- Bloques con definiciones locales.
- Índices de de Bruijn o nombres únicos para las variables ligadas (afecta a `Term`, no a la gramática).


## 8. Lo que fijó la implementación (2026-09-30)

El intérprete de versión 0 está en `src/luthier/`. Al escribirlo se decidieron cosas que la gramática dejaba sueltas:

- Palabras reservadas: `data`, `match`, `extern`, `test`, `gen`, `forget`, `U`. `and`, `or` y `mod` son nombres comunes con tratamiento infijo, así el preludio los define en Luthier.
- Las leyes viven en el tipo. `Def` tiene tres campos, nombre, tipo y cuerpo. Una definición cuyo tipo declarado (tras pelar los binders) es un subtipo genera una obligación: el predicado aplicado al valor, cuantificado sobre los parámetros. `test nombre` corre las obligaciones de esa definición.
- Un valor cerrado contra un subtipo se comprueba al verificar: `x : Z7 := 9` es un error de tipos. Con variables libres, se difiere a `test`.
- Un valor de subtipo pasa donde se espera el tipo base sin escribir `forget` (la coerción va en una sola dirección).
- Componentes de un subtipo: una por línea o separadas por `,`. Los nombres de componentes son ligaduras y pueden coincidir con constructores (`zero`).
- `test` es una directiva del archivo, `test nombre with n` o `test nombre exhaustive`, y también un comando de línea. Produce `archivo.cert.json`.
- Exhaustivo: `Bool`, `data` sin recursión, `Int` en un rango configurable, subtipos de esos por filtrado. Lo demás se muestrea; los `data` recursivos se generan por constructor con profundidad acotada.
- `Ring` en el preludio lleva `neg` y las leyes de inverso. Sin ellas es `Semiring`, y `(or, and)` sobre `Bool` lo satisface: el test lo mostró antes que yo.
- Sin parámetros implícitos: `nil N`, `cons N x xs`.
- `import "archivo.lut"` une las definiciones de otro archivo (rutas relativas al que importa, después la librería base; `.lut` opcional). Es el `combinar` de los docs: idempotente, y un ciclo o una definición repetida con cuerpo son errores. `core.lut` se importa solo; con `--no-core` se escribe `import "core"`.

- Generadores en Luthier (2026-09-30): `Gen (A : U) := Nat -> Int -> A * Int` en el preludio, tamaño y semilla a valor y semilla siguiente, con un generador congruencial en aritmética de `Int`. Por defecto `genInt`, `genNat`, `genN`, `genBool`, `genR`, y `genList` parametrizado. La directiva `gen T := término` elige el generador de un tipo (el término tiene que ser un `Gen T`); `gen T := extern "python:mod.fn"` uno de Python, llamado como `fn(rng, size)`. Un solo parámetro `size` acota todo valor generado y crece de 1 al tope a lo largo de una corrida muestreada; `test x with n size k` o `--size k` lo fijan. El certificado registra qué generador se usó por variable. Lo que queda en Python: la semilla de cada llamada sale del flujo aleatorio de la corrida, y la derivación de un generador para un `data` sin `gen`, hasta que un programa pueda inspeccionar declaraciones.
- Coerción por componentes: un valor de tipo `A * B` donde se espera `A' * B` con `A'` subtipo de `A` se acepta proyectando con `match` y la obligación cae sobre la proyección.
- Líneas de continuación: dentro de una definición de nivel superior, una línea indentada continúa la anterior.
- `Int`, `R` y `String` son definiciones (2026-10-01, tarde): huecos declarados en `core.lut`, que el intérprete llena con sus literales, aritmética y comparaciones. Antes estaban cableados en el intérprete (`BUILTIN_TYPES`), contra lo que dice la sección 1; ahora el intérprete solo reserva `Law`. Lo que se puede decir de `R` (su épsilon, sus operaciones como funciones) va en `lib/real.lut`.
- Sin preludio (2026-10-01): lo implícito es `core.lut`, solo lo que el elaborador nombra (`Bool` con `and`/`or`/`implies`, `List`, `Maybe`, `Unit`, `Nat`). El resto son librerías en `lib/`, importadas por nombre: `real` (abs, toR, approx, Positive), `random` (Gen y generadores), `peano` (N), `algebra` (leyes y estructuras). El criterio: es núcleo lo que el intérprete necesita para funcionar; todo lo demás se pide.
- Lo que `04` y `05` revierten (2026-10-04). Cuatro decisiones de esta lista dejan de valer: el chequeo en el orden del archivo (el verificador lee el programa entero, arma el grafo y chequea por objetos, sus componentes fuertemente conexas, `05 §2`); los registros `{ ... | true }` como forma de nombrar componentes sin ley (son el producto con etiquetas, sin `|`, y se nombran con un alias, `05` R3, R4, R7); que `T : U := extern` dé un tipo opaco (un extern da valores, nunca tipos, `05` R5); y que `Bool`, `Maybe` y los `data` no recursivos sean `data` (son sumas, `04 §2`). Se agregan el calificador `provisional` de `extern`, el alias con `=`, la suma primitiva y la suma con nombres `< ... >`.
- Proyección de componentes (2026-10-01): `e.position` es la componente `position` de un valor cuyo tipo es un subtipo con componentes nombradas; se elabora al `match` de una rama sobre el patrón del tipo, y se imprime como se escribió. Vale también tras un paréntesis, `(f x).campo`, y a través de refinamientos (`{ s : Scene | p }` tiene las componentes de `Scene`). El punto es el mismo de la calificación de módulos y no hace falta otro símbolo (`::` quedó descartado): un módulo es un registro cuyas componentes son sus definiciones, así que calificar es proyectar. La regla de resolución: primero el nombre entero como nombre calificado; si no existe, el prefijo más largo que sea variable o definición, y una proyección por segmento restante. El subtipo con componentes nombradas es ahora un producto dependiente, `{ n : Int, m : { k : Int | k <= n } | ... }`: el tipo de una componente puede mencionar las anteriores, y el tipo de `d.m` las sustituye por proyecciones de `d`.
