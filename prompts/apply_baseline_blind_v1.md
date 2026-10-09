# Prompt: apply_baseline_blind_v1

Below is a numbered list of decisions, each a question with two options, A and B. For each decision,
which option is better supported by the information given? If the information does not discriminate
between them, answer NEITHER.

Judge each decision on its own; the order of the list means nothing, and your answer to one decision
must not depend on your answers to the others. Do not use anything you may know about who took these
decisions or how they turned out.

## Your answer

One JSON object and nothing else, no fence, no prose:

```
{"answers": [{"case": <number>, "choice": "A" | "B" | "NEITHER", "confidence": <0 to 1>, "reason": "a few words"}]}
```

Every decision of the list appears once.

## The decisions

<<<INPUT>>>
