# Validating Luthier's principles against real decisions: the execution

Draft 1, 2026-10-09, after GPT's review of draft 0 (`record/IA/handoff de gpt para claude 3.md`).
Written for the sessions that carry it out and for GPT and Luciano to review.
The choices it rests on are in `plan-principles-validation-2026-10-09-decisions.md` (D1 to D14);
where a step depends on one, it says which and what it assumes until Luciano answers.

## Rules for every step

- Commit before every change; one step, one commit at least; infrastructure and results in separate
  commits, and a commit of results says it is a result.
- Every time is stored in UTC. Sources differ: transcripts are in UTC, git commits carry +0800,
  voice notes local time in their names. Each date keeps its resolution (minute, day).
- Every output records its inputs by sha256, the script and its version, every parameter, the
  prompt and its sha256, model, effort, CLI version, git HEAD, and the seed of any draw.
- Prompts are files under `prompts/`, versioned; a prompt is not edited after it has produced a
  scored result: a new version is made.
- No step changes `find_principles_v2`, the controls, or `approved` in a case.
- Every quote a model writes is checked verbatim against its source by the script.
- Output that goes to the repository passes `scripts/check_private.py`.

## Step 0. Pin the transcripts (Luciano)

```
iachat ingest claude-code
```

The pin of 2026-10-09 02:45 UTC lacks the later sessions of that day. Done when the manifest of
IA_chat lists them.

## Step 1. Mine the decision units (done; rerun after step 0)

`scripts/mine_decisions.py` (commit 45fab10, tests in `tests/test_mine_decisions.py`). No model.

Reads the main transcripts of the luthier and sonolocalización sessions pinned in IA_chat. A unit
is a turn of Luciano's followed by an action before his next turn: the model's last text before his
turn, his turn, the actions (files, start of command), the commits (hash, message, files from git),
the areas (language, method, other), the form of his turn (short, at most six words, or long).
Writes `record/validation/decision_units.jsonl` and `.md`.

First run, on the pin of the early hours: 409 units from 56 sessions, 80 with a commit, 12 withheld.

To add in this step:
- the session's project and the repository a unit's files belong to, needed for D2;
- reversals: a unit whose commit removes or replaces what an earlier unit's commit added (same file,
  overlapping lines), linked to it; mechanical, from git;
- `decided_by` stays empty here; the drafter proposes it (step 4).

Done when the tests pass (including reversal detection on a fixture repository), the rerun covers
every pinned session, and ten units drawn with a recorded seed match their transcripts when read by
hand.

## Step 2. The dates of each principle

Writes `record/validation/principle_dates.json`, one entry per principle P1 to P14 (D1: no
emergence in v1):

```json
{"P11": {"explicit":  {"time": "2026-09-10T..Z", "resolution": "minute", "source": "chat:6878a98d:1148"},
         "operative": {"luthier":          {"time": "2026-10-06T08:18Z", "source": "luthier@fea45bf:CLAUDE.md"},
                       "sonolocalizacion": {"time": "2026-09-11T12:53Z", "source": "memory nunca-hardcodear.md, written in session ..."}},
         "statement": "...", "quote": "...", "status": "current"}}
```

- explicit: the `Quote:` and `Source:` of the principle in `record/principles.md`; its time from the
  transcript line or the commit.
- operative, per repository (D2, i to iii): the commit that put the principle in that repository's
  `CLAUDE.md`; the transcript event that wrote it in `~/.claude/CLAUDE.md`; the transcript event that
  wrote a memory note stating it, per project folder. Found mechanically, by searching the
  transcripts for writes to those files; which note states which principle is proposed by the
  script from the text and checked by hand.

No model call. Done when every principle has both dates with sources and Luciano has marked the file
(one screen). Until then nothing downstream is scored.

## Step 3. Temporal eligibility (mechanical)

`scripts/eligible_cases.py` crosses the units with the dates. A pair (unit, principle) is temporally
eligible when the unit's time is after the principle's explicit date and before its operative date
in the unit's repository. A unit exactly at a boundary is not eligible.

The lexical overlap of the session's earlier turns with the principle's quote and statement is
computed and stored as a flag (`lexical_exposure`, with the turns it points at); it decides nothing
(D3).

Writes `record/validation/eligibility.jsonl`: every pair with its verdict and the reason, the
excluded ones included. The units eligible for at least one principle, plus every reversal, are the
candidates for drafting.

Done when the tests cover each exclusion, the boundary, and the flag.

## Step 4. Draft the cases

`scripts/draft_cases.py`, prompt `prompts/draft_decision_case_v1.md`, one isolated call per
candidate unit. The drafter sees: the model's turn before Luciano's, his turn, the model's next turn
when the act is not clear without it, the files touched and the diff (D7). It does not see the
principles, the dates, or any other unit.

It answers, or says that the unit holds no decision:

```json
{"is_decision": true,
 "question": "...",
 "alternatives": ["...", "..."],
 "chosen_index": 0,
 "counterfactual_status": "explicitly_discussed" | "strongly_implied" | "constructed",
 "evidence_chosen": "a verbatim quote from the turns or the diff",
 "evidence_counterfactual": "a verbatim quote, or empty when constructed",
 "decided_by": "luciano_choice" | "luciano_confirmation" | "model_margin",
 "evidence_decided_by": "a verbatim quote"}
```

The prompt asks for the strongest alternative genuinely available at that point, not a foil, and
for the two options in parallel wording (GPT). The script then:
- checks every quote against the transcript or the diff;
- assigns A and B by a draw with a recorded seed, so the drafter never labels the options;
- writes `record/validation/decision_cases.jsonl`, every case with `approved: false`, its evidence,
  the unit and the commit;
- skips units withheld for private words (D6, assumed (a)).

Done when the tests pass on a stub (malformed answer, a quote not in its source, the draw, the
skipping), and a dry run lists the units it would send.

## Step 5. The sample, its exposure, and Luciano's review

1. `scripts/draw_sample.py` draws forty drafted cases, stratified (D9), with a recorded seed, and
   freezes the list in `record/validation/sample_<date>.json`, committed before anyone reads the
   cases. Rejected cases are never replaced.
2. The exposure judge (D3), prompt `prompts/judge_exposure_v1.md`, one call per sampled case: it
   reads the session up to the decision and the case's temporally eligible principles, and answers
   per principle `none`, `possible` or `explicit`, with the quote of the turn. It never sees the
   outcome as such (only the turns up to Luciano's), and is not the drafter or the scorer. The
   script checks its quotes.
3. `scripts/write_review.py` writes `record/validation/review_<date>.md`: per case, the question, A
   and B, which was chosen, the evidence quotes, the source turn and commit, the exposure answers
   that are not `none` with their quotes, a line for a known tradeoff in his words (optional, no
   principle named), and a line `Mark:` for `ok`, `no`, or a correction.
4. The review document is committed before he marks it; his marks are committed verbatim; then
   `scripts/apply_review.py` sets `approved: true` on the cases marked `ok`, records the review
   commit, and records his verdict on each exposure answer. A correction makes a new case, with his
   text.

## Step 6. Score

`scripts/validate_principles_temporal.py`, prompts `apply_principle_blind_v1.md` and
`apply_baseline_blind_v1.md`. Refuses any case not approved, any pair not temporally eligible or
with an exposure other than `none` for the main run (D3), and any prompt with an unfilled field.

- The principle's call receives only the principle's statement and, when it has one, the road it
  rejects, and the eligible approved cases, each as its number, question, A and B. No id, date,
  source, outcome, status, other principle, or document name. The payload is built from these
  fields only, and a test checks it.
- Each principle runs twice, the options in the original order and swapped; the cases are shuffled
  with a recorded seed. A case whose answer changes meaning with the order is position-unstable and
  is not evidence.
- D10 first: ten cases drawn with a recorded seed, run one per call, compared with the batched
  answers before any outcome is looked at; at least 90% agreement, or everything is rerun one case
  per call.
- Baselines (D13): B0 without a principle; B1 each case with a principle drawn among those not
  eligible for it; B2 the whole run with the statements permuted among the ids.
- Per case and principle (D14): picked the chosen option; picked the other while another principle
  picked the chosen one (lost a conflict); picked the other and no principle picked the chosen one;
  NEITHER.

Report per principle: n and its label (D4: anecdotal under 5, exploratory 5 to 9, scored from 10);
coverage; the four outcomes of D14; stable accuracy with a Wilson interval, only for scored
principles; the same for B1 and B2 on the same cases, and the difference; the conflict matrix with
its cases; reversals one by one. A denominator of zero gives null, said so.

Writes `record/validation/runs/<UTC timestamp>_temporal_principles_<model>.json` (every payload,
raw answer, parsed answer, retry) and `.md`: one screen of results, then the errors, the unstable
cases, the conflicts, the reversals, the cases the baselines got without the principle. A run never
overwrites another.

Done when GPT's thirteen tests pass, plus: the conflict matrix and the D14 outcomes on a fixture,
the order mapping of a batched answer, the D10 rule, B1's draw and B2's permutation. No run on a
real model before step 5 ends.

## Step 7. What comes later, not now

The discovery experiment: timeline rows before a cutoff T, lineages of those rows only, the finding
step, then the cases after T. The validator takes `--principles <find_principles output>` and
`--cutoff T`; no path lets a case after T reach the finding. Before it, the extraction and linking
prompts get a version that keeps the normative force of what was said ("it must be", not "it was").

## Order and who

| step | who | waits for |
|---|---|---|
| 0 pin | Luciano | nothing |
| 1 mine (rerun, reversals) | model writes; runs mechanically | 0 |
| 2 dates | model writes; mechanical; Luciano marks | 0 |
| 3 eligibility | model writes; mechanical | 1, 2 |
| 4 draft | model writes; runs as D11 says | 3 |
| 5 sample, exposure, review | model draws and runs the judge; Luciano reviews | 4 |
| 6 score | model writes; Luciano runs | 5 |
