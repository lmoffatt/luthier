# Prompt: apply_principle_blind_v1

Below is a principle and a numbered list of decisions, each a question with two options, A and B.
For each decision, say which option follows more directly from the principle. If the principle does
not bear on the choice, or does not tell the two options apart, answer NEITHER.

Judge each decision on its own, from the principle and the question alone; the order of the list
means nothing, and your answer to one decision must not depend on your answers to the others. Do
not use anything you may know about who took these decisions or how they turned out.

## The principle

{principle}

## Your answer

One JSON object and nothing else, no fence, no prose:

```
{"answers": [{"case": <number>, "choice": "A" | "B" | "NEITHER", "confidence": <0 to 1>, "reason": "a few words"}]}
```

Every decision of the list appears once.

## The decisions

<<<INPUT>>>
