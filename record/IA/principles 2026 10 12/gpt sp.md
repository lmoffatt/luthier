Sí. Mi impresión es que el documento ha mejorado mucho respecto de las versiones anteriores, pero ahora su problema principal ya no es que falten ideas: es que **hay demasiadas ideas de distinto nivel llamadas “principios”**. El propio documento dice que llegó a 15 principios mediante fusiones y absorciones sucesivas, lo que explica por qué algunos terminaron enormes. principles

## 1. ¿Hay principios de más?

Sí, aunque no porque las ideas sobren. Sobran como **principios independientes**.

Yo veo aproximadamente **9–10 principios reales**. Los 15 actuales mezclan cuatro clases de cosas:

| Tipo de contenido | Ejemplos actuales | Qué haría |
|---|---|---|
| Principio conceptual | L1, L2, L9 | mantener |
| Consecuencia de otro principio | L3, L12 | absorber |
| Regla operacional del runtime/planner | grandes partes de L10, L13 | mover a especificación |
| Detalle de implementación o provenance | hashes, seeds, thread count, memo keys, versiones | sacar del documento de principios |

El caso extremo es **L10**. Empieza como un principio perfectamente claro —“The demand determines the computation and the types produced”— pero luego contiene estrategia de evaluación, dual numbers, memoización, identidad de runs, seeds, thread scheduling, certificates, sessions, cache behavior, subtyping y derivación de propiedades. principles

Eso no es un principio: es casi un capítulo de la especificación.

**L12 tampoco necesita existir como principio independiente.** “No hardcoded constants: every criterion is a parameter” es una consecuencia casi inmediata de G3/L10: si el demandante decide tolerancia, coste, nivel estadístico, etc., esos criterios necesariamente deben ser parámetros. principles

También fusionaría **L5+L6+L7** a nivel de principio. Hay tres cosas distintas técnicamente —igualdad, álgebra de leyes y certificación—, pero conceptualmente constituyen una sola idea:

> Las leyes definen equivalencias/costes y la evidencia certificada de esas leyes se compone explícitamente.

Después la especificación puede volver a separarlas.

---

# 2. Sí hay contradicciones

No todas tienen la misma gravedad. Hay algunas contradicciones bastante concretas y otras que son ambigüedades semánticas peligrosas.

### A. `type`, `structure` y `theory` no forman todavía una jerarquía coherente

En Terms:

> a structure is a type in the kernel language

y:

> a theory is a structure with its law.

principles

Pero G1 dice:

> **A type is a theory and its values are its models.**

principles

Tomado literalmente:

\[
Structure \subset Type
\]

\[
Theory = Structure + Law
\]

pero simultáneamente

\[
Type = Theory.
\]

Entonces ¿un `Int`, un producto o `A -> B` ya son teorías? ¿O solamente se convierten en teorías al asociarles una ley?

Creo que conceptualmente sabes qué quieres decir, pero **el documento usa “type” en dos niveles diferentes**:

1. tipo estructural del kernel;
2. tipo refinado/semántico que representa una teoría.

Eso debería hacerse explícito.

Una formulación mucho más implementable sería:

\[
Theory(S,L)
\]

donde `S` es una estructura del kernel y `L : S -> Bool/Cost`.

Y entonces:

\[
m : Theory(S,L)
\]

significa que `m : S` y existe el certificado de `L(m)`.

Eso elimina muchísimo barro conceptual.

---

### B. L5 permite componer sampled certificates; L13 lo prohíbe

Esta sí es una contradicción textual bastante limpia.

L5 dice que los paths se componen sumando costes y que un sampled link compone sobre la intersección de los dominios certificados. principles

Pero L13 dice:

> a sampled edge is admissible ... **only as a direct edge, never summed into a path**, until a probabilistic bound exists as a law.

principles

Las dos reglas no pueden mantenerse simultáneamente.

Yo conservaría la versión de **L13**, que es más prudente.

L5 debería decir aproximadamente:

> Deterministic cost certificates compose additively. Sampled certificates do not compose transitively unless an explicit law justifies the probabilistic composition.

Eso además deja muy claro el límite entre álgebra de costes y evidencia estadística.

---

### C. L14 dice a la vez que un extern sin ley no corre y que sí puede correr

Primero:

> without a type with a law to validate against it is not applied.

y:

> A function with no laws at all is not a function to run but a hole.

principles

Pero unas líneas más abajo:

> an extern with no law yet [...] is allowed inside a named world [...] the plan shows the world it ran in.

principles

Eso necesita una decisión semántica.

Creo que tu idea correcta es:

**puede ejecutarse, pero no puede participar del universo certificado de Luthier.**

Es decir:

\[
extern\ without\ law
\]

puede tener semántica operacional dentro de un `World`, pero no produce un modelo certificado ni puede ser sustituido por el planner.

Eso es mucho más limpio que decir primero “cannot run” y después permitirlo.

---

### D. L13 llama “quotient/class” a algo que inmediatamente reconoce que no es una relación de equivalencia

L13 dice que las implementaciones forman un quotient y una clase por equivalencia. Pero luego dice que en el caso aproximado la cercanía no es transitiva, y por eso el planner en realidad trabaja sobre un **weighted graph, not a class**. principles

Ahí se están mezclando dos niveles.

En el nivel matemático ideal:

\[
f \sim g
\]

puede ser una equivalencia genuina y formar un quotient.

En el nivel de realizaciones aproximadas:

\[
d(f,g)\le \epsilon
\]

no es una equivalencia transitiva.

Por tanto no deberías llamarlas la misma “class”.

La distinción podría ser magníficamente simple:

> **Semantic equivalence forms classes; certified substitutability forms a graph.**

Creo que esa frase debería aparecer casi literalmente en Luthier.

---

### E. La composición Bool/Cost de L6 todavía no está matemáticamente especificada

L6 afirma que `lift` y `exact` son homomorfismos y que `Bool` es retracto de `Cost`. principles

Pero ¿homomorfismos respecto de qué operaciones?

Por ejemplo:

\[
lift(true)=0,\quad lift(false)=\infty
\]

funciona maravillosamente para

\[
p\land q \leftrightarrow lift(p)+lift(q)
\]

en el sentido cero/no-cero.

Pero `or` naturalmente correspondería a `min`, y `min` ni siquiera aparece entre las operaciones de Cost que acabas de enumerar.

No considero esto una contradicción con otro principio. Es algo quizá peor para implementación: **una afirmación algebraica demasiado fuerte antes de haber definido el álgebra**.

Y el propio documento reconoce que esa álgebra sigue abierta. principles

---

## 3. Hay un principio importante que falta

Paradójicamente, la frase que yo considero más importante de todo el documento aparece escondida en mitad de L10:

> **Three objects, never one: the meaning of a program [...] a realization [...] the evidence, its certificates.**

principles

Esto debería ascender a principio fundamental.

Porque resuelve gran parte de los problemas anteriores:

\[
\boxed{\text{Meaning} \neq \text{Realization} \neq \text{Evidence}}
\]

Un programa significa una cosa.

Un plan produce una realización concreta.

Un certificado dice qué evidencia existe acerca de esa realización.

Creo que ésta es una de las ideas más potentes de Luthier y ahora está enterrada en unas cincuenta líneas de L10.

La convertiría probablemente en **L2**.

---

## 4. También falta un base case claro para las dependencias

Terms dice que toda teoría tiene dependencias, que `Monoid A` depende de `Setoid A`, y que un carrier se supone que viene con los modelos que nombra. principles

Pero entonces aparece inmediatamente la pregunta:

**¿de dónde sale el primer Setoid?**

El propio documento reconoce todavía abierta la cuestión del tipo con su igualdad como base de toda teoría. principles

Esto no necesita necesariamente convertirse en otro “principio”, pero sí debe solucionarse antes de que la arquitectura de tipos sea cerrada. De lo contrario existe riesgo de regresión/circularidad:

\[
A \to Setoid(A) \to ...
\]

Debería haber un base case del kernel.

---

# 5. Yo reduciría los 15 a unos 10

No intentaría conservar la numeración actual. Haría algo aproximadamente así:

| Nuevo | Principio | Absorbe |
|---|---|---|
| P1 | Luthier expresa invariancias como teorías y sus habitantes como modelos | G1, L1, L2, L3 |
| P2 | Meaning, realization and evidence are distinct | parte central de L10 |
| P3 | La incompletitud es explícita: declare → define → inhabit | L4 |
| P4 | Equality, laws and certification compose explicitly | L5, L6, L7 |
| P5 | Ideal theories may have quantitative realizations with explicit error | G2, L8 |
| P6 | Evaluation is a pure dependency graph; effects are explicit actions | L9, L11 |
| P7 | The demand determines what is required and all decision criteria are explicit | G3, L10, L12 |
| P8 | The planner may change implementations only through certified substitutions | L13 |
| P9 | Foreign computation crosses an explicit trust/world boundary | L14 |
| P10 | The kernel is minimal and programs/plans are data | L15 |

Y dejaría **G0 como tesis de diseño**, no como otro principio:

> Type theory guides meaning; demand guides execution.

Eso es una excelente frase de apertura.

---

# 6. El documento además tiene un problema de “status”

Hay principios denominados `settled` que contienen párrafos `proposed`.

L5 termina diciendo que la composición es proposed aunque el status general sea settled. principles

L8 es “settled in its statement”, mientras la corrección matemática sobre rounding sigue pending. principles

Y L14 acaba de una forma especialmente confusa: “Status: settled ... proposed, candidate”. principles

Eso impide que un implementador sepa qué debe implementar.

Yo prohibiría que un principio tenga status mixto.

El **principio normativo** puede estar `settled`.

Sus mecanismos pueden aparecer fuera como:

`Derived rule — proposed`

`Implementation — pending`

`Open mathematical question`

Pero no dentro de la misma unidad normativa.

---

# 7. Cómo mejoraría radicalmente el documento

Ahora mismo intenta servir simultáneamente como manifiesto, semántica, especificación, rationale, changelog y registro de decisiones. Eso está haciendo que principios muy buenos resulten más difíciles de ver.

Yo le impondría esta disciplina:

1. **Cada principio: máximo 3–5 líneas.** Debe poder leerse independientemente.
2. Debajo: `Consequences`, no más de 3–5 consecuencias.
3. Ejemplos y counterexamples fuera del principio.
4. Seeds, hashes, thread counts, memo keys, library versions, etc. van a la runtime spec.
5. Todo “was Lx”, fechas, decisiones y provenance queda exclusivamente en `record/`.
6. Cada término tiene una sola categoría formal: `Structure`, `Theory`, `Model`, `Law`, `Certificate`, `Plan`, `Demand`, `Action`, `World`.
7. Añadir al comienzo un pequeño diagrama formal que muestre la relación principal:

\[
\text{Structure}
\xrightarrow{+\ Law}
\text{Theory}
\]

\[
\text{value} + \text{certificate}
\longrightarrow
\text{Model}
\]

\[
\text{Demand}
\longrightarrow
\text{Plan}
\longrightarrow
\text{Realization}
\]

\[
\text{Realization}
+\text{Evidence}
\neq
\text{Meaning}
\]

Ese diagrama aclararía más que varias páginas actuales.

---

## Mi diagnóstico global

El problema de este Draft 10 **ya no es falta de pensamiento**. De hecho ocurre lo contrario: cada crítica anterior ha sido incorporada directamente dentro de los principios y eso ha generado una especie de sedimentación.

Eso es buena señal para la teoría, pero mala para el documento.

Yo haría ahora una poda bastante agresiva:

**15 L → 10 principios.**

Y antes de añadir ningún principio nuevo resolvería cuatro cosas: **`Type/Structure/Theory`, composición de sampled evidence, semántica de extern/world, y class vs graph**.

Después de eso, el documento probablemente quedaría no sólo más corto sino **mucho más formalizable**. La idea central de separar *meaning / realization / evidence* puede convertirse, además, en el eje que organice casi todo Luthier.







