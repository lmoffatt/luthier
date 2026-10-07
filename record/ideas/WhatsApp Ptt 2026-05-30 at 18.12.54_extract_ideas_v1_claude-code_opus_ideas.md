---
audio: WhatsApp Ptt 2026-05-30 at 18.12.54.mp3
fecha: 2026-05-30
duracion: ~01:05
ideas: 3
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### conmutatividad-de-statements
- **Qué**: Los statements en Luthier serían conmutativos; el orden en que se escriben no determina su semántica.
- **Cita** (verbatim): "la pregunta de la conmutatividad de statements es sí, sí habría conmutatividad de statements, o sea, la idea es que sí" `[00:00]`

### programa-como-dag
- **Qué**: Un programa Luthier, estáticamente, se modela como un DAG (grafo dirigido acíclico). Esta es la estructura que sustenta la conmutatividad: el orden textual no importa porque la dependencia la da el grafo.
- **Cita** (verbatim): "estoy inclinado a que sí y que sí, tomaríamos el modelo de los DAGs, que digamos como que sería un DAG, básicamente" `[00:07]`

### dag-sobre-dags-meta-operación
- **Qué**: Más allá del DAG estático de un programa, se puede tener un DAG que opera sobre DAGs, es decir, programas que manipulan programas. El DAG base es estático, pero hay algo que opera sobre él y lo transforma, usando instrucciones de sí mismo.
- **Cita** (verbatim): "vos podés tener en realidad un DAG que opera sobre DAGs, que opera sobre programas [...] pero vos lo podés tomar como un DAG estático, que después, claro, hay algo que opera sobre ese DAG y después se transforma en otra cosa con instrucciones de sí mismo" `[00:19]`
- **Ambigüedad / tensión**: Queda sin desarrollar qué es exactamente ese "algo que opera sobre el DAG" ni cómo funciona la auto-transformación. El autor lo señala como una idea interesante pero la deja abierta: "Es interesante pensar un poco esa idea, pero bueno."
