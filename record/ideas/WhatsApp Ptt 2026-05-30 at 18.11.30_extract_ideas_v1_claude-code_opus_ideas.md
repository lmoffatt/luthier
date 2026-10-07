---
audio: WhatsApp Ptt 2026-05-30 at 18.11.30.mp3
fecha: 2026-05-30
duracion: ~01:12
ideas: 4
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### programa-como-funcion-vs-interaccion
- **Qué**: Luthier tiene que decidir si un programa es como una función pura (input → output) o si tiene capacidad de interacción.
- **Cita** (verbatim): "pensar si es un programa que es tipo una función, como si fuera una función que vos le das un input y te tira un output, o si tiene una función de interacción" `[00:00]`
- **Ambigüedad / tensión**: no se define qué significa "función de interacción" ni cómo se modelaría; queda explícitamente abierto ("eso no sé cómo se define ni nada").

### simplicidad-primero-extensibilidad-despues
- **Qué**: Empezar con el modelo más simple (función pura) y después extenderlo al modelo interactivo.
- **Cita** (verbatim): "en principio uno podría pensarlo como lo primero para hacerlo más simple. Supongo que después vos podés extenderlo al otro." `[00:27]`

### programa-que-opera-sobre-programas
- **Qué**: Si un programa de Luthier es como una función, entonces un programa de Luthier puede tomar como input otro programa de Luthier y trabajar sobre él.
- **Cita** (verbatim): "si es tipo una función, entonces una cosa que puede hacer un programa de Luthier es trabajar sobre otro programa de Luthier" `[00:38]`

### auto-referencia
- **Qué**: La posibilidad de que un programa de Luthier trabaje sobre sí mismo. Normalmente no se puede, pero dado que Luthier define su propio universo, podría habilitarse.
- **Cita** (verbatim): "normalmente no se puede, pero en principio, dado que es nuestro propio universo, podríamos hacer que Luthier trabaje sobre sí mismo. Es una pregunta interesante." `[00:54]`
- **Ambigüedad / tensión**: queda como pregunta abierta; no se resuelve si conviene ni cómo se implementaría.
