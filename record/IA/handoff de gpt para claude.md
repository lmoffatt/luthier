Quiero implementar una validación temporal/predictiva de los principios de Luthier. No quiero modificar todavía `find_principles_v2` ni reinterpretar los controles Python/Haskell. Este es un experimento nuevo.

Antes de escribir código, inspeccioná las convenciones de los scripts actuales, especialmente:

- `scripts/find_principles.py`
- `scripts/link_ideas.py`
- `scripts/principles_common.py`
- `scripts/compare_principles.py`
- `scripts/principles_ledger.py`
- `record/decisions.md`
- `docs/principles.md`
- tests relacionados con estos scripts

Seguí las convenciones existentes de provenance, hashes, prompts versionados, estado de las corridas, respuestas crudas, validación y tests.

## Hipótesis que queremos probar

Un principio no se valida porque reconstruya una lista canónica de principios escrita por el diseñador.

Queremos probar algo más fuerte:

> Un principio inferido o formulado usando solamente información disponible hasta tiempo T debe discriminar correctamente entre alternativas de decisiones posteriores a T.

Es decir:

past ideas → principle → unseen future decisions

La información posterior al cutoff jamás puede entrar al descubrimiento/formulación del principio.

## Primera fase

Primero NO vuelvas a correr `find_principles`.

Validá los principios Luthier ya existentes. La pregunta inicial es:

> ¿Los principios que actualmente consideramos principios realmente discriminan decisiones posteriores mejor que un baseline sin principio?

Si ni siquiera los principios actuales lo hacen, no tiene sentido todavía medir la calidad de `find_principles`.

## Archivos a crear

Como mínimo:

- `scripts/validate_principles_temporal.py`
- `prompts/apply_principle_blind_v1.md`
- `prompts/apply_baseline_blind_v1.md`
- `record/validation/README.md`
- `record/validation/decision_cases.jsonl`
- tests unitarios correspondientes

Si necesitás un helper separado para preparar casos, crealo, pero mantené pequeña la arquitectura.

## decision_cases.jsonl

Cada caso representa una decisión real posterior y debe tener al menos:

```json
{
  "id": "D-...",
  "date": "2026-10-06T...",
  "question": "...",
  "A": "...",
  "B": "...",
  "actual": "A",
  "approved": false,
  "source": "...",
  "notes": ""
}
```

Puede ser A o B.

### Regla crítica

El modelo puede ayudar a PROPONER `question`, `A` y `B` a partir del decision log, pero esos casos deben quedar:

```json
"approved": false
```

El script de validación DEBE REHUSARSE a puntuarlos.

Sólo casos explícitamente marcados:

```json
"approved": true
```

pueden entrar en las métricas.

No cambies `approved` automáticamente.

Esto existe para evitar que un modelo construya retrospectivamente un contraste diseñado para que el principio gane.

Podés preparar una primera tanda de, digamos, 20-30 casos buenos de `record/decisions.md`, pero dejalos todos `approved:false` para que Luciano los revise.

Favorecé decisiones donde haya una alternativa real identificable, y especialmente reversals.

No inventes una oposición absurda para que la respuesta sea obvia.

## Prompt apply_principle_blind_v1

Debe recibir exclusivamente:

- statement del principio;
- si existe, su `instead_of`;
- pregunta de decisión;
- alternativa A;
- alternativa B.

NO debe recibir:

- ID de la decisión;
- fecha;
- resultado real;
- status;
- rationale posterior;
- otros principios;
- nombres de documentos;
- ninguna indicación de que una opción fue finalmente elegida.

Debe preguntar cuál alternativa sigue más directamente del principio.

Respuesta estricta JSON, por ejemplo:

```json
{
  "choice": "A",
  "confidence": 0.78,
  "reason": "..."
}
```

`choice` sólo:

- `A`
- `B`
- `NEITHER`

La razón debe ser corta.

El script valida el JSON.

## Control de posición

Cada caso debe correrse al menos dos veces:

1. orden original A/B;
2. alternativas intercambiadas.

La elección semántica debe mantenerse.

Ejemplo:

run 1:
A = X
B = Y
respuesta B

run 2:
A = Y
B = X
respuesta A

Eso cuenta como estable.

Si cambia de contenido al intercambiar la posición, marcar:

```text
position_unstable
```

y no contarlo como evidencia positiva.

Guardá ambas respuestas crudas.

## Baseline

Necesitamos saber qué puede resolver el modelo SIN el principio.

`apply_baseline_blind_v1.md` recibe sólo:

- pregunta;
- A;
- B.

No debe decir “qué elegiría Luthier”, porque eso invita memoria/conocimiento previo.

La pregunta debe ser aproximadamente:

> Which option is better supported by the information given? If the information does not discriminate, answer NEITHER.

Como casi no tiene contexto, esperamos muchos `NEITHER`.

Este baseline mide cuánto está implícito en la formulación del caso.

También correr A/B y B/A.

## Importante: otro baseline útil

Agregá, si no complica demasiado, un `random/majority baseline` puramente computacional para que el reporte muestre que accuracy aislada no alcanza.

## Fechas de los principios

Para la primera fase hay que determinar cuándo cada principio pasó a existir, o al menos el primer momento comprobable en el repo.

NO uses simplemente la fecha actual de `docs/principles.md`.

Investigá git history / decision log / provenance existente.

Guardá un archivo explícito si hace falta, por ejemplo:

`record/validation/principle_first_seen.json`

con:

```json
{
  "P1": {
    "first_seen": "...",
    "source": "commit/path/etc"
  }
}
```

No inventes precisión temporal que las fuentes no permiten. Si sólo sabemos el día, registrá resolución día.

El runner sólo puede probar:

```text
principle_first_seen < decision_date
```

Nunca una decisión anterior al principio.

## Métricas

Por principio calcular:

- eligible_cases
- applicable = A o B
- neither
- coverage = applicable / eligible
- correct
- incorrect
- accuracy = correct / applicable
- position_stable
- position_unstable
- stable_accuracy
- baseline_correct
- baseline_applicable
- baseline_accuracy
- gain_over_baseline

No fuerces una métrica cuando el denominador es cero: usar null y explicarlo.

Además agregá intervalos binomiales razonables para accuracy si es fácil hacerlo sin dependencia pesada. Wilson está bien.

No uses p-values decorativos con muestras diminutas.

## Reversals

Las decisiones revertidas son especialmente informativas.

Si `record/decisions.md` permite identificar:

initial choice A
later final choice B

guardalo en el caso, por ejemplo:

```json
{
  "reversal": {
    "initial": "A",
    "final": "B",
    "reversal_source": "..."
  }
}
```

La métrica/reporte debe distinguir:

- principle predicted initial;
- principle predicted eventual/final;
- neither.

Un caso donde el principio anterior predice la elección final antes de la reversión merece quedar visible individualmente en el reporte.

No declares causalidad. Sólo “predicted eventual choice”.

## Contaminación temporal

Este punto tiene que estar testeado.

El script debe abortar si:

- una decisión no es posterior al principio;
- un caso no está aprobado;
- falta `actual`;
- A == B;
- el resultado real aparece literalmente incrustado en el prompt de evaluación mediante metadata accidental;
- hay IDs/fechas/source enviados al modelo;
- un prompt deja placeholders sin llenar.

Idealmente construí el payload al modelo mediante una estructura explícita permitida, no serializando el case entero.

## Provenance de la corrida

Como tus otros scripts, guardar:

- versión del script;
- prompt + sha256;
- input files + sha256;
- git HEAD;
- modelo;
- effort;
- CLI version;
- fecha/hora;
- cada request/payload enviado;
- respuesta cruda;
- respuesta parseada;
- errores/retries;
- swap A/B;
- seeds si corresponden.

No sobreescribas una corrida anterior.

## Output

Algo del estilo:

`record/validation/runs/<timestamp>_temporal_principles_<model>.json`

y:

`record/validation/runs/<timestamp>_temporal_principles_<model>.md`

El Markdown debe ser legible por Luciano.

Primero resumen:

```text
Principle   eligible  coverage  stable accuracy  baseline  gain
P1          ...
P2          ...
```

Después casos interesantes:

- errores;
- position-unstable;
- reversals;
- casos donde baseline acertó sin principio;
- casos donde el principio discriminó y baseline dio NEITHER.

No esconder fallas.

## Segunda fase: principios encontrados automáticamente

Diseñá el formato de forma que luego podamos agregar:

```bash
--principles <find_principles output>
--cutoff T
```

pero NO hace falta ejecutar todavía el descubrimiento temporal completo.

La futura regla será:

timeline rows <= T
→ link lineages <= T
→ find principles
→ decisions > T

No debe existir ninguna vía por la cual las decisiones futuras entren a `find_principles`.

Si implementar soporte para esto ahora requiere modificar mucho el pipeline, dejá una interfaz limpia y un TODO documentado. No hagas una refactorización grande.

## Tests imprescindibles

Tests sin llamar al modelo real para:

1. rechaza `approved:false`;
2. rechaza decision anterior o igual a first_seen;
3. swap A/B se mapea correctamente;
4. detecta position instability;
5. NEITHER baja coverage, no cuenta como error;
6. accuracy sólo usa casos applicable;
7. baseline se calcula separadamente;
8. denominador cero produce null;
9. no pasan ID/date/source/actual al prompt;
10. placeholders incompletos fallan;
11. no sobreescribe runs;
12. parsing de `decision_cases.jsonl`;
13. reversal final/initial se reporta correctamente.

Usá stub/mock del agente siguiendo el patrón de los tests existentes.

## Primer dataset

Después de implementar y pasar tests:

1. Leé `record/decisions.md`.
2. Prepará una tanda inicial de 20-30 casos potencialmente útiles.
3. `approved:false` en TODOS.
4. Para cada caso explicá en `notes` por qué A/B representan una elección real y no una oposición inventada.
5. Priorizá decisiones con conflicto real y reversals.
6. No ejecutes scoring real hasta que Luciano los apruebe.

## README

`record/validation/README.md` debe explicar en lenguaje corto:

- qué hipótesis prueba;
- qué información está permitida;
- qué información está prohibida;
- por qué los casos requieren aprobación humana;
- qué significan coverage/accuracy/gain;
- que esto valida capacidad predictiva/discriminativa, no “verdad filosófica” ni causalidad.

## Restricciones

- No modificar `find_principles_v2`.
- No modificar resultados de controles Python/Haskell.
- No adaptar el prompt después de mirar resultados reales de este experimento sin registrar explícitamente una nueva versión.
- No usar `docs/principles.md` ni `record/decisions.md` dentro del prompt que decide A/B, salvo el texto concreto del principio que se está testeando.
- No dejar que el modelo vea `actual`.
- No hacer commits enormes mezclando esta infraestructura con cambios semánticos de Luthier.

## Al terminar

1. Corré todos los tests relevantes.
2. Mostrame los bugs encontrados y cómo los corregiste.
3. Mostrame exactamente qué archivos creaste/modificaste.
4. Mostrame 3-5 ejemplos de `decision_cases.jsonl`.
5. Mostrame un dry-run con un agente stub.
6. No corras todavía el experimento con modelo real.
7. No marques ningún caso como approved por tu cuenta.
8. Commit final sólo cuando tests estén verdes, con un mensaje que deje claro que es infraestructura experimental, no resultado.

Si encontrás que alguna parte de esta especificación entra en conflicto con la arquitectura actual del repo, no la fuerces silenciosamente: explicá el conflicto y elegí la adaptación mínima que preserve la separación temporal y el cegamiento.