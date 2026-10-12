# The specification, wave 1: the execution

Draft 0, 2026-10-12. Written for the sessions that carry it out, including a session that starts
with no memory of this one: everything it needs is in files, and the status lines below are
updated at each step. The choices it rests on are D1 to D10 of
`plan-spec-2026-10-12-decisions.md`; until Luciano answers, every step assumes them as proposed
and says so in its commit. Inputs: `docs/principles.md` draft 11 (bd4537e; the twelve chapters
and their principles were settled in chat on 2026-10-12, see *The chapters* below), the six spec
files of today (`docs/spec/02-grammar.md`, `03-libraries.md`, `04-kernel.md`,
`05-static-semantics.md`, `06-numbers.md`, `08-tests.md`, at bd4537e), the rationale documents as
sources (`docs/rationale/09-extern-and-the-world.md`, `11-cost-valued-laws.md`,
`07-characterizations.md`), `tests/spec/` (50 programs), `scripts/check_spec_tests.py`,
`record/decisions.md`.

## Status

- 2026-10-12: plan written; decisions D1 to D10 with Luciano; nothing started.
- 2026-10-12, on his observation that the other principle documents carried past decisions: `docs/way-of-working.md` (4eb914e), `docs/rationale/11-cost-valued-laws.md` (d953792) and `docs/principles-for-readers.md` draft 6 (5076a6d) brought to draft 11, and the citation check of `project_principles.py --check` now covers the three; an agent of wave 1 may cite any of them.
- 2026-10-12, later: his marks on D1 to D10 taken (D-2026-10-12-y, -z, -aa; L14 and Term as data, -x). Step 0 done: `docs/spec/00-index.md`, `record/spec-drafts.md`, `record/spec-brief-template.md`, the briefs in `record/spec-briefs/` (3445ad8); `scripts/check_spec.py` being written by a Sonnet agent in a worktree (not yet merged). Step 1 started: seven Sonnet agents (all Sonnet, not Opus for 4 and 7, to spare tokens) launched in worktrees at 3445ad8, one chapter each (1, 2, 3, 4, 7, 11, 12); none committed. Next, for whoever integrates: find the worktrees (`git worktree list`), read each chapter whole, run `scripts/check_spec.py` on it once merged, compare against its source by a word-level diff, commit chapter by chapter with its row in `record/spec-drafts.md`, delete the old file it replaces, update the index; then step 2.
- 2026-10-12, end of the Fable session: chapters 12 (7552f7a, lint clean), 2, 3, 4, 11 committed as draft 0 with the lint's findings saved in `record/spec-wave-1-lint-2026-10-12.txt` (runs shared with the old files they replace, which vanish when those are deleted; a few runs shared with the principles or between chapters to reword; 4.R9 without status; 4.R10 and 4.R11 with placeholder file names). Chapter 1 committed too (findings appended to the lint file). Chapter 7 committed too: all seven chapters of wave 1 are in as draft 0, no worktree left; their reports arrive as task notifications to the session that spawned them, so a new session must read the files from the worktrees directly. Next session (Opus, to spare the Fable quota): copy 1 and 7 in, fix the findings of all six, delete the six old files (02 is already replaced in place; 03-libraries, 04-kernel, 05-static-semantics, 06-numbers, 08-tests) and update `project_principles.py`'s DOC_RE expectations if `--check --strict` complains about backticked numbers, run `python3 scripts/check_spec.py` clean, update the index, remove the worktrees (`git worktree remove --force`), then step 2 and the for-his-marks document with the agents' questions listed in `record/spec-drafts.md`.

## Rules for every step

- Commit before every change; one chapter, at least one commit; the message names the chapter
  and the decisions it rests on.
- The principles are not edited by the spec work; a chapter that finds a contradiction with
  them stops and reports it as one question (W15), it does not resolve it.
- A rule keeps the words of its source where the source is decided or implemented; what the
  model adds is `[proposed]`.
- Every chapter ends with "Open", citing the O ids of the principles, never a list of its own.
- An agent writes one chapter in its own worktree and never touches another chapter, the
  interpreter, the principles or the record; the integrating session merges, runs the check,
  commits.
- State lives in files: this status section, `record/spec-drafts.md`, the commits.

## The chapters

Settled in chat 2026-10-12 (Luciano: "vamos a la especificación", "que secciones tiene que
tener"). Each with the principle it realizes and its sources; the wave says when.

| Chapter | Realizes | Sources today | Wave |
|---|---|---|---|
| 1 Terms and notation | Terms of the principles | the §0 of 04, 05, 06, 08, 09 | 1 |
| 2 Grammar | L7 (surface to kernel) | 02 whole; 08 §12 for the test directive and `gen` | 1 |
| 3 Kernel | L7 | 04 | 1 |
| 4 Static semantics | L2, L8 | 05 §1 to §6, §8; O7 | 1 |
| 5 Laws | L12, L3 | 05 §9, 11 §2 and §5 | 2 |
| 6 Certification | L9, L10 | 05 §7, 03 §4, 08 §8 and §9 | 2 |
| 7 Tests and generators | L10.3, L5.18 | 08 | 1 |
| 8 The demand and the plan | L5 | 02 §8 and §9 (session); nothing else | 3 |
| 9 Specimens and the planner | L6 | 04 §6, 05 R10 | 3 |
| 10 Actions and the world | L4, L11 | 05 R5 and R12, 02 §9, 09 | 3 |
| 11 Numbers | L13 | 06 | 1 |
| 12 Files and tools | L5, L10 (tools) | 03 §1 to §4, 05 §7 (as implemented) | 1 |

## Step 0. The frame (this session's model, before any agent)

1. `docs/spec/00-index.md`: the table of contents above, the status legend of D2, the citation
   form of D1, and a line per chapter: written / not yet, with its commit.
2. `record/spec-drafts.md`: one row per chapter, sources by commit, who wrote it, the commits.
3. `scripts/check_spec_tests.py` extended as D2 says (statuses, D ids, references, the two
   files of each implemented rule, duplicate runs across chapters), with tests in
   `tests/test_check_spec_tests.py`; informational until a chapter is written, then blocking on
   that chapter. Commit.
4. The brief template, `record/spec-brief-template.md`: goal, sources by path and commit, the
   decisions in force (D1 to D10 by their statement), what is settled by the principles (the
   chapter's L and its clauses, quoted), what not to touch, the shape of a rule (`**4.R3. title**
   [status] text. Files: ...`), the check that closes it, and the report expected (what was
   dropped from the source and why, what was marked proposed, what contradiction was found).

## Step 1. Wave 1, seven chapters in parallel (D9)

For each chapter an agent in its own worktree, with the template filled:

- Chapter 1 (Sonnet): the notation of the five §0, merged, each symbol once; Terms cited.
- Chapter 2 (Sonnet): 02 with 08 §12 applied (`test` extended, `profile` act, `gen` removed) and
  the blocks of §9 as they are; every production that the parser implements `[implemented]`,
  the rest `[decided]` with its D id.
- Chapter 3 (Sonnet): 04 as it stands, O7's wording for cycles, the bridge rules of §6; the
  interpreter's status of §7 moved to the index.
- Chapter 4 (Opus): 05 §1 to §6 and §8 as rules with status and files; O7 taken (D5); the grades
  mentioned by the five of Terms (D4); §7 and §9 left for chapters 6 and 5 with a pointer.
- Chapter 7 (Opus): 08 with the grades of D4, C2's 3/n as the first instance of the conversion
  (D-2026-10-12-r), every budget an argument (L5.18), the statistical laws (C8 to C10).
- Chapter 11 (Sonnet): 06 as it stands, L13.3 and L13.4 at the status D6 gives them, the
  rounding law of 06 §8 as the worked instance.
- Chapter 12 (Sonnet): 03 §1 to §4 and the commands, certification by default (D7), the
  libraries' table to the record (D8).

Each agent reports; the integrating session reads the chapter whole, runs the check, compares
against the source by a word-level diff (what disappeared must be named in the report), and
commits with the chapter's row in `record/spec-drafts.md`. The old file of each chapter is
deleted in that commit (D1).

## Step 2. Integration of wave 1

One pass over the seven chapters: one home per fact (the check's duplicate runs), references
between chapters resolve, the index updated, `tests/spec` runs green, the readers of `docs/`
(`README.md` if it points at the spec, `docs/guide/00-fundamental-elements.md` header) point at
the new chapters. Commit. Then the diff of statuses (every `[proposed]` item, one line each) goes
to Luciano as one document, `record/spec-wave-1-for-his-marks.md`, one screen per chapter.

## Step 3. His marks, and the next wave

His marks committed verbatim and applied; then `plan-spec-2026-10-12-decisions.md` gains the
decisions of wave 2 (chapters 5 and 6: Cost in the kernel or a library, the default conjunction,
the conversion's shape, the opt-out's syntax, the names lift/exact/within), written by the
integrating session after wave 1 is done, not before.

## If the session that reads this has no memory of the chat

What was settled in chat on 2026-10-12 and is nowhere else: Luthier has four documents and the
record (principles, specification, manual, way of working); the rationale folder dissolves into
the record once the manual exists; the spec describes the language designed, not only what runs,
with a status per rule; the twelve chapters above; three waves, Luciano the critical path between
them; agents by chapter, Sonnet for the chapters with a fixed source, Opus for 4 and 7, this
session's model for integration and for waves 2 and 3. The estimate given to him: about twenty
decisions in all, six of them semantic (Cost, the conversion, the demand's form, the world's
token, the ranking, the trace), the rest syntax or placement.
