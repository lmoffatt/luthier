# Plan: putting the working method into practice, 2026-10-06

Draft 1, 2026-10-06. Status: phase 0 is done; steps 2.2, 2.3, 3.1 and 3.2 are confirmed by Luciano;
the rest is proposed.

Written for Luciano, and for the sessions that will execute it. It assumes no memory of the
conversation that produced it; everything needed is here or in the files named.

Sources:

- The working method, `docs/working-method.md` at `ed8052a`, cited by section number and title.
- Luciano's annotations on draft 0 of the working method, commit `2a660c8`, cited as "annotation on
  the method, line n".
- Luciano's annotations on draft 0 of this plan, commit `daa5b95`, cited as "annotation on the
  plan, line n".
- Claude Code session `7217f251`
  (`~/.claude/projects/-home-lmoffatt-Projects-luthier/7217f251-afdd-4548-8d5d-2cf7468c47d4.jsonl`),
  cited as "chat, line n", the line of that transcript. The file only grows, so the line is stable.
- `docs/plan-mechanical-rules-2026-10-06.md`, written by another session the same day: lints and
  hooks for the rules that a script can check. Untracked, so cited by path only.
- Measurements of 2026-10-06: `/home` is 97% full (56 GB free); `~/Projects/Oral transcriptions` is
  2.7 GB (1509 `.md`, 1149 `.mp3`, 967 `.ogg`); sonolocalización tracks 234 files under
  `prototipo-cero/2026-09-07/derived/`; on GitHub, `lmoffatt/luthier` is public and
  `lmoffatt/sonolocalizacion` is private.

What changed from draft 0, all from Luciano's annotations on the plan and the chat:

- Section 1 analyses what a step is, as he asked (annotation on the plan, lines 36 and 37), and every
  step now says whether it goes to him or stays in the model's margin.
- Every principle, decision and section is named by its number and its statement (chat, line 366).
  The records themselves (`principles.md`, `decisions.md`) may stay terse (chat, line 382).
- The chat exports go to GitHub (chat, line 366); step 1.1 says what that implies, since the luthier
  repository is public.
- The principles audit asks the three questions of annotation on the plan, lines 116 to 120 (step
  5.2).
- `CLAUDE.md` is a living document of operative rules with no meta-information in it (annotation on
  the plan, line 163; step 2.1).
- Two new principles proposed from the annotations: P12 (Luciano's attention is the scarce resource)
  and P13 (a principle is worth the decisions it guides).

## Conventions of this document

- **Origin** of each step or claim: "Luciano", with the source of his words; "the model", for a
  proposal of the model; "the model, confirmed by Luciano", with his words.
- **For Luciano** marks a step that needs his answer; **model's margin** marks a step the model can
  take on its own, under the criterion of section 1.
- **References.** A principle, a decision or a section of another document is named by its number and
  its statement every time, as in "P6 (every change can be undone)".

The principles named in this plan, drafted in full in Appendix B:

| | Statement | Status |
|---|---|---|
| P1 | Luciano's part stays discernible | proposed |
| P2 | Everything derived carries how it was derived | proposed |
| P3 | Keep the original and its corrections; the best reading goes in front | proposed |
| P4 | Decisions follow guiding principles, found as the work goes | proposed |
| P5 | A free choice is a legitimate principle, for Luciano and, within margins, for a model | proposed |
| P6 | Every change can be undone | proposed |
| P7 | Each repository is self-contained | proposed |
| P8 | No more bureaucracy than it pays for | proposed |
| P9 | What Luciano hasn't fully understood may come in, contained | proposed |
| P10 | The mathematical object that best represents a concept is the invariant of its type | in force since 2026-10-05 |
| P11 | Every criterion is a parameter, never a constant in the code | in force since 2026-09-11 |
| P12 | Luciano's attention is the scarce resource | proposed, new |
| P13 | A principle is worth the decisions it guides | proposed, new |

## 1. What a step is

Luciano's criterion (annotation on the plan, line 37): "La limitante aqui es mi capacidad de
procesamiento de informacion, de modo que una step deberia ser un bocado de decision que yo pueda
manejar y que tenga implicancias mas que locales." He asked whether it is a good criterion.

It is, and it separates two units that draft 0 confused. The unit of review is what reaches him: a
bite of decision. The unit of reversal is a commit (working method §8, reversibility). A step may
take several commits; a commit never spans two steps. Each half of the criterion needs a test that
someone other than him can apply.

**"A bite I can handle."** A step for Luciano is one question he can answer with ok, no, or a
correction, after reading at most a screen: what is decided, what it implies beyond its own place,
what it costs, how it is undone. If it needs more than that, it is split. Draft 0 broke this twice:
step 2.3 put the git for the memory and the git for the transcripts in one step, and Appendix B asked
him to judge 21 entries at once. Draft 1 splits both.

**"Implications more than local."** A decision is local when one commit undoes it and nothing else
depends on it yet. It is not local when any of these hold: it touches a principle; it sets a format
or a rule that others will follow (a record format, `CLAUDE.md`, the specification); it is expensive
to undo (data, recertification); or it exposes something (a push to a public repository). Local
decisions are the model's margin (working method §6, decisions) and reach Luciano only in the report
at the end of a task. The rest are his steps.

**The risk the criterion leaves open.** Many local decisions can add up to a change that is not
local, and none of them would have reached him. The principles audit of step 5.2 is what looks for
that drift.

This criterion is a principle in its own right: P12 (Luciano's attention is the scarce resource).
It also gives the test of when the model asks and when it acts, which `CLAUDE.md` needs in one line
(step 2.1).

## 2. The order, and why

The method needs pieces that don't exist yet: a decision log, a list of principles, a check of
quotes, a copy of the chat in the repository. Each phase builds what the next one needs. Until a
piece exists, its job is done by hand, and the plan says where.

| Phase | What | Needs | Cost |
|---|---|---|---|
| 0 | Pin the sources | nothing | done |
| 1 | The record: chat export, principles, decisions | 0 | half a day, plus Luciano's reading of Appendix B |
| 2 | The model's conduct: `CLAUDE.md`, the end-of-task report, memory under git | 1, for the principles to report against | two hours |
| 3 | Data: manifests | nothing | one hour |
| 4 | Mechanical checks: quotes, specification against tests | 1, for a log to check | half a day |
| 5 | Audits by prompt: fidelity, principles | 1, and the hand results of Appendices A and B to calibrate against | a day, plus the runs |
| 6 | The list of working method §12 (what is out of place today) | 1, since each fix is a logged decision | an hour per item |

Phase 3 can run in parallel with anything.

## Phase 0. Pin the sources (done)

**0.1 Three commits for the working method.** `bf05457` is draft 0, recovered verbatim from the
Write call that created it (chat, line 116). `2a660c8` is Luciano's annotations; before committing,
the diff between the two was checked to contain only his added lines and trailing spaces he added to
three of the model's. `62ac538` is draft 1, whose header cites the two commits.

- Origin: the model, applying working method §3 (everything derived carries its derivation) and
  annotation on the method, line 61 ("keeping the original evidence an its correction path").
- Principles: for P1 (Luciano's part stays discernible), P2 (everything derived carries how it was
  derived), P3 (keep the original and its corrections).
- Undo: `git reset --soft 21aa9c9` puts all of phase 0 back in the working tree.

**0.2 Correction of working method §8 (reversibility)**, `ed8052a`. Draft 1 of the method proposed a
git nested inside `prototipo-cero/2026-09-07/`; sonolocalización already tracks files there, so the
repository for large data has to live outside the folder. Marked in §8 as decided by the
implementation.

**0.3 This plan**: draft 0 `a8cc4c9`, Luciano's annotations `daa5b95`, this draft 1 on its own
commit.

**Finding.** Committing a document before Luciano annotates it makes his part a diff at no cost:
`git diff bf05457 2a660c8` is exactly what he wrote. For draft 0 of the method the separation had to
be rebuilt from the transcript; for this plan it was free. Decision D-2026-10-06-j (a document for
Luciano is committed before he annotates it).

## Phase 1. The record

**1.1 The chat, exported.** Model's margin to write the script; Luciano runs it.

Luciano asked whether there is anything for the model to do here (annotation on the plan, line 105).
There is, once: the export doesn't exist yet. The model writes `scripts/export_chat.py <session.jsonl>`.
After that, he runs it the way he runs the transcription of his voice notes.

What it writes: `docs/chat/<date>_<session8>.md` with the text of every turn, by author, each with
its timestamp and its line in the transcript. It exports both sides, Luciano's turns and the model's
replies, because a confirmation means nothing without what it answered: "Si." (chat, line 227) only
says something next to the proposal before it. Tool calls and their outputs are left out. Text
inserted by the harness (`<system-reminder>`, `<ide_opened_file>`, the output of local commands) is
dropped. Text Luciano pasted is kept and marked as pasted, since it may not be his. Messages he
sends while the model is working are recorded as `attachment` in the transcript (chat, line 382),
and the script reads them too. The frontmatter is written by Python: session id, sha256 of the
transcript, number of turns.

The exports go to GitHub. Luciano's reason: they are the final proof of where an idea came from, as
the voice notes are (chat, line 366). Decision D-2026-10-06-k (the chat exports go to GitHub).

What it implies. `lmoffatt/luthier` is public, so each export is published at the next push of
`main`, and publishing can't be undone (working method §8, reversibility). Two proposals, one bite
for Luciano:

- He reads each export before committing it. He runs the script anyway, so the export is a file in
  front of him.
- A session that touches sonolocalización's private matters (the agreement with databaum, the
  strategy on intellectual property) is exported into the private sonolocalización repository and
  never into luthier.

The rest of the step:

- Principles: for P1 (Luciano's part stays discernible), P2 (everything derived carries how it was
  derived).
- Assumption: the transcript format of Claude Code stays readable. It is internal and may change, so
  the script fails loudly on a line it can't parse.
- Undo: one commit, until the push.
- Detects: the check of quotes of step 4.1 fails when a quote is missing from the export.
- Done when: the export of session `7217f251` holds every chat quote of Appendix B.

**1.2 `docs/principles.md`**, from Appendix B once Luciano has marked it. Model's margin to write the
file; the marks are his.

The file is a record, so it can be terse (chat, line 382): number, statement, quote, source,
assumption, status. An entry stays `proposed` until Luciano writes `ok` on it, and a model never
writes that mark (working method §6, decisions).

- Origin: the model, from working method §5 (principles), which comes from annotation on the method,
  line 234.
- Principles: for P4 (decisions follow guiding principles); against P8 (no more bureaucracy than it
  pays for), since it is one more file to keep up. The audit of step 5.2 decides whether it pays.
- Assumption: a principle can be stated in a sentence, with one assumption.

**1.3 `docs/decisions.md`**, from Appendix B. Model's margin.

A record, terse. Its format is the one of working method §6 (decisions), with one change found while
drafting Appendix B: `Source:` carries the line, `path@commit:line`. Two of Luciano's confirmations
are one word ("true" and "ok", annotation on the method, lines 65 and 67), and a one-word quote can't
be checked by searching the file for it.

- Origin: Luciano, annotation on the method, lines 302 and 306; the format is the model's.
- Principles: for P1 (Luciano's part stays discernible), P4 (decisions follow guiding principles).
- Assumption: entries get written when the decision is taken. Rebuilt afterwards, as Appendix B does,
  they cost an hour of reading the transcript per session.

**1.4 Sonolocalización.** Model's margin. `docs/decisions.md` and `docs/principles.md` at its root,
in a new `docs/` folder. The decisions about the method get a short entry there that refers to
Luthier's log. The method isn't copied: sonolocalización's `CLAUDE.md` cites
`luthier@<commit>:docs/working-method.md`.

- Origin: Luciano, annotation on the method, line 303: "para evitar duplicacion se pueden citar los
  documentos de uno al otro".
- Principles: for P7 (each repository is self-contained).

## Phase 2. The model's conduct

**2.1 `CLAUDE.md`.** For Luciano: its content.

Luciano's annotation on the plan, line 163: the lines of `CLAUDE.md` work as principles. That's fine
at the start, but in the long run it has to be a living document that keeps changing. And the file
Claude reads should carry no meta-information: it spends tokens on every session for nothing, so the
meta-annotations live outside it. Decision D-2026-10-06-n (`CLAUDE.md` is a living document of
operative rules, with no meta-information).

Three consequences:

- `CLAUDE.md` holds rules, one line each, with no origins, quotes or sources. The provenance of each
  line is in `docs/decisions.md`, and changing a line is a logged decision.
- It doesn't send the model to read the working method whole. The method is full of meta-information
  (annotation lines, origins, reasons), which is what a human reader and the audits need. `CLAUDE.md`
  carries the operative distillation of it.
- It lists the principles in force by statement only. `docs/principles.md`, with its quotes and
  assumptions, is read by the audits.

Draft for Luthier (sonolocalización gets the same lines added to the file that phase 6.2 of
`plan-mechanical-rules`, its `CLAUDE.md`, writes):

```
# Working rules

- Luciano's notes, transcripts and annotations are never edited. A correction keeps the original
  in git and puts the corrected version in front, with a note at its top.
- In a document you write, mark what comes from a source (cite it) and what you propose.
- Everything derived records its inputs (by commit or hash), the script or prompt with its
  version, every parameter, and the seed.
- Commit before every change. One decision, one commit.
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

The list of principles grows as Luciano marks the ones of Appendix B.

- Origin: the model, from working method §6 (decisions) and §8 (reversibility); the report of the
  principles at each decision is Luciano's (annotation on the method, line 236); the absence of
  meta-information is Luciano's (annotation on the plan, line 163).
- Principles: for P1 (Luciano's part stays discernible), P6 (every change can be undone), P9 (what
  he hasn't understood may come in, contained), P12 (Luciano's attention is the scarce resource).
- Assumption: written instructions hold. `plan-mechanical-rules` reports that they degrade over a
  long run (the constant `lmMaxIter`, night of 2026-10-05), which is why steps 2.2 and 4.1 exist.

**2.2 Reminder at the end of a turn.** Confirmed by Luciano ("ok", annotation on the plan, line 174).
A `Stop` hook, next to the one `plan-mechanical-rules` adds to run the fast lints, prints the commits
of the session that touch the specification or the implementation and that no entry of the log
names. It doesn't block, since not every commit is a decision.

- Principles: for P6 (every change can be undone), P9 (what he hasn't understood may come in,
  contained); against P8 (no more bureaucracy than it pays for) if it fires on routine commits, in
  which case it goes.

**2.3a Git for the model's memory.** Confirmed by Luciano ("Ok", annotation on the plan, line 195).
`git init` in `~/.claude/projects/<project>/memory/` for each project, a first commit of its current
state, and a `Stop` hook that commits whatever changed there during the turn. Then `git log -p` in
that folder shows what the model wrote about Luciano and the project, at the one place where a
misread principle survives any revert of the repository.

**2.3b Git for the oral transcriptions.** Confirmed by the same "Ok". `git init` in
`~/Projects/Oral transcriptions/`, tracking only the text (`*.md`, `*.txt`). The audio (2.7 GB, with
the disk at 97%) is covered by a `manifest.sha256` committed with the text. Transcripts are what gets
corrected (working method §3, the corrections), and audio never changes.

For both:

- Principles: for P2 (everything derived carries how it was derived), P3 (keep the original and its
  corrections), P6 (every change can be undone), P9 (what he hasn't understood may come in,
  contained).
- Runs: the model; `git init` processes nothing.
- Undo: deleting the `.git` folder leaves the memory and the transcripts as they were.
- Cost: minutes.

## Phase 3. Data

**3.1 Manifests in sonolocalización.** Confirmed by Luciano ("ok", annotation on the plan, line
208). `prototipo-cero/2026-09-07/manifest.sha256` and `audio-campo/manifest.sha256`, covering every
file the parent repository ignores there (`*.wav`, `*.zip`, `*.npz`), committed.
`sha256sum -c --quiet` goes into `lint/full.sh`, the slow check of `plan-mechanical-rules`.

- Principles: for P2 (everything derived carries how it was derived), P3 (keep the original and its
  corrections).
- Runs: the model; hashing is a check and produces no result.
- Cost: minutes, about 5 GB of hashing.

**3.2 The git for large data, deferred.** Confirmed by Luciano ("ok", annotation on the plan, line
219). With the disk at 97% it would take 5 GB that aren't there, and it would protect derived `.npz`
files, which can be produced again from code and arguments. It waits until there is a derived file
that is expensive to produce again and changes between runs.

- Principles: for P8 (no more bureaucracy than it pays for).

## Phase 4. Mechanical checks

**4.1 Check of quotes.** Model's margin. `scripts/check_quotes.py`: every entry of
`docs/decisions.md` and `docs/principles.md` whose author is Luciano has `Quote:` and
`Source: path@commit:line`, and the quote is at that line or the lines after it in
`git show commit:path`, with whitespace normalized. Chat sources are read from the exports of step
1.1. A source in the other repository is read with `git -C`; if that repository is absent the check
warns and doesn't fail, by P7 (each repository is self-contained). Output in the format of
`plan-mechanical-rules`, `path:line: rule: message`, exit 1 on findings.

- Origin: the model, answering annotation on the method, line 306: "una revision de algun modo
  certificada quizas? (sin irnos a la mierda en la burocracia)".
- Principles: for P1 (Luciano's part stays discernible); for P8 (no more bureaucracy than it pays
  for), since it is a script instead of a ritual.
- Runs: the model and the hooks, like a lint.

**4.2 Specification against tests.** Model's margin. `scripts/check_spec_tests.py` takes the rules
R1 to R11 of `docs/semantica/05-static-semantics.md` and looks for them in the names of the files of
`tests/spec/`. Each rule needs a file that must be accepted (`.accept.lut`) and one that must be
rejected (`.reject.lut`), and a rule marked "not implemented" is reported as such. Expected output
today: R10 (a law characterizes; a second implementation is not a law) has no test, and R11 (a
condition refines in its branch) is not implemented. This is the mechanical part of Q3, the audit of
correspondence between specification and implementation (working method §10, the audits).

- Origin: Luciano, annotation on the method, line 313, "La implementacion es fiel a la
  especificacion?"; the check is the model's.
- Runs: the model and the hooks.

**4.3 Header check, as a warning.** Model's margin. A document for Luciano dated 2026-10-06 or later
has the four items of the header of working method §11 (common rules): what it is and its date, who
it is written for, its sources, its status. Older documents are listed in an allow file.

- Principles: for P1 (Luciano's part stays discernible); against P8 (no more bureaucracy than it pays
  for) if it turns into form-filling. The first time it flags a document whose header was fine for a
  human reader, it goes.

## Phase 5. Audits by prompt

Each audit is a prompt in `prompts/` and a script in `scripts/`, in the style of `extract_ideas.py`.
Outputs go to `docs/audits/<date>_<audit>_<prompt version>_<model>.md`.

**5.1 Q1, the fidelity audit.** Model's margin to write it; Luciano runs it.
`prompts/audit_fidelity_v1.md`. First target: `docs/working-method.md` at `ed8052a`, against its
sources (`2a660c8`, the export of the chat). Appendix A is the same audit done by hand. If the prompt
and Appendix A disagree, find out which is right before the prompt is used on anything else.

- Assumption: a model can tell Luciano's ideas from its own in a document that blends them.
  Appendix A is the test.

**5.2 Q2, the principles audit.** For Luciano: how often it runs.

Luciano's design (annotation on the plan, lines 116 to 120): every so often a script calls an agent
to read the repository and analyse three things.

1. Whether the principles are followed, and whether they are useful: whether they are used. A
   principle can be irrelevant, guiding no decision at all.
2. Whether the principles fail: whether one conflicts with itself or with another, documenting how
   it happens.
3. Whether there are new principles in the documents or in the repository that aren't listed, whether
   they conflict with the current ones, and the costs and benefits of including them.

Decision D-2026-10-06-o (the principles audit asks these three questions, run by a script). The
first question gives P13 (a principle is worth the decisions it guides). Section 1 adds a fourth
thing for the same audit to look for: drift, a run of local decisions that adds up to a change that
isn't local.

How it runs: `prompts/audit_principles_v1.md` and `scripts/audit_principles.py`. Inputs:
`docs/principles.md`, `docs/decisions.md`, the commits since the previous audit, and the documents
changed since then. Output: for each principle, the decisions that invoked it, for or against; the
conflicts found; the candidate principles, with their assumption and the cost and benefit of adding
them. Calibration: the principles drafted in Appendix B that come from Luciano's words were found
by hand in a small part of the sources, so the first run on the same sources should find them again.

When it runs, the bite for Luciano. "Cada tanto" admits three readings: a fixed calendar (cron), a
count of commits, or a milestone. The proposal is a milestone: before each push of `main` to GitHub,
and whenever he asks. A calendar spends tokens whether or not anyone will read the output, which goes
against P8 (no more bureaucracy than it pays for) and P12 (Luciano's attention is the scarce
resource). A milestone is when he has to read anyway.

**5.3 Q3, the part of the correspondence audit that needs a model.** Model's margin. Rules whose text
and tests disagree; behavior of the implementation that no rule covers.

## Phase 6. The list of working method §12 (what is out of place today)

Each item is a logged decision with its own commit.

| Item | What | Who decides |
|---|---|---|
| 1 | Commit `Lucianos feedbacks/` and `funcion de los tipos en Luthier.txt` in sonolocalización | Luciano: they are his files, and may be untracked on purpose |
| 2 | Add the commit to the citations of item 1 | the model, after item 1 |
| 3 | The certification logs of 2026-10-05/06 | the model: a note in `plan-2026-10-06.md` saying they are gone, unless Luciano has them |
| 4 | Decision log and principles | phase 1 |
| 5 | The notes at the end of `lib/random.lut` | Luciano (working method §13, open questions) |
| 6 to 8 | Moving the surveys of prior art and the answers of other models | the model, one commit each, references updated in the same commit |
| 9 | R10 (a law characterizes; a second implementation is not a law) without a test | the next round of the interpreter; step 4.2 reports it |
| 10 | `CLAUDE.md` | step 2.1 |
| 11, 12 | Git for the memory and the transcripts; manifests | steps 2.3 and 3.1 |
| 13 | The working method names principles, sections and kinds by letter or number without their statement | the model: apply D-2026-10-06-l (numbered references carry their statement) to it, in one commit |

## 7. What this plan needs from Luciano

Each item is one bite.

1. **The principles of Appendix B**: `ok` on the ones you recognize as yours, a correction on the
   rest. Thirteen sentences. This starts phase 1.
2. **The five new decisions of Appendix B**: the chat exports go to GitHub; in documents for you a
   numbered reference carries its statement; what a step is; `CLAUDE.md` without meta-information;
   the three questions of the principles audit. Check that they say what you said.
3. **Chat exports in a public repository** (step 1.1): you read each export before committing it, and
   sessions on sonolocalización's private matters go to its private repository. Yes or no.
4. **When the principles audit runs** (step 5.2): before each push of `main`, and on request. Yes, or
   another trigger.
5. **The questions of working method §13 (open questions)** remain: whether principles and conflicts
   between them are yours on top of safety; whether a checked quote is enough to confirm a decision;
   whether each repository needs a list of references.

## Appendix A. Fidelity of the working method, by hand

The first application of Q1 (the fidelity audit), to `docs/working-method.md` at `ed8052a`. One row
per rule or claim. "Bundle" means confirmed only by "Si." (chat, line 227), which answered a proposal
of several parts at once.

| Section of the working method | Rule or claim | Origin |
|---|---|---|
| §1 (what the structure is for) | The three questions the structure is for | Luciano, annotation on the method, lines 309 to 314 |
| §1 | Luciano's part must be discernible | Luciano, line 74 |
| §1 | The fidelity audit runs in two directions (lost, and attributed without a source) | the model, elaborating line 310 |
| §2 (two repositories) | Each repository is self-contained | Luciano, line 303 |
| §2 | Notes stay where Luciano wrote them | Luciano, line 305 |
| §2 | Citation across repositories as `repo@commit:path`, plus a quote | the model |
| §3 (everything derived carries its derivation) | The chain of derivation; the key rule | Luciano, lines 96 and 97 |
| §3 | Deterministic links against links through a model | the model |
| §3 | A correction keeps the original and puts the best reading in front | Luciano, lines 60 and 61 |
| §3 | The sibling file `.orig` when nothing was committed | the model |
| §4 (the kinds of material) | Classes by authorship | Luciano, line 74, for the axis; the letters, the model |
| §4 | Luciano's sources are primary material; what to do with them depends | Luciano, line 45 |
| §4 | Luciano's sources stay in their language | the model, confirmed by Luciano: "true", line 65 |
| §4 | Luciano's sources are committed before anything cites them | the model, confirmed by Luciano: "ok", line 67 |
| §4 | A chat with a model is mixed: the questions are his | Luciano, line 73 |
| §4 | The rules for others' sources, data, specification, implementation, tools, results | the model, with no comment from Luciano |
| §4 | A document of elaboration marks, idea by idea, what is sourced and what is proposed | the model, answering line 109 |
| §5 (principles) | Principles as a kind of their own | the model, from line 234 |
| §5 | A free choice is a valid principle | Luciano, line 235 |
| §5 | Principles stay proposed until his mark | the model |
| §5 | Decisions may follow a likelihood principle | Luciano, line 234 |
| §5 | Start with the sign of the effect, numbers later | the model |
| §6 (decisions) | A model decides, following principles | Luciano, lines 44 and 234 |
| §6 | Luciano keeps safety | Luciano, line 234 |
| §6 | Luciano also keeps principles and conflicts between them | the model, open in §13 |
| §6 | The model reports the principles touched at each decision | Luciano, line 236 |
| §6 | One log per repository; both when a decision affects both | Luciano, line 302 |
| §6 | A rationale may be "because I wanted it so" | Luciano, chat, line 68 |
| §6 | The format of an entry; the four kinds of rationale | the model |
| §6 | Confirmation by a checked quote; his mark only for principles | the model, answering line 306; open in §13 |
| §7 (the model's part in view) | What he hasn't understood must be contained | Luciano, line 110 |
| §7 | The four mechanisms of containment | the model |
| §8 (reversibility) | The loophole; commit before every change makes decisions reversible | Luciano, chat, line 196 |
| §8 | Detection latency as the real cost; the five rules | the model, bundle |
| §8 | Push only tagged milestones | the model, bundle |
| §8 | What git doesn't revert | the model, bundle |
| §8 | What is ignored for size needs its own treatment | Luciano, chat, line 220 |
| §8 | The three cases of large files; the git for large data | the model, bundle |
| §9 (specification and implementation) | Implementing brings out problems and questions | Luciano, line 171 |
| §9 | The same form applies to the analysis of data | Luciano, line 170 |
| §9 | The route back from implementation to specification | the model |
| §10 (the audits) | Audits by prompt, in the style of the ideas pipeline | Luciano, line 309; the design, the model |
| §11 (common rules) | The header | the model |
| §11 | Who runs what | Luciano, in rules of earlier sessions kept in memory files outside git |
| §11 | Language | Luciano, rule of 2026-10-01, kept in a memory file outside git |
| §12 (what is out of place today) | The findings | the model, facts that can be checked |

Line numbers without a source are annotations on the method.

Count, by script over the 46 rows: 24 have Luciano as origin (two of them with a part by the model),
2 are proposals he confirmed explicitly, 20 are proposals of the model, 4 of those confirmed only in a
bundle. The rows where he is the origin are the ideas: what the structure is for, authorship,
derivation, principles, reversibility. Most of the model's rows are mechanics: formats, the header,
the rules of the minor kinds. That's the expected split, and it is also what working method §7 (the
model's part in view) warns about. Mechanics read as neutral, and so get accepted without being
looked at.

Two of his rules (who runs what, language) rest on memory files outside git, whose original words
were said in other sessions. Step 2.3a versions the memory from now on; the earlier words would need
the export of step 1.1 run on those sessions.

## Appendix B. Draft entries for the principles and the log

For Luciano to mark. Once marked, phase 1 moves them to `docs/principles.md` and `docs/decisions.md`,
where they can be terse. Quotes are verbatim, typos included. Sources of the form `@2a660c8` are
annotations on the method, `@daa5b95` annotations on the plan, both in this repository.

### Principles

```
P1  Luciano's part stays discernible.
Quote:      "the idea of course is that this project is generated by a human and the human
            signature has to be distinctive (discernible), otherwise it is just IA generated
            content with not particular value, but as such."
Source:     luthier@2a660c8:docs/working-method.md:74
Assumption: the value of the project lies in what he contributes, and that part can be told
            apart at a cost the project can bear.
Status:     proposed

P2  Everything derived carries how it was derived.
Quote:      "Well theres is raw data and its chains of interpreatations, all with proper chains
            of how they were generated, so we can generate again the same analysis or data
            processing."
Source:     luthier@2a660c8:docs/working-method.md:96
Assumption: recording the chain costs less than reconstructing a result whose origin was lost.
Status:     proposed

P3  Keep the original evidence and its corrections; put the best reading in front.
Quote:      "The principle is of keeping the original evidence an its correction path but
            surfacing the best interpreatation possible."
Source:     luthier@2a660c8:docs/working-method.md:61
Assumption: keeping is cheap next to losing evidence. (The disk at 97% puts a limit on it.)
Status:     proposed

P4  Decisions follow guiding principles, found as the work goes.
Quote:      "en realidad la decision no deberia ser tomada por Luciano (salvo cuestiones de
            seguridad), sino de acuerdo a ciertos principios rectores que vamos descubriendo a
            medida que vamos avanzando."
Source:     luthier@2a660c8:docs/working-method.md:234
Assumption: a few principles explain most decisions. If every decision needs a reason of its
            own, the principles compress nothing.
Status:     proposed

P5  A free choice is a legitimate principle, for Luciano and, within margins, for a model.
Quote:      "un ppio rector puede ser a veces Luciano hace lo que se le canta (y a veces la IA
            tambien, con margenes definidos), de hecho la estoscasticidad es necesaria para
            ciertos tipos de optimizaciones o al menos es un ppio valido."
Source:     luthier@2a660c8:docs/working-method.md:235
Assumption: free choices are cheap to undo, by P6 (every change can be undone).
Status:     proposed

P6  Every change can be undone.
Quote:      "si siempre comiteamos antes de aplicar un cambio, en principio toda decision es
            reversible y si los efetos inesperados aparecen y los detecto, siempre se puede
            volver atras y rectificar."
Source:     chat 7217f251, line 196
Assumption: unexpected effects are detected before much is built on them (working method §8,
            reversibility).
Status:     proposed

P7  Each repository is self-contained.
Quote:      "ese seria el criterio: cada repositorio es autocontenido, aunque para evitar
            duplicacion se pueden citar los documentos de uno al otro o algo similar"
Source:     luthier@2a660c8:docs/working-method.md:303
Assumption: the repositories will be read apart: by another person, another session, a release.
Status:     proposed

P8  No more bureaucracy than it pays for.
Quote:      "(sin irnos a la mierda en la burocracia)"
Source:     luthier@2a660c8:docs/working-method.md:306
Assumption: every mechanism costs less than what it prevents. This plan is the first thing to
            judge against it.
Status:     proposed

P9  What Luciano hasn't fully understood may come in, contained.
Quote:      "sometimes some ideas of the AI are not fully understood by Luciano so the human
            oversight is compromised. Thats tolerable, but has to be contained."
Source:     luthier@2a660c8:docs/working-method.md:110
Assumption: what can't be understood can at least be located.
Status:     proposed

P10 The mathematical object that best represents a concept is the invariant of its type.
Source:     docs/semantica/07-characterizations.md, "Principle (Luciano, 2026-10-05)". A document
            of the model citing him: the chain stops one link short of his words.
Status:     in force since 2026-10-05; source to pin

P11 Every criterion is a parameter, never a constant in the code.
Source:     memory of sonolocalización, nunca-hardcodear.md (2026-09-11), outside git; rule 1 of
            plan-mechanical-rules.
Status:     in force since 2026-09-11; source to pin

P12 Luciano's attention is the scarce resource.
Quote:      "La limitante aqui es mi capacidad de procesamiento de informacion"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:37
Assumption: what the model produces grows faster than what he can read, so every document,
            step and audit is sized to his reading, and the rest is the model's margin.
Status:     proposed, new

P13 A principle is worth the decisions it guides.
Quote:      "si los principios se cumplen y si son utiles (es decir si se usan, un principio
            puede ser irrelevante, no servir para guiar o tomar ninguna decision)"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:117
Assumption: the use of a principle can be read from the record of decisions.
Status:     proposed, new
```

### Decisions

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
Quote:      "true" (line 65), "ok" (line 67)
Source:     luthier@2a660c8:docs/working-method.md:65, :67
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
Source:     chat 7217f251, line 196
Kind:       principle. For P6 (every change can be undone), P5 (a free choice is legitimate),
            since it is what makes free choices cheap
Status:     current

D-2026-10-06-g  A model takes decisions within margins, following principles; Luciano keeps
                safety.
Author:     Luciano
Quote:      "The agent has to make decisions otherwise it will be stuck." (line 44);
            "salvo cuestiones de seguridad" (line 234)
Source:     luthier@2a660c8:docs/working-method.md:44, :234
Kind:       principle. For P4 (decisions follow guiding principles), P5 (a free choice is
            legitimate); against P9 (what he hasn't understood may come in, contained) unless
            the end-of-task report of step 2.1 is kept
Status:     current for this part. That Luciano also keeps principles and the conflicts
            between them is the model's addition, proposed (working method §13).

D-2026-10-06-h  Reversibility, the parts of working method §8 that "Si." confirmed as a bundle.
Author:     the model
Quote:      "Si."
Source:     chat 7217f251, line 227
Kind:       principle. For P6 (every change can be undone), P2 (everything derived carries how
            it was derived), P3 (keep the original and its corrections)
Status:     by part:
            - one decision per commit: proposed
            - a reversal keeps its entry as a datum: proposed
            - the model's margin is what can be undone before Luciano next looks: replaced by
              the criterion of plan §1 (a decision is local when one commit undoes it and
              nothing depends on it yet), proposed
            - push only tagged milestones: proposed
            - local git for the memory: confirmed, "Ok", luthier@daa5b95:...:195
            - local git for the oral transcriptions, text only: confirmed, same line
            - manifests for raw data: confirmed, "ok", luthier@daa5b95:...:208
            - git outside the folder for large derived data: deferred, "ok",
              luthier@daa5b95:...:219

D-2026-10-06-i  The git for large data keeps its repository outside the folder it tracks.
Author:     the model, decided by the implementation
Kind:       case: sonolocalización tracks 234 files under prototipo-cero/2026-09-07/derived/
Status:     current, and deferred by step 3.2

D-2026-10-06-j  A document for Luciano is committed before he annotates it.
Author:     the model
Kind:       case: his annotations on draft 0 of the method had to be separated from the model's
            text by rebuilding draft 0 from the transcript; on this plan they came as a diff
Principles: for P1 (Luciano's part stays discernible), P8 (no more bureaucracy than it pays for)
Status:     proposed

D-2026-10-06-k  The chat exports go to GitHub.
Author:     Luciano
Quote:      "I think that the chat exports should be in GItHub because they are the ultimate
            proof (the audios) of the ideas origin."
Source:     chat 7217f251, line 366
Kind:       principle. For P1 (Luciano's part stays discernible)
Status:     current; how, in plan §7, item 3

D-2026-10-06-l  In a document for Luciano, a numbered reference carries its statement; records
                may be terse.
Author:     Luciano
Quote:      "Fijate la idea de que documentos que yo voy a consumir no pueden referir a
            principios con numero porque no se de que me estas hablando." (line 366);
            "Documentos que son de registro pueden ser sintenticos, eso se aplica para los que
            son de mi consumo" (line 382)
Source:     chat 7217f251, lines 366 and 382
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
Author:     Luciano; the trigger is proposed by the model (plan step 5.2)
Quote:      "Aqui la idea es que cada tanto un script llame a leer el repositorio a un agente y
            que analice dos cosas"
Source:     luthier@daa5b95:docs/plan-working-method-2026-10-06.md:116
Kind:       principle. For P4 (decisions follow guiding principles), P13 (a principle is
            worth the decisions it guides)
Status:     current; trigger proposed
```
