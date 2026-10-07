---
audio: WhatsApp Ptt 2026-05-29 at 14.46.22.mp3
fecha: 2026-05-29
duracion: ~03:57
ideas: 7
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### contexto-como-dag
- **Qué**: El concepto de contexto (donde están definidos los tipos y paths de un programa) se modela como un DAG (Directed Acyclic Graph), donde los tipos dependen de otros tipos.
- **Cita** (verbatim): "La manera de definir contexto sería como un DAG, un Directed Acyclic Graph, donde vos partís de tipos que dependen de otros, etc." `[00:23]`

### tipos-implicitos-por-solucion
- **Qué**: Posibilidad de definir tipos implícitamente, como soluciones a un problema o como el óptimo de una función, en vez de declararlos directamente.
- **Cita** (verbatim): "vos podrías definir tipos implícitos a través de soluciones o de, por ejemplo, el tipo que soluciona determinado problema" `[00:37]`
- **Ambigüedad / tensión**: El autor duda si esto sigue siendo modelable como DAG o no. Parece concluir que sí ("creo que lo estás definiendo con un DAG, me parece igual") pero no lo cierra del todo.

### tipos-desconocidos-definicion-diferida
- **Qué**: Permitir referirse a tipos que aún no están definidos, y definirlos después (forward reference), o incluso dejarlos sin definir, en cuyo caso funcionarían como inputs del programa.
- **Cita** (verbatim): "vos podrías dejar tomar tipos como tipos desconocidos hasta que sean definidos [...] vos podés por ejemplo pasarte a un tipo que no está definido, lo definís después, por ejemplo. O ese tipo, por ejemplo, es un input del programa, si no está definido nunca." `[01:16]`

### verificacion-definicion-unica-vs-producto-cartesiano
- **Qué**: El compilador de Luthier debería verificar que ningún tipo esté definido dos veces, pero se abre la posibilidad de que una doble definición se interprete como producto cartesiano, ganando poder expresivo.
- **Cita** (verbatim): "el compilador de Luthier, sería verificar que ningún tipo está definido dos veces. Aunque podría estar definido dos veces y que sea un producto cartesiano también." `[01:38]`
- **Ambigüedad / tensión**: Queda abierto si la doble definición sería error, producto cartesiano, o configurable. Se menciona un posible "cartel" o warning como mecanismo intermedio.

### expresividad-vs-robustez
- **Qué**: Tensión entre maximizar la expresividad (permitir tipos diferidos, doble definición, etc.) a costa de menor robustez, y si buenos mensajes del compilador pueden compensar esa pérdida de robustez.
- **Cita** (verbatim): "un poco de optimización de la expresividad a costa de ser un poco menos robusto. Pero bueno, es cuestión de ver, digamos, dónde está la robustez ahí, ¿no? Digamos, con buenos mensajes de qué es lo que está ocurriendo, por ahí lo podés eso tener gran flexibilidad y no tener error" `[02:36]`

### redundancia-vs-expresividad
- **Qué**: Dos orientaciones posibles para Luthier: forzar redundancia (expresar lo mismo de varios lados para disminuir errores) o priorizar expresividad. El autor se inclina hacia lo expresivo porque lo redundante puede ser incómodo y limitar innecesariamente.
- **Cita** (verbatim): "Si vas a ser más redundante o expresivo, digamos, me parece que son cosas que tenés que elegir una de las dos. [...] lo expresivo, digamos, garpa más, porque puede ser que lo redundante sea incómodo a veces y te limite al pedo, ¿no?" `[03:26]`
- **Ambigüedad / tensión**: El autor se inclina pero no decide categóricamente; además se pregunta si esto es filosófico o de detalle de implementación.

### redundancia-como-implementacion-configurable
- **Qué**: La idea de que forzar redundancia o permitir flexibilidad podría ser una cuestión de implementación particular de Luthier, no necesariamente de su filosofía central.
- **Cita** (verbatim): "también puede ser que uno fuerce a ser redundante y entonces expresarlo de varios lados de manera a disminuir la tasa de errores, también eso es otra implementación de Luthier posible, creo que esos son más bien detalles, no hacen a la filosofía" `[03:03]`
- **Ambigüedad / tensión**: Inmediatamente después se contradice: "Bueno, la filosofía podría ser, ¿no?" — no queda resuelto si es detalle o filosofía.
