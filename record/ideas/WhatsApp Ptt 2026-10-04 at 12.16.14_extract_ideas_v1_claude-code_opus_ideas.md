---
audio: WhatsApp Ptt 2026-10-04 at 12.16.14.mp3
fecha: 2026-10-04
duracion: ~03:51
ideas: 7
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### tipos-declarados-antes-de-definidos
- **Qué**: Refinamiento de la idea previa de que los tipos primero se declaran y después se definen, y de que no se puede definir un valor de un tipo que todavía no está definido.
- **Cita** (verbatim): "fui refiniando el tema de que los tipos están primero declarados y después definidos, y que vos no podés definir un valor de un tipo no definido" `[00:07]`

### tipos-como-productos-y-sumas-sujetos-a-leyes
- **Qué**: Los tipos se definen ensamblando otros tipos existentes; generalmente son productos y sumas de otros tipos, sujetos a ciertas leyes.
- **Cita** (verbatim): "los tipos van a ser generalmente productos y sumas de otros tipos existentes sujetos a ciertas leyes" `[00:45]`

### leyes-que-conectan-los-subtipos
- **Qué**: Las definiciones de tipos tienen que tener leyes que conecten a los subtipos que ensamblan.
- **Cita** (verbatim): "las definiciones de tipos tienen que tener leyes que conecten" `[00:24]`

### nucleo-circular-vs-colgado
- **Qué**: Primera formulación del requisito: las leyes deben incluir circularmente a todos los subtipos del nuevo tipo; si alguno no entra en la circularidad, queda un núcleo circular y lo demás colgado.
- **Cita** (verbatim): "esas leyes tienen que incluir circularmente a todos los tipos de este nuevo tipo que se genera" `[01:02]`
- **Ambigüedad / tensión**: Queda como primera versión, corregida más adelante en el mismo audio (ver `conectado-no-circular`).

### conectado-no-circular
- **Qué**: Corrección en vivo de la formulación anterior: el requisito no es que el grafo de subtipos sea circular, sino que esté conectado; con que todos estén conectados, forman un tipo.
- **Cita** (verbatim): "El tema es que tiene que estar conectado. No que tenga que ser circular" `[02:22]`
- **Ambigüedad / tensión**: La corrección surge razonando sobre un ejemplo (dos tipos circularmente dependientes más un tercero que depende de ellos pero no al revés); no cierra qué es ese tercer caso ("¿Y eso qué es? ¿Es otro tipo?").

### tipos-universales-solo-nucleo
- **Qué**: Se pueden construir tipos "más universales" que solo incluyan al núcleo.
- **Cita** (verbatim): "vos podés hacer, digamos, tipos más universales que, digamos, sí, que solo incluyan al núcleo" `[02:48]`
- **Ambigüedad / tensión**: Apenas insinuado; lo deja abierto con "cualquier mapa de esos podría funcionar si lo pensamos un poco."

### funciones-no-campos-conectan
- **Qué**: Lo que cuenta para la conexión del grafo son las funciones, no los campos; una función puede quedar "colgada" de otro tipo.
- **Cita** (verbatim): "es una función que está colgada de otro tipo" `[03:40]`
- **Ambigüedad / tensión**: Queda explícitamente sin resolver; cierra con "Eso tengo que pensarlo bien" `[03:47]`.
