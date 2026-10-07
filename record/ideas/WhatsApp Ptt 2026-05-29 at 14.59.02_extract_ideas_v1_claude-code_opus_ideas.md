---
audio: WhatsApp Ptt 2026-05-29 at 14.59.02.mp3
fecha: 2026-05-29
duracion: ~02:49
ideas: 5
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### algebra-tipos-dependientes-rigurosa
- **Qué**: Si el lenguaje va a tener tipos dependientes, necesita un álgebra de tipos dependientes bien definida; no se pueden aplicar soluciones toscas como truncamiento u olvido arbitrario.
- **Cita** (verbatim): "Si vas a tener tipos de pendientes, los tenés con un álgebra de tipos de pendientes bien definida, no podés hacer una cosa así." `[00:09]`

### tipos-como-historia-de-composicion
- **Qué**: El tipo de un valor puede registrar la historia de las funciones que se le aplicaron. En un algoritmo con un loop, el tipo queda expresado como una combinación de tipos elevada a una potencia, y eso "te da una idea del tipo que es".
- **Cita** (verbatim): "el tipo te puede quedar expresado así que se yo como una combinación de tipos con una potencia y listo y eso te da una idea del tipo que es entonces ahí lo que tenés en el tipo es la historia de cómo llegaste hasta ahí" `[01:27]`

### asociatividad-de-funciones-y-patrones-de-composicion
- **Qué**: Si las funciones son asociativas, se pueden encontrar patrones en la composición (por ejemplo, una serie de funciones elevada a una potencia para representar un loop).
- **Cita** (verbatim): "si las funciones son todas asociativas son digamos los funciones son asociativos entonces vos encontrás un patrón por ejemplo si vos tenés un algoritmo que tiene que repite un loop va a ser una serie de funciones y después a una potencia" `[01:04]`

### olvido-selectivo-como-funcion
- **Qué**: Se puede hacer olvido selectivo sobre la historia acumulada en el tipo, aplicando una función no invertible que descarta parte de la información (por ejemplo, "tuvo raíz cuadrada, tuvo cosas").
- **Cita** (verbatim): "si puedes hacer algún tipo de selección por ejemplo bueno tuvo tuvo raíz cuadrada tuvo cosas y si con olvido selectivo ahí puede ser una función digamos no se llama eso, no invertible, una función de olvido." `[01:51]`

### functores-de-olvido-como-componente-central
- **Qué**: La elección de qué función de olvido se aplica a los tipos define el lenguaje que se está hablando. Los functores de olvido serían uno de los componentes más importantes de Luthier, tanto en implementación como conceptualmente.
- **Cita** (verbatim): "los functores de olvido serían, digamos, uno de los componentes más importantes de Luthier en cuanto a la implementación y en cuanto a todo, ¿no?" `[02:29]`
- **Ambigüedad / tensión**: Queda completamente abierto qué functores de olvido aplicar y cómo elegirlos. El autor lo marca explícitamente: "Eso hay que seguir pensándolo." `[02:44]`
