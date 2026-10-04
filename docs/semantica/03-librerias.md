# Librerías: qué es un módulo, cómo se importa, qué viaja con él

Borrador 0, 2026-09-30. Implementado en `src/luthier/cli.py` (cargador) y `certify.py`.

## 1. Un archivo es una estructura

Un `.lut` es un conjunto de definiciones con dependencias entre sí, y eso denota un valor de un tipo Σ con componentes nombradas: `a : A := ..., b : B a := ...` es un término de `(a : A) * (b : B a) * ...`, donde las leyes de cada definición son los subtipos de cada campo. Un archivo es lo mismo que `Ring`: una estructura. Es la lectura de los módulos de ML como registros dependientes.

Consecuencias: la signatura de una librería es su tipo; dos librerías intercambiables son dos valores del mismo tipo; una librería parametrizada es una función de módulo a módulo; y una librería con huecos es un functor cuyos parámetros son los huecos, que el importador llena.

En versión 0 el módulo no se construye como valor Σ: se implementa por prefijado de nombres. El modelo conceptual es el registro; la implementación llega cuando haga falta pasar un módulo como argumento.

## 2. Importar

    import "x.lut"            -- plano: las definiciones entran al espacio del importador; colisión con cuerpo es error
    import "x.lut" as m       -- calificado: se alcanzan como m.f; sin colisiones

Búsqueda: al lado del archivo que importa, después los directorios de `LUTHIER_PATH`, después `lib/` del paquete. `.lut` es opcional. Importar dos veces bajo el mismo prefijo no hace nada; el mismo archivo puede cargarse bajo dos prefijos distintos. Un ciclo es error. `core.lut` se importa solo; con `--no-core` se escribe `import "core"`.

Resolución de nombres dentro de un módulo `m`: primero `m.x` (lo propio), después `x` (los globales: core y lo importado plano en la raíz). Un módulo no ve las definiciones de quien lo importa. Los constructores y los `data` se prefijan igual que las funciones.

## 3. Declaración e implementación: el hueco como parámetro

Un archivo puede declarar `sqrt : SquareRoot` sin cuerpo, con las leyes en el tipo, y otro archivo darle cuerpo, `sqrt := extern "python:math.sqrt"`. El tipo de la implementación, si se escribe, tiene que coincidir con el declarado; si se omite, se hereda. Las leyes del tipo declarado pasan a ser obligaciones de la implementación. Así una especificación tiene tantas implementaciones como archivos la llenen, y todas se comparan contra las mismas leyes. Es la separación declaración e implementación de C++, y es el functor de ML: el hueco es el parámetro.

(2026-10-04: esto sigue valiendo para valores: un hueco de un tipo definido, con sus leyes en el tipo, se llena en otro archivo con un cuerpo nativo o con un extern, y hereda las leyes como obligaciones. Lo que cambia es que un extern da valores, nunca tipos (`05` R5): los tipos se definen nativamente, y el estilo en que un archivo declaraba un tipo opaco con sus operaciones y otro lo llenaba con externs desaparece. En su lugar, el objeto es una teoría (un tipo registro con leyes) y cada implementación es un valor de ella, un modelo dado con un literal de registro, `pyCodec : Codec := { parse := extern "...", ... }`; `05 §1` y `§8`. Así el modelo da todas sus operaciones a la vez, que es lo que este documento leía en §1 como un archivo que es una estructura. `extern provisional` exime de definir el tipo y queda registrado como deuda.)

## 4. Qué viaja: el certificado con hash

`luthier test x.lut` escribe `x.cert.json` con, por definición, las leyes corridas, el modo, los casos, el resultado, y un hash del **cono de dependencias**: la definición y todo lo que referencia, transitivamente, escrito con el prefijo del módulo quitado. Cambiar `addN` cambia el hash de todo lo que lo usa.

Al importar un archivo se lee su certificado. Una entrada se acepta si pasó y su hash coincide con el cono actual; la definición queda **certificada** y `test` no la vuelve a correr salvo `--deep`. Si el hash no coincide, la entrada es **stale** y la obligación vuelve a estar pendiente. `luthier check -v` muestra el estado de cada una.

(2026-10-04: lo que se certifica es una ley aplicada a valores concretos, con un grado: un punto, muestreado `n`, exhaustivo, atestiguado; "certificada" es el resumen de esas entradas, no un estado fijo del nombre; `05 §7`.)

Las leyes del importador que mencionan funciones importadas son obligaciones del importador y se corren siempre. Un certificado heredado trae el `n` y el modo con que se produjo; quien quiera más garantía corre `--deep`.

Por defecto `luthier test` corre las directivas de los archivos dados en la línea de comandos y escribe sus certificados; lo importado se acepta o se reporta como pendiente. `--name m.f --deep` corre una definición importada y escribe en el certificado de su archivo, con nombre local y hash canónico.

## 5. Abierto

- Módulos como valores pasables (`fft : FFTLib := import "fft.lut"`), y functores explícitos. (2026-10-04: menos urgente: una implementación ya es un valor, el modelo de una teoría, y se pasa como cualquier otro.)
- Visibilidad: en versión 0 todo es público. Lo privado son definiciones locales de un bloque, cuando existan los bloques.
- Los `extern` hacen que un `.lut` dependa de paquetes de Python; hoy eso no se declara en ningún lado.
- (2026-10-04) Si un archivo que importa una definición `provisional` puede certificarse, o hereda la marca.
- Un `test` que corre dentro de un módulo importado escribe en el certificado del módulo; falta decidir si el importador puede exigir un `n` mínimo en el tipo o en la directiva.
