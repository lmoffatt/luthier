# Prompt: draft_decision_case_v1

You reconstruct one decision from the record of a project. Luciano Moffatt directs the project and
AI models write most of its code and documents. Below is one moment of a working session: what the
model said just before his turn, his turn, what the model said just after, and what was then changed
in the files. Your job is to say whether a decision between real alternatives was taken here, and if
so, to state it as a question with two options, for a later reader who will not see this session.

## What counts as a decision

A choice that could have gone another way and that shapes the project: what the language is or how
it works, how the work is organized, what is kept or dropped, what is tried first. Not a decision:
running a command, committing, reading a file, fixing a typo, a request for information, carrying out
a step already decided earlier in the session. When you hesitate, answer that there is no decision;
a missing case costs less than a false one.

## The two options

- One option is what was done here. The other is the strongest alternative that was genuinely
  available at that moment: one that someone in the session proposed or weighed, or that the context
  plainly offered. Not a foil: an option a reasonable person in that session could have chosen.
- Write both in parallel wording, of similar length and tone, neither more reasonable-sounding than
  the other. Do not label which one was done inside the options or the question.
- The question names the choice neutrally, as it stood before it was made. No dates, no names of
  files or sessions, no word that reveals which option won.
- Say how you know the alternative: `explicitly_discussed` (someone in the session put it forward),
  `strongly_implied` (the context makes it the obvious other road, though nobody named it),
  `constructed` (you had to build it).

## Who decided

- `luciano_choice`: Luciano chose between options, or said in his own words what to do.
- `luciano_confirmation`: Luciano accepted what the model had proposed ("ok", "dale", "si", "acepto")
  without adding anything that changes it; the decision is his, the idea is the model's.
- `model_margin`: the model acted on its own; Luciano's turn did not ask for what was done.

## Evidence

Every evidence field is a quote, verbatim, from the material below (words you skip are marked
"..."). A script checks each one against the material. `evidence_counterfactual` may be empty only
when the alternative is `constructed`.

## Your answer

One JSON object and nothing else, no fence, no prose:

```
{"is_decision": true | false,
 "reason_if_not": "a few words, when is_decision is false",
 "question": "...",
 "alternatives": ["...", "..."],
 "chosen_index": 0 | 1,
 "counterfactual_status": "explicitly_discussed" | "strongly_implied" | "constructed",
 "evidence_chosen": "verbatim",
 "evidence_counterfactual": "verbatim, or empty when constructed",
 "decided_by": "luciano_choice" | "luciano_confirmation" | "model_margin",
 "evidence_decided_by": "verbatim"}
```

When `is_decision` is false, the other fields may be empty.

## The moment

<<<INPUT>>>
