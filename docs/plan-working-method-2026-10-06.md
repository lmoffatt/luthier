# Plan: putting the working method into practice, 2026-10-06

Draft 2, 2026-10-06. Status: twelve bites wait for Luciano's answer; phase 0 is done; the steps that
wait for nothing can start.

Written for Luciano. It holds only what needs his answer. The steps themselves, with their inputs and
the test that says each one is done, are in `docs/plan-working-method-execution-2026-10-06.md`,
written for the sessions that carry them out.

Sources:

- Draft 1 of this plan, `32f82a7`. Luciano's annotations on draft 0, `daa5b95`, cited as
  "annotation on the plan, line n".
- The working method, `docs/working-method.md` at `ed8052a`, cited by section number and title.
  Luciano's annotations on its draft 0, `2a660c8`, cited as "annotation on the method, line n".
- Two Claude Code sessions, cited as "chat 7217f251, line n" and "chat 8d5ce152, line n": the line of
  the transcript in `~/.claude/projects/-home-lmoffatt-Projects-luthier/`. The files only grow, so
  the lines are stable.

What changed from draft 1:

- Draft 1 was two documents in one. Luciano asked to split it ("hace la separacion", chat 8d5ce152,
  line 140). This one keeps the decisions. The execution plan keeps the steps, the measurements, and
  Appendix A (the fidelity audit done by hand), which is now the calibration for the automated one.
- Draft 1 asked for thirteen principles in one item, the mistake its own section 1 found in draft 0.
  Here they come in four bites.
- Phase 1 no longer waits for the marks. An entry Luciano hasn't marked goes into the record as
  `proposed`, which is what it is anyway, and his mark changes it later in one commit.
- A review of draft 1 (chat 8d5ce152, the reply to line 3) found three defects that would stop a
  session. The execution plan fixes them; two of the fixes set formats, so they are bite 2 here.
- Luciano's observations on code have a place of their own, outside the code (decision
  D-2026-10-06-p in the appendix).

## How to answer

Write under each bite `ok`, `no`, or a correction, as with draft 0. A bite says what is decided, what
it implies beyond its own place, what it costs, how it is undone, and which steps wait for it. Bites
1 to 4 unblock steps. Bites 5 to 9 are about the record and can wait. Bites 10 to 12 can wait longer.

## 1. What a step is

Luciano's criterion (annotation on the plan, line 37): "La limitante aqui es mi capacidad de
procesamiento de informacion, de modo que una step deberia ser un bocado de decision que yo pueda
manejar y que tenga implicancias mas que locales." He asked whether it is a good criterion.

It is, and it separates two units that draft 0 confused. The unit of review is what reaches him: a
bite of decision. The unit of reversal is a commit (working method §8, reversibility). A step may take
several commits; a commit never spans two steps. Each half of the criterion needs a test that someone
other than him can apply.

"A bite I can handle." One question he can answer with ok, no, or a correction, after reading at
most a screen: what is decided, what it implies beyond its own place, what it costs, how it is
undone. If it needs more than that, it is split.

"Implications more than local." A decision is local when one commit undoes it and nothing else
depends on it yet. It is not local when any of these hold: it touches a principle; it sets a format
or a rule that others will follow (a record format, `CLAUDE.md`, the specification); it is expensive
to undo (data, recertification); or it exposes something (a push to a public repository). Local
decisions are the model's margin (working method §6, decisions) and reach Luciano only in the report
at the end of a task. The rest are his bites.

The risk the criterion leaves open: many local decisions can add up to a change that is not local,
and none of them would have reached him. The principles audit (bite 4) looks for that drift.

The criterion is a principle in its own right, P12 (Luciano's attention is the scarce resource), in
bite 9.

## Bite 1. Chat exports in a public repository

Already decided: the chat exports go to GitHub, because they are "the ultimate proof (the audios) of
the ideas origin" (D-2026-10-06-k, chat 7217f251, line 366).

What it implies: `lmoffatt/luthier` is public, so an export is published at the next push of `main`,
and a publication can't be undone (working method §8, reversibility). An export carries both sides
of every turn, his and the model's, and what he pasted.

Proposal:

- You skim each export before committing it. You run the script anyway, so the file is in front of
  you. The script lists first the turns that mention a word from a short list of private matters
  (databaum, acuerdo, propiedad intelectual, patente), so those are what you read.
- A session that touches sonolocalización's private matters is exported into the private
  sonolocalización repository, never into luthier.

Cost: a few minutes per export. Undo: one commit, until the push. Waits for it: committing the first
export (step 1.1). Writing the script doesn't wait.

## Bite 2. How the record is tied to git

Two formats, each needed by a step.

**(a) Commits name their decision.** Step 2.2 (a reminder, when the model stops, of the commits that
no decision names) was confirmed ("ok", annotation on the plan, line 174), but as written it can't be
built. An entry of the log points to the quote that supports it, not to the commit that carries it
out, and git doesn't know which commits belong to a session.

Proposal: every commit that touches the specification or the implementation ends with a line
`Decision: D-2026-10-06-k` (the entry it carries out) or `Decision: none`. A hook at the start of a
session notes where `HEAD` was. The reminder lists the commits since then that have neither line.

A correction to what you confirmed: a reminder that only prints, without blocking, isn't read by the
model, since Claude Code shows that output only in its detailed transcript view. For the model to
read it, the hook holds the turn once, with the list, and lets it end at the second try. The hook of
`plan-mechanical-rules` that runs the fast lints does the same.

**(b) One way to write a source.** Draft 1 wrote sources in five ways, one of them with an ellipsis
that no script can read. Proposal, one source per line:

- in a repository: `luthier@2a660c8:docs/working-method.md:74`, or `:60-61` for a range;
- in a chat: `chat:7217f251:196`, the line of the transcript, read through its export.

Implies: one more line in each commit message on the specification or the implementation, written by
the model. With it, the reminder (step 2.2) and the check of quotes (step 4.1) are scripts. Cost:
seconds per commit. Undo: one commit for the hook; old messages stay as they are. Waits for it: steps
2.2 and 4.1. Steps 1.2 and 1.3 are written in this grammar now and rewritten in one commit if you
change it.

## Bite 3. The content of `CLAUDE.md` (step 2.1)

Already decided: `CLAUDE.md` is a living document of operative rules, with no meta-information
(D-2026-10-06-n, annotation on the plan, line 163). One rule per line. Where each line comes from is
in the decision log, and changing a line is a logged decision. The principles appear by statement
only.

Draft, for both repositories (in sonolocalización, next to the lines that `plan-mechanical-rules`
step 6.2 adds):

```
# Working rules

- Luciano's notes, transcripts, annotations and observations are never edited. A correction keeps
  the original in git and puts the corrected version in front, with a note at its top.
- His observations on code are in `docs/Lucianos observations/` in luthier and in
  `Lucianos feedbacks/` in sonolocalización. Read the ones on a file before changing it.
- In a document you write, mark what comes from a source (cite it) and what you propose.
- Everything derived records its inputs (by commit or hash), the script or prompt with its
  version, every parameter, and the seed.
- Commit before every change. One decision, one commit. A commit that touches the specification
  or the implementation ends with `Decision: <id>` or `Decision: none`.
- A decision is yours when one commit undoes it and nothing depends on it yet. Otherwise it goes
  to Luciano as one question he can answer after reading a screen.
- Before a decision that isn't routine, say in one line which principles it touches, in which
  direction, and what it assumes.
- At the end of each task, list the decisions you took on your own.
- Commit a document before Luciano annotates it; his annotations are the diff.
- In anything Luciano reads, a numbered reference carries its statement: "P6 (every change can be
  undone)". Records (decisions.md, principles.md) may be terse.
- Written material is in English; chat with Luciano is in Spanish.
- Luciano runs scripts that process data or the record of the project. Lints, luthier check and
  luthier certify you may run.

## Principles in force

- The mathematical object that best represents a concept is the invariant of its type.
- Every criterion is a parameter, never a constant in the code.
```

The line on `Decision:` enters with bite 2, and "one decision, one commit" with bite 10. The list of
principles grows as you mark bites 6 to 9.

Cost: about twenty lines read at the start of every session. Undo: one commit. Waits for it: step
2.1.

## Bite 4. When the principles audit runs (step 5.2)

Already decided: the audit asks your three questions (whether the principles are followed and used,
whether they conflict, whether new ones appear and at what cost) and a script runs it
(D-2026-10-06-o). Open: "cada tanto".

Proposal: before each push of `main`, and whenever you ask. A hook before the push doesn't run the
audit, since the audit processes the record and is yours to run; it prints the date of the last audit
and the number of commits since, and lets the push go on.

A calendar would spend tokens whether or not anyone reads the output, against P8 (no more
bureaucracy than it pays for) and P12 (Luciano's attention is the scarce resource). Before a push you
read anyway.

Cost: one run per push, a few minutes of a model and the reading of its output. Undo: delete the
hook. Waits for it: the hook of step 5.2. The script doesn't wait.

## Bite 5. Is a checked quote enough to confirm a decision of yours?

An open question of working method §13. Eleven entries of the log are your words with a quote (b, d,
e, f, g, k, l, m, n, o, p in the appendix). If a quote that the script of step 4.1 finds at its line
is enough, they stand as `current` without your reading them. If not, you read the appendix, about
175 lines.

What the check can't see: the first line of each entry, the statement, is the model's summary of your
quote. The quote proves you said it; it doesn't prove the summary says the same. That comparison is
the job of the fidelity audit (step 5.1).

Proposal: yes. A checked quote confirms; the statements go through the fidelity audit. Undo: a change
of status, one commit.

## Bite 6. Principles: your part and the chain of derivation

Mark each one. What you don't mark stays `proposed`.

```
P1  Luciano's part stays discernible.
Quote:      "the idea of course is that this project is generated by a human and the human
            signature has to be distinctive (discernible), otherwise it is just IA generated
            content with not particular value, but as such."
Source:     luthier@2a660c8:docs/working-method.md:74
Assumption: the value of the project lies in what he contributes, and that part can be told
            apart at a cost the project can bear.

P2  Everything derived carries how it was derived.
Quote:      "Well theres is raw data and its chains of interpreatations, all with proper chains
            of how they were generated, so we can generate again the same analysis or data
            processing."
Source:     luthier@2a660c8:docs/working-method.md:96
Assumption: recording the chain costs less than reconstructing a result whose origin was lost.

P3  Keep the original evidence and its corrections; put the best reading in front.
Quote:      "The principle is of keeping the original evidence an its correction path but
            surfacing the best interpreatation possible."
Source:     luthier@2a660c8:docs/working-method.md:61
Assumption: keeping is cheap next to losing evidence. (The disk at 97% puts a limit on it.)
```

## Bite 7. Principles: how decisions are taken

```
P4  Decisions follow guiding principles, found as the work goes.
Quote:      "en realidad la decision no deberia ser tomada por Luciano (salvo cuestiones de
            seguridad), sino de acuerdo a ciertos principios rectores que vamos descubriendo a
            medida que vamos avanzando."
Source:     luthier@2a660c8:docs/working-method.md:234
Assumption: a few principles explain most decisions. If every decision needs a reason of its
            own, the principles compress nothing.

P5  A free choice is a legitimate principle, for Luciano and, within margins, for a model.
Quote:      "un ppio rector puede ser a veces Luciano hace lo que se le canta (y a veces la IA
            tambien, con margenes definidos), de hecho la estoscasticidad es necesaria para
            ciertos tipos de optimizaciones o al menos es un ppio valido."
Source:     luthier@2a660c8:docs/working-method.md:235
Assumption: free choices are cheap to undo, by P6 (every change can be undone).

P13 A principle is worth the decisions it guides.
Quote:      "si los principios se cumplen y si son utiles (es decir si se usan, un principio
            puede ser irrelevante, no servir para guiar o tomar ninguna decision)"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:117
Assumption: the use of a principle can be read from the record of decisions.
```

## Bite 8. Principles: the safety net

```
P6  Every change can be undone.
Quote:      "si siempre comiteamos antes de aplicar un cambio, en principio toda decision es
            reversible y si los efetos inesperados aparecen y los detecto, siempre se puede
            volver atras y rectificar."
Source:     chat:7217f251:196
Assumption: unexpected effects are detected before much is built on them (working method §8,
            reversibility).

P8  No more bureaucracy than it pays for.
Quote:      "(sin irnos a la mierda en la burocracia)"
Source:     luthier@2a660c8:docs/working-method.md:306
Assumption: every mechanism costs less than what it prevents. This plan is the first thing to
            judge against it.

P9  What Luciano hasn't fully understood may come in, contained.
Quote:      "sometimes some ideas of the AI are not fully understood by Luciano so the human
            oversight is compromised. Thats tolerable, but has to be contained."
Source:     luthier@2a660c8:docs/working-method.md:110
Assumption: what can't be understood can at least be located.
```

## Bite 9. Principles: scope and attention

```
P7  Each repository is self-contained.
Quote:      "ese seria el criterio: cada repositorio es autocontenido, aunque para evitar
            duplicacion se pueden citar los documentos de uno al otro o algo similar"
Source:     luthier@2a660c8:docs/working-method.md:303
Assumption: the repositories will be read apart: by another person, another session, a release.

P12 Luciano's attention is the scarce resource.
Quote:      "La limitante aqui es mi capacidad de procesamiento de informacion"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:37
Assumption: what the model produces grows faster than what he can read, so every document,
            step and audit is sized to his reading, and the rest is the model's margin.
```

Two more are already in force and need only their sources pinned (step 1.2): P10 (the mathematical
object that best represents a concept is the invariant of its type), since 2026-10-05, and P11
(every criterion is a parameter, never a constant in the code), since 2026-09-11.

## Bite 10. Rules on commits and documents that the model proposed

Most of these were confirmed by a single "Si." that answered a proposal of several parts at once
(chat 7217f251, line 227). The fidelity audit done by hand found that the model's part of the method
is mostly mechanics like these, which read as neutral and so get accepted without being looked at
(working method §7, the model's part in view). One by one:

a. One decision per commit.
b. A decision that is reversed keeps its entry in the log, marked reversed, as a datum.
c. Only tagged milestones are pushed to GitHub.
d. A document for Luciano is committed before he annotates it, so his annotations are the diff
   (D-2026-10-06-j).
e. A plan comes in two documents: the decisions for Luciano, the execution for the sessions
   (D-2026-10-06-q, from this split).

The one with reach is c: it decides when the exports, the audits and every other change become
public. Its cost is that nothing is public between tags. Undo: each is a line of `CLAUDE.md`.

## Bite 11. Your untracked files in sonolocalización

`Lucianos feedbacks/` and `Lucianos ideas dir/funcion de los tipos en Luthier.txt` are untracked
there. You said the feedbacks are the same kind of thing as the observations here ("si, es el mismo
contenido", chat 8d5ce152, line 140), and your sources are committed before anything cites them
(D-2026-10-06-c).

Proposal: commit both as they are, names included, in one commit of their own. The folder keeps its
name, since your notes stay where you wrote them (D-2026-10-06-d), so the two repositories use two
names for the same kind of material, and `CLAUDE.md` names both. The repository is private and
nothing is pushed by this. Undo: one commit. Waits for it: phase 6, items 1 and 2.

## Bite 12. The other open questions of working method §13

- Whether principles and the conflicts between them are yours to decide, on top of safety (the
  model's addition to D-2026-10-06-g).
- Whether each repository needs a list of references.

Nothing waits for these.

## Appendix. Draft entries for the decision log

For the record of step 1.3, and for you to read only if bite 5 is `no`. Quotes are verbatim, typos
included. Sources follow the grammar of bite 2.

```
D-2026-10-06-a  Material is classed by authorship, in the kinds of working method §4.
Author:     Luciano for the axis; the model for the scheme
Quote:      "And authority is somewhat too much"
Source:     luthier@2a660c8:docs/working-method.md:74
Kind:       principle. For P1 (Luciano's part stays discernible)
Status:     proposed (the scheme hasn't been discussed)

D-2026-10-06-b  One decision log per repository; a decision that affects both goes in both.
Author:     Luciano
Quote:      "un decision log per repository, decisiones que afectan a ambos se ponen en ambos."
Source:     luthier@2a660c8:docs/working-method.md:302
Kind:       principle. For P7 (each repository is self-contained)
Status:     current

D-2026-10-06-c  Luciano's sources stay in their language and are committed before anything
                cites them.
Author:     the model, confirmed by Luciano
Quote:      "true"
            "ok"
Source:     luthier@2a660c8:docs/working-method.md:65
            luthier@2a660c8:docs/working-method.md:67
Kind:       principle. For P1 (Luciano's part stays discernible), P2 (everything derived
            carries how it was derived)
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
Kind:       principle. For P3 (keep the original and its corrections)
Status:     current

D-2026-10-06-f  Every change is applied on top of a commit.
Author:     Luciano
Quote:      "si siempre comiteamos antes de aplicar un cambio, en principio toda decision es
            reversible"
Source:     chat:7217f251:196
Kind:       principle. For P6 (every change can be undone), P5 (a free choice is legitimate),
            since it is what makes free choices cheap
Status:     current

D-2026-10-06-g  A model takes decisions within margins, following principles; Luciano keeps
                safety.
Author:     Luciano
Quote:      "The agent has to make decisions otherwise it will be stuck."
            "salvo cuestiones de seguridad"
Source:     luthier@2a660c8:docs/working-method.md:44
            luthier@2a660c8:docs/working-method.md:234
Kind:       principle. For P4 (decisions follow guiding principles), P5 (a free choice is
            legitimate); against P9 (what he hasn't understood may come in, contained) unless
            the end-of-task report of CLAUDE.md is kept
Status:     current for this part. That Luciano also keeps principles and the conflicts
            between them is the model's addition, proposed (bite 12).

D-2026-10-06-h  Reversibility, the parts of working method §8 that "Si." confirmed as a bundle.
Author:     the model
Quote:      "Si."
Source:     chat:7217f251:227
Kind:       principle. For P6 (every change can be undone), P2 (everything derived carries how
            it was derived), P3 (keep the original and its corrections)
Status:     by part:
            - one decision per commit: proposed (bite 10a)
            - a reversal keeps its entry as a datum: proposed (bite 10b)
            - the model's margin is what can be undone before Luciano next looks: replaced by
              the criterion of plan §1 (a decision is local when one commit undoes it and
              nothing depends on it yet), proposed
            - push only tagged milestones: proposed (bite 10c)
            - local git for the memory: confirmed, "Ok",
              luthier@daa5b95:docs/plan-working-method-2026-10-06.md:195
            - local git for the oral transcriptions, text only: confirmed, same line
            - manifests for raw data: confirmed, "ok",
              luthier@daa5b95:docs/plan-working-method-2026-10-06.md:208
            - git outside the folder for large derived data: deferred, "ok",
              luthier@daa5b95:docs/plan-working-method-2026-10-06.md:219

D-2026-10-06-i  The git for large data keeps its repository outside the folder it tracks.
Author:     the model, decided by the implementation
Kind:       case: sonolocalización tracks 234 files under prototipo-cero/2026-09-07/derived/
Status:     current, and deferred

D-2026-10-06-j  A document for Luciano is committed before he annotates it.
Author:     the model
Kind:       case: his annotations on draft 0 of the method had to be separated from the model's
            text by rebuilding draft 0 from the transcript; on this plan they came as a diff
Principles: for P1 (Luciano's part stays discernible), P8 (no more bureaucracy than it pays for)
Status:     proposed (bite 10d)

D-2026-10-06-k  The chat exports go to GitHub.
Author:     Luciano
Quote:      "I think that the chat exports should be in GItHub because they are the ultimate
            proof (the audios) of the ideas origin."
Source:     chat:7217f251:366
Kind:       principle. For P1 (Luciano's part stays discernible)
Status:     current; how, in bite 1

D-2026-10-06-l  In a document for Luciano, a numbered reference carries its statement; records
                may be terse.
Author:     Luciano
Quote:      "Fijate la idea de que documentos que yo voy a consumir no pueden referir a
            principios con numero porque no se de que me estas hablando."
            "Documentos que son de registro pueden ser sintenticos, eso se aplica para los que
            son de mi consumo"
Source:     chat:7217f251:366
            chat:7217f251:382
Kind:       principle. For P12 (Luciano's attention is the scarce resource)
Status:     current

D-2026-10-06-m  A step is a bite of decision Luciano can handle, with implications beyond its
                place; local decisions are the model's margin.
Author:     Luciano for the criterion; the model for its tests (plan §1)
Quote:      "una step deberia ser un bocado de decision que yo pueda manejar y que tenga
            implicancias mas que locales."
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:37
Kind:       principle. For P12 (Luciano's attention is the scarce resource), P4 (decisions
            follow guiding principles)
Status:     current for the criterion; the tests of plan §1 proposed

D-2026-10-06-n  CLAUDE.md is a living document of operative rules, with no meta-information.
Author:     Luciano
Quote:      "Este documento que lee claude no deberia tener la metainformacion ya que es gastar
            tokens al pedo, las meta-anotaciones estaria fuera."
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:163
Kind:       principle. For P8 (no more bureaucracy than it pays for), P12 (Luciano's attention
            is the scarce resource)
Status:     current

D-2026-10-06-o  The principles audit asks three questions (followed and useful; failing by
                conflict; new principles and their cost) and is run by a script.
Author:     Luciano; the trigger is proposed by the model (bite 4)
Quote:      "Aqui la idea es que cada tanto un script llame a leer el repositorio a un agente y
            que analice dos cosas"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:116
Kind:       principle. For P4 (decisions follow guiding principles), P13 (a principle is
            worth the decisions it guides)
Status:     current; trigger proposed

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
Kind:       principle. For P1 (Luciano's part stays discernible), P2 (everything derived
            carries how it was derived)
Status:     current for the folder, carried out in d41026e. The rest was confirmed by "si",
            which answered it together with a question about sonolocalización: a bundle.
            Of his reason, the fact is narrower: a file next to the code changes no hash, but
            any file under src/luthier, even untracked, makes the lock report "with uncommitted
            changes".

D-2026-10-06-q  This plan is split into a document of decisions for Luciano and an execution
                plan for the sessions.
Author:     the model, asked by Luciano
Quote:      "hace la separacion"
Source:     chat:8d5ce152:140
Kind:       case. For P12 (Luciano's attention is the scarce resource)
Status:     current for this plan; as a rule for every plan, proposed (bite 10e)
```
