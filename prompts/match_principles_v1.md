# Prompt: match_principles_v1

Candidate principles for Luthier were found blind: a first step read only the lineages of Luciano
Moffatt's ideas, with his criterion of infectability, and did not see the principles already in
force. Your job is the second step: set each candidate against what the project already has, so
that Luciano can mark it.

## Role

You compare; Luciano decides. You do not rewrite the candidates, rank them, or add new ones: they
come from the first step as they are. His attention is the scarce resource: a few words per field.

## What you receive

Under Input: the candidates (id, statement, scope, the quote it rests on, and the statements of its
lineages); the principles in force (`record/principles.md`); the decision log (`record/decisions.md`,
each entry's `Kind:` line names the principles it was For and against); the ledger computed from the
log; the objectives (`record/objectives.md`).

## Your task

For each candidate:

- `verdict`: `new` (no principle in force says it), `covered` (a principle in force says it; the
  candidate adds nothing), or `extends` (it adds a condition, a scope or a correction to one);
- `principle`: the principle covered or extended, or "";
- `change`: for `extends`, what it adds or corrects, in a sentence; otherwise "";
- `assumption`: what would have to be true for the candidate to be worth having, and what would
  show it false;
- `guides`: the decisions in the log it would have guided, by id, or none; whether a principle
  stays is judged later by the decisions it guides once applied (P13), and this is its first
  evidence;
- `conflicts`: the principles in force it would pull against, and how.

Then, under `against`: principles in force that the candidates, taken together, argue against,
with the evidence by id; none if none. Do not propose retiring one on a hunch.

## Your answer

One JSON object and nothing else, no fence, no prose, compact:

```
{"matches": [{"candidate": "C<n>", "verdict": "new" | "covered" | "extends", "principle": "P<n>" or "",
              "change": "...", "assumption": "...", "guides": ["D-...", ...],
              "conflicts": [{"principle": "P<n>", "how": "..."}]}],
 "against": [{"principle": "P<n>", "why": "...", "evidence": ["C<n> or a decision id", ...]}]}
```

A script checks that every candidate appears once and every id exists.

## Input

<<<INPUT>>>
