# Objectives of Luthier

Draft 0, 2026-10-06. Status: for Luciano to mark, ok, no or a correction under each objective.
Written for Luciano. The principles orient decisions toward these objectives; once they're marked, any decision can be asked which of them it serves.
Sources: his voice notes (luthier docs/audios and the Oral transcriptions repository), his notes in luthier and sonolocalizacion, his typed turns in the Claude Code chats of both projects, his annotations in git. Summaries written by models were used only to find his words.
Who wrote what: text in quotation marks is his, verbatim, at the cited line. Everything else is the model's: each objective heading is its wording of the quotes under it, and the "How we would know" lines and the Tensions are its proposals.

## O1. Be useful now, in a real project, sonolocalizacion first and macroIR after, and not something purely theoretical.
Luciano: "cosa que ya empiece a ser útil. O sea, el tema con Luthier creo que es que tiene que ser útil, tiene que servir para algo que no sea algo puramente teórico,"  (luthier@1196e56:docs/audios/WhatsApp Ptt 2026-09-21 at 11.42.19.md:25)
Luciano: "Luthier va a ser usado en dos proyectos Sonolocalizacion y macroir , en ese orden."  (chat:890a551c:876)
Luciano: "vamos a usar luthier para  correr todos los analisis de sonolocalizacion."  (chat:1e377538:3)
Older words, for context. On 2026-06-03 he wanted syntax and semantics settled before implementing: "una vez que tenemos a Luthier establecida su sintaxis su semántica ahí recién lo empezamos a implementar" (luthier@1196e56:docs/audios/WhatsApp Ptt 2026-06-03 at 12.03.35.md:79). On 2026-08-31, asking himself what objective Luthier would have, he said "y qué objetivo tendría porque hasta ahora es como una aventura una aventura intelectual más que nada," (luthier@1196e56:docs/audios/WhatsApp Ptt 2026-08-31 at 19.48.17.md:253). Whether the September words replace the June ones is his to say; on 2026-10-04 he still wanted the foundations first (see Tensions).
How we would know it is going well (the model's proposal): every sonolocalizacion analysis runs from a .lut program with its certificate, and each change to Luthier's design names the sonolocalizacion case that asked for it.

## O2. Membership in a type certifies that a value passed the type's check, so nothing is checked twice. Functions are included: a function's type is its postconditions and invariants, and defining the function defines its test.
Luciano: "un cosa que odio es cuando un programa chequea dos o mas veces lo mismo. La idea de los tipos es que la pertenerncia a un tipo es un certificado de que eso que el valor pasa el chequeo que el tipo tiene."  (sonolocalizacion@e4d5658:Lucianos ideas dir/funcion de los tipos en Luthier.txt:3)
Luciano: "La idea que me hizo empezar era types as propositions pero extendido tambien a funciones (son tipos) y los tipos de las funciones son sus postconditions e invariantes."  (chat:ba3fd298:4573)
Luciano: "en el cual vos definas una función y que al definir la función ya con eso quede definido el test sobre esa función."  (luthier@1196e56:docs/audios/WhatsApp Ptt 2026-08-31 at 19.48.17.md:121)
How we would know it is going well (the model's proposal): a deliberately broken copy of each certified definition fails with a counterexample, and analysis results carry their certificate, so no later run checks them again.

## O3. Give models a structure to work in at length, and make what they write legible to Luciano, a project written in Python included.
Luciano: "ya no tengo contacto con el código, el código lo hace todo la IA"  (luthier@1196e56:docs/audios/WhatsApp Ptt 2026-08-31 at 19.48.17.md:13)
Luciano: "me parece que podemos hacer ambos como una forma de volver legible un proyecto escrito en python."  (chat:51cca364:2295)
Luciano: "me da la sensacion de que luthier tiene una estructura que permite a la IA trabajar sostenidamente. Nunca me paso que la IA me trabaje toda la noche. Era mi esperanza que luthier sirva para esto"  (chat:fea341bd:122)
How we would know it is going well (the model's proposal): Luciano reads a .lut file without opening the Python and can say whether it states the concept right, and his annotations on .lut files stop asking what the code means.

## O4. Write one concept in several implementations, native and extern, test that they are equivalent, and pick the fastest for each case, keeping the choice.
Luciano: "una de las ideas fundamentales de Luthier es expresar los distintos niveles de equivalencia. Eso tiene que ser, digamos, bastante claro como objetivo, ¿no?"  (luthier@1196e56:docs/audios/WhatsApp Ptt 2026-05-30 at 18.01.53.md:57)
Luciano: "gaussian y profiled justamente deben escribirse tanto como extern como nativas de luthier. Luego las comparamos como test. Ese seria el paradigma."  (chat:51cca364:529)
Luciano: "Mi idea es juntas testing y tipos en una sola cosa y tambien (aunque no lo empezamos) la optimizacion porque si vos tenes un conjunto de implementaciones {f} de F, ejegis la f mas rapida para tu caso particular. Y eso se guarda tambien."  (chat:ba3fd298:4585)
How we would know it is going well (the model's proposal): each sonolocalizacion function with a native and an extern version has a certified equivalence law and a recorded time and error per version. He says the optimization isn't started ("aunque no lo empezamos", chat:ba3fd298:4585), so picking the fastest waits.

## O5. Start from a minimal core that can run on paper, write Luthier schemas that are very reusable, and grow so that the program's function stays and gets stronger instead of degrading.
Luciano: "la idea es que luthier se pueda ejecutar en papel. En realidad lo primero es definir los elementos del lenguaje. La idea era que fuese minimalista y recursivo,"  (chat:890a551c:1)
Luciano: "La idea es que los esquemas luthier sean muy re-utilizables."  (chat:51cca364:2139)
Luciano: "El programa crece, pero la función queda, se fortalece, no se degrada."  (Oral transcriptions@139f059:plan 2026 2/WhatsApp Ptt 2026-06-30 at 10.40.58.md:55)
How we would know it is going well (the model's proposal): macroIR, the second project, uses the definitions in lib/ without changing them, and the kernel stays small enough to reduce an example by hand.

## Tensions (the model's reading)
- O1 (be useful now) against settling the foundations first, which the model reads into O2 (membership in a type is a certificate) and O5 (a minimal core). His words pull both ways: asked whether to try the laws on Vec first, he answered "No, yo lo que quiero primero es estar seguro de que las bases de Luthier estan firmes y completas" (chat:52d3e68e:535, 2026-10-04). Cost if left latent: changes to the kernel force rewrites of sonolocalizacion's .lut layer; it was archived on 2026-10-02 to start again, and archived again on 2026-10-04 to be rewritten under the specification (sonolocalizacion commits 5627ddc and 8c9411a).
- O3 (models work at length) against O2 (membership in a type is a certificate). A certificate is worth the laws it checks, and laws a model wrote and Luciano didn't read certify the model's reading of the concept. Cost if left latent: libraries that pass and miss their concept. src/luthier/lib/random.lut has a certificate (random.cert.json), and the first of his criticisms of it reads "la mas importante en ningun momento se define la invariante de estoscasticidad" (luthier@1196e56:docs/Lucianos observations/random.lut.observations.txt:4).
