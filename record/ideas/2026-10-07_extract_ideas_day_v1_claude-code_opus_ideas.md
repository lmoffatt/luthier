---
date: 2026-10-07
notes:
  - audio: WhatsApp Ptt 2026-10-07 at 17.02.25.mp3
    transcript: WhatsApp Ptt 2026-10-07 at 17.02.25.md
    duration: ~16:18
    sha256: 80eb8c42c7f14104b9db14e56272ec2c8cda69ebb3cf69c627a0f33cb0344067
ideas: 14
quotes_found: 14/14
generated_by: extract_ideas_day_v1
prompt_sha256: 73e1209ad6ae639a83a6f9a717caaea120e02966659544221e05bb847dd88079
mode: editor
agent: claude-code
model: opus
effort: low
---

## Ideas

### chaining-ai-output-you-can-interpret
- **What**: Claude generates so much output that it is hard to tell what is relevant; the only workable way to use the AI is to chain steps whose result you can interpret.
- **Quote**: "la única manera de usar la inteligencia artificial es encadenar las cosas cosas que uno sepa interpretar lo que tiene" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[00:30]`)
- **Course**: `[00:14]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: the volume of output makes it hard to know if it is relevant; `[00:30]`: the way out is to chain things one can interpret, not just anything, a structure "atada con alambres".

### intermediate-scale-of-ai-leverage
- **What**: Delegating wholesale to the AI means you can't tell if it solved the problem; when a project is already 90% yours the AI helps with a bug, but building from zero doesn't convince him. He asks whether there is an intermediate scale where the AI multiplies his effort by something he can still see and check.
- **Quote**: "¿existe una escala intermedia donde yo multiplique con la IA mi esfuerzo pero no tanto como para que no sepa lo que da no lo infinito sino que lo multiplique por algo que yo pueda ver el resultado y lo pueda acotejar" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[02:20]`)
- **Course**: `[01:04]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: delegating everything, you don't know if it solved it; `[01:33]`: when the project is 90% yours and it fixes a bug, that works, but from zero it doesn't; `[01:56]`: he couldn't build Luthier alone, and inflates it beyond what he can digest; `[02:20]`: the question of an intermediate scale he can verify.
- **Open**: He poses the intermediate scale as a question, doesn't answer it.

### types-as-propositions-tests-from-the-function
- **What**: The core argument for having Luthier at all: types as propositions and as guarantees, so that defining a function already defines the tests that will be run on it, which speeds up development.
- **Quote**: "cuando vos definís una función ya estás definiendo los test que se van a hacer" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[03:53]`)
- **Course**: `[03:36]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: types as propositions and guarantees, which already exist in many languages but done clearly; `[03:53]`: defining a function defines its tests; `[04:09]`: not a token test but one that really covers it.

### statistical-and-deductive-tests
- **What**: Two verification paths for a function's type: a statistical test for what you can't prove, and a deductive test for what you can; keep both because for many things the statistical one is easier.
- **Quote**: "el test estadístico para cosas que no tenés una demostración y un test y un test, digamos deductivo para los que sí tenés" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[04:39]`)
- **Course**: `[04:21]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: a statistical test because a deductive one, though possible, is harder for many things; `[04:39]`: keep both vias; `[04:57]`: example, a squaring function gives a number greater than zero, which can go in the type.
- **Open**: Which cases get the deductive path he leaves unsettled ("que no sé cuáles son").

### forgetful-functors-and-a-utility-for-relevance
- **What**: Carrying too much information overwhelms; the accumulated information can outweigh the useful part, so you need a utility function or calculation to decide what is relevant, and it would be good to express that in the language.
- **Quote**: "algún tipo de función de utilidad, un cálculo para poder decidir, digamos, qué cosas son relevantes y qué cosas no" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[05:48]`)
- **Course**: `[05:22]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: the problem of forgetful functors, too much information overwhelms; `[05:48]`: hence a utility function to decide relevance, worth expressing in a language; `[06:08]`: he calls these "listas de deseos".
- **Open**: Named as a wish list, not developed.

### language-that-forces-method-tames-the-ai
- **What**: Packaging these demands in a language that forces you to be careful and methodical is how you tame the beast of the AI; as Lean's proofs are reliable, a program that compiles in Luthier gives some assurance it isn't garbage.
- **Quote**: "uno empaqueta eso en un lenguaje que te fuerza, te obliga a ser, digamos, cuidadoso ... podés de alguna manera domar la bestia de la IA" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[06:16]`)
- **Course**: `[06:16]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: the language forces care and tames the AI; `[06:39]`: like Lean's proofs being reliable, a Luthier program that compiles gives assurance; `[07:51]`: Luthier obliges you to be methodical and write the postconditions, which makes you think.

### cheaper-alternatives-exist
- **What**: Against his own argument: you could write those verified functions by hand without the whole Luthier apparatus; the justification is only that Luthier obliges you to be methodical.
- **Quote**: "hay otras formas más baratas de hacer eso ... vos podés hacer esas funciones sin todo el aparato de luthier" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[07:15]`)
- **Course**: `[07:15]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: you can do the function with its verification by hand, without a program to do it; `[07:47]`: but he thought Luthier forces method and that is a good thing.

### write-the-interpreter-by-hand-small-core-in-c
- **What**: Once he pins down Luthier's syntax (lines of which already exist that he didn't write), he could write things by hand and write the interpreter himself, eventually a small interpreter in C for speed, with the rest in Luthier lines.
- **Quote**: "tratar de escribir yo mismo lo que sería el propio intérprete de Luthier, y eventualmente hacer intérprete en C directamente para que sea rápido" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[08:44]`)
- **Course**: `[08:16]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: Luthier code exists that he didn't write because he wasn't sure of the syntax; `[08:44]`: once he finds the syntax he could write the interpreter himself, eventually in C; `[09:09]`: a way to manage it if the interpreter is small, few C lines and the rest Luthier lines.

### clash-external-libraries-vs-code-through-luthier
- **What**: A tension he names directly: using existing external libraries is unavoidable, and that clashes with the idea of the code passing through Luthier; Luthier could be an orchestrator pointing outward, or the code passes through it, or both, and he thinks both is fine with passage between them.
- **Quote**: "la idea de que el código pase por Luthier o Luthier sea un orquestador más hacia afuera o las dos" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[10:36]`)
- **Course**: `[09:33]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: it makes no sense to build everything from scratch, there are many existing libraries he'll have to use; `[10:26]`: that is where the two ideas clash; `[10:51]`: both can be done and it's good they be both, passing from one side to the other.

### monads-functors-in-luthier
- **What**: An open doubt about whether he has to write monads or functors in Luthier, as Haskell has a way to write monads, which he admits he doesn't understand well.
- **Quote**: "una de las dudas es si tengo que ver por tener que escribir yo monads o cosas por el estilo o juntores en Luthier" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[11:04]`)
- **Course**: `[11:04]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: the doubt whether he must write monads/functors in Luthier as in Haskell, which he doesn't fully understand.
- **Open**: Left as a doubt, unresolved.

### pin-down-the-bnf-and-write-sonolocalizacion-in-it
- **What**: What he does have to do: understand Luthier's syntax, keep a well-defined BNF, and try to write his sonolocalización in it and see it work, with execution possibly in Python.
- **Quote**: "lo que sí tengo que hacer es entender la sintaxis de Luthier o sea, quedarme con un BNF de Luthier bien definido y tratar de escribir ahí mi sonolocalización" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[11:29]`)
- **Course**: `[11:29]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: understand the syntax, fix a well-defined BNF, write sonolocalización in it and see it work, executed possibly in Python.

### levenberg-marquardt-two-ways-check-equivalence
- **What**: Writing an algorithm like Levenberg-Marquardt both natively in Luthier and in Python, and checking the equivalence of the two and the speed.
- **Quote**: "hacerlo en el mermacquart nativo en en Luthier y hacerlo también en Python y ver la equivalencia de los dos y ver la velocidad" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[12:34]`)
- **Course**: `[11:49]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: something like Levenberg-Marquardt would have to be in Python, not Luthier; `[12:34]`: but it could be written both ways and the equivalence and speed compared.

### luthier-synthesizes-the-python-call-working-in-layers
- **What**: Luthier should be able to synthesize the call to a Python function using Luthier syntax, so one can work in different layers, more outward or more inward of Python.
- **Quote**: "que mi programa me sintetice la llamada a la asunción de de Python usando la sintaxis de Luthier" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[13:19]`)
- **Course**: `[13:19]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: Luthier synthesizes the Python call from Luthier syntax; `[13:39]`: this lets him work in different layers, more outward or inward of Python.

### slop-and-minimization-as-test
- **What**: The AI fills the output with filler that sounds good but is cognitively hard to judge as useful; a way to handle it is to ask whether the thing can be reduced further and still work, as one would minimize an algorithm.
- **Quote**: "se puede reducir esto menos y que siga funcionando" (`WhatsApp Ptt 2026-10-07 at 17.02.25.mp3` `[15:27]`)
- **Course**: `[14:18]` of `WhatsApp Ptt 2026-10-07 at 17.02.25.mp3`: the amount of generated code is too much to manage, he'll have to read the specs and documentation; `[14:43]`: reading becomes tiring and it is hard to tell if it solves the problem or has excess; `[15:06]`: the slop fills with filler that sounds good but is hard to judge; `[15:27]`: minimization as a test, can it be reduced and still work; `[15:51]`: harder when you are writing specifications, but he'll apply it.

## Notes

none
