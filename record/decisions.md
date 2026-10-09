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
