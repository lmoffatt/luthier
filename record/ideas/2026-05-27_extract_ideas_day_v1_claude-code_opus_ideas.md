---
date: 2026-05-27
notes:
  - audio: WhatsApp Ptt 2026-05-27 at 13.39.04.mp3
    transcript: WhatsApp Ptt 2026-05-27 at 13.39.04.md
    duration: ~04:54
    sha256: e0221133fc16a196b311284503ddbc2a61220c6bd4423bcda1db98d8389a04de
  - audio: WhatsApp Ptt 2026-05-27 at 13.49.54.mp3
    transcript: WhatsApp Ptt 2026-05-27 at 13.49.54.md
    duration: ~01:02
    sha256: 67d93aacac56a9bee29763cce468e14763f584bff09d98faf3d605b52c3c1817
  - audio: WhatsApp Ptt 2026-05-27 at 13.51.41.mp3
    transcript: WhatsApp Ptt 2026-05-27 at 13.51.41.md
    duration: ~00:52
    sha256: 6dd045065891b06e4252b7bed8e53b366cdd55fdb174a8d07d4e9c2feb1fc689
  - audio: WhatsApp Ptt 2026-05-27 at 13.51.51.mp3
    transcript: WhatsApp Ptt 2026-05-27 at 13.51.51.md
    duration: ~00:54
    sha256: db6ab92a240ee9787a4f655aa00535aa945bee552b9fea675c8b65eeaea1c544
  - audio: WhatsApp Ptt 2026-05-27 at 13.52.41.mp3
    transcript: WhatsApp Ptt 2026-05-27 at 13.52.41.md
    duration: ~00:21
    sha256: bda36a4197cd83d93202f018714dc90f9364c7c2c60481c5c3f722859c0cfb3b
ideas: 11
quotes_found: 11/11
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
---

## Ideas

### luthier-as-butler-running-and-comparing-programs
- **What**: Luthier imagined as a butler that can run basically any program and compare their outputs.
- **Quote**: "me lo imagino como un mayordomo que puede correr" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:00]`)
- **Course**: Note 1 `[00:00]`: the butler image appears; `[00:13]`: it can run basically any program and compare the outputs.

### compose-input-output-and-see-equivalence-of-paths
- **What**: Luthier should compose the input and output of one program and another and see the equivalences, so that two alternative paths that do the same thing can be compared, including conversion stages at the start and end.
- **Quote**: "dos caminos para hacer lo mismo" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:47]`)
- **Course**: Note 1 `[00:26]`: compose the input and output of one program and another; `[00:38]`: see the equivalences; `[00:44]`–`[00:47]`: you compare two paths to do the same thing; `[01:12]`–`[01:20]`: two paths equivalent with different routes; `[01:25]`: it can be a conversion stage from one format to another, at the start and the end; `[01:44]`: verify that the paths are alternatives.

### verifiability-of-functions
- **What**: Beyond comparing paths, verify that a function is correct; this is the idea of verifiability, which with equivalences makes up the minimal elements.
- **Quote**: "que una función es correcta" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[00:52]`)
- **Course**: Note 1 `[00:52]`: in addition to comparing paths, you check that a function is correct; `[00:56]`: he names it "la idea de verificabilidad"; `[02:12]`: he lists "equivalencias y verificabilidad de las funciones" as the minimal elements.

### time-complexity-and-resources-as-a-second-layer
- **What**: A later layer that measures how long things take, lets you pick the faster of two equivalent paths and estimate the time, and decorates runs with complexity, success/failure and resources.
- **Quote**: "la posibilidad de decorar con tiempo y con complejidad y esas cosas" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[03:56]`)
- **Course**: Note 1 `[01:04]`–`[01:10]`: determine the times something takes to execute; `[01:49]`–`[01:57]`: if you can choose between two alternative paths, take the one that takes less time, and later estimate the time; `[02:03]`: these are posterior stages; `[03:56]`: decorate with time and complexity; `[04:08]`: define whether operations are successful or not, and resources; `[04:18]`: this is the second layer, the first being equivalence and verifiability.

### primitives-or-only-the-identity
- **What**: Open question of whether Luthier needs primitive functions or only coordinates functions existing outside it, so the only internal element might be the identity (A∘B = identity means A is the inverse of B).
- **Quote**: "bueno, A no sé lo que es A, pero yo compongo A y B, claro, y me da la identidad, por ejemplo." (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[03:01]`)
- **Course**: Note 1 `[02:43]`–`[02:57]`: the question, primitive functions or just coordinating functions that exist outside Luthier; `[03:01]`: the A∘B = identity example; `[03:08]`: so the only thing you need internally is the identity; `[03:46]`: the only thing you would need is some kind of equality or equivalence function.
- **Open**: left as a question ("habría que pensar"); whether the sole native element is the identity, or an equality/equivalence function, is not decided.

### minimal-bridge-language
- **What**: Luthier should be minimal, with the fewest possible native components, essentially a bridge language between other languages.
- **Quote**: "que tenga los mínimos componentes nativos posibles, cosa que básicamente sea así, un lenguaje puente" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[03:27]`)
- **Course**: Note 1 `[03:22]`: he wants Luthier to be minimal; `[03:27]`: the fewest native components, a bridge language; `[03:39]`: a bridge language between other languages.

### delegate-execution-keep-only-verification
- **What**: Since executing requires calling many things, Luthier might delegate execution entirely and do only the verification.
- **Quote**: "Uno podría decir, bueno, a ver si yo hasta puedo delegar la parte de ejecución" (`WhatsApp Ptt 2026-05-27 at 13.39.04.mp3` `[04:35]`)
- **Course**: Note 1 `[04:27]`: possibly being able to execute; `[04:30]`: to execute you have to call a lot of things; `[04:35]`: maybe delegate the execution part; `[04:43]`: and have it do only the verification.
- **Open**: raised as a possibility ("no sé, habría que ver"), not settled.

### luthier-as-database-of-program-runs
- **What**: Luthier as a database about how programs run: each run generates a characterization (memory used, CPUs, which computer, time, range of results).
- **Quote**: "de los programas, de cada vez que corren es como que generas un output acerca de cómo corrió," (`WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:07]`)
- **Course**: Note 2 `[00:00]`: Luthier as a database of how programs run; `[00:14]`: characterizations of the run, how much memory it used; `[00:20]`: how many CPUs; `[00:26]`: on which computer, how long, what range of results.

### synthesizing-run-data
- **What**: The challenge of synthesizing all the run information so it doesn't become monstrous or paralyzing; yet the summary (the model of the data) can end up bigger than the data itself, which is useful for interpreting a particular case but dangerous.
- **Quote**: "de cómo vos tenés que ir sintetizando esa información para que no se vea paralizante." (`WhatsApp Ptt 2026-05-27 at 13.49.54.mp3` `[00:46]`)
- **Course**: Note 2 `[00:32]`: the problem of how you synthesize all that information in the long run; `[00:39]`: it can be a monstrous thing; `[00:46]`: synthesize so it isn't paralyzing; `[00:54]`: one of the principal challenges of Luthier. Note 3 `[00:00]`: you summarize the string of statistics; `[00:12]`: sometimes the summary is bigger than the text; `[00:17]`: "como hay más interpretaciones de los libros de Borges que los libros de Borges en sí"; `[00:29]`–`[00:34]`: you want an interpretation for a particular case, to predict and interpret; `[00:39]`: "Entonces puede ser que sea más grande el modelo de los datos"; `[00:48]`: "Pero bueno, es peligroso."
- **Open**: the tension between condensing (so it isn't monstrous) and allowing the model of the data to exceed the data is left standing; "es peligroso" is not resolved.

### luthier-as-model-of-the-world
- **What**: Luthier as a model of the world, a model of computation that you keep testing and simplifying and must keep active, through selective forgetting or through aggregation/averaging.
- **Quote**: "Porque vos tenés un modelo de la computación que vas probando, ¿no?" (`WhatsApp Ptt 2026-05-27 at 13.51.51.mp3` `[00:11]`)
- **Course**: Note 4 `[00:00]`: Luthier as something like a model of the world; `[00:11]`: a model of computation that you keep testing; `[00:18]`: and simplifying; `[00:32]`: keeping it active; `[00:35]`: possibly by selective forgetting ("el video selectivo"); `[00:41]`–`[00:47]`: or by aggregation, your average; `[00:49]`: how that is generated is still to be worked out.
- **Open**: the mechanism for keeping the model active (forgetting vs aggregation/averaging) is undecided; "eso hay que ir viendo cómo se genera eso."

### decompose-what-is-lumped-together
- **What**: A first task: understand within Luthier all the things currently put together as one, to see which are functionally different and separable and which depend on which.
- **Quote**: "para ver cuáles son funcionalmente diferentes y separables, cuáles dependen de cuáles." (`WhatsApp Ptt 2026-05-27 at 13.52.41.mp3` `[00:11]`)
- **Course**: Note 5 `[00:00]`: one of the first things is to understand all the things he is putting together as one; `[00:11]`: to see which are functionally different and separable, and which depend on which.

## Notes

none
