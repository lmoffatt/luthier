# Qué existe ya, y qué robar

Borrador 0, 2026-09-29. Resultado de cuatro búsquedas paralelas sobre la pregunta "¿existe ya el patrón de construcción con certificado de `01-patron-de-construccion.md`?". Cada mecanismo lleva su fuente. Términos: PBT es property-based testing (leyes corridas sobre entradas generadas); SMT es un demostrador automático para fórmulas de primer orden con aritmética.

## 1. Veredicto

Cada pieza existe en algún lado. La combinación no la encontramos, y hay tres huecos con nombre:

- Nadie empaqueta operaciones con evidencia de test en lugar de prueba. Idris tiene `Semigroup` y `VerifiedSemigroup` (sin nivel intermedio); Lean y Coq exigen la prueba como campo; Scala `discipline` y Haskell `quickcheck-classes` tienen las leyes como datos pero el resultado es un reporte, no un valor atado a la instancia.
- Nadie persiste evidencia de éxito como certificado componible. Hypothesis y proptest guardan solo fallos, por nombre de test. Lean `plausible` termina en `sorry`; Isabelle y QuickChick devuelven un mensaje.
- La verificación gradual tiene un orden de dos puntos (preciso, hueco). El orden de tres (probado, testeado con `n` casos, hueco) no está formulado ni tiene sus garantías probadas. Es un lugar donde Luthier puede decir algo.

Lo más parecido en espíritu: SPARK con "Explicit Assumptions" (Kanig et al., TAP 2014), Frama-C con estados por propiedad "válido bajo hipótesis", y EVE (Eiffel) que junta AutoTest y AutoProof en un score por rutina.

## 2. Qué robar

### 2.1 El certificado como suma con el mismo enunciado

De Lean `plausible`: `TestResult p` tiene `success` con `Unit ⊕ p` (testeado sin prueba, o prueba real) y `failure` con una refutación genuina más el contraejemplo (https://github.com/leanprover-community/plausible/blob/main/Plausible/Testable.lean). De Isabelle: `by eval` deja el teorema marcado como "tainted" por oráculo, visible por inspección.

Para Luthier:

    Certificado P x := probado (evidencia de P x)
                     | testeado RegistroTest
                     | asumido Motivo
    Resultado X     := ok X | refutado Contraejemplo

Mismo `P` en todos los constructores; subir de testeado a probado es cambiar de constructor. Regla de subida automática: `testeado` con modo exhaustivo sobre dominio finito y átomo decidible equivale a `probado` (Isabelle `exhaustive`, Lean `decide`, QuickChick `Dec`).

### 2.2 Contenido del registro de test

De QuickCheck `Result` (la representación más completa que hay: `numTests`, `numDiscarded`, `labels`, `usedSeed`, `usedSize`, `failingTestCase`; https://hackage.haskell.org/package/QuickCheck/docs/Test-QuickCheck.html), de proptest (guarda la semilla, no el valor: `cc <seed> # shrinks to v`; https://proptest-rs.github.io/proptest/proptest/failure-persistence.html) y de Hypothesis (clave = digest de la función de test, valor = secuencia de elecciones del generador; https://hypothesis.readthedocs.io/en/latest/database.html).

    RegistroTest := {
      enunciado    : Hash            -- del enunciado, no del nombre
      generador    : IdGenerador     -- tipo y estrategia: aleatorio | exhaustivo | filtrado por P
      semilla      : Maybe Semilla   -- ausente si exhaustivo
      casos        : N               -- éxitos
      descartes    : N               -- entradas que no cumplieron la precondición
      distribucion : List (Etiqueta × N)
      modo         : Aleatorio | Exhaustivo N | Repeticion (List Semilla)
      version      : Hash            -- del código de las funciones involucradas
    }

El número de casos sin el generador no dice nada (QuickChick: 20000 descartes y 2415 tests triviales de un nodo). Por eso `generador` y `descartes` son obligatorios. Reproducir primero las semillas guardadas y después generar (proptest).

### 2.3 El certificado como cláusula con hipótesis explícitas

De Kanig, Chapman, Comar, Guitton, Moy, Rees, "Explicit Assumptions: A Prenup for Marrying Static and Dynamic Program Verification" (TAP 2014, https://www.adacore.com/uploads/blog/tap.pdf): cada actividad de verificación produce `A1 ∧ ... ∧ An → C`, con etiquetas por subprograma (`Pre(P)`, `Contract(P)`, `Init(P)`, `Term(P)`), y una tabla de qué método externo descarga cada hipótesis. De Frama-C: estado por propiedad (válido, válido bajo hipótesis, inválido, desconocido) con dependencias, consolidado por el kernel (https://julien-signoles.fr/publis/2015_fac.pdf). De SLSA VSA: un certificado de segundo orden que resume otros y cuenta `dependency_levels` (https://slsa.dev/spec/v0.1/verification_summary).

Para Luthier: un certificado no dice "L vale" sino "L vale si valen H1 ... Hn", donde las `Hi` son certificados de otras leyes y de los predicados de tipo de las funciones que la ley menciona. El certificado de un programa es el cierre de esas cláusulas. Con eso se responde "de qué hipótesis no verificadas depende L" y "si A cae, qué cae". `combinar` de dos programas recalcula el cierre. Los sujetos se identifican por digest del material y de las funciones (in-toto: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md), así un cambio en cualquier función invalida el certificado sin lógica extra.

### 2.4 La ley como objeto propio, sobre una signatura

De Larch (trait: `introduces` firma, `asserts` ecuaciones, `implies` consecuencias, semántica loose; https://www.cs.cmu.edu/afs/cs/usr/wing/www/publications/LarchBook.pdf), del `axiom` de C++0x N2887 (https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2009/n2887.pdf) y de Catsfoot, donde los axiomas de un concept se testean con generadores y se mide cobertura de axiomas (https://www.jot.fm/issues/issue_2011_01/article10.pdf).

Ya lo tenemos: `Resta (s : N -> N -> N) : List Ley` es un trait. Dos cosas a agregar. La igualdad con que se compara es parámetro de la ley, no un default (CafeOBJ advierte que la igualdad sintáctica devuelve `false` antes de tiempo; Gaudel: para tipos sin igualdad observable se compara por contextos observables, y el certificado registra cuáles). Y cobertura: el certificado de un concepto dice qué leyes se ejercitaron y cuáles nunca corrieron.

### 2.5 Las hipótesis de selección de Gaudel

De Gaudel, "Testing can be formal too" (1995, https://link.springer.com/chapter/10.1007/3-540-59293-8_188) y Gaudel & Le Gall 2008 (https://arxiv.org/pdf/0804.0970): un test es una instancia cerrada de un axioma; el conjunto exhaustivo es todas las instancias; seleccionar es agregar hipótesis explícitas, uniformidad (pasar un representante implica pasar su clase) y regularidad (pasar todo hasta tamaño `k` implica pasar todo). La fórmula: bajo la hipótesis mínima, pasar el exhaustivo equivale a ser correcto.

Para Luthier: `testeado` significa "válido bajo las hipótesis {generador, n, rango}". Escribirlas como hipótesis en la cláusula de 2.3, en lugar de dejarlas implícitas en un número.

### 2.6 Borrado del certificado en tiempo de ejecución

De Idris 2 (cantidades 0, 1, ω; https://idris2.readthedocs.io/en/latest/tutorial/multiplicities.html) y Agda `@0` (https://agda.readthedocs.io/en/latest/language/runtime-irrelevance.html). Un par `(x : T) × (0 c : Certificado P x)` tiene el certificado en cantidad 0: usable en tipos, ausente en ejecución, sin `match` sobre él. `material = fst` tipa porque la segunda componente es 0.

Distinción que hay que mantener: borrable no es irrelevante. Dos pruebas de `P x` son intercambiables; dos certificados de test no, porque registran corridas distintas. El certificado se borra del valor y vive en el almacén de corridas.

### 2.7 Leyes con herencia sin volver a correr

De Scala `discipline` (`RuleSet` con `parents` y `bases`, `all` funde por nombre; https://github.com/typelevel/discipline/blob/main/core/src/main/scala/org/typelevel/discipline/Laws.scala) y de Stainless (una subclase no puede debilitar una ley: la postcondición fuerza `res && super.ley`; https://epfl-lara.github.io/stainless/laws.html).

Para Luthier: `Grupo A := Monoide A ++ [inversos]` hereda los certificados de `Monoide A` por referencia; no se vuelven a correr. Una extensión solo agrega leyes.

### 2.8 La frontera entre testeado y probado

De SPARK (UG 8 y Comar, Kanig, Moy, ERTS 2012, https://www.adacore.com/uploads/papers/Hi-Lite_ERTS-2012.pdf): probado y testeado se mezclan libremente si al testear B se ejecutan la Pre de lo probado que B llama y la Post de B; los tres supuestos de frontera son pre respetada, valores válidos para su tipo, sin aliasing. De Dafny `--test-assumptions Externs` y Agten et al. 2015: cheques solo en la frontera con lo no verificado.

Para Luthier: al correr los tests de una definición, evaluar también los predicados de tipo de sus entradas y salidas, y contar esas evaluaciones como evidencia para las hipótesis de los vecinos. Un mismo lenguaje de aserciones ejecutable y demostrable (Hi-Lite lo llama "un lenguaje común de especificación entre test y prueba"). Y niveles de aserción (Ada 2022 `Assertion_Level`, SPARKlib `Full`) para leyes que no tiene sentido ejecutar (cuantificadores sobre infinitos), que solo pueden estar probadas o sin probar.

### 2.9 Semántica del hueco y el orden de precisión

De Bader, Aldrich, Tanter (VMCAI 2018, https://pleiad.cl/papers/2018/baderAl-vmcai2018.pdf) y el marco AGT: el hueco `?` significa "cualquier fortalecimiento satisfacible de lo conocido"; una demanda `Q` sobre un valor con certificado parcial se acepta solo si existe un fortalecimiento que implique `Q`, y se rechaza estáticamente si lo conocido contradice `Q`. Eso separa "no sé" de "es falso". Dos garantías graduales: bajar precisión nunca rompe un programa válido, y un error en ejecución nunca se arregla bajando un certificado. Localidad (Lehmann & Tanter, POPL 2017, https://pleiad.cl/papers/2017/lehmannTanter-popl2017.pdf): un hueco en `Certificado P x` solo puede fortalecer `P` sobre `x`, no sobre otras definiciones; sin eso el sistema acepta casi todo.

Para Luthier: `probado ⊑ testeado ⊑ asumido`, con significado por conjuntos de predicados compatibles, y las dos garantías como meta-leyes testeables con el método del retículo de Gradual C0 (degradar certificados de un programa completo y comprobar que sigue verificando; https://arxiv.org/abs/2210.02428). Reformular las garantías para tres puntos es trabajo nuevo.

### 2.10 Un score como vista, no como certificado

De EVE (Tschannen, Furia, Nordio, Meyer, SEFM 2011, https://bugcounting.net/pubs/sefm11.pdf): por rutina, un número en `[-1, 1]`: prueba exitosa 1, test fallido -1, test sin fallo sube con casos y tiempo hasta 0.9, timeout 0; y política por cláusula (un test que refuta una conjunción no invalida las otras). Sirve como resumen legible de un grupo o de un programa. El certificado es la cláusula de 2.3; el score se calcula de ella.

## 3. Qué no robar

- Heap, permisos, footprints, marcos de exclusión: casi todo el esfuerzo técnico de la verificación gradual 2020-2024 es por memoria mutable con aliasing. Para valores construidos e inmutables sobra.
- Motores de WLP y ejecución simbólica sobre comandos: la unidad de Luthier es la definición y la construcción. Tomar las fronteras, no el motor.
- Evidencia con SMT en tiempo de ejecución (Lehmann & Tanter): los autores mismos lo dan por caro. Cheques que se reducen a evaluar una fórmula sobre valores cerrados.
- Los niveles Stone a Platinum de SPARK: son por proyecto y por categoría fija, no por ley ni por definición. Robar "categoría de obligación" (predicado de tipo, precondición, ley entre funciones, terminación), no la escalera.
- El `?` binario tal cual: no tiene el nivel testeado.
- Mezclar en un mismo residuo un cheque dinámico (corre en producción sobre la entrada real) con un test (corre en build sobre una muestra): son evidencias de naturaleza distinta y mezclarlas es unsound. Si un valor testeado evita el cheque dinámico, es una política que el certificado registra.
- Axiomas de C++0x sin chequeo; semántica inicial de OBJ (Luthier certifica un modelo concreto, no la clase de todos); Alloy salvo como generador de modelos finitos; PCC clásico (política del consumidor sobre seguridad de memoria).
- Claves por string de typeclass (`lawsTypeclass`): clavar por hash del enunciado.

## 4. Cambios sobre `01-patron-de-construccion.md`

- `Certificado` pasa a ser la suma de 2.1 y `RegistroTest` el registro de 2.2.
- Un certificado es una cláusula con hipótesis (2.3), no un hecho. El certificado de un programa es el cierre.
- `Ley` recibe la igualdad como parámetro y el certificado de un concepto registra cobertura (2.4).
- Las hipótesis de selección van explícitas en la cláusula (2.5).
- El certificado se borra del valor en ejecución y vive en el almacén de corridas (2.6).
- Conceptos con padres heredan certificados por referencia (2.7).
- Los predicados de tipo se evalúan en las fronteras al testear (2.8).
- Nueva pregunta abierta, y candidata a resultado propio: las garantías graduales para el orden de tres puntos (2.9).
