# Validating Luthier's principles against real decisions: the decisions

Draft 1, 2026-10-09. Written for Luciano and for GPT, to review before anything runs. Draft 0
(da4b910) was reviewed by GPT (`record/IA/handoff de gpt para claude 3.md`, b0fcd6c); what changed
because of that review is marked "(GPT)". The execution is in
`plan-principles-validation-2026-10-09-execution.md`. What comes from a source is cited; the rest is
Claude's proposal.

## What this is for

Luciano: a principle is "una idea organizadora que ayude a tomar decisiones" (an organizing idea
that helps make decisions). The experiment asks whether the principles Luthier already has do that,
on real decisions the agents were not instructed by them to take.

The question is not only "does the principle pick the option that was chosen". A genuine principle
can lose a decision to another one. The question is (GPT): does the principle show a stable and
specific preference on the decisions of its domain, how much of the domain it covers, more than
other principles do, and where does it collide with them? Accuracy against the outcome is one
reading among these, not the verdict.

It is the first of two experiments (GPT, second reply). The second, whether the pipeline from
sources to candidates discovers principles, waits for this one, and for a fix of the loss of
normative force in extraction and linking that the controls showed (`record/controls/README.md`).

Agreed already: decisions come from the Claude Code transcripts, not from `record/decisions.md`;
cases start unapproved and the scorer refuses them; the payload to the model is built from allowed
fields only; every case runs in both orders; constructed alternatives leave the main result;
`luciano_choice`, `luciano_confirmation` and `model_margin` are kept apart; no change to
`find_principles_v2` or to the controls; the result may score few principles, and that is a result.

## Whose exposure matters

A point the review raised (GPT, problem 1) and that this draft answers with a distinction. If
Luciano formulated a principle and later decided according to it, that is not a confound: it is the
principle organizing his decisions, which is what is being tested. What would make the test
circular is the agent: a model told the principle (by `CLAUDE.md`, by its memory, or earlier in the
session) proposing or taking the decision. So exposure is judged for the agent, and it matters most
for `luciano_confirmation` (the option came from a model) and `model_margin`; for `luciano_choice`
it matters only when the agent's earlier turns shaped the options he chose between.

## The decisions

Answer with the number and ok, no, or a correction.

**D1. When does a principle start to count?** From its explicit formulation, the quote Luciano
marked in `record/principles.md`, until it became operative for the agent (D2).
- Changed (GPT): the earliest vague trace of the idea (emergence) is left out of v1. Finding it
  costs model annotation and Luciano's judgment before there is any signal; it can be reconstructed
  later as history if the result calls for it.
  explicit formulation, if its logical structure is enough to make decisions


**D2. What makes a principle operative for the agent?** The earliest of: (i) the `CLAUDE.md` of the
repository the session ran in (luthier and sonolocalización: 2026-10-06); (ii) `~/.claude/CLAUDE.md`
(global, 2026-10-06 for P12); (iii) a memory note of that project stating it (memory is per project:
sonolocalización's note on hardcoding, which states P11, existed by 2026-09-11; luthier's memory
never stated it); (iv) the principle in the agent's context earlier in the same session (D3).
- Recommended: all four. A principle can then be operative in one repository and not in the other
  on the same day, which gives cases of a natural experiment.
    OK


**D3. How is exposure in the session found?** (GPT, problem 2: a lexical overlap is too fragile to
decide the main dataset; a principle can be conveyed without its words, and words can recur without
it.)
- The lexical overlap stays, only as a flag that points at turns worth reading.
- For the pairs (case, principle) that would enter the scoring, and only those, a judge reads the
  session up to the decision with the list of that case's eligible principles and says, per
  principle, `none`, `possible` or `explicit`, quoting the turn. This judge sees principles and is
  never the drafter or the scorer. One call per case, about 40.
- Luciano checks the `possible` and `explicit` answers in his review (D9).
- Main result: `none` only. `possible` goes to a sensitivity analysis.

ok


**D4. When is a principle scored?** (Changed, GPT, problem 7.) By its number of approved independent
cases, n: n < 5 is reported as anecdotal, 5 to 9 as exploratory, 10 or more as scored. All are shown
with their n; only the last kind gets a percentage in the summary table. The thresholds are
parameters, fixed now.
      porque vestir un numero entendible con umbrales arbitrarios? Dejemos el numero y listo. 



**D5. Kinds of decision.** `luciano_choice` and `luciano_confirmation` in the main result, reported
apart from each other; `model_margin` apart.
   ok
 

**D6. Units with private words.** Twelve of the 409 units mined so far; their texts are withheld from
the repository. Recommended: leave them out now; a local-only run later if the counts are too small.
   ok



**D7. The drafter sees the diff**, as evidence stored with the case; the options sent to the scorer
are a separate abstraction, which Luciano's approval checks (GPT).

                 ok

**D8. Constructed alternatives** leave the main result (GPT).
  ok



**D9. The sample Luciano reviews.** (Changed, GPT, problem 4.) Forty cases drawn with a recorded
seed, stratified (language and method, choice and confirmation, both repositories, every reversal),
drawn and frozen before he sees any of them. He reviews exactly those forty. The approved subset is
the experiment: no replacement of rejected cases, by any rule. If 21 survive, n is 21.
- His marks are committed verbatim; a script turns `ok` into `approved: true`; nothing else sets
  it. A correction creates a new case with his text, which enters as his.
- Cost: about forty minutes of his reading, once.
  ok



**D10. Batched calls, with the rule fixed now.** (Changed, GPT, problem 8.) Each principle runs on all
its eligible cases in one call. Before any answer is compared with an outcome, ten cases drawn with
a recorded seed are run one per call, and the answers alone (not the outcomes) are compared. If they
agree on at least 90% of the cases, the batched run stands; if not, it is discarded and everything
runs one case per call.
ok


**D11. Who runs it.** Recommended: Luciano authorizes the model to run the drafting and the exposure
judge (long, mechanical to follow); Luciano runs the scoring, after his review.
ok


**D12. Which sessions.** Luthier and sonolocalización now; macro_dr's DSL and macroir later, if the
counts call for them.
ok


**D13. Baselines that a principle has to beat.** (New, GPT, problem 5: a model given any rule may do
better than one given none.)
- B0, no principle: "Which option is better supported by the information given? If it does not
  discriminate, answer NEITHER."
- B1, an unrelated principle: each case is also run with another real principle drawn at random
  among those not eligible for it.
- B2, shuffled: the statements of the principles are permuted among their ids, and the whole scoring
  is run again; this gives how much any normative sentence "predicts".
- The comparison that counts is the target principle against B1 and B2. B0 is reported for scale.
ok



**D14. How a case is read after scoring.** (New, GPT, problem 6.) Per case and principle: the target
picked the option chosen; it picked the other option while another principle picked the one chosen
(it lost a conflict); it picked the other option and no principle picked the one chosen; it answered
NEITHER. Luciano's review may add, per case, a known tradeoff in his words, without naming a
principle. The report is a table of these four outcomes per principle, with the conflicts named.
ok

## What it will cost

| step | model calls | Luciano's attention |
|---|---|---|
| mine the decisions | none | none |
| dates of the principles | none (explicit and operative are found mechanically) | one screen: 14 entries |
| draft the cases | one per candidate unit, 100 to 200 | none |
| exposure judge | about 40 | inside the review |
| review the sample | none | forty cases, about forty minutes |
| score | about 30 per run (target, B1, B2 in both orders), plus the subset of D10 | one screen of results |
