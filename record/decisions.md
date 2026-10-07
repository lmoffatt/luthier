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
