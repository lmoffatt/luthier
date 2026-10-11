# Decisions

The decision log of luthier. Written for the audits and for anyone checking why something is the way
it is. An entry is written when its decision is taken; a decision that is reversed keeps its entry,
marked reversed. Sources follow the grammar of `docs/plan-working-method-execution-2026-10-06.md`;
principles are named by number, their statements are in `docs/principles.md`. Luciano's answers to
the bites of the plan are at `efd8143`, cited as `plan@efd8143`.

```
D-2026-10-06-a  Material is classed by authorship, in the kinds of working method §4.
Author:     Luciano for the axis; the model for the scheme
Quote:      "And authority is somewhat too much"
Source:     luthier@2a660c8:docs/working-method.md:74
Kind:       principle. For P1
Status:     proposed (the scheme hasn't been discussed)

D-2026-10-06-b  One decision log per repository; a decision that affects both goes in both.
Author:     Luciano
Quote:      "un decision log per repository, decisiones que afectan a ambos se ponen en ambos."
Source:     luthier@2a660c8:docs/working-method.md:302
Kind:       principle. For P7
Status:     current

D-2026-10-06-c  Luciano's sources stay in their language and are committed before anything
                cites them.
Author:     the model, confirmed by Luciano
Quote:      "true"
            "ok"
Source:     luthier@2a660c8:docs/working-method.md:65
            luthier@2a660c8:docs/working-method.md:67
Kind:       principle. For P1, P2
Status:     current

D-2026-10-06-d  Luciano's notes stay where he wrote them, as part of his sources.
Author:     Luciano
Quote:      "Mis notas (como estas) se quedan donde estan, pero forman parte de A"
Source:     luthier@2a660c8:docs/working-method.md:305
Kind:       free ("estoy abierto a sugerencias", same line)
Status:     current

D-2026-10-06-e  A correction keeps the original and puts the corrected version in front.
Author:     Luciano
Quote:      "In this case we might, store the old version and replace it with the correction
            with a note at the begining of the document."
Source:     luthier@2a660c8:docs/working-method.md:60
Kind:       principle. For P3
Status:     current

D-2026-10-06-f  Every change is applied on top of a commit.
Author:     Luciano
Quote:      "si siempre comiteamos antes de aplicar un cambio, en principio toda decision es
            reversible"
Source:     chat:7217f251:196
Kind:       principle. For P6, P5 (what makes free choices cheap)
Status:     current

D-2026-10-06-g  A model takes decisions within margins, following principles; Luciano keeps
                safety, and the principles and the conflicts between them.
Author:     Luciano; the part on principles and conflicts was the model's, settled by
            D-2026-10-06-r
Quote:      "The agent has to make decisions otherwise it will be stuck."
            "salvo cuestiones de seguridad"
Source:     luthier@2a660c8:docs/working-method.md:44
            luthier@2a660c8:docs/working-method.md:234
Kind:       principle. For P4, P5; against P9 unless the end-of-task report is kept
Status:     current

D-2026-10-06-h  Reversibility, the parts of working method §8 that "Si." confirmed as a bundle.
Author:     the model
Quote:      "Si."
Source:     chat:7217f251:227
Kind:       principle. For P6, P2, P3
Status:     by part:
            - one decision per commit: dropped by D-2026-10-06-s; commits stay small by habit
            - a reversal keeps its entry as a datum: current, "es un si", chat:8d5ce152:257
            - the model's margin is what can be undone before Luciano next looks: replaced by
              D-2026-10-06-m (a decision is local when one commit undoes it and nothing
              depends on it yet)
            - push only tagged milestones: current, "es un si", chat:8d5ce152:257
            - local git for the memory: current, "Ok", plan@daa5b95 line 195
            - local git for the oral transcriptions, text only: current, same line
            - manifests for raw data: current, "ok", plan@daa5b95 line 208
            - git outside the folder for large derived data: deferred, "ok", plan@daa5b95
              line 219

D-2026-10-06-i  The git for large data keeps its repository outside the folder it tracks.
Author:     the model, decided by the implementation
Kind:       case: sonolocalización tracks 234 files under prototipo-cero/2026-09-07/derived/
Status:     current, and deferred

D-2026-10-06-j  A document for Luciano is committed before he annotates it; his annotations are
                then committed verbatim, so they are the diff.
Author:     the model, confirmed by Luciano
Quote:      "es un si"
Source:     chat:8d5ce152:257
Kind:       case: his annotations on draft 0 of the method had to be separated from the model's
            text by rebuilding draft 0 from the transcript; on the plan they came as a diff
Principles: for P1, P8
Status:     current

D-2026-10-06-k  The chat exports go to GitHub.
Author:     Luciano
Quote:      "I think that the chat exports should be in GItHub because they are the ultimate
            proof (the audios) of the ideas origin."
Source:     chat:7217f251:366
Kind:       principle. For P1
Status:     current. How (bite 1, "ok", plan@efd8143 line 87): Luciano skims each export before
            committing it, the script lists first the turns with a word of a private list,
            and a session on sonolocalización's private matters is exported into that
            repository.

D-2026-10-06-l  In a document for Luciano, a numbered reference carries its statement; records
                may be terse.
Author:     Luciano
Quote:      "Fijate la idea de que documentos que yo voy a consumir no pueden referir a
            principios con numero porque no se de que me estas hablando."
            "Documentos que son de registro pueden ser sintenticos, eso se aplica para los que
            son de mi consumo"
Source:     chat:7217f251:366
            chat:7217f251:382
Kind:       principle. For P12
Status:     current

D-2026-10-06-m  A step is a bite of decision Luciano can handle, with implications beyond its
                place; local decisions are the model's margin.
Author:     Luciano for the criterion; the model for its tests (plan §1)
Quote:      "una step deberia ser un bocado de decision que yo pueda manejar y que tenga
            implicancias mas que locales."
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:37
Kind:       principle. For P12, P4
Status:     current

D-2026-10-06-n  CLAUDE.md is a living document of operative rules, with no meta-information.
Author:     Luciano
Quote:      "Este documento que lee claude no deberia tener la metainformacion ya que es gastar
            tokens al pedo, las meta-anotaciones estaria fuera."
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:163
Kind:       principle. For P8, P12
Status:     current. Its content is bite 3 of the plan ("ok", plan@efd8143 line 163), less
            the lines D-2026-10-06-s drops and plus D-2026-10-06-r.

D-2026-10-06-o  The principles audit asks three questions (followed and useful; failing by
                conflict; new principles and their cost) and is run by a script.
Author:     Luciano; the trigger is the model's, confirmed
Quote:      "Aqui la idea es que cada tanto un script llame a leer el repositorio a un agente y
            que analice dos cosas"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:116
Kind:       principle. For P4, P13
Status:     current. Trigger (bite 4, "ok", plan@efd8143 line 189): before each push of main
            and on request, run by hand; the reminder hook was dropped by D-2026-10-06-s. The
            prompt follows the scheme of the extraction of ideas (same line).

D-2026-10-06-p  Luciano's observations on code live in a folder of their own, outside the code,
                each committed alone, so that the commit pins the code they observe.
Author:     Luciano for the folder; the model for the commit alone and the pin
Quote:      "quizas lo mejor sea hacer un directorio Lucianos observations y poner mis
            observaciones ahi?"
            "porque modificar el codigo es modificar el hash y es mala idea"
            "si, es el mismo contenido"
Source:     chat:8d5ce152:107
            chat:8d5ce152:108
            chat:8d5ce152:140
Kind:       principle. For P1, P2
Status:     current. Carried out in d41026e; sonolocalización's Lucianos feedbacks/ is the
            same kind of material and keeps its name, committed in sonolocalizacion@6485d1a
            (bite 11, "OK", plan@efd8143 line 361). Of his reason, the fact is narrower: a file
            next to the code changes no hash, but any file under src/luthier, even
            untracked, makes the lock report "with uncommitted changes".

D-2026-10-06-q  A plan comes in two documents: the decisions for Luciano, the execution for the
                sessions.
Author:     the model, asked by Luciano for this plan, confirmed as a rule
Quote:      "hace la separacion"
            "es un si"
Source:     chat:8d5ce152:140
            chat:8d5ce152:257
Kind:       principle. For P12
Status:     current

D-2026-10-06-r  The model raises a latent conflict between principles when what it could cost is
                worth Luciano's attention, without nitpicking; he decides.
Author:     Luciano
Quote:      "bueno, pero vos podes llamarme la atencion de posibles conflictos, sin buscar el
            pelo al huevo, tenes que evaluar el costo posible del conflicto latente."
Source:     luthier@efd8143:docs/plan-working-method-2026-10-06.md:372
Kind:       principle. For P4, P12
Status:     current

D-2026-10-06-s  A mechanism with a recurring cost (per commit, per session, or on Luciano's
                attention) is added only after a real case it would have caught. Applied to
                the plan: dropped the Decision: line in commits and its reminder (step 2.2),
                the header check (4.3), the hook before a push (5.2); the correspondence audit
                by prompt (5.3) waits for the next round of the interpreter; one decision per
                commit is no longer a rule. Commit before every change stays.
Author:     the model, after Luciano's annotations; accepted
Quote:      "El runaway de costo burocratico ya lo siento."
            "aca tengo miedo de un problema y es que una decision un commit puede llevar
            demasiada carga a git?"
            "Asceleremos que estamos estaticos."
Source:     luthier@efd8143:docs/plan-working-method-2026-10-06.md:295
            luthier@efd8143:docs/plan-working-method-2026-10-06.md:154
            chat:8d5ce152:257
Kind:       principle. For P8, P12; against P9, since the end-of-task report is now the only
            check on the decisions the model takes alone. Git itself carries commits at no
            real cost: 70 commits weigh nothing next to the 49 .ogg tracked in docs/audios.
Status:     current, except the deferral of step 5.3, reversed by D-2026-10-06-x

D-2026-10-06-t  Sources are written in one grammar: repo@commit:path:line (or :a-b), and
                chat:session8:line.
Author:     the model, confirmed by Luciano
Quote:      "ok"
Source:     luthier@efd8143:docs/plan-working-method-2026-10-06.md:118
Kind:       case: draft 1 of the plan wrote sources five ways, one of them unreadable by a
            script. For P2
Status:     current. The other half of the same bite (a Decision: line per commit) was
            dropped by D-2026-10-06-s.

D-2026-10-06-u  A quote that the check of quotes finds at its line confirms a decision of
                Luciano's; the statements go through the fidelity audit.
Author:     the model, confirmed by Luciano
Quote:      "ok"
Source:     luthier@efd8143:docs/plan-working-method-2026-10-06.md:206
Kind:       principle. For P8, P12; against P1 until the fidelity audit runs
Status:     current

D-2026-10-06-v  The objectives of each project are written down, in Luciano's words, for him to
                mark; the principles and the synthesis of P12 are measured against them.
Author:     the model, from Luciano's annotations on P4 and P12
Quote:      "algo que tenga que ver con el objetivo del proyecto."
            "de acuerdo a los objetivos del proyecto."
Source:     luthier@efd8143:docs/plan-working-method-2026-10-06.md:255
            luthier@efd8143:docs/plan-working-method-2026-10-06.md:323
Kind:       principle. For P4, P12, P13
Status:     proposed; drafts in docs/objectives.md

D-2026-10-06-w  P12 (Luciano's attention is the scarce resource) goes into his global
                CLAUDE.md, which applies to every project.
Author:     Luciano
Quote:      "(esto es un principio generalizable a toda interaccion con IA)"
Source:     luthier@efd8143:docs/plan-working-method-2026-10-06.md:323
Kind:       principle. For P12
Status:     current; ~/.claude/CLAUDE.md is outside git

D-2026-10-06-x  The correspondence audit runs now, both directions, not deferred: that the
                specification reflects the implementation and the documentation is what matters
                most to Luciano. Reverses the part of D-2026-10-06-s that deferred step 5.3.
Author:     Luciano
Quote:      "A mi lo que mas me importa es saber si las especificaciones de luthier son un fiel
            reflejo de la documentacion y de la implementacion"
Source:     chat:8d5ce152:487
Kind:       principle. For P4, P1; P8 is met, since there were real cases: R11 decided and not
            enforced, R10 without tests
Status:     current; the first run, by workflow, at b15f2a1 (an attempt at f079e0d failed to
            authenticate); its report is docs/audits/2026-10-06_correspondence_v1_claude-opus-5-5.md

D-2026-10-06-y  Every normative statement of docs/semantica carries an identifier, never reused:
                R, G and C as today, S for 02, K for 04, N for 06, L for 07, and in 00, 01 and
                03 only what code enforces. A checker message carries the identifier of its
                rule, a test of tests/spec is named by it, and check_spec_tests.py grows into a
                check of traceability with an explicit list of what the checker decides outside
                the specification. The identifiers enter the specification once the report of
                the correspondence audit is in; the code, in the next round of the interpreter,
                since any change to it invalidates every certificate.
Author:     the model, confirmed by Luciano
Quote:      "Acetpo todas tus sugerencias."
Source:     chat:8d5ce152:675
Kind:       principle. For P2, P4; P8 is met, with real cases: R10 without tests, R11 not
            enforced, four documents whose rules no code can cite
Status:     current; not started

D-2026-10-06-z  The invariant of stochasticity is written before A-9 builds generators on it, as
                a library task under today's tester: the invariant, its statistical tests at a
                level, and an extern source that draws in batches. Seed is a key and a counter.
Author:     the model, from Luciano's observations on random.lut; confirmed by Luciano
Quote:      "la mas importante en ningun momento se define la invariante de estoscasticidad"
            "Acetpo todas tus sugerencias."
Source:     luthier@d41026e:docs/Lucianos observations/random.lut.observations.txt:4
            chat:8d5ce152:675
Kind:       principle. For P10, P4; changes the order of A-9 in plan-2026-10-06
Status:     current; starts when the correspondence audit, which reads the tree, is done

D-2026-10-07-a  Luthier proper is separated from the record of its development: README, docs/,
                src/, examples/ and tests/ present Luthier; record/ holds how it came to be.
                scripts/ and prompts/ stay at the root. Three passes: the record moves, then
                docs/semantica becomes docs/spec, then guide/ and rationale/ are split from it.
Author:     Luciano for the separation and what proper contains; the model for the layout and
            the passes
Quote:      "Luthier proper serian los elementos  minimos para presentar Luthier a la comunidad:
            documentos explicativos, documentos tecnicos, codigo y ejemplos."
            "si, scripts y prompts quedan en la raiz. Y acepto 1-3"
Source:     chat:c15e8d85:196
            chat:c15e8d85:284
Kind:       principle. For P12, P1; P7 kept (one repository; the record can be split off later
            without losing history)
Status:     current. The transcript of c15e8d85 is under ~/.claude-databaum/projects/, not
            ~/.claude/projects/: check_quotes needs --transcripts for it.
```

D-2026-10-07-b  A function defined by its laws is an element of the guide: a type over an
                exponential defined by the laws of the function, whose values are its
                implementations, each certified against the same laws. Written once over a
                number model, `Exp (R : U) (m : NumberModel R)`: `Exp Real realModel` is the
                ideal, declared and never run; `Exp Float64 (float64Model tol)` runs. The arrow
                between them goes from the ideal to the doubles, `realize f x = round (f x)`, and
                a machine exp realizes the ideal when it stays within tolerance of that; stated,
                not run, until a Real computes (06 §9). The other direction, `Exp Float64 : Exp
                Real`, is false and R9 rejects it. examples/exp.lut holds it with two models, a
                Taylor sum and math.exp; section 8 of the guide replaces the agreement law
                `SameDouble`, which R10 does not count as a law, by `Double` defined by its
                recursion.
Author:     Luciano for the element, its example and the generic form; the model for the writing,
            for the number model as the parameter, and for the direction of the arrow
Quote:      "Hay un tema: Funcion Type es un concepto importante"
            "Lo de serie de Taylor fue lo unico que se me ocurrio como una distinta implementacion de exp"
            "Exp (R: U) : R->R := {Homeomorf R & Atzero R}"
Source:     chat:182f2465:3
            chat:182f2465:176
            chat:182f2465:270
Kind:       principle. For P10, P1; P11 for the tolerance. The model as a parameter is the
            generic definition of 06 §4 and the number model of 06 §7
Status:     current. The transcript of 182f2465 is under ~/.claude-databaum/projects/, not
            ~/.claude/projects/: check_quotes needs --transcripts for it.

D-2026-10-07-c  `Real` stays the ideal, declared and never run, and the reals by construction
                (Cauchy sequences of rationals with a modulus, `examples/cauchy.lut`) are one more
                realization of it beside `Float64`, not its definition. The alternative, defining
                `Real` as `Cauchy`, would make `Float64 : Real` an embedding instead of a subset
                and touch R9's free passage of a double where a real is expected and 06 §2.
                With this realization the arrow of examples/exp.lut, from the ideal to the
                doubles, can be run: `roundC (f (fromDouble x))`.
Author:     Luciano, choosing between the two options the model stated
Quote:      "a, por supuesto."
            "Pasemoslo a examples por ahora."
Source:     chat:182f2465:462
Kind:       principle. For P10, P6 (nothing in the kernel changes), P8
Status:     current. The transcript of 182f2465 is under ~/.claude-databaum/projects/.

D-2026-10-07-d  The element of the guide for a function defined by its laws is named "Theory and
                model": Hilbert's implicit definition made a type, the type the theory and a value
                a model, so `Exp` and `Ring` are one element. The guide gains the section
                "Declared, defined, computable": a value is a hole, a procedure or a datum, and the
                line is how many observations an answer needs; declared is defined implicitly,
                defined explicitly, computable reduces to a datum. Eight changes, one commit each
                (33d3f87..7c2f86f).
Author:     Luciano for the question and the choice; the model for the name, taken from 05 §1 and
            01 §2, and for the eight changes
Quote:      "Function definition by Properties as a type ? Podria ser by postconditions, pero buscamos algo mas generico mas matematico no?"
            "Si, hacelo. QUiero ver como queda"
Source:     chat:182f2465:508
            chat:182f2465:515
Kind:       principle. For P12, P1; the principle of 07 (one name for each concept)
Status:     current. The transcript of 182f2465 is under ~/.claude-databaum/projects/.

D-2026-10-07-e  No loose functions: a value is defined only at a defined type, and an exponential
                without laws is a base, as a lawless product is (R4); a function is a value of a
                defined function type, a theory. The guide's list is reordered around it (Type,
                Value, Declaration, Law, Subtype/theory, Function type, Definition, ...), 05 R2
                and R4 carry the rule as decided and not implemented, and P14 is proposed in his
                words. The libraries do not comply (exp in real.lut, the helpers); check -v is to
                report loose functions first.
Author:     Luciano
Quote:      "Las funciones como valor son de un tipo de una funcion definida."
            "Pero para habitarlo primero lo tenemos que definir."
Source:     chat:182f2465:568
            chat:182f2465:575
Kind:       principle. For P10, P4; P8 is met, the real case is exp without laws in real.lut
Status:     current; not implemented. The transcript of 182f2465 is under ~/.claude-databaum/projects/.

D-2026-10-07-f  The elements of the guide follow Luciano's scheme: Type with its bases, named by
                alias; the formers of a bicartesian closed category; the dependent type, an
                element of its own; Law; subtype by law as the theory, the way to define a type;
                value as the model, the way to define a value; declaration; recursion as the
                second way (R4); apply and reduce. A functor is a theory over U, not an element;
                a lawless function is an alias; Function type folds into the theory, Value and
                Definition into the model (amends the list of D-2026-10-07-e, not its rule).
Author:     Luciano for the scheme, the dependent type, and functors as an alias of their object
            map; the model for Law and Recursion as elements, for the alias of a lawless
            function, and for folding Function type, Value and Definition
Quote:      "SubType por Ley --> unica forma de definir nuevos nombres?"
            "Otro tipo elemental que falta es el dependent type."
Source:     chat:d3b76232:386
            chat:d3b76232:445
Kind:       principle. For P14 (proposed), P10, P12
Status:     current. The transcript of d3b76232 is under ~/.claude-databaum/projects/.

D-2026-10-07-g  GPT's reading of the list of elements is answered point by point in record/IA; the
                guide is corrected on eleven points and says what the specification answers on
                four; point 2 is declined on P14, with the reading that an explicit definition is
                the model of the singleton theory whose law is its formula, so a function without
                laws of its own is an expression, an alias, or that model. A mirror of the list,
                with why each thing is said, is record/elements-rationale-2026-10-07.md.
Author:     Luciano for the reply, the corrections and the mirror, and for the singleton reading;
            the model for the verdict on each point and the wording
Quote:      "y de alguna forma zafar y decir lo que queremos decir"
            "escribi un documento contestando las correccione de GPT en el mismo directorio y luego corregi el fundamental-elements"
            "un documento espejo en record donde seas mas explicito en porque decimos que cosa"
Source:     chat:d3b76232:534
            chat:d3b76232:553
            chat:d3b76232:553
Kind:       principle. For P14 (proposed), P1, P3; P12 in the form of the reply, a screen per point
Status:     current. Transcript under ~/.claude-databaum/projects/.

D-2026-10-07-h  Program is an element of the guide, the last of the list: the theories a program
                states, the models it gives them, and the compositions of models by application,
                certified as a chain graded by its weakest link (05 §7); taken from the closing
                hierarchy of GPT's reading.
Author:     Luciano; the model for the wording and the place
Quote:      "Program como la composicion de Theorias y Modelos suena una buena idea que habria que incluir."
Source:     chat:d3b76232:593
Kind:       principle. For P14 (proposed), P12
Status:     current. Transcript under ~/.claude-databaum/projects/.

D-2026-10-08-a  The program's relation with the world, and its certificates, are read in a Bayesian
                frame: the program is an observer that updates its knowledge of the world by what
                it reads. With exact laws and assumed hypotheses the frame works in its logical
                limit, probabilities 0 and 1 (Cox's theorem, as Jaynes uses it, makes graded
                knowledge probability). Probabilities enter with the classes of 09 §9 and with the
                grade sampled, whose n cases from a declared generator are evidence on a law.
Author:     Luciano; the model for the logical-limit reading and the wording
Quote:      "pero una vez que ponemos probabilidades si, se vuelve bayesiano."
            "Bayes es observador <->Universo actualizando su conocimiento de acuerdo a lo que observa."
            "Bueno, si tomamos el grado sampled de los certificados estamos en pleno universo bayesiano."
Source:     chat:893831f1:94
            chat:893831f1:94
            chat:893831f1:102
Kind:       principle. For P4, P10; bears on D-2026-10-06-z, whose "statistical tests at a level"
            are open to restatement in this frame
Status:     current. Not yet in 05 §7 nor in docs/rationale/09-extern-and-the-world.md.

D-2026-10-08-b  The elements of the guide are framed by Luthier's view of computation: a timeless
                part, the plan, equivalence of expressions, and a temporal part, the execution of
                actions, tied both ways (the properties of actions and the strategies of their
                composition are values of types under the timeless rules; the equivalences are
                computed by executing actions), with knowledge between them read as Bayesian
                (D-2026-10-08-a). The list is grouped in three: the plan, the execution (action and
                reading, extern, world and pointer, execution and trace, realization), and what is
                known (certificate). The elements of the guide are fixed before the notes that
                argue them (09) are reviewed.
Author:     Luciano for the view and for fixing the elements first; the model for the grouping,
            the elements of the execution and of what is known, and the wording, to be reviewed
Quote:      "con partes atemporales (basicamente equivalencia de expresiones) y partes temporales (ejecucion de acciones)"
            "1-> las propiedades de las acciones y las estrategias de su composicion pueden ser vistos como elementos de tipos sujetos a las reglas atemporales de equivalencia."
            "2-> el calculo de las reglas de equivalencia se hace a traves de la ejecucion de acciones."
            "Lo importante para mi es fijar los elementos de Luthier de una vez"
            "si agrega lo que te parezca cuando llegue lo reviso."
Source:     chat:893831f1:131
            chat:893831f1:131
            chat:893831f1:131
            chat:893831f1:152
            chat:893831f1:152
Kind:       principle. For P12, P4; the execution group takes the four bullets of 09 §11 plus
            action and reading, ahead of the five decisions 09 leaves to Luciano
Status:     current, in docs/guide/00-fundamental-elements.md at 8863420; to be reviewed by
            Luciano.

D-2026-10-08-c  The list of elements is written for one use: to state the interpreter of Luthier in
                Luthier, with the executable kernel reduced to what a host must do (reduce terms
                given as data, the operations of the primitive types, call an extern and read and
                write a File); the parser, checker, tester and certificates would be Luthier
                definitions over Program, and the first Luthier interpreter is certified against
                the Python one.
Author:     Luciano for the aim and the minimal kernel; the model for the list of three and the
            certification against the Python host
Quote:      "la idea es escribir la especificacion del interprete / compilador lo que sea de Luthier en luthier."
            "Tengo la idea de que si reducimos el nucleo ejecutable de luthier al minimo  es posible ejecutar en luthier."
Source:     chat:893831f1:158
Kind:       objective. For P7, P10; moves section 5 of the guide, the program as data, from a
            later layer to the aim the list is written for (still not in version 0)
Status:     current, in docs/guide/00-fundamental-elements.md at 8863420.

D-2026-10-09-a  The bibliography holds pointers, not copies: no PDF or book enters git, and each
                source is linked by its DOI (the publisher's or the author's page where it has
                none). The copies read stay in record/bibliography/pdf/, outside git, each pinned
                by its SHA-256 in record/bibliography/README.md.
Author:     Luciano; the model for keeping the hash of the copy read
Quote:      "si no commiteemos pdfs ni libros. Tomemos el doi como link."
            "como puntero quiero decir"
Source:     chat:b377c2a0
Kind:       rule. For P2 (the hash says which copy was read); P7 (each repository is
            self-contained) gives way for sources, which are pointed at as a File is in 09 §5
Status:     current, in record/bibliography/ and .gitignore.

D-2026-10-09-b  Candidate principles are found by infectability and kept by P13: the distillation
                chooses and orders its candidates by infectability (Luciano's criterion of May for
                finding Luthier's principles: how much an idea changes the way of programming, on
                four axes, frequency not being one), and whether a principle stays is judged later
                by the decisions it guides once applied. Recurrence is shown as data, not used to rank.
Author:     Luciano chose among three options; the model wrote them, after finding that the
            distillation it had written ranked by recurrence, against the criterion he had chosen
Quote:      "Ok vamos con la 3."
            "La infectabilidad no es un principio *de* Luthier; es el mejor criterio *para
            encontrar* los principios de Luthier: las ideas que más cambian la forma de programar
            son las que más estructuran el lenguaje."
Source:     chat:8c2cb06b:1185
            luthier@97330c9:prompts/consolidate_ideas_v1.md:29
Kind:       method. The second quote is his criterion as the prompt records it; the model's memory
            of 2026-05-30 records that he chose to keep it. For P1 (his criterion, not one the
            model chose), P13 (kept in its place)
Status:     current for its two criteria; where they act changed with D-2026-10-09-c (the single
            distillation became a blind finding step and a matching step)

D-2026-10-09-c  The step that finds candidate principles is blind: it sees only the lineages, the
                language's name and designers, and Luciano's criterion of infectability unchanged,
                with no description of Luthier, no principles in force, no log and no objectives;
                a second step sets its candidates against what is in force. A table that read the
                axes for Luthier's two kinds of idea was dropped. The filter is tested by a control
                on Python and Haskell (record/controls/), with references fixed before any run, a
                baseline of what the model knows without the corpus, and names redacted.
Author:     Luciano for the principle and the control; the model for the two steps, the baseline
            and the redaction (the last two after his objection that a model knows Python and
            Haskell)
Quote:      "estan inyectando ideas de Luthier en el filtro que busca las ideas de Luthier."
            "hace el control sobre python y haskell me gusto"
Source:     chat:8c2cb06b:1427
            chat:8c2cb06b:1439
Kind:       method. For P1 (what is found is in his ideas, not in the filter), P4 (principles are
            found, not brought)
Status:     current, in prompts/find_principles_v1.md, scripts/find_principles.py,
            scripts/match_principles.py, scripts/compare_principles.py and record/controls/README.md

D-2026-10-09-d  The principles are validated against real decisions mined from the Claude Code
                transcripts, by the plan record/plan-principles-validation-2026-10-09-decisions.md
                (draft 1) as Luciano marked it: D2, D3 and D5 to D14 as written; D1 qualified, a
                principle counts from its explicit formulation, when that formulation's logical
                structure is enough to make decisions; D4 replaced, each principle is reported with
                its number of cases and its figures, without thresholds or labels.
Author:     Luciano, on the model's plan revised after GPT's review
Quote:      "explicit formulation, if its logical structure is enough to make decisions"
            "porque vestir un numero entendible con umbrales arbitrarios? Dejemos el numero y listo."
Source:     luthier@94cb3e1:record/plan-principles-validation-2026-10-09-decisions.md:50
            luthier@94cb3e1:record/plan-principles-validation-2026-10-09-decisions.md:81
Kind:       method. For P13 (a principle is worth the decisions it guides, now measured), P1 (the
            cases enter only with his approval), P11 (every threshold the plan keeps is a parameter)
Status:     current; step 0 waits for Luciano (iachat ingest claude-code)

D-2026-10-09-e  The synthesis of Luthier's ideas, rules and principles (map of themes and states,
                candidate principles set against those in force, rules traced to the ideas) and the
                validation of the candidates with a cutoff are carried out overnight by the model,
                by record/plan-synthesis-2026-10-09.md, which Luciano approved whole; for this plan
                the model may run the scripts that process the record. The review of cases and the
                scoring stay his.
Author:     Luciano
Quote:      "SI apruebo todo el plan escribilo por si te quedas sin memoria e implementalo durante
            toda la noche, te doy libertad de correr scripts."
Source:     chat:8c2cb06b:2902
Kind:       method. For P12 (the work reaches him synthesized), P8 (no step he must wait for at
            night); against the working rule that he runs the scripts processing the record, set
            aside here by his word for this plan
Status:     current

D-2026-10-10-a  The pipeline that finds candidate principles is measured against a naive agent:
                every idea of the timeline, the question "what are the rules and principles of
                this language?", nothing more; on the controls of Python and Haskell, judged as
                before, and on Luthier, judged against the pipeline's ten candidates and P1 to P14.
                The model runs the scripts for this comparison.
Author:     Luciano for the hypothesis and the leave to run; the model for the measure
Quote:      "Quizas darle todas las ideas a un agente naive y pedirle que extraiga de ahi las
            reglas y principios sea mejor que esta arquitectura elaborada y pretendidamente
            precisa?"
            "Si correlo ahora"
Source:     chat (session of 2026-10-10)
Kind:       method. For P8 (no more bureaucracy than it pays for: the pipeline's steps must earn
            their place); against the working rule that he runs the scripts processing the
            record, set aside here by his word for this comparison
Status:     current, in record/controls/README.md (the naive run)

D-2026-10-10-b  The principles of the language and the way of working get a presentation document,
                docs/principles.md, drafted from the synthesis, the cutoff run, the naive runs and
                the five web answers, to be worked with Luciano in another thread; and the days of
                synthesis and validation close with a conclusions document in the record.
Author:     Luciano
Quote:      "Quiero que entonces ahora hagamos un documento ya en docs con los principios y la
            forma de trabajar. Vamos a trabajar en otro hilo sobre este documento."
Source:     chat (session of 2026-10-10)
Kind:       rule. For P12 (what reaches him is synthesized); docs/ presents Luthier, record/ holds
            how it came to be (D-2026-10-07-a)
Status:     current: docs/principles.md draft 0 (unapproved), record/conclusions-2026-10-10.md

D-2026-10-10-c  A definition has no effects. Its result depends only on its inputs; effects live
                only in the actions (print, save). A mutable parameter written as two variables,
                before and after, is not an effect: the dependence is an edge of the graph. What is
                forbidden is what the graph does not show.
Author:     Luciano
Quote:      "lo que si es no-side effects"
Source:     chat (session of 2026-10-10, on the audios of 2026-10-10)
Kind:       principle of the language, candidate for docs/principles.md. For L9 (a program is a
            DAG), L12 (execution is the verification of equivalences); it is the one assumption
            under which every evaluation strategy gives the same result
Status:     current

D-2026-10-10-d  Forward on demand: the evaluation strategy is a parameter separate from the
                program (P11). By default: a plan backward from the actions over names, evaluating
                nothing (a branch whose use depends on a value marks both branches live); then a
                strict forward run over the live subgraph, in topological order, each node once and
                whole. Three conditions it rests on: (i) errors and holes are values that flow,
                so a live-but-unused branch cannot abort the run; (ii) results are memoized in a
                store keyed by the hash of (code, inputs, mode), the retention policy a parameter;
                (iii) the tests are actions, so "verify everything" is asking for all tests and
                "verify on demand" is asking for the tests of what an action uses (L3). Named by
                Luciano "forward por demanda"; mechanism "retro-forward"; not Haskell's laziness,
                which is per expression and interleaved with the run.
Author:     Luciano for the scheme and the name; the model for the three conditions, accepted
Quote:      "1) cargas el arbol de definiciones 2) detectas los 'print' 3) corres para atras desde
            el print hasta la base, pero no ramifico (no genero 3 f, solo detecto nombres)
            4) calculo los caminos detectados forward."
            "Lo ideal es no elegir, es decir, poder expresar todo, solo elegir lo que va por
            default."
            "si, dale."
Source:     chat (session of 2026-10-10); record/audios/WhatsApp Ptt 2026-10-10 at 11.42.15.md
            (60a10aa, 01:51 to 04:07, backward and forward "las dos tienen un rol"); 11.11.22.md
            (60a10aa, 00:00, "la Lazy Evaluation sería la mejor manera de definir qué es lo que
            quiero exactamente definir")
Kind:       implementation decision. For P11 (every criterion is a parameter), L7 (the core is
            executable by hand: the plan is readable node by node), L9, L13 (forgetting: the last
            consumer of a node is known from the plan). Prior art: topological schedulers of build
            systems (Make, Bazel; Mokhov, Mitchell, Peyton Jones 2018), magic sets, Halide's
            algorithm/schedule split
Status:     current; the strategy parameter has its place from the start and only the default is
            implemented (P8)

D-2026-10-10-e  Mutable parameters are two variables, before and after, in the core (x1 = f(x0));
                in-place mutation is an optimization the planner applies when x0 has no other
                consumer after f, the same last-consumer analysis that frees nodes. The form f(x)
                that mutates is library, translated to the two names. A uniqueness or linearity
                annotation on the type (a guarantee of no copy) is foreseen, not implemented.
Author:     Luciano for the model of two variables; the model for the planner's criterion and
            the annotation, accepted
Quote:      "Los parametros mutables son una optimizacion importante y se pueden modelar como dos
            variables (antes y despues), que es como se modela un incremento con una funcion
            pura."
Source:     chat (session of 2026-10-10)
Kind:       implementation decision. For D-2026-10-10-c, L7 (both names explicit in the core),
            L2 (uniqueness as a proposition on the type). Prior art: SSA, Fortran intent(inout),
            LAPACK's overwrite of A, Clean's uniqueness types, Perceus (Reinking, Xie, de Moura,
            Leijen 2021)
Status:     current

D-2026-10-10-f  Decorations (value with error, derivative, test, any monad) are chosen backward
                and propagated forward: the fourth condition of D-2026-10-10-d. The action names
                the mode ("print de la derivada de y respecto de x"); the plan marks each live
                node with its mode; the run interprets the same DAG under that mode (L6, code is
                data) and the decorated values flow forward. At the leaves one of three: the leaf
                lifts on its own (a constant has error zero and derivative zero); the leaf takes
                an explicit mark given with the demand (the variable differentiated against, the
                uncertainty of a measurement); or the leaf cannot supply what the mode asks and
                is a hole (L8), found at planning, before anything is computed. The derivative is
                the one decoration with two propagation modes, forward (dual numbers) and reverse
                (the tape); the choice is by cost, a parameter (P11), default by shape (forward
                for few inputs, reverse for few outputs).
Author:     Luciano for the scheme and the question; the model for the three cases at the leaves
            and the derivative's exception, accepted
Quote:      "Cuando vos demandás, demandás con tus condiciones."
            "si estas decoraciones son forward o backward, y acá estoy un poquito en la duda de
            cuál de las dos sería mejor"
            "Si"
Source:     record/audios/WhatsApp Ptt 2026-10-10 at 16.49.14.md (8a4c70f, 03:20 to 07:06); chat
            (session of 2026-10-10)
Kind:       implementation decision. For D-2026-10-10-d (the memo key already carries the mode),
            L6, L8, P11. Prior art: tagless final interpreters, JAX's transformations (grad as a
            reinterpretation of the traced program), forward and reverse mode AD; his own
            Transfer_Op_to in C++ is the forward version
Status:     current

D-2026-10-10-g  Code is universal over the models of the theories it requires. A function is
                parametrized by theories (Real, Field, LinearAlgebra), not by single functions;
                the model is resolved implicitly from the scope and can be passed explicitly.
                Modules are values: a parametrized module is a function from models to records
                of definitions, applicative because definitions have no effects (D-2026-10-10-c),
                instantiated on demand with the parameter threaded down from the action, so C
                calls A(Field) and B(Field) with the one Field. A specialization (overload) is one
                more representative of the law's class, valid on a subtype, chosen by cost with
                "most specific" as one parametrized criterion (P11), and certified against the
                same law as the generic one. Overloads are the only source of mismatch between
                representations; there the orchestrator inserts bridges (conversions, L14) by
                cost, under three conditions: two bridge paths agree up to the law (a commuting
                diagram, checked); a bridge carries its error in the certificate (L11); the
                bridges inserted appear in the plan (L7). Edges of the DAG are by operation used,
                the signature by theory.
Author:     Luciano for the parametrization by theory, overloading, modules parametrized and
            instantiated on demand, bridges by the orchestrator; the model for the three
            conditions on bridges and the two levels of granularity, accepted
Quote:      "el codigo seria, en principio universal a los valores de funciones que cumplan las
            leyes requeridas, por lo que la opcion de parametrizar todo suena saludable. Y uno
            parameterizaria a nivel de aReal o LinearAlgebra"
            "si no lo son, bueno se especifican como en C++ por overloading?"
            "los modulos (o librerias, no se como llamarlo) tambien estaria parameterizados"
            "C llama a A (FieldA) y B(FieldA). Y sino habria que hacer puentes automagicos de una
            representacion a la otra. Igual esto estaria manejado por el orquetador que buscaria
            lo mas eficiente."
Source:     chat (session of 2026-10-10); record/audios/WhatsApp Ptt 2026-10-10 at 17.00.40.md
            (76ba165, the question "cómo se hace normalmente")
Kind:       implementation decision. For L6 (modules as values), L10 (the quotient: overloads and
            bridged specializations as representatives of one class), L14, L7, P11, L8 (a module
            with an unfilled parameter is a module with a hole). Prior art: ML functors and 1ML
            (Rossberg 2015), Stepanov's concepts, typeclasses and modular implicits, Backpack,
            Julia's promotion rules; Reynolds' parametricity as the ground of universality
Status:     current

D-2026-10-10-h  Return-type polymorphism by demand. A function may have several certified
                codomains (sin into Real, into [-1, 1]); the type the consumer requires flows
                backward along the plan, as decorations do (D-2026-10-10-f), and selects which
                certificate of the codomain is demanded. The narrower codomain is the same
                function with a theorem attached (L4), so asking for it has the cost of its
                certificate. When no consumer fixes the type, a default applies, a parameter
                (P11); without a default the demand is a hole (L8), found at planning.
Author:     Luciano for the polymorphism and its ground in execution on demand; the model for
            its reading as bidirectional typing and the quotient, and for default and hole,
            accepted
Quote:      "Una función podría tener multiplicidad de tipos de salida y que el tipo de salida
            queda definido por el tipo de entrada que es requerido ... habría un polimorfismo en
            las funciones y un polimorfismo en la función de retorno. Fíjate vos que eso lo podés
            hacer si vos haces ejecución en demanda."
            "Si"
Source:     record/audios/WhatsApp Ptt 2026-10-10 at 17.25.23.md (7b0481d, 05:49 to 07:53); chat
            (session of 2026-10-10)
Kind:       implementation decision. For D-2026-10-10-d and f, L4, L8, P11. Prior art:
            bidirectional typing (Pierce and Turner 2000; Dunfield and Krishnaswami 2021),
            Haskell's return-type polymorphism (read, mempty) and its defaulting rules
Status:     current

D-2026-10-10-i  A first use case: absorb an existing library into Luthier by writing its
                theoretical module (types, functions, laws, no values) and certifying the
                existing implementation against it (L14). The first candidate is tidyverse's
                pivot_wider and pivot_longer: the law "one is the inverse of the other" fails in
                general (row order, column types), and writing it forces saying up to which
                equality it holds (L16). A failing law is the finding: the conditions under
                which it holds are the reasons of the library's design ("obliga a ver porque
                eligio lo que eligio"), not a verdict on it.
Author:     Luciano
Quote:      "el primer trabajo que podría hacer Luthier es agarrar y decirle a la IA, bueno,
            ahora vos agarrame toda esta librería de Python ... y que ponga, digamos, en el
            lenguaje de Luthier todas las leyes que cumplen todas las funciones"
            "vos podés hacer pivot wide y pivot long, creo, en R, en tidyverse. y una no es la
            inversa de la otra y tendrían que ser una inversa de la otra"
            "lo de pivot_wide puede ser una buen caso de uso, no?"
Source:     record/audios/WhatsApp Ptt 2026-10-10 at 17.25.23.md (7b0481d, 01:44 to 03:45); chat
            (session of 2026-10-10)
Kind:       objective, candidate for record/objectives.md (which is his to mark). For O1 (be
            useful now), O3 (make what others wrote legible), O4 (several implementations,
            tested equivalent), L14, L16; a real case before any mechanism (P8), and one that
            exercises bridges (R and Python representations of one table)
Status:     current; not started

D-2026-10-10-j  docs/principles.md goes to draft 1 in this thread, from the nine voice notes of
                2026-10-10 and D-2026-10-10-c to i, before the timeline carries the day's rows
                (notes cited by file and minute until then). L18, L19, L20 and W14 new; L4, L5,
                L8, L9, L10, L11, L13, L14 retouched; draft 0 kept at 6d9dbd3.
Author:     Luciano
Quote:      "Bueno, con todo esto edita el documento en doc"
Source:     chat (session of 2026-10-10)
Kind:       rule. For P3 (the best reading in front, the original in git), P12; amends
            D-2026-10-10-b (the document was to be worked in another thread)
Status:     current: docs/principles.md draft 1 (5769005), unapproved


D-2026-10-11-a  smartMaybe: a predicate is written once, in its explaining form (the failures
                it finds), and the poorer forms (the first failure, Maybe, Bool) are its
                forgetful projections, chosen by the demand. Laws too return the explaining
                form. The demand asks for the first n failures or for all of them, as a
                compiler's error limit; Bool is the first failure, forgotten. Inverts the
                primacy of 05 §9 (Checks), where Bool is primary and the explaining forms are
                written apart and tied by a law (firstViolation and ReportsValidity).
Author:     Luciano
Quote:      "Yo quisiera un smartMaybe que de acuerdo a la demanda sea o un Maybe comun o un
            maybeError" (note); "Si, vamos con smartMaybe. Y la idea es que podes pedir
            n-fallas o completo (como un compilador, no?)" (chat)
Source:     record/Lucianos ideas/El problema de las tipos recursivos.txt (ba108aa); chat
            (session of 2026-10-11); analysis in record/recursive-types-and-objects-2026-10-11.md
            §4 and §5
Kind:       language design. For L13 (forgetting is determined by the demand), L19 (the demand
            determines the computation), P11 (n is a parameter of the demand). Cost: not of an
            explaining form explains only as much as its success side carries
Status:     current; spec amended (05 §9, 04 §3); not implemented; stopping the fold at n failures is open

D-2026-10-11-b  An if without else is a guarded value: `if c then a` is `if c then just a else
                nothing` when c is a Bool, and `ok a` or `failed` with the first failure when c
                is a Failures E (D-2026-10-11-a), which a demand for Maybe forgets. Without
                effects (L18) a branch that does nothing has no meaning, so this is the only
                reading; a forgotten else is caught by the type checker (a Maybe where a value
                was expected). An else belongs to the nearest if without one. Precedent: Rust
                bool::then, Scala Option.when.
Author:     Luciano
Quote:      "monoide (T:U) (op:T->T->T ) -> Maybe monoide := if (leyesdeMonoide T op ->
            monoide{T op}" (note); "acepto eso, entonces." (chat)
Source:     record/Lucianos ideas/El problema de las tipos recursivos.txt (0cbe437); chat
            (session of 2026-10-11); record/recursive-types-and-objects-2026-10-11.md §3
Kind:       language design, grammar. For L18 (a definition has no effects), P8 (no more
            bureaucracy than it pays for). Sugar only: no kernel construct added
Status:     current; spec amended (02 §3, 04 §5); not implemented

D-2026-10-11-c  `:=` defines a name once; `<-` binds and rebinds. Each `<-` is a fresh name in the
                core (SSA, D-2026-10-10-e) and later uses mean the latest; a name bound with :=
                cannot be rebound. `<-` needs order: allowed in blocks, defaults and named
                arguments, an error at the top level of a file. Default arguments are written
                `(tol : T <- d)` and called by name `f a (tol <- v)`; defaults are filled once
                every parameter without a default is given; they belong to the definition, not
                the type; the elaborated call carries every value. `<-` is one token, so a
                comparison with a negative number needs a space.
Author:     Luciano for `<-` as the operator of rebinding and of defaults, and for default
            arguments in the Python style; Claude for the type before the default, the filling
            rule and the restriction to ordered places, accepted
Quote:      "default arguments y como indicarlos y llamarlos ... (arg<-value:T) ... F (arg<-value)"
            (note); "si es inmutable --> error, si es mutable --> pasa"; "por eso yo queria
            introducir <-"; "Si, me parece que es un buen avance" (chat)
Source:     record/Lucianos ideas/python style.txt (c3c63d9); chat (session of 2026-10-11);
            record/default-arguments-2026-10-11.md
Kind:       language design, grammar. For P11 (every criterion is a parameter: defaults make it
            livable), P2 (the elaborated call records every parameter), L18 (no effects: no
            mutable default shared between calls). Partly answers the open item on implicit
            arguments (05 §10)
Status:     current; spec amended (02 §1, §2, §3, §8; 04 §5; 05 R12); not implemented; the syntax
            of blocks is still open

D-2026-10-11-d  Laws accumulate; a function need not be characterized. A law may only constrain
                (a subtype of A → B with many inhabitants); a set of laws that determines the
                function up to its equality (the definite description, "à la Russell") is the
                limit a definition may reach, never what it must reach. Requiring it of every
                function would forbid adding laws one at a time, and that is against being
                expressive (organizer E). The implementation of an under-determined function is
                a free choice among the inhabitants (P5), certified against the laws it has.
Author:     Luciano
Quote:      "si es a lo Russell para toda funcion no puedo contruir leyes acumulativamente, y eso
            va en contra de ser expresivo" (chat)
Source:     record/Lucianos ideas/principios organizadores.txt (fa3f972, 1c7a284); chat (session
            of 2026-10-11); record/organizing-principles-2026-10-11.md §5
Kind:       language design, semantics of laws. For E (expressive over restrictive) and P5 (a
            free choice is legitimate); bounds C's "properties that determine the function
            univocally" to the limit case; consistent with L4, L5 as drafted
Clarified:  "à la Russell" in the note does not mean uniqueness; it means definition by
            description, from outside, as against constructive definition by a term: "no ser a lo
            tarski (constructivo) sino a lo matematico (desde afuera, como un entomologo observa
            un bicho)" (chat). The model's reading: Russell's knowledge by description against
            knowledge by acquaintance; a function is known by the properties observed of it, and
            the implementation, native or extern, is the specimen. The accumulation of laws
            stands as decided above. Correction from the audio of 08.58 (45df807, 32:01 to
            34:07): by "Tarski" he means the compositional derivation of a property from the
            properties of the parts (the sum of two normals is normal), not constructivism;
            Luthier wants both routes, derived and observed, and the demand chooses which
            invariances are produced.
Status:     current; settles the first of the two open items of the analysis of 2026-10-11; W5
            (native against extern) still open

D-2026-10-11-e  docs/principles.md is rewritten from Luciano's organizers: three tiers in his
                words (the guide, type theory; two eurekas, the demand and the function type as
                its laws; principles of good use, cost and expressive), the twenty L derived
                under them with numbers kept, L21 candidate, W5 restated as bootstrapping. The
                plan's D1 to D8 are taken as recommended on his instruction to write the file;
                every formulation and derivation stays *Proposed* until his marks. Steps 1 to 4
                of the execution collapse into the one file (derivations inline, P13 check in
                the header); step 5 (the rationale of cost-valued laws) remains.
Author:     Luciano for the organizers, the tiers and the instruction; Claude for the
            formulations, derivations and the collapse of the steps
Quote:      "mi idea ahora es tener un archivo de principios actualizado asi lo veo yo" (chat);
            "la guía es la te[o]ría de tipos ... los tipos de funciones son las leyes que las
            definen. Esa fue mi eureka moment ... la demanda de un valor por el mundo externo me
            define todos los tipos necesarios ... Después son sí principios de buen uso" (audio
            09.19)
Source:     record/plan-principles-generative-2026-10-11-decisions.md (f4cb0d6);
            record/organizing-principles-2026-10-11.md (384fc5f); docs/principles.md draft 2
            (cd24137)
Kind:       method, record of the principles. For P1 (his quotes first, the model's text marked),
            P3 (draft 1 kept in git, the best reading in front), P13 (the check of decisions
            guided per organizer), W14 (five organizers instead of thirty-four peers)
Status:     current; draft 2 unapproved, awaiting his marks

D-2026-10-11-f  A function known correct by a theorem outside Luthier is certified `proved` by
                citation: the citation is recorded in the certificate, the grade is `proved`,
                allowed in user code (unlike `axiom`, whose grade `assumed` records nothing). The
                certificate of a law travels to another implementation by a certificate of
                identity: exactly where the identity law is boolean (`==` structural, 05 R8),
                with the observed distance added where it is a cost (G3); the type of the
                identity law's result (Bool or Cost) says which. Proposed syntax `cite name
                "..."`, a directive next to `test`.
Author:     Luciano for the idea (axiom for a known-correct implementation, verified by bitwise
            identity) and the yes; Claude for `proved` by citation instead of `axiom`, the
            condition on floats and the syntax
Quote:      "cuando sabemos por ejemplo que una implementacion es correcta por teorema matematico
            conocido (esto seria algo que requeriria una palabra clave nueva, quizas axiom ?) y
            luego por identidad bitwise con valores conocidos se verifica una implementacion
            externa"; "Si, desde ya" (annotations, 2c18c41, 18da042)
Source:     record/answers-annotations-principles-2026-10-11.md §11, §4; -b.md §11
Kind:       language design, certification (05 §7). For G2 (description), L21, L11; distinguishes
            assumed (no justification) from proved (a citation to check)
Amended:    (same day, his feedback at 9d65118) the citation is a key into a .bib whose entry
            carries a DOI, ISBN or URL resolved by record/bibliography/checkdoi.py; the
            certificate records who checked the correspondence: human, ai+human, or none.
            Proposed syntax `cite name bibkey checked ai+human`. Amended again (c167022): the
            citation is a value of a type Reference (key, doi, isbn, url, sha256, law
            Resolvable), read from a .bib as a module (`biblio.kantorovich1948`), and the
            certificate records its identifiers and hash.
Status:     current; spec amendment to 05 §7 pending; syntax `cite` open to his preference

D-2026-10-11-g  W15 enters docs/principles.md: a long analysis is reported as such, as a delicate
                question or as a conflict between principles, and goes to Luciano as one question.
                P15 proposed in his words for record/principles.md: adherence to the principles
                must be cheap to compute; what is cheap is found as the work goes.
Author:     Luciano for the distinction and the principle; Claude for the trigger (the same
            decision revisited twice without new evidence, or more than one screen)
Quote:      "mi engagement va a ser mejor cuando mi capacidad cognitiva es usada para el
            desarrollo optimo del proyecto ... deadlocks ... legitimos ... o ilegitimos"; "agree. I
            think that making the principle adherance manageable to calculate is key and should
            be a guiding principle. what is manageable is something to be discovered"
Source:     docs/principles.md annotations (2c18c41, 18da042); record/answers-...-b.md §15
Kind:       method. For P12 (his attention is the scarce resource), P4, P13; a rule of behaviour,
            no recurring mechanism
Status:     current; W15 in draft 3; P15 awaiting his mark on the wording

D-2026-10-11-h  Mutation testing enters W6 as a check to implement: `luthier test --mutate` alters
                an implementation (a constant, an operator, a branch) and reports every law that
                still passes; a law that no mutation fails is reported as not diagnostic. Added
                before a case it would have caught, on Luciano's instruction, which overrides the
                rule of CLAUDE.md for this one mechanism.
Author:     Luciano
Quote:      "Mutation test es un principio o working trait que deberia ser implementado, buena
            sugerencia." (9d65118)
Source:     record/answers-annotations-principles-2026-10-11-c.md
Kind:       method, testing. For W6 (a test must fail when the thing is wrong), G2 (the power of a
            description is measured on specimens that differ)
Status:     current; not implemented

D-2026-10-11-i  Blocks. A brace term whose last item is a bare expression is a block, its value
                that expression; without a final expression it is a record value. Items: `x := t`
                once, `x <- t` bind or rebind, an action with its result bound. Each item becomes a
                definition with a fresh name (SSA, 04 §5, 05 R12), after which dependencies give
                the only order. A name is visible from its binding to the end of its block and in
                nested blocks; `:=` of a name defined in an enclosing scope is an error, not a
                shadowing; `<-` rebinds only block-local `<-` names and the parameters of the
                enclosing definition. Actions take and return the world, `w1 <- print w0 "x"`, so
                their order is the dependency through `w`. Three kinds of block: the body of a
                definition or lambda, `main` in a file, the session; a file is never a block. A
                rebinding whose previous binding has no consumer is an error in a file and
                allowed in a session.
Author:     Luciano for the demand (blocks, boundaries, scopes; the dead-rebinding question) and
            the acceptance; Claude for the rules
Quote:      "Lo cual nos introduce al concepto de bloques. Y ahi te pido ayuda."; "tenemos que
            definir las boundaries para los blocks y los name scopes."; "Si" (c167022, read as
            accepting the two pending decisions)
Source:     record/answers-annotations-principles-2026-10-11-c.md (blocks), -d.md
Kind:       language design, grammar and static semantics (02 §3, §8; 04 §5; 05 R12). For L9 (the
            DAG is the only order), L12 draft 3 (actions verified before and after), L13, G1, G4;
            resolves the open collision of block and record syntax (02 §8)
Status:     current; spec amendment pending; not implemented

D-2026-10-11-j  Operators are resolved by the type, and a type names its model: `i : Int` has the
                ring of Int, `j : Z7` has ringZ7; a carrier with two models is two types, with
                explicit conversion (forget and a constructor); operators of a wider model apply
                to a narrower type only through a homomorphism stated and certified as a law.
                Where a theory does not fix the operator's role (a function over Monoid on Int,
                which carries two), the model is named. The scope rule proposed in the second
                round is withdrawn.
Author:     Luciano for the principle (a value belongs to a type of a model, whose operators it
            uses; laws must coincide across models) and the acceptance; Claude for the two-types
            rule and the homomorphism condition
Quote:      "un valor pertenece a un tipo de un modelo, y ese modelo tiene sus operadores. Claro
            que podrias tener operadores para modelos mas amplios, pero ahi entiendo que deberia
            haber coincidencia de leyes" (9d65118); "Si" (c167022)
Source:     record/answers-annotations-principles-2026-10-11-c.md (operators and models)
Kind:       language design, static semantics (02 §3 operator directive; 05 §10 implicit
            arguments). For G0 (the type is the proposition "member of this model"), G2, L13, L20
            draft 3; examples/z7ring.lut to be rewritten (Z7 as a quotient, not a subtype)
Status:     current; spec amendment pending; not implemented

D-2026-10-11-k  Separators are Python-like in blocks and record values: a line break separates
                items and `;` is equivalent to it; inside parentheses, brackets, `< >` and the
                braces of `match`, line breaks are ignored as before. The braces of a lambda stop
                ignoring line breaks, since a lambda body is a block.
Author:     Claude, proposed; Luciano, accepted ("Si a todo")
Quote:      "aca cabe la pregunta somos C (siempre ;) o somos Python (supongo que ; es
            equivalente a line break)" (c167022)
Source:     record/answers-annotations-principles-2026-10-11-d.md
Kind:       grammar (02 §1). For G4 (nothing gained by a mandatory `;`)
Status:     current; spec amended; not implemented

D-2026-10-11-l  The laws of relations and actions (Reflexive, Symmetric, Antisymmetric,
                Transitive, Total, Associative, the identities, inverses, commutativity,
                distributivity, homomorphism) move from lib/algebra.lut to lib/laws.lut;
                algebra.lut imports it and keeps the structures (Setoid, Monoid, Group, Ring,
                Field and their instances). No change of meaning.
Author:     Luciano for the question; Claude for the split and the name; accepted ("Si a todo")
Quote:      "ahora las leyes de asociatividad, simetria etc deberian definirse en un modulos laws
            o algebra o un nombre mejor?" (c167022)
Source:     record/answers-annotations-principles-2026-10-11-d.md
Kind:       libraries (03). For G2 (laws come first, stated once over the signature they need)
Status:     current; to be done in this session
