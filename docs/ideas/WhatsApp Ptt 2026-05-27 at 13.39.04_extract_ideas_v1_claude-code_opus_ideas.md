---
audio: WhatsApp Ptt 2026-05-27 at 13.39.04.mp3
fecha: 2026-05-27
duracion: ~04:54
ideas: 10
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### luthier-como-mayordomo
- **Qué**: Luthier se concibe como un "mayordomo" que puede correr programas y comparar sus outputs. La metáfora apunta a un rol de coordinación y servicio, no de ejecución directa.
- **Cita** (verbatim): "me lo imagino como un mayordomo que puede correr básicamente cualquier programa y que puede comparar los outputs" `[00:00]`

### composición-entrada-salida
- **Qué**: Luthier debería poder componer la entrada y salida de un programa con otro, encadenando programas externos.
- **Cita** (verbatim): "Luthier lo que tendría que hacer es poder componer la entrada y salida de un programa y otro" `[00:26]`

### equivalencia-de-caminos
- **Qué**: Una capacidad central es comparar dos caminos para hacer lo mismo y determinar que son equivalentes, posiblemente con etapas de conversión de formato al principio y al final.
- **Cita** (verbatim): "vos comparás dos caminos para hacer lo mismo" `[00:44]`

### verificabilidad-de-funciones
- **Qué**: Luthier debe poder comprobar que una función es correcta. Esto se describe como "una especie de verificabilidad" y aparece como elemento mínimo del lenguaje.
- **Cita** (verbatim): "comprobas que una función es correcta, es la idea de verificabilidad, es como una especie de verificabilidad" `[00:52]`

### decoración-con-tiempo-y-complejidad
- **Qué**: Una vez establecida la equivalencia entre caminos, se puede elegir el que tarda menos y empezar a estimar tiempos de ejecución, complejidad, recursos, éxito/fracaso. Esto se ubica explícitamente en una "segunda capa".
- **Cita** (verbatim): "después poder determinar los tiempos que tardan en ejecutarse algo y que dos caminos son equivalentes con distintos recorridos" `[01:04]`
- **Ambigüedad / tensión**: Se menciona también "definir si las operaciones son exitosas o no, por ejemplo, y recursos" `[04:08]`, pero queda sin desarrollar qué forma tomarían estas decoraciones.

### minimalismo-de-primitivas
- **Qué**: Luthier debería tener los mínimos componentes nativos posibles. La pregunta es cuáles son esos elementos mínimos: quizás solo la identidad y alguna noción de igualdad o equivalencia.
- **Cita** (verbatim): "yo lo que querría es que Luthier sea mínimo, o sea, que tenga los mínimos componentes nativos posibles" `[03:22]`

### funciones-externas-vs-primitivas
- **Qué**: Tensión entre tener funciones primitivas internas o simplemente coordinar funciones existentes por fuera de Luthier. Se da el ejemplo de componer A y B para obtener la identidad, de modo que lo único interno necesario sería la identidad.
- **Cita** (verbatim): "la pregunta es si vos tenés que tener funciones primitivas o simplemente vos coordenás las funciones existentes por fuera de Luthier" `[02:43]`
- **Ambigüedad / tensión**: Queda abierto cuáles serían exactamente los elementos mínimos. "No sé, habría que pensar un poco cuáles son los elementos" `[03:18]`.

### lenguaje-puente
- **Qué**: Luthier como "lenguaje puente" entre otros lenguajes, consecuencia directa del minimalismo: si casi todo es externo, Luthier solo conecta.
- **Cita** (verbatim): "que básicamente sea así, un lenguaje puente, ¿no? Lenguaje puente entre otros lenguajes" `[03:33]`

### delegación-de-ejecución
- **Qué**: Se plantea si Luthier podría delegar incluso la parte de ejecución y quedarse solo con la verificación, como forma extrema de minimalismo.
- **Cita** (verbatim): "a ver si yo hasta puedo delegar la parte de ejecución y que lo único que haga sea la verificación" `[04:35]`
- **Ambigüedad / tensión**: Se reconoce que ejecutar requiere "llamar un montón de cosas" y queda sin resolver si la ejecución es parte de Luthier o no.

### capas-del-lenguaje
- **Qué**: Se distinguen al menos dos capas: la primera capa con equivalencias y verificabilidad; la segunda con tiempo, complejidad, recursos, éxito/fracaso de operaciones.
- **Cita** (verbatim): "Pero eso me parece que es como de la segunda capa. La primera capa sería, bueno, eso." `[04:18]`
- **Ambigüedad / tensión**: La frontera entre capas queda indicada pero no definida con precisión.
