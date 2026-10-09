---
source: claude-code
key: claude-code::46f06546-e0bb-41bb-bf4a-df07423bb06f
title: "Bien, en luthier fije ciertas normas de trabajo, las podes leer?"
started: 2026-10-06T08:34:46Z
ended: 2026-10-06T13:10:18Z
thread: 2026-10-06_46f06546_bien-en-luthier-fije-ciertas-normas-de-t.md
thread_sha256: 35cd57bd00eec392aa23a347b2916b5c82f7bb005076064e41705b2bd27c3867
copy: tracked
turns: 20
windows: 1
window_chars: 60000
ideas: 3
quotes_found: 3/3
generated_by: extract_ideas_dialogue_v1
prompt_sha256: 0954c180c11dae5ddb862a5d39b34f06d21364d490f686f249be18f04f740c22
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

Most of this conversation is about the sonolocalización experiment (the A2 distance block, the mic1 priors, the audio of 15:28:52), which does not touch Luthier. Three moves touch Luthier or the working method that guides its development.

### objetivos-escritos-como-vara-de-las-decisiones
- **Who**: model
- **Turn**: 3, 2026-10-06 08:35:35 UTC
- **Kind**: idea
- **What**: Without a written `docs/objectives.md`, a model deciding on its own within its margin has nothing to measure its decisions against; P4 and P12 are measured against those objectives.
- **Quote**: "P4 (las decisiones siguen principios hacia los objetivos del proyecto) y P12 (lo que te llega se resume según esos objetivos) se miden contra ellos. Sin objetivos escritos, cuando decido por mi cuenta dentro del margen no tengo contra qué medir."

### tension-util-ya-vs-asentar-bases
- **Who**: model
- **Turn**: 11, 2026-10-06 11:55:13 UTC
- **Kind**: idea
- **What**: Restating the Luthier draft, the model names a tension between Luthier's O1 (be useful now, sonolocalización first) and laying the foundations first; the cost falls on sonolocalización, whose `.lut` layer must be rewritten on every kernel change.
- **Quote**: "El borrador de luthier señala una tensión entre su O1 (ser útil ya, sonolocalización primero) y asentar las bases antes. El costo cae acá: cada cambio del kernel obliga a reescribir la capa `.lut` de sonolocalización, que ya se archivó dos veces"
- **Open**: left for Luciano to settle by marking Luthier's objectives.

### nota-de-un-modelo-no-es-un-hecho
- **Who**: model
- **Turn**: 19, 2026-10-06 12:57:18 UTC
- **Kind**: correction of turn 17
- **What**: A note a model wrote inside a data table is not a field datum, and the model had repeated it as if it were; the script even keyed its behavior on the word "nominal" in that note.
- **Quote**: "La frase \"Valor nominal del arreglo, no medicion individual\" no es tuya: es una nota que escribió un modelo en `distancias.csv` cuando armó la tabla, y yo la repetí como si fuera un dato del campo."
