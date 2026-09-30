# Gramática de Luthier, borrador 0

2026-09-29. Notación EBNF: `::=` define, `|` alterna, `[ ]` opcional, `{ }` repetición (cero o más), `" "` literal. Para no confundir con los símbolos del lenguaje, los literales van siempre entre comillas.

Dos capas. El núcleo es lo que `Term` representa y lo que se ejecuta a mano. La azúcar es todo lo demás, y cada regla trae su traducción al núcleo. Regla de admisión: una azúcar que exigiera un constructor nuevo en `Term` no es azúcar.

## 1. Léxico

    nombre    ::= letra { letra | dígito | "_" | "'" }     -- los que empiezan en mayúscula son tipos y predicados por convención, no por regla
    número    ::= dígito { dígito } [ "." dígito { dígito } ]
    string    ::= '"' { carácter } '"'
    comentario ::= "--" hasta fin de línea

Palabras reservadas: `data`, `match`, `extern`, `test`. Nada más. `U`, `Unit`, `Bool`, `N`, `R`, `List`, `Maybe`, `Resultado` son nombres de definiciones de la librería base, no palabras reservadas.

## 2. Núcleo

    programa  ::= { definición }

    definición ::= nombre ":" término [ ":=" término ]         -- sin ":=" es un hueco
                 | nombre ":" término ":=" "extern" string     -- hueco que el entorno llena por ese nombre
                 | nombre ":" "U" ":=" "data" "{" { constructor } "}"

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
              | término "+" término           -- suma; con más de dos sumandos es Variant
              | "(" término "," término { "," término } ")"    -- par, asocia a la derecha
              | "{" patrón ":" término "|" término "}"         -- subtipo: { x : T | p }  ≡  Subtype T (\ x { p })
              | "{" { nombre ":" término } "|" término "}"     -- subtipo con componentes nombradas; ≡ { (a, b, ...) : A * B * ... | p }
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
- `import "archivo.lut"` une las definiciones de otro archivo (rutas relativas al que importa, después la librería base; `.lut` opcional). Es el `combinar` de los docs: idempotente, y un ciclo o una definición repetida con cuerpo son errores. El preludio se importa solo; con `--no-prelude` se escribe `import "prelude"`.
