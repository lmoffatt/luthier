# Working method for Luthier and sonolocalización

Draft 0, 2026-10-06. Written for Luciano and for every session, of any model, that works in
`~/Projects/luthier` or `~/Projects/sonolocalizacion`. It assumes no memory of the conversation that
produced it. It is a proposal: nothing in it binds until Luciano says so, and when he does, that
goes in the decision log of section 4.

Sources: the conversation of 2026-10-06 on the levels of information in the project (Luciano's list
of seven levels plus data and bibliography, and the critique of it); `docs/plan-mechanical-rules-2026-10-06.md`,
which moves the rules a script can check into lints and hooks; the rules kept in the memory of both
projects (everything written in English, never hardcode a criterion, who runs the scripts).

This document covers what stays judgment: what kind of material each file is, what authority it
carries, how it cites its sources, and how a decision is recorded. Rules a script can check belong
to `plan-mechanical-rules` and its `lint/`.

## 1. Two repositories

Luthier (`~/Projects/luthier`) is the language: its specification, its interpreter and its
libraries. Sonolocalización (`~/Projects/sonolocalizacion`) is the project that uses it: the
experiment, its data and its analysis, with the laws of its computations written in Luthier under
`prototipo-cero/luthier/`. Sonolocalización pins the version of Luthier it was certified with in
`prototipo-cero/luthier.lock`.

Material crosses in both directions. What sonolocalización can't express in Luthier comes back as a
design case (`docs/casos-desde-sonolocalizacion.md`). Luciano's notes about Luthier are often
written while he works on sonolocalización, so they land there (`Lucianos ideas dir/funcion de los
tipos en Luthier.txt`, `Lucianos feedbacks/oct 6 0703.txt`), and Luthier's specification cites them
(`docs/semantica/08-tests.md`).

A reference to the other repository names the repository, the commit and the path:
`sonolocalizacion@7f5f664:prototipo-cero/luthier/positions.lut`. A path alone breaks without warning
when the file changes or moves. Today the two notes cited above are worse off than that: they are
untracked in sonolocalización, so no commit holds them at all.

## 2. The kinds of material

Seven kinds, ordered by the authority they carry. The letters are used in the rest of this document.

### A1. Luciano's sources

His voice notes and their transcripts, his written notes, his annotations on a plan or a library,
his questions. This is the only kind of material that decides anything.

Where it lives today:

- Luthier: `docs/audios/` (transcripts tracked, `.ogg` in `raw/` tracked, `.mp3` ignored) and
  `docs/Lucianos ideas/`.
- Sonolocalización: the file `Lucianos ideas` and the folder `Lucianos ideas dir/` at the root,
  `Lucianos feedbacks/`, `prototipo-cero/scripts/plan by Luciano`, and the voice notes of the field
  session in `prototipo-cero/2026-09-07/`.
- Outside both: `~/Projects/Oral transcriptions/Sonolocalizacion`.
- Inside code: comments at the end of `src/luthier/lib/random.lut`, kept uncommitted on purpose.

Rules:

- A model never edits an A1 file. It may transcribe one and it may quote one.
- A1 stays in the language Luciano wrote it in.
- A1 is committed before anything cites it. A source that can't be pinned can't support a decision.

### A2. Outside sources

Answers of other models (Gemini, GPT, Claude on the web), talks, papers, other people's code. They
carry no authority; they are evidence or ideas to weigh.

Where: in Luthier, `docs/IA/` and the Kolomatskaia transcript at the root; in sonolocalización,
`prototipo-cero/AI/` and `prototipo-cero/luthier/AI/` (untracked); papers in `~/papers/ranas`,
outside git.

Rules: kept as they came, in their original language. A document that uses one names whose answer
or which paper it is. A model's answer is never cited as if Luciano had said it, even when he was
the one who pasted it into the repository.

### A3. Data

Recordings and measurements of an experiment (`prototipo-cero/2026-09-07/`, about 5 GB;
`audio-campo/`). Audio and archives are too large for git and are ignored (`*.wav`, `*.zip`,
`*.npz` in `.gitignore`); they live on disk and in Drive.

Rules: data is never edited. Derived data can be reproduced from the raw data, the commit and the
arguments of the script; sonolocalización already writes these next to each output
(`sonolib.write_sidecar`, the `.meta.json` file). Luthier holds no copies of sonolocalización's
data. When it needs them, as for the bit-exact reproduction of session A, it refers to them by
repository, commit, path and a hash of the file.

### B. Elaboration

Analyses, plans, surveys of prior art, handoff notes, the outputs of the ideas pipeline
(`docs/ideas/`), analyses of runs. Mostly written by a model, for Luciano. A B proposes; whatever it
proposes becomes binding only through a decision (C).

Where: `docs/*.md` and `docs/ideas/` in Luthier; in sonolocalización, documents at the root
(`analisis_critico_inventario.md`, `informe_hilos_gemini.md` and others), `ideas/`,
`analisis/diseno_biblioteca.md`.

Rules:

- Every B opens with the header of section 3.
- An analysis of a run is a B whose inputs are results (G). Its header pins them like any other
  source.
- A plan marks which parts are done as it goes (`plan-2026-10-05.md` does it with its "as done"
  sections).
- When Luciano answers a B with a decision, the decision goes to the log. The B is left as it was,
  so it still shows what was proposed.
- An answer given only in chat can't be cited. If it will matter later, it gets written as a B.

### C. Decisions

The record of what Luciano decided, why, and what it replaces. Section 4.

### D. Specification

What the implementation must do. In Luthier: `docs/semantica/`, the conformance tests in
`tests/spec/` (each `.accept.lut` or `.reject.lut` is a line of the specification in executable
form), and `core.lut`. In sonolocalización: the protocol of the experiment
(`protocolo_experimento_cero.md`) and the `.lut` files of `prototipo-cero/luthier/`, which state the
laws the computations must satisfy.

Rules:

- A claim of a D that comes from a decision cites the entry of the log, and through it the source.
- A specification that changes says so in a dated note pointing to what replaces it, as
  `04-kernel.md` and `05-static-semantics.md` already do.
- When the implementation settles something the specification didn't say, the line goes into D in
  the same commit, marked so that Luciano sees it was decided by the implementation
  (`plan-mechanical-rules`, phase 5).

### E. Implementation

The interpreter (`src/luthier/`), the libraries (`src/luthier/lib/`) and the examples; in
sonolocalización, `sonolik/`, `prototipo-cero/src/` and the analysis pipeline in `analisis/`. Code
that no longer runs on the current interpreter goes to `archive/` with a README saying what it was
(Luthier's `archive/README.md` is the model).

### F. Process tools

What produces or polices the rest: the prompts (`prompts/`) and scripts (`scripts/`) of the ideas
pipeline, the lints and hooks of `plan-mechanical-rules`, `CLAUDE.md`, the memory of each project,
and this document. They are versioned like code, and when an output depends on their version, the
version goes in the output's name (`extract_ideas_v1`).

### G. Results

Certificates (`.cert.json`), records of runs (`.run.json`), the sidecars of the analysis pipeline
(`.meta.json`), figures with their heads, logs of certification.

Rule: a result that a document cites is either kept in the repository or reproducible from what the
document records (command, commit, seed). `plan-2026-10-06.md` cites "the certification logs of
2026-10-05/06", and those logs are in neither repository.

## 3. The header of a document

Every B and every D opens with:

- what it is and its date;
- who it is written for;
- its sources, pinned: A1 by file and commit, or by voice note and timestamp; G by command, commit
  and seed; other documents by path;
- its status: draft n, current, done, or replaced by (path).

The recent plans do most of this already (`plan-2026-10-06.md`: "Written for Luciano and for the
sessions that will execute it ... Sources: ..."). Status is what is most often missing, and it's
the first thing a session that comes in without memory needs.

## 4. The decision log

Decisions get revised. The log records each one with its rationale, so that whoever revisits it can
tell whether the reason still holds. "Because I wanted it so" is a rationale and goes in as one: it
tells the next reader the choice is cheap to change.

The kind of rationale says what it takes to undo the decision:

- preference: Luciano chose it and no further reason is needed. Changing it costs the migration.
- principle: it follows from a principle he stated (cite it). Changing it means changing the
  principle or making an exception to it.
- case: something failed or couldn't be expressed (cite the case). Changing it means saying what
  happens to that case.
- evidence: a measurement or a run showed it (cite the result). Changing it takes new evidence.

One file per repository, `docs/decisions.md`, entries appended in order. A decision about Luthier
taken while working on sonolocalización goes in Luthier's log.

An entry, reconstructed from a real reversal (its fields would be checked against the sources
before it goes in the log):

```
D-2026-10-06-a  Every test names the generators it uses; no type owns a generator.
Rationale: the same type is drawn differently for different purposes: one typical
           value, a census, a distribution with bounds or on a log scale.
Kind:      principle (Luciano's note on what types are for in Luthier)
Source:    sonolocalizacion@<commit>:Lucianos feedbacks/oct 6 0703.txt
Replaces:  D-2026-09-30-x, `gen T := term`, one generator per type. Its rationale,
           to take the ranges out of Python and write them in Luthier, still holds.
Status:    current
Landed in: docs/semantica/08-tests.md, G4
```

Rules:

- Only Luciano decides. A model may draft an entry; an entry without a source from Luciano has
  `Status: proposed` until he confirms it.
- A decision taken in chat leaves no file behind. Its entry quotes his words verbatim, with the date
  and `chat` as the source.
- A reversal keeps the old entry. The new entry says `Replaces:`, and the only change to the old one
  is its status, which becomes `replaced by D-...`.
- The specification cites the entry and the entry cites the source. That is the chain from any line
  of the specification back to Luciano's words.

## 5. The cycle

```
A1, A2, A3 --> B --> Luciano reads --> C --> D --> E --> G
               ^                                         |
               +------------ analysis of a run ----------+

Luciano's annotations on a B or on an E are A1 again.
```

A B that Luciano hasn't read reaches D only as a line marked "decided by the implementation"
(section 2, D). That is the case of a long unattended run working from a numbered plan: what it
settles on its own stays visible as such.

## 6. Who runs what

- The scripts that process data (the ideas pipeline, the analysis stages of sonolocalización):
  Luciano runs them, so that "the script ran" and "the model is thinking" stay distinct.
- Lints, `luthier check` and `luthier certify`: hooks and models may run them (Luciano, 2026-10-06,
  recorded in `plan-mechanical-rules`).

## 7. Language

Chat with Luciano is in Spanish. Everything written to the repositories is in English: code,
comments, `.lut`, file names, documents. The exceptions are A1 and A2 as they came, and `archive/`.
This is the rule of 2026-10-01; phase 3 of `plan-mechanical-rules` turns it into a lint.

## 8. What is out of place today

Found on 2026-10-06. None of the fixes requires moving the A1 folders, which many documents cite by
path. Ordered by harm.

1. A1 cited by the specification but untracked: `sonolocalizacion/Lucianos feedbacks/` and
   `Lucianos ideas dir/funcion de los tipos en Luthier.txt`. They need a commit.
2. Citations across repositories without a commit, in `docs/generators-2026-10-06.md`,
   `docs/semantica/08-tests.md` and `docs/plan-2026-10-06.md`. Add the commit once item 1 is done.
3. The certification logs of 2026-10-05/06, cited by `plan-2026-10-06.md`, are not stored. Recover
   them, or say in the plan that they are gone.
4. No decision log in either repository.
5. Prior art in three places: the Kolomatskaia transcript at the root of Luthier (an A2);
   `docs/semantica/02-que-robar.md` (a B among specifications, in Spanish, and sharing the number 02
   with `02-grammar.md`); `docs/ideas/generators-prior-art-2026-10-06.md` (a B among pipeline
   outputs). Proposal: surveys to `docs/prior-art/`, the transcript next to the other A2.
6. `docs/ideas/` mixes the outputs of the ideas pipeline with analyses of other kinds
   (`generators-inventory-2026-10-06.md`, `interval-bounds-2026-10-06.md`).
7. A2 in four places: `docs/IA/` and the root in Luthier, `prototipo-cero/AI/` and
   `prototipo-cero/luthier/AI/` (untracked) in sonolocalización.
8. No `CLAUDE.md` in either repository, so a session without memory doesn't find this document.
   Phase 6.2 of `plan-mechanical-rules` plans one for sonolocalización; both should point here.

## 9. Open for Luciano

- One decision log per repository, or one for both?
- Notes about Luthier written in sonolocalización: do they stay there, cited with a commit, or move
  to Luthier's A1?
- Notes inside code, like the critique at the end of `lib/random.lut`, are kept uncommitted on
  purpose. Should they stay that way, or move to an A1 file so they can be cited?
- Is a decision quoted from chat enough as a source, or should every decision taken in chat end up
  in a file of his?
- Papers stay outside git (`~/papers/`). Does each repository need a list of references?
