---
audio: WhatsApp Ptt 2026-10-07 at 17.02.25.mp3
fecha: 2026-10-07
duracion: ~16:18
ideas: 16
generado_por: extract_ideas_v1
modo: editor
agente: claude-code
modelo: opus
---

## Ideas de diseño

### escala-intermedia-de-amplificacion-con-ia
- **Qué**: El motor del audio es una pregunta abierta sobre el método: si existe un punto medio donde la IA multiplique el esfuerzo del autor sin que el resultado deje de ser legible y cotejable por él. Marca el problema que Luthier vendría a atacar.
- **Cita** (verbatim): "¿existe una escala intermedia donde yo multiplique con la IA mi esfuerzo pero no tanto como para que no sepa lo que da... sino que lo multiplique por algo que yo pueda ver el resultado y lo pueda acotejar bien" `[02:20]`
- **Ambigüedad / tensión**: Queda como pregunta sin respuesta. El autor distingue el caso de un proyecto ya armado con un bug (90% suyo) del armar algo de cero, donde "lo inflo más de lo que puedo digerir".

### tipos-como-proposiciones
- **Qué**: El argumento de fondo para que Luthier exista: tipos como proposiciones, tipos como garantías de cosas, algo que ya existe en otros lenguajes pero que acá se haría "bien claro".
- **Cita** (verbatim): "esto de los tipos como proposiciones y que los tipos sean garantías de cosas que ya existen en muchos lenguajes, pero bueno, hacerlo bien claro" `[03:36]`

### tests-que-nacen-con-la-definicion
- **Qué**: Al definir una función ya se definen los tests que se van a correr, y eso acelera todo el desarrollo. Con la condición de que sea un test de verdad, uno que cubra, no una formalidad.
- **Cita** (verbatim): "cuando vos definís una función ya estás definiendo los test que se van a hacer" `[03:53]`
- **Ambigüedad / tensión**: El autor opone el test "de verdad... que realmente lo cubra" a "una boludez" `[04:09]`, sin fijar qué distingue a uno del otro.

### doble-via-estadistica-y-deductiva
- **Qué**: Tener dos vías de verificación: un test estadístico para lo que no tenés demostración y un test deductivo para lo que sí.
- **Cita** (verbatim): "tener además las dos vías, el test estadístico para cosas que no tenés una demostración... y un test deductivo para los que sí tenés" `[04:37]`
- **Ambigüedad / tensión**: Qué cosas admiten la vía deductiva queda sin cerrar: "para los que sí tenés, que no sé cuáles son".

### garantias-dentro-del-tipo
- **Qué**: Poner dentro del tipo las garantías conocidas de una función (ejemplo: el cuadrado da un número mayor que cero), para no perder información relevante.
- **Cita** (verbatim): "si vos en una función... le vas al cuadrado, bueno, te va a dar un número que es mayor que cero... podés poner eso como dentro del tipo" `[05:00]`

### functores-de-olvido-y-funcion-de-utilidad
- **Qué**: El reverso del anterior: demasiada información abruma y pesa más que lo útil (los "functores de olvido"), así que haría falta una función de utilidad, un cálculo para decidir qué es relevante, y sería interesante poder expresar eso en el lenguaje.
- **Cita** (verbatim): "ya tenés que tener... algún tipo de función de utilidad, un cálculo para poder decidir... qué cosas son relevantes y qué cosas no" `[05:48]`
- **Ambigüedad / tensión**: El propio autor lo marca como no desarrollado: "pero son listas de deseos" `[06:08]`. Queda en tensión con "no perder información relevante" del punto anterior.

### luthier-como-disciplina-para-domar-la-ia
- **Qué**: La relevancia de Luthier sería forzar al autor (y a la IA) a ser metódico, a escribir poscondiciones y a pensar las cosas; un programa que compila en Luthier da cierta seguridad de que no es basura, por analogía con las demostraciones de Lean. Aparece la imagen de "domar la bestia de la IA".
- **Cita** (verbatim): "es que Luthier te, digamos, como que te obliga a ser metódico y a escribir las poscondiciones y todo eso" `[07:51]`
- **Ambigüedad / tensión**: La confiabilidad de Lean la pone "entre comillas" `[06:58]`.

### aparato-de-luthier-vs-hacerlo-a-mano
- **Qué**: Tensión que el autor se plantea: lo mismo (funciones con su verificación) se puede hacer a mano, por formas más baratas, sin todo el aparato de Luthier.
- **Cita** (verbatim): "vos podés hacer esas funciones sin todo el aparato de luthier... simplemente diciendo bueno, vamos a hacer una función con su verificación y todo, hacerlo a mano" `[07:25]`
- **Ambigüedad / tensión**: La responde solo en parte con el punto anterior (Luthier obliga a ser metódico); reconoce "eso es cierto" sobre la alternativa barata.

### interprete-pequeno-autoescrito
- **Qué**: Una vez fijada la sintaxis, escribir él mismo el intérprete de Luthier, eventualmente un núcleo en C para que sea rápido; sería manejable si el intérprete es chico y el resto son líneas de Luthier.
- **Cita** (verbatim): "escribir yo mismo lo que sería el propio intérprete de Luthier, y eventualmente hacer intérprete en C directamente para que sea rápido" `[08:44]`
- **Ambigüedad / tensión**: Él mismo lo desarma enseguida: "eso no tiene mucho sentido porque... hay un montón de librerías ya existentes que voy a tener que usar" `[09:33]`.

### luthier-orquestador-o-codigo-que-pasa-por-luthier
- **Qué**: Dos roles posibles para Luthier, que el código pase por él o que sea un orquestador hacia afuera, y la postura de que convienen los dos y poder pasar de un lado al otro.
- **Cita** (verbatim): "la idea de que el código pase por Luthier o Luthier sea un orquestador más hacia afuera, o las dos... yo creo que está bien que sean las dos cosas, se pueda pasar de un lado al otro" `[10:36]`

### monads-y-juntores-en-luthier
- **Qué**: Duda abierta sobre si hay que poder escribir monads o functores en Luthier, como existen en Haskell.
- **Cita** (verbatim): "una de las dudas es si tengo que... escribir yo monads o cosas por el estilo o juntores en Luthier como existe... en Haskell" `[11:04]`
- **Ambigüedad / tensión**: Sin resolver, y el autor aclara "que igual yo tampoco las entiendo bien" `[11:19]`.

### bnf-de-luthier-bien-definido
- **Qué**: La tarea concreta que se fija: entender la sintaxis de Luthier y quedarse con un BNF bien definido.
- **Cita** (verbatim): "lo que sí tengo que hacer es entender la sintaxis de Luthier... quedarme con un BNF de Luthier bien definido" `[11:29]`

### sonolocalizacion-escrita-en-luthier
- **Qué**: Usar su sonolocalización como caso real: escribirla en Luthier, ver que funcione y que después se ejecute posiblemente en Python.
- **Cita** (verbatim): "escribir ahí mi sonolocalización y ver que eso funcione... que después se ejecuten posiblemente en Python" `[11:40]`

### doble-implementacion-y-chequeo-de-equivalencia
- **Qué**: Para un algoritmo como Levenberg-Marquardt (que iría en Python), escribirlo de las dos maneras, nativo en Luthier y en Python, y comparar equivalencia y velocidad.
- **Cita** (verbatim): "si lo podes escribir de dos maneras, hacerlo en el mermacquart nativo en... Luthier y hacerlo también en Python y ver la equivalencia de los dos y ver la velocidad" `[12:34]`
- **Ambigüedad / tensión**: El nombre lo dice primero como "Levenberg Macquart" `[11:57]` y después como "mermacquart".

### luthier-sintetiza-la-llamada-a-python-y-capas
- **Qué**: Que el programa sintetice, usando la sintaxis de Luthier, la llamada a una función de Python; eso permitiría trabajar en distintas capas, más hacia afuera (Python) o más hacia adentro (Luthier).
- **Cita** (verbatim): "que mi programa me sintetice la llamada a la... de Python usando la sintaxis de Luthier, o sea que Luthier pueda sintetizar la llamada" `[13:19]`

### minimizar-el-slop-de-la-ia
- **Qué**: El código y las especificaciones que genera la IA vienen con relleno que suena bien pero es difícil de evaluar; un criterio posible es reducir hasta el mínimo que siga funcionando, como con un algoritmo.
- **Cita** (verbatim): "se puede reducir esto menos y que siga funcionando... como un algoritmo" `[15:27]`
- **Ambigüedad / tensión**: Queda como vía tentativa ("sí, le voy a hacer esa" `[15:51]`) frente al cansancio de leer especificaciones completas para distinguir lo que sirve de lo que sobra.
