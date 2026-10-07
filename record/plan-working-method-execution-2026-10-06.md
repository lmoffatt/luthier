# Execution plan: putting the working method into practice, 2026-10-06

Note, 2026-10-07: the development record moved from `docs/` to `record/` (D-2026-10-07-a, Luthier
proper separated from the record of its development). A path `docs/<x>` named below for a plan, the
decision log, the principles, an audit, the voice notes or Luciano's notes now reads `record/<x>`;
`docs/semantica/` is unchanged by that pass. The text below is kept as written.

Draft 1, 2026-10-06. Status: as in the table below.

Written for the sessions that carry out the plan. It assumes no memory of the conversations that
produced it; everything needed is here or in the files named.

Sources:

- The decisions behind each step, and Luciano's answers to them, are in
  `docs/plan-working-method-2026-10-06.md`, draft 2, called "the decisions" below. A step that waits
  for a bite there doesn't start until the bite has his answer. His answer is a line under the bite
  that `git diff <commit of draft 2> -- docs/plan-working-method-2026-10-06.md` shows as added.
- The working method, `docs/working-method.md`, cited by section number and title.
- `sonolocalizacion@3023967:docs/plan-mechanical-rules-2026-10-06.md`, cited as
  `plan-mechanical-rules`: the lints and hooks of sonolocalización. Several steps here meet it.
- Draft 1 of the plan, `32f82a7`, which held both documents in one.

## Where things are

- Luthier: `/home/lmoffatt/Projects/luthier`, public on GitHub as `lmoffatt/luthier`.
- Sonolocalización: `/home/lmoffatt/Projects/sonolocalizacion`, private as `lmoffatt/sonolocalizacion`.
  No `lint/`, `docs/`, `CLAUDE.md` or `.claude/` yet.
- Oral transcriptions: `/home/lmoffatt/Projects/Oral transcriptions`, no git. The scripts that write
  there live in `/home/lmoffatt/Projects/scripts`.
- The model's memory: `~/.claude/projects/<project>/memory/`, 13 folders. The one of macro_dr
  already has a git, with its own history and a `check_memory.sh`.
- Claude Code transcripts: `~/.claude/projects/<project>/<session id>.jsonl`, one JSON object per
  line.

Measurements of 2026-10-06: `/home` is 97% full (56 GB free). Oral transcriptions holds 2.7 GB, of
which 13 MB are text: 1509 `.md`, 7 more whose names end in `.md ` (with a space), 37 `.txt`. The
rest: 1149 `.mp3`, 967 `.ogg`, 127 `.opus`, 7 `.zip`, one `.vcf`, one file with no extension.
Sonolocalización tracks 234 files under `prototipo-cero/2026-09-07/derived/` and ignores `*.wav`,
`*.zip` and `*.npz`.

## Rules for every step

- Commit per step, in English, one sentence that says what is now true, in the style of the
  repository. A step may take several commits; a commit never spans two steps. No push.
- Who runs what. The model writes scripts and may run lints, tests, `luthier check`,
  `luthier certify`, `git init` and hashing. Luciano runs the scripts that process data or the
  record of the project: the chat export, the audits.
- Every check prints one finding per line as `path:line: rule: message` and exits 1 on findings, as
  in `plan-mechanical-rules`.
- Sources are written in the grammar of bite 2 of the decisions: `luthier@<commit>:<path>:<line>`
  (or `:<a>-<b>`), `sonolocalizacion@...` likewise, `chat:<first 8 characters of the session
  id>:<line of the transcript>`. A git outside both repositories (the memory, the transcriptions)
  is named by its absolute path in place of the repository name.
- A decision the step forces and this plan doesn't settle: if one commit undoes it and nothing
  depends on it yet, take it and list it at the end of the task. Otherwise stop and ask Luciano, in
  one question he can answer after reading a screen.
- Hooks are configured with the `update-config` skill. Check there how a hook's output reaches the
  model before relying on it.

## Order

| Step | What | Status |
|---|---|---|
| 1.1 | `scripts/export_chat.py` | done, `6603948`; an export is committed after Luciano skims it |
| 1.2 | `docs/principles.md` | done, `f3cc031` |
| 1.3 | `docs/decisions.md` | done, `f3cc031`, entries added as decisions are taken |
| 1.4 | the record in sonolocalización | done, `sonolocalizacion@ede219f` |
| 2.1 | `CLAUDE.md` in both repositories | done, `fea45bf` and `sonolocalizacion@e4d5658` |
| 2.2 | reminder of commits with no decision | dropped, D-2026-10-06-s |
| 2.3a | git for the model's memory | done; a Stop hook in `~/.claude/settings.json` commits it |
| 2.3b | git for the oral transcriptions | done, `139f059` in that folder |
| 3.1 | manifests of the raw data of sonolocalización | done, `sonolocalizacion@3107f50`; `derived/` left out |
| 4.1 | `scripts/check_quotes.py` | done, `0185d22`; the record passes |
| 4.2 | `scripts/check_spec_tests.py` | done, `f079e0d` |
| 4.3 | header check | dropped, D-2026-10-06-s |
| 5.1 | fidelity audit | to do; needs an export of `7217f251` |
| 5.2 | principles audit | to do; run by hand before a push |
| 5.3 | correspondence audit | run by workflow at `b15f2a1`, report `docs/audits/2026-10-06_correspondence_v1_claude-opus-5-5.md`; script `60fd7d8`, its calibration against that run pending |
| 6 | the list of working method §12 | items 1, 3, 4, 5, 10, 11, 12 done |

The git for large derived data is deferred (decision D-2026-10-06-i) until a derived file exists that
is expensive to produce again and changes between runs. It has no step.

## Phase 0. Pin the sources (done)

`bf05457` draft 0 of the working method, `2a660c8` Luciano's annotations on it, `62ac538` draft 1,
`ed8052a` its correction to §8. `a8cc4c9` draft 0 of the plan, `daa5b95` his annotations, `32f82a7`
draft 1, then the split into this file and draft 2 of the decisions. `d41026e` his observations on
`lib/random.lut`, moved out of the code.

## Phase 1. The record

### 1.1 `scripts/export_chat.py`

Input: one transcript `.jsonl`. Output: `docs/chat/<date>_<session8>.md`, where `<session8>` is the
first 8 characters of the session id.

The export holds the text of every turn, by author, each with its timestamp and its line in the
transcript. Both sides: a confirmation means nothing without what it answered. Dropped: tool calls
and their outputs, and the text the harness inserts (`<system-reminder>`, `<ide_opened_file>`, the
output of local commands). Kept and marked as pasted: text inside `<pasted_content>`, since it may
not be Luciano's. Messages he sends while the model is working are recorded as `attachment` with
type `queued_command`, and are read too. Frontmatter written by the script: session id, sha256 of
the transcript, number of turns, the script's version.

At the top of the export, before the turns, the script lists the turns that contain a word of
`scripts/export_chat.private` (one word per line: databaum, acuerdo, propiedad intelectual,
patente), so Luciano reads those first (decisions, bite 1).

The transcript format is internal to Claude Code and may change, so the script stops with the line
number on any line it doesn't understand.

Done when:

- the export of `7217f251` holds the quotes of its lines 68, 196, 220, 227, 366 and 382, and the export of
  `8d5ce152` those of its lines 107, 108 and 140, each under its line number;
- the export of `8d5ce152` marks line 140's pasted text as pasted;
- no `<system-reminder>`, `<ide_opened_file>` or tool output appears in either export;
- two runs on the same transcript give the same bytes.

Exports are committed only after bite 1. A session on sonolocalización's private matters is
exported into that repository's `docs/chat/`.

### 1.2 `docs/principles.md`

A record, terse. One entry per principle P1 to P13, as in bites 6 to 9 of the decisions: number and
statement, `Quote:`, `Source:`, `Assumption:`, `Status:`. The status is what Luciano marked in the
decisions at the time of writing (`ok` gives `current since <date>`), and `proposed` where he hasn't
marked. A model never writes `ok`.

P10 and P11 need their sources pinned.

- P10 (the mathematical object that best represents a concept is the invariant of its type):
  `docs/semantica/07-characterizations.md`, "Principle (Luciano, 2026-10-05)". Find the commit that
  added the line, and Luciano's words in the session of 2026-10-05 (its transcript, through an export
  of 1.1 or by search). If his words aren't found, `Source:` names the line of `07` and says so.
- P11 (every criterion is a parameter, never a constant in the code):
  `~/.claude/projects/-home-lmoffatt-Projects-sonolocalizacion/memory/nunca-hardcodear.md`. After
  step 2.3a that folder has a git, so the source is its path, commit and line.

Done when: thirteen entries with every field; the statuses agree with the decisions; step 4.1, once
it exists, passes on the file.

### 1.3 `docs/decisions.md`

A record, terse, in the format of working method §6 (decisions) with sources in the grammar above.
Its first entries are D-2026-10-06-a to q, from the appendix of the decisions, with the statuses
there. From then on an entry is written when its decision is taken.

Done when: seventeen entries; every entry authored by Luciano has `Quote:` and `Source:`; step 4.1,
once it exists, passes on the file.

### 1.4 The record in sonolocalización

`docs/decisions.md` and `docs/principles.md` at its root, in a new `docs/` folder. A decision about
the method gets a one-line entry that refers to luthier's log
(`luthier@<commit>:docs/decisions.md`, with the entry's id). The principles appear by statement, each
with the same reference. Decision D-2026-10-06-p (Luciano's observations on code live in a folder of
their own) applies here to `Lucianos feedbacks/`.

Done when: both files exist, and no line of `docs/working-method.md` longer than 60 characters
appears in them (the method is cited, never copied).

## Phase 2. The model's conduct

### 2.1 `CLAUDE.md`

The text of bite 3 of the decisions, as Luciano answered it, at the root of luthier and of
sonolocalización. If `plan-mechanical-rules` step 6.2 hasn't written sonolocalización's yet, this
step creates the file and 6.2 adds its lines.

Done when: each file holds the answered text; no line carries a source, a quote, a date or an origin
(no match for `annotation`, `chat:`, `@[0-9a-f]{7}`, `line [0-9]`).

### 2.2 Reminder of commits that no decision names (dropped)

Dropped by D-2026-10-06-s (a mechanism with a recurring cost waits for a real case): it needed a
`Decision:` line in every commit. The report at the end of each task, a rule of `CLAUDE.md`, is the
check that remains. If a decision taken alone ever goes unreported, the design that was here is in
`5e4f134`.

### 2.3a Git for the model's memory

For each folder `~/.claude/projects/*/memory/` without a `.git`: `git init` and a first commit of
its current state. A `Stop` hook in the user's settings (`~/.claude/settings.json`, since it applies
to every project) takes the memory folder of the session from the directory of `transcript_path` in
its input, runs `git init` there if needed, and commits whatever changed, with the session id in the
message. In macro_dr's folder it commits on top of the history already there.

Done when: every memory folder has a git with at least one commit; after a turn that writes a memory
file, `git -C <folder> log -1` shows a commit of that turn; a turn that writes none makes no commit.

### 2.3b Git for the oral transcriptions

`git init` in `/home/lmoffatt/Projects/Oral transcriptions`. A `.gitignore` that ignores everything
except directories, `*.md`, the seven names ending in `.md ` (in `.gitignore` a trailing space needs
a backslash, `*.md\ `), `*.txt`, `.gitignore`, `manifest.sha256` and `refresh-manifest.sh`.
`refresh-manifest.sh` writes `manifest.sha256`: the sha256 of every file git ignores
(`git ls-files --others --ignored --exclude-standard -z`), sorted by path. The folder holds private
material and never gets a remote.

Done when: `git ls-files` lists the text files and the three files above and no audio;
`sha256sum -c --quiet manifest.sha256` exits 0; `.git` weighs about as much as the text, not the
audio.

## Phase 3. Data

### 3.1 Manifests in sonolocalización

`prototipo-cero/2026-09-07/manifest.sha256` and `audio-campo/manifest.sha256`: the sha256 of every
file that git ignores under each folder for its size (`*.wav`, `*.zip`, `*.npz`), with paths relative
to the folder. `lint/manifests.sh` checks both with `sha256sum -c --quiet` and lists the ignored data
files that a manifest lacks, in the format of the rules above. `lint/full.sh` of
`plan-mechanical-rules` step 2.1 calls it once that file exists. Until then it is run by hand, and
that plan's phase 0 should know that `lint/` now exists.

Hashing about 5 GB takes minutes and produces no result, so the model runs it.

Done when: both manifests are committed; `lint/manifests.sh` exits 0, and exits 1 on a copy of a
manifest with one hash changed.

## Phase 4. Mechanical checks

### 4.1 `scripts/check_quotes.py`

For every entry of `docs/decisions.md` and `docs/principles.md` authored by Luciano: it has `Quote:`
and `Source:`, as many sources as quotes, paired in order. Each quote is at its line (or starting at
it) in `git show <commit>:<path>`, with whitespace normalized and nothing else. A `chat:` source is
read from the export in `docs/chat/` whose name ends in that session; with no export, from the
transcript under `~/.claude/projects/`, with a warning. A source in a repository that isn't on disk
gives a warning and no failure, since each repository is self-contained. `--repo` points it at
sonolocalización's record.

Tests in `tests/test_check_quotes.py`: a right quote passes; a quote at the wrong line fails; a
one-word quote (`"ok"`) at the wrong line fails; a missing repository warns.

Done when: the tests pass, and the script passes on the files of 1.2 and 1.3.

### 4.2 `scripts/check_spec_tests.py`

It reads the rules R1 to R11 of `docs/semantica/05-static-semantics.md` §5 and looks for them in the
names of the files of `tests/spec/` (`r<n>_<name>.accept.lut`, `r<n>_<name>.reject.lut`). Each rule
needs at least one file of each kind. A rule whose paragraph says "not implemented" is reported as
such, not as missing tests.

Done when: on today's tree it reports exactly two findings, R10 (a law characterizes; a second
implementation is not a law) with no tests and R11 (a condition refines in its branch) not
implemented, and exits 1; a test in `tests/` with a small specification of its own passes.

### 4.3 Header check (dropped)

Dropped by D-2026-10-06-s: no document has yet reached Luciano without a usable header.

## Phase 5. Audits by prompt

Each audit is a prompt in `prompts/` and a script in `scripts/` in the style of
`scripts/extract_ideas.py`, which calls the `claude` or `codex` command line and records the prompt
version, the model and the hashes of its inputs. Outputs go to
`docs/audits/<date>_<audit>_<prompt version>_<model>.md`. Luciano runs them.

### 5.1 The fidelity audit

`prompts/audit_fidelity_v1.md`, `scripts/audit_fidelity.py`. Inputs: a target document at a commit,
and its sources (the annotated draft at its commit, the chat exports). Output: one row per rule or
claim of the target, with its origin: Luciano, with the source; the model; the model confirmed by
Luciano, with the source; or confirmed only in a bundle.

Calibration: target `docs/working-method.md` at `ed8052a`, sources `2a660c8` and the export of
`7217f251`. Appendix A is the same audit done by hand.

Done when: the calibration run ends with a comparison against Appendix A (the rows that agree, the
rows that don't, and for each disagreement which side is right after reading the source). The
prompt is used on nothing else before that.

### 5.2 The principles audit

`prompts/audit_principles_v1.md`, `scripts/audit_principles.py`. Inputs: `docs/principles.md`,
`docs/decisions.md`, the commits since the previous audit (whose output names the commit it reached),
and the documents changed since. Output, for Luciano's three questions and the risk of the decisions
§1:

1. for each principle, the decisions that invoked it, for or against, and whether it guided any;
2. the conflicts, of a principle with itself or with another, with how each happens;
3. candidate principles found in the documents, each with its assumption, its conflicts with the
   current ones, and the cost and benefit of adding it;
4. drift: runs of local decisions that add up to a change that isn't local.

Calibration: a run on the sources of draft 1's principles (`2a660c8`, `daa5b95`, the export of
`7217f251`) with an empty `principles.md` should find P1 to P9, P12 and P13 again, or equivalents.

When it runs (bite 4, D-2026-10-06-o): before each push of `main` and on request, by hand. The
reminder hook before a push was dropped by D-2026-10-06-s.

Done when: the calibration run ends with its comparison against the list above.

### 5.3 The correspondence audit

Deferred by D-2026-10-06-s, then reinstated by D-2026-10-06-x: it is what matters most to Luciano.

Both directions over the whole specification: each document of `docs/semantica/` against the code and
the tests, each group of modules against the specification, and `README.md` and `examples/` against
both; a skeptic per unit tries to refute each finding; one report for Luciano (a screen of summary,
bites, tables). The first run was a workflow at `b15f2a1`;
`scripts/audit_correspondence_journal.py` wrote its results in the layout below, under
`docs/audits/2026-10-06_correspondence_v1_claude-opus-5-5/`, with the report.

`scripts/audit_correspondence.py`, with `prompts/audit_correspondence_*_v1.md` and the units in
`prompts/audit_correspondence_units_v1.json`. It pins a commit in a throwaway worktree, runs the
calls there, resumes where a run stopped, and writes `docs/audits/<date>_correspondence_v1_<model>/`
and the report. The permission rules of the calls are not a sandbox; the script compares Luciano's
tree before and after and says so in the report if it changed. Start small:
`python3 scripts/audit_correspondence.py --only spec-08 --model sonnet --no-report`.

Calibration: the first run of the script agrees with the workflow's run on the same commit, unit by
unit, or each disagreement is settled by reading the source.

Done when: the calibration passes. Step 4.2 is the mechanical half of the same audit; the check of
traceability of D-2026-10-06-y will be the rest.

## Phase 6. The list of working method §12 (what is out of place today)

Each item is a logged decision with its own commit. Working method §12 names the files.

| Item | What | Who decides |
|---|---|---|
| 1 | Commit `Lucianos feedbacks/` and `funcion de los tipos en Luthier.txt` in sonolocalización | bite 11 |
| 2 | Add the commit to the citations of item 1 | the model, after item 1 |
| 3 | The certification logs of 2026-10-05/06 | done: found in the scratchpad of session c7437496, committed at `sonolocalizacion@81ba456`, and `plan-2026-10-06.md` says where each figure is |
| 4 | Decision log and principles | phase 1 |
| 5 | The notes at the end of `lib/random.lut` | done, `d41026e` |
| 6 to 8 | Moving the surveys of prior art and the answers of other models | the model, one commit each, references updated in the same commit |
| 9 | R10 (a law characterizes) without a test | the next round of the interpreter; step 4.2 reports it |
| 10 | `CLAUDE.md` | step 2.1 |
| 11, 12 | Git for the memory and the transcriptions; manifests | steps 2.3a, 2.3b, 3.1 |
| 13 | The working method names principles, sections and kinds by letter or number without their statement | the model: apply D-2026-10-06-l (a numbered reference carries its statement), one commit |
| 14 | Working method §4 says Luciano's notes on code are at the end of `src/luthier/lib/random.lut` | the model: replace it with `docs/Lucianos observations/` and sonolocalización's `Lucianos feedbacks/`, one commit |

## Appendix A. Fidelity of the working method, by hand

The calibration of step 5.1: the fidelity audit applied by hand to `docs/working-method.md` at
`ed8052a`. One row per rule or claim. "Bundle" means confirmed only by "Si." (chat 7217f251, line
227), which answered a proposal of several parts at once. Line numbers without a source are
annotations on the method (`2a660c8`).

| Section of the working method | Rule or claim | Origin |
|---|---|---|
| §1 (what the structure is for) | The three questions the structure is for | Luciano, lines 309 to 314 |
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
| §6 | A rationale may be "because I wanted it so" | Luciano, chat 7217f251, line 68 |
| §6 | The format of an entry; the four kinds of rationale | the model |
| §6 | Confirmation by a checked quote; his mark only for principles | the model, answering line 306; open in §13 |
| §7 (the model's part in view) | What he hasn't understood must be contained | Luciano, line 110 |
| §7 | The four mechanisms of containment | the model |
| §8 (reversibility) | The loophole; commit before every change makes decisions reversible | Luciano, chat 7217f251, line 196 |
| §8 | Detection latency as the real cost; the five rules | the model, bundle |
| §8 | Push only tagged milestones | the model, bundle |
| §8 | What git doesn't revert | the model, bundle |
| §8 | What is ignored for size needs its own treatment | Luciano, chat 7217f251, line 220 |
| §8 | The three cases of large files; the git for large data | the model, bundle |
| §9 (specification and implementation) | Implementing brings out problems and questions | Luciano, line 171 |
| §9 | The same form applies to the analysis of data | Luciano, line 170 |
| §9 | The route back from implementation to specification | the model |
| §10 (the audits) | Audits by prompt, in the style of the ideas pipeline | Luciano, line 309; the design, the model |
| §11 (common rules) | The header | the model |
| §11 | Who runs what | Luciano, in rules of earlier sessions kept in memory files outside git |
| §11 | Language | Luciano, rule of 2026-10-01, kept in a memory file outside git |
| §12 (what is out of place today) | The findings | the model, facts that can be checked |

Count, by script over the 46 rows: 24 have Luciano as origin (two of them with a part by the model),
2 are proposals he confirmed explicitly, 20 are proposals of the model, 4 of those confirmed only in
a bundle.
