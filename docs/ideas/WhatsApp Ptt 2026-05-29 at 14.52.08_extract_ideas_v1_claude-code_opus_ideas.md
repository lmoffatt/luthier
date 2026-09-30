---
audio: WhatsApp Ptt 2026-05-29 at 14.52.08.mp3
fecha: 2026-05-29
duracion: ~02:28
ideas: 5
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### acumulación-de-carga-de-tipado
- **Qué**: En un sistema de tipos dependientes, la composición sucesiva de funciones va acumulando información de tipado ("cada función va poniendo su granito de arena"), de modo que el tipo resultante crece con cada operación.
- **Cita** (verbatim): "vos vas acumulando, digamos, una carga de tipado que se va haciendo cada vez más fuerte" `[00:08]`

### problema-del-olvido
- **Qué**: El crecimiento descontrolado de la información de tipado genera un problema que el autor llama "el olvido", identificado como uno de los problemas fundamentales que Luthier tiene que solucionar.
- **Cita** (verbatim): "tenés ahí los problemas del olvido, que tiene que ser uno de los problemas fundamentales de Luthier que tiene que solucionar" `[00:24]`
- **Ambigüedad / tensión**: El autor nombra el problema ("el olvido") pero no define qué mecanismo concreto de olvido imagina ni cuándo debería activarse.

### contador-obsesivo
- **Qué**: Analogía para Luthier como un sistema que registra cada operación realizada, lo cual puede hacer que el decorado (la información de tipo) se vuelva mucho más grande que el valor decorado.
- **Cita** (verbatim): "si Luthier es como una especie de contador obsesivo que registra cada una de las operaciones que vos haces, claro, puede ser que de repente, digamos, lo que es el decorado se vuelva muchísimo más grande que el valor que está siendo decorado" `[00:36]`

### álgebra-simplificadora-de-tipado
- **Qué**: La solución al crecimiento de tipos sería un álgebra de tipado que no sea un monoide libre, sino un monoide que mantenga acotada la complejidad del tipo resultante al componer funciones.
- **Cita** (verbatim): "algún tipo de álgebra de tipado que sea un álgebra simplificadora, o sea, que no sea un monoide libre, básicamente" `[01:06]`
- **Ambigüedad / tensión**: No se define qué relaciones o ecuaciones tendría ese monoide para dejar de ser libre, ni qué información sería descartable.

### simplificación-de-composición-como-problema-ingenieril-clave
- **Qué**: El autor identifica la simplificación de la composición de tipos dependientes como uno de los problemas ingenieriles claves de Luthier, distinto de un problema teórico: se trata de que el resultado sea "informativo" sin arrastrar toda la historia.
- **Cita** (verbatim): "cómo hacer para simplificar la composición de tipos dependientes" `[02:19]`
- **Ambigüedad / tensión**: El autor duda de si es realmente necesario limitar ("quizás te queda, digamos, una ristra de 17 funciones y está todo bien") pero se inclina a que sí conviene un mecanismo.
