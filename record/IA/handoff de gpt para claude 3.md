El plan está bastante bien armado, pero tiene un problema central: **mezcla “independencia causal” con “ventana temporal” y después trata de repararlo con proxies demasiado débiles**. Yo lo aprobaría sólo con cambios en D1–D3 y D10.

La buena noticia es que el núcleo experimental ya es mucho mejor que el control Python/Haskell: separa el experimento “¿estos principios realmente discriminan decisiones?” del experimento “¿el pipeline logra descubrirlos?”, y explícitamente pospone el segundo hasta arreglar la pérdida de fuerza normativa en extraction/linking. Eso es correcto. plan-principles-validation-2026…

## Lo que mantendría tal cual

La arquitectura general:

**transcripts → unidades mecánicas → fechas → eligibility → drafting A/B → aprobación tuya → scoring ciego**

es buena.

También mantendría sin tocar:

- `approved:false` hasta revisión humana;
- el drafter no ve principios;
- el scorer no ve outcome, IDs, fechas, source ni otros principios;
- swap A/B;
- `NEITHER` como falta de cobertura, no error;
- separar `luciano_choice`, `luciano_confirmation` y `model_margin`;
- excluir alternativas `constructed` del resultado principal;
- conflict matrix;
- reversals visibles;
- provenance completa y prompts congelados después de un resultado puntuado. plan-principles-validation-2026… plan-principles-validation-2026… plan-principles-validation-2026…

El miner también me parece razonable como primera capa. Que sea puramente mecánico y que `decided_by` quede para el drafter es una buena separación entre extracción factual e interpretación. plan-principles-validation-2026…

## Problema 1: `explicit < decision < operative` no garantiza independencia

Claude propone que el resultado principal use desde que el principio fue formulado explícitamente hasta que entró en una instrucción operativa. plan-principles-validation-2026…

Eso tiene una intuición buena, pero la interpretación está demasiado fuerte.

Supongamos:

```text
10:00 Luciano formula claramente P7
10:05 conversa con Claude sobre P7
11:00 toma una decisión D
15:00 P7 entra en CLAUDE.md
```

Formalmente:

```text
explicit(P7) < D < operative(P7)
```

pero D **no es independiente de P7**. Luciano ya lo tenía en mente y el agente puede haberlo visto en la conversación.

El propio plan intenta reparar esto excluyendo sesiones donde el principio “fue stated earlier”. plan-principles-validation-2026…

Pero ahí aparece el segundo problema.

## Problema 2: D3, el detector de exposición por overlap textual, es demasiado frágil

D3 dice buscar en turnos previos de la sesión overlap con el quote y statement del principio y excluir por encima de un threshold. plan-principles-validation-2026…

No confiaría en esto para decidir el conjunto experimental principal.

Un principio puede haber sido comunicado semánticamente sin repetir su frase.

Ejemplo:

```text
Principio:
No agregar mecanismos recurrentes sin un caso que los justifique.

Conversación:
"esto nos está metiendo demasiada burocracia al pedo"
```

Overlap textual casi cero.

Exposición conceptual: enorme.

Y al revés, podría aparecer vocabulario parecido en otro contexto sin transmitir el principio.

Entonces el threshold introduce una clasificación importantísima mediante una heurística lexical arbitraria.

### Mi modificación

Distinguiría:

```text
temporally_eligible
exposure_status
```

y no dejaría que `eligible_cases.py` decida semánticamente la exposición.

Por ejemplo:

```json
{
  "temporally_eligible": true,
  "exposure": "unknown"
}
```

Luego el drafter —que ya lee los turns relevantes— puede marcar:

```text
none
possible
explicit
```

pero sin ver el principio, obviamente no puede hacerlo principio por principio.

Mejor todavía: para las primeras 30 unidades que vos vas a revisar, hacer una revisión específica de exposición por principio sólo para los pares que realmente entren en el scoring.

Eso reduce muchísimo el problema: no revisar cientos de pares, sólo quizá 30 × pocos principios elegibles.

El **main result** debería usar únicamente `exposure = none`.

`possible` va a sensibilidad.

No usaría overlap lexical para decidir el main dataset.

---

## Problema 3: “emergence” probablemente sobra para este primer experimento

El plan propone encontrar `emergence` con 14 llamadas y después que vos elijas la primera fila que representa la idea. plan-principles-validation-2026…

Conceptualmente me gusta tenerlo en el archivo histórico.

Experimentalmente no lo usaría ahora.

Porque “la primera vez que aparece vagamente una idea” es extremadamente interpretativo y probablemente genere discusiones que no cambian el resultado principal.

Claude ya propone que `explicit` sea el resultado principal y emergence sólo secundario. plan-principles-validation-2026…

Yo iría más lejos:

**para v1, no gastaría las 14 llamadas en emergence.**

Guardar:

```text
explicit
operative
```

y empezar.

Después, si el experimento produce algo interesante, reconstruís emergence como análisis histórico.

Eso simplifica y además evita otra capa de model-assisted annotation antes de tener siquiera una señal experimental.

---

## Problema 4: hay riesgo de selección en Step 5

Claude propone draftar quizá 100–200 casos y que vos revises una muestra estratificada de ~30. plan-principles-validation-2026…

Eso es razonable por costo humano.

Pero hay que congelar una regla importante:

**la muestra debe seleccionarse antes de que vos veas los casos individuales.**

Y si corregís/rechazás uno, no debe reemplazarse buscando “otro mejor” del mismo estrato salvo mediante una regla automática predefinida.

Porque si ocurre:

```text
sample 30
Luciano descarta 12 casos malos
reemplazamos con otros 12
```

terminás enriqueciendo involuntariamente el dataset con casos limpios/interpretables.

Yo pre-registraría:

```text
draw N=40
review exactly those 40
approved subset = experiment
```

Si sólo 21 sobreviven, entonces N=21.

No replenishment.

Eso importa bastante.

---

## Problema 5: el baseline actual es demasiado fácil de vencer

El baseline recibe:

> Which option is better supported by the information given? If it does not discriminate, answer NEITHER. plan-principles-validation-2026…

Pero el scorer con principio recibe información adicional semánticamente potente.

Entonces una mejora sobre baseline podría simplemente significar:

> “darle cualquier regla pertinente ayuda”

y no:

> “este principio particular organiza estas decisiones”.

Necesitás **un baseline más duro**.

Yo pondría tres:

```text
B0: no principle
B1: unrelated principle
B2: shuffled principle
```

### `B1 unrelated principle`

Para cada caso, darle otro principio real de Luthier seleccionado aleatoriamente entre los no evaluados para ese caso.

Pregunta:

> Which option follows more directly from this principle?

Si P7 tiene 80% pero principios aleatorios tienen 72%, P7 no tiene mucha especificidad.

### `B2 shuffled`

Permutar la asignación principio→statement entre IDs.

Esto da una distribución nula de cuánto “predice” cualquier frase normativa.

Para mí este cambio es **mucho más importante que Wilson intervals**.

La verdadera comparación debería ser:

\[
\text{target principle}
\quad vs \quad
\text{other principles}
\]

no sólo:

\[
\text{principle}
\quad vs \quad
\text{no information}
\]

---

## Problema 6: accuracy contra “lo que se eligió” no es suficiente

El objetivo está formulado como: si el principio escoge la opción efectivamente elegida más que el baseline. plan-principles-validation-2026…

Pero un principio puede ser genuino y vos haber tomado decisiones en contra de él.

De hecho el ledger ya admite `For` y `against`.

Entonces:

```text
principle predicts B
Luciano chose A
```

no necesariamente falsifica el principio.

Puede significar:

```text
P7 favorecía B
P12 dominó y favorecía A
```

Por eso la **conflict matrix no es una feature secundaria**. Es parte central de la interpretación.

Yo reformularía la hipótesis:

> Un principio válido debe mostrar una preferencia estable y específica en decisiones de su dominio, y esa preferencia debe corresponder sistemáticamente con decisiones o tensiones observadas.

Es más sutil que accuracy.

Idealmente cada case después de tu review podría tener además:

```text
actual = A
known_tradeoff = optional
```

pero sin decir qué principio.

Después del scoring se puede mirar:

- target acertó;
- target perdió contra otro principio;
- target no aplicó;
- target dio dirección opuesta.

Esto se parece mucho más a cómo realmente trabajan principios en conflicto.

---

## Problema 7: `>=3 casos` es demasiado poco para “score”

D4 propone puntuar un principio con tres casos independientes. plan-principles-validation-2026…

Con \(n=3\), 3/3 parece 100%, pero te dice poquísimo.

No prohibiría mostrarlo, pero cambiaría lenguaje:

```text
n < 5        anecdotal
5 <= n < 10  exploratory
n >= 10      scored
```

No porque 10 sea mágico, sino para impedir que una tabla con `100%` sobre tres decisiones adquiera una autoridad visual que no merece.

Wilson ayuda pero no resuelve el problema interpretativo.

---

## Problema 8: D10 batching puede introducir un efecto considerable

Claude correctamente identifica que meter todos los casos de un principio en una sola llamada puede hacer que los casos se influyan entre sí. plan-principles-validation-2026…

Su solución de comparar diez casos individualmente es buena.

Pero yo la convertiría en una regla **antes del experimento**:

```text
agreement >= 90% → batch accepted
agreement < 90% → discard batched result and rerun per-case
```

No “beyond a threshold” elegido después.

Y ese threshold debe fijarse ahora.

Además correría el subset check antes de mirar accuracy contra outcomes. Sólo comparar respuestas batch vs singleton.

---

# Lo que creo que Claude hizo especialmente bien

Hay una cosa metodológica que me gusta mucho: reconoce de antemano que el experimento puede terminar con pocos principios evaluables y dice explícitamente:

> eso es un resultado, no un fracaso del plan. plan-principles-validation-2026…

Eso es exactamente lo correcto.

Si P1–P13 aparecen casi simultáneamente con su entrada operativa, **la historia simplemente no contiene el natural experiment que querríamos**.

No hay que fabricar observaciones para salvar la hipótesis.

También me parece acertado explotar que un mismo principio puede ser operativo en un repo y no en otro. Eso sí puede producir un natural experiment razonablemente interesante. plan-principles-validation-2026…

Y separar language/method porque el decision log estaba sesgado a method es imprescindible. plan-principles-validation-2026…

# Mi veredicto

**Lo ejecutaría, pero no todavía tal cual.**

Cambiaría cinco cosas antes de gastar las 100–200 llamadas de drafting:

1. **Eliminar `emergence` del camino crítico de v1.** Usar `explicit → operative`.
2. **No usar overlap textual como criterio definitivo de exposición.** Guardarlo como flag heurístico, no como verdad.
3. **Congelar la muestra de review sin reemplazos posteriores.**
4. **Agregar baseline con otros principios reales / shuffled principles.**
5. **Pre-fijar el criterio batch vs singleton**, por ejemplo 90% de agreement.

Y conceptualizaría el resultado no como:

> “P7 predice tus decisiones con 82% accuracy”

sino como:

> **“P7 discrimina estas decisiones de manera estable, con esta cobertura, esta especificidad frente a otros principios y estos conflictos con P4/P12.”**

Eso sí sería evidencia interesante sobre si tus P1–P14 son realmente “ideas organizadoras que ayudan a tomar decisiones”.

En cambio, si termina siendo simplemente `accuracy(target) > accuracy(no-context)`, me parecería una validación demasiado débil para justificar todo este aparato.