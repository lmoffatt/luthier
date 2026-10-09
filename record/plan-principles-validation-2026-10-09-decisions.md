# Validating Luthier's principles against real decisions: the decisions

Draft 0, 2026-10-09. Written for Luciano and for GPT, to review before anything runs. The execution,
step by step, is in `plan-principles-validation-2026-10-09-execution.md`. What comes from a source
is cited; the rest is Claude's proposal.

## What this is for

Luciano: a principle is "una idea organizadora que ayude a tomar decisiones" (an organizing idea
that helps make decisions). The experiment asks whether the principles Luthier already has do that:
given a real decision taken before the principle could have steered it, does the principle pick the
option that was chosen, more often than a model with no principle does, and where do two
principles pick opposite options?

It is the first of two experiments (GPT, `record/IA/handoff de gpt para claude 2.md`). The second,
whether the pipeline from sources to candidates discovers principles, waits for this one, and for a
fix of the loss of normative force in extraction and linking that the controls showed
(`record/controls/README.md`, results).

Agreed already, not asked again: the decisions come from the Claude Code transcripts, not from
`record/decisions.md` ("la historia esta mas en los chats en .claude que en git"); cases drafted by
a model start unapproved and the scorer refuses them; the payload to the model is built from
allowed fields only; every case runs with its options in both orders; a baseline without the
principle; Wilson intervals, no p-values; no change to `find_principles_v2` or to the controls.

## The decisions

Each has options, a recommendation, and what it costs. Answer with the number and ok, no, or a
correction.

**D1. When does a principle start to count?** A case is independent for a principle only between
the moment the principle existed and the moment it could steer the agent (GPT's three dates:
emergence, the first evidence of the idea in Luciano's words; explicit, its first formulation as a
rule; operative, when it entered what the agent had to follow).
- (a) from explicit to operative. (b) from emergence to operative.
- Recommended: (a) for the main result, (b) reported apart. Emergence is often a passing remark;
  a principle can't be blamed for missing decisions taken before anyone stated it as a rule.

**D2. What makes a principle operative?** Its entry in an instruction the agent read.
- Proposed: the earliest of (i) `CLAUDE.md` of the repository the session ran in (luthier and
  sonolocalización: 2026-10-06), (ii) `~/.claude/CLAUDE.md` (global, 2026-10-06 for P12), (iii) a
  memory note of that project (memory is per project: sonolocalización's note on hardcoding, which
  states P11, existed by 2026-09-11; luthier's memory never stated it), (iv) the principle stated
  earlier in the same session.
- Recommended: all four. It follows that a principle can be operative in one repository and not in
  the other on the same day, which gives cases of a natural experiment.
- Cost: fewer cases. For P11 the window in sonolocalización is about one day.

**D3. How is "stated earlier in the same session" detected?** Mechanically: the session's earlier
turns are searched for the principle's quote and statement; an overlap above a threshold (a
parameter) marks the case exposed.
- Recommended: exposed cases leave the main result and are listed. A model reading the session for
  exposure would be more accurate and cost a call per case; not now.

**D4. Which principles?** P1 to P14 (`record/principles.md`).
- Recommended: every principle with at least three approved independent cases (the threshold is a
  parameter); the others are listed with their count and not scored.
- Expected consequence, said in advance: most of P1 to P13 became explicit and operative on the same
  day (2026-10-06), so their windows are empty or tiny. P10, P11, P14 and parts of P4 have longer
  windows. The experiment may end with few principles scored. That is a result, not a failure of
  the plan.

**D5. Who decided, and which kinds of case count?** Each case says who decided: Luciano chose between
alternatives; Luciano confirmed a model's proposal (his decision, the model's idea); the model acted
within its margin with no turn of his asking.
- Recommended: the first two in the main result, reported apart from each other; the third apart,
  since it tests whether a model behaved as the principle says, not whether Luciano did.

**D6. Units with private words.** Twelve of the 409 units mined so far mention words of
`scripts/export_chat.private`; their texts are withheld from the repository.
- (a) leave them out. (b) draft them into a local-only folder (outside git) and score them there.
- Recommended: (a) now; (b) if the counts turn out too small.

**D7. Does the drafter see the diff?** GPT: yes, as evidence of what happened, stored with the case;
the options sent to the scorer are a separate abstraction, which Luciano's approval checks.
- Recommended: yes, as GPT says.

**D8. Constructed alternatives.** The drafter writes the strongest alternative genuinely available,
and marks it as explicitly discussed, strongly implied, or constructed (GPT).
- Recommended: constructed alternatives leave the main result.

**D9. How many cases does Luciano review, and how?** All drafted cases is too many for his
attention (P12, Luciano's attention is the scarce resource).
- Proposed: a stratified sample of about 30 (language and method, choice and confirmation, the
  reversals, both repositories), in one review document with an `ok`, `no` or correction line under
  each case. His marks are committed verbatim; a script turns `ok` into `approved: true`. Nothing
  else ever sets it.
- Cost: about half an hour of his reading.

**D10. One call per principle, or one per case?** Per case is the cleanest and costs hundreds of
calls (14 principles, 30 cases, 2 orders). Per principle, all its eligible cases in one call, with
no other principle in view, costs about 30 calls; the risk is that cases in one call influence each
other.
- Recommended: per principle, cases in a shuffled order with the seed recorded, and a check on a
  subset run one case per call; if the two disagree beyond a threshold, per case.

**D11. Who runs it.** The drafting and the scoring read Luciano's record, which by the working
rules he runs.
- (a) Luciano runs each step. (b) Luciano authorizes the model to run them, as for the controls.
- Recommended: (b) for the drafting (long, mechanical to follow); (a) for the scoring, after he has
  approved the cases.

**D12. Which sessions.** The luthier and sonolocalización sessions (62 so far). macro_dr's DSL and
macroir are ancestors with their own sessions.
- Recommended: these two now; the ancestors later, if the result calls for more cases.

## What it will cost

| step | model calls | Luciano's attention |
|---|---|---|
| mine the decisions | none | none |
| dates of the principles | about 14 short ones, to find emergence | one screen: 14 entries |
| draft the cases | one per candidate unit, 100 to 200 | none |
| review the sample | none | about 30 cases, half an hour |
| score | about 30, plus the subset check | one screen of results |
