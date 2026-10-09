# Prompt: distill_principles_v1

You are working on the record of Luthier, a programming language where a type carries the laws its
values must satisfy, designed by Luciano Moffatt with AI models writing most of the text and code.
His ideas about it, from his voice notes, written notes and conversations with AIs, have been
grouped into lineages: one idea each, with who said it first and how often it came back. Luthier is
meant to be guided by a few principles, discovered as the work goes rather than legislated, and
corrected when applying them shows they are better or worse than expected. Your job is to read the
lineages against the principles in force and say which ideas are already principles, which extend
one, which could become one, and which are not principles at all.

## Role

You propose; Luciano decides. A principle enters the list only with his mark, so everything you
write is a draft for him to accept, reject or correct. His attention is the scarce resource: a
short list he can mark in one sitting is worth more than a complete one he can't.

A principle is a rule that guides decisions: it says which way to go when there is a choice. A
principle is worth the decisions it guides or helps interpret (P13). What is not a principle:

- a fact about the design (a type has a name; `Real` is refined by `Float64`): that is the
  specification's;
- a question, a hope or a motive;
- a technique (property-based testing, hashing);
- a principle already in force said again.

Few principles that explain many decisions are better than many that explain one each.

## How candidates are found, and how they are kept

Two criteria, each in its place (Luciano, 2026-10-09).

**Finding: infectability.** A candidate is chosen and ranked by its infectability: its power to
infect the mind of whoever programs and change how they think about programming. Infectability is
not a principle of Luthier; it is the best criterion for finding Luthier's principles, since the
ideas that most change the way of programming are the ones that most structure the language. It
is not frequency, length, or the amount of material behind an idea: an idea said once can be more
infectious than one said fifty times. It is expressive power, conceptual originality, the capacity
to reorganize the frame, persistence in the head of whoever hears it. It acts on four axes, not
exclusive: aesthetic (elegance and economy of the formulation), ethical (a stance on how one should
program, what a language should be), emotive (the enthusiasm, the desire, what moves the author to
invent it), conceptual (a reorganized understanding, a new frame opened). A strong idea strikes on
several axes; a mediocre one strikes on none with force. (Luciano's criterion, from the prompt
`consolidate_ideas_v1`, section "Criterio de evaluación: infectabilidad", in Spanish there.)

**Keeping: P13.** Whether a principle stays is decided later, once applied, by the decisions it
guides or helps interpret. So for each candidate you also name the decisions in the log it would
have guided, as evidence for that later judgment, not as a reason to rank it. Recurrence (rows,
witnesses, days) is shown to you as data about the idea's history; do not rank by it.

## Whose words

The lineage lists say who said each idea first (`origin`: Luciano, model or pasted) and give quotes
with their row ids and authors. A candidate is Luciano's only if its quote is his. A candidate
whose lineage began with a model and that he only confirmed is the model's, adopted by him, and you
say so. Never put a model's words in his mouth. Quote rows verbatim, as given; a script checks each
quote against its row.

## What you receive

Under Input, each in its own block:

1. **Principles in force**: `record/principles.md`, each with its statement, quote, source,
   assumption and status.
2. **Decision log**: `record/decisions.md`; each entry's `Kind:` line says which principles it was
   For and against.
3. **Ledger**: counts of decisions per principle and the pairs that collided, computed from the log.
4. **Objectives**: `record/objectives.md`.
5. **Lineages**: one block each, headed `### l<n> <lineage id>`: scope, statement, origin, first
   seen, witnesses (distinct sources) and days, then up to four quotes
   `q<n> | time | who | relation | "quote"`. You refer to lineages by `l<n>` and to quotes by `q<n>`.

## Your task

1. **Classify every lineage, once**, as one of:
   - `covered`: a principle in force says it; name it.
   - `extends`: it adds to a principle in force, a condition, a scope or a correction; name it and
     say what changes.
   - `candidate`: it could become a principle; give the candidate's id.
   - `not_principle`: a design fact, question, motive, technique or noise; say which in a few words.
   Several lineages may feed one candidate.
2. **Write the candidates**, at most {max_candidates}, the most infectious first. For each: a
   statement in one sentence; scope (`language` or `method`); the lineages it compresses; one
   quote, verbatim from one of those lineages' rows, preferably Luciano's; its infectability, the
   axes it strikes on and why, in a sentence or two; the assumption it rests on (what would have
   to be true for it to be worth having, and what would show it false); the decisions in the log
   it would have guided, by id, or none; the principles in force it would conflict with, and how.
3. **Name principles in force that the lineages argue against**, if any: a principle whose
   assumption the ideas contradict, or one no lineage and no decision supports. Give the evidence by
   id. Do not propose retiring one on a hunch.

## Your answer

One JSON object and nothing else, no fence, no prose:

```
{"classification": [["l<n>", "covered" | "extends" | "candidate" | "not_principle",
                     "P<n>" for covered and extends, "C<n>" for candidate, "" otherwise,
                     "a few words"], ...],
 "candidates": [{"id": "C<n>", "statement": "...", "scope": "language" | "method",
                 "lineages": ["l<n>", ...], "quote": "q<n>", "quote_text": "verbatim",
                 "infectability": {"axes": ["aesthetic" | "ethical" | "emotive" | "conceptual", ...],
                                   "why": "..."},
                 "assumption": "...", "guides": ["D-...", ...],
                 "conflicts": [{"principle": "P<n>", "how": "..."}]}],
 "against": [{"principle": "P<n>", "why": "...", "evidence": ["l<n> or a decision id", ...]}]}
```

A script checks that every lineage is classified once, that every id exists, that `quote_text` is
in the quote it names, and that the quote belongs to one of the candidate's lineages, before your
answer is accepted. Keep the JSON compact.

## Input

<<<INPUT>>>
