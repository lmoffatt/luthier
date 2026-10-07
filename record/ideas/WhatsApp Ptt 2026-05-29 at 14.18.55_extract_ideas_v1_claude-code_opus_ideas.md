---
audio: WhatsApp Ptt 2026-05-29 at 14.18.55.mp3
fecha: 2026-05-29
duracion: ~01:57
ideas: 4
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### core-y-librerias
- **Qué**: Luthier se estructura como un core cerrado más librerías que manejan la interacción con el exterior.
- **Cita** (verbatim): "Una posibilidad es pensar a Luthier con un core y después librerías, que las librerías serían las que harían a Luthier interactuar con otros programas." `[00:00]`
- **Ambigüedad / tensión**: no queda claro si las librerías son parte del lenguaje o extensiones separadas; el autor oscila entre "librerías" y "funciones de Luthier".

### elemento-externo
- **Qué**: Todo lo que no es Luthier (C++, Python, la computadora, cualquier recurso) es conceptualmente externo al lenguaje; habría que modelar eso como algún tipo de "elemento externo".
- **Cita** (verbatim): "C++ o un programa de Python o la computadora o cualquier recurso no es un elemento de Luthier, es como un elemento externo" `[00:37]`
- **Ambigüedad / tensión**: el autor no sabe cómo se modela exactamente ese concepto de elemento externo — "tendríamos que incluir una especie de tipo de elemento externo o algo así, no sé eso como es exactamente" `[00:55]`.

### luthier-cerrado-observador-del-universo
- **Qué**: Luthier como sistema cerrado y completo internamente ("todos sus tipos perfectos") que observa el universo exterior; la analogía es la de un observador.
- **Cita** (verbatim): "yo lo estoy pensando como un observador y del universo, o sea, Luthier sería cerrado, como que tiene todos sus tipos así perfectos" `[01:11]`

### read-write-como-interfaz
- **Qué**: La comunicación con el exterior se piensa como un ciclo de lectura/escritura: convertir código Luthier en código ejecutable (C, etc.) y leer archivos o datos externos convirtiéndolos en Luthier.
- **Cita** (verbatim): "convertís un código de Luthier en un código ejecutable en C o en qué sé yo, lo que sea, y a la vez vos también leés files o leés algo y lo convertís en Luthier también, ¿no? O sea, sería como un read-write" `[01:21]`
- **Ambigüedad / tensión**: el autor no resuelve si esto es compilación, input-output, o algo distinto — "que a la vez sea una especie de compilación o lectura o algo así, input-output, no sé" `[01:43]`.
