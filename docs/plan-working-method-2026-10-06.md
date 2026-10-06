# Plan: putting the working method into practice, 2026-10-06

Draft 0, 2026-10-06. Status: proposed. Phase 0 is done; nothing after it has started.

Written for Luciano, and for the sessions that will execute it. It assumes no memory of the
conversation that produced it; everything needed is here or in the files named.

Sources:

- `docs/working-method.md` at `ed8052a`, cited as WM §n.
- Luciano's annotations on draft 0 of it, commit `2a660c8`, cited as "annotation, line n" (the line
  of `docs/working-method.md` at that commit).
- Luciano's turns in Claude Code session `7217f251`
  (`~/.claude/projects/-home-lmoffatt-Projects-luthier/7217f251-afdd-4548-8d5d-2cf7468c47d4.jsonl`),
  cited as "chat, line n", the line of that transcript. The file only grows, so the line is stable;
  step 1.1 copies the turns into the repository.
- `docs/plan-mechanical-rules-2026-10-06.md`, written by another session the same day. It is
  untracked, so it is cited by path and can't be pinned until it is committed.
- Measurements of 2026-10-06: `/home` is 97% full (56 GB free); `~/Projects/Oral transcriptions` is
  2.7 GB (1509 `.md`, 1149 `.mp3`, 967 `.ogg`); sonolocalización tracks 234 files under
  `prototipo-cero/2026-09-07/derived/`.

## How this plan applies the method to itself

- **Origin marks.** [L] is Luciano's, with its source. [M] is the model's proposal. [M; L "..."] is a
  proposal Luciano confirmed, with his words. Appendix A applies the same marks to the working method
  itself.
- **Every step is a decision** and carries the fields of WM §6: origin; principles it touches (the
  drafts P1 to P11 of Appendix B), for or against; the assumption it leans on; who runs it; how it is
  undone; what detects its unexpected effects; its cost; when it is done. Cost is there because of P8,
  no more bureaucracy than it pays for. Every step of this plan is a candidate for violating it.
- **One step, one commit** (WM §8).
- **This plan is committed before Luciano reads it**, so that his annotations on it are
  `git diff` against that commit.

## 1. The order, and why

The method needs pieces that don't exist yet: a decision log, a list of principles, a check of
quotes, a copy of the chat in the repository. Each phase builds what the next one needs. Until a
piece exists, its job is done by hand, and the plan says where.

| Phase | What | Needs | Cost |
|---|---|---|---|
| 0 | Pin the sources | nothing | done |
| 1 | The record: chat export, principles, decisions | 0 | half a day, plus Luciano's reading of Appendix B |
| 2 | The model's conduct: `CLAUDE.md`, the end-of-task report, memory under git | 1 (principles to report against) | two hours |
| 3 | Data: manifests | nothing | one hour |
| 4 | Mechanical checks: quotes, specification against tests | 1 (a log to check) | half a day |
| 5 | Audits by prompt: Q1 and Q2 | 1, and the hand results of Appendices A and B to calibrate | a day, plus the runs |
| 6 | The list of WM §12 | 1 (each fix is a logged decision) | an hour per item |

Phase 3 can run in parallel with anything. Phase 5 runs after Luciano has annotated Appendix B,
because Appendix B is what its prompts are calibrated against.

## Phase 0. Pin the sources (done)

**0.1 Three commits for the working method.** `bf05457` is draft 0, recovered verbatim from the
Write call that created it (chat, line 116, 03:39 UTC). `2a660c8` is Luciano's annotations. Before
committing, the diff between the two was checked to contain only his added lines and trailing spaces
he added to three of mine. `62ac538` is draft 1, whose header now cites the two commits instead of
the copy of the annotated file kept while nothing was committed.

- Origin: [M], applying WM §3 and annotation line 61 ("keeping the original evidence an its
  correction path").
- Principles: for P1, P2, P3.
- Undo: `git reset --soft 21aa9c9` puts the three back in the working tree.

**0.2 Correction of WM §8** (`ed8052a`). Draft 1 proposed a nested git inside
`prototipo-cero/2026-09-07/`; sonolocalización already tracks files there, so the repository for
large data has to live outside the folder. Marked in §8 as decided by the implementation.

**0.3 This plan**, committed on its own.

**Finding.** Committing a B before Luciano annotates it makes his part a diff: `git diff bf05457
2a660c8` is exactly what he wrote, separated from what the model wrote at no cost. In this session
the separation had to be rebuilt from the transcript. Proposal [M] for WM §11: a B is committed before
it goes to Luciano. Principles: for P1, P8 (the cheapest mechanism for P1 found so far). Draft entry
D-2026-10-06-j in Appendix B.

## Phase 1. The record

**1.1 Luciano's chat turns, exported.** `scripts/export_chat_turns.py <session.jsonl>` writes
`docs/chat/<date>_<session8>.md`: his turns verbatim, each with its timestamp and its line in the
transcript. Text inserted by the harness (`<system-reminder>`, `<ide_opened_file>`, the output of
local commands) is dropped. Text he pasted (`<pasted_content>`) is kept and marked as pasted, since
it may not be his. The frontmatter is written by Python: session id, sha256 of the transcript, number
of turns. A deterministic link (WM §3).

- Origin: [M; L "Si." chat, line 227], implementing WM §8, "decisions taken in chat copy the message
  into the repository".
- Principles: for P1, P2.
- Assumption: the transcript format of Claude Code stays readable. It is internal and may change; the
  script fails loudly on a line it can't parse.
- Who runs it: Luciano, since it processes the record of the project (WM §11).
- Undo: one commit. Detects: 4.1 fails when a quote is missing from the export.
- Done when: the export of session `7217f251` has nine turns and holds every chat quote of
  Appendix B.
- Caveat: exposure. A chat may hold things that shouldn't reach GitHub, and WM §8 pushes `main` at
  milestones. Question for Luciano in section 7.

**1.2 `docs/principles.md`**, from Appendix B after Luciano has annotated it. Entries stay `proposed`
until he writes `ok` on them; a model never writes it (WM §6).

- Origin: [M], from WM §5, which comes from annotation line 234.
- Principles: for P4; against P8 (one more file to keep up).
- Assumption: a principle can be stated in a sentence, with one assumption.
- Who runs it: the model writes, Luciano marks.

**1.3 `docs/decisions.md`**, from Appendix B, in the format of WM §6 with one change found while
drafting the appendix: `Source:` carries the line, `path@commit:line`. Two of Luciano's confirmations
are one word ("true", "ok", annotation lines 65 and 67), and a one-word quote can't be checked by
searching the file for it.

- Origin: [L] annotations, lines 302 and 306; format [M].
- Principles: for P1, P4.
- Assumption: entries get written when the decision is taken. Rebuilt afterwards, as Appendix B
  does, they cost an hour of transcript reading per session.

**1.4 Sonolocalización.** `docs/decisions.md` and `docs/principles.md` at its root (a new `docs/`
folder). The decisions about the method get a short entry there with a reference to Luthier's log
(WM §6). The method itself isn't copied: sonolocalización's `CLAUDE.md` cites
`luthier@<commit>:docs/working-method.md`.

- Origin: [L] annotation, line 303: "para evitar duplicacion se pueden citar los documentos de uno
  al otro".
- Principles: for P7.

## Phase 2. The model's conduct

**2.1 `CLAUDE.md`.** A new one in Luthier. In sonolocalización, lines added to the file that phase
6.2 of `plan-mechanical-rules` writes, so there are no two competing files. Content, a line each:

- read `docs/working-method.md` before working;
- before a decision that isn't routine, say which principles it touches, in which direction, and the
  assumption it leans on (WM §6);
- commit before changing; one decision, one commit (WM §8);
- at the end of each task, list the decisions taken within margins, unasked (WM §8);
- in a B, mark what comes from a source and what the model proposes (WM §4);
- commit a B before it goes to Luciano (D-2026-10-06-j).

- Origin: [M], from WM §6 and §8; the report of principles at each decision is [L] annotation, line
  236.
- Principles: for P1, P6, P9.
- Assumption: written instructions hold. `plan-mechanical-rules` reports that they degrade over a
  long run (the constant `lmMaxIter`, night of 2026-10-05), which is why 2.2 and phase 4 exist.

**2.2 Reminder at the end of a turn.** A `Stop` hook, next to the one of `plan-mechanical-rules`
2.2, prints the commits of the session that touch D or E and that no entry of the log names. It
doesn't block: not every commit is a decision.

- Origin: [M]. Principles: for P6, P9; against P8 if it fires on routine commits, in which case it
  goes.
- Who runs it: the hook.

**2.3 Local git for what git doesn't cover** (WM §8).

- The memory of each project (`~/.claude/projects/<project>/memory/`): `git init`, a first commit of
  its current state, and a `Stop` hook that commits whatever changed there during the turn. Then
  `git log -p` in that folder shows what the model wrote about Luciano and about the project, at the
  one place where a misread principle survives any revert of the repository.
- `~/Projects/Oral transcriptions/`: `git init` tracking only the text (`*.md`, `*.txt`). The audio
  (2.7 GB, and a disk at 97%) goes in a `manifest.sha256` committed with the text. Transcripts are
  what gets corrected (WM §3), and audio never changes.

- Origin: [M; L "Si." chat, line 227]. That "Si." confirmed a bundle of five rules and three
  proposals at once, the case of WM §7. D-2026-10-06-h in Appendix B lists the parts so he can confirm them one by
  one.
- Principles: for P2, P3, P6, P9.
- Who runs it: the model (`git init` processes nothing).
- Undo: deleting the `.git` folder leaves the memory and the transcripts as they were.
- Cost: minutes.

## Phase 3. Data

**3.1 Manifests in sonolocalización.** `prototipo-cero/2026-09-07/manifest.sha256` and
`audio-campo/manifest.sha256`, covering every file the parent repository ignores there (`*.wav`,
`*.zip`, `*.npz`), committed. `sha256sum -c --quiet` goes into `lint/full.sh` of
`plan-mechanical-rules`.

- Origin: [M; L "Si." chat, line 227], WM §8, raw data needs integrity.
- Principles: for P2, P3.
- Who runs it: the model; hashing is a check and produces no result.
- Cost: minutes (about 5 GB of hashing).

**3.2 The git for large data, deferred.** WM §8 proposes a repository outside the folder, holding the
raw data once and the derived data per run. With the disk at 97% it would take 5 GB that aren't
there, and it would protect the derived `.npz` files, which can be produced again from code and
arguments. Recommendation [M]: don't do it until there is a derived file that is expensive to
produce again and changes between runs. The manifest of 3.1 covers the raw data.

- Principles: for P8; against P2 only for results that are expensive to produce again, of which there
  are none today.

## Phase 4. Mechanical checks

**4.1 `scripts/check_quotes.py`.** For every entry of `docs/decisions.md` and `docs/principles.md`
whose author is Luciano: it has `Quote:` and `Source: path@commit:line`, and the quote is in that
line or the lines after it of `git show commit:path`, with whitespace normalized. Chat sources are
read from the exports of 1.1. A source in the other repository is read with `git -C`. If that
repository is absent, the check warns and doesn't fail (P7). Output in the format of
`plan-mechanical-rules`: `path:line: rule: message`, exit 1 on findings.

- Origin: [M], answering annotation line 306: "una revision de algun modo certificada quizas? (sin
  irnos a la mierda en la burocracia)".
- Principles: for P1; for P8 (a script instead of a ritual).
- Who runs it: the model and the hooks, like a lint.

**4.2 `scripts/check_spec_tests.py`.** The rules `R1` to `R11` of `05-static-semantics.md` against
the names of the files of `tests/spec/`: each rule needs an `.accept.lut` and a `.reject.lut`, and a
rule marked "not implemented" is reported as such. Expected output today: R10 has no test; R11 is
not implemented. The mechanical part of Q3 (WM §10).

- Origin: [L] annotation, line 313, "La implementacion es fiel a la especificacion?"; the check [M].
- Who runs it: the model and the hooks.

**4.3 Header check, as a warning.** A B or D dated 2026-10-06 or later has the four items of the
header of WM §11. Older documents are listed in an allow file.

- Principles: for P1; against P8 if it turns into form-filling. The first time it flags a document
  whose header was fine for a human reader, it goes.

## Phase 5. Audits by prompt (Luciano runs them)

Each one is a prompt in `prompts/` and a script in `scripts/`, in the style of `extract_ideas.py`.
Outputs go to `docs/audits/<date>_<audit>_<prompt version>_<model>.md`.

**5.1 Q1, fidelity.** `prompts/audit_fidelity_v1.md`. First target: `docs/working-method.md` at
`ed8052a`, against its sources (`2a660c8`, the export of the chat). Appendix A is the same audit done
by hand. If the prompt and Appendix A disagree, find out which one is right before the prompt is used
on anything else.

**5.2 Q2, principles.** Two prompts. The first extracts candidate principles, each with its
assumption, from A1: the transcripts in `docs/audios/`, `Lucianos ideas`, the feedback files,
annotations recovered as diffs, the chat exports. It should find P1 to P9 of Appendix B again, which
come from a small part of A1, and others from the voice notes. The second takes a range of commits
and gives the effect of each one on each principle. First range: the phases of
`plan-2026-10-05.md`.

**5.3 Q3, the part for a model.** Rules whose text and tests disagree; behavior of the
implementation that no rule covers.

- Origin: [L] annotation, lines 309 to 314; the design [M].
- Principles: for P1, P4; P8 is at risk if the audits are run more often than someone reads them.
- Assumption: a model can tell Luciano's ideas from its own in a document that blends them. Appendix
  A is the test of that assumption.

## Phase 6. The list of WM §12

Each item is a logged decision with its own commit.

| Item | What | Who decides |
|---|---|---|
| 1 | Commit `Lucianos feedbacks/` and `funcion de los tipos en Luthier.txt` in sonolocalización | Luciano: they are his files, and may be untracked on purpose |
| 2 | Add the commit to the citations of item 1 | the model, after 1 |
| 3 | Certification logs of 2026-10-05/06 | the model: a note in `plan-2026-10-06.md` saying they are gone, unless Luciano has them |
| 4 | Decision log and principles | phase 1 |
| 5 | Notes at the end of `lib/random.lut` | Luciano (WM §13) |
| 6 to 8 | Moves of prior art and of A2 | the model, one commit each, references updated in the same commit (today only WM cites `02-que-robar.md`) |
| 9 | R10 without a test | the next round of the interpreter, not this plan; 4.2 reports it |
| 10 | `CLAUDE.md` | 2.1 |
| 11, 12 | Git for the memory and the transcripts; manifests | 2.3, 3.1 |

## 7. What this plan needs from Luciano

- Annotate Appendix B: `ok` on the principles you recognize as yours, corrections on the rest. That
  starts phase 1.
- Chat exports and GitHub: should `docs/chat/` reach GitHub when `main` is pushed, or stay local
  (ignored, with only the hashes committed)?
- Phase 3.2, the git for large data: defer it, as recommended, or do it now?
- The questions of WM §13 remain open: the split of who decides, whether the confirmation is enough,
  and the list of references.

## Appendix A. Fidelity of `docs/working-method.md`, by hand

The first application of Q1, to the method itself, at `ed8052a`. One row per rule or claim. "Bundle"
means confirmed only by "Si." (chat, line 227), which answered a proposal of several parts at once.

| WM | Rule or claim | Origin |
|---|---|---|
| §1 | The three questions the structure is for | [L] annotation, lines 309 to 314 |
| §1 | Luciano's part must be discernible | [L] annotation, line 74 |
| §1 | Q1 runs in two directions (lost, and attributed without a source) | [M], elaborating line 310 |
| §2 | Each repository is self-contained | [L] annotation, line 303 |
| §2 | Notes stay where Luciano wrote them | [L] annotation, line 305 |
| §2 | Citation across repositories as `repo@commit:path`, plus a quote | [M] |
| §3 | Everything derived carries its derivation; the key rule | [L] annotation, lines 96 and 97 |
| §3 | Deterministic links against links through a model | [M] |
| §3 | A correction keeps the original and puts the best reading in front | [L] annotation, lines 60 and 61 |
| §3 | The sibling file `.orig` when nothing was committed | [M] |
| §4 | Classes by authorship | [L] annotation, line 74, for the axis; the letters [M] |
| §4 | A1 is primary material; what to do with it depends | [L] annotation, line 45 |
| §4 | A1 stays in its language | [M; L "true", annotation line 65] |
| §4 | A1 is committed before anything cites it | [M; L "ok", annotation line 67] |
| §4 | A chat with a model is mixed: the questions are his | [L] annotation, line 73 |
| §4 | The rules of A2, A3, D, E, F, G | [M], with no comment from Luciano |
| §4 | A B marks, idea by idea, what is sourced and what is proposed | [M], answering line 109 |
| §5 | Principles as a kind of their own | [M], from line 234 |
| §5 | A free choice is a valid principle | [L] annotation, line 235 |
| §5 | Principles stay proposed until his mark | [M] |
| §5 | Decisions may follow a likelihood principle | [L] annotation, line 234 |
| §5 | Start with the sign of the effect, numbers later | [M] |
| §6 | A model decides, following principles | [L] annotation, lines 44 and 234 |
| §6 | Luciano keeps safety | [L] annotation, line 234 |
| §6 | Luciano also keeps principles and conflicts between them | [M], open in WM §13 |
| §6 | The model reports the principles touched at each decision | [L] annotation, line 236 |
| §6 | One log per repository; both when a decision affects both | [L] annotation, line 302 |
| §6 | A rationale may be "because I wanted it so" | [L] chat, line 68 |
| §6 | The format of an entry; the four kinds of rationale | [M] |
| §6 | Confirmation by checked quote; his mark only for principles | [M], answering line 306; open in WM §13 |
| §7 | What he hasn't understood must be contained | [L] annotation, line 110 |
| §7 | The four mechanisms of containment | [M] |
| §8 | The loophole; commit before every change makes decisions reversible | [L] chat, line 196 |
| §8 | Detection latency as the real cost; the five rules | [M], bundle |
| §8 | Push only tagged milestones | [M], bundle |
| §8 | What git doesn't revert | [M], bundle |
| §8 | What is ignored for size needs its own treatment | [L] chat, line 220 |
| §8 | The three cases; the git for large data | [M], bundle |
| §9 | Implementing brings out problems and questions | [L] annotation, line 171 |
| §9 | The same form applies to the analysis of data | [L] annotation, line 170 |
| §9 | The route back from implementation to specification | [M] |
| §10 | Audits by prompt, in the style of the ideas pipeline | [L] annotation, line 309; the design [M] |
| §11 | The header | [M] |
| §11 | Who runs what | [L] in rules of earlier sessions, kept in memory files outside git |
| §11 | Language | [L] rule of 2026-10-01, kept in a memory file outside git |
| §12 | The findings | [M], facts that can be checked |

Count, by script over the 46 rows: 24 have Luciano as origin (two of them with a part by the
model), 2 are proposals he confirmed explicitly, 20 are proposals of the model, 4 of those confirmed
only in a bundle. The rows where he is the origin are the ideas: what
the structure is for, authorship, derivation, principles, reversibility. Most of the model's rows are
mechanics: formats, the header, the rules of the minor kinds. That's the expected split, and it is
also what WM §7 warns about. Mechanics read as neutral, and so get accepted without being looked at.

Two of his rules (who runs what, language) rest on memory files outside git, whose original words
were said in other sessions. Step 2.3 versions the memory from now on; the earlier words would need
the export of 1.1 run on those sessions.

## Appendix B. Draft entries for the principles and the log

For Luciano to annotate. Once annotated, phase 1 moves them to `docs/principles.md` and
`docs/decisions.md`. Quotes are verbatim, typos included.

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
Assumption: free choices are cheap to undo (P6).
Status:     proposed

P6  Every change can be undone.
Quote:      "si siempre comiteamos antes de aplicar un cambio, en principio toda decision es
            reversible y si los efetos inesperados aparecen y los detecto, siempre se puede
            volver atras y rectificar."
Source:     chat 7217f251, line 196
Assumption: unexpected effects are detected before much is built on them (WM §8).
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

P10 Find the mathematical object that best represents each concept and make it the invariant
    of the type.
Source:     docs/semantica/07-characterizations.md, "Principle (Luciano, 2026-10-05)". A B citing
            him: the chain stops one link short of his words.
Status:     in force since 2026-10-05; source to pin

P11 Every criterion is a parameter, never a constant in the code.
Source:     memory of sonolocalización, nunca-hardcodear.md (2026-09-11), outside git; rule 1 of
            plan-mechanical-rules.
Status:     in force since 2026-09-11; source to pin
```

### Decisions

```
D-2026-10-06-a  Material is classed by authorship, in the kinds A1 to G of WM §4.
Author:     Luciano for the axis; the model for the scheme
Quote:      "And authority is somewhat too much"
Source:     luthier@2a660c8:docs/working-method.md:74
Kind:       principle. Principles: for P1
Status:     proposed (the scheme hasn't been discussed)
Landed in:  WM §4, 62ac538

D-2026-10-06-b  One decision log per repository; a decision that affects both goes in both.
Author:     Luciano
Quote:      "un decision log per repository, decisiones que afectan a ambos se ponen en ambos."
Source:     luthier@2a660c8:docs/working-method.md:302
Kind:       principle. Principles: for P7
Status:     current
Landed in:  WM §6, 62ac538

D-2026-10-06-c  A1 stays in its language and is committed before anything cites it.
Author:     the model, confirmed by Luciano
Quote:      "true" (line 65), "ok" (line 67)
Source:     luthier@2a660c8:docs/working-method.md:65, :67
Kind:       principle. Principles: for P1, P2
Status:     current
Landed in:  WM §4, 62ac538

D-2026-10-06-d  Luciano's notes stay where he wrote them, as part of A.
Author:     Luciano
Quote:      "Mis notas (como estas) se quedan donde estan, pero forman parte de A"
Source:     luthier@2a660c8:docs/working-method.md:305
Kind:       free ("estoy abierto a sugerencias", same line)
Status:     current
Landed in:  WM §2, §4, 62ac538

D-2026-10-06-e  A correction keeps the original and puts the corrected version in front.
Author:     Luciano
Quote:      "In this case we might, store the old version and replace it with the correction
            with a note at the begining of the document."
Source:     luthier@2a660c8:docs/working-method.md:60
Kind:       principle. Principles: for P3
Status:     current
Landed in:  WM §3, 62ac538

D-2026-10-06-f  Every change is applied on top of a commit.
Author:     Luciano
Quote:      "si siempre comiteamos antes de aplicar un cambio, en principio toda decision es
            reversible"
Source:     chat 7217f251, line 196
Kind:       principle. Principles: for P6, P5 (it is what makes free choices cheap)
Status:     current
Landed in:  WM §8, 62ac538

D-2026-10-06-g  A model takes decisions within margins, following principles; Luciano keeps
                safety.
Author:     Luciano
Quote:      "The agent has to make decisions otherwise it will be stuck." (line 44);
            "salvo cuestiones de seguridad" (line 234)
Source:     luthier@2a660c8:docs/working-method.md:44, :234
Kind:       principle. Principles: for P4, P5; against P9 unless the report of 2.1 is kept
Status:     current for this part. That Luciano also keeps principles and the conflicts between
            them is the model's addition, proposed (WM §13).
Landed in:  WM §6, 62ac538

D-2026-10-06-h  Reversibility, the parts of WM §8 that "Si." confirmed as a bundle: one decision
                per commit; a reversal keeps its entry as a datum; the margin of a model is what
                can be undone before Luciano next looks; push only tagged milestones; local git
                for the memory and the transcripts; manifests for raw data; a git outside the
                folder for large derived data.
Author:     the model
Quote:      "Si."
Source:     chat 7217f251, line 227
Kind:       principle. Principles: for P6, P2, P3; P8 at stake in the last part (see 3.2)
Status:     proposed, part by part: Luciano marks each part he confirms
Landed in:  WM §8, 62ac538 and ed8052a

D-2026-10-06-i  The git for large data keeps its repository outside the folder it tracks.
Author:     the model, decided by the implementation
Kind:       case: sonolocalización tracks 234 files under prototipo-cero/2026-09-07/derived/
Status:     proposed; deferred by 3.2 in any case
Landed in:  WM §8, ed8052a

D-2026-10-06-j  A B is committed before it goes to Luciano for annotation.
Author:     the model
Kind:       case: in this session his annotations had to be separated from the model's text by
            rebuilding draft 0 from the transcript
Principles: for P1, P8
Status:     proposed
Landed in:  this plan, phase 0
```
