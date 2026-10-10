---
date: 2026-06-05
notes:
  - audio: WhatsApp Ptt 2026-06-05 at 13.09.45.mp3
    transcript: WhatsApp Ptt 2026-06-05 at 13.09.45.md
    duration: ~04:56
    sha256: 74db6870b2d59910948eb9212cbb8b712ac85f819caed9d0fe58113b07c7fae2
  - audio: WhatsApp Ptt 2026-06-05 at 13.16.35.mp3
    transcript: WhatsApp Ptt 2026-06-05 at 13.16.35.md
    duration: ~01:34
    sha256: 5e15e25b0d59f63fd49072e308443e17283068672aa33061b7e9412ca1fc82fc
ideas: 7
quotes_found: 6/7 (match: words)
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### generic-status-and-iteration-across-algorithms
- **What**: A general concept like "status" or "iteration" exists across all optimization algorithms, so there can be a generic `status` or `iteration` class; the particular algorithm it belongs to is known from the context it sits inside.
- **Quote**: "En todo algoritmo tienen iteraciones, en todo algoritmo tenés estatus. Entonces vos podés tener una clase estatus genérica." (`WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[01:33]`)
- **Course**: `[00:05]` of `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3`: starts from the concrete problem of organizing a Gaussian-Newton class, a set of functions and structures representing the algorithm; `[00:50]`: wants to apply the Vector Space logic, a class that already carries the structure and gives access to its records; `[01:20]`: separates `iteración` and `estatus` as concepts more general than those of one algorithm; `[01:37]`: a generic status class is possible; `[01:43]`: you know which algorithm's status it is because it sits inside that algorithm.
- **Open**: Whether the generic class should still carry the algorithm's identifier is left hanging: "debería tener el identifier del algoritmo, posiblemente".

### iteration-is-bound-unlike-the-mean
- **What**: Unlike a component like the mean, which can be lifted out of the moments and used on its own, an iteration cannot live independently; it is inherently the iteration of some algorithm.
- **Quote**: "La iteración es la iteración, sí, es de un algoritmo y es de un algoritmo" (`WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[02:28]`)
- **Course**: `[01:59]` of `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3`: contrasts with the moments, where the mean is the mean of someone in particular yet usable outside the moments; `[02:19]`: the mean can live alone, apart from the variance or the sum; `[02:28]`: the iteration, by contrast, is always of an algorithm.
- **Open**: The precise difference between a component that detaches (the mean) and one that stays bound (the iteration) is asserted but not spelled out.

### algorithm-identity-as-nested-specification
- **What**: What an iteration belongs to is itself structured: an iteration of a method that is a creation of an MLE or MAP, where an MLE could in turn use Gaussian-Newton or another method.
- **Quote**: "es una creación de un MLE o un MAP o lo que sea. Claro si es un MLE podría ser un MLE que usa Gaussian-Newton u otro método si es una máxima likelihood estimation." (`WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[02:46]`)
- **Course**: `[02:35]` of `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3`: should carry the algorithm's identifier; `[02:46]`: the identity is layered (MLE/MAP, then the method it uses); `[03:16]`: asks how you state and store the information of what the thing is.

### database-as-model-for-storing-what-a-thing-is
- **What**: The information of what a record is could be stored as a relational database: fields with elements and relations, a record being a subset of the cartesian product, with duplicates removed.
- **Quote**: "Claro, es un subconjunto del producto cartesiano, sería, ¿no? Una base de datos, de alguna manera..." (`WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[03:58]`)
- **Course**: `[03:24]` of `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3`: a database as one way, fields and their elements; `[03:35]`: it has relations; `[03:43]`: "relational" names interactions; `[03:51]`: records are a subset of the cartesian product; `[04:10]`: duplicate records are eliminated.

### code-as-data-same-treatment-as-records
- **What**: If functions are taken as data, code as data, then they admit the same treatment as database records.
- **Quote**: "Las funciones como datos, o sea, el código como datos. entonces sí podés tener también lo mismo, ¿no?" (`WhatsApp Ptt 2026-06-05 at 13.09.45.mp3` `[04:34]`)
- **Course**: `[04:14]` of `WhatsApp Ptt 2026-06-05 at 13.09.45.mp3`: begins from functions over the data; `[04:34]`: functions as data, code as data, so the same applies.
- **Open**: He breaks off into unfinished questions ("¿Qué es? Es un... ¿Por qué la...?") without resolving what this treatment yields.

### forget-function-as-projection
- **What**: A first form of the "forget" function (`función olvido`): from an object that is the iteration of a given algorithm on a given function under given circumstances, `get iteration` drops everything and leaves a bare iteration; this forgetting is like a projection onto an axis, a reduction of dimensionality.
- **Quote**: "si, lo olvidás sería, es como una especie de proyección una reducción de dimensionalidad" (`WhatsApp Ptt 2026-06-05 at 13.16.35.mp3` `[00:47]`)
- **Course**: `[00:00]` of `WhatsApp Ptt 2026-06-05 at 13.16.35.mp3`: names the first form of the forget function; `[00:05]`: the full object (iteration of an algorithm on a function in circumstances); `[00:16]`: you forget all that and think of it as just an iteration; `[00:42]`: like a projection onto one axis, forgetting the rest; `[00:54]`: a reduction of dimensionality.

### reconstructing-the-object-from-its-projections
- **What**: The projections can be rejoined to recover the original object; the interesting case is projections that are disjoint or complementary, which would be "normal", though they may or may not be.
- **Quote**: "vos unís todas las proyecciones y recuperas el objeto original" (`WhatsApp Ptt 2026-06-05 at 13.16.35.mp3` `[01:07]`)
- **Course**: `[01:02]` of `WhatsApp Ptt 2026-06-05 at 13.16.35.mp3`: the projections can later be reconstructed; `[01:07]`: joining all projections recovers the original; `[01:15]`: the projections would be disjoint or complementary, in which case "normal"; `[01:25]`: they could be or not.
- **Open**: Whether the projections have such properties is left undecided: "que podrían ser o no. No tenés propiedades ahí, ¿no?".

## Notes

none
