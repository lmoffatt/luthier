# Working method for Luthier and sonolocalización

Draft 1, 2026-10-06. Written for Luciano and for every session, of any model, that works in
`~/Projects/luthier` or `~/Projects/sonolocalizacion`. It assumes no memory of the conversations that
produced it. It is a proposal until Luciano confirms it.

Sources: draft 0 of the same day (commit `bf05457`) and Luciano's annotations on it (commit
`2a660c8`; `git diff bf05457 2a660c8` is his text), cited here as "annotation, line n", the line of
this file at `2a660c8`; the conversation
of 2026-10-06 on the levels of information in the project (Claude Code session `7217f251`);
`docs/plan-mechanical-rules-2026-10-06.md`, which moves the rules a script can check into lints and
hooks; the rules kept in the memory of both projects.

What changed from draft 0, all from the annotations:

- The document starts from what the structure is for: three questions that an audit can ask of the
  repositories (section 1, annotation line 309).
- The chain of derivation is the first rule (section 3, line 96).
- Material is classed by authorship. Draft 0 classed it by authority; what matters is that Luciano's
  part stays discernible (line 74).
- Guiding principles are a kind of material of their own, and decisions follow from them. A model
  takes decisions too, within margins (lines 44, 234).
- One decision log per repository; decisions that affect both go in both (line 302).
- Reversibility (section 8), from the conversation that followed the annotations: a commit before
  every change makes a wrong decision cheap, which is what lets a model decide within margins; the
  cost moves to detecting the effect.

## 1. What the structure is for

The project is made by a person working with models. Its value depends on the person's part being
discernible; without that it is generated content with no particular value (annotation, line 74).
The structure in this document exists so that three questions can be asked of the repositories at
any time:

**Q1. Fidelity.** Are the ideas carried faithfully from the sources to the analyses, the decisions,
the specification and the code? In both directions: what Luciano said that was lost or bent on the
way, and what reached the specification attributed to him, or attributed to no one, that a model
proposed.

**Q2. Principles.** What are the guiding principles of Luthier and of sonolocalización, and does
each decision, analysis and implementation advance them or work against them? A principle carries an
assumption that may be false, so the same audit asks which assumptions the work is putting to test.

**Q3. Correspondence.** Does the implementation do what the specification says, and does the
specification say enough? The target is a correspondence both ways: every rule of the specification
has its implementation and its tests, and every behavior of the implementation has its rule. At a
coarser grain, the same between the principles and the program as a whole.

Q3 is mostly mechanical. Q1 and Q2 need a model, with prompts in the style of the ideas pipeline
(`prompts/extract_ideas_v1.md`). Section 10 says what each question needs and how it would run.

## 2. Two repositories

Luthier (`~/Projects/luthier`) is the language: its specification, its interpreter and its
libraries. Sonolocalización (`~/Projects/sonolocalizacion`) is the project that uses it: the
experiment, its data and its analysis, with the laws of its computations written in Luthier under
`prototipo-cero/luthier/`. Sonolocalización pins the version of Luthier it was certified with in
`prototipo-cero/luthier.lock`.

Each repository is self-contained: a session that has only one of them can read its decisions and
its specification (annotation, line 303). Material still crosses. What sonolocalización can't
express in Luthier comes back as a design case (`docs/casos-desde-sonolocalizacion.md`), and
Luciano's notes about Luthier are often written while he works on sonolocalización
(`Lucianos ideas dir/funcion de los tipos en Luthier.txt`, `Lucianos feedbacks/oct 6 0703.txt`).

A note stays where Luciano wrote it (annotation, line 305). The other repository cites it by
repository, commit and path, as in `sonolocalizacion@7f5f664:prototipo-cero/luthier/positions.lut`,
and the decision that rests on it quotes the sentence it needs. The quote is what keeps the citing
repository readable without the other one; the reference is what lets anyone check the quote.

## 3. The first rule: everything derived carries its derivation

There is raw material, and on top of it chains of interpretation, each link saying how it was
produced, so that the same processing or analysis can be generated again (annotation, line 96).
This is the rule that saves the most trouble, and the rest of the document leans on it.

A link records:

- its inputs, pinned: file and commit, or a hash for what is not in git;
- the transformation: the script or the prompt, with its version, and the model when there is one;
- every parameter (never hardcoding a criterion is this same rule, seen from the code);
- the seed of anything random.

A deterministic link (a script with its arguments, `luthier certify` with its seed) can be run
again, so its output needs keeping only when running it again is expensive. A link through a model
(a transcription by whisper, an extraction by Claude) gives a different output each time, so the
output is kept and the record says how it was made. Running it again gives another sample, which is
useful as a check of the first.

What already follows the rule: `sonolib.write_sidecar` writes a `.meta.json` with the arguments and
inputs next to each output of the analysis pipeline of sonolocalización; Luthier's certificates
record the seed, the generators and the hash of the code; the ideas pipeline writes its frontmatter
from Python, with the prompt and the model. What breaks it is listed in section 12.

**Corrections.** A transcript is already a link: the audio is the raw material and the `.md` is
whisper's reading of it. When a link is wrong (a misheard word, a misnomer), the correction is a
new link. The previous version is kept (in git history if it was committed, otherwise as a sibling
file ending in `.orig`), the corrected one takes its place, and a note at its top says what was
corrected (annotation, line 60). The original evidence and the path of its corrections are kept,
and the best available reading is the one in front. The header of the Kolomatskaia transcript
already does this. The audio itself, and a text as Luciano wrote it, are never altered.

## 4. The kinds of material

Classed by who wrote it and by its place in the chain. The letters are used in the rest of this
document.

### A1. Luciano's sources

His voice notes (the audio is the raw material, the transcript its first reading), his written
notes, his annotations on documents and code, his questions, including the ones he puts to other
models. Primary material: it carries his signature, and what to do with it depends on the case
(annotation, line 45). An idea in A1 is evidence of what he thought on that date; it becomes a
decision or a principle only through section 5 or 6.

Where it lives today:

- Luthier: `docs/audios/` (transcripts tracked, `.ogg` in `raw/` tracked, `.mp3` ignored) and
  `docs/Lucianos ideas/`.
- Sonolocalización: the file `Lucianos ideas` and the folder `Lucianos ideas dir/` at the root,
  `Lucianos feedbacks/`, `prototipo-cero/scripts/plan by Luciano`, and the voice notes of the field
  session in `prototipo-cero/2026-09-07/`.
- Outside both: `~/Projects/Oral transcriptions/Sonolocalizacion`.
- Inside other files: his annotations on documents (this one's draft 0) and on code (the end of
  `src/luthier/lib/random.lut`); his turns in the conversations with models of A2.

Rules: it stays where he wrote it; it stays in the language he wrote it in; it changes only by
correction (section 3); it is committed before anything cites it, since a source that can't be
pinned can't support anything.

### A2. Other authors' sources

Answers of other models (Gemini, GPT, Claude on the web), talks, papers, other people's code.
Evidence and ideas to weigh.

A conversation with a model is a mixed file: the questions are Luciano's (A1) and the answers are
the model's (A2), and some of his ideas exist only in those questions (annotation, line 73). An
extraction from such a file separates the turns by author and attributes to him only what is in his
turns. Where the file doesn't mark the turns, the extraction says it couldn't tell.

Where: in Luthier, `docs/IA/` and the Kolomatskaia transcript at the root; in sonolocalización,
`prototipo-cero/AI/` and `prototipo-cero/luthier/AI/` (untracked); papers in `~/papers/ranas`,
outside git.

Rules: kept as they came, in their original language; a document that uses one names whose answer
or which paper it is; a model's answer is never attributed to Luciano, even when he was the one who
pasted it into the repository.

### A3. Data

Recordings and measurements of an experiment (`prototipo-cero/2026-09-07/`, about 5 GB;
`audio-campo/`). Audio and archives are too large for git and are ignored (`*.wav`, `*.zip`,
`*.npz`); they live on disk and in Drive. Raw data is never edited, and everything derived from it
follows section 3. Luthier holds no copies of sonolocalización's data; when it needs them, as for the
bit-exact reproduction of session A, it refers to them by repository, commit, path and hash.

### P. Principles

Section 5.

### B. Elaboration

Analyses, plans, surveys of prior art, handoff notes, the outputs of the ideas pipeline
(`docs/ideas/`), analyses of runs. Mostly written by a model, for Luciano. A B proposes.

Where: `docs/*.md` and `docs/ideas/` in Luthier; in sonolocalización, documents at the root
(`analisis_critico_inventario.md`, `informe_hilos_gemini.md` and others), `ideas/`,
`analisis/diseno_biblioteca.md`.

Rules:

- Every B opens with the header of section 11.
- A B marks, idea by idea, what comes from a source (cited) and what the model proposes. This is the
  boundary Q1 checks, and the one that gets blurred most easily (annotation, line 109).
- An analysis of a run is a B whose inputs are results (G); its header pins them.
- A plan marks which parts are done as it goes (`plan-2026-10-05.md` does it with its "as done"
  sections).
- When Luciano answers a B, his answer is A1 and the decision goes to the log. The B is left as it
  was, so it still shows what was proposed.
- An answer given only in chat can't be cited. If it will matter later, it gets written as a B.

### C. Decisions

Section 6.

### D. Specification

What the implementation must do. In Luthier: `docs/semantica/`, the conformance tests in
`tests/spec/`, and `core.lut`. The rules of `05-static-semantics.md` have identifiers (R1 to R11)
and the conformance tests carry them in their names (`r1_declaration.accept.lut`,
`r1_declaration.reject.lut`); that is what makes Q3 mechanical. In sonolocalización: the protocol of
the experiment (`protocolo_experimento_cero.md`) and the `.lut` files of `prototipo-cero/luthier/`,
which state the laws the computations must satisfy.

Rules:

- A line of D that comes from a decision cites its entry in the log.
- A specification that changes says so in a dated note pointing to what replaces it, as
  `04-kernel.md` and `05-static-semantics.md` already do.
- Section 9 for what the implementation brings back.

### E. Implementation

The interpreter (`src/luthier/`), the libraries (`src/luthier/lib/`) and the examples; in
sonolocalización, `sonolik/`, `prototipo-cero/src/` and the analysis pipeline in `analisis/`. Code
that no longer runs on the current interpreter goes to `archive/` with a README saying what it was
(Luthier's `archive/README.md` is the model).

### F. Process tools

What produces or polices the rest: the prompts (`prompts/`) and scripts (`scripts/`) of the ideas
pipeline and of the audits of section 10, the lints and hooks of `plan-mechanical-rules`,
`CLAUDE.md`, the memory of each project, and this document. Versioned like code; when an output
depends on their version, the version goes in the output's name (`extract_ideas_v1`).

### G. Results

Certificates (`.cert.json`), records of runs (`.run.json`), the sidecars of the analysis pipeline
(`.meta.json`), figures with their heads, logs of certification. A result that a document cites is
kept, or can be produced again from what the document records (section 3).

## 5. Principles

A principle is a statement of what Luthier or sonolocalización is trying to be, used to choose
between options. Two that are already written down: "find the mathematical object that best
represents each concept and put it as the invariant of the type" (Luciano, 2026-10-05, in
`07-characterizations.md`); every criterion is a parameter, never a constant in the code (Luciano,
2026-09-11, rule 1 of `plan-mechanical-rules`).

An entry records:

- the statement;
- the assumption it carries: what has to be true for following it to pay off;
- who stated it, and the source;
- its status: proposed, confirmed by Luciano, or retired (and why).

A free choice is a valid principle: Luciano decides as he likes, and a model may choose freely
within a margin he sets (annotation, line 235). Randomness has its place in a search, since a choice
made without a reason reaches options a rule would never try. The log records that the choice was
free, so that nobody later reads it as a consequence of some principle.

Principles are extracted from A1 and from the rationales of past decisions, by a prompt (Q2). An
extracted principle stays proposed until Luciano marks it. This is where his signature matters most:
a principle steers many decisions, so a principle he hasn't understood is the most expensive thing a
model can bring in (section 7).

They live in `docs/principles.md` in each repository, under the same rule as decisions for the ones
that apply to both.

Luciano suspects that many decisions follow a likelihood principle, and that writing the principles
as terms of a cost function would be the biggest prize (annotation, line 234). The first step needs
no numbers: for each decision, the sign of its effect on each principle it touches (for, against,
neutral) and the assumption it leans on. If weights can be estimated at all, it will be from that
record and from how the decisions turned out.

## 6. Decisions

**Who decides.** Most decisions follow from principles, and whoever applies them can take them, a
model included; an agent that has to ask for everything gets stuck (annotation, lines 44 and 234).
Luciano's part: stating and confirming principles; settling a conflict between principles, which is
a matter of preference and therefore his; safety; and any decision he wants to take himself. A model
decides within the margins those leave, and says it did.

**What a model owes at each decision** (annotation, line 236): which principles the decision touches,
in which direction, and which assumption it leans on. In chat, a line before acting on anything that
isn't routine; in the log, the fields of the entry.

**The log.** One file per repository, `docs/decisions.md`, entries appended in order. A decision that
affects both repositories goes in both: the full entry in the one it mainly concerns, and in the
other the decision and its rationale with a reference to the full entry (annotation, line 302).

An entry, reconstructed from a real reversal (its fields would be checked against the sources before
it goes in the log):

```
D-2026-10-06-a  Every test names the generators it uses; no type owns a generator.
Author:     Luciano
Quote:      "<his sentence, verbatim>"
Source:     sonolocalizacion@<commit>:Lucianos feedbacks/oct 6 0703.txt
Rationale:  the same type is drawn differently for different purposes: one typical
            value, a census, a distribution with bounds or on a log scale.
Kind:       principle
Principles: for: belonging to a type certifies that a value passed the type's check
            (Lucianos ideas dir/funcion de los tipos en Luthier.txt)
Replaces:   D-2026-09-30-x, `gen T := term`, one generator per type. Its rationale,
            to take the ranges out of Python and write them in Luthier, still holds.
Status:     current
Landed in:  docs/semantica/08-tests.md, G4
```

The kind of rationale says what it takes to undo the decision:

- free: Luciano's preference, or a model's choice within a margin he set. Undoing it costs only the
  migration.
- principle: it follows from a principle (named in the entry). Undoing it means changing the
  principle or making an exception to it.
- case: something failed or couldn't be expressed (cite the case). Undoing it means saying what
  happens to that case.
- evidence: a measurement or a run showed it (cite the result). Undoing it takes new evidence.

**Confirmation, without bureaucracy** (annotation, line 306). The log is written by a model, from
Luciano's words. An entry whose author is Luciano carries the words it rests on, verbatim, and a
script checks that the quote is in the source at that commit. For a decision taken in chat, the
source is the transcript Claude Code keeps of the session (`~/.claude/projects/<project>/<session>.jsonl`),
and the same check works for as long as that file exists. An entry whose author is a model says so,
with the margin it acted in. Luciano's explicit mark (he writes `ok` on it, as he does in his
annotations) is needed only for principles; a model never writes it.

A reversal keeps the old entry: the new one says `Replaces:`, and the only change to the old one is
its status, which becomes `replaced by D-...`.

## 7. Keeping the model's part in view

Some ideas proposed by a model reach the work without Luciano having fully understood them. That is
tolerable, provided it stays contained (annotation, line 110). The containment:

- A B marks the model's ideas as proposals (section 4, B).
- A model's idea may reach D or E through a decision taken within a margin, recorded as such. It
  can't become a principle without Luciano's mark.
- When a model asks Luciano to accept something, it first says in a sentence or two, in his terms,
  what accepting it implies. A "dale" to a bundle of ten changes confirms the bundle, and the log
  says so.
- Q1 lists every line of D whose chain ends in a model's proposal. The length of that list, against
  the length of D, is a rough measure of how much of the work is his.

## 8. Reversibility

There is a loophole in section 6: a model may believe it follows a principle, or follow it in fact,
and its automatic actions still have effects nobody expected. Luciano's answer (2026-10-06, chat): if
every change is applied on top of a commit, every decision is reversible in principle, and when the
unexpected effect is detected, the work goes back and is corrected.

This holds, with a precision: within the two repositories almost everything is files, so the
previous state always exists. That is what bounds the cost of a wrong decision and what makes the
split of section 6 reasonable; without it, letting a model decide would be imprudent. The hard part
is not going back but knowing when to: an unexpected effect of a principle followed well is, by
definition, something nobody was looking at. The constant `lmMaxIter : Int := 200` of the night of
2026-10-05 was committed and could be reverted in a second; it was found only when a status report
was asked for at 04:41. The cost of a wrong decision is the detection latency times what was built
on top of it in the meantime, and reverting is cheap at the level of files and expensive at the
level of meaning: dependents are left dangling, and any change to the interpreter invalidates every
certificate.

Rules:

- A change is applied on a clean tree: everything before it is committed first. The pre-commit hook
  of `plan-mechanical-rules` runs the lints at that point.
- One decision, one commit, and the entry in the log names the commit. Reverting a decision is then
  reverting one commit, and `Replaces:` is mechanical. Several decisions in one commit are reverted
  together or not at all.
- A reversal keeps the entry, with status `reverted` and the effect that caused it. A reversal is a
  datum: either the principle was misread or its assumption was false, and the entry says which. This
  is the most direct evidence there is about which principles the project really follows (Q2).
- The margin within which a model decides without asking is what can be reverted before the next
  time Luciano looks.
- What looks for the effects: certificates and lints (mechanical, at every commit); the model's own
  report of what it decided within margins, at the end of each task and not only when asked; the
  audits of section 10, run by Luciano.

**What is pushed.** Git is local by construction; GitHub is a copy. The history of a branch that has
not been pushed is as reversible as if the remote did not exist, and today the working branches of
both repositories are ahead of the remote. What a push makes irreversible is exposure: pushed
content may be cloned or cached. So `main` is pushed at tagged milestones (as `v0.1` was), and work
branches stay local until a milestone absorbs them.

**What git does not revert.** The model's memory (`~/.claude/projects/<project>/memory/`), where a
misread principle survives any revert of the repository; the transcripts of oral notes in
`~/Projects/Oral transcriptions/`, which are A1; the session transcripts Claude Code keeps; compute
already spent; and Luciano's own reading of an analysis that carried a wrong idea, which is the one
irreversible effect that matters here and is what section 7 contains. The first two get a local git
of their own, with no remote. Decisions taken in chat copy the message into the repository when the
entry is written, so the check of section 6 does not depend on the session transcript.

**What is ignored for size.** `*.wav`, `*.zip`, `*.npz` and the `.mp3` of the voice notes are
ignored for GitHub's limits, not git's; a local git holds 5 GB without trouble, what it holds badly
is large files that change often, since each version is stored whole and audio does not compress.
Three cases:

- Raw data never changes (`prototipo-cero/2026-09-07/raw`, `measures`, the `.ogg`). It needs
  integrity, not reversibility: a `manifest.sha256` committed in the repository says that the file of
  today is the file of the experiment.
- Derived data is produced again from code, arguments and seed (section 3); its reversibility is in
  the commit of the code. What justifies keeping it is the cost of producing it again (the
  certificates of the project took about ten hours).
- Large, edited and not reproducible: nothing in these repositories is in this case.

The proposal: a nested git with no remote in `prototipo-cero/2026-09-07/`, ignored by the parent as
a directory, with the raw data committed once and the derived data committed per run, each commit
naming the commit of the code that produced it. If the derived data grows past what that bears, the
step is git-annex, which keeps the content out of the history; DVC does the same with more
machinery than the project needs.

## 9. Specification and implementation

Implementing brings out problems and questions the specification didn't foresee (annotation, line
171). That is expected, and it has a fixed route back: a question goes to a B, or to Luciano if it
touches a principle; a choice the implementation had to make goes into D in the same commit, marked
"decided by the implementation", so Luciano sees it (`plan-mechanical-rules`, phase 5). A long
unattended run settles many such choices; this is how they stay visible.

The same form (a specification with its laws, and one or more implementations that must satisfy
them) applies to the processing and analysis of data, beyond building the language (annotation, line
170). A stage of the analysis pipeline of sonolocalización is specified by the laws its output must
satisfy, and its scripts are implementations of it. `prototipo-cero/luthier/` already does this for
the estimators.

## 10. The audits

Each audit is a prompt in `prompts/` and a script in `scripts/`, in the style of `extract_ideas.py`:
the script assembles the inputs, calls the model, and writes the frontmatter of the output itself.
The output is a B. Mechanical audits are scripts with no model, and may run as lints.

**Q1. Fidelity.** Inputs: the extractions of ideas per source (`docs/ideas/*_ideas.md`, already
verbatim and with timestamps), the decision log, D. Two passes. From the sources forward: ideas that
were decided and never landed in D, and ideas that landed changed. From D back: lines attributed to
Luciano with no quote behind them, and lines with no source at all (the list of section 7).

**Q2. Principles.** First prompt: candidate principles from A1 and from the rationales in the log,
each with its assumption; the output is proposed entries for `docs/principles.md`. Second prompt: for
a range of commits, a plan or a set of decisions, the effect on each principle (for, against,
neutral) and the assumptions being leaned on.

**Q3. Correspondence.** Mechanical part: every rule of `05-static-semantics.md` against the files of
`tests/spec/` and the error messages of the checker. Today R1 to R9 have conformance tests; R10 has
none; R11 has none and says it isn't implemented. Part for a model: rules whose text and tests
disagree, and behavior of the implementation that no rule covers. Principles against the program as
a whole, coarsely, by a model.

Who runs them: the mechanical part of Q3, like any lint, may be run by hooks and models. Q1 and Q2
process the record of the project, so Luciano runs them, as he runs the ideas pipeline.

## 11. Common rules

**Header.** Every B and every D opens with: what it is and its date; who it is written for; its
sources, pinned (A1 by file and commit, or by voice note and timestamp; G by command, commit and
seed; other documents by path); its status (draft n, current, done, or replaced by a given path).

**Who runs what.** The scripts that process data or the record of the project (the ideas pipeline,
the audits Q1 and Q2, the analysis stages of sonolocalización): Luciano runs them, so that "the
script ran" and "the model is thinking" stay distinct. Lints, `luthier check` and `luthier certify`:
hooks and models may run them (Luciano, 2026-10-06, recorded in `plan-mechanical-rules`).

**Language.** Chat with Luciano is in Spanish. Everything written to the repositories is in English:
code, comments, `.lut`, file names, documents. The exceptions are A1 and A2 as they came, and
`archive/`. Rule of 2026-10-01; phase 3 of `plan-mechanical-rules` makes it a lint.

## 12. What is out of place today

Found on 2026-10-06. None of the fixes requires moving an A1 folder. Ordered by harm.

1. A1 cited by the specification but untracked: `sonolocalizacion/Lucianos feedbacks/` and
   `Lucianos ideas dir/funcion de los tipos en Luthier.txt`. They need a commit.
2. Citations across repositories without a commit, in `docs/generators-2026-10-06.md`,
   `docs/semantica/08-tests.md` and `docs/plan-2026-10-06.md`. Add the commit after item 1.
3. The certification logs of 2026-10-05/06, cited by `plan-2026-10-06.md`, are stored nowhere.
   Recover them, or say in the plan that they are gone.
4. No decision log and no list of principles in either repository.
5. The notes at the end of `src/luthier/lib/random.lut` are kept uncommitted, so nothing can cite
   them.
6. Prior art in three places: the Kolomatskaia transcript at the root of Luthier (an A2);
   `docs/semantica/02-que-robar.md` (a B among specifications, in Spanish, sharing the number 02 with
   `02-grammar.md`); `docs/ideas/generators-prior-art-2026-10-06.md` (a B among pipeline outputs).
   Proposal: surveys to `docs/prior-art/`, the transcript next to the other A2.
7. `docs/ideas/` mixes the outputs of the ideas pipeline with analyses of other kinds
   (`generators-inventory-2026-10-06.md`, `interval-bounds-2026-10-06.md`).
8. A2 in four places: `docs/IA/` and the root in Luthier, `prototipo-cero/AI/` and
   `prototipo-cero/luthier/AI/` (untracked) in sonolocalización.
9. R10 of `05-static-semantics.md` has no conformance test.
10. No `CLAUDE.md` in either repository, so a session without memory doesn't find this document.
    Phase 6.2 of `plan-mechanical-rules` plans one for sonolocalización; both should point here.
11. No git in the memory of either project nor in `~/Projects/Oral transcriptions/` (section 8).
12. No `manifest.sha256` of the raw data of `prototipo-cero/2026-09-07/`, and no git of its own.

## 13. Open for Luciano

- The split of section 6: principles, conflicts between principles and safety are Luciano's, the
  rest can be a model's within margins. Is that the split?
- Confirmation: decisions rest on a quote checked by a script, principles need Luciano's mark. Is
  that enough, or too much?
- Papers stay outside git (`~/papers/`). Does each repository need a list of references?
