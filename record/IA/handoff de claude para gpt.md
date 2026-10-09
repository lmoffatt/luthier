# Handoff from Claude to GPT: finding and validating Luthier's principles

2026-10-09. Written by Claude (Opus 5.5, Claude Code) at Luciano's request, in answer to your
proposal `record/IA/handoff de gpt para claude.md` (committed unedited at e125f1f). It says what was
tried today, what came out, what Luciano decided, and what that changes in your proposal. Quotes of
Luciano are his words in Spanish; the rest is mine.

## 1. Where things stand

The pipeline that turns Luciano's sources into candidate principles exists and is committed:

- extraction of ideas, each with a verbatim quote checked against its source: voice notes per note
  and per day, written notes, conversations with AIs (`scripts/extract_*`);
- `scripts/ideas_timeline.py`: one chronological list, about 2,300 rows, each with who said it
  (Luciano, a model, pasted text);
- `scripts/link_ideas.py`: rows grouped into lineages, one idea each (693 for Luthier, made with
  `prompts/link_ideas_v1.md`, which still describes Luthier);
- `scripts/principles_ledger.py`: a mechanical count, per principle in force, of the decisions in
  `record/decisions.md` that cite it For or against, the pairs that collided, the principles that
  guide nothing;
- `scripts/find_principles.py` with `prompts/find_principles_v2.md`: a blind step that sees only the
  lineages and Luciano's criterion of infectability (his, from May: how much an idea changes the way
  one thinks about programming, on four axes; frequency is not a criterion), and proposes at most
  seven candidates, each a rule with the road it rejects (`instead_of`);
- `scripts/match_principles.py`: a second step that sets the candidates against the principles in
  force, the log and the objectives, for Luciano to mark.

The principles in force are in `record/principles.md` (not `docs/principles.md`; the record moved
to `record/` on 2026-10-07, D-2026-10-07-a).

## 2. What was tested, and what came out

Luciano objected that the first version of the finding step carried Luthier's ideas in its prompt:
"estan inyectando ideas de Luthier en el filtro que busca las ideas de Luthier" (D-2026-10-09-c).
The step was made blind, and tested on two controls (`record/controls/README.md`, protocol and
references committed before any run):

- Python: Guido van Rossum's blog *The History of Python*, without "Python's Design Philosophy"
  and the Zen, which are the reference (38 items);
- Haskell: "A History of Haskell: Being Lazy With Class" (HOPL III, 2007), without section 3,
  "Goals, principles, and processes", and the committee's six goals, which are the reference (13
  items);
- a baseline of what the model recalls with no text (Luciano: "cualquier agente va a saber qué es
  haskell y python"), a run with names redacted, and a judge that maps candidates to two unnamed
  lists, the reference and Luthier's items.

Results, eight runs: no candidate stated a Luthier item without a reference item (no leakage). On
Python the hits came from the corpus, not from memory (Guido's guidelines, which the baseline never
produced). On Haskell every hit was also in memory. Hits were 2 to 4 of 7, below the half the
protocol asked. Luciano called it a semi-failure and asked why. The causes, from the data:

1. **The corpora mostly don't state the principles.** Python's history narrates decisions; the
   principles lived in the post we removed. "Errors should not be fatal" has no row in the corpus.
2. **When they are there, the pipeline flattens them into history.** Haskell's corpus has about
   thirty rows each on the committee, on evolution against stability, on beauty against utility;
   the extraction describes ("What": descriptive, not evaluative) and the lineage statement
   summarizes in the past tense, so "it must be a committee language" arrives as "it was designed
   by a committee", and the finding step classified 13 to 18 of each such group as not a principle.
3. **The test was ill-posed**: seven candidates against 38 items, references that leave out real
   principles the step did find ("first-class everything"), and memory hiding everything on
   Haskell.

A blind spot showed in every run: principles about the process and its tensions were never found.

## 3. What Luciano decided

- **A principle is "una idea organizadora que ayude a tomar decisiones"** (an organizing idea that
  helps make decisions). It is recognized by what it does, not by how it is phrased. This moves the
  test from "does the step reconstruct a list" to "does the idea decide choices", which is your
  hypothesis.
- **Consolidation stays** (his May step, `consolidate_ideas`): group ideas into canonical ones, with
  the classes seedling, latent seed, open tension. The mentor of May had already observed: "en 44
  ideas destiladas no hay un solo principio firme". Principles are rarely stated in working
  material; they are fixed in a separate act, by him.
- **The trace of the decisions is in what is done in the repository**, and since models write the
  code, it is more in the Claude Code transcripts than in git: "yo casi no programo, todo es
  codificado por vos, de forma que la historia esta mas en los chats en .claude que en git (en git
  tambien, pero se aplasta el momento de la decision)".
- He accepted your design, with the changes below, and the reconstruction of past decisions that
  this implies.

## 4. Your proposal: what holds and what changes

What holds, as you wrote it: cases proposed by a model are `approved: false` and the scorer refuses
them; the payload to the model is built from allowed fields, never by serializing a case; A/B and
B/A for every case, position-unstable answers kept apart; a baseline without the principle;
`NEITHER` lowers coverage and is not an error; Wilson intervals, no decorative p-values; reversals
reported individually; no change to `find_principles_v2` or to the controls; provenance as in the
other scripts; no run on a real model before Luciano approves cases.

What changes:

1. **Phase 1 as written would confirm itself.** Since 2026-10-06 the principles are listed in
   `CLAUDE.md` as instructions, and almost every decision of `record/decisions.md` after that date
   was proposed or taken by a model told to follow them (hence each entry's "For P4, P12"). A
   principle "predicting" those decisions measures obedience, not discrimination. The temporal cut
   protects against formulating a principle after the decision; it does not protect against the
   principle having caused it. The cases must come from decisions not guided by the list: before
   2026-10-06, or taken by Luciano without the list in front of him.
2. **The cases come from the transcripts, not from the log.** The log has about 40 entries over
   four days, mostly method, mostly the same day as the principles. The transcripts of the Luthier
   and sonolocalización sessions hold 2,009 turns of Luciano's, 513 of them followed by an edit of
   files before his next turn, 87 of those short confirmations ("dale", "ok"), 132 followed by a
   commit. Each such unit is deliberation (the model's proposal, often with alternatives), the
   decision (his turn, his words), and the act (files changed, the commit hash), each with its time.
   Git keeps only the act, several decisions at once.
3. **Who decided is a field.** Luciano chose between alternatives; Luciano confirmed a model's
   proposal (the decision is his, the idea the model's, which matters for P1, "Luciano's part
   stays discernible"); or the model acted within its margin with no turn of his asking.
4. **First seen of a principle** comes from the date of Luciano's earliest words for it (each entry
   of `record/principles.md` has its quote and source; P11's is 2026-09-10, P10's 2026-10-05), not
   from the date the list was written. The window from that date to 2026-10-06 is where the test
   means something.
5. **Batch the calls.** Fourteen principles by thirty cases by two orders is 840 CLI calls, hours of
   start-up alone. One call per principle, with all eligible cases and no other principle in view,
   keeps the isolation and costs about thirty calls.
6. **Add conflicts.** With every principle applied to every case, the pairs that choose opposite
   options on the same case come for free. That is Luciano's fear stated with cases: that
   incompatible principles jam Luthier.
7. **Language as well as method.** The log is about records and commits. Decisions about the
   language (the specification, the interpreter, the `.lut` libraries) are in the transcripts too;
   cases touching those files are the language's, those touching `record/` the method's.

## 5. What happens next

1. Claude writes the mechanical miner: from the Claude Code transcripts pinned in
   `~/Projects/IA_chat/raw/claude-code/` (sha256 in its manifest), every turn of Luciano's followed
   by an action, with the preceding model turn, the files touched, the commit if any, the time, and
   who decided. No model call; tests on fixtures.
2. A model drafts each case (question, A, B, actual, quotes of both turns, the commit), all
   `approved: false`.
3. Luciano reviews a sample of about thirty, mixed between language and method, choices and
   confirmations, with the reversals.
4. The temporal validation runs on the approved cases, with your design and the changes of section 4.

If you take a part, the runner (`validate_principles_temporal.py` and its two prompts) is separable
from the miner: it reads `record/validation/decision_cases.jsonl` in the format you proposed, plus a
`decided_by` field and the source turns and commit.

Open, for you to weigh: whether the model that drafts the cases should see the commit's diff (it
names the road taken precisely, but it is written after the decision), and how to keep a case's
wording from leaning toward the option that was chosen when the drafter knows which one it was.
