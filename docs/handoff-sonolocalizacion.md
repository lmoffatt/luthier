# Luthier en Sonolocalización: nota de traspaso

Para la sesión de trabajo del repo de Sonolocalización. Estado de Luthier al 2026-10-01, commit `8fc7f84` y siguientes en `~/Projects/luthier`.

## Qué es y qué hace hoy

Luthier es un lenguaje donde un tipo lleva las leyes que sus valores cumplen, y declarar `x : T` con `T` un subtipo con leyes deja una obligación que `luthier test` corre con casos generados y certifica. En la versión 0 no demuestra: testea y guarda el certificado con hash del código, semilla, generadores y casos.

En Sonolocalización la idea acordada es que Luthier solo describa: tipos, leyes, `extern` a las rutinas de Python que ya existen, y `test`. Ninguna función con cuerpo que no sea trivial. Si una función necesita cuerpo, va en Python y se importa con `extern`.

## Instalar y correr

    pip install -e ~/Projects/luthier      # en el entorno donde corre Sonolocalización (miniconda)
    luthier check archivo.lut -v
    luthier test archivo.lut [--seed N] [--size K] [--show-cases]
    luthier eval archivo.lut "término"

Los `.lut` de Sonolocalización van en su repo, por ejemplo `luthier/estimadores.lut`. Los `extern` apuntan a módulos de Python importables desde ese entorno.

## La receta para luthierizar una rutina

    import "real"                                    -- abs, toR, approx, Positive

    Signal : U := extern "python:numpy.ndarray"      -- tipo opaco: los arrays pasan sin tocarse
    gen Signal := extern "python:luthier.pygen.normal_signal"   -- o uno propio: fn(rng, size) -> ndarray

    shift : Signal -> R -> Signal := extern "python:sono.signals.shift"
    delay : Signal -> Signal -> R := extern "python:sono.estimators.delay"

    DelayEstimator : U := { f : Signal -> Signal -> R |
        \ (x : Signal) { approx 0.000001 (f x x) 0.0 }                              -- cero para idénticas
      & \ (x : Signal) (d : Lag) { approx 0.01 (f x (shift x d)) d }                -- recupera un retardo conocido
      & \ (x y : Signal) { approx 0.000001 (f x y) (0.0 - f y x) }                  -- antisimetría
    }
    Lag : U := { d : R | 0.0 - 20.0 <= d and d <= 20.0 }

    myDelay : DelayEstimator := delay
    test myDelay with 200

Las leyes van en el tipo, con la función primero y las variables cuantificadas después. Cada variable se genera según su tipo: `R` y `Int` con los generadores de `random` (importar `random` si se quieren en Luthier; sin importarlo hay un respaldo en Python que el certificado marca como tal), un subtipo por rechazo sobre su base, un tipo opaco con el generador de Python que se le registre. `test` corre `n` casos con tamaño creciente; el primer contraejemplo suele aparecer en el borde del dominio.

Dos implementaciones del mismo estimador se declaran contra el mismo subtipo, y el certificado dice cuál cumple qué. Una ley que se cree cierta y falla es información: el contraejemplo trae los valores.

## Qué existe en `lib/`

`real` (abs, toR, approx, Positive), `random` (Gen y generadores en Luthier), `peano` (naturales conceptuales), `algebra` (leyes y estructuras). `core.lut` se carga solo. Los ejemplos en `examples/` muestran cada cosa; `signal.lut` es el más cercano a Sonolocalización.

## Lo que probablemente falte, y hay que traer de vuelta a Luthier

- Registros con campos nombrados para funciones que devuelven varias cosas (hoy: pares anidados, o un tipo opaco de Python).
- Un tipo opaco no tiene `==`; comparar señales es una función `extern` a `R` y una tolerancia.
- Generadores de señales realistas (chirps, ruido con espectro dado) son Python: `luthier.pygen` tiene tres básicos; los propios se registran igual.
- Rendimiento: el evaluador es un intérprete en Python; con 200 casos y arrays de miles de muestras el costo lo dominan las rutinas externas, no Luthier. Si un `test` tarda, bajar `n` o el largo de la señal que produce el generador.
- Todo lo que sea "esto no se puede expresar" se anota y vuelve al repo de Luthier como caso de diseño. Ese es el trato: Sonolocalización define las leyes; Luthier crece donde las leyes lo pidan.
